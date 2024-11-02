from gambling_bot.models.dict_data.dict_data import DictData

class TableData(DictData):

    def __init__(self, data, *path):
        default_data = {
            'name': "Table",
            'description': "Table description",
            'bets': [10],
            'max_bet': 1000,
            'chips_placed': 0,
        }
        super().__init__(default_data, data, *path)


    def __str__(self):
        return (
            f"🎰 {self['name']}\n"
            f"📝 {self['description']}\n"
            f"🎲 Zakłady: {self['bets']}\n"
            f"💰 Max zakład: {self['max_bet']}\n"
            f"🪙 Hajs: {self['chips_placed']}\n"
        )
