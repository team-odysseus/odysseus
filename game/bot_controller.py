import logging
from game.game import Game


class BotController:
    def __init__(self, _com):
        self.game = Game()
        self.game.com = _com
        pass

    def player_start(self, player_id):
        joined = self.game.join(player_id)
        if self.game.is_ready():
            logging.info("Game starts")
            self.game.start()
        return joined

    def player_message(self, player_id, text):
        self.game.player_move(player_id, choice=int(text))

