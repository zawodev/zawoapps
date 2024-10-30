import discord
from gambling_bot.models.table.table_data import TableData

class Table:
    def __init__(self, data, *path):
        self.table_data = TableData(data, *path)
        self.game_active = False
        self.players = []

    def add_player(self, player, bet):
        self.players.append((player, bet))
