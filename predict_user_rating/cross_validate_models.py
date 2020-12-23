'''
Created on 21 Dec 2020

@author: bradishp
'''
import numpy as np
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from predict_user_rating.plot_graphs import display_graphs, plot_mean_with_deviation
from predict_user_rating.read_in_features import read_in_csv_files, read_in_csv_file
from sklearn.neighbors import KNeighborsRegressor

def create_lasso_regression(C):
    return Lasso(alpha=(1/(2*C)), max_iter=100000)

def create_ridge_regression(C):
    return Ridge(alpha=(1/(2*C)), max_iter=100000)

def cross_validate_penalty_parameter(x, y, title, create_model_func, hyperparameters):
    number_of_folds = 5
    mean_error=[]
    standard_deviations=[]
    for C in hyperparameters:
        model = create_model_func(C)
        results = cross_validate(model, x, y, number_of_folds)
        mean_error.append(results.mean())
        standard_deviations.append(results.std())
    plot_mean_with_deviation("%s C value comparison"%(title), "C", hyperparameters, mean_error, standard_deviations)
    
def cross_validate_nearest_neighbours_parameter(x, y, title, hyperparameters):
    number_of_folds = 5
    mean_error=[]
    standard_deviations=[]
    for k in hyperparameters:
        model = KNeighborsRegressor(n_neighbors=k, weights='uniform')
        results = cross_validate(model, x, y, number_of_folds)
        mean_error.append(results.mean())
        standard_deviations.append(results.std())
    plot_mean_with_deviation("%s k value comparison"%(title), "K", hyperparameters, mean_error, standard_deviations)

def cross_validate(model, x, y, number_of_folds):
    temp = []
    kf = KFold(n_splits = number_of_folds)
    for train, test in kf.split(x):
        model.fit(x[train], y[train])
        ypred = model.predict(x[test])
        temp.append(mean_squared_error(y[test], ypred))
    return np.array(temp)

if __name__ == '__main__':
    parameter_list = ['film_avg_rating', 'user_avg_rating', 'film_total_likes', 'film_total_views', 'film_total_ratings', 'film_age', 'film_franchise', \
                  'film_rate_ratio', 'film_like_ratio', 'user_film_watched', 'director_avg', 'action_avg', 'adventure_avg', 'comedy_avg', 'crime_avg', \
                  'documentary_avg', 'drama_avg', 'family_avg', 'fantasy_avg', 'history_avg', 'horror_avg', 'music_avg', 'mystery_avg', 'romance_avg',\
                  'science fiction_avg', 'thriller_avg', 'tv movie_avg', 'war_avg', 'western_avg']
    #x, y = read_in_csv_file("training_points/pairs_0.csv", parameter_list) # Can test with just one file
    x, y = read_in_csv_files("training_points", parameter_list)
    cross_validate_penalty_parameter(x, y, "Lasso Regression", create_lasso_regression, [0.1, 1, 10, 100, 1000])
    cross_validate_penalty_parameter(x, y, "Ridge Regression", create_ridge_regression, [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10])
    #cross_validate_nearest_neighbours_parameter(x, y, "K nearest neighbours", [1, 10, 100, 200, 500]) # Very computationally expensive
    display_graphs()
