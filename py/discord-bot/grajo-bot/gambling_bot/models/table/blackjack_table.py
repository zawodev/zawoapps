from gambling_bot.models.table.table import Table


class BlackJackTable(Table):
    def __init__(self, data, *path):
        super().__init__(data, *path)
        self.table_data.data['type'] = 'blackjack'
