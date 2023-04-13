from anki_generator import VerbNote, AnkiGenerator, NounNote

def split_hyphenated_string(s):
    words = s.split('-')
    result = []
    for i, word in enumerate(words):
        if i == 0:
            result.append(word.capitalize())
        elif i == len(words) - 1:
            result.append(' ' + word.capitalize())
            result.append(''.join(words).capitalize())
        else:
            result.append(' ' + word.capitalize())
    return result


generator = AnkiGenerator("path")
note = NounNote(["1", "2", "3", "4"])
generator.add_note(note)
print(generator)
