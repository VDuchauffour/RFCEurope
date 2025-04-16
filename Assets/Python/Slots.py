from CoreTypes import Civ
from StoredData import data
from Core import player, civilization
from CvPythonExtensions import CyGlobalContext
from PyUtils import next

gc = CyGlobalContext()
NUM_PLAYERS = gc.getMAX_PLAYERS()


def find_slot(iCiv):
    iSlot = next(iSlot for iSlot in range(NUM_PLAYERS) if civilization(iSlot).id == iCiv)
    if iSlot is not None:
        return iSlot

    iSlot = next(
        iSlot for iSlot in range(NUM_PLAYERS) if civilization(iSlot).is_minor()
    )  # not sure that is_minor is releavant because maxPlayer is not minor
    if iSlot is not None:
        return iSlot

    iSlot = next(iSlot for iSlot in range(NUM_PLAYERS) if available_slot(iSlot))
    if iSlot is not None:
        return iSlot

    return -1


def find_minor_slot(iCiv):
    return next(iSlot for iSlot in reversed(range(NUM_PLAYERS)) if civilization(iSlot).is_minor())


def available_slot(iSlot):
    if player(iSlot).isAlive():
        return False

    if player(iSlot).isHuman():
        return False

    if player(iSlot).isMinorCiv():
        return False

    return True


def add_player(iPlayer, iCiv, iBirthTurn=-1, bAlive=False, bMinor=False):
    # game.addPlayer(iPlayer, 0, iCiv, iBirthTurn, bAlive, bMinor)  # TODO when dropping the R&F module
    data.slots[iCiv] = iPlayer


def slot(iCiv):
    if not isinstance(iCiv, Civ):
        raise TypeError("Can only pass Civ to determine slot, got: %s of %s" % (iCiv, type(iCiv)))

    if iCiv in data.slots:
        return data.slots[iCiv]

    return -1
