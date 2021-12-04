import pandas as pd
import numpy as np


class LoadData:
    def __init__(self, name):
        self.db = pd.read_csv(name, delimiter=',',
                              names=['cat_num',
                                     'category',
                                     'question',
                                     'score',
                                     'correct',
                                     'not_correct_1',
                                     'not_correct_2',
                                     'not_correct_3',
                                     'not_correct_4'
                                     ]
                              )

    def get_lines_by_category(self, category):
        a = self.db[self.db.Category == category]
        print(a)

    def get_column(self, column):
        return self.db[column]

    def get_data_by_index(self, i, j):
        return self.db.iat[i, j]

    def base_size(self):
        return self.db.Category.count()-1


#ld = LoadData('game.csv')
#print(ld.get_data_by_index(1, 3))
