import discord
from gambling_bot.models.table.table import Table
from gambling_bot.views.table_view import table_view
from discord.ui import Button


async def display(interaction: discord.Interaction, table: Table):
    embed = discord.Embed(title=table.table_data.path[-1], description="opis stolu konkretnego", color=0xffff00)
    view = BetSelectView(table)
    await interaction.response.send_message(embed=embed, view=view)


def _create_button_callback(table: Table, bet: int):
    async def button_callback(interaction: discord.Interaction):
        await table_view.display(interaction, table, bet)
    return button_callback

class BetSelectView(discord.ui.View):
    def __init__(self, table: Table):
        super().__init__()
        for bet in table.table_data['bets']:
            bet_name = f"bet {bet}"
            bet_unq_id = f"{table.table_data.path[-1]}_{table.table_data.path[-2]}_{bet}"
            button = Button(
                label=bet_name,
                style=discord.ButtonStyle.blurple, custom_id=bet_unq_id
            )
            button.callback = _create_button_callback(table, bet)
            self.add_item(button)
