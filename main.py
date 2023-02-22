from flask import Flask, render_template, request,flash
import pandas as pd
import os
from sqlalchemy import create_engine, text
import geopandas as gpd
import psycopg2
import json
import yaml

static_folder = os.path.join('static')

#create Flask application
app = Flask(__name__)
app.secret_key = "abc" 

app.config['UPLOAD_FOLDER'] = static_folder

def read_config(fname: str) -> dict:
   """ Reads the configuration file

   Args:
      fname (str): the configuration file

   Returns:
      dict: a dictionary with the configuration
   """
   try:
      with open(fname) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
   except yaml.YAMLError as err:
      print(err)
   return data


#Connect to postgres SQL database
def get_data(country_name, data):
   # establishing the connection

   user= data['username']
   password = data['password']
   host = data['host']
   port = data['port']
   database = data['database']

   database_uri = f"postgresql://{user}:{password}@{host}:{port}/{database}"
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
def pop():
    if request.method == "POST": #if requesting method is post, we get the input data from HTML form
       # Getting the country name
       error= None
       country_name = request.form.get("country_name")
              
       data=read_config('config.yml') #read .yml file to get pgadmin credentials
       population_json=get_data(country_name, data) #query postgre to get data for the selected country

       if country_name != "":
         return render_template("output.html",country_name=country_name, static_folder = static_folder, population_json = population_json)
       
       else:
         error= "Please select a country!"
         return render_template("input.html", static_folder = static_folder, error=error )

    else:
      #render the input page
      return render_template("input.html", static_folder = static_folder)


if __name__=='__main__':
   app.run(debug=True)