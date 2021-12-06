#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import math

# Remove empty lists from nested set of lists
def removeEmptyLists(myList):
    newList = []
    
    for index, lst in enumerate(myList):
        if len(lst)!=0: newList.append(myList[index])
            
    return newList


# Divide two lists element by element. If any NAN or INFINITY elements, replace with 0
def listDivision(list1, list2):
    new_list = np.ndarray.tolist((np.array(list1) / np.array(list2)))
    
    for arr in new_list:
        for i, value in enumerate(arr):
            if math.isnan(value) or math.isinf(value): arr[i] = 0
                
    return new_list


def largePlotterMultipleTicks(labels, x, y, yrange, legendLoc, xTick):
    
    # Figsize(x, y) in units of inches. dpi = 'dots per inch'
    figure(figsize = (10, 6), dpi = 80)  # Initialize the figure

    plt.tick_params(labelsize = 14)
    plt.rcParams["font.family"] = "Arial"

    # Axes and title label configurations
    plt.xlabel(labels[0], fontsize = 16, loc = 'right', labelpad = 12)  
    plt.ylabel(labels[1], fontsize = 16, loc = 'top', labelpad = 12)   
    plt.title(labels[2], fontsize = 20, loc = 'right', pad = 12) 
    
    #for index, plots in enumerate(y): 
    #    plt.scatter(x[index], y[index], label=labels[3][index])
    plt.scatter(x, y)#, label=labels[3])
    
    if xTick[0]:
        plt.xticks(xTick[1], xTick[2])  # Manually set the date labels

    plt.legend(loc = legendLoc, prop = {'size': 12})
    plt.ylim(ymax = yrange[1], ymin = yrange[0])
    
    plt.show()
    
    
def largePlotterMultiple(labels, x, y):
    
    # Figsize(x, y) in units of inches. dpi = 'dots per inch'
    figure(figsize = (10, 6), dpi = 80)  # Initialize the figure

    plt.tick_params(labelsize = 14)
    plt.rcParams["font.family"] = "Arial"

    # Axes and title label configurations
    plt.xlabel(labels[0], fontsize = 16, loc = 'right', labelpad = 12)  
    plt.ylabel(labels[1], fontsize = 16, loc = 'top', labelpad = 12)   
    plt.title(labels[2], fontsize = 20, loc = 'right', pad = 12) 
    
    for index, plots in enumerate(y): 
        plt.scatter(x[index], y[index], label=labels[3][index])

    plt.legend(loc = 2, prop = {'size': 12})
    
    plt.show()


def largePlotterSingle(labels, x, y, xTick):
    figure(figsize = (10, 6), dpi = 80)  # Initialize the figure
    
    plt.tick_params(labelsize = 14)
    plt.rcParams["font.family"] = "Arial"

    # Axes and title label configurations
    plt.xlabel(labels[0], fontsize = 16, loc = 'right', labelpad = 12)  
    plt.ylabel(labels[1], fontsize = 14, loc = 'top', labelpad = 10)   
    plt.title(labels[2], fontsize = 20, loc = 'right', pad = 12) 
    
    plt.scatter(x, y)
    
    if xTick[0]:
        plt.xticks(xTick[1], xTick[2])  # Manually set the date labels
    
    #plt.legend(loc = 2, prop = {'size': 12})
    
    plt.show()