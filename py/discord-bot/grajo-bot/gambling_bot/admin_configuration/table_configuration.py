import discord
from gambling_bot.casino import casino
from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.models.table.texas_holdem_table import TexasHoldemTable
from gambling_bot.models.table.spin_and_play_table import SpinAndPlayTable


async def add_table(interaction: discord.Interaction, table_type: str, table_name: str):
    if table_type == "blackjack":
        blackjack_table = BlackJackTable({'name': table_name}, 'tables', 'blackjack', table_name)
        blackjack_table.table_data.save()
        casino.blackjack_tables.append(blackjack_table)
    elif table_type == "texas_holdem":
        texas_holdem_table = TexasHoldemTable({'name': table_name}, 'tables', 'texas_holdem', table_name)
        texas_holdem_table.table_data.save()
        casino.texas_holdem_tables.append(texas_holdem_table)
    elif table_type == "spin_and_play":
        spin_and_play_table = SpinAndPlayTable({'name': table_name}, 'tables', 'spin_and_play', table_name)
        spin_and_play_table.table_data.save()
        casino.spin_and_play_tables.append(spin_and_play_table)
    else:
        await interaction.response.send_message(f"table type not found", ephemeral=True)
        return
    await interaction.response.send_message(f"added table", ephemeral=True)

#popraw to ponizej bo nie dziala chyba!!!
async def remove_table(interaction: discord.Interaction, table_type: str, table_name: str):
    if table_type == "blackjack":
        for table in casino.blackjack_tables:
            if table.table_data.data['name'] == table_name:
                casino.blackjack_tables.remove(table)
                table.table_data.delete()
                break
    elif table_type == "texas_holdem":
        for table in casino.texas_holdem_tables:
            if table.table_data.data['name'] == table_name:
                casino.texas_holdem_tables.remove(table)
                table.table_data.delete()
                break
    elif table_type == "spin_and_play":
        for table in casino.spin_and_play_tables:
            if table.table_data.data['name'] == table_name:
                casino.spin_and_play_tables.remove(table)
                table.table_data.delete()
                break
    else:
        await interaction.response.send_message(f"table type not found", ephemeral=True)
        return
    await interaction.response.send_message("removed table", ephemeral=True)
