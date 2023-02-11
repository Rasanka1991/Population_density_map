# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 15:40:55 2023

@author: Francisco
"""


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
import psycopg2
from sqlalchemy import create_engine
from pyproj import CRS, Proj, transform
import os

cw = os.getcwd()


#set correct directory
#pyproj.datadir.set_data_dir("C:\\Users\\Francisco\\miniconda3\\envs\\project-env\\Library\\share\\proj")


#####################################################################################################################EXTRACT AND TRANSFORM DATA#####################################################################################################################################

# # Data aquisition (population data from the web)
data = pd.read_html('https://citypopulation.de/php/argentina-admin.php')[0]
data = data.iloc[0:,:]

print("#### AQUIRING DATA ####")

# #select just the colums i want/need
data = data[['Name','Status','Population Census 2022-05-18']]

print('##### SELECTING THE RIGHT COLUMNS #####')

# #change the name of a column
data.rename(columns = {'Population Census 2022-05-18':'Population'}, inplace = True)

print('##### RENAMING SOME COLUMNS #####')

# #filter rows by value
data = data.loc[data['Status'] == 'Province']

print('##### FILTERING DATA #####')

# #Create empty column
data['District'] = ''
data['Pop_density'] = ''

print('##### CREATING NEW COLUMNS #####')

# #For loop to clean the data and add in the new column
for index, row in data.iterrows():
    if '('and ')' in row['Name']:
        start_index = row['Name'].find('')
        end_index = row['Name'].find('(')
        data.loc[index,'District'] = data.loc[index]['Name'][start_index:end_index -1]
        
    else:
        data.loc[index,'District'] = data.loc[index]['Name']

# # Transforming the population columns into int    
for index, row in data.iterrows():
    data.loc[index,'Pop_density'] = int(data.loc[index]['Population'])
    
######################################################################################################################################### LOAD DATA INTO DATABASE  ##############################################################################################
print('#### CONECTING WITH THE DATA BASE ####') 
user = "postgres"
password = "postgres"
host = "localhost"
port = 5432
database = "test"
 
conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conn)
  
#Import shapefile to databse
data.to_sql('data', conn, if_exists= 'append')
 
print("#### THE CONNECTION WITH THE DATA BASE WAS ESTABLISHED ####")


#################################################################################################################EXTRACT AND TRANSFORM THE SHAPEFILE ########################################################################################################

# #Reading data from the shapefile
shp_loc= os.path.join(cw, 'static','data','data')
ctry = gpd.read_file(os.path.join(shp_loc,'ARG_adm1.shp'))


print('#### READING SHAPEFILE ####')
    
# # to select only the columns i want from prt shapefile
ctry =ctry[['NAME_1','geometry']] 

print('##### SELECTING THE RIGHT COLUMNS OF THE SHAPEFILE #####')

# #change the name of the columns of the shapefile
ctry.rename(columns = {'NAME_1': 'District'}, inplace =True)

print('##### RENAMING SOME COLUMNS OF THE SHAPEFILE #####')


#Reprojection of the coordinate system (change degrees to meters to calculate the area of the polygons in squared meters)
ctry.to_crs(epsg=6893, inplace =True)

print("#### ASSIGNING THE RIGHT COORDINATE SYSTEM ####")

# #Replace the names misspelled (do it do whenever necessary) put this code above the for loop
#population_data.replace('Lisbon', 'Lisboa', inplace = True)

# #crosschecking shapefile + data from website 
i=0
for index, row in ctry['District'].iteritems():
    if row in data['District'].tolist():
        pass
    else:
        print('The district ', row, 'is not in the population_data list')
        i+= 1
        

# #Create a new column in shapefile to calculate the area of the district
ctry['area'] = ctry.area/1000000

# #attreibute match (join)
print("#### MATCHING THE INFORMATION FROM DATA WITH THE SHAPEFILE ####")
ctry = ctry.merge(data, on='District')

# #Create a population density column
print('#### CALCULATING THE POPULATION DENSITY ####')
ctry['pop_density (people/sq Km)'] = ctry['Pop_density']/ctry['area']

##########################################################################################################################LOAD THE SHAPEFILE INTO DATABASE#####################################################################################################
# #Load Shapefile into the Data Base 

print('#### CONECTING WITH THE DATA BASE ####') 

user = "postgres"
password = "postgres"
host = "localhost"
port = 5432
database = "test"
 
conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conn)
 
# #Import shapefile to databse
ctry.to_postgis(name="shp", con=engine, if_exists= 'append', schema="public")
 
print("#### THE CONNECTION WITH THE DATA BASE WAS ESTABLISHED ####")

#####################################################################################################PLOTING DENSITY POPULATION MAP###############################################################################################################################

print('#### PLOTING A BEUTIFULL MAP JUST FOR YOU ####')
with plt.style.context(("seaborn", "ggplot")):
    ctry.plot(column ='pop_density (people/sq Km)', cmap = 'YlOrRd', figsize=(10,5),legend= True, edgecolor="black",scheme='natural_breaks', k=7, legend_kwds={'loc': 'center left', 'title': 'Population Density (people/sq Km)','fontsize':12,'frameon':True, 'bbox_to_anchor':(1,0.5)})


plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Population Density Map")
plt.savefig('population_density_ctry.jpg')