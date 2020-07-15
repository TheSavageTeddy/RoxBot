import json
from collections import namedtuple

def getJSON(file):
    with open(file, encoding='utf8') as data:
        return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))