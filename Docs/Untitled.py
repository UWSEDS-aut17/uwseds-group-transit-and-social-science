
# coding: utf-8

# In[22]:


from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
import geopandas as gpd
import pysal as ps


# In[23]:


import geopandas as gpd


# In[24]:


grid_fp = r"C:/Users/jabbari/Desktop/uwseds-group-transit-and-social-science/Data/tract2010/tract2010.shp"


# In[53]:


grid = gpd.read_file(grid_fp)
grid = grid.loc[grid['COUNTYFP10'] == '033']


# In[54]:


grid['geometry'] = grid['geometry'].to_crs(crs='+init=epsg:4326')


# In[55]:


CRS = grid.crs
print(CRS)


# In[56]:


grid['geometry'].head()


# In[57]:


def getXYCoords(geometry, coord_type):
    """ Returns either x or y coordinates from  geometry coordinate sequence. Used with LineString and Polygon geometries."""
    if coord_type == 'x':
        return geometry.coords.xy[0]
    elif coord_type == 'y':
        return geometry.coords.xy[1]


# In[58]:


def getPolyCoords(geometry, coord_type):
    """ Returns Coordinates of Polygon using the Exterior of the Polygon."""
    ext = geometry.exterior
    return getXYCoords(ext, coord_type)


# In[59]:


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
        


# In[60]:


grid['x'] = grid.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
grid['y'] = grid.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)


# In[61]:


def getPolyCoords(row, geom, coord_type):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior"""

    # Parse the exterior of the coordinate
    exterior = row[geom].exterior

    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list( exterior.coords.xy[0] )
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list( exterior.coords.xy[1] )


# In[35]:


# Get the Polygon x and y coordinates
grid['x'] = grid.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
grid['y'] = grid.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)


# In[62]:


grid.head ()


# In[63]:


g_df = grid.drop('geometry', axis=1).copy()
gsource = ColumnDataSource(g_df)


# In[64]:


from bokeh.palettes import RdYlBu11 as palette
from bokeh.models import LogColorMapper

# Create the color mapper
color_mapper = LogColorMapper(palette=palette)


# In[67]:


p = figure(title="Travel times with Public transportation to Central Railway station")

# Plot grid
p.patches('x', 'y', source=gsource,
         fill_color="white",
         fill_alpha=1.0, line_color="black", line_width=0.5)


# In[68]:


outfp = r"C:/Users/jabbari/Desktop/uwseds-group-transit-and-social-science/Docs/map.html"
save(p, outfp)

