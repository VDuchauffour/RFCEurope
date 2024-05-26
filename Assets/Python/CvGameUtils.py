from CoreData import civilization
from CoreFunctions import get_religion_by_id, text
from CoreStructures import turn
from CoreTypes import Building, Civ, Religion, StabilityCategory, Unit, Wonder
import CvUtil
from CvPythonExtensions import *
from ReligionData import RELIGION_PERSECUTION_ORDER
import PyHelpers
from PyUtils import rand  # Absinthe
from RFCUtils import prosecute
import Stability  # Absinthe

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer  # Absinthe
sta = Stability.Stability()  # Absinthe


class CvGameUtils:
    "Miscellaneous game functions"

    def __init__(self):
        pass

    def isVictoryTest(self):
        return CyGame().getElapsedGameTurns() > 10

    def isVictory(self, argsList):
        eVictory = argsList[0]
        return True

    def isPlayerResearch(self, argsList):
        ePlayer = argsList[0]
        return True

    def getExtraCost(self, argsList):
        ePlayer = argsList[0]
        return 0

    def createBarbarianCities(self):
        return False

    def createBarbarianUnits(self):
        return False

    def skipResearchPopup(self, argsList):
        ePlayer = argsList[0]
        return False

    def showTechChooserButton(self, argsList):
        ePlayer = argsList[0]
        return True

    def getFirstRecommendedTech(self, argsList):
        ePlayer = argsList[0]
        return TechTypes.NO_TECH

    def getSecondRecommendedTech(self, argsList):
        ePlayer = argsList[0]
        eFirstTech = argsList[1]
        return TechTypes.NO_TECH

    def canRazeCity(self, argsList):
        iRazingPlayer, pCity = argsList
        return True

    def canDeclareWar(self, argsList):
        iAttackingTeam, iDefendingTeam = argsList
        return True

    def skipProductionPopup(self, argsList):
        pCity = argsList[0]
        return False

    def showExamineCityButton(self, argsList):
        pCity = argsList[0]
        return True

    def getRecommendedUnit(self, argsList):
        pCity = argsList[0]
        return UnitTypes.NO_UNIT

    def getRecommendedBuilding(self, argsList):
        pCity = argsList[0]
        return BuildingTypes.NO_BUILDING

    def updateColoredPlots(self):
        return False

    def isActionRecommended(self, argsList):
        pUnit = argsList[0]
        iAction = argsList[1]
        return False

    def unitCannotMoveInto(self, argsList):
        ePlayer = argsList[0]
        iUnitId = argsList[1]
        iPlotX = argsList[2]
        iPlotY = argsList[3]
        return False

    def cannotHandleAction(self, argsList):
        pPlot = argsList[0]
        iAction = argsList[1]
        bTestVisible = argsList[2]
        return False

    def canBuild(self, argsList):
        iX, iY, iBuild, iPlayer = argsList
        return (
            -1
        )  # Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can

    def cannotFoundCity(self, argsList):
        iPlayer, iPlotX, iPlotY = argsList
        return False

    def cannotSelectionListMove(self, argsList):
        pPlot = argsList[0]
        bAlt = argsList[1]
        bShift = argsList[2]
        bCtrl = argsList[3]
        return False

    def cannotSelectionListGameNetMessage(self, argsList):
        eMessage = argsList[0]
        iData2 = argsList[1]
        iData3 = argsList[2]
        iData4 = argsList[3]
        iFlags = argsList[4]
        bAlt = argsList[5]
        bShift = argsList[6]
        return False

    def cannotDoControl(self, argsList):
        eControl = argsList[0]
        return False

    def canResearch(self, argsList):
        ePlayer = argsList[0]
        eTech = argsList[1]
        bTrade = argsList[2]
        return False

    def cannotResearch(self, argsList):
        ePlayer = argsList[0]
        eTech = argsList[1]
        bTrade = argsList[2]
        return False

    def canDoCivic(self, argsList):
        ePlayer = argsList[0]
        eCivic = argsList[1]
        return False

    def cannotDoCivic(self, argsList):
        ePlayer = argsList[0]
        eCivic = argsList[1]
        return False

    def canTrain(self, argsList):
        pCity = argsList[0]
        eUnit = argsList[1]
        bContinue = argsList[2]
        bTestVisible = argsList[3]
        bIgnoreCost = argsList[4]
        bIgnoreUpgrades = argsList[5]
        return False

    def cannotTrain(self, argsList):
        pCity = argsList[0]
        eUnit = argsList[1]
        bContinue = argsList[2]
        bTestVisible = argsList[3]
        bIgnoreCost = argsList[4]
        bIgnoreUpgrades = argsList[5]
        return False

    def canConstruct(self, argsList):
        pCity = argsList[0]
        eBuilding = argsList[1]
        bContinue = argsList[2]
        bTestVisible = argsList[3]
        bIgnoreCost = argsList[4]
        return False

    def cannotConstruct(self, argsList):
        pCity = argsList[0]
        eBuilding = argsList[1]
        bContinue = argsList[2]
        bTestVisible = argsList[3]
        bIgnoreCost = argsList[4]
        return False

    def canCreate(self, argsList):
        pCity = argsList[0]
        eProject = argsList[1]
        bContinue = argsList[2]
        bTestVisible = argsList[3]
        return False

    def cannotCreate(self, argsList):
        pCity = argsList[0]
        eProject = argsList[1]
        bContinue = argsList[2]
        bTestVisible = argsList[3]
        return False

    def canMaintain(self, argsList):
        pCity = argsList[0]
        eProcess = argsList[1]
        bContinue = argsList[2]
        return False

    def cannotMaintain(self, argsList):
        pCity = argsList[0]
        eProcess = argsList[1]
        bContinue = argsList[2]
        return False

    def AI_chooseTech(self, argsList):
        ePlayer = argsList[0]
        bFree = argsList[1]
        return TechTypes.NO_TECH

    def AI_chooseProduction(self, argsList):
        pCity = argsList[0]
        return False

    # Absinthe: start Inquisitor AI proper (based on SoI)
    def AI_unitUpdate(self, argsList):
        pUnit = argsList[0]
        iOwner = pUnit.getOwner()
        AIpPlayer = gc.getPlayer(iOwner)
        if (
            not AIpPlayer.isNone()
            and not AIpPlayer.isBarbarian()
            and not AIpPlayer.isHuman()
            and AIpPlayer.isAlive()
        ):
            if pUnit.getUnitType() == Unit.PROSECUTOR.value:
                return self.doInquisitorCore_AI(pUnit)
        return False

    # Absinthe: Inquisitor AI, this is also called from the .dll, CvCityAI::AI_chooseUnit
    def isHasPurgeTarget(self, argsList):
        iCiv = argsList[0]
        bReportCity = argsList[1]
        iStateReligion = gc.getPlayer(iCiv).getStateReligion()
        iTolerance = civilization(iCiv).religion.tolerance
        apCityList = PyPlayer(iCiv).getCityList()
        # Checks whether the AI controls a city with a target religion that is not the State Religion, not a Holy City, and doesn't have religious wonders in it
        for iReligion in RELIGION_PERSECUTION_ORDER[get_religion_by_id(iStateReligion)]:
            bCanPurge = False
            # If the civ's tolerance > 70 it won't purge any religions
            # If > 50 (but < 70) it will only purge Islam with a Christian State Religion, and all Christian Religions with Islam as State Religion
            # If > 30 (but < 50) it will also purge Judaism
            # If < 30 it will purge all but the State Religion (so the other 2 Christian Religions as well)
            if iTolerance < 70 and (
                iReligion == Religion.ISLAM
                or (
                    iStateReligion == Religion.ISLAM
                    and iReligion
                    in [Religion.CATHOLICISM, Religion.ORTHODOXY, Religion.PROTESTANTISM]
                )
            ):
                bCanPurge = True

            if not bCanPurge and iTolerance < 50 and iReligion == Religion.JUDAISM:
                bCanPurge = True

            if not bCanPurge and iTolerance < 30:
                bCanPurge = True

            if bCanPurge:
                for pCity in apCityList:
                    if pCity.GetCy().isHasReligion(
                        iReligion.value
                    ) and not pCity.GetCy().isHolyCityByType(iReligion.value):
                        # do not purge religions with an associated wonder in the city
                        bWonder = False
                        for iBuilding in xrange(gc.getNumBuildingInfos()):  # type: ignore  # type: ignore
                            if pCity.GetCy().getNumRealBuilding(iBuilding):
                                BuildingInfo = gc.getBuildingInfo(iBuilding)
                                if BuildingInfo.getPrereqReligion() == iReligion.value:
                                    if isWorldWonderClass(
                                        BuildingInfo.getBuildingClassType()
                                    ) or isNationalWonderClass(
                                        BuildingInfo.getBuildingClassType()
                                    ):
                                        bWonder = True
                                        break  # end the loop if found one
                        if not bWonder:
                            # for the python code below, we need to pass the city too
                            if bReportCity:
                                return pCity
                            # for the AI function in the .dll we only need to know whether such city exist
                            else:
                                return True
        return False

    def doInquisitorCore_AI(self, pUnit):

        iOwner = pUnit.getOwner()
        pCity = self.isHasPurgeTarget(iOwner, True)
        if pCity:
            city = pCity.GetCy()
            # if we can generate a valid path to the city
            if pUnit.generatePath(city.plot(), 0, False, None):
                self.doInquisitorMove(pUnit, city)
                return True
        return False

    def doInquisitorMove(self, pUnit, pCity):
        if pUnit.getX() != pCity.getX() or pUnit.getY() != pCity.getY():
            pUnit.getGroup().pushMission(
                MissionTypes.MISSION_MOVE_TO,
                pCity.getX(),
                pCity.getY(),
                0,
                False,
                True,
                MissionAITypes.NO_MISSIONAI,
                pUnit.plot(),
                pUnit,
            )
        else:
            prosecute(pCity.getX(), pCity.getY(), pUnit.getID())

    def AI_doWar(self, argsList):
        eTeam = argsList[0]
        return False

    def AI_doDiplo(self, argsList):
        ePlayer = argsList[0]
        return False

    def calculateScore(self, argsList):
        ePlayer = argsList[0]
        bFinal = argsList[1]
        bVictory = argsList[2]

        if not bFinal:
            iPopulationScore = CvUtil.getScoreComponent(
                gc.getPlayer(ePlayer).getPopScore(),
                gc.getGame().getInitPopulation(),
                gc.getGame().getMaxPopulation(),
                gc.getDefineINT("SCORE_POPULATION_FACTOR"),
                True,
                bFinal,
                bVictory,
            )
            iLandScore = CvUtil.getScoreComponent(
                gc.getPlayer(ePlayer).getLandScore(),
                gc.getGame().getInitLand(),
                gc.getGame().getMaxLand(),
                gc.getDefineINT("SCORE_LAND_FACTOR"),
                True,
                bFinal,
                bVictory,
            )
            iTechScore = CvUtil.getScoreComponent(
                gc.getPlayer(ePlayer).getTechScore(),
                gc.getGame().getInitTech(),
                gc.getGame().getMaxTech(),
                gc.getDefineINT("SCORE_TECH_FACTOR"),
                True,
                bFinal,
                bVictory,
            )
            iWondersScore = CvUtil.getScoreComponent(
                gc.getPlayer(ePlayer).getWondersScore(),
                gc.getGame().getInitWonders(),
                gc.getGame().getMaxWonders(),
                gc.getDefineINT("SCORE_WONDER_FACTOR"),
                False,
                bFinal,
                bVictory,
            )
            return int(iPopulationScore + iLandScore + iWondersScore + iTechScore)
        else:
            # 3Miro: we compute the final scores different now
            iPopulationScore = self.getScoreComponentRFCE(
                gc.getPlayer(ePlayer).getPopScore(),
                gc.getGame().getInitPopulation(),
                gc.getGame().getMaxPopulation(),
                gc.getDefineINT("SCORE_POPULATION_FACTOR"),
                True,
                bFinal,
                bVictory,
            )
            iLandScore = self.getScoreComponentRFCE(
                gc.getPlayer(ePlayer).getLandScore(),
                gc.getGame().getInitLand(),
                gc.getGame().getMaxLand(),
                gc.getDefineINT("SCORE_LAND_FACTOR"),
                True,
                bFinal,
                bVictory,
            )
            iTechScore = self.getScoreComponentRFCE(
                gc.getPlayer(ePlayer).getTechScore(),
                gc.getGame().getInitTech(),
                gc.getGame().getMaxTech(),
                gc.getDefineINT("SCORE_TECH_FACTOR"),
                True,
                bFinal,
                bVictory,
            )
            iWondersScore = self.getScoreComponentRFCE(
                gc.getPlayer(ePlayer).getWondersScore(),
                gc.getGame().getInitWonders(),
                gc.getGame().getMaxWonders(),
                gc.getDefineINT("SCORE_WONDER_FACTOR"),
                False,
                bFinal,
                bVictory,
            )
            iUHVDone = 0
            for iUHV in range(3):
                if gc.getPlayer(ePlayer).getUHV(iUHV) == 1:
                    iUHVDone += 1
            iUHVScore = iUHVDone * 3000
            if iUHVDone == 3:  # if finished all 3 UHV conditions
                iUHVScore += 6000
            return int(iPopulationScore + iLandScore + iWondersScore + iTechScore + iUHVScore)

    def getScoreComponentRFCE(
        self, iRawScore, iInitial, iMax, iFactor, bExponential, bFinal, bVictory
    ):
        # 3Miro: to compensate for the late starts, we remove the time dependence for the final score
        if bFinal and bVictory:
            fTurnRatio = 1
            if bExponential and (iInitial != 0):
                fRatio = iMax / iInitial
                iMax = iInitial * pow(fRatio, fTurnRatio)
            else:
                iMax = iInitial + fTurnRatio * (iMax - iInitial)
        iFree = (gc.getDefineINT("SCORE_FREE_PERCENT") * iMax) / 100
        if (iFree + iMax) != 0:
            iScore = (iFactor * (iRawScore + iFree)) / (iFree + iMax)
        else:
            iScore = iFactor
        if bVictory:
            iScore = ((100 + gc.getDefineINT("SCORE_VICTORY_PERCENT")) * iScore) / 100
        if bFinal:
            iScore = (
                (
                    100
                    + gc.getDefineINT("SCORE_HANDICAP_PERCENT_OFFSET")
                    + (
                        gc.getGame().getHandicapType()
                        * gc.getDefineINT("SCORE_HANDICAP_PERCENT_PER")
                    )
                )
                * iScore
            ) / 100
        return int(iScore)

    def doHolyCity(self):
        return False

    def doHolyCityTech(self, argsList):
        eTeam = argsList[0]
        ePlayer = argsList[1]
        eTech = argsList[2]
        bFirst = argsList[3]
        return False

    def doGold(self, argsList):
        ePlayer = argsList[0]
        return False

    def doResearch(self, argsList):
        ePlayer = argsList[0]
        return False

    def doGoody(self, argsList):
        ePlayer = argsList[0]
        pPlot = argsList[1]
        pUnit = argsList[2]
        return False

    def doGrowth(self, argsList):
        pCity = argsList[0]
        return False

    def doProduction(self, argsList):
        pCity = argsList[0]
        return False

    def doCulture(self, argsList):
        pCity = argsList[0]
        return False

    def doPlotCulture(self, argsList):
        pCity = argsList[0]
        bUpdate = argsList[1]
        ePlayer = argsList[2]
        iCultureRate = argsList[3]
        return False

    def doReligion(self, argsList):
        pCity = argsList[0]
        return False

    def cannotSpreadReligion(self, argsList):
        iOwner, iUnitID, iReligion, iX, iY = argsList[0]
        return False

    def doGreatPeople(self, argsList):
        pCity = argsList[0]
        return False

    # Absinthe: not used in RFCE, we can remove it
    # def doMeltdown(self,argsList):
    #     pCity = argsList[0]
    #     return False

    def doReviveActivePlayer(self, argsList):
        "allows you to perform an action after an AIAutoPlay"
        iPlayer = argsList[0]
        return False

    def doPillageGold(self, argsList):
        "controls the gold result of pillaging"
        pPlot = argsList[0]
        pUnit = argsList[1]

        pillage_gold = gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold()

        value = rand(pillage_gold) + rand(pillage_gold)
        value += (pUnit.getPillageChange() * value) / 100
        return value

    def doCityCaptureGold(self, argsList):
        "controls the gold result of capturing a city"

        pOldCity = argsList[0]

        iCaptureGold = 0

        iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
        iCaptureGold += pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION")
        iCaptureGold += rand(gc.getDefineINT("CAPTURE_GOLD_RAND1"))
        iCaptureGold += rand(gc.getDefineINT("CAPTURE_GOLD_RAND2"))

        if gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0:
            iCaptureGold *= cyIntRange(
                (turn() - pOldCity.getGameTurnAcquired()),
                0,
                gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"),
            )
            iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")

        return iCaptureGold

    def citiesDestroyFeatures(self, argsList):
        iX, iY = argsList
        return True

    def canFoundCitiesOnWater(self, argsList):
        iX, iY = argsList
        return False

    def doCombat(self, argsList):
        pSelectionGroup, pDestPlot = argsList
        return False

    def getConscriptUnitType(self, argsList):
        iPlayer = argsList[0]
        iConscriptUnitType = (
            -1
        )  # return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system
        return iConscriptUnitType

    def getCityFoundValue(self, argsList):
        iPlayer, iPlotX, iPlotY = argsList
        iFoundValue = -1  # Any value besides -1 will be used
        return iFoundValue

    def canPickPlot(self, argsList):
        pPlot = argsList[0]
        return True

    def getUnitCostMod(self, argsList):
        iPlayer, iUnit = argsList
        iCostMod = -1  # Any value > 0 will be used
        return iCostMod

    def getBuildingCostMod(self, argsList):
        iPlayer, iCityID, iBuilding = argsList
        pPlayer = gc.getPlayer(iPlayer)
        pCity = pPlayer.getCity(iCityID)

        iCostMod = -1  # Any value > 1 will be used
        iDiscount = 0

        # Absinthe: Borgund Stave Church start
        if pPlayer.countNumBuildings(Wonder.BORGUND_STAVE_CHURCH.value) > 0:
            if Building.PAGAN_SHRINE.value <= iBuilding <= Building.RELIQUARY.value:
                iDiscount += 40
        # Absinthe: Borgund Stave Church end

        # Absinthe: Blue Mosque start
        if pPlayer.countNumBuildings(Wonder.BLUE_MOSQUE.value) > 0:
            if pPlayer.getCapitalCity().getNumActiveBuilding(iBuilding) and not pCity.isCapital():
                iDiscount += 20
        # Absinthe: Blue Mosque end

        if iDiscount > 0:
            iCostMod = 100 - iDiscount
        return iCostMod

    def canUpgradeAnywhere(self, argsList):
        pUnit = argsList
        bCanUpgradeAnywhere = 0
        return bCanUpgradeAnywhere

    def getWidgetHelp(self, argsList):
        # 3Miro and sedna17, saint and prosecutor Info
        eWidgetType, iData1, iData2, bOption = argsList
        if iData1 == 666:
            return text("TXT_KEY_CLEANSE_RELIGION_MOUSE_OVER")
        elif iData1 == 1618:
            return text("TXT_KEY_FAITH_SAINT")
        elif iData1 == 1919:
            return text("TXT_KEY_MERCENARY_HELP")
        elif iData1 == 1920:
            return text("TXT_KEY_BARBONLY_HELP")
        ## Platy WorldBuilder ##
        elif eWidgetType == WidgetTypes.WIDGET_PYTHON:
            if iData1 == 1027:
                return text("TXT_KEY_WB_PLOT_DATA")
            elif iData1 == 1028:
                return gc.getGameOptionInfo(iData2).getHelp()
            elif iData1 == 1029:
                if iData2 == 0:
                    sText = text("TXT_KEY_WB_PYTHON")
                    sText += "\n" + text("[ICON_BULLET]") + "onFirstContact"
                    sText += "\n" + text("[ICON_BULLET]") + "onChangeWar"
                    sText += "\n" + text("[ICON_BULLET]") + "onVassalState"
                    sText += "\n" + text("[ICON_BULLET]") + "onCityAcquired"
                    sText += "\n" + text("[ICON_BULLET]") + "onCityBuilt"
                    sText += "\n" + text("[ICON_BULLET]") + "onCultureExpansion"
                    sText += "\n" + text("[ICON_BULLET]") + "onGoldenAge"
                    sText += "\n" + text("[ICON_BULLET]") + "onEndGoldenAge"
                    sText += "\n" + text("[ICON_BULLET]") + "onGreatPersonBorn"
                    sText += "\n" + text("[ICON_BULLET]") + "onPlayerChangeStateReligion"
                    sText += "\n" + text("[ICON_BULLET]") + "onReligionFounded"
                    sText += "\n" + text("[ICON_BULLET]") + "onReligionSpread"
                    sText += "\n" + text("[ICON_BULLET]") + "onReligionRemove"
                    sText += "\n" + text("[ICON_BULLET]") + "onCorporationFounded"
                    sText += "\n" + text("[ICON_BULLET]") + "onCorporationSpread"
                    sText += "\n" + text("[ICON_BULLET]") + "onCorporationRemove"
                    sText += "\n" + text("[ICON_BULLET]") + "onUnitCreated"
                    sText += "\n" + text("[ICON_BULLET]") + "onUnitLost"
                    sText += "\n" + text("[ICON_BULLET]") + "onUnitPromoted"
                    sText += "\n" + text("[ICON_BULLET]") + "onBuildingBuilt"
                    sText += "\n" + text("[ICON_BULLET]") + "onProjectBuilt"
                    sText += "\n" + text("[ICON_BULLET]") + "onTechAcquired"
                    sText += "\n" + text("[ICON_BULLET]") + "onImprovementBuilt"
                    sText += "\n" + text("[ICON_BULLET]") + "onImprovementDestroyed"
                    sText += "\n" + text("[ICON_BULLET]") + "onRouteBuilt"
                    sText += "\n" + text("[ICON_BULLET]") + "onPlotRevealed"
                    return sText
                elif iData2 == 1:
                    return text("TXT_KEY_WB_PLAYER_DATA")
                elif iData2 == 2:
                    return text("TXT_KEY_WB_TEAM_DATA")
                elif iData2 == 3:
                    return text("TXT_KEY_PEDIA_CATEGORY_TECH")
                elif iData2 == 4:
                    return text("TXT_KEY_PEDIA_CATEGORY_PROJECT")
                elif iData2 == 5:
                    return (
                        text("TXT_KEY_PEDIA_CATEGORY_UNIT")
                        + " + "
                        + text("TXT_KEY_CONCEPT_CITIES")
                    )
                elif iData2 == 6:
                    return text("TXT_KEY_PEDIA_CATEGORY_PROMOTION")
                elif iData2 == 7:
                    return text("TXT_KEY_WB_CITY_DATA2")
                elif iData2 == 8:
                    return text("TXT_KEY_PEDIA_CATEGORY_BUILDING")
                elif iData2 == 9:
                    return "Platy Builder\nVersion: 4.17b"
                elif iData2 == 10:
                    return text("TXT_KEY_CONCEPT_EVENTS")
                elif iData2 == 11:
                    return text("TXT_KEY_WB_RIVER_PLACEMENT")
                elif iData2 == 12:
                    return text("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT")
                elif iData2 == 13:
                    return text("TXT_KEY_PEDIA_CATEGORY_BONUS")
                elif iData2 == 14:
                    return text("TXT_KEY_WB_PLOT_TYPE")
                elif iData2 == 15:
                    return text("TXT_KEY_CONCEPT_TERRAIN")
                elif iData2 == 16:
                    return text("TXT_KEY_PEDIA_CATEGORY_ROUTE")
                elif iData2 == 17:
                    return text("TXT_KEY_PEDIA_CATEGORY_FEATURE")
                elif iData2 == 18:
                    return text("TXT_KEY_MISSION_BUILD_CITY")
                elif iData2 == 19:
                    return text("TXT_KEY_WB_ADD_BUILDINGS")
                elif iData2 == 20:
                    return text("TXT_KEY_PEDIA_CATEGORY_RELIGION")
                elif iData2 == 21:
                    return text("TXT_KEY_CONCEPT_CORPORATIONS")
                elif iData2 == 22:
                    return text("TXT_KEY_ESPIONAGE_CULTURE")
                elif iData2 == 23:
                    return text("TXT_KEY_PITBOSS_GAME_OPTIONS")
                elif iData2 == 24:
                    return text("TXT_KEY_WB_SENSIBILITY")
                elif iData2 == 27:
                    return text("TXT_KEY_WB_ADD_UNITS")
                elif iData2 == 28:
                    return text("TXT_KEY_WB_TERRITORY")
                elif iData2 == 29:
                    return text("TXT_KEY_WB_ERASE_ALL_PLOTS")
                elif iData2 == 30:
                    return text("TXT_KEY_WB_REPEATABLE")
                elif iData2 == 31:
                    return text("TXT_KEY_PEDIA_HIDE_INACTIVE")
                elif iData2 == 32:
                    return text("TXT_KEY_WB_STARTING_PLOT")
                elif iData2 == 33:
                    return text("TXT_KEY_INFO_SCREEN")
                elif iData2 == 34:
                    return text("TXT_KEY_CONCEPT_TRADE")
            elif iData1 > 1029 and iData1 < 1040:
                if iData1 % 2:
                    return "-"
                return "+"
            elif iData1 == 1041:
                return text("TXT_KEY_WB_KILL")
            elif iData1 == 1042:
                return text("TXT_KEY_MISSION_SKIP")
            elif iData1 == 1043:
                if iData2 == 0:
                    return text("TXT_KEY_WB_DONE")
                elif iData2 == 1:
                    return text("TXT_KEY_WB_FORTIFY")
                elif iData2 == 2:
                    return text("TXT_KEY_WB_WAIT")
            elif iData1 == 6785:
                return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
            elif iData1 == 6787:
                return gc.getProcessInfo(iData2).getDescription()
            elif iData1 == 6788:
                if iData2 == -1:
                    return text("TXT_KEY_CULTURELEVEL_NONE")
                return gc.getRouteInfo(iData2).getDescription()
            ## City Hover Text ##
            elif iData1 > 7199 and iData1 < 7300:
                iPlayer = iData1 - 7200
                pPlayer = gc.getPlayer(iPlayer)
                pCity = pPlayer.getCity(iData2)
                if CyGame().GetWorldBuilderMode():
                    sText = "<font=3>"
                    if pCity.isCapital():
                        sText += text("[ICON_STAR]")
                    elif pCity.isGovernmentCenter():
                        sText += text("[ICON_SILVER_STAR]")
                    sText += u"%s: %d<font=2>" % (pCity.getName(), pCity.getPopulation())
                    sTemp = ""
                    if pCity.isConnectedToCapital(iPlayer):
                        sTemp += text("[ICON_TRADE]")
                    for i in xrange(gc.getNumReligionInfos()):  # type: ignore
                        if pCity.isHolyCityByType(i):
                            sTemp += u"%c" % (gc.getReligionInfo(i).getHolyCityChar())
                        elif pCity.isHasReligion(i):
                            sTemp += u"%c" % (gc.getReligionInfo(i).getChar())

                    for i in xrange(gc.getNumCorporationInfos()):  # type: ignore
                        if pCity.isHeadquartersByType(i):
                            sTemp += u"%c" % (gc.getCorporationInfo(i).getHeadquarterChar())
                        elif pCity.isHasCorporation(i):
                            sTemp += u"%c" % (gc.getCorporationInfo(i).getChar())
                    if len(sTemp) > 0:
                        sText += "\n" + sTemp

                    iMaxDefense = pCity.getTotalDefense(False)
                    if iMaxDefense > 0:
                        sText += u"\n%s: " % (text("[ICON_DEFENSE]"))
                        iCurrent = pCity.getDefenseModifier(False)
                        if iCurrent != iMaxDefense:
                            sText += u"%d/" % (iCurrent)
                        sText += u"%d%%" % (iMaxDefense)

                    sText += u"\n%s: %d/%d" % (
                        text("[ICON_FOOD]"),
                        pCity.getFood(),
                        pCity.growthThreshold(),
                    )
                    iFoodGrowth = pCity.foodDifference(True)
                    if iFoodGrowth != 0:
                        sText += u" %+d" % (iFoodGrowth)

                    if pCity.isProduction():
                        sText += u"\n%s:" % (text("[ICON_PRODUCTION]"))
                        if not pCity.isProductionProcess():
                            sText += u" %d/%d" % (
                                pCity.getProduction(),
                                pCity.getProductionNeeded(),
                            )
                            iProduction = pCity.getCurrentProductionDifference(False, True)
                            if iProduction != 0:
                                sText += u" %+d" % (iProduction)
                        sText += u" (%s)" % (pCity.getProductionName())

                    iGPRate = pCity.getGreatPeopleRate()
                    iProgress = pCity.getGreatPeopleProgress()
                    if iGPRate > 0 or iProgress > 0:
                        sText += u"\n%s: %d/%d %+d" % (
                            text("[ICON_GREATPEOPLE]"),
                            iProgress,
                            pPlayer.greatPeopleThreshold(False),
                            iGPRate,
                        )

                    sText += u"\n%s: %d/%d (%s)" % (
                        text("[ICON_CULTURE]"),
                        pCity.getCulture(iPlayer),
                        pCity.getCultureThreshold(),
                        gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription(),
                    )

                    lTemp = []
                    for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):  # type: ignore
                        iAmount = pCity.getCommerceRateTimes100(i)
                        if iAmount <= 0:
                            continue
                        sTemp = u"%d.%02d%c" % (
                            pCity.getCommerceRate(i),
                            pCity.getCommerceRateTimes100(i) % 100,
                            gc.getCommerceInfo(i).getChar(),
                        )
                        lTemp.append(sTemp)
                    if len(lTemp) > 0:
                        sText += "\n"
                        for i in xrange(len(lTemp)):  # type: ignore
                            sText += lTemp[i]
                            if i < len(lTemp) - 1:
                                sText += ", "

                    iMaintenance = pCity.getMaintenanceTimes100()
                    if iMaintenance != 0:
                        sText += (
                            "\n"
                            + text("[COLOR_WARNING_TEXT]")
                            + text("INTERFACE_CITY_MAINTENANCE")
                            + " </color>"
                        )
                        sText += u"-%d.%02d%c" % (
                            iMaintenance / 100,
                            iMaintenance % 100,
                            gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(),
                        )

                    lBuildings = []
                    lWonders = []
                    for i in xrange(gc.getNumBuildingInfos()):  # type: ignore
                        if pCity.isHasBuilding(i):
                            Info = gc.getBuildingInfo(i)
                            if isLimitedWonderClass(Info.getBuildingClassType()):
                                lWonders.append(Info.getDescription())
                            else:
                                lBuildings.append(Info.getDescription())
                    if len(lBuildings) > 0:
                        lBuildings.sort()
                        sText += (
                            "\n"
                            + text("[COLOR_BUILDING_TEXT]")
                            + text("TXT_KEY_PEDIA_CATEGORY_BUILDING")
                            + ": </color>"
                        )
                        for i in xrange(len(lBuildings)):  # type: ignore
                            sText += lBuildings[i]
                            if i < len(lBuildings) - 1:
                                sText += ", "
                    if len(lWonders) > 0:
                        lWonders.sort()
                        sText += (
                            "\n"
                            + text("[COLOR_SELECTED_TEXT]")
                            + text("TXT_KEY_CONCEPT_WONDERS")
                            + ": </color>"
                        )
                        for i in xrange(len(lWonders)):  # type: ignore
                            sText += lWonders[i]
                            if i < len(lWonders) - 1:
                                sText += ", "
                    sText += "</font>"
                    return sText
            ## Religion Widget Text##
            elif iData1 == 7869:
                return CyGameTextMgr().parseReligionInfo(iData2, False)
            ## Building Widget Text##
            elif iData1 == 7870:
                return CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)
            ## Tech Widget Text##
            elif iData1 == 7871:
                if iData2 == -1:
                    return text("TXT_KEY_CULTURELEVEL_NONE")
                return CyGameTextMgr().getTechHelp(iData2, False, False, False, False, -1)
            ## Civilization Widget Text##
            elif iData1 == 7872:
                iCiv = iData2 % 10000
                return CyGameTextMgr().parseCivInfos(iCiv, False)
            ## Promotion Widget Text##
            elif iData1 == 7873:
                return CyGameTextMgr().getPromotionHelp(iData2, False)
            ## Feature Widget Text##
            elif iData1 == 7874:
                if iData2 == -1:
                    return text("TXT_KEY_CULTURELEVEL_NONE")
                iFeature = iData2 % 10000
                return CyGameTextMgr().getFeatureHelp(iFeature, False)
            ## Terrain Widget Text##
            elif iData1 == 7875:
                return CyGameTextMgr().getTerrainHelp(iData2, False)
            ## Leader Widget Text##
            elif iData1 == 7876:
                iLeader = iData2 % 10000
                return CyGameTextMgr().parseLeaderTraits(iLeader, -1, False, False)
            ## Improvement Widget Text##
            elif iData1 == 7877:
                if iData2 == -1:
                    return text("TXT_KEY_CULTURELEVEL_NONE")
                return CyGameTextMgr().getImprovementHelp(iData2, False)
            ## Bonus Widget Text##
            elif iData1 == 7878:
                if iData2 == -1:
                    return text("TXT_KEY_CULTURELEVEL_NONE")
                return CyGameTextMgr().getBonusHelp(iData2, False)
            ## Specialist Widget Text##
            elif iData1 == 7879:
                return CyGameTextMgr().getSpecialistHelp(iData2, False)
            ## Yield Text##
            elif iData1 == 7880:
                return gc.getYieldInfo(iData2).getDescription()
            ## Commerce Text##
            elif iData1 == 7881:
                return gc.getCommerceInfo(iData2).getDescription()
            ## Build Text##
            elif iData1 == 7882:
                return gc.getBuildInfo(iData2).getDescription()
            ## Corporation Screen ##
            elif iData1 == 8201:
                return CyGameTextMgr().parseCorporationInfo(iData2, False)
            ## Military Screen ##
            elif iData1 == 8202:
                if iData2 == -1:
                    return text("TXT_KEY_PEDIA_ALL_UNITS")
                return CyGameTextMgr().getUnitHelp(iData2, False, False, False, None)
            elif iData1 > 8299 and iData1 < 8400:
                iPlayer = iData1 - 8300
                pUnit = gc.getPlayer(iPlayer).getUnit(iData2)
                sText = CyGameTextMgr().getSpecificUnitHelp(pUnit, True, False)
                if CyGame().GetWorldBuilderMode():
                    sText += "\n" + text("TXT_KEY_WB_UNIT") + " ID: " + str(iData2)
                    sText += "\n" + text("TXT_KEY_WB_GROUP") + " ID: " + str(pUnit.getGroupID())
                    sText += "\n" + "X: " + str(pUnit.getX()) + ", Y: " + str(pUnit.getY())
                    sText += "\n" + text("TXT_KEY_WB_AREA_ID") + ": " + str(pUnit.plot().getArea())
                return sText
            ## Civics Screen ##
            elif iData1 == 8205 or iData1 == 8206:
                sText = CyGameTextMgr().parseCivicInfo(iData2, False, True, False)
                if gc.getCivicInfo(iData2).getUpkeep() > -1:
                    sText += (
                        "\n"
                        + gc.getUpkeepInfo(gc.getCivicInfo(iData2).getUpkeep()).getDescription()
                    )
                else:
                    sText += "\n" + text("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP")
                return sText
        ## Ultrapack ##

        # Espionage Advisor
        if eWidgetType == WidgetTypes.WIDGET_ESPIONAGE_SELECT_PLAYER:
            pPlayer = gc.getPlayer(iData1)
            szHelp = CyTranslator().changeTextColor(
                pPlayer.getName(), gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")
            )
            szHelp += "\n"
            szHelp += pPlayer.getCivilizationDescription(0)
            szHelp += "\n\n"
            szHelp += CyGameTextMgr().getAttitudeString(iData1, iData2)
            return szHelp

        elif eWidgetType == WidgetTypes.WIDGET_ESPIONAGE_SELECT_CITY:
            return " "

        elif eWidgetType == WidgetTypes.WIDGET_ESPIONAGE_SELECT_MISSION:
            MissionInfo = gc.getEspionageMissionInfo(iData1)
            szHelp = CyTranslator().changeTextColor(
                MissionInfo.getDescription(), gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")
            )
            szHelp += "\n"
            szHelp += MissionInfo.getHelp()
            return szHelp

        # Go to City
        elif eWidgetType == WidgetTypes.WIDGET_GO_TO_CITY:
            szHelp = "Locate this city in the world"
            return szHelp
        return u""

    # Absinthe: 1st turn anarchy instability, called form C++ CvPlayer::revolution and CvPlayer::convert
    def doAnarchyInstability(self, argsList):
        iPlayer = argsList[0]
        pPlayer = gc.getPlayer(iPlayer)
        sta.recalcCivicCombos(iPlayer)
        sta.recalcEpansion(iPlayer)
        iNumCities = pPlayer.getNumCities()
        # anarchy instability should appear right on revolution / converting, not one turn later
        if iPlayer != Civ.PRUSSIA.value:  # Prussian UP
            if pPlayer.isHuman():
                # anarchy swing instability
                pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 8)
                pPlayer.setStabSwingAnarchy(
                    8
                )  # the value doesn't really matter, but has to remain > 0 after the first StabSwingAnarchy check of sta.updateBaseStability
                # anarchy base instability
                pPlayer.changeStabilityBase(
                    StabilityCategory.CIVICS.value, min(0, max(-2, (-iNumCities + 4) / 7))
                )  # 0 with 1-4 cities, -1 with 5-11 cities, -2 with at least 12 cities

            else:
                # anarchy swing instability
                pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 4)  # reduced for the AI
                pPlayer.setStabSwingAnarchy(
                    4
                )  # the value doesn't really matter, but has to remain > 0 after the first StabSwingAnarchy check of sta.updateBaseStability
                # anarchy base instability
                pPlayer.changeStabilityBase(
                    StabilityCategory.CIVICS.value, min(0, max(-1, (-iNumCities + 6) / 7))
                )  # reduced for the AI: 0 with 1-6 cities, -1 with at least 7

        lResult = 1
        return lResult

    def getUpgradePriceOverride(self, argsList):
        iPlayer, iUnitID, iUnitTypeUpgrade = argsList
        return -1  # Any value 0 or above will be used

    def getExperienceNeeded(self, argsList):
        # use this function to set how much experience a unit needs
        iLevel, iOwner = argsList

        iExperienceNeeded = 0

        # regular epic game experience
        iExperienceNeeded = iLevel * iLevel + 1
        iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
        if 0 != iModifier:
            iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100  # ROUND UP
        return iExperienceNeeded
