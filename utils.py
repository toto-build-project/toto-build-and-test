"""
<Program Name>
  utils.py

<Author>
  Casey McGinley
  Fernando Maymi
  Catherine Eng
  Justin Valcarel
  Wilson Li

<Started>
  November 18, 2015

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Provides a library of utility functions to be used in main.py. These include:
  genJSON() which outputs a dictionary to a JSON file, get_hash() which generates
  an MD5 checksum of the file corresponding to a given filename, write_to_file 
  writes a given string to he file corresponding to a given filename.
"""

import canonicaljson as json
import hashlib

def genJSON(dict, name):
  """
  <Purpose>
    Generates the a metadata file in JSON format corresponding to the given
    dictionary. We use pretty-printing to make it human-readable.

  <Arguments>
    dict:
      The dictionary to be written to a JSON file.

    name:
      The name to be used for the metadata file (e.g. "metadata.json").

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  fname = name + '.json'
  f = open(fname, 'w')
  f.write(json.encode_pretty_printed_json(dict))
  f.close()

def get_hash(filename):
  """
  <Purpose>
    Returns an MD5 checksum of the file represented by the given filename.

  <Arguments>
    filename:
      The name of the file for which an MD5 checksum will be generated.

  <Exceptions>
    TBD.

  <Return>
    A 32-character string (a 128-bit hash value).
  """

  md5 = hashlib.md5()

  # Read the file as bytes
  f = open(filename,"rb")

  # We read the file in 128-byte chunks
  while True:
    d = f.read(128)
    if not d:
      break
    md5.update(d)
  f.close()
  return md5.hexdigest()

def write_to_file(s, filename):
  """
  <Purpose>
    Takes a given string and writes it to the file represented by the given
    filename.

  <Arguments>
    s:
      The string to be written.

    filename:
      The name of the file to which the string should be written.

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  f = open(filename, "w")
  f.write(s)
  f.close()
