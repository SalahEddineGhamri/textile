# adjectives in all forms
import warnings
import pandas as pd
from config import ADJECTIVES_CACHE_FILE
from words_meanings_scrapper import nouns_definition_parser
import time
import random

# TODO: investigate the pandas performance issues later on
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


class AdjectivesCache(pd.DataFrame):

    aspects = ["basic_forms",
               "verbs",
               "nouns",
               "noun_details",
               "adjectives_or_adverbs",
               "phrases_or_collocations",
               "examples"]

    language = ["english", "german"]

    index = pd.MultiIndex.from_product([aspects, language],
                                       names=('aspects', 'language'))

    def __init__(self):
        if not ADJECTIVES_CACHE_FILE.exists():
            super().__init__(index=self.index)
        else:
            super().__init__(pd.read_csv(ADJECTIVES_CACHE_FILE,
                                         index_col=['aspects', 'language']))

        self.fillna(value="None", inplace=True)

    def get_adjective(self, adjective, aspect, language):
        adjective_df = self[adjective]
        if adjective_df is not None:
            return adjective_df[aspect][language]
        else:
            return None

    def add_adjective(self, adjective, aspect, language, value):
        if adjective in self.columns:
            self.loc[(aspect, language), adjective] = value
        else:
            self[adjective] = pd.Series(index=self.index, dtype='object')
            self.loc[(aspect, language), adjective] = value

    def cache(self):
        try:
            if super().empty:
                # print('The DataFrame is empty')
                return False

            if not ADJECTIVES_CACHE_FILE:
                # print('The file path is empty')
                return False

            super().to_csv(ADJECTIVES_CACHE_FILE, index=True)
            # print(f'DataFrame has been written to {AJECTIVES_CACHE_FILE}')
            return True

        except Exception as e:
            # print(f'An error occurred while writing to file: {e}')
            return False

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            sleep_interval = random.uniform(0.1, 0.4)
            time.sleep(sleep_interval)
            # print("scrapping for noun ...")
            new_noun = nouns_definition_parser('adjectives_table', key)
            if new_noun:
                for aspect, languages in new_noun.items():
                    if languages is not None:
                        self.loc[(aspect, 'english'), key] = languages[0]
                        self.loc[(aspect, 'german'), key] = languages[1]
                self.to_csv(ADJECTIVES_CACHE_FILE, index=True)
                return self[key]
            else:
                return None


if __name__ == "__main__":
    adjective_cache = AdjectivesCache()
    df = adjective_cache['schön']
    print(df)
    adjective_cache.cache()
