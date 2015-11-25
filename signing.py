"""
<Program Name>
  signing.py

<Author>
  Casey McGinley
  Fernando Maymi
  Catherine Eng
  Justin Valcarel
  Wilson Li

<Started>
  November 22, 2015

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  To sign and verify the metadata.
"""

import tuf.keys
import tuf.sig
import tuf.util


def print_object(obj_desc, object):
  # Return on prints, potentially remove this function
  return
  verbose = 0
  if (verbose != 0):
  	return
  print obj_desc + "\n==============================\n" 
  print object
  print "\n==============================\n" 





def sign_json(in_data):
  # copy the input dictionary for modified return 
  data = in_data.copy()
  print_object("INITIAL_DATA", data);

  # generate rsa keys
  rsakey_dict = tuf.keys.generate_rsa_key()
  print_object("RSAKEY_DICT", rsakey_dict);

  # generate signature
  #signature = tuf.keys.create_signature(rsakey_dict, data)
  #print_object("SIGNATURE", signature);
  rsa_signature  = tuf.sig.generate_rsa_signature(data, rsakey_dict)
  print_object("RSA_SIGNATURE", rsa_signature);

  # update metadata with public key and signature
  rsakey_dict['keyval']['private'] = ""; 
  data['signed'] = rsakey_dict
  data['signatures'] = rsa_signature
  print_object("FINAL_DATA", data);

  return data





def verify_json(data):
  canonicalData = data.copy()
  del canonicalData['signed']
  del canonicalData['signatures']
  canonicalData = tuf.formats.encode_canonical(canonicalData)
  verify_state = tuf.keys.verify_signature(data['signed'], data['signatures'], canonicalData)

  return verify_state





def run_test1():
  # Setup for dictionary and sign json 
  data =  {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
  retdata = sign_json(data)

  # GOOD DATA - testing verify_json
  print "Good Test:  "
  print verify_json(retdata)

  # BAD DATA - testing verify_json
  print "Bad Test:  "
  xdata = retdata
  xdata['Name'] = 'FakeName'
  print verify_json(xdata)
