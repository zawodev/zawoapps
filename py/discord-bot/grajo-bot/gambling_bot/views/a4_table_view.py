import discord

from gambling_bot.casino import casino
from gambling_bot.models.table.table import Table
from gambling_bot.models.table.table_type import TableType
from gambling_bot.views.table_view.blackjack_table_view import BlackjackTableView
from gambling_bot.views.table_view.poker_table_view import PokerTableView
from gambling_bot.views.table_view.table_view import TableView


async def display(interaction: discord.Interaction, table: Table):

    view: TableView

    table_type = str(table.table_data.path[-2])
    if table_type == str(TableType.BLACKJACK):
        view = BlackjackTableView(table) # noqa
    elif table_type == TableType.POKER:
        view = PokerTableView(table) # noqa
    else:
        raise ValueError(f"Unknown table type: {table_type}")

    embed = view.create_embed()

    if table.active_game_message is not None:
        await table.active_game_message.edit(embed=embed, view=view)
    else:
        msg = await interaction.channel.send(embed=embed, view=view)
        table.start_game(msg)

    await interaction.response.defer()
