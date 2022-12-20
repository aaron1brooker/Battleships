import os
import logging
import time
from colorama import Fore

from svc.game_setup import GameSetup
from src.grid_components.automated_grid import AutomatedGrid
from src.grid_components.salvo_grid import SalvoGrid
from src.grid_components.mines_grid import MinesGrid
from src.games.traditional_battleships import TraditionalBattleships
from src.games.salvo_battleship import SalvoBattleships
from src.games.hidden_mines import HiddenMines

# Logging output will be put into a txt file to help debugging
logging.basicConfig(filename="logs.txt", level=logging.INFO)


class Battleships:
    """Main class that holds/executes the different games"""

    def __init__(self) -> None:
        """Constructor"""

        # fetch config data
        game_config = GameSetup()
        self.__board, self.__boats = game_config.get_game_config()

    def __battleships(self, is_computer_p1: bool, is_computer_p2: bool) -> None:
        """Play Battleships (player vs computer)"""

        # Intialise Players
        player1 = AutomatedGrid(self.__board["x"], self.__board["y"], self.__boats)
        player2 = AutomatedGrid(self.__board["x"], self.__board["y"], self.__boats)

        # Play the game
        battleships = TraditionalBattleships(
            player1, player2, is_computer_p1, is_computer_p2
        )
        battleships.play_game()

    def __salvo_battleships(self, is_computer: bool) -> None:
        """Play Salvo Battleships (player vs computer)"""

        # Intialise Players
        player1 = SalvoGrid(self.__board["x"], self.__board["y"], self.__boats)
        player2 = SalvoGrid(self.__board["x"], self.__board["y"], self.__boats)

        # Play the game
        salvo_battleships = SalvoBattleships(player1, player2, False, is_computer)
        salvo_battleships.play_game()

    def __hidden_mines_battleship(self, is_computer: bool) -> None:
        "Play Hidden Mines Battleships"

        # Intialise Players
        player1 = MinesGrid(self.__board["x"], self.__board["y"], self.__boats)
        player2 = MinesGrid(self.__board["x"], self.__board["y"], self.__boats)

        # Play the game
        salvo_battleships = HiddenMines(player1, player2, False, is_computer)
        salvo_battleships.play_game()

    def menu(self):
        """Allows the user to choose the game to play"""

        os.system("clear")

        menu_screen = (
            f"{Fore.BLUE}MENU:\n{Fore.WHITE}1) Battleships (Player v Computer)\n2) Battleships (Two player)\n3) Salvo Battleships (Player v Computer)\n"
            + "4) Salvo Battleships (Two player)\n5) Hidden Mines Battleships (Player v Computer)\n"
            + "6) Hidden Mines Battleships (Two player)\n7) Battleships (Computer v Computer)\n8) Quit\n"
        )
        user_choice = input(menu_screen)

        if user_choice == "1":
            self.__battleships(False, True)
            return
        elif user_choice == "2":
            self.__battleships(False, False)
            return
        elif user_choice == "3":
            self.__salvo_battleships(True)
            return
        elif user_choice == "4":
            self.__salvo_battleships(False)
            return
        elif user_choice == "5":
            self.__hidden_mines_battleship(True)
            return
        elif user_choice == "6":
            self.__hidden_mines_battleship(False)
        elif user_choice == "7":
            self.__battleships(True, True)
            return
        elif user_choice == "8":
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
        # This is the wrapper handler to catch any unhandled exceptions
        logging.error(e)
        print("Ensure that the configuration file is correct and try again")


main()
