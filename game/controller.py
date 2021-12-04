import logging

import game


class Controller:
    def __init__(self, _game):
        self.game = _game
        pass

    def game_loop(self):
        logging.info("Game starts")
        self.game.start()
        while True:
            break
        logging.info("Game is over")
