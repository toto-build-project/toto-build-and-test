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

def sign_json(data):
  #signed - keys
  rsakey_dict = tuf.keys.generate_rsa_key()
	
  #signatures - keyid, method, sig
  signature_dict = tuf.sig.generate_rsa_signature(data, rsakey_dict)
	
  rsakey_dict["keyval"]["private"] = ""

  data["signatures"] = signature_dict
  data["signed"] = rsakey_dict
	
  return data

