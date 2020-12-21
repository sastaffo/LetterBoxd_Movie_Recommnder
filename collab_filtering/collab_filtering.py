from lenskit.datasets import ML100K
from lenskit import batch, topn, util
from lenskit import crossfold as xf
from lenskit.algorithms import Recommender, als, item_knn as knn
from lenskit.metrics.predict import rmse
import json
import os
import pandas as pd

algo_ii = knn.ItemItem(20)

def eval(aname, algo, train, test, all_preds):
    fittable = util.clone(algo)
    fittable = Recommender.adapt(fittable)
    fittable.fit(train)
    # predict ratings
    preds = batch.predict(fittable, test)
    preds['Algorithm'] = aname
    all_preds.append(preds)

def main():
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

    # get all files in directory
    dir = "../user_film_merge/"
    user_film_files = os.listdir(dir)

    # get data from all files into one big list
    all_data = []
    for filename in user_film_files:
        filepath = dir + filename
        with open(filepath) as fp:
            files_data = json.load(fp)
            all_data.extend(files_data)

    # get all the users, films and ratings for the films by the users from the list
    user_lids = []
    film_lids = []
    users_ratings = []
    for user_film_pair in all_data:
        user_lids.append(user_film_pair["user_lid"])
        film_lids.append(user_film_pair["film_lid"])
        users_ratings.append(user_film_pair["user_rating_for_film"])

    # add user ids, films ids and ratings to the pandas dataframe
    ratings = pd.DataFrame({'user' : user_lids,
                            'item' : film_lids,
                            'rating' : users_ratings})
    print(ratings.head())

    # collaborative filtering
    # main()
