# RFC Europe - Companies
# Implemented by AbsintheRed, based on the wonderful idea of embryodead

from CvPythonExtensions import *
from CoreData import CIVILIZATIONS
from CoreData import COMPANIES
from CoreStructures import get_enum_by_id
from LocationsData import CITIES
import PyHelpers
import XMLConsts as xml
import RFCUtils
import Crusades
from operator import itemgetter

from TimelineData import DateTurn
from MiscData import MessageData
from CoreTypes import Building, City, Civ, Company, Province, Scenario, SpecialParameter, Religion

# globals
utils = RFCUtils.RFCUtils()
crus = Crusades.Crusades()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

lCompanyBuilding = [
    xml.iCorporation1,
    xml.iCorporation2,
    xml.iCorporation3,
    xml.iCorporation4,
    xml.iCorporation5,
    xml.iCorporation6,
    xml.iCorporation7,
    xml.iCorporation8,
    xml.iCorporation9,
]


class Companies:
    def setup(self):

        # update companies at the beginning of the 1200AD scenario:
        if utils.getScenario() == Scenario.i1200AD:
            iGameTurn = DateTurn.i1200AD
            for company in COMPANIES:
                if iGameTurn > company.birthdate and iGameTurn < company.deathdate:
                    self.addCompany(company.id, 2)

    def checkTurn(self, iGameTurn):

        # check if it's not too early
        iCompany = iGameTurn % COMPANIES.len()
        if iGameTurn < COMPANIES[iCompany].birthdate:
            return

        # check if it's not too late
        elif iGameTurn > COMPANIES[iCompany].deathdate + gc.getGame().getSorenRandNum(
            COMPANIES.len(), "small randomness with a couple extra turns"
        ):
            iMaxCompanies = 0
            # do not dissolve the Templars while Jerusalem is under Catholic control
            if iCompany == Company.TEMPLARS.value:
                plot = gc.getMap().plot(*CITIES[City.JERUSALEM].to_tuple())
                if plot.isCity():
                    if (
                        gc.getPlayer(plot.getPlotCity().getOwner()).getStateReligion()
                        == Religion.CATHOLICISM.value
                    ):
                        iMaxCompanies = COMPANIES[iCompany].limit

        # set the company limit
        else:
            iMaxCompanies = COMPANIES[iCompany].limit

        # modified limit for Hospitallers and Teutons after the Crusades
        if iGameTurn > COMPANIES[Company.TEMPLARS].deathdate:
            if (
                iCompany == Company.HOSPITALLERS.value
                and iGameTurn < COMPANIES[iCompany].deathdate
            ):
                iMaxCompanies -= 1
            elif iCompany == Company.TEUTONS.value and iGameTurn < COMPANIES[iCompany].deathdate:
                iMaxCompanies += 2
        # increased limit for Hansa after their first general Diet in 1356
        if iCompany == Company.HANSA.value:
            if DateTurn.i1356AD < iGameTurn < COMPANIES[iCompany].deathdate:
                iMaxCompanies += 3

        # Templars are Teutons are gone after the Protestant reformation
        if iCompany in [Company.TEMPLARS.value, Company.TEUTONS.value]:
            if gc.getGame().isReligionFounded(Religion.PROTESTANTISM.value):
                iMaxCompanies = 0
        # Order of Calatrava is only active if Cordoba or Morocco is alive
        # TODO: Only if Cordoba is alive, or Morocco has some territories in Europe?
        if iCompany == Company.CALATRAVA.value:
            if not (
                gc.getPlayer(Civ.CORDOBA.value).isAlive()
                or gc.getPlayer(Civ.MOROCCO.value).isAlive()
            ):
                iMaxCompanies = 0
        # Order of the Dragon is only active if the Ottomans are alive
        if iCompany == Company.DRAGON.value:
            if not gc.getPlayer(Civ.OTTOMAN.value).isAlive():
                iMaxCompanies = 0

        # loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
        cityValueList = []
        for iPlayer in CIVILIZATIONS.majors().ids():
            for city in utils.getCityList(iPlayer):
                iValue = self.getCityValue(city, iCompany)
                if iValue > 0:
                    sCityName = city.getName()
                    bPresent = False
                    if city.isHasCorporation(iCompany):
                        bPresent = True
                    print("Company value:", sCityName, iCompany, iValue, bPresent)
                    cityValueList.append(
                        (city, iValue * 10 + gc.getGame().getSorenRandNum(10, "random bonus"))
                    )
                elif city.isHasCorporation(
                    iCompany
                ):  # remove company from cities with a negative value
                    city.setHasCorporation(iCompany, False, True, True)
                    city.setHasRealBuilding(lCompanyBuilding[iCompany], False)
                    sCityName = city.getName()
                    print("Company removed: ", sCityName, iCompany, iValue)
                    # interface message for the human player
                    self.announceHuman(iCompany, city, True)

        # sort cities from highest to lowest value
        cityValueList.sort(key=itemgetter(1), reverse=True)

        # count the number of companies
        iCompanyCount = 0
        for civ in CIVILIZATIONS.majors():
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
            city.setHasRealBuilding(lCompanyBuilding[iCompany], True)
            iCompanyCount += 1
            sCityName = city.getName()
            print("Company spread: ", sCityName, iCompany, iValue)
            # interface message for the human player
            self.announceHuman(iCompany, city)
            # spread the religion if it wasn't present before
            if iCompany in [
                Company.HOSPITALLERS.value,
                Company.TEMPLARS.value,
                Company.TEUTONS.value,
                Company.CALATRAVA.value,
            ]:
                if not city.isHasReligion(Religion.CATHOLICISM.value):
                    city.setHasReligion(Religion.CATHOLICISM.value, True, True, False)
            # one change at a time, only add the highest ranked city (which didn't have the company before)
            break

        # if the limit was exceeded, remove company from it's worst city
        if iCompanyCount > iMaxCompanies:
            for (city, iValue) in reversed(cityValueList):  # loop backwards in the ordered list
                if city.isHasCorporation(iCompany):
                    city.setHasCorporation(iCompany, False, True, True)
                    city.setHasRealBuilding(lCompanyBuilding[iCompany], False)
                    sCityName = city.getName()
                    print("Company removed: ", sCityName, iCompany, iValue)
                    # interface message for the human player
                    self.announceHuman(iCompany, city, True)
                    # one change at a time, only add the lowest ranked city
                    break

    def onPlayerChangeStateReligion(self, argsList):
        iPlayer, iNewReligion, iOldReligion = argsList

        for city in utils.getCityList(iPlayer):
            for iCompany in COMPANIES.ids():
                if city.isHasCorporation(iCompany):
                    if self.getCityValue(city, iCompany) < 0:
                        city.setHasCorporation(iCompany, False, True, True)
                        city.setHasRealBuilding(lCompanyBuilding[iCompany], False)
                        sCityName = city.getName()
                        print("Company removed on religion change: ", sCityName, iCompany)
                        # interface message for the human player
                        self.announceHuman(iCompany, city, True)

    def onBuildingBuilt(self, iPlayer, iBuilding):

        # Galata Tower ownership
        pPlayer = gc.getPlayer(iPlayer)
        if iBuilding == xml.iGalataTower:
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER.value, 1)

    def onCityAcquired(self, iOldOwner, iNewOwner, city):

        for iCompany in COMPANIES.ids():
            if city.isHasCorporation(iCompany):
                if self.getCityValue(city, iCompany) < 0:
                    city.setHasCorporation(iCompany, False, True, True)
                    city.setHasRealBuilding(lCompanyBuilding[iCompany], False)
                    sCityName = city.getName()
                    print("Company removed on conquest: ", sCityName, iCompany)
                    # interface message for the human player
                    self.announceHuman(iCompany, city, True)

        # Galata Tower ownership
        pOldOwner = gc.getPlayer(iOldOwner)
        pNewOwner = gc.getPlayer(iNewOwner)
        if city.isHasBuilding(xml.iGalataTower):
            pNewOwner.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER.value, 1)
            pOldOwner.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER.value, 0)

    def onCityRazed(self, iOldOwner, iPlayer, city):

        # Galata Tower ownership
        pOldOwner = gc.getPlayer(iOldOwner)
        pPlayer = gc.getPlayer(iPlayer)
        if city.isHasBuilding(xml.iGalataTower):
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER.value, 0)
            pOldOwner.setPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER.value, 0)

    def announceHuman(self, iCompany, city, bRemove=False):
        iHuman = utils.getHumanID()
        iHumanTeam = gc.getPlayer(iHuman).getTeam()
        if not utils.isActive(iHuman) or not city.isRevealed(iHumanTeam, False):
            return

        sCityName = city.getName()
        sCompanyName = gc.getCorporationInfo(iCompany).getDescription()
        iX = city.getX()
        iY = city.getY()

        if bRemove:
            sText = CyTranslator().getText(
                "TXT_KEY_MISC_CORPORATION_REMOVED", (sCompanyName, sCityName)
            )
        else:
            sText = CyTranslator().getText(
                "TXT_KEY_MISC_CORPORATION_SPREAD", (sCompanyName, sCityName)
            )
        CyInterface().addMessage(
            iHuman,
            False,
            MessageData.DURATION,
            sText,
            gc.getCorporationInfo(iCompany).getSound(),
            InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
            gc.getCorporationInfo(iCompany).getButton(),
            ColorTypes(MessageData.WHITE),
            iX,
            iY,
            True,
            True,
        )

    def getCityValue(self, city, iCompany):

        if city is None:
            return -1
        elif city.isNone():
            return -1

        iValue = 0

        owner = gc.getPlayer(city.getOwner())
        iOwner = owner.getID()
        ownerTeam = gc.getTeam(owner.getTeam())

        # spread the Teutons to Teutonic Order cities and don't spread if the owner civ is at war with the Teutons
        if iCompany == Company.TEUTONS.value:
            if iOwner == Civ.PRUSSIA.value:
                iValue += 5
            elif ownerTeam.isAtWar(Civ.PRUSSIA.value):
                return -1

        # Genoese UP
        if iOwner == Civ.GENOA.value:
            iValue += 1
            # extra bonus for banking companies
            if iCompany in [Company.MEDICI.value, Company.AUGSBURG.value, Company.ST_GEORGE.value]:
                iValue += 1

        # state religion requirements
        iStateReligion = owner.getStateReligion()
        if iCompany in [Company.HOSPITALLERS.value, Company.TEMPLARS.value, Company.TEUTONS.value]:
            if iStateReligion == Religion.CATHOLICISM.value:
                iValue += 3
            elif iStateReligion in [Religion.PROTESTANTISM.value, Religion.ORTHODOXY.value]:
                iValue -= 2
            else:
                return -1
        elif iCompany == Company.DRAGON.value:
            if iStateReligion == Religion.CATHOLICISM.value:
                iValue += 2
            elif iStateReligion == Religion.ORTHODOXY.value:
                iValue += 1
            elif iStateReligion == Religion.ISLAM.value:
                return -1
        elif iCompany == Company.CALATRAVA.value:
            if iStateReligion == Religion.CATHOLICISM.value:
                iValue += 2
            else:
                return -1
        else:
            if iStateReligion == Religion.ISLAM.value:
                return -1

        # geographical requirements
        iProvince = city.getProvince()
        if (
            len(COMPANIES[iCompany].region)
            and get_enum_by_id(Province, iProvince) not in COMPANIES[iCompany].region
        ):
            return -1
        if iCompany == Company.MEDICI.value:
            if iProvince == xml.iP_Tuscany:
                iValue += 4
        elif iCompany == Company.AUGSBURG.value:
            if iProvince == xml.iP_Bavaria:
                iValue += 3
            elif iProvince == xml.iP_Swabia:
                iValue += 2
        elif iCompany == Company.ST_GEORGE.value:
            if iProvince == xml.iP_Liguria:
                iValue += 3
        elif iCompany == Company.HANSA.value:
            if iProvince == xml.iP_Holstein:
                iValue += 5
            if iProvince in [xml.iP_Brandenburg, xml.iP_Saxony]:
                iValue += 2

        # geographical requirement changes after the Crusades
        iGameTurn = gc.getGame().getGameTurn()
        if iGameTurn < COMPANIES[Company.TEMPLARS].deathdate:
            if iCompany in [
                Company.HOSPITALLERS.value,
                Company.TEMPLARS.value,
                Company.TEUTONS.value,
            ]:
                if iStateReligion == Religion.CATHOLICISM.value:
                    if iProvince in [xml.iP_Antiochia, xml.iP_Lebanon, xml.iP_Jerusalem]:
                        iValue += 5
                    elif iProvince in [xml.iP_Cyprus, xml.iP_Egypt]:
                        iValue += 3
        else:
            if iCompany == Company.HOSPITALLERS.value:
                if iProvince in [xml.iP_Rhodes, xml.iP_Malta]:
                    iValue += 4
            elif iCompany == Company.TEUTONS.value:
                if iProvince == xml.iP_Transylvania:
                    iValue += 2

        # bonus for civs whom actively participate (with units) in the actual Crusade:
        if iOwner < CIVILIZATIONS.majors().len():
            if crus.getNumUnitsSent(iOwner) > 0:
                if iCompany in [
                    Company.HOSPITALLERS.value,
                    Company.TEMPLARS.value,
                    Company.TEUTONS.value,
                ]:
                    iValue += 2

        # additional bonus for the city of Jerusalem
        if (city.getX(), city.getY()) == CITIES[City.JERUSALEM].to_tuple():
            if iCompany in [
                Company.HOSPITALLERS.value,
                Company.TEMPLARS.value,
                Company.TEUTONS.value,
            ]:
                iValue += 3

        # coastal and riverside check
        if iCompany == Company.HANSA.value:
            if not city.isCoastal(20):  # water body with at least 20 tiles
                if not city.plot().isRiverSide():
                    return -1
        elif iCompany == Company.HOSPITALLERS.value:
            if city.isCoastal(20):
                iValue += 2

        # bonus for religions in the city
        if iCompany in [
            Company.HANSA.value,
            Company.MEDICI.value,
            Company.AUGSBURG.value,
            Company.ST_GEORGE.value,
        ]:
            if city.isHasReligion(
                Religion.JUDAISM.value
            ):  # not necessarily historic, but has great gameplay synergies
                iValue += 1
        elif iCompany in [
            Company.HOSPITALLERS.value,
            Company.TEMPLARS.value,
            Company.TEUTONS.value,
            Company.CALATRAVA.value,
        ]:
            # they have a harder time to choose a city without Catholicism, but they spread the religion there
            if not city.isHasReligion(Religion.CATHOLICISM.value):
                iValue -= 1
            if city.isHasReligion(Religion.ISLAM.value):
                iValue -= 1
        elif iCompany == Company.DRAGON.value:
            if city.isHasReligion(Religion.CATHOLICISM.value) or city.isHasReligion(
                Religion.ORTHODOXY.value
            ):
                iValue += 1
            if city.isHasReligion(Religion.ISLAM.value):
                iValue -= 1

        # faith points of the population
        if iCompany in [
            Company.HOSPITALLERS.value,
            Company.TEMPLARS.value,
            Company.TEUTONS.value,
            Company.CALATRAVA.value,
        ]:
            # print ("faith points:", city.getOwner(), owner.getFaith())
            if owner.getFaith() >= 50:
                iValue += 3
            elif owner.getFaith() >= 30:
                iValue += 2
            elif owner.getFaith() >= 15:
                iValue += 1

        # city size
        if iCompany in [
            Company.HANSA.value,
            Company.DRAGON.value,
            Company.MEDICI.value,
            Company.AUGSBURG.value,
            Company.ST_GEORGE.value,
        ]:
            if city.getPopulation() > 9:
                iValue += 3
            elif city.getPopulation() > 6:
                iValue += 2
            elif city.getPopulation() > 3:
                iValue += 1

        # Galata Tower bonus: 2 for all cities, additional 2 for the wonder's city
        if owner.getPicklefreeParameter(SpecialParameter.HAS_GALATA_TOWER.value) == 1:
            iValue += 2
            if city.isHasBuilding(xml.iGalataTower):
                iValue += 2

        # various building bonuses, trade route bonus
        iBuildCounter = 0  # building bonus counter: we don't want buildings to be the deciding factor in company spread
        if iCompany in [Company.HOSPITALLERS.value, Company.TEMPLARS.value, Company.TEUTONS.value]:
            iMaxPossible = 11  # building bonus counter: we don't want buildings to be the deciding factor in company spread
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWalls)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCastle)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBarracks)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStable)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iArcheryRange)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iForge)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCatholicTemple)) > 0:
                iBuildCounter += 1
            if (
                city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCatholicMonastery))
                > 0
            ):
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iGuildHall)) > 0:
                iBuildCounter += 1
            iValue += (4 * iBuildCounter) / iMaxPossible  # maximum is 4, with all buildings built
            # wonders should be handled separately
            if city.getNumRealBuilding(xml.iKrakDesChevaliers) > 0:
                if iCompany == Company.HOSPITALLERS.value:
                    iValue += 5
                else:
                    iValue += 2
            if city.getNumRealBuilding(xml.iDomeRock) > 0:
                if iCompany == Company.TEMPLARS.value:
                    iValue += 5
                else:
                    iValue += 2
        elif iCompany == Company.CALATRAVA.value:
            iMaxPossible = 11  # building bonus counter: we don't want buildings to be the deciding factor in company spread
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWalls)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCastle)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBarracks)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStable)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iArcheryRange)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iForge)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCatholicTemple)) > 0:
                iBuildCounter += 1
            if (
                city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCatholicMonastery))
                > 0
            ):
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStarFort)) > 0:
                iBuildCounter += 1
            iValue += (5 * iBuildCounter) / iMaxPossible  # maximum is 5, with all buildings built
        elif iCompany == Company.DRAGON.value:
            iMaxPossible = 9  # building bonus counter: we don't want buildings to be the deciding factor in company spread
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWalls)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCastle)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBarracks)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStable)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iArcheryRange)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iForge)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStarFort)) > 0:
                iBuildCounter += 2
            iValue += (5 * iBuildCounter) / iMaxPossible  # maximum is 5, with all buildings built
        elif iCompany in [Company.MEDICI.value, Company.AUGSBURG.value, Company.ST_GEORGE.value]:
            iMaxPossible = 11  # building bonus counter: we don't want buildings to be the deciding factor in company spread
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iMarket)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBank)) > 0:
                iBuildCounter += 3
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iJeweler)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iGuildHall)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iLuxuryStore)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCourthouse)) > 0:
                iBuildCounter += 2
            iValue += (5 * iBuildCounter) / iMaxPossible  # maximum is 5, with all buildings built
            # wonders should be handled separately
            if city.getNumRealBuilding(xml.iPalace) > 0:
                iValue += 1
            if city.getNumRealBuilding(Building.SUMMER_PALACE.value) > 0:
                iValue += 1
            # bonus from trade routes
            iValue += max(0, city.getTradeRoutes() - 1)
        elif iCompany == Company.HANSA.value:
            iMaxPossible = 16  # building bonus counter: we don't want buildings to be the deciding factor in company spread
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iHarbor)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iLighthouse)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWharf)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCustomHouse)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iMarket)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBrewery)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWeaver)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iGuildHall)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWarehouse)) > 0:
                iBuildCounter += 2
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iTannery)) > 0:
                iBuildCounter += 1
            if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iTextileMill)) > 0:
                iBuildCounter += 1
            iValue += (6 * iBuildCounter) / iMaxPossible  # maximum is 6, with all buildings built
            # bonus from trade routes
            iValue += city.getTradeRoutes()

        # civic bonuses
        if owner.getCivics(0) == xml.iCivicMerchantRepublic:
            if iCompany in [
                Company.MEDICI.value,
                Company.ST_GEORGE.value,
                Company.HOSPITALLERS.value,
            ]:
                iValue += 1
            elif iCompany == Company.HANSA.value:
                iValue += 2
        if owner.getCivics(1) == xml.iCivicFeudalLaw:
            if iCompany in [
                Company.HOSPITALLERS.value,
                Company.TEMPLARS.value,
                Company.TEUTONS.value,
                Company.DRAGON.value,
                Company.CALATRAVA.value,
            ]:
                iValue += 2
        elif owner.getCivics(1) == xml.iCivicReligiousLaw:
            if iCompany in [
                Company.HOSPITALLERS.value,
                Company.TEMPLARS.value,
                Company.TEUTONS.value,
                Company.CALATRAVA.value,
            ]:
                iValue += 1
        if owner.getCivics(2) == xml.iCivicApprenticeship:
            if iCompany == Company.HANSA.value:
                iValue += 1
        if owner.getCivics(3) == xml.iCivicTradeEconomy:
            if iCompany in [Company.MEDICI.value, Company.AUGSBURG.value, Company.ST_GEORGE.value]:
                iValue += 1
            elif iCompany == Company.HANSA.value:
                iValue += 2
        elif owner.getCivics(3) == xml.iCivicGuilds:
            if iCompany in [
                Company.HOSPITALLERS.value,
                Company.TEMPLARS.value,
                Company.TEUTONS.value,
                Company.MEDICI.value,
                Company.AUGSBURG.value,
                Company.ST_GEORGE.value,
                Company.DRAGON.value,
                Company.CALATRAVA.value,
            ]:
                iValue += 1
            elif iCompany == Company.HANSA.value:
                iValue += 2
        elif owner.getCivics(3) == xml.iCivicMercantilism:
            if iCompany == Company.HANSA.value:
                return -1
            elif iCompany in [
                Company.MEDICI.value,
                Company.AUGSBURG.value,
                Company.ST_GEORGE.value,
            ]:
                iValue -= 2
        if owner.getCivics(4) == xml.iCivicTheocracy:
            if iCompany in [Company.HOSPITALLERS.value, Company.TEMPLARS.value]:
                iValue += 1
            elif iCompany == Company.TEUTONS.value:
                iValue += 2
        elif owner.getCivics(4) == xml.iCivicFreeReligion:
            if iCompany in [
                Company.HOSPITALLERS.value,
                Company.TEMPLARS.value,
                Company.TEUTONS.value,
                Company.DRAGON.value,
            ]:
                iValue -= 1
            elif iCompany == Company.CALATRAVA.value:
                iValue -= 2
        if owner.getCivics(5) == xml.iCivicOccupation:
            if iCompany in [
                Company.HOSPITALLERS.value,
                Company.TEMPLARS.value,
                iCompany,
                iCompany == Company.CALATRAVA.value,
            ]:
                iValue += 1

        # bonus for techs
        if iCompany in [
            Company.HOSPITALLERS.value,
            Company.TEMPLARS.value,
            Company.TEUTONS.value,
            Company.DRAGON.value,
            Company.CALATRAVA.value,
        ]:
            for iTech in [xml.iChivalry, xml.iPlateArmor, xml.iGuilds, xml.iMilitaryTradition]:
                if ownerTeam.isHasTech(iTech):
                    iValue += 1
        elif iCompany == Company.HANSA.value:
            for iTech in [xml.iGuilds, xml.iClockmaking, xml.iOptics, xml.iShipbuilding]:
                if ownerTeam.isHasTech(iTech):
                    iValue += 1
        elif iCompany in [Company.MEDICI.value, Company.ST_GEORGE.value]:
            for iTech in [
                xml.iBanking,
                xml.iPaper,
                xml.iClockmaking,
                xml.iOptics,
                xml.iShipbuilding,
            ]:
                if ownerTeam.isHasTech(iTech):
                    iValue += 1
        elif iCompany == Company.AUGSBURG.value:
            for iTech in [xml.iBanking, xml.iPaper, xml.iChemistry]:
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
                        Company.HOSPITALLERS.value,
                        Company.TEMPLARS.value,
                        Company.TEUTONS.value,
                        Company.DRAGON.value,
                        Company.CALATRAVA.value,
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
                Company.HANSA.value,
                Company.MEDICI.value,
                Company.AUGSBURG.value,
                Company.ST_GEORGE.value,
            ]
            and not bFound
        ):
            return -1
        # we don't want the bonus to get too big, and dominate the selection values
        iValue += iTempValue / 4

        # bonus for resources in the fat cross of a city?

        # competition
        if iCompany == Company.HOSPITALLERS.value:
            if city.isHasCorporation(Company.TEMPLARS.value):
                iValue *= 2
                iValue /= 3
            if city.isHasCorporation(Company.TEUTONS.value):
                iValue *= 2
                iValue /= 3
        elif iCompany == Company.TEMPLARS.value:
            if city.isHasCorporation(Company.HOSPITALLERS.value):
                iValue *= 2
                iValue /= 3
            if city.isHasCorporation(Company.TEUTONS.value):
                iValue *= 2
                iValue /= 3
        elif iCompany == Company.TEUTONS.value:
            if city.isHasCorporation(Company.TEMPLARS.value):
                iValue *= 2
                iValue /= 3
            if city.isHasCorporation(Company.HOSPITALLERS.value):
                iValue *= 2
                iValue /= 3
        elif iCompany == Company.MEDICI.value:
            if city.isHasCorporation(Company.ST_GEORGE.value) or city.isHasCorporation(
                Company.AUGSBURG.value
            ):
                iValue /= 2
        elif iCompany == Company.ST_GEORGE.value:
            if city.isHasCorporation(Company.MEDICI.value) or city.isHasCorporation(
                Company.AUGSBURG.value
            ):
                iValue /= 2
        elif iCompany == Company.AUGSBURG.value:
            if city.isHasCorporation(Company.MEDICI.value) or city.isHasCorporation(
                Company.ST_GEORGE.value
            ):
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
        if iCompOwned > 0:
            print("Number of companies already present in civ:", city.getName(), iCompOwned)

        return iValue

    def addCompany(self, iCompany, iNumber):

        # adds the company to the best iNumber cities
        cityValueList = []
        iCompaniesAdded = 0
        for iPlayer in CIVILIZATIONS.majors().ids():
            for city in utils.getCityList(iPlayer):
                iValue = self.getCityValue(city, iCompany)
                if iValue > 0:
                    cityValueList.append(
                        (city, iValue * 10 + gc.getGame().getSorenRandNum(10, "random bonus"))
                    )
        # sort cities from highest to lowest value
        cityValueList.sort(key=itemgetter(1), reverse=True)
        # spread the company
        for (city, _) in cityValueList:
            if not city.isHasCorporation(iCompany):
                city.setHasCorporation(iCompany, True, True, True)
                city.setHasRealBuilding(lCompanyBuilding[iCompany], True)
                print("Company added under special circumstance:", city.getName(), iCompany)
                iCompaniesAdded += 1
                if iCompaniesAdded == iNumber:
                    break
