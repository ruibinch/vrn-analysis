import re

"""
general.py contains all of the general functions used in the Transform phase.
"""

def is_car_type(s: str) -> bool:
    """Checks if the string represents a car type in the form of
    '{make} / {model}'.
    """
    
    def _is_vrn_letters(s: str) -> bool:
        """Checks if the string matches the VRN letter structure.
        
        4 possible variants:
        1. 1-letter S
        2. 2-letter starting with S, e.g. SB
        3. 2-letter starting with E, e.g. EP
        4. 3-letter starting with S, e.g. SDD
        """
        return s.isalpha() \
            and (re.match('^S$', s) is not None \
                or re.match('^(S|E)[A-Z]$', s) is not None \
                or re.match('^(S)[A-Z]{2}$', s) is not None)   
    
    return not (s.isnumeric() or s == '' or s == '-' or _is_vrn_letters(s))
