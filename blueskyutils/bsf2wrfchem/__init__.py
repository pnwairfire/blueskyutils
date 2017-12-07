import csv
import logging
import traceback

from .speciation import BSF2FINN_SPECIATION_FACTORS
from .fccs2genveg import FCCS2GENVEG

M2_PER_ACRE = 1000000 / 247.105  # == 4046.8626697153
KG_PER_TON = 907.185

def convert_bsf_to_finn(bsf_fire):
    gen_veg = FCCS2GENVEG[bsf_fire['fccs_number']]
    bsf_fire_voc = float(bsf_fire['voc'])
    finn_fire = {
        'DAY': '', # TODO: fill in using file timestamp
        'TIME': '', # TODO: not sure hot to fill in
        'GENVEG': gen_veg,
        'LATI': float(bsf_fire['latitude']),
        'LONGI': float(bsf_fire['longitude']),
        'AREA': float(bsf_fire['area']) * M2_PER_ACRE,
        'PM25': float(bsf_fire['pm25']) * KG_PER_TON,
        'PM10': float(bsf_fire['pm10']) * KG_PER_TON,
        'CO': float(bsf_fire['co']) * KG_PER_TON *1000 / 28,
        'CO2': float(bsf_fire['co2']) * KG_PER_TON * 1000 / 44,
        'CH4': float(bsf_fire['ch4']) * KG_PER_TON * 1000 / 16,
        'NO': float(bsf_fire['nox']) * KG_PER_TON * 1000 * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["NO"]) / 30,
        'NO2': float(bsf_fire['nox']) * KG_PER_TON * 1000 * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["NO2"]) / 46,
        'NH3': float(bsf_fire['nh3']) * KG_PER_TON * 1000 / 17,
        'SO2': float(bsf_fire['so2']) * KG_PER_TON * 1000 / 64,
        'BIGALD': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["BIGALD"]),
        'BIGALK': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["BIGALK"]),
        'BIGENE': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["BIGENE"]),
        'C10H16': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["C10H16"]),
        'C2H4': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["C2H4"]),
        'C2H5OH': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["C2H5OH"]),
        'C2H6': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["C2H6"]),
        'C3H6': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["C3H6"]),
        'C3H8': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["C3H8"]),
        'CH2O': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["CH2O"]),
        'CH3CHO': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["CH3CHO"]),
        'CH3CN': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["CH3CN"]),
        'CH3COCH3': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["CH3COCH3"]),
        'CH3COCHO': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["CH3COCHO"]),
        'CH3COOH': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["CH3COOH"]),
        'CH3OH': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["CH3OH"]),
        'CRESOL': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["CRESOL"]),
        'GLYALD': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["GLYALD"]),
        'HCN': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["HCN"]),
        'HYAC': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["HYAC"]),
        'ISOP': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["ISOP"]),
        'MACR': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["MACR"]),
        'MEK': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["MEK"]),
        'MVK': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["MVK"]),
        'TOLUENE': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["TOLUENE"]),
        'HCOOH': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["HCOOH"]),
        'C2H2': bsf_fire_voc * float(BSF2FINN_SPECIATION_FACTORS[gen_veg]["C2H2"])


        # ''


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
    finn_fires = []
    for f in bsf_fires:
        try:
            finn_fires.append(convert_bsf_to_finn(f))
        except Exception as e:
            logging.error("Failed to convert BSF fire %s", f)
            logging.debug(traceback.format_exc())
    if not finn_fires:
        raise RuntimeError("Failed to convert all BSF fires")

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
