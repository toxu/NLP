import os
import re
import json

def push_word_back(path, word):
    with open(path, 'a') as f:
        f.write(word + os.linesep)

def get_words(path):
    words = set([])
    with open(path, 'rb') as f:
        for line in f.readlines():
            words.update(set(re.findall('[a-zA-Z]+', line.lower())))
    return words

def dump_json(path, content):
    with open(path, 'w') as f:
        json.dump(content, f, indent = 2, sort_keys = True)

def load_json(path):
    with open(path, 'rb') as f:
        obj = json.load(f)
        return obj

def try_load_json(path):
    try:
        return load_json(path)
    except Exception as e:
        return {}

