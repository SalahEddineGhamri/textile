# contains a cache for nouns
import warnings
import pandas as pd
from config import NOUNS_CACHE_FILE, INPUT_PATH
from words_meanings_scrapper import nouns_definition_parser
import time
import random

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
        if not NOUNS_CACHE_FILE.exists():
            super().__init__(index=self.index)
        else:
            super().__init__(pd.read_csv(NOUNS_CACHE_FILE,
                                         index_col=['aspects', 'language']))

    def get_noun(self, noun, aspect, language):
        noun_df = self[noun]
        if noun_df is not None:
            return noun_df[aspect][language]
        else:
            return None

    def delete_noun(self, noun):
        self.drop(noun, axis=1, inplace=True)

    def add_noun(self, noun, aspect, language, value):
        if noun in self.columns:
            self.loc[(aspect, language), noun] = value
        else:
            self[noun] = pd.Series(index=self.index, dtype='object')
            self.loc[(aspect, language), noun] = value

    def cache(self):
        try:
            if super().empty:
                print('The DataFrame is empty')
                return False

            if not NOUNS_CACHE_FILE:
                print('The file path is empty')
                return False

            super().to_csv(NOUNS_CACHE_FILE, index=True)
            #print(f'------->>>> DataFrame has been written to {NOUNS_CACHE_FILE}')
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
            #print("scrapping for noun ...")
            new_noun = nouns_definition_parser(key)
            if new_noun is not None:
                if new_noun['nouns'] is not None:
                    for aspect, languages in new_noun.items():
                        if languages is not None:
                            self.loc[(aspect, 'english'), key] = languages[0]
                            self.loc[(aspect, 'german'), key] = languages[1]
                    return self[key]
                else:
                    return None


if __name__ == "__main__":
    noun_cache = NounsCache()
    noun_cache.fillna(value="None", inplace=True)
    word = 'Quartier'
    print(noun_cache[word])
    print(word in noun_cache.columns)
    noun_cache.cache()
