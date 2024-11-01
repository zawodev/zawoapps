from gambling_bot.views.table_view.table_view import TableView
from gambling_bot.models.table.blackjack_table import BlackJackTable
import discord
from gambling_bot.models.player import Player


class BlackjackTableView(TableView):
    def __init__(self, table: BlackJackTable):
        super().__init__()
        self.table = table

    def create_embed(self):
        embed = discord.Embed(title="Game View", description="opis", color=0xffff00)

        for player in self.table.players:
            player: Player
            embed.add_field(name=player.profile.profile_data['name'], value=player.get_current_hand(), inline=False)

        return embed

    @discord.ui.button(label="hit", style=discord.ButtonStyle.green, custom_id="hit")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.hit(interaction.user.id)

    @discord.ui.button(label="stand", style=discord.ButtonStyle.red, custom_id="stand")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="double", style=discord.ButtonStyle.blurple, custom_id="double")
    async def double(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="split", style=discord.ButtonStyle.gray, custom_id="split")
    async def split(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="forfeit", style=discord.ButtonStyle.danger, custom_id="forfeit")
    async def forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
