# Rhye's and Fall of Civilization: Europe - Religions management

from CvPythonExtensions import *
from CoreData import CIVILIZATIONS
from CoreFunctions import get_religion_by_id
from CoreTypes import Civ, City, Civic, StabilityCategory, Religion
from LocationsData import CITIES
from TimelineData import DateTurn
import PyHelpers
import Popup
import XMLConsts as xml
import RFCUtils
import RFCEMaps
from StoredData import sd

from MiscData import MessageData

# globals
gc = CyGlobalContext()
localText = CyTranslator()  # Absinthe
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()


# initialise coordinates
tToledo = (30, 27)
tAugsburg = (55, 41)
tSpainTL = (25, 20)
tSpainBR = (38, 34)
tMainzTL = (49, 41)
tMainzBR = (55, 52)
tPolandTL = (64, 43)
tPolandBR = (75, 54)

### Religious Buildings that give Faith Points ###
tCatholicBuildings = [xml.iCatholicTemple, xml.iCatholicMonastery, xml.iCatholicCathedral]
tOrthodoxBuildings = [xml.iOrthodoxTemple, xml.iOrthodoxMonastery, xml.iOrthodoxCathedral]
tProtestantBuildings = [xml.iProtestantTemple, xml.iProtestantSchool, xml.iProtestantCathedral]
tIslamicBuildings = [xml.iIslamicTemple, xml.iIslamicCathedral, xml.iIslamicMadrassa]
tReligiousWonders = [
    xml.iMonasteryOfCluny,
    xml.iWestminster,
    xml.iKrakDesChevaliers,
    xml.iNotreDame,
    xml.iPalaisPapes,
    xml.iStBasil,
    xml.iSophiaKiev,
    xml.iStCatherineMonastery,
    xml.iSistineChapel,
    xml.iJasnaGora,
    xml.iMontSaintMichel,
    xml.iBoyanaChurch,
    xml.iFlorenceDuomo,
    xml.iBorgundStaveChurch,
    xml.iDomeRock,
    xml.iThomaskirche,
    xml.iBlueMosque,
    xml.iSelimiyeMosque,
    xml.iMosqueOfKairouan,
    xml.iKoutoubiaMosque,
    xml.iLaMezquita,
    xml.iSanMarco,
    xml.iStephansdom,
    xml.iRoundChurch,
]


### Reformation Begin ###
# Matrix determines how likely the AI is to switch to Protestantism
lReformationMatrix = [
    20,  # Byzantium
    40,  # France
    40,  # Arabia
    20,  # Bulgaria
    40,  # Cordoba
    30,  # Venice
    50,  # Burgundy
    90,  # Germany
    30,  # Novgorod
    80,  # Norway
    30,  # Kiev
    50,  # Hungary
    10,  # Spain
    80,  # Denmark
    80,  # Scotland
    30,  # Poland
    20,  # Genoa
    40,  # Morocco
    80,  # England
    20,  # Portugal
    30,  # Aragon
    90,  # Sweden
    90,  # Prussia
    30,  # Lithuania
    20,  # Austria
    40,  # Turkey
    30,  # Moscow
    90,  # Dutch
    0,  # Rome
    40,  # Indies and Barbs
    40,
    40,
    40,
    40,
]

# Reformation neighbours spread reformation choice to each other
lReformationNeighbours = [
    [Civ.ARABIA.value, Civ.BULGARIA.value, Civ.OTTOMAN.value],  # Byzantium
    [
        Civ.BURGUNDY.value,
        Civ.CASTILLE.value,
        Civ.GERMANY.value,
        Civ.GENOA.value,
        Civ.ENGLAND.value,
        Civ.DUTCH.value,
        Civ.SCOTLAND.value,
    ],  # France
    [Civ.BYZANTIUM.value, Civ.CORDOBA.value, Civ.OTTOMAN.value],  # Arabia
    [Civ.BYZANTIUM.value, Civ.KIEV.value, Civ.HUNGARY.value, Civ.OTTOMAN.value],  # Bulgaria
    [
        Civ.ARABIA.value,
        Civ.CASTILLE.value,
        Civ.PORTUGAL.value,
        Civ.ARAGON.value,
        Civ.MOROCCO.value,
    ],  # Cordoba
    [
        Civ.GENOA.value,
        Civ.GERMANY.value,
        Civ.AUSTRIA.value,
        Civ.HUNGARY.value,
        Civ.POPE.value,
    ],  # Venice
    [Civ.FRANCE.value, Civ.GERMANY.value, Civ.GENOA.value, Civ.DUTCH.value],  # Burgundy
    [
        Civ.BURGUNDY.value,
        Civ.FRANCE.value,
        Civ.DENMARK.value,
        Civ.VENECIA.value,
        Civ.HUNGARY.value,
        Civ.POLAND.value,
        Civ.GENOA.value,
        Civ.AUSTRIA.value,
        Civ.DUTCH.value,
    ],  # Germany
    [
        Civ.SWEDEN.value,
        Civ.HUNGARY.value,
        Civ.POLAND.value,
        Civ.MOSCOW.value,
        Civ.LITHUANIA.value,
        Civ.KIEV.value,
    ],  # Novgorod
    [Civ.DENMARK.value, Civ.SWEDEN.value],  # Norway
    [
        Civ.BULGARIA.value,
        Civ.HUNGARY.value,
        Civ.POLAND.value,
        Civ.MOSCOW.value,
        Civ.LITHUANIA.value,
        Civ.NOVGOROD.value,
    ],  # Kiev
    [
        Civ.BULGARIA.value,
        Civ.VENECIA.value,
        Civ.KIEV.value,
        Civ.GERMANY.value,
        Civ.POLAND.value,
        Civ.AUSTRIA.value,
        Civ.OTTOMAN.value,
    ],  # Hungary
    [Civ.FRANCE.value, Civ.CORDOBA.value, Civ.PORTUGAL.value, Civ.ARAGON.value],  # Spain
    [Civ.NORWAY.value, Civ.SWEDEN.value, Civ.GERMANY.value],  # Denmark
    [Civ.FRANCE.value, Civ.DUTCH.value, Civ.ENGLAND.value],  # Scotland
    [
        Civ.KIEV.value,
        Civ.HUNGARY.value,
        Civ.GERMANY.value,
        Civ.MOSCOW.value,
        Civ.AUSTRIA.value,
        Civ.LITHUANIA.value,
    ],  # Poland
    [
        Civ.BURGUNDY.value,
        Civ.FRANCE.value,
        Civ.VENECIA.value,
        Civ.GERMANY.value,
        Civ.POPE.value,
        Civ.ARAGON.value,
    ],  # Genoa
    [
        Civ.ARABIA.value,
        Civ.CASTILLE.value,
        Civ.PORTUGAL.value,
        Civ.ARAGON.value,
        Civ.CORDOBA.value,
    ],  # Morocco
    [Civ.FRANCE.value, Civ.DUTCH.value, Civ.SCOTLAND.value],  # England
    [Civ.CASTILLE.value, Civ.CORDOBA.value, Civ.ARAGON.value],  # Portugal
    [
        Civ.CASTILLE.value,
        Civ.CORDOBA.value,
        Civ.PORTUGAL.value,
        Civ.FRANCE.value,
        Civ.GENOA.value,
    ],  # Aragon
    [Civ.NORWAY.value, Civ.DENMARK.value, Civ.MOSCOW.value, Civ.NOVGOROD.value],  # Sweden
    [
        Civ.GERMANY.value,
        Civ.LITHUANIA.value,
        Civ.MOSCOW.value,
        Civ.AUSTRIA.value,
        Civ.POLAND.value,
    ],  # Prussia
    [
        Civ.KIEV.value,
        Civ.MOSCOW.value,
        Civ.PRUSSIA.value,
        Civ.NOVGOROD.value,
        Civ.POLAND.value,
    ],  # Lithuania
    [Civ.VENECIA.value, Civ.HUNGARY.value, Civ.GERMANY.value, Civ.POLAND.value],  # Austria
    [Civ.BYZANTIUM.value, Civ.ARABIA.value, Civ.BULGARIA.value, Civ.HUNGARY.value],  # Turkey
    [
        Civ.KIEV.value,
        Civ.POLAND.value,
        Civ.SWEDEN.value,
        Civ.LITHUANIA.value,
        Civ.NOVGOROD.value,
    ],  # Moscow
    [
        Civ.BURGUNDY.value,
        Civ.FRANCE.value,
        Civ.GERMANY.value,
        Civ.ENGLAND.value,
        Civ.SCOTLAND.value,
    ],  # Dutch
    [Civ.VENECIA.value, Civ.GENOA.value],  # Pope
]
### Reformation End ###


### Regions to spread religion ###
tProvinceMap = RFCEMaps.tProvinceMap
tSpain = [
    xml.iP_Leon,
    xml.iP_GaliciaSpain,
    xml.iP_Aragon,
    xml.iP_Catalonia,
    xml.iP_Castile,
    xml.iP_LaMancha,
    xml.iP_Andalusia,
    xml.iP_Valencia,
]
tPoland = [
    xml.iP_GreaterPoland,
    xml.iP_LesserPoland,
    xml.iP_Masovia,
    xml.iP_Silesia,
    xml.iP_Suvalkija,
    xml.iP_Brest,
    xml.iP_Pomerania,
    xml.iP_GaliciaPoland,
]
tGermany = [xml.iP_Lorraine, xml.iP_Franconia, xml.iP_Bavaria, xml.iP_Swabia]
tWestAfrica = [xml.iP_Tetouan, xml.iP_Morocco, xml.iP_Marrakesh, xml.iP_Fez, xml.iP_Oran]
tNorthAfrica = [xml.iP_Algiers, xml.iP_Ifriqiya, xml.iP_Tripolitania, xml.iP_Cyrenaica]
tBalkansAndAnatolia = [
    xml.iP_Constantinople,
    xml.iP_Thrace,
    xml.iP_Opsikion,
    xml.iP_Paphlagonia,
    xml.iP_Thrakesion,
    xml.iP_Cilicia,
    xml.iP_Anatolikon,
    xml.iP_Armeniakon,
    xml.iP_Charsianon,
]
tCentralEurope = [
    xml.iP_GreaterPoland,
    xml.iP_LesserPoland,
    xml.iP_Masovia,
    xml.iP_GaliciaPoland,
    xml.iP_Brest,
    xml.iP_Suvalkija,
    xml.iP_Lithuania,
    xml.iP_Prussia,
    xml.iP_Pomerania,
    xml.iP_Saxony,
    xml.iP_Brandenburg,
    xml.iP_Holstein,
    xml.iP_Denmark,
    xml.iP_Bavaria,
    xml.iP_Swabia,
    xml.iP_Bohemia,
    xml.iP_Moravia,
    xml.iP_Silesia,
    xml.iP_Hungary,
    xml.iP_Transylvania,
    xml.iP_UpperHungary,
    xml.iP_Pannonia,
    xml.iP_Slavonia,
    xml.iP_Carinthia,
    xml.iP_Austria,
]
tMaghrebAndalusia = [
    xml.iP_Tetouan,
    xml.iP_Morocco,
    xml.iP_Marrakesh,
    xml.iP_Fez,
    xml.iP_Oran,
    xml.iP_Algiers,
    xml.iP_Ifriqiya,
    xml.iP_Tripolitania,
    xml.iP_Cyrenaica,
    xml.iP_LaMancha,
    xml.iP_Andalusia,
    xml.iP_Valencia,
]
tBulgariaBalkans = [xml.iP_Moesia, xml.iP_Macedonia, xml.iP_Serbia, xml.iP_Wallachia]
tOldRus = [
    xml.iP_Novgorod,
    xml.iP_Rostov,
    xml.iP_Polotsk,
    xml.iP_Smolensk,
    xml.iP_Minsk,
    xml.iP_Chernigov,
    xml.iP_Kiev,
    xml.iP_Pereyaslavl,
    xml.iP_Sloboda,
]
tSouthScandinavia = [
    xml.iP_Denmark,
    xml.iP_Gotaland,
    xml.iP_Skaneland,
    xml.iP_Vestfold,
    xml.iP_Norway,
]
tHungary = [xml.iP_Hungary, xml.iP_Transylvania, xml.iP_UpperHungary, xml.iP_Pannonia]


class Religions:

    ##################################################
    ### Secure storage & retrieval of script data ###
    ################################################

    def getSeed(self):
        return sd.scriptDict["iSeed"]

    def setSeed(self):
        sd.scriptDict["iSeed"] = gc.getGame().getSorenRandNum(100, "Seed for random delay")

    def getReformationActive(self):
        return sd.scriptDict["bReformationActive"]

    def setReformationActive(self, bNewValue):
        sd.scriptDict["bReformationActive"] = bNewValue

    def getReformationHitMatrix(self, iCiv):
        return sd.scriptDict["lReformationHitMatrix"][iCiv]

    def setReformationHitMatrix(self, iCiv, bNewValue):
        sd.scriptDict["lReformationHitMatrix"][iCiv] = bNewValue

    def getReformationHitMatrixAll(self):
        return sd.scriptDict["lReformationHitMatrix"]

    def getCounterReformationActive(self):
        return sd.scriptDict["bCounterReformationActive"]

    def setCounterReformationActive(self, bNewValue):
        sd.scriptDict["bCounterReformationActive"] = bNewValue

    #######################################
    ### Main methods (Event-Triggered) ###
    #####################################

    def setup(self):
        gc.getPlayer(Civ.BYZANTIUM.value).changeFaith(10)
        gc.getPlayer(Civ.OTTOMAN.value).changeFaith(20)
        self.setSeed()

    def checkTurn(self, iGameTurn):
        # Absinthe: Spreading religion in a couple preset dates
        if iGameTurn == DateTurn.i700AD - 2:
            # Spread Judaism to Toledo
            self.spreadReligion(tToledo, Religion.JUDAISM.value)
            # Spread Islam to a random city in Africa
            tCity = self.selectRandomCityRegion(tNorthAfrica, Religion.ISLAM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.ISLAM.value)
        elif iGameTurn == DateTurn.i700AD + 2:
            # Spread Judaism and Islam to a random city in Africa
            tCity = self.selectRandomCityRegion(tWestAfrica, Religion.ISLAM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.ISLAM.value)
            tCity = self.selectRandomCityRegion(tWestAfrica, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
        elif iGameTurn == DateTurn.i900AD:
            # Spread Judaism to another city in Spain
            tCity = self.selectRandomCityRegion(tSpain, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
        elif iGameTurn == DateTurn.i1000AD:
            # Spread Judaism to a city in France/Germany
            tCity = self.selectRandomCityRegion(tGermany, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
            # Spread Islam to another city in Africa
            tCity = self.selectRandomCityRegion(tNorthAfrica, Religion.ISLAM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.ISLAM.value)
        elif iGameTurn == DateTurn.i1101AD:
            # Spread Judaism to a couple towns in Poland
            tCity = self.selectRandomCityRegion(tPoland, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
        elif iGameTurn == DateTurn.i1200AD:
            # Spread Judaism to a couple towns in Poland
            tCity = self.selectRandomCityRegion(tPoland, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
        elif DateTurn.i1299AD < iGameTurn < DateTurn.i1350AD and iGameTurn % 3 == 0:
            # Spread Islam to a couple cities in Anatolia before the Ottoman spawn
            tCity = self.selectRandomCityRegion(tBalkansAndAnatolia, Religion.ISLAM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.ISLAM.value)
        elif iGameTurn == DateTurn.i1401AD:
            # Spread Judaism to a couple towns in Poland
            tCity = self.selectRandomCityRegion(tPoland, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)

        # Absinthe: Spreading Judaism in random dates
        # General 6% chance to spread Jews to a random city in every third turn
        if DateTurn.i800AD < iGameTurn < DateTurn.i1700AD and iGameTurn % 3 == 0:
            if gc.getGame().getSorenRandNum(100, "Spread Jews") < 6:
                tCity = self.selectRandomCityAll()
                if tCity:
                    self.spreadReligion(tCity, Religion.JUDAISM.value)

        # Additional 11% chance to spread Jews to a random Central European city in every third turn
        if DateTurn.i1000AD < iGameTurn < DateTurn.i1500AD and iGameTurn % 3 == 1:
            if gc.getGame().getSorenRandNum(100, "Spread Jews") < 11:
                tCity = self.selectRandomCityRegion(tCentralEurope, Religion.JUDAISM.value)
                if tCity:
                    self.spreadReligion(tCity, Religion.JUDAISM.value)

        # Absinthe: Encouraging desired religion spread in a couple areas (mostly for Islam and Orthodoxy)
        # Maghreb and Cordoba:
        if DateTurn.i700AD < iGameTurn < DateTurn.i800AD and iGameTurn % 2 == 1:
            if gc.getGame().getSorenRandNum(100, "Spread chance") < 32:
                tCity = self.selectRandomCityRegion(tMaghrebAndalusia, Religion.ISLAM.value, True)
                if tCity:
                    self.spreadReligion(tCity, Religion.ISLAM.value)
        if DateTurn.i800AD < iGameTurn < DateTurn.i1200AD and iGameTurn % 3 == 2:
            if gc.getGame().getSorenRandNum(100, "Spread chance") < 28:
                tCity = self.selectRandomCityRegion(tMaghrebAndalusia, Religion.ISLAM.value, True)
                if tCity:
                    self.spreadReligion(tCity, Religion.ISLAM.value)

        # Bulgaria and Balkans:
        if DateTurn.i700AD < iGameTurn < DateTurn.i800AD and iGameTurn % 3 == 1:
            if gc.getGame().getSorenRandNum(100, "Spread chance") < 25:
                tCity = self.selectRandomCityRegion(
                    tBulgariaBalkans, Religion.ORTHODOXY.value, True
                )
                if tCity:
                    self.spreadReligion(tCity, Religion.ORTHODOXY.value)
        if DateTurn.i800AD < iGameTurn < DateTurn.i1000AD and iGameTurn % 4 == 1:
            if gc.getGame().getSorenRandNum(100, "Spread chance") < 15:
                tCity = self.selectRandomCityRegion(
                    tBulgariaBalkans, Religion.ORTHODOXY.value, True
                )
                if tCity:
                    self.spreadReligion(tCity, Religion.ORTHODOXY.value)
        # Old Rus territories:
        if DateTurn.i852AD < iGameTurn < DateTurn.i1300AD and iGameTurn % 4 == 3:
            if gc.getGame().getSorenRandNum(100, "Spread chance") < 25:
                tCity = self.selectRandomCityRegion(tOldRus, Religion.ORTHODOXY.value, True)
                if tCity:
                    self.spreadReligion(tCity, Religion.ORTHODOXY.value)

        # Extra chance for early Orthodoxy spread in Novgorod:
        if DateTurn.i852AD < iGameTurn < DateTurn.i960AD and iGameTurn % 5 == 2:
            if gc.getGame().getSorenRandNum(100, "Spread chance") < 34:
                tCity = self.selectRandomCityRegion(
                    [xml.iP_Novgorod, xml.iP_Polotsk, xml.iP_Smolensk],
                    Religion.ORTHODOXY.value,
                    True,
                )
                if tCity:
                    self.spreadReligion(tCity, Religion.ORTHODOXY.value)
        # Hungary:
        if DateTurn.i960AD < iGameTurn < DateTurn.i1200AD and iGameTurn % 4 == 2:
            if gc.getGame().getSorenRandNum(100, "Spread chance") < 21:
                tCity = self.selectRandomCityRegion(tHungary, Religion.CATHOLICISM.value, True)
                if tCity:
                    self.spreadReligion(tCity, Religion.CATHOLICISM.value)

        # Scandinavia:
        if DateTurn.i1000AD < iGameTurn < DateTurn.i1300AD and iGameTurn % 4 == 0:
            if gc.getGame().getSorenRandNum(100, "Spread chance") < 24:
                tCity = self.selectRandomCityRegion(
                    tSouthScandinavia, Religion.CATHOLICISM.value, True
                )
                if tCity:
                    self.spreadReligion(tCity, Religion.CATHOLICISM.value)

        # Absinthe: Persecution cooldown
        for i in CIVILIZATIONS.majors().ids():
            pPlayer = gc.getPlayer(i)
            if pPlayer.getProsecutionCount() > 0:
                pPlayer.changeProsecutionCount(-1)
            # Religious Law means a bigger decrease in persecution points
            if pPlayer.getCivics(1) == Civic.RELIGIOUS_LAW.value:
                if pPlayer.getProsecutionCount() > 0:
                    pPlayer.changeProsecutionCount(-1)

        # Absinthe: Resettle Jewish refugees
        iRefugies = gc.getMinorReligionRefugies()
        for i in range(iRefugies):
            self.resettleRefugies()
        gc.setMinorReligionRefugies(0)

        # Absinthe: Benefits for Catholics from the Pope
        lCatholicCivs = self.getCatholicCivs(
            True
        )  # all Catholic civs with open borders with the Pope
        pPope = gc.getPlayer(Civ.POPE.value)
        teamPope = gc.getTeam(pPope.getTeam())
        # Gold gift
        if iGameTurn >= DateTurn.i752AD:
            if iGameTurn > DateTurn.i1648AD:  # End of religious wars
                iDivBy = 14
            elif iGameTurn > DateTurn.i1517AD:  # Protestantism
                iDivBy = 11
            elif iGameTurn > DateTurn.i1053AD:  # Schism
                iDivBy = 6
            else:
                iDivBy = 9
            if iGameTurn % iDivBy == 3:
                iPopeGold = pPope.getGold()
                if iPopeGold > 100:
                    if (
                        gc.getGame().getSorenRandNum(10, "Random entry") != 0
                    ):  # 10% chance for not giving anything
                        lWeightValues = []
                        for iPlayer in lCatholicCivs:
                            iCatholicFaith = 0
                            pPlayer = gc.getPlayer(iPlayer)
                            # Relations with the Pope are much more important here
                            iCatholicFaith += pPlayer.getFaith()
                            iCatholicFaith += 8 * max(0, pPope.AI_getAttitude(iPlayer))
                            if iCatholicFaith > 0:
                                lWeightValues.append((iPlayer, iCatholicFaith))
                        iChosenPlayer = utils.getRandomByWeight(lWeightValues)
                        if iChosenPlayer != -1:
                            pPlayer = gc.getPlayer(iChosenPlayer)
                            if iGameTurn < 100:
                                iGift = min(
                                    iPopeGold / 5, 40
                                )  # between 20-40, based on the Pope's wealth
                            else:
                                iGift = min(
                                    iPopeGold / 2, 80
                                )  # between 50-80, based on the Pope's wealth
                            pPope.changeGold(-iGift)
                            pPlayer.changeGold(iGift)
                            if iChosenPlayer == utils.getHumanID():
                                sText = CyTranslator().getText("TXT_KEY_FAITH_GOLD_GIFT", (iGift,))
                                CyInterface().addMessage(
                                    iPlayer,
                                    False,
                                    MessageData.DURATION,
                                    sText,
                                    "",
                                    0,
                                    "",
                                    ColorTypes(MessageData.BLUE),
                                    -1,
                                    -1,
                                    True,
                                    True,
                                )
        # Free religious building
        if iGameTurn > DateTurn.i800AD:  # The crowning of Charlemagne
            if iGameTurn > DateTurn.i1648AD:  # End of religious wars
                iDivBy = 21
            elif iGameTurn > DateTurn.i1517AD:  # Protestantism
                iDivBy = 14
            elif iGameTurn > DateTurn.i1053AD:  # Schism
                iDivBy = 8
            else:
                iDivBy = 11
            if iGameTurn % iDivBy == 2:
                if (
                    gc.getGame().getSorenRandNum(5, "Random entry") != 0
                ):  # there is 20% chance for not building anything
                    lWeightValues = []
                    iJerusalemOwner = (
                        gc.getMap()
                        .plot(*CITIES[City.JERUSALEM].to_tuple())
                        .getPlotCity()
                        .getOwner()
                    )
                    for iPlayer in lCatholicCivs:
                        iCatholicFaith = 0
                        pPlayer = gc.getPlayer(iPlayer)
                        # Faith points are the deciding factor for buildings
                        iCatholicFaith += pPlayer.getFaith()
                        iCatholicFaith += 2 * max(0, pPope.AI_getAttitude(iPlayer))
                        if (
                            iPlayer == iJerusalemOwner
                        ):  # The Catholic owner of Jerusalem has a greatly improved chance
                            iCatholicFaith += 30
                        if iCatholicFaith > 0:
                            lWeightValues.append((iPlayer, iCatholicFaith))
                    iChosenPlayer = utils.getRandomByWeight(lWeightValues)
                    if iChosenPlayer != -1:
                        pPlayer = gc.getPlayer(iChosenPlayer)
                        iCatholicBuilding = xml.iCatholicTemple
                        # No chance for monastery if the selected player knows the Scientific Method tech (which obsoletes monasteries), otherwise 50-50% for temple and monastery
                        teamPlayer = gc.getTeam(pPlayer.getTeam())
                        if (
                            not teamPlayer.isHasTech(xml.iScientificMethod)
                            and gc.getGame().getSorenRandNum(2, "random Catholic BuildingType")
                            == 0
                        ):
                            iCatholicBuilding = xml.iCatholicMonastery
                        self.buildInRandomCity(
                            iChosenPlayer, iCatholicBuilding, Religion.CATHOLICISM.value
                        )
        # Free technology
        if (
            iGameTurn > DateTurn.i843AD
        ):  # Treaty of Verdun, the Carolingian Empire divided into 3 parts
            if (
                iGameTurn % 13 == 4
            ):  # checked every 13th turn - won't change it as the game progresses, as the number of available techs will already change with the number of Catholic civs
                lWeightValues = []
                for iPlayer in lCatholicCivs:
                    iCatholicFaith = 0
                    pPlayer = gc.getPlayer(iPlayer)
                    # Faith points are the deciding factor for techs
                    iCatholicFaith += pPlayer.getFaith()
                    iCatholicFaith += 2 * max(0, pPope.AI_getAttitude(iPlayer))
                    if iCatholicFaith > 0:
                        lWeightValues.append((iPlayer, iCatholicFaith))
                iChosenPlayer = utils.getRandomByWeight(
                    lWeightValues
                )  # 100% chance to choose a civ, as this doesn't guarantee that there will be a given tech at all
                if iChosenPlayer != -1:
                    pPlayer = gc.getPlayer(iChosenPlayer)
                    teamPlayer = gc.getTeam(pPlayer.getTeam())
                    # look for techs which are known by the Pope but unknown to the chosen civ
                    for iTech in range(xml.iNumTechs):
                        if teamPope.isHasTech(iTech):
                            if not teamPlayer.isHasTech(iTech):
                                # chance for actually giving this tech, based on faith points
                                iRandomTechNum = gc.getGame().getSorenRandNum(
                                    70, "Pope random tech chance"
                                )
                                if (
                                    pPlayer.getFaith() + 20 > iRandomTechNum
                                ):  # +20, to have a real chance with low faith points as well
                                    teamPlayer.setHasTech(iTech, True, iChosenPlayer, False, True)
                                    if iChosenPlayer == utils.getHumanID():
                                        sText = CyTranslator().getText(
                                            "TXT_KEY_FAITH_TECH_GIFT",
                                            (gc.getTechInfo(iTech).getDescription(),),
                                        )
                                        CyInterface().addMessage(
                                            iChosenPlayer,
                                            True,
                                            MessageData.DURATION,
                                            sText,
                                            "",
                                            0,
                                            "",
                                            ColorTypes(MessageData.BLUE),
                                            -1,
                                            -1,
                                            True,
                                            True,
                                        )
                                    # don't continue if a tech was already given - this also means that there is bigger chance for getting a tech if the chosen civ is multiple techs behind
                                    break

        # Absinthe: Pope gets all techs known by at least 3 Catholic civs
        if iGameTurn % 6 == 3:
            lCatholicCivs = self.getCatholicCivs(
                False
            )  # all Catholic civs, open borders with the Pope doesn't matter here
            pPope = gc.getPlayer(Civ.POPE.value)
            teamPope = gc.getTeam(pPope.getTeam())
            for iTech in range(xml.iNumTechs):
                if not teamPope.isHasTech(iTech):
                    iTechCounter = 0
                    for iPlayer in lCatholicCivs:
                        pPlayer = gc.getPlayer(iPlayer)
                        teamPlayer = gc.getTeam(pPlayer.getTeam())
                        if teamPlayer.isHasTech(iTech):
                            iTechCounter += 1
                            if iTechCounter >= 3:
                                teamPope.setHasTech(iTech, True, Civ.POPE.value, False, True)
                                break

        # Absinthe: Reformation
        if self.getCounterReformationActive():
            self.doCounterReformation()
        if self.getReformationActive():
            self.reformationArrayChoice()
            if self.getReformationActive():
                self.reformationArrayChoice()
                if self.getReformationActive():
                    self.reformationArrayChoice()

    def onReligionSpread(self, iReligion, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        if pPlayer.getStateReligion() == iReligion:
            pPlayer.changeFaith(1)
        else:
            pPlayer.changeFaith(-1)

    def onBuildingBuilt(seld, iPlayer, iBuilding):
        pPlayer = gc.getPlayer(iPlayer)
        iStateReligion = pPlayer.getStateReligion()
        if iStateReligion != -1:
            if iStateReligion == Religion.CATHOLICISM.value and iBuilding in tCatholicBuildings:
                pPlayer.changeFaith(1)
                if iBuilding == xml.iCatholicCathedral:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(xml.iPalaisPapes) > 0:
                    pPlayer.changeFaith(1)
            elif iStateReligion == Religion.ORTHODOXY.value and iBuilding in tOrthodoxBuildings:
                pPlayer.changeFaith(1)
                if iBuilding == xml.iOrthodoxCathedral:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(xml.iPalaisPapes) > 0:
                    pPlayer.changeFaith(1)
            elif iStateReligion == Religion.ISLAM.value and iBuilding in tIslamicBuildings:
                pPlayer.changeFaith(1)
                if iBuilding == xml.iIslamicCathedral:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(xml.iPalaisPapes) > 0:
                    pPlayer.changeFaith(1)
            elif (
                iStateReligion == Religion.PROTESTANTISM.value
                and iBuilding in tProtestantBuildings
            ):
                pPlayer.changeFaith(1)
                if iBuilding == xml.iProtestantCathedral:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(xml.iPalaisPapes) > 0:
                    pPlayer.changeFaith(1)
            elif iStateReligion == Religion.JUDAISM.value and iBuilding in [
                xml.iJewishQuarter,
                xml.iKazimierz,
            ]:
                pPlayer.changeFaith(1)
                if iBuilding == xml.iKazimierz:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(xml.iPalaisPapes) > 0:
                    pPlayer.changeFaith(1)
            # Absinthe: Wonders: Mont Saint-Michel wonder effect
            if utils.getBaseBuilding(iBuilding) in [xml.iWalls, xml.iCastle]:
                if pPlayer.countNumBuildings(xml.iMontSaintMichel) > 0:
                    pPlayer.changeFaith(1)
        if iBuilding in tReligiousWonders:
            pPlayer.changeFaith(4)
            if pPlayer.countNumBuildings(xml.iPalaisPapes) > 0:
                pPlayer.changeFaith(1)
        if iStateReligion != Religion.JUDAISM.value and iBuilding == xml.iKazimierz:
            pPlayer.changeFaith(-min(1, pPlayer.getFaith()))
            # Kazimierz tries to spread Judaism to a couple new cities
            cityList = utils.getCityList(iPlayer)
            iJewCityNum = max(
                (len(cityList) + 2) / 3 + 1, 3
            )  # number of tries are based on number of cities, but at least 3
            for i in range(iJewCityNum):
                city = utils.getRandomEntry(cityList)
                if not city.isHasReligion(Religion.JUDAISM.value):
                    city.setHasReligion(Religion.JUDAISM.value, True, True, False)
            # Adds Jewish Quarter to all cities which already has Judaism (including the ones where it just spread)
            for city in cityList:
                if city.isHasReligion(Religion.JUDAISM.value):
                    city.setHasRealBuilding(xml.iJewishQuarter, True)

    def selectRandomCityAll(self):
        "selects a random city from the whole map"
        cityList = []
        for iPlayer in CIVILIZATIONS.ids():
            cityList.extend(utils.getCityList(iPlayer))
        if cityList:
            city = utils.getRandomEntry(cityList)
            return (city.getX(), city.getY())
        return False

    def selectRandomCityCiv(self, iCiv):
        "selects a random city from a given civ"
        if gc.getPlayer(iCiv).isAlive():
            cityList = utils.getCityList(iCiv)
            if cityList:
                city = utils.getRandomEntry(cityList)
                return (city.getX(), city.getY())
        return False

    def selectRandomCityProvince(self, tProvinces):  # currently unused
        "selects a random city in a given province/region"
        cityList = []
        for iPlayer in CIVILIZATIONS.ids():
            if not gc.getPlayer(iPlayer).isAlive():
                continue
            for city in utils.getCityList(iPlayer):
                if tProvinceMap[city.getY()][city.getX()] in tProvinces:
                    cityList.append(city)
        if cityList:
            city = utils.getRandomEntry(cityList)
            return (city.getX(), city.getY())
        return False

    def selectRandomCityProvinceCiv(self, tProvinces, iCiv):  # currently unused
        "selects a random city from a given civ in a given province/region"
        if gc.getPlayer(iCiv).isAlive():
            cityList = []
            for city in utils.getCityList(iCiv):
                if tProvinceMap[city.getY()][city.getX()] in tProvinces:
                    cityList.append(city)
            if cityList:
                city = utils.getRandomEntry(cityList)
                return (city.getX(), city.getY())
        return False

    def selectRandomCityArea(self, tTopLeft, tBottomRight):  # currently unused
        "selects a random city in the tTopLeft tBottomRight rectangle"
        cityList = []
        for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
            pCurrent = gc.getMap().plot(x, y)
            if pCurrent.isCity():
                for iPlayer in CIVILIZATIONS.ids():
                    if not gc.getPlayer(iPlayer).isAlive():
                        continue
                    if pCurrent.getPlotCity().getOwner() == iPlayer:
                        cityList.append(pCurrent.getPlotCity())
        if cityList:
            city = utils.getRandomEntry(cityList)
            return (city.getX(), city.getY())
        return False

    def selectRandomCityAreaCiv(self, tTopLeft, tBottomRight, iCiv):  # currently unused
        "selects a random city from a given civ in the tTopLeft tBottomRight rectangle"
        if gc.getPlayer(iCiv).isAlive():
            cityList = []
            for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
                pCurrent = gc.getMap().plot(x, y)
                if pCurrent.isCity():
                    if pCurrent.getPlotCity().getOwner() == iCiv:
                        cityList.append(pCurrent.getPlotCity())
            if cityList:
                city = utils.getRandomEntry(cityList)
                return (city.getX(), city.getY())
        return False

    def selectRandomCityReligion(self, iReligion):  # currently unused
        "selects a random city with a given religion"
        if gc.getGame().isReligionFounded(iReligion):
            cityList = []
            for iPlayer in CIVILIZATIONS.majors().ids():
                if not gc.getPlayer(iPlayer).isAlive():
                    continue
                for city in utils.getCityList(iPlayer):
                    if city.isHasReligion(iReligion):
                        cityList.append(city)
            if cityList:
                city = utils.getRandomEntry(cityList)
                return (city.getX(), city.getY())
        return False

    def selectRandomCityReligionCiv(self, iReligion, iCiv):  # currently unused
        "selects a random city from a given civ with a given religion"
        if gc.getGame().isReligionFounded(iReligion):
            if gc.getPlayer(iCiv).isAlive():
                cityList = []
                for city in utils.getCityList(iCiv):
                    if city.isHasReligion(iReligion):
                        cityList.append(city)
                if cityList:
                    city = utils.getRandomEntry(cityList)
                    return (city.getX(), city.getY())
        return False

    def selectRandomCityRegion(self, tProvinces, iReligionToSpread, bNoSpreadWithReligion=False):
        cityList = []
        for iPlayer in CIVILIZATIONS.ids():
            if not gc.getPlayer(iPlayer).isAlive():
                continue
            for city in utils.getCityList(iPlayer):
                if tProvinceMap[city.getY()][city.getX()] in tProvinces:
                    # do not try to spread to cities which already have the desired religion
                    if not city.isHasReligion(iReligionToSpread):
                        if bNoSpreadWithReligion:
                            # check if there is any religion already present in the city
                            bAlreadyHasReligion = False
                            for iReligion in range(len(Religion)):
                                if city.isHasReligion(iReligion):
                                    bAlreadyHasReligion = True
                                    break
                            if not bAlreadyHasReligion:
                                cityList.append(city)
                        else:
                            cityList.append(city)
        if cityList:
            city = utils.getRandomEntry(cityList)
            return (city.getX(), city.getY())
        return False

    def spreadReligion(self, tPlot, iReligion):
        x, y = tPlot
        pPlot = gc.getMap().plot(x, y)
        if pPlot.isCity():
            pPlot.getPlotCity().setHasReligion(
                iReligion, True, True, False
            )  # Absinthe: puts the given religion into this city, with interface message

    def buildInRandomCity(self, iPlayer, iBuilding, iReligion):
        cityList = []
        for city in utils.getCityList(iPlayer):
            if not city.hasBuilding(iBuilding) and city.isHasReligion(iReligion):
                cityList.append(city)
        if cityList:
            city = utils.getRandomEntry(cityList)
            city.setHasRealBuilding(iBuilding, True)
            gc.getPlayer(iPlayer).changeFaith(1)
            if utils.getHumanID() == iPlayer:
                sText = (
                    CyTranslator().getText("TXT_KEY_FAITH_BUILDING1", ())
                    + " "
                    + gc.getBuildingInfo(iBuilding).getDescription()
                    + " "
                    + CyTranslator().getText("TXT_KEY_FAITH_BUILDING2", ())
                    + " "
                    + city.getName()
                )
                CyInterface().addMessage(
                    iPlayer,
                    False,
                    MessageData.DURATION,
                    sText,
                    "",
                    0,
                    gc.getBuildingInfo(iBuilding).getButton(),
                    ColorTypes(MessageData.BLUE),
                    city.getX(),
                    city.getY(),
                    True,
                    True,
                )

    # Absinthe: free religious revolution
    def onPlayerChangeAllCivics(self, iPlayer, lNewCivics, lOldCivics):
        # free religion change when switching away from Paganism
        if lOldCivics[4] == Civic.PAGANISM.value:
            if lNewCivics[4] in [
                Civic.STATE_RELIGION.value,
                Civic.THEOCRACY.value,
                Civic.ORGANIZED_RELIGION.value,
            ]:
                if iPlayer == utils.getHumanID():
                    # check the available religions
                    religionList = []
                    for city in utils.getCityList(iPlayer):
                        for iReligion in range(gc.getNumReligionInfos()):
                            if iReligion not in religionList:
                                if city.isHasReligion(iReligion):
                                    religionList.append(iReligion)
                                    if (
                                        len(religionList) == gc.getNumReligionInfos()
                                    ):  # no need to check any further, if we already have all religions in the list
                                        break
                        if (
                            len(religionList) == gc.getNumReligionInfos()
                        ):  # no need to check any further, if we already have all religions in the list
                            break
                    self.setFreeRevolutionReligions(religionList)
                    # no popup if no available religions
                    if religionList:
                        self.showFreeRevolutionPopup(iPlayer, religionList)
                elif iPlayer < CIVILIZATIONS.main().len():
                    iBestReligionPoint = 0
                    iBestReligion = Religion.CATHOLICISM.value
                    # loop through all religions
                    for iReligion in range(gc.getNumReligionInfos()):
                        iReligionPoint = 0
                        # check cities for religions and holy cities
                        for city in utils.getCityList(iPlayer):
                            if city.isHasReligion(iReligion):
                                iReligionPoint += 10
                            if city.isHolyCityByType(iReligion):
                                iReligionPoint += 1000
                        spread_factor = CIVILIZATIONS[iPlayer].religion.spreading_threshold[
                            get_religion_by_id(iReligion)
                        ]
                        if spread_factor < 60:
                            iReligionPoint = (iReligionPoint * 5) / 10
                        elif spread_factor < 100:
                            iReligionPoint = (iReligionPoint * 8) / 10
                        elif spread_factor > 200:
                            iReligionPoint = (iReligionPoint * 12) / 10
                        # update if better
                        if iReligionPoint > iBestReligionPoint:
                            iBestReligionPoint = iReligionPoint
                            iBestReligion = iReligion
                    # convert to the best religion
                    pPlayer = gc.getPlayer(iPlayer)
                    pPlayer.convertForFree(iBestReligion)

    def getFreeRevolutionReligions(self):
        return sd.scriptDict["lReligionChoices"]

    def setFreeRevolutionReligions(self, val):
        sd.scriptDict["lReligionChoices"] = val

    # Absinthe: free religion change popup
    def showFreeRevolutionPopup(self, iPlayer, religionList):
        """Possibility for the human player to select a religion anarchy-free."""
        popup = Popup.PyPopup(7629, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setHeaderString("Religious Revolution")
        popup.setBodyString("Choose the religion you want to adopt as your State Religion:")
        for iReligion in religionList:
            strIcon = gc.getReligionInfo(iReligion).getType()
            strIcon = "[%s]" % (strIcon.replace("RELIGION_", "ICON_"))
            strButtonText = "%s %s" % (
                localText.getText(strIcon, ()),
                gc.getReligionInfo(iReligion).getText(),
            )
            popup.addButton(strButtonText)
        popup.addButton("We don't want to adopt a State Religion right now")
        popup.launch(False)

    # Absinthe: event of the free religion change popup
    def eventApply7629(self, playerID, popupReturn):
        """Free religious revolution."""
        iDecision = popupReturn.getButtonClicked()
        religionList = self.getFreeRevolutionReligions()
        # the last option is the no change option
        pPlayer = gc.getPlayer(playerID)
        pPlayer.convertForFree(religionList[popupReturn.getButtonClicked()])

    ##REFORMATION

    def showPopup(self, popupID, title, message, labels):
        popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setHeaderString(title)
        popup.setBodyString(message)
        for i in labels:
            popup.addButton(i)
        popup.launch(False)

    def reformationPopup(self):
        self.showPopup(
            7624,
            CyTranslator().getText("TXT_KEY_REFORMATION_TITLE", ()),
            CyTranslator().getText("TXT_KEY_REFORMATION_MESSAGE", ()),
            (
                CyTranslator().getText("TXT_KEY_POPUP_YES", ()),
                CyTranslator().getText("TXT_KEY_POPUP_NO", ()),
            ),
        )

    def eventApply7624(self, popupReturn):
        iHuman = utils.getHumanID()
        if popupReturn.getButtonClicked() == 0:
            self.reformationyes(iHuman)
        elif popupReturn.getButtonClicked() == 1:
            self.reformationno(iHuman)

    def onTechAcquired(self, iTech, iPlayer):
        if iTech == xml.iPrintingPress:
            if gc.getPlayer(iPlayer).getStateReligion() == Religion.CATHOLICISM.value:
                if not gc.getGame().isReligionFounded(Religion.PROTESTANTISM.value):
                    gc.getPlayer(iPlayer).foundReligion(
                        Religion.PROTESTANTISM.value, Religion.PROTESTANTISM.value, False
                    )
                    gc.getGame().getHolyCity(Religion.PROTESTANTISM.value).setNumRealBuilding(
                        xml.iProtestantShrine, 1
                    )
                    self.setReformationActive(True)
                    self.reformationchoice(iPlayer)
                    self.reformationOther(Civ.INDEPENDENT.value)
                    self.reformationOther(Civ.INDEPENDENT_2.value)
                    self.reformationOther(Civ.INDEPENDENT_3.value)
                    self.reformationOther(Civ.INDEPENDENT_4.value)
                    self.reformationOther(Civ.BARBARIAN.value)
                    self.setReformationHitMatrix(iPlayer, 2)
                    for iCiv in CIVILIZATIONS.majors().ids():
                        if (
                            iCiv in lReformationNeighbours[iPlayer]
                        ) and self.getReformationHitMatrix(iCiv) == 0:
                            self.setReformationHitMatrix(iCiv, 1)

    def reformationArrayChoice(self):
        lCivs = [
            iCiv
            for iCiv in CIVILIZATIONS.majors().ids()
            if self.getReformationHitMatrix(iCiv) == 1
        ]
        iCiv = utils.getRandomEntry(lCivs)
        pPlayer = gc.getPlayer(iCiv)
        if pPlayer.isAlive() and pPlayer.getStateReligion() == Religion.CATHOLICISM.value:
            self.reformationchoice(iCiv)
        else:
            self.reformationOther(iCiv)
        self.setReformationHitMatrix(iCiv, 2)
        for iNextCiv in CIVILIZATIONS.majors().ids():
            if (
                iNextCiv in lReformationNeighbours[iCiv]
                and self.getReformationHitMatrix(iNextCiv) == 0
            ):
                self.setReformationHitMatrix(iNextCiv, 1)
        if sum(self.getReformationHitMatrixAll()) == 2 * CIVILIZATIONS.majors().len():
            self.setReformationActive(False)
            self.setCounterReformationActive(
                True
            )  # after all players have been hit by the Reformation

    def reformationchoice(self, iCiv):
        if iCiv == Civ.POPE.value:
            return  # Absinthe: totally exclude the Pope from the Reformation

        if gc.getPlayer(iCiv).getStateReligion() == Religion.PROTESTANTISM.value:
            self.reformationyes(iCiv)
        elif gc.getPlayer(iCiv).isHuman():
            self.reformationPopup()
        else:
            rndnum = gc.getGame().getSorenRandNum(100, "Reformation")
            if rndnum <= lReformationMatrix[iCiv]:
                self.reformationyes(iCiv)
            else:
                self.reformationno(iCiv)

    def reformationyes(self, iCiv):
        iFaith = 0
        for city in utils.getCityList(iCiv):
            if city.isHasReligion(Religion.CATHOLICISM.value):
                iFaith += self.reformationReformCity(city, iCiv)

        # disband catholic missionaries of the AI civs on reformation
        if iCiv != utils.getHumanID():
            unitList = PyPlayer(iCiv).getUnitList()
            for pUnit in unitList:
                iUnitType = pUnit.getUnitType()
                if iUnitType == xml.iCatholicMissionary:
                    pUnit.kill(0, -1)

        pPlayer = gc.getPlayer(iCiv)
        # iStateReligion = pPlayer.getStateReligion()
        # if (pPlayer.getStateReligion() == Religion.CATHOLICISM.value):
        pPlayer.setLastStateReligion(Religion.PROTESTANTISM.value)
        pPlayer.setConversionTimer(10)
        pPlayer.setFaith(iFaith)

    def reformationno(self, iCiv):
        cityList = PyPlayer(iCiv).getCityList()
        iLostFaith = 0
        pPlayer = gc.getPlayer(iCiv)
        for city in utils.getCityList(iCiv):
            if city.isHasReligion(Religion.CATHOLICISM.value) and not city.isHasReligion(
                Religion.PROTESTANTISM.value
            ):
                rndnum = gc.getGame().getSorenRandNum(100, "ReformationAnyway")
                if rndnum <= 25 + (
                    lReformationMatrix[iCiv] / 2
                ):  # only add the religion, chance between 30% and 70%, based on lReformationMatrix
                    city.setHasReligion(
                        Religion.PROTESTANTISM.value, True, False, False
                    )  # no announcement in this case
                    if pPlayer.isHuman():  # message for the human player
                        CityName = city.getNameKey()
                        CyInterface().addMessage(
                            utils.getHumanID(),
                            False,
                            MessageData.DURATION,
                            CyTranslator().getText(
                                "TXT_KEY_REFORMATION_RELIGION_STILL_SPREAD", (CityName,)
                            ),
                            "",
                            InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            "",
                            ColorTypes(MessageData.WHITE),
                            -1,
                            -1,
                            True,
                            True,
                        )
                    iLostFaith += 1
        gc.getPlayer(iCiv).changeFaith(-min(gc.getPlayer(iCiv).getFaith(), iLostFaith))

    def reformationOther(self, iCiv):
        for city in utils.getCityList(iCiv):
            if city.isHasReligion(Religion.CATHOLICISM.value):
                self.reformationOtherCity(city, iCiv)

    def reformationReformCity(self, pCity, iCiv):
        iFaith = 0
        iPopBonus = 0
        iAIBonus = 0
        pPlayer = gc.getPlayer(iCiv)
        # bigger cities have more chance for a new religion to spread
        if pCity.getPopulation() > 11:
            iPopBonus = 20
        elif pCity.getPopulation() > 8:
            iPopBonus = 15
        elif pCity.getPopulation() > 5:
            iPopBonus = 10
        elif pCity.getPopulation() > 2:
            iPopBonus = 5
        # civ-specific modifier, between 3 and 27
        iCivRef = (lReformationMatrix[pCity.getOwner()] / 10) * 3
        # AI bonus
        if utils.getHumanID() == iCiv:
            iAIBonus = 10

        # spread the religion: range goes from 48-68% (Catholicism-lovers) to 72-92% (Protestantism-lovers), based on lReformationMatrix
        # 						+10% extra bonus for the AI
        if (
            gc.getGame().getSorenRandNum(100, "Religion spread to City")
            < 45 + iCivRef + iPopBonus + iAIBonus
        ):
            pCity.setHasReligion(Religion.PROTESTANTISM.value, True, True, False)
            iFaith += 1
            iChance = 55 + iCivRef
            # if protestantism has spread, chance for replacing the buildings: between 58% and 82%, based on lReformationMatrix
            if (
                pCity.hasBuilding(xml.iCatholicChapel)
                and gc.getGame().getSorenRandNum(100, "Reformation of a City") < iChance
            ):
                pCity.setHasRealBuilding(xml.iCatholicChapel, False)
                pCity.setHasRealBuilding(xml.iProtestantChapel, True)
            if (
                pCity.hasBuilding(xml.iCatholicTemple)
                and gc.getGame().getSorenRandNum(100, "Reformation of a City") < iChance
            ):
                pCity.setHasRealBuilding(xml.iCatholicTemple, False)
                pCity.setHasRealBuilding(xml.iProtestantTemple, True)
                iFaith += 1
            if (
                pCity.hasBuilding(xml.iCatholicMonastery)
                and gc.getGame().getSorenRandNum(100, "Reformation of a City") < iChance
            ):
                pCity.setHasRealBuilding(xml.iCatholicMonastery, False)
                pCity.setHasRealBuilding(xml.iProtestantSeminary, True)
                iFaith += 1
            if (
                pCity.hasBuilding(xml.iCatholicCathedral)
                and gc.getGame().getSorenRandNum(100, "Reformation of a City") < iChance
            ):
                pCity.setHasRealBuilding(xml.iCatholicCathedral, False)
                pCity.setHasRealBuilding(xml.iProtestantCathedral, True)
                iFaith += 2

            # remove Catholicism if there are no religious buildings left, and there are no catholic wonders in the city
            if (
                gc.getGame().getSorenRandNum(100, "Remove Religion")
                < 55 + ((lReformationMatrix[iCiv] / 5) * 2) - iPopBonus
            ):  # range goes from 39-59% to 71-91%, based on lReformationMatrix
                lCathlist = [
                    xml.iCatholicTemple,
                    xml.iCatholicChapel,
                    xml.iCatholicMonastery,
                    xml.iCatholicCathedral,
                    xml.iMonasteryOfCluny,
                    xml.iKrakDesChevaliers,
                    xml.iPalaisPapes,
                    xml.iNotreDame,
                    xml.iWestminster,
                ]
                bCathBuildings = False
                for iBuilding in lCathlist:
                    if pCity.hasBuilding(iBuilding):
                        bCathBuildings = True
                        break
                if not bCathBuildings:
                    pCity.setHasReligion(Religion.CATHOLICISM.value, False, False, False)
                    if pPlayer.isHuman():  # message for the human player
                        CityName = pCity.getNameKey()
                        CyInterface().addMessage(
                            utils.getHumanID(),
                            False,
                            MessageData.DURATION,
                            CyTranslator().getText(
                                "TXT_KEY_REFORMATION_PEOPLE_ABANDON_CATHOLICISM_1", (CityName,)
                            ),
                            "",
                            InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            "",
                            ColorTypes(MessageData.WHITE),
                            -1,
                            -1,
                            True,
                            True,
                        )

        return iFaith

    def reformationOtherCity(self, pCity, iCiv):
        iPopBonus = 0
        pPlayer = gc.getPlayer(iCiv)
        # bigger cities have more chance for a new religion to spread
        if pCity.getPopulation() > 11:
            iPopBonus = 30
        elif pCity.getPopulation() > 7:
            iPopBonus = 20
        elif pCity.getPopulation() > 3:
            iPopBonus = 10
        # civ-specific, between 3 and 27
        iCivRef = (lReformationMatrix[pCity.getOwner()] / 10) * 3

        # spread the religion: range goes from 23-53% (Catholicism-lovers) to 47-77% (Protestantism-lovers), based on lReformationMatrix
        if gc.getGame().getSorenRandNum(100, "Religion spread to City") < 20 + iCivRef + iPopBonus:
            pCity.setHasReligion(Religion.PROTESTANTISM.value, True, True, False)
            # if protestantism has spread, chance for replacing the buildings: between 31% and 79%, based on lReformationMatrix
            iChance = 25 + 2 * iCivRef
            if (
                pCity.hasBuilding(xml.iCatholicChapel)
                and gc.getGame().getSorenRandNum(100, "Reformation of a City") < iChance
            ):
                pCity.setHasRealBuilding(xml.iCatholicChapel, False)
                pCity.setHasRealBuilding(xml.iProtestantChapel, True)
            if (
                pCity.hasBuilding(xml.iCatholicTemple)
                and gc.getGame().getSorenRandNum(100, "Reformation of a City") < iChance
            ):
                pCity.setHasRealBuilding(xml.iCatholicTemple, False)
                pCity.setHasRealBuilding(xml.iProtestantTemple, True)
            if (
                pCity.hasBuilding(xml.iCatholicMonastery)
                and gc.getGame().getSorenRandNum(100, "Reformation of a City") < iChance
            ):
                pCity.setHasRealBuilding(xml.iCatholicMonastery, False)
                pCity.setHasRealBuilding(xml.iProtestantSeminary, True)
            if (
                pCity.hasBuilding(xml.iCatholicCathedral)
                and gc.getGame().getSorenRandNum(100, "Reformation of a City") < iChance
            ):
                pCity.setHasRealBuilding(xml.iCatholicCathedral, False)
                pCity.setHasRealBuilding(xml.iProtestantCathedral, True)

            # remove Catholicism if there are no religious buildings left, and there are no catholic wonders in the city
            if gc.getGame().getSorenRandNum(100, "Remove Religion") < 50 + (
                (lReformationMatrix[iCiv] / 5) * 2
            ) - (
                iPopBonus / 2
            ):  # range goes from 39-54% to 71-86%, based on lReformationMatrix
                lCathlist = [
                    xml.iCatholicTemple,
                    xml.iCatholicChapel,
                    xml.iCatholicMonastery,
                    xml.iCatholicCathedral,
                    xml.iMonasteryOfCluny,
                    xml.iKrakDesChevaliers,
                    xml.iPalaisPapes,
                    xml.iNotreDame,
                    xml.iWestminster,
                ]
                bCathBuildings = False
                for iBuilding in lCathlist:
                    if pCity.hasBuilding(iBuilding):
                        bCathBuildings = True
                        break
                if not bCathBuildings:
                    pCity.setHasReligion(Religion.CATHOLICISM.value, False, False, False)
                    if pPlayer.isHuman():  # message for the human player
                        CityName = pCity.getNameKey()
                        if pPlayer.getStateReligion() == Religion.ISLAM.value:
                            CyInterface().addMessage(
                                utils.getHumanID(),
                                False,
                                MessageData.DURATION,
                                CyTranslator().getText(
                                    "TXT_KEY_REFORMATION_PEOPLE_ABANDON_CATHOLICISM_2", (CityName,)
                                ),
                                "",
                                InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                "",
                                ColorTypes(MessageData.WHITE),
                                -1,
                                -1,
                                True,
                                True,
                            )
                        else:
                            CyInterface().addMessage(
                                utils.getHumanID(),
                                False,
                                MessageData.DURATION,
                                CyTranslator().getText(
                                    "TXT_KEY_REFORMATION_PEOPLE_ABANDON_CATHOLICISM_3", (CityName,)
                                ),
                                "",
                                InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                "",
                                ColorTypes(MessageData.WHITE),
                                -1,
                                -1,
                                True,
                                True,
                            )

    def doCounterReformation(self):
        for iPlayer in range(Civ.POPE.value - 1):
            pPlayer = gc.getPlayer(iPlayer)
            if pPlayer.isAlive() and pPlayer.getStateReligion() == Religion.CATHOLICISM.value:
                if pPlayer.isHuman():
                    self.doCounterReformationHuman(iPlayer)
                elif lReformationMatrix[iPlayer] < gc.getGame().getSorenRandNum(
                    100, "Counter Reformation AI"
                ):
                    self.doCounterReformationYes(iPlayer)
                else:
                    self.doCounterReformationNo(iPlayer)
        self.setCounterReformationActive(False)

    def doCounterReformationHuman(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        szMessageYes = (
            CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_YES_1", ())
            + " +%d " % (max(1, pPlayer.getNumCities() / 3))
            + CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_YES_2", ())
        )
        szMessageNo = (
            CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_NO_1", ())
            + " +%d " % (max(1, pPlayer.getNumCities() / 3))
            + CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_NO_2", ())
        )
        self.showCounterPopup(
            7626,
            CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_TITLE", ()),
            CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE", ()),
            (szMessageYes, szMessageNo),
        )

    def showCounterPopup(self, popupID, title, message, labels):
        popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setHeaderString(title)
        popup.setBodyString(message)
        for i in labels:
            popup.addButton(i)
        popup.launch(False)

    def eventApply7626(self, popupReturn):
        iHuman = utils.getHumanID()
        if popupReturn.getButtonClicked() == 0:
            self.doCounterReformationYes(iHuman)
        elif popupReturn.getButtonClicked() == 1:
            self.doCounterReformationNo(iHuman)

    def eventApply7628(self, popupReturn):  # Absinthe: persecution popup
        """Persecution popup event."""
        iPlotX, iPlotY, iUnitID = utils.getPersecutionData()
        religionList = utils.getPersecutionReligions()
        iChosenButton = popupReturn.getButtonClicked()
        iChosenReligion = religionList[iChosenButton]
        utils.prosecute(iPlotX, iPlotY, iUnitID, iChosenReligion)

    def doCounterReformationYes(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        pCapital = pPlayer.getCapitalCity()
        iX = pCapital.getX()
        iY = pCapital.getY()
        if not pCapital.isNone():
            if pPlayer.getNumCities() > 0:
                pCapital = utils.getRandomEntry(utils.getCityList(iPlayer))
                iX = pCapital.getX()
                iY = pCapital.getY()
            else:
                return
        iNumProsecutors = max(1, pPlayer.getNumCities() / 3)
        for i in range(iNumProsecutors):
            pPlayer.initUnit(
                xml.iProsecutor,
                iX,
                iY,
                UnitAITypes.UNITAI_MISSIONARY,
                DirectionTypes.DIRECTION_SOUTH,
            )
        for iNbr in range(len(lReformationNeighbours[iPlayer])):
            pNbr = gc.getPlayer(lReformationNeighbours[iPlayer][iNbr])
            if pNbr.isAlive() and pNbr.getStateReligion() == Religion.PROTESTANTISM.value:
                pNCapital = pNbr.getCapitalCity()
                iX = pNCapital.getX()
                iY = pNCapital.getY()
                if not pNCapital.isNone():
                    if pNbr.getNumCities() > 0:
                        pNCapital = utils.getRandomEntry(
                            utils.getCityList(lReformationNeighbours[iPlayer][iNbr])
                        )
                        iX = pNCapital.getX()
                        iY = pNCapital.getY()
                    else:
                        return

                pNbr.initUnit(
                    xml.iProsecutor,
                    iX,
                    iY,
                    UnitAITypes.UNITAI_MISSIONARY,
                    DirectionTypes.DIRECTION_SOUTH,
                )

    def doCounterReformationNo(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        pPlayer.changeStabilityBase(
            StabilityCategory.CITIES.value, max(1, pPlayer.getNumCities() / 3)
        )

    ### End Reformation ###

    def resettleRefugies(self):
        intolerance = [-1] * CIVILIZATIONS.len()
        for iPlayer in CIVILIZATIONS.ids():
            pPlayer = gc.getPlayer(iPlayer)
            if pPlayer.isAlive():
                if iPlayer < Civ.POPE.value:
                    # add a random element
                    intolerance[iPlayer] += gc.getGame().getSorenRandNum(
                        100, "roll to randomize the migration of refugies"
                    )
                    intolerance[iPlayer] += 10 * pPlayer.getProsecutionCount()
                    if pPlayer.getProsecutionCount() == 0:
                        intolerance[iPlayer] = max(
                            0, intolerance[iPlayer] - 30
                        )  # if this player doesn't prosecute, decrease intolerance
                    iRCivic = pPlayer.getCivics(4)
                    if iRCivic == Civic.THEOCRACY.value:
                        intolerance[iPlayer] += 50
                    elif iRCivic == Civic.FREE_RELIGION.value:
                        intolerance[iPlayer] = max(0, intolerance[iPlayer] - 30)
                if iPlayer > Civ.POPE.value:
                    intolerance[iPlayer] += gc.getGame().getSorenRandNum(
                        100, "roll to randomize the migration of refugies"
                    )
        # once we have the list of potential nations
        iCandidate1 = 0
        for iPlayer in CIVILIZATIONS.ids():
            if intolerance[iPlayer] > -1 and intolerance[iPlayer] < intolerance[iCandidate1]:
                iCandidate1 = iPlayer
        iCandidate2 = 0
        if iCandidate2 == iCandidate1:
            iCandidate2 = 1
        for iPlayer in CIVILIZATIONS.ids():
            if (
                intolerance[iPlayer] > -1
                and iPlayer != iCandidate1
                and intolerance[iPlayer] < intolerance[iCandidate1]
            ):
                iCandidate2 = iPlayer

        if (
            gc.getGame().getSorenRandNum(
                100, "roll to migrate to one of the two most tolerant players"
            )
            > 50
        ):
            self.migrateJews(iCandidate1)
        else:
            self.migrateJews(iCandidate2)

    def migrateJews(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)

        lCityList = [
            city
            for city in utils.getCityList(iPlayer)
            if not city.isHasReligion(Religion.JUDAISM.value)
        ]

        if lCityList:
            city = utils.getRandomEntry(lCityList)
            city.setHasReligion(Religion.JUDAISM.value, True, True, False)

    def spread1200ADJews(self):
        # Spread Judaism to a random city in Africa
        tCity = self.selectRandomCityRegion(tWestAfrica, Religion.JUDAISM.value)
        if tCity:
            self.spreadReligion(tCity, Religion.JUDAISM.value)
        # Spread Judaism to another city in Spain
        tCity = self.selectRandomCityRegion(tSpain, Religion.JUDAISM.value)
        if tCity:
            self.spreadReligion(tCity, Religion.JUDAISM.value)
        # Spread Judaism to a city in France/Germany
        tCity = self.selectRandomCityRegion(tGermany, Religion.JUDAISM.value)
        if tCity:
            self.spreadReligion(tCity, Religion.JUDAISM.value)

    def setStartingFaith(self):
        for civilization in CIVILIZATIONS.dropna("initial"):
            condition = civilization.initial.condition
            if condition:
                civilization.player.setFaith(condition.faith)

    def getCatholicCivs(self, bOpenBorders=False):
        teamPope = gc.getTeam(gc.getPlayer(Civ.POPE.value).getTeam())
        lCatholicCivs = []
        for iPlayer in CIVILIZATIONS.main().ids():
            pPlayer = gc.getPlayer(iPlayer)
            if pPlayer.getStateReligion() == Religion.CATHOLICISM.value:
                if bOpenBorders and not teamPope.isOpenBorders(pPlayer.getTeam()):
                    continue
                lCatholicCivs.append(iPlayer)
        return lCatholicCivs
