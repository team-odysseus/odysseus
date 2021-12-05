class ComConsole:
    # send msg to all players
    def print_all(self, text):
        print("COMMON: " + text)

    # send msg to specific player
    def print_player(self, player_id, text):
        print("TO PLAYER: " + str(player_id) + " " + text)
