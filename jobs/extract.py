import gspread
from pyspark import SparkContext
from pyspark.rdd import RDD

from utils import gsheet

"""
Extract phase of the ETL pipeline.
"""

def run(sc: SparkContext,
        spreadsheet_id: str,
        ws_title: str) -> RDD:
    """Runner of Extract phase.
    
    Loads the "VRN" worksheet that contains all the car details.

    Args:
        sc: SparkContext object
        spreadsheet_id: Google Sheets ID
        ws_title: Worksheet title

    Returns:
        PySpark RDD
    """

    data = gsheet.load_worksheet(spreadsheet_id, ws_title)

    # FIXME: only include rows from "SLL" onwards for now
    data_trunc = [data[0], *data[40:]]
    return sc.parallelize(data_trunc)
