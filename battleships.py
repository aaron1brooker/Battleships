import os
import logging
import time
from colorama import Fore

from svc.game_setup import GameSetup
from src.player_grid import PlayerGrid
from util.util import Util
from util.exceptions import UserError

# Logging output will be put into a txt file to help debugging
logging.basicConfig(filename="battleships_logs.txt", level=logging.INFO)


def start_game():
    """This will start battleships"""

    # Setup game
    try:
        game_config = GameSetup()
        board, boats = game_config.get_game_config()
        player = PlayerGrid(board["x"], board["y"], boats)
    except UserError as e:
        print(e)
        print("Reconfigure configuration file and try again")
        return

    while player.is_boats():
        os.system("clear")  # clears the console so we can put the updated grid in
        player.display_board()
        player.display_remaining_boats()
        choice = input(
            f"{Fore.BLUE}\nEnter the boat, postion and direction. E.g. carrier E1 down: {Fore.WHITE}"
        )
        try:
            boat, pos, direction = Util.seperate_choice(choice)
            if not player.place_boat(pos, boat, direction):
                print(
                    f"{Fore.RED}It was not possible to position this boat. Please try again{Fore.WHITE}"
                )
                time.sleep(1.5)
        except UserError as e:
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)

    os.system("clear")
    player.display_board()


start_game()
