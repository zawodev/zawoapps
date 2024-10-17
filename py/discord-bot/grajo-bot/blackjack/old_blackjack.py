import random
import discord
from discord import app_commands, Embed
from asyncio import sleep, create_task
from datetime import datetime, timedelta
import asyncio

import json
import os


bot = None


# Globalne dane gry
game_active = False
wait_time = 5
players = {}
deck = []

# Słownik do przechowywania oczekujących napiwków {odbiorca_id: nadawca_id}
pending_tips = {}

loan_data = {}

DATA_FILE = "temp.json"

class Participant:
    def __init__(self, display_name, start_chips, data=None):
        self.display_name = display_name
        self.chips = data.get('chips', start_chips) if data else start_chips
        self.wins = data.get('wins', 0) if data else 0
        self.losses = data.get('losses', 0) if data else 0
        self.pushes = data.get('pushes', 0) if data else 0
        self.blackjacks = data.get('blackjacks', 0) if data else 0
        self.max_balance = data.get('max_balance', 0) if data else 0
        self.biggest_win = data.get('biggest_win', 0) if data else 0
        self.biggest_loss = data.get('biggest_loss', 0) if data else 0
        self.games_by_day = data.get('games_by_day', {}) if data else {}
        self.total_won_chips = data.get('total_won_chips', 0) if data else 0
        self.total_lost_chips = data.get('total_lost_chips', 0) if data else 0
        self.free_bet_by_day = data.get('free_bet_by_day', {}) if data else {}

    def to_dict(self):
        return {
            'display_name': self.display_name,
            'chips': self.chips,
            'wins': self.wins,
            'losses': self.losses,
            'pushes': self.pushes,
            'blackjacks': self.blackjacks,
            'max_balance': self.max_balance,
            'biggest_win': self.biggest_win,
            'biggest_loss': self.biggest_loss,
            'games_by_day': self.games_by_day,
            'total_won_chips': self.total_won_chips,
            'total_lost_chips': self.total_lost_chips,
            'free_bet_by_day': self.free_bet_by_day
        }


class Player2(Participant):
    def __init__(self, user, data=None):
        super().__init__(user.display_name, 1000, data)
        self.user = user
        self.bet = [0]  # Zakład na każdą rękę
        self.hands = [[]]  # Obsługuje do dwóch rąk
        self.stands = [False]  # Zapisuje stan każdej ręki
        self.active_hand = 0
        self.split_used = False
        self.forfeited = False

    def to_dict(self):
        return super().to_dict()


class Dealer2(Participant):
    def __init__(self, data=None):
        super().__init__("Dealer", 1000, data)
        self.hand = []

    def to_dict(self):
        return super().to_dict()  # Dealer nie potrzebuje dodatkowych pól

dealer = Dealer2()

def load_player_data():
    """Wczytaj dane graczy z pliku JSON"""
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}



def save_player_data(player_data=None):
    """Zapisz dane graczy do pliku JSON"""

    existing_data = load_player_data()

    # zapisz dane dealera
    existing_data['dealer'] = dealer.to_dict()

    if player_data is None:
        player_data = {str(player_id): player.to_dict() for player_id, player in players.items()}

    # nadpisz istniejące dane graczy
    for player_id, data in player_data.items():
        existing_data[player_id] = data

    with open(DATA_FILE, 'w') as f:
        json.dump(existing_data, f, indent=4)


def shuffle_deck():
    """Przetasuj talię kart"""
    global deck
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [rank + suit for rank in ranks for suit in suits]
    random.shuffle(deck)


def deal_card():
    """Rozdaj jedną kartę"""
    return deck.pop()


def calculate_hand_value(hand):
    """Oblicza wartość kart w ręce"""
    value = 0
    ace_count = 0
    for card in hand:
        rank = card[:-1]  # Ignoruje symbol
        if rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            ace_count += 1
            value += 11
        else:
            value += int(rank)
    while value > 21 and ace_count > 0:
        value -= 10
        ace_count -= 1
    return value


def calculate_card_value(card):
    """Oblicza wartość karty"""
    rank = card[:-1]
    if rank in ['J', 'Q', 'K']:
        return 10
    if rank == 'A':
        return 11
    return int(rank)


def create_table_embed():
    """Tworzy embed ze stanem gry dla wszystkich graczy i dealera"""
    embed = Embed(title="Place your bets now!", color=0x00ff00)
    global dealer, players



    # Karty graczy
    for player_id, player in players.items():
        bet_sum = sum(player.bet)
        #hand_info = f"{player.chips + bet_sum}$ -> {player.chips}$ ({bet_sum}$)\n"
        hand_info = ""
        for i, hand in enumerate(player.hands):
            hand_value = calculate_hand_value(hand)
            status = "✅" if player.stands[i] else "⏸️"

            hand_info += f"{status} - {' '.join(hand)} [{hand_value}] ({bet_sum}$)\n"

        embed.add_field(name=f"Gracz: {player.user.display_name}", value=hand_info, inline=False)

    # Karty dealera
    dealer_hand_info = f"{dealer.hand[0]} ??"  # Ukryta karta dealera
    embed.add_field(name="Dealer:", value=dealer_hand_info, inline=False)

    return embed


async def update_table(channel, sleep_time=0):
    """Aktualizuje stan stołu na kanale tekstowym"""
    global players, dealer, game_active

    await sleep(sleep_time)

    game_active = True
    embed = create_table_embed()
    await channel.send(embed=embed)

    # Sprawdź, czy wszyscy gracze zakończyli swoje ruchy
    if all(all(player.stands) for player in players.values()):
        await finalize_game(channel)


def update_games_by_day(player):
    """Aktualizuje liczbę gier gracza na dzień"""
    today = datetime.now().strftime('%Y-%m-%d')
    if today in player.games_by_day:
        player.games_by_day[today] += 1
    else:
        player.games_by_day[today] = 1


async def finalize_game(channel):
    global game_active, dealer, players

    # dealer dobiera karty do momentu, aż wartość ręki osiągnie co najmniej 17
    while calculate_hand_value(dealer.hand) < 17:
        dealer.hand.append(deal_card())

    embed = Embed(title="Thanks for the tip!", color=0xff0000)

    dealer_hand_value = calculate_hand_value(dealer.hand)
    #dealer_hand_info = f"{' '.join(dealer.hand)} [{dealer_hand_value}]"
    #embed.add_field(name="Dealer:", value=dealer_hand_info, inline=False)

    total_dealer_balance = 0
    total_dealer_winnings = 0

    def update_stats(player, winnings, balance):
        player.chips += winnings
        player.total_won_chips += max(balance, 0)
        player.total_lost_chips += max(-balance, 0)
        player.max_balance = max(player.max_balance, player.chips)
        player.biggest_win = max(player.biggest_win, balance)
        player.biggest_loss = max(player.biggest_loss, -balance)
        update_games_by_day(player)

    for player_id, player in players.items():
        total_winnings = 0
        hand_info = ""

        for i, hand in enumerate(player.hands):
            hand_value = calculate_hand_value(hand)
            winnings = 0

            if player.forfeited:
                result = "forfeited"
                winnings = player.bet[i] // 2
            elif dealer_hand_value == 21 and len(dealer.hand) == 2 and hand_value == 21 and len(hand) == 2:
                result = "blackjack push (very rare)"
                player.pushes += 1
                dealer.pushes += 1
                winnings = player.bet[i]
            elif dealer_hand_value == 21 and len(dealer.hand) == 2:
                result = "dealer blackjack"
                player.losses += 1
                dealer.blackjacks += 1
                dealer.wins += 1
                winnings = 0
            elif hand_value > 21:
                result = "busted"
                player.losses += 1
                dealer.wins += 1
                winnings = 0
            elif hand_value == 21 and len(hand) == 2:
                result = "blackjack"
                player.blackjacks += 1
                player.wins += 1
                dealer.losses += 1
                winnings = int(player.bet[i] * 2.5)
            elif dealer_hand_value > 21:
                result = "dealer busted"
                player.wins += 1
                dealer.losses += 1
                winnings = player.bet[i] * 2
            elif hand_value > dealer_hand_value:
                result = "brawooo wygrałeś"
                player.wins += 1
                dealer.losses += 1
                winnings = player.bet[i] * 2
            elif hand_value < dealer_hand_value:
                result = "dealer lepszy"
                player.losses += 1
                dealer.wins += 1
                winnings = 0
            else:
                result = "push"
                player.pushes += 1
                dealer.pushes += 1
                winnings = player.bet[i]

            # zapis wyników każdej ręki
            total_winnings += winnings
            balance = winnings - player.bet[i]
            winnings_txt = f"{'+' if balance > 0 else ''}{balance}"
            hand_info += f"{' '.join(hand)} [{hand_value}] - {result} ({winnings_txt}$)\n"

        total_balance = total_winnings - sum(player.bet)
        total_winnings_txt = f"{'+' if total_balance > 0 else ''}{total_balance}"

        update_stats(player, total_winnings, total_balance)

        # DEALER
        total_dealer_winnings -= total_winnings
        total_dealer_balance -= total_balance
        # END DEALER

        embed.add_field(
            name=f"Gracz: {player.user.display_name}",
            value=f"{player.chips - total_balance}$ -> {player.chips}$ ({total_winnings_txt}$)\n{hand_info}",
            inline=False
        )

    update_stats(dealer, total_dealer_winnings, total_dealer_balance)

    total_dealer_winnings_txt = f"{'+' if total_dealer_balance > 0 else ''}{total_dealer_balance}"
    dealer_hand_info = f"{' '.join(dealer.hand)} [{dealer_hand_value}]"

    embed.add_field(
        name=f"Dealer: {dealer.display_name}",
        value=f"{dealer.chips - total_dealer_balance}$ -> {dealer.chips}$ ({total_dealer_winnings_txt}$)\n{dealer_hand_info}",
        inline=False
    )

    save_player_data()  # Zapisz dane po zakończeniu gry

    game_active = False
    players.clear()

    await channel.send(embed=embed)



async def sprawdz_wszystkie_pozyczki(channel=None):
    dzisiaj = datetime.datetime.now()
    do_usuniecia = []  # lista użytkowników do usunięcia z loan_data po przetworzeniu

    for user_id, loan_info in loan_data.items():
        termin_splaty = loan_info['termin_splaty']
        if dzisiaj > termin_splaty:
            kwota_pozyczki = loan_info['kwota_pozyczki']
            timeout_czas = kwota_pozyczki  # czas timeouta równy pożyczonej kwocie w minutach

            # pobierz użytkownika na podstawie user_id
            user = await bot.fetch_user(user_id)
            if user:
                await user.timeout_for(duration=datetime.timedelta(minutes=timeout_czas))
                await user.send(f"Nie spłaciłeś pożyczki na czas! Zostajesz wyciszony na {timeout_czas} minut.")
                if channel is not None:
                    await channel.send(f"{user.mention} nie spłacił pożyczki na czas! Zostaje wyciszony na {timeout_czas} minut.")

            do_usuniecia.append(user_id)  # dodajemy użytkownika do listy do usunięcia

    # usuwanie przeterminowanych pożyczek
    for user_id in do_usuniecia:
        del loan_data[user_id]

    return len(do_usuniecia)  # opcjonalnie zwracamy ilość timeoutów




def setup_blackjack_commands(new_bot):
    """Dodaje komendy blackjacka do bota"""
    global bot
    bot = new_bot
    # bot.add_listener(sprawdz_wszystkie_pozyczki, name="on_message")

    @bot.tree.command(name="forfeit", description="Zrezygnuj z gry")
    async def forfeit(interaction: discord.Interaction):
        global game_active, players, dealer

        if not game_active:
            await interaction.response.send_message("Nie ma aktywnej gry!", ephemeral=True)
            return

        player = players.get(interaction.user.id)
        if not player:
            await interaction.response.send_message("Nie jesteś w grze!", ephemeral=True)
            return

        player.stands[0] = True
        if player.split_used:
            player.stands[1] = True

        player.forfeited = True

        save_player_data()

        await interaction.response.send_message("Zrezygnowałeś z gry!", ephemeral=True)

        await update_table(interaction.channel, 0)


        # Zwróć połowę wartości zakładu w żetonach graczowi i zakończ gre


    async def place_bet(interaction: discord.Interaction, player: Player2, amount: int):
        global players, dealer, deck, wait_time

        if len(players) == 0:
            shuffle_deck()
            player_data = load_player_data()
            dealer_data = player_data.get('dealer', {})
            dealer = Dealer2(dealer_data)
            dealer.hand = [deal_card(), deal_card()]
            await interaction.channel.send(interaction.user.display_name + " rozpoczął grę! Macie: " + str(
                wait_time) + " sekund na postawienie zakładu!")
            create_task(update_table(interaction.channel, wait_time))

        player.bet[0] = amount
        dealer.chips += amount
        player.hands = [[deal_card(), deal_card()]]
        player.stands = [False]
        players[interaction.user.id] = player

        save_player_data()

        # napisz ile osób gra i kto dołączył
        await interaction.channel.send(f"> {interaction.user.display_name} dołączył do gry! (łącznie {len(players)} graczy)")


    @bot.tree.command(name="freebet", description="Jeden dziennie darmowy zakład za 50$")
    async def freebet(interaction: discord.Interaction):
        player_data = load_player_data()
        player = player_data.get(str(interaction.user.id), {})
        today = datetime.now().strftime('%Y-%m-%d')

        if today in player.get('free_bet_by_day', {}):
            await interaction.response.send_message("Już odebrałeś darmowy zakład dzisiaj!", ephemeral=True)
            return

        if game_active:
            await interaction.response.send_message("Gra jest już w toku, poczekaj na kolejną rundę!", ephemeral=True)
            return

        if interaction.user.id in players:
            await interaction.response.send_message("Jesteś już w grze!", ephemeral=True)
            return

        player_instance = Player2(interaction.user, player)
        player_instance.free_bet_by_day[today] = True
        player_instance.total_won_chips += 50

        dealer.chips -= 50
        dealer.total_lost_chips += 50

        save_player_data()

        await interaction.response.send_message("Odebrano darmowy zakład!", ephemeral=True)
        await place_bet(interaction, player_instance, 50)


    @bot.tree.command(name="bet", description="Postaw zakład")
    async def bet(interaction: discord.Interaction, amount: int):
        global game_active, players, dealer, deck, wait_time

        player_data = load_player_data()

        if game_active:
            await interaction.response.send_message("Gra jest już w toku, poczekaj na kolejną rundę!", ephemeral=True)
            return

        if interaction.user.id in players:
            await interaction.response.send_message("Jesteś już w grze!", ephemeral=True)
            return

        if amount < 1:
            await interaction.response.send_message("Nie możesz postawić mniej niż 1 żeton!", ephemeral=True)
            return

        player_instance = Player2(interaction.user, player_data.get(str(interaction.user.id), {}))

        if amount > player_instance.chips:
            await interaction.response.send_message("Nie masz wystarczająco żetonów!", ephemeral=True)
            return

        player_instance.chips -= amount

        await interaction.response.send_message("Postawiono zakład o wysokości " + str(amount) + "$!", ephemeral=True)
        await place_bet(interaction, player_instance, amount)


    @bot.tree.command(name="hit", description="Dobierz kartę")
    async def hit(interaction: discord.Interaction):
        player = players.get(interaction.user.id)
        if not player:
            await interaction.response.send_message("Nie jesteś w grze!", ephemeral=True)
            return

        if all(player.stands):
            await interaction.response.send_message("już zakończyłeś ruch dla wszystkich rąk!", ephemeral=True)
            return

        player.hands[player.active_hand].append(deal_card())

        if calculate_hand_value(player.hands[player.active_hand]) > 21:
            player.stands[player.active_hand] = True
            if player.split_used and player.active_hand == 0:
                player.active_hand = 1
                await interaction.response.send_message("przekroczyłeś 21 na pierwszej rence, teraz druga reka", ephemeral=True)
            else:
                await interaction.response.send_message("Przekroczyłeś 21, automatyczne zakończenie ruchu!", ephemeral=True)
        else:
            await interaction.response.send_message("Dobierasz kartę!", ephemeral=True)

        await update_table(interaction.channel, 0)


    @bot.tree.command(name="stand", description="Zakończ swoją turę")
    async def stand(interaction: discord.Interaction):
        player = players.get(interaction.user.id)
        if not player:
            await interaction.response.send_message("Nie jesteś w grze!", ephemeral=True)
            return

        player.stands[player.active_hand] = True

        if player.split_used and player.active_hand == 0:
            player.active_hand = 1

        await update_table(interaction.channel, 0)

        if all(player.stands):
            await interaction.response.send_message(f"{player.user.display_name} zakończył swoją turę!", ephemeral=True)
        else:
            await interaction.response.send_message(f"{player.user.display_name} zakończył ruch dla ręki {player.active_hand}!", ephemeral=True)


    @bot.tree.command(name="double", description="Podwój zakład i dobierz kartę")
    async def double(interaction: discord.Interaction):
        player = players.get(interaction.user.id)
        if not player:
            await interaction.response.send_message("Nie jesteś w grze!", ephemeral=True)
            return

        if all(player.stands):
            await interaction.response.send_message("już zakończyłeś ruch lol", ephemeral=True)
            return

        if player.bet[player.active_hand] > player.chips:
            await interaction.response.send_message("Nie masz wystarczająco żetonów na podwojenie!", ephemeral=True)
            return

        player.chips -= player.bet[player.active_hand]
        dealer.chips += player.bet[player.active_hand]
        player.bet[player.active_hand] *= 2
        player.hands[player.active_hand].append(deal_card())
        player.stands[player.active_hand] = True

        save_player_data()

        if player.split_used and player.active_hand == 0:
            player.active_hand = 1
            await interaction.response.send_message("Podwoiłeś zakład na pierwszej ręce, teraz druga ręka", ephemeral=True)
        else:
            await interaction.response.send_message("Podwoiłeś zakład i zakończyłeś swoją turę!", ephemeral=True)

        await update_table(interaction.channel, 0)


    @bot.tree.command(name="split", description="Podziel rękę na dwie")
    async def split(interaction: discord.Interaction):
        player = players.get(interaction.user.id)
        if not player:
            await interaction.response.send_message("Nie jesteś w grze!", ephemeral=True)
            return

        if player.split_used:
            await interaction.response.send_message("Możesz podzielić tylko raz!", ephemeral=True)
            return

        if len(player.hands[0]) != 2:
            await interaction.response.send_message("Możesz podzielić tylko rękę z dwoma kartami!", ephemeral=True)
            return

        if calculate_card_value(player.hands[0][0]) != calculate_card_value(player.hands[0][1]):
            await interaction.response.send_message("karty są różnej wartości, nie możesz podzielić", ephemeral=True)
            return

        if player.bet[0] > player.chips:
            await interaction.response.send_message("Nie masz wystarczająco żetonów na podzielenie!", ephemeral=True)
            return

        player.split_used = True
        player.chips -= player.bet[0]
        dealer.chips += player.bet[0]
        player.bet.append(player.bet[0])
        player.hands.append([player.hands[0].pop()])
        player.hands[0].append(deal_card())
        player.hands[1].append(deal_card())
        player.stands.append(False)

        save_player_data()

        await interaction.response.send_message("Podzieliłeś rękę na dwie!", ephemeral=True)
        await update_table(interaction.channel, 0)


    @bot.tree.command(name="tip", description="Podaruj napiwek innemu graczowi")
    async def tip(interaction: discord.Interaction, target_player: discord.Member):
        global game_active

        if game_active:
            await interaction.response.send_message("Gra jest w toku, poczekaj na zakończenie rundy!", ephemeral=True)
            return

        player_data = load_player_data()
        tipper_data = player_data.get(str(interaction.user.id))

        if tipper_data is None:
            tipper_data = Player2(interaction.user).to_dict()
            player_data[str(interaction.user.id)] = tipper_data

        if tipper_data['chips'] < 1:
            await interaction.response.send_message("Nie masz wystarczająco żetonów, by dać napiwek!", ephemeral=True)
            return

        target_player_data = player_data.get(str(target_player.id))
        if target_player_data is None:
            target_player_data = Player2(target_player).to_dict()
            player_data[str(target_player.id)] = target_player_data

        pending_tips[str(interaction.user.id)] = str(target_player.id)
        await interaction.response.send_message(f"Co się mówi, {target_player.mention}? Użyj /thanks_for_the_tip, aby odebrać napiwek!")

        # Zapisanie stanu graczy
        save_player_data(player_data)

    @bot.tree.command(name="thanks_for_the_tip", description="Podziękuj za napiwek albo odbierz napiwek jako zbankrutowany gracz")
    async def thanks_for_the_tip(interaction: discord.Interaction, tipper: discord.Member = None):
        global game_active

        if game_active:
            await interaction.response.send_message("Gra jest w toku, poczekaj na zakończenie rundy!", ephemeral=True)
            return

        player_data = load_player_data()
        target_player_data = player_data.get(str(interaction.user.id))


        if target_player_data is None:
            target_player_data = Player2(interaction.user).to_dict()

        if tipper is None:  # Odbieranie napiwku od dealera (gdy gracz zbankrutował)
            if target_player_data['chips'] > 0:
                await interaction.response.send_message("Masz jeszcze kasę cwaniaku, tipy tylko dla bankrutów!")
                return

            target_player_data['chips'] += 1
            target_player_data['total_won_chips'] += 1

            dealer_data = player_data.get('dealer', {})
            dealer_data['chips'] -= 1
            dealer_data['total_lost_chips'] += 1
            player_data['dealer'] = dealer_data

            await interaction.response.send_message( f"Ho ho ho! No problem {interaction.user.display_name}!")
        else:  # Odbieranie napiwku od innego gracza
            tipper_data = player_data.get(str(tipper.id))
            pending_tip_target_id = pending_tips.get(str(tipper.id))

            if pending_tip_target_id != str(interaction.user.id):
                await interaction.response.send_message(f"{tipper.display_name} nie wysłał ci napiwku!", ephemeral=True)
                return

            if tipper_data is None:
                await interaction.response.send_message(f"{tipper.display_name} nie istnieje jakimś cudem?", ephemeral=True)
                return

            if tipper_data['chips'] < 1:
                await interaction.response.send_message(f"{tipper.display_name} jest zbankrutowany i nie może dać napiwku!")
                return

            # Przeniesienie 1$ z konta tippera do odbiorcy
            tipper_data['chips'] -= 1
            tipper_data['total_lost_chips'] += 1
            target_player_data['chips'] += 1
            target_player_data['total_won_chips'] += 1
            await interaction.response.send_message(f"{interaction.user.display_name} odebrał napiwek od {tipper.display_name}!")

            # Usunięcie zakończonego napiwku z pending_tips
            del pending_tips[str(tipper.id)]
            player_data[str(tipper.id)] = tipper_data

        player_data[str(interaction.user.id)] = target_player_data

        # Zapisanie danych graczy
        save_player_data(player_data)


    @bot.tree.command(name="stats", description="Wyświetl statystyki gracza lub wszystkich graczy")
    async def stats(interaction: discord.Interaction, user: discord.User = None):
        player_data = load_player_data()
        embed = Embed(title="Blackjack Stats", color=0x0000ff)

        def add_player_stats_to_embed(embed: Embed, display_name: str, data: dict):
            today_str = datetime.now().strftime('%Y-%m-%d')
            week_ago_str = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

            chips = data['chips']
            wins = data['wins']
            losses = data['losses']
            pushes = data['pushes']
            blackjacks = data['blackjacks']
            max_balance = data['max_balance']
            biggest_win = data['biggest_win']
            biggest_loss = data['biggest_loss']

            games_by_day = data.get('games_by_day', {})
            day_games = games_by_day.get(today_str, 0)
            week_games = sum(games for date, games in games_by_day.items() if week_ago_str <= date <= today_str)
            total_games = sum(games_by_day.values())

            total_won_chips = data['total_won_chips']
            total_lost_chips = data['total_lost_chips']

            # dodanie statystyk do embed
            embed.add_field(
                name=f"Gracz: {display_name}",
                value=(
                    f"🪙 Hajs: {chips}$\n"
                    f"🎮 Rozegranych (Today/Week/All): {day_games}/{week_games}/{total_games}\n"
                    f"🏆 Win/Push/Lose: {wins}/{pushes}/{losses}\n"
                    f"🃏 Blackjacks: {blackjacks}\n"
                    f"🔝 Maksymalny Hajs: {max_balance}$\n"
                    f"💥 Największa Wygrana: {biggest_win}$\n"
                    f"💸 Największa Przegrana: {biggest_loss}$\n"
                    f"💰 Łącznie Wygrane: {total_won_chips}$\n"
                    f"💸 Łącznie Przegrane: {total_lost_chips}$"
                ),
                inline=False
            )

        # sprawdzenie, czy podano usera
        if user:
            if user == bot.user:  # statystyki dealera
                dealer_data = player_data.get('dealer', None)  # zakładam, że dealer ma jakieś dane
                if dealer_data:
                    add_player_stats_to_embed(embed, "Dealer", dealer_data)
                else:
                    await interaction.response.send_message(f"Nie znaleziono statystyk dla dealera.")
                    return
            else:  # statystyki konkretnego gracza
                data = player_data.get(str(user.id), None)
                if data:
                    add_player_stats_to_embed(embed, user.display_name, data)
                else:
                    await interaction.response.send_message(f"Nie znaleziono statystyk dla {user.display_name}.")
                    return
        else:  # statystyki wszystkich graczy
            for player_id, data in player_data.items():
                add_player_stats_to_embed(embed, data['display_name'], data)

        await interaction.response.send_message(embed=embed)


    @bot.tree.command(name="ranking", description="wyświetl ranking graczy od najbogatszego do najbiedniejszego")
    async def ranking(interaction: discord.Interaction):
        player_data = load_player_data()
        sorted_players = sorted(player_data.items(), key=lambda x: x[1]['chips'], reverse=True)

        embed = Embed(title="Blackjack Ranking", color=0xff00ff)

        for player_id, data in sorted_players:
            display_name = data['display_name']
            chips = data['chips']

            embed.add_field(
                name=f"Gracz: {display_name}",
                value=f"🪙 Hajs: {chips}$",
                inline=False
            )

        await interaction.response.send_message(embed=embed)


    @bot.tree.command(name="loan", description="Weź pożyczkę (maksymalna kwota: 1000$)")
    async def loan(interaction: discord.Interaction, kwota: int):
        return
        user_id = str(interaction.user.id)

        if kwota > 1000:
            await interaction.response.send_message("Maksymalna kwota pożyczki to 1000$.")
            return

        if kwota <= 0:
            await interaction.response.send_message("Nie możesz pożyczyć kwoty mniejszej lub równej 0.")
            return

        if user_id in loan_data:
            await interaction.response.send_message("Masz już aktywną pożyczkę! Najpierw ją spłać.")
            return

        # obliczenie początkowej kwoty do zwrotu (5% początkowe od kwoty pożyczki)
        kwota_do_zwrotu = int(kwota * 1.05)  # zaokrąglamy w dół
        termin_splaty =  datetime.datetime.now() + datetime.timedelta(days=3)  # 3 dni na spłatę

        # zapisanie pożyczki w strukturze danych
        loan_data[user_id] = {
            'kwota_pozyczki': kwota,
            'kwota_do_zwrotu': kwota_do_zwrotu,
            'data_pozyczki': datetime.datetime.now(),
            'termin_splaty': termin_splaty
        }

        await interaction.response.send_message(
            f"Pożyczyłeś {kwota}$! Kwota do zwrotu to {kwota_do_zwrotu}$. Termin spłaty: {termin_splaty}."
        )


    @bot.tree.command(name="pay_loan", description="Spłać pożyczkę")
    async def pay_loan(interaction: discord.Interaction, kwota: int = None):
        return
        user_id = str(interaction.user.id)

        if user_id not in loan_data:
            await interaction.response.send_message("Nie masz żadnej aktywnej pożyczki.")
            return

        loan_info = loan_data[user_id]
        data_pozyczki = loan_info['data_pozyczki']
        termin_splaty = loan_info['termin_splaty']
        dzisiaj = datetime.datetime.now()

        # obliczenie ile dni minęło od pożyczenia
        dni_minelo = (dzisiaj - data_pozyczki).days

        # jeśli pożyczka nie została spłacona na czas, dodaj 5% dziennie (od oryginalnej kwoty pożyczki)
        if dni_minelo > 0:
            dodatkowy_koszt = int(loan_info['kwota_pozyczki'] * 0.05 * dni_minelo)
            loan_info['kwota_do_zwrotu'] = loan_info['kwota_pozyczki'] + dodatkowy_koszt

        # jeśli nie podano kwoty, wyświetl informacje o pożyczce
        if kwota is None:
            pozostalo_dni = (termin_splaty - dzisiaj).days
            await interaction.response.send_message(
                f"Pożyczyłeś {loan_info['kwota_pozyczki']}$.\n"
                f"Kwota do zwrotu: {loan_info['kwota_do_zwrotu']}$.\n"
                f"Pozostało ci {pozostalo_dni} dni na spłatę.\n"
                f"Termin spłaty: {termin_splaty}."
            )
            return

        # jeśli podano kwotę do spłaty
        if kwota >= loan_info['kwota_do_zwrotu']:
            del loan_data[user_id]
            await interaction.response.send_message(f"Spłaciłeś pożyczkę! Kwota {kwota}$ została zwrócona.")
        else:
            await interaction.response.send_message(
                f"Kwota {kwota}$ jest niewystarczająca. Musisz zwrócić {loan_info['kwota_do_zwrotu']}$.")


    @bot.tree.command(name="help", description="Wyświetl pomoc")
    async def help(interaction: discord.Interaction):
        embed = Embed(title="Blackjack Help", color=0xffffff)
        embed.add_field(
            name="Komendy",
            value=(
                "/bet <kwota> - Postaw zakład\n"
                "/hit - Dobierz kartę\n"
                "/stand - Zakończ swoją turę\n"
                "/double - Podwój zakład i dobierz kartę\n"
                "/split - Podziel rękę na dwie\n"
                "/freebet - Odbierz darmowy zakład o wysokości 50$\n"
                "/tip <gracz> - Podaruj napiwek innemu graczowi\n"
                "/thanks_for_the_tip - Podziękuj za napiwek albo odbierz napiwek jako zbankrutowany gracz\n"
                "/stats - Wyświetl statystyki wszystkich graczy\n"
            ),
            inline=False
        )

        await interaction.response.send_message(embed=embed)
