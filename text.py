import spacy
import pandas as pd
from rich.text import Text


def analyze_text(text):
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

    return pd.DataFrame(data=data, columns=['text',
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


# colors dict
colors_definitions = {
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


# colorize based of entry
# if entry is None colorize following default colors_definitions
def colorize_text(df, entry=None):
    '''
    for each pos_ fill the color
    '''
    df['color'] = df.apply(lambda x: colors_definitions[x['pos_']], axis=1)
    return df


# build rich text with colors
def generate_rich_text(df, entry=None, width=100):
    text = Text()
    text_width = 0
    for index, row in df.iterrows():
        if text_width >= width:
            text.append("\n")
            text_width = 0

        if index != 0 and row['pos_'] != 'PUNCT' and text_width != 0:
            text.append(" ")
            text_width += 1

        text.append(row['text'], style=row['color'])
        text_width += len(row['text'])
    text.no_wrap = False
    return text
