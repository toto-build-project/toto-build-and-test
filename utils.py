import canonicaljson as json
import hashlib

def genJSON(dict, name):
  fname = name + '.json'
  f = open(fname, 'w')
  f.write(json.encode_pretty_printed_json(dict))

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
