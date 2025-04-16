from CvPythonExtensions import *
from Core import human, make_unit, player, game, text, turn, year
from CoreTypes import Civ, Unit
import CvMercenaryManager
import CvScreenEnums
from Events import events, handler, popup_handler
from ProvinceMapData import PROVINCES_MAP
from RFCUtils import getProvinceStabilityLevel
import CvUtil
from Slots import add_player, find_slot, slot
from StoredData import data

gc = CyGlobalContext()
lastProvinceID = -1
mercenaryManager = CvMercenaryManager.CvMercenaryManager(CvScreenEnums.MERCENARY_MANAGER)


@handler("kbdEvent")
def display_mercenary_manager_with_key_shortcut(eventType, key, mx, my, px, py):
    key = int(key)
    if player().isAlive():
        if (
            events.bCtrl
            and eventType == events.EventKeyDown
            and key == int(InputTypes.KB_M)
            and gc.getActivePlayer().getNumCities() > 0
        ):
            mercenaryManager.interfaceScreen()


@handler("kbdEvent")
def print_plots_debug(eventType, key, mx, my, px, py):
    key = int(key)
    if events.bAlt and eventType == events.EventKeyDown and key == int(InputTypes.KB_N):
        events.printPlotsDebug()


@handler("kbdEvent")
def province_highlight(eventType, key, mx, my, px, py):
    global lastProvinceID
    key = int(key)
    if (
        events.bCtrl
        and not events.bAlt
        and eventType == events.EventKeyDown
        and px >= 0
        and py >= 0
        and int(key) == 45
    ):

        plot = gc.getMap().plot(px, py)
        iActivePlayer = gc.getGame().getActivePlayer()
        iActiveTeam = gc.getPlayer(iActivePlayer).getTeam()
        iProvinceID = PROVINCES_MAP[plot.getY()][plot.getX()]

        # do not show provinces of unrevealed tiles
        if not plot.isRevealed(iActiveTeam, False) and not gc.getGame().isDebugMode():
            return

        # do not redraw if already drawn
        if lastProvinceID == iProvinceID:
            return

        map = CyMap()
        engine = CyEngine()

        # clear the highlight
        engine.clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)

        # cache the plot's coords
        lastProvinceID = PROVINCES_MAP[plot.getY()][plot.getX()]

        # select an appropriate color
        if PROVINCES_MAP[plot.getY()][plot.getX()] == -1:  # ocean and non-province tiles
            return
        else:
            iLevel = getProvinceStabilityLevel(human(), iProvinceID)
            if iLevel == 4:
                color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_CORE")).getColor()
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

    if eventType == events.EventKeyUp and events.bCtrl or eventType == events.EventKeyDown:
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)
        lastProvinceID = -1


@handler("kbdEvent")
def observerModeShortcut(eventType, key):
    if eventType == events.EventKeyDown and events.bCtrl and key == InputTypes.KB_C:
        popup = CyPopup(4568, EventContextTypes.EVENTCONTEXT_ALL, True)

        popup.setHeaderString(
            text("TXT_KEY_INTERFACE_OBSERVER_MODE_HEADER"), CvUtil.FONT_LEFT_JUSTIFY
        )
        popup.setBodyString(text("TXT_KEY_INTERFACE_OBSERVER_MODE_BODY"), CvUtil.FONT_LEFT_JUSTIFY)
        popup.createEditBox(str(game.getGameTurnYear()), 0)

        popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)


@popup_handler(4568)
def handleStartObserverMode(iPlayer, netUserData, popupReturn):
    iDestinationYear = int(popupReturn.getEditBoxString(0))
    iAutoplayTurns = year(iDestinationYear) - turn()

    if iAutoplayTurns > 0:
        startObserverMode(iAutoplayTurns)


@handler("autoplayEnded")
def observerModeEnds():
    endObserverMode()


def startObserverMode(iTurns):
    data.before_observer_slot = human()
    iObserverCiv = Civ.BURGUNDY
    iObserverSlot = slot(iObserverCiv)

    if iObserverSlot < 0:
        iObserverSlot = find_slot(iObserverCiv)
        add_player(iObserverSlot, iObserverCiv)

    make_unit(iObserverCiv, Unit.CATAPULT, (0, 0))

    game.setActivePlayer(iObserverCiv, False)
    game.setAIAutoPlay(iTurns)


def endObserverMode():
    if data.before_observer_slot != -1:
        if player(data.before_observer_slot).isAlive():
            game.setActivePlayer(data.before_observer_slot, False)
            data.before_observer_slot = -1
        else:
            make_unit(human(), Unit.CATAPULT, (0, 0))
