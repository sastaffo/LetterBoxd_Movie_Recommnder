import keys

API_KEY = keys.TMDB_KEY
TMDB_URL = "https://api.themoviedb.org/"

MOVIE_KEYS = [ "belongs_to_collection", "budget", "original_language", "production_companies", "production_countries", "release_date", "revenue", "runtime" ]

LIST_KEYS = { "production_companies": ["name", "id"],
               "production_countries": ["name"] }

# production_companies(array) -> name, id
# production_countries (array) -> name
