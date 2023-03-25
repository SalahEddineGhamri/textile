import spacy
import pandas as pd


# df['new_col'] = df['text'].parallel_apply(lambda x: nlp(x))
# pandarallel.initialize(progress_bar=False)


def analyze_text(text):
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)
    data = []
    for token in doc:
        data.append([token.text,
                     token.lemma_,
                     token.pos_,
                     spacy.explain(token.pos_),
                     token.morph,
                     token.morph.get("Case"),
                     token.morph.get("Number"),
                     token.morph.get("Person"),
                     token.morph.get("PronType"),
                     token.tag_,
                     token.dep_,
                     token.shape_,
                     token.is_alpha,
                     token.is_stop])

    return pd.DataFrame(data=data, columns=['text',
                                            'lemma_',
                                            'pos_',
                                            'pos_meaning_',
                                            'morph',
                                            'morph_case',
                                            'morph_number',
                                            'morph_person',
                                            'morph_prontype',
                                            'tag_',
                                            'dep_',
                                            'shape_',
                                            'is_alpha',
                                            'is_stop'])
