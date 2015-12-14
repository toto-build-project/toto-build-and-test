"""
<Program Name>
  test_main.py

<Author>
  Casey McGinley
  Fernando Maymi
  Catherine Eng
  Justin Valcarel
  Wilson Li

<Started>
  December 13, 2015

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Test cases for main.py 
"""

import unittest
import canonicaljson as json
import tuf
import tuf.keys
import tuf.sig
import tuf.util
import signing
import utils
import hashlib


MAINMETADATA_PATH = "./work/main_metadata.json"

class TestMainMethods(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    pass 

  def tearClassDown():
    pass


  def test_verify_metadatafiles(self):
    # This function verifies the hash matchup between the 
    # main_metadata and <name>_metadata files. 
    return_metadata_verify = utils.verify_metadatafiles(MAINMETADATA_PATH)
    self.assertTrue(return_metadata_verify, "Error: The cumulative hashes read from each <name>_metadata.json must match main_metadata.json hash.")
        

# Run the unit tests.
if __name__ == '__main__':
  unittest.main()
