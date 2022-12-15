import os
import time
import sys

from colorama import Fore

from src.games.parent_battleship import BattleshipGame
from src.grid_components.salvo_grid import SalvoGrid
from util.exceptions import UserError
from util.constants import POSITIONING_HELP_MSG
from util.util import GridUtil


class SalvoBattleships(BattleshipGame):
    """Salvo Battleships player vs computer"""

    def __handle_shots_helper(self, choice: str, player_num: int) -> bool:
        """Helper method to both player and bot shot handlers"""

        player_shooting: SalvoGrid = self._player1 if player_num == 1 else self._player2
        player_recieving: SalvoGrid = (
            self._player2 if player_num == 1 else self._player1
        )

        positions = choice.split()
        outcomes = player_recieving.multi_shots_recieved(positions)
        os.system("cls")
        player_shooting.multi_shots_sent(positions, outcomes)
        if "lost" in outcomes:
            print(f"{Fore.GREEN}Player {player_num} wins the game!!!{Fore.WHITE}")
            return True
        player_shooting.display_board(True, player_num)
        print(f"{Fore.BLUE}{' '.join(outcomes)}!{Fore.WHITE}")
        return False

    def __handle_players_shots(self, player_num: int) -> bool:
        """Handles the scenario when a player fires a shot"""

        player_guessing: SalvoGrid = self._player1 if player_num == 1 else self._player2

        try:
            player_guessing.display_board(True, player_num)
            boats_left = player_guessing.get_boats_left()
            choice = input(
                f"{Fore.BLUE}\nEnter {boats_left} position(s) or less to try to shoot your opponents ships. E.g. C1 A2 B3 if you had 3 ships left: {Fore.WHITE}"
            ).lower()

            if choice == "quit":
                print(f"{Fore.GREEN}Thank you for playing!{Fore.WHITE}")
                sys.exit()
            elif choice == "reset":
                self._reset_game()
                sys.exit()
            elif choice == "auto":
                choice = player_guessing.multi_auto_guess()
                # validation is not required as it is generated
                print(f"{Fore.BLUE}Generating a positions... {choice}{Fore.WHITE}")
                time.sleep(1.5)
                os.system("cls")
                return self.__handle_shots_helper(choice, player_num)

            error_guesses = player_guessing.multi_guess_validation(choice)
            if len(error_guesses) != 0:
                raise UserError(
                    f"{' '.join([x for x in error_guesses])} are either repeated or unvalid positions"
                )

            # Go to the bots grid to see if it hit, missed or sunk a boat
            return self.__handle_shots_helper(choice, player_num)

        except UserError as e:
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)
            os.system("cls")
            return self.__handle_players_shots(player_num)

        except RuntimeError as e:
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)
            os.system("cls")
            return self.__handle_players_shots(player_num)

    def __handle_bots_shots(self, player_num: int) -> bool:
        """Handles the scenario when a player fires a shot"""

        player_guessing: SalvoGrid = self._player1 if player_num == 1 else self._player2

        player_guessing.display_board(True, 2)
        # auto guess will be unique to the bots guesses
        choice = player_guessing.multi_auto_guess()
        return self.__handle_shots_helper(choice, player_num)

    def __players_attack(self) -> None:
        """Where both player and computer choose a position to try to hit their opponent"""

        # player 1's turn to attack
        os.system("cls")
        if self._is_p1_bot:
            if self.__handle_bots_shots(1):
                return
        else:
            if self.__handle_players_shots(1):
                return

        input("Press enter to start Player 2's turn...")

        # player 2's turn to attack
        os.system("cls")
        if self._is_p2_bot:
            if self.__handle_bots_shots(2):
                return
        else:
            if self.__handle_players_shots(2):
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
