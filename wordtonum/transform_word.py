# Import modules

import re

from wordtonum.standardize import standardize_string

# Function to transform number in words to numeric value


def transform_word_to_num(string_number):

    # Defines a decimal number system dictionary
    numeric_system = {
        'zero': 0,
        'um': 1,
        'dois': 2,
        'tres': 3,
        'quatro': 4,
        'cinco': 5,
        'seis': 6,
        'sete': 7,
        'oito': 8,
        'nove': 9,
        'dez': 10,
        'onze': 11,
        'doze': 12,
        'treze': 13,
        'catorze': 14,
        'quinze': 15,
        'dezesseis': 16,
        'dezessete': 17,
        'dezoito': 18,
        'dezenove': 19,
        'vinte': 20,
        'trinta': 30,
        'quarenta': 40,
        'cinquenta': 50,
        'sessenta': 60,
        'setenta': 70,
        'oitenta': 80,
        'noventa': 90,
        'cem': 100,
        'cento': 100,
        'duzentos': 200,
        'trezentos': 300,
        'quatrocentos': 400,
        'quinhentos': 500,
        'seiscentos': 600,
        'setecentos': 700,
        'oitocentos': 800,
        'novecentos': 900
    }

    # Defines a measurement unit (thousand, million, billion) dictionary

    measurement_unit = {'mil': 1000,
                        'k': 1000,
                        'm': 1000000,
                        'milhao': 1000000,
                        'milhoes': 1000000,
                        'bilhao': 1000000000,
                        'bilhoes': 1000000000,
                        'g': 1000000000,

                        }

    """
    Defines a boolean variable. The objective is to separate the number in word in two types. If 
    the word in number merge digits and units, like '2,5k' the script follow in one way, else it 
    follows another logic 
    """

    # Gets the number part with regex

    verify_digit = bool(re.match('[\d]', string_number))

    try:

        # If true, gets the unit part with regex
        if verify_digit:

            verify_unit = re.search(
                '[^0-9 . ; |, |# |% |-]+', string_number).group()

            # If 'k', 'm' or 'g' is the unit, we have to multiply the number part with the unit
            # For this, we search the unit in the dictionary of units
            if 'k' in verify_unit:
                string_number = re.search(
                    '[0-9 . ; |, |# |% |-]+', string_number).group()
                string_number = string_number.replace(
                    ',', '.').replace(';', '.')
                string_number = float(string_number) * measurement_unit['k']
                return string_number

            elif 'm' in verify_unit:
                string_number = re.search(
                    '[0-9 . ; |, |# |% |-]+', string_number).group()
                string_number = string_number.replace(
                    ',', '.').replace(';', '.')
                string_number = float(string_number) * measurement_unit['m']
                return string_number

            elif 'g' in verify_unit:
                string_number = re.search(
                    '[0-9 . ; |, |# |% |-]+', string_number).group()
                string_number = string_number.replace(
                    ',', '.').replace(';', '.')
                string_number = float(string_number) * measurement_unit['g']
                return string_number

        # If the number in word don't merge digits with units:
        else:
            # standardizes the string, removing accents etc
            standardize_num_word = standardize_string(string_number)

            # Defines auxiliary variables
            part_sum = 0
            result = 0

            for i in standardize_num_word.split():
                # For each number in the list, we sum it with the part sum variable
                if i in numeric_system.keys():
                    part_sum += numeric_system[i]

                # If the number in the list is a unit, we have to multiply the unit with we
                # already have in the part_sum variable. But, if we have nothing in this variable
                # we multiply the unit with 1. After multiply, we set the value of part_sum to zero
                if i in measurement_unit.keys():
                    if part_sum == 0:
                        part_sum = 1
                        result += part_sum * measurement_unit[i]
                        part_sum = 0
                    else:
                        result += part_sum * measurement_unit[i]
                        part_sum = 0

            # Returns the result
            result += part_sum
            return result

    except Exception as e:
        erro = e
    raise erro
