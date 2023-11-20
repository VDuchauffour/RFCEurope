from CoreTypes import Civ, Scenario
from TimelineData import DateTurn


try:
    from CvPythonExtensions import CyGlobalContext

    gc = CyGlobalContext()

except ImportError:
    gc = None


def get_scenario():
    """Return scenario given the current situation."""
    if gc is not None and gc.getPlayer(Civ.BURGUNDY.value).isPlayable():
        return Scenario.i500AD
    return Scenario.i1200AD


def get_scenario_start_years(scenario=None):
    """Return scenario start year given a scenario."""
    if scenario is None:
        scenario = get_scenario()

    years = [500, 1200]
    return years[scenario]


def get_scenario_start_turn(scenario=None):
    """Return scenario start turn given a scenario."""
    if scenario is None:
        scenario = get_scenario()

    dateturn = [DateTurn.i500AD, DateTurn.i1200AD]
    return dateturn[scenario]
