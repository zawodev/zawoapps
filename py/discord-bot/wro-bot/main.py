import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from zawolib import msgcount, progressbar
from datetime import datetime, timedelta

import random
import pytz
import asyncio

#intents = discord.Intents.default()
intents = discord.Intents(messages=True, guilds=True, members=True)
#intents.members = True
#bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)
slash=SlashCommand(bot, sync_commands=True)
tz = pytz.timezone("Europe/Warsaw")

async def timer():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await update()
        await asyncio.sleep(60)
        
bot.loop.create_task(timer())


async def update():
    #day = time.weekday()
    time = datetime.now(tz)
    guild = bot.get_guild(998715648446308442) #PWR server
    role = guild.get_role(999270889138946111) #IST role
    members_len = len(role.members)
    await guild.get_channel(1003080449809195088).edit(name=f"{progressbar.progress_bar(members_len, 0, 127, length=9)} {members_len}/127")

    print(time.strftime('%H:%M'))
    if time.strftime('%H:%M') == "21:37":
        print(time.strftime('%H:%M'))


#@slash.slash(name="Count", description="sratatata", guild_ids=[870021183737823262, 998715648446308442], required=True, options=[create_option(name='C', description='D', required=True, option_type=3, choices=[create_choice(name='E', value='F'), create_choice(name='G', value='H')])])
@slash.slash(name="msgcount", description="liczenie wiadomosci serwerowych i sortowanie w kolejnosci malejacej", guild_ids=[870021183737823262, 998715648446308442], options=[create_option(name='startdate', description='Data i godzina w formacie "DD/MM/YY HH:MM:SS" startu', required=True, option_type=3)])
async def _msgcount(ctx:SlashContext, startdate:str):
    if (ctx.author.id == 336921078138011650): #zawodev
        await ctx.send("rozpoczynam liczenie wiadomosci...")
        await msgcount.downloadUserMessagesCount(bot, guildid[any], ctx, True, None, startdate)
    else:
        await ctx.send("`do not put semen into your watercooling tubes`\nno permission to use that command bro")

@slash.slash(name="usercount", description="pff", guild_ids=[guild1, guild2(any guild)])
async def _usercount(ctx:SlashContext):
    if (ctx.author.id == 336921078138011650): #zawodev
        await update()
        await ctx.send("updated correcty")
    else:
        await ctx.send("`do not put semen into your watercooling tubes`\nno permission to use that command bro")


@bot.event
async def on_ready():
    print("rdy")
    #msg = await bot.get_channel(998772279259451392).send("loll")
    #await msg.edit(content="lolll", embed=discord.Embed("elo","",discord.Color(value=int(''.join(random.choices('0123456789ABCDEF', k=6)), 16))))

#@bot.event
#async def on_message(ctx):
    


bot.run("TOKEN_HERE")