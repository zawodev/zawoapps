import discord

from datetime import datetime

from blackjack.game.blackjack_game import BlackJackGame
from blackjack.game.game_checks import get_table_or_notify, get_or_create_player

async def place_bet(interaction: discord.Interaction, bjg: BlackJackGame, amount: int):
    table = await get_table_or_notify(interaction, bjg)

    if table is None:
        return

    player = await get_or_create_player(bjg, interaction.user.id)

    if player.has_chips(amount):
        player.place_bet(amount)
        await interaction.response.send_message(f"Postawiłeś {amount}$", ephemeral=True)
    else:
        await interaction.response.send_message(
            f"Nie masz tyle żetonów, twój stan konta to {player.stats.chips}$",
            ephemeral=True
        )






async def bet(interaction: discord.Interaction, bjg: BlackJackGame, amount: int):
    player = await get_or_create_player(bjg, interaction.user.id)
    table = await get_table_or_notify(interaction, bjg)
    if table is None:
        return

    table.add_player(player)
    table.bet(player, amount)

async def free_bet(interaction: discord.Interaction, bjg: BlackJackGame):
    player = await get_or_create_player(bjg, interaction.user.id)
    table = await get_table_or_notify(interaction, bjg)
    if table is None:
        return

    table.add_player(player)

    today = datetime.now().strftime('%Y-%m-%d')
    if today in player.stats.freebet_dates:
        await interaction.response.send_message("Już odebrałeś swoj darmowy zakład dzisiaj", ephemeral=True)
        return

    player.stats.freebet_dates.append(today)
    table.dealer.transfer_chips(player, 50)
    table.bet(player, 50)

