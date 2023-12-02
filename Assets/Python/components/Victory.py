from CvPythonExtensions import *
from CoreData import civilization, civilizations, COMPANIES
from CoreStructures import human, player, team, turn
from CoreTypes import (
    Building,
    City,
    Civ,
    Civic,
    Colony,
    Company,
    Project,
    ProvinceStatus,
    Region,
    Specialist,
    StabilityCategory,
    Religion,
    Improvement,
    Technology,
    Unit,
    Bonus,
    Wonder,
    Province,
)
from LocationsData import CITIES, CIV_CAPITAL_LOCATIONS, REGIONS
import PyHelpers
import Popup
from PyUtils import rand
import RFCUtils
import UniquePowers
from ProvinceMapData import PROVINCES_MAP
from StoredData import data
import random

from TimelineData import DateTurn
from MiscData import MessageData

utils = RFCUtils.RFCUtils()
up = UniquePowers.UniquePowers()
gc = CyGlobalContext()
localText = CyTranslator()  # Absinthe


tByzantiumControl = [
    Province.CALABRIA.value,
    Province.APULIA.value,
    Province.DALMATIA.value,
    Province.VERONA.value,
    Province.LOMBARDY.value,
    Province.LIGURIA.value,
    Province.TUSCANY.value,
    Province.LATIUM.value,
    Province.CORSICA.value,
    Province.SARDINIA.value,
    Province.SICILY.value,
    Province.TRIPOLITANIA.value,
    Province.IFRIQIYA.value,
]
tByzantiumControlII = [
    Province.COLONEA.value,
    Province.ANTIOCHIA.value,
    Province.CHARSIANON.value,
    Province.CILICIA.value,
    Province.ARMENIAKON.value,
    Province.ANATOLIKON.value,
    Province.PAPHLAGONIA.value,
    Province.THRAKESION.value,
    Province.OPSIKION.value,
    Province.CONSTANTINOPLE.value,
    Province.THRACE.value,
    Province.THESSALONIKI.value,
    Province.MOESIA.value,
    Province.MACEDONIA.value,
    Province.SERBIA.value,
    Province.ARBERIA.value,
    Province.EPIRUS.value,
    Province.THESSALY.value,
    Province.MOREA.value,
]
tFrankControl = [
    Province.SWABIA.value,
    Province.SAXONY.value,
    Province.LORRAINE.value,
    Province.ILE_DE_FRANCE.value,
    Province.NORMANDY.value,
    Province.PICARDY.value,
    Province.AQUITAINE.value,
    Province.PROVENCE.value,
    Province.BURGUNDY.value,
    Province.ORLEANS.value,
    Province.CHAMPAGNE.value,
    Province.CATALONIA.value,
    Province.LOMBARDY.value,
    Province.TUSCANY.value,
]
tArabiaControlI = [
    Province.ARABIA.value,
    Province.JERUSALEM.value,
    Province.SYRIA.value,
    Province.LEBANON.value,
    Province.ANTIOCHIA.value,
    Province.EGYPT.value,
    Province.CYRENAICA.value,
    Province.TRIPOLITANIA.value,
    Province.IFRIQIYA.value,
    Province.SICILY.value,
    Province.CRETE.value,
    Province.CYPRUS.value,
]
tArabiaControlII = [
    Province.ARABIA.value,
    Province.JERUSALEM.value,
    Province.SYRIA.value,
    Province.LEBANON.value,
    Province.ANTIOCHIA.value,
    Province.EGYPT.value,
]
tBulgariaControl = [
    Province.CONSTANTINOPLE.value,
    Province.THESSALONIKI.value,
    Province.SERBIA.value,
    Province.THRACE.value,
    Province.MACEDONIA.value,
    Province.MOESIA.value,
    Province.ARBERIA.value,
]
tCordobaWonders = [
    Wonder.ALHAMBRA.value,
    Wonder.LA_MEZQUITA.value,
    Wonder.GARDENS_AL_ANDALUS.value,
]
tCordobaIslamize = [
    Province.GALICIA.value,
    Province.CASTILE.value,
    Province.LEON.value,
    Province.LUSITANIA.value,
    Province.CATALONIA.value,
    Province.ARAGON.value,
    Province.NAVARRE.value,
    Province.VALENCIA.value,
    Province.LA_MANCHA.value,
    Province.ANDALUSIA.value,
]
tNorwayControl = [
    Province.THE_ISLES.value,
    Province.IRELAND.value,
    Province.SCOTLAND.value,
    Province.NORMANDY.value,
    Province.SICILY.value,
    Province.APULIA.value,
    Province.CALABRIA.value,
    Province.ICELAND.value,
]
tNorwayOutrank = [
    Civ.SWEDEN.value,
    Civ.DENMARK.value,
    Civ.SCOTLAND.value,
    Civ.ENGLAND.value,
    Civ.GERMANY.value,
    Civ.FRANCE.value,
]
# tNorseControl = [ Province.SICILY.value, Province.ICELAND.value, Province.NORTHUMBRIA.value, Province.SCOTLAND.value, Province.NORMANDY.value, Province.IRELAND.value, Province.NOVGOROD.value ]
tVenetianControl = [
    Province.EPIRUS.value,
    Province.DALMATIA.value,
    Province.VERONA.value,
    Province.ARBERIA.value,
]
tVenetianControlII = [
    Province.THESSALY.value,
    Province.MOREA.value,
    Province.CRETE.value,
    Province.CYPRUS.value,
]
tBurgundyControl = [
    Province.FLANDERS.value,
    Province.PICARDY.value,
    Province.PROVENCE.value,
    Province.BURGUNDY.value,
    Province.CHAMPAGNE.value,
    Province.LORRAINE.value,
]
tBurgundyOutrank = [Civ.FRANCE.value, Civ.ENGLAND.value, Civ.GERMANY.value]
tGermanyControl = [
    Province.TUSCANY.value,
    Province.LIGURIA.value,
    Province.LOMBARDY.value,
    Province.LORRAINE.value,
    Province.SWABIA.value,
    Province.SAXONY.value,
    Province.BAVARIA.value,
    Province.FRANCONIA.value,
    Province.BRANDENBURG.value,
    Province.HOLSTEIN.value,
]
tGermanyControlII = [
    Province.AUSTRIA.value,
    Province.FLANDERS.value,
    Province.POMERANIA.value,
    Province.SILESIA.value,
    Province.BOHEMIA.value,
    Province.MORAVIA.value,
    Province.SWABIA.value,
    Province.SAXONY.value,
    Province.BAVARIA.value,
    Province.FRANCONIA.value,
    Province.BRANDENBURG.value,
    Province.HOLSTEIN.value,
]
tKievControl = [
    Province.KIEV.value,
    Province.PODOLIA.value,
    Province.PEREYASLAVL.value,
    Province.SLOBODA.value,
    Province.CHERNIGOV.value,
    Province.VOLHYNIA.value,
    Province.MINSK.value,
    Province.POLOTSK.value,
    Province.SMOLENSK.value,
    Province.MOSCOW.value,
    Province.MUROM.value,
    Province.ROSTOV.value,
    Province.NOVGOROD.value,
    Province.VOLOGDA.value,
]
tHungaryControl = [
    Province.AUSTRIA.value,
    Province.CARINTHIA.value,
    Province.MORAVIA.value,
    Province.SILESIA.value,
    Province.BOHEMIA.value,
    Province.DALMATIA.value,
    Province.BOSNIA.value,
    Province.BANAT.value,
    Province.WALLACHIA.value,
    Province.MOLDOVA.value,
]
tHungaryControlII = [
    Province.THRACE.value,
    Province.MOESIA.value,
    Province.MACEDONIA.value,
    Province.THESSALONIKI.value,
    Province.WALLACHIA.value,
    Province.THESSALY.value,
    Province.MOREA.value,
    Province.EPIRUS.value,
    Province.ARBERIA.value,
    Province.SERBIA.value,
    Province.BANAT.value,
    Province.BOSNIA.value,
    Province.DALMATIA.value,
    Province.SLAVONIA.value,
]
tSpainConvert = [
    Province.GALICIA.value,
    Province.CASTILE.value,
    Province.LEON.value,
    Province.LUSITANIA.value,
    Province.CATALONIA.value,
    Province.ARAGON.value,
    Province.NAVARRE.value,
    Province.VALENCIA.value,
    Province.LA_MANCHA.value,
    Province.ANDALUSIA.value,
]
tPolishControl = [
    Province.BOHEMIA.value,
    Province.MORAVIA.value,
    Province.UPPER_HUNGARY.value,
    Province.PRUSSIA.value,
    Province.LITHUANIA.value,
    Province.LIVONIA.value,
    Province.POLOTSK.value,
    Province.MINSK.value,
    Province.VOLHYNIA.value,
    Province.PODOLIA.value,
    Province.MOLDOVA.value,
    Province.KIEV.value,
]
tGenoaControl = [
    Province.CORSICA.value,
    Province.SARDINIA.value,
    Province.CRETE.value,
    Province.RHODES.value,
    Province.THRAKESION.value,
    Province.CYPRUS.value,
    Province.CRIMEA.value,
]
tEnglandControl = [
    Province.AQUITAINE.value,
    Province.LONDON.value,
    Province.WALES.value,
    Province.WESSEX.value,
    Province.SCOTLAND.value,
    Province.EAST_ANGLIA.value,
    Province.MERCIA.value,
    Province.NORTHUMBRIA.value,
    Province.IRELAND.value,
    Province.NORMANDY.value,
    Province.BRETAGNE.value,
    Province.ILE_DE_FRANCE.value,
    Province.ORLEANS.value,
    Province.PICARDY.value,
]
tPortugalControlI = [Province.AZORES.value, Province.CANARIES.value, Province.MADEIRA.value]
tPortugalControlII = [Province.MOROCCO.value, Province.TETOUAN.value, Province.ORAN.value]
tAustriaControl = [
    Province.HUNGARY.value,
    Province.UPPER_HUNGARY.value,
    Province.AUSTRIA.value,
    Province.CARINTHIA.value,
    Province.BAVARIA.value,
    Province.TRANSYLVANIA.value,
    Province.PANNONIA.value,
    Province.MORAVIA.value,
    Province.SILESIA.value,
    Province.BOHEMIA.value,
]
tOttomanControlI = [
    Province.SERBIA.value,
    Province.BOSNIA.value,
    Province.BANAT.value,
    Province.MACEDONIA.value,
    Province.THRACE.value,
    Province.MOESIA.value,
    Province.CONSTANTINOPLE.value,
    Province.ARBERIA.value,
    Province.EPIRUS.value,
    Province.THESSALONIKI.value,
    Province.THESSALY.value,
    Province.MOREA.value,
    Province.COLONEA.value,
    Province.ANTIOCHIA.value,
    Province.CHARSIANON.value,
    Province.CILICIA.value,
    Province.ARMENIAKON.value,
    Province.ANATOLIKON.value,
    Province.PAPHLAGONIA.value,
    Province.THRAKESION.value,
    Province.OPSIKION.value,
    Province.SYRIA.value,
    Province.LEBANON.value,
    Province.JERUSALEM.value,
    Province.EGYPT.value,
]
tOttomanWonders = [
    Wonder.TOPKAPI_PALACE.value,
    Wonder.BLUE_MOSQUE.value,
    Wonder.SELIMIYE_MOSQUE.value,
    Wonder.TOMB_AL_WALID.value,
]
tOttomanControlII = [Province.AUSTRIA.value, Province.PANNONIA.value, Province.LESSER_POLAND.value]
tMoscowControl = [
    Province.DONETS.value,
    Province.KUBAN.value,
    Province.ZAPORIZHIA.value,
    Province.SLOBODA.value,
    Province.KIEV.value,
    Province.MOLDOVA.value,
    Province.CRIMEA.value,
    Province.PEREYASLAVL.value,
    Province.CHERNIGOV.value,
    Province.SIMBIRSK.value,
    Province.NIZHNYNOVGOROD.value,
    Province.VOLOGDA.value,
    Province.ROSTOV.value,
    Province.NOVGOROD.value,
    Province.KARELIA.value,
    Province.SMOLENSK.value,
    Province.POLOTSK.value,
    Province.MINSK.value,
    Province.VOLHYNIA.value,
    Province.PODOLIA.value,
    Province.MOSCOW.value,
    Province.MUROM.value,
]
# tSwedenControlI = [ Province.GOTALAND.value, Province.SVEALAND.value, Province.NORRLAND.value, Province.SKANELAND.value, Province.GOTLAND.value, Province.OSTERLAND.value ]
# tSwedenControlII = [ Province.SAXONY.value, Province.BRANDENBURG.value, Province.HOLSTEIN.value, Province.POMERANIA.value, Province.PRUSSIA.value, Province.GREATER_POLAND.value, Province.MASOVIA.value, Province.SUVALKIJA.value, Province.LITHUANIA.value, Province.LIVONIA.value, Province.ESTONIA.value, Province.SMOLENSK.value, Province.POLOTSK.value, Province.MINSK.value, Province.MUROM.value, Province.CHERNIGOV.value, Province.MOSCOW.value, Province.NOVGOROD.value, Province.ROSTOV.value ]
tSwedenControl = [Province.NORRLAND.value, Province.OSTERLAND.value, Province.KARELIA.value]
tNovgorodControl = [
    Province.NOVGOROD.value,
    Province.KARELIA.value,
    Province.ESTONIA.value,
    Province.LIVONIA.value,
    Province.ROSTOV.value,
    Province.VOLOGDA.value,
    Province.OSTERLAND.value,
]
# tNovgorodControlII = [ Province.KARELIA.value, Province.VOLOGDA.value ]
tMoroccoControl = [
    Province.MOROCCO.value,
    Province.MARRAKESH.value,
    Province.FEZ.value,
    Province.TETOUAN.value,
    Province.ORAN.value,
    Province.ALGIERS.value,
    Province.IFRIQIYA.value,
    Province.ANDALUSIA.value,
    Province.VALENCIA.value,
    Province.BALEARS.value,
]
tAragonControlI = [
    Province.CATALONIA.value,
    Province.VALENCIA.value,
    Province.BALEARS.value,
    Province.SICILY.value,
]
tAragonControlII = [
    Province.CATALONIA.value,
    Province.VALENCIA.value,
    Province.ARAGON.value,
    Province.BALEARS.value,
    Province.CORSICA.value,
    Province.SARDINIA.value,
    Province.SICILY.value,
    Province.CALABRIA.value,
    Province.APULIA.value,
    Province.PROVENCE.value,
    Province.THESSALY.value,
]
tPrussiaControlI = [
    Province.LITHUANIA.value,
    Province.SUVALKIJA.value,
    Province.LIVONIA.value,
    Province.ESTONIA.value,
    Province.POMERANIA.value,
    Province.PRUSSIA.value,
]
tPrussiaDefeat = [
    Civ.AUSTRIA.value,
    Civ.MOSCOW.value,
    Civ.GERMANY.value,
    Civ.SWEDEN.value,
    Civ.FRANCE.value,
    Civ.CASTILE.value,
]
tScotlandControl = [
    Province.SCOTLAND.value,
    Province.THE_ISLES.value,
    Province.IRELAND.value,
    Province.WALES.value,
    Province.BRETAGNE.value,
]
tDenmarkControlI = [
    Province.DENMARK.value,
    Province.SKANELAND.value,
    Province.GOTALAND.value,
    Province.SVEALAND.value,
    Province.MERCIA.value,
    Province.LONDON.value,
    Province.EAST_ANGLIA.value,
    Province.NORTHUMBRIA.value,
]
# tDenmarkControlII = [ Province.BRANDENBURG.value, Province.POMERANIA.value, Province.ESTONIA.value ]
tDenmarkControlIII = [
    Province.DENMARK.value,
    Province.NORWAY.value,
    Province.VESTFOLD.value,
    Province.SKANELAND.value,
    Province.GOTALAND.value,
    Province.SVEALAND.value,
    Province.NORRLAND.value,
    Province.GOTLAND.value,
    Province.OSTERLAND.value,
    Province.ESTONIA.value,
    Province.ICELAND.value,
]

# tHugeHungaryControl = ( 0, 23, 99, 72 )
totalLand = gc.getMap().getLandPlots()


class Victory:
    def __init__(self):
        self.switchConditionsPerCiv = {
            Civ.BYZANTIUM.value: self.checkByzantium,
            Civ.FRANCE.value: self.checkFrankia,
            Civ.ARABIA.value: self.checkArabia,
            Civ.BULGARIA.value: self.checkBulgaria,
            Civ.CORDOBA.value: self.checkCordoba,
            Civ.VENECIA.value: self.checkVenecia,
            Civ.BURGUNDY.value: self.checkBurgundy,
            Civ.GERMANY.value: self.checkGermany,
            Civ.NOVGOROD.value: self.checkNovgorod,
            Civ.NORWAY.value: self.checkNorway,
            Civ.KIEV.value: self.checkKiev,
            Civ.HUNGARY.value: self.checkHungary,
            Civ.CASTILE.value: self.checkSpain,
            Civ.DENMARK.value: self.checkDenmark,
            Civ.SCOTLAND.value: self.checkScotland,
            Civ.POLAND.value: self.checkPoland,
            Civ.GENOA.value: self.checkGenoa,
            Civ.MOROCCO.value: self.checkMorocco,
            Civ.ENGLAND.value: self.checkEngland,
            Civ.PORTUGAL.value: self.checkPortugal,
            Civ.ARAGON.value: self.checkAragon,
            Civ.SWEDEN.value: self.checkSweden,
            Civ.PRUSSIA.value: self.checkPrussia,
            Civ.LITHUANIA.value: self.checkLithuania,
            Civ.AUSTRIA.value: self.checkAustria,
            Civ.OTTOMAN.value: self.checkTurkey,
            Civ.MOSCOW.value: self.checkMoscow,
            Civ.DUTCH.value: self.checkDutch,
        }

    ##################################################
    ### Secure storage & retrieval of script data ###
    ################################################

    def setup(self):
        # ignore AI goals
        bIgnoreAI = gc.getDefineINT("NO_AI_UHV_CHECKS") == 1
        self.setIgnoreAI(bIgnoreAI)
        if bIgnoreAI:
            for iPlayer in civilizations().majors().ids():
                if human() != iPlayer:
                    self.setAllUHVFailed(iPlayer)

    def isIgnoreAI(self):
        return data.bIgnoreAIUHV

    def setIgnoreAI(self, bVal):
        data.bIgnoreAIUHV = bVal

    #######################################
    ### Main methods (Event-Triggered) ###
    #####################################

    def checkTurn(self, iGameTurn):
        pass

    def checkPlayerTurn(self, iGameTurn, iPlayer):
        # We use Python version of Switch statement, it is supposed to be better, now all condition checks are in separate functions
        pPlayer = gc.getPlayer(iPlayer)
        if iPlayer != human() and self.isIgnoreAI():
            return
        if not gc.getGame().isVictoryValid(7):  # 7 == historical
            return
        if not pPlayer.isAlive():
            return
        if iPlayer >= civilizations().main().len():
            return

        self.switchConditionsPerCiv[iPlayer](iGameTurn)

        # Generic checks:
        if not pPlayer.getUHV2of3():
            if (
                utils.countAchievedGoals(iPlayer) >= 2
            ):  # in case the last 2 goals were achieved in the same turn
                # intermediate bonus
                pPlayer.setUHV2of3(True)
                if pPlayer.getNumCities() > 0:  # this check is needed, otherwise game crashes
                    capital = pPlayer.getCapitalCity()
                    # 3Miro: Golden Age after 2/3 victories
                    capital.setHasRealBuilding(Building.TRIUMPHAL_ARCH.value, True)
                    if pPlayer.isHuman():
                        CyInterface().addMessage(
                            iPlayer,
                            False,
                            MessageData.DURATION,
                            CyTranslator().getText("TXT_KEY_VICTORY_INTERMEDIATE", ()),
                            "",
                            0,
                            "",
                            ColorTypes(MessageData.PURPLE),
                            -1,
                            -1,
                            True,
                            True,
                        )
                        for iCiv in civilizations().majors().ids():
                            if iCiv != iPlayer:
                                pCiv = gc.getPlayer(iCiv)
                                if pCiv.isAlive():
                                    iAttitude = pCiv.AI_getAttitude(iPlayer)
                                    if iAttitude != 0:
                                        pCiv.AI_setAttitudeExtra(iPlayer, iAttitude - 1)

                        # Absinthe: maximum 3 of your rivals declare war on you
                        lCivs = [
                            iCiv
                            for iCiv in civilizations().main().ids()
                            if iCiv != iPlayer and gc.getPlayer(iCiv).isAlive()
                        ]
                        iWarCounter = 0
                        # we run through a randomized list of all available civs
                        random.shuffle(lCivs)
                        for iCiv in lCivs:
                            pCiv = gc.getPlayer(iCiv)
                            teamCiv = gc.getTeam(pCiv.getTeam())
                            # skip civ if it's vassal (safety check for own vassals, want to look for the master for other vassals)
                            if teamCiv.isAVassal():
                                continue
                            if teamCiv.canDeclareWar(pPlayer.getTeam()):
                                if pCiv.canContact(iPlayer) and not teamCiv.isAtWar(iPlayer):
                                    iModifier = 0
                                    # bigger chance for civs which hate you
                                    if pCiv.AI_getAttitude(iPlayer) == 0:
                                        iModifier += 3
                                    elif pCiv.AI_getAttitude(iPlayer) == 1:
                                        iModifier += 1
                                    elif pCiv.AI_getAttitude(iPlayer) == 3:
                                        iModifier -= 1
                                    elif pCiv.AI_getAttitude(iPlayer) == 4:
                                        iModifier -= 3
                                    # bigger chance for close civs
                                    PlayerCapital = gc.getPlayer(iPlayer).getCapitalCity()
                                    CivCapital = gc.getPlayer(iCiv).getCapitalCity()
                                    iDistance = utils.calculateDistance(
                                        CivCapital.getX(),
                                        CivCapital.getY(),
                                        PlayerCapital.getX(),
                                        PlayerCapital.getY(),
                                    )
                                    if iDistance < 20:
                                        iModifier += 2
                                    elif iDistance < 40:
                                        iModifier += 1
                                    # bigger chance for big civs
                                    if pCiv.getNumCities() > 19:
                                        iModifier += 4
                                    elif pCiv.getNumCities() > 14:
                                        iModifier += 3
                                    elif pCiv.getNumCities() > 9:
                                        iModifier += 2
                                    elif pCiv.getNumCities() > 4:
                                        iModifier += 1
                                    iRndnum = rand(7)
                                    if iRndnum + iModifier > 6:
                                        teamCiv.declareWar(pPlayer.getTeam(), True, -1)
                                        iWarCounter += 1
                                        if iWarCounter == 3:
                                            break
                        if iWarCounter > 0:
                            CyInterface().addMessage(
                                iPlayer,
                                False,
                                MessageData.DURATION,
                                CyTranslator().getText("TXT_KEY_VICTORY_RIVAL_CIVS", ()),
                                "",
                                0,
                                "",
                                ColorTypes(MessageData.LIGHT_RED),
                                -1,
                                -1,
                                True,
                                True,
                            )

        if gc.getGame().getWinner() == -1:
            if pPlayer.getUHV(0) == 1 and pPlayer.getUHV(1) == 1 and pPlayer.getUHV(2) == 1:
                gc.getGame().setWinner(iPlayer, 7)  # Historical Victory

    def onCityBuilt(self, city, iPlayer):  # see onCityBuilt in CvRFCEventHandler
        # Portugal UHV 1: Settle 3 cities on the Azores, Canaries and Madeira and 2 in Morocco, Tetouan and Oran
        if iPlayer == Civ.PORTUGAL.value:
            if self.isPossibleUHV(iPlayer, 0, False):
                iProv = city.getProvince()
                if iProv in tPortugalControlI or iProv in tPortugalControlII:
                    iCounter = player(Civ.PORTUGAL).getUHVCounter(0)
                    iIslands = iCounter % 100
                    iAfrica = iCounter / 100
                    if iProv in tPortugalControlI:
                        iIslands += 1
                    else:
                        iAfrica += 1
                    if iIslands >= 3 and iAfrica >= 2:
                        self.wonUHV(Civ.PORTUGAL.value, 0)
                    player(Civ.PORTUGAL).setUHVCounter(0, iAfrica * 100 + iIslands)

    def onReligionFounded(self, iReligion, iFounder):
        # Germany UHV 2: Start the Reformation (Found Protestantism)
        if iReligion == Religion.PROTESTANTISM.value:
            if iFounder == Civ.GERMANY.value:
                self.wonUHV(Civ.GERMANY.value, 1)
            else:
                self.lostUHV(Civ.GERMANY.value, 1)

    def onCityAcquired(self, owner, iNewOwner, city, bConquest, bTrade):
        if not gc.getGame().isVictoryValid(7):  # Victory 7 == historical
            return

        iPlayer = owner
        iGameTurn = turn()

        # Bulgaria UHV 3: Do not lose a city to Barbarians, Mongols, Byzantines, or Ottomans before 1396
        if iPlayer == Civ.BULGARIA.value:
            if self.isPossibleUHV(iPlayer, 2, False):
                if iGameTurn <= DateTurn.i1396AD:
                    if iNewOwner in [Civ.BARBARIAN.value, Civ.BYZANTIUM.value, Civ.OTTOMAN.value]:
                        # conquered and flipped cities always count
                        # for traded cities, there should be a distinction between traded in peace (gift) and traded in ending a war (peace negotiations)
                        # instead of that, we check if the civ is at peace when the trade happens
                        # TODO#BUG# unfortunately the trade deal just ending a war is taken into account as a peace deal - maybe check if there was a war in this turn, or the last couple turns?
                        if not bTrade:
                            self.lostUHV(Civ.BULGARIA.value, 2)
                        else:
                            bIsAtWar = False
                            for civ in civilizations().take(Civ.BYZANTIUM, Civ.OTTOMAN).alive():
                                if civilization(Civ.BULGARIA).at_war(civ):
                                    bIsAtWar = True
                            if bIsAtWar:
                                self.lostUHV(Civ.BULGARIA.value, 2)

        # Portugal UHV 2: Do not lose a city before 1640
        elif iPlayer == Civ.PORTUGAL.value:
            if self.isPossibleUHV(iPlayer, 1, False):
                # conquered and flipped cities always count
                # for traded cities, there should be a distinction between traded in peace (gift) and traded in ending a war (peace negotiations)
                # instead of that, we check if the civ is at peace when the trade happens
                # TODO#BUG# unfortunately the trade deal just ending a war is taken into account as a peace deal - maybe check if there was a war in this turn, or the last couple turns?
                if not bTrade:
                    self.lostUHV(Civ.PORTUGAL.value, 1)
                else:
                    bIsAtWar = False
                    for civ in civilizations().majors().alive():
                        if civilization(Civ.BULGARIA).at_war(civ):
                            bIsAtWar = True
                            break
                    if bIsAtWar:
                        self.lostUHV(Civ.PORTUGAL.value, 1)

        # Norway UHV 1: Going Viking
        elif iNewOwner == Civ.NORWAY.value and iGameTurn < DateTurn.i1066AD + 2:
            # Absinthe: city is already reduced by 1 on city conquest, so city.getPopulation() is one less than the original size (unless it was already 1)
            if bConquest:
                if city.getPopulation() > 1:
                    player(Civ.NORWAY).setUHVCounter(
                        0,
                        player(Civ.NORWAY).getUHVCounter(0) + city.getPopulation() + 1,
                    )
                else:
                    player(Civ.NORWAY).setUHVCounter(
                        0,
                        player(Civ.NORWAY).getUHVCounter(0) + city.getPopulation(),
                    )

        # Poland UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
        elif iNewOwner == Civ.POLAND.value:
            if self.isPossibleUHV(iNewOwner, 2, False):
                if city.hasBuilding(
                    Wonder.KAZIMIERZ.value
                ):  # you cannot acquire religious buildings on conquest, only wonders
                    iCounter = player(Civ.POLAND).getUHVCounter(2)
                    iCathCath = (iCounter / 10000) % 10
                    iOrthCath = (iCounter / 1000) % 10
                    iProtCath = (iCounter / 100) % 10
                    iJewishQu = 99
                    iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
                    player(Civ.POLAND).setUHVCounter(2, iCounter)
                    if iCathCath >= 3 and iOrthCath >= 2 and iProtCath >= 2 and iJewishQu >= 2:
                        self.wonUHV(Civ.POLAND.value, 2)

        # Prussia UHV 2: Conquer two cities from each of Austria, Muscovy, Germany, Sweden, France and Spain between 1650 and 1763, if they are still alive
        elif iNewOwner == Civ.PRUSSIA.value:
            if self.isPossibleUHV(iNewOwner, 1, False):
                if owner in tPrussiaDefeat and DateTurn.i1650AD <= iGameTurn <= DateTurn.i1763AD:
                    lNumConq = []
                    iConqRaw = player(Civ.PRUSSIA).getUHVCounter(1)
                    bConq = True
                    for iI in range(len(tPrussiaDefeat)):
                        lNumConq.append((iConqRaw / pow(10, iI)) % 10)
                        if tPrussiaDefeat[iI] == owner:
                            lNumConq[iI] += 1
                            if lNumConq[iI] > 9:
                                # Prevent overflow
                                lNumConq[iI] = 9
                        if lNumConq[iI] < 2 and gc.getPlayer(tPrussiaDefeat[iI]).isAlive():
                            bConq = False

                    if bConq:
                        self.wonUHV(Civ.PRUSSIA.value, 1)

                    iConqRaw = 0
                    for iI in range(len(tPrussiaDefeat)):
                        iConqRaw += lNumConq[iI] * pow(10, iI)
                    player(Civ.PRUSSIA).setUHVCounter(1, iConqRaw)

    def onCityRazed(self, iPlayer, city):
        # Sweden UHV 2: Raze 5 Catholic cities while being Protestant by 1660
        if iPlayer == Civ.SWEDEN.value:
            if self.isPossibleUHV(iPlayer, 1, False):
                if civilization(Civ.SWEDEN).has_state_religion(
                    Religion.PROTESTANTISM
                ) and city.isHasReligion(Religion.CATHOLICISM.value):
                    iRazed = player(Civ.SWEDEN).getUHVCounter(1) + 1
                    player(Civ.SWEDEN).setUHVCounter(1, iRazed)
                    if iRazed >= 5:
                        self.wonUHV(Civ.SWEDEN.value, 1)

    def onPillageImprovement(self, iPillager, iVictim, iImprovement, iRoute, iX, iY):
        # Norway UHV 1: Going Viking
        if iPillager == Civ.NORWAY.value and iRoute == -1 and turn() < DateTurn.i1066AD + 2:
            if gc.getMap().plot(iX, iY).getOwner() != Civ.NORWAY.value:
                player(Civ.NORWAY).setUHVCounter(0, player(Civ.NORWAY).getUHVCounter(0) + 1)

    def onCombatResult(self, argsList):
        pWinningUnit, pLosingUnit = argsList
        cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())

        # Norway UHV 1: Going Viking
        if pWinningUnit.getOwner() == Civ.NORWAY.value and turn() < DateTurn.i1066AD + 2:
            if cLosingUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
                # Absinthe: only 1 Viking point for Work Boats
                if pLosingUnit.getUnitType() != Unit.WORKBOAT.value:
                    player(Civ.NORWAY).setUHVCounter(0, player(Civ.NORWAY).getUHVCounter(0) + 2)
                else:
                    player(Civ.NORWAY).setUHVCounter(0, player(Civ.NORWAY).getUHVCounter(0) + 1)

    def onTechAcquired(self, iTech, iPlayer):
        if not gc.getGame().isVictoryValid(7):  # 7 == historical
            return

        # England UHV 3: Be the first to enter the Industrial age
        if iTech == Technology.INDUSTRIAL_TECH.value:
            if self.isPossibleUHV(Civ.ENGLAND.value, 2, False):
                if iPlayer == Civ.ENGLAND.value:
                    self.wonUHV(Civ.ENGLAND.value, 2)
                else:
                    self.lostUHV(Civ.ENGLAND.value, 2)

    def onBuildingBuilt(self, iPlayer, iBuilding):
        if not gc.getGame().isVictoryValid(7):  # 7 == historical
            return

        iGameTurn = turn()

        # Kiev UHV 1: Build 2 Orthodox cathedrals and 8 Orthodox monasteries by 1250
        if iPlayer == Civ.KIEV.value:
            if self.isPossibleUHV(iPlayer, 0, False):
                if iBuilding in [
                    Building.ORTHODOX_MONASTERY.value,
                    Building.ORTHODOX_CATHEDRAL.value,
                ]:
                    iBuildSoFar = player(Civ.KIEV).getUHVCounter(0)
                    iCathedralCounter = iBuildSoFar % 100
                    iMonasteryCounter = iBuildSoFar / 100
                    if iBuilding == Building.ORTHODOX_MONASTERY.value:
                        iMonasteryCounter += 1
                    else:
                        iCathedralCounter += 1
                    if iCathedralCounter >= 2 and iMonasteryCounter >= 8:
                        self.wonUHV(Civ.KIEV.value, 0)
                    player(Civ.KIEV).setUHVCounter(0, 100 * iMonasteryCounter + iCathedralCounter)

        # Poland UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
        # HHG: Polish UHV3 now uses Wonder Kazimierz with maximum value 99, and all other buildings have boundary checks
        elif iPlayer == Civ.POLAND.value:
            if self.isPossibleUHV(iPlayer, 2, False):
                lBuildingList = [
                    Building.CATHOLIC_CATHEDRAL.value,
                    Building.ORTHODOX_CATHEDRAL.value,
                    Building.PROTESTANT_CATHEDRAL.value,
                    Building.JEWISH_QUARTER.value,
                    Wonder.KAZIMIERZ.value,
                ]
                if iBuilding in lBuildingList:
                    iCounter = player(Civ.POLAND).getUHVCounter(2)
                    iCathCath = (iCounter / 10000) % 10
                    iOrthCath = (iCounter / 1000) % 10
                    iProtCath = (iCounter / 100) % 10
                    iJewishQu = iCounter % 100
                    if iBuilding == Building.CATHOLIC_CATHEDRAL.value and iCathCath < 9:
                        iCathCath += 1
                    elif iBuilding == Building.ORTHODOX_CATHEDRAL.value and iOrthCath < 9:
                        iOrthCath += 1
                    elif iBuilding == Building.PROTESTANT_CATHEDRAL.value and iProtCath < 9:
                        iProtCath += 1
                    elif iBuilding == Wonder.KAZIMIERZ.value:
                        iJewishQu = 99
                    elif iBuilding == Building.JEWISH_QUARTER.value and iJewishQu < 99:
                        iJewishQu += 1
                    if iCathCath >= 3 and iOrthCath >= 3 and iProtCath >= 2 and iJewishQu >= 2:
                        self.wonUHV(Civ.POLAND.value, 2)
                    iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
                    player(Civ.POLAND).setUHVCounter(2, iCounter)

        # Cordoba UHV 2: Build the Alhambra, the Gardens of Al-Andalus, and La Mezquita by 1309
        if iBuilding in tCordobaWonders:
            if self.isPossibleUHV(Civ.CORDOBA.value, 1, False):
                if iPlayer == Civ.CORDOBA.value:
                    iWondersBuilt = player(Civ.CORDOBA).getUHVCounter(1)
                    player(Civ.CORDOBA).setUHVCounter(1, iWondersBuilt + 1)
                    if iWondersBuilt == 2:  # so we already had 2 wonders, and this is the 3rd one
                        self.wonUHV(Civ.CORDOBA.value, 1)
                else:
                    self.lostUHV(Civ.CORDOBA.value, 1)

        # Ottoman UHV 2: Construct the Topkapi Palace, the Blue Mosque, the Selimiye Mosque and the Tomb of Al-Walid by 1616
        if iBuilding in tOttomanWonders:
            if self.isPossibleUHV(Civ.OTTOMAN.value, 1, False):
                if iPlayer == Civ.OTTOMAN.value:
                    iWondersBuilt = player(Civ.OTTOMAN).getUHVCounter(1)
                    player(Civ.OTTOMAN).setUHVCounter(1, iWondersBuilt + 1)
                    if iWondersBuilt == 3:  # so we already had 3 wonders, and this is the 4th one
                        self.wonUHV(Civ.OTTOMAN.value, 1)
                else:
                    self.lostUHV(Civ.OTTOMAN.value, 1)

    def onProjectBuilt(self, iPlayer, iProject):
        bColony = self.isProjectAColony(iProject)
        # Absinthe: note that getProjectCount (thus getNumRealColonies too) won't count the latest project/colony (which was currently built) if called from this function
        # 			way more straightforward, and also faster to use the UHVCounters for the UHV checks

        # Venice UHV 3: Be the first to build a Colony from the Age of Discovery (Vinland is from the Viking Age)
        if self.isPossibleUHV(Civ.VENECIA.value, 2, False):
            if iProject != Colony.VINLAND.value:
                if bColony:
                    if iPlayer == Civ.VENECIA.value:
                        self.wonUHV(Civ.VENECIA.value, 2)
                    else:
                        self.lostUHV(Civ.VENECIA.value, 2)

        # France UHV 3: Build 5 Colonies
        if iPlayer == Civ.FRANCE.value:
            if self.isPossibleUHV(iPlayer, 2, False):
                if bColony:
                    player(Civ.FRANCE).setUHVCounter(2, player(Civ.FRANCE).getUHVCounter(2) + 1)
                    if player(Civ.FRANCE).getUHVCounter(2) >= 5:
                        self.wonUHV(Civ.FRANCE.value, 2)

        # England UHV 2: Build 7 Colonies
        elif iPlayer == Civ.ENGLAND.value:
            if self.isPossibleUHV(iPlayer, 1, False):
                if bColony:
                    player(Civ.ENGLAND).setUHVCounter(1, player(Civ.ENGLAND).getUHVCounter(1) + 1)
                    if player(Civ.ENGLAND).getUHVCounter(1) >= 7:
                        self.wonUHV(Civ.ENGLAND.value, 1)

        # Spain UHV 2: Have more Colonies than any other nation in 1588 (while having at least 3)
        # this is only for the Main Screen counter
        elif iPlayer == Civ.CASTILE.value:
            player(Civ.CASTILE).setUHVCounter(1, player(Civ.CASTILE).getUHVCounter(1) + 1)

        # Portugal UHV 3: Build 5 Colonies
        elif iPlayer == Civ.PORTUGAL.value:
            if self.isPossibleUHV(iPlayer, 2, False):
                if bColony:
                    player(Civ.PORTUGAL).setUHVCounter(
                        2, player(Civ.PORTUGAL).getUHVCounter(2) + 1
                    )
                    if player(Civ.PORTUGAL).getUHVCounter(2) >= 5:
                        self.wonUHV(Civ.PORTUGAL.value, 2)

        # Dutch UHV 2: Build 3 Colonies and complete both Trading Companies
        elif iPlayer == Civ.DUTCH.value:
            if self.isPossibleUHV(iPlayer, 1, False):
                if bColony:
                    player(Civ.DUTCH).setUHVCounter(1, player(Civ.DUTCH).getUHVCounter(1) + 1)
                if player(Civ.DUTCH).getUHVCounter(1) >= 3:
                    iWestCompany = team(Civ.DUTCH).getProjectCount(
                        Project.WEST_INDIA_COMPANY.value
                    )
                    iEastCompany = team(Civ.DUTCH).getProjectCount(
                        Project.EAST_INDIA_COMPANY.value
                    )
                    # if the companies are already built previously, or currently being built (one of them is the current project)
                    if iProject == Project.WEST_INDIA_COMPANY.value or iWestCompany >= 1:
                        if iProject == Project.EAST_INDIA_COMPANY.value or iEastCompany >= 1:
                            self.wonUHV(Civ.DUTCH.value, 1)

        # Denmark UHV 3: Build 3 Colonies and complete both Trading Companies
        elif iPlayer == Civ.DENMARK.value:
            if self.isPossibleUHV(iPlayer, 2, False):
                if bColony:
                    player(Civ.DENMARK).setUHVCounter(2, player(Civ.DENMARK).getUHVCounter(2) + 1)
                if player(Civ.DENMARK).getUHVCounter(2) >= 3:
                    iWestCompany = team(Civ.DENMARK).getProjectCount(
                        Project.WEST_INDIA_COMPANY.value
                    )
                    iEastCompany = team(Civ.DENMARK).getProjectCount(
                        Project.EAST_INDIA_COMPANY.value
                    )
                    # if the companies are already built previously, or currently being built (one of them is the current project)
                    if iProject == Project.WEST_INDIA_COMPANY.value or iWestCompany == 1:
                        if iProject == Project.EAST_INDIA_COMPANY.value or iEastCompany == 1:
                            self.wonUHV(Civ.DENMARK.value, 2)

    def getOwnedLuxes(self, pPlayer):
        lBonus = [
            Bonus.SHEEP.value,
            Bonus.DYE.value,
            Bonus.FUR.value,
            Bonus.GEMS.value,
            Bonus.GOLD.value,
            Bonus.INCENSE.value,
            Bonus.IVORY.value,
            Bonus.SILK.value,
            Bonus.SILVER.value,
            Bonus.SPICES.value,
            Bonus.WINE.value,
            Bonus.HONEY.value,
            Bonus.WHALE.value,
            Bonus.AMBER.value,
            Bonus.COTTON.value,
            Bonus.COFFEE.value,
            Bonus.TEA.value,
            Bonus.TOBACCO.value,
        ]
        iCount = 0
        for iBonus in lBonus:
            iCount += pPlayer.countOwnedBonuses(iBonus)
        return iCount

    def getOwnedGrain(self, pPlayer):
        iCount = 0
        iCount += pPlayer.countOwnedBonuses(Bonus.WHEAT.value)
        iCount += pPlayer.countOwnedBonuses(Bonus.BARLEY.value)
        return iCount

    def isProjectAColony(self, iProject):
        if iProject >= len(Project):
            return True
        else:
            return False

    def getNumRealColonies(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        tPlayer = gc.getTeam(pPlayer.getTeam())
        iCount = 0
        for col in Colony:
            if tPlayer.getProjectCount(col.value) > 0:
                iCount += 1
        return iCount

    def getTerritoryPercentEurope(self, iPlayer, bReturnTotal=False):
        iTotal = 0
        iCount = 0
        for (x, y) in utils.getWorldPlotsList():
            plot = gc.getMap().plot(x, y)
            if plot.isWater():
                continue
            iProvinceID = PROVINCES_MAP[y][x]
            if iProvinceID in REGIONS[Region.NOT_EUROPE]:
                continue
            iTotal += 1
            if plot.getOwner() == iPlayer:
                iCount += 1
        if bReturnTotal:
            return iCount, iTotal
        return iCount

    def checkByzantium(self, iGameTurn):

        # UHV 1: Own at least 6 cities in Calabria, Apulia, Dalmatia, Verona, Lombardy, Liguria, Tuscany, Latium, Corsica, Sardinia, Sicily, Tripolitania and Ifriqiya provinces in 632
        if iGameTurn == DateTurn.i632AD:
            if self.isPossibleUHV(Civ.BYZANTIUM.value, 0, True):
                iNumCities = 0
                for iProv in tByzantiumControl:
                    iNumCities += player(Civ.BYZANTIUM).getProvinceCityCount(iProv)
                if iNumCities >= 6:
                    self.wonUHV(Civ.BYZANTIUM.value, 0)
                else:
                    self.lostUHV(Civ.BYZANTIUM.value, 0)

        # UHV 2: Control Constantinople, Thrace, Thessaloniki, Moesia, Macedonia, Serbia, Arberia, Epirus, Thessaly, Morea, Colonea, Antiochia, Charsianon, Cilicia, Armeniakon, Anatolikon, Paphlagonia, Thrakesion and Opsikion in 1282
        elif iGameTurn == DateTurn.i1282AD:
            if self.isPossibleUHV(Civ.BYZANTIUM.value, 1, True):
                if self.checkProvincesStates(Civ.BYZANTIUM.value, tByzantiumControlII):
                    self.wonUHV(Civ.BYZANTIUM.value, 1)
                else:
                    self.lostUHV(Civ.BYZANTIUM.value, 1)

        # UHV 3: Make Constantinople the largest and most cultured city while being the richest empire in the world in 1453
        elif iGameTurn == DateTurn.i1453AD:
            if self.isPossibleUHV(Civ.BYZANTIUM.value, 2, True):
                x, y = CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM]
                iGold = player(Civ.BYZANTIUM).getGold()
                bMost = True
                for iCiv in civilizations().majors().ids():
                    if iCiv != Civ.BYZANTIUM.value and gc.getPlayer(iCiv).isAlive():
                        if gc.getPlayer(iCiv).getGold() > iGold:
                            bMost = False
                            break
                if (
                    gc.isLargestCity(x, y)
                    and gc.isTopCultureCity(x, y)
                    and gc.getMap().plot(x, y).getPlotCity().getOwner() == Civ.BYZANTIUM.value
                    and bMost
                ):
                    self.wonUHV(Civ.BYZANTIUM.value, 2)
                else:
                    self.lostUHV(Civ.BYZANTIUM.value, 2)

    def checkFrankia(self, iGameTurn):

        # UHV 1: Achieve Charlemagne's Empire by 840
        if self.isPossibleUHV(Civ.FRANCE.value, 0, True):
            if self.checkProvincesStates(Civ.FRANCE.value, tFrankControl):
                self.wonUHV(Civ.FRANCE.value, 0)
        if iGameTurn == DateTurn.i840AD:
            self.expireUHV(Civ.FRANCE.value, 0)

        # UHV 2: Control Jerusalem in 1291
        elif iGameTurn == DateTurn.i1291AD:
            if self.isPossibleUHV(Civ.FRANCE.value, 1, True):
                pJPlot = gc.getMap().plot(*CITIES[City.JERUSALEM])
                if pJPlot.isCity():
                    if pJPlot.getPlotCity().getOwner() == Civ.FRANCE.value:
                        self.wonUHV(Civ.FRANCE.value, 1)
                    else:
                        self.lostUHV(Civ.FRANCE.value, 1)
                else:
                    self.lostUHV(Civ.FRANCE.value, 1)

        # UHV 3: Build 5 Colonies
        # handled in the onProjectBuilt function

    def checkArabia(self, iGameTurn):

        # UHV 1: Control all territories from Tunisia to Asia Minor in 850
        if iGameTurn == DateTurn.i850AD:
            if self.isPossibleUHV(Civ.ARABIA.value, 0, True):
                if self.checkProvincesStates(Civ.ARABIA.value, tArabiaControlI):
                    self.wonUHV(Civ.ARABIA.value, 0)
                else:
                    self.lostUHV(Civ.ARABIA.value, 0)

        # UHV 2: Control the Levant and Egypt in 1291AD while being the most advanced civilization
        elif iGameTurn == DateTurn.i1291AD:
            if self.isPossibleUHV(Civ.ARABIA.value, 1, True):
                iMostAdvancedCiv = utils.getMostAdvancedCiv()
                if (
                    self.checkProvincesStates(Civ.ARABIA.value, tArabiaControlII)
                    and iMostAdvancedCiv == Civ.ARABIA.value
                ):
                    self.wonUHV(Civ.ARABIA.value, 1)
                else:
                    self.lostUHV(Civ.ARABIA.value, 1)

        # UHV 3: Spread Islam to at least 35% of the population of Europe
        if self.isPossibleUHV(Civ.ARABIA.value, 2, True):
            iPerc = gc.getGame().calculateReligionPercent(Religion.ISLAM.value)
            if iPerc >= 35:
                self.wonUHV(Civ.ARABIA.value, 2)

    def checkBulgaria(self, iGameTurn):

        # UHV 1: Conquer Moesia, Thrace, Macedonia, Serbia, Arberia, Thessaloniki and Constantinople by 917
        if self.isPossibleUHV(Civ.BULGARIA.value, 0, True):
            if self.checkProvincesStates(Civ.BULGARIA.value, tBulgariaControl):
                self.wonUHV(Civ.BULGARIA.value, 0)
        if iGameTurn == DateTurn.i917AD:
            self.expireUHV(Civ.BULGARIA.value, 0)

        # UHV 2: Accumulate at least 100 Orthodox Faith Points by 1259
        if self.isPossibleUHV(Civ.BULGARIA.value, 1, True):
            if (
                civilization(Civ.BULGARIA).has_state_religion(Religion.ORTHODOXY)
                and player(Civ.BULGARIA).getFaith() >= 100
            ):
                self.wonUHV(Civ.BULGARIA.value, 1)
        if iGameTurn == DateTurn.i1259AD:
            self.expireUHV(Civ.BULGARIA.value, 1)

        # UHV 3: Do not lose a city to Barbarians, Mongols, Byzantines, or Ottomans before 1396
        # Controlled in the onCityAcquired function
        elif iGameTurn == DateTurn.i1396AD:
            if self.isPossibleUHV(Civ.BULGARIA.value, 2, True):
                self.wonUHV(Civ.BULGARIA.value, 2)

    def checkCordoba(self, iGameTurn):

        # UHV 1: Make Cordoba the largest city in the world in 961
        if iGameTurn == DateTurn.i961AD:
            if self.isPossibleUHV(Civ.CORDOBA.value, 0, True):
                x, y = CIV_CAPITAL_LOCATIONS[Civ.CORDOBA]
                if (
                    gc.isLargestCity(x, y)
                    and gc.getMap().plot(x, y).getPlotCity().getOwner() == Civ.CORDOBA.value
                ):
                    self.wonUHV(Civ.CORDOBA.value, 0)
                else:
                    self.lostUHV(Civ.CORDOBA.value, 0)

        # UHV 2: Build the Alhambra, the Gardens of Al-Andalus, and La Mezquita by 1309
        # Controlled in the onBuildingBuilt function
        elif iGameTurn == DateTurn.i1309AD:
            self.expireUHV(Civ.CORDOBA.value, 1)

        # UHV 3: Make sure Islam is present in every city in the Iberian peninsula in 1492
        elif iGameTurn == DateTurn.i1492AD:
            if self.isPossibleUHV(Civ.CORDOBA.value, 2, True):
                bIslamized = True
                for iProv in tCordobaIslamize:
                    if not player(Civ.CORDOBA).provinceIsSpreadReligion(
                        iProv, Religion.ISLAM.value
                    ):
                        bIslamized = False
                        break
                if bIslamized:
                    self.wonUHV(Civ.CORDOBA.value, 2)
                else:
                    self.lostUHV(Civ.CORDOBA.value, 2)

    def checkNorway(self, iGameTurn):

        # Old UHV1: explore all water tiles
        # if ( iGameTurn == DateTurn.i1009AD and pNorway.getUHV( 0 ) == -1 ):
        # 	if ( gc.canSeeAllTerrain( iNorway, Terrain.OCEAN.value ) ):
        # 		self.wonUHV( iNorway, 0 )
        # 	else:
        # 		self.lostUHV( iNorway, 0 )

        # UHV 1: Gain 100 Viking Points and build Vinland by 1066
        # Viking points counted in the onCityAcquired, onPillageImprovement and onCombatResult functions
        if self.isPossibleUHV(Civ.NORWAY.value, 0, True):
            if (
                player(Civ.NORWAY).getUHVCounter(0) >= 100
                and team(Civ.NORWAY).getProjectCount(Colony.VINLAND.value) >= 1
            ):
                self.wonUHV(Civ.NORWAY.value, 0)
        if iGameTurn == DateTurn.i1066AD:
            self.expireUHV(Civ.NORWAY.value, 0)

        # UHV 2: Conquer The Isles, Ireland, Scotland, Normandy, Sicily, Apulia, Calabria and Iceland by 1194
        if iGameTurn <= DateTurn.i1194AD:
            if self.isPossibleUHV(Civ.NORWAY.value, 1, True):
                if self.checkProvincesStates(Civ.NORWAY.value, tNorwayControl):
                    self.wonUHV(Civ.NORWAY.value, 1)
        if iGameTurn == DateTurn.i1194AD:
            self.expireUHV(Civ.NORWAY.value, 1)

        # UHV 3: Have a higher score than Sweden, Denmark, Scotland, England, Germany and France in 1320
        elif iGameTurn == DateTurn.i1320AD:
            if self.isPossibleUHV(Civ.NORWAY.value, 2, True):
                iNorwayRank = gc.getGame().getTeamRank(Civ.NORWAY.value)
                bIsOnTop = True
                for iTestPlayer in tNorwayOutrank:
                    if gc.getGame().getTeamRank(iTestPlayer) < iNorwayRank:
                        bIsOnTop = False
                        break
                if bIsOnTop:
                    self.wonUHV(Civ.NORWAY.value, 2)
                else:
                    self.lostUHV(Civ.NORWAY.value, 2)

    def checkDenmark(self, iGameTurn):

        # UHV 1: Control Denmark, Skaneland, G�taland, Svealand, Mercia, London, Northumbria and East Anglia in 1050
        if iGameTurn == DateTurn.i1050AD:
            if self.isPossibleUHV(Civ.DENMARK.value, 0, True):
                if self.checkProvincesStates(Civ.DENMARK.value, tDenmarkControlI):
                    self.wonUHV(Civ.DENMARK.value, 0)
                else:
                    self.lostUHV(Civ.DENMARK.value, 0)

        # UHV 2: Control Denmark, Norway, Vestfold, Skaneland, G�taland, Svealand, Norrland, Gotland, �sterland, Estonia and Iceland in 1523
        elif iGameTurn == DateTurn.i1523AD:
            if self.isPossibleUHV(Civ.DENMARK.value, 1, True):
                if self.checkProvincesStates(Civ.DENMARK.value, tDenmarkControlIII):
                    self.wonUHV(Civ.DENMARK.value, 1)
                else:
                    self.lostUHV(Civ.DENMARK.value, 1)

        # UHV 3: Build 3 Colonies and complete both Trading Companies
        # handled in the onProjectBuilt function

    def checkVenecia(self, iGameTurn):

        # UHV 1: Conquer the Adriatic by 1004
        if self.isPossibleUHV(Civ.VENECIA.value, 0, True):
            if self.checkProvincesStates(Civ.VENECIA.value, tVenetianControl):
                self.wonUHV(Civ.VENECIA.value, 0)
        if iGameTurn == DateTurn.i1004AD:
            self.expireUHV(Civ.VENECIA.value, 0)

        # UHV 2: Conquer Constantinople, Thessaly, Morea, Crete and Cyprus by 1204
        if self.isPossibleUHV(Civ.VENECIA.value, 1, True):
            if (
                player(Civ.VENECIA).getProvinceCurrentState(Province.CONSTANTINOPLE.value)
                >= ProvinceStatus.CONQUER.value
            ):
                if self.checkProvincesStates(Civ.VENECIA.value, tVenetianControlII):
                    self.wonUHV(Civ.VENECIA.value, 1)
        if iGameTurn == DateTurn.i1204AD:
            self.expireUHV(Civ.VENECIA.value, 1)

        # UHV 3: Be the first to build a Colony from the Age of Discovery
        # UHV 3: Vinland is from the Viking Age, all other Colonies are from the Age of Discovery
        # handled in the onProjectBuilt function

    def checkBurgundy(self, iGameTurn):

        # UHV 1: Produce 12,000 culture points in your cities by 1336
        # The counter should be updated until the deadline for the challenge UHVs, even after UHV completion
        if iGameTurn < DateTurn.i1336AD + 2:
            iCulture = (
                player(Civ.BURGUNDY).getUHVCounter(0) + player(Civ.BURGUNDY).countCultureProduced()
            )
            player(Civ.BURGUNDY).setUHVCounter(0, iCulture)
            if self.isPossibleUHV(Civ.BURGUNDY.value, 0, True):
                if iCulture >= 12000:
                    self.wonUHV(Civ.BURGUNDY.value, 0)
        if iGameTurn == DateTurn.i1336AD:
            self.expireUHV(Civ.BURGUNDY.value, 0)

        # UHV 2: Control Burgundy, Provence, Picardy, Flanders, Champagne and Lorraine in 1376
        elif iGameTurn == DateTurn.i1376AD:
            if self.isPossibleUHV(Civ.BURGUNDY.value, 1, True):
                if self.checkProvincesStates(Civ.BURGUNDY.value, tBurgundyControl):
                    self.wonUHV(Civ.BURGUNDY.value, 1)
                else:
                    self.lostUHV(Civ.BURGUNDY.value, 1)

        # UHV 3: Have a higher score than France, England and Germany in 1473
        elif iGameTurn == DateTurn.i1473AD:
            if self.isPossibleUHV(Civ.BURGUNDY.value, 2, True):
                iBurgundyRank = gc.getGame().getTeamRank(Civ.BURGUNDY.value)
                bIsOnTop = True
                for iTestPlayer in tBurgundyOutrank:
                    if gc.getGame().getTeamRank(iTestPlayer) < iBurgundyRank:
                        bIsOnTop = False
                        break
                if bIsOnTop:
                    self.wonUHV(Civ.BURGUNDY.value, 2)
                else:
                    self.lostUHV(Civ.BURGUNDY.value, 2)

    def checkGermany(self, iGameTurn):

        # Old UHVs: Have most Catholic FPs in 1077 (Walk to Canossa)
        # 			Have 3 vassals

        # UHV 1: Control Lorraine, Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Lombardy, Liguria and Tuscany in 1167
        if iGameTurn == DateTurn.i1167AD:
            if self.isPossibleUHV(Civ.GERMANY.value, 0, True):
                if self.checkProvincesStates(Civ.GERMANY.value, tGermanyControl):
                    self.wonUHV(Civ.GERMANY.value, 0)
                else:
                    self.lostUHV(Civ.GERMANY.value, 0)

        # UHV 2: Start the Reformation (Found Protestantism)
        # Controlled in the onReligionFounded function

        # UHV 3: Control Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Flanders, Pomerania, Silesia, Bohemia, Moravia and Austria in 1648
        elif iGameTurn == DateTurn.i1648AD:
            if self.isPossibleUHV(Civ.GERMANY.value, 2, True):
                if self.checkProvincesStates(Civ.GERMANY.value, tGermanyControlII):
                    self.wonUHV(Civ.GERMANY.value, 2)
                else:
                    self.lostUHV(Civ.GERMANY.value, 2)

    def checkNovgorod(self, iGameTurn):

        # UHV 1: Control Novgorod, Karelia, Estonia, Livonia, Rostov, Vologda and Osterland in 1284
        if iGameTurn == DateTurn.i1284AD:
            if self.isPossibleUHV(Civ.NOVGOROD.value, 0, True):
                if self.checkProvincesStates(Civ.NOVGOROD.value, tNovgorodControl):
                    self.wonUHV(Civ.NOVGOROD.value, 0)
                else:
                    self.lostUHV(Civ.NOVGOROD.value, 0)

        # UHV 2: Control eleven sources of fur by 1397
        if self.isPossibleUHV(Civ.NOVGOROD.value, 1, True):
            if player(Civ.NOVGOROD).countCultBorderBonuses(Bonus.FUR.value) >= 11:
                self.wonUHV(Civ.NOVGOROD.value, 1)
        if iGameTurn == DateTurn.i1397AD:
            self.expireUHV(Civ.NOVGOROD.value, 1)

        # UHV 3: Control the province of Moscow or have Muscovy as a vassal in 1478
        if iGameTurn == DateTurn.i1478AD:
            if self.isPossibleUHV(Civ.NOVGOROD.value, 2, True):
                if (
                    player(Civ.NOVGOROD).getProvinceCurrentState(Province.MOSCOW.value)
                    >= ProvinceStatus.CONQUER.value
                ):
                    self.wonUHV(Civ.NOVGOROD.value, 2)
                elif civilization(Civ.MOSCOW).is_alive() and civilization(Civ.MOSCOW).is_vassal(
                    Civ.NOVGOROD
                ):
                    self.wonUHV(Civ.NOVGOROD.value, 2)
                else:
                    self.lostUHV(Civ.NOVGOROD.value, 2)

    def checkKiev(self, iGameTurn):

        # UHV 1: Build 2 Orthodox cathedrals and 8 Orthodox monasteries by 1250
        # Controlled in the onBuildingBuilt function
        if iGameTurn == DateTurn.i1250AD + 1:
            self.expireUHV(Civ.KIEV.value, 0)

        # UHV 2: Control 10 provinces out of Kiev, Podolia, Pereyaslavl, Sloboda, Chernigov, Volhynia, Minsk, Polotsk, Smolensk, Moscow, Murom, Rostov, Novgorod and Vologda in 1288
        elif iGameTurn == DateTurn.i1288AD:
            if self.isPossibleUHV(Civ.KIEV.value, 1, True):
                iConq = 0
                for iProv in tKievControl:
                    if (
                        player(Civ.KIEV).getProvinceCurrentState(iProv)
                        >= ProvinceStatus.CONQUER.value
                    ):
                        iConq += 1
                if iConq >= 10:
                    self.wonUHV(Civ.KIEV.value, 1)
                else:
                    self.lostUHV(Civ.KIEV.value, 1)

        # UHV 3: Produce 25000 food by 1300
        # The counter should be updated until the deadline for the challenge UHVs, even after UHV completion
        if iGameTurn < DateTurn.i1300AD + 2:
            iFood = player(Civ.KIEV).getUHVCounter(2) + player(Civ.KIEV).calculateTotalYield(
                YieldTypes.YIELD_FOOD
            )
            player(Civ.KIEV).setUHVCounter(2, iFood)
            if self.isPossibleUHV(Civ.KIEV.value, 2, True):
                if iFood > 25000:
                    self.wonUHV(Civ.KIEV.value, 2)
        if iGameTurn == DateTurn.i1300AD:
            self.expireUHV(Civ.KIEV.value, 2)

    def checkHungary(self, iGameTurn):

        # UHV 1: Control Austria, Carinthia, Moravia, Silesia, Bohemia, Dalmatia, Bosnia, Banat, Wallachia and Moldova in 1490
        if iGameTurn == DateTurn.i1490AD:
            if self.isPossibleUHV(Civ.HUNGARY.value, 0, True):
                if self.checkProvincesStates(Civ.HUNGARY.value, tHungaryControl):
                    self.wonUHV(Civ.HUNGARY.value, 0)
                else:
                    self.lostUHV(Civ.HUNGARY.value, 0)

        # UHV 2: Allow no Ottoman cities in Europe in 1541
        elif iGameTurn == DateTurn.i1541AD:
            if self.isPossibleUHV(Civ.HUNGARY.value, 1, True):
                bClean = True
                if civilization(Civ.OTTOMAN).is_alive():
                    for iProv in tHungaryControlII:
                        if player(Civ.OTTOMAN).getProvinceCityCount(iProv) > 0:
                            bClean = False
                            break
                if bClean:
                    self.wonUHV(Civ.HUNGARY.value, 1)
                else:
                    self.lostUHV(Civ.HUNGARY.value, 1)

        # UHV 3: Be the first to adopt Free Religion
        if self.isPossibleUHV(Civ.HUNGARY.value, 2, True):
            iReligiousCivic = player(Civ.HUNGARY).getCivics(4)
            if iReligiousCivic == Civic.FREE_RELIGION.value:
                self.wonUHV(Civ.HUNGARY.value, 2)
            else:
                for iPlayer in civilizations().majors().ids():
                    pPlayer = gc.getPlayer(iPlayer)
                    if pPlayer.isAlive() and pPlayer.getCivics(4) == Civic.FREE_RELIGION.value:
                        self.lostUHV(Civ.HUNGARY.value, 2)

    def checkSpain(self, iGameTurn):

        # UHV 1: Reconquista (make sure Catholicism is the only religion present in every city in the Iberian peninsula in 1492)
        if iGameTurn == DateTurn.i1492AD:
            if self.isPossibleUHV(Civ.CASTILE.value, 0, True):
                bConverted = True
                for iProv in tSpainConvert:
                    if not player(Civ.CASTILE).provinceIsConvertReligion(
                        iProv, Religion.CATHOLICISM.value
                    ):
                        bConverted = False
                        break
                if bConverted:
                    self.wonUHV(Civ.CASTILE.value, 0)
                else:
                    self.lostUHV(Civ.CASTILE.value, 0)

        # UHV 2: Have more Colonies than any other nation in 1588, while having at least 3
        elif iGameTurn == DateTurn.i1588AD:
            if self.isPossibleUHV(Civ.CASTILE.value, 1, True):
                bMost = True
                iSpainColonies = self.getNumRealColonies(Civ.CASTILE.value)
                for iPlayer in civilizations().majors().ids():
                    if iPlayer != Civ.CASTILE.value:
                        pPlayer = gc.getPlayer(iPlayer)
                        if (
                            pPlayer.isAlive()
                            and self.getNumRealColonies(iPlayer) >= iSpainColonies
                        ):
                            bMost = False
                if bMost and iSpainColonies >= 3:
                    self.wonUHV(Civ.CASTILE.value, 1)
                else:
                    self.lostUHV(Civ.CASTILE.value, 1)

        # UHV 3: Ensure that Catholic nations have more population and more land than any other religion in 1648
        elif iGameTurn == DateTurn.i1648AD:
            if self.isPossibleUHV(Civ.CASTILE.value, 2, True):
                if player(Civ.CASTILE).getStateReligion() != Religion.CATHOLICISM.value:
                    self.lostUHV(Civ.CASTILE.value, 2)
                else:
                    lLand = [0, 0, 0, 0, 0, 0]  # Prot, Islam, Cath, Orth, Jew, Pagan
                    lPop = [0, 0, 0, 0, 0, 0]
                    for iPlayer in civilizations().majors().ids():
                        pPlayer = gc.getPlayer(iPlayer)
                        iStateReligion = pPlayer.getStateReligion()
                        if iStateReligion > -1:
                            lLand[iStateReligion] += pPlayer.getTotalLand()
                            lPop[iStateReligion] += pPlayer.getTotalPopulation()
                        else:
                            lLand[5] += pPlayer.getTotalLand()
                            lPop[5] += pPlayer.getTotalPopulation()
                    # The Barbarian civ counts as Pagan, Independent cities are included separately, based on the religion of the population
                    lLand[5] += civilizations().barbarian().unwrap().player.getTotalLand()
                    lPop[5] += civilizations().barbarian().unwrap().player.getTotalPopulation()
                    for iIndyCiv in [
                        Civ.INDEPENDENT.value,
                        Civ.INDEPENDENT_2.value,
                        Civ.INDEPENDENT_3.value,
                        Civ.INDEPENDENT_4.value,
                    ]:
                        for pCity in utils.getCityList(iIndyCiv):
                            pIndyCiv = gc.getPlayer(iIndyCiv)
                            iAverageCityLand = pIndyCiv.getTotalLand() / pIndyCiv.getNumCities()
                            if pCity.getReligionCount() == 0:
                                lLand[5] += iAverageCityLand
                                lPop[5] += pCity.getPopulation()
                            else:
                                for iReligion in range(len(Religion)):
                                    if pCity.isHasReligion(iReligion):
                                        lLand[iReligion] += (
                                            iAverageCityLand / pCity.getReligionCount()
                                        )
                                        lPop[iReligion] += (
                                            pCity.getPopulation() / pCity.getReligionCount()
                                        )

                    iCathLand = lLand[Religion.CATHOLICISM.value]
                    iCathPop = lPop[Religion.CATHOLICISM.value]

                    bWon = True
                    for iReligion in range(len(Religion) + 1):
                        if iReligion != Religion.CATHOLICISM.value:
                            if lLand[iReligion] >= iCathLand:
                                bWon = False
                                break
                            if lPop[iReligion] >= iCathPop:
                                bWon = False
                                break

                    if bWon:
                        self.wonUHV(Civ.CASTILE.value, 2)
                    else:
                        self.lostUHV(Civ.CASTILE.value, 2)

    def checkScotland(self, iGameTurn):

        # UHV 1: Have 10 Forts and 4 Castles by 1296
        if self.isPossibleUHV(Civ.SCOTLAND.value, 0, True):
            iForts = player(Civ.SCOTLAND).getImprovementCount(Improvement.FORT.value)
            iCastles = player(Civ.SCOTLAND).countNumBuildings(Building.CASTLE.value)
            if iForts >= 10 and iCastles >= 4:
                self.wonUHV(Civ.SCOTLAND.value, 0)
        if iGameTurn == DateTurn.i1296AD:
            self.expireUHV(Civ.SCOTLAND.value, 0)

        # UHV 2: Have 1500 Attitude Points with France by 1560 (Attitude Points are added every turn depending on your relations)
        if self.isPossibleUHV(Civ.SCOTLAND.value, 1, True):
            if civilization(Civ.FRANCE).is_alive():
                # Being at war with France gives a big penalty (and ignores most bonuses!)
                if civilization(Civ.SCOTLAND).at_war(Civ.FRANCE):
                    iScore = -10
                else:
                    # -1 for Furious 0 for Annoyed 1 for Cautious 2 for Pleased 3 for Friendly
                    iScore = player(Civ.FRANCE).AI_getAttitude(Civ.SCOTLAND.value) - 1
                    # Agreements
                    if team(Civ.FRANCE).isOpenBorders(Civ.SCOTLAND.value):
                        iScore += 1
                    if team(Civ.FRANCE).isDefensivePact(Civ.SCOTLAND.value):
                        iScore += 2
                    # Imports/Exports
                    iTrades = 0
                    iTrades += player(Civ.SCOTLAND).getNumTradeBonusImports(Civ.FRANCE.value)
                    iTrades += player(Civ.FRANCE).getNumTradeBonusImports(Civ.SCOTLAND.value)
                    iScore += iTrades / 2
                    # Common Wars
                    for iEnemy in civilizations().majors().ids():
                        if iEnemy in [Civ.SCOTLAND.value, Civ.FRANCE.value]:
                            continue
                        if team(Civ.FRANCE).isAtWar(iEnemy) and team(Civ.SCOTLAND).isAtWar(iEnemy):
                            iScore += 2
                # Different religion from France also gives a penalty, same religion gives a bonus (but only if both have a state religion)
                if (
                    civilization(Civ.SCOTLAND).has_a_state_religion()
                    and civilization(Civ.FRANCE).has_a_state_religion()
                ):
                    if (
                        civilization(Civ.SCOTLAND).state_religion()
                        != civilization(Civ.FRANCE).state_religion()
                    ):
                        iScore -= 3
                    elif (
                        civilization(Civ.SCOTLAND).state_religion()
                        == civilization(Civ.FRANCE).state_religion()
                    ):
                        iScore += 1
                iOldScore = player(Civ.SCOTLAND).getUHVCounter(1)
                iNewScore = iOldScore + iScore
                player(Civ.SCOTLAND).setUHVCounter(1, iNewScore)
                if iNewScore >= 1500:
                    self.wonUHV(Civ.SCOTLAND.value, 1)
        if iGameTurn == DateTurn.i1560AD:
            self.expireUHV(Civ.SCOTLAND.value, 1)

        # UHV 3: Control Scotland, The Isles, Ireland, Wales, Brittany and Galicia in 1700
        elif iGameTurn == DateTurn.i1700AD:
            if self.isPossibleUHV(Civ.SCOTLAND.value, 2, True):
                if self.checkProvincesStates(Civ.SCOTLAND.value, tScotlandControl):
                    self.wonUHV(Civ.SCOTLAND.value, 2)
                else:
                    self.lostUHV(Civ.SCOTLAND.value, 2)

    def checkPoland(self, iGameTurn):

        # Old UHVs: Don't lose cities until 1772 or conquer Russia until 1772
        # 			Vassalize Russia, Germany and Austria

        # UHV 1: Food production between 1500 and 1520
        if DateTurn.i1500AD <= iGameTurn <= DateTurn.i1520AD:
            if self.isPossibleUHV(Civ.POLAND.value, 0, True):
                iAgriculturePolish = player(Civ.POLAND).calculateTotalYield(YieldTypes.YIELD_FOOD)
                bFood = True
                for iPlayer in civilizations().majors().ids():
                    if (
                        gc.getPlayer(iPlayer).calculateTotalYield(YieldTypes.YIELD_FOOD)
                        > iAgriculturePolish
                    ):
                        bFood = False
                        break
                if bFood:
                    self.wonUHV(Civ.POLAND.value, 0)
        if iGameTurn == DateTurn.i1520AD + 1:
            self.expireUHV(Civ.POLAND.value, 0)

        # UHV 2: Own at least 12 cities in the given provinces in 1569
        elif iGameTurn == DateTurn.i1569AD:
            if self.isPossibleUHV(Civ.POLAND.value, 1, True):
                iNumCities = 0
                for iProv in tPolishControl:
                    iNumCities += player(Civ.POLAND).getProvinceCityCount(iProv)
                if iNumCities >= 12:
                    self.wonUHV(Civ.POLAND.value, 1)
                else:
                    self.lostUHV(Civ.POLAND.value, 1)

        # UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
        # Controlled in the onBuildingBuilt and onCityAcquired functions

    def checkGenoa(self, iGameTurn):

        # UHV 1: Control Corsica, Sardinia, Crete, Rhodes, Thrakesion, Cyprus and Crimea in 1400
        if iGameTurn == DateTurn.i1400AD:
            if self.isPossibleUHV(Civ.GENOA.value, 0, True):
                if self.checkProvincesStates(Civ.GENOA.value, tGenoaControl):
                    self.wonUHV(Civ.GENOA.value, 0)
                else:
                    self.lostUHV(Civ.GENOA.value, 0)

        # UHV 2: Have the largest total amount of commerce from foreign Trade Route Exports and Imports in 1566
        # UHV 2: Export is based on your cities' trade routes with foreign cities, import is based on foreign cities' trade routes with your cities
        elif iGameTurn == DateTurn.i1566AD:
            if self.isPossibleUHV(Civ.GENOA.value, 1, True):
                iGenoaTrade = player(Civ.GENOA).calculateTotalImports(
                    YieldTypes.YIELD_COMMERCE
                ) + player(Civ.GENOA).calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                bLargest = True
                for iPlayer in civilizations().majors().ids():
                    if iPlayer != Civ.GENOA.value:
                        pPlayer = gc.getPlayer(iPlayer)
                        if (
                            pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
                            + pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                            > iGenoaTrade
                        ):
                            bLargest = False
                            break
                if bLargest:
                    self.wonUHV(Civ.GENOA.value, 1)
                else:
                    self.lostUHV(Civ.GENOA.value, 1)

        # UHV 3: Have 8 Banks and own all Bank of St. George cities in 1625
        elif iGameTurn == DateTurn.i1625AD:
            if self.isPossibleUHV(Civ.GENOA.value, 2, True):
                iBanks = 0
                for city in utils.getCityList(Civ.GENOA.value):
                    if (
                        city.getNumRealBuilding(Building.BANK.value) > 0
                        or city.getNumRealBuilding(Building.GENOA_BANK.value) > 0
                        or city.getNumRealBuilding(Building.ENGLISH_ROYAL_EXCHANGE.value) > 0
                    ):
                        iBanks += 1
                iCompanyCities = player(Civ.GENOA).countCorporations(Company.ST_GEORGE.value)
                if iBanks >= 8 and iCompanyCities == COMPANIES[Company.ST_GEORGE].limit:
                    self.wonUHV(Civ.GENOA.value, 2)
                else:
                    self.lostUHV(Civ.GENOA.value, 2)

    def checkMorocco(self, iGameTurn):

        # UHV 1: Control Morocco, Marrakesh, Fez, Tetouan, Oran, Algiers, Ifriqiya, Andalusia, Valencia and the Balearic Islands in 1248
        if iGameTurn == DateTurn.i1248AD:
            if self.isPossibleUHV(Civ.MOROCCO.value, 0, True):
                if self.checkProvincesStates(Civ.MOROCCO.value, tMoroccoControl):
                    self.wonUHV(Civ.MOROCCO.value, 0)
                else:
                    self.lostUHV(Civ.MOROCCO.value, 0)

        # UHV 2: Have 5000 culture in each of three cities in 1465
        elif iGameTurn == DateTurn.i1465AD:
            if self.isPossibleUHV(Civ.MOROCCO.value, 1, True):
                iGoodCities = 0
                for city in utils.getCityList(Civ.MOROCCO.value):
                    if city.getCulture(Civ.MOROCCO.value) >= 5000:
                        iGoodCities += 1
                if iGoodCities >= 3:
                    self.wonUHV(Civ.MOROCCO.value, 1)
                else:
                    self.lostUHV(Civ.MOROCCO.value, 1)

        # UHV 3: Destroy or vassalize Portugal, Spain, and Aragon by 1578
        if DateTurn.i1164AD <= iGameTurn <= DateTurn.i1578AD:
            if self.isPossibleUHV(Civ.MOROCCO.value, 2, True):
                bConq = True
                if (
                    (
                        civilization(Civ.CASTILE).is_alive()
                        and not civilization(Civ.CASTILE).is_vassal(Civ.MOROCCO)
                    )
                    or (
                        civilization(Civ.PORTUGAL).is_alive()
                        and not civilization(Civ.PORTUGAL).is_vassal(Civ.MOROCCO)
                    )
                    or (
                        civilization(Civ.ARAGON).is_alive()
                        and not civilization(Civ.ARAGON).is_vassal(Civ.MOROCCO)
                    )
                ):
                    bConq = False

                if bConq:
                    self.wonUHV(Civ.MOROCCO.value, 2)
        if iGameTurn == DateTurn.i1578AD + 1:
            self.expireUHV(Civ.MOROCCO.value, 2)

    def checkEngland(self, iGameTurn):

        # UHV 1: Control London, Wessex, East Anglia, Mercia, Northumbria, Scotland, Wales, Ireland, Normandy, Picardy, Bretagne, Il-de-France, Aquitania and Orleans in 1452
        if iGameTurn == DateTurn.i1452AD:
            if self.isPossibleUHV(Civ.ENGLAND.value, 0, True):
                if self.checkProvincesStates(Civ.ENGLAND.value, tEnglandControl):
                    self.wonUHV(Civ.ENGLAND.value, 0)
                else:
                    self.lostUHV(Civ.ENGLAND.value, 0)

        # UHV 2: Build 7 Colonies
        # Controlled in the onProjectBuilt function

        # UHV 3: Be the first to enter the Industrial age
        # Controlled in the onTechAcquired function

    def checkPortugal(self, iGameTurn):

        # UHV 1: Settle 3 cities on the Azores, Canaries and Madeira and 2 in Morocco, Tetouan and Oran
        # Controlled in the onCityBuilt function

        # UHV 2: Do not lose a city before 1640
        # Controlled in the onCityAcquired function
        if iGameTurn == DateTurn.i1640AD:
            if self.isPossibleUHV(Civ.PORTUGAL.value, 1, True):
                self.wonUHV(Civ.PORTUGAL.value, 1)

        # UHV 3: Build 5 Colonies
        # Controlled in the onProjectBuilt function

    def checkAragon(self, iGameTurn):

        # UHV 1: Control Catalonia, Valencia, Balears and Sicily in 1282
        if iGameTurn == DateTurn.i1282AD:
            if self.isPossibleUHV(Civ.ARAGON.value, 0, True):
                if self.checkProvincesStates(Civ.ARAGON.value, tAragonControlI):
                    self.wonUHV(Civ.ARAGON.value, 0)
                else:
                    self.lostUHV(Civ.ARAGON.value, 0)

        # UHV 2: Have 12 Consulates of the Sea and 30 Trade Ships in 1444
        # UHV 2: Ships with at least one cargo space count as Trade Ships
        elif iGameTurn == DateTurn.i1444AD:
            if self.isPossibleUHV(Civ.ARAGON.value, 1, True):
                iPorts = player(Civ.ARAGON).countNumBuildings(Building.ARAGON_SEAPORT.value)
                iCargoShips = utils.getCargoShips(Civ.ARAGON.value)
                if iPorts >= 12 and iCargoShips >= 30:
                    self.wonUHV(Civ.ARAGON.value, 1)
                else:
                    self.lostUHV(Civ.ARAGON.value, 1)

        # UHV 3: Control Catalonia, Valencia, Aragon, Balears, Corsica, Sardinia, Sicily, Calabria, Apulia, Provence and Thessaly in 1474
        elif iGameTurn == DateTurn.i1474AD:
            if self.isPossibleUHV(Civ.ARAGON.value, 2, True):
                if self.checkProvincesStates(Civ.ARAGON.value, tAragonControlII):
                    self.wonUHV(Civ.ARAGON.value, 2)
                else:
                    self.lostUHV(Civ.ARAGON.value, 2)

    def checkPrussia(self, iGameTurn):

        # UHV 1: Control Prussia, Suvalkija, Lithuania, Livonia, Estonia, and Pomerania in 1410
        if iGameTurn == DateTurn.i1410AD:
            if self.isPossibleUHV(Civ.PRUSSIA.value, 0, True):
                if self.checkProvincesStates(Civ.PRUSSIA.value, tPrussiaControlI):
                    self.wonUHV(Civ.PRUSSIA.value, 0)
                else:
                    self.lostUHV(Civ.PRUSSIA.value, 0)

        # UHV 2: Conquer two cities from each of Austria, Muscovy, Germany, Sweden, France and Spain between 1650 and 1763, if they are still alive
        # Controlled in the onCityAcquired function
        if iGameTurn == DateTurn.i1763AD + 1:
            self.expireUHV(Civ.PRUSSIA.value, 1)

        # UHV 3: Settle a total of 15 Great People in your capital
        # UHV 3: Great People can be settled in any combination, Great Generals included
        if self.isPossibleUHV(Civ.PRUSSIA.value, 2, True):
            pCapital = player(Civ.PRUSSIA).getCapitalCity()
            iGPStart = gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST")
            iGPEnd = gc.getInfoTypeForString("SPECIALIST_GREAT_SPY")
            iGPeople = 0
            for iType in range(iGPStart, iGPEnd + 1):
                iGPeople += pCapital.getFreeSpecialistCount(iType)
            if iGPeople >= 15:
                self.wonUHV(Civ.PRUSSIA.value, 2)

    def checkLithuania(self, iGameTurn):

        # UHV 1: Accumulate 2500 Culture points without declaring a state religion before 1386
        # The counter should be updated until the deadline for the challenge UHVs, even after UHV completion
        if iGameTurn < DateTurn.i1386AD + 2:
            iCulture = (
                player(Civ.LITHUANIA).getUHVCounter(0)
                + player(Civ.LITHUANIA).countCultureProduced()
            )
            player(Civ.LITHUANIA).setUHVCounter(0, iCulture)
            if self.isPossibleUHV(Civ.LITHUANIA.value, 0, True):
                if civilization(Civ.LITHUANIA).has_a_state_religion():
                    self.lostUHV(Civ.LITHUANIA.value, 0)
                else:
                    if iCulture >= 2500:
                        self.wonUHV(Civ.LITHUANIA.value, 0)
        if iGameTurn == DateTurn.i1386AD:
            self.expireUHV(Civ.LITHUANIA.value, 0)

        # UHV 2: Control the most territory in Europe in 1430
        elif iGameTurn == DateTurn.i1430AD:
            if self.isPossibleUHV(Civ.LITHUANIA.value, 1, True):
                bMost = True
                iCount = self.getTerritoryPercentEurope(Civ.LITHUANIA.value)
                for iOtherPlayer in civilizations().majors().ids():
                    if (
                        not gc.getPlayer(iOtherPlayer).isAlive()
                        or iOtherPlayer == Civ.LITHUANIA.value
                    ):
                        continue
                    iOtherCount = self.getTerritoryPercentEurope(iOtherPlayer)
                    if iOtherCount >= iCount:
                        bMost = False
                        break
                if bMost:
                    self.wonUHV(Civ.LITHUANIA.value, 1)
                else:
                    self.lostUHV(Civ.LITHUANIA.value, 1)

        # UHV 3: Destroy or Vassalize Muscovy, Novgorod and Prussia by 1795
        if DateTurn.i1380AD <= iGameTurn <= DateTurn.i1795AD:
            if self.isPossibleUHV(Civ.LITHUANIA.value, 2, True):
                bConq = True
                if (
                    (
                        civilization(Civ.MOSCOW).is_alive()
                        and not civilization(Civ.MOSCOW).is_vassal(Civ.LITHUANIA)
                    )
                    or (
                        civilization(Civ.NOVGOROD).is_alive()
                        and not civilization(Civ.NOVGOROD).is_vassal(Civ.LITHUANIA)
                    )
                    or (
                        civilization(Civ.PRUSSIA).is_alive()
                        and not civilization(Civ.PRUSSIA).is_vassal(Civ.LITHUANIA)
                    )
                ):
                    bConq = False

                if bConq:
                    self.wonUHV(Civ.LITHUANIA.value, 2)
        if iGameTurn == DateTurn.i1795AD + 1:
            self.expireUHV(Civ.LITHUANIA.value, 2)

    def checkAustria(self, iGameTurn):

        # UHV 1: Control all of medieval Austria, Hungary and Bohemia in 1617
        if iGameTurn == DateTurn.i1617AD:
            if self.isPossibleUHV(Civ.AUSTRIA.value, 0, True):
                if self.checkProvincesStates(Civ.AUSTRIA.value, tAustriaControl):
                    self.wonUHV(Civ.AUSTRIA.value, 0)
                else:
                    self.lostUHV(Civ.AUSTRIA.value, 0)

        # UHV 2: Have 3 vassals in 1700
        elif iGameTurn == DateTurn.i1700AD:
            if self.isPossibleUHV(Civ.AUSTRIA.value, 1, True):
                iCount = 0
                for iPlayer in civilizations().majors().ids():
                    if iPlayer == Civ.AUSTRIA.value:
                        continue
                    pPlayer = gc.getPlayer(iPlayer)
                    if pPlayer.isAlive():
                        if gc.getTeam(pPlayer.getTeam()).isVassal(team(Civ.AUSTRIA).getID()):
                            iCount += 1
                if iCount >= 3:
                    self.wonUHV(Civ.AUSTRIA.value, 1)
                else:
                    self.lostUHV(Civ.AUSTRIA.value, 1)

        # UHV 3: Have the highest score in 1780
        elif iGameTurn == DateTurn.i1780AD:
            if self.isPossibleUHV(Civ.AUSTRIA.value, 2, True):
                if gc.getGame().getTeamRank(Civ.AUSTRIA.value) == 0:
                    self.wonUHV(Civ.AUSTRIA.value, 2)
                else:
                    self.lostUHV(Civ.AUSTRIA.value, 2)

    def checkTurkey(self, iGameTurn):

        # UHV 1: Control Constantinople, the Balkans, Anatolia, the Levant and Egypt in 1517
        if iGameTurn == DateTurn.i1517AD:
            if self.isPossibleUHV(Civ.OTTOMAN.value, 0, True):
                if self.checkProvincesStates(Civ.OTTOMAN.value, tOttomanControlI):
                    self.wonUHV(Civ.OTTOMAN.value, 0)
                else:
                    self.lostUHV(Civ.OTTOMAN.value, 0)

        # UHV 2: Construct the Topkapi Palace, the Blue Mosque, the Selimiye Mosque and the Tomb of Al-Walid by 1616
        # Controlled in the onBuildingBuilt function
        elif iGameTurn == DateTurn.i1616AD:
            self.expireUHV(Civ.OTTOMAN.value, 1)

        # UHV 3: Conquer Austria, Pannonia and Lesser Poland by 1683
        if self.isPossibleUHV(Civ.OTTOMAN.value, 2, True):
            if self.checkProvincesStates(Civ.OTTOMAN.value, tOttomanControlII):
                self.wonUHV(Civ.OTTOMAN.value, 2)
        if iGameTurn == DateTurn.i1683AD:
            self.expireUHV(Civ.OTTOMAN.value, 2)

    def checkMoscow(self, iGameTurn):

        # UHV 1: Free Eastern Europe from the Mongols (Make sure there are no Mongol (or any other Barbarian) cities in Russia and Ukraine in 1482)
        if iGameTurn == DateTurn.i1482AD:
            if self.isPossibleUHV(Civ.MOSCOW.value, 0, True):
                bClean = True
                for iProv in tMoscowControl:
                    if civilizations().barbarian().unwrap().player.getProvinceCityCount(iProv) > 0:
                        bClean = False
                        break
                if bClean:
                    self.wonUHV(Civ.MOSCOW.value, 0)
                else:
                    self.lostUHV(Civ.MOSCOW.value, 0)

        # UHV 2: Control at least 25% of Europe
        if self.isPossibleUHV(Civ.MOSCOW.value, 1, True):
            totalLand = gc.getMap().getLandPlots()
            RussianLand = player(Civ.MOSCOW).getTotalLand()
            if totalLand > 0:
                landPercent = (RussianLand * 100.0) / totalLand
            else:
                landPercent = 0.0
            if landPercent >= 25:
                self.wonUHV(Civ.MOSCOW.value, 1)

        # UHV 3: Get into warm waters (Conquer Constantinople or control an Atlantic Access resource)
        if self.isPossibleUHV(Civ.MOSCOW.value, 2, True):
            if player(Civ.MOSCOW).countCultBorderBonuses(Bonus.ACCESS.value) > 0:
                self.wonUHV(Civ.MOSCOW.value, 2)
            elif (
                gc.getMap().plot(*CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM]).getPlotCity().getOwner()
                == Civ.MOSCOW.value
            ):
                self.wonUHV(Civ.MOSCOW.value, 2)

    def checkSweden(self, iGameTurn):

        # Old UHVs: Conquer Gotaland, Svealand, Norrland, Skaneland, Gotland and Osterland in 1600
        # 			Don't lose any cities to Poland, Lithuania or Russia before 1700
        # 			Have 15 cities in Saxony, Brandenburg, Holstein, Pomerania, Prussia, Greater Poland, Masovia, Suvalkija, Lithuania, Livonia, Estonia, Smolensk, Polotsk, Minsk, Murom, Chernigov, Moscow, Novgorod and Rostov in 1750

        # UHV 1: Have six cities in Norrland, Osterland and Karelia in 1323
        if iGameTurn == DateTurn.i1323AD:
            if self.isPossibleUHV(Civ.SWEDEN.value, 0, True):
                iNumCities = 0
                for iProv in tSwedenControl:
                    iNumCities += player(Civ.SWEDEN).getProvinceCityCount(iProv)
                if iNumCities >= 6:
                    self.wonUHV(Civ.SWEDEN.value, 0)
                else:
                    self.lostUHV(Civ.SWEDEN.value, 0)

        # UHV 2: Raze 5 Catholic cities while being Protestant by 1660
        # Controlled in the onCityRazed function
        elif iGameTurn == DateTurn.i1660AD:
            self.expireUHV(Civ.SWEDEN.value, 1)

        # UHV 3: Control every coastal city on the Baltic Sea in 1750
        elif iGameTurn == DateTurn.i1750AD:
            if self.isPossibleUHV(Civ.SWEDEN.value, 2, True):
                if up.getNumForeignCitiesOnBaltic(Civ.SWEDEN.value, True) > 0:
                    self.lostUHV(Civ.SWEDEN.value, 2)
                else:
                    self.wonUHV(Civ.SWEDEN.value, 2)

    def checkDutch(self, iGameTurn):

        # UHV 1: Settle 5 Great Merchants in Amsterdam by 1750
        if self.isPossibleUHV(Civ.DUTCH.value, 0, True):
            pPlot = gc.getMap().plot(*CIV_CAPITAL_LOCATIONS[Civ.DUTCH])
            if pPlot.isCity():
                city = pPlot.getPlotCity()
                if (
                    city.getFreeSpecialistCount(Specialist.GREAT_MERCHANT.value) >= 5
                    and city.getOwner() == Civ.DUTCH.value
                ):
                    self.wonUHV(Civ.DUTCH.value, 0)
        if iGameTurn == DateTurn.i1750AD:
            self.expireUHV(Civ.DUTCH.value, 0)

        # UHV 2: Build 3 Colonies and complete both Trading Companies
        # Controlled in the onProjectBuilt function

        # UHV 3: Become the richest country in Europe
        if self.isPossibleUHV(Civ.DUTCH.value, 2, True):
            iGold = player(Civ.DUTCH).getGold()
            bMost = True
            for iCiv in civilizations().majors().ids():
                if iCiv == Civ.DUTCH.value:
                    continue
                pPlayer = gc.getPlayer(iCiv)
                if pPlayer.isAlive():
                    if pPlayer.getGold() > iGold:
                        bMost = False
                        break
            if bMost:
                self.wonUHV(Civ.DUTCH.value, 2)

    def checkProvincesStates(self, iPlayer, tProvinces):
        pPlayer = gc.getPlayer(iPlayer)
        for iProv in tProvinces:
            if pPlayer.getProvinceCurrentState(iProv) < ProvinceStatus.CONQUER.value:
                return False
        return True

    def wonUHV(self, iCiv, iUHV):
        pCiv = gc.getPlayer(iCiv)
        pCiv.setUHV(iUHV, 1)
        pCiv.changeStabilityBase(StabilityCategory.EXPANSION.value, 3)
        if human() == iCiv:
            if iUHV == 0:
                sText = "first"
            elif iUHV == 1:
                sText = "second"
            elif iUHV == 2:
                sText = "third"
            popup = Popup.PyPopup()
            popup.setBodyString(localText.getText("TXT_KEY_VICTORY_UHV_GOAL_WON", (sText,)))
            popup.launch()

    def lostUHV(self, iCiv, iUHV):
        pCiv = gc.getPlayer(iCiv)
        pCiv.setUHV(iUHV, 0)
        if human() == iCiv:
            if iUHV == 0:
                sText = "first"
            elif iUHV == 1:
                sText = "second"
            elif iUHV == 2:
                sText = "third"
            popup = Popup.PyPopup()
            popup.setBodyString(localText.getText("TXT_KEY_VICTORY_UHV_GOAL_LOST", (sText,)))
            popup.launch()

    def setAllUHVFailed(self, iCiv):
        pPlayer = gc.getPlayer(iCiv)
        for i in range(3):
            pPlayer.setUHV(i, 0)

    def switchUHV(self, iNewCiv, iOldCiv):
        pPlayer = gc.getPlayer(iNewCiv)
        for i in range(3):
            pPlayer.setUHV(i, -1)
        if self.isIgnoreAI():
            self.setAllUHVFailed(iOldCiv)

    def isPossibleUHV(self, iCiv, iUHV, bAlreadyAIChecked):
        pCiv = gc.getPlayer(iCiv)
        if pCiv.getUHV(iUHV) != -1:
            return False
        if not pCiv.isAlive():
            return False

        if not bAlreadyAIChecked:
            if (
                iCiv != human() and self.isIgnoreAI()
            ):  # Skip calculations if no AI UHV option is enabled
                return False

        return True

    def expireUHV(self, iCiv, iUHV):
        # UHVs have to expire on the given deadline, even if the civ is not alive currently (would be an issue on respawns otherwise)
        # if self.isPossibleUHV(iCiv, iUHV, True):
        pCiv = gc.getPlayer(iCiv)
        if pCiv.getUHV(iUHV) == -1:
            self.lostUHV(iCiv, iUHV)

    def set1200UHVDone(self, iCiv):
        if iCiv == Civ.BYZANTIUM.value:
            player(Civ.BYZANTIUM).setUHV(0, 1)
        elif iCiv == Civ.FRANCE.value:
            player(Civ.FRANCE).setUHV(0, 1)
        elif iCiv == Civ.ARABIA.value:
            player(Civ.ARABIA).setUHV(0, 1)
        elif iCiv == Civ.BULGARIA.value:
            player(Civ.BULGARIA).setUHV(0, 1)
        elif iCiv == Civ.VENECIA.value:  # Venice gets conquerors near Constantinople for 2nd UHV
            player(Civ.VENECIA).setUHV(0, 1)
        elif iCiv == Civ.GERMANY.value:
            player(Civ.GERMANY).setUHV(0, 1)
        elif iCiv == Civ.NORWAY.value:
            player(Civ.NORWAY).setUHV(0, 1)
        elif iCiv == Civ.DENMARK.value:
            player(Civ.DENMARK).setUHV(0, 1)
        elif iCiv == Civ.SCOTLAND.value:
            player(Civ.SCOTLAND).setUHVCounter(1, 100)
