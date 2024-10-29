from gambling_bot.models.dict_data.dict_data import DictData

class ProfileData(DictData):

    def __init__(self, data, *path):
        default_profile = {
            "name": 'Profile',
            "wins": 0,
            "pushes": 0,
            "losses": 0,
            "cards_drawn": 0,
            "hands_played": 0,
            "blackjacks": 0,
            "busts": 0,
            "doubles": 0,
            "splits": 0,
            "stands": 0,
            "hits": 0,
            "chips": 1000,
            "total_won_chips": 0,
            "total_lost_chips": 0,
            "biggest_win": 0,
            "biggest_loss": 0,
            "max_chips": 1000,
            "loans": 0,
            "loans_paid": 0,
            "biggest_loan": 0,
            "biggest_loan_paid": 0,
            "total_freebets": 0,
            "freebets_won": 0,
            "freebets_lost": 0,
            "total_games_dates": {},
            "freebet_dates": {}
        }
        profile_data = data or {}
        default_profile.update(profile_data)
        super().__init__(default_profile, *path)


    def __str__(self):
        return (
            f"👤 Name: {self.data.get('name')}\n"
            f"🪙 Hajs: {self.chips}$\n"
            f"🏆 Wygrane: {self.wins}\n"
            f"🤝 Remisy: {self.pushes}\n"
            f"🥺 Porażki: {self.losses}\n"
            f"🃏 Karty: {self.cards_drawn}\n"
            f"🤲 Ręce: {self.hands_played}\n"
            f"🔥 Blackjacks: {self.blackjacks}\n"
            f"💥 Busts: {self.busts}\n"
            f"🔁 Double: {self.doubles}\n"
            f"🔀 Split: {self.splits}\n"
            f"🛑 Stand: {self.stands}\n"
            f"👊 Hit: {self.hits}\n"
            f"🏦 Max hajs: {self.max_chips}$\n"
            f"🏧 Pożyczki: {self.loans}\n"
            f"💸 Pożyczki spłacone: {self.loans_paid}\n"
            f"🎰 Freebety: {self.total_freebets}\n"
            f"🎰 Freebety wygrane: {self.freebets_won}\n"
            f"🎰 Freebety przegrane: {self.freebets_lost}\n"
            f"📅 Gry: {sum(self.total_games_dates)}\n"
            f"📅 Freebety: {len(self.freebet_dates)}\n"
        )
