import os
import pandas as pd
from userclass import User

__version_ = 0.0003


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

    # DEF: add to score list new user
    # TODO: make check unique user_id
    def add_data(self, user_data: User):
        score_row_df = pd.DataFrame({'user_id': [user_data.id],
                                     'user_name': [user_data.name],
                                     'phone': [user_data.phone],
                                     'time': [user_data.time],
                                     'score': [user_data.score]
                                     })

        self.score_df = self.score_df.append(score_row_df, ignore_index=True)
        self.score_df = self.score_df.sort_values(by='score')
        pass

    # DEF: save to CSV file users score
    def save_data(self):
        self.score_df.to_csv(self.filename, index=False)
        pass

    # DEF: return DataFrame with best 10 places
    def get_hiscore(self):
        msg = ''
        for row in self.score_df.values[:self.score_len+1]:
            msg += f"{row[1]} : {row[4]}\n"
#        print(msg)
        return msg

# if __name__ == "__main__":
#     s = ScoreBoard()
#     print(s.get_hiscore())

