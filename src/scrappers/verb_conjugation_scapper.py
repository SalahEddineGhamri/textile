import requests
from bs4 import BeautifulSoup
import json

# TODO: scrapper must state if None is returned

# Construct the URL to search for the verb
url = "https://www.verbformen.com/conjugation/?w="
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
headers = {"User-Agent": user_agent}


def verb_url(verb):
    return url + verb


def scrapp_for_verb(verb):
    response = requests.get(verb_url(verb), headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    voices = [
        "indicative_active",
        "subjunctive_active",
        "conditional_active",
        "imperative_active",
        "infinitive_participle_active",
    ]

    tenses = [
        "Present",
        "Imperfect",
        "Perfect",
        "Pluperfect",
        "Future",
        "FuturePerfect",
        "InfinitiveI",
        "InfinitiveII",
        "ParticipleI",
        "ParticipleII",
    ]

    # init conjugation_dict
    conjugation_dict = {}
    for voice in voices:
        for tense in tenses:
            conjugation_dict[(voice, tense)] = {verb: None}

    def fill_table(tense, table):
        for voice in voices:
            if conjugation_dict[(voice, tense)][verb] is None:
                conjugation_dict[(voice, tense)][verb] = table

    for entry in soup.find_all("li"):
        if entry.b is None:
            continue

        tag = entry.b.text.strip().replace(" ", "")
        if tag in tenses:
            text = entry.text.split(":")
            text = text[1].replace("\n", " ").split(",")
            text = "\n".join(text)
            fill_table(tag, text)

    return conjugation_dict


if __name__ == "__main__":
    print(scrapp_for_verb("gesagt"))
