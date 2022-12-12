DIRECTION = {"up": 1, "right": 2, "down": 3, "left": 4}

LONGEST_BOAT_HEADER_LEN = (
    13  # This is a constant as the boat naming scheme in battleships is constant
)

POSITIONING_HELP_MSG = (
    "- To place/re-place a boat, type 'boat coordinate direction'. E.g. 'carrier e10 up'"
    + "\n- Once you are satisfied with the positions of your boats, type 'continue'"
    + "\n- To auto place all/remaining unplaced boats, type 'continue'"
    + "\n- To see this message again when placing your boats, type 'help'"
    + "\n Press 'enter' to start/continue placing your ships..."
)
