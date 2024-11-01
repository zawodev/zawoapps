from tabnanny import check

from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.table.table import Table
from gambling_bot.models.player import Player

class BlackJackTable(Table):
    def __init__(self, dealer, data, *path):
        super().__init__(dealer, data, *path)

    def check(self):
        if all(player.stands() for player in self.players):
            self.end_game()

    def hit(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.stands():
            player.hit(self.dealer.deck.draw())

    def stand(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.stands():
            player.stand()

    def double(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.stands() and player.has_chips(player.hands[0].bet):
            player.double(self.dealer.deck.draw())

    def split(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.stands() and player.has_chips(player.hands[0].bet) and not player.split_used:
            player.split(self.dealer.deck.draw(), self.dealer.deck.draw())

    def forfeit(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.stands():
            player.forfeit()
