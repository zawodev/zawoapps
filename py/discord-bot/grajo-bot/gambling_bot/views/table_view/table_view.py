import discord

from gambling_bot.models.player import Player
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.table.table import Table

def create_player(profile: Profile, table: Table):
    player_id = profile.profile_data.path[-1]
    if player_id not in table.players:
        table.players.append(Player(profile))

class TableView(discord.ui.View):
    def __init__(self):
        super().__init__()

    def create_embeds(self):
        pass
