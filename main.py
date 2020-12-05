# TODO: good code in all files
# TODO: function comments
# TODO: separate files (functions and constants)
# TODO: error checking in needed functions
# TODO: access modifiers

import movie_utils
import printer
import constants
import tmdb_api
import json_utils
import country_info

# from tmdbv3api import TMDb
# from tmdbv3api import Movie
import requests
import dateutil.parser as date_parser
import datetime
import time
import random
import pycountry

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
        movie_details["release_year"] = date_parser.parse(release_date).year

    #TODO: check for errors here
    if "release_year" in movie_details:
        curr_year = datetime.datetime.now().year
        release_year = movie_details["release_year"]
        movie_details["movie_age"] = curr_year - release_year
        decade = (int) (release_year/10)
        decade = decade * 10
        movie_details["release_decade"] = decade

    #TODO: error checking
    if "production_companies" in movie_details:
        parent_companies = []
        for company_details in movie_details["production_companies"]:
            company_id = company_details["id"]
            parent_company = tmdb_api.get_parent_company(company_id)
            parent_companies.append(parent_company)
        movie_details["parent_companies"] = parent_companies

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

    result = { "films_details": [] }

    tmdb_ids = json_utils.read_from_file("letterbox_data/films")
    print(tmdb_ids)
    i = 1
    for film in tmdb_ids["film_list"]:
        if film == None:
            continue
        # print(str(i) + ": " + film["lid"] + ", " + film["name"] + ", " + film["tmdb_id"])
        movie_id = film["tmdb_id"]
        d = tmdb_api.get_selective_movie_details(movie_id, constants.MOVIE_KEYS, constants.LIST_KEYS)
        d["name"] = film["name"]
        d["lid"] = film["lid"]
        d["tmdb_id"] = movie_id
        d = post_call_work(d)
        # printer.pretty_print_dict(d)
        print("Film number " + str(i) + " parsed, with lid " + str(film["lid"]))
        i = i + 1
        time.sleep(random.randint(15, 30))
        result["films_details"].append(d)

    json_utils.write_to_file(result, "tmdb_film_details")

    # country = pycountry.countries.search_fuzzy('England')
    # country_code = country.alpha_2
    # find_continent(country_code)

    # print(i)
    # print(len(result["films_details"]))

    # print(len(tmdb_ids["film_list"]))

# Code Execution Control point
if __name__ == "__main__":
    main()
