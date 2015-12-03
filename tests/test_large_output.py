"""
<Program Name>
  test_large_output.py
<Author>
  Justin Valcarcel
<Started>
  December 2nd, 2015
<Purpose>
  This is to see if a very large standard output will cause problems with running Toto.
  It is going to print "hello" 100,000 times and see if there are any errors.
"""

for x in range (0, 99999):
  print("hello")


