import csv
import datetime
import logging
import os
import traceback

from .speciation import BSF2FINN_SPECIATION_FACTORS
from .fccs2genveg import FCCS2GENVEG

M2_PER_ACRE = 1000000 / 247.105  # == 4046.8626697153
KG_PER_TON = 907.185

def extract_julian_day_from_fire_locations_csv_filename(filename):
    dt = datetime.datetime.strptime(filename, 'fire_locations_%Y%m%d.csv')
    tt = dt.timetuple()
    return tt.tm_yday

def convert_bsf_to_finn(bsf_fire):
    gen_veg = FCCS2GENVEG[bsf_fire.get('fccs_number') or '0']
    bsf_fire_voc = float(bsf_fire['voc']) * KG_PER_TON
    finn_fire = {
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

def convert(fire_locations_input_file, finn_input_file):
    # load bsf fires
    julia_day = extract_julian_day_from_fire_locations_csv_filename(
        os.path.basename(fire_locations_input_file))
    logging.debug("Opening %s", fire_locations_input_file)
    with open(fire_locations_input_file, 'r') as file:
        bsf_fires = [f for f in csv.DictReader(file)]

    # convert fires from bsf format to finn
    finn_fires = []
    for f in bsf_fires:
        try:
            finn_fire = convert_bsf_to_finn(f)
            finn_fire['DAY'] = julia_day
            finn_fire['TIME'] = '1000'
            finn_fires.append(finn_fire)
        except Exception as e:
            logging.error("Failed to convert BSF fire %s", f)
            logging.debug(traceback.format_exc())
    if not finn_fires:
        raise RuntimeError("Failed to convert all BSF fires")

    with open(finn_input_file, 'w') as finn_output_file:
        writer = csv.DictWriter(finn_output_file, list(finn_fires[0].keys()))
        writer.writeheader()
        writer.writerows(finn_fires)

def create_finn_config_file(finn_fire, finn_config_file):
    # path will be specified by the user
    wrf_directory = '/home/susan/WRF/data_from_Serena/'
    fire_directory = os.path.dirname(finn_input_file)
    fire_filename = os.path.basename(finn_input_file)
    start_date = get_start_date_from_args
    end_date = get_end_date_from_args
    SPECIES_MAPPINGS = """wrf2fire_map = 'co -> CO', 'no -> NO', 'so2 -> SO2', 'bigalk -> BIGALK',
                         'bigene -> BIGENE', 'c2h4 -> C2H4', 'c2h5oh -> C2H5OH',
                         'c2h6 -> C2H6', 'c3h8 -> C3H8','c3h6 -> C3H6','ch2o -> CH2O', 'ch3cho -> CH3CHO',
                         'ch3coch3 -> CH3COCH3','ch3oh -> CH3OH','mek -> MEK','toluene -> TOLUENE',
                         'nh3 -> NH3','no2 -> NO2','open -> BIGALD','c10h16 -> C10H16',
                         'ch3cooh -> CH3COOH','cres -> CRESOL','glyald -> GLYALD','mgly -> CH3COCHO',
                         'acetol -> HYAC','isop -> ISOP','macr -> MACR'
                         'mvk -> MVK','hcn -> HCN','hcooh -> HCOOH','c2h2 -> C2H2',
                         'oc -> 0.24*PM25 + 0.3*PM10;aerosol', 'bc -> 0.01*PM25 + 0.08*PM10;aerosol',
                         'sulf -> -0.01*PM25 + 0.02*PM10;aerosol',
                         'pm25 -> 0.36*PM25;aerosol','pm10 -> -0.61*PM25 + 0.61*PM10;aerosol'
                       """
    f.write(SPECIES_MAPPINGS)

    # create finn config files
    finn_pre_config_files = []
    for f in finn_fires:
        try:
            finn_pre_config_file = create_finn_config_file(f)
            diag_level = 400
            max_fire_size = 50
            # how to add species mappings?
            SPECIES_MAPPINGS = SPECIES_MAPPINGS
            finn_pre_config_files.append(finn_config_file)
            # is e the right variable?
        except Exception as e:
            # is %s the correct placeholder?
            logging.error("Failed to create FINN config file %s")
            logging.debug(traceback.format_exc())
    if not finn_pre_config_files:
        raise RuntimeError("Failed to create all FINN config files")

    # this file needs stop to be written as a FINN compatible file, not a csv
    with open(finn_pre_config_file, 'w') as finn_config_file:
        writer =

    # convert fires from finn format to wrfchem if user specified
    # wrfchem input file
    # if wrf_chem_input_file:
    #     wrfchem_fires = [convert_finn_to_wrfchem(f) for f in finn_fires]
    #     with open(wrf_chem_input_file, 'w') as wrfchem_output_file:
    #         writer = csv.DictWriter(wrfchem_output_file, list(wrfchem_fires[0].keys()))
    #         writer.writeheader()
    #         writer.writerows(wrfchem_fires)
