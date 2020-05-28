import re

"""Common cleaning methods.

Used for cleaning of the car model name.
"""

def _remove_all_words_in_brackets(s):
    # e.g. "E200 AVG (R18 LED)" to "E200 AVG"
    return re.sub('\s(\(.*\))', '', s)

def _remove_text_after_marker(s, marker):
    # e.g. "B3 BITURBO TOURING S/R" to "B3 BITURBO"
    return re.sub(f'(?<={marker}).*', '', s)

def _remove_trailing_letters_behind_engine_cc(s):
    # e.g. "ODYSSEY 2.4L" to "ODYSSEY 2.4"
    return re.sub('(?<=\d\.\d)\S+', '', s)

def _remove_trailing_words(s, words):
    pattern = '|'.join(words)
    return re.sub(f'\s({pattern})$', '', s)
    
"""Main method"""

def clean_model_name(car_details):
    """Performs cleaning of the car model name.
    
    Args:
        details (str): In the structure of `{make} / {model}`
    """

    def clean_alpina(model_name):
        model_name = _remove_text_after_marker(model_name, 'BITURBO')
        return model_name
    
    def clean_aston_martin(model_name):
        # remove the following words
        model_name = re.sub('\s(ABS|A|D\/AB|HID|SMT)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def clean_audi(model_name):
        model_name = re.sub('Q7 40', 'Q7 2.0 40', model_name)
        model_name = re.sub('SB', 'SPORTBACK', model_name)
        
        # e.g. convert "A3 SEDAN 1.0 TFSI S TRONIC (LED)" to "A3 SEDAN 1.0"
        model_name = re.match('[AQRS](.*)(\d\.\d)', model_name)[0]
        return model_name
    
    def clean_bmw(model_name):
        model_name = re.sub('GT', 'GRAN TOURER', model_name)
        model_name = re.sub('(MSPT|MSPORT|M SPORT)', 'M-SPORT', model_name)
        model_name = re.sub('X5 M', 'X5 M-SPORT', model_name)
        model_name = re.sub('X5 XL', 'X5 XLINE', model_name)
        model_name = re.sub('630CI', '630I', model_name)
        model_name = re.sub('740I', '740LI', model_name)
        model_name = re.sub('XDRIVE 40I', 'XDRIVE40I', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\d\.\d\w?|\dWD|\dDR|ABS|AUTO|A\/?T|D\/A(IR)?B(AG)?|DSC|FOG LIGHTS|GAS\/D|HID|HUD|LED|NAV|NVD|PGR|RCP|RR\/ENT|SALOON|SMT|SR|SUNROOF|XL$)', '', model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        return model_name
    
    def clean_bentley(model_name):
        model_name = re.sub('SPUR V8 S', 'SPUR V8 4.0', model_name)
        model_name = re.sub('GT V8 S', 'GT V8', model_name)
        model_name = re.sub('CONTINENTAL FLYING SPUR', 'FLYING SPUR', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\d\sSEATER|ABS|A\/?T|A(UTO)?|DIESEL|\dWD|S\/R)', '', model_name)
        return model_name
    
    def clean_citroen(model_name):
        # remove the following words
        model_name = re.sub('\s(EAT6|S\/R)', '', model_name)
        return model_name
    
    def clean_ferrari(model_name):
        model_name = re.sub('CALIFORNIA T', 'CALIFORNIA 4.3', model_name)
        model_name = re.sub('F430 A', 'F430', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\dWD|\dDR|A\/T|ABS|D\/AB|HID|SMT)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def clean_ford(model_name):
        # remove the following words
        model_name = re.sub('\s(AT|GTDI)', '', model_name)
        return model_name
    
    def clean_honda(model_name):
        model_name = re.sub('ODYSSEY ABSOLUTE', 'ODYSSEY', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\dWD|ABS\b|AT|CVT|D\/AIRBAG|EXV?-S|SR|VTI(R|S))', '', model_name)
        model_name = _remove_trailing_words(model_name, ['ABS', 'A', 'M'])
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        
        return model_name
    
    def clean_hummer(model_name):
        # remove the following trailing words
        model_name = _remove_trailing_words(model_name, ['A'])
        return model_name
    
    def clean_infiniti(model_name):
        # remove the following words
        model_name = re.sub('\s(AWD|A\/T|EU6|S\/R)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
  
    def clean_jaguar(model_name):
        # remove the following words
        model_name = re.sub('\s(V6|SC|SR|SWB|TSS|\(\w+\))', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def clean_jeep(model_name):
        # remove the following words
        model_name = re.sub('\s(ABS|A\/BAG|SRT?)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def clean_kia(model_name):
        # remove the following words
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def clean_lamborghini(model_name):
        # remove the following words
        model_name = re.sub('\s(SMT)', '', model_name)
        return model_name
    
    def clean_land_rover(model_name):
        model_name = re.sub('(7 SEATER|7STR)', '7-SEATER', model_name)
        model_name = re.sub('DISCOVERY SPORT (2.0(D|P))', 'DISCOVERY SPORT 2.0 SI4 SE', model_name)
        model_name = re.sub('DISCOVERY (4 3.0|3.0P)', 'DISCOVERY 3.0 HSE', model_name)
        model_name = re.sub('ROVER 4.4SDV8', 'ROVER 4.4 SDV8', model_name)
        model_name = re.sub('SPORT 3.0S/C', 'SPORT 3.0 SDV6', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\d-SEATER|\dWD|ABS|AT|D\/AB|EU\d|HID|S\/?R|TC|TSS|\(\w+\))', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def clean_maserati(model_name):
        # remove the following words
        model_name = re.sub('\s(AUTO(MATIC)?|DIESEL|MY15|SR)', '', model_name)
        return model_name
    
    def clean_mazda(model_name):
        # remove the following words
        model_name = re.sub('\s(\dDR|\dWD|AT|AUTO|EU6)', '', model_name)
        return model_name
    
    def clean_mclaren(model_name):
        # remove the following words
        model_name = re.sub('MP4 -12C\s', '', model_name)
        return model_name
    
    def clean_mercedes(model_name):
        model_name = re.sub('4M\+ ', '4MATIC+ ', model_name)
        model_name = re.sub('AVG', 'AVANTGARDE', model_name)
        model_name = re.sub('SALN', 'SALOON', model_name)
        model_name = re.sub('C 180', 'C180', model_name)
        model_name = re.sub('E 250', 'E250', model_name)
        model_name = re.sub('250CGI', '250 CGI', model_name)
        # standardise "AMG" as the 2nd word (except for AMG GT)
        model_name = re.sub('AMG E63', 'E63 AMG', model_name)
        model_name = re.sub('AMG GLE43', 'GLE43 AMG', model_name)
        model_name = re.sub('4MATIC COUPE AMG', 'AMG 4MATIC COUPE', model_name)
        model_name = re.sub('GT63 S AMG', 'AMG GT63 S', model_name)
        model_name = re.sub('COUPE (4MATIC|SPORT)', '4MATIC COUPE', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\dDR|\dWD|AT|AUTO|COMPT|D\/AIRBAG|EDITION 1|LINE|SEDAN LONG|PLUS|PREMIUM|SMT|URBAN)', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        
        # standardise model types cause damn Mercedes has so many variations that all sound alike
        # set default type to "AVANTGARDE" for simplicity
        model_name = re.sub('CGI|KOMP(RESSOR)?|SEDAN', 'AVANTGARDE', model_name)
        model_name = re.sub('^CLA180$', 'CLA180 COUPE', model_name)
        model_name = re.sub('^CLA200$', 'CLA200 COUPE', model_name)
        model_name = re.sub('^E250(\sEXCLUSIVE)?$', 'E250 AVANTGARDE', model_name)
        model_name = re.sub('^E320$', 'E320 AVANTGARDE', model_name)
        return model_name
        
    def clean_mini(model_name):
        model_name = re.sub('COOP S', 'COOPER S', model_name)
        model_name = re.sub('CAB-A|CABRIO', 'CABRIOLET', model_name)
        model_name = re.sub('CABRIOLET$', 'CABRIOLET 1.6', model_name)
        model_name = re.sub('COUNTRYMAN JCW', 'JCW COUNTRYMAN', model_name)
        model_name = re.sub('1.6 3DR', '3DR 1.6', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\dWD|ABS|ALL 4 AUTO|AT|D\/A(IR)?B(AG)?|DSC|HB|HID|HUD|LED|NAV)', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        return model_name
    
    def clean_mitsubishi(model_name):
        # remove the following words
        model_name = re.sub('\s(5MT|SUNROOF)', '', model_name)
        return model_name
    
    def clean_nissan(model_name):
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        return model_name
    
    def clean_peugeot(model_name):
        # remove the following words
        model_name = re.sub('\s(AUTO)', '', model_name)
        return model_name
    
    def clean_porsche(model_name):
        model_name = re.sub('CARRERAS\(991\)', 'CARRERA S', model_name)
        model_name = re.sub('^PORSCHE 911 GT3$', '911 GT3', model_name)
        model_name = re.sub('CAB\s', 'CABRIOLET ', model_name)
        model_name = re.sub('EXEC\s', 'EXECUTIVE ', model_name)
        
        # remove the following words
        model_name = _remove_all_words_in_brackets(model_name)
        model_name = re.sub('\s(\d\.\d|\dWD|(\d|S)MT|A\/T|ABS|AUTO|CYP|D\/AIRBAG|DIESEL|E\d|G2|PDK|SES|S(UN)?R(OOF)?|TIP(TRONIC)?|V\d|W\/\w+|WO)', '', model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        
        # standardise model types
        model_name = re.sub('^911 CARRERA S COUPE$', '911 CARRERA S', model_name)
        model_name = re.sub('^MACAN$', 'MACAN II', model_name)
        model_name = re.sub('^MACAN S$', 'MACAN S II', model_name)
        
        return model_name
    
    def clean_renault(model_name):
        # remove the following words
        model_name = re.sub('\s(\d\.\d|AT|EU6)', '', model_name)
        return model_name
    
    def clean_rolls_royce(model_name):
        # remove the following words
        model_name = re.sub('\s(\d.\d|\dWD|\d-SEAT|ABS|A\/?T|AUTO|D\/A(IR)?B(AG)?|GAS\/D|MY\d{2}|NAV|SEDAN|S\/R|TC|V12)', '', model_name)
        model_name = _remove_trailing_words(model_name, ['A'])
        return model_name
    
    def clean_ruf(model_name):
        # remove the following words
        model_name = re.sub('\s(SMT)', '', model_name)
        return model_name
    
    def clean_seat(model_name):
        model_name = re.sub('XCELL', 'XCELLENCE', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\d.\d|\dAT|STYLE|TSI)', '', model_name)
        return model_name
    
    def clean_skoda(model_name):
        model_name = re.sub('L&K', 'LAURIN&KLEMENT', model_name)
        
        # remove the following words
        model_name = re.sub('\s(\d.\d|4x4|TSI)', '', model_name)
        model_name = _remove_all_words_in_brackets(model_name)
        return model_name
    
    def clean_subaru(model_name):
        return model_name
    
    def clean_suzuki(model_name):
        model_name = re.sub('\s(AT|GLX)', '', model_name)
        model_name = _remove_trailing_letters_behind_engine_cc(model_name)
        return model_name
    
    def clean_toyota(model_name):
        # remove the following words
        model_name = _remove_all_words_in_brackets(model_name)
        model_name = re.sub('\s(\d(\s|-)SEATER|\dDR|\dWD|ABS|A\/?T|AIRBAG|AUTO|CVT|EXECUTIVE LOUNGE|M(OON)?R(OOF)?|S\/R|SEDAN|ST(ANDAR)?D|SUV)', '', model_name)
        model_name = _remove_trailing_words(model_name, ['A', 'M'])
        
        # standardise model types cause somehow Alphard has so many different variations
        model_name = re.sub('2.5S', '2.5 S', model_name)
        model_name = re.sub('2.5 SA', '2.5 S-A', model_name)
        model_name = re.sub('2.5\s?S-?C', '2.5 S-C', model_name)
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
        model_name = re.sub('VELLFIRE ELEGANCE', 'VELLFIRE 2.5 ELEGANCE', model_name)
        
        return model_name
    
    def clean_volkswagen(model_name):
        # remove the following words
        model_name = re.sub('\s(\d\w\d{2}\w{2}|AT|CL|HLG|STYLE|TSI)', '', model_name)
        return model_name
    
    def clean_volvo(model_name):
        # remove the following words
        model_name = re.sub('\s(\d\.\d|\dWD|\dDR|ABS|AUTO|D\/AB|TURBO)', '', model_name)
        return model_name

    make_to_clean_fn_mapping = {
        'ALPINA': clean_alpina,
        'ASTON MARTIN': clean_aston_martin,
        'AUDI': clean_audi,
        'B.M.W.': clean_bmw,
        'BENTLEY': clean_bentley,
        'CITROEN': clean_citroen,
        'FERRARI': clean_ferrari,
        'FORD': clean_ford,
        'HONDA': clean_honda,
        'HUMMER': clean_hummer,
        'INFINITI': clean_infiniti,
        'JAGUAR': clean_jaguar,
        'JEEP': clean_jeep,
        'KIA': clean_kia,
        'LAMBORGHINI': clean_lamborghini,
        'LAND ROVER': clean_land_rover,
        'MASERATI': clean_maserati,
        'MAZDA': clean_mazda,
        'MCLAREN': clean_mclaren,
        'MERCEDES BENZ': clean_mercedes,
        'MINI': clean_mini,
        'MITSUBISHI': clean_mitsubishi,
        'NISSAN': clean_nissan,
        'PEUGEOT': clean_peugeot,
        'PORSCHE': clean_porsche,
        'RENAULT': clean_renault,
        'ROLLS ROYCE': clean_rolls_royce,
        'RUF': clean_ruf,
        'SEAT': clean_seat,
        'SKODA': clean_skoda,
        'SUBARU': clean_subaru,
        'SUZUKI': clean_suzuki,
        'TOYOTA': clean_toyota,
        'VOLKSWAGEN': clean_volkswagen,
        'VOLVO': clean_volvo,
    }
    
    make, model_name = car_details.split(' / ')
    if make in make_to_clean_fn_mapping:
        model_name = make_to_clean_fn_mapping[make](model_name)
   
    return f'{make} / {model_name}'
