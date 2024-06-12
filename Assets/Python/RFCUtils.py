# Rhye's and Fall of Civilization: Europe - Utilities

from CvPythonExtensions import *
from Core import (
    city,
    civilization,
    civilizations,
    get_religion_by_id,
    human,
    location,
    make_unit,
    make_units,
    message,
    name,
    player,
    symbol,
    team,
    teamtype,
    text,
    text_if_exists,
    turn,
    units,
    cities,
    plots,
    get_data_from_upside_down_map,
)
from CoreTypes import (
    City,
    Civ,
    FaithPointBonusCategory,
    PlagueType,
    Religion,
    Scenario,
    SpecialParameter,
    StabilityCategory,
    UniquePower,
    Wonder,
    Promotion,
    Terrain,
    Technology,
    Unit,
    Feature,
)
import CvUtil
import CvScreenEnums
from LocationsData import CITIES
import Popup
from PyUtils import percentage, percentage_chance, rand
from ReligionData import RELIGION_PERSECUTION_ORDER
from Scenario import get_scenario
from SettlerMapData import SETTLERS_MAP
from StoredData import data
from MiscData import GREAT_PROPHET_FAITH_POINT_BONUS

from CoreTypes import ProvinceType
from ProvinceMapData import PROVINCES_MAP
from Consts import MINOR_CIVS, WORLD_HEIGHT, MessageData

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()


tCol = ("255,255,255", "200,200,200", "150,150,150", "128,128,128")

iScreenIsUp = 0
iSelectedCivID = -1

bStabilityOverlay = False


# RiseAndFall, Stability
def getLastTurnAlive(iCiv):
    return data.lLastTurnAlive[iCiv]


def setLastTurnAlive(iCiv, iNewValue):
    data.lLastTurnAlive[iCiv] = iNewValue


def getLastRespawnTurn(iCiv):
    return data.lLastRespawnTurn[iCiv]


def setLastRespawnTurn(iCiv, iNewValue):
    data.lLastRespawnTurn[iCiv] = iNewValue


# Stability
def getTempFlippingCity():
    return data.iTempFlippingCity


def setTempFlippingCity(tNewValue):
    data.iTempFlippingCity = tNewValue


def getProsecutionCount(iCiv):
    return gc.getProsecutionCount(iCiv)


def setProsecutionCount(iCiv, iNewValue):
    gc.setProsecutionCount(iCiv, iNewValue)


# Plague
def getPlagueCountdown(iCiv):
    return data.lPlagueCountdown[iCiv]


def setPlagueCountdown(iCiv, iNewValue):
    data.lPlagueCountdown[iCiv] = iNewValue


# Victory
def countAchievedGoals(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    iResult = 0
    for j in range(3):
        iTemp = pPlayer.getUHV(j)
        if iTemp < 0:
            iTemp = 0
        iResult += iTemp
    return iResult


def getGoalsColor(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    iCol = 0
    for j in range(3):
        if pPlayer.getUHV(j) == 0:
            iCol += 1
    return tCol[iCol]


# Plague, UP
def isMortalUnit(unit):
    # Absinthe: leader units, and great people won't be killed by the plague
    if unit.isHasPromotion(Promotion.LEADER):
        if not gc.getPlayer(unit.getOwner()).isHuman():
            return False
    iUnitType = unit.getUnitType()
    if Unit.GREAT_PROPHET <= iUnitType <= Unit.GREAT_SPY:
        return False
    return True


# AIWars
def checkUnitsInEnemyTerritory(iCiv1, iCiv2):
    unitList = units().owner(iCiv1).entities()
    if unitList:
        for unit in unitList:
            iX = unit.getX()
            iY = unit.getY()
            if gc.getMap().plot(iX, iY).getOwner() == iCiv2:
                return True
    return False


# AIWars
def restorePeaceAI(iMinorCiv, bOpenBorders):
    teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
    for iActiveCiv in civilizations().majors().ids():
        if gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman():
            if teamMinor.isAtWar(iActiveCiv):
                bActiveUnitsInIndependentTerritory = checkUnitsInEnemyTerritory(
                    iActiveCiv, iMinorCiv
                )
                bIndependentUnitsInActiveTerritory = checkUnitsInEnemyTerritory(
                    iMinorCiv, iActiveCiv
                )
                if (
                    not bActiveUnitsInIndependentTerritory
                    and not bIndependentUnitsInActiveTerritory
                ):
                    teamMinor.makePeace(iActiveCiv)
                    if bOpenBorders:
                        teamMinor.signOpenBorders(iActiveCiv)


# AIWars
def restorePeaceHuman(iMinorCiv):
    teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
    for iActiveCiv in civilizations().majors().ids():
        if gc.getPlayer(iActiveCiv).isHuman():
            if gc.getPlayer(iActiveCiv).isAlive():
                if teamMinor.isAtWar(iActiveCiv):
                    bActiveUnitsInIndependentTerritory = checkUnitsInEnemyTerritory(
                        iActiveCiv, iMinorCiv
                    )
                    bIndependentUnitsInActiveTerritory = checkUnitsInEnemyTerritory(
                        iMinorCiv, iActiveCiv
                    )
                    if (
                        not bActiveUnitsInIndependentTerritory
                        and not bIndependentUnitsInActiveTerritory
                    ):
                        teamMinor.makePeace(iActiveCiv)
            return


# AIWars
def minorWars(iMinorCiv, iGameTurn):
    teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
    for city in cities().owner(iMinorCiv).entities():
        x = city.getX()
        y = city.getY()
        for iActiveCiv in civilizations().majors().ids():
            if (
                gc.getPlayer(iActiveCiv).isAlive()
                and not gc.getPlayer(iActiveCiv).isHuman()
                and not iActiveCiv == Civ.POPE
            ):
                if not teamMinor.isAtWar(iActiveCiv):
                    if iGameTurn > civilization(iActiveCiv).date.birth + 20:
                        # Absinthe: probably better to use war maps instead of settler maps, but let the AI concentrate on it's core area first
                        # maybe we should use both settler and war maps? distance calculations would be great, but use too much iterations
                        random_value = percentage()
                        war_map_value = player(iActiveCiv).getWarsMaps(WORLD_HEIGHT - y - 1, x)
                        if (
                            (random_value < 30 and war_map_value >= 2)
                            or (random_value < 70 and war_map_value >= 6)
                            or war_map_value >= 99
                        ):
                            team(iActiveCiv).declareWar(
                                iMinorCiv, False, WarPlanTypes.WARPLAN_LIMITED
                            )


# AIWars
# Absinthe: declare war sooner / more frequently if an Indy city has huge value on the civ's war map
def minorCoreWars(iMinorCiv, iGameTurn):
    teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
    for city in cities().owner(iMinorCiv).entities():
        x = city.getX()
        y = city.getY()
        for iActiveCiv in civilizations().majors().ids():
            if (
                gc.getPlayer(iActiveCiv).isAlive()
                and not gc.getPlayer(iActiveCiv).isHuman()
                and not iActiveCiv == Civ.POPE
            ):
                # Absinthe: do not want to force the AI into these wars with WARPLAN_TOTAL too early
                if iGameTurn > civilization(iActiveCiv).date.birth + 40:
                    if not teamMinor.isAtWar(iActiveCiv):
                        if gc.getPlayer(iActiveCiv).getWarsMaps(WORLD_HEIGHT - y - 1, x) == 16:
                            teamActive = gc.getTeam(gc.getPlayer(iActiveCiv).getTeam())
                            teamActive.declareWar(iMinorCiv, False, WarPlanTypes.WARPLAN_TOTAL)


# RiseAndFall, Stability
def calculateDistance(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return max(dx, dy)


# RiseAndFall
def updateMinorTechs(iMinorCiv, iMajorCiv):
    for t in range(len(Technology)):
        if gc.getTeam(gc.getPlayer(iMajorCiv).getTeam()).isHasTech(t):
            gc.getTeam(gc.getPlayer(iMinorCiv).getTeam()).setHasTech(
                t, True, iMinorCiv, False, False
            )


# RiseAndFall
# Absinthe: separate city flip rules for secession and minor nation mechanics
def flipUnitsInCitySecession(tCityPlot, iNewOwner, iOldOwner):
    plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
    city = plotCity.getPlotCity()
    iNumUnitsInAPlot = plotCity.getNumUnits()
    j = 0  # Absinthe: index for remaining units in the plot
    k = 0  # Absinthe: counter for all units from the original owner

    # Absinthe: one free defender unit
    pPlayer = gc.getPlayer(iOldOwner)
    iFreeDefender = Unit.ARCHER
    lUnits = [
        Unit.LINE_INFANTRY,
        Unit.MUSKETMAN,
        Unit.LONGBOWMAN,
        Unit.ARBALEST,
        Unit.CROSSBOWMAN,
    ]
    for iUnit in lUnits:
        if pPlayer.canTrain(getUniqueUnit(iNewOwner, iUnit), False, False):
            iFreeDefender = getUniqueUnit(iNewOwner, iUnit)
            break
    make_unit(iNewOwner, iFreeDefender, (28, 0))

    for i in range(iNumUnitsInAPlot):
        unit = plotCity.getUnit(j)
        unitType = unit.getUnitType()
        bSafeUnit = False
        if unit.getOwner() == iOldOwner:
            # Absinthe: # no civilian units will flip on city secession
            lNoFlip = [
                Unit.SETTLER,
                Unit.GREAT_PROPHET,
                Unit.GREAT_ARTIST,
                Unit.GREAT_SCIENTIST,
                Unit.GREAT_MERCHANT,
                Unit.GREAT_ENGINEER,
                Unit.GREAT_GENERAL,
                Unit.GREAT_SPY,
            ]
            for i in range(0, len(lNoFlip)):
                if lNoFlip[i] == unitType:
                    bSafeUnit = True
            if not bSafeUnit:
                # Absinthe: instead of switching all units to indy, only 60% chance that the unit will defect
                #             the first unit from the old owner should always defect though
                k += 1
                if k < 2 or percentage_chance(60, strict=True):
                    unit.kill(False, Civ.BARBARIAN)
                    make_unit(iNewOwner, unitType, (28, 0))
                # Absinthe: skip unit if it won't defect, so it will move out of the city territory
                else:
                    j += 1
            # Absinthe: skip unit if civilian
            else:
                j += 1
        # Absinthe: skip unit if from another player
        else:
            j += 1


# RiseAndFall
# Absinthe: this is for city flips connected to spawn, collapse and respawn mechanics
def flipUnitsInCityBefore(tCityPlot, iNewOwner, iOldOwner):
    plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
    city = plotCity.getPlotCity()
    iNumUnitsInAPlot = plotCity.getNumUnits()
    j = 0  # Absinthe: index for remaining units in the plot
    for i in range(iNumUnitsInAPlot):
        unit = plotCity.getUnit(j)
        unitType = unit.getUnitType()
        if unit.getOwner() == iOldOwner:
            unit.kill(False, Civ.BARBARIAN)
            if (
                iNewOwner < civilizations().majors().len() or unitType > Unit.SETTLER
            ):  # Absinthe: major players can even flip settlers (spawn/respawn mechanics)
                make_unit(iNewOwner, unitType, (28, 0))
        # Absinthe: skip unit if from another player
        else:
            j += 1


# RiseAndFall
def flipUnitsInCityAfter(tCityPlot, iCiv):
    # moves new units back in their place
    tempPlot = gc.getMap().plot(28, 0)
    if tempPlot.getNumUnits() != 0:
        iNumUnitsInAPlot = tempPlot.getNumUnits()
        for i in range(iNumUnitsInAPlot):
            unit = tempPlot.getUnit(0)
            unit.setXYOld(tCityPlot[0], tCityPlot[1])
    # cover revealed plots
    gc.getMap().plot(27, 0).setRevealed(iCiv, False, True, -1)
    gc.getMap().plot(28, 0).setRevealed(iCiv, False, True, -1)
    gc.getMap().plot(29, 0).setRevealed(iCiv, False, True, -1)
    gc.getMap().plot(27, 1).setRevealed(iCiv, False, True, -1)
    gc.getMap().plot(28, 1).setRevealed(iCiv, False, True, -1)
    gc.getMap().plot(29, 1).setRevealed(iCiv, False, True, -1)

    # Absinthe: if there are no units in the city after the flip, add a free defender
    cityPlot = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
    if cityPlot.getNumUnits() == 0:
        # The latest available ranged/gun class
        RangedClass = getUniqueUnit(iCiv, Unit.ARCHER)
        lRangedList = [
            Unit.LINE_INFANTRY,
            Unit.MUSKETMAN,
            Unit.LONGBOWMAN,
            Unit.ARBALEST,
            Unit.CROSSBOWMAN,
            Unit.ARCHER,
        ]
        for iUnit in lRangedList:
            if gc.getPlayer(iCiv).canTrain(getUniqueUnit(iCiv, iUnit), False, False):
                RangedClass = getUniqueUnit(iCiv, iUnit)
                break
        make_unit(iCiv, RangedClass, tCityPlot)


def killAllUnitsInArea(tTopLeft, tBottomRight):
    for plot in plots().rectangle(tTopLeft, tBottomRight).entities():
        iNumUnitsInAPlot = plot.getNumUnits()
        if iNumUnitsInAPlot > 0:
            for i in range(iNumUnitsInAPlot):
                unit = plot.getUnit(0)
                unit.kill(False, Civ.BARBARIAN)


def killUnitsInPlots(lPlots, iCiv):
    for (x, y) in lPlots:
        killPlot = gc.getMap().plot(x, y)
        iNumUnitsInAPlot = killPlot.getNumUnits()
        if iNumUnitsInAPlot > 0:
            iSkippedUnit = 0
            for i in range(iNumUnitsInAPlot):
                unit = killPlot.getUnit(iSkippedUnit)
                if unit.getOwner() == iCiv:
                    unit.kill(False, Civ.BARBARIAN)
                else:
                    iSkippedUnit += 1


# RiseAndFall
# Absinthe: create units at (28, 0), in the unreachable desert area, near the autoplay plot
def flipUnitsInArea(tTopLeft, tBottomRight, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
    """Deletes, recreates units in 28, 0 and moves them to the previous tile.
    If there are units belonging to others in that plot and the new owner is barbarian, the units aren't recreated.
    Settlers aren't created.
    If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
    # Absinthe: safety check, kill all units on the tempplot before the flip
    killPlot = gc.getMap().plot(28, 0)
    iNumUnitsInAPlot = killPlot.getNumUnits()
    if iNumUnitsInAPlot > 0:
        for i in range(iNumUnitsInAPlot):
            unit = killPlot.getUnit(0)
            unit.kill(False, Civ.BARBARIAN)
    for plot in plots().rectangle(tTopLeft, tBottomRight).entities():
        iNumUnitsInAPlot = plot.getNumUnits()
        if iNumUnitsInAPlot > 0:
            bRevealedZero = False
            if gc.getMap().plot(28, 0).isRevealed(gc.getPlayer(iNewOwner).getTeam(), False):
                bRevealedZero = True
            if bSkipPlotCity and plot.isCity():
                pass
            else:
                j = 0
                for i in range(iNumUnitsInAPlot):
                    unit = plot.getUnit(j)
                    if unit.getOwner() == iOldOwner:
                        unit.kill(False, Civ.BARBARIAN)
                        if bKillSettlers:
                            if unit.getUnitType() > Unit.SETTLER:
                                make_unit(iNewOwner, unit.getUnitType(), (28, 0))
                        else:
                            if unit.getUnitType() >= Unit.SETTLER:  # skip animals
                                make_unit(iNewOwner, unit.getUnitType(), (28, 0))
                    else:
                        j += 1
                tempPlot = gc.getMap().plot(28, 0)
                # moves new units back in their place
                if tempPlot.getNumUnits() != 0:
                    iNumUnitsInAPlot = tempPlot.getNumUnits()
                    for i in range(iNumUnitsInAPlot):
                        unit = tempPlot.getUnit(0)
                        unit.setXYOld(*location(plot))
                    iCiv = iNewOwner
                    if not bRevealedZero:
                        gc.getMap().plot(27, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(28, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(29, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(27, 1).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(28, 1).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(29, 1).setRevealed(iCiv, False, True, -1)


# RiseAndFall
# Absinthe: similar to the function above, but flips on a list of plots
def flipUnitsInPlots(lPlots, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
    """Deletes, recreates units in 28, 0 and moves them to the previous tile.
    If there are units belonging to others in that plot and the new owner is barbarian, the units aren't recreated.
    Settlers aren't created.
    If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
    # Absinthe: safety check, kill all units on the tempplot before the flip
    killPlot = gc.getMap().plot(28, 0)
    iNumUnitsInAPlot = killPlot.getNumUnits()
    if iNumUnitsInAPlot > 0:
        for i in range(iNumUnitsInAPlot):
            unit = killPlot.getUnit(0)
            unit.kill(False, Civ.BARBARIAN)
    for (x, y) in lPlots:
        killPlot = gc.getMap().plot(x, y)
        iNumUnitsInAPlot = killPlot.getNumUnits()
        if iNumUnitsInAPlot > 0:
            bRevealedZero = False
            if gc.getMap().plot(28, 0).isRevealed(gc.getPlayer(iNewOwner).getTeam(), False):
                bRevealedZero = True
            if bSkipPlotCity and killPlot.isCity():
                pass
            else:
                j = 0
                for i in range(iNumUnitsInAPlot):
                    unit = killPlot.getUnit(j)
                    if unit.getOwner() == iOldOwner:
                        unit.kill(False, Civ.BARBARIAN)
                        if bKillSettlers:
                            if unit.getUnitType() > Unit.SETTLER:
                                make_unit(iNewOwner, unit.getUnitType(), (28, 0))
                        else:
                            if unit.getUnitType() >= Unit.SETTLER:  # skip animals
                                make_unit(iNewOwner, unit.getUnitType(), (28, 0))
                    else:
                        j += 1
                tempPlot = gc.getMap().plot(28, 0)
                # moves new units back in their place
                if tempPlot.getNumUnits() > 0:
                    iNumUnitsInAPlot = tempPlot.getNumUnits()
                    for i in range(iNumUnitsInAPlot):
                        unit = tempPlot.getUnit(0)
                        unit.setXYOld(x, y)
                    iCiv = iNewOwner
                    if not bRevealedZero:
                        gc.getMap().plot(27, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(28, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(29, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(27, 1).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(28, 1).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(29, 1).setRevealed(iCiv, False, True, -1)


# RiseAndFall
def flipCity(tCityPlot, bConquest, bKillUnits, iNewOwner, lOldOwners):
    """Changes owner of city specified by tCityPlot.
    bConquest specifies if it's conquered or traded.
    If bKillUnits != 0 all the units in the city will be killed.
    lOldOwners is a list. Flip happens only if the old owner is in the list.
    An empty list will cause the flip to always happen."""
    pNewOwner = player(iNewOwner)
    x, y = location(tCityPlot)
    flipCity = city(x, y)

    if flipCity:
        iOldOwner = flipCity.getOwner()
        if not lOldOwners or iOldOwner in lOldOwners:

            if bKillUnits:
                for unit in units().at(x, y).filter(lambda unit: not unit.isCargo()).entities():
                    unit.kill(False, iNewOwner)

            pNewOwner.acquireCity(flipCity, bConquest, not bConquest)

            flippedCity = city(x, y)
            # flippedCity.setInfoDirty(True) # TODO: add these to CyCity
            # flippedCity.setLayoutDirty(True)

            # Absinthe: if there are mercs available in the new city's province, interface message about it to the human player
            for lMerc in data.lMercGlobalPool:
                if lMerc[4] == flippedCity.getProvince():
                    if iNewOwner == human():
                        szProvName = "TXT_KEY_PROVINCE_NAME_%i" % lMerc[4]
                        szCurrentProvince = text(szProvName)
                        message(
                            iNewOwner,
                            text(
                                "TXT_KEY_MERC_AVAILABLE_IN_PROVINCE_OF_NEW_CITY", szCurrentProvince
                            ),
                            button=ArtFileMgr.getInterfaceArtInfo(
                                "INTERFACE_MERCENARY_ICON"
                            ).getPath(),
                            color=MessageData.LIME,
                            location=flippedCity,
                        )
                        break

            return flippedCity

    return None


# RiseAndFall
def cultureManager(
    tCityPlot,
    iCulturePercent,
    iNewOwner,
    iOldOwner,
    bBarbarian2x2Decay,
    bBarbarian2x2Conversion,
    bAlwaysOwnPlots,
):
    """Converts the culture of the city and of the surrounding plots to the new owner of a city.
    iCulturePercent determine the percentage that goes to the new owner.
    If old owner is barbarian, all the culture is converted"""

    pCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
    city = pCity.getPlotCity()

    # city
    if pCity.isCity():
        iCurrentCityCulture = city.getCulture(iOldOwner)
        if iNewOwner != Civ.BARBARIAN:
            city.setCulture(Civ.BARBARIAN, 0, True)

        # Absinthe: changeCulture instead of setCulture for the new civ, so previously acquired culture won't disappear
        #             for the old civ some of the culture is lost when the city is conquered
        #             note that this is the amount of culture "resource" for each civ, not population percent
        city.changeCulture(iNewOwner, iCurrentCityCulture * iCulturePercent / 100, False)
        # Absinthe: only half of the amount is lost, so only 25% on city secession and minor nation revolts
        city.setCulture(
            iOldOwner, iCurrentCityCulture * (100 - (iCulturePercent / 2)) / 100, False
        )

        if city.getCulture(iNewOwner) <= 10:
            city.setCulture(iNewOwner, 10, False)

    # halve barbarian culture in a broader area
    if bBarbarian2x2Decay or bBarbarian2x2Conversion:
        if iNewOwner not in MINOR_CIVS:
            for plot in plots().surrounding(tCityPlot, radius=2).entities():
                for iMinor in MINOR_CIVS:
                    iPlotMinorCulture = plot.getCulture(iMinor)
                    if iPlotMinorCulture > 0:
                        if plot.isNone() or location(plot) == tCityPlot:
                            if bBarbarian2x2Decay:
                                plot.setCulture(iMinor, iPlotMinorCulture / 4, True)
                            if bBarbarian2x2Conversion:
                                plot.setCulture(iMinor, 0, True)
                                # Absinthe: changeCulture instead of setCulture for the new civ, so previously acquired culture won't disappear
                                plot.changeCulture(iNewOwner, iPlotMinorCulture, True)

    # plot
    for plot in plots().surrounding(tCityPlot).entities():
        iCurrentPlotCulture = plot.getCulture(iOldOwner)

        if plot.isCity():
            # Absinthe: changeCulture instead of setCulture for the new civ, so previously acquired culture won't disappear
            plot.changeCulture(iNewOwner, iCurrentPlotCulture * iCulturePercent / 100, True)
            # Absinthe: only half of the amount is lost
            plot.setCulture(
                iOldOwner, iCurrentPlotCulture * (100 - iCulturePercent / 2) / 100, True
            )
        else:
            # Absinthe: changeCulture instead of setCulture for the new civ, so previously acquired culture won't disappear
            plot.changeCulture(iNewOwner, iCurrentPlotCulture * iCulturePercent / 3 / 100, True)
            # Absinthe: only half of the amount is lost
            plot.setCulture(
                iOldOwner, iCurrentPlotCulture * (100 - iCulturePercent / 6) / 100, True
            )

        if not plot.isCity():
            if bAlwaysOwnPlots:
                plot.setOwner(iNewOwner)
            else:
                if plot.getCulture(iNewOwner) * 4 > plot.getCulture(iOldOwner):
                    plot.setOwner(iNewOwner)


# RFCEventHandler
def spreadMajorCulture(iMajorCiv, iX, iY):
    # Absinthe: spread some of the major civ's culture to the nearby indy cities
    for city in plots().surrounding((iX, iY), radius=4).cities().entities():
        previous_owner = city.getPreviousOwner()
        if previous_owner in MINOR_CIVS:
            iDen = 25
            if get_data_from_upside_down_map(SETTLERS_MAP, iMajorCiv, city) >= 400:
                iDen = 10
            elif get_data_from_upside_down_map(SETTLERS_MAP, iMajorCiv, city) >= 150:
                iDen = 15

            # Absinthe: changeCulture instead of setCulture, otherwise previous culture will be lost
            iMinorCityCulture = city.getCulture(previous_owner)
            city.changeCulture(iMajorCiv, iMinorCityCulture / iDen, True)

            iMinorPlotCulture = city.getCulture(previous_owner)
            city.changeCulture(iMajorCiv, iMinorPlotCulture / iDen, True)


# UniquePowers, Crusades, RiseAndFall
def convertPlotCulture(pCurrent, iCiv, iPercent, bOwner):
    if pCurrent.isCity():
        city = pCurrent.getPlotCity()
        iCivCulture = city.getCulture(iCiv)
        iLoopCivCulture = 0
        for civ in civilizations().drop(Civ.BARBARIAN).ids():
            if civ != iCiv:
                iLoopCivCulture += city.getCulture(civ)
                city.setCulture(civ, city.getCulture(civ) * (100 - iPercent) / 100, True)
        city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

    iCivCulture = pCurrent.getCulture(iCiv)
    iLoopCivCulture = 0
    for civ in civilizations().drop(Civ.BARBARIAN).ids():
        if civ != iCiv:
            iLoopCivCulture += pCurrent.getCulture(civ)
            pCurrent.setCulture(civ, pCurrent.getCulture(civ) * (100 - iPercent) / 100, True)
    pCurrent.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)
    if bOwner:
        pCurrent.setOwner(iCiv)


# RiseAndFall
def pushOutGarrisons(tCityPlot, iOldOwner):
    tDestination = (-1, -1)
    for plot in (
        plots().surrounding(tCityPlot, radius=2).passable().land().owner(iOldOwner).entities()
    ):
        tDestination = location(plot)
        break
    if tDestination != (-1, -1):
        plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
        iNumUnitsInAPlot = plotCity.getNumUnits()
        j = 0
        for i in range(iNumUnitsInAPlot):
            unit = plotCity.getUnit(j)
            if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
                unit.setXYOld(tDestination[0], tDestination[1])
            else:
                j = j + 1


# RiseAndFall
def relocateSeaGarrisons(tCityPlot, iOldOwner):
    tDestination = (-1, -1)
    for city in cities().owner(iOldOwner).entities():
        if city.isCoastalOld():
            tDestination = (city.getX(), city.getY())
            break
    if tDestination == (-1, -1):
        for plot in plots().surrounding(tCityPlot, radius=12).water().entities():
            tDestination = location(plot)
            break
    if tDestination != (-1, -1):
        plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
        iNumUnitsInAPlot = plotCity.getNumUnits()
        j = 0
        for i in range(iNumUnitsInAPlot):
            unit = plotCity.getUnit(j)
            if unit.getDomainType() == DomainTypes.DOMAIN_SEA:
                unit.setXYOld(tDestination[0], tDestination[1])
            else:
                j = j + 1


# RiseAndFall
def createGarrisons(tCityPlot, iNewOwner, iNumUnits):
    pPlayer = gc.getPlayer(iNewOwner)

    # Sedna17: makes garrison units based on new tech tree/units
    iUnitType = Unit.ARCHER
    lUnits = [
        Unit.LINE_INFANTRY,
        Unit.MUSKETMAN,
        Unit.ARQUEBUSIER,
        Unit.ARBALEST,
        Unit.ARBALEST,
        Unit.CROSSBOWMAN,
    ]
    for iUnit in lUnits:
        if pPlayer.canTrain(getUniqueUnit(iNewOwner, iUnit), False, False):
            iUnitType = getUniqueUnit(iNewOwner, iUnit)
            break

    make_units(iNewOwner, iUnitType, tCityPlot, iNumUnits)


def killAndFragmentCiv(iCiv, bBarbs, bAssignOneCity):
    clearPlague(iCiv)
    iNumLoyalCities = 0
    iCounter = rand(6)
    for city in cities().owner(iCiv).entities():
        tCoords = (city.getX(), city.getY())
        iX, iY = tCoords
        pCurrent = gc.getMap().plot(iX, iY)
        # 1 loyal city for the human player
        if bAssignOneCity and iNumLoyalCities < 1 and city.isCapital():
            iNumLoyalCities += 1
            for i in civilizations().independents().ids():
                teamMinor = gc.getTeam(gc.getPlayer(i).getTeam())
                if not teamMinor.isAtWar(iCiv):
                    gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(i, False, -1)
            continue
        # assign to neighbours first
        bNeighbour = False
        iRndnum = rand(civilizations().majors().len())
        for j in civilizations().majors().ids():
            iLoopCiv = (j + iRndnum) % civilizations().majors().len()
            if (
                gc.getPlayer(iLoopCiv).isAlive()
                and iLoopCiv != iCiv
                and not gc.getPlayer(iLoopCiv).isHuman()
            ):
                if pCurrent.getCulture(iLoopCiv) > 0:
                    if (
                        pCurrent.getCulture(iLoopCiv)
                        * 100
                        / (
                            pCurrent.getCulture(iLoopCiv)
                            + pCurrent.getCulture(iCiv)
                            + pCurrent.getCulture(Civ.BARBARIAN)
                            + pCurrent.getCulture(Civ.INDEPENDENT)
                            + pCurrent.getCulture(Civ.INDEPENDENT_2)
                        )
                        >= 5
                    ):  # change in vanilla
                        flipUnitsInCityBefore(tCoords, iLoopCiv, iCiv)
                        setTempFlippingCity(tCoords)
                        flipCity(tCoords, 0, 0, iLoopCiv, [iCiv])
                        # city.setHasRealBuilding(Plague.PLAGUE, False) #buggy
                        # Sedna17: Possibly buggy, used to flip units in 2 radius, which could take us outside the map.
                        flipUnitsInArea(
                            (iX - 1, iY - 1), (iX + 1, iY + 1), iLoopCiv, iCiv, False, True
                        )
                        flipUnitsInCityAfter(getTempFlippingCity(), iLoopCiv)
                        bNeighbour = True
                        break
        if bNeighbour:
            continue
        # fragmentation in 2
        if not bBarbs:
            iNewCiv = min(civilizations().independents().ids()) + rand(
                max(civilizations().independents().ids())
                - min(civilizations().independents().ids())
                + 1
            )
            flipUnitsInCityBefore(tCoords, iNewCiv, iCiv)
            setTempFlippingCity(tCoords)
            cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
            flipCity(tCoords, 0, 0, iNewCiv, [iCiv])
            # city.setHasRealBuilding(Plague.PLAGUE, False) #buggy
            flipUnitsInCityAfter(getTempFlippingCity(), iNewCiv)
            iCounter += 1
            flipUnitsInArea((iX - 1, iY - 1), (iX + 1, iY + 1), iNewCiv, iCiv, False, True)
        # fragmentation with barbs
        else:
            iNewCiv = min(civilizations().independents().ids()) + rand(
                max(civilizations().independents().ids())
                - min(civilizations().independents().ids())
                + 2
            )
            if iNewCiv == max(civilizations().independents().ids()) + 1:
                iNewCiv = Civ.BARBARIAN
            flipUnitsInCityBefore(tCoords, iNewCiv, iCiv)
            setTempFlippingCity(tCoords)
            cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
            flipCity(tCoords, 0, 0, iNewCiv, [iCiv])
            flipUnitsInCityAfter(getTempFlippingCity(), iNewCiv)
            iCounter += 1
            flipUnitsInArea((iX - 1, iY - 1), (iX + 1, iY + 1), iNewCiv, iCiv, False, True)
    if not bAssignOneCity:
        # flipping units may cause a bug: if a unit is inside another civ's city when it becomes independent or barbarian, may raze it
        for unit in units().owner(iCiv).entities():
            unit.kill(False, Civ.BARBARIAN)
        resetUHV(iCiv)

        setLastTurnAlive(iCiv, turn())
        # Absinthe: alive status should be updated right on collapse - may result in crashes if it only updates on the beginning of the next turn
        gc.getPlayer(iCiv).setAlive(False)
        # Absinthe: respawn status
        if gc.getPlayer(iCiv).getRespawnedAlive():
            gc.getPlayer(iCiv).setRespawnedAlive(False)


def resetUHV(iPlayer):
    if iPlayer < civilizations().majors().len():
        pPlayer = gc.getPlayer(iPlayer)
        for i in range(3):
            if pPlayer.getUHV(i) == -1:
                pPlayer.setUHV(i, 0)


def clearPlague(iCiv):
    for city in cities().owner(iCiv).building(PlagueType.PLAGUE).entities():
        city.setHasRealBuilding(PlagueType.PLAGUE, False)


# TODO refacto with structure
# AIWars
def isAVassal(iCiv):
    return gc.getTeam(gc.getPlayer(iCiv).getTeam()).isAVassal()


# TODO refacto with structure
# UP, UHV, idea from DoC
def getMaster(iCiv):
    team = gc.getTeam(gc.getPlayer(iCiv).getTeam())
    if team.isAVassal():
        for iMaster in civilizations().drop(Civ.BARBARIAN).ids():
            if team.isVassal(iMaster):
                return iMaster
    return -1


def squareSearch(tTopLeft, tBottomRight, function, argsList):  # by LOQ
    """Searches all tiles in the square from tTopLeft to tBottomRight and calls function for every tile, passing argsList."""
    tPaintedList = []
    for plot in plots().rectangle(tTopLeft, tBottomRight).entities():
        bPaintPlot = function(location(plot), argsList)
        if bPaintPlot:
            tPaintedList.append(location(plot))
    return tPaintedList


def outerInvasion(tCoords, argsList):
    """Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory."""
    pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
    if pCurrent.isHills() or pCurrent.isFlatlands():
        if pCurrent.getFeatureType() not in [Feature.MARSH, Feature.JUNGLE]:
            if not pCurrent.isCity() and not pCurrent.isUnit():
                if pCurrent.countTotalCulture() == 0:
                    return True
    return False


def forcedInvasion(tCoords, argsList):
    """Plot is valid if it's hill or flatlands, it isn't marsh or jungle, and it isn't occupied by a unit or city."""
    pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
    if pCurrent.isHills() or pCurrent.isFlatlands():
        if pCurrent.getFeatureType() not in [Feature.MARSH, Feature.JUNGLE]:
            if not pCurrent.isCity() and not pCurrent.isUnit():
                return True
    return False


def outerSeaSpawn(tCoords, argsList):
    """Plot is valid if it's water (coast), it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots."""
    pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
    if pCurrent.isWater() and pCurrent.getTerrainType() == Terrain.COAST:
        if not pCurrent.isUnit():
            if pCurrent.countTotalCulture() == 0:
                for plot in plots().surrounding(tCoords).entities():
                    if plot.isUnit():
                        return False
                return True
    return False


def innerSeaSpawn(tCoords, argsList):
    """Plot is valid if it's water (coast) and it isn't occupied by any unit. Unit check extended to adjacent plots."""
    pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
    if pCurrent.isWater() and pCurrent.getTerrainType() == Terrain.COAST:
        if not pCurrent.isUnit():
            for plot in plots().surrounding(tCoords).entities():
                if plot.isUnit():
                    return False
            return True
    return False


def outerSpawn(tCoords, argsList):
    """Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory. Unit check extended to adjacent plots."""
    pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
    if pCurrent.isHills() or pCurrent.isFlatlands():
        if pCurrent.getFeatureType() not in [Feature.MARSH, Feature.JUNGLE]:
            if not pCurrent.isCity() and not pCurrent.isUnit():
                if pCurrent.countTotalCulture() == 0:
                    for plot in plots().surrounding(tCoords).entities():
                        if plot.isUnit():
                            return False
                    return True
    return False


def innerSpawn(tCoords, argsList):
    """Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it's in a given civ's territory. Unit check extended to adjacent plots."""
    pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
    if pCurrent.isHills() or pCurrent.isFlatlands():
        if pCurrent.getFeatureType() not in [Feature.MARSH, Feature.JUNGLE]:
            if not pCurrent.isCity() and not pCurrent.isUnit():
                if pCurrent.getOwner() in argsList:
                    for plot in plots().surrounding(tCoords).entities():
                        if plot.isUnit():
                            return False
                    return True
    return False


def goodPlots(tCoords, argsList):
    """Plot is valid if it's hill or flatlands, it isn't desert, tundra, marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory. Unit check extended to adjacent plots."""
    pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
    if pCurrent.isHills() or pCurrent.isFlatlands():
        if not pCurrent.isImpassable():
            if not pCurrent.isCity() and not pCurrent.isUnit():
                if (
                    pCurrent.getTerrainType()
                    not in [
                        Terrain.DESERT,
                        Terrain.TUNDRA,
                    ]
                    and pCurrent.getFeatureType() not in [Feature.MARSH, Feature.JUNGLE]
                ):
                    if pCurrent.countTotalCulture() == 0:
                        return True
    return False


def ownedCityPlots(tCoords, argsList):
    """Plot is valid if it contains a city belonging to the given civ."""
    pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
    if pCurrent.getOwner() == argsList:
        if pCurrent.isCity():
            return True
    return False


def collapseImmune(iCiv):
    # 3MiroUP: Emperor
    if gc.hasUP(iCiv, UniquePower.NO_COLLAPSE_IN_CORE_AND_NORMAL_AREAS):
        plot = gc.getMap().plot(*civilization(iCiv).location.capital)
        if plot.isCity():
            if plot.getOwner() == iCiv:
                return True
    return False


# Absinthe: chooseable persecution popup
def showPersecutionPopup():
    """Asks the human player to select a religion to persecute."""

    popup = Popup.PyPopup(7628, EventContextTypes.EVENTCONTEXT_ALL)
    popup.setHeaderString("Religious Persecution")
    popup.setBodyString("Choose a religious minority to deal with...")
    for iReligion in data.lPersecutionReligions:
        strIcon = gc.getReligionInfo(iReligion).getType()
        strIcon = "[%s]" % (strIcon.replace("RELIGION_", "ICON_"))
        strButtonText = "%s %s" % (text(strIcon), gc.getReligionInfo(iReligion).getText())
        popup.addButton(strButtonText)
    popup.launch(False)


# Absinthe: persecution
def prosecute(iPlotX, iPlotY, iUnitID, iReligion=-1):
    """Removes one religion from the city and handles the consequences."""

    if gc.getMap().plot(iPlotX, iPlotY).isCity():
        city = gc.getMap().plot(iPlotX, iPlotY).getPlotCity()
    else:
        return

    iOwner = city.getOwner()
    pPlayer = gc.getPlayer(iOwner)
    pUnit = pPlayer.getUnit(iUnitID)
    iStateReligion = pPlayer.getStateReligion()

    # sanity check - can only persecute with a state religion
    if iStateReligion == -1:
        return False

    # determine the target religion, if not supplied by the popup decision (for the AI)
    if iReligion == -1:
        for iReligion in RELIGION_PERSECUTION_ORDER[get_religion_by_id(iStateReligion)]:
            if not city.isHolyCityByType(iReligion):  # spare holy cities
                if city.isHasReligion(iReligion):
                    # so this will be the iReligion for further calculations
                    break

    # count the number of religious buildings and wonders (for the chance)
    if iReligion > -1:
        lReligionBuilding = []
        iReligionWonder = 0
        for iBuilding in xrange(gc.getNumBuildingInfos()):  # type: ignore  # type: ignore
            if city.getNumRealBuilding(iBuilding):
                BuildingInfo = gc.getBuildingInfo(iBuilding)
                if BuildingInfo.getPrereqReligion() == iReligion:
                    lReligionBuilding.append(iBuilding)
                    if isWorldWonderClass(
                        BuildingInfo.getBuildingClassType()
                    ) or isNationalWonderClass(BuildingInfo.getBuildingClassType()):
                        iReligionWonder += 1
    else:
        return False  # when there is no available religion to purge

    # base chance to work: about 50-80%, based on faith:
    iChance = 50 + pPlayer.getFaith() / 3
    # lower chance for purging any religion from Jerusalem:
    if (iPlotX, iPlotY) == CITIES[City.JERUSALEM]:
        iChance -= 24
    # lower chance if the city has the chosen religion's buildings/wonders:
    iBuildingChanceReduction = min(24, len(lReligionBuilding) * 4)
    iBuildingChanceReduction += (
        iReligionWonder * 12
    )  # the wonders have an extra chance reduction (in addition to the building reduction)
    iChance -= iBuildingChanceReduction
    # bonus for the AI:
    if human() != iOwner:
        iChance += 16
    # population modifier:
    if city.getPopulation() > 11:
        iChance -= 12
    elif city.getPopulation() > 7:
        iChance -= 8
    elif city.getPopulation() > 3:
        iChance -= 4

    if percentage_chance(iChance, strict=True):
        # on successful persecution
        # remove a single non-state religion and its buildings from the city, count the loot
        iLootModifier = 3 * city.getPopulation() / city.getReligionCount()
        iLoot = 5 + iLootModifier
        city.setHasReligion(iReligion, 0, 0, 0)
        for i in range(len(lReligionBuilding)):
            city.setNumRealBuilding(lReligionBuilding[i], 0)
            iLoot += iLootModifier
        if iReligion == Religion.JUDAISM:
            iLoot = iLoot * 3 / 2

        # kill / expel some population
        if city.getPopulation() > 15 and city.getReligionCount() < 2:
            city.changePopulation(-4)
        elif city.getPopulation() > 10 and city.getReligionCount() < 3:
            city.changePopulation(-3)
        elif city.getPopulation() > 6 and city.getReligionCount() < 4:
            city.changePopulation(-2)
        elif city.getPopulation() > 3:
            city.changePopulation(-1)

        # distribute the loot
        iLoot += rand(iLoot)
        pPlayer.changeGold(iLoot)

        # add faith for the persecution itself (there is an indirect increase too, the negative modifier from having a non-state religion is gone)
        pPlayer.changeFaith(1)

        # apply diplomatic penalty
        for iLoopPlayer in civilizations().majors().ids():
            pLoopPlayer = gc.getPlayer(iLoopPlayer)
            if pLoopPlayer.isAlive() and iLoopPlayer != iOwner:
                if pLoopPlayer.getStateReligion() == iReligion:
                    pLoopPlayer.AI_changeAttitudeExtra(iOwner, -1)

        # count minor religion persecutions - resettling jewish people on persecution is handled another way
        # if ( i == minorReligion ){ // 3Miro: count the minor religion prosecutions
        # minorReligionRefugies++;
        # gc.setMinorReligionRefugies( 0 )

        # interface message for the player
        message(
            iOwner,
            text(
                "TXT_KEY_MESSAGE_INQUISITION",
                city.getName(),
                gc.getReligionInfo(iReligion).getDescription(),
                iLoot,
            ),
            sound="AS2D_PLAGUE",
            event=InterfaceMessageTypes.MESSAGE_TYPE_INFO,
            button=pUnit.getButton(),
            color=MessageData.GREEN,
            location=(iPlotX, iPlotY),
        )

        # Jews may spread to another random city
        if iReligion == Religion.JUDAISM:
            if percentage_chance(80, strict=True):
                pSpreadCity = cities().majors().random_entry()
                spreadJews(location(pSpreadCity), Religion.JUDAISM)
                if pSpreadCity.getOwner() == iOwner:
                    message(
                        iOwner,
                        text(
                            "TXT_KEY_MESSAGE_JEWISH_MOVE_OWN_CITY",
                            city.getName(),
                            pSpreadCity.getName(),
                        ),
                        sound="AS2D_PLAGUE",
                        event=InterfaceMessageTypes.MESSAGE_TYPE_INFO,
                        button=pUnit.getButton(),
                        color=MessageData.GREEN,
                        location=(iPlotX, iPlotY),
                    )
                else:
                    message(
                        iOwner,
                        text("TXT_KEY_MESSAGE_JEWISH_MOVE", city.getName()),
                        sound="AS2D_PLAGUE",
                        event=InterfaceMessageTypes.MESSAGE_TYPE_INFO,
                        button=pUnit.getButton(),
                        color=MessageData.GREEN,
                        location=(iPlotX, iPlotY),
                    )

        # persecution countdown for the civ (causes indirect instability - stability.recalcCity)
        if gc.hasUP(iOwner, UniquePower.LESS_INSTABILITY_WITH_RELIGIOUS_PROSECUTION):  # Spanish UP
            pPlayer.changeProsecutionCount(4)
        else:
            pPlayer.changeProsecutionCount(8)
            # also some swing instability:
            pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 3)

        # "We cannot forget your cruel oppression" unhappiness from persecution
        city.changeHurryAngerTimer(city.flatHurryAngerLength())

    else:
        # on failed persecution
        message(
            iOwner,
            text("TXT_KEY_MESSAGE_INQUISITION_FAIL", city.getName()),
            sound="AS2D_SABOTAGE",
            event=InterfaceMessageTypes.MESSAGE_TYPE_INFO,
            button=pUnit.getButton(),
            color=MessageData.RED,
            location=(iPlotX, iPlotY),
        )

        # persecution countdown for the civ (causes indirect instability - stability.recalcCity)
        if gc.hasUP(iOwner, UniquePower.LESS_INSTABILITY_WITH_RELIGIOUS_PROSECUTION):  # Spanish UP
            pPlayer.changeProsecutionCount(2)
        else:
            pPlayer.changeProsecutionCount(4)

    # start a small revolt
    city.changeCultureUpdateTimer(1)
    city.changeOccupationTimer(1)

    # consume the inquisitor
    pUnit.kill(0, -1)

    return True


# Absinthe: end


def saint(iOwner, iUnitID):
    # 3Miro: kill the Saint :), just make it so he cannot be used for other purposes
    pPlayer = gc.getPlayer(iOwner)
    # Absinthe: Wonders: Boyana Church wonder effect
    if pPlayer.countNumBuildings(Wonder.BOYANA_CHURCH) > 0:
        pPlayer.changeFaith(GREAT_PROPHET_FAITH_POINT_BONUS * 3 / 2 + 2)
    else:
        pPlayer.changeFaith(GREAT_PROPHET_FAITH_POINT_BONUS)
    pUnit = pPlayer.getUnit(iUnitID)
    pUnit.kill(0, -1)


def spreadJews(tPlot, iReligion):
    if tPlot:
        plot = gc.getMap().plot(tPlot[0], tPlot[1])
        if not plot.getPlotCity().isNone():
            plot.getPlotCity().setHasReligion(
                iReligion, 1, 0, 0
            )  # puts the religion into this city
            return True
        else:
            return False
    return False


# Absinthe: stability overlay
def toggleStabilityOverlay():

    engine = CyEngine()
    map = CyMap()

    # clear the highlight
    engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)

    global iScreenIsUp
    global bStabilityOverlay
    if bStabilityOverlay:  # if it's already on
        bStabilityOverlay = False
        iScreenIsUp = 0
        CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState(
            "StabilityOverlay", False
        )
        # remove the selectable civs and the selection box
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        for i in civilizations().main().ids():
            szName = "StabilityOverlayCiv" + str(i)
            screen.hide(szName)
        screen.hide("ScoreBackground")
        return

    bStabilityOverlay = True
    iScreenIsUp = 1
    CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState(
        "StabilityOverlay", True
    )

    # set up colors
    colors = []
    colors.append("COLOR_HIGHLIGHT_FOREIGN")
    colors.append("COLOR_HIGHLIGHT_BORDER")
    colors.append("COLOR_HIGHLIGHT_POTENTIAL")
    colors.append("COLOR_HIGHLIGHT_NATURAL")
    colors.append("COLOR_HIGHLIGHT_CORE")

    # Globe View type civ choice
    # when one of the civs is clicked on, it will run the StabilityOverlayCiv function with the chosen civ (check handleInput in CvMainInterface.py)
    screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
    xResolution = screen.getXResolution()
    yResolution = screen.getYResolution()
    iGlobeLayerOptionsY_Regular = 170  # distance from bottom edge
    iGlobeLayerOptionsY_Minimal = 38  # distance from bottom edge
    iGlobeLayerOptionsWidth = 400
    iGlobeLayerOptionHeight = 20
    iY = yResolution - iGlobeLayerOptionsY_Regular
    iCurY = iY
    iMaxTextWidth = -1
    for iCiv in civilizations().main().ids():
        szDropdownName = str("StabilityOverlayCiv") + str(iCiv)
        szCaption = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
        if iCiv == human():
            szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
        else:
            szBuffer = "  %s  " % (szCaption)
        iTextWidth = CyInterface().determineWidth(szBuffer)

        screen.setText(
            szDropdownName,
            "Background",
            szBuffer,
            CvUtil.FONT_LEFT_JUSTIFY,
            xResolution - 9 - iTextWidth,
            iCurY - iGlobeLayerOptionHeight - 10,
            -0.3,
            FontTypes.SMALL_FONT,
            WidgetTypes.WIDGET_GENERAL,
            iCiv,
            1234,
        )
        screen.show(szDropdownName)

        iCurY -= iGlobeLayerOptionHeight

        if iTextWidth > iMaxTextWidth:
            iMaxTextWidth = iTextWidth

    # panel for the Globe View type civ choice:
    iCurY -= iGlobeLayerOptionHeight
    iPanelWidth = iMaxTextWidth + 16
    iPanelHeight = iY - iCurY
    iPanelX = xResolution - 14 - iPanelWidth
    iPanelY = iCurY
    screen.setPanelSize("ScoreBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight)
    screen.show("ScoreBackground")

    # apply the highlight for the default civ (the human civ)
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if gc.getGame().isDebugMode() or plot.isRevealed(teamtype(), False):
            if PROVINCES_MAP[plot.getY()][plot.getX()] == -1:  # ocean and non-province tiles
                szColor = "COLOR_GREY"
            else:
                szColor = colors[getProvinceStabilityLevel(human(), plot.getProvince())]
            engine.addColoredPlotAlt(
                plot.getX(),
                plot.getY(),
                int(PlotStyles.PLOT_STYLE_BOX_FILL),
                int(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER),
                szColor,
                0.2,
            )


def refreshStabilityOverlay():

    engine = CyEngine()
    map = CyMap()

    colors = []
    colors.append("COLOR_HIGHLIGHT_FOREIGN")
    colors.append("COLOR_HIGHLIGHT_BORDER")
    colors.append("COLOR_HIGHLIGHT_POTENTIAL")
    colors.append("COLOR_HIGHLIGHT_NATURAL")
    colors.append("COLOR_HIGHLIGHT_CORE")
    iHuman = human()
    iHumanTeam = gc.getPlayer(iHuman).getTeam()

    # if it's on, refresh the overlay, with showing the stability for the last selected civ
    global iScreenIsUp
    if iScreenIsUp == 1:
        # clear the highlight
        engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)

        # if no civ was selected before
        global iSelectedCivID
        if iSelectedCivID == -1:
            iSelectedCivID = iHuman

        # apply the highlight
        for i in range(map.numPlots()):
            plot = map.plotByIndex(i)
            if gc.getGame().isDebugMode() or plot.isRevealed(iHumanTeam, False):
                if PROVINCES_MAP[plot.getY()][plot.getX()] == -1:  # ocean and non-province tiles
                    szColor = "COLOR_GREY"
                else:
                    szColor = colors[getProvinceStabilityLevel(iSelectedCivID, plot.getProvince())]
                engine.addColoredPlotAlt(
                    plot.getX(),
                    plot.getY(),
                    int(PlotStyles.PLOT_STYLE_BOX_FILL),
                    int(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER),
                    szColor,
                    0.2,
                )


def StabilityOverlayCiv(iChoice):
    engine = CyEngine()

    # clear the highlight
    engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)

    colors = [
        "COLOR_HIGHLIGHT_FOREIGN",
        "COLOR_HIGHLIGHT_BORDER",
        "COLOR_HIGHLIGHT_POTENTIAL",
        "COLOR_HIGHLIGHT_NATURAL",
        "COLOR_HIGHLIGHT_CORE",
    ]

    iHuman = human()
    iHumanTeam = gc.getPlayer(iHuman).getTeam()

    # save the last selected civ in a global variable
    global iSelectedCivID
    iSelectedCivID = iChoice

    # refreshing and coloring Globe View type civ choice
    screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
    xResolution = screen.getXResolution()
    yResolution = screen.getYResolution()
    iGlobeLayerOptionsY_Regular = 170  # distance from bottom edge
    iGlobeLayerOptionsY_Minimal = 38  # distance from bottom edge
    iGlobeLayerOptionsWidth = 400
    iGlobeLayerOptionHeight = 20
    iY = yResolution - iGlobeLayerOptionsY_Regular
    iCurY = iY
    iMaxTextWidth = -1
    for iCiv in civilizations().main().ids():
        szDropdownName = str("StabilityOverlayCiv") + str(iCiv)
        szCaption = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
        if iCiv == iSelectedCivID:
            szBuffer = "  <color=0,255,255>%s</color>  " % (szCaption)
        elif iCiv == human():
            szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
        else:
            szBuffer = "  %s  " % (szCaption)
        iTextWidth = CyInterface().determineWidth(szBuffer)

        screen.setText(
            szDropdownName,
            "Background",
            szBuffer,
            CvUtil.FONT_LEFT_JUSTIFY,
            xResolution - 9 - iTextWidth,
            iCurY - iGlobeLayerOptionHeight - 10,
            -0.3,
            FontTypes.SMALL_FONT,
            WidgetTypes.WIDGET_GENERAL,
            iCiv,
            1234,
        )
        screen.show(szDropdownName)

        iCurY -= iGlobeLayerOptionHeight

        if iTextWidth > iMaxTextWidth:
            iMaxTextWidth = iTextWidth

    # apply the highlight
    for plot in plots().all().land().entities():
        if gc.getGame().isDebugMode() or plot.isRevealed(iHumanTeam, False):
            if PROVINCES_MAP[plot.getY()][plot.getX()] == -1:  # ocean and non-province tiles
                szColor = "COLOR_GREY"
            else:
                szColor = colors[getProvinceStabilityLevel(iChoice, plot.getProvince())]
            engine.addColoredPlotAlt(
                plot.getX(),
                plot.getY(),
                int(PlotStyles.PLOT_STYLE_BOX_FILL),
                int(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER),
                szColor,
                0.2,
            )


def getProvinceStabilityLevel(iCiv, iProvince):
    """Returns the stability level of the province for the given civ."""

    pPlayer = gc.getPlayer(iCiv)
    iProvType = pPlayer.getProvinceType(iProvince)
    if iProvType == ProvinceType.CORE:
        return 4  # core
    elif iProvType == ProvinceType.HISTORICAL:
        return 3  # natural/historical
    elif iProvType == ProvinceType.POTENTIAL:
        return 2  # potential
    elif iProvType == ProvinceType.CONTESTED:
        return 1  # border/contested
    else:
        return 0  # unstable


# Absinthe: end


def getUniqueUnit(iPlayer, iUnit):
    pPlayer = gc.getPlayer(iPlayer)
    return gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(
        gc.getUnitInfo(iUnit).getUnitClassType()
    )


def getBaseUnit(iUnit):
    return gc.getUnitClassInfo(gc.getUnitInfo(iUnit).getUnitClassType()).getDefaultUnitIndex()


def getUniqueBuilding(iPlayer, iBuilding):
    pPlayer = gc.getPlayer(iPlayer)
    return gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationBuildings(
        gc.getBuildingInfo(iBuilding).getBuildingClassType()
    )


def getBaseBuilding(iBuilding):
    return gc.getBuildingClassInfo(
        gc.getBuildingInfo(iBuilding).getBuildingClassType()
    ).getDefaultBuildingIndex()


def getMostAdvancedCiv():
    iBestCiv = -1
    iMostTechs = 0
    for iPlayer in civilizations().main().ids():
        pPlayer = gc.getPlayer(iPlayer)
        if pPlayer.isAlive():
            iTeam = pPlayer.getTeam()
            pTeam = gc.getTeam(iTeam)
            iTechNumber = 0
            for iTech in xrange(gc.getNumTechInfos()):  # type: ignore
                if pTeam.isHasTech(iTech):
                    iTechNumber += 1
            if iTechNumber > iMostTechs:
                iBestCiv = iPlayer
                iMostTechs = iTechNumber
            # we aim for the single most advanced civ
            elif iTechNumber == iMostTechs:
                iBestCiv = -1
    return iBestCiv


def getNumberCargoShips(iPlayer):
    return units().owner(iPlayer).filter(lambda u: u.cargoSpace() > 0).len()


def isWonder(iBuilding):
    return iBuilding in [w for w in Wonder]


def getDawnOfManText(iPlayer):
    scenario = get_scenario()
    base_key = "TXT_KEY_DOM_%s" % str(name(iPlayer).replace(" ", "_").upper())

    full_key = base_key
    if scenario == Scenario.i1200AD:
        full_key += "_1200AD"

    return text_if_exists(full_key, otherwise=base_key)


def change_attitude_extra_between_civ(iPlayer1, iPlayer2, iValue):
    gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
    gc.getPlayer(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)


def get_stability_category_value(iPlayer, stability_category):
    if stability_category == StabilityCategory.SWING:
        return player(iPlayer).getStabilitySwing()
    else:
        return player(iPlayer).getStabilityBase(stability_category)


def stability(civ):
    value = player(civ).getStability()
    if value < -15:
        _text = text("TXT_KEY_STABILITY_COLLAPSING")
        _symbol = symbol(FontSymbols.COLLAPSING_CHAR)
    elif -15 <= value < -5:
        _text = text("TXT_KEY_STABILITY_UNSTABLE")
        _symbol = symbol(FontSymbols.UNSTABLE_CHAR)
    elif -5 <= value < 5:
        _text = text("TXT_KEY_STABILITY_SHAKY")
        _symbol = symbol(FontSymbols.SHAKY_CHAR)
    elif 5 <= value < 15:
        _text = text("TXT_KEY_STABILITY_STABLE")
        _symbol = symbol(FontSymbols.STABLE_CHAR)
    elif value >= 15:
        _text = text("TXT_KEY_STABILITY_SOLID")
        _symbol = symbol(FontSymbols.SOLID_CHAR)
    elif value >= 25:
        _text = text("TXT_KEY_STABILITY_VERYSOLID")
        _symbol = symbol(FontSymbols.SOLID_CHAR)
    return value, _text, _symbol


def calculate_gold_rate(identifier):
    # Returns the new version of the gold text that takes into account the
    # mercenary maintenance cost and contract income
    pPlayer = player(identifier)

    totalUnitCost = pPlayer.calculateUnitCost()
    totalUnitSupply = pPlayer.calculateUnitSupply()
    totalMaintenance = pPlayer.getTotalMaintenance()
    totalCivicUpkeep = pPlayer.getCivicUpkeep([], False)
    totalPreInflatedCosts = pPlayer.calculatePreInflatedCosts()
    totalInflatedCosts = pPlayer.calculateInflatedCosts()
    totalMercenaryCost = (
        pPlayer.getPicklefreeParameter(SpecialParameter.MERCENARY_COST_PER_TURN) + 99
    ) / 100

    # Colony Upkeep
    iColonyNumber = pPlayer.getNumColonies()
    iColonyUpkeep = 0
    if iColonyNumber > 0:
        iColonyUpkeep = int((0.5 * iColonyNumber * iColonyNumber + 0.5 * iColonyNumber) * 3 + 7)
    goldCommerce = pPlayer.getCommerceRate(CommerceTypes.COMMERCE_GOLD)

    iIncome = 0
    iExpenses = 0
    iIncome = goldCommerce

    goldFromCivs = pPlayer.getGoldPerTurn()
    if goldFromCivs > 0:
        iIncome += goldFromCivs

    iInflation = totalInflatedCosts - totalPreInflatedCosts

    iExpenses = (
        totalUnitCost
        + totalUnitSupply
        + totalMaintenance
        + totalCivicUpkeep
        + iInflation
        + totalMercenaryCost
        + iColonyUpkeep
    )

    if goldFromCivs < 0:
        iExpenses -= goldFromCivs

    iDelta = iIncome - iExpenses
    return iDelta


def render_faith_status(identifier):
    pPlayer = player(identifier)
    prosecution_count = pPlayer.getProsecutionCount()
    faith_text = text("TXT_KEY_FAITH_POINTS") + (": %i " % pPlayer.getFaith())

    prosecution_text = text("TXT_KEY_FAITH_PROSECUTION_COUNT") + (": %i " % prosecution_count)
    faith_status = faith_text + "\n" + prosecution_text
    return faith_status


def _get_faith_benefits(identifier):
    pPlayer = player(identifier)
    prosecution_count = pPlayer.getProsecutionCount()

    faith_benefits_mapper = {
        FaithPointBonusCategory.BOOST_STABILITY: (
            "TXT_KEY_FAITH_STABILITY",
            "+%i",
        ),
        FaithPointBonusCategory.REDUCE_CIVIC_UPKEEP: (
            "TXT_KEY_FAITH_CIVIC",
            "-%i percent",
        ),
        FaithPointBonusCategory.FASTER_POPULATION_GROWTH: (
            "TXT_KEY_FAITH_GROWTH",
            "+%i percent",
        ),
        FaithPointBonusCategory.REDUCING_COST_UNITS: (
            "TXT_KEY_FAITH_UNITS",
            "-%i percent",
        ),
        FaithPointBonusCategory.REDUCING_TECH_COST: (
            "TXT_KEY_FAITH_SCIENCE",
            "-%i percent",
        ),
        FaithPointBonusCategory.REDUCING_WONDER_COST: (
            "TXT_KEY_FAITH_PRODUCTION",
            "-%i percent",
        ),
        FaithPointBonusCategory.BOOST_DIPLOMACY: (
            "TXT_KEY_FAITH_DIPLOMACY",
            "+%i",
        ),
    }
    faith_benefits = {}
    faith_benefits_text = ""

    for benefit, (_text, indicator) in faith_benefits_mapper.items():
        if pPlayer.isFaithBenefit(benefit):
            faith_benefit = pPlayer.getFaithBenefit(benefit)
            indicator = indicator % faith_benefit
            faith_benefits[benefit] = faith_benefit
            faith_benefits_text += text(_text) + " " + indicator + " \n"

    if prosecution_count > 0:
        prosecution_stability = (prosecution_count + 2) / 3
        faith_benefits["prosecution_stability"] = prosecution_stability
        faith_benefits_text += text("TXT_KEY_FAITH_PROSECUTION_INSTABILITY") + (
            " -%i \n" % prosecution_stability
        )

    return faith_benefits, faith_benefits_text


def calculate_faith_benefits(identifier, total=True):
    faith_benefits = _get_faith_benefits(identifier)[0]
    if total:
        faith_benefits = sum(faith_benefits.values())
    return faith_benefits


def render_faith_benefits(identifier):
    return _get_faith_benefits(identifier)[1]
