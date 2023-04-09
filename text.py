import spacy
import pandas as pd
from rich.text import Text, Style
from file_io import File
from rich import print
from nouns_table import NounsCache
from verbs_table import VerbsCache
import time
import random
from multiprocessing import Process
from rich.table import Table
import numpy as np

# TODO: create an entity TEXTANALYZER that holds everything
# TODO: Status when all operations are done

def run_in_background(func, *args, **kwargs):
    process = Process(target=func, args=args, kwargs=kwargs)
    process.start()


# colors dict
colors_definitions = {
    'Bg': "#282828",
    'White': "#fbf1c7",
    'Green': "#b8bb26",
    'Blue': "#08f9e4",
    'Red': "#fe0606",
    'Undefined': "#fabd2f",
    'ADJ': '#baf808',
    'ADP': '#0996b4',
    'ADV': '#e296b4',
    'AUX': '#fc04b7',
    'CONJ': '#0fbed8',
    'CCONJ': '#fa6b97',
    'DET': '#f1d367',
    'INTJ': None,
    'NOUN': '#08f9e4',
    'NUM': '#d9ced6',
    'PART': None,
    'PRON': '#f9c602',
    'PROPN': '#f9c602',
    'PUNCT': '#d9ced6',
    'SCONJ': None,
    'SYM': '#d9ced6',
    'VERB': '#fe0606',
    'X': '#d9ced6',
    'SPACE': None
}


def read_input():
    """
    reads the file input
    """
    text = ""
    with File(INPUT_PATH, "r") as f:
        text = f.getData()
    return text


noun_cache = NounsCache()
verb_cache = VerbsCache()


def analyze_verb(verbs_list):
    for verb in verbs_list:
        # TODO: move randomness to cache
        sleep_interval = random.uniform(0.1, 0.4)
        time.sleep(sleep_interval)
        verb_cache[verb]


def analyze_noun(nouns_list):
    for noun in nouns_list:
        # TODO: move randomness to cache
        sleep_interval = random.uniform(0.1, 0.4)
        time.sleep(sleep_interval)
        noun_cache[noun]


def analyze_text(text):
    """
    intensive function should be called once
    it fills launches all tables filling
    """
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)
    data = []
    for token in doc:
        data.append([token.text,
                     token.lemma_,
                     token.pos_,
                     spacy.explain(token.pos_),
                     token.morph,
                     token.morph.get("Case"),
                     token.morph.get("Number"),
                     token.morph.get("Person"),
                     token.morph.get("PronType"),
                     token.tag_,
                     token.dep_,
                     token.shape_,
                     token.is_alpha,
                     token.is_stop])

    df = pd.DataFrame(data=data, columns=['text',
                                          'lemma_',
                                          'pos_',
                                          'pos_meaning_',
                                          'morph',
                                          'morph_case',
                                          'morph_number',
                                          'morph_person',
                                          'morph_prontype',
                                          'tag_',
                                          'dep_',
                                          'shape_',
                                          'is_alpha',
                                          'is_stop'])

    df['color'] = colors_definitions['White']
    df['highlight'] = False

    # fill the meta data Case, Gender, Number, Person
    df['meta'] = df['morph'].apply(lambda x: x.get('Case'))
    df.apply(lambda row: row['meta'].extend(row['morph'].get('Gender')), axis=1)
    df.apply(lambda row: row['meta'].extend(row['morph'].get('Number')), axis=1)
    df.apply(lambda row: row['meta'].extend(row['morph'].get('Person')), axis=1)

    # trigger meaning parsing for all nouns
    nouns_list = df.loc[(df['pos_'] == 'NOUN'), 'text'].tolist()
    run_in_background(analyze_noun, nouns_list)

    # trigger verb conjugation for all verbs
    verbs_list = df.loc[(df['pos_'] == 'NOUN'), 'text'].tolist()
    run_in_background(analyze_verb, verbs_list)

    return df


INPUT_PATH = "./texts/input_2.txt"

ANALYZED_TEXT = analyze_text(read_input())


def colorize_text(df, scheme=None):
    '''
    Applies colorschems based
    '''
    # reset eveything
    df['color'] = colors_definitions['White']
    df['highlight'] = False

    if scheme == "VERB":
        df.loc[df['pos_'] == scheme, 'color'] = colors_definitions[scheme]
        df.loc[df['pos_'] == "AUX", 'color'] = colors_definitions[scheme]
        df.loc[df['pos_'] == scheme, 'highlight'] = True
        df.loc[df['pos_'] == "AUX", 'highlight'] = True

    elif scheme == "NOUN":
        df.loc[df['pos_'] == scheme, 'color'] = colors_definitions["Undefined"]
        df.loc[(df['pos_'] == 'NOUN') &
               (df['morph'].apply(lambda x: x.get('Gender') == ['Masc'])),
               'color'] = colors_definitions["Green"]
        df.loc[(df['pos_'] == 'NOUN') &
               (df['morph'].apply(lambda x: x.get('Gender') == ['Fem'])),
               'color'] = colors_definitions["Red"]
        df.loc[(df['pos_'] == 'NOUN') &
               (df['morph'].apply(lambda x: x.get('Gender') == ['Neut'])),
               'color'] = colors_definitions["Blue"]
        # highlight
        df.loc[(df['pos_'] == 'NOUN'), 'highlight'] = True

    else:
        df['color'] = df.apply(lambda x: colors_definitions[x['pos_']], axis=1)

    return df


# build rich text with colors
def generate_rich_text(df, width=30):
    text = Text()
    text.no_wrap = False
    text_width = 0
    for index, row in df.iterrows():
        if row['text'] == '\n':
            text.append('\n')
            text_width = 0
            continue

        if text_width >= width:
            text.append('\n')
            text_width = 0

        if index != 0 and row['pos_'] != 'PUNCT' and text_width != 0:
            text.append(" ")
            text_width += 1

        style = Style(color=row['color'])
        text.append(row['text'], style=style)
        text_width += len(row['text'])

        if row['highlight']:
            # meta
            text.append(" ")
            text_width += 1
            style = Style(color=colors_definitions['Bg'],
                          bgcolor=colors_definitions["White"],
                          dim=True)
            text.append(f" {''.join(row['meta'])} ", style=style)
            text_width += len(''.join(row['meta']))

            # lemma_
            text.append("|")
            text_width += 1
            style = Style(color=row['color'],
                          bgcolor=colors_definitions["White"],
                          reverse=True,
                          dim=True)
            text.append(f" {row['lemma_']} ", style=style)
            text_width += len(row['lemma_'])
    return text


def generate_rich_analysis(df):
    tables = []
    nouns_list = df.loc[(df['pos_'] == 'NOUN'), 'text'].tolist()
    for element in nouns_list:
        df = noun_cache[element]
        df.fillna(value="None", inplace=True)
        english_text = noun_cache[element]['nouns']['english']
        german_text = noun_cache[element]['nouns']['german']

        english_text = english_text.split('\n')
        german_text = german_text.split('\n')

        table = Table(title=f"{element}")
        table.add_column("English", justify="left", no_wrap=True)
        table.add_column("German", justify="left", no_wrap=True)
        for eng, ger in zip(english_text, german_text):
            table.add_row(eng, ger)
        tables.append(table)
    return tables


if __name__ == "__main__":
    ##print(ANALYZED_TEXT)
    df = colorize_text(ANALYZED_TEXT, 'NOUN')
    print(generate_rich_analysis(df)[0])
    # print(df)
    # TEXT = generate_rich_text(df, 90)
    # print(TEXT)
