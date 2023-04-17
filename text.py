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
from text_agents import TextAgent

from adverbs_table import AdverbsCache
from adjectives_table import AdjectivesCache
from prepositions_table import PrepositionsCache


class Blackboard:
    def __init__(self, input_path):
        # create a multiprocessing manager
        manager = Manager()
        self.manager = manager.dict()
        self.manager['text'] = None
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

        # get caches
        self.manager['adjective_cache'] = AdjectivesCache()
        self.manager['adverb_cache'] = AdverbsCache()
        self.manager['preposition_cache'] = PrepositionsCache()

        self.manager['stages']['input_read'] = 'STARTED'
        with File(input_path, "r") as f:
            self.manager['text'] = f.getData()
            self.manager['stages']['input_read'] = 'DONE'


class TextAnalyzer:
    def __init__(self, blackboard):
        self.agents = [
            TextAgent(blackboard),
            VerbsAgent(blackboard),
            NounsAgent(blackboard),
            AdjectivesAgent(blackboard),
            AdverbsAgent(blackboard),
            PrepositionsAgent(blackboard),
            AnkiGenerationAgent(blackboard)
        ]

        for agent in self.agents:
            agent.start()

    def join(self):
        for agent in self.agents:
            agent.join()


if __name__ == "__main__":
    blackboard = Blackboard(INPUT_PATH)
    text_analyzer = TextAnalyzer(blackboard.manager)

    while not all(value == 'DONE' for value in blackboard.manager['stages'].values()):
        print(blackboard.manager['stages'])
        sleep(0.1)
