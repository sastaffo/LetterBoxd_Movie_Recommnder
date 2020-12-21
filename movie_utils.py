"""
@author: Shaun
"""

import helper
import tmdb_api

def get_specific_movie_details(movie_id, details, list_details):
    """
    Get movie details of the movie specified by the movie id. Get only those details specified by details (dict_details) and list_details
    """

    movie_details = tmdb_api.__get_movie_details(movie_id)
    movie_details = helper.trim_dict(movie_details, details, list_details)

    return movie_details
