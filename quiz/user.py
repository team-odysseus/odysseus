#STEPS = reg
#       1qq
#       1qa
#       2qq
#       2qa
#       score


class User(object):
    def __init__(self):
        self.name = ''
        self.id = 0
        self.step = 0
    pass

    def set_name(self, name):
        self.name = name
    pass

    def set_id(self, id):
        self.id = id
    pass