import discord
from blackjack.game.blackjack_game import BlackJackGame

import blackjack.systems.join_table_system as jts

def slash_commands_setup(bjg: BlackJackGame):

    @bjg.bot.tree.command(name="join table", description="Dołącz do stołu na danym kanale")
    async def join_table(interaction: discord.Interaction):
        await jts.join_table(interaction, bjg)

    @bjg.bot.tree.command(name="leave table", description="Opuść stół")
    async def leave_table(interaction: discord.Interaction):
        await jts.leave_table(interaction, bjg)

    @bjg.bot.tree.command(name="freebet", description="Jeden dziennie darmowy zakład za 50$")
    async def freebet(interaction: discord.Interaction):
        pass

    @bjg.bot.tree.command(name="bet", description="Zakład na grę")
    async def bet(interaction: discord.Interaction, amount: int):
        pass

    @bjg.bot.tree.command(name="hit", description="Dobierz kartę")
    async def hit(interaction: discord.Interaction):
        pass

    @bjg.bot.tree.command(name="stand", description="Zakończ swoją turę")
    async def stand(interaction: discord.Interaction):
        pass

    @bjg.bot.tree.command(name="double", description="Podwój zakład i dobierz kartę")
    async def double(interaction: discord.Interaction):
        pass

    @bjg.bot.tree.command(name="split", description="Podziel rękę na dwie")
    async def split(interaction: discord.Interaction):
        pass

    @bjg.bot.tree.command(name="tip", description="Podaruj napiwek innemu graczowi")
    async def tip(interaction: discord.Interaction, target_player: discord.Member):
        pass

    @bjg.bot.tree.command(name="thanks for the tip", description="Podziękuj za napiwek albo odbierz napiwek jako zbankrutowany gracz")
    async def thanks_for_the_tip(interaction: discord.Interaction, tipper: discord.Member = None):
        pass

    @bjg.bot.tree.command(name="stats", description="Wyświetl statystyki gracza lub wszystkich graczy")
    async def stats(interaction: discord.Interaction, user: discord.User = None):
        pass

    @bjg.bot.tree.command(name="ranking", description="wyświetl ranking graczy od najbogatszego do najbiedniejszego")
    async def ranking(interaction: discord.Interaction):
        pass

    @bjg.bot.tree.command(name="loan", description="Weź pożyczkę (maksymalna kwota: 1000$)")
    async def loan(interaction: discord.Interaction, kwota: int):
        pass

    @bjg.bot.tree.command(name="pay loan", description="Spłać pożyczkę")
    async def pay_loan(interaction: discord.Interaction, kwota: int = None):
        pass

    @bjg.bot.tree.command(name="help", description="Wyświetl pomoc")
    async def help(interaction: discord.Interaction):
        pass
