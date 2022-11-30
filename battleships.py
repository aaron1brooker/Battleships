from svc.game_setup import GameSetup
from src.create_grid import PlayerGrids

def start_game():
	"""This will start battleships"""
	game_config = GameSetup()
	board, boats = game_config.get_game_config()

	print(isinstance(board["y"], int))
	player = PlayerGrids(board["x"], board["y"], boats)
	player.display_remaining_boats()
	player.insert_boat(("C",0), 3, "left")
	

start_game()