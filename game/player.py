import logging


class Player:
    def __init__(self, _iq, _role):
        self.iq = _iq
        self.role = _role
        logging.debug("Player created " + str(self.iq) + " " + self.role)

