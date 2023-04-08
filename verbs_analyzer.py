# verb_analyzer.py
from event_layer import Event
from event_layer import EventHandler
from verbs_table import VerbsCache

verb_cache = VerbsCache()


class VerbAnalyzer:
    def __init__(self, event_handler):
        self.event_handler = event_handler

    def analyze(self, verbs):
        for verb in verbs:
            # check the verbs cache first for availability
            # otherwise call the verb conjugator
            # introduce randomness in this loop so the calls are more human
            self.event_handler.handle(Event('verb_found', {'verb': verb}))

    def get(self, verb):
        self.event_handler.handle(Event('verb_called', {'verb': verb}))


def on_verb_found(data):
    # check availability in verbs cache
    # call verbs conjugator if not in the cache
    # write verb to the cache
    print(f'Found verb: {data["verb"]}')
    verb_cache[data["verb"]]


def on_verb_called(data):
    # return verb conjugation
    conjugation = verb_cache[data["verb"]]
    print(f'Conjugation for verb {data["verb"]}: {conjugation}')


def main():
    event_handler = EventHandler()
    verb_analyzer = VerbAnalyzer(event_handler)

    event_handler.register('verb_found', on_verb_found)
    event_handler.register('verb_called', on_verb_called)

    verbs = ['gehen']
    verb_analyzer.analyze(verbs)
    verb_analyzer.get(verbs[0])


if __name__ == "__main__":
    main()
