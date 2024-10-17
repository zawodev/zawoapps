import discord
from blackjack.game.blackjack_game import BlackJackGame
from blackjack.table.player import Player

from blackjack.game.game_checks import get_table_or_notify, get_or_create_player

async def join_table(interaction: discord.Interaction, bjg: BlackJackGame):
    player = await get_or_create_player(bjg, interaction.user.id)
    table = await get_table_or_notify(interaction, bjg)
    if table is None:
        return

    table.add_player(player)
    await interaction.response.send_message(f"Zasiadłeś przy stole {table.channel.name}", ephemeral=True)

async def leave_table(interaction: discord.Interaction, bjg: BlackJackGame):
    player = await get_or_create_player(bjg, interaction.user.id)
    table = await get_table_or_notify(interaction, bjg)
    if table is None:
        return

    table.remove_player(player)
    await interaction.response.send_message(f"Opuszczasz stół {table.channel.name}", ephemeral=True)
