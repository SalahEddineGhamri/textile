import requests
from bs4 import BeautifulSoup
import bs4
import warnings
from german_nouns.lookup import Nouns
import sys
import pandas as pd
from config import BLACKLIST_CACHE_FILE
# TODO: should use other sources for scrapping like
# https://www.dict.cc/?s=Mitgliedsl%C3%A4nder
import multiprocessing

nouns_scrapper_lock = multiprocessing.Lock()


# TODO: protect with lock
class BlacklistCache(pd.DataFrame):
    def __init__(self):
        # get blacklisted words
        if not BLACKLIST_CACHE_FILE.exists():
            super().__init__(columns=['word'])
        else:
            super().__init__(pd.read_csv(BLACKLIST_CACHE_FILE,
                                         header=None,
                                         names=['word']))


BLACKLIST = BlacklistCache()

with warnings.catch_warnings():
    warnings.simplefilter("ignore", ResourceWarning)
    NOUNS = Nouns()


# define the URL and headers for the website
url = "https://dict.leo.org/german-english/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def split_page_content(word, soup):
    page_content = {"Possible": None,
                    "Verbs": None,
                    "Nouns": None,
                    "Definitions": None,
                    "Adjectives_or_Adverbs": None,
                    "Phrases_or_Collocations": None,
                    "Examples": None}
    key_map = {
        f'Possible base forms for "{word}"': "Possible",
        "Verbs": "Verbs",
        "Nouns": "Nouns",
        "Definitions": "Definitions",
        "Adjectives / Adverbs": "Adjectives_or_Adverbs",
        "Phrases / Collocations": "Phrases_or_Collocations",
        "Examples": "Examples"
    }
    for entry in soup.find_all('table'):
        for ent in entry.find_all('thead'):
            text = ent.text.strip()
            if text in key_map:
                key = key_map[text]
                page_content[key] = entry
    return page_content


def base_forms(possible_table):
    if possible_table is not None:
        base_forms = ""
        for entry in possible_table.find_all('td',
                                             {'data-dz-attr': 'relink',
                                              'lang': 'en'}):
            word_type = entry.text.strip().split()[-1].strip('()')
            word = ' '.join(entry.text.strip().split()[:-1])
            base_forms += f"{word} : {word_type}\n"
        return (base_forms, "")
    else:
        return None


def parse(table):
    if table is not None:
        english_, german_ = "", ""

        for cell in table.find_all('td', attrs={'data-dz-attr': 'relink'}):
            lang = cell.get('lang')
            if lang == 'en':
                words = cell.text.strip().replace('\n', '').split()
                words = " ".join(words)
                english_ += f"{words}\n"
            elif lang == 'de':
                words = cell.text.strip().replace('\n', '').split()
                words = " ".join(words)
                german_ += f"{words}\n"

        return english_, german_
    else:
        return None


def extract_noun_details(entry):
    english_entry = entry[0]
    german_entry = entry[1]
    # first pair in the table has the info
    phrases = german_entry.split("\n")
    words = phrases[0].split()
    if len(words) < 2:
        words = ["", ""]

    # find plural
    if "pl.:" in words:
        indx = words.index("pl.:")
    elif "pl." in words:
        indx = words.index("pl.")
    else:
        indx = len(words) - 2
    plural = " ".join(words[indx + 1:])

    # Determin the genus based on the article
    genus = {"der": "MASC",
             "die": "FEMI",
             "das": "NEUT"}.get(words[0], "")

    meaning = english_entry.split("\n")[:2]
    meaning = "\n".join(meaning)

    return {'article': words[0],
            'word': words[1],
            'genus': genus,
            'plural': plural,
            'meaning': meaning}


def nouns_definition_parser(caller, word):
    with nouns_scrapper_lock:
        if word+f"<{caller}>" in BLACKLIST['word'].values:
            return None
        print(f"[[ ALERT ]] parsing ... {word} for {caller}")

        response = requests.get(url + word, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        page_content = split_page_content(word, soup)
        basic_forms = base_forms(page_content["Possible"])
        verbs = parse(page_content["Verbs"])
        nouns = parse(page_content["Nouns"])
        adjectives_or_adverbs = parse(page_content["Adjectives_or_Adverbs"])
        phrases_or_collocations = parse(page_content["Phrases_or_Collocations"])
        examples = parse(page_content["Examples"])

        # TODO: parse table here to correct the plural and gender
        """
        data-dz-ui="dictentry:showFlecttab"
        """

        noun_details = None

        result = {"basic_forms": basic_forms,
                  "verbs": verbs,
                  "nouns": nouns,
                  "noun_details": noun_details,
                  "adjectives_or_adverbs": adjectives_or_adverbs,
                  "phrases_or_collocations": phrases_or_collocations,
                  "examples": examples}

        if all(ele is None for ele in result.values()):
            # blacklist this key
            BLACKLIST.loc[len(BLACKLIST)] = [word+f"<{caller}>"]
            BLACKLIST.to_csv(BLACKLIST_CACHE_FILE, index=False, header=False)
            return None

        # if nouns add more details, these are the absolute truth
        noun_details = ""
        if nouns:
            details = extract_noun_details(nouns)
            nouns_definition_nouns(word, details)
            for key, value in details.items():
                noun_details += f"{key}: {value}\n"
        result['noun_details'] = (noun_details, "")
        return result


# adds more to nouns
def nouns_definition_nouns(word, details):
    # Lookup a word

    word = NOUNS[word]

    if word:
        if word[0].get('flexion') is not None:
            if word[0]['flexion'].get('nominativ plural') is not None:
                details['plural'] = word[0]['flexion']['nominativ plural']
            else:
                if word[0]['flexion'].get('nominativ plural 1') is not None:
                    details['plural'] = word[0]['flexion']['nominativ plural 1']
                if word[0]['flexion'].get('nominativ plural 2') is not None:
                    details['plural'] += " / "
                    details['plural'] += word[0]['flexion']['nominativ plural 2']
            if word[0]['flexion'].get('nominativ singular') is not None:
                details['word'] = word[0]['flexion']['nominativ singular']

        # get article based on genus
        if word[0].get('genus') is not None:
            article = {"m": "Der",
                       "f": "Die",
                       "n": "Das"}.get(word[0]['genus'], "")
            if article != "":
                details['article'] = article
    else:
        # parse compound word
        # words = nouns.parse_compound(result['word'])
        pass


if __name__ == "__main__":
    word = sys.argv[1]
    print(nouns_definition_parser('main', word))
