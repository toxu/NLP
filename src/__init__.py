import os
import argparse

import character_freq

class GlobalEnv:
    pass

ENV = GlobalEnv()

def run(args):
    pass

def train(args):
    chn_freq = character_freq.cal_ch_freq(os.path.join(ENV.data_dir, 'chn.txt'))
    eng_freq = character_freq.cal_ch_freq(os.path.join(ENV.data_dir,'eng.txt'))
    print chn_freq
    print eng_freq

def setup_env(root):
    ENV.proj_root = root
    ENV.src_dir = os.path.join(root, 'src')
    ENV.data_dir = os.path.join(root, 'data')

def execute():
    main_parser = argparse.ArgumentParser()
    sub_parser = main_parser.add_subparsers(title = "valid operations", metavar = 'commad')

    #run
    parser = sub_parser.add_parser('run', help="run the main function")
    parser.set_defaults(func = run)
    parser.add_argument('-s', '--setting', metavar='NAME', help='use settings-NAME.json')

    #train
    parser = sub_parser.add_parser('train', help="run the main function")
    parser.set_defaults(func = train)
    parser.add_argument('-s', '--setting', metavar='NAME', help='use settings-NAME.json')
    
    args = main_parser.parse_args()
    return args.func(args)

def setup(root, settings = None):
    setup_env(root)
    execute()

def main(root):
    setup(root)
