class Hand:
    def __init__(self):
        self.cards = []
        self.bet = 0

        self.finished = False
        self.is_hidden = False # ❌ ❓ 🎲 ✅
        self.is_ready = True

    def __str__(self):
        # ustawienia na podstawie stanu gry
        state_mapping = {False: ("❌", "playing"), True: ("✅", "finished")}
        emoji, description = state_mapping[self.finished]
        state_output = f"{emoji} {description}"

        # wyświetlanie stawki w zależności od is_hidden
        bet_output = f"{'pot' if self.is_hidden else 'bet'}: {self.bet}$"

        # formatowanie ręki, jeśli is_hidden jest aktywne i gra nie zakończona
        if not self.is_ready:
            hand_output = "hand: ?? ??"
        elif self.is_hidden and not self.finished:
            hand_output = f"hand: {str(self.cards[0])} ??" if self.cards else "hand: ?? ??"
        else:
            hand_output = "hand: " + " ".join(str(card) for card in self.cards) if self.cards else "hand: ?? ??"

        return f"{state_output}\n{bet_output}\n{hand_output}"

    def deal(self, card1, card2):
        self.cards = [card1, card2]

    # ------------- HAND ACTIONS -------------

    def add_bet(self, amount: int):
        self.bet += amount

    def bust(self):
        self.finished = True

    def blackjack(self):
        self.finished = True

    # ------------- HAND ACTIONS -------------

    def stand(self):
        self.finished = True

    def hit(self, card):
        self.cards.append(card)

    def split(self, card1, card2):
        second_hand = Hand()
        second_hand.cards.append(self.cards.pop())
        second_hand.cards.append(card2)
        self.cards.append(card1)
        return second_hand

    def double(self, card):
        self.bet *= 2
        self.hit(card)
        self.stand()

    def forfeit(self):
        self.bet //= 2
        self.finished = True

    # ------------- HAND ACTIONS -------------

    def value(self):
        return self.values()[-1]

    def values(self):

        if not self.is_ready:
            return [0]

        has_ace = False
        values = []
        value = 0

        cards_to_count = self.cards[:1] if self.is_hidden else self.cards

        for card in cards_to_count:
            value += card.value()
            if card.rank == 'A':
                has_ace = True

        values.append(value)
        if has_ace and value <= 11:
            values.append(value + 10)

        return values
