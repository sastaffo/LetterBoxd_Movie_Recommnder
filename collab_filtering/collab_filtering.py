"""
@author: Shaun
"""

from lenskit import batch, util
from lenskit import crossfold as xf
from lenskit.algorithms import Recommender, item_knn as knn
from lenskit.metrics.predict import rmse
import json
import os
import pandas as pd

algo_ii = knn.ItemItem(20)

def eval(aname, algo, train, test, all_preds):
    """
    Predict the raitings using the model
    """
    fittable = util.clone(algo)
    fittable = Recommender.adapt(fittable)
    fittable.fit(train)
    # predict ratings
    preds = batch.predict(fittable, test)
    preds['Algorithm'] = aname
    all_preds.append(preds)

def main():
    """
    Perform item based collaborative filtering from the ratings data in 'ratings' variable
    """
    all_preds = []
    test_data = []
    for train, test in xf.partition_users(ratings[['user', 'item', 'rating']], 5, xf.SampleFrac(0.2)):
        test_data.append(test)
        eval('II', algo_ii, train, test, all_preds)
    preds = pd.concat(all_preds, ignore_index = True)
    preds_ii = preds[preds['Algorithm'].str.match('II')]
    print(preds_ii.head())
    test_data = pd.concat(test_data, ignore_index = True)
    print('RMSE II:', rmse(preds_ii['prediction'],preds_ii['rating']))


if __name__ == '__main__':

    filepath = "refined_film_data.json"
    user_lids = []
    film_lids = []
    users_ratings = []

    # Read user id's, film id's and user's ratings of films into different lists, from the refined file given
    with open(filepath) as fp:
        all_users_films = json.load(fp)
        for user_film_pair in all_users_films:
            user_lids.append(user_film_pair["user_lid"])
            film_lids.append(user_film_pair["film_lid"])
            users_ratings.append(user_film_pair["user_rating_for_film"])

    # add user ids, films ids and ratings to the pandas dataframe
    ratings = pd.DataFrame({'user' : user_lids,
                            'item' : film_lids,
                            'rating' : users_ratings})

    # Perform collaborative filtering on data in ratings
    main()
