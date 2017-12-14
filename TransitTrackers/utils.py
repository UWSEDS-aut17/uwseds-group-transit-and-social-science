import urllib.request
import zipfile
import os
import urllib3


def filename_gen(url):
    """This function generates a unique file name from the download urllib
    inputs: url
    returns: unique file name
    """
    parsed_url = urllib3.util.parse_url(url)
    file_name = parsed_url.path.split('/')[-1]
    return file_name


def get_data(url):
    """This function downloads and unzips the data from a specific urllib
    inputs: url
    returns: extracted zip file in our Data/ directory
    This will raise a ValueError if the url provided is incorrect
    """
    filename = filename_gen(url)
    # changing the dir to /data to download all the data in /data
    if os.path.exists(filename):
        print(filename, "is present locally")
    else:
        try:
            urllib.request.urlretrieve(url, filename)
            zip_ref = zipfile.ZipFile('2014-hhsurvey.zip', 'r')
            zip_ref.extractall('../Data')
            zip_ref.close()
            print("Valid URL! Downloading and unzipping %s" % filename)
        except (ValueError, urllib.error.URLError, urllib.error.HTTPError):
            raise ValueError
