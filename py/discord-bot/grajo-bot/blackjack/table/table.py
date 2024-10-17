from blackjack.data_storage.json_data_storage import save_data, load_data
from blackjack.table.hand import Hand
from blackjack.table.dealer import Dealer
from blackjack.table.deck import Deck
from blackjack.table.player import Player

class Table:
    def __init__(self, dealer: Dealer, channel, decks_in_deck=1, min_bet=10, max_bet=1000):
        self.decks_in_deck = decks_in_deck
        self.min_bet = min_bet
        self.max_bet = max_bet

        self.players = [] # jak pokazac ze to tablica obiektow klasy Player? dla interpretera python
        self.dealer = dealer

        self.deck = Deck(self.decks_in_deck)

        self.channel = channel

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def has_player(self, player):
        return player in self.players

    def bet(self, player, amount):
        if player.has_chips(amount):
            player.bet(amount)
        else:
            print("Not enough chips")



    def place_bets(self):
        for player in self.players:
            player.place_bet(self.min_bet, self.max_bet)

    def deal_initial_hands(self):
        for player in self.players:
            player.hand = Hand()
            player.deal_hand(self.deck.draw(), self.deck.draw())
        self.dealer.hand = Hand()
        self.dealer.hand.deal(self.deck.draw(), self.deck.draw())

    def play_round(self):
        self.place_bets()
        self.deal_initial_hands()
        for player in self.players:
            player.play(self.shoe, self.dealer)
        self.dealer.play(self.shoe)
        for player in self.players:
            player.resolve(self.dealer)

    def save_players(self):
        for player in self.players:
            player.save()
