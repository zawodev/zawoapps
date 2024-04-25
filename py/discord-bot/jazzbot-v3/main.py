import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

import count_react_emojis as cre

load_dotenv()
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # await bot.process_commands(message) # this is not needed
    # await message.channel.send("Hello, world!")


@bot.tree.command(name="count_react_emojis")
async def count_react_emojis(ctx: discord.Interaction):
    await ctx.response.send_message("done")
    embed = await cre.emoji_count_to_embed(ctx.guild)
    await ctx.channel.send(embed=embed)


@bot.tree.command(name="count_react_emojis_args")
@app_commands.describe(guild_id="put description here")
async def count_react_emojis_args(ctx: discord.Interaction, guild_id: str):
    await ctx.response.send_message("done")
    embed = await cre.emoji_count_to_embed(bot.get_guild(int(guild_id)))
    await ctx.channel.send(embed=embed)


bot.run(os.getenv("DISCORD_TOKEN"))

# ideas:

# - message edited and deleted logger

# - message response with character.ai api, group messages into
# conversations (which are group of messages that are 3 min apart max) and respond to them (commands
# /start-responder-webhook, /stop-responder-webhook)

# - message response with gpt-3 api, group messages into
# conversations and respond to them (commands /start-gpt3-webhook, /stop-gpt3-webhook)

# - message auto react bot (gives thumbs up to most grajo's messages
# if there is long time that passed from the last one for example)
