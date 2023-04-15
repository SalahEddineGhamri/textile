import spacy
import pandas as pd
from file_io import File
from rich import print
from multiprocessing import Manager
from time import sleep
from config import INPUT_PATH
from anki_generation_agent import AnkiGenerationAgent
from color_scheme import colors_definitions, colorize_text
from verbs_agents import VerbsAgent
from nouns_agents import NounsAgent
from adjectives_agents import AdjectivesAgent
from adverbs_agents import AdverbsAgent
from prepositions_agents import PrepositionsAgent


# TODO: seperate a blackboard from the text analyzer
# - blackboard contains the input - solution - status
# - text analyzer is a manager for all agents
# TODO: text analyzer channels the status
# TODO: pass the status to the tui.
# TODO: fix the issue of the printing from nouns
# TODO: an analyzed text should never trigger scrapping


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

        stages = manager.dict()
        stages['input_read'] = None
        stages['analyzed_input'] = None
        stages['analyzed_nouns'] = None
        stages['analyzed_verbs'] = None
        stages['analyzed_adjectives'] = None
        stages['analyzed_adverbs'] = None
        stages['analyzed_prepositions'] = None
        stages['anki_generation'] = 'DONE'

        # stages: None - 'started' - 'done'
        self.manager['stages'] = stages

        # Agents
        self.anki_generation_agent = AnkiGenerationAgent(self.manager)
        self.anki_generation_agent.start()

        self.verbs_agent = VerbsAgent(self.manager)
        self.verbs_agent.start()

        self.nouns_agent = NounsAgent(self.manager)
        self.nouns_agent.start()

        self.adjectives_agent = AdjectivesAgent(self.manager)
        self.adjectives_agent.start()

        self.adverbs_agent = AdverbsAgent(self.manager)
        self.adverbs_agent.start()

        self.prepositions_agent = PrepositionsAgent(self.manager)
        self.prepositions_agent.start()

        self.read_input(input_path)

    def read_input(self, input_path):
        self.manager['stages']['input_read'] = 'STARTED'
        with File(input_path, "r") as f:
            self.text = f.getData()
            self.manager['stages']['input_read'] = 'DONE'

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

    def get_analysed_text(self):
        return self.manager['analyzed_text']


if __name__ == "__main__":
    # TODO: work on this
    blackboard = Blackboard(INPUT_PATH)
    blackboard.read_input(INPUT_PATH)
    blackboard.analyze_text()
    ANALYZED_TEXT = blackboard.get_analysed_text()

    TEXT_WIDTH = 90
    df = colorize_text(ANALYZED_TEXT, 'NOUN')

    while not all(value == 'DONE' for value in blackboard.manager['stages'].values()):
        print(blackboard.manager['stages'])
        sleep(0.1)
