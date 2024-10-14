class Stats:
    def __init__(self):
        # Display name
        self.display_name = "Player"

        # W/P/L
        self.wins = 0
        self.pushes = 0
        self.losses = 0

        # Cards and hands
        self.cards_drawn = 0
        self.hands_played = 0

        # Result
        self.blackjacks = 0
        self.busts = 0

        # Actions
        self.doubles = 0
        self.splits = 0
        self.stands = 0
        self.hits = 0

        # Money
        self.total_won_chips = 0
        self.total_lost_chips = 0
        self.biggest_win = 0
        self.biggest_loss = 0
        self.max_chips = 0

        # Loans
        self.loans = 0
        self.loans_paid = 0
        self.biggest_loan = 0
        self.biggest_loan_paid = 0

        # By day
        self.total_games_by_day = {}
        self.free_bet_by_day = {}

    def to_dict(self):
        return {
            "display_name": self.display_name,
            "wins": self.wins,
            "pushes": self.pushes,
            "losses": self.losses,
            "cards_drawn": self.cards_drawn,
            "hands_played": self.hands_played,
            "blackjacks": self.blackjacks,
            "busts": self.busts,
            "doubles": self.doubles,
            "splits": self.splits,
            "stands": self.stands,
            "hits": self.hits,
            "total_won_chips": self.total_won_chips,
            "total_lost_chips": self.total_lost_chips,
            "biggest_win": self.biggest_win,
            "biggest_loss": self.biggest_loss,
            "max_chips": self.max_chips,
            "loans": self.loans,
            "loans_paid": self.loans_paid,
            "biggest_loan": self.biggest_loan,
            "biggest_loan_paid": self.biggest_loan_paid,
            "total_games_by_day": self.total_games_by_day,
            "free_bet_by_day": self.free_bet_by_day,
        }

