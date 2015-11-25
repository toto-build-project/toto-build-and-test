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
  To sign the metadata.
"""

import tuf.keys
import tuf.sig
import tuf.util

verbose = 0

def print_object(obj_desc, object):
  if (verbose != 0):
  	return
  print obj_desc + "\n==============================\n" 
  print object
  print "\n==============================\n" 



def test_verify(orig, data):
  signature = tuf.sig.generate_rsa_signature(rsa_key, data)

  print "test_verify GOOD results:  " 
  print tuf.keys.verify_signature(rsa_key, signature, data)
  print "\ntest_verify BAD results:  " 
  data =  {'AAAName': 'Zara', 'Age': 7, 'Class': 'First'}
  print tuf.keys.verify_signature(rsa_key, signature, orig)
  return



def sign_json(in_data):
  # copy the input dictionary for modified return 
  data = in_data.copy()
  print_object("INITIAL_DATA", data);

  # generate rsa key
  rsakey_dict = tuf.keys.generate_rsa_key()
  print_object("RSAKEY_DICT", rsakey_dict);

  # generate signature
  signature = tuf.keys.create_signature(rsakey_dict, data)
  print_object("SIGNATURE", signature);

  rsa_signature  = tuf.sig.generate_rsa_signature(signature, rsakey_dict)
  ##print "\nprivate=" + rsakey_dict["keyval"]["private"] + "]]"; 
  ##print_object("RSA_SIGNATURE", rsa_signature);

  # update data with key and signature
  #rsakey_dict["keyval"]["private"] = ""; 
  data["signed"] = rsakey_dict
  data["signatures"] = signature
  print_object("FINAL_DATA", data);

  return data



def verify_json(data, retdata):
  verify_state = tuf.keys.verify_signature(retdata["signed"], retdata["signatures"], data)

  return verify_state


def run_test1():
  # Setup for dictionary and sign json 
  data =  {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
  retdata = sign_json(data)

  # GOOD DATA - verify json call
  print "Good Test:  "
  print verify_json(data, retdata)

  # BAD DATA - verify json call
  print "Bad Test:  "
  xdata =  {'BBBBBName': 'Zara', 'Age': 7, 'Class': 'First'}
  print verify_json(xdata, retdata)


##run_test1()


