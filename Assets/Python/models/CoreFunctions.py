from CoreData import CIVILIZATIONS
from CoreStructures import Civilization
import CoreTypes
from Errors import NotTypeExpectedError

try:
    from CvPythonExtensions import CyGlobalContext, CyPlayer, CyTeam, CyPlot, CyCity, CyUnit

    gc = CyGlobalContext()

except ImportError:
    gc = None


def get_enum_by_id(enum, id):
    """Return a enum member by its index."""
    return enum[enum._member_names_[id]]


def get_civ_by_id(id):
    """Return a Civ member by its index."""
    return get_enum_by_id(CoreTypes.Civ, id)


def get_religion_by_id(id):
    """Return a Religion member by its index."""
    return get_enum_by_id(CoreTypes.Religion, id)


def player(identifier=None):
    """Return CyPlayer object given an identifier."""
    if identifier is None:
        return gc.getActivePlayer()

    if isinstance(identifier, Civilization):
        return identifier.player

    if isinstance(identifier, int):
        return gc.getPlayer(identifier)

    if isinstance(identifier, CyPlayer):
        return identifier

    if isinstance(identifier, CyTeam):
        return gc.getPlayer(identifier.getLeaderID())

    if isinstance(identifier, (CyPlot, CyCity, CyUnit)):
        return gc.getPlayer(identifier.getOwner())

    raise NotTypeExpectedError(
        "CyPlayer, CyTeam, CyPlot, CyCity, CyUnit, or int", type(identifier)
    )


def team(identifier=None):
    """Return CyTeam object given an identifier."""
    if identifier is None:
        return gc.getTeam(gc.getActivePlayer().getTeam())

    if isinstance(identifier, Civilization):
        return identifier.team

    if isinstance(identifier, int):
        return gc.getTeam(gc.getPlayer(identifier).getTeam())

    if isinstance(identifier, CyTeam):
        return identifier

    if isinstance(identifier, (CyPlayer, CyUnit, CyCity, CyPlot)):
        return gc.getTeam(identifier.getTeam())

    raise NotTypeExpectedError(
        "CyPlayer, CyTeam, CyPlot, CyCity, CyUnit, or int", type(identifier)
    )


def civ(identifier=None):
    """Return Civilization object given an identifier."""
    if identifier is None:
        return CIVILIZATIONS[get_civ_by_id(gc.getGame().getActiveCivilizationType())]

    if isinstance(identifier, Civilization):
        return identifier

    if isinstance(identifier, (CyPlayer, CyUnit)):
        return CIVILIZATIONS[get_civ_by_id(identifier.getCivilizationType())]

    if isinstance(identifier, CyPlot):
        if not identifier.isOwned():
            return None
        return civ(identifier.getOwner())

    return CIVILIZATIONS[get_civ_by_id(identifier).getCivilizationType()]


def period(identifier):
    """Return period given an identifier."""
    if identifier >= 0:
        return player(identifier).getPeriod()
    return None
