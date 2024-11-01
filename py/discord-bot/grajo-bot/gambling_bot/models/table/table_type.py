from enum import Enum

class TableType(Enum):
    BLACKJACK = "blackjack"
    POKER = "poker"

    # gamemodes
    ROULETTE = "roulette"
    SLOTS = "slots"
    SPIN_AND_PLAY = "spin_and_play"
    TEXAS_HOLDEM = "texas_holdem"
    WAR = "war"
    WHEEL_OF_FORTUNE = "wheel_of_fortune"
    YAHTZEE = "yahtzee"
    ZILCH = "zilch"

    def __str__(self):
        return str(self.value)
