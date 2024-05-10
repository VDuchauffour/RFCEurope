from CvPythonExtensions import CyGlobalContext
from CoreData import civilizations
from CoreTypes import Civ

gc = CyGlobalContext()

def setup():
    init_player_births()


def init_player_births():
    for civ in civilizations().drop(Civ.BARBARIAN):
        gc.setStartingTurn(civ.id, civ.date.birth)
