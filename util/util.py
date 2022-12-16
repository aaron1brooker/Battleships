import logging
import re

from colorama import Fore
from typing import Tuple, List

from util.exceptions import UserError
from util.constants import LONGEST_BOAT_HEADER_LEN


class GridUtil:
    """Holds all helper methods that are utilised through out the program"""

    # Static methods are used to help organise these methods
    @staticmethod
    def add_spaces(value: str, column_length: int) -> str:
        """Adds spaces so that columns align"""

        no_spaces = column_length - len(value)
        spaces = "".join([" "] * no_spaces)
        return value + spaces

    @staticmethod
    def position_to_tuple(pos: str) -> Tuple[str, int]:
        """converts a postion string to a tuple"""

        pattern = "^[A-Za-z]{1,2}[0-9]{1,2}"  # This regex pattern will allow all values that contain
        # one letter & one or two numbers.

        if len(re.findall(pattern, pos)) == 0:  # check if pos has complied with regex
            raise UserError(f"{pos} is not a valid choice")

        x_axis = re.findall("[A-Za-z]", pos)  # seperate x component
        y_axis = re.findall("[0-9]", pos)  # seperate y component
        return ("".join(x_axis), int("".join(y_axis)))

    @staticmethod
    def seperate_choice(choice: str) -> Tuple[str, Tuple[str, str], str]:
        """Seperates users choice into the 3 components (boat, position and direction)"""

        choice_components = choice.split()

        if len(choice_components) != 3:
            raise UserError(
                f"Exactly 3 options can be provided - {len(choice_components)} choices were given"
            )

        return (
            choice_components[0],
            GridUtil.position_to_tuple(choice_components[1]),
            choice_components[2],
        )

    @staticmethod
    def invert_dictionary(dictionary):
        """Flips a dictionary so that the key is now the value and vice versa"""

        return dict((v, k) for k, v in dictionary.items())

    @staticmethod
    def find_index(pos: Tuple[str, int], x_length: int, y_length: int) -> int:
        """Finds the indexs of where the position is held in the grids array"""

        x, y = pos
        x = x.upper()
        y -= 1

        position_values = []
        for letter in x:
            letter_int = ord(letter) - 64
            position_values.append(letter_int)

        if len(position_values) == 1:
            x_int = position_values[0]
        else:
            sum = 26
            for ii in range(len(position_values) - 1):
                sum *= position_values[ii]
            x_int = sum + position_values[len(position_values) - 1]

        x_int -= 1

        if not 0 <= x_int < x_length:
            logging.error(f"{x} is not a valid x value")
            raise UserError("Not a valid x value")

        if not 0 <= y < y_length:
            logging.error(f"{y} is not a valid y value")
            raise UserError("Not a valid y value")

        return (y * x_length) + x_int
    
    @staticmethod
    def index_to_position(index: int, x_length) -> str:
        """Converts the index of the array into a board position"""

        x = 0
        y = 0
        while (index - x_length) > 0:
            index -= x_length
            y += 1
        
        x = index
        return chr(x + 65) + str(y + 1)
    
    @staticmethod
    def structure_all_boats(
        unplaced_boats: List[str], placed_boats: List[str]
    ) -> List[str]:
        """Structures the boats in a format so that they can be displayed"""

        display_rows = [
            Fore.GREEN
            + GridUtil.add_spaces("Placed Boats:", LONGEST_BOAT_HEADER_LEN + 1)
            + Fore.RED
            + "Unplaced Boats:"
        ]  # This is what the user will see
        placed_boats_len = len(placed_boats)
        unplaced_boats_len = len(unplaced_boats)

        # Find out greater List & workout the difference
        is_placed_greater = True if placed_boats_len > unplaced_boats_len else False
        if is_placed_greater:
            diff = placed_boats_len - unplaced_boats_len
        else:
            diff = unplaced_boats_len - placed_boats_len

        # Place populated values side by side
        for ii in range(unplaced_boats_len if is_placed_greater else placed_boats_len):
            display_row = Fore.GREEN + GridUtil.add_spaces(
                placed_boats[ii], LONGEST_BOAT_HEADER_LEN + 1
            )
            display_row += Fore.RED + unplaced_boats[ii]

            display_rows.append(display_row)

        # Place the rest of the boats next to an empty string
        if is_placed_greater:
            for ii in range(placed_boats_len - diff, placed_boats_len):
                display_rows.append(
                    Fore.GREEN
                    + GridUtil.add_spaces(placed_boats[ii], LONGEST_BOAT_HEADER_LEN + 1)
                )
            return display_rows

        for ii in range(unplaced_boats_len - diff, unplaced_boats_len):
            display_row = GridUtil.add_spaces("", LONGEST_BOAT_HEADER_LEN + 1)
            display_row += Fore.RED + unplaced_boats[ii]

            display_rows.append(display_row)
        return display_rows

    @staticmethod
    def convert_int_to_x_header(value: int) -> str:
        """Converts an integer to the appropriate header value. E.g. 1 = A"""

        value_div = value // 26
        value_remainder = value % 26

        if value_remainder == 0:
            if value_div == 1:
                return "Z"  # 26th letter in alphabet is Z
            # As 26 equally goes into value we know it is a letter + Z
            # Also, it is still apart of previous set so we minus 1
            return str(chr(value_div - 1 + 64)) + "Z"
        if value_div == 0:
            return str(chr(value_remainder + 64))
        return str(chr(value_div + 64)) + str(chr(value_remainder + 64))
