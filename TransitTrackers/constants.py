#List of constants accessed in our main transit_tracker.py script

#URL for downloading data
URL = 'https://www.psrc.org/sites/default/files/2014-hhsurvey.zip'
#list of age ranges used to make labels
AGE_RANGE_LIST = list(range(0,12))
#List of education ranges used to make labels
EDU_RANGE_LIST = list(range(0,7))
#Tools used in Bokeh  plotting
TOOLS = "pan,wheel_zoom,reset,poly_select,box_select,tap,box_zoom,save"
#List of zip codes used for PSRC data
USED_ZIPS_PSRC = ['98101', '98102', '98103', '98104', '98105', '98106', '98107',
             '98108', '98109', '98112', '98115', '98116', '98117', '98118',
             '98119', '98121', '98122', '98125', '98126', '98133', '98136',
             '98144', '98146', '98177', '98178', '98195', '98199']
#list of length of used_zips for customJS code creation
N_PSRC = range(len(used_zips))
#Line width for Bokeh plotting PSRC data
WD = 2
#Line width for Bokeh plotting bus routes
WD2 = 2
