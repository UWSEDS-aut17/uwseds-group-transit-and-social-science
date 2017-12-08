import sys
try:
    from setuptools import setup
except:
    from distutils.core import setup


opts = dict(name='uwseds-group-transit-and-social-science',
            description='A python package to analyze transit trends in Seattle',
            url='https://github.com/UWSEDS-aut17/uwseds-group-transit-and-social-science',
            version='1.0',
            packages=['uwseds-group-transit-and-social-science'],
            install_requires=['numpy',
                              'pandas',
                              'geopandas',
                              'bokeh',
                              ]
            )


if __name__ == '__main__':
    setup(**opts)
