import re

from typing import Tuple

from util.exceptions import UserError


class Util:
    """Holds all helper methods that are utilised through out the program"""

    # Static methods are used to help organise these methods
    @staticmethod
    def add_spaces(value: str, column_length: int) -> str:
        no_spaces = column_length - len(value)
        spaces = "".join([" "] * no_spaces)
        return value + spaces

    @staticmethod
    def seperate_choice(choice: str) -> Tuple[str, Tuple[str, str], str]:
        pattern = "^[A-Za-z][0-9]{1,2}"  # This regex pattern will allow all values that contain
        # one letter & one or two numbers.

        choice_components = choice.split()

        if len(choice_components) != 3:
            raise UserError(
                f"Exactly 3 options can be provided - {len(choice_components)} choices were given"
            )

        if (
            len(re.findall(pattern, choice_components[1])) == 0
        ):  # check if pos has complied with regex
            raise UserError(f"{choice_components[1]} is not a valid choice")

        x_axis = re.findall("[A-Za-z]", choice_components[1])  # seperate x component
        y_axis = re.findall("[0-9]", choice_components[1])  # seperate y component
        pos = ("".join(x_axis), int("".join(y_axis)))

        return choice_components[0], pos, choice_components[2]
    
    @staticmethod
    def invert_dictionary(dictionary):
        return dict((v,k) for k,v in dictionary.items())