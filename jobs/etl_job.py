from . import extract, transform, load
from helpers.spark import start_spark

def main():
    """Main ETL script definition.

    Returns:
        None
    """

    # start Spark application and get session, logger, config
    spark, log, config = start_spark(
        app_name='vrn_analysis',
        files=['configs/etl_config.json'])

    log.info('ETL job running')

    # execute ETL pipeline
    data = extract.run(spark)
    data_transformed = transform.run(data)
    load.run(data_transformed)

    log.info('ETL job finished')
    spark.stop()
    return None
