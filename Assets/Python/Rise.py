from Core import civilizations, get_scenario_start_turn, game, year
from CoreTypes import Civ
import CvScreensInterface
from Events import handler
from Slots import add_player, find_slot
from StoredData import data
from CvPythonExtensions import CyGlobalContext

gc = CyGlobalContext()


@handler("BeginGameTurn")
def showDawnOfMan(iGameTurn):
    if (
        iGameTurn == get_scenario_start_turn()
        and game.getAIAutoPlay() > 0
        and data.before_observer_slot == -1
    ):
        CvScreensInterface.dawnOfMan.interfaceScreen()


@handler("GameStart")
def init_slots():
    data.slots[game.getActiveCivilizationType()] = game.getActivePlayer()
    data.slots[Civ.BARBARIAN.value] = gc.getBARBARIAN_PLAYER()

    for civ in civilizations().independents():
        add_to_slot(civ.id)


@handler("BeginGameTurn")
def set_slot_to_new_civ(gameturn):
    for civ in civilizations().filter(lambda c: year(c.date.birth) == gameturn):
        add_to_slot(civ.id)


def add_to_slot(civ):
    add_player(civ, find_slot(civ))
