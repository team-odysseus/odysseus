import pandas as pd

class Quiz(object):
    def __init__(self):
        self.ld = LoadData()
        self.categories_num: int = 5
        self.unq_categories = np.arange(self.categories_num)
        pass

    def get_one_cat_questions(self):

        pass


    def choose_categories(self):
        categories = self.ld.get_column('cat_num')
        unq_categories, unq_counts = np.unique(categories, return_counts=True)
        unq_categories = unq_categories[unq_counts >= 4]
        self.unq_categories = random.sample(unq_categories, k=self.categories_num)
        return unq_categories





if __name__ == "__main__":
    q = Quiz(5, 4)
    q


