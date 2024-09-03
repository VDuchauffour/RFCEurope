from CoreTypes import Civ


WORLD_WIDTH = 100
WORLD_HEIGHT = 73

# Hardcoded because CyPlayer::isMinorCiv doesn't seems to work when the game starts
INDEPENDENT_CIVS = [Civ.INDEPENDENT, Civ.INDEPENDENT_2, Civ.INDEPENDENT_3, Civ.INDEPENDENT_4]
MINOR_CIVS = INDEPENDENT_CIVS + [Civ.BARBARIAN]

# Used for messages
class MessageData(object):
    DURATION = 14
    WHITE = 0
    RED = 7
    GREEN = 8
    BLUE = 9
    LIGHT_BLUE = 10
    YELLOW = 11
    DARK_PINK = 12
    LIGHT_RED = 20
    PURPLE = 25
    CYAN = 44
    BROWN = 55
    ORANGE = 88
    TAN = 90
    LIME = 100
