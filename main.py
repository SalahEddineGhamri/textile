import verbs_table
import adjectives_table
import nouns_table
from articles_table import articles_table, pd
import adverbs_table
from file_io import File
from text import tokenize_text
import sys
# TODO: manager arguments in the TUI script
# TODO: find a way how to find sources for each token

INPUT_PATH = "./texts/input_1.txt"

if __name__ == "__main__":
    # Read the text
    text = ""
    with File(INPUT_PATH, "r") as f:
        text = f.getData()

    # tokenize text using german module
    tokens = tokenize_text(text)

    # How to search for a source to each token ?

    print(tokens)
