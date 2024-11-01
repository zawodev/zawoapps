from gambling_bot.models.table.table import Table
from gambling_bot.models.player import Player

class BlackJackTable(Table):
    def __init__(self, dealer, data, *path):
        super().__init__(dealer, data, *path)

    def ready(self, player_id):
        player: Player = self.get_player(player_id)
        player.deal(self.dealer.deck.draw(), self.dealer.deck.draw())
        player.ready()

    def hit(self, player_id):
        player: Player = self.get_player(player_id)
        player.hit(self.dealer.deck.draw())

    def stand(self, player_id):
        player: Player = self.get_player(player_id)
        player.stand()

    def double(self, player_id):
        player: Player = self.get_player(player_id)
        player.double(self.dealer.deck.draw())

    def split(self, player_id):
        player: Player = self.get_player(player_id)
        player.split(self.dealer.deck.draw(), self.dealer.deck.draw())

    def forfeit(self, player_id):
        player: Player = self.get_player(player_id)
        player.forfeit()
