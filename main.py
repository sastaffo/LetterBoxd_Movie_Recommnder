# TODO: good code in all files
# TODO: function comments
# TODO: separate files (functions and constants)
# TODO: error checking in needed functions
# TODO: access modifiers

import helper
import constants

# from tmdbv3api import TMDb
# from tmdbv3api import Movie
import requests
import dateutil.parser as date_parser
import datetime

#
# def initIds(films):
#
#     for film in films:
#         if(film.Id == None):
#             film.id = getImdbId(film)
#
#     return films
#
#
# def getImdbId(film):

# def getDetails():



# tmdb = TMDb()
# tmdb.api_key = 'cca18093a5d24304779e745f384197a1'
# tmdb.language = 'en'
# tmdb.debug = True
# Environment variable: export TMDB_API_KEY='YOUR_API_KEY'

# movie = Movie(76341)

# print(str(movie))

# recommendations = movie.recommendations(movie_id=111)
#
# for recommendation in recommendations:
#     print(recommendation.title)
#     print(recommendation.overview)
#
def get_film_details(film, details, list_details):

    movie_id = get_movie_id(film)
    movie_details = helper.get_movie_details(movie_id)
    movie_details = helper.trim_dict(movie_details, details, list_details)

    return movie_details


def get_movie_id(film):

    # NOTE
    #   movie_id will sought from films
    #   if(movie_id == None) get IMDB id
    movie_id = 76341

    return movie_id


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




def pretty_print(d, indent=0):
    for key, value in d.items():
          print('\t' * indent + str(key))
          if isinstance(value, dict):
             pretty_print(value, indent+1)
          else:

             print('\t' * (indent+1) + str(value))

# MAIN:
d = get_film_details(None, constants.MOVIE_KEYS, constants.LIST_KEYS)
d = post_call_work(d)
pretty_print(d)
