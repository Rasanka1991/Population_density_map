# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 15:40:55 2023

@author: Francisco
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
from pyproj import CRS, Proj, transform
import os



#set correct directory
pyproj.datadir.set_data_dir("C:\\Users\\Francisco\\miniconda3\\envs\\project-env\\Library\\share\\proj")

#####################################################################################################################ETL PART#####################################################################################################################################

# Data aquisition (population data from the web)
data = pd.read_html('https://citypopulation.de/php/argentina-admin.php')

#extract the data from the list gave by the link and save it in another variable
for population_data in data:
    print(population_data)

#save population data in excel file 
population_data.to_excel(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\pop.xlsx')


# def extract_from_csv(file):
#     population_data = pd.read_excel(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\pop.xlsx')
#     return population_data

# def extract():
#        extracted_data = pd.DataFrame(columns=['car_model','year_of_manufacture','price', 'fuel']) 
#     #for csv files
#       for csvfile in glob.glob(r"C:\Users\Francisco\Documents\Nova IMS\Programing\teste\pop.xlsx'"):
#           extracted_data = extracted_data.append(extract_from_csv(csvfile), ignore_index=True)
#       return extracted_data



# #select just the colums i want/need
population_data = population_data[['Name','Status','Population Projection 2019-07-01']]

# #change the name of a column
population_data.rename(columns = {'Population Projection 2019-07-01':'Population'}, inplace = True)


# #filter rows by value
population_data = population_data.loc[population_data['Status'] == 'Province']

# #Create empty column
population_data['District'] = ''
population_data['Pop_density'] = ''

#For loop to clean the data and add in the new column
# for index, row in population_data.iterrows():
#     if '('and ')' in row['Name']:
#         start_index = row['Name'].find('')
#         end_index = row['Name'].find('(')
#         population_data.loc[index,'District'] = population_data.loc[index]['Name'][start_index:end_index -1]
        
#     else:
#         population_data.loc[index,'District'] = population_data.loc[index]['Name']

for index, row in population_data.iterrows():
    population_data.loc[index,'District'] = population_data.loc[index]['Name']
    
for index, row in population_data.iterrows():
    population_data.loc[index,'Pop_density'] = int(population_data.loc[index]['Population'])

# #Reading data from the shapefile
ctry = gpd.read_file(r'C:\Users\Francisco\Documents\Nova IMS\Programing\teste\argentina_data\ARG_adm1.shp')
    
# # to select only the columns i want from prt shapefile
ctry =ctry[['NAME_1','geometry']] 

# #change the name of the columns of the shapefile
ctry.rename(columns = {'NAME_1': 'District'}, inplace =True)


# #plot Country
# ctry.plot()  

#Reprojection of the coordinate system (change degrees to meters to calculate the area of the polygons in squared meters)
ctry.to_crs(epsg=9252, inplace =True)
 
#Replace the names misspelled (do it do whenever necessary) put this code above the for loop
#population_data.replace('Lisbon', 'Lisboa', inplace = True)

# #crosschecking shapefile + data from website 
i=0
for index, row in ctry['District'].iteritems():
    if row in population_data['District'].tolist():
        pass
    else:
        print('The district ', row, 'is not in the population_data list')
        i+= 1
print(i)        

#Create a new column in shapefile to calculate the area of the district
ctry['area'] = ctry.area/1000000

#attreibute match (join)
ctry = ctry.merge(population_data, on='District')

#Create a population density column
ctry['pop_density (people/sq Km)'] = ctry['Pop_density']/ctry['area']

##################################################################################################################################plot pop_density map

with plt.style.context(("seaborn", "ggplot")):
    ctry.plot(column ='pop_density (people/sq Km)', cmap = 'YlOrRd', figsize=(10,5),legend= True, edgecolor="black",scheme='natural_breaks', k=7, legend_kwds={'loc': 'center left', 'title': 'Population Density (people/sq Km)','fontsize':12,'frameon':True, 'bbox_to_anchor':(1,0.5)})


plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Population Density Map")
plt.savefig('population_density_ctry.jpg')