# TODO: good code in all files
# TODO: function comments
# TODO: separate files (functions and constants)
# TODO: error checking in needed functions
# TODO: access modifiers

import movie_utils
import printer
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

    if not isinstance(movie_details, dict):
        return None

    return additional_details(movie_details)


def additional_details(movie_details):

    if "belongs_to_collection" in movie_details:
        movie_details["in_franchise"] = movie_details["belongs_to_collection"] is not None

    # TODO: Check types here if appropriate
    if "revenue" in movie_details and "budget" in movie_details:
        revenue = movie_details["revenue"]
        budget = movie_details["budget"]
        movie_details["profit"] = revenue - budget

    #TODO: check for errors here
    if "release_date" in movie_details:
        release_date = movie_details["release_date"]
        if is_date(release_date):
            movie_details["release_year"] = date_parser.parse(release_date).year
        else:
            movie_details["release_year"] = ""

    #TODO: check for errors here
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

            # url = "https://maps.googleapis.com/maps/api/geocode/json?components=country:{country}&key={key}".format(country = country, key = "AIzaSyC2L6z8n-ZzW74DgYQP8i5jxWPEjQOtXZs")
            # response = requests.request("GET", url)
            #
            # short_name = ""
            #
            # if not response or not response.json()["status"] == "OK":
            #     print("You're a failure Shaun :D")
            #     return
            # else:
            #     short_name =  response.json()["results"][0]["address_components"][0]["short_name"]
            #     print country_codes[short_name]

    #TODO: check errors
    # if "production_countries" in movie_details:
    #     movie_details["production_country_group"] = []
    #     for country_dict in movie_details["production_countries"]:
    #         country_name = country_dict["name"]
    #         country_code = pycountry.country_name_to_country_alpha2(country_name, cn_name_format = "default")
    #         continent_name = pycountry.country_alpha2_to_continent_code(country_code)
    #         movie_details["production_country_group"].append({"name":continent_name})

    return movie_details

# def find_continent(country_code):
#
#     for country_dict in country_info.countries:
#         if country_dict["code"] == country_code:
#             return country_dict["continent"]

# Main function
def main():
    # TODO: HERES THE PLAN
    # get all movie ids -> func call
    # init missing movie_ids -> func call
    # Init json doc if it doesn't exist
    # Func with loop over ids:
    #   Get one movie's details
    #   Trim details
    #   Print to json doc
    #   Wait 15-30 seconds

    # NOTE: START
    # result = {}
    #
    # films = json_utils.read_from_file("letterbox_data/films.json")
    # i = 1
    # for lid in films:
    #     film = films[lid]
    #     if film == None:
    #         continue
    #     movie_id = film["tmdb_id"]
    #     d = tmdb_api.get_selective_movie_details(movie_id, constants.MOVIE_KEYS, constants.LIST_KEYS)
    #     print("Parsing film " + str(i) + ", with lid " + str(lid))
    #     if d is None:
    #         d = {}
    #     d["name"] = film["name"]
    #     d["tmdb_id"] = movie_id
    #     d = post_call_work(d)
    #     # printer.pretty_print_dict(d)
    #     i = i + 1
    #     time.sleep(random.randint(15, 30))
    #     result[lid] = d
    #     json_utils.write_to_file(result, "tmdb_film_details.json")
    #
    #
    # continents_countries = {}
    # country_groups = json_utils.read_from_file("continent_country_pairs.json")
    #
    # for country_dict in country_groups:
    #     continent = country_dict["continent"]
    #     country = country_dict["country"]
    #     if continent not in continents_countries:
    #         continents_countries[continent] = []
    #     continents_countries[continent].append(country)

    # json_utils.write_to_file(continents_countries, "countries_by_continent.json")


    films_data = json_utils.read_from_file("letterbox_data/films.json")
    cleaned_up_films_data = {}

    for key in films_data:
        film_data = films_data[key]
        if film_data["tmdb_id"] == "":
            continue
        cleaned_up_films_data[key] = film_data

    json_utils.write_to_file(cleaned_up_films_data, "tmdb_film_details.json")
    # NOTE: END



    # # NOTE: GOOGLE MAPS: WORKS
    # country = "united kinGDom"
    # url = "https://maps.googleapis.com/maps/api/geocode/json?components=country:{country}&key={key}".format(country = country, key = "AIzaSyC2L6z8n-ZzW74DgYQP8i5jxWPEjQOtXZs")
    # response = requests.request("GET", url)
    #
    # if not response or not response.json()["status"] == "OK":
    #     print("You're a failure Shaun :D")
    #     return
    # else:
    #     print response.json()["results"][0]["address_components"][0]["short_name"]

    # NOTE: DIFF RATIO = 0.6: WORKS
    # print SequenceMatcher(None, "united states of america".lower(), "United States".lower()).ratio()

    # # NOTE: GOOGLE MAPS WITH FILE FOR CONTINENT: WORKS BUT USE THE RIGHT COUNTRY NAME
    # country = "united states"
    # url = "https://maps.googleapis.com/maps/api/geocode/json?components=country:{country}&key={key}".format(country = country, key = "AIzaSyC2L6z8n-ZzW74DgYQP8i5jxWPEjQOtXZs")
    # response = requests.request("GET", url)
    #
    # short_name = ""
    #
    # if not response or not response.json()["status"] == "OK":
    #     print("You're a failure Shaun :D")
    #     return
    # else:
    #     short_name =  response.json()["results"][0]["address_components"][0]["short_name"]
    #     print country_codes[short_name]


    # print(i)
    # print(len(result["films_details"]))

    # print(len(films["film_list"]))


# Code Execution Control point
if __name__ == "__main__":
    main()
