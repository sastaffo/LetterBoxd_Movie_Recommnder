'''
Created on 1 Dec 2020

@author: bradishp
'''
import json
import jsonpickle
import os
import random
import re
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from letterboxd_film_scrapper.get_list_of_films import extract_number

BASE_URL = "https://letterboxd.com%s"
users = []
STRING_WITHIN_CURLY_BRACKETS_REGEX = '{.*}'
invalid_film_list = []

class Films():
    
    def __init__(self):
        self.film_list = {}
        
    def store_film(self, film):
        self.film_list[film.lid] = film
                
        
class Film():
    
    def __init__(self, name, url, lid, tmdb_id, number_of_ratings, avg_rating, genres, director_url, actors_urls, number_of_likes, number_of_views):
        self.name = name
        self.url = url
        self.lid = lid
        self.tmdb_id = tmdb_id
        self.number_of_ratings = number_of_ratings
        self.avg_rating = avg_rating
        self.genres = genres
        self.director_url = director_url
        self.actors_urls = actors_urls
        self.number_of_likes = number_of_likes
        self.number_of_views = number_of_views


def iterate_through_genres(genres_folder):
    directory = os.fsencode(genres_folder)
        
    for file in os.listdir(directory):
        genre_films = Films()
        filename = os.fsdecode(file)
        if filename.startswith('a') or filename.startswith('c') or filename.startswith('d'):
            continue
        with open("%s/%s"%(genres_folder, filename), 'r') as f:
            genre_details = json.load(f)
        get_film_details_for_genre(genre_films, genre_details)
        
        print("Outputting results for %s"%(genre_details['name']))
        output_to_json("films/users_%s"%(genre_details['name']), users)
        output_to_json("films/films_%s"%(genre_details['name']), genre_films)
        
        genre_wait_time = random.randint(0, 20)
        time.sleep(genre_wait_time)
    output_to_json("invalid_films/invalid_films", invalid_film_list)
            
def get_film_details_for_genre(films, genre_details):
    film_list = genre_details['film_list']
    for film in film_list:
        try:
            film_details = get_film_details(film)
            films.store_film(film_details)
            page_wait_time = random.randint(0, 10)
            time.sleep(page_wait_time)
        except Exception:   # Catch all exceptions to avoid exiting and loosing all the progress
            print("Invalid movie %s"%(film['name']))
            invalid_film_list.append(film)
    
def get_film_details(film_info):
    film_url = film_info['url']
    film_lid = film_info['letterboxd_id']
    film_name = film_info['name']
    
    page_url = BASE_URL%(film_url)
    print("Getting page %s"%(page_url))
    session = HTMLSession()
    page = session.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
        
    film_json = soup.find(type="application/ld+json")
    info_json = get_info_in_curly_brackets(film_json.contents[0])
    
    aggregate_rating = info_json["aggregateRating"]
    if aggregate_rating is None:
        print("Movie doesn't have enough ratings")
        raise TypeError()
    number_of_ratings = aggregate_rating["ratingCount"]
    avg_rating = aggregate_rating["ratingValue"]
    genres = info_json["genre"]
    director_url = info_json["director"][0]["sameAs"]
    
    actors_json = info_json["actors"]
    if actors_json: # Not all movies have actors
        actors_urls = [actor["sameAs"] for actor in actors_json]
    else:
        actors_urls = []
    
    number_of_likes, number_of_views = get_member_page_info(page_url, film_url)
    
    tmdb = soup.find(attrs={"data-tmdb-type" : "movie"})
    tmdb_id = tmdb.get("data-tmdb-id")
    
    return Film(name = film_name, url = film_url, lid = film_lid, tmdb_id = tmdb_id, number_of_ratings = number_of_ratings, avg_rating = avg_rating, genres = genres, \
                director_url = director_url, actors_urls = actors_urls, number_of_likes = number_of_likes, number_of_views = number_of_views)
    
def get_member_page_info(page_url, film_url):
    session = HTMLSession()
    members_list_url = "%smembers"%(page_url)
    print("Getting page %s"%(members_list_url))
    
    page = session.get(members_list_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    user_table = soup.find(class_="person-table film-table")
    user_table_body = user_table.find("tbody")
    user_list = user_table_body.findAll("tr")
    for user in user_list:
        user_rating = user.find(class_="film-detail-meta rating-green")
        if user_rating:
            user_info = user.find(class_="follow-button-wrapper js-follow-button-wrapper")
            username = user_info.get("data-username")
            users.append(username)
            break

    likes_info = soup.find(attrs={"href" : "%slikes/"%(film_url)})
    number_of_likes = extract_number(likes_info["title"])
    views_info = soup.find(attrs={"href" : "%smembers/"%(film_url)})
    number_of_views = extract_number(views_info["title"])
    return number_of_likes, number_of_views

def get_info_in_curly_brackets(info):
    match = re.search(STRING_WITHIN_CURLY_BRACKETS_REGEX, info)
    if match == None:
        print("Error couldn't find anything inside curly brackets in the string:\n%s"%(info))
        raise ValueError()
    json_output = json.loads(match.group(0))
    return json_output

def output_to_json(filename, obj):
    with open("%s.json"%(filename), 'w') as f:
        json_format = jsonpickle.encode(obj, unpicklable=False)
        print(json_format, file=f)

if __name__ == '__main__':
    iterate_through_genres("film_genres")
