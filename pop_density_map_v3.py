# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 17:03:42 2023

@author: Francisco
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
import psycopg2
from sqlalchemy import create_engine
from pyproj import CRS, Proj, transform

URL_arg = 'https://citypopulation.de/php/argentina-admin.php'
URL_prt = 'https://citypopulation.de/en/portugal/admin/'
URL_ger = 'https://citypopulation.de/en/germany/admin/'
URL_aus = 'https://citypopulation.de/en/austria/admin/'

x = int(input("""Choose the country that you want to plot?
          1- Argentina
          2-Portugal
          3-Germany
          4-Austria
          """))
#######################################################################################################ETL Data + Shapefile#####################################################################################################################################
# # Data aquisition (population data from the web)
if x ==1:
    data = pd.read_html(URL_arg)[0]
    data = data.iloc[0:,:]
elif x ==2:
    data =pd.read_html(URL_prt)[0]
    data = data.iloc[0:,:]
elif x ==3:
    data = pd.read_html(URL_ger)[0]
    data = data.iloc[0:,:]
elif x ==4:
    data = pd.read_html(URL_aus)[0]
    data = data.iloc[0:,:]
else:
    print("YOU MUST CHOOSE A NUMBER BETWEEN 1 AND 4... WE'RE WORKING HARD TO HAVE MORE COUNTRIES AVAILABLE")

print("#### AQUIRING DATA ####")

# #select just the colums i want/need
if x ==1:
    data = data[['Name','Status','Population Census 2022-05-18']]
elif x ==2:
    data = data[['Name','Status','Population Census 2021-03-22']]
elif x==3:
    data = data[['Name','Status','Population Estimate 2021-12-31']]
elif x ==4:
    data= data[['Name','Status','Population Estimate 2022-01-01']]
else:
    print("We're facing a problem... Try again!")

print('##### SELECTING THE RIGHT COLUMNS #####')

# #change the name of a column
if x == 1:
    data.rename(columns = {'Population Census 2022-05-18':'Population'}, inplace = True)
elif x == 2:
    data.rename(columns = {'Population Census 2021-03-22':'Population'}, inplace = True)
elif x == 3:
    data.rename(columns = {'Population Estimate 2021-12-31':'Population'}, inplace = True)
elif x == 4:
    data.rename(columns = {'Population Estimate 2022-01-01':'Population'}, inplace = True)
else:
    print("We're facing a problem... Try again!")
    
    
print('##### RENAMING SOME COLUMNS #####')

# #filter rows by value
if x == 1:
    data = data.loc[data['Status'] == 'Province']
elif x == 2:
    data = data.loc[data['Status'] == 'District'] 
elif x == 3:
    data = data.loc[data['Status'] == 'State']
elif x == 4:
    data = data.loc[data['Status'] == 'State']
else:
    print("We're facing a problem... Try again!")

print('##### FILTERING DATA #####')

# #Create empty column
data['District'] = ''
data['Pop_density'] = ''
if x == 1:
    data['Country'] = 'Argentina'
elif x ==2:
    data['Country'] = 'Portugal'
elif x ==3:
    data['Country'] = 'Germany'
elif x ==4:
    data['Country'] = 'Austria'
else:
    print("We're facing a problem... Try again!")


    

print('##### CREATING NEW COLUMNS #####')

# #For loop to clean the data and add in the new 
if x == 1:
    for index, row in data.iterrows():
        if '('and ')' in row['Name']:
            start_index = row['Name'].find('')
            end_index = row['Name'].find('(')
            data.loc[index,'District'] = data.loc[index]['Name'][start_index:end_index -1]
            
        else:
            data.loc[index,'District'] = data.loc[index]['Name']
elif x == 2:
    for index, row in data.iterrows():
        if '['and ']' in row['Name']:
            start_index = row['Name'].find('')
            end_index = row['Name'].find('[')
            data.loc[index,'District'] = data.loc[index]['Name'][start_index:end_index -1]
            
        else:
            data.loc[index,'District'] = data.loc[index]['Name']
elif x == 3:
    for index, row in data.iterrows():
        if '['and ']' in row['Name']:
            start_index = row['Name'].find('')
            end_index = row['Name'].find('[')
            data.loc[index,'District'] = data.loc[index]['Name'][start_index:end_index -1]
            
        else:
            data.loc[index,'District'] = data.loc[index]['Name']
elif x == 4:
    for index, row in data.iterrows():
        if '['and ']' in row['Name']:
            start_index = row['Name'].find('')
            end_index = row['Name'].find('[')
            data.loc[index,'District'] = data.loc[index]['Name'][start_index:end_index -1]
            
        else:
            data.loc[index,'District'] = data.loc[index]['Name']


# # Transforming the population columns into int    
for index, row in data.iterrows():
    data.loc[index,'Pop'] = int(data.loc[index]['Population'])
    


# #Reading data from the shapefile
if x == 1:
    ctry = gpd.read_file(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\data\ARG_adm1.shp')
elif x == 2:
    ctry = gpd.read_file(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\data\PRT_adm1.shp')
elif x ==3:
    ctry = gpd.read_file(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\data\DEU_adm1.shp')
elif x ==4:
    ctry = gpd.read_file(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\data\AUT_adm1.shp')
else:
    print("We don't have that shapefile!")
    

print('#### READING SHAPEFILE ####')
    
# # to select only the columns i want from shapefile
ctry =ctry[['NAME_1','geometry']] 

print('##### SELECTING THE RIGHT COLUMNS OF THE SHAPEFILE #####')

# #change the name of the columns of the shapefile
ctry.rename(columns = {'NAME_1': 'District'}, inplace =True)

print('##### RENAMING SOME COLUMNS OF THE SHAPEFILE #####')


#Reprojection of the coordinate system (change degrees to meters to calculate the area of the polygons in squared meters)


ctry = ctry.to_crs('+proj= merc')


print("#### ASSIGNING THE RIGHT COORDINATE SYSTEM ####")

# #Replace the names misspelled (do it do whenever necessary) put this code above the for loop
#population_data.replace('Lisbon', 'Lisboa', inplace = True)

# #crosschecking shapefile + data from website 

for index, row in ctry['District'].iteritems():
    if row in data['District'].tolist():
        pass
    else:
        print('The district ', row, 'is not in the population_data list')
        
        

# #Create a new column in shapefile to calculate the area of the district
ctry['area'] = ctry.area/1000000


# #attreibute match (join)
print("#### MATCHING THE INFORMATION FROM DATA WITH THE SHAPEFILE ####")
ctry = ctry.merge(data, on='District')

# #Create a population density column
print('#### CALCULATING THE POPULATION DENSITY ####')
ctry['pop_density'] = ctry['Pop']/ctry['area']

##########################################################################################################################LOAD THE SHAPEFILE INTO DATABASE#####################################################################################################
# #Load Shapefile into the Data Base 

print('#### CONECTING WITH THE DATA BASE ####') 
if x == 1:
    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = 5432
    database = "test"
     
    conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(conn)
     
    # #Import shapefile to databse
    ctry.to_postgis(name="shp_arg", con=engine, if_exists= 'append', schema="public")
elif x == 2:
    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = 5432
    database = "test"
     
    conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(conn)
     
    # #Import shapefile to databse
    ctry.to_postgis(name="shp_prt", con=engine, if_exists= 'append', schema="public")
elif x == 3:
    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = 5432
    database = "test"
     
    conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(conn)
     
    # #Import shapefile to databse
    ctry.to_postgis(name="shp_ger", con=engine, if_exists= 'append', schema="public")
elif x == 4:
    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = 5432
    database = "test"
     
    conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(conn)
     
    # #Import shapefile to databse
    ctry.to_postgis(name="shp_aus", con=engine, if_exists= 'append', schema="public")
else:
    print("We're having troubles... Try again!")
    
print("#### THE CONNECTION WITH THE DATA BASE WAS ESTABLISHED ####")



