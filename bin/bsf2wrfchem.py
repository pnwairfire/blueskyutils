#!/usr/bin/env python3

import argparse
import csv
import logging
import os
import sys
import linecache

EPILOG_STR = """
Example

   $ {script_name} -i fire_locations_20130817.csv \\
        -f finn-input-20130817.csv -w wrf-chem-input-20130817.csv

 """.format(script_name=sys.argv[0])

def parse_args():
    parser = argparse.ArgumentParser(description='Choose file: integer 0 - 6',
        epilog=EPILOG_STR, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--fire-locations-input-file', required=True,
        help='Fire locations csv file to process')
    parser.add_argument('-f', '--finn-input-file', required=True,
        help='Finn input input csv file to generate')
    parser.add_argument('-w', '--wrf-chem-input-file', required=False,
        help='WRF-Chem input csv file to generate')
    return parser.parse_args()

def main(args):
    logging.debug("Opening %s", args.fire_locations_input_file)
    with open(args.fire_locations_input_file, 'r') as file:
        csv_reader = csv.DictReader(file)

        n = 5
        line = next((x for i, x in enumerate(csv_reader) if i == n), None)
        print(line['pm25'])

        #for line in csv_reader:
            #print(line)

if __name__ == '__main__':
    args = parse_args()
    main(args)
