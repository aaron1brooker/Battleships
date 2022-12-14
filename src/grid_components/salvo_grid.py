import logging
from typing import List

from src.grid_components.automated_grid import AutomatedGrid
from util.exceptions import UserError

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
    
    def multi_shots_sent(self, positions: List[str], outcomes: List[str], player: int) -> None:
        """Handles multipe guess so that the user can track them"""

        if len(outcomes) != len(positions):
            error_msg = "Outcomes require to be equal to number of positions entered"
            logging.error(f"{error_msg}. OUTCOMES: {outcomes}. POSITIONS: {positions}")
            raise RuntimeError("Outcomes require to be equal to number of positions entered")

        for ii, pos in enumerate(positions):
            self.shot_sent(pos, outcomes[ii], player)
    
    def multi_auto_guess(self) -> None:
        choices = []
        for _ in range(self.get_boats_left()):
            choices.append(self.auto_guess())

        return ' '.join(choices)
