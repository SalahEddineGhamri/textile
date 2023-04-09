import spacy
import pandas as pd
from rich.text import Text, Style
from file_io import File
from rich import print

# TODO: fill meta in the analysis
# TODO: in noun scheme we have the color showing gender
#     : - green: maschuline
#     : - red: feminine
#     : - blue: Neutrom

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


def analyze_text(text):
    """
    intensive function should be called
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
    return df


INPUT_PATH = "./texts/input_3.txt"

# this is our blackboard
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
# TODO: revize the width
def generate_rich_text(df, entry=None, width=30):
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


if __name__ == "__main__":
    print(ANALYZED_TEXT)
    df = colorize_text(ANALYZED_TEXT, 'NOUN')
    # print(df)
    # TEXT = generate_rich_text(df, 90)
    # print(TEXT)
