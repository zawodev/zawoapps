from gambling_bot.models.hand import Hand
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.deck import Deck

class Dealer:
    def __init__(self, profile: Profile):
        self.profile = profile
        self.hand = None
        self.deck = None
        self.init()

    def save(self):
        self.profile.save()

    def __str__(self): #❌ if is not ready + profile to str
        emoji = "✅" if self.hand.is_ready else "❌"
        return f"{emoji} {self.profile}"

    def init(self):
        self.deck = Deck()
        self.hand = Hand()

        self.hand.deal(self.deck.draw(), self.deck.draw())
        while self.hand.value() < 17:
            self.hand.hit(self.deck.draw())

        self.hand.is_dealer = True
        self.hand.is_ready = False
        self.hand.is_hidden = True
