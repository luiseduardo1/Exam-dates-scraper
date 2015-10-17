#!/usr/bin/env python

from codecs import open
from os import path

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'Exams-dates-scraper',
    version = Exams-dates-scraper.__version__,
    description = 'A program to recuperate all your exams/homeworks dates 
                    from your Pixel/Laval university account',
    long_description = long_description,
    url = 'http://github.com/luiseduardo1/Exam-dates-scraper',
    author = 'Luis Eduardo Obando',
    author_email = 'luiseduardo.obando@gmail.com'
    license = 'MIT',
    packages = find_packages(),
    install_requires = ['Beautifulsoup4>=4.4.1',
                        'Mechanize==0.2.5'
                        ],
)
