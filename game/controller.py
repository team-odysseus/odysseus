import logging

import game


class Controller:
    def __init__(self, _game):
        self.game = _game
        pass

    def game_loop(self):
        logging.info("Game starts")
        self.game.start()

        while not self.game.is_over():
            self.game.player_move(7374768, choice=0)
            self.game.player_move(8347838, choice=1)
            logging.info(f"Round {self.game.round_index} is over")
            self.game.advance_round()

        self.game.finish()

        logging.info("Game is over")
