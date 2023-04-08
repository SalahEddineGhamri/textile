# contains a cache for verbs
import warnings
import pandas as pd
from config import VERBS_CACHE_FILE
from verb_conjugation_scapper import scrapp_for_verb

# TODO: investigate the pandas performance issues later on
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
        verb_df = self[verb]
        if verb_df is not None:
            return verb_df[voice][tense]
        else:
            return None

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
            print("scrapping for verb ...")
            new_verb = scrapp_for_verb(key)
            self[key] = pd.Series(index=self.index, dtype='object')
            for (voice, tense), values in new_verb.items():
                if values[key] is not None:
                    self.loc[(voice, tense), key] = values[key]
            self.cache()
            return self[key]


if __name__ == "__main__":
    verb_cache = VerbsCache()
    print(verb_cache['gehen'])
    verb_cache.cache()
