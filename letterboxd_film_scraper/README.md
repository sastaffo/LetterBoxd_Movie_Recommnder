# LetterBoxd Movie Recommnder
*author: XanthusXX (Philip Bradish 16339490)*

Code for scraping the film data off Letterboxd and combining all the film data together.

* get_failed_films.py - Deprecated script for getting films which failed the first pass of the system using the console output. No longer needed.
* get_film_details.py - Takes in a folder containing a list of films in json format and gathers data from each one off Letterboxd. Films will be put in a folder called films. Lists of random users will also be collected and will be put in a folder called users. Any films which we can't get the details for will be put in a folder called invalid_films.
* get_list_of_films.py - Gets a list containing n most popular films and m random films from each genre. n and m can be set within the file. Will output a json file for each genre to a folder called genre_films.
* merge_film_data.py - Merges the data collected from TMDB and Letterboxd into a single json.
* merge_film_lists.py - Merges all the films output by get_film_details.py into one json file. Can also merge all users together.
