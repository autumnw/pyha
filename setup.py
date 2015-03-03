from setuptools import setup, find_packages
import sys, os

version = '1.0.0'

setup(name='pyha',
      version=version,
      description="Python based HA cluster",
      long_description="""\
Python based HA cluster""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='HA',
      author='Autumn Wang',
      author_email='shoujinwang@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'requests'
      ],
      data_files=[('/etc/pyha', ['conf/pyha.json.example', 'conf/logging.json']),
                  ('/etc/init.d', ['etc/init.d/pyha'])],
      scripts=['bin/pyha'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
