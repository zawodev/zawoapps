import discord
from blackjack.game.blackjack_game import BlackJackGame
from blackjack.table.player import Player

async def get_or_create_player(bjg: BlackJackGame, user_id: int) -> Player:
    # Get existing player or create new
    player = bjg.get_player(user_id)
    if player is None:
        player = Player(user_id)
        bjg.add_player(player)
    return player

async def get_table_or_notify(interaction: discord.Interaction, bjg: BlackJackGame):
    # Get the table or notify the user if not in a valid channel
    table = bjg.get_table(interaction.channel_id)
    if table is None:
        await interaction.response.send_message(
            f"Nie możesz grać w blackjacka poza kasynem mordo, zapraszamy na <#{bjg.casino_channel_id}>",
            ephemeral=True
        )
    return table

async def join_table(interaction: discord.Interaction, bjg: BlackJackGame):
    player = await get_or_create_player(bjg, interaction.user.id)
    table = await get_table_or_notify(interaction, bjg)
    if table is None:
        return

    table.add_player(player)
    await interaction.response.send_message(f"Zasiadłeś przy stole {table.channel.name}", ephemeral=True)

async def leave_table(interaction: discord.Interaction, bjg: BlackJackGame):
    player = await get_or_create_player(bjg, interaction.user.id)
    table = await get_table_or_notify(interaction, bjg)
    if table is None:
        return

    table.remove_player(player)
    await interaction.response.send_message(f"Opuszczasz stół {table.channel.name}", ephemeral=True)
