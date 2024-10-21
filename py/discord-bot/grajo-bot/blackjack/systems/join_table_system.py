import discord
from blackjack.blackjackgame.blackjackgame import BlackJackGame
from blackjack.table.player import Player

async def join_table(interaction: discord.Interaction, player: Player):
    await interaction.response.send_message(f"Zasiadłeś przy stole {player.table.channel.name}", ephemeral=True)

async def leave_table(interaction: discord.Interaction, player: Player):
    player.table.remove_player(player.profile.profile_id)
    await interaction.response.send_message(f"Opuszczasz stół {player.table.channel.name}", ephemeral=True)
