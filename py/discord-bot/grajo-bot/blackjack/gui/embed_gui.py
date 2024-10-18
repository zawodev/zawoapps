import discord
from blackjack.game.blackjack_game import BlackJackGame
from blackjack.table.player import Player
from blackjack.table.profile import Profile
from blackjack.table.table import Table


def draw_table(table: Table, color: discord.Color):
    embed = discord.Embed(
        title="BlackJack",
        description="Gra w blackjacka",
        color=color
    )

    embed.add_field(name=table.dealer, value=table.dealer.hand)
    for player in table.players:
        embed.add_field(
            name=player,
            value="\n".join([hand for hand in player.hands]),
            inline=False
        )

    return embed


def draw_stats(profile: Profile, color: discord.Color):
    embed = discord.Embed(
        title="Statystyki",
        description="Statystyki gracza",
        color=color
    )

    embed.add_field(name=profile.stats.name, value=profile.stats, inline=False)

    return embed


def draw_ranking(profiles, color: discord.Color):
    embed = discord.Embed(
        title="Ranking",
        description="Ranking graczy",
        color=color
    )

    for profile in profiles:
        embed.add_field(name=profile.stats.name, value=profile.stats, inline=False)

    return embed
