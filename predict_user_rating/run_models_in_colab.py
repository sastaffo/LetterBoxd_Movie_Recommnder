# adapted from Philip's predict_user_rating directory to run in colab by Sarah

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
import matplotlib.pyplot as plt

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
eval_results_path_generic = folder_path + "models/evaluate_all_DATE.txt"
train_csv_path = folder_path + "merged_csv_pairs/pairs_X.csv"
test_csv_path  = folder_path + "test_merged_csv_pairs/test_pairs_X.csv"

all_files_data = []
all_files_output = []

"""## methods

### read csvs
"""

def read_in_csv_files(parameter_list=None, train=True):
    print("Reading in the data")
    max = 24
    pth = train_csv_path
    if not train:
        max = 9
        pth = test_csv_path

    for i in range(max+1):
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

"""### plot"""

def plot_mean_with_deviation(title, x_axis_label, cross_validation_numbers, mean_errors, standard_deviations):
    legend_location = 4
    ax = plt.figure().add_subplot(111)
    ax.set_title(title, fontdict = {'fontsize' : 20})
    ax.set_xlabel(x_axis_label, fontdict = {'fontsize' : 20})
    ax.set_ylabel("Average mean square error", fontdict = {'fontsize' : 20})
    ax.errorbar(cross_validation_numbers, mean_errors, yerr=standard_deviations, label="Mean error and standard deviation against %s"%(x_axis_label))
    ax.legend(loc=legend_location, fontsize=14)

def display_graphs():
    plt.show()

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

"""### evaluate models"""

def disp_model_parameters(model):
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

def evaluate_kernel_ridge(x_train, y_train, x_test, y_test, C=1, gamma=5):
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
    s = ("Average baseline is predicting a constant value of %f\n\n\n"%(model.constant_[0][0]))
    append_f(this_eval_path, s)

def evaluate_constant_baseline(x_train, y_train, x_test, y_test, constant_value):
    model = DummyRegressor(constant=constant_value)
    model.fit(x_train, y_train)
    evaluate_model("Constant center value %f"%(constant_value), model, x_test, y_test)
    append_f(this_eval_path, "\n\n")

def evaluate_feature_baseline(x_test, y_test, parameters, feature):
    feature_index = parameters.index(feature)
    model = InputFeatureBaseline(feature_index)
    evaluate_model("Baseline with value of feature %s"%(feature), model, x_test, y_test)
    append_f(this_eval_path, "\n\n")

def evaluate_model(label, model, x_test, y_test):
    ypred = model.predict(x_test)
    mean_sq_error = mean_squared_error(y_test, ypred)
    s = label + "\n>> result: " + str(mean_sq_error)
    append_f(this_eval_path, (s+"\n"))


def evaluate_all_models(parameter_list):
    start = dt.now()
    x_train, y_train= read_in_csv_files(parameter_list, train=True)
    x_test, y_test = read_in_csv_files(parameter_list, train=False)
    print("Using %d training points and %d testing points"%(len(x_train), len(x_test)))
    end = dt.now()
    time_to_read_in_data = end - start
    print("Time taken to read in the data %d"%(time_to_read_in_data))

    print(dt.now(), "Training models")
    evaluate_linear_regression(x_train, y_train, x_test, y_test)
    print(dt.now(), "linreg")
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 1)
    print(dt.now(), "lasso 1")
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 10)
    print(dt.now(), "lasso 10")
    evaluate_lasso_regression(x_train, y_train, x_test, y_test, 100)
    print(dt.now(), "lasso 100")
    evaluate_ridge_regression(x_train, y_train, x_test, y_test, 0.01)
    print(dt.now(), "ridge 0.01")
    evaluate_ridge_regression(x_train, y_train, x_test, y_test, 1)
    print(dt.now(), "ridge 1")
    #evaluate_knn_regression(x_train, y_train, x_test, y_test, 100)

    evaluate_average_baseline(x_train, y_train, x_test, y_test)
    print(dt.now(), "avg base")
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.5)
    print(dt.now(), "const 2.5")
    evaluate_constant_baseline(x_train, y_train, x_test, y_test, 2.75)
    print(dt.now(), "const 2.75")
    if 'film_avg_rating' in parameter_list:
        evaluate_feature_baseline(x_test, y_test, parameter_list, 'film_avg_rating')
        print(dt.now(), "film's avg rating")
    if 'user_avg_rating' in parameter_list:
        evaluate_feature_baseline(x_test, y_test, parameter_list, 'user_avg_rating')
        print(dt.now(), "user's avg rating")

    end = dt.now()
    time_to_run_program = end - start
    print("Time taken for the whole program in the data %d"%(time_to_run_program))

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

## run all eval
"""

params = ["user_film_watched", "film_avg_rating", "film_like_ratio", "film_runtime_min", "film_franchise",
 "user_from_prod_country", "user_from_prod_continent", "director_avg", "director_count", "actor0_avg", "actor1_avg", "actor2_avg", "actor3_avg", "actor4_avg",
 "actor0_count", "actor1_count", "actor2_count", "actor3_count", "actor4_count", "action_avg", "adventure_avg", "animation_avg", "comedy_avg", "crime_avg",
 "documentary_avg", "drama_avg", "family_avg", "fantasy_avg", "history_avg", "horror_avg", "music_avg", "mystery_avg", "romance_avg", "science fiction_avg",
 "thriller_avg", "tv movie_avg", "war_avg", "western_avg", "action_count", "adventure_count", "animation_count", "comedy_count", "crime_count", "documentary_count",
 "drama_count", "family_count", "fantasy_count", "history_count", "horror_count", "music_count", "mystery_count", "romance_count", "science fiction_count",
 "thriller_count", "tv movie_count", "war_count", "western_count", "1880s", "1890s", "1900s", "1910s", "1920s", "1930s", "1940s", "1950s", "1960s", "1970s",
 "1980s", "1990s", "2000s", "2010s", "2020s", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "None", "Africa", "Asia", "Europe",
 "North America", "Oceania", "South America", "South America (Portuguese)"]

this_eval_path = eval_results_path_generic.replace("DATE", str(dt.now()))
print(this_eval_path, end=" ")
write_params(params, this_eval_path)
print("written params")
evaluate_all_models(params)

"""## cross validation"""

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

"""
if __name__ == '__main__':
    parameter_list = ['film_avg_rating', 'user_avg_rating', 'film_total_likes', 'film_total_views', 'film_total_ratings', 'film_age', 'film_franchise', \
                  'film_rate_ratio', 'film_like_ratio', 'user_film_watched', 'director_avg']
    #x, y = read_in_csv_file("data_points/pairs_0.csv", parameter_list) # Can test with just one file
    x, y = read_in_csv_files("training_points", parameter_list)
    cross_validate_penalty_parameter(x, y, "Lasso Regression", create_lasso_regression, [0.1, 1, 10, 100, 1000])
    cross_validate_penalty_parameter(x, y, "Ridge Regression", create_ridge_regression, [0.0001, 0.1, 1, 10])
    display_graphs()
    """
