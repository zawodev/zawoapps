class Hand:
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.stands = False

    def __str__(self):
        output = ""
        for card in self.cards:
            output += str(card) + " "
        return output

    def deal(self, card1, card2):
        self.cards = [card1, card2]

    def hit(self, card):
        self.cards.append(card)

    def stand(self):
        self.stands = True

    def double(self):
        self.bet *= 2

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

