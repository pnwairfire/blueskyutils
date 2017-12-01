import csv
import logging

from .speciation import BSF2FINN_SPECIATION_FACTORS
from .fccs2genveg import FCCS2GENVEG

M2_PER_ACRE = 1000000 / 247.105  # == 4046.8626697153
KG_PER_TON = 907.185

def convert_bsf_to_finn(bsf_fire):
    finn_fire = {
        'DAY': '', # TODO: fill in using file timestamp
        'TIME': '', # TODO: not sure hot to fill in
        'GENVEG': FCCS2GENVEG.get(bsf_fire['fccs_number'], ''),
        'LATI': float(bsf_fire['latitude']),
        'LONGI': float(bsf_fire['longitude']),
        'AREA': float(bsf_fire['area']) * M2_PER_ACRE,
        'PM25': float(bsf_fire['pm25']) * KG_PER_TON

        # TODO: continue setting fields in finn_fire based on
        #  what's in bsf_fire

    }


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
