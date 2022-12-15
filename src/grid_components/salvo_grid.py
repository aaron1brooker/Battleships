import logging
from typing import List

from src.grid_components.automated_grid import AutomatedGrid
from util.exceptions import UserError
from util.util import GridUtil


class SalvoGrid(AutomatedGrid):
    """Holds all additional methods required for the salvo variation of the game"""

    def get_boats_left(self) -> int:
        """This returns the number of boats left"""

        return len(self._placed_boats)

    def multi_shots_recieved(self, positions: List[str]) -> List[str]:
        """Handles multiple positions fired and returns the outcome of each shot"""

        outcomes = []

        for pos in positions:
            # Don't allow any repeated guesses
            if self.is_guess_repeated(pos):
                raise UserError(f"{pos} guess has already been made")
            outcomes.append(self.shot_recieved(pos))

        return outcomes

    def multi_shots_sent(
        self, positions: List[str], outcomes: List[str], player: int
    ) -> None:
        """Handles multipe guess so that the user can track them"""

        if len(outcomes) != len(positions):
            error_msg = "Outcomes require to be equal to number of positions entered"
            logging.error(f"{error_msg}. OUTCOMES: {outcomes}. POSITIONS: {positions}")
            raise RuntimeError(
                "Outcomes require to be equal to number of positions entered"
            )

        for ii, pos in enumerate(positions):
            self.shot_sent(pos, outcomes[ii], player)

    def multi_auto_guess(self) -> None:
        """Does an auto guess for each boat the player has left"""

        choices = []
        for _ in range(self.get_boats_left()):
            choices.append(self.auto_guess())

        return " ".join(choices)

    def multi_guess_validation(self, guesses: str) -> List[str]:
        """Returns any guesses that have been repeated or invalid"""

        error_guesses = []
        positions = guesses.split()

        # First see if there are repeated values in the guesses
        if len(set(positions)) != len(positions):
            raise UserError("Each guess requires to be unique")

        for pos in positions:
            # We check if any are repeated
            if pos in self._guesses:
                error_guesses.append(pos)
                continue
            try:
                # Now we see if it matches our regex in position_to_tuple
                pos_tuple = GridUtil.position_to_tuple(pos)
                # See if it is within the grids boundaries
                GridUtil.find_index(pos_tuple, self._x_length, self._y_length)
            except UserError:
                error_guesses.append(pos)

        # Now we know that they are all valid we can add them to guesses
        if len(error_guesses) == 0:
            for pos in positions:
                self._guesses.append(pos)

        return error_guesses
