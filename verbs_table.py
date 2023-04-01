# contains a cache for verbs
# functions to be implemented:
# 2. save every missing verb
import warnings
import pandas as pd
from config import VERBS_CACHE_FILE

# TODO: investigate the performance issues later on
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


class VerbsCache(pd.DataFrame):

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
              "Imperfect",
              "InfinitiveI",
              "InfinitiveII",
              "ParticipleI",
              "ParticipleII"]

    index = pd.MultiIndex.from_product([voices, tenses],
                                       names=('voice', 'tense'))

    def __init__(self):
        if not VERBS_CACHE_FILE.exists():
            super().__init__(index=self.index)
        else:
            super().__init__(pd.read_csv(VERBS_CACHE_FILE,
                                         index_col=['voice', 'tense']))

    def get_verb(self, verb, voice, tense):
        return self[verb][voice][tense]

    def add_verb(self, verb, voice, tense, value):
        if verb in self.columns:
            self.loc[(voice, tense), verb] = value
        else:
            self[verb] = pd.Series(index=self.index, dtype='object')
            self.loc[(voice, tense), verb] = value

    def cache(self):
        try:
            if super().empty:
                print('The DataFrame is empty')
                return False

            if not VERBS_CACHE_FILE:
                print('The file path is empty')
                return False

            super().to_csv(VERBS_CACHE_FILE, index=True)
            print(f'DataFrame has been written to {VERBS_CACHE_FILE}')
            return True

        except Exception as e:
            print(f'An error occurred while writing to file: {e}')
            return False

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            # start scapping for the verb
            pass


if __name__ == "__main__":

    verb_cache = VerbsCache()

    verb_cache.add_verb('run',
                        'indicative_active',
                        'Present',
                        'I am present table')

    print(verb_cache.get_verb('run', 'indicative_active', 'Present'))

    verb_cache.add_verb('run',
                        'indicative_active',
                        'Future',
                        'I am future table')

    print(verb_cache.get_verb('run', 'indicative_active', 'Future'))

    verb_cache.add_verb('go',
                        'indicative_active',
                        'Present',
                        'I am present table')

    print(verb_cache.get_verb('go', 'indicative_active', 'Present'))

    verb_cache.cache()
