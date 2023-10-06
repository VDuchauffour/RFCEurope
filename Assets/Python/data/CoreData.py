from CoreStructures import CompaniesFactory
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
