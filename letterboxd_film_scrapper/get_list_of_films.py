'''
Created on 16 Nov 2020

@author: bradishp
'''
import jsonpickle
import random
import re
import time
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from math import floor

BASE_URL = "https://letterboxd.com/films/ajax/popular/genre/%s/size/small/page/%d/"
MOST_POPULAR_FILMS = 100
TOTAL_FILMS = 500

class Genre():
    
    def __init__(self, name):
        self.name = name
        self.film_list = []
        
    def add_film(self, film):
        self.film_list.append(film)
        
    def add_random_movie_indexes(self, total_movies):
        self.random_film_indexes = set([])
        top_fifteen_percent = (total_movies/100)*15
        max_sample = max(top_fifteen_percent, 1000)
        while len(self.random_film_indexes) < TOTAL_FILMS - MOST_POPULAR_FILMS:
            random_movie_index = random.randint(MOST_POPULAR_FILMS, floor(max_sample))
            if random_movie_index not in self.random_film_indexes:
                self.random_film_indexes.add(random_movie_index)

            
class Film():
    
    def __init__(self, name, letterboxd_id, url):
        self.name = name
        self.letterboxd_id = letterboxd_id
        self.url = url
        
    def __str__(self):
        return "name: %s\nid: %s\nurl: %s"%(self.name, self.letterboxd_id, self.url)

def output_genre(film_genre, dir_name):
    with open('%s/%s.json'%(dir_name, film_genre.name), 'w') as f:
        json_format = jsonpickle.encode(film_genre, unpicklable=False)
        print(json_format, file=f)
        
def extract_number(text):
    total_number_string = re.findall(r'[0-9,]+', text)
    return int(total_number_string[0].replace(',', ''))
    
def get_films_from_genres(film_genres, dir_path):
    for film_genre in film_genres:
        page_num = 1
        film_index = 0
        while(len(film_genre.film_list) < TOTAL_FILMS):
            url = BASE_URL%(film_genre.name, page_num)
            print("Searching page %s\n%d films collected"%(url, len(film_genre.film_list)))
            session = HTMLSession()
            page = session.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            
            if page_num == 1:
                heading = soup.find(class_='ui-block-heading')
                total_number = extract_number(heading.text)
                film_genre.add_random_movie_indexes(total_number)
            
            film_list = soup.find(class_='poster-list -p70 -grid')
            
            for film in film_list:
                film_details = film.find("div")
                if film_details != -1:
                    if film_index < MOST_POPULAR_FILMS or film_index in film_genre.random_film_indexes:
                        # One of the most popular movies or a randomly chosen one
                        film_name = film_details.get("data-film-name")
                        letterboxd_id = film_details.get("data-film-id")
                        film_url = film_details.get("data-film-link")
                        film_genre.add_film(Film(film_name, letterboxd_id, film_url))
                    film_index += 1
            page_num += 1
            page_wait_time = random.randint(0, 10)
            time.sleep(page_wait_time)
        genre_wait_time = random.randint(0, 20)
        time.sleep(genre_wait_time)
        output_genre(film_genre, dir_path)
    
if __name__ == '__main__':
    film_genres = [Genre('action'), Genre('adventure'), Genre("animation"), Genre("comedy"), Genre("crime"), Genre("documentary"), Genre("drama"), Genre("family"), \
                    Genre("fantasy"), Genre("history"), Genre("horror"), Genre("music"), Genre("mystery"), Genre("romance"), Genre("science-fiction"), Genre("thriller"), \
                    Genre("tv-movie"), Genre("war"), Genre("western")]
    get_films_from_genres(film_genres, "genre_films")
