#
# Mercenaries Mod
# By: The Lopez
# CvMercenaryManager
#
# 3Miro: we take the merc screen as it looks well. However, the rest of the mechanics have been changed mostly to remove unnecessary features that slow down things

from CvPythonExtensions import *
import CvUtil
import PyHelpers

# import MercenaryUtils
import Mercenaries
import Consts as con
import XMLConsts as xml

# from sets import Set
# import CvConfigParser #Rhye
from CvMercenaryScreensEnums import *

PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
# objMercenaryUtils = MercenaryUtils.MercenaryUtils()

# 3Miro: this class will provide the needed interface for the RFCE Merc mechanics
GMU = Mercenaries.GlobalMercenaryUtils()
lMercList = Mercenaries.lMercList

# Change this to True if hiring mercenaries should only be allowed if one or more of
# a player's civilization contains one or more of the buildings specified in the
# "Mercenary Starting Location" option. Oh did I forget to mention, if the "Mercenary
# Starting Location" option isn't set to a list of buildings players won't be able to
# hire any mercenaries.
# Default value is False
g_bRequireStartingLocationContainBuildings = False

# Change this to True to delay the return of contracted out units to player's cities
# by the amount indicated in "Unit Return Delay Amount". The value set to "Consume Unit
# Moves On Return" will be treated as if set to False if "Delay Mercenary Placement" is
# set to True.
# Default value is True
g_bDelayUnitReturn = True

# Change this to False to allow contracting out units outside of cities.
# Default value is True
g_bRequireCityUnitContractCreation = True

# Set to True to print out debug messages in the logs
g_bDebug = False


class CvMercenaryManager:
    "Mercenary Manager"

    def __init__(self, iScreenId):

        self.mercenaryName = None
        self.screenFunction = None

        # The different UI wiget names
        self.MERCENARY_MANAGER_SCREEN_NAME = "MercenaryManager"

        self.WIDGET_ID = "MercenaryManagerWidget"
        self.Z_BACKGROUND = -2.1
        self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
        self.EventKeyDown = 6

        self.iScreenId = iScreenId

        # When populated this dictionary will contain the information needed to build
        # the widgets for the current screen resolution.
        self.screenWidgetData = {}

        self.nWidgetCount = 0
        self.iActivePlayer = -1

        self.currentScreen = MERCENARY_MANAGER

        global g_bRequireStartingLocationContainBuildings
        global g_bDelayUnitReturn
        global g_bRequireCityUnitContractCreation

    # Returns the instance of the mercenary manager screen.
    def getScreen(self):
        return CyGInterfaceScreen(self.MERCENARY_MANAGER_SCREEN_NAME, self.iScreenId)

    # Gets the instance of the mercenary manager screen and hides it.
    def hideScreen(self):
        screen = self.getScreen()
        screen.hideScreen()

    # Returns True if the screen is active, False otherwise.
    def isActive(self):
        return self.getScreen().isActive()

    # Screen construction function
    def interfaceScreen(self):

        # Create a new screen
        screen = self.getScreen()

        if screen.isActive():
            return

        screen.setRenderInterfaceOnly(True)
        screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

        self.nWidgetCount = 0

        self.iActivePlayer = gc.getGame().getActivePlayer()

        screen = self.getScreen()

        # Calculate all of the screen position data
        self.calculateScreenWidgetData(screen)

        if self.currentScreen == MERCENARY_MANAGER:
            self.drawMercenaryScreenContent(screen)

    # Populates the panel that shows all of the available mercenaries in the
    # global mercenary pool.
    def populateAvailableMercenariesPanel(self, screen):
        ## 3Miro: draw the available merc info
        # read in the available mercs
        lAvailableMercs = GMU.getMercGlobalPool()
        print("lAvailableMercs", lAvailableMercs)

        # Get the ID for the current active player
        iPlayer = gc.getGame().getActivePlayer()
        # Get the actual current player object
        pPlayer = gc.getPlayer(iPlayer)
        # Get the player's current gold amount
        iGold = pPlayer.getGold()

        # get a list of the provinces controlled by the player
        lProvList = GMU.getOwnedProvinces(iPlayer)
        # lProvList = Set( lProvList ) # set as in set-theory

        mercenaryCount = 0

        iStateReligion = pPlayer.getStateReligion()

        for lMerc in lAvailableMercs:
            # get the name and note that names are no longer Unique
            iMerc = lMerc[0]
            mercenaryName = CyTranslator().getText(lMercList[iMerc][1], ())

            # Absinthe: religion and culture will be checked on the hire button, so the mercs appear on the list even if you can't hire them
            if lMerc[4] not in lProvList:  # we have no matching provinces, skip
                continue

            # screen needs unique internal names
            szUniqueInternalName = "HiredMercID" + self.numToStr(iMerc)

            pUnitInfo = gc.getUnitInfo(lMercList[iMerc][0])
            screen.attachPanel(
                AVAILABLE_MERCENARIES_INNER_PANEL_ID,
                szUniqueInternalName,
                "",
                "",
                False,
                False,
                PanelStyles.PANEL_STYLE_DAWN,
            )
            screen.attachImageButton(
                szUniqueInternalName,
                szUniqueInternalName + "_AInfoButton",
                pUnitInfo.getButton(),
                GenericButtonSizes.BUTTON_SIZE_CUSTOM,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                False,
            )
            if lMercList[iMerc][1] == "TXT_KEY_MERC_GENERIC":
                screen.attachPanel(
                    szUniqueInternalName,
                    szUniqueInternalName + "Text",
                    pUnitInfo.getDescription(),
                    "",
                    True,
                    False,
                    PanelStyles.PANEL_STYLE_EMPTY,
                )
            else:
                screen.attachPanel(
                    szUniqueInternalName,
                    szUniqueInternalName + "Text",
                    pUnitInfo.getDescription() + " (" + mercenaryName + ")",
                    "",
                    True,
                    False,
                    PanelStyles.PANEL_STYLE_EMPTY,
                )

            iHireCost = GMU.getModifiedCostPerPlayer(lMerc[2], iPlayer)
            iUpkeepCost = GMU.getModifiedCostPerPlayer(lMerc[3], iPlayer)

            strHCost = u"%d%c" % (
                iHireCost,
                gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(),
            )
            strMCost = u"%1.2f%c" % (
                0.01 * iUpkeepCost,
                gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(),
            )

            # Absinthe: Add the province name
            sProvName = "TXT_KEY_PROVINCE_NAME_%i" % lMerc[4]
            sProvName = localText.getText(sProvName, ())

            screen.attachLabel(
                szUniqueInternalName + "Text",
                szUniqueInternalName + "text3",
                "     Province: " + sProvName,
            )
            screen.attachLabel(
                szUniqueInternalName + "Text",
                szUniqueInternalName + "text4",
                "     Hire Cost: " + strHCost + "     Maint. Cost: " + strMCost,
            )
            # screen.attachLabel( szUniqueInternalName+"Text", szUniqueInternalName  + "text5", "     Promotions: " + str(len(lMerc[1])-1))

            # Absinthe: checks whether the player has a city with enough culture in the province
            bCulturedEnough = False
            apCityList = PyPlayer(iPlayer).getCityList()
            for pCity in apCityList:
                city = pCity.GetCy()
                if city.getProvince() == lMerc[4] and city.getCultureLevel() >= 2:
                    bCulturedEnough = True
                    break

            # Absinthe: checks whether the player has a coastal city in the province (if the merc is a naval unit)
            bHasCoastalCity = True
            iMercType = lMercList[iMerc][0]
            if gc.getUnitInfo(iMercType).getDomainType() == 0:
                bHasCoastalCity = False
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                    city = pCity.GetCy()
                    if city.getProvince() == lMerc[4] and city.isCoastal(1):
                        bHasCoastalCity = True
                        break

            # Absinthe: money, religion, culture and coastal city check for the hire button
            if (
                iGold - iHireCost >= 0
                and iStateReligion not in lMercList[iMerc][5]
                and bCulturedEnough
                and bHasCoastalCity
            ):
                screen.attachPanel(
                    szUniqueInternalName,
                    szUniqueInternalName + "hireButtonPanel",
                    "",
                    "",
                    False,
                    True,
                    PanelStyles.PANEL_STYLE_EMPTY,
                )
                screen.attachImageButton(
                    szUniqueInternalName,
                    szUniqueInternalName + "_HireButton",
                    "Art/Interface/Buttons/Actions/Join.dds",
                    GenericButtonSizes.BUTTON_SIZE_32,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    False,
                )

            mercenaryCount = mercenaryCount + 1

        # Add the padding to the available mercenaries panel to improve the look of the screen
        if (4 - mercenaryCount) > 0:
            for i in range(4 - mercenaryCount):
                screen.attachPanel(
                    AVAILABLE_MERCENARIES_INNER_PANEL_ID,
                    "dummyPanelHire" + str(i),
                    "",
                    "",
                    True,
                    False,
                    PanelStyles.PANEL_STYLE_EMPTY,
                )
                screen.attachLabel("dummyPanelHire" + str(i), "", "     ")
                # screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
                # screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")

    def clearAvailableMercs(self, screen):

        lGlobalMercPool = GMU.getMercGlobalPool()

        for iI in range(len(lGlobalMercPool)):
            screen.deleteWidget(
                "HiredMercID" + self.numToStr(lGlobalMercPool[iI][0])
            )  # it is OK to delete non-existent widgets

        for iI in range(4):
            screen.deleteWidget("dummyPanelHire" + str(iI))

    # Populates the panel that shows all of the players hired mercenaries
    def populateHiredMercenariesPanel(self, screen):
        ## 3Miro: draw the hired merc info

        iPlayer = gc.getGame().getActivePlayer()
        unitList = PyPlayer(iPlayer).getUnitList()

        mercenaryCount = 0

        for pUnit in unitList:
            iMerc = pUnit.getMercID()
            if iMerc > -1:
                # if this is a Merc
                mercenaryName = pUnit.getNameNoDesc()
                # szUniqueInternalName = "HiredMercID%d" %iMerc
                szUniqueInternalName = "HiredMercID" + self.numToStr(iMerc)

                pUnitInfo = gc.getUnitInfo(pUnit.getUnitType())

                screen.attachPanel(
                    HIRED_MERCENARIES_INNER_PANEL_ID,
                    szUniqueInternalName,
                    "",
                    "",
                    False,
                    False,
                    PanelStyles.PANEL_STYLE_DAWN,
                )
                screen.attachImageButton(
                    szUniqueInternalName,
                    szUniqueInternalName + "_HInfoButton",
                    pUnitInfo.getButton(),
                    GenericButtonSizes.BUTTON_SIZE_CUSTOM,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    False,
                )
                if lMercList[iMerc][1] == "TXT_KEY_MERC_GENERIC":
                    screen.attachPanel(
                        szUniqueInternalName,
                        szUniqueInternalName + "Text",
                        pUnitInfo.getDescription(),
                        "",
                        True,
                        False,
                        PanelStyles.PANEL_STYLE_EMPTY,
                    )
                else:
                    screen.attachPanel(
                        szUniqueInternalName,
                        szUniqueInternalName + "Text",
                        pUnitInfo.getDescription() + " (" + mercenaryName + ")",
                        "",
                        True,
                        False,
                        PanelStyles.PANEL_STYLE_EMPTY,
                    )

                iUpkeep = pUnit.getMercUpkeep()
                strCost = u"%1.2f%c" % (
                    (0.01 * iUpkeep),
                    gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(),
                )

                strXP = u"%d/%d" % (pUnit.getExperience(), pUnit.experienceNeeded())

                screen.attachLabel(
                    szUniqueInternalName + "Text",
                    szUniqueInternalName + "text3",
                    "     Level: " + str(pUnit.getLevel()) + "     XP: " + strXP,
                )
                screen.attachLabel(
                    szUniqueInternalName + "Text",
                    szUniqueInternalName + "text4",
                    "     Maintenance Cost: " + strCost,
                )

                screen.attachPanel(
                    szUniqueInternalName,
                    szUniqueInternalName + "fireButtonPanel",
                    "",
                    "",
                    False,
                    True,
                    PanelStyles.PANEL_STYLE_EMPTY,
                )

                screen.attachImageButton(
                    szUniqueInternalName,
                    szUniqueInternalName + "_FindButton",
                    "Art/Interface/Buttons/Actions/Wake.dds",
                    GenericButtonSizes.BUTTON_SIZE_32,
                    WidgetTypes.WIDGET_CLOSE_SCREEN,
                    -1,
                    -1,
                    False,
                )

                screen.attachImageButton(
                    szUniqueInternalName,
                    szUniqueInternalName + "_FireButton",
                    "Art/Interface/Buttons/Actions/Cancel.dds",
                    GenericButtonSizes.BUTTON_SIZE_32,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    False,
                )

                mercenaryCount = mercenaryCount + 1

        # Add the padding to the hired mercenaries panel to improve the look of the screen
        if (4 - mercenaryCount) > 0:
            for i in range(4 - mercenaryCount):
                screen.attachPanel(
                    HIRED_MERCENARIES_INNER_PANEL_ID,
                    "dummyPanelFire" + str(i),
                    "",
                    "",
                    True,
                    False,
                    PanelStyles.PANEL_STYLE_EMPTY,
                )
                screen.attachLabel("dummyPanelFire" + str(i), "", "     ")
                # screen.attachLabel( "dummyPanelFire"+str(i), "", "     ")
                # screen.attachLabel( "dummyPanelFire"+str(i), "", "     ")

    def clearHiredMercs(self, screen):
        iPlayer = gc.getGame().getActivePlayer()
        unitList = PyPlayer(iPlayer).getUnitList()

        mercenaryCount = 0

        for pUnit in unitList:
            iMerc = pUnit.getMercID()
            if iMerc > -1:
                screen.deleteWidget(
                    "HiredMercID" + self.numToStr(iMerc)
                )  # it is OK to delete non-existent widgets

        for iI in range(4):
            screen.deleteWidget("dummyPanelFire" + str(iI))

    # Clears out the unit information panel contents
    def clearUnitInformation(self, screen):
        screen.deleteWidget(UNIT_INFORMATION_PROMOTION_PANEL_ID)
        screen.deleteWidget(UNIT_INFORMATION_INNER_PROMOTION_PANEL_ID)
        screen.deleteWidget(UNIT_INFORMATION_DETAILS_PANEL_ID)
        screen.deleteWidget(UNIT_GRAPHIC)

    # Clears out the mercenary information panel contents
    def clearMercenaryInformation(self, screen):
        screen.deleteWidget(MERCENARY_INFORMATION_PROMOTION_PANEL_ID)
        screen.deleteWidget(MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_ID)
        screen.deleteWidget(MERCENARY_INFORMATION_DETAILS_PANEL_ID)
        screen.deleteWidget(MERCENARIES_UNIT_GRAPHIC)
        screen.deleteWidget("CombatButtonPanel")
        screen.deleteWidget(MERCENARY_INFORMATION_DETAILS_LIST_ID + "PROVTEXT")

    # Populates the mercenary information panel with the unit information details
    def populateMercenaryInformation(self, screen, lMerc):

        # lMerc = [ iMerc, lPromotions, 0, iUpkeepCost ]
        iMerc = lMerc[0]

        screen.addPanel(
            MERCENARY_INFORMATION_PROMOTION_PANEL_ID,
            "",
            "",
            True,
            True,
            self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X],
            self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y],
            self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH],
            self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.addPanel(
            MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_ID,
            "Promotions",
            "",
            True,
            True,
            self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_X],
            self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_Y],
            self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_WIDTH],
            self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_EMPTY,
        )
        screen.addPanel(
            MERCENARY_INFORMATION_DETAILS_PANEL_ID,
            "",
            "",
            True,
            False,
            self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_X],
            self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_Y],
            self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_WIDTH],
            self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_EMPTY,
        )
        screen.attachListBoxGFC(
            MERCENARY_INFORMATION_DETAILS_PANEL_ID,
            MERCENARY_INFORMATION_DETAILS_LIST_ID,
            "",
            TableStyles.TABLE_STYLE_EMPTY,
        )
        screen.enableSelect(MERCENARY_INFORMATION_DETAILS_LIST_ID, False)

        # Build the mercenary hire cost string
        strHCost = u"%d%c" % (lMerc[2], gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

        # Build the mercenary maintenance cost string
        strMCost = u"%1.2f%c" % (
            0.01 * lMerc[3],
            gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(),
        )

        # Build the unit stats and combat type strings
        pUnitInfo = gc.getUnitInfo(lMercList[lMerc[0]][0])
        iCombatType = pUnitInfo.getUnitCombatType()
        strStats = u"%d%c     %d%c" % (
            pUnitInfo.getCombat(),
            CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR),
            pUnitInfo.getMoves(),
            CyGame().getSymbolID(FontSymbols.MOVES_CHAR),
        )
        strCombat = gc.getUnitCombatInfo(iCombatType).getDescription()

        # Build the mercenary level and XP strings
        iPlayer = gc.getGame().getActivePlayer()
        unitList = PyPlayer(iPlayer).getUnitList()
        bAlreadyHired = 0
        for pUnit in unitList:
            if pUnit.getMercID() == iMerc:
                pMerc = pUnit
                bAlreadyHired = 1
                break
        if bAlreadyHired == 1:
            strXP = u"%d/%d" % (pMerc.getExperience(), pMerc.experienceNeeded())
            strLevel = str(pMerc.getLevel())

        if lMercList[iMerc][1] == "TXT_KEY_MERC_GENERIC":
            screen.appendListBoxString(
                MERCENARY_INFORMATION_DETAILS_LIST_ID,
                pUnitInfo.getDescription(),
                WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT,
                lMercList[lMerc[0]][0],
                -1,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        else:
            screen.appendListBoxString(
                MERCENARY_INFORMATION_DETAILS_LIST_ID,
                pUnitInfo.getDescription()
                + " ("
                + CyTranslator().getText(lMercList[iMerc][1], ())
                + ")",
                WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT,
                lMercList[lMerc[0]][0],
                -1,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        screen.setImageButton(
            "CombatButtonPanel",
            gc.getUnitCombatInfo(iCombatType).getButton(),
            self.screenWidgetData[MERCENARY_ANIMATION_X]
            + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH]
            + 21,
            self.screenWidgetData[MERCENARY_ANIMATION_Y] + 27,
            28,
            28,
            WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT,
            iCombatType,
            -1,
        )
        screen.appendListBoxString(
            MERCENARY_INFORMATION_DETAILS_LIST_ID,
            "          " + strCombat,
            WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT,
            iCombatType,
            -1,
            CvUtil.FONT_LEFT_JUSTIFY,
        )
        screen.appendListBoxString(
            MERCENARY_INFORMATION_DETAILS_LIST_ID,
            "  " + strStats,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            CvUtil.FONT_LEFT_JUSTIFY,
        )
        screen.appendListBoxString(
            MERCENARY_INFORMATION_DETAILS_LIST_ID,
            "  ",
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            CvUtil.FONT_LEFT_JUSTIFY,
        )
        # screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  Number of promotions: " + str(len(lMerc[1])-1 ), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
        if bAlreadyHired == 0:
            screen.appendListBoxString(
                MERCENARY_INFORMATION_DETAILS_LIST_ID,
                "  Hire Cost: " + strHCost,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        if bAlreadyHired == 1:
            screen.appendListBoxString(
                MERCENARY_INFORMATION_DETAILS_LIST_ID,
                "  Level: " + strLevel + "     XP: " + strXP,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        screen.appendListBoxString(
            MERCENARY_INFORMATION_DETAILS_LIST_ID,
            "  Maintenance Cost: " + strMCost,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            CvUtil.FONT_LEFT_JUSTIFY,
        )

        screen.attachMultiListControlGFC(
            MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_ID,
            MERCENARY_INFORMATION_PROMOTION_LIST_CONTROL_ID,
            "",
            1,
            64,
            64,
            TableStyles.TABLE_STYLE_STANDARD,
        )

        # Add all of the promotions the mercenary has
        lMerc[1].sort()
        for iPromotion in lMerc[1]:
            pPromotionInfo = gc.getPromotionInfo(iPromotion)
            screen.appendMultiListButton(
                MERCENARY_INFORMATION_PROMOTION_LIST_CONTROL_ID,
                pPromotionInfo.getButton(),
                0,
                WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION,
                gc.getInfoTypeForString(pPromotionInfo.getType()),
                -1,
                False,
            )

        screen.addUnitGraphicGFC(
            MERCENARIES_UNIT_GRAPHIC,
            lMercList[lMerc[0]][0],
            self.screenWidgetData[MERCENARY_ANIMATION_X],
            self.screenWidgetData[MERCENARY_ANIMATION_Y],
            self.screenWidgetData[MERCENARY_ANIMATION_WIDTH],
            self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT],
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_X],
            self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_Z],
            self.screenWidgetData[MERCENARY_ANIMATION_SCALE],
            True,
        )

        # 3Miro: Add the provinces
        iPlayer = gc.getGame().getActivePlayer()
        pPlayer = gc.getPlayer(iPlayer)
        szProvinces = localText.getText("TXT_KEY_MERC_AVAILABLE_IN_PROVINCES", ())
        if lMerc[4] > -1:
            sProvName = "TXT_KEY_PROVINCE_NAME_%i" % lMerc[4]
            sProvName = localText.getText(sProvName, ())
            szProvinces = szProvinces + " " + u"<color=0,255,0>%s</color>" % (sProvName)

            # Absinthe: add the money, culture, coastal city and religion prereq texts
            # Absinthe: checks for enough gold
            iGold = pPlayer.getGold()
            iHireCost = lMerc[2]  # it's already modified
            if iGold < iHireCost:
                szProvinces = (
                    szProvinces
                    + "\n"
                    + u"<color=255,0,0>Can't hire them:</color>"
                    + " "
                    + localText.getText("TXT_KEY_MERC_NOT_ENOUGH_MONEY", ())
                )
            # Absinthe: checks if the player has a city with enough culture in the province
            bCulturedEnough = False
            apCityList = PyPlayer(iPlayer).getCityList()
            for pCity in apCityList:
                city = pCity.GetCy()
                if city.getProvince() == lMerc[4] and city.getCultureLevel() >= 2:
                    bCulturedEnough = True
                    break
            if bCulturedEnough is False:
                szProvinces = (
                    szProvinces
                    + "\n"
                    + u"<color=255,0,0>Can't hire them:</color>"
                    + " "
                    + localText.getText("TXT_KEY_MERC_LACK_CULTURE", ())
                )
            # Absinthe: checks if the player has a coastal city in the province
            bHasCoastalCity = True
            iMercType = lMercList[iMerc][0]
            if gc.getUnitInfo(iMercType).getDomainType() == 0:
                bHasCoastalCity = False
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                    city = pCity.GetCy()
                    if city.getProvince() == lMerc[4] and city.isCoastal(1):
                        bHasCoastalCity = True
                        break
            if bHasCoastalCity is False:
                szProvinces = (
                    szProvinces
                    + "\n"
                    + u"<color=255,0,0>Can't hire them:</color>"
                    + " "
                    + localText.getText("TXT_KEY_MERC_NO_PORT", ())
                )
            # Absinthe: checks for the correct religion
            iStateReligion = pPlayer.getStateReligion()
            if iStateReligion in lMercList[iMerc][5]:
                szProvinces = (
                    szProvinces
                    + "\n"
                    + u"<color=255,0,0>Can't hire them:</color>"
                    + " "
                    + localText.getText("TXT_KEY_MERC_WRONG_RELIGION", ())
                )
        else:
            szProvinces = ""

        screen.addMultilineText(
            MERCENARY_INFORMATION_DETAILS_LIST_ID + "PROVTEXT",
            szProvinces,
            (self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X] + 20),
            500,
            500,
            200,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            CvUtil.FONT_LEFT_JUSTIFY,
        )

    # Draws the gold information in the "Mercenary Manager" screens
    def drawGoldInformation(self, screen):

        iCost = 0
        strCost = ""

        # iCost = objMercenaryUtils.getPlayerMercenaryMaintenanceCost(gc.getGame().getActivePlayer())
        pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
        strCost = u"%s %c: %1.2f" % (
            "Mercenary Maintenance",
            gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(),
            0.01 * pPlayer.getPicklefreeParameter(con.iMercCostPerTurn),
        )

        # Get the players current gold text
        szText = self.getGoldText(gc.getGame().getActivePlayer())
        screen.setLabel(
            "GoldText",
            "Background",
            szText,
            CvUtil.FONT_LEFT_JUSTIFY,
            12,
            6,
            -1,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.show("GoldText")
        screen.moveToFront("GoldText")

        screen.setLabel(
            "MaintainText",
            "Background",
            strCost,
            CvUtil.FONT_LEFT_JUSTIFY,
            12,
            24,
            -1,
            FontTypes.GAME_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.show("MaintainText")
        screen.moveToFront("MaintainText")

    # Draws the top bar of the "Mercenary Manager" screens
    def drawScreenTop(self, screen):
        screen.setDimensions(
            0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT]
        )
        screen.addDrawControl(
            BACKGROUND_ID,
            ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(),
            0,
            0,
            self.screenWidgetData[SCREEN_WIDTH],
            self.screenWidgetData[SCREEN_HEIGHT],
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        screen.addDDSGFC(
            BACKGROUND_ID,
            ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(),
            0,
            0,
            self.screenWidgetData[SCREEN_WIDTH],
            self.screenWidgetData[SCREEN_HEIGHT],
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        screen.addPanel(
            SCREEN_TITLE_PANEL_ID,
            u"",
            u"",
            True,
            False,
            self.screenWidgetData[SCREEN_TITLE_PANEL_X],
            self.screenWidgetData[SCREEN_TITLE_PANEL_Y],
            self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH],
            self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_TOPBAR,
        )
        screen.setText(
            SCREEN_TITLE_TEXT_PANEL_ID,
            "Background",
            self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL],
            CvUtil.FONT_CENTER_JUSTIFY,
            self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X],
            self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y],
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        # Draw the gold information for the screen
        self.drawGoldInformation(screen)

    # Draws the bottom bar of the "Mercenary Manager" screens
    def drawScreenBottom(self, screen):
        screen.addPanel(
            BOTTOM_PANEL_ID,
            "",
            "",
            True,
            True,
            self.screenWidgetData[BOTTOM_PANEL_X],
            self.screenWidgetData[BOTTOM_PANEL_Y],
            self.screenWidgetData[BOTTOM_PANEL_WIDTH],
            self.screenWidgetData[BOTTOM_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_BOTTOMBAR,
        )
        screen.setText(
            MERCENARIES_TEXT_PANEL_ID,
            "Background",
            self.screenWidgetData[MERCENARIES_TEXT_PANEL],
            CvUtil.FONT_LEFT_JUSTIFY,
            self.screenWidgetData[MERCENARIES_TEXT_PANEL_X],
            self.screenWidgetData[MERCENARIES_TEXT_PANEL_Y],
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )
        # Commented out due to mercenary groups not being implemented yet.
        # screen.setText(MERCENARY_GROUPS_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL], CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_X], self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        # screen.setText(MERCENARY_CONTRACTS_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL], CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_X], self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        screen.setText(
            EXIT_TEXT_PANEL_ID,
            "Background",
            self.screenWidgetData[EXIT_TEXT_PANEL],
            CvUtil.FONT_RIGHT_JUSTIFY,
            self.screenWidgetData[EXIT_TEXT_PANEL_X],
            self.screenWidgetData[EXIT_TEXT_PANEL_Y],
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_CLOSE_SCREEN,
            -1,
            -1,
        )

    # Draws the mercenary screen content
    def drawMercenaryScreenContent(self, screen):

        # Draw the top bar
        self.drawScreenTop(screen)

        # Draw the bottom bar
        self.drawScreenBottom(screen)

        screen.addPanel(
            AVAILABLE_MERCENARIES_PANEL_ID,
            "",
            "",
            True,
            True,
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X],
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y],
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH],
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.addPanel(
            AVAILABLE_MERCENARIES_INNER_PANEL_ID,
            "",
            "",
            True,
            True,
            self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_X],
            self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_Y],
            self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_WIDTH],
            self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_IN,
        )
        screen.addPanel(
            AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_ID,
            u"",
            u"",
            True,
            False,
            self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X],
            self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_Y],
            self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH],
            self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setText(
            AVAILABLE_MERCENARIES_TEXT_PANEL_ID,
            "Background",
            self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL],
            CvUtil.FONT_CENTER_JUSTIFY,
            self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_X],
            self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_Y],
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        screen.addPanel(
            HIRED_MERCENARIES_PANEL_ID,
            "",
            "",
            True,
            True,
            self.screenWidgetData[HIRED_MERCENARIES_PANEL_X],
            self.screenWidgetData[HIRED_MERCENARIES_PANEL_Y],
            self.screenWidgetData[HIRED_MERCENARIES_PANEL_WIDTH],
            self.screenWidgetData[HIRED_MERCENARIES_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.addPanel(
            HIRED_MERCENARIES_INNER_PANEL_ID,
            "",
            "",
            True,
            True,
            self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_X],
            self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_Y],
            self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_WIDTH],
            self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_IN,
        )
        screen.addPanel(
            HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_ID,
            u"",
            u"",
            True,
            False,
            self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_X],
            self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_Y],
            self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH],
            self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setText(
            HIRED_MERCENARIES_TEXT_PANEL_ID,
            "Background",
            self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL],
            CvUtil.FONT_CENTER_JUSTIFY,
            self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL_X],
            self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL_Y],
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        screen.addPanel(
            MERCENARY_INFORMATION_PANEL_ID,
            "",
            "",
            True,
            True,
            self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X],
            self.screenWidgetData[MERCENARY_INFORMATION_PANEL_Y],
            self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH],
            self.screenWidgetData[MERCENARY_INFORMATION_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.addPanel(
            MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_ID,
            u"",
            u"",
            True,
            False,
            self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X],
            self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_Y],
            self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH],
            self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT],
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.setText(
            MERCENARY_INFORMATION_TEXT_PANEL_ID,
            "Background",
            self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL],
            CvUtil.FONT_CENTER_JUSTIFY,
            self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_X],
            self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_Y],
            self.Z_CONTROLS,
            FontTypes.TITLE_FONT,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
        )

        screen.showWindowBackground(False)

        # Populate the available mercenaries panel
        self.populateAvailableMercenariesPanel(screen)

        # Populate the hired mercenaries panel
        self.populateHiredMercenariesPanel(screen)

    # Returns the new version of the gold text that takes into account the
    # mercenary maintenance cost and contract income
    def getGoldText(self, iPlayer):

        # Get the player
        pPlayer = gc.getPlayer(iPlayer)

        # get the number of cities the player owns
        numCities = pPlayer.getNumCities()

        totalUnitCost = pPlayer.calculateUnitCost()
        totalUnitSupply = pPlayer.calculateUnitSupply()
        totalMaintenance = pPlayer.getTotalMaintenance()
        totalCivicUpkeep = pPlayer.getCivicUpkeep([], False)
        totalPreInflatedCosts = pPlayer.calculatePreInflatedCosts()
        totalInflatedCosts = pPlayer.calculateInflatedCosts()
        # totalMercenaryCost = objMercenaryUtils.getPlayerMercenaryMaintenanceCost(iPlayer)
        totalMercenaryCost = (pPlayer.getPicklefreeParameter(con.iMercCostPerTurn) + 99) / 100
        # totalMercenaryContractIncome = (pPlayer.getPlayerMercenaryContractIncome(iPlayer) + 99) / 100
        # Colony Upkeep
        iColonyNumber = pPlayer.getNumColonies()
        iColonyUpkeep = 0
        if iColonyNumber > 0:
            iColonyUpkeep = int(
                (0.5 * iColonyNumber * iColonyNumber + 0.5 * iColonyNumber) * 3 + 7
            )
        goldCommerce = pPlayer.getCommerceRate(CommerceTypes.COMMERCE_GOLD)
        gold = pPlayer.getGold()

        goldFromCivs = pPlayer.getGoldPerTurn()

        iIncome = 0

        iExpenses = 0

        iIncome = goldCommerce

        if goldFromCivs > 0:
            iIncome += goldFromCivs

        iInflation = totalInflatedCosts - totalPreInflatedCosts

        iExpenses = (
            totalUnitCost
            + totalUnitSupply
            + totalMaintenance
            + totalCivicUpkeep
            + iInflation
            + totalMercenaryCost
            + iColonyUpkeep
        )

        if goldFromCivs < 0:
            iExpenses -= goldFromCivs

        iDelta = iIncome - iExpenses

        # Build the gold string
        strGoldText = u"%c: %d" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(), gold)

        strDelta = ""

        # Set the color for the gold/turn.
        if iDelta > 0:
            strDelta = u"%s" % (
                localText.changeTextColor(
                    " (+" + str(iDelta) + "/Turn)", gc.getInfoTypeForString("COLOR_GREEN")
                )
            )
        elif iDelta < 0:
            strDelta = u"%s" % (
                localText.changeTextColor(
                    " (" + str(iDelta) + "/Turn)", gc.getInfoTypeForString("COLOR_RED")
                )
            )

        return strGoldText + strDelta

    # Hires a mercenary for a player
    def hireMercenary(self, screen, iMerc):

        # Get the active player ID
        iPlayer = gc.getGame().getActivePlayer()

        # Delete the UI representation of the unit from the available mercenaries
        # panel
        # 3Miro: get the Unique internal name
        szUniqueInternalName = "HiredMercID" + self.numToStr(iMerc)
        # screen.deleteWidget(szUniqueInternalName)

        lGlobalMercPool = GMU.getMercGlobalPool()

        for iI in range(len(lGlobalMercPool)):
            if lGlobalMercPool[iI][0] == iMerc:
                lMerc = lGlobalMercPool[iI]

        GMU.hireMerc(lMerc, iPlayer)

        # Draw the gold information for the screen
        self.drawGoldInformation(screen)

        # 3Miro: update hired mercs
        self.clearAvailableMercs(screen)
        self.clearHiredMercs(screen)

        self.populateAvailableMercenariesPanel(screen)
        self.populateHiredMercenariesPanel(screen)

        # Clear the information in the mercenary information panel
        self.clearMercenaryInformation(screen)

    # Fire the mercenary from the player
    def fireMercenary(self, screen, iMerc):

        iPlayer = gc.getGame().getActivePlayer()
        unitList = PyPlayer(iPlayer).getUnitList()

        for pUnit in unitList:
            if pUnit.getMercID() == iMerc:
                # print(" 3Miro: firing: ",iMerc)
                GMU.fireMerc(pUnit)
                screen.deleteWidget(
                    "HiredMercID" + self.numToStr(iMerc)
                )  # it is OK to delete non-existent widgets
                break

        # Draw the gold information for the screen
        self.drawGoldInformation(screen)

        # 3Miro: redraw merc information
        self.clearAvailableMercs(screen)
        self.clearHiredMercs(screen)

        self.populateAvailableMercenariesPanel(screen)
        self.populateHiredMercenariesPanel(screen)

        # Clear the information in the mercenary information panel
        self.clearMercenaryInformation(screen)

    # Handles the input to the mercenary manager screens
    def handleInput(self, inputClass):

        # Get the instance of the screen
        screen = self.getScreen()

        # Debug code - start
        if g_bDebug:
            screen.setText(
                "TopPanelDebugMsg",
                "TopPanel",
                inputClass.getFunctionName(),
                CvUtil.FONT_RIGHT_JUSTIFY,
                1010,
                20,
                -10,
                FontTypes.SMALL_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )
        # Debug code - end

        # Get the data
        theKey = int(inputClass.getData())

        # If the escape key was pressed then set the current screen to mercenary manager
        if inputClass.getNotifyCode() == self.EventKeyDown and theKey == int(InputTypes.KB_ESCAPE):
            self.currentScreen = MERCENARY_MANAGER

        # If the exit text was pressed then set the current screen to mercenary manager.
        if inputClass.getFunctionName() == EXIT_TEXT_PANEL_ID:
            self.currentScreen = MERCENARY_MANAGER

        # If the mercenaries text was pressed and we aren't currently looking at
        # the main mercenaries manager screen then set the current screen to
        # mercenaries manager, hide the screen and redraw the screen.
        if (
            inputClass.getFunctionName() == MERCENARIES_TEXT_PANEL_ID
            and self.currentScreen != MERCENARY_MANAGER
        ):
            self.currentScreen = MERCENARY_MANAGER
            self.hideScreen()
            self.interfaceScreen()
            return

        # If someone pressed one of the buttons in the screen then handle the
        # action
        if inputClass.getFunctionName().endswith("Button"):
            # Split up the function name into the mercenary name and the actual
            # action that was performed
            szUniqueInternalName, function = inputClass.getFunctionName().split("_")

            self.screenFunction = function
            self.mercenaryName = None

            # If the function was find, then close the screen and find the unit
            if function == "FindButton":
                dummy, iMerc = szUniqueInternalName.split("MercID")
                # iMerc = int( iMerc )
                iMerc = self.strToNum(iMerc)
                print("Find mercenary: ", iMerc)

                # Convert the unit ID string back into a number
                # unitID = self.alphaToNumber(unitID)

                # Get the player ID
                iPlayer = gc.getGame().getActivePlayer()

                # Get the actual player reference
                pPlayer = gc.getPlayer(iPlayer)

                # Get the actual unit in the game
                # pUnit = player.getUnit(unitID)
                unitList = PyPlayer(iPlayer).getUnitList()
                for pUnit in unitList:
                    if pUnit.getMercID() == iMerc:
                        print("Mercenary found: ", iMerc, pUnit.getX(), pUnit.getY())
                        pMercUnit = pUnit
                        break

                # If the unit is not set to None then look at them and select them.
                if pMercUnit is not None:
                    # CyCamera().LookAtUnit(pMercUnit)
                    pPlot = gc.getMap().plot(pMercUnit.getX(), pMercUnit.getY())
                    CyCamera().JustLookAtPlot(pPlot)
                    if not CyGame().isNetworkMultiPlayer():
                        CyInterface().selectUnit(pMercUnit, True, False, False)

                self.currentScreen = MERCENARY_MANAGER

                return

            # If the function was hire, then hire the mercenary
            if function == "HireButton":
                dummy, iMerc = szUniqueInternalName.split("MercID")
                iMerc = self.strToNum(iMerc)
                self.hireMercenary(screen, iMerc)

            # If the function was fire, then fire the mercenary
            if function == "FireButton":
                dummy, iMerc = szUniqueInternalName.split("MercID")
                iMerc = self.strToNum(iMerc)
                self.fireMercenary(screen, iMerc)

            # If the function was to show the mercenary information then
            # populate the mercenary information panel.
            if function == "AInfoButton":

                dummy, iMerc = szUniqueInternalName.split("MercID")
                iMerc = self.strToNum(iMerc)
                iPlayer = gc.getGame().getActivePlayer()

                lGlobalMercPool = GMU.getMercGlobalPool()

                for iI in range(len(lGlobalMercPool)):
                    if lGlobalMercPool[iI][0] == iMerc:
                        lMerc = lGlobalMercPool[iI]

                if xml.iPromotionMerc not in lMerc[1]:
                    lMerc[1].append(xml.iPromotionMerc)

                self.calculateScreenWidgetData(screen)

                # Absinthe: we need to make sure this is applied only once
                iModifiedCost = GMU.getModifiedCostPerPlayer(lMerc[2], iPlayer)
                iModifiedUpkeep = GMU.getModifiedCostPerPlayer(lMerc[3], iPlayer)

                lModifiedMerc = [lMerc[0], lMerc[1], iModifiedCost, iModifiedUpkeep, lMerc[4]]

                self.populateMercenaryInformation(screen, lModifiedMerc)

            if function == "HInfoButton":

                dummy, iMerc = szUniqueInternalName.split("MercID")
                iMerc = self.strToNum(iMerc)

                iPlayer = gc.getGame().getActivePlayer()
                unitList = PyPlayer(iPlayer).getUnitList()

                for pUnit in unitList:
                    if pUnit.getMercID() == iMerc:
                        pMerc = pUnit
                        break

                iUpkeepCost = pMerc.getMercUpkeep()

                lPromotionList = []
                # almost all promotions are available through experience, so this is not only for the otherwise used iNumTotalMercPromotions (in Mercenaries.py)
                for iPromotion in range(
                    xml.iNumPromotions - 1
                ):  # merc promotion is added separately
                    if pMerc.isHasPromotion(iPromotion):
                        lPromotionList.append(iPromotion)

                if xml.iPromotionMerc not in lPromotionList:
                    lPromotionList.append(xml.iPromotionMerc)

                lMerc = [iMerc, lPromotionList, 0, iUpkeepCost, -1]

                self.calculateScreenWidgetData(screen)
                self.populateMercenaryInformation(screen, lMerc)

                # self.mercenaryName = mercenaryName

                ## If the mercenary name was actually set then get their
                ## information from the global mercenary pool.
                # if(mercenaryName != None):

                ## Get the mercenary from the global mercenary pool
                # mercenary = objMercenaryUtils.getMercenary(mercenaryName)

                ## If we couldn't get the mercenary information try to get it
                ## from the player's mercenary pool.
                # if(mercenary == None):
                # mercenary = objMercenaryUtils.getPlayerMercenary(mercenaryName,gc.getGame().getActivePlayer())

                ## Return immediately if we still couldn't get the mercenary information
                # if(mercenary == None):
                # return

                ## Calculate the screen information
                ### Calculate the screen information
                # self.calculateScreenWidgetData(screen)

                ## Populate the mercenary information panel
                # self.populateMercenaryInformation(screen, mercenary)

        return 0

    # returns a unique ID for a widget in this screen
    def getNextWidgetName(self):
        szName = self.WIDGET_ID + str(self.nWidgetCount)
        self.nWidgetCount += 1
        return szName

    def update(self, fDelta):
        screen = self.getScreen()

    # Calculates the screens widgets positions, dimensions, text, etc.
    def calculateScreenWidgetData(self, screen):
        "Calculates the screens widgets positions, dimensions, text, etc."

        # The border width should not be a hard coded number
        self.screenWidgetData[BORDER_WIDTH] = 4

        self.screenWidgetData[SCREEN_WIDTH] = screen.getXResolution()
        self.screenWidgetData[SCREEN_HEIGHT] = screen.getYResolution()

        strScreenTitle = ""

        if self.currentScreen == MERCENARY_MANAGER:
            strScreenTitle = localText.getText("TXT_KEY_MERCENARY_SCREEN_TITLE", ()).upper()
        elif self.currentScreen == MERCENARY_GROUPS_MANAGER:
            strScreenTitle = localText.getText("TXT_KEY_MERCENARY_GROUPS_SCREEN_TITLE", ()).upper()
        elif self.currentScreen == MERCENARY_CONTRACT_MANAGER:
            strScreenTitle = localText.getText(
                "TXT_KEY_MERCENARY_CONTRACTS_SCREEN_TITLE", ()
            ).upper()

        # Screen title panel information
        self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
        self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] = 55
        self.screenWidgetData[SCREEN_TITLE_PANEL_X] = 0
        self.screenWidgetData[SCREEN_TITLE_PANEL_Y] = 0
        self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL] = (
            u"<font=4b>"
            + localText.getText("TXT_KEY_MERCENARIES_SCREEN_TITLE", ()).upper()
            + ": "
            + strScreenTitle
            + "</font>"
        )
        self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] / 2
        self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y] = 8

        # Exit panel information
        self.screenWidgetData[BOTTOM_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
        self.screenWidgetData[BOTTOM_PANEL_HEIGHT] = 55
        self.screenWidgetData[BOTTOM_PANEL_X] = 0
        self.screenWidgetData[BOTTOM_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 55

        self.screenWidgetData[MERCENARIES_TEXT_PANEL] = (
            u"<font=4>"
            + localText.getText("TXT_KEY_MERCENARY_SCREEN_TITLE", ()).upper()
            + "</font>"
        )
        self.screenWidgetData[MERCENARIES_TEXT_PANEL_X] = 30
        self.screenWidgetData[MERCENARIES_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

        self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL] = (
            u"<font=4>"
            + localText.getText("TXT_KEY_MERCENARY_GROUPS_SCREEN_TITLE", ()).upper()
            + "</font>"
        )
        self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_X] = 220
        self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_Y] = (
            self.screenWidgetData[SCREEN_HEIGHT] - 42
        )

        self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL] = (
            u"<font=4>"
            + localText.getText("TXT_KEY_MERCENARY_CONTRACTS_SCREEN_TITLE", ()).upper()
            + "</font>"
        )
        # Commented out since mercenary groups are not being implemented in the v0.5 release of the mod.
        # self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_X] = 485
        self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_X] = 220
        self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_Y] = (
            self.screenWidgetData[SCREEN_HEIGHT] - 42
        )

        self.screenWidgetData[EXIT_TEXT_PANEL] = (
            u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
        )
        self.screenWidgetData[EXIT_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] - 30
        self.screenWidgetData[EXIT_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

        # Available mercenaries panel information
        self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
        self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y] = (
            self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] = 550
        self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT] = (
            self.screenWidgetData[SCREEN_HEIGHT]
            - (
                (self.screenWidgetData[BORDER_WIDTH] * 3)
                + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT]
                + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]
            )
        ) / 2
        self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_X] = self.screenWidgetData[
            AVAILABLE_MERCENARIES_PANEL_X
        ] + (4 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_Y] = self.screenWidgetData[
            AVAILABLE_MERCENARIES_PANEL_Y
        ] + (10 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_WIDTH] = self.screenWidgetData[
            AVAILABLE_MERCENARIES_PANEL_WIDTH
        ] - (8 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_HEIGHT] = self.screenWidgetData[
            AVAILABLE_MERCENARIES_PANEL_HEIGHT
        ] - (14 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X] = (
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] = (
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y]
            + self.screenWidgetData[BORDER_WIDTH]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[
            AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH
        ] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] - (
            self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
        self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL] = (
            "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_MERCENARIES", ()) + "</font>"
        )
        self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_X] = self.screenWidgetData[
            AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X
        ] + (self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH] / 2)
        self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_Y] = (
            self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] + 4
        )

        # Hired mercenaries panel information
        self.screenWidgetData[HIRED_MERCENARIES_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
        self.screenWidgetData[HIRED_MERCENARIES_PANEL_Y] = (
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y]
            + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[HIRED_MERCENARIES_PANEL_WIDTH] = 550
        self.screenWidgetData[HIRED_MERCENARIES_PANEL_HEIGHT] = (
            self.screenWidgetData[SCREEN_HEIGHT]
            - (
                (self.screenWidgetData[BORDER_WIDTH] * 3)
                + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT]
                + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]
            )
        ) / 2
        self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_X] = self.screenWidgetData[
            HIRED_MERCENARIES_PANEL_X
        ] + (4 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_Y] = self.screenWidgetData[
            HIRED_MERCENARIES_PANEL_Y
        ] + (10 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_WIDTH] = self.screenWidgetData[
            HIRED_MERCENARIES_PANEL_WIDTH
        ] - (8 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_HEIGHT] = self.screenWidgetData[
            HIRED_MERCENARIES_PANEL_HEIGHT
        ] - (14 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_X] = (
            self.screenWidgetData[HIRED_MERCENARIES_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[
            HIRED_MERCENARIES_PANEL_Y
        ] + (self.screenWidgetData[BORDER_WIDTH] * 2)
        self.screenWidgetData[
            HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH
        ] = self.screenWidgetData[HIRED_MERCENARIES_PANEL_WIDTH] - (
            self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_X]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
        self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL] = (
            "<font=3b>" + localText.getText("TXT_KEY_HIRED_MERCENARIES", ()) + "</font>"
        )
        self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL_X] = self.screenWidgetData[
            HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_X
        ] + (self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH] / 2)
        self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL_Y] = (
            self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] + 4
        )

        # Mercenary information panel information
        self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X] = (
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X]
            + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[MERCENARY_INFORMATION_PANEL_Y] = (
            self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[
            SCREEN_WIDTH
        ] - (
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X]
            + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[MERCENARY_INFORMATION_PANEL_HEIGHT] = self.screenWidgetData[
            SCREEN_HEIGHT
        ] - (
            (self.screenWidgetData[BORDER_WIDTH] * 2)
            + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT]
            + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]
        )
        self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X] = (
            self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = (
            self.screenWidgetData[MERCENARY_INFORMATION_PANEL_Y]
            + self.screenWidgetData[BORDER_WIDTH]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[
            MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH
        ] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] - (
            self.screenWidgetData[BORDER_WIDTH] * 6
        )
        self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
        self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL] = (
            "<font=3b>" + localText.getText("TXT_KEY_MERCENARY_INFORMATION", ()) + "</font>"
        )
        self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[
            MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X
        ] + (self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] / 2)
        self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_Y] = (
            self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4
        )

        self.screenWidgetData[MERCENARY_ANIMATION_X] = (
            self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X] + 20
        )
        self.screenWidgetData[MERCENARY_ANIMATION_Y] = (
            self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_Y] + 40
        )
        self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] = 303
        self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT] = 200
        self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_X] = -20
        self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_Z] = 30
        self.screenWidgetData[MERCENARY_ANIMATION_SCALE] = 0.84

        self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[
            MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X
        ]
        self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] = (
            self.screenWidgetData[MERCENARY_ANIMATION_Y]
            + self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[
            MERCENARY_INFORMATION_PANEL_WIDTH
        ] - (self.screenWidgetData[BORDER_WIDTH] * 6)
        self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (
            self.screenWidgetData[BORDER_WIDTH] * 9
        )

        self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_X] = (
            self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_Y] = (
            self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[
            MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_WIDTH
        ] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] + (
            self.screenWidgetData[BORDER_WIDTH] * 2
        )
        self.screenWidgetData[
            MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT
        ] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] - (
            self.screenWidgetData[BORDER_WIDTH] * 2
        )

        self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_X] = (
            self.screenWidgetData[MERCENARY_ANIMATION_X]
            + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[
            MERCENARY_ANIMATION_Y
        ]
        self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[
            SCREEN_WIDTH
        ] - (
            self.screenWidgetData[MERCENARY_ANIMATION_X]
            + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH]) * 6
        )
        self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[
            MERCENARY_ANIMATION_HEIGHT
        ]

        # Units contracted out panel information
        self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
        self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y] = (
            self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] = 450
        self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_HEIGHT] = (
            self.screenWidgetData[SCREEN_HEIGHT]
            - (
                (self.screenWidgetData[BORDER_WIDTH] * 3)
                + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT]
                + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]
            )
        ) / 2
        self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_X] = self.screenWidgetData[
            UNITS_CONTRACTED_OUT_PANEL_X
        ] + (4 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_Y] = self.screenWidgetData[
            UNITS_CONTRACTED_OUT_PANEL_Y
        ] + (10 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_WIDTH] = self.screenWidgetData[
            UNITS_CONTRACTED_OUT_PANEL_WIDTH
        ] - (8 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_HEIGHT] = self.screenWidgetData[
            UNITS_CONTRACTED_OUT_PANEL_HEIGHT
        ] - (14 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X] = (
            self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_Y] = (
            self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y]
            + self.screenWidgetData[BORDER_WIDTH]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[
            UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_WIDTH
        ] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] - (
            self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
        self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL] = (
            "<font=3b>" + localText.getText("TXT_KEY_UNITS_CONTRACTED_OUT", ()) + "</font>"
        )
        self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL_X] = self.screenWidgetData[
            UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X
        ] + (self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_WIDTH] / 2)
        self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL_Y] = (
            self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_Y] + 4
        )

        # Available units panel information
        self.screenWidgetData[AVAILABLE_UNITS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
        self.screenWidgetData[AVAILABLE_UNITS_PANEL_Y] = (
            self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y]
            + self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_HEIGHT]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[AVAILABLE_UNITS_PANEL_WIDTH] = 450
        self.screenWidgetData[AVAILABLE_UNITS_PANEL_HEIGHT] = (
            self.screenWidgetData[SCREEN_HEIGHT]
            - (
                (self.screenWidgetData[BORDER_WIDTH] * 3)
                + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT]
                + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]
            )
        ) / 2
        self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_X] = self.screenWidgetData[
            AVAILABLE_UNITS_PANEL_X
        ] + (4 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_Y] = self.screenWidgetData[
            AVAILABLE_UNITS_PANEL_Y
        ] + (10 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_WIDTH] = self.screenWidgetData[
            AVAILABLE_UNITS_PANEL_WIDTH
        ] - (8 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_HEIGHT] = self.screenWidgetData[
            AVAILABLE_UNITS_PANEL_HEIGHT
        ] - (14 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X] = (
            self.screenWidgetData[AVAILABLE_UNITS_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[
            AVAILABLE_UNITS_PANEL_Y
        ] + (self.screenWidgetData[BORDER_WIDTH] * 2)
        self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[
            AVAILABLE_UNITS_PANEL_WIDTH
        ] - (
            self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
        self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL] = (
            "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_UNITS", ()) + "</font>"
        )
        self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL_X] = self.screenWidgetData[
            AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X
        ] + (self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_WIDTH] / 2)
        self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL_Y] = (
            self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_Y] + 4
        )

        # Unit information panel information
        self.screenWidgetData[UNIT_INFORMATION_PANEL_X] = (
            self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X]
            + self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[UNIT_INFORMATION_PANEL_Y] = (
            self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[
            SCREEN_WIDTH
        ] - (
            self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X]
            + self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[UNIT_INFORMATION_PANEL_HEIGHT] = self.screenWidgetData[
            SCREEN_HEIGHT
        ] - (
            (self.screenWidgetData[BORDER_WIDTH] * 2)
            + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT]
            + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]
        )
        self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X] = (
            self.screenWidgetData[UNIT_INFORMATION_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = (
            self.screenWidgetData[UNIT_INFORMATION_PANEL_Y]
            + self.screenWidgetData[BORDER_WIDTH]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[
            UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH
        ] = self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] - (
            self.screenWidgetData[BORDER_WIDTH] * 6
        )
        self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
        self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL] = (
            "<font=3b>" + localText.getText("TXT_KEY_UNIT_INFORMATION", ()) + "</font>"
        )
        self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[
            UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X
        ] + (self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] / 2)
        self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y] = (
            self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4
        )

        self.screenWidgetData[UNIT_ANIMATION_X] = (
            self.screenWidgetData[UNIT_INFORMATION_PANEL_X] + 20
        )
        self.screenWidgetData[UNIT_ANIMATION_Y] = (
            self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y] + 40
        )
        self.screenWidgetData[UNIT_ANIMATION_WIDTH] = 303
        self.screenWidgetData[UNIT_ANIMATION_HEIGHT] = 200
        self.screenWidgetData[UNIT_ANIMATION_ROTATION_X] = -20
        self.screenWidgetData[UNIT_ANIMATION_ROTATION_Z] = 30
        self.screenWidgetData[UNIT_ANIMATION_SCALE] = 1.0

        self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[
            UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X
        ]
        self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y] = (
            self.screenWidgetData[UNIT_ANIMATION_Y]
            + self.screenWidgetData[UNIT_ANIMATION_HEIGHT]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[
            UNIT_INFORMATION_PANEL_WIDTH
        ] - (self.screenWidgetData[BORDER_WIDTH] * 18)
        self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (
            self.screenWidgetData[BORDER_WIDTH] * 9
        )

        self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_X] = (
            self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_Y] = (
            self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[
            UNIT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH
        ] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH] + (
            self.screenWidgetData[BORDER_WIDTH] * 2
        )
        self.screenWidgetData[
            UNIT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT
        ] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT] - (
            self.screenWidgetData[BORDER_WIDTH] * 2
        )

        self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_X] = (
            self.screenWidgetData[UNIT_ANIMATION_X]
            + self.screenWidgetData[UNIT_ANIMATION_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[
            UNIT_ANIMATION_Y
        ]
        self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[
            SCREEN_WIDTH
        ] - (
            self.screenWidgetData[UNIT_ANIMATION_X]
            + self.screenWidgetData[UNIT_ANIMATION_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH]) * 6
        )
        self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[
            UNIT_ANIMATION_HEIGHT
        ]
        self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[
            MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X
        ]
        self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] = (
            self.screenWidgetData[MERCENARY_ANIMATION_Y]
            + self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[
            MERCENARY_INFORMATION_PANEL_WIDTH
        ] - (self.screenWidgetData[BORDER_WIDTH] * 6)
        self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (
            self.screenWidgetData[BORDER_WIDTH] * 9
        )

        self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_X] = (
            self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_Y] = (
            self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[
            MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_WIDTH
        ] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] + (
            self.screenWidgetData[BORDER_WIDTH] * 2
        )
        self.screenWidgetData[
            MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT
        ] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] - (
            self.screenWidgetData[BORDER_WIDTH] * 2
        )

        self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_X] = (
            self.screenWidgetData[MERCENARY_ANIMATION_X]
            + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[
            MERCENARY_ANIMATION_Y
        ]
        self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[
            SCREEN_WIDTH
        ] - (
            self.screenWidgetData[MERCENARY_ANIMATION_X]
            + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH]) * 6
        )
        self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[
            MERCENARY_ANIMATION_HEIGHT
        ]

        # Available mercenary groups panel information
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X] = self.screenWidgetData[
            BORDER_WIDTH
        ]
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] = (
            self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH] = 450
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT] = (
            self.screenWidgetData[SCREEN_HEIGHT]
            - (
                (self.screenWidgetData[BORDER_WIDTH] * 3)
                + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT]
                + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]
            )
        ) / 2
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_X] = self.screenWidgetData[
            AVAILABLE_MERCENARY_GROUPS_PANEL_X
        ] + (4 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_Y] = self.screenWidgetData[
            AVAILABLE_MERCENARY_GROUPS_PANEL_Y
        ] + (10 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[
            AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_WIDTH
        ] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH] - (
            8 * self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[
            AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_HEIGHT
        ] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT] - (
            14 * self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] = (
            self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[
            AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y
        ] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] + (
            self.screenWidgetData[BORDER_WIDTH] * 2
        )
        self.screenWidgetData[
            AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH
        ] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH] - (
            self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL] = (
            "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_MERCENARY_GROUPS", ()) + "</font>"
        )
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_X] = self.screenWidgetData[
            AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X
        ] + (self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH] / 2)
        self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_Y] = (
            self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] + 4
        )

        # Hired mercenary groups panel information
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y] = (
            self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y]
            + self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH] = 450
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_HEIGHT] = (
            self.screenWidgetData[SCREEN_HEIGHT]
            - (
                (self.screenWidgetData[BORDER_WIDTH] * 3)
                + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT]
                + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]
            )
        ) / 2
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_X] = self.screenWidgetData[
            HIRED_MERCENARY_GROUPS_PANEL_X
        ] + (4 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_Y] = self.screenWidgetData[
            HIRED_MERCENARY_GROUPS_PANEL_Y
        ] + (10 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_WIDTH] = self.screenWidgetData[
            HIRED_MERCENARY_GROUPS_PANEL_WIDTH
        ] - (8 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_HEIGHT] = self.screenWidgetData[
            HIRED_MERCENARY_GROUPS_PANEL_HEIGHT
        ] - (14 * self.screenWidgetData[BORDER_WIDTH])
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] = (
            self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[
            HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y
        ] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y] + (
            self.screenWidgetData[BORDER_WIDTH] * 2
        )
        self.screenWidgetData[
            HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH
        ] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH] - (
            self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL] = (
            "<font=3b>" + localText.getText("TXT_KEY_HIRED_MERCENARY_GROUPS", ()) + "</font>"
        )
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_X] = self.screenWidgetData[
            HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X
        ] + (self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH] / 2)
        self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_Y] = (
            self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] + 4
        )

        # Mercenary groups information panel information
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_X] = (
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X]
            + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_Y] = (
            self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[
            SCREEN_WIDTH
        ] - (
            self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X]
            + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_HEIGHT] = self.screenWidgetData[
            SCREEN_HEIGHT
        ] - (
            (self.screenWidgetData[BORDER_WIDTH] * 2)
            + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT]
            + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]
        )
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_X] = (
            self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_X]
            + self.screenWidgetData[BORDER_WIDTH]
            + (self.screenWidgetData[BORDER_WIDTH] * 2)
        )
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = (
            self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_Y]
            + self.screenWidgetData[BORDER_WIDTH]
            + self.screenWidgetData[BORDER_WIDTH]
        )
        self.screenWidgetData[
            MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH
        ] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_WIDTH] - (
            self.screenWidgetData[BORDER_WIDTH] * 6
        )
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL] = (
            "<font=3b>" + localText.getText("TXT_KEY_MERCENARY_GROUP_INFORMATION", ()) + "</font>"
        )
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[
            MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_X
        ] + (self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] / 2)
        self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_Y] = (
            self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4
        )

    # Converts a number into its string representation. This is needed since
    # for whatever reason, numbers did not work very well when using them
    # for all of the different panels in the mercenary manager screen. The
    # unit ID number 382343 is converted to: CHBCDC.
    def numberToAlpha(self, iNum):
        # 			  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26
        alphaList = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        strNum = str(iNum)
        strAlpha = ""

        # Go though the alphaList and convert the numbers to letters
        for i in range(len(strNum)):
            strAlpha = strAlpha + alphaList[int(strNum[i])]

        return strAlpha

    # Converts a number into its string representation. This is needed since
    # for whatever reason, numbers did not work very well when using them
    # for all of the different panels in the mercenary manager screen. The
    # string "CHBCDC" is converted to: 382343.
    def alphaToNumber(self, strAlpha):
        # 			  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26
        alphaList = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]

        strNum = ""

        # Go though the alphaList and convert the letters to numbers
        for i in range(len(strAlpha)):
            strNum = strNum + str(alphaList.index(strAlpha[i]))

        return int(strNum)

    # 3Miro: a bit more efficient version of the above two functions
    # the different panels don't work with numbers, replace the numbers 0 - 9 with A - J
    def strToNum(self, szStr):

        CharacterMap = {
            "A": "0",
            "B": "1",
            "C": "2",
            "D": "3",
            "E": "4",
            "F": "5",
            "G": "6",
            "H": "7",
            "I": "8",
            "J": "9",
        }

        szNum = ""
        for iI in range(len(szStr)):
            szNum = szNum + CharacterMap[szStr[iI]]

        return int(szNum)

    def numToStr(self, iNum):
        szNum = "%d" % iNum
        CharacterMap = {
            "0": "A",
            "1": "B",
            "2": "C",
            "3": "D",
            "4": "E",
            "5": "F",
            "6": "G",
            "7": "H",
            "8": "I",
            "9": "J",
        }

        szResult = ""
        for iI in range(len(szNum)):
            szResult = szResult + CharacterMap[szNum[iI]]

        return szResult
