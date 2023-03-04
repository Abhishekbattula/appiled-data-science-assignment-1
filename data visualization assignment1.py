"""
This module provides functions for data visualization using Pandas, Seaborn, and Matplotlib libraries.
It also uses Basemap toolkit for creating geographic maps and color maps from matplotlib.
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import cm

get_ipython().run_line_magic('matplotlib', 'inline')


# Reading the data file with pandas

"""
Read Uber data from a CSV file and return a pandas DataFrame containing the data.

Args:
    file_path (str): The path to the CSV file.

Returns:
    pandas.DataFrame: A DataFrame containing the Uber data.
"""
DATA_FILE = 'uber-raw-data-aug14.csv'  
uber_data = pd.read_csv(DATA_FILE)
uber_data.head()


# checking the datatypes of the variables
uber_data.info()

"""
Preprocess the Uber data by extracting additional features and converting data types.

Args:
    data (pandas.DataFrame): A DataFrame containing the raw Uber data.

Returns:
    pandas.DataFrame: A DataFrame containing the preprocessed Uber data with additional features.
"""

uber_data['Date/Time'] = pd.to_datetime(uber_data['Date/Time'], format="%m/%d/%Y %H:%M:%S")
uber_data['DayOfWeekNum'] = uber_data['Date/Time'].dt.dayofweek
uber_data['DayOfWeek'] = uber_data['Date/Time'].dt.day_name()
uber_data['MonthDayNum'] = uber_data['Date/Time'].dt.day
uber_data['HourOfDay'] = uber_data['Date/Time'].dt.hour

uber_data.head()


# Plotting the uber hourly pickups for each day of the week


def visualize_hourly_pickups_by_day(data):
    """
    Visualize the hourly Uber pickups by day of the week using a multiline plot.

    Args:
        data (pandas.DataFrame): A DataFrame containing the preprocessed Uber data.

    Returns:
        None
    """
    data['Date/Time'] = pd.to_datetime(data['Date/Time'], format='%m/%d/%Y %H:%M:%S')

    # Create a new column for the hour of the day
    data['Hour'] = data['Date/Time'].dt.hour

    # Group the data by hour and by day of the week, and count the number of pickups
    hourly_pickups = data.groupby(['Hour', data['Date/Time'].dt.dayofweek])['Date/Time'].count().unstack()

    # Plot a multiline plot
    hourly_pickups.plot(kind='line', figsize=(12, 8))

    # Add axis labels and title
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Pickups')
    plt.title('Hourly Uber Pickups by Day of the Week')


# Call the function
visualize_hourly_pickups_by_day(uber_data)
plt.show()


# Bar plot for journeys by hour

def plot_journeys_by_hour(data):
    """
    Visualize the total number of Uber journeys by hour of the day.

    Args:
        data (pandas.DataFrame): A DataFrame containing the preprocessed Uber data.

    Returns:
        plot with uber journeys per hour
    """
    # Journeys by hour
    uber_hour = data.pivot_table(index=['HourOfDay'],
                                  values='Base',
                                  aggfunc='count')
    uber_hour.plot(kind='bar', figsize=(8,6))
    plt.ylabel('Total Journeys')
    plt.title('Journeys by Hour')

plot_journeys_by_hour(uber_data)
plt.show()


# Overview of rides distribution in all of NYC

def plot_hexbin_map(dataframe, west, south, east, north):
    """
    Plots a hexbin map of latitude and longitude coordinates using the Basemap library.

    Args:
    - dataframe: A pandas DataFrame object containing the latitude and longitude coordinates.
    - west: The western boundary of the map.
    - south: The southern boundary of the map.
    - east: The eastern boundary of the map.
    - north: The northern boundary of the map.

    Returns:
    - None
    """

    fig = plt.figure(figsize=(14,10))
    ax = fig.add_subplot(111)
    m = Basemap(projection='merc', llcrnrlat=south, urcrnrlat=north,
                llcrnrlon=west, urcrnrlon=east, lat_ts=south, resolution='i')
    x, y = m(dataframe['Lon'].values, dataframe['Lat'].values)
    m.hexbin(x, y, gridsize=1000,
             bins='log', cmap=cm.YlOrRd_r)

    # Add labels to the graph
    ax.set_title('NYC uber pickups Hexbin Map')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

# Print the hexbin map
plot_hexbin_map(uber_data, -74.26, 40.50, -73.70, 40.92)  

