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

  python main.py <command> <in> <details>

  Where:
    <command> -> the command to be executed for the build/test you want to 
      metadata about; should be encapsulated within quotes ("") if multiple
      words
    <in> -> optional; a filename for the file from which the stdin should come;
      if opting to not use this arg, provide the dash character (-) in this 
      space
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
  command = sys.argv[1]
  stdin = sys.argv[2]
  details = sys.argv[3]

  # Check if input file was explicitly specified
  set_stdin = True
  if stdin.strip() == '-':
    set_stdin = False

  # Setup the metadata dictionary
  metadata = dict()
  metadata['variables'] = dict()
  metadata['application'] = dict()

  # Execute the given command and fill the metadata dict
  process_env_vars(metadata)
  stdout, stderr = exec_cmd(command, set_stdin, stdin)
  process_app_data(metadata, command, set_stdin, stdin, stdout, stderr, details)

  # Generate the JSON
  utils.genJSON(metadata, "metadata")

def exec_cmd(command, set_stdin, stdin):
  """
  <Purpose>
    Execute the given command and redirect input (as necessary).

  <Arguments>
    command:
      The command provided to execute the build or test (e.g. "python test.py", 
      "make").

    set_stdin:
      A Boolean flag dictating whether or not stdin needs to be specified.

    stdin:
      The filename of the file from which stdin should be read; will be "-" in 
      the case of set_stdin = False.

  <Exceptions>
    TBD.

  <Return>
    A tuple of strings: (stdout, stderr).
  """

  if set_stdin:
    input_path = os.path.join(os.getcwd(),stdin)
    f = open(input_path,"r")
    proc = subprocess.Popen(command, stdin=f, stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE, shell=True)
    f.close()
  else:
    proc = ubprocess.Popen(command, stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE, shell=True)
  return proc.communicate()

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

def process_app_data(metadata, command, set_stdin, stdin, stdout, stderr, details):
  """
  <Purpose>
    Execute the given command and redirect input (as necessary).

  <Arguments>
    metadata:
      The metadata dictonary.

    command:
      The command that was provided to execute the build or test (e.g. "python 
      test.py", "make").

    set_stdin:
      A Boolean flag dictating whether or not stdin needs to be specified.

    stdin:
      The filename of the file from which stdin should be read; will be "-" in 
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

  metadata['application']['command'] = command

  cwd = os.getcwd()

  # For the stdin, stdout and stderr, write each to a file, hash it, and store 
  # the hash and filepath to the metadata
  if set_stdin:
    input_path = os.path.join(cwd,"in")
    shutil.copyfile(stdin,input_path)
    metadata['application']['input_hash'] = utils.get_hash(input_path)
    metadata['application']['input_path'] = input_path
  else:
    metadata['application']['input_hash'] = None
    metadata['application']['input_path'] = None

  output_path = os.path.join(cwd,"out")
  utils.write_to_file(stdout, output_path)
  metadata['application']['output_hash'] = utils.get_hash(output_path)
  metadata['application']['output_path'] = output_path
  err_path = os.path.join(cwd,"err")
  utils.write_to_file(stderr, err_path)
  metadata['application']['err_hash'] = utils.get_hash(err_path)
  metadata['application']['err_path'] = err_path

  metadata['application']['details'] = details

main()
