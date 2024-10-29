from gambling_bot.models.hand import Hand
from gambling_bot.models.profile.profile import Profile

class Dealer:
    def __init__(self, profile: Profile):
        # self.name = name
        self.profile = profile
        #names = ['Marek', 'Romper', 'Extreme', 'Gambler', 'WYGRAŁEM', 'NIE', 'Fenomenalnie', 'Jogurt']
        #profile.profile_data.data['name'] = 'Dealer' + names.pop()

        # temporary, mid game class
        self.hand = Hand()

    def __str__(self):
        return self.profile.stats.name
        pass

    def deal(self, card1, card2):
        self.hand.deal(card1, card2)

    def hit(self, card):
        self.hand.hit(card)

    def stand(self):
        self.hand.stand()

    def clear_hand(self):
        self.hand = Hand()
