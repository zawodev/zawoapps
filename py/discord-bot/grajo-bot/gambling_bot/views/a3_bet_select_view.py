import discord
from gambling_bot.models.table.table import Table
from gambling_bot.views import a4_table_view
from discord.ui import Button
from gambling_bot.casino import casino


async def display(interaction: discord.Interaction, table: Table):
    name = table.table_data.data['name']
    description = table.table_data.__str__()
    embed = discord.Embed(title=name, description=description, color=0xffaff0)
    view = BetSelectView(table)
    await interaction.response.send_message(embed=embed, view=view)


def _create_button_callback(table: Table, bet: int):
    async def button_callback(interaction: discord.Interaction):
        player_profile = casino.get_player_profile_with_id(str(interaction.user.id))
        table.add_bet_player(player_profile, bet)
        await a4_table_view.display(interaction, table)
    return button_callback

class BetSelectView(discord.ui.View):
    def __init__(self, table: Table):
        super().__init__()
        self.table = table
        for bet in table.table_data['bets']:
            bet_name = f"bet {bet}"
            bet_unq_id = f"{table.table_data.path[-1]}_{table.table_data.path[-2]}_{bet}"
            button = Button(
                label=bet_name,
                style=discord.ButtonStyle.blurple, custom_id=bet_unq_id
            )
            button.callback = _create_button_callback(table, int(bet))
            self.add_item(button)

    @discord.ui.button(label="ready", style=discord.ButtonStyle.green, custom_id="ready")
    async def ready(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.ready(interaction.user.id)
        await a4_table_view.display(interaction, self.table)
