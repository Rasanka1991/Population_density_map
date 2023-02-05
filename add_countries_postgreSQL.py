""" 
This code adds the countries of the world stored in a GeoJson file to a new PostgreSQL Table.
Replace the line 23 with your own Postgress SQL username,password and database (Should be a postGIS enabled database, execute ).


The code structure is as follows,
engine = create_engine('postgresql://username:password@localhost:5432/database')

"""

import geopandas
import pandas 
from sqlalchemy import create_engine
import pyproj 


#set the table name in the database
TABLE = "countries"

#url where the geojson file is located
url_countries = "https://opendata.arcgis.com/datasets/ac80670eb213440ea5899bbf92a04998_0.geojson"


#convert the geojson file to geodataframe
gdf = geopandas.read_file(url_countries)

#set the connection the the database
engine = create_engine('postgresql://postgres:123@localhost:5432/population_density')

#load the geodataframe created to PostGIS
gdf.to_postgis(
    con=engine,
    name=TABLE,
)
