from pprint import pprint
from german_nouns.lookup import Nouns

nouns = Nouns()


# Lookup a word
def nouns_definition_nouns(word, details):
  # Lookup a word
  word = nouns[word]
  print(word)

  if word:
    if word[0].get("flexion") is not None:
      if word[0]["flexion"].get("nominativ plural") is not None:
        details["plural"] = word[0]["flexion"]["nominativ plural"]
      else:
        if word[0]["flexion"].get("nominativ plural 1") is not None:
          details["plural"] = word[0]["flexion"]["nominativ plural 1"]
        if word[0]["flexion"].get("nominativ plural 2") is not None:
          details["plural"] += " / "
          details["plural"] += word[0]["flexion"]["nominativ plural 2"]
      if word[0]["flexion"].get("nominativ singular") is not None:
        details["word"] = word[0]["flexion"]["nominativ singular"]

    # get article based on genus
    if word[0].get("genus") is not None:
      article = {"m": "Der", "f": "Die", "n": "Das"}.get(word[0]["genus"], "")
      if article != "":
        details["article"] = article
  else:
    # parse compound word
    # words = nouns.parse_compound(result['word'])
    pass


details = {}
nouns_definition_nouns("Land", details)
print(details)
