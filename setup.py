#!/usr/bin/env python

from codecs import open
from os import path

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

version = '1.0'

with open('README.md') as readme_file:
    readme = read_file.read()

requirements = [
        'Beautifulsoup4>=4.4.1',
        'Mechanize==0.2.5',
        ]

long_description = readme
setup(
    name = 'ExamsDatesScraper',
    version = version,
    description = 'A program to recuperate all your exams/homeworks dates 
                    from your Pixel/Laval university account',
    long_description = long_description,
    url = 'http://github.com/luiseduardo1/ExamsDatesScraper',
    author = 'Luis Eduardo Obando',
    author_email = 'luiseduardo.obando@gmail.com'
    license = 'MIT',
    packages = find_packages(),
    install_requires = requirements 
)
