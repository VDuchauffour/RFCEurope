from CvPythonExtensions import *
import CvUtil
import CvScreenEnums
import WBPlotScreen
import WBEventScreen
import WBCityEditScreen
import WBCityDataScreen
import WBBuildingScreen
import WBUnitScreen
import WBPromotionScreen
import WBGameDataScreen
import WBReligionScreen
import WBCorporationScreen
import WBDiplomacyScreen
import WBPlayerScreen
import WBTeamScreen
import WBTechScreen
import WBProjectScreen
import WBPlayerUnits
import WBInfoScreen
import WBTradeScreen
import CvEventManager
import Popup

gc = CyGlobalContext()
iChange = 1
bPython = True
bHideInactive = True
Activities = [
    "AWAKE",
    "HOLD",
    "SLEEP",
    "HEAL",
    "SENTRY",
    "INTERCEPT",
    "MISSION",
    "PATROL",
    "PLUNDER",
]


class CvWorldBuilderScreen:
    def __init__(self):
        self.m_advancedStartTabCtrl = None
        self.m_bShowBigBrush = False
        self.m_bChangeFocus = False
        self.m_iAdvancedStartCurrentIndexes = []
        self.m_iAdvancedStartCurrentList = []
        self.m_iCurrentPlayer = 0
        self.m_iCurrentTeam = 0
        self.m_iCurrentX = -1
        self.m_iCurrentY = -1
        self.m_pCurrentPlot = 0
        self.m_pRiverStartPlot = -1

        self.m_iASUnitTabID = 1
        self.m_iASUnitListID = 0
        self.m_iASCityTabID = 0
        self.m_iASCityListID = 0
        self.m_iASBuildingsListID = 2
        self.m_iASAutomateListID = 1
        self.m_iASImprovementsTabID = 2
        self.m_iASRoutesListID = 0
        self.m_iASImprovementsListID = 1
        self.m_iASVisibilityTabID = 3
        self.m_iASVisibilityListID = 0
        self.m_iASTechTabID = 4
        self.m_iASTechListID = 0

        self.m_bSideMenuDirty = False
        self.m_bASItemCostDirty = False
        self.m_iCost = 0

        ## Platy Builder ##
        self.PlayerMode = ["Ownership", "Units", "Buildings", "City", "StartingPlot"]
        self.MapMode = [
            "AddLandMark",
            "PlotData",
            "River",
            "Improvements",
            "Bonus",
            "PlotType",
            "Terrain",
            "Routes",
            "Features",
        ]
        self.RevealMode = ["RevealPlot", "INVISIBLE_SUBMARINE", "INVISIBLE_STEALTH", "Blockade"]
        self.iBrushWidth = 1
        self.iBrushHeight = 1
        self.iPlayerAddMode = "Units"
        self.iSelection = -1
        self.iSelectClass = -2
        self.bSensibility = True
        self.lMoveUnit = []
        self.iMoveCity = -1
        self.iTargetPlotX = -1
        self.iTargetPlotY = -1
        self.TempInfo = []

    ## Platy Builder ##

    def interfaceScreen(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        self.__init__()
        screen.setCloseOnEscape(False)
        screen.setAlwaysShown(True)
        self.setSideMenu()
        self.refreshSideMenu()
        self.refreshAdvancedStartTabCtrl(False)

        if CyInterface().isInAdvancedStart():
            pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
            pPlot = pPlayer.getStartingPlot()
            CyCamera().JustLookAtPlot(pPlot)
        screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
        screen.setForcedRedraw(True)

    def killScreen(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        screen.hideScreen()
        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)

    def mouseOverPlot(self, argsList):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
        self.m_iCurrentX = self.m_pCurrentPlot.getX()
        self.m_iCurrentY = self.m_pCurrentPlot.getY()
        if not CyInterface().isInAdvancedStart():
            sText = "<font=3b>%s, X: %d, Y: %d</font>" % (
                CyTranslator().getText(
                    "TXT_KEY_WB_LATITUDE", (self.m_pCurrentPlot.getLatitude(),)
                ),
                self.m_iCurrentX,
                self.m_iCurrentY,
            )
            screen.setLabel(
                "WBCoords",
                "Background",
                sText,
                CvUtil.FONT_CENTER_JUSTIFY,
                screen.getXResolution() / 2,
                6,
                -0.3,
                FontTypes.GAME_FONT,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
            )

        if self.iPlayerAddMode in self.RevealMode:
            if CyInterface().isLeftMouseDown():
                self.setMultipleReveal(True)
            elif CyInterface().isRightMouseDown():
                self.setMultipleReveal(False)

        else:
            if CyInterface().isLeftMouseDown():
                if self.useLargeBrush():
                    self.placeMultipleObjects()
                else:
                    self.placeObject()
            elif CyInterface().isRightMouseDown():
                if self.useLargeBrush():
                    self.removeMultipleObjects()
                else:
                    self.removeObject()
        return

    def getHighlightPlot(self, argsList):
        self.refreshASItemCost()
        if self.m_pCurrentPlot != 0:
            if CyInterface().isInAdvancedStart():
                if self.m_iCost <= 0:
                    return []

        if (self.m_pCurrentPlot != 0) and not self.m_bShowBigBrush and isMouseOverGameSurface():  # type: ignore
            return (self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY())
        return []

    def update(self, fDelta):
        if (not self.m_bChangeFocus) and (not isMouseOverGameSurface()):  # type: ignore
            self.m_bChangeFocus = True
        if (
            self.m_bChangeFocus
            and isMouseOverGameSurface()  # type: ignore
            and (self.iPlayerAddMode != "EditUnit" and self.iPlayerAddMode != "EditCity")
        ):
            self.m_bChangeFocus = False
            setFocusToCVG()  # type: ignore
        return

    # Will update the screen (every 250 MS)
    def updateScreen(self):
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

        self.m_bShowBigBrush = self.useLargeBrush()
        if self.iPlayerAddMode == "River":
            if self.m_pRiverStartPlot != -1:
                self.setRiverHighlights()
                return 0
        if self.m_bShowBigBrush:
            self.highlightBrush()
        return 0

    def highlightBrush(self):
        if self.iPlayerAddMode == "StartingPlot":
            return
        if self.m_pCurrentPlot == 0:
            return
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
        Data = self.getMultiplePlotData()
        for x in range(Data[0], Data[1]):
            for y in range(Data[2], Data[3]):
                pPlot = CyMap().plot(x, y)
                if pPlot.isNone():
                    continue
                CyEngine().fillAreaBorderPlotAlt(
                    pPlot.getX(),
                    pPlot.getY(),
                    AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER,
                    "COLOR_GREEN",
                    1,
                )

    def refreshReveal(self):
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
        for i in xrange(CyMap().numPlots()):  # type: ignore
            pPlot = CyMap().plotByIndex(i)
            if pPlot.isNone():
                continue
            self.showRevealed(pPlot)

    def refreshStartingPlots(self):
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
        for iPlayerX in xrange(gc.getMAX_PLAYERS()):  # type: ignore
            pPlayerX = gc.getPlayer(iPlayerX)
            pPlot = pPlayerX.getStartingPlot()
            if not pPlot.isNone():
                sColor = "COLOR_MAGENTA"
                if iPlayerX == self.m_iCurrentPlayer:
                    sColor = "COLOR_BLACK"
                CyEngine().fillAreaBorderPlotAlt(
                    pPlot.getX(),
                    pPlot.getY(),
                    AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS,
                    sColor,
                    1.0,
                )

    ########################################################
    ### Advanced Start Stuff
    ########################################################

    def refreshASItemCost(self):
        if CyInterface().isInAdvancedStart():
            self.m_iCost = 0
            if self.m_pCurrentPlot != 0:
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
            self.m_iCost = max(0, self.m_iCost)
            self.refreshSideMenu()

    def getASActiveUnit(self):
        # Unit Tab
        if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID:
            iUnitType = getASUnit(  # type: ignore
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
                iBuildingType = getASBuilding(  # type: ignore
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
                iRouteType = getASRoute(  # type: ignore
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
                iImprovementType = getASImprovement(  # type: ignore
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
        if self.m_iCurrentX == -1 or self.m_iCurrentY == -1:
            return
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
                            if pPlayer.getAdvancedStartCityCost(True, pPlot) > -1:
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
                                if pPlayer.getAdvancedStartPopCost(True, pCity) > -1:
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
                                if pPlayer.getAdvancedStartCultureCost(True, pCity) > -1:
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
                            iBuildingType = getASBuilding(  # type: ignore
                                self.m_iAdvancedStartCurrentIndexes[
                                    self.m_advancedStartTabCtrl.getActiveTab()
                                ]
                            )
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
                    iUnitType = getASUnit(  # type: ignore
                        self.m_iAdvancedStartCurrentIndexes[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                    )
                    if (
                        iUnitType > -1
                        and pPlayer.getAdvancedStartUnitCost(iUnitType, True, pPlot) > -1
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
                        iRouteType = getASRoute(  # type: ignore
                            self.m_iAdvancedStartCurrentIndexes[
                                self.m_advancedStartTabCtrl.getActiveTab()
                            ]
                        )
                        if (
                            iRouteType > -1
                            and pPlayer.getAdvancedStartRouteCost(iRouteType, True, pPlot) > -1
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
                        iImprovementType = getASImprovement(  # type: ignore
                            self.m_iAdvancedStartCurrentIndexes[
                                self.m_advancedStartTabCtrl.getActiveTab()
                            ]
                        )
                        if (
                            iImprovementType > -1
                            and pPlayer.getAdvancedStartImprovementCost(
                                iImprovementType, True, pPlot
                            )
                            > -1
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
                    if pPlayer.getAdvancedStartVisibilityCost(True, pPlot) > -1:
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

        if self.iPlayerAddMode == "EraseAll":
            self.m_pCurrentPlot.erase()
            CyEngine().removeLandmark(self.m_pCurrentPlot)
            for iPlayerX in xrange(gc.getMAX_PLAYERS()):  # type: ignore
                CyEngine().removeSign(self.m_pCurrentPlot, iPlayerX)
        elif self.iPlayerAddMode == "AddLandMark":
            iIndex = -1
            for i in xrange(CyEngine().getNumSigns()):  # type: ignore
                pSign = CyEngine().getSignByIndex(i)
                if pSign.getPlot().getX() != self.m_pCurrentPlot.getX():
                    continue
                if pSign.getPlot().getY() != self.m_pCurrentPlot.getY():
                    continue
                if pSign.getPlayerType() == self.m_iCurrentPlayer:
                    iIndex = i
                    break
            sText = ""
            if iIndex > -1:
                sText = CyEngine().getSignByIndex(iIndex).getCaption()
            popup = Popup.PyPopup(CvUtil.EventWBLandmarkPopup, EventContextTypes.EVENTCONTEXT_ALL)
            popup.setHeaderString(CyTranslator().getText("TXT_KEY_WB_LANDMARK_START", ()))
            popup.setUserData(
                (
                    self.m_pCurrentPlot.getX(),
                    self.m_pCurrentPlot.getY(),
                    self.m_iCurrentPlayer,
                    iIndex,
                )
            )
            popup.createEditBox(sText)
            popup.launch()
        elif self.iSelection == -1:
            return
        elif self.iPlayerAddMode == "Ownership":
            self.m_pCurrentPlot.setOwner(self.m_iCurrentPlayer)
        ## Python Effects ##
        elif self.iPlayerAddMode == "Units":
            for i in xrange(iChange):  # type: ignore
                gc.getPlayer(self.m_iCurrentPlayer).initUnit(
                    self.iSelection,
                    self.m_pCurrentPlot.getX(),
                    self.m_pCurrentPlot.getY(),
                    UnitAITypes.NO_UNITAI,
                    DirectionTypes.NO_DIRECTION,
                )
        elif self.iPlayerAddMode == "Buildings":
            if self.m_pCurrentPlot.isCity():
                pCity = self.m_pCurrentPlot.getPlotCity()
                bEffects = False
                if bPython and pCity.getNumRealBuilding(self.iSelection) == 0:
                    bEffects = True
                pCity.setNumRealBuilding(self.iSelection, 1)
                if bEffects:
                    CvEventManager.CvEventManager().onBuildingBuilt([pCity, self.iSelection])
        elif self.iPlayerAddMode == "City":
            if self.m_pCurrentPlot.isCity():
                return
            pCity = gc.getPlayer(self.m_iCurrentPlayer).initCity(
                self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY()
            )
            if bPython:
                CvEventManager.CvEventManager().onCityBuilt([pCity])
        ## Python Effects ##
        elif self.iPlayerAddMode == "Improvements":
            self.m_pCurrentPlot.setImprovementType(self.iSelection)
        elif self.iPlayerAddMode == "Bonus":
            self.m_pCurrentPlot.setBonusType(self.iSelection)
        elif self.iPlayerAddMode == "Routes":
            self.m_pCurrentPlot.setRouteType(self.iSelection)
        elif self.iPlayerAddMode == "Terrain":
            self.m_pCurrentPlot.setTerrainType(self.iSelection, True, True)
        elif self.iPlayerAddMode == "PlotType":
            if self.iSelection == gc.getInfoTypeForString("TERRAIN_PEAK"):
                self.m_pCurrentPlot.setPlotType(PlotTypes.PLOT_PEAK, True, True)
            elif self.iSelection == gc.getInfoTypeForString("TERRAIN_HILL"):
                self.m_pCurrentPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
            elif self.iSelection == gc.getInfoTypeForString("TERRAIN_GRASS"):
                self.m_pCurrentPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
            elif self.iSelection == gc.getInfoTypeForString("TERRAIN_OCEAN"):
                self.m_pCurrentPlot.setPlotType(PlotTypes.PLOT_OCEAN, True, True)
        elif self.iPlayerAddMode == "Features":
            self.m_pCurrentPlot.setFeatureType(self.iSelection, self.iSelectClass)
        elif self.iPlayerAddMode == "River":
            if self.m_pRiverStartPlot == self.m_pCurrentPlot:
                self.m_pRiverStartPlot = -1
                CyEngine().clearColoredPlots(
                    PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS
                )
            elif self.m_pRiverStartPlot != -1:
                iXDiff = abs(self.m_pCurrentPlot.getX() - self.m_pRiverStartPlot.getX())
                iYDiff = abs(self.m_pCurrentPlot.getY() - self.m_pRiverStartPlot.getY())

                if (
                    (iXDiff == iYDiff)
                    and (iXDiff == 1)
                    and (self.m_pRiverStartPlot.getX() > self.m_pCurrentPlot.getX())
                    and (self.m_pRiverStartPlot.getY() < self.m_pCurrentPlot.getY())
                ):
                    self.placeRiverNW(True)
                    self.m_pRiverStartPlot = CyMap().plot(
                        self.m_pRiverStartPlot.getX() - 1, self.m_pRiverStartPlot.getY() + 1
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
        return 1

    def removeObject(self):
        if self.m_iCurrentX == -1 or self.m_iCurrentY == -1:
            return
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
                        # City Population
                        if iOptionID == 1:
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

                    # Buildings List
                    elif (
                        self.m_iAdvancedStartCurrentList[
                            self.m_advancedStartTabCtrl.getActiveTab()
                        ]
                        == self.m_iASBuildingsListID
                    ):
                        if pPlot.isCity():
                            if pPlot.getPlotCity().getOwner() == self.m_iCurrentPlayer:
                                iBuildingType = getASBuilding(  # type: ignore
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
                    iUnitType = getASUnit(  # type: ignore
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
                        iRouteType = getASRoute(  # type: ignore
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
                        iImprovementType = getASImprovement(  # type: ignore
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
                    return 1
            self.m_bSideMenuDirty = True
            self.m_bASItemCostDirty = True
            return 1

        if self.iPlayerAddMode == "EraseAll":
            self.m_pCurrentPlot.erase()
            CyEngine().removeLandmark(self.m_pCurrentPlot)
            for iPlayerX in xrange(gc.getMAX_PLAYERS()):  # type: ignore
                CyEngine().removeSign(self.m_pCurrentPlot, iPlayerX)
        elif self.iPlayerAddMode == "Ownership":
            self.m_pCurrentPlot.setOwner(-1)
        elif self.iPlayerAddMode == "Units":
            for i in xrange(self.m_pCurrentPlot.getNumUnits()):  # type: ignore
                pUnit = self.m_pCurrentPlot.getUnit(i)
                if pUnit.getUnitType() == self.iSelection:
                    pUnit.kill(False, PlayerTypes.NO_PLAYER)
                    return 1
            if self.m_pCurrentPlot.getNumUnits() > 0:
                pUnit = self.m_pCurrentPlot.getUnit(0)
                pUnit.kill(False, PlayerTypes.NO_PLAYER)
                return 1
        elif self.iPlayerAddMode == "Buildings":
            if self.m_pCurrentPlot.isCity():
                self.m_pCurrentPlot.getPlotCity().setNumRealBuilding(self.iSelection, 0)
        elif self.iPlayerAddMode == "City":
            if self.m_pCurrentPlot.isCity():
                pCity = self.m_pCurrentPlot.getPlotCity()
                pCity.kill()
        elif self.iPlayerAddMode == "Improvements":
            self.m_pCurrentPlot.setImprovementType(-1)
            return 1
        elif self.iPlayerAddMode == "Bonus":
            self.m_pCurrentPlot.setBonusType(-1)
            return 1
        elif self.iPlayerAddMode == "Features":
            self.m_pCurrentPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
        elif self.iPlayerAddMode == "Routes":
            self.m_pCurrentPlot.setRouteType(-1)
        elif self.iPlayerAddMode == "River":
            if self.m_pRiverStartPlot != -1:
                self.m_pRiverStartPlot = -1
                CyEngine().clearColoredPlots(
                    PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS
                )
            else:
                self.m_pCurrentPlot.setNOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
                self.m_pCurrentPlot.setWOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
        elif self.iPlayerAddMode == "AddLandMark":
            CyEngine().removeSign(self.m_pCurrentPlot, self.m_iCurrentPlayer)
        return 1

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

    def toggleUnitEditCB(self):
        self.iPlayerAddMode = "EditUnit"
        self.refreshSideMenu()
        return

    def normalPlayerTabModeCB(self):
        self.m_iCurrentTeam = gc.getPlayer(self.m_iCurrentPlayer).getTeam()
        self.iPlayerAddMode = "Units"
        self.iSelectClass = -2
        self.iSelection = -1
        self.refreshSideMenu()
        getWBToolNormalPlayerTabCtrl().enable(False)  # type: ignore
        getWBToolNormalMapTabCtrl().enable(False)  # type: ignore
        return

    def normalMapTabModeCB(self):
        self.iPlayerAddMode = "PlotData"
        self.refreshSideMenu()
        return

    def revealTabModeCB(self):
        self.iPlayerAddMode = "RevealPlot"
        self.refreshSideMenu()
        self.refreshReveal()
        return

    def toggleCityEditCB(self):
        self.iPlayerAddMode = "CityDataI"
        self.refreshSideMenu()
        return

    def landmarkModeCB(self):
        self.iPlayerAddMode = "AddLandMark"
        self.m_iCurrentPlayer = gc.getBARBARIAN_PLAYER()
        self.refreshSideMenu()
        return

    def eraseCB(self):
        self.m_pRiverStartPlot = -1
        self.iPlayerAddMode = "EraseAll"
        self.refreshSideMenu()
        return

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

    def placeMultipleObjects(self):
        permCurrentPlot = self.m_pCurrentPlot
        Data = self.getMultiplePlotData()
        for x in range(Data[0], Data[1]):
            for y in range(Data[2], Data[3]):
                self.m_pCurrentPlot = CyMap().plot(x, y)
                if self.m_pCurrentPlot.isNone():
                    continue
                if self.bSensibility and (self.iBrushWidth > 1 or self.iBrushHeight > 1):
                    if self.iPlayerAddMode == "Improvements":
                        if self.m_pCurrentPlot.canHaveImprovement(self.iSelection, -1, True):
                            self.placeObject()
                    elif self.iPlayerAddMode == "Bonus":
                        iOldBonus = self.m_pCurrentPlot.getBonusType(-1)
                        self.m_pCurrentPlot.setBonusType(-1)
                        if self.m_pCurrentPlot.canHaveBonus(self.iSelection, False):
                            self.placeObject()
                        else:
                            self.m_pCurrentPlot.setBonusType(iOldBonus)
                    elif self.iPlayerAddMode == "Features":
                        iOldFeature = self.m_pCurrentPlot.getFeatureType()
                        iOldVariety = self.m_pCurrentPlot.getFeatureVariety()
                        self.m_pCurrentPlot.setFeatureType(-1, 0)
                        if self.m_pCurrentPlot.canHaveFeature(self.iSelection):
                            self.placeObject()
                        else:
                            self.m_pCurrentPlot.setFeatureType(iOldFeature, iOldVariety)
                    elif self.iPlayerAddMode == "Routes":
                        if not (
                            self.m_pCurrentPlot.isImpassable() or self.m_pCurrentPlot.isWater()
                        ):
                            self.placeObject()
                    elif self.iPlayerAddMode == "Terrain":
                        if (
                            self.m_pCurrentPlot.isWater()
                            == gc.getTerrainInfo(self.iSelection).isWater()
                        ):
                            self.placeObject()
                    else:
                        self.placeObject()
                else:
                    self.placeObject()
        self.m_pCurrentPlot = permCurrentPlot
        return

    def removeMultipleObjects(self):
        permCurrentPlot = self.m_pCurrentPlot
        Data = self.getMultiplePlotData()
        for x in range(Data[0], Data[1]):
            for y in range(Data[2], Data[3]):
                self.m_pCurrentPlot = CyMap().plot(x, y)
                if self.m_pCurrentPlot.isNone():
                    continue
                self.removeObject()
        self.m_pCurrentPlot = permCurrentPlot
        return

    def getMultiplePlotData(self):
        iMinX = self.m_pCurrentPlot.getX()
        iMaxX = self.m_pCurrentPlot.getX() + self.iBrushWidth
        iMinY = self.m_pCurrentPlot.getY() - self.iBrushHeight + 1
        iMaxY = self.m_pCurrentPlot.getY() + 1
        if self.iBrushWidth == -1:
            iMinX = 0
            iMaxX = CyMap().getGridWidth()
        if self.iBrushHeight == -1:
            iMinY = 0
            iMaxY = CyMap().getGridHeight()
        if not CyMap().isWrapX():
            iMaxX = min(iMaxX, CyMap().getGridWidth())
        if not CyMap().isWrapY():
            iMinY = max(iMinY, 0)
        return [iMinX, iMaxX, iMinY, iMaxY]

    def setMultipleReveal(self, bReveal):
        Data = self.getMultiplePlotData()
        for x in range(Data[0], Data[1]):
            for y in range(Data[2], Data[3]):
                pPlot = CyMap().plot(x, y)
                if pPlot.isNone():
                    continue
                self.RevealCurrentPlot(bReveal, pPlot)
        self.refreshReveal()
        return

    def useLargeBrush(self):
        if self.iPlayerAddMode in self.RevealMode:
            return True
        if self.iPlayerAddMode == "EraseAll":
            return True
        if self.iPlayerAddMode == "Improvements":
            return True
        if self.iPlayerAddMode == "Bonus":
            return True
        if self.iPlayerAddMode == "PlotType":
            return True
        if self.iPlayerAddMode == "Terrain":
            return True
        if self.iPlayerAddMode == "Routes":
            return True
        if self.iPlayerAddMode == "Features":
            return True
        return False

    def setSideMenu(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        iButtonWidth = 32
        iAdjust = iButtonWidth + 3

        iScreenWidth = 16 + iAdjust * 6
        iScreenHeight = 16 + iAdjust * 4

        iXStart = screen.getXResolution() - iScreenWidth
        if CyInterface().isInAdvancedStart():
            iXStart = 0
            iScreenWidth = 226
            iScreenHeight = 10 + 37 * 2

        screen.addPanel(
            "WorldBuilderBackgroundPanel",
            "",
            "",
            True,
            True,
            iXStart,
            0,
            iScreenWidth,
            iScreenHeight,
            PanelStyles.PANEL_STYLE_MAIN,
        )

        if CyInterface().isInAdvancedStart():

            iX = 50
            iY = 15
            szText = (
                u"<font=4>"
                + CyTranslator().getText(
                    "TXT_KEY_WB_AS_POINTS",
                    (gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartPoints(),),
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
            szText = CyTranslator().getText("TXT_KEY_ADVANCED_START_BEGIN_GAME", ())
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
                u"<font=4>"
                + CyTranslator().getText("TXT_KEY_WB_AS_COST_THIS_LOCATION", (self.m_iCost,))
                + u"</font>"
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
            iX = iXStart + 8
            iY = 10

            screen.setImageButton(
                "Version",
                CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                9,
            )
            iX += iAdjust
            screen.setImageButton(
                "WorldBuilderRegenerateMap",
                CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_REVEAL_ALL_TILES").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_REGENERATE_MAP,
                -1,
                -1,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "WorldBuilderEraseButton",
                CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_ERASE").getPath(),
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_ERASE_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.setImageButton(
                "WorldBuilderSaveButton",
                CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_SAVE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_SAVE_BUTTON,
                -1,
                -1,
            )
            iX += iAdjust
            screen.setImageButton(
                "WorldBuilderLoadButton",
                CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_LOAD").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_LOAD_BUTTON,
                -1,
                -1,
            )
            iX += iAdjust
            screen.setImageButton(
                "WorldBuilderExitButton",
                CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_EXIT").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_EXIT_BUTTON,
                -1,
                -1,
            )

            iX = iXStart + 8
            iY += iAdjust

            screen.setImageButton(
                "EditGameOptions",
                "",
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                23,
            )
            screen.setStyle("EditGameOptions", "Button_HUDAdvisorVictory_Style")
            iX += iAdjust
            screen.setImageButton(
                "EditReligions",
                "",
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                20,
            )
            screen.setStyle("EditReligions", "Button_HUDAdvisorReligious_Style")
            iX += iAdjust
            screen.setImageButton(
                "EditCorporations",
                "",
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                21,
            )
            screen.setStyle("EditCorporations", "Button_HUDAdvisorCorporation_Style")
            iX += iAdjust
            screen.setImageButton(
                "EditDiplomacy",
                "",
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_DIPLOMACY_MODE_BUTTON,
                -1,
                -1,
            )
            screen.setStyle("EditDiplomacy", "Button_HUDAdvisorForeign_Style")
            iX += iAdjust
            screen.setImageButton(
                "EditEspionage",
                "",
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                22,
            )
            screen.setStyle("EditEspionage", "Button_HUDAdvisorEspionage_Style")
            iX += iAdjust
            screen.setImageButton(
                "TradeScreen",
                "",
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                34,
            )
            screen.setStyle("TradeScreen", "Button_HUDAdvisorFinance_Style")

            iX = iXStart + 8
            iY += iAdjust
            screen.addCheckBoxGFC(
                "WorldBuilderNormalPlayerModeButton",
                ",Art/Interface/Buttons/Buildings/SDI.dds,Art/Interface/Buttons/FinalFrontier1_Atlas.dds,2,15",
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_NORMAL_PLAYER_TAB_MODE_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "WorldBuilderNormalMapModeButton",
                ",Art/Interface/Buttons/Buildings/SDI.dds,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,3,6",
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_NORMAL_MAP_TAB_MODE_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "WorldBuilderRevealTileModeButton",
                CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(),
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_REVEAL_TAB_MODE_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "PythonEffectButton",
                ",Art/Interface/Buttons/Units/Warrior.dds,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,3,4",
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                0,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "HideInactive",
                ",Art/Interface/Buttons/Units/Warrior.dds,Art/Interface/Buttons/GodsOfOld_Atlas.dds,8,3",
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                31,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.setImageButton(
                "InfoScreen",
                "",
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                33,
            )
            screen.setStyle("InfoScreen", "Button_HUDAdvisorRecord_Style")

            iX = iXStart + 8
            iY += iAdjust

            screen.addCheckBoxGFC(
                "EditUnitData",
                ",Art/Interface/Buttons/Units/Warrior.dds,Art/Interface/Buttons/Afterworld_Atlas.dds,4,9",
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_UNIT_EDIT_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "EditPromotions",
                ",Art/Interface/Buttons/Promotions/Combat1.dds,Art/Interface/Buttons/Promotions_Atlas.dds,8,2",
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                6,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "EditCityDataI",
                CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_TOGGLE_CITY_EDIT_MODE").getPath(),
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_WB_CITY_EDIT_BUTTON,
                -1,
                -1,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "EditCityDataII",
                ",Art/Interface/Buttons/Buildings/SDI.dds,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,1,8",
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                7,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "EditCityBuildings",
                ",Art/Interface/Buttons/Buildings/SDI.dds,Art/Interface/Buttons/FinalFrontier1_Atlas.dds,5,14",
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                8,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            iX += iAdjust
            screen.addCheckBoxGFC(
                "EditEvents",
                "",
                CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                iX,
                iY,
                iButtonWidth,
                iButtonWidth,
                WidgetTypes.WIDGET_PYTHON,
                1029,
                10,
                ButtonStyles.BUTTON_STYLE_LABEL,
            )
            screen.setStyle("EditEvents", "Button_HUDLog_Style")

            self.setCurrentModeCheckbox()
        return

    def refreshSideMenu(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
        CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
        iButtonWidth = 32
        iAdjust = iButtonWidth + 3
        iScreenWidth = 16 + iAdjust * 6
        iScreenHeight = 16 + iAdjust * 4

        if CyInterface().isInAdvancedStart():
            iX = 50
            iY = 15
            szText = (
                u"<font=4>"
                + CyTranslator().getText(
                    "TXT_KEY_WB_AS_POINTS",
                    (gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartPoints(),),
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
                u"<font=4>"
                + CyTranslator().getText("TXT_KEY_WB_AS_COST_THIS_LOCATION", (self.m_iCost,))
                + u"</font>"
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
            screen.deleteWidget("WorldBuilderLandmarkButton")
            screen.deleteWidget("WorldBuilderRevealAll")
            screen.deleteWidget("WorldBuilderUnrevealAll")
            screen.deleteWidget("WorldBuilderRevealPanel")
            screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
            screen.deleteWidget("EditPlayerData")
            screen.deleteWidget("EditTeamData")
            screen.deleteWidget("EditTechnologies")
            screen.deleteWidget("EditProjects")
            screen.deleteWidget("EditUnitsCities")
            screen.deleteWidget("ChangeBy")
            screen.deleteWidget("AddOwnershipButton")
            screen.deleteWidget("AddUnitsButton")
            screen.deleteWidget("AddBuildingsButton")
            screen.deleteWidget("AddCityButton")
            screen.deleteWidget("EditStartingPlot")
            screen.deleteWidget("EditPlotData")
            screen.deleteWidget("AddImprovementButton")
            screen.deleteWidget("AddBonusButton")
            screen.deleteWidget("AddPlotTypeButton")
            screen.deleteWidget("AddTerrainButton")
            screen.deleteWidget("AddRouteButton")
            screen.deleteWidget("AddFeatureButton")
            screen.deleteWidget("AddRiverButton")
            screen.deleteWidget("WBCurrentItem")
            screen.deleteWidget("WBSelectClass")
            screen.deleteWidget("WBSelectItem")
            screen.deleteWidget("RevealMode")
            screen.deleteWidget("WorldBuilderEraseAll")
            screen.deleteWidget("BrushWidth")
            screen.deleteWidget("BrushHeight")
            screen.deleteWidget("SensibilityCheck")
            ## Panel Screen ##
            nRows = 1
            if (
                self.iPlayerAddMode in self.PlayerMode
                or self.iPlayerAddMode in self.RevealMode
                or self.iPlayerAddMode in self.MapMode
            ):
                nRows = 3
            iHeight = 16 + iAdjust * nRows
            iXStart = screen.getXResolution() - iScreenWidth
            screen.addPanel(
                "WorldBuilderBackgroundBottomPanel",
                "",
                "",
                True,
                True,
                iXStart,
                iScreenHeight - 10,
                iScreenWidth,
                iHeight,
                PanelStyles.PANEL_STYLE_MAIN,
            )
            iY = iScreenHeight
            if self.iPlayerAddMode in self.PlayerMode:
                iX = iXStart + 8
                screen.addCheckBoxGFC(
                    "AddOwnershipButton",
                    gc.getCivilizationInfo(
                        gc.getPlayer(self.m_iCurrentPlayer).getCivilizationType()
                    ).getButton(),
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    28,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addDropDownBoxGFC(
                    "WorldBuilderPlayerChoice",
                    iX,
                    iY,
                    screen.getXResolution() - 8 - iX,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for iPlayer in xrange(gc.getMAX_PLAYERS()):  # type: ignore
                    if gc.getPlayer(iPlayer).isEverAlive():
                        sName = gc.getPlayer(iPlayer).getName()
                        if not gc.getPlayer(iPlayer).isAlive():
                            sName = "*" + sName
                        if gc.getPlayer(iPlayer).isTurnActive():
                            sName = "[" + sName + "]"
                        screen.addPullDownString(
                            "WorldBuilderPlayerChoice",
                            sName,
                            iPlayer,
                            iPlayer,
                            self.m_iCurrentPlayer == iPlayer,
                        )
                iX = screen.getXResolution() - iScreenWidth + 8
                iY += iAdjust
                screen.setImageButton(
                    "EditPlayerData",
                    gc.getLeaderHeadInfo(
                        gc.getPlayer(self.m_iCurrentPlayer).getLeaderType()
                    ).getButton(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    1,
                )
                iX += iAdjust
                screen.setImageButton(
                    "EditTeamData",
                    ",Art/Interface/Buttons/Buildings/SDI.dds,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,8,7",
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    2,
                )
                iX += iAdjust
                screen.setImageButton(
                    "EditTechnologies",
                    ",Art/Interface/Buttons/TechTree/Physics.dds,Art/Interface/Buttons/TechTree_Atlas.dds,5,6",
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    3,
                )
                iX += iAdjust
                screen.setImageButton(
                    "EditProjects",
                    ",Art/Interface/Buttons/Buildings/SDI.dds,Art/Interface/Buttons/Buildings_Atlas.dds,1,6",
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    4,
                )
                iX += iAdjust
                screen.setImageButton(
                    "EditUnitsCities",
                    ",Art/Interface/Buttons/Buildings/SDI.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,3,12",
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    5,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "EditStartingPlot",
                    ",Art/Interface/Buttons/Units/Warrior.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,4,13",
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    32,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )

                iY += iAdjust
                iX = iXStart + 8
                screen.addCheckBoxGFC(
                    "AddUnitsButton",
                    ",Art/Interface/Buttons/Units/Warrior.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,6,10",
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    27,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "AddBuildingsButton",
                    CyArtFileMgr()
                    .getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION")
                    .getPath(),
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    19,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "AddCityButton",
                    ",Art/Interface/Buttons/Actions/FoundCity.dds,Art/Interface/Buttons/Charlemagne_Atlas.dds,4,2",
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    18,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addDropDownBoxGFC(
                    "ChangeBy",
                    iX,
                    iY,
                    screen.getXResolution() - 8 - iX,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                i = 1
                while i < 1001:
                    screen.addPullDownString("ChangeBy", str(i), i, i, iChange == i)
                    if str(i)[0] == "1":
                        i *= 5
                    else:
                        i *= 2
                sText = (
                    "<font=3b>"
                    + CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ())
                    + "</font>"
                )

            elif self.iPlayerAddMode in self.MapMode:
                iX = iXStart + 8
                screen.addCheckBoxGFC(
                    "EditPlotData",
                    ",Art/Interface/Buttons/WorldBuilder/Gems.dds,Art/Interface/Buttons/FinalFrontier1_Atlas.dds,4,16",
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1027,
                    -1,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "AddRiverButton",
                    CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_RIVER_PLACEMENT").getPath(),
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    11,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "WorldBuilderLandmarkButton",
                    CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_LANDMARK_MODE").getPath(),
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_WB_LANDMARK_BUTTON,
                    -1,
                    -1,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addDropDownBoxGFC(
                    "WorldBuilderPlayerChoice",
                    iX,
                    iY,
                    screen.getXResolution() - 8 - iX,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                screen.addPullDownString(
                    "WorldBuilderPlayerChoice",
                    CyTranslator().getText("TXT_KEY_WB_LANDMARKS", ()),
                    gc.getBARBARIAN_PLAYER(),
                    gc.getBARBARIAN_PLAYER(),
                    self.m_iCurrentPlayer == gc.getBARBARIAN_PLAYER(),
                )
                for iPlayer in xrange(gc.getMAX_PLAYERS()):  # type: ignore
                    if iPlayer == gc.getBARBARIAN_PLAYER():
                        continue
                    if gc.getPlayer(iPlayer).isEverAlive():
                        sName = gc.getPlayer(iPlayer).getName()
                        if not gc.getPlayer(iPlayer).isAlive():
                            sName = "*" + sName
                        if gc.getPlayer(iPlayer).isTurnActive():
                            sName = "[" + sName + "]"
                        screen.addPullDownString(
                            "WorldBuilderPlayerChoice",
                            sName,
                            iPlayer,
                            iPlayer,
                            self.m_iCurrentPlayer == iPlayer,
                        )

                iX = iXStart + 8
                iY += iAdjust
                screen.addCheckBoxGFC(
                    "AddImprovementButton",
                    CyArtFileMgr()
                    .getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION")
                    .getPath(),
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    12,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "AddBonusButton",
                    ",Art/Interface/Buttons/WorldBuilder/Gems.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,7,9",
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    13,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "AddPlotTypeButton",
                    CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_CHANGE_ALL_PLOTS").getPath(),
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    14,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "AddTerrainButton",
                    ",Art/Interface/Buttons/BaseTerrain/Grassland.dds,Art/Interface/Buttons/BaseTerrain_TerrainFeatures_Atlas.dds,3,1",
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    15,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "AddRouteButton",
                    "Art/Interface/Buttons/Builds/BuildRoad.dds",
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    16,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                screen.addCheckBoxGFC(
                    "AddFeatureButton",
                    ",Art/Interface/Buttons/TerrainFeatures/Forest.dds,Art/Interface/Buttons/BaseTerrain_TerrainFeatures_Atlas.dds,3,3",
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    17,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )

                iX = iXStart + 8
                iY += iAdjust
                screen.addCheckBoxGFC(
                    "SensibilityCheck",
                    ",Art/Interface/Buttons/WorldBuilder/Gems.dds,Art/Interface/Buttons/FinalFrontier1_Atlas.dds,1,16",
                    CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    24,
                    ButtonStyles.BUTTON_STYLE_LABEL,
                )
                iX += iAdjust
                iWidth = (screen.getXResolution() - 8 - iX - 3) / 2
                screen.addDropDownBoxGFC(
                    "BrushWidth",
                    iX,
                    iY,
                    iWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in range(1, 11):
                    screen.addPullDownString(
                        "BrushWidth", "W: " + str(i), i, i, self.iBrushWidth == i
                    )
                screen.addPullDownString(
                    "BrushWidth", "W: " + "--", -1, -1, self.iBrushWidth == -1
                )
                iX += iWidth
                screen.addDropDownBoxGFC(
                    "BrushHeight",
                    iX,
                    iY,
                    iWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in range(1, 11):
                    screen.addPullDownString(
                        "BrushHeight", "H: " + str(i), i, i, self.iBrushHeight == i
                    )
                screen.addPullDownString(
                    "BrushHeight", "H: " + "--", -1, -1, self.iBrushHeight == -1
                )

            elif self.iPlayerAddMode in self.RevealMode:
                iX = iXStart + 8
                screen.addDropDownBoxGFC(
                    "RevealMode",
                    iX,
                    iY,
                    screen.getXResolution() - 8 - iX,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                screen.addPullDownString(
                    "RevealMode",
                    CyTranslator().getText("TXT_KEY_REVEAL_PLOT", ()),
                    0,
                    0,
                    self.iPlayerAddMode == self.RevealMode[0],
                )
                screen.addPullDownString(
                    "RevealMode",
                    CyTranslator().getText("TXT_KEY_REVEAL_SUBMARINE", ()),
                    1,
                    1,
                    self.iPlayerAddMode == self.RevealMode[1],
                )
                screen.addPullDownString(
                    "RevealMode",
                    CyTranslator().getText("TXT_KEY_REVEAL_STEALTH", ()),
                    2,
                    2,
                    self.iPlayerAddMode == self.RevealMode[2],
                )
                screen.addPullDownString(
                    "RevealMode",
                    gc.getMissionInfo(gc.getInfoTypeForString("MISSION_PLUNDER")).getDescription(),
                    3,
                    3,
                    self.iPlayerAddMode == self.RevealMode[3],
                )

                iY += iAdjust
                screen.setImageButton(
                    "WorldBuilderRevealAll",
                    CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_REVEAL_ALL_TILES").getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_WB_REVEAL_ALL_BUTTON,
                    -1,
                    -1,
                )
                iX += iAdjust
                screen.addDropDownBoxGFC(
                    "WorldBuilderPlayerChoice",
                    iX,
                    iY,
                    screen.getXResolution() - 8 - iX,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for iPlayer in xrange(gc.getMAX_PLAYERS()):  # type: ignore
                    if gc.getPlayer(iPlayer).isEverAlive():
                        sName = gc.getPlayer(iPlayer).getName()
                        if not gc.getPlayer(iPlayer).isAlive():
                            sName = "*" + sName
                        if gc.getPlayer(iPlayer).isTurnActive():
                            sName = "[" + sName + "]"
                        screen.addPullDownString(
                            "WorldBuilderPlayerChoice",
                            sName,
                            iPlayer,
                            iPlayer,
                            self.m_iCurrentPlayer == iPlayer,
                        )
                iX = iXStart + 8
                iY += iAdjust
                screen.setImageButton(
                    "WorldBuilderUnrevealAll",
                    CyArtFileMgr()
                    .getInterfaceArtInfo("WORLDBUILDER_UNREVEAL_ALL_TILES")
                    .getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_WB_UNREVEAL_ALL_BUTTON,
                    -1,
                    -1,
                )
                iX += iAdjust
                iWidth = (screen.getXResolution() - 8 - iX - 3) / 2
                screen.addDropDownBoxGFC(
                    "BrushWidth",
                    iX,
                    iY,
                    iWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in range(1, 11):
                    screen.addPullDownString(
                        "BrushWidth", "W: " + str(i), i, i, self.iBrushWidth == i
                    )
                screen.addPullDownString(
                    "BrushWidth", "W: " + "--", -1, -1, self.iBrushWidth == -1
                )
                iX += iWidth
                screen.addDropDownBoxGFC(
                    "BrushHeight",
                    iX,
                    iY,
                    iWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in range(1, 11):
                    screen.addPullDownString(
                        "BrushHeight", "H: " + str(i), i, i, self.iBrushHeight == i
                    )
                screen.addPullDownString(
                    "BrushHeight", "H: " + "--", -1, -1, self.iBrushHeight == -1
                )

            elif self.iPlayerAddMode == "EraseAll":
                iX = iXStart + 8
                screen.setImageButton(
                    "WorldBuilderEraseAll",
                    CyArtFileMgr()
                    .getInterfaceArtInfo("WORLDBUILDER_UNREVEAL_ALL_TILES")
                    .getPath(),
                    iX,
                    iY,
                    iButtonWidth,
                    iButtonWidth,
                    WidgetTypes.WIDGET_PYTHON,
                    1029,
                    29,
                )
                iX += iAdjust
                iWidth = (screen.getXResolution() - 8 - iX - 3) / 2
                screen.addDropDownBoxGFC(
                    "BrushWidth",
                    iX,
                    iY,
                    iWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in range(1, 11):
                    screen.addPullDownString(
                        "BrushWidth", "W: " + str(i), i, i, self.iBrushWidth == i
                    )
                screen.addPullDownString(
                    "BrushWidth", "W: " + "--", -1, -1, self.iBrushWidth == -1
                )
                iX += iWidth
                screen.addDropDownBoxGFC(
                    "BrushHeight",
                    iX,
                    iY,
                    iWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in range(1, 11):
                    screen.addPullDownString(
                        "BrushHeight", "H: " + str(i), i, i, self.iBrushHeight == i
                    )
                screen.addPullDownString(
                    "BrushHeight", "H: " + "--", -1, -1, self.iBrushHeight == -1
                )
            else:
                screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
            self.setCurrentModeCheckbox()
            self.setSelectionTable()

    def setCurrentModeCheckbox(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        screen.setState("EditUnitData", self.iPlayerAddMode == "EditUnit")
        screen.setState("EditPromotions", self.iPlayerAddMode == "Promotions")
        screen.setState(
            "WorldBuilderNormalPlayerModeButton", self.iPlayerAddMode in self.PlayerMode
        )
        screen.setState("WorldBuilderNormalMapModeButton", self.iPlayerAddMode in self.MapMode)
        screen.setState("WorldBuilderRevealTileModeButton", self.iPlayerAddMode in self.RevealMode)
        screen.setState("WorldBuilderLandmarkButton", self.iPlayerAddMode == "AddLandMark")
        screen.setState("WorldBuilderEraseButton", self.iPlayerAddMode == "EraseAll")
        screen.setState("AddOwnershipButton", self.iPlayerAddMode == "Ownership")
        screen.setState("AddUnitsButton", self.iPlayerAddMode == "Units")
        screen.setState("AddBuildingsButton", self.iPlayerAddMode == "Buildings")
        screen.setState("AddCityButton", self.iPlayerAddMode == "City")
        screen.setState("EditStartingPlot", self.iPlayerAddMode == "StartingPlot")
        screen.setState("EditPlotData", self.iPlayerAddMode == "PlotData")
        screen.setState("EditEvents", self.iPlayerAddMode == "Events")
        screen.setState("AddRiverButton", self.iPlayerAddMode == "River")
        screen.setState("AddImprovementButton", self.iPlayerAddMode == "Improvements")
        screen.setState("AddBonusButton", self.iPlayerAddMode == "Bonus")
        screen.setState("AddPlotTypeButton", self.iPlayerAddMode == "PlotType")
        screen.setState("AddTerrainButton", self.iPlayerAddMode == "Terrain")
        screen.setState("AddRouteButton", self.iPlayerAddMode == "Routes")
        screen.setState("AddFeatureButton", self.iPlayerAddMode == "Features")
        screen.setState("EditCityDataI", self.iPlayerAddMode == "CityDataI")
        screen.setState("EditCityDataII", self.iPlayerAddMode == "CityDataII")
        screen.setState("EditCityBuildings", self.iPlayerAddMode == "CityBuildings")
        screen.setState("PythonEffectButton", bPython)
        screen.setState("HideInactive", bHideInactive)
        screen.setState("SensibilityCheck", self.bSensibility)

    def setSelectionTable(self):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        iWidth = 200
        iCivilization = gc.getPlayer(self.m_iCurrentPlayer).getCivilizationType()
        if self.iPlayerAddMode == "Units":
            iY = 25
            screen.addDropDownBoxGFC(
                "WBSelectClass",
                0,
                iY,
                iWidth,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                FontTypes.GAME_FONT,
            )
            screen.addPullDownString(
                "WBSelectClass",
                CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()),
                -2,
                -2,
                -2 == self.iSelectClass,
            )
            screen.addPullDownString(
                "WBSelectClass",
                CyTranslator().getText("TXT_PEDIA_NON_COMBAT", ()),
                -1,
                -1,
                -1 == self.iSelectClass,
            )
            for iCombatClass in xrange(gc.getNumUnitCombatInfos()):  # type: ignore
                screen.addPullDownString(
                    "WBSelectClass",
                    gc.getUnitCombatInfo(iCombatClass).getDescription(),
                    iCombatClass,
                    iCombatClass,
                    iCombatClass == self.iSelectClass,
                )

            lItems = []
            for i in xrange(gc.getNumUnitInfos()):  # type: ignore
                ItemInfo = gc.getUnitInfo(i)
                if bHideInactive:
                    iClass = ItemInfo.getUnitClassType()
                    if gc.getCivilizationInfo(iCivilization).getCivilizationUnits(iClass) != i:
                        continue
                if ItemInfo.getUnitCombatType() != self.iSelectClass and self.iSelectClass > -2:
                    continue
                lItems.append([ItemInfo.getDescription(), i])
            lItems.sort()

            iY += 30
            iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
            screen.addTableControlGFC(
                "WBSelectItem",
                1,
                0,
                iY,
                iWidth,
                iHeight,
                False,
                False,
                24,
                24,
                TableStyles.TABLE_STYLE_EMPTY,
            )
            screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
            bValid = False
            for item in lItems:
                iRow = screen.appendTableRow("WBSelectItem")
                if self.iSelection == item[1]:
                    bValid = True
                screen.setTableText(
                    "WBSelectItem",
                    0,
                    iRow,
                    "<font=3>" + item[0] + "</font>",
                    gc.getUnitInfo(item[1]).getButton(),
                    WidgetTypes.WIDGET_PYTHON,
                    8202,
                    item[1],
                    CvUtil.FONT_LEFT_JUSTIFY,
                )
            if not bValid:
                self.iSelection = -1
                if len(lItems) > 0:
                    self.iSelection = lItems[0][1]

        elif self.iPlayerAddMode == "Buildings":
            iY = 25
            sWonder = CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ())
            screen.addDropDownBoxGFC(
                "WBSelectClass",
                0,
                iY,
                iWidth,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                FontTypes.GAME_FONT,
            )
            screen.addPullDownString(
                "WBSelectClass",
                CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()),
                0,
                0,
                0 == self.iSelectClass,
            )
            screen.addPullDownString(
                "WBSelectClass",
                CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()),
                1,
                1,
                1 == self.iSelectClass,
            )
            screen.addPullDownString(
                "WBSelectClass",
                CyTranslator().getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ()),
                2,
                2,
                2 == self.iSelectClass,
            )
            screen.addPullDownString(
                "WBSelectClass",
                CyTranslator().getText("TXT_KEY_PEDIA_TEAM_WONDER", ()),
                3,
                3,
                3 == self.iSelectClass,
            )
            screen.addPullDownString(
                "WBSelectClass",
                CyTranslator().getText("TXT_KEY_PEDIA_WORLD_WONDER", ()),
                4,
                4,
                4 == self.iSelectClass,
            )

            lItems = []
            for i in xrange(gc.getNumBuildingInfos()):  # type: ignore
                ItemInfo = gc.getBuildingInfo(i)
                iClass = ItemInfo.getBuildingClassType()
                if bHideInactive:
                    if gc.getCivilizationInfo(iCivilization).getCivilizationBuildings(iClass) != i:
                        continue
                if self.iSelectClass == 1:
                    if isLimitedWonderClass(iClass):
                        continue
                elif self.iSelectClass == 2:
                    if not isNationalWonderClass(iClass):
                        continue
                elif self.iSelectClass == 3:
                    if not isTeamWonderClass(iClass):
                        continue
                elif self.iSelectClass == 4:
                    if not isWorldWonderClass(iClass):
                        continue
                lItems.append([ItemInfo.getDescription(), i])
            lItems.sort()

            iY += 30
            iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
            screen.addTableControlGFC(
                "WBSelectItem",
                1,
                0,
                iY,
                iWidth,
                iHeight,
                False,
                False,
                24,
                24,
                TableStyles.TABLE_STYLE_EMPTY,
            )
            screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
            bValid = False
            for item in lItems:
                iRow = screen.appendTableRow("WBSelectItem")
                if self.iSelection == item[1]:
                    bValid = True
                screen.setTableText(
                    "WBSelectItem",
                    0,
                    iRow,
                    "<font=3>" + item[0] + "</font>",
                    gc.getBuildingInfo(item[1]).getButton(),
                    WidgetTypes.WIDGET_HELP_BUILDING,
                    item[1],
                    item[1],
                    CvUtil.FONT_LEFT_JUSTIFY,
                )
            if not bValid:
                self.iSelection = -1
                if len(lItems) > 0:
                    self.iSelection = lItems[0][1]

        elif self.iPlayerAddMode == "Features":
            iY = 55
            lItems = []
            for i in xrange(gc.getNumFeatureInfos()):  # type: ignore
                ItemInfo = gc.getFeatureInfo(i)
                lItems.append([ItemInfo.getDescription(), i])
            lItems.sort()

            iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
            screen.addTableControlGFC(
                "WBSelectItem",
                1,
                0,
                iY,
                iWidth,
                iHeight,
                False,
                False,
                24,
                24,
                TableStyles.TABLE_STYLE_EMPTY,
            )
            screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
            for item in lItems:
                iRow = screen.appendTableRow("WBSelectItem")
                if self.iSelection == -1:
                    self.iSelection = item[1]
                screen.setTableText(
                    "WBSelectItem",
                    0,
                    iRow,
                    "<font=3>" + item[0] + "</font>",
                    gc.getFeatureInfo(item[1]).getButton(),
                    WidgetTypes.WIDGET_PYTHON,
                    7874,
                    item[1],
                    CvUtil.FONT_LEFT_JUSTIFY,
                )

        elif self.iPlayerAddMode == "Improvements":
            iY = 25
            lItems = []
            for i in xrange(gc.getNumImprovementInfos()):  # type: ignore
                ItemInfo = gc.getImprovementInfo(i)
                if ItemInfo.isGraphicalOnly():
                    continue
                lItems.append([ItemInfo.getDescription(), i])
            lItems.sort()

            iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
            screen.addTableControlGFC(
                "WBSelectItem",
                1,
                0,
                iY,
                iWidth,
                iHeight,
                False,
                False,
                24,
                24,
                TableStyles.TABLE_STYLE_EMPTY,
            )
            screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
            for item in lItems:
                iRow = screen.appendTableRow("WBSelectItem")
                if self.iSelection == -1:
                    self.iSelection = item[1]
                screen.setTableText(
                    "WBSelectItem",
                    0,
                    iRow,
                    "<font=3>" + item[0] + "</font>",
                    gc.getImprovementInfo(item[1]).getButton(),
                    WidgetTypes.WIDGET_PYTHON,
                    7877,
                    item[1],
                    CvUtil.FONT_LEFT_JUSTIFY,
                )

        elif self.iPlayerAddMode == "Bonus":
            iY = 25
            screen.addDropDownBoxGFC(
                "WBSelectClass",
                0,
                iY,
                iWidth,
                WidgetTypes.WIDGET_GENERAL,
                -1,
                -1,
                FontTypes.GAME_FONT,
            )
            screen.addPullDownString(
                "WBSelectClass",
                CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()),
                -1,
                -1,
                -1 == self.iSelectClass,
            )
            screen.addPullDownString(
                "WBSelectClass",
                CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL", ()),
                0,
                0,
                0 == self.iSelectClass,
            )
            iBonusClass = 1
            while gc.getBonusClassInfo(iBonusClass) is not None:
                sText = gc.getBonusClassInfo(iBonusClass).getType()
                sText = sText[sText.find("_") + 1 :]
                sText = sText.lower()
                sText = sText.capitalize()
                screen.addPullDownString(
                    "WBSelectClass",
                    sText,
                    iBonusClass,
                    iBonusClass,
                    iBonusClass == self.iSelectClass,
                )
                iBonusClass += 1

            lItems = []
            for i in xrange(gc.getNumBonusInfos()):  # type: ignore
                ItemInfo = gc.getBonusInfo(i)
                if ItemInfo.getBonusClassType() != self.iSelectClass and self.iSelectClass > -1:
                    continue
                lItems.append([ItemInfo.getDescription(), i])
            lItems.sort()

            iY += 30
            iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
            screen.addTableControlGFC(
                "WBSelectItem",
                1,
                0,
                iY,
                iWidth,
                iHeight,
                False,
                False,
                24,
                24,
                TableStyles.TABLE_STYLE_EMPTY,
            )
            screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
            for item in lItems:
                iRow = screen.appendTableRow("WBSelectItem")
                if self.iSelection == -1:
                    self.iSelection = item[1]
                screen.setTableText(
                    "WBSelectItem",
                    0,
                    iRow,
                    "<font=3>" + item[0] + "</font>",
                    gc.getBonusInfo(item[1]).getButton(),
                    WidgetTypes.WIDGET_PYTHON,
                    7878,
                    item[1],
                    CvUtil.FONT_LEFT_JUSTIFY,
                )

        elif self.iPlayerAddMode == "Routes":
            iY = 25
            lItems = []
            for i in xrange(gc.getNumRouteInfos()):  # type: ignore
                ItemInfo = gc.getRouteInfo(i)
                lItems.append([ItemInfo.getDescription(), i])
            lItems.sort()

            iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
            screen.addTableControlGFC(
                "WBSelectItem",
                1,
                0,
                iY,
                iWidth,
                iHeight,
                False,
                False,
                24,
                24,
                TableStyles.TABLE_STYLE_EMPTY,
            )
            screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
            for item in lItems:
                iRow = screen.appendTableRow("WBSelectItem")
                if self.iSelection == -1:
                    self.iSelection = item[1]
                screen.setTableText(
                    "WBSelectItem",
                    0,
                    iRow,
                    "<font=3>" + item[0] + "</font>",
                    gc.getRouteInfo(item[1]).getButton(),
                    WidgetTypes.WIDGET_PYTHON,
                    6788,
                    item[1],
                    CvUtil.FONT_LEFT_JUSTIFY,
                )

        elif self.iPlayerAddMode == "Terrain":
            iY = 25
            lItems = []
            for i in xrange(gc.getNumTerrainInfos()):  # type: ignore
                ItemInfo = gc.getTerrainInfo(i)
                if ItemInfo.isGraphicalOnly():
                    continue
                lItems.append([ItemInfo.getDescription(), i])
            lItems.sort()

            iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
            screen.addTableControlGFC(
                "WBSelectItem",
                1,
                0,
                iY,
                iWidth,
                iHeight,
                False,
                False,
                24,
                24,
                TableStyles.TABLE_STYLE_EMPTY,
            )
            screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
            for item in lItems:
                iRow = screen.appendTableRow("WBSelectItem")
                if self.iSelection == -1:
                    self.iSelection = item[1]
                screen.setTableText(
                    "WBSelectItem",
                    0,
                    iRow,
                    "<font=3>" + item[0] + "</font>",
                    gc.getTerrainInfo(item[1]).getButton(),
                    WidgetTypes.WIDGET_PYTHON,
                    7875,
                    item[1],
                    CvUtil.FONT_LEFT_JUSTIFY,
                )

        elif self.iPlayerAddMode == "PlotType":
            iY = 25
            iHeight = 4 * 24 + 2
            screen.addTableControlGFC(
                "WBSelectItem",
                1,
                0,
                25,
                iWidth,
                iHeight,
                False,
                False,
                24,
                24,
                TableStyles.TABLE_STYLE_EMPTY,
            )
            screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
            for i in xrange(PlotTypes.NUM_PLOT_TYPES):  # type: ignore
                screen.appendTableRow("WBSelectItem")
            item = gc.getInfoTypeForString("TERRAIN_PEAK")
            if self.iSelection == -1:
                self.iSelection = item
            screen.setTableText(
                "WBSelectItem",
                0,
                0,
                "<font=3>" + gc.getTerrainInfo(item).getDescription() + "</font>",
                gc.getTerrainInfo(item).getButton(),
                WidgetTypes.WIDGET_PYTHON,
                7875,
                item,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
            item = gc.getInfoTypeForString("TERRAIN_HILL")
            screen.setTableText(
                "WBSelectItem",
                0,
                1,
                "<font=3>" + gc.getTerrainInfo(item).getDescription() + "</font>",
                gc.getTerrainInfo(item).getButton(),
                WidgetTypes.WIDGET_PYTHON,
                7875,
                item,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
            item = gc.getInfoTypeForString("TERRAIN_GRASS")
            screen.setTableText(
                "WBSelectItem",
                0,
                2,
                "<font=3>" + gc.getTerrainInfo(item).getDescription() + "</font>",
                gc.getTerrainInfo(item).getButton(),
                WidgetTypes.WIDGET_PYTHON,
                7875,
                item,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
            item = gc.getInfoTypeForString("TERRAIN_OCEAN")
            screen.setTableText(
                "WBSelectItem",
                0,
                3,
                "<font=3>" + gc.getTerrainInfo(item).getDescription() + "</font>",
                gc.getTerrainInfo(item).getButton(),
                WidgetTypes.WIDGET_PYTHON,
                7875,
                item,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        self.refreshSelection()

    def refreshSelection(self):
        if self.iSelection == -1:
            return
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        iWidth = 200
        screen.addTableControlGFC(
            "WBCurrentItem",
            1,
            0,
            0,
            iWidth,
            25,
            False,
            True,
            24,
            24,
            TableStyles.TABLE_STYLE_EMPTY,
        )
        screen.setTableColumnHeader("WBCurrentItem", 0, "", iWidth)
        screen.appendTableRow("WBCurrentItem")
        if self.iPlayerAddMode == "Units":
            ItemInfo = gc.getUnitInfo(self.iSelection)
            sText = (
                "<font=3>"
                + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
                + ItemInfo.getDescription()
                + "</color></font>"
            )
            screen.setTableText(
                "WBCurrentItem",
                0,
                0,
                sText,
                ItemInfo.getButton(),
                WidgetTypes.WIDGET_PYTHON,
                8202,
                self.iSelection,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        elif self.iPlayerAddMode == "Buildings":
            ItemInfo = gc.getBuildingInfo(self.iSelection)
            sText = (
                "<font=3>"
                + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
                + ItemInfo.getDescription()
                + "</color></font>"
            )
            screen.setTableText(
                "WBCurrentItem",
                0,
                0,
                sText,
                ItemInfo.getButton(),
                WidgetTypes.WIDGET_HELP_BUILDING,
                self.iSelection,
                1,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        elif self.iPlayerAddMode == "Features":
            ItemInfo = gc.getFeatureInfo(self.iSelection)
            sText = (
                "<font=3>"
                + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
                + ItemInfo.getDescription()
                + "</color></font>"
            )
            screen.setTableText(
                "WBCurrentItem",
                0,
                0,
                sText,
                ItemInfo.getButton(),
                WidgetTypes.WIDGET_PYTHON,
                7874,
                self.iSelection,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
            if ItemInfo.getNumVarieties() > 1:
                screen.addDropDownBoxGFC(
                    "WBSelectClass",
                    0,
                    25,
                    iWidth,
                    WidgetTypes.WIDGET_GENERAL,
                    -1,
                    -1,
                    FontTypes.GAME_FONT,
                )
                for i in xrange(ItemInfo.getNumVarieties()):  # type: ignore
                    screen.addPullDownString(
                        "WBSelectClass",
                        CyTranslator().getText("TXT_KEY_WB_FEATURE_VARIETY", (i,)),
                        i,
                        i,
                        i == self.iSelectClass,
                    )
            else:
                self.iSelectClass = 0
                screen.hide("WBSelectClass")
        elif self.iPlayerAddMode == "Improvements":
            ItemInfo = gc.getImprovementInfo(self.iSelection)
            sText = (
                "<font=3>"
                + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
                + ItemInfo.getDescription()
                + "</color></font>"
            )
            screen.setTableText(
                "WBCurrentItem",
                0,
                0,
                sText,
                ItemInfo.getButton(),
                WidgetTypes.WIDGET_PYTHON,
                7877,
                self.iSelection,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        elif self.iPlayerAddMode == "Bonus":
            ItemInfo = gc.getBonusInfo(self.iSelection)
            sText = (
                "<font=3>"
                + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
                + ItemInfo.getDescription()
                + "</color></font>"
            )
            screen.setTableText(
                "WBCurrentItem",
                0,
                0,
                sText,
                ItemInfo.getButton(),
                WidgetTypes.WIDGET_PYTHON,
                7878,
                self.iSelection,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        elif self.iPlayerAddMode == "Routes":
            ItemInfo = gc.getRouteInfo(self.iSelection)
            sText = (
                "<font=3>"
                + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
                + ItemInfo.getDescription()
                + "</color></font>"
            )
            screen.setTableText(
                "WBCurrentItem",
                0,
                0,
                sText,
                ItemInfo.getButton(),
                WidgetTypes.WIDGET_PYTHON,
                6788,
                self.iSelection,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        elif self.iPlayerAddMode == "Terrain" or self.iPlayerAddMode == "PlotType":
            ItemInfo = gc.getTerrainInfo(self.iSelection)
            sText = (
                "<font=3>"
                + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
                + ItemInfo.getDescription()
                + "</color></font>"
            )
            screen.setTableText(
                "WBCurrentItem",
                0,
                0,
                sText,
                ItemInfo.getButton(),
                WidgetTypes.WIDGET_PYTHON,
                7875,
                self.iSelection,
                CvUtil.FONT_LEFT_JUSTIFY,
            )
        else:
            screen.hide("WBCurrentItem")

    ## Platy Reveal Mode Start ##
    def revealAll(self, bReveal):
        for i in xrange(CyMap().numPlots()):  # type: ignore
            pPlot = CyMap().plotByIndex(i)
            if pPlot.isNone():
                continue
            self.RevealCurrentPlot(bReveal, pPlot)
        self.refreshReveal()
        return

    def RevealCurrentPlot(self, bReveal, pPlot):
        if self.iPlayerAddMode == "Blockade":
            return
        iType = gc.getInfoTypeForString(self.iPlayerAddMode)
        if iType == -1:
            if bReveal or (not pPlot.isVisible(self.m_iCurrentTeam, False)):
                pPlot.setRevealed(self.m_iCurrentTeam, bReveal, False, -1)
        elif bReveal:
            if pPlot.isInvisibleVisible(self.m_iCurrentTeam, iType):
                return
            pPlot.changeInvisibleVisibilityCount(self.m_iCurrentTeam, iType, 1)
        else:
            pPlot.changeInvisibleVisibilityCount(
                self.m_iCurrentTeam,
                iType,
                -pPlot.getInvisibleVisibilityCount(self.m_iCurrentTeam, iType),
            )
        return

    def showRevealed(self, pPlot):
        if self.iPlayerAddMode == "RevealPlot":
            if not pPlot.isRevealed(self.m_iCurrentTeam, False):
                CyEngine().fillAreaBorderPlotAlt(
                    pPlot.getX(),
                    pPlot.getY(),
                    AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS,
                    "COLOR_BLACK",
                    1.0,
                )
        elif self.iPlayerAddMode == "INVISIBLE_SUBMARINE":
            if (
                pPlot.getInvisibleVisibilityCount(
                    self.m_iCurrentTeam, gc.getInfoTypeForString(self.iPlayerAddMode)
                )
                == 0
            ):
                CyEngine().fillAreaBorderPlotAlt(
                    pPlot.getX(),
                    pPlot.getY(),
                    AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS,
                    "COLOR_RED",
                    1.0,
                )
        elif self.iPlayerAddMode == "INVISIBLE_STEALTH":
            if (
                pPlot.getInvisibleVisibilityCount(
                    self.m_iCurrentTeam, gc.getInfoTypeForString(self.iPlayerAddMode)
                )
                == 0
            ):
                CyEngine().fillAreaBorderPlotAlt(
                    pPlot.getX(),
                    pPlot.getY(),
                    AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS,
                    "COLOR_BLUE",
                    1.0,
                )
        elif self.iPlayerAddMode == "Blockade":
            if pPlot.isTradeNetwork(self.m_iCurrentTeam):
                return
            if gc.getTeam(self.m_iCurrentTeam).isAtWar(pPlot.getTeam()):
                return
            if pPlot.isTradeNetworkImpassable(self.m_iCurrentTeam):
                return
            if not pPlot.isOwned() and not pPlot.isRevealed(self.m_iCurrentTeam, False):
                return
            if not pPlot.isBonusNetwork(self.m_iCurrentTeam):
                return
            CyEngine().fillAreaBorderPlotAlt(
                pPlot.getX(),
                pPlot.getY(),
                AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS,
                "COLOR_MAGENTA",
                1.0,
            )
        return

    ## Platy Reveal Mode End ##

    def Exit(self):
        CyInterface().setWorldBuilder(False)
        return

    def refreshAdvancedStartTabCtrl(self, bReuse):
        if CyInterface().isInAdvancedStart():
            iActiveTab = 0
            iActiveList = 0
            iActiveIndex = 0

            if self.m_advancedStartTabCtrl and bReuse:
                iActiveTab = self.m_advancedStartTabCtrl.getActiveTab()
                iActiveList = self.m_iAdvancedStartCurrentList[iActiveTab]
                iActiveIndex = self.m_iAdvancedStartCurrentIndexes[iActiveTab]

            self.m_iCurrentPlayer = CyGame().getActivePlayer()
            self.m_iCurrentTeam = CyGame().getActiveTeam()
            self.m_iAdvancedStartCurrentIndexes = []
            self.m_iAdvancedStartCurrentList = []

            initWBToolAdvancedStartControl()  # type: ignore

            self.m_advancedStartTabCtrl = getWBToolAdvancedStartTabCtrl()  # type: ignore

            self.m_advancedStartTabCtrl.setNumColumns((gc.getNumBuildingInfos() / 10) + 2)
            self.m_advancedStartTabCtrl.addTabSection(
                CyTranslator().getText("TXT_KEY_WB_AS_CITIES", ())
            )
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iAdvancedStartCurrentList.append(self.m_iASCityListID)

            self.m_advancedStartTabCtrl.setNumColumns((gc.getNumUnitInfos() / 10) + 2)
            self.m_advancedStartTabCtrl.addTabSection(
                CyTranslator().getText("TXT_KEY_WB_AS_UNITS", ())
            )
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iAdvancedStartCurrentList.append(0)

            self.m_advancedStartTabCtrl.setNumColumns((gc.getNumImprovementInfos() / 10) + 2)
            self.m_advancedStartTabCtrl.addTabSection(
                CyTranslator().getText("TXT_KEY_WB_AS_IMPROVEMENTS", ())
            )
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iAdvancedStartCurrentList.append(self.m_iASRoutesListID)

            self.m_advancedStartTabCtrl.setNumColumns(1)
            self.m_advancedStartTabCtrl.addTabSection(
                CyTranslator().getText("TXT_KEY_WB_AS_VISIBILITY", ())
            )
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iAdvancedStartCurrentList.append(0)

            self.m_advancedStartTabCtrl.setNumColumns(1)
            self.m_advancedStartTabCtrl.addTabSection(
                CyTranslator().getText("TXT_KEY_WB_AS_TECH", ())
            )
            self.m_iAdvancedStartCurrentIndexes.append(0)

            self.m_iAdvancedStartCurrentList.append(0)

            addWBAdvancedStartControlTabs()  # type: ignore

            self.m_advancedStartTabCtrl.setActiveTab(iActiveTab)
            self.setCurrentAdvancedStartIndex(iActiveIndex)
            self.setCurrentAdvancedStartList(iActiveList)
        else:
            self.m_advancedStartTabCtrl = getWBToolAdvancedStartTabCtrl()  # type: ignore
            self.m_advancedStartTabCtrl.enable(False)
        return

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

        for x in xrange(self.m_pRiverStartPlot.getX() - 1, self.m_pRiverStartPlot.getX() + 2):  # type: ignore
            for y in xrange(self.m_pRiverStartPlot.getY() - 1, self.m_pRiverStartPlot.getY() + 2):  # type: ignore
                if x == self.m_pRiverStartPlot.getX() and y == self.m_pRiverStartPlot.getY():
                    continue
                CyEngine().addColoredPlotAlt(
                    x,
                    y,
                    PlotStyles.PLOT_STYLE_BOX_FILL,
                    PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS,
                    "COLOR_WHITE",
                    0.2,
                )
        return

    def leftMouseDown(self, argsList):
        bShift, bCtrl, bAlt = argsList
        pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
        if CyInterface().isInAdvancedStart():
            self.placeObject()
        elif bAlt or self.iPlayerAddMode == "EditUnit":
            if self.m_pCurrentPlot.getNumUnits():
                WBUnitScreen.WBUnitScreen(self).interfaceScreen(self.m_pCurrentPlot.getUnit(0))
        elif self.iPlayerAddMode == "Promotions":
            if self.m_pCurrentPlot.getNumUnits():
                WBPromotionScreen.WBPromotionScreen().interfaceScreen(
                    self.m_pCurrentPlot.getUnit(0)
                )
        elif bCtrl or self.iPlayerAddMode == "CityDataI":
            if self.m_pCurrentPlot.isCity():
                WBCityEditScreen.WBCityEditScreen(self).interfaceScreen(
                    self.m_pCurrentPlot.getPlotCity()
                )
        elif self.iPlayerAddMode == "CityDataII":
            if self.m_pCurrentPlot.isCity():
                WBCityDataScreen.WBCityDataScreen().interfaceScreen(
                    self.m_pCurrentPlot.getPlotCity()
                )
        elif self.iPlayerAddMode == "CityBuildings":
            if self.m_pCurrentPlot.isCity():
                WBBuildingScreen.WBBuildingScreen().interfaceScreen(
                    self.m_pCurrentPlot.getPlotCity()
                )
        elif self.iPlayerAddMode in self.RevealMode:
            if not self.m_pCurrentPlot.isNone():
                self.setMultipleReveal(True)
        elif self.iPlayerAddMode == "PlotData":
            WBPlotScreen.WBPlotScreen().interfaceScreen(self.m_pCurrentPlot)
        elif self.iPlayerAddMode == "Events":
            WBEventScreen.WBEventScreen().interfaceScreen(self.m_pCurrentPlot)
        elif self.iPlayerAddMode == "StartingPlot":
            pPlayer.setStartingPlot(self.m_pCurrentPlot, True)
            self.refreshStartingPlots()
        elif self.iPlayerAddMode == "TargetPlot":
            self.iTargetPlotX = self.m_pCurrentPlot.getX()
            self.iTargetPlotY = self.m_pCurrentPlot.getY()
            self.iPlayerAddMode = "EditUnit"
            if len(self.TempInfo) >= 2:
                pPlayerX = gc.getPlayer(self.TempInfo[0])
                if pPlayerX:
                    pUnitX = pPlayerX.getUnit(self.TempInfo[1])
                    if pUnitX:
                        WBUnitScreen.WBUnitScreen(self).interfaceScreen(pUnitX)
        elif self.iPlayerAddMode == "MoveUnits":
            if len(self.lMoveUnit) > 0:
                for item in self.lMoveUnit:
                    loopUnit = gc.getPlayer(item[0]).getUnit(item[1])
                    if loopUnit.isNone():
                        continue
                    loopUnit.setXY(
                        self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY(), True, True, False
                    )
                pUnitX = gc.getPlayer(self.lMoveUnit[0][0]).getUnit(self.lMoveUnit[0][1])
                self.lMoveUnit = []
                self.iPlayerAddMode = "EditUnit"
                WBUnitScreen.WBUnitScreen(self).interfaceScreen(pUnitX)
        elif self.iPlayerAddMode == "MoveCity" or self.iPlayerAddMode == "MoveCityPlus":
            if self.m_pCurrentPlot.isCity():
                return
            pOldCity = pPlayer.getCity(self.iMoveCity)
            if pOldCity:
                pNewCity = pPlayer.initCity(self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY())
                sName = pOldCity.getName()
                pOldCity.setName("ToBeRazed", False)
                pNewCity.setName(sName, True)
                self.copyCityStats(pOldCity, pNewCity, True)
                pOldPlot = pOldCity.plot()
                pOldCity.kill()
                pOldPlot.setImprovementType(-1)
                if self.iPlayerAddMode == "MoveCityPlus":
                    for item in self.lMoveUnit:
                        loopUnit = gc.getPlayer(item[0]).getUnit(item[1])
                        if loopUnit.isNone():
                            continue
                        loopUnit.setXY(
                            self.m_pCurrentPlot.getX(),
                            self.m_pCurrentPlot.getY(),
                            True,
                            True,
                            False,
                        )
                    self.lMoveUnit = []
            self.iPlayerAddMode = "CityDataI"
            self.iMoveCity = -1
        elif self.iPlayerAddMode == "DuplicateCity" or self.iPlayerAddMode == "DuplicateCityPlus":
            if self.m_pCurrentPlot.isCity():
                return
            pOldCity = pPlayer.getCity(self.iMoveCity)
            if pOldCity:
                pNewCity = pPlayer.initCity(self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY())
                self.copyCityStats(pOldCity, pNewCity, False)
                if self.iPlayerAddMode == "DuplicateCityPlus":
                    for item in self.lMoveUnit:
                        loopUnit = gc.getPlayer(item[0]).getUnit(item[1])
                        if loopUnit.isNone():
                            continue
                        pNewUnit = pPlayer.initUnit(
                            loopUnit.getUnitType(),
                            self.m_pCurrentPlot.getX(),
                            self.m_pCurrentPlot.getY(),
                            UnitAITypes.NO_UNITAI,
                            DirectionTypes.NO_DIRECTION,
                        )
                        pNewUnit.setName(loopUnit.getNameNoDesc())
                        pNewUnit.setLevel(loopUnit.getLevel())
                        pNewUnit.setExperience(loopUnit.getExperience(), -1)
                        pNewUnit.setBaseCombatStr(loopUnit.baseCombatStr())
                        for iPromotion in xrange(gc.getNumPromotionInfos()):  # type: ignore
                            pNewUnit.setHasPromotion(
                                iPromotion, loopUnit.isHasPromotion(iPromotion)
                            )
                        pNewUnit.setDamage(loopUnit.getDamage(), -1)
                        pNewUnit.setMoves(loopUnit.getMoves())
                        pNewUnit.setLeaderUnitType(loopUnit.getLeaderUnitType())
                        pNewUnit.changeCargoSpace(loopUnit.cargoSpace() - pNewUnit.cargoSpace())
                        pNewUnit.setImmobileTimer(loopUnit.getImmobileTimer())
                        pNewUnit.setScriptData(loopUnit.getScriptData())
        elif self.useLargeBrush():
            self.placeMultipleObjects()
        else:
            self.placeObject()
        return 1

    def copyCityStats(self, pOldCity, pNewCity, bMove):
        pNewCity.setPopulation(pOldCity.getPopulation())
        for iBuilding in xrange(gc.getNumBuildingInfos()):  # type: ignore
            pNewCity.setBuildingProduction(iBuilding, pOldCity.getBuildingProduction(iBuilding))
            if gc.getBuildingInfo(iBuilding).isCapital() and not bMove:
                continue
            pNewCity.setNumRealBuilding(iBuilding, pOldCity.getNumRealBuilding(iBuilding))
        for iClass in xrange(gc.getNumBuildingClassInfos()):  # type: ignore
            for iCommerce in xrange(CommerceTypes.NUM_COMMERCE_TYPES):  # type: ignore
                pNewCity.setBuildingCommerceChange(
                    iClass, iCommerce, pOldCity.getBuildingCommerceChange(iClass, iCommerce)
                )
            for iYield in xrange(YieldTypes.NUM_YIELD_TYPES):  # type: ignore
                pNewCity.setBuildingYieldChange(
                    iClass, iYield, pOldCity.getBuildingYieldChange(iClass, iYield)
                )
        ##		pNewCity.setBuildingHappyChange(iClass, pOldCity.getBuildingHappyChange(iClass))
        ##		pNewCity.setBuildingHealthChange(iClass, pOldCity.getBuildingHealthChange(iClass))
        for iPlayerX in xrange(gc.getMAX_PLAYERS()):  # type: ignore
            pNewCity.setCultureTimes100(iPlayerX, pOldCity.getCultureTimes100(iPlayerX), False)
        for iReligion in xrange(gc.getNumReligionInfos()):  # type: ignore
            pNewCity.setHasReligion(iReligion, pOldCity.isHasReligion(iReligion), False, False)
            if bMove and pOldCity.isHolyCityByType(iReligion):
                CyGame().setHolyCity(iReligion, pNewCity, False)
            pNewCity.changeReligionInfluence(
                iReligion,
                pOldCity.getReligionInfluence(iReligion)
                - pNewCity.getReligionInfluence(iReligion),
            )
            pNewCity.changeStateReligionHappiness(
                iReligion,
                pOldCity.getStateReligionHappiness(iReligion)
                - pNewCity.getStateReligionHappiness(iReligion),
            )
        for iCorporation in xrange(gc.getNumCorporationInfos()):  # type: ignore
            pNewCity.setHasCorporation(
                iCorporation, pOldCity.isHasCorporation(iCorporation), False, False
            )
            if bMove and pOldCity.isHeadquartersByType(iCorporation):
                CyGame().setHeadquarters(iCorporation, pNewCity, False)
        for iImprovement in xrange(gc.getNumImprovementInfos()):  # type: ignore
            pNewCity.changeImprovementFreeSpecialists(
                iImprovement,
                pOldCity.getImprovementFreeSpecialists(iImprovement)
                - pNewCity.getImprovementFreeSpecialists(iImprovement),
            )
        for iSpecialist in xrange(gc.getNumSpecialistInfos()):  # type: ignore
            pNewCity.setFreeSpecialistCount(
                iSpecialist, pOldCity.getFreeSpecialistCount(iSpecialist)
            )
            pNewCity.setForceSpecialistCount(
                iSpecialist, pOldCity.getForceSpecialistCount(iSpecialist)
            )
        for iUnit in xrange(gc.getNumUnitInfos()):  # type: ignore
            pNewCity.setUnitProduction(iUnit, pOldCity.getUnitProduction(iUnit))
            pNewCity.setGreatPeopleUnitProgress(iUnit, pOldCity.getGreatPeopleUnitProgress(iUnit))
        for iCommerce in xrange(CommerceTypes.NUM_COMMERCE_TYPES):  # type: ignore
            pNewCity.changeSpecialistCommerce(
                iCommerce,
                pOldCity.getSpecialistCommerce(iCommerce)
                - pNewCity.getSpecialistCommerce(iCommerce),
            )
        for iBonus in xrange(gc.getNumBonusInfos()):  # type: ignore
            pNewCity.changeFreeBonus(
                iBonus, pOldCity.getFreeBonus(iBonus) - pNewCity.getFreeBonus(iBonus)
            )
            while pOldCity.isNoBonus(iBonus) != pNewCity.isNoBonus(iBonus):
                if pOldCity.isNoBonus(iBonus):
                    pNewCity.changeNoBonusCount(iBonus, 1)
                else:
                    pNewCity.changeNoBonusCount(iBonus, -1)
        for iOrder in xrange(pOldCity.getOrderQueueLength()):  # type: ignore
            OrderData = pOldCity.getOrderFromQueue(iOrder)
            pNewCity.pushOrder(
                OrderData.eOrderType,
                OrderData.iData1,
                OrderData.iData2,
                OrderData.bSave,
                False,
                True,
                False,
            )
        pNewCity.changeBaseGreatPeopleRate(
            pOldCity.getBaseGreatPeopleRate() - pNewCity.getBaseGreatPeopleRate()
        )
        pNewCity.changeConscriptAngerTimer(
            pOldCity.getConscriptAngerTimer() - pNewCity.getConscriptAngerTimer()
        )
        pNewCity.changeDefenseDamage(pOldCity.getDefenseDamage() - pNewCity.getDefenseDamage())
        pNewCity.changeDefyResolutionAngerTimer(
            pOldCity.getDefyResolutionAngerTimer() - pNewCity.getDefyResolutionAngerTimer()
        )
        pNewCity.changeEspionageHappinessCounter(
            pOldCity.getEspionageHappinessCounter() - pNewCity.getEspionageHappinessCounter()
        )
        pNewCity.changeEspionageHealthCounter(
            pOldCity.getEspionageHealthCounter() - pNewCity.getEspionageHealthCounter()
        )
        pNewCity.changeExtraHappiness(pOldCity.getExtraHappiness() - pNewCity.getExtraHappiness())
        pNewCity.changeExtraHealth(pOldCity.getExtraHealth() - pNewCity.getExtraHealth())
        pNewCity.changeExtraTradeRoutes(
            pOldCity.getExtraTradeRoutes() - pNewCity.getExtraTradeRoutes()
        )
        pNewCity.changeGreatPeopleProgress(
            pOldCity.getGreatPeopleProgress() - pNewCity.getGreatPeopleProgress()
        )
        pNewCity.changeHappinessTimer(pOldCity.getHappinessTimer() - pNewCity.getHappinessTimer())
        pNewCity.changeHurryAngerTimer(
            pOldCity.getHurryAngerTimer() - pNewCity.getHurryAngerTimer()
        )
        pNewCity.setAirliftTargeted(pOldCity.isAirliftTargeted())
        pNewCity.setBombarded(pOldCity.isBombarded())
        pNewCity.setCitizensAutomated(pOldCity.isCitizensAutomated())
        pNewCity.setDrafted(pOldCity.isDrafted())
        pNewCity.setFeatureProduction(pOldCity.getFeatureProduction())
        pNewCity.setFood(pOldCity.getFood())
        pNewCity.setHighestPopulation(pOldCity.getHighestPopulation())
        pNewCity.setNeverLost(pOldCity.isNeverLost())
        pNewCity.setOccupationTimer(pOldCity.getOccupationTimer())
        pNewCity.setOverflowProduction(pOldCity.getOverflowProduction())
        pNewCity.setPlundered(pOldCity.isPlundered())
        pNewCity.setProduction(pOldCity.getProduction())
        pNewCity.setProductionAutomated(pOldCity.isProductionAutomated())
        pNewCity.setScriptData(pOldCity.getScriptData())
        pNewCity.setWallOverride(pOldCity.isWallOverride())

    def rightMouseDown(self, argsList):
        if CyInterface().isInAdvancedStart():
            self.removeObject()
        elif self.iPlayerAddMode in self.RevealMode:
            if not self.m_pCurrentPlot.isNone():
                self.setMultipleReveal(False)
        elif self.useLargeBrush():
            self.removeMultipleObjects()
        else:
            self.removeObject()
        return 1

    ## Add "," ##
    def addComma(self, iValue):
        sTemp = str(iValue)
        sStart = ""
        while len(sTemp) > 0:
            if sTemp[0].isdigit():
                break
            sStart += sTemp[0]
            sTemp = sTemp[1:]
        sEnd = sTemp[-3:]
        while len(sTemp) > 3:
            sTemp = sTemp[:-3]
            sEnd = sTemp[-3:] + "," + sEnd
        return sStart + sEnd

    ## Add "," ##

    def handleInput(self, inputClass):
        screen = CyGInterfaceScreen("WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
        global iChange
        global bPython
        global bHideInactive

        if inputClass.getFunctionName() == "WorldBuilderEraseAll":
            for i in xrange(CyMap().numPlots()):  # type: ignore
                self.m_pCurrentPlot = CyMap().plotByIndex(i)
                self.placeObject()

        elif inputClass.getFunctionName() == "TradeScreen":
            WBTradeScreen.WBTradeScreen().interfaceScreen()

        elif inputClass.getFunctionName() == "InfoScreen":
            WBInfoScreen.WBInfoScreen().interfaceScreen(self.m_iCurrentPlayer)

        elif inputClass.getFunctionName() == "EditGameOptions":
            WBGameDataScreen.WBGameDataScreen(self).interfaceScreen()

        elif inputClass.getFunctionName() == "EditReligions":
            WBReligionScreen.WBReligionScreen().interfaceScreen(self.m_iCurrentPlayer)

        elif inputClass.getFunctionName() == "EditCorporations":
            WBCorporationScreen.WBCorporationScreen().interfaceScreen(self.m_iCurrentPlayer)

        elif inputClass.getFunctionName() == "EditEspionage":
            WBDiplomacyScreen.WBDiplomacyScreen().interfaceScreen(self.m_iCurrentPlayer, True)

        elif inputClass.getFunctionName() == "EditPlayerData":
            WBPlayerScreen.WBPlayerScreen().interfaceScreen(self.m_iCurrentPlayer)

        elif inputClass.getFunctionName() == "EditTeamData":
            WBTeamScreen.WBTeamScreen().interfaceScreen(self.m_iCurrentTeam)

        elif inputClass.getFunctionName() == "EditTechnologies":
            WBTechScreen.WBTechScreen().interfaceScreen(self.m_iCurrentTeam)

        elif inputClass.getFunctionName() == "EditProjects":
            WBProjectScreen.WBProjectScreen().interfaceScreen(self.m_iCurrentTeam)

        elif inputClass.getFunctionName() == "EditUnitsCities":
            WBPlayerUnits.WBPlayerUnits().interfaceScreen(self.m_iCurrentPlayer)

        elif inputClass.getFunctionName() == "WorldBuilderPlayerChoice":
            self.m_iCurrentPlayer = screen.getPullDownData(
                "WorldBuilderPlayerChoice",
                screen.getSelectedPullDownID("WorldBuilderPlayerChoice"),
            )
            self.m_iCurrentTeam = gc.getPlayer(self.m_iCurrentPlayer).getTeam()
            self.refreshSideMenu()
            if self.iPlayerAddMode in self.RevealMode:
                self.refreshReveal()

        elif inputClass.getFunctionName() == "ChangeBy":
            iChange = screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))

        elif inputClass.getFunctionName() == "AddOwnershipButton":
            self.iPlayerAddMode = "Ownership"
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddUnitsButton":
            self.iPlayerAddMode = "Units"
            self.iSelectClass = -2
            self.iSelection = -1
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddBuildingsButton":
            self.iPlayerAddMode = "Buildings"
            self.iSelectClass = 0
            self.iSelection = -1
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "EditStartingPlot":
            self.iPlayerAddMode = "StartingPlot"
            self.refreshSideMenu()
            self.refreshStartingPlots()

        elif inputClass.getFunctionName() == "EditPromotions":
            self.iPlayerAddMode = "Promotions"
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddCityButton":
            self.iPlayerAddMode = "City"
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "EditCityDataII":
            self.iPlayerAddMode = "CityDataII"
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "EditCityBuildings":
            self.iPlayerAddMode = "CityBuildings"
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "EditPlotData":
            self.iPlayerAddMode = "PlotData"
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "EditEvents":
            self.iPlayerAddMode = "Events"
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddImprovementButton":
            self.iPlayerAddMode = "Improvements"
            self.iSelection = -1
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddBonusButton":
            self.iPlayerAddMode = "Bonus"
            self.iSelectClass = -1
            self.iSelection = -1
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddPlotTypeButton":
            self.iPlayerAddMode = "PlotType"
            self.iSelection = -1
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddTerrainButton":
            self.iPlayerAddMode = "Terrain"
            self.iSelection = -1
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddRouteButton":
            self.iPlayerAddMode = "Routes"
            self.iSelection = -1
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddFeatureButton":
            self.iPlayerAddMode = "Features"
            self.iSelectClass = 0
            self.iSelection = -1
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "AddRiverButton":
            self.iPlayerAddMode = "River"
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "WBSelectClass":
            self.iSelectClass = screen.getPullDownData(
                "WBSelectClass", screen.getSelectedPullDownID("WBSelectClass")
            )
            if self.iPlayerAddMode != "Features":
                self.iSelection = -1
                self.refreshSideMenu()

        elif inputClass.getFunctionName() == "WBSelectItem":
            self.iSelection = inputClass.getData2()
            self.refreshSelection()

        elif inputClass.getFunctionName() == "RevealMode":
            self.iPlayerAddMode = self.RevealMode[
                screen.getPullDownData("RevealMode", screen.getSelectedPullDownID("RevealMode"))
            ]
            self.refreshReveal()

        elif inputClass.getFunctionName() == "BrushWidth":
            self.iBrushWidth = screen.getPullDownData(
                "BrushWidth", screen.getSelectedPullDownID("BrushWidth")
            )

        elif inputClass.getFunctionName() == "BrushHeight":
            self.iBrushHeight = screen.getPullDownData(
                "BrushHeight", screen.getSelectedPullDownID("BrushHeight")
            )

        elif inputClass.getFunctionName() == "HideInactive":
            bHideInactive = not bHideInactive
            self.refreshSideMenu()

        elif inputClass.getFunctionName() == "PythonEffectButton":
            bPython = not bPython
            self.setCurrentModeCheckbox()

        elif inputClass.getFunctionName() == "SensibilityCheck":
            self.bSensibility = not self.bSensibility
            self.setCurrentModeCheckbox()
        return 1
