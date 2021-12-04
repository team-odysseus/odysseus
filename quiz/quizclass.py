import os
import random
import numpy as np
import pandas as pd
from storage.database import LoadData


class Quiz(object):
    def __init__(self):
        self.ld = LoadData(os.path.join(os.getcwd(), 'game.csv'))
        self.categories_num: int = 5
        self.unq_categories = np.arange(self.categories_num)
        pass

    def get_one_cat_questions(self, cat_num):
        cat_lines = self.ld.db[self.ld.db.Category == cat_num]
        pass

    def choose_categories(self):
        categories = self.ld.get_column('cat_num')
        unq_categories, unq_counts = np.unique(categories, return_counts=True)
        unq_categories = unq_categories[unq_counts >= 4]
        self.unq_categories = random.sample(unq_categories, k=self.categories_num)
        return unq_categories

    def prepare_questions(self):
        return

    def create_5x4_question_box(self):
        pass

if __name__ == "__main__":

    q = Quiz(5, 4)
    q




