from pprint import pprint
from german_nouns.lookup import Nouns

nouns = Nouns()

# Lookup a word
word = nouns['Fahrad']
pprint(word)

# parse compound word
words = nouns.parse_compound('Vermögensbildung')
print(words)
