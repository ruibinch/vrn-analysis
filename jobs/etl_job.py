from . import extract, transform, load
from helpers.spark import start_spark

def main():
    """Main ETL script definition."""

    # start Spark application and get session, logger, config
    spark, log, config = start_spark(
        app_name='vrn_analysis',
        files=['configs/etl_config.json'])
    sc = spark.sparkContext

    log.info('ETL job running')

    # Extract phase: get VRN + Prices sheets
    rdd_vrn, rdd_prices = extract.run(
        sc, 
        log,
        config['gsheet_spreadsheet_id'],
        config['gsheet_ws_vrn'],
        config['gsheet_ws_prices'])

    # Transform phase: Convert each car model to a price
    data_transformed = transform.run(rdd_vrn, rdd_prices)

    # Load phase: Load the transformed data as a CSV and upload back to GSheets
    load.run(data_transformed)

    log.info('ETL job finished')
    spark.stop()
    return None
