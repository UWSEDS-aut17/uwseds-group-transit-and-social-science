import unittest
import utils
from urllib import request
import os

psrc_url = 'https://www.psrc.org/sites/default/files/2014-hhsurvey.zip'
psrc_wrong_url = 'https://www.psrc.org/sites/default/filed/2014-ppsurvey.zip'


class Data_test(unittest.TestCase):

    def test_get_data(self):

        # (a) file is present locally
        # Condition: Assumption that the zip file exists
        # test(a)
        os.chdir('./Data')
        request.urlretrieve(psrc_url, utils.filename_gen(psrc_url))
        os.chdir('..')
        print("\nTest(a): Testing if the file is present locally\n")
        self.assertEqual(utils.get_data(psrc_url), 1)
        print("Test(a) Success")
        print("----------------------------------------------------------")

        # (b) Checks if the URL is valid and downloads/unzips the data
        # Condition: Assumption that the file does not exist
        # test(b) part 1
        os.chdir('./Data')
        os.remove(utils.filename_gen(psrc_url))
        os.chdir('..')
        print("\nTest(b) Part 1: Testing if the URL is valid. If so, download "
              "and unzip the data from the URL")
        self.assertEqual(utils.get_data(psrc_url), 2)
        print("Test(b) Part 1 Success")
        print("----------------------------------------------------------")

        # (b) Checks if the URL is invalid
        # Condition: Assumption that the file does not exist
        # test(b) part 2
        utils.remove_data(psrc_url)
        print("\nTest(b) Part 2: Testing if the URL is invalid")
        self.assertEqual(utils.get_data(psrc_wrong_url), 3)
        print("Test(b) Part 2 Success")
        print("----------------------------------------------------------")

    def test_remove_data(self):
        # (c) test for remove_data
        # Condition: Assumption that all files are existing to be removed
        # test(c)
        utils.get_data(psrc_url)
        print("\nTest(c): Testing if all the data are removed from the "
              "directory")
        self.assertEqual(utils.remove_data(psrc_url), 4)
        print("Test(c) Success")


if __name__ == '__main__':
    unittest.main()
