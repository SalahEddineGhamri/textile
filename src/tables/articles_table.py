import pandas as pd


class ArticlesTable:
    def __init__(self):
        self._df = pd.read_csv(r"database/articles.csv")

    def get_df(self):
        return self._df


articles_table = ArticlesTable()
