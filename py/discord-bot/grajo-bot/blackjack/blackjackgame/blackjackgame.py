from blackjack.table.table import Table
from blackjack.table.player import Player
from blackjack.table.dealer import Dealer
from blackjack.table.profile import Profile

from blackjack.data_storage.txt_data_storage import load_data_as_list

import discord

import random

from blackjack.data_storage.json_data_storage import load_data

class BlackJackGame:
    def __init__(self, bot, casino_channel_id):
        self.bot = bot
        self.casino_channel_id = casino_channel_id

        self.table_amount = None
        self.casino_channel = None
        self.threads = None

        self.player_profiles = [Profile('players', player_key) for player_key in load_data('players').keys()]
        self.dealer_profiles = [Profile('dealers', dealer_key) for dealer_key in load_data('dealers').keys()]
        self.available_dealers = [Dealer(dealer_profile) for dealer_profile in self.dealer_profiles]

        self.tables = []


    async def setup(self):
        self.casino_channel = await self.bot.fetch_channel(self.casino_channel_id)
        self.threads = await self.casino_channel.threads()
        self.table_amount = len(self.threads) + 1

        dealer_names = load_data_as_list() #dziwne

        while len(self.available_dealers) < self.table_amount:
            self.available_dealers.append(Dealer(Profile('dealers', str(len(self.available_dealers) + 1))))

        self.create_tables()


    def create_table(self, channel):
        table_dealer = random.choice(self.available_dealers)
        self.available_dealers.remove(table_dealer)
        return Table(table_dealer, channel, 1, 10, 1000)


    def create_tables(self):
        self.tables.append(self.create_table(self.casino_channel))  # main table
        for thread in self.threads:
            self.tables.append(self.create_table(thread))  # other tables

# -----------------------

    async def get_table_or_notify(self, interaction: discord.Interaction):
        def get_table(channel_id):
            for _ in self.tables:
                if _.channel.id == channel_id:
                    return _
            return None

        table = get_table(interaction.channel_id)

        if table is None:
            await interaction.response.send_message(
                f"Nie możesz grać w blackjacka poza kasynem mordo, zapraszamy na <#{self.casino_channel.id}>",
                ephemeral=True
            )
        return table

# -----------------------

    def get_player_profile(self, profile_id):
        for profile in self.player_profiles:
            if profile.profile_id == str(profile_id):
                return profile
        new_profile = Profile('players', str(profile_id))
        self.player_profiles.append(new_profile)
        return new_profile

# -----------------------
