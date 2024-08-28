# Rhye's and Fall of Civilization: Europe - Event handler

from CvPythonExtensions import *
from Core import (
    civilization,
    civilizations,
    message,
    human,
    make_unit,
    make_units,
    player,
    show,
    text,
    turn,
    year,
    cities,
)
import CvUtil
import PyHelpers
import CvMercenaryManager  # Mercenaries
import CvScreenEnums  # Mercenaries

from StoredData import data
import RiseAndFall
import Barbs
import Religions
import Resources
import UniquePowers
import AIWars
from RFCUtils import forcedInvasion, getProvinceStabilityLevel

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

from Consts import MessageData
from ProvinceMapData import PROVINCES_MAP
from CoreTypes import (
    Civ,
    Improvement,
    UniquePower,
    Unit,
    Wonder,
)

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
        return 0

    def onPreSave(self, argsList):
        "called before a game is actually saved"
        return 0

    # This method creates a new instance of the MercenaryUtils class to be used later
    def onLoadGame(self, argsList):
        data.load()  # edead: load & unpickle script data
        Locations.setup()
        Modifiers.setup()
        Civilizations.setup()

    def onCityAcquired(self, argsList):
        "City Acquired"
        return 0

    def onCityAcquiredAndKept(self, argsList):
        "City Acquired and Kept"
        return 0

    def onCityRazed(self, argsList):
        "City Razed"
        return 0

    def onCityBuilt(self, argsList):
        "City Built"
        return 0

    def onCombatResult(self, argsList):
        return 0

    def onReligionFounded(self, argsList):
        "Religion Founded"
        return 0

    def onBuildingBuilt(self, argsList):
        return 0

    def onProjectBuilt(self, argsList):
        return 0

    def onUnitPillage(self, argsList):
        pUnit, iImprovement, iRoute, iOwner = argsList
        iPlotX = pUnit.getX()
        iPlotY = pUnit.getY()
        pPlot = CyMap().plot(iPlotX, iPlotY)
        if pPlot.countTotalCulture() == 0:
            if iImprovement >= Improvement.COTTAGE and iImprovement <= Improvement.TOWN:
                Barbs.onImprovementDestroyed(iPlotX, iPlotY)
        iVictim = pPlot.getOwner()
        if iVictim > -1 and iVictim < civilizations().majors().len():
            Stability.onImprovementDestroyed(iVictim)

        Victory.onPillageImprovement(
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
                    Barbs.spawnUnits(
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

        Barbs.checkTurn(iGameTurn)
        RiseAndFall.checkTurn(iGameTurn)
        Religions.checkTurn(iGameTurn)
        Resources.checkTurn(iGameTurn)
        UniquePowers.checkTurn(iGameTurn)
        AIWars.checkTurn(iGameTurn)
        Plague.checkTurn(iGameTurn)
        Victory.checkTurn(iGameTurn)
        Stability.checkTurn(iGameTurn)
        Crusades.checkTurn(iGameTurn)
        Provinces.checkTurn(iGameTurn)
        Companies.checkTurn(iGameTurn)

        return 0

    def onBeginPlayerTurn(self, argsList):
        iGameTurn, iPlayer = argsList
        iHuman = human()
        if RiseAndFall.getDeleteMode(0) != -1:
            RiseAndFall.deleteMode(iPlayer)
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
            UniquePowers.soundUP(iPlayer)

        # Absinthe: Aragonese UP
        # safety check: probably redundant, calls from onBuildingBuilt, onCityBuilt, onCityAcquired and onCityRazed should be enough
        elif iPlayer == Civ.ARAGON:
            UniquePowers.confederationUP(iPlayer)

        # Ottoman UP
        if gc.hasUP(iPlayer, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS):
            UniquePowers.janissaryDraftUP(iPlayer)

        Plague.checkPlayerTurn(iGameTurn, iPlayer)
        Victory.checkPlayerTurn(iGameTurn, iPlayer)

        if gc.getPlayer(iPlayer).isAlive() and iPlayer < civilizations().majors().len():
            if gc.getPlayer(iPlayer).getNumCities() > 0:
                Stability.updateBaseStability(iGameTurn, iPlayer)

            # for the AI only, leader switch and cheats
            if iPlayer != iHuman:
                RiseAndFall.checkPlayerTurn(iGameTurn, iPlayer)

            # not really needed, we set it on collapse anyway
            # setLastTurnAlive( iPlayer, iGameTurn )

        Crusades.checkPlayerTurn(iGameTurn, iPlayer)

    def onEndPlayerTurn(self, argsList):
        """Called at the end of a players turn"""
        # 3Miro does not get called
        iGameTurn, iPlayer = argsList

    def onEndGameTurn(self, argsList):
        iGameTurn = argsList[0]
        Stability.checkImplosion(iGameTurn)
        Mercenaries.doMercsTurn(iGameTurn)

    def onReligionSpread(self, argsList):
        iReligion, iOwner, pSpreadCity = argsList
        Stability.onReligionSpread(iReligion, iOwner)
        Religions.onReligionSpread(iReligion, iOwner)

    def onFirstContact(self, argsList):

        iTeamX, iHasMetTeamY = argsList
        RiseAndFall.onFirstContact(iTeamX, iHasMetTeamY)

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
            Religions.onPlayerChangeAllCivics(iPlayer, lNewCivics, lOldCivics)

    def onPlayerChangeSingleCivic(self, argsList):
        # note that this reports all civic changes in single instances (so also reports force converts by diplomacy or with spies)
        "Civics are changed for a player"
        iPlayer, iNewCivic, iOldCivic = argsList

    def onPlayerChangeStateReligion(self, argsList):
        "Player changes his state religion"
        iPlayer, iNewReligion, iOldReligion = argsList

        if iPlayer < civilizations().majors().len():
            Companies.onPlayerChangeStateReligion(argsList)

    def onTechAcquired(self, argsList):
        iPlayer = argsList[2]
        Victory.onTechAcquired(argsList[0], argsList[2])

        if (
            gc.getPlayer(iPlayer).isAlive()
            and turn() > civilization(iPlayer).date.birth
            and iPlayer < civilizations().majors().len()
        ):
            Religions.onTechAcquired(argsList[0], argsList[2])
            Stability.onTechAcquired(argsList[0], argsList[2])

    # This method will redraw the main interface once a unit is promoted. This way the
    # gold/turn information will be updated.
    def onUnitPromoted(self, argsList):
        "Unit Promoted"

        Mercenaries.onUnitPromoted(argsList)

    # This method will remove a mercenary unit from the game if it is killed
    def onUnitKilled(self, argsList):
        "Unit Killed"

        Mercenaries.onUnitKilled(argsList)

    # This method will remove a mercenary unit from the game if it is lost
    def onUnitLost(self, argsList):
        "Unit Lost"

        Mercenaries.onUnitLost(argsList)

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
