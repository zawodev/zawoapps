from gambling_bot.models.table.table import Table

class TexasHoldemTable(Table):
    def __init__(self, data, *path):
        super().__init__(data, *path)
