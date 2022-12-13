from colorama import Fore

DIRECTION = {"up": 1, "right": 2, "down": 3, "left": 4}

LONGEST_BOAT_HEADER_LEN = (
    14  # This is a constant as the boat naming scheme in battleships is constant
)

POSITIONING_HELP_MSG = (
    f"{Fore.BLUE}RULES:\n\n{Fore.WHITE}- To place/re-place a boat, type '{Fore.GREEN}boat coordinate direction{Fore.WHITE}'. E.g. 'carrier e10 up'\n\n"
    + f"- Once you are satisfied with the positions of your boats, type '{Fore.GREEN}continue{Fore.WHITE}'\n\n"
    + f"-To auto place all/remaining unplaced boats, type '{Fore.GREEN}auto{Fore.WHITE}'\n\n"
    + f"- To see this message again when placing your boats, type '{Fore.GREEN}help{Fore.WHITE}\n\n"
    + f"Press '{Fore.GREEN}enter{Fore.WHITE}' to start/continue placing your ships..."
)
