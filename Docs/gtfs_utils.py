#    Python script to process King County GTFS data
import pandas as pd
import os
import zipfile
import csv
from pylab import *

#    Downloading data and making pandas dataframes
#    from GTFS CSV TXT files
def make_dataframes():
    trips_df = pd.csv_read('1_gtfs/trips.txt')
    shapes_df = pd.csv_read('1_gtfs/shapes.txt')
    routes_df = pd.csv_read('1_gtfs/routes.txt')
    stop_times_df = pd.csv_read('1_gtfs/stop_times.txt')

#    Functions that process the dataframes
def get_stop_locations(route_id_num):
'''This function uses a route id to find the latitude and
longitude of the route's bus stops. The output is a pandas
dataframe with columns of latitude and longitude.
'''
    loc = trips_df.index[trips_df['route_id'] == route_id_num].values
    shape_id_num = trips_df.get_value(loc[0], 'shape_id')
    shape_info = shapes_df.query('shape_id ==' + str(shape_id_num))
    route_lat_lon = shape_info.groupby('shape_id')['shape_pt_lat',
        'shape_pt_lon']

def read_ascii_boundary(filestem):
    '''
    Reads polygon data from an ASCII boundary file.
    Returns a dictionary with polygon IDs for keys. The value for each
    key is another dictionary with three keys:
    'name' - the name of the polygon
    'polygon' - list of (longitude, latitude) pairs defining the main
    polygon boundary
    'exclusions' - list of lists of (lon, lat) pairs for any exclusions in
    the main polygon
    '''
    metadata_file = filestem + 'a.dat'
    data_file = filestem + '.dat'
    # Read metadata
    lines = [line.strip().strip('"') for line in open(metadata_file)]
    polygon_ids = lines[::6]
    polygon_names = lines[2::6]
    polygon_data = {}
    for polygon_id, polygon_name in zip(polygon_ids, polygon_names):
        # Initialize entry with name of polygon.
        # In this case the polygon_name will be the 5-digit ZIP code.
        polygon_data[polygon_id] = {'name': polygon_name}
    del polygon_data['0']
    # Read lon and lat.
    f = open(data_file)
    for line in f:
        fields = line.split()
        if len(fields) == 3:
            # Initialize new polygon
            polygon_id = fields[0]
            polygon_data[polygon_id]['polygon'] = []
            polygon_data[polygon_id]['exclusions'] = []
        elif len(fields) == 1:
            # -99999 denotes the start of a new sub-polygon
            if fields[0] == '-99999':
                polygon_data[polygon_id]['exclusions'].append([])
        else:
            # Add lon/lat pair to main polygon or exclusion
            lon = float(fields[0])
            lat = float(fields[1])
            if polygon_data[polygon_id]['exclusions']:
                polygon_data[polygon_id]['exclusions'][-1].append((lon, lat))
            else:
                polygon_data[polygon_id]['polygon'].append((lon, lat))
    return polygon_data

# Read in ZIP code boundaries for Seattle
d = read_ascii_boundary('')

# Create figure and axes
figure(figsize=(5, 5), dpi=30)
map_axis = axes([0.0, 0.0, 0.8, 0.9])

# Create the map axis
axes(map_axis)
axis([-125, -114, 32, 42.5])
gca().set_axis_off()

# Loop over the ZIP codes in the boundary file
for polygon_id in d:
    polygon_data = array(d[polygon_id]['polygon'])
    zipcode = d[polygon_id]['name']
    # Draw the ZIP code
    patch = Polygon(array(polygon_data)
    gca().add_patch(patch)

# Change all fonts to Arial
for o in gcf().findobj(matplotlib.text.Text):
    o.set_fontname('Arial')

# Export figure to bitmap?
savefig('../images/Seattle_zips.png')
