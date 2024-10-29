import discord
import game_select_view

async def display_blackjack(interaction: discord.Interaction):
    embed = discord.Embed(title="Casino Bot", description="wersja: 0.1 alpha", color=0x00ff00)
    view = GameSelectView()
    await interaction.response.send_message(embed=embed, view=view)

async def display_texas_holdem(interaction: discord.Interaction):
    pass

async def display_spin_and_play(interaction: discord.Interaction):
    pass

class BetSelectView(discord.ui.View):
    def __init__(self, bet_a, bet_b, bet_c):
        super().__init__()
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
