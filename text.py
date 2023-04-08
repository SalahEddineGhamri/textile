import spacy
import pandas as pd
from rich.text import Text, Style
from file_io import File
from rich import print

# TODO: introduce colorschems
# TODO: in noun scheme we have the color showing gender
#     : - green: maschuline
#     : - red: feminine
#     : - blue: Neutrom
# TODO: we have under blue line for accusative or red for dative.


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
    TODO: intensive function should be called
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


INPUT_PATH = "./texts/input_3.txt"
ANALYZED_TEXT = analyze_text(read_input())


# colorize dataframe
def get_colorized_dataframe(scheme=None):
    return colorize_text(ANALYZED_TEXT, scheme=scheme)


# colors dict
# TODO: move color definion to schemes.py where all colors are defined
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


def colorize_text(df, scheme=None):
    '''
    for each pos_ fill the color
    '''
    df['color'] = colors_definitions['White']
    df['reversed'] = False
    df['meta'] = ""
    if scheme == "VERB":
        df.loc[df['pos_'] == scheme, 'color'] = colors_definitions[scheme]
        df.loc[df['pos_'] == "AUX", 'color'] = colors_definitions[scheme]
        df.loc[df['pos_'] == scheme, 'reversed'] = True
        df.loc[df['pos_'] == "AUX", 'reversed'] = True
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
        # reversed
        df.loc[(df['pos_'] == 'NOUN'), 'reversed'] = True
        df.loc[(df['pos_'] == 'NOUN'), 'meta'] = df.loc[(df['pos_'] == 'NOUN'), 'lemma_']
    else:
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

        style = Style(color=row['color'])

        text_string = row['text']
        text.append(text_string, style=style)
        text_width += len(row['text'])

        # style for meta only
        if row['meta']:
            text.append(" ")
            text_width += 1
            # style for morph case
            if row['morph_case'] == ['Acc']:
                style = Style(color=colors_definitions["Bg"],
                              bgcolor=colors_definitions["White"],
                              reverse=False,
                              dim=True)
                text.append("Acc", style=style)
                text_width += 3
            if row['morph_case'] == ['Dat']:
                style = Style(color=colors_definitions["Bg"],
                              bgcolor=colors_definitions["White"],
                              reverse=False,
                              dim=True)
                text.append("Dat", style=style)
                text_width += 3

            if row['morph_number'] == ['Plur']:
                style = Style(color=colors_definitions["Bg"],
                              bgcolor=colors_definitions["White"],
                              reverse=False,
                              dim=True)
                text.append("Plur", style=style)
                text_width += 4


            text.append("|")
            text_width += 1
            style = Style(color=row['color'],
                          bgcolor=None,
                          reverse=row['reversed'],
                          bold=False,
                          italic=True,
                          dim=True)
            text.append(f" {row['meta']} ", style=style)
            text_width += len(row['meta'])

        text_width += len(row['text'])
    text.no_wrap = False
    return text


if __name__ == "__main__":
    df = get_colorized_dataframe('NOUN')
    print(df)
    #TEXT = generate_rich_text(df, 90)
    #print(TEXT)
