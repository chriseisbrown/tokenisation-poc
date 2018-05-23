# !/usr/bin/env python3
import os
from os import listdir
from os.path import isfile, join
import configparser
import argparse
import csv
from pprint import pprint

"""
    "heads" a .csv file
"""

DEFAULT_NUMBER_ROWS = 10


def parse_args():
    '''
        Parse command line arguments
    '''
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser(description='Display top-most rows of a csv file')
    ap.add_argument('filename', help='Name of CSV file to head.')
    ap.add_argument("--n", required=False, type=int, help="number of rows to head", nargs='?')
    args = vars(ap.parse_args())
    if args['n'] is None:
        args['n'] = DEFAULT_NUMBER_ROWS
    return args


def main():
    command_args = parse_args()
    n = command_args['n']
    file_name = command_args['filename']
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        for x in range(0,n):
            for row in reader:
                print(row)
                break





if __name__ == "__main__":
    main()

