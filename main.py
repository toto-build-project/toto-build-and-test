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

  usage: main.py [-h] [--version] [--input FILEPATH] [--output FILENAME] [--policy FILENAME] [--command_policy FILENAME or --command <arg>] 

  Captures the given build/test command's I/O and relevant system details.

  positional arguments:
    --command_policy or --command must be specified.
  
  optional arguments:
    -h, --help         show this help message and exit
    --version          show program's version number and exit
    --input FILEPATH   the path to the desired input file to be routed through
    --output FILEPATH  the path to the desired output file to be generated
    --policy FILENAME  the path to the desired file specifying build/test policy
    --command_policy   FILENAME  the path to the desired file specifying command policy
    --command          the bash command to execute the build or test
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
import re
import tuf
import hashlib
import json

TOTO_TOOL_VERSION = "Toto Build/Test Metadata Generator 0.4"
DEFAULT_POLICY_FILENAME = "default_policy.json"
DEFAULT_CUR_DIR = os.getcwd()
DEFAULT_WORK_DIR = os.path.join(DEFAULT_CUR_DIR, "work")
DEFAULT_SOURCE_INPUT_DIR = os.path.join(DEFAULT_WORK_DIR, "source_input")
DEFAULT_CMD_TO_SOURCE_INPUT_DIR_BEGIN = "cd "
DEFAULT_CMD_TO_SOURCE_INPUT_DIR_END = " && "
DEFAULT_ELEMS_TO_ACCUMULATE_HASH = ["metadata", "output_tar"]

def main():
  # Setup the command line parser
  args = get_command_line_args()

  # Read the commands and begin execution
  read_command_policy(args)


def read_command_policy(args):
  """
  <Purpose>
    This function reads and sets up the commands that will be executed.
    Commands are either passed in:  1) via the command_policy file option
    or 2) a single command in the COMMAND option.  The command_policy 
    option will be more robust (ex: allows users to set the cmd_name, 
    set a verify_command) while the single command omits these options.
    Since the single command option does not allow a cmd_name to be 
    specified, the output files for this option are prepended with
    "generic" (ex: generic_metadata.json).
 
    This function will create a list of executing commands and their 
    attributes (cmd_name, verify_command, input_file, output_file), validate 
    attributes, execute the command.  Take the hash value from the 
    metatdata and create a cumulative hash.  These values are then 
    stored into a main_metadata.json file.
   
    Note:  function asserts that cmd_name must be filled out 
    for the command_policy option and if an input file is 
    specified then it must exist else the program will exit.  

  <Arguments>
    args:
      The arguments that are passed from the command line.

  <Exceptions>
    IOError: 
      1) Returned if the cmd_name is not specified correctly.
      2) Returned if the input file does not exist.

  <Returns>
    None.
  """

  commands = []
  # Setup the command policy here.  The user can either pass
  # a file in from the commandline (command_policy option), 
  # otherwise pass a single command line entry.
  if args.command_policy:
    # Begin processing the commands from the command policy. 
    command_policy_filepath = args.command_policy
    commandList = tuf.util.load_json_file(command_policy_filepath)
    commands = commandList["commands"]
  else:
    # The command is read from the commandline (COMMAND var).
    # We will autoname the file generic_metadata.json. 
    tmp_commands = [[args.command, None, "generic", args.input]]
    commands = json.dumps(tmp_commands)
    commands = tuf.util.load_json_string(commands)


  # Setup for the main_metadata file fields.
  metadata_files_processed = dict()
  metadata_files_processed["application"] = dict()
  # Setup for policy sequence field details.
  metadata_filepath = ""
  output_tar_filepath = ""
  cmd_counter = 0
  add_hash_data = dict()
  list_all_cmds = list()

  # Begin to iterate through the commands.  First verify 
  # the command setup is valid, next process the actual command.
  for cmd_elem in commands:
    cmd_name = cmd_elem[2]

    # Check if the cmd_name is empty or is 'main'.  We need to use
    # the cmd_name field when naming our metadata files so 
    # make sure they are set here.
    assert (cmd_name), "Error: The cmd_name cannot be null."
    assert (cmd_name != "main"), "Error: The cmd_name cannot equal 'main'."

    # Validate the input file exists else flag an error.
    ##assert (cmd_elem[3] and os.path.exists(cmd_elem[3])), "Error:  The input file " + cmd_elem[3] + " specified does not exist."
    """  CCCCCCCCCCCCCCC
      if (cmd_elem[3]):
        try:
          os.path.exists(cmd_elem[3])
        except IOError:
          print "Error:  The input file was specified, however it does not exist."
    """


    # Process the commands and create the metadata files here.
    metadata_filepath, output_tar_filepath = process_command(cmd_elem, args.policy, output_tar_filepath)

    """
    # Capture the command output to add to main_metadata.
    metadata_files_processed["application"][cmd_name] = dict()
    add_hash_data[cmd_name] = dict()
    add_hash_data[cmd_name]["metadata"] = metadata_filepath
    add_hash_data[cmd_name]["output_tar"] = output_tar_filepath
    add_hash_data[cmd_name]["sequence"] = cmd_counter
    cmd_counter = cmd_counter + 1
    list_all_cmds.append(add_hash_data)
    """

    # Capture the command output to add to main_metadata.
    add_hash_data[cmd_counter] = dict()
    add_hash_data[cmd_counter]["cmd_name"] = cmd_name
    add_hash_data[cmd_counter]["metadata"] = metadata_filepath
    add_hash_data[cmd_counter]["output_tar"] = output_tar_filepath
    add_hash_data[cmd_counter]["sequence"] = cmd_counter
    cmd_counter = cmd_counter + 1
    list_all_cmds.append(add_hash_data)

  # Add the output to the main_metadata dictionary.
  add_main_hash_details_for_policy_seq(add_hash_data, metadata_files_processed, DEFAULT_ELEMS_TO_ACCUMULATE_HASH, list_all_cmds)
  metadata_files_processed["timestamp"] = str(datetime.datetime.utcnow())
    
  # Sign the data and write to main_metadata.json.
  signed_metadata = signing.sign_json(metadata_files_processed)
  main_metadata_path = os.path.join(DEFAULT_WORK_DIR, "main_metadata")
  utils.gen_json(signed_metadata, main_metadata_path)



def add_main_hash_details_for_policy_seq(cmd_data, metadata_files_processed, elems_to_accumulate_hash, list_all_cmds):

  ## CCCCC 
  curcount = 0
  alt_seq_hashsum = dict()
  sha256_alt = hashlib.sha256()

  # Initialize the SHA elements we will create cumulative hashes for.
  sha256_hasher = dict()
  for file_desc in elems_to_accumulate_hash:
    sha256_hasher[file_desc] = hashlib.sha256()

  for counter in xrange(0, len(cmd_data)):
    seq_key = "sequence_" + str(counter)
    metadata_files_processed["application"][seq_key] = dict()
    metadata_files_processed["application"][seq_key]["cmd_name"]  = cmd_data[counter]["cmd_name"]

    for file_desc in elems_to_accumulate_hash:
      filename = cmd_data[counter][file_desc]
      hash_val = utils.get_hash(filename)
      metadata_files_processed["application"][seq_key][file_desc + "_hash"] = hash_val
      metadata_files_processed["application"][seq_key][file_desc + "_path"] = filename
      sha256_hasher[file_desc].update(hash_val)
    
  for file_desc in elems_to_accumulate_hash:
    metadata_files_processed["cumulative_" + file_desc + "_hash"] = sha256_hasher[file_desc].hexdigest()

  return



  """
    curhash = alt_seq_hashsum[counter]["metadata"]
    sha256_alt.update(curhash)
    print "\n\n cur[", counter, "] hash=", curhash, "\n curhash=", sha256_alt.hexdigest()


  # Iterate through each command and process the cmd_data field. 
  for cmd_name, desclist in cmd_data.iteritems():
    # Add specific command information to main_metadata.
    for desc, desc_val in desclist.iteritems():  
      # Adding a sequence number.
      if (desc in ["sequence"]):
        metadata_files_processed["application"][cmd_name][desc] = desc_val
      else:
        # Process the hash and filepath details.
        hash_val = utils.get_hash(desc_val)
        metadata_files_processed["application"][cmd_name][desc + "_hash"] = hash_val
        metadata_files_processed["application"][cmd_name][desc + "_path"] = desc_val 
        # Accumulate the hash for this file type.
        sha256_hasher[desc].update(hash_val)

        if (desc == "metadata"):
          print "CCCCC", metadata_files_processed["application"][cmd_name]["sequence"], "--- hash[", cmd_name, "][", desc, "]=", hash_val, "\n--hashcur=", sha256_hasher[desc].hexdigest()
          curcount = curcount + 1


    seq_num = metadata_files_processed["application"][cmd_name]["sequence"]
    ### CCCCC altaccum test 
    alt_seq_hashsum[seq_num] = dict()
    alt_seq_hashsum[seq_num]["metadata"] = metadata_files_processed["application"][cmd_name]["metadata_hash"]
    ##print "THE METADATA =================",  metadata_files_processed["application"][cmd_name]


  ##  CCCCCCC
  for counter in xrange(0, len(alt_seq_hashsum)):  
    curhash = alt_seq_hashsum[counter]["metadata"]
    sha256_alt.update(curhash)
    print "\n\n cur[", counter, "] hash=", curhash, "\n curhash=", sha256_alt.hexdigest()

  # Create the final hex value for the hash and assign to main_metadata.
  for desc in elems_to_accumulate_hash:
    metadata_files_processed["cumulative_" + desc + "_hash"] = sha256_hasher[desc].hexdigest()
    if (desc == "metadata"):
       print "CCCCC finalhash=", metadata_files_processed["cumulative_" + desc + "_hash"]
  """



def add_main_hash_details_for_policy_seq3(cmd_data, metadata_files_processed, elems_to_accumulate_hash, list_all_cmds):

  ## CCCCC 
  curcount = 0
  alt_seq_hashsum = dict()
  sha256_alt = hashlib.sha256()

  # Initialize the SHA elements we will create cumulative hashes for.
  sha256_hasher = dict()
  for desc in elems_to_accumulate_hash:
    sha256_hasher[desc] = hashlib.sha256()

  # Iterate through each command and process the cmd_data field. 
  for cmd_name, desclist in cmd_data.iteritems():
    # Add specific command information to main_metadata.
    for desc, desc_val in desclist.iteritems():  
      # Adding a sequence number.
      if (desc in ["sequence"]):
        metadata_files_processed["application"][cmd_name][desc] = desc_val
      else:
        # Process the hash and filepath details.
        hash_val = utils.get_hash(desc_val)
        metadata_files_processed["application"][cmd_name][desc + "_hash"] = hash_val
        metadata_files_processed["application"][cmd_name][desc + "_path"] = desc_val 
        # Accumulate the hash for this file type.
        sha256_hasher[desc].update(hash_val)

        if (desc == "metadata"):
          print "CCCCC", metadata_files_processed["application"][cmd_name]["sequence"], "--- hash[", cmd_name, "][", desc, "]=", hash_val, "\n--hashcur=", sha256_hasher[desc].hexdigest()
          curcount = curcount + 1


    seq_num = metadata_files_processed["application"][cmd_name]["sequence"]
    ### CCCCC altaccum test 
    alt_seq_hashsum[seq_num] = dict()
    alt_seq_hashsum[seq_num]["metadata"] = metadata_files_processed["application"][cmd_name]["metadata_hash"]
    ##print "THE METADATA =================",  metadata_files_processed["application"][cmd_name]


  ##  CCCCCCC
  for counter in xrange(0, len(alt_seq_hashsum)):  
    curhash = alt_seq_hashsum[counter]["metadata"]
    sha256_alt.update(curhash)
    print "\n\n cur[", counter, "] hash=", curhash, "\n curhash=", sha256_alt.hexdigest()

  # Create the final hex value for the hash and assign to main_metadata.
  for desc in elems_to_accumulate_hash:
    metadata_files_processed["cumulative_" + desc + "_hash"] = sha256_hasher[desc].hexdigest()
    if (desc == "metadata"):
       print "CCCCC finalhash=", metadata_files_processed["cumulative_" + desc + "_hash"]



def add_main_hash_details_for_policy_seq2(cmd_data, metadata_files_processed):
  #sha256_hasher = hashlib.sha256()
  sha256_hasher = dict()
  """
  sha256_hasher["metadata"] = {}
  sha256_hasher["output_tar"] = {}
  """
  sha256_hasher["metadata"] = hashlib.sha256()
  sha256_hasher["output_tar"] = hashlib.sha256()

  for cmd_name, desclist in cmd_data.iteritems():
    # Add command specific information to the main_metadata file.
    print "CCC desclist=", desclist
    for desc, desc_val in desclist.iteritems():  
      if (desc in ["sequence"]):
        metadata_files_processed["application"][cmd_name][desc] = desc_val
      else:
        # Process the hash and filepath details.
        hash_val = utils.get_hash(desc_val)
        metadata_files_processed["application"][cmd_name][desc + "_hash"] = hash_val
        metadata_files_processed["application"][cmd_name][desc + "_path"] = desc_val 
        # Add to the hasher to calculate the cumulative hash of metadata files.
        sha256_hasher[desc].update(hash_val)
    metadata_files_processed["cumulative_" + desc + "_hash"] = sha256_hasher[desc].hexdigest()



def process_command(command, args_policy, prev_output_filepath):
  """
  <Purpose>
    Straightforward function to encapsulate the program's core logic. Called
    for each command that will be processed.

  <Arguments>
    command:
      Data object that contains the command, verify_command, 
      command_name and input_file for the command.
    args_policy:
      Is the filepath of the passed in policy file from the 
      commandline. 
    prev_output_filepath:
      The previous output filepath generated from the last 
      command and the use_previous_output flag is True.

  <Exceptions>
    TBD.

  <Returns>
    This function returns the file path/name of metadata file 
    and the file path/name of the output_tar file.
  """

  # Grab the command line arguments
  cmd_name = command[2]
  cmd_source_input_path = os.path.join(DEFAULT_SOURCE_INPUT_DIR, cmd_name)
  cd_source_input = DEFAULT_CMD_TO_SOURCE_INPUT_DIR_BEGIN + cmd_source_input_path + DEFAULT_CMD_TO_SOURCE_INPUT_DIR_END

  # Now tie the cmds to the the source_input directory.  
  cmd_string = cd_source_input + command[0]
  cmd_to_verify = command[1]
  if (command[1]):
    cmd_to_verify = cd_source_input + command[1]

  # Details for the output_filepath, also tie to the source_input dir.
  output_filepath = command[5]
  if (output_filepath):
    output_filepath = os.path.join(cmd_source_input_path, output_filepath)
  orig_output_filepath = command[5]
  output_prefilename = os.path.join(cmd_source_input_path, cmd_name) 

  # Details for the use of input_filepath.
  use_prev_output = command[4]
  input_filepath = command[3]
  if (use_prev_output):
    input_filepath = prev_output_filepath


  # Setup the policy file which is either passed from the commandline, 
  # otherwise the default policy is used.
  if args_policy:
    policy_filepath = args_policy
  else:
    home_directory = os.path.dirname(os.path.realpath(__file__))
    policy_filepath = os.path.join(home_directory, DEFAULT_POLICY_FILENAME)


  # Setup the metadata dictionary
  metadata = dict()
  metadata['variables'] = dict()
  metadata['application'] = dict()


  # The input file is expected to be passed as a tar, 
  # and will be uncompressed in the DEFAULT_SOURCE_INPUT_DIR. 
  # If errors are found processing input files (does not exist, 
  # etc) then a build error is typically logged in the metadata and this  
  # program continues to process the command.
  utils.untar_file(cmd_source_input_path, input_filepath) 

  # Execute the given command and fill the metadata dict
  process_env_vars(metadata)
  stdout, stderr, return_code = exec_cmd(cmd_string, input_filepath)
  process_app_data(metadata, cmd_string, input_filepath, cmd_name, stdout, stderr, return_code)

  # Execute the verify command
  metadata["application"]["verify_cmd"] = cmd_to_verify
  metadata["application"]["verify_cmd_return_code"] = ""
  if (cmd_to_verify != None):
    stdout, stderr, return_code = exec_cmd(cmd_to_verify, None)
    metadata["application"]["verify_cmd_return_code"] = "No|" + str(return_code) + "|" + stderr
    if return_code == 0:
      metadata["application"]["verify_cmd_return_code"] = "Yes|" + stdout


  # If the output target is specified, tar it and place 
  # into the source_input/<cmd_name>/<cmd_name>.tar
  utils.tar_file(output_filepath, output_prefilename, orig_output_filepath)
  qualified_output_file = output_prefilename + ".tar"
  metadata["application"]["output_tar_path"] = qualified_output_file
  metadata["application"]["output_tar_hash"] = utils.get_hash(qualified_output_file)

  # Process the policy file 
  policy_dict = process_policy_file(metadata, policy_filepath)
  stdout_file = os.path.join(DEFAULT_WORK_DIR, cmd_name + "_out")
  stderr_file = os.path.join(DEFAULT_WORK_DIR, cmd_name + "_err")
  check_file_against_wordlists(metadata, policy_dict["supplied_data"]["word_lists"], stdout_file, "output_data")
  check_file_against_wordlists(metadata, policy_dict["supplied_data"]["word_lists"], stderr_file, "err_data")

  # Generate the signed JSON
  metadata_file = os.path.join(DEFAULT_WORK_DIR, cmd_name + "_metadata")
  qualified_metadata_file = metadata_file + ".json"
  signed_metadata = signing.sign_json(metadata)
  utils.gen_json(signed_metadata, metadata_file)

  # Return the metadata and output file for main_metadata.
  return (qualified_metadata_file, qualified_output_file)



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
    A list of strings: [stdout, stderr, return_code].
  """

  cmd_process = subprocess.Popen(cmd_string, stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE, shell=True)
  stdout_stderr = cmd_process.communicate()
  process_attributes = [stdout_stderr[0], stdout_stderr[1], cmd_process.returncode]
  return process_attributes


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

  metadata
  metadata['variables']['os'] = dict()
  metadata['variables']['os']['kernel'] = uname[0]
  metadata['variables']['os']['release'] = uname[2]
  metadata['variables']['os']['version'] = uname[3]
  metadata['variables']['hostname'] = uname[1]
  metadata['variables']['cpu_arch'] = uname[4]
  metadata['variables']['timestamp'] = str(datetime.datetime.utcnow())
  metadata['variables']['toto_tool_version'] = TOTO_TOOL_VERSION

  # We use the getpass module here for Unix and Windows compatibility 
  metadata['variables']['user'] = getpass.getuser()
  metadata['variables']['curr_working_dir'] = os.getcwd()


def process_app_data(metadata, cmd_string, input_filepath, cmd_name, stdout, stderr, return_code):
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

    cmd_name:
      A string with a name description for this command.  This value is 
      prepended to output files - err, out, and metatadata.

    stdout:
      A string representing the stdout from the command that was run.

    stderr:
      A string representing the stderr from the command that was run.

    return_code:
      An integer representing the return code from the command that was run.

  <Exceptions>
    TBD.

  <Return>
    None.
  """

  metadata['application']['command'] = cmd_string
  metadata['application']['return_code'] = return_code

  cwd = os.getcwd()
  work_cwd = os.path.join(cwd, DEFAULT_WORK_DIR)
  cmd_source_input_cwd =  os.path.join(DEFAULT_SOURCE_INPUT_DIR, cmd_name)

  # This is to write all files to work directory.  This should
  # probably be created in the main function however.  
  if not os.path.exists(work_cwd): 
    os.mkdir(work_cwd)
  # Create the work/source_input directory to handle the uncompressed 
  if not os.path.exists(DEFAULT_SOURCE_INPUT_DIR): 
    os.mkdir(DEFAULT_SOURCE_INPUT_DIR)
  if not os.path.exists(cmd_source_input_cwd): 
    os.mkdir(cmd_source_input_cwd)

  # For the stdin, stdout and stderr, write each to a file, hash it, and store 
  # the hash and filepath to the metadata
  if input_filepath:
    metadata['application']['input_hash'] = utils.get_hash(input_filepath)
    metadata['application']['input_path'] = input_filepath
  else:
    metadata['application']['input_hash'] = None
    metadata['application']['input_path'] = None

  saved_output_path = os.path.join(work_cwd, cmd_name + "_out")
  utils.write_to_file(stdout, saved_output_path)
  metadata['application']['output_hash'] = utils.get_hash(saved_output_path)
  metadata['application']['output_path'] = saved_output_path
  saved_err_path = os.path.join(work_cwd, cmd_name + "_err")
  utils.write_to_file(stderr, saved_err_path)
  metadata['application']['err_hash'] = utils.get_hash(saved_err_path)
  metadata['application']['err_path'] = saved_err_path


def check_file_against_wordlists(metadata_dict, word_lists, filename, metadata_category):
  """
  <Purpose>
    Reads through a specified output file, searches for related terms 
    corresponding to the categories of failure, warning and success, and records
    the lines and line numbers in which these terms appear.

  <Arguments>
    metadata_dict:
      The dictionary in which we are storing our metadata.

    word_lists:
      A dictionary storing the wordlists for success, failure and warning.

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
  success_words = word_lists["success"]
  failure_words = word_lists["failure"]
  warning_words = word_lists["warning"]

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
  # Straightforward regex to remove non-alpha characters
  regexobj = re.compile('[^a-zA-Z]')
  line_num = 0
  success_count = 0
  failure_count = 0
  warning_count = 0
  for line in fileobj:
    line_num += 1
    line_lower = line.lower()
    line_lower_alpha = regexobj.sub(" ", line_lower)
    tokens = line_lower_alpha.split()
    dict_to_add = dict()
    dict_to_add["line"] = line
    dict_to_add["line_number"] = line_num
    for token in tokens:
      if any(word == token for word in success_words):
        success_list.append(dict_to_add)
        success_count += 1
      elif any(word == token for word in failure_words):
        failure_list.append(dict_to_add)
        failure_count += 1
      elif any(word == token for word in warning_words):
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
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('--command_policy', metavar='FILENAME', help='the path to the desired file command policy')
  group.add_argument('--command', metavar='COMMAND', type=str, help='the bash command to execute the build or test')

  parser.add_argument('--version', action='version', version=TOTO_TOOL_VERSION)
  parser.add_argument('--input', metavar='FILEPATH', help='the path to the desired input file to be routed through stdin')
  parser.add_argument('--policy', metavar='FILENAME', help='the path to the desired file specifying build/test policy')

  return parser.parse_args()


def process_policy_file(metadata_dict, policy_filepath):
  """
  <Purpose>
    Reads in the policy file, converts it to a dictionary and also checks system
    data against constraints from the policy file.

  <Arguments>
    metadata_dict:
      The dictionary representing the metadata.

    policy_filepath:
      The string representing the path to the policy file.

  <Exceptions>
    TBD.

  <Return>
    The dictionary representing the data in the policy file.
  """

  # Load the JSON into a dictionary
  policy_dict = tuf.util.load_json_file(policy_filepath)

  # Check the constraints
  if policy_dict['constraints']['return_code']:
    if metadata_dict['variables']['return_code'] != policy_dict['constraints']['return_code']:
      raise PolicyConstraintException("ERROR: constraint on return_code not met; expected - \"" + policy_dict['constraints']['return_code'] + "\", actual - \"" + metadata_dict['variables']['return_code'] + "\"")
  if policy_dict['constraints']['cpu_arch']:
    if metadata_dict['variables']['cpu_arch'] != policy_dict['constraints']['cpu_arch']:
      raise PolicyConstraintException("ERROR: constraint on cpu_arch not met; expected - \"" + policy_dict['constraints']['cpu_arch'] + "\", actual - \"" + metadata_dict['variables']['cpu_arch'] + "\"")
  if policy_dict['constraints']['os']['kernel']:
    if metadata_dict['variables']['os']['kernel'] != policy_dict['constraints']['os']['kernel']:
      raise PolicyConstraintException("ERROR: constraint on os-kernel not met; expected - \"" + policy_dict['constraints']['os']['kernel'] + "\", actual - \"" + metadata_dict['variables']['os']['kernel'] + "\"")
  if policy_dict['constraints']['os']['release']:
    if metadata_dict['variables']['os']['release'] != policy_dict['constraints']['os']['release']:
      raise PolicyConstraintException("ERROR: constraint on os-release not met; expected - \"" + policy_dict['constraints']['os']['release'] + "\", actual - \"" + metadata_dict['variables']['os']['release'] + "\"")
  if policy_dict['constraints']['os']['version']:
    if metadata_dict['variables']['os']['version'] != policy_dict['constraints']['os']['version']:
      raise PolicyConstraintException("ERROR: constraint on os-version not met; expected - \"" + policy_dict['constraints']['os']['version'] + "\", actual - \"" + metadata_dict['variables']['os']['version'] + "\"")

  for flag in policy_dict['constraints']['command_flags']:
    if flag not in metadata_dict['application']['command']:
      raise PolicyConstraintException("ERROR: constraint on flags not met; flag \"" + flag + "\" not found")

  return policy_dict


class PolicyConstraintException(Exception):
  """This exception indicates that a constraint specified in the policy file was not met"""

  def __init__(self, value):
    self.value = value


  def __str__(self):
    return repr(self.value)


main()
