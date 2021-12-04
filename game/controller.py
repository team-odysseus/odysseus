import logging

import game


class Controller:
    def __init__(self, _game):
        self.game = _game
        pass

    def game_loop(self):
        logging.info("Game starts")
        self.game.start()
        self.game.player_move(7374768, choice=0)
        self.game.player_move(8347838, choice=1)
        #self.game.player_move(666, choice=1)

        logging.info("Round 1 is over")
        while True:
            break
        logging.info("Game is over")
