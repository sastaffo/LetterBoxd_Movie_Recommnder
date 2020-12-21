"""
@author: Shaun
"""

import os
import json
import time

def get_refined_list(films):
    """
    Takes list of film dictionaries and reduces it to a list of smaller film dictionaries, containing only user_id, film_id and user's rating for the film

    :param films: List of film dictionaries
    :return: List of reduced (smaller) film dictionaries, with user_id, film_id, film rating
    """

    # Iterate through list of dicts, create smaller dicts by taking specific fields and append to a list
    refined_list = []
    for film in films:
        refined_dict = {}
        refined_dict["user_lid"] = film["user_lid"]
        refined_dict["film_lid"] = film["film_lid"]
        refined_dict["user_rating_for_film"] = film["user_rating_for_film"]
        refined_list.append(refined_dict)

    return refined_list


def main():

    # Record starting time
    start = time.time()

    # Get list of all filenames in the directory
    dir = "user_film_merge/"
    user_film_files = os.listdir(dir)

    # Iterate through files, reduce the dictionaries in the lists of all files, and make a reduced list (list with smaller dicitonaries - with only the necessary fields)
    refined_data = []
    for filename in user_film_files:
        filepath = dir + filename
        with open(filepath) as fp:
            films_in_file = json.load(fp)
            refined_list = get_refined_list(films_in_file)
            refined_data.extend(refined_list)

    # Write the refined list to a json file
    with open("refined_film_data.json", 'w') as fp:
        fp.write(json.dumps(refined_data))

    # Record end time and print how much time this code took to run
    end = time.time()
    time_gap = end - start
    print("Time taken to refine all lists: " + str(time_gap))


if __name__ == '__main__':

    main()
