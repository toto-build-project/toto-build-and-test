import canonicaljson as json

def genJSON(dict, name):
    fname = name + '.json'
    f = open(fname, 'w')
    f.write(json.encode_canonical_json(dict))
