import discord
import json
import asyncio
import os
from datetime import datetime,timedelta

token = os.getenv("DISCORD_TOKEN")

bot = discord.Client()
rozklad = {}
with open("data.json",'r') as jsonfile:
    titles = json.loads(jsonfile.read())

async def zrob_rozklad(ctx):
    global rozklad
    time = datetime.now()
    for t in titles:
        if not t["title"] == "perfect sunday":
            track_time = t["duration"].split(":")
            time += timedelta(minutes=int(track_time[0]),seconds=int(track_time[1]))
        rozklad[t["title"]] = {"duration":t["duration"],"time_starts":time}
    await ctx.channel.send("Rozkład zrobiony!")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Rozklad jazdy"))
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(ctx):
    messageContent = ctx.content
    if messageContent.startswith("mplay https://open.spotify.com/playlist/37i9dQZF1DXdwTUxmGKrdN?si=RNCbTCqmSc6Xtizt4HihNA"):
    #if messageContent.startswith("g"):
        await zrob_rozklad(ctx)
    elif messageContent.startswith("rozklad"):
        messageContent = messageContent.lower()
        messageContent = messageContent.replace("rozklad ","")
        if rozklad == {}: 
            await ctx.channel.send("Najpierw musisz odpalić playliste debilu")
            return
        try:
            selected_track = rozklad[messageContent]
        except: 
            await ctx.channel.send("nie ma takiego utworu lol")
        else:
            await ctx.channel.send(f"Utwór: {messageContent},\nCzas trwania: {selected_track['duration']}\nGodzina rozpoczęcia: {selected_track['time_starts'].strftime('%H:%M')}")
        


bot.run(token)