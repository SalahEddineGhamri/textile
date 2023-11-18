# textile
Helper to learn sturdy german texts and extract vocabulary
it show case grammer cases and help you remember the rules
while reading the text

## roadmap
- input a text from a txt file
- analyze text for what is available "article"
- define a color scheme
- give all article colors
- show the text nin text widget
- make articles csv complete

## dependencies
- pip3 install pandas
- pip3 install genanki
- pip3 install spacy
- python3 -m spacy download de_core_news_sm
- pip3 install pandarallel
- pip3 install rich
- pip3 install textual==0.15.0
- pip3 install bs4
- pip3 install german_nouns

```sh
pip3 install -r requirements.txt
```

## code format
from within the src folder:
```sh
autopep8 --in-place --aggressive --aggressive --max-line-length 100 --indent-size 2 ./*.py
```
Please, we use tab size 2.


## categories of part of speech
- ADJ: adjective, e.g. big, old, green, incomprehensible, first
- ADP: adposition, e.g. in, to, during
- ADV: adverb, e.g. very, tomorrow, down, where, there
- AUX: auxiliary, e.g. is, has (done), will (do), should (do)
- CONJ: conjunction, e.g. and, or, but
- CCONJ: coordinating conjunction, e.g. and, or, but
- DET: determiner, e.g. a, an, the
- INTJ: interjection, e.g. psst, ouch, bravo, hello
- NOUN: noun, e.g. girl, cat, tree, air, beauty
- NUM: numeral, e.g. 1, 2017, one, seventy-seven, IV, MMXIV
- PART: particle, e.g. ’s, not,
- PRON: pronoun, e.g I, you, he, she, myself, themselves, somebody
- PROPN: proper noun, e.g. Mary, John, London, NATO, HBO
- PUNCT: punctuation, e.g. ., (, ), ?
- SCONJ: subordinating conjunction, e.g. if, while, that
- SYM: symbol, e.g. $, %, §, ©, +, −, ×, ÷, =, :), 😝
- VERB: verb, e.g. run, runs, running, eat, ate, eating
- X: other, e.g. sfpksdpsxmsa
- SPACE: space, e.g.
