import discord
from blackjack.game.blackjack_game import BlackJackGame
from blackjack.old_blackjack import players, game_active

from blackjack.systems import (
    join_table_system as jts,
    bet_system as bs,
    table_game_system as tgs,
    tip_system as ts,
    stats_system as ss,
    ranking_system as rs,
    loan_system as ls,
    help_system as hs
)


async def get_player_if_valid(bjg: BlackJackGame,
                              interaction: discord.Interaction,
                              check_game_activity=False,
                              check_chips=0):
    # zawsze sprawdzamy czy jakiś stół istnieje
    table = await bjg.get_table_or_notify(interaction)
    if table is None:
        return None

    # opcjonalne sprawdzenie, czy gra jest aktywna
    if check_game_activity:
        table_game_active = table.game_active_or_notify(interaction)
        if table_game_active:
            return None

    # uzyskanie profilu gracza
    player_profile = bjg.get_player_profile(interaction.user.id)
    player = table.get_or_create_player(player_profile)

    # opcjonalne sprawdzenie, czy gracz ma wystarczająco żetonów
    if check_chips == -1:
        chips_amount = player.get_current_hand().bet
    else:
        chips_amount = int(check_chips)
    has_chips = player.has_chips_or_notify(interaction, chips_amount)
    if not has_chips:
        return None

    return player


def slash_commands_setup(bjg: BlackJackGame):

    @bjg.bot.tree.command(name="join table", description="Dołącz do stołu na danym kanale")
    async def join_table(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction)
        await jts.join_table(interaction, player)

    @bjg.bot.tree.command(name="leave table", description="Opuść stół")
    async def leave_table(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction)
        await jts.leave_table(interaction, player)

    @bjg.bot.tree.command(name="freebet", description="Jeden dziennie darmowy zakład za 50$")
    async def freebet(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction, check_game_activity=True)
        await bs.free_bet(interaction, player)

    @bjg.bot.tree.command(name="bet", description="Zakład na grę")
    async def bet(interaction: discord.Interaction, amount: int):
        player = await get_player_if_valid(bjg, interaction, check_game_activity=True, check_chips=amount)
        await bs.bet(interaction, player, amount)

    @bjg.bot.tree.command(name="hit", description="Dobierz kartę")
    async def hit(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction, check_game_activity=True)
        await tgs.hit(interaction, player)

    @bjg.bot.tree.command(name="stand", description="Zakończ swoją turę")
    async def stand(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction, check_game_activity=True)
        await tgs.stand(interaction, player)

    @bjg.bot.tree.command(name="double", description="Podwój zakład i dobierz kartę")
    async def double(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction, check_game_activity=True, check_chips=-1)
        await tgs.double(interaction, player)

    @bjg.bot.tree.command(name="split", description="Podziel rękę na dwie")
    async def split(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction, check_game_activity=True, check_chips=-1)
        await tgs.split(interaction, player)

    @bjg.bot.tree.command(name="forfeit", description="Zrezygnuj z gry")
    async def forfeit(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction, check_game_activity=True)
        await tgs.forfeit(interaction, player)

    @bjg.bot.tree.command(name="tip", description="Podaruj napiwek innemu graczowi")
    async def tip(interaction: discord.Interaction, target_player: discord.Member):
        player = await get_player_if_valid(bjg, interaction, check_chips=1)
        await ts.tip(interaction, player, target_player)

    @bjg.bot.tree.command(name="thanks for the tip", description="Podziękuj za napiwek albo odbierz napiwek jako zbankrutowany gracz")
    async def thanks_for_the_tip(interaction: discord.Interaction, tipper: discord.Member = None):
        player = await get_player_if_valid(bjg, interaction)
        await ts.thanks_for_the_tip(interaction, player, tipper)

    @bjg.bot.tree.command(name="stats", description="Wyświetl statystyki gracza lub wszystkich graczy")
    async def stats(interaction: discord.Interaction, user: discord.User = None):
        player = await get_player_if_valid(bjg, interaction)
        await ss.stats(interaction, player, user)

    @bjg.bot.tree.command(name="ranking", description="wyświetl ranking graczy od najbogatszego do najbiedniejszego")
    async def ranking(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction)
        await rs.ranking(interaction, player)

    @bjg.bot.tree.command(name="loan", description="Weź pożyczkę (maksymalna kwota: 1000$)")
    async def loan(interaction: discord.Interaction, kwota: int):
        player = await get_player_if_valid(bjg, interaction)
        await ls.loan(interaction, player, kwota)

    @bjg.bot.tree.command(name="pay loan", description="Spłać pożyczkę")
    async def pay_loan(interaction: discord.Interaction, kwota: int = None):
        player = await get_player_if_valid(bjg, interaction)
        await ls.pay_loan(interaction, player, kwota)

    @bjg.bot.tree.command(name="help", description="Wyświetl pomoc")
    async def help(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction)
        await hs.help(interaction, player)
