import discord

from gambling_bot.models.player import Player
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.models.table.table import Table


def create_player(profile: Profile, table: Table):
    player_id = profile.profile_data.path[-1]
    if player_id not in table.players:
        table.players.append(Player(profile))


async def display(interaction: discord.Interaction, table: Table, bet: int):

    table.add_player(interaction, bet)

    view = BlackjackTableView(table) # noqa
    embed = view.create_embed()

    if table.game_active:
        await interaction.response.edit_message(embed=embed, view=view)
    else:
        await interaction.response.send_message(embed=embed, view=view)
        table.start_game()


class TableView(discord.ui.View):
    def __init__(self):
        super().__init__()

    def create_embed(self):
        pass

class BlackjackTableView(TableView):
    def __init__(self, table: BlackJackTable):
        super().__init__()
        self.table = table

    def create_embed(self):
        embed = discord.Embed(title="Game View", description="opis", color=0xffff00)

        for player in self.table.players:
            player: Player
            embed.add_field(name=player.profile.profile_data['name'], value=player.get_current_hand(), inline=False)

        return embed

    @discord.ui.button(label="hit", style=discord.ButtonStyle.green, custom_id="hit")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.hit(interaction.user.id)

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
