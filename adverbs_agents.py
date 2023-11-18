from color_scheme import colorize_text, colors_definitions
from threading import Thread
from rich.table import Table
from rich.text import Text, Style
from time import sleep
from adverbs_table import ADVERBS_CACHE


class AdverbsAgent(Thread):
  def __init__(self, blackboard):
    super().__init__()
    self.blackboard = blackboard
    self.blackboard["adverbs_rich_text"] = ""
    self.blackboard["adverbs_rich_analysis"] = ""

  def analyze(self):
    df = self.blackboard["analyzed_text"]
    adverbs_list = df.loc[(df["pos_"] == "ADV"), "text"].tolist()
    for adverb in adverbs_list:
      ADVERBS_CACHE[adverb]

  def generate_rich_text(self, width=100):
    df = colorize_text(self.blackboard["analyzed_text"], "ADV")
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
    self.blackboard["adverbs_rich_text"] = text

  def generate_rich_analysis(self, row_nbr=5):
    df = colorize_text(self.blackboard["analyzed_text"], "ADV")
    df = df.loc[df["pos_"] == "ADV"]
    tables = []

    # add more possiblities for hyphen words
    adverbs_list = df.loc[(df["pos_"] == "ADV"), "text"].tolist()

    # unique values
    adverbs_list = list(set(adverbs_list))

    for element in adverbs_list:
      df = ADVERBS_CACHE[element]
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
    self.blackboard["adverbs_rich_analysis"] = tables

  def run(self):
    while self.blackboard["stages"]["analyzed_input"] != "DONE":
      sleep(0.0001)

    self.blackboard["stages"]["analyzed_adverbs"] = "STARTED"
    ADVERBS_CACHE.refresh_cache()
    self.analyze()
    ADVERBS_CACHE.cache()
    self.blackboard["stages"]["analyzed_adverbs"] = "Analyzed Adverbs!"
    self.generate_rich_text()
    self.blackboard["stages"]["analyzed_adverbs"] = "Generated rich text!"
    self.generate_rich_analysis()
    self.blackboard["stages"]["analyzed_adverbs"] = "Generated rich analysis!"
    self.blackboard["stages"]["analyzed_adverbs"] = "DONE"
