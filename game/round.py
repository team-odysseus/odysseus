import role


class Round:
    def __init__(self):
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
        pass

    def load(self, file):
        self.config = dict()

    def get_role_text(self, role_id):
        text, choices = self.role_descriptions[role_id]

        choices_text = [str(i + 1) + ": " + choice for i, choice in enumerate(choices)]

        return text + " Your options: " + ", ".join(choices_text)
