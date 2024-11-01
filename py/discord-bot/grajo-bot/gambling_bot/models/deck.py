import random
from gambling_bot.models.card import Card

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['♠', '♥', '♦', '♣']

class Deck:
    def __init__(self, decks_in_deck=1):
        self.cards = [Card(rank, suit) for _ in range(decks_in_deck) for rank in ranks for suit in suits]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)
