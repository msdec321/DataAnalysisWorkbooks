import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import pandas as pd
import numpy as np


def apply_filters(df, rotating_on_tank, spriest, innervate, bloodlust, natures_grace, power_infusion, nHealers):
    n_filters = 0
    filters = ""
    
    if rotating_on_tank in ['Yes', 'No']:
        df = df.loc[df['Rotating on tank?'] == rotating_on_tank]
        n_filters += 1
        filters += f"_tankrotating{rotating_on_tank}"

    if nHealers in [4, 5, 6]:
        df = df.loc[df['nHealers'] == nHealers]
        filters += f"_{nHealers}healers"

    if spriest in ['Yes', 'No']:
        df = df.loc[df['Spriest?'] == spriest]
        n_filters += 1
        filters += f"_spriest{spriest}"

    if innervate in ['Yes', 'No']:
        df = df.loc[df['Innervate?'] == innervate]
        n_filters += 1
        filters += f"_innervate{innervate}"
        
    if bloodlust in ['Yes', 'No']:
        df = df.loc[df['Bloodlust?'] == bloodlust]
        n_filters += 1
        filters += f"_bloodlust{bloodlust}"
        
    if natures_grace in ['Yes', 'No']:
        df = df.loc[df["Nature's Grace?"] == natures_grace]
        n_filters += 1
        filters += f"_naturesgrace{natures_grace}"
        
    if power_infusion in ['Yes', 'No']:
        df = df.loc[df["Power Infusion?"] == power_infusion]
        n_filters += 1
        filters += f"_powerinfusion{_powerinfusion}"
        
    return df, n_filters, filters


def plot_rotations(boss, df, n_filters, filters, save):
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
        if i == 20: break # Limit the number of rotations plotted to the top 20

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
    
    if save:
        boss = boss.replace(" ", "")
        boss = boss.replace("'", "")
        
        if n_filters == 0:
            plt.savefig(f'plots/{boss.lower()}_N{df.shape[0]}_nofilters.png', dpi = 100)
            
        else:
            plt.savefig(f'plots/{boss.lower()}_N{df.shape[0]}{filters}.png', dpi = 100)
            
    if df.shape[0] < 100: print(f"WARNING! Low statistics! N = {df.shape[0]}. Consider using a looser set of filters.")

    plt.show()
    