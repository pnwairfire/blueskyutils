#!/usr/bin/env python3

import argparse
import csv
import logging
import os
import sys

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

def convert_bsf_to_finn(bsf_fire):
    finn_fire = {"fake_finn_field_1": 1, "fake_finn_field_2": "sdf"}
    # TODO: set fields in finn_fire based on waht's in bsf_fire
    return finn_fire

def convert_finn_to_wrfchem(finn_fire):
    wrfchem_fire = {"fake_wrfchem_field_1": 312, "fake_wrfchem_field_2": "jsdflkj"}
    # TODO: set fields in finn_fire based on waht's in bsf_fire
    return wrfchem_fire


def main(args):
    # load bsf fires
    logging.debug("Opening %s", args.fire_locations_input_file)
    with open(args.fire_locations_input_file, 'r') as file:
        bsf_fires = [f for f in csv.DictReader(file)]

    # convert fires from bsf format to finn
    finn_fires = [convert_bsf_to_finn(f) for f in bsf_fires]
    with open(args.finn_input_file, 'w') as finn_output_file:
        writer = csv.DictWriter(finn_output_file, list(finn_fires[0].keys()))
        writer.writeheader()
        writer.writerows(finn_fires)

    # convert fires from finn format to wrfchem if user specified
    # wrfchem input file
    if args.wrf_chem_input_file:
        wrfchem_fires = [convert_finn_to_wrfchem(f) for f in finn_fires]
        with open(args.wrf_chem_input_file, 'w') as wrfchem_output_file:
            writer = csv.DictWriter(wrfchem_output_file, list(wrfchem_fires[0].keys()))
            writer.writeheader()
            writer.writerows(wrfchem_fires)

if __name__ == '__main__':
    args = parse_args()
    main(args)
