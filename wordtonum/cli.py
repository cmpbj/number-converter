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
