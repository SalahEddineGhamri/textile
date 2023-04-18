# contains a cache for verbs
import warnings
import pandas as pd
from config import VERBS_CONJUGATION_CACHE_FILE, VERBS_MEANING_CACHE_FILE
from verb_conjugation_scapper import scrapp_for_verb
from words_meanings_scrapper import nouns_definition_parser
import time
import random
import multiprocessing

# TODO: investigate the pandas performance issues later on
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


class VerbsMeaningCache(pd.DataFrame):
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
        if not VERBS_MEANING_CACHE_FILE.exists():
            super().__init__(index=self.index)
        else:
            super().__init__(pd.read_csv(VERBS_MEANING_CACHE_FILE,
                                         index_col=['aspects', 'language']))
        self.lock = multiprocessing.Lock()

    def cache(self):
        with self.lock:
            try:
                if super().empty:
                    return False
                if not VERBS_MEANING_CACHE_FILE:
                    return False
                super().to_csv(VERBS_MEANING_CACHE_FILE, index=True)
                return True
            except Exception as e:
                return False

    def __getitem__(self, key):
            if key in self.columns:
                return super().__getitem__(key)
            else:
                with self.lock:
                    sleep_interval = random.uniform(0.1, 0.4)
                    time.sleep(sleep_interval)
                    new_verb = nouns_definition_parser('verbs_table', key)
                    if new_verb is not None:
                        if new_verb['verbs'] is not None:
                            self[key] = pd.Series(index=self.index, dtype='object')
                            for aspect, languages in new_verb.items():
                                if languages is not None:
                                    self.loc[(aspect, 'english'), key] = languages[0]
                                    self.loc[(aspect, 'german'), key] = languages[1]
                            self.to_csv(VERBS_MEANING_CACHE_FILE, index=True)
                            return super().loc[(slice(None), slice(None)), key]
                        else:
                            return None
                    else:
                        return None


class VerbsConjugationCache(pd.DataFrame):

    voices = ['indicative_active',
              'subjunctive_active',
              'conditional_active',
              'imperative_active',
              'infinitive_participle_active']

    tenses = ["Present",
              "Imperfect",
              "Perfect",
              "Pluperfect",
              "Future",
              "FuturePerfect",
              "InfinitiveI",
              "InfinitiveII",
              "ParticipleI",
              "ParticipleII"]

    index = pd.MultiIndex.from_product([voices, tenses],
                                       names=('voice', 'tense'))

    def __init__(self):
        if not VERBS_CONJUGATION_CACHE_FILE.exists():
            super().__init__(index=self.index)
        else:
            super().__init__(pd.read_csv(VERBS_CONJUGATION_CACHE_FILE,
                                         index_col=['voice', 'tense']))
        self.lock = multiprocessing.Lock()

    def cache(self):
        with self.lock:
            try:
                if super().empty:
                    # print('The DataFrame is empty')
                    return False

                if not VERBS_CONJUGATION_CACHE_FILE:
                    # print('The file path is empty')
                    return False

                super().to_csv(VERBS_CONJUGATION_CACHE_FILE, index=True)
                # print(f'DataFrame has been written to {VERBS_CACHE_FILE}')
                return True

            except Exception as e:
                # print(f'An error occurred while writing to file: {e}')
                return False

    def __getitem__(self, key):
        with self.lock:
            try:
                return super().__getitem__(key)
            except KeyError:
                sleep_interval = random.uniform(0.1, 0.4)
                time.sleep(sleep_interval)
                # print("scrapping for verb ...")
                # new_verb_meaning = nouns_definition_parser(key)
                new_verb = scrapp_for_verb(key)
                self[key] = pd.Series(index=self.index, dtype='object')
                for (voice, tense), values in new_verb.items():
                    if values[key] is not None:
                        self.loc[(voice, tense), key] = values[key]
                    else:
                        return None
                super().to_csv(VERBS_CONJUGATION_CACHE_FILE, index=True)
                return super().loc[(slice(None), slice(None)), key]


VERBS_CONJUGATION_CACHE = VerbsConjugationCache()
VERBS_MEANING_CACHE = VerbsMeaningCache()

if __name__ == "__main__":
    verb_meaning_cache = VerbsMeaningCache()
    df = verb_meaning_cache['machen']
    print(df)
    verb_conjugation_cache = VerbsConjugationCache()
    df = verb_conjugation_cache['gehen']['indicative_active']
    print(df.values)
    verb_conjugation_cache.cache()
