from commands_setup.slash_commands_setup import slash_commands_setup
from commands_setup.reaction_listener_setup import reaction_listener_setup
from game_logic.game_logic import BlackJackGame

def setup_blackjack_game(bot):
    # game logic
    BJG = BlackJackGame(0, 1)

    # new reaction UI for later
    reaction_listener_setup(bot, BJG)
    # classic /commands
    slash_commands_setup(bot, BJG)


