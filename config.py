from pathlib import Path

CONFIG_FILE_PATH = Path(__file__)
VERBS_CACHE_FILE = Path('cache/verbs.csv')
NOUNS_CACHE_FILE = Path('cache/nouns.csv')
ADJECTIVES_CACHE_FILE = Path('cache/adjectives.csv')
ADVERBS_CACHE_FILE = Path('cache/adverbs.csv')
PREPOSITIONS_CACHE_FILE = Path('cache/prepositions.csv')
ARTICLES_CACHE_FILE = Path('cache/articles.csv')

# Create the directory if not found
VERBS_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
NOUNS_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
