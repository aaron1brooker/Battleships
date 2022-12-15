import os
import time
import sys
from colorama import Fore

from src.games.parent_battleship import BattleshipGame
from src.grid_components.automated_grid import AutomatedGrid
from util.exceptions import UserError
from util.constants import POSITIONING_HELP_MSG


class TraditionalBattleships(BattleshipGame):
    """Traditional Battleships Player Vs Computer"""

    def __handle_shot_helper(self, choice: str, player_num: int) -> bool:
        """Helper method to both player and bot shot handlers"""

        player_shooting: AutomatedGrid = (
            self._player1 if player_num == 1 else self._player2
        )
        player_recieving: AutomatedGrid = (
            self._player2 if player_num == 1 else self._player1
        )

        outcome = player_recieving.shot_recieved(choice)
        os.system("cls")
        # update players guess grid
        player_shooting.shot_sent(choice, outcome)
        player_shooting.display_board(True, player_num)
        if outcome == "lost":
            print(f"{Fore.GREEN}Player {player_num} wins the game!!!{Fore.WHITE}")
            return True
        print(f"{Fore.BLUE}{outcome}!{Fore.WHITE}")
        return False

    def __handle_player_shot(self, player_num: int) -> bool:
        """Handles the scenario when a player fires a shot"""

        try:
            # Require exception handling as we can not guarantee user will enter a valid position

            player_guessing: AutomatedGrid = (
                self._player1 if player_num == 1 else self._player2
            )

            player_guessing.display_board(True, player_num)
            choice = input(
                f"{Fore.BLUE}\nEnter a position to try to shoot your opponents ship: {Fore.WHITE}"
            ).lower()

            # Provide user the option to quit or reset
            if choice == "quit":
                print(f"{Fore.GREEN}Thank you for playing!{Fore.WHITE}")
                sys.exit()
            elif choice == "reset":
                self._reset_game()
                sys.exit()

            # Check if the choice is repeated
            if player_guessing.is_guess_repeated(choice):
                print("This guess has already been made, try again")
                time.sleep(1.5)
                os.system("cls")
                return self.__handle_player_shot(player_num)

            return self.__handle_shot_helper(choice, player_num)

        except UserError as e:
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)
            os.system("cls")
            return self.__handle_player_shot(player_num)

    def __handle_bot_shot(self, player_num: int) -> bool:
        """Handles the scenario when a bot fires a shot"""

        player_guessing = self._player1 if player_num == 1 else self._player2

        self._player2.display_board(True, player_num)
        # auto guess will be unique to the bots guesses
        choice = player_guessing.auto_guess()

        print(f"Player {player_num} BOT chose {choice}")
        time.sleep(1.5)
        return self.__handle_shot_helper(choice, player_num)

    def __players_attack(self) -> None:
        """Where both player and computer choose a position to try to hit their opponent"""

        # player 1's turn to attack
        os.system("cls")
        if self._is_p1_bot:
            if self.__handle_bot_shot(1):
                return
        else:
            if self.__handle_player_shot(1):
                return

        input("Press enter to start Player 2's turn...")

        # player 2's turn to attack
        os.system("cls")
        if self._is_p2_bot:
            if self.__handle_bot_shot(2):
                return
        else:
            if self.__handle_player_shot(2):
                return

        input("Press enter to start Player 1's turn...")

        # recursive until bot or player wins
        self.__players_attack()

    def play_game(self) -> None:
        """Starts the Game"""

        os.system("cls")
        input(POSITIONING_HELP_MSG)

        # See whether player 1 is a bot and place boats accordingly
        self._place_boat_helper(1)

        input("Press enter to move onto player 2's turn...")
        os.system("cls")

        # Now we do the same but with player 2
        self._place_boat_helper(2)

        input("Press enter to start the game...")
        os.system("cls")
        self.__players_attack()
