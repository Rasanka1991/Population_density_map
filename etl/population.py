import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from pyproj import CRS, Proj, transform
import psycopg2
import os
import yaml


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

data=read_config('config.yml')

user= data['username']
password = data['password']
host = data['host']
port = data['port']
database = data['database']


# Set paths for working and data directories
cw = os.getcwd()
data_location = os.path.join(cw,'static','data')


print('#### READING SHAPEFILE ####')
ctry = gpd.read_file(os.path.join(data_location,'EU_Merge.shp'))


print("#### SET THE COORDINATE SYSTEM WGS84 ####")
#Define the coordinate system
ctry = ctry.set_crs("EPSG:4326")


print("#### REPROJECT TO ESRI:102013 ####")
#Reproject the coordinate system to change degrees to meters to calculate the area of the polygons in squared meters
ctry = ctry.to_crs("ESRI:102013")

      
print('#### CALCULATE THE POLYGON AREA #####')
#Create a new column in shapefile to calculate the area of the district
ctry['area'] = (ctry.area)/1000000


print('#### CALCULATING THE POPULATION DENSITY ####')
# Create a population density column and calculate population density(person per squre kilometer)
ctry['pop_density'] = ctry['Population']/ctry['area']


print('#### SELECTING THE RIGHT COLUMNS OF THE SHAPEFILE #####')
#Required Colum selection
ctry =ctry[['NAME','Type','NAME_1','Population','pop_density','area','geometry']] 
#Load Shapefile into the Data Base  


print('#### REPROJECT TO WGS84 ####') 
#Reproject again to WGS84 for display on leafleat map
ctry= ctry.to_crs("EPSG:4326")


print('#### CONECTING WITH THE DATA BASE ####')
#Conection establish to the database
conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conn)
print("#### THE CONNECTION WITH THE DATA BASE WAS ESTABLISHED ####") 


#Load Shapefile into the Data Base
ctry.to_postgis(name="eu_merge", con=engine, if_exists= 'replace', schema="public")
print("#### THE DATA WAS STORED IN POSTGRES DATABASE ####")   


#Add primary key to the table
sql_query_1= " ALTER TABLE eu_merge ADD COLUMN id SERIAL PRIMARY KEY "
with psycopg2.connect(conn) as conn:
    with conn.cursor() as curs:
        curs.execute(sql_query_1)
        conn.commit()
        curs.close()
print("#### PRIMARY KEY ADDED TO THE DATABASE ####")
