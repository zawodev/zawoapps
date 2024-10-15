from blackjack.data_storage.json_data_storage import save_data, load_data

class Table:
    def __init__(self, dealer, n_decks=1, min_bet=10, max_bet=1000):
        self.n_decks = n_decks
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.shoe = Shoe(n_decks) # Shoe meaning a collection of decks
        self.players = []
        self.dealer = dealer

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

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

    def play(self, n_rounds=100):
        for _ in range(n_rounds):
            self.play_round()
            self.shoe.shuffle()

    def save_player_stats(self):
        players = {}
        for player in self.players:
            players[str(player.user_id)] = player.stats.to_dict()
