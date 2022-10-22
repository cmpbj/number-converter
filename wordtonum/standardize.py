# Import modules

import unicodedata

# Function for normalize strings


def standardize_string(string):
    string = string.lower()
    string = unicodedata.normalize("NFD", string)
    string = string.encode("ascii", "ignore")
    string = string.decode("utf-8")

    return string
