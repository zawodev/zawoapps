import discord

from gambling_bot.models.table.table_type import TableType
from gambling_bot.views import a2_table_select_view


async def display(interaction: discord.Interaction):
    embed = discord.Embed(title="Casino Bot", description="wersja: 0.28 alpha", color=0x00ff77)
    view = GameSelectView()
    await interaction.response.send_message(embed=embed, view=view)


class GameSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="blackjack", style=discord.ButtonStyle.blurple, custom_id="blackjack")
    async def blackjack(self, interaction: discord.Interaction, button: discord.ui.Button):
        await a2_table_select_view.display(interaction, TableType.BLACKJACK)

    @discord.ui.button(label="[poker]", style=discord.ButtonStyle.red, custom_id="texas_holdem")
    async def texas_holdem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await a2_table_select_view.display(interaction, TableType.POKER)
