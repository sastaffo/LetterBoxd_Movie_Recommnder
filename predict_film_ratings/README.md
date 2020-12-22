# LetterBoxd Movie Recommnder 
Script for predicting average rating of Letterboxd films.

* baseline_film_ratings_models.py - predicts the average rating of a film on Letterboxd using data collected from Letterboxd and TMDB. Can get high accuracy (within half a star). Input must be in json format in a a file all_film_data/all_film_data.json. Json file must have fields for number_of_likes, number_of_views, number_of_ratings, movie_age, in_franchise and lists of genres and production_companies which it will perform one hot encoding on. Output avg_rating must also be included in the json.
