import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

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
    await bot.process_commands(message)
    await message.channel.send("Hello, world!")


@bot.tree.command(name="hello")
async def hello(ctx: discord.Interaction):
    await ctx.response.send_message("Hello, world!")


@bot.tree.command(name="hello2")
@app_commands.describe(thing_to_say="sdfsdaf")
async def hello2(ctx: discord.Interaction, thing_to_say: str):
    await ctx.response.send_message(f"you said: {thing_to_say}")

bot.run(os.getenv("DISCORD_TOKEN"))
