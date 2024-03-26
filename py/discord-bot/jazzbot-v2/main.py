import discord
from discord.ext import commands
#from discord_slash import SlashCommand, SlashContext
#from discord_slash.utils.manage_commands import create_choice, create_option
import interactions
from discord import app_commands
import os, asyncio, pytz, random
from datetime import datetime
from dotenv import load_dotenv
from zawolib import msgcount, progressbar

load_dotenv()
clear = lambda: os.system('cls')
token = os.getenv("DISCORD_TOKEN")
tz = pytz.timezone("Europe/Warsaw")
intents = discord.Intents(messages=True, guilds=True, members=True)
#bot = commands.Bot(command_prefix='/', intents=intents)
bot = interactions.Client(token=token)

#slash = SlashCommand(bot, sync_commands=True)

#===============================================================

async def send(channel, msg):
    global isMuted
    if isMuted: await channel.send(":no_mouth:")
    else: await channel.send(msg)

def isowner(id):
    return id == 336921078138011650 #zawodev

def setguild(id):
    global guild
    guild = bot.get_guild(id)

async def timer():
    global isLoaded
    while not bot.is_closed():
        await asyncio.sleep(60)

#bot.loop.create_task(timer())

#===============================================================

isLoaded = False
isMuted = False
guild = None

#===============================================================

#1 sub_command, 2 sub_command_group, 3 string, 4 integer, 5 boolean, 6 user, 7 channel, 8 role
#@slash.slash(name="Count", description="sratatata", guild = discord.Object(id=deafult_guild_id), guild_ids=[guild1, guild2], required=True, options=[create_option(name='C', description='D', required=True, option_type=3, choices=[create_choice(name='E', value='F'), create_choice(name='G', value='H')])])
#@slash.slash(name="servermsgcount", description="liczenie wiadomosci serwerowych i sortowanie w kolejnosci malejacej", guild_ids=None, options=[create_option(name="guildid", description="ID serwera do pobrania wiadomosci", required=False, option_type=3), create_option(name="admininterval", description="ile okresow pomiarowych ma posiadac pomiar", required=False, option_type=4), create_option(name='startdate', description='Data i godzina w formacie "DD/MM/YY HH:MM:SS" startu', required=False, option_type=3)])
#async def _servermsgcount(ctx:SlashContext, guildid:str = None, admininterval:int = None, startdate:str = "now"):
#    if isowner(ctx.author.id):
#        msg = await ctx.send("liczenie wiadomości za chwilę się rozpocznie...")
#        await msgcount.downloadServerMessagesCount(bot, ctx, msg, adminOutput=True, guildid=guildid, adminNumsInterval=admininterval, adminBeforeTime=startdate)
#    else:
#        await ctx.send("`no permission to use that command bro`:face_with_raised_eyebrow:")
#
#@slash.slash(name="usermsgcount", description="liczenie wiadomosci poszczegolnych uzytkownikow na przestrzeni czasu")
#async def _usermsgcount(ctx: SlashContext):
#    if isowner(ctx.author.id):
#       await ctx.send("liczenie wiadomości za chwilę się rozpocznie...")
#        await msgcount.downloadUserMessagesCount()
#    else:
#        await ctx.send("`no permission to use that command bro`:face_with_raised_eyebrow:")

@bot.command(name="servermsgcount", description="liczenie wiadomosci serwerowych i sortowanie w kolejnosci malejacej") #scope=idserwra
async def servermsgcount(ctx:interactions.CommandContext, guildid:str = None, admininterval:int = None, startdate:str = "now"):
    if isowner(ctx.author.id):
        msg = await ctx.send("liczenie wiadomości za chwilę się rozpocznie...")
        await msgcount.downloadServerMessagesCount(bot, ctx, msg, adminOutput=True, guildid=guildid, adminNumsInterval=admininterval, adminBeforeTime=startdate)
    else:
        await ctx.send("`no permission to use that command bro`:face_with_raised_eyebrow:")

@bot.command(name="usermsgcount", description="liczenie wiadomosci poszczegolnych uzytkownikow na przestrzeni czasu")
async def usermsgcount(ctx:interactions.CommandContext):
    if isowner(ctx.author.id):
        await ctx.send("liczenie wiadomości za chwilę się rozpocznie...")
        await msgcount.downloadUserMessagesCount()
    else:
        await ctx.send("`no permission to use that command bro`:face_with_raised_eyebrow:")

#dodaj date nad tabem

@bot.event
async def on_ready():
    global isLoaded
    isLoaded = True

@bot.event
async def on_message(ctx):
    global owner
    msg = ctx.content
    if msg.startswith("czesc bocie"): 
        #await send(ctx.channel, "siema zawo")
        ctx = ctx.channel
        msg = await ctx.send("liczenie wiadomości za chwilę się rozpocznie...")
        await msgcount.downloadServerMessagesCount(bot, ctx, msg, adminOutput=True, guildid=(GUILD_ID_HERE), adminNumsInterval=150000, adminBeforeTime="now")


#bot.run(token)
bot.start()