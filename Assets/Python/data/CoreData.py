from CivilizationsData import (
    CIV_AI_STOP_BIRTH_THRESHOLD,
    CIV_HIRE_MERCENARY_THRESHOLD,
    CIV_INITIAL_CONTACTS,
    CIV_INITIAL_WARS,
    CIV_LEADERS,
    CIV_PROPERTIES,
    CIV_RELIGION_SPREADING_THRESHOLD,
    CIV_RELIGIOUS_TOLERANCE,
    CIV_RESPAWNING_THRESHOLD,
    CIV_STABILITY_AI_BONUS,
    CIV_INITIAL_CONDITION,
)
from CoreStructures import CivilizationsFactory, CompaniesFactory
from LocationsData import (
    CIV_AREAS,
    CIV_CAPITAL_LOCATIONS,
    CIV_HOME_LOCATIONS,
    CIV_NEIGHBOURS,
    CIV_NEW_CAPITAL_LOCATIONS,
    CIV_OLDER_NEIGHBOURS,
    CIV_VISIBLE_AREA,
    COMPANY_REGION,
)
from MiscData import CIV_DAWN_OF_MAN_VALUES, COMPANY_LIMIT
from Scenario import get_scenario
from TimelineData import (
    CIV_BIRTHDATE,
    CIV_COLLAPSE_DATE,
    CIV_RESPAWNING_DATE,
    COMPANY_BIRTHDATE,
    COMPANY_DEATHDATE,
)

CURRENT_SCENARIO = get_scenario()

COMPANIES = (
    CompaniesFactory()
    .attach("birthdate", COMPANY_BIRTHDATE)
    .attach("deathdate", COMPANY_DEATHDATE)
    .attach("region", COMPANY_REGION)
    .attach("limit", COMPANY_LIMIT)
    .collect()
)

CIVILIZATIONS = (
    CivilizationsFactory()
    .add_key("initial", "location", "religion", "ai", "misc", "date")
    .attach("properties", CIV_PROPERTIES)
    .attach("leaders", CIV_LEADERS)
    .attach("condition", CIV_INITIAL_CONDITION[CURRENT_SCENARIO], key="initial")
    .attach("contact", CIV_INITIAL_CONTACTS[CURRENT_SCENARIO], key="initial")
    .attach("wars", CIV_INITIAL_WARS[CURRENT_SCENARIO], key="initial")
    .attach("respawning_threshold", CIV_RESPAWNING_THRESHOLD, key="location")
    .attach("capital", CIV_CAPITAL_LOCATIONS, key="location")
    .attach("new_capital", CIV_NEW_CAPITAL_LOCATIONS, key="location")
    .attach("neighbours", CIV_NEIGHBOURS, key="location")
    .attach("old_neighbours", CIV_OLDER_NEIGHBOURS, key="location")
    .attach("home_colony", CIV_HOME_LOCATIONS, key="location")
    .attach("area", CIV_AREAS, key="location")
    .attach("visible_area", CIV_VISIBLE_AREA[CURRENT_SCENARIO], key="location")
    .attach("spreading_threshold", CIV_RELIGION_SPREADING_THRESHOLD, key="religion")
    .attach("tolerance", CIV_RELIGIOUS_TOLERANCE, key="religion")
    .attach("stop_birth_threshold", CIV_AI_STOP_BIRTH_THRESHOLD, key="ai")
    .attach("stability_bonus", CIV_STABILITY_AI_BONUS, key="ai")
    .attach("hire_mercenary_threshold", CIV_HIRE_MERCENARY_THRESHOLD, key="misc")
    .attach("dawn_of_man", CIV_DAWN_OF_MAN_VALUES, key="misc")
    .attach("birth", CIV_BIRTHDATE, key="date")
    .attach("collapse", CIV_COLLAPSE_DATE, key="date")
    .attach("respawning", CIV_RESPAWNING_DATE, key="date")
    .collect()
)
