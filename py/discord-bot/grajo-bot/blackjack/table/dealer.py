from blackjack.table.stats import Stats

class Dealer:
    def __init__(self, dealer_data=None):
        self.hand = []
        self.stats = Stats(dealer_data)

    def deal(self, card):
        self.hand.append(card)

    def show_hand(self):
        print(f"{self.hand[0]} ??")

    def clear_hand(self):
        self.hand = []
