import re
from typing import List

from . import general

"""
cleaners.py contains all of the functions used for various data cleaning.
"""

# Basic data cleaning

def clean_raw_data(s: str) -> str:
    """Basic data cleaning on each cell value in the "VRN" worksheet.

    Just so that subsequent splitting by " / " will not result in any problems.
    This is run at the start of the Transform phase.

    Args:
        s: Input string

    Returns:
        String with extra "/" symbols removed
    """

    s = re.sub('TOYOTA / TOYOTA /', 'TOYOTA /', s)
    return s

# Main data cleaning on car model name

def _remove_all_words_in_brackets(s: str) -> str:
    # e.g. "E200 AVG (R18 LED)" to "E200 AVG"
    return re.sub('\s(\(.*\))', '', s)

def _remove_text_after_marker(s: str, marker: str) -> str:
    # e.g. marker = "BITURBO"
    # then, "B3 BITURBO TOURING S/R" to "B3 BITURBO"
    return re.sub(f'(?<={marker}).*', '', s)

def _remove_trailing_letters_behind_engine_cc(s: str) -> str:
    # e.g. "ODYSSEY 2.4L" to "ODYSSEY 2.4"
    return re.sub('(?<=\d\.\d)\S+', '', s)

def _remove_trailing_words(s: str, words: List[str]) -> str:
    # e.g. words = ['A']
    # then, "ROLLS ROYCE / WRAITH 6.6 A" to "ROLLS ROYCE / WRAITH 6.6"
    pattern = '|'.join(words)
    return re.sub(f'\s({pattern})$', '', s)

def clean_model_name(s: str) -> str:
    """Performs cleaning of the car model name, if the input string is so.

    This function contains many child functions, where each child function
    performs the data cleaning for a particular car make.

    This segregation facilitates maintainability and debugging.
    
    Args:
        s: Input string

    Returns:
        Cleaned model name if input string was a car model name.
        Else, the input string is returned as it is.
    """

    def _clean_alfa_romeo(model_name: str) -> str:
        return model_name

    def _clean_alpina(model_name: str) -> str:
        model_name = _remove_text_after_marker(model_name, 'BITURBO')
        return model_name
    
    def _clean_aston_martin(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(ABS|A|D\/AB|HID|SMT)', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def _clean_audi(model_name: str) -> str:
        model_name = re.sub(',18\'\'', '', model_name)
        model_name = re.sub('Q7 40', 'Q7 2.0 40', model_name)
        model_name = re.sub('SB', 'SPORTBACK', model_name)
        
        # e.g. convert "A3 SEDAN 1.0 TFSI S TRONIC (LED)" to "A3 SEDAN 1.0"
        model_name = _remove_text_after_marker(model_name, '(\d\.\d)')
        return model_name
    
    def _clean_bmw(model_name: str) -> str:
        # remove phrases with commas first
        model_name = re.sub(', LED HL', '', model_name)
        model_name = re.sub(',HUD, NAV, LASERLIGHT', '', model_name)

        # remove the following words
        # not sure if "SE" is integral
        model_name = re.sub('\s(\d\.\d\w?|\d\s?S(EA)?TE?R?|(A|\d)WD|\dDR|ABS?|AUTO|A\/STR|A\/?T|(D\/)?A?(IR)?B(AG)?S?|DSC|EU6|FL|FOG\s?LIGHTS?|GAS\/D|HATCH|HBA|HID|HL|HUD|INT|LASERLIGHT|LED|NAV|NVD|PGR|RCP|RR\/ENT|SALOON|SE(DAN)?|SMT|SR|SUNROOF|TC|XL$)', '', model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        
        model_name = re.sub('630CI', '630I', model_name)
        model_name = re.sub('740I', '740LI', model_name)
        model_name = re.sub('GT', 'GRAN TOURER', model_name)
        model_name = re.sub('(MSPT|MSPORT|M SPORT)', 'M-SPORT', model_name)
        model_name = re.sub('M-SPORTX', 'M-SPORT X', model_name)
        model_name = re.sub('M6 4.4', 'M6 GRAN COUPE', model_name)
        model_name = re.sub('X3 SDRIVE 20I', 'X3 SDRIVE20I', model_name)
        model_name = re.sub('^X5 M$', 'X5 M-SPORT', model_name)
        model_name = re.sub('^X5$', 'X5 XLINE', model_name)
        model_name = re.sub('^X5 XL$', 'X5 XLINE', model_name)
        model_name = re.sub('^X6 M$', 'X6 M-SPORT', model_name)
        model_name = re.sub('X7 XDRIVE 40I', 'X7 XDRIVE40I', model_name)
        return model_name
    
    def _clean_bentley(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\d\sSEATER|ABS|A\/?T|A(UTO)?|D\/AB|DIESEL|\dWD|S\/?R|SUNROOF|WITHOUT)', '', model_name)
        
        model_name = re.sub('BENTAYGA 6.0', 'BENTAYGA V8', model_name)
        model_name = re.sub('CONTI FS', 'CONTINENTAL FLYING SPUR 6.0', model_name)
        model_name = re.sub('GT SPEED$', 'GT SPEED 6.0', model_name)
        model_name = re.sub('GT V8 S', 'GT V8', model_name)
        model_name = re.sub('GTC V8', 'GT V8 CONVERTIBLE', model_name)
        model_name = re.sub('SPUR V8 S', 'SPUR V8 4.0', model_name)
        return model_name
    
    def _clean_citroen(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(EAT6|ABS|EGS|DRL|PSR|SMT|S\/R)', '', model_name)
        model_name = re.sub('C4 PICASSO 1.6$', 'C4 PICASSO 1.6 THP', model_name)
        return model_name
    
    def _clean_ferrari(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\dWD|\dDR|A\/T|ABS|D\/AB|HID|SMT)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)

        model_name = re.sub('CALIFORNIA T', 'CALIFORNIA 4.3', model_name)
        model_name = re.sub('^360SPIDER F1$', '360 F1 SPIDER', model_name)
        model_name = re.sub('F430 A', 'F430', model_name)
        model_name = re.sub('430F1', '430 F1', model_name)
        model_name = re.sub('SPECIALE$', 'SPECIALE 4.5', model_name)
        return model_name
    
    def _clean_fiat(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(16V|SMT)', '', model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        return model_name
    
    def _clean_ford(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(AT|GTDI)', '', model_name)
        
        model_name = re.sub('SMAX TITN', 'S-MAX TITANIUM', model_name)
        return model_name
    
    def _clean_honda(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\dWD|ABS\b|AT|AUTO|CVT|D\/AIRBAG|EXV?-S|SR|VTI(R|S))', '', model_name)
        model_name = _remove_trailing_words(model_name, ['ABS', 'A', 'M'])
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        
        model_name = re.sub('ODYSSEY ABSOLUTE', 'ODYSSEY', model_name)
        model_name = re.sub('VEZEL 1.5', 'VEZEL HYBRID 1.5', model_name)
        return model_name
    
    def _clean_hummer(model_name: str) -> str:
        # remove the following trailing words
        model_name = _remove_trailing_words(model_name, ['A'])
        return model_name

    def _clean_hyundai(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\dWD|\dDR|ABS|AD|AT|D\/AB|EU6|GLS|S\/R)', '', model_name)
        model_name = re.sub('AD\s', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        model_name = _remove_trailing_words(model_name, ['S'])
        return model_name
    
    def _clean_infiniti(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(AWD|A\/T|DCT|EU6|PREMIUM|S\/R)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
  
    def _clean_jaguar(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\dWD|\dDR|\d+PS|V6|ABS|AT|D\/AB|GAS\/D|HID|I4D|PL|RWD|SC|SR|TSS|\(\w+\))', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def _clean_jeep(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(ABS|A\/BAG|SRT?)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def _clean_kia(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(DCT)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def _clean_lamborghini(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(SMT)', '', model_name)
        return model_name
    
    def _clean_land_rover(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\d(-|\s)?S(EA)?TE?R|\dWD|7S|ABS|AT|D\/AB|EU\d|HID|HSE|S\/C|S\/?R|SDV6|SE|SI\d|SVAB|TC|TSS|\(\w+\))', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)

        model_name = re.sub('DISCOVERY 4 3.0', 'DISCOVERY 3.0', model_name)
        return model_name
    
    def _clean_maserati(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\d\.\d|AUTO(MATIC)?|DIESEL|MY15|SR|V6)', '', model_name)
        model_name = re.sub('GHIBLI$', 'GHIBLI 3.0 V6', model_name)
        model_name = re.sub('GRANTURISMO$', 'GRANTURISMO 4.2', model_name)
        return model_name
    
    def _clean_mazda(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\d-?D(OO)?R|5SP|\dWD|AT|AUTO|EU6|SP\.6EAT|WAGON)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def _clean_mclaren(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('MP4 -12C\s', '', model_name)
        return model_name
    
    def _clean_mercedes(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\d\.\d|\dDR|\dWD|A\/?T|ABS|AUTO|BLUEEFFICIENCY|COMPT|D\/AIRBAG|EDITION\s?(1|E)|LINE|LONG|PLUS|PREMIUM|SEDAN|SMT|URBAN)', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        model_name = _remove_trailing_words(model_name, ['A'])

        model_name = re.sub('250CGI', '250 CGI', model_name)
        model_name = re.sub('4M\+', '4MATIC+', model_name)
        model_name = re.sub('AVG', 'AVANTGARDE', model_name)
        model_name = re.sub('CAB$', 'CABRIOLET', model_name)
        model_name = re.sub('C 180', 'C180', model_name)
        model_name = re.sub('C180K', 'C180 AVANTGARDE', model_name)
        model_name = re.sub('CLS 350', 'CLS350', model_name)
        model_name = re.sub('E 200', 'E200', model_name)
        model_name = re.sub('E 250', 'E250', model_name)
        model_name = re.sub('SALN', 'SALOON', model_name)
        # standardise "AMG" as the 1st word for AMG types (i.e. 2 numbers)
        # for other series with AMG engines, standardise "AMG" as the 2nd word
        model_name = re.sub('A45 AMG', 'AMG A45', model_name)
        model_name = re.sub('C43 AMG', 'AMG C43', model_name)
        model_name = re.sub('C63 AMG', 'AMG C63', model_name)
        model_name = re.sub('CLS 63 AMG', 'AMG CLS63', model_name)
        model_name = re.sub('E63 AMG', 'AMG E63', model_name)
        model_name = re.sub('G63 AMG', 'AMG G63', model_name)
        model_name = re.sub('GLE43 AMG', 'AMG GLE43', model_name)
        model_name = re.sub('GT63 S AMG', 'AMG GT63 S', model_name)
        model_name = re.sub('^GLC250 4MATIC COUPE AMG$', 'GLC250 AMG 4MATIC COUPE', model_name)
        model_name = re.sub('COUPE (4MATIC|SPORT)', '4MATIC COUPE', model_name)
        
        # standardise model types cause damn Mercedes has so many variations that all sound alike
        # set default type for general sedan to "AVANTGARDE" for simplicity
        model_name = re.sub('^AMG C63 S$', 'AMG C63 S COUPE', model_name)
        model_name = re.sub('^AMG G63$', 'AMG G63 4MATIC', model_name)
        model_name = re.sub('CGI|KOMP(RESSOR)?|SEDAN', 'AVANTGARDE', model_name)
        model_name = re.sub('^CLA180$', 'CLA180 COUPE', model_name)
        model_name = re.sub('^CLA200$', 'CLA200 COUPE', model_name)
        model_name = re.sub('^E200$', 'E200 AVANTGARDE', model_name)
        model_name = re.sub('^E250(\sEXCLUSIVE)?$', 'E250 AVANTGARDE', model_name)
        model_name = re.sub('^E320$', 'E320 AVANTGARDE', model_name)
        model_name = re.sub('^S400$', 'S400L', model_name)
        model_name = _remove_text_after_marker(model_name, 'V250')
        return model_name
        
    def _clean_mini(model_name: str) -> str:        
        # remove the following words
        model_name = re.sub('\s(\d\.\d|(A|F|\d)WD|ABS|ALL 4 AUTO|A\/?T|D\/A(IR)?B(AG)?|DSC|HB|HID|HUD|LED|NAV|SR|TC)', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        
        model_name = re.sub('2DR', '3DR', model_name)
        model_name = re.sub('COOP S', 'COOPER S', model_name)
        model_name = re.sub('CAB-A|CABRIO', 'CABRIOLET', model_name)
        model_name = re.sub('COUNTRYMAN JCW', 'JCW COUNTRYMAN', model_name)

        # standardise model names
        model_name = re.sub('JCW 3DR LCI', 'JCW COUNTRYMAN', model_name)
        return model_name
    
    def _clean_mitsubishi(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(LANC|5MT|SUNROOF)', '', model_name)
        model_name = re.sub('^LANC\s', '', model_name)
        return model_name
    
    def _clean_nissan(model_name: str) -> str:
        model_name = re.sub('\s(\dDR|\d-STR|\dWD|ABS|AUTO|CVT|D\/AIRBAG|DIG-T|S\/R)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        return model_name
    
    def _clean_peugeot(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(AUTO)', '', model_name)
        return model_name
    
    def _clean_porsche(model_name: str) -> str:        
        # remove the following words
        model_name = _remove_all_words_in_brackets(model_name)
        model_name = re.sub('\s(\d\.\d|(A|\d)WD|(\d|S)MT|A\/T|ABS|AUTO|COUPE|CYP|D\/AIRBAG|DIESEL|E\d|EDITION|G2|PDK|S\/R|SES|S(UN)?R(OOF)?|TIP(TRONIC)?|V\d|W\/\w+|WO)', '', model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        
        model_name = re.sub('PORSCHE CAYENNE TURBO', 'CAYENNE TURBO', model_name)
        model_name = re.sub('911SCOUPETIP', '911 CARRERA S', model_name)
        model_name = re.sub('CARRERAS\(991\)', 'CARRERA S', model_name)
        model_name = re.sub('^PORSCHE 911 GT3$', '911 GT3', model_name)
        model_name = re.sub('CAB\s', 'CABRIOLET ', model_name)
        model_name = re.sub('CAB$', 'CABRIOLET', model_name)
        model_name = re.sub('EXEC\s', 'EXECUTIVE ', model_name)
        model_name = re.sub('EXEC$', 'EXECUTIVE', model_name)

        # standardise model types
        model_name = re.sub('^MACAN$', 'MACAN II', model_name)
        model_name = re.sub('^MACAN S$', 'MACAN S II', model_name)
        model_name = re.sub('^MACAN TURBO$', 'MACAN TURBO II', model_name)
        return model_name
    
    def _clean_renault(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\d\.\d|AT|EU6)', '', model_name)
        return model_name
    
    def _clean_rolls_royce(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\d.\d\w?|\dDR|\dWD|\d-SEAT|ABS|A\/?T|AUTO|D\/A(IR)?B(AG)?|COUPE|GAS\/D|HID|MY\d{2}|NAV|S\/R|SEDAN|SERIES II|SR|TC|TV|V12)', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        return model_name
    
    def _clean_ruf(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(SMT)', '', model_name)
        return model_name
    
    def _clean_seat(model_name: str) -> str:
        model_name = re.sub('XCELL', 'XCELLENCE', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\d.\d|\dAT|STYLE|TSI)', '', model_name)
        return model_name
    
    def _clean_skoda(model_name: str) -> str:
        model_name = re.sub('L&K', 'LAURIN&KLEMENT', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\d.\d|4x4|TSI)', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        return model_name
    
    def _clean_subaru(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\dDR?|ABS|AIRBAG|\d?AT|AWD|CVT|EYESIGHT|SR)', '', model_name)

        model_name = re.sub('2.0XT', '2.0I-L', model_name)
        model_name = re.sub('IMPREZA 1.5R', 'IMPREZA 1.5', model_name)
        model_name = re.sub('WRX STI 2.0M', 'WRX STI 2.0', model_name)
        return model_name
    
    def _clean_suzuki(model_name: str) -> str:
        model_name = re.sub('\s(AT|CVT|GLX)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        return model_name
    
    def _clean_toyota(model_name: str) -> str:
        model_name = re.sub('TOYOTA / TOYOTA /', 'TOYOTA /', model_name)
        model_name = re.sub('ESTIMA', 'PREVIA', model_name)

        # remove the following words
        model_name = re.sub('\s(7(\s|-)SEATER|\dDR|\dWD|ABS|A\/?T|(D\/)?AIRBAG|AUTO|CVT|EDITION|EXECUTIVE\sLOUNGE|G\'S|M(OON)?R(OOF)?|PACKAGE|PLATINUM|PREMIUM|S\/R|SEDAN|SELECTION|ST(ANDAR)?D|SUV)', '', model_name)
        model_name = re.sub('^TOYOTA ', '', model_name)
        model_name = re.sub('-PACKAGE', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        model_name = _remove_trailing_words(model_name, ['A', 'M'])
        
        # standardise Alphard model types cause somehow Alphard has so many different variations
        model_name = re.sub('2.5S', '2.5 S', model_name)
        model_name = re.sub('2.5 SA', '2.5 S-A', model_name)
        model_name = re.sub('2.5\s?S(-|\s)?C-?', '2.5 S-C', model_name)
        model_name = re.sub('3.5SA-C', '3.5 SA-C', model_name)
        model_name = re.sub('3.5SC', '3.5 S-C', model_name)
        model_name = re.sub('^ALPHARD 3.5$', 'ALPHARD 3.5 S-C', model_name)
        model_name = re.sub('ALPHARD ELEGANCE', 'ALPHARD 2.5 ELEGANCE', model_name)
        # and also Vellfire
        model_name = re.sub('2.5Z-?', '2.5 Z', model_name)
        model_name = re.sub('ZG(\sEDITION)?', 'Z G-EDITION', model_name)
        model_name = re.sub('2.4X', '2.4 X', model_name)
        model_name = re.sub('2.4Z', '2.4 Z', model_name)
        model_name = re.sub('2.5X', '2.5 X', model_name)
        model_name = re.sub('Z G-EDITION 3.5', '3.5 Z G-EDITION', model_name)
        model_name = re.sub('3.5VL?', '3.5 V', model_name)
        model_name = re.sub('3.5Z', '3.5 Z', model_name)
        model_name = re.sub('3.5ZA', '3.5 ZA', model_name)
        model_name = re.sub('VELLFIRE ELEGANCE', 'VELLFIRE 2.5', model_name)
        # and for Noah
        model_name = re.sub('2.0X', '2.0 X', model_name)
        model_name = re.sub('1.8X', '1.8 X', model_name)
        # Lexus
        model_name = re.sub('ES300H$', 'ES300H EXECUTIVE', model_name)
        # general
        model_name = re.sub('8 SEATER', '8-SEATER', model_name)
        model_name = re.sub('ALTIS 1.6L$', 'ALTIS 1.6', model_name)
        model_name = re.sub('HYBRID 2.5G$', 'HYBRID 2.5', model_name)
        model_name = re.sub('^HARRIER(\sELEGANCE)? 2.0$', 'HARRIER 2.0 ELEGANCE', model_name)
        model_name = re.sub('^PREVIA(\sHYBRID)? 2.4 X$', 'PREVIA AERAS 2.4', model_name)
        model_name = re.sub('RUSH 1.5G$', 'RUSH 1.5', model_name)
        model_name = re.sub('VIOS 1.5E$', 'VIOS 1.5', model_name)
        
        return model_name
    
    def _clean_volkswagen(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(90|\d\w\d{2}\w{2}|280|A\/?T|A7|CL|GP|HID|HLG?|LED|SR|STYLE|TSI|W\/O)', '', model_name)
        
        model_name = re.sub('^GOLF TL$', 'GOLF 1.4', model_name)
        return model_name
    
    def _clean_volvo(model_name: str) -> str:
        # remove the following words
        model_name = re.sub('\s(\d\.\d|\dWD|\dDR|ABS|AUTO|D\/AB|TURBO)', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        return model_name

    # First, check if the input string is of a car type structure
    # If not, simply return the string
    if not general.is_car_type(s):
        return s

    # Mapping of car make to the corresponding cleaning function
    make_to_clean_fn_mapping = {
        'ALFA ROMEO': _clean_alfa_romeo,
        'ALPINA': _clean_alpina,
        'ASTON MARTIN': _clean_aston_martin,
        'AUDI': _clean_audi,
        'B.M.W.': _clean_bmw,
        'BENTLEY': _clean_bentley,
        'CITROEN': _clean_citroen,
        'FERRARI': _clean_ferrari,
        'FIAT': _clean_fiat,
        'FORD': _clean_ford,
        'HONDA': _clean_honda,
        'HUMMER': _clean_hummer,
        'HYUNDAI': _clean_hyundai,
        'INFINITI': _clean_infiniti,
        'JAGUAR': _clean_jaguar,
        'JEEP': _clean_jeep,
        'KIA': _clean_kia,
        'LAMBORGHINI': _clean_lamborghini,
        'LAND ROVER': _clean_land_rover,
        'MASERATI': _clean_maserati,
        'MAZDA': _clean_mazda,
        'MCLAREN': _clean_mclaren,
        'MERCEDES BENZ': _clean_mercedes,
        'MINI': _clean_mini,
        'MITSUBISHI': _clean_mitsubishi,
        'NISSAN': _clean_nissan,
        'PEUGEOT': _clean_peugeot,
        'PORSCHE': _clean_porsche,
        'RENAULT': _clean_renault,
        'ROLLS ROYCE': _clean_rolls_royce,
        'RUF': _clean_ruf,
        'SEAT': _clean_seat,
        'SKODA': _clean_skoda,
        'SUBARU': _clean_subaru,
        'SUZUKI': _clean_suzuki,
        'TOYOTA': _clean_toyota,
        'VOLKSWAGEN': _clean_volkswagen,
        'VOLVO': _clean_volvo,
    }
    
    make, model_name = s.split(' / ')
    if make in make_to_clean_fn_mapping:
        model_name = make_to_clean_fn_mapping[make](model_name)
   
    return f'{make} / {model_name}'
