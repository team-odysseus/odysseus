import logging
from game.game import Game


class BotController:
    def __init__(self, _com):
        self.game = None
        self.com = _com
        self.game_restart()

    def game_restart(self):
        self.game = Game()
        self.game.com = self.com

    def player_start(self, player_id):
        joined = self.game.join(player_id)
        if self.game.is_ready():
            logging.info("Game starts")
            self.game.start()
        return joined

    def player_message(self, player_id, text):
        try:
            self.game.player_move(player_id, choice=int(text))
        except ValueError:
            pass


