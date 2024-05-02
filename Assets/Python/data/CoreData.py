from CivilizationsData import (
    CIV_ADDITIONAL_UNITS,
    CIV_AI_MODIFIERS,
    CIV_AI_REFORMATION_THRESHOLD,
    CIV_AI_STOP_BIRTH_THRESHOLD,
    CIV_HIRE_MERCENARY_THRESHOLD,
    CIV_INITIAL_BUILDINGS,
    CIV_INITIAL_CONTACTS,
    CIV_INITIAL_TECH,
    CIV_INITIAL_UNITS,
    CIV_INITIAL_WARS,
    CIV_INITIAL_WORKERS,
    CIV_LEADERS,
    CIV_HUMAN_MODIFIERS,
    CIV_RELIGION_SPREADING_THRESHOLD,
    CIV_RELIGIOUS_TOLERANCE,
    CIV_RESPAWNING_THRESHOLD,
    CIV_STABILITY_AI_BONUS,
    CIV_SCENARIO_CONDITION,
)
from CoreFunctions import get_civ_by_id
from CoreStructures import Civilization, CivilizationsFactory, CompaniesFactory
from CoreTypes import Scenario, Civ
from Errors import NotTypeExpectedError
from LocationsData import (
    CIV_AREAS,
    CIV_CAPITAL_LOCATIONS,
    CIV_EVENT_DRIVE_PROVINCES,
    CIV_HOME_LOCATIONS,
    CIV_NEIGHBOURS,
    CIV_NEW_CAPITAL_LOCATIONS,
    CIV_PROVINCES,
    CIV_REFORMATION_NEIGHBOURS,
    CIV_VISIBLE_AREA,
    COMPANY_REGION,
)
from MiscData import COMPANY_LIMIT
from Scenario import get_scenario
from TimelineData import (
    CIV_BIRTHDATE,
    CIV_COLLAPSE_DATE,
    CIV_RESPAWNING_DATE,
    COMPANY_BIRTHDATE,
    COMPANY_DEATHDATE,
)

try:
    from CvPythonExtensions import CyGlobalContext, CyPlayer, CyPlot, CyUnit, CyCity

    gc = CyGlobalContext()

except ImportError:
    gc = None


COMPANIES = (
    CompaniesFactory()
    .attach("birthdate", COMPANY_BIRTHDATE)
    .attach("deathdate", COMPANY_DEATHDATE)
    .attach("region", COMPANY_REGION)
    .attach("limit", COMPANY_LIMIT)
    .collect()
)

CIVILIZATIONS_BASE = (
    CivilizationsFactory()
    .add_key("initial", "location", "religion", "human", "ai", "misc", "date", "event", "scenario")
    .attach("leaders", CIV_LEADERS)
    .attach("respawning_threshold", CIV_RESPAWNING_THRESHOLD, key="location")
    .attach("capital", CIV_CAPITAL_LOCATIONS, key="location")
    .attach("new_capital", CIV_NEW_CAPITAL_LOCATIONS, key="location")
    .attach("neighbours", CIV_NEIGHBOURS, key="location")
    .attach("reformation_neighbours", CIV_REFORMATION_NEIGHBOURS, key="location")
    .attach("home_colony", CIV_HOME_LOCATIONS, key="location")
    .attach("provinces", CIV_PROVINCES, key="location")
    .attach("area", CIV_AREAS, key="location")
    .attach("spreading_threshold", CIV_RELIGION_SPREADING_THRESHOLD, key="religion")
    .attach("tolerance", CIV_RELIGIOUS_TOLERANCE, key="religion")
    .attach("modifiers", CIV_HUMAN_MODIFIERS, key="human")
    .attach("modifiers", CIV_AI_MODIFIERS, key="ai")
    .attach("stop_birth_threshold", CIV_AI_STOP_BIRTH_THRESHOLD, key="ai")
    .attach("stability_bonus", CIV_STABILITY_AI_BONUS, key="ai")
    .attach("reformation_threshold", CIV_AI_REFORMATION_THRESHOLD, key="ai")
    .attach("hire_mercenary_threshold", CIV_HIRE_MERCENARY_THRESHOLD, key="misc")
    .attach("birth", CIV_BIRTHDATE, key="date")
    .attach("collapse", CIV_COLLAPSE_DATE, key="date")
    .attach("respawning", CIV_RESPAWNING_DATE, key="date")
    .attach("buildings", CIV_INITIAL_BUILDINGS, key="initial")
    .attach("tech", CIV_INITIAL_TECH, key="initial")
    .attach("workers", CIV_INITIAL_WORKERS, key="initial")
    .attach("units", CIV_INITIAL_UNITS, key="initial")
    .attach("additional_units", CIV_ADDITIONAL_UNITS, key="initial")
    .attach("provinces", CIV_EVENT_DRIVE_PROVINCES, key="event")
)

CIVILIZATIONS_500AD = (
    CIVILIZATIONS_BASE.attach("visible_area", CIV_VISIBLE_AREA[Scenario.i500AD], key="location")
    .attach("condition", CIV_SCENARIO_CONDITION[Scenario.i500AD], key="scenario")
    .attach("contact", CIV_INITIAL_CONTACTS[Scenario.i500AD], key="scenario")
    .attach("wars", CIV_INITIAL_WARS[Scenario.i500AD], key="scenario")
    .collect()
)

CIVILIZATIONS_1200AD = (
    CIVILIZATIONS_BASE.attach("visible_area", CIV_VISIBLE_AREA[Scenario.i1200AD], key="location")
    .attach("condition", CIV_SCENARIO_CONDITION[Scenario.i1200AD], key="scenario")
    .attach("contact", CIV_INITIAL_CONTACTS[Scenario.i1200AD], key="scenario")
    .attach("wars", CIV_INITIAL_WARS[Scenario.i1200AD], key="scenario")
    .collect()
)


def civilizations(scenario=None):
    """Return civilizations data given a scenario."""
    if scenario is None:
        scenario = get_scenario()

    data_mapper = {Scenario.i500AD: CIVILIZATIONS_500AD, Scenario.i1200AD: CIVILIZATIONS_1200AD}
    return data_mapper[scenario]


def civilization(identifier=None):
    """Return Civilization object given an identifier."""
    if identifier is None:
        return civilizations()[get_civ_by_id(gc.getGame().getActiveCivilizationType())]

    if isinstance(identifier, int):
        return civilizations()[identifier]

    if isinstance(identifier, Civ):
        return civilizations()[identifier]

    if isinstance(identifier, Civilization):
        return civilizations()[identifier.id]

    if isinstance(identifier, (CyPlayer, CyUnit)):
        return civilizations()[get_civ_by_id(identifier.getCivilizationType())]

    if isinstance(identifier, CyPlot):
        if not identifier.isOwned():
            return None
        return civilizations()[identifier.getOwner()]

    if isinstance(identifier, CyCity):
        return civilizations()[identifier.getOwner()]

    raise NotTypeExpectedError(
        "CoreTypes.Civ, Civilization, CyPlayer, CyPlot, CyCity or CyUnit, or int", type(identifier)
    )
