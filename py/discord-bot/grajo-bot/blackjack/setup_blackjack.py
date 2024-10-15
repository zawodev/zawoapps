from commands_setup.slash_commands_setup import slash_commands_setup
from commands_setup.reaction_listener_setup import reaction_listener_setup
from game.blackjack_game import BlackJackGame

async def setup_blackjack_game(bot):
    # game logic
    bjg = BlackJackGame(bot, 0)
    await bjg.setup()

    # new reaction UI for later
    reaction_listener_setup(bjg)
    # classic /commands
    slash_commands_setup(bjg)


