class Hand:
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.stands = False
        self.forfeited = False

    def __str__(self):
        output = ""
        for card in self.cards:
            output += str(card) + " "
        return output

    def deal(self, card1, card2):
        self.cards = [card1, card2]

# ------------- HAND ACTIONS -------------

    def bet(self, amount):
        self.bet = amount

    def stand(self):
        self.stands = True

    def hit(self, card):
        self.cards.append(card)

    def split(self):
        second_hand = Hand()
        second_hand.cards.append(self.cards.pop())
        return second_hand

    def double(self):
        self.bet *= 2

    def forfeit(self):
        self.bet //= 2
        self.forfeited = True

# ------------- HAND ACTIONS -------------

    def value(self):
        has_ace = False
        values = []
        value = 0

        for card in self.cards:
            value += card.value()
            if card.rank == 'A':
                has_ace = True

        values.append(value)
        if has_ace and value <= 11:
            values.append(value + 10)

        return values

