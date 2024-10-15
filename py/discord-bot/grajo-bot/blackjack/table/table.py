from blackjack.data_storage.json_data_storage import save_data, load_data
from blackjack.table.hand import Hand
from blackjack.table.dealer import Dealer

class Table:
    def __init__(self, dealer: Dealer, channel, n_decks=1, min_bet=10, max_bet=1000):
        self.n_decks = n_decks
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.players = []
        self.dealer = dealer
        self.channel = channel

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def has_player(self, player_id):
        return any([player.user_id == player_id for player in self.players])

    def place_bets(self):
        for player in self.players:
            player.place_bet(self.min_bet, self.max_bet)

    def deal_initial_hands(self):
        for player in self.players:
            player.hand = Hand(self.shoe.draw(), self.shoe.draw())
        self.dealer.hand = Hand(self.shoe.draw(), self.shoe.draw())

    def play_round(self):
        self.place_bets()
        self.deal_initial_hands()
        for player in self.players:
            player.play(self.shoe, self.dealer)
        self.dealer.play(self.shoe)
        for player in self.players:
            player.resolve(self.dealer)

    def save_player_stats(self):
        players = {}
        for player in self.players:
            players[str(player.user_id)] = player.stats.to_dict()
        save_data('players', players)
