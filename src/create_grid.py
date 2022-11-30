from typing import Dict, Tuple

class PlayerGrids:
	"""Class that controls players actions and their grids"""
	
	def __init__(self, x_length: int, y_length: int, boats: Dict) -> None:
		"""Constructor"""

		self.__grid_x = [0] * x_length
		self.__grid_y = [0] * y_length
		self.__player_boats = boats

	def insert_boat(self, pos: Tuple[str,int], boat_len, direction) -> bool:
		"""This adds a boat to the grid and returns a bool to indicate if it was successful"""
		
		x, y = pos
		
		if len(x) != 1:
			# In future we would seperate them further into seperate letters
			return False

		
		x_int = ord(x.upper()) - 65
		if (not (0 <= x_int <= 26)) or (not (x_int <= len(self.__grid_x))):
			# Check if it was an alpha value and if within grid x component
			return False

		if not 1 <= y <= len(self.__grid_y):
			# Check if within grid y component
			return False

		if not (self.__grid_x[x_int] and self.__grid_y[y]):
			# Valid and boat can be placed
			self.__grid_x[x_int] = 1
			self.__grid_y[y - 1] = 1

			return True

		# Boat is already present
		return False
			
	def display_remaining_boats(self) -> None:
		"""Prints the remaining boats to place onto the grid"""
		
		for boat in self.__player_boats:
			print(boat)