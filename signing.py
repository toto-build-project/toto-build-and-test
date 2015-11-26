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

import tuf
import tuf.keys
import tuf.sig
import tuf.util
import canonicaljson as json


def print_object(obj_desc, object):
  # Return on prints, potentially remove this function
  #return
  verbose = 0
  if (verbose != 0):
  	return
  print obj_desc + "\n==============================\n" 
  print object
  print "\n==============================\n" 





def sign_json(data):
  """
  <Purpose>
    Return a dictionary of the original data with
    the added fields 'signed' and 'signatures'.

    'signed' will contain a dictionary of the form:
    {'keytype': 'rsa',
     'keyid': keyid,
     'keyval': {'public': '-----BEGIN RSA PUBLIC KEY----- ...',
                'private': ''}}

    Note that the private key will be cleared in the resulting dictionary.

    'signatures' will contain a dictionary of the form:
    {'keyid': 'f30a0870d026980100c0573bd557394f8c1bbd6...',
     'method': '...',
     'sig': '...'}.

    The signing process will use the generated RSA keys 
    and the data to generate the signature.

  <Arguments>
    data:
      Data object used to generate the signature.

  <Exceptions>
    tuf.FormatError, if 'rsakey_dict' does not have the correct format.

    tuf.UnsupportedLibraryError, if an unsupported or unavailable library is
    detected.

    TypeError, if a private key is not defined for 'rsakey_dict'.

  <Side Effects>
    'data' is modified to include the 'signed' and 'signatures' fields.
    A 'keystore.txt' file containing the encrypted RSA keys will be created.

  <Returns>
    A dictionary containing the original data with the addition
    of the 'signed' and 'signatures' fields.
  """

  # Use generated RSA keys to create signature.
  rsakey_dict = tuf.keys.generate_rsa_key()
  rsa_signature = tuf.sig.generate_rsa_signature(data, rsakey_dict)

  # The RSA keys need to be encrypted before it is stored locally
  encrypted_keys = tuf.keys.encrypt_key(rsakey_dict, "badpassword")
  fileobj = open('keystore.txt', 'w')
  fileobj.write(encrypted_keys)
  fileobj.close()

  # Update metadata with public key and signature.
  rsakey_dict['keyval']['private'] = ''
  data['signed'] = rsakey_dict
  data['signatures'] = rsa_signature

  return data





def verify_json(jsondata):
  """
  <Purpose>
    Determine whether the private key belonging to 'key_dict' produced
    'signatures' in 'jsondata'. 
    
    The public key found in 'key_dict', the 'method' and 'sig' objects 
    contained in 'signatures' of 'jsondata', and the other metadata in 'jsondata' 
    will be used to complete the verification.

  <Arguments>
    jsondata:
      A json string containing the metadata with the
      'signed' and 'signatures' fields.

  <Exceptions>
    tuf.FormatError, raised if either 'signed' or 'signatures' fields
    in 'data' are improperly formatted.
    
    tuf.UnsupportedLibraryError, if an unsupported or unavailable library is
    detected.
    
    tuf.UnknownMethodError.  Raised if the signing method used by
    'signatures' field in 'data' is not one supported.

  <Side Effects>
    None.

  <Returns>
    Boolean. True if the signature is legitimate for the data.
    False otherwise.  
  """

  # Need to convert JSON string to dict in order to verify.
  canonicalData = tuf.util.load_json_string(jsondata)
  signed = canonicalData['signed']
  signatures = canonicalData['signatures']

  # Verification on metadata needs to be in canonical JSON,
  # and have the 'signed' and 'signatures' key-value pairs removed. 
  del canonicalData['signed']
  del canonicalData['signatures']
  canonicalData = tuf.formats.encode_canonical(canonicalData)
  verify_state = tuf.keys.verify_signature(signed, signatures, canonicalData)

  return verify_state

