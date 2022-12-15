import os
import time

from colorama import Fore

from util.exceptions import UserError
from util.constants import POSITIONING_HELP_MSG
from util.util import GridUtil
from src.grid_components.salvo_grid import SalvoGrid


class SalvoBattleships:
    """Salvo Battleships player vs computer"""

    def __init__(self, player1: SalvoGrid, player2: SalvoGrid) -> None:
        """Constructor"""

        self.__player1 = player1
        self.__player2 = player2

        # place boats for the computer
        self.__player2.auto_place_all()

    def _reset_game(self) -> None:
        """Resets the game back to the start"""

        print(f"{Fore.GREEN}RESETTING GAME{Fore.WHITE}")
        self.__player1.reset_grid()
        self.__player2.reset_grid()
        time.sleep(1.5)
        self.play_game()

    def _player_place_boats(self) -> bool:  # True if they want to continue to play
        """Where the player can place their boats on the grid"""

        os.system("cls")  # clears the console so we can put the updated grid in
        self.__player1.display_board(False, 1)
        self.__player1.display_remaining_boats()
        choice = input(
            f"{Fore.BLUE}\nEnter the boat, postion and direction or type help for a list of commands: {Fore.WHITE}"
        ).lower()

        if choice == "continue":
            # continue will exit the recursive function and move onto the game
            if self.__player1.unplaced_boats_left():
                print(f"{Fore.BLUE}Placing all remaining boats...{Fore.WHITE}")
                self.__player1.auto_place_all()
                time.sleep(2)

            os.system("cls")
            self.__player1.display_board(False, 1)
            print(f"{Fore.GREEN}Placing all of the bots boats...{Fore.WHITE}")
            time.sleep(1.5)
            print(
                f"{Fore.GREEN}Boat positions are now locked in... Lets play!{Fore.WHITE}"
            )
            return True

        elif choice == "help":
            # Allows the user to look at the instructions again
            os.system("cls")
            input(Fore.BLUE + POSITIONING_HELP_MSG + Fore.WHITE)
            self._player_place_boats()
            return True

        elif choice == "auto":
            # Allows the user to auto place all unplaced boats
            print(f"{Fore.BLUE}Placing remaining boats...{Fore.WHITE}")
            self.__player1.auto_place_all()
            time.sleep(1.5)
            self._player_place_boats()
            return True

        elif choice == "quit":
            print(f"{Fore.GREEN}Thank you for playing!{Fore.WHITE}")
            return False

        elif choice == "reset":
            self._reset_game()
            return True

        try:
            # try to place the boat
            boat, pos, direction = GridUtil.seperate_choice(choice)
            if not self.__player1.place_boat(pos, boat, direction):
                print(
                    f"{Fore.RED}It was not possible to position this boat. Please try again{Fore.WHITE}"
                )
                time.sleep(1.5)
        except UserError as e:
            # Not a valid response has been given by the user
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)

        self._player_place_boats()
        return True

    def __handle_shots(
        self, is_bot: bool, choice: str
    ) -> bool:  # True if a player wins the game
        """Handles the scenario when the opposition fires multiple shots"""

        player_shooting = self.__player2 if is_bot else self.__player1
        player_recieving = self.__player2 if not is_bot else self.__player1
        player_num = 2 if is_bot else 1  # The number of the shooter

        positions = choice.split()
        if len(positions) > player_shooting.get_boats_left():
            raise UserError(
                f"Did not give {player_shooting.get_boats_left()} positions"
            )
        outcomes = player_recieving.multi_shots_recieved(positions)
        os.system("cls")
        player_shooting.multi_shots_sent(positions, outcomes, player_num)
        if "lost" in outcomes:
            print(
                f"{Fore.GREEN}{'Player' if not is_bot else 'bot'} wins the game!!!{Fore.WHITE}"
            )
            return True
        player_shooting.display_board(True, player_num)
        print(f"{Fore.BLUE}{' '.join(outcomes)}!{Fore.WHITE}")
        return False

    def __players_attack(self) -> None:
        """Where both player and computer choose positions to try to hit their opponent"""

        try:
            # players turn - unique guess required
            os.system("cls")
            self.__player1.display_board(True, 1)
            boats_left = self.__player1.get_boats_left()
            choice = input(
                f"{Fore.BLUE}\nEnter {boats_left} position(s) or less to try to shoot your opponents ships. E.g. C1 A2 B3 if you had 3 ships left: {Fore.WHITE}"
            ).lower()

            if choice == "quit":
                print(f"{Fore.GREEN}Thank you for playing!{Fore.WHITE}")
                return
            elif choice == "reset":
                self._reset_game()
                return

            error_guesses = self.__player1.multi_guess_validation(choice)
            if len(error_guesses) != 0:
                raise UserError(
                    f"{' '.join([x for x in error_guesses])} are either repeated or unvalid positions"
                )

            # Go to the bots grid to see if it hit, missed or sunk a boat
            if self.__handle_shots(False, choice):
                return
            input("Press enter to start the BOTS turn...")

            # bots turn
            os.system("cls")
            self.__player2.display_board(True, 2)
            # auto guess will be unique to the bots guesses
            choice = self.__player2.multi_auto_guess()
            if self.__handle_shots(True, choice):
                return
            input("Press enter to start your turn again...")

            # recursive until bot or player wins
            self.__players_attack()

        except UserError as e:
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)
            self.__players_attack()

        except RuntimeError as e:
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)
            self.__players_attack()

    def play_game(self) -> None:
        """Starts the Game"""

        os.system("cls")
        input(Fore.BLUE + POSITIONING_HELP_MSG + Fore.WHITE)

        if self._player_place_boats():
            input("Press enter to start the game...")
            os.system("cls")
            self.__players_attack()
