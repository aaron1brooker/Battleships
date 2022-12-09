import random
import copy
from typing import Tuple

from src.player_grid import PlayerGrid
from util.constants import INVERT_DIRECTION


class AutomatedGrid(PlayerGrid):
    """Controls all automated grid components. Child class of PlayerGrid"""

    def auto_place_boat(self, boat: str):
        """Generates a random position and direction to place a specified boat"""

        has_placed = False

        while not has_placed:
            rnd_x = chr(random.randint(65, 65 + self._x_length - 1))
            rnd_y = random.randint(1, self._x_length)

            if self.place_boat(
                (rnd_x, rnd_y), boat, INVERT_DIRECTION[random.randint(1, 4)]
            ):
                has_placed = True

    def auto_place_all(self):
        """Places all boats automatically"""

        players_boats = copy.deepcopy(
            self._unplaced_boats
        )  # Required as self._unplaced_boats will change size
        for boat in players_boats:
            self.auto_place_boat(boat)

    def auto_guess(self) -> str:
        """Randomly makes a unique guess"""

        rnd_x = chr(random.randint(65, 65 + self._x_length - 1))
        rnd_y = random.randint(1, self._x_length)
        guess_str = rnd_x + str(rnd_y)

        if guess_str not in self._guesses:
            self._guesses.append(guess_str)
            return guess_str

        return self.auto_guess()
