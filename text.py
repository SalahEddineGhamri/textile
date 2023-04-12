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
from multiprocessing import Process, Manager
from rich.table import Table
from time import sleep
from anki_generator import AnkiGenerator, VerbNote, NounNote
from config import NOUNS_CACHE_FILE, INPUT_PATH
import re

# TODO: if noun not found try lemma and try decomposing it <corrector>


def extract_info(noun, english, german):

    english = english.split('\n')
    german = german.split('\n')

    full_noun = []
    for line in german:
        pattern = r'((?:der|die|das)\s+)(\w+)\s+pl.:\s+die\s+(\w+)'
        match = re.match(pattern, line)
        if match:
            full_noun.append(match.group(1) + " " + match.group(2))

    # extract plural forms of German nouns starting with "die"
    plural = []
    for line in german:
        match = re.match(r'die\s+(\w+)\s+pl.:\s+die\s+(\w+)', line)
        if match:
            plural.append(match.group(2))

    full_noun = list(set(full_noun))
    plural = list(set(plural))
    # combine into a dictionary
    return {
        'Noun': noun,
        'English': english[:2],
        'FullNoun': full_noun,
        'Plural': plural,
    }


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

# TODO: must be joined
def run_in_background(func, *args, **kwargs):
    process = Process(target=func, args=args, kwargs=kwargs)
    process.start()


def split_hyphenated_string(s):
    words = s.split('-')
    result = []
    for i, word in enumerate(words):
        if i == 0:
            result.append(word.capitalize())
        elif i == len(words) - 1:
            result.append(' ' + word.capitalize())
            result.append(''.join(words).capitalize())
        else:
            result.append(' ' + word.capitalize())
    return result

class Blackboard:
    def __init__(self, input_path):
        # create a multiprocessing manager
        manager = Manager()
        self.manager = manager.dict()

        self.text = ""
        # dataframe
        self.manager['analyzed_text'] = None

        # caches
        self.noun_cache = NounsCache()
        self.verb_cache = VerbsCache()
        self.adjective_cache = AdjectivesCache()
        self.adverb_cache = AdverbsCache()
        self.preposition_cache = PrepositionsCache()

        stages = manager.dict()
        stages['input_read'] = None
        stages['analyzed_input'] = None
        stages['analyzed_nouns'] = None
        stages['analyzed_verbs'] = None
        stages['analyzed_adjectives'] = None
        stages['analyzed_adverbs'] = None
        stages['analyzed_prepositions'] = None
        stages['correction'] = 'DONE'
        stages['anki_generation'] = 'DONE'

        # stages: None - 'started' - 'done'
        self.manager['stages'] = stages

        self.read_input(input_path)
        deck_name = input_path.split('/')[-1]
        self.anki_generator = AnkiGenerator(deck_name)

    def read_input(self, input_path):
        self.manager['stages']['input_read'] = 'STARTED'
        with File(input_path, "r") as f:
            self.text = f.getData()
            self.manager['stages']['input_read'] = 'DONE'

    def analyze_verbs(self, cache):
        self.manager['stages']['analyzed_verbs'] = 'STARTED'
        verbs_list = self.manager['analyzed_text'].loc[(self.manager['analyzed_text']['pos_'] == 'VERB'), 'text'].tolist()
        for verb in verbs_list:
            cache[verb]
        cache.cache()
        self.manager['stages']['analyzed_verbs'] = 'DONE'

    def analyze_nouns(self, cache):
        self.manager['stages']['analyzed_nouns'] = 'STARTED'
        # trigger meaning parsing for all nouns
        df = self.manager['analyzed_text']
        nouns_list = df.loc[(df['pos_'] == 'NOUN'), 'text'].tolist()
        # add more possiblities for hyphen words
        nouns_with_hyphen = df.loc[df['text'].str.contains('-'), 'text'].tolist()
        nouns_with_hyphen = [word for noun in nouns_with_hyphen for word in split_hyphenated_string(noun)]
        for noun in nouns_list+nouns_with_hyphen:
            cache[noun]
        cache.cache()
        self.manager['stages']['analyzed_nouns'] = 'DONE'

    def analyze_adjectives(self, cache):
        self.manager['stages']['analyzed_adjectives'] = 'STARTED'
        adjectives_list = self.manager['analyzed_text'].loc[(self.manager['analyzed_text']['pos_'] == 'ADJ'), 'text'].tolist()
        for adjective in adjectives_list:
            cache[adjective]
        cache.cache()
        self.manager['stages']['analyzed_adjectives'] = 'DONE'

    def analyze_adverbs(self, cache):
        self.manager['stages']['analyzed_adverbs'] = 'STARTED'
        adverbs_list = self.manager['analyzed_text'].loc[(self.manager['analyzed_text']['pos_'] == 'ADV'), 'text'].tolist()
        for adverb in adverbs_list:
            cache[adverb]
        cache.cache()
        self.manager['stages']['analyzed_adverbs'] = 'DONE'

    def analyze_prepositions(self, cache):
        self.manager['stages']['analyzed_prepositions'] = 'STARTED'
        prepos_ = ['CONJ', 'CCONJ', 'SCONJ', 'INTJ', 'ADP', 'X']
        prepositions_list = self.manager['analyzed_text'].loc[self.manager['analyzed_text']['pos_'].isin(prepos_), 'text'].tolist()
        for preposition in prepositions_list:
            cache[preposition]
        cache.cache()
        self.manager['stages']['analyzed_prepositions'] = 'DONE'

    def anki_generation(self, noun_cache):
        # anki generation will start if all stages all done
        # TODO: max loop exit with failure
        while not all(value == 'DONE' for value in self.manager['stages'].values()):
            sleep(0.001)

        self.manager['stages']['correction'] = 'STARTED'
        nouns = self.manager['analyzed_text'].loc[(self.manager['analyzed_text']['pos_'] == 'NOUN'), 'text'].tolist()
        nouns = list(set(nouns))
        for noun in nouns:
            nc = noun_cache[noun]
            if nc is not None:
                if nc['nouns']['english'] != "None":
                    print(self.manager['analyzed_text'].loc[(self.manager['analyzed_text']['text'] == noun)])
                    print(extract_info(noun,nc['nouns']['english'], nc['nouns']['german']))
        self.manager['stages']['correction'] = 'DONE'

        """
        # loop all nouns and verbs
        nouns_df = self.manager['analyzed_text'].loc[(self.manager['analyzed_text']['pos_'] == 'NOUN')]
        print(nouns_df)
        #fields = ['Noun', 'English', 'FullNoun', 'Plural']
        #self.anki_generator.add_note()

        verbs_df = self.manager['analyzed_text'].loc[(self.manager['analyzed_text']['pos_'] == 'VERB')]
        #fields = ['Verb', 'English', 'PresentPastParticip']
        #self.anki_generator.add_note()

        self.anki_generator.add_note()
        self.manager['stages']['correction'] = 'DONE'
        """


    def analyze_text(self):
        self.manager['stages']['analyzed_input'] = 'STARTED'
        nlp = spacy.load("de_core_news_sm")
        doc = nlp(self.text)
        data = []
        for token in doc:
            data.append([token.text,
                         token.lemma_,
                         token.pos_,
                         spacy.explain(token.pos_),
                         token.morph.get("Case"),
                         token.morph.get("Gender"),
                         token.morph.get("Number"),
                         token.morph.get("Person"),
                         token.morph.get("PronType"),
                         token.tag_,
                         token.dep_,
                         token.shape_,
                         token.is_alpha,
                         token.is_stop,
                         token.morph.to_dict()])

        columns = ['text',
                   'lemma_',
                   'pos_',
                   'pos_meaning_',
                   'morph_case',
                   'morph_gender',
                   'morph_number',
                   'morph_person',
                   'morph_prontype',
                   'tag_',
                   'dep_',
                   'shape_',
                   'is_alpha',
                   'is_stop',
                   'all_morph']

        self.manager['analyzed_text'] = pd.DataFrame(data=data, columns=columns)
        self.manager['analyzed_text']['color'] = colors_definitions['White']
        self.manager['analyzed_text']['highlight'] = False


        # fill the meta data Case, Gender, Number, Person
        df = self.manager['analyzed_text']
        df['meta'] = df['morph_case'].apply(lambda x: x.copy())
        df.apply(lambda row: row['meta'].extend(row['morph_gender']), axis=1)
        df.apply(lambda row: row['meta'].extend(row['morph_number']), axis=1)
        df.apply(lambda row: row['meta'].extend(row['morph_person']), axis=1)
        self.manager['analyzed_text'] = df
        self.manager['stages']['analyzed_input'] = 'DONE'

        run_in_background(self.analyze_nouns, self.noun_cache)
        run_in_background(self.analyze_verbs, self.verb_cache)
        run_in_background(self.analyze_adjectives, self.adjective_cache)
        run_in_background(self.analyze_adverbs, self.adverb_cache)
        run_in_background(self.analyze_prepositions, self.preposition_cache)

        #run_in_background(self.corrector)
        run_in_background(self.anki_generation, self.noun_cache)

    def get_analysed_text(self):
        return self.manager['analyzed_text']


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


# build rich text with colors
def generate_rich_text(df, width=30):
    text = Text()
    text.no_wrap = False
    text_width = 0
    for index, row in df.iterrows():
        print(row['color'])
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


def generate_rich_analysis(df, blackboard, group='NOUN', row_nbr=5):
    # map [group: [select part of meaning, select cache, tags]]
    map = {'NOUN': ['nouns', blackboard.noun_cache, ['NOUN']],
           'ADJ': ['adjectives_or_adverbs', blackboard.adjective_cache, ['ADJ']],
           'ADV': ['adjectives_or_adverbs', blackboard.adverb_cache, ['ADV']],
           'PREP': ['examples', blackboard.preposition_cache, ['CONJ', 'CCONJ', 'SCONJ', 'INTJ', 'ADP', 'X']],
           }
    tables = []
    nouns_list = df.loc[(df['pos_'].isin(map[group][2])), 'text'].tolist()
    # add more possiblities for hyphen words
    nouns_with_hyphen = df.loc[df['text'].str.contains('-'), 'text'].tolist()
    nouns_with_hyphen = [word for noun in nouns_with_hyphen for word in split_hyphenated_string(noun)]

    cache = map[group][1]

    # unique values
    nouns_list = list(set(nouns_list + nouns_with_hyphen))

    # TODO: more check on the none values
    for element in nouns_list:
        df = cache[element]
        if df is None:
            continue
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


def generate_rich_analysis_verb(df, blackboard, row_nbr=5):
    tables = []
    verbs_list = df.loc[(df['pos_'] == 'VERB'), 'text'].tolist()
    lemmas_list = df.loc[(df['pos_'] == 'VERB'), 'lemma_'].tolist()

    verbs_list = list(set(verbs_list))
    lemmas_list = list(set(lemmas_list))

    for verb, lemma in zip(verbs_list, lemmas_list):
        df = blackboard.noun_cache[verb]
        df.fillna(value="None", inplace=True)
        english_text = blackboard.noun_cache[verb]['verbs']['english']
        german_text = blackboard.noun_cache[verb]['verbs']['german']

        english_text = english_text.split('\n')
        german_text = german_text.split('\n')

        table = Table(title=f"{verb}")
        table.add_column("English", justify="left", no_wrap=True)
        table.add_column("German", justify="left", no_wrap=True)
        for eng, ger in zip(english_text[:row_nbr], german_text[:row_nbr]):
            table.add_row(eng, ger)
        tables.append(table)
        conj_tables = blackboard.verb_cache[verb]['indicative_active']
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
            conj_tables = blackboard.verb_cache[lemma]['indicative_active']
            conj_tables.fillna(value="None", inplace=True)
            table.add_row(conj_tables['Present'],
                          conj_tables['Imperfect'],
                          conj_tables['Perfect'],
                          conj_tables['Future'])

        tables.append(table)
    return tables


if __name__ == "__main__":
    # TODO: work on this
    blackboard = Blackboard(INPUT_PATH)
    blackboard.read_input(INPUT_PATH)
    blackboard.analyze_text()
    ANALYZED_TEXT = blackboard.get_analysed_text()

    noun_cache = blackboard.noun_cache
    verb_cache = blackboard.verb_cache
    adjective_cache = blackboard.adjective_cache
    adverb_cache = blackboard.adverb_cache
    preposition_cache = blackboard.preposition_cache

    TEXT_WIDTH = 90
    df = colorize_text(ANALYZED_TEXT, 'NOUN')
    #print(generate_rich_analysis(df, blackboard)[0])
    #print(generate_rich_text(colorize_text(ANALYZED_TEXT, "NOUN"), width=TEXT_WIDTH))
    #print(generate_rich_analysis(ANALYZED_TEXT, blackboard))

    while not all(value == 'DONE' for value in blackboard.manager['stages'].values()):
        print(blackboard.manager['stages'])
        sleep(1)
