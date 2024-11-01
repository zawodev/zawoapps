import discord

from gambling_bot.models.player import Player
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.models.table.table import Table
from gambling_bot.table_type import TableType
from gambling_bot.views.table_view.blackjack_table_view import BlackjackTableView


def create_player(profile: Profile, table: Table):
    player_id = profile.profile_data.path[-1]
    if player_id not in table.players:
        table.players.append(Player(profile))


async def display(interaction: discord.Interaction, table: Table, bet: int):

    table.add_player(interaction, bet)

    view: TableView

    table_type = table.table_data.path[-2]
    if table_type == TableType.BLACKJACK:
        view = BlackjackTableView(table)
    elif table_type == TableType.TEXAS_HOLDEM:
        view = TexasHoldemTableView(table)
    elif table_type == TableType.SPIN_AND_PLAY:
        view = SpinAndPlayTableView(table)
    else:
        raise ValueError(f"Unknown table type: {table_type}")

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
