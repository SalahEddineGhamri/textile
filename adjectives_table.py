# adjectives in all forms
import warnings
import pandas as pd
from config import ADJECTIVES_CACHE_FILE
from words_meanings_scrapper import nouns_definition_parser
import time
import random
from multiprocessing import Lock

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
        self.lock = Lock()

    def refresh_cache(self):
        with self.lock:
            self.update(pd.read_csv(ADJECTIVES_CACHE_FILE, index_col=['aspects', 'language']))

    def cache(self):
        with self.lock:
            try:
                if super().empty:
                    return False
                if not ADJECTIVES_CACHE_FILE:
                    return False
                super().to_csv(ADJECTIVES_CACHE_FILE, index=True)
                return True
            except Exception:
                return False

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            with self.lock:
                sleep_interval = random.uniform(0.1, 2)
                time.sleep(sleep_interval)

                new_noun = nouns_definition_parser('adjectives_table', key)

                if new_noun is not None:
                    self[key] = pd.Series(index=self.index, dtype='object')
                    for aspect, languages in new_noun.items():
                        if languages is not None:
                            self.loc[(aspect, 'english'), key] = languages[0]
                            self.loc[(aspect, 'german'), key] = languages[1]
                    return super().loc[(slice(None), slice(None)), key]
                else:
                    return None


ADJECTIVES_CACHE = AdjectivesCache()

if __name__ == "__main__":
    adjective_cache = AdjectivesCache()
    df = adjective_cache['schön']
    print(df)
    adjective_cache.cache()
