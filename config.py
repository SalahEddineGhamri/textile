from pathlib import Path

CONFIG_FILE_PATH = Path(__file__)
BLACKLIST_CACHE_FILE = Path('cache/blacklist.csv')
VERBS_CONJUGATION_CACHE_FILE = Path('cache/verbs_conjugation.csv')
VERBS_MEANING_CACHE_FILE = Path('cache/verbs_meaning.csv')
NOUNS_CACHE_FILE = Path('cache/nouns.csv')
ADJECTIVES_CACHE_FILE = Path('cache/adjectives.csv')
ADVERBS_CACHE_FILE = Path('cache/adverbs.csv')
PREPOSITIONS_CACHE_FILE = Path('cache/prepositions.csv')
ARTICLES_CACHE_FILE = Path('cache/articles.csv')
ANKI_PATH = Path('./anki')

INPUT_PATH = "./texts/cannabis_soll_erlaubt_werden.txt"

# Create the directory if not found
VERBS_CONJUGATION_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
VERBS_MEANING_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
NOUNS_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
