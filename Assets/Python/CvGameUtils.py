## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Implementation of miscellaneous game functions

from CoreData import CIVILIZATIONS
from CoreFunctions import get_religion_by_id
from CoreTypes import Civ, Religion, StabilityCategory
import CvUtil
from CvPythonExtensions import *
from MiscData import RELIGION_PERSECUTION_ORDER
import PyHelpers  # Absinthe
import XMLConsts as xml  # Absinthe
import RFCUtils
import Stability  # Absinthe

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer  # Absinthe
utils = RFCUtils.RFCUtils()  # Absinthe
sta = Stability.Stability()  # Absinthe


class CvGameUtils:
    "Miscellaneous game functions"

    def __init__(self):
        pass

    def isVictoryTest(self):
        if gc.getGame().getElapsedGameTurns() > 10:
            return True
        else:
            return False

    def isVictory(self, argsList):
        eVictory = argsList[0]
        return True

    def isPlayerResearch(self, argsList):
        ePlayer = argsList[0]
        return True

    def getExtraCost(self, argsList):
        ePlayer = argsList[0]
        pPlayer = gc.getPlayer(ePlayer)
        iExtraCost = 0
        return iExtraCost

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

    def canRaze(self, argsList):
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
            if pUnit.getUnitType() == xml.iProsecutor:
                return self.doInquisitorCore_AI(pUnit)
        return False

    # Absinthe: Inquisitor AI, this is also called from the .dll, CvCityAI::AI_chooseUnit
    def isHasPurgeTarget(self, iCiv, bReportCity):
        iStateReligion = gc.getPlayer(iCiv).getStateReligion()
        iTolerance = CIVILIZATIONS[iCiv].religion.tolerance
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
                    in [
                        Religion.CATHOLICISM,
                        Religion.ORTHODOXY,
                        Religion.PROTESTANTISM,
                    ]
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
                        for iBuilding in xrange(gc.getNumBuildingInfos()):  # type: ignore
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
            utils.prosecute(pCity.getX(), pCity.getY(), pUnit.getID())

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
    # 	pCity = argsList[0]
    # 	return False

    def doReviveActivePlayer(self, argsList):
        "allows you to perform an action after an AIAutoPlay"
        iPlayer = argsList[0]
        return False

    def doPillageGold(self, argsList):
        "controls the gold result of pillaging"
        pPlot = argsList[0]
        pUnit = argsList[1]

        iPillageGold = 0
        iPillageGold = CyGame().getSorenRandNum(
            gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 1"
        )
        iPillageGold += CyGame().getSorenRandNum(
            gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 2"
        )

        iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100

        return iPillageGold

    def doCityCaptureGold(self, argsList):
        "controls the gold result of capturing a city"

        pOldCity = argsList[0]

        iCaptureGold = 0

        iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
        iCaptureGold += pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION")
        iCaptureGold += CyGame().getSorenRandNum(
            gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1"
        )
        iCaptureGold += CyGame().getSorenRandNum(
            gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2"
        )

        if gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0:
            iCaptureGold *= cyIntRange(
                (CyGame().getGameTurn() - pOldCity.getGameTurnAcquired()),
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
        if pPlayer.countNumBuildings(xml.iBorgundStaveChurch) > 0:
            if xml.iPaganShrine <= iBuilding <= xml.iReliquary:
                iDiscount += 40
        # Absinthe: Borgund Stave Church end

        # Absinthe: Blue Mosque start
        if pPlayer.countNumBuildings(xml.iBlueMosque) > 0:
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
            return CyTranslator().getText("TXT_KEY_CLEANSE_RELIGION_MOUSE_OVER", ())
        elif iData1 == 1618:
            return CyTranslator().getText("TXT_KEY_FAITH_SAINT", ())
        elif iData1 == 1919:
            return CyTranslator().getText("TXT_KEY_MERCENARY_HELP", ())
        elif iData1 == 1920:
            return CyTranslator().getText("TXT_KEY_BARBONLY_HELP", ())
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
