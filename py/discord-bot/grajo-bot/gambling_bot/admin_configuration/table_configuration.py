import discord

from gambling_bot.models.table.table_type import TableType
from gambling_bot.casino import casino
from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.models.table.poker_table import PokerTable


async def add_table(interaction: discord.Interaction, table_type: TableType, table_name: str, bets: list):
    # można się pozbyć tego ifa jeśli zrównasz klasy oraz dasz type jako argument zamiast ręcznie
    if table_type.value[0] == TableType.BLACKJACK.value[0]:
        blackjack_table = BlackJackTable(casino.get_random_dealer(), {'bets': bets}, 'tables', 'blackjack', table_name)
        casino.blackjack_tables.append(blackjack_table)
    elif table_type.value[0] == TableType.POKER.value[0]:
        poker_table = PokerTable(casino.get_random_dealer(), {'bets': bets}, 'tables', 'poker', table_name)
        casino.spin_and_play_tables.append(poker_table)
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
    elif table_type == "poker":
        for table in casino.poker_tables:
            if table.table_data.path[-1] == table_name:
                table.table_data.delete()
                casino.poker_tables.remove(table)
                break
    else:
        await interaction.response.send_message(f"table type not found", ephemeral=True)
        return
    await interaction.response.send_message("removed table", ephemeral=True)
