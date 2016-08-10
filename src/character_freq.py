import os
import re
import string

import utils

def cal_ch_freq(path):
    dir_name, file_name = os.path.dirname(path), os.path.basename(path)
    words = set([])
    ch_freq = {}
    for ch in string.ascii_lowercase:
        ch_freq[ch] = 0.0
    with open(path) as f:
        for line in f.readlines():
            words.update(set(re.findall('[a-zA-Z]+', line.lower())))
    total = len(words)
    for word in words:
        for ch in set(word):
            ch_freq[ch] += 1
    for k, v in ch_freq.iteritems():
        ch_freq[k] = v/total
    utils.dump_json(os.path.join(dir_name, '%s.json'%file_name), ch_freq)
    return ch_freq
