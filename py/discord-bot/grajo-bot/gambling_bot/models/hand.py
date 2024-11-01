class Hand:
    def __init__(self):
        self.cards = []
        self.bet = 0
        #self.stands = False
        #self.forfeited = False
        self.hand_state = 0 # 0 - not ready, 1 - playing, 2 - finished

    def __str__(self):
        state_mapping = {
            0: ("❌", "not ready"),
            1: ("🎲", "playing"),
            2: ("✅", "finished")
        }
        emoji, description = state_mapping.get(self.hand_state, ("❓", "error"))
        state_output = f"{emoji} {description}"

        bet_output = f"bet: {self.bet}$"

        if not self.cards:
            hand_output = "hand: Empty hand"
        else:
            hand_output = "hand: " + " ".join(str(card) for card in self.cards)

        return f"{state_output}\n{bet_output}\n{hand_output}"

    def deal(self, card1, card2):
        self.cards = [card1, card2]

    # ------------- HAND ACTIONS -------------

    def ready(self):
        self.hand_state = 1

    def place_bet(self, amount):
        self.bet = amount

    def stand(self):
        self.hand_state = 2

    def hit(self, card):
        self.cards.append(card)

    def split(self, card1, card2):
        second_hand = Hand()
        second_hand.cards.append(self.cards.pop())
        second_hand.cards.append(card2)
        self.cards.append(card1)
        return second_hand

    def double(self):
        self.bet *= 2

    def forfeit(self):
        self.bet //= 2
        self.hand_state = 2

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
