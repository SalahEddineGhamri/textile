import requests
from bs4 import BeautifulSoup
import sys

verb = sys.argv[1]
verb = "gehen"

# Construct the URL to search for the verb
url = f'https://www.verbformen.com/conjugation/?w={verb}'

# Send a GET request to the website and parse the HTML response
response = requests.get(url)

text = ""
with open('output.html', 'r') as file:
    text = file.read()

# soup = BeautifulSoup(response.text, 'html.parser')
soup = BeautifulSoup(text, 'html.parser')

"""
with open("output.html", "w") as file:
    file.write(str(soup))
"""

tenses = ["Present",
          "Imperfect",
          "Perfect",
          "Pluperfect",
          "Future",
          "FuturePerfect",
          "Present",
          "Imperfect",
          "Perfect",
          "Pluperfect",
          "Future",
          "InfinitiveI",
          "InfinitiveII",
          "ParticipleI",
          "ParticipleII"]

conjugation_dict = {'indicative_active': {},
                    'subjunctive_active': {},
                    'conditional_active': {},
                    'imperative_active': {},
                    'infinitive_participle_active': {}}


def fill_table(tense, table, conjugation_dict):
    for key, value in conjugation_dict.items():
        if value.get(tense) is None:
            value[tense] = table


for entry in soup.find_all('li'):
    if entry.b is None:
        continue

    tag = entry.b.text.strip()
    if tag in tenses:
        fill_table(tag, entry.text, conjugation_dict)

print(conjugation_dict['indicative_active'])

"""
# Find the table containing the verb conjugation
table = soup.find('table', {'class': 'vtable'})

# Parse the table rows to extract the verb forms
rows = table.find_all('tr')

# Extract the tense names from the first row of the table
tenses = [th.text.strip() for th in rows[0].find_all('th')[1:]]

# Extract the pronoun names from the first column of the table
pronouns = [row.find('th').text.strip() for row in rows[1:]]

# Extract the verb forms for each tense and pronoun
forms = {}
for tense, row in zip(tenses, rows[1:]):
    cols = row.find_all('td')[1:]
    for pronoun, col in zip(pronouns, cols):
        form = col.text.strip()
        forms.setdefault(pronoun, {})[tense] = form

# Print the verb conjugation in a table format
print(f'{"":>6}{" | ".join(tenses)}')
for pronoun in pronouns:
    print(f'{pronoun:>6} | {" | ".join(forms[pronoun].values())}')
"""
