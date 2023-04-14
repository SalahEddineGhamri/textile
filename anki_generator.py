import genanki
import random

# fields are HTML


class NounNote(genanki.Note):
    model = genanki.Model(
                        9607292589,
                        'Simple Model',
                        fields=[
                            {'name': 'Noun'},
                            {'name': 'English'},
                            {'name': 'FullNoun'},
                            {'name': 'Plural'}
                        ],
                        templates=[
                            {
                                'name': 'Noun_Card',
                                'qfmt': '<div style="text-align: center; font-size: 24px;">{{Noun}}</div>',
                                'afmt': '{{FrontSide}}<hr id="answer"><div style="text-align: center; font-size: 24px;"> meaning: {{English}} <br> noun: {{FullNoun}} <br> plural: Die {{Plural}} </div>',
                            },
                        ],
                    )

    def __init__(self, inputs):
        '''
        fields = ['Noun', 'English', 'FullNoun', 'Plural']
        '''
        super().__init__(model=NounNote.model, fields=inputs,)


class VerbNote(genanki.Note):
    model = genanki.Model(
                        1607492519,
                        'Simple Model',
                        fields=[
                            {'name': 'Verb'},
                            {'name': 'English'},
                            {'name': 'Conjugation'}
                        ],
                        templates=[
                            {
                                'name': 'Verb_Card',
                                'qfmt': '<div style="text-align: center; font-size: 24px;">{{Verb}}',
                                'afmt': '{{FrontSide}}<hr id="answer"><div style="text-align: center; font-size: 24px;"> meaning: {{English}} <br> conjugation: <br> {{Conjugation}}',
                            },
                        ],
                    )

    def __init__(self, inputs):
        '''
        fields = ['Verb', 'English', 'Conjugation']
        '''
        super().__init__(model=VerbNote.model, fields=inputs,)


class AnkiGenerator:
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.deck = genanki.Deck(random.randint(10**(9), 10**9), deck_name)

    def add_note(self, note):
        self.deck.add_note(note)

    def save(self, path):
        '''
        ./anki/my_deck.apkg
        '''
        package = genanki.Package(self.deck)
        file_name = self.deck_name + ".apkg"
        path = path / file_name
        package.write_to_file(path)
