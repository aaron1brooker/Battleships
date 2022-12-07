import logging
from colorama import Fore
from typing import Dict, Tuple

from util.constants import DIRECTION
from util.exceptions import UserError
from util.util import GridUtil


class PlayerGrid:
    """Class that controls players actions and their grids"""

    def __init__(self, x_length: int, y_length: int, boats: Dict) -> None:
        """Constructor - all protected members"""

        # Game Mechanics related
        self._unplaced_boats = boats
        self._placed_boats = []
        self._guesses = []

        # Grid related
        self._x_length = x_length
        self._y_length = y_length
        self._grid = [0] * x_length * y_length

    def __insert_boat(
        self, pos: Tuple[str, int], boat_len: int, direction: int
    ) -> bool:
        """Inserts the boat into the grid and returns a status boolean if successful"""

        grid_index = GridUtil.find_index(pos, self._x_length, self._y_length)
        if grid_index == 1:
            logging.warning(
                "Cannot place boat. Position is occupied by an object already"
            )
            return False

        _, y = pos
        index_row = y * self._y_length  # Furthest left value in row
        positions = [grid_index]

        for ii in range(boat_len - 1):
            # 'direction_sum' determines how much it needs to move by to place the next 'part'
            # of the ship
            if direction == 1 or direction == 3:
                direction_sum = -self._x_length if direction == 1 else self._x_length
                # Check if it is within the grids dimensions
                if positions[ii] + direction_sum < 0 or positions[
                    ii
                ] + direction_sum > len(self._grid):
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
            if self._grid[positions[ii] + direction_sum] == 1:
                logging.warning(
                    "Cannot place boat. Position is occupied by an object already"
                )
                return False

            positions.append(positions[ii] + direction_sum)

        for position in positions:
            self._grid[position] = 1

        return True

    def place_boat(self, pos: Tuple[str, int], boat: str, direction: str) -> bool:
        """Supplies and executes __insert_boat with boat data and validates direction"""

        direction = DIRECTION.get(direction.lower())
        boat_len = self._unplaced_boats.get(boat.lower())

        if not (direction and boat_len):
            logging.warning(
                f"Unable to place the boat due to provided parameters: {direction} {boat}"
            )
            return False

        if self.__insert_boat(pos, boat_len, direction):
            self._unplaced_boats.pop(boat.lower())
            self._placed_boats.append(boat.lower())
            return True

        # A warning message will have been provided by __insert_boat if it failed
        return False

    def shots_recieved(self, pos: Tuple[str, int]) -> bool:
        """Checks if an oppositions shot has hit the boat and actions accordingly"""

        grid_index = GridUtil.find_index(pos, self._x_length, self._y_length)
        if self._grid[grid_index] == 1:
            return True

        return False

    def boats_left(self) -> bool:
        """Returns true if there are boats still left to be placed onto the grid"""

        if len(self._unplaced_boats) == 0:
            return False

        return True

    def display_remaining_boats(self) -> None:
        """Prints the remaining boats to place onto the grid"""

        for boat in self._unplaced_boats:
            print(Fore.WHITE + boat)

    def display_board(self) -> None:
        """Prints the board in its current state"""

        column_spacing = len(str(self._y_length)) + 1

        x_axis_label = []
        x_axis_label.append(f"{GridUtil.add_spaces('', column_spacing)}|")
        for ii in range(self._x_length):
            # Print x axis labels
            if ii + 65 > 90:
                # For now, we do not allow columns greater than 26
                raise UserError("X axis is not able to exceed for that 26 columns")
            x_axis_label.append(chr(ii + 65))
        print(" ".join(x_axis_label))

        # Print dashes under headers
        x_axis_dashes = []
        x_axis_dashes.append(f"{GridUtil.add_spaces('', column_spacing)}|")
        for ii in range(len(x_axis_label) - len(x_axis_dashes)):
            x_axis_dashes.append("-")
        print(" ".join(x_axis_dashes))

        pos = 0
        for y_label in range(self._y_length):
            row_data = []
            row_data.append(f"{GridUtil.add_spaces(str(y_label + 1), column_spacing)}|")
            for ii in range(self._x_length):
                row_data.append(str(self._grid[pos]))
                pos += 1
            print(" ".join(row_data))
