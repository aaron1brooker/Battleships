import os
import time
from colorama import Fore

from src.grid_components.automated_grid import AutomatedGrid
from util.util import GridUtil
from util.exceptions import UserError
from util.constants import POSITIONING_HELP_MSG


class TraditionalBattleships:
    """Traditional Battleships Player Vs Computer"""

    def __init__(self, player: AutomatedGrid, bot: AutomatedGrid) -> None:
        """Constructor"""

        self.__player = player
        self.__bot = bot

        # place boats for the computer
        self.__bot.auto_place_all()

    def _reset_game(self) -> None:
        """Resets the game back to the start"""

        print(f"{Fore.GREEN}RESETTING GAME{Fore.WHITE}")
        self.__bot.reset_grid()
        self.__player.reset_grid()
        time.sleep(1.5)
        self.play_game()

    def _player_place_boats(self) -> bool:  # True if they want to continue to play
        """Where the player can place their boats on the grid"""

        os.system("cls")  # clears the console so we can put the updated grid in
        self.__player.display_board(False, 1)
        self.__player.display_remaining_boats()
        choice = input(
            f"{Fore.BLUE}\nEnter the boat, postion and direction or type help for a list of commands: {Fore.WHITE}"
        ).lower()

        if choice == "continue":
            # continue will exit the recursive function and move onto the game
            if self.__player.unplaced_boats_left():
                print(f"{Fore.BLUE}Placing all remaining boats...{Fore.WHITE}")
                self.__player.auto_place_all()
                time.sleep(2)

            os.system("cls")
            self.__player.display_board(False, 1)
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
            self.__player.auto_place_all()
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
            if not self.__player.place_boat(pos, boat, direction):
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

    def __handle_shot(
        self, is_bot: bool, choice: str
    ) -> bool:  # True if player wins a game
        """Handles the scenario when the opposition fires a shot"""

        player1 = self.__bot if not is_bot else self.__player
        player2 = self.__bot if is_bot else self.__player
        player_num = 2 if is_bot else 1

        outcome = player1.shot_recieved(choice)
        os.system("cls")
        # update players guess grid
        player2.shot_sent(choice, outcome, player_num)
        player2.display_board(True, player_num)
        if outcome == "lost":
            print(
                f"{Fore.GREEN}{'Player' if not is_bot else 'bot'} wins the game!!!{Fore.WHITE}"
            )
            return True
        if is_bot:
            print(f"{Fore.BLUE}\nBOTS turn... It chose {choice} and it...{Fore.WHITE}")
            time.sleep(1)
        print(f"{Fore.BLUE}{outcome}!{Fore.WHITE}")
        return False

    def __players_attack(self) -> None:
        """Where both player and computer choose a position to try to hit their opponent"""

        try:
            # players turn - unique guess required
            os.system("cls")
            self.__player.display_board(True, 1)
            choice = input(
                f"{Fore.BLUE}\nEnter a position to try to shoot your opponents ship: {Fore.WHITE}"
            ).lower()

            if choice == "quit":
                print(f"{Fore.GREEN}Thank you for playing!{Fore.WHITE}")
                return
            elif choice == "reset":
                self._reset_game()
                return

            # Check if the choice is repeated
            if self.__player.is_guess_repeated(choice):
                raise UserError("This guess has already been made")

            # Go to the bots grid to see if it hit, missed or sunk a boat
            if self.__handle_shot(False, choice):
                return
            input("Press enter to start the BOTS turn...")

            # bots turn
            os.system("cls")
            self.__bot.display_board(True, 2)
            # auto guess will be unique to the bots guesses
            choice = self.__bot.auto_guess()
            if self.__handle_shot(True, choice):
                return
            input("Press enter to start your turn again...")

            # recursive until bot or player wins
            self.__players_attack()

        except UserError as e:
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
