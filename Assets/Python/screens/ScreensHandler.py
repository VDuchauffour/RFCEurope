from CvPythonExtensions import *
import CvPlatyBuilderSettings
import CvAdvisorUtils
import CvTopCivs
import CvEspionageAdvisor
import CvScreensInterface
import CvDebugTools
import CvWBPopups
import CvCameraControls
import CvUtil
import PyHelpers
import Popup as PyPopup
from Core import (
    civilization,
    get_data_from_upside_down_map,
    get_scenario_start_turn,
    human,
    player,
    text,
)
from MiscData import MODNET_EVENTS
from CityMapData import CITIES_MAP
from Events import events, handler

## Ultrapack ##
import WBCityEditScreen
import WBUnitScreen
import WBPlayerScreen
import WBGameDataScreen
import WBPlotScreen
import CvPlatyBuilderScreen

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo


@handler("kbdEvent")
def onKbdEvent(eventType, key, mx, my, px, py):
    if events.bAllowCheats:
        # notify debug tools of input to allow it to override the control
        argsList = (
            eventType,
            key,
            events.bCtrl,
            events.bShift,
            events.bAlt,
            mx,
            my,
            px,
            py,
            gc.getGame().isNetworkMultiPlayer(),
        )
        if CvDebugTools.g_CvDebugTools.notifyInput(argsList):
            return 0

    if eventType == events.EventKeyDown:
        key = int(key)

        CvCameraControls.g_CameraControls.handleInput(key)

        if events.bAllowCheats:
            # Shift - T (Debug - No MP)
            if key == int(InputTypes.KB_T):
                if events.bShift:
                    events.beginEvent(CvUtil.EventAwardTechsAndGold)
                    # events.beginEvent(CvUtil.EventCameraControlPopup)
                    return 1

            elif key == int(InputTypes.KB_W):
                if events.bShift and events.bCtrl:
                    events.beginEvent(CvUtil.EventShowWonder)
                    return 1

            # Shift - ] (Debug - currently mouse-overd unit, health += 10
            elif key == int(InputTypes.KB_LBRACKET) and events.bShift:
                unit = CyMap().plot(px, py).getUnit(0)
                if not unit.isNone():
                    d = min(unit.maxHitPoints() - 1, unit.getDamage() + 10)
                    unit.setDamage(d, PlayerTypes.NO_PLAYER)

            # Shift - [ (Debug - currently mouse-overd unit, health -= 10
            elif key == int(InputTypes.KB_RBRACKET) and events.bShift:
                unit = CyMap().plot(px, py).getUnit(0)
                if not unit.isNone():
                    d = max(0, unit.getDamage() - 10)
                    unit.setDamage(d, PlayerTypes.NO_PLAYER)

            elif key == int(InputTypes.KB_F1):
                if events.bShift:
                    CvScreensInterface.replayScreen.showScreen(False)
                    return 1
                # don't return 1 unless you want the input consumed

            elif key == int(InputTypes.KB_F2):
                if events.bShift:
                    CvScreensInterface.showDebugInfoScreen()
                    return 1

            elif key == int(InputTypes.KB_F3):
                if events.bShift:
                    CvScreensInterface.showDanQuayleScreen(())
                    return 1

            elif key == int(InputTypes.KB_F4):
                if events.bShift:
                    CvScreensInterface.showUnVictoryScreen(())
                    return 1


@handler("mouseEvent")
def onMouseEvent(eventType, mx, my, px, py, interfaceConsumed, screens):
    if px != -1 and py != -1:
        if eventType == events.EventLButtonDown:
            if (
                events.bAllowCheats
                and events.bCtrl
                and events.bAlt
                and CyMap().plot(px, py).isCity()
                and not interfaceConsumed
            ):
                # Launch Edit City Event
                events.beginEvent(CvUtil.EventEditCity, (px, py))
                return 1

            elif events.bAllowCheats and events.bCtrl and events.bShift and not interfaceConsumed:
                # Launch Place Object Event
                events.beginEvent(CvUtil.EventPlaceObject, (px, py))
                return 1

    if eventType == events.EventBack:
        return CvScreensInterface.handleBack(screens)
    elif eventType == events.EventForward:
        return CvScreensInterface.handleForward(screens)


@handler("ModNetMessage")
def onModNetMessage(iData1, iData2, iData3, iData4, iData5):
    if iData1 == MODNET_EVENTS["CHANGE_COMMERCE_PERCENT"]:
        CommerceType = [
            CommerceTypes.COMMERCE_GOLD,
            CommerceTypes.COMMERCE_RESEARCH,
            CommerceTypes.COMMERCE_CULTURE,
            CommerceTypes.COMMERCE_ESPIONAGE,
        ]
        gc.getPlayer(iData2).changeCommercePercent(CommerceType[iData3], iData4)
        if iData2 == CyGame().getActivePlayer():
            screen = CvEspionageAdvisor.CvEspionageAdvisor().getScreen()
            if screen.isActive():
                CvEspionageAdvisor.CvEspionageAdvisor().updateEspionageWeights()


@handler("Update")
def onUpdate(delta_time):
    # allow camera to be updated
    CvCameraControls.g_CameraControls.onUpdate(delta_time)


@handler("OnLoad")
def onLoadGame():
    CvAdvisorUtils.resetNoLiberateCities()
    return 0


@handler("GameStart")
def onGameStart():
    # Rhye - Dawn of Man must appear in late starts too
    # Duplicate with Assets/Python/Contrib/CvAllErasDawnOfManScreenEventManager.py
    if gc.getGame().getStartEra() == gc.getDefineINT("STANDARD_ERA") or gc.getGame().isOption(
        GameOptionTypes.GAMEOPTION_ADVANCED_START
    ):
        if civilization().date.birth <= get_scenario_start_turn():
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
            popupInfo.setText(u"showDawnOfMan")
            popupInfo.addPopup(human())
    else:
        CyInterface().setSoundSelectionReady(true)

        if gc.getGame().isPbem():
            for iPlayer in range(gc.getMAX_PLAYERS()):
                player = gc.getPlayer(iPlayer)
                if player.isAlive() and player.isHuman():
                    popupInfo = CyPopupInfo()
                    popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_DETAILS)
                    popupInfo.setOption1(true)
                    popupInfo.addPopup(iPlayer)

        CvAdvisorUtils.resetNoLiberateCities()


@handler("BeginGameTurn")
def onBeginTurn(iGameTurn):
    CvTopCivs.CvTopCivs().turnChecker(iGameTurn)


@handler("EndPlayerTurn")
def onEndPlayerTurn(iGameTurn, iPlayer):
    if gc.getGame().getElapsedGameTurns() == 1:
        if gc.getPlayer(iPlayer).isHuman():
            if gc.getPlayer(iPlayer).canRevolution(0):
                popupInfo = CyPopupInfo()
                popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHANGECIVIC)
                popupInfo.addPopup(iPlayer)

    CvAdvisorUtils.resetAdvisorNags()
    CvAdvisorUtils.endTurnFeats(iPlayer)


@handler("firstContact")
def onFirstContact(iTeamX, iHasMetTeamY):
    ## Platy Builder ##
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    ## Platy Builder ##
    if not events._LOG_CONTACT:
        return
    CvUtil.pyPrint("Team %d has met Team %d" % (iTeamX, iHasMetTeamY))


@handler("combatResult")
def onCombatResult(pWinner, pLoser):
    playerX = PyPlayer(pWinner.getOwner())
    unitX = PyInfo.UnitInfo(pWinner.getUnitType())
    playerY = PyPlayer(pLoser.getOwner())
    unitY = PyInfo.UnitInfo(pLoser.getUnitType())
    if not events._LOG_COMBAT:
        return
    if playerX and playerX and unitX and playerY:
        CvUtil.pyPrint(
            "Player %d Civilization %s Unit %s has defeated Player %d Civilization %s Unit %s"
            % (
                playerX.getID(),
                playerX.getCivilizationName(),
                unitX.getDescription(),
                playerY.getID(),
                playerY.getCivilizationName(),
                unitY.getDescription(),
            )
        )


@handler("combatLogCalc")
def onCombatLogCalc(argsList):
    "Combat Result"
    genericArgs = argsList[0]
    cdAttacker = genericArgs[0]
    cdDefender = genericArgs[1]
    iCombatOdds = genericArgs[2]
    CvUtil.combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds)


@handler("combatLogHit")
def onCombatLogHit(argsList):
    "Combat Message"
    global gCombatMessages, gCombatLog
    genericArgs = argsList[0]
    cdAttacker = genericArgs[0]
    cdDefender = genericArgs[1]
    iIsAttacker = genericArgs[2]
    iDamage = genericArgs[3]
    if cdDefender.eOwner == cdDefender.eVisualOwner:
        szDefenderName = gc.getPlayer(cdDefender.eOwner).getNameKey()
    else:
        szDefenderName = text("TXT_KEY_TRAIT_PLAYER_UNKNOWN")
    if cdAttacker.eOwner == cdAttacker.eVisualOwner:
        szAttackerName = gc.getPlayer(cdAttacker.eOwner).getNameKey()
    else:
        szAttackerName = text("TXT_KEY_TRAIT_PLAYER_UNKNOWN")

    if iIsAttacker == 0:
        combatMessage = text(
            "TXT_KEY_COMBAT_MESSAGE_HIT",
            szDefenderName,
            cdDefender.sUnitName,
            iDamage,
            cdDefender.iCurrHitPoints,
            cdDefender.iMaxHitPoints,
        )
        CyInterface().addCombatMessage(cdAttacker.eOwner, combatMessage)
        CyInterface().addCombatMessage(cdDefender.eOwner, combatMessage)
        if cdDefender.iCurrHitPoints <= 0:
            combatMessage = text(
                "TXT_KEY_COMBAT_MESSAGE_DEFEATED",
                szAttackerName,
                cdAttacker.sUnitName,
                szDefenderName,
                cdDefender.sUnitName,
            )
            CyInterface().addCombatMessage(cdAttacker.eOwner, combatMessage)
            CyInterface().addCombatMessage(cdDefender.eOwner, combatMessage)
    elif iIsAttacker == 1:
        combatMessage = text(
            "TXT_KEY_COMBAT_MESSAGE_HIT",
            szAttackerName,
            cdAttacker.sUnitName,
            iDamage,
            cdAttacker.iCurrHitPoints,
            cdAttacker.iMaxHitPoints,
        )
        CyInterface().addCombatMessage(cdAttacker.eOwner, combatMessage)
        CyInterface().addCombatMessage(cdDefender.eOwner, combatMessage)
        if cdAttacker.iCurrHitPoints <= 0:
            combatMessage = text(
                "TXT_KEY_COMBAT_MESSAGE_DEFEATED",
                szDefenderName,
                cdDefender.sUnitName,
                szAttackerName,
                cdAttacker.sUnitName,
            )
            CyInterface().addCombatMessage(cdAttacker.eOwner, combatMessage)
            CyInterface().addCombatMessage(cdDefender.eOwner, combatMessage)


@handler("improvementBuilt")
def onImprovementBuilt(iImprovement, iX, iY):
    ## Platy Builder ##
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    ## Platy Builder ##
    "Improvement Built"
    if not events._LOG_IMPROVEMENT:
        return
    CvUtil.pyPrint(
        "Improvement %s was built at %d, %d"
        % (PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY)
    )


@handler("improvementDestroyed")
def onImprovementDestroyed(iImprovement, iOwner, iX, iY):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    "Improvement Destroyed"
    if not events._LOG_IMPROVEMENT:
        return
    CvUtil.pyPrint(
        "Improvement %s was Destroyed at %d, %d"
        % (PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY)
    )


@handler("routeBuilt")
def onRouteBuilt(iRoute, iX, iY):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    "Route Built"
    if not events._LOG_IMPROVEMENT:
        return
    CvUtil.pyPrint(
        "Route %s was built at %d, %d" % (gc.getRouteInfo(iRoute).getDescription(), iX, iY)
    )


@handler("buildingBuilt")
def onBuildingBuilt(pCity, iBuildingType):
    game = gc.getGame()
    iPlayer = pCity.getOwner()
    if (
        (not game.isNetworkMultiPlayer())
        and (iPlayer == game.getActivePlayer())
        and isWorldWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType())
    ):
        if not CyGame().GetWorldBuilderMode():
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
            popupInfo.setData1(iBuildingType)
            popupInfo.setData2(pCity.getID())
            popupInfo.setData3(0)
            popupInfo.setText(u"showWonderMovie")
            popupInfo.addPopup(iPlayer)

    CvAdvisorUtils.buildingBuiltFeats(pCity, iBuildingType)

    if not events._LOG_BUILDING:
        return
    CvUtil.pyPrint(
        "%s was finished by Player %d Civilization %s"
        % (
            PyInfo.BuildingInfo(iBuildingType).getDescription(),
            iPlayer,
            player(iPlayer).getCivilizationDescription(0),
        )
    )


@handler("projectBuilt")
def onProjectBuilt(pCity, iProjectType):
    iPlayer = pCity.getOwner()
    game = gc.getGame()
    if (not game.isNetworkMultiPlayer()) and (iPlayer == game.getActivePlayer()):
        if not CyGame().GetWorldBuilderMode():
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
            popupInfo.setData1(iProjectType)
            popupInfo.setData2(pCity.getID())
            popupInfo.setData3(2)
            popupInfo.setText(u"showWonderMovie")
            popupInfo.addPopup(iPlayer)


@handler("selectionGroupPushMission")
def onSelectionGroupPushMission(eOwner, eMission):
    if not events._LOG_PUSH_MISSION:
        return
    if pHeadUnit:  # type: ignore
        CvUtil.pyPrint("Selection Group pushed mission %d" % (eMission))


@handler("unitMove")
def onUnitMove(pPlot, pUnit, pOldPlot):
    player = PyPlayer(pUnit.getOwner())
    unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
    if not events._LOG_MOVEMENT:
        return
    if player and unitInfo:
        CvUtil.pyPrint(
            "Player %d Civilization %s unit %s is moving to %d, %d"
            % (
                player.getID(),
                player.getCivilizationName(),
                unitInfo.getDescription(),
                pUnit.getX(),
                pUnit.getY(),
            )
        )


@handler("unitCreated")
def on_unit_created(unit):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    player = PyPlayer(unit.getOwner())
    if not events._LOG_UNITBUILD:
        return


@handler("unitBuilt")
def on_unit_built(city, unit):
    player = PyPlayer(city.getOwner())
    CvAdvisorUtils.unitBuiltFeats(city, unit)

    if not events._LOG_UNITBUILD:
        return
    CvUtil.pyPrint(
        "%s was finished by Player %d Civilization %s"
        % (
            PyInfo.UnitInfo(unit.getUnitType()).getDescription(),
            player.getID(),
            player.getCivilizationName(),
        )
    )


@handler("unitKilled")
def onUnitKilled(unit, iAttacker):
    player = PyPlayer(unit.getOwner())
    attacker = PyPlayer(iAttacker)
    if not events._LOG_UNITKILLED:
        return
    CvUtil.pyPrint(
        "Player %d Civilization %s Unit %s was killed by Player %d"
        % (
            player.getID(),
            player.getCivilizationName(),
            PyInfo.UnitInfo(unit.getUnitType()).getDescription(),
            attacker.getID(),
        )
    )


@handler("unitLost")
def onUnitLost(unit):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return

    player = PyPlayer(unit.getOwner())
    if not events._LOG_UNITLOST:
        return
    CvUtil.pyPrint(
        "%s was lost by Player %d Civilization %s"
        % (
            PyInfo.UnitInfo(unit.getUnitType()).getDescription(),
            player.getID(),
            player.getCivilizationName(),
        )
    )


@handler("unitPromoted")
def onUnitPromoted(unit, promotion):
    player = PyPlayer(unit.getOwner())
    if not events._LOG_UNITPROMOTED:
        return
    CvUtil.pyPrint(
        "Unit Promotion Event: %s - %s" % (player.getCivilizationName(), unit.getName())
    )


@handler("unitSelected")
def onUnitSelected(unit):
    player = PyPlayer(unit.getOwner())
    if not events._LOG_UNITSELECTED:
        return
    CvUtil.pyPrint(
        "%s was selected by Player %d Civilization %s"
        % (
            PyInfo.UnitInfo(unit.getUnitType()).getDescription(),
            player.getID(),
            player.getCivilizationName(),
        )
    )


@handler("UnitRename")
def onUnitRename(pUnit):
    if pUnit.getOwner() == gc.getGame().getActivePlayer():
        __eventEditUnitNameBegin(pUnit)


@handler("unitPillage")
def onUnitPillage(pUnit, iImprovement, iRoute, iOwner):
    iPlotX = pUnit.getX()
    iPlotY = pUnit.getY()

    if not events._LOG_UNITPILLAGE:
        return
    CvUtil.pyPrint(
        "Player %d's %s pillaged improvement %d and route %d at plot at (%d, %d)"
        % (
            iOwner,
            PyInfo.UnitInfo(pUnit.getUnitType()).getDescription(),
            iImprovement,
            iRoute,
            iPlotX,
            iPlotY,
        )
    )


@handler("goodyReceived")
def onGoodyReceived(iPlayer):
    if not events._LOG_GOODYRECEIVED:
        return
    CvUtil.pyPrint(
        "%s received a goody" % (gc.getPlayer(iPlayer).getCivilizationDescription(0)),
    )


@handler("greatPersonBorn")
def onGreatPersonBorn(pUnit, iPlayer, pCity):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    if pUnit.isNone() or pCity.isNone():
        return
    if not events._LOG_GREATPERSON:
        return
    CvUtil.pyPrint(
        "A %s was born for %s in %s"
        % (pUnit.getName(), player.getCivilizationName(), pCity.getName())
    )


@handler("techAcquired")
def onTechAcquired(iTechType, iTeam, iPlayer, bAnnounce):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    # Note that iPlayer may be NULL (-1) and not a refer to a player object
    # Show tech splash when applicable
    if iPlayer > -1 and bAnnounce and not CyInterface().noTechSplash():
        if gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode():
            if (not gc.getGame().isNetworkMultiPlayer()) and (
                iPlayer == gc.getGame().getActivePlayer()
            ):
                popupInfo = CyPopupInfo()
                popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
                popupInfo.setData1(iTechType)
                popupInfo.setText(u"showTechSplash")
                popupInfo.addPopup(iPlayer)

    if not events._LOG_TECH:
        return
    CvUtil.pyPrint(
        "%s was finished by Team %d" % (PyInfo.TechnologyInfo(iTechType).getDescription(), iTeam)
    )


@handler("techSelected")
def onTechSelected(iTechType, iPlayer):
    if not events._LOG_TECH:
        return
    CvUtil.pyPrint(
        "%s was selected by Player %d"
        % (PyInfo.TechnologyInfo(iTechType).getDescription(), iPlayer)
    )


@handler("religionFounded")
def onReligionFounded(iReligion, iFounder):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    player = PyPlayer(iFounder)

    iCityId = gc.getGame().getHolyCity(iReligion).getID()
    if gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode():
        if (not gc.getGame().isNetworkMultiPlayer()) and (
            iFounder == gc.getGame().getActivePlayer()
        ):
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
            popupInfo.setData1(iReligion)
            popupInfo.setData2(iCityId)
            popupInfo.setData3(1)
            popupInfo.setText(u"showWonderMovie")
            popupInfo.addPopup(iFounder)

    if not events._LOG_RELIGION:
        return
    CvUtil.pyPrint(
        "Player %d Civilization %s has founded %s"
        % (
            iFounder,
            player.getCivilizationName(),
            gc.getReligionInfo(iReligion).getDescription(),
        )
    )


@handler("religionSpread")
def onReligionSpread(iReligion, iOwner, pSpreadCity):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    player = PyPlayer(iOwner)
    if not events._LOG_RELIGIONSPREAD:
        return
    CvUtil.pyPrint(
        "%s has spread to Player %d Civilization %s city of %s"
        % (
            gc.getReligionInfo(iReligion).getDescription(),
            iOwner,
            player.getCivilizationName(),
            pSpreadCity.getName(),
        )
    )


@handler("religionRemove")
def onReligionRemove(iReligion, iOwner, pRemoveCity):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    player = PyPlayer(iOwner)
    if not events._LOG_RELIGIONSPREAD:
        return
    CvUtil.pyPrint(
        "%s has been removed from Player %d Civilization %s city of %s"
        % (
            gc.getReligionInfo(iReligion).getDescription(),
            iOwner,
            player.getCivilizationName(),
            pRemoveCity.getName(),
        )
    )


@handler("corporationFounded")
def onCorporationFounded(iCorporation, iFounder):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    player = PyPlayer(iFounder)
    if not events._LOG_RELIGION:
        return
    CvUtil.pyPrint(
        "Player %d Civilization %s has founded %s"
        % (
            iFounder,
            player.getCivilizationName(),
            gc.getCorporationInfo(iCorporation).getDescription(),
        )
    )


@handler("corporationSpread")
def onCorporationSpread(iCorporation, iOwner, pSpreadCity):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    player = PyPlayer(iOwner)
    if not events._LOG_RELIGIONSPREAD:
        return
    CvUtil.pyPrint(
        "%s has spread to Player %d Civilization %s city of %s"
        % (
            gc.getCorporationInfo(iCorporation).getDescription(),
            iOwner,
            player.getCivilizationName(),
            pSpreadCity.getName(),
        )
    )


@handler("corporationRemove")
def onCorporationRemove(iCorporation, iOwner, pRemoveCity):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    player = PyPlayer(iOwner)
    if not events._LOG_RELIGIONSPREAD:
        return
    CvUtil.pyPrint(
        "%s has been removed from Player %d Civilization %s city of %s"
        % (
            gc.getReligionInfo(iReligion).getDescription(),  # type: ignore
            iOwner,
            player.getCivilizationName(),
            pRemoveCity.getName(),
        )
    )


@handler("goldenAge")
def onGoldenAge(iPlayer):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    player = PyPlayer(iPlayer)
    if not events._LOG_GOLDENAGE:
        return
    CvUtil.pyPrint(
        "Player %d Civilization %s has begun a golden age"
        % (iPlayer, player.getCivilizationName())
    )


@handler("endGoldenAge")
def onEndGoldenAge(iPlayer):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    player = PyPlayer(iPlayer)
    if not events._LOG_ENDGOLDENAGE:
        return
    CvUtil.pyPrint(
        "Player %d Civilization %s golden age has ended" % (iPlayer, player.getCivilizationName())
    )


@handler("changeWar")
def onChangeWar(bIsWar, iTeam, iRivalTeam):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    if not events._LOG_WARPEACE:
        return
    if bIsWar:
        strStatus = "declared war"
    else:
        strStatus = "declared peace"
    CvUtil.pyPrint("Team %d has %s on Team %d" % (iTeam, strStatus, iRivalTeam))


@handler("cityBuilt")
def onCityBuilt(city):
    # Absinthe: city naming popup on city foundation - settable in GlobalDefines_Alt.xml
    iPlayer = city.getOwner()
    bCityNamePopup = gc.getDefineINT("CITY_NAME_POPUP") == 1
    if bCityNamePopup:
        if iPlayer == gc.getGame().getActivePlayer():
            __eventEditCityNameBegin(city, False)
    CvUtil.pyPrint("City Built Event: %s" % (city.getName()))


@handler("cityRazed")
def onCityRazed(city, iPlayer):
    # Rhye - start bugfix
    owner = PyPlayer(city.getOwner())
    if city.getOwner() == iPlayer:
        if city.getPreviousOwner() != -1:
            owner = PyPlayer(city.getPreviousOwner())
    # Rhye - end bugfix

    CvUtil.pyPrint("City Razed Event: %s" % (city.getName(),))
    razor = PyPlayer(iPlayer)
    CvUtil.pyPrint(
        "Player %d Civilization %s City %s was razed by Player %d Civilization %s"
        % (
            owner.getID(),
            owner.getCivilizationName(),
            city.getName(),
            razor.getID(),
            razor.getCivilizationName(),
        )
    )

    # TODO see RFC DOC partisans

    # Absinthe: Partisans! - not used currently
    # if city.getPopulation > 1 and iOwner != -1 and iPlayer != -1:
    #     owner = gc.getPlayer(iOwner)
    #     if not owner.isBarbarian() and owner.getNumCities() > 0:
    #         if gc.getTeam(owner.getTeam()).isAtWar(gc.getPlayer(iPlayer).getTeam()):
    #             if gc.getNumEventTriggerInfos() > 0: # prevents mods that don't have events from getting an error
    #                 iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_PARTISANS')
    #                 if iEvent != -1 and gc.getGame().isEventActive(iEvent) and owner.getEventTriggerWeight(iEvent) < 0:
    #                     triggerData = owner.initTriggeredData(iEvent, True, -1, city.getX(), city.getY(), iPlayer, city.getID(), -1, -1, -1, -1)
    # Absinthe: end


@handler("cityAcquired")
def onCityAcquired(iPreviousOwner, iNewOwner, pCity, bConquest, bTrade):
    if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython:
        return
    CvUtil.pyPrint("City Acquired Event: %s" % (pCity.getName()))


@handler("cityAcquiredAndKept")
def onCityAcquiredAndKept(iPlayer, pCity):
    CvUtil.pyPrint("City Acquired and Kept Event: %s" % (pCity.getName()))
    CvUtil.pyPrint(
        "NewOwner: %s, PreviousOwner: %s"
        % (
            PyPlayer(pCity.getOwner()).getCivilizationName(),
            PyPlayer(pCity.getPreviousOwner()).getCivilizationName(),
        )
    )


@handler("cityLost")
def onCityLost(city):
    player = PyPlayer(city.getOwner())
    if not events._LOG_CITYLOST:
        return
    CvUtil.pyPrint(
        "City %s was lost by Player %d Civilization %s"
        % (city.getName(), player.getID(), player.getCivilizationName())
    )


@handler("cityDoTurn")
def onCityDoTurn(pCity, iPlayer):
    CvAdvisorUtils.cityAdvise(pCity, iPlayer)


@handler("cityBuildingUnit")
def onCityBuildingUnit(pCity, iUnitType):
    if not events._LOG_CITYBUILDING:
        return
    CvUtil.pyPrint(
        "%s has begun building a %s"
        % (pCity.getName(), gc.getUnitInfo(iUnitType).getDescription())
    )


@handler("cityBuildingBuilding")
def onCityBuildingBuilding(pCity, iBuildingType):
    if not events._LOG_CITYBUILDING:
        return
    CvUtil.pyPrint(
        "%s has begun building a %s"
        % (pCity.getName(), gc.getBuildingInfo(iBuildingType).getDescription())
    )


@handler("cityRename")
def onCityRename(pCity):
    if pCity.getOwner() == gc.getGame().getActivePlayer():
        __eventEditCityNameBegin(pCity, True)


@handler("victory")
def onVictory(iTeam, iVictory):
    if iVictory >= 0 and iVictory < gc.getNumVictoryInfos():
        victoryInfo = gc.getVictoryInfo(int(iVictory))
        CvUtil.pyPrint(
            "Victory! Team %d achieves a %s victory" % (iTeam, victoryInfo.getDescription())
        )


@handler("vassalState")
def onVassalState(iMaster, iVassal, bVassal):
    if bVassal:
        CvUtil.pyPrint("Team %d becomes a Vassal State of Team %d" % (iVassal, iMaster))
    else:
        CvUtil.pyPrint(
            "Team %d revolts and is no longer a Vassal State of Team %d" % (iVassal, iMaster)
        )


#################### TRIGGERED EVENTS ##################


def __eventEditCityNameBegin(city, bRename):
    popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
    popup.setUserData((city.getID(), bRename))
    popup.setHeaderString(text("TXT_KEY_NAME_CITY"))
    popup.setBodyString(text("TXT_KEY_SETTLE_NEW_CITY_NAME"))
    # Absinthe: if not a rename, it should offer the CNM__eventEditCityBegin name as the default name
    if bRename:
        popup.createEditBox(city.getName())
    else:
        szName = get_data_from_upside_down_map(CITIES_MAP, city.getOwner(), city)
        if szName == "-1":
            popup.createEditBox(city.getName())
        else:
            szName = unicode(szName)
            popup.createEditBox(szName)
    # Absinthe: end
    popup.setEditBoxMaxCharCount(15)
    popup.launch()


def __eventEditCityNameApply(playerID, userData, popupReturn):
    "Edit City Name Event"
    iCityID = userData[0]
    bRename = userData[1]
    player = gc.getPlayer(playerID)
    city = player.getCity(iCityID)
    cityName = popupReturn.getEditBoxString(0)
    if len(cityName) > 30:
        cityName = cityName[:30]
    city.setName(cityName, not bRename)


def __eventEditCityBegin(argsList):
    "Edit City Event"
    px, py = argsList
    CvWBPopups.CvWBPopups().initEditCity(argsList)


def __eventEditCityApply(playerID, userData, popupReturn):
    "Edit City Event Apply"
    if getChtLvl() > 0:
        CvWBPopups.CvWBPopups().applyEditCity((popupReturn, userData))


def __eventPlaceObjectBegin(argsList):
    "Place Object Event"
    CvDebugTools.CvDebugTools().initUnitPicker(argsList)


def __eventPlaceObjectApply(playerID, userData, popupReturn):
    "Place Object Event Apply"
    if getChtLvl() > 0:
        CvDebugTools.CvDebugTools().applyUnitPicker((popupReturn, userData))


def __eventAwardTechsAndGoldBegin(argsList):
    "Award Techs & Gold Event"
    CvDebugTools.CvDebugTools().cheatTechs()


def __eventAwardTechsAndGoldApply(playerID, netUserData, popupReturn):
    "Award Techs & Gold Event Apply"
    if getChtLvl() > 0:
        CvDebugTools.CvDebugTools().applyTechCheat((popupReturn))


def __eventShowWonderBegin(argsList):
    "Show Wonder Event"
    CvDebugTools.CvDebugTools().wonderMovie()


def __eventShowWonderApply(playerID, netUserData, popupReturn):
    "Wonder Movie Apply"
    if getChtLvl() > 0:
        CvDebugTools.CvDebugTools().applyWonderMovie((popupReturn))


## Platy Builder ##
def __eventEditUnitNameBegin(argsList):
    pUnit = argsList
    popup = PyPopup.PyPopup(CvUtil.EventEditUnitName, EventContextTypes.EVENTCONTEXT_ALL)
    popup.setUserData((pUnit.getID(), CyGame().getActivePlayer()))
    popup.setBodyString(text("TXT_KEY_RENAME_UNIT"))
    popup.createEditBox(pUnit.getNameNoDesc())
    popup.setEditBoxMaxCharCount(25)
    popup.launch()


def __eventEditUnitNameApply(playerID, userData, popupReturn):
    unit = gc.getPlayer(userData[1]).getUnit(userData[0])
    newName = popupReturn.getEditBoxString(0)
    unit.setName(newName)
    if CyGame().GetWorldBuilderMode():
        WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeStats()
        WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeCurrentUnit()


def __eventEditCityNameBegin(city, bRename):
    popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
    popup.setUserData((city.getID(), bRename, CyGame().getActivePlayer()))
    popup.setHeaderString(text("TXT_KEY_NAME_CITY"))
    popup.setBodyString(text("TXT_KEY_SETTLE_NEW_CITY_NAME"))
    # Absinthe: if not a rename, it should offer the CNM__eventEditCityBegin name as the default name
    if bRename:
        popup.createEditBox(city.getName())
    else:
        szName = get_data_from_upside_down_map(CITIES_MAP, city.getOwner(), city)
        if szName == "-1":
            popup.createEditBox(city.getName())
        else:
            szName = unicode(szName)
            popup.createEditBox(szName)
    # Absinthe: end
    popup.setEditBoxMaxCharCount(15)
    popup.launch()


def __eventEditCityNameApply(playerID, userData, popupReturn):
    city = gc.getPlayer(userData[2]).getCity(userData[0])
    cityName = popupReturn.getEditBoxString(0)
    city.setName(cityName, not userData[1])
    if CyGame().GetWorldBuilderMode() and not CyGame().isInAdvancedStart():
        WBCityEditScreen.WBCityEditScreen().placeStats()


def __eventWBUnitScriptPopupApply(playerID, userData, popupReturn):
    sScript = popupReturn.getEditBoxString(0)
    pUnit = gc.getPlayer(userData[0]).getUnit(userData[1])
    pUnit.setScriptData(CvUtil.convertToStr(sScript))
    WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
    return


def __eventWBPlayerScriptPopupApply(playerID, userData, popupReturn):
    sScript = popupReturn.getEditBoxString(0)
    gc.getPlayer(userData[0]).setScriptData(CvUtil.convertToStr(sScript))
    WBPlayerScreen.WBPlayerScreen().placeScript()
    return


def __eventWBCityScriptPopupApply(playerID, userData, popupReturn):
    sScript = popupReturn.getEditBoxString(0)
    pCity = gc.getPlayer(userData[0]).getCity(userData[1])
    pCity.setScriptData(CvUtil.convertToStr(sScript))
    WBCityEditScreen.WBCityEditScreen().placeScript()
    return


def __eventWBScriptPopupBegin():
    return


def __eventWBGameScriptPopupApply(playerID, userData, popupReturn):
    sScript = popupReturn.getEditBoxString(0)
    CyGame().setScriptData(CvUtil.convertToStr(sScript))
    WBGameDataScreen.WBGameDataScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
    return


def __eventWBPlotScriptPopupApply(playerID, userData, popupReturn):
    sScript = popupReturn.getEditBoxString(0)
    pPlot = CyMap().plot(userData[0], userData[1])
    pPlot.setScriptData(CvUtil.convertToStr(sScript))
    WBPlotScreen.WBPlotScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
    return


# def __eventWBStoredDataValuePopupApply(playerID, userData, popupReturn):
#     sScript = popupReturn.getEditBoxString(0)
#     try:
#         int(sScript)
#         bInt = True
#     except ValueError:
#         bInt = False
#     if bInt:
#         iValue = int(sScript)
#         WBStoredDataScreen.WBStoredDataScreen(
#             CvPlatyBuilderScreen.CvWorldBuilderScreen()
#         ).changeListTableValue(userData[0], iValue)
#     return


def __eventWBLandmarkPopupApply(playerID, userData, popupReturn):
    sScript = popupReturn.getEditBoxString(0)
    pPlot = CyMap().plot(userData[0], userData[1])
    iPlayer = userData[2]
    if userData[3] > -1:
        pSign = CyEngine().getSignByIndex(userData[3])
        iPlayer = pSign.getPlayerType()
        CyEngine().removeSign(pPlot, iPlayer)
    if len(sScript):
        if iPlayer == gc.getBARBARIAN_PLAYER():
            CyEngine().addLandmark(pPlot, CvUtil.convertToStr(sScript))
        else:
            CyEngine().addSign(pPlot, iPlayer, CvUtil.convertToStr(sScript))
    WBPlotScreen.iCounter = 10
    return


### REGISTER POPUP HANDLERS ###
events.setPopupHandlers(
    CvUtil.EventEditCityName, "EditCityName", __eventEditCityNameBegin, __eventEditCityNameApply
)
events.setPopupHandlers(
    CvUtil.EventPlaceObject, "PlaceObject", __eventPlaceObjectBegin, __eventPlaceObjectApply
)
events.setPopupHandlers(
    CvUtil.EventAwardTechsAndGold,
    "AwardTechsAndGold",
    __eventAwardTechsAndGoldBegin,
    __eventAwardTechsAndGoldApply,
)
events.setPopupHandlers(
    CvUtil.EventEditUnitName, "EditUnitName", __eventEditUnitNameBegin, __eventEditUnitNameApply
)

## Platy Builder ##
events.setPopupHandlers(
    CvUtil.EventWBLandmarkPopup,
    "WBLandmarkPopup",
    __eventWBScriptPopupBegin,
    __eventWBLandmarkPopupApply,
)
events.setPopupHandlers(
    CvUtil.EventShowWonder, "ShowWonder", __eventShowWonderBegin, __eventShowWonderApply
)
events.setPopupHandlers(
    1111, "WBPlayerScript", __eventWBScriptPopupBegin, __eventWBPlayerScriptPopupApply
)
events.setPopupHandlers(
    2222, "WBCityScript", __eventWBScriptPopupBegin, __eventWBCityScriptPopupApply
)
events.setPopupHandlers(
    3333, "WBUnitScript", __eventWBScriptPopupBegin, __eventWBUnitScriptPopupApply
)
events.setPopupHandlers(
    4444, "WBGameScript", __eventWBScriptPopupBegin, __eventWBGameScriptPopupApply
)
events.setPopupHandlers(
    5555, "WBPlotScript", __eventWBScriptPopupBegin, __eventWBPlotScriptPopupApply
)
# events.setPopupHandlers(
#     7777, "WBStoredDataValue", __eventWBScriptPopupBegin, __eventWBStoredDataValuePopupApply
# ),
## Platy Builder ##
