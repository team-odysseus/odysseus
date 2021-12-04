import role


class Round:
    def __init__(self):
        self.common_description = "Hello, round starts"
        self.role_descriptions = {
            role.ROLE_GOOD:
                {"text": "You should change password.",
                 "choices": [{"text": "Choice A",
                              "safety": -10,
                              "money": -100},
                             {"text": "Choice B",
                              "safety": 20,
                              "money": -50}]},
            role.ROLE_BAD:
                {"text": "You should find out password.",
                 "choices": [{"text": "Kill all",
                              "safety": -10},
                             {"text": "Kill one",
                              "safety": -50}]}}
        pass

    def get_role_text(self, role_id):
        text, choices = self.role_descriptions[role_id]

        choices_text = [str(i + 1) + ": " + choice for i, choice in enumerate(choices)]

        return text + " Your options: " + ", ".join(choices_text)
