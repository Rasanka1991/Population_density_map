# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:47:05 2023

@author: Francisco
"""
from flask import Flask
from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
from pyproj import CRS, Proj, transform

# establishing the connection

DB_CONFIG = {
    "database": "test",
    "username": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"}

# Create a flask application
app = Flask(__name__)

username = DB_CONFIG['username']
password = DB_CONFIG['password']
host = DB_CONFIG['host']
port = DB_CONFIG['port']
database = DB_CONFIG['database']

database_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"
conn = database_uri
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
engine = create_engine(conn)
sql = 'SELECT geometry as geom, pop_density FROM shp_prt'

print('#### PLOTING A BEUTIFULL MAP JUST FOR YOU ####')
ctry = gpd.read_postgis(sql, con = engine)
with plt.style.context(("seaborn", "ggplot")):
    ctry.plot(column ='pop_density', cmap = 'YlOrRd', figsize=(10,5),
               legend= True,
               edgecolor="black",
               scheme='natural_breaks', 
               k=7, 
               legend_kwds={'loc': 'center left', 'title': 'Population Density (people/sq Km)','fontsize':12,'frameon':True, 'bbox_to_anchor':(1,0.5)})




plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Population Density Map")
plt.savefig('population_density_ctry.jpg')

if __name__ == '__main__':
    
    app.run(debug=True)