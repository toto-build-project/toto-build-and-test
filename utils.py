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
  countStr() which returns the number of times a certain substring appears in 
  a string gen_json() which outputs a dictionary to a JSON file, get_hash() which 
  generates an MD5 checksum of the file corresponding to a given filename, 
  write_to_file writes a given string to he file corresponding to a given 
  filename.
"""

import canonicaljson as json
import hashlib

def count_string(s, substring):
  """
  <Purpose>
    Counts occurences of a substring in a string
  <Arguments>
    s:
      The string to be searched.

    substring:
      The substring that will be searched for in s

  <Exceptions>
    TBD.

  <Return>
    count:
      The number of times substring occured in s
  """
  s = s.lower()
  return s.count(substring)

def gen_json(metadata_dict, metadata_name):
  """
  <Purpose>
    Generates the a metadata file in JSON format corresponding to the given
    dictionary. We use pretty-printing to make it human-readable.

  <Arguments>
    metadata_dict:
      The dictionary to be written to a JSON file.

    metadata_name:
      The name to be used for the metadata file (e.g. "metadata"), which will be
      appended with ".json"

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  filename = metadata_name + '.json'
  fileobj = open(filename, 'w')
  fileobj.write(json.encode_pretty_printed_json(metadata_dict))
  fileobj.close()


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

  md5_hasher = hashlib.md5()

  # Read the file as bytes
  fileobj = open(filename,"rb")

  # We read the file in 128-byte chunks
  while True:
    data = fileobj.read(128)
    if not data:
      break
    md5_hasher.update(data)
  fileobj.close()
  return md5_hasher.hexdigest()

def write_to_file(string_to_write, filename):
  """
  <Purpose>
    Takes a given string and writes it to the file represented by the given
    filename.

  <Arguments>
    string_to_write:
      The string to be written.

    filename:
      The name of the file to which the string should be written.

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  fileobj = open(filename, "w")
  fileobj.write(string_to_write)
  fileobj.close()


def default_out_parser(metadata_dict, out_filename):
  """
  <Purpose>
    Reads through a specified output file, searches for related terms 
    corresponding to the categories of failure, warning and success, and records
    the lines and line numbers in which these terms appear.

  <Arguments>
    metadata_dict:
      The dictionary in which we are storing our metadata.

    filename:
      A string for the path to the outfile we are parsing.

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  # The wordlists used to check got success, failure and warnings
  success_words = ["success", "succeed"]
  failure_words = ["fail", "error", "fault"]
  warning_words = ["warn", "alert", "caution"]

  # Setup the dictionary with lists for success/failure/warning occurences
  metadata_dict["output_data"] = dict()
  metadata_dict["output_data"]["success"] = list()
  metadata_dict["output_data"]["failure"] = list()
  metadata_dict["output_data"]["warning"] = list()

  # Setup three variables to point to the lists for clarity 
  success_list = metadata_dict["output_data"]["success"]
  failure_list = metadata_dict["output_data"]["failure"]
  warning_list = metadata_dict["output_data"]["warning"]

  # Read through the file and add lines to the corresponding lists
  out_fileobj = open(out_filename, "r")
  line_num = 0
  for line in out_fileobj:
    line_num += 1
    dict_to_add = dict()
    dict_to_add["line"] = line
    dict_to_add["line_number"] = line_num
    if any(word in line for word in success_words):
      success_list.append(dict_to_add)
    else if any(word in line for word in failure_list):
      failure_list.append(dict_to_add)
    else if any(word in line for word in warning_list):
      warning_list.append(dict_to_add)

  out_fileobj.close()
