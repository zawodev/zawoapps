import discord

from datetime import datetime
from blackjack.game.blackjack_game import BlackJackGame
from blackjack.old_blackjack import players
from blackjack.table.player import Player


async def bet(interaction: discord.Interaction, player: Player, amount: int):
    player.table.bet(player, amount)
    await interaction.response.send_message(f"Postawiłeś {amount}$", ephemeral=True)


async def free_bet(interaction: discord.Interaction, player: Player):
    today = datetime.now().strftime('%Y-%m-%d')
    player.profile.stats.freebet_dates.append(today)

    amount = 50
    player.table.dealer.profile.transfer_chips(player.profile, amount)
    await bet(interaction, player, amount)
