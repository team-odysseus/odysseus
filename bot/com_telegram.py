from bot.bot import send_message


class ComTelegram:
    def __init__(self):
        self.player_list = None

    def set_players(self, _player_list):
        self.player_list = _player_list

    # send msg to all players
    def print_all(self, text):
        if self.player_list is not None:
            for player_id in self.player_list:
                send_message(player_id, text)

    # send msg to specific player
    def print_player(self, player_id, text):
        send_message(player_id, text)
