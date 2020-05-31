import gspread
from pyspark import SparkContext
from pyspark.rdd import RDD
from typing import Dict, List, Tuple

from helpers import logging
from utils import constants, gsheet

"""
Extract phase of the ETL pipeline.
"""

def run(sc: SparkContext,
        log: logging.Log4j,
        config: Dict[str, str]) -> Tuple[RDD, RDD]:
    """Runner of Extract phase.
    
    Loads the "VRN" and "Prices" worksheets that contains the car details
    and car prices.

    Args:
        sc: SparkContext object
        log: Log4j object
        config: Key-value mappings of config values

    Returns:
        "VRN" worksheet as a list of lists in an RDD
        "Prices" worksheet as a list of lists in an RDD
    """

    # config values used
    spreadsheet_id = config[constants.CONFIG_GSHEET_SPREADSHEET_ID]
    ws_title_vrn = config[constants.CONFIG_GSHEET_WS_VRN]
    ws_title_prices = config[constants.CONFIG_GSHEET_WS_PRICES]

    vrn_data = gsheet.load_worksheet(spreadsheet_id, ws_title_vrn)
    # FIXME: only include rows from "SLL" onwards for now
    vrn_data = [vrn_data[0], *vrn_data[40:]]
    log.info(f'"{ws_title_vrn}" worksheet loaded')

    prices_data = gsheet.load_worksheet(spreadsheet_id, ws_title_prices)
    prices_data = prices_data[1:] # remove header column
    log.info(f'"{ws_title_prices}" worksheet loaded')

    return sc.parallelize(vrn_data), sc.parallelize(prices_data)
