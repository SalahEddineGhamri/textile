from textile.utils import File
from rich import print
from time import sleep
from textile.config import INPUT_PATH


# import agents
from textile.agents import (
    AnkiGenerationAgent,
    VerbsAgent,
    NounsAgent,
    AdjectivesAgent,
    AdverbsAgent,
    PrepositionsAgent,
    TextAgent
)

"""
SCM: is a componant that reads the blckboard
it reads the stages and outputs and richlog text
the output of the scm changes only if stages changes
it surveil the stages variable

output: [Nouns: generating rich text] [verbs] [adjective]
        red                           green   green
"""

class Blackboard:
    def __init__(self, input_path):
        self.manager = dict()
        stages = dict()
        self.manager["text"] = None
        self.manager["analyzed_text"] = None

        # stages represent textile state
        stages["input_read"] = None
        stages["analyzed_input"] = None
        stages["analyzed_nouns"] = None
        stages["analyzed_verbs"] = None
        stages["analyzed_adjectives"] = None
        stages["analyzed_adverbs"] = None
        stages["analyzed_prepositions"] = None
        stages["anki_generation"] = "DONE"

        self.manager["stages"] = stages

        self.manager["stages"]["input_read"] = "STARTED"
        with File(input_path, "r") as f:
            self.manager["text"] = f.getData()
            self.manager["stages"]["input_read"] = "DONE"


class TextAnalyzer:
    def __init__(self, blackboard):
        self.agents = [
            TextAgent(blackboard),
            VerbsAgent(blackboard),
            NounsAgent(blackboard),
            AdjectivesAgent(blackboard),
            AdverbsAgent(blackboard),
            PrepositionsAgent(blackboard),
            AnkiGenerationAgent(blackboard),
        ]

        for agent in self.agents:
            agent.start()

    def join(self):
        for agent in self.agents:
            agent.join()


if __name__ == "__main__":
    blackboard = Blackboard(INPUT_PATH)
    text_analyzer = TextAnalyzer(blackboard.manager)

    while not all(value == "DONE" for value in blackboard.manager["stages"].values()):
        print(blackboard.manager["stages"])
        sleep(0.1)
