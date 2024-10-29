import discord
from discord.ui import Button
from gambling_bot.casino import casino

# display blackjack tables
async def display_blackjack_tables(interaction: discord.Interaction):
    embed = discord.Embed(title="Blackjack Tables", description="<tu wstaw descrtpipion>", color=0x00ff00)
    tables = casino.blackjack_tables
    view = TableSelectView(tables)
    await interaction.response.send_message(embed=embed, view=view)

async def display_texas_holdem_tables(interaction: discord.Interaction):
    embed = discord.Embed(title="Texas Holdem Tables", description="<tu wstaw descrtpipion>", color=0x00ff00)
    tables = casino.texas_holdem_tables
    view = TableSelectView(tables)
    await interaction.response.send_message(embed=embed, view=view)

async def display_spin_and_play_tables(interaction: discord.Interaction):
    embed = discord.Embed(title="Spin and Play Tables", description="<tu wstaw descrtpipion>", color=0x00ff00)
    tables = casino.spin_and_play_tables
    view = TableSelectView(tables)
    await interaction.response.send_message(embed=embed, view=view)


def create_button_callback(table_number):
    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_message(f"Table {table_number}")
    return button_callback


class TableSelectView(discord.ui.View):
    def __init__(self, tables):
        super().__init__()
        for i, table in enumerate(tables, start=1):
            button = Button(
                label=f"Table {i}",
                style=discord.ButtonStyle.secondary,
                custom_id=f"table_{i}"
            )
            button.callback = create_button_callback(i)
            self.add_item(button)
