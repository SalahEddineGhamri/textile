import requests
from bs4 import BeautifulSoup
import sys

word = sys.argv[1]

# define the URL and headers for the website
url = "https://dict.leo.org/german-english/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# get user input for the German word to look up
# word = input("Enter a German word to look up: ")

# send a GET request to the website with the user input as a query parameter
response = requests.get(url + word, headers=headers)

# parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# print(soup.prettify())

""""
with open('result.json', 'w') as outfile:
    outfile.write(soup.prettify())
"""
english_ = []
german_ = []

for entry in soup.find_all('td'):
    if entry.get('data-dz-attr') == 'relink':
        if entry.get('lang') == 'en':
            if entry is not None:
                word = entry.text
                english_.append(word)
        if entry.get('lang') == 'de':
            if entry is not None:
                word = entry.text
                german_.append(word)

for eng, deu in zip(english_, german_[:len(english_)]):
    print(eng, " ------ ", deu)


def extract_data(entry):
    words = entry.split()

    article = words[0]
    # TODO: extract adj. verb. and protect against failur
    # TODO: plural of FEM words is not correct
    # pl. start of plural (article + word)
    # | in case of feminin
    plural = " ".join(words[-2:])
    genus = ""

    if article == "der":
        genus = "MASC"
    elif article == "die":
        genus = "FEMI"
    elif article == "das":
        genus = "NEUT"

    print(genus)
    print(plural)


extract_data(german_[0])
