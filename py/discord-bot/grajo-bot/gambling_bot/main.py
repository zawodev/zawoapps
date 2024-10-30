import discord

from gambling_bot.models.profile.profile import Profile
from gambling_bot.table_type import TableType
from gambling_bot.views import game_select_view
from gambling_bot.casino import casino
from gambling_bot.admin_configuration import table_configuration

# both commands: bet
# blackjack commands: hit, stand, double, split, forfeit
# poker commands: check, call, raise, fold


def create_profile(interaction: discord.Interaction):
    profile_id = str(interaction.user.id)
    profile_name = interaction.user.name
    if profile_id not in casino.player_profiles:
        player_profile = Profile({'name': profile_name}, 'profiles', 'players', profile_id)
        casino.player_profiles.append(player_profile)


async def setup(bot):
    # casino setup
    casino.setup(bot)

    @bot.tree.command(name="gamble", description="rozpocznij grę w kasynie")
    async def gamble(interaction: discord.Interaction):
        create_profile(interaction)
        await game_select_view.display(interaction)

    # ------- ADMIN COMMANDS -------

    # add table command
    @bot.tree.command(name="add_table", description="dodaj stół do kasyna")
    async def add_table(interaction: discord.Interaction, table_type: TableType, table_name: str, bets: str = "1 10 100"):
        bets_list = bets.split(" ")
        await table_configuration.add_table(interaction, table_type, table_name, bets_list)

    # remove table command
    @bot.tree.command(name="remove_table", description="usuń stół z kasyna")
    async def remove_table(interaction: discord.Interaction, table_type: str, table_name: str):
        await table_configuration.remove_table(interaction, table_type, table_name)
