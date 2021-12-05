import role

TEXT_KEY = "text"
CHOISES_KEY = "choices"

class Round:
    def __init__(self, _dict=None):
        if _dict is not None:
            self.config = _dict
            return
        self.config = {"common_description": "Hello, round starts",
                       "good": {"text": "You should change password.",
                                "choices": [{"text": "Choice A",
                                             "safety": -10,
                                             "money": -100},
                                            {"text": "Choice B",
                                             "safety": 20,
                                             "money": -50}]},
                       "bad": {"text": "You should find out password.",
                               "choices": [{"text": "Kill all",
                                            "safety": -10},
                                           {"text": "Kill one",
                                            "safety": -50}]}}

    def get_round_description(self):
        return self.config['common_description']

    def get_role_choices(self, r_role:str):
        return [c for c in iter(self.config[r_role][CHOISES_KEY]) if c != TEXT_KEY]

    def get_role_text(self, r_role: str):
        return self.config[r_role][TEXT_KEY]

    def print_role_options(self, r_role: str):
        choices = self.get_role_choices(r_role)
        i = 1
        choices_text = []
        for choice in choices:
            choices_text.append(str(i) + " : " + choice[TEXT_KEY])
            i += 1
        return self.get_role_text(r_role) + " Your options: " + ", ".join(choices_text)

    def get_choice_stat(self, r_role, choice):
        stats = self.config[r_role][CHOISES_KEY][choice]
        stats.pop(TEXT_KEY)
        return stats
