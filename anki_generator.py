import genanki
import random

# fields are HTML


class GeneralNote(genanki.Note):
    model = genanki.Model(
                        2617295532,
                        'General Model',
                        fields=[
                            {'name': 'Noun'},
                            {'name': 'English'},
                            {'name': 'German'}
                        ],
                        templates=[
                            {
                                'name': 'General_Card',
                                'qfmt': '<div style="text-align: center; font-size: 18px;">{{Noun}}</div>',
                                'afmt': '{{FrontSide}}<hr id="answer"><div style="display: flex; justify-content: center; font-size: 12px;"><div style="margin-right: 50px;"><br>{{English}}</div><div><br>{{German}}</div></div>'
                            },
                        ],
                    )

    def __init__(self, inputs):
        super().__init__(model=GeneralNote.model, fields=inputs,)



class NounNote(genanki.Note):
    model = genanki.Model(
                        9607292589,
                        'Noun Model',
                        fields=[
                            {'name': 'Noun'},
                            {'name': 'English'},
                            {'name': 'FullNoun'},
                            {'name': 'Plural'}
                        ],
                        templates=[
                            {
                                'name': 'Noun_Card',
                                'qfmt': '<div style="text-align: center; font-size: 18px;">{{Noun}}</div>',
                                'afmt': '{{FrontSide}}<hr id="answer"><div style="text-align: left; font-size: 12px;"> <strong>meaning</strong>: {{English}} <br> <strong>noun</strong>: {{FullNoun}} <br> <strong>plural</strong>: Die {{Plural}} </div>',
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
                        'Verb Model',
                        fields=[
                            {'name': 'Verb'},
                            {'name': 'English'},
                            {'name': 'Conjugation'}
                        ],
                        templates=[
                            {
                                'name': 'Verb_Card',
                                'qfmt': '<div style="text-align: center; font-size: 18px;">{{Verb}}',
                                'afmt': '{{FrontSide}}<hr id="answer"><div style="text-align: left; font-size: 12px;"> <strong>meaning</strong>: {{English}} <br> <br> <strong>conjugation</strong>: <br> <br> {{Conjugation}}',
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
