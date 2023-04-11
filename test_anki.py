import genanki

# create a model for the cards in the deck
model = genanki.Model(
    1607392319,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
)

# create a new deck
deck = genanki.Deck(
    2059400110,
    'My Deck',
)

# create new notes (cards) and add them to the deck
note1 = genanki.Note(
    model=model,
    fields=['Question 1', 'Answer 1'],
)
deck.add_note(note1)

note2 = genanki.Note(
    model=model,
    fields=['Question 2', 'Answer 2'],
)
deck.add_note(note2)

# create a new package and add the deck to it
package = genanki.Package(deck)

# write the package to a file
package.write_to_file('./anki/my_deck.apkg')
