import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import pandas as pd
import numpy as np


def plot_rotations(boss, df):
    rotations =  df['Rotation 1'].unique().tolist()
    rot_data = []
    
    df1 = df.set_index('Rotation 1')
    for rot in rotations:
        try:
            rot_data.append([rot, round(df1.loc[rot].mean()['HPS'], 2), round(df1.loc[rot].std()['HPS'], 2), df1.loc[rot].count()['HPS']])

        except:
            pass
        
    rot_data = sorted(rot_data, key=lambda l:l[1], reverse=True)
    
    temp_rot, temp_mean, temp_err = [], [], []

    for i in range(len(rot_data)):
        if rot_data[i][3] <= 3: continue  # Skip rotations that don't have enough data.

        temp_rot.append(rot_data[i][0])
        temp_mean.append(rot_data[i][1])
        temp_err.append(rot_data[i][2] / np.sqrt(rot_data[i][3]))
        
    temp_y = list(np.arange(len(temp_mean) + 1, 1, -1))

    figure(figsize=(10, 10), dpi = 80)

    plt.errorbar(x = temp_mean, y = temp_y, yerr = None, xerr = temp_err, fmt='o')

    for i in range(len(temp_y)):
        plt.annotate(temp_rot[i], (temp_mean[i] + 0.1, temp_y[i] + 0.2))

    plt.yticks(color='None')

    plt.title(f'{boss}', fontsize = 20, loc = 'right', pad = 12)
    plt.xlabel('Avg HPS', fontsize = 16, loc = 'right', labelpad = 12) 
    plt.ylabel('Rotation', fontsize = 24, loc = 'top')

    plt.show()