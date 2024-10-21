import discord
from blackjack.blackjackgame.blackjackgame import BlackJackGame
from blackjack.old_blackjack import players
from blackjack.table.player import Player
from blackjack.table.table import Table


async def hit(interaction: discord.Interaction, player: Player):
    player.table.hit(player)
    await interaction.response.send_message("Dobierasz kartę", ephemeral=True)


async def stand(interaction: discord.Interaction, player: Player):
    player.table.stand(player)
    await interaction.response.send_message("Kończysz swoją turę", ephemeral=True)


async def double(interaction: discord.Interaction, player: Player):
    player.table.double(player)
    await interaction.response.send_message("Kończysz swoją turę", ephemeral=True)


async def split(interaction: discord.Interaction, player: Player):
    player.table.split(player)
    await interaction.response.send_message("Kończysz swoją turę", ephemeral=True)


async def forfeit(interaction: discord.Interaction, player: Player):
    player.table.forfeit(player)
    await interaction.response.send_message("Kończysz swoją turę", ephemeral=True)
