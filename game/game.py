import logging

import role
from player import Player
from round import Round
import communications

MAX_PLAYERS = 2


class Game:
    def __init__(self):
        self.moveCount = 0
        self.safety = 100
        self.players = list()
        self.start_iq = 100
        self.available_roles = [role.ROLE_GOOD, role.ROLE_BAD]
        self.rounds = [Round(), Round()]
        self.current_round = None
        self.com = communications.ComConsole()
        logging.info("Game created")

    def join(self, player_id):
        if len(self.available_roles) == 0:
            return False

        player_role = self.available_roles.pop()

        self.players.append(Player(player_id, self.start_iq, player_role))

        if len(self.players) == MAX_PLAYERS:
            self.start()

        return True

    def start(self):
        self.com.print_all("Game start")
        self.current_round = self.rounds[0]
        self.announce_round()
        pass

    def announce_round(self):
        print("Round starts: " + self.current_round.common_description)
        for p in self.players:
            role_instruction = self.current_round.get_role_text(p.role)
            print("Player instructions {}: {} ".format(p.id, role_instruction))

    def player_move(self, player_id, answer):
        pass
