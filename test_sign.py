import tuf.keys
import tuf.sig
import tuf.util
from signing import *

fav_things = {'Color':'Violet', 
              'Book':'Twilight', 
              'Artist':'Justin Bieber', 
              'Food':'Tacos'}

print sign_json(fav_things)
