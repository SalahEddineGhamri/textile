import requests
from bs4 import BeautifulSoup
import bs4
import sys


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
        return (base_forms, None)


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


def extract_noun_details(entry):
    # first pair in the table has the info
    phrases = entry.split("\n")
    words = phrases[0].split()

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

    return {'article': words[0],
            'word': words[1],
            'genus': genus,
            'plural': plural}


def nouns_definition_parser(word):
    response = requests.get(url + word, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_content = split_page_content(word, soup)
    basic_forms = base_forms(page_content["Possible"])
    verbs = parse(page_content["Verbs"])
    nouns = parse(page_content["Nouns"])
    adjectives_or_adverbs = parse(page_content["Adjectives_or_Adverbs"])
    phrases_or_collocations = parse(page_content["Phrases_or_Collocations"])
    examples = parse(page_content["Examples"])

    noun_details = ""
    # if nouns add more details
    if nouns:
        for key, value in extract_noun_details(nouns[1]).items():
            noun_details += f"{key}: {value}\n"
    noun_details = (noun_details, None)

    return {"basic_forms": basic_forms,
            "verbs": verbs,
            "nouns": nouns,
            "noun_details": noun_details,
            "adjectives_or_adverbs": adjectives_or_adverbs,
            "phrases_or_collocations": phrases_or_collocations,
            "examples": examples}


if __name__ == "__main__":
    word = sys.argv[1]
    print(nouns_definition_parser(word))
