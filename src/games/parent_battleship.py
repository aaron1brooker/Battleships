import os
import time
import sys

from colorama import Fore

from util.constants import POSITIONING_HELP_MSG
from util.exceptions import UserError
from util.util import GridUtil
from src.grid_components.automated_grid import AutomatedGrid


class BattleshipGame:
    """Parent class that holds all shared methods for Battleships games"""

    def __init__(self, player1, player2, p1_bot: bool, p2_bot: bool) -> None:
        """Constructor"""

        # Player1 or Player2 can take the form of any grid_component class
        self._player1 = player1
        self._player2 = player2

        self._is_p1_bot = p1_bot
        self._is_p2_bot = p2_bot

    def _reset_game(self) -> None:
        """Resets the game back to the start"""

        print(f"{Fore.GREEN}RESETTING GAME{Fore.WHITE}")
        self._player1.reset_grid()
        self._player2.reset_grid()
        time.sleep(1.5)
        self.play_game()

    def _player_place_boats(self, player_num: int) -> None:
        """Where the real player can place their boats on the grid"""

        player: AutomatedGrid = self._player1 if player_num == 1 else self._player2

        os.system("cls")  # clears the console so we can put the updated grid in
        player.display_board(False, player_num)
        player.display_remaining_boats()
        choice = input(
            f"{Fore.BLUE}\nEnter the boat, postion and direction or type help for a list of commands: {Fore.WHITE}"
        ).lower()

        if choice == "continue":
            # continue will exit the recursive function and move onto the game
            if player.unplaced_boats_left():
                print(f"{Fore.BLUE}Placing all remaining boats...{Fore.WHITE}")
                player.auto_place_all()
                time.sleep(2)

            os.system("cls")
            player.display_board(False, player_num)
            return

        elif choice == "help":
            # Allows the user to look at the instructions again
            os.system("cls")
            input(POSITIONING_HELP_MSG)
            self._player_place_boats(player_num)
            return

        elif choice == "auto":
            # Allows the user to auto place all unplaced boats
            print(f"{Fore.BLUE}Placing remaining boats...{Fore.WHITE}")
            player.auto_place_all()
            time.sleep(1.5)
            self._player_place_boats(player_num)
            return

        elif choice == "quit":
            print(f"{Fore.GREEN}Thank you for playing!{Fore.WHITE}")
            sys.exit()

        elif choice == "reset":
            self._reset_game()
            sys.exit()

        try:
            # try to place the boat
            boat, pos, direction = GridUtil.seperate_choice(choice)
            if not player.place_boat(pos, boat, direction):
                print(
                    f"{Fore.RED}It was not possible to position this boat. Please try again{Fore.WHITE}"
                )
                time.sleep(1.5)
        except UserError as e:
            # Not a valid response has been given by the user
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)

        self._player_place_boats(player_num)

    def _place_boat_helper(self, player_num: int) -> None:
        """Helper function for placing boats in play_game"""

        player: AutomatedGrid = self._player1 if player_num == 1 else self._player2
        is_player_bot = self._is_p1_bot if player_num == 1 else self._is_p2_bot

        if is_player_bot:
            player.auto_place_all()
            print(
                f"{Fore.BLUE}Player {player_num} BOT... placing all boats{Fore.WHITE}"
            )
            time.sleep(1.5)
        else:
            if not self._player_place_boats(player_num):
                # If player wants to quit game
                return
        # Show final result
        player.display_board(False, player_num)
        print(f"{Fore.GREEN}Boat positions are now locked in...{Fore.WHITE}")

    def play_game():
        """This method will be overwritten in each child class"""
        # required for the reset method
        pass
