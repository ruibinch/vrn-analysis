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

    # Extract phase: get VRN + Prices sheets as RDDs
    vrn_rdd, prices_rdd = extract.run(
        sc, 
        log,
        config)

    # Transform phase:
    # convert each car model to a price
    # update prices RDD with any new car types 
    vrn_rdd_tfm, prices_rdd_tfm = transform.run(
        log,
        vrn_rdd,
        prices_rdd)

    # Load phase: Load the transformed RDDs as CSVs and upload back to GSheets
    n_cols = len(vrn_rdd.take(1)[0])
    # load.run(vrn_data_tfm)

    log.info('ETL job finished')
    spark.stop()
    return None
