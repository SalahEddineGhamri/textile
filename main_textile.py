# import verbs_table
# import adjectives_table
# import nouns_table
# from articles_table import articles_table, pd
# import adverbs_table
from file_io import File
from text import analyze_text, colorize_text
# import sys

# PROGRESS in TEXTILE--------------------------------
# TODO: manager arguments in the TUI script
# TODO: connect tui with the main text facility
# TODO: show already morphological info
# TODO: get versbs conjugation store it in the dataframe
# TODO: get words meaning store it in the dataframe
# ---------------------------------------------------

# TODO: goes to a config & add as argument
INPUT_PATH = "./texts/input_1.txt"


def read_input():
    text = ""
    with File(INPUT_PATH, "r") as f:
        text = f.getData()
    return text


# colorize dataframe
def get_colorized_dataframe():
    return colorize_text(analyze_text(read_input()), None)


if __name__ == "__main__":
    print(get_colorized_dataframe())
