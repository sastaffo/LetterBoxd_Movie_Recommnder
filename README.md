# LetterBoxd Movie Recommnder
Movie recommender system that uses data from Letterboxd and TMDB.

Different folders contain different parts of the project.

* collab_filtering - has code for filtering information of user-film pairs and carrying out collaborative filtering on the data.    
* datapoint_manufacturing_sarah -    
* file_samples -    
* letterboxd_film_scrapper - has scripts for getting films off Letterboxd.   
* predict_film_ratings - has a script for predicting the average rating of a Letterboxd film based on scrapped data. We briefly explored this area when we weren't sure we would get meaningful results for user predictions, but we ended up not using it.    
* predict_user_rating - has scripts for training a model to predict a user's rating of a film. Includes code for cross validation.    
* sarah_data -    
* tmdb_film_detail_fetcher - has code which users a file containing the tmdb ids of movies, to fetch specific details about those movies from the tmdb api, and add some more fields using the fields fetched.    
* user_collection_sarah -    
