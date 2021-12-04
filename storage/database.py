import pandas as pd
import numpy as np

__version__ = 0.0004

class LoadData:
    def __init__(self, name):
        self.db = pd.read_csv(name,
                              delimiter=',',
                              usecols=['index',
                                       'cat_num',
                                       'category',
                                       'question',
                                       'score',
                                       'correct',
                                       'not_correct_1',
                                       'not_correct_2',
                                       'not_correct_3',
                                       'not_correct_4'
                                       ],
                              index_col='index'
                              )

    def get_lines_by_category(self, category):
        lines_df = self.db[self.db['cat_num'] == category]
        return lines_df

    def get_column(self, column):
        return self.db[column]

    def get_data_by_index(self, i, j):
        return self.db.iat[i, j]

    def base_size(self):
        return self.db.category.count()-1


#ld = LoadData('game.csv')
#print(ld.get_data_by_index(1, 3))
