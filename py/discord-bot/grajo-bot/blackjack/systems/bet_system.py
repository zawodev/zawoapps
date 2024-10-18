import discord

from datetime import datetime
from blackjack.game.blackjack_game import BlackJackGame
from blackjack.old_blackjack import players
from blackjack.table.player import Player


async def bet(interaction: discord.Interaction, player: Player, amount: int):
    if player.bet_used:
        await interaction.response.send_message("Już postawiłeś zakład", ephemeral=True)
        return

    if player.table.game_active:
        await interaction.response.send_message("Gra już trwa!", ephemeral=True)
        return

    if amount < player.table.min_bet:
        await interaction.response.send_message(f"Minimalny zakład to {player.table.min_bet}$", ephemeral=True)
        return

    if amount > player.table.max_bet:
        await interaction.response.send_message(f"Maxymalny zakład to {player.table.max_bet}$", ephemeral=True)
        return

    if not player.profile.has_chips(amount):
        await interaction.response.send_message("Nie masz tyle żetonów", ephemeral=True)
        return

    player.table.bet(player, amount)

    await interaction.response.send_message(f"Postawiłeś {amount}$", ephemeral=True)


async def free_bet(interaction: discord.Interaction, player: Player):
    today = datetime.now().strftime('%Y-%m-%d')
    if today in player.profile.stats.freebet_dates:
        await interaction.response.send_message("Już odebrałeś swoj darmowy zakład dzisiaj", ephemeral=True)
        return
    player.profile.stats.freebet_dates.append(today)

    amount = 50
    player.table.dealer.profile.transfer_chips(player.profile, amount)
    await bet(interaction, player, amount)
