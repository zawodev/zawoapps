import discord

async def add_table(interaction: discord.Interaction, table_type: str, table_name: str):
    await interaction.response.send_message(f"added table", ephemeral=True)

async def remove_table(interaction: discord.Interaction, table_type: str, table_name: str):
    await interaction.response.send_message("removed table", ephemeral=True)
