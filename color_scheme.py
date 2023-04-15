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


# apples the colorscheme
def colorize_text(df, scheme=None):
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
        df.loc[(df['pos_'] == 'NOUN') & (df['morph_gender'].apply(lambda x: x == ['Masc'])),
               'color'] = colors_definitions["Green"]
        df.loc[(df['pos_'] == 'NOUN') & (df['morph_gender'].apply(lambda x: x == ['Fem'])),
               'color'] = colors_definitions["Red"]
        df.loc[(df['pos_'] == 'NOUN') & (df['morph_gender'].apply(lambda x: x == ['Neut'])),
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
