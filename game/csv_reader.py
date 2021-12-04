import pandas as pd

data = pd.read_csv('../tests/test_scenario.csv')

s_x, s_y = data.shape

print(s_x, s_y)
