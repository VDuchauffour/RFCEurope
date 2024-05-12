from CvPythonExtensions import (
    CyGlobalContext,
    EventContextTypes,
    InterfaceMessageTypes,
    UnitAITypes,
    DirectionTypes,
)
from Consts import MessageData
from CoreData import civilization, civilizations
from CoreFunctions import event_popup, get_religion_by_id, location, message, text
from CoreStructures import human, player, year, cities, units
from CoreTypes import (
    Building,
    Civ,
    City,
    Civic,
    Province,
    StabilityCategory,
    Religion,
    Technology,
    Unit,
    Wonder,
)
from LocationsData import CITIES
import Popup
from ProvinceMapData import PROVINCES_MAP
from RFCUtils import getBaseBuilding, prosecute
from StoredData import data
from PyUtils import choice, percentage, percentage_chance, rand

from MiscData import RELIGIOUS_BUILDINGS, RELIGIOUS_WONDERS

gc = CyGlobalContext()


### Regions to spread religion ###
tSpain = [
    Province.LEON.value,
    Province.GALICIA.value,
    Province.ARAGON.value,
    Province.CATALONIA.value,
    Province.CASTILE.value,
    Province.LA_MANCHA.value,
    Province.ANDALUSIA.value,
    Province.VALENCIA.value,
]
tPoland = [
    Province.GREATER_POLAND.value,
    Province.LESSER_POLAND.value,
    Province.MASOVIA.value,
    Province.SILESIA.value,
    Province.SUVALKIJA.value,
    Province.BREST.value,
    Province.POMERANIA.value,
    Province.GALICJA.value,
]
tGermany = [
    Province.LORRAINE.value,
    Province.FRANCONIA.value,
    Province.BAVARIA.value,
    Province.SWABIA.value,
]
tWestAfrica = [
    Province.TETOUAN.value,
    Province.MOROCCO.value,
    Province.MARRAKESH.value,
    Province.FEZ.value,
    Province.ORAN.value,
]
tNorthAfrica = [
    Province.ALGIERS.value,
    Province.IFRIQIYA.value,
    Province.TRIPOLITANIA.value,
    Province.CYRENAICA.value,
]
tBalkansAndAnatolia = [
    Province.CONSTANTINOPLE.value,
    Province.THRACE.value,
    Province.OPSIKION.value,
    Province.PAPHLAGONIA.value,
    Province.THRAKESION.value,
    Province.CILICIA.value,
    Province.ANATOLIKON.value,
    Province.ARMENIAKON.value,
    Province.CHARSIANON.value,
]
tCentralEurope = [
    Province.GREATER_POLAND.value,
    Province.LESSER_POLAND.value,
    Province.MASOVIA.value,
    Province.GALICJA.value,
    Province.BREST.value,
    Province.SUVALKIJA.value,
    Province.LITHUANIA.value,
    Province.PRUSSIA.value,
    Province.POMERANIA.value,
    Province.SAXONY.value,
    Province.BRANDENBURG.value,
    Province.HOLSTEIN.value,
    Province.DENMARK.value,
    Province.BAVARIA.value,
    Province.SWABIA.value,
    Province.BOHEMIA.value,
    Province.MORAVIA.value,
    Province.SILESIA.value,
    Province.HUNGARY.value,
    Province.TRANSYLVANIA.value,
    Province.UPPER_HUNGARY.value,
    Province.PANNONIA.value,
    Province.SLAVONIA.value,
    Province.CARINTHIA.value,
    Province.AUSTRIA.value,
]
tMaghrebAndalusia = [
    Province.TETOUAN.value,
    Province.MOROCCO.value,
    Province.MARRAKESH.value,
    Province.FEZ.value,
    Province.ORAN.value,
    Province.ALGIERS.value,
    Province.IFRIQIYA.value,
    Province.TRIPOLITANIA.value,
    Province.CYRENAICA.value,
    Province.LA_MANCHA.value,
    Province.ANDALUSIA.value,
    Province.VALENCIA.value,
]
tBulgariaBalkans = [
    Province.MOESIA.value,
    Province.MACEDONIA.value,
    Province.SERBIA.value,
    Province.WALLACHIA.value,
]
tOldRus = [
    Province.NOVGOROD.value,
    Province.ROSTOV.value,
    Province.POLOTSK.value,
    Province.SMOLENSK.value,
    Province.MINSK.value,
    Province.CHERNIGOV.value,
    Province.KIEV.value,
    Province.PEREYASLAVL.value,
    Province.SLOBODA.value,
]
tSouthScandinavia = [
    Province.DENMARK.value,
    Province.GOTALAND.value,
    Province.SKANELAND.value,
    Province.VESTFOLD.value,
    Province.NORWAY.value,
]
tHungary = [
    Province.HUNGARY.value,
    Province.TRANSYLVANIA.value,
    Province.UPPER_HUNGARY.value,
    Province.PANNONIA.value,
]


class Religions:

    ##################################################
    ### Secure storage & retrieval of script data ###
    ################################################

    def getReformationActive(self):
        return data.bReformationActive

    def setReformationActive(self, bNewValue):
        data.bReformationActive = bNewValue

    def getReformationHitMatrix(self, iCiv):
        return data.lReformationHitMatrix[iCiv]

    def setReformationHitMatrix(self, iCiv, bNewValue):
        data.lReformationHitMatrix[iCiv] = bNewValue

    def getReformationHitMatrixAll(self):
        return data.lReformationHitMatrix

    def getCounterReformationActive(self):
        return data.bCounterReformationActive

    def setCounterReformationActive(self, bNewValue):
        data.bCounterReformationActive = bNewValue

    #######################################
    ### Main methods (Event-Triggered) ###
    #####################################

    def setup(self):
        gc.getPlayer(Civ.BYZANTIUM.value).changeFaith(10)
        gc.getPlayer(Civ.OTTOMAN.value).changeFaith(20)

    def checkTurn(self, iGameTurn):
        # Absinthe: Spreading religion in a couple preset dates
        if iGameTurn == year(700) - 2:
            # Spread Judaism to Toledo
            self.spreadReligion(CITIES[City.TOLEDO], Religion.JUDAISM.value)
            # Spread Islam to a random city in Africa
            tCity = self.selectRandomCityRegion(tNorthAfrica, Religion.ISLAM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.ISLAM.value)
        elif iGameTurn == year(700) + 2:
            # Spread Judaism and Islam to a random city in Africa
            tCity = self.selectRandomCityRegion(tWestAfrica, Religion.ISLAM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.ISLAM.value)
            tCity = self.selectRandomCityRegion(tWestAfrica, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
        elif iGameTurn == year(900):
            # Spread Judaism to another city in Spain
            tCity = self.selectRandomCityRegion(tSpain, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
        elif iGameTurn == year(1000):
            # Spread Judaism to a city in France/Germany
            tCity = self.selectRandomCityRegion(tGermany, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
            # Spread Islam to another city in Africa
            tCity = self.selectRandomCityRegion(tNorthAfrica, Religion.ISLAM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.ISLAM.value)
        elif iGameTurn == year(1101):
            # Spread Judaism to a couple towns in Poland
            tCity = self.selectRandomCityRegion(tPoland, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
        elif iGameTurn == year(1200):
            # Spread Judaism to a couple towns in Poland
            tCity = self.selectRandomCityRegion(tPoland, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)
        elif year(1299) < iGameTurn < year(1350) and iGameTurn % 3 == 0:
            # Spread Islam to a couple cities in Anatolia before the Ottoman spawn
            tCity = self.selectRandomCityRegion(tBalkansAndAnatolia, Religion.ISLAM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.ISLAM.value)
        elif iGameTurn == year(1401):
            # Spread Judaism to a couple towns in Poland
            tCity = self.selectRandomCityRegion(tPoland, Religion.JUDAISM.value)
            if tCity:
                self.spreadReligion(tCity, Religion.JUDAISM.value)

        # Absinthe: Spreading Judaism in random dates
        # General 6% chance to spread Jews to a random city in every third turn
        if year(800) < iGameTurn < year(1700) and iGameTurn % 3 == 0:
            if percentage_chance(6, strict=True):
                tCity = cities().all().random_entry()
                if tCity is not None:
                    self.spreadReligion(tCity, Religion.JUDAISM.value)

        # Additional 11% chance to spread Jews to a random Central European city in every third turn
        if year(1000) < iGameTurn < year(1500) and iGameTurn % 3 == 1:
            if percentage_chance(11, strict=True):
                tCity = self.selectRandomCityRegion(tCentralEurope, Religion.JUDAISM.value)
                if tCity:
                    self.spreadReligion(tCity, Religion.JUDAISM.value)

        # Absinthe: Encouraging desired religion spread in a couple areas (mostly for Islam and Orthodoxy)
        # Maghreb and Cordoba:
        if year(700) < iGameTurn < year(800) and iGameTurn % 2 == 1:
            if percentage_chance(32, strict=True):
                tCity = self.selectRandomCityRegion(tMaghrebAndalusia, Religion.ISLAM.value, True)
                if tCity:
                    self.spreadReligion(tCity, Religion.ISLAM.value)
        if year(800) < iGameTurn < year(1200) and iGameTurn % 3 == 2:
            if percentage_chance(28, strict=True):
                tCity = self.selectRandomCityRegion(tMaghrebAndalusia, Religion.ISLAM.value, True)
                if tCity:
                    self.spreadReligion(tCity, Religion.ISLAM.value)

        # Bulgaria and Balkans:
        if year(700) < iGameTurn < year(800) and iGameTurn % 3 == 1:
            if percentage_chance(25, strict=True):
                tCity = self.selectRandomCityRegion(
                    tBulgariaBalkans, Religion.ORTHODOXY.value, True
                )
                if tCity:
                    self.spreadReligion(tCity, Religion.ORTHODOXY.value)
        if year(800) < iGameTurn < year(1000) and iGameTurn % 4 == 1:
            if percentage_chance(15, strict=True):
                tCity = self.selectRandomCityRegion(
                    tBulgariaBalkans, Religion.ORTHODOXY.value, True
                )
                if tCity:
                    self.spreadReligion(tCity, Religion.ORTHODOXY.value)
        # Old Rus territories:
        if year(852) < iGameTurn < year(1300) and iGameTurn % 4 == 3:
            if percentage_chance(25, strict=True):
                tCity = self.selectRandomCityRegion(tOldRus, Religion.ORTHODOXY.value, True)
                if tCity:
                    self.spreadReligion(tCity, Religion.ORTHODOXY.value)

        # Extra chance for early Orthodoxy spread in Novgorod:
        if year(852) < iGameTurn < year(960) and iGameTurn % 5 == 2:
            if percentage_chance(34, strict=True):
                tCity = self.selectRandomCityRegion(
                    [Province.NOVGOROD.value, Province.POLOTSK.value, Province.SMOLENSK.value],
                    Religion.ORTHODOXY.value,
                    True,
                )
                if tCity:
                    self.spreadReligion(tCity, Religion.ORTHODOXY.value)
        # Hungary:
        if year(960) < iGameTurn < year(1200) and iGameTurn % 4 == 2:
            if percentage_chance(21, strict=True):
                tCity = self.selectRandomCityRegion(tHungary, Religion.CATHOLICISM.value, True)
                if tCity:
                    self.spreadReligion(tCity, Religion.CATHOLICISM.value)

        # Scandinavia:
        if year(1000) < iGameTurn < year(1300) and iGameTurn % 4 == 0:
            if percentage_chance(24, strict=True):
                tCity = self.selectRandomCityRegion(
                    tSouthScandinavia, Religion.CATHOLICISM.value, True
                )
                if tCity:
                    self.spreadReligion(tCity, Religion.CATHOLICISM.value)

        # Absinthe: Persecution cooldown
        for i in civilizations().majors().ids():
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
        catholic_civs = civilizations().main().catholic().open_borders(Civ.POPE)
        # Gold gift
        if iGameTurn >= year(752):
            if iGameTurn > year(1648):  # End of religious wars
                iDivBy = 14
            elif iGameTurn > year(1517):  # Protestantism
                iDivBy = 11
            elif iGameTurn > year(1053):  # Schism
                iDivBy = 6
            else:
                iDivBy = 9
            if (
                iGameTurn % iDivBy == 3
                and player(Civ.POPE).getGold() > 100
                and percentage_chance(90)
            ):
                weights = []
                for civ in catholic_civs:
                    iCatholicFaith = 0
                    # Relations with the Pope are much more important here
                    iCatholicFaith += civ.player.getFaith()
                    iCatholicFaith += 8 * max(0, player(Civ.POPE).AI_getAttitude(civ.id))
                    if iCatholicFaith > 0:
                        weights.append(iCatholicFaith)
                    else:
                        weights.append(0)

                if catholic_civs:
                    iChosenPlayer = choice(catholic_civs, weights)
                    if iGameTurn < 100:
                        iGift = min(
                            player(Civ.POPE).getGold() / 5, 40
                        )  # between 20-40, based on the Pope's wealth
                    else:
                        iGift = min(
                            player(Civ.POPE).getGold() / 2, 80
                        )  # between 50-80, based on the Pope's wealth
                    civilization(Civ.POPE).send_gold(iChosenPlayer, iGift)

                    if iChosenPlayer.is_human():
                        sText = text("TXT_KEY_FAITH_GOLD_GIFT", iGift)
                        message(civ.id, sText, color=MessageData.BLUE)
        # Free religious building
        if iGameTurn > year(800):  # The crowning of Charlemagne
            if iGameTurn > year(1648):  # End of religious wars
                iDivBy = 21
            elif iGameTurn > year(1517):  # Protestantism
                iDivBy = 14
            elif iGameTurn > year(1053):  # Schism
                iDivBy = 8
            else:
                iDivBy = 11
            if iGameTurn % iDivBy == 2 and percentage_chance(80, strict=True):
                weights = []
                iJerusalemOwner = (
                    gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity().getOwner()
                )
                for civ in catholic_civs:
                    iCatholicFaith = 0
                    # Faith points are the deciding factor for buildings
                    iCatholicFaith += civ.player.getFaith()
                    iCatholicFaith += 2 * max(0, player(Civ.POPE).AI_getAttitude(civ.id))
                    if (
                        civ.id == iJerusalemOwner
                    ):  # The Catholic owner of Jerusalem has a greatly improved chance
                        iCatholicFaith += 30
                    if iCatholicFaith > 0:
                        weights.append(iCatholicFaith)

                if catholic_civs:
                    iChosenPlayer = choice(catholic_civs, weights)
                    iCatholicBuilding = Building.CATHOLIC_TEMPLE.value
                    # No chance for monastery if the selected player knows the Scientific Method tech (which obsoletes monasteries), otherwise 50-50% for temple and monastery
                    if not iChosenPlayer.has_tech(
                        Technology.SCIENTIFIC_METHOD
                    ) and percentage_chance(50):
                        iCatholicBuilding = Building.CATHOLIC_MONASTERY.value
                    self.buildInRandomCity(
                        iChosenPlayer.id, iCatholicBuilding, Religion.CATHOLICISM.value
                    )
        # Free technology
        if iGameTurn > year(843):  # Treaty of Verdun, the Carolingian Empire divided into 3 parts
            if (
                iGameTurn % 13 == 4
            ):  # checked every 13th turn - won't change it as the game progresses, as the number of available techs will already change with the number of Catholic civs
                weights = []
                for civ in catholic_civs:
                    iCatholicFaith = 0
                    # Faith points are the deciding factor for techs
                    iCatholicFaith += civ.player.getFaith()
                    iCatholicFaith += 2 * max(0, player(Civ.POPE).AI_getAttitude(civ.id))
                    if iCatholicFaith > 0:
                        weights.append(iCatholicFaith)
                    else:
                        weights.append(0)

                if catholic_civs:
                    iChosenPlayer = choice(catholic_civs, weights)
                    # look for techs which are known by the Pope but unknown to the chosen civ
                    for tech in Technology:
                        if (
                            civilization(Civ.POPE).has_tech(tech)
                            and not iChosenPlayer.has_tech(tech)
                            and iChosenPlayer.player.getFaith() + 20 > rand(70)
                        ):
                            # chance for actually giving this tech, based on faith points
                            # +20, to have a real chance with low faith points as well
                            iChosenPlayer.add_tech(tech, annoncing=True)
                            if iChosenPlayer.is_human():
                                sText = text(
                                    "TXT_KEY_FAITH_TECH_GIFT",
                                    gc.getTechInfo(tech).getDescription(),
                                )
                                message(
                                    iChosenPlayer.id, sText, force=True, color=MessageData.BLUE
                                )
                            # don't continue if a tech was already given - this also means that there is bigger chance for getting a tech if the chosen civ is multiple techs behind
                            break

        if iGameTurn % 6 == 3:
            self.update_pope_techs(catholic_civs)

        # Absinthe: Reformation
        if self.getCounterReformationActive():
            self.doCounterReformation()
        if self.getReformationActive():
            self.reformationArrayChoice()
            if self.getReformationActive():
                self.reformationArrayChoice()
                if self.getReformationActive():
                    self.reformationArrayChoice()

    def update_pope_techs(self, catholic_civs):
        # Absinthe: Pope gets all techs known by at least 3 Catholic civs
        catholic_civs = civilizations().main().catholic()
        for tech in Technology:
            if not civilization(Civ.POPE).has_tech(tech):
                counter = 0
                for civ in catholic_civs:
                    if civ.has_tech(tech):
                        counter += 1
                        if counter >= 3:
                            civilization(Civ.POPE).add_tech(tech)
                            break

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
            if (
                iStateReligion == Religion.CATHOLICISM
                and iBuilding in RELIGIOUS_BUILDINGS[Religion.CATHOLICISM]
            ):
                pPlayer.changeFaith(1)
                if iBuilding == Building.CATHOLIC_CATHEDRAL.value:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(Wonder.PALAIS_DES_PAPES.value) > 0:
                    pPlayer.changeFaith(1)
            elif (
                iStateReligion == Religion.ORTHODOXY
                and iBuilding in RELIGIOUS_BUILDINGS[Religion.ORTHODOXY]
            ):
                pPlayer.changeFaith(1)
                if iBuilding == Building.ORTHODOX_CATHEDRAL.value:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(Wonder.PALAIS_DES_PAPES.value) > 0:
                    pPlayer.changeFaith(1)
            elif (
                iStateReligion == Religion.ISLAM
                and iBuilding in RELIGIOUS_BUILDINGS[Religion.ISLAM]
            ):
                pPlayer.changeFaith(1)
                if iBuilding == Building.ISLAMIC_CATHEDRAL.value:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(Wonder.PALAIS_DES_PAPES.value) > 0:
                    pPlayer.changeFaith(1)
            elif (
                iStateReligion == Religion.PROTESTANTISM
                and iBuilding in RELIGIOUS_BUILDINGS[Religion.PROTESTANTISM]
            ):
                pPlayer.changeFaith(1)
                if iBuilding == Building.PROTESTANT_CATHEDRAL.value:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(Wonder.PALAIS_DES_PAPES.value) > 0:
                    pPlayer.changeFaith(1)
            elif iStateReligion == Religion.JUDAISM.value and iBuilding in [
                Building.JEWISH_QUARTER.value,
                Wonder.KAZIMIERZ.value,
            ]:
                pPlayer.changeFaith(1)
                if iBuilding == Wonder.KAZIMIERZ.value:
                    pPlayer.changeFaith(3)
                if pPlayer.countNumBuildings(Wonder.PALAIS_DES_PAPES.value) > 0:
                    pPlayer.changeFaith(1)
            # Absinthe: Wonders: Mont Saint-Michel wonder effect
            if getBaseBuilding(iBuilding) in [Building.WALLS.value, Building.CASTLE.value]:
                if pPlayer.countNumBuildings(Wonder.MONT_SAINT_MICHEL.value) > 0:
                    pPlayer.changeFaith(1)
        if iBuilding in RELIGIOUS_WONDERS:
            pPlayer.changeFaith(4)
            if pPlayer.countNumBuildings(Wonder.PALAIS_DES_PAPES.value) > 0:
                pPlayer.changeFaith(1)
        if iStateReligion != Religion.JUDAISM.value and iBuilding == Wonder.KAZIMIERZ.value:
            pPlayer.changeFaith(-min(1, pPlayer.getFaith()))
            # Kazimierz tries to spread Judaism to a couple new cities
            cityList = cities().owner(iPlayer).entities()
            iJewCityNum = int(max((len(cityList) + 2) / 3 + 1, 3))
            # number of tries are based on number of cities, but at least 3
            for i in range(iJewCityNum):
                city = choice(cityList)
                if not city.isHasReligion(Religion.JUDAISM.value):
                    city.setHasReligion(Religion.JUDAISM.value, True, True, False)
            # Adds Jewish Quarter to all cities which already has Judaism (including the ones where it just spread)
            for city in cityList:
                if city.isHasReligion(Religion.JUDAISM.value):
                    city.setHasRealBuilding(Building.JEWISH_QUARTER.value, True)

    def selectRandomCityRegion(self, tProvinces, iReligionToSpread, bNoSpreadWithReligion=False):
        cityList = []
        for iPlayer in civilizations().ids():
            if not gc.getPlayer(iPlayer).isAlive():
                continue
            for city in cities().owner(iPlayer).entities():
                if PROVINCES_MAP[city.getY()][city.getX()] in tProvinces:
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
            city = choice(cityList)
            return (city.getX(), city.getY())
        return False

    def spreadReligion(self, tPlot, iReligion):
        x, y = location(tPlot)
        pPlot = gc.getMap().plot(x, y)
        if pPlot.isCity():
            pPlot.getPlotCity().setHasReligion(
                iReligion, True, True, False
            )  # Absinthe: puts the given religion into this city, with interface message

    def buildInRandomCity(self, iPlayer, iBuilding, iReligion):
        cityList = []
        for city in cities().owner(iPlayer).entities():
            if not city.hasBuilding(iBuilding) and city.isHasReligion(iReligion):
                cityList.append(city)
        if cityList:
            city = choice(cityList)
            city.setHasRealBuilding(iBuilding, True)
            gc.getPlayer(iPlayer).changeFaith(1)
            if human() == iPlayer:
                sText = (
                    text("TXT_KEY_FAITH_BUILDING1")
                    + " "
                    + gc.getBuildingInfo(iBuilding).getDescription()
                    + " "
                    + text("TXT_KEY_FAITH_BUILDING2")
                    + " "
                    + city.getName()
                )
                message(
                    iPlayer,
                    sText,
                    button=gc.getBuildingInfo(iBuilding).getButton(),
                    color=MessageData.BLUE,
                    location=city,
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
                if iPlayer == human():
                    # check the available religions
                    religionList = []
                    for city in cities().owner(iPlayer).entities():
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
                    data.lReligionChoices = religionList
                    # no popup if no available religions
                    if religionList:
                        self.showFreeRevolutionPopup(iPlayer, religionList)
                elif iPlayer < civilizations().main().len():
                    iBestReligionPoint = 0
                    iBestReligion = Religion.CATHOLICISM.value
                    # loop through all religions
                    for iReligion in range(gc.getNumReligionInfos()):
                        iReligionPoint = 0
                        # check cities for religions and holy cities
                        for city in cities().owner(iPlayer).entities():
                            if city.isHasReligion(iReligion):
                                iReligionPoint += 10
                            if city.isHolyCityByType(iReligion):
                                iReligionPoint += 1000
                        spread_factor = civilization(iPlayer).religion.spreading_threshold[
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

    # Absinthe: free religion change popup
    def showFreeRevolutionPopup(self, iPlayer, religionList):
        """Possibility for the human player to select a religion anarchy-free."""
        popup = Popup.PyPopup(7629, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setHeaderString("Religious Revolution")
        popup.setBodyString("Choose the religion you want to adopt as your State Religion:")
        for iReligion in religionList:
            strIcon = gc.getReligionInfo(iReligion).getType()
            strIcon = "[%s]" % (strIcon.replace("RELIGION_", "ICON_"))
            strButtonText = "%s %s" % (text(strIcon), gc.getReligionInfo(iReligion).getText())
            popup.addButton(strButtonText)
        popup.addButton("We don't want to adopt a State Religion right now")
        popup.launch(False)

    # Absinthe: event of the free religion change popup
    def eventApply7629(self, playerID, popupReturn):
        """Free religious revolution."""
        # the last option is the no change option
        player(playerID).convertForFree(data.lReligionChoices[popupReturn.getButtonClicked()])

    # REFORMATION

    def eventApply7624(self, popupReturn):
        iHuman = human()
        if popupReturn.getButtonClicked() == 0:
            self.reformationyes(iHuman)
        elif popupReturn.getButtonClicked() == 1:
            self.reformationno(iHuman)

    def onTechAcquired(self, iTech, iPlayer):
        if iTech == Technology.PRINTING_PRESS.value:
            if gc.getPlayer(iPlayer).getStateReligion() == Religion.CATHOLICISM.value:
                if not gc.getGame().isReligionFounded(Religion.PROTESTANTISM.value):
                    gc.getPlayer(iPlayer).foundReligion(
                        Religion.PROTESTANTISM.value, Religion.PROTESTANTISM.value, False
                    )
                    gc.getGame().getHolyCity(Religion.PROTESTANTISM.value).setNumRealBuilding(
                        Building.PROTESTANT_SHRINE.value, 1
                    )
                    self.setReformationActive(True)
                    self.reformationchoice(iPlayer)
                    self.reformationOther(Civ.INDEPENDENT.value)
                    self.reformationOther(Civ.INDEPENDENT_2.value)
                    self.reformationOther(Civ.INDEPENDENT_3.value)
                    self.reformationOther(Civ.INDEPENDENT_4.value)
                    self.reformationOther(Civ.BARBARIAN.value)
                    self.setReformationHitMatrix(iPlayer, 2)
                    self.spread_reform_to_neighbour(iPlayer)

    def spread_reform_to_neighbour(self, player_id):
        for neighbour in civilization(player_id).location.reformation_neighbours:
            if self.getReformationHitMatrix(neighbour.value) == 0:
                self.setReformationHitMatrix(neighbour.value, 1)

    def reformationArrayChoice(self):
        civ = (
            civilizations()
            .majors()
            .filter(lambda c: self.getReformationHitMatrix(c.id) == 1)
            .random_entry()
        )
        if civ is not None:
            if civ.is_alive() and civ.is_catholic():
                self.reformationchoice(civ.id)
            else:
                self.reformationOther(civ.id)
            self.setReformationHitMatrix(civ.id, 2)
            self.spread_reform_to_neighbour(civ.id)

            if sum(self.getReformationHitMatrixAll()) == 2 * civilizations().majors().len():
                self.setReformationActive(False)
                # after all players have been hit by the Reformation
                self.setCounterReformationActive(True)

    def reformationchoice(self, iCiv):
        if iCiv == Civ.POPE.value:
            return  # Absinthe: totally exclude the Pope from the Reformation

        if civilization(iCiv).has_state_religion(Religion.PROTESTANTISM) or percentage_chance(
            civilization(iCiv).ai.reformation_threshold
        ):
            self.reformationyes(iCiv)
        elif civilization(iCiv).is_human():
            event_popup(
                7624,
                text("TXT_KEY_REFORMATION_TITLE"),
                text("TXT_KEY_REFORMATION_MESSAGE"),
                [text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO")],
            )
        else:
            self.reformationno(iCiv)

    def reformationyes(self, iCiv):
        iFaith = 0
        for city in cities().owner(iCiv).entities():
            if city.isHasReligion(Religion.CATHOLICISM.value):
                iFaith += self.reformationReformCity(city, iCiv)

        # disband catholic missionaries of the AI civs on reformation
        if iCiv != human():
            for pUnit in units().owner(iCiv).entities():
                iUnitType = pUnit.getUnitType()
                if iUnitType == Unit.CATHOLIC_MISSIONARY.value:
                    pUnit.kill(0, -1)

        pPlayer = gc.getPlayer(iCiv)
        # iStateReligion = pPlayer.getStateReligion()
        # if (pPlayer.getStateReligion() == Religion.CATHOLICISM.value):
        pPlayer.setLastStateReligion(Religion.PROTESTANTISM.value)
        pPlayer.setConversionTimer(10)
        pPlayer.setFaith(iFaith)

    def reformationno(self, iCiv):
        iLostFaith = 0
        pPlayer = gc.getPlayer(iCiv)
        for city in cities().owner(iCiv).entities():
            if city.isHasReligion(Religion.CATHOLICISM.value) and not city.isHasReligion(
                Religion.PROTESTANTISM.value
            ):
                if percentage_chance(25 + civilization(iCiv).ai.reformation_threshold / 2):
                    city.setHasReligion(
                        Religion.PROTESTANTISM.value, True, False, False
                    )  # no announcement in this case
                    if pPlayer.isHuman():
                        CityName = city.getNameKey()
                        message(
                            human(),
                            text("TXT_KEY_REFORMATION_RELIGION_STILL_SPREAD", CityName),
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            color=MessageData.WHITE,
                        )
                    iLostFaith += 1
        gc.getPlayer(iCiv).changeFaith(-min(gc.getPlayer(iCiv).getFaith(), iLostFaith))

    def reformationOther(self, iCiv):
        for city in cities().owner(iCiv).entities():
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
        iCivRef = (civilization(pCity).ai.reformation_threshold / 10) * 3
        # AI bonus
        if human() == iCiv:
            iAIBonus = 10

        # spread the religion: range goes from 48-68% (Catholicism-lovers) to 72-92% (Protestantism-lovers), based on lReformationMatrix
        # 						+10% extra bonus for the AI
        if percentage_chance(45 + iCivRef + iPopBonus + iAIBonus, strict=True):
            pCity.setHasReligion(Religion.PROTESTANTISM.value, True, True, False)
            iFaith += 1
            iChance = 55 + iCivRef
            # if protestantism has spread, chance for replacing the buildings: between 58% and 82%, based on lReformationMatrix
            if pCity.hasBuilding(Building.CATHOLIC_CHAPEL.value) and percentage_chance(
                iChance, strict=True
            ):
                pCity.setHasRealBuilding(Building.CATHOLIC_CHAPEL.value, False)
                pCity.setHasRealBuilding(Building.PROTESTANT_CHAPEL.value, True)
            if pCity.hasBuilding(Building.CATHOLIC_TEMPLE.value) and percentage_chance(
                iChance, strict=True
            ):
                pCity.setHasRealBuilding(Building.CATHOLIC_TEMPLE.value, False)
                pCity.setHasRealBuilding(Building.PROTESTANT_TEMPLE.value, True)
                iFaith += 1
            if pCity.hasBuilding(Building.CATHOLIC_MONASTERY.value) and percentage_chance(
                iChance, strict=True
            ):
                pCity.setHasRealBuilding(Building.CATHOLIC_MONASTERY.value, False)
                pCity.setHasRealBuilding(Building.PROTESTANT_SEMINARY.value, True)
                iFaith += 1
            if pCity.hasBuilding(Building.CATHOLIC_CATHEDRAL.value) and percentage_chance(
                iChance, strict=True
            ):
                pCity.setHasRealBuilding(Building.CATHOLIC_CATHEDRAL.value, False)
                pCity.setHasRealBuilding(Building.PROTESTANT_CATHEDRAL.value, True)
                iFaith += 2

            # remove Catholicism if there are no religious buildings left, and there are no catholic wonders in the city
            # range goes from 39-59% to 71-91%, based on lReformationMatrix
            if percentage_chance(
                55 + ((civilization(iCiv).ai.reformation_threshold / 5) * 2) - iPopBonus,
                strict=True,
            ):
                lCathlist = [
                    Building.CATHOLIC_TEMPLE.value,
                    Building.CATHOLIC_CHAPEL.value,
                    Building.CATHOLIC_MONASTERY.value,
                    Building.CATHOLIC_CATHEDRAL.value,
                    Wonder.MONASTERY_OF_CLUNY.value,
                    Wonder.KRAK_DES_CHEVALIERS.value,
                    Wonder.PALAIS_DES_PAPES.value,
                    Wonder.NOTRE_DAME.value,
                    Wonder.WESTMINSTER.value,
                ]
                bCathBuildings = False
                for iBuilding in lCathlist:
                    if pCity.hasBuilding(iBuilding):
                        bCathBuildings = True
                        break
                if not bCathBuildings:
                    pCity.setHasReligion(Religion.CATHOLICISM.value, False, False, False)
                    if pPlayer.isHuman():
                        CityName = pCity.getNameKey()
                        message(
                            human(),
                            text("TXT_KEY_REFORMATION_PEOPLE_ABANDON_CATHOLICISM_1", CityName),
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            color=MessageData.WHITE,
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
        iCivRef = (civilization(pCity).ai.reformation_threshold / 10) * 3

        # spread the religion: range goes from 23-53% (Catholicism-lovers) to 47-77% (Protestantism-lovers), based on lReformationMatrix
        if percentage_chance(20 + iCivRef + iPopBonus, strict=True):
            pCity.setHasReligion(Religion.PROTESTANTISM.value, True, True, False)
            # if protestantism has spread, chance for replacing the buildings: between 31% and 79%, based on lReformationMatrix
            iChance = 25 + 2 * iCivRef
            if pCity.hasBuilding(Building.CATHOLIC_CHAPEL.value) and percentage_chance(
                iChance, strict=True
            ):
                pCity.setHasRealBuilding(Building.CATHOLIC_CHAPEL.value, False)
                pCity.setHasRealBuilding(Building.PROTESTANT_CHAPEL.value, True)
            if pCity.hasBuilding(Building.CATHOLIC_TEMPLE.value) and percentage_chance(
                iChance, strict=True
            ):
                pCity.setHasRealBuilding(Building.CATHOLIC_TEMPLE.value, False)
                pCity.setHasRealBuilding(Building.PROTESTANT_TEMPLE.value, True)
            if pCity.hasBuilding(Building.CATHOLIC_MONASTERY.value) and percentage_chance(
                iChance, strict=True
            ):
                pCity.setHasRealBuilding(Building.CATHOLIC_MONASTERY.value, False)
                pCity.setHasRealBuilding(Building.PROTESTANT_SEMINARY.value, True)
            if pCity.hasBuilding(Building.CATHOLIC_CATHEDRAL.value) and percentage_chance(
                iChance, strict=True
            ):
                pCity.setHasRealBuilding(Building.CATHOLIC_CATHEDRAL.value, False)
                pCity.setHasRealBuilding(Building.PROTESTANT_CATHEDRAL.value, True)

            # remove Catholicism if there are no religious buildings left, and there are no catholic wonders in the city
            # range goes from 39-54% to 71-86%, based on lReformationMatrix
            if percentage_chance(
                50 + ((civilization(iCiv).ai.reformation_threshold / 5) * 2) - (iPopBonus / 2),
                strict=True,
            ):
                lCathlist = [
                    Building.CATHOLIC_TEMPLE.value,
                    Building.CATHOLIC_CHAPEL.value,
                    Building.CATHOLIC_MONASTERY.value,
                    Building.CATHOLIC_CATHEDRAL.value,
                    Wonder.MONASTERY_OF_CLUNY.value,
                    Wonder.KRAK_DES_CHEVALIERS.value,
                    Wonder.PALAIS_DES_PAPES.value,
                    Wonder.NOTRE_DAME.value,
                    Wonder.WESTMINSTER.value,
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
                            message(
                                human(),
                                text("TXT_KEY_REFORMATION_PEOPLE_ABANDON_CATHOLICISM_2", CityName),
                                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                color=MessageData.WHITE,
                            )
                        else:
                            message(
                                human(),
                                text("TXT_KEY_REFORMATION_PEOPLE_ABANDON_CATHOLICISM_3", CityName),
                                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                color=MessageData.WHITE,
                            )

    def doCounterReformation(self):
        for iPlayer in range(Civ.POPE.value - 1):
            pPlayer = gc.getPlayer(iPlayer)
            if pPlayer.isAlive() and pPlayer.getStateReligion() == Religion.CATHOLICISM.value:
                if pPlayer.isHuman():
                    self.doCounterReformationHuman(iPlayer)
                elif percentage_chance(
                    civilization(iPlayer).ai.reformation_threshold, strict=True, reverse=True
                ):
                    self.doCounterReformationYes(iPlayer)
                else:
                    self.doCounterReformationNo(iPlayer)
        self.setCounterReformationActive(False)

    def doCounterReformationHuman(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        szMessageYes = (
            text("TXT_KEY_COUNTER_REFORMATION_MESSAGE_YES_1")
            + " +%d " % (max(1, pPlayer.getNumCities() / 3))
            + text("TXT_KEY_COUNTER_REFORMATION_MESSAGE_YES_2")
        )
        szMessageNo = (
            text("TXT_KEY_COUNTER_REFORMATION_MESSAGE_NO_1")
            + " +%d " % (max(1, pPlayer.getNumCities() / 3))
            + text("TXT_KEY_COUNTER_REFORMATION_MESSAGE_NO_2")
        )
        self.showCounterPopup(
            7626,
            text("TXT_KEY_COUNTER_REFORMATION_TITLE"),
            text("TXT_KEY_COUNTER_REFORMATION_MESSAGE"),
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
        iHuman = human()
        if popupReturn.getButtonClicked() == 0:
            self.doCounterReformationYes(iHuman)
        elif popupReturn.getButtonClicked() == 1:
            self.doCounterReformationNo(iHuman)

    def eventApply7628(self, popupReturn):  # Absinthe: persecution popup
        """Persecution popup event."""
        iPlotX, iPlotY, iUnitID = data.lPersecutionData
        iChosenReligion = data.lPersecutionReligions[popupReturn.getButtonClicked()]
        prosecute(iPlotX, iPlotY, iUnitID, iChosenReligion)

    def doCounterReformationYes(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        pCapital = pPlayer.getCapitalCity()
        iX = pCapital.getX()
        iY = pCapital.getY()
        if not pCapital.isNone():
            if pPlayer.getNumCities() > 0:
                pCapital = cities().owner(iPlayer).random_entry()
                iX = pCapital.getX()
                iY = pCapital.getY()
            else:
                return
        iNumProsecutors = max(1, pPlayer.getNumCities() / 3)
        for i in range(iNumProsecutors):
            pPlayer.initUnit(
                Unit.PROSECUTOR.value,
                iX,
                iY,
                UnitAITypes.UNITAI_MISSIONARY,
                DirectionTypes.DIRECTION_SOUTH,
            )

        for neighbour in civilization(iPlayer).location.reformation_neighbours:
            civ = civilization(neighbour)
            if civ.is_alive() and civ.is_protestant():
                if not civ.player.getCapitalCity().isNone() and civ.player.getNumCities() > 0:
                    capital = cities().owner(neighbour).random_entry()
                else:
                    return

                civ.player.initUnit(
                    Unit.PROSECUTOR.value,
                    capital.getX(),
                    capital.getY(),
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
        intolerance = [-1] * civilizations().len()
        for iPlayer in civilizations().ids():
            pPlayer = gc.getPlayer(iPlayer)
            if pPlayer.isAlive():
                if iPlayer < Civ.POPE.value:
                    # add a random element
                    intolerance[iPlayer] += percentage()
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
                    intolerance[iPlayer] += percentage()
        # once we have the list of potential nations
        iCandidate1 = 0
        for iPlayer in civilizations().ids():
            if intolerance[iPlayer] > -1 and intolerance[iPlayer] < intolerance[iCandidate1]:
                iCandidate1 = iPlayer
        iCandidate2 = 0
        if iCandidate2 == iCandidate1:
            iCandidate2 = 1
        for iPlayer in civilizations().ids():
            if (
                intolerance[iPlayer] > -1
                and iPlayer != iCandidate1
                and intolerance[iPlayer] < intolerance[iCandidate1]
            ):
                iCandidate2 = iPlayer

        if percentage_chance(50, strict=True):
            self.migrateJews(iCandidate1)
        else:
            self.migrateJews(iCandidate2)

    def migrateJews(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)

        lCityList = [
            city
            for city in cities().owner(iPlayer).entities()
            if not city.isHasReligion(Religion.JUDAISM.value)
        ]

        if lCityList:
            city = choice(lCityList)
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
