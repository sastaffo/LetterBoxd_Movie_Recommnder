import helper

## TODO: function that gets all movie ids

def get_specific_movie_details(movie_id, details, list_details):

    ## TODO: this one separate?
    movie_details = helper.get_movie_details(movie_id)
    movie_details = helper.trim_dict(movie_details, details, list_details)

    return movie_details

def get_movie_id(film):

    # NOTE
    #   movie_id will sought from films
    #   if(movie_id == None) get IMDB id
    movie_id = 76341

    return movie_id
