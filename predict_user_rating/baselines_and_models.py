'''
Created on 10 Dec 2020

@author: bradishp
'''
import numpy as np
import time
from predict_user_rating.input_feature_baseline import InputFeatureBaseline
from predict_user_rating.read_in_features import read_in_csv_files, read_in_csv_file
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.kernel_ridge import KernelRidge

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
    
def gaussian_kernel(gamma, distances): # Based on code from the slides
    weights = np.exp(-gamma*(distances**2))
    return weights/np.sum(weights)


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
    
def evaluate_ridge_regression(x_train, y_train, x_test, y_test, C=1):
    model = Ridge(alpha=(1/(2*C)), max_iter=1000000)
    model.fit(x_train, y_train)
    evaluate_model("Ridge regression C=%f"%(C), model, x_test, y_test)
    disp_model_parameters(model)
    
def evaluate_kernel_ridge(x_train, y_train, x_test, y_test, C=1, gamma=5):  # Not used as there is too much data
    model = KernelRidge(alpha=(1.0/(2*C)), kernel='rbf', gamma=gamma)
    model.fit(x_train, y_train)
    evaluate_model("Ridge regression C=%f and gamma=%d"%(C, gamma), model, x_test, y_test)
    
def evaluate_knn_regression(x_train, y_train, x_test, y_test, number_of_neighbours=5):
    model = KNeighborsRegressor(n_neighbors=number_of_neighbours, weights='uniform')
    model.fit(x_train, y_train)
    evaluate_model("KNN regression k=%d"%(number_of_neighbours), model, x_test, y_test)

def evaluate_average_baseline(x_train, y_train, x_test, y_test):
    model = DummyRegressor(strategy="mean")
    model.fit(x_train, y_train)
    evaluate_model("Average Baseline", model, x_test, y_test)
    print("Average baseline is predicting a constant value of %f"%(model.constant_[0][0]))
    
def evaluate_constant_baseline(x_train, y_train, x_test, y_test, constant_value):
    model = DummyRegressor(constant=constant_value)
    model.fit(x_train, y_train)
    
    evaluate_model("Constant center value %f"%(constant_value), model, x_test, y_test)
    
def evaluate_baseline(x_train, y_train, x_test, y_test, constant_value):
    model = DummyRegressor(constant=constant_value)
    model.fit(x_train, y_train)
    
    evaluate_model("Constant center value %f"%(constant_value), model, x_test, y_test)
    
def evaluate_feature_baseline(x_test, y_test, parameters, feature):
    feature_index = parameters.index(feature)
    model = InputFeatureBaseline(feature_index)
    
    evaluate_model("Baseline with value of feature %s"%(feature), model, x_test, y_test)
    
def evaluate_model(label, model, x_test, y_test):
    ypred = model.predict(x_test)
    mean_sq_error = mean_squared_error(y_test, ypred)
    print("%s model %f"%(label, mean_sq_error))


def evaluate_all_models(x_train, y_train, x_test, y_test, parameter_list):
    print("Training models")
    evaluate_linear_regression(x_train, y_train, x_test, y_test)
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 1)
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 10)
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 100)
    evaluate_ridge_regression(x_train, y_train, x_test, y_test, 0.0001)
    evaluate_ridge_regression(x_train, y_train, x_test, y_test, 1)
    evaluate_knn_regression(x_train, y_train, x_test, y_test, 100)
    
    evaluate_average_baseline(x_train, y_train, x_test, y_test)
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.5)
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.75)
    if parameter_list is not None and 'film_avg_rating' in parameter_list:
        evaluate_feature_baseline(x_test, y_test, parameter_list, 'film_avg_rating')
    if parameter_list is not None and 'user_avg_rating' in parameter_list:
        evaluate_feature_baseline(x_test, y_test, parameter_list, 'user_avg_rating')

def evaluate_system(parameter_list):
    start = time.time()
    x, y= read_in_csv_files("training_points", parameter_list)
    end = time.time()
    time_to_read_in_data = end - start
    print("Time taken to read in the data %d"%(time_to_read_in_data))
    
    #x, y = read_in_csv_file("training_points/pairs_0.csv", parameter_list) # Can test with just one file
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)    # Use 20% for testing
    print("Training using %d training points and %d testing points"%(len(x_train), len(x_test)))
    evaluate_all_models(x_train, y_train, x_test, y_test, parameter_list)
    
    unseen_x_test, unseen_y_test = read_in_csv_files("testing_points", parameter_list) # Use completely new users and movies for testing
    print("\nTraining using %d training points and %d testing points made from unseen movies and users"%(len(x_train), len(unseen_x_test)))
    evaluate_all_models(x_train, y_train, unseen_x_test, unseen_y_test, parameter_list)
    
    end = time.time()
    time_to_run_program = end - start
    print("Time taken for the whole program in the data %d"%(time_to_run_program))

if __name__ == '__main__':
    parameter_list = ['film_avg_rating', 'user_avg_rating', 'film_total_likes', 'film_total_views', 'film_total_ratings', 'film_age', 'film_franchise', \
                  'film_rate_ratio', 'film_like_ratio', 'user_film_watched', 'director_avg', 'action_avg', 'adventure_avg', 'comedy_avg', 'crime_avg', \
                  'documentary_avg', 'drama_avg', 'family_avg', 'fantasy_avg', 'history_avg', 'horror_avg', 'music_avg', 'mystery_avg', 'romance_avg',\
                  'science fiction_avg', 'thriller_avg', 'tv movie_avg', 'war_avg', 'western_avg']
    evaluate_system(parameter_list)

