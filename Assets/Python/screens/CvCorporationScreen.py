## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
from Core import text
import PyHelpers
import CvUtil
import CvScreenEnums

PyPlayer = PyHelpers.PyPlayer

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()


class CvCorporationScreen:
    "Corporation Advisor Screen"

    def __init__(self):

        self.SCREEN_NAME = "CorporationScreen"
        self.BUTTON_NAME = "CorporationScreenButton"
        self.CORPORATION_NAME = "CorporationText"
        self.CITY_NAME = "CorporationCity"
        self.HEADER_NAME = "CorporationScreenHeader"
        self.DEBUG_DROPDOWN_ID = "CorporationDropdownWidget"
        self.AREA1_ID = "CorporationAreaWidget1"
        self.AREA2_ID = "CorporationAreaWidget2"
        self.BACKGROUND_ID = "CorporationBackground"
        self.CORPORATION_PANEL_ID = "CorporationPanel"
        self.EXIT_NAME = "CorporationExitButton"

        self.BORDER_WIDTH = 2
        self.BUTTON_SIZE = 48
        self.HIGHLIGHT_EXTRA_SIZE = 4

        self.X_SCREEN = 500
        self.Y_SCREEN = 396
        self.W_SCREEN = 1024
        self.H_SCREEN = 768
        self.Z_SCREEN = -6.1

        self.Y_TITLE = 8
        self.Z_TEXT = self.Z_SCREEN - 0.2
        self.DZ = -0.2
        self.Z_CONTROLS = self.Z_TEXT

        self.X_EXIT = 994
        self.Y_EXIT = 726

        self.LEFT_EDGE_TEXT = 10
        self.X_CORPORATION_START = 60  # Absinthe (155)
        self.DX_CORPORATION = 102  # Absinthe (116)
        self.Y_CORPORATION = 70  # Absinthe (35)
        self.Y_GREAT_PERSON = 57
        self.Y_BONUSES = 114  # Absinthe (77)
        self.Y_FOUNDED = 112
        self.Y_HEADQUARTERS = 142
        self.Y_CORPORATION_NAME = 58

        self.X_CORPORATION_AREA = 45
        self.Y_CORPORATION_AREA = 84
        self.W_CORPORATION_AREA = 934
        self.H_CORPORATION_AREA = 180

        self.X_CITY1_AREA = 45
        self.X_CITY2_AREA = 522
        self.Y_CITY_AREA = 282
        self.W_CITY_AREA = 457
        self.H_CITY_AREA = 395

        self.X_CITY = 10
        self.DY_CITY = 38

        self.iCorporationExamined = -1
        self.iCorporationSelected = -1
        self.iCorporationOriginal = -1
        self.iActivePlayer = -1

        self.bScreenUp = False

        self.CorporationScreenInputMap = {
            self.CORPORATION_NAME: self.CorporationScreenButton,
            self.EXIT_NAME: self.Exit,
            self.BUTTON_NAME: self.CorporationScreenButton,
        }

    def getScreen(self):
        return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.CORPORATION_SCREEN)

    def interfaceScreen(self):

        self.SCREEN_ART = ArtFileMgr.getInterfaceArtInfo("TECH_BG").getPath()
        self.EXIT_TEXT = u"<font=4>" + text("TXT_KEY_PEDIA_SCREEN_EXIT").upper() + "</font>"

        self.iActivePlayer = gc.getGame().getActivePlayer()

        self.bScreenUp = True

        screen = self.getScreen()
        if screen.isActive():
            return
        screen.setRenderInterfaceOnly(True)
        screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

        # Set the background and exit button, and show the screen
        screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

        screen.addDDSGFC(
            self.BACKGROUND_ID,
            ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(),
            0,
            0,
            self.W_SCREEN,
            self.H_SCREEN,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.addPanel(
            "TechTopPanel",
            u"",
            u"",
            True,
            False,
            0,
            0,
            self.W_SCREEN,
            55,
            PanelStyles.PANEL_STYLE_TOPBAR,
        )
        screen.addPanel(
            "TechBottomPanel",
            u"",
            u"",
            True,
            False,
            0,
            713,
            self.W_SCREEN,
            55,
            PanelStyles.PANEL_STYLE_BOTTOMBAR,
        )

        screen.showWindowBackground(False)

        # Make the scrollable areas for the city list...

        if CyGame().isDebugMode():
            self.szDropdownName = self.DEBUG_DROPDOWN_ID
            screen.addDropDownBoxGFC(
                self.szDropdownName,
                22,
                12,
                300,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                FontTypes.GAME_FONT,
            )
            for j in range(gc.getMAX_PLAYERS()):
                if gc.getPlayer(j).isAlive():
                    screen.addPullDownString(
                        self.szDropdownName,
                        gc.getPlayer(j).getCivilizationShortDescription(0),
                        j,
                        j,
                        False,
                    )

        # Draw Corporation info
        self.drawCorporationInfo()

        self.drawCityInfo(self.iCorporationSelected)

    # Draws the Corporation buttons and information
    def drawCorporationInfo(self):

        screen = self.getScreen()

        # Put everything on a scrollable area
        szArea = self.CORPORATION_PANEL_ID
        screen.addPanel(
            szArea,
            "",
            "",
            False,
            True,
            self.X_CORPORATION_AREA,
            self.Y_CORPORATION_AREA,
            self.W_CORPORATION_AREA,
            self.H_CORPORATION_AREA,
            PanelStyles.PANEL_STYLE_MAIN,
        )

        # Corporation buttons at the top
        xLoop = self.X_CORPORATION_START
        for i in range(gc.getNumCorporationInfos()):
            szButtonName = self.getCorporationButtonName(i)
            screen.addCheckBoxGFC(
                szButtonName,
                gc.getCorporationInfo(i).getButton(),
                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                self.X_CORPORATION_AREA + xLoop - self.BUTTON_SIZE / 2,
                self.Y_CORPORATION_AREA + self.Y_CORPORATION - self.BUTTON_SIZE / 2,
                self.BUTTON_SIZE,
                self.BUTTON_SIZE,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            xLoop += self.DX_CORPORATION

        # Absinthe: no need for these with the new company system
        # Great Person
        # xLoop = self.X_CORPORATION_START
        # for i in range(gc.getNumCorporationInfos()):
        # szGreatPerson = ""
        # for iBuilding in range(gc.getNumBuildingInfos()):
        # if (gc.getBuildingInfo(iBuilding).getFoundsCorporation() == i):
        # break
        # for iUnit in range(gc.getNumUnitInfos()):
        # if gc.getUnitInfo(iUnit).getBuildings(iBuilding) or gc.getUnitInfo(iUnit).getForceBuildings(iBuilding):
        # szGreatPerson = gc.getUnitInfo(iUnit).getDescription()
        # break
        # screen.setLabelAt("", szArea, szGreatPerson, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_GREAT_PERSON, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        # xLoop += self.DX_CORPORATION
        # Absinthe: end

        # Bonuses
        xLoop = self.X_CORPORATION_START
        for i in range(gc.getNumCorporationInfos()):
            szListLabels = []
            iNum = 0
            szList = u""
            for iRequired in range(gc.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES")):
                eBonus = gc.getCorporationInfo(i).getPrereqBonus(iRequired)
                if -1 != eBonus:
                    if iNum == 0:
                        szList = u""
                    else:
                        szList += u"  "  # Absinthe
                    iNum += 1
                    szList += u"%c" % (gc.getBonusInfo(eBonus).getChar(),)

                    if iNum > 2:  # Absinthe
                        iNum = 0
                        szListLabels.append(szList)
                        szList = u""

            if len(szList) > 0:
                szListLabels.append(szList)

            iRow = 0
            for szList in szListLabels:
                screen.setLabelAt(
                    "",
                    szArea,
                    szList,
                    CvUtil.FONT_CENTER_JUSTIFY,
                    xLoop,
                    self.Y_BONUSES + iRow,
                    self.DZ,
                    FontTypes.SMALL_FONT,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                )
                iRow += 16

            xLoop += self.DX_CORPORATION

        # Absinthe: no need for these with the new company system
        # Founded...
        # screen.setLabelAt("", szArea, text("TXT_KEY_RELIGION_SCREEN_DATE_FOUNDED"), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        # Date Founded:
        # xLoop = self.X_CORPORATION_START
        # for i in range(gc.getNumCorporationInfos()):
        # if (gc.getGame().getCorporationGameTurnFounded(i) < 0):
        # szFounded = text("TXT_KEY_RELIGION_SCREEN_NOT_FOUNDED")
        # else:
        # szFounded = CyGameTextMgr().getTimeStr(gc.getGame().getCorporationGameTurnFounded(i), False)
        # screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        # xLoop += self.DX_CORPORATION

        # Headquarters
        # screen.setLabelAt("", szArea, text("TXT_KEY_CORPORATION_SCREEN_HEADQUARTERS"), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_HEADQUARTERS, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        # xLoop = self.X_CORPORATION_START
        # for i in range(gc.getNumCorporationInfos()):
        # pHeadquarters = gc.getGame().getHeadquarters(i)
        # if pHeadquarters.isNone():
        # szFounded = u"-"
        # screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HEADQUARTERS, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
        # elif not pHeadquarters.isRevealed(gc.getPlayer(self.iActivePlayer).getTeam(), False):
        # szFounded = text("TXT_KEY_UNKNOWN")
        # screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HEADQUARTERS, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
        # else:
        # szFounded = pHeadquarters.getName()
        # screen.setLabelAt("", szArea, "(%s)" % gc.getPlayer(pHeadquarters.getOwner()).getCivilizationAdjective(0), CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HEADQUARTERS+8, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
        # screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HEADQUARTERS-8, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
        # xLoop += self.DX_CORPORATION
        # Absinthe: end

        self.iCorporationSelected = -1
        self.iCorporationExamined = self.iCorporationSelected
        self.iCorporationOriginal = self.iCorporationSelected

    # Draws the city list
    def drawCityInfo(self, iCorporation):

        if not self.bScreenUp:
            return

        screen = self.getScreen()

        if iCorporation == gc.getNumCorporationInfos():
            iLinkCorporation = -1
        else:
            iLinkCorporation = iCorporation

        szArea1 = self.AREA1_ID
        screen.addPanel(
            self.AREA1_ID,
            "",
            "",
            True,
            True,
            self.X_CITY1_AREA,
            self.Y_CITY_AREA,
            self.W_CITY_AREA,
            self.H_CITY_AREA,
            PanelStyles.PANEL_STYLE_MAIN,
        )

        szArea2 = self.AREA2_ID
        screen.addPanel(
            self.AREA2_ID,
            "",
            "",
            True,
            True,
            self.X_CITY2_AREA,
            self.Y_CITY_AREA,
            self.W_CITY_AREA,
            self.H_CITY_AREA,
            PanelStyles.PANEL_STYLE_MAIN,
        )

        szArea = self.CORPORATION_PANEL_ID
        for i in range(gc.getNumCorporationInfos()):
            if self.iCorporationSelected == i:
                screen.setState(self.getCorporationButtonName(i), True)
            else:
                screen.setState(self.getCorporationButtonName(i), False)

        iPlayer = PyPlayer(self.iActivePlayer)

        cityList = iPlayer.getCityList()

        # Loop through the cities
        szLeftCities = u""
        szRightCities = u""
        for i in range(len(cityList)):

            bFirstColumn = i % 2 == 0

            pLoopCity = cityList[i]

            # Constructing the City name...
            szCityName = u""
            if pLoopCity.isCapital():
                szCityName += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)

            lHeadquarters = pLoopCity.getHeadquarters()
            if lHeadquarters:
                for iI in range(len(lHeadquarters)):
                    szCityName += u"%c" % (
                        gc.getCorporationInfo(lHeadquarters[iI]).getHeadquarterChar()
                    )

            lCorporations = pLoopCity.getCorporations()
            if lCorporations:
                for iI in range(len(lCorporations)):
                    if lCorporations[iI] not in lHeadquarters:
                        szCityName += u"%c" % (gc.getCorporationInfo(lCorporations[iI]).getChar())

            # Absinthe: long name fix
            szCityName += pLoopCity.getName()[0:27] + "  "

            if iLinkCorporation == -1:
                bFirst = True
                for iI in range(len(lCorporations)):
                    szTempBuffer = CyGameTextMgr().getCorporationHelpCity(
                        lCorporations[iI], pLoopCity.GetCy(), False, False
                    )
                    if szTempBuffer:
                        if not bFirst:
                            szCityName += u", "
                        szCityName += szTempBuffer
                        bFirst = False
            else:
                szCityName += CyGameTextMgr().getCorporationHelpCity(
                    iLinkCorporation, pLoopCity.GetCy(), False, True
                )

            if bFirstColumn:
                szLeftCities += u"<font=3>" + szCityName + u"</font>\n"
            else:
                szRightCities += u"<font=3>" + szCityName + u"</font>\n"

        screen.addMultilineText(
            "Child" + self.AREA1_ID,
            szLeftCities,
            self.X_CITY1_AREA + 5,
            self.Y_CITY_AREA + 5,
            self.W_CITY_AREA - 10,
            self.H_CITY_AREA - 10,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            CvUtil.FONT_LEFT_JUSTIFY,
        )
        screen.addMultilineText(
            "Child" + self.AREA2_ID,
            szRightCities,
            self.X_CITY2_AREA + 5,
            self.Y_CITY_AREA + 5,
            self.W_CITY_AREA - 10,
            self.H_CITY_AREA - 10,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            CvUtil.FONT_LEFT_JUSTIFY,
        )

        # Header...
        if self.iCorporationExamined != -1:
            screen.setLabel(
                self.HEADER_NAME,
                "Background",
                u"<font=4b>"
                + gc.getCorporationInfo(self.iCorporationExamined).getDescription().upper()
                + u"</font>",
                CvUtil.FONT_CENTER_JUSTIFY,
                self.X_SCREEN,
                self.Y_TITLE,
                self.Z_TEXT,
                FontTypes.TITLE_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )
        else:
            screen.setLabel(
                self.HEADER_NAME,
                "Background",
                u"<font=4b>" + text("TXT_KEY_CORPORATION_SCREEN_TITLE").upper() + u"</font>",
                CvUtil.FONT_CENTER_JUSTIFY,
                self.X_SCREEN,
                self.Y_TITLE,
                self.Z_TEXT,
                FontTypes.TITLE_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )

        screen.setText(
            self.EXIT_NAME,
            "Background",
            self.EXIT_TEXT,
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXIT,
            self.Y_EXIT,
            self.Z_TEXT,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            1,
            0,
        )

    def Exit(self, inputClass):
        screen = self.getScreen()
        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
            screen.hideScreen()

    def getCorporationButtonName(self, iCorporation):
        szName = self.BUTTON_NAME + str(iCorporation)
        return szName

    def getCorporationTextName(self, iCorporation):
        szName = self.CORPORATION_NAME + str(iCorporation)
        return szName

    # Will handle the input for this screen...
    def handleInput(self, inputClass):
        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
            screen = self.getScreen()
            iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
            self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
            self.drawCorporationInfo()
            self.drawCityInfo(self.iCorporationSelected)
            return 1
        elif self.CorporationScreenInputMap.has_key(inputClass.getFunctionName()):
            "Calls function mapped in CorporationScreenInputMap"
            # only get from the map if it has the key

            # get bound function from map and call it
            self.CorporationScreenInputMap.get(inputClass.getFunctionName())(inputClass)
            return 1
        return 0

    def update(self, fDelta):
        return

    # Corporation Button
    def CorporationScreenButton(self, inputClass):
        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
            if self.iCorporationSelected == inputClass.getID():
                self.iCorporationSelected = -1
            else:
                self.iCorporationSelected = inputClass.getID()
            self.iCorporationExamined = self.iCorporationSelected
            self.drawCityInfo(self.iCorporationSelected)
        elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON:
            self.iCorporationExamined = inputClass.getID()
            self.drawCityInfo(self.iCorporationExamined)
        elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF:
            self.iCorporationExamined = self.iCorporationSelected
            self.drawCityInfo(self.iCorporationSelected)
        return 0
