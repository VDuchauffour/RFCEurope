from CoreStructures import player
from CoreTypes import Civ, Scenario
from TimelineData import DateTurn


def get_scenario():
    """Return scenario given the current situation."""
    try:
        if player(Civ.BURGUNDY).isPlayable():
            return Scenario.i500AD
    except:  # noqa: E722
        return Scenario.i1200AD
    else:
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
