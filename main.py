"""
<Program Name>
  main.py

<Author>
  Casey McGinley
  Fernando Maymi
  Catherine Eng
  Justin Valcarel
  Wilson Li

<Started>
  November 10, 2015

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  To generate metadata files of the relevant info from the build and test 
  development phases. This script represents the backbone of this application. 
  This script is called as below:

  python main.py <cmd_string> <input_filepath> <details>

  Where:
    <cmd_string> -> the command to be executed for the build/test you want to 
      metadata about; should be encapsulated within quotes ("") if multiple
      words
    <input_filepath> -> optional; a filepath for the file from which the stdin 
      should come; if opting to not use this arg, provide the dash character (-)
      in this space
    <details> -> any extra details the developer may wish to provide to be 
      included in the metadata file (e.g. software version; developer's not to 
      the user, etc); should be encapsulated within quotes ("") if multiple
      words
"""

import subprocess
import os
import datetime
import sys
import getpass
import utils
import shutil
import signing

def main():
  """
  <Purpose>
    Straightforward function to encapsulate the program's core logic. Called
    at the end of this file.

  <Arguments>
    None.

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  # Grab the command line arguments
  cmd_string = sys.argv[1]
  input_filepath = sys.argv[2]
  details = sys.argv[3]

  # Check if input file was explicitly specified
  set_stdin = True
  if input_filepath.strip() == '-':
    set_stdin = False

  # Setup the metadata dictionary
  metadata = dict()
  metadata['variables'] = dict()
  metadata['application'] = dict()

  # Execute the given command and fill the metadata dict
  process_env_vars(metadata)
  stdout, stderr = exec_cmd(cmd_string, set_stdin, input_filepath)
  process_app_data(metadata, cmd_string, set_stdin, input_filepath, stdout, stderr, details)
  default_out_parser(metadata, "out")

  # Generate the signed JSON
  signed_metadata = signing.sign_json(metadata)
  utils.gen_json(signed_metadata, "metadata")

def exec_cmd(cmd_string, set_stdin, input_filepath):
  """
  <Purpose>
    Execute the given command and redirect input (as necessary).

  <Arguments>
    cmd_string:
      A string of the command provided to execute the build or test (e.g. 
      "python test.py", "make").

    set_stdin:
      A Boolean flag dictating whether or not stdin needs to be specified.

    input_filepath:
      The filepath of the file from which stdin should be read; will be "-" in 
      the case of set_stdin = False.

  <Exceptions>
    TBD.

  <Return>
    A tuple of strings: (stdout, stderr).
  """

  if set_stdin:
    input_fileobj = open(input_filepath,"r")
    cmd_process = subprocess.Popen(cmd_string, stdin=input_fileobj, stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE, shell=True)
    input_fileobj.close()
  else:
    cmd_process = subprocess.Popen(cmd_string, stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE, shell=True)
  return cmd_process.communicate()

def process_env_vars(metadata):
  """
  <Purpose>
    Add environment/system data to the metadata dictionary.

  <Arguments>
    metadata:
      The metadata dictonary.

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  # Returns a tuple containing various system data, including: cpu architecture, 
  # kernel name, kernel verison, etc.
  uname = os.uname()

  metadata['variables']['os'] = dict()
  metadata['variables']['os']['kernel'] = uname[0]
  metadata['variables']['os']['release'] = uname[2]
  metadata['variables']['os']['version'] = uname[3]
  metadata['variables']['hostname'] = uname[1]
  metadata['variables']['cpu_arch'] = uname[4]
  metadata['variables']['timestamp'] = str(datetime.datetime.utcnow())

  # We use the getpass module here for Unix and Windows compatibility 
  metadata['variables']['user'] = getpass.getuser()
  metadata['variables']['curr_working_dir'] = os.getcwd()

def process_app_data(metadata, cmd_string, set_stdin, input_filepath, stdout, stderr, details):
  """
  <Purpose>
    Execute the given command and redirect input (as necessary).

  <Arguments>
    metadata:
      The metadata dictonary.

    cmd_string:
      A string of the command that was provided to execute the build or test 
      (e.g. "python test.py", "make").

    set_stdin:
      A Boolean flag dictating whether or not stdin needs to be specified.

    input_filepath:
      The filepath of the file from which stdin should be read; will be "-" in 
      the case of set_stdin = False.

    stdout:
      A string representing the stdout from the command that was run.

    stderr:
      A string representing the stderr from the command that was run.

    details:
      A string representing the miscellaneous details provided by the developer.

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  metadata['application']['command'] = cmd_string

  cwd = os.getcwd()

  # For the stdin, stdout and stderr, write each to a file, hash it, and store 
  # the hash and filepath to the metadata
  if set_stdin:
    saved_input_path = os.path.join(cwd,"in")
    shutil.copyfile(input_filepath, saved_input_path)
    metadata['application']['input_hash'] = utils.get_hash(saved_input_path)
    metadata['application']['input_path'] = saved_input_path
  else:
    metadata['application']['input_hash'] = None
    metadata['application']['input_path'] = None

  saved_output_path = os.path.join(cwd,"out")
  utils.write_to_file(stdout, saved_output_path)
  metadata['application']['output_hash'] = utils.get_hash(saved_output_path)
  metadata['application']['output_path'] = saved_output_path
  saved_err_path = os.path.join(cwd,"err")
  utils.write_to_file(stderr, saved_err_path)
  metadata['application']['err_hash'] = utils.get_hash(saved_err_path)
  metadata['application']['err_path'] = saved_err_path

  metadata['application']['details'] = details


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
  metadata_dict["output_data"]["success"] = dict()
  metadata_dict["output_data"]["failure"] = dict()
  metadata_dict["output_data"]["warning"] = dict()
  metadata_dict["output_data"]["success"]["instances"] = list()
  metadata_dict["output_data"]["failure"]["instances"] = list()
  metadata_dict["output_data"]["warning"]["instances"] = list()

  # Setup three variables to point to the lists and for clarity 
  success_list = metadata_dict["output_data"]["success"]["instances"]
  failure_list = metadata_dict["output_data"]["failure"]["instances"]
  warning_list = metadata_dict["output_data"]["warning"]["instances"]

  # Read through the file and add lines to the corresponding lists
  out_fileobj = open(out_filename, "r")
  line_num = 0
  success_count = 0
  failure_count = 0
  warning_count = 0
  for line in out_fileobj:
    line_num += 1
    line_lower = line.lower()
    dict_to_add = dict()
    dict_to_add["line"] = line
    dict_to_add["line_number"] = line_num
    if any(word in line_lower for word in success_words):
      success_list.append(dict_to_add)
      success_count += 1
    elif any(word in line_lower for word in failure_words):
      failure_list.append(dict_to_add)
      failure_count += 1
    elif any(word in line_lower for word in warning_words):
      warning_list.append(dict_to_add)
      warning_count += 1

  # Add the counts to the dictionary
  metadata_dict["output_data"]["success"]["count"] = success_count
  metadata_dict["output_data"]["failure"]["count"] = failure_count
  metadata_dict["output_data"]["warning"]["count"] = warning_count

  out_fileobj.close()


main()
