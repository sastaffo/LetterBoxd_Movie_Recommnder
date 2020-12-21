"""
@author: Shaun
"""

import keys

API_KEY = keys.TMDB_KEY

TMDB_VERSION = "3"
TMDB_URL = "https://api.themoviedb.org/{v}".format(v = TMDB_VERSION)
TMDB_MOVIE_URL = "{url}/movie/{movie_id}?api_key={key}".format(url = TMDB_URL, movie_id = "{movie_id}", key = API_KEY)
TMDB_COMPANY_URL = "{url}/company/{company_id}?api_key={key}".format(url = TMDB_URL, company_id = "{company_id}", key = API_KEY)

MOVIE_KEYS = [ "belongs_to_collection", "budget", "original_language", "production_companies", "production_countries", "release_date", "revenue", "runtime" ]

LIST_KEYS = { "production_companies": ["name", "id"], # production_companies(array) -> name, id
               "production_countries": ["name"] } # production_countries (array) -> name
