from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.views.table_view.table_view import TableView
import discord
from gambling_bot.models.player import Player
from gambling_bot.views import a4_table_view
import random

from gambling_bot.core.hand_values import HandValue


class BlackjackTableView(TableView):
    def __init__(self, table: BlackJackTable):
        super().__init__()
        self.table = table

    def create_embeds(self):
        embeds = []
        used_colors = set()

        for player in self.table.players:
            player: Player

            player_color = random.randint(0x100000, 0xFFFFFF)
            while player_color in used_colors:
                player_color = random.randint(0x100000, 0xFFFFFF)
            used_colors.add(player_color)

            for hand in player.hands:
                hand_value = hand.value()
                embed = discord.Embed(
                    title=player,
                    description=hand,
                    color=player_color
                )
                embed.set_thumbnail(url=HandValue.from_int(hand_value))
                embeds.append(embed)

        dealer_embed = discord.Embed(
            title=self.table.dealer,
            description=f"{self.table.dealer.hand.cards[0]} ??",
            color=0xFFFF00
        )
        dealer_value = self.table.dealer.hand.cards[0].value()
        dealer_embed.set_thumbnail(url=HandValue.from_int(dealer_value))
        embeds.append(dealer_embed)

        return embeds

    @discord.ui.button(label="hit", style=discord.ButtonStyle.green, custom_id="hit")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.hit(interaction.user.id)
        await a4_table_view.display(interaction, self.table)
        self.table.check()

    @discord.ui.button(label="stand", style=discord.ButtonStyle.red, custom_id="stand")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.stand(interaction.user.id)
        await a4_table_view.display(interaction, self.table)
        self.table.check()

    @discord.ui.button(label="double", style=discord.ButtonStyle.blurple, custom_id="double")
    async def double(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.double(interaction.user.id)
        await a4_table_view.display(interaction, self.table)
        self.table.check()

    @discord.ui.button(label="split", style=discord.ButtonStyle.gray, custom_id="split")
    async def split(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.split(interaction.user.id)
        await a4_table_view.display(interaction, self.table)
        self.table.check()

    @discord.ui.button(label="forfeit", style=discord.ButtonStyle.danger, custom_id="forfeit")
    async def forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.forfeit(interaction.user.id)
        await a4_table_view.display(interaction, self.table)
        self.table.check()
