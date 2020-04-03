# CoronavirusWebScraper
 Web scraper that gets information about the corona virus spread from https://www.worldometers.info/coronavirus/ and world population in  from https://www.worldometers.info/world-population/population-by-country/ and generates three maps with folium that represent the ratio between cases and population, between recovered people and cases and between death people and cases using circles

The project has the following structure:
 - Folder api: Here we have included all the files in modules that are part of our API. These methods are of general use to perform several tasks and therefore they are reusable:
   - MapGenerator.py: This module contains several methods to build maps
   - worldofmetersPopulationAPI.py: This module contains the methods needed to get the information about the population in each country on Earth from the site: https://www.worldometers.info/world-population/population-by-country/
   - worldometersCoronavirusScraperAPI.py: This module contains the methods needed to get the information about the population in each country on Earth from the site: https://www.worldometers.info/coronavirus/
 
 - Folder data: Here we have the fields with data needed to generate our maps:
   - world-countries.json: This json file contains the division by countries in our map
   - world_capitals.csv: This csv file contains the name of every country and the latitude and longitude of its capital
 
 - Folder maps: Here we will save the HTML files result of our program. We will have 3 diferent kinds of maps:
   - cases_yyyy-MM-dd.html: Map of the date that indicates the date in the title that displays in circles the ratio between number of cases and the population in the country
   - deaths_yyyy-MM-dd.html: Map of the data that indicates the date in the title that displays in circles the ratio between the number of people that died from this virus and the number of cases in that country
   - recovered_yyyy-MM-dd.html: Map of the data that indicates the date in the title that displays in circles the ratio between the number of recovered people and the number of cases in that country
 
 - Folder reports: Here we will save the txt files that are result of our program. Those txt files will be title with the date and timestamp in which they were generated. The reports contain the name of the country, the number of cases, deaths and recovered people
 
 - Folder utils: This folder contains modules that perform several tasks that are needed and repeated during this program:
   - Calculations.py: This module contains the methods that generate the data frames that we will use in our 3 kinds of maps gathering the data and performing the different calculations
   - countryNameNormalizer.py: This module contains the method that makes the different names of countries the same as the one in the json file world-countries.json

- Module CoronaVirusMapGenerator.py: Module that we have to run to create our maps, this is the main module
