import discord
from gambling_bot.views import table_select_view


async def display(interaction: discord.Interaction):
    embed = discord.Embed(title="Casino Bot", description="wersja: 0.1 alpha", color=0x00ff00)
    view = GameSelectView()
    await interaction.response.send_message(embed=embed, view=view)

class GameSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="blackjack", style=discord.ButtonStyle.secondary, custom_id="blackjack")
    async def blackjack(self, interaction: discord.Interaction, button: discord.ui.Button):
        await table_select_view.display_blackjack_tables(interaction)

    @discord.ui.button(label="texas_holdem", style=discord.ButtonStyle.red, custom_id="texas_holdem")
    async def texas_holdem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await table_select_view.display_texas_holdem_tables(interaction)

    @discord.ui.button(label="spin_and_play", style=discord.ButtonStyle.gray, custom_id="spin_and_play")
    async def spin_and_play(self, interaction: discord.Interaction, button: discord.ui.Button):
        await table_select_view.display_spin_and_play_tables(interaction)
