from blackjack.table.stats import Stats
from blackjack.table.profile import Profile
from blackjack.table.hand import Hand
from blackjack.table.table import Table
import discord

class Player:
    def __init__(self, profile: Profile, table: Table):
        # self.name = name
        self.profile = profile
        self.table = table

        # temporary, mid game class
        self.hands = [Hand()]  # Karty na każdą rękę
        self.active_hand = 0
        self.split_used = False
        self.bet_used = False

    def save(self):
        self.profile.save()

    def __str__(self):
        return self.profile.stats.name

    def print_hands(self):
        # print his hands and bets
        pass

# ------------- GAME ACTIONS -------------

    def deal(self, card1, card2):
        self.hands[self.active_hand].deal(card1, card2)

    def is_finished(self):
        return self.active_hand == len(self.hands)

    def get_current_hand(self):
        return self.hands[self.active_hand]

# ------------- HAND ACTIONS -------------

    def bet(self, amount):
        self.hands[self.active_hand].bet(amount)
        self.bet_used = True

    def stand(self):
        self.active_hand += 1

    def hit(self, card):
        self.hands[self.active_hand].hit(card)

    def split(self):
        self.hands.append(self.hands[self.active_hand].split())
        self.split_used = True

    def double(self, card):
        self.hands[self.active_hand].double()
        self.hit(card)
        self.stand()

    def forfeit(self):
        self.hands[self.active_hand].forfeit()
        self.active_hand += 1

# ------------- HAND ACTIONS -------------

    def get_result(self):
        return

    def clear_hands(self):
        self.hands = [Hand()]

    def has_chips_or_notify(self, interaction: discord.Interaction, amount: int):
        if not self.profile.has_chips(amount):
            interaction.response.send_message("Nie masz wystarczająco żetonów!", ephemeral=True)
            return False
        return True
