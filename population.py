import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
import psycopg2
from sqlalchemy import create_engine
from pyproj import CRS, Proj, transform
import os

# #Reading data from the shapefile
cw = os.getcwd()
data_location = os.path.join(cw,'static','data')

ctry = gpd.read_file(os.path.join(data_location,'EU_Merge.shp'))

print('#### READING SHAPEFILE ####')
    

#Reprojection of the coordinate system (change degrees to meters to calculate the area of the polygons in squared meters)
ctry = ctry.to_crs('+proj= merc')

print("#### ASSIGNING THE RIGHT COORDINATE SYSTEM ####")


#to select only the columns i want from shapefile
ctry =ctry[['NAME','NAME_1','Population','geometry']] 

print('##### SELECTING THE RIGHT COLUMNS OF THE SHAPEFILE #####')

        
# #Create a new column in shapefile to calculate the area of the district
ctry['area'] = ctry.area/1000000


# #Create a population density column
ctry['pop_density'] = ctry['Population']/ctry['area']

print('#### CALCULATING THE POPULATION DENSITY ####')


# #Load Shapefile into the Data Base 
print('#### CONECTING WITH THE DATA BASE ####') 

user = "postgres"
password = "postgres"
host = "localhost"
port = 5432
database = "project"
     
conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conn)

ctry.to_postgis(name="eu_mergre", con=engine, if_exists= 'replace', schema="public")

print("#### THE CONNECTION WITH THE DATA BASE WAS ESTABLISHED ####")