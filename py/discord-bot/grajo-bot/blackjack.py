import random
import discord
from discord import app_commands, Embed
from asyncio import sleep, create_task

import json
import os

# Globalne dane gry
game_active = False
wait_time = 1
players = {}
deck = []
dealer = None

# Słownik do przechowywania oczekujących napiwków {odbiorca_id: nadawca_id}
pending_tips = {}

DATA_FILE = "player_data.json"


class Player:
    def __init__(self, user, data=None):
        self.user = user
        self.display_name = user.display_name
        self.chips = data.get('chips', 1000) if data else 1000
        self.bet = [0]  # Zakład na każdą rękę
        self.hands = [[]]  # Obsługuje do dwóch rąk
        self.stands = [False]  # Zapisuje stan każdej ręki
        self.active_hand = 0
        self.split_used = False

        # Statystyki
        self.total_games = data.get('total_games', 0) if data else 0
        self.wins = data.get('wins', 0) if data else 0
        self.losses = data.get('losses', 0) if data else 0
        self.pushes = data.get('pushes', 0) if data else 0
        self.blackjacks = data.get('blackjacks', 0) if data else 0
        self.max_balance = data.get('max_balance', 1000) if data else 1000
        self.biggest_win = data.get('biggest_win', 0) if data else 0

    def to_dict(self):
        return {
            'display_name': self.display_name,
            'chips': self.chips,
            'total_games': self.total_games,
            'wins': self.wins,
            'losses': self.losses,
            'pushes': self.pushes,
            'blackjacks': self.blackjacks,
            'max_balance': self.max_balance,
            'biggest_win': self.biggest_win,
        }


class Dealer:
    def __init__(self):
        self.hand = []


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

    if player_data is None:
        player_data = {str(player_id): player.to_dict() for player_id, player in players.items()}

    # nadpisz istniejące dane
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

    # Karty dealera
    dealer_hand_info = f"{dealer.hand[0]} ??"  # Ukryta karta dealera
    embed.add_field(name="Dealer:", value=dealer_hand_info, inline=False)

    # Karty graczy
    for player_id, player in players.items():
        bet_sum = sum(player.bet)
        hand_info = f"{player.chips + bet_sum}$ -> {player.chips}$ ({bet_sum}$)\n"
        for i, hand in enumerate(player.hands):
            hand_value = calculate_hand_value(hand)
            status = "✅" if player.stands[i] else "⏸️"

            hand_info += f"{status} - {' '.join(hand)} [{hand_value}]\n"

        embed.add_field(name=f"Gracz: {player.user.display_name}", value=hand_info, inline=False)

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


async def finalize_game(channel):
    global game_active, dealer, players

    # dealer dobiera karty do momentu, aż wartość ręki osiągnie co najmniej 17
    while calculate_hand_value(dealer.hand) < 17:
        dealer.hand.append(deal_card())

    embed = Embed(title="Thanks for the tip!", color=0xff0000)

    dealer_hand_value = calculate_hand_value(dealer.hand)
    dealer_hand_info = f"{' '.join(dealer.hand)} [{dealer_hand_value}]"
    embed.add_field(name="Dealer:", value=dealer_hand_info, inline=False)

    for player_id, player in players.items():
        total_winnings = 0
        hand_info = ""
        player.total_games += 1
        for i, hand in enumerate(player.hands):
            hand_value = calculate_hand_value(hand)
            winnings = 0

            if dealer_hand_value == 21 and len(dealer.hand) == 2:
                result = "dealer blackjack"
                player.losses += 1
                winnings = 0
            elif hand_value > 21:
                result = "busted"
                player.losses += 1
                winnings = 0
            elif hand_value == 21 and len(hand) == 2:
                result = "blackjack"
                player.blackjacks += 1
                player.wins += 1
                winnings = player.bet[i] * 2.5
            elif dealer_hand_value > 21:
                result = "dealer busted"
                player.wins += 1
                winnings = player.bet[i] * 2
            elif hand_value > dealer_hand_value:
                result = "brawooo wygrałeś"
                player.wins += 1
                winnings = player.bet[i] * 2
            elif hand_value < dealer_hand_value:
                result = "dealer lepszy"
                player.losses += 1
                winnings = 0
            else:
                result = "push"
                player.pushes += 1
                winnings = player.bet[i]

            # zapis wyników każdej ręki
            total_winnings += winnings
            balance = winnings - player.bet[i]
            winnings_txt = f"{'+' if balance > 0 else ''}{balance}"
            hand_info += f"{' '.join(hand)} [{hand_value}] - {result} ({winnings_txt}$)\n"

        # zaktualizowanie liczby żetonów gracza
        player.chips += total_winnings
        total_balance = total_winnings - sum(player.bet)
        total_winnings_txt = f"{'+' if total_balance > 0 else ''}{total_balance}"

        # Aktualizacja statystyk
        player.max_balance = max(player.max_balance, player.chips)
        player.biggest_win = max(player.biggest_win, total_balance)

        embed.add_field(
            name=f"Gracz: {player.user.display_name}",
            value=f"{player.chips - total_balance}$ -> {player.chips}$ ({total_winnings_txt}$)\n{hand_info}",
            inline=False
        )

    save_player_data()  # Zapisz dane po zakończeniu gry

    game_active = False
    players.clear()
    dealer = None

    await channel.send(embed=embed)




def setup_blackjack_commands(bot: discord.Client):
    """Dodaje komendy blackjacka do bota"""

    @bot.tree.command(name="bet", description="Postaw zakład")
    async def bet(interaction: discord.Interaction, amount: int):
        global game_active, players, dealer, deck, wait_time

        player_data = load_player_data()

        if game_active:
            await interaction.response.send_message("Gra jest już w toku, poczekaj na kolejną rundę!")
            return

        if interaction.user.id in players:
            await interaction.response.send_message("Jesteś już w grze!")
            return

        if amount < 1:
            await interaction.response.send_message("Nie możesz postawić mniej niż 1 żeton!")
            return

        player = Player(interaction.user, player_data.get(str(interaction.user.id), {}))

        if amount > player.chips:
            await interaction.response.send_message("Nie masz wystarczająco żetonów!")
            return

        if len(players) == 0:
            shuffle_deck()
            dealer = Dealer()
            dealer.hand = [deal_card(), deal_card()]
            await interaction.channel.send("Gracz: " + interaction.user.display_name + " zaczął grę! Macie: " + str(
                wait_time) + " sekund na postawienie zakładu!")
            create_task(update_table(interaction.channel, wait_time))

        player.bet[0] = amount
        player.chips -= amount
        player.hands = [[deal_card(), deal_card()]]
        player.stands = [False]
        players[interaction.user.id] = player

        save_player_data()

        await interaction.response.send_message(f"Postawiłeś {amount} żetonów!", ephemeral=True)


    @bot.tree.command(name="hit", description="Dobierz kartę")
    async def hit(interaction: discord.Interaction):
        player = players.get(interaction.user.id)
        if not player:
            await interaction.response.send_message("Nie jesteś w grze!")
            return

        if all(player.stands):
            await interaction.response.send_message("już zakończyłeś ruch dla wszystkich rąk!")
            return

        player.hands[player.active_hand].append(deal_card())

        if calculate_hand_value(player.hands[player.active_hand]) > 21:
            player.stands[player.active_hand] = True
            if player.split_used and player.active_hand == 0:
                player.active_hand = 1
                await interaction.response.send_message("przekroczyłeś 21 na pierwszej rence, teraz druga reka")
            else:
                await interaction.response.send_message("Przekroczyłeś 21, automatyczne zakończenie ruchu!")
        else:
            await interaction.response.send_message("Dobierasz kartę!")

        await update_table(interaction.channel, 0)


    @bot.tree.command(name="stand", description="Zakończ swoją turę")
    async def stand(interaction: discord.Interaction):
        player = players.get(interaction.user.id)
        if not player:
            await interaction.response.send_message("Nie jesteś w grze!")
            return

        player.stands[player.active_hand] = True

        if player.split_used and player.active_hand == 0:
            player.active_hand = 1
            await interaction.response.send_message("Zakończyłeś ruch dla ręki 1, teraz druga ręka")
        else:
            await interaction.channel.send(f"Zakończyłeś ruch!")

        await update_table(interaction.channel, 0)

        if all(player.stands):
            await interaction.response.send_message(f"{player.user.display_name} zakończył swoją turę!")


    @bot.tree.command(name="double", description="Podwój zakład i dobierz kartę")
    async def double(interaction: discord.Interaction):
        player = players.get(interaction.user.id)
        if not player:
            await interaction.response.send_message("Nie jesteś w grze!")
            return

        if all(player.stands):
            await interaction.response.send_message("już zakończyłeś ruch lol")
            return

        if player.bet[player.active_hand] > player.chips:
            await interaction.response.send_message("Nie masz wystarczająco żetonów na podwojenie!")
            return

        player.chips -= player.bet[player.active_hand]
        player.bet[player.active_hand] *= 2
        player.hands[player.active_hand].append(deal_card())
        player.stands[player.active_hand] = True

        save_player_data()

        if player.split_used and player.active_hand == 0:
            player.active_hand = 1
            await interaction.response.send_message("Podwoiłeś zakład na pierwszej ręce, teraz druga ręka")
        else:
            await interaction.response.send_message("Podwoiłeś zakład i zakończyłeś swoją turę!")

        await update_table(interaction.channel, 0)


    @bot.tree.command(name="split", description="Podziel rękę na dwie")
    async def split(interaction: discord.Interaction):
        player = players.get(interaction.user.id)
        if not player:
            await interaction.response.send_message("Nie jesteś w grze!")
            return

        if player.split_used:
            await interaction.response.send_message("Możesz podzielić tylko raz!")
            return

        if len(player.hands[0]) != 2:
            await interaction.response.send_message("Możesz podzielić tylko rękę z dwoma kartami!")
            return

        if calculate_card_value(player.hands[0][0]) != calculate_card_value(player.hands[0][1]):
            await interaction.response.send_message("karty są różnej wartości, nie możesz podzielić")
            return

        if player.bet[0] > player.chips:
            await interaction.response.send_message("Nie masz wystarczająco żetonów na podzielenie!")
            return

        player.split_used = True
        player.chips -= player.bet[0]
        player.bet.append(player.bet[0])
        player.hands.append([player.hands[0].pop()])
        player.hands[0].append(deal_card())
        player.hands[1].append(deal_card())
        player.stands.append(False)

        save_player_data()

        await interaction.response.send_message("Podzieliłeś rękę na dwie!")
        await update_table(interaction.channel, 0)


    @bot.tree.command(name="tip", description="Podaruj napiwek innemu graczowi")
    async def tip(interaction: discord.Interaction, target_player: discord.Member):
        global game_active

        if game_active:
            await interaction.response.send_message("Gra jest w toku, poczekaj na zakończenie rundy!")
            return

        player_data = load_player_data()
        tipper_data = player_data.get(str(interaction.user.id))

        if tipper_data is None:
            tipper_data = Player(interaction.user).to_dict()
            player_data[str(interaction.user.id)] = tipper_data

        if tipper_data['chips'] < 1:
            await interaction.response.send_message("Nie masz wystarczająco żetonów, by dać napiwek!")
            return

        target_player_data = player_data.get(str(target_player.id))
        if target_player_data is None:
            target_player_data = Player(target_player).to_dict()
            player_data[str(target_player.id)] = target_player_data

        pending_tips[str(interaction.user.id)] = str(target_player.id)
        await interaction.response.send_message(f"Co się mówi, {target_player.mention}? Użyj /thanks_for_the_tip, aby odebrać napiwek!")

        # Zapisanie stanu graczy
        save_player_data(player_data)

    @bot.tree.command(name="thanks_for_the_tip", description="Podziękuj za napiwek albo odbierz napiwek jako zbankrutowany gracz")
    async def thanks_for_the_tip(interaction: discord.Interaction, tipper: discord.Member = None):
        global game_active

        if game_active:
            await interaction.response.send_message("Gra jest w toku, poczekaj na zakończenie rundy!")
            return

        player_data = load_player_data()
        target_player_data = player_data.get(str(interaction.user.id))

        if target_player_data is None:
            target_player_data = Player(interaction.user).to_dict()

        if tipper is None:  # Odbieranie napiwku od dealera (gdy gracz zbankrutował)
            if target_player_data['chips'] > 0:
                await interaction.response.send_message("Masz jeszcze kasę cwaniaku, tipy tylko dla bankrutów!")
                return

            target_player_data['chips'] += 1
            await interaction.response.send_message( f"Ho ho ho! No problem {interaction.user.display_name}!")
        else:  # Odbieranie napiwku od innego gracza
            tipper_data = player_data.get(str(tipper.id))
            pending_tip_target_id = pending_tips.get(str(tipper.id))

            if pending_tip_target_id != str(interaction.user.id):
                await interaction.response.send_message(f"{tipper.display_name} nie wysłał ci napiwku!")
                return

            if tipper_data is None:
                await interaction.response.send_message(f"{tipper.display_name} nie istnieje jakimś cudem?")
                return

            if tipper_data['chips'] < 1:
                await interaction.response.send_message(f"{tipper.display_name} jest zbankrutowany i nie może dać napiwku!")
                return

            # Przeniesienie 1$ z konta tippera do odbiorcy
            tipper_data['chips'] -= 1
            target_player_data['chips'] += 1
            await interaction.response.send_message(f"{interaction.user.display_name} odebrał napiwek od {tipper.display_name}!")

            # Usunięcie zakończonego napiwku z pending_tips
            del pending_tips[str(tipper.id)]
            player_data[str(tipper.id)] = tipper_data

        player_data[str(interaction.user.id)] = target_player_data
        # Zapisanie danych graczy
        save_player_data(player_data)



