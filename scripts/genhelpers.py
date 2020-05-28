import re

from data import prices as price_data
from . import cleaners

def clean_raw_data(s):
    """Basic data cleaning on car details.
    Just so that subsequent splitting by "," or " / " will not result in any problems.
    """

    s = re.sub(',18\'\'', '', s)
    s = re.sub(',HUD, NAV, LASERLIGHT', '', s)
    s = re.sub('TOYOTA / TOYOTA /', 'TOYOTA /', s)
    return s

def is_car_detail(s):
    """Checks if the string represents a car detail in the form of '<make> / <model>'."""
    
    def _is_vrn_letters(s):
        """Checks if the string matches the VRN letter structure."""
        return s.isalpha() \
            and (re.match('^S$', s) is not None \
                or re.match('^(S|E)[A-Z]$', s) is not None \
                or re.match('^(S)[A-Z]{2}$', s) is not None)   
    
    return not (s.isnumeric() or s == '' or s == '-' or _is_vrn_letters(s))

def get_price(car_details):
    """Returns the corresponding price of the input car.

    Args:
        car_details (str): In the structure of `{make} / {model}`
    """

    price = 0.0
    if car_details.isnumeric() or car_details == '':
        return car_details
    elif car_details != '-':
        details_cleaned = cleaners.clean_model_name(car_details)
        if details_cleaned in price_data.prices:
            price_with_commas = price_data.prices[details_cleaned]
            price = float(re.sub(',', '', price_with_commas))
    
    return price
