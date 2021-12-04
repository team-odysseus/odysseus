import random
import numpy as np
import pandas as pd

from storage.database import LoadData


class Quiz(object):
    def __init__(self, name_quiz_data_file, categories_num: int = 5):
        self.ld = LoadData(name_quiz_data_file)
        self.categories_num: int = categories_num
        self.unq_categories = np.arange(self.categories_num)
        pass

    def get_one_cat_questions(self):
        pass

    def choose_categories(self):
        """ take list of question categories from DB.
        Leave just unique and calculate count questions each category.
        If count of questions in category is 4 or more keep for use
        Take from category list just self.categories_num elements in random sequence.

        return:
            list of unique categories"""
        categories = self.ld.get_column('cat_num').tolist()
        unq_categories, unq_counts = np.unique(categories, return_counts=True)
        unq_categories = unq_categories[unq_counts >= 4]
        self.unq_categories = random.choices(unq_categories, k=self.categories_num)
        return unq_categories

    def prepare_questions(self):
        return

    def create_5x4_question_box(self):
        pass


if __name__ == "__main__":
    q = Quiz(name_quiz_data_file='../storage/quiz.csv')
    print(q.choose_categories())
