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

def print_object(obj_desc, object):
	print obj_desc + "\n==============================\n" 
	print object
	print "\n==============================\n" 

def test_verify(data):
	rsa_key = tuf.keys.generate_rsa_key()
	signature = tuf.keys.create_signature(rsa_key, data)
	###signature = tuf.sig.generate_rsa_signature(rsa_key, data)

	print "test_verify GOOD results:  " 
	print tuf.keys.verify_signature(rsa_key, signature, data)
	print "\ntest_verify BAD results:  " 
	data =  {'AAAName': 'Zara', 'Age': 7, 'Class': 'First'}
	print tuf.keys.verify_signature(rsa_key, signature, data)
	return


def sign_json(data):
	print_object("INITIAL_DATA", data);
	rsakey_dict = tuf.keys.generate_rsa_key()


	print_object("RSAKEY_DICT", rsakey_dict);
	signature = tuf.keys.create_signature(rsakey_dict, data)


	print_object("SIGNATURE", signature);
	rsa_signature  = tuf.sig.generate_rsa_signature(signature, rsakey_dict)


	##print "\nprivate=" + rsakey_dict["keyval"]["private"] + "]]"; 
	##print_object("RSA_SIGNATURE", rsa_signature);

	data["signed"] = rsakey_dict
	data["signatures"] = signature

	print_object("FINAL_DATA", data);
	return data


def verify_json(data, retdata):
	verify_state = tuf.keys.verify_signature(retdata["signed"], retdata["signatures"], data)

	print ("Verify_json Return:", verify_state)
	return



##### Setup for dictionary and sign json #####
data =  {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
retdata = sign_json(data.copy())

##### GOOD DATA - verify json  #####
print "Good Test:  "
verify_json(data, retdata)


##### BAD DATA - verify json #####
print "Bad Test:  "
xdata =  {'BBBBBName': 'Zara', 'Age': 7, 'Class': 'First'}
verify_json(xdata, retdata)


