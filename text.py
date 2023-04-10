import spacy
import pandas as pd
from rich.text import Text, Style
from file_io import File
from rich import print
from nouns_table import NounsCache
from verbs_table import VerbsCache
from adjectives_table import AdjectivesCache
from adverbs_table import AdverbsCache
from prepositions_table import PrepositionsCache
from multiprocessing import Process
from rich.table import Table
import numpy as np

# TODO: avoid repeating words
# TODO: if noun not found try lemma and try decomposing it
# TODO: create an entity TEXTANALYZER that holds everything
# TODO: Status when all operations are done


def run_in_background(func, *args, **kwargs):
    process = Process(target=func, args=args, kwargs=kwargs)
    process.start()
    return process


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
    'INTJ': '#f1d367',
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
adjective_cache = AdjectivesCache()
adverb_cache = AdverbsCache()
preposition_cache = PrepositionsCache()


# TODO: add adjective adverbs prepositions ...
def analyze_verbs(verbs_list):
    # TODO: verifiy return and add other options
    for verb in verbs_list:
        verb_cache[verb]


def analyze_nouns(nouns_list):
    for noun in nouns_list:
        noun_cache[noun]


def analyze_adjectives(adjectives_list):
    for adjective in adjectives_list:
        adjective_cache[adjective]


def analyze_adverbs(adverbs_list):
    for adverb in adverbs_list:
        adverb_cache[adverb]


def analyze_prepositions(prepositions_list):
    for preposition in prepositions_list:
        preposition_cache[preposition]


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
    df.loc[df['pos_'] == 'NOUN', 'text'] = df.loc[df['pos_'] == 'NOUN', 'text'].str.replace('-', '')
    nouns_list = df.loc[(df['pos_'] == 'NOUN'), 'text'].tolist()
    pgetting_nouns = run_in_background(analyze_nouns, nouns_list)

    # trigger verb conjugation for all verbs
    verbs_list = df.loc[(df['pos_'] == 'VERB'), 'text'].tolist()
    pgetting_verbs = run_in_background(analyze_verbs, verbs_list)

    # trigger adjective conjugation for all adjectives
    adjectives_list = df.loc[(df['pos_'] == 'ADJ'), 'text'].tolist()
    pgetting_adjectives = run_in_background(analyze_adjectives, adjectives_list)

    # trigger adverb conjugation for all adverbs
    adverbs_list = df.loc[(df['pos_'] == 'ADV'), 'text'].tolist()
    pgetting_adverbs = run_in_background(analyze_adverbs, adverbs_list)

    # trigger preposition conjugation for all prepositions
    prepositions_list = df.loc[df['pos_'].isin(['CONJ', 'CCONJ', 'SCONJ', 'INTJ', 'ADP', 'X']), 'text'].tolist()
    pgetting_prepositions = run_in_background(analyze_prepositions, prepositions_list)

    # trigger a corrector in the background
    # checks for nouns and verbs are not None

    return df


INPUT_PATH = "./texts/input_5.txt"

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

    elif scheme == "ADJ":
        df.loc[df['pos_'] == scheme,
                 ['highlight', 'color']] = [True, colors_definitions[scheme]]

    elif scheme == "ADV":
        df.loc[df['pos_'] == scheme,
                 ['highlight', 'color']] = [True, colors_definitions[scheme]]

    elif scheme == "PREP":
        df.loc[df['pos_'].isin(['CONJ', 'CCONJ', 'SCONJ', 'INTJ', 'ADP', 'X']),
                 ['highlight', 'color']] = [True, colors_definitions['CONJ']]

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
            style = Style(color=row['color'],
                          bgcolor=colors_definitions["White"],
                          reverse=True,
                          dim=True)
            text.append(f" {row['lemma_']} ", style=style)
            text_width += len(row['lemma_'])
    return text


def generate_rich_analysis(df, group='NOUN', row_nbr=5):
    # map [group: [select part of meaning, select cache, tags]]
    map = {'NOUN': ['nouns', noun_cache, ['NOUN']],
           'ADJ': ['adjectives_or_adverbs', adjective_cache, ['ADJ']],
           'ADV': ['adjectives_or_adverbs', adverb_cache, ['ADV']],
           'PREP': ['examples', preposition_cache, ['CONJ', 'CCONJ', 'SCONJ', 'INTJ', 'ADP', 'X']],
           }
    tables = []
    nouns_list = df.loc[(df['pos_'].isin(map[group][2])), 'text'].tolist()
    nouns_list = list(set(nouns_list))

    cache = map[group][1]

    for element in nouns_list:
        df = cache[element]
        df.fillna(value="None", inplace=True)
        english_text = cache[element][map[group][0]]['english']
        german_text = cache[element][map[group][0]]['german']

        noun_details = cache[element]['noun_details']['english'].split('\n')

        if len(noun_details) > 2 and group == 'NOUN':
            noun_gender = noun_details[2]
        else:
            noun_gender = "None"

        english_text = english_text.split('\n')
        german_text = german_text.split('\n')

        gender_styles = {
            'genus: MASC': colors_definitions['Green'],
            'genus: FEMI': colors_definitions['Red'],
            'genus: NEUT': colors_definitions['Blue']
        }

        style = gender_styles.get(noun_gender, colors_definitions['White'])

        table = Table(title=f"{element}", style=style, header_style=style, title_style=style)
        table.add_column("English", justify="left", style=style, no_wrap=True)
        table.add_column("German", justify="left", style=style,no_wrap=True)
        for eng, ger in zip(english_text[:row_nbr], german_text[:row_nbr]):
            table.add_row(eng, ger)
        tables.append(table)
    return tables


def generate_rich_analysis_verb(df, row_nbr=5):
    tables = []
    verbs_list = df.loc[(df['pos_'] == 'VERB'), 'text'].tolist()
    lemmas_list = df.loc[(df['pos_'] == 'VERB'), 'lemma_'].tolist()

    verbs_list = list(set(verbs_list))
    lemmas_list = list(set(lemmas_list))

    for verb, lemma in zip(verbs_list, lemmas_list):
        df = noun_cache[verb]
        df.fillna(value="None", inplace=True)
        english_text = noun_cache[verb]['verbs']['english']
        german_text = noun_cache[verb]['verbs']['german']

        english_text = english_text.split('\n')
        german_text = german_text.split('\n')

        table = Table(title=f"{verb}")
        table.add_column("English", justify="left", no_wrap=True)
        table.add_column("German", justify="left", no_wrap=True)
        for eng, ger in zip(english_text[:row_nbr], german_text[:row_nbr]):
            table.add_row(eng, ger)
        tables.append(table)
        conj_tables = verb_cache[verb]['indicative_active']
        conj_tables.fillna(value="None", inplace=True)
        table = Table()
        table.add_column("Present", justify="left", no_wrap=False)
        table.add_column("Imperfect", justify="left", no_wrap=False)
        table.add_column("Perfect", justify="left", no_wrap=False)
        table.add_column("Future", justify="left", no_wrap=False)
        if all(val != "None" for val in conj_tables.values):
            table.add_row(conj_tables['Present'],
                          conj_tables['Imperfect'],
                          conj_tables['Perfect'],
                          conj_tables['Future'])
        else:
            conj_tables = verb_cache[lemma]['indicative_active']
            conj_tables.fillna(value="None", inplace=True)
            table.add_row(conj_tables['Present'],
                          conj_tables['Imperfect'],
                          conj_tables['Perfect'],
                          conj_tables['Future'])

        tables.append(table)
    return tables


if __name__ == "__main__":
    df = colorize_text(ANALYZED_TEXT, 'NOUN')
    print(generate_rich_analysis(df)[0])
