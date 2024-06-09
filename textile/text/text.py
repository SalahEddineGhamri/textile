from textile.utils import File
from rich import print
from time import sleep
from textile.config import INPUT_PATH, colors_definitions
from rich.text import Text, Style
from time import sleep


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

def style(type_name):
  if type_name == "busy":
    return Style(
        color=colors_definitions["Bg"],
        bgcolor=colors_definitions["Red"],
        reverse=True,
        dim=True,
        encircle=True
    )
  elif type_name == "done":
    return Style(
        color=colors_definitions["Bg"],
        bgcolor=colors_definitions["Green"],
        reverse=True,
        dim=True
    )


def generate_sequence():
    triangle_symbols = ["◯", "◔", "◑", "◕", "●"]
    count = 0
    while True:
        sleep(0.1)
        yield triangle_symbols[count % len(triangle_symbols)]
        count += 1


class Blackboard:
    seq = generate_sequence()
    def __init__(self, input_path):
        self.manager = dict()
        stages = dict()
        self.manager["text"] = None
        self.manager["analyzed_text"] = None

        self.status_text = Text()
        self.status_text.no_wrap = True

        # stages represent textile state
        stages["input_read"] = None
        stages["analyzed_input"] = None
        stages["analyzed_nouns"] = None
        stages["analyzed_verbs"] = None
        stages["analyzed_adjectives"] = None
        stages["analyzed_adverbs"] = None
        stages["analyzed_prepositions"] = None
        stages["anki_generation"] = None

        self.manager["stages"] = stages


        self.manager["stages"]["input_read"] = "STARTED"
        with File(input_path, "r") as f:
            self.manager["text"] = f.getData()
            self.manager["stages"]["input_read"] = "DONE"

    def stages(self):
        stl = None
        stages = self.manager["stages"]
        self.status_text.__init__()
        for key, value in stages.items():
            if "analyzed" in key:
              name = key.replace("analyzed_", "")
            else:
              name = key.replace("_", " ")

            if value != "DONE" and value is not None:
              stl = style("busy")
              name += " " + next(self.seq)
            elif value == "DONE":
              stl = style("done")
              name += " " + "●"
            elif value is None:
              name += " " + "◯"

            self.status_text.append(name, stl)
            self.status_text.append(" ")
        return self.status_text


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
        sleep(0.01)
