import genanki
import random


class NounNote:
    def __init__(self, fields):
        '''
        fields = ['Noun', 'English', 'FullNoun', 'Plural']
        '''
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
                                    'name': 'Card 1',
                                    'qfmt': '{{Noun}}',
                                    'afmt': '{{FrontSide}}<hr id="answer">{{English}}{{FullNoun}}{{Plural}}',
                                },
                            ],
                        )
        return genanki.Note(model=model, fields=fields,)


class VerbNote:
    def __init__(self, fields):
        '''
        fields = ['Verb', 'English', 'PresentPastParticip']
        '''
        model = genanki.Model(
                            1607492519,
                            'Simple Model',
                            fields=[
                                {'name': 'Verb'},
                                {'name': 'English'},
                                {'name': 'PresentPastParticip'}
                            ],
                            templates=[
                                {
                                    'name': 'Card 1',
                                    'qfmt': '{{Verb}}',
                                    'afmt': '{{FrontSide}}<hr id="answer">{{English}}{{PresentPastParticip}}',
                                },
                            ],
                        )
        return genanki.Note(model=model, fields=fields,)


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
        package.write_to_file(path+self.deck_name+".apkg")
