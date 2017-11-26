'''
Example of bus route graph
'''
import geoplotlib
from geoplotlib.utils import read_csv

data = read_csv('./data/testroute_line.csv')
geoplotlib.graph(data,
                 src_lat='x',
                 src_lon='y',
                 dest_lat='xd',
                 dest_lon='yd',
                 color='Greens',
                 alpha=255,
                 linewidth=5)
geoplotlib.show()
