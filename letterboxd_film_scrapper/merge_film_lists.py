'''
Created on 7 Dec 2020

@author: bradi
'''
import os
import json
import jsonpickle

def merge_films():
    all_film_dict = {}
    directory = os.fsencode("../films")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open("../films/%s"%(filename), 'r') as f:
            films = json.load(f)
        film_list = films['film_list']
        if type(film_list) is dict:
            for (lid, film) in film_list.items():
                all_film_dict[lid] = film
        elif type(film_list) is list:
            for film in film_list:
                all_film_dict[film['lid']] = film
    with open("../films/all_films.json", 'w') as f:
        json_format = jsonpickle.encode(all_film_dict, unpicklable=False)
        print(json_format, file=f)

def merge_users():
    all_users = []
    directory = os.fsencode("../users")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open("../%s/%s"%("users", filename), 'r') as f:
            users = json.load(f)
        all_users += users
    with open("../users/all_users.json", 'w') as f:
        json_format = jsonpickle.encode(all_users, unpicklable=False)
        print(json_format, file=f)

if __name__ == '__main__':
    merge_users()
