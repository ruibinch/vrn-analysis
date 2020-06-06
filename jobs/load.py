from pyspark.rdd import RDD
from typing import Dict, Union

from helpers import logging
from utils import constants, genhelpers, gsheet

"""
Load phase of the ETL pipeline.
"""

def _log_load_resp(log: logging.Log4j,
                   ws_title: str,
                   resp: Dict[str, Union[str, int]]) -> None:
    """Outputs logging messages based on the response object in the Load phase.
    
    Args:
        log: Log4j object
        ws_title: Worksheet title
        resp: Load phase response object
    """

    load_resp_cols = [constants.UPDATED_RANGE, constants.UPDATED_ROWS]
    
    if all(k in resp for k in load_resp_cols):
        log.info(f'{resp[constants.UPDATED_ROWS]} rows updated'
                 f'in range {resp[constants.UPDATED_RANGE]}')
    else:
        log.error(f'Error in saving to "{ws_title}" worksheet')

def run(log: logging.Log4j,
        config: Dict[str, str],
        n_cols: int,
        vrn_rdd_tfm: RDD,
        results_rdd: RDD,
        prices_rdd_tfm: RDD) -> None:
    """Runner of Load phase.

    Loads the transformed RDDs back into the respective worksheets in GSheets:
    - vrn_rdd_tfm - "VRNCleaned" worksheet
    - results_rdd - "Results" worksheet
    - prices_rdd_tfm - "Prices" worksheet

    Args:
        log: Log4j object
        config: Key-value mappings of config values
        n_cols: Number of columns in original VRN worksheet
        vrn_rdd_tfm: Transformed VRN RDD
        results_rdd: Results RDD
        prices_rdd_tfm: Transformed car prices RDD
    """

    # config values used
    spreadsheet_id = config[constants.CONFIG_GSHEET_SPREADSHEET_ID_DEV]
    ws_title_vrn_cleaned = config[constants.CONFIG_GSHEET_WS_VRN_CLEANED]
    ws_title_results = config[constants.CONFIG_GSHEET_WS_RESULTS]
    ws_title_prices = config[constants.CONFIG_GSHEET_WS_PRICES]

    # load VRN RDD and save to "VRNCleaned" worksheet
    vrn_data_tfm_flattened = vrn_rdd_tfm.collect()
    # Split this list into chunks, where each chunk is the number of elements per row
    vrn_data_tfm = list(genhelpers._chunks(vrn_data_tfm_flattened, n_cols))
    vrn_resp = gsheet.save_to_worksheet(
        spreadsheet_id,
        ws_title_vrn_cleaned,
        vrn_data_tfm,
        False)
    _log_load_resp(log, ws_title_results, vrn_resp)

    # load results RDD and save to "Results" worksheet
    results_data_flattened = results_rdd.collect()
    # Split this list into chunks, where each chunk is the number of elements per row
    results_data = list(genhelpers._chunks(results_data_flattened, n_cols))
    results_resp = gsheet.save_to_worksheet(
        spreadsheet_id,
        ws_title_results,
        results_data,
        False)
    _log_load_resp(log, ws_title_results, results_resp)

    # load prices RDD and save to "Prices" worksheet
    prices_data_tfm = prices_rdd_tfm.collect()
    prices_resp = gsheet.save_to_worksheet(
        spreadsheet_id,
        ws_title_prices,
        prices_data_tfm,
        True)
    _log_load_resp(log, ws_title_prices, prices_resp)

    return None
