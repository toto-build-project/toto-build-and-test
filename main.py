import subprocess
import os
import datetime
import sys
import getpass
import genJSON
import shutil
import hashlib

def main():
	command = sys.argv[1]
	stdin = sys.argv[2]
	details = sys.argv[3]

	set_stdin = True
	if stdin.strip() == '-':
		set_stdin = False

	metadata = dict()
	metadata['variables'] = dict()
	metadata['application'] = dict()

	process_env_vars(metadata)
	stdout, stderr = exec_cmd(command, set_stdin, stdin)
	process_app_data(metadata, command, set_stdin, stdin, stdout, stderr, details)
	genJSON.genJSON(metadata, "metadata")

def exec_cmd(command, set_stdin, stdin):
	if set_stdin:
		input_path = os.path.join(os.getcwd(),stdin)
		f = open(input_path,"r")
		command_redirect = command + " < " + input_path
		proc = subprocess.Popen(command, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		f.close()
	else:
		proc = ubprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	return proc.communicate()

def process_env_vars(metadata):
	uname = os.uname()

	metadata['variables']['os'] = dict()
	metadata['variables']['os']['kernel'] = uname[0]
	metadata['variables']['os']['release'] = uname[2]
	metadata['variables']['os']['version'] = uname[3]

	metadata['variables']['hostname'] = uname[1]
	metadata['variables']['cpu_arch'] = uname[4]
	metadata['variables']['timestamp'] = str(datetime.datetime.utcnow())
	metadata['variables']['user'] = getpass.getuser()
	metadata['variables']['curr_working_dir'] = os.getcwd()

def process_app_data(metadata, command, set_stdin, stdin, stdout, stderr, details):
	metadata['application']['command'] = command

	cwd = os.getcwd()

	if set_stdin:
		input_path = os.path.join(cwd,"in")
		shutil.copyfile(stdin,input_path)
		metadata['application']['input_hash'] = get_hash(input_path)
		metadata['application']['input_path'] = input_path
	else:
		metadata['application']['input_hash'] = None
		metadata['application']['input_path'] = None

	output_path = os.path.join(cwd,"out")
	write_to_file(stdout, output_path)
	metadata['application']['output_hash'] = get_hash(output_path)
	metadata['application']['output_path'] = output_path

	err_path = os.path.join(cwd,"err")
	write_to_file(stderr, err_path)
	metadata['application']['err_hash'] = get_hash(err_path)
	metadata['application']['err_path'] = err_path

	metadata['application']['details'] = details

def get_hash(filename):
	md5 = hashlib.md5()
	f = open(filename,"rb")
	while True:
		d = f.read(128)
		if not d:
			break
		md5.update(d)
	f.close()
	return md5.hexdigest()

def write_to_file(s, filename):
	f = open(filename, "w")
	f.write(s)
	f.close()

main()
























