import discord

from gambling_bot.models.player import Player
from gambling_bot.models.table.table import Table


def create_player(profile, table):
    player_id = profile.profile_data.path[-1]
    if player_id not in table.players:
        table.players.append(Player(profile, table))


async def display(interaction: discord.Interaction, table: Table, bet: int):
    view = BlackjackTableView()
    embed = discord.Embed(title="gogow", description="opis stolu konkretnego", color=0xffff00)

    for player in table.players:
        embed.add_field(name=player.name, value=f"{player.hand} {player.bet}")

    if table.game_active:
        await interaction.response.edit_message(embed=embed, view=view)
    else:
        await interaction.response.send_message(embed=embed, view=view)
        table.game_active = True


class BlackjackTableView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="hit", style=discord.ButtonStyle.green, custom_id="hit")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="stand", style=discord.ButtonStyle.red, custom_id="stand")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="double", style=discord.ButtonStyle.blurple, custom_id="double")
    async def double(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="split", style=discord.ButtonStyle.gray, custom_id="split")
    async def split(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="forfeit", style=discord.ButtonStyle.danger, custom_id="forfeit")
    async def forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
