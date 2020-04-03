# We import requests to get the HTML of our target site
import requests
# We use BeautifulSoup to parse that HTML and scrap the information
from bs4 import BeautifulSoup


def get_html_parser_population(url: str) -> BeautifulSoup:
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


def get_information_from_nth_row_population(row) -> (str, str):
    """
    This method gets the HTML code of a row in the table in the page
    https://www.worldometers.info/world-population/population-by-country/
    In each row, we have the population of a country, we return for each row the name of the country and the population
    :param row: HMTL code of this iteration's row
    :return:
    """
    country = row.find_all("td")[1].getText()
    population = row.find_all("td")[2].getText().replace(",", "")
    return country, population


def get_data_dictionary_population(url: str) -> dict:
    """
    This method makes the request to https://www.worldometers.info/world-population/population-by-country/ parses it
    and gets the data_coronavirus of the population from every country in the table where this page displays that information
    and return a dictionary where the key is the name of the country and the value is the population
    :param url: URL of the site, in this case this parser is prepared for
    :return: dictionary with the information of the population for each country. Keys = country and value = population
    """
    # We create an empty dictionary that we will return
    data = {}
    # We get the HMTL parser
    url_soup = get_html_parser_population(url)
    # We get all the row in that page (all the rows un tge table) where each one will contain the information for
    # the population of a country
    html_trs = url_soup.find_all("tr")
    # For each row (not counting the header)
    for i in range(1, (len(html_trs))):
        # We call to the method get_information_from_nth_row_population described above to get the name of the country
        # and its population
        country, population = get_information_from_nth_row_population(html_trs[i])
        # We add a pair key-value to this dictionary, where key = country and value = population
        data[country] = population
    # We return the dictionary this the information about the population in every country
    return data
