'''
Created on 21 Dec 2020

@author: bradishp
'''
from math import log10
import matplotlib.pyplot as plt

legend_location = 1

def plot_mean_with_deviation(title, x_axis_label, cross_validation_numbers, mean_errors, standard_deviations):
    ax = plt.figure().add_subplot(111)
    ax.set_title(title, fontdict = {'fontsize' : 20})
    ax.set_xlabel(r'$log_{10}(%s)$'%(x_axis_label), fontdict = {'fontsize' : 20})
    ax.set_ylabel("Average mean square error", fontdict = {'fontsize' : 20})
    cross_validation_labels = [log10(x) for x in cross_validation_numbers]
    ax.errorbar(cross_validation_labels, mean_errors, yerr=standard_deviations, label="Mean error and standard deviation against %s"%(x_axis_label))
    ax.legend(loc=legend_location, fontsize=14)
    
def display_graphs():
    plt.show()
    