class Stats:
    def __init__(self, profile_data=None):
        # Name
        self.name = profile_data.get('name', 'Profile')

        # W/P/L
        self.wins = profile_data.get('wins', 0)
        self.pushes = profile_data.get('pushes', 0)
        self.losses = profile_data.get('losses', 0)

        # Cards and hands
        self.cards_drawn = profile_data.get('cards_drawn', 0)
        self.hands_played = profile_data.get('hands_played', 0)

        # Result
        self.blackjacks = profile_data.get('blackjacks', 0)
        self.busts = profile_data.get('busts', 0)

        # Actions
        self.doubles = profile_data.get('doubles', 0)
        self.splits = profile_data.get('splits', 0)
        self.stands = profile_data.get('stands', 0)
        self.hits = profile_data.get('hits', 0)

        # Money
        self.chips = profile_data.get('chips', 1000)
        self.total_won_chips = profile_data.get('total_won_chips', 0)
        self.total_lost_chips = profile_data.get('total_lost_chips', 0)
        self.biggest_win = profile_data.get('biggest_win', 0)
        self.biggest_loss = profile_data.get('biggest_loss', 0)
        self.max_chips = profile_data.get('max_chips', 1000)

        # Loans
        self.loans = profile_data.get('loans', 0)
        self.loans_paid = profile_data.get('loans_paid', 0)
        self.biggest_loan = profile_data.get('biggest_loan', 0)
        self.biggest_loan_paid = profile_data.get('biggest_loan_paid', 0)

        # By day
        self.total_games_by_day = profile_data.get('total_games_by_day', {})
        self.free_bet_by_day = profile_data.get('free_bet_by_day', {})


    def to_dict(self):
        return {
            "name": self.name,
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
