from cProfile import label

import discord
from discord.ext import commands
from discord.ui import Button, View

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN_NAPIERDALER')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class TableView(discord.ui.View):
    def __init__(self, bet_a, bet_b, bet_c):
        super().__init__()
        # prywatna zmienna dla danej instancji embeda
        self.current_value = 0
        self.bet_a = bet_a
        self.bet_b = bet_b
        self.bet_c = bet_c
        self.bet_a_button.label = f"bet {bet_a}"
        self.bet_b_button.label = f"bet {bet_b}"
        self.bet_c_button.label = f"bet {bet_c}"

    async def update_embed(self, interaction: discord.Interaction):
        # odświeża embed i edytuje wiadomość
        embed = discord.Embed(title="Table (playing)", description=f"Aktualna wartość: {self.current_value}", color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="bet_a", style=discord.ButtonStyle.secondary, custom_id="bet_a")
    async def bet_a_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value += self.bet_a
        await self.update_embed(interaction)

    @discord.ui.button(label="bet_b", style=discord.ButtonStyle.red, custom_id="bet_b")
    async def bet_b_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value += self.bet_b
        await self.update_embed(interaction)

    @discord.ui.button(label="bet_c", style=discord.ButtonStyle.gray, custom_id="bet_c")
    async def bet_c_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value += self.bet_c
        await self.update_embed(interaction)

    @discord.ui.button(label="hit", style=discord.ButtonStyle.green, custom_id="hit")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value += 3
        await self.update_embed(interaction)

    @discord.ui.button(label="stand", style=discord.ButtonStyle.red, custom_id="stand")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value -= 2
        await self.update_embed(interaction)

    @discord.ui.button(label="double", style=discord.ButtonStyle.blurple, custom_id="double")
    async def double(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value *= 2
        await self.update_embed(interaction)

    @discord.ui.button(label="split", style=discord.ButtonStyle.gray, custom_id="split")
    async def split(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value //= 2  # dzielenie całkowite
        await self.update_embed(interaction)

    @discord.ui.button(label="forfeit", style=discord.ButtonStyle.danger, custom_id="forfeit")
    async def forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_value = 0
        await self.update_embed(interaction)


class BlackjackTableView(TableView):
    def __init__(self, bet_a, bet_b, bet_c):
        super().__init__(bet_a, bet_b, bet_c)
        # inne przyciski


@bot.command(name="play")
async def play(ctx): #blackjack/texas/spinandplay, bet_a, bet_b, bet_c (domyslnie 10, 100, 1000)
    # interaction.channel -> create thread -> create embed (zablokuj thread, zeby nie dało sie pisac, daj mu tytuł itd)
    embed = discord.Embed(title="Table", description="place your bets now!", color=0x00ff00)
    view = TableView(10, 100, 1000)
    await ctx.send(embed=embed, view=view)

bot.run(token)
