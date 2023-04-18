# prepositions in all forms
import warnings
import pandas as pd
from config import PREPOSITIONS_CACHE_FILE
from words_meanings_scrapper import nouns_definition_parser
import time
import random
from multiprocessing import Lock
import sys

# TODO: investigate the pandas performance issues later on
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


class PrepositionsCache(pd.DataFrame):

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
        if not PREPOSITIONS_CACHE_FILE.exists():
            super().__init__(index=self.index)
        else:
            super().__init__(pd.read_csv(PREPOSITIONS_CACHE_FILE,
                                         index_col=['aspects', 'language']))
        self.lock = Lock()

    def cache(self):
        with self.lock:
            try:
                if super().empty:
                    return False
                if not PREPOSITIONS_CACHE_FILE:
                    return False
                super().to_csv(PREPOSITIONS_CACHE_FILE, index=True)
                return True
            except Exception:
                return False

    def __getitem__(self, key):
        if key in self.columns:
            return super().__getitem__(key)
        else:
            with self.lock:
                sleep_interval = random.uniform(0.1, 1)
                time.sleep(sleep_interval)

                new_noun = nouns_definition_parser('prepositions_table', key)

                if new_noun is not None:
                    self[key] = pd.Series(index=self.index, dtype='object')
                    for aspect, languages in new_noun.items():
                        if languages is not None:
                            self.loc[(aspect, 'english'), key] = languages[0]
                            self.loc[(aspect, 'german'), key] = languages[1]
                    self.to_csv(PREPOSITIONS_CACHE_FILE, index=True)
                    return super().loc[(slice(None), slice(None)), key]
                else:
                    return None


PREPOSITIONS_CACHE = PrepositionsCache()

if __name__ == "__main__":
    word = sys.argv[1]
    preposition_cache = PrepositionsCache()
    df = preposition_cache[word]
    print(df)
    preposition_cache.cache()
