# contains a cache for nouns
import warnings
import pandas as pd
from config import NOUNS_CACHE_FILE
from words_meanings_scrapper import nouns_definition_parser
import time
import random
import sys
from multiprocessing import Lock

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


class NounsCache(pd.DataFrame):

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
        # get nouns cache
        if not NOUNS_CACHE_FILE.exists():
            super().__init__(index=self.index)
        else:
            super().__init__(pd.read_csv(NOUNS_CACHE_FILE,
                                         index_col=['aspects', 'language']))

        self.fillna(value="None", inplace=True)
        self.lock = Lock()

    def delete_noun(self, noun):
        with self.lock:
            self.drop(noun, axis=1, inplace=True)

    def refresh_cache(self):
        with self.lock:
            self.update(pd.read_csv(NOUNS_CACHE_FILE, index_col=['aspects', 'language']))

    def cache(self):
        with self.lock:
            try:
                if super().empty:
                    return False
                if not NOUNS_CACHE_FILE:
                    return False
                super().to_csv(NOUNS_CACHE_FILE, index=True)
                return True
            except Exception as e:
                return False

    def __getitem__(self, key):
        if key in self.columns:
            return super().__getitem__(key)
        else:
            with self.lock:
                if not isinstance(key, str):
                    return None

                sleep_interval = random.uniform(0.1, 2)
                time.sleep(sleep_interval)
                new_noun = nouns_definition_parser('nouns_table', key)

                if new_noun is not None:
                    self[key] = pd.Series(index=self.index, dtype='object')
                    for aspect, languages in new_noun.items():
                        if languages is not None:
                            self.loc[(aspect, 'english'), key] = languages[0]
                            self.loc[(aspect, 'german'), key] = languages[1]
                    return super().loc[(slice(None), slice(None)), key]
                else:
                    return None


NOUN_CACHE = NounsCache()

if __name__ == "__main__":
    word = sys.argv[1]
    noun_cache = NounsCache()
    print(noun_cache[word])
