# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# CvRandomEventInterface.py
#
# These functions are App Entry Points from C++
# WARNING: These function names should not be changed
# WARNING: These functions can not be placed into a class
#
# No other modules should import this
#
from random import choice
from CoreStructures import turn
from CoreTypes import Civ
import CvUtil
from CvPythonExtensions import *

from PyUtils import percentage_chance, rand

gc = CyGlobalContext()
localText = CyTranslator()


######## BLESSED SEA ###########


def getHelpBlessedSea1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()
    iOurMinLandmass = (3 * gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()) / 2
    # Rhye
    iOurMinLandmass /= 2

    szHelp = localText.getText("TXT_KEY_EVENT_BLESSED_SEA_HELP", (iOurMinLandmass,))

    return szHelp


def canTriggerBlessedSea(argsList):
    kTriggeredData = argsList[0]
    map = gc.getMap()

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    iMapMinLandmass = 2 * gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
    iOurMaxLandmass = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers() / 2
    # Rhye
    iMapMinLandmass /= 2
    iMapMinLandmass -= 1

    if map.getNumLandAreas() < iMapMinLandmass:
        return False

    iOurLandmasses = 0
    for i in range(map.getIndexAfterLastArea()):
        area = map.getArea(i)
        if (
            not area.isNone()
            and not area.isWater()
            and area.getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
        ):
            iOurLandmasses += 1

    if iOurLandmasses > iOurMaxLandmass:
        return False

    player = gc.getPlayer(kTriggeredData.ePlayer)
    if (
        player.getUnitClassCount(
            CvUtil.findInfoTypeNum(
                gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_GALLEY"
            )
        )
        == 0
    ):
        if (
            player.getUnitClassCount(
                CvUtil.findInfoTypeNum(
                    gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_CARAVEL"
                )
            )
            == 0
        ):
            if (
                player.getUnitClassCount(
                    CvUtil.findInfoTypeNum(
                        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_GALLEON"
                    )
                )
                == 0
            ):
                return False

    return True


def canTriggerBlessedSea2(argsList):

    kTriggeredData = argsList[0]
    map = gc.getMap()
    iOurMinLandmass = (3 * gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()) / 2
    # Rhye
    iOurMinLandmass /= 2

    iOurLandmasses = 0
    for i in range(map.getIndexAfterLastArea()):
        area = map.getArea(i)
        if (
            not area.isNone()
            and not area.isWater()
            and area.getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
        ):
            iOurLandmasses += 1

    if iOurLandmasses < iOurMinLandmass:
        return False

    return True


def applyBlessedSea2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iBuilding = -1

    if -1 != kTriggeredData.eReligion:
        for i in range(gc.getNumBuildingInfos()):
            if gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(
                gc.getSpecialBuildingInfo,
                gc.getNumSpecialBuildingInfos(),
                "SPECIALBUILDING_TEMPLE",
            ):
                if gc.getBuildingInfo(i).getReligionType() == kTriggeredData.eReligion:
                    iBuilding = i
                    break

    if iBuilding == -1:
        return

    player = gc.getPlayer(kTriggeredData.ePlayer)
    (loopCity, iter) = player.firstCity(False)

    while loopCity:

        if loopCity.getPopulation() >= 5:
            if loopCity.canConstruct(iBuilding, False, False, True):
                loopCity.setNumRealBuilding(iBuilding, 1)

        (loopCity, iter) = player.nextCity(iter, False)


def canApplyBlessedSea2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iBuilding = -1

    if -1 != kTriggeredData.eReligion:
        for i in range(gc.getNumBuildingInfos()):
            if gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(
                gc.getSpecialBuildingInfo,
                gc.getNumSpecialBuildingInfos(),
                "SPECIALBUILDING_TEMPLE",
            ):
                if gc.getBuildingInfo(i).getReligionType() == kTriggeredData.eReligion:
                    iBuilding = i
                    break

    if iBuilding == -1:
        return False

    player = gc.getPlayer(kTriggeredData.ePlayer)
    (loopCity, iter) = player.firstCity(False)
    bFound = False

    while loopCity:

        if loopCity.getPopulation() >= 5:
            if loopCity.canConstruct(iBuilding, False, False, True):
                bFound = True
                break

        (loopCity, iter) = player.nextCity(iter, False)

    return bFound


######## HOLY MOUNTAIN ###########


def getHelpHolyMountain1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()
    iMinPoints = 2 * gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
    # Rhye
    iMinPoints /= 2

    iBuilding = -1
    iReligion = gc.getPlayer(kTriggeredData.ePlayer).getStateReligion()

    if -1 != iReligion:
        for i in range(gc.getNumBuildingInfos()):
            if gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(
                gc.getSpecialBuildingInfo,
                gc.getNumSpecialBuildingInfos(),
                "SPECIALBUILDING_CATHEDRAL",
            ):
                if gc.getBuildingInfo(i).getReligionType() == iReligion:
                    iBuilding = i
                    break

        szHelp = localText.getText(
            "TXT_KEY_EVENT_HOLY_MOUNTAIN_HELP",
            (
                gc.getBuildingInfo(iBuilding).getTextKey(),
                gc.getBuildingInfo(iBuilding).getTextKey(),
                iMinPoints,
            ),
        )

    return szHelp


def canTriggerHolyMountain(argsList):
    kTriggeredData = argsList[0]
    map = gc.getMap()

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if plot.getOwner() == -1:
        return True

    return False


def expireHolyMountain1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if plot is None:
        return True

    if plot.getOwner() != kTriggeredData.ePlayer and plot.getOwner() != -1:
        return True

    return False


def canTriggerHolyMountainDone(argsList):

    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    if kOrigTriggeredData is None:
        return False

    plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)
    if plot is None:
        return False

    if plot.getOwner() != kTriggeredData.ePlayer:
        return False

    return True


def canTriggerHolyMountainRevealed(argsList):

    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    if kOrigTriggeredData is None:
        return False

    iNumPoints = 0

    for i in range(gc.getNumBuildingInfos()):
        if gc.getBuildingInfo(i).getReligionType() == kOrigTriggeredData.eReligion:
            if gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(
                gc.getSpecialBuildingInfo,
                gc.getNumSpecialBuildingInfos(),
                "SPECIALBUILDING_CATHEDRAL",
            ):
                iNumPoints += 4 * player.countNumBuildings(i)
            elif gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(
                gc.getSpecialBuildingInfo,
                gc.getNumSpecialBuildingInfos(),
                "SPECIALBUILDING_TEMPLE",
            ):
                iNumPoints += player.countNumBuildings(i)
            elif gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(
                gc.getSpecialBuildingInfo,
                gc.getNumSpecialBuildingInfos(),
                "SPECIALBUILDING_MONASTERY",
            ):
                iNumPoints += player.countNumBuildings(i)

    # Rhye
    iNumPoints *= 2

    if iNumPoints < 2 * gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers():
        return False

    plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)
    if plot is None:
        return False

    plot.setRevealed(player.getTeam(), True, True, -1)

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY

    return True


def doHolyMountainRevealed(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    if kTriggeredData.ePlayer == gc.getGame().getActivePlayer():
        CyCamera().JustLookAtPlot(CyMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY))

    return 1


######## MARATHON ###########


def canTriggerMarathon(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    team = gc.getTeam(player.getTeam())

    if team.AI_getAtWarCounter(otherPlayer.getTeam()) == 1:
        (loopUnit, iter) = otherPlayer.firstUnit(False)
        while loopUnit:
            plot = loopUnit.plot()
            if not plot.isNone():
                if plot.getOwner() == kTriggeredData.ePlayer:
                    return True
            (loopUnit, iter) = otherPlayer.nextUnit(iter, False)

    return False


######## WEDDING FEUD ###########


def doWeddingFeud2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    (loopCity, iter) = player.firstCity(False)

    while loopCity:
        if loopCity.isHasReligion(kTriggeredData.eReligion):
            loopCity.changeHappinessTimer(30)
        (loopCity, iter) = player.nextCity(iter, False)

    return 1


def getHelpWeddingFeud2(argsList):
    iEvent = argsList[0]
    event = gc.getEventInfo(iEvent)
    kTriggeredData = argsList[1]
    religion = gc.getReligionInfo(kTriggeredData.eReligion)

    szHelp = localText.getText(
        "TXT_KEY_EVENT_WEDDING_FEUD_2_HELP",
        (gc.getDefineINT("TEMP_HAPPY"), 30, religion.getChar()),
    )

    return szHelp


def canDoWeddingFeud3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getGold() - 10 * player.getNumCities() < 0:
        return False

    return True


def doWeddingFeud3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iLoopPlayer)
        if loopPlayer.isAlive() and loopPlayer.getStateReligion() == player.getStateReligion():
            loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
            player.AI_changeAttitudeExtra(iLoopPlayer, 1)

    if gc.getTeam(destPlayer.getTeam()).canDeclareWar(player.getTeam()):
        if destPlayer.isHuman():
            # this works only because it's a single-player only event
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
            popupInfo.setText(
                localText.getText(
                    "TXT_KEY_EVENT_WEDDING_FEUD_OTHER_3",
                    (
                        gc.getReligionInfo(kTriggeredData.eReligion).getAdjectiveKey(),
                        player.getCivilizationShortDescriptionKey(),
                    ),
                )
            )
            popupInfo.setData1(kTriggeredData.eOtherPlayer)
            popupInfo.setData2(kTriggeredData.ePlayer)
            popupInfo.setPythonModule("CvRandomEventInterface")
            popupInfo.setOnClickedPythonCallback("weddingFeud3Callback")
            popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
            popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
            popupInfo.addPopup(kTriggeredData.eOtherPlayer)
        else:
            gc.getTeam(destPlayer.getTeam()).declareWar(
                player.getTeam(), False, WarPlanTypes.WARPLAN_LIMITED
            )

    return 1


def weddingFeud3Callback(argsList):
    iButton = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    szText = argsList[4]
    bOption1 = argsList[5]
    bOption2 = argsList[6]

    if iButton == 0:
        destPlayer = gc.getPlayer(iData1)
        player = gc.getPlayer(iData2)
        gc.getTeam(destPlayer.getTeam()).declareWar(
            player.getTeam(), False, WarPlanTypes.WARPLAN_LIMITED
        )

    return 0


def getHelpWeddingFeud3(argsList):
    iEvent = argsList[0]
    event = gc.getEventInfo(iEvent)
    kTriggeredData = argsList[1]
    religion = gc.getReligionInfo(kTriggeredData.eReligion)

    szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_3_HELP", (1, religion.getChar()))

    return szHelp


######## SPICY ###########


def canTriggerSpicy(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSpice = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_SPICES")
    iHappyBonuses = 0
    bSpices = False
    for i in range(gc.getNumBonusInfos()):
        bonus = gc.getBonusInfo(i)
        iNum = player.getNumAvailableBonuses(i)
        if iNum > 0:
            if bonus.getHappiness() > 0:
                iHappyBonuses += 1
                if iHappyBonuses > 4:
                    return False
            if i == iSpice:
                return False

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if not plot.canHaveBonus(iSpice, False):
        return False

    return True


def doSpicy2(argsList):
    # 	need this because plantations are normally not allowed unless there are already spices
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if not plot.isNone():
        plot.setImprovementType(
            CvUtil.findInfoTypeNum(
                gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_PLANTATION"
            )
        )

    return 1


def getHelpSpicy2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iPlantation = CvUtil.findInfoTypeNum(
        gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_PLANTATION"
    )
    szHelp = localText.getText(
        "TXT_KEY_EVENT_IMPROVEMENT_GROWTH", (gc.getImprovementInfo(iPlantation).getTextKey(),)
    )

    return szHelp


######## BABY BOOM ###########


def canTriggerBabyBoom(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    if team.getAtWarCount(True) > 0:
        return False

    for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
        if iLoopTeam != player.getTeam():
            if team.AI_getAtPeaceCounter(iLoopTeam) == 1:
                return True

    return False


######## BARD TALE ###########


def applyBardTale3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    player.changeGold(-10 * player.getNumCities())


def canApplyBardTale3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getGold() - 10 * player.getNumCities() < 0:
        return False

    return True


def getHelpBardTale3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    szHelp = localText.getText("TXT_KEY_EVENT_GOLD_LOST", (10 * player.getNumCities(),))

    return szHelp


######## LOOTERS ###########


def getHelpLooters3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

    szHelp = localText.getText("TXT_KEY_EVENT_LOOTERS_3_HELP", (1, 2, city.getNameKey()))

    return szHelp


def canApplyLooters3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

    iNumBuildings = 0
    for iBuilding in range(gc.getNumBuildingInfos()):
        if (
            city.getNumRealBuilding(iBuilding) > 0
            and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100
            and gc.getBuildingInfo(iBuilding).getProductionCost() > 0
            and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())
        ):
            iNumBuildings += 1

    return iNumBuildings > 0


def applyLooters3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

    iNumBuildingsDestroyed = 0

    listBuildings = []
    for iBuilding in range(gc.getNumBuildingInfos()):
        if (
            city.getNumRealBuilding(iBuilding) > 0
            and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100
            and gc.getBuildingInfo(iBuilding).getProductionCost() > 0
            and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())
        ):
            listBuildings.append(iBuilding)

    for _ in range(rand(2) + 1):
        if len(listBuildings) > 0:
            iBuilding = choice(listBuildings)
            szBuffer = localText.getText(
                "TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED",
                (gc.getBuildingInfo(iBuilding).getTextKey(),),
            )
            CyInterface().addMessage(
                kTriggeredData.eOtherPlayer,
                False,
                gc.getEVENT_MESSAGE_TIME(),
                szBuffer,
                "AS2D_BOMBARDED",
                InterfaceMessageTypes.MESSAGE_TYPE_INFO,
                gc.getBuildingInfo(iBuilding).getButton(),
                gc.getInfoTypeForString("COLOR_RED"),
                city.getX(),
                city.getY(),
                True,
                True,
            )
            city.setNumRealBuilding(iBuilding, 0)
            iNumBuildingsDestroyed += 1
            listBuildings.remove(iBuilding)

    if iNumBuildingsDestroyed > 0:
        szBuffer = localText.getText(
            "TXT_KEY_EVENT_NUM_BUILDINGS_DESTROYED",
            (
                iNumBuildingsDestroyed,
                gc.getPlayer(kTriggeredData.eOtherPlayer).getCivilizationAdjectiveKey(),
                city.getNameKey(),
            ),
        )
        CyInterface().addMessage(
            kTriggeredData.ePlayer,
            False,
            gc.getEVENT_MESSAGE_TIME(),
            szBuffer,
            "AS2D_BOMBARDED",
            InterfaceMessageTypes.MESSAGE_TYPE_INFO,
            None,
            gc.getInfoTypeForString("COLOR_WHITE"),
            -1,
            -1,
            True,
            True,
        )


######## BROTHERS IN NEED ###########


def canTriggerBrothersInNeed(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    if not player.canTradeNetworkWith(kTriggeredData.eOtherPlayer):
        return False

    listResources = []
    listResources.append(
        CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_COPPER")
    )
    listResources.append(
        CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_IRON")
    )
    listResources.append(
        CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_HORSE")
    )
    listResources.append(
        CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_IVORY")
    )
    listResources.append(
        CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_OIL")
    )
    listResources.append(
        CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_URANIUM")
    )

    bFound = False
    for iResource in listResources:
        if (
            player.getNumTradeableBonuses(iResource) > 1
            and otherPlayer.getNumAvailableBonuses(iResource) <= 0
        ):
            bFound = True
            break

    if not bFound:
        return False

    for iTeam in range(gc.getMAX_CIV_TEAMS()):
        if (
            iTeam != player.getTeam()
            and iTeam != otherPlayer.getTeam()
            and gc.getTeam(iTeam).isAlive()
        ):
            if gc.getTeam(iTeam).isAtWar(otherPlayer.getTeam()) and not gc.getTeam(iTeam).isAtWar(
                player.getTeam()
            ):
                return True

    return False


def canDoBrothersInNeed1(argsList):
    kTriggeredData = argsList[1]
    newArgs = (kTriggeredData,)

    return canTriggerBrothersInNeed(newArgs)


######## HURRICANE ###########


def canTriggerHurricaneCity(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return False

    if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
        return False

    if city.plot().getLatitude() <= 0:
        return False

    if city.getPopulation() < 2:
        return False

    return True


def canApplyHurricane1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    listBuildings = []
    for iBuilding in range(gc.getNumBuildingInfos()):
        if (
            city.getNumRealBuilding(iBuilding) > 0
            and gc.getBuildingInfo(iBuilding).getProductionCost() > 0
            and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())
        ):
            listBuildings.append(iBuilding)

    return len(listBuildings) > 0


def canApplyHurricane2(argsList):
    return not canApplyHurricane1(argsList)


def applyHurricane1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    listCheapBuildings = []
    listExpensiveBuildings = []
    for iBuilding in range(gc.getNumBuildingInfos()):
        if (
            city.getNumRealBuilding(iBuilding) > 0
            and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100
            and gc.getBuildingInfo(iBuilding).getProductionCost() > 0
            and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())
        ):
            listCheapBuildings.append(iBuilding)
        if (
            city.getNumRealBuilding(iBuilding) > 0
            and gc.getBuildingInfo(iBuilding).getProductionCost() > 100
            and gc.getBuildingInfo(iBuilding).getProductionCost() > 0
            and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())
        ):
            listExpensiveBuildings.append(iBuilding)

    if len(listCheapBuildings) > 0:
        iBuilding = choice(listCheapBuildings)
        szBuffer = localText.getText(
            "TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED",
            (gc.getBuildingInfo(iBuilding).getTextKey(),),
        )
        CyInterface().addMessage(
            kTriggeredData.ePlayer,
            False,
            gc.getEVENT_MESSAGE_TIME(),
            szBuffer,
            "AS2D_BOMBARDED",
            InterfaceMessageTypes.MESSAGE_TYPE_INFO,
            gc.getBuildingInfo(iBuilding).getButton(),
            gc.getInfoTypeForString("COLOR_RED"),
            city.getX(),
            city.getY(),
            True,
            True,
        )
        city.setNumRealBuilding(iBuilding, 0)

    if len(listExpensiveBuildings) > 0:
        iBuilding = choice(listExpensiveBuildings)
        szBuffer = localText.getText(
            "TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED",
            (gc.getBuildingInfo(iBuilding).getTextKey(),),
        )
        CyInterface().addMessage(
            kTriggeredData.ePlayer,
            False,
            gc.getEVENT_MESSAGE_TIME(),
            szBuffer,
            "AS2D_BOMBARDED",
            InterfaceMessageTypes.MESSAGE_TYPE_INFO,
            gc.getBuildingInfo(iBuilding).getButton(),
            gc.getInfoTypeForString("COLOR_RED"),
            city.getX(),
            city.getY(),
            True,
            True,
        )
        city.setNumRealBuilding(iBuilding, 0)


######## CYCLONE ###########


def canTriggerCycloneCity(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return False

    if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
        return False

    if city.plot().getLatitude() >= 0:
        return False

    return True


######## TSUNAMI ###########


def canTriggerTsunamiCity(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return False

    if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
        return False

    return True


def canApplyTsunami1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    # Rhye
    return city.getPopulation() < 2
    # return (city.getPopulation() < 6)


def canApplyTsunami2(argsList):
    return not canApplyTsunami1(argsList)


def applyTsunami1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    city.kill()


def applyTsunami2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    listBuildings = []
    for iBuilding in range(gc.getNumBuildingInfos()):
        if (
            city.getNumRealBuilding(iBuilding) > 0
            and gc.getBuildingInfo(iBuilding).getProductionCost() > 0
            and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())
        ):
            listBuildings.append(iBuilding)
    # Rhye
    for i in range(2):
        # for i in range(5):
        if len(listBuildings) > 0:
            iBuilding = choice(listBuildings)
            szBuffer = localText.getText(
                "TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED",
                (gc.getBuildingInfo(iBuilding).getTextKey(),),
            )
            CyInterface().addMessage(
                kTriggeredData.ePlayer,
                False,
                gc.getEVENT_MESSAGE_TIME(),
                szBuffer,
                "AS2D_BOMBARDED",
                InterfaceMessageTypes.MESSAGE_TYPE_INFO,
                gc.getBuildingInfo(iBuilding).getButton(),
                gc.getInfoTypeForString("COLOR_RED"),
                city.getX(),
                city.getY(),
                True,
                True,
            )
            city.setNumRealBuilding(iBuilding, 0)
            listBuildings.remove(iBuilding)


def getHelpTsunami2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    # Rhye
    szHelp = localText.getText("TXT_KEY_EVENT_TSUNAMI_2_HELP", (2, city.getNameKey()))
    # szHelp = localText.getText("TXT_KEY_EVENT_TSUNAMI_2_HELP", (5, city.getNameKey()))

    return szHelp


######## MONSOON ###########


def canTriggerMonsoonCity(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return False

    if city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
        return False

    iJungleType = CvUtil.findInfoTypeNum(
        gc.getFeatureInfo, gc.getNumFeatureInfos(), "FEATURE_JUNGLE"
    )

    for iDX in range(-3, 4):
        for iDY in range(-3, 4):
            pLoopPlot = plotXY(city.getX(), city.getY(), iDX, iDY)
            if not pLoopPlot.isNone() and pLoopPlot.getFeatureType() == iJungleType:
                return True

    return False


######## VOLCANO ###########


def getHelpVolcano1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_VOLCANO_1_HELP", ())

    return szHelp


def canApplyVolcano1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumImprovements = 0
    for iDX in range(-1, 2):
        for iDY in range(-1, 2):
            loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
            if not loopPlot.isNone():
                if iDX != 0 or iDY != 0:
                    if loopPlot.getImprovementType() != -1:
                        iNumImprovements += 1

    return iNumImprovements > 0


def applyVolcano1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    listPlots = []
    for iDX in range(-1, 2):
        for iDY in range(-1, 2):
            loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
            if not loopPlot.isNone():
                if iDX != 0 or iDY != 0:
                    if loopPlot.getImprovementType() != -1:
                        listPlots.append(loopPlot)

    listRuins = []
    listRuins.append(
        CvUtil.findInfoTypeNum(
            gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_COTTAGE"
        )
    )
    listRuins.append(
        CvUtil.findInfoTypeNum(
            gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_HAMLET"
        )
    )
    listRuins.append(
        CvUtil.findInfoTypeNum(
            gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_VILLAGE"
        )
    )
    listRuins.append(
        CvUtil.findInfoTypeNum(
            gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_TOWN"
        )
    )

    iRuins = CvUtil.findInfoTypeNum(
        gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_CITY_RUINS"
    )

    for i in range(3):
        if len(listPlots) > 0:
            plot = choice(listPlots)
            iImprovement = plot.getImprovementType()
            szBuffer = localText.getText(
                "TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED",
                (gc.getImprovementInfo(iImprovement).getTextKey(),),
            )
            CyInterface().addMessage(
                kTriggeredData.ePlayer,
                False,
                gc.getEVENT_MESSAGE_TIME(),
                szBuffer,
                "AS2D_BOMBARDED",
                InterfaceMessageTypes.MESSAGE_TYPE_INFO,
                gc.getImprovementInfo(iImprovement).getButton(),
                gc.getInfoTypeForString("COLOR_RED"),
                plot.getX(),
                plot.getY(),
                True,
                True,
            )
            if iImprovement in listRuins:
                plot.setImprovementType(iRuins)
            else:
                plot.setImprovementType(-1)
            listPlots.remove(plot)

            if i == 1 and percentage_chance(50, strict=True):
                break


######## DUSTBOWL ###########


def canTriggerDustbowlCont(argsList):
    kTriggeredData = argsList[0]

    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    if kOrigTriggeredData is None:
        return False

    iFarmType = CvUtil.findInfoTypeNum(
        gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_FARM"
    )
    iPlainsType = CvUtil.findInfoTypeNum(
        gc.getTerrainInfo, gc.getNumTerrainInfos(), "TERRAIN_PLAINS"
    )

    map = gc.getMap()
    iBestValue = map.getGridWidth() + map.getGridHeight()
    bestPlot = None
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == kTriggeredData.ePlayer
            and plot.getImprovementType() == iFarmType
            and plot.getTerrainType() == iPlainsType
        ):
            iValue = plotDistance(
                kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY, plot.getX(), plot.getY()
            )
            if iValue < iBestValue:
                iBestValue = iValue
                bestPlot = plot

    if bestPlot is not None:
        kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
        kActualTriggeredDataObject.iPlotX = bestPlot.getX()
        kActualTriggeredDataObject.iPlotY = bestPlot.getY()
    else:
        player.resetEventOccured(trigger.getPrereqEvent(0))
        return False

    return True


def getHelpDustBowl2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_DUSTBOWL_2_HELP", ())

    return szHelp


######## SALTPETER ###########


def getSaltpeterNumExtraPlots():
    map = gc.getMap()
    if map.getWorldSize() <= 1:
        return 1
    elif map.getWorldSize() <= 3:
        return 2
    elif map.getWorldSize() <= 4:
        return 3
    else:
        return 4


def getHelpSaltpeter(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_SALTPETER_HELP", (getSaltpeterNumExtraPlots(),))

    return szHelp


def canApplySaltpeter(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()

    player = gc.getPlayer(kTriggeredData.ePlayer)

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if plot is None:
        return False

    iWoodland = CvUtil.findInfoTypeNum(
        gc.getFeatureInfo, gc.getNumFeatureInfos(), "FEATURE_FOREST"
    )

    iNumPlots = 0
    for i in range(map.numPlots()):
        loopPlot = map.plotByIndex(i)
        if (
            loopPlot.getOwner() == kTriggeredData.ePlayer
            and loopPlot.getFeatureType() == iWoodland
            and loopPlot.isHills()
        ):
            iDistance = plotDistance(
                kTriggeredData.iPlotX, kTriggeredData.iPlotY, loopPlot.getX(), loopPlot.getY()
            )
            if iDistance > 0:
                iNumPlots += 1

    return iNumPlots >= getSaltpeterNumExtraPlots()


def applySaltpeter(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()

    player = gc.getPlayer(kTriggeredData.ePlayer)

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if plot is None:
        return

    iWoodland = CvUtil.findInfoTypeNum(
        gc.getFeatureInfo, gc.getNumFeatureInfos(), "FEATURE_FOREST"
    )

    listPlots = []
    for i in range(map.numPlots()):
        loopPlot = map.plotByIndex(i)
        if (
            loopPlot.getOwner() == kTriggeredData.ePlayer
            and loopPlot.getFeatureType() == iWoodland
            and loopPlot.isHills()
        ):
            iDistance = plotDistance(
                kTriggeredData.iPlotX, kTriggeredData.iPlotY, loopPlot.getX(), loopPlot.getY()
            )
            if iDistance > 0:
                listPlots.append((iDistance, loopPlot))

    listPlots.sort()

    iCount = getSaltpeterNumExtraPlots()
    for loopPlot in listPlots:
        if iCount == 0:
            break
        iCount -= 1
        gc.getGame().setPlotExtraYield(
            loopPlot[1].getX(), loopPlot[1].getY(), YieldTypes.YIELD_COMMERCE, 1
        )
        CyInterface().addMessage(
            kTriggeredData.ePlayer,
            False,
            gc.getEVENT_MESSAGE_TIME(),
            localText.getText("TXT_KEY_EVENT_SALTPETER_DISCOVERED", ()),
            "",
            InterfaceMessageTypes.MESSAGE_TYPE_INFO,
            None,
            gc.getInfoTypeForString("COLOR_WHITE"),
            loopPlot[1].getX(),
            loopPlot[1].getY(),
            True,
            True,
        )


######## GREAT DEPRESSION ###########


def applyGreatDepression(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    corporation = gc.getCorporationInfo(kTriggeredData.eCorporation)

    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            loopPlayer.changeGold(-loopPlayer.getGold() / 4)

            if iPlayer != kTriggeredData.ePlayer:
                szText = localText.getText(
                    "TXT_KEY_EVENTTRIGGER_GREAT_DEPRESSION",
                    (
                        player.getCivilizationAdjectiveKey(),
                        u"",
                        u"",
                        u"",
                        u"",
                        corporation.getTextKey(),
                    ),
                )
                szText += u"\n\n" + localText.getText("TXT_KEY_EVENT_GREAT_DEPRESSION_HELP", (25,))
                popupInfo = CyPopupInfo()
                popupInfo.setText(szText)
                popupInfo.addPopup(iPlayer)


def getHelpGreatDepression(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_GREAT_DEPRESSION_HELP", (25,))

    return szHelp


######## CHAMPION ###########


def canTriggerChampion(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    if team.getAtWarCount(True) > 0:
        return False

    return True


def canTriggerChampionUnit(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iUnit = argsList[2]

    player = gc.getPlayer(ePlayer)
    unit = player.getUnit(iUnit)

    if unit.isNone():
        return False

    if unit.getDamage() > 0:
        return False

    if unit.getExperience() < 3:
        return False

    iLeadership = CvUtil.findInfoTypeNum(
        gc.getPromotionInfo, gc.getNumPromotionInfos(), "PROMOTION_LEADERSHIP"
    )
    if unit.isHasPromotion(iLeadership):
        return False

    return True


def applyChampion(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    iLeadership = CvUtil.findInfoTypeNum(
        gc.getPromotionInfo, gc.getNumPromotionInfos(), "PROMOTION_LEADERSHIP"
    )

    unit.setHasPromotion(iLeadership, True)


def getHelpChampion(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    iLeadership = CvUtil.findInfoTypeNum(
        gc.getPromotionInfo, gc.getNumPromotionInfos(), "PROMOTION_LEADERSHIP"
    )

    szHelp = localText.getText(
        "TXT_KEY_EVENT_CHAMPION_HELP",
        (unit.getNameKey(), gc.getPromotionInfo(iLeadership).getTextKey()),
    )

    return szHelp


######## ELECTRIC COMPANY ###########


def canTriggerElectricCompany(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    player = gc.getPlayer(kTriggeredData.ePlayer)

    (loopCity, iter) = player.firstCity(False)

    while loopCity:

        if loopCity.angryPopulation(0) > 0:
            return False

        (loopCity, iter) = player.nextCity(iter, False)

    return True


######## GOLD RUSH ###########


def canTriggerGoldRush(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    iIndustrial = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), "ERA_INDUSTRIAL")

    if player.getCurrentEra() != iIndustrial:
        return False

    return True


######## INFLUENZA ###########


def canTriggerInfluenza(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    iIndustrial = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), "ERA_INDUSTRIAL")

    if player.getCurrentEra() <= iIndustrial:
        return False

    iMedicine = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_MEDICINE")

    if team.isHasTech(iMedicine):
        return False

    return True


def applyInfluenza2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    eventCity = player.getCity(kTriggeredData.iCityId)

    iNumCities = 2 + rand(3)

    listCities = []
    (loopCity, iter) = player.firstCity(False)
    while loopCity:
        if loopCity.getPopulation() > 2:
            iDistance = plotDistance(
                eventCity.getX(), eventCity.getY(), loopCity.getX(), loopCity.getY()
            )
            if iDistance > 0:
                listCities.append((iDistance, loopCity))
        (loopCity, iter) = player.nextCity(iter, False)

    listCities.sort()

    if iNumCities > len(listCities):
        iNumCities = len(listCities)

    for i in range(iNumCities):
        (iDist, loopCity) = listCities[i]
        loopCity.changePopulation(-2)
        szBuffer = localText.getText("TXT_KEY_EVENT_INFLUENZA_HIT_CITY", (loopCity.getNameKey(),))
        CyInterface().addMessage(
            kTriggeredData.ePlayer,
            False,
            gc.getEVENT_MESSAGE_TIME(),
            szBuffer,
            "AS2D_PILLAGE",
            InterfaceMessageTypes.MESSAGE_TYPE_INFO,
            None,
            gc.getInfoTypeForString("COLOR_RED"),
            loopCity.getX(),
            loopCity.getY(),
            True,
            True,
        )


def getHelpInfluenza2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_INFLUENZA_HELP_2", (2,))

    return szHelp


######## SOLO FLIGHT ###########


def canTriggerSoloFlight(argsList):
    kTriggeredData = argsList[0]

    map = gc.getMap()
    if map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_DUEL"
    ):
        iMinLandmass = 3
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_TINY"
    ):
        iMinLandmass = 4
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_SMALL"
    ):
        iMinLandmass = 6
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_STANDARD"
    ):
        iMinLandmass = 8
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_LARGE"
    ):
        iMinLandmass = 10
    else:
        iMinLandmass = 12

    if map.getNumLandAreas() < iMinLandmass:
        return False

    if gc.getGame().isGameMultiPlayer():
        return False

    return True


def getHelpSoloFlight(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1,))

    return szHelp


def applySoloFlight(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
            loopTeam = gc.getTeam(loopPlayer.getTeam())
            if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
                loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)


######## ANTELOPE ###########


def canTriggerAntelope(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iDeer = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_DEER")
    iHappyBonuses = 0
    bDeer = False
    for i in range(gc.getNumBonusInfos()):
        bonus = gc.getBonusInfo(i)
        iNum = player.getNumAvailableBonuses(i)
        if iNum > 0:
            if bonus.getHappiness() > 0:
                iHappyBonuses += 1
                if iHappyBonuses > 5:
                    return False
            if i == iDeer:
                return False

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if not plot.canHaveBonus(iDeer, False):
        return False

    return True


def doAntelope2(argsList):
    # 	Need this because camps are not normally allowed unless there is already deer.
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if not plot.isNone():
        plot.setImprovementType(
            CvUtil.findInfoTypeNum(
                gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_CAMP"
            )
        )

    return 1


def getHelpAntelope2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iCamp = CvUtil.findInfoTypeNum(
        gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_CAMP"
    )
    szHelp = localText.getText(
        "TXT_KEY_EVENT_IMPROVEMENT_GROWTH", (gc.getImprovementInfo(iCamp).getTextKey(),)
    )

    return szHelp


######## WHALEOFATHING ###########


def canTriggerWhaleOfAThing(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iWhale = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_WHALE")
    iHappyBonuses = 0
    bWhale = False
    for i in range(gc.getNumBonusInfos()):
        bonus = gc.getBonusInfo(i)
        iNum = player.getNumAvailableBonuses(i)
        if iNum > 0:
            if bonus.getHappiness() > 0:
                iHappyBonuses += 1
                if iHappyBonuses > 5:
                    return False
            if i == iWhale:
                return False

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if not plot.canHaveBonus(iWhale, False):
        return False

    return True


######## HIYOSILVER ###########


def canTriggerHiyoSilver(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSilver = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_SILVER")
    iHappyBonuses = 0
    bSilver = False
    for i in range(gc.getNumBonusInfos()):
        bonus = gc.getBonusInfo(i)
        iNum = player.getNumAvailableBonuses(i)
        if iNum > 0:
            if bonus.getHappiness() > 0:
                iHappyBonuses += 1
                if iHappyBonuses > 5:
                    return False
            if i == iSilver:
                return False

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if not plot.canHaveBonus(iSilver, False):
        return False

    return True


######## WININGMONKS ###########


def canTriggerWiningMonks(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if (
        player.getNumAvailableBonuses(
            CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_WINE")
        )
        > 0
    ):
        return False

    return True


def doWiningMonks2(argsList):
    # 	Need this because wineries are not normally allowed unless there is already wine.
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if not plot.isNone():
        plot.setImprovementType(
            CvUtil.findInfoTypeNum(
                gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_WINERY"
            )
        )

    return 1


def getHelpWiningMonks2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iImp = CvUtil.findInfoTypeNum(
        gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_WINERY"
    )
    szHelp = localText.getText(
        "TXT_KEY_EVENT_IMPROVEMENT_GROWTH", (gc.getImprovementInfo(iImp).getTextKey(),)
    )

    return szHelp


######## INDEPENDENTFILMS ###########


def canTriggerIndependentFilms(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    for i in range(gc.getNumBuildingInfos()):
        if gc.getBuildingInfo(i).getFreeBonus() == CvUtil.findInfoTypeNum(
            gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_MOVIES"
        ):
            if player.countNumBuildings(i) > 0:
                return False

    return True


def doIndependentFilms(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_MOVIES")

    city.changeFreeBonus(iBonus, 1)

    return 1


def getHelpIndependentFilms(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_MOVIES")

    szHelp = localText.getText(
        "TXT_KEY_EVENT_INDEPENDENTFILMS_HELP_1",
        (1, gc.getBonusInfo(iBonus).getChar(), city.getNameKey()),
    )

    return szHelp


######## ANCIENT OLYMPICS ###########


def canTriggerAncientOlympics(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    stateReligion = player.getStateReligion()

    if stateReligion == CvUtil.findInfoTypeNum(
        gc.getReligionInfo, gc.getNumReligionInfos(), "RELIGION_JUDAISM"
    ):
        return False

    if stateReligion == CvUtil.findInfoTypeNum(
        gc.getReligionInfo, gc.getNumReligionInfos(), "RELIGION_CHRISTIANITY"
    ):
        return False

    if stateReligion == CvUtil.findInfoTypeNum(
        gc.getReligionInfo, gc.getNumReligionInfos(), "RELIGION_ISLAM"
    ):
        return False

    return True


def doAncientOlympics2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()

    for j in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(j)
        if j != kTriggeredData.ePlayer and loopPlayer.isAlive() and not loopPlayer.isMinorCiv():

            for i in range(map.numPlots()):
                plot = map.plotByIndex(i)
                if (
                    not plot.isWater()
                    and plot.getOwner() == kTriggeredData.ePlayer
                    and plot.isAdjacentPlayer(j, True)
                ):
                    loopPlayer.AI_changeMemoryCount(
                        kTriggeredData.ePlayer, MemoryTypes.MEMORY_EVENT_GOOD_TO_US, 1
                    )
                    break

    return 1


def getHelpAncientOlympics2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_ANCIENTOLYMPICS_HELP_2", (1,))

    return szHelp


######## MODERN OLYMPICS ###########


def canTriggerModernOlympics(argsList):

    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    if kOrigTriggeredData is None:
        return False

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY

    return True


def getHelpModernOlympics(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1,))

    return szHelp


def applyModernOlympics(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
            loopTeam = gc.getTeam(loopPlayer.getTeam())
            if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
                loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)


######## INTERSTATE ###########


def canTriggerInterstate(argsList):

    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if not player.isCivic(
        CvUtil.findInfoTypeNum(gc.getCivicInfo, gc.getNumCivicInfos(), "CIVIC_EMANCIPATION")
    ):
        return False

    return True


def getHelpInterstate(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText(
        "TXT_KEY_UNIT_MOVEMENT",
        (
            1,
            gc.getRouteInfo(
                CvUtil.findInfoTypeNum(gc.getRouteInfo, gc.getNumRouteInfos(), "ROUTE_ROAD")
            ).getTextKey(),
        ),
    )

    return szHelp


def applyInterstate(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    iRoad = CvUtil.findInfoTypeNum(gc.getRouteInfo, gc.getNumRouteInfos(), "ROUTE_ROAD")

    team.changeRouteChange(iRoad, -5)


######## EARTH DAY ###########


def getHelpEarthDay2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_EARTHDAY_HELP_2", ())

    return szHelp


def canApplyEarthDay2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    iCivic = CvUtil.findInfoTypeNum(
        gc.getCivicInfo, gc.getNumCivicInfos(), "CIVIC_ENVIRONMENTALISM"
    )

    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer and not loopPlayer.isHuman():
            loopTeam = gc.getTeam(loopPlayer.getTeam())
            if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
                tradeData = TradeData()
                tradeData.ItemType = TradeableItems.TRADE_CIVIC
                tradeData.iData = iCivic
                if loopPlayer.canTradeItem(kTriggeredData.ePlayer, tradeData, False):
                    if (
                        loopPlayer.getTradeDenial(kTriggeredData.ePlayer, tradeData)
                        == DenialTypes.NO_DENIAL
                    ):
                        return True
    return False


def applyEarthDay2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iCivic = CvUtil.findInfoTypeNum(
        gc.getCivicInfo, gc.getNumCivicInfos(), "CIVIC_ENVIRONMENTALISM"
    )
    iCivicOption = CvUtil.findInfoTypeNum(
        gc.getCivicOptionInfo, gc.getNumCivicOptionInfos(), "CIVICOPTION_ECONOMY"
    )

    listPlayers = []
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer and not loopPlayer.isHuman():
            loopTeam = gc.getTeam(loopPlayer.getTeam())
            if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
                tradeData = TradeData()
                tradeData.ItemType = TradeableItems.TRADE_CIVIC
                tradeData.iData = iCivic
                if loopPlayer.canTradeItem(kTriggeredData.ePlayer, tradeData, False):
                    if (
                        loopPlayer.getTradeDenial(kTriggeredData.ePlayer, tradeData)
                        == DenialTypes.NO_DENIAL
                    ):
                        listPlayers.append((-loopPlayer.AI_civicValue(iCivic), iPlayer))

    listPlayers.sort()

    if len(listPlayers) > 3:
        listPlayers = listPlayers[:2]

    for (iValue, iPlayer) in listPlayers:
        gc.getPlayer(iPlayer).setCivics(iCivicOption, iCivic)


######## FREEDOM CONCERT ###########


def getHelpFreedomConcert2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_FREEDOMCONCERT_HELP_2", ())

    return szHelp


def canApplyFreedomConcert2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    eventCity = player.getCity(kTriggeredData.iCityId)

    for iReligion in range(gc.getNumReligionInfos()):
        if eventCity.isHasReligion(iReligion):
            (loopCity, iter) = player.firstCity(False)
            while loopCity:
                if not loopCity.isHasReligion(iReligion):
                    for jReligion in range(gc.getNumReligionInfos()):
                        if loopCity.isHasReligion(jReligion):
                            return True
                (loopCity, iter) = player.nextCity(iter, False)

    return False


def applyFreedomConcert2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    eventCity = player.getCity(kTriggeredData.iCityId)

    for iReligion in range(gc.getNumReligionInfos()):
        if eventCity.isHasReligion(iReligion):

            bestCity = None
            iBestDistance = 0
            (loopCity, iter) = player.firstCity(False)
            while loopCity:
                if not loopCity.isHasReligion(iReligion):
                    bValid = False
                    for jReligion in range(gc.getNumReligionInfos()):
                        if loopCity.isHasReligion(jReligion):
                            bValid = True
                            break

                    if bValid:
                        iDistance = plotDistance(
                            eventCity.getX(), eventCity.getY(), loopCity.getX(), loopCity.getY()
                        )

                        if iDistance < iBestDistance or bestCity is None:
                            bestCity = loopCity
                            iBestDistance = iDistance

                (loopCity, iter) = player.nextCity(iter, False)

            if bestCity is not None:
                bestCity.setHasReligion(iReligion, True, True, True)


######## HEROIC_GESTURE ###########


def canTriggerHeroicGesture(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    if not gc.getTeam(destPlayer.getTeam()).canChangeWarPeace(player.getTeam()):
        return False

    if gc.getTeam(destPlayer.getTeam()).AI_getWarSuccess(player.getTeam()) <= 0:
        return False

    if gc.getTeam(player.getTeam()).AI_getWarSuccess(destPlayer.getTeam()) <= 0:
        return False

    return True


def doHeroicGesture2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if destPlayer.isHuman():
        # this works only because it's a single-player only event
        popupInfo = CyPopupInfo()
        popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popupInfo.setText(
            localText.getText(
                "TXT_KEY_EVENT_HEROIC_GESTURE_OTHER_3", (player.getCivilizationAdjectiveKey(),)
            )
        )
        popupInfo.setData1(kTriggeredData.eOtherPlayer)
        popupInfo.setData2(kTriggeredData.ePlayer)
        popupInfo.setPythonModule("CvRandomEventInterface")
        popupInfo.setOnClickedPythonCallback("heroicGesture2Callback")
        popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
        popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
        popupInfo.addPopup(kTriggeredData.eOtherPlayer)
    else:
        destPlayer.forcePeace(kTriggeredData.ePlayer)
        destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
        player.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

    return


def heroicGesture2Callback(argsList):
    iButton = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    szText = argsList[4]
    bOption1 = argsList[5]
    bOption2 = argsList[6]

    if iButton == 0:
        destPlayer = gc.getPlayer(iData1)
        player = gc.getPlayer(iData2)
        destPlayer.forcePeace(iData2)
        destPlayer.AI_changeAttitudeExtra(iData2, 1)
        player.AI_changeAttitudeExtra(iData1, 1)

    return 0


def getHelpHeroicGesture2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    # Get help text
    szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()))

    return szHelp


######## GREAT_MEDIATOR ###########


def canTriggerGreatMediator(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    if not gc.getTeam(player.getTeam()).canChangeWarPeace(destPlayer.getTeam()):
        return False

    # if gc.getTeam(player.getTeam()).AI_getAtWarCounter(destPlayer.getTeam()) < 10: #Rhye
    if gc.getTeam(player.getTeam()).AI_getAtWarCounter(destPlayer.getTeam()) < 6:  # Rhye
        return False

    # Rhye - start
    if player.getID() in [
        Civ.INDEPENDENT.value,
        Civ.INDEPENDENT_2.value,
        Civ.INDEPENDENT_3.value,
        Civ.INDEPENDENT_4.value,
    ]:
        return False

    if destPlayer.getID() in [
        Civ.INDEPENDENT.value,
        Civ.INDEPENDENT_2.value,
        Civ.INDEPENDENT_3.value,
        Civ.INDEPENDENT_4.value,
    ]:
        return False
    # Rhye - end

    return True


def doGreatMediator2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if destPlayer.isHuman():
        # this works only because it's a single-player only event
        popupInfo = CyPopupInfo()
        popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popupInfo.setText(
            localText.getText(
                "TXT_KEY_EVENT_GREAT_MEDIATOR_OTHER_3", (player.getCivilizationAdjectiveKey(),)
            )
        )
        popupInfo.setData1(kTriggeredData.eOtherPlayer)
        popupInfo.setData2(kTriggeredData.ePlayer)
        popupInfo.setPythonModule("CvRandomEventInterface")
        popupInfo.setOnClickedPythonCallback("greatMediator2Callback")
        popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
        popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
        popupInfo.addPopup(kTriggeredData.eOtherPlayer)
    else:
        gc.getTeam(player.getTeam()).makePeace(destPlayer.getTeam())
        destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
        player.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

    return


def greatMediator2Callback(argsList):
    iButton = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    szText = argsList[4]
    bOption1 = argsList[5]
    bOption2 = argsList[6]

    if iButton == 0:
        destPlayer = gc.getPlayer(iData1)
        player = gc.getPlayer(iData2)
        gc.getTeam(destPlayer.getTeam()).makePeace(player.getTeam())
        destPlayer.AI_changeAttitudeExtra(iData2, 1)
        player.AI_changeAttitudeExtra(iData1, 1)

    return 0


def getHelpGreatMediator2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    # Get help text
    szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()))

    return szHelp


######## ANCIENT_TEXTS ###########


def doAncientTexts2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
            loopTeam = gc.getTeam(loopPlayer.getTeam())
            if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
                loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)

    return


def getHelpAncientTexts2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1,))

    return szHelp


######## IMPACT_CRATER ###########


def canTriggerImpactCrater(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iUranium = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_URANIUM")
    if player.getNumAvailableBonuses(iUranium) > 0:
        return False

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if not plot.canHaveBonus(iUranium, False):
        return False

    return True


def doImpactCrater2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if not plot.isNone():
        plot.setImprovementType(
            CvUtil.findInfoTypeNum(
                gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_MINE"
            )
        )

    return 1


def getHelpImpactCrater2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iMine = CvUtil.findInfoTypeNum(
        gc.getImprovementInfo, gc.getNumImprovementInfos(), "IMPROVEMENT_MINE"
    )
    szHelp = localText.getText(
        "TXT_KEY_EVENT_IMPROVEMENT_GROWTH", (gc.getImprovementInfo(iMine).getTextKey(),)
    )

    return szHelp


######## THE_HUNS ###########


def canTriggerTheHuns(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return False

    #   At least one civ on the board must know Horseback Riding.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_HORSEBACK_RIDING")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    #   At least one civ on the board must know Iron Working.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_IRON_WORKING")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    # Can we build the counter unit?
    iCounterUnitClass = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_SPEARMAN"
    )
    iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(
        iCounterUnitClass
    )
    if iCounterUnit == -1:
        return False

    (loopCity, iter) = player.firstCity(False)
    bFound = False
    while loopCity:
        if loopCity.canTrain(iCounterUnit, False, False):
            bFound = True
            break

        (loopCity, iter) = player.nextCity(iter, False)

    if not bFound:
        return False

    # 	Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            return True

    return False


def getHelpTheHuns1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_HUNS_HELP_1", ())

    return szHelp


def applyTheHuns1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(choice(listPlots))

    if map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_DUEL"
    ):
        iNumUnits = 1
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_TINY"
    ):
        iNumUnits = 2
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_SMALL"
    ):
        iNumUnits = 3
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_STANDARD"
    ):
        iNumUnits = 4
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_LARGE"
    ):
        iNumUnits = 5
    else:
        iNumUnits = 6

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_HORSE_ARCHER")

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(
            iUnitType,
            plot.getX(),
            plot.getY(),
            UnitAITypes.UNITAI_ATTACK_CITY_LEMMING,
            DirectionTypes.DIRECTION_SOUTH,
        )


######## THE_VANDALS ###########


def canTriggerTheVandals(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return False

    #   At least one civ on the board must know Metal Casting.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_METAL_CASTING")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    #   At least one civ on the board must know Iron Working.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_IRON_WORKING")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    # Can we build the counter unit?
    iCounterUnitClass = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_AXEMAN"
    )
    iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(
        iCounterUnitClass
    )
    if iCounterUnit == -1:
        return False

    (loopCity, iter) = player.firstCity(False)
    bFound = False
    while loopCity:
        if loopCity.canTrain(iCounterUnit, False, False):
            bFound = True
            break

        (loopCity, iter) = player.nextCity(iter, False)

    if not bFound:
        return False

    # 	Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            return True

    return False


def getHelpTheVandals1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_VANDALS_HELP_1", ())

    return szHelp


def applyTheVandals1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(choice(listPlots))

    if map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_DUEL"
    ):
        iNumUnits = 1
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_TINY"
    ):
        iNumUnits = 2
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_SMALL"
    ):
        iNumUnits = 3
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_STANDARD"
    ):
        iNumUnits = 4
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_LARGE"
    ):
        iNumUnits = 5
    else:
        iNumUnits = 6

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_SWORDSMAN")

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(
            iUnitType,
            plot.getX(),
            plot.getY(),
            UnitAITypes.UNITAI_ATTACK_CITY_LEMMING,
            DirectionTypes.DIRECTION_SOUTH,
        )


######## THE_GOTHS ###########


def canTriggerTheGoths(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return False

    #   At least one civ on the board must know Mathematics.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_MATHEMATICS")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    #   At least one civ on the board must know Iron Working.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_IRON_WORKING")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    # Can we build the counter unit?
    iCounterUnitClass = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_CHARIOT"
    )
    iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(
        iCounterUnitClass
    )
    if iCounterUnit == -1:
        return False

    (loopCity, iter) = player.firstCity(False)
    bFound = False
    while loopCity:
        if loopCity.canTrain(iCounterUnit, False, False):
            bFound = True
            break

        (loopCity, iter) = player.nextCity(iter, False)

    if not bFound:
        return False

    # 	Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            return True

    return False


def getHelpThGoths1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_GOTHS_HELP_1", ())

    return szHelp


def applyTheGoths1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(choice(listPlots))

    if map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_DUEL"
    ):
        iNumUnits = 1
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_TINY"
    ):
        iNumUnits = 2
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_SMALL"
    ):
        iNumUnits = 3
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_STANDARD"
    ):
        iNumUnits = 4
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_LARGE"
    ):
        iNumUnits = 5
    else:
        iNumUnits = 6

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_AXEMAN")

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(
            iUnitType,
            plot.getX(),
            plot.getY(),
            UnitAITypes.UNITAI_ATTACK_CITY_LEMMING,
            DirectionTypes.DIRECTION_SOUTH,
        )


######## THE_PHILISTINES ###########


def canTriggerThePhilistines(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return False

    #   At least one civ on the board must know Monotheism.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_MONOTHEISM")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    #   At least one civ on the board must know Bronze Working.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_BRONZE_WORKING")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    # Can we build the counter unit?
    iCounterUnitClass = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_AXEMAN"
    )
    iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(
        iCounterUnitClass
    )
    if iCounterUnit == -1:
        return False

    (loopCity, iter) = player.firstCity(False)
    bFound = False
    while loopCity:
        if loopCity.canTrain(iCounterUnit, False, False):
            bFound = True
            break

        (loopCity, iter) = player.nextCity(iter, False)

    if not bFound:
        return False

    # 	Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            return True

    return False


def getHelpThePhilistines1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_PHILISTINES_HELP_1", ())

    return szHelp


def applyThePhilistines1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(choice(listPlots))

    if map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_DUEL"
    ):
        iNumUnits = 1
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_TINY"
    ):
        iNumUnits = 2
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_SMALL"
    ):
        iNumUnits = 3
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_STANDARD"
    ):
        iNumUnits = 4
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_LARGE"
    ):
        iNumUnits = 5
    else:
        iNumUnits = 6

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_SPEARMAN")

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(
            iUnitType,
            plot.getX(),
            plot.getY(),
            UnitAITypes.UNITAI_ATTACK_CITY_LEMMING,
            DirectionTypes.DIRECTION_SOUTH,
        )


######## THE_VEDIC_ARYANS ###########


def canTriggerTheVedicAryans(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return False

    #   At least one civ on the board must know Polytheism.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_POLYTHEISM")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    #   At least one civ on the board must know Archery.
    bFoundValid = False
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_ARCHERY")
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = True
                break

    if not bFoundValid:
        return False

    # Can we build the counter unit?
    iCounterUnitClass = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_ARCHER"
    )
    iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(
        iCounterUnitClass
    )
    if iCounterUnit == -1:
        return False

    (loopCity, iter) = player.firstCity(False)
    bFound = False
    while loopCity:
        if loopCity.canTrain(iCounterUnit, False, False):
            bFound = True
            break

        (loopCity, iter) = player.nextCity(iter, False)

    if not bFound:
        return False

    # 	Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            return True

    return False


def getHelpTheVedicAryans1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_VEDIC_ARYANS_HELP_1", ())

    return szHelp


def applyTheVedicAryans1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    # Rhye - bugfix
    # for i in range(map.numPlots()):
    for i in range(8432):
        plot = map.plotByIndex(i)
        if (
            plot.getOwner() == -1
            and not plot.isWater()
            and not plot.isImpassable()
            and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0
            and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)
        ):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(choice(listPlots))

    if map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_DUEL"
    ):
        iNumUnits = 1
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_TINY"
    ):
        iNumUnits = 2
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_SMALL"
    ):
        iNumUnits = 3
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_STANDARD"
    ):
        iNumUnits = 4
    elif map.getWorldSize() == CvUtil.findInfoTypeNum(
        gc.getWorldInfo, gc.getNumWorldInfos(), "WORLDSIZE_LARGE"
    ):
        iNumUnits = 5
    else:
        iNumUnits = 6

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_ARCHER")

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(
            iUnitType,
            plot.getX(),
            plot.getY(),
            UnitAITypes.UNITAI_ATTACK_CITY_LEMMING,
            DirectionTypes.DIRECTION_SOUTH,
        )


######## SECURITY_TAX ###########


def canTriggerSecurityTax(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iWalls = CvUtil.findInfoTypeNum(
        gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), "BUILDINGCLASS_WALLS"
    )
    if player.getNumCities() > player.getBuildingClassCount(iWalls):
        return False

    return True


######## LITERACY ###########


def canTriggerLiteracy(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iLibrary = CvUtil.findInfoTypeNum(
        gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), "BUILDINGCLASS_LIBRARY"
    )
    if player.getNumCities() > player.getBuildingClassCount(iLibrary):
        return False

    return True


######## TEA ###########


def canTriggerTea(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.isCivic(
        CvUtil.findInfoTypeNum(gc.getCivicInfo, gc.getNumCivicInfos(), "CIVIC_MERCANTILISM")
    ):
        return False

    bCanTrade = False
    for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
        if player.canHaveTradeRoutesWith(iLoopPlayer):
            bCanTrade = True
            break

    if not bCanTrade:
        return False

    return True


######## HORSE WHISPERING ###########


def canTriggerHorseWhispering(argsList):
    kTriggeredData = argsList[0]

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    return True


def getHelpHorseWhispering1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()

    iNumStables = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
    # Rhye
    iNumStables /= 2
    iNumStables += 1
    szHelp = localText.getText("TXT_KEY_EVENT_HORSE_WHISPERING_HELP", (iNumStables,))

    return szHelp


def canTriggerHorseWhisperingDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iStable = CvUtil.findInfoTypeNum(
        gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), "BUILDINGCLASS_STABLE"
    )
    # Rhye
    # if gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() > player.getBuildingClassCount(iStable):
    iNumStables = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    iNumStables /= 2
    iNumStables += 1
    if iNumStables > player.getBuildingClassCount(iStable):
        return False

    return True


def getHelpHorseWhisperingDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()

    iNumUnits = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
    # Rhye
    iNumUnits /= 2
    iNumUnits += 1
    szHelp = localText.getText("TXT_KEY_EVENT_HORSE_WHISPERING_DONE_HELP_1", (iNumUnits,))

    return szHelp


def applyHorseWhisperingDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    map = gc.getMap()
    plot = map.plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    iNumUnits = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
    iUnitClassType = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_HORSE_ARCHER"
    )
    iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(
        iUnitClassType
    )

    if iUnitType != -1:
        for i in range(iNumUnits):
            player.initUnit(
                iUnitType,
                plot.getX(),
                plot.getY(),
                UnitAITypes.UNITAI_ATTACK,
                DirectionTypes.DIRECTION_SOUTH,
            )


######## HARBORMASTER ###########


def getHelpHarbormaster1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iHarborsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iHarborsRequired /= 2
    iHarborsRequired += 2
    iCaravelsRequired = iHarborsRequired / 2 + 1

    szHelp = localText.getText(
        "TXT_KEY_EVENT_HARBORMASTER_HELP", (iHarborsRequired, iCaravelsRequired)
    )

    return szHelp


def canTriggerHarbormaster(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    map = gc.getMap()

    iNumWater = 0

    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)

        if plot.isWater():
            iNumWater += 1

        if 100 * iNumWater >= 40 * map.numPlots():
            return True

    return False


def canTriggerHarbormasterDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iHarbor = CvUtil.findInfoTypeNum(
        gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), "BUILDINGCLASS_HARBOR"
    )
    iHarborsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iHarborsRequired /= 2
    iHarborsRequired += 2
    if iHarborsRequired > player.getBuildingClassCount(iHarbor):
        return False

    iCaravel = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_CARAVEL"
    )
    iCaravelsRequired = iHarborsRequired / 2 + 1
    if iCaravelsRequired > player.getUnitClassCount(iCaravel):
        return False

    return True


######## CLASSIC LITERATURE ###########


def canTriggerClassicLiterature(argsList):
    kTriggeredData = argsList[0]

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    return True


def getHelpClassicLiterature1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iLibrariesRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iLibrariesRequired /= 2
    iLibrariesRequired += 2

    szHelp = localText.getText("TXT_KEY_EVENT_CLASSIC_LITERATURE_HELP_1", (iLibrariesRequired,))

    return szHelp


def canTriggerClassicLiteratureDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iLibrary = CvUtil.findInfoTypeNum(
        gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), "BUILDINGCLASS_LIBRARY"
    )
    iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iBuildingsRequired /= 2
    iBuildingsRequired += 2
    if iBuildingsRequired > player.getBuildingClassCount(iLibrary):
        return False

    return True


def getHelpClassicLiteratureDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_CLASSIC_LITERATURE_DONE_HELP_2", ())

    return szHelp


def canApplyClassicLiteratureDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iEraAncient = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), "ERA_ANCIENT")

    for iTech in range(gc.getNumTechInfos()):
        if gc.getTechInfo(iTech).getEra() == iEraAncient and player.canResearch(iTech, False):
            return True

    return False


def applyClassicLiteratureDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iEraAncient = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), "ERA_ANCIENT")

    listTechs = []
    for iTech in range(gc.getNumTechInfos()):
        if gc.getTechInfo(iTech).getEra() == iEraAncient and player.canResearch(iTech, False):
            listTechs.append(iTech)

    if len(listTechs) > 0:
        iTech = choice(listTechs)
        gc.getTeam(player.getTeam()).setHasTech(iTech, True, kTriggeredData.ePlayer, True, True)


def getHelpClassicLiteratureDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSpecialist = CvUtil.findInfoTypeNum(
        gc.getSpecialistInfo,
        gc.getNumSpecialistInfos(),
        "SPECIALIST_SCIENTIST",
    )
    iGreatLibrary = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_GREAT_LIBRARY"
    )

    szCityName = u""
    (loopCity, iter) = player.firstCity(False)
    while loopCity:
        if loopCity.isHasBuilding(iGreatLibrary):
            szCityName = loopCity.getNameKey()
            break

        (loopCity, iter) = player.nextCity(iter, False)

    szHelp = localText.getText(
        "TXT_KEY_EVENT_FREE_SPECIALIST",
        (1, gc.getSpecialistInfo(iSpecialist).getTextKey(), szCityName),
    )

    return szHelp


def canApplyClassicLiteratureDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iGreatLibrary = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_GREAT_LIBRARY"
    )

    (loopCity, iter) = player.firstCity(False)
    while loopCity:
        if loopCity.isHasBuilding(iGreatLibrary):
            return True

        (loopCity, iter) = player.nextCity(iter, False)

    return False


def applyClassicLiteratureDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSpecialist = CvUtil.findInfoTypeNum(
        gc.getSpecialistInfo,
        gc.getNumSpecialistInfos(),
        "SPECIALIST_SCIENTIST",
    )
    iGreatLibrary = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_GREAT_LIBRARY"
    )

    (loopCity, iter) = player.firstCity(False)
    while loopCity:
        if loopCity.isHasBuilding(iGreatLibrary):
            loopCity.changeFreeSpecialistCount(iSpecialist, 1)
            return

        (loopCity, iter) = player.nextCity(iter, False)


######## MASTER BLACKSMITH ###########


def canTriggerMasterBlacksmith(argsList):
    kTriggeredData = argsList[0]

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    return True


def getHelpMasterBlacksmith1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iRequired /= 2
    iRequired += 2

    szHelp = localText.getText(
        "TXT_KEY_EVENT_MASTER_BLACKSMITH_HELP_1",
        (iRequired, player.getCity(kTriggeredData.iCityId).getNameKey()),
    )

    return szHelp


def expireMasterBlacksmith1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)
    if city is None or city.getOwner() != kTriggeredData.ePlayer:
        return True

    return False


def canTriggerMasterBlacksmithDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iForge = CvUtil.findInfoTypeNum(
        gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), "BUILDINGCLASS_FORGE"
    )
    iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iBuildingsRequired /= 2
    iBuildingsRequired += 2
    if iBuildingsRequired > player.getBuildingClassCount(iForge):
        return False

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    city = player.getCity(kOrigTriggeredData.iCityId)
    if city is None or city.getOwner() != kTriggeredData.ePlayer:
        return False

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId

    return True


def canApplyMasterBlacksmithDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_COPPER")
    city = player.getCity(kTriggeredData.iCityId)

    if city is None:
        return False

    map = gc.getMap()
    iBestValue = map.getGridWidth() + map.getGridHeight()
    bestPlot = None
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == kTriggeredData.ePlayer and plot.canHaveBonus(iBonus, False):
            iValue = plotDistance(city.getX(), city.getY(), plot.getX(), plot.getY())
            if iValue < iBestValue:
                iBestValue = iValue
                bestPlot = plot

    if bestPlot is None:
        return False

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iPlotX = bestPlot.getX()
    kActualTriggeredDataObject.iPlotY = bestPlot.getY()

    return True


def applyMasterBlacksmithDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    city = player.getCity(kTriggeredData.iCityId)

    iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_COPPER")
    plot.setBonusType(iBonus)

    szBuffer = localText.getText(
        "TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE",
        (gc.getBonusInfo(iBonus).getTextKey(), city.getNameKey()),
    )
    CyInterface().addMessage(
        kTriggeredData.ePlayer,
        False,
        gc.getEVENT_MESSAGE_TIME(),
        szBuffer,
        "AS2D_DISCOVERBONUS",
        InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
        gc.getBonusInfo(iBonus).getButton(),
        gc.getInfoTypeForString("COLOR_WHITE"),
        plot.getX(),
        plot.getY(),
        True,
        True,
    )


def canApplyMasterBlacksmithDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getStateReligion() == -1:
        return False

    return True


######## THE BEST DEFENSE ###########


def canTriggerBestDefense(argsList):
    kTriggeredData = argsList[0]

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    return True


def getHelpBestDefense1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iRequired /= 2
    iRequired += 1

    szHelp = localText.getText("TXT_KEY_EVENT_BEST_DEFENSE_HELP_1", (iRequired,))

    return szHelp


def canTriggerBestDefenseDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iCastle = CvUtil.findInfoTypeNum(
        gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), "BUILDINGCLASS_CASTLE"
    )
    iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iBuildingsRequired /= 2
    iBuildingsRequired += 2
    if iBuildingsRequired > player.getBuildingClassCount(iCastle):
        return False

    return True


def getHelpBestDefenseDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_BEST_DEFENSE_DONE_HELP_2", (3,))

    return szHelp


def applyBestDefenseDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
            loopTeam = gc.getTeam(loopPlayer.getTeam())
            if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
                loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 3)


def canApplyBestDefenseDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iGreatWall = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_GREAT_WALL"
    )

    (loopCity, iter) = player.firstCity(False)
    while loopCity:
        if loopCity.isHasBuilding(iGreatWall):
            return True

        (loopCity, iter) = player.nextCity(iter, False)

    return False


######## NATIONAL SPORTS LEAGUE ###########


def canTriggerSportsLeague(argsList):
    kTriggeredData = argsList[0]

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    return True


def getHelpSportsLeague1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iRequired /= 2
    iRequired += 2
    iBuilding = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_STATUE_OF_ZEUS"
    )

    szHelp = localText.getText(
        "TXT_KEY_EVENT_SPORTS_LEAGUE_HELP_1",
        (iRequired, gc.getBuildingInfo(iBuilding).getTextKey()),
    )

    return szHelp


def canTriggerSportsLeagueDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iCastle = CvUtil.findInfoTypeNum(
        gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), "BUILDINGCLASS_COLOSSEUM"
    )
    # Rhye
    iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    # Rhye
    iBuildingsRequired /= 2
    iBuildingsRequired += 2
    if iBuildingsRequired > player.getBuildingClassCount(iCastle):
        return False

    return True


def canApplySportsLeagueDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iZeus = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_STATUE_OF_ZEUS"
    )

    (loopCity, iter) = player.firstCity(False)
    while loopCity:
        if loopCity.isHasBuilding(iZeus):
            return True

        (loopCity, iter) = player.nextCity(iter, False)

    return False


######## CRUSADE ###########


def canTriggerCrusade(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    if holyCity.getOwner() != kTriggeredData.eOtherPlayer:
        return False

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iOtherPlayerCityId = holyCity.getID()

    return True


def getHelpCrusade1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

    szHelp = localText.getText("TXT_KEY_EVENT_CRUSADE_HELP_1", (holyCity.getNameKey(),))

    return szHelp


def expireCrusade1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

    if holyCity.getOwner() == kTriggeredData.ePlayer:
        return False

    if player.getStateReligion() != kTriggeredData.eReligion:
        return True

    if holyCity.getOwner() != kTriggeredData.eOtherPlayer:
        return True

    if not gc.getTeam(player.getTeam()).isAtWar(otherPlayer.getTeam()):
        return True

    return False


def canTriggerCrusadeDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
    holyCity = gc.getGame().getHolyCity(kOrigTriggeredData.eReligion)

    if holyCity.getOwner() != kTriggeredData.ePlayer:
        return False

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iCityId = holyCity.getID()
    kActualTriggeredDataObject.eOtherPlayer = kOrigTriggeredData.eOtherPlayer
    kActualTriggeredDataObject.eReligion = kOrigTriggeredData.eReligion

    for iBuilding in range(gc.getNumBuildingInfos()):
        if gc.getBuildingInfo(iBuilding).getHolyCity() == kOrigTriggeredData.eReligion:
            kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
            break

    return True


def getHelpCrusadeDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
    szUnit = gc.getUnitInfo(holyCity.getConscriptUnit()).getTextKey()
    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1
    szHelp = localText.getText(
        "TXT_KEY_EVENT_CRUSADE_DONE_HELP_1", (iNumUnits, szUnit, holyCity.getNameKey())
    )

    return szHelp


def canApplyCrusadeDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
    if -1 == holyCity.getConscriptUnit():
        return False

    return True


def applyCrusadeDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
    iUnitType = holyCity.getConscriptUnit()
    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1

    if iUnitType != -1:
        for i in range(iNumUnits):
            player.initUnit(
                iUnitType,
                holyCity.getX(),
                holyCity.getY(),
                UnitAITypes.UNITAI_CITY_DEFENSE,
                DirectionTypes.DIRECTION_SOUTH,
            )


def getHelpCrusadeDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

    szHelp = localText.getText(
        "TXT_KEY_EVENT_CRUSADE_DONE_HELP_2",
        (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), holyCity.getNameKey()),
    )

    return szHelp


def canApplyCrusadeDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

    if -1 == kTriggeredData.eBuilding or holyCity.isHasBuilding(kTriggeredData.eBuilding):
        return False

    return True


def applyCrusadeDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
    holyCity.setNumRealBuilding(kTriggeredData.eBuilding, 1)

    if (
        not gc.getGame().isNetworkMultiPlayer()
        and kTriggeredData.ePlayer == gc.getGame().getActivePlayer()
    ):
        popupInfo = CyPopupInfo()
        popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
        popupInfo.setData1(kTriggeredData.eBuilding)
        popupInfo.setData2(holyCity.getID())
        popupInfo.setData3(0)
        popupInfo.setText(u"showWonderMovie")
        popupInfo.addPopup(kTriggeredData.ePlayer)


def getHelpCrusadeDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumCities = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

    szHelp = localText.getText(
        "TXT_KEY_EVENT_CRUSADE_DONE_HELP_3",
        (gc.getReligionInfo(kTriggeredData.eReligion).getTextKey(), iNumCities),
    )

    return szHelp


def canApplyCrusadeDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumCities = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()

    if gc.getGame().getNumCities() == gc.getGame().countReligionLevels(kTriggeredData.eReligion):
        return False

    return True


def applyCrusadeDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

    listCities = []
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            (loopCity, iter) = loopPlayer.firstCity(False)

            while loopCity:
                if not loopCity.isHasReligion(kTriggeredData.eReligion):
                    iDistance = plotDistance(
                        holyCity.getX(), holyCity.getY(), loopCity.getX(), loopCity.getY()
                    )
                    listCities.append((iDistance, loopCity))

                (loopCity, iter) = loopPlayer.nextCity(iter, False)

    listCities.sort()

    iNumCities = min(
        gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers(), len(listCities)
    )

    for i in range(iNumCities):
        iDistance, loopCity = listCities[i]
        loopCity.setHasReligion(kTriggeredData.eReligion, True, True, True)


######## ESTEEMEED_PLAYWRIGHT ###########


def canTriggerEsteemedPlaywright(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    # If source civ is operating this Civic, disallow the event to trigger.
    if player.isCivic(
        CvUtil.findInfoTypeNum(gc.getCivicInfo, gc.getNumCivicInfos(), "CIVIC_SLAVERY")
    ):
        return False

    return True


######## SECRET_KNOWLEDGE ###########


def getHelpSecretKnowledge2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    szHelp = localText.getText(
        "TXT_KEY_EVENT_YIELD_CHANGE_BUILDING",
        (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), u"+4[ICON_CULTURE]"),
    )

    return szHelp


def applySecretKnowledge2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = player.getCity(kTriggeredData.iCityId)
    city.setBuildingCommerceChange(
        gc.getBuildingInfo(kTriggeredData.eBuilding).getBuildingClassType(),
        CommerceTypes.COMMERCE_CULTURE,
        4,
    )


######## HIGH_WARLORD ###########


def canTriggerHighWarlord(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    # If source civ is operating this Civic, disallow the event to trigger.
    if player.isCivic(
        CvUtil.findInfoTypeNum(gc.getCivicInfo, gc.getNumCivicInfos(), "CIVIC_EMANCIPATION")
    ):
        return False

    return True


######## EXPERIENCED_CAPTAIN ###########


def canTriggerExperiencedCaptain(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    if unit.isNone():
        return False

    if unit.getExperience() < 7:
        return False

    return True


######## PARTISANS ###########


def getNumPartisanUnits(plot, iPlayer):
    for i in range(gc.getNumCultureLevelInfos()):
        iI = gc.getNumCultureLevelInfos() - i - 1
        if plot.getCulture(iPlayer) >= gc.getCultureLevelInfo(iI).getSpeedThreshold(
            gc.getGame().getGameSpeedType()
        ):
            return iI
    return 0


def getHelpPartisans1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    capital = player.getCapitalCity()
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if None is not capital and not capital.isNone():
        iNumUnits = getNumPartisanUnits(plot, kTriggeredData.ePlayer)
        szUnit = gc.getUnitInfo(capital.getConscriptUnit()).getTextKey()

        szHelp = localText.getText("TXT_KEY_EVENT_PARTISANS_HELP_1", (iNumUnits, szUnit))

    return szHelp


def canApplyPartisans1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if getNumPartisanUnits(plot, kTriggeredData.ePlayer) <= 0:
        return False

    for i in range(3):
        for j in range(3):
            loopPlot = gc.getMap().plot(
                kTriggeredData.iPlotX + i - 1, kTriggeredData.iPlotY + j - 1
            )
            if None is not loopPlot and not loopPlot.isNone():
                if not (
                    loopPlot.isVisibleEnemyUnit(kTriggeredData.ePlayer)
                    or loopPlot.isWater()
                    or loopPlot.isImpassable()
                    or loopPlot.isCity()
                ):
                    return True
    return False


def applyPartisans1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    capital = player.getCapitalCity()
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if None is not capital and not capital.isNone():
        iNumUnits = getNumPartisanUnits(plot, kTriggeredData.ePlayer)

        listPlots = []
        for i in range(3):
            for j in range(3):
                loopPlot = gc.getMap().plot(
                    kTriggeredData.iPlotX + i - 1, kTriggeredData.iPlotY + j - 1
                )
                if None is not loopPlot and not loopPlot.isNone() and (i != 1 or j != 1):
                    if not (
                        loopPlot.isVisibleEnemyUnit(kTriggeredData.ePlayer)
                        or loopPlot.isWater()
                        or loopPlot.isImpassable()
                    ):
                        listPlots.append(loopPlot)

        if len(listPlots) > 0:
            for i in range(iNumUnits):
                iPlot = choice(listPlots)
                player.initUnit(
                    capital.getConscriptUnit(),
                    iPlot.getX(),
                    iPlot.getY(),
                    UnitAITypes.UNITAI_ATTACK,
                    DirectionTypes.DIRECTION_SOUTH,
                )


def getHelpPartisans2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    capital = player.getCapitalCity()
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if None is not capital and not capital.isNone():
        iNumUnits = max(1, getNumPartisanUnits(plot, kTriggeredData.ePlayer) / 2)
        szUnit = gc.getUnitInfo(capital.getConscriptUnit()).getTextKey()

        szHelp = localText.getText(
            "TXT_KEY_EVENT_PARTISANS_HELP_2", (iNumUnits, szUnit, capital.getNameKey())
        )

    return szHelp


def canApplyPartisans2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    return max(1, getNumPartisanUnits(plot, kTriggeredData.ePlayer) / 2) > 0


def applyPartisans2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    capital = player.getCapitalCity()
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if None is not capital and not capital.isNone():
        iNumUnits = max(1, getNumPartisanUnits(plot, kTriggeredData.ePlayer) / 2)
        for i in range(iNumUnits):
            player.initUnit(
                capital.getConscriptUnit(),
                capital.getX(),
                capital.getY(),
                UnitAITypes.UNITAI_ATTACK,
                DirectionTypes.DIRECTION_SOUTH,
            )


######## GREED ###########


def canTriggerGreed(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    if not gc.getTeam(player.getTeam()).canChangeWarPeace(otherPlayer.getTeam()):
        return False

    listBonuses = []
    iOil = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_OIL")
    if 0 == player.getNumAvailableBonuses(iOil):
        listBonuses.append(iOil)
    iIron = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_IRON")
    if 0 == player.getNumAvailableBonuses(iIron):
        listBonuses.append(iIron)
    iHorse = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_HORSE")
    if 0 == player.getNumAvailableBonuses(iHorse):
        listBonuses.append(iHorse)
    iCopper = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_COPPER")
    if 0 == player.getNumAvailableBonuses(iCopper):
        listBonuses.append(iCopper)

    map = gc.getMap()
    bFound = False
    listPlots = []
    for iBonus in listBonuses:
        for i in range(map.numPlots()):
            loopPlot = map.plotByIndex(i)
            if (
                loopPlot.getOwner() == kTriggeredData.eOtherPlayer
                and loopPlot.getBonusType(player.getTeam()) == iBonus
                and loopPlot.isRevealed(player.getTeam(), False)
                and not loopPlot.isWater()
            ):
                listPlots.append(loopPlot)
                bFound = True
        if bFound:
            break

    if not bFound:
        return False

    plot = choice(listPlots)

    if -1 == getGreedUnit(player, plot):
        return False

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iPlotX = plot.getX()
    kActualTriggeredDataObject.iPlotY = plot.getY()

    return True


def getHelpGreed1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    iBonus = (
        gc.getMap()
        .plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
        .getBonusType(player.getTeam())
    )

    iTurns = gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent()

    szHelp = localText.getText(
        "TXT_KEY_EVENT_GREED_HELP_1",
        (
            otherPlayer.getCivilizationShortDescriptionKey(),
            gc.getBonusInfo(iBonus).getTextKey(),
            iTurns,
        ),
    )

    return szHelp


def expireGreed1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if plot.getOwner() == kTriggeredData.ePlayer or plot.getOwner() == -1:
        return False

    if (
        turn()
        >= kTriggeredData.iTurn
        + gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent()
    ):
        return True

    if plot.getOwner() != kTriggeredData.eOtherPlayer:
        return True

    return False


def canTriggerGreedDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
    plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)

    if plot.getOwner() != kOrigTriggeredData.ePlayer:
        return False

    if -1 == getGreedUnit(player, plot):
        return False

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY
    kActualTriggeredDataObject.eOtherPlayer = kOrigTriggeredData.eOtherPlayer

    return True


def getGreedUnit(player, plot):
    iBonus = plot.getBonusType(player.getTeam())
    iBestValue = 0
    iBestUnit = -1
    for iUnitClass in range(gc.getNumUnitClassInfos()):
        iUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(
            iUnitClass
        )
        if (
            -1 != iUnit
            and player.canTrain(iUnit, False, False)
            and (gc.getUnitInfo(iUnit).getDomainType() == DomainTypes.DOMAIN_LAND)
        ):
            iValue = 0
            if gc.getUnitInfo(iUnit).getPrereqAndBonus() == iBonus:
                iValue = player.AI_unitValue(iUnit, UnitAITypes.UNITAI_ATTACK, plot.area())
            else:
                for j in range(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
                    if gc.getUnitInfo(iUnit).getPrereqOrBonuses(j) == iBonus:
                        iValue = player.AI_unitValue(iUnit, UnitAITypes.UNITAI_ATTACK, plot.area())
                        break
            if iValue > iBestValue:
                iBestValue = iValue
                iBestUnit = iUnit

    return iBestUnit


def getHelpGreedDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1
    iUnitType = getGreedUnit(player, plot)

    if iUnitType != -1:
        szHelp = localText.getText(
            "TXT_KEY_EVENT_GREED_DONE_HELP_1", (iNumUnits, gc.getUnitInfo(iUnitType).getTextKey())
        )

    return szHelp


def applyGreedDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iUnitType = getGreedUnit(player, plot)
    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1

    if iUnitType != -1:
        for i in range(iNumUnits):
            player.initUnit(
                iUnitType,
                plot.getX(),
                plot.getY(),
                UnitAITypes.UNITAI_ATTACK,
                DirectionTypes.DIRECTION_SOUTH,
            )


######## WAR CHARIOTS ###########


def canTriggerWarChariots(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eReligion = ReligionTypes(player.getStateReligion())

    return True


def getHelpWarChariots1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
    szHelp = localText.getText("TXT_KEY_EVENT_WAR_CHARIOTS_HELP_1", (iNumUnits,))

    return szHelp


def canTriggerWarChariotsDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
    iUnitClassType = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_CHARIOT"
    )
    if player.getUnitClassCount(iUnitClassType) < iNumUnits:
        return False

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eReligion = kOrigTriggeredData.eReligion

    return True


######## ELITE SWORDSMEN ###########


def getHelpEliteSwords1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
    szHelp = localText.getText("TXT_KEY_EVENT_ELITE_SWORDS_HELP_1", (iNumUnits,))

    return szHelp


def canTriggerEliteSwordsDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
    iUnitClassType = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_SWORDSMAN"
    )
    if player.getUnitClassCount(iUnitClassType) < iNumUnits:
        return False

    return True


def canApplyEliteSwordsDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iCivic = CvUtil.findInfoTypeNum(
        gc.getCivicInfo, gc.getNumCivicInfos(), "CIVIC_HEREDITARY_RULE"
    )

    if not player.isCivic(iCivic):
        return False

    return True


######## WARSHIPS ###########


def canTriggerWarships(argsList):
    kTriggeredData = argsList[0]

    map = gc.getMap()
    iNumWater = 0

    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)

        if plot.isWater():
            iNumWater += 1

        if 100 * iNumWater >= 55 * map.numPlots():
            return True

    return False


def getHelpWarships1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()

    iBuilding = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_GREAT_LIGHTHOUSE"
    )
    szHelp = localText.getText(
        "TXT_KEY_EVENT_WARSHIPS_HELP_1", (iNumUnits, gc.getBuildingInfo(iBuilding).getTextKey())
    )

    return szHelp


def canTriggerWarshipsDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
    iUnitClassType = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_TRIREME"
    )

    if player.getUnitClassCount(iUnitClassType) < iNumUnits:
        return False

    return True


def canApplyWarshipsDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iBuilding = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_GREAT_LIGHTHOUSE"
    )
    if player.getBuildingClassCount(gc.getBuildingInfo(iBuilding).getBuildingClassType()) == 0:
        return False

    return True


######## GUNS NOT BUTTER ###########


def getHelpGunsButter1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
    iBuilding = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_TAJ_MAHAL"
    )

    szHelp = localText.getText(
        "TXT_KEY_EVENT_GUNS_BUTTER_HELP_1", (iNumUnits, gc.getBuildingInfo(iBuilding).getTextKey())
    )

    return szHelp


def canTriggerGunsButterDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
    iUnitClassType = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_MUSKETMAN"
    )

    if player.getUnitClassCount(iUnitClassType) < iNumUnits:
        return False

    return True


def canApplyGunsButterDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iCivic = CvUtil.findInfoTypeNum(gc.getCivicInfo, gc.getNumCivicInfos(), "CIVIC_VASSALAGE")

    if not player.isCivic(iCivic):
        return False

    return True


def canApplyGunsButterDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iBuilding = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_TAJ_MAHAL"
    )
    if player.getBuildingClassCount(gc.getBuildingInfo(iBuilding).getBuildingClassType()) == 0:
        return False

    return True


######## NOBLE KNIGHTS ###########


def canTriggerNobleKnights(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eReligion = ReligionTypes(player.getStateReligion())

    return True


def getHelpNobleKnights1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
    iBuilding = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_ORACLE"
    )

    szHelp = localText.getText(
        "TXT_KEY_EVENT_NOBLE_KNIGHTS_HELP_1",
        (iNumUnits, gc.getBuildingInfo(iBuilding).getTextKey()),
    )

    return szHelp


def canTriggerNobleKnightsDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
    iUnitClassType = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_KNIGHT"
    )

    if player.getUnitClassCount(iUnitClassType) < iNumUnits:
        return False

    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eReligion = kOrigTriggeredData.eReligion

    iBuilding = CvUtil.findInfoTypeNum(
        gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_ORACLE"
    )

    (loopCity, iter) = player.firstCity(False)
    while loopCity:
        if loopCity.isHasBuilding(iBuilding):
            kActualTriggeredDataObject.iPlotX = loopCity.getX()
            kActualTriggeredDataObject.iPlotY = loopCity.getY()
            kActualTriggeredDataObject.iCityId = loopCity.getID()
            break

        (loopCity, iter) = player.nextCity(iter, False)

    return True


def canApplyNobleKnightsDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iCivic = CvUtil.findInfoTypeNum(
        gc.getCivicInfo, gc.getNumCivicInfos(), "CIVIC_ORGANIZED_RELIGION"
    )

    if not player.isCivic(iCivic):
        return False

    return True


######## OVERWHELM DOCTRINE ###########


def canTriggerOverwhelm(argsList):
    kTriggeredData = argsList[0]

    map = gc.getMap()
    iNumWater = 0

    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.isWater():
            iNumWater += 1
        # Rhye
        # if 100 * iNumWater >= 55 * map.numPlots():
        if 100 * iNumWater >= 45 * map.numPlots():
            return True
    return False


def getHelpOverwhelm1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iDestroyer = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_DESTROYER")
    iNumDestroyers = 4
    iBattleship = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_BATTLESHIP")
    iNumBattleships = 2
    iCarrier = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_CARRIER")
    iNumCarriers = 3
    iFighter = CvUtil.findInfoTypeNum(
        gc.getSpecialUnitInfo, gc.getNumSpecialUnitInfos(), "SPECIALUNIT_FIGHTER"
    )
    iNumFighters = 9
    iProject = CvUtil.findInfoTypeNum(
        gc.getProjectInfo, gc.getNumProjectInfos(), "PROJECT_MANHATTAN_PROJECT"
    )

    szHelp = localText.getText(
        "TXT_KEY_EVENT_OVERWHELM_HELP_1",
        (
            iNumDestroyers,
            gc.getUnitInfo(iDestroyer).getTextKey(),
            iNumBattleships,
            gc.getUnitInfo(iBattleship).getTextKey(),
            iNumCarriers,
            gc.getUnitInfo(iCarrier).getTextKey(),
            iNumFighters,
            gc.getSpecialUnitInfo(iFighter).getTextKey(),
            gc.getProjectInfo(iProject).getTextKey(),
        ),
    )

    return szHelp


def canTriggerOverwhelmDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iDestroyer = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_DESTROYER"
    )
    iNumDestroyers = 4
    if player.getUnitClassCount(iDestroyer) < iNumDestroyers:
        return False

    iBattleship = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_BATTLESHIP"
    )
    iNumBattleships = 2
    if player.getUnitClassCount(iBattleship) < iNumBattleships:
        return False

    iCarrier = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_CARRIER"
    )
    iNumCarriers = 3
    if player.getUnitClassCount(iCarrier) < iNumCarriers:
        return False

    iFighter = CvUtil.findInfoTypeNum(
        gc.getSpecialUnitInfo, gc.getNumSpecialUnitInfos(), "SPECIALUNIT_FIGHTER"
    )
    iNumFighters = 9
    iNumPlayerFighters = 0
    (loopUnit, iter) = player.firstUnit(False)
    while loopUnit:
        if loopUnit.getSpecialUnitType() == iFighter:
            iNumPlayerFighters += 1
        (loopUnit, iter) = player.nextUnit(iter, False)

    if iNumPlayerFighters < iNumFighters:
        return False

    return True


def getHelpOverwhelmDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_OVERWHELM_DONE_HELP_3", ())

    return szHelp


def canApplyOverwhelmDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iProject = CvUtil.findInfoTypeNum(
        gc.getProjectInfo, gc.getNumProjectInfos(), "PROJECT_MANHATTAN_PROJECT"
    )
    if gc.getTeam(player.getTeam()).getProjectCount(iProject) == 0:
        return False

    return True


def applyOverwhelmDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    gc.getGame().changeNoNukesCount(1)


######## CORPORATE EXPANSION ###########


def canTriggerCorporateExpansion(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = gc.getGame().getHeadquarters(kTriggeredData.eCorporation)
    if None is city or city.isNone():
        return False

    # Hack to remember the number of cities you already have with the Corporation
    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iOtherPlayerCityId = gc.getGame().countCorporationLevels(
        kTriggeredData.eCorporation
    )
    kActualTriggeredDataObject.iCityId = city.getID()
    kActualTriggeredDataObject.iPlotX = city.getX()
    kActualTriggeredDataObject.iPlotY = city.getY()

    bFound = False
    for iBuilding in range(gc.getNumBuildingInfos()):
        if gc.getBuildingInfo(iBuilding).getFoundsCorporation() == kTriggeredData.eCorporation:
            kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
            bFound = True
            break

    if not bFound:
        return False

    return True


def expireCorporateExpansion1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = player.getCity(kTriggeredData.iCityId)
    if None is city or city.isNone():
        return True

    return False


def getHelpCorporateExpansion1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumCities = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1

    szHelp = localText.getText(
        "TXT_KEY_EVENT_CORPORATE_EXPANSION_HELP_1",
        (gc.getCorporationInfo(kTriggeredData.eCorporation).getTextKey(), iNumCities),
    )

    return szHelp


def canTriggerCorporateExpansionDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    iNumCitiesRequired = (
        gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
        + 1
        + kOrigTriggeredData.iOtherPlayerCityId
    )

    if iNumCitiesRequired > gc.getGame().countCorporationLevels(kOrigTriggeredData.eCorporation):
        return False

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eCorporation = kOrigTriggeredData.eCorporation
    kActualTriggeredDataObject.eBuilding = kOrigTriggeredData.eBuilding
    kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY

    return True


def getHelpCorporateExpansionDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText(
        "TXT_KEY_EVENT_YIELD_CHANGE_BUILDING",
        (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), u"+10[ICON_GOLD]"),
    )

    return szHelp


def applyCorporateExpansionDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = player.getCity(kTriggeredData.iCityId)
    if None is not city and not city.isNone():
        city.setBuildingCommerceChange(
            gc.getBuildingInfo(kTriggeredData.eBuilding).getBuildingClassType(),
            CommerceTypes.COMMERCE_GOLD,
            10,
        )


######## HOSTILE TAKEOVER ###########


def canTriggerHostileTakeover(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if (
        gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
        and gc.getPlayer(kTriggeredData.ePlayer).isHuman()
    ):
        return False

    city = gc.getGame().getHeadquarters(kTriggeredData.eCorporation)
    if None is city or city.isNone():
        return False

    # Hack to remember the number of cities you already have with the Corporation
    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iCityId = city.getID()
    kActualTriggeredDataObject.iPlotX = city.getX()
    kActualTriggeredDataObject.iPlotY = city.getY()

    bFound = False
    for iBuilding in range(gc.getNumBuildingInfos()):
        if gc.getBuildingInfo(iBuilding).getFoundsCorporation() == kTriggeredData.eCorporation:
            kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
            bFound = True
            break

    if not bFound:
        return False

    listResources = getHostileTakeoverListResources(
        gc.getCorporationInfo(kTriggeredData.eCorporation), player
    )
    if len(listResources) == 0:
        return False

    return True


def expireHostileTakeover1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = player.getCity(kTriggeredData.iCityId)
    if None is city or city.isNone():
        return True

    return False


def getHostileTakeoverListResources(corporation, player):
    map = gc.getMap()
    listHave = []
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == player.getID():
            iBonus = plot.getBonusType(player.getTeam())
            if iBonus != -1:
                if iBonus not in listHave:
                    listHave.append(iBonus)
    listNeed = []
    for i in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
        iBonus = corporation.getPrereqBonus(i)
        if iBonus != -1:
            if iBonus not in listHave:
                listNeed.append(iBonus)
    return listNeed


def getHelpHostileTakeover1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listResources = getHostileTakeoverListResources(
        gc.getCorporationInfo(kTriggeredData.eCorporation), player
    )
    szList = u""
    bFirst = True
    for iBonus in listResources:
        if not bFirst:
            szList += u", "
        else:
            bFirst = False
        szList += (
            u"[COLOR_HIGHLIGHT_TEXT]"
            + gc.getBonusInfo(iBonus).getDescription()
            + u"[COLOR_REVERT]"
        )

    szHelp = localText.getText(
        "TXT_KEY_EVENT_HOSTILE_TAKEOVER_HELP_1", (len(listResources), szList)
    )

    return szHelp


def canTriggerHostileTakeoverDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    listResources = getHostileTakeoverListResources(
        gc.getCorporationInfo(kOrigTriggeredData.eCorporation), player
    )

    if len(listResources) > 0:
        return False

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eCorporation = kOrigTriggeredData.eCorporation
    kActualTriggeredDataObject.eBuilding = kOrigTriggeredData.eBuilding
    kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY

    return True


def getHelpHostileTakeoverDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText(
        "TXT_KEY_EVENT_YIELD_CHANGE_BUILDING",
        (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), u"+20[ICON_GOLD]"),
    )

    return szHelp


def applyHostileTakeoverDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = player.getCity(kTriggeredData.iCityId)
    if None is not city and not city.isNone():
        city.setBuildingCommerceChange(
            gc.getBuildingInfo(kTriggeredData.eBuilding).getBuildingClassType(),
            CommerceTypes.COMMERCE_GOLD,
            20,
        )


######## Great Beast ########


def doGreatBeast3(argsList):
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    (loopCity, iter) = player.firstCity(False)

    while loopCity:
        if loopCity.isHasReligion(kTriggeredData.eReligion):
            loopCity.changeHappinessTimer(40)
        (loopCity, iter) = player.nextCity(iter, False)


def getHelpGreatBeast3(argsList):
    kTriggeredData = argsList[1]
    religion = gc.getReligionInfo(kTriggeredData.eReligion)

    szHelp = localText.getText(
        "TXT_KEY_EVENT_GREAT_BEAST_3_HELP", (gc.getDefineINT("TEMP_HAPPY"), 40, religion.getChar())
    )

    return szHelp


####### Comet Fragment ########


def canDoCometFragment(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if (player.getSpaceProductionModifier()) > 10:
        return False

    return True


####### Immigrants ########


def canTriggerImmigrantCity(argsList):
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return False

    if (city.happyLevel() - city.unhappyLevel(0) < 1) or (
        city.goodHealth() - city.badHealth(True) < 1
    ):
        return False

    if city.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE) < 5500:
        return False


####### Controversial Philosopher ######


def canTriggerControversialPhilosopherCity(argsList):
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return False
    if not city.isCapital():
        return False
    if city.getCommerceRateTimes100(CommerceTypes.COMMERCE_RESEARCH) < 3500:
        return False

    return True


####### Spy Discovered #######


def canDoSpyDiscovered3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getNumCities() < 4:
        return False

    if player.getCapitalCity().isNone():
        return False

    return True


def doSpyDiscovered3(argsList):
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    plot = player.getCapitalCity().plot()
    iNumUnits = player.getNumCities() / 4
    iUnitClassType = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_TANK"
    )
    iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(
        iUnitClassType
    )

    if iUnitType != -1:
        for i in range(iNumUnits):
            player.initUnit(
                iUnitType,
                plot.getX(),
                plot.getY(),
                UnitAITypes.UNITAI_ATTACK,
                DirectionTypes.DIRECTION_SOUTH,
            )


def getHelpSpyDiscovered3(argsList):
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    iNumUnits = player.getNumCities() / 4
    szHelp = localText.getText("TXT_KEY_EVENT_SPY_DISCOVERED_3_HELP", (iNumUnits,))

    return szHelp


####### Nuclear Protest #######


def canTriggerNuclearProtest(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iICBMClass = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_ICBM"
    )
    iTacNukeClass = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_TACTICAL_NUKE"
    )
    if player.getUnitClassCount(iICBMClass) + player.getUnitClassCount(iTacNukeClass) < 10:
        return False

    return True


def doNuclearProtest1(argsList):
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iICBMClass = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_ICBM"
    )
    iTacNukeClass = CvUtil.findInfoTypeNum(
        gc.getUnitClassInfo, gc.getNumUnitClassInfos(), "UNITCLASS_TACTICAL_NUKE"
    )

    (loopUnit, iter) = player.firstUnit(False)
    while loopUnit:
        if (
            loopUnit.getUnitClassType() == iICBMClass
            or loopUnit.getUnitClassType() == iTacNukeClass
        ):
            loopUnit.kill(False, -1)
        (loopUnit, iter) = player.nextUnit(iter, False)


def getHelpNuclearProtest1(argsList):
    szHelp = localText.getText("TXT_KEY_EVENT_NUCLEAR_PROTEST_1_HELP", ())
    return szHelp


######## Preaching Researcher #######


def canTriggerPreachingResearcherCity(argsList):
    iCity = argsList[2]

    player = gc.getPlayer(argsList[1])
    city = player.getCity(iCity)

    if city.isHasBuilding(gc.getInfoTypeForString("BUILDING_UNIVERSITY")):
        return True
    return False


######## Toxcatl (Aztec event) #########


def canTriggerToxcatl(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_AZTEC"):
        return True
    return False


######## Dissident Priest (Egyptian event) #######


def canTriggerDissidentPriest(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_EGYPT"):
        return True
    return False


def canTriggerDissidentPriestCity(argsList):
    iCity = argsList[2]

    player = gc.getPlayer(argsList[1])
    city = player.getCity(iCity)

    if city.isGovernmentCenter():
        return False
    if city.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE) < 3000:
        return False
    if player.getStateReligion() != -1:
        return False

    return True


######## Rogue Station  (Russian event) ###########


def canTriggerRogueStation(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_RUSSIA"):
        return True
    return False


######## Antimonarchists (French event) #########


def canTriggerAntiMonarchists(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_FRANCE"):
        return True
    return False


######## Impeachment (American event) ########


def canTriggerImpeachment(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_AMERICA"):
        return True
    return False


def canTriggerImpeachmentCity(argsList):
    iCity = argsList[2]

    player = gc.getPlayer(argsList[1])
    city = player.getCity(iCity)

    if city.isCapital():
        return True
    return False
