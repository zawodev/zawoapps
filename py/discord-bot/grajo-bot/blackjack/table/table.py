from blackjack.data_storage.json_data_storage import save_data, load_data
from blackjack.old_blackjack import game_active
from blackjack.table.hand import Hand
from blackjack.table.dealer import Dealer
from blackjack.table.deck import Deck
from blackjack.table.profile import Profile


class Table:
    def __init__(self, dealer: Dealer, channel, decks_in_deck=1, min_bet=10, max_bet=1000):
        self.decks_in_deck = decks_in_deck
        self.min_bet = min_bet
        self.max_bet = max_bet

        self.players = []
        self.dealer = dealer

        self.deck = Deck(self.decks_in_deck)

        self.channel = channel
        self.game_active = False

# ------------- GAME ACTIONS -------------

    def remove_player_with_id(self, player_id):
        self.players.remove(player_id)

    def has_player_with_id(self, player_id):
        return any(player.profile.id == player_id for player in self.players)

    def get_player_with_id(self, player_id):
        return next(player for player in self.players if player.profile.id == player_id)

# ------------- GAME ACTIONS -------------

    def game_active_or_notify(self, interaction):
        if self.game_active:
            interaction.response.send_message("Gra już trwa!", ephemeral=True)
            return True
        return False

# ------------- GAME ACTIONS -------------

    def bet(self, player, amount: int):
        if player in self.players:
            player.bet(amount)
            player.profile.transfer_chips(self.dealer.profile, amount)
        else:
            print("Player not in table")

    def hit(self, player):
        if player in self.players:
            player.hit(self.deck.draw())
        else:
            print("Player not in table")

    def stand(self, player):
        if player in self.players:
            player.stand()
        else:
            print("Player not in table")

    def double(self, player):
        if player in self.players:
            player.double(self.deck.draw())
            player.profile.transfer_chips(self.dealer.profile, player.get_current_hand().bet)
        else:
            print("Player not in table")

    def split(self, player):
        if player in self.players:
            player.split()
            player.profile.transfer_chips(self.dealer.profile, player.get_current_hand().bet)
        else:
            print("Player not in table")

    def forfeit(self, player):
        if player in self.players:
            player.forfeit()
        else:
            print("Player not in table")

# ------------- GAME ACTIONS -------------

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
