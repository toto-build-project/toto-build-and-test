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

with open('README.md') as file_object:
  long_description = file_object.read()

setup(
  name = 'toto-build-and-test',
  version = '0.1.0',
  description = 'A testing verification framework',
  long_description = long_description,
  url = 'https://github.com/toto-build-project',
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
  license = '',
  classifiers =[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Topic :: Software Development :: Testing',
    'Programming Lanugae :: Python :: 2',
    'Programming Language :: Python :: 2.7'
  ],
  keywords='testing verification framework',
  packages = find_packages(exclude=['tests', 'excludes/c_code_proj']),
  install_requires=[
    'tuf',
    'hashlib',
    'pycrypto',
    'canonicaljson'
    'iso8601',
    'six',
    'pycrypto==2.6.1',
    'pynacl==0.2.3',
    'cryptography==1.0'
  ]
  )
