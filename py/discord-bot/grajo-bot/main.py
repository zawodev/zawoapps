import discord
import random
import asyncio
from discord.ext import commands
import pytz
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from blackjack import setup_blackjack_commands
from marek import setup_marek_commands

# ======================== DISCORD BOT ========================

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# ======================== MAREK ========================

setup_marek_commands(bot)

# ======================== BLACKJACK ========================

setup_blackjack_commands(bot)

# ======================== RUN DISCORD BOT ========================

bot.run(token)
