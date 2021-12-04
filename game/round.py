import role


class Round:
    def __init__(self):
        self.common_description = "Hello, round starts"
        self.role_descriptions = {role.ROLE_GOOD: ("You are very good.", ["Choice A", "Choice B"]),
                                  role.ROLE_BAD: ("You are so bad.", ["Kill all", "Kill one"])}

        pass

    def get_role_text(self, role_id):
        text, choices = self.role_descriptions[role_id]

        choices_text = [str(i + 1) + ": " + choice for i, choice in enumerate(choices)]

        return text + " Your options: " + ", ".join(choices_text)
