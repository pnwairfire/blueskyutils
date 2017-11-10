#!/usr/bin/env python3

import csv



def main():
    with open('/Users/rhoffman/code/airfire_misc/susan/blueskyutils/test/data/bsf2wrfchem_data/fire_locations_20130818.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)


    #this function skips the first line, which in this case is the label for the column which is not necessary when using DictReader() instead of csv.reader()
    #next(csv_reader)


        for line in csv_reader:
            print(line)


if __name__ == '__main__':
    main()
