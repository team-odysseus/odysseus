import logging


class Player:
    def __init__(self, _id, _iq, _role):
        # Telegram user id
        self.id = _id
        self.iq = _iq
        self.role = _role
        logging.debug("Player created " + str(self.iq) + " " + self.role)

