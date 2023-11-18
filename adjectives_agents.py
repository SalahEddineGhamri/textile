from color_scheme import colorize_text, colors_definitions
from threading import Thread
from adjectives_table import ADJECTIVES_CACHE
from rich.table import Table
from rich.text import Text, Style
from time import sleep


class AdjectivesAgent(Thread):
    def __init__(self, blackboard):
        super().__init__()
        self.blackboard = blackboard
        self.blackboard["adjectives_rich_text"] = ""
        self.blackboard["adjectives_rich_analysis"] = ""

    def analyze_adjectives(self):
        df = self.blackboard["analyzed_text"]
        adjectives_list = df.loc[(df["pos_"] == "ADJ"), "text"].tolist()
        for adjective in adjectives_list:
            ADJECTIVES_CACHE[adjective]
        ADJECTIVES_CACHE.cache()

    def generate_rich_text(self, width=100):
        df = colorize_text(self.blackboard["analyzed_text"], "ADJ")
        text = Text()
        text.no_wrap = False
        text_width = 0
        for index, row in df.iterrows():
            if row["text"] == "\n":
                text.append("\n")
                text_width = 0
                continue

            if text_width >= width:
                text.append("\n")
                text_width = 0

            if index != 0 and row["pos_"] != "PUNCT" and text_width != 0:
                text.append(" ")
                text_width += 1

            style = Style(color=row["color"])
            text.append(row["text"], style=style)
            text_width += len(row["text"])

            if row["highlight"]:
                # meta
                text.append(" ")
                text_width += 1
                style = Style(
                    color=colors_definitions["Bg"],
                    bgcolor=colors_definitions["White"],
                    dim=True,
                )
                text.append(f" {''.join(row['meta'])} ", style=style)
                text_width += len("".join(row["meta"]))

                # lemma_
                style = Style(
                    color=row["color"],
                    bgcolor=colors_definitions["White"],
                    reverse=True,
                    dim=True,
                )
                text.append(f" {row['lemma_']} ", style=style)
                text_width += len(row["lemma_"])
        self.blackboard["adjectives_rich_text"] = text

    def generate_rich_analysis(self, row_nbr=5):
        df = colorize_text(self.blackboard["analyzed_text"], "ADJ")
        df = df.loc[df["pos_"] == "ADJ"]
        tables = []

        # add more possiblities for hyphen words
        adjectives_list = df.loc[(df["pos_"] == "ADJ"), "text"].tolist()

        # unique values
        adjectives_list = list(set(adjectives_list))

        for element in adjectives_list:
            df = ADJECTIVES_CACHE[element]
            if df is None:
                continue
            df.fillna(value="None", inplace=True)
            english_text = df["adjectives_or_adverbs"]["english"]
            german_text = df["adjectives_or_adverbs"]["german"]

            english_text = english_text.split("\n")
            german_text = german_text.split("\n")

            style = colors_definitions["White"]

            table = Table(
                title=f"{element}", style=style, header_style=style, title_style=style
            )
            table.add_column("English", justify="left", style=style, no_wrap=True)
            table.add_column("German", justify="left", style=style, no_wrap=True)
            for eng, ger in zip(english_text[:row_nbr], german_text[:row_nbr]):
                table.add_row(eng, ger)
            tables.append(table)
        self.blackboard["adjectives_rich_analysis"] = tables

    def run(self):
        while self.blackboard["stages"]["analyzed_input"] != "DONE":
            sleep(0.0001)

        self.blackboard["stages"]["analyzed_adjectives"] = "STARTED"
        ADJECTIVES_CACHE.refresh_cache()
        self.analyze_adjectives()
        ADJECTIVES_CACHE.cache()
        self.blackboard["stages"]["analyzed_adjectives"] = "Analyzed Adjectives!"
        self.generate_rich_text()
        self.blackboard["stages"]["analyzed_adjectives"] = "Generated rich text!"
        self.generate_rich_analysis()
        self.blackboard["stages"]["analyzed_adjectives"] = "Generated rich analysis!"
        self.blackboard["stages"]["analyzed_adjectives"] = "DONE"
