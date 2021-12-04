import logging

import game.role as role
from game.player import Player
from game.round import Round

MAX_PLAYERS = 2


class Game:
    def __init__(self):
        self.round_index = 0
        self.players = list()
        self.start_iq = 100
        self.available_roles = [role.ROLE_GOOD, role.ROLE_BAD]
        self.rounds = [Round(), Round()]
        self.current_round = None
        self.com = None
        self.history = dict()
        self.stats = {"safety": 100,
                      "money": 10000}
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
        self.com.set_players(list([p.id for p in self.players]))
        self.com.print_all("Game start")
        self.current_round = self.rounds[0]
        self.announce_round()
        pass

    def announce_round(self):
        self.history[self.round_index] = []
        self.com.print_all(f"Round {self.round_index} starts: " + self.current_round.get_round_description())
        for p in self.players:
            role_instruction = self.current_round.print_role_options(p.role)
            self.com.print_player(p.id, role_instruction)

    def round_results(self):
        self.com.print_all("Round results: ")
#        for p in self.history[self.moveCount]:
#            self.com.print_all(str(p[0]) + ': ' + p[1]["text"])
        for stat, s_value in self.stats.items():
            self.com.print_all(stat + " is " + str(s_value))

    def player_move(self, player_id, choice: int):
        # TODO: check choice is valid
        self.history[self.round_index].append([player_id, choice])
        for p in self.players:
            if p.id == player_id:
                self.update_stats(p.role, p.iq, choice)
        if len(self.history[self.round_index]) == len(self.players):
            self.round_results()
            self.advance_round()

    def update_stats(self, p_role, p_iq, choice: int):
        for stat, increment in self.current_round.get_choice_stat(p_role, choice).items():
            self.stats[stat] += increment * p_iq / 100

    def advance_round(self):
        self.round_index += 1

        if not self.is_over():
            self.current_round = self.rounds[self.round_index]
            self.announce_round()
        else:
            self.current_round = None
            self.finish()

    def is_over(self):
        return self.round_index >= len(self.rounds)

    def finish(self):
        self.com.print_all(f"Game is over. Result {self.stats}")



