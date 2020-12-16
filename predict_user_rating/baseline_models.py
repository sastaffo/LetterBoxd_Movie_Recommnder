'''
Created on 10 Dec 2020

@author: bradishp
'''
import json
import math
import numpy as np
import os
import time
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import MultiLabelBinarizer

# TODO maybe output parameters to a file instead
def disp_model_parameters(model):
    print("Theta0: %0.6f"%(model.intercept_), end = ", ")
    param_num = 1
    parameters = model.coef_
    if isinstance(parameters[0],(list, np.ndarray)):    # Some models have their parameters in a list within the list
        parameters = parameters[0]
        
    for param in parameters:
        print("Theta%d: %0.6f"%(param_num, param), end = ", ")
        param_num += 1
    print("\n")
    
def evaluate_linear_regression(x_train, y_train, x_test, y_test):
    model = LinearRegression()
    model.fit(x_train, y_train)
    evaluate_model("Linear regression", model, x_test, y_test)
    disp_model_parameters(model)

def evaluate_lasso_regression(x_train, y_train, x_test, y_test, C=1):
    model = Lasso(alpha=(1/(2*C)), max_iter=1000000)
    model.fit(x_train, y_train)
    evaluate_model("Lasso regression C=%d"%(C), model, x_test, y_test)
    disp_model_parameters(model)
    
def evaluate_average_baseline(x_train, y_train, x_test, y_test):
    model = DummyRegressor(strategy="mean")
    model.fit(x_train, y_train)
    evaluate_model("Average Baseline", model, x_test, y_test)
    print("Average baseline predicting a constant value of %f"%(model.constant_[0][0]))
    
def evaluate_constant_baseline(x_train, y_train, x_test, y_test, constant_value):
    model = DummyRegressor(constant=constant_value)
    model.fit(x_train, y_train)
    
    evaluate_model("Constant center value %f"%(constant_value), model, x_test, y_test)
    
def evaluate_model(label, model, x_test, y_test):
    ypred = model.predict(x_test)
    mean_sq_error = mean_squared_error(y_test, ypred)
    print("%s model %f"%(label, mean_sq_error))
    
def read_in_data(dir_name):
    print("Reading in the data")
    directory = os.fsencode(dir_name)
    all_user_films = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open("%s%s"%(dir_name, filename), 'r') as f:
            user_films = json.load(f)
            all_user_films += user_films
    return all_user_films

def read_in_test_file(filename):
    with open(filename, 'r') as f:
        user_films = json.load(f)
    return user_films

# Legacy method
def parse_data(user_films_data):
    print("Parsing the data")
    number_of_films = len(user_films_data)
    likes = np.zeros(number_of_films).reshape(number_of_films, 1)
    views = np.zeros(number_of_films).reshape(number_of_films, 1)
    rating_count = np.zeros(number_of_films).reshape(number_of_films, 1)
    film_age = np.zeros(number_of_films).reshape(number_of_films, 1)
    runtime = np.zeros(number_of_films).reshape(number_of_films, 1)
    in_franchise = np.zeros(number_of_films).reshape(number_of_films, 1)
    avg_rating = np.zeros(number_of_films)
    
    user_films_watched = np.zeros(number_of_films)

    feature_list = [likes, views, rating_count, film_age, runtime, in_franchise, avg_rating, user_films_watched]
    print("Parameters 1 = likes, 2 = views, 3 = ratings, 4 = movie age, 5 = runtime, 6 = in franchise, 7 = Average rating, 8 = Users films watched")
    
    # Output
    user_rating = np.zeros(number_of_films)
    
    film_index = 0
    for user_film in user_films_data:
        likes[film_index] = user_film['film_total_likes']
        views[film_index] = user_film['film_total_views']
        rating_count[film_index] = user_film['film_total_ratings']
        film_age[film_index] = user_film['film_age']
        in_franchise[film_index] = user_film['film_franchise']
        avg_rating[film_index] = user_film['film_avg_rating']

        film_runtime = user_film['film_runtime_min']
        runtime[film_index] = film_runtime
        if film_runtime == None or math.isnan(film_runtime):
            # TODO what should we do if movie doesn't have a runtime (only 1 so far FrightFest: Beneath the Dark Heart of Cinema)
            film_runtime = 0
        runtime[film_index] = film_runtime
        
        user_films_watched[film_index] = user_film['user_films_watched']

        user_rating[film_index] = user_film['user_previous_rating_not_seen_avg']
        film_index += 1
        
    features = np.column_stack(feature_list)
    
    return features, user_rating

def configurable_parse_data(user_films_data, parameter_list):
    number_of_data_points = len(user_films_data)
    print("Parsing all %d data points"%(number_of_data_points))
    parameters = create_parameters(parameter_list, number_of_data_points)
    y = np.zeros(number_of_data_points)
    film_index = 0
    for user_film in user_films_data:
        for parameter_name, parameter_values in parameters.items():
            value = user_film.get(parameter_name, None)
            if value == None or math.isnan(value) or math.isinf(value):
                print("User %s and film %s has an invalid value for %s"%(user_film['user_lid'], user_film['film_lid'], parameter_name))
                value = 0
            parameter_values[film_index] = value
        y[film_index] = user_film['user_rating_for_film']
        film_index += 1
        
    parameters_values = []
    param_index = 0
    print("Theta%d = base"%(param_index), end = "")
    param_index += 1
    for parameter_name, parameter_values in parameters.items():
        parameters_values.append(parameter_values)
        print(", Theta%d = %s"%(param_index, parameter_name), end = "")
        param_index += 1
    print(":")
    
    x = np.column_stack(parameters_values)
    y = y.reshape(number_of_data_points, -1)
    
    return x, y
    
def create_parameters(parameter_names, number_of_data_points):
    parameters = {}
    for parameter_name in parameter_names:
        parameters[parameter_name] = np.zeros(number_of_data_points)
    return parameters

def run_full_evaluation(all_user_films, parameter_list):
    x, y = configurable_parse_data(all_user_films, parameter_list)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)    # Use 20% for testing
    
    print("Training models")
    evaluate_linear_regression(x_train, y_train, x_test, y_test)
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 1)
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 100)
    evaluate_average_baseline(x_train, y_train, x_test, y_test)
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.5)
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.75)

'''
Sample film-user pair json
[{"user_lid": "qreeneyes", "user_rating_for_film": 4.5, "user_country": "united kingdom", "user_country_group": "Europe", "user_films_watched": 536, "user_average_rating": 3.388059701492537,
"film_lid": "51539", "film_avg_rating": 3.69, "film_total_views": 70727, "film_total_ratings": 33299, "film_rate_ratio": 0.47081029875436536, "film_total_likes": 11906,
"film_like_ratio": 0.16833741004142688, "film_prod_companies": [335, 2630], "film_prod_counties": ["united kingdom", "united states"], "film_prod_continents": ["Europe", "North America"],
"film_release_year": 1990, "film_release_month": "03", "film_age": 30, "film_runtime_min": 181, "film_franchise": false, "film_budget": 22000000, "film_revenue": 424208848,
"film_profit": 402208848, "film_language": null, "user_from_prod_country": true, "user_from_prod_continent": true, "user_director_avg": 4.5, "user_director_avg_minus avg": 1.111940298507463,
"user_genres_avg": [{"drama": 3.659090909090909}, {"western": 3.5}, {"adventure": 3.417293233082707}], "user_genres_avg_minus_avg": [{"drama": 0.27103120759837207}, 
{"western": 0.1119402985074629}, {"adventure": 0.029233531590169726}], "user_actors_avg": [{"actor0": 3.6666666666666665}, {"actor1": 4.5}, {"actor2": 4.5}, {"actor3": 4.5}, {"actor4": 4.5}],
"user_actors_avg_minus": [{"actor0": 0.2786069651741294}, {"actor1": 1.111940298507463}, {"actor2": 1.111940298507463}, {"actor3": 1.111940298507463}, {"actor4": 1.111940298507463}], 
"film_rating_minus_user_avg": 0.30194029850746285}
'''

if __name__ == '__main__':
    start = time.time()
    #all_user_films = read_in_test_file("../user_films_pairs/gen_000_099_film_pairs.json")    # Can test with just one file
    all_user_films = read_in_data("../user_films_pairs/")
    end = time.time()
    time_to_read_in_data = end - start
    print("Time taken to read in the data %d"%(time_to_read_in_data))

    print("\nVerbose Feature Set")
    parameter_list = ['film_total_likes', 'film_total_views', 'film_total_ratings', 'film_age', 'film_franchise', 'film_avg_rating', 'film_runtime_min', 'user_films_watched', 'film_age', \
                      'film_rating_minus_user_avg', 'film_rate_ratio', 'film_like_ratio', 'user_director_avg']
    run_full_evaluation(all_user_films, parameter_list)
    
    print("\nMedium Feature Set")
    parameter_list = ['film_age', 'film_franchise', 'film_avg_rating', 'film_runtime_min', 'user_films_watched', 'film_age', \
                      'film_rate_ratio', 'film_like_ratio']
    run_full_evaluation(all_user_films, parameter_list)
    
    print("\nSmall Feature Set")
    parameter_list = ['film_avg_rating', 'user_films_watched', 'film_rating_minus_user_avg']
    run_full_evaluation(all_user_films, parameter_list)
    
    end = time.time()
    time_to_run_program = end - start
    print("Time taken for the whole program in the data %d"%(time_to_run_program))
