#    Python script to process King County GTFS data 
import pandas as pd
import os
import zipfile

#    Downloading data and making pandas dataframes 
#    from GTFS CSV TXT files
make_dataframes():
    trips_df = pd.csv_read('1_gtfs/trips.txt')
    shapes_df = pd.csv_read('1_gtfs/shapes.txt')
    routes_df = pd.csv_read('1_gtfs/routes.txt')
    stop_times_df = pd.csv_read('1_gtfs/stop_times.txt')

#    Functions that process the dataframes    
get_stop_locations(route_id_num):
'''This function uses a route id to find the latitude and 
longitude of the route's bus stops. The output is a pandas
dataframe with columns of latitude and longitude. 
'''
    loc = trips_df.index[trips_df['route_id'] == route_id_num].values
    shape_id_num = trips_df.get_value(loc[0], 'shape_id')
    shape_info = shapes_df.query('shape_id ==' + str(shape_id_num))
    route_lat_lon = shape_info.groupby('shape_id')['shape_pt_lat',
        'shape_pt_lon']


