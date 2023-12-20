## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
from CoreData import civilizations
import CvUtil
import CvScreensInterface
import CvEventInterface
import CvScreenEnums
import Popup as PyPopup
from CoreFunctions import text

# Caliom RFCE imports
import MapUtils

# Caliom globals
CITY_NAME_POPUP_EVENT_ID = MapUtils.getNewEventID()
RESTORE_LANDMARKS_POPUP_EVENT_ID = MapUtils.getNewEventID()
MapManager = MapUtils.MapManager
MapVisualizer = MapUtils.MapVisualizer

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()


class CvWorldBuilderScreen:
    "World Builder Screen"

    def __init__(self):
        self.m_advancedStartTabCtrl = None
        self.m_normalPlayerTabCtrl = 0
        self.m_normalMapTabCtrl = 0
        self.m_tabCtrlEdit = 0
        self.m_flyoutMenu = 0
        self.m_bCtrlEditUp = False
        self.m_bUnitEdit = False
        self.m_bCityEdit = False
        self.m_bNormalPlayer = True
        self.m_bNormalMap = False
        self.m_bReveal = False
        self.m_bDiplomacy = False
        self.m_bLandmark = False
        self.m_bEraseAll = False
        self.m_bUnitEditCtrl = False
        self.m_bCityEditCtrl = False
        self.m_bShowBigBrush = False
        self.m_bLeftMouseDown = False
        self.m_bRightMouseDown = False
        self.m_bChangeFocus = False
        self.m_iNormalPlayerCurrentIndexes = []
        self.m_iNormalMapCurrentIndexes = []
        self.m_iNormalMapCurrentList = []
        self.m_iAdvancedStartCurrentIndexes = []
        self.m_iAdvancedStartCurrentList = []
        self.m_iCurrentPlayer = 0
        self.m_iCurrentTeam = 0
        self.m_iCurrentUnitPlayer = 0
        self.m_iCurrentUnit = 0
        self.m_iCurrentX = -1
        self.m_iCurrentY = -1
        self.m_pCurrentPlot = 0
        self.m_pActivePlot = 0
        self.m_pRiverStartPlot = -1

        self.m_iUnitTabID = -1
        self.m_iBuildingTabID = -1
        self.m_iTechnologyTabID = -1
        self.m_iImprovementTabID = -1
        self.m_iBonusTabID = -1
        self.m_iImprovementListID = -1
        self.m_iBonusListID = -1
        self.m_iTerrainTabID = -1
        self.m_iTerrainListID = -1
        self.m_iFeatureListID = -1
        self.m_iPlotTypeListID = -1
        self.m_iRouteListID = -1
        self.m_iTerritoryTabID = -1
        self.m_iTerritoryListID = -1

        self.m_iASUnitTabID = -1
        self.m_iASUnitListID = -1
        self.m_iASCityTabID = -1
        self.m_iASCityListID = -1
        self.m_iASBuildingsListID = -1
        self.m_iASAutomateListID = -1
        self.m_iASImprovementsTabID = -1
        self.m_iASRoutesListID = -1
        self.m_iASImprovementsListID = -1
        self.m_iASVisibilityTabID = -1
        self.m_iASVisibilityListID = -1
        self.m_iASTechTabID = -1
        self.m_iASTechListID = -1

        self.m_iBrushSizeTabID = -1
        self.m_iBrushWidth = 1
        self.m_iBrushHeight = 1
        self.m_iFlyoutEditUnit = 1
        self.m_iFlyoutEditCity = 0
        self.m_iFlyoutAddScript = -1
        self.m_iFlyoutChangeStartYear = -2
        self.m_pFlyoutPlot = 0
        self.m_bFlyout = False
        self.m_pUnitToScript = -1
        self.m_pCityToScript = -1
        self.m_pPlotToScript = -1
        self.m_iUnitEditCheckboxID = -1
        self.m_iCityEditCheckboxID = -1
        self.m_iNormalPlayerCheckboxID = -1
        self.m_iNormalMapCheckboxID = -1
        self.m_iRevealTileCheckboxID = -1
        self.m_iDiplomacyCheckboxID = -1
        self.m_iLandmarkCheckboxID = -1
        self.m_iEraseCheckboxID = -1
        self.iScreenWidth = 228

        self.m_bSideMenuDirty = False
        self.m_bASItemCostDirty = False
        self.m_iCost = 0

        self.revealMode = RevealMode(self)  # Caliom
        self.landmarkMode = LandmarkMode(self)  # Caliom
        self.currentMode = None  # Caliom
        return

    def interfaceScreen(self):
        # This is the main interface screen, create it as such

        # Caliom begin
        if self.currentMode is not None:
            self.currentMode.activate()
            return
        # Caliom end

        self.initVars()
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        screen.setCloseOnEscape(False)
        screen.setAlwaysShown(True)

        self.setSideMenu()
        self.refreshSideMenu()

        # add interface items
        self.refreshPlayerTabCtrl()

        self.refreshAdvancedStartTabCtrl(False)

        if CyInterface().isInAdvancedStart():
            pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
            pPlot = pPlayer.getStartingPlot()
            CyCamera().JustLookAtPlot(pPlot)

        self.m_normalMapTabCtrl = getWBToolNormalMapTabCtrl()

        self.m_normalMapTabCtrl.setNumColumns((gc.getNumBonusInfos() / 10) + 1)
        self.m_normalMapTabCtrl.addTabSection(text("TXT_KEY_WB_IMPROVEMENTS"))
        self.m_iImprovementTabID = 0
        self.m_iNormalMapCurrentIndexes.append(0)

        self.m_iNormalMapCurrentList.append(0)
        self.m_iImprovementListID = 0

        self.m_normalMapTabCtrl.addTabSection(text("TXT_KEY_WB_BONUSES"))
        self.m_iBonusTabID = 1
        self.m_iNormalMapCurrentIndexes.append(0)

        self.m_iNormalMapCurrentList.append(0)
        self.m_iBonusListID = 0

        self.m_normalMapTabCtrl.setNumColumns((gc.getNumTerrainInfos() / 10) + 1)
        self.m_normalMapTabCtrl.addTabSection(text("TXT_KEY_WB_TERRAINS"))
        self.m_iTerrainTabID = 2
        self.m_iNormalMapCurrentIndexes.append(0)

        self.m_iNormalMapCurrentList.append(0)
        self.m_iTerrainListID = 0
        self.m_iPlotTypeListID = 1
        self.m_iFeatureListID = 2
        self.m_iRouteListID = 3

        # Territory

        self.m_normalMapTabCtrl.setNumColumns(8)
        self.m_normalMapTabCtrl.addTabSection(text("TXT_KEY_WB_TERRITORY"))
        self.m_iTerritoryTabID = 3
        self.m_iNormalMapCurrentIndexes.append(0)

        self.m_iNormalMapCurrentList.append(0)
        self.m_iTerritoryListID = 0

        # This should be a forced redraw screen
        screen.setForcedRedraw(True)

        screen.setDimensions(0, 0, screen.getXResolution(), screen.getYResolution())
        # This should show the screen immidiately and pass input to the game
        screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)

        setWBInitialCtrlTabPlacement()

        MapManager.initMaps()  # Caliom
        return 0

    def killScreen(self):
        # Caliom begin
        if self.currentMode is not None:
            self.currentMode.deactivate()
            self.currentMode = None
        # Caliom end

        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.destroy()
            self.m_tabCtrlEdit = 0

        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        screen.hideScreen()
        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)

        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)
        CvScreensInterface.hideWorldBuilderDiplomacyScreen()

    def handleInput(self, inputClass):
        if (
            (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED)
            and inputClass.isShiftKeyDown()
            and inputClass.isCtrlKeyDown()
        ):
            return 1
        elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER:
            key = inputClass.getData()
            if key == int(InputTypes.KB_ESCAPE):
                if self.m_bDiplomacy:
                    self.normalPlayerTabModeCB()
                return 1
        elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:

            if self.currentMode is not None:
                screen = CyGInterfaceScreen(
                    "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN
                )
                name = inputClass.getFunctionName()
                index = int(inputClass.getData())
                value = screen.getPullDownType(name, index)

                return self.currentMode.handleDropdown(name, index, value)

            if inputClass.getFunctionName() == "WorldBuilderPlayerChoice":
                self.handlePlayerUnitPullDownCB(inputClass.getData())
            elif inputClass.getFunctionName() == "WorldBuilderTechByEra":
                self.handleWorldBuilderTechByEraPullDownCB(inputClass.getData())
            elif inputClass.getFunctionName() == "WorldBuilderBrushSize":
                self.handleBrushHeightCB(inputClass.getData())
                self.handleBrushWidthCB(inputClass.getData())
            elif inputClass.getFunctionName() == "WorldBuilderTeamChoice":
                self.handleSelectTeamPullDownCB(inputClass.getData())
        return 1

    def mouseOverPlot(self, argsList):

        if self.currentMode is not None:
            self.m_pCurrentPlot = CyInterface().getMouseOverPlot()

            self.currentMode.mouseOverPlot(self.m_pCurrentPlot, argsList)

            if CyInterface().isLeftMouseDown() and self.m_bLeftMouseDown:
                self.currentMode.leftMouseDown(self.m_pCurrentPlot, argsList)
            elif CyInterface().isRightMouseDown() and self.m_bRightMouseDown:
                self.currentMode.rightMouseDown(self.m_pCurrentPlot, argsList)

        elif self.m_bReveal:
            self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
            if CyInterface().isLeftMouseDown() and self.m_bLeftMouseDown:
                self.setMultipleReveal(True)
            elif CyInterface().isRightMouseDown() and self.m_bRightMouseDown:
                self.setMultipleReveal(False)
        else:  # if ((self.m_tabCtrlEdit == 0) or (not self.m_tabCtrlEdit.isEnabled())):
            self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
            self.m_iCurrentX = self.m_pCurrentPlot.getX()
            self.m_iCurrentY = self.m_pCurrentPlot.getY()
            if CyInterface().isLeftMouseDown() and self.m_bLeftMouseDown:
                if self.useLargeBrush():
                    self.placeMultipleObjects()
                else:
                    self.placeObject()
            elif CyInterface().isRightMouseDown() and self.m_bRightMouseDown:
                if not (self.m_bCityEdit or self.m_bUnitEdit):
                    if self.useLargeBrush():
                        self.removeMultipleObjects()
                    else:
                        self.removeObject()
        return

    def getHighlightPlot(self, argsList):

        if self.currentMode is not None and not self.currentMode.isHighlightPlot():
            return []

        self.refreshASItemCost()

        if self.m_pCurrentPlot != 0:
            # 			if (CyInterface().isInAdvancedStart() and self.m_pCurrentPlot.isAdjacentNonrevealed(CyGame().getActiveTeam())):
            # 				if (self.getASActiveVisibility() == -1):
            # 					return []
            if CyInterface().isInAdvancedStart():
                if self.m_iCost <= 0:
                    return []

        if (
            (self.m_pCurrentPlot != 0)
            and not self.m_bShowBigBrush
            and not self.m_bDiplomacy
            and isMouseOverGameSurface()
        ):
            return (self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY())

        return []

    def leftMouseDown(self, argsList):
        bShift, bCtrl, bAlt = argsList
        self.m_bLeftMouseDown = True

        if self.currentMode is not None:
            self.currentMode.leftMouseDown(self.m_pCurrentPlot, argsList)
            return

        if CyInterface().isInAdvancedStart():
            self.placeObject()
            return 1

        if (bAlt and bCtrl) or (self.m_bUnitEdit):
            if self.m_pCurrentPlot.getNumUnits() > 0:
                self.m_iCurrentUnit = 0
                self.setUnitEditInfo(False)
            return 1
        elif (bCtrl) or (self.m_bCityEdit):
            if self.m_pCurrentPlot.isCity():
                self.initCityEditScreen()
            return 1
        elif self.m_bReveal:
            if self.m_pCurrentPlot != 0:
                self.setMultipleReveal(True)
        elif bShift and not bCtrl and not bAlt:
            self.createFlyoutMenu()
            return 1

        if self.useLargeBrush():
            self.placeMultipleObjects()
        else:
            self.placeObject()
        return 1

    def rightMouseDown(self, argsList):
        self.m_bRightMouseDown = True

        if self.currentMode is not None:
            self.currentMode.rightMouseDown(self.m_pCurrentPlot, argsList)
            return

        if CyInterface().isInAdvancedStart():
            self.removeObject()
            return 1

        if self.m_bCityEdit or self.m_bUnitEdit:
            self.createFlyoutMenu()
        elif self.m_bReveal:
            if self.m_pCurrentPlot != 0:
                self.setMultipleReveal(False)
        else:
            if self.useLargeBrush():
                self.removeMultipleObjects()
            else:
                self.removeObject()

        return 1

    def rightMouseUp(self):
        if self.currentMode is not None:
            self.currentMode.rightMouseUp(self.m_pCurrentPlot)
        return

    def leftMouseUp(self):
        if self.currentMode is not None:
            self.currentMode.leftMouseUp(self.m_pCurrentPlot)
        return

    def update(self, fDelta):
        if not CyInterface().isLeftMouseDown():
            if self.m_bLeftMouseDown:
                self.leftMouseUp()
            self.m_bLeftMouseDown = False
        if not CyInterface().isRightMouseDown():
            if self.m_bRightMouseDown:
                self.rightMouseUp()
            self.m_bRightMouseDown = False

        if (not self.m_bChangeFocus) and (not isMouseOverGameSurface()):
            self.m_bChangeFocus = True

        if (
            self.m_bChangeFocus
            and isMouseOverGameSurface()
            and (not self.m_bUnitEdit and not self.m_bCityEdit)
        ):
            self.m_bChangeFocus = False
            setFocusToCVG()
        return

    def setMode(self, mode):
        if self.currentMode is not None:
            self.currentMode.deactivate()

        self.currentMode = mode

        if self.currentMode is not None:
            self.currentMode.activate()
        return

    # Will update the screen (every 250 MS)
    def updateScreen(self):

        if self.currentMode is not None:
            self.currentMode.updateScreen(self.m_pCurrentPlot)
            return 0

        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)

        if CyInterface().isInAdvancedStart():
            if self.m_bSideMenuDirty:
                self.refreshSideMenu()
            if self.m_bASItemCostDirty:
                self.refreshASItemCost()

        if (
            CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT)
            and not CyInterface().isFocusedWidget()
        ):
            self.refreshAdvancedStartTabCtrl(True)
            CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, False)

        if self.useLargeBrush():
            self.m_bShowBigBrush = True
        else:
            self.m_bShowBigBrush = False

        if self.m_bCtrlEditUp:
            if (
                (not self.m_bUnitEdit)
                and (not self.m_bCityEdit)
                and (not self.m_tabCtrlEdit.isEnabled())
                and not CyInterface().isInAdvancedStart()
            ):
                if self.m_bNormalMap:
                    self.m_normalMapTabCtrl.enable(True)
                if self.m_bNormalPlayer:
                    self.m_normalPlayerTabCtrl.enable(True)
                self.m_bCtrlEditUp = False
                return 0
        if (
            (self.m_bNormalMap)
            and (self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerrainTabID)
            and (
                self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                == self.m_iRouteListID
            )
        ):
            if (
                self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
                == gc.getNumRouteInfos()
            ):
                if self.m_pRiverStartPlot != -1:
                    self.setRiverHighlights()
                    return 0
        self.highlightBrush()
        return 0

    def redraw(self):
        return 0

    def resetTechButtons(self):
        for i in range(gc.getNumTechInfos()):
            strName = "Tech_%s" % (i,)
            self.m_normalPlayerTabCtrl.setCheckBoxState(
                "Technologies",
                gc.getTechInfo(i).getDescription(),
                gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).isHasTech(i),
            )
        return 1

    def handleAllPlotsCB(self, popupReturn):
        iButton = popupReturn.getButtonClicked()
        if iButton < PlotTypes.NUM_PLOT_TYPES:
            iTempVal = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
            self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] = iButton
            self.setAllPlots()
            self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] = iTempVal
        if not (self.m_bUnitEdit or self.m_bCityEdit):
            self.m_normalPlayerTabCtrl.enable(self.m_bNormalPlayer)
            self.m_normalMapTabCtrl.enable(self.m_bNormalMap)
        else:
            self.m_normalPlayerTabCtrl.enable(False)
            self.m_normalMapTabCtrl.enable(False)
        return 1

    def allPlotsCB(self):
        self.m_normalPlayerTabCtrl.enable(False)
        self.m_normalMapTabCtrl.enable(False)
        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.enable(False)
        popup = PyPopup.PyPopup(CvUtil.EventWBAllPlotsPopup, EventContextTypes.EVENTCONTEXT_ALL)
        iPopupWidth = 200
        iPopupHeight = 50 * PlotTypes.NUM_PLOT_TYPES
        popup.setSize(iPopupWidth, iPopupHeight)
        popup.setHeaderString(text("TXT_KEY_WB_CHANGE_ALL_PLOTS"))
        for i in range(PlotTypes.NUM_PLOT_TYPES):
            if i == 0:
                popup.addButton(text("TXT_KEY_WB_ADD_MOUNTAIN"))
            elif i == 1:
                popup.addButton(text("TXT_KEY_WB_ADD_HILL"))
            elif i == 2:
                popup.addButton(text("TXT_KEY_WB_ADD_GRASS"))
            elif i == 3:
                popup.addButton(text("TXT_KEY_WB_ADD_OCEAN"))
        popup.addButton(text("TXT_KEY_SCREEN_CANCEL"))
        popup.launch(False)
        return 1

    def refreshReveal(self):
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
        for i in range(CyMap().getGridWidth()):
            for j in range(CyMap().getGridHeight()):
                pPlot = CyMap().plot(i, j)
                if not pPlot.isNone():
                    self.showRevealed(pPlot)
        return 1

    def setAllPlots(self):
        iPlotType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
        CyMap().setAllPlotTypes(iPlotType)
        # for i in range (CyMap().getGridWidth()):
        # for j in range (CyMap().getGridHeight()):
        # CyMap().plot(i,j).setPlotType(PlotTypes(iPlotType), True, True)
        return 1

    def handleUnitEditExperienceCB(self, argsList):
        iNewXP = int(argsList[0])
        self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setExperience(iNewXP, -1)
        return 1

    def handleUnitEditLevelCB(self, argsList):
        iNewLevel = int(argsList[0])
        self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setLevel(iNewLevel)
        return 1

    def handleUnitEditNameCB(self, argsList):
        if (
            (len(argsList[0]) < 1)
            or (self.m_pActivePlot == 0)
            or (self.m_iCurrentUnit < 0)
            or (self.m_pActivePlot.getNumUnits() <= self.m_iCurrentUnit)
        ):
            return 1
        szNewName = argsList[0]
        unit = self.m_pActivePlot.getUnit(self.m_iCurrentUnit)
        if unit:
            unit.setName(szNewName)
        return 1

    def handleCityEditPopulationCB(self, argsList):
        iNewPop = int(argsList[0])
        self.m_pActivePlot.getPlotCity().setPopulation(iNewPop)
        return 1

    def handleCityEditCultureCB(self, argsList):
        iNewCulture = int(argsList[0])
        self.m_pActivePlot.getPlotCity().setCulture(
            self.m_pActivePlot.getPlotCity().getOwner(), iNewCulture, True
        )
        return 1

    def handleCityEditGoldCB(self, argsList):
        iNewGold = int(argsList[0])
        gc.getPlayer(self.m_iCurrentPlayer).setGold(iNewGold)
        return 1

    def handleCityEditNameCB(self, argsList):
        if (len(argsList[0]) < 1) or (not self.m_pActivePlot.isCity()):
            return 1
        szNewName = argsList[0]
        city = self.m_pActivePlot.getPlotCity()
        if city:
            city.setName(szNewName, False)
        return 1

    def handleUnitEditPullDownCB(self, argsList):
        self.m_iCurrentUnit = int(argsList[0])
        self.m_iCurrentUnitPlayer = self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getOwner()
        self.setUnitEditInfo(True)
        self.setEditUnitTabs()
        return 1

    def handleUnitAITypeEditPullDownCB(self, argsList):
        iNewAIType = int(argsList[0])
        self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setUnitAIType(iNewAIType)
        return 1

    def handlePlayerEditPullDownCB(self, argsList):
        self.m_iCurrentUnitPlayer = int(argsList[0])
        return 1

    def handlePlayerUnitPullDownCB(self, argsList):
        iIndex = int(argsList)
        iCount = -1
        for i in range(gc.getMAX_CIV_PLAYERS()):
            if gc.getPlayer(i).isEverAlive():
                iCount = iCount + 1
                if iCount == iIndex:
                    self.m_iCurrentPlayer = i
                    self.refreshPlayerTabCtrl()
                    return 1

        i = i + 1
        self.m_iCurrentPlayer = i
        self.refreshPlayerTabCtrl()
        return 1

    def handleWorldBuilderTechByEraPullDownCB(self, argsList):
        iIndex = int(argsList)
        for i in range(gc.getNumTechInfos()):
            if gc.getTechInfo(i).getEra() == iIndex:
                gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).setHasTech(
                    i, True, self.m_iCurrentPlayer, False, False
                )

        self.refreshPlayerTabCtrl()
        return 1

    def handleSelectTeamPullDownCB(self, argsList):
        iIndex = int(argsList)
        iCount = -1
        for i in range(gc.getMAX_CIV_TEAMS()):
            if gc.getTeam(i).isEverAlive():
                iCount = iCount + 1
                if iCount == iIndex:
                    self.m_iCurrentTeam = i

        self.refreshReveal()
        return 1

    def handlePromotionCB(self, iNewPromotion):
        bOn = not self.m_pActivePlot.getUnit(self.m_iCurrentUnit).isHasPromotion(iNewPromotion)
        self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setHasPromotion(iNewPromotion, bOn)
        return 1

    def hasPromotion(self, iPromotion):
        return self.m_pActivePlot.getUnit(self.m_iCurrentUnit).isHasPromotion(iPromotion)

    def hasTech(self, iTech):
        return gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).isHasTech(iTech)

    def getNumBuilding(self, iBuilding):
        return self.m_pActivePlot.getPlotCity().getNumBuilding(iBuilding)

    def hasReligion(self, iReligion):
        return self.m_pActivePlot.getPlotCity().isHasReligion(iReligion)

    def hasHolyCity(self, iReligion):
        return self.m_pActivePlot.getPlotCity().isHolyCityByType(iReligion)

    def hasCorporation(self, iCorporation):
        return self.m_pActivePlot.getPlotCity().isHasCorporation(iCorporation)

    def hasHeadquarters(self, iCorporation):
        return self.m_pActivePlot.getPlotCity().isHeadquartersByType(iCorporation)

    def handleTechCB(self, argsList):
        bOn, strName = argsList
        if (strName.find("_") != -1) and (self.m_iCurrentPlayer >= 0):
            iTech = int(strName[strName.find("_") + 1 :])
            gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).setHasTech(
                iTech, bOn, self.m_iCurrentPlayer, False, False
            )
            self.resetTechButtons()
        return 1

    def handleEditCityBuildingCB(self, argsList):
        bOn, strName = argsList
        iNewBuilding = int(strName[strName.find("_") + 1 :])
        if bOn:
            self.m_pActivePlot.getPlotCity().setNumRealBuilding(iNewBuilding, 1)
        else:
            self.m_pActivePlot.getPlotCity().setNumRealBuilding(iNewBuilding, 0)
        return 1

    def handleBrushWidthCB(self, argsList):
        if int(argsList) == 0:
            self.m_iBrushWidth = int(1)
        elif int(argsList) == 1:
            self.m_iBrushWidth = int(2)
        elif int(argsList) == 2:
            self.m_iBrushWidth = int(3)
        return 1

    def handleBrushHeightCB(self, argsList):
        if int(argsList) == 0:
            self.m_iBrushHeight = int(1)
        elif int(argsList) == 1:
            self.m_iBrushHeight = int(2)
        elif int(argsList) == 2:
            self.m_iBrushHeight = int(3)
        return 1

    def handleLandmarkCB(self, argsList):
        return 1

    ########################################################
    ### Advanced Start Stuff
    ########################################################

    def refreshASItemCost(self):

        if CyInterface().isInAdvancedStart():

            self.m_iCost = 0

            if self.m_pCurrentPlot != 0:

                # 				if (not self.m_pCurrentPlot.isAdjacentNonrevealed(CyGame().getActiveTeam()) and self.m_pCurrentPlot.isRevealed(CyGame().getActiveTeam(), False)):
                if self.m_pCurrentPlot.isRevealed(CyGame().getActiveTeam(), False):

                    # Unit mode
                    if self.getASActiveUnit() != -1:
                        self.m_iCost = gc.getPlayer(
                            self.m_iCurrentPlayer
                        ).getAdvancedStartUnitCost(
                            self.getASActiveUnit(), True, self.m_pCurrentPlot
                        )
                    elif self.getASActiveCity() != -1:
                        self.m_iCost = gc.getPlayer(
                            self.m_iCurrentPlayer
                        ).getAdvancedStartCityCost(True, self.m_pCurrentPlot)
                    elif self.getASActivePop() != -1 and self.m_pCurrentPlot.isCity():
                        self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartPopCost(
                            True, self.m_pCurrentPlot.getPlotCity()
                        )
                    elif self.getASActiveCulture() != -1 and self.m_pCurrentPlot.isCity():
                        self.m_iCost = gc.getPlayer(
                            self.m_iCurrentPlayer
                        ).getAdvancedStartCultureCost(True, self.m_pCurrentPlot.getPlotCity())
                    elif self.getASActiveBuilding() != -1 and self.m_pCurrentPlot.isCity():
                        self.m_iCost = gc.getPlayer(
                            self.m_iCurrentPlayer
                        ).getAdvancedStartBuildingCost(
                            self.getASActiveBuilding(), True, self.m_pCurrentPlot.getPlotCity()
                        )
                    elif self.getASActiveRoute() != -1:
                        self.m_iCost = gc.getPlayer(
                            self.m_iCurrentPlayer
                        ).getAdvancedStartRouteCost(
                            self.getASActiveRoute(), True, self.m_pCurrentPlot
                        )
                    elif self.getASActiveImprovement() != -1:
                        self.m_iCost = gc.getPlayer(
                            self.m_iCurrentPlayer
                        ).getAdvancedStartImprovementCost(
                            self.getASActiveImprovement(), True, self.m_pCurrentPlot
                        )

                elif self.m_pCurrentPlot.isAdjacentNonrevealed(CyGame().getActiveTeam()):
                    if self.getASActiveVisibility() != -1:
                        self.m_iCost = gc.getPlayer(
                            self.m_iCurrentPlayer
                        ).getAdvancedStartVisibilityCost(True, self.m_pCurrentPlot)

            if self.m_iCost < 0:
                self.m_iCost = 0

            self.refreshSideMenu()

    def getASActiveUnit(self):
        # Unit Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID:
            iUnitType = getASUnit(
                self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
            )
            return iUnitType

        return -1

    def getASActiveCity(self):
        # City Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
            # City List
            if (
                self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()]
                == self.m_iASCityListID
            ):
                iOptionID = self.m_iAdvancedStartCurrentIndexes[
                    self.m_advancedStartTabCtrl.getActiveTab()
                ]
                # Place City
                if iOptionID == 0:
                    return 1

        return -1

    def getASActivePop(self):
        # City Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
            # City List
            if (
                self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()]
                == self.m_iASCityListID
            ):
                iOptionID = self.m_iAdvancedStartCurrentIndexes[
                    self.m_advancedStartTabCtrl.getActiveTab()
                ]
                # Place Pop
                if iOptionID == 1:
                    return 1

        return -1

    def getASActiveCulture(self):
        # City Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
            # City List
            if (
                self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()]
                == self.m_iASCityListID
            ):
                iOptionID = self.m_iAdvancedStartCurrentIndexes[
                    self.m_advancedStartTabCtrl.getActiveTab()
                ]
                # Place Culture
                if iOptionID == 2:
                    return 1

        return -1

    def getASActiveBuilding(self):
        # Building Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
            # Buildings List
            if (
                self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()]
                == self.m_iASBuildingsListID
            ):
                iBuildingType = getASBuilding(
                    self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
                )
                return iBuildingType

        return -1

    def getASActiveRoute(self):
        # Improvements Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:
            # Routes List
            if (
                self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()]
                == self.m_iASRoutesListID
            ):
                iRouteType = getASRoute(
                    self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
                )
                if -1 == iRouteType:
                    self.m_iAdvancedStartCurrentList[
                        self.m_advancedStartTabCtrl.getActiveTab()
                    ] = self.m_iASImprovementsListID
                return iRouteType

        return -1

    def getASActiveImprovement(self):
        # Improvements Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:
            # Improvements List
            if (
                self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()]
                == self.m_iASImprovementsListID
            ):
                iImprovementType = getASImprovement(
                    self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
                )
                if -1 == iImprovementType:
                    self.m_iAdvancedStartCurrentList[
                        self.m_advancedStartTabCtrl.getActiveTab()
                    ] = self.m_iASRoutesListID
                return iImprovementType

        return -1

    def getASActiveVisibility(self):
        # Visibility Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASVisibilityTabID:
            return 1

        return -1

    def getASActiveTech(self):
        # Tech Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASTechTabID:
            return 1

        return -1

    def placeObject(self):

        # Advanced Start
        if CyInterface().isInAdvancedStart():

            pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
            pPlot = CyMap().plot(self.m_iCurrentX, self.m_iCurrentY)

            iActiveTeam = CyGame().getActiveTeam()
            if self.m_pCurrentPlot.isRevealed(iActiveTeam, False):

                # City Tab
                if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:

                    # City List
                    if (
                        self.m_iAdvancedStartCurrentList[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                        == self.m_iASCityListID
                    ):

                        iOptionID = self.m_iAdvancedStartCurrentIndexes[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]

                        # Place City
                        if iOptionID == 0:

                            # Cost -1 means may not be placed here
                            if pPlayer.getAdvancedStartCityCost(True, pPlot) != -1:

                                CyMessageControl().sendAdvancedStartAction(
                                    AdvancedStartActionTypes.ADVANCEDSTARTACTION_CITY,
                                    self.m_iCurrentPlayer,
                                    self.m_iCurrentX,
                                    self.m_iCurrentY,
                                    -1,
                                    True,
                                )  # Action, Player, X, Y, Data, bAdd

                        # City Population
                        elif iOptionID == 1:

                            if pPlot.isCity():
                                pCity = pPlot.getPlotCity()

                                # Cost -1 means may not be placed here
                                if pPlayer.getAdvancedStartPopCost(True, pCity) != -1:

                                    CyMessageControl().sendAdvancedStartAction(
                                        AdvancedStartActionTypes.ADVANCEDSTARTACTION_POP,
                                        self.m_iCurrentPlayer,
                                        self.m_iCurrentX,
                                        self.m_iCurrentY,
                                        -1,
                                        True,
                                    )  # Action, Player, X, Y, Data, bAdd

                        # City Culture
                        elif iOptionID == 2:

                            if pPlot.isCity():
                                pCity = pPlot.getPlotCity()

                                # Cost -1 means may not be placed here
                                if pPlayer.getAdvancedStartCultureCost(True, pCity) != -1:

                                    CyMessageControl().sendAdvancedStartAction(
                                        AdvancedStartActionTypes.ADVANCEDSTARTACTION_CULTURE,
                                        self.m_iCurrentPlayer,
                                        self.m_iCurrentX,
                                        self.m_iCurrentY,
                                        -1,
                                        True,
                                    )  # Action, Player, X, Y, Data, bAdd

                    # Buildings List
                    elif (
                        self.m_iAdvancedStartCurrentList[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                        == self.m_iASBuildingsListID
                    ):

                        if pPlot.isCity():
                            pCity = pPlot.getPlotCity()

                            iBuildingType = getASBuilding(
                                self.m_iAdvancedStartCurrentIndexes[
                                    self.m_advancedStartTabCtrl.getActiveTab()
                                ]
                            )

                            # Cost -1 means may not be placed here
                            if (
                                iBuildingType != -1
                                and pPlayer.getAdvancedStartBuildingCost(
                                    iBuildingType, True, pCity
                                )
                                != -1
                            ):

                                CyMessageControl().sendAdvancedStartAction(
                                    AdvancedStartActionTypes.ADVANCEDSTARTACTION_BUILDING,
                                    self.m_iCurrentPlayer,
                                    self.m_iCurrentX,
                                    self.m_iCurrentY,
                                    iBuildingType,
                                    True,
                                )  # Action, Player, X, Y, Data, bAdd

                # Unit Tab
                elif self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID:
                    iUnitType = getASUnit(
                        self.m_iAdvancedStartCurrentIndexes[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                    )

                    # Cost -1 means may not be placed here
                    if (
                        iUnitType != -1
                        and pPlayer.getAdvancedStartUnitCost(iUnitType, True, pPlot) != -1
                    ):

                        CyMessageControl().sendAdvancedStartAction(
                            AdvancedStartActionTypes.ADVANCEDSTARTACTION_UNIT,
                            self.m_iCurrentPlayer,
                            self.m_iCurrentX,
                            self.m_iCurrentY,
                            iUnitType,
                            True,
                        )  # Action, Player, X, Y, Data, bAdd

                # Improvements Tab
                elif self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:

                    # Routes List
                    if (
                        self.m_iAdvancedStartCurrentList[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                        == self.m_iASRoutesListID
                    ):

                        iRouteType = getASRoute(
                            self.m_iAdvancedStartCurrentIndexes[
                                self.m_advancedStartTabCtrl.getActiveTab()
                            ]
                        )

                        # Cost -1 means may not be placed here
                        if (
                            iRouteType != -1
                            and pPlayer.getAdvancedStartRouteCost(iRouteType, True, pPlot) != -1
                        ):

                            CyMessageControl().sendAdvancedStartAction(
                                AdvancedStartActionTypes.ADVANCEDSTARTACTION_ROUTE,
                                self.m_iCurrentPlayer,
                                self.m_iCurrentX,
                                self.m_iCurrentY,
                                iRouteType,
                                True,
                            )  # Action, Player, X, Y, Data, bAdd

                    # Improvements List
                    elif (
                        self.m_iAdvancedStartCurrentList[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                        == self.m_iASImprovementsListID
                    ):

                        iImprovementType = getASImprovement(
                            self.m_iAdvancedStartCurrentIndexes[
                                self.m_advancedStartTabCtrl.getActiveTab()
                            ]
                        )

                        # Cost -1 means may not be placed here
                        if (
                            pPlayer.getAdvancedStartImprovementCost(iImprovementType, True, pPlot)
                            != -1
                        ):

                            CyMessageControl().sendAdvancedStartAction(
                                AdvancedStartActionTypes.ADVANCEDSTARTACTION_IMPROVEMENT,
                                self.m_iCurrentPlayer,
                                self.m_iCurrentX,
                                self.m_iCurrentY,
                                iImprovementType,
                                True,
                            )  # Action, Player, X, Y, Data, bAdd

            # Adjacent nonrevealed
            else:

                # Visibility Tab
                if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASVisibilityTabID:

                    # Cost -1 means may not be placed here
                    if pPlayer.getAdvancedStartVisibilityCost(True, pPlot) != -1:

                        CyMessageControl().sendAdvancedStartAction(
                            AdvancedStartActionTypes.ADVANCEDSTARTACTION_VISIBILITY,
                            self.m_iCurrentPlayer,
                            self.m_iCurrentX,
                            self.m_iCurrentY,
                            -1,
                            True,
                        )  # Action, Player, X, Y, Data, bAdd

            self.m_bSideMenuDirty = True
            self.m_bASItemCostDirty = True

            return 1

        if (
            (self.m_iNormalPlayerCurrentIndexes[self.m_normalPlayerTabCtrl.getActiveTab()] == -1)
            or (self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] == -1)
            or (self.m_iCurrentX == -1)
            or (self.m_iCurrentY == -1)
            or (self.m_iCurrentPlayer == -1)
        ):
            return 1

        if self.m_bEraseAll:
            self.eraseAll()
        elif (self.m_bNormalPlayer) and (
            self.m_normalPlayerTabCtrl.getActiveTab() == self.m_iUnitTabID
        ):
            iUnitType = self.m_iNormalPlayerCurrentIndexes[
                self.m_normalPlayerTabCtrl.getActiveTab()
            ]
            pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
            iPlotX = self.m_iCurrentX
            iPlotY = self.m_iCurrentY
            pPlayer.initUnit(
                iUnitType, iPlotX, iPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION
            )
        elif (self.m_bNormalPlayer) and (
            self.m_normalPlayerTabCtrl.getActiveTab() == self.m_iBuildingTabID
        ):
            iBuildingType = self.m_iNormalPlayerCurrentIndexes[
                self.m_normalPlayerTabCtrl.getActiveTab()
            ]
            if (self.m_pCurrentPlot.isCity()) and (iBuildingType != 0):
                self.m_pCurrentPlot.getPlotCity().setNumRealBuilding(iBuildingType - 1, 1)
            if iBuildingType == 0:
                if not self.m_pCurrentPlot.isCity():
                    pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
                    iX = self.m_pCurrentPlot.getX()
                    iY = self.m_pCurrentPlot.getY()
                    pPlayer.initCity(iX, iY)
                    # Absinthe: correct CNM name for new cities in the WB
                    if (
                        self.m_iCurrentPlayer < civilizations().majors().len()
                    ):  # indy and barb civs don't have a city name map
                        cityName = MapManager.getCityName(
                            self.m_iCurrentPlayer, self.m_pCurrentPlot
                        )
                        if cityName is not None:
                            city = gc.getMap().plot(iX, iY).getPlotCity()
                            city.setName(unicode(cityName, "latin-1"), False)  # type: ignore
        elif (self.m_bNormalMap) and (
            self.m_normalMapTabCtrl.getActiveTab() == self.m_iImprovementTabID
        ):
            iImprovementType = self.m_iNormalMapCurrentIndexes[
                self.m_normalMapTabCtrl.getActiveTab()
            ]
            iIndex = -1
            iCounter = -1
            while (iIndex < iImprovementType) and (iCounter < gc.getNumImprovementInfos()):
                iCounter = iCounter + 1
                if not gc.getImprovementInfo(iCounter).isGraphicalOnly():
                    iIndex = iIndex + 1
            if iIndex > -1:
                self.m_pCurrentPlot.setImprovementType(iCounter)
        elif (self.m_bNormalMap) and (
            self.m_normalMapTabCtrl.getActiveTab() == self.m_iBonusTabID
        ):
            iBonusType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
            self.m_pCurrentPlot.setBonusType(iBonusType)
        elif (self.m_bNormalMap) and (
            self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerrainTabID
        ):
            if (
                self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                == self.m_iTerrainListID
            ):
                iTerrainType = self.m_iNormalMapCurrentIndexes[
                    self.m_normalMapTabCtrl.getActiveTab()
                ]
                self.m_pCurrentPlot.setTerrainType(iTerrainType, True, True)
            elif (
                self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                == self.m_iFeatureListID
            ):
                iButtonIndex = self.m_iNormalMapCurrentIndexes[
                    self.m_normalMapTabCtrl.getActiveTab()
                ]
                iCount = -1
                for i in range(gc.getNumFeatureInfos()):
                    for j in range(gc.getFeatureInfo(i).getNumVarieties()):
                        iCount = iCount + 1
                        if iCount == iButtonIndex:
                            self.m_pCurrentPlot.setFeatureType(i, j)
            elif (
                self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                == self.m_iPlotTypeListID
            ):
                iPlotType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
                if (iPlotType >= 0) and (iPlotType < PlotTypes.NUM_PLOT_TYPES):
                    self.m_pCurrentPlot.setPlotType(PlotTypes(iPlotType), True, True)
            elif (
                self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                == self.m_iRouteListID
            ):
                iRouteType = self.m_iNormalMapCurrentIndexes[
                    self.m_normalMapTabCtrl.getActiveTab()
                ]
                if iRouteType == gc.getNumRouteInfos():
                    if self.m_pRiverStartPlot == self.m_pCurrentPlot:
                        self.m_pRiverStartPlot = -1
                        CyEngine().clearColoredPlots(
                            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS
                        )
                        return 1
                    if self.m_pRiverStartPlot != -1:
                        iXDiff = 0
                        iYDiff = 0
                        if self.m_pRiverStartPlot.getX() < self.m_pCurrentPlot.getX():
                            iXDiff = self.m_pCurrentPlot.getX() - self.m_pRiverStartPlot.getX()
                        elif self.m_pRiverStartPlot.getX() > self.m_pCurrentPlot.getX():
                            iXDiff = self.m_pRiverStartPlot.getX() - self.m_pCurrentPlot.getX()
                        if self.m_pRiverStartPlot.getY() < self.m_pCurrentPlot.getY():
                            iYDiff = self.m_pCurrentPlot.getY() - self.m_pRiverStartPlot.getY()
                        elif self.m_pRiverStartPlot.getY() > self.m_pCurrentPlot.getY():
                            iYDiff = self.m_pRiverStartPlot.getY() - self.m_pCurrentPlot.getY()

                        if (
                            (iXDiff == iYDiff)
                            and (iXDiff == 1)
                            and (self.m_pRiverStartPlot.getX() > self.m_pCurrentPlot.getX())
                            and (self.m_pRiverStartPlot.getY() < self.m_pCurrentPlot.getY())
                        ):
                            self.placeRiverNW(True)
                            self.m_pRiverStartPlot = CyMap().plot(
                                self.m_pRiverStartPlot.getX() - 1,
                                self.m_pRiverStartPlot.getY() + 1,
                            )
                        elif (
                            (iXDiff == 0)
                            and (iYDiff == 1)
                            and (self.m_pRiverStartPlot.getY() < self.m_pCurrentPlot.getY())
                        ):
                            self.placeRiverN(True)
                            self.m_pRiverStartPlot = self.m_pCurrentPlot
                        elif (
                            (iXDiff == iYDiff)
                            and (iXDiff == 1)
                            and (self.m_pRiverStartPlot.getX() < self.m_pCurrentPlot.getX())
                            and (self.m_pRiverStartPlot.getY() < self.m_pCurrentPlot.getY())
                        ):
                            self.placeRiverNE(True)
                            self.m_pRiverStartPlot = self.m_pCurrentPlot
                        elif (
                            (iXDiff == 1)
                            and (iYDiff == 0)
                            and (self.m_pRiverStartPlot.getX() > self.m_pCurrentPlot.getX())
                        ):
                            self.placeRiverW(True)
                            self.m_pRiverStartPlot = self.m_pCurrentPlot
                        elif (
                            (iXDiff == 1)
                            and (iYDiff == 0)
                            and (self.m_pRiverStartPlot.getX() < self.m_pCurrentPlot.getX())
                        ):
                            self.placeRiverE(True)
                            self.m_pRiverStartPlot = self.m_pCurrentPlot
                        elif (
                            (iXDiff == iYDiff)
                            and (iXDiff == 1)
                            and (self.m_pRiverStartPlot.getX() > self.m_pCurrentPlot.getX())
                            and (self.m_pRiverStartPlot.getY() > self.m_pCurrentPlot.getY())
                        ):
                            self.placeRiverSW(True)
                            self.m_pRiverStartPlot = self.m_pCurrentPlot
                        elif (
                            (iXDiff == 0)
                            and (iYDiff == 1)
                            and (self.m_pRiverStartPlot.getY() > self.m_pCurrentPlot.getY())
                        ):
                            self.placeRiverS(True)
                            self.m_pRiverStartPlot = self.m_pCurrentPlot
                        elif (
                            (iXDiff == iYDiff)
                            and (iXDiff == 1)
                            and (self.m_pRiverStartPlot.getX() < self.m_pCurrentPlot.getX())
                            and (self.m_pRiverStartPlot.getY() > self.m_pCurrentPlot.getY())
                        ):
                            self.placeRiverSE(True)
                            self.m_pRiverStartPlot = self.m_pCurrentPlot
                        else:
                            self.m_pRiverStartPlot = self.m_pCurrentPlot
                    else:
                        self.m_pRiverStartPlot = self.m_pCurrentPlot
                else:
                    self.m_pCurrentPlot.setRouteType(iRouteType)
        elif (self.m_bNormalMap) and (
            self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerritoryTabID
        ):
            iPlayer = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
            if gc.getPlayer(iPlayer).isEverAlive():
                self.m_pCurrentPlot.setOwner(iPlayer)
        elif self.m_bLandmark:
            CvEventInterface.beginEvent(CvUtil.EventWBLandmarkPopup)
        return 1

    def removeObject(self):

        # Advanced Start
        if CyInterface().isInAdvancedStart():

            pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
            pPlot = CyMap().plot(self.m_iCurrentX, self.m_iCurrentY)

            iActiveTeam = CyGame().getActiveTeam()
            # 			if (not self.m_pCurrentPlot.isAdjacentNonrevealed(iActiveTeam) and self.m_pCurrentPlot.isRevealed(iActiveTeam, False)):
            if self.m_pCurrentPlot.isRevealed(iActiveTeam, False):

                # City Tab
                if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:

                    # City List
                    if (
                        self.m_iAdvancedStartCurrentList[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                        == self.m_iASCityListID
                    ):

                        iOptionID = self.m_iAdvancedStartCurrentIndexes[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]

                        # Place City
                        if iOptionID == 0:

                            # Ability to remove cities not allowed because of 'sploitz (visibility, chopping down jungle, etc.)
                            return 1

                            if self.m_pCurrentPlot.isCity():

                                if (
                                    self.m_pCurrentPlot.getPlotCity().getOwner()
                                    == self.m_iCurrentPlayer
                                ):

                                    CyMessageControl().sendAdvancedStartAction(
                                        AdvancedStartActionTypes.ADVANCEDSTARTACTION_CITY,
                                        self.m_iCurrentPlayer,
                                        self.m_iCurrentX,
                                        self.m_iCurrentY,
                                        -1,
                                        False,
                                    )  # Action, Player, X, Y, Data, bAdd

                        # City Population
                        elif iOptionID == 1:

                            if pPlot.isCity():
                                if pPlot.getPlotCity().getOwner() == self.m_iCurrentPlayer:

                                    CyMessageControl().sendAdvancedStartAction(
                                        AdvancedStartActionTypes.ADVANCEDSTARTACTION_POP,
                                        self.m_iCurrentPlayer,
                                        self.m_iCurrentX,
                                        self.m_iCurrentY,
                                        -1,
                                        False,
                                    )  # Action, Player, X, Y, Data, bAdd

                        # City Culture
                        elif iOptionID == 2:

                            # Ability to remove cities not allowed because of 'sploitz (visibility)
                            return 1

                            if pPlot.isCity():
                                if pPlot.getPlotCity().getOwner() == self.m_iCurrentPlayer:

                                    CyMessageControl().sendAdvancedStartAction(
                                        AdvancedStartActionTypes.ADVANCEDSTARTACTION_CULTURE,
                                        self.m_iCurrentPlayer,
                                        self.m_iCurrentX,
                                        self.m_iCurrentY,
                                        -1,
                                        False,
                                    )  # Action, Player, X, Y, Data, bAdd

                    # Buildings List
                    elif (
                        self.m_iAdvancedStartCurrentList[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                        == self.m_iASBuildingsListID
                    ):

                        if pPlot.isCity():
                            if pPlot.getPlotCity().getOwner() == self.m_iCurrentPlayer:

                                iBuildingType = getASBuilding(
                                    self.m_iAdvancedStartCurrentIndexes[
                                        self.m_advancedStartTabCtrl.getActiveTab()
                                    ]
                                )

                                if -1 != iBuildingType:
                                    CyMessageControl().sendAdvancedStartAction(
                                        AdvancedStartActionTypes.ADVANCEDSTARTACTION_BUILDING,
                                        self.m_iCurrentPlayer,
                                        self.m_iCurrentX,
                                        self.m_iCurrentY,
                                        iBuildingType,
                                        False,
                                    )  # Action, Player, X, Y, Data, bAdd

                # Unit Tab
                elif self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID:

                    iUnitType = getASUnit(
                        self.m_iAdvancedStartCurrentIndexes[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                    )

                    if -1 != iUnitType:
                        CyMessageControl().sendAdvancedStartAction(
                            AdvancedStartActionTypes.ADVANCEDSTARTACTION_UNIT,
                            self.m_iCurrentPlayer,
                            self.m_pCurrentPlot.getX(),
                            self.m_pCurrentPlot.getY(),
                            iUnitType,
                            False,
                        )  # Action, Player, X, Y, Data, bAdd

                # Improvements Tab
                elif self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:

                    # Routes List
                    if (
                        self.m_iAdvancedStartCurrentList[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                        == self.m_iASRoutesListID
                    ):

                        iRouteType = getASRoute(
                            self.m_iAdvancedStartCurrentIndexes[
                                self.m_advancedStartTabCtrl.getActiveTab()
                            ]
                        )

                        if -1 != iRouteType:
                            CyMessageControl().sendAdvancedStartAction(
                                AdvancedStartActionTypes.ADVANCEDSTARTACTION_ROUTE,
                                self.m_iCurrentPlayer,
                                self.m_iCurrentX,
                                self.m_iCurrentY,
                                iRouteType,
                                False,
                            )  # Action, Player, X, Y, Data, bAdd

                    # Improvements List
                    elif (
                        self.m_iAdvancedStartCurrentList[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                        == self.m_iASImprovementsListID
                    ):

                        iImprovementType = getASImprovement(
                            self.m_iAdvancedStartCurrentIndexes[
                                self.m_advancedStartTabCtrl.getActiveTab()
                            ]
                        )

                        if -1 != iImprovementType:
                            CyMessageControl().sendAdvancedStartAction(
                                AdvancedStartActionTypes.ADVANCEDSTARTACTION_IMPROVEMENT,
                                self.m_iCurrentPlayer,
                                self.m_iCurrentX,
                                self.m_iCurrentY,
                                iImprovementType,
                                False,
                            )  # Action, Player, X, Y, Data, bAdd

            # Adjacent nonrevealed
            else:

                # Visibility Tab
                if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASVisibilityTabID:

                    # Ability to remove sight not allowed because of 'sploitz
                    return 1

                    # Remove Visibility
                    if pPlot.isRevealed(iActiveTeam, False):

                        CyMessageControl().sendAdvancedStartAction(
                            AdvancedStartActionTypes.ADVANCEDSTARTACTION_VISIBILITY,
                            self.m_iCurrentPlayer,
                            self.m_iCurrentX,
                            self.m_iCurrentY,
                            -1,
                            False,
                        )  # Action, Player, X, Y, Data, bAdd

            self.m_bSideMenuDirty = True
            self.m_bASItemCostDirty = True

            return 1

        if (
            (self.m_iNormalPlayerCurrentIndexes[self.m_normalPlayerTabCtrl.getActiveTab()] == -1)
            or (self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] == -1)
            or (self.m_iCurrentX == -1)
            or (self.m_iCurrentY == -1)
            or (self.m_iCurrentPlayer == -1)
        ):
            return 1

        if self.m_bEraseAll:
            self.eraseAll()
        elif (self.m_bNormalPlayer) and (
            self.m_normalPlayerTabCtrl.getActiveTab() == self.m_iUnitTabID
        ):
            for i in range(self.m_pCurrentPlot.getNumUnits()):
                pUnit = self.m_pCurrentPlot.getUnit(i)
                if (
                    pUnit.getUnitType()
                    == self.m_iNormalPlayerCurrentIndexes[
                        self.m_normalPlayerTabCtrl.getActiveTab()
                    ]
                ):
                    pUnit.kill(False, PlayerTypes.NO_PLAYER)
                    return 1
            if self.m_pCurrentPlot.getNumUnits() > 0:
                pUnit = self.m_pCurrentPlot.getUnit(0)
                pUnit.kill(False, PlayerTypes.NO_PLAYER)
                return 1
        elif (self.m_bNormalPlayer) and (
            self.m_normalPlayerTabCtrl.getActiveTab() == self.m_iBuildingTabID
        ):
            if self.m_pCurrentPlot.isCity():
                iBuildingType = self.m_iNormalPlayerCurrentIndexes[
                    self.m_normalPlayerTabCtrl.getActiveTab()
                ]
                if iBuildingType == 0:
                    self.m_pCurrentPlot.getPlotCity().kill()
                else:
                    self.m_pCurrentPlot.getPlotCity().setNumRealBuilding(iBuildingType - 1, 0)
        elif (self.m_bNormalMap) and (
            self.m_normalMapTabCtrl.getActiveTab() == self.m_iImprovementTabID
        ):
            self.m_pCurrentPlot.setImprovementType(-1)
            return 1
        elif (self.m_bNormalMap) and (
            self.m_normalMapTabCtrl.getActiveTab() == self.m_iBonusTabID
        ):
            iBonusType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
            self.m_pCurrentPlot.setBonusType(-1)
            return 1
        elif (self.m_bNormalMap) and (
            self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerrainTabID
        ):
            if (
                self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                == self.m_iTerrainListID
            ):
                return 1
            elif (
                self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                == self.m_iFeatureListID
            ):
                iFeatureType = self.m_iNormalMapCurrentIndexes[
                    self.m_normalMapTabCtrl.getActiveTab()
                ]
                self.m_pCurrentPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
                return 1
            elif (
                self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                == self.m_iPlotTypeListID
            ):
                return 1
            elif (
                self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                == self.m_iRouteListID
            ):
                iRouteType = self.m_iNormalMapCurrentIndexes[
                    self.m_normalMapTabCtrl.getActiveTab()
                ]
                if iRouteType == gc.getNumRouteInfos():
                    if self.m_pRiverStartPlot != -1:
                        self.m_pRiverStartPlot = -1
                        CyEngine().clearColoredPlots(
                            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS
                        )
                    else:
                        self.m_pCurrentPlot.setNOfRiver(
                            False, CardinalDirectionTypes.NO_CARDINALDIRECTION
                        )
                        self.m_pCurrentPlot.setWOfRiver(
                            False, CardinalDirectionTypes.NO_CARDINALDIRECTION
                        )
                else:
                    self.m_pCurrentPlot.setRouteType(-1)
        elif (self.m_bNormalMap) and (
            self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerritoryTabID
        ):
            self.m_pCurrentPlot.setOwner(-1)
            return 1
        elif self.m_bLandmark:
            self.removeLandmarkCB()
        return 1

    def handleClicked(self):
        return

    def setEditUnitTabs(self):
        self.m_tabCtrlEdit.setDropDownSelection("Choose Unit", "Current_Unit", self.m_iCurrentUnit)
        self.m_tabCtrlEdit.setDropDownSelection(
            "Choose Unit",
            "Unit_AI_Type",
            self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getUnitAIType(),
        )
        return

    def isIntString(self, arg):
        for i in range(len(arg)):
            if arg[i] > "9":
                return False
            elif arg[i] < "0":
                return False
        return True

    def placeRiverNW(self, bUseCurrent):
        if bUseCurrent:
            pRiverStepPlot = CyMap().plot(
                self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()
            )
            if not pRiverStepPlot.isNone():
                pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)

        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX() - 1, self.m_pRiverStartPlot.getY()
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX() - 1, self.m_pRiverStartPlot.getY() + 1
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
        return

    def placeRiverN(self, bUseCurrent):
        if bUseCurrent:
            pRiverStepPlot = CyMap().plot(
                self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()
            )
            if not pRiverStepPlot.isNone():
                pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)

        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY() + 1
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
        return

    def placeRiverNE(self, bUseCurrent):
        if bUseCurrent:
            pRiverStepPlot = CyMap().plot(
                self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()
            )
            if not pRiverStepPlot.isNone():
                pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)

        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX() + 1, self.m_pRiverStartPlot.getY()
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)
            pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX() + 1, self.m_pRiverStartPlot.getY() + 1
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
        return

    def placeRiverW(self, bUseCurrent):
        if bUseCurrent:
            pRiverStepPlot = CyMap().plot(
                self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()
            )
            if not pRiverStepPlot.isNone():
                pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)

        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX() - 1, self.m_pRiverStartPlot.getY()
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)
        return

    def placeRiverE(self, bUseCurrent):
        if bUseCurrent:
            pRiverStepPlot = CyMap().plot(
                self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()
            )
            if not pRiverStepPlot.isNone():
                pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)

        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX() + 1, self.m_pRiverStartPlot.getY()
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)
        return

    def placeRiverSW(self, bUseCurrent):
        if bUseCurrent:
            pRiverStepPlot = CyMap().plot(
                self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()
            )
            if not pRiverStepPlot.isNone():
                pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)

        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX() - 1, self.m_pRiverStartPlot.getY() - 1
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
        return

    def placeRiverS(self, bUseCurrent):
        if bUseCurrent:
            pRiverStepPlot = CyMap().plot(
                self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()
            )
            if not pRiverStepPlot.isNone():
                pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)

        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY() - 1
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
        return

    def placeRiverSE(self, bUseCurrent):
        if bUseCurrent:
            pRiverStepPlot = CyMap().plot(
                self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()
            )
            if not pRiverStepPlot.isNone():
                pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)

        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX() + 1, self.m_pRiverStartPlot.getY()
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)
        pRiverStepPlot = CyMap().plot(
            self.m_pRiverStartPlot.getX() + 1, self.m_pRiverStartPlot.getY() - 1
        )
        if not pRiverStepPlot.isNone():
            pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
        return

    def setUnitEditInfo(self, bSamePlot):
        initWBToolEditCtrl()
        self.m_tabCtrlEdit = getWBToolEditTabCtrl()

        self.m_bUnitEditCtrl = True
        self.m_bCityEditCtrl = False

        if self.m_bFlyout:
            self.m_bFlyout = False
            self.m_pCurrentPlot = self.m_pFlyoutPlot

        if not bSamePlot:
            self.m_pActivePlot = self.m_pCurrentPlot

        self.m_tabCtrlEdit.setNumColumns((gc.getNumPromotionInfos() / 10) + 1)
        self.m_tabCtrlEdit.setColumnLength(20)
        self.m_tabCtrlEdit.addTabSection(text("TXT_KEY_WB_CHOOSE_UNIT"))
        strTest = ()
        for i in range(self.m_pActivePlot.getNumUnits()):
            if len(self.m_pActivePlot.getUnit(i).getNameNoDesc()):
                strTest = strTest + (self.m_pActivePlot.getUnit(i).getNameNoDesc(),)
            else:
                strTest = strTest + (self.m_pActivePlot.getUnit(i).getName(),)

        self.m_tabCtrlEdit.addSectionDropdown(
            "Current_Unit",
            strTest,
            "CvScreensInterface",
            "WorldBuilderHandleUnitEditPullDownCB",
            "UnitEditPullDown",
            0,
            self.m_iCurrentUnit,
        )

        if len(self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getNameNoDesc()):
            strName = self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getNameNoDesc()
        else:
            strName = self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getName()
        self.m_tabCtrlEdit.addSectionEditCtrl(
            strName, "CvScreensInterface", "WorldBuilderHandleUnitEditNameCB", "UnitEditName", 0
        )
        self.m_tabCtrlEdit.addSectionLabel(text("TXT_KEY_WB_EXPERIENCE"), 0)
        strExperience = str("UnitEditExperienceCB")
        self.m_tabCtrlEdit.addSectionSpinner(
            strExperience,
            "CvScreensInterface",
            "WorldBuilderHandleUnitEditExperienceCB",
            "UnitEditExperience",
            0,
            0.0,
            1000.0,
            1.0,
            self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getExperience(),
            0,
            0,
        )
        self.m_tabCtrlEdit.addSectionLabel(text("TXT_KEY_WB_LEVEL"), 0)
        strLevel = str("UnitEditLevelCB")
        self.m_tabCtrlEdit.addSectionSpinner(
            strLevel,
            "CvScreensInterface",
            "WorldBuilderHandleUnitEditLevelCB",
            "UnitEditLevel",
            0,
            1.0,
            1000.0,
            1.0,
            self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getLevel(),
            0,
            0,
        )
        strTest = ()
        for i in range(UnitAITypes.NUM_UNITAI_TYPES):
            strTest = strTest + (gc.getUnitAIInfo(i).getDescription(),)

        self.m_tabCtrlEdit.addSectionDropdown(
            "Unit_AI_Type",
            strTest,
            "CvScreensInterface",
            "WorldBuilderHandleUnitAITypeEditPullDownCB",
            "UnitAITypeEditPullDown",
            0,
            self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getUnitAIType(),
        )

        self.m_tabCtrlEdit.addSectionButton(
            text("TXT_KEY_WB_ADD_SCRIPT"),
            "CvScreensInterface",
            "WorldBuilderHandleUnitEditAddScriptCB",
            "UnitEditAddScript",
            0,
        )

        initWBToolEditCtrlTab(True)

        if not self.m_tabCtrlEdit.isNone():
            self.m_normalPlayerTabCtrl.enable(False)
            self.m_normalMapTabCtrl.enable(False)
            self.m_bCtrlEditUp = True
        return

    def setCityEditInfo(self):
        self.m_bUnitEditCtrl = False
        self.m_bCityEditCtrl = True

        if self.m_bFlyout:
            self.m_bFlyout = False
            self.m_pCurrentPlot = self.m_pFlyoutPlot

        initWBToolEditCtrl()
        self.m_tabCtrlEdit = getWBToolEditTabCtrl()
        self.m_pActivePlot = self.m_pCurrentPlot

        self.m_tabCtrlEdit.setNumColumns((gc.getNumBuildingInfos() / 10) + 2)
        self.m_tabCtrlEdit.setColumnLength(20)
        self.m_tabCtrlEdit.addTabSection(text("TXT_KEY_WB_CITY_DATA"))
        strName = self.m_pActivePlot.getPlotCity().getName()
        self.m_tabCtrlEdit.addSectionEditCtrl(
            strName, "CvScreensInterface", "WorldBuilderHandleCityEditNameCB", "CityEditName", 0
        )
        self.m_tabCtrlEdit.addSectionLabel(text("TXT_KEY_WB_POPULATION"), 0)
        strPopulation = str("CityEditPopulationCB")
        self.m_tabCtrlEdit.addSectionSpinner(
            strPopulation,
            "CvScreensInterface",
            "WorldBuilderHandleCityEditPopulationCB",
            "CityEditPopulation",
            0,
            1.0,
            1000.0,
            1.0,
            self.m_pActivePlot.getPlotCity().getPopulation(),
            0,
            0,
        )
        self.m_tabCtrlEdit.addSectionLabel(text("TXT_KEY_WB_CULTURE"), 0)
        strCulture = str("CityEditCultureCB")
        self.m_tabCtrlEdit.addSectionSpinner(
            strCulture,
            "CvScreensInterface",
            "WorldBuilderHandleCityEditCultureCB",
            "CityEditCulture",
            0,
            1.0,
            100000000.0,
            1.0,
            self.m_pActivePlot.getPlotCity().getCulture(
                self.m_pActivePlot.getPlotCity().getOwner()
            ),
            0,
            0,
        )
        self.m_tabCtrlEdit.addSectionLabel(text("TXT_KEY_WB_GOLD"), 0)
        strGold = str("CityEditGoldCB")
        self.m_tabCtrlEdit.addSectionSpinner(
            strGold,
            "CvScreensInterface",
            "WorldBuilderHandleCityEditGoldCB",
            "CityEditGold",
            0,
            -1000.0,
            5000.0,
            1.0,
            gc.getPlayer(self.m_iCurrentPlayer).getGold(),
            0,
            0,
        )
        self.m_tabCtrlEdit.addSectionButton(
            text("TXT_KEY_WB_ADD_SCRIPT"),
            "CvScreensInterface",
            "WorldBuilderHandleCityEditAddScriptCB",
            "CityEditAddScript",
            0,
        )

        initWBToolEditCtrlTab(False)

        if not self.m_tabCtrlEdit.isNone():
            self.m_normalPlayerTabCtrl.enable(False)
            self.m_normalMapTabCtrl.enable(False)
            self.m_bCtrlEditUp = True
        return

    def initCityEditScreen(self):
        self.setCityEditInfo()
        return

    def toggleUnitEditCB(self):
        self.setMode(None)
        self.m_bUnitEdit = True
        self.m_bCityEdit = False
        self.m_bNormalPlayer = False
        self.m_bNormalMap = False
        self.m_bReveal = False
        self.m_bDiplomacy = False
        self.m_bLandmark = False
        self.m_bEraseAll = False
        CvScreensInterface.hideWorldBuilderDiplomacyScreen()

        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.enable(False)

        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)

        self.refreshSideMenu()
        self.setCurrentModeCheckbox(self.m_iUnitEditCheckboxID)
        self.m_normalPlayerTabCtrl.enable(False)
        self.m_normalMapTabCtrl.enable(False)
        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.destroy()
        return

    def toggleCityEditCB(self):
        self.setMode(None)
        self.m_bCityEdit = True
        self.m_bUnitEdit = False
        self.m_bNormalPlayer = False
        self.m_bNormalMap = False
        self.m_bReveal = False
        self.m_bDiplomacy = False
        self.m_bLandmark = False
        self.m_bEraseAll = False
        CvScreensInterface.hideWorldBuilderDiplomacyScreen()

        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.enable(False)

        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)

        self.refreshSideMenu()
        self.setCurrentModeCheckbox(self.m_iCityEditCheckboxID)
        self.m_normalPlayerTabCtrl.enable(False)
        self.m_normalMapTabCtrl.enable(False)
        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.destroy()
        return

    def normalPlayerTabModeCB(self):
        self.setMode(None)
        self.m_bCityEdit = False
        self.m_bUnitEdit = False
        self.m_bNormalPlayer = True
        self.m_bNormalMap = False
        self.m_bReveal = False
        self.m_bDiplomacy = False
        self.m_bLandmark = False
        self.m_bEraseAll = False
        CvScreensInterface.hideWorldBuilderDiplomacyScreen()

        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)

        self.refreshSideMenu()
        self.setCurrentModeCheckbox(self.m_iNormalPlayerCheckboxID)
        if self.m_normalMapTabCtrl:
            self.m_normalMapTabCtrl.enable(False)
        if not self.m_normalPlayerTabCtrl.isEnabled() and not CyInterface().isInAdvancedStart():
            self.m_normalPlayerTabCtrl.enable(True)
            if self.m_tabCtrlEdit:
                self.m_tabCtrlEdit.enable(False)
            self.m_bCtrlEditUp = False
        return

    def normalMapTabModeCB(self):
        self.setMode(None)
        self.m_bCityEdit = False
        self.m_bUnitEdit = False
        self.m_bNormalPlayer = False
        self.m_bNormalMap = True
        self.m_bReveal = False
        self.m_bDiplomacy = False
        self.m_bLandmark = False
        self.m_bEraseAll = False
        CvScreensInterface.hideWorldBuilderDiplomacyScreen()

        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)

        self.refreshSideMenu()
        self.setCurrentModeCheckbox(self.m_iNormalMapCheckboxID)
        if self.m_normalPlayerTabCtrl:
            self.m_normalPlayerTabCtrl.enable(False)
        if not self.m_normalMapTabCtrl.isEnabled() and not CyInterface().isInAdvancedStart():
            self.m_normalMapTabCtrl.enable(True)
            if self.m_tabCtrlEdit:
                self.m_tabCtrlEdit.enable(False)
            self.m_bCtrlEditUp = False
        return

    def revealTabModeCB(self):
        self.setMode(self.revealMode)
        self.m_bCtrlEditUp = False
        self.m_bCityEdit = False
        self.m_bUnitEdit = False
        self.m_bNormalPlayer = False
        self.m_bNormalMap = False
        self.m_bReveal = True
        self.m_bDiplomacy = False
        self.m_bLandmark = False
        self.m_bEraseAll = False
        CvScreensInterface.hideWorldBuilderDiplomacyScreen()

        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
        self.refreshReveal()
        self.refreshSideMenu()
        self.setCurrentModeCheckbox(self.m_iRevealTileCheckboxID)
        if self.m_normalPlayerTabCtrl:
            self.m_normalPlayerTabCtrl.enable(False)
        if self.m_normalMapTabCtrl:
            self.m_normalMapTabCtrl.enable(False)
        if self.m_tabCtrlEdit:
            self.m_tabCtrlEdit.enable(False)
        return

    def diplomacyModeCB(self):
        self.setMode(None)
        self.m_bCtrlEditUp = False
        self.m_bCityEdit = False
        self.m_bUnitEdit = False
        self.m_bNormalPlayer = False
        self.m_bNormalMap = False
        self.m_bReveal = False
        self.m_bDiplomacy = True
        self.m_bLandmark = False
        self.m_bEraseAll = False

        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
        self.refreshSideMenu()
        self.setCurrentModeCheckbox(self.m_iDiplomacyCheckboxID)
        if self.m_normalPlayerTabCtrl != 0:
            self.m_normalPlayerTabCtrl.enable(False)
        if self.m_normalMapTabCtrl != 0:
            self.m_normalMapTabCtrl.enable(False)
        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.enable(False)

        CvScreensInterface.showWorldBuilderDiplomacyScreen()
        return

    def landmarkModeCB(self):
        self.setMode(self.landmarkMode)
        self.m_bCtrlEditUp = False
        self.m_bCityEdit = False
        self.m_bUnitEdit = False
        self.m_bNormalPlayer = False
        self.m_bNormalMap = False
        self.m_bReveal = False
        self.m_bDiplomacy = False
        self.m_bLandmark = True
        self.m_bEraseAll = False
        CvScreensInterface.hideWorldBuilderDiplomacyScreen()
        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
        self.refreshSideMenu()
        self.setCurrentModeCheckbox(self.m_iLandmarkCheckboxID)
        if self.m_normalPlayerTabCtrl != 0:
            self.m_normalPlayerTabCtrl.enable(False)
        if self.m_normalMapTabCtrl != 0:
            self.m_normalMapTabCtrl.enable(False)
        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.enable(False)
        return

    def eraseCB(self):
        self.setMode(None)
        self.m_bCtrlEditUp = False
        self.m_bCityEdit = False
        self.m_bUnitEdit = False
        self.m_bNormalPlayer = False
        self.m_bNormalMap = False
        self.m_bReveal = False
        self.m_bDiplomacy = False
        self.m_bLandmark = False
        self.m_bEraseAll = True
        self.m_pRiverStartPlot = -1
        CvScreensInterface.hideWorldBuilderDiplomacyScreen()

        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
        self.refreshSideMenu()
        self.setCurrentModeCheckbox(self.m_iEraseCheckboxID)
        if self.m_normalPlayerTabCtrl != 0:
            self.m_normalPlayerTabCtrl.enable(False)
        if self.m_normalMapTabCtrl != 0:
            self.m_normalMapTabCtrl.enable(False)
        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.enable(False)
        return

    def createFlyoutMenu(self):
        if self.m_pCurrentPlot == 0:
            return
        self.m_flyoutMenu = CyGFlyoutMenu()
        self.m_pFlyoutPlot = self.m_pCurrentPlot
        if self.m_pFlyoutPlot.getNumUnits() > 0:
            for i in range(self.m_pFlyoutPlot.getNumUnits()):
                if len(self.m_pFlyoutPlot.getUnit(i).getNameNoDesc()):
                    strName = self.m_pFlyoutPlot.getUnit(i).getNameNoDesc()
                else:
                    strName = self.m_pFlyoutPlot.getUnit(i).getName()
                self.m_flyoutMenu.addTextItem(
                    strName, "CvScreensInterface", "WorldBuilderHandleFlyoutMenuCB", i + 1
                )
        if self.m_pFlyoutPlot.isCity():
            self.m_flyoutMenu.addTextItem(
                text("TXT_KEY_WB_EDIT_CITY"),
                "CvScreensInterface",
                "WorldBuilderHandleFlyoutMenuCB",
                self.m_iFlyoutEditCity,
            )

        self.m_flyoutMenu.addTextItem(
            text("TXT_KEY_WB_ADD_SCRIPT_TO_PLOT"),
            "CvScreensInterface",
            "WorldBuilderHandleFlyoutMenuCB",
            self.m_iFlyoutAddScript,
        )
        self.m_flyoutMenu.addTextItem(
            text("TXT_KEY_WB_CHANGE_START_YEAR"),
            "CvScreensInterface",
            "WorldBuilderHandleFlyoutMenuCB",
            self.m_iFlyoutChangeStartYear,
        )
        self.m_flyoutMenu.show()
        return

    def destroyFlyoutMenu(self):
        if self.m_flyoutMenu != 0:
            self.m_flyoutMenu.destroy()
            self.m_flyoutMenu = 0
        return

    def handleFlyoutMenuCB(self, argsList):
        iFlyoutIndex = int(argsList[0])
        if self.m_tabCtrlEdit != 0:
            self.m_tabCtrlEdit.enable(False)
        if iFlyoutIndex == self.m_iFlyoutAddScript:
            self.m_pPlotToScript = self.m_pFlyoutPlot
            self.getScript()
        elif iFlyoutIndex == self.m_iFlyoutChangeStartYear:
            self.getNewStartYear()
        elif iFlyoutIndex == self.m_iFlyoutEditCity:
            self.m_normalPlayerTabCtrl.enable(False)
            self.m_normalMapTabCtrl.enable(False)
            self.m_bFlyout = True
            self.initCityEditScreen()
        else:
            self.m_normalPlayerTabCtrl.enable(False)
            self.m_normalMapTabCtrl.enable(False)
            self.m_iCurrentUnit = iFlyoutIndex - 1
            self.m_bFlyout = True
            self.setUnitEditInfo(False)
        return 1

    def setCurrentNormalPlayerIndex(self, argsList):
        iIndex = int(argsList)
        if self.m_normalPlayerTabCtrl.getActiveTab() != self.m_iTechnologyTabID:
            self.m_iNormalPlayerCurrentIndexes[self.m_normalPlayerTabCtrl.getActiveTab()] = int(
                argsList
            )
        else:
            bOn = gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).isHasTech(iIndex)
            bOn = not bOn
            gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).setHasTech(
                iIndex, bOn, self.m_iCurrentPlayer, False, False
            )
        return 1

    def setCurrentNormalMapIndex(self, argsList):
        iIndex = int(argsList)
        self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] = int(argsList)
        return 1

    def setCurrentNormalMapList(self, argsList):
        self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] = int(argsList)
        return 1

    def setCurrentAdvancedStartIndex(self, argsList):
        iIndex = int(argsList)
        self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()] = int(
            argsList
        )
        return 1

    def setCurrentAdvancedStartList(self, argsList):
        self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] = int(
            argsList
        )
        return 1

    def setEditButtonClicked(self, argsList):
        iIndex = int(argsList)
        if self.m_bUnitEditCtrl:
            bOn = not self.m_pActivePlot.getUnit(self.m_iCurrentUnit).isHasPromotion(iIndex)
            self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setHasPromotion(iIndex, bOn)
        elif self.m_bCityEditCtrl:
            if self.m_pActivePlot.getPlotCity().getNumBuilding(iIndex) > 0:
                iNum = 0
            else:
                iNum = 1
            self.m_pActivePlot.getPlotCity().setNumRealBuilding(iIndex, iNum)
        return 1

    def setEditReligionSelected(self, argsList):
        iReligion = int(argsList)
        bOn = not self.m_pActivePlot.getPlotCity().isHasReligion(iReligion)
        self.m_pActivePlot.getPlotCity().setHasReligion(iReligion, bOn, False, False)
        if not bOn:
            gc.getGame().clearHolyCity(iReligion)

        refreshWBEditCtrlReligionButtons(True)
        return 1

    def setEditHolyCitySelected(self, argsList):
        iReligion = int(argsList)

        if self.m_pActivePlot.getPlotCity().isHolyCityByType(iReligion):
            gc.getGame().clearHolyCity(iReligion)
        else:
            gc.getGame().setHolyCity(iReligion, self.m_pActivePlot.getPlotCity(), False)

        refreshWBEditCtrlReligionButtons(False)
        return 1

    def setEditCorporationSelected(self, argsList):
        iCorporation = int(argsList)
        bOn = not self.m_pActivePlot.getPlotCity().isHasCorporation(iCorporation)
        self.m_pActivePlot.getPlotCity().setHasCorporation(iCorporation, bOn, False, False)
        if not bOn:
            gc.getGame().clearHeadquarters(iCorporation)

        refreshWBEditCtrlCorporationButtons(True)
        return 1

    def setEditHeadquartersSelected(self, argsList):
        iCorporation = int(argsList)

        if self.m_pActivePlot.getPlotCity().isHeadquartersByType(iCorporation):
            gc.getGame().clearHeadquarters(iCorporation)
        else:
            gc.getGame().setHeadquarters(iCorporation, self.m_pActivePlot.getPlotCity(), False)

        refreshWBEditCtrlCorporationButtons(False)
        return 1

    def getUnitTabID(self):
        return self.m_iUnitTabID

    def getBuildingTabID(self):
        return self.m_iBuildingTabID

    def getTechnologyTabID(self):
        return self.m_iTechnologyTabID

    def getImprovementTabID(self):
        return self.m_iImprovementTabID

    def getBonusTabID(self):
        return self.m_iBonusTabID

    def getImprovementListID(self):
        return self.m_iImprovementListID

    def getBonusListID(self):
        return self.m_iBonusListID

    def getTerrainTabID(self):
        return self.m_iTerrainTabID

    def getTerrainListID(self):
        return self.m_iTerrainListID

    def getFeatureListID(self):
        return self.m_iFeatureListID

    def getPlotTypeListID(self):
        return self.m_iPlotTypeListID

    def getRouteListID(self):
        return self.m_iRouteListID

    def getTerritoryTabID(self):
        return self.m_iTerritoryTabID

    def getTerritoryListID(self):
        return self.m_iTerritoryListID

    def getASUnitTabID(self):
        return self.m_iASUnitTabID

    def getASUnitListID(self):
        return self.m_iASUnitListID

    def getASCityTabID(self):
        return self.m_iASCityTabID

    def getASCityListID(self):
        return self.m_iASCityListID

    def getASBuildingsListID(self):
        return self.m_iASBuildingsListID

    def getASAutomateListID(self):
        return self.m_iASAutomateListID

    def getASImprovementsTabID(self):
        return self.m_iASImprovementsTabID

    def getASRoutesListID(self):
        return self.m_iASRoutesListID

    def getASImprovementsListID(self):
        return self.m_iASImprovementsListID

    def getASVisibilityTabID(self):
        return self.m_iASVisibilityTabID

    def getASVisibilityListID(self):
        return self.m_iASVisibilityListID

    def getASTechTabID(self):
        return self.m_iASTechTabID

    def getASTechListID(self):
        return self.m_iASTechListID

    def highlightBrush(self):

        if self.m_bShowBigBrush:
            if self.m_pCurrentPlot == 0:
                return

            CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
            CyEngine().fillAreaBorderPlotAlt(
                self.m_pCurrentPlot.getX(),
                self.m_pCurrentPlot.getY(),
                AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                "COLOR_GREEN",
                1,
            )
            for i in range((self.m_iBrushWidth - 1)):
                for j in range((self.m_iBrushHeight)):
                    pPlot = CyMap().plot(
                        self.m_pCurrentPlot.getX() - (i + 1), self.m_pCurrentPlot.getY() - (j)
                    )
                    if not pPlot.isNone():
                        CyEngine().fillAreaBorderPlotAlt(
                            pPlot.getX(),
                            pPlot.getY(),
                            AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                            "COLOR_GREEN",
                            1,
                        )
                    pPlot = CyMap().plot(
                        self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY() - (j)
                    )
                    if not pPlot.isNone():
                        CyEngine().fillAreaBorderPlotAlt(
                            pPlot.getX(),
                            pPlot.getY(),
                            AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                            "COLOR_GREEN",
                            1,
                        )
                    pPlot = CyMap().plot(
                        self.m_pCurrentPlot.getX() + (i + 1), self.m_pCurrentPlot.getY() - (j)
                    )
                    if not pPlot.isNone():
                        CyEngine().fillAreaBorderPlotAlt(
                            pPlot.getX(),
                            pPlot.getY(),
                            AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                            "COLOR_GREEN",
                            1,
                        )
                    pPlot = CyMap().plot(
                        self.m_pCurrentPlot.getX() - (i + 1), self.m_pCurrentPlot.getY() + (j)
                    )
                    if not pPlot.isNone():
                        CyEngine().fillAreaBorderPlotAlt(
                            pPlot.getX(),
                            pPlot.getY(),
                            AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                            "COLOR_GREEN",
                            1,
                        )
                    pPlot = CyMap().plot(
                        self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY() + (j)
                    )
                    if not pPlot.isNone():
                        CyEngine().fillAreaBorderPlotAlt(
                            pPlot.getX(),
                            pPlot.getY(),
                            AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                            "COLOR_GREEN",
                            1,
                        )
                    pPlot = CyMap().plot(
                        self.m_pCurrentPlot.getX() + (i + 1), self.m_pCurrentPlot.getY() + (j)
                    )
                    if not pPlot.isNone():
                        CyEngine().fillAreaBorderPlotAlt(
                            pPlot.getX(),
                            pPlot.getY(),
                            AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                            "COLOR_GREEN",
                            1,
                        )
            if not self.m_iBrushWidth:
                pPlot = CyMap().plot(self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY())
                if not pPlot.isNone():
                    CyEngine().fillAreaBorderPlotAlt(
                        pPlot.getX(),
                        pPlot.getY(),
                        AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                        "COLOR_GREEN",
                        1,
                    )
                for j in range((self.m_iBrushHeight)):
                    pPlot = CyMap().plot(
                        self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY() - (j)
                    )
                    if not pPlot.isNone():
                        CyEngine().fillAreaBorderPlotAlt(
                            pPlot.getX(),
                            pPlot.getY(),
                            AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                            "COLOR_GREEN",
                            1,
                        )
                    pPlot = CyMap().plot(
                        self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY() - (j)
                    )
                    if not pPlot.isNone():
                        CyEngine().fillAreaBorderPlotAlt(
                            pPlot.getX(),
                            pPlot.getY(),
                            AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                            "COLOR_GREEN",
                            1,
                        )

        return

    def placeMultipleObjects(self):
        bInsideForLoop = False
        permCurrentPlot = self.m_pCurrentPlot
        for i in range((self.m_iBrushWidth - 1)):
            for j in range((self.m_iBrushHeight)):
                bInsideForLoop = True
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX() - (i + 1), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.placeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX(), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.placeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX() + (i + 1), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.placeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX() - (i + 1), permCurrentPlot.getY() + (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.placeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX(), permCurrentPlot.getY() + (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.placeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX() + (i + 1), permCurrentPlot.getY() + (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.placeObject()
        if not bInsideForLoop:
            self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY())
            if not self.m_pCurrentPlot.isNone():
                self.placeObject()
            for j in range((self.m_iBrushHeight)):
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX(), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.placeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX(), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.placeObject()
        self.m_pCurrentPlot = permCurrentPlot
        return

    def removeMultipleObjects(self):
        bInsideForLoop = False
        permCurrentPlot = self.m_pCurrentPlot
        for i in range((self.m_iBrushWidth - 1)):
            for j in range((self.m_iBrushHeight)):
                bInsideForLoop = True
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX() - (i + 1), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.removeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX(), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.removeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX() + (i + 1), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.removeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX() - (i + 1), permCurrentPlot.getY() + (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.removeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX(), permCurrentPlot.getY() + (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.removeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX() + (i + 1), permCurrentPlot.getY() + (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.removeObject()
        if not bInsideForLoop:
            self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY())
            if not self.m_pCurrentPlot.isNone():
                self.removeObject()
            for j in range((self.m_iBrushHeight)):
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX(), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.removeObject()
                self.m_pCurrentPlot = CyMap().plot(
                    permCurrentPlot.getX(), permCurrentPlot.getY() - (j)
                )
                if not self.m_pCurrentPlot.isNone():
                    self.removeObject()
        self.m_pCurrentPlot = permCurrentPlot
        return

    def showMultipleReveal(self):
        self.refreshReveal()
        return

    def setMultipleReveal(self, bReveal):

        # Caliom: had to change the loop because Firaxis implementation covered some plots several times. Had to ensure that each plot is called only once.
        # Rectangle size and Brushsize are not equal. Firaxis mapping is
        # Rectangle: 1x1 Brush 1x1
        # Rectangle: 3x3 Brush 2x2
        # Rectangle: 5x5 Brush 3x3
        # bInsideForLoop = False
        permCurrentPlot = self.m_pCurrentPlot

        iLowerLeftX = self.m_pCurrentPlot.getX() - self.m_iBrushWidth + 1
        iLowerLeftY = self.m_pCurrentPlot.getY() - self.m_iBrushHeight + 1
        iRectangleWidth = 2 * self.m_iBrushWidth - 1
        iRectangleHeight = 2 * self.m_iBrushHeight - 1
        for i in range(iRectangleWidth):
            for j in range(iRectangleHeight):
                self.m_pCurrentPlot = CyMap().plot(iLowerLeftX + i, iLowerLeftY + j)
                if not self.m_pCurrentPlot.isNone():
                    self.RevealCurrentPlot(bReveal)
        # Caliom end
        self.m_pCurrentPlot = permCurrentPlot
        self.showMultipleReveal()
        return

    def useLargeBrush(self):
        if ((self.m_bNormalMap) and (not self.m_bUnitEdit) and (not self.m_bCityEdit)) and (
            (
                (self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerrainTabID)
                and (
                    (
                        self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                        == self.m_iTerrainListID
                    )
                    or (
                        self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                        == self.m_iFeatureListID
                    )
                    or (
                        self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()]
                        == self.m_iPlotTypeListID
                    )
                )
            )
            or ((self.m_normalMapTabCtrl.getActiveTab() == self.m_iBonusTabID))
            or ((self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerritoryTabID))
        ):
            return True
        elif self.m_bReveal:
            return True
        else:
            return False

    def clearSideMenu(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        screen.deleteWidget("WorldBuilderMainPanel")
        screen.deleteWidget("WorldBuilderBackgroundPanel")

        screen.deleteWidget("WorldBuilderSaveButton")
        screen.deleteWidget("WorldBuilderLoadButton")
        screen.deleteWidget("WorldBuilderAllPlotsButton")
        screen.deleteWidget("WorldBuilderExitButton")

        screen.deleteWidget("WorldBuilderUnitEditMode")
        screen.deleteWidget("WorldBuilderCityEditMode")

        screen.deleteWidget("WorldBuilderNormalPlayerMode")
        screen.deleteWidget("WorldBuilderNormalMapMode")
        screen.deleteWidget("WorldBuilderRevealMode")

        screen.deleteWidget("WorldBuilderPlayerChoice")
        screen.deleteWidget("WorldBuilderTechByEra")
        screen.deleteWidget("WorldBuilderBrushSize")
        screen.deleteWidget("WorldBuilderRegenerateMap")
        screen.deleteWidget("WorldBuilderTeamChoice")

        screen.deleteWidget("WorldBuilderRevealAll")
        screen.deleteWidget("WorldBuilderUnrevealAll")
        screen.deleteWidget("WorldBuilderRevealPanel")

        screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
        return

    def setSideMenu(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)

        iMaxScreenWidth = screen.getXResolution()
        iMaxScreenHeight = screen.getYResolution()
        iScreenHeight = 10 + 37 + 37

        iButtonWidth = 32
        iButtonHeight = 32
        iButtonX = 0
        iButtonY = 0

        if CyInterface().isInAdvancedStart():
            iX = 0
        else:
            iX = iMaxScreenWidth - self.iScreenWidth

        screen.addPanel(
            "WorldBuilderBackgroundPanel",
            "",
            "",
            True,
            True,
            iX,
            0,
            self.iScreenWidth,
            iScreenHeight,
            PanelStyles.PANEL_STYLE_MAIN,
        )
        screen.addScrollPanel(
            "WorldBuilderMainPanel",
            "",
            iX,
            0,
            self.iScreenWidth,
            iScreenHeight,
            PanelStyles.PANEL_STYLE_MAIN,
        )

        if CyInterface().isInAdvancedStart():

            iX = 50
            iY = 15
            szText = (
                u"<font=4>"
                + text(
                    "TXT_KEY_WB_AS_POINTS",
                    gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartPoints(),
                )
                + "</font>"
            )
            screen.setLabel(
                "AdvancedStartPointsText",
                "Background",
                szText,
                CvUtil.FONT_LEFT_JUSTIFY,
                iX,
                iY,
                -2,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )

            iY += 30
            szText = text("TXT_KEY_ADVANCED_START_BEGIN_GAME")
            screen.setButtonGFC(
                "WorldBuilderExitButton",
                szText,
                "",
                iX,
                iY,
                130,
                28,
                WidgetTypes.WIDGET_WB_EXIT_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_STANDARD,
            )

            szText = (
                u"<font=4>" + text("TXT_KEY_WB_AS_COST_THIS_LOCATION", self.m_iCost) + u"</font>"
            )
            iY = 85
            screen.setLabel(
                "AdvancedStartCostText",
                "Background",
                szText,
                CvUtil.FONT_LEFT_JUSTIFY,
                iX - 20,
                iY,
                -2,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )

        else:

            iPanelWidth = 35 * 6
            screen.attachPanelAt(
                "WorldBuilderMainPanel",
                "WorldBuilderLoadSavePanel",
                "",
                "",
                False,
                True,
                PanelStyles.PANEL_STYLE_CITY_TANSHADE,
                70,
                0,
                iPanelWidth - 70,
                35,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )

            screen.setImageButtonAt(
                "WorldBuilderAllPlotsButton",
                "WorldBuilderLoadSavePanel",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_CHANGE_ALL_PLOTS").getPath(),
                iButtonX,
                iButtonY,
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_ALL_PLOTS_BUTTON,
                -1,
                -1,
            )
            iButtonX = iButtonX + 35
            screen.setImageButtonAt(
                "WorldBuilderSaveButton",
                "WorldBuilderLoadSavePanel",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_SAVE").getPath(),
                iButtonX,
                iButtonY,
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_SAVE_BUTTON,
                -1,
                -1,
            )
            iButtonX = iButtonX + 35
            screen.setImageButtonAt(
                "WorldBuilderLoadButton",
                "WorldBuilderLoadSavePanel",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_LOAD").getPath(),
                iButtonX,
                iButtonY,
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_LOAD_BUTTON,
                -1,
                -1,
            )
            iButtonX = iButtonX + 35
            screen.setImageButtonAt(
                "WorldBuilderExitButton",
                "WorldBuilderLoadSavePanel",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_EXIT").getPath(),
                iButtonX,
                iButtonY,
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_EXIT_BUTTON,
                -1,
                -1,
            )

            iButtonWidth = 32
            iButtonHeight = 32
            iButtonX = 0
            iButtonY = 0
            self.m_iUnitEditCheckboxID = 0
            screen.addCheckBoxGFC(
                "WorldBuilderUnitEditModeButton",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_TOGGLE_UNIT_EDIT_MODE").getPath(),
                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                (10 + 36),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_UNIT_EDIT_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )

            iButtonX = iButtonX + 35
            self.m_iCityEditCheckboxID = 1
            screen.addCheckBoxGFC(
                "WorldBuilderCityEditModeButton",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_TOGGLE_CITY_EDIT_MODE").getPath(),
                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                (10 + 36),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_CITY_EDIT_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )

            iButtonX = iButtonX + 35
            self.m_iNormalPlayerCheckboxID = 2
            screen.addCheckBoxGFC(
                "WorldBuilderNormalPlayerModeButton",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_NORMAL_UNIT_MODE").getPath(),
                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                (10 + 36),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_NORMAL_PLAYER_TAB_MODE_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )

            iButtonX = iButtonX + 35
            self.m_iNormalMapCheckboxID = 3
            screen.addCheckBoxGFC(
                "WorldBuilderNormalMapModeButton",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_NORMAL_MAP_MODE").getPath(),
                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                (10 + 36),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_NORMAL_MAP_TAB_MODE_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )

            iButtonX = iButtonX + 35
            self.m_iRevealTileCheckboxID = 4
            screen.addCheckBoxGFC(
                "WorldBuilderRevealTileModeButton",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_REVEAL_TILE_MODE").getPath(),
                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                (10 + 36),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_REVEAL_TAB_MODE_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )

            iButtonX = iButtonX + 35
            self.m_iDiplomacyCheckboxID = 5
            screen.addCheckBoxGFC(
                "WorldBuilderDiplomacyModeButton",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_DIPLOMACY_MODE").getPath(),
                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                (10 + 36),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_DIPLOMACY_MODE_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )

            iButtonX = 0
            self.m_iLandmarkCheckboxID = 6
            screen.addCheckBoxGFC(
                "WorldBuilderLandmarkButton",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_LANDMARK_MODE").getPath(),
                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                (10),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_LANDMARK_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )

            iButtonX = iButtonX + 35
            self.m_iEraseCheckboxID = 7
            screen.addCheckBoxGFC(
                "WorldBuilderEraseButton",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_ERASE").getPath(),
                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                (10),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_ERASE_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )

            self.setCurrentModeCheckbox(self.m_iNormalPlayerCheckboxID)

        return

    def refreshSideMenu(self):

        if self.currentMode is not None:
            return

        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)

        iMaxScreenWidth = screen.getXResolution()
        iMaxScreenHeight = screen.getYResolution()
        iScreenHeight = 10 + 37 + 37

        if CyInterface().isInAdvancedStart():

            iX = 50
            iY = 15
            szText = (
                u"<font=4>"
                + text(
                    "TXT_KEY_WB_AS_POINTS",
                    gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartPoints(),
                )
                + "</font>"
            )
            screen.setLabel(
                "AdvancedStartPointsText",
                "Background",
                szText,
                CvUtil.FONT_LEFT_JUSTIFY,
                iX,
                iY,
                -2,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )

            szText = (
                u"<font=4>" + text("TXT_KEY_WB_AS_COST_THIS_LOCATION", self.m_iCost) + u"</font>"
            )
            iY = 85
            screen.setLabel(
                "AdvancedStartCostText",
                "Background",
                szText,
                CvUtil.FONT_LEFT_JUSTIFY,
                iX - 20,
                iY,
                -2,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )

        else:

            screen.deleteWidget("WorldBuilderPlayerChoice")
            screen.deleteWidget("WorldBuilderTechByEra")
            screen.deleteWidget("WorldBuilderBrushSize")
            screen.deleteWidget("WorldBuilderRegenerateMap")
            screen.deleteWidget("WorldBuilderTeamChoice")
            screen.deleteWidget("WorldBuilderRevealAll")
            screen.deleteWidget("WorldBuilderUnrevealAll")
            screen.deleteWidget("WorldBuilderRevealPanel")
            screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
            iPanelWidth = 35 * 6
            if self.m_bReveal or (
                self.m_bNormalPlayer and (not self.m_bUnitEdit) and (not self.m_bCityEdit)
            ):
                screen.addPanel(
                    "WorldBuilderBackgroundBottomPanel",
                    "",
                    "",
                    True,
                    True,
                    iMaxScreenWidth - self.iScreenWidth,
                    10 + 32 + 32,
                    self.iScreenWidth,
                    45 + 40,
                    PanelStyles.PANEL_STYLE_MAIN,
                )
            else:
                screen.addPanel(
                    "WorldBuilderBackgroundBottomPanel",
                    "",
                    "",
                    True,
                    True,
                    iMaxScreenWidth - self.iScreenWidth,
                    10 + 32 + 32,
                    self.iScreenWidth,
                    45,
                    PanelStyles.PANEL_STYLE_MAIN,
                )

            if self.m_bNormalPlayer and (not self.m_bUnitEdit) and (not self.m_bCityEdit):
                szDropdownName = str("WorldBuilderPlayerChoice")
                screen.addDropDownBoxGFC(
                    szDropdownName,
                    (iMaxScreenWidth - self.iScreenWidth) + 8,
                    (10 + 36 + 36),
                    iPanelWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in range(gc.getMAX_CIV_PLAYERS()):
                    if gc.getPlayer(i).isEverAlive():
                        if i == self.m_iCurrentPlayer:
                            screen.addPullDownString(
                                szDropdownName, gc.getPlayer(i).getName(), i, i, True
                            )
                        else:
                            screen.addPullDownString(
                                szDropdownName, gc.getPlayer(i).getName(), i, i, False
                            )

                if gc.getBARBARIAN_PLAYER() == self.m_iCurrentPlayer:
                    screen.addPullDownString(
                        szDropdownName,
                        gc.getPlayer(gc.getBARBARIAN_PLAYER()).getName(),
                        gc.getBARBARIAN_PLAYER(),
                        gc.getBARBARIAN_PLAYER(),
                        True,
                    )
                else:
                    screen.addPullDownString(
                        szDropdownName,
                        gc.getPlayer(gc.getBARBARIAN_PLAYER()).getName(),
                        gc.getBARBARIAN_PLAYER(),
                        gc.getBARBARIAN_PLAYER(),
                        False,
                    )
                # Loop through Era Infos and add names
                szDropdownName = str("WorldBuilderTechByEra")
                screen.addDropDownBoxGFC(
                    szDropdownName,
                    (iMaxScreenWidth - self.iScreenWidth) + 8,
                    (10 + 36 + 36 + 36),
                    iPanelWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in range(gc.getNumEraInfos()):
                    szPullDownString = text(
                        "TXT_KEY_WB_ADD_ERA_TECH", gc.getEraInfo(i).getTextKey()
                    )
                    screen.addPullDownString(szDropdownName, szPullDownString, i, i, True)
                screen.addPullDownString(
                    szDropdownName, text("TXT_KEY_WB_ADD_ERA_TECH_DESC"), i, i, True
                )
            elif self.m_bNormalMap and (not self.m_bUnitEdit) and (not self.m_bCityEdit):
                iButtonWidth = 32
                iButtonHeight = 32
                iButtonX = 0
                iButtonY = 0
                screen.setImageButton(
                    "WorldBuilderRegenerateMap",
                    ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_REVEAL_ALL_TILES").getPath(),
                    (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                    (10 + 36 + 36),
                    iButtonWidth,
                    iButtonHeight,
                    WidgetTypes.WIDGET_WB_REGENERATE_MAP,
                    -1,
                    -1,
                )

                szDropdownName = str("WorldBuilderBrushSize")
                screen.addDropDownBoxGFC(
                    szDropdownName,
                    (iMaxScreenWidth - self.iScreenWidth) + 48,
                    (10 + 36 + 36),
                    iPanelWidth - 40,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                bActive = False
                if self.m_iBrushWidth == 1:
                    bActive = True
                else:
                    bActive = False
                screen.addPullDownString(szDropdownName, text("TXT_KEY_WB_1_BY_1"), 1, 1, bActive)
                if self.m_iBrushWidth == 2:
                    bActive = True
                else:
                    bActive = False
                screen.addPullDownString(szDropdownName, text("TXT_KEY_WB_3_BY_3"), 2, 2, bActive)
                if self.m_iBrushWidth == 3:
                    bActive = True
                else:
                    bActive = False
                screen.addPullDownString(szDropdownName, text("TXT_KEY_WB_5_BY_5"), 3, 3, bActive)

            elif self.m_bReveal:
                iPanelWidth = 35 * 6
                iButtonWidth = 32
                iButtonHeight = 32
                iButtonX = 0
                iButtonY = 0
                screen.setImageButton(
                    "WorldBuilderRevealAll",
                    ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_REVEAL_ALL_TILES").getPath(),
                    (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                    (10 + 36 + 36),
                    iButtonWidth,
                    iButtonHeight,
                    WidgetTypes.WIDGET_WB_REVEAL_ALL_BUTTON,
                    -1,
                    -1,
                )
                iButtonX = iButtonX + 35
                screen.setImageButton(
                    "WorldBuilderUnrevealAll",
                    ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_UNREVEAL_ALL_TILES").getPath(),
                    (iMaxScreenWidth - self.iScreenWidth) + 8 + iButtonX,
                    (10 + 36 + 36),
                    iButtonWidth,
                    iButtonHeight,
                    WidgetTypes.WIDGET_WB_UNREVEAL_ALL_BUTTON,
                    -1,
                    -1,
                )
                iButtonX = iButtonX + 35

                szDropdownName = str("WorldBuilderBrushSize")
                screen.addDropDownBoxGFC(
                    szDropdownName,
                    (iMaxScreenWidth - self.iScreenWidth) + 8 + 80,
                    (10 + 36 + 36),
                    iPanelWidth - 80,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                bActive = False
                if self.m_iBrushWidth == 1:
                    bActive = True
                else:
                    bActive = False
                screen.addPullDownString(szDropdownName, text("TXT_KEY_WB_1_BY_1"), 1, 1, bActive)
                if self.m_iBrushWidth == 2:
                    bActive = True
                else:
                    bActive = False
                screen.addPullDownString(szDropdownName, text("TXT_KEY_WB_3_BY_3"), 2, 2, bActive)
                if self.m_iBrushWidth == 3:
                    bActive = True
                else:
                    bActive = False
                screen.addPullDownString(szDropdownName, text("TXT_KEY_WB_5_BY_5"), 3, 3, bActive)

                szDropdownName = str("WorldBuilderTeamChoice")
                screen.addDropDownBoxGFC(
                    szDropdownName,
                    (iMaxScreenWidth - self.iScreenWidth) + 8,
                    (10 + 36 + 36 + 36),
                    iPanelWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in range(gc.getMAX_CIV_TEAMS()):
                    if gc.getTeam(i).isEverAlive():
                        if i == self.m_iCurrentTeam:
                            screen.addPullDownString(
                                szDropdownName, gc.getTeam(i).getName(), i, i, True
                            )
                        else:
                            screen.addPullDownString(
                                szDropdownName, gc.getTeam(i).getName(), i, i, False
                            )
            else:
                screen.deleteWidget("WorldBuilderBackgroundBottomPanel")

        return

    def revealAll(self, bReveal):
        # Caliom begin
        # The reveal stuff is now handled in the reveal mode. Only the revealall/unrevealall functionality is handled in the old code.
        # But the old code does not know if the player was changed in reveal mode. So i have to fetch the player/team here
        self.m_iCurrentPlayer = self.revealMode.iPlayer
        self.m_iCurrentTeam = gc.getPlayer(self.revealMode.iPlayer).getTeam()
        # Caliom end

        for i in range(CyMap().getGridWidth()):
            for j in range(CyMap().getGridHeight()):
                pPlot = CyMap().plot(i, j)
                if not pPlot.isNone():
                    if bReveal or (not pPlot.isVisible(self.m_iCurrentTeam, False)):
                        pPlot.setRevealed(self.m_iCurrentTeam, bReveal, False, -1)
        self.refreshReveal()
        return

    def RevealCurrentPlot(self, bReveal):
        if bReveal or (not self.m_pCurrentPlot.isVisible(self.m_iCurrentTeam, False)):
            self.m_pCurrentPlot.setRevealed(self.m_iCurrentTeam, bReveal, False, -1)
        return

    def showRevealed(self, pPlot):
        if not pPlot.isRevealed(self.m_iCurrentTeam, False):
            CyEngine().fillAreaBorderPlotAlt(
                pPlot.getX(),
                pPlot.getY(),
                AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS,
                "COLOR_BLACK",
                1.0,
            )
        return

    def getNumPlayers(self):
        iCount = 0
        for i in range(gc.getMAX_CIV_PLAYERS()):
            if gc.getPlayer(i).isEverAlive():
                iCount = iCount + 1

        return iCount

    def Exit(self):
        CyInterface().setWorldBuilder(False)
        return

    def setLandmarkCB(self, szLandmark):
        self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
        CyEngine().addLandmarkPopup(self.m_pCurrentPlot)  # , u"%s" %(szLandmark))
        return

    def removeLandmarkCB(self):
        self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
        CyEngine().removeLandmark(self.m_pCurrentPlot)
        return

    def refreshPlayerTabCtrl(self):

        initWBToolPlayerControl()

        self.m_normalPlayerTabCtrl = getWBToolNormalPlayerTabCtrl()

        self.m_normalPlayerTabCtrl.setNumColumns((gc.getNumUnitInfos() / 10) + 2)
        self.m_normalPlayerTabCtrl.addTabSection(text("TXT_KEY_WB_UNITS"))
        self.m_iUnitTabID = 0
        self.m_iNormalPlayerCurrentIndexes.append(0)

        self.m_normalPlayerTabCtrl.setNumColumns((gc.getNumBuildingInfos() / 10) + 1)
        self.m_normalPlayerTabCtrl.addTabSection(text("TXT_KEY_WB_BUILDINGS"))
        self.m_iBuildingTabID = 1
        self.m_iNormalPlayerCurrentIndexes.append(0)

        self.m_normalPlayerTabCtrl.setNumColumns((gc.getNumTechInfos() / 10) + 1)
        self.m_normalPlayerTabCtrl.addTabSection(text("TXT_KEY_WB_TECHNOLOGIES"))
        self.m_iTechnologyTabID = 2
        self.m_iNormalPlayerCurrentIndexes.append(0)

        addWBPlayerControlTabs()
        return

    def refreshAdvancedStartTabCtrl(self, bReuse):

        if CyInterface().isInAdvancedStart():

            if self.m_advancedStartTabCtrl and bReuse:
                iActiveTab = self.m_advancedStartTabCtrl.getActiveTab()
                iActiveList = self.m_iAdvancedStartCurrentList[iActiveTab]
                iActiveIndex = self.m_iAdvancedStartCurrentIndexes[iActiveTab]
            else:
                iActiveTab = 0
                iActiveList = 0
                iActiveIndex = 0

            self.m_iCurrentPlayer = CyGame().getActivePlayer()
            self.m_iCurrentTeam = CyGame().getActiveTeam()
            self.m_iAdvancedStartCurrentIndexes = []
            self.m_iAdvancedStartCurrentList = []

            initWBToolAdvancedStartControl()

            self.m_advancedStartTabCtrl = getWBToolAdvancedStartTabCtrl()

            self.m_advancedStartTabCtrl.setNumColumns((gc.getNumBuildingInfos() / 10) + 2)
            self.m_advancedStartTabCtrl.addTabSection(text("TXT_KEY_WB_AS_CITIES"))
            self.m_iASCityTabID = 0
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iASCityListID = 0
            self.m_iASBuildingsListID = 2
            self.m_iASAutomateListID = 1
            self.m_iAdvancedStartCurrentList.append(self.m_iASCityListID)

            self.m_advancedStartTabCtrl.setNumColumns((gc.getNumUnitInfos() / 10) + 2)
            self.m_advancedStartTabCtrl.addTabSection(text("TXT_KEY_WB_AS_UNITS"))
            self.m_iASUnitTabID = 1
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iAdvancedStartCurrentList.append(0)
            self.m_iASUnitListID = 0

            self.m_advancedStartTabCtrl.setNumColumns((gc.getNumImprovementInfos() / 10) + 2)
            self.m_advancedStartTabCtrl.addTabSection(text("TXT_KEY_WB_AS_IMPROVEMENTS"))
            self.m_iASImprovementsTabID = 2
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iASRoutesListID = 0
            self.m_iASImprovementsListID = 1
            self.m_iAdvancedStartCurrentList.append(self.m_iASRoutesListID)

            self.m_advancedStartTabCtrl.setNumColumns(1)
            self.m_advancedStartTabCtrl.addTabSection(text("TXT_KEY_WB_AS_VISIBILITY"))
            self.m_iASVisibilityTabID = 3
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iAdvancedStartCurrentList.append(0)
            self.m_iASVisibilityListID = 0

            self.m_advancedStartTabCtrl.setNumColumns(1)
            self.m_advancedStartTabCtrl.addTabSection(text("TXT_KEY_WB_AS_TECH"))
            self.m_iASTechTabID = 4
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iAdvancedStartCurrentList.append(0)
            self.m_iASTechListID = 0

            addWBAdvancedStartControlTabs()

            self.m_advancedStartTabCtrl.setActiveTab(iActiveTab)
            self.setCurrentAdvancedStartIndex(iActiveIndex)
            self.setCurrentAdvancedStartList(iActiveList)
        else:

            self.m_advancedStartTabCtrl = getWBToolAdvancedStartTabCtrl()

            self.m_advancedStartTabCtrl.enable(False)

        return

    def eraseAll(self):
        # kill all units on plot if one is selected
        if self.m_pCurrentPlot != 0:
            while self.m_pCurrentPlot.getNumUnits() > 0:
                pUnit = self.m_pCurrentPlot.getUnit(0)
                pUnit.kill(False, PlayerTypes.NO_PLAYER)

            self.m_pCurrentPlot.setBonusType(-1)
            self.m_pCurrentPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)

            if self.m_pCurrentPlot.isCity():
                self.m_pCurrentPlot.getPlotCity().kill()

            self.m_pCurrentPlot.setRouteType(-1)
            self.m_pCurrentPlot.setNOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
            self.m_pCurrentPlot.setWOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
            self.m_pCurrentPlot.setImprovementType(-1)
            self.removeLandmarkCB()
        return

    def getUnitScript(self):
        self.m_pUnitToScript = self.m_pActivePlot.getUnit(self.m_iCurrentUnit)
        self.getScript()
        return

    def getCityScript(self):
        self.m_pCityToScript = self.m_pActivePlot.getPlotCity()
        self.getScript()
        return

    def getScript(self):
        CvEventInterface.beginEvent(CvUtil.EventWBScriptPopup)
        return

    def getNewStartYear(self):
        CvEventInterface.beginEvent(CvUtil.EventWBStartYearPopup)
        return

    def setScriptCB(self, szScript):
        if self.m_pUnitToScript != -1:
            self.m_pUnitToScript.setScriptData(CvUtil.convertToStr(szScript))
            self.m_pUnitToScript = -1
            return

        if self.m_pCityToScript != -1:
            self.m_pCityToScript.setScriptData(CvUtil.convertToStr(szScript))
            self.m_pCityToScript = -1
            return

        if self.m_pPlotToScript != -1:
            self.m_pPlotToScript.setScriptData(CvUtil.convertToStr(szScript))
            self.m_pPlotToScript = -1
            return
        return

    def setStartYearCB(self, iStartYear):
        gc.getGame().setStartYear(iStartYear)
        return

    def getCurrentScript(self):
        if self.m_pUnitToScript != -1:
            return self.m_pUnitToScript.getScriptData()

        if self.m_pCityToScript != -1:
            return self.m_pCityToScript.getScriptData()

        if self.m_pPlotToScript != -1:
            return self.m_pPlotToScript.getScriptData()

        return ""

    def setRiverHighlights(self):
        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().addColoredPlotAlt(
            self.m_pRiverStartPlot.getX(),
            self.m_pRiverStartPlot.getY(),
            PlotStyles.PLOT_STYLE_RIVER_SOUTH,
            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
            "COLOR_GREEN",
            1,
        )

        fAlpha = 0.2
        CyEngine().addColoredPlotAlt(
            self.m_pRiverStartPlot.getX() - 1,
            self.m_pRiverStartPlot.getY() + 1,
            PlotStyles.PLOT_STYLE_BOX_FILL,
            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
            "COLOR_WHITE",
            fAlpha,
        )
        CyEngine().addColoredPlotAlt(
            self.m_pRiverStartPlot.getX(),
            self.m_pRiverStartPlot.getY() + 1,
            PlotStyles.PLOT_STYLE_BOX_FILL,
            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
            "COLOR_WHITE",
            fAlpha,
        )
        CyEngine().addColoredPlotAlt(
            self.m_pRiverStartPlot.getX() + 1,
            self.m_pRiverStartPlot.getY() + 1,
            PlotStyles.PLOT_STYLE_BOX_FILL,
            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
            "COLOR_WHITE",
            fAlpha,
        )
        CyEngine().addColoredPlotAlt(
            self.m_pRiverStartPlot.getX() - 1,
            self.m_pRiverStartPlot.getY(),
            PlotStyles.PLOT_STYLE_BOX_FILL,
            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
            "COLOR_WHITE",
            fAlpha,
        )

        CyEngine().addColoredPlotAlt(
            self.m_pRiverStartPlot.getX() + 1,
            self.m_pRiverStartPlot.getY(),
            PlotStyles.PLOT_STYLE_BOX_FILL,
            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
            "COLOR_WHITE",
            fAlpha,
        )
        CyEngine().addColoredPlotAlt(
            self.m_pRiverStartPlot.getX() - 1,
            self.m_pRiverStartPlot.getY() - 1,
            PlotStyles.PLOT_STYLE_BOX_FILL,
            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
            "COLOR_WHITE",
            fAlpha,
        )
        CyEngine().addColoredPlotAlt(
            self.m_pRiverStartPlot.getX(),
            self.m_pRiverStartPlot.getY() - 1,
            PlotStyles.PLOT_STYLE_BOX_FILL,
            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
            "COLOR_WHITE",
            fAlpha,
        )
        CyEngine().addColoredPlotAlt(
            self.m_pRiverStartPlot.getX() + 1,
            self.m_pRiverStartPlot.getY() - 1,
            PlotStyles.PLOT_STYLE_BOX_FILL,
            PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
            "COLOR_WHITE",
            fAlpha,
        )
        return

    def setCurrentModeCheckbox(self, iButton):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)

        if iButton == self.m_iUnitEditCheckboxID:
            screen.setState("WorldBuilderUnitEditModeButton", True)
        else:
            screen.setState("WorldBuilderUnitEditModeButton", False)

        if iButton == self.m_iCityEditCheckboxID:
            screen.setState("WorldBuilderCityEditModeButton", True)
        else:
            screen.setState("WorldBuilderCityEditModeButton", False)

        if iButton == self.m_iNormalPlayerCheckboxID:
            screen.setState("WorldBuilderNormalPlayerModeButton", True)
        else:
            screen.setState("WorldBuilderNormalPlayerModeButton", False)

        if iButton == self.m_iNormalMapCheckboxID:
            screen.setState("WorldBuilderNormalMapModeButton", True)
        else:
            screen.setState("WorldBuilderNormalMapModeButton", False)

        if iButton == self.m_iRevealTileCheckboxID:
            screen.setState("WorldBuilderRevealTileModeButton", True)
        else:
            screen.setState("WorldBuilderRevealTileModeButton", False)

        if iButton == self.m_iDiplomacyCheckboxID:
            screen.setState("WorldBuilderDiplomacyModeButton", True)
        else:
            screen.setState("WorldBuilderDiplomacyModeButton", False)

        if iButton == self.m_iLandmarkCheckboxID:
            screen.setState("WorldBuilderLandmarkButton", True)
        else:
            screen.setState("WorldBuilderLandmarkButton", False)

        if iButton == self.m_iEraseCheckboxID:
            screen.setState("WorldBuilderEraseButton", True)
        else:
            screen.setState("WorldBuilderEraseButton", False)

        return

    def initVars(self):
        self.m_normalPlayerTabCtrl = 0
        self.m_normalMapTabCtrl = 0
        self.m_tabCtrlEdit = 0
        self.m_flyoutMenu = 0
        self.m_bCtrlEditUp = False
        self.m_bUnitEdit = False
        self.m_bCityEdit = False
        self.m_bNormalPlayer = True
        self.m_bNormalMap = False
        self.m_bReveal = False
        self.m_bDiplomacy = False
        self.m_bLandmark = False
        self.m_bEraseAll = False
        self.m_bUnitEditCtrl = False
        self.m_bCityEditCtrl = False
        self.m_bShowBigBrush = False
        self.m_bLeftMouseDown = False
        self.m_bRightMouseDown = False
        self.m_bChangeFocus = False
        self.m_iNormalPlayerCurrentIndexes = []
        self.m_iNormalMapCurrentIndexes = []
        self.m_iNormalMapCurrentList = []
        self.m_iCurrentPlayer = 0
        self.m_iCurrentTeam = 0
        self.m_iCurrentUnitPlayer = 0
        self.m_iCurrentUnit = 0
        self.m_iCurrentX = -1
        self.m_iCurrentY = -1
        self.m_pCurrentPlot = 0
        self.m_pActivePlot = 0
        self.m_pRiverStartPlot = -1
        self.m_iUnitTabID = -1
        self.m_iBuildingTabID = -1
        self.m_iTechnologyTabID = -1
        self.m_iImprovementTabID = -1
        self.m_iBonusTabID = -1
        self.m_iImprovementListID = -1
        self.m_iBonusListID = -1
        self.m_iTerrainTabID = -1
        self.m_iTerrainListID = -1
        self.m_iFeatureListID = -1
        self.m_iPlotTypeListID = -1
        self.m_iRouteListID = -1
        self.m_iTerritoryTabID = -1
        self.m_iTerritoryListID = -1
        self.m_iBrushSizeTabID = -1
        self.m_iBrushWidth = 1
        self.m_iBrushHeight = 1
        self.m_iFlyoutEditUnit = 1
        self.m_iFlyoutEditCity = 0
        self.m_iFlyoutAddScript = -1
        self.m_iFlyoutChangeStartYear = -2
        self.m_pFlyoutPlot = 0
        self.m_bFlyout = False
        self.m_pUnitToScript = -1
        self.m_pCityToScript = -1
        self.m_pPlotToScript = -1
        self.m_iUnitEditCheckboxID = -1
        self.m_iCityEditCheckboxID = -1
        self.m_iNormalPlayerCheckboxID = -1
        self.m_iNormalMapCheckboxID = -1
        self.m_iRevealTileCheckboxID = -1
        self.m_iDiplomacyCheckboxID = -1
        self.m_iLandmarkCheckboxID = -1
        self.m_iEraseCheckboxID = -1
        self.iScreenWidth = 228
        self.currentMode = None  # Caliom
        return


# Caliom own classes
class Mode:
    "Editor Mode template"

    def __init__(self, worldBuilderScreen):
        self.iPlayer = None
        self.worldBuilderScreen = worldBuilderScreen

    def activate(self):
        self.iPlayer = self.worldBuilderScreen.m_iCurrentPlayer

    def deactivate(self):
        pass

    def mouseOverPlot(self, pPlot, argsList):
        pass

    def leftMouseDown(self, pPlot, argsList):
        pass

    def leftMouseUp(self, pPlot):
        pass

    def rightMouseDown(self, pPlot, argsList):
        pass

    def rightMouseUp(self, pPlot):
        pass

    def updateScreen(self, pCurrentPlot):
        pass

    def handleDropdown(self, name, index, value):
        pass

    def isHighlightPlot(self):
        return True


class RevealMode(Mode):
    "Editor Mode for BTS Visible Maps, RFCE War Maps, RFCE Settler Maps, RFCE Provinces, RFCE Core Areas, RFCE Normal Areas"

    def __init__(self, worldBuilderScreen):
        Mode.__init__(self, worldBuilderScreen)
        self.VISIBLE_MAP = 1
        self.WAR_MAP = 2
        self.SETTLER_MAP = 3
        self.PROVINCE_MAP = 4
        self.CORE_AREA = 5
        self.NORMAL_AREA = 6
        self.iMapType = self.VISIBLE_MAP
        self.sBrushColor = "COLOR_GREEN"
        self.iBrushValue = -1
        self.iBrushSize = 1  # redundant
        self.iPlayer = 0  # redundant
        self.selectedPlots = set()
        self.selectedPlot = None
        self.worldBuilderScreen = worldBuilderScreen

    def activate(self):
        self.iPlayer = self.worldBuilderScreen.m_iCurrentPlayer

        self.refreshSideMenu()

    def deactivate(self):
        self.clearMaps()
        self.clearWidgets()

    def mouseOverPlot(self, pPlot, argsList):
        # CyInterface().addImmediateMessage(("onmouseover (%d,%d)"%(pPlot.getX(),pPlot.getY())), "")
        self.highlightBrush(pPlot)
        return

    def leftMouseDown(self, pPlot, argsList):
        if self.isSettlerMap() or self.isWarMap() or self.isProvinceMap() or self.isVisibleMap():
            for pPlot in self.getBrushPlots(pPlot):
                coords = (pPlot.getX(), pPlot.getY())
                if coords not in self.selectedPlots:
                    if self.isSettlerMap():
                        MapManager.setSettlerValue(self.iPlayer, pPlot, self.iBrushValue)
                    elif self.isWarMap():
                        MapManager.setWarValue(self.iPlayer, pPlot, self.iBrushValue)
                    elif self.isProvinceMap():
                        MapManager.setProvinceId(pPlot, self.iBrushValue)
                    elif self.isVisibleMap():
                        self.revealPlot(pPlot, True)
                    self.selectedPlots.add(coords)
        elif self.isCoreArea() or self.isNormalArea():
            if self.selectedPlot is None:
                self.selectedPlot = (pPlot.getX(), pPlot.getY())
                self.highlightRectangleBrush(self.selectedPlot, self.selectedPlot)
            else:
                self.highlightRectangleBrush(self.selectedPlot, (pPlot.getX(), pPlot.getY()))
            # MapManager.addCoreAreaAdditionalPlot(self.iPlayer, (pPlot.getX(), pPlot.getY()))
        return

    def leftMouseUp(self, pPlot):
        if self.isCoreArea():
            BL = self.getBL(self.selectedPlot, (pPlot.getX(), pPlot.getY()))
            TR = self.getTR(self.selectedPlot, (pPlot.getX(), pPlot.getY()))
            if BL == TR:
                MapManager.addCoreAreaAdditionalPlot(self.iPlayer, BL)
            else:
                MapManager.setCoreAreaBLTR(self.iPlayer, BL, TR)
            self.selectedPlot = None
        elif self.isNormalArea():
            BL = self.getBL(self.selectedPlot, (pPlot.getX(), pPlot.getY()))
            TR = self.getTR(self.selectedPlot, (pPlot.getX(), pPlot.getY()))
            if BL == TR:
                MapManager.addNormalAreaSubtractedPlot(self.iPlayer, BL)
            else:
                MapManager.setNormalAreaBLTR(self.iPlayer, BL, TR)
            self.selectedPlot = None

        self.refreshMaps()
        self.selectedPlots.clear()
        if self.isProvinceMap():
            MapVisualizer.highlightProvince(self.iBrushValue)

    def rightMouseDown(self, pPlot, argsList):
        if self.isSettlerMap():
            self.iBrushValue = MapManager.getSettlerValue(
                self.iPlayer, CyInterface().getMouseOverPlot()
            )
            self.sBrushColor = MapVisualizer.getSettlerMapColor(self.iBrushValue)
            self.highlightBrush(pPlot)
            self.refreshSideMenu()
        elif self.isWarMap():
            self.iBrushValue = MapManager.getWarValue(
                self.iPlayer, CyInterface().getMouseOverPlot()
            )
            self.sBrushColor = MapVisualizer.getWarMapColor(self.iBrushValue)
            self.highlightBrush(pPlot)
            self.refreshSideMenu()
        elif self.isProvinceMap():
            self.iBrushValue = MapManager.getProvinceId(CyInterface().getMouseOverPlot())
            self.sBrushColor = MapVisualizer.getProvinceColor(self.iBrushValue)
            self.highlightBrush(pPlot)
            MapVisualizer.highlightProvince(self.iBrushValue)
            self.refreshSideMenu()
        elif self.isVisibleMap():
            for pPlot in self.getBrushPlots(pPlot):
                coords = (pPlot.getX(), pPlot.getY())
                if coords not in self.selectedPlots:
                    self.revealPlot(pPlot, False)
                    self.selectedPlots.add(coords)
        elif self.isCoreArea():
            MapManager.removeCoreAreaAdditionalPlot(self.iPlayer, (pPlot.getX(), pPlot.getY()))
            self.refreshMaps()
        elif self.isNormalArea():
            MapManager.removeNormalAreaSubtractedPlot(self.iPlayer, (pPlot.getX(), pPlot.getY()))
            self.refreshMaps()
        return

    def rightMouseUp(self, pPlot):
        if self.isVisibleMap():
            self.refreshMaps()
            self.selectedPlots.clear()

    def handleDropdown(self, name, index, value):
        if name == "WorldBuilderPlayerChoice":
            self.handlePlayerDropdown(index, value)
        elif name == "WorldBuilderBrushSize":
            self.handleBrushSizeDropdown(index, value)
        elif name == "WorldBuilderBrushValue":
            self.handleBrushValueDropdown(index, value)
        elif name == "WorldBuilderMapType" or name == "WorldBuilderRevealType":
            self.handleMapTypeDropdown(index, value)
        elif name == "WorldBuilderProvince":
            self.handleProvinceDropdown(index, value)

    def isHighlightPlot(self):
        return False

    def refreshSideMenu(self):
        # self.worldBuilderScreen.refreshSideMenu()

        self.clearWidgets()
        self.clearOtherWidgets()

        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)

        iMaxScreenWidth = screen.getXResolution()
        iMaxScreenHeight = screen.getYResolution()
        iScreenHeight = 10 + 37 + 37
        iPanelWidth = 35 * 6
        iScreenWidth = self.worldBuilderScreen.iScreenWidth
        iPanelX = iMaxScreenWidth - iScreenWidth

        # panel background height
        if self.isWarMap() or self.isSettlerMap():
            iHeight = 45 + 40 + 40 + 40
        elif self.isCoreArea() or self.isNormalArea():
            iHeight = 45 + 40
        else:
            iHeight = 45 + 40 + 40
        screen.addPanel(
            "WorldBuilderBackgroundBottomPanel",
            "",
            "",
            True,
            True,
            iPanelX,
            10 + 32 + 32,
            iScreenWidth,
            iHeight,
            PanelStyles.PANEL_STYLE_MAIN,
        )

        # map type dropdown
        szDropdownName = str("WorldBuilderMapType")
        screen.addDropDownBoxGFC(
            szDropdownName,
            iPanelX + 8,
            (10 + 36 + 36),
            iPanelWidth,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            FontTypes.GAME_FONT,
        )
        screen.addPullDownString(
            szDropdownName, "Visible Map", self.VISIBLE_MAP, self.VISIBLE_MAP, self.isVisibleMap()
        )
        screen.addPullDownString(
            szDropdownName, "War Map", self.WAR_MAP, self.WAR_MAP, self.isWarMap()
        )
        screen.addPullDownString(
            szDropdownName, "Settler Map", self.SETTLER_MAP, self.SETTLER_MAP, self.isSettlerMap()
        )
        screen.addPullDownString(
            szDropdownName, "Provinces", self.PROVINCE_MAP, self.PROVINCE_MAP, self.isProvinceMap()
        )
        screen.addPullDownString(
            szDropdownName, "Spawn Area", self.CORE_AREA, self.CORE_AREA, self.isCoreArea()
        )
        screen.addPullDownString(
            szDropdownName, "Respawn Area", self.NORMAL_AREA, self.NORMAL_AREA, self.isNormalArea()
        )

        # province dropdown
        if self.isProvinceMap():
            szDropdownName = str("WorldBuilderProvince")
            screen.addDropDownBoxGFC(
                szDropdownName,
                iPanelX + 8,
                (10 + 36 + 36 + 36),
                iPanelWidth,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                FontTypes.GAME_FONT,
            )
            screen.addPullDownString(szDropdownName, "None", -1, -1, (-1 == self.iBrushValue))
            for i in range(MapUtils.iNumProvinces):
                try:
                    ProvinceName = unicode(MapManager.getProvinceName(i), "latin-1")  # type: ignore
                except TypeError:
                    ProvinceName = MapManager.getProvinceName(i)
                screen.addPullDownString(
                    szDropdownName, ProvinceName, i, i, (i == self.iBrushValue)
                )

        # player dropdown
        else:
            szDropdownName = str("WorldBuilderPlayerChoice")
            screen.addDropDownBoxGFC(
                szDropdownName,
                iPanelX + 8,
                (10 + 36 + 36 + 36),
                iPanelWidth,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                FontTypes.GAME_FONT,
            )
            for i in civilizations().majors().ids():
                screen.addPullDownString(
                    szDropdownName, gc.getPlayer(i).getName(), i, i, i == self.iPlayer
                )

        # revale/hide all buttons
        if self.isVisibleMap():
            iButtonWidth = 32
            iButtonHeight = 32
            screen.setImageButton(
                "WorldBuilderRevealAll",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_REVEAL_ALL_TILES").getPath(),
                iPanelX + 8,
                (10 + 36 + 36 + 36 + 36),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_REVEAL_ALL_BUTTON,
                -1,
                -1,
            )
            screen.setImageButton(
                "WorldBuilderUnrevealAll",
                ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_UNREVEAL_ALL_TILES").getPath(),
                iPanelX + 8 + 35,
                (10 + 36 + 36 + 36 + 36),
                iButtonWidth,
                iButtonHeight,
                WidgetTypes.WIDGET_WB_UNREVEAL_ALL_BUTTON,
                -1,
                -1,
            )

        # brushsize dropdown
        if self.isWarMap() or self.isSettlerMap() or self.isProvinceMap() or self.isVisibleMap():
            szDropdownName = str("WorldBuilderBrushSize")
            if self.isVisibleMap():
                screen.addDropDownBoxGFC(
                    szDropdownName,
                    iPanelX + 8 + 80,
                    (10 + 36 + 36 + 36 + 36),
                    iPanelWidth - 80,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
            else:
                screen.addDropDownBoxGFC(
                    szDropdownName,
                    iPanelX + 8,
                    (10 + 36 + 36 + 36 + 36),
                    iPanelWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
            screen.addPullDownString(
                szDropdownName, text("TXT_KEY_WB_1_BY_1"), 1, 1, self.iBrushSize == 1
            )
            screen.addPullDownString(
                szDropdownName, text("TXT_KEY_WB_3_BY_3"), 2, 2, self.iBrushSize == 2
            )
            screen.addPullDownString(
                szDropdownName, text("TXT_KEY_WB_5_BY_5"), 3, 3, self.iBrushSize == 3
            )

        # brushvalue dropdown
        if self.isWarMap() or self.isSettlerMap():
            szDropdownName = str("WorldBuilderBrushValue")
            screen.addDropDownBoxGFC(
                szDropdownName,
                iPanelX + 8,
                (10 + 36 + 36 + 36 + 36 + 36),
                iPanelWidth,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                FontTypes.GAME_FONT,
            )
            if self.isWarMap():
                shades = MapUtils.warMapShades
            else:
                shades = MapUtils.settlerMapShades
            for shade in shades:
                screen.addPullDownString(
                    szDropdownName, shade[3], shade[0], shade[0], shade[0] == self.iBrushValue
                )
        return

    def clearWidgets(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        screen.deleteWidget("WorldBuilderMapType")
        screen.deleteWidget("WorldBuilderPlayerChoice")
        screen.deleteWidget("WorldBuilderBrushSize")
        screen.deleteWidget("WorldBuilderBrushValue")
        screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
        screen.deleteWidget("WorldBuilderProvince")
        screen.deleteWidget("WorldBuilderRevealAll")
        screen.deleteWidget("WorldBuilderUnrevealAll")

    def clearOtherWidgets(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        screen.deleteWidget("WorldBuilderTechByEra")
        screen.deleteWidget("WorldBuilderRegenerateMap")
        screen.deleteWidget("WorldBuilderTeamChoice")
        screen.deleteWidget("WorldBuilderLandmarkType")
        screen.deleteWidget("WorldBuilderRevealPanel")  # is this realy used somewhere?

    def getBrushPlots(self, pPlot):
        plots = list()
        if pPlot is not None and not pPlot.isNone():
            iLowerLeftX = pPlot.getX() - self.iBrushSize + 1
            iLowerLeftY = pPlot.getY() - self.iBrushSize + 1
            iRectangleWidth = 2 * self.iBrushSize - 1
            iRectangleHeight = 2 * self.iBrushSize - 1

            for i in range(iRectangleWidth):
                for j in range(iRectangleHeight):
                    pPlot = CyMap().plot(iLowerLeftX + i, iLowerLeftY + j)
                    if not pPlot.isNone():
                        plots.append(pPlot)
        return plots

    def getRectanglePlots(self, coords1, coords2):
        BL = self.getBL(coords1, coords2)
        TR = self.getTR(coords1, coords2)
        plots = list()
        plotX = BL[0]
        plotY = TR[1]
        for iX in range(TR[0] - BL[0] + 1):
            for iY in range(TR[1] - BL[1] + 1):
                pPlot = CyMap().plot(plotX + iX, plotY - iY)
                if not pPlot.isNone():
                    plots.append(pPlot)
        return plots

    def getBL(self, coords1, coords2):
        B = min(coords1[0], coords2[0])
        L = min(coords1[1], coords2[1])
        return (B, L)

    def getTR(self, coords1, coords2):
        T = max(coords1[0], coords2[0])
        R = max(coords1[1], coords2[1])
        return (T, R)

    def highlightRectangleBrush(self, coords1, coords2):
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
        for pPlot in self.getRectanglePlots(coords1, coords2):
            CyEngine().fillAreaBorderPlotAlt(
                pPlot.getX(),
                pPlot.getY(),
                AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                "COLOR_WHITE",
                1,
            )
        return

    def highlightBrush(self, pPlot=None):
        if pPlot is None:
            pPlot = CyInterface().getMouseOverPlot()
        if pPlot is not None and not pPlot == 0 and not pPlot.isNone():
            CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
            for pBrushPlot in self.getBrushPlots(pPlot):
                CyEngine().fillAreaBorderPlotAlt(
                    pBrushPlot.getX(),
                    pBrushPlot.getY(),
                    AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                    self.sBrushColor,
                    1,
                )
        return

    def refreshMaps(self):
        self.clearMaps()

        if self.isVisibleMap():
            for i in range(CyMap().getGridWidth()):
                for j in range(CyMap().getGridHeight()):
                    pPlot = CyMap().plot(i, j)
                    if not pPlot.isNone():
                        self.showRevealed(pPlot)

        elif self.isSettlerMap():
            MapVisualizer.setPlayer(self.iPlayer)
            MapVisualizer.showSettlerMap()

        elif self.isWarMap():
            MapVisualizer.setPlayer(self.iPlayer)
            MapVisualizer.showWarMap()

        elif self.isProvinceMap():
            MapVisualizer.showProvinces()

        elif self.isCoreArea():
            MapVisualizer.setPlayer(self.iPlayer)
            MapVisualizer.showCoreArea()

        elif self.isNormalArea():
            MapVisualizer.setPlayer(self.iPlayer)
            MapVisualizer.showNormalArea()

        return 1

    def clearMaps(self):
        MapVisualizer.hideSettlerMap()
        MapVisualizer.hideWarMap()
        MapVisualizer.hideProvinces()
        MapVisualizer.hideCoreArea()
        MapVisualizer.hideNormalArea()
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)

    def isWarMap(self):
        return self.iMapType == self.WAR_MAP

    def isSettlerMap(self):
        return self.iMapType == self.SETTLER_MAP

    def isProvinceMap(self):
        return self.iMapType == self.PROVINCE_MAP

    def isVisibleMap(self):
        return self.iMapType == self.VISIBLE_MAP

    def isCoreArea(self):
        return self.iMapType == self.CORE_AREA

    def isNormalArea(self):
        return self.iMapType == self.NORMAL_AREA

    def showRevealed(self, pPlot):
        iTeam = self.iPlayer
        if not pPlot.isRevealed(iTeam, False):
            CyEngine().fillAreaBorderPlotAlt(
                pPlot.getX(),
                pPlot.getY(),
                AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS,
                "COLOR_BLACK",
                1.0,
            )

    def revealPlot(self, pPlot, bReveal):
        iTeam = self.iPlayer
        if bReveal or (not pPlot.isVisible(iTeam, False)):
            pPlot.setRevealed(iTeam, bReveal, False, -1)

    def handleMapTypeDropdown(self, index, value):
        self.iMapType = value
        if self.isWarMap():
            self.iBrushValue = MapUtils.warMapDefault
            self.sBrushColor = MapVisualizer.getWarMapColor(self.iBrushValue)
        elif self.isSettlerMap():
            self.iBrushValue = MapUtils.settlerMapDefault
            self.sBrushColor = MapVisualizer.getSettlerMapColor(self.iBrushValue)
        elif self.isProvinceMap():
            self.iBrushValue = MapUtils.provinceMapDefault
            self.sBrushColor = MapVisualizer.getProvinceColor(self.iBrushValue)
        elif self.isVisibleMap():
            self.sBrushColor = "COLOR_GREEN"
        elif self.isCoreArea() or self.isNormalArea():
            self.iBrushSize = 1
            self.sBrushColor = "COLOR_GREY"

        self.refreshMaps()
        self.refreshSideMenu()
        return 1

    def handlePlayerDropdown(self, index, value):
        self.iPlayer = value
        self.refreshMaps()

        return 1

    def handleProvinceDropdown(self, index, value):
        self.iBrushValue = value
        self.sBrushColor = MapVisualizer.getProvinceColor(self.iBrushValue)
        self.highlightBrush()
        MapVisualizer.highlightProvince(self.iBrushValue)
        return 1

    def handleBrushSizeDropdown(self, index, value):
        self.iBrushSize = value
        self.highlightBrush()
        return 1

    def handleBrushValueDropdown(self, index, value):

        self.iBrushValue = value
        if self.isWarMap():
            self.sBrushColor = MapVisualizer.getWarMapColor(self.iBrushValue)
        elif self.isSettlerMap():
            self.sBrushColor = MapVisualizer.getSettlerMapColor(self.iBrushValue)
        else:
            self.sBrushColor = "COLOR_GREEN"
        self.highlightBrush()
        return 1


class LandmarkMode(Mode):
    "Editor Mode for BTS Landmarks, RFCE City Maps"

    def __init__(self, worldBuilderScreen):
        Mode.__init__(self, worldBuilderScreen)
        self.iPlayer = None
        self.LANDMARKS = 1
        self.CITY_NAMES = 2
        self.mode = self.LANDMARKS
        self.worldBuilderScreen = worldBuilderScreen
        self.landmarks = None
        return

    def activate(self):
        self.iPlayer = self.worldBuilderScreen.m_iCurrentPlayer

        CvEventInterface.getEventManager().setPopupHandler(
            CITY_NAME_POPUP_EVENT_ID,
            ("CityNamePopup", self.cityNamePopupApply, self.cityNamePopupBegin),
        )
        CvEventInterface.getEventManager().setPopupHandler(
            RESTORE_LANDMARKS_POPUP_EVENT_ID,
            (
                "RestoreLandmarksPopup",
                self.restoreLandmarksPopupApply,
                self.restoreLandmarksPopupBegin,
            ),
        )
        # alternativ way of setting events ()without the need to add "setPopupHandler" to RFCEventManager)
        # CvEventInterface.getEventManager().Events[CITY_NAME_POPUP_EVENT_ID] = ("CityNamePopup", cityNamePopupApply, cityNamePopupBegin)

        if self.isCityNames():
            self.backupLandmarks()

        self.refreshScreen()
        self.refreshSideMenu()
        return

    def deactivate(self):
        self.clearScreen()
        self.clearSideMenu()
        self.checkRestoreLandmarks()

    def leftMouseDown(self, pPlot, argsList):
        if self.isCityNames():
            if self.iPlayer != gc.getBARBARIAN_PLAYER():
                CvEventInterface.getEventManager().beginEvent(
                    CITY_NAME_POPUP_EVENT_ID, (self.iPlayer, pPlot)
                )
        else:
            CvEventInterface.beginEvent(CvUtil.EventWBLandmarkPopup)
        return

    def leftMouseUp(self, pPlot):
        pass

    def rightMouseDown(self, pPlot, argsList):
        if self.isCityNames():
            if self.iPlayer != gc.getBARBARIAN_PLAYER():
                MapManager.removeCityName(self.iPlayer, pPlot)
                MapVisualizer.hideCityName(pPlot)
        else:
            CyEngine().removeLandmark(pPlot)
        return

    def rightMouseUp(self, pPlot):
        pass

    def handleDropdown(self, name, index, value):
        if name == "WorldBuilderPlayerChoice":
            return self.handlePlayerDropdown(index, value)
        elif name == "WorldBuilderLandmarkType":
            return self.handleLandmarkTypeDropdown(index, value)

    def isHighlightPlot(self):
        return True

    def refreshSideMenu(self):
        # self.worldBuilderScreen.refreshSideMenu()

        self.clearSideMenu()
        self.clearOtherWidgets()

        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)

        iMaxScreenWidth = screen.getXResolution()
        iMaxScreenHeight = screen.getYResolution()
        iScreenHeight = 10 + 37 + 37
        iPanelWidth = 35 * 6
        iScreenWidth = self.worldBuilderScreen.iScreenWidth
        iPanelX = iMaxScreenWidth - iScreenWidth

        iHeight = 45
        if self.isCityNames():
            iHeight = 45 + 40

        screen.addPanel(
            "WorldBuilderBackgroundBottomPanel",
            "",
            "",
            True,
            True,
            iPanelX,
            10 + 32 + 32,
            iScreenWidth,
            iHeight,
            PanelStyles.PANEL_STYLE_MAIN,
        )

        szDropdownName = str("WorldBuilderLandmarkType")
        screen.addDropDownBoxGFC(
            szDropdownName,
            iPanelX + 8,
            (10 + 36 + 36),
            iPanelWidth,
            WidgetTypes.WIDGET_GENERAL,
            -1,
            -1,
            FontTypes.GAME_FONT,
        )
        screen.addPullDownString(
            szDropdownName, "Landmarks", self.LANDMARKS, self.LANDMARKS, self.isLandmarks()
        )
        screen.addPullDownString(
            szDropdownName, "City Names", self.CITY_NAMES, self.CITY_NAMES, self.isCityNames()
        )

        if self.isCityNames():
            szDropdownName = str("WorldBuilderPlayerChoice")
            screen.addDropDownBoxGFC(
                szDropdownName,
                iPanelX + 8,
                (10 + 36 + 36 + 36),
                iPanelWidth,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                FontTypes.GAME_FONT,
            )

            for i in civilizations().majors().ids():
                if gc.getPlayer(i).isEverAlive():
                    screen.addPullDownString(
                        szDropdownName,
                        gc.getPlayer(i).getCivilizationShortDescription(0),
                        i,
                        i,
                        self.iPlayer == i,
                    )
            screen.addPullDownString(
                szDropdownName,
                "Generic map",
                (civilizations().majors().len()),
                (civilizations().majors().len()),
                self.iPlayer == civilizations().majors().len(),
            )
            iBarb = gc.getBARBARIAN_PLAYER()
            screen.addPullDownString(
                szDropdownName, "Please choose again", iBarb, iBarb, self.iPlayer == iBarb
            )
        return

    def refreshScreen(self):
        if self.isCityNames():
            if self.iPlayer != gc.getBARBARIAN_PLAYER():
                MapVisualizer.setPlayer(self.iPlayer)
                MapVisualizer.showCityNames()

    def clearScreen(self):
        if self.isCityNames():
            MapVisualizer.hideCityNames()

    def clearSideMenu(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        screen.deleteWidget("WorldBuilderPlayerChoice")
        screen.deleteWidget("WorldBuilderLandmarkType")
        screen.deleteWidget("WorldBuilderBackgroundBottomPanel")

    def clearOtherWidgets(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        screen.deleteWidget("WorldBuilderTechByEra")
        screen.deleteWidget("WorldBuilderRegenerateMap")
        screen.deleteWidget("WorldBuilderTeamChoice")
        screen.deleteWidget("WorldBuilderLandmarkType")
        screen.deleteWidget("WorldBuilderRevealPanel")  # is this realy used somewhere?
        screen.deleteWidget("WorldBuilderBrushSize")

    def isCityNames(self):
        return self.mode == self.CITY_NAMES

    def isLandmarks(self):
        return self.mode == self.LANDMARKS

    def handleLandmarkTypeDropdown(self, index, value):
        self.clearScreen()

        self.mode = value

        if self.isCityNames():
            self.backupLandmarks()
            self.refreshScreen()
        elif self.isLandmarks():
            self.clearScreen()
            self.checkRestoreLandmarks()

        self.refreshSideMenu()
        return 1

    def handlePlayerDropdown(self, index, value):
        iBarbarian = gc.getBARBARIAN_PLAYER()
        if (value == iBarbarian or self.iPlayer != iBarbarian) and self.isCityNames():
            # always switch to Barbarian player between two normal players to hide landmarks
            self.clearScreen()
            self.iPlayer = iBarbarian
            self.refreshSideMenu()
            return 1

        self.iPlayer = value
        self.refreshScreen()

        return 1

    def cityNamePopupBegin(self, userData):
        iPlayer, pPlot = userData

        cityName = MapManager.getCityName(iPlayer, pPlot)
        if cityName is None:
            cityName = ""
        else:
            cityName = unicode(cityName, "latin-1")  # type: ignore

        MapVisualizer.hideCityName(pPlot)  # landmark-update-problem-fix

        cityNames = []
        # all major civs' city names, in civ order
        for i in civilizations().majors().ids():
            if i != iPlayer:
                name = MapManager.getCityName(i, pPlot)
                civ = gc.getPlayer(i).getCivilizationShortDescription(0)
                if name is not None:
                    cityNames.append((unicode(name, "latin-1"), civ))  # type: ignore
        # uncomment for city names in alphabetic order
        # cityNames.sort()
        # generic city name, always on last place
        if civilizations().majors().len() != iPlayer:
            name = MapManager.getCityName(civilizations().majors().len(), pPlot)
            if name is not None:
                cityNames.append((unicode(name, "latin-1"), "GENERIC NAME"))  # type: ignore

        cityHeader = cityName
        if cityHeader == "":
            cityHeader = "New City"
        if iPlayer == civilizations().majors().len():
            sHeaderText = "%s - %s" % (cityHeader, "Generic Name")
        else:
            sHeaderText = "%s - %s" % (
                cityHeader,
                gc.getPlayer(iPlayer).getCivilizationShortDescription(0),
            )
        sBodyText = ""
        for i in range(len(cityNames)):
            sBodyText = sBodyText + ("%s - %s \n" % cityNames[i])

        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        iMaxScreenWidth = screen.getXResolution()
        iMaxScreenHeight = screen.getYResolution()

        iHeight = 200 + len(cityNames) * 22
        if iHeight > iMaxScreenHeight - 20:
            iHeight = iMaxScreenHeight - 20
        iWidth = 400
        iPosY = (iMaxScreenHeight - iHeight) / 2  # centered
        iPosX = (iMaxScreenWidth - iWidth) / 2  # centered

        popup = PyPopup.PyPopup(CITY_NAME_POPUP_EVENT_ID, EventContextTypes.EVENTCONTEXT_SELF)
        popup.setPosition(iPosX, iPosY)
        popup.setSize(iWidth, iHeight)
        popup.setHeaderString(sHeaderText)
        popup.setBodyString(sBodyText)
        popup.createEditBox(cityName, 1)
        popup.addSeparator()
        popup.addButton("Ok")
        popup.addButton("Cancel")

        popup.setUserData((iPlayer, pPlot.getX(), pPlot.getY()))
        popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)
        return

    def cityNamePopupApply(self, playerID, userData, popupReturn):
        iPlayer, plotX, plotY = userData
        pPlot = CyMap().plot(plotX, plotY)

        if popupReturn.getButtonClicked() == 0:  # Index of OK Button
            cityName = popupReturn.getEditBoxString(1)
            cityName = CvUtil.convertToStr(cityName)
            MapManager.setCityName(iPlayer, pPlot, cityName)

        MapVisualizer.showCityName(pPlot)
        return

    def backupLandmarks(self):
        if self.landmarks is None:
            self.landmarks = []
            for i in range(CyEngine().getNumSigns()):
                sign = CyEngine().getSignByIndex(i)
                if sign.getPlayerType() == -1:
                    self.landmarks.append((sign.getPlot(), str(sign.getCaption())))

            if len(self.landmarks) > 0:
                self.iPlayer = gc.getBARBARIAN_PLAYER()
                self.clearScreen()
        return

    def checkRestoreLandmarks(self):
        if self.landmarks is not None:
            length = len(self.landmarks)
            if length > 0:
                self.restoreLandmarksPopupBegin(length)
        return

    def restoreLandmarks(self):
        if self.landmarks is not None:
            for i in range(len(self.landmarks)):
                pPlot, caption = self.landmarks[i]
                CyEngine().addLandmark(pPlot, caption)
            self.landmarks = None
        return

    def restoreLandmarksPopupBegin(self, userData=None):
        popup = PyPopup.PyPopup(
            RESTORE_LANDMARKS_POPUP_EVENT_ID, EventContextTypes.EVENTCONTEXT_SELF
        )
        popup.setHeaderString("Restore Landmarks")
        popup.setBodyString(
            ("Found %d landmarks that will be restored. Click ok to proceed." % userData)
        )
        popup.setPosition(400, 400)
        popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)
        return

    def restoreLandmarksPopupApply(self, playerID, userData, popupReturn):
        self.restoreLandmarks()
        return
