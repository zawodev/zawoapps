import discord
import random
import asyncio
from discord.ext import commands
import pytz
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# ======================== DISCORD BOT ========================

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
admin_ids = [336921078138011650] # zawodev

# ======================== WORD LIST ========================

WORDS_FILE = 'word_list.txt'

def load_words():
    try:
        # encoding utf-8 # encoding='utf-8'
        with open(WORDS_FILE, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_words(words):
    # encoding utf-8 # encoding='utf-8'
    with open(WORDS_FILE, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(f'{word}\n')

word_list = load_words()

# ======================== TIMER ========================

tz = pytz.timezone("Europe/Warsaw")

async def timer():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await update()
        await asyncio.sleep(60)

async def update():
    time = datetime.now(tz)
    print(time.strftime('%H:%M'))

# ======================== DISCORD BOT EVENTS ========================

@bot.event
async def setup_hooks():
    await bot.loop.create_task(timer())

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

    #await channel.send("bot is online")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()

    if 'graj' in msg or 'marek' in msg or 'bot' in msg or bot.user.mentioned_in(message):
        action = random.randint(1, 7)
        print(action)

        async with message.channel.typing():
            await asyncio.sleep(random.uniform(1, 5))

        random_words = random.sample(word_list, random.randint(1, 5))
        last_messages = [msg async for msg in message.channel.history(limit=300)]
        random_message = random.choice(last_messages)

        if action == 1: # respond to random message with "." as a text using discord respond feature
            await random_message.reply(".")

        elif action == 2: # respond to random message with "." as a text using discord respond feature
            await random_message.reply(random_words[0])

        elif action == 3: # react to the last message with 👍
            await last_messages[0].add_reaction("👍")

        elif action == 4: # send random word from the list
            await message.channel.send(random_words[0])

        elif action == 5: # send 1-5 random words from the list
            await message.channel.send(" ".join(random_words))

        # elif action >= 6: # do nothing


    await bot.process_commands(message)

@bot.tree.command(name="add_word", description="dodaj swoje ulubione słowo graja")
async def add_word(interaction: discord.Interaction, word: str):
    word_list.append(word)
    save_words(word_list)
    await interaction.response.send_message(f'słowo "{word}" zostało dodane do listy moich słów!')


@bot.tree.command(name="say", description="say something") # channel_id optional, deafult is general
async def say_something(interaction: discord.Interaction, message: str, channel_id: int = 1250873886426402937):
    if interaction.user.id not in admin_ids:
        await interaction.response.send_message(f'nie masz uprawnień do użycia tej komendy')
        return

    channel = bot.get_channel(int(channel_id))
    await channel.send(message)
    await interaction.response.send_message(f'wysłano wiadomość', ephemeral=True)


@bot.tree.command(name="play_sound", description="dołącza do kanału głosowego i puszcza dźwięk")
async def play_sound(interaction: discord.Interaction, channel_id: int = 1028303332193873981):
    if interaction.user.id not in admin_ids:
        await interaction.response.send_message(f'nie masz uprawnień do użycia tej komendy')
        return

    await interaction.response.send_message("wysłano dźwięk na kanale: " + interaction.channel.name, ephemeral=True)

    guild = interaction.guild  # serwer, na którym jest bot
    voice_channel = guild.get_channel(channel_id)  # kanał głosowy na podstawie id

    if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
        # await interaction.response.send_message("nie znaleziono kanału głosowego o podanym ID.", ephemeral=True)
        print("nie znaleziono kanału głosowego o podanym ID.")
        return

    # Dołączanie do kanału głosowego
    voice_client = await voice_channel.connect()

    # Sprawdzamy, czy bot jest już podłączony i czy nie gra dźwięku
    if voice_client.is_playing():
        # await interaction.response.send_message("bot już odtwarza dźwięk!", ephemeral=True)
        print("bot już odtwarza dźwięk!")
        return

    # Odtwarzanie dźwięku MP3
    audio_source = discord.FFmpegPCMAudio('sound.mp3')
    voice_client.play(audio_source)

    # Poczekaj, aż dźwięk się skończy
    while voice_client.is_playing():
        await asyncio.sleep(1)

    print("dźwięk został odtworzony")

    # Opuść kanał głosowy po zakończeniu odtwarzania

    # await voice_client.disconnect()
    # print("bot opuścił kanał głosowy")




bot.run(token)
