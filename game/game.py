import logging

from player import Player


class Game:
    def __init__(self):
        self.moveCount = 0
        self.safety = 100
        self.players = [Player(100, "good"), Player(70, "bad")]
        logging.info("Game created")
