
# coding: utf-8

# In[3]:


from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
import geopandas as gpd
import pysal as ps


# In[13]:


import geopandas as gpd


# In[4]:


grid_fp = r"C:/Users/jabbari/Desktop/uwseds-group-transit-and-social-science/Data/tract2010/tract2010.shp"


# In[5]:


grid = gpd.read_file(grid_fp)


# In[6]:


grid['geometry'] = grid['geometry'].to_crs(crs='+init=epsg:4326')


# In[7]:


CRS = grid.crs
print(CRS)


# In[20]:


grid['geometry'].head(1)


# In[9]:


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


# In[19]:





# In[21]:


# Get the Polygon x and y coordinates
grid['x'] = grid.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
grid['y'] = grid.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)


# In[11]:


grid.head ()

