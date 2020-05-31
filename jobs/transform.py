from pyspark.rdd import RDD
import re
from typing import Dict, Generator, List, Union, Tuple

from .transform_scripts import cleaners, general
from helpers import logging
from utils import constants

"""
Transform phase of the ETL pipeline.
"""

def _get_prices_dict(prices_rdd: RDD) -> Dict[str, str]:
    """Performs transformation on the prices RDD to return a dict
    of car model to price.

    Input RDD is a list of lists, where each list has the structure
        [{make}, {model}, {price}],
        e.g. "['B.M.W.', 'M5 30 JAHRE EDITION', '588,800 ']"

    Each list is transformed to a key-value pair of the structure
        {make} / {model}: {price},
        e.g. "B.M.W. / M5 30 JAHRE EDITION: 588,800"

    Args:
        prices_rdd: RDD of car prices

    Returns:
        A dict of key-value mappings from car model to car price.
    """

    prices_dict = prices_rdd \
        .map(lambda x: [x[0], x[1], x[2].strip()]) \
        .map(lambda x: (f'{x[0]} / {x[1]}', x[2])) \
        .collectAsMap()
    return prices_dict

def _car_type_to_price(prices: Dict[str, str],
                       s: str) -> Union[str, float]:
    """Maps the car type to the corresponding price.
    
    If the input string is not a car type,
        - Return the string as it is
    If the input string is a car type,
        - Return the price in float, if it exists
        - Else, return the input string, with an additional prefix to indicate that the price is missing
    """

    # First, check if the input string is of a car type structure
    # If not, simply return the string
    if not general.is_car_type(s):
        return s

    if s in prices:
        return re.sub(',', '', prices[s])
    else:
        return f'{constants.ERROR_MISSING_PRICE}{s}'

def _add_new_car_types(log: logging.Log4j,
                       results_rdd: RDD,
                       prices_rdd: RDD) -> List[List[str]]:
    """Adds any new car types found to the overall prices dict.

    Car types with a missing price indicate that these are new car models that
    are not currently part of the existing data.

    These new car types will be added to the prices dict for subsequent manual
    intervention to find the corresponding price for these new car types.

    Args:
        log: Log4j object
        results_rdd: Results RDD
        prices_rdd: Car prices RDD
    
    Returns:
        Transformed car prices RDD
    """

    # create a RDD of new car types
    # reshape it in the form of [{make}, {model}, "0"]
    prices_new_rdd = results_rdd \
        .filter(lambda x: constants.ERROR_MISSING_PRICE in x) \
        .map(lambda x: x.replace(constants.ERROR_MISSING_PRICE, '')) \
        .map(lambda x: [*x.split(' / '), '0']) \

    car_types_new = [f'{x[0]} / {x[1]}' for x in prices_new_rdd.collect()]
    log.info(f'New car types found: {car_types_new}')

    # join the 2 prices RDDs together
    # sort by make, then model name
    prices_rdd_tfm = prices_rdd \
        .union(prices_new_rdd) \
        .sortBy(lambda x: x[1]) \
        .sortBy(lambda x: x[0])

    return prices_rdd_tfm

def run(log: logging.Log4j,
        vrn_rdd: RDD,
        prices_rdd: RDD) -> Tuple[RDD, RDD, RDD]:
    """Runner of Transform phase.

    Args:
        log: Log4j object
        vrn_rdd: VRN RDD
        prices_rdd: Car prices RDD

    Returns:
        Transformed VRN RDD
        Results RDD
        Transformed car prices RDD
    """

    # get car prices as a dict
    prices_dict = _get_prices_dict(prices_rdd)

    # Basic cleaning of raw data
    # Cleans the car model name
    vrn_rdd_tfm = vrn_rdd \
        .flatMap(lambda x: x) \
        .map(lambda x: cleaners.clean_raw_data(x)) \
        .map(lambda x: cleaners.clean_model_name(x))

    # Finds the price mapping for each car type
    results_rdd = vrn_rdd_tfm \
        .map(lambda x: _car_type_to_price(prices_dict, x))

    # Add any new car types to the prices RDD
    prices_rdd_tfm = _add_new_car_types(log, results_rdd, prices_rdd)

    return vrn_rdd_tfm, results_rdd, prices_rdd_tfm
