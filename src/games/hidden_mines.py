import os
import sys
import time

from colorama import Fore

from src.grid_components.mines_grid import MinesGrid
from src.games.parent_battleship import BattleshipGame
from util.constants import GUESSING_HELP_MSG, POSITIONING_HELP_MSG
from util.exceptions import UserError


class HiddenMines(BattleshipGame):
    """Play Hidden Mines Battleships"""

    def __handle_shot_helper(self, choice: str, player_num: int) -> bool:
        """Helper method to both player and bot shot handlers"""

        player_shooting: MinesGrid = self._player1 if player_num == 1 else self._player2
        player_recieving: MinesGrid = (
            self._player2 if player_num == 1 else self._player1
        )

        outcomes = player_recieving.shot_recieved_mine(choice)
        os.system("cls")
        # update players guess grid
        user_outcomes = []  # this is what the user sees
        for status in outcomes:
            for choice in outcomes[status]:
                player_shooting.shot_sent(choice, status)
                if status == "lost":
                    print(
                        f"{Fore.GREEN}Player {player_num} wins the game!!!{Fore.WHITE}"
                    )
                    return True

                user_outcomes.append(status)

        player_shooting.display_board(True, player_num)
        print(f"{Fore.BLUE}{' '.join(user_outcomes)}!{Fore.WHITE}")
        return False

    def __handle_player_shot(self, player_num: int) -> bool:
        """Handles the scenario when a player fires a shot"""

        try:
            # Require exception handling as we can not guarantee user will enter a valid position

            player_guessing: MinesGrid = (
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
            elif choice == "auto":
                choice = player_guessing.auto_guess()
                print(f"{Fore.BLUE}Generating a position... {choice}{Fore.WHITE}")
                time.sleep(1.5)
                os.system("cls")
                return self.__handle_shot_helper(choice, player_num)
            elif choice == "help":
                os.system("cls")
                input(GUESSING_HELP_MSG)
                return self.__handle_player_shot(player_num)

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

        player_guessing: MinesGrid = self._player1 if player_num == 1 else self._player2

        player_guessing.display_board(True, player_num)
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
        self._player1.auto_place_mines()

        input("Press enter to move onto player 2's turn...")
        os.system("cls")

        # Now we do the same but with player 2
        self._place_boat_helper(2)
        self._player2.auto_place_mines()

        input("Press enter to start the game...")
        os.system("cls")
        input(GUESSING_HELP_MSG)
        os.system("cls")
        self.__players_attack()
