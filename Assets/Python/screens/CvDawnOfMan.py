## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

import math
from Core import civilization, human, text, get_scenario_start_turn, turns, game
import CvUtil
from CvPythonExtensions import *

from RFCUtils import getDawnOfManText

## HOF MOD
import Buffy  # noqa: F401
import BugCore
import GameSetUpCheck  # noqa: F401

BUFFYOpt = BugCore.game.BUFFY
## end HOF MOD


ArtFileMgr = CyArtFileMgr()
gc = CyGlobalContext()


class CvDawnOfMan:
    "Dawn of man screen"

    def __init__(self, iScreenID):
        self.iScreenID = iScreenID

        self.iLastTurn = -1

        self.X_SCREEN = 0
        self.Y_SCREEN = 0
        self.W_SCREEN = 1024
        self.H_SCREEN = 768

        self.X_MAIN_PANEL = 250
        self.Y_MAIN_PANEL = 190
        self.W_MAIN_PANEL = 550
        self.H_MAIN_PANEL = 350

        self.iMarginSpace = 15

        self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
        self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
        self.W_HEADER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
        self.H_HEADER_PANEL = int(self.H_MAIN_PANEL * (2.0 / 5.0))

        self.X_LEADER_ICON = self.X_HEADER_PANEL + self.iMarginSpace
        self.Y_LEADER_ICON = self.Y_HEADER_PANEL + self.iMarginSpace
        self.H_LEADER_ICON = self.H_HEADER_PANEL - (15 * 2)
        self.W_LEADER_ICON = int(self.H_LEADER_ICON / 1.272727)

        self.X_LEADER_TITLE_TEXT = 505
        self.Y_LEADER_TITLE_TEXT = self.Y_HEADER_PANEL + self.iMarginSpace + 6
        self.W_LEADER_TITLE_TEXT = self.W_HEADER_PANEL / 3 + 10
        self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 2

        self.X_FANCY_ICON1 = self.X_HEADER_PANEL + 170
        self.X_FANCY_ICON2 = self.X_HEADER_PANEL + 430
        self.Y_FANCY_ICON = self.Y_LEADER_TITLE_TEXT - 6
        self.WH_FANCY_ICON = 64

        self.X_STATS_TEXT = self.X_FANCY_ICON1
        self.Y_STATS_TEXT = self.Y_LEADER_TITLE_TEXT + 75
        self.W_STATS_TEXT = int(self.W_HEADER_PANEL * (5.25 / 7.0))
        self.H_STATS_TEXT = int(self.H_HEADER_PANEL * (2.25 / 5.0))

        self.X_TEXT_PANEL = self.X_HEADER_PANEL
        self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + self.iMarginSpace
        self.W_TEXT_PANEL = self.W_HEADER_PANEL
        self.H_TEXT_PANEL = self.H_MAIN_PANEL - (self.iMarginSpace * 3) + 10
        self.iTEXT_PANEL_MARGIN = 35

        self.X_EXIT = 460
        self.Y_EXIT = self.Y_MAIN_PANEL + 290
        self.W_EXIT = 120
        self.H_EXIT = 30

    def interfaceScreen(self):
        "Use a popup to display the opening text"
        if CyGame().isPitbossHost():
            return

        self.player = gc.getPlayer(gc.getGame().getActivePlayer())
        self.EXIT_TEXT = text("TXT_KEY_SCREEN_CONTINUE")

        screen = CyGInterfaceScreen("CvDawnOfMan", self.iScreenID)
        screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
        screen.showWindowBackground(False)
        screen.setDimensions(
            screen.centerX(self.X_SCREEN),
            screen.centerY(self.Y_SCREEN),
            self.W_SCREEN,
            self.H_SCREEN,
        )
        screen.enableWorldSounds(False)

        szMainPanel = "DawnOfManMainPanel"
        screen.addPanel(
            szMainPanel,
            "",
            "",
            True,
            True,
            self.X_MAIN_PANEL,
            self.Y_MAIN_PANEL,
            self.W_MAIN_PANEL,
            self.H_MAIN_PANEL,
            PanelStyles.PANEL_STYLE_MAIN,
        )

        szTextPanel = "DawnOfManTextPanel"
        screen.addPanel(
            szTextPanel,
            "",
            "",
            True,
            True,
            self.X_TEXT_PANEL,
            self.Y_TEXT_PANEL,
            self.W_TEXT_PANEL,
            self.H_TEXT_PANEL,
            PanelStyles.PANEL_STYLE_DAWNBOTTOM,
        )

        # Main Body text
        szDawnTitle = u"<font=3>" + text("TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE").upper() + u"</font>"
        screen.setLabel(
            "DawnTitle",
            "Background",
            szDawnTitle,
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_TEXT_PANEL + (self.W_TEXT_PANEL / 2),
            self.Y_TEXT_PANEL + 15,
            -2.0,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        # Leoreth: imported individual texts from Sword of Islam (edead)
        bodyString = getDawnOfManText(human())

        screen.addStackedBarGFC(
            "ProgressBar",
            300,
            400,
            435,
            40,
            InfoBarTypes.NUM_INFOBAR_TYPES,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.setStackedBarColors(
            "ProgressBar",
            InfoBarTypes.INFOBAR_STORED,
            gc.getInfoTypeForString("COLOR_PLAYER_GREEN"),
        )
        screen.setStackedBarColors(
            "ProgressBar",
            InfoBarTypes.INFOBAR_RATE,
            gc.getInfoTypeForString("COLOR_RESEARCH_RATE"),
        )
        screen.setStackedBarColors(
            "ProgressBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY")
        )
        screen.setStackedBarColors(
            "ProgressBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY")
        )
        self.iTurnsRemaining = -1

        screen.addMultilineText(
            "BodyText",
            bodyString,
            self.X_TEXT_PANEL + self.iMarginSpace,
            self.Y_TEXT_PANEL + self.iMarginSpace + self.iTEXT_PANEL_MARGIN,
            self.W_TEXT_PANEL - (self.iMarginSpace * 2),
            self.H_TEXT_PANEL - (self.iMarginSpace * 2) - 165,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            CvUtil.FONT_LEFT_JUSTIFY,
        )

        screen.setButtonGFC(
            "Exit",
            self.EXIT_TEXT,
            "",
            self.X_EXIT,
            self.Y_EXIT,
            self.W_EXIT,
            self.H_EXIT,
            WidgetTypes.WIDGET_CLOSE_SCREEN,
            -1,
            -1,
            ButtonStyles.BUTTON_STYLE_STANDARD,
        )
        screen.hide("Exit")

        pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
        pLeaderHeadInfo = gc.getLeaderHeadInfo(pActivePlayer.getLeaderType())
        screen.setSoundId(
            CyAudioGame().Play2DSoundWithId(pLeaderHeadInfo.getDiploPeaceMusicScriptIds(0))
        )

    def handleInput(self, inputClass):
        return 0

    def update(self, fDelta):
        iGameTurn = game.getGameTurn()

        if iGameTurn <= self.iLastTurn:
            return

        self.iLastTurn = iGameTurn

        iTotalAutoplay = civilization().date.birth - get_scenario_start_turn()

        iAutoplayRemaining = game.getAIAutoPlay()
        iAutoplayElapsed = iTotalAutoplay - iAutoplayRemaining

        if iAutoplayRemaining > 0:
            exponent = 1 + 1.0 * iTotalAutoplay / turns(190)
            fBarPercentage = float(math.pow(iAutoplayElapsed, exponent)) / float(
                math.pow(iTotalAutoplay, exponent)
            )
        else:
            fBarPercentage = 1.0

        screen = CyGInterfaceScreen("CvLoadingScreen", self.iScreenID)
        screen.setBarPercentage("ProgressBar", InfoBarTypes.INFOBAR_STORED, fBarPercentage)
        screen.setLabel(
            "Text",
            "",
            text("TXT_KEY_AUTOPLAY_TURNS_REMAINING", iAutoplayRemaining),
            CvUtil.FONT_CENTER_JUSTIFY,
            530,
            445,
            0,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        if iAutoplayRemaining <= 0:
            screen.show("Exit")

    def onClose(self):
        CyInterface().setSoundSelectionReady(True)
        return 0
