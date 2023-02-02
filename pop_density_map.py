# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 12:47:45 2023

@author: Francisco
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
from pyproj import CRS, Proj, transform
#my_geoseries = my_geoseries.set_crs("EPSG:4326")

# crs=CRS('EPSG:4326')


#set correct directory
pyproj.datadir.set_data_dir("C:\\Users\\Francisco\\miniconda3\\envs\\project-env\\Library\\share\\proj")

# Data aquisition (population data from the web)~
data = pd.read_html('https://www.citypopulation.de/en/portugal/cities/') #read the weblink

#extract the data from the list gave by the link and save in another variable
for population_data in data:
    print(population_data)

#save population data in excel file 
population_data.to_excel(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\pop.xlsx')

population_data = pd.read_excel(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\pop.xlsx')


# #select just the colums i want/need
population_data = population_data[['Name','Adm.','Population Census (Cf) 2021-03-22', 'Area']]

# #change the name of a column
population_data.rename(columns = {'Population Census (Cf) 2021-03-22':'Population Census 2021'}, inplace = True)


# #filter rows by value
# #population_data = population__data.loc[population_data['Status'] == 'District']

# #Create empty column
# #population_data['Districts'] = ''
# # for index, row in population_data.iterrows():
# #     if '['and ']' in row['Name']:
# #         start_index = row['Name'].find('[')
# #         end_index = row['Name'].find(']')
# #         population_data.loc[index,'District']=population_data.loc[index]['Name'][start_index+1: end_index]
# #     else:
# #         population_data.loc[index,'District'] = population_data.loc[index['Name']]


# #Reading data from the shapefile
prt = gpd.read_file(r'C:/Users/Francisco/Documents/Nova IMS/Programing/teste/data/PRT_adm3.shp')
    
# # to select only the columns i want from prt shapefile
# #prt =prt[['NAME_3','geometry']] 

# #change the name of the columns of the shapefile
# #prt.rename(columns = {'NAME_3': 'District'}, inplace =True)


# #plot 
prt.plot()  

#Reprojection of the coordinate system (change degrees to meters to calculate the area of the polygons in squared meters)
#prt.to_crs(epsg=3763, inplace =True)

#crosschecking shapefile + data from website 

# for index, row in prt['District'].iteritems():
#     if row in population_data['Name'].tolist():
#         pass
#     else:
#         print('The district ', row, 'is not in the population_data list')
        

# #Replace the names misspelled (do it do whenever necessary) put this code above the for loop
# #population_data.replace('names misspelled', 'right name', inplace = True)

# #Create a new column in shapefile to calculate the area of the district
# prt['area'] = prt.area/1000000

# #attreibute match (join)
# prt = prt.merge(population_data, on='Name')

# #Create a population density column
# prt['pop_density (people/sq Km)'] = prt['population']/prt['area']

# #plot pop_density map
# prt.plot(column ='pop_density (people/sq Km)', cmap = 'Spectral', legend= True)
# plt.savefig('population_density_prt.jpg')


 

