# We import pandas to manage and create dafa frames
import pandas as pd


def return_data_frame_cases(dict_corona_virus: dict, dict_population: dict,
                            data_frame_countries: pd.DataFrame) -> pd.DataFrame:
    """
    This method will return a data_coronavirus frame with the fields we need to create our map with circles. In this
     cases, the the circle will represent the ratio between cases and the population in every country
    :param dict_corona_virus: This is a dictionary that contains the information about corona virus spread for
    country, they key is the country and value is a list with 3 elements, cases, deaths and recovered in that order.
    This is the result of a web scraper
    :param dict_population: This is a dictionary that contains the population of every country. Key is the name of
    the country and value is the population. It is also the result of a web scraper
    :param data_frame_countries: Data frame with columns Country, Lat and Lon (where Lat y Lon is the latitude
    and longitude of that country's capital
    :return: A data_coronavirus frame with the following columns Country, Popup_Text (the text we will display when
    clicking in the circle), Population (in that country), Cases_Rate (cases/population), Lat (latitude of the capital
    of that country), Lon (longitude of the capital of that country)
    """
    # We create a list that contains all the column for the data_coronavirus frame result
    columns_list = ["Country", "Popup_Text", "Population", "Cases_Rate", "Lat", "Lon"]
    # We create a new empty data_coronavirus frame with those columns
    result_data_frame = pd.DataFrame(columns=columns_list)
    # We get every country that has people affected by the virus
    for country in dict_corona_virus.keys():
        # We check in that country is in the dictionary for populations and the data_coronavirus frame for countries
        # and capitals
        if country in dict_population.keys() and country in data_frame_countries["Country"].values:
            # We get the population of the country of this iteration
            population = dict_population[country]
            # We get the number of cases of corona virus in that country
            cases = dict_corona_virus[country][0]
            # We get the rate between cases and population in those cases
            rate = int(cases) / int(population)
            # We get the row in the data_coronavirus frame that contains the countries and longitude and latitude of
            # the capital
            df_aux = data_frame_countries.loc[data_frame_countries['Country'] == country]
            # We get the longitude of the capital of the country for this iteration
            lon = df_aux["Lon"].values
            # We get the latitude of the capital of the country for this iteration
            lat = df_aux["Lat"].values
            # We set the text for the popup
            popup_text = "<h3>{0}</h3>\n<h5>Population: {1}</h5>\n<h5>Cases: {2}</h5>".format(country, population,
                                                                                              cases)
            # We create the now row for this country
            df2 = pd.DataFrame([[country, popup_text, population, rate, lat[0], lon[0]]], columns=columns_list)
            # We add the row to the data_coronavirus frame that we will return
            result_data_frame = result_data_frame.append(df2, ignore_index=True)
    # We return the data_coronavirus frame
    return result_data_frame


def return_data_frame_recovered_vs_cases(dict_corona_virus: dict, data_frame_countries: pd.DataFrame) -> pd.DataFrame:
    """
    This method will return a data_coronavirus frame with the fields we need to create our map with circles. In this
    case, the circles will represent the ratio between recovered cases vs number of cases
    :param dict_corona_virus: This is a dictionary that contains the information about corona virus spread for
    country, they key is the country and value is a list with 3 elements, cases, deaths and recovered in that order.
    This is the result of a web scraper
    :param data_frame_countries: Data frame with columns Country, Lat and Lon (where Lat y Lon is the latitude
    and longitude of that country's capital
    :return: A data_coronavirus frame with the following columns Country, Popup_Text (the text we will display when
    clicking in the circle), Population (in that country), Cases_Rate (cases/population), Lat (latitude of the capital
    of that country), Lon (longitude of the capital of that country)
    """
    # We create a list that contains all the column for the data_coronavirus frame result
    columns_list = ["Country", "Popup_Text", "Recovered", "Recovered_Rate", "Lat", "Lon"]
    # We create a new empty data_coronavirus frame with those columns
    result_data_frame = pd.DataFrame(columns=columns_list)
    # We get every country that has people affected by the virus
    for country in dict_corona_virus.keys():
        # We check in that country is in the dictionary for populations and the data_coronavirus frame for countries
        # and capitals
        if country in data_frame_countries["Country"].values:
            # We get the number of recovered cases of corona virus in that country
            recovered = dict_corona_virus[country][2]
            # We get the number of cases of corona virus in that country
            cases = dict_corona_virus[country][0]
            # We get the rate between recovered cases and cases in those cases
            if recovered > 0:
                rate = int(recovered) / int(cases)
            else:
                rate = 0
            # We get the row in the data_coronavirus frame that contains the countries and longitude and latitude
            # of the capital
            df_aux = data_frame_countries.loc[data_frame_countries['Country'] == country]
            # We get the longitude of the capital of the country for this iteration
            lon = df_aux["Lon"].values
            # We get the latitude of the capital of the country for this iteration
            lat = df_aux["Lat"].values
            # We set the text for the popup
            popup_text = "<h3>{0}</h3>\n<h5>Recovered: {1}</h5>\n<h5>Cases: {2}</h5>".format(country, recovered, cases)
            # We create the now row for this country
            df2 = pd.DataFrame([[country, popup_text, recovered, rate, lat[0], lon[0]]], columns=columns_list)
            # We add the row to the data_coronavirus frame that we will return
            result_data_frame = result_data_frame.append(df2, ignore_index=True)
    # We return the data_coronavirus frame
    return result_data_frame


def return_data_frame_deaths_vs_cases(dict_corona_virus: dict, data_frame_countries: pd.DataFrame) -> pd.DataFrame:
    """
    This method will return a data_coronavirus frame with the fields we need to create our map with circles:
    In this map, the circles will represent the ratio between deaths and number of cases
    :param dict_corona_virus: This is a dictionary that contains the information about corona virus spread for
    country, they key is the country and value is a list with 3 elements, cases, deaths and recovered in that order.
    This is the result of a web scraper
    :param data_frame_countries: Data frame with columns Country, Lat and Lon (where Lat y Lon is the latitude
    and longitude of that country's capital
    :return: A data_coronavirus frame with the following columns Country, Popup_Text (the text we will display when
    clicking in the circle), Population (in that country), Cases_Rate (cases/population), Lat (latitude of the capital
    of that country), Lon (longitude of the capital of that country)
    """
    # We create a list that contains all the column for the data_coronavirus frame result
    columns_list = ["Country", "Popup_Text", "Recovered", "Recovered_Rate", "Lat", "Lon"]
    # We create a new empty data_coronavirus frame with those columns
    result_data_frame = pd.DataFrame(columns=columns_list)
    # We get every country that has people affected by the virus
    for country in dict_corona_virus.keys():
        # We check in that country is in the dictionary for populations and the data_coronavirus frame for
        # countries and capitals
        if country in data_frame_countries["Country"].values:
            # We get the number of deaths due to corona virus in that country
            deaths = dict_corona_virus[country][1]
            # We get the number of cases of corona virus in that country
            cases = dict_corona_virus[country][0]
            # We get the rate between recovered cases and cases in those cases
            if deaths > 0:
                rate = int(deaths) / int(cases)
            else:
                rate = 0
            # We get the row in the data_coronavirus frame that contains the countries and longitude and latitude of the
            # capital
            df_aux = data_frame_countries.loc[data_frame_countries['Country'] == country]
            # We get the longitude of the capital of the country for this iteration
            lon = df_aux["Lon"].values
            # We get the latitude of the capital of the country for this iteration
            lat = df_aux["Lat"].values
            # We set the text for the popup
            popup_text = "<h3>{0}</h3>\n<h5>Deaths: {1}</h5>\n<h5>Cases: {2}</h5>".format(country, deaths, cases)
            # We create the now row for this country
            df2 = pd.DataFrame([[country, popup_text, deaths, rate, lat[0], lon[0]]], columns=columns_list)
            # We add the row to the data_coronavirus frame that we will return
            result_data_frame = result_data_frame.append(df2, ignore_index=True)
    # We return the data_coronavirus frame
    return result_data_frame
