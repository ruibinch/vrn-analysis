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
        ws_title_vrn: str,
        ws_title_prices: str) -> Tuple[RDD, RDD]:
    """Runner of Extract phase.
    
    Loads the "VRN" and "Prices" worksheets that contains the car details
    and car prices.

    Args:
        sc: SparkContext object
        log: Log4j object
        spreadsheet_id: Google Sheets ID
        ws_title_vrn: Title of VRN worksheet
        ws_title_prices: Title of car prices worksheet

    Returns:
        PySpark RDD
    """

    data_vrn = gsheet.load_worksheet(spreadsheet_id, ws_title_vrn)
    # FIXME: only include rows from "SLL" onwards for now
    data_vrn = [data_vrn[0], *data_vrn[40:]]
    log.info(f'"{ws_title_vrn}" worksheet loaded')

    data_prices = gsheet.load_worksheet(spreadsheet_id, ws_title_prices)
    data_prices = data_prices[1:] # remove header column
    log.info(f'"{ws_title_prices}" worksheet loaded')

    return sc.parallelize(data_vrn), sc.parallelize(data_prices)
