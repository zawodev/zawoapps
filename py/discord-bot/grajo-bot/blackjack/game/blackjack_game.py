from blackjack.table.table import Table
from blackjack.table.player import Player
from blackjack.table.dealer import Dealer

import random

from blackjack.data_storage.json_data_storage import load_data
from blackjack.data_storage.create_empty_profile import create_empty_dealers


class BlackJackGame:
    def __init__(self, bot, casino_channel_id):
        self.bot = bot
        self.casino_channel_id = casino_channel_id

        self.table_amount = None
        self.casino_channel = None
        self.threads = None

        create_empty_dealers(['Marek', 'Jarek', 'Darek', 'Fifonż', 'Wojtek', 'Piotrek', 'Kuba'])

        self.dealers = [Dealer(dealer_key) for dealer_key in load_data('dealers').keys()]
        self.players = [Player(player_key) for player_key in load_data('players').keys()]
        self.tables = []
        self.create_tables() # możliwe że to musi być w setup bo nie wiem czy sie podmieni???

    async def setup(self):
        self.casino_channel = await self.bot.fetch_channel(self.casino_channel_id)
        self.threads = await self.casino_channel.threads()
        self.table_amount = len(self.threads) + 1

    def create_table(self, channel):
        table_dealer = random.choice(self.dealers)
        self.dealers.remove(table_dealer)
        return Table(table_dealer, channel, 1, 10, 1000)

    def create_tables(self):
        self.tables.append(self.create_table(self.casino_channel))  # main table
        for thread in self.threads:
            self.tables.append(self.create_table(thread))  # other tables

    def add_player(self, player):
        self.players.append(player)
        player.save()

    def get_player(self, profile_id):
        for player in self.players:
            if player.profile_id == profile_id:
                return player
        return None

    def get_table(self, channel_id):
        for table in self.tables:
            if table.channel.id == channel_id:
                return table
        return None
