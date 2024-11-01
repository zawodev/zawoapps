from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.views.table_view.table_view import TableView
import discord
from gambling_bot.models.player import Player
from gambling_bot.views import a4_table_view


class BlackjackTableView(TableView):
    def __init__(self, table: BlackJackTable):
        super().__init__()
        self.table = table

    def create_embed(self):
        embed = discord.Embed(title="Blackjack game View", description="blackjack opis", color=0xffff00)

        for player in self.table.players:
            player: Player
            embed.add_field(name=player, value=player.get_hands_str(), inline=False)

        embed.add_field(name=self.table.dealer.profile.profile_data['name'], value=self.table.dealer.hand, inline=False)

        return embed

    @discord.ui.button(label="ready", style=discord.ButtonStyle.green, custom_id="ready")
    async def ready(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.ready(interaction.user.id)
        await a4_table_view.display(interaction, self.table)

    @discord.ui.button(label="hit", style=discord.ButtonStyle.green, custom_id="hit")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.hit(interaction.user.id)
        await a4_table_view.display(interaction, self.table)

    @discord.ui.button(label="stand", style=discord.ButtonStyle.red, custom_id="stand")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.stand(interaction.user.id)
        await a4_table_view.display(interaction, self.table)

    @discord.ui.button(label="double", style=discord.ButtonStyle.blurple, custom_id="double")
    async def double(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.double(interaction.user.id)
        await a4_table_view.display(interaction, self.table)

    @discord.ui.button(label="split", style=discord.ButtonStyle.gray, custom_id="split")
    async def split(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.split(interaction.user.id)
        await a4_table_view.display(interaction, self.table)

    @discord.ui.button(label="forfeit", style=discord.ButtonStyle.danger, custom_id="forfeit")
    async def forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.forfeit(interaction.user.id)
        await a4_table_view.display(interaction, self.table)
