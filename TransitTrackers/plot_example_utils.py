from bokeh.io import output_file, show, save
from bokeh.models import ColumnDataSource, CustomJS, HoverTool, LogColorMapper
from bokeh.models import GeoJSONDataSource
from bokeh.palettes import Viridis11 as palette
from bokeh.palettes import Magma4 as palette1
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, gridplot
from bokeh.models.widgets import CheckboxGroup, Select, Paragraph, Div
import utils
import js_utils
import geopandas as gpd
import pandas as pd
import math

# Shapefile of Seattle zipcodes
grid_fp = r"../Data/zips_sea/shp.shp"

# Shapefile of bus routes of Seattle
network_fp = r"../Data/bus_seattle/network.shp"

# CSV file of zip codes and number of routes passing through them
zips_sea_fp = '../Data/zips_seattle.csv'

# CSV file of route numbers that passing through each zip code
zip_route_fp = '../Data/routes_zipcode.csv'


def plot(grid_fp, network_fp, zip_route_fp, zips_sea_fp):

    grid = gpd.read_file(grid_fp)
    network = gpd.read_file(network_fp)

    # The following functions help us to get coordinates from the shapefiles
   # to map

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
            return list(getLineCoords(geom, coord_type))
        elif gtype == "Polygon":
            return list(getPolyCoords(geom, coord_type))

    grid['x'] = grid.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
    grid['y'] = grid.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)

    # CSV file of zip codes and number of routes passing through them
    zips_sea = pd.read_csv(zips_sea_fp)

    # CSV file of route numbers that passing through each zip code
    zip_route = pd.read_csv(zip_route_fp)

    zip_route = zip_route.dropna(axis=0, how='any')
    routes = {}
    name = ()
    f = 0
    for c in range(0, 30):
        name = zips_sea.zip[c].astype(str)
        routes[c] = zip_route['x'][f:(zips_sea['count'][c].astype(int)) +f].astype(int).astype(str)
        f = f + zips_sea['count'][c].astype(int)

    # PSRC Data Plotting

    g_df = grid.drop('geometry', axis=1).copy()
    gsource = ColumnDataSource(g_df)

    network0 = network.loc[network.OBJECTID.isin(routes[0]), :]
    network0['zip'] = zips_sea.zip[0]
    ns0 = GeoJSONDataSource(geojson=network0.to_json())

    network1 = network.loc[network.OBJECTID.isin(routes[1]), :]
    network1['zip'] = zips_sea.zip[1]
    ns1 = GeoJSONDataSource(geojson=network0.to_json())

    # Javascript code for bus routes map
    N_plots = range(0, 1)
    checkbox_code = js_utils.js_code(N_plots)
    TOOLS = "pan,wheel_zoom,reset,poly_select,box_select,tap,box_zoom,save"
    # Defining the figure
    p = figure(title="Seattle Bus Routes by Zipcode", tools=TOOLS,
    x_range=(-122.5, -122.1), y_range=(47.46, 47.8),
    plot_width=600, plot_height=600)

    # Plot grid with income as base colors
    grid2 = p.patches('x', 'y', source=gsource,
                  fill_color='white',
                  fill_alpha=1, line_color="black", line_width=.4,
                  legend='bin')

    # Color and line width for routes
    col = palette1[2]
    wd = 0.5

    # ploting routes
    r0 = p.multi_line('xs', 'ys', source=ns0, color=col, line_width=wd)
    r1 = p.multi_line('xs', 'ys', source=ns1, color=col, line_width=wd)	

    ghover = HoverTool(renderers=[grid2])
    ghover.tooltips = [("zip code", "@GEOID10")]
    p.add_tools(ghover)

    # Defining checkbox
    checkbox = CheckboxGroup(labels=list(zips_sea['zip'][0:30].astype(str)),
                         active=[])
    checkbox.callback = CustomJS(args=dict(l0=r0, l1=r1),
                             code=checkbox_code)
    description = Div(text="""This is <b>Transit Trackers!</b> Your interactive map
    for Seattle transit trends and socioeconomic data. Customize these maps by selecting which zipcodes you are intersted in. Each figure can be saved by clicking on the save icon in the toolbar for the Map.""", width=600, height=100)
    para_routes = Paragraph(text="""Map of Bus Routes and Seattle Income 
    Brackets. Specifying a zipcode from the checkbox list displays the bus routes 
    that service the specified zipcode.
    """,
                        width=200, height=100)
    layout = gridplot([widgetbox(description)],
                  [widgetbox(para_routes), p, widgetbox(checkbox)])
    outfp = r"../TransitTrackers/transit_trackers_ex.html"
    output_file(outfp, title='Transit Trackers', mode='cdn', root_dir=None)
    save (layout)
    return(layout, outfp)             						 
plot(grid_fp, network_fp, zip_route_fp, zips_sea_fp)