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
