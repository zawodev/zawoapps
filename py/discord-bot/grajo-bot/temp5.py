import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
token = os.getenv('DISCORD_TOKEN_MAREKROMPER')

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}.')

@bot.command()
async def pokaz_embed(ctx):
    # 1. podstawowy embed
    embed1 = discord.Embed(title="Podstawowy Embed", description="Opis w podstawowym embedzie.")

    # 2. kolorowy embed
    embed2 = discord.Embed(title="Kolorowy Embed", description="Embed z niestandardowym kolorem.", color=discord.Color.blue())

    # 3. embed z thumbnail
    embed3 = discord.Embed(title="Embed z Thumbnail", description="Miniaturka po prawej.")
    embed3.set_thumbnail(url="https://gratisography.com/wp-content/uploads/2024/01/gratisography-cyber-kitty-800x525.jpg")

    # 4. embed z obrazkiem
    embed4 = discord.Embed(title="Embed z Obrazkiem", description="Główny obrazek poniżej.")
    embed4.set_thumbnail(url="https://gratisography.com/wp-content/uploads/2024/01/gratisography-cyber-kitty-800x525.jpg")

    # 5. embed z autorem
    embed5 = discord.Embed(title="Embed z Autorem", description="Autor wyświetlony powyżej.")
    embed5.set_author(name="Autor Embed")

    # 6. embed z polami
    embed6 = discord.Embed(title="Embed z Polami", description="Różne pola w embedzie.")
    embed6.add_field(name="Pole 1", value="Wartość pola 1", inline=True)
    embed6.add_field(name="Pole 2", value="Wartość pola 2", inline=True)
    embed6.add_field(name="Pole 3", value="Wartość pola 3", inline=False)

    # 7. embed z timestampem
    embed7 = discord.Embed(title="Embed z Timestampem", description="Znacznik czasu poniżej.")
    embed7.timestamp = ctx.message.created_at

    # 8. embed z footerm
    embed8 = discord.Embed(title="Embed z Footerm", description="Stopka poniżej.")
    embed8.set_footer(text="Przykładowa stopka")

    # 9. embed z linkiem w tytule
    embed9 = discord.Embed(title="[Tytuł z Linkiem](https://example.com)", description="Klikalny tytuł.")

    # 10. dynamiczny kolor
    embed10 = discord.Embed(title="Dynamiczny Kolor", description="Kolor zależny od wartości pola.")
    value = 10  # przykładowa wartość
    embed10.color = discord.Color.green() if value > 5 else discord.Color.red()
    embed10.add_field(name="Wartość", value=value)

    # wysyłanie embedów
    embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9, embed10]
    for embed in embeds:
        await ctx.send(embeds=embeds)

# uruchomienie bota
bot.run(token)
