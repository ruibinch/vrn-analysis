import gspread
from pyspark import SparkContext
from pyspark.rdd import RDD
from typing import Dict, List, Tuple

from helpers import logging
from utils import gsheet

"""
Extract phase of the ETL pipeline.
"""

def run(sc: SparkContext,
        log: logging.Log4j,
        spreadsheet_id: str,
        vrn_ws_title: str,
        prices_ws_title: str) -> Tuple[RDD, RDD]:
    """Runner of Extract phase.
    
    Loads the "VRN" and "Prices" worksheets that contains the car details
    and car prices.

    Args:
        sc: SparkContext object
        log: Log4j object
        spreadsheet_id: Google Sheets ID
        vrn_ws_title: Title of VRN worksheet
        prices_ws_title: Title of car prices worksheet

    Returns:
        "VRN" worksheet as a list of lists in an RDD
        "Prices" worksheet as a list of lists in an RDD
    """

    vrn_data = gsheet.load_worksheet(spreadsheet_id, vrn_ws_title)
    # FIXME: only include rows from "SLL" onwards for now
    vrn_data = [vrn_data[0], *vrn_data[40:]]
    log.info(f'"{vrn_ws_title}" worksheet loaded')

    prices_data = gsheet.load_worksheet(spreadsheet_id, prices_ws_title)
    prices_data = prices_data[1:] # remove header column
    log.info(f'"{prices_ws_title}" worksheet loaded')

    return sc.parallelize(vrn_data), sc.parallelize(prices_data)
