from flask import Flask, render_template, request
import pandas as pd
import os
from sqlalchemy import create_engine, text
import geopandas as gpd

statics_folder = os.path.join('static')

#create Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = statics_folder


#Connect to postgres SQL database
def get_data(country_name):
   username = "postgres"
   password = "postgres"
   host = "localhost"
   port = 5432
   database = "project"

   database_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"
   conn = database_uri
   app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
   engine = create_engine(conn)

   with engine.begin() as connection: 
      ctry = gpd.read_postgis(
         sql=text(fr'SELECT geometry as geom, pop_density FROM eu_mergre WHERE NAME = {country_name}'),
         con=connection,
      )
   return ctry


@app.route('/', methods =["GET", "POST"]) 
#importing flask and creating a home route which has both get and post methods
def gfg():
    if request.method == "POST": #if requesting method is post, we get the input data from HTML form
       # Getting the country name
       country_name = request.form.get("con")
       print(country_name)
       
       
       ctry=get_data(country_name)

       print('data recieved')
       #render the output html with the population density map
       return render_template("output.html",ctry )

    else:
      #render the input page
      return render_template("input.html", statics_folder = statics_folder )



if __name__=='__main__':
   app.run(debug=True)