import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_html_parser(url: str) -> BeautifulSoup:
    """
    This method makes the request to the URL we pass as a parameter and gets the HTML code of that page
    then we parse that as HTML as return the HTML code parsed
    :param url:
    :return: BeautifulSoup HTML parser
    """
    # We get the request to that URL
    url_request = requests.get(url)
    # We get the text, the HTML source code
    url_html = url_request.text
    # We create a parser for that HTML code
    url_soup = BeautifulSoup(url_html, 'html.parser')
    # We return that parser
    return url_soup


def get_information_from_nth_row_coronavirus(row) -> (str, list):
    """
    This method gets a row of the table in the site https://www.worldometers.info/coronavirus/ with the information
    this site provides. In each row, we are given the name of the country, the number of cases, the number of
    new cases, deaths, new deaths, recovered people... and we get the country, number of cases, number of deaths
    and number of recovered cases in that country and return
    :param row: HTML of a row in the table in  https://www.worldometers.info/coronavirus/ where the page provides
    information about the name of the country, cases, deaths and recovered people
    :return: A str with the name of the country in that row and a list with the cases in that country, the number of
    deaths and recovered people in that order
    """
    country = row.find_all("td")[0].getText()
    total_cases = row.find_all("td")[1].getText().replace(",", "")
    total_cases = total_cases.replace(" ", "")
    if total_cases == "":
        total_cases = 0
    total_deaths = row.find_all("td")[3].getText().replace(",", "")
    total_deaths = total_deaths.replace(" ", "")
    if total_deaths == "":
        total_deaths = 0
    total_recovered = row.find_all("td")[5].getText().replace(",", "")
    total_recovered = total_recovered.replace(" ", "")
    if total_recovered == "":
        total_recovered = 0
    figures = [int(total_cases), int(total_deaths), int(total_recovered)]
    return country, figures


def get_data_dictionary_coronavirus(url: str) -> dict:
    """
    This method requests the URL in https://www.worldometers.info/coronavirus/ and turn the table with the information
    about cases, deaths and recovered people in each country into a dictionory where key is the name of the country and
    the value is a list with cases, deaths and recovered in that order
    :param url: String with the URL of the site to scrap
    :return: A dictionary with the information about the corona virus in the world, where key is the name of the country
    and value is a list of cases, deaths and recovered people in that country in that order
    """
    # We create an empty dictionary to be returned at the end of this method
    data = {}
    # We get the HTML parser
    url_soup = get_html_parser(url)
    # We get all the rows in that page (all the rows in the table with the information)
    html_trs = url_soup.find_all("tr")
    # For each row
    for i in range(1, (len(html_trs))):
        # We call get_information_from_nth_row_coronavirus to get the name of the country and the data_coronavirus about
        # cases, deaths and recovered people in that list in that order
        country, figures = get_information_from_nth_row_coronavirus(html_trs[i])
        # We create a new key:value pair in that dictionary where key=country and value = list of figures
        data[country] = figures
        # When we get to the last row in that toble (which is Total) we break this loop
        if country == "Total:":
            break
    # We return the dictionary
    return data


def from_coronavirus_dict_to_report_txt(data: dict):
    """
    This method turns the information that we recovered from the web into a data_coronavirus frame into a text file
    :param data: Dictionary result of the method that scraps the site to get the information about the corona virus
    :return: None
    """
    # If data_coronavirus is not a dictionary, we raise an exception
    if not isinstance(data, dict):
        raise TypeError("Parameter data_coronavirus must be a dictionary")
    # We get the current date
    now = datetime.now()
    # We turn that date into string using the format detailed below
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    # We initialize a variable f for a file to None
    f = None
    try:
        # We try to create that file
        f = open("./reports/{0}.txt".format(date_str), "+w")
        # For each country in the dictionary
        for country in data.keys():
            # We get the figures
            figures = data[country]
            cases = figures[0]
            deaths = figures[1]
            recovered = figures[2]
            # We generate the line to add to the file
            line = "{0} - Cases: {1}, Deaths: {2}, Recovered: {3}\n".format(country, cases, deaths, recovered)
            # We write that line in that file
            f.write(line)
    except Exception as e:
        # We catch any exception
        print("When opening or writing the file the following exception happened: {0}".format(e))
    finally:
        # We always close this file (if we opened it)
        if f is not None:
            f.close()
