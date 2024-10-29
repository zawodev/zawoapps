import discord

from gambling_bot.views import game_select_view
from gambling_bot.casino import casino
from gambling_bot.admin_configuration import table_configuration

# both commands: bet
# blackjack commands: hit, stand, double, split, forfeit
# poker commands: check, call, raise, fold

async def setup(bot):
    # casino setup
    casino.setup(bot)

    @bot.tree.command(name="play", description="rozpocznij grę w kasynie")
    async def play(interaction: discord.Interaction):
        await game_select_view.display(interaction)

    # ------- ADMIN COMMANDS -------

    # add table command
    @bot.tree.command(name="add_table", description="dodaj stół do kasyna")
    async def add_table(interaction: discord.Interaction, table_type: str, table_name: str):
        await table_configuration.add_table(interaction, table_type, table_name)

    # remove table command
    @bot.tree.command(name="remove_table", description="usuń stół z kasyna")
    async def remove_table(interaction: discord.Interaction, table_type: str, table_name: str):
        await table_configuration.remove_table(interaction, table_type, table_name)
