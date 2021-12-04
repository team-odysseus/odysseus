class ComBase:
    def __init__(self):
        pass

    # send msg to all players
    def print_all(self, text):
        pass

    # send msg to specific player
    def print_player(self, player_id, text):
        pass


class ComConsole(ComBase):
    def __init__(self):
        super(ComBase, self).__init__()

    # send msg to all players
    def print_all(self, text):
        print("COMMON: " + text)

    # send msg to specific player
    def print_player(self, player_id, text):
        print("TO PLAYER: " + str(player_id) + " " + text)