from CvPythonExtensions import *
from Civilizations import (
    set_initial_contacts,
    reveal_areas,
    set_starting_techs_1200AD,
    set_starting_gold,
    set_starting_techs,
    create_starting_units_1200AD,
    create_starting_units_500AD,
    create_starting_workers,
    set_starting_diplomacy_1200AD,
    set_starting_faith,
)
from Consts import MessageData
from Core import (
    civilization,
    civilizations,
    event_popup,
    get_scenario,
    get_scenario_start_turn,
    human,
    is_major_civ,
    is_minor_civ,
    location,
    make_unit,
    make_units,
    message,
    player,
    text,
    turn,
    year,
    cities,
    plots,
)
from History import ottoman_invasion
from PyUtils import percentage, percentage_chance, rand, choice
import Provinces
from RFCUtils import (
    clearPlague,
    convertPlotCulture,
    cultureManager,
    flipCity,
    flipUnitsInArea,
    flipUnitsInCityAfter,
    flipUnitsInCityBefore,
    flipUnitsInPlots,
    forcedInvasion,
    getLastTurnAlive,
    getPlagueCountdown,
    getUniqueBuilding,
    goodPlots,
    innerSpawn,
    killAllUnitsInArea,
    killUnitsInPlots,
    outerInvasion,
    ownedCityPlots,
    setPlagueCountdown,
    spreadMajorCulture,
    squareSearch,
    updateMinorTechs,
)
import Religions
from Collapse import collapseByBarbs, collapseGeneric, collapseMotherland
from Secession import secession, secessionCloseCollapse
from Resurrection import resurectCiv, resurrection
import Victory
from StoredData import data
import Crusades

from MiscData import PLAGUE_IMMUNITY
from CoreTypes import (
    Area,
    AreaType,
    Building,
    Civ,
    LeaderType,
    PlayerType,
    Scenario,
    Terrain,
    Feature,
    Improvement,
    Unit,
)
from Wonders import leaning_tower_effect
from Events import handler

gc = CyGlobalContext()

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 66
iRebellionDelay = 15
iEscapePeriod = 30


@handler("GameStart")
def setup():
    setEarlyLeaders()
    setupRespawnTurns()

    iHuman = human()
    if get_scenario() == Scenario.i500AD:
        create_starting_units_500AD()
        for civ in civilizations().majors().filter(lambda c: c.date.birth == year(500)).ids():
            reveal_areas(civ)
            set_initial_contacts(civ)

    else:
        create_starting_units_1200AD()
        for civ in (
            civilizations()
            .main()
            .filter(lambda c: c.date.birth < get_scenario_start_turn(Scenario.i1200AD))
            .ids()
        ):
            reveal_areas(civ)
            set_initial_contacts(civ, False)
            # Temporarily all civs get the same starting techs as Aragon
            set_starting_techs_1200AD(civ)

        set_starting_faith()
        set_starting_diplomacy_1200AD()
        leaning_tower_effect()
        Religions.spread1200ADJews()  # Spread Jews to some random cities
        Victory.set1200UHVDone(iHuman)
        # Temporarily all civs get the same starting techs as Aragon
        set_starting_techs_1200AD(Civ.POPE)
        Crusades.do1200ADCrusades()

    set_starting_gold()
    set_war_on_spawn()


@handler("cityAcquired")
def spread_culture_to_new_acquired_city(owner, player, city, bConquest, bTrade):
    # Absinthe: Spread some culture to the newly acquired city, this is for nearby indy cities,
    # so should be applied in all cases (conquest, flip, trade)
    if player < civilizations().majors().len():
        spreadMajorCulture(player, city.getX(), city.getY())


def set_war_on_spawn():
    for civ in civilizations():
        wars = civ.scenario.get("wars")
        if wars is not None:
            for other, war_threshold in wars.items():
                if percentage_chance(war_threshold, strict=True) and not civ.at_war(other):
                    civ.set_war(other)


def setSpecialRespawnTurn(iCiv, iNewValue):
    data.lSpecialRespawnTurn[iCiv] = iNewValue


def setupRespawnTurns():
    """Uniform spawns within +/- 10 turns of desired turn."""
    for iCiv in civilizations().majors().ids():
        setSpecialRespawnTurn(
            iCiv, civilization(iCiv).date.respawning + (rand(21) - 10) + (rand(21) - 10)
        )


def setEarlyLeaders():
    for civ in civilizations().majors().ai():
        if civ.leaders[LeaderType.EARLY] != civ.leaders[LeaderType.PRIMARY]:
            leader = civ.leaders[LeaderType.EARLY]
            civ.player.setLeader(leader)


def getNewCiv():
    return data.iNewCiv


def setNewCiv(iNewValue):
    data.iNewCiv = iNewValue


def getNewCivFlip():
    return data.iNewCivFlip


def setNewCivFlip(iNewValue):
    data.iNewCivFlip = iNewValue


def getOldCivFlip():
    return data.iOldCivFlip


def setOldCivFlip(iNewValue):
    data.iOldCivFlip = iNewValue


def getTempTopLeft():
    return data.iTempTopLeft


def setTempTopLeft(tNewValue):
    data.iTempTopLeft = tNewValue


def getTempBottomRight():
    return data.iTempBottomRight


def setTempBottomRight(tNewValue):
    data.iTempBottomRight = tNewValue


def getSpawnWar():
    return data.iSpawnWar


def setSpawnWar(iNewValue):
    data.iSpawnWar = iNewValue


def getAlreadySwitched():
    return data.bAlreadySwitched


def setAlreadySwitched(bNewValue):
    data.bAlreadySwitched = bNewValue


def getSpawnDelay(iCiv):
    return data.lSpawnDelay[iCiv]


def setSpawnDelay(iCiv, iNewValue):
    data.lSpawnDelay[iCiv] = iNewValue


def getFlipsDelay(iCiv):
    return data.lFlipsDelay[iCiv]


def setFlipsDelay(iCiv, iNewValue):
    data.lFlipsDelay[iCiv] = iNewValue


def getBetrayalTurns():
    return data.iBetrayalTurns


def setBetrayalTurns(iNewValue):
    data.iBetrayalTurns = iNewValue


def getRebelCiv():
    return data.iRebelCiv


def getRebelCities():
    return data.lRebelCities


def getRebelSuppress():
    return data.lRebelSuppress


def setRebelSuppress(lSuppressList):
    data.lRebelSuppress = lSuppressList


def getTempFlippingCity():
    return data.iTempFlippingCity


def setTempFlippingCity(tNewValue):
    data.iTempFlippingCity = tNewValue


def getCheatersCheck(i):
    return data.lCheatersCheck[i]


def setCheatersCheck(i, iNewValue):
    data.lCheatersCheck[i] = iNewValue


def getDeleteMode(i):
    return data.lDeleteMode[i]


def setDeleteMode(i, iNewValue):
    data.lDeleteMode[i] = iNewValue


def newCivPopup(iCiv):
    event_popup(
        7614,
        text("TXT_KEY_NEWCIV_TITLE"),
        text("TXT_KEY_NEWCIV_MESSAGE", player(iCiv).getCivilizationAdjectiveKey()),
        [text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO")],
    )
    setNewCiv(iCiv)


def eventApply7614(popupReturn):
    if popupReturn.getButtonClicked() == 0:  # 1st button
        iOldHandicap = gc.getActivePlayer().getHandicapType()
        iNewCiv = getNewCiv()
        Victory.switchUHV(iNewCiv, human())
        gc.getActivePlayer().setHandicapType(gc.getPlayer(iNewCiv).getHandicapType())
        gc.getGame().setActivePlayer(iNewCiv, False)
        gc.getPlayer(iNewCiv).setHandicapType(iOldHandicap)
        for iMaster in civilizations().majors().ids():
            if gc.getTeam(gc.getPlayer(iNewCiv).getTeam()).isVassal(iMaster):
                gc.getTeam(gc.getPlayer(iNewCiv).getTeam()).setVassal(iMaster, False, False)
        setAlreadySwitched(True)
        gc.getPlayer(iNewCiv).setPlayable(True)


def flipPopup(iNewCiv, tTopLeft, tBottomRight):
    iHuman = human()
    flipText = text("TXT_KEY_FLIPMESSAGE1")

    for city in (
        plots()
        .rectangle(tTopLeft, tBottomRight)
        .add(civilization(iNewCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES])
        .cities()
        .filter(lambda c: c.getOwner() == iHuman and not c.isCapital())
        .entities()
    ):
        flipText += city.getName() + "\n"
    flipText += text("TXT_KEY_FLIPMESSAGE2")

    event_popup(
        7615,
        text("TXT_KEY_NEWCIV_TITLE"),
        flipText,
        [text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO")],
    )
    setNewCivFlip(iNewCiv)
    setOldCivFlip(iHuman)
    setTempTopLeft(tTopLeft)
    setTempBottomRight(tBottomRight)


def eventApply7615(popupReturn):
    iHuman = human()
    tTopLeft = getTempTopLeft()
    tBottomRight = getTempBottomRight()
    iNewCivFlip = getNewCivFlip()

    humanCityList = []

    for city in (
        plots()
        .rectangle(tTopLeft, tBottomRight)
        .add(civilization(iNewCivFlip).location.area[AreaType.CORE][Area.ADDITIONAL_TILES])
        .cities()
        .filter(lambda c: c.getOwner() == iHuman and not c.isCapital())
        .entities()
    ):
        humanCityList.append(city)

    if popupReturn.getButtonClicked() == 0:  # 1st button
        message(iHuman, text("TXT_KEY_FLIP_AGREED"), force=True, color=MessageData.GREEN)

        if humanCityList:
            for city in humanCityList:
                tCity = (city.getX(), city.getY())
                cultureManager(tCity, 100, iNewCivFlip, iHuman, False, False, False)
                flipUnitsInCityBefore(tCity, iNewCivFlip, iHuman)
                setTempFlippingCity(tCity)
                flipCity(tCity, 0, 0, iNewCivFlip, [iHuman])
                flipUnitsInCityAfter(tCity, iNewCivFlip)

        # same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
        for plot in plots().rectangle(tTopLeft, tBottomRight).entities():
            iNumUnitsInAPlot = plot.getNumUnits()
            if iNumUnitsInAPlot > 0:
                for i in range(iNumUnitsInAPlot):
                    unit = plot.getUnit(i)
                    if unit.getOwner() == iHuman:
                        rndNum = percentage()
                        if rndNum >= iBetrayalThreshold:
                            if unit.getDomainType() == DomainTypes.DOMAIN_SEA:  # land unit
                                iUnitType = unit.getUnitType()
                                unit.kill(False, iNewCivFlip)
                                make_unit(iNewCivFlip, iUnitType, location(plot))
                                i = i - 1

        if getCheatersCheck(0) == 0:
            setCheatersCheck(0, iCheatersPeriod)
            setCheatersCheck(1, getNewCivFlip())

    elif popupReturn.getButtonClicked() == 1:  # 2nd button
        message(iHuman, text("TXT_KEY_FLIP_REFUSED"), force=True, color=MessageData.RED)

        if humanCityList:
            for city in humanCityList:
                pCurrent = gc.getMap().plot(city.getX(), city.getY())
                oldCulture = pCurrent.getCulture(iHuman)
                # Absinthe: changeCulture instead of setCulture, otherwise previous culture will be lost
                pCurrent.changeCulture(iNewCivFlip, oldCulture / 2, True)
                pCurrent.setCulture(iHuman, oldCulture / 2, True)
                iWar = getSpawnWar() + 1
                setSpawnWar(iWar)
                if getSpawnWar() == 1:
                    # safety check - don't want to use canDeclareWar, as here we want to always declare war
                    if not gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).isAtWar(iHuman):
                        gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).declareWar(
                            iHuman, False, -1
                        )
                    setBetrayalTurns(iBetrayalPeriod)
                    initBetrayal()


# resurrection when some human controlled cities are also included
def eventApply7622(popupReturn):
    iHuman = human()
    iRebelCiv = getRebelCiv()
    iChoice = popupReturn.getButtonClicked()
    iHumanCity = 0
    lCityList = getRebelCities()
    for (x, y) in lCityList:
        iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
        if iOwner == iHuman:
            iHumanCity += 1

    if iChoice == 1:
        lList = getRebelSuppress()
        lList[iHuman] = 2  # let go + war
        setRebelSuppress(lList)
    elif iChoice == 2:
        if percentage_chance(40, strict=True):
            lCityList = getRebelCities()
            for (x, y) in lCityList:
                pCity = gc.getMap().plot(x, y).getPlotCity()
                if pCity.getOwner() == iHuman:
                    pCity.changeOccupationTimer(2)
                    pCity.changeHurryAngerTimer(10)
            lList = getRebelSuppress()
            lList[iHuman] = 3  # keep cities + war
            setRebelSuppress(lList)
        else:
            lList = getRebelSuppress()
            lList[iHuman] = 4  # let go + war
            setRebelSuppress(lList)
    elif iChoice == 3:
        iLoyalPrice = min((10 * gc.getPlayer(iHuman).getGold()) / 100, 50 * iHumanCity)
        gc.getPlayer(iHuman).setGold(gc.getPlayer(iHuman).getGold() - iLoyalPrice)
        if percentage_chance(iLoyalPrice / iHumanCity, strict=True):
            lList = getRebelSuppress()
            lList[iHuman] = 1  # keep + no war
            setRebelSuppress(lList)
        else:
            lList = getRebelSuppress()
            lList[iHuman] = 4  # let go + war
            setRebelSuppress(lList)
    elif iChoice == 4:
        iLoyalPrice = min((10 * gc.getPlayer(iHuman).getGold()) / 100, 50 * iHumanCity)
        gc.getPlayer(iHuman).setGold(gc.getPlayer(iHuman).getGold() - iLoyalPrice)
        if percentage_chance(iLoyalPrice / iHumanCity + 40, strict=True):
            lCityList = getRebelCities()
            for (x, y) in lCityList:
                pCity = gc.getMap().plot(x, y).getPlotCity()
                if pCity.getOwner() == iHuman:
                    pCity.changeOccupationTimer(2)
                    pCity.changeHurryAngerTimer(10)
            lList = getRebelSuppress()
            lList[iHuman] = 3  # keep + war
            setRebelSuppress(lList)
        else:
            lList = getRebelSuppress()
            lList[iHuman] = 2  # let go + war
            setRebelSuppress(lList)
    resurectCiv(getRebelCiv())


@handler("cityBuilt")
def onCityBuilt(pCity):
    iPlayer = pCity.getOwner()
    tCity = (pCity.getX(), pCity.getY())
    Provinces.onCityBuilt(iPlayer, pCity.getX(), pCity.getY())
    # Absinthe: We can add free buildings for new cities here
    # 			Note that it will add the building every time a city is founded on the plot, not just on the first time
    # 			Venice (56, 35), Augsburg (55, 41), Porto (23, 31), Prague (60, 44), Riga (74, 58), Perekop (87, 36)
    # 			London (41, 52), Novgorod (80, 62) currently has preplaced fort on the map instead
    if tCity in [(56, 35), (55, 41), (23, 31), (60, 44), (74, 58), (87, 36)]:
        pCity.setHasRealBuilding(getUniqueBuilding(iPlayer, Building.WALLS), True)
    elif tCity == (75, 53):  # Vilnius - important for AI Lithuania against Prussia
        if not gc.getPlayer(Civ.LITHUANIA).isHuman():
            pCity.setHasRealBuilding(getUniqueBuilding(iPlayer, Building.WALLS), True)


@handler("BeginGameTurn")
def checkTurn(iGameTurn):
    # Trigger betrayal mode
    if getBetrayalTurns() > 0:
        initBetrayal()

    if getCheatersCheck(0) > 0:
        teamPlayer = gc.getTeam(gc.getPlayer(human()).getTeam())
        if teamPlayer.isAtWar(getCheatersCheck(1)):
            initMinorBetrayal(getCheatersCheck(1))
            setCheatersCheck(0, 0)
            setCheatersCheck(1, -1)
        else:
            setCheatersCheck(0, getCheatersCheck(0) - 1)

    if iGameTurn % 20 == 0:
        for civ in civilizations().independents().alive():
            updateMinorTechs(civ.id, Civ.BARBARIAN)

    # Absinthe: checking the spawn dates
    for iLoopCiv in civilizations().majors().ids():
        if (
            civilization(iLoopCiv).date.birth != 0
            and iGameTurn >= civilization(iLoopCiv).date.birth - 2
            and iGameTurn <= civilization(iLoopCiv).date.birth + 4
        ):
            initBirth(iGameTurn, civilization(iLoopCiv).date.birth, iLoopCiv)

    # Fragment minor civs:
    # 3Miro: Shuffle cities between Indies and Barbs to make sure there is no big Independent nation
    if iGameTurn >= 20:
        if iGameTurn % 15 == 6:
            fragmentIndependents()
        if iGameTurn % 30 == 12:
            fragmentBarbarians(iGameTurn)

    # Fall of civs:
    # Barb collapse: if more than 1/3 of the empire is conquered and/or held by barbs = collapse
    # Generic collapse: if 1/2 of the empire is lost in only a few turns (16 ATM) = collapse
    # Motherland collapse: if no city is in the core area and the number of cities in the normal area is less than the number of foreign cities = collapse
    # Secession: if stability is negative there is a chance (bigger chance with worse stability) for a random city to declare it's independence
    if iGameTurn >= 64 and iGameTurn % 7 == 0:  # mainly for Seljuks, Mongols, Timurids
        collapseByBarbs(iGameTurn)
    if iGameTurn >= 34 and iGameTurn % 16 == 0:
        collapseGeneric(iGameTurn)
    if iGameTurn >= 34 and iGameTurn % 9 == 7:
        collapseMotherland(iGameTurn)
    if iGameTurn > 20 and iGameTurn % 3 == 1:
        secession(iGameTurn)
    if iGameTurn > 20 and iGameTurn % 7 == 3:
        secessionCloseCollapse(iGameTurn)

    # Resurrection of civs:
    # This is one place to control the frequency of resurrection; will not be called with high iNumDeadCivs
    # Generally we want to allow Kiev, Bulgaria, Cordoba, Burgundy, Byzantium at least to be dead in late game without respawning
    # Absinthe: was 12 and 8 originally in RFCE, but we don't need that many dead civs
    iNumDeadCivs1 = 8  # 5 in vanilla RFC, 8 in warlords RFC
    iNumDeadCivs2 = 5  # 3 in vanilla RFC, 6 in warlords RFC

    iCiv = getSpecialRespawn(iGameTurn)
    if iCiv > -1:
        resurrection(iGameTurn, iCiv)
    elif (
        gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive()
        > iNumDeadCivs1
    ):
        if iGameTurn % 10 == 7:
            resurrection(iGameTurn, -1)
    elif (
        gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive()
        > iNumDeadCivs2
    ):
        if iGameTurn % 23 == 11:
            resurrection(iGameTurn, -1)

    # Absinthe: Reduce cities to towns, in order to make room for new civs
    if iGameTurn == civilization(Civ.SCOTLAND).date.birth - 3:
        # Reduce Inverness and Scone, so more freedom in where to found cities in Scotland
        reduceCity((37, 65))
        reduceCity((37, 67))
    elif iGameTurn == civilization(Civ.ENGLAND).date.birth - 3:
        # Reduce Norwich and Nottingham, so more freedom in where to found cities in England
        reduceCity((43, 55))
        reduceCity((39, 56))
    elif iGameTurn == civilization(Civ.SWEDEN).date.birth - 2:
        # Reduce Uppsala
        reduceCity((65, 66))
    # Absinthe: Reduce cities to town, if not owned by the human player
    if iGameTurn == year(1057):
        # Reduce Kairouan
        pPlot = gc.getMap().plot(43, 55)
        if pPlot.isCity():
            if pPlot.getPlotCity().getOwner() != human():
                reduceCity((43, 55))


def reduceCity(tPlot):
    # Absinthe: disappearing cities (reducing them to an improvement)
    pPlot = gc.getMap().plot(tPlot[0], tPlot[1])
    if pPlot.isCity():
        # Absinthe: apologize from the player:
        msgString = (
            text("TXT_KEY_REDUCE_CITY_1")
            + " "
            + pPlot.getPlotCity().getName()
            + " "
            + text("TXT_KEY_REDUCE_CITY_2")
        )
        message(
            pPlot.getPlotCity().getOwner(), msgString, color=MessageData.ORANGE, location=pPlot
        )

        pPlot.eraseCityDevelopment()
        pPlot.setImprovementType(Improvement.TOWN)  # Improvement Town instead of the city
        pPlot.setRouteType(0)  # Also adding a road there


def checkPlayerTurn(iGameTurn, iPlayer):
    # Absinthe & Merijn: leader switching with any number of leaders
    late_leaders = civilization(iPlayer).leaders[LeaderType.LATE]
    if late_leaders:
        for tLeader in reversed(late_leaders):
            if iGameTurn >= year(tLeader[1]):
                switchLateLeaders(iPlayer, tLeader)
                break

    # 3Miro: English cheat, the AI is utterly incompetent when it has to launch an invasion on an island
    # 			if in 1300AD Dublin is still Barbarian, it will flip to England
    if (
        iGameTurn == year(1300)
        and human() != Civ.ENGLAND
        and iPlayer == Civ.ENGLAND
        and player(Civ.ENGLAND).isAlive()
    ):
        tDublin = (32, 58)
        pPlot = gc.getMap().plot(tDublin[0], tDublin[1])
        if pPlot.isCity():
            if pPlot.getPlotCity().getOwner() == Civ.BARBARIAN:
                pDublin = pPlot.getPlotCity()
                cultureManager(tDublin, 50, Civ.ENGLAND, Civ.BARBARIAN, False, True, True)
                flipUnitsInCityBefore(tDublin, Civ.ENGLAND, Civ.BARBARIAN)
                setTempFlippingCity(tDublin)
                flipCity(
                    tDublin, 0, 0, Civ.ENGLAND, [Civ.BARBARIAN]
                )  # by trade because by conquest may raze the city
                flipUnitsInCityAfter(tDublin, Civ.ENGLAND)

    # Absinthe: Another English AI cheat, extra defenders and defensive buildings in Normandy some turns after spawn - from RFCE++
    if (
        iGameTurn == year(1066) + 3
        and human() != Civ.ENGLAND
        and iPlayer == Civ.ENGLAND
        and player(Civ.ENGLAND).isAlive()
    ):
        for city in plots().rectangle((39, 46), (45, 50)).cities().owner(Civ.ENGLAND).entities():
            make_unit(Civ.ENGLAND, Unit.GUISARME, city)
            make_unit(Civ.ENGLAND, Unit.ARBALEST, city)
            city.setHasRealBuilding(Building.WALLS, True)
            city.setHasRealBuilding(Building.CASTLE, True)


def switchLateLeaders(iPlayer, tLeader):
    iLeader, iDate, iThreshold, iEra = tLeader
    if iLeader == gc.getPlayer(iPlayer).getLeader():
        return
    if gc.getPlayer(iPlayer).getCurrentEra() >= iEra:
        iThreshold *= 2
    if (
        gc.getPlayer(iPlayer).getAnarchyTurns() != 0
        or getPlagueCountdown(iPlayer) > 0
        or player(iPlayer).getStability() <= -10
        or percentage_chance(iThreshold, strict=True)
    ):
        gc.getPlayer(iPlayer).setLeader(iLeader)

        # Absinthe: message about the leader switch for the human player
        iHuman = human()
        HumanTeam = gc.getTeam(gc.getPlayer(iHuman).getTeam())
        PlayerTeam = gc.getPlayer(iPlayer).getTeam()
        if HumanTeam.isHasMet(PlayerTeam) and player().isExisting():
            message(
                iHuman,
                text(
                    "TXT_KEY_LEADER_SWITCH",
                    gc.getPlayer(iPlayer).getName(),
                    gc.getPlayer(iPlayer).getCivilizationDescriptionKey(),
                ),
                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                color=MessageData.PURPLE,
            )


def fragmentIndependents():
    for iIndep1 in civilizations().independents().ids():
        pIndep1 = gc.getPlayer(iIndep1)
        iNumCities1 = pIndep1.getNumCities()
        for iIndep2 in civilizations().independents().ids():
            if iIndep1 == iIndep2:
                continue
            pIndep2 = gc.getPlayer(iIndep2)
            iNumCities2 = pIndep2.getNumCities()
            if abs(iNumCities1 - iNumCities2) > 5:
                if iNumCities1 > iNumCities2:
                    iBig = iIndep1
                    iSmall = iIndep2
                else:
                    iBig = iIndep2
                    iSmall = iIndep1
                iDivideCounter = 0
                iCounter = 0
                for city in cities().owner(iBig).entities():
                    iDivideCounter += 1
                    if iDivideCounter % 2 == 1:
                        tCity = (city.getX(), city.getY())
                        pCurrent = gc.getMap().plot(tCity[0], tCity[1])
                        cultureManager(tCity, 50, iSmall, iBig, False, True, True)
                        flipUnitsInCityBefore(tCity, iSmall, iBig)
                        setTempFlippingCity(tCity)
                        flipCity(
                            tCity, 0, 0, iSmall, [iBig]
                        )  # by trade because by conquest may raze the city
                        flipUnitsInCityAfter(tCity, iSmall)
                        iCounter += 1
                        if iCounter == 3:
                            break


def fragmentBarbarians(iGameTurn):
    iRndnum = rand(civilizations().majors().len())
    for j in civilizations().majors().ids():
        iDeadCiv = (j + iRndnum) % civilizations().majors().len()
        if (
            not gc.getPlayer(iDeadCiv).isAlive()
            and iGameTurn > civilization(iDeadCiv).date.birth + 50
        ):
            lCities = [
                location(city)
                for city in (
                    plots()
                    .rectangle(
                        civilization(iDeadCiv).location.area[AreaType.NORMAL][Area.TILE_MIN],
                        civilization(iDeadCiv).location.area[AreaType.NORMAL][Area.TILE_MAX],
                    )
                    .cities()
                    .owner(Civ.BARBARIAN)
                    .entities()
                )
            ]
            if len(lCities) > 5:
                iDivideCounter = 0
                for tCity in lCities:
                    iNewCiv = min(civilizations().independents().ids()) + rand(
                        max(civilizations().independents().ids())
                        - min(civilizations().independents().ids())
                        + 1
                    )
                    if iDivideCounter % 4 in [0, 1]:
                        cultureManager(tCity, 50, iNewCiv, Civ.BARBARIAN, False, True, True)
                        flipUnitsInCityBefore(tCity, iNewCiv, Civ.BARBARIAN)
                        setTempFlippingCity(tCity)
                        flipCity(
                            tCity, 0, 0, iNewCiv, [Civ.BARBARIAN]
                        )  # by trade because by conquest may raze the city
                        flipUnitsInCityAfter(tCity, iNewCiv)
                        iDivideCounter += 1
                return


def initBirth(iCurrentTurn, iBirthYear, iCiv):
    iHuman = human()
    if iCurrentTurn == iBirthYear - 1 + getSpawnDelay(iCiv) + getFlipsDelay(iCiv):
        tCapital = civilization(iCiv).location.capital
        core_tile_min = civilization(iCiv).location.area[AreaType.CORE][Area.TILE_MIN]
        core_tile_max = civilization(iCiv).location.area[AreaType.CORE][Area.TILE_MAX]
        broader_tile_min = civilization(iCiv).location.area[AreaType.BROADER][Area.TILE_MIN]
        broader_tile_max = civilization(iCiv).location.area[AreaType.BROADER][Area.TILE_MAX]
        if getFlipsDelay(iCiv) == 0:  # city hasn't already been founded

            # Absinthe: for the human player, kill all foreign units on the capital plot - this probably fixes a couple instances of the -1 turn autoplay bug
            if iCiv == iHuman:
                killPlot = gc.getMap().plot(tCapital[0], tCapital[1])
                iNumUnitsInAPlot = killPlot.getNumUnits()
                if iNumUnitsInAPlot > 0:
                    iSkippedUnit = 0
                    for i in range(iNumUnitsInAPlot):
                        unit = killPlot.getUnit(iSkippedUnit)
                        if unit.getOwner() != iCiv:
                            unit.kill(False, Civ.BARBARIAN)
                        else:
                            iSkippedUnit += 1

            # Absinthe: if the plot is owned by a civ, bDeleteEverything becomes True unless there is a human city in the 1+8 neighbour plots.
            bDeleteEverything = False
            if gc.getMap().plot(tCapital[0], tCapital[1]).isOwned():
                if iCiv == iHuman or not gc.getPlayer(iHuman).isAlive():
                    bDeleteEverything = True
                else:
                    bDeleteEverything = True
                    if plots().surrounding(tCapital).cities().owner(iHuman).entities():
                        bDeleteEverything = False

            if not gc.getMap().plot(tCapital[0], tCapital[1]).isOwned():
                birthInFreeRegion(iCiv, tCapital, core_tile_min, core_tile_max)
            elif bDeleteEverything:
                setDeleteMode(0, iCiv)
                # Absinthe: kill off units near the starting plot
                killAllUnitsInArea(
                    (tCapital[0] - 1, tCapital[1] - 1), (tCapital[0] + 1, tCapital[1] + 1)
                )
                for plot in plots().surrounding(tCapital).entities():
                    if plot.isCity():
                        plot.eraseAIDevelopment()  # new function, similar to erase but won't delete rivers, resources and features
                    for civ in civilizations().ids():
                        if iCiv != civ:
                            plot.setCulture(civ, 0, True)
                    plot.setOwner(-1)
                birthInFreeRegion(iCiv, tCapital, core_tile_min, core_tile_max)
            else:
                birthInForeignBorders(
                    iCiv,
                    core_tile_min,
                    core_tile_max,
                    broader_tile_min,
                    broader_tile_max,
                    tCapital,
                )
        else:
            birthInFreeRegion(iCiv, tCapital, core_tile_min, core_tile_max)

    # 3MiroCrusader modification. Crusaders cannot change nations.
    # Sedna17: Straight-up no switching within 40 turns of your birth
    if iCurrentTurn == iBirthYear + getSpawnDelay(iCiv):
        if (
            gc.getPlayer(iCiv).isAlive()
            and not getAlreadySwitched()
            and iCurrentTurn > civilization(iHuman).date.birth + 40
            and not gc.getPlayer(iHuman).getIsCrusader()
        ):
            newCivPopup(iCiv)


def deleteMode(iCurrentPlayer):
    iCiv = getDeleteMode(0)
    tCapital = civilization(iCiv).location.capital
    if iCurrentPlayer == iCiv:
        for plot in plots().surrounding(tCapital, radius=2).entities():
            plot.setCulture(iCiv, 300, True)
        for plot in plots().surrounding(tCapital).entities():
            convertPlotCulture(plot, iCiv, 100, True)
            if plot.getCulture(iCiv) < 3000:
                # 2000 in vanilla/warlords, cos here Portugal is choked by Spanish culture
                plot.setCulture(iCiv, 3000, True)
            plot.setOwner(iCiv)
        setDeleteMode(0, -1)
        return

    if iCurrentPlayer != iCiv - 1:
        return

    for plot in plots().surrounding(tCapital).entities():
        if plot.isOwned():
            for iLoopCiv in civilizations().ids():
                if iLoopCiv != iCiv:
                    plot.setCulture(iLoopCiv, 0, True)
            plot.setOwner(iCiv)

    # Absinthe: what's this +-11? do we really want to move all flipped units in the initial turn to the starting plot??


def birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight):
    startingPlot = gc.getMap().plot(tCapital[0], tCapital[1])
    if getFlipsDelay(iCiv) == 0:
        iFlipsDelay = getFlipsDelay(iCiv) + 2

        if iFlipsDelay > 0:
            # Absinthe: kill off units near the starting plot
            killAllUnitsInArea(
                (tCapital[0] - 1, tCapital[1] - 1), (tCapital[0] + 1, tCapital[1] + 1)
            )
            createStartingUnits(iCiv, (tCapital[0], tCapital[1]))
            reveal_areas(iCiv)
            set_initial_contacts(iCiv)
            # Absinthe: there was another mistake here with barbarian and indy unit flips...
            # 			we don't simply want to check an area based on distance from capital, as it might lead out from the actual spawn area
            # 			so we only check plots which are in the core area: in 4 distance for barb units, 2 distance for indies
            lPlotBarbFlip = []
            lPlotIndyFlip = []
            # if inside the core rectangle and extra plots, and in 4 (barb) or 2 (indy) distance from the starting plot, append to barb or indy flip zone

            lSurroundingPlots4 = [
                location(plot) for plot in plots().surrounding(tCapital, radius=4).entities()
            ]
            lSurroundingPlots2 = [
                location(plot) for plot in plots().surrounding(tCapital, radius=2).entities()
            ]
            for tPlot in (
                plots()
                .rectangle(tTopLeft, tBottomRight)
                .add(civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES])
                .apply(location)  # TODO  fix this with _keyify by default
            ):
                if tPlot in lSurroundingPlots2:
                    lPlotIndyFlip.append(tPlot)
                    lPlotBarbFlip.append(tPlot)
                elif tPlot in lSurroundingPlots4:
                    lPlotBarbFlip.append(tPlot)
            # remaining barbs in the region: killed for the human player, flipped for the AI
            if iCiv == human():
                killUnitsInPlots(lPlotBarbFlip, Civ.BARBARIAN)
            else:
                flipUnitsInPlots(lPlotBarbFlip, iCiv, Civ.BARBARIAN, True, True)
            for iIndyCiv in civilizations().independents().ids():
                # remaining independents in the region: killed for the human player, flipped for the AI
                if iCiv == human():
                    killUnitsInPlots(lPlotIndyFlip, iIndyCiv)
                else:
                    flipUnitsInPlots(lPlotIndyFlip, iCiv, iIndyCiv, True, False)
            set_starting_techs(iCiv)
            setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
            clearPlague(iCiv)
            setFlipsDelay(iCiv, iFlipsDelay)  # save

    else:  # starting units have already been placed, now the second part
        iNumAICitiesConverted, iNumHumanCitiesToConvert = convertSurroundingCities(
            iCiv, tTopLeft, tBottomRight
        )
        convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)
        if iCiv != human():
            flipUnitsInArea(
                tTopLeft, tBottomRight, iCiv, Civ.BARBARIAN, False, True
            )  # remaining barbs in the region now belong to the new civ
            flipUnitsInPlots(
                civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES],
                iCiv,
                Civ.BARBARIAN,
                False,
                True,
            )  # remaining barbs in the region now belong to the new civ
        for iIndyCiv in civilizations().independents().ids():
            if iCiv != human():
                flipUnitsInArea(
                    tTopLeft, tBottomRight, iCiv, iIndyCiv, False, False
                )  # remaining independents in the region now belong to the new civ
                flipUnitsInPlots(
                    civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES],
                    iCiv,
                    iIndyCiv,
                    False,
                    False,
                )  # remaining independents in the region now belong to the new civ
        # cover plots revealed by the catapult
        plotZero = gc.getMap().plot(32, 0)  # sync with rfcebalance module
        if plotZero.getNumUnits():
            catapult = plotZero.getUnit(0)
            catapult.kill(False, iCiv)
        gc.getMap().plot(31, 0).setRevealed(iCiv, False, True, -1)
        gc.getMap().plot(32, 0).setRevealed(iCiv, False, True, -1)
        gc.getMap().plot(33, 0).setRevealed(iCiv, False, True, -1)
        gc.getMap().plot(31, 1).setRevealed(iCiv, False, True, -1)
        gc.getMap().plot(32, 1).setRevealed(iCiv, False, True, -1)
        gc.getMap().plot(33, 1).setRevealed(iCiv, False, True, -1)

        if gc.getPlayer(iCiv).getNumCities() > 0:
            capital = gc.getPlayer(iCiv).getCapitalCity()
            create_starting_workers(iCiv, (capital.getX(), capital.getY()))
            if iCiv == Civ.OTTOMAN:
                ottoman_invasion(iCiv, (77, 23))

        if iNumHumanCitiesToConvert > 0:
            flipPopup(iCiv, tTopLeft, tBottomRight)


def birthInForeignBorders(
    iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight, tCapital
):
    iNumAICitiesConverted, iNumHumanCitiesToConvert = convertSurroundingCities(
        iCiv, tTopLeft, tBottomRight
    )
    convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)

    # now starting units must be placed
    if iNumAICitiesConverted > 0:
        # Absinthe: there is an issue that core area is not calculated correctly for flips, as the additional tiles in lExtraPlots are not checked here
        # 			so if all flipped cities are outside of the core area (they are in the "exceptions"), the civ will start without it's starting units and techs
        plotList = squareSearch(tTopLeft, tBottomRight, ownedCityPlots, iCiv)
        # Absinthe: add the exception plots
        for plot in civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES]:
            plot = gc.getMap().plot(*plot)
            if plot.getOwner() == iCiv:
                if plot.isCity():
                    plotList.append(plot)
        if plotList:
            plot = choice(plotList)
            createStartingUnits(iCiv, plot)
            reveal_areas(iCiv)
            set_initial_contacts(iCiv)
            set_starting_techs(iCiv)
            setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
            clearPlague(iCiv)
        flipUnitsInArea(
            tTopLeft, tBottomRight, iCiv, Civ.BARBARIAN, False, True
        )  # remaining barbs in the region now belong to the new civ
        flipUnitsInPlots(
            civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES],
            iCiv,
            Civ.BARBARIAN,
            False,
            True,
        )  # remaining barbs in the region now belong to the new civ
        for iIndyCiv in civilizations().independents().ids():
            flipUnitsInArea(
                tTopLeft, tBottomRight, iCiv, iIndyCiv, False, False
            )  # remaining independents in the region now belong to the new civ
            flipUnitsInPlots(
                civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES],
                iCiv,
                iIndyCiv,
                False,
                False,
            )  # remaining independents in the region now belong to the new civ

    else:
        # Absinthe: there is an issue that core area is not calculated correctly for flips, as the additional tiles in lExtraPlots are not checked here
        # 			so if all flipped cities are outside of the core area (they are in the "exceptions"), the civ will start without it's starting units and techs
        plotList = squareSearch(tTopLeft, tBottomRight, goodPlots, [])
        # Absinthe: add the exception plots
        for plot in civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES]:
            plot = gc.getMap().plot(*plot)
            if (plot.isHills() or plot.isFlatlands()) and not plot.isImpassable():
                if not plot.isUnit():
                    if plot.getTerrainType() not in [
                        Terrain.DESERT,
                        Terrain.TUNDRA,
                    ] and plot.getFeatureType() not in [
                        Feature.MARSH,
                        Feature.JUNGLE,
                    ]:
                        if plot.countTotalCulture() == 0:
                            plotList.append(plot)
        if plotList:
            plot = choice(plotList)
            createStartingUnits(iCiv, plot)
            reveal_areas(iCiv)
            set_initial_contacts(iCiv)
            set_starting_techs(iCiv)
            setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
            clearPlague(iCiv)
        else:
            plotList = squareSearch(tBroaderTopLeft, tBroaderBottomRight, goodPlots, [])
            if plotList:
                plot = choice(plotList)
                createStartingUnits(iCiv, plot)
                reveal_areas(iCiv)
                set_initial_contacts(iCiv)
                create_starting_workers(iCiv, plot)
                if iCiv == Civ.OTTOMAN:
                    ottoman_invasion(iCiv, (77, 23))
                set_starting_techs(iCiv)
                setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
                clearPlague(iCiv)
        flipUnitsInArea(
            tTopLeft, tBottomRight, iCiv, Civ.BARBARIAN, True, True
        )  # remaining barbs in the region now belong to the new civ
        flipUnitsInPlots(
            civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES],
            iCiv,
            Civ.BARBARIAN,
            True,
            True,
        )  # remaining barbs in the region now belong to the new civ
        for iIndyCiv in civilizations().independents().ids():
            flipUnitsInArea(
                tTopLeft, tBottomRight, iCiv, iIndyCiv, True, False
            )  # remaining independents in the region now belong to the new civ
            flipUnitsInPlots(
                civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES],
                iCiv,
                iIndyCiv,
                True,
                False,
            )  # remaining independents in the region now belong to the new civ

    if iNumHumanCitiesToConvert > 0:
        flipPopup(iCiv, tTopLeft, tBottomRight)


def convertSurroundingCities(iCiv, tTopLeft, tBottomRight):
    iConvertedCitiesCount = 0
    iNumHumanCities = 0
    setSpawnWar(0)

    # collect all the cities in the spawn region
    for city in (
        plots()
        .rectangle(tTopLeft, tBottomRight)
        .add(civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES])
        .cities()
        .not_owner(iCiv)
        .entities()
    ):
        # if 0, no flip; if > 0, flip will occur with the value as variable for CultureManager()
        iCultureChange = 0

        if is_minor_civ(city):
            iCultureChange = 100
        # case 2: human city
        elif city.getOwner() == human() and not city.isCapital():
            if iNumHumanCities == 0:
                iNumHumanCities += 1
        # case 3: other
        elif not city.isCapital():  # 3Miro: this keeps crashing in the C++, makes no sense
            if iConvertedCitiesCount < 6:  # there won't be more than 5 flips in the area
                iCultureChange = 50
                if turn() <= civilization(iCiv).date.birth + 5:  # if we're during a birth
                    rndNum = percentage()
                    # 3Miro: I don't know why the iOwner check is needed below, but the module crashes sometimes
                    if is_major_civ(city) and rndNum >= civilization(city).ai.stop_birth_threshold:
                        if not civilization(iCiv).at_war(city):
                            civilization(iCiv).declare_war(city)
                            if player(iCiv).getNumCities() > 0:
                                if location(player(iCiv).getCapitalCity()) != (-1, -1):
                                    # this check is needed, otherwise game crashes
                                    createAdditionalUnits(iCiv, player(iCiv).getCapitalCity())
                                else:
                                    createAdditionalUnits(
                                        iCiv, civilization(iCiv).location.capital
                                    )

        if iCultureChange > 0:
            cultureManager(
                location(city), iCultureChange, iCiv, city.getOwner(), True, False, False
            )
            flipUnitsInCityBefore(location(city), iCiv, city.getOwner())
            setTempFlippingCity(location(city))  # necessary for the (688379128, 0) bug
            flipCity(location(city), 0, 0, iCiv, [city.getOwner()])
            flipUnitsInCityAfter(getTempFlippingCity(), iCiv)
            iConvertedCitiesCount += 1

    if iConvertedCitiesCount > 0:
        if player(iCiv).isHuman():
            message(iCiv, text("TXT_KEY_FLIP_TO_US"), force=True, color=MessageData.GREEN)
    return (iConvertedCitiesCount, iNumHumanCities)


def convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight):
    for plot in (
        plots()
        .rectangle(tTopLeft, tBottomRight)
        .add(civilization(iCiv).location.area[AreaType.CORE][Area.ADDITIONAL_TILES])
        .filter(lambda p: not p.isCity())
        .entities()
    ):
        convertPlotCulture(plot, iCiv, 100, False)


def findSeaPlots(tCoords, iRange):
    """Searches a sea plot that isn't occupied by a unit within range of the starting coordinates"""
    # we can search inside other players territory, since all naval units can cross sea borders
    seaPlotList = [
        location(plot)
        for plot in (
            plots()
            .surrounding(tCoords, radius=iRange)
            .water()
            .filter(lambda p: not p.isUnit())
            .entities()
        )
    ]
    # this is a good plot, so paint it and continue search
    if seaPlotList:
        return choice(seaPlotList)
    return None


def getSpecialRespawn(
    iGameTurn,
):  # Absinthe: only the first civ for which it is True is returned, so the order of the civs is very important here
    if canSpecialRespawn(Civ.FRANCE, iGameTurn, 12):
        # France united in it's modern borders, start of the Bourbon royal line
        if year(1588) < iGameTurn < year(1700) and iGameTurn % 5 == 3:
            return Civ.FRANCE
    if canSpecialRespawn(Civ.ARABIA, iGameTurn):
        # Saladin, Ayyubid Dynasty
        if year(1080) < iGameTurn < year(1291) and iGameTurn % 7 == 3:
            return Civ.ARABIA
    if canSpecialRespawn(Civ.BULGARIA, iGameTurn):
        # second Bulgarian Empire
        if year(1080) < iGameTurn < year(1299) and iGameTurn % 5 == 1:
            return Civ.BULGARIA
    if canSpecialRespawn(Civ.CORDOBA, iGameTurn):
        # special respawn as the Hafsid dynasty in North Africa
        if year(1229) < iGameTurn < year(1540) and iGameTurn % 5 == 3:
            return Civ.CORDOBA
    if canSpecialRespawn(Civ.BURGUNDY, iGameTurn, 20):
        # Burgundy in the 100 years war
        if year(1336) < iGameTurn < year(1453) and iGameTurn % 8 == 1:
            return Civ.BURGUNDY
    if canSpecialRespawn(Civ.PRUSSIA, iGameTurn):
        # respawn as the unified Prussia
        if iGameTurn > year(1618) and iGameTurn % 3 == 1:
            return Civ.PRUSSIA
    if canSpecialRespawn(Civ.HUNGARY, iGameTurn):
        # reconquest of Buda from the Ottomans
        if iGameTurn > year(1680) and iGameTurn % 6 == 2:
            return Civ.HUNGARY
    if canSpecialRespawn(Civ.CASTILE, iGameTurn, 25):
        # respawn as the Castile/Aragon Union
        if year(1470) < iGameTurn < year(1580) and iGameTurn % 5 == 0:
            return Civ.CASTILE
    if canSpecialRespawn(Civ.ENGLAND, iGameTurn, 12):
        # restoration of monarchy
        if iGameTurn > year(1660) and iGameTurn % 6 == 2:
            return Civ.ENGLAND
    if canSpecialRespawn(Civ.SCOTLAND, iGameTurn, 30):
        if iGameTurn <= year(1600) and iGameTurn % 6 == 3:
            return Civ.SCOTLAND
    if canSpecialRespawn(Civ.PORTUGAL, iGameTurn):
        # respawn to be around for colonies
        if year(1431) < iGameTurn < year(1580) and iGameTurn % 5 == 3:
            return Civ.PORTUGAL
    if canSpecialRespawn(Civ.AUSTRIA, iGameTurn):
        # increasing Habsburg influence in Hungary
        if year(1526) < iGameTurn < year(1690) and iGameTurn % 8 == 3:
            return Civ.AUSTRIA
    if canSpecialRespawn(Civ.KIEV, iGameTurn):
        # Cossack Hetmanate
        if year(1620) < iGameTurn < year(1750) and iGameTurn % 5 == 3:
            return Civ.KIEV
    if canSpecialRespawn(Civ.MOROCCO, iGameTurn):
        # Alaouite Dynasty
        if iGameTurn > year(1631) and iGameTurn % 8 == 7:
            return Civ.MOROCCO
    if canSpecialRespawn(Civ.ARAGON, iGameTurn):
        # Kingdom of Sicily
        if iGameTurn > year(1700) and iGameTurn % 8 == 7:
            return Civ.ARAGON
    if canSpecialRespawn(Civ.VENECIA, iGameTurn):
        if year(1401) < iGameTurn < year(1571) and iGameTurn % 8 == 7:
            return Civ.VENECIA
    if canSpecialRespawn(Civ.POLAND, iGameTurn):
        if year(1410) < iGameTurn < year(1570) and iGameTurn % 8 == 7:
            return Civ.POLAND
    if canSpecialRespawn(Civ.OTTOMAN, iGameTurn):
        # Mehmed II's conquests
        if year(1453) < iGameTurn < year(1514) and iGameTurn % 6 == 3:
            return Civ.OTTOMAN
    return -1


def canSpecialRespawn(iPlayer, iGameTurn, iLastAliveInterval=10):
    pPlayer = gc.getPlayer(iPlayer)
    if pPlayer.isAlive():
        return False
    if pPlayer.getEverRespawned():
        return False
    if iGameTurn <= civilization(iPlayer).date.birth + 25:
        return False
    if iGameTurn <= (getLastTurnAlive(iPlayer) + iLastAliveInterval):
        return False
    return True


def initMinorBetrayal(iCiv):
    iHuman = human()
    plotList = squareSearch(
        civilization(iCiv).location.area[AreaType.CORE][Area.TILE_MIN],
        civilization(iCiv).location.area[AreaType.CORE][Area.TILE_MAX],
        outerInvasion,
        [],
    )
    if plotList:
        tPlot = choice(plotList)
        createAdditionalUnits(iCiv, tPlot)
        unitsBetrayal(
            iCiv,
            iHuman,
            civilization(iCiv).location.area[AreaType.CORE][Area.TILE_MIN],
            civilization(iCiv).location.area[AreaType.CORE][Area.TILE_MAX],
            tPlot,
        )


def initBetrayal():
    iHuman = human()
    turnsLeft = getBetrayalTurns()
    plotList = squareSearch(getTempTopLeft(), getTempBottomRight(), outerInvasion, [])
    if not plotList:
        plotList = squareSearch(
            getTempTopLeft(),
            getTempBottomRight(),
            innerSpawn,
            [getOldCivFlip(), getNewCivFlip()],
        )
    if not plotList:
        plotList = squareSearch(
            getTempTopLeft(),
            getTempBottomRight(),
            forcedInvasion,
            [getOldCivFlip(), getNewCivFlip()],
        )
    if plotList:
        tPlot = choice(plotList)
        if turnsLeft == iBetrayalPeriod:
            createAdditionalUnits(getNewCivFlip(), tPlot)
        unitsBetrayal(
            getNewCivFlip(),
            getOldCivFlip(),
            getTempTopLeft(),
            getTempBottomRight(),
            tPlot,
        )
    setBetrayalTurns(turnsLeft - 1)


def unitsBetrayal(iNewOwner, iOldOwner, tTopLeft, tBottomRight, tPlot):
    if gc.getPlayer(getOldCivFlip()).isHuman():
        message(getOldCivFlip(), text("TXT_KEY_FLIP_BETRAYAL"), color=MessageData.RED)
    elif gc.getPlayer(getNewCivFlip()).isHuman():
        message(getNewCivFlip(), text("TXT_KEY_FLIP_BETRAYAL_NEW"), color=MessageData.GREEN)
    for unit in plots().rectangle(tTopLeft, tBottomRight).units().owner(iOldOwner).entities():
        if percentage_chance(iBetrayalThreshold, reverse=True):
            if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
                iUnitType = unit.getUnitType()
                unit.kill(False, iNewOwner)
                make_unit(iNewOwner, iUnitType, tPlot)
                i = i - 1


def createAdditionalUnits(iCiv, tPlot):
    # additional starting units if someone declares war on the civ during birth
    units = civilization(iCiv).initial.get("additional_units")
    if units is not None:
        if iCiv != human():
            for unit, number in units.get(PlayerType.AI, {}).items():
                make_units(iCiv, unit, tPlot, number)
        else:
            for unit, number in units.get(PlayerType.HUMAN, {}).items():
                make_units(iCiv, unit, tPlot, number)


def createStartingUnits(iCiv, tPlot):
    # set the provinces
    Provinces.onSpawn(iCiv)

    units = civilization(iCiv).initial.get("units")
    if units is not None:
        for unit, number in units.get(PlayerType.ANY, {}).items():
            make_units(iCiv, unit, tPlot, number)

        if iCiv != human():
            for unit, number in units.get(PlayerType.AI, {}).items():
                make_units(iCiv, unit, tPlot, number)
        else:
            for unit, number in units.get(PlayerType.HUMAN, {}).items():
                make_units(iCiv, unit, tPlot, number)

    if iCiv == Civ.VENECIA:
        tSeaPlot = findSeaPlots((57, 35), 2)
        if tSeaPlot:
            make_unit(iCiv, Unit.WORKBOAT, tSeaPlot)
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
            make_unit(iCiv, Unit.SETTLER, tSeaPlot)
            make_unit(iCiv, Unit.ARCHER, tSeaPlot)
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
            make_unit(iCiv, Unit.SETTLER, tSeaPlot)
            make_unit(iCiv, Unit.SPEARMAN, tSeaPlot)
    elif iCiv == Civ.NORWAY:
        tSeaPlot = findSeaPlots(tPlot, 2)
        if tSeaPlot:
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
            make_unit(iCiv, Unit.SETTLER, tSeaPlot)
            make_unit(iCiv, Unit.ARCHER, tSeaPlot)
    elif iCiv == Civ.DENMARK:
        tSeaPlot = findSeaPlots((60, 57), 2)
        if tSeaPlot:
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
            make_unit(iCiv, Unit.SETTLER, tSeaPlot)
            make_unit(iCiv, Unit.CROSSBOWMAN, tSeaPlot)
            make_unit(iCiv, Unit.SETTLER, tSeaPlot)
            make_unit(iCiv, Unit.CROSSBOWMAN, tSeaPlot)
    elif iCiv == Civ.GENOA:
        tSeaPlot = findSeaPlots(tPlot, 2)
        if tSeaPlot:
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
            make_unit(iCiv, Unit.WAR_GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
            make_unit(iCiv, Unit.SETTLER, tSeaPlot)
            make_unit(iCiv, Unit.CROSSBOWMAN, tSeaPlot)
            make_unit(iCiv, Unit.WORKBOAT, tSeaPlot)
    elif iCiv == Civ.ENGLAND:
        tSeaPlot = findSeaPlots((43, 53), 1)
        if tSeaPlot:
            make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
            make_unit(iCiv, Unit.WAR_GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
    elif iCiv == Civ.ARAGON:
        tSeaPlot = findSeaPlots((42, 29), 1)
        if tSeaPlot:
            make_units(iCiv, Unit.WAR_GALLEY, tSeaPlot, 2, UnitAITypes.UNITAI_ESCORT_SEA)
            make_unit(iCiv, Unit.COGGE, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
            make_unit(iCiv, Unit.SETTLER, tSeaPlot)
            make_unit(iCiv, Unit.CROSSBOWMAN, tSeaPlot)
            make_unit(iCiv, Unit.WORKBOAT, tSeaPlot)
    elif iCiv == Civ.SWEDEN:
        tSeaPlot = findSeaPlots((69, 65), 2)
        if tSeaPlot:
            make_unit(iCiv, Unit.WORKBOAT, tSeaPlot)
            make_unit(iCiv, Unit.WAR_GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
            make_units(iCiv, Unit.COGGE, tSeaPlot, 2, UnitAITypes.UNITAI_SETTLER_SEA)
            make_unit(iCiv, Unit.SETTLER, tSeaPlot)
            make_unit(iCiv, Unit.ARBALEST, tSeaPlot)
    elif iCiv == Civ.DUTCH:
        tSeaPlot = findSeaPlots(tPlot, 2)
        if tSeaPlot:
            make_units(iCiv, Unit.WORKBOAT, tSeaPlot, 2)
            make_units(iCiv, Unit.GALLEON, tSeaPlot, 2)
