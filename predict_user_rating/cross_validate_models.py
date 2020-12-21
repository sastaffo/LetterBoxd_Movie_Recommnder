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
    plot_mean_with_deviation("%s C value comparison"%(title), "C value", hyperparameters, mean_error, standard_deviations)

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
                  'film_rate_ratio', 'film_like_ratio', 'user_film_watched', 'director_avg']
    #x, y = read_in_csv_file("data_points/pairs_0.csv", parameter_list) # Can test with just one file
    x, y = read_in_csv_files("training_points", parameter_list)
    cross_validate_penalty_parameter(x, y, "Lasso Regression", create_lasso_regression, [0.1, 1, 10, 100, 1000])
    cross_validate_penalty_parameter(x, y, "Ridge Regression", create_ridge_regression, [0.0001, 0.1, 1, 10])
    display_graphs()
