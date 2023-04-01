from pathlib import Path

CONFIG_FILE_PATH = Path(__file__)
VERBS_CACHE_FILE = Path('cache/verbs.csv')
NOUNS_CACHE_FILE = Path('cache/nouns.csv')
ARTICLES_CACHE_FILE = Path('cache/verbs.csv')

# Create the directory if not found
VERBS_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
