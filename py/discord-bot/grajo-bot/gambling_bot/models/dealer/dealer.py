from gambling_bot.models.hand import Hand
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.deck import Deck

class Dealer:
    def __init__(self, profile: Profile):
        self.profile = profile
        self.hand = Hand()
        self.deck = Deck()

        self.hand.deal(self.deck.draw(), self.deck.draw())
        while self.hand.value() < 17:
            self.hand.hit(self.deck.draw())

    def __str__(self):
        return self.profile.profile_data.data['name']
        pass

    def deal(self):
        self.hand.deal(self.deck.draw(), self.deck.draw())

    def hit(self):
        self.hand.hit(self.deck.draw())

    def stand(self):
        self.hand.stand()

    def clear_hand(self):
        self.hand = Hand()
