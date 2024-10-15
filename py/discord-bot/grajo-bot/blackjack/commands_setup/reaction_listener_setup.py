import discord
from blackjack.game_logic.game_logic import BlackJackGame

def reaction_listener_setup(bot, BJG: BlackJackGame):

    @bot.listen()
    async def on_raw_reaction_add(payload):
        pass

    @bot.listen()
    async def on_raw_reaction_remove(payload):
        pass

    @bot.listen()
    async def on_raw_reaction_clear(payload):
        pass

    @bot.listen()
    async def on_raw_reaction_clear_emoji(payload):
        pass
