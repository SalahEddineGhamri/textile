from color_scheme import colorize_text, colors_definitions
from multiprocessing import Process
from nouns_table import NounsCache
from verbs_table import VerbsCache
from rich.table import Table
from rich.text import Text, Style
from time import sleep


class VerbsAgent(Process):
    def __init__(self, blackboard):
        super().__init__()
        self.blackboard = blackboard
        self.noun_cache = NounsCache()
        self.verb_cache = VerbsCache()
        self.blackboard['verbs_rich_text'] = ""
        self.blackboard['verbs_rich_analysis'] = ""

    def analyze_verbs(self):
        df = self.blackboard['analyzed_text']
        verbs_list = df.loc[(df['pos_'] == 'VERB'), 'text'].tolist()
        for verb in verbs_list:
            self.verb_cache[verb]
        self.verb_cache.cache()

    def generate_rich_text(self, width=100):
        df = colorize_text(self.blackboard['analyzed_text'], "VERB")
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
        self.blackboard['verbs_rich_text'] = text

    def generate_rich_analysis(self, row_nbr=5):
        df = self.blackboard['analyzed_text']
        tables = []
        verbs_list = df.loc[(df['pos_'] == 'VERB'), 'text'].tolist()
        lemmas_list = df.loc[(df['pos_'] == 'VERB'), 'lemma_'].tolist()

        verbs_list = list(set(verbs_list))
        lemmas_list = list(set(lemmas_list))

        for verb, lemma in zip(verbs_list, lemmas_list):
            df = self.noun_cache[verb]
            if df is None:
                continue
            df.fillna(value="None", inplace=True)
            english_text = self.noun_cache[verb]['verbs']['english']
            german_text = self.noun_cache[verb]['verbs']['german']

            english_text = english_text.split('\n')
            german_text = german_text.split('\n')

            table = Table(title=f"{verb}")
            table.add_column("English", justify="left", no_wrap=True)
            table.add_column("German", justify="left", no_wrap=True)
            for eng, ger in zip(english_text[:row_nbr], german_text[:row_nbr]):
                table.add_row(eng, ger)
            tables.append(table)
            conj_tables = self.verb_cache[verb]['indicative_active']
            conj_tables.fillna(value="None", inplace=True)
            table = Table()
            table.add_column("Present", justify="left", no_wrap=False)
            table.add_column("Imperfect", justify="left", no_wrap=False)
            table.add_column("Perfect", justify="left", no_wrap=False)
            table.add_column("Future", justify="left", no_wrap=False)
            if all(val != "None" for val in conj_tables.values):
                table.add_row(conj_tables['Present'],
                              conj_tables['Imperfect'],
                              conj_tables['Perfect'],
                              conj_tables['Future'])
            else:
                conj_tables = self.verb_cache[lemma]['indicative_active']
                conj_tables.fillna(value="None", inplace=True)
                table.add_row(conj_tables['Present'],
                              conj_tables['Imperfect'],
                              conj_tables['Perfect'],
                              conj_tables['Future'])

            tables.append(table)
        self.blackboard['verbs_rich_analysis'] = tables

    def run(self):
        while self.blackboard['stages']['analyzed_input'] != 'DONE':
            sleep(0.0001)

        self.blackboard['stages']['analyzed_verbs'] = 'STARTED'
        self.analyze_verbs()
        self.blackboard['stages']['analyzed_verbs'] = 'Analyzed verbs!'
        self.generate_rich_text()
        self.blackboard['stages']['analyzed_verbs'] = 'Generated rich text!'
        self.generate_rich_analysis()
        self.blackboard['stages']['analyzed_verbs'] = 'Generated rich analysis!'
        self.blackboard['stages']['analyzed_verbs'] = 'DONE'
