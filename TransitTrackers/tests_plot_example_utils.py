from bs4 import BeautifulSoup
import codecs
import os
import re
import unittest
import plot_example_utils
import geopandas as gpd


# Shapefile of Seattle zipcodes
grid_fp = r"../Data/zips_sea/shp.shp"

# Shapefile of bus routes of Seattle
network_fp = r"../Data/bus_seattle/network.shp"

# CSV file of zip codes and number of routes passing through them
zips_sea_fp = '../Data/zips_seattle.csv'

# CSV file of route numbers that passing through each zip code
zip_route_fp = '../Data/routes_zipcode.csv'


class plotting_test(unittest.TestCase):

    def test_plot_bokeh(self):
        # Test for plotting code generator to see if the outecome
        # is actually in bokeh model format
        arg0 = plot_example_utils.plot(
            grid_fp, network_fp, zip_route_fp, zips_sea_fp)
        self.assertEqual(str(type(arg0[0])),
                         "<class 'bokeh.models.layouts.Column'>")

    def test_plot_bokeh_html(self):
        # This test is to make sure that the code store
        # Result as html file
        arg1 = plot_example_utils.plot(
            grid_fp, network_fp, zip_route_fp, zips_sea_fp)
        st = arg1[1].split('/')
        l = len(st)
        self.assertTrue(os.path.exists(st[l - 1]) is True)

    def test_html_parser(self):
                # This function tests whether the created html
                # has bk-root and bk-plotdiv which should exist in
                # HTML files generated for bokeh plots
        plot_example_utils.plot(
            grid_fp, network_fp, zip_route_fp, zips_sea_fp)
        f = codecs.open("transit_trackers_ex.html")
        x = f.read()
        soup = BeautifulSoup(x, "html.parser")
        item = soup.findAll("div")
        self.assertTrue(item[0]['class'], ['bk-root'])
        self.assertTrue(item[1]['class'], ['bk-plotdiv'])
        os.remove("transit_trackers_ex.html")
		
        


if __name__ == '__main__':
    unittest.main()

