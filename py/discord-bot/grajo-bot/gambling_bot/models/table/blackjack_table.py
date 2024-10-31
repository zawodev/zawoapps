from gambling_bot.models.table.table import Table

class BlackJackTable(Table):
    def __init__(self, data, *path):
        super().__init__(data, *path)

    def hit(self, player_id):
        pass

