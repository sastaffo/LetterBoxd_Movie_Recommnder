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
                if film_data == None:   # Film is invalid
                    continue
                film_data.update(tmdb_film_data)
                
                film_data['name'] = film_data['name'].lower()
                film_data['genres'] = [genre.lower() for genre in film_data['genres']]
                actors_urls = film_data.pop('actors_urls', None)
                if actors_urls is not None:
                    actors_names = convert_actor_urls_to_name(actors_urls[:5])
                    film_data['actors'] = actors_names
                elif 'actors' not in film_data:
                    print("No actors specified")
                    raise ValueError()
                director_url = film_data.pop('director_url', None)
                if director_url is not None:
                    director = convert_url_to_name(director_url)
                    film_data['director'] = director
                elif 'director' not in film_data:
                    print("No director specified")
                    raise ValueError()
                
                all_films_data[lid] = film_data
                
    with open(all_film_data_file_name, 'w') as all_film_data_file:
        json_format = jsonpickle.encode(all_films_data, unpicklable=False)
        print(json_format, file=all_film_data_file)

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
    merge_film_info("../all_film_data/all_films.json", "../all_film_data/tmdb_data.json", "../all_film_data/all_film_data.json")
