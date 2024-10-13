import discord
import random
import asyncio
from discord.ext import commands
from datetime import datetime
import pytz

admin_ids = [336921078138011650] # zawodev
WORDS_FILE = 'word_list.txt'
tz = pytz.timezone("Europe/Warsaw")
bot = None

# ======================== WORD LIST ========================

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

async def timer():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await update()
        await asyncio.sleep(60)

async def update():
    time = datetime.now(tz)
    print(time.strftime('%H:%M'))

async def setup_hook():
    bot.loop.create_task(timer())

# ======================== DISCORD BOT EVENTS ========================

async def on_voice_state_update(member, before, after):

    voice_client = None

    # na razie wyłączamy funkcje dołączania na voice call
    # return

    if member.bot: # jeśli bot dołączył na kanał głosowy, to nic nie rób
        return

    # sprawdzamy czy użytkownik dołączył na kanał głosowy
    if before.channel is None and after.channel is not None:
        # member dołączył na kanał głosowy
        print(f'{member} dołączył na kanał {after.channel}')

        # sprawdzamy, czy bot jest już na kanale, żeby nie połączyć go ponownie
        if voice_client is None or not voice_client.is_connected():
            # odczekaj 1-3 sekundy
            await asyncio.sleep(random.uniform(1, 3))
            # bot nie jest na kanale, łączymy go
            voice_client = await after.channel.connect()

    # sprawdzamy czy użytkownik opuścił kanał głosowy
    if before.channel is not None and after.channel is None:
        # member opuścił kanał głosowy
        print(f'{member} opuścił kanał {before.channel}')

        # sprawdzamy, czy kanał głosowy jest teraz pusty, ignorując bota
        non_bot_members = [m for m in before.channel.members if not m.bot]

        # sprawdzamy, czy kanał głosowy jest teraz pusty
        if len(non_bot_members) == 0 and voice_client is not None:
            # kanał głosowy stał się pusty, rozłączamy bota
            print(f'kanał {before.channel.name} jest teraz pusty')

            # odczekaj 1-3 sekundy
            await asyncio.sleep(random.uniform(1, 3))

            await voice_client.disconnect()
            voice_client = None

            # bot opuścił kanał głosowy
            print("bot opuścił kanał głosowy")


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

async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    # get user from id 380820820466991116 (grajo)
    real_grajo = await bot.fetch_user(380820820466991116)

    if 'graj' in msg or 'marek' in msg or 'bot' in msg or bot.user.mentioned_in(message) or real_grajo.mentioned_in(message):
        action = random.randint(1, 7)
        print(action)

        async with message.channel.typing():
            await asyncio.sleep(random.uniform(1, 5))

        random_words = random.sample(word_list, random.randint(1, 5))
        last_messages = [msg async for msg in message.channel.history(limit=100)]
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

    # if message owner is grajo then add his message to the list
    if message.author.id == 1291727291881226280:
        word_list.append(message.content)
        save_words(word_list)
        await message.channel.send(f'słowo "{message.content}" zostało dodane do listy moich słów!')


    await bot.process_commands(message)



# ======================== DISCORD BOT COMMANDS ========================

async def add_word(interaction: discord.Interaction, word: str):
    word_list.append(word)
    save_words(word_list)
    await interaction.response.send_message(f'słowo "{word}" zostało dodane do listy moich słów!')


async def say_something(interaction: discord.Interaction, message: str, channel_id: int = 1250873886426402937):
    if interaction.user.id not in admin_ids:
        await interaction.response.send_message(f'nie masz uprawnień do użycia tej komendy')
        return

    channel = bot.get_channel(int(channel_id))
    await channel.send(message)
    await interaction.response.send_message(f'wysłano wiadomość', ephemeral=True)


async def play_sound(interaction: discord.Interaction, channel_id: int = 1028303332193873981, sound_id: int = -1):
    global voice_client

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

    # Dołączanie do kanału głosowego jeśli jeszcze tam nie dołączyliśmy
    if voice_client is None or not voice_client.is_connected():
        voice_client = await voice_channel.connect()
        print("bot dołączył do kanału głosowego")

    # Sprawdzamy, czy bot jest już podłączony i czy nie gra dźwięku
    if voice_client.is_playing():
        # await interaction.response.send_message("bot już odtwarza dźwięk!", ephemeral=True)
        print("bot już odtwarza dźwięk!")
        return

    # Odtwarzanie dźwięku MP3
    if sound_id == -1:
        sound_id = random.randint(1, 3)
    sound = 'grajo' + str(sound_id) + '.mp3'

    audio_source = discord.FFmpegPCMAudio(sound)
    voice_client.play(audio_source)

    # Poczekaj, aż dźwięk się skończy
    # while voice_client.is_playing():
    #    await asyncio.sleep(1)

    print("dźwięk został odtworzony")

    # Opuść kanał głosowy po zakończeniu odtwarzania

    # await voice_client.disconnect()
    # print("bot opuścił kanał głosowy")

def setup_marek_commands(new_bot):

    global bot
    bot = new_bot

    # ------------------------ COMMANDS ------------------------

    bot.tree.command(name="add_word", description="dodaj swoje ulubione słowo graja")(add_word)
    bot.tree.command(name="say_something", description="powiedz coś na kanale tekstowym")(say_something)
    bot.tree.command(name="play_sound", description="odtwarzaj dźwięk na kanale głosowym")(play_sound)

    # ------------------------ EVENTS ------------------------

    bot.add_listener(on_voice_state_update, name="on_voice_state_update")
    bot.add_listener(on_ready, name="on_ready")
    bot.add_listener(on_message, name="on_message")

    # ------------------------ TIMER ------------------------

    bot.add_listener(setup_hook, name="setup_hook")
