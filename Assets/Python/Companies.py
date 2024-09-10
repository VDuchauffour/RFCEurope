# RFC Europe - Companies
# Implemented by AbsintheRed, based on the wonderful idea of embryodead

from CvPythonExtensions import *
from Consts import MessageData
from Core import (
    civilizations,
    get_scenario,
    message,
    human,
    player,
    text,
    turn,
    year,
    cities,
    companies,
)
from LocationsData import CITIES
from PyUtils import rand
from operator import itemgetter
from RFCUtils import getUniqueBuilding
from Events import handler
from MiscData import COMPANY_BUILDINGS
from CoreTypes import (
    Building,
    City,
    Civ,
    Civic,
    Company,
    Province,
    Scenario,
    SpecialParameter,
    Religion,
    Technology,
    Wonder,
)
from StoredData import data

gc = CyGlobalContext()


@handler("GameStart")
def setup():
    # update companies at the beginning of the 1200AD scenario:
    if get_scenario() == Scenario.i1200AD:
        for company in companies:
            if year(1200).between(company.birthdate, company.deathdate):
                addCompany(company.id, 2)


def getCityValue(city, iCompany):
    if city is None:
        return -1
    elif city.isNone():
        return -1

    iValue = 0
    owner = gc.getPlayer(city.getOwner())
    iOwner = owner.getID()
    ownerTeam = gc.getTeam(owner.getTeam())

    # spread the Teutons to Teutonic Order cities and don't spread if the owner civ is at war with the Teutons
    if iCompany == Company.TEUTONS:
        if iOwner == Civ.PRUSSIA:
            iValue += 5
        elif ownerTeam.isAtWar(Civ.PRUSSIA):
            return -1

    # Genoese UP
    if iOwner == Civ.GENOA:
        iValue += 1
        # extra bonus for banking companies
        if iCompany in [Company.MEDICI, Company.AUGSBURG, Company.ST_GEORGE]:
            iValue += 1

    # state religion requirements
    iStateReligion = owner.getStateReligion()
    if iCompany in [Company.HOSPITALLERS, Company.TEMPLARS, Company.TEUTONS]:
        if iStateReligion == Religion.CATHOLICISM:
            iValue += 3
        elif iStateReligion in [Religion.PROTESTANTISM, Religion.ORTHODOXY]:
            iValue -= 2
        else:
            return -1
    elif iCompany == Company.DRAGON:
        if iStateReligion == Religion.CATHOLICISM:
            iValue += 2
        elif iStateReligion == Religion.ORTHODOXY:
            iValue += 1
        elif iStateReligion == Religion.ISLAM:
            return -1
    elif iCompany == Company.CALATRAVA:
        if iStateReligion == Religion.CATHOLICISM:
            iValue += 2
        else:
            return -1
    else:
        if iStateReligion == Religion.ISLAM:
            return -1

    # geographical requirements
    iProvince = city.getProvince()
    if len(companies[iCompany].region) and iProvince not in companies[iCompany].region:
        return -1
    if iCompany == Company.MEDICI:
        if iProvince == Province.TUSCANY:
            iValue += 4
    elif iCompany == Company.AUGSBURG:
        if iProvince == Province.BAVARIA:
            iValue += 3
        elif iProvince == Province.SWABIA:
            iValue += 2
    elif iCompany == Company.ST_GEORGE:
        if iProvince == Province.LIGURIA:
            iValue += 3
    elif iCompany == Company.HANSA:
        if iProvince == Province.HOLSTEIN:
            iValue += 5
        if iProvince in [Province.BRANDENBURG, Province.SAXONY]:
            iValue += 2

    # geographical requirement changes after the Crusades
    iGameTurn = turn()
    if iGameTurn < year(companies[Company.TEMPLARS].deathdate):
        if iCompany in [
            Company.HOSPITALLERS,
            Company.TEMPLARS,
            Company.TEUTONS,
        ]:
            if iStateReligion == Religion.CATHOLICISM:
                if iProvince in [
                    Province.ANTIOCHIA,
                    Province.LEBANON,
                    Province.JERUSALEM,
                ]:
                    iValue += 5
                elif iProvince in [Province.CYPRUS, Province.EGYPT]:
                    iValue += 3
    else:
        if iCompany == Company.HOSPITALLERS:
            if iProvince in [Province.RHODES, Province.MALTA]:
                iValue += 4
        elif iCompany == Company.TEUTONS:
            if iProvince == Province.TRANSYLVANIA:
                iValue += 2

    # bonus for civs whom actively participate (with units) in the actual Crusade:
    if iOwner < civilizations().majors().len():
        if data.players[iOwner].num_crusader_units_sent > 0:
            if iCompany in [
                Company.HOSPITALLERS,
                Company.TEMPLARS,
                Company.TEUTONS,
            ]:
                iValue += 2

    # additional bonus for the city of Jerusalem
    if (city.getX(), city.getY()) == CITIES[City.JERUSALEM]:
        if iCompany in [
            Company.HOSPITALLERS,
            Company.TEMPLARS,
            Company.TEUTONS,
        ]:
            iValue += 3

    # coastal and riverside check
    if iCompany == Company.HANSA:
        if not city.isCoastal(20):  # water body with at least 20 tiles
            if not city.plot().isRiverSide():
                return -1
    elif iCompany == Company.HOSPITALLERS:
        if city.isCoastal(20):
            iValue += 2

    # bonus for religions in the city
    if iCompany in [
        Company.HANSA,
        Company.MEDICI,
        Company.AUGSBURG,
        Company.ST_GEORGE,
    ]:
        if city.isHasReligion(
            Religion.JUDAISM
        ):  # not necessarily historic, but has great gameplay synergies
            iValue += 1
    elif iCompany in [
        Company.HOSPITALLERS,
        Company.TEMPLARS,
        Company.TEUTONS,
        Company.CALATRAVA,
    ]:
        # they have a harder time to choose a city without Catholicism, but they spread the religion there
        if not city.isHasReligion(Religion.CATHOLICISM):
            iValue -= 1
        if city.isHasReligion(Religion.ISLAM):
            iValue -= 1
    elif iCompany == Company.DRAGON:
        if city.isHasReligion(Religion.CATHOLICISM) or city.isHasReligion(Religion.ORTHODOXY):
            iValue += 1
        if city.isHasReligion(Religion.ISLAM):
            iValue -= 1

    # faith points of the population
    if iCompany in [
        Company.HOSPITALLERS,
        Company.TEMPLARS,
        Company.TEUTONS,
        Company.CALATRAVA,
    ]:
        if owner.getFaith() >= 50:
            iValue += 3
        elif owner.getFaith() >= 30:
            iValue += 2
        elif owner.getFaith() >= 15:
            iValue += 1

    # city size
    if iCompany in [
        Company.HANSA,
        Company.DRAGON,
        Company.MEDICI,
        Company.AUGSBURG,
        Company.ST_GEORGE,
    ]:
        if city.getPopulation() > 9:
            iValue += 3
        elif city.getPopulation() > 6:
            iValue += 2
        elif city.getPopulation() > 3:
            iValue += 1

    # Galata Tower bonus: 2 for all cities, additional 2 for the wonder's city
    if owner.getPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER) == 1:
        iValue += 2
        if city.isHasBuilding(Wonder.GALATA_TOWER):
            iValue += 2

    # various building bonuses, trade route bonus
    iBuildCounter = 0  # building bonus counter: we don't want buildings to be the deciding factor in company spread
    if iCompany in [Company.HOSPITALLERS, Company.TEMPLARS, Company.TEUTONS]:
        iMaxPossible = 11  # building bonus counter: we don't want buildings to be the deciding factor in company spread
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.WALLS)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.CASTLE)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.BARRACKS)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.STABLE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.ARCHERY_RANGE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.FORGE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.CATHOLIC_TEMPLE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.CATHOLIC_MONASTERY)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.GUILD_HALL)) > 0:
            iBuildCounter += 1
        iValue += (4 * iBuildCounter) / iMaxPossible  # maximum is 4, with all buildings built
        # wonders should be handled separately
        if city.getNumRealBuilding(Wonder.KRAK_DES_CHEVALIERS) > 0:
            if iCompany == Company.HOSPITALLERS:
                iValue += 5
            else:
                iValue += 2
        if city.getNumRealBuilding(Wonder.DOME_ROCK) > 0:
            if iCompany == Company.TEMPLARS:
                iValue += 5
            else:
                iValue += 2
    elif iCompany == Company.CALATRAVA:
        iMaxPossible = 11  # building bonus counter: we don't want buildings to be the deciding factor in company spread
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.WALLS)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.CASTLE)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.BARRACKS)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.STABLE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.ARCHERY_RANGE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.FORGE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.CATHOLIC_TEMPLE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.CATHOLIC_MONASTERY)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.STAR_FORT)) > 0:
            iBuildCounter += 1
        iValue += (5 * iBuildCounter) / iMaxPossible  # maximum is 5, with all buildings built
    elif iCompany == Company.DRAGON:
        iMaxPossible = 9  # building bonus counter: we don't want buildings to be the deciding factor in company spread
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.WALLS)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.CASTLE)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.BARRACKS)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.STABLE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.ARCHERY_RANGE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.FORGE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.STAR_FORT)) > 0:
            iBuildCounter += 2
        iValue += (5 * iBuildCounter) / iMaxPossible  # maximum is 5, with all buildings built
    elif iCompany in [Company.MEDICI, Company.AUGSBURG, Company.ST_GEORGE]:
        iMaxPossible = 11  # building bonus counter: we don't want buildings to be the deciding factor in company spread
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.MARKET)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.BANK)) > 0:
            iBuildCounter += 3
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.JEWELER)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.GUILD_HALL)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.LUXURY_STORE)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.COURTHOUSE)) > 0:
            iBuildCounter += 2
        iValue += (5 * iBuildCounter) / iMaxPossible  # maximum is 5, with all buildings built
        # wonders should be handled separately
        if city.getNumRealBuilding(Building.PALACE) > 0:
            iValue += 1
        if city.getNumRealBuilding(Building.SUMMER_PALACE) > 0:
            iValue += 1
        # bonus from trade routes
        iValue += max(0, city.getTradeRoutes() - 1)
    elif iCompany == Company.HANSA:
        iMaxPossible = 16  # building bonus counter: we don't want buildings to be the deciding factor in company spread
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.HARBOR)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.LIGHTHOUSE)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.WHARF)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.CUSTOM_HOUSE)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.MARKET)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.BREWERY)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.WEAVER)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.GUILD_HALL)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.WAREHOUSE)) > 0:
            iBuildCounter += 2
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.TANNERY)) > 0:
            iBuildCounter += 1
        if city.getNumRealBuilding(getUniqueBuilding(iOwner, Building.TEXTILE_MILL)) > 0:
            iBuildCounter += 1
        iValue += (6 * iBuildCounter) / iMaxPossible  # maximum is 6, with all buildings built
        # bonus from trade routes
        iValue += city.getTradeRoutes()

    # civic bonuses
    if owner.getCivics(0) == Civic.MERCHANT_REPUBLIC:
        if iCompany in [
            Company.MEDICI,
            Company.ST_GEORGE,
            Company.HOSPITALLERS,
        ]:
            iValue += 1
        elif iCompany == Company.HANSA:
            iValue += 2
    if owner.getCivics(1) == Civic.FEUDAL_LAW:
        if iCompany in [
            Company.HOSPITALLERS,
            Company.TEMPLARS,
            Company.TEUTONS,
            Company.DRAGON,
            Company.CALATRAVA,
        ]:
            iValue += 2
    elif owner.getCivics(1) == Civic.RELIGIOUS_LAW:
        if iCompany in [
            Company.HOSPITALLERS,
            Company.TEMPLARS,
            Company.TEUTONS,
            Company.CALATRAVA,
        ]:
            iValue += 1
    if owner.getCivics(2) == Civic.APPRENTICESHIP:
        if iCompany == Company.HANSA:
            iValue += 1
    if owner.getCivics(3) == Civic.TRADE_ECONOMY:
        if iCompany in [Company.MEDICI, Company.AUGSBURG, Company.ST_GEORGE]:
            iValue += 1
        elif iCompany == Company.HANSA:
            iValue += 2
    elif owner.getCivics(3) == Civic.GUILDS:
        if iCompany in [
            Company.HOSPITALLERS,
            Company.TEMPLARS,
            Company.TEUTONS,
            Company.MEDICI,
            Company.AUGSBURG,
            Company.ST_GEORGE,
            Company.DRAGON,
            Company.CALATRAVA,
        ]:
            iValue += 1
        elif iCompany == Company.HANSA:
            iValue += 2
    elif owner.getCivics(3) == Civic.MERCANTILISM:
        if iCompany == Company.HANSA:
            return -1
        elif iCompany in [
            Company.MEDICI,
            Company.AUGSBURG,
            Company.ST_GEORGE,
        ]:
            iValue -= 2
    if owner.getCivics(4) == Civic.THEOCRACY:
        if iCompany in [Company.HOSPITALLERS, Company.TEMPLARS]:
            iValue += 1
        elif iCompany == Company.TEUTONS:
            iValue += 2
    elif owner.getCivics(4) == Civic.FREE_RELIGION:
        if iCompany in [
            Company.HOSPITALLERS,
            Company.TEMPLARS,
            Company.TEUTONS,
            Company.DRAGON,
        ]:
            iValue -= 1
        elif iCompany == Company.CALATRAVA:
            iValue -= 2
    if owner.getCivics(5) == Civic.OCCUPATION:
        if iCompany in [
            Company.HOSPITALLERS,
            Company.TEMPLARS,
            iCompany,
            iCompany == Company.CALATRAVA,
        ]:
            iValue += 1

    # bonus for techs
    if iCompany in [
        Company.HOSPITALLERS,
        Company.TEMPLARS,
        Company.TEUTONS,
        Company.DRAGON,
        Company.CALATRAVA,
    ]:
        for iTech in [
            Technology.CHIVALRY,
            Technology.PLATE_ARMOR,
            Technology.GUILDS,
            Technology.MILITARY_TRADITION,
        ]:
            if ownerTeam.isHasTech(iTech):
                iValue += 1
    elif iCompany == Company.HANSA:
        for iTech in [
            Technology.GUILDS,
            Technology.CLOCKMAKING,
            Technology.OPTICS,
            Technology.SHIP_BUILDING,
        ]:
            if ownerTeam.isHasTech(iTech):
                iValue += 1
    elif iCompany in [Company.MEDICI, Company.ST_GEORGE]:
        for iTech in [
            Technology.BANKING,
            Technology.PAPER,
            Technology.CLOCKMAKING,
            Technology.OPTICS,
            Technology.SHIP_BUILDING,
        ]:
            if ownerTeam.isHasTech(iTech):
                iValue += 1
    elif iCompany == Company.AUGSBURG:
        for iTech in [
            Technology.BANKING,
            Technology.PAPER,
            Technology.CHEMISTRY,
        ]:
            if ownerTeam.isHasTech(iTech):
                iValue += 1

    # resources
    iTempValue = 0
    bFound = False
    for i in range(5):
        iBonus = gc.getCorporationInfo(iCompany).getPrereqBonus(i)
        if iBonus > -1:
            if city.getNumBonuses(iBonus) > 0:
                bFound = True
                if iCompany in [
                    Company.HOSPITALLERS,
                    Company.TEMPLARS,
                    Company.TEUTONS,
                    Company.DRAGON,
                    Company.CALATRAVA,
                ]:
                    iTempValue += (
                        city.getNumBonuses(iBonus) + 2
                    )  # 3 for the first bonus, 1 for the rest of the same type
                else:
                    iTempValue += (
                        city.getNumBonuses(iBonus) + 1
                    ) * 2  # 4 for the first bonus, 2 for the rest
    if (
        iCompany
        in [
            Company.HANSA,
            Company.MEDICI,
            Company.AUGSBURG,
            Company.ST_GEORGE,
        ]
        and not bFound
    ):
        return -1
    # we don't want the bonus to get too big, and dominate the selection values
    iValue += iTempValue / 4

    # bonus for resources in the fat cross of a city?

    # competition
    if iCompany == Company.HOSPITALLERS:
        if city.isHasCorporation(Company.TEMPLARS):
            iValue *= 2
            iValue /= 3
        if city.isHasCorporation(Company.TEUTONS):
            iValue *= 2
            iValue /= 3
    elif iCompany == Company.TEMPLARS:
        if city.isHasCorporation(Company.HOSPITALLERS):
            iValue *= 2
            iValue /= 3
        if city.isHasCorporation(Company.TEUTONS):
            iValue *= 2
            iValue /= 3
    elif iCompany == Company.TEUTONS:
        if city.isHasCorporation(Company.TEMPLARS):
            iValue *= 2
            iValue /= 3
        if city.isHasCorporation(Company.HOSPITALLERS):
            iValue *= 2
            iValue /= 3
    elif iCompany == Company.MEDICI:
        if city.isHasCorporation(Company.ST_GEORGE) or city.isHasCorporation(Company.AUGSBURG):
            iValue /= 2
    elif iCompany == Company.ST_GEORGE:
        if city.isHasCorporation(Company.MEDICI) or city.isHasCorporation(Company.AUGSBURG):
            iValue /= 2
    elif iCompany == Company.AUGSBURG:
        if city.isHasCorporation(Company.MEDICI) or city.isHasCorporation(Company.ST_GEORGE):
            iValue /= 2

    # threshold
    if iValue < 3:
        return -1

    # spread it out
    iCompOwned = owner.countCorporations(iCompany)
    if city.isHasCorporation(iCompany):
        iValue -= iCompOwned  # -1 per city if the company is already present here (smaller penalty in the value list)
    else:
        iValue -= (
            5 * iCompOwned / 2
        )  # -2,5 per city if it's a possible new spread (bigger penalty in the value list)

    return iValue


def addCompany(iCompany, iNumber):

    # adds the company to the best iNumber cities
    cityValueList = []
    iCompaniesAdded = 0
    for iPlayer in civilizations().majors().ids():
        for city in cities.owner(iPlayer).entities():
            iValue = getCityValue(city, iCompany)
            if iValue > 0:
                cityValueList.append((city, iValue * 10 + rand(10)))
    # sort cities from highest to lowest value
    cityValueList.sort(key=itemgetter(1), reverse=True)
    # spread the company
    for (city, _) in cityValueList:
        if not city.isHasCorporation(iCompany):
            city.setHasCorporation(iCompany, True, True, True)
            city.setHasRealBuilding(COMPANY_BUILDINGS[iCompany], True)
            iCompaniesAdded += 1
            if iCompaniesAdded == iNumber:
                break


@handler("BeginGameTurn")
def checkTurn(iGameTurn):
    # check if it's not too early
    iCompany = iGameTurn % companies.len()
    if iGameTurn < year(companies[iCompany].birthdate):
        return

    # check if it's not too late
    elif iGameTurn > year(companies[iCompany].deathdate) + rand(companies.len()):
        iMaxCompanies = 0
        # do not dissolve the Templars while Jerusalem is under Catholic control
        if iCompany == Company.TEMPLARS:
            plot = gc.getMap().plot(*CITIES[City.JERUSALEM])
            if plot.isCity():
                if (
                    gc.getPlayer(plot.getPlotCity().getOwner()).getStateReligion()
                    == Religion.CATHOLICISM
                ):
                    iMaxCompanies = companies[iCompany].limit

    # set the company limit
    else:
        iMaxCompanies = companies[iCompany].limit

    # modified limit for Hospitallers and Teutons after the Crusades
    if iGameTurn > year(companies[Company.TEMPLARS].deathdate):
        if iCompany == Company.HOSPITALLERS and iGameTurn < year(companies[iCompany].deathdate):
            iMaxCompanies -= 1
        elif iCompany == Company.TEUTONS and iGameTurn < year(companies[iCompany].deathdate):
            iMaxCompanies += 2
    # increased limit for Hansa after their first general Diet in 1356
    if iCompany == Company.HANSA:
        if year(1356) < iGameTurn < year(companies[iCompany].deathdate):
            iMaxCompanies += 3

    # Templars are Teutons are gone after the Protestant reformation
    if iCompany in [Company.TEMPLARS, Company.TEUTONS]:
        if gc.getGame().isReligionFounded(Religion.PROTESTANTISM):
            iMaxCompanies = 0
    # Order of Calatrava is only active if Cordoba or Morocco is alive
    # TODO: Only if Cordoba is alive, or Morocco has some territories in Europe?
    if iCompany == Company.CALATRAVA:
        if not (gc.getPlayer(Civ.CORDOBA).isAlive() or gc.getPlayer(Civ.MOROCCO).isAlive()):
            iMaxCompanies = 0
    # Order of the Dragon is only active if the Ottomans are alive
    if iCompany == Company.DRAGON:
        if not gc.getPlayer(Civ.OTTOMAN).isAlive():
            iMaxCompanies = 0

    # loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
    cityValueList = []
    for iPlayer in civilizations().majors().ids():
        for city in cities.owner(iPlayer).entities():
            iValue = getCityValue(city, iCompany)
            if iValue > 0:
                sCityName = city.getName()
                bPresent = False
                if city.isHasCorporation(iCompany):
                    bPresent = True
                cityValueList.append((city, iValue * 10 + rand(10)))
            elif city.isHasCorporation(
                iCompany
            ):  # remove company from cities with a negative value
                city.setHasCorporation(iCompany, False, True, True)
                city.setHasRealBuilding(COMPANY_BUILDINGS[iCompany], False)
                sCityName = city.getName()
                # interface message for the human player
                announceHuman(iCompany, city, True)

    # sort cities from highest to lowest value
    cityValueList.sort(key=itemgetter(1), reverse=True)

    # count the number of companies
    iCompanyCount = 0
    for civ in civilizations().majors():
        if civ.player.isAlive():
            iCompanyCount += civ.player.countCorporations(iCompany)

    # spread the company
    for i in range(len(cityValueList)):
        city, iValue = cityValueList[i]
        if city.isHasCorporation(iCompany):
            continue
        if (
            i >= iMaxCompanies
        ):  # the goal is to have the company in the first iMaxCompanies number of cities
            break
        city.setHasCorporation(iCompany, True, True, True)
        city.setHasRealBuilding(COMPANY_BUILDINGS[iCompany], True)
        iCompanyCount += 1
        sCityName = city.getName()
        # interface message for the human player
        announceHuman(iCompany, city)
        # spread the religion if it wasn't present before
        if iCompany in [
            Company.HOSPITALLERS,
            Company.TEMPLARS,
            Company.TEUTONS,
            Company.CALATRAVA,
        ]:
            if not city.isHasReligion(Religion.CATHOLICISM):
                city.setHasReligion(Religion.CATHOLICISM, True, True, False)
        # one change at a time, only add the highest ranked city (which didn't have the company before)
        break

    # if the limit was exceeded, remove company from it's worst city
    if iCompanyCount > iMaxCompanies:
        for (city, iValue) in reversed(cityValueList):  # loop backwards in the ordered list
            if city.isHasCorporation(iCompany):
                city.setHasCorporation(iCompany, False, True, True)
                city.setHasRealBuilding(COMPANY_BUILDINGS[iCompany], False)
                sCityName = city.getName()
                # interface message for the human player
                announceHuman(iCompany, city, True)
                # one change at a time, only add the lowest ranked city
                break


@handler("playerChangeStateReligion")
def onPlayerChangeStateReligion(iPlayer, iNewReligion, iOldReligion):
    if iPlayer < civilizations().majors().len():
        for city in cities.owner(iPlayer).entities():
            for iCompany in companies.ids():
                if city.isHasCorporation(iCompany):
                    if getCityValue(city, iCompany) < 0:
                        city.setHasCorporation(iCompany, False, True, True)
                        city.setHasRealBuilding(COMPANY_BUILDINGS[iCompany], False)
                        announceHuman(iCompany, city, True)


@handler("buildingBuilt")
def onBuildingBuilt(city, building_type):
    # Galata Tower ownership
    if city.getOwner() < civilizations().majors().len():
        iPlayer = city.getOwner()
        pPlayer = gc.getPlayer(iPlayer)
        if building_type == Wonder.GALATA_TOWER:
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER, 1)


@handler("cityAcquired")
def onCityAcquired(iOldOwner, iNewOwner, city):

    for iCompany in companies.ids():
        if city.isHasCorporation(iCompany):
            if getCityValue(city, iCompany) < 0:
                city.setHasCorporation(iCompany, False, True, True)
                city.setHasRealBuilding(COMPANY_BUILDINGS[iCompany], False)
                sCityName = city.getName()
                # interface message for the human player
                announceHuman(iCompany, city, True)

    # Galata Tower ownership
    pOldOwner = gc.getPlayer(iOldOwner)
    pNewOwner = gc.getPlayer(iNewOwner)
    if city.isHasBuilding(Wonder.GALATA_TOWER):
        pNewOwner.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER, 1)
        pOldOwner.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER, 0)


@handler("cityRazed")
def onCityRazed(city, iPlayer):
    iPreviousOwner = city.getOwner()
    if iPreviousOwner == iPlayer and city.getPreviousOwner() != -1:
        iPreviousOwner = city.getPreviousOwner()

    # TODO move to Wonders.py?
    # Galata Tower ownership
    pPreviousOwner = gc.getPlayer(iPreviousOwner)
    pPlayer = gc.getPlayer(iPlayer)
    if city.isHasBuilding(Wonder.GALATA_TOWER):
        pPlayer.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER, 0)
        pPreviousOwner.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER, 0)


def announceHuman(iCompany, city, bRemove=False):
    iHuman = human()
    iHumanTeam = gc.getPlayer(iHuman).getTeam()
    if not player().isExisting() or not city.isRevealed(iHumanTeam, False):
        return

    sCityName = city.getName()
    sCompanyName = gc.getCorporationInfo(iCompany).getDescription()

    if bRemove:
        sText = text("TXT_KEY_MISC_CORPORATION_REMOVED", sCompanyName, sCityName)
    else:
        sText = text("TXT_KEY_MISC_CORPORATION_SPREAD", sCompanyName, sCityName)
    message(
        iHuman,
        sText,
        sound=gc.getCorporationInfo(iCompany).getSound(),
        event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
        button=gc.getCorporationInfo(iCompany).getButton(),
        color=MessageData.WHITE,
        location=city,
    )
