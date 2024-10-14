import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from blackjack import setup_blackjack_commands

# ======================== DISCORD BOT ========================

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# ======================== DISCORD BOT EVENTS ========================

@bot.event
async def on_ready():

    # ustaw status bota jako niewidoczny
    await bot.change_presence(status=discord.Status.invisible)

    print(f'bot zalogowany jako {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands.')
    except Exception as e:
        print(e)

    # await channel.send("bot is online")

# ======================== MAREK ========================

# setup_marek_commands(bot)

# ======================== BLACKJACK ========================

setup_blackjack_commands(bot)

# ======================== RUN DISCORD BOT ========================

bot.run(token)
