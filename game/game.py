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
        self.history = dict()
        logging.info("Game created")

    def join(self, player_id):
        if len(self.available_roles) == 0:
            return False

        player_role = self.available_roles.pop()

        self.players.append(Player(player_id, self.start_iq, player_role))

        return True

    def is_ready(self):
        return len(self.players) == MAX_PLAYERS

    def start(self):
        self.com.print_all("Game start")
        self.current_round = self.rounds[0]
        self.announce_round()
        pass

    def announce_round(self):
        self.history[self.moveCount] = []
        self.com.print_all("Round starts: " + self.current_round.common_description)
        for p in self.players:
            role_instruction = self.current_round.get_role_text(p.role)
            self.com.print_player(p.id, role_instruction)

    def round_results(self):
        self.com.print_all("Round results: ")
        for p in self.history[self.moveCount]:
            self.com.print_all(str(p[0]) + ': ' + p[1]["text"])
        self.com.print_all("Safety is " + str(self.safety))

    def player_move(self, player_id, answer):
        self.history[self.moveCount].append([player_id, answer])
        self.safety += answer["influence"]
        if len(self.history[self.moveCount]) == len(self.players):
            self.round_results()


