import unittest
import utils
from urllib import request
import os

GOOD_URL = 'https://www.psrc.org/sites/default/files/2014-hhsurvey.zip'
BAD_URL = 'http://sobad/junkurl.html'
FILENAME = '2014-hhsurvey.zip'

class UtilsTest(unittest.TestCase):

    def test_bad_url(self):
        with self.assertRaises(ValueError):
            utils.get_data(BAD_URL)

    def test_good_url(self):
        utils.get_data(GOOD_URL)
        self.assertTrue(os.path.isfile(FILENAME))
        os.remove(FILENAME)

    def test_when_file_exists(self):
        open(FILENAME, 'w')
        utils.get_data(GOOD_URL)
        self.assertTrue(os.path.getsize(FILENAME) == 0)
        os.remove(FILENAME)

    def test_extract(self):
        path = '../Data/2014-pr3-hhsurvey-households.xlsx'
        self.assertTrue(os.path.isfile(path))


if __name__ == '__main__':
    unittest.main()
