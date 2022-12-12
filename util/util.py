import logging
import re

from typing import Tuple, List

from util.exceptions import UserError


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

        pattern = "^[A-Za-z][0-9]{1,2}"  # This regex pattern will allow all values that contain
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
        x_int = ord(x.upper()) - 65
        y -= 1

        if not 0 <= x_int < x_length:
            logging.error(f"{x} is not a valid x value")
            raise UserError("Not a valid x value")

        if not 0 <= y < y_length:
            logging.error(f"{y} is not a valid y value")
            raise UserError("Not a valid y value")

        return (y * y_length) + x_int
    
