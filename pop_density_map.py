# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 20:20:02 2023

@author: Francisco
"""



import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
from pyproj import CRS, Proj, transform



#set correct directory
pyproj.datadir.set_data_dir("C:\\Users\\Francisco\\miniconda3\\envs\\project-env\\Library\\share\\proj")

# Data aquisition (population data from the web)
data = pd.read_html('https://en.wikipedia.org/wiki/Ranked_list_of_Portuguese_districts')

#extract the data from the list gave by the link and save it in another variable
for population_data in data:
    print(population_data)

#save population data in excel file 
population_data.to_excel(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\pop.xlsx')

population_data = pd.read_excel(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\pop.xlsx')


# #select just the colums i want/need
population_data = population_data[['District','Population']]

# #change the name of a column
population_data.rename(columns = {'District':'Name'}, inplace = True)


# #filter rows by value
# #population_data = population__data.loc[population_data['Status'] == 'District']

# #Create empty column
population_data['District'] = ''

#For loop to clean the data and add in the new column
for index, row in population_data.iterrows():
    if '('and ')' in row['Name']:
        start_index = row['Name'].find('')
        end_index = row['Name'].find('(')
        population_data.loc[index,'District'] = population_data.loc[index]['Name'][start_index:end_index -1]
        
    else:
        population_data.loc[index,'District'] = population_data.loc[index]['Name']


# #Reading data from the shapefile
prt = gpd.read_file(r'C:/Users/Francisco/Documents/Nova IMS/Programing/teste/data/PRT_adm1.shp')
    
# # to select only the columns i want from prt shapefile
prt =prt[['NAME_1','geometry']] 

# #change the name of the columns of the shapefile
prt.rename(columns = {'NAME_1': 'District'}, inplace =True)


# #plot Country
#prt.plot()  

#Reprojection of the coordinate system (change degrees to meters to calculate the area of the polygons in squared meters)
prt.to_crs(epsg=3763, inplace =True)
 
#Replace the names misspelled (do it do whenever necessary) put this code above the for loop
population_data.replace('Lisbon', 'Lisboa', inplace = True)

# #crosschecking shapefile + data from website 
i=0
for index, row in prt['District'].iteritems():
    if row in population_data['District'].tolist():
        pass
    else:
        print('The district ', row, 'is not in the population_data list')
        i+= 1
print(i)        

#Create a new column in shapefile to calculate the area of the district
prt['area'] = prt.area/1000000

#attreibute match (join)
prt = prt.merge(population_data, on='District')

#Create a population density column
prt['pop_density (people/sq Km)'] = prt['Population']/prt['area']

#plot pop_density map

with plt.style.context(("seaborn", "ggplot")):
    prt.plot(column ='pop_density (people/sq Km)',
             cmap = 'YlOrRd',
             figsize=(8,8),
             legend= True,
             legend_kwds={"label":"Population Density", "orientation":"horizontal"},
             edgecolor="black")

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Portugal Population Density Map")
plt.savefig('population_density_prt.jpg')