import requests
from bs4 import BeautifulSoup
import bs4
import sys
import pprint
import json

word = sys.argv[1]

# define the URL and headers for the website
url = "https://dict.leo.org/german-english/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# send a GET request to the website with the user input as a query parameter
response = requests.get(url + word, headers=headers)

# parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

"""
with open("mysoup.html", "r") as file:
    content = file.read()
soup = BeautifulSoup(content, 'html.parser')
"""

with open("mysoup.html", "w") as file:
    file.write(str(soup.prettify()))


"""
def soup_to_dict(soup):
    tag = soup.name
    attrs = soup.attrs
    children = []

    for child in soup.children:
        if isinstance(child, bs4.element.Tag):
            children.append(soup_to_dict(child))
        elif isinstance(child, bs4.element.NavigableString):
            children.append(str(child).strip())

    # Check if soup.string is None and return an empty string instead
    text = soup.string.strip() if soup.string else ''

    return {
        'tag': tag,
        'attrs': attrs,
        'text': text,
        'children': children
    }


soup_dict = soup_to_dict(soup)
with open("myscope.json", 'w') as f:
    json.dump(soup_dict, f)
"""

page_content = {"Possible": None,
                "Verbs": None,
                "Nouns": None,
                "Definitions": None,
                "Adjectives_or_Adverbs": None,
                "Phrases_or_Collocations": None,
                "Examples": None}

english_ = []
german_ = []

key_map = {
    f'Possible base forms for "{word}"': "Possible",
    "Verbs": "Verbs",
    "Nouns": "Nouns",
    "Definitions": "Definitions",
    "Adjectives / Adverbs": "Adjectives_or_Adverbs",
    "Phrases / Collocations": "Phrases_or_Collocations",
    "Examples": "Examples"
}


def tables_to_page_content(soup):
    for entry in soup.find_all('table'):
        for ent in entry.find_all('thead'):
            text = ent.text.strip()
            if text in key_map:
                key = key_map[text]
                page_content[key] = entry

tables_to_page_content(soup)

def base_forms(possible_table):
    if possible_table is not None:
        base_forms = []
        for entry in possible_table.find_all('td',
                                             {'data-dz-attr': 'relink',
                                              'lang': 'en'}):
            word_type = entry.text.strip().split()[-1].strip('()')
            word = ' '.join(entry.text.strip().split()[:-1])
            base_forms.append({'word': word, 'type': word_type})
        return base_forms


print(base_forms(page_content["Possible"]))


def parse(table, table_name):
    print(f"-----------------{table_name}------------------")
    if table is not None:
        english_ = []
        german_ = []

        for cell in table.find_all('td', attrs={'data-dz-attr': 'relink'}):
            lang = cell.get('lang')
            if lang == 'en':
                words = cell.text.strip().replace('\n', '').split()
                words = " ".join(words)
                english_.append(words)
            elif lang == 'de':
                words = cell.text.strip().replace('\n', '').split()
                words = " ".join(words)
                german_.append(words)

        for eng, deu in zip(english_, german_[:len(english_)]):
            print(eng, " >---< ", deu)


parse(page_content["Verbs"], "Verbs")
parse(page_content["Nouns"], "Nouns")
parse(page_content["Adjectives_or_Adverbs"], "Adjectives_or_Adverbs")
parse(page_content["Phrases_or_Collocations"], "Phrases_or_Collocations")
parse(page_content["Examples"], "Examples")

# TODO: extract adj. verb. and protect against failur
# TODO: plural of FEM words is not correct


def word_type(english):
    """
    Extracts the word type from the English definition.
    """
    for eng in english:
        if "adj." in eng:
            return "adj."
        elif "verb." in eng:
            return "verb."
    return "noun."


def extract_noun(entry):
    words = entry.split()
    print(words)

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


def meanings(english_, german_):
    n = min(len(english_), len(german_))
    english = [element.replace("\xa0", " ") for element in english_]
    german = [element.replace("\xa0", " ") for element in german_]
    return {'english': english[:n],
            'german': german[:n]}

"""
print(word_type(english_))
if word_type(english_) == "noun.":
    pprint.pprint(extract_noun(german_[0]))
pprint.pprint(meanings(english_, german_))
"""
