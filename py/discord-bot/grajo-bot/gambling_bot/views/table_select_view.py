import discord
from discord.ui import Button
from gambling_bot.casino import casino
from gambling_bot.models.table.table import Table
from gambling_bot.views import bet_select_view

# display blackjack tables
async def display_blackjack_tables(interaction: discord.Interaction):
    embed = discord.Embed(title="Blackjack Tables", description="<tu wstaw descrtpipion>", color=0x00ff00)
    tables = casino.blackjack_tables
    view = TableSelectView(tables)
    await interaction.response.send_message(embed=embed, view=view)

async def display_texas_holdem_tables(interaction: discord.Interaction):
    embed = discord.Embed(title="Texas Holdem Tables", description="<tu wstaw descrtpipion>", color=0x00ff00)
    tables = casino.texas_holdem_tables
    view = TableSelectView(tables)
    await interaction.response.send_message(embed=embed, view=view)

async def display_spin_and_play_tables(interaction: discord.Interaction):
    embed = discord.Embed(title="Spin and Play Tables", description="<tu wstaw descrtpipion>", color=0x00ff00)
    tables = casino.spin_and_play_tables
    view = TableSelectView(tables)
    await interaction.response.send_message(embed=embed, view=view)

def _create_button_callback(table: Table):
    async def button_callback(interaction: discord.Interaction):
        await bet_select_view.display(interaction, table)
    return button_callback

class TableSelectView(discord.ui.View):
    def __init__(self, tables):
        super().__init__()
        for table in tables:
            table_name = f"{table.table_data.path[-1]}"
            table_unq_id = f"{table.table_data.path[-1]}_{table.table_data.path[-2]}"
            button = Button(
                label=table_name,
                style=discord.ButtonStyle.secondary,
                custom_id=table_unq_id
            )
            button.callback = _create_button_callback(table)
            self.add_item(button)
