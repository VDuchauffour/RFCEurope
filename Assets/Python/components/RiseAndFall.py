from CvPythonExtensions import *
from CoreData import CIVILIZATIONS
from CoreStructures import team, civ
import PyHelpers  # LOQ
import Popup
from PyUtils import percentage_chance
import RFCUtils
import ProvinceManager
import Consts
import XMLConsts as xml
import Religions
import Victory
from StoredData import sd
import Crusades

from MiscData import PLAGUE_IMMUNITY, MessageData
from CoreTypes import (
    Civ,
    Scenario,
    Religion,
    Specialist,
    Terrain,
    StartingSituation,
    ProvinceTypes,
    UniquePower,
    StabilityCategory,
)
from CivilizationsData import (
    CIV_AI_STOP_BIRTH_THRESHOLD,
    CIV_RESPAWNING_THRESHOLD,
    CIV_STARTING_SITUATION,
)
from CoreFunctions import get_civ_by_id
from LocationsData import CIV_CAPITAL_LOCATIONS, CIV_NEW_CAPITAL_LOCATIONS, CIV_OLDER_NEIGHBOURS
from TimelineData import CIV_BIRTHDATE, CIV_RESPAWNING_DATE, DateTurn

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


pBurgundy = gc.getPlayer(Civ.BURGUNDY.value)
pByzantium = gc.getPlayer(Civ.BYZANTIUM.value)
pFrankia = gc.getPlayer(Civ.FRANCE.value)
pArabia = gc.getPlayer(Civ.ARABIA.value)
pBulgaria = gc.getPlayer(Civ.BULGARIA.value)
pCordoba = gc.getPlayer(Civ.CORDOBA.value)
pSpain = gc.getPlayer(Civ.CASTILLE.value)
pNorway = gc.getPlayer(Civ.NORWAY.value)
pDenmark = gc.getPlayer(Civ.DENMARK.value)
pVenecia = gc.getPlayer(Civ.VENECIA.value)
pNovgorod = gc.getPlayer(Civ.NOVGOROD.value)
pKiev = gc.getPlayer(Civ.KIEV.value)
pHungary = gc.getPlayer(Civ.HUNGARY.value)
pGermany = gc.getPlayer(Civ.GERMANY.value)
pScotland = gc.getPlayer(Civ.SCOTLAND.value)
pPoland = gc.getPlayer(Civ.POLAND.value)
pMoscow = gc.getPlayer(Civ.MOSCOW.value)
pGenoa = gc.getPlayer(Civ.GENOA.value)
pMorocco = gc.getPlayer(Civ.MOROCCO.value)
pEngland = gc.getPlayer(Civ.ENGLAND.value)
pPortugal = gc.getPlayer(Civ.PORTUGAL.value)
pAragon = gc.getPlayer(Civ.ARAGON.value)
pPrussia = gc.getPlayer(Civ.PRUSSIA.value)
pLithuania = gc.getPlayer(Civ.LITHUANIA.value)
pAustria = gc.getPlayer(Civ.AUSTRIA.value)
pTurkey = gc.getPlayer(Civ.OTTOMAN.value)
pSweden = gc.getPlayer(Civ.SWEDEN.value)
pDutch = gc.getPlayer(Civ.DUTCH.value)
pPope = gc.getPlayer(Civ.POPE.value)
pIndependent = gc.getPlayer(Civ.INDEPENDENT.value)
pIndependent2 = gc.getPlayer(Civ.INDEPENDENT_2.value)
pIndependent3 = gc.getPlayer(Civ.INDEPENDENT_3.value)
pIndependent4 = gc.getPlayer(Civ.INDEPENDENT_4.value)
pBarbarian = gc.getPlayer(Civ.BARBARIAN.value)

teamBurgundy = gc.getTeam(pBurgundy.getTeam())
teamByzantium = gc.getTeam(pByzantium.getTeam())
teamFrankia = gc.getTeam(pFrankia.getTeam())
teamArabia = gc.getTeam(pArabia.getTeam())
teamBulgaria = gc.getTeam(pBulgaria.getTeam())
teamCordoba = gc.getTeam(pCordoba.getTeam())
teamSpain = gc.getTeam(pSpain.getTeam())
teamNorway = gc.getTeam(pNorway.getTeam())
teamDenmark = gc.getTeam(pDenmark.getTeam())
teamVenecia = gc.getTeam(pVenecia.getTeam())
teamNovgorod = gc.getTeam(pNovgorod.getTeam())
teamKiev = gc.getTeam(pKiev.getTeam())
teamHungary = gc.getTeam(pHungary.getTeam())
teamGermany = gc.getTeam(pGermany.getTeam())
teamScotland = gc.getTeam(pScotland.getTeam())
teamPoland = gc.getTeam(pPoland.getTeam())
teamMoscow = gc.getTeam(pMoscow.getTeam())
teamGenoa = gc.getTeam(pGenoa.getTeam())
teamMorocco = gc.getTeam(pMorocco.getTeam())
teamEngland = gc.getTeam(pEngland.getTeam())
teamPortugal = gc.getTeam(pPortugal.getTeam())
teamAragon = gc.getTeam(pAragon.getTeam())
teamPrussia = gc.getTeam(pPrussia.getTeam())
teamLithuania = gc.getTeam(pLithuania.getTeam())
teamAustria = gc.getTeam(pAustria.getTeam())
teamTurkey = gc.getTeam(pTurkey.getTeam())
teamSweden = gc.getTeam(pSweden.getTeam())
teamDutch = gc.getTeam(pDutch.getTeam())
teamPope = gc.getTeam(pPope.getTeam())
teamIndependent = gc.getTeam(pIndependent.getTeam())
teamIndependent2 = gc.getTeam(pIndependent2.getTeam())
teamIndependent3 = gc.getTeam(pIndependent3.getTeam())
teamIndependent4 = gc.getTeam(pIndependent4.getTeam())
teamBarbarian = gc.getTeam(pBarbarian.getTeam())


# This is now obsolete
# for not allowing new civ popup if too close
# Sedna17, moving around the order in which civs rise without changing their WBS requires you to do funny things here to prevent "Change Civ?" popups
# Spain and Moscow have really long delays for this reason
# This is now obsolete
# tDifference = (0, 0, 0, 1, 0, 1, 10, 0, 0, 1, 0, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


class RiseAndFall:
    def __init__(self):
        self.pm = ProvinceManager.ProvinceManager()
        # Init the Province Manager

    ##################################################
    ### Secure storage & retrieval of script data ###
    ################################################

    def getNewCiv(self):
        return sd.scriptDict["iNewCiv"]

    def setNewCiv(self, iNewValue):
        sd.scriptDict["iNewCiv"] = iNewValue

    def getNewCivFlip(self):
        return sd.scriptDict["iNewCivFlip"]

    def setNewCivFlip(self, iNewValue):
        sd.scriptDict["iNewCivFlip"] = iNewValue

    def getOldCivFlip(self):
        return sd.scriptDict["iOldCivFlip"]

    def setOldCivFlip(self, iNewValue):
        sd.scriptDict["iOldCivFlip"] = iNewValue

    def getTempTopLeft(self):
        return sd.scriptDict["tempTopLeft"]

    def setTempTopLeft(self, tNewValue):
        sd.scriptDict["tempTopLeft"] = tNewValue

    def getTempBottomRight(self):
        return sd.scriptDict["tempBottomRight"]

    def setTempBottomRight(self, tNewValue):
        sd.scriptDict["tempBottomRight"] = tNewValue

    def getSpawnWar(self):
        return sd.scriptDict["iSpawnWar"]

    def setSpawnWar(self, iNewValue):
        sd.scriptDict["iSpawnWar"] = iNewValue

    def getAlreadySwitched(self):
        return sd.scriptDict["bAlreadySwitched"]

    def setAlreadySwitched(self, bNewValue):
        sd.scriptDict["bAlreadySwitched"] = bNewValue

    def getColonistsAlreadyGiven(self, iCiv):
        return sd.scriptDict["lColonistsAlreadyGiven"][iCiv]

    def setColonistsAlreadyGiven(self, iCiv, iNewValue):
        sd.scriptDict["lColonistsAlreadyGiven"][iCiv] = iNewValue

    def getNumCities(self, iCiv):
        return sd.scriptDict["lNumCities"][iCiv]

    def setNumCities(self, iCiv, iNewValue):
        sd.scriptDict["lNumCities"][iCiv] = iNewValue

    def getSpawnDelay(self, iCiv):
        return sd.scriptDict["lSpawnDelay"][iCiv]

    def setSpawnDelay(self, iCiv, iNewValue):
        sd.scriptDict["lSpawnDelay"][iCiv] = iNewValue

    def getFlipsDelay(self, iCiv):
        return sd.scriptDict["lFlipsDelay"][iCiv]

    def setFlipsDelay(self, iCiv, iNewValue):
        sd.scriptDict["lFlipsDelay"][iCiv] = iNewValue

    def getBetrayalTurns(self):
        return sd.scriptDict["iBetrayalTurns"]

    def setBetrayalTurns(self, iNewValue):
        sd.scriptDict["iBetrayalTurns"] = iNewValue

    def getLatestFlipTurn(self):
        return sd.scriptDict["iLatestFlipTurn"]

    def setLatestFlipTurn(self, iNewValue):
        sd.scriptDict["iLatestFlipTurn"] = iNewValue

    def getLatestRebellionTurn(self, iCiv):
        return sd.scriptDict["lLatestRebellionTurn"][iCiv]

    def setLatestRebellionTurn(self, iCiv, iNewValue):
        sd.scriptDict["lLatestRebellionTurn"][iCiv] = iNewValue

    def getRebelCiv(self):
        return sd.scriptDict["iRebelCiv"]

    def setRebelCiv(self, iNewValue):
        sd.scriptDict["iRebelCiv"] = iNewValue

    def getRebelCities(self):
        return sd.scriptDict["lRebelCities"]

    def setRebelCities(self, lCityList):
        sd.scriptDict["lRebelCities"] = lCityList

    def getRebelSuppress(self):
        return sd.scriptDict["lRebelSuppress"]

    def setRebelSuppress(self, lSuppressList):
        sd.scriptDict["lRebelSuppress"] = lSuppressList

    def getExileData(self, i):
        return sd.scriptDict["lExileData"][i]

    def setExileData(self, i, iNewValue):
        sd.scriptDict["lExileData"][i] = iNewValue

    def getTempFlippingCity(self):
        return sd.scriptDict["tempFlippingCity"]

    def setTempFlippingCity(self, tNewValue):
        sd.scriptDict["tempFlippingCity"] = tNewValue

    def getCheatersCheck(self, i):
        return sd.scriptDict["lCheatersCheck"][i]

    def setCheatersCheck(self, i, iNewValue):
        sd.scriptDict["lCheatersCheck"][i] = iNewValue

    def getBirthTurnModifier(self, iCiv):
        return sd.scriptDict["lBirthTurnModifier"][iCiv]

    def setBirthTurnModifier(self, iCiv, iNewValue):
        sd.scriptDict["lBirthTurnModifier"][iCiv] = iNewValue

    def getDeleteMode(self, i):
        return sd.scriptDict["lDeleteMode"][i]

    def setDeleteMode(self, i, iNewValue):
        sd.scriptDict["lDeleteMode"][i] = iNewValue

    def getFirstContactConquerors(self, iCiv):
        return sd.scriptDict["lFirstContactConquerors"][iCiv]

    def setFirstContactConquerors(self, iCiv, iNewValue):
        sd.scriptDict["lFirstContactConquerors"][iCiv] = iNewValue

    # Sedna17 Respawn
    def setSpecialRespawnTurn(self, iCiv, iNewValue):
        sd.scriptDict["lSpecialRespawnTurn"][iCiv] = iNewValue

    def getSpecialRespawnTurns(self):
        return sd.scriptDict["lSpecialRespawnTurn"]

    ###############
    ### Popups ###
    #############

    """ popupID has to be a registered ID in CvRhyesCatapultEventManager.__init__!! """

    def showPopup(self, popupID, title, message, labels):
        popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setHeaderString(title)
        popup.setBodyString(message)
        for i in labels:
            popup.addButton(i)
        popup.launch(False)

    def newCivPopup(self, iCiv):
        self.showPopup(
            7614,
            CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()),
            CyTranslator().getText(
                "TXT_KEY_NEWCIV_MESSAGE", (gc.getPlayer(iCiv).getCivilizationAdjectiveKey(),)
            ),
            (
                CyTranslator().getText("TXT_KEY_POPUP_YES", ()),
                CyTranslator().getText("TXT_KEY_POPUP_NO", ()),
            ),
        )
        self.setNewCiv(iCiv)

    def eventApply7614(self, popupReturn):
        if popupReturn.getButtonClicked() == 0:  # 1st button
            iOldHandicap = gc.getActivePlayer().getHandicapType()
            iNewCiv = self.getNewCiv()
            vic.switchUHV(iNewCiv, utils.getHumanID())
            gc.getActivePlayer().setHandicapType(gc.getPlayer(iNewCiv).getHandicapType())
            gc.getGame().setActivePlayer(iNewCiv, False)
            gc.getPlayer(iNewCiv).setHandicapType(iOldHandicap)
            # for i in range(Consts.iNumStabilityParameters):
            # 	utils.setStabilityParameters(utils.getHumanID(),i, 0)
            # 	utils.setLastRecordedStabilityStuff(0, 0)
            # 	utils.setLastRecordedStabilityStuff(1, 0)
            # 	utils.setLastRecordedStabilityStuff(2, 0)
            # 	utils.setLastRecordedStabilityStuff(3, 0)
            # 	utils.setLastRecordedStabilityStuff(4, 0)
            # 	utils.setLastRecordedStabilityStuff(5, 0)
            for iMaster in CIVILIZATIONS.majors().ids():
                if gc.getTeam(gc.getPlayer(iNewCiv).getTeam()).isVassal(iMaster):
                    gc.getTeam(gc.getPlayer(iNewCiv).getTeam()).setVassal(iMaster, False, False)
            self.setAlreadySwitched(True)
            gc.getPlayer(iNewCiv).setPlayable(True)
            # CyInterface().addImmediateMessage("first button", "")
        # elif( popupReturn.getButtonClicked() == 1 ): # 2nd button
        # CyInterface().addImmediateMessage("second button", "")

    def flipPopup(self, iNewCiv, tTopLeft, tBottomRight):
        iHuman = utils.getHumanID()
        flipText = CyTranslator().getText("TXT_KEY_FLIPMESSAGE1", ())
        lPlots = utils.getPlotList(tTopLeft, tBottomRight) + Consts.lExtraPlots[iNewCiv]
        for (x, y) in lPlots:
            plot = gc.getMap().plot(x, y)
            if plot.isCity():
                if plot.getPlotCity().getOwner() == iHuman:
                    if not plot.getPlotCity().isCapital():
                        flipText += plot.getPlotCity().getName() + "\n"
        flipText += CyTranslator().getText("TXT_KEY_FLIPMESSAGE2", ())

        self.showPopup(
            7615,
            CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()),
            flipText,
            (
                CyTranslator().getText("TXT_KEY_POPUP_YES", ()),
                CyTranslator().getText("TXT_KEY_POPUP_NO", ()),
            ),
        )
        self.setNewCivFlip(iNewCiv)
        self.setOldCivFlip(iHuman)
        self.setTempTopLeft(tTopLeft)
        self.setTempBottomRight(tBottomRight)

    def eventApply7615(self, popupReturn):
        iHuman = utils.getHumanID()
        tTopLeft = self.getTempTopLeft()
        tBottomRight = self.getTempBottomRight()
        iNewCivFlip = self.getNewCivFlip()

        humanCityList = []
        lPlots = (
            utils.getPlotList(tTopLeft, tBottomRight) + Consts.lExtraPlots[self.getNewCivFlip()]
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
                CyTranslator().getText("TXT_KEY_FLIP_AGREED", ()),
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

                    # iEra = gc.getPlayer(iNewCivFlip).getCurrentEra()
                    # if (iEra >= 2): #medieval
                    # 	if (city.getPopulation() < iEra):
                    # 		city.setPopulation(iEra) #causes an unidentifiable C++ exception

                    # humanCityList[i].setHasRealBuilding(Plague.PLAGUE.value, False) #buggy

            # same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
            for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
                betrayalPlot = gc.getMap().plot(x, y)
                iNumUnitsInAPlot = betrayalPlot.getNumUnits()
                if iNumUnitsInAPlot > 0:
                    for i in range(iNumUnitsInAPlot):
                        unit = betrayalPlot.getUnit(i)
                        if unit.getOwner() == iHuman:
                            rndNum = gc.getGame().getSorenRandNum(100, "betrayal")
                            if rndNum >= iBetrayalThreshold:
                                if unit.getDomainType() == DomainTypes.DOMAIN_SEA:  # land unit
                                    iUnitType = unit.getUnitType()
                                    unit.kill(False, iNewCivFlip)
                                    utils.makeUnit(iUnitType, iNewCivFlip, (x, y), 1)
                                    i = i - 1

            if self.getCheatersCheck(0) == 0:
                self.setCheatersCheck(0, iCheatersPeriod)
                self.setCheatersCheck(1, self.getNewCivFlip())

        elif popupReturn.getButtonClicked() == 1:  # 2nd button
            CyInterface().addMessage(
                iHuman,
                True,
                MessageData.DURATION,
                CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()),
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
                    # city.setCulture(self.getNewCivFlip(), city.countTotalCulture(), True)
                    pCurrent = gc.getMap().plot(city.getX(), city.getY())
                    oldCulture = pCurrent.getCulture(iHuman)
                    # Absinthe: changeCulture instead of setCulture, otherwise previous culture will be lost
                    pCurrent.changeCulture(iNewCivFlip, oldCulture / 2, True)
                    pCurrent.setCulture(iHuman, oldCulture / 2, True)
                    iWar = self.getSpawnWar() + 1
                    self.setSpawnWar(iWar)
                    if self.getSpawnWar() == 1:
                        # CyInterface().addImmediateMessage(CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "")
                        # safety check - don't want to use canDeclareWar, as here we want to always declare war
                        if not gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).isAtWar(iHuman):
                            gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).declareWar(
                                iHuman, False, -1
                            )
                        self.setBetrayalTurns(iBetrayalPeriod)
                        self.initBetrayal()

    # resurrection when some human controlled cities are also included
    def rebellionPopup(self, iRebelCiv, iNumCities):
        iLoyalPrice = min((10 * gc.getPlayer(utils.getHumanID()).getGold()) / 100, 50 * iNumCities)
        self.showPopup(
            7622,
            CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()),
            CyTranslator().getText(
                "TXT_KEY_REBELLION_HUMAN", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)
            ),
            (
                CyTranslator().getText("TXT_KEY_REBELLION_LETGO", ()),
                CyTranslator().getText("TXT_KEY_REBELLION_DONOTHING", ()),
                CyTranslator().getText("TXT_KEY_REBELLION_CRACK", ()),
                CyTranslator().getText("TXT_KEY_REBELLION_BRIBE", ()) + " " + str(iLoyalPrice),
                CyTranslator().getText("TXT_KEY_REBELLION_BOTH", ()),
            ),
        )

    # resurrection when some human controlled cities are also included
    def eventApply7622(self, popupReturn):
        iHuman = utils.getHumanID()
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
            if gc.getGame().getSorenRandNum(100, "odds") < 40:
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
            if gc.getGame().getSorenRandNum(100, "odds") < iLoyalPrice / iHumanCity:
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
            if gc.getGame().getSorenRandNum(100, "odds") < iLoyalPrice / iHumanCity + 40:
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

        self.pm.setup()

        # self.setupBirthTurnModifiers() #causes a crash on civ switch?

        self.setEarlyLeaders()

        # Sedna17 Respawn setup special respawn turns
        self.setupRespawnTurns()

        iHuman = utils.getHumanID()
        if utils.getScenario() == Scenario.i500AD:
            self.create500ADstartingUnits()
        else:
            self.create1200ADstartingUnits()
            for iCiv in range(Civ.ARAGON.value + 1):
                self.showArea(iCiv, Scenario.i1200AD)
                self.assign1200ADtechs(
                    iCiv
                )  # Temporarily all civs get the same starting techs as Aragon
                self.initContact(iCiv, False)
            rel.setStartingFaith()
            self.setDiplo1200AD()
            self.LeaningTowerGP()
            rel.spread1200ADJews()  # Spread Jews to some random cities
            vic.set1200UHVDone(iHuman)
            self.assign1200ADtechs(
                Civ.POPE.value
            )  # Temporarily all civs get the same starting techs as Aragon
            cru.do1200ADCrusades()

        self.assignGold()

    def assignGold(self):
        for civilization in CIVILIZATIONS.dropna("initial"):
            gold = civilization.initial.condition.gold
            if gold:
                civilization.player.changeGold(gold)

    def onCityBuilt(self, iPlayer, pCity):
        tCity = (pCity.getX(), pCity.getY())
        x, y = tCity
        self.pm.onCityBuilt(iPlayer, pCity.getX(), pCity.getY())
        # Absinthe: We can add free buildings for new cities here
        # 			Note that it will add the building every time a city is founded on the plot, not just on the first time
        # 			Venice (56, 35), Augsburg (55, 41), Porto (23, 31), Prague (60, 44), Riga (74, 58), Perekop (87, 36)
        # 			London (41, 52), Novgorod (80, 62) currently has preplaced fort on the map instead
        if tCity in [(56, 35), (55, 41), (23, 31), (60, 44), (74, 58), (87, 36)]:
            pCity.setHasRealBuilding(utils.getUniqueBuilding(iPlayer, xml.iWalls), True)
        elif tCity == (75, 53):  # Vilnius - important for AI Lithuania against Prussia
            if not gc.getPlayer(Civ.LITHUANIA.value).isHuman():
                pCity.setHasRealBuilding(utils.getUniqueBuilding(iPlayer, xml.iWalls), True)

    def onCityAcquired(self, owner, iPlayer, city, bConquest, bTrade):
        self.pm.onCityAcquired(owner, iPlayer, city, bConquest, bTrade)
        # Constantinople -> Istanbul
        if iPlayer == Civ.OTTOMAN.value:
            cityList = utils.getCityList(iPlayer)
            if (city.getX(), city.getY()) == CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM].to_tuple():
                for loopCity in cityList:
                    if loopCity != city:
                        loopCity.setHasRealBuilding((xml.iPalace), False)
                city.setHasRealBuilding(xml.iPalace, True)
                if pTurkey.getStateReligion() == Religion.ISLAM.value:
                    city.setHasReligion(Religion.ISLAM.value, True, True, False)
                # some stability boost and flavour message
                pTurkey.changeStabilityBase(StabilityCategory.EXPANSION.value, 6)
                if utils.getHumanID() == iPlayer:
                    CyInterface().addMessage(
                        iPlayer,
                        True,
                        MessageData.DURATION,
                        CyTranslator().getText("TXT_KEY_GLORY_ON_CONQUEST", ()),
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
                    IstanbulPlot = gc.getMap().plot(
                        *CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM].to_tuple()
                    )
                    if IstanbulPlot.isCity():
                        if IstanbulPlot.getPlotCity().getOwner() == iPlayer:
                            bHasIstanbul = True
                    if not bHasIstanbul:
                        gc.getPlayer(iPlayer).getCapitalCity().setHasRealBuilding(
                            xml.iPalace, False
                        )
                        city.setHasRealBuilding(xml.iPalace, True)
                    if (
                        pTurkey.getStateReligion() == Religion.ISLAM.value
                    ):  # you get Islam anyway, as a bonus
                        city.setHasReligion(Religion.ISLAM.value, True, True, False)

        # Absinthe: Message for the human player, if the last city of a known civ is conquered
        iOriginalOwner = owner
        pOriginalOwner = gc.getPlayer(iOriginalOwner)
        if not pOriginalOwner.isHuman():
            iNumCities = pOriginalOwner.getNumCities()
            if iNumCities == 0:
                # all collapses operate with flips, so if the last city was conquered, we are good to go (this message won't come after a collapse message)
                if bConquest:
                    iHuman = utils.getHumanID()
                    if gc.getPlayer(iHuman).canContact(iOriginalOwner):
                        CyInterface().addMessage(
                            iHuman,
                            False,
                            MessageData.DURATION,
                            pOriginalOwner.getCivilizationDescription(0)
                            + " "
                            + CyTranslator().getText("TXT_KEY_STABILITY_CONQUEST_LAST_CITY", ()),
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

    def clear600ADChina(self):
        pass

    # Sedna17 Respawn
    def setupRespawnTurns(self):
        for iCiv in CIVILIZATIONS.majors().ids():
            self.setSpecialRespawnTurn(
                iCiv,
                CIV_RESPAWNING_DATE[get_civ_by_id(iCiv)]
                + (gc.getGame().getSorenRandNum(21, "BirthTurnModifier") - 10)
                + (gc.getGame().getSorenRandNum(21, "BirthTurnModifier2") - 10),
            )  # bell-curve-like spawns within +/- 10 turns of desired turn (3Miro: Uniform, not a bell-curve)

    def setupBirthTurnModifiers(self):
        # 3Miro: first and last civ (first that does not start)
        # Absinthe: currently unused
        for iCiv in CIVILIZATIONS.majors().ids():
            if iCiv >= Civ.ARABIA.value and not gc.getPlayer(iCiv).isHuman():
                self.setBirthTurnModifier(
                    iCiv, (gc.getGame().getSorenRandNum(11, "BirthTurnModifier") - 5)
                )  # -5 to +5
        # now make sure that no civs spawn in the same turn and cause a double "new civ" popup
        for iCiv in CIVILIZATIONS.majors().ids():
            if iCiv > utils.getHumanID() and iCiv < CIVILIZATIONS.majors().len():
                for j in range(CIVILIZATIONS.main().len() - iCiv):
                    iNextCiv = iCiv + j + 1
                    if CIV_BIRTHDATE[get_civ_by_id(iCiv)] + self.getBirthTurnModifier(
                        iCiv
                    ) == CIV_BIRTHDATE[get_civ_by_id(iNextCiv)] + self.getBirthTurnModifier(
                        iNextCiv
                    ):
                        self.setBirthTurnModifier(
                            iNextCiv, (self.getBirthTurnModifier(iNextCiv) + 1)
                        )

    def setEarlyLeaders(self):
        for civilization in CIVILIZATIONS.majors():
            if (
                civilization.leaders.early != civilization.leaders.primary
                and not civilization.player.isHuman()
            ):
                leader = civilization.leaders.early
                civilization.player.setLeader(leader.value)

    def setWarOnSpawn(self):
        # Absinthe: will use setAtWar here instead of declareWar, so it won't affect diplo relations and other stuff between major civs
        for civilization in CIVILIZATIONS.dropna("initial"):
            if civilization.initial.wars:
                for other, war_threshold in civilization.initial.wars.items():
                    if percentage_chance(war_threshold, strict=True):
                        if not civilization.at_war(other):
                            civilization.team.setAtWar(other.team, True)

    def checkTurn(self, iGameTurn):
        # Trigger betrayal mode
        if self.getBetrayalTurns() > 0:
            self.initBetrayal()

        if self.getCheatersCheck(0) > 0:
            teamPlayer = gc.getTeam(gc.getPlayer(utils.getHumanID()).getTeam())
            if teamPlayer.isAtWar(self.getCheatersCheck(1)):
                self.initMinorBetrayal(self.getCheatersCheck(1))
                self.setCheatersCheck(0, 0)
                self.setCheatersCheck(1, -1)
            else:
                self.setCheatersCheck(0, self.getCheatersCheck(0) - 1)

        if iGameTurn % 20 == 0:
            for civilization in CIVILIZATIONS.independents():
                if civilization.player.isAlive():
                    utils.updateMinorTechs(civilization.id, Civ.BARBARIAN.value)

        # Absinthe: checking the spawn dates
        for iLoopCiv in CIVILIZATIONS.majors().ids():
            if (
                CIV_BIRTHDATE[get_civ_by_id(iLoopCiv)] != 0
                and iGameTurn >= CIV_BIRTHDATE[get_civ_by_id(iLoopCiv)] - 2
                and iGameTurn <= CIV_BIRTHDATE[get_civ_by_id(iLoopCiv)] + 4
            ):
                self.initBirth(iGameTurn, CIV_BIRTHDATE[get_civ_by_id(iLoopCiv)], iLoopCiv)

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
        # lSpecialRespawnTurn = self.getSpecialRespawnTurns()
        # if iGameTurn in lSpecialRespawnTurn:
        # 	iCiv = lSpecialRespawnTurn.index(iGameTurn)#Lookup index for
        # 	if iCiv < CIVILIZATIONS.majors().len() and iCiv > 0:
        # 		self.resurrection(iGameTurn,iCiv)

        # Absinthe: Reduce cities to towns, in order to make room for new civs
        if iGameTurn == CIV_BIRTHDATE[get_civ_by_id(Civ.SCOTLAND.value)] - 3:
            # Reduce Inverness and Scone, so more freedom in where to found cities in Scotland
            self.reduceCity((37, 65))
            self.reduceCity((37, 67))
        elif iGameTurn == CIV_BIRTHDATE[get_civ_by_id(Civ.ENGLAND.value)] - 3:
            # Reduce Norwich and Nottingham, so more freedom in where to found cities in England
            self.reduceCity((43, 55))
            self.reduceCity((39, 56))
        elif iGameTurn == CIV_BIRTHDATE[get_civ_by_id(Civ.SWEDEN.value)] - 2:
            # Reduce Uppsala
            self.reduceCity((65, 66))
        # Absinthe: Reduce cities to town, if not owned by the human player
        if iGameTurn == DateTurn.i1057AD:
            # Reduce Kairouan
            pPlot = gc.getMap().plot(43, 55)
            if pPlot.isCity():
                if pPlot.getPlotCity().getOwner() != utils.getHumanID():
                    self.reduceCity((43, 55))

    def reduceCity(self, tPlot):
        # Absinthe: disappearing cities (reducing them to an improvement)
        pPlot = gc.getMap().plot(tPlot[0], tPlot[1])
        if pPlot.isCity():
            # Absinthe: apologize from the player:
            msgString = (
                CyTranslator().getText("TXT_KEY_REDUCE_CITY_1", ())
                + " "
                + pPlot.getPlotCity().getName()
                + " "
                + CyTranslator().getText("TXT_KEY_REDUCE_CITY_2", ())
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
            pPlot.setImprovementType(xml.iImprovementTown)  # Improvement Town instead of the city
            pPlot.setRouteType(0)  # Also adding a road there

    def checkPlayerTurn(self, iGameTurn, iPlayer):
        # Absinthe & Merijn: leader switching with any number of leaders
        late_leaders = CIVILIZATIONS[iPlayer].leaders.late
        if late_leaders:
            for tLeader in reversed(late_leaders):
                if iGameTurn >= tLeader[1]:
                    self.switchLateLeaders(iPlayer, tLeader)
                    break

        # 3Miro: English cheat, the AI is utterly incompetent when it has to launch an invasion on an island
        # 			if in 1300AD Dublin is still Barbarian, it will flip to England
        if (
            iGameTurn == DateTurn.i1300AD
            and utils.getHumanID() != Civ.ENGLAND.value
            and iPlayer == Civ.ENGLAND.value
            and pEngland.isAlive()
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
            and utils.getHumanID() != Civ.ENGLAND.value
            and iPlayer == Civ.ENGLAND.value
            and pEngland.isAlive()
        ):
            for (x, y) in utils.getPlotList((39, 46), (45, 50)):
                pCurrent = gc.getMap().plot(x, y)
                if pCurrent.isCity():
                    pCity = pCurrent.getPlotCity()
                    if pCity.getOwner() == Civ.ENGLAND.value:
                        utils.makeUnit(xml.iGuisarme, Civ.ENGLAND.value, (x, y), 1)
                        utils.makeUnit(xml.iArbalest, Civ.ENGLAND.value, (x, y), 1)
                        pCity.setHasRealBuilding(xml.iWalls, True)
                        pCity.setHasRealBuilding(xml.iCastle, True)

    def switchLateLeaders(self, iPlayer, tLeader):
        iLeader, iDate, iThreshold, iEra = tLeader
        if iLeader == gc.getPlayer(iPlayer).getLeader():
            return
        if gc.getPlayer(iPlayer).getCurrentEra() >= iEra:
            iThreshold *= 2
        if (
            gc.getPlayer(iPlayer).getAnarchyTurns() != 0
            or utils.getPlagueCountdown(iPlayer) > 0
            or utils.getStability(iPlayer) <= -10
            or gc.getGame().getSorenRandNum(100, "die roll") < iThreshold
        ):
            gc.getPlayer(iPlayer).setLeader(iLeader.value)

            # Absinthe: message about the leader switch for the human player
            iHuman = utils.getHumanID()
            HumanTeam = gc.getTeam(gc.getPlayer(iHuman).getTeam())
            PlayerTeam = gc.getPlayer(iPlayer).getTeam()
            if HumanTeam.isHasMet(PlayerTeam) and utils.isActive(
                iHuman
            ):  # only if it's a known civ
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
        for iIndep1 in CIVILIZATIONS.independents().ids():
            pIndep1 = gc.getPlayer(iIndep1)
            iNumCities1 = pIndep1.getNumCities()
            for iIndep2 in CIVILIZATIONS.independents().ids():
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
        iRndnum = gc.getGame().getSorenRandNum(CIVILIZATIONS.majors().len(), "starting count")
        for j in CIVILIZATIONS.majors().ids():
            iDeadCiv = (j + iRndnum) % CIVILIZATIONS.majors().len()
            if (
                not gc.getPlayer(iDeadCiv).isAlive()
                and iGameTurn > CIV_BIRTHDATE[get_civ_by_id(iDeadCiv)] + 50
            ):
                pDeadCiv = gc.getPlayer(iDeadCiv)
                teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
                lCities = []
                for (x, y) in utils.getPlotList(
                    Consts.tNormalAreasTL[iDeadCiv], Consts.tNormalAreasBR[iDeadCiv]
                ):
                    plot = gc.getMap().plot(x, y)
                    if plot.isCity():
                        if plot.getPlotCity().getOwner() == Civ.BARBARIAN.value:
                            lCities.append((x, y))
                if len(lCities) > 5:
                    iDivideCounter = 0
                    for tCity in lCities:
                        iNewCiv = min(
                            CIVILIZATIONS.independents().ids()
                        ) + gc.getGame().getSorenRandNum(
                            max(CIVILIZATIONS.independents().ids())
                            - min(CIVILIZATIONS.independents().ids())
                            + 1,
                            "randomIndep",
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
        for iCiv in CIVILIZATIONS.majors().ids():
            pCiv = gc.getPlayer(iCiv)
            if pCiv.isAlive():
                # Absinthe: no barb collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
                iRespawnTurn = utils.getLastRespawnTurn(iCiv)
                if (
                    iGameTurn >= CIV_BIRTHDATE[get_civ_by_id(iCiv)] + 20
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
                        iHuman = utils.getHumanID()
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
        lNumCitiesLastTime = [0] * CIVILIZATIONS.majors().len()
        for iCiv in CIVILIZATIONS.majors().ids():
            pCiv = gc.getPlayer(iCiv)
            teamCiv = gc.getTeam(pCiv.getTeam())
            if pCiv.isAlive():
                lNumCitiesLastTime[iCiv] = self.getNumCities(iCiv)
                iNumCitiesCurrently = pCiv.getNumCities()
                self.setNumCities(iCiv, iNumCitiesCurrently)
                # Absinthe: no generic collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
                iRespawnTurn = utils.getLastRespawnTurn(iCiv)
                if (
                    iGameTurn >= CIV_BIRTHDATE[get_civ_by_id(iCiv)] + 20
                    and iGameTurn >= iRespawnTurn + 10
                    and not utils.collapseImmune(iCiv)
                ):
                    # Absinthe: pass for small civs, we have bad stability collapses and collapseMotherland anyway, which is better suited for the collapse of those
                    if (
                        lNumCitiesLastTime[iCiv] > 2
                        and iNumCitiesCurrently * 2 <= lNumCitiesLastTime[iCiv]
                    ):
                        iHuman = utils.getHumanID()
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
        for iCiv in CIVILIZATIONS.majors().ids():
            pCiv = gc.getPlayer(iCiv)
            teamCiv = gc.getTeam(pCiv.getTeam())
            if pCiv.isAlive():
                # Absinthe: no motherland collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
                iRespawnTurn = utils.getLastRespawnTurn(iCiv)
                if (
                    iGameTurn >= CIV_BIRTHDATE[get_civ_by_id(iCiv)] + 20
                    and iGameTurn >= iRespawnTurn + 10
                    and not utils.collapseImmune(iCiv)
                ):
                    # Absinthe: respawned Cordoba or Aragon shouldn't collapse because not holding the original core area
                    if iCiv in [Civ.CORDOBA.value, Civ.ARAGON.value] and pCiv.getRespawnedAlive():
                        continue
                    if not gc.safeMotherland(iCiv):
                        iHuman = utils.getHumanID()
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
        iRndnum = gc.getGame().getSorenRandNum(CIVILIZATIONS.majors().len(), "starting count")
        iSecessionNumber = 0
        for j in CIVILIZATIONS.majors().ids():
            iPlayer = (j + iRndnum) % CIVILIZATIONS.majors().len()
            pPlayer = gc.getPlayer(iPlayer)
            # Absinthe: no city secession for 15 turns after spawn, for 10 turns after respawn
            iRespawnTurn = utils.getLastRespawnTurn(iPlayer)
            if (
                pPlayer.isAlive()
                and iGameTurn >= CIV_BIRTHDATE[get_civ_by_id(iPlayer)] + 15
                and iGameTurn >= iRespawnTurn + 10
            ):
                iStability = pPlayer.getStability()
                if gc.getGame().getSorenRandNum(10, "do the check for city secession") < (
                    -2 - iStability
                ):  # 10% at -3, increasing by 10% with each point (100% with -12 or less)
                    self.revoltCity(iPlayer, False)
                    iSecessionNumber += 1
                    if iSecessionNumber > 2:
                        return  # max 3 secession per turn
                    continue  # max 1 secession for each civ

    def secessionCloseCollapse(self, iGameTurn):
        # Absinthe: another instance of secession, now with possibility for multiple cities revolting for the same civ
        # Absinthe: this can only happen with very bad stability, in case of fairly big empires
        iRndnum = gc.getGame().getSorenRandNum(CIVILIZATIONS.majors().len(), "starting count")
        for j in CIVILIZATIONS.majors().ids():
            iPlayer = (j + iRndnum) % CIVILIZATIONS.majors().len()
            pPlayer = gc.getPlayer(iPlayer)
            iRespawnTurn = utils.getLastRespawnTurn(iPlayer)
            if (
                pPlayer.isAlive()
                and iGameTurn >= CIV_BIRTHDATE[get_civ_by_id(iPlayer)] + 20
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
                and tCity != CIV_CAPITAL_LOCATIONS[get_civ_by_id(iPlayer)].to_tuple()
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
                            if iProvType >= ProvinceTypes.POTENTIAL.value:
                                if not bCollapseImmune:
                                    cityListInCore.append(city)
                            else:
                                cityListInNotCore.append(city)
                        # Absinthe: angry population, bad health, untolerated religion, no military garrison can add the city to the list a couple more times (per type)
                        # 			if the city is in a contested province, the city is added a couple more times by default, if in a foreign province, a lot more times
                        # Absinthe: bigger chance to choose the city if unhappy
                        if city.angryPopulation(0) > 0:
                            if iProvType >= ProvinceTypes.POTENTIAL.value:
                                if not bCollapseImmune:
                                    for i in range(2):
                                        cityListInCore.append(city)
                            else:
                                for i in range(4):
                                    cityListInNotCore.append(city)
                        # Absinthe: health issues do not cause city secession in core provinces for anyone
                        # 			also less chance from unhealth for cities in contested and foreign provinces
                        if city.goodHealth() - city.badHealth(False) < -1:
                            if iProvType < ProvinceTypes.POTENTIAL.value:
                                cityListInNotCore.append(city)
                        # Absinthe: also not a cause for secession in core provinces, no need to punish the player this much (and especially the AI) for using the civic
                        if city.getReligionBadHappiness() < 0:
                            if iProvType < ProvinceTypes.POTENTIAL.value:
                                for i in range(2):
                                    cityListInNotCore.append(city)
                        # Absinthe: no defensive units in the city increase chance
                        if city.getNoMilitaryPercentAnger() > 0:
                            if iProvType >= ProvinceTypes.POTENTIAL.value:
                                if not bCollapseImmune:
                                    cityListInCore.append(city)
                            else:
                                for i in range(2):
                                    cityListInNotCore.append(city)
                        # Absinthe: also add core cities if they have less than 40% own culture (and the civ doesn't have the Cultural Tolerance UP)
                        if iProvType >= ProvinceTypes.POTENTIAL.value:
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
                        elif iProvType == ProvinceTypes.OUTER.value:
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
                        elif iProvType == ProvinceTypes.NONE.value:
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
                splittingCity = utils.getRandomEntry(cityListInNotCore)
            else:
                splittingCity = utils.getRandomEntry(cityListInCore)

            # Absinthe: city goes to random independent
            iRndNum = gc.getGame().getSorenRandNum(
                max(CIVILIZATIONS.independents().ids())
                - min(CIVILIZATIONS.independents().ids())
                + 1,
                "random independent",
            )
            iIndy = min(CIVILIZATIONS.independents().ids()) + iRndNum

            tCity = (splittingCity.getX(), splittingCity.getY())
            sCityName = splittingCity.getName()
            if iPlayer == utils.getHumanID():
                CyInterface().addMessage(
                    iPlayer,
                    True,
                    MessageData.DURATION,
                    sCityName + " " + CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()),
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

        iRndnum = gc.getGame().getSorenRandNum(CIVILIZATIONS.majors().len(), "starting count")
        for j in CIVILIZATIONS.majors().ids():
            if not bSpecialRespawn:
                iDeadCiv = (j + iRndnum) % CIVILIZATIONS.majors().len()
            else:
                iDeadCiv = iDeadCiv  # We want a specific civ for special re-spawn
            cityList = []
            if (
                not gc.getPlayer(iDeadCiv).isAlive()
                and iGameTurn > CIV_BIRTHDATE[get_civ_by_id(iDeadCiv)] + 25
                and iGameTurn > utils.getLastTurnAlive(iDeadCiv) + 10
            ):  # Sedna17: Allow re-spawns only 10 turns after death and 25 turns after birth
                pDeadCiv = gc.getPlayer(iDeadCiv)
                teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
                tTopLeft = Consts.tNormalAreasTL[iDeadCiv]
                tBottomRight = Consts.tNormalAreasBR[iDeadCiv]

                for tPlot in utils.getPlotList(tTopLeft, tBottomRight):
                    x, y = tPlot
                    if tPlot in Consts.tNormalAreasSubtract[iDeadCiv]:
                        continue
                    # if ((x,y) not in Consts.lExtraPlots[iDeadCiv]):
                    plot = gc.getMap().plot(x, y)
                    if plot.isCity():
                        city = plot.getPlotCity()
                        iOwner = city.getOwner()
                        if (
                            iOwner >= CIVILIZATIONS.majors().len()
                        ):  # if iOwner in [Civ.INDEPENDENT.value, Civ.INDEPENDENT_2.value, Civ.BARBARIAN.value]: #remove in vanilla
                            cityList.append(tPlot)
                        else:
                            iMinNumCitiesOwner = 3
                            # iOwnerStability = utils.getStability(iOwner)
                            iOwnerStability = gc.getPlayer(iOwner).getStability()
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
                                        and tPlot
                                        != CIV_CAPITAL_LOCATIONS[get_civ_by_id(iOwner)].to_tuple()
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
                                if not bSpecialRespawn and iOwnerStability < 10:
                                    if (
                                        tPlot
                                        == CIV_CAPITAL_LOCATIONS[
                                            get_civ_by_id(iDeadCiv)
                                        ].to_tuple()
                                    ):
                                        if tPlot not in cityList:
                                            cityList.append(tPlot)
                if len(cityList) >= iMinNumCities:
                    if bSpecialRespawn or (
                        gc.getGame().getSorenRandNum(100, "roll")
                        < CIV_RESPAWNING_THRESHOLD[get_civ_by_id(iDeadCiv)]
                    ):
                        self.setRebelCities(cityList)
                        self.setRebelCiv(iDeadCiv)  # for popup and CollapseCapitals()
                        return iDeadCiv
        return -1

    def suppressResurection(self, iDeadCiv):
        lSuppressList = self.getRebelSuppress()
        lCityList = self.getRebelCities()
        lCityCount = [0] * CIVILIZATIONS.majors().len()

        for (x, y) in lCityList:
            iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
            if iOwner < CIVILIZATIONS.majors().len():
                lCityCount[iOwner] += 1

        iHuman = utils.getHumanID()
        for iCiv in CIVILIZATIONS.majors().ids():
            # Absinthe: have to reset the suppress values
            lSuppressList[iCiv] = 0
            if iCiv != iHuman:
                if lCityCount[iCiv] > 0:
                    # Absinthe: for the AI there is 30% chance that the actual respawn does not happen (under these suppress situations), only some revolt in the corresponding cities
                    iActualSpawnChance = gc.getGame().getSorenRandNum(100, "odds")
                    if iActualSpawnChance > 70:
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
        iHuman = utils.getHumanID()
        lCityCount = [0] * CIVILIZATIONS.majors().len()
        for (x, y) in lCityList:
            iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
            if iOwner < CIVILIZATIONS.majors().len():
                lCityCount[iOwner] += 1

        # Absinthe: if any of the AI civs didn't manage to suppress it, there is resurrection
        for iCiv in CIVILIZATIONS.majors().ids():
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
                    CyTranslator().getText("TXT_KEY_SUPPRESSED_RESURRECTION", ()),
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
        iGameTurn = gc.getGame().getGameTurn()
        utils.setLastRespawnTurn(iDeadCiv, iGameTurn)

        # Absinthe: update province status before the cities are flipped, so potential provinces will update if there are cities in them
        self.pm.onRespawn(
            iDeadCiv
        )  # Absinthe: resetting the original potential provinces, and adding special province changes on respawn (Cordoba)

        # Absinthe: we shouldn't get a previous leader on respawn - would be changed to a newer one in a couple turns anyway
        # 			instead we have a random chance to remain with the leader before the collapse, or to switch to the next one
        leaders = CIVILIZATIONS[iDeadCiv].leaders.late
        if leaders:
            # no change if we are already at the last leader
            # for iLeader in range(len(tLeaderCiv) - 1):
            for leader in leaders[:-1]:
                if pDeadCiv.getLeader() == leader[0].value:
                    iRnd = gc.getGame().getSorenRandNum(5, "odds")
                    if iRnd > 1:  # 60% chance for the next leader
                        pDeadCiv.setLeader(leader[0].value)
                    break
        # Absinthe: old code for leader-change on respawn
        # if (len(tLeaders[iDeadCiv]) > 1):
        # 	iLen = len(tLeaders[iDeadCiv])
        # 	iRnd = gc.getGame().getSorenRandNum(iLen, 'odds')
        # 	for k in range(iLen):
        # 		iLeader = (iRnd + k) % iLen
        # 		if (pDeadCiv.getLeader() != tLeaders[iDeadCiv][iLeader]):
        # 			pDeadCiv.setLeader(tLeaders[iDeadCiv][iLeader])
        # 			break

        for iCiv in CIVILIZATIONS.majors().ids():
            if iCiv != iDeadCiv:
                if teamDeadCiv.isAtWar(iCiv):
                    teamDeadCiv.makePeace(iCiv)
        self.setNumCities(iDeadCiv, 0)  # reset collapse condition

        # Absinthe: reset vassalage and update dynamic civ names
        for iOtherCiv in CIVILIZATIONS.majors().ids():
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
        self.setLatestRebellionTurn(iDeadCiv, gc.getGame().getGameTurn())
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

            if iOwner >= CIVILIZATIONS.majors().len():
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
                    rndNum = gc.getGame().getSorenRandNum(100, "odds")
                    if (
                        rndNum >= CIV_AI_STOP_BIRTH_THRESHOLD[get_civ_by_id(iOwner)]
                        and not bOwnerHumanVassal
                        and not bAlreadyVassal
                    ):  # if bOwnerHumanVassal is True, it will skip to the 3rd condition, as bOwnerVassal is True as well
                        if not teamOwner.isAtWar(iDeadCiv):
                            teamOwner.declareWar(iDeadCiv, False, -1)
                        bAtWar = True
                    # Absinthe: do we really want to auto-vassal them on respawn? why?
                    # 			set it to 0 from 60 temporarily (so it's never True), as a quick fix until the mechanics are revised
                    elif rndNum <= 0 - (CIV_AI_STOP_BIRTH_THRESHOLD[get_civ_by_id(iOwner)] / 2):
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
                    for iTech in range(xml.iNumTechs):
                        if teamOwner.isHasTech(iTech):
                            teamDeadCiv.setHasTech(iTech, True, iDeadCiv, False, False)

        # all techs added from minor civs
        for iTech in range(xml.iNumTechs):
            if (
                teamBarbarian.isHasTech(iTech)
                or teamIndependent.isHasTech(iTech)
                or teamIndependent2.isHasTech(iTech)
                or teamIndependent3.isHasTech(iTech)
                or teamIndependent4.isHasTech(iTech)
            ):
                teamDeadCiv.setHasTech(iTech, True, iDeadCiv, False, False)

        self.moveBackCapital(iDeadCiv)

        # add former colonies that are still free
        # 3Miro: no need, we don't have "colonies", this causes trouble with Cordoba's special respawn, getting cities back from Iberia
        # colonyList = []
        # for iIndCiv in CIVILIZATIONS.minors().ids():
        # 	if gc.getPlayer(iIndCiv).isAlive():
        # 		for indepCity in utils.getCityList(iIndCiv):
        # 			if indepCity.getOriginalOwner() == iDeadCiv:
        # 				indX = indepCity.getX()
        # 				indY = indepCity.getY()
        # 				tCitySpot = ( indX, indY );
        # 				if gc.getPlayer(iDeadCiv).getSettlersMaps( WORLD_HEIGHT-indY-1, indX ) >= 90:
        # 					if tCitySpot not in lCityList and indepCity not in colonyList:
        # 						colonyList.append(indepCity)
        # if colonyList:
        # 	for colony in colonyList:
        # 		iOwner = colony.getOwner()
        # 		tColony = (colony.getX(), colony.getY())
        # 		utils.cultureManager(tColony, 100, iDeadCiv, iOwner, False, True, True)
        # 		utils.flipUnitsInCityBefore(tColony, iDeadCiv, iOwner)
        # 		self.setTempFlippingCity(tColony)
        # 		utils.flipCity(tColony, 0, 0, iDeadCiv, [iOwner])
        # 		utils.flipUnitsInArea((tColony[0]-2, tColony[1]-2), (tColony[0]+2, tColony[1]+2), iDeadCiv, iOwner, True, False)

        if utils.isActive(iHuman):
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
        # if (bHuman == True):
        # 	self.rebellionPopup(iDeadCiv)
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
        tiles = CIV_NEW_CAPITAL_LOCATIONS[get_civ_by_id(iCiv)]
        if tiles is None:
            tiles = [CIV_CAPITAL_LOCATIONS[get_civ_by_id(iCiv)]]

        # TODO: remove for/else implementation
        for tile in tiles:
            plot = gc.getMap().plot(*tile.to_tuple())
            if plot.isCity():
                newCapital = plot.getPlotCity()
                if newCapital.getOwner() == iCiv:
                    if not newCapital.hasBuilding(xml.iPalace):
                        for city in cityList:
                            city.setHasRealBuilding((xml.iPalace), False)
                        newCapital.setHasRealBuilding((xml.iPalace), True)
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
                        loopCity.setHasRealBuilding((xml.iPalace), False)
                bestCity.setHasRealBuilding((xml.iPalace), True)
                self.makeResurectionUnits(iCiv, bestCity.getX(), bestCity.getY())

    def makeResurectionUnits(self, iPlayer, iX, iY):
        if iPlayer == Civ.CORDOBA.value:
            utils.makeUnit(xml.iSettler, Civ.CORDOBA.value, (iX, iY), 2)
            utils.makeUnit(xml.iCrossbowman, Civ.CORDOBA.value, (iX, iY), 2)
            utils.makeUnit(xml.iIslamicMissionary, Civ.CORDOBA.value, (iX, iY), 1)

    def convertBackCulture(self, iCiv):
        # 3Miro: same as Normal Areas in Resurrection
        # Sedna17: restored to be normal areas, not core
        # tTopLeft = tCoreAreasTL[iCiv]
        # tBottomRight = tCoreAreasBR[iCiv]
        tTopLeft = Consts.tNormalAreasTL[iCiv]
        tBottomRight = Consts.tNormalAreasBR[iCiv]
        cityList = []
        # collect all the cities in the region
        for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
            pCurrent = gc.getMap().plot(x, y)
            if pCurrent.isCity():
                for (ix, iy) in utils.surroundingPlots((x, y)):
                    pCityArea = gc.getMap().plot(ix, iy)
                    iCivCulture = pCityArea.getCulture(iCiv)
                    iLoopCivCulture = 0
                    for civilization in CIVILIZATIONS.minors().ids():
                        iLoopCivCulture += pCityArea.getCulture(civilization)
                        pCityArea.setCulture(civilization, 0, True)
                    pCityArea.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

                city = pCurrent.getPlotCity()
                iCivCulture = city.getCulture(iCiv)
                iLoopCivCulture = 0
                for civilization in CIVILIZATIONS.minors().ids():
                    iLoopCivCulture += pCityArea.getCulture(civilization)
                    pCityArea.setCulture(civilization, 0, True)
                city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

    def initBirth(self, iCurrentTurn, iBirthYear, iCiv):
        iHuman = utils.getHumanID()
        if iCurrentTurn == iBirthYear - 1 + self.getSpawnDelay(iCiv) + self.getFlipsDelay(iCiv):
            tCapital = CIV_CAPITAL_LOCATIONS[get_civ_by_id(iCiv)].to_tuple()
            tTopLeft = Consts.tCoreAreasTL[iCiv]
            tBottomRight = Consts.tCoreAreasBR[iCiv]
            tBroaderTopLeft = Consts.tBroaderAreasTL[iCiv]
            tBroaderBottomRight = Consts.tBroaderAreasBR[iCiv]
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
                    # if (iCiv == iNetherlands or iCiv == iPortugal): #dangerous starts
                    # 	self.setDeleteMode(0, iCiv)
                    self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
                elif bDeleteEverything:
                    self.setDeleteMode(0, iCiv)
                    # Absinthe: kill off units near the starting plot
                    utils.killAllUnitsInArea(
                        (tCapital[0] - 1, tCapital[1] - 1), (tCapital[0] + 1, tCapital[1] + 1)
                    )
                    # Absinthe: why do we flip units in these areas if we are under bDeleteEverything?
                    # for iLoopCiv in CIVILIZATIONS.ids():
                    # 	if iCiv != iLoopCiv:
                    # 		utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iLoopCiv, True, False)
                    # 		utils.flipUnitsInPlots(Consts.lExtraPlots[iCiv], iCiv, iLoopCiv, True, False)
                    for (x, y) in utils.surroundingPlots(tCapital):
                        plot = gc.getMap().plot(x, y)
                        # self.moveOutUnits(x, y, tCapital[0], tCapital[1])
                        if plot.isCity():
                            plot.eraseAIDevelopment()  # new function, similar to erase but won't delete rivers, resources and features
                        for civilization in CIVILIZATIONS.ids():
                            if iCiv != civilization:
                                plot.setCulture(civilization, 0, True)
                        # pCurrent.setCulture(iCiv,10,True)
                        plot.setOwner(-1)
                    self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
                else:
                    self.birthInForeignBorders(
                        iCiv,
                        tTopLeft,
                        tBottomRight,
                        tBroaderTopLeft,
                        tBroaderBottomRight,
                        tCapital,
                    )
            else:
                self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)

        # 3MiroCrusader modification. Crusaders cannot change nations.
        # Sedna17: Straight-up no switching within 40 turns of your birth
        if iCurrentTurn == iBirthYear + self.getSpawnDelay(iCiv):
            if (
                gc.getPlayer(iCiv).isAlive()
                and not self.getAlreadySwitched()
                and iCurrentTurn > CIV_BIRTHDATE[get_civ_by_id(iHuman)] + 40
                and not gc.getPlayer(iHuman).getIsCrusader()
            ):
                self.newCivPopup(iCiv)

    ##	def moveOutUnits(self, x, y, tCapitalX, tCapitalY) #not used
    ##		pCurrent=gc.getMap().plot(x, y)
    ##		if pCurrent.getNumUnits() > 0:
    ##			unit = pCurrent.getUnit(0)
    ##			tDestination = (-1, -1)
    ##			plotList = []
    ##			if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
    ##				plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodPlots, [] )
    ##				#plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodOwnedPlots, [] )
    ##			else: #sea unit
    ##				plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodOwnedPlots, [] )
    ##
    ##			if plotList:
    ##				tPlot = utils.getRandomEntry(plotList)
    ##			if tPlot != (-1, -1):
    ##				for i in range(pCurrent.getNumUnits()):
    ##					unit = pCurrent.getUnit(0)
    ##					unit.setXY(tPlot[0], tPlot[1])

    def deleteMode(self, iCurrentPlayer):
        iCiv = self.getDeleteMode(0)
        tCapital = CIV_CAPITAL_LOCATIONS[get_civ_by_id(iCiv)].to_tuple()
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
                for iLoopCiv in CIVILIZATIONS.ids():
                    if iLoopCiv != iCiv:
                        plot.setCulture(iLoopCiv, 0, True)
                    # else:
                    # 	if plot.getCulture(iCiv) < 4000:
                    # 		plot.setCulture(iCiv, 4000, True)
                # plot.setOwner(-1)
                plot.setOwner(iCiv)

        # Absinthe: what's this +-11? do we really want to move all flipped units in the initial turn to the starting plot??

    # 	for (x, y) in utils.surroundingPlots(tCapital, 11): # must include the distance from Sogut to the Caspius
    # 		if tCapital != (x, y):
    # 			plot = gc.getMap().plot(x, y)
    # 			if plot.getNumUnits() > 0 and not plot.isWater():
    # 				unit = plot.getUnit(0)
    # 				if unit.getOwner() == iCiv:
    # 					for i in range(plot.getNumUnits()):
    # 						unit = plot.getUnit(0)
    # 						unit.setXYOld(tCapital[0], tCapital[1])
    # may intersect plot close to tCapital
    ##							for (i, j) in utils.surroundingPlots((x, y), 6):
    ##								pCurrentFar = gc.getMap().plot(i, j)
    ##								if pCurrentFar.getNumUnits() == 0:
    ##									pCurrentFar.setRevealed(iCiv, False, True, -1);

    def birthInFreeRegion(self, iCiv, tCapital, tTopLeft, tBottomRight):
        startingPlot = gc.getMap().plot(tCapital[0], tCapital[1])
        if self.getFlipsDelay(iCiv) == 0:
            iFlipsDelay = self.getFlipsDelay(iCiv) + 2
            ##			if startingPlot.getNumUnits() > 0:
            ##				unit = startingPlot.getUnit(0)
            ##				if unit.getOwner() != utils.getHumanID() or iCiv == utils.getHumanID(): #2nd check needed because in delete mode it finds the civ's (human's) units placed
            ##					for i in range(startingPlot.getNumUnits()):
            ##						unit = startingPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
            ##						unit.kill(False, iCiv)
            ##					iFlipsDelay = self.getFlipsDelay(iCiv) + 2
            ##					#utils.debugTextPopup( 'birthInFreeRegion in starting location' )
            ##				else: #search another place
            ##					plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.goodPlots, [] )
            ##					if plotList:
            ##						tPlot = utils.getRandomEntry(plotList)
            ##						self.createStartingUnits(iCiv, tPlot)
            ##						tCapital = tPlot
            ##						#utils.debugTextPopup( 'birthInFreeRegion in another location' )
            ##						iFlipsDelay = self.getFlipsDelay(iCiv) + 1 #add delay before flipping other cities
            ##					else:
            ##						if self.getSpawnDelay(iCiv) < 10: #wait
            ##							iSpawnDelay = self.getSpawnDelay(iCiv) + 1
            ##							self.setSpawnDelay(iCiv, iSpawnDelay)
            ##			else:
            ##				iFlipsDelay = self.getFlipsDelay(iCiv) + 2

            if iFlipsDelay > 0:
                # startingPlot.setImprovementType(-1)

                # gc.getPlayer(iCiv).found(tCapital[0], tCapital[1])
                # gc.getMap().plot(tCapital[0], tCapital[1]).setRevealed(iCiv, False, True, -1);
                # gc.getMap().plot(tCapital[0], tCapital[1]).setRevealed(iCiv, True, True, -1);

                # Absinthe: kill off units near the starting plot
                utils.killAllUnitsInArea(
                    (tCapital[0] - 1, tCapital[1] - 1), (tCapital[0] + 1, tCapital[1] + 1)
                )
                self.createStartingUnits(iCiv, (tCapital[0], tCapital[1]))

                # if (self.getDeleteMode(0) == iCiv):
                # 	self.createStartingWorkers(iCiv, tCapital) #XXX bugfix? no!

                ##				settlerPlot = gc.getMap().plot( tCapital[0], tCapital[1] )
                ##				for i in range(settlerPlot.getNumUnits()):
                ##					unit = settlerPlot.getUnit(i)
                ##					if unit.getUnitType() == xml.iSettler:
                ##						break
                ##				unit.found()

                # Absinthe: there was another mistake here with barbarian and indy unit flips...
                # 			we don't simply want to check an area based on distance from capital, as it might lead out from the actual spawn area
                # 			so we only check plots which are in the core area: in 4 distance for barb units, 2 distance for indies
                lPlotBarbFlip = []
                lPlotIndyFlip = []
                # if inside the core rectangle and extra plots, and in 4 (barb) or 2 (indy) distance from the starting plot, append to barb or indy flip zone
                lPlots = utils.getPlotList(tTopLeft, tBottomRight) + Consts.lExtraPlots[iCiv]
                lSurroundingPlots4 = utils.surroundingPlots(tCapital, 4)
                lSurroundingPlots2 = utils.surroundingPlots(tCapital, 2)
                for tPlot in lPlots:
                    if tPlot in lSurroundingPlots2:
                        lPlotIndyFlip.append(tPlot)
                        lPlotBarbFlip.append(tPlot)
                    elif tPlot in lSurroundingPlots4:
                        lPlotBarbFlip.append(tPlot)
                # remaining barbs in the region: killed for the human player, flipped for the AI
                if iCiv == utils.getHumanID():
                    utils.killUnitsInPlots(lPlotBarbFlip, Civ.BARBARIAN.value)
                else:
                    utils.flipUnitsInPlots(lPlotBarbFlip, iCiv, Civ.BARBARIAN.value, True, True)
                for iIndyCiv in CIVILIZATIONS.independents().ids():
                    # remaining independents in the region: killed for the human player, flipped for the AI
                    if iCiv == utils.getHumanID():
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
            if iCiv != utils.getHumanID():
                utils.flipUnitsInArea(
                    tTopLeft, tBottomRight, iCiv, Civ.BARBARIAN.value, False, True
                )  # remaining barbs in the region now belong to the new civ
                utils.flipUnitsInPlots(
                    Consts.lExtraPlots[iCiv], iCiv, Civ.BARBARIAN.value, False, True
                )  # remaining barbs in the region now belong to the new civ
            for iIndyCiv in CIVILIZATIONS.independents().ids():
                if iCiv != utils.getHumanID():
                    utils.flipUnitsInArea(
                        tTopLeft, tBottomRight, iCiv, iIndyCiv, False, False
                    )  # remaining independents in the region now belong to the new civ
                    utils.flipUnitsInPlots(
                        Consts.lExtraPlots[iCiv], iCiv, iIndyCiv, False, False
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
                self.createStartingWorkers(iCiv, (capital.getX(), capital.getY()))

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
            # utils.debugTextPopup( 'iConverted OK for placing units' )
            # Absinthe: there is an issue that core area is not calculated correctly for flips, as the additional tiles in lExtraPlots are not checked here
            # 			so if all flipped cities are outside of the core area (they are in the "exceptions"), the civ will start without it's starting units and techs
            plotList = utils.squareSearch(tTopLeft, tBottomRight, utils.ownedCityPlots, iCiv)
            # Absinthe: add the exception plots
            for tPlot in Consts.lExtraPlots[iCiv]:
                plot = gc.getMap().plot(tPlot[0], tPlot[1])
                if plot.getOwner() == iCiv:
                    if plot.isCity():
                        plotList.append(tPlot)
            if plotList:
                tPlot = utils.getRandomEntry(plotList)
                self.createStartingUnits(iCiv, tPlot)
                # utils.debugTextPopup( 'birthInForeignBorders after a flip' )
                self.assignTechs(iCiv)
                utils.setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
                utils.clearPlague(iCiv)
                # gc.getPlayer(iCiv).changeAnarchyTurns(1)
            utils.flipUnitsInArea(
                tTopLeft, tBottomRight, iCiv, Civ.BARBARIAN.value, False, True
            )  # remaining barbs in the region now belong to the new civ
            utils.flipUnitsInPlots(
                Consts.lExtraPlots[iCiv], iCiv, Civ.BARBARIAN.value, False, True
            )  # remaining barbs in the region now belong to the new civ
            for iIndyCiv in CIVILIZATIONS.independents().ids():
                utils.flipUnitsInArea(
                    tTopLeft, tBottomRight, iCiv, iIndyCiv, False, False
                )  # remaining independents in the region now belong to the new civ
                utils.flipUnitsInPlots(
                    Consts.lExtraPlots[iCiv], iCiv, iIndyCiv, False, False
                )  # remaining independents in the region now belong to the new civ

        else:  # search another place
            # Absinthe: there is an issue that core area is not calculated correctly for flips, as the additional tiles in lExtraPlots are not checked here
            # 			so if all flipped cities are outside of the core area (they are in the "exceptions"), the civ will start without it's starting units and techs
            plotList = utils.squareSearch(tTopLeft, tBottomRight, utils.goodPlots, [])
            # Absinthe: add the exception plots

            for tPlot in Consts.lExtraPlots[iCiv]:
                plot = gc.getMap().plot(tPlot[0], tPlot[1])
                if (plot.isHills() or plot.isFlatlands()) and not plot.isImpassable():
                    if not plot.isUnit():
                        if (
                            plot.getTerrainType()
                            not in [
                                Terrain.DESERT.value,
                                Terrain.TUNDRA.value,
                            ]
                            and plot.getFeatureType() not in [xml.iMarsh, xml.iJungle]
                        ):
                            if plot.countTotalCulture() == 0:
                                plotList.append(tPlot)
            rndNum = gc.getGame().getSorenRandNum(len(plotList), "searching another free plot")
            if plotList:
                tPlot = utils.getRandomEntry(plotList)
                self.createStartingUnits(iCiv, tPlot)
                # utils.debugTextPopup( 'birthInForeignBorders in another location' )
                self.assignTechs(iCiv)
                utils.setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
                utils.clearPlague(iCiv)
            else:
                plotList = utils.squareSearch(
                    tBroaderTopLeft, tBroaderBottomRight, utils.goodPlots, []
                )
                if plotList:
                    tPlot = utils.getRandomEntry(plotList)
                    self.createStartingUnits(iCiv, tPlot)
                    self.createStartingWorkers(iCiv, tPlot)
                    # utils.debugTextPopup( 'birthInForeignBorders in a broader area' )
                    self.assignTechs(iCiv)
                    utils.setPlagueCountdown(iCiv, -PLAGUE_IMMUNITY)
                    utils.clearPlague(iCiv)
            utils.flipUnitsInArea(
                tTopLeft, tBottomRight, iCiv, Civ.BARBARIAN.value, True, True
            )  # remaining barbs in the region now belong to the new civ
            utils.flipUnitsInPlots(
                Consts.lExtraPlots[iCiv], iCiv, Civ.BARBARIAN.value, True, True
            )  # remaining barbs in the region now belong to the new civ
            for iIndyCiv in CIVILIZATIONS.independents().ids():
                utils.flipUnitsInArea(
                    tTopLeft, tBottomRight, iCiv, iIndyCiv, True, False
                )  # remaining independents in the region now belong to the new civ
                utils.flipUnitsInPlots(
                    Consts.lExtraPlots[iCiv], iCiv, iIndyCiv, True, False
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
        lPlots = utils.getPlotList(tTopLeft, tBottomRight) + Consts.lExtraPlots[iCiv]
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
                iHuman = utils.getHumanID()
                iOwner = loopCity.getOwner()
                iCultureChange = 0  # if 0, no flip; if > 0, flip will occur with the value as variable for utils.CultureManager()

                if iOwner >= CIVILIZATIONS.majors().len():
                    # utils.debugTextPopup( 'BARB' )
                    iCultureChange = 100
                # case 2: human city
                elif iOwner == iHuman and not loopCity.isCapital():
                    if iNumHumanCities == 0:
                        iNumHumanCities += 1
                        # self.flipPopup(iCiv, tTopLeft, tBottomRight)
                # case 3: other
                elif (
                    not loopCity.isCapital()
                ):  # 3Miro: this keeps crashing in the C++, makes no sense
                    # elif ( True ): #utils.debugTextPopup( 'OTHER' )
                    if iConvertedCitiesCount < 6:  # there won't be more than 5 flips in the area
                        # utils.debugTextPopup( 'iConvertedCities OK' )
                        iCultureChange = 50
                        if (
                            gc.getGame().getGameTurn() <= CIV_BIRTHDATE[get_civ_by_id(iCiv)] + 5
                        ):  # if we're during a birth
                            rndNum = gc.getGame().getSorenRandNum(100, "odds")
                            # 3Miro: I don't know why the iOwner check is needed below, but the module crashes sometimes
                            if (
                                iOwner > -1
                                and iOwner < CIVILIZATIONS.majors().len()
                                and rndNum >= CIV_AI_STOP_BIRTH_THRESHOLD[get_civ_by_id(iOwner)]
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
                                                iCiv,
                                                CIV_CAPITAL_LOCATIONS[
                                                    get_civ_by_id(iCiv)
                                                ].to_tuple(),
                                            )

                if iCultureChange > 0:
                    utils.cultureManager(
                        (loopX, loopY), iCultureChange, iCiv, iOwner, True, False, False
                    )
                    # gc.getMap().plot(cityList[i].getX(),cityList[i].getY()).setImprovementType(-1)

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
                    CyTranslator().getText("TXT_KEY_FLIP_TO_US", ()),
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

        lPlots = utils.getPlotList(tTopLeft, tBottomRight) + Consts.lExtraPlots[iCiv]
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
            return utils.getRandomEntry(seaPlotList)
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
        if self.canSpecialRespawn(Civ.CASTILLE.value, iGameTurn, 25):
            # respawn as the Castile/Aragon Union
            if DateTurn.i1470AD < iGameTurn < DateTurn.i1580AD and iGameTurn % 5 == 0:
                return Civ.CASTILLE.value
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
        if iGameTurn <= CIV_BIRTHDATE[get_civ_by_id(iPlayer)] + 25:
            return False
        if iGameTurn <= (utils.getLastTurnAlive(iPlayer) + iLastAliveInterval):
            return False
        return True

    def initMinorBetrayal(self, iCiv):
        iHuman = utils.getHumanID()
        plotList = utils.squareSearch(
            Consts.tCoreAreasTL[iCiv], Consts.tCoreAreasBR[iCiv], utils.outerInvasion, []
        )
        if plotList:
            tPlot = utils.getRandomEntry(plotList)
            self.createAdditionalUnits(iCiv, tPlot)
            self.unitsBetrayal(
                iCiv, iHuman, Consts.tCoreAreasTL[iCiv], Consts.tCoreAreasBR[iCiv], tPlot
            )

    def initBetrayal(self):
        iHuman = utils.getHumanID()
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
            tPlot = utils.getRandomEntry(plotList)
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
                CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL", ()),
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
                CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL_NEW", ()),
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
                        rndNum = gc.getGame().getSorenRandNum(100, "betrayal")
                        if rndNum >= iBetrayalThreshold:
                            if unit.getDomainType() == DomainTypes.DOMAIN_LAND:  # land unit
                                iUnitType = unit.getUnitType()
                                unit.kill(False, iNewOwner)
                                utils.makeUnit(iUnitType, iNewOwner, tPlot, 1)
                                i = i - 1

    def createAdditionalUnits(self, iCiv, tPlot):
        # additional starting units if someone declares war on the civ during birth
        iHuman = utils.getHumanID()
        # significant number of units for the AI
        if iCiv != iHuman:
            if iCiv == Civ.ARABIA.value:
                utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
            elif iCiv == Civ.BULGARIA.value:
                utils.makeUnit(xml.iBulgarianKonnik, iCiv, tPlot, 2)
            elif iCiv == Civ.CORDOBA.value:
                utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
            elif iCiv == Civ.VENECIA.value:
                utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
            elif iCiv == Civ.BURGUNDY.value:
                utils.makeUnit(xml.iLancer, iCiv, tPlot, 3)
            elif iCiv == Civ.GERMANY.value:
                utils.makeUnit(xml.iLancer, iCiv, tPlot, 3)
            elif iCiv == Civ.NOVGOROD.value:
                utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
            elif iCiv == Civ.NORWAY.value:
                utils.makeUnit(xml.iVikingBerserker, iCiv, tPlot, 3)
            elif iCiv == Civ.KIEV.value:
                utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
            elif iCiv == Civ.HUNGARY.value:
                utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
            elif iCiv == Civ.CASTILLE.value:
                utils.makeUnit(xml.iLancer, iCiv, tPlot, 4)
            elif iCiv == Civ.DENMARK.value:
                utils.makeUnit(xml.iDenmarkHuskarl, iCiv, tPlot, 3)
            elif iCiv == Civ.SCOTLAND.value:
                utils.makeUnit(xml.iAxeman, iCiv, tPlot, 4)
            elif iCiv == Civ.POLAND.value:
                utils.makeUnit(xml.iLancer, iCiv, tPlot, 3)
            elif iCiv == Civ.GENOA.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
            elif iCiv == Civ.MOROCCO.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
            elif iCiv == Civ.ENGLAND.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
            elif iCiv == Civ.PORTUGAL.value:
                utils.makeUnit(xml.iPortugalFootKnight, iCiv, tPlot, 4)
            elif iCiv == Civ.ARAGON.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 4)
            elif iCiv == Civ.SWEDEN.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 4)
            elif iCiv == Civ.PRUSSIA.value:
                utils.makeUnit(xml.iTeutonic, iCiv, tPlot, 3)
            elif iCiv == Civ.LITHUANIA.value:
                utils.makeUnit(xml.iLithuanianBajoras, iCiv, tPlot, 3)
            elif iCiv == Civ.AUSTRIA.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 4)
            elif iCiv == Civ.OTTOMAN.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
            elif iCiv == Civ.MOSCOW.value:
                utils.makeUnit(xml.iMoscowBoyar, iCiv, tPlot, 3)
            elif iCiv == Civ.DUTCH.value:
                utils.makeUnit(xml.iNetherlandsGrenadier, iCiv, tPlot, 4)
        # less for the human player
        else:
            if iCiv == Civ.ARABIA.value:
                utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 2)
            elif iCiv == Civ.BULGARIA.value:
                utils.makeUnit(xml.iBulgarianKonnik, iCiv, tPlot, 1)
            elif iCiv == Civ.CORDOBA.value:
                utils.makeUnit(xml.iAxeman, iCiv, tPlot, 1)
            elif iCiv == Civ.VENECIA.value:
                utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
            elif iCiv == Civ.BURGUNDY.value:
                utils.makeUnit(xml.iLancer, iCiv, tPlot, 1)
            elif iCiv == Civ.GERMANY.value:
                utils.makeUnit(xml.iLancer, iCiv, tPlot, 1)
            elif iCiv == Civ.NOVGOROD.value:
                utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 1)
            elif iCiv == Civ.NORWAY.value:
                utils.makeUnit(xml.iVikingBerserker, iCiv, tPlot, 1)
            elif iCiv == Civ.KIEV.value:
                utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 2)
            elif iCiv == Civ.HUNGARY.value:
                utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 2)
            elif iCiv == Civ.CASTILLE.value:
                utils.makeUnit(xml.iLancer, iCiv, tPlot, 1)
            elif iCiv == Civ.DENMARK.value:
                utils.makeUnit(xml.iDenmarkHuskarl, iCiv, tPlot, 1)
            elif iCiv == Civ.SCOTLAND.value:
                utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
            elif iCiv == Civ.POLAND.value:
                utils.makeUnit(xml.iLancer, iCiv, tPlot, 1)
            elif iCiv == Civ.GENOA.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 1)
            elif iCiv == Civ.MOROCCO.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 1)
            elif iCiv == Civ.ENGLAND.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 1)
            elif iCiv == Civ.PORTUGAL.value:
                utils.makeUnit(xml.iPortugalFootKnight, iCiv, tPlot, 1)
            elif iCiv == Civ.ARAGON.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
            elif iCiv == Civ.SWEDEN.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 1)
            elif iCiv == Civ.PRUSSIA.value:
                utils.makeUnit(xml.iTeutonic, iCiv, tPlot, 1)
            elif iCiv == Civ.LITHUANIA.value:
                utils.makeUnit(xml.iLithuanianBajoras, iCiv, tPlot, 1)
            elif iCiv == Civ.AUSTRIA.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
            elif iCiv == Civ.OTTOMAN.value:
                utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 1)
            elif iCiv == Civ.MOSCOW.value:
                utils.makeUnit(xml.iMoscowBoyar, iCiv, tPlot, 1)
            elif iCiv == Civ.DUTCH.value:
                utils.makeUnit(xml.iNetherlandsGrenadier, iCiv, tPlot, 2)

    def createStartingUnits(self, iCiv, tPlot):
        # set the provinces
        self.pm.onSpawn(iCiv)
        iHuman = utils.getHumanID()
        # Change here to make later starting civs work
        if iCiv == Civ.ARABIA.value:
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 7)
            utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSpearman, iCiv, tPlot, 2)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 2)
                utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
                utils.makeUnit(xml.iSpearman, iCiv, tPlot, 2)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
        elif iCiv == Civ.BULGARIA.value:
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iBulgarianKonnik, iCiv, tPlot, 5)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iArcher, iCiv, tPlot, 1)
                utils.makeUnit(xml.iSpearman, iCiv, tPlot, 2)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
        elif iCiv == Civ.CORDOBA.value:
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 3)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
            utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 3)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
                utils.makeUnit(xml.iAxeman, iCiv, tPlot, 1)
                utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 2)
            # so the human player can raid further north rather than sit and wait for Spain
            if iCiv == iHuman:
                utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 3)
        elif iCiv == Civ.VENECIA.value:
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
            utils.makeUnit(xml.iSpearman, iCiv, tPlot, 1)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
            tSeaPlot = self.findSeaPlots((57, 35), 2)
            if tSeaPlot:
                utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1)
                pVenecia.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pVenecia.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_ESCORT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iArcher, iCiv, tSeaPlot, 1)
                pVenecia.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iSpearman, iCiv, tSeaPlot, 1)
        elif iCiv == Civ.BURGUNDY.value:
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
            utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
            utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
        elif iCiv == Civ.GERMANY.value:
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
                utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
        elif iCiv == Civ.NOVGOROD.value:
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 3)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iAxeman, iCiv, tPlot, 1)
            utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 1)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
        elif iCiv == Civ.NORWAY.value:
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iVikingBerserker, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 1)
            tSeaPlot = self.findSeaPlots(tPlot, 2)
            if tSeaPlot:
                pNorway.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pNorway.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_ESCORT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pNorway.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_ESCORT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iArcher, iCiv, tSeaPlot, 1)
        elif iCiv == Civ.KIEV.value:
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 3)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iArcher, iCiv, tPlot, 3)
                utils.makeUnit(xml.iSpearman, iCiv, tPlot, 3)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
        elif iCiv == Civ.HUNGARY.value:
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
                utils.makeUnit(xml.iSpearman, iCiv, tPlot, 2)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
        elif iCiv == Civ.CASTILLE.value:
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCatapult, iCiv, tPlot, 1)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 1)
                utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
                utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
        elif iCiv == Civ.DENMARK.value:
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iDenmarkHuskarl, iCiv, tPlot, 4)
            tSeaPlot = self.findSeaPlots((60, 57), 2)
            if tSeaPlot:
                pDenmark.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pDenmark.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pDenmark.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_ESCORT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1)
        elif iCiv == Civ.SCOTLAND.value:
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
        elif iCiv == Civ.POLAND.value:
            utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
        elif iCiv == Civ.GENOA.value:
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
            tSeaPlot = self.findSeaPlots(tPlot, 2)
            if tSeaPlot:
                pGenoa.initUnit(
                    xml.iWarGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_ESCORT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pGenoa.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1)
        elif iCiv == Civ.MOROCCO.value:
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
            utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 1)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
                utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 2)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
        elif iCiv == Civ.ENGLAND.value:
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iLongSwordsman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
            tSeaPlot = self.findSeaPlots((43, 53), 1)
            if tSeaPlot:
                pEngland.initUnit(
                    xml.iGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pEngland.initUnit(
                    xml.iWarGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_ESCORT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
                utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
                utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
                utils.makeUnit(xml.iLongSwordsman, iCiv, tPlot, 2)
        elif iCiv == Civ.PORTUGAL.value:
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iPortugalFootKnight, iCiv, tPlot, 4)
            utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
            utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
        elif iCiv == Civ.ARAGON.value:
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iAragonAlmogavar, iCiv, tPlot, 5)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
            # Look for a sea plot close to the coast
            tSeaPlot = self.findSeaPlots((42, 29), 1)
            if tSeaPlot:
                pAragon.initUnit(
                    xml.iWarGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_ESCORT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pAragon.initUnit(
                    xml.iWarGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_ESCORT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pAragon.initUnit(
                    xml.iCogge,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1)
        elif iCiv == Civ.SWEDEN.value:
            utils.makeUnit(xml.iLongSwordsman, iCiv, tPlot, 3)
            utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 1)
            utils.makeUnit(xml.iKnight, iCiv, tPlot, 1)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
            utils.makeUnit(xml.iArbalest, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
            tSeaPlot = self.findSeaPlots((69, 65), 2)
            if tSeaPlot:
                utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1)
                pSweden.initUnit(
                    xml.iWarGalley,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_ESCORT_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pSweden.initUnit(
                    xml.iCogge,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pSweden.initUnit(
                    xml.iCogge,
                    tSeaPlot[0],
                    tSeaPlot[1],
                    UnitAITypes.UNITAI_SETTLER_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
                utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1)
                utils.makeUnit(xml.iArbalest, iCiv, tSeaPlot, 1)
        elif iCiv == Civ.PRUSSIA.value:
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(
                xml.iTeutonic, iCiv, tPlot, 3
            )  # at least one will probably leave for Crusade
            utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
            utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 3)
        elif iCiv == Civ.LITHUANIA.value:
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iLithuanianBajoras, iCiv, tPlot, 5)
            utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 3)
        elif iCiv == Civ.AUSTRIA.value:
            utils.makeUnit(xml.iArbalest, iCiv, tPlot, 4)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iMaceman, iCiv, tPlot, 3)
            utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
            utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
            utils.makeUnit(xml.iKnight, iCiv, tPlot, 4)
            utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
        elif iCiv == Civ.OTTOMAN.value:
            utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 5)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iMaceman, iCiv, tPlot, 4)
            utils.makeUnit(xml.iKnight, iCiv, tPlot, 2)
            utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
            utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
            utils.makeUnit(xml.iTurkeyGreatBombard, iCiv, tPlot, 3)
            utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 4)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iKnight, iCiv, tPlot, 2)
                utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 2)
                utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 3)
        elif iCiv == Civ.MOSCOW.value:
            utils.makeUnit(xml.iArbalest, iCiv, tPlot, 5)
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
            utils.makeUnit(xml.iMoscowBoyar, iCiv, tPlot, 5)
            utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 4)
            utils.makeUnit(xml.iMaceman, iCiv, tPlot, 3)
            utils.makeUnit(xml.iOrthodoxMissionary, iCiv, tPlot, 3)
            # additional units for the AI
            if iCiv != iHuman:
                utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
                utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
                utils.makeUnit(xml.iOrthodoxMissionary, iCiv, tPlot, 1)
                utils.makeUnit(xml.iArbalest, iCiv, tPlot, 2)
        elif iCiv == Civ.DUTCH.value:
            utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
            utils.makeUnit(xml.iMusketman, iCiv, tPlot, 8)
            utils.makeUnit(xml.iMaceman, iCiv, tPlot, 3)
            utils.makeUnit(xml.iProtestantMissionary, iCiv, tPlot, 2)
            tSeaPlot = self.findSeaPlots(tPlot, 2)
            if tSeaPlot:
                utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 2)
                utils.makeUnit(xml.iGalleon, iCiv, tSeaPlot, 2)

        self.showArea(iCiv)
        self.initContact(iCiv)

    def createStartingWorkers(self, iCiv, tPlot):
        utils.makeUnit(
            xml.iWorker,
            iCiv,
            tPlot,
            CIV_STARTING_SITUATION[utils.getScenario()][get_civ_by_id(iCiv)][
                StartingSituation.WORKERS
            ],
        )
        # Absinthe: second Ottoman spawn stack may stay, although they now spawn in Gallipoli in the first place (one plot SE)
        if iCiv == Civ.OTTOMAN.value:
            self.ottomanInvasion(iCiv, (77, 23))

    def create1200ADstartingUnits(self):
        iHuman = utils.getHumanID()
        if (
            CIV_BIRTHDATE[get_civ_by_id(iHuman)] > DateTurn.i1200AD
        ):  # so iSweden, iPrussia, iLithuania, iAustria, iTurkey, iMoscow, iDutch
            tStart = CIV_CAPITAL_LOCATIONS[get_civ_by_id(iHuman)].to_tuple()

            # Absinthe: changes in the unit positions, in order to prohibit these contacts in 1200AD
            if iHuman == Civ.SWEDEN:  # contact with Denmark
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.SWEDEN].x - 2,
                    CIV_CAPITAL_LOCATIONS[Civ.SWEDEN].y + 2,
                )
            elif iHuman == Civ.PRUSSIA:  # contact with Poland
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.PRUSSIA].x + 1,
                    CIV_CAPITAL_LOCATIONS[Civ.PRUSSIA].y + 1,
                )
            elif iHuman == Civ.LITHUANIA:  # contact with Kiev
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.LITHUANIA].x - 2,
                    CIV_CAPITAL_LOCATIONS[Civ.LITHUANIA].y,
                )
            elif iHuman == Civ.AUSTRIA:  # contact with Germany and Hungary
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.AUSTRIA].x - 3,
                    CIV_CAPITAL_LOCATIONS[Civ.AUSTRIA].y - 1,
                )
            elif iHuman == Civ.OTTOMAN:  # contact with Byzantium
                tStart = (98, 18)

            utils.makeUnit(xml.iSettler, iHuman, tStart, 1)
            utils.makeUnit(xml.iMaceman, iHuman, tStart, 1)

    def ottomanInvasion(self, iCiv, tPlot):
        utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 2)
        utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
        utils.makeUnit(xml.iKnight, iCiv, tPlot, 3)
        utils.makeUnit(xml.iTurkeyGreatBombard, iCiv, tPlot, 2)
        utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 2)

    def create500ADstartingUnits(self):
        # 3Miro: units on start (note Spearman might become an upgraded defender, tech dependent)

        utils.makeUnit(xml.iSettler, Civ.FRANCE, CIV_CAPITAL_LOCATIONS[Civ.FRANCE].to_tuple(), 3)
        utils.makeUnit(xml.iArcher, Civ.FRANCE, CIV_CAPITAL_LOCATIONS[Civ.FRANCE].to_tuple(), 4)
        utils.makeUnit(xml.iAxeman, Civ.FRANCE, CIV_CAPITAL_LOCATIONS[Civ.FRANCE].to_tuple(), 5)
        utils.makeUnit(xml.iScout, Civ.FRANCE, CIV_CAPITAL_LOCATIONS[Civ.FRANCE].to_tuple(), 1)
        utils.makeUnit(xml.iWorker, Civ.FRANCE, CIV_CAPITAL_LOCATIONS[Civ.FRANCE].to_tuple(), 2)
        utils.makeUnit(
            xml.iCatholicMissionary, Civ.FRANCE, CIV_CAPITAL_LOCATIONS[Civ.FRANCE].to_tuple(), 2
        )

        self.showArea(Civ.BYZANTIUM.value)
        self.initContact(Civ.BYZANTIUM.value)
        self.showArea(Civ.FRANCE.value)
        self.showArea(Civ.POPE.value)

        iHuman = utils.getHumanID()
        if (
            CIV_BIRTHDATE[get_civ_by_id(iHuman)] > DateTurn.i500AD
        ):  # so everyone apart from Byzantium and France
            tStart = CIV_CAPITAL_LOCATIONS[get_civ_by_id(iHuman)].to_tuple()

            # Absinthe: changes in the unit positions, in order to prohibit these contacts in 500AD
            if iHuman == Civ.ARABIA.value:  # contact with Byzantium
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.ARABIA].x,
                    CIV_CAPITAL_LOCATIONS[Civ.ARABIA].y - 10,
                )
            elif iHuman == Civ.BULGARIA.value:  # contact with Byzantium
                tStart = (
                    CIV_CAPITAL_LOCATIONS[Civ.BULGARIA].x,
                    CIV_CAPITAL_LOCATIONS[Civ.BULGARIA].y + 1,
                )
            elif iHuman == Civ.OTTOMAN.value:  # contact with Byzantium
                tStart = (97, 23)

            utils.makeUnit(xml.iSettler, iHuman, tStart, 1)
            utils.makeUnit(xml.iSpearman, iHuman, tStart, 1)

    def assign1200ADtechs(self, iCiv):
        # As a temporary solution, everyone gets Aragon's starting techs
        teamCiv = gc.getTeam(iCiv)
        for iTech in range(xml.iFarriers + 1):
            teamCiv.setHasTech(iTech, True, iCiv, False, False)
        teamCiv.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
        teamCiv.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
        teamCiv.setHasTech(xml.iLiterature, True, iCiv, False, False)
        teamCiv.setHasTech(xml.iLateenSails, True, iCiv, False, False)
        teamCiv.setHasTech(xml.iMapMaking, True, iCiv, False, False)
        teamCiv.setHasTech(xml.iAristocracy, True, iCiv, False, False)
        teamCiv.setHasTech(xml.iPlateArmor, True, iCiv, False, False)
        teamCiv.setHasTech(xml.iGothicArchitecture, True, iCiv, False, False)
        teamCiv.setHasTech(xml.iSiegeEngines, True, iCiv, False, False)
        if iCiv in [Civ.ARABIA.value, Civ.MOROCCO.value]:
            teamCiv.setHasTech(xml.iArabicKnowledge, True, iCiv, False, False)

    def assignTechs(self, iCiv):
        # 3Miro: other than the original techs

        if CIV_BIRTHDATE[get_civ_by_id(iCiv)] == 0:
            return

        if iCiv == Civ.ARABIA.value:
            teamArabia.setHasTech(xml.iTheology, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iCalendar, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iStirrup, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iBronzeCasting, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iArchitecture, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iArt, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iAstrolabe, True, iCiv, False, False)
            teamArabia.setHasTech(xml.iArabicKnowledge, True, iCiv, False, False)

        elif iCiv == Civ.BULGARIA.value:
            teamBulgaria.setHasTech(xml.iTheology, True, iCiv, False, False)
            teamBulgaria.setHasTech(xml.iCalendar, True, iCiv, False, False)
            teamBulgaria.setHasTech(xml.iStirrup, True, iCiv, False, False)
            teamBulgaria.setHasTech(xml.iArchitecture, True, iCiv, False, False)
            teamBulgaria.setHasTech(xml.iBronzeCasting, True, iCiv, False, False)

        elif iCiv == Civ.CORDOBA.value:
            teamCordoba.setHasTech(xml.iTheology, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iCalendar, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iStirrup, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iBronzeCasting, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iArchitecture, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iArt, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iAstrolabe, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iArabicKnowledge, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iEngineering, True, iCiv, False, False)
            teamCordoba.setHasTech(xml.iArabicMedicine, True, iCiv, False, False)

        elif iCiv == Civ.VENECIA.value:
            for iTech in range(xml.iStirrup + 1):
                teamVenecia.setHasTech(iTech, True, iCiv, False, False)
            teamVenecia.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamVenecia.setHasTech(xml.iAstrolabe, True, iCiv, False, False)
            teamVenecia.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamVenecia.setHasTech(xml.iArt, True, iCiv, False, False)
            teamVenecia.setHasTech(xml.iMusic, True, iCiv, False, False)
            teamVenecia.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)
            teamVenecia.setHasTech(xml.iChainMail, True, iCiv, False, False)

        elif iCiv == Civ.BURGUNDY.value:
            for iTech in range(xml.iStirrup + 1):
                teamBurgundy.setHasTech(iTech, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iFeudalism, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iFarriers, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iArt, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iEngineering, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iChainMail, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iAristocracy, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamBurgundy.setHasTech(xml.iAstrolabe, True, iCiv, False, False)

        elif iCiv == Civ.GERMANY.value:
            for iTech in range(xml.iStirrup + 1):
                teamGermany.setHasTech(iTech, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iFeudalism, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iFarriers, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iArt, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iEngineering, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iChainMail, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iAristocracy, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamGermany.setHasTech(xml.iAstrolabe, True, iCiv, False, False)

        elif iCiv == Civ.NOVGOROD.value:
            for iTech in range(xml.iStirrup + 1):
                teamNovgorod.setHasTech(iTech, True, iCiv, False, False)
            teamNovgorod.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamNovgorod.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamNovgorod.setHasTech(xml.iFarriers, True, iCiv, False, False)
            teamNovgorod.setHasTech(xml.iChainMail, True, iCiv, False, False)

        elif iCiv == Civ.NORWAY.value:
            for iTech in range(xml.iStirrup + 1):
                teamNorway.setHasTech(iTech, True, iCiv, False, False)
            teamNorway.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamNorway.setHasTech(xml.iAstrolabe, True, iCiv, False, False)
            teamNorway.setHasTech(xml.iFarriers, True, iCiv, False, False)
            teamNorway.setHasTech(xml.iChainMail, True, iCiv, False, False)
            teamNorway.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)

        elif iCiv == Civ.KIEV.value:
            for iTech in range(xml.iStirrup + 1):
                teamKiev.setHasTech(iTech, True, iCiv, False, False)
            teamKiev.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamKiev.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamKiev.setHasTech(xml.iFarriers, True, iCiv, False, False)
            teamKiev.setHasTech(xml.iChainMail, True, iCiv, False, False)

        elif iCiv == Civ.HUNGARY.value:
            for iTech in range(xml.iStirrup + 1):
                teamHungary.setHasTech(iTech, True, iCiv, False, False)
            teamHungary.setHasTech(xml.iChainMail, True, iCiv, False, False)
            teamHungary.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)
            teamHungary.setHasTech(xml.iVassalage, True, iCiv, False, False)

        elif iCiv == Civ.CASTILLE.value:
            for iTech in range(xml.iStirrup + 1):
                teamSpain.setHasTech(iTech, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iAstrolabe, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iArt, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iEngineering, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iMachinery, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iFeudalism, True, iCiv, False, False)
            teamSpain.setHasTech(xml.iChainMail, True, iCiv, False, False)

        elif iCiv == Civ.DENMARK.value:
            for iTech in range(xml.iStirrup + 1):
                teamDenmark.setHasTech(iTech, True, iCiv, False, False)
            teamDenmark.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamDenmark.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamDenmark.setHasTech(xml.iFeudalism, True, iCiv, False, False)
            teamDenmark.setHasTech(xml.iAristocracy, True, iCiv, False, False)
            teamDenmark.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamDenmark.setHasTech(xml.iAstrolabe, True, iCiv, False, False)
            teamDenmark.setHasTech(xml.iFarriers, True, iCiv, False, False)
            teamDenmark.setHasTech(xml.iChainMail, True, iCiv, False, False)
            teamDenmark.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)

        elif iCiv == Civ.SCOTLAND.value:
            for iTech in range(xml.iStirrup + 1):
                teamScotland.setHasTech(iTech, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iAstrolabe, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iArt, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iMusic, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iEngineering, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iMachinery, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iFeudalism, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iChainMail, True, iCiv, False, False)
            teamScotland.setHasTech(xml.iAristocracy, True, iCiv, False, False)

        elif iCiv == Civ.POLAND.value:
            for iTech in range(xml.iStirrup + 1):
                teamPoland.setHasTech(iTech, True, iCiv, False, False)
            teamPoland.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamPoland.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)
            teamPoland.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamPoland.setHasTech(xml.iFeudalism, True, iCiv, False, False)
            teamPoland.setHasTech(xml.iFarriers, True, iCiv, False, False)
            teamPoland.setHasTech(xml.iArt, True, iCiv, False, False)
            teamPoland.setHasTech(xml.iEngineering, True, iCiv, False, False)
            teamPoland.setHasTech(xml.iChainMail, True, iCiv, False, False)

        elif iCiv == Civ.GENOA.value:
            for iTech in range(xml.iStirrup + 1):
                teamGenoa.setHasTech(iTech, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iAstrolabe, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iMonasticism, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iArt, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iMusic, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iHerbalMedicine, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iVassalage, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iEngineering, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iMachinery, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iFeudalism, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iVaultedArches, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iChainMail, True, iCiv, False, False)
            teamGenoa.setHasTech(xml.iAristocracy, True, iCiv, False, False)

        elif iCiv == Civ.MOROCCO.value:
            for iTech in range(xml.iFarriers + 1):
                teamMorocco.setHasTech(iTech, True, iCiv, False, False)
            teamMorocco.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
            teamMorocco.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamMorocco.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamMorocco.setHasTech(xml.iMapMaking, True, iCiv, False, False)
            teamMorocco.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamMorocco.setHasTech(xml.iArabicKnowledge, True, iCiv, False, False)

        elif iCiv == Civ.ENGLAND.value:
            for iTech in range(xml.iFarriers + 1):
                teamEngland.setHasTech(iTech, True, iCiv, False, False)
            teamEngland.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
            teamEngland.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamEngland.setHasTech(xml.iAristocracy, True, iCiv, False, False)

        elif iCiv == Civ.PORTUGAL.value:
            for iTech in range(xml.iFarriers + 1):
                teamPortugal.setHasTech(iTech, True, iCiv, False, False)
            teamPortugal.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
            teamPortugal.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamPortugal.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamPortugal.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamPortugal.setHasTech(xml.iMapMaking, True, iCiv, False, False)
            teamPortugal.setHasTech(xml.iAristocracy, True, iCiv, False, False)

        elif iCiv == Civ.ARAGON.value:
            for iTech in range(xml.iFarriers + 1):
                teamAragon.setHasTech(iTech, True, iCiv, False, False)
            teamAragon.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
            teamAragon.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamAragon.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamAragon.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamAragon.setHasTech(xml.iMapMaking, True, iCiv, False, False)
            teamAragon.setHasTech(xml.iAristocracy, True, iCiv, False, False)
            teamAragon.setHasTech(xml.iPlateArmor, True, iCiv, False, False)
            teamAragon.setHasTech(xml.iGothicArchitecture, True, iCiv, False, False)
            teamAragon.setHasTech(xml.iSiegeEngines, True, iCiv, False, False)

        elif iCiv == Civ.SWEDEN.value:
            for iTech in range(xml.iFarriers + 1):
                teamSweden.setHasTech(iTech, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iGothicArchitecture, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iChivalry, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iAristocracy, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iPlateArmor, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iSiegeEngines, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iClassicalKnowledge, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iMonumentBuilding, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iPhilosophy, True, iCiv, False, False)
            teamSweden.setHasTech(xml.iMapMaking, True, iCiv, False, False)

        elif iCiv == Civ.PRUSSIA.value:
            for iTech in range(xml.iFarriers + 1):
                teamPrussia.setHasTech(iTech, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iGothicArchitecture, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iChivalry, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iAristocracy, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iPlateArmor, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iSiegeEngines, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iAlchemy, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iCivilService, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iGuilds, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iClassicalKnowledge, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iMonumentBuilding, True, iCiv, False, False)
            teamPrussia.setHasTech(xml.iPhilosophy, True, iCiv, False, False)

        elif iCiv == Civ.LITHUANIA.value:
            for iTech in range(xml.iFarriers + 1):
                teamLithuania.setHasTech(iTech, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iGothicArchitecture, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iAristocracy, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iCivilService, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iSiegeEngines, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iAlchemy, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iClassicalKnowledge, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iPlateArmor, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iMonumentBuilding, True, iCiv, False, False)
            teamLithuania.setHasTech(xml.iCivilService, True, iCiv, False, False)

        elif iCiv == Civ.AUSTRIA.value:
            for iTech in range(xml.iFarriers + 1):
                teamAustria.setHasTech(iTech, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iGothicArchitecture, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iChivalry, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iAristocracy, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iPlateArmor, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iSiegeEngines, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iAlchemy, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iCivilService, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iGuilds, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iClassicalKnowledge, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iMonumentBuilding, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iPhilosophy, True, iCiv, False, False)
            teamAustria.setHasTech(xml.iEducation, True, iCiv, False, False)

        elif iCiv == Civ.OTTOMAN.value:
            for iTech in range(xml.iChivalry + 1):
                teamTurkey.setHasTech(iTech, True, iCiv, False, False)
            teamTurkey.setHasTech(xml.iGunpowder, True, iCiv, False, False)
            teamTurkey.setHasTech(xml.iMilitaryTradition, True, iCiv, False, False)
            teamTurkey.setHasTech(xml.iArabicKnowledge, True, iCiv, False, False)

        elif iCiv == Civ.MOSCOW.value:
            for iTech in range(xml.iFarriers + 1):
                teamMoscow.setHasTech(iTech, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iBlastFurnace, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iCodeOfLaws, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iGothicArchitecture, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iChivalry, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iAristocracy, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iCivilService, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iLiterature, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iMonumentBuilding, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iPlateArmor, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iSiegeEngines, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iLateenSails, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iMapMaking, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iClassicalKnowledge, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iClockmaking, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iAlchemy, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iGuilds, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iPhilosophy, True, iCiv, False, False)
            teamMoscow.setHasTech(xml.iReplaceableParts, True, iCiv, False, False)

        elif iCiv == Civ.DUTCH.value:
            for iTech in range(xml.iAstronomy + 1):
                teamDutch.setHasTech(iTech, True, iCiv, False, False)

        self.hitNeighboursStability(iCiv)

    def hitNeighboursStability(self, iCiv):
        # 3Miro: Stability on Spawn
        neighbours = CIV_OLDER_NEIGHBOURS[get_civ_by_id(iCiv)]
        if neighbours is not None:
            bHuman = False
            # for iLoop in Consts.lOlderNeighbours[iCiv]:
            # if (gc.getPlayer(iLoop).isAlive()):
            # if (iLoop == utils.getHumanID()):
            # bHuman = True
            # utils.setStabilityParameters(iLoop, Consts.iParDiplomacyE, utils.getStabilityParameters(iLoop, Consts.iParDiplomacyE)-5)
            # utils.setStability(iLoop, utils.getStability(iLoop)-5)

    def showRect(self, iCiv, tArea):
        iXs, iYs, iXe, iYe = tArea
        for (iX, iY) in utils.getPlotList((iXs, iYs), (iXe, iYe)):
            gc.getMap().plot(iX, iY).setRevealed(gc.getPlayer(iCiv).getTeam(), True, False, -1)

    def showArea(self, iCiv, iScenario=Scenario.i500AD):
        for iI in range(len(Consts.tVisible[iScenario][iCiv])):
            self.showRect(iCiv, Consts.tVisible[iScenario][iCiv][iI])
        # pass

    def initContact(self, iCiv, bMeet=True):
        _civ = team(iCiv)
        contacts = CIVILIZATIONS[iCiv].initial.contact
        if contacts:
            for contact in contacts:
                other = civ(contact)
                if other.player.isAlive() and not _civ.isHasMet(other.team_id):
                    _civ.meet(other.team_id, bMeet)
        # pCiv = gc.getPlayer(iCiv)
        # teamCiv = gc.getTeam(pCiv.getTeam())
        # for contact in CIV_INITIAL_CONTACTS[utils.getScenario()][get_civ_by_id(iCiv)]:
        #     if contact:
        #         pOtherPlayer = gc.getPlayer(contact.value)
        #         tOtherPlayer = pOtherPlayer.getTeam()
        #         if pOtherPlayer.isAlive() and not teamCiv.isHasMet(tOtherPlayer):
        #             teamCiv.meet(tOtherPlayer, bMeet)

    def LeaningTowerGP(self):
        iGP = gc.getGame().getSorenRandNum(7, "starting count")
        pFlorentia = gc.getMap().plot(54, 32).getPlotCity()
        iSpecialist = Specialist.GREAT_PROPHET.value + iGP
        pFlorentia.setFreeSpecialistCount(iSpecialist, 1)

    def setDiplo1200AD(self):
        self.changeAttitudeExtra(Civ.BYZANTIUM.value, Civ.ARABIA.value, -2)
        self.changeAttitudeExtra(Civ.SCOTLAND.value, Civ.FRANCE.value, 4)

    def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):
        gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
        gc.getPlayer(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)
