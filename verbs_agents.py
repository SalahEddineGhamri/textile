from color_scheme import colorize_text, colors_definitions
from multiprocessing import Process
from threading import Thread
from verbs_table import VERBS_MEANING_CACHE, VERBS_CONJUGATION_CACHE
from rich.table import Table
from rich.text import Text, Style
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


class VerbsAgent(Thread):
    def __init__(self, blackboard):
        super().__init__()
        self.blackboard = blackboard
        self.verb_meaning_cache = VERBS_MEANING_CACHE
        self.verb_conjugation_cache = VERBS_CONJUGATION_CACHE
        self.blackboard['verbs_rich_text'] = ""
        self.blackboard['verbs_rich_analysis'] = ""

    def analyze_verbs(self):
        df = self.blackboard['analyzed_text']
        verbs_list = df.loc[(df['pos_'] == 'VERB'), 'text'].tolist()
        for verb in verbs_list:
            self.verb_conjugation_cache[verb]
            self.verb_meaning_cache[verb]

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

    def generate_rich_analysis_mt(self, row_nbr=5):
        df = self.blackboard['analyzed_text']

        # Cache frequently used data
        verb_conjugation_cache = self.verb_conjugation_cache
        verb_meaning_cache = self.verb_meaning_cache

        # Vectorize DataFrame operations
        verbs_df = df.loc[df['pos_'] == 'VERB', ['text', 'lemma_']]
        verbs_df = verbs_df.drop_duplicates()
        verbs = verbs_df['text'].tolist()
        lemmas = verbs_df['lemma_'].tolist()

        tables = []
        with ThreadPoolExecutor() as executor:
            # Multi-threaded generation of tables
            future_to_verb = {executor.submit(self._generate_verb_table, verb, lemma, verb_meaning_cache, verb_conjugation_cache, row_nbr): verb for verb, lemma in zip(verbs, lemmas)}
            for future in concurrent.futures.as_completed(future_to_verb):
                verb = future_to_verb[future]
                try:
                    meaning_table, conj_table = future.result()
                    tables.append(meaning_table)
                    tables.append(conj_table)
                except Exception as exc:
                    pass

        self.blackboard['verbs_rich_analysis'] = tables

    def _generate_verb_table(self, verb, lemma, verb_meaning_cache, verb_conjugation_cache, row_nbr):
        df = verb_meaning_cache[verb]
        if df is None:
            return None
        df.fillna(value="None", inplace=True)
        english_text = df['verbs']['english']
        german_text = df['verbs']['german']

        english_text = english_text.split('\n')
        german_text = german_text.split('\n')

        meaning_table = Table(title=f"{verb}")
        meaning_table.add_column("English", justify="left", no_wrap=True)
        meaning_table.add_column("German", justify="left", no_wrap=True)
        for eng, ger in zip(english_text[:row_nbr], german_text[:row_nbr]):
            meaning_table.add_row(eng, ger)

        # verbs conjugation
        conj_tables = verb_conjugation_cache.get(verb, {}).get('indicative_active')
        if conj_tables is not None:
            conj_tables.fillna(value="None", inplace=True)
            table = Table()
            table.add_column("Present", justify="left", no_wrap=False)
            table.add_column("Imperfect", justify="left", no_wrap=False)
            table.add_column("Perfect", justify="left", no_wrap=False)
            table.add_column("Future", justify="left", no_wrap=False)
            if "None" not in conj_tables.values:
                table.add_row(conj_tables['Present'], conj_tables['Imperfect'], conj_tables['Perfect'], conj_tables['Future'])
            else:
                conj_tables = verb_conjugation_cache.get(lemma, {}).get('indicative_active')
                if conj_tables is not None:
                    conj_tables.fillna(value="None", inplace=True)
                    table.add_row(conj_tables['Present'], conj_tables['Imperfect'], conj_tables['Perfect'], conj_tables['Future'])

        return meaning_table, table

    def generate_rich_analysis(self, row_nbr=5):
        df = self.blackboard['analyzed_text']
        tables = []
        verbs_df = df.loc[df['pos_'] == 'VERB', ['text', 'lemma_']]
        verbs_df = verbs_df.drop_duplicates()
        verbs_list = verbs_df['text'].tolist()
        lemmas_list = verbs_df['lemma_'].tolist()

        verb_meaning_cache = self.verb_meaning_cache
        verb_conjugation_cache = self.verb_conjugation_cache

        for verb, lemma in zip(verbs_list, lemmas_list):
            df = verb_meaning_cache[verb]
            if df is None:
                continue
            df.fillna(value="None", inplace=True)
            english_text = df['verbs']['english']
            german_text = df['verbs']['german']

            english_text = english_text.split('\n')
            german_text = german_text.split('\n')

            table = Table(title=f"{verb}")
            table.add_column("English", justify="left", no_wrap=True)
            table.add_column("German", justify="left", no_wrap=True)
            for eng, ger in zip(english_text[:row_nbr], german_text[:row_nbr]):
                table.add_row(eng, ger)
            tables.append(table)

            # verbs conjugation
            conj_tables = verb_conjugation_cache[verb]['indicative_active']
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
                conj_tables = verb_conjugation_cache[lemma]['indicative_active']
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
        VERBS_MEANING_CACHE.cache()
        VERBS_CONJUGATION_CACHE.cache()

        self.blackboard['stages']['analyzed_verbs'] = 'Analyzed verbs!'
        self.generate_rich_text()
        self.blackboard['stages']['analyzed_verbs'] = 'Generated rich text!'
        self.generate_rich_analysis()
        self.blackboard['stages']['analyzed_verbs'] = 'Generated rich analysis!'
        self.blackboard['stages']['analyzed_verbs'] = 'DONE'
