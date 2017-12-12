from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, CustomJS, HoverTool, LogColorMapper, GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
from bokeh.io import show, output_notebook
from bokeh.models import GeoJSONDataSource, LinearColorMapper
from bokeh.palettes import Viridis11 as palette
from bokeh.palettes import Magma4 as palette1
from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.events import Tap
from bokeh.layouts import widgetbox, column, row, gridplot
from bokeh.models.widgets import CheckboxGroup, Select, Paragraph, Div

import os
import geopandas as gpd
import pysal as ps
import pandas as pd
import numpy as np
import math

# Processing SocioEconomic Data
#Read in data from the households and persons sheets
household_df = pd.read_excel('../Data/2014-pr3-hhsurvey-households.xlsx')
persons_df = pd.read_excel('../Data/2014-pr3-hhsurvey-persons.xlsx')

#Add household data required to persons_df
hh_zip = []
hh_city = []
#for i in range(0,len(household_df['hhid'])):
for i in range(0,len(persons_df['hhid'])):
    hh_zip.extend(household_df.query('hhid ==' + str(persons_df['hhid'][i]))['h_zip'])
    hh_city.extend(household_df.query('hhid ==' + str(persons_df['hhid'][i]))['h_city'])

persons_df['h_zip'] = hh_zip
persons_df['h_city'] =hh_city

Sea_df = persons_df[(persons_df['h_city'] == 'SEATTLE')]
ddf = Sea_df[['h_zip', 'h_city', 'age', 'relationship', 'gender',
              'employment', 'worker', 'education']]

df = ddf.dropna(how='any')

df['h_zip'] = df.h_zip.astype(int)
df['employment'] = df.employment.astype(int)
df['education'] = df.education.astype(int)

df['age_scaled'] = df['age']
df['edu_scaled'] = df['education']
df.loc[df['age'] == 1, 'age_scaled'] = 'Under 5'
df.loc[df['age'] == 2, 'age_scaled'] = '5-11'
df.loc[df['age'] == 3, 'age_scaled'] = '12-15'
df.loc[df['age'] == 4, 'age_scaled'] = '16-17'
df.loc[df['age'] == 5, 'age_scaled'] = '18-24'
df.loc[df['age'] == 6, 'age_scaled'] = '25-34'
df.loc[df['age'] == 7, 'age_scaled'] = '35-44'
df.loc[df['age'] == 8, 'age_scaled'] = '45-54'
df.loc[df['age'] == 9, 'age_scaled'] = '55-64'
df.loc[df['age'] == 10, 'age_scaled'] = '65-74'
df.loc[df['age'] == 11, 'age_scaled'] = '75-84'
df.loc[df['age'] == 12, 'age_scaled'] = '85 or older'
df.loc[df['education'] == 1, 'edu_scaled'] = 'Less than High School'
df.loc[df['education'] == 2, 'edu_scaled'] = 'High School'
df.loc[df['education'] == 3, 'edu_scaled'] = 'Some College'
df.loc[df['education'] == 4, 'edu_scaled'] = 'Vocational/Technical Training'
df.loc[df['education'] == 5, 'edu_scaled'] = 'Associates Degree'
df.loc[df['education'] == 6, 'edu_scaled'] = 'Bachelor Degree'
df.loc[df['education'] == 7, 'edu_scaled'] = 'Graduate/Post-Graduate Degree'

age_group = df.groupby(['h_zip'])['age_scaled'].value_counts().to_frame()
edu_group = df.groupby(['h_zip'])['edu_scaled'].value_counts().to_frame()
age_group.to_csv('../Data/age_grouped.csv')
edu_group.to_csv('../Data/edu_grouped.csv')

#Process data for Trip Frequency

#Read initial dataframes from GitHub
households_df = pd.read_excel('../Data/2014-pr3-hhsurvey-households.xlsx')
persons_df = pd.read_excel('../Data/2014-pr3-hhsurvey-persons.xlsx')
trips_df = pd.read_excel('../Data/2014-pr3-hhsurvey-trips.xlsx')

#Clean dataframes to include only Seattle data
sea_trips_df = trips_df.loc[(trips_df['ocity']== 'SEATTLE') & (trips_df['dcity'] == 'SEATTLE')]
sea_households_df = households_df.loc[households_df['hhid'].isin(sea_trips_df['hhid'])]
sea_person_df = persons_df.loc[persons_df['personid'].isin(sea_trips_df['personID'])]

#Merge dataframes to all_df
trips_households_df = sea_trips_df.merge(sea_households_df, left_on = 'hhid', right_on = 'hhid', how = 'inner')
all_df = trips_households_df.merge(sea_person_df, left_on ='personID', right_on='personid', how = 'inner')

#Extract only the columns we need from the all_df to df
df = all_df[['ozip', 'dzip']]

#Want a count of trips taken from any ozip to any dzip
trip_freq = df.groupby(['ozip'])['dzip'].value_counts().to_frame()

#Any frequency less than 50 is filtered out
sub = trip_freq.query('dzip > 10')
sub.to_csv('../Data/trip_freq.csv')
trip_freq2 = pd.read_csv('../Data/trip_freq.csv')
zip_latlon = pd.read_excel('../Data/zipcode_latlong.xlsx')

# Adds latitude and longitude to the origin and destination zipcodes
olat = list(range(0,len(trip_freq2)))
olon = list(range(0,len(trip_freq2)))
dlat = list(range(0,len(trip_freq2)))
dlon = list(range(0,len(trip_freq2)))

for i in list(range(0,len(trip_freq2))):
    origin_zip = trip_freq2.loc[i]['ozip']
    dest_zip = trip_freq2.loc[i]['dzip']
    olat[i] = float(zip_latlon.query('zipcode ==' +
                str(origin_zip))[['lat']].reset_index().loc[0]['lat'])
    olon[i] = float(zip_latlon.query('zipcode ==' +
                str(origin_zip))[['lon']].reset_index().loc[0]['lon'])
    dlat[i] = float(zip_latlon.query('zipcode ==' +
                str(dest_zip))[['lat']].reset_index().loc[0]['lat'])
    dlon[i] = float(zip_latlon.query('zipcode ==' +
                str(dest_zip))[['lon']].reset_index().loc[0]['lon'])

trip_freq2['olat'] = pd.Series(olat, index=trip_freq2.index)
trip_freq2['olon'] = pd.Series(olon, index=trip_freq2.index)
trip_freq2['dlat'] = pd.Series(dlat, index=trip_freq2.index)
trip_freq2['dlon'] = pd.Series(dlon, index=trip_freq2.index)
trip_freq2.to_csv('../Data/trip_freq_latlong.csv')

trip_freq2 = pd.read_csv('../Data/trip_freq_latlong.csv')

def make_trip_xsys(origin_zip):
    '''
    This function constructs the list of xs and ys
    properly formatted for the bokeh line plot.
    '''
    freq_trip = trip_freq2.query('ozip ==' + origin_zip).reset_index()
    freq_trip = freq_trip[['olat','olon','dlat','dlon']]
    ys = []
    xs = []
    for i in list(range(0,len(freq_trip))):
        ys = ys + [float(freq_trip.loc[0]['olat']),
                    float(freq_trip.loc[i]['dlat'])]
        xs = xs + [float(freq_trip.loc[0]['olon']),
                    float(freq_trip.loc[i]['dlon'])]
    return xs, ys

#Start assigning data of xs and ys from the origin and destination lat long
#to new dataframes for each zip code
[t0_xs,t0_ys] = make_trip_xsys('98101')
[t1_xs,t1_ys] = make_trip_xsys('98102')
[t2_xs,t2_ys] = make_trip_xsys('98103')
[t3_xs,t3_ys] = make_trip_xsys('98104')
[t4_xs,t4_ys] = make_trip_xsys('98105')
[t5_xs,t5_ys] = make_trip_xsys('98106')
[t6_xs,t6_ys] = make_trip_xsys('98107')
[t7_xs,t7_ys] = make_trip_xsys('98108')
[t8_xs,t8_ys] = make_trip_xsys('98109')
[t9_xs,t9_ys] = make_trip_xsys('98112')
[t10_xs,t10_ys] = make_trip_xsys('98115')
[t11_xs,t11_ys] = make_trip_xsys('98116')
[t12_xs,t12_ys] = make_trip_xsys('98117')
[t13_xs,t13_ys] = make_trip_xsys('98118')
[t14_xs,t14_ys] = make_trip_xsys('98119')
[t15_xs,t15_ys] = make_trip_xsys('98121')
[t16_xs,t16_ys] = make_trip_xsys('98122')
[t17_xs,t17_ys] = make_trip_xsys('98125')
[t18_xs,t18_ys] = make_trip_xsys('98126')
[t19_xs,t19_ys] = make_trip_xsys('98133')
[t20_xs,t20_ys] = make_trip_xsys('98136')
[t21_xs,t21_ys] = make_trip_xsys('98144')
[t22_xs,t22_ys] = make_trip_xsys('98146')
[t23_xs,t23_ys] = make_trip_xsys('98177')
[t24_xs,t24_ys] =make_trip_xsys('98178')
[t25_xs,t25_ys] =make_trip_xsys('98195')
[t26_xs,t26_ys] =make_trip_xsys('98199')

#Create list of the zip codes we're interested in
used_zips = ['98101','98102','98103','98104','98105','98106','98107',
            '98108','98109','98112','98115','98116','98117','98118',
             '98119','98121','98122','98125','98126','98133','98136',
             '98144','98146','98177','98178','98195','98199']

#Start Bokeh Plotting


#Assign grid from Seattle zips shapefile
grid_fp = r"../Data/zips_sea2/shp1.shp"

#Shapefile of bus routes of Seattle
network_fp = r"../Data/bus_seattle/network.shp"

#CSV file of zip codes and number of routes passing through them
zips_sea =pd.read_csv('../Data/zips_seattle.csv')

#CSV file of route numbers that passing through each zip code
zip_route =pd.read_csv('../Data/routes_zipcode.csv')

grid = gpd.read_file(grid_fp)
network = gpd.read_file(network_fp)


#The following functions help us to get coordinates from the shapefiles to map


def getXYCoords(geometry, coord_type):
    """
    Returns either x or y coordinates from  geometry coordinate sequence.
    Used with LineString and Polygon geometries.
    """
    if coord_type == 'x':
        return geometry.coords.xy[0]
    elif coord_type == 'y':
        return geometry.coords.xy[1]


def getLineCoords(geometry, coord_type):
    """
    Returns Coordinates of Linestring object.
    """
    return getXYCoords(geometry, coord_type)


def getPolyCoords(geometry, coord_type):
    """
    Returns Coordinates of Polygon using the Exterior of the Polygon.
    """
    ext = geometry.exterior
    return getXYCoords(ext, coord_type)


def getCoords(row, geom_col, coord_type):
    """
    Returns coordinates ('x' or 'y') of a geometry (Point, LineString or
    Polygon) as a list (if geometry is LineString or Polygon).
    Can also handle MultiGeometries.
    """
    # Get geometry
    geom = row[geom_col]

    # Check the geometry type
    gtype = geom.geom_type

    if gtype == "Point":
        return getPointCoords(geom, coord_type)
    elif gtype == "LineString":
        return list( getLineCoords(geom, coord_type) )
    elif gtype == "Polygon":
        return list( getPolyCoords(geom, coord_type) )


grid['x'] = grid.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
grid['y'] = grid.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)


#PSRC Data Plotting


g_df_psrc = grid.drop('geometry', axis=1).copy()
gsource_psrc = ColumnDataSource(g_df_psrc)

TOOLS = "pan,wheel_zoom,reset,poly_select,box_select,tap,box_zoom,save"
p_psrc = figure(title="Most Frequent Destinations by Zipcode",
            tools=TOOLS,x_range=(-122.5, -122.1),y_range=(47.46, 47.8),
            plot_width=600,plot_height=600)

# Plot grid
grid2_psrc = p_psrc.patches('x', 'y', source=gsource_psrc,
         fill_color=palette[2],
         fill_alpha=1.0, line_color="black", line_width=1)

#Color and line width for routes
col = palette1[3]
wd = 2

trip0 = p_psrc.line(t0_xs, t0_ys, color=col, line_width=wd)
trip1 = p_psrc.line(t1_xs, t1_ys, color=col, line_width=wd)
trip2 = p_psrc.line(t2_xs, t2_ys, color=col, line_width=wd)
trip3 = p_psrc.line(t3_xs, t3_ys, color=col, line_width=wd)
trip4 = p_psrc.line(t4_xs, t4_ys, color=col, line_width=wd)
trip5 = p_psrc.line(t5_xs, t5_ys, color=col, line_width=wd)
trip6 = p_psrc.line(t6_xs, t6_ys, color=col, line_width=wd)
trip7 = p_psrc.line(t7_xs, t7_ys, color=col, line_width=wd)
trip8 = p_psrc.line(t8_xs, t8_ys, color=col, line_width=wd)
trip9 = p_psrc.line(t9_xs, t9_ys, color=col, line_width=wd)
trip10 = p_psrc.line(t10_xs, t10_ys, color=col, line_width=wd)
trip11 = p_psrc.line(t11_xs, t11_ys, color=col, line_width=wd)
trip12 = p_psrc.line(t12_xs, t12_ys, color=col, line_width=wd)
trip13 = p_psrc.line(t13_xs, t13_ys, color=col, line_width=wd)
trip14 = p_psrc.line(t14_xs, t14_ys, color=col, line_width=wd)
trip15 = p_psrc.line(t15_xs, t15_ys, color=col, line_width=wd)
trip16 = p_psrc.line(t16_xs, t16_ys, color=col, line_width=wd)
trip17 = p_psrc.line(t17_xs, t17_ys, color=col, line_width=wd)
trip18 = p_psrc.line(t18_xs, t18_ys, color=col, line_width=wd)
trip19 = p_psrc.line(t19_xs, t19_ys, color=col, line_width=wd)
trip20 = p_psrc.line(t20_xs, t20_ys, color=col, line_width=wd)
trip21 = p_psrc.line(t21_xs, t21_ys, color=col, line_width=wd)
trip22 = p_psrc.line(t22_xs, t22_ys, color=col, line_width=wd)
trip23 = p_psrc.line(t23_xs, t23_ys, color=col, line_width=wd)
trip24 = p_psrc.line(t24_xs, t24_ys, color=col, line_width=wd)
trip25 = p_psrc.line(t25_xs, t25_ys, color=col, line_width=wd)
trip26 = p_psrc.line(t26_xs, t26_ys, color=col, line_width=wd)

checkbox_psrc = CheckboxGroup(labels=used_zips)

checkbox_psrc.callback = CustomJS(args=dict(l0=trip0, l1=trip1, l2=trip2,
                                    l3=trip3, l4=trip4, l5=trip5, l6=trip6,
                                    l7=trip7, l8=trip8, l9=trip9, l10=trip10,
                                    l11=trip11, l12=trip12, l13=trip13,
                                    l14=trip14, l15=trip15, l16=trip16,
                                    l17=trip17, l18=trip18, l19=trip19,
                                    l20=trip20, l21=trip21, l22=trip22,
                                    l23=trip23, l24 = trip24,
                                    l25 = trip25, l26 = trip26 ),
                                    code="""
    //console.log(cb_obj.active);
    l0.visible = false;
    l1.visible = false;
    l2.visible = false;
    l3.visible = false;
    l4.visible = false;
    l5.visible = false;
    l6.visible = false;
    l7.visible = false;
    l8.visible = false;
    l9.visible = false;
    l10.visible = false;
    l11.visible = false;
    l12.visible = false;
    l13.visible = false;
    l14.visible = false;
    l15.visible = false;
    l16.visible = false;
    l17.visible = false;
    l18.visible = false;
    l19.visible = false;
    l20.visible = false;
    l21.visible = false;
    l22.visible = false;
    l23.visible = false;
    l24.visible = false;
    l25.visible = false;
    l26.visible = false;

    for (i in cb_obj.active) {
        //console.log(cb_obj.active[i]);
        if (cb_obj.active[i] == 0) {
            l0.visible = true;
        } else if (cb_obj.active[i] == 1) {
            l1.visible = true;
        } else if (cb_obj.active[i] == 2) {
            l2.visible = true;
        } else if (cb_obj.active[i] == 3) {
            l3.visible = true;
        } else if (cb_obj.active[i] == 4) {
            l4.visible = true;
        } else if (cb_obj.active[i] == 5) {
            l5.visible = true;
        } else if (cb_obj.active[i] == 6) {
            l6.visible = true;
        } else if (cb_obj.active[i] == 7) {
            l7.visible = true;
        } else if (cb_obj.active[i] == 8) {
            l8.visible = true;
        } else if (cb_obj.active[i] == 9) {
            l9.visible = true;
        } else if (cb_obj.active[i] == 10) {
            l10.visible = true;
        } else if (cb_obj.active[i] == 11) {
            l11.visible = true;
        } else if (cb_obj.active[i] == 12) {
            l12.visible = true;
        } else if (cb_obj.active[i] == 13) {
            l13.visible = true;
        } else if (cb_obj.active[i] == 14) {
            l14.visible = true;
        } else if (cb_obj.active[i] == 15) {
            l15.visible = true;
        } else if (cb_obj.active[i] == 16) {
            l16.visible = true;
        } else if (cb_obj.active[i] == 17) {
            l17.visible = true;
        } else if (cb_obj.active[i] == 18) {
            l18.visible = true;
        } else if (cb_obj.active[i] == 19) {
            l19.visible = true;
        } else if (cb_obj.active[i] == 20) {
            l20.visible = true;
        } else if (cb_obj.active[i] == 21) {
            l21.visible = true;
        } else if (cb_obj.active[i] == 22) {
            l22.visible = true;
        } else if (cb_obj.active[i] == 23) {
            l23.visible = true;
        } else if (cb_obj.active[i] == 24) {
            l24.visible = true;
        } else if (cb_obj.active[i] == 25) {
            l25.visible = true;
        } else if (cb_obj.active[i] == 26) {
            l26.visible = true;
        }
    }
""")

para_psrc = Paragraph(text="""Network Map of Seattle Travel. For each zipcode,
a line from the selected zipcode conects to the most frequent destination
zipcodes. A dot representsthat the most frequent trips were within
the same zipcode.""",
width=200, height=100)

#Seattle Transit Mapping


# Creating routes list to store bus number for each zip code
zip_route = zip_route.dropna(axis= 0, how='any')
routes = {}
name = ()
f = 0
for c in range(0,30):
    name = zips_sea.zip[c].astype(str)
    routes[c] = zip_route['x'][f:(zips_sea['count'][c].astype(int))+f].astype(int).astype(str)
    f = f + zips_sea['count'][c].astype(int)

#Extracting bus routes for each zip code
network0 = network.loc[network.ROUTE_NUM.isin(routes[0]) , :]
network0['zip'] = zips_sea.zip[0]
ns0 = GeoJSONDataSource(geojson=network0.to_json())

network1 = network.loc[network.ROUTE_NUM.isin(routes[1]) , :]
network1['zip'] = zips_sea.zip[1]
ns1 = GeoJSONDataSource(geojson=network1.to_json())

network2 = network.loc[network.ROUTE_NUM.isin(routes[2]) , :]
network2['zip'] = zips_sea.zip[2]
ns2 = GeoJSONDataSource(geojson=network2.to_json())

network3 = network.loc[network.ROUTE_NUM.isin(routes[3]) , :]
network3['zip'] = zips_sea.zip[3]
ns3 = GeoJSONDataSource(geojson=network3.to_json())

network4 = network.loc[network.ROUTE_NUM.isin(routes[4]) , :]
network4['zip'] = zips_sea.zip[4]
ns4 = GeoJSONDataSource(geojson=network4.to_json())

network5 = network.loc[network.ROUTE_NUM.isin(routes[5]) , :]
network5['zip'] = zips_sea.zip[5]
ns5 = GeoJSONDataSource(geojson=network5.to_json())

network6 = network.loc[network.ROUTE_NUM.isin(routes[6]) , :]
network6['zip'] = zips_sea.zip[6]
ns6 = GeoJSONDataSource(geojson=network6.to_json())

network7 = network.loc[network.ROUTE_NUM.isin(routes[7]) , :]
network7['zip'] = zips_sea.zip[7]
ns7 = GeoJSONDataSource(geojson=network7.to_json())

network8 = network.loc[network.ROUTE_NUM.isin(routes[8]) , :]
network8['zip'] = zips_sea.zip[8]
ns8 = GeoJSONDataSource(geojson=network8.to_json())

network9 = network.loc[network.ROUTE_NUM.isin(routes[9]) , :]
network9['zip'] = zips_sea.zip[9]
ns9 = GeoJSONDataSource(geojson=network9.to_json())

network10 = network.loc[network.ROUTE_NUM.isin(routes[10]) , :]
network10['zip'] = zips_sea.zip[10]
ns10 = GeoJSONDataSource(geojson=network10.to_json())

network11 = network.loc[network.ROUTE_NUM.isin(routes[11]) , :]
network11['zip'] = zips_sea.zip[11]
ns11 = GeoJSONDataSource(geojson=network11.to_json())

network12 = network.loc[network.ROUTE_NUM.isin(routes[12]) , :]
network12['zip'] = zips_sea.zip[12]
ns12 = GeoJSONDataSource(geojson=network12.to_json())

network13 = network.loc[network.ROUTE_NUM.isin(routes[13]) , :]
network13['zip'] = zips_sea.zip[13]
ns13 = GeoJSONDataSource(geojson=network13.to_json())

network14 = network.loc[network.ROUTE_NUM.isin(routes[14]) , :]
network14['zip'] = zips_sea.zip[14]
ns14 = GeoJSONDataSource(geojson=network14.to_json())

network15 = network.loc[network.ROUTE_NUM.isin(routes[15]) , :]
network15['zip'] = zips_sea.zip[15]
ns15 = GeoJSONDataSource(geojson=network15.to_json())

network16 = network.loc[network.ROUTE_NUM.isin(routes[16]) , :]
network16['zip'] = zips_sea.zip[16]
ns16 = GeoJSONDataSource(geojson=network16.to_json())

network17 = network.loc[network.ROUTE_NUM.isin(routes[17]) , :]
network17['zip'] = zips_sea.zip[17]
ns17 = GeoJSONDataSource(geojson=network17.to_json())

network18 = network.loc[network.ROUTE_NUM.isin(routes[18]) , :]
network18['zip'] = zips_sea.zip[18]
ns18 = GeoJSONDataSource(geojson=network18.to_json())

network19 = network.loc[network.ROUTE_NUM.isin(routes[19]) , :]
network19['zip'] = zips_sea.zip[19]
ns19 = GeoJSONDataSource(geojson=network19.to_json())

network20 = network.loc[network.ROUTE_NUM.isin(routes[20]) , :]
network20['zip'] = zips_sea.zip[20]
ns20 = GeoJSONDataSource(geojson=network20.to_json())

network21 = network.loc[network.ROUTE_NUM.isin(routes[21]) , :]
network21['zip'] = zips_sea.zip[21]
ns21 = GeoJSONDataSource(geojson=network21.to_json())

network22 = network.loc[network.ROUTE_NUM.isin(routes[22]) , :]
network22['zip'] = zips_sea.zip[22]
ns22 = GeoJSONDataSource(geojson=network20.to_json())

network23 = network.loc[network.ROUTE_NUM.isin(routes[23]) , :]
network23['zip'] = zips_sea.zip[23]
ns23 = GeoJSONDataSource(geojson=network23.to_json())

network24 = network.loc[network.ROUTE_NUM.isin(routes[24]) , :]
network24['zip'] = zips_sea.zip[24]
ns24 = GeoJSONDataSource(geojson=network24.to_json())

network25 = network.loc[network.ROUTE_NUM.isin(routes[25]) , :]
network25['zip'] = zips_sea.zip[25]
ns25 = GeoJSONDataSource(geojson=network25.to_json())

network26 = network.loc[network.ROUTE_NUM.isin(routes[26]) , :]
network26['zip'] = zips_sea.zip[26]
ns26 = GeoJSONDataSource(geojson=network26.to_json())

network27 = network.loc[network.ROUTE_NUM.isin(routes[27]) , :]
network27['zip'] = zips_sea.zip[27]
ns27 = GeoJSONDataSource(geojson=network27.to_json())

network28 = network.loc[network.ROUTE_NUM.isin(routes[28]) , :]
network28['zip'] = zips_sea.zip[28]
ns28 = GeoJSONDataSource(geojson=network28.to_json())

network29 = network.loc[network.ROUTE_NUM.isin(routes[29]) , :]
network29['zip'] = zips_sea.zip[29]
ns29 = GeoJSONDataSource(geojson=network29.to_json())



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

#Sort shapefile based on income so have the legend in acsending order
grid = grid.sort_values(['income'])

#Drop the geometry from shapefile and create ColumnDataSource

g_df = grid.drop('geometry', axis=1).copy()
gsource = ColumnDataSource(g_df)

# Javascript code to be inputed in CustomJS for checkbox widget

code ="""
    //console.log(cb_obj.active);
    l0.visible = false;
    l1.visible = false;
    l2.visible = false;
    l3.visible = false;
    l4.visible = false;
    l5.visible = false;
    l6.visible = false;
    l7.visible = false;
    l8.visible = false;
    l9.visible = false;
    l10.visible = false;
    l11.visible = false;
    l12.visible = false;
    l13.visible = false;
    l14.visible = false;
    l15.visible = false;
    l16.visible = false;
    l17.visible = false;
    l18.visible = false;
    l19.visible = false;
    l20.visible = false;
    l21.visible = false;
    l22.visible = false;
    l23.visible = false;
    l24.visible = false;
    l25.visible = false;
    l26.visible = false;
    l27.visible = false;
    l28.visible = false;
    l29.visible = false;


    for (i in cb_obj.active) {
        //console.log(cb_obj.active[i]);
        if (cb_obj.active[i] == 0) {
            l0.visible = true;
        } else if (cb_obj.active[i] == 1) {
            l1.visible = true;
        } else if (cb_obj.active[i] == 2) {
            l2.visible = true;
        } else if (cb_obj.active[i] == 3) {
            l3.visible = true;
        } else if (cb_obj.active[i] == 4) {
            l4.visible = true;
        } else if (cb_obj.active[i] == 5) {
            l5.visible = true;
        } else if (cb_obj.active[i] == 6) {
            l6.visible = true;
        } else if (cb_obj.active[i] == 7) {
            l7.visible = true;
        } else if (cb_obj.active[i] == 8) {
            l8.visible = true;
        } else if (cb_obj.active[i] == 9) {
            l9.visible = true;
        } else if (cb_obj.active[i] == 10) {
            l10.visible = true;
        } else if (cb_obj.active[i] == 11) {
            l11.visible = true;
        } else if (cb_obj.active[i] == 12) {
            l12.visible = true;
        } else if (cb_obj.active[i] == 13) {
            l13.visible = true;
        } else if (cb_obj.active[i] == 14) {
            l14.visible = true;
        } else if (cb_obj.active[i] == 15) {
            l15.visible = true;
        } else if (cb_obj.active[i] == 16) {
            l16.visible = true;
        } else if (cb_obj.active[i] == 17) {
            l17.visible = true;
        } else if (cb_obj.active[i] == 18) {
            l18.visible = true;
        } else if (cb_obj.active[i] == 19) {
            l19.visible = true;
        } else if (cb_obj.active[i] == 20) {
            l20.visible = true;
        } else if (cb_obj.active[i] == 21) {
            l21.visible = true;
        } else if (cb_obj.active[i] == 22) {
            l22.visible = true;
        } else if (cb_obj.active[i] == 23) {
            l23.visible = true;
        } else if (cb_obj.active[i] == 24) {
            l24.visible = true;
        } else if (cb_obj.active[i] == 25) {
            l25.visible = true;
        } else if (cb_obj.active[i] == 26) {
            l26.visible = true;
        } else if (cb_obj.active[i] == 27) {
            l27.visible = true;
        } else if (cb_obj.active[i] == 28) {
            l28.visible = true;
        } else if (cb_obj.active[i] == 29) {
            l29.visible = true;
        }
    }
"""

#Generating colors for identifying income on map
color_mapper = LogColorMapper(palette=palette)

#Defining the figure
p = figure(title="Seattle Bus Routes",tools=TOOLS,x_range=(-122.5, -122.1),
                y_range=(47.46, 47.8),plot_width=600,plot_height=600)

# Plot grid with income as base colors
grid2 = p.patches('x', 'y', source=gsource,
        fill_color={'field': 'incomeb', 'transform' : color_mapper},
         fill_alpha=1, line_color="black", line_width=.4,legend = 'bin')

#Color and line width for routes
col = palette1[2]
wd = 0.5

#ploting routes
r0=p.multi_line('xs', 'ys', source=ns0, color= col, line_width= wd)
r1=p.multi_line('xs', 'ys', source=ns1, color= col, line_width= wd)
r2=p.multi_line('xs', 'ys', source=ns2, color= col, line_width= wd)
r3=p.multi_line('xs', 'ys', source=ns3, color= col, line_width= wd)
r4=p.multi_line('xs', 'ys', source=ns4, color= col, line_width= wd)
r5=p.multi_line('xs', 'ys', source=ns5, color= col, line_width= wd)
r6=p.multi_line('xs', 'ys', source=ns6, color= col, line_width= wd)
r7=p.multi_line('xs', 'ys', source=ns7, color= col, line_width= wd)
r8=p.multi_line('xs', 'ys', source=ns8, color= col, line_width= wd)
r9=p.multi_line('xs', 'ys', source=ns9, color= col, line_width= wd)
r10=p.multi_line('xs', 'ys', source=ns10, color= col, line_width= wd)
r11=p.multi_line('xs', 'ys', source=ns11, color= col, line_width= wd)
r12=p.multi_line('xs', 'ys', source=ns12, color= col, line_width= wd)
r13=p.multi_line('xs', 'ys', source=ns13, color= col, line_width= wd)
r14=p.multi_line('xs', 'ys', source=ns14, color= col, line_width= wd)
r15=p.multi_line('xs', 'ys', source=ns15, color= col, line_width= wd)
r16=p.multi_line('xs', 'ys', source=ns16, color= col, line_width= wd)
r17=p.multi_line('xs', 'ys', source=ns17, color= col, line_width= wd)
r18=p.multi_line('xs', 'ys', source=ns18, color= col, line_width= wd)
r19=p.multi_line('xs', 'ys', source=ns19, color= col, line_width= wd)
r20=p.multi_line('xs', 'ys', source=ns20, color= col, line_width= wd)
r21=p.multi_line('xs', 'ys', source=ns21, color= col, line_width= wd)
r22=p.multi_line('xs', 'ys', source=ns22, color= col, line_width= wd)
r23=p.multi_line('xs', 'ys', source=ns23, color= col, line_width= wd)
r24=p.multi_line('xs', 'ys', source=ns24, color= col, line_width= wd)
r25=p.multi_line('xs', 'ys', source=ns25, color= col, line_width= wd)
r26=p.multi_line('xs', 'ys', source=ns26, color= col, line_width= wd)
r27=p.multi_line('xs', 'ys', source=ns27, color= col, line_width= wd)
r28=p.multi_line('xs', 'ys', source=ns28, color= col, line_width= wd)
r29=p.multi_line('xs', 'ys', source=ns29, color= col, line_width= wd)


#Defining hover tool
ghover = HoverTool(renderers=[grid2])
ghover.tooltips=[("zip code", "@GEOID10")]
p.add_tools(ghover)

#Defining checkbox
checkbox = CheckboxGroup(labels=list(zips_sea['zip'][0:30].astype(str)),
                            active= [])
checkbox.callback = CustomJS(args=dict(l0=r0, l1=r1, l2=r2, l3=r3,l4=r4,
                                l5=r5, l6=r6, l7=r7, l8=r8,l9=r9,l10=r10,
                                l11=r11, l12=r12, l13=r13, l14=r14, l15=r15,
                                l16=r16, l17=r17, l18=r18,l19=r19, l20=r20,
                                l21=r21, l22=r22, l23=r23, l24=r24, l25=r25,
                                l26=r26, l27=r27, l28=r28, l29=r29),
                                code=code )

para_routes = Paragraph(text="""Map of Bus Routes and Seattle Income
Brackets. Specifying a zipcode from the checkbox list displays the bus routes
that service the specified zipcode.
""",
width=200, height=100)

group = widgetbox(checkbox)

#Begin processing socioeconomic data


age_group = pd.read_csv('../Data/age_grouped.csv')
edu_group = pd.read_csv('../Data/edu_grouped.csv')
age_group = age_group.rename(index=str, columns={'age_scaled.1':'age_counts'})
edu_group = edu_group.rename(index=str, columns={'edu_scaled.1':'edu_counts'})

age_scale = {}
edu_scale = {}
age_count = {}
edu_count = {}
for i in used_zips:
    age_scale[i] = age_group.query('h_zip ==' + i)['age_scaled'].tolist()
    age_count[i] = age_group.query('h_zip ==' + i)['age_counts'].tolist()
    edu_scale[i] = edu_group.query('h_zip ==' + i)['edu_scaled'].tolist()
    edu_count[i] = edu_group.query('h_zip ==' + i)['edu_counts'].tolist()

age_x = age_scale['98102']
age_y = age_count['98102']
edu_x = edu_scale['98102']
edu_y = edu_count['98102']

age_data_CDS = ColumnDataSource(data = age_scale)
age_count_CDS = ColumnDataSource(data = age_count)
age_data_zip = {'x': age_x,'y': age_y}
age_plot_data = ColumnDataSource(data=age_data_zip)
edu_data_CDS = ColumnDataSource(data=edu_scale)
edu_count_CDS = ColumnDataSource(data=edu_count)
edu_data_zip = {'x': edu_x,'y': edu_y}
edu_plot_data = ColumnDataSource(data=edu_data_zip)

age_plot = figure(title ='Age Distribution by Zipcode',tools=TOOLS,plot_width=600, plot_height=600,x_range=age_x)
age_plot.vbar(x = 'x',top = 'y',source=age_plot_data, width = .5, color = 'firebrick')
edu_plot = figure(title = 'Education Distribution by Zipcode',tools=TOOLS,plot_width=600, plot_height=600,x_range=edu_x)
edu_plot.vbar(x = 'x',top = 'y',source=edu_plot_data,width = 0.5, color = 'firebrick')
edu_plot.xaxis.major_label_orientation = math.pi/3

select = Select(title='Zipcode', value='98102',options = used_zips)

callback = CustomJS(args={'source1':age_plot_data,'source2':age_data_CDS,'source3':age_count_CDS,
                         'source4':edu_plot_data,'source5':edu_data_CDS,'source6':edu_count_CDS}, code="""
        var age_plot_data = source1.data;
        var age_scale_data = source2.data;
        var age_count_data = source3.data;
        var edu_plot_data = source4.data;
        var edu_scale_data = source5.data;
        var edu_count_data = source6.data;
        var f = cb_obj.value
        for (var e in age_plot_data) delete age_plot_data[e];
        age_plot_data['x'] = age_scale_data[f]
        age_plot_data['y'] = age_count_data[f]
        for (var e in edu_plot_data) delete edu_plot_data[e];
        edu_plot_data['x'] = edu_scale_data[f]
        edu_plot_data['y'] = edu_count_data[f]
        source1.change.emit();
        source4.change.emit();
    """)

select.js_on_change('value',callback)

description = Div(text="""This is <b>Transit Trackers!</b> Your interactive map
for Seattle transit trends and socioeconomic data. Customize these
maps by selecting which zipcodes you are intersted in.
Each figure can be saved by clicking on the save icon in the
toolbar for the Map.""",width=600, height=100)

para_soc = Paragraph(text="""These graphs show the age and education
distribution for the zipcode selected in the dropdown menu""",width=200,
height=100)

layout = gridplot([widgetbox(description)],
            [widgetbox(para_routes),p, widgetbox(checkbox)],
            [widgetbox(para_psrc),p_psrc,widgetbox(checkbox_psrc)],
            [age_plot,edu_plot,widgetbox(select,para_soc)])

outfp = r"../examples/transit_trackers.html"
output_file(outfp , title='Transit Trackers', mode='cdn', root_dir=None)
show(layout)