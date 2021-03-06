"""
@author: Shaun
"""

import requests

import helper


def get_selective_movie_details(movie_id, details, list_details):
    """
    Gets the specific movie details from all the movie details. Movie specified by the movie_id
    """

    movie_details = __get_movie_details(movie_id)
    movie_details = helper.trim_dict(movie_details, details, list_details)

    return movie_details


def __get_movie_details(movie_id):
    """
    Returns all details of a movie, if the movie with the movie_id is found

    :param movie_id: id of the movie that we're seeking details for
    :return: all movie's details, if the movie with the id is found. else None
    """

    if movie_id == None:
        return None

    request = helper.get_movie_url(movie_id)
    response = requests.request("GET", request)

    if not response.ok:
        return None

    return response.json()


def get_parent_company(company_id):
    """
    Get parent company of the company by the company id provided
    """

    request = helper.get_company_url(company_id)
    response = requests.request("GET", request)

    if not response.ok:
        print("Failed")
        return None

    return response.json()["parent_company"]
