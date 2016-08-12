import os
import argparse
import itertools

import character_freq
import utils
import naive_baysian_classifier
import worker

class GlobalEnv:
    pass

ENV = GlobalEnv()

def parse_settings(setting):
    if setting != None:
        setting_file = os.path.join(ENV.config_dir, '%s.json' % setting)
    else:
        setting_file = os.path.join(ENV.config_dir, 'default.json')
    return utils.try_load_json(setting_file)

def run(args):
    settings = parse_settings(args.setting)
    try:
        chn_trained_file = os.path.join(ENV.data_dir, "%s.json" % settings['chn'])
        eng_trained_file = os.path.join(ENV.data_dir, "%s.json" % settings['eng'])
        test_data = os.path.join(ENV.data_dir, settings['input'])
    except Exception as e:
        print e
    if os.path.isfile(chn_trained_file) and os.path.isfile(eng_trained_file):
        chn_freq = utils.load_json(chn_trained_file)
        eng_freq = utils.load_json(eng_trained_file)
    else:
        chn_freq, eng_freq = train(args)
    
    classifier = naive_baysian_classifier.NaiveBaysianClassifier(chn_freq, eng_freq)
    worker.start_classify(test_data, classifier)

def train(args):
    settings = parse_settings(args.setting)
    try:
        chn_freq = character_freq.cal_ch_freq(os.path.join(ENV.data_dir, settings['chn']))
        eng_freq = character_freq.cal_ch_freq(os.path.join(ENV.data_dir,settings['eng']))
        return chn_freq, eng_freq
    except Exception as e:
        print e

def test(args):
    chn_freq, eng_freq = load_train_result(args)
    classifier = naive_baysian_classifier.NaiveBaysianClassifier(chn_freq, eng_freq)
    print worker.classify_word(args.word, classifier)

def evaluate(args):
    settings = parse_settings(args.setting)
    chn_freq, eng_freq = load_train_result(args)
    classifier = naive_baysian_classifier.NaiveBaysianClassifier(chn_freq, eng_freq)
    benchmark = os.path.join(ENV.data_dir, settings['benchmark'])
    p, total = 0, 0
    with open(benchmark, 'rb') as f:
        for line in f.readlines():
            try:
                word, t = line.split(' ')
            except:
                continue
            if word != '':
                result = worker.classify_word(word.lower(), classifier)
                if result == 'words' and int(t) == 1:
                    p += 1
                if result == 'pinyin' and int(t) == 2:
                    p += 1
                total += 1
    print "total %d, pass: %f" %(total, float(p)/total)
def load_train_result(args):
    settings = parse_settings(args.setting)
    try:
        chn_trained_file = os.path.join(ENV.data_dir, "%s.json" % settings['chn'])
        eng_trained_file = os.path.join(ENV.data_dir, "%s.json" % settings['eng'])
    except Exception as e:
        print e
    if os.path.isfile(chn_trained_file) and os.path.isfile(eng_trained_file):
        chn_freq = utils.load_json(chn_trained_file)
        eng_freq = utils.load_json(eng_trained_file)
    else:
        chn_freq, eng_freq = train(args)
    return chn_freq, eng_freq

def prepare_chn_data(args):
    settings = parse_settings(args.setting)
    try:
        chn_file = os.path.join(ENV.data_dir, "%s" % settings['chn'])
        combinations = os.path.join(ENV.data_dir, "combination_%s" % settings['chn'])
        words = utils.get_words(chn_file)
        for i in range(2,3):
            for expression in list(itertools.combinations(words, i)):
                utils.push_word_back(combinations, ''.join(expression))
    except Exception as e:
        print e


def setup_env(root):
    ENV.proj_root = root
    ENV.src_dir = os.path.join(root, 'src')
    ENV.data_dir = os.path.join(root, 'data')
    ENV.config_dir = os.path.join(root, 'config')
    ENV.output_dir = os.path.join(root, 'output')

def execute():
    main_parser = argparse.ArgumentParser()
    sub_parser = main_parser.add_subparsers(title = "valid operations", metavar = 'commad')

    #run
    parser = sub_parser.add_parser('run', help="run the main function")
    parser.set_defaults(func = run)
    parser.add_argument('-s', '--setting', metavar='NAME', help='use NAME.json')

    #train
    parser = sub_parser.add_parser('train', help="train from the existing data")
    parser.set_defaults(func = train)
    parser.add_argument('-s', '--setting', metavar='NAME', help='use NAME.json')

    #test
    parser = sub_parser.add_parser('test', help="classify one word")
    parser.set_defaults(func = test)
    parser.add_argument('-s', '--setting', metavar='NAME', help='use NAME.json')
    parser.add_argument('-w', '--word', metavar='WORD', help='input a word')

    #prepare
    parser = sub_parser.add_parser('prepare', help="prepare the data for pinyin training")
    parser.set_defaults(func = prepare_chn_data)
    parser.add_argument('-s', '--setting', metavar='NAME', help='use NAME.json')

    #evaluate
    parser = sub_parser.add_parser('evaluate', help="evaluate the performance")
    parser.set_defaults(func = evaluate)
    parser.add_argument('-s', '--setting', metavar='NAME', help='use NAME.json')
    
    args = main_parser.parse_args()
    return args.func(args)

def setup(root, settings = None):
    setup_env(root)

def main(root):
    setup(root)
    execute()
