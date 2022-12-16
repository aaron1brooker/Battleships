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

    def __battleships(self):
        """Play Battleships (player vs computer)"""

        # Intialise Players
        player1 = AutomatedGrid(self.__board["x"], self.__board["y"], self.__boats)
        player2 = AutomatedGrid(self.__board["x"], self.__board["y"], self.__boats)

        # Play the game
        battleships = TraditionalBattleships(player1, player2, False, True)
        battleships.play_game()

    def __battleships_two_player(self):
        """Play Battleships (Two Player)"""

        # Intialise Players
        player1 = AutomatedGrid(self.__board["x"], self.__board["y"], self.__boats)
        player2 = AutomatedGrid(self.__board["x"], self.__board["y"], self.__boats)

        # Play the game
        battleships = TraditionalBattleships(player1, player2, False, False)
        battleships.play_game()

    def __salvo_battleships(self):
        """Play Salvo Battleships (player vs computer)"""

        # Intialise Players
        player1 = SalvoGrid(self.__board["x"], self.__board["y"], self.__boats)
        player2 = SalvoGrid(self.__board["x"], self.__board["y"], self.__boats)

        # Play the game
        salvo_battleships = SalvoBattleships(player1, player2, False, True)
        salvo_battleships.play_game()

    def __salvo_battleships_two_player(self):
        """Play Salvo Battleships (Two Player)"""

        # Intialise Players
        player1 = SalvoGrid(self.__board["x"], self.__board["y"], self.__boats)
        player2 = SalvoGrid(self.__board["x"], self.__board["y"], self.__boats)

        # Play the game
        salvo_battleships = SalvoBattleships(player1, player2, False, False)
        salvo_battleships.play_game()
    
    def __hidden_mines_battleship(self):
        "Play Hidden Mines Battleships"

        # Intialise Players
        player1 = MinesGrid(self.__board["x"], self.__board["y"], self.__boats)
        player2 = MinesGrid(self.__board["x"], self.__board["y"], self.__boats)

        # Play the game
        salvo_battleships = HiddenMines(player1, player2, False, True)
        salvo_battleships.play_game()        

    def menu(self):
        """Allows the user to choose the game to play"""

        os.system("cls")

        menu_screen = (
            f"{Fore.BLUE}MENU:\n{Fore.WHITE}1) Battleships (player v computer)\n2) Battleships (two player)\n3) Salvo Battleships (player v computer)\n"
            + "4) Salvo Battleships (two player)\n5) Quit\n"
        )
        user_choice = input(menu_screen)

        if user_choice == "1":
            self.__battleships()
            return
        elif user_choice == "2":
            self.__battleships_two_player()
            return
        elif user_choice == "3":
            self.__salvo_battleships()
            return
        elif user_choice == "4":
            self.__salvo_battleships_two_player()
            return
        elif user_choice == "5":
            self.__hidden_mines_battleship()
            return
        elif user_choice == "6":
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
