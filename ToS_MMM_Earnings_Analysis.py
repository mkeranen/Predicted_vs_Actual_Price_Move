#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 07:42:59 2018

@author: markkeranen

This script analyzes data gathered during the week of 01/29/2018, in which
many companies reported earnings. ThinkorSwim by TD Ameritrade has a 
'Market Maker Move (MMM)' calculation that aims to predict expected move. This
was recorded along with actual moves by each security post earnings reporting.
Additionally, IV and IV percentile was recorded pre and post earnings.

The chart displays the ratio of Actual move to Predicted (MMM) move with the 
IV percentile crush displayed in the background. The shaded green area between
positive and negative one is the area within which the ToS MMM encapsulates.
Any data point outside of the shaded area indicates a move outside of the
expected move.

"""

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.cm as cm
import numpy as np

style.use('ggplot')

#Read stock data into dataframe from .csv
df = pd.read_csv('ToS_MMM.csv')
df['Earnings Date'] = pd.to_datetime(df['Earnings Date'])

#Create colormap to color scatterplot points
colors = cm.rainbow(np.linspace(0, 1, len(df.index)))

#Setup figure for double y-axis
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title('Predicted (MMM) vs. Actual Move - Q1 2018', fontweight='bold', position=(0.5,1.05))

#Loop through df and plot scatter points and bars
for index, row in df.iterrows():
    x = index
    y = df.loc[index,'Actual:Expected Move Open']
    bar_y = df.loc[index, 'IV Crush Rank']
    ticker = df.loc[index,'Ticker']
    
    ax1.scatter(x,y,c=colors[index])
    ax1.annotate(ticker,(x,y), fontsize=6, fontweight='light')
    
    ax2.bar(x,bar_y, color='grey', alpha=.2)
    
    
#Format plot

#Remove ticks
ax1.tick_params(length=0)
ax2.tick_params(length=0)

#Set x limits
plt.xlim([-1,29])

#Format axis 1 - Actual : Predicted Move
ax1.get_xaxis().set_visible(False)
ax1.set_ylim(-3.5,3.5)
ax1.set_ylabel('Actual Move : Predicted Move')

#Shade in between upper and lower predicted move bounds
ax1.axhline(1, linewidth=0.5, color='g')
ax1.axhline(-1, linewidth=0.5, color='g')
ax1.fill_between(list(range(-10,50)), -1, 1, color='g', alpha=0.05)

#Visually separate different sectors
plt.axvline(4.5, linewidth=0.5, color='grey')
plt.axvline(9.5, linewidth=0.5, color='grey')
plt.axvline(13.5, linewidth=0.5, color='grey')
plt.axvline(16.5, linewidth=0.5, color='grey')
plt.axvline(21.5, linewidth=0.5, color='grey')

#Add labels to identify different sectors
ax1.annotate('Basic Materials', (-.3, -2), fontsize=6, fontweight='light', alpha=0.5)
ax1.annotate('Consumer Goods', (4.7, -2), fontsize=6, fontweight='light', alpha=0.5)
ax1.annotate('Financial', (10.3, -2), fontsize=6, fontweight='light', alpha=0.5)
ax1.annotate('Healthcare', (13.55, -2), fontsize=6, fontweight='light', alpha=0.5)
ax1.annotate('Services', (17.9, -2), fontsize=6, fontweight='light', alpha=0.5)
ax1.annotate('Technology', (23.8, -2), fontsize=6, fontweight='light', alpha=0.5)

#Format Axis 2 - IV Percentile Crush
ax2.grid(False)
ax2.set_ylim(-80,80)

#Hide axis labels above 0
for index, label in enumerate(ax2.yaxis.get_ticklabels()):
    if index > 4:
        label.set_visible(False)
ax2.set_ylabel('IV Percentile Crush')

#Add save figure and show
plt.tight_layout()
plt.savefig('Predicted (MMM) vs. Actual Move - Q1 2018.pdf')
plt.show()

