# NOTE: All data from https://www.worldometers.info/coronavirus/ and
# https://www.worldometers.info/world-population/population-by-country/
# We import pandas to create and manage data_coronavirus frames
import pandas as pd
# We import folium to create and manage maps in HTML format
import folium
# We import datetime to generate the current date for a file name
import datetime
# We import this custom made method to get a data_coronavirus frame to create the map with the ratio cases/populaiton
from utils.Calculations import return_data_frame_cases, return_data_frame_recovered_vs_cases, \
    return_data_frame_deaths_vs_cases
# We import this custom made method to add circles in the map the represent the ratio described above
from api.MapGenerator import put_circles_in_map
# We import this custom made method so the names of countries are the same in every piece of data_coronavirus
from utils.countryNameNormalizer import normalize_country_keys
# We import this custom made method to get the dictionary that contains the information of the population in each
# country from the site https://www.worldometers.info/world-population/population-by-country/
from api.worldofmetersPopulationAPI import get_data_dictionary_population
# We import this custom made method to get the dictionary that contains the information of the figures
# (cases, deaths and recovered people) related to corona virus in each country from
# https://www.worldometers.info/coronavirus/
from api.worldometersCoronavirusScraperAPI import get_data_dictionary_coronavirus

# URL with the page to scrap to get the info related to the corona virus outbreak
url = "https://www.worldometers.info/coronavirus/"
# URL with the page to scrap to get the info related to the population in each country
url2 = "https://www.worldometers.info/world-population/population-by-country/"

# We read the csv that contains the longitude and latitude of the capitals for each country into a data_coronavirus
# frame
df_world_capitals = pd.read_csv("data/world_capitals.csv", sep=",")

# We get scrap the site https://www.worldometers.info/coronavirus/ and turn the information into a dictionary
data_coronavirus = get_data_dictionary_coronavirus(url)
# We get scrap the sitehttps://www.worldometers.info/world-population/population-by-country/
# and turn the information into a dictionary
data_population = get_data_dictionary_population(url2)
# We "normalize" the names of the countries so they match with the ones in the json file that we will use to build
# the map
data_coronavirus = normalize_country_keys(data_coronavirus)
data_population = normalize_country_keys(data_population)

print(data_coronavirus)
print(data_population)
# We build the data_coronavirus frame we will use to build the map where we will have in the same data_coronavirus frame
# the name of the country, the latitude and longitude of the capital of that country and the ratio between the number
# of cases and the population in that country (cases/population)
df_ratio_cases_vs_population = return_data_frame_cases(data_coronavirus, data_population, df_world_capitals)
print(df_ratio_cases_vs_population)

# We build a basic world map
cases_rate_world = folium.Map(titles='Mapbox Bright', start_zoom=3)
# We generate the map with the circles in the capital of each country with cases where the circle will have a radius
# with the ratio between cases/population multiplied by 100000000
cases_rate_world = put_circles_in_map(cases_rate_world, df_ratio_cases_vs_population, "Popup_Text", "Lat", "Lon",
                                      "Cases_Rate", 50000000, "red", "red")

# We get the current date
x = datetime.datetime.now()
# We save the map into a HTML file using today's date
cases_rate_world.save("./maps/cases_{0}-{1}-{2}.html".format(x.year, x.month, x.day))

# We get the data frame with the information with the latitude and longitude of the capital of each country and the
# ratio between recovered cases and number of cases in that country
df_ratio_recovered_vs_cases = return_data_frame_recovered_vs_cases(data_coronavirus, df_world_capitals)
print(df_ratio_recovered_vs_cases)

# We generate a new map
recovered_rate_world = folium.Map(titles='Mapbox Bright', start_zoom=3)
# We put the circles in that map that represent the ratio described above
recovered_rate_world = put_circles_in_map(recovered_rate_world, df_ratio_recovered_vs_cases, "Popup_Text", "Lat", "Lon",
                                          "Recovered_Rate", 500000, "green", "green")
# We save the map into a file with the current date
recovered_rate_world.save("./maps/recovered_{0}-{1}-{2}.html".format(x.year, x.month, x.day))

# We get the data frame with the information with the latitude and longitude of the capital of each country and the
# ratio between deaths and number of cases in that country
df_ratio_deaths_vs_cases = return_data_frame_deaths_vs_cases(data_coronavirus, df_world_capitals)
print(df_ratio_deaths_vs_cases)

# We generate a new map
death_rate_world = folium.Map(titles='Mapbox Bright', start_zoom=3)
# We put circles in that map that represent the ratio described above
death_rate_world = put_circles_in_map(death_rate_world, df_ratio_deaths_vs_cases, "Popup_Text", "Lat",
                                      "Lon", "Recovered_Rate", 1000000, "black", "black")
# We save this map to an HTML file
death_rate_world.save("./maps/deaths_{0}-{1}-{2}.html".format(x.year, x.month, x.day))
