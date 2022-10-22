# Convertor of "numbers in words" to numbers values

The goal of this application is to convert 'numbers in words' to numbers values.

An user gives a number in words through the command line and the application returns one value that corresponds to that word.

The user also can gives a file in text format with a list of numbers in words through the command line, and the application will returns an output for each numbers in words on the list.

## Instructions about how to use the application

The simplest way to use the application is going to the root of the directory where the application is using the command line. So, you can clone this repository and acess the folder through your command line. After, you can use this commands to interact with the application:

```
$ python -m wordtonum -h

usage: wordtonum [-h] [-n numbers_string [numbers_string ...]] [-f FILE]

Transforma um número por extenso em número

optional arguments:
  -h, --help            show this help message and exit
  -n numbers_string [numbers_string ...], --numbers_string numbers_string [numbers_string ...]
                        Insira uma ou mais números por extenso
  -f FILE, --input-file FILE
                        lê os números por extenso de um arquivo

$ python -m wordtonum "cinco mil oitocentos e sessenta e um"

5861

$ python -m wordtonum -n "cinco mil oitocentos e sessenta e um" "quarenta e nove mil quatrocentos e vinte e dois" "dezesseis milhões setecentos e setenta e sete mil setecentos e noventa e nove" "vinte e um milhões trezentos e sessenta e um mil quatrocentos e oitenta e seis"

5861
49422
16777799
21361486

$ python -m wordtonum -f input.txt

92
1961
1371
2111
4183
5231
4841
5861
8764
1290
874
6945
4838
6172
12187
...

$ python -m wordtonum -f input.txt > output.txt

```

## Scripts

### Creates a function that standardizes the strings

```
# Import modules

import unicodedata

# Function for normalize strings


def standardize_string(string):
    string = string.lower()
    string = unicodedata.normalize("NFD", string)
    string = string.encode("ascii", "ignore")
    string = string.decode("utf-8")

    return string

```

### Creates a function that transforms the strings in values

```
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


```

### CLI

```
#  Import modules

import argparse

from wordtonum.standardize import standardize_string

# Defines the role that will be responsible for allowing the user to interact
# with the application through the command line interface


def cli_read_args_user():

    # Defines an ArgumentParser instance so you can parse
    # the arguments given on the command line.
    parser = argparse.ArgumentParser(
        prog="wordtonum", description="Transforma um número por extenso em número"
    )
    # Add arguments and options for the user to interact with the application
    # In the case below, the add_argument allows the user to include one or more
    # numbers in full on the same command line
    parser.add_argument(
        "-n",
        "--numbers_string",
        metavar="numbers_string",
        nargs='+',
        type=str,
        default=[],
        help="Insira uma ou mais números por extenso"
    )
    # Allows the user to include the Path of a file containing the numbers in words
    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="lê os números por extenso de um arquivo"
    )

    return parser.parse_args()


# Defines a function to print the result

def print_result(result, erro=''):

    if result:
        print(result)
    else:
        print(f"Erro: {erro}")


```

### Puts all the parts together

```
# Import modules

import pathlib
import sys

from wordtonum.cli import print_result, cli_read_args_user
from wordtonum.transform_word import transform_word_to_num

# Defines the main function


def main():

    args_user = cli_read_args_user()
    word_numbers = _get_numbers(args_user)

    if not word_numbers:
        print("Erro: não há números para checar", file=sys.stderr)
        sys.exit(1)
    transform(word_numbers)

# Defines the function that get the numbers


def _get_numbers(args_user):

    word_numbers = args_user.numbers_string

    if args_user.input_file:
        word_numbers += _read_file_numbers(args_user.input_file)
    return word_numbers

# Defines the function that read a file


def _read_file_numbers(file):
    file_path = pathlib.Path(file)
    if file_path.is_file():
        with file_path.open(encoding='utf-8') as numbers_file:
            numbers = filter(lambda linha: linha != '\n', numbers_file)
            numbers = list(map(lambda linha: linha.strip(), numbers))

            if numbers:
                return numbers
            print(f"Erro: arquivo vazio, {file}", file=sys.stderr)
    else:
        print("Erro: arquivo não encontrado", arquivo=sys.stderr)
    return []

# Defines the function that tranform the number in word to numeric value and print the result


def transform(string_numbers):
    for string_number in string_numbers:
        erro = ""

        try:
            result = transform_word_to_num(string_number)
        except Exception as e:
            result = False
            erro = str(e)
        print_result(result, erro)


if __name__ == '__main__':
    main()


```
