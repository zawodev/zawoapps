from gambling_bot.models.dict_data.dict_data import DictData

class TableData(DictData):

    def __init__(self, data, *path):
        default_table = {
            "chips": 0,
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
            "max_chips": 0,
            "loans": 0,
            "loans_paid": 0,
            "total_freebets": 0,
            "freebets_won": 0,
            "freebets_lost": 0,
            "total_games_dates": [],
            "freebet_dates": []
        }
        table_data = data or {}
        default_table.update(table_data)
        super().__init__(default_table, *path)


    def __str__(self):
        return (
            f"🪙 Hajs: {self.chips}\n"
            f"🏆 Wygrane: {self.wins}\n"
            f"🤝 Remisy: {self.pushes}\n"
        )
