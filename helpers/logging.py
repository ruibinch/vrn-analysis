from pyspark import SparkSession

"""
This module contains a class that wraps the log4j object instantiated
by the active SparkContext, enabling Log4j logging for PySpark use.
"""

class Log4j(object):
    """Wrapper class for Log4j JVM object.

    Args:
        spark: SparkSession object
    """

    def __init__(self, spark: SparkSession):
        conf = spark.sparkContext.getConf()
        app_id = conf.get('spark.app.id')
        app_name = conf.get('spark.app.name')

        log4j = spark._jvm.org.apache.log4j
        message_prefix = '<' + app_name + ' ' + app_id + '>'
        self.logger = log4j.LogManager.getLogger(message_prefix)

    def error(self, message: str) -> None:
        self.logger.error(message)
        return None
        
    def warn(self, message: str) -> None:
        self.logger.warn(message)
        return None
        
    def info(self, message: str) -> None:
        self.logger.info(message)
        return None
