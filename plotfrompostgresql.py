# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:47:05 2023

@author: Francisco
"""

from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
from pyproj import CRS, Proj, transform

# establishing the connection

user = "postgres"
password = "postgres"
host = "localhost"
port = 5432
database = "test"
 
conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conn)
sql = 'SELECT geometry as geom, pop_density FROM shp_aus'

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