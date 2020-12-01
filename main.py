# TODO: good code in all files
# TODO: function comments
# TODO: separate files (functions and constants)
# TODO: error checking in needed functions
# TODO: access modifiers

import movie_utils
import printer
import constants

# from tmdbv3api import TMDb
# from tmdbv3api import Movie
import requests
import dateutil.parser as date_parser
import datetime


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

    return movie_details


# MAIN:
if __name__ == "__main__":
    d = movie_utils.get_specific_movie_details(76341, constants.MOVIE_KEYS, constants.LIST_KEYS)
    d = post_call_work(d)
    printer.pretty_print_dict(d)
