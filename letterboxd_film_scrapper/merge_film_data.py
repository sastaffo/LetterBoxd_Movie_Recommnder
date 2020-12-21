'''
Created on 10 Dec 2020

@author: bradishp
'''
import json
import jsonpickle

STRING_WITHIN_BACKSLASHES_REGEX = '/[^//]*/'

def merge_film_info(letterboxd_file_name, tmdb_file_name, all_film_data_file_name):
    all_films_data = {}
    with open(letterboxd_file_name, 'r') as letterbox_file:
        with open(tmdb_file_name, 'r') as tmdb_file:
            letterboxd_data = json.load(letterbox_file)
            tmdb_data = json.load(tmdb_file)
            for lid, tmdb_film_data in tmdb_data.items():
                film_data = letterboxd_data.get(lid)
                movie_age = tmdb_film_data.get('movie_age')
                if film_data == None or movie_age == None:   # All movies should have an age
                    continue    # Film is invalid
                
                film_data.update(tmdb_film_data)
                reformat_film_data(film_data)
                all_films_data[lid] = film_data
                
    with open(all_film_data_file_name, 'w') as all_film_data_file:
        json_format = jsonpickle.encode(all_films_data, unpicklable=False)
        print(json_format, file=all_film_data_file)

def reformat_film_data(film_data):
    film_data['name'] = film_data['name'].lower()
    film_data['genres'] = [genre.lower() for genre in film_data['genres']]
    
    actors_urls = film_data.pop('actors_urls', None)
    if actors_urls is not None:
        actors_names = convert_actor_urls_to_name(actors_urls[:5])
        film_data['actor'] = actors_names
    elif 'actor' not in film_data:
        raise KeyError("No actors specified")
    
    director_url = film_data.pop('director_url', None)
    if director_url is not None:
        director = convert_url_to_name(director_url)
        film_data['director'] = director
    elif 'director' not in film_data:
        raise KeyError("No director specified")
    
    film_data['production_companies'] = [production_company['id'] for production_company in film_data['production_companies']]

def convert_actor_urls_to_name(actor_urls):
    actor_names = []
    for actor_url in actor_urls:
        actor_name = convert_url_to_name(actor_url)
        actor_names.append(actor_name)
    return actor_names
 
def convert_url_to_name(url):
    parts_of_url = url.split("/")
    return parts_of_url[2]
        
if __name__ == '__main__':
    merge_film_info("../all_film_data/test_all_films.json", "../all_film_data/test_film_details.json", "../all_film_data/test_all_film_data.json")
