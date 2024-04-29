## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
from CoreFunctions import text
import CvUtil
import CvScreenEnums
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()


class CvPediaCorporation:
    "Civilopedia Screen for Corporations"

    def __init__(self, main):
        self.iCorporation = -1
        self.top = main

        self.X_MAIN_PANE = self.top.X_PEDIA_PAGE + 20
        self.Y_MAIN_PANE = 55
        self.W_MAIN_PANE = 250
        self.H_MAIN_PANE = 260

        self.W_ICON = 150
        self.H_ICON = 150
        self.X_ICON = self.X_MAIN_PANE + (self.W_MAIN_PANE - self.W_ICON) / 2
        self.Y_ICON = self.Y_MAIN_PANE + (self.H_MAIN_PANE - self.H_ICON) / 2
        self.ICON_SIZE = 64

        self.X_ENABLES = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
        self.Y_ENABLES = 55
        self.W_ENABLES = 1024 - (self.X_ENABLES) - 24
        self.H_ENABLES = 110

        self.X_SPECIAL = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
        self.Y_SPECIAL = self.Y_ENABLES + self.H_ENABLES
        self.W_SPECIAL = 1024 - (self.X_MAIN_PANE + self.W_MAIN_PANE + 10) - 24
        self.H_SPECIAL = self.Y_MAIN_PANE + self.H_MAIN_PANE - self.Y_SPECIAL

        self.X_TEXT = self.X_MAIN_PANE
        self.Y_TEXT = self.Y_MAIN_PANE + self.H_MAIN_PANE + 20
        self.W_TEXT = 1024 - (self.X_MAIN_PANE) - 24
        self.H_TEXT = 705 - self.Y_TEXT

    # Screen construction function
    def interfaceScreen(self, iCorporation):

        self.iCorporation = iCorporation

        self.top.deleteAllWidgets()

        screen = self.top.getScreen()

        bNotActive = not screen.isActive()
        if bNotActive:
            self.top.setPediaCommonWidgets()
            self.placeLinks()

        # Header...
        szHeader = (
            u"<font=4b>"
            + gc.getCorporationInfo(self.iCorporation).getDescription().upper()
            + u"</font>"
        )
        szHeaderId = self.top.getNextWidgetName()
        screen.setLabel(
            szHeaderId,
            "Background",
            szHeader,
            CvUtil.FONT_CENTER_JUSTIFY,
            self.top.X_SCREEN,
            self.top.Y_TITLE,
            0,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        # Top
        screen.setText(
            self.top.getNextWidgetName(),
            "Background",
            self.top.MENU_TEXT,
            CvUtil.FONT_LEFT_JUSTIFY,
            self.top.X_MENU,
            self.top.Y_MENU,
            0,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_PEDIA_MAIN,
            CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION,
            -1,
        )

        if self.top.iLastScreen != CvScreenEnums.PEDIA_CORPORATION or bNotActive:
            if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
                self.placeLinks()
            self.top.iLastScreen = CvScreenEnums.PEDIA_CORPORATION

        # Icon
        screen.addPanel(
            self.top.getNextWidgetName(),
            "",
            "",
            False,
            False,
            self.X_MAIN_PANE,
            self.Y_MAIN_PANE,
            self.W_MAIN_PANE,
            self.H_MAIN_PANE,
            PanelStyles.PANEL_STYLE_BLUE50,
        )
        screen.addPanel(
            self.top.getNextWidgetName(),
            "",
            "",
            False,
            False,
            self.X_ICON,
            self.Y_ICON,
            self.W_ICON,
            self.H_ICON,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.addDDSGFC(
            self.top.getNextWidgetName(),
            gc.getCorporationInfo(self.iCorporation).getButton(),
            self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2,
            self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2,
            self.ICON_SIZE,
            self.ICON_SIZE,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        self.placeSpecial()
        self.placeEnables()
        self.placeText()

    def placeEnables(self):

        screen = self.top.getScreen()

        panelName = self.top.getNextWidgetName()
        screen.addPanel(
            panelName,
            text("TXT_KEY_PEDIA_BONUS_TRADE"),
            "",
            False,
            True,
            self.X_ENABLES,
            self.Y_ENABLES,
            self.W_ENABLES,
            self.H_ENABLES,
            PanelStyles.PANEL_STYLE_BLUE50,
        )
        screen.attachLabel(panelName, "", "  ")

        for iBuilding in range(gc.getNumBuildingInfos()):
            if gc.getBuildingInfo(iBuilding).getPrereqCorporation() == self.iCorporation:
                screen.attachImageButton(
                    panelName,
                    "",
                    gc.getBuildingInfo(iBuilding).getButton(),
                    GenericButtonSizes.BUTTON_SIZE_CUSTOM,
                    WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING,
                    iBuilding,
                    1,
                    False,
                )

        for iUnit in range(gc.getNumUnitInfos()):
            if gc.getUnitInfo(iUnit).getPrereqCorporation() == self.iCorporation:
                screen.attachImageButton(
                    panelName,
                    "",
                    gc.getUnitInfo(iUnit).getButton(),
                    GenericButtonSizes.BUTTON_SIZE_CUSTOM,
                    WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT,
                    iUnit,
                    1,
                    False,
                )

    def placeSpecial(self):

        screen = self.top.getScreen()

        panelName = self.top.getNextWidgetName()
        screen.addPanel(
            panelName,
            text("TXT_KEY_PEDIA_EFFECTS"),
            "",
            True,
            False,
            self.X_SPECIAL,
            self.Y_SPECIAL,
            self.W_SPECIAL,
            self.H_SPECIAL,
            PanelStyles.PANEL_STYLE_BLUE50,
        )

        listName = self.top.getNextWidgetName()
        screen.attachListBoxGFC(panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY)
        screen.enableSelect(listName, False)

        szSpecialText = CyGameTextMgr().parseCorporationInfo(self.iCorporation, True)[1:]
        splitText = string.split(szSpecialText, "\n")
        for special in splitText:
            if len(special) != 0:
                screen.appendListBoxString(
                    listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY
                )

    def placeText(self):

        screen = self.top.getScreen()

        panelName = self.top.getNextWidgetName()
        screen.addPanel(
            panelName,
            "",
            "",
            True,
            True,
            self.X_TEXT,
            self.Y_TEXT,
            self.W_TEXT,
            self.H_TEXT,
            PanelStyles.PANEL_STYLE_BLUE50,
        )

        szText = gc.getCorporationInfo(self.iCorporation).getCivilopedia()
        screen.attachMultilineText(
            panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY
        )

    def placeLinks(self):

        self.top.placeLinks()
        self.top.placeCorporations()

    # Will handle the input for this screen...
    def handleInput(self, inputClass):
        return 0
