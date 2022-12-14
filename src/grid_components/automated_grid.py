import random
import copy

from src.grid_components.player_grid import PlayerGrid
from util.util import GridUtil
from util.constants import DIRECTION


class AutomatedGrid(PlayerGrid):
    """Controls all automated grid components. Child class of PlayerGrid"""

    invert_direction = GridUtil.invert_dictionary(
        DIRECTION
    )  # Makes directions key the value in the new map

    def __auto_place_boat(self, boat: str) -> None:
        """Generates a random position and direction to place a specified boat"""

        rnd_x_int = random.randint(1, self._x_length)
        rnd_x = GridUtil.convert_int_to_x_header(rnd_x_int)
        rnd_y = random.randint(1, self._y_length)

        if not self.place_boat(
            (rnd_x, rnd_y), boat, self.invert_direction[random.randint(1, 4)]
        ):
            self.__auto_place_boat(boat)

    def auto_place_all(self) -> None:
        """Places all boats automatically"""

        players_boats = copy.deepcopy(
            self._unplaced_boats
        )  # Required as self._unplaced_boats will change size

        for boat in players_boats:
            self.__auto_place_boat(boat)

    def is_guess_repeated(self, guess: str) -> bool:
        if guess not in self._guesses:
            self._guesses.append(guess)
            return False
        return True

    def auto_guess(self) -> str:
        """Randomly makes a unique guess"""

        rnd_x_int = random.randint(1, self._x_length)
        rnd_x = GridUtil.convert_int_to_x_header(rnd_x_int)
        rnd_y = random.randint(1, self._y_length)
        guess_str = rnd_x + str(rnd_y)

        if not self.is_guess_repeated(guess_str):
            return guess_str

        return self.auto_guess()

    def reset_grid(self) -> None:
        """This reverts the grid back to its default"""

        # Grab constructor parameters that have not been changed
        x_length = self._x_length
        y_length = self._y_length
        boats = self._boat_to_length

        # Re-construct grid
        self.__init__(x_length, y_length, boats)
