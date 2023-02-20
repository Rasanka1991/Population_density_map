from flask import Flask, render_template, request
import pandas as pd
import os
from sqlalchemy import create_engine, text
import geopandas as gpd
import psycopg2
import json

statics_folder = os.path.join('static')

#create Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = statics_folder


#Connect to postgres SQL database
def get_data(country_name):
   # establishing the connection

   DB_CONFIG = {
      "database": "project",
      "username": "postgres",
      "password": "postgres",
      "host": "localhost",
      "port": "5432"}


   username = DB_CONFIG['username']
   password = DB_CONFIG['password']
   host = DB_CONFIG['host']
   port = DB_CONFIG['port']
   database = DB_CONFIG['database']

   database_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"
   conn = database_uri
   engine = create_engine(conn)
   

   sql_query = f'''SELECT jsonb_build_object(
    'type', 'FeatureCollection', 
    'features', jsonb_agg(features.feature)
   )
   FROM ( 
   SELECT jsonb_build_object(
      'type',       'Feature',
      'id',         id,
      'geometry',   ST_AsGeoJSON(geometry)::jsonb,
      'properties', to_jsonb(inputs) - 'id' - 'geometry' - 'country' - 'POP_DEN' -'District'
   ) AS feature
   FROM (SELECT   e.id, e.geometry, "NAME", "pop_density", "NAME_1"
      FROM eu_merge as e
      WHERE ("NAME" = '{country_name}')
   ) inputs) features'''  

   feature_collection_data = pd.read_sql_query(sql=text(sql_query), con=engine.connect())
   feature_collection_dict_data = feature_collection_data.iloc[0]['jsonb_build_object']
   population_feature_collection = json.dumps(feature_collection_dict_data)

   return population_feature_collection





@app.route('/', methods =["GET", "POST"]) 
#importing flask and creating a home route which has both get and post methods
def gfg():
    if request.method == "POST": #if requesting method is post, we get the input data from HTML form
       # Getting the country name
       country_name = request.form.get("country_name")
       #print(country_name)       
       
       population_json=get_data(country_name)

       #render the output html with the population density map
       return render_template("output.html",country_name=country_name, statics_folder = statics_folder, population_json = population_json )

    else:
      #render the input page
      return render_template("input.html", statics_folder = statics_folder )



if __name__=='__main__':
   app.run(debug=True)