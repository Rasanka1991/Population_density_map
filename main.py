from flask import Flask, render_template, jsonify, request, redirect
#from flask_sqlalchemy import SQLAlchemy
import psycopg2 
import osgeo.ogr
import pandas as pd
import json
import os



#get bottom type geojson from inputted coordinates
def get_country_data(country_name,connection):
   """ Query and select population density data from the database, store it in a dataframe and convert it to geojson

      Args:
            country_name(text): a text of country name
            connection (string): credentials and connection to the database

      Returns:
            results from the query in json format
   """
   #query that gives a Feature Collection object with population densities in each administrative boundary
   query_country_2 = f'''SELECT jsonb_build_object(
      'type',     'FeatureCollection',
      'features', jsonb_agg(features.feature)
   )
   FROM (
   SELECT jsonb_build_object(
      'type',       'Feature',
      'id',         FID,
      'geometry',   ST_AsGeoJSON(geometry)::jsonb,
      'properties', to_jsonb(inputs) - 'FID' - 'geometry'
   ) AS feature
   FROM (SELECT b.FID, b.country, b.geometry
      FROM countries AS b
      WHERE country (b.country= country)) inputs) features'''



   query_country = f'''SELECT row_to_json(f) As feature 
     FROM (SELECT 'Feature' As type \
     , ST_AsGeoJSON('GEOM')::json As geometry \
     , row_to_json((SELECT l FROM (SELECT fid AS feat_id) As l)) As properties \
     FROM countries As l WHERE l.country = country) As f'''

   #Reads the query and store it in a dataframe
   feature_collection_country = pd.read_sql(query_country, connection)

   #Getting geojson dictionary by calling iloc[0] on the jsonb_build_object column
   feature_collection_dict_country = feature_collection_country.iloc[0]['jsonb_build_object']

   #Converting to geojson to return to the fransisco's code
   pop_density_feature_collection = json.dumps(feature_collection_dict_country)
   print("country_feature_collection created")

   return  pop_density_feature_collection

#get connection to the Postgres database
def get_db_connection():
   """ Creates a connection to the database

      Returns:
            the connection to the database
   """
   connection = psycopg2.connect(database="population_density", user="postgres", password = "123")
   return connection


statics_folder = os.path.join('static')


#create Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = statics_folder


@app.route('/', methods =["GET", "POST"]) #importing flask and creating a home route which has both get and post methods
def gfg():
    if request.method == "POST": #if requesting method is post, we get the input data from HTML form
       # Getting the country name
       country_name = request.form.get("con")
       print(country_name)

      #connecting to the database
       connection = get_db_connection()
       cursor = connection.cursor()

       # getting the separate data types to display on the map
       data_to_map = get_country_data(country_name,connection)

       #Send data to the fransisco python script to get the population density map


       #Get the population density map
       A_map= 2


       #render the output html with the population density map
       return render_template("output.html", map = A_map)

    else:
      #render the input page
      return render_template("input.html", statics_folder = statics_folder )



if __name__=='__main__':
   app.run()