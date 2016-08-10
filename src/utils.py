import os
import json

def dump_json(path, content):
    with open(path, 'w') as f:
        json.dump(content, f, indent = 2, sort_keys = True)
