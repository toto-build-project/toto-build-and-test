"""
<Program Name>
  test_signing.py

<Author>
  Casey McGinley
  Fernando Maymi
  Catherine Eng
  Justin Valcarel
  Wilson Li

<Started>
  November 26, 2015

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Test cases for signing.py 
"""

import unittest
import tuf
import tuf.keys
import tuf.sig
import tuf.util
import canonicaljson as json
import signing
import utils

test_data = {}
return_data = {}



class TestSigningMethods(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    # Setup test_data dictionary to hold data, key, and sig fields.
    test_data["data"] = {'hostname': 'inapp11wk20', 'os': 'Darwin Kernel 12.6.0', 'Arguments': '-v'}

    # Call the sign_json function to populate the test_data dictonary.
    return_data["cdata"] = signing.sign_json(test_data["data"]).copy()
    

  def tearClassDown():
    pass


  def test_sign_json(self):
    # Verify return_data is modified with the addition of key and signatures.
    # Check the results after sign_json and assert that data 
    # is copied and populated.  
    self.assertTrue("cdata" in return_data, "The results could not be added after sign_json")
    self.assertEqual(test_data["data"], return_data["cdata"], "Compare data and return_data are not updated to reflect key, sig fields.")

    # Verify that the signed (public, private) fields are populated.
    self.assertTrue(bool(return_data["cdata"]["signed"]), "Signed data is empty")
    self.assertTrue(len(return_data["cdata"]["signed"]["keyval"]["public"])>0, "Signed public key length must be greater than 0")
    self.assertTrue(len(return_data["cdata"]["signed"]["keyval"]["private"])==0, "Signed private key length must be equal to 0")

    # Verify that the signature fields (sig, keyid) are populated.
    self.assertTrue(bool(return_data), "Signature data is empty")
    self.assertTrue(len(return_data["cdata"]["signatures"]["sig"])>0, "Signature sig length must be greater than 0")
    self.assertTrue(len(return_data["cdata"]["signatures"]["keyid"])>0, "Signature key length must be greater than 0")

    ## CE- WL, if the private key missing - no exception(check sign doc)
    # Add invalid public key.  Should raise an exception.
    xdata = test_data["data"].copy()
    del xdata["signed"]["keyval"]["private"]
    signing.sign_json(xdata)
    # Add a Name field.  This should return false.
    ##self.assertFalse(return_verify, "Verify json test did not return false on invalid data")


  def test_keystore(self):
    # Count the number of lines in keystore.txt, call sign and 
    # and make sure afterwards, the line count is not availble
    # and we cannot find the public key.
    time1 = utils.get_file_modification_time("keystore.txt")
    signing.sign_json(test_data["data"].copy())
    time2 = utils.get_file_modification_time("keystore.txt")
    count2 = utils.filecount("keystore.txt")

    # Raise an error if the keystore file hasn't updated after signing.
    self.assertTrue(time1 < time2, "The keystore.txt file was NOT updated after signing") 
    # Raise an error if the keystore does not contain at least 1 entry 
    # after signing. 
    self.assertTrue(count2 >= 1, "The keystore.txt file does NOT contain an entry.") 

    # Search the file and make sure that we cannot see the public key.
    found_word = utils.word_found_in_file("keystore.txt", "public")
    self.assertFalse(found_word, "The keystore.txt file contains word 'public'")
    


  def test_verify_json(self):
    # Call verify_json with valid dictionary and confirm results.
    json_return_data_string = json.encode_pretty_printed_json(return_data["cdata"])
    return_verify = signing.verify_json(json_return_data_string)
    self.assertTrue(return_verify, "Verify json test did not return true when valid data was passed in")

    # Test the verify_json function to make sure it is correctly 
    # returning valid results when passing in bad data.
    xdata = return_data["cdata"].copy()
    xdata["FakeName"] = 'FakeHost'
    json_xdata_string = json.encode_pretty_printed_json(xdata)
    return_verify = signing.verify_json(json_xdata_string)
    # Add a Name field.  This should return false.
    self.assertFalse(return_verify, "Verify json test did not return false on invalid data")

    # Delete the name field.  Should return true.
    xdata = return_data["cdata"].copy()
    json_xdata_string = json.encode_pretty_printed_json(xdata)
    return_verify = signing.verify_json(json_xdata_string)
    self.assertTrue(return_verify, "JSON reverted back, should return true.")

    # Add invalid public key.  Should raise an exception.
    xdata = return_data["cdata"].copy()
    xdata["signed"]["keyval"]["public"] = "000234234243adsfadfasd"
    json_xdata_string = json.encode_pretty_printed_json(xdata)
    self.assertRaises(tuf.CryptoError, signing.verify_json, json_xdata_string)

    # Add invalid private key.  Should raise an exception.
    xdata = return_data["cdata"].copy()
    xdata["signed"]["keyval"]["private"] = "000234234243adsfadfasd"
    json_xdata_string = json.encode_pretty_printed_json(xdata)
    self.assertRaises(tuf.CryptoError, signing.verify_json, json_xdata_string)

    # Add invalid signature sig key.  Should raise an exception.
    xdata = return_data["cdata"].copy()
    xdata["signatures"]["sig"] = "000234234243adfadfadbcs"
    json_xdata_string = json.encode_pretty_printed_json(xdata)
    # Raise a format error for the field.  This field should be
    # formatted as:  a-f, 0-9.
    self.assertRaises(tuf.FormatError, signing.verify_json, json_xdata_string)
    # Raise an error for an invalid sig field.
    xdata["signatures"]["sig"] = "000234234243adfadfadbc"
    json_xdata_string = json.encode_pretty_printed_json(xdata)
    self.assertRaises(tuf.CryptoError, signing.verify_json, json_xdata_string)

    # Add invalid signature keyid key.  Should raise an exception.
    xdata = return_data["cdata"].copy()
    xdata["signatures"]["keyid"] = "000234234243adfadfadbcs"
    json_xdata_string = json.encode_pretty_printed_json(xdata)
    # Raise a format error for the field.  This field should be
    # formatted as:  a-f, 0-9.
    self.assertRaises(tuf.FormatError, signing.verify_json, json_xdata_string)
    # Raise an error for an invalid keyid field.
    xdata["signatures"]["keyid"] = "000234234243adfadfadbc"
    json_xdata_string = json.encode_pretty_printed_json(xdata)
    self.assertRaises(tuf.CryptoError, signing.verify_json, json_xdata_string)



# Run the unit tests.
if __name__ == '__main__':
  unittest.main()
