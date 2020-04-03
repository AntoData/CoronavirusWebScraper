# Created on 21 jul. 2019

# @author: ingov

# We use folium to genetate the maps
import folium
# We use LinearColormap to create scales for pair of colours-values
from branca.colormap import LinearColormap
# We use branca to create the legend for our map
import branca

import pandas


def color_scale(color1: str, color2: str, value: float, min_value: float, max_value: float) -> LinearColormap:
    """
    :param color1: This parameter is a string that contains a hexadecimal color (format #XXXXXX)
    or a valid color (for instance red, orange, yellow, blue) that establishes the first color
    in that range of values, the color that will be associated with minValue
    :param color2: This parameter is a string that contains a hexadecimal color (format #XXXXXX)
    or a valid color (for instance red, orange, yellow, blue) that establishes the second color
    in that range of values the color that will be associated with maxValue
    :param value: This parameter is a number, the value we have to paint with a color between
    color1 and color2 and that has to be between minValue and maxValue
    :param min_value: This parameter is a number, the lowest value possible within this range
    we are defining
    :param max_value: This parameter is a number, the highest value possible within this range
    we are defining
    :return: LinearColorMap object
    """
    return LinearColormap([color1, color2], vmin=min_value, vmax=max_value)(value)


def get_color(feature: dict, data_map: dict, colours: dict, map_property: str):
    """
    This function gets the object feature that represents the property feature in the json,
    a dictionary with the data_coronavirus (we use a data_frame and turn it into a dictionary),
    and a map with the ranges and colours where the key is the value and the value
    is the color associated to that value
    :param feature: Contains the property feature in the json of our map
    :param data_map: A dictionary with the data_coronavirus (we use a data_frame and turn it into a dictionary)
    :param colours: Dictionary with the ranges and colours where the key is the value and the value
    is the color associated to that value. It is important to notice that we can mix string values
    that will be static values (no range for them) and ranges. We will have to put all string/static
    values first in the map and them the number values that will be paired to make ranges.
    Also important to notice, the keys are the values and the values are the color a string
    with the hexadecimal color (#XXXXXX) or a valid color name
    :param map_property: Property in feature we will use to identify the zones defined in the
    json
    :return: the colour for the region we are iterating over, if it was a string/static value we will
    just return the colour in the map colours. But if it is a float we will evaluate inside which
    range it is and use the previously defined funcion color_scale to get the right color
    """
    # We get the keys of the dict colours which are the range of values to consider to
    # colour this map, we will use it to compare the values in the dictionary with the values
    # for each row in the dictionary dataMap
    colours_key = list(colours.keys())
    # We get the value of the associated to the region of our json that is going to be painted
    # in our data_coronavirus frame (well, the dictionary that we got from our data_frame), in this case
    # the property we use in the json (mapProperty) to get the value has to be a child of
    # properties. Also, our key values have to coincide with the property in the json that is
    # represented by mapProperty
    print(feature['properties'][map_property])
    value = data_map.get(feature['properties'][map_property])
    try:
        number = int(value)
        value = number
    except TypeError:
        try:
            number = float(value)
            value = number
        except TypeError:
            pass
    # If value is not None, it means it is in our dataMap so we have to color that area
    if value is not None:
        # If value is not int or float, it means is a static value
        if not isinstance(value, (int, float)):
            i = 0
            # We iterate through the different values that are associated with colors
            while i < len(colours_key) and value is not None:
                # If our value is equal to the value associated with a certain color, we return
                # that color
                if colours_key[i] == value:
                    return colours.get(colours_key[i])
                i = i + 1
        else:
            # We iterate through the values that define the ranges of colours that we got from
            # our dictionary of colors (key:value, value:colour)
            i = 1
            while i < len(colours_key) and value is not None:
                # if our current value is in that range, we use the function color_scale
                # that we defined previously to get the corresponding shade of the colour
                # for that value
                if isinstance(colours_key[i - 1], (int, float)) and isinstance(colours_key[i], (int, float)):
                    lower_value = float(colours_key[i - 1])
                    upper_value = float(colours_key[i])
                    num_value = float(value)
                    if lower_value <= num_value <= upper_value:
                        return color_scale(colours.get(lower_value), colours.get(upper_value), num_value, lower_value,
                                           upper_value)
                i = i + 1


def build_map(v_map: folium.Map, json_data: str, data_map: dict, colours: dict, v_caption: str, v_caption2: str,
              map_property: str) -> folium.Map:
    """
    This function is the one that builds the map in v_map
    :param v_map: Folium map object we will use as the base to build the regions and paint them
    :param json_data: Route to the json we will use to divide our map into regions and to paint them
    :param data_map: A dictionary with the data_coronavirus (we use a data_frame and turn it into a dictionary)
    :param colours: Dictionary with the ranges and colours where the key is the value and the value
    is the color associated to that value. It is important to notice that we can mix string values
    that will be static values (no range for them) and ranges. We will have to put all string/static
    values first in the map and them the number values that will be paired to make ranges.
    Also important to notice, the keys are the values and the values are the color a string
    with the hexadecimal color (#XXXXXX) or a valid color name
    :param v_caption: Text we will put in the legend for the linear colours in the map
    :param v_caption2: Text we will put in the legend for the static colours in the map
    :param map_property: Property in feature we will use to identify the zones defined in the
    json
    :return: the map divided in regions, with the regions painted and coloured according to the
    values we indicated in the dictionary dataMap
    """
    # We color the map in v_map using the feature GeoJson
    # and add it to the map
    folium.GeoJson(
        data=json_data,
        style_function=lambda feature: {
            'fillColor': get_color(feature, data_map, colours, map_property),
            'fillOpacity': 0.7,
            'color': None,
            'weight': 1,
        }
    ).add_to(v_map)
    # We create a legend for the colours which we have painted our map with
    colours_keys = list(colours.keys())
    # coloursValues = list(colours.values())
    linear_legend_keys = []
    linear_legend_values = []
    nonlinear_legend_keys = []
    nonlinear_legend_values = []
    num_value = True
    for v_colour in colours_keys:
        if isinstance(v_colour, (int, float)):
            linear_legend_values.append(colours[v_colour])
            linear_legend_keys.append(v_colour)
        else:
            nonlinear_legend_keys.append(v_colour)
            nonlinear_legend_values.append(colours[v_colour])
            num_value = False

    # We create a colormap object to be used as legend
    if len(linear_legend_keys) > 1 and len(linear_legend_values) > 1:
        colormap = branca.colormap.LinearColormap(linear_legend_values)
        colormap = colormap.to_step(index=linear_legend_keys)
        colormap.caption = v_caption
        # We add the colormap to our map
        colormap.add_to(v_map)
    # We this value corresponds to an static value, we will add it to the legend for static values
    if not num_value:
        html_legend = """
        <div style='position: fixed;bottom:50px;left:50px;border:2px solid grey;z-index:9999; font-size:14px'>
        &nbsp; """ + v_caption2
        for key in nonlinear_legend_keys:
            html_legend += '<br> &nbsp; ' + key + ' &nbsp;'
            html_legend += '<svg width="40" height="11">'
            color = colours[key].replace(' ', "")
            rgb_color = list(int(color[i:i + 2], 16) for i in (1, 3, 5))
            html_legend += '    <rect width="40" height="11" style="fill:rgb({0},{1},{2});stroke-width:3;stroke:' \
                           'rgb(0,0,0)" />'.format(rgb_color[0], rgb_color[1], rgb_color[2])
            html_legend += '</svg>'
        html_legend += """
        </div>
        """
        v_map.get_root().html.add_child(folium.Element(html_legend))

    return v_map


def put_markers(v_map: folium.map, v_data: pandas.DataFrame, col_lat: str, col_lon: str, col_popup: str,
                marker_colour: str) -> folium.Map:
    """
    :param v_map: Folium map object we will use as the base to build the regions and paint them
    :param v_data: A data_frame with the data_coronavirus
    :param col_lat: Name of the column in the data_frame where the latitude for the point where
    we want to display the marker is saved
    :param col_lon: Name of the column in the data_frame where the longitude for the point where
    we want to display the marker is saved
    :param col_popup: Name of the column in the data_frame where the message for the popup for that
    marker is saved
    :param marker_colour: Colour for the marker
    :return: Our map v_map with the markers added
    """
    # we go through the data_frame
    for i in range(0, v_data.shape[0]):
        # And create and add a marker for every row
        folium.Marker(location=[v_data.loc[i][col_lat], v_data.loc[i][col_lon]],
                      popup="<b>{0}</b>".format(v_data.loc[i][col_popup]),
                      icon=folium.Icon(color=marker_colour, size=1)).add_to(v_map)

    return v_map


def put_generic_markers(v_map, v_data, func_html, col_lat, col_lon, marker_colour):
    """
    :param v_map: Folium map object we will use as the base to build the regions and paint them
    :param v_data: A data_frame with the data_coronavirus
    :param func_html: This is a function that will provide the HTML code for the popup for
    that every marker
    :param col_lat: Name of the column in the data_frame where the latitude for the point where
    we want to display the marker is saved
    :param col_lon: Name of the column in the data_frame where the longitude for the point where
    we want to display the marker is saved
    :param marker_colour: Colour for the marker
    :return: Our map v_map with the markers added
    """
    # we go through the data_frame
    for i in range(0, v_data.shape[0]):
        # And create and add a marker for every row
        folium.Marker(location=[v_data.loc[i][col_lat], v_data.loc[i][col_lon]], popup=func_html(v_data.loc[i]),
                      icon=folium.Icon(color=marker_colour, size=1)).add_to(v_map)
    return v_map


def put_circles_in_map(v_map, data_frame, popup_field, latitude_field, longitude_field,
                       value_field, proportion, color='crimson', fill_color=None):
    """
    This function draws circles with a proportion related to the value of a field in a data_frame
    :param v_map: Map where we want to draw the circles
    :param data_frame: data_frame where we have the data_coronavirus we will use as value for the radius of these
    circles (we will multiply by proportion to get the radius)
    :param popup_field: Field in our data_frame we will use as information to display in the pop-up
    that is opened when we click in one of these circles we are drawing
    :param latitude_field: Field in our data_frame where we store the latitude of the point where we
    want to display a circle for a particular row
    :param longitude_field: Field in our data_frame where we store the longitude of the point where we
    want to display a circle for a particular row
    :param value_field: Field with the data_coronavirus we will use to get the radius of our circle. We will
    multiply this by proportion
    :param proportion: Proportion of the size we want our circles to have in relation to our values
    :param color: Color for the border of the circle. By default 'crimson'
    :param fill_color: Color of the interior of the circle. By default, None (so it won't be filed)
    :return Our map v_map with the circles added
    """
    # For each row in the data_frame we paint a circle using the columns we set up before
    # for that particular eow
    for i in range(0, len(data_frame)):
        if fill_color is None:
            v_map.add_child(folium.Circle(
                location=(data_frame.iloc[i][latitude_field], data_frame.iloc[i][longitude_field]),
                popup=data_frame.iloc[i][popup_field],
                radius=int(data_frame.iloc[i][value_field] * proportion),
                color=color,
                fill=False))
        else:
            v_map.add_child(folium.Circle(
                location=(data_frame.iloc[i][latitude_field], data_frame.iloc[i][longitude_field]),
                popup=data_frame.iloc[i][popup_field],
                radius=int(data_frame.iloc[i][value_field] * proportion),
                color=color,
                fill=True,
                fill_color=fill_color))
    # We return our map with the circle
    return v_map
