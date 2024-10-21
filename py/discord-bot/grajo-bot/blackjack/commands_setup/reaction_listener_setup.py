import discord
from blackjack.blackjackgame.blackjackgame import BlackJackGame

def reaction_listener_setup(bjg: BlackJackGame):

    @bjg.bot.listen()
    async def on_raw_reaction_add(payload):
        pass

    @bjg.bot.listen()
    async def on_raw_reaction_remove(payload):
        pass

    @bjg.bot.listen()
    async def on_raw_reaction_clear(payload):
        pass

    @bjg.bot.listen()
    async def on_raw_reaction_clear_emoji(payload):
        pass
