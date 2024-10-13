import random
import discord
from discord import app_commands, Embed
from asyncio import sleep, create_task

# Globalne dane gry
game_active = False
wait_time = 1
players = {}
deck = []
dealer = None


class Player:
    def __init__(self, user):
        self.user = user
        self.chips = 1000
        self.bet = [0]  # Zakład na każdą rękę
        self.hands = [[]]  # Obsługuje do dwóch rąk
        self.stands = [False]  # Zapisuje stan każdej ręki
        self.active_hand = 0
        self.split_used = False


class Dealer:
    def __init__(self):
        self.hand = []


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
        hand_info = ""
        for i, hand in enumerate(player.hands):
            hand_value = calculate_hand_value(hand)
            status = "✅" if player.stands[i] else "⏸️"

            hand_info += f"{status} - {' '.join(hand)} [{hand_value}]\n"

        embed.add_field(name=f"Gracz: {player.user.display_name} ({sum(player.bet)}$)", value=hand_info, inline=False)

    # Karty dealera
    dealer_hand_info = f"{dealer.hand[0]} ??"  # Ukryta karta dealera
    embed.add_field(name="Karty dealera", value=dealer_hand_info, inline=False)
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
        for i, hand in enumerate(player.hands):
            hand_value = calculate_hand_value(hand)
            winnings = 0

            if dealer_hand_value == 21 and len(dealer.hand) == 2:
                result = "dealer blackjack"
                winnings = 0
            elif hand_value > 21:
                result = "busted"
                winnings = 0
            elif hand_value == 21 and len(hand) == 2:
                result = "blackjack"
                winnings = player.bet[i] * 2.5
            elif dealer_hand_value > 21:
                result = "dealer busted"
                winnings = player.bet[i] * 2
            elif hand_value > dealer_hand_value:
                result = "brawooo wygrałeś"
                winnings = player.bet[i] * 2
            elif hand_value < dealer_hand_value:
                result = "dealer lepszy"
                winnings = 0
            else:
                result = "push"
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
        embed.add_field(
            name=f"Gracz: {player.user.display_name}",
            value=f"{player.chips - total_balance}$ -> {player.chips}$ ({total_winnings_txt}$)\n{hand_info}",
            inline=False
        )

    game_active = False
    players.clear()
    dealer = None

    await channel.send(embed=embed)



def setup_blackjack_commands(bot: discord.Client):
    """Dodaje komendy blackjacka do bota"""

    @bot.tree.command(name="bet", description="Postaw zakład")
    async def bet(interaction: discord.Interaction, amount: int):
        global game_active, players, dealer, deck, wait_time

        if game_active:
            await interaction.response.send_message("Gra jest już w toku, poczekaj na kolejną rundę!")
            return

        if interaction.user.id in players:
            await interaction.response.send_message("Jesteś już w grze!")
            return

        if amount < 1:
            await interaction.response.send_message("Nie możesz postawić mniej niż 1 żeton!")
            return

        player = players.get(interaction.user.id, Player(interaction.user))
        if amount > player.chips:
            await interaction.response.send_message("Nie masz wystarczająco żetonów!")
            return

        if len(players) == 0:
            shuffle_deck()
            dealer = Dealer()
            dealer.hand = [deal_card(), deal_card()]
            await interaction.channel.send("Gracz: " + interaction.user.display_name + " zaczął grę! Macie: " + str(wait_time) + " sekund na postawienie zakładu!")
            create_task(update_table(interaction.channel, wait_time))

        player.bet[0] = amount
        player.chips -= amount
        card = deal_card()
        player.hands = [[card, card]]
        player.stands = [False]
        players[interaction.user.id] = player

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

        if player.bet[0] > player.chips:
            await interaction.response.send_message("Nie masz wystarczająco żetonów na podwojenie!")
            return

        player.chips -= player.bet
        player.bet[0] *= 2
        player.hands[player.active_hand].append(deal_card())
        player.stands[player.active_hand] = True

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

        if player.bet > player.chips:
            await interaction.response.send_message("Nie masz wystarczająco żetonów na podzielenie!")

        player.split_used = True
        player.chips -= player.bet
        player.hands.append([player.hands[0].pop()])
        player.hands[0].append(deal_card())
        player.hands[1].append(deal_card())
        player.stands.append(False)

        await interaction.response.send_message("Podzieliłeś rękę na dwie!")
        await update_table(interaction.channel, 0)
