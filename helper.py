import constants
import requests

def get_movie_url(id):
     return constants.TMDB_MOVIE_URL.format(movie_id = id)

def get_movie_details(movie_id):

    if movie_id == None:
        return None

    request = get_movie_url(movie_id)
    response = requests.request("GET", request)

    if not response.ok:
        return None

    return response.json()


def trim_dict(dict, keys, list_keys):

    trimmed_dict = {}

    for key in keys:
        val = None
        if key in dict:
            val = dict[key]

            if key in list_keys and isinstance(val, list):
                val = trim_dicts_in_lists(val, list_keys[key])

        trimmed_dict[key] = val

    return trimmed_dict


def trim_dicts_in_lists(list, keys):

    if list == None:
        return None

    trimmed_list = []

    for elem in list:
        if isinstance(elem, dict):
            trimmed_list.append(trim_dict(elem, keys, ""))

    return trimmed_list
