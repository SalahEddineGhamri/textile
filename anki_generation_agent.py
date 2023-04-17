from multiprocessing import Process
from time import sleep
from anki_generator import AnkiGenerator, VerbNote, NounNote, GeneralNote
from config import INPUT_PATH, ANKI_PATH
from nouns_table import NOUN_CACHE
from verbs_table import VERBS_MEANING_CACHE, VERBS_CONJUGATION_CACHE
from adjectives_table import AdjectivesCache
from adverbs_table import AdverbsCache
from prepositions_table import PrepositionsCache
from nouns_agents import split_hyphenated_string


def extract_info(noun, noun_details):
    # i puted it in english to save form
    details = noun_details['english']
    if details != 'None' and details is not None:
        details = details.split('\n')

        article = details[0].split(':')[1].strip()
        word = details[1].split(':')[1].strip()
        plural = details[3].split(':')[1].strip()
        meaning = details[4].split(':')[1].strip()

        return {
            'Noun': noun,
            'English': meaning,
            'FullNoun': article + " " + word,
            'Plural': plural,
        }
    else:
        return {
            'Noun': "",
            'English': "",
            'FullNoun': "",
            'Plural': "",
        }


def generate_html_table(column1, column2, column3):
    # Check that all inputs are strings
    if not all(isinstance(col, str) for col in [column1, column2, column3]):
        return None

    rows1 = column1.split('\n')
    rows2 = column2.split('\n')
    rows3 = column3.split('\n')

    # Get the maximum number of rows in the three columns
    max_rows = max(len(rows1), len(rows2), len(rows3))

    # Fill in empty rows if necessary
    rows1 += [''] * (max_rows - len(rows1))
    rows2 += [''] * (max_rows - len(rows2))
    rows3 += [''] * (max_rows - len(rows3))

    # Generate the HTML table
    html = '<table>'
    for row1, row2, row3 in zip(rows1, rows2, rows3):
        html += f'<tr><td style="border-right: 1px solid red; text-align: left;">{row1}</td> \
                      <td style="border-right: 1px solid red; text-align: left;">{row2}</td> \
                      <td style="text-align: left;">{row3}</td></tr>'
    html += '</table>'
    return html


class AnkiGenerationAgent(Process):
    def __init__(self, blackboard):
        super().__init__()
        self.blackboard = blackboard
        deck_name = INPUT_PATH.split('/')[-1].split(".")[0]
        self.anki_generator = AnkiGenerator(deck_name)
        self.noun_cache = NOUN_CACHE
        self.verb_meaning_cache = VERBS_MEANING_CACHE
        self.verb_conjugation_cache = VERBS_CONJUGATION_CACHE
        self.adjective_cache = blackboard['adjective_cache']
        self.adverb_cache = blackboard['adverb_cache']
        self.preposition_cache = blackboard['preposition_cache']


    def add_nouns(self):
        df = self.blackboard['analyzed_text'].loc[(self.blackboard['analyzed_text']['pos_'] == 'NOUN')]

        # add more possiblities for hyphen words
        nouns_with_hyphen = df.loc[df['text'].str.contains('-'), 'text'].drop_duplicates().tolist()
        nouns_without_hyphen = df.loc[~df['text'].str.contains('-'), 'text'].drop_duplicates().tolist()
        nouns_with_hyphen = [word for noun in nouns_with_hyphen for word in split_hyphenated_string(noun)]

        nouns = nouns_without_hyphen + nouns_with_hyphen

        for noun in nouns:
            nc = self.noun_cache[noun]
            if nc is not None:
                if nc['nouns']['english'] != "None" and nc['noun_details'][0] != 'None':
                    inputs = list(extract_info(noun, nc['noun_details']).values())
                    if all(inputs) != '':
                        anki_noun_note = NounNote(inputs)
                        self.anki_generator.add_note(anki_noun_note)

    def add_verbs(self):
        text = self.blackboard['analyzed_text']
        verbs = text.loc[(text['pos_'] == 'VERB'), 'text'].tolist()
        verbs_lemma = text.loc[(text['pos_'] == 'VERB'), 'lemma_'].tolist()
        verbs = list(zip(verbs, verbs_lemma))
        verbs = list(set(verbs))
        for verb, lemma in verbs:
            meaning = ""
            nc = self.verb_meaning_cache[verb]
            if nc is not None:
                if nc['verbs']['english'] != "None":
                    meaning = " ".join(nc['verbs']['english'].split('\n')[:3])
            else:
                nc = self.verb_meaning_cache[lemma]
                if nc is not None:
                    if nc['verbs']['english'] != "None":
                        meaning = " ".join(nc['verbs']['english'].split('\n')[:3])

            vc = self.verb_conjugation_cache[verb]
            if vc is not None:
                column1 = vc['indicative_active']['Present']
                column2 = vc['indicative_active']['Imperfect']
                column3 = vc['indicative_active']['Perfect']
                presentpastperfect = generate_html_table(column1, column2, column3)
                if presentpastperfect is not None:
                    inputs = [verb, meaning, presentpastperfect]
                    anki_verb_note = VerbNote(inputs)
                    self.anki_generator.add_note(anki_verb_note)

    def add_else(self):
        df = self.blackboard['analyzed_text']
        # adjectives
        words = df.loc[(df['pos_'] == 'ADJ'), 'text']
        words = words.drop_duplicates()
        words = words.tolist()
        for word in words:
            nc = self.adjective_cache[word]
            if nc is not None:
                english_text = str(nc['adjectives_or_adverbs']['english'])
                german_text = str(nc['adjectives_or_adverbs']['german'])

                inputs = [word, english_text.replace('\n', '<br>'), german_text.replace('\n', '<br>')]
                if all(inputs) != '':
                    anki_note = GeneralNote(inputs)
                    self.anki_generator.add_note(anki_note)

        # adverbs
        words = df.loc[(df['pos_'] == 'ADV'), 'text']
        words = words.drop_duplicates()
        words = words.tolist()
        for word in words:
            nc = self.adverb_cache[word]
            if nc is not None:
                english_text = str(nc['adjectives_or_adverbs']['english'])
                german_text = str(nc['adjectives_or_adverbs']['german'])
                inputs = [word, english_text.replace('\n', '<br>'), german_text.replace('\n', '<br>')]
                if all(inputs) != '':
                    anki_note = GeneralNote(inputs)
                    self.anki_generator.add_note(anki_note)

        # prepositions
        words = df.loc[df['pos_'].isin(['CONJ', 'CCONJ', 'SCONJ', 'INTJ', 'ADP', 'X']), 'text']
        words = words.drop_duplicates()
        words = words.tolist()
        for word in words:
            nc = self.preposition_cache[word]
            if nc is not None:
                english_text = str(nc['adjectives_or_adverbs']['english'])
                german_text = str(nc['adjectives_or_adverbs']['german'])
                inputs = [word, english_text.replace('\n', '<br>'), german_text.replace('\n', '<br>')]
                if all(inputs) != '':
                    anki_note = GeneralNote(inputs)
                    self.anki_generator.add_note(anki_note)


    def save_to_file(self):
        self.anki_generator.save(ANKI_PATH)

    def run(self):
        while not all(value == 'DONE' for value in self.blackboard['stages'].values()):
            # this will break the pipe
            sleep(0.001)

        self.blackboard['stages']['anki_generation'] = 'STARTED'
        self.add_nouns()
        self.blackboard['stages']['anki_generation'] = 'Nouns added!'
        self.add_verbs()
        self.blackboard['stages']['anki_generation'] = 'Verbs added!'
        self.add_else()
        self.blackboard['stages']['anki_generation'] = 'Adjectives/Adverbs/Prepostion added!'
        self.save_to_file()
        self.blackboard['stages']['anki_generation'] = 'Saved to file!'
        self.blackboard['stages']['anki_generation'] = 'DONE'
