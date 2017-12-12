import urllib.request
import zipfile
import os
import urllib3


def filename_gen(url):
    parsed_url = urllib3.util.parse_url(url)
    file_name = parsed_url.path.split('/')[-1]
    return file_name


def get_data(url):
    filename = filename_gen(url)
    # changing the dir to /data to download all the data in /data
    if os.path.exists(filename):
        print(filename, "is present locally")
        os.chdir('..')
        return 1
    else:
        try:
            # retrieving url
            urllib.request.urlretrieve(url, filename)
            # unzipping the psrc data
            zip_ref = zipfile.ZipFile(filename, 'r')
            zip_ref.extractall('../Data')
            zip_ref.close()
            print("Valid URL! Downloading and unzipping %s" % filename)
            # returning the dir up one level
            os.chdir('..')
            return 2
        except (ValueError, urllib.error.URLError, urllib.error.HTTPError):
            print("Invalid URL!")
            os.chdir('..')
            return 3


def remove_data(url):
    filename = filename_gen(url)
    # changing the dir to /data to remove all the data in /data
    os.chdir('./Data')
    if os.path.exists(filename):
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_archive_list = zip_ref.namelist()
        os.remove(zip_archive_list[0])
        os.remove(zip_archive_list[1])
        os.remove(zip_archive_list[2])
        os.remove(zip_archive_list[3])
        os.remove(filename)
        print("Removing %s and unzipped data files" % filename)
        os.chdir('..')
        return 4
    else:
        pass


# psrc_url = 'https://www.psrc.org/sites/default/files/2014-hhsurvey.zip'
#
#
# get_data(psrc_url)
# remove_data(psrc_url)
