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
        self.bet_used = False

    def save(self):
        self.profile.profile_data.save()


    def __eq__(self, other):
        if isinstance(other, str):
            return self.profile.__eq__(other)
        elif isinstance(other, Player):
            return self.profile.__eq__(other.profile)
        return False

    def __str__(self):
        return self.profile.__str__()

    def print_hands(self):
        # print his hands and bets
        pass

    # ------------- GAME ACTIONS -------------

    def ready(self):
        self.hands[self.active_hand].ready()

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
        self.hands[self.active_hand].stand()

    def hit(self, card):
        self.hands[self.active_hand].hit(card)

    def split(self, card1, card2):
        self.hands.append(self.hands[0].split(card1, card2))
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

    def finish(self):
        self.hands = [Hand()]
        self.active_hand = 0
        self.split_used = False
        self.bet_used = False
        self.player_state = 2

    def has_chips_or_notify(self, interaction: discord.Interaction, amount: int):
        if not self.profile.has_chips(amount):
            interaction.response.send_message("Nie masz wystarczająco żetonów!", ephemeral=True)
            return False
        return True
