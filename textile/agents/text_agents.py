import spacy
import pandas as pd
from textile.config import colors_definitions
from threading import Thread
from textile.utils import get_logger

def log(msg):
  msg = f"[text_agents] {msg}"
  logger = get_logger()
  logger.info(msg)


class TextAgent(Thread):
    def __init__(self, blackboard):
        super().__init__()
        self.blackboard = blackboard
        self.blackboard["input_rich_text"] = ""

    def analyze(self):
        nlp = spacy.load("de_core_news_sm")
        log("successfully loaded spacy")
        doc = nlp(self.blackboard["text"])
        log("NLP model applied")
        data = []
        for token in doc:
            data.append(
                [
                    token.text,
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
                    token.morph.to_dict(),
                ]
            )

        columns = [
            "text",
            "lemma_",
            "pos_",
            "pos_meaning_",
            "morph_case",
            "morph_gender",
            "morph_number",
            "morph_person",
            "morph_prontype",
            "tag_",
            "dep_",
            "shape_",
            "is_alpha",
            "is_stop",
            "all_morph",
        ]

        self.blackboard["analyzed_text"] = pd.DataFrame(data=data, columns=columns)
        self.blackboard["analyzed_text"]["color"] = colors_definitions["White"]
        self.blackboard["analyzed_text"]["highlight"] = False

        # fill the meta data Case, Gender, Number, Person
        df = self.blackboard["analyzed_text"]
        df["meta"] = df["morph_case"].apply(lambda x: x.copy())
        df.apply(lambda row: row["meta"].extend(row["morph_gender"]), axis=1)
        df.apply(lambda row: row["meta"].extend(row["morph_number"]), axis=1)
        df.apply(lambda row: row["meta"].extend(row["morph_person"]), axis=1)
        self.blackboard["analyzed_text"] = df
        log("analyzed text")

    def run(self):
        self.blackboard["stages"]["analyzed_input"] = "STARTED"
        self.analyze()
        self.blackboard["stages"]["analyzed_input"] = "DONE"
