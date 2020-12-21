"""
@author: Shaun
"""

# import printer # - this can be helpful for debugging
import movie_utils
import constants
import tmdb_api
import helper

import requests
import json_utils
import dateutil.parser as date_parser
import datetime
import time
import random


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        date_parser.parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def post_call_work(movie_details):
    """
    After getting data from calls, adds additional fields if movie_details received is a dictionary
    """
    if not isinstance(movie_details, dict):
        return None

    return additional_details(movie_details)


def additional_details(movie_details):
    """
    Adds the more needed fields which can be calculated based on field values that already exist for the movie dictionary
    """

    if "belongs_to_collection" in movie_details:
        movie_details["in_franchise"] = movie_details["belongs_to_collection"] is not None

    if "revenue" in movie_details and "budget" in movie_details:
        revenue = movie_details["revenue"]
        budget = movie_details["budget"]
        movie_details["profit"] = revenue - budget

    if "release_date" in movie_details:
        release_date = movie_details["release_date"]
        if is_date(release_date):
            movie_details["release_year"] = date_parser.parse(release_date).year
        else:
            movie_details["release_year"] = ""

    if "release_year" in movie_details:
        if is_date(release_date):
            curr_year = datetime.datetime.now().year
            release_year = movie_details["release_year"]
            movie_details["movie_age"] = curr_year - release_year
            decade = (int) (release_year/10)
            decade = decade * 10
            movie_details["release_decade"] = decade
        else:
            movie_details["movie_age"] = ""
            movie_details["release_decade"] = ""

    country_groups = json_utils.read_from_file("continent_country_pairs.json")
    if "production_countries" in movie_details:
        movie_details["production_country_group"] = []
        for country_name in movie_details["production_countries"]:
            country_name = country_name.lower()
            for country in country_groups:
                curr_country_name = country["country"].lower()
                same_country = (country_name in curr_country_name) or (curr_country_name in country_name)
                if same_country:
                    continent = country["continent"]
                    movie_details["production_country_group"].append(continent)
                    break

    if "belongs_to_collection" in movie_details:
        movie_details["belongs_to_collection"] = helper.trim_dict(movie_details["belongs_to_collection"], ["name", "id"], None)

    return movie_details


# Main function
def main():
    """
    Get films for letterbox_data. Then use the tmdb api to get details about all these films.
    Finally, create a countries list by continent file.
    """
    result = {}

    # films = json_utils.read_from_file("letterbox_data/films.json") # - for films
    films = json_utils.read_from_file("letterbox_data/test_all_films.json") # - for test films
    i = 1

    # get all details of the films present in the films file, from the tmdb_api
    for lid in films:
        film = films[lid]
        if film == None:
            continue
        movie_id = film["tmdb_id"]
        if movie_id == "" or movie_id == None: #disregard films with no tmdb_id
            continue
        d = tmdb_api.get_selective_movie_details(movie_id, constants.MOVIE_KEYS, constants.LIST_KEYS)
        print("Parsing film " + str(i) + ", with lid " + str(lid))
        if d is None:
            d = {}
        d["name"] = film["name"]
        d["tmdb_id"] = movie_id
        d = post_call_work(d)
        i = i + 1
        time.sleep(random.randint(15, 30))
        result[lid] = d
        json_utils.write_to_file(result, "tmdb_film_details.json")


    # Get the manual file created of continent_country_pairs
    continents_countries = {}
    country_groups = json_utils.read_from_file("continent_country_pairs.json")

    # Create a list of countries in each continent (NOTE: another team member needs this file)
    for country_dict in country_groups:
        continent = country_dict["continent"]
        country = country_dict["country"]
        if continent not in continents_countries:
            continents_countries[continent] = []
        continents_countries[continent].append(country)

    # Write the list of countries by continent to a file (another team member needs this file)
    json_utils.write_to_file(continents_countries, "countries_by_continent.json")


# Code Execution Control point
if __name__ == "__main__":
    main()
