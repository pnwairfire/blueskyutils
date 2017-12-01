import csv
import logging

FINN_SPECIATION = {
    "1": {
        "C10H16": "0.01", "CH3OH": "1.92", "CH3COCH3": "0.22", "GLYALD": "0.5",
        "CH3CHO": "1.03", "CH3CN": "0.21", "ISOP": "0.05", "CH3COOH": "2.08",
        "BIGALK": "0.2", "C2H2": "0.72", "C2H6": "0.82", "HYAC": "1.01",
        "BIGALD": "0.02", "C2H5OH": "0.02", "CRESOL": "0.44", "NO": "0.26",
        "CH2O": "2.12", "BIGENE": "0.45", "NO2": "0.74", "CH3COCHO": "0.81",
        "C3H6": "0.43", "C2H4": "2.27", "MEK": "1.31", "C3H8": "0.18",
        "HCN": "1.01", "MACR": "0", "TOLUENE": "1.16", "HCOOH": "0.65", "MVK": "0"
    },
    "2": {
        "C10H16": "0.01", "CH3OH": "2.49", "CH3COCH3": "0.71", "GLYALD": "1.39",
        "CH3CHO": "0.96", "CH3CN": "0.41", "ISOP": "0.03", "CH3COOH": "1.24",
        "BIGALK": "0.42", "C2H2": "0.55", "C2H6": "1.01", "HYAC": "0",
        "BIGALD": "0.02", "C2H5OH": "0.02", "CRESOL": "0", "NO": "0.61",
        "CH2O": "2.23", "BIGENE": "0.63", "NO2": "0.39", "CH3COCHO": "0.86",
        "C3H6": "0.77", "C2H4": "2.3", "MEK": "1.16", "C3H8": "0.37",
        "HCN": "1.29", "MACR": "0", "TOLUENE": "1.32", "HCOOH": "0.16", "MVK": "0"
    },
    "3": {
        "C10H16": "0.04", "CH3OH": "2.6", "CH3COCH3": "0.39", "GLYALD": "0.79",
        "CH3CHO": "1.27", "CH3CN": "0.36", "ISOP": "0.07", "CH3COOH": "1.87",
        "BIGALK": "0.13", "C2H2": "0.36", "C2H6": "0.82", "HYAC": "0.55",
        "BIGALD": "0.01", "C2H5OH": "0.01", "CRESOL": "0.17", "NO": "0.28",
        "CH2O": "2.08", "BIGENE": "0.52", "NO2": "0.72", "CH3COCHO": "0.37",
        "C3H6": "0.56", "C2H4": "1.38", "MEK": "0.85", "C3H8": "0.1",
        "HCN": "0.56", "MACR": "0.08", "TOLUENE": "2.06", "HCOOH": "0.44", "MVK": "0.2"
    },
    "4": {
        "C10H16": "0.03", "CH3OH": "1.51", "CH3COCH3": "0.2", "GLYALD": "0.28",
        "CH3CHO": "0.38", "CH3CN": "0.12", "ISOP": "0.03", "CH3COOH": "0.53",
        "BIGALK": "0.11", "C2H2": "0.14", "C2H6": "0.29", "HYAC": "8.03",
        "BIGALD": "0.01", "C2H5OH": "0.01", "CRESOL": "0.07", "NO": "0.16",
        "CH2O": "1.33", "BIGENE": "0.22", "NO2": "0.84", "CH3COCHO": "0.17",
        "C3H6": "0.26", "C2H4": "1.11", "MEK": "0.41", "C3H8": "0.1",
        "HCN": "0.51", "MACR": "0", "TOLUENE": "0.61", "HCOOH": "0.26", "MVK": "0"
    },
    "5": {
        "C10H16": "0.04", "CH3OH": "2.5", "CH3COCH3": "0.2", "GLYALD": "0.25",
        "CH3CHO": "0.67", "CH3CN": "0.13", "ISOP": "0.14", "CH3COOH": "1.8",
        "BIGALK": "0.16", "C2H2": "0.2", "C2H6": "1.63", "HYAC": "0.77",
        "BIGALD": "0.01", "C2H5OH": "0.01", "CRESOL": "0.85", "NO": "0.43",
        "CH2O": "1.46", "BIGENE": "0.35", "NO2": "0.57", "CH3COCHO": "0.28",
        "C3H6": "0.76", "C2H4": "1.62", "MEK": "1.64", "C3H8": "0.13",
        "HCN": "2.49", "MACR": "0", "TOLUENE": "1.3", "HCOOH": "0.57", "MVK": "0"
    },
    "6": {
        "C10H16": "0.03", "CH3OH": "1.51", "CH3COCH3": "0.2", "GLYALD": "0.28",
        "CH3CHO": "0.38", "CH3CN": "0.12", "ISOP": "0.03", "CH3COOH": "0.53",
        "BIGALK": "0.11", "C2H2": "0.14", "C2H6": "0.29", "HYAC": "8.03",
        "BIGALD": "0.01", "C2H5OH": "0.01", "CRESOL": "0.07", "NO": "0.16",
        "CH2O": "1.33", "BIGENE": "0.22", "NO2": "0.84", "CH3COCHO": "0.17",
        "C3H6": "0.26", "C2H4": "1.11", "MEK": "0.41", "C3H8": "0.1",
        "HCN": "0.51", "MACR": "0", "TOLUENE": "0.61", "HCOOH": "0.26", "MVK": "0"
    },
    "9": {
        "C10H16": "0", "CH3OH": "2.11", "CH3COCH3": "0.83", "GLYALD": "1.68",
        "CH3CHO": "3.05", "CH3CN": "0.55", "ISOP": "0.6", "CH3COOH": "2.19",
        "BIGALK": "0.09", "C2H2": "0.21", "C2H6": "0.43", "HYAC": "0",
        "BIGALD": "0.01", "C2H5OH": "0.01", "CRESOL": "0.6", "NO": "0.4",
        "CH2O": "1.84", "BIGENE": "0.37", "NO2": "0.6", "CH3COCHO": "0.19",
        "C3H6": "0.38", "C2H4": "1.08", "MEK": "0.79", "C3H8": "0.08",
        "HCN": "0.33", "MACR": "0", "TOLUENE": "1.07", "HCOOH": "0.9", "MVK": "0"
    }
}

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
