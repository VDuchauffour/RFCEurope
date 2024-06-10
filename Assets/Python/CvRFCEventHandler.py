# Rhye's and Fall of Civilization: Europe - Event handler

from CvPythonExtensions import *
from CoreData import civilizations, civilization
from Core import message, human, make_unit, make_units, player, show, text, turn, year, cities
import CvUtil
import CvEventManager
import PyHelpers
import CvMercenaryManager  # Mercenaries
import CvScreenEnums  # Mercenaries
from PyUtils import rand, percentage_chance

from StoredData import data
import RiseAndFall
import Barbs
import Religions
import Resources
import CityNameManager
import UniquePowers
import AIWars
from RFCUtils import (
    forcedInvasion,
    getProvinceStabilityLevel,
    spreadMajorCulture,
    getUniqueBuilding,
)

import Victory
import Stability
import Plague
import Crusades
import Companies
import Locations
import Modifiers
import Provinces
import Civilizations
import Mercenaries

from Scenario import get_scenario
from Consts import MessageData
from ProvinceMapData import PROVINCES_MAP
from CoreTypes import (
    Building,
    Civ,
    City,
    Improvement,
    Religion,
    Scenario,
    UniquePower,
    StabilityCategory,
    Technology,
    Unit,
    Wonder,
)
from LocationsData import CITIES

gc = CyGlobalContext()

# Absinthe: Turn Randomization constants
iLighthouseEarthQuake = 0
iByzantiumVikingAttack = 1

# Absinthe: all of this Mercenary stuff is unused
# Mercenaries - start

PyGame = PyHelpers.PyGame()
PyInfo = PyHelpers.PyInfo

# Set g_bGameTurnMercenaryCreation to True if mercenary creation should happen during the
# onBeginGameTurn method, False if it should happen during the onBeginPlayerTurn method
# Default value is True
g_bGameTurnMercenaryCreation = True

# Set g_bDisplayMercenaryManagerOnBeginPlayerTurn to True if the "Mercenary Manager"
# screen should be displayed at the beginning of every player turn.
# Default value is False
g_bDisplayMercenaryManagerOnBeginPlayerTurn = False

# This value also controls the "Mercenary Manager" button and when it should be displayed.
# Default value is "ERA_ANCIENT"
# Rhye - start (was causing an assert)
# g_iStartingEra = gc.getInfoTypeForString("ERA_ANCIENT")
g_iStartingEra = 0
# Rhye - end

# Change this to False if mercenaries should be removed from the global mercenary pool
# at the beginning of the game turn. When set to True a number of mercenaries will
# wander away from the global mercenary pool. This is another variable used to control
# the load time for the "Mercenary Manager" screen.
# Default valus is True
g_bWanderlustMercenaries = True

# Change this to increase the max number of mercenaries that may wander away from the
# global mercenary pool.
# Default valus is 3
g_iWanderlustMercenariesMaximum = 7  # Rhye

# Default valus is 0
g_iWanderlustMercenariesMinimum = 2  # Rhye

# Change this to False to supress the mercenary messages.
# Default value is True
g_bDisplayMercenaryMessages = False  # Rhye

# Set to True to print out debug messages in the logs
g_bDebug = True

# Default valus is 1
g_bUpdatePeriod = 5  # Rhye

# Default valus is 1
g_bAIThinkPeriod = 6  # Rhye (5 in Warlords, 4 in vanilla)

# globals

# Mercenaries - end


class CvRFCEventHandler:

    mercenaryManager = None  # Mercenaries

    def __init__(self, eventManager):

        self.lastProvinceID = -1
        self.bStabilityOverlay = False
        self.EventKeyDown = 6
        self.EventKeyUp = 7
        self.eventManager = eventManager

        # initialize base class
        eventManager.addEventHandler("GameStart", self.onGameStart)  # Stability
        eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn)  # Stability
        eventManager.addEventHandler("cityAcquired", self.onCityAcquired)  # Stability
        eventManager.addEventHandler(
            "cityAcquiredAndKept", self.onCityAcquiredAndKept
        )  # Stability
        eventManager.addEventHandler("cityRazed", self.onCityRazed)  # Stability
        eventManager.addEventHandler("cityBuilt", self.onCityBuilt)  # Stability
        eventManager.addEventHandler("combatResult", self.onCombatResult)  # Stability
        # eventManager.addEventHandler("changeWar", self.onChangeWar)
        eventManager.addEventHandler("religionFounded", self.onReligionFounded)  # Victory
        eventManager.addEventHandler("buildingBuilt", self.onBuildingBuilt)  # Victory
        eventManager.addEventHandler("projectBuilt", self.onProjectBuilt)  # Victory
        eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)  # Mercenaries
        # eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
        eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)  # Stability
        eventManager.addEventHandler(
            "kbdEvent", self.onKbdEvent
        )  # Mercenaries and Stability overlay
        eventManager.addEventHandler("unitLost", self.onUnitLost)  # Mercenaries
        eventManager.addEventHandler("unitKilled", self.onUnitKilled)  # Mercenaries
        eventManager.addEventHandler("OnPreSave", self.onPreSave)  # edead: StoredData
        eventManager.addEventHandler("OnLoad", self.onLoadGame)  # Mercenaries, StoredData
        eventManager.addEventHandler("unitPromoted", self.onUnitPromoted)  # Mercenaries
        eventManager.addEventHandler("techAcquired", self.onTechAcquired)  # Mercenaries #Stability
        # eventManager.addEventHandler("improvementDestroyed",self.onImprovementDestroyed) #Stability
        eventManager.addEventHandler("unitPillage", self.onUnitPillage)  # Stability
        eventManager.addEventHandler("religionSpread", self.onReligionSpread)  # Stability
        eventManager.addEventHandler("firstContact", self.onFirstContact)
        eventManager.addEventHandler(
            "playerChangeAllCivics", self.onPlayerChangeAllCivics
        )  # Absinthe: Python Event for civic changes
        eventManager.addEventHandler(
            "playerChangeSingleCivic", self.onPlayerChangeSingleCivic
        )  # Absinthe: Python Event for civic changes
        eventManager.addEventHandler("playerChangeStateReligion", self.onPlayerChangeStateReligion)

        self.eventManager = eventManager

        self.rnf = RiseAndFall.RiseAndFall()
        self.barb = Barbs.Barbs()
        self.rel = Religions.Religions()
        self.res = Resources.Resources()
        self.cnm = CityNameManager.CityNameManager()
        self.up = UniquePowers.UniquePowers()
        self.aiw = AIWars.AIWars()
        self.vic = Victory.Victory()
        self.sta = Stability.Stability()
        self.pla = Plague.Plague()
        self.crusade = Crusades.Crusades()
        self.provinces = Provinces.ProvinceManager()
        self.mercs = Mercenaries.MercenaryManager()  # 3MiroMercs
        self.company = Companies.Companies()  # Absinthe

        # Mercenaries - start

        self.mercenaryManager = CvMercenaryManager.CvMercenaryManager(
            CvScreenEnums.MERCENARY_MANAGER
        )

        global g_bGameTurnMercenaryCreation
        global g_bDisplayMercenaryManagerOnBeginPlayerTurn
        global g_iStartingEra
        global g_bWanderlustMercenaries
        global g_iWanderlustMercenariesMaximum
        global g_bDisplayMercenaryMessages

    def onGameStart(self, argsList):
        "Called at the start of the game"
        Locations.setup()
        Modifiers.setup()
        Civilizations.setup()

        data.setup()
        self.provinces.setup()
        self.rnf.setup()
        self.rel.setup()
        self.pla.setup()
        self.sta.setup()
        self.aiw.setup()
        self.company.setup()  # Absinthe: initial company setup for the 1200AD scenario

        # 3Miro: WarOnSpawn
        self.rnf.setWarOnSpawn()
        self.vic.setup()

        # Absinthe: generate and store randomized turn modifiers
        data.lEventRandomness[iLighthouseEarthQuake] = rand(40)
        data.lEventRandomness[iByzantiumVikingAttack] = rand(10)

        # Absinthe: rename cities on the 1200AD scenario - the WB file cannot handle special chars and long names properly
        #             some of the cities intentionally have different names though (compared to the CNM), for example some Kievan cities
        #             thus it's only set for Hungary for now, we can add more civs/cities later on if there are naming issues
        if get_scenario() == Scenario.i1200AD:
            for city in cities().owner(Civ.HUNGARY).entities():
                self.cnm.renameCities(city, Civ.HUNGARY)

        # Absinthe: refresh Dynamic Civ Names for all civs on the initial turn of the given scenario
        for iPlayer in civilizations().majors().ids():
            gc.getPlayer(iPlayer).processCivNames()

        return 0

    def onPreSave(self, argsList):
        "called before a game is actually saved"
        data.save()  # edead: pickle & save script data

    # This method creates a new instance of the MercenaryUtils class to be used later
    def onLoadGame(self, argsList):
        data.load()  # edead: load & unpickle script data
        Locations.setup()
        Modifiers.setup()
        Civilizations.setup()

    def onCityAcquired(self, argsList):
        "City Acquired"
        owner, playerType, city, bConquest, bTrade = argsList
        # CvUtil.pyPrint('City Acquired Event: %s' %(city.getName()))

        self.rnf.onCityAcquired(owner, playerType, city, bConquest, bTrade)
        self.cnm.renameCities(city, playerType)

        tCity = (city.getX(), city.getY())

        # Absinthe: If Arabia doesn't found it's first city, but acquires it with a different method (conquest, flip, trade), it should found Islam there (otherwise no holy city at all)
        if playerType == Civ.ARABIA and not gc.getGame().isReligionFounded(Religion.ISLAM):
            # has to be done before the Arab UP is triggered
            gc.getPlayer(Civ.ARABIA).foundReligion(Religion.ISLAM, Religion.ISLAM, False)
            gc.getGame().getHolyCity(Religion.ISLAM).setNumRealBuilding(Building.ISLAMIC_SHRINE, 1)

        # 3Miro: Arab UP
        if gc.hasUP(playerType, UniquePower.SPREAD_STATE_RELIGION_TO_NEW_CITIES):
            self.up.faithUP(playerType, city)

        # Absinthe: Ottoman UP
        if gc.hasUP(playerType, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS):
            self.up.janissaryNewCityUP(playerType, city, bConquest)

        # Absinthe: Scottish UP
        #             against all players (including indies and barbs), but only on conquest
        if owner == Civ.SCOTLAND and bConquest:  # playerType < civilizations().len()
            # only in cities with at least 20% Scottish culture
            iTotalCulture = city.countTotalCultureTimes100()
            if iTotalCulture == 0 or (city.getCulture(owner) * 10000) / iTotalCulture > 20:
                self.up.defianceUP(owner)

        # Absinthe: Aragonese UP
        #             UP tile yields should be recalculated right away, in case the capital was conquered, or province number changed
        if owner == Civ.ARAGON:
            self.up.confederationUP(owner)
        if playerType == Civ.ARAGON:
            self.up.confederationUP(playerType)

        # Absinthe: If Protestantism has not been founded by the time the Dutch spawn, then the Dutch should found it with their first city
        if playerType == Civ.DUTCH and not gc.getGame().isReligionFounded(Religion.PROTESTANTISM):
            gc.getPlayer(Civ.DUTCH).foundReligion(
                Religion.PROTESTANTISM, Religion.PROTESTANTISM, False
            )
            gc.getGame().getHolyCity(Religion.PROTESTANTISM).setNumRealBuilding(
                Building.PROTESTANT_SHRINE, 1
            )
            self.rel.setReformationActive(True)
            self.rel.reformationchoice(Civ.DUTCH)
            self.rel.reformationOther(Civ.INDEPENDENT)
            self.rel.reformationOther(Civ.INDEPENDENT_2)
            self.rel.reformationOther(Civ.INDEPENDENT_3)
            self.rel.reformationOther(Civ.INDEPENDENT_4)
            self.rel.reformationOther(Civ.BARBARIAN)
            self.rel.setReformationHitMatrix(Civ.DUTCH, 2)

            for neighbour in civilization(Civ.DUTCH).location.reformation_neighbours:
                if self.rel.getReformationHitMatrix(neighbour) == 0:
                    self.rel.setReformationHitMatrix(neighbour, 1)

        # Absinthe: Spread some culture to the newly acquired city - this is for nearby indy cities, so should be applied in all cases (conquest, flip, trade)
        if playerType < civilizations().majors().len():
            spreadMajorCulture(playerType, city.getX(), city.getY())

        self.sta.onCityAcquired(owner, playerType, city, bConquest, bTrade)

        # 3Miro: Jerusalem's Golden Age Incentive
        if tCity == CITIES[City.JERUSALEM]:
            pPlayer = gc.getPlayer(playerType)
            if pPlayer.getStateReligion() == Religion.CATHOLICISM:
                # Absinthe: interface message for the player
                if pPlayer.isHuman():
                    CityName = city.getNameKey()
                    message(
                        human(),
                        text("TXT_KEY_CRUSADE_JERUSALEM_SAFE", CityName),
                        force=True,
                        color=MessageData.GREEN,
                    )
                # Absinthe: spread Catholicism if not present already
                if not city.isHasReligion(Religion.CATHOLICISM):
                    self.rel.spreadReligion(tCity, Religion.CATHOLICISM)
                self.crusade.success(playerType)

            # Absinthe: acquiring Jerusalem, with any faith (but not Paganism) -> chance to find a relic
            #             maybe only after a specific date? maybe only if there isn't any ongoing Crusades?
            if (
                percentage_chance(15, strict=True)
                and playerType in civilizations().majors().ids()
                and pPlayer.getStateReligion() != -1
            ):
                pPlayer.initUnit(
                    Unit.HOLY_RELIC,
                    CITIES[City.JERUSALEM][0],
                    CITIES[City.JERUSALEM][1],
                    UnitAITypes.NO_UNITAI,
                    DirectionTypes.DIRECTION_SOUTH,
                )

        # Sedna17: code for Krak des Chevaliers
        if bConquest:
            iNewOwner = city.getOwner()
            pNewOwner = gc.getPlayer(iNewOwner)
            if pNewOwner.countNumBuildings(Wonder.KRAK_DES_CHEVALIERS) > 0:
                city.setHasRealBuilding(getUniqueBuilding(iNewOwner, Building.WALLS), True)
                # Absinthe: if the Castle building were built with the Krak, then it should add stability
                #             the safety checks are probably unnecessary, as Castle buildings are destroyed on conquest (theoretically)
                if not (
                    city.isHasBuilding(Building.SPANISH_CITADEL)
                    or city.isHasBuilding(Building.MOSCOW_KREMLIN)
                    or city.isHasBuilding(Building.HUNGARIAN_STRONGHOLD)
                    or city.isHasBuilding(Building.CASTLE)
                ):
                    city.setHasRealBuilding(getUniqueBuilding(iNewOwner, Building.CASTLE), True)
                    pNewOwner.changeStabilityBase(StabilityCategory.EXPANSION, 1)
        # Sedna17, end

        self.pla.onCityAcquired(owner, playerType, city)  # Plague
        self.vic.onCityAcquired(owner, playerType, city, bConquest, bTrade)  # Victory
        self.company.onCityAcquired(owner, playerType, city)

        # Remove Silk resource near Constantinople if it is conquered
        if tCity == (81, 24):
            self.res.removeResource(80, 24)

        # Remove horse resource near Hadrianople in 1200 AD scenario if someone captures Hadrianople or Constantinople
        if get_scenario() == Scenario.i1200AD:
            if tCity == (76, 25) or tCity == (81, 24):
                self.res.removeResource(77, 24)

        return 0

    def onCityAcquiredAndKept(self, argsList):
        "City Acquired and Kept"
        iOwner, pCity = argsList

        self.mercs.onCityAcquiredAndKept(iOwner, pCity)

    def onCityRazed(self, argsList):
        "City Razed"
        city, iPlayer = argsList

        iPreviousOwner = city.getOwner()
        if iPreviousOwner == iPlayer and city.getPreviousOwner() != -1:
            iPreviousOwner = city.getPreviousOwner()

        self.rnf.onCityRazed(iPreviousOwner, iPlayer, city)  # Rise and Fall
        self.sta.onCityRazed(iPreviousOwner, iPlayer, city)  # Stability
        self.company.onCityRazed(iPreviousOwner, iPlayer, city)
        self.vic.onCityRazed(iPlayer, city)  # Victory
        self.pla.onCityRazed(city, iPlayer)  # Plague

        # Absinthe: Aragonese UP
        #             UP tile yields should be recalculated if your new city is razed
        if iPlayer == Civ.ARAGON:
            self.up.confederationUP(iPlayer)

    def onCityBuilt(self, argsList):
        "City Built"
        city = argsList[0]

        iOwner = city.getOwner()

        self.rnf.onCityBuilt(iOwner, city)
        tCity = (city.getX(), city.getY())

        if iOwner < civilizations().majors().len():
            self.cnm.assignName(city)

        # Absinthe: merc notifications, after the city is named
        self.mercs.onCityBuilt(iOwner, city)

        # Absinthe: Aragonese UP
        #             UP tile yields should be recalculated on city foundation
        if iOwner == Civ.ARAGON:
            self.up.confederationUP(iOwner)

        # Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
        pCurrent = gc.getMap().plot(city.getX(), city.getY())
        for civ in civilizations().minors().ids():
            pCurrent.setCulture(civ, 0, True)

        if iOwner < civilizations().majors().len():
            spreadMajorCulture(iOwner, city.getX(), city.getY())

            if iOwner == Civ.PORTUGAL:
                self.vic.onCityBuilt(city, iOwner)  # needed in Victory.py

                if gc.getTeam(gc.getPlayer(Civ.PORTUGAL).getTeam()).isHasTech(
                    Technology.ASTRONOMY
                ):
                    city.setHasRealBuilding(Building.PORTUGAL_FEITORIA, True)

        # Absinthe: Free buildings if city is built on a tile improvement
        #             The problem is that the improvement is auto-destroyed before the city is founded, and totally separately from this function, thus a workaround is needed
        #             Solution: getting the coordinates of the last destroyed improvement from a different file in a global variable
        #             If the last destroyed improvement in the game is a fort, and it was in the same place as the city, then it's good enough for me
        #             (only problem might be if currently there is no improvement on the city-founding tile, but the last destroyed improvement in the game
        #                 was a fort on the exact same plot some turns ago - but IMO that's not much of a stress of reality, there was a fort there after all)
        #             Note that CvEventManager.iImpBeforeCity needs to have some initial value if a city is founded before the first destroyed improvement
        #                 adding an improvement in the scenario map to one of the preplaced Byzantine cities won't work perfectly:
        #                 while the improvement will be autorazed on the beginning of the 1st players turn when starting in 500AD, does nothing if you load a saved game
        iImpBeforeCityType = (CvEventManager.iImpBeforeCity / 10000) % 100
        iImpBeforeCityX = (CvEventManager.iImpBeforeCity / 100) % 100
        iImpBeforeCityY = CvEventManager.iImpBeforeCity % 100
        # Absinthe: free walls if built on fort
        if iImpBeforeCityType == Improvement.FORT and (iImpBeforeCityX, iImpBeforeCityY) == tCity:
            city.setHasRealBuilding(getUniqueBuilding(iOwner, Building.WALLS), True)
        # Absinthe: free granary if built on hamlet
        if (
            iImpBeforeCityType == Improvement.HAMLET
            and (iImpBeforeCityX, iImpBeforeCityY) == tCity
        ):
            city.setHasRealBuilding(getUniqueBuilding(iOwner, Building.GRANARY), True)
        # Absinthe: free granary and +1 population if built on village or town
        if iImpBeforeCityType in [Improvement.TOWN, Improvement.VILLAGE]:
            if (iImpBeforeCityX, iImpBeforeCityY) == tCity:
                city.changePopulation(1)
                city.setHasRealBuilding(getUniqueBuilding(iOwner, Building.GRANARY), True)

        # Absinthe: Some initial food for all cities on foundation
        #             So Leon and Roskilde for example don't lose a population in the first couple turns
        #             Nor the indy cities on spawn (they start with zero-sized culture, so they shrink without some food reserves)
        #             Currently 1/5 of the treshold of the next population growth
        city.setFood(city.growthThreshold() / 5)

        # 3MiroUP: spread religion on city foundation
        if gc.hasUP(iOwner, UniquePower.SPREAD_STATE_RELIGION_TO_NEW_CITIES):
            self.up.faithUP(iOwner, city)

        # Absinthe: If Protestantism has not been founded by the time the Dutch spawn, then the Dutch should found it with their first city
        if iOwner == Civ.DUTCH and not gc.getGame().isReligionFounded(Religion.PROTESTANTISM):
            gc.getPlayer(Civ.DUTCH).foundReligion(
                Religion.PROTESTANTISM, Religion.PROTESTANTISM, False
            )
            gc.getGame().getHolyCity(Religion.PROTESTANTISM).setNumRealBuilding(
                Building.PROTESTANT_SHRINE, 1
            )
            self.rel.setReformationActive(True)
            self.rel.reformationchoice(Civ.DUTCH)
            self.rel.reformationOther(Civ.INDEPENDENT)
            self.rel.reformationOther(Civ.INDEPENDENT_2)
            self.rel.reformationOther(Civ.INDEPENDENT_3)
            self.rel.reformationOther(Civ.INDEPENDENT_4)
            self.rel.reformationOther(Civ.BARBARIAN)
            self.rel.setReformationHitMatrix(Civ.DUTCH, 2)

            for neighbour in civilization(Civ.DUTCH).location.reformation_neighbours:
                if self.rel.getReformationHitMatrix(neighbour) == 0:
                    self.rel.setReformationHitMatrix(neighbour, 1)

        if iOwner < civilizations().majors().len():
            self.sta.onCityBuilt(iOwner, city.getX(), city.getY())

    def onCombatResult(self, argsList):
        self.vic.onCombatResult(argsList)
        self.sta.onCombatResult(argsList)

    def onReligionFounded(self, argsList):
        "Religion Founded"
        iReligion, iFounder = argsList

        if iReligion != Religion.JUDAISM:
            for city in cities().owner(iFounder).entities():
                if city.isHolyCityByType(
                    iReligion
                ):  # Sedna: Protestant Shrine is now starting point for consistency with Religion.xml, Judaism is special
                    if iReligion == Religion.PROTESTANTISM:
                        iTemple = Building.PROTESTANT_TEMPLE
                        iShrine = Building.PROTESTANT_SHRINE
                    elif iReligion == Religion.ISLAM:
                        iTemple = Building.ISLAMIC_TEMPLE
                        iShrine = Building.ISLAMIC_SHRINE
                    elif iReligion == Religion.CATHOLICISM:
                        iTemple = Building.CATHOLIC_TEMPLE
                        iShrine = Building.CATHOLIC_SHRINE
                    elif iReligion == Religion.ORTHODOXY:
                        iTemple = Building.ORTHODOX_TEMPLE
                        iShrine = Building.ORTHODOX_SHRINE
                    if not city.isHasRealBuilding(iShrine):
                        city.setHasRealBuilding(iShrine, True)
                    if not city.isHasRealBuilding(iTemple):
                        city.setHasRealBuilding(iTemple, True)
                    break

        self.vic.onReligionFounded(iReligion, iFounder)

        if iFounder < civilizations().majors().len():
            self.sta.onReligionFounded(iFounder)

        # 3Miro: end Crusades for the Holy Land after the Reformation
        if iReligion == Religion.PROTESTANTISM:
            self.crusade.endCrusades()

    def onBuildingBuilt(self, argsList):
        city, iBuildingType = argsList
        iOwner = city.getOwner()

        self.vic.onBuildingBuilt(iOwner, iBuildingType)
        if city.getOwner() < civilizations().majors().len():
            self.sta.onBuildingBuilt(iOwner, iBuildingType)
            self.company.onBuildingBuilt(iOwner, iBuildingType)
        # Absinthe: Faith, Kazimierz, Mont Saint-Michel
        self.rel.onBuildingBuilt(iOwner, iBuildingType)

        # Absinthe: Aragonese UP
        # UP tile yields should be recalculated right away if a new Palace was built
        if iOwner == Civ.ARAGON and iBuildingType == Building.PALACE:
            self.up.confederationUP(iOwner)

    def onProjectBuilt(self, argsList):
        city, iProjectType = argsList
        self.vic.onProjectBuilt(city.getOwner(), iProjectType)
        if city.getOwner() < civilizations().majors().len():
            self.sta.onProjectBuilt(city.getOwner(), iProjectType)

    def onUnitPillage(self, argsList):
        pUnit, iImprovement, iRoute, iOwner = argsList
        iPlotX = pUnit.getX()
        iPlotY = pUnit.getY()
        pPlot = CyMap().plot(iPlotX, iPlotY)
        if pPlot.countTotalCulture() == 0:
            if iImprovement >= Improvement.COTTAGE and iImprovement <= Improvement.TOWN:
                self.barb.onImprovementDestroyed(iPlotX, iPlotY)
        iVictim = pPlot.getOwner()
        if iVictim > -1 and iVictim < civilizations().majors().len():
            self.sta.onImprovementDestroyed(iVictim)

        self.vic.onPillageImprovement(
            pUnit.getOwner(), iVictim, iImprovement, iRoute, iPlotX, iPlotY
        )

    def onBeginGameTurn(self, argsList):
        iGameTurn = argsList[0]

        # Absinthe: 868AD Viking attack on Constantinople
        if iGameTurn == year(860) + data.lEventRandomness[iByzantiumVikingAttack] - 2:
            if human() == Civ.BYZANTIUM:
                show(text("TXT_KEY_EVENT_VIKING_CONQUERERS_RUMOURS"))

        if iGameTurn == year(860) + data.lEventRandomness[iByzantiumVikingAttack]:
            if human() == Civ.BYZANTIUM:
                for unit, number in zip((Unit.DENMARK_HUSKARL, Unit.VIKING_BERSERKER), (3, 4)):
                    self.barb.spawnUnits(
                        Civ.BARBARIAN,
                        (80, 24),
                        (80, 25),
                        unit,
                        number,
                        iGameTurn,
                        1,
                        0,
                        forcedInvasion,
                        UnitAITypes.UNITAI_ATTACK,
                        text("TXT_KEY_BARBARIAN_NAMES_VIKINGS"),
                    )
                message(
                    Civ.BYZANTIUM,
                    text("TXT_KEY_EVENT_VIKING_CONQUERERS_ARRIVE"),
                    color=MessageData.RED,
                )

        # Absinthe: Message for the human player about the Schism
        elif iGameTurn == year(1053):
            if player().isExisting():
                sText = text("TXT_KEY_GREAT_SCHISM")
                message(human(), sText, color=MessageData.DARK_PINK)

        # Absinthe: Remove the Great Lighthouse, message for the human player if the city is visible
        elif iGameTurn == year(1323) - 40 + data.lEventRandomness[iLighthouseEarthQuake]:
            for iPlayer in civilizations().drop(Civ.BARBARIAN).ids():
                bFound = 0
                for city in cities().owner(iPlayer).entities():
                    if city.isHasBuilding(Wonder.GREAT_LIGHTHOUSE):
                        city.setHasRealBuilding(Wonder.GREAT_LIGHTHOUSE, False)
                        GLcity = city
                        bFound = 1
                if bFound and human() == iPlayer:
                    pPlayer = gc.getPlayer(iPlayer)
                    iTeam = pPlayer.getTeam()
                    if GLcity.isRevealed(iTeam, False):
                        message(
                            iPlayer,
                            text("TXT_KEY_BUILDING_GREAT_LIGHTHOUSE_REMOVED"),
                            color=MessageData.RED,
                        )

        self.barb.checkTurn(iGameTurn)
        self.rnf.checkTurn(iGameTurn)
        self.rel.checkTurn(iGameTurn)
        self.res.checkTurn(iGameTurn)
        self.up.checkTurn(iGameTurn)
        self.aiw.checkTurn(iGameTurn)
        self.pla.checkTurn(iGameTurn)
        self.vic.checkTurn(iGameTurn)
        self.sta.checkTurn(iGameTurn)
        self.crusade.checkTurn(iGameTurn)
        self.provinces.checkTurn(iGameTurn)
        self.company.checkTurn(iGameTurn)

        return 0

    def onBeginPlayerTurn(self, argsList):
        iGameTurn, iPlayer = argsList
        iHuman = human()
        if self.rnf.getDeleteMode(0) != -1:
            self.rnf.deleteMode(iPlayer)
        # Absinthe: refresh Dynamic Civ Names
        if iPlayer < civilizations().majors().len():
            gc.getPlayer(iPlayer).processCivNames()

        # Absinthe: Byzantine conqueror army
        if iGameTurn == year(520):
            if iPlayer == Civ.BYZANTIUM:
                pByzantium = gc.getPlayer(Civ.BYZANTIUM)
                tStartingPlot = (59, 16)
                pByzantium.initUnit(
                    Unit.GALLEY,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GALLEY,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GALLEY,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GALLEY,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GALLEY,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GREAT_GENERAL,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_GENERAL,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pPlot = CyMap().plot(tStartingPlot[0], tStartingPlot[1])
                for iUnitLoop in range(pPlot.getNumUnits()):
                    pUnit = pPlot.getUnit(iUnitLoop)
                    if pUnit.getUnitType() == CvUtil.findInfoTypeNum(
                        gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_GREAT_GENERAL"
                    ):
                        pUnit.setName(text("TXT_KEY_GREAT_PERSON_BELISARIUS"))
                make_units(Civ.BYZANTIUM, Unit.SWORDSMAN, tStartingPlot, 4)
                make_units(Civ.BYZANTIUM, Unit.AXEMAN, tStartingPlot, 3)
                make_units(Civ.BYZANTIUM, Unit.ARCHER, tStartingPlot, 2)
                if iPlayer == iHuman:
                    show(text("TXT_KEY_EVENT_CONQUEROR_BELISARIUS"))

        # Absinthe: popup message a couple turns before the Seljuk/Mongol/Timurid invasions
        if iPlayer == iHuman:
            # Seljuks
            if iGameTurn == year(1064) - 7:
                if iPlayer == Civ.BYZANTIUM:
                    show(("TXT_KEY_EVENT_BARBARIAN_INVASION_START"))
            elif iGameTurn == year(1094) + 1:
                if iPlayer == Civ.BYZANTIUM:
                    sText = "Seljuk"
                    show(text("TXT_KEY_EVENT_BARBARIAN_INVASION_END", sText))
            # Mongols
            elif iGameTurn == year(1236) - 7:
                if iPlayer in [
                    Civ.KIEV,
                    Civ.HUNGARY,
                    Civ.POLAND,
                    Civ.BULGARIA,
                ]:
                    show(text("TXT_KEY_EVENT_BARBARIAN_INVASION_START"))
            elif iGameTurn == year(1288) + 1:
                if iPlayer in [
                    Civ.KIEV,
                    Civ.HUNGARY,
                    Civ.POLAND,
                    Civ.BULGARIA,
                ]:
                    sText = "Tatar"
                    show(text("TXT_KEY_EVENT_BARBARIAN_INVASION_END", sText))
            # Timurids
            elif iGameTurn == year(1380) - 7:
                if iPlayer in [Civ.ARABIA, Civ.OTTOMAN, Civ.BYZANTIUM]:
                    show(text("TXT_KEY_EVENT_TIMURID_INVASION_START"))
            elif iGameTurn == year(1431) + 1:
                if iPlayer in [Civ.ARABIA, Civ.OTTOMAN, Civ.BYZANTIUM]:
                    sText = "Timurid"
                    show(text("TXT_KEY_EVENT_BARBARIAN_INVASION_END", sText))

        # Absinthe: Denmark UP
        if iPlayer == Civ.DENMARK:
            self.up.soundUP(iPlayer)

        # Absinthe: Aragonese UP
        # safety check: probably redundant, calls from onBuildingBuilt, onCityBuilt, onCityAcquired and onCityRazed should be enough
        elif iPlayer == Civ.ARAGON:
            self.up.confederationUP(iPlayer)

        # Ottoman UP
        if gc.hasUP(iPlayer, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS):
            self.up.janissaryDraftUP(iPlayer)

        self.pla.checkPlayerTurn(iGameTurn, iPlayer)
        self.vic.checkPlayerTurn(iGameTurn, iPlayer)

        if gc.getPlayer(iPlayer).isAlive() and iPlayer < civilizations().majors().len():
            if gc.getPlayer(iPlayer).getNumCities() > 0:
                self.sta.updateBaseStability(iGameTurn, iPlayer)

            # for the AI only, leader switch and cheats
            if iPlayer != iHuman:
                self.rnf.checkPlayerTurn(iGameTurn, iPlayer)

            # not really needed, we set it on collapse anyway
            # setLastTurnAlive( iPlayer, iGameTurn )

        self.crusade.checkPlayerTurn(iGameTurn, iPlayer)

    def onEndPlayerTurn(self, argsList):
        """Called at the end of a players turn"""
        # 3Miro does not get called
        iGameTurn, iPlayer = argsList

    def onEndGameTurn(self, argsList):
        iGameTurn = argsList[0]
        self.sta.checkImplosion(iGameTurn)
        self.mercs.doMercsTurn(iGameTurn)

    def onReligionSpread(self, argsList):
        iReligion, iOwner, pSpreadCity = argsList
        self.sta.onReligionSpread(iReligion, iOwner)
        self.rel.onReligionSpread(iReligion, iOwner)

    def onFirstContact(self, argsList):

        iTeamX, iHasMetTeamY = argsList
        self.rnf.onFirstContact(iTeamX, iHasMetTeamY)

    # Absinthe: Python Event for civic changes
    def onPlayerChangeAllCivics(self, argsList):
        # note that this only reports civic change if it happened via normal revolution
        "Player changes his civics"
        iPlayer = argsList[0]
        lNewCivics = [argsList[1], argsList[2], argsList[3], argsList[4], argsList[5], argsList[6]]
        lOldCivics = [
            argsList[7],
            argsList[8],
            argsList[9],
            argsList[10],
            argsList[11],
            argsList[12],
        ]
        if iPlayer < civilizations().majors().len():
            self.rel.onPlayerChangeAllCivics(iPlayer, lNewCivics, lOldCivics)

    def onPlayerChangeSingleCivic(self, argsList):
        # note that this reports all civic changes in single instances (so also reports force converts by diplomacy or with spies)
        "Civics are changed for a player"
        iPlayer, iNewCivic, iOldCivic = argsList

    def onPlayerChangeStateReligion(self, argsList):
        "Player changes his state religion"
        iPlayer, iNewReligion, iOldReligion = argsList

        if iPlayer < civilizations().majors().len():
            self.company.onPlayerChangeStateReligion(argsList)

    def onTechAcquired(self, argsList):
        iPlayer = argsList[2]
        self.vic.onTechAcquired(argsList[0], argsList[2])

        if (
            gc.getPlayer(iPlayer).isAlive()
            and turn() > civilization(iPlayer).date.birth
            and iPlayer < civilizations().majors().len()
        ):
            self.rel.onTechAcquired(argsList[0], argsList[2])
            self.sta.onTechAcquired(argsList[0], argsList[2])

    # This method will redraw the main interface once a unit is promoted. This way the
    # gold/turn information will be updated.
    def onUnitPromoted(self, argsList):
        "Unit Promoted"

        self.mercs.onUnitPromoted(argsList)

    # This method will remove a mercenary unit from the game if it is killed
    def onUnitKilled(self, argsList):
        "Unit Killed"

        self.mercs.onUnitKilled(argsList)

    # This method will remove a mercenary unit from the game if it is lost
    def onUnitLost(self, argsList):
        "Unit Lost"

        self.mercs.onUnitLost(argsList)

    # This method handles the key input and will bring up the mercenary manager screen if the
    # player has at least one city and presses 'ctrl' and the 'M' key.
    def onKbdEvent(self, argsList):
        "keypress handler - return 1 if the event was consumed"

        if player().isAlive():
            eventType, key, mx, my, px, py = argsList
            theKey = int(key)

            if (
                eventType == self.EventKeyDown
                and theKey == int(InputTypes.KB_M)
                and self.eventManager.bCtrl
                and gc.getActivePlayer().getNumCities() > 0
            ):

                self.mercenaryManager.interfaceScreen()

        # Rhye - start debug
        eventType, key, mx, my, px, py = argsList

        theKey = int(key)

        if (
            eventType == self.EventKeyDown
            and theKey == int(InputTypes.KB_B)
            and self.eventManager.bAlt
        ):

            iGameTurn = turn()
            pass

        if (
            eventType == self.EventKeyDown
            and theKey == int(InputTypes.KB_N)
            and self.eventManager.bAlt
        ):
            self.printPlotsDebug()

        if (
            eventType == self.EventKeyDown
            and theKey == int(InputTypes.KB_E)
            and self.eventManager.bAlt
            and self.eventManager.bShift
        ):
            # picks a dead civ so that autoplay can be started with game.AIplay xx
            iDebugDeadCiv = Civ.BURGUNDY  # always dead in 500AD
            make_unit(iDebugDeadCiv, Unit.AXEMAN, (0, 0))
            gc.getGame().setActivePlayer(iDebugDeadCiv, False)
            gc.getPlayer(iDebugDeadCiv).setPlayable(True)
        # Rhye - end debug

        # Absinthe: province highlight - based on SoI
        if (
            eventType == self.EventKeyDown
            and px >= 0
            and py >= 0
            and int(key) == 45
            and self.eventManager.bCtrl
            and not self.eventManager.bAlt
        ):

            plot = gc.getMap().plot(px, py)
            iActivePlayer = gc.getGame().getActivePlayer()
            iActiveTeam = gc.getPlayer(iActivePlayer).getTeam()
            iProvinceID = PROVINCES_MAP[plot.getY()][plot.getX()]

            # do not show provinces of unrevealed tiles
            if not plot.isRevealed(iActiveTeam, False) and not gc.getGame().isDebugMode():
                return

            # do not redraw if already drawn
            if self.lastProvinceID == iProvinceID:
                return

            map = CyMap()
            engine = CyEngine()

            # clear the highlight
            engine.clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)

            # cache the plot's coords
            self.lastProvinceID = PROVINCES_MAP[plot.getY()][plot.getX()]

            # select an appropriate color
            if PROVINCES_MAP[plot.getY()][plot.getX()] == -1:  # ocean and non-province tiles
                return
            else:
                iLevel = getProvinceStabilityLevel(human(), iProvinceID)
                if iLevel == 4:
                    color = gc.getColorInfo(
                        gc.getInfoTypeForString("COLOR_HIGHLIGHT_CORE")
                    ).getColor()
                elif iLevel == 3:
                    color = gc.getColorInfo(
                        gc.getInfoTypeForString("COLOR_HIGHLIGHT_NATURAL")
                    ).getColor()
                elif iLevel == 2:
                    color = gc.getColorInfo(
                        gc.getInfoTypeForString("COLOR_HIGHLIGHT_POTENTIAL")
                    ).getColor()
                elif iLevel == 1:
                    color = gc.getColorInfo(
                        gc.getInfoTypeForString("COLOR_HIGHLIGHT_BORDER")
                    ).getColor()
                else:
                    color = gc.getColorInfo(
                        gc.getInfoTypeForString("COLOR_HIGHLIGHT_FOREIGN")
                    ).getColor()

            # apply the highlight
            for i in range(map.numPlots()):
                plot = map.plotByIndex(i)
                if PROVINCES_MAP[plot.getY()][plot.getX()] == iProvinceID and (
                    gc.getGame().isDebugMode() or plot.isRevealed(iActiveTeam, False)
                ):
                    engine.fillAreaBorderPlot(
                        plot.getX(),
                        plot.getY(),
                        color,
                        AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT,
                    )

            return

        # clear all highlights
        if (eventType == self.EventKeyUp and self.eventManager.bCtrl) or (
            eventType == self.EventKeyDown
        ):
            CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)
            self.lastProvinceID = -1
        # Absinthe: end

    def printPlotsDebug(self):
        pass
