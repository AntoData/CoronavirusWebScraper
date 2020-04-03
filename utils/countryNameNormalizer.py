list_intersection = lambda lst1,lst2: [value for value in lst1 if value in lst2]


list1_not_in_list2 = lambda lst1,lst2: [value for value in lst1 if value not in lst2]


def get_canonical_country_name(country: str) -> str:
    """
    This method turns the name of countries in the page for the page with information about the corona virus or
    the information about the population in each country into the name of that country in the file
    data_coronavirus/world-countries.json
    :param country: The name of the country in any of the pages we request to scrap them
    :return: The name of the country we pass as a parameter to this method in the json file mentioned above
    """
    if country == "USA" or country == "US":
        return "United States"
    if country == "UK":
        return "United Kingdom"
    if country == "S. Korea":
        return "South Korea"
    if country == "Czech Republic (Czechia)" or country == "Czechia":
        return "Czech Republic"
    if country == "DR Congo" or country == "DRC":
        return "Democratic Republic of the Congo"
    if country == "Côte d'Ivoire":
        return "Ivory Coast"
    if country == "UAE":
        return "United Arab Emirates"
    if country == "Palestine":
        return "West Bank"
    if country == "CAR":
        return "Central African Republic"


def normalize_country_keys(data_dict: dict) -> dict:
    """
    This method builds a new dictionary file with the values of the dictionary parameter we pass as a parameter
    with the name of the country in the json file and the same values
    :param data_dict: Dictionary where the keys are the names of countries
    :return: Same dictionary where the names of the countries are the names of the countries in the json file
    """
    # We build an empty dictionary
    res_dict = {}
    # For each country in the dictionary we have passed as a parameter
    for v_key in data_dict.keys():
        # We try to get the name of the country in the json calling to the following method described above
        v_country = get_canonical_country_name(v_key)
        # If v_country is not None it means that country was on the list of countries that are not the same
        # in the json file and in our dictionary
        if v_country is not None:
            # In that case, we add a new pair key:value using the new name of the country
            # We first get the value in the original dictionary
            value = data_dict[v_key]
            # And then we proceed to add the new pair to the new dictionary
            res_dict[v_country] = value
        else:
            # Otherwise, we just add the same pair key:value to the new dictionary
            res_dict[v_key] = data_dict[v_key]
    # We return the new dictionary
    return res_dict
