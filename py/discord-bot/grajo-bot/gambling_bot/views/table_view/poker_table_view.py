from gambling_bot.models.table.poker_table import PokerTable
from gambling_bot.views.table_view.table_view import TableView
import discord


class PokerTableView(TableView):
    def __init__(self, table: PokerTable):
        super().__init__()
        self.table = table

    def create_embeds(self):
        pass

    @discord.ui.button(label="call", style=discord.ButtonStyle.green, custom_id="call")
    async def call(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.call(interaction.user.id)

    @discord.ui.button(label="raise", style=discord.ButtonStyle.red, custom_id="raise")
    async def raise_(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.raise_bet(interaction.user.id)

    @discord.ui.button(label="fold", style=discord.ButtonStyle.blurple, custom_id="fold")
    async def fold(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.fold(interaction.user.id)

    @discord.ui.button(label="check", style=discord.ButtonStyle.gray, custom_id="check")
    async def check(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.check(interaction.user.id)

    @discord.ui.button(label="all in", style=discord.ButtonStyle.danger, custom_id="all_in")
    async def all_in(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.all_in(interaction.user.id)
