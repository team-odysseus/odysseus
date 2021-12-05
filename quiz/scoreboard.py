import os
import pandas as pd
from userclass import User

__version_ = 0.0002

class ScoreBoard(object):
    def __init__(self):
        self.filename = os.path.join('..', 'storage', 'score.csv')
        self.columns = ['user_id',
                        'user_name',
                        'phone',
                        'time',
                        'score']
        self.score_len = 10
        if not os.path.exists(self.filename):
            self.score_df = pd.DataFrame(columns=self.columns)
        else:
            self.score_df = pd.read_csv(self.filename)
        pass

    def add_data(self, user_data: User):
        score_row_df = pd.DataFrame(user_data, columns=self.columns)
        self.score_df = self.score_df.append(score_row_df, ignore_index=True)
        self.score_df = self.score_df.sort_values('score')[self.score_len]
        pass

    def save_data(self):
        self.score_df.to_csv(self.filename, index=False)
        pass

    def get_hiscore(self):
        return self.score_df[:self.score_len+1]