# import verbs_table
# import adjectives_table
# import nouns_table
# from articles_table import articles_table, pd
# import adverbs_table
from file_io import File
from text import analyze_text
# import sys
# TODO: spacy provides a part of word use it
# TODO: manager arguments in the TUI script
# TODO: find a way how to find sources for each token

INPUT_PATH = "./texts/input_1.txt"

if __name__ == "__main__":
    # Read the text
    text = ""
    with File(INPUT_PATH, "r") as f:
        text = f.getData()

    # tokenize text using german module
    analyzed_dataframe = analyze_text(text)

    # print
    print(analyzed_dataframe.head())
