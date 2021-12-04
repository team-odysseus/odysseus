import logging

import game


class Controller:
    def __init__(self, _game):
        self.game = _game
        pass

    def game_loop(self):
        logging.info("Game starts")
        self.game.start()
        self.game.player_move(1, answer={"influence": 20, "text": "Good move"})
        self.game.player_move(2, answer={"influence": -30, "text": "Bad move"})
        logging.info("Round 1 is over")
        while True:
            break
        logging.info("Game is over")
