from CivilizationsData import (
    CIV_AI_AGGRESSION_LEVEL,
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
    CIV_STARTING_SITUATION,
)
from CoreStructures import CivilizationsFactory, CompaniesFactory
from LocationsData import COMPANY_REGION
from MiscData import COMPANY_LIMIT
from Scenario import get_scenario
from TimelineData import COMPANY_BIRTHDATE, COMPANY_DEATHDATE

CURRENT_SCENARIO = get_scenario()

COMPANIES = (
    CompaniesFactory()
    .attach("birthdate", COMPANY_BIRTHDATE)
    .attach("deathdate", COMPANY_DEATHDATE)
    .attach("region", COMPANY_REGION)
    .attach("limit", COMPANY_LIMIT)
    .collect()
)

# TODO add all remaining CivDataMapper and use RFCUtils getScenario
CIVILIZATIONS = (
    CivilizationsFactory()
    .attach("properties", CIV_PROPERTIES)
    .attach("leaders", CIV_LEADERS)
    .attach("starting_situation", CIV_STARTING_SITUATION[CURRENT_SCENARIO])
    .attach("initial_contact", CIV_INITIAL_CONTACTS[CURRENT_SCENARIO])
    .attach("initial_wars", CIV_INITIAL_WARS[CURRENT_SCENARIO])
    .attach("respawning_threshold", CIV_RESPAWNING_THRESHOLD)
    .attach("religious_tolerance", CIV_RELIGIOUS_TOLERANCE)
    .attach("religion_spreading_threshold", CIV_RELIGION_SPREADING_THRESHOLD)
    .attach("hire_mercenary_threshold", CIV_HIRE_MERCENARY_THRESHOLD)
    .attach("ai_stop_birth_threshold", CIV_AI_STOP_BIRTH_THRESHOLD)
    .attach("ai_aggression_level", CIV_AI_AGGRESSION_LEVEL)
    .attach("ai_stability_ai_bonus", CIV_STABILITY_AI_BONUS)
    .collect()
)
