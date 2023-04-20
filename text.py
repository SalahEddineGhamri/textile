from file_io import File
from rich import print
from time import sleep
from config import INPUT_PATH
from anki_generation_agent import AnkiGenerationAgent
from verbs_agents import VerbsAgent
from nouns_agents import NounsAgent
from adjectives_agents import AdjectivesAgent
from adverbs_agents import AdverbsAgent
from prepositions_agents import PrepositionsAgent
from text_agents import TextAgent


# TODO: add protection with locks
# TODO: change this into a mutable object
# TODO: add methods to store solutions status and read problem
class Blackboard:
    def __init__(self, input_path):
        self.manager = dict()
        stages = dict()
        self.manager['text'] = None
        self.manager['analyzed_text'] = None

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
