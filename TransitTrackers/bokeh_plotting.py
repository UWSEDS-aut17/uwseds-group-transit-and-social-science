from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper, GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
from bokeh.io import show, output_notebook
from bokeh.models import GeoJSONDataSource, LinearColorMapper
import geopandas as gpd
from bokeh.palettes import Viridis6 as palette
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

grid_fp = r"C:/Users/tdjor/OneDrive/Documents/Grad School Classes/SoftwareDesign/uwseds-group-transit-and-social-science/Data/zips_sea/shp.shp"
grid = gpd.read_file(grid_fp)

def getXYCoords(geometry, coord_type):
    """ Returns either x or y coordinates from  geometry coordinate sequence. Used with LineString and Polygon geometries."""
    if coord_type == 'x':
        return geometry.coords.xy[0]
    elif coord_type == 'y':
        return geometry.coords.xy[1]

def getLineCoords(geometry, coord_type):
    """ Returns Coordinates of Linestring object."""
    return getXYCoords(geometry, coord_type)

def getPolyCoords(geometry, coord_type):
    """ Returns Coordinates of Polygon using the Exterior of the Polygon."""
    ext = geometry.exterior
    return getXYCoords(ext, coord_type)

def getCoords(row, geom_col, coord_type):
    """
    Returns coordinates ('x' or 'y') of a geometry (Point, LineString or Polygon) as a list (if geometry is LineString or Polygon).
    Can handle also MultiGeometries.
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

    #p.legend.location = "top_right"
    #p.legend.orientation = "vertical"


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
    show(layout)
