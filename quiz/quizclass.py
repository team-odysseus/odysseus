import random
import numpy as np
import pandas as pd
from storage.database import LoadData

__version_ = 0.0004


class Quiz(object):
    def __init__(self, name_quiz_data_file, categories_num: int = 5):
        self.ld = LoadData(name_quiz_data_file)
        self.categories_num: int = categories_num
        self.unq_categories = np.arange(self.categories_num)
        self.all_categories_questions: list = []
        self.user_all_q_a: dict = {}
        pass

    def get_one_cat_questions(self, cat_num):
        questions = self.ld.get_lines_by_category(cat_num)
        questions_out = questions.sample(n=4, random_state=42)
        return questions_out

    def choose_categories(self) -> None:
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
        pass

    def prepare_questions(self):
        for cat_num in self.unq_categories:
            cat_questions = self.get_one_cat_questions(cat_num)
            self.all_categories_questions.append(cat_questions)
            q_a_dict: dict = {}
            for idx in cat_questions.index:
                """ creating dictionary for user answers """
                q_a_dict.update({idx: -1})
            self.user_all_q_a.update({cat_num: q_a_dict})
        pass

    def create_5x4_question_box(self):
        pass


if __name__ == "__main__":
    q = Quiz(name_quiz_data_file='../storage/quiz.csv')
    q.choose_categories()
    q.prepare_questions()
    print(q.all_categories_questions)
