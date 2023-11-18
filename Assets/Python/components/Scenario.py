from CoreTypes import Civ, Scenario
from TimelineData import DateTurn


try:
    from CvPythonExtensions import CyGlobalContext

    gc = CyGlobalContext()

except ImportError:
    gc = None


# duplicates with RFCUtils
def get_scenario():
    if gc is not None and gc.getPlayer(Civ.BURGUNDY.value).isPlayable():
        return Scenario.i500AD
    return Scenario.i1200AD


def get_scenario_start_years():
    years = [500, 1200]
    return years[get_scenario()]


def get_scenario_start_turn():
    dateturn = [DateTurn.i500AD, DateTurn.i1200AD]
    return dateturn[get_scenario()]
