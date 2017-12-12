import sys
try:
    from setuptools import setup
except:
    from distutils.core import setup


opts = dict(name='uwseds-transit-trackers',
            description='A python package to analyze transit trends in Seattle',
            url='https://github.com/UWSEDS-aut17/uwseds-group-transit-trackers',
            version='1.0',
            packages=['uwseds-transit-trackers'],
            install_requires=['numpy',
                              'pandas',
                              'geopandas',
                              'bokeh',
                              'math',
                              'pysal',
                              'os'
                              ]
            )


if __name__ == '__main__':
    setup(**opts)
