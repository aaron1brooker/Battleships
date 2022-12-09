import os
import logging
import time
from colorama import Fore

from svc.game_setup import GameSetup
from src.automated_grid import AutomatedGrid
from src.player_grid import PlayerGrid
from util.util import GridUtil
from util.exceptions import UserError

# Logging output will be put into a txt file to help debugging
logging.basicConfig(filename="logs.txt", level=logging.INFO)


def setup_game():
    """Setup the grid and position boats"""

    try:
        game_config = GameSetup()
        board, boats = game_config.get_game_config()

        # Intialise Players
        player = PlayerGrid(board["x"], board["y"], boats)
        bot = AutomatedGrid(board["x"], board["y"], boats)
        bot.auto_place_all()
    except UserError as e:
        print(e)
        print("Reconfigure configuration file and try again")
        return

    # Let real player place the boat
    while player.unplaced_boats_left():
        os.system("cls")  # clears the console so we can put the updated grid in
        player.display_board()
        player.display_remaining_boats()
        choice = input(
            f"{Fore.BLUE}\nEnter the boat, postion and direction. E.g. carrier E1 down: {Fore.WHITE}"
        )
        try:
            boat, pos, direction = GridUtil.seperate_choice(choice)
            if not player.place_boat(pos, boat, direction):
                print(
                    f"{Fore.RED}It was not possible to position this boat. Please try again{Fore.WHITE}"
                )
                time.sleep(1.5)
        except UserError as e:
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)

    print(f"{Fore.GREEN}All boats have been placed... Lets play!{Fore.WHITE}")
    time.sleep(1.5)

    return player, bot


def play_game(player1, player2):
    os.system("cls")
    player1.display_board()

    # players turn
    # make guess unique
    choice = input(
        f"{Fore.BLUE}\nEnter a position to try to shoot your opponents ship: {Fore.WHITE}"
    )
    try:
        outcome = player2.shots_recieved(choice)
        if outcome == "lost":
            print(f"{Fore.GREEN}Player 1 wins the game!!!{Fore.WHITE}")
            return
        print(outcome)
        time.sleep(1.5)
        os.system("cls")

        # bots turn
        choice = player2.auto_guess()
        print(f"{Fore.BLUE}\nBOTS turn... It chose {choice}{Fore.WHITE}")
        time.sleep(1.5)
        outcome = player1.shots_recieved(choice)
        if outcome == "lost":
            print(f"{Fore.GREEN}Bot wins the game!!!{Fore.WHITE}")
            return
        print(outcome)
        time.sleep(1.5)

        play_game(player1, player2)

    except UserError as e:
        print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
        time.sleep(1.5)
        play_game(player1, player2)


def start_game():
    """This will start battleships"""

    player, bot = setup_game()
    play_game(player, bot)


start_game()
