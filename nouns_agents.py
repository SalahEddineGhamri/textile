from color_scheme import colorize_text, colors_definitions
from threading import Thread
from rich.table import Table
from rich.text import Text, Style
from time import sleep
from nouns_table import NOUN_CACHE


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


class NounsAgent(Thread):
    def __init__(self, blackboard):
        super().__init__()
        self.blackboard = blackboard
        self.blackboard['nouns_rich_text'] = ""
        self.blackboard['nouns_rich_analysis'] = ""

    def analyze_nouns(self):
        # trigger meaning parsing for all nouns
        df = self.blackboard['analyzed_text']
        df = df.loc[df['pos_'] == 'NOUN']
        # add more possiblities for hyphen words
        nouns_with_hyphen = df.loc[df['text'].str.contains('-'), 'text'].tolist()
        nouns_without_hyphen = df.loc[~df['text'].str.contains('-'), 'text'].tolist()
        nouns_with_hyphen = [word for noun in nouns_with_hyphen for word in split_hyphenated_string(noun)]
        nouns_list = list(set(nouns_without_hyphen + nouns_with_hyphen))
        for noun in nouns_list:
            NOUN_CACHE[noun]

    def generate_rich_text(self, width=100):
        df = colorize_text(self.blackboard['analyzed_text'], "NOUN")
        text = Text()
        text.no_wrap = False
        text_width = 0
        for index, row in df.iterrows():
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
        self.blackboard['nouns_rich_text'] = text

    def generate_rich_analysis(self, row_nbr=5):
        df = colorize_text(self.blackboard['analyzed_text'], "NOUN")
        df = df.loc[df['pos_'] == 'NOUN']
        tables = []

        # add more possiblities for hyphen words
        nouns_with_hyphen = df.loc[df['text'].str.contains('-'), 'text'].tolist()
        nouns_without_hyphen = df.loc[~df['text'].str.contains('-'), 'text'].tolist()
        nouns_with_hyphen = [word for noun in nouns_with_hyphen for word in split_hyphenated_string(noun)]

        # unique values
        nouns_list = list(set(nouns_without_hyphen + nouns_with_hyphen))

        for element in nouns_list:
            df = NOUN_CACHE[element]

            if df is None:
                continue

            df.fillna(value="None", inplace=True)
            english_text = df['nouns']['english']
            german_text = df['nouns']['german']
            noun_details = df['noun_details']['english'].split('\n')

            if len(noun_details) > 2:
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
        self.blackboard['nouns_rich_analysis'] = tables

    def run(self):
        while self.blackboard['stages']['analyzed_input'] != 'DONE':
            sleep(0.0001)

        self.blackboard['stages']['analyzed_nouns'] = 'STARTED'
        NOUN_CACHE.refresh_cache()
        self.analyze_nouns()
        NOUN_CACHE.cache()
        self.blackboard['stages']['analyzed_nouns'] = 'Analyzed nouns!'
        self.generate_rich_text()
        self.blackboard['stages']['analyzed_nouns'] = 'Generated rich text!'
        self.generate_rich_analysis()
        self.blackboard['stages']['analyzed_nouns'] = 'Generated rich analysis!'
        self.blackboard['stages']['analyzed_nouns'] = 'DONE'
