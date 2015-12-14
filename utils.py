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

import canonicaljson
import json
import hashlib
import os.path
import time
import tuf

METADATA_PATH_WORD = "_path"
METADATA_CUMULATIVE_WORD = "cumulative_metadata_hash"


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
  fileobj.write(canonicaljson.encode_pretty_printed_json(metadata_dict))
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

  sha256_hasher = hashlib.sha256()

  # Read the file as bytes
  fileobj = open(filename,"rb")

  # We read the file in 128-byte chunks
  while True:
    data = fileobj.read(128)
    if not data:
      break
    sha256_hasher.update(data)
  fileobj.close()
  return sha256_hasher.hexdigest()


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


def file_line_counter(filename):
  """
  <Purpose>
    Takes a filename and counts the number of lines in the file.

  <Arguments>
    filename:
      The name of the file to line count.

  <Exceptions>
    TBD.

  <Return>
    A number representing lines found in the file.  If no
    lines were found, then return 0.  
  """
  
  count = 0
  with open(filename) as f:
    for count, line in enumerate(f):
      count = count + 1
  f.close()
  return count


def get_file_modification_time(filename):
  """
  <Purpose>
    Takes a filename and find the last modification time
    of this file.

  <Arguments>
    filename:
      The name of the file to find last modification time on. 

  <Exceptions>
    TBD.

  <Return>
    The modification time is returned (secs from epoch).  
    The time is formatted as: "1448502239.82".
  """

  mtime = os.path.getmtime(filename)
  return mtime


def word_found_in_file(filename, word):
  """
  <Purpose>
    Helps to check if a keyword is found in a file. 

  <Arguments>
    filename:
      The name of the file for the keyword check. 
    word:
      The keyword that will be used to search in the file.

  <Exceptions>
    TBD.

  <Return>
    True is returned when the word is available, otherwise
    a False is returned.
  """

  with open(filename) as f:
    for line in f:
      if (word in line):
        f.close()
        return True
  f.close()
  return False


def verify_metadatafiles(mainmeta_filepath):
  """
  <Purpose>
    This function verifies the metadatafiles are correct. 
    It will read the main_metadata file and parse 
    through for the sub metadata files <name>_metadata.json.
    The <name>_metadata.json files are hashed through
    and the cumulative hash is compared to the one 
    stored in main_metadata.  
    
    TBA:  Additional fields may be added in the future, 
    this function to be updated with those changes.

  <Arguments>
    mainmeta_filepath:
      The filepath of the main_metadata.json file.

  <Exceptions>
    IOError:  
      Raised when the main_metadata.json is not available.

  <Return>
    True is returned when the hash is valid, otherwise 
    a False is returned.
  """

  mainmeta_data = tuf.util.load_json_file(mainmeta_filepath)
  cumulative_mainfile_hash = ""
  sha256_hasher = hashlib.sha256()

  for key, value in mainmeta_data.iteritems():
    # Found_path checks the end of the key to see if keyword
    # exists.  If it does, we want to pull the path's value
    # to retrieve the file for hashing.
    found_path = key[-(len(METADATA_PATH_WORD)):]  == METADATA_PATH_WORD

    if (key == METADATA_CUMULATIVE_WORD):
      cumulative_mainfile_hash = value;
    if (found_path):
      submetadata_filepath = value
      hash_submetadata = utils.get_hash(submetadata_filepath)
      sha256_hasher.update(hash_submetadata)

  # After iterating through for all file hashes
  cumulative_read_hashes = sha256_hasher.hexdigest()

  return (cumulative_read_hashes == cumulative_mainfile_hash)

