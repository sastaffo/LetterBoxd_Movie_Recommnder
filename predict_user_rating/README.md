# LetterBoxd Movie Recommnder
Code for estimating user's ratings of films.

* baselines_and_models.py - Uses a specified set of features and runs through a bunch of models and baselines to get their mean square errors. It will use 20% of the training data as testing. It will then perform a second run of on the model using the same training data but instead using data collected specifically for testing. This data won't have any of the previous users or films so it will be entirely unseen.
* cross_validate_models.py - Uses a specified set of features and performs cross validation on the Lasso and Ridge models to get their optimal C values. Can also be run on a KNN regressor to get the optimal number of nearest neighbours but this is very time consuming.
* input_feature_baseline.py - A baseline that uses a specified input feature's value as the predicted output value. Used as an intelligent baseline.
* plot_graphs.py - Code for plotting cross validation graphs.
* run_models_in_colab - Code for running the models specifically in Google Collab.
