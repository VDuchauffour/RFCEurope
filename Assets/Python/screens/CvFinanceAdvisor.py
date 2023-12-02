## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
from CoreTypes import SpecialParameter, StabilityCategory
from CoreStructures import player as _player
import CvUtil
import CvScreenEnums


import RFCUtils  # Rhye
import Stability  # Absinthe

# Mercenary Upkeep
# import MercenaryUtils
# objMercenaryUtils = MercenaryUtils.MercenaryUtils()

utils = RFCUtils.RFCUtils()  # Rhye
stab = Stability.Stability()  # Absinthe

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvFinanceAdvisor:
    def __init__(self):
        self.SCREEN_NAME = "FinanceAdvisor"
        self.DEBUG_DROPDOWN_ID = "FinanceAdvisorDropdownWidget"
        self.WIDGET_ID = "FinanceAdvisorWidget"
        self.WIDGET_HEADER = "FinanceAdvisorWidgetHeader"
        self.EXIT_ID = "FinanceAdvisorExitWidget"
        self.BACKGROUND_ID = "FinanceAdvisorBackground"
        self.X_SCREEN = 500
        self.Y_SCREEN = 396
        self.W_SCREEN = 1024
        self.H_SCREEN = 768
        self.Y_TITLE = 12
        self.BORDER_WIDTH = 4
        self.PANE_HEIGHT = 340  # 450 #Rhye
        self.PANE_WIDTH = 283
        self.X_SLIDERS = 50
        self.X_INCOME = 373
        self.X_EXPENSES = 696
        self.Y_TREASURY = 60  # 90 #Rhye
        self.H_TREASURY = 60  # 100 #Rhye
        self.Y_LOCATION = 130  # 230 #Rhye
        self.Y_SPACING = 30
        self.TEXT_MARGIN = 15
        self.Z_BACKGROUND = -2.1
        self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
        self.DZ = -0.2
        self.X_EXIT = 994
        self.Y_EXIT = 726
        self.Y_STABILITY = 480  # Rhye
        self.Y_PARAMETERS = 550  # Rhye
        self.H_PARAMETERS = 140  # Rhye
        self.PARAMETERS_WIDTH = 170  # Rhye
        self.X_PARAMETERS1 = self.X_SLIDERS  # Rhye
        self.X_PARAMETERS2 = self.X_PARAMETERS1 + self.PARAMETERS_WIDTH + 20  # Rhye
        self.X_PARAMETERS3 = self.X_PARAMETERS2 + self.PARAMETERS_WIDTH + 20  # Rhye
        self.X_PARAMETERS4 = self.X_PARAMETERS3 + self.PARAMETERS_WIDTH + 20  # Rhye
        self.X_PARAMETERS5 = self.X_PARAMETERS4 + self.PARAMETERS_WIDTH + 20  # Rhye

        self.nWidgetCount = 0

    def getScreen(self):
        return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.FINANCE_ADVISOR)

    def interfaceScreen(self):

        self.iActiveLeader = CyGame().getActivePlayer()

        player = gc.getPlayer(self.iActiveLeader)

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
        screen.setText(
            self.EXIT_ID,
            "Background",
            u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>",
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXIT,
            self.Y_EXIT,
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_CLOSE_SCREEN,
            -1,
            -1,
        )

        # Header...
        screen.setLabel(
            self.WIDGET_HEADER,
            "Background",
            u"<font=4b>"
            + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TITLE", ()).upper()
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_SCREEN,
            self.Y_TITLE,
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

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
                        self.szDropdownName, gc.getPlayer(j).getName(), j, j, False
                    )

        # Absinthe: update all stability values for the active player
        # iGameTurn = turn()
        stab.refreshBaseStability(self.iActiveLeader)

        # draw the contents
        self.drawContents()

    def drawContents(self):
        self.deleteAllWidgets()
        self.drawFinance()
        return 0

    def drawFinance(self):
        # Create a new screen, called FinanceAdvisor, using the file FinanceAdvisor.py for input
        screen = self.getScreen()
        player = gc.getPlayer(self.iActiveLeader)
        ePlayer = self.iActiveLeader  # Rhye

        # Rhye - start
        iStability = player.getStability()
        if iStability < -15:
            szTempBuffer = localText.getText("TXT_KEY_STABILITY_COLLAPSING", ())
        elif iStability >= -15 and iStability < -5:
            szTempBuffer = localText.getText("TXT_KEY_STABILITY_UNSTABLE", ())
        elif iStability >= -5 and iStability < 0:
            szTempBuffer = localText.getText("TXT_KEY_STABILITY_SHAKY", ())
        elif iStability >= 0 and iStability < 8:
            szTempBuffer = localText.getText("TXT_KEY_STABILITY_STABLE", ())
        elif iStability >= 8 and iStability < 15:
            szTempBuffer = localText.getText("TXT_KEY_STABILITY_SOLID", ())
        elif iStability >= 15:
            szTempBuffer = localText.getText("TXT_KEY_STABILITY_VERYSOLID", ())

        if gc.getPlayer(ePlayer).isHuman():
            szTempBuffer = "%s  %i" % (szTempBuffer, iStability)
        # Rhye - end

        totalUnitCost = player.calculateUnitCost()
        totalUnitSupply = player.calculateUnitSupply()
        totalMaintenance = player.getTotalMaintenance()
        totalCivicUpkeep = player.getCivicUpkeep([], False)
        totalPreInflatedCosts = player.calculatePreInflatedCosts()
        totalInflatedCosts = player.calculateInflatedCosts()
        goldCommerce = player.getCommerceRate(CommerceTypes.COMMERCE_GOLD)
        if not player.isCommerceFlexible(CommerceTypes.COMMERCE_RESEARCH):
            goldCommerce += player.calculateBaseNetResearch()
        gold = player.getGold()
        goldFromCivs = player.getGoldPerTurn()

        # Colony Upkeep
        # 1 -> 10, 2 -> 16, 3 -> 25, 4 -> 37, 5 -> 52, 6 -> 70, 7 -> 91, 8 -> 115, 9 -> 142, 10 -> 172
        iColonyNumber = player.getNumColonies()
        iColonyUpkeep = 0
        if iColonyNumber > 0:
            iColonyUpkeep = int(
                (0.5 * iColonyNumber * iColonyNumber + 0.5 * iColonyNumber) * 3 + 7
            )

        # Mercenary Upkeep
        totalMercenaryMaintenanceCost = (
            player.getPicklefreeParameter(SpecialParameter.MERCENARY_COST_PER_TURN.value) + 99
        ) / 100

        szTreasuryPanel = self.getNextWidgetName()
        screen.addPanel(
            szTreasuryPanel,
            u"",
            "",
            True,
            True,
            self.X_SLIDERS,
            self.Y_TREASURY,
            self.X_EXPENSES + self.PANE_WIDTH - self.X_SLIDERS,
            self.H_TREASURY,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            szTreasuryPanel,
            u"<font=4>"
            + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TREASURY", (gold,)).upper()
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            (self.X_SLIDERS + self.PANE_WIDTH + self.X_EXPENSES) / 2,
            self.Y_TREASURY + self.H_TREASURY / 2 - self.Y_SPACING / 2,
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_GOLD_RESERVE,
            -1,
            -1,
        )

        szCommercePanel = self.getNextWidgetName()
        screen.addPanel(
            szCommercePanel,
            u"",
            "",
            True,
            True,
            self.X_SLIDERS,
            self.Y_LOCATION,
            self.PANE_WIDTH,
            self.PANE_HEIGHT,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_COMMERCE", ()).upper() + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_SLIDERS + self.PANE_WIDTH / 2,
            self.Y_LOCATION + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        szIncomePanel = self.getNextWidgetName()
        screen.addPanel(
            szIncomePanel,
            u"",
            "",
            True,
            True,
            self.X_INCOME,
            self.Y_LOCATION,
            self.PANE_WIDTH,
            self.PANE_HEIGHT,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_INCOME_HEADER", ()).upper()
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_INCOME + self.PANE_WIDTH / 2,
            self.Y_LOCATION + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        szExpensePanel = self.getNextWidgetName()
        screen.addPanel(
            szExpensePanel,
            u"",
            "",
            True,
            True,
            self.X_EXPENSES,
            self.Y_LOCATION,
            self.PANE_WIDTH,
            self.PANE_HEIGHT,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_EXPENSES_HEADER", ()).upper()
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_EXPENSES + self.PANE_WIDTH / 2,
            self.Y_LOCATION + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        # Rhye - start
        szStabilityPanel = self.getNextWidgetName()
        screen.addPanel(
            szStabilityPanel,
            u"",
            "",
            True,
            True,
            self.X_SLIDERS,
            self.Y_STABILITY,
            self.X_EXPENSES + self.PANE_WIDTH - self.X_SLIDERS,
            self.H_TREASURY,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            szStabilityPanel,
            u"<font=4>"
            + localText.getText("TXT_KEY_STABILITY_ADVISOR_TITLE", ()).upper()
            + " "
            + szTempBuffer
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            (self.X_SLIDERS + self.PANE_WIDTH + self.X_EXPENSES) / 2,
            self.Y_STABILITY + self.H_TREASURY / 2 - self.Y_SPACING / 2,
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        szParametersPanel1 = self.getNextWidgetName()
        screen.addPanel(
            szParametersPanel1,
            u"",
            "",
            True,
            True,
            self.X_PARAMETERS1,
            self.Y_PARAMETERS,
            self.PARAMETERS_WIDTH,
            self.H_PARAMETERS,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_STABILITY_PARAMETER_CITIES", ()).upper()
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS1 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            szParametersPanel1,
            u"<font=4>"
            + str(self.retrieve_stability_category_value(ePlayer, StabilityCategory.CITIES))
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS1 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN + 50,
            self.Z_CONTROLS + self.DZ,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,  # pour context menu changer ce widget
            -1,  # et mettre eplayer ici ?
            -1,
        )

        szParametersPanel2 = self.getNextWidgetName()
        screen.addPanel(
            szParametersPanel2,
            u"",
            "",
            True,
            True,
            self.X_PARAMETERS2,
            self.Y_PARAMETERS,
            self.PARAMETERS_WIDTH,
            self.H_PARAMETERS,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_STABILITY_PARAMETER_CIVICS", ()).upper()
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS2 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            szParametersPanel2,
            u"<font=4>"
            + str(self.retrieve_stability_category_value(ePlayer, StabilityCategory.CIVICS))
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS2 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN + 50,
            self.Z_CONTROLS + self.DZ,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        szParametersPanel3 = self.getNextWidgetName()
        screen.addPanel(
            szParametersPanel3,
            u"",
            "",
            True,
            True,
            self.X_PARAMETERS3,
            self.Y_PARAMETERS,
            self.PARAMETERS_WIDTH,
            self.H_PARAMETERS,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_STABILITY_PARAMETER_ECONOMY", ()).upper()
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS3 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            szParametersPanel3,
            u"<font=4>"
            + str(self.retrieve_stability_category_value(ePlayer, StabilityCategory.ECONOMY))
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS3 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN + 50,
            self.Z_CONTROLS + self.DZ,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        szParametersPanel4 = self.getNextWidgetName()
        screen.addPanel(
            szParametersPanel4,
            u"",
            "",
            True,
            True,
            self.X_PARAMETERS4,
            self.Y_PARAMETERS,
            self.PARAMETERS_WIDTH,
            self.H_PARAMETERS,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_STABILITY_PARAMETER_EXPANSION", ()).upper()
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS4 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            szParametersPanel4,
            u"<font=4>"
            + str(self.retrieve_stability_category_value(ePlayer, StabilityCategory.EXPANSION))
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS4 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN + 50,
            self.Z_CONTROLS + self.DZ,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        szParametersPanel5 = self.getNextWidgetName()
        screen.addPanel(
            szParametersPanel5,
            u"",
            "",
            True,
            True,
            self.X_PARAMETERS5,
            self.Y_PARAMETERS,
            self.PARAMETERS_WIDTH,
            self.H_PARAMETERS,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_STABILITY_PARAMETER_SWING", ()).upper()
            + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS5 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            szParametersPanel5,
            u"<font=4>" + str(self.retrieve_stability_category_value(ePlayer, None)) + u"</font>",
            CvUtil.FONT_CENTER_JUSTIFY,
            self.X_PARAMETERS5 + self.PARAMETERS_WIDTH / 2,
            self.Y_PARAMETERS + self.TEXT_MARGIN + 50,
            self.Z_CONTROLS + self.DZ,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        # # Rhye - end

        # Slider percentages
        yLocation = self.Y_LOCATION

        yLocation += 0.5 * self.Y_SPACING
        for iI in range(CommerceTypes.NUM_COMMERCE_TYPES):
            eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES

            if player.isCommerceFlexible(eCommerce):
                yLocation += self.Y_SPACING
                screen.setButtonGFC(
                    self.getNextWidgetName(),
                    u"",
                    "",
                    self.X_SLIDERS + self.TEXT_MARGIN,
                    int(yLocation) + self.TEXT_MARGIN,
                    20,
                    20,
                    WidgetTypes.WIDGET_CHANGE_PERCENT,
                    eCommerce,
                    gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"),
                    ButtonStyles.BUTTON_STYLE_CITY_PLUS,
                )
                screen.setButtonGFC(
                    self.getNextWidgetName(),
                    u"",
                    "",
                    self.X_SLIDERS + self.TEXT_MARGIN + 24,
                    int(yLocation) + self.TEXT_MARGIN,
                    20,
                    20,
                    WidgetTypes.WIDGET_CHANGE_PERCENT,
                    eCommerce,
                    -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"),
                    ButtonStyles.BUTTON_STYLE_CITY_MINUS,
                )

                szText = (
                    u"<font=3>"
                    + gc.getCommerceInfo(eCommerce).getDescription()
                    + u" ("
                    + unicode(player.getCommercePercent(eCommerce))  # type: ignore
                    + u"%)</font>"
                )
                screen.setLabel(
                    self.getNextWidgetName(),
                    "Background",
                    szText,
                    CvUtil.FONT_LEFT_JUSTIFY,
                    self.X_SLIDERS + self.TEXT_MARGIN + 50,
                    yLocation + self.TEXT_MARGIN,
                    self.Z_CONTROLS + self.DZ,
                    FontTypes.GAME_FONT,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                )
                szRate = (
                    u"<font=3>"
                    + unicode(player.getCommerceRate(CommerceTypes(eCommerce)))  # type: ignore
                    + u"</font>"
                )
                screen.setLabel(
                    self.getNextWidgetName(),
                    "Background",
                    szRate,
                    CvUtil.FONT_RIGHT_JUSTIFY,
                    self.X_SLIDERS + self.PANE_WIDTH - self.TEXT_MARGIN,
                    yLocation + self.TEXT_MARGIN,
                    self.Z_CONTROLS + self.DZ,
                    FontTypes.GAME_FONT,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                )

        yLocation += self.Y_SPACING
        szText = (
            u"<font=3>"
            + gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getDescription()
            + u" ("
            + unicode(player.getCommercePercent(CommerceTypes.COMMERCE_GOLD))  # type: ignore
            + u"%)</font>"
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            szText,
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_SLIDERS + self.TEXT_MARGIN + 50,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        szCommerce = u"<font=3>" + unicode(goldCommerce) + u"</font>"  # type: ignore
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            szCommerce,
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_SLIDERS + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        # Income
        yLocation = self.Y_LOCATION
        iIncome = 0

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TAXES", ()) + "</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_INCOME + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_GROSS_INCOME,
            -1,
            -1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(goldCommerce) + "</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_INCOME + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_GROSS_INCOME,
            -1,
            -1,
        )
        iIncome += goldCommerce

        if goldFromCivs > 0:
            yLocation += self.Y_SPACING
            szText = (
                unicode(goldFromCivs)  # type: ignore
                + " : "
                + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_PER_TURN", ())
            )
            screen.setLabel(
                self.getNextWidgetName(),
                "Background",
                u"<font=3>"
                + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_PER_TURN", ())
                + "</font>",
                CvUtil.FONT_LEFT_JUSTIFY,
                self.X_INCOME + self.TEXT_MARGIN,
                yLocation + self.TEXT_MARGIN,
                self.Z_CONTROLS + self.DZ,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME,
                self.iActiveLeader,
                1,
            )
            screen.setLabel(
                self.getNextWidgetName(),
                "Background",
                u"<font=3>" + unicode(goldFromCivs) + "</font>",  # type: ignore
                CvUtil.FONT_RIGHT_JUSTIFY,
                self.X_INCOME + self.PANE_WIDTH - self.TEXT_MARGIN,
                yLocation + self.TEXT_MARGIN,
                self.Z_CONTROLS + self.DZ,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME,
                self.iActiveLeader,
                1,
            )
            iIncome += goldFromCivs

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_INCOME", ()) + "</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_INCOME + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(iIncome) + "</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_INCOME + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        iIncome += goldFromCivs

        # Expenses
        yLocation = self.Y_LOCATION
        iExpenses = 0

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_UNITCOST", ()) + u"</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_EXPENSES + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_UNIT_COST,
            self.iActiveLeader,
            1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(totalUnitCost) + u"</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_UNIT_COST,
            self.iActiveLeader,
            1,
        )
        iExpenses += totalUnitCost

        yLocation += self.Y_SPACING
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_UNITSUPPLY", ())
            + "</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_EXPENSES + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_AWAY_SUPPLY,
            self.iActiveLeader,
            1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(totalUnitSupply) + "</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_AWAY_SUPPLY,
            self.iActiveLeader,
            1,
        )
        iExpenses += totalUnitSupply

        # Absinthe: Mercenary Upkeep
        yLocation += self.Y_SPACING
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_MERCENARY_MAINTENANCE", ())
            + "</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_EXPENSES + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_MERCENARY_MAINTENANCE,
            self.iActiveLeader,
            1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(totalMercenaryMaintenanceCost) + "</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_MERCENARY_MAINTENANCE,
            self.iActiveLeader,
            1,
        )
        iExpenses += totalMercenaryMaintenanceCost

        yLocation += self.Y_SPACING
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_MAINTENANCE", ())
            + "</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_EXPENSES + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_CITY_MAINT,
            self.iActiveLeader,
            1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(totalMaintenance) + "</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_CITY_MAINT,
            self.iActiveLeader,
            1,
        )
        iExpenses += totalMaintenance

        # Absinthe: Colony Upkeep
        yLocation += self.Y_SPACING
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>"
            + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_COLONY_UPKEEP", ())
            + "</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_EXPENSES + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_COLONY_UPKEEP,
            self.iActiveLeader,
            1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(iColonyUpkeep) + "</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_COLONY_UPKEEP,
            self.iActiveLeader,
            1,
        )
        iExpenses += iColonyUpkeep

        yLocation += self.Y_SPACING
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_CIVICS", ()) + "</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_EXPENSES + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_CIVIC_UPKEEP,
            self.iActiveLeader,
            1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(totalCivicUpkeep) + "</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_CIVIC_UPKEEP,
            self.iActiveLeader,
            1,
        )
        iExpenses += totalCivicUpkeep

        if goldFromCivs < 0:
            yLocation += self.Y_SPACING
            screen.setLabel(
                self.getNextWidgetName(),
                "Background",
                u"<font=3>"
                + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_COST_PER_TURN", ())
                + "</font>",
                CvUtil.FONT_LEFT_JUSTIFY,
                self.X_EXPENSES + self.TEXT_MARGIN,
                yLocation + self.TEXT_MARGIN,
                self.Z_CONTROLS + self.DZ,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME,
                self.iActiveLeader,
                1,
            )
            screen.setLabel(
                self.getNextWidgetName(),
                "Background",
                u"<font=3>" + unicode(-goldFromCivs) + "</font>",  # type: ignore
                CvUtil.FONT_RIGHT_JUSTIFY,
                self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN,
                yLocation + self.TEXT_MARGIN,
                self.Z_CONTROLS + self.DZ,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME,
                self.iActiveLeader,
                1,
            )
            iExpenses -= goldFromCivs

        yLocation += self.Y_SPACING
        iInflation = totalInflatedCosts - totalPreInflatedCosts
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_INFLATION", ()) + "</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_EXPENSES + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_INFLATED_COSTS,
            self.iActiveLeader,
            1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(iInflation) + "</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_HELP_FINANCE_INFLATED_COSTS,
            self.iActiveLeader,
            1,
        )
        iExpenses += iInflation

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_EXPENSES", ()) + "</font>",
            CvUtil.FONT_LEFT_JUSTIFY,
            self.X_EXPENSES + self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.setLabel(
            self.getNextWidgetName(),
            "Background",
            u"<font=3>" + unicode(iExpenses) + "</font>",  # type: ignore
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN,
            yLocation + self.TEXT_MARGIN,
            self.Z_CONTROLS + self.DZ,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        return 0

    # returns a unique ID for a widget in this screen
    def getNextWidgetName(self):
        szName = self.WIDGET_ID + str(self.nWidgetCount)
        self.nWidgetCount += 1
        return szName

    def deleteAllWidgets(self):
        screen = self.getScreen()
        i = self.nWidgetCount - 1
        while i >= 0:
            self.nWidgetCount = i
            screen.deleteWidget(self.getNextWidgetName())
            i -= 1

        self.nWidgetCount = 0

    # Will handle the input for this screen...
    def handleInput(self, inputClass):
        "Calls function mapped in FinanceAdvisorInputMap"
        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
            screen = self.getScreen()
            iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
            self.iActiveLeader = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
            self.drawContents()
        return 0

    def update(self, fDelta):
        if CyInterface().isDirty(InterfaceDirtyBits.Financial_Screen_DIRTY_BIT) is True:
            CyInterface().setDirty(InterfaceDirtyBits.Financial_Screen_DIRTY_BIT, False)
            self.drawContents()
        return

    # Rhye - start
    def printStars(self, ePlayer, panel, n, x, y, z):
        totStars = ""
        for i in range(n):
            totStars = totStars + unichr(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))  # type: ignore
        if gc.getPlayer(ePlayer).isHuman():
            self.getScreen().setLabel(
                panel,
                "Background",
                totStars,
                CvUtil.FONT_CENTER_JUSTIFY,
                x,
                y,
                z,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )

    def printArrow(self, ePlayer, panel, iParameter, x, y, z):
        if gc.getPlayer(ePlayer).isHuman():
            self.getScreen().setLabel(
                panel,
                "Background",
                unichr(  # type: ignore
                    CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 8 + utils.getArrow(iParameter)
                ),
                CvUtil.FONT_CENTER_JUSTIFY,
                x,
                y,
                z,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )

    def retrieve_stability_category_value(self, player, stability_category):
        if stability_category is not None:
            return _player(player).getStabilityBase(stability_category.value)
        else:
            return _player(player).getStabilitySwing()

    # Rhye - end
