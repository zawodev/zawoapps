import discord

from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.hand import Hand


class Player:
    def __init__(self, profile: Profile):
        # self.name = name
        self.profile = profile

        # temporary, mid game class
        self.hands = [Hand()]  # Karty na każdą rękę
        self.active_hand = 0

        self.split_used = False
        self.is_ready = False

    def save(self):
        self.profile.save()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.profile.__eq__(other)
        elif isinstance(other, Player):
            return self.profile.__eq__(other.profile)
        return False

    def __str__(self): #❌ if is not ready + profile to str
        emoji = "✅" if self.is_ready else "❌"
        return f"{emoji} {self.profile}"

    def get_hands_str(self):
        return "\n".join(str(hand) for hand in self.hands)

    def check(self):
        hand_value = self.get_current_hand().value()
        if hand_value > 21:
            self.get_current_hand().bust()
            if self.split_used:
                self.active_hand = 1
        elif hand_value == 21:
            self.get_current_hand().blackjack()
            if self.split_used:
                self.active_hand = 1

    # ------------- GAME ACTIONS -------------

    def deal(self, card1, card2):
        self.hands[0].deal(card1, card2)

    def ready(self):
        self.is_ready = True

    def add_bet(self, amount):
        self.hands[0].add_bet(amount)

    def get_bet(self):
        return self.hands[0].bet

    def get_all_bets(self):
        return sum(hand.bet for hand in self.hands)

    def all_hands_stand(self):
        return all(hand.is_finished for hand in self.hands)

    # ------------- HAND ACTIONS -------------

    def stand(self):
        self.hands[self.active_hand].stand()
        if self.split_used:
            self.active_hand = 1

    def hit(self, card):
        self.hands[self.active_hand].hit(card)
        self.check()

    def split(self, card1, card2):
        self.hands.append(self.hands[0].split(card1, card2))
        self.split_used = True

    def double(self, card):
        self.hands[self.active_hand].double(card)
        self.check()
        if self.split_used:
            self.active_hand = 1

    def forfeit(self):
        self.hands[self.active_hand].forfeit()
        if self.split_used:
            self.active_hand = 1

    # ------------- HAND ACTIONS -------------

    def has_chips(self, amount: int):
        return self.profile.has_chips(amount)

    def get_current_hand(self):
        return self.hands[self.active_hand]
