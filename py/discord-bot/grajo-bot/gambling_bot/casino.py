from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.dealer.dealer import Dealer
from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.models.table.spin_and_play_table import SpinAndPlayTable
from gambling_bot.models.table.texas_holdem_table import TexasHoldemTable
from gambling_bot.data.json_manager import load_data

class Casino:
    def __init__(self):
        self.bot = None

        self.player_profiles = [Profile(player_data, 'profiles', 'players', player_key)
                                for player_key, player_data in load_data('profiles', 'players').items()]
        self.dealer_profiles = [Profile(dealer_data, 'profiles', 'dealers', dealer_key)
                                for dealer_key, dealer_data in load_data('profiles', 'dealers').items()]
        self.available_dealers = [Dealer(dealer_profile) for dealer_profile in self.dealer_profiles]

        self.blackjack_tables = [BlackJackTable(table_data, 'tables', 'blackjack', table_key)
                                 for table_key, table_data in load_data('tables', 'blackjack').items()]
        self.spin_and_play_tables = [SpinAndPlayTable(table_data, 'tables', 'spin_and_play', table_key)
                                     for table_key, table_data in load_data('tables', 'spin_and_play').items()]
        self.texas_holdem_tables = [TexasHoldemTable(table_data, 'tables', 'texas_holdem', table_key)
                                    for table_key, table_data in load_data('tables', 'texas_holdem').items()]

    def setup(self, bot):
        self.bot = bot

# uzyskanie instancji casino
casino = Casino()
