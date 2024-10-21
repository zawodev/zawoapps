from blackjack.commands_setup.slash_commands_setup import slash_commands_setup
from blackjack.commands_setup.reaction_listener_setup import reaction_listener_setup
from blackjack.blackjackgame.blackjackgame import BlackJackGame

async def setup_blackjack(bot, casino_channel_id):
    # game logic
    bjg = BlackJackGame(bot, casino_channel_id)
    await bjg.setup()

    # new reaction UI for later
    reaction_listener_setup(bjg)
    # classic /commands
    slash_commands_setup(bjg)


