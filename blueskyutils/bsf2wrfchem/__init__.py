import csv
import logging

from .speciation import BSF2FINN_SPECIATION_FACTORS

def convert_bsf_to_finn(bsf_fire):
    finn_fire = {"fake_finn_field_1": 1, "fake_finn_field_2": "sdf"}
    # TODO: set fields in finn_fire based on waht's in bsf_fire
    return finn_fire

def convert_finn_to_wrfchem(finn_fire):
    wrfchem_fire = {"fake_wrfchem_field_1": 312, "fake_wrfchem_field_2": "jsdflkj"}
    # TODO: set fields in finn_fire based on waht's in bsf_fire
    return wrfchem_fire

def convert(fire_locations_input_file, finn_input_file, wrf_chem_input_file):
    # load bsf fires
    logging.debug("Opening %s", fire_locations_input_file)
    with open(fire_locations_input_file, 'r') as file:
        bsf_fires = [f for f in csv.DictReader(file)]

    # convert fires from bsf format to finn
    finn_fires = [convert_bsf_to_finn(f) for f in bsf_fires]
    with open(finn_input_file, 'w') as finn_output_file:
        writer = csv.DictWriter(finn_output_file, list(finn_fires[0].keys()))
        writer.writeheader()
        writer.writerows(finn_fires)

    # convert fires from finn format to wrfchem if user specified
    # wrfchem input file
    if wrf_chem_input_file:
        wrfchem_fires = [convert_finn_to_wrfchem(f) for f in finn_fires]
        with open(wrf_chem_input_file, 'w') as wrfchem_output_file:
            writer = csv.DictWriter(wrfchem_output_file, list(wrfchem_fires[0].keys()))
            writer.writeheader()
            writer.writerows(wrfchem_fires)
