from colorama import Fore

DIRECTION = {"up": 1, "right": 2, "down": 3, "left": 4}

LONGEST_BOAT_HEADER_LEN = (
    14  # This is a constant as the boat naming scheme in battleships is constant
)

POSITIONING_HELP_MSG = (
    f"{Fore.BLUE}HOW TO PLACE A SHIP:\n\n{Fore.WHITE}- To place/re-place a boat, type '{Fore.GREEN}boat coordinate direction{Fore.WHITE}'. E.g. 'carrier e10 up'\n\n"
    + f"- Once you are satisfied with the positions of your boats, type '{Fore.GREEN}continue{Fore.WHITE}'\n\n"
    + f"- To auto place all/remaining unplaced boats, type '{Fore.GREEN}auto{Fore.WHITE}'\n\n"
    + f"- To reset the game, type '{Fore.GREEN}reset{Fore.WHITE}'\n\n"
    + f"- To quit the game, type '{Fore.GREEN}quit{Fore.WHITE}'\n\n"
    + f"- To see this message again when placing your boats, type '{Fore.GREEN}help{Fore.WHITE}'\n\n"
    + f"Press '{Fore.GREEN}enter{Fore.WHITE}' to start/continue placing your ships..."
)

GUESSING_HELP_MSG = (
    f"{Fore.BLUE}HOW TO GUESS FOR A BOATS POSITIONS:\n\n{Fore.WHITE}- To guess for a boats position, type the position. E.g. '{Fore.GREEN}A1{Fore.WHITE}'.\n\n"
    + f"- To auto guess a position, type '{Fore.GREEN}auto{Fore.WHITE}'\n\n"
    + f"- To reset the game, type '{Fore.GREEN}reset{Fore.WHITE}'\n\n"
    + f"- To quit the game, type '{Fore.GREEN}quit{Fore.WHITE}'\n\n"
    + f"- To see this message again when guessing, type '{Fore.GREEN}help{Fore.WHITE}'\n\n"
    + f"Press '{Fore.GREEN}enter{Fore.WHITE}' to start/continue guessing your opponents ships..."
)

SALVO_GUESSING_HELP_MSG = (
    f"{Fore.BLUE}HOW TO GUESS FOR MULTIPLE BOATS POSITIONS:\n\n{Fore.WHITE}"
    + f"- The number of guesses per round equals the number of ships you have. To execute this, type the positions on the board."
    + f"E.g '{Fore.GREEN}A1 A3 B2{Fore.WHITE}' if you had 3 ships left\n\n"
    + f"- To auto guess multiple positions, type '{Fore.GREEN}auto{Fore.WHITE}'\n\n"
    + f"- To reset the game, type '{Fore.GREEN}reset{Fore.WHITE}'\n\n"
    + f"- To quit the game, type '{Fore.GREEN}quit{Fore.WHITE}'\n\n"
    + f"- To see this message again when guessing, type '{Fore.GREEN}help{Fore.WHITE}'\n\n"
    + f"Press '{Fore.GREEN}enter{Fore.WHITE}' to start/continue guessing your opponents ships..."
)
