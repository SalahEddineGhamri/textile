from pathlib import Path
import os

"""
from appdirs import user_cache_dir, user_config_dir
cache_dir = user_cache_dir('textile')
config_dir = user_config_dir('textile')
"""

# Get the directory of the current script (__file__)
SCRIPT_DIR = Path(__file__).resolve().parent
TEXTILE_DIR = (SCRIPT_DIR.parent / "../textile").resolve()

BLACKLIST_CACHE_FILE = TEXTILE_DIR / "cache/blacklist.csv"
VERBS_CONJUGATION_CACHE_FILE = TEXTILE_DIR / "cache/verbs_conjugation.csv"
VERBS_MEANING_CACHE_FILE = TEXTILE_DIR / "cache/verbs_meaning.csv"
NOUNS_CACHE_FILE = TEXTILE_DIR / "cache/nouns.csv"
ADJECTIVES_CACHE_FILE = TEXTILE_DIR / "cache/adjectives.csv"
ADVERBS_CACHE_FILE = TEXTILE_DIR / "cache/adverbs.csv"
PREPOSITIONS_CACHE_FILE = TEXTILE_DIR / "cache/prepositions.csv"
ARTICLES_CACHE_FILE = TEXTILE_DIR / "cache/articles.csv"
ANKI_PATH = TEXTILE_DIR / "anki_output"

# TODO change to INPUT_TEXT_PATH
INPUT_PATH = TEXTILE_DIR / "texts/input_4.txt"

# Create the directory if not found
VERBS_CONJUGATION_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
VERBS_MEANING_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
NOUNS_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
