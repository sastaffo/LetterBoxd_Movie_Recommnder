"""
@author: Shaun
"""

import constants

def get_movie_url(id):
    return constants.TMDB_MOVIE_URL.format(movie_id = id)

def get_company_url(id):
    return constants.TMDB_COMPANY_URL.format(company_id = id)


def trim_dict(dict, keys, list_keys):
    """
    Make dict smaller - as we need only some details
    """

    if keys is None or dict is None:
        return dict

    return_list = False
    if len(keys) == 1:
        return dict[keys[0]]

    trimmed_dict = {}

    for key in keys:
        val = None

        if key in dict:
            val = dict[key]
            if list_keys is not None and key in list_keys and isinstance(val, list):
                val = trim_dicts_in_lists(val, list_keys[key])

        trimmed_dict[key] = val

    return trimmed_dict


def trim_dicts_in_lists(list, keys):
    """
    Make some lists in the dictionary smaller (eg: we dont need logo path of a production company)
    """

    if list == None:
        return None

    trimmed_list = []

    for elem in list:
        if isinstance(elem, dict):
            trimmed_list.append(trim_dict(elem, keys, None))

    return trimmed_list
