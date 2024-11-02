import discord
from discord.ui import Button
from gambling_bot.casino import casino
from gambling_bot.models.table.table import Table
from gambling_bot.models.table.table_type import TableType
from gambling_bot.views import a3_bet_select_view

async def display(interaction: discord.Interaction, table_type: TableType):
    embed = discord.Embed(title=table_type.value[0], description=table_type.value[1], color=0xff14aa)
    tables = []
    if table_type.value[0] == TableType.BLACKJACK.value[0]:
        tables = casino.blackjack_tables
    elif table_type.value[0] == TableType.POKER.value[0]:
        tables = casino.poker_tables
    view = TableSelectView(tables)
    await interaction.response.send_message(embed=embed, view=view)

def _create_button_callback(table: Table):
    async def button_callback(interaction: discord.Interaction):
        await a3_bet_select_view.display(interaction, table)
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
