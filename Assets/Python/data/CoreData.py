from CivilizationsData import CIV_LEADERS, CIV_PROPERTIES
from CoreStructures import CivilizationsFactory, CompaniesFactory
from LocationsData import COMPANY_REGION
from MiscData import COMPANY_LIMIT
from TimelineData import COMPANY_BIRTHDATE, COMPANY_DEATHDATE


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
    .collect()
)
