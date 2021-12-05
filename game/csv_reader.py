import pandas as pd

TEXT_KEY = "text"
CHOISES_KEY = "choices"
ROLE_GOOD, ROLE_BAD = "good", "bad"
STAT_1_KEY = 'safety'
STAT_2_KEY = 'money'
COM_DESCR_KEY = "common_description"
scenario = []
round_d = dict()
role_d = dict()
choices_d = []
choice_d = dict()

data = pd.read_csv('../tests/test_scenario.csv')

s_x, s_y = data.shape

print(s_x, s_y)
print(data.info())
mask = data.round_index == 1
t_data = 0
print(data[data.round_index == 1]['good.text'].iloc[1])
for r_number in range(1, data.round_index.max()+1):
    d = data[data.round_index == 1]
    print(d.index)
    for role_i in ROLE_GOOD, ROLE_BAD:
        for choice_i in d.index:
            choice_d[TEXT_KEY] = d[role_i+'.'+CHOISES_KEY+'.'+TEXT_KEY].iloc[choice_i]
            choice_d[STAT_1_KEY] = d[role_i+'.'+CHOISES_KEY+'.'+STAT_1_KEY].iloc[choice_i]
            choices_d.append(choice_d)
        role_d[CHOISES_KEY] = choices_d
        role_d[TEXT_KEY] = d[role_i+'.'+TEXT_KEY]
        round_d[role_i] = role_d
    round_d[COM_DESCR_KEY] = d.common_description.iloc[0]
    scenario.append(round_d)
print(data.columns)
print(scenario)
