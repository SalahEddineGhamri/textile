import pandas as pd
import spacy
from pandarallel import pandarallel

#df['new_col'] = df['text'].parallel_apply(lambda x: nlp(x))
#pandarallel.initialize(progress_bar=False)

def tokenize_text(text):
    nlp = spacy.load("de_core_news_sm")
    df = pd.DataFrame(nlp(text), columns=['tokens'])
    return df
