import discord
from blackjack.blackjackgame.blackjackgame import BlackJackGame
from blackjack.old_blackjack import players, game_active
from datetime import datetime

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
from blackjack.table.player import Player


async def get_player_if_valid(
        bjg: BlackJackGame,
        interaction: discord.Interaction,
        check_game_activity=False,
        check_chips=0,
        check_min_max_bet=False,
        check_player_freebet_used=False,
        check_player_bet_used=False):
    # CHECK 0: zawsze sprawdzamy, czy dany stół w ogóle istnieje
    table = await bjg.get_table_or_notify(interaction)
    if table is None:
        return None

    # CHECK 1: opcjonalne sprawdzenie, czy gra jest aktywna
    if check_game_activity:
        table_game_active = table.game_active_or_notify(interaction)
        if table_game_active:
            return None

    # weź gracza, jego profil, dodaj na stół
    player_profile = bjg.get_player_profile(interaction.user.id)

    # tworzenie gracza
    if not table.has_player_with_id(player_profile.profile_id):
        player = Player(player_profile, table)
    else:
        player = table.get_player_with_id(player_profile.profile_id)

    # CHECK 2: opcjonalne sprawdzenie, czy gracz ma wystarczająco żetonów
    if check_chips == -1:
        chips_amount = player.get_current_hand().bet
    else:
        chips_amount = int(check_chips)
    has_chips = player.has_chips_or_notify(interaction, chips_amount)
    if not has_chips:
        return None

    # CHECK 3: opcjonalne sprawdzenie, czy zakład mieści się w przedziale
    if check_min_max_bet:
        if chips_amount < table.min_bet:
            await interaction.response.send_message(f"Minimalny zakład to {table.min_bet}$", ephemeral=True)
            return None
        if chips_amount > table.max_bet:
            await interaction.response.send_message(f"Maxymalny zakład to {table.max_bet}$", ephemeral=True)
            return None

    # CHECK 4: opcjonalne sprawdzenie, czy gracz już odebrał darmowy zakład
    if check_player_freebet_used:
        today = datetime.now().strftime('%Y-%m-%d')
        if today in player.profile.stats.freebet_dates:
            await interaction.response.send_message("Już odebrałeś swoj darmowy zakład dzisiaj", ephemeral=True)
            return None

    # CHECK 5: opcjonalne sprawdzenie, czy gracz już postawił zakład
    if check_player_bet_used:
        if player.bet_used:
            await interaction.response.send_message("Już postawiłeś zakład", ephemeral=True)
            return None

    return player


async def slash_commands_setup(bot, bjg: BlackJackGame):

    @bot.tree.command(name="join_table", description="Dołącz do stołu na danym kanale")
    async def join_table(interaction: discord.Interaction):
        player = await get_player_if_valid(
            bjg,
            interaction,
            check_game_activity=False,
            check_chips=0,
            check_min_max_bet=False,
            check_player_freebet_used=False,
            check_player_bet_used=False
        )
        if player is not None:
            await jts.join_table(interaction, player)

    @bot.tree.command(name="leave_table", description="Opuść stół")
    async def leave_table(interaction: discord.Interaction):
        player = await get_player_if_valid(
            bjg,
            interaction,
            check_game_activity=False,
            check_chips=0,
            check_min_max_bet=False,
            check_player_freebet_used=False,
            check_player_bet_used=False
        )
        if player is not None:
            await jts.leave_table(interaction, player)

    @bot.tree.command(name="free_bet", description="Jeden dziennie darmowy zakład za 50$")
    async def freebet(interaction: discord.Interaction):
        player = await get_player_if_valid(
            bjg,
            interaction,
            check_game_activity=True,
            check_chips=0,
            check_min_max_bet=True,
            check_player_freebet_used=True,
            check_player_bet_used=True
        )
        if player is not None:
            await bs.free_bet(interaction, player)

    @bot.tree.command(name="bet", description="Zakład na grę")
    async def bet(interaction: discord.Interaction, amount: int):
        player = await get_player_if_valid(
            bjg,
            interaction,
            check_game_activity=True,
            check_chips=amount,
            check_min_max_bet=True,
            check_player_freebet_used=False,
            check_player_bet_used=True
        )
        if player is not None:
            await bs.bet(interaction, player, amount)

    @bot.tree.command(name="hit", description="Dobierz kartę")
    async def hit(interaction: discord.Interaction):
        player = await get_player_if_valid(
            bjg,
            interaction,
            check_game_activity=True,
            check_chips=0,
            check_min_max_bet=False,
            check_player_freebet_used=False,
            check_player_bet_used=False
        )
        if player is not None:
            await tgs.hit(interaction, player)

    @bot.tree.command(name="stand", description="Zakończ swoją turę")
    async def stand(interaction: discord.Interaction):
        player = await get_player_if_valid(
            bjg,
            interaction,
            check_game_activity=True,
            check_chips=0,
            check_min_max_bet=False,
            check_player_freebet_used=False,
            check_player_bet_used=False
        )
        if player is not None:
            await tgs.stand(interaction, player)

    @bot.tree.command(name="double", description="Podwój zakład i dobierz kartę")
    async def double(interaction: discord.Interaction):
        player = await get_player_if_valid(
            bjg,
            interaction,
            check_game_activity=True,
            check_chips=-1,
            check_min_max_bet=False,
            check_player_freebet_used=False,
            check_player_bet_used=False
        )
        if player is not None:
            await tgs.double(interaction, player)

    @bot.tree.command(name="split", description="Podziel rękę na dwie")
    async def split(interaction: discord.Interaction):
        player = await get_player_if_valid(
            bjg,
            interaction,
            check_game_activity=True,
            check_chips=-1,
            check_min_max_bet=False,
            check_player_freebet_used=False,
            check_player_bet_used=False
        )
        if player is not None:
            await tgs.split(interaction, player)

    @bot.tree.command(name="forfeit", description="Zrezygnuj z gry")
    async def forfeit(interaction: discord.Interaction):
        player = await get_player_if_valid(
            bjg,
            interaction,
            check_game_activity=True,
            check_chips=0,
            check_min_max_bet=False,
            check_player_freebet_used=False,
            check_player_bet_used=False
        )
        if player is not None:
            await tgs.forfeit(interaction, player)

    @bot.tree.command(name="tip", description="Podaruj napiwek innemu graczowi")
    async def tip(interaction: discord.Interaction, target_player: discord.Member):
        player = await get_player_if_valid(bjg, interaction, check_chips=1)
        await ts.tip(interaction, player, target_player)

    @bot.tree.command(name="thanks_for_the_tip", description="Podziękuj za napiwek albo odbierz napiwek jako zbankrutowany gracz")
    async def thanks_for_the_tip(interaction: discord.Interaction, tipper: discord.Member = None):
        player = await get_player_if_valid(bjg, interaction)
        if player is not None:
            await ts.thanks_for_the_tip(interaction, player, tipper)

    @bot.tree.command(name="stats", description="Wyświetl statystyki gracza lub wszystkich graczy")
    async def stats(interaction: discord.Interaction, user: discord.User = None):
        player = await get_player_if_valid(bjg, interaction)
        if player is not None:
            await ss.stats(interaction, player, user)

    @bot.tree.command(name="ranking", description="wyświetl ranking graczy od najbogatszego do najbiedniejszego")
    async def ranking(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction)
        if player is not None:
            await rs.ranking(interaction, player)

    @bot.tree.command(name="loan", description="Weź pożyczkę (maksymalna kwota: 1000$)")
    async def loan(interaction: discord.Interaction, kwota: int):
        player = await get_player_if_valid(bjg, interaction)
        if player is not None:
            await ls.loan(interaction, player, kwota)

    @bot.tree.command(name="pay_loan", description="Spłać pożyczkę")
    async def pay_loan(interaction: discord.Interaction, kwota: int = None):
        player = await get_player_if_valid(bjg, interaction)
        if player is not None:
            await ls.pay_loan(interaction, player, kwota)

    @bot.tree.command(name="help", description="Wyświetl pomoc")
    async def help(interaction: discord.Interaction):
        player = await get_player_if_valid(bjg, interaction)
        if player is not None:
            await hs.help(interaction, player)
