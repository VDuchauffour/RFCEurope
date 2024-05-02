## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

import math
from CoreData import civilization
from CoreFunctions import text
from CoreStructures import turn
import CvUtil
from CvPythonExtensions import *
import RFCUtils

from Scenario import get_scenario_start_turn

ArtFileMgr = CyArtFileMgr()
gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()


class CvDawnOfMan:
    "Dawn of man screen"

    def __init__(self, iScreenID):
        self.iScreenID = iScreenID

        self.X_SCREEN = 0
        self.Y_SCREEN = 0
        self.W_SCREEN = 1024
        self.H_SCREEN = 768

        self.X_MAIN_PANEL = 238  # position of the main panel's top-left corner: pixels from left side of the screen
        self.Y_MAIN_PANEL = 180  # pixels from top of the screen
        self.W_MAIN_PANEL = 556  # number of pixels wide
        self.H_MAIN_PANEL = 355  # number of pixels height

        self.iMarginSpace = 15

        self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
        self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + 10  # self.iMarginSpace
        self.W_HEADER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
        self.H_HEADER_PANEL = self.H_MAIN_PANEL - 146  # int(self.H_MAIN_PANEL * (2.0 / 5.0))

        self.X_LEADER_ICON = self.X_HEADER_PANEL + self.iMarginSpace
        self.Y_LEADER_ICON = self.Y_HEADER_PANEL + self.iMarginSpace
        self.H_LEADER_ICON = self.H_HEADER_PANEL - (15 * 2)  # 140
        self.W_LEADER_ICON = int(self.H_LEADER_ICON / 1.272727)  # 110

        self.X_LEADER_TITLE_TEXT = (
            505  # iXHeaderPanelRemainingAfterLeader + (iWHeaderPanelRemainingAfterLeader / 2)
        )
        self.Y_LEADER_TITLE_TEXT = self.Y_HEADER_PANEL + self.iMarginSpace + 6
        self.W_LEADER_TITLE_TEXT = self.W_HEADER_PANEL / 3 + 10
        self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 2

        self.X_FANCY_ICON1 = self.X_HEADER_PANEL + 170
        self.X_FANCY_ICON2 = self.X_HEADER_PANEL + 430
        self.Y_FANCY_ICON = self.Y_LEADER_TITLE_TEXT - 6
        self.WH_FANCY_ICON = 64

        self.X_STATS_TEXT = (
            self.X_FANCY_ICON1
        )  # + self.W_LEADER_ICON + (self.iMarginSpace * 2) + 5
        self.Y_STATS_TEXT = self.Y_LEADER_TITLE_TEXT + 75
        self.W_STATS_TEXT = int(self.W_HEADER_PANEL * (5.25 / 7.0))
        self.H_STATS_TEXT = int(self.H_HEADER_PANEL * (2.25 / 5.0))

        self.X_TEXT_PANEL = self.X_HEADER_PANEL
        self.Y_TEXT_PANEL = (
            self.Y_HEADER_PANEL + self.iMarginSpace
        )  # 10 is the fudge factor  #self.Y_HEADER_PANEL + self.H_HEADER_PANEL + self.iMarginSpace - 10		self.W_TEXT_PANEL = self.W_HEADER_PANEL
        self.W_TEXT_PANEL = self.W_HEADER_PANEL
        self.H_TEXT_PANEL = (
            self.H_MAIN_PANEL - 32
        )  # (self.iMarginSpace * 3) + 10 #10 is the fudge factor
        self.iTEXT_PANEL_MARGIN = 40  # from the top of the header panel

        self.X_EXIT = 456  # self.X_MAIN_PANEL + self.W_MAIN_PANEL/2 - self.W_EXIT/2
        self.Y_EXIT = self.Y_MAIN_PANEL + 307  # const = main panel height - 48
        self.W_EXIT = 120
        self.H_EXIT = 30

    def interfaceScreen(self):
        "Use a popup to display the opening text"
        if CyGame().isPitbossHost():
            return

        self.player = gc.getPlayer(gc.getGame().getActivePlayer())
        self.EXIT_TEXT = text("TXT_KEY_SCREEN_CONTINUE")

        # Create screen

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

        # Create panels

        # Main
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
        # Bottom
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

        ##Rhye - begin
        pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())

        bodyString = utils.getDawnOfManText(CyGame().getActiveTeam())

        # Progress bar position (top left corner, width, height) #X coordinate: self.X_MAIN_PANEL + self.W_MAIN_PANEL/2 - Progress bar width/2
        screen.addStackedBarGFC(
            "ProgressBar",
            271,
            425,
            490,
            35,
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

        ##Rhye - end
        screen.addMultilineText(
            "BodyText",
            bodyString,
            self.X_TEXT_PANEL + self.iMarginSpace,
            self.Y_TEXT_PANEL + self.iMarginSpace + self.iTEXT_PANEL_MARGIN,
            self.W_TEXT_PANEL - (self.iMarginSpace * 2),
            self.H_TEXT_PANEL - (self.iMarginSpace * 2) - 139,
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
        screen.hide("Exit")  # Rhye

        pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
        pLeaderHeadInfo = gc.getLeaderHeadInfo(pActivePlayer.getLeaderType())
        screen.setSoundId(
            CyAudioGame().Play2DSoundWithId(pLeaderHeadInfo.getDiploPeaceMusicScriptIds(0))
        )

    def handleInput(self, inputClass):
        return 0

    def update(self, fDelta):

        ##Rhye - begin
        if civilization(CyGame().getActiveTeam()).date.birth <= get_scenario_start_turn():
            screen = CyGInterfaceScreen("CvLoadingScreen", self.iScreenID)
            screen.setBarPercentage("ProgressBar", InfoBarTypes.INFOBAR_STORED, 1)
            screen.setLabel(
                "Text",
                "",
                text("TXT_KEY_AUTOPLAY_TURNS_REMAINING", 0),
                CvUtil.FONT_CENTER_JUSTIFY,
                516,
                465,
                0,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )
            screen.show("Exit")  # Rhye
        else:
            iGameTurn = turn()

            iNumAutoPlayTurns = civilization(CyGame().getActiveTeam()).date.birth
            iNumTurnsRemaining = iNumAutoPlayTurns - iGameTurn

            screen = CyGInterfaceScreen("CvLoadingScreen", self.iScreenID)

            exponent = 1 + iNumAutoPlayTurns / 190
            # Absinthe: for all scenarios:
            screen.setBarPercentage(
                "ProgressBar",
                InfoBarTypes.INFOBAR_STORED,
                float(math.pow(iGameTurn - get_scenario_start_turn(), exponent))
                / float(math.pow(iNumAutoPlayTurns - get_scenario_start_turn(), exponent)),
            )
            screen.setLabel(
                "Text",
                "",
                text("TXT_KEY_AUTOPLAY_TURNS_REMAINING", iNumTurnsRemaining),
                CvUtil.FONT_CENTER_JUSTIFY,
                514,
                465,
                0,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )
            if iNumTurnsRemaining <= 0:  # Rhye
                screen.show("Exit")  # Rhye

        return

    ##Rhye - end

    def onClose(self):
        # Absinthe: do not play the initial RFC song on start - might even lead to sound selection issues
        CyInterface().setSoundSelectionReady(True)
        return 0
