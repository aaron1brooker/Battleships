import os
import time
from colorama import Fore

from src.grid_components.automated_grid import AutomatedGrid
from util.util import GridUtil
from util.exceptions import UserError


class Traditional_Battleships:
    """Traditional Game Player Vs Computer"""

    def __init__(self, player: AutomatedGrid, bot: AutomatedGrid) -> None:
        """Constructor"""

        self.__player = player
        self.__bot = bot

        # place boats for the computer
        self.__bot.auto_place_all()
        
    def __player_place_boats(self) -> None:
        """Where the player can place their boats on the grid"""

        while self.__player.unplaced_boats_left():
            os.system("cls")  # clears the console so we can put the updated grid in
            self.__player.display_board()
            self.__player.display_remaining_boats()
            choice = input(
                f"{Fore.BLUE}\nEnter the boat, postion and direction. E.g. carrier E1 down: {Fore.WHITE}"
            )
            try:
                boat, pos, direction = GridUtil.seperate_choice(choice)
                if not self.__player.place_boat(pos, boat, direction):
                    print(
                        f"{Fore.RED}It was not possible to position this boat. Please try again{Fore.WHITE}"
                    )
                    time.sleep(1.5)
            except UserError as e:
                print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
                time.sleep(1.5)

        print(f"{Fore.GREEN}All boats have been placed... Lets play!{Fore.WHITE}")
        time.sleep(1.5)
    
    def __players_attack(self) -> None:
        """Where both player and computer choose a position to try to hit their opponent"""

        try:
            # players turn - unique guess required
            choice = input(
                f"{Fore.BLUE}\nEnter a position to try to shoot your opponents ship: {Fore.WHITE}"
            )
            outcome = self.__bot.shots_recieved(choice)
            if outcome == "lost":
                print(f"{Fore.GREEN}Player 1 wins the game!!!{Fore.WHITE}")
                return
            print(outcome)
            time.sleep(1.5)
            os.system("cls")

            # bots turn
            choice = self.__bot.auto_guess()
            print(f"{Fore.BLUE}\nBOTS turn... It chose {choice}{Fore.WHITE}")
            time.sleep(1.5)
            outcome = self.__player.shots_recieved(choice)
            if outcome == "lost":
                print(f"{Fore.GREEN}Bot wins the game!!!{Fore.WHITE}")
                return
            print(outcome)
            time.sleep(1.5)

            # recursive until bot or player wins
            self.__players_attack()
        
        except UserError as e:
            print(f"{Fore.RED}{e}. Please try again{Fore.WHITE}")
            time.sleep(1.5)
            self.__players_attack()
    
    
    def play_game(self) -> None:
        """Starts the Game"""

        self.__player_place_boats()
        self.__players_attack()
