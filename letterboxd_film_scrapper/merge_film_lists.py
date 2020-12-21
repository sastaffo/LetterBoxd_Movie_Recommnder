'''
Created on 7 Dec 2020

@author: bradishp
'''
import os
import json
import jsonpickle

def merge_films(dir_path, output_file):
    all_film_dict = {}
    directory = os.fsencode(dir_path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open("%s/%s"%(dir_path, filename), 'r') as f:
            films = json.load(f)
        film_list = films['film_list']
        if type(film_list) is dict:
            for (lid, film) in film_list.items():
                if film["tmdb_id"] != "":
                    all_film_dict[lid] = film
        elif type(film_list) is list:
            for film in film_list:
                if film["tmdb_id"] != "":
                    all_film_dict[film['lid']] = film
    with open(output_file, 'w') as f:
        json_format = jsonpickle.encode(all_film_dict, unpicklable=False)
        print(json_format, file=f)

def merge_users(dir_path, output_file):
    all_users = []
    directory = os.fsencode(dir_path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open("%s/%s"%(dir_path, filename), 'r') as f:
            users = json.load(f)
        all_users += users
    with open(output_file, 'w') as f:
        json_format = jsonpickle.encode(all_users, unpicklable=False)
        print(json_format, file=f)

if __name__ == '__main__':
    merge_films("../test_films", "../test_all_films.json")
    merge_users("../test_users", "../test_users.json")
