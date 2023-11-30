from CoreTypes import Civ


WORLD_WIDTH = 100
WORLD_HEIGHT = 73

# Hardcoded because CyPlayer::isMinorCiv doesn't seems to work when the game starts
INDEPENDENT_CIVS = [
    Civ.INDEPENDENT,
    Civ.INDEPENDENT_2,
    Civ.INDEPENDENT_3,
    Civ.INDEPENDENT_4,
]
MINOR_CIVS = [INDEPENDENT_CIVS] + [
    Civ.BARBARIAN,
]
