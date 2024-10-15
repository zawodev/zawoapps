# w black jack py logika całej apki, potencjalanie kilka stołów jednocześnie
#w tym pliku logika gry na jednym stole cały przebieg stołu
from blackjack.blackjack import Dealer, dealer
# wblackjackpy robimy wszystkie discord slash komendy, które wywołują funkcje z innych plików

from blackjack.table.table import Table
from blackjack.table.player import Player


from blackjack.data_storage.json_data_storage import save_data, load_data

class BlackJackGame:
    def __init__(self, casino_channel_id, table_amount):
        self.casino_channel_id = casino_channel_id
        self.table_amount = table_amount

        self.dealer = Dealer(load_data('dealer'))
        self.players = [Player(player_data) for player_data in load_data('players').values()]
        self.tables = [Table(dealer, 1, 10, 1000) for _ in range(table_amount)]
