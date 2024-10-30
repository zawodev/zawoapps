import discord

from gambling_bot.table_type import TableType
from gambling_bot.casino import casino
from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.models.table.texas_holdem_table import TexasHoldemTable
from gambling_bot.models.table.spin_and_play_table import SpinAndPlayTable


async def add_table(interaction: discord.Interaction, table_type: TableType, table_name: str, bets: list):
    # można się pozbyć tego ifa jeśli zrównasz klasy oraz dasz type jako argument zamiast ręcznie
    if table_type == TableType.BLACKJACK:
        blackjack_table = BlackJackTable({'bets': bets}, 'tables', 'blackjack', table_name)
        casino.blackjack_tables.append(blackjack_table)
    elif table_type == TableType.TEXAS_HOLDEM:
        texas_holdem_table = TexasHoldemTable({'bets': bets}, 'tables', 'texas_holdem', table_name)
        casino.texas_holdem_tables.append(texas_holdem_table)
    elif table_type == TableType.SPIN_AND_PLAY:
        spin_and_play_table = SpinAndPlayTable({'bets': bets}, 'tables', 'spin_and_play', table_name)
        casino.spin_and_play_tables.append(spin_and_play_table)
    else:
        await interaction.response.send_message(f"table type not found", ephemeral=True)
        return
    await interaction.response.send_message(f"added table {table_type}", ephemeral=True)


async def remove_table(interaction: discord.Interaction, table_type: str, table_name: str):
    if table_type == "blackjack":
        for table in casino.blackjack_tables:
            if table.table_data.path[-1] == table_name:
                table.table_data.delete()
                casino.blackjack_tables.remove(table)
                break
    elif table_type == "texas_holdem":
        for table in casino.texas_holdem_tables:
            if table.table_data.path[-1] == table_name:
                table.table_data.delete()
                casino.texas_holdem_tables.remove(table)
                break
    elif table_type == "spin_and_play":
        for table in casino.spin_and_play_tables:
            if table.table_data.path[-1] == table_name:
                table.table_data.delete()
                casino.spin_and_play_tables.remove(table)
                break
    else:
        await interaction.response.send_message(f"table type not found", ephemeral=True)
        return
    await interaction.response.send_message("removed table", ephemeral=True)
