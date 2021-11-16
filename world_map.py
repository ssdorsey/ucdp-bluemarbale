# %matplotlib widget
# import IPython
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from matplotlib.lines import Line2D
import cartopy.crs as ccrs # projection: Plate Carree - WGS84
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
from joblib import Parallel, delayed
import multiprocessing
# ------------------------------------------------------------------------------
# import data
# ------------------------------------------------------------------------------
df = pd.read_csv('Data/ucdp_ged.csv', low_memory=False)
df['date'] = pd.to_datetime(df['date_start'])
df['date_start'] = pd.to_datetime(df['date_start'])
df['date_end'] = pd.to_datetime(df['date_end'])
df['date_end_new'] = pd.to_datetime(df['date_end_new'])

# set minimum 10-day duration for events
# df.loc[:,'date_end_new'] = df['date_end']
# for row_num in tqdm(range(0, df.shape[0])):
#     if (df.loc[row_num, 'date_end'] - df.loc[row_num, 'date_start']).days < 10:
#         df.loc[row_num, 'date_end_new'] = df.loc[row_num, 'date_start'] + timedelta(days=10)
# df.to_csv('Data/ucdp_ged.csv', index=False)

# Type of UCDP conflict:
# 1 : state-based conflict
# 2 : non-state conflict
# 3 : one-sided violence

# background maps
os.environ["CARTOPY_USER_BACKGROUNDS"] = "Data/Maps/"

# first_day = df[df['date'] == df['date'].min()]

colors = {1: (1.0, .325, .325),  # '#FF5353',
          2: (1.0, .6, .2), # '#FF9933',
          3: (.992, .992, .588)} # '#FDFD96'}

legend_elements = [ Line2D([0], [0], marker='o', color='w', label='State-Based Conflict',
                          markerfacecolor=colors[1], markersize=15),
                Line2D([0], [0], marker='o', color='w', label='Non-State Conflict',
                          markerfacecolor=colors[2], markersize=15),
                Line2D([0], [0], marker='o', color='w', label='One-Sided Violence',
                          markerfacecolor=colors[3], markersize=15)]

# naming convention
total_days = (df['date_end'].max() - df['date_start'].min()).days
all_dates = [df['date_start'].min() + timedelta(days=ii) for ii in range(0, total_days+30)] # TODO: check trailing date
position = range(0, len(all_dates))
file_num = dict(zip(all_dates, position))

figsize = (18, 9)

# ------------------------------------------------------------------------------
# function to make event blips for each day
# ------------------------------------------------------------------------------

def make_colors(frame):
    """
    Args:
        dataframe with events

    Returns:
        list of tuples
    """
    rgba = []

    for row_num in frame.index:
        rgb = colors[frame.loc[row_num, 'type_of_violence']]
        alpha = (1 - (frame.loc[row_num, 'duration_passed'].round(decimals=2)))
        # put values into rgba
        rgba.append(rgb + (alpha,))

    return rgba


def single_day(ax, date):
    """
    graphs all the events for a single day

    Args:
        ax: the matplotlib ax
        date_graph: the date of the events to map
        date_current: age of event (for alpha + expand)

    Returns:
        ax with points graphed out
    """
    # restrict the data
    sub_frame = df[(df['date_start'] <= date) & (df['date_end_new'] >= date)]
    sub_frame = sub_frame.reset_index()

    # get % of duration
    time_passed = pd.Series([ii.days for ii in date - sub_frame['date_start']])
    time_passed[time_passed < 1] = 1
    total_duration = pd.Series([ii.days for ii in sub_frame['date_end_new'] -
                                sub_frame['date_start']])
    sub_frame.loc[:, 'duration_passed'] = time_passed / total_duration

    # set size
    sub_frame.loc[:, 'size'] = (sub_frame['best'] * sub_frame['duration_passed']) * 7

    # set color + alpha
    sub_colors = make_colors(sub_frame)

    # plot the events
    if sub_frame.shape[0] > 0:
        scatter = ax.scatter(x=sub_frame['longitude'],
                   y=sub_frame['latitude'],
                   color=sub_colors,
                   s=sub_frame['size'], # TODO: map to timedelta
                   transform=ccrs.PlateCarree())
        
        legend = ax.legend(handles=legend_elements,
                            loc="lower left")
        ax.add_artist(legend)


def multiple_days(date, res="high"): # TODO: change to high res for final
    """
    graphs the day + t-30 days with explosions + fade

    Args:
        date: date to graph

    Returns:
    """
    # set up the plot
    fig = plt.figure(figsize=figsize, dpi=150)
    ax = plt.axes(projection=ccrs.Mercator(central_longitude=0,
                                           min_latitude=-65,
                                           max_latitude=70))
    ax.background_img(name=date.month_name(), resolution=res)
    ax.set_extent([-170, 179, -65, 70], crs=ccrs.PlateCarree())
    single_day(ax=ax, date=date)
    plt.title(f'{date.day} {date.month_name()} {date.year}', loc='left', fontsize=20)
    fig.savefig(f'Results/Map_Frames/frame_{file_num[date]}.png',
                figsize=figsize,
                dpi=150, # TODO:
                bbox_inches='tight',
                pad_inches=0)
    plt.clf()

multiple_days(all_dates[1000], "high")
# ------------------------------------------------------------------------------
# draw them all
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # num_cores = multiprocessing.cpu_count()
    num_cores = 6

    print('starting parallel')

    # check for work already done
    if len(os.listdir('Results/Map_Frames/')) > 0:
        latest = max([int(ii.split('_')[1].split('.png')[0]) for ii in os.listdir('Results/Map_Frames/')])
    else:
        latest = 0

    Parallel(n_jobs=num_cores)(delayed(multiple_days)(ii) for ii in tqdm(all_dates[latest:]))
