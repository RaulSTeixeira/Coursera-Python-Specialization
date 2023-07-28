# MADE BY RAUL TEIXEIRA - 26.07.2023

"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline="") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """

    data_base = read_csv_as_nested_dict(
        codeinfo["codefile"], codeinfo["plot_codes"], codeinfo["separator"], codeinfo["quote"]
    )

    dict_converter = {}
    for row in data_base:
        dict_converter[row] = data_base[row][codeinfo["data_codes"]]

    return dict_converter


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    converter_plot_gdp = build_country_code_converter(codeinfo)

    def convert_dict_keys_and_values_to_lower(dictionary):
        lower_case_dict = {}
        for key, value in dictionary.items():
            if isinstance(key, str):
                lower_key = key.lower()
            else:
                lower_key = key

            if isinstance(value, str):
                lower_value = value.lower()
            else:
                lower_value = value

            lower_case_dict[lower_key] = lower_value

        return lower_case_dict

    converter_plot_gdp_mod = convert_dict_keys_and_values_to_lower(converter_plot_gdp)

    gdp_country_code_lst = []
    for gpd_country_code in gdp_countries:
        gdp_country_code_lst.append(gpd_country_code.lower())

    output_dict = {}
    output_set = set()

    for plot_country_code in plot_countries:
        gdp_country_code_converted = converter_plot_gdp_mod.get(plot_country_code.lower(), None)
        if gdp_country_code_converted is None:
            output_set.add(plot_country_code)
        else:
            if (gdp_country_code_converted.lower()) in gdp_country_code_lst:
                for gpd_country_code in gdp_countries:
                    if gdp_country_code_converted.lower() == gpd_country_code.lower():
                        output_dict[plot_country_code] = gpd_country_code
            else:
                output_set.add(plot_country_code)
    return output_dict, output_set


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """

    gdp_data_base = read_csv_as_nested_dict(
        gdpinfo["gdpfile"], gdpinfo["country_code"], gdpinfo["separator"], gdpinfo["quote"]
    )
    gdp_selected_countries = reconcile_countries_by_code(codeinfo, plot_countries, gdp_data_base)

    output_dict = {}
    output_set1 = gdp_selected_countries[1]
    output_set2 = set()

    for plot_countries_codes in gdp_selected_countries[0]:
        if gdp_data_base[gdp_selected_countries[0][plot_countries_codes]][year] != "":
            output_dict[plot_countries_codes] = math.log(
                float(gdp_data_base[gdp_selected_countries[0][plot_countries_codes]][year]), 10
            )
        else:
            output_set2.add(plot_countries_codes)

    return output_dict, output_set1, output_set2


# Testing the last function
# gdpinfo = {
#         "gdpfile": "isp_gdp.csv",
#         "separator": ",",
#         "quote": '"',
#         "min_year": 1960,
#         "max_year": 2015,
#         "country_name": "Country Name",
#         "country_code": "Country Code"
#     }

# codeinfo = {
#         "codefile": "isp_country_codes.csv",
#         "separator": ",",
#         "quote": '"',
#         "plot_codes": "ISO3166-1-Alpha-2",
#         "data_codes": "ISO3166-1-Alpha-3"
#     }

# plot_countries = {'xxx': 'yyyy'}
# year = '1960'

# print(build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year))


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """

    data_base = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = f"GDP per Country for the year {year}"
    worldmap_chart.add(f"GDP for {year}", data_base[0])
    worldmap_chart.add("Missing data", data_base[1])
    worldmap_chart.add(f"No GDP data for {year}", data_base[2])

    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code",
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3",
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
