import pandas as pd
import numpy as np


class Database:
    def __init__(self, name):
        self.db = pd.read_csv(name, delimiter=',')

    def put(self):
        self.db.head()




