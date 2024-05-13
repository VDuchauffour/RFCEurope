## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## #####   WARNING - MODIFYING THE FUNCTION NAMES OF THIS FILE IS PROHIBITED  #####
##
## The app specifically calls the functions as they are named. Use this file to pass
## args to another file that contains your modifications
##
## MODDERS - If you create a GameUtils file, update the CvGameInterfaceFile reference to point to your new file

#
import CvGameInterfaceFile
from CvPythonExtensions import *

# globals
gc = CyGlobalContext()
normalGameUtils = CvGameInterfaceFile.GameUtils


def gameUtils():
    "replace normalGameUtils with your mod version"
    return normalGameUtils


def isVictoryTest():
    return gameUtils().isVictoryTest()


def isVictory(argsList):
    return gameUtils().isVictory(argsList)


def isPlayerResearch(argsList):
    return gameUtils().isPlayerResearch(argsList)


def getExtraCost(argsList):
    return gameUtils().getExtraCost(argsList)


def createBarbarianCities():
    return gameUtils().createBarbarianCities()


def createBarbarianUnits():
    return gameUtils().createBarbarianUnits()


def skipResearchPopup(argsList):
    return gameUtils().skipResearchPopup(argsList)


def showTechChooserButton(argsList):
    return gameUtils().showTechChooserButton(argsList)


def getFirstRecommendedTech(argsList):
    return gameUtils().getFirstRecommendedTech(argsList)


def getSecondRecommendedTech(argsList):
    return gameUtils().getSecondRecommendedTech(argsList)


def skipProductionPopup(argsList):
    return gameUtils().skipProductionPopup(argsList)


def canRazeCity(argsList):
    return gameUtils().canRazeCity(argsList)


def canDeclareWar(argsList):
    return gameUtils().canDeclareWar(argsList)


def showExamineCityButton(argsList):
    return gameUtils().showExamineCityButton(argsList)


def getRecommendedUnit(argsList):
    return gameUtils().getRecommendedUnit(argsList)


def getRecommendedBuilding(argsList):
    return gameUtils().getRecommendedBuilding(argsList)


def updateColoredPlots():
    return gameUtils().updateColoredPlots()


def isActionRecommended(argsList):
    return gameUtils().isActionRecommended(argsList)


def unitCannotMoveInto(argsList):
    return gameUtils().unitCannotMoveInto(argsList)


def cannotHandleAction(argsList):
    return gameUtils().cannotHandleAction(argsList)


def canBuild(argsList):
    return gameUtils().canBuild(argsList)


def cannotFoundCity(argsList):
    return gameUtils().cannotFoundCity(argsList)


def cannotSelectionListMove(argsList):
    return gameUtils().cannotSelectionListMove(argsList)


def cannotSelectionListGameNetMessage(argsList):
    return gameUtils().cannotSelectionListGameNetMessage(argsList)


def cannotDoControl(argsList):
    return gameUtils().cannotDoControl(argsList)


def canResearch(argsList):
    return gameUtils().canResearch(argsList)


def cannotResearch(argsList):
    return gameUtils().cannotResearch(argsList)


def canDoCivic(argsList):
    return gameUtils().canDoCivic(argsList)


def cannotDoCivic(argsList):
    return gameUtils().cannotDoCivic(argsList)


def canTrain(argsList):
    return gameUtils().canTrain(argsList)


def cannotTrain(argsList):
    return gameUtils().cannotTrain(argsList)


def canConstruct(argsList):
    return gameUtils().canConstruct(argsList)


def cannotConstruct(argsList):
    return gameUtils().cannotConstruct(argsList)


def canCreate(argsList):
    return gameUtils().canCreate(argsList)


def cannotCreate(argsList):
    return gameUtils().cannotCreate(argsList)


def canMaintain(argsList):
    return gameUtils().canMaintain(argsList)


def cannotMaintain(argsList):
    return gameUtils().cannotMaintain(argsList)


def AI_chooseTech(argsList):
    "AI chooses what to research"
    return gameUtils().AI_chooseTech(argsList)


def AI_chooseProduction(argsList):
    "AI chooses city production"
    return gameUtils().AI_chooseProduction(argsList)


def AI_unitUpdate(argsList):
    "AI moves units - return 0 to let AI handle it, return 1 to say that the move is handled in python"
    return gameUtils().AI_unitUpdate(argsList)


# Absinthe: new code for AI persecution - handled through python
def isHasPurgeTarget(argsList):
    "AI has target for persecution - return 0 if no possible targets, return 1 if there are at least one"
    return gameUtils().isHasPurgeTarget(argsList)


def AI_doWar(argsList):
    "AI decides whether to make war or peace - return 0 to let AI handle it, return 1 to say that the move is handled in python"
    return gameUtils().AI_doWar(argsList)


def AI_doDiplo(argsList):
    "AI decides does diplomacy for the turn - return 0 to let AI handle it, return 1 to say that the move is handled in python"
    return gameUtils().AI_doDiplo(argsList)


def calculateScore(argsList):
    return gameUtils().calculateScore(argsList)


def doHolyCity():
    return gameUtils().doHolyCity()


def doHolyCityTech(argsList):
    return gameUtils().doHolyCityTech(argsList)


def doGold(argsList):
    return gameUtils().doGold(argsList)


def doResearch(argsList):
    return gameUtils().doResearch(argsList)


def doGoody(argsList):
    return gameUtils().doGoody(argsList)


def doGrowth(argsList):
    return gameUtils().doGrowth(argsList)


def doProduction(argsList):
    return gameUtils().doProduction(argsList)


def doCulture(argsList):
    return gameUtils().doCulture(argsList)


def doPlotCulture(argsList):
    return gameUtils().doPlotCulture(argsList)


def doReligion(argsList):
    return gameUtils().doReligion(argsList)


def doGreatPeople(argsList):
    return gameUtils().doGreatPeople(argsList)


# Absinthe: not used in RFCE, we can remove it
# def doMeltdown(argsList):
# 	return gameUtils().doMeltdown(argsList)


def doReviveActivePlayer(argsList):
    return gameUtils().doReviveActivePlayer(argsList)


def doPillageGold(argsList):
    return gameUtils().doPillageGold(argsList)


def doCityCaptureGold(argsList):
    return gameUtils().doCityCaptureGold(argsList)


def citiesDestroyFeatures(argsList):
    return gameUtils().citiesDestroyFeatures(argsList)


def canFoundCitiesOnWater(argsList):
    return gameUtils().canFoundCitiesOnWater(argsList)


def doCombat(argsList):
    return gameUtils().doCombat(argsList)


def getConscriptUnitType(argsList):
    return gameUtils().getConscriptUnitType(argsList)


def getCityFoundValue(argsList):
    return gameUtils().getCityFoundValue(argsList)


def canPickPlot(argsList):
    return gameUtils().canPickPlot(argsList)


def getUnitCostMod(argsList):
    return gameUtils().getUnitCostMod(argsList)


def getBuildingCostMod(argsList):
    return gameUtils().getBuildingCostMod(argsList)


def canUpgradeAnywhere(argsList):
    return gameUtils().canUpgradeAnywhere(argsList)


def getWidgetHelp(argsList):
    return gameUtils().getWidgetHelp(argsList)


# Absinthe
def doAnarchyInstability(argsList):
    return gameUtils().doAnarchyInstability(argsList)


def getUpgradePriceOverride(argsList):
    return gameUtils().getUpgradePriceOverride(argsList)


def getExperienceNeeded(argsList):
    return gameUtils().getExperienceNeeded(argsList)
