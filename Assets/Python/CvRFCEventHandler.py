# Rhye's and Fall of Civilization: Europe - Event handler

from CvPythonExtensions import *
from CoreData import civilizations, civilization
from CoreStructures import human, player
import CvUtil
import CvEventManager  # Mercenaries
import PyHelpers
import CvMercenaryManager  # Mercenaries
import CvScreenEnums  # Mercenaries
import Popup

from StoredData import sd
import RiseAndFall
import Barbs
import Religions
import Resources
import CityNameManager
import UniquePowers
import AIWars
import RFCUtils

import Victory
import Stability
import Plague
import Crusades
import Companies
import DataLoader
import Province
import Mercenaries

from Scenario import get_scenario
from MiscData import MessageData
from TimelineData import DateTurn
from MapsData import PROVINCES_MAP
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
localText = CyTranslator()  # Absinthe
utils = RFCUtils.RFCUtils()
# iBetrayalCheaters = 15


# Absinthe: Turn Randomization constants
iLighthouseEarthQuake = 0
iByzantiumVikingAttack = 1

# Absinthe: all of this Mercenary stuff is unused
# Mercenaries - start

PyPlayer = PyHelpers.PyPlayer
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


###################################################
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
        self.province = Province.ProvinceManager()
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

        # Rhye - start comment

    ##		# Load the Mercenaries Mod Config INI file containing all of the configuration information
    ##		config = CvConfigParser.CvConfigParser("Mercenaries Mod Config.ini")
    ##
    ##		# If we actually were able to open the "Mercenaries Mod Config.ini" file then read in the values.
    ##		# otherwise we'll keep the default values that were set at the top of this file.
    ##		if(config != None):
    ##			g_bGameTurnMercenaryCreation = config.getboolean("Mercenaries Mod", "Game Turn Mercenary Creation", True)
    ##			g_bDisplayMercenaryManagerOnBeginPlayerTurn = config.getboolean("Mercenaries Mod", "Display Mercenary Manager On Begin Player Turn", False)
    ##			g_iStartingEra = gc.getInfoTypeForString(config.get("Mercenaries Mod","Starting Era","ERA_ANCIENT"))
    ##			g_bWanderlustMercenaries = config.getboolean("Mercenaries Mod", "Wanderlust Mercenaries", True)
    ##			g_iWanderlustMercenariesMaximum = config.getint("Mercenaries Mod","Wanderlust Mercenaries Maximum", 5)
    ##			g_bDisplayMercenaryMessages = config.getboolean("Mercenaries Mod", "Display Mercenary Messages", True)
    # Rhye - end comment

    def onGameStart(self, argsList):
        "Called at the start of the game"
        # self.pm.setup()
        DataLoader.setup()
        sd.setup()  # initialise global script data
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
        sd.scriptDict["lEventRandomness"][iLighthouseEarthQuake] = gc.getGame().getSorenRandNum(
            40, "Final Earthquake"
        )
        sd.scriptDict["lEventRandomness"][iByzantiumVikingAttack] = gc.getGame().getSorenRandNum(
            10, "Viking Attack"
        )

        # Absinthe: rename cities on the 1200AD scenario - the WB file cannot handle special chars and long names properly
        # 			some of the cities intentionally have different names though (compared to the CNM), for example some Kievan cities
        # 			thus it's only set for Hungary for now, we can add more civs/cities later on if there are naming issues
        if get_scenario() == Scenario.i1200AD:
            for city in utils.getCityList(Civ.HUNGARY.value):
                self.cnm.renameCities(city, Civ.HUNGARY.value)

        # Absinthe: refresh Dynamic Civ Names for all civs on the initial turn of the given scenario
        for iPlayer in civilizations().majors().ids():
            gc.getPlayer(iPlayer).processCivNames()

        return 0

    def onCityAcquired(self, argsList):
        "City Acquired"
        owner, playerType, city, bConquest, bTrade = argsList
        # CvUtil.pyPrint('City Acquired Event: %s' %(city.getName()))

        self.rnf.onCityAcquired(owner, playerType, city, bConquest, bTrade)
        self.cnm.renameCities(city, playerType)

        tCity = (city.getX(), city.getY())

        # Absinthe: If Arabia doesn't found it's first city, but acquires it with a different method (conquest, flip, trade), it should found Islam there (otherwise no holy city at all)
        if playerType == Civ.ARABIA.value and not gc.getGame().isReligionFounded(
            Religion.ISLAM.value
        ):
            # has to be done before the Arab UP is triggered
            gc.getPlayer(Civ.ARABIA.value).foundReligion(
                Religion.ISLAM.value, Religion.ISLAM.value, False
            )
            gc.getGame().getHolyCity(Religion.ISLAM.value).setNumRealBuilding(
                Building.ISLAMIC_SHRINE.value, 1
            )

        # 3Miro: Arab UP
        if gc.hasUP(playerType, UniquePower.SPREAD_STATE_RELIGION_TO_NEW_CITIES.value):
            self.up.faithUP(playerType, city)

        # Absinthe: Ottoman UP
        if gc.hasUP(playerType, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS.value):
            self.up.janissaryNewCityUP(playerType, city, bConquest)

        # Absinthe: Scottish UP
        # 			against all players (including indies and barbs), but only on conquest
        if owner == Civ.SCOTLAND.value and bConquest:  # playerType < civilizations().len()
            # only in cities with at least 20% Scottish culture
            iTotalCulture = city.countTotalCultureTimes100()
            if iTotalCulture == 0 or (city.getCulture(owner) * 10000) / iTotalCulture > 20:
                self.up.defianceUP(owner)

        # Absinthe: Aragonese UP
        # 			UP tile yields should be recalculated right away, in case the capital was conquered, or province number changed
        if owner == Civ.ARAGON.value:
            self.up.confederationUP(owner)
        if playerType == Civ.ARAGON.value:
            self.up.confederationUP(playerType)

        # Absinthe: If Protestantism has not been founded by the time the Dutch spawn, then the Dutch should found it with their first city
        if playerType == Civ.DUTCH.value and not gc.getGame().isReligionFounded(
            Religion.PROTESTANTISM.value
        ):
            gc.getPlayer(Civ.DUTCH.value).foundReligion(
                Religion.PROTESTANTISM.value, Religion.PROTESTANTISM.value, False
            )
            gc.getGame().getHolyCity(Religion.PROTESTANTISM.value).setNumRealBuilding(
                Building.PROTESTANT_SHRINE.value, 1
            )
            self.rel.setReformationActive(True)
            self.rel.reformationchoice(Civ.DUTCH.value)
            self.rel.reformationOther(Civ.INDEPENDENT.value)
            self.rel.reformationOther(Civ.INDEPENDENT_2.value)
            self.rel.reformationOther(Civ.INDEPENDENT_3.value)
            self.rel.reformationOther(Civ.INDEPENDENT_4.value)
            self.rel.reformationOther(Civ.BARBARIAN.value)
            self.rel.setReformationHitMatrix(Civ.DUTCH.value, 2)
            for iCiv in civilizations().majors().ids():
                if (
                    iCiv in Religions.lReformationNeighbours[Civ.DUTCH.value]
                    and self.rel.getReformationHitMatrix(iCiv) == 0
                ):
                    self.rel.setReformationHitMatrix(iCiv, 1)

        # Absinthe: Spread some culture to the newly acquired city - this is for nearby indy cities, so should be applied in all cases (conquest, flip, trade)
        if playerType < civilizations().majors().len():
            utils.spreadMajorCulture(playerType, city.getX(), city.getY())

        self.sta.onCityAcquired(owner, playerType, city, bConquest, bTrade)

        # 3Miro: Jerusalem's Golden Age Incentive
        if tCity == CITIES[City.JERUSALEM].to_tuple():
            pPlayer = gc.getPlayer(playerType)
            if pPlayer.getStateReligion() == Religion.CATHOLICISM.value:
                # Absinthe: interface message for the player
                if pPlayer.isHuman():
                    CityName = city.getNameKey()
                    CyInterface().addMessage(
                        human(),
                        True,
                        MessageData.DURATION,
                        CyTranslator().getText("TXT_KEY_CRUSADE_JERUSALEM_SAFE", (CityName,)),
                        "",
                        0,
                        "",
                        ColorTypes(MessageData.GREEN),
                        -1,
                        -1,
                        True,
                        True,
                    )
                # Absinthe: spread Catholicism if not present already
                if not city.isHasReligion(Religion.CATHOLICISM.value):
                    self.rel.spreadReligion(tCity, Religion.CATHOLICISM.value)
                self.crusade.success(playerType)

            # Absinthe: acquiring Jerusalem, with any faith (but not Paganism) -> chance to find a relic
            # 			maybe only after a specific date? maybe only if there isn't any ongoing Crusades?
            if gc.getGame().getSorenRandNum(100, "Relic found") < 15:
                # for major players only
                if playerType < civilizations().majors().len():
                    if pPlayer.getStateReligion() in range(len(Religion)):
                        pPlayer.initUnit(
                            Unit.HOLY_RELIC.value,
                            CITIES[City.JERUSALEM].x,
                            CITIES[City.JERUSALEM].y,
                            UnitAITypes.NO_UNITAI,
                            DirectionTypes.DIRECTION_SOUTH,
                        )

        # Sedna17: code for Krak des Chevaliers
        if bConquest:
            iNewOwner = city.getOwner()
            pNewOwner = gc.getPlayer(iNewOwner)
            if pNewOwner.countNumBuildings(Wonder.KRAK_DES_CHEVALIERS.value) > 0:
                city.setHasRealBuilding(
                    utils.getUniqueBuilding(iNewOwner, Building.WALLS.value), True
                )
                # Absinthe: if the Castle building were built with the Krak, then it should add stability
                # 			the safety checks are probably unnecessary, as Castle buildings are destroyed on conquest (theoretically)
                if not (
                    city.isHasBuilding(Building.SPANISH_CITADEL.value)
                    or city.isHasBuilding(Building.MOSCOW_KREMLIN.value)
                    or city.isHasBuilding(Building.HUNGARIAN_STRONGHOLD.value)
                    or city.isHasBuilding(Building.CASTLE.value)
                ):
                    city.setHasRealBuilding(
                        utils.getUniqueBuilding(iNewOwner, Building.CASTLE.value), True
                    )
                    pNewOwner.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)
        # Sedna17, end

        # 3Miro: National wonders and city acquire by trade
        # if (bTrade):
        # 	for i in range (iScotlandYard +1 - Building.HEROIC_EPIC.value):
        # 		iNationalWonder = i + Building.HEROIC_EPIC.value
        # 		if (city.hasBuilding(iNationalWonder)):
        # 			city.setHasRealBuilding((iNationalWonder), False)

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
        # 			UP tile yields should be recalculated if your new city is razed
        if iPlayer == Civ.ARAGON.value:
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
        # 			UP tile yields should be recalculated on city foundation
        if iOwner == Civ.ARAGON.value:
            self.up.confederationUP(iOwner)

        # Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
        pCurrent = gc.getMap().plot(city.getX(), city.getY())
        for civ in civilizations().minors().ids():
            pCurrent.setCulture(civ, 0, True)

        if iOwner < civilizations().majors().len():
            utils.spreadMajorCulture(iOwner, city.getX(), city.getY())

            if iOwner == Civ.PORTUGAL.value:
                self.vic.onCityBuilt(city, iOwner)  # needed in Victory.py

                if gc.getTeam(gc.getPlayer(Civ.PORTUGAL.value).getTeam()).isHasTech(
                    Technology.ASTRONOMY.value
                ):
                    city.setHasRealBuilding(Building.PORTUGAL_FEITORIA.value, True)

        # Absinthe: Free buildings if city is built on a tile improvement
        # 			The problem is that the improvement is auto-destroyed before the city is founded, and totally separately from this function, thus a workaround is needed
        # 			Solution: getting the coordinates of the last destroyed improvement from a different file in a global variable
        # 			If the last destroyed improvement in the game is a fort, and it was in the same place as the city, then it's good enough for me
        # 			(only problem might be if currently there is no improvement on the city-founding tile, but the last destroyed improvement in the game
        # 				was a fort on the exact same plot some turns ago - but IMO that's not much of a stress of reality, there was a fort there after all)
        # 			Note that CvEventManager.iImpBeforeCity needs to have some initial value if a city is founded before the first destroyed improvement
        # 				adding an improvement in the scenario map to one of the preplaced Byzantine cities won't work perfectly:
        # 				while the improvement will be autorazed on the beginning of the 1st players turn when starting in 500AD, does nothing if you load a saved game
        iImpBeforeCityType = (CvEventManager.iImpBeforeCity / 10000) % 100
        iImpBeforeCityX = (CvEventManager.iImpBeforeCity / 100) % 100
        iImpBeforeCityY = CvEventManager.iImpBeforeCity % 100
        # Absinthe: free walls if built on fort
        if (
            iImpBeforeCityType == Improvement.FORT.value
            and (iImpBeforeCityX, iImpBeforeCityY) == tCity
        ):
            city.setHasRealBuilding(utils.getUniqueBuilding(iOwner, Building.WALLS.value), True)
        # Absinthe: free granary if built on hamlet
        if (
            iImpBeforeCityType == Improvement.HAMLET.value
            and (iImpBeforeCityX, iImpBeforeCityY) == tCity
        ):
            city.setHasRealBuilding(utils.getUniqueBuilding(iOwner, Building.GRANARY.value), True)
        # Absinthe: free granary and +1 population if built on village or town
        if iImpBeforeCityType in [Improvement.TOWN.value, Improvement.VILLAGE.value]:
            if (iImpBeforeCityX, iImpBeforeCityY) == tCity:
                city.changePopulation(1)
                city.setHasRealBuilding(
                    utils.getUniqueBuilding(iOwner, Building.GRANARY.value), True
                )

        # Absinthe: Some initial food for all cities on foundation
        # 			So Leon and Roskilde for example don't lose a population in the first couple turns
        # 			Nor the indy cities on spawn (they start with zero-sized culture, so they shrink without some food reserves)
        # 			Currently 1/5 of the treshold of the next population growth
        city.setFood(city.growthThreshold() / 5)

        # 3MiroUP: spread religion on city foundation
        if gc.hasUP(iOwner, UniquePower.SPREAD_STATE_RELIGION_TO_NEW_CITIES.value):
            self.up.faithUP(iOwner, city)

        # Absinthe: If Protestantism has not been founded by the time the Dutch spawn, then the Dutch should found it with their first city
        if iOwner == Civ.DUTCH.value and not gc.getGame().isReligionFounded(
            Religion.PROTESTANTISM.value
        ):
            gc.getPlayer(Civ.DUTCH.value).foundReligion(
                Religion.PROTESTANTISM.value, Religion.PROTESTANTISM.value, False
            )
            gc.getGame().getHolyCity(Religion.PROTESTANTISM.value).setNumRealBuilding(
                Building.PROTESTANT_SHRINE.value, 1
            )
            self.rel.setReformationActive(True)
            self.rel.reformationchoice(Civ.DUTCH.value)
            self.rel.reformationOther(Civ.INDEPENDENT.value)
            self.rel.reformationOther(Civ.INDEPENDENT_2.value)
            self.rel.reformationOther(Civ.INDEPENDENT_3.value)
            self.rel.reformationOther(Civ.INDEPENDENT_4.value)
            self.rel.reformationOther(Civ.BARBARIAN.value)
            self.rel.setReformationHitMatrix(Civ.DUTCH.value, 2)
            for iCiv in civilizations().majors().ids():
                if (
                    iCiv in Religions.lReformationNeighbours[Civ.DUTCH.value]
                    and self.rel.getReformationHitMatrix(iCiv) == 0
                ):
                    self.rel.setReformationHitMatrix(iCiv, 1)

        if iOwner < civilizations().majors().len():
            self.sta.onCityBuilt(iOwner, city.getX(), city.getY())

    def onCombatResult(self, argsList):
        self.vic.onCombatResult(argsList)
        self.sta.onCombatResult(argsList)

    def onReligionFounded(self, argsList):
        "Religion Founded"
        iReligion, iFounder = argsList

        if iReligion != Religion.JUDAISM.value:
            for city in utils.getCityList(iFounder):
                if city.isHolyCityByType(
                    iReligion
                ):  # Sedna: Protestant Shrine is now starting point for consistency with Religion.xml, Judaism is special
                    if iReligion == Religion.PROTESTANTISM.value:
                        iTemple = Building.PROTESTANT_TEMPLE.value
                        iShrine = Building.PROTESTANT_SHRINE.value
                    elif iReligion == Religion.ISLAM.value:
                        iTemple = Building.ISLAMIC_TEMPLE.value
                        iShrine = Building.ISLAMIC_SHRINE.value
                    elif iReligion == Religion.CATHOLICISM.value:
                        iTemple = Building.CATHOLIC_TEMPLE.value
                        iShrine = Building.CATHOLIC_SHRINE.value
                    elif iReligion == Religion.ORTHODOXY.value:
                        iTemple = Building.ORTHODOX_TEMPLE.value
                        iShrine = Building.ORTHODOX_SHRINE.value
                    if not city.isHasRealBuilding(iShrine):
                        city.setHasRealBuilding(iShrine, True)
                    if not city.isHasRealBuilding(iTemple):
                        city.setHasRealBuilding(iTemple, True)
                    break

        self.vic.onReligionFounded(iReligion, iFounder)

        if iFounder < civilizations().majors().len():
            self.sta.onReligionFounded(iFounder)

        # 3Miro: end Crusades for the Holy Land after the Reformation
        if iReligion == Religion.PROTESTANTISM.value:
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
        if iOwner == Civ.ARAGON.value and iBuildingType == Building.PALACE.value:
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
            if (
                iImprovement >= Improvement.COTTAGE.value
                and iImprovement <= Improvement.TOWN.value
            ):
                self.barb.onImprovementDestroyed(iPlotX, iPlotY)
        iVictim = pPlot.getOwner()
        if iVictim > -1 and iVictim < civilizations().majors().len():
            self.sta.onImprovementDestroyed(iVictim)

        self.vic.onPillageImprovement(
            pUnit.getOwner(), iVictim, iImprovement, iRoute, iPlotX, iPlotY
        )

    def onBeginGameTurn(self, argsList):
        iGameTurn = argsList[0]

        # Absinthe tests
        # if iGameTurn == DateTurn.i508AD:
        # 	for city in utils.getCityList(Civ.FRANCE.value):
        # 		plot = gc.getMap().plot(city.getX(),city.getY())

        # 	unitList = PyPlayer(Civ.FRANCE.value).getUnitList()
        # 	for unit in unitList:
        # 		iCargoSpace = unit.cargoSpace()

        # 	for iCiv in civilizations().majors().ids():
        # 		pCiv = gc.getPlayer(iCiv)
        # 		leaderName = pCiv.getLeader()
        # 		leaderName2 = gc.getLeaderHeadInfo( pCiv.getLeaderType() )
        # 		leaderName3 = leaderName2.getDescription()
        # 		leaderName4 = leaderName2.getLeaderHead()
        # 	#	leaderName5 = (pCiv.getLeaderType()).getLeaderID()
        # 	#	leaderName6 = leaderName2.getLeaderType()
        # 		leaderName7 = pCiv.getLeaderType()
        # 		LeaderType = gc.getLeaderHeadInfo(pCiv.getLeaderType()).getType()

        # for city in utils.getCityList(Civ.HUNGARY.value):
        # 	city.setBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_GRANARY"), CommerceTypes.COMMERCE_GOLD, 2)
        # 	city.setBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_CASTLE"), CommerceTypes.COMMERCE_GOLD, 12)
        # 	city.setBuildingYieldChange(gc.getInfoTypeForString("BUILDINGCLASS_GRANARY"), YieldTypes.YIELD_COMMERCE, 4)
        # 	city.setBuildingYieldChange(gc.getInfoTypeForString("BUILDINGCLASS_GRANARY"), YieldTypes.YIELD_FOOD, 2)
        # 	city.setBuildingYieldChange(gc.getInfoTypeForString("BUILDINGCLASS_CASTLE"), YieldTypes.YIELD_FOOD, 3)

        # 	for x in range(76):
        # 		plot = CyMap().plot(x, 46) # France, Paris included
        # 	for x in range(76):
        # 		plot = CyMap().plot(x, 36) # Hungary, accents

        # Absinthe: 868AD Viking attack on Constantinople
        if (
            iGameTurn
            == DateTurn.i860AD + sd.scriptDict["lEventRandomness"][iByzantiumVikingAttack] - 2
        ):
            if human() == Civ.BYZANTIUM.value:
                popup = Popup.PyPopup()
                popup.setBodyString(
                    localText.getText("TXT_KEY_EVENT_VIKING_CONQUERERS_RUMOURS", ())
                )
                popup.launch()

        if (
            iGameTurn
            == DateTurn.i860AD + sd.scriptDict["lEventRandomness"][iByzantiumVikingAttack]
        ):
            if human() == Civ.BYZANTIUM.value:
                self.barb.spawnMultiTypeUnits(
                    Civ.BARBARIAN.value,
                    (80, 24),
                    (80, 25),
                    [Unit.VIKING_BERSERKER.value, Unit.DENMARK_HUSKARL.value],
                    [4, 3],
                    iGameTurn,
                    1,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_VIKINGS", ()),
                )
                CyInterface().addMessage(
                    Civ.BYZANTIUM.value,
                    False,
                    MessageData.DURATION,
                    CyTranslator().getText("TXT_KEY_EVENT_VIKING_CONQUERERS_ARRIVE", ()),
                    "",
                    0,
                    "",
                    ColorTypes(MessageData.RED),
                    -1,
                    -1,
                    True,
                    True,
                )

        # Absinthe: Message for the human player about the Schism
        elif iGameTurn == DateTurn.i1053AD:
            if player().isExisting():
                sText = CyTranslator().getText("TXT_KEY_GREAT_SCHISM", ())
                CyInterface().addMessage(
                    human(),
                    False,
                    MessageData.DURATION,
                    sText,
                    "",
                    0,
                    "",
                    ColorTypes(MessageData.DARK_PINK),
                    -1,
                    -1,
                    True,
                    True,
                )

        # Absinthe: Remove the Great Lighthouse, message for the human player if the city is visible
        elif (
            iGameTurn
            == DateTurn.i1323AD - 40 + sd.scriptDict["lEventRandomness"][iLighthouseEarthQuake]
        ):
            for iPlayer in civilizations().drop(Civ.BARBARIAN).ids():
                bFound = 0
                for city in utils.getCityList(iPlayer):
                    if city.isHasBuilding(Wonder.GREAT_LIGHTHOUSE.value):
                        city.setHasRealBuilding(Wonder.GREAT_LIGHTHOUSE.value, False)
                        GLcity = city
                        bFound = 1
                if bFound and human() == iPlayer:
                    pPlayer = gc.getPlayer(iPlayer)
                    iTeam = pPlayer.getTeam()
                    if GLcity.isRevealed(iTeam, False):
                        CyInterface().addMessage(
                            iPlayer,
                            False,
                            MessageData.DURATION,
                            CyTranslator().getText(
                                "TXT_KEY_BUILDING_GREAT_LIGHTHOUSE_REMOVED", ()
                            ),
                            "",
                            0,
                            "",
                            ColorTypes(MessageData.RED),
                            -1,
                            -1,
                            True,
                            True,
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
        self.province.checkTurn(iGameTurn)
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

        ## Absinthe: refresh Dynamic Civ Names for all civs on the human player's initial turn of the given scenario
        ##			it's probably enough to refresh it on onGameStart for the scenario
        # if human() == iPlayer:
        # 	if iGameTurn == get_scenario_start_turn():
        # 		for iDCNPlayer in civilizations().majors().ids():
        # 			gc.getPlayer(iDCNPlayer).processCivNames()

        # Absinthe: Byzantine conqueror army
        if iGameTurn == DateTurn.i520AD:
            if iPlayer == Civ.BYZANTIUM.value:
                pByzantium = gc.getPlayer(Civ.BYZANTIUM.value)
                tStartingPlot = (59, 16)
                pByzantium.initUnit(
                    Unit.GALLEY.value,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GALLEY.value,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GALLEY.value,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GALLEY.value,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GALLEY.value,
                    tStartingPlot[0],
                    tStartingPlot[1],
                    UnitAITypes.UNITAI_ASSAULT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pByzantium.initUnit(
                    Unit.GREAT_GENERAL.value,
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
                        pUnit.setName(localText.getText("TXT_KEY_GREAT_PERSON_BELISARIUS", ()))
                utils.makeUnit(Unit.SWORDSMAN.value, Civ.BYZANTIUM.value, tStartingPlot, 4)
                utils.makeUnit(Unit.AXEMAN.value, Civ.BYZANTIUM.value, tStartingPlot, 3)
                utils.makeUnit(Unit.ARCHER.value, Civ.BYZANTIUM.value, tStartingPlot, 2)
                if iPlayer == iHuman:
                    popup = Popup.PyPopup()
                    popup.setBodyString(
                        localText.getText("TXT_KEY_EVENT_CONQUEROR_BELISARIUS", ())
                    )
                    popup.launch()

        # Absinthe: popup message a couple turns before the Seljuk/Mongol/Timurid invasions
        if iPlayer == iHuman:
            # Seljuks
            if iGameTurn == DateTurn.i1064AD - 7:
                if iPlayer == Civ.BYZANTIUM.value:
                    popup = Popup.PyPopup()
                    popup.setBodyString(
                        localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_START", ())
                    )
                    popup.launch()
            elif iGameTurn == DateTurn.i1094AD + 1:
                if iPlayer == Civ.BYZANTIUM.value:
                    popup = Popup.PyPopup()
                    sText = "Seljuk"
                    popup.setBodyString(
                        localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_END", (sText,))
                    )
                    popup.launch()
            # Mongols
            elif iGameTurn == DateTurn.i1236AD - 7:
                if iPlayer in [
                    Civ.KIEV.value,
                    Civ.HUNGARY.value,
                    Civ.POLAND.value,
                    Civ.BULGARIA.value,
                ]:
                    popup = Popup.PyPopup()
                    popup.setBodyString(
                        localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_START", ())
                    )
                    popup.launch()
            elif iGameTurn == DateTurn.i1288AD + 1:
                if iPlayer in [
                    Civ.KIEV.value,
                    Civ.HUNGARY.value,
                    Civ.POLAND.value,
                    Civ.BULGARIA.value,
                ]:
                    popup = Popup.PyPopup()
                    sText = "Tatar"
                    popup.setBodyString(
                        localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_END", (sText,))
                    )
                    popup.launch()
            # Timurids
            elif iGameTurn == DateTurn.i1380AD - 7:
                if iPlayer in [Civ.ARABIA.value, Civ.OTTOMAN.value, Civ.BYZANTIUM.value]:
                    popup = Popup.PyPopup()
                    popup.setBodyString(
                        localText.getText("TXT_KEY_EVENT_TIMURID_INVASION_START", ())
                    )
                    popup.launch()
            elif iGameTurn == DateTurn.i1431AD + 1:
                if iPlayer in [Civ.ARABIA.value, Civ.OTTOMAN.value, Civ.BYZANTIUM.value]:
                    popup = Popup.PyPopup()
                    sText = "Timurid"
                    popup.setBodyString(
                        localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_END", (sText,))
                    )
                    popup.launch()

        # Absinthe: Denmark UP
        if iPlayer == Civ.DENMARK.value:
            self.up.soundUP(iPlayer)

        # Absinthe: Aragonese UP
        # safety check: probably redundant, calls from onBuildingBuilt, onCityBuilt, onCityAcquired and onCityRazed should be enough
        elif iPlayer == Civ.ARAGON.value:
            self.up.confederationUP(iPlayer)

        # Ottoman UP
        if gc.hasUP(iPlayer, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS.value):
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
            # utils.setLastTurnAlive( iPlayer, iGameTurn )

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

        iHuman = human()

        self.vic.onTechAcquired(argsList[0], argsList[2])
        # self.res.onTechAcquired(argsList[0], argsList[2])

        if (
            gc.getPlayer(iPlayer).isAlive()
            and gc.getGame().getGameTurn() > civilization(iPlayer).date.birth
            and iPlayer < civilizations().majors().len()
        ):
            self.rel.onTechAcquired(argsList[0], argsList[2])
            self.sta.onTechAcquired(argsList[0], argsList[2])

    def onPreSave(self, argsList):
        "called before a game is actually saved"
        sd.save()  # edead: pickle & save script data

    # This method creates a new instance of the MercenaryUtils class to be used later
    def onLoadGame(self, argsList):
        sd.load()  # edead: load & unpickle script data
        DataLoader.setup()  # Absinthe: also needed on loading saved games
        # pass

        # if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(Technology.NATIONALISM.value)) and gc.getGame().getGameTurn() >= civilization(human()).date.birth):
        # if (gc.getGame().getGameTurn() >= civilization(human()).date.birth):

        # global objMercenaryUtils

        # objMercenaryUtils = MercenaryUtils.MercenaryUtils()

    # This method will redraw the main interface once a unit is promoted. This way the
    # gold/turn information will be updated.
    def onUnitPromoted(self, argsList):
        "Unit Promoted"

        self.mercs.onUnitPromoted(argsList)

        # if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(Technology.NATIONALISM.value)) and gc.getGame().getGameTurn() >= civilization(human()).date.birth):
        # if (gc.getGame().getGameTurn() >= civilization(human()).date.birth):
        # 	pUnit, iPromotion = argsList
        # 	player = PyPlayer(pUnit.getOwner())
        #
        # 	if (objMercenaryUtils.isMercenary(pUnit)):
        # 		CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)

    # This method will remove a mercenary unit from the game if it is killed
    def onUnitKilled(self, argsList):
        "Unit Killed"

        self.mercs.onUnitKilled(argsList)

        # if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(Technology.NATIONALISM.value)) and gc.getGame().getGameTurn() >= civilization(human()).date.birth):
        # if (gc.getGame().getGameTurn() >= civilization(human()).date.birth):

        # unit, iAttacker = argsList

        # mercenary = objMercenaryUtils.getMercenary(unit.getNameNoDesc())

        # if(mercenary != None and g_bDisplayMercenaryMessages and mercenary.getBuilder() != -1 and unit.isDead()):
        # strMessage = mercenary.getName() + " has died under " + gc.getPlayer(mercenary.getOwner()).getName() + "'s service."
        ## Inform the player that the mercenary has died.
        # CyInterface().addMessage(mercenary.getBuilder(), True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True)

        # objMercenaryUtils.removePlayerMercenary(unit)

    # This method will remove a mercenary unit from the game if it is lost
    def onUnitLost(self, argsList):
        "Unit Lost"

        self.mercs.onUnitLost(argsList)

    # This method handles the key input and will bring up the mercenary manager screen if the
    # player has at least one city and presses 'ctrl' and the 'M' key.
    def onKbdEvent(self, argsList):
        "keypress handler - return 1 if the event was consumed"

        iHuman = human()
        if gc.getGame().getGameTurn() >= civilization(iHuman).date.birth:

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

            iGameTurn = gc.getGame().getGameTurn()
            pass

        if (
            eventType == self.EventKeyDown
            and theKey == int(InputTypes.KB_N)
            and self.eventManager.bAlt
        ):
            # self.printEmbassyDebug()
            self.printPlotsDebug()
            # self.printStabilityDebug()

        if (
            eventType == self.EventKeyDown
            and theKey == int(InputTypes.KB_E)
            and self.eventManager.bAlt
            and self.eventManager.bShift
        ):
            # picks a dead civ so that autoplay can be started with game.AIplay xx
            iDebugDeadCiv = Civ.BURGUNDY.value  # always dead in 500AD
            # 3Miro: not sure
            # gc.getTeam(gc.getPlayer(iDebugDeadCiv).getTeam()).setHasTech(Technology.CALENDAR.value, True, iDebugDeadCiv, False, False)
            utils.makeUnit(Unit.AXEMAN.value, iDebugDeadCiv, (0, 0), 1)
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
            # engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS)

            # cache the plot's coords
            self.lastProvinceID = PROVINCES_MAP[plot.getY()][plot.getX()]

            # select an appropriate color
            if PROVINCES_MAP[plot.getY()][plot.getX()] == -1:  # ocean and non-province tiles
                return
            else:
                iLevel = utils.getProvinceStabilityLevel(iHuman, iProvinceID)
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

    def printDebug(self, iGameTurn):
        pass

    def printPlotsDebug(self):
        pass

    def printEmbassyDebug(self):
        pass

    def printStabilityDebug(self):
        for iCiv in civilizations().majors().ids():
            if gc.getPlayer(iCiv).isAlive():
                print(
                    "Base:",
                    utils.getBaseStabilityLastTurn(iCiv),
                    "Modifier:",
                    utils.getStability(iCiv) - utils.getBaseStabilityLastTurn(iCiv),
                    "Total:",
                    utils.getStability(iCiv),
                    "civic",
                    gc.getPlayer(iCiv).getCivics(5),
                    gc.getPlayer(iCiv).getCivilizationDescription(0),
                )

        for i in civilizations().majors().ids():
            print(
                gc.getPlayer(i).getCivilizationShortDescription(0),
                "PLOT OWNERSHIP ABROAD:",
                self.sta.getOwnedPlotsLastTurn(i),
                "CITY OWNERSHIP LOST:",
                self.sta.getOwnedCitiesLastTurn(i),
            )
