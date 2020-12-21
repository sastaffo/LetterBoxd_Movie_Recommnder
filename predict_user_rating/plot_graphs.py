'''
Created on 21 Dec 2020

@author: bradishp
'''
import numpy as np
import matplotlib.pyplot as plt

legend_location = 4

def plot_mean_with_deviation(title, x_axis_label, cross_validation_numbers, mean_errors, standard_deviations):
    ax = plt.figure().add_subplot(111)
    ax.set_title(title, fontdict = {'fontsize' : 20})
    ax.set_xlabel(x_axis_label, fontdict = {'fontsize' : 20})
    ax.set_ylabel("Average mean square error", fontdict = {'fontsize' : 20})
    ax.errorbar(cross_validation_numbers, mean_errors, yerr=standard_deviations, label="Mean error and standard deviation against %s"%(x_axis_label))
    ax.legend(loc=legend_location, fontsize=14)
    
def display_graphs():
    plt.show()
    