#!/usr/bin/env python3

import csv
import os
import argparse

parser = argparse.ArgumentParser(description='Choose file: integer 0 - 6')
parser.add_argument('-x', '--file_number', type=int, help='number of file')
args = parser.parse_args()

path = '/Users/rhoffman/code/airfire_misc/susan/blueskyutils/test/data/bsf2wrfchem_data/'
files = [
        'fire_locations_20130817.csv',
        'fire_locations_20130818.csv',
        'fire_locations_20130819.csv',
        'fire_locations_20130820.csv',
        'fire_locations_20130821.csv',
        'fire_locations_20130822.csv',
        'fire_locations_20130823.csv'
        ]


def main(x):
    f = files[x]
    file = open(path +'%s' % f, 'r')
    csv_reader = csv.DictReader(file)
    for line in csv_reader:
        print(line)


if __name__ == '__main__':
    main(args.file_number)