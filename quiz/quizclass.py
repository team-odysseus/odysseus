import random
from typing import Tuple

import numpy as np
import pandas as pd
from storage.database import LoadData

__version_ = 0.0006


class Quiz(object):
    def __init__(self,
                 name_quiz_data_file,
                 categories_num: int = 5):
        self.ld = LoadData(name_quiz_data_file)
        self.categories_num: int = categories_num
        self.unq_categories = np.arange(self.categories_num)
        self.all_categories_questions: list = []
        self.q_a_matrix_rows = categories_num
        self.q_a_matrix_cols = 4
        self.all_categories_questions_idxs: np.array = np.zeros([self.q_a_matrix_cols, self.q_a_matrix_rows])
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
        unq_categories = unq_categories[unq_counts >= self.q_a_matrix_cols]
        unq_categories = list(unq_categories)
        # TODO: add check and get only ONE question from each unique score_group
        self.unq_categories = random.sample(unq_categories, k=self.categories_num)
        pass

    def prepare_questions(self):
        all_categories_questions_idxs: list = []
        for cat_num in self.unq_categories:
            cat_questions = self.get_one_cat_questions(cat_num)
            cat_questions_idxs = cat_questions.index.tolist()
            self.all_categories_questions.append(cat_questions)
            q_a_dict: dict = {}
            for idx in cat_questions.index:
                """ creating dictionary for user answers """
                q_a_dict.update({idx: -1})
            self.user_all_q_a.update({cat_num: q_a_dict})
            all_categories_questions_idxs.append(cat_questions_idxs)
        self.all_categories_questions_idxs = np.asarray(all_categories_questions_idxs)
        pass

    def create_rows_cols_pic_box(self) -> Tuple[list, np.array]:
        """

        Returns:
            pic_matrix (list):      list of lists with str for buttons and picture creating
            array_idxs (np.array):  array with question indxs
        """
        pic_matrix: list = []
        for row_idx in range(self.q_a_matrix_rows):
            row_list: list = []
            q_a = self.get_q_a(row_idx, 0)
            row_list.append(q_a['category'].item())
            row_list.append(str(q_a['score'].item()))
            for cols_idx in range(1, self.q_a_matrix_cols):
                q_a = self.get_q_a(row_idx, cols_idx)
                row_list.append(str(q_a['score'].item()))
            pic_matrix.append(row_list)
        return pic_matrix, self.all_categories_questions_idxs

    def get_q_a(self, row_idx, col_idx) -> pd.DataFrame:
        question_idx = self.all_categories_questions_idxs[row_idx, col_idx]
        q_a = self.ld.db[self.ld.db.index == question_idx]
        return q_a


if __name__ == "__main__":
    q = Quiz(name_quiz_data_file='../storage/quiz.csv')
    q.choose_categories()
    q.prepare_questions()
    print(q.all_categories_questions)
    print(q.get_q_a(2, 3))
    pic_list, _ = q.create_rows_cols_pic_box()
    print(pic_list)
