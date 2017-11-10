#!/usr/bin/env python3

import csv
#import os



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


def main():
    for f in files:
        file = open(path +'%s' % f, 'r')
        csv_reader = csv.DictReader(file)
        for line in csv_reader:
                print(line)


if __name__ == '__main__':
    main()