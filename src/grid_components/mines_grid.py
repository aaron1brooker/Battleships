import random

from typing import Tuple, List, Dict

from src.grid_components.automated_grid import AutomatedGrid
from util.exceptions import UserError
from util.util import GridUtil

class MinesGrid(AutomatedGrid):
    """Hold the components related to the Hidden Mines Battleships game"""

    def __init__(self, x_length: int, y_length: int, boats: Dict) -> None:
        super().__init__(x_length, y_length, boats)
        self._mine_index_positions = []
    
    def auto_place_mines(self) -> None:
        """Places mines randomly on a players grid"""

        for _ in range(5):
            # Require 5 mines
            is_valid = False

            while not is_valid:
                rnd_index = random.randint(0, len(self._grid) -1)
                if self._grid[rnd_index] == 0:
                    self._grid[rnd_index] = "m"
                    self._mine_index_positions.append(rnd_index)
                    is_valid = True

        print(self._mine_index_positions)
    
    
    def __shot_hit_mine(self, pos_tuple: Tuple[str, int]) -> List[str]:
        """Workouts out which positions will be effected and the outcome of them"""

        x, y = pos_tuple
        operations = [0, 1, -1]
        positions = []

        # Calculate potential positions that surround the mine
        # This may include invalid positions to start with
        for y_operation in operations:
            y += y_operation
            for x_operation in operations:
                new_letter_int = ord(x) + x_operation
                positions.append(GridUtil.convert_int_to_x_header(new_letter_int) + str(y))
        
        # Now we want to validate the positions to see if they are correct
        for ii, position in enumerate(positions):
            # if invalid then we remove it from the list
            try:
                pos_tuple = GridUtil.position_to_tuple(position)
                grid_index = GridUtil.find_index(pos_tuple, self._x_length, self._y_length)
                # Has is hit another mine? if yes we do the process again
                if grid_index in self._guesses:
                    self._guesses.remove(grid_index)
                    mine_position_list = self.__shot_hit_mine(pos_tuple)
                    positions.extend(mine_position_list)
                
            except UserError:
                positions.pop(ii)
            
        return set(positions) # So there are no duplicates
    
    def __shot_recieved(self, pos: str) -> str:
        """An extensions to PlayerGrid method shot_recieved"""

        pos_tuple = GridUtil.position_to_tuple(pos)
        grid_index = GridUtil.find_index(pos_tuple, self._x_length, self._y_length)

        if self._grid[grid_index] == "m":
            return "mine"
        
        return self.shot_recieved(pos)


    def shot_recieved_mine(self, pos: str) -> Dict[str,str]:
        """Checks if the opposition has hit a mine"""

        outcomes = {"mine": [],"hit": [], "missed": [], "sunk": [], "lost": []}
        pos_tuple = GridUtil.position_to_tuple(pos)
        grid_index = GridUtil.find_index(pos_tuple, self._x_length, self._y_length)

        if grid_index in self._mine_index_positions:
            self._guesses.remove(grid_index)
            valid_positions = self.__shot_hit_mine(pos_tuple, grid_index)
            for valid_position in valid_positions:
                outcomes[self.__shot_recieved(valid_position)].append(valid_position)
            return outcomes
        else:
            outcomes[self.shot_recieved(pos)].append(pos)
            return outcomes
