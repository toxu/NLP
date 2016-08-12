'''
from https://gist.github.com/wong2/1971238
'''
import os
import re
import string

import utils

def init_freq():
    ch_freq = {}
    cared_chs = list(string.ascii_lowercase)
    cared_chs += ['ing', 'ang', 'eng', 'ao', 'ou', 'zh', 'ch']
    for ch in cared_chs:
        ch_freq[ch] = 0.0
    return ch_freq

def init_two_chs_freq():
    two_chs_freq = {}
    all_characters = list(string.ascii_lowercase)
    for ch1 in all_characters:
        for ch2 in all_characters:
            two_chs_freq[''.join([ch1, ch2])] = 0.0
    return two_chs_freq

def init_three_chs_freq():
    three_chs_freq = {}
    all_characters = list(string.ascii_lowercase)
    for ch1 in all_characters:
        for ch2 in all_characters:
            for ch3 in all_characters:
                three_chs_freq[''.join([ch1, ch2, ch3])] = 0.0
    return three_chs_freq

def cal_ch_freq(path):
    dir_name, file_name = os.path.dirname(path), os.path.basename(path)
    #ch_freq = init_freq()
    ch_freq = init_two_chs_freq()
    ch_freq.update(init_three_chs_freq())
    words = utils.get_words(path)
    total = len(words)
    for word in words:
        for cared_ch in ch_freq:
            if cared_ch in word:
                ch_freq[cared_ch] += 1
    for k, v in ch_freq.iteritems():
        ch_freq[k] = v/total
    utils.dump_json(os.path.join(dir_name, '%s.json'%file_name), ch_freq)
    return ch_freq
