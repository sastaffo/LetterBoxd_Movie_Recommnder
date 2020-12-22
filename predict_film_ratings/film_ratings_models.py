'''
Created on 10 Dec 2020

@author: bradishp
'''
import json
import math
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import MultiLabelBinarizer

ALL_FILM_DATA_FILE_PATH = "all_film_data/all_film_data.json"

# TODO maybe output parameters to a file instead
def disp_model_parameters(model):
    print("Theta 0: %0.6f"%(model.intercept_), end = ", ")
    param_num = 1
    parameters = model.coef_
    if isinstance(parameters[0],(list, np.ndarray)):    # Some models have their parameters in a list within the list
        parameters = parameters[0]
        
    for param in parameters:
        print("Theta %d: %0.6f"%(param_num, param), end = ", ")
        param_num += 1
    print("\n")
    
def evaluate_linear_regression(x_train, y_train, x_test, y_test):
    model = LinearRegression()
    model.fit(x_train, y_train)
    evaluate_model("Linear regression", model, x_test, y_test)
    disp_model_parameters(model)

def evaluate_lasso_regression(x_train, y_train, x_test, y_test, C=1):
    model = Lasso(alpha=(1/(2*C)))
    model.fit(x_train, y_train)
    evaluate_model("Lasso regression C=%d"%(C), model, x_test, y_test)
    disp_model_parameters(model)
    
def evaluate_average_baseline(x_train, y_train, x_test, y_test):
    model = DummyRegressor(strategy="mean")
    model.fit(x_train, y_train)
    evaluate_model("Average Baseline", model, x_test, y_test)
    
def evaluate_constant_baseline(x_train, y_train, x_test, y_test, constant_value):
    model = DummyRegressor(constant=constant_value)
    model.fit(x_train, y_train)
    
    evaluate_model("Constant center value %d"%(constant_value), model, x_test, y_test)
    
def evaluate_model(label, model, x_test, y_test):
    ypred = model.predict(x_test)
    print("%s model %f"%(label, mean_squared_error(y_test, ypred)))
    
def read_in_data():
    with open(ALL_FILM_DATA_FILE_PATH, 'r') as f:
        films = json.load(f)
    number_of_films = len(films)
    
    # Add fields
    # TODO change system to instead use users ratings and information about users
    # TODO still need to add information such as name(maybe), release decade(maybe could be done using one hot encoding),
    # production countries (maybe done using one hot encoding), revenue (may not be present for all), profit, production_country_group
    # (maybe related to users or one hot encoding), original(maybe related to users or one hot encoding)
    likes = np.zeros(number_of_films).reshape(number_of_films, 1)
    views = np.zeros(number_of_films).reshape(number_of_films, 1)
    rating_count = np.zeros(number_of_films).reshape(number_of_films, 1)
    movie_age = np.zeros(number_of_films).reshape(number_of_films, 1)
    runtime = np.zeros(number_of_films).reshape(number_of_films, 1)
    in_franchise = np.zeros(number_of_films).reshape(number_of_films, 1)
    
    feature_list = [likes, views, rating_count, movie_age, runtime, in_franchise]
    print("Parameters 1 = likes, 2 = views, 3 = ratings, 4 = movie age, 5 = runtime, 6 = in franchise")

    # Lists for one hot encoding
    genre_lists = []
    studio_lists = []
    
    # Output
    avg_rating = np.zeros(number_of_films)
    
    film_index = 0
    for film in films.values():
        likes[film_index] = film['number_of_likes']
        views[film_index] = film['number_of_views']
        rating_count[film_index] = film['number_of_ratings']
        movie_age[film_index] = film['movie_age']
        in_franchise[film_index] = film['in_franchise']
        
        film_runtime = film['runtime']
        runtime[film_index] = film_runtime
        if film_runtime == None or math.isnan(film_runtime):
            # TODO what should we do if movie doesn't have a runtime (only 1 so far FrightFest: Beneath the Dark Heart of Cinema)
            film_runtime = 0
        runtime[film_index] = film_runtime
        
        genre_lists.append(film['genres'])
        studio_lists.append(film['production_companies'])

        avg_rating[film_index] = film['avg_rating']
        film_index += 1
        
    mlb = MultiLabelBinarizer()
    multi_class_genres = mlb.fit_transform(genre_lists)
    print(mlb.classes)
    
    multi_class_studios = mlb.fit_transform(studio_lists)

    features = np.column_stack(feature_list)
    features = np.concatenate((multi_class_genres, features), axis=1)
    #features = np.concatenate((multi_class_studios, features), axis=1)    # Currently damaging performance
    
    return features, avg_rating

if __name__ == '__main__':
    x, y = read_in_data()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)    # Use 20% for testing
    
    evaluate_linear_regression(x_train, y_train, x_test, y_test)
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 1)
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 100)
    evaluate_average_baseline(x_train, y_train, x_test, y_test)
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.5)
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.75)
