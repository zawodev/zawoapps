import discord
from discord import Embed


async def count_react_emojis(guild):
    """
    Count the total number of emojis given by each member of guild.

    Returns a dict of members and their emoji count
    """
    emoji_counts = {}

    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            print(channel.name)
            msgs = 0
            async for message in channel.history(limit=None):
                msgs += 1
                if msgs % 100 == 0:
                    print(msgs)
                for reaction in message.reactions:
                    async for user in reaction.users():
                        if isinstance(user, discord.Member):
                            emoji_counts[user] = emoji_counts.get(user, 0) + 1
    print("udalo sie!!!")
    return emoji_counts


async def emoji_count_to_embed(guild):
    """
    Returns the emoji counts in a human-readable format as an embedded message
    """
    emoji_counts = await count_react_emojis(guild)

    embed = Embed(title="Emoji Counts", description="Number of emojis reacted by each member")

    for member, count in emoji_counts.items():
        embed.add_field(name=member.display_name, value=str(count), inline=False)

    return embed

