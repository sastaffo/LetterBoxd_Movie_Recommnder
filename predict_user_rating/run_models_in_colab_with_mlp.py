# adapted from Philip's baselines_and_models.py file to run on colab
# MLP support added by Sarah

from google.colab import drive
drive.mount('/content/drive')

"""## importing"""

import json
import numpy as np
import pandas as pd
import os
from datetime import datetime as dt
import time
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
import math
import traceback

"""## basic read/write methods"""

def read_f(path):
    try:
        f = open(path, "r")
        s = f.read()
        f.close()
        return s
    except FileNotFoundError:
        print("file not found")
        return None
    except Exception as e:
        raise e
#end

def read_csv_1d(path):
    read = read_f(path)
    if read is not None:
        return read.split("\n")
    return None

def append_f(path, s):
    f = open(path, "a+")
    f.write(s)
    f.close()
    return
#end

def write_f(path, s):
    f = open(path, "w+")
    f.write(s)
    f.close()
    return
#end

def write_csv_1d(path, s_list):
    s = "\n".join(s_list)
    write_f(path, s)
    return
#end

def valid_json(path):
    j = read_f(path)
    try:
        json.loads(j)
        return True
    except:
        return False
#end

"""## global vars"""

folder_path = "/content/drive/MyDrive/4th_Year/ML Group Project/Sarah_data/"
eval_results_path_generic = folder_path + "models/evaluate_all_DATE_TEST.txt"
train_csv_path = folder_path + "merged_csv_pairs/pairs_X.csv"
test_csv_path  = folder_path + "test_merged_csv_pairs/test_pairs_X.csv"
this_eval_path = ""

all_files_data = []
all_files_output = []

"""## methods

### read csvs
"""

def read_in_csv_files(parameter_list=None, train=True, get_train_files=25, get_test_files=10):
    print("Reading in the data")
    max = get_train_files
    pth = train_csv_path
    if not train:
        max = get_test_files
        pth = test_csv_path

    for i in range(max):
        file_path = pth.replace("X", str(i))
        print("Reading in %s"%(file_path.split("/")[-1]))
        x_new, y_new = read_in_csv_file(file_path, parameter_list)

        all_files_data.append(x_new)
        all_files_output.append(y_new)

    x = np.concatenate(all_files_data)
    y = np.concatenate(all_files_output)
    return x, y

def read_in_csv_file(file_name, parameter_list=None):
    df = pd.read_csv(file_name, comment='#', index_col=False)
    columns = df.columns.tolist()
    columns = [col.strip() for col in columns]
    if parameter_list == None:
        parameter_list = columns[1:] # Get all columns
    x = np.zeros(shape=(len(df.index), len(parameter_list)))
    col_count = 0
    for parameter_name in parameter_list:
        feature_index = columns.index(parameter_name)
        col = np.array(df.iloc[:,feature_index])
        for i in range(len(col)):
            if col[i] != None and col[i] != 'None':
                x[i, col_count] = col[i]
            # else just leave it as zero
        col_count += 1

    y = np.array(df.iloc[:,0])
    return x, y

"""### input feature baseline class"""

class InputFeatureBaseline(object):

    def __init__(self, feature_index):
        self.feature_index = feature_index

    def predict(self, x):
        number_of_points = len(x)
        y_preds = np.zeros(number_of_points)
        for i in range(number_of_points):
            y_preds[i] = x[i][self.feature_index]
        return y_preds

"""### evaluate models

#### write params and predictions
"""

def disp_model_parameters(model, this_eval_path):
    s = ("Theta0: %0.6f"%(model.intercept_) + ", ")
    param_num = 1
    parameters = model.coef_
    if isinstance(parameters[0],(list, np.ndarray)):    # Some models have their parameters in a list within the list
        parameters = parameters[0]

    for param in parameters:
        s = s + ("Theta%d: %0.6f"%(param_num, param) + ", ")
        param_num += 1
    s = s + ("\n\n\n")
    append_f(this_eval_path, s)

def evaluate_model(label, model, x_test, y_test, this_eval_path):
    ypred = model.predict(x_test)
    mean_sq_error = mean_squared_error(y_test, ypred)
    root_mse = math.sqrt(mean_sq_error)
    s = label + "\n>> mean_sq_error: " + str(mean_sq_error) + "\n>> root_mean_sq_error: " + str(root_mse)
    append_f(this_eval_path, (s+"\n"))

"""#### the models"""

def gaussian_kernel(gamma, distances): # Based on code from the slides
    weights = np.exp(-gamma*(distances**2))
    return weights/np.sum(weights)

def evaluate_linear_regression(x_train, y_train, x_test, y_test, this_eval_path):
    model = LinearRegression()
    model.fit(x_train, y_train)
    evaluate_model("Linear regression", model, x_test, y_test, this_eval_path)
    disp_model_parameters(model, this_eval_path)

def evaluate_mlp_regressor(x_train, y_train, x_test, y_test, this_eval_path, layers=3, layer_size=500, L2_alpha=0.0001, iterations=500, verbose=True, learning_rate="constant"):
    label = ("MLP Regressor Neural Net: layers:" + str(layers) + " layer size:" + str(layer_size) + " alpha(L2 penalty):" + str(L2_alpha)
                + " iterations:" + str(iterations) + "learning rate:\"" + learning_rate + "\"")
    model = MLPRegressor(hidden_layer_sizes=(layers,layer_size), verbose=verbose, alpha=L2_alpha, max_iter=iterations, early_stopping=True, learning_rate=learning_rate)
    model.fit(x_train, y_train)
    evaluate_model(label, model, x_test, y_test, this_eval_path)
    append_f(this_eval_path, "\n\n")

def evaluate_lasso_regression(x_train, y_train, x_test, y_test, this_eval_path, C=1):
    model = Lasso(alpha=(1/(2*C)), max_iter=1000000)
    model.fit(x_train, y_train)
    evaluate_model("Lasso regression C=%d"%(C), model, x_test, y_test, this_eval_path)
    disp_model_parameters(model, this_eval_path)

def evaluate_ridge_regression(x_train, y_train, x_test, y_test, this_eval_path, C=1):
    model = Ridge(alpha=(1/(2*C)), max_iter=1000000)
    model.fit(x_train, y_train)
    evaluate_model("Ridge regression C=%f"%(C), model, x_test, y_test, this_eval_path)
    disp_model_parameters(model, this_eval_path)

def evaluate_kernel_ridge(x_train, y_train, x_test, y_test, this_eval_path, C=1, gamma=5):
    model = KernelRidge(alpha=(1.0/(2*C)), kernel='rbf', gamma=gamma)
    model.fit(x_train, y_train)
    evaluate_model("Ridge regression C=%f and gamma=%d"%(C, gamma), model, x_test, y_test, this_eval_path)
    append_f(this_eval_path, "\n\n")

def evaluate_knn_regression(x_train, y_train, x_test, y_test, this_eval_path, number_of_neighbours=5):
    model = KNeighborsRegressor(n_neighbors=number_of_neighbours, weights='uniform')
    model.fit(x_train, y_train)
    evaluate_model("KNN regression k=%d"%(number_of_neighbours), model, x_test, y_test, this_eval_path)
    append_f(this_eval_path, "\n\n")

def evaluate_average_baseline(x_train, y_train, x_test, y_test, this_eval_path):
    model = DummyRegressor(strategy="mean")
    model.fit(x_train, y_train)
    evaluate_model("Average Baseline", model, x_test, y_test, this_eval_path)
    s = ("Average baseline is predicting a constant value of %f\n\n"%(model.constant_[0][0]))
    append_f(this_eval_path, s)

def evaluate_constant_baseline(x_train, y_train, x_test, y_test, constant_value, this_eval_path):
    model = DummyRegressor(constant=constant_value)
    model.fit(x_train, y_train)
    evaluate_model("Constant center value %f"%(constant_value), model, x_test, y_test, this_eval_path)
    append_f(this_eval_path, "\n\n")

def evaluate_feature_baseline(x_test, y_test, parameters, feature, this_eval_path):
    feature_index = parameters.index(feature)
    model = InputFeatureBaseline(feature_index)
    evaluate_model("Baseline with value of feature %s"%(feature), model, x_test, y_test, this_eval_path)
    append_f(this_eval_path, "\n\n")

"""#### evaluate all"""

def evaluate_all_models(x_train, y_train, x_test, y_test, parameter_list, this_eval_path):
    start = dt.now()
    evaluate_linear_regression(x_train, y_train, x_test, y_test, this_eval_path)
    print(dt.now(), "linreg\n")

    evaluate_lasso_regression(x_train, y_train, x_test, y_test, this_eval_path, 1)
    print(dt.now(), "lasso 1\n")
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, this_eval_path, 10)
    print(dt.now(), "lasso 10\n")
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, this_eval_path, 100)
    print(dt.now(), "lasso 100\n")
    evaluate_ridge_regression(x_train, y_train, x_test, y_test, this_eval_path, 0.01)
    print(dt.now(), "ridge 0.01\n")
    evaluate_ridge_regression(x_train, y_train, x_test, y_test, this_eval_path, 1)
    print(dt.now(), "ridge 1\n")
    evaluate_knn_regression(x_train, y_train, x_test, y_test, this_eval_path, 100)
    print(dt.now(), "kNN k=100\n")

    evaluate_average_baseline(x_train, y_train, x_test, y_test, this_eval_path)
    print(dt.now(), "avg base\n")
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, this_eval_path, 2.5)
    print(dt.now(), "const 2.5\n")
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, this_eval_path, 2.75)
    print(dt.now(), "const 2.75\n")
    if 'film_avg_rating' in parameter_list:
        evaluate_feature_baseline(x_test, y_test, parameter_list, 'film_avg_rating', this_eval_path)
        print(dt.now(), "film's avg rating\n")
    if 'user_avg_rating' in parameter_list:
        evaluate_feature_baseline(x_test, y_test, parameter_list, 'user_avg_rating', this_eval_path)
        print(dt.now(), "user's avg rating\n")

    print("Time taken for this evaluation", (dt.now()-start), "\n\n")

"""#### evaluate MLP"""

def evaluate_mlp_models(x_train, y_train, x_test, y_test, parameter_list):
    start = dt.now()
    evaluate_linear_regression(x_train, y_train, x_test, y_test)
    print(dt.now(), "linreg\n")

    layers = [3,4,5]
    layer_sizes = [100,150,200,300,750]
    alphas = [0.1, 0.05, 0.01, 0.005, 0.001, 0.0001]
    learning_rates = ['constant', 'adaptive', 'invscaling']
    max_iters = 1000
    loop_num = 1
    for l in layers:
        for ls in layer_sizes:
            for a in alphas:
                for lnr in learning_rates:
                    model_start = dt.now()
                    print(model_start, "start mlp", loop_num)
                    loop_num = loop_num + 1
                    evaluate_mlp_regressor(x_train, y_train, x_test, y_test, this_eval_path, layers=l, layer_size=ls,
                                           L2_alpha=a, iterations=max_iters, verbose=False, learning_rate=lnr)
                    print((dt.now() - model_start), "end\n")

    evaluate_average_baseline(x_train, y_train, x_test, y_test, this_eval_path)
    print(dt.now(), "avg base\n")
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.5, this_eval_path)
    print(dt.now(), "const 2.5\n")
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.75, this_eval_path)
    print(dt.now(), "const 2.75\n")
    if 'film_avg_rating' in parameter_list:
        evaluate_feature_baseline(x_test, y_test, parameter_list, 'film_avg_rating', this_eval_path)
        print(dt.now(), "film's avg rating\n")
    if 'user_avg_rating' in parameter_list:
        evaluate_feature_baseline(x_test, y_test, parameter_list, 'user_avg_rating', this_eval_path)
        print(dt.now(), "user's avg rating\n")

    print("Time taken for this evaluation", (dt.now()-start), "\n\n")

"""### write params"""

def write_params(params_list, dst_path):
    s = "parameters = ["
    first = True
    for i in range(len(params_list)):
        if first: first = False
        else: s = s + ",   "
        s = s + str(i+1) + ":\"" + params_list[i] + "\""
    s = s + "]\n\n"
    write_f(dst_path, s)

"""# model running

## system
"""

parameter_list = ['film_avg_rating', 'user_avg_rating', 'film_total_likes', 'film_total_views', 'film_total_ratings', 'film_age', 'film_franchise',
    'film_rate_ratio', 'film_like_ratio', 'user_film_watched', 'director_avg', 'action_avg', 'adventure_avg', 'comedy_avg', 'crime_avg',
    'documentary_avg', 'drama_avg', 'family_avg', 'fantasy_avg', 'history_avg', 'horror_avg', 'music_avg', 'mystery_avg', 'romance_avg',
    'science fiction_avg', 'thriller_avg', 'tv movie_avg', 'war_avg', 'western_avg']

def evaluate_system(parameter_list):
    start = dt.now()
    print(start, "starting evaluate all")
    (x, y) = read_in_csv_files(parameter_list, train=True)
    print("Read in %d points"%(len(x)))
    end = dt.now()
    time_to_read_in_data = end - start
    print("Time taken to read in the data", time_to_read_in_data)

    this_eval_path = eval_results_path_generic.replace("DATE", str(dt.now())).replace("TEST", "MLP_80_20")
    print(this_eval_path)
    write_params(parameter_list, this_eval_path)
    print("written params")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)    # Use 20% for testing
    print("Training using %d training points and %d testing points"%(len(x_train), len(x_test)))
    print(dt.now(), "Training models, 80/20")
    evaluate_all_models(x_train, y_train, x_test, y_test, parameter_list, this_eval_path)
    print("\n\ndone - time taken", (dt.now()-start))

    this_eval_path = eval_results_path_generic.replace("DATE", str(dt.now())).replace("TEST", "MLP_unseen")
    print(this_eval_path)
    write_params(parameter_list, this_eval_path)
    print("written params")
    unseen_x_test, unseen_y_test = read_in_csv_files(parameter_list, train=False) # Use completely new users and movies for testing
    print("\nTraining using %d training points and %d testing points made from unseen movies and users"%(len(x_train), len(unseen_x_test)))
    print(dt.now(), "Training models, unseen")
    evaluate_all_models(x_train, y_train, unseen_x_test, unseen_y_test, parameter_list, this_eval_path)

    print("Time taken both evaluations", (dt.now()-start))

"""### run MLP on some data"""

parameter_list = ['film_avg_rating', 'user_avg_rating', 'film_total_likes', 'film_total_views', 'film_total_ratings', 'film_age', 'film_franchise',
    'film_rate_ratio', 'film_like_ratio', 'user_film_watched', 'director_avg', 'action_avg', 'adventure_avg', 'comedy_avg', 'crime_avg',
    'documentary_avg', 'drama_avg', 'family_avg', 'fantasy_avg', 'history_avg', 'horror_avg', 'music_avg', 'mystery_avg', 'romance_avg',
    'science fiction_avg', 'thriller_avg', 'tv movie_avg', 'war_avg', 'western_avg']

def evaluate_mlp_data_subset(parameter_list):
    start = dt.now()
    print(start, "starting evaluate all")
    (x, y) = read_in_csv_file(train_csv_path.replace("X", "0"), parameter_list=parameter_list)
    print("Read in %d points"%(len(x)))
    print("Time taken to read in the data", (dt.now()-start))

    this_eval_path = eval_results_path_generic.replace("DATE", str(dt.now())).replace("TEST", "MLP_80_20")
    print(this_eval_path)
    write_params(parameter_list, this_eval_path)
    print("written params")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)    # Use 20% for testing
    print("Training using %d training points and %d testing points"%(len(x_train), len(x_test)))
    print(dt.now(), "Training models, 80/20")
    evaluate_all_models(x_train, y_train, x_test, y_test, parameter_list, this_eval_path)
    print("\n\ndone - total time taken", (dt.now()-start))

    this_eval_path = eval_results_path_generic.replace("DATE", str(dt.now())).replace("TEST", "test_MLP_unseen")
    print(this_eval_path)
    write_params(parameter_list, this_eval_path)
    print("written params")
    unseen_x_test, unseen_y_test = read_in_csv_file(test_csv_path.replace("X", "0"), parameter_list=parameter_list) # Use completely new users and movies for testing
    s = "\nTraining using %d training points and %d testing points made from unseen movies and users\n\n"%(len(x), len(unseen_x_test))
    append_f(this_eval_path, (s))
    print(s)
    print(dt.now(), "Training models, unseen")
    evaluate_all_models(x, y, unseen_x_test, unseen_y_test, parameter_list, this_eval_path)
    print("\n\ndone - total time taken", (dt.now()-start))
