<h1 align="center"><b>Population density mapper for countries in Europe </b></h1>

![alt text](/static/images/cover.png)

## Introduction

Population density is the average number of people per unit, usually miles or kilometers, of land area. Understanding and mapping population density is important. Experts can use this information to inform decisions around resource allocation, natural disaster relief, and new infrastructure projects. The objective of this web application is to provide the user with information on population density for any country pick on the map. 

## Data and Method

Population statistics downloaded from the [city population](https://www.citypopulation.de/) data portal and the administrative boundary information retrieved from the [DIVA-GIS](http://www.diva-gis.org/Data) data portal were used as the main data source for the project to calculate the population density of selected 27 countries of the European Union.


## Running on your local environment
To run the app locally, the following requirements are necessary:
* Python 3.x
* Postgres SQL database with enabled PostGIS extension 
* Install packages listed in the requirements.txt file

``` conda install requirements.txt -c conda forge ```


Then clone the repository in to your local working environment and update the configuration.yml with your own database name, user name and password of the postgres server. Finally, run the file “main.py” and open the application locally in the browser.


## Disclaimer
This project was done within the GPS group project class of the Master in Geospatial Technologies (Winter term 2022/2023) of the NOVA Information Management School of Lisbon by the students Rasanka De Silva, Fransisco Boieiro and Romarick Tewiy. This is therefore an educational exercise that would need further proofing in case the app were to be launched into the general public.
