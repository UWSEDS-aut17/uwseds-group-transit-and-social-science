'''
Example of bus route graph
'''
import geoplotlib
from geoplotlib.utils import read_csv
data = read_csv('./data/testroute.csv')
geoplotlib.dot(data)
geoplotlib.show()
