# LetterBoxd Movie Recommnder
Movie recommender system that uses data from Letterboxd and TMDB.

Different folders contain different parts of the project.

* collab_filtering - has code for filtering information of user-film pairs and carrying out collaborative filtering on the data.    
* datapoint_manufacturing - has code that takes in collected film and user data and manufactures datapoints to feed into the models    
* file_samples - since we collected too much data to post on github, we added some examples of the files here. contains the data of a sample LetterBoxd user, samples of film data gathered from LetterBoxd and TMDb, and a sample user-film pair, both in json and csv form.
* letterboxd_film_scraper - has scripts for getting films off Letterboxd.  
* predict_film_ratings - has a script for predicting the average rating of a Letterboxd film based on scrapped data. We briefly explored this area when we weren't sure we would get meaningful results for user predictions, but we ended up not using it.    
* predict_user_rating - has scripts for training a model to predict a user's rating of a film. Includes code for cross validation.    
* tmdb_film_detail_fetcher - has code which users a file containing the tmdb ids of movies, to fetch specific details about those movies from the tmdb api, and add some more fields using the fields fetched.    
* user_collection - has code that collects usernames and user information from LetterBoxd     
