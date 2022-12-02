import configparser
import logging
from typing import Tuple, Dict

from util.exceptions import UserError


class GameSetup:
    """Manages the data in the configuration file"""

    def __init__(self) -> None:
        """Contructor"""

        # Connect and read the configuration file
        game_config = configparser.ConfigParser()
        game_config.read("./svc/game_setup_config.ini")  # relative to main directory
        # Seperate values to their components
        # if header is not present then the member variable will be an empty dictionary
        self.__board = (
            {} if "BOARD" not in game_config else game_config["BOARD"]
        )  # private member

        self.__boats = (
            {} if "BOATS" not in game_config else game_config["BOATS"]
        )  # private member

    def __validate_and_parse_board(self) -> Tuple[bool, Dict]:
        """Validates and parses the board configuration values"""

        try:
            x = None if "x" not in self.__board else int(self.__board["x"])
            y = None if "y" not in self.__board else int(self.__board["y"])
        except ValueError:
            # an integer is not inputed within the fields
            logging.warning("An integer was not provide for the boards size")
            return False, {}

        if (not (x or y)) or (not ((5 <= x <= 80) and (5 <= y <= 80))):
            # x/y needs to be present in the config file
            # x/y needs to be greater/equal to 5 and smaller/equal to 80
            # if it fails to comply with these rules then a UserError will be raised
            logging.warning(
                f"Board size is not in the valid range between 5 - 80. x: {x}, y: {y}"
            )
            return False, {}

        return True, {"x": x, "y": y}

    def __validate_and_parse_boats(self) -> Tuple[bool, Dict]:
        """Validates and parses the boats configuration values"""

        boats = {}
        for boat in self.__boats:
            try:
                boat_length = int(self.__boats[boat])
                boats[boat] = boat_length
            except ValueError:
                # an integer is not inputed for size of boat
                logging.warning("An integer was not provide for the boat size")
                return False, {}

        return True, boats

    def get_game_config(self) -> Tuple[Dict[str, int], Dict[str, int]]:
        """Returns back valid game configuration values"""

        is_valid_board, board = self.__validate_and_parse_board()
        is_valid_boat, boats = self.__validate_and_parse_boats()

        if is_valid_board and is_valid_boat:
            return board, boats

        # We raise a UserError as the dimensions will be controlled by the user
        raise UserError("Grid size is not valid")
