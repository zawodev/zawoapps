import discord

from gambling_bot.casino import casino
from gambling_bot.models.player import Player
from gambling_bot.models.table.table_data import TableData

class Table:
    def __init__(self, data, *path):
        self.table_data = TableData(data, *path)
        self.game_active = False
        self.players = []

    def add_player(self, interaction: discord.Interaction, bet: int):
        player_profile = casino.get_player_profile_with_id(str(interaction.user.id))
        player = Player(player_profile)
        player.get_current_hand().bet(bet)

        self.players.append(player)

    def get_player(self, player_id):
        for player in self.players:
            if player.profile.profile_data.path[-1] == player_id:
                return player
        return None

    def start_game(self):
        self.game_active = True

    def end_game(self):
        self.game_active = False
        self.players = []
        self.table_data.save()
