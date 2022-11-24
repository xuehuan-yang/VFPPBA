import argparse
import os

dir = '../../doc/cpas/'

def parse_config():
    parser = argparse.ArgumentParser(description='arg parser')
    parser.add_argument('--dir', type=str, default='0',
                        help='root')
    parser.add_argument('--seq', type=str, default='1',
                        help='root')
    args = parser.parse_args()
    return args

def output_func(dir0):
    args = parse_config()
    if args.dir== '0':
        path = os.path.join(dir, dir0 + '.txt')
    elif args.dir== '1':
        path = os.path.join(dir, dir0 + '_ubuntu.txt')
    elif args.dir== '2':
        path = os.path.join(dir, dir0 + '_raspberry.txt')
    return path

def seq_func():
    args = parse_config()
    seq = int(args.seq)
    return seq