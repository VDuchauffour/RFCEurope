from CvPythonExtensions import *
from CoreData import civilization, civilizations
from CoreStructures import human, make_unit, make_units, player, team, teamtype, turn
import PyHelpers  # LOQ
from PyUtils import chance, percentage, percentage_chance, rand, choice
import RFCUtils
import Province
import Religions
from Scenario import get_scenario, get_scenario_start_turn
import Victory
from StoredData import data
import Crusades

from MiscData import PLAGUE_IMMUNITY, MessageData
from CoreTypes import (
    Building,
    Civ,
    PlayerType,
    Scenario,
    Religion,
    Specialist,
    Terrain,
    Feature,
    Improvement,
    ProvinceType,
    UniquePower,
    StabilityCategory,
    Technology,
    Unit,
)
from CoreFunctions import event_popup, get_civ_by_id, text
from LocationsData import CIV_CAPITAL_LOCATIONS
from TimelineData import DateTurn

gc = CyGlobalContext()  # LOQ
PyPlayer = PyHelpers.PyPlayer  # LOQ
utils = RFCUtils.RFCUtils()
rel = Religions.Religions()
vic = Victory.Victory()
cru = Crusades.Crusades()

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 66
iRebellionDelay = 15
iEscapePeriod = 30


class RiseAndFall:
    def __init__(self):
        self.pm = Province.ProvinceManager()
        # Init the Province Manager

    ##################################################
    ### Secure storage & retrieval of script data ###
    ################################################

    def getNewCiv(self):
        return data.iNewCiv

    def setNewCiv(self, iNewValue):
        data.iNewCiv = iNewValue

    def getNewCivFlip(self):
        return data.iNewCivFlip

    def setNewCivFlip(self, iNewValue):
        data.iNewCivFlip = iNewValue

    def getOldCivFlip(self):
        return data.iOldCivFlip

    def setOldCivFlip(self, iNewValue):
        data.iOldCivFlip = iNewValue

    def getTempTopLeft(self):
        return data.iTempTopLeft

    def setTempTopLeft(self, tNewValue):
        data.iTempTopLeft = tNewValue

    def getTempBottomRight(self):
        return data.iTempBottomRight

    def setTempBottomRight(self, tNewValue):
        data.iTempBottomRight = tNewValue

    def getSpawnWar(self):
        return data.iSpawnWar

    def setSpawnWar(self, iNewValue):
        data.iSpawnWar = iNewValue

    def getAlreadySwitched(self):
        return data.bAlreadySwitched

    def setAlreadySwitched(self, bNewValue):
        data.bAlreadySwitched = bNewValue

    def getColonistsAlreadyGiven(self, iCiv):
        return data.lColonistsAlreadyGiven[iCiv]

    def setColonistsAlreadyGiven(self, iCiv, iNewValue):
        data.lColonistsAlreadyGiven[iCiv] = iNewValue

    def getNumCities(self, iCiv):
        return data.lNumCities[iCiv]

    def setNumCities(self, iCiv, iNewValue):
        data.lNumCities[iCiv] = iNewValue

    def getSpawnDelay(self, iCiv):
        return data.lSpawnDelay[iCiv]

    def setSpawnDelay(self, iCiv, iNewValue):
        data.lSpawnDelay[iCiv] = iNewValue

    def getFlipsDelay(self, iCiv):
        return data.lFlipsDelay[iCiv]

    def setFlipsDelay(self, iCiv, iNewValue):
        data.lFlipsDelay[iCiv] = iNewValue

    def getBetrayalTurns(self):
        return data.iBetrayalTurns

    def setBetrayalTurns(self, iNewValue):
        data.iBetrayalTurns = iNewValue

    def getLatestRebellionTurn(self, iCiv):
        return data.lLatestRebellionTurn[iCiv]

    def setLatestRebellionTurn(self, iCiv, iNewValue):
        data.lLatestRebellionTurn[iCiv] = iNewValue

    def getRebelCiv(self):
        return data.iRebelCiv

    def setRebelCiv(self, iNewValue):
        data.iRebelCiv = iNewValue

    def getRebelCities(self):
        return data.lRebelCities

    def setRebelCities(self, lCityList):
        data.lRebelCities = lCityList

    def getRebelSuppress(self):
        return data.lRebelSuppress

    def setRebelSuppress(self, lSuppressList):
        data.lRebelSuppress = lSuppressList

    def getExileData(self, i):
        return data.lExileData[i]

    def setExileData(self, i, iNewValue):
        data.lExileData[i] = iNewValue

    def getTempFlippingCity(self):
        return data.iTempFlippingCity

    def setTempFlippingCity(self, tNewValue):
        data.iTempFlippingCity = tNewValue

    def getCheatersCheck(self, i):
        return data.lCheatersCheck[i]

    def setCheatersCheck(self, i, iNewValue):
        data.lCheatersCheck[i] = iNewValue

    def getDeleteMode(self, i):
        return data.lDeleteMode[i]

    def setDeleteMode(self, i, iNewValue):
        data.lDeleteMode[i] = iNewValue

    # Sedna17 Respawn
    def setSpecialRespawnTurn(self, iCiv, iNewValue):
        data.lSpecialRespawnTurn[iCiv] = iNewValue

    def getSpecialRespawnTurns(self):
        return data.lSpecialRespawnTurn

    ###############
    ### Popups ###
    #############

    """ popupID has to be a registered ID in CvRhyesCatapultEventManager.__init__!! """

    def newCivPopup(self, iCiv):
        event_popup(
            7614,
            text("TXT_KEY_NEWCIV_TITLE"),
            text("TXT_KEY_NEWCIV_MESSAGE", player(iCiv).getCivilizationAdjectiveKey()),
            [text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO")],
        )
        self.setNewCiv(iCiv)

    def eventApply7614(self, popupReturn):
        if popupReturn.getButtonClicked() == 0:  # 1st button
            iOldHandicap = gc.getActivePlayer().getHandicapType()
            iNewCiv = self.getNewCiv()
            vic.switchUHV(iNewCiv, human())
            gc.getActivePlayer().setHandicapType(gc.getPlayer(iNewCiv).getHandicapType())
            gc.getGame().setActivePlayer(iNewCiv, False)
            gc.getPlayer(iNewCiv).setHandicapType(iOldHandicap)
            for iMaster in civilizations().majors().ids():
                if gc.getTeam(gc.getPlayer(iNewCiv).getTeam()).isVassal(iMaster):
                    gc.getTeam(gc.getPlayer(iNewCiv).getTeam()).setVassal(iMaster, False, False)
            self.setAlreadySwitched(True)
            gc.getPlayer(iNewCiv).setPlayable(True)

    def flipPopup(self, iNewCiv, tTopLeft, tBottomRight):
        iHuman = human()
        flipText = text("TXT_KEY_FLIPMESSAGE1")

        lPlots = (
            utils.getPlotList(tTopLeft, tBottomRight)
            + civilization(iNewCiv).location.area.core.additional_tiles
        )
        for (x, y) in lPlots:
            plot = gc.getMap().plot(x, y)
            if plot.isCity():
                if plot.getPlotCity().getOwner() == iHuman:
                    if not plot.getPlotCity().isCapital():
                        flipText += plot.getPlotCity().getName() + "\n"
        flipText += text("TXT_KEY_FLIPMESSAGE2")

        event_popup(
            7615,
            text("TXT_KEY_NEWCIV_TITLE"),
            flipText,
            [text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO")],
        )
        self.setNewCivFlip(iNewCiv)
        self.setOldCivFlip(iHuman)
        self.setTempTopLeft(tTopLeft)
        self.setTempBottomRight(tBottomRight)

    def eventApply7615(self, popupReturn):
        iHuman = human()
        tTopLeft = self.getTempTopLeft()
        tBottomRight = self.getTempBottomRight()
        iNewCivFlip = self.getNewCivFlip()

        humanCityList = []

        lPlots = (
            utils.getPlotList(tTopLeft, tBottomRight)
            + civilization(iNewCivFlip).location.area.core.additional_tiles
        )
        for (x, y) in lPlots:
            plot = gc.getMap().plot(x, y)
            if plot.isCity():
                city = plot.getPlotCity()
                if city.getOwner() == iHuman:
                    if not city.isCapital():
                        humanCityList.append(city)

        if popupReturn.getButtonClicked() == 0:  # 1st button
            CyInterface().addMessage(
                iHuman,
                True,
                MessageData.DURATION,
                text("TXT_KEY_FLIP_AGREED"),
                "",
                0,
                "",
                ColorTypes(MessageData.GREEN),
                -1,
                -1,
                True,
                True,
            )

            if humanCityList:
                for city in humanCityList:
                    tCity = (city.getX(), city.getY())
                    utils.cultureManager(tCity, 100, iNewCivFlip, iHuman, False, False, False)
                    utils.flipUnitsInCityBefore(tCity, iNewCivFlip, iHuman)
                    self.setTempFlippingCity(tCity)
                    utils.flipCity(tCity, 0, 0, iNewCivFlip, [iHuman])
                    utils.flipUnitsInCityAfter(tCity, iNewCivFlip)

            # same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
            for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
                betrayalPlot = gc.getMap().plot(x, y)
                iNumUnitsInAPlot = betrayalPlot.getNumUnits()
                if iNumUnitsInAPlot > 0:
                    for i in range(iNumUnitsInAPlot):
                        unit = betrayalPlot.getUnit(i)
                        if unit.getOwner() == iHuman:
                            rndNum = percentage()
                            if rndNum >= iBetrayalThreshold:
                                if unit.getDomainType() == DomainTypes.DOMAIN_SEA:  # land unit
                                    iUnitType = unit.getUnitType()
                                    unit.kill(False, iNewCivFlip)
                                    make_unit(iNewCivFlip, iUnitType, (x, y))
                                    i = i - 1

            if self.getCheatersCheck(0) == 0:
                self.setCheatersCheck(0, iCheatersPeriod)
                self.setCheatersCheck(1, self.getNewCivFlip())

        elif popupReturn.getButtonClicked() == 1:  # 2nd button
            CyInterface().addMessage(
                iHuman,
                True,
                MessageData.DURATION,
                text("TXT_KEY_FLIP_REFUSED"),
                "",
                0,
                "",
                ColorTypes(MessageData.RED),
                -1,
                -1,
                True,
                True,
            )

            if humanCityList:
                for city in humanCityList:
                    pCurrent = gc.getMap().plot(city.getX(), city.getY())
                    oldCulture = pCurrent.getCulture(iHuman)
                    # Absinthe: changeCulture instead of setCulture, otherwise previous culture will be lost
                    pCurrent.changeCulture(iNewCivFlip, oldCulture / 2, True)
                    pCurrent.setCulture(iHuman, oldCulture / 2, True)
                    iWar = self.getSpawnWar() + 1
                    self.setSpawnWar(iWar)
                    if self.getSpawnWar() == 1:
                        # safety check - don't want to use canDeclareWar, as here we want to always declare war
                        if not gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).isAtWar(iHuman):
                            gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).declareWar(
                                iHuman, False, -1
                            )
                        self.setBetrayalTurns(iBetrayalPeriod)
                        self.initBetrayal()

    # resurrection when some human controlled cities are also included
    def rebellionPopup(self, iRebelCiv, iNumCities):
        iLoyalPrice = min((10 * gc.getPlayer(human()).getGold()) / 100, 50 * iNumCities)
        event_popup(
            7622,
            text("TXT_KEY_REBELLION_TITLE"),
            text("TXT_KEY_REBELLION_HUMAN", player(iRebelCiv).getCivilizationAdjectiveKey()),
            [
                text("TXT_KEY_REBELLION_LETGO"),
                text("TXT_KEY_REBELLION_DONOTHING"),
                text("TXT_KEY_REBELLION_CRACK"),
                text("TXT_KEY_REBELLION_BRIBE") + " " + str(iLoyalPrice),
                text("TXT_KEY_REBELLION_BOTH"),
            ],
        )

    # resurrection when some human controlled cities are also included
    def eventApply7622(self, popupReturn):
        iHuman = human()
        iRebelCiv = self.getRebelCiv()
        iChoice = popupReturn.getButtonClicked()
        iHumanCity = 0
        lCityList = self.getRebelCities()
        for (x, y) in lCityList:
            iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
            if iOwner == iHuman:
                iHumanCity += 1

        if iChoice == 1:
            lList = self.getRebelSuppress()
            lList[iHuman] = 2  # let go + war
            self.setRebelSuppress(lList)
        elif iChoice == 2:
            if percentage_chance(40, strict=True):
                lCityList = self.getRebelCities()
                for (x, y) in lCityList:
                    pCity = gc.getMap().plot(x, y).getPlotCity()
                    if pCity.getOwner() == iHuman:
                        pCity.changeOccupationTimer(2)
                        pCity.changeHurryAngerTimer(10)
                lList = self.getRebelSuppress()
                lList[iHuman] = 3  # keep cities + war
                self.setRebelSuppress(lList)
            else:
                lList = self.getRebelSuppress()
                lList[iHuman] = 4  # let go + war
                self.setRebelSuppress(lList)
        elif iChoice == 3:
            iLoyalPrice = min((10 * gc.getPlayer(iHuman).getGold()) / 100, 50 * iHumanCity)
            gc.getPlayer(iHuman).setGold(gc.getPlayer(iHuman).getGold() - iLoyalPrice)
            if percentage_chance(iLoyalPrice / iHumanCity, strict=True):
                lList = self.getRebelSuppress()
                lList[iHuman] = 1  # keep + no war
                self.setRebelSuppress(lList)
            else:
                lList = self.getRebelSuppress()
                lList[iHuman] = 4  # let go + war
                self.setRebelSuppress(lList)
        elif iChoice == 4:
            iLoyalPrice = min((10 * gc.getPlayer(iHuman).getGold()) / 100, 50 * iHumanCity)
            gc.getPlayer(iHuman).setGold(gc.getPlayer(iHuman).getGold() - iLoyalPrice)
            if percentage_chance(iLoyalPrice / iHumanCity + 40, strict=True):
                lCityList = self.getRebelCities()
                for (x, y) in lCityList:
                    pCity = gc.getMap().plot(x, y).getPlotCity()
                    if pCity.getOwner() == iHuman:
                        pCity.changeOccupationTimer(2)
                        pCity.changeHurryAngerTimer(10)
                lList = self.getRebelSuppress()
                lList[iHuman] = 3  # keep + war
                self.setRebelSuppress(lList)
            else:
                lList = self.getRebelSuppress()
                lList[iHuman] = 2  # let go + war
                self.setRebelSuppress(lList)
        self.resurectCiv(self.getRebelCiv())

    #######################################
    ### Main methods (Event-Triggered) ###
    #####################################

    def setup(self):
        self.setEarlyLeaders()

        # Sedna17 Respawn setup special respawn turns
        self.setupRespawnTurns()

        iHuman = human()
        if get_scenario() == Scenario.i500AD:
            self.create500ADstartingUnits()
            for civ in (
                civilizations().majors().filter(lambda c: c.date.birth == DateTurn.i500AD).ids()
            ):
                self.showArea(civ)
                self.initContact(civ)

        else:
            self.create1200ADstartingUnits()
            for civ in (
                civilizations()
                .main()
                .filter(lambda c: c.date.birth < get_scenario_start_turn(Scenario.i1200AD))
                .ids()
            ):
                self.showArea(civ)
                self.initContact(civ, False)
                # Temporarily all civs get the same starting techs as Aragon
                self.assign1200ADtechs(civ)
            self.setStartingFaith()
            self.setDiplo1200AD()
            self.LeaningTowerGP()
            rel.spread1200ADJews()  # Spread Jews to some random cities
            vic.set1200UHVDone(iHuman)
            # Temporarily all civs get the same starting techs as Aragon
            self.assign1200ADtechs(Civ.POPE.value)
            cru.do1200ADCrusades()

        self.assignGold()

    def assignGold(self):
        for civ in civilizations():
            condition = civ.scenario.get("condition")
            if condition is not None:
                civ.player.changeGold(condition.gold)

    def setStartingFaith(self):
        for civ in civilizations():
            condition = civ.scenario.get("condition")
            if condition is not None:
                civ.player.setFaith(condition.faith)

    def onCityBuilt(self, iPlayer, pCity):
        tCity = (pCity.getX(), pCity.getY())
        x, y = tCity
        self.pm.onCityBuilt(iPlayer, pCity.getX(), pCity.getY())
        # Absinthe: We can add free buildings for new cities here
        # 			Note that it will add the building every time a city is founded on the plot, not just on the first time
        # 			Venice (56, 35), Augsburg (55, 41), Porto (23, 31), Prague (60, 44), Riga (74, 58), Perekop (87, 36)
        # 			London (41, 52), Novgorod (80, 62) currently has preplaced fort on the map instead
        if tCity in [(56, 35), (55, 41), (23, 31), (60, 44), (74, 58), (87, 36)]:
            pCity.setHasRealBuilding(utils.getUniqueBuilding(iPlayer, Building.WALLS.value), True)
        elif tCity == (75, 53):  # Vilnius - important for AI Lithuania against Prussia
            if not gc.getPlayer(Civ.LITHUANIA.value).isHuman():
                pCity.setHasRealBuilding(
                    utils.getUniqueBuilding(iPlayer, Building.WALLS.value), True
                )

    def onCityAcquired(self, owner, iPlayer, city, bConquest, bTrade):
        self.pm.onCityAcquired(owner, iPlayer, city, bConquest, bTrade)
        # Constantinople -> Istanbul
        if iPlayer == Civ.OTTOMAN.value:
            cityList = utils.getCityList(iPlayer)
            if (city.getX(), city.getY()) == CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM]:
                for loopCity in cityList:
                    if loopCity != city:
                        loopCity.setHasRealBuilding((Building.PALACE.value), False)
                city.setHasRealBuilding(Building.PALACE.value, True)
                if civilization(Civ.OTTOMAN).has_state_religion(Religion.ISLAM):
                    city.setHasReligion(Religion.ISLAM.value, True, True, False)
                # some stability boost and flavour message
                player(Civ.OTTOMAN).changeStabilityBase(StabilityCategory.EXPANSION.value, 6)
                if human() == iPlayer:
                    CyInterface().addMessage(
                        iPlayer,
                        True,
                        MessageData.DURATION,
                        text("TXT_KEY_GLORY_ON_CONQUEST"),
                        "",
                        0,
                        "",
                        ColorTypes(MessageData.GREEN),
                        -1,
                        -1,
                        True,
                        True,
                    )

            # Absinthe: Edirne becomes capital if conquered before Constantinople
            else:
                if (city.getX(), city.getY()) == (76, 25):
                    bHasIstanbul = False
                    IstanbulPlot = gc.getMap().plot(*CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM])
                    if IstanbulPlot.isCity():
                        if IstanbulPlot.getPlotCity().getOwner() == iPlayer:
                            bHasIstanbul = True
                    if not bHasIstanbul:
                        gc.getPlayer(iPlayer).getCapitalCity().setHasRealBuilding(
                            Building.PALACE.value, False
                        )
                        city.setHasRealBuilding(Building.PALACE.value, True)
                    if civilization(Civ.OTTOMAN).has_state_religion(Religion.ISLAM):
                        city.setHasReligion(Religion.ISLAM.value, True, True, False)

        # Absinthe: Message for the human player, if the last city of a known civ is conquered
        iOriginalOwner = owner
        pOriginalOwner = gc.getPlayer(iOriginalOwner)
        if not pOriginalOwner.isHuman():
            iNumCities = pOriginalOwner.getNumCities()
            if iNumCities == 0:
                # all collapses operate with flips, so if the last city was conquered, we are good to go (this message won't come after a collapse message)
                if bConquest:
                    iHuman = human()
                    if gc.getPlayer(iHuman).canContact(iOriginalOwner):
                        CyInterface().addMessage(
                            iHuman,
                            False,
                            MessageData.DURATION,
                            pOriginalOwner.getCivilizationDescription(0)
                            + " "
                            + text("TXT_KEY_STABILITY_CONQUEST_LAST_CITY"),
                            "",
                            0,
                            "",
                            ColorTypes(MessageData.RED),
                            -1,
                            -1,
                            True,
                            True,
                        )

    def onCityRazed(self, iOwner, iPlayer, city):
        self.pm.onCityRazed(iOwner, iPlayer, city)  # Province Manager

    # Sedna17 Respawn
    def setupRespawnTurns(self):
        for iCiv in civilizations().majors().ids():
            self.setSpecialRespawnTurn(
                iCiv, civilization(iCiv).date.respawning + (rand(21) - 10) + (rand(21) - 10)
            )  # bell-curve-like spawns within +/- 10 turns of desired turn (3Miro: Uniform, not a bell-curve)

    def setEarlyLeaders(self):
        for civ in civilizations().majors().ai():
            if civ.leaders.early != civ.leaders.primary:
                leader = civ.leaders.early
                civ.player.setLeader(leader.value)

    def setWarOnSpawn(self):
        for civ in civilizations():
            wars = civ.scenario.get("wars")
            if wars is not None:
                for other, war_threshold in wars.items():
                    if percentage_chance(war_threshold, strict=True) and not civ.at_war(other):
                        civ.set_war(other)

    def checkTurn(self, iGameTurn):
        # Trigger betrayal mode
        if self.getBetrayalTurns() > 0:
            self.initBetrayal()

        if self.getCheatersCheck(0) > 0:
            teamPlayer = gc.getTeam(gc.getPlayer(human()).getTeam())
            if teamPlayer.isAtWar(self.getCheatersCheck(1)):
                self.initMinorBetrayal(self.getCheatersCheck(1))
                self.setCheatersCheck(0, 0)
                self.setCheatersCheck(1, -1)
            else:
                self.setCheatersCheck(0, self.getCheatersCheck(0) - 1)

        if iGameTurn % 20 == 0:
            for civ in civilizations().independents().alive():
                utils.updateMinorTechs(civ.id, Civ.BARBARIAN.value)

        # Absinthe: checking the spawn dates
        for iLoopCiv in civilizations().majors().ids():
            if (
                civilization(iLoopCiv).date.birth != 0
                and iGameTurn >= civilization(iLoopCiv).date.birth - 2
                and iGameTurn <= civilization(iLoopCiv).date.birth + 4
            ):
                self.initBirth(iGameTurn, civilization(iLoopCiv).date.birth, iLoopCiv)

        # Fragment minor civs:
        # 3Miro: Shuffle cities between Indies and Barbs to make sure there is no big Independent nation
        if iGameTurn >= 20:
            if iGameTurn % 15 == 6:
                self.fragmentIndependents()
            if iGameTurn % 30 == 12:
                self.fragmentBarbarians(iGameTurn)

        # Fall of civs:
        # Barb collapse: if more than 1/3 of the empire is conquered and/or held by barbs = collapse
        # Generic collapse: if 1/2 of the empire is lost in only a few turns (16 ATM) = collapse
        # Motherland collapse: if no city is in the core area and the number of cities in the normal area is less than the number of foreign cities = collapse
        # Secession: if stability is negative there is a chance (bigger chance with worse stability) for a random city to declare it's independence
        if iGameTurn >= 64 and iGameTurn % 7 == 0:  # mainly for Seljuks, Mongols, Timurids
            self.collapseByBarbs(iGameTurn)
        if iGameTurn >= 34 and iGameTurn % 16 == 0:
            self.collapseGeneric(iGameTurn)
        if iGameTurn >= 34 and iGameTurn % 9 == 7:
            self.collapseMotherland(iGameTurn)
        if iGameTurn > 20 and iGameTurn % 3 == 1:
            self.secession(iGameTurn)
        if iGameTurn > 20 and iGameTurn % 7 == 3:
            self.secessionCloseCollapse(iGameTurn)

        # Resurrection of civs:
        # This is one place to control the frequency of resurrection; will not be called with high iNumDeadCivs
        # Generally we want to allow Kiev, Bulgaria, Cordoba, Burgundy, Byzantium at least to be dead in late game without respawning
        # Absinthe: was 12 and 8 originally in RFCE, but we don't need that many dead civs
        iNumDeadCivs1 = 8  # 5 in vanilla RFC, 8 in warlords RFC
        iNumDeadCivs2 = 5  # 3 in vanilla RFC, 6 in warlords RFC

        iCiv = self.getSpecialRespawn(iGameTurn)
        if iCiv > -1:
            self.resurrection(iGameTurn, iCiv)
        elif (
            gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive()
            > iNumDeadCivs1
        ):
            if iGameTurn % 10 == 7:
                self.resurrection(iGameTurn, -1)
        elif (
            gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive()
            > iNumDeadCivs2
        ):
            if iGameTurn % 23 == 11:
                self.resurrection(iGameTurn, -1)

        # Absinthe: Reduce cities to towns, in order to make room for new civs
        if iGameTurn == civilization(Civ.SCOTLAND).date.birth - 3:
            # Reduce Inverness and Scone, so more freedom in where to found cities in Scotland
            self.reduceCity((37, 65))
            self.reduceCity((37, 67))
        elif iGameTurn == civilization(Civ.ENGLAND).date.birth - 3:
            # Reduce Norwich and Nottingham, so more freedom in where to found cities in England
            self.reduceCity((43, 55))
            self.reduceCity((39, 56))
        elif iGameTurn == civilization(Civ.SWEDEN).date.birth - 2:
            # Reduce Uppsala
            self.reduceCity((65, 66))
        # Absinthe: Reduce cities to town, if not owned by the human player
        if iGameTurn == DateTurn.i1057AD:
            # Reduce Kairouan
            pPlot = gc.getMap().plot(43, 55)
            if pPlot.isCity():
                if pPlot.getPlotCity().getOwner() != human():
                    self.reduceCity((43, 55))

    def reduceCity(self, tPlot):
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
            CyInterface().addMessage(
                pPlot.getPlotCity().getOwner(),
                False,
                MessageData.DURATION,
                msgString,
                "",
                0,
                "",
                ColorTypes(MessageData.ORANGE),
                tPlot[0],
                tPlot[1],
                True,
                True,
            )

            pPlot.eraseCityDevelopment()
            pPlot.setImprovementType(
                Improvement.TOWN.value
            )  # Improvement Town instead of the city
            pPlot.setRouteType(0)  # Also adding a road there

    def checkPlayerTurn(self, iGameTurn, iPlayer):
        # Absinthe & Merijn: leader switching with any number of leaders
        late_leaders = civilization(iPlayer).leaders.late
        if late_leaders:
            for tLeader in reversed(late_leaders):
                if iGameTurn >= tLeader[1]:
                    self.switchLateLeaders(iPlayer, tLeader)
                    break

        # 3Miro: English cheat, the AI is utterly incompetent when it has to launch an invasion on an island
        # 			if in 1300AD Dublin is still Barbarian, it will flip to England
        if (
            iGameTurn == DateTurn.i1300AD
            and human() != Civ.ENGLAND
            and iPlayer == Civ.ENGLAND
            and player(Civ.ENGLAND).isAlive()
        ):
            tDublin = (32, 58)
            pPlot = gc.getMap().plot(tDublin[0], tDublin[1])
            if pPlot.isCity():
                if pPlot.getPlotCity().getOwner() == Civ.BARBARIAN.value:
                    pDublin = pPlot.getPlotCity()
                    utils.cultureManager(
                        tDublin, 50, Civ.ENGLAND.value, Civ.BARBARIAN.value, False, True, True
                    )
                    utils.flipUnitsInCityBefore(tDublin, Civ.ENGLAND.value, Civ.BARBARIAN.value)
                    self.setTempFlippingCity(tDublin)
                    utils.flipCity(
                        tDublin, 0, 0, Civ.ENGLAND.value, [Civ.BARBARIAN.value]
                    )  # by trade because by conquest may raze the city
                    utils.flipUnitsInCityAfter(tDublin, Civ.ENGLAND.value)

        # Absinthe: Another English AI cheat, extra defenders and defensive buildings in Normandy some turns after spawn - from RFCE++
        if (
            iGameTurn == DateTurn.i1066AD + 3
            and human() != Civ.ENGLAND.value
            and iPlayer == Civ.ENGLAND.value
            and player(Civ.ENGLAND).isAlive()
        ):
            for (x, y) in utils.getPlotList((39, 46), (45, 50)):
                pCurrent = gc.getMap().plot(x, y)
                if pCurrent.isCity():
                    pCity = pCurrent.getPlotCity()
                    if pCity.getOwner() == Civ.ENGLAND.value:
                        make_unit(Civ.ENGLAND, Unit.GUISARME, (x, y))
                        make_unit(Civ.ENGLAND, Unit.ARBALEST, (x, y))
                        pCity.setHasRealBuilding(Building.WALLS.value, True)
                        pCity.setHasRealBuilding(Building.CASTLE.value, True)

    def switchLateLeaders(self, iPlayer, tLeader):
        iLeader, iDate, iThreshold, iEra = tLeader
        if iLeader == gc.getPlayer(iPlayer).getLeader():
            return
        if gc.getPlayer(iPlayer).getCurrentEra() >= iEra:
            iThreshold *= 2
        if (
            gc.getPlayer(iPlayer).getAnarchyTurns() != 0
            or utils.getPlagueCountdown(iPlayer) > 0
            or player(iPlayer).getStability() <= -10
            or percentage_chance(iThreshold, strict=True)
        ):
            gc.getPlayer(iPlayer).setLeader(iLeader.value)

            # Absinthe: message about the leader switch for the human player
            iHuman = human()
            HumanTeam = gc.getTeam(gc.getPlayer(iHuman).getTeam())
            PlayerTeam = gc.getPlayer(iPlayer).getTeam()
            if HumanTeam.isHasMet(PlayerTeam) and player().isExisting():
                CyInterface().addMessage(
                    iHuman,
                    False,
                    MessageData.DURATION / 2,
                    CyTranslator().getText(
                        "TXT_KEY_LEADER_SWITCH",
                        (
                            gc.getPlayer(iPlayer).getName(),
                            gc.getPlayer(iPlayer).getCivilizationDescriptionKey(),
                        ),
                    ),
                    "",
                    InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                    "",
                    ColorTypes(MessageData.PURPLE),
                    -1,
                    -1,
                    True,
                    True,
                )

    def fragmentIndependents(self):
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
                    for city in utils.getCityList(iBig):
                        iDivideCounter += 1
                        if iDivideCounter % 2 == 1:
                            tCity = (city.getX(), city.getY())
                            pCurrent = gc.getMap().plot(tCity[0], tCity[1])
                            utils.cultureManager(tCity, 50, iSmall, iBig, False, True, True)
                            utils.flipUnitsInCityBefore(tCity, iSmall, iBig)
                            self.setTempFlippingCity(tCity)
                            utils.flipCity(
                                tCity, 0, 0, iSmall, [iBig]
                            )  # by trade because by conquest may raze the city
                            utils.flipUnitsInCityAfter(tCity, iSmall)
                            iCounter += 1
                            if iCounter == 3:
                                break

    def fragmentBarbarians(self, iGameTurn):
        iRndnum = rand(civilizations().majors().len())
        for j in civilizations().majors().ids():
            iDeadCiv = (j + iRndnum) % civilizations().majors().len()
            if (
                not gc.getPlayer(iDeadCiv).isAlive()
                and iGameTurn > civilization(iDeadCiv).date.birth + 50
            ):
                lCities = []
                for (x, y) in utils.getPlotList(
                    civilization(iDeadCiv).location.area.normal.tile_min,
                    civilization(iDeadCiv).location.area.normal.tile_max,
                ):
                    plot = gc.getMap().plot(x, y)
                    if plot.isCity():
                        if plot.getPlotCity().getOwner() == Civ.BARBARIAN.value:
                            lCities.append((x, y))
                if len(lCities) > 5:
                    iDivideCounter = 0
                    for tCity in lCities:
                        iNewCiv = min(civilizations().independents().ids()) + rand(
                            max(civilizations().independents().ids())
                            - min(civilizations().independents().ids())
                            + 1
                        )
                        if iDivideCounter % 4 in [0, 1]:
                            utils.cultureManager(
                                tCity, 50, iNewCiv, Civ.BARBARIAN.value, False, True, True
                            )
                            utils.flipUnitsInCityBefore(tCity, iNewCiv, Civ.BARBARIAN.value)
                            self.setTempFlippingCity(tCity)
                            utils.flipCity(
                                tCity, 0, 0, iNewCiv, [Civ.BARBARIAN.value]
                            )  # by trade because by conquest may raze the city
                            utils.flipUnitsInCityAfter(tCity, iNewCiv)
                            iDivideCounter += 1
                    return

    def collapseByBarbs(self, iGameTurn):
        # Absinthe: collapses if more than 1/3 of the empire is conquered and/or held by barbs
        for iCiv in civilizations().majors().ids():
            pCiv = gc.getPlayer(iCiv)
            if pCiv.isAlive():
                # Absinthe: no barb collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
                iRespawnTurn = utils.getLastRespawnTurn(iCiv)
                if (
                    iGameTurn >= civilization(iCiv).date.birth + 20
                    and iGameTurn >= iRespawnTurn + 10
                    and not utils.collapseImmune(iCiv)
                ):
                    iNumCities = pCiv.getNumCities()
                    iLostCities = gc.countCitiesLostTo(iCiv, Civ.BARBARIAN.value)
                    # Absinthe: if the civ is respawned, it's harder to collapse them by barbs
                    if pCiv.getRespawnedAlive():
                        iLostCities = max(iLostCities - (iNumCities / 4), 0)
                    # Absinthe: if more than one third is captured, the civ collapses
                    if iLostCities * 2 > iNumCities + 1 and iNumCities > 0:
                        iHuman = human()
                        if not pCiv.isHuman():
                            if gc.getPlayer(iHuman).canContact(iCiv):
                                CyInterface().addMessage(
                                    iHuman,
                                    False,
                                    MessageData.DURATION,
                                    pCiv.getCivilizationDescription(0)
                                    + " "
                                    + CyTranslator().getText(
                                        "TXT_KEY_STABILITY_CIVILWAR_BARBS", ()
                                    ),
                                    "",
                                    0,
                                    "",
                                    ColorTypes(MessageData.RED),
                                    -1,
                                    -1,
                                    True,
                                    True,
                                )
                            utils.killAndFragmentCiv(iCiv, True, False)
                        elif pCiv.getNumCities() > 1:
                            CyInterface().addMessage(
                                iCiv,
                                True,
                                MessageData.DURATION,
                                CyTranslator().getText(
                                    "TXT_KEY_STABILITY_CIVILWAR_BARBS_HUMAN", ()
                                ),
                                "",
                                0,
                                "",
                                ColorTypes(MessageData.RED),
                                -1,
                                -1,
                                True,
                                True,
                            )
                            utils.killAndFragmentCiv(iCiv, True, True)

    def collapseGeneric(self, iGameTurn):
        # Absinthe: collapses if number of cities is less than half than some turns ago
        lNumCitiesLastTime = [0] * civilizations().majors().len()
        for iCiv in civilizations().majors().ids():
            pCiv = gc.getPlayer(iCiv)
            teamCiv = gc.getTeam(pCiv.getTeam())
            if pCiv.isAlive():
                lNumCitiesLastTime[iCiv] = self.getNumCities(iCiv)
                iNumCitiesCurrently = pCiv.getNumCities()
                self.setNumCities(iCiv, iNumCitiesCurrently)
                # Absinthe: no generic collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
                iRespawnTurn = utils.getLastRespawnTurn(iCiv)
                if (
                    iGameTurn >= civilization(iCiv).date.birth + 20
                    and iGameTurn >= iRespawnTurn + 10
                    and not utils.collapseImmune(iCiv)
                ):
                    # Absinthe: pass for small civs, we have bad stability collapses and collapseMotherland anyway, which is better suited for the collapse of those
                    if (
                        lNumCitiesLastTime[iCiv] > 2
                        and iNumCitiesCurrently * 2 <= lNumCitiesLastTime[iCiv]
                    ):
                        iHuman = human()
                        if not pCiv.isHuman():
                            if gc.getPlayer(iHuman).canContact(iCiv):
                                CyInterface().addMessage(
                                    iHuman,
                                    False,
                                    MessageData.DURATION,
                                    pCiv.getCivilizationDescription(0)
                                    + " "
                                    + CyTranslator().getText(
                                        "TXT_KEY_STABILITY_CIVILWAR_DECLINE", ()
                                    ),
                                    "",
                                    0,
                                    "",
                                    ColorTypes(MessageData.RED),
                                    -1,
                                    -1,
                                    True,
                                    True,
                                )
                            utils.killAndFragmentCiv(iCiv, False, False)
                        elif pCiv.getNumCities() > 1:
                            CyInterface().addMessage(
                                iCiv,
                                True,
                                MessageData.DURATION,
                                CyTranslator().getText(
                                    "TXT_KEY_STABILITY_CIVILWAR_DECLINE_HUMAN", ()
                                ),
                                "",
                                0,
                                "",
                                ColorTypes(MessageData.RED),
                                -1,
                                -1,
                                True,
                                True,
                            )
                            utils.killAndFragmentCiv(iCiv, False, True)

    def collapseMotherland(self, iGameTurn):
        # Absinthe: collapses if completely pushed out of the core area and also doesn't have enough presence in the normal area
        for iCiv in civilizations().majors().ids():
            pCiv = gc.getPlayer(iCiv)
            teamCiv = gc.getTeam(pCiv.getTeam())
            if pCiv.isAlive():
                # Absinthe: no motherland collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
                iRespawnTurn = utils.getLastRespawnTurn(iCiv)
                if (
                    iGameTurn >= civilization(iCiv).date.birth + 20
                    and iGameTurn >= iRespawnTurn + 10
                    and not utils.collapseImmune(iCiv)
                ):
                    # Absinthe: respawned Cordoba or Aragon shouldn't collapse because not holding the original core area
                    if iCiv in [Civ.CORDOBA.value, Civ.ARAGON.value] and pCiv.getRespawnedAlive():
                        continue
                    if not gc.safeMotherland(iCiv):
                        iHuman = human()
                        if not pCiv.isHuman():
                            if gc.getPlayer(iHuman).canContact(iCiv):
                                CyInterface().addMessage(
                                    iHuman,
                                    False,
                                    MessageData.DURATION,
                                    pCiv.getCivilizationDescription(0)
                                    + " "
                                    + CyTranslator().getText(
                                        "TXT_KEY_STABILITY_CIVILWAR_MOTHERLAND", ()
                                    ),
                                    "",
                                    0,
                                    "",
                                    ColorTypes(MessageData.RED),
                                    -1,
                                    -1,
                                    True,
                                    True,
                                )
                            utils.killAndFragmentCiv(iCiv, False, False)
                        elif pCiv.getNumCities() > 1:
                            CyInterface().addMessage(
                                iCiv,
                                True,
                                MessageData.DURATION,
                                CyTranslator().getText(
                                    "TXT_KEY_STABILITY_CIVILWAR_MOTHERLAND_HUMAN", ()
                                ),
                                "",
                                0,
                                "",
                                ColorTypes(MessageData.RED),
                                -1,
                                -1,
                                True,
                                True,
                            )
                            utils.killAndFragmentCiv(iCiv, False, True)

    def secession(self, iGameTurn):
        # Absinthe: if stability is negative there is a chance for a random city to declare it's independence, checked every 3 turns
        iRndnum = rand(civilizations().majors().len())
        iSecessionNumber = 0
        for j in civilizations().majors().ids():
            iPlayer = (j + iRndnum) % civilizations().majors().len()
            pPlayer = gc.getPlayer(iPlayer)
            # Absinthe: no city secession for 15 turns after spawn, for 10 turns after respawn
            iRespawnTurn = utils.getLastRespawnTurn(iPlayer)
            if (
                pPlayer.isAlive()
                and iGameTurn >= civilization(iPlayer).date.birth + 15
                and iGameTurn >= iRespawnTurn + 10
            ):
                if chance(10, -2 - pPlayer.getStability(), strict=True):
                    # 10% at -3, increasing by 10% with each point (100% with -12 or less)
                    self.revoltCity(iPlayer, False)
                    iSecessionNumber += 1
                    if iSecessionNumber > 2:
                        return  # max 3 secession per turn
                    continue  # max 1 secession for each civ

    def secessionCloseCollapse(self, iGameTurn):
        # Absinthe: another instance of secession, now with possibility for multiple cities revolting for the same civ
        # Absinthe: this can only happen with very bad stability, in case of fairly big empires
        iRndnum = rand(civilizations().majors().len())
        for j in civilizations().majors().ids():
            iPlayer = (j + iRndnum) % civilizations().majors().len()
            pPlayer = gc.getPlayer(iPlayer)
            iRespawnTurn = utils.getLastRespawnTurn(iPlayer)
            if (
                pPlayer.isAlive()
                and iGameTurn >= civilization(iPlayer).date.birth + 20
                and iGameTurn >= iRespawnTurn + 10
            ):
                iStability = pPlayer.getStability()
                if (
                    iStability < -15 and pPlayer.getNumCities() > 10
                ):  # so the civ is close to a civil war
                    self.revoltCity(iPlayer, False)
                    self.revoltCity(iPlayer, False)
                    self.revoltCity(iPlayer, True)
                    self.revoltCity(iPlayer, True)
                    return  # max for 1 civ at a turn

    def revoltCity(self, iPlayer, bForce):
        pPlayer = gc.getPlayer(iPlayer)
        iStability = pPlayer.getStability()

        cityListInCore = []
        cityListInNotCore = []
        for city in utils.getCityList(iPlayer):
            tCity = (city.getX(), city.getY())
            x, y = tCity
            pCurrent = gc.getMap().plot(city.getX(), city.getY())

            # Absinthe: cities with We Love The King Day, your current and original capitals, and cities very close to your current capital won't revolt
            if (
                not city.isWeLoveTheKingDay()
                and not city.isCapital()
                and tCity != civilization(iPlayer).location.capital
            ):
                if pPlayer.getNumCities() > 0:  # this check is needed, otherwise game crashes
                    capital = gc.getPlayer(iPlayer).getCapitalCity()
                    iDistance = utils.calculateDistance(x, y, capital.getX(), capital.getY())
                    if iDistance > 3:
                        # Absinthe: Byzantine UP: cities in normal and core provinces won't go to the list
                        # bCollapseImmuneCity = utils.collapseImmuneCity(iPlayer, x, y)
                        bCollapseImmune = utils.collapseImmune(iPlayer)
                        iProvType = pPlayer.getProvinceType(city.getProvince())
                        # Absinthe: if forced revolt, all cities go into the list by default (apart from the Byzantine UP and the special ones above)
                        if bForce:
                            if iProvType >= ProvinceType.POTENTIAL.value:
                                if not bCollapseImmune:
                                    cityListInCore.append(city)
                            else:
                                cityListInNotCore.append(city)
                        # Absinthe: angry population, bad health, untolerated religion, no military garrison can add the city to the list a couple more times (per type)
                        # 			if the city is in a contested province, the city is added a couple more times by default, if in a foreign province, a lot more times
                        # Absinthe: bigger chance to choose the city if unhappy
                        if city.angryPopulation(0) > 0:
                            if iProvType >= ProvinceType.POTENTIAL.value:
                                if not bCollapseImmune:
                                    for i in range(2):
                                        cityListInCore.append(city)
                            else:
                                for i in range(4):
                                    cityListInNotCore.append(city)
                        # Absinthe: health issues do not cause city secession in core provinces for anyone
                        # 			also less chance from unhealth for cities in contested and foreign provinces
                        if city.goodHealth() - city.badHealth(False) < -1:
                            if iProvType < ProvinceType.POTENTIAL.value:
                                cityListInNotCore.append(city)
                        # Absinthe: also not a cause for secession in core provinces, no need to punish the player this much (and especially the AI) for using the civic
                        if city.getReligionBadHappiness() < 0:
                            if iProvType < ProvinceType.POTENTIAL.value:
                                for i in range(2):
                                    cityListInNotCore.append(city)
                        # Absinthe: no defensive units in the city increase chance
                        if city.getNoMilitaryPercentAnger() > 0:
                            if iProvType >= ProvinceType.POTENTIAL.value:
                                if not bCollapseImmune:
                                    cityListInCore.append(city)
                            else:
                                for i in range(2):
                                    cityListInNotCore.append(city)
                        # Absinthe: also add core cities if they have less than 40% own culture (and the civ doesn't have the Cultural Tolerance UP)
                        if iProvType >= ProvinceType.POTENTIAL.value:
                            if not bCollapseImmune and not gc.hasUP(
                                iPlayer, UniquePower.NO_UNHAPPINESS_WITH_FOREIGN_CULTURE.value
                            ):
                                if (
                                    city.countTotalCultureTimes100() > 0
                                    and (
                                        city.getCulture(iPlayer)
                                        * 10000
                                        / city.countTotalCultureTimes100()
                                    )
                                    < 40
                                ):
                                    cityListInCore.append(city)
                                elif (
                                    city.countTotalCultureTimes100() > 0
                                    and (
                                        city.getCulture(iPlayer)
                                        * 10000
                                        / city.countTotalCultureTimes100()
                                    )
                                    < 20
                                ):
                                    for i in range(2):
                                        cityListInCore.append(city)
                        # Absinthe: cities in outer and unstable provinces have chance by default, the number of times they are added is modified by the civ's own culture in the city
                        elif iProvType == ProvinceType.CONTESTED.value:
                            if (
                                city.countTotalCultureTimes100() > 0
                                and (
                                    city.getCulture(iPlayer)
                                    * 10000
                                    / city.countTotalCultureTimes100()
                                )
                                > 80
                            ):
                                cityListInNotCore.append(city)
                            elif (
                                city.countTotalCultureTimes100() > 0
                                and (
                                    city.getCulture(iPlayer)
                                    * 10000
                                    / city.countTotalCultureTimes100()
                                )
                                > 60
                            ):
                                for i in range(2):
                                    cityListInNotCore.append(city)
                            elif (
                                city.countTotalCultureTimes100() > 0
                                and (
                                    city.getCulture(iPlayer)
                                    * 10000
                                    / city.countTotalCultureTimes100()
                                )
                                > 40
                            ):
                                for i in range(3):
                                    cityListInNotCore.append(city)
                            else:
                                for i in range(4):
                                    cityListInNotCore.append(city)
                        elif iProvType == ProvinceType.NONE.value:
                            if (
                                city.countTotalCultureTimes100() > 0
                                and (
                                    city.getCulture(iPlayer)
                                    * 10000
                                    / city.countTotalCultureTimes100()
                                )
                                > 80
                            ):
                                for i in range(3):
                                    cityListInNotCore.append(city)
                            elif (
                                city.countTotalCultureTimes100() > 0
                                and (
                                    city.getCulture(iPlayer)
                                    * 10000
                                    / city.countTotalCultureTimes100()
                                )
                                > 60
                            ):
                                for i in range(5):
                                    cityListInNotCore.append(city)
                            elif (
                                city.countTotalCultureTimes100() > 0
                                and (
                                    city.getCulture(iPlayer)
                                    * 10000
                                    / city.countTotalCultureTimes100()
                                )
                                > 40
                            ):
                                for i in range(7):
                                    cityListInNotCore.append(city)
                            else:
                                for i in range(9):
                                    cityListInNotCore.append(city)

        if cityListInNotCore or cityListInCore:
            # Absinthe: we only choose among the core cities if there are no non-core ones
            # Absinthe: each city can appear multiple times in both lists
            if cityListInNotCore:
                splittingCity = choice(cityListInNotCore)
            else:
                splittingCity = choice(cityListInCore)

            # Absinthe: city goes to random independent
            iRndNum = rand(
                max(civilizations().independents().ids())
                - min(civilizations().independents().ids())
                + 1
            )
            iIndy = min(civilizations().independents().ids()) + iRndNum

            tCity = (splittingCity.getX(), splittingCity.getY())
            sCityName = splittingCity.getName()
            if iPlayer == human():
                CyInterface().addMessage(
                    iPlayer,
                    True,
                    MessageData.DURATION,
                    sCityName + " " + text("TXT_KEY_STABILITY_SECESSION"),
                    "",
                    0,
                    "",
                    ColorTypes(MessageData.ORANGE),
                    -1,
                    -1,
                    True,
                    True,
                )
            utils.cultureManager(tCity, 50, iIndy, iPlayer, False, True, True)
            utils.flipUnitsInCitySecession(tCity, iIndy, iPlayer)
            self.setTempFlippingCity(tCity)
            utils.flipCity(
                tCity, 0, 0, iIndy, [iPlayer]
            )  # by trade because by conquest may raze the city
            utils.flipUnitsInCityAfter(tCity, iIndy)

            # Absinthe: loosing a city to secession/revolt gives a small boost to stability, to avoid a city-revolting chain reaction
            pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)
            # Absinthe: AI declares war on the indy city right away
            teamPlayer = gc.getTeam(pPlayer.getTeam())
            iTeamIndy = gc.getPlayer(iIndy).getTeam()
            if not teamPlayer.isAtWar(iTeamIndy):
                teamPlayer.declareWar(iTeamIndy, False, WarPlanTypes.WARPLAN_LIMITED)

    def resurrection(self, iGameTurn, iDeadCiv):
        if iDeadCiv == -1:
            iDeadCiv = self.findCivToResurect(iGameTurn, 0, -1)
        else:
            iDeadCiv = self.findCivToResurect(iGameTurn, 1, iDeadCiv)  # For special re-spawn
        if iDeadCiv > -1:
            self.suppressResurection(iDeadCiv)

    def findCivToResurect(self, iGameTurn, bSpecialRespawn, iDeadCiv):
        if bSpecialRespawn:
            iMinNumCities = 1
        else:
            iMinNumCities = 2

        iRndnum = rand(civilizations().majors().len())
        for j in civilizations().majors().ids():
            if not bSpecialRespawn:
                iDeadCiv = (j + iRndnum) % civilizations().majors().len()
            else:
                iDeadCiv = iDeadCiv  # We want a specific civ for special re-spawn
            cityList = []
            if (
                not gc.getPlayer(iDeadCiv).isAlive()
                and iGameTurn > civilization(iDeadCiv).date.birth + 25
                and iGameTurn > utils.getLastTurnAlive(iDeadCiv) + 10
            ):  # Sedna17: Allow re-spawns only 10 turns after death and 25 turns after birth
                tile_min = civilization(iDeadCiv).location.area.normal.tile_min
                tile_max = civilization(iDeadCiv).location.area.normal.tile_max

                for tPlot in utils.getPlotList(tile_min, tile_max):
                    x, y = tPlot
                    if tPlot in civilization(iDeadCiv).location.area.normal.exception_tiles:
                        continue
                    plot = gc.getMap().plot(x, y)
                    if plot.isCity():
                        city = plot.getPlotCity()
                        iOwner = city.getOwner()
                        if (
                            iOwner >= civilizations().majors().len()
                        ):  # if iOwner in [Civ.INDEPENDENT.value, Civ.INDEPENDENT_2.value, Civ.BARBARIAN.value]: #remove in vanilla
                            cityList.append(tPlot)
                        else:
                            iMinNumCitiesOwner = 3
                            iOwnerStability = player(iOwner).getStability()
                            if not gc.getPlayer(iOwner).isHuman():
                                iMinNumCitiesOwner = 2
                                iOwnerStability -= 5
                            if gc.getPlayer(iOwner).getNumCities() >= iMinNumCitiesOwner:
                                if iOwnerStability < -5:
                                    if not city.isWeLoveTheKingDay() and not city.isCapital():
                                        cityList.append(tPlot)
                                elif iOwnerStability < 0:
                                    if (
                                        not city.isWeLoveTheKingDay()
                                        and not city.isCapital()
                                        and tPlot != civilization(iOwner).location.capital
                                    ):
                                        if (
                                            gc.getPlayer(iOwner).getNumCities() > 0
                                        ):  # this check is needed, otherwise game crashes
                                            capital = gc.getPlayer(iOwner).getCapitalCity()
                                            iDistance = utils.calculateDistance(
                                                x, y, capital.getX(), capital.getY()
                                            )
                                            if (
                                                (
                                                    iDistance >= 6
                                                    and gc.getPlayer(iOwner).getNumCities() >= 4
                                                )
                                                or city.angryPopulation(0) > 0
                                                or city.goodHealth() - city.badHealth(False) < -1
                                                or city.getReligionBadHappiness() < 0
                                                or city.getLargestCityHappiness() < 0
                                                or city.getHurryAngerModifier() > 0
                                                or city.getNoMilitaryPercentAnger() > 0
                                            ):
                                                cityList.append(tPlot)
                                if (
                                    not bSpecialRespawn
                                    and iOwnerStability < 10
                                    and (tPlot == civilization(iDeadCiv).location.capital)
                                    and tPlot not in cityList
                                ):
                                    cityList.append(tPlot)
                if len(cityList) >= iMinNumCities:
                    if bSpecialRespawn or percentage_chance(
                        civilization(iDeadCiv).location.respawning_threshold, strict=True
                    ):
                        self.setRebelCities(cityList)
                        self.setRebelCiv(iDeadCiv)  # for popup and CollapseCapitals()
                        return iDeadCiv
        return -1

    def suppressResurection(self, iDeadCiv):
        lSuppressList = self.getRebelSuppress()
        lCityList = self.getRebelCities()
        lCityCount = [0] * civilizations().majors().len()

        for (x, y) in lCityList:
            iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
            if iOwner < civilizations().majors().len():
                lCityCount[iOwner] += 1

        iHuman = human()
        for iCiv in civilizations().majors().ids():
            # Absinthe: have to reset the suppress values
            lSuppressList[iCiv] = 0
            if iCiv != iHuman:
                if lCityCount[iCiv] > 0:
                    # Absinthe: for the AI there is 30% chance that the actual respawn does not happen (under these suppress situations), only some revolt in the corresponding cities
                    if percentage_chance(30, strict=True):
                        lSuppressList[iCiv] = 1
                        for (x, y) in lCityList:
                            pCity = gc.getMap().plot(x, y).getPlotCity()
                            if pCity.getOwner() == iCiv:
                                pCity.changeOccupationTimer(1)
                                pCity.changeHurryAngerTimer(10)

        self.setRebelSuppress(lSuppressList)

        if lCityCount[iHuman] > 0:
            self.rebellionPopup(iDeadCiv, lCityCount[iHuman])
        else:
            self.resurectCiv(iDeadCiv)

    def resurectCiv(self, iDeadCiv):
        lCityList = self.getRebelCities()
        lSuppressList = self.getRebelSuppress()
        bSuppressed = True
        iHuman = human()
        lCityCount = [0] * civilizations().majors().len()
        for (x, y) in lCityList:
            iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
            if iOwner < civilizations().majors().len():
                lCityCount[iOwner] += 1

        # Absinthe: if any of the AI civs didn't manage to suppress it, there is resurrection
        for iCiv in civilizations().majors().ids():
            if iCiv != iHuman and lCityCount[iCiv] > 0 and lSuppressList[iCiv] == 0:
                bSuppressed = False
        if lCityCount[iHuman] > 0:
            # Absinthe: if the human player didn't choose any suppress options or didn't succeed in it (so it has 0, 2 or 4 in the lSuppressList), there is resurrection
            if lSuppressList[iHuman] in [0, 2, 4]:
                bSuppressed = False
            # Absinthe: if the human player managed to suppress it, message about it
            else:
                CyInterface().addMessage(
                    iHuman,
                    True,
                    MessageData.DURATION,
                    text("TXT_KEY_SUPPRESSED_RESURRECTION"),
                    "",
                    0,
                    "",
                    ColorTypes(MessageData.GREEN),
                    -1,
                    -1,
                    True,
                    True,
                )
        # Absinthe: if neither of the above happened, so everyone managed to suppress it, no resurrection
        if bSuppressed:
            return

        pDeadCiv = gc.getPlayer(iDeadCiv)
        teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())

        # Absinthe: respawn status
        pDeadCiv.setRespawnedAlive(True)
        pDeadCiv.setEverRespawned(
            True
        )  # needed for first turn vassalization and peace status fixes

        # Absinthe: store the turn of the latest respawn for each civ
        iGameTurn = turn()
        utils.setLastRespawnTurn(iDeadCiv, iGameTurn)

        # Absinthe: update province status before the cities are flipped, so potential provinces will update if there are cities in them
        self.pm.onRespawn(
            iDeadCiv
        )  # Absinthe: resetting the original potential provinces, and adding special province changes on respawn (Cordoba)

        # Absinthe: we shouldn't get a previous leader on respawn - would be changed to a newer one in a couple turns anyway
        # 			instead we have a random chance to remain with the leader before the collapse, or to switch to the next one
        leaders = civilization(iDeadCiv).leaders.late
        if leaders:
            # no change if we are already at the last leader
            # for iLeader in range(len(tLeaderCiv) - 1):
            for leader in leaders[:-1]:
                if pDeadCiv.getLeader() == leader[0].value:
                    if percentage_chance(60, strict=True):
                        pDeadCiv.setLeader(leader[0].value)
                    break

        for iCiv in civilizations().majors().ids():
            if iCiv != iDeadCiv:
                if teamDeadCiv.isAtWar(iCiv):
                    teamDeadCiv.makePeace(iCiv)
        self.setNumCities(iDeadCiv, 0)  # reset collapse condition

        # Absinthe: reset vassalage and update dynamic civ names
        for iOtherCiv in civilizations().majors().ids():
            if iOtherCiv != iDeadCiv:
                if teamDeadCiv.isVassal(iOtherCiv) or gc.getTeam(
                    gc.getPlayer(iOtherCiv).getTeam()
                ).isVassal(iDeadCiv):
                    teamDeadCiv.freeVassal(iOtherCiv)
                    gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).freeVassal(iDeadCiv)
                    gc.getPlayer(iOtherCiv).processCivNames()
                    gc.getPlayer(iDeadCiv).processCivNames()

        # Absinthe: no vassalization in the first 10 turns after resurrection?

        iNewUnits = 2
        if self.getLatestRebellionTurn(iDeadCiv) > 0:
            iNewUnits = 4
        self.setLatestRebellionTurn(iDeadCiv, turn())
        bHuman = False
        for (x, y) in lCityList:
            if gc.getMap().plot(x, y).getPlotCity().getOwner() == iHuman:
                bHuman = True
                break

        ownersList = []
        bAlreadyVassal = False
        for tCity in lCityList:
            pCity = gc.getMap().plot(tCity[0], tCity[1]).getPlotCity()
            iOwner = pCity.getOwner()
            teamOwner = gc.getTeam(gc.getPlayer(iOwner).getTeam())
            bOwnerVassal = teamOwner.isAVassal()
            bOwnerHumanVassal = teamOwner.isVassal(iHuman)

            if iOwner >= civilizations().majors().len():
                utils.cultureManager(tCity, 100, iDeadCiv, iOwner, False, True, True)
                utils.flipUnitsInCityBefore(tCity, iDeadCiv, iOwner)
                self.setTempFlippingCity(tCity)
                utils.flipCity(tCity, 0, 0, iDeadCiv, [iOwner])
                utils.flipUnitsInCityAfter(tCity, iOwner)
                utils.flipUnitsInArea(
                    (tCity[0] - 2, tCity[1] - 2),
                    (tCity[0] + 2, tCity[1] + 2),
                    iDeadCiv,
                    iOwner,
                    True,
                    False,
                )
            else:
                if lSuppressList[iOwner] in [0, 2, 4]:
                    utils.cultureManager(tCity, 50, iDeadCiv, iOwner, False, True, True)
                    utils.pushOutGarrisons(tCity, iOwner)
                    utils.relocateSeaGarrisons(tCity, iOwner)
                    self.setTempFlippingCity(tCity)
                    utils.flipCity(
                        tCity, 0, 0, iDeadCiv, [iOwner]
                    )  # by trade because by conquest may raze the city
                    utils.createGarrisons(tCity, iDeadCiv, iNewUnits)

                # 3Miro: indent to make part of the else on the if statement, otherwise one can make peace with the Barbs
                bAtWar = False  # AI won't vassalise if another owner has declared war; on the other hand, it won't declare war if another one has vassalised
                if (
                    iOwner != iHuman
                    and iOwner not in ownersList
                    and iOwner != iDeadCiv
                    and lSuppressList[iOwner] == 0
                ):  # declare war or peace only once - the 3rd condition is obvious but "vassal of themselves" was happening
                    rndNum = percentage()
                    if (
                        rndNum >= civilization(iOwner).ai.stop_birth_threshold
                        and not bOwnerHumanVassal
                        and not bAlreadyVassal
                    ):  # if bOwnerHumanVassal is True, it will skip to the 3rd condition, as bOwnerVassal is True as well
                        if not teamOwner.isAtWar(iDeadCiv):
                            teamOwner.declareWar(iDeadCiv, False, -1)
                        bAtWar = True
                    # Absinthe: do we really want to auto-vassal them on respawn? why?
                    # 			set it to 0 from 60 temporarily (so it's never True), as a quick fix until the mechanics are revised
                    elif rndNum <= 0 - (civilization(iOwner).ai.stop_birth_threshold / 2):
                        if teamOwner.isAtWar(iDeadCiv):
                            teamOwner.makePeace(iDeadCiv)
                        if (
                            not bAlreadyVassal and not bHuman and not bOwnerVassal and not bAtWar
                        ):  # bHuman == False cos otherwise human player can be deceived to declare war without knowing the new master
                            gc.getTeam(gc.getPlayer(iDeadCiv).getTeam()).setVassal(
                                iOwner, True, False
                            )
                            gc.getPlayer(
                                iOwner
                            ).processCivNames()  # setVassal already updates DCN for iDeadCiv
                            bAlreadyVassal = True
                    else:
                        if teamOwner.isAtWar(iDeadCiv):
                            teamOwner.makePeace(iDeadCiv)
                    ownersList.append(iOwner)
                    for iTech in range(len(Technology)):
                        if teamOwner.isHasTech(iTech):
                            teamDeadCiv.setHasTech(iTech, True, iDeadCiv, False, False)

        # all techs added from minor civs
        for iTech in range(len(Technology)):
            if (
                team(Civ.BARBARIAN).isHasTech(iTech)
                or team(Civ.INDEPENDENT).isHasTech(iTech)
                or team(Civ.INDEPENDENT_2).isHasTech(iTech)
                or team(Civ.INDEPENDENT_3).isHasTech(iTech)
                or team(Civ.INDEPENDENT_4).isHasTech(iTech)
            ):
                teamDeadCiv.setHasTech(iTech, True, iDeadCiv, False, False)

        self.moveBackCapital(iDeadCiv)

        if player().isExisting():
            CyInterface().addMessage(
                iHuman,
                True,
                MessageData.DURATION,
                (
                    CyTranslator().getText(
                        "TXT_KEY_INDEPENDENCE_TEXT", (pDeadCiv.getCivilizationAdjectiveKey(),)
                    )
                ),
                "",
                0,
                "",
                ColorTypes(MessageData.DARK_PINK),
                -1,
                -1,
                True,
                True,
            )
        if lSuppressList[iHuman] in [2, 3, 4]:
            if not gc.getTeam(gc.getPlayer(iHuman).getTeam()).isAtWar(iDeadCiv):
                gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iDeadCiv, False, -1)
        else:
            if gc.getTeam(gc.getPlayer(iHuman).getTeam()).isAtWar(iDeadCiv):
                gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iDeadCiv)

        # Absinthe: the new civs start as slightly stable
        pDeadCiv.changeStabilityBase(
            StabilityCategory.CITIES.value,
            -pDeadCiv.getStabilityBase(StabilityCategory.CITIES.value),
        )
        pDeadCiv.changeStabilityBase(
            StabilityCategory.CIVICS.value,
            -pDeadCiv.getStabilityBase(StabilityCategory.CIVICS.value),
        )
        pDeadCiv.changeStabilityBase(
            StabilityCategory.ECONOMY.value,
            -pDeadCiv.getStabilityBase(StabilityCategory.ECONOMY.value),
        )
        pDeadCiv.changeStabilityBase(
            StabilityCategory.EXPANSION.value,
            -pDeadCiv.getStabilityBase(StabilityCategory.EXPANSION.value),
        )
        pDeadCiv.changeStabilityBase(StabilityCategory.EXPANSION.value, 5)

        # Absinthe: refresh dynamic civ name for the new civ
        pDeadCiv.processCivNames()

        utils.setPlagueCountdown(iDeadCiv, -10)
        utils.clearPlague(iDeadCiv)
        self.convertBackCulture(iDeadCiv)

        # Absinthe: alive status is now updated right on respawn, otherwise it would only update on the beginning of the next turn
        pDeadCiv.setAlive(True)

    def moveBackCapital(self, iCiv):
        cityList = utils.getCityList(iCiv)
        tiles = civilization(iCiv).location.get(
            lambda c: c.new_capital, [civilization(iCiv).location.capital]
        )

        # TODO: remove for/else implementation
        for tile in tiles:
            plot = gc.getMap().plot(*tile)
            if plot.isCity():
                newCapital = plot.getPlotCity()
                if newCapital.getOwner() == iCiv:
                    if not newCapital.hasBuilding(Building.PALACE.value):
                        for city in cityList:
                            city.setHasRealBuilding((Building.PALACE.value), False)
                        newCapital.setHasRealBuilding((Building.PALACE.value), True)
                        self.makeResurectionUnits(iCiv, newCapital.getX(), newCapital.getY())
        else:
            iMaxValue = 0
            bestCity = None
            for loopCity in cityList:
                # loopCity.AI_cityValue() doesn't work as area AI types aren't updated yet
                loopValue = (
                    max(0, 500 - loopCity.getGameTurnFounded()) + loopCity.getPopulation() * 10
                )
                if loopValue > iMaxValue:
                    iMaxValue = loopValue
                    bestCity = loopCity
            if bestCity is not None:
                for loopCity in cityList:
                    if loopCity != bestCity:
                        loopCity.setHasRealBuilding((Building.PALACE.value), False)
                bestCity.setHasRealBuilding((Building.PALACE.value), True)
                self.makeResurectionUnits(iCiv, bestCity.getX(), bestCity.getY())

    def makeResurectionUnits(self, iPlayer, iX, iY):
        if iPlayer == Civ.CORDOBA.value:
            make_units(Civ.CORDOBA, Unit.SETTLER, (iX, iY), 2)
            make_units(Civ.CORDOBA, Unit.CROSSBOWMAN, (iX, iY), 2)
            make_unit(Civ.CORDOBA, Unit.ISLAMIC_MISSIONARY, (iX, iY))

    def convertBackCulture(self, iCiv):
        # 3Miro: same as Normal Areas in Resurrection
        # Sedna17: restored to be normal areas, not core
        tile_min = civilization(iCiv).location.area.normal.tile_min
        tile_max = civilization(iCiv).location.area.normal.tile_max
        # collect all the cities in the region
        for (x, y) in utils.getPlotList(tile_min, tile_max):
            pCurrent = gc.getMap().plot(x, y)
            if pCurrent.isCity():
                for (ix, iy) in utils.surroundingPlots((x, y)):
                    pCityArea = gc.getMap().plot(ix, iy)
                    iCivCulture = pCityArea.getCulture(iCiv)
                    iLoopCivCulture = 0
                    for civ in civilizations().minors().ids():
                        iLoopCivCulture += pCityArea.getCulture(civ)
                        pCityArea.setCulture(civ, 0, True)
                    pCityArea.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

                city = pCurrent.getPlotCity()
                iCivCulture = city.getCulture(iCiv)
                iLoopCivCulture = 0
                for civ in civilizations().minors().ids():
                    iLoopCivCulture += pCityArea.getCulture(civ)
                    pCityArea.setCulture(civ, 0, True)
                city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

    def initBirth(self, iCurrentTurn, iBirthYear, iCiv):
        iHuman = human()
        if iCurrentTurn == iBirthYear - 1 + self.getSpawnDelay(iCiv) + self.getFlipsDelay(iCiv):
            tCapital = civilization(iCiv).location.capital
            core_tile_min = civilization(iCiv).location.area.core.tile_min
            core_tile_max = civilization(iCiv).location.area.core.tile_max
            broader_tile_min = civilization(iCiv).location.area.broader.tile_min
            broader_tile_max = civilization(iCiv).location.area.broader.tile_max
            if self.getFlipsDelay(iCiv) == 0:  # city hasn't already been founded

                # Absinthe: for the human player, kill all foreign units on the capital plot - this probably fixes a couple instances of the -1 turn autoplay bug
                if iCiv == iHuman:
                    killPlot = gc.getMap().plot(tCapital[0], tCapital[1])
                    iNumUnitsInAPlot = killPlot.getNumUnits()
                    if iNumUnitsInAPlot > 0:
                        iSkippedUnit = 0
                        for i in range(iNumUnitsInAPlot):
                            unit = killPlot.getUnit(iSkippedUnit)
                            if unit.getOwner() != iCiv:
                                unit.kill(False, Civ.BARBARIAN.value)
                            else:
                                iSkippedUnit += 1

                # Absinthe: if the plot is owned by a civ, bDeleteEverything becomes True unless there is a human city in the 1+8 neighbour plots.
                bDeleteEverything = False
                if gc.getMap().plot(tCapital[0], tCapital[1]).isOwned():
                    if iCiv == iHuman or not gc.getPlayer(iHuman).isAlive():
                        bDeleteEverything = True
                    else:
                        bDeleteEverything = True
                        for (x, y) in utils.surroundingPlots(tCapital):
                            plot = gc.getMap().plot(x, y)
                            if plot.isCity() and plot.getPlotCity().getOwner() == iHuman:
                                bDeleteEverything = False
                                break

                if not gc.getMap().plot(tCapital[0], tCapital[1]).isOwned():
                    self.birthInFreeRegion(iCiv, tCapital, core_tile_min, core_tile_max)
                elif bDeleteEverything:
                    self.setDeleteMode(0, iCiv)
                    # Absinthe: kill off units near the starting plot
                    utils.killAllUnitsInArea(
                        (tCapital[0] - 1, tCapital[1] - 1), (tCapital[0] + 1, tCapital[1] + 1)
                    )
                    for (x, y) in utils.surroundingPlots(tCapital):
                        plot = gc.getMap().plot(x, y)
                        if plot.isCity():
                            plot.eraseAIDevelopment()  # new function, similar to erase but won't delete rivers, resources and features
                        for civ in civilizations().ids():
                            if iCiv != civ:
                                plot.setCulture(civ, 0, True)
                        plot.setOwner(-1)
                    self.birthInFreeRegion(iCiv, tCapital, core_tile_min, core_tile_max)
                else:
                    self.birthInForeignBorders(
                        iCiv,
                        core_tile_min,
                        core_tile_max,
                        broader_tile_min,
                        broader_tile_max,
                        tCapital,
                    )
            else:
                self.birthInFreeRegion(iCiv, tCapital, core_tile_min, core_tile_max)

        # 3MiroCrusader modification. Crusaders cannot change nations.
        # Sedna17: Straight-up no switching within 40 turns of your birth
        if iCurrentTurn == iBirthYear + self.getSpawnDelay(iCiv):
            if (
                gc.getPlayer(iCiv).isAlive()
                and not self.getAlreadySwitched()
                and iCurrentTurn > civilization(iHuman).date.birth + 40
                and not gc.getPlayer(iHuman).getIsCrusader()
            ):
                self.newCivPopup(iCiv)

    def deleteMode(self, iCurrentPlayer):
        iCiv = self.getDeleteMode(0)
        tCapital = civilization(iCiv).location.capital
        if iCurrentPlayer == iCiv:
            for (x, y) in utils.surroundingPlots(tCapital, 2):
                plot = gc.getMap().plot(x, y)
                plot.setCulture(iCiv, 300, True)
            for (x, y) in utils.surroundingPlots(tCapital):
                plot = gc.getMap().plot(x, y)
                utils.convertPlotCulture(plot, iCiv, 100, True)
                if plot.getCulture(iCiv) < 3000:
                    plot.setCulture(
                        iCiv, 3000, True
                    )  # 2000 in vanilla/warlords, cos here Portugal is choked by Spanish culture
                plot.setOwner(iCiv)
            self.setDeleteMode(0, -1)
            return

        if iCurrentPlayer != iCiv - 1:
            return

        for (x, y) in utils.surroundingPlots(tCapital):
            plot = gc.getMap().plot(x, y)
            if plot.isOwned():
                for iLoopCiv in civilizations().ids():
                    if iLoopCiv != iCiv:
                        plot.setCulture(iLoopCiv, 0, True)
                    # else:
                    # 	if plot.getCulture(iCiv) < 4000:
                    # 		plot.setCulture(iCiv, 4000, True)
                # plot.setOwner(-1)
                plot.setOwner(iCiv)

        # Absinthe: what's this +-11? do we really want to move all flipped units in the initial turn to the starting plot??

    def birthInFreeRegion(self, iCiv, tCapital, tTopLeft, tBottomRight):
        startingPlot = gc.getMap().plot(tCapital[0], tCapital[1])
        if self.getFlipsDelay(iCiv) == 0:
            iFlipsDelay = self.getFlipsDelay(iCiv) + 2

            if iFlipsDelay > 0:
                # Absinthe: kill off units near the starting plot
                utils.killAllUnitsInArea(
                    (tCapital[0] - 1, tCapital[1] - 1), (tCapital[0] + 1, tCapital[1] + 1)
                )
                self.createStartingUnits(iCiv, (tCapital[0], tCapital[1]))
                # Absinthe: there was another mistake here with barbarian and indy unit flips...
                # 			we don't simply want to check an area based on distance from capital, as it might lead out from the actual spawn area
                # 			so we only check plots which are in the core area: in 4 distance for barb units, 2 distance for indies
                lPlotBarbFlip = []
                lPlotIndyFlip = []
                # if inside the core rectangle and extra plots, and in 4 (barb) or 2 (indy) distance from the starting plot, append to barb or indy flip zone

                lPlots = (
                    utils.getPlotList(tTopLeft, tBottomRight)
                    + civilization(iCiv).location.area.core.additional_tiles
                )
                lSurroundingPlots4 = utils.surroundingPlots(tCapital, 4)
                lSurroundingPlots2 = utils.surroundingPlots(tCapital, 2)
                for tPlot in lPlots:
                    if tPlot in lSurroundingPlots2:
                        lPlotIndyFlip.append(tPlot)
                        lPlotBarbFlip.append(tPlot)
                    elif tPlot in lSurroundingPlots4:
                        lPlotBarbFlip.append(tPlot)
                # remaining barbs in the region: killed for the human player, flipped for the AI
                if iCiv == human():
                    utils.killUnitsInPlots(lPlotBarbFlip, Civ.BARBARIAN.value)
                else:
                    utils.flipUnitsInPlots(lPlotBarbFlip, iCiv, Civ.BARBARIAN.value, True, True)
                for iIndyCiv in civilizations().independents().ids():
                    # remaining independents in the region: killed for the human player, flipped for the AI
                    if iCiv == human():
                        utils.killUnitsInPlots(lPlotIndyFlip, iIndyCiv)
                    else:
                        utils.flipUnitsInPlots(lPlotIndyFlip, iCiv, iIndyCiv, True, False)
                self.assignTechs(iCiv)
                utils.setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
                utils.clearPlague(iCiv)
                self.setFlipsDelay(iCiv, iFlipsDelay)  # save

        else:  # starting units have already been placed, now the second part
            iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(
                iCiv, tTopLeft, tBottomRight
            )
            self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)
            if iCiv != human():
                utils.flipUnitsInArea(
                    tTopLeft, tBottomRight, iCiv, Civ.BARBARIAN.value, False, True
                )  # remaining barbs in the region now belong to the new civ
                utils.flipUnitsInPlots(
                    civilization(iCiv).location.area.core.additional_tiles,
                    iCiv,
                    Civ.BARBARIAN.value,
                    False,
                    True,
                )  # remaining barbs in the region now belong to the new civ
            for iIndyCiv in civilizations().independents().ids():
                if iCiv != human():
                    utils.flipUnitsInArea(
                        tTopLeft, tBottomRight, iCiv, iIndyCiv, False, False
                    )  # remaining independents in the region now belong to the new civ
                    utils.flipUnitsInPlots(
                        civilization(iCiv).location.area.core.additional_tiles,
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
                self.create_starting_workers(iCiv, (capital.getX(), capital.getY()))
                if iCiv == Civ.OTTOMAN:
                    self.ottomanInvasion(iCiv, (77, 23))

            if iNumHumanCitiesToConvert > 0:
                self.flipPopup(iCiv, tTopLeft, tBottomRight)

    def birthInForeignBorders(
        self, iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight, tCapital
    ):
        iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(
            iCiv, tTopLeft, tBottomRight
        )
        self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)

        # now starting units must be placed
        if iNumAICitiesConverted > 0:
            # Absinthe: there is an issue that core area is not calculated correctly for flips, as the additional tiles in lExtraPlots are not checked here
            # 			so if all flipped cities are outside of the core area (they are in the "exceptions"), the civ will start without it's starting units and techs
            plotList = utils.squareSearch(tTopLeft, tBottomRight, utils.ownedCityPlots, iCiv)
            # Absinthe: add the exception plots
            for plot in civilization(iCiv).location.area.core.additional_tiles:
                plot = gc.getMap().plot(*plot)
                if plot.getOwner() == iCiv:
                    if plot.isCity():
                        plotList.append(plot)
            if plotList:
                plot = choice(plotList)
                self.createStartingUnits(iCiv, plot)
                self.assignTechs(iCiv)
                utils.setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
                utils.clearPlague(iCiv)
            utils.flipUnitsInArea(
                tTopLeft, tBottomRight, iCiv, Civ.BARBARIAN.value, False, True
            )  # remaining barbs in the region now belong to the new civ
            utils.flipUnitsInPlots(
                civilization(iCiv).location.area.core.additional_tiles,
                iCiv,
                Civ.BARBARIAN.value,
                False,
                True,
            )  # remaining barbs in the region now belong to the new civ
            for iIndyCiv in civilizations().independents().ids():
                utils.flipUnitsInArea(
                    tTopLeft, tBottomRight, iCiv, iIndyCiv, False, False
                )  # remaining independents in the region now belong to the new civ
                utils.flipUnitsInPlots(
                    civilization(iCiv).location.area.core.additional_tiles,
                    iCiv,
                    iIndyCiv,
                    False,
                    False,
                )  # remaining independents in the region now belong to the new civ

        else:
            # Absinthe: there is an issue that core area is not calculated correctly for flips, as the additional tiles in lExtraPlots are not checked here
            # 			so if all flipped cities are outside of the core area (they are in the "exceptions"), the civ will start without it's starting units and techs
            plotList = utils.squareSearch(tTopLeft, tBottomRight, utils.goodPlots, [])
            # Absinthe: add the exception plots
            for plot in civilization(iCiv).location.area.core.additional_tiles:
                plot = gc.getMap().plot(*plot)
                if (plot.isHills() or plot.isFlatlands()) and not plot.isImpassable():
                    if not plot.isUnit():
                        if plot.getTerrainType() not in [
                            Terrain.DESERT.value,
                            Terrain.TUNDRA.value,
                        ] and plot.getFeatureType() not in [
                            Feature.MARSH.value,
                            Feature.JUNGLE.value,
                        ]:
                            if plot.countTotalCulture() == 0:
                                plotList.append(plot)
            if plotList:
                plot = choice(plotList)
                self.createStartingUnits(iCiv, plot)
                self.assignTechs(iCiv)
                utils.setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
                utils.clearPlague(iCiv)
            else:
                plotList = utils.squareSearch(
                    tBroaderTopLeft, tBroaderBottomRight, utils.goodPlots, []
                )
                if plotList:
                    plot = choice(plotList)
                    self.createStartingUnits(iCiv, plot)
                    self.create_starting_workers(iCiv, plot)
                    if iCiv == Civ.OTTOMAN:
                        self.ottomanInvasion(iCiv, (77, 23))
                    self.assignTechs(iCiv)
                    utils.setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
                    utils.clearPlague(iCiv)
            utils.flipUnitsInArea(
                tTopLeft, tBottomRight, iCiv, Civ.BARBARIAN.value, True, True
            )  # remaining barbs in the region now belong to the new civ
            utils.flipUnitsInPlots(
                civilization(iCiv).location.area.core.additional_tiles,
                iCiv,
                Civ.BARBARIAN.value,
                True,
                True,
            )  # remaining barbs in the region now belong to the new civ
            for iIndyCiv in civilizations().independents().ids():
                utils.flipUnitsInArea(
                    tTopLeft, tBottomRight, iCiv, iIndyCiv, True, False
                )  # remaining independents in the region now belong to the new civ
                utils.flipUnitsInPlots(
                    civilization(iCiv).location.area.core.additional_tiles,
                    iCiv,
                    iIndyCiv,
                    True,
                    False,
                )  # remaining independents in the region now belong to the new civ

        if iNumHumanCitiesToConvert > 0:
            self.flipPopup(iCiv, tTopLeft, tBottomRight)

    def convertSurroundingCities(self, iCiv, tTopLeft, tBottomRight):
        iConvertedCitiesCount = 0
        iNumHumanCities = 0
        cityList = []
        self.setSpawnWar(0)
        pCiv = gc.getPlayer(iCiv)

        # collect all the cities in the spawn region
        lPlots = (
            utils.getPlotList(tTopLeft, tBottomRight)
            + civilization(iCiv).location.area.core.additional_tiles
        )
        for (x, y) in lPlots:
            plot = gc.getMap().plot(x, y)
            if plot.isCity():
                if plot.getPlotCity().getOwner() != iCiv:
                    cityList.append(plot.getPlotCity())

        # for each city
        if cityList:
            for loopCity in cityList:
                loopX = loopCity.getX()
                loopY = loopCity.getY()
                iHuman = human()
                iOwner = loopCity.getOwner()
                iCultureChange = 0  # if 0, no flip; if > 0, flip will occur with the value as variable for utils.CultureManager()

                if iOwner >= civilizations().majors().len():
                    iCultureChange = 100
                # case 2: human city
                elif iOwner == iHuman and not loopCity.isCapital():
                    if iNumHumanCities == 0:
                        iNumHumanCities += 1
                # case 3: other
                elif (
                    not loopCity.isCapital()
                ):  # 3Miro: this keeps crashing in the C++, makes no sense
                    if iConvertedCitiesCount < 6:  # there won't be more than 5 flips in the area
                        iCultureChange = 50
                        if turn() <= civilization(iCiv).date.birth + 5:  # if we're during a birth
                            rndNum = percentage()
                            # 3Miro: I don't know why the iOwner check is needed below, but the module crashes sometimes
                            if (
                                iOwner > -1
                                and iOwner < civilizations().majors().len()
                                and rndNum >= civilization(iOwner).ai.stop_birth_threshold
                            ):
                                pOwner = gc.getPlayer(iOwner)
                                if not gc.getTeam(pOwner.getTeam()).isAtWar(iCiv):
                                    gc.getTeam(pOwner.getTeam()).declareWar(iCiv, False, -1)
                                    if (
                                        pCiv.getNumCities() > 0
                                    ):  # this check is needed, otherwise game crashes
                                        if (
                                            pCiv.getCapitalCity().getX(),
                                            pCiv.getCapitalCity().getY(),
                                        ) != (-1, -1):
                                            self.createAdditionalUnits(
                                                iCiv,
                                                (
                                                    pCiv.getCapitalCity().getX(),
                                                    pCiv.getCapitalCity().getY(),
                                                ),
                                            )
                                        else:
                                            self.createAdditionalUnits(
                                                iCiv, civilization(iCiv).location.capital
                                            )

                if iCultureChange > 0:
                    utils.cultureManager(
                        (loopX, loopY), iCultureChange, iCiv, iOwner, True, False, False
                    )

                    utils.flipUnitsInCityBefore((loopX, loopY), iCiv, iOwner)
                    self.setTempFlippingCity(
                        (loopX, loopY)
                    )  # necessary for the (688379128, 0) bug
                    utils.flipCity((loopX, loopY), 0, 0, iCiv, [iOwner])
                    utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iCiv)

                    iConvertedCitiesCount += 1

        if iConvertedCitiesCount > 0:
            if gc.getPlayer(iCiv).isHuman():
                CyInterface().addMessage(
                    iCiv,
                    True,
                    MessageData.DURATION,
                    text("TXT_KEY_FLIP_TO_US"),
                    "",
                    0,
                    "",
                    ColorTypes(MessageData.GREEN),
                    -1,
                    -1,
                    True,
                    True,
                )
        return (iConvertedCitiesCount, iNumHumanCities)

    def convertSurroundingPlotCulture(self, iCiv, tTopLeft, tBottomRight):
        lPlots = (
            utils.getPlotList(tTopLeft, tBottomRight)
            + civilization(iCiv).location.area.core.additional_tiles
        )
        for (x, y) in lPlots:
            plot = gc.getMap().plot(x, y)
            if not plot.isCity():
                utils.convertPlotCulture(plot, iCiv, 100, False)

    def findSeaPlots(self, tCoords, iRange):
        """Searches a sea plot that isn't occupied by a unit within range of the starting coordinates"""
        # we can search inside other players territory, since all naval units can cross sea borders
        seaPlotList = []
        for (x, y) in utils.surroundingPlots(tCoords, iRange):
            plot = gc.getMap().plot(x, y)
            if plot.isWater() and not plot.isUnit():
                seaPlotList.append((x, y))
                # this is a good plot, so paint it and continue search
        if seaPlotList:
            return choice(seaPlotList)
        return None

    def giveColonists(self, iCiv, tBroaderAreaTL, tBroaderAreaBR):
        # 3Miro: Conquistador event
        pass

    def onFirstContact(self, iTeamX, iHasMetTeamY):
        # 3Miro: Conquistador event
        pass

    def getSpecialRespawn(
        self, iGameTurn
    ):  # Absinthe: only the first civ for which it is True is returned, so the order of the civs is very important here
        if self.canSpecialRespawn(Civ.FRANCE.value, iGameTurn, 12):
            # France united in it's modern borders, start of the Bourbon royal line
            if DateTurn.i1588AD < iGameTurn < DateTurn.i1700AD and iGameTurn % 5 == 3:
                return Civ.FRANCE.value
        if self.canSpecialRespawn(Civ.ARABIA.value, iGameTurn):
            # Saladin, Ayyubid Dynasty
            if DateTurn.i1080AD < iGameTurn < DateTurn.i1291AD and iGameTurn % 7 == 3:
                return Civ.ARABIA.value
        if self.canSpecialRespawn(Civ.BULGARIA.value, iGameTurn):
            # second Bulgarian Empire
            if DateTurn.i1080AD < iGameTurn < DateTurn.i1299AD and iGameTurn % 5 == 1:
                return Civ.BULGARIA.value
        if self.canSpecialRespawn(Civ.CORDOBA.value, iGameTurn):
            # special respawn as the Hafsid dynasty in North Africa
            if DateTurn.i1229AD < iGameTurn < DateTurn.i1540AD and iGameTurn % 5 == 3:
                return Civ.CORDOBA.value
        if self.canSpecialRespawn(Civ.BURGUNDY.value, iGameTurn, 20):
            # Burgundy in the 100 years war
            if DateTurn.i1336AD < iGameTurn < DateTurn.i1453AD and iGameTurn % 8 == 1:
                return Civ.BURGUNDY.value
        if self.canSpecialRespawn(Civ.PRUSSIA.value, iGameTurn):
            # respawn as the unified Prussia
            if iGameTurn > DateTurn.i1618AD and iGameTurn % 3 == 1:
                return Civ.PRUSSIA.value
        if self.canSpecialRespawn(Civ.HUNGARY.value, iGameTurn):
            # reconquest of Buda from the Ottomans
            if iGameTurn > DateTurn.i1680AD and iGameTurn % 6 == 2:
                return Civ.HUNGARY.value
        if self.canSpecialRespawn(Civ.CASTILE.value, iGameTurn, 25):
            # respawn as the Castile/Aragon Union
            if DateTurn.i1470AD < iGameTurn < DateTurn.i1580AD and iGameTurn % 5 == 0:
                return Civ.CASTILE.value
        if self.canSpecialRespawn(Civ.ENGLAND.value, iGameTurn, 12):
            # restoration of monarchy
            if iGameTurn > DateTurn.i1660AD and iGameTurn % 6 == 2:
                return Civ.ENGLAND.value
        if self.canSpecialRespawn(Civ.SCOTLAND.value, iGameTurn, 30):
            if iGameTurn <= DateTurn.i1600AD and iGameTurn % 6 == 3:
                return Civ.SCOTLAND.value
        if self.canSpecialRespawn(Civ.PORTUGAL.value, iGameTurn):
            # respawn to be around for colonies
            if DateTurn.i1431AD < iGameTurn < DateTurn.i1580AD and iGameTurn % 5 == 3:
                return Civ.PORTUGAL.value
        if self.canSpecialRespawn(Civ.AUSTRIA.value, iGameTurn):
            # increasing Habsburg influence in Hungary
            if DateTurn.i1526AD < iGameTurn < DateTurn.i1690AD and iGameTurn % 8 == 3:
                return Civ.AUSTRIA.value
        if self.canSpecialRespawn(Civ.KIEV.value, iGameTurn):
            # Cossack Hetmanate
            if DateTurn.i1620AD < iGameTurn < DateTurn.i1750AD and iGameTurn % 5 == 3:
                return Civ.KIEV.value
        if self.canSpecialRespawn(Civ.MOROCCO.value, iGameTurn):
            # Alaouite Dynasty
            if iGameTurn > DateTurn.i1631AD and iGameTurn % 8 == 7:
                return Civ.MOROCCO.value
        if self.canSpecialRespawn(Civ.ARAGON.value, iGameTurn):
            # Kingdom of Sicily
            if iGameTurn > DateTurn.i1700AD and iGameTurn % 8 == 7:
                return Civ.ARAGON.value
        if self.canSpecialRespawn(Civ.VENECIA.value, iGameTurn):
            if DateTurn.i1401AD < iGameTurn < DateTurn.i1571AD and iGameTurn % 8 == 7:
                return Civ.VENECIA.value
        if self.canSpecialRespawn(Civ.POLAND.value, iGameTurn):
            if DateTurn.i1410AD < iGameTurn < DateTurn.i1570AD and iGameTurn % 8 == 7:
                return Civ.POLAND.value
        if self.canSpecialRespawn(Civ.OTTOMAN.value, iGameTurn):
            # Mehmed II's conquests
            if DateTurn.i1453AD < iGameTurn < DateTurn.i1514AD and iGameTurn % 6 == 3:
                return Civ.OTTOMAN.value
        return -1

    def canSpecialRespawn(self, iPlayer, iGameTurn, iLastAliveInterval=10):
        pPlayer = gc.getPlayer(iPlayer)
        if pPlayer.isAlive():
            return False
        if pPlayer.getEverRespawned():
            return False
        if iGameTurn <= civilization(iPlayer).date.birth + 25:
            return False
        if iGameTurn <= (utils.getLastTurnAlive(iPlayer) + iLastAliveInterval):
            return False
        return True

    def initMinorBetrayal(self, iCiv):
        iHuman = human()
        plotList = utils.squareSearch(
            civilization(iCiv).location.area.core.tile_min,
            civilization(iCiv).location.area.core.tile_max,
            utils.outerInvasion,
            [],
        )
        if plotList:
            tPlot = choice(plotList)
            self.createAdditionalUnits(iCiv, tPlot)
            self.unitsBetrayal(
                iCiv,
                iHuman,
                civilization(iCiv).location.area.core.tile_min,
                civilization(iCiv).location.area.core.tile_max,
                tPlot,
            )

    def initBetrayal(self):
        iHuman = human()
        turnsLeft = self.getBetrayalTurns()
        plotList = utils.squareSearch(
            self.getTempTopLeft(), self.getTempBottomRight(), utils.outerInvasion, []
        )
        if not plotList:
            plotList = utils.squareSearch(
                self.getTempTopLeft(),
                self.getTempBottomRight(),
                utils.innerSpawn,
                [self.getOldCivFlip(), self.getNewCivFlip()],
            )
        if not plotList:
            plotList = utils.squareSearch(
                self.getTempTopLeft(),
                self.getTempBottomRight(),
                utils.forcedInvasion,
                [self.getOldCivFlip(), self.getNewCivFlip()],
            )
        if plotList:
            tPlot = choice(plotList)
            if turnsLeft == iBetrayalPeriod:
                self.createAdditionalUnits(self.getNewCivFlip(), tPlot)
            self.unitsBetrayal(
                self.getNewCivFlip(),
                self.getOldCivFlip(),
                self.getTempTopLeft(),
                self.getTempBottomRight(),
                tPlot,
            )
        self.setBetrayalTurns(turnsLeft - 1)

    def unitsBetrayal(self, iNewOwner, iOldOwner, tTopLeft, tBottomRight, tPlot):
        if gc.getPlayer(self.getOldCivFlip()).isHuman():
            CyInterface().addMessage(
                self.getOldCivFlip(),
                False,
                MessageData.DURATION,
                text("TXT_KEY_FLIP_BETRAYAL"),
                "",
                0,
                "",
                ColorTypes(MessageData.RED),
                -1,
                -1,
                True,
                True,
            )
        elif gc.getPlayer(self.getNewCivFlip()).isHuman():
            CyInterface().addMessage(
                self.getNewCivFlip(),
                False,
                MessageData.DURATION,
                text("TXT_KEY_FLIP_BETRAYAL_NEW"),
                "",
                0,
                "",
                ColorTypes(MessageData.GREEN),
                -1,
                -1,
                True,
                True,
            )
        for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
            killPlot = gc.getMap().plot(x, y)
            iNumUnitsInAPlot = killPlot.getNumUnits()
            if iNumUnitsInAPlot > 0:
                for i in range(iNumUnitsInAPlot):
                    unit = killPlot.getUnit(i)
                    if unit.getOwner() == iOldOwner:
                        if percentage_chance(iBetrayalThreshold, reverse=True):
                            if unit.getDomainType() == DomainTypes.DOMAIN_LAND:  # land unit
                                iUnitType = unit.getUnitType()
                                unit.kill(False, iNewOwner)
                                make_unit(iNewOwner, iUnitType, tPlot)
                                i = i - 1

    def createAdditionalUnits(self, iCiv, tPlot):
        # additional starting units if someone declares war on the civ during birth
        units = civilization(iCiv).initial.get("additional_units")
        if units is not None:
            if iCiv != human():
                for unit, number in units.get(PlayerType.AI, {}).items():
                    make_units(iCiv, unit, tPlot, number)
            else:
                for unit, number in units.get(PlayerType.HUMAN, {}).items():
                    make_units(iCiv, unit, tPlot, number)

    def createStartingUnits(self, iCiv, tPlot):
        # set the provinces
        self.pm.onSpawn(iCiv)

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

        if iCiv == Civ.VENECIA.value:
            tSeaPlot = self.findSeaPlots((57, 35), 2)
            if tSeaPlot:
                make_unit(iCiv, Unit.WORKBOAT, tSeaPlot)
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
                make_unit(iCiv, Unit.SETTLER, tSeaPlot)
                make_unit(iCiv, Unit.ARCHER, tSeaPlot)
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
                make_unit(iCiv, Unit.SETTLER, tSeaPlot)
                make_unit(iCiv, Unit.SPEARMAN, tSeaPlot)
        elif iCiv == Civ.NORWAY.value:
            tSeaPlot = self.findSeaPlots(tPlot, 2)
            if tSeaPlot:
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
                make_unit(iCiv, Unit.SETTLER, tSeaPlot)
                make_unit(iCiv, Unit.ARCHER, tSeaPlot)
        elif iCiv == Civ.DENMARK.value:
            tSeaPlot = self.findSeaPlots((60, 57), 2)
            if tSeaPlot:
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
                make_unit(iCiv, Unit.SETTLER, tSeaPlot)
                make_unit(iCiv, Unit.CROSSBOWMAN, tSeaPlot)
                make_unit(iCiv, Unit.SETTLER, tSeaPlot)
                make_unit(iCiv, Unit.CROSSBOWMAN, tSeaPlot)
        elif iCiv == Civ.GENOA.value:
            tSeaPlot = self.findSeaPlots(tPlot, 2)
            if tSeaPlot:
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
                make_unit(iCiv, Unit.WAR_GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
                make_unit(iCiv, Unit.SETTLER, tSeaPlot)
                make_unit(iCiv, Unit.CROSSBOWMAN, tSeaPlot)
                make_unit(iCiv, Unit.WORKBOAT, tSeaPlot)
        elif iCiv == Civ.ENGLAND.value:
            tSeaPlot = self.findSeaPlots((43, 53), 1)
            if tSeaPlot:
                make_unit(iCiv, Unit.GALLEY, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
                make_unit(iCiv, Unit.WAR_GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
        elif iCiv == Civ.ARAGON.value:
            tSeaPlot = self.findSeaPlots((42, 29), 1)
            if tSeaPlot:
                make_units(iCiv, Unit.WAR_GALLEY, tSeaPlot, 2, UnitAITypes.UNITAI_ESCORT_SEA)
                make_unit(iCiv, Unit.COGGE, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
                make_unit(iCiv, Unit.SETTLER, tSeaPlot)
                make_unit(iCiv, Unit.CROSSBOWMAN, tSeaPlot)
                make_unit(iCiv, Unit.WORKBOAT, tSeaPlot)
        elif iCiv == Civ.SWEDEN.value:
            tSeaPlot = self.findSeaPlots((69, 65), 2)
            if tSeaPlot:
                make_unit(iCiv, Unit.WORKBOAT, tSeaPlot)
                make_unit(iCiv, Unit.WAR_GALLEY, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
                make_units(iCiv, Unit.COGGE, tSeaPlot, 2, UnitAITypes.UNITAI_SETTLER_SEA)
                make_unit(iCiv, Unit.SETTLER, tSeaPlot)
                make_unit(iCiv, Unit.ARBALEST, tSeaPlot)
        elif iCiv == Civ.DUTCH.value:
            tSeaPlot = self.findSeaPlots(tPlot, 2)
            if tSeaPlot:
                make_units(iCiv, Unit.WORKBOAT, tSeaPlot, 2)
                make_units(iCiv, Unit.GALLEON, tSeaPlot, 2)

        self.showArea(iCiv)
        self.initContact(iCiv)

    def create1200ADstartingUnits(self):
        iHuman = human()
        if (
            civilization(iHuman).date.birth > DateTurn.i1200AD
        ):  # so iSweden, iPrussia, iLithuania, iAustria, iTurkey, iMoscow, iDutch
            tStart = civilization(iHuman).location.capital

            # Absinthe: changes in the unit positions, in order to prohibit these contacts in 1200AD
            if iHuman == Civ.SWEDEN:  # contact with Denmark
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.SWEDEN][0] - 2,
                    CIV_CAPITAL_LOCATIONS[Civ.SWEDEN][1] + 2,
                )
            elif iHuman == Civ.PRUSSIA:  # contact with Poland
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.PRUSSIA][0] + 1,
                    CIV_CAPITAL_LOCATIONS[Civ.PRUSSIA][1] + 1,
                )
            elif iHuman == Civ.LITHUANIA:  # contact with Kiev
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.LITHUANIA][0] - 2,
                    CIV_CAPITAL_LOCATIONS[Civ.LITHUANIA][1],
                )
            elif iHuman == Civ.AUSTRIA:  # contact with Germany and Hungary
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.AUSTRIA][0] - 3,
                    CIV_CAPITAL_LOCATIONS[Civ.AUSTRIA][1] - 1,
                )
            elif iHuman == Civ.OTTOMAN:  # contact with Byzantium
                tStart = (98, 18)

            make_unit(iHuman, Unit.SETTLER, tStart)
            make_unit(iHuman, Unit.MACEMAN, tStart)

    def ottomanInvasion(self, iCiv, tPlot):
        # Absinthe: second Ottoman spawn stack may stay, although they now spawn in Gallipoli in the first place (one plot SE)
        make_units(iCiv, Unit.LONGBOWMAN, tPlot, 2)
        make_units(iCiv, Unit.MACEMAN, tPlot, 2)
        make_units(iCiv, Unit.KNIGHT, tPlot, 3)
        make_units(iCiv, Unit.TURKEY_GREAT_BOMBARD, tPlot, 2)
        make_units(iCiv, Unit.ISLAMIC_MISSIONARY, tPlot, 2)

    def create500ADstartingUnits(self):
        make_units(Civ.FRANCE, Unit.SETTLER, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 3)
        make_units(Civ.FRANCE, Unit.ARCHER, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 4)
        make_units(Civ.FRANCE, Unit.AXEMAN, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 5)
        make_unit(Civ.FRANCE, Unit.SCOUT, CIV_CAPITAL_LOCATIONS[Civ.FRANCE])
        make_units(Civ.FRANCE, Unit.WORKER, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 2)
        make_units(Civ.FRANCE, Unit.CATHOLIC_MISSIONARY, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 2)

        iHuman = human()
        if (
            civilization(iHuman).date.birth > DateTurn.i500AD
        ):  # so everyone apart from Byzantium and France
            tStart = CIV_CAPITAL_LOCATIONS[get_civ_by_id(iHuman)]

            # Absinthe: changes in the unit positions, in order to prohibit these contacts in 500AD
            if iHuman == Civ.ARABIA:  # contact with Byzantium
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.ARABIA][0],
                    CIV_CAPITAL_LOCATIONS[Civ.ARABIA][1] - 10,
                )
            elif iHuman == Civ.BULGARIA:  # contact with Byzantium
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.BULGARIA][0],
                    CIV_CAPITAL_LOCATIONS[Civ.BULGARIA][1] + 1,
                )
            elif iHuman == Civ.OTTOMAN:  # contact with Byzantium
                tStart = (97, 23)

            make_unit(iHuman, Unit.SETTLER, tStart)
            make_unit(iHuman, Unit.SPEARMAN, tStart)

    def assign1200ADtechs(self, iCiv):
        # As a temporary solution, everyone gets Aragon's starting techs
        teamCiv = gc.getTeam(iCiv)
        for iTech in range(Technology.FARRIERS.value + 1):
            teamCiv.setHasTech(iTech, True, iCiv, False, False)
        teamCiv.setHasTech(Technology.BLAST_FURNACE.value, True, iCiv, False, False)
        teamCiv.setHasTech(Technology.CODE_OF_LAWS.value, True, iCiv, False, False)
        teamCiv.setHasTech(Technology.LITERATURE.value, True, iCiv, False, False)
        teamCiv.setHasTech(Technology.LATEEN_SAILS.value, True, iCiv, False, False)
        teamCiv.setHasTech(Technology.MAPMAKING.value, True, iCiv, False, False)
        teamCiv.setHasTech(Technology.ARISTOCRACY.value, True, iCiv, False, False)
        teamCiv.setHasTech(Technology.PLATE_ARMOR.value, True, iCiv, False, False)
        teamCiv.setHasTech(Technology.GOTHIC_ARCHITECTURE.value, True, iCiv, False, False)
        teamCiv.setHasTech(Technology.SIEGE_ENGINES.value, True, iCiv, False, False)
        if iCiv in [Civ.ARABIA.value, Civ.MOROCCO.value]:
            teamCiv.setHasTech(Technology.ARABIC_KNOWLEDGE.value, True, iCiv, False, False)

    def assignTechs(self, iCiv):
        civ = civilization(iCiv)
        techs = civ.initial.get("tech")
        if techs is not None:
            for tech in techs:
                civ.add_tech(tech)

    def showRect(self, iCiv, area):
        for iX, iY in utils.getPlotList(area.tile_min, area.tile_max):
            gc.getMap().plot(iX, iY).setRevealed(teamtype(iCiv), True, False, -1)

    def showArea(self, iCiv):
        for area in civilization(iCiv).location.visible_area:
            self.showRect(iCiv, area)

    def initContact(self, iCiv, bMeet=True):
        civ = team(iCiv)
        contacts = civilization(iCiv).scenario.get("contact")
        if contacts is not None:
            for contact in contacts:
                other = civilization(contact)
                if other.is_alive() and not civ.isHasMet(other.teamtype):
                    civ.meet(other.teamtype, bMeet)

    def LeaningTowerGP(self):
        iGP = rand(7)
        pFlorentia = gc.getMap().plot(54, 32).getPlotCity()
        iSpecialist = Specialist.GREAT_PROPHET.value + iGP
        pFlorentia.setFreeSpecialistCount(iSpecialist, 1)

    def setDiplo1200AD(self):
        self.changeAttitudeExtra(Civ.BYZANTIUM.value, Civ.ARABIA.value, -2)
        self.changeAttitudeExtra(Civ.SCOTLAND.value, Civ.FRANCE.value, 4)

    def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):
        gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
        gc.getPlayer(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)

    def create_starting_workers(self, iCiv, tPlot):
        make_units(iCiv, Unit.WORKER, tPlot, civilization(iCiv).initial.workers)
