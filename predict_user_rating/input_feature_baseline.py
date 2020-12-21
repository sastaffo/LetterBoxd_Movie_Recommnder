'''
Created on 19 Dec 2020

@author: bradishp
'''
import numpy as np

class InputFeatureBaseline(object):

    def __init__(self, feature_index):
        self.feature_index = feature_index
     
    def predict(self, x):
        number_of_points = len(x)
        y_preds = np.zeros(number_of_points)
        for i in range(number_of_points):
            y_preds[i] = x[i][self.feature_index]
        return y_preds
    
