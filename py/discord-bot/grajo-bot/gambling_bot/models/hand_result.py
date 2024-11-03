from enum import Enum

class HandResult(Enum):
    BLACKJACK = 2.5
    WIN = 2
    PUSH = 1
    FORFEIT = 0.5
    LOSE = 0
    BUST = 0
    NONE = 0

    def __float__(self):
        return float(self.value)

    def __str__(self):
        return self.name.lower()
