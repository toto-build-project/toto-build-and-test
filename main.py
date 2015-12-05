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

  python main.py <cmd_string> <input_filepath>

  Where:
    <cmd_string> -> the command to be executed for the build/test you want to 
      metadata about; should be encapsulated within quotes ("") if multiple
      words
    <input_filepath> -> optional; a filepath for the file from which the stdin 
      should come; if opting to not use this arg, provide the dash character (-)
      in this space
"""

import subprocess
import os
import datetime
import sys
import getpass
import utils
import shutil
import signing
import argparse

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

  # Setup the command line parser
  args = get_command_line_args()

  # Grab the command line arguments
  cmd_string = args.command
  input_filepath = args.input
  policy_filepath = args.policy

  # Setup the metadata dictionary
  metadata = dict()
  metadata['variables'] = dict()
  metadata['application'] = dict()

  # Execute the given command and fill the metadata dict
  process_env_vars(metadata)
  stdout, stderr = exec_cmd(cmd_string, input_filepath)
  process_app_data(metadata, cmd_string, input_filepath, stdout, stderr)
  default_parser(metadata, "out", "output_data")
  default_parser(metadata, "err", "err_data")

  # Generate the signed JSON
  signed_metadata = signing.sign_json(metadata)
  utils.gen_json(signed_metadata, "metadata")


def exec_cmd(cmd_string, input_filepath):
  """
  <Purpose>
    Execute the given command and redirect input (as necessary).

  <Arguments>
    cmd_string:
      A string of the command provided to execute the build or test (e.g. 
      "python test.py", "make").

    input_filepath:
      The filepath of the file from which stdin should be read; will be None if 
      no explicit file specified

  <Exceptions>
    TBD.

  <Return>
    A tuple of strings: (stdout, stderr).
  """

  if input_filepath:
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


def process_app_data(metadata, cmd_string, input_filepath, stdout, stderr):
  """
  <Purpose>
    Execute the given command and redirect input (as necessary).

  <Arguments>
    metadata:
      The metadata dictonary.

    cmd_string:
      A string of the command that was provided to execute the build or test 
      (e.g. "python test.py", "make").

    input_filepath:
      The filepath of the file from which stdin should be read; will be None if 
      no explicit file specified

    stdout:
      A string representing the stdout from the command that was run.

    stderr:
      A string representing the stderr from the command that was run.

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  metadata['application']['command'] = cmd_string

  cwd = os.getcwd()

  # For the stdin, stdout and stderr, write each to a file, hash it, and store 
  # the hash and filepath to the metadata
  if input_filepath:
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


def default_parser(metadata_dict, filename, metadata_category):
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

    metadata_category:
      A string for the upper level key to be used to store this data.

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  # The wordlists used to check got success, failure and warnings
  success_words = ["success", "succeed", "installed", "finished"]
  failure_words = ["fail", "error"]
  warning_words = ["warn", "alert", "caution"]

  # Setup the dictionary with lists for success/failure/warning occurences
  metadata_dict[metadata_category] = dict()
  metadata_dict[metadata_category]["success"] = dict()
  metadata_dict[metadata_category]["failure"] = dict()
  metadata_dict[metadata_category]["warning"] = dict()
  metadata_dict[metadata_category]["success"]["instances"] = list()
  metadata_dict[metadata_category]["failure"]["instances"] = list()
  metadata_dict[metadata_category]["warning"]["instances"] = list()

  # Setup three variables to point to the lists and for clarity 
  success_list = metadata_dict[metadata_category]["success"]["instances"]
  failure_list = metadata_dict[metadata_category]["failure"]["instances"]
  warning_list = metadata_dict[metadata_category]["warning"]["instances"]

  # Read through the file and add lines to the corresponding lists
  fileobj = open(filename, "r")
  line_num = 0
  success_count = 0
  failure_count = 0
  warning_count = 0
  for line in fileobj:
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
  metadata_dict[metadata_category]["success"]["count"] = success_count
  metadata_dict[metadata_category]["failure"]["count"] = failure_count
  metadata_dict[metadata_category]["warning"]["count"] = warning_count

  fileobj.close()


def get_command_line_args():
  """
  <Purpose>
    Uses the argparse module to parse, process and return the command line 
    arguments.

  <Arguments>
    None.

  <Exceptions>
    TBD.

  <Return>
    An object representing the command line arguments.
  """
  parser = argparse.ArgumentParser(prog='main.py', description='Captures the given build/test command\'s I/O and relevant system details.')
  parser.add_argument('--version', action='version', version='Toto Build/Test Metadata Generator 0.4')
  parser.add_argument('--input', metavar='FILEPATH', help='the path to the desired input file to be routed through stdin')
  parser.add_argument('--policy', metavar='FILENAME', help='the path to the desired file specifying build/test policy')
  parser.add_argument('command', metavar='COMMAND', type=str, help='the bash command to execute the build or test')

  return parser.parse_args()


main()
