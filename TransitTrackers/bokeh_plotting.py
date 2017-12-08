from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper, GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
from bokeh.io import show, output_notebook
from bokeh.models import GeoJSONDataSource, LinearColorMapper
import geopandas as gpd
from bokeh.palettes import Viridis6 as palette
from bokeh.palettes import Viridis11 as palette
from bokeh.palettes import Magma4 as palette1
import geopandas as gpd
import pysal as ps
import pandas as pd
import numpy as np
import math
from bokeh.palettes import Viridis11 as palette
from bokeh.models import LogColorMapper
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.plotting import figure, output_file, show
from bokeh.events import Tap
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Button,CheckboxGroup, Select
from bokeh.layouts import column, row,gridplot
import process_data

#Assign grid from Seattle zips shapefile
# shapefile of Seattle zip codes
grid_fp = r"uwseds-transit-trackers/Data/zips_sea/shp.shp"

#Shapefile of bus routes of Seattle
network_fp = r"uwseds-transit-trackers/Data/bus_seattle/network.shp"

#CSV file of zip codes and number of routes passing through them
zips_sea =pd.read_csv('uwseds-transit-trackers/Data/zips_seattle.csv')

#CSV file of route numbers that passing through each zip code
zip_route =pd.read_csv('uwseds-transit-trackers/Data/routes_zipcode.csv')

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

    # "Normal" geometries
    # -------------------

    if gtype == "Point":
        return getPointCoords(geom, coord_type)
    elif gtype == "LineString":
        return list( getLineCoords(geom, coord_type) )
    elif gtype == "Polygon":
        return list( getPolyCoords(geom, coord_type) )


grid['x'] = grid.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
grid['y'] = grid.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)


def psrc_trip_plotting():
    """
    This function takes the processed data from process_data.py and uses bokeh
    to plot an interactive map at an html.
    """
    #First we need to get the data processed in process_data for PSRC
    process_data.psrc_trip_data()
    g_df = grid.drop('geometry', axis=1).copy()
    gsource = ColumnDataSource(g_df)
    output_notebook()

    TOOLS = "pan,wheel_zoom,reset,poly_select,box_select,tap,box_zoom"
    p = figure(title="Most Frequent Destinations by Zipcode",tools=TOOLS)

    # Plot grid
    grid2 = p.patches('x', 'y', source=gsource,
             fill_color='blue',
             fill_alpha=0.010, line_color="black", line_width=1)

    trip0 = p.line(t0_xs, t0_ys, color="red", line_width=2)
    trip1 = p.line(t1_xs, t1_ys, color="red", line_width=2)
    trip2 = p.line(t2_xs, t2_ys, color="red", line_width=2)
    trip3 = p.line(t3_xs, t3_ys, color="red", line_width=2)
    trip4 = p.line(t4_xs, t4_ys, color="red", line_width=2)
    trip5 = p.circle(t5_xs, t5_ys, color="red", line_width=2)
    trip6 = p.line(t6_xs, t6_ys, color="red", line_width=2)
    trip7 = p.circle(t7_xs, t7_ys, color="red", line_width=2)
    trip8 = p.line(t8_xs, t8_ys, color="red", line_width=2)
    trip9 = p.line(t9_xs, t9_ys, color="red", line_width=2)
    trip10 = p.line(t10_xs, t10_ys, color="red", line_width=2)
    trip11 = p.circle(t11_xs, t11_ys, color="red", line_width=2)
    trip12 = p.line(t12_xs, t12_ys, color="red", line_width=2)
    trip13 = p.circle(t13_xs, t13_ys, color="red", line_width=2)
    trip14 = p.line(t14_xs, t14_ys, color="red", line_width=2)
    trip15 = p.line(t15_xs, t15_ys, color="red", line_width=2)
    trip16 = p.line(t16_xs, t16_ys, color="red", line_width=2)
    trip17 = p.line(t17_xs, t17_ys, color="red", line_width=2)
    trip18 = p.line(t18_xs, t18_ys, color="red", line_width=2)
    trip19 = p.circle(t19_xs, t19_ys, color="red", line_width=2)
    trip20 = p.circle(t20_xs, t20_ys, color="red", line_width=2)
    trip21 = p.line(t21_xs, t21_ys, color="red", line_width=2)
    trip22 = p.line(t22_xs, t22_ys, color="red", line_width=2)
    trip23 = p.circle(t23_xs, t23_ys, color="red", line_width=2)


    checkbox = CheckboxGroup(labels=used_zips)

    checkbox.callback = CustomJS(args=dict(l0=trip0, l1=trip1, l2=trip2, l3=trip3,
                                           l4=trip4, l5=trip5, l6=trip6, l7=trip7, l8=trip8,
                                           l9=trip9, l10=trip10, l11=trip11, l12=trip12,
                                           l13=trip13, l14=trip14, l15=trip15, l16=trip16,
                                           l17=trip17, l18=trip18, l19=trip19, l20=trip20,
                                           l21=trip21, l22=trip22, l23=trip23 ),
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

            }
        }
    """)
    checkbox_code = """
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
            }
        }
    """

    layout = row(p, widgetbox(checkbox))
    outfp = r"C:/Users/tdjor/OneDrive/Documents/Grad School Classes/SoftwareDesign/uwseds-group-transit-and-social-science/examples/trip_map.html"
    output_file(outfp, title = "Trip Map", mode= 'cdn', root_dir=None)
    show(layout)


def bus_plotting():
    """
    This function takes the processed data from process_data.py and uses bokeh
    to plot an interactive map at an html.
    """

    # Creating routes list to store bus number for each zip code

    routes = {}
    name = ()
    f = 0
    for c in range(0,30):
        name = zips_sea.zip[c].astype(str)
        routes[c] = zip_route['x'][f:(zips_sea['count'][c].astype(int))+f].astype(int).astype(str)
        f = f + zips_sea['count'][c].astype(int)

    #extracting bus routes for each zip code

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

    network30 = network.loc[network.ROUTE_NUM.isin(routes[30]) , :]
    network30['zip'] = zips_sea.zip[30]
    ns30 = GeoJSONDataSource(geojson=network30.to_json())

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
        l30.visible = false;

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
            } else if (cb_obj.active[i] == 30) {
                l30.visible = true;

            }
        }
    """
    #Desired tools for Bokeh map
    TOOLS = "pan,wheel_zoom,reset,poly_select,box_select,tap,box_zoom"

    #Generating colors for identifying income on map
    color_mapper = LogColorMapper(palette=palette)

    #Defining the figure
    p = figure(title="Seattle Bus Routes",tools=TOOLS,x_range=(-122.5, -122.1),y_range=(47.46, 47.8))

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
    r21=p.multi_line('xs', 'ys', source=ns11, color= col, line_width= wd)
    r22=p.multi_line('xs', 'ys', source=ns12, color= col, line_width= wd)
    r23=p.multi_line('xs', 'ys', source=ns13, color= col, line_width= wd)
    r24=p.multi_line('xs', 'ys', source=ns14, color= col, line_width= wd)
    r25=p.multi_line('xs', 'ys', source=ns15, color= col, line_width= wd)
    r26=p.multi_line('xs', 'ys', source=ns16, color= col, line_width= wd)
    r27=p.multi_line('xs', 'ys', source=ns17, color= col, line_width= wd)
    r28=p.multi_line('xs', 'ys', source=ns18, color= col, line_width= wd)
    r29=p.multi_line('xs', 'ys', source=ns19, color= col, line_width= wd)
    r30=p.multi_line('xs', 'ys', source=ns20, color= col, line_width= wd)

    #Defining hover tool
    ghover = HoverTool(renderers=[grid2])
    ghover.tooltips=[("zip code", "@GEOID10")]
    p.add_tools(ghover)

    #Defining checkbox
    checkbox = CheckboxGroup(labels=list(zips_sea['zip'][0:30].astype(str)), active= [])
    checkbox.callback = CustomJS(args=dict(l0=r0, l1=r1, l2=r2, l3=r3,l4=r4, l5=r5, l6=r6, l7=r7, l8=r8,l9=r9,l10=r10,l11=r11,
                                   l12=r12,l13=r13,l14=r14,l15=r15,l16=r16,l17=r17,l18=r18,l19=r19,l20=r20,l21=r21,
                                          l22=r22,l23=r23,l24=r24,l25=r25,l26=r26,l27=r27,l28=r28,l29=r29,l30=r30),
                                 code=code )

    group = widgetbox(checkbox)

    layout = gridplot([[p,group]])
    outfp = r"C:/Users/ASUS/Desktop/uwsed/uwseds-group-transit-and-social-science/examples/map.html"
    output_file(outfp , title='Bokeh Plot', mode='cdn', root_dir=None)
    show(layout)
