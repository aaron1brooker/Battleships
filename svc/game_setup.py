import configparser

class GameSetup:
  def __init__(self):
    # Connect and read the configuration file
    game_config = configparser.ConfigParser()
    game_config.read("game_setup_config.ini")

    # Seperate values to their components
    # if header is not present then the member variable will be an empty dictionary
    self.__board = {} if "BOARD" not in game_config else game_config["BOARD"] # private member
    self.__boats = {} if "BOATS" not in game_config else game_config["BOATS"] # private member



gameSetup = GameSetup()
