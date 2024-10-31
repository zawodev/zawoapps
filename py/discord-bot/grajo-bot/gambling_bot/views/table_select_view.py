import discord
from discord.ui import Button
from gambling_bot.casino import casino
from gambling_bot.models.table.table import Table
from gambling_bot.table_type import TableType
from gambling_bot.views import bet_select_view

async def display(interaction: discord.Interaction, table_type: TableType):
    embed = discord.Embed(title=table_type, description="opis", color=0xff14aa)
    tables = []
    if table_type == TableType.BLACKJACK:
        tables = casino.blackjack_tables
    elif table_type == TableType.TEXAS_HOLDEM:
        tables = casino.texas_holdem_tables
    elif table_type == TableType.SPIN_AND_PLAY:
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
