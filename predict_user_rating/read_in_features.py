'''
Created on 20 Dec 2020

@author: bradishp
'''
import numpy as np
import pandas as pd
import os

def read_in_csv_files(dir_name, parameter_list=None):
    print("Reading in the data")
    directory = os.fsencode(dir_name)
    all_files_data = []
    all_files_output = []
    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        file_path = "%s/%s"%(dir_name, file_name)
        print("Reading in %s"%(file_path))
        
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
        parameter_list = columns # Get all columns
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

