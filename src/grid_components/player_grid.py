import logging
import copy
from colorama import Fore
from typing import Dict, Tuple

from util.constants import DIRECTION
from util.exceptions import UserError
from util.util import GridUtil


class PlayerGrid:
    """Parent Class that controls players actions and their grids"""

    def __init__(self, x_length: int, y_length: int, boats: Dict) -> None:
        """Constructor"""

        # Boats related
        self._unplaced_boats = copy.deepcopy(
            boats
        )  # so the boats are independant from other objects
        self._placed_boats = {}
        self._boat_to_length = boats

        # Grid related
        self._x_length = x_length
        self._y_length = y_length
        self._grid = [0] * x_length * y_length

        # Guessing mechanics related
        self._guesses = []
        self._guesses_grid = [0] * x_length * y_length

    def __insert_boat(self, pos: Tuple[str, int], boat: str, direction: int) -> bool:
        """Inserts the boat into the grid and returns a status boolean if successful"""

        boat_len = self._boat_to_length[boat]

        grid_index = GridUtil.find_index(pos, self._x_length, self._y_length)
        if self._grid[grid_index] == 1:
            logging.warning(
                "Cannot place boat. Position is occupied by an object already"
            )
            return False

        _, y = pos
        index_row = (y - 1) * self._x_length  # Furthest left value in row
        positions = [grid_index]

        for ii in range(boat_len - 1):
            # 'direction_sum' determines how much it needs to move by to place the next 'part'
            # of the ship
            if direction == 1 or direction == 3:
                direction_sum = -self._x_length if direction == 1 else self._x_length
                # Check if it is within the grids dimensions
                if positions[ii] + direction_sum < 0 or positions[
                    ii
                ] + direction_sum >= len(self._grid):
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

        # Move boat to placed boats with the coordinates & change grid status
        # Also need to check if it is already there, if so revert old coords to 0

        if boat in self._placed_boats:
            for position in self._placed_boats[boat]:
                self._grid[position] = 0

        self._placed_boats[
            boat
        ] = []  # length of boat is unique so we can use it as a key
        for position in positions:
            self._grid[position] = 1
            self._placed_boats[boat].append(position)

        return True

    def place_boat(self, pos: Tuple[str, int], boat: str, direction: str) -> bool:
        """Supplies and executes __insert_boat with boat data and validates direction"""

        boat = boat.lower()
        direction = DIRECTION.get(direction.lower())
        boat_len = self._boat_to_length.get(boat)

        if not (direction and boat_len):
            logging.warning(
                f"Unable to place the boat due to provided parameters: {direction} {boat}"
            )
            return False

        if self.__insert_boat(pos, boat, direction):
            if boat in self._unplaced_boats:
                self._unplaced_boats.pop(boat)
            return True

        # A warning message will have been provided by __insert_boat if it failed
        return False

    def shot_recieved(self, pos: str) -> str:
        """Checks if an oppositions shot has hit the boat and actions accordingly"""

        pos_tuple = GridUtil.position_to_tuple(pos)
        grid_index = GridUtil.find_index(pos_tuple, self._x_length, self._y_length)

        # Check if this is a position of a boat
        if self._grid[grid_index] == 1:
            # No concerns with complexity here due to the fact that we are
            # dealing with small values of n.
            for boat in self._placed_boats:
                for ii, position in enumerate(self._placed_boats[boat]):
                    if position == grid_index:
                        # position hit belongs to _placed_boats[boat]
                        self._placed_boats[boat].pop(ii)
                        # Check if the boat has sunk
                        if len(self._placed_boats[boat]) == 0:
                            self._placed_boats.pop(boat)
                            # As we have sunk a boat, we want to check if there are still boats left
                            if len(self._placed_boats) == 0:
                                return "lost"
                            return "sunk"
                        return "hit"

        return "missed"

    def shot_sent(self, pos: str, status: str, player: int) -> None:
        """Allows the user to track their guesses"""

        pos_tuple = GridUtil.position_to_tuple(pos)
        grid_index = GridUtil.find_index(pos_tuple, self._x_length, self._y_length)
        if status == "missed":
            self._guesses_grid[grid_index] = "x"
        else:
            self._guesses_grid[grid_index] = 1

    def unplaced_boats_left(self) -> bool:
        """Returns true if there are boats still left to be placed onto the grid"""

        if len(self._unplaced_boats) == 0:
            return False

        return True

    def display_remaining_boats(self) -> None:
        """Prints the remaining boats to place onto the grid"""

        placed_boats_list = [boat for boat in self._placed_boats]
        unplaced_boats_list = [boat for boat in self._unplaced_boats]

        display_rows = GridUtil.structure_all_boats(
            unplaced_boats_list, placed_boats_list
        )

        for rows in display_rows:
            print(rows)

    def display_board(self, is_guess_board: bool, player: int) -> None:
        """Prints the board in its current state"""

        if is_guess_board:
            print(f"{Fore.BLUE}PLAYER {player} GUESSES:{Fore.WHITE}\n")
            board = self._guesses_grid
        else:
            print(f"{Fore.BLUE}PLAYER {player} POSITIONED BOATS:{Fore.WHITE}\n")
            board = self._grid

        column_spacing = len(str(self._y_length)) + 1

        x_axis_label = []
        x_axis_label.append(f"{GridUtil.add_spaces('', column_spacing)}|")
        for ii in range(1, self._x_length + 1):
            # Print x axis labels
            label = GridUtil.convert_int_to_x_header(ii)

            # ensure that each label has a length of 2
            if len(label) == 1:
                label += " "
            x_axis_label.append(label)

        print(Fore.LIGHTMAGENTA_EX + " ".join(x_axis_label) + Fore.WHITE)

        # Print dashes under headers
        x_axis_dashes = []
        x_axis_dashes.append(f"{GridUtil.add_spaces('', column_spacing)}|")
        for ii in range(len(x_axis_label) - len(x_axis_dashes)):
            x_axis_dashes.append("--")
        print(Fore.LIGHTMAGENTA_EX + " ".join(x_axis_dashes) + Fore.WHITE)

        pos = 0
        for y_label in range(self._y_length):
            row_data = []
            row_data.append(
                f"{Fore.LIGHTMAGENTA_EX}{GridUtil.add_spaces(str(y_label + 1), column_spacing)}|{Fore.WHITE}"
            )
            for ii in range(self._x_length):
                if is_guess_board:
                    if board[pos] == 1:
                        colour = Fore.GREEN if player == 1 else Fore.RED
                        row_data.append(f"{colour}{str(board[pos])}{Fore.WHITE} ")
                    elif board[pos] == "x":
                        row_data.append(f"{Fore.BLACK}{board[pos]}{Fore.WHITE} ")
                    else:
                        row_data.append(f"{str(board[pos])} ")
                else:
                    if board[pos] == 1:
                        row_data.append(f"{Fore.GREEN}{str(board[pos])}{Fore.WHITE} ")
                    else:
                        row_data.append(f"{str(board[pos])} ")
                pos += 1

            print(" ".join(row_data))
