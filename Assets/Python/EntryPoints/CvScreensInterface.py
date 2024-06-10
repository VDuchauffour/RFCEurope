## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
# ruff: noqa: F401, F811
from Core import player
import CvMainInterface
import CvDomesticAdvisor
import CvTechChooser
import CvForeignAdvisor
import CvExoticForeignAdvisor
import CvMilitaryAdvisor
import CvFinanceAdvisor
import CvReligionScreen
import CvCorporationScreen
import CvCivicsScreen
import CvVictoryScreen
import CvEspionageAdvisor

import CvOptionsScreen
import CvReplayScreen
import CvHallOfFameScreen
import CvDanQuayle
import CvUnVictoryScreen

import CvDawnOfMan
import CvTechSplashScreen
import CvTopCivs
import CvInfoScreen

import CvIntroMovieScreen
import CvVictoryMovieScreen
import CvWonderMovieScreen
import CvEraMovieScreen
import CvSpaceShipScreen

import CvPediaMain
import CvPediaHistory

import CvDebugTools
import CvDebugInfoScreen

import CvUtil
import CvEventInterface
import CvScreenUtilsInterface
import ScreenInput as PyScreenInput
from CvScreenEnums import *
from CvPythonExtensions import *
from RFCUtils import toggleStabilityOverlay as _toggleStabilityOverlay
from RFCUtils import countAchievedGoals as _countAchievedGoals

# BUG - Options - end
import BugCore

AdvisorOpt = BugCore.game.Advisors
CustDomAdvOpt = BugCore.game.CustDomAdv
TechWindowOpt = BugCore.game.TechWindow
# BUG - Options - end

# < Mercenaries Mod Start >
import CvMercenaryManager

# < Mercenaries Mod End >

g_bIsScreenActive = -1


gc = CyGlobalContext()

## World Builder ## Platypedia
import CvPlatyBuilderScreen
import WBPlotScreen
import WBEventScreen
import WBBuildingScreen
import WBCityDataScreen
import WBCityEditScreen
import WBTechScreen
import WBProjectScreen
import WBTeamScreen
import WBPlayerScreen
import WBUnitScreen
import WBPromotionScreen
import WBDiplomacyScreen
import WBGameDataScreen
import WBPlayerUnits
import WBReligionScreen
import WBCorporationScreen
import WBInfoScreen
import WBTradeScreen


def toggleSetNoScreens():
    global g_bIsScreenActive
    print("SCREEN OFF")
    g_bIsScreenActive = -1


def toggleSetScreenOn(argsList):
    global g_bIsScreenActive
    print("%s SCREEN TURNED ON" % (argsList[0],))
    g_bIsScreenActive = argsList[0]


# diplomacyScreen = CvDiplomacy.CvDiplomacy()

mainInterface = CvMainInterface.CvMainInterface()


def showMainInterface():
    mainInterface.interfaceScreen()


def reinitMainInterface():
    mainInterface.initState()


def numPlotListButtons():
    return mainInterface.numPlotListButtons()


techChooser = CvTechChooser.CvTechChooser()


def showTechChooser():
    if CyGame().getActivePlayer() > -1:
        techChooser.interfaceScreen()


hallOfFameScreen = CvHallOfFameScreen.CvHallOfFameScreen(HALL_OF_FAME)


def showHallOfFame(argsList):
    hallOfFameScreen.interfaceScreen(argsList[0])


civicScreen = CvCivicsScreen.CvCivicsScreen()


def showCivicsScreen():
    if CyGame().getActivePlayer() > -1:
        civicScreen.interfaceScreen()


religionScreen = CvReligionScreen.CvReligionScreen()


def showReligionScreen():
    if CyGame().getActivePlayer() > -1:
        religionScreen.interfaceScreen()


corporationScreen = CvCorporationScreen.CvCorporationScreen()


def showCorporationScreen():
    if CyGame().getActivePlayer() > -1:
        corporationScreen.interfaceScreen()


optionsScreen = CvOptionsScreen.CvOptionsScreen()


def showOptionsScreen():
    optionsScreen.interfaceScreen()


foreignAdvisor = CvExoticForeignAdvisor.CvExoticForeignAdvisor()


def showForeignAdvisorScreen(argsList):
    if CyGame().getActivePlayer() > -1:
        foreignAdvisor.interfaceScreen(argsList[0])


# BUG - Finance Advisor - start
financeAdvisor = None


def createFinanceAdvisor():
    """Creates the correct Finance Advisor based on an option."""
    global financeAdvisor
    if financeAdvisor is None:
        if AdvisorOpt.isBugFinanceAdvisor():
            import BugFinanceAdvisor

            financeAdvisor = BugFinanceAdvisor.BugFinanceAdvisor()
        else:
            import CvFinanceAdvisor

            financeAdvisor = CvFinanceAdvisor.CvFinanceAdvisor()
        HandleInputMap[FINANCE_ADVISOR] = financeAdvisor


# BUG - Finance Advisor - end


def showFinanceAdvisor():
    if CyGame().getActivePlayer() > -1:
        financeAdvisor.interfaceScreen()


# BUG - CustDomAdv - start
domesticAdvisor = None


def createDomesticAdvisor():
    """Creates the correct Domestic Advisor based on an option."""
    global domesticAdvisor
    if domesticAdvisor is None:
        if CustDomAdvOpt.isEnabled():
            import CvCustomizableDomesticAdvisor

            domesticAdvisor = CvCustomizableDomesticAdvisor.CvCustomizableDomesticAdvisor()
        else:
            import CvDomesticAdvisor

            domesticAdvisor = CvDomesticAdvisor.CvDomesticAdvisor()
        HandleInputMap[DOMESTIC_ADVISOR] = domesticAdvisor


# BUG - CustDomAdv - end


def showDomesticAdvisor(argsList):
    if CyGame().getActivePlayer() > -1:
        domesticAdvisor.interfaceScreen()


# BUG - Military Advisor - start
militaryAdvisor = None


def createMilitaryAdvisor():
    """Creates the correct Military Advisor based on an option."""
    global militaryAdvisor
    if militaryAdvisor is None:
        if AdvisorOpt.isBUG_MA():
            import CvBUGMilitaryAdvisor

            militaryAdvisor = CvBUGMilitaryAdvisor.CvMilitaryAdvisor(MILITARY_ADVISOR)
        else:
            import CvMilitaryAdvisor

            militaryAdvisor = CvMilitaryAdvisor.CvMilitaryAdvisor(MILITARY_ADVISOR)
        HandleInputMap[MILITARY_ADVISOR] = militaryAdvisor


def showMilitaryAdvisor():
    if CyGame().getActivePlayer() > -1:
        if AdvisorOpt.isBUG_MA():
            # TODO: move to CvBUGMilitaryAdvisor.interfaceScreen()
            militaryAdvisor.IconGridActive = False
        militaryAdvisor.interfaceScreen()


# BUG - Military Advisor - end

espionageAdvisor = CvEspionageAdvisor.CvEspionageAdvisor()


def showEspionageAdvisor():
    if CyGame().getActivePlayer() > -1:
        espionageAdvisor.interfaceScreen()


dawnOfMan = CvDawnOfMan.CvDawnOfMan(DAWN_OF_MAN)


def showDawnOfMan(argsList):
    dawnOfMan.interfaceScreen()


introMovie = CvIntroMovieScreen.CvIntroMovieScreen()


def showIntroMovie(argsList):
    introMovie.interfaceScreen()


victoryMovie = CvVictoryMovieScreen.CvVictoryMovieScreen()


def showVictoryMovie(argsList):
    victoryMovie.interfaceScreen(argsList[0])


wonderMovie = CvWonderMovieScreen.CvWonderMovieScreen()


def showWonderMovie(argsList):
    wonderMovie.interfaceScreen(argsList[0], argsList[1], argsList[2])


eraMovie = CvEraMovieScreen.CvEraMovieScreen()


def showEraMovie(argsList):
    eraMovie.interfaceScreen(argsList[0])


spaceShip = CvSpaceShipScreen.CvSpaceShipScreen()


def showSpaceShip(argsList):
    showVictoryScreen(argsList)


replayScreen = CvReplayScreen.CvReplayScreen(REPLAY_SCREEN)


def showReplay(argsList):
    if argsList[0] > -1:
        CyGame().saveReplay(argsList[0])
    replayScreen.showScreen(argsList[4])


danQuayleScreen = CvDanQuayle.CvDanQuayle()


def showDanQuayleScreen(argsList):
    danQuayleScreen.interfaceScreen()


unVictoryScreen = CvUnVictoryScreen.CvUnVictoryScreen()


def showUnVictoryScreen(argsList):
    unVictoryScreen.interfaceScreen()


topCivs = CvTopCivs.CvTopCivs()


def showTopCivs():
    topCivs.showScreen()


infoScreen = CvInfoScreen.CvInfoScreen(INFO_SCREEN)


def showInfoScreen(argsList):
    if CyGame().getActivePlayer() > -1:
        iTabID = argsList[0]
        iEndGame = argsList[1]
        infoScreen.showScreen(-1, iTabID, iEndGame)


debugInfoScreen = CvDebugInfoScreen.CvDebugInfoScreen()


def showDebugInfoScreen():
    debugInfoScreen.interfaceScreen()


# BUG - Tech Splash Screen - start
techSplashScreen = None


def createTechSplash():
    """Creates the correct Tech Splash Screen based on an option."""
    global techSplashScreen
    if techSplashScreen is None:
        if TechWindowOpt.isDetailedView():
            import TechWindow

            techSplashScreen = TechWindow.CvTechSplashScreen(TECH_SPLASH)
        elif TechWindowOpt.isWideView():
            import TechWindowWide

            techSplashScreen = TechWindowWide.CvTechSplashScreen(TECH_SPLASH)
        else:
            import CvTechSplashScreen

            techSplashScreen = CvTechSplashScreen.CvTechSplashScreen(TECH_SPLASH)
    HandleInputMap[TECH_SPLASH] = techSplashScreen


def deleteTechSplash(option=None, value=None):
    global techSplashScreen
    techSplashScreen = None
    if TECH_SPLASH in HandleInputMap:
        del HandleInputMap[TECH_SPLASH]


def showTechSplash(argsList):
    if techSplashScreen is None:
        createTechSplash()
    techSplashScreen.interfaceScreen(argsList[0])


# BUG - Tech Splash Screen - end

victoryScreen = CvVictoryScreen.CvVictoryScreen(VICTORY_SCREEN)


def showVictoryScreen():
    if CyGame().getActivePlayer() > -1:
        victoryScreen.interfaceScreen()


# < Mercenaries Mod Start >
mercenaryManager = CvMercenaryManager.CvMercenaryManager(MERCENARY_MANAGER)


def showMercenaryManager():
    mercenaryManager.interfaceScreen()
    # < Mercenaries Mod End >


# Absinthe: stability overlay
def toggleStabilityOverlay():
    _toggleStabilityOverlay()


def getStability(argsList):
    return player(argsList[0]).getStability()


def countAchievedGoals(argsList):
    return _countAchievedGoals(argsList[0])


### PEDIA

pediaMainScreen = None


def createCivilopedia():
    """Creates the correct Civilopedia based on an option."""
    global pediaMainScreen
    if pediaMainScreen is None:
        pediaMainScreen = CvPediaMain.CvPediaMain()
        HandleInputMap.update(
            {
                PEDIA_MAIN: pediaMainScreen,
                PEDIA_TECH: pediaMainScreen,
                PEDIA_UNIT: pediaMainScreen,
                PEDIA_BUILDING: pediaMainScreen,
                PEDIA_PROMOTION: pediaMainScreen,
                PEDIA_PROJECT: pediaMainScreen,
                PEDIA_UNIT_CHART: pediaMainScreen,
                PEDIA_BONUS: pediaMainScreen,
                PEDIA_IMPROVEMENT: pediaMainScreen,
                PEDIA_TERRAIN: pediaMainScreen,
                PEDIA_FEATURE: pediaMainScreen,
                PEDIA_CIVIC: pediaMainScreen,
                PEDIA_CIVILIZATION: pediaMainScreen,
                PEDIA_LEADER: pediaMainScreen,
                PEDIA_RELIGION: pediaMainScreen,
                PEDIA_CORPORATION: pediaMainScreen,
                PEDIA_HISTORY: pediaMainScreen,
            }
        )
        global HandleNavigationMap
        HandleNavigationMap = {
            MAIN_INTERFACE: mainInterface,
            PEDIA_MAIN: pediaMainScreen,
            PEDIA_TECH: pediaMainScreen,
            PEDIA_UNIT: pediaMainScreen,
            PEDIA_BUILDING: pediaMainScreen,
            PEDIA_PROMOTION: pediaMainScreen,
            PEDIA_PROJECT: pediaMainScreen,
            PEDIA_UNIT_CHART: pediaMainScreen,
            PEDIA_BONUS: pediaMainScreen,
            PEDIA_IMPROVEMENT: pediaMainScreen,
            PEDIA_TERRAIN: pediaMainScreen,
            PEDIA_FEATURE: pediaMainScreen,
            PEDIA_CIVIC: pediaMainScreen,
            PEDIA_CIVILIZATION: pediaMainScreen,
            PEDIA_LEADER: pediaMainScreen,
            PEDIA_HISTORY: pediaMainScreen,
            PEDIA_RELIGION: pediaMainScreen,
            PEDIA_CORPORATION: pediaMainScreen,
        }


def linkToPedia(argsList):
    pediaMainScreen.link(argsList[0])


def pediaShow():
    createCivilopedia()
    return pediaMainScreen.pediaShow()


def pediaBack():
    return pediaMainScreen.back()


def pediaForward():
    return pediaMainScreen.forward()


def pediaMain(argsList):
    pediaMainScreen.pediaJump(PEDIA_MAIN, argsList[0], True)


def pediaJumpToTech(argsList):
    pediaMainScreen.pediaJump(PEDIA_TECH, argsList[0], True)


def pediaJumpToUnit(argsList):
    pediaMainScreen.pediaJump(PEDIA_UNIT, argsList[0], True)


def pediaJumpToBuilding(argsList):
    pediaMainScreen.pediaJump(PEDIA_BUILDING, argsList[0], True)


def pediaJumpToProject(argsList):
    pediaMainScreen.pediaJump(PEDIA_PROJECT, argsList[0], True)


def pediaJumpToReligion(argsList):
    pediaMainScreen.pediaJump(PEDIA_RELIGION, argsList[0], True)


def pediaJumpToCorporation(argsList):
    pediaMainScreen.pediaJump(PEDIA_CORPORATION, argsList[0], True)


def pediaJumpToPromotion(argsList):
    pediaMainScreen.pediaJump(PEDIA_PROMOTION, argsList[0], True)


def pediaJumpToUnitChart(argsList):
    pediaMainScreen.pediaJump(PEDIA_UNIT_CHART, argsList[0], True)


def pediaJumpToBonus(argsList):
    pediaMainScreen.pediaJump(PEDIA_BONUS, argsList[0], True)


def pediaJumpToTerrain(argsList):
    pediaMainScreen.pediaJump(PEDIA_TERRAIN, argsList[0], True)


def pediaJumpToFeature(argsList):
    pediaMainScreen.pediaJump(PEDIA_FEATURE, argsList[0], True)


def pediaJumpToImprovement(argsList):
    pediaMainScreen.pediaJump(PEDIA_IMPROVEMENT, argsList[0], True)


def pediaJumpToCivic(argsList):
    pediaMainScreen.pediaJump(PEDIA_CIVIC, argsList[0], True)


def pediaJumpToCiv(argsList):
    pediaMainScreen.pediaJump(PEDIA_CIVILIZATION, argsList[0], True)


def pediaJumpToLeader(argsList):
    pediaMainScreen.pediaJump(PEDIA_LEADER, argsList[0], True)


def pediaJumpToSpecialist(argsList):
    pediaMainScreen.pediaJump(PEDIA_SPECIALIST, argsList[0], True)


def pediaShowHistorical(argsList):
    iEntryId = pediaMainScreen.pediaHistorical.getIdFromEntryInfo(argsList[0], argsList[1])
    pediaMainScreen.pediaJump(PEDIA_HISTORY, iEntryId, True)
    return


#################################################
## Worldbuilder
#################################################
worldBuilderScreen = CvPlatyBuilderScreen.CvWorldBuilderScreen()


def getWorldBuilderScreen():
    return worldBuilderScreen


def showWorldBuilderScreen():
    worldBuilderScreen.interfaceScreen()


def hideWorldBuilderScreen():
    worldBuilderScreen.killScreen()


def WorldBuilderToggleUnitEditCB():
    worldBuilderScreen.toggleUnitEditCB()


def WorldBuilderEraseCB():
    worldBuilderScreen.eraseCB()


def WorldBuilderLandmarkCB():
    worldBuilderScreen.landmarkModeCB()


def WorldBuilderExitCB():
    worldBuilderScreen.Exit()


def WorldBuilderToggleCityEditCB():
    worldBuilderScreen.toggleCityEditCB()


def WorldBuilderNormalPlayerTabModeCB():
    worldBuilderScreen.normalPlayerTabModeCB()


def WorldBuilderNormalMapTabModeCB():
    worldBuilderScreen.normalMapTabModeCB()


def WorldBuilderRevealTabModeCB():
    worldBuilderScreen.revealTabModeCB()


def WorldBuilderDiplomacyModeCB():
    WBDiplomacyScreen.WBDiplomacyScreen().interfaceScreen(CyGame().getActivePlayer(), False)


def WorldBuilderRevealAllCB():
    worldBuilderScreen.revealAll(True)


def WorldBuilderUnRevealAllCB():
    worldBuilderScreen.revealAll(False)


def WorldBuilderGetHighlightPlot(argsList):
    return worldBuilderScreen.getHighlightPlot(argsList)


def WorldBuilderOnAdvancedStartBrushSelected(argsList):
    iList, iIndex, iTab = argsList
    print("WB Advanced Start brush selected, iList=%d, iIndex=%d, type=%d" % (iList, iIndex, iTab))
    if iTab == worldBuilderScreen.m_iASTechTabID:
        showTechChooser()
    elif (
        iTab == worldBuilderScreen.m_iASCityTabID
        and iList == worldBuilderScreen.m_iASAutomateListID
    ):
        CyMessageControl().sendAdvancedStartAction(
            AdvancedStartActionTypes.ADVANCEDSTARTACTION_AUTOMATE,
            worldBuilderScreen.m_iCurrentPlayer,
            -1,
            -1,
            -1,
            True,
        )

    if worldBuilderScreen.setCurrentAdvancedStartIndex(iIndex):
        if worldBuilderScreen.setCurrentAdvancedStartList(iList):
            return 1
    return 0


def WorldBuilderGetASUnitTabID():
    return worldBuilderScreen.getASUnitTabID()


def WorldBuilderGetASCityTabID():
    return worldBuilderScreen.getASCityTabID()


def WorldBuilderGetASCityListID():
    return worldBuilderScreen.getASCityListID()


def WorldBuilderGetASBuildingsListID():
    return worldBuilderScreen.getASBuildingsListID()


def WorldBuilderGetASAutomateListID():
    return worldBuilderScreen.getASAutomateListID()


def WorldBuilderGetASImprovementsTabID():
    return worldBuilderScreen.getASImprovementsTabID()


def WorldBuilderGetASRoutesListID():
    return worldBuilderScreen.getASRoutesListID()


def WorldBuilderGetASImprovementsListID():
    return worldBuilderScreen.getASImprovementsListID()


def WorldBuilderGetASVisibilityTabID():
    return worldBuilderScreen.getASVisibilityTabID()


def WorldBuilderGetASTechTabID():
    return worldBuilderScreen.getASTechTabID()


#################################################
## Utility Functions (can be overridden by CvScreenUtilsInterface
#################################################


def movieDone(argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().movieDone(argsList):
        return

    if argsList[0] == INTRO_MOVIE_SCREEN:
        introMovie.hideScreen()

    if argsList[0] == VICTORY_MOVIE_SCREEN:
        victoryMovie.hideScreen()


def leftMouseDown(argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().leftMouseDown(argsList):
        return

    if argsList[0] == WORLDBUILDER_SCREEN:
        worldBuilderScreen.leftMouseDown(argsList[1:])
        return 1
    return 0


def rightMouseDown(argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().rightMouseDown(argsList):
        return

    if argsList[0] == WORLDBUILDER_SCREEN:
        worldBuilderScreen.rightMouseDown(argsList)
        return 1
    return 0


def mouseOverPlot(argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().mouseOverPlot(argsList):
        return

    if WORLDBUILDER_SCREEN == argsList[0]:
        worldBuilderScreen.mouseOverPlot(argsList)


def handleInput(argsList):
    "handle input is called when a screen is up"
    inputClass = PyScreenInput.ScreenInput(argsList)

    # allows overides for mods
    ret = CvScreenUtilsInterface.getScreenUtils().handleInput(
        (inputClass.getPythonFile(), inputClass)
    )

    # get the screen that is active from the HandleInputMap Dictionary
    screen = HandleInputMap.get(inputClass.getPythonFile())

    # call handle input on that screen
    if screen and not ret:
        return screen.handleInput(inputClass)
    return 0


def update(argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().update(argsList):
        return

    if HandleInputMap.has_key(argsList[0]):
        screen = HandleInputMap.get(argsList[0])
        screen.update(argsList[1])


def onClose(argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().onClose(argsList):
        return

    if HandleCloseMap.has_key(argsList[0]):
        screen = HandleCloseMap.get(argsList[0])
        screen.onClose()


# Forced screen update
def forceScreenUpdate(argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().forceScreenUpdate(argsList):
        return

    # Tech chooser update (forced from net message)
    if argsList[0] == TECH_CHOOSER:
        techChooser.updateTechRecords(False)
    # Main interface Screen
    elif argsList[0] == MAIN_INTERFACE:
        mainInterface.updateScreen()
    # world builder Screen
    elif argsList[0] == WORLDBUILDER_SCREEN:
        worldBuilderScreen.updateScreen()


# Forced redraw
def forceScreenRedraw(argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().forceScreenRedraw(argsList):
        return

    # Main Interface Screen
    if argsList[0] == MAIN_INTERFACE:
        mainInterface.redraw()
    elif argsList[0] == TECH_CHOOSER:
        techChooser.updateTechRecords(true)


def minimapClicked(argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().minimapClicked(argsList):
        return

    if MILITARY_ADVISOR == argsList[0]:
        militaryAdvisor.minimapClicked()
    return


############################################################################
## Misc Functions
############################################################################


def handleBack(screens):
    for iScreen in screens:
        if HandleNavigationMap.has_key(iScreen):
            screen = HandleNavigationMap.get(iScreen)
            screen.back()
    print("Mouse BACK")
    return 0


def handleForward(screens):
    for iScreen in screens:
        if HandleNavigationMap.has_key(iScreen):
            screen = HandleNavigationMap.get(iScreen)
            screen.forward()
    print("Mouse FWD")
    return 0


def refreshMilitaryAdvisor(argsList):
    if 1 == argsList[0]:
        militaryAdvisor.refreshSelectedGroup(argsList[1])
    elif 2 == argsList[0]:
        militaryAdvisor.refreshSelectedLeader(argsList[1])
    elif 3 == argsList[0]:
        militaryAdvisor.drawCombatExperience()
    elif argsList[0] <= 0:
        militaryAdvisor.refreshSelectedUnit(-argsList[0], argsList[1])


def updateMusicPath(argsList):
    szPathName = argsList[0]
    optionsScreen.updateMusicPath(szPathName)


def refreshOptionsScreen():
    optionsScreen.refreshScreen()


def cityWarningOnClickedCallback(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]
    city = (
        CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
    )
    if not city.isNone():
        if iButtonId == 0:
            if city.isProductionProcess():
                CyMessageControl().sendPushOrder(iData1, iData2, iData3, False, False, False)
            else:
                CyMessageControl().sendPushOrder(iData1, iData2, iData3, False, True, False)
        elif iButtonId == 2:
            CyInterface().selectCity(city, False)


def cityWarningOnFocusCallback(argsList):
    CyInterface().playGeneralSound("AS2D_ADVISOR_SUGGEST")
    CyInterface().lookAtCityOffset(argsList[0])
    return 0


def liberateOnClickedCallback(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]
    city = (
        CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
    )
    if not city.isNone():
        if iButtonId == 0:
            CyMessageControl().sendDoTask(
                iData1, TaskTypes.TASK_LIBERATE, 0, -1, False, False, False, False
            )
        elif iButtonId == 2:
            CyInterface().selectCity(city, False)


def colonyOnClickedCallback(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]
    city = (
        CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
    )
    if not city.isNone():
        if iButtonId == 0:
            CyMessageControl().sendEmpireSplit(
                CyGlobalContext().getGame().getActivePlayer(), city.area().getID()
            )
        elif iButtonId == 2:
            CyInterface().selectCity(city, False)


def featAccomplishedOnClickedCallback(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    if iButtonId == 1:
        if iData1 == FeatTypes.FEAT_TRADE_ROUTE:
            showDomesticAdvisor(())
        elif (iData1 >= FeatTypes.FEAT_UNITCOMBAT_ARCHER) and (iData1 <= FeatTypes.FEAT_UNIT_SPY):
            showMilitaryAdvisor()
        elif (iData1 >= FeatTypes.FEAT_COPPER_CONNECTED) and (
            iData1 <= FeatTypes.FEAT_FOOD_CONNECTED
        ):
            showForeignAdvisorScreen([0])
        elif iData1 == FeatTypes.FEAT_NATIONAL_WONDER:
            # 2 is for the wonder tab...
            showInfoScreen([2, 0])
        elif (iData1 >= FeatTypes.FEAT_POPULATION_100_THOUSAND) and (
            iData1 <= FeatTypes.FEAT_POPULATION_100_MILLION
        ):
            # 1 is for the demographics tab...
            showInfoScreen([1, 0])
        elif iData1 == FeatTypes.FEAT_CORPORATION_ENABLED:
            showCorporationScreen()


def featAccomplishedOnFocusCallback(argsList):
    iData1 = argsList[0]
    iData2 = argsList[1]
    iData3 = argsList[2]
    iData4 = argsList[3]
    szText = argsList[4]
    bOption1 = argsList[5]
    bOption2 = argsList[6]

    CyInterface().playGeneralSound("AS2D_FEAT_ACCOMPLISHED")
    if (iData1 >= FeatTypes.FEAT_UNITCOMBAT_ARCHER) and (iData1 <= FeatTypes.FEAT_FOOD_CONNECTED):
        CyInterface().lookAtCityOffset(iData2)

    return 0


#######################################################################################
## Handle Close Map
#######################################################################################
HandleCloseMap = {
    DAWN_OF_MAN: dawnOfMan,
    SPACE_SHIP_SCREEN: spaceShip,
    TECH_CHOOSER: techChooser,
    # add new screens here
}

#######################################################################################
## Handle Input Map
#######################################################################################
HandleInputMap = {
    MAIN_INTERFACE: mainInterface,
    # 					DOMESTIC_ADVISOR : domesticAdvisor,
    RELIGION_SCREEN: religionScreen,
    CORPORATION_SCREEN: corporationScreen,
    CIVICS_SCREEN: civicScreen,
    TECH_CHOOSER: techChooser,
    FOREIGN_ADVISOR: foreignAdvisor,
    # 					FINANCE_ADVISOR : financeAdvisor,
    # 					MILITARY_ADVISOR : militaryAdvisor,
    DAWN_OF_MAN: dawnOfMan,
    WONDER_MOVIE_SCREEN: wonderMovie,
    ERA_MOVIE_SCREEN: eraMovie,
    SPACE_SHIP_SCREEN: spaceShip,
    INTRO_MOVIE_SCREEN: introMovie,
    OPTIONS_SCREEN: optionsScreen,
    INFO_SCREEN: infoScreen,
    # TECH_SPLASH: techSplashScreen,
    REPLAY_SCREEN: replayScreen,
    VICTORY_SCREEN: victoryScreen,
    TOP_CIVS: topCivs,
    HALL_OF_FAME: hallOfFameScreen,
    VICTORY_MOVIE_SCREEN: victoryMovie,
    ESPIONAGE_ADVISOR: espionageAdvisor,
    DAN_QUAYLE_SCREEN: danQuayleScreen,
    # < Mercenaries Mod Start >
    MERCENARY_MANAGER: mercenaryManager,
    # < Mercenaries Mod End   >
    WORLDBUILDER_SCREEN: worldBuilderScreen,
    DEBUG_INFO_SCREEN: debugInfoScreen,
    ## World Builder ##
    WB_PLOT: WBPlotScreen.WBPlotScreen(),
    WB_EVENT: WBEventScreen.WBEventScreen(),
    WB_BUILDING: WBBuildingScreen.WBBuildingScreen(),
    WB_CITYDATA: WBCityDataScreen.WBCityDataScreen(),
    WB_CITYEDIT: WBCityEditScreen.WBCityEditScreen(worldBuilderScreen),
    WB_TECH: WBTechScreen.WBTechScreen(),
    WB_PROJECT: WBProjectScreen.WBProjectScreen(),
    WB_TEAM: WBTeamScreen.WBTeamScreen(),
    WB_PLAYER: WBPlayerScreen.WBPlayerScreen(),
    WB_UNIT: WBUnitScreen.WBUnitScreen(worldBuilderScreen),
    WB_PROMOTION: WBPromotionScreen.WBPromotionScreen(),
    WB_DIPLOMACY: WBDiplomacyScreen.WBDiplomacyScreen(),
    WB_GAMEDATA: WBGameDataScreen.WBGameDataScreen(worldBuilderScreen),
    WB_UNITLIST: WBPlayerUnits.WBPlayerUnits(),
    WB_RELIGION: WBReligionScreen.WBReligionScreen(),
    WB_CORPORATION: WBCorporationScreen.WBCorporationScreen(),
    WB_INFO: WBInfoScreen.WBInfoScreen(),
    WB_TRADE: WBTradeScreen.WBTradeScreen(),
}

#######################################################################################
## Handle Navigation Map
#######################################################################################
HandleNavigationMap = {}


# BUG - Options - start
def init():
    createDomesticAdvisor()
    createFinanceAdvisor()
    createMilitaryAdvisor()
    createCivilopedia()
    createTechSplash()


# BUG - Options - end
