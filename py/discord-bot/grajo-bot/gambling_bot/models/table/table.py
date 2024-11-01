import discord
from gambling_bot.models.player import Player
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.table.table_data import TableData

class Table:
    def __init__(self, dealer, data, *path):
        self.table_data = TableData(data, *path)
        self.active_game_message = None
        self.players = []
        self.dealer = dealer

    def add_player(self, player_profile: Profile, bet: int):
        player = Player(player_profile)
        player.get_current_hand().place_bet(bet)

        self.players.append(player)

    def get_player(self, player_id):
        player_id = str(player_id)
        for player in self.players:
            if player.profile.profile_data.path[-1] == player_id:
                return player
        return None

    def start_game(self, game_message):
        self.active_game_message = game_message

    def end_game(self):
        self.active_game_message = None
        self.players = []
        self.dealer = None
        self.table_data.save()
