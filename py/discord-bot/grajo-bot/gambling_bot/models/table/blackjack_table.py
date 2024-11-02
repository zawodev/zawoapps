from tabnanny import check

from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.table.table import Table
from gambling_bot.models.player import Player

class BlackJackTable(Table):
    def __init__(self, dealer, data, *path):
        super().__init__(dealer, data, *path)

    def hit(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.all_hands_stand():
            player.hit(self.dealer.deck.draw())

    def stand(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.all_hands_stand():
            player.stand()

    def double(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.all_hands_stand() and player.has_chips(player.hands[0].bet):
            player.profile.transfer_chips(self.dealer.profile, player.hands[0].bet)
            player.double(self.dealer.deck.draw())

    def split(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.all_hands_stand() and player.has_chips(player.hands[0].bet) and not player.split_used:
            player.profile.transfer_chips(self.dealer.profile, player.hands[0].bet)
            player.split(self.dealer.deck.draw(), self.dealer.deck.draw())

    def forfeit(self, player_id):
        player: Player = self.get_player(player_id)
        if player.is_ready and not player.all_hands_stand():
            player.forfeit()
