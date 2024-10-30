from gambling_bot.models.dict_data.dict_data import DictData

class TableData(DictData):

    def __init__(self, data, *path):
        default_data = {
            'bets': [10],
            'chips_placed': 0,
        }
        super().__init__(default_data, data, *path)


    def __str__(self):
        return (
            f"🪙 Hajs: {self['chips_placed']}\n"
            f"🎲 Zakłady: {self['bets']}\n"
            f"🎰 Typ: {self['type']}"
        )
