import pandas as pd

class Quiz(object):

    def __init__(self, price, topic):

        self.price = price
        self.topic = topic

    def questions(self):
        data = pd.read_csv('/content/drive/MyDrive/dataset/c.csv', index_col=0)
        question = '123'
        return question







if __name__ == "__main__":
    q = Quiz(5, 4)
    q

