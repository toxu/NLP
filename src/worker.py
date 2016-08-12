import os
import time

import utils
import src
import pinyin_seg

def prepare_output():
    if not os.path.isdir(src.ENV.output_dir):
        os.mkdir(src.ENV.output_dir)
    output_folder = os.path.join(src.ENV.output_dir, time.strftime("%Y%m%d%H%M%S"))
    os.mkdir(output_folder)
    return output_folder

def post_processing(word):
    try:
        word = pinyin_seg.seg(word).split(' ')[0]
    except:
        pass
    return word


def start_classify(path, classifier):
    output_folder = prepare_output()
    words = utils.get_words(path)
    for word in words:
        #word = post_processing
        if classifier.classify(word) == 'words':
            utils.push_word_back(os.path.join(output_folder, "words.txt"), word)
        elif classifier.classify(word) == 'pinyin':
            utils.push_word_back(os.path.join(output_folder, "pinyin.txt"), word)
        else:
            pass

def classify_word(word, classifier):
    #word = post_processing(word)
    result =  classifier.classify(word)
    return result
