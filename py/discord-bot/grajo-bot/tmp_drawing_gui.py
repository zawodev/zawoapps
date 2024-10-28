import discord
from discord.ext import commands
from discord.ui import Button, View

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN_NAPIERDALER')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class CounterEmbed(discord.ui.View):
    def __init__(self):
        super().__init__()
        # prywatna zmienna dla danej instancji embeda
        self.current_value = 0

    async def update_embed(self, interaction: discord.Interaction):
        # odświeża embed i edytuje wiadomość
        embed = discord.Embed(title="Licznik", description=f"Aktualna wartość: {self.current_value}", color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Dodaj 3", style=discord.ButtonStyle.green, custom_id="add_3_unique")
    async def add_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value += 3
        await self.update_embed(interaction)

    @discord.ui.button(label="Odejmij 2", style=discord.ButtonStyle.red, custom_id="subtract_2_unique")
    async def subtract_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value -= 2
        await self.update_embed(interaction)

    @discord.ui.button(label="Pomnóż przez 2", style=discord.ButtonStyle.blurple, custom_id="multiply_2_unique")
    async def multiply_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value *= 2
        await self.update_embed(interaction)

    @discord.ui.button(label="Podziel przez 2", style=discord.ButtonStyle.gray, custom_id="divide_2_unique")
    async def divide_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value //= 2  # dzielenie całkowite
        await self.update_embed(interaction)

    @discord.ui.button(label="Zresetuj", style=discord.ButtonStyle.danger, custom_id="reset_unique")
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value = 0
        await self.update_embed(interaction)

@bot.command(name="licznik")
async def licznik(ctx):
    # tworzy nowy embed i widok przy każdym wywołaniu komendy
    embed = discord.Embed(title="Licznik", description="Aktualna wartość: 0", color=0x00ff00)
    view = CounterEmbed()
    await ctx.send(embed=embed, view=view)

bot.run(token)
