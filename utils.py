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
import tarfile
import time
import sys
import tuf

METADATA_WORD = "metadata"
METADATA_OUTPUT_TAR_WORD = "output_tar"
METADATA_INPUT_TAR_WORD = "input"

METADATA_CUMULATIVE_WORD = "cumulative_metadata_hash"
METADATA_APPLICATION_WORD = "application"
METADATA_SEQUENCE_KEY = "sequence_"
METADATA_CUMULATIVE_FILE_ELEMS = [METADATA_WORD, METADATA_OUTPUT_TAR_WORD, METADATA_INPUT_TAR_WORD]


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
  try:
    fileobj = open(filename,"rb")

    # We read the file in 128-byte chunks
    while True:
      data = fileobj.read(128)
      if not data:
        break
      sha256_hasher.update(data)
    fileobj.close()
  except IOError: 
    write_message("err", "Cannot open file for hash " + filename + ".")
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

  elems_to_accumulate_hash = METADATA_CUMULATIVE_FILE_ELEMS
  mainmeta_data = tuf.util.load_json_file(mainmeta_filepath)
  cmd_data = mainmeta_data[METADATA_APPLICATION_WORD]

  # Initialize the SHA elements we will create cumulative hashes for.
  sha256_hasher = dict()
  for file_desc in elems_to_accumulate_hash:
    sha256_hasher[file_desc] = hashlib.sha256()
 
  counter = 0
  for cmd_key, cmd_value in cmd_data.iteritems():
    # Skip non sequence entries in the application dictionary.
    if (not cmd_key or not cmd_key.startswith(METADATA_SEQUENCE_KEY)):
      break

    # Process the current policy sequence.  
    seq_key = METADATA_SEQUENCE_KEY + str(counter)
    prev_seq_key = METADATA_SEQUENCE_KEY + str(counter-1)
    for file_desc in elems_to_accumulate_hash:
      hash_val = None
      filename = cmd_data[seq_key][file_desc + "_path"] 
      if (filename):
        hash_val = get_hash(filename)
        sha256_hasher[file_desc].update(hash_val)
      """
      if (filename):
        print "CCCCf file=", filename + ", hash=", hash_val
      """

    # Test1: Validate the previous sequence, so if we see that the 
    # main_metadata file has the prev_output_used_and_hashes_valid
    # flag then open the current input file and compare to 
    # previous sequence's output file. 

    """
    # CE - use this to spoof an error 
    if (cmd_data[seq_key]["cmd_name"] == "build_snap_execute"):
     cmd_data[prev_seq_key]["output_tar_path"] = "spoof_error"
    """

    if (counter > 0 and "prev_output_used_and_hashes_valid" in cmd_data[seq_key]):
      hash_input = get_hash(cmd_data[seq_key]["input_path"])
      hash_output = get_hash(cmd_data[prev_seq_key]["output_tar_path"])
      if (hash_input != hash_output):
        write_message("err", "Error: The previous output does not match input tar seq" + str(counter) + ".")
        return False

    counter = counter + 1

  # Test2: Compare the file element's cumulative_hash and read_hashes.
  for file_desc in elems_to_accumulate_hash:
    main_cumulative_hash = mainmeta_data["cumulative_" + file_desc + "_hash"]
    if (main_cumulative_hash != sha256_hasher[file_desc].hexdigest()):
      write_message("err", "Error: The previous output does not match input tar seq" + str(counter) + ".")
      return False

  return True



def untar_file(path, filename):
  try: 
    if (filename and filename.endswith("tar")):
      tar = tarfile.open(filename, mode="r")
      tar.extractall(path)
      tar.close()
      ret_code = 1
  except IOError:
     write_message("err", "Tar file is not found for [" + os.path.join(path, filename) + "].")


def tar_file(source_filepath, output_prefilename, arc_name):
  if (not (source_filepath and output_prefilename and arc_name)):
    return
  try:
    with tarfile.open(output_prefilename + ".tar", "w") as tar:
      tar.add(source_filepath, arcname=arc_name)
  except OSError:
     write_message("err", "The target filename is [" + output_prefilename)
     write_message("err", "]  --> for [" + source_filepath + "].")


def write_message(message_type, message):
  return
  if (message_type == "err"):
    print "ERROR: ", message
