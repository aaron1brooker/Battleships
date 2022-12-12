import os
import logging
import time
from colorama import Fore

from svc.game_setup import GameSetup
from src.grid_components.automated_grid import AutomatedGrid
from src.games.traditional_battleships import Traditional_Battleships

# Logging output will be put into a txt file to help debugging
logging.basicConfig(filename="logs.txt", level=logging.INFO)


class Battleships:
    """Main class that holds/executes the different games"""

    def __init__(self) -> None:
        """Constructor"""

        # fetch config data
        game_config = GameSetup()
        self.__board, self.__boats = game_config.get_game_config()

    def __battleships(self):
        """Play Battleships (real player vs computer)"""

        # Intialise Players
        player1 = AutomatedGrid(self.__board["x"], self.__board["y"], self.__boats)
        player2 = AutomatedGrid(self.__board["x"], self.__board["y"], self.__boats)

        # Play the game
        battleships = Traditional_Battleships(player1, player2)
        battleships.play_game()

    def menu(self):
        """Allows the user to choose the game to play"""

        os.system("cls")

        menu_screen = f"{Fore.BLUE}Menu:\n1) Battleships\n2) Quit{Fore.WHITE}\n"
        user_choice = input(menu_screen)

        if user_choice == "1":
            self.__battleships()
            return
        elif user_choice == "2":
            print(f"{Fore.BLUE}Goodbye!!{Fore.WHITE}")
            return
        else:
            print(f"{Fore.RED}Not a valid choice. Try again")
            time.sleep(1.5)
            self.menu()


def main():
    try:
        battleships = Battleships()
        battleships.menu()
    except Exception as e:
        print(e)
        print("Ensure that the configuration file is correct and try again")


main()
