# noun_analyzer.py
from event_layer import Event
from event_layer import EventHandler
from nouns_table import NounsCache

noun_cache = NounsCache()


class NounAnalyzer:
    def __init__(self, event_handler):
        self.event_handler = event_handler

    def analyze(self, nouns):
        for noun in nouns:
            # check the nouns cache first for availability
            # otherwise call the noun conjugator
            # introduce randomness in this loop so the calls are more human
            self.event_handler.handle(Event('noun_found', {'noun': noun}))

    def get(self, noun):
        self.event_handler.handle(Event('noun_called', {'noun': noun}))


def on_noun_found(data):
    # check availability in nouns cache
    # call nouns conjugator if not in the cache
    print(f'Found noun: {data["noun"]}')
    noun_cache[data["noun"]]


def on_noun_called(data):
    # return noun conjugation
    meaning = noun_cache[data["noun"]]
    print(f'Meaning of {data["noun"]}: {meaning}')


def main():
    event_handler = EventHandler()
    noun_analyzer = NounAnalyzer(event_handler)

    event_handler.register('noun_found', on_noun_found)
    event_handler.register('noun_called', on_noun_called)

    nouns = ['Flasche']
    noun_analyzer.analyze(nouns)
    noun_analyzer.get(nouns[0])


if __name__ == "__main__":
    main()
