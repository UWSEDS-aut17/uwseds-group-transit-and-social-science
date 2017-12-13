import os
import geopandas as gpd
import pysal as ps
import pandas as pd
import numpy as np
import math

def js_code (N_plots):
    part1 = ''.join(['\n l'+str(i)+'.visible = '+'false;' for i in N_plots])
    part2 = ''.join(['\n if (cb_obj.active[i] == '+str(i)+')'+'{l'+str(i)+'.visible = '+'true;' +  '} else ' for i in N_plots])
    if part2.endswith('else '):
        part2 = part2[:-5]
    checkbox_code = '//console.log(cb_obj.active); '+ part1 + """for (i in cb_obj.active) {//console.log(cb_obj.active[i]);""" + part2 + """}"""
    return (checkbox_code)

def income_classifier(grid):

    #Defining thresholds for income
    breaks = [x for x in range(55000, 110000, 5000)]

    #Initialize the classifier and apply it
    classifier = ps.User_Defined.make(bins=breaks)
    pt_classif = grid[['income']].apply(classifier)
    # Rename the classified column
    pt_classif.columns = ['incomeb']
    # Join it back to the grid layer
    grid = grid.join(pt_classif)
    # Adding new column with bin names to be used in legend
    grid['bin']= pd.np.where(grid.incomeb.astype(str) == '1', "[55000-60000]",
                         pd.np.where(grid.incomeb.astype(str) == '2',
                         "[60000-65000]",pd.np.where(grid.incomeb.astype(str) == '3',
                         "[65000-70000]",pd.np.where(grid.incomeb.astype(str) == '4',
                         "[70000-75000]",pd.np.where(grid.incomeb.astype(str) == '5',
                         "[75000-80000]",pd.np.where(grid.incomeb.astype(str) == '6',
                         "[80000-85000]",pd.np.where(grid.incomeb.astype(str) == '7',
                         "[85000-90000]",pd.np.where(grid.incomeb.astype(str) == '8',
                         "[90000-95000]",pd.np.where(grid.incomeb.astype(str) == '9',
                         "[95000-100000]",pd.np.where(grid.incomeb.astype(str) == '10',
                         "[100000-105000]",pd.np.where(grid.incomeb.astype(str) == '11',
                         "[105000-110000]",'NA')
                        ))))))))))
    return(grid)
