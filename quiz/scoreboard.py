import pandas as pd
import os


class ScoreBoard(object):

    def __init__(self):
        filename = os.path.join('..', 'storage', 'score.csv')
        self.columns = ['user_id',
                        'user_name',
                        'phone',
                        'time',
                        'score']
        if not os.path.exists(filename):
            self.score_df = pd.DataFrame(columns=self.columns)
        else:
            self.score_df = pd.read_csv(filename)
        pass

    def add_data(self, user_data):
        pass

    def save_data(self):
        pass