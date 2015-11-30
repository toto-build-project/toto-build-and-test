"""
<Program Name>
  setup.py

<Author>
  Casey McGinley
  Fernando Maymi
  Catherine Eng
  Justin Valcarel
  Wilson Li

<Started>
  November 29, 2015

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  This is the setup script to make sure all proper utilities and modules are available to the main program.
"""

from setuptools import setup
from setuptools import find_packages

setup(
  name = 'toto-build-and-test',
  version = '0.1',
  description = 'A testing verification framework',
  author = [
    'Casey McGinley',
    'Fernando Maymi',
    'Catherine Eng',
    'Justin Valcarcel',
    'Wilson Li'
  ],
  author_email = [
    'cmm771@nyu.edu, '
    'fernando.maymi@nyu.edu, '
    'ce2086@nyu.edu, '
    'jpv259@nyu.edu, '
    'wl868@nyu.edu'
  ],
  url = 'https://github.com/toto-build-project',
  py_modules = ['signing', 'test_sign', 'test_signing', 'utils'],
  packages = find_packages(exclude=['tests',
                                    'excludes/c_code_proj'])
)
