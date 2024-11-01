from gambling_bot.models.table.table import Table

class PokerTable(Table):
    def __init__(self, dealer, data, *path):
        super().__init__(data, *path)
        self.dealer = dealer

    def check(self, player_id):
        pass

    def call(self, player_id):
        pass

    def raise_bet(self, player_id):
        pass

    def fold(self, player_id):
        pass

    def all_in(self, player_id):
        pass
