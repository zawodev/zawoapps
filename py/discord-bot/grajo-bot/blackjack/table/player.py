from blackjack.table.stats import Stats
from blackjack.table.profile import Profile

class Player(Profile):
    def __init__(self, player_id):
        super().__init__('players', player_id)

        # temporary, mid game
        self.bets = [0]  # Zakład na każdą rękę
        self.hands = [[]]  # Obsługuje do dwóch rąk
        self.active_hand = 0
        self.split_used = False

    def save(self):
        self.stats.save('players', self.profile_id)

    def __str__(self):
        return f'{self.stats.name} has {self.stats.chips}$'




    def transfer_chips(self, other, amount):
        self.stats.chips -= amount
        other.stats.chips += amount

    def deal_hand(self, card1, card2):
        if not self.hands[self.active_hand]:
            print("Hand is empty")
        self.hands[self.active_hand] = [card1, card2]



    def bet(self, amount):
        if self.bets[self.active_hand] > 0:
            print("Bet already placed")
        self.bets[self.active_hand] = amount

    def stand(self):
        self.active_hand += 1

    def hit(self, card):
        self.hands[self.active_hand].append(card)

        if self.split_used:
            self.active_hand += 1
            self.stands[self.active_hand] = False

    def split(self, card1, card2):
        self.hands.append([self.hands[0].pop()])
        self.hands[0].append(card1)
        self.hands[1].append(card2)

        self.bets[1] = self.bets[0]
        self.split_used = True

    def double(self, card):
        self.bets[self.active_hand] *= 2
        self.hit(card)
        self.stand()



    def win(self):
        self.stats.chips += self.bet
        self.stats.total_won_chips += self.bet

    def lose(self):
        self.stats.chips -= self.bet
        self.stats.total_lost_chips += self.bet

    def push(self):
        pass



    def get_hand_value(self):
        return self.hand_value

    def clear_hand(self):
        self.hand = []
        self.hand_value = 0

    def show_hand(self):
        print(f'{self.name} has:')
        for card in self.hand:
            print(f'{card.rank} of {card.suit}')

    def show_hand_value(self):
        print(f'{self.name} has {self.hand_value}')

    def show_bankroll(self):
        print(f'{self.name} has ${self.bankroll}')

    def show_bet(self):
        print(f'{self.name} bet ${self.bet}')

    def show_all(self):
        self.show_hand()
        self.show_hand_value()
        self.show_bankroll()
        self.show_bet()

    def is_busted(self):
        return self.hand_value > 21

    def is_blackjack(self):
        return self.hand_value == 21

    def is_21(self):
        return self.hand_value == 21

    def is_double_down(self):
        return len(self.hand) == 2

    def is_split(self):
        return len(self.hand) == 2 and self.hand[0].rank == self.hand[1].rank

    def is_surrender(self):
        return len(self.hand) == 2

    def is_insurance(self):
        return len(self.hand) == 2 and self.hand[0].rank == 'Ace'

    def is_even_money(self):
        return len(self.hand) == 2 and self.hand[0].rank == 'Ace'

    def is_soft_hand(self):
        return any(card.rank == 'Ace' for card in self.hand)

    def is_hard_hand(self):
        return not self.is_soft_hand()