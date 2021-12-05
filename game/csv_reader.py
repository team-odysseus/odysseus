import pandas as pd

TEXT_KEY = "text"
CHOISES_KEY = "choices"
ROLE_GOOD, ROLE_BAD = "good", "bad"
STAT_1_KEY = 'safety'
STAT_2_KEY = 'money'
COM_DESCR_KEY = "common_description"


def load_rounds(csv_location='tests/test_scenario_2.csv'):
    scenario = []
    round_d = dict()
    role_d = dict()
    choices_d = []
    choice_d = dict()

    data = pd.read_csv(csv_location)
    for r_number in range(1, data.round_index.max()+1):
        d = data[data.round_index == r_number]
        for role_i in ROLE_GOOD, ROLE_BAD:
            for choice_i in range(d.index.min(), d.index.max()+1):
                choice_d[TEXT_KEY] = d[role_i+'_'+CHOISES_KEY+'_'+TEXT_KEY][choice_i]
                choice_d[STAT_1_KEY] = d[role_i+'_'+CHOISES_KEY+'_'+STAT_1_KEY][choice_i]
                choices_d.append(dict(choice_d))
                choice_d.clear()
            role_d[CHOISES_KEY] = list(choices_d)
            choices_d = []
            role_d[TEXT_KEY] = d[role_i+'_'+TEXT_KEY][d.index.min()]
            round_d[role_i] = dict(role_d)
            role_d.clear()
        round_d[COM_DESCR_KEY] = d.common_description[d.index.min()]
        scenario.append(dict(round_d))
        round_d.clear()

    return scenario

if __name__ == "__main__":
    print(load_rounds('../tests/test_scenario_2.csv'))
