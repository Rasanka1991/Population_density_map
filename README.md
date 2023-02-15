# NOVA IMS Group Project- Master of science in Geospatial Technologies

### This git hub repository is still under construction, it is intending to develop a code using python programing language to read a database from a postgressql data base.

## The conceptual work flow of the project is as follows,

1. Click on top of the country flag or select the country of interest using the dispalyed map in the html page
2. Collect the clicked country name and pass to the main.py
3. Search the database to obtain the population and boundary information of the selected country
4. Pass the data to the pop_density_map_v3.py to calculate the population density and obtain the raster to display
5. Get the output map from  pop_density_map_v3.py to the main.py
6. Display the population density raster using HTML Map

## Steps to followed to work on a local directory

1. Clone the repository from Github environment to your working directory
2. Create a working environment and install the required libraries listed in requirements.txt
3. Create a database named Population_density in PgAdmin (PostgreSQL)
4. Update the configuration.yml with the user name and password of the postgres server
5. Execute the ............py to create data tables in Population_density database
6. Execute main.py
