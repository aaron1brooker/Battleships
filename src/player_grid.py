import logging
from colorama import Fore
from typing import Dict, Tuple

from util.constants import DIRECTION
from util.exceptions import UserError
from util.util import Util


class PlayerGrid:
    """Class that controls players actions and their grids"""

    def __init__(self, x_length: int, y_length: int, boats: Dict) -> None:
        """Constructor"""

        # protected
        self._player_boats = boats
        self._guesses = []
        self._x_length = x_length
        
        # private
        self.__grid = [0] * x_length * y_length
        self.__y_length = y_length
    
    
    def __insert_boat(
        self, pos: Tuple[str, int], boat_len: int, direction: int
    ) -> bool:
        """Inserts the boat into the grid and returns a status boolean if successful"""

        x, y = pos
        x_int = ord(x.upper()) - 65
        y -= 1

        if not 0 <= x_int < self._x_length:
            logging.warning(f"{x} is not a valid x value")
            return False

        if not 0 <= y < self.__y_length:
            logging.warning(f"{y} is not a valid y value")
            return False

        index_row = y * self.__y_length  # this is the furthest left index of the row
        if self.__grid[index_row + x_int] == 1:
            logging.warning(
                "Cannot place boat. Position is occupied by an object already"
            )
            return False
        positions = [index_row + x_int]

        for ii in range(boat_len - 1):
            # 'direction_sum' determines how much it needs to move by to place the next 'part'
            # of the ship
            if direction == 1 or direction == 3:
                direction_sum = -self._x_length if direction == 1 else self._x_length
                # Check if it is within the grids dimensions
                if positions[ii] + direction_sum < 0 or positions[
                    ii
                ] + direction_sum > len(self.__grid):
                    logging.warning("Out of the grids range")
                    return False
            else:
                # We cam safely assume that only direction 2 and 4 will be passed
                direction_sum = 1 if direction == 2 else -1
                furthest_right_index = index_row + self._x_length - 1

                # Without this check it would go on to the previous/next grid row
                if ((positions[ii] + direction_sum) > furthest_right_index) or (
                    (positions[ii] + direction_sum) < index_row
                ):
                    logging.warning("Out of the grids range")
                    return False

            # Check if position is currently occupied
            if self.__grid[positions[ii] + direction_sum] == 1:
                logging.warning(
                    "Cannot place boat. Position is occupied by an object already"
                )
                return False

            positions.append(positions[ii] + direction_sum)

        for position in positions:
            self.__grid[position] = 1

        return True

    def place_boat(self, pos: Tuple[str, int], boat: str, direction: str) -> bool:
        """Supplies and executes __insert_boat with boat data and validates direction"""

        direction = DIRECTION.get(direction.lower())
        boat_len = self._player_boats.get(boat.lower())

        if not (direction and boat_len):
            logging.warning(
                f"Unable to place the boat due to provided parameters: {direction} {boat}"
            )
            return False

        if self.__insert_boat(pos, boat_len, direction):
            self._player_boats.pop(boat.lower())
            return True

        # A warning message will have been provided by __insert_boat if it failed
        return False


    def boats_left(self) -> bool:
        """Returns true if there are boats still left"""

        if len(self._player_boats) == 0:
            return False

        return True

    def display_remaining_boats(self) -> None:
        """Prints the remaining boats to place onto the grid"""

        for boat in self._player_boats:
            print(Fore.WHITE + boat)

    def display_board(self) -> None:
        """Prints the board in its current state"""

        column_spacing = len(str(self.__y_length)) + 1

        x_axis_label = []
        x_axis_label.append(f"{Util.add_spaces('', column_spacing)}|")
        for ii in range(self._x_length):
            # Print x axis labels
            if ii + 65 > 90:
                # For now, we do not allow columns greater than 26
                raise UserError("X axis is not able to exceed for that 26 columns")
            x_axis_label.append(chr(ii + 65))
        print(" ".join(x_axis_label))

        # Print dashes under headers
        x_axis_dashes = []
        x_axis_dashes.append(f"{Util.add_spaces('', column_spacing)}|")
        for ii in range(len(x_axis_label) - len(x_axis_dashes)):
            x_axis_dashes.append("-")
        print(" ".join(x_axis_dashes))

        pos = 0
        for y_label in range(self.__y_length):
            row_data = []
            row_data.append(f"{Util.add_spaces(str(y_label + 1), column_spacing)}|")
            for ii in range(self._x_length):
                row_data.append(str(self.__grid[pos]))
                pos += 1
            print(" ".join(row_data))
