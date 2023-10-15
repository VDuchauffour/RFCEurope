from CvPythonExtensions import *
import Consts
from CoreData import civilizations
from CoreTypes import (
    City,
    Civ,
    Civic,
    Colony,
    Feature,
    PlagueType,
    Promotion,
    Terrain,
    ProvinceTypes,
    Religion,
    Improvement,
    Project,
    UniquePower,
    FaithPointBonusCategory,
)
import XMLConsts as xml
import RFCEMaps
import RFCUtils
from MiscData import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    GREAT_PROPHET_FAITH_POINT_BONUS,
    PROSECUTOR_UNITCLASS,
)
from LocationsData import CITIES
from TimelineData import DateTurn

gc = CyGlobalContext()  # LOQ
utils = RFCUtils.RFCUtils()


class RFCEBalance:
    def setBalanceParameters(self):

        self.preMapsNSizes()
        self.setTechTimeline()  # Timeline for correct tech three

        # 3Miro: consolidate several modifiers into fewer calls, makes it more structured. Each modifier works as described below.

        # void setGrowthModifiers( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop );
        # iInitPop is the initial population in a city, also can use gc.setInitialPopulation( iCiv, iInitPop ) to change a single civ
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100, 1 )
        # 3Miro: ABOUT CULTURE notice the culture modifier is different from the others, it modifies the culture output as opposed to the culture threshold
        # 	50 means less culture, 200 means more culture. This is applied to Culture output of 10 or more.
        gc.setGrowthModifiersAI(Civ.BYZANTIUM.value, 200, 100, 200, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.BYZANTIUM.value, 150, 100, 200, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.FRANCE.value, 110, 100, 110, 100, 100, 1)
        gc.setGrowthModifiersHu(Civ.FRANCE.value, 110, 100, 110, 100, 100, 1)
        gc.setGrowthModifiersAI(Civ.ARABIA.value, 150, 100, 150, 100, 100, 1)
        gc.setGrowthModifiersHu(Civ.ARABIA.value, 150, 100, 150, 100, 100, 1)
        gc.setGrowthModifiersAI(Civ.BULGARIA.value, 150, 100, 100, 100, 100, 1)
        gc.setGrowthModifiersHu(Civ.BULGARIA.value, 125, 100, 100, 100, 100, 1)
        gc.setGrowthModifiersAI(Civ.CORDOBA.value, 150, 100, 100, 100, 100, 1)
        gc.setGrowthModifiersHu(Civ.CORDOBA.value, 150, 100, 100, 100, 100, 1)
        gc.setGrowthModifiersAI(Civ.VENECIA.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.VENECIA.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.BURGUNDY.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.BURGUNDY.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.GERMANY.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.GERMANY.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.NOVGOROD.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.NOVGOROD.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.NORWAY.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.NORWAY.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.KIEV.value, 150, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.KIEV.value, 150, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.HUNGARY.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.HUNGARY.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.CASTILLE.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.CASTILLE.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.DENMARK.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.DENMARK.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.SCOTLAND.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.SCOTLAND.value, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.POLAND.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Civ.POLAND.value, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Civ.GENOA.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.GENOA.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.MOROCCO.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.MOROCCO.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.ENGLAND.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.ENGLAND.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.PORTUGAL.value, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.PORTUGAL.value, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.ARAGON.value, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.ARAGON.value, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.SWEDEN.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.SWEDEN.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.PRUSSIA.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.PRUSSIA.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.LITHUANIA.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.LITHUANIA.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(
            Civ.AUSTRIA.value, 100, 200, 100, 100, 100, 3
        )  # Austria is squashed by other's culture, they need the boost
        gc.setGrowthModifiersHu(Civ.AUSTRIA.value, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.OTTOMAN.value, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.OTTOMAN.value, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.MOSCOW.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Civ.MOSCOW.value, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Civ.DUTCH.value, 100, 200, 60, 100, 50, 4)
        gc.setGrowthModifiersHu(Civ.DUTCH.value, 100, 200, 60, 100, 50, 4)
        gc.setGrowthModifiersAI(Civ.POPE.value, 150, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Civ.INDEPENDENT.value, 100, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Civ.INDEPENDENT_2.value, 100, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Civ.INDEPENDENT_3.value, 100, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Civ.INDEPENDENT_4.value, 100, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Civ.BARBARIAN.value, 100, 100, 100, 50, 100, 1)

        # void setProductionModifiers( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100 )
        # 3Miro: at 100 research cost, the cost is exactly as in the XML files, the cost in general is however increased for all civs
        gc.setProductionModifiersAI(Civ.BYZANTIUM.value, 200, 200, 200, 350)
        gc.setProductionModifiersHu(Civ.BYZANTIUM.value, 200, 150, 200, 350)
        gc.setProductionModifiersAI(Civ.FRANCE.value, 140, 120, 125, 150)
        gc.setProductionModifiersHu(Civ.FRANCE.value, 150, 120, 125, 130)
        gc.setProductionModifiersAI(Civ.ARABIA.value, 130, 125, 150, 280)
        gc.setProductionModifiersHu(Civ.ARABIA.value, 150, 125, 150, 230)
        gc.setProductionModifiersAI(Civ.BULGARIA.value, 130, 125, 125, 250)
        gc.setProductionModifiersHu(Civ.BULGARIA.value, 150, 150, 125, 200)
        gc.setProductionModifiersAI(Civ.CORDOBA.value, 180, 170, 130, 250)
        gc.setProductionModifiersHu(Civ.CORDOBA.value, 200, 180, 140, 230)
        gc.setProductionModifiersAI(Civ.VENECIA.value, 100, 100, 100, 150)
        gc.setProductionModifiersHu(Civ.VENECIA.value, 100, 100, 100, 130)
        gc.setProductionModifiersAI(Civ.BURGUNDY.value, 130, 120, 120, 150)
        gc.setProductionModifiersHu(Civ.BURGUNDY.value, 150, 120, 120, 150)
        gc.setProductionModifiersAI(Civ.GERMANY.value, 120, 120, 100, 140)
        gc.setProductionModifiersHu(Civ.GERMANY.value, 140, 140, 125, 130)
        gc.setProductionModifiersAI(Civ.NOVGOROD.value, 120, 120, 120, 150)
        gc.setProductionModifiersHu(Civ.NOVGOROD.value, 125, 125, 125, 150)
        gc.setProductionModifiersAI(Civ.NORWAY.value, 125, 125, 125, 130)
        gc.setProductionModifiersHu(Civ.NORWAY.value, 125, 125, 100, 140)
        gc.setProductionModifiersAI(Civ.KIEV.value, 100, 120, 100, 140)
        gc.setProductionModifiersHu(Civ.KIEV.value, 125, 150, 125, 150)
        gc.setProductionModifiersAI(Civ.HUNGARY.value, 120, 120, 100, 150)
        gc.setProductionModifiersHu(Civ.HUNGARY.value, 125, 125, 100, 130)
        gc.setProductionModifiersAI(Civ.CASTILLE.value, 100, 100, 100, 130)
        gc.setProductionModifiersHu(Civ.CASTILLE.value, 125, 100, 100, 120)
        gc.setProductionModifiersAI(Civ.DENMARK.value, 100, 100, 100, 110)
        gc.setProductionModifiersHu(Civ.DENMARK.value, 100, 100, 100, 120)
        gc.setProductionModifiersAI(Civ.SCOTLAND.value, 100, 100, 100, 125)
        gc.setProductionModifiersHu(Civ.SCOTLAND.value, 110, 110, 110, 125)
        gc.setProductionModifiersAI(Civ.POLAND.value, 100, 120, 120, 140)
        gc.setProductionModifiersHu(Civ.POLAND.value, 120, 120, 120, 130)
        gc.setProductionModifiersAI(Civ.GENOA.value, 100, 100, 100, 130)
        gc.setProductionModifiersHu(Civ.GENOA.value, 100, 100, 100, 125)
        gc.setProductionModifiersAI(Civ.MOROCCO.value, 120, 120, 120, 175)
        gc.setProductionModifiersHu(Civ.MOROCCO.value, 120, 120, 120, 175)
        gc.setProductionModifiersAI(Civ.ENGLAND.value, 80, 80, 100, 120)
        gc.setProductionModifiersHu(Civ.ENGLAND.value, 100, 100, 100, 110)
        gc.setProductionModifiersAI(Civ.PORTUGAL.value, 70, 90, 100, 110)
        gc.setProductionModifiersHu(Civ.PORTUGAL.value, 80, 90, 100, 100)
        gc.setProductionModifiersAI(Civ.ARAGON.value, 75, 90, 100, 125)
        gc.setProductionModifiersHu(Civ.ARAGON.value, 80, 100, 100, 125)
        gc.setProductionModifiersAI(Civ.SWEDEN.value, 80, 80, 100, 100)
        gc.setProductionModifiersHu(Civ.SWEDEN.value, 80, 80, 100, 100)
        gc.setProductionModifiersAI(Civ.PRUSSIA.value, 60, 80, 120, 90)
        gc.setProductionModifiersHu(Civ.PRUSSIA.value, 75, 80, 120, 100)
        gc.setProductionModifiersAI(Civ.LITHUANIA.value, 70, 100, 110, 110)
        gc.setProductionModifiersHu(Civ.LITHUANIA.value, 80, 100, 110, 100)
        gc.setProductionModifiersAI(Civ.AUSTRIA.value, 50, 80, 100, 80)
        gc.setProductionModifiersHu(Civ.AUSTRIA.value, 80, 80, 100, 100)
        gc.setProductionModifiersAI(Civ.OTTOMAN.value, 60, 75, 100, 120)
        gc.setProductionModifiersHu(Civ.OTTOMAN.value, 75, 75, 100, 110)
        gc.setProductionModifiersAI(Civ.MOSCOW.value, 80, 80, 100, 120)
        gc.setProductionModifiersHu(Civ.MOSCOW.value, 110, 110, 100, 120)
        gc.setProductionModifiersAI(Civ.DUTCH.value, 80, 50, 50, 50)
        gc.setProductionModifiersHu(Civ.DUTCH.value, 90, 50, 60, 50)
        gc.setProductionModifiersAI(Civ.POPE.value, 300, 200, 100, 350)
        gc.setProductionModifiersAI(Civ.INDEPENDENT.value, 170, 100, 400, 200)  # The peaceful ones
        gc.setProductionModifiersAI(
            Civ.INDEPENDENT_2.value, 170, 100, 400, 200
        )  # The peaceful ones
        gc.setProductionModifiersAI(
            Civ.INDEPENDENT_3.value, 125, 100, 600, 300
        )  # The warlike ones
        gc.setProductionModifiersAI(
            Civ.INDEPENDENT_4.value, 125, 100, 600, 300
        )  # The warlike ones
        gc.setProductionModifiersAI(Civ.BARBARIAN.value, 125, 100, 900, 350)

        # void setSupportModifiers( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100 )
        # note that iCityNum also gets an additional modifier based on population in the city
        # note that the base for inflation is modified by turn number (among many other things)
        gc.setSupportModifiersAI(Civ.BYZANTIUM.value, 50, 150, 70, 50, 120)
        gc.setSupportModifiersHu(Civ.BYZANTIUM.value, 50, 150, 70, 50, 120)
        gc.setSupportModifiersAI(Civ.FRANCE.value, 30, 120, 70, 50, 100)
        gc.setSupportModifiersHu(Civ.FRANCE.value, 30, 120, 70, 50, 100)
        gc.setSupportModifiersAI(Civ.ARABIA.value, 30, 150, 70, 40, 120)
        gc.setSupportModifiersHu(Civ.ARABIA.value, 30, 150, 70, 40, 120)
        gc.setSupportModifiersAI(Civ.BULGARIA.value, 40, 150, 80, 50, 120)
        gc.setSupportModifiersHu(Civ.BULGARIA.value, 40, 150, 80, 50, 120)
        gc.setSupportModifiersAI(Civ.CORDOBA.value, 40, 150, 70, 40, 120)
        gc.setSupportModifiersHu(Civ.CORDOBA.value, 40, 150, 70, 40, 120)
        gc.setSupportModifiersAI(Civ.VENECIA.value, 20, 100, 60, 50, 100)
        gc.setSupportModifiersHu(Civ.VENECIA.value, 20, 100, 60, 50, 100)
        gc.setSupportModifiersAI(Civ.BURGUNDY.value, 30, 120, 70, 40, 100)
        gc.setSupportModifiersHu(Civ.BURGUNDY.value, 30, 120, 70, 40, 100)
        gc.setSupportModifiersAI(Civ.GERMANY.value, 20, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Civ.GERMANY.value, 20, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Civ.NOVGOROD.value, 30, 120, 70, 40, 100)
        gc.setSupportModifiersHu(Civ.NOVGOROD.value, 30, 120, 70, 40, 100)
        gc.setSupportModifiersAI(Civ.NORWAY.value, 20, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Civ.NORWAY.value, 20, 100, 60, 40, 100)
        gc.setSupportModifiersAI(Civ.KIEV.value, 30, 120, 60, 40, 100)
        gc.setSupportModifiersHu(Civ.KIEV.value, 30, 120, 60, 40, 100)
        gc.setSupportModifiersAI(Civ.HUNGARY.value, 25, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Civ.HUNGARY.value, 25, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Civ.CASTILLE.value, 20, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Civ.CASTILLE.value, 20, 100, 60, 40, 100)
        gc.setSupportModifiersAI(Civ.DENMARK.value, 20, 100, 80, 50, 100)
        gc.setSupportModifiersHu(Civ.DENMARK.value, 20, 100, 80, 50, 100)
        gc.setSupportModifiersAI(Civ.SCOTLAND.value, 25, 100, 80, 50, 100)
        gc.setSupportModifiersHu(Civ.SCOTLAND.value, 25, 100, 80, 50, 100)
        gc.setSupportModifiersAI(Civ.POLAND.value, 25, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Civ.POLAND.value, 25, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Civ.GENOA.value, 20, 100, 60, 50, 100)
        gc.setSupportModifiersHu(Civ.GENOA.value, 20, 100, 60, 50, 100)
        gc.setSupportModifiersAI(Civ.MOROCCO.value, 25, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Civ.MOROCCO.value, 25, 100, 60, 40, 100)
        gc.setSupportModifiersAI(Civ.ENGLAND.value, 20, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Civ.ENGLAND.value, 20, 100, 60, 40, 100)
        gc.setSupportModifiersAI(Civ.PORTUGAL.value, 20, 100, 70, 50, 100)
        gc.setSupportModifiersHu(Civ.PORTUGAL.value, 20, 100, 70, 50, 100)
        gc.setSupportModifiersAI(Civ.ARAGON.value, 25, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Civ.ARAGON.value, 25, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Civ.SWEDEN.value, 20, 90, 70, 40, 100)
        gc.setSupportModifiersHu(Civ.SWEDEN.value, 20, 90, 70, 40, 100)
        gc.setSupportModifiersAI(Civ.PRUSSIA.value, 20, 90, 70, 40, 100)
        gc.setSupportModifiersHu(Civ.PRUSSIA.value, 20, 90, 70, 40, 100)
        gc.setSupportModifiersAI(Civ.LITHUANIA.value, 25, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Civ.LITHUANIA.value, 25, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Civ.AUSTRIA.value, 20, 80, 80, 40, 100)
        gc.setSupportModifiersHu(Civ.AUSTRIA.value, 20, 80, 80, 40, 100)
        gc.setSupportModifiersAI(Civ.OTTOMAN.value, 30, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Civ.OTTOMAN.value, 30, 100, 60, 40, 100)
        gc.setSupportModifiersAI(
            Civ.MOSCOW.value, 25, 100, 70, 40, 100
        )  # note that the city maintenance values are further modified by their UP
        gc.setSupportModifiersHu(
            Civ.MOSCOW.value, 25, 100, 70, 40, 100
        )  # note that the city maintenance values are further modified by their UP
        gc.setSupportModifiersAI(Civ.DUTCH.value, 20, 70, 80, 50, 100)
        gc.setSupportModifiersHu(Civ.DUTCH.value, 20, 70, 80, 50, 100)
        gc.setSupportModifiersAI(Civ.POPE.value, 20, 150, 80, 50, 100)
        gc.setSupportModifiersAI(Civ.INDEPENDENT.value, 10, 100, 10, 20, 100)
        gc.setSupportModifiersAI(Civ.INDEPENDENT_2.value, 10, 100, 10, 20, 100)
        gc.setSupportModifiersAI(Civ.INDEPENDENT_3.value, 10, 100, 10, 20, 100)
        gc.setSupportModifiersAI(Civ.INDEPENDENT_4.value, 10, 100, 10, 20, 100)
        gc.setSupportModifiersAI(Civ.BARBARIAN.value, 10, 250, 10, 20, 100)

        # 3Miro: setGrowthTreshold(iCiv,iVal), for each civ, a value in percent. How much food is needed for the next growth level.
        # in c++, iTreshold *= value, iTreshlod /= 100 (value is in percent, with integer truncation, default 100)
        # low percent means faster growth

        # 3Miro: setProductionModifiersUnits(iCiv,iVal) for each civ. Same as growth.
        # on all production, low percent means fast production

        # 3Miro: setProductionModifiersBuildings(iCiv,iVal) for each civ. Same as growth.

        # 3Miro: setProductionModifiersWonders(iCiv,iVal) for each civ. Same as growth.

        # 3Miro: setInflationModifier(iCiv,iVal) for each civ. Same as growth.
        # low percent means low inflation

        # 3Miro: setGPModifier(iCiv,iVal) for each civ. The rate at which GP would appear. Same as growth.
        # low percent means faster GP rate

        # 3Miro: setUnitSupportModifier(iCiv, iVal), set unit support modifiers for the player. Same as growth.
        # low percent means lower support cost)

        # 3Miro: setDistanceSupportModifier(iCiv,iVal), set modifiers for the distance to the capital support. Same as growth.
        # low percent means low cost

        # 3Miro: setNumberOfCitiesSupport(iCiv,iVal), set number of cities modifier. Same as growth
        # low percent means low cost

        # 3Miro: setCivicSupportModifier(iCiv,iVal), set the civic support modifiers. Same as growth.
        # low percent means low cost

        # 3Miro: setResearchModifier(iCiv, iVal), set research modifier for all the civs. Same as growth.
        # low percent means faster research

        # 3Miro: setHealthModifier(iCiv,iVal), multiply the health modifier for the difficulty level by iVal

        # 3Miro: setWorkerModifier(iCiv,iVal), modify the rate at witch workers build improvements. Not the same as growth.
        # higher number, faster workers

        # 3Miro: setCultureModifier(iCiv, iVal ), modify culture if the city makes more than 4 (especially low for Indeps and Barbs)
        # Same as growth. higher number more culture

        ##### Set Initial buildings for the civs
        # gc.setInitialBuilding( iCiv, iBuilding, True\False ), if ( True) give iCiv, building iBuildings else don't Default is False
        # we can change True <-> False with the onTechAquire event

        gc.setInitialBuilding(Civ.VENECIA.value, xml.iHarbor, True)
        gc.setInitialBuilding(Civ.VENECIA.value, xml.iGranary, True)

        gc.setInitialBuilding(Civ.CASTILLE.value, xml.iBarracks, True)

        gc.setInitialBuilding(Civ.DENMARK.value, xml.iBarracks, True)

        gc.setInitialBuilding(Civ.SCOTLAND.value, xml.iBarracks, True)

        gc.setInitialBuilding(Civ.MOSCOW.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.MOSCOW.value, xml.iBarracks, True)
        gc.setInitialBuilding(Civ.MOSCOW.value, xml.iForge, True)
        gc.setInitialBuilding(Civ.MOSCOW.value, xml.iMarket, True)

        gc.setInitialBuilding(Civ.GENOA.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.GENOA.value, xml.iBarracks, True)
        gc.setInitialBuilding(Civ.GENOA.value, xml.iHarbor, True)

        gc.setInitialBuilding(Civ.MOROCCO.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.MOROCCO.value, xml.iBarracks, True)

        gc.setInitialBuilding(Civ.ENGLAND.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.ENGLAND.value, xml.iBarracks, True)

        gc.setInitialBuilding(Civ.PORTUGAL.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.PORTUGAL.value, xml.iBarracks, True)

        gc.setInitialBuilding(Civ.ARAGON.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.ARAGON.value, xml.iBarracks, True)
        gc.setInitialBuilding(Civ.ARAGON.value, xml.iHarbor, True)

        gc.setInitialBuilding(Civ.PRUSSIA.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.PRUSSIA.value, xml.iBarracks, True)

        gc.setInitialBuilding(Civ.LITHUANIA.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.LITHUANIA.value, xml.iBarracks, True)

        gc.setInitialBuilding(Civ.AUSTRIA.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.AUSTRIA.value, xml.iBarracks, True)
        gc.setInitialBuilding(Civ.AUSTRIA.value, xml.iForge, True)

        gc.setInitialBuilding(Civ.OTTOMAN.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.OTTOMAN.value, xml.iBarracks, True)
        gc.setInitialBuilding(Civ.OTTOMAN.value, xml.iForge, True)
        gc.setInitialBuilding(Civ.OTTOMAN.value, xml.iHarbor, True)

        gc.setInitialBuilding(Civ.SWEDEN.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.SWEDEN.value, xml.iBarracks, True)
        gc.setInitialBuilding(Civ.SWEDEN.value, xml.iHarbor, True)

        gc.setInitialBuilding(Civ.DUTCH.value, xml.iGranary, True)
        gc.setInitialBuilding(Civ.DUTCH.value, xml.iBarracks, True)
        gc.setInitialBuilding(Civ.DUTCH.value, xml.iForge, True)
        gc.setInitialBuilding(Civ.DUTCH.value, xml.iHarbor, True)
        gc.setInitialBuilding(Civ.DUTCH.value, xml.iAqueduct, True)
        gc.setInitialBuilding(Civ.DUTCH.value, xml.iMarket, True)
        gc.setInitialBuilding(Civ.DUTCH.value, xml.iLighthouse, True)
        gc.setInitialBuilding(Civ.DUTCH.value, xml.iTheatre, True)
        gc.setInitialBuilding(Civ.DUTCH.value, xml.iSmokehouse, True)

        ####### AI Modifiers
        # 3Miro: setCityClusterAI(iCiv,iTop,iBottom,iMinus) for each AI civilization (set them for all, but only the AI make difference)
        # this determines how clustered the cities would be
        # AI_foundValue in PlayerAI would compute for a candidate city location the number of plots that are taken (i.e. by another city)
        # in CivIV, if more than a third of the tiles are "taken", do not found city there. In RFC, cities are clustered closer
        # if ( iTaken > 21 * iTop / iBottom - iMinus ) do not build city there.
        # RFC default values are 2/3 -1 for Europe, 1/3 - 0 for Russia and 1/2 for Mongolia
        # for example gc.setCityClusterAI( iByzantium, 1, 3, 0 ) wouldn't allow Byzantium to settle cities if more than 7 tiles are taken
        gc.setCityClusterAI(Civ.BYZANTIUM.value, 1, 3, 0)  # won't settle if 8+ tiles are taken
        gc.setCityClusterAI(Civ.FRANCE.value, 1, 3, 0)  # 8
        gc.setCityClusterAI(Civ.ARABIA.value, 1, 3, 1)  # 7
        gc.setCityClusterAI(Civ.BULGARIA.value, 2, 3, 4)  # 11
        gc.setCityClusterAI(Civ.CORDOBA.value, 1, 2, 1)  # 10
        gc.setCityClusterAI(Civ.VENECIA.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.BURGUNDY.value, 2, 3, 3)  # 12
        gc.setCityClusterAI(Civ.GERMANY.value, 2, 3, 4)  # 11
        gc.setCityClusterAI(Civ.NOVGOROD.value, 1, 3, 2)  # 6
        gc.setCityClusterAI(Civ.NORWAY.value, 1, 2, 1)  # 10
        gc.setCityClusterAI(Civ.KIEV.value, 1, 3, 2)  # 6
        gc.setCityClusterAI(Civ.HUNGARY.value, 2, 3, 3)  # 12
        gc.setCityClusterAI(Civ.CASTILLE.value, 1, 2, 1)  # 10
        gc.setCityClusterAI(Civ.DENMARK.value, 2, 3, 3)  # 12
        gc.setCityClusterAI(Civ.SCOTLAND.value, 2, 3, 2)  # 13
        gc.setCityClusterAI(Civ.POLAND.value, 1, 3, 0)  # 8
        gc.setCityClusterAI(Civ.GENOA.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.MOROCCO.value, 1, 3, 2)  # 6
        gc.setCityClusterAI(Civ.ENGLAND.value, 1, 2, 1)  # 10
        gc.setCityClusterAI(Civ.PORTUGAL.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.ARAGON.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.SWEDEN.value, 1, 2, 2)  # 9
        gc.setCityClusterAI(Civ.PRUSSIA.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.LITHUANIA.value, 1, 3, 0)  # 8
        gc.setCityClusterAI(Civ.AUSTRIA.value, 2, 3, 3)  # 12
        gc.setCityClusterAI(Civ.OTTOMAN.value, 1, 3, 1)  # 7
        gc.setCityClusterAI(Civ.MOSCOW.value, 1, 4, 1)  # 5
        gc.setCityClusterAI(Civ.DUTCH.value, 2, 3, 1)  # 14

        # 3Miro: setCityWarDistanceAI(iCiv,iVal), depending on the type of the empire, modify how likely the AI is to attack a city
        # values are 1 - small empires, 2 - large continuous empires, 3 - not necessarily continuous empires
        gc.setCityWarDistanceAI(Civ.BYZANTIUM.value, 2)
        gc.setCityWarDistanceAI(Civ.FRANCE.value, 2)
        gc.setCityWarDistanceAI(Civ.ARABIA.value, 2)
        gc.setCityWarDistanceAI(Civ.BULGARIA.value, 1)
        gc.setCityWarDistanceAI(Civ.CORDOBA.value, 2)
        gc.setCityWarDistanceAI(Civ.VENECIA.value, 3)
        gc.setCityWarDistanceAI(Civ.BURGUNDY.value, 1)
        gc.setCityWarDistanceAI(Civ.GERMANY.value, 2)
        gc.setCityWarDistanceAI(Civ.NOVGOROD.value, 2)
        gc.setCityWarDistanceAI(Civ.NORWAY.value, 3)
        gc.setCityWarDistanceAI(Civ.KIEV.value, 2)
        gc.setCityWarDistanceAI(Civ.HUNGARY.value, 2)
        gc.setCityWarDistanceAI(Civ.CASTILLE.value, 3)
        gc.setCityWarDistanceAI(Civ.DENMARK.value, 2)
        gc.setCityWarDistanceAI(Civ.SCOTLAND.value, 1)
        gc.setCityWarDistanceAI(Civ.POLAND.value, 2)
        gc.setCityWarDistanceAI(Civ.GENOA.value, 3)
        gc.setCityWarDistanceAI(Civ.MOROCCO.value, 2)
        gc.setCityWarDistanceAI(Civ.ENGLAND.value, 3)
        gc.setCityWarDistanceAI(Civ.PORTUGAL.value, 3)
        gc.setCityWarDistanceAI(Civ.ARAGON.value, 3)
        gc.setCityWarDistanceAI(Civ.SWEDEN.value, 3)
        gc.setCityWarDistanceAI(Civ.PRUSSIA.value, 2)
        gc.setCityWarDistanceAI(Civ.LITHUANIA.value, 2)
        gc.setCityWarDistanceAI(Civ.AUSTRIA.value, 2)
        gc.setCityWarDistanceAI(Civ.OTTOMAN.value, 2)
        gc.setCityWarDistanceAI(Civ.MOSCOW.value, 2)
        gc.setCityWarDistanceAI(Civ.DUTCH.value, 1)

        # 3Miro: setTechPreferenceAI(iCiv,iTech,iVal), for each civ, for each tech, specify how likable it is. iVal is same as in growth.
        # low percent makes the tech less desirable
        gc.setTechPreferenceAI(Civ.BULGARIA.value, xml.iBronzeCasting, 200)
        gc.setTechPreferenceAI(Civ.GERMANY.value, xml.iPrintingPress, 200)
        gc.setTechPreferenceAI(Civ.ENGLAND.value, xml.iPrintingPress, 150)
        gc.setTechPreferenceAI(Civ.POPE.value, xml.iPrintingPress, 10)  # Pope shouldn't want this
        gc.setTechPreferenceAI(Civ.CASTILLE.value, xml.iAstronomy, 200)
        gc.setTechPreferenceAI(Civ.PORTUGAL.value, xml.iAstronomy, 200)

        # 3Miro: setDiplomacyModifiers(iCiv1,iCiv2,iVal) hidden modifier for the two civ's AI relations. More likely to have OB and so on.
        # + means they will like each other - they will hate each other.
        # from Civ1 towards Civ2 (make them symmetric)
        gc.setDiplomacyModifiers(Civ.CORDOBA.value, Civ.ARABIA.value, +5)
        gc.setDiplomacyModifiers(Civ.ARABIA.value, Civ.CORDOBA.value, +5)
        gc.setDiplomacyModifiers(Civ.ARABIA.value, Civ.BYZANTIUM.value, -8)
        gc.setDiplomacyModifiers(Civ.BYZANTIUM.value, Civ.ARABIA.value, -8)
        gc.setDiplomacyModifiers(Civ.BULGARIA.value, Civ.BYZANTIUM.value, +3)
        gc.setDiplomacyModifiers(Civ.BYZANTIUM.value, Civ.BULGARIA.value, +3)
        gc.setDiplomacyModifiers(Civ.CORDOBA.value, Civ.CASTILLE.value, -14)
        gc.setDiplomacyModifiers(Civ.CASTILLE.value, Civ.CORDOBA.value, -14)
        gc.setDiplomacyModifiers(Civ.MOROCCO.value, Civ.CASTILLE.value, -10)
        gc.setDiplomacyModifiers(Civ.CASTILLE.value, Civ.MOROCCO.value, -10)
        gc.setDiplomacyModifiers(Civ.ARAGON.value, Civ.CASTILLE.value, +4)
        gc.setDiplomacyModifiers(Civ.CASTILLE.value, Civ.ARAGON.value, +4)
        gc.setDiplomacyModifiers(Civ.PORTUGAL.value, Civ.CASTILLE.value, +6)
        gc.setDiplomacyModifiers(Civ.CASTILLE.value, Civ.PORTUGAL.value, +6)
        gc.setDiplomacyModifiers(Civ.CORDOBA.value, Civ.PORTUGAL.value, -8)
        gc.setDiplomacyModifiers(Civ.PORTUGAL.value, Civ.CORDOBA.value, -8)
        gc.setDiplomacyModifiers(Civ.KIEV.value, Civ.NOVGOROD.value, +5)
        gc.setDiplomacyModifiers(Civ.NOVGOROD.value, Civ.KIEV.value, +5)
        gc.setDiplomacyModifiers(Civ.MOSCOW.value, Civ.NOVGOROD.value, -8)
        gc.setDiplomacyModifiers(Civ.NOVGOROD.value, Civ.MOSCOW.value, -8)
        gc.setDiplomacyModifiers(Civ.FRANCE.value, Civ.BURGUNDY.value, -2)
        gc.setDiplomacyModifiers(Civ.BURGUNDY.value, Civ.FRANCE.value, -2)
        gc.setDiplomacyModifiers(Civ.OTTOMAN.value, Civ.BYZANTIUM.value, -14)
        gc.setDiplomacyModifiers(Civ.BYZANTIUM.value, Civ.OTTOMAN.value, -14)
        gc.setDiplomacyModifiers(Civ.GERMANY.value, Civ.POLAND.value, -5)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.GERMANY.value, -5)
        gc.setDiplomacyModifiers(Civ.MOSCOW.value, Civ.POLAND.value, -4)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.MOSCOW.value, -4)
        gc.setDiplomacyModifiers(Civ.MOSCOW.value, Civ.LITHUANIA.value, -2)
        gc.setDiplomacyModifiers(Civ.LITHUANIA.value, Civ.MOSCOW.value, -2)
        gc.setDiplomacyModifiers(Civ.AUSTRIA.value, Civ.POLAND.value, -2)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.AUSTRIA.value, -2)
        gc.setDiplomacyModifiers(Civ.LITHUANIA.value, Civ.POLAND.value, +4)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.LITHUANIA.value, +4)
        gc.setDiplomacyModifiers(Civ.HUNGARY.value, Civ.POLAND.value, +3)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.HUNGARY.value, +3)
        gc.setDiplomacyModifiers(Civ.AUSTRIA.value, Civ.HUNGARY.value, -6)
        gc.setDiplomacyModifiers(Civ.HUNGARY.value, Civ.AUSTRIA.value, -6)
        gc.setDiplomacyModifiers(Civ.SWEDEN.value, Civ.POLAND.value, -2)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.SWEDEN.value, -2)
        gc.setDiplomacyModifiers(Civ.SWEDEN.value, Civ.MOSCOW.value, -8)
        gc.setDiplomacyModifiers(Civ.MOSCOW.value, Civ.SWEDEN.value, -8)
        gc.setDiplomacyModifiers(Civ.PRUSSIA.value, Civ.POLAND.value, -6)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.PRUSSIA.value, -6)
        gc.setDiplomacyModifiers(Civ.PRUSSIA.value, Civ.LITHUANIA.value, -8)
        gc.setDiplomacyModifiers(Civ.LITHUANIA.value, Civ.PRUSSIA.value, -8)
        gc.setDiplomacyModifiers(Civ.ENGLAND.value, Civ.SCOTLAND.value, -8)
        gc.setDiplomacyModifiers(Civ.SCOTLAND.value, Civ.ENGLAND.value, -8)
        gc.setDiplomacyModifiers(Civ.FRANCE.value, Civ.SCOTLAND.value, +4)
        gc.setDiplomacyModifiers(Civ.SCOTLAND.value, Civ.FRANCE.value, +4)
        gc.setDiplomacyModifiers(Civ.NORWAY.value, Civ.DENMARK.value, +4)
        gc.setDiplomacyModifiers(Civ.DENMARK.value, Civ.NORWAY.value, +4)
        gc.setDiplomacyModifiers(Civ.SWEDEN.value, Civ.DENMARK.value, -4)
        gc.setDiplomacyModifiers(Civ.DENMARK.value, Civ.SWEDEN.value, -4)

        ####### 3Miro: UNIQUE POWERS
        # 3Miro: setUP(iCiv,iPower) sets the Unique Powers for C++

        # 3Miro: setUP(iCiv,iPower,iParameter)
        # iUP_Happiness, iParameter = the amount of additional happiness
        # iUP_PerCityCommerce, iParameter = 1000000 * bonus_in_gold + 10000*bonus_in_research + 100*bonus_in_culture + bonus_in_espionage (bonuses are limited to 0 - 99)
        # iUP_CommercePercent, iParameter = 1000000 * bonus_in_gold + 10000*bonus_in_research + 100*bonus_in_culture + bonus_in_espionage (bonuses are limited to 0 - 99 percent)
        # iUP_CulturalTolerance, iParameter = 0 for no unhappiness or iParameter = k for unhappiness = unhappiness / k
        # iUP_ReligiousTolerance, iParameter = 0 for no instability
        # iUP_Conscription, iParameter = percent of foreign culture needed to draft + 100 * max number of units to draft per turn
        # iUP_NoResistance, iParameter = 0 for no resistance or iParameter = k for resistance turns = resistance turns / k
        # iUP_UnitProduction, iParameter = iRequiredTech * 100 + Percent ( 75% for 25% faster unit building)
        # iUP_EnableCivics, iParameter = Civic5 * 100000000 + Civic4 * 1000000 + Civic3 * 10000 + Civic2 * 100 + Civic1, NOTE: also need to enable this in the WB, civic indexed by 0 is always available, civic5 cannot be bigger than 20
        # iUP_TradeRoutes, iParameter = number of extra trade routes, NOTE: this must be synchronized with GlobalDefines.xml: max trade routes
        # iUP_PromotionI, iParameter = the bonus promotion
        # iUP_PromotionII, iParameter = the bonus promotion
        # iUP_Inquisition, iParameter is not used
        # iUP_CanEnterTerrain, iParameter is the terrain to enter, NOTE: also enables trade through the given terrain type
        # iUP_Discovery, iParameter = ColonyStart * 1000000 + ColonyEnd * 1000 + iModifier modifies the cost associated with all projects (iCost *= iModifier; iCost /= 100 )
        # iUP_EndlessLand, iParameter = percent change (i.e. upkeep *= iParameter, upkeep /= 100 )
        # iUP_ForeignSea, use iParameter = 1 to activate
        # iUP_Pious, whenever changeFaith( x ) is called, x is multiplied by iParameter
        # iUP_HealthFood, iParameter = percentage, what ratio of the city's excess health should be converted into food
        # iUP_TerrainBonus, iParameter = iActivate * 100000 (1 to be active) + iTerrain * 1000 + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus (bonuses are limited to 0-9)
        # iUP_FeatureBonus, iParameter = iActivate * 100000 (1 to be active) + iFeature * 1000 + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus (bonuses are limited to 0-9)
        # iUP_ImprovementBonus, iParameter = iActivate * 100000 (1 to be active) + iImprovement * 1000 + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus (bonuses are limited to 0-9)
        # iUP_CityTileYield, iParameter = iActivate * 1000 (1 to be active) + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus, (bonuses are limited to 0-9)

        gc.setUP(Civ.BURGUNDY.value, UniquePower.HAPPINESS_BONUS.value, 1)
        gc.setUP(Civ.BURGUNDY.value, UniquePower.PER_CITY_COMMERCE_BONUS.value, 200)

        gc.setUP(Civ.BYZANTIUM.value, UniquePower.NO_COLLAPSE_IN_CORE_AND_NORMAL_AREAS.value, 1)
        gc.setUP(Civ.BYZANTIUM.value, UniquePower.PRE_ACCESS_CIVICS.value, Civic.IMPERIALISM.value)

        gc.setUP(Civ.FRANCE.value, UniquePower.LESS_INSTABILITY_WITH_FOREIGN_LAND.value, 1)

        gc.setUP(Civ.ARABIA.value, UniquePower.SPREAD_STATE_RELIGION_TO_NEW_CITIES.value, 1)

        gc.setUP(Civ.BULGARIA.value, UniquePower.NO_RESISTANCE.value, 0)

        gc.setUP(
            Civ.CORDOBA.value,
            UniquePower.PROMOTION_FOR_ALL_VALID_UNITS.value,
            Promotion.MEDIC.value,
        )
        gc.setUP(Civ.CORDOBA.value, UniquePower.GROWTH_CITY_WITH_HEALTH_EXCESS.value, 50)

        gc.setUP(
            Civ.MOROCCO.value,
            UniquePower.TERRAIN_BONUS.value,
            1 * 100000 + Terrain.DESERT.value * 1000 + 10 + 1,
        )
        gc.setUP(
            Civ.MOROCCO.value,
            UniquePower.FEATURE_BONUS.value,
            1 * 100000 + Feature.OASIS.value * 1000 + 100 + 1,
        )

        gc.setUP(
            Civ.CASTILLE.value, UniquePower.LESS_INSTABILITY_WITH_RELIGIOUS_PROSECUTION.value, 1
        )
        gc.setUP(Civ.CASTILLE.value, UniquePower.PER_CITY_COMMERCE_BONUS.value, 2)

        gc.setUP(Civ.NORWAY.value, UniquePower.CAN_ENTER_TERRAIN.value, Terrain.OCEAN.value)
        gc.setUP(
            Civ.NORWAY.value, UniquePower.STABILITY_BONUS_FOUNDING.value, 1
        )  # "hidden" part of the UP

        gc.setUP(
            Civ.VENECIA.value, UniquePower.PRE_ACCESS_CIVICS.value, Civic.MERCHANT_REPUBLIC.value
        )
        # gc.setUP( iVenecia, UniquePower.ALLOW_SHIPS_IN_FOREIGN_SEA.value, 1 )

        gc.setUP(Civ.KIEV.value, UniquePower.CITY_TILE_YIELD_BONUS.value, 1 * 1000 + 100 * 2)

        gc.setUP(Civ.HUNGARY.value, UniquePower.HAPPINESS_BONUS.value, 1)
        gc.setUP(Civ.HUNGARY.value, UniquePower.NO_UNHAPPINESS_WITH_FOREIGN_CULTURE.value, 0)

        gc.setUP(
            Civ.GERMANY.value, UniquePower.FASTER_UNIT_PRODUCTION.value, xml.iGunpowder * 100 + 75
        )

        gc.setUP(Civ.POLAND.value, UniquePower.NO_INSTABILITY_WITH_FOREIGN_RELIGION.value, 0)

        gc.setUP(Civ.LITHUANIA.value, UniquePower.CULTURE_BONUS_WITH_NO_STATE_RELIGION.value, 200)
        gc.setUP(Civ.LITHUANIA.value, UniquePower.HAPPINESS_BONUS_WITH_NO_STATE_RELIGION.value, 1)

        gc.setSupportModifiersAI(Civ.MOSCOW.value, 10, 100, 20, 10, 100)  # sync with preset values
        gc.setSupportModifiersHu(Civ.MOSCOW.value, 10, 100, 20, 10, 100)  # sync with preset values
        gc.setUP(Civ.MOSCOW.value, UniquePower.LOWER_CITY_MAINTENANCE_COST.value, 50)

        gc.setUP(
            Civ.GENOA.value, UniquePower.HALVE_COST_OF_MERCENARIES.value, 1
        )  # Absinthe: this actually has no effect, it is implemented in Mercenaries.py entirely

        gc.setUP(
            Civ.SCOTLAND.value,
            UniquePower.IMPROVEMENT_BONUS.value,
            1 * 100000 + Improvement.FORT.value * 1000 + 2,
        )

        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS.value,
            1 * 100000 + Improvement.WORKSHOP.value * 1000 + 1,
        )
        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS_2.value,
            1 * 100000 + Improvement.COTTAGE.value * 1000 + 10,
        )
        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS_3.value,
            1 * 100000 + Improvement.HAMLET.value * 1000 + 10,
        )
        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS_4.value,
            1 * 100000 + Improvement.VILLAGE.value * 1000 + 10,
        )
        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS_5.value,
            1 * 100000 + Improvement.TOWN.value * 1000 + 10,
        )

        # Speed up East/West India Trading Companies and all Colonies
        gc.setUP(
            Civ.PORTUGAL.value,
            UniquePower.LOWER_COST_FOR_PROJECTS.value,
            (len(Project) - 2) * 1000000 + max(Colony) * 1000 + 30,
        )
        gc.setUP(
            Civ.PORTUGAL.value, UniquePower.STABILITY_BONUS_FOUNDING.value, 1
        )  # "hidden" part of the UP

        for i in civilizations().drop(Civ.BARBARIAN).ids():
            if not i == Civ.AUSTRIA.value:
                gc.setDiplomacyModifiers(i, Civ.AUSTRIA.value, +4)
        gc.setUP(Civ.AUSTRIA.value, UniquePower.PER_CITY_COMMERCE_BONUS.value, 200)

        # gc.setUP( iTurkey, UniquePower.CONSCRIPTION.value, 330 )
        # gc.setUP( iTurkey, UniquePower.CONSCRIPTION.value, 1 )
        gc.setUP(Civ.OTTOMAN.value, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS.value, 1)

        gc.setUP(
            Civ.SWEDEN.value,
            UniquePower.PROMOTION_FOR_ALL_VALID_UNITS.value,
            Promotion.FORMATION.value,
        )

        gc.setUP(Civ.NOVGOROD.value, UniquePower.PRE_ACCESS_CIVICS.value, Civic.BUREAUCRACY.value)

        gc.setUP(Civ.PRUSSIA.value, UniquePower.PRE_ACCESS_CIVICS.value, Civic.THEOCRACY.value)
        # Absinthe: handled in python currently
        # gc.setUP( iPrussia, UniquePower.NO_INSTABILITY_WITH_CIVIC_AND_STATE_RELIGION_CHANGE.value, 1 )

        # Absinthe: handled in python currently
        # gc.setUP( iAragon, UniquePower.EXTRA_COMMERCE_BONUS.value, 0 )

        # Absinthe: handled in python currently
        # gc.setUP( iScotland, UniquePower.EXTRA_UNITS_WHEN_LOSING_CITY.value, 1 )

        gc.setUP(Civ.DUTCH.value, UniquePower.EXTRA_TRADE_ROUTES.value, 2)
        gc.setUP(
            Civ.DUTCH.value, UniquePower.IMPROVE_GAIN_FAITH_POINTS.value, 2
        )  # 3Miro: "hidden" buff to the Dutch FP, otherwise they have too little piety (not enough cities)
        gc.setUP(
            Civ.DUTCH.value,
            UniquePower.LOWER_COST_FOR_PROJECTS.value,
            (len(Project) - 2) * 1000000 + max(Colony) * 1000 + 30,
        )  # "hidden" part of the UP

        gc.setUP(Civ.POPE.value, UniquePower.NO_COLLAPSE_IN_CORE_AND_NORMAL_AREAS.value, 1)

        # GlobalWarming
        gc.setGlobalWarming(False)

        # Set FastTerrain (i.e. double movement over ocean)
        gc.setFastTerrain(Terrain.OCEAN.value)

        # set religious spread factors
        for civ in civilizations():
            for religion, threshold in civ.religion.spreading_threshold.items():
                gc.setReligionSpread(
                    civ.id,
                    religion.value,
                    threshold,
                )

        # set the religions and year of the great schism
        gc.setSchism(Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, DateTurn.i1053AD)

        gc.setHoliestCity(*CITIES[City.JERUSALEM].to_tuple())

        # 3Miro: Faith Points benefits
        # gc.setReligionBenefit( iReligion, iFP_(whatever it is), iParameter, iCap )
        # 	note that for powers iParameter = -1 means that this religion doesn't have this power (-1 is the default)
        # 	iCap sets a cap for the maximum number of FP a religion can have (per player) Can be adjusted per Player
        #
        # iFP_Stability: stability += iParameter * num_FaithPoints / 100
        # 		 i.e. 1 Faith Point = iParameter percent of a stability point
        # iFP_Civic: civic_upkeep *= 100 - (num_FaithPoints * iParameter) / 100
        # 		civic_upkeep /= 100
        # 		iParameter = 200, means 2% lower cost per Faith Point, iParameter = 50 means .5% lower cost per FP
        # iFP_Growth: iTreshhold *= 100 - (num_FaithPoints * iParameter) / 100
        # 		iTreshhold /= 100
        # 		iParameter = 200, means 2% faster growth per Faith Point, iParameter = 50 means .5% faster growth per FP
        # iFP_Units: iProductionNeeded *= 100 - (num_FaithPoints * iParameter) / 100
        # 		iProductionNeeded /= 100
        # 		iParameter = 200, means 2% faster production per Faith Point, iParameter = 50 means .5% faster production per FP
        # iFP_Science: same as units, iParameter = 200, means 2% lower tech cost per Faith Point, iParameter = 50 means .5% lower tech cost per FP
        # iFP_Production: iProductionNeeded *= 100 - (num_FaithPoints * iParameter) / 100
        # 		iProductionNeeded /= 100
        # 		iParameter = 200, means 2% faster production per Faith Point, iParameter = 50 means .5% faster production per FP
        # 		Counts for Wonders and Projects
        # iFP_Diplomacy: iAttitude += iParameter * num_FaithPoints / 100
        # 		i.e. 1 Faith Point = iParameter percent of an attitude point

        gc.setReligionBenefit(
            Religion.ORTHODOXY.value, FaithPointBonusCategory.BOOST_STABILITY.value, 10, 100
        )
        gc.setReligionBenefit(
            Religion.ORTHODOXY.value, FaithPointBonusCategory.REDUCE_CIVIC_UPKEEP.value, 50, 100
        )

        gc.setReligionBenefit(
            Religion.ISLAM.value, FaithPointBonusCategory.FASTER_POPULATION_GROWTH.value, 50, 100
        )
        gc.setReligionBenefit(
            Religion.ISLAM.value, FaithPointBonusCategory.REDUCING_COST_UNITS.value, 50, 100
        )

        gc.setReligionBenefit(
            Religion.PROTESTANTISM.value, FaithPointBonusCategory.REDUCING_TECH_COST.value, 30, 100
        )
        gc.setReligionBenefit(
            Religion.PROTESTANTISM.value,
            FaithPointBonusCategory.REDUCING_WONDER_COST.value,
            30,
            100,
        )

        gc.setReligionBenefit(
            Religion.CATHOLICISM.value, FaithPointBonusCategory.BOOST_DIPLOMACY.value, 6, 100
        )
        gc.setReligionBenefit(
            Religion.ISLAM.value, FaithPointBonusCategory.BOOST_DIPLOMACY.value, 5, 100
        )
        gc.setReligionBenefit(
            Religion.PROTESTANTISM.value, FaithPointBonusCategory.BOOST_DIPLOMACY.value, 4, 100
        )
        gc.setReligionBenefit(
            Religion.ORTHODOXY.value, FaithPointBonusCategory.BOOST_DIPLOMACY.value, 3, 100
        )

        # a land tile that is normally impassable but the desired player can pass through it
        # gc.setStrategicTile( iVenecia, 56, 35 )

        # set AI modifiers for preferred buildings
        # use values -10 for very unlikely, 0 for default neutral and positive for desirable
        # values less than -10 might not work, above 10 should be fine

        # the utils.getUniqueBuilding function does not work, probably the util functions are not yet usable when these initial values are set
        # but in the .dll these values are only used for the civ-specific building of the given buildingclass, so we can these add redundantly
        for iPlayer in civilizations().majors().ids():
            # walls, kasbah
            gc.setBuildingPref(iPlayer, xml.iWalls, 5)
            gc.setBuildingPref(iPlayer, xml.iMoroccoKasbah, 5)
            # castle, stronghold, citadel, kremlin
            gc.setBuildingPref(iPlayer, xml.iCastle, 7)
            gc.setBuildingPref(iPlayer, xml.iMoscowKremlin, 7)
            gc.setBuildingPref(iPlayer, xml.iHungarianStronghold, 7)
            gc.setBuildingPref(iPlayer, xml.iSpanishCitadel, 7)
            # manor house, chateau, naval base
            gc.setBuildingPref(iPlayer, xml.iManorHouse, 5)
            gc.setBuildingPref(iPlayer, xml.iFrenchChateau, 5)
            gc.setBuildingPref(iPlayer, xml.iVeniceNavalBase, 5)
            # courthouse, rathaus, veche, voivodeship
            gc.setBuildingPref(iPlayer, xml.iCourthouse, 5)
            gc.setBuildingPref(iPlayer, xml.iKievVeche, 5)
            gc.setBuildingPref(iPlayer, xml.iHolyRomanRathaus, 5)
            gc.setBuildingPref(iPlayer, xml.iLithuanianVoivodeship, 5)
            # nightwatch, soldattorp
            gc.setBuildingPref(iPlayer, xml.iNightWatch, 3)
            gc.setBuildingPref(iPlayer, xml.iSwedishTennant, 3)

        gc.setBuildingPref(Civ.BYZANTIUM.value, xml.iStCatherineMonastery, 15)
        gc.setBuildingPref(Civ.BYZANTIUM.value, xml.iBoyanaChurch, 2)
        gc.setBuildingPref(Civ.BYZANTIUM.value, xml.iRoundChurch, 2)
        gc.setBuildingPref(Civ.BYZANTIUM.value, xml.iSophiaKiev, 5)

        gc.setBuildingPref(Civ.FRANCE.value, xml.iNotreDame, 20)
        gc.setBuildingPref(Civ.FRANCE.value, xml.iVersailles, 20)
        gc.setBuildingPref(Civ.FRANCE.value, xml.iFontainebleau, 10)
        gc.setBuildingPref(Civ.FRANCE.value, xml.iMonasteryOfCluny, 10)
        gc.setBuildingPref(Civ.FRANCE.value, xml.iMontSaintMichel, 10)
        gc.setBuildingPref(Civ.FRANCE.value, xml.iPalaisPapes, 5)
        gc.setBuildingPref(Civ.FRANCE.value, xml.iLouvre, 20)

        gc.setBuildingPref(Civ.ARABIA.value, xml.iDomeRock, 15)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iTombAlWalid, 20)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iAlAzhar, 20)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iMosqueOfKairouan, 10)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iKoutoubiaMosque, 5)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iGardensAlAndalus, 5)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iLaMezquita, 5)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iAlhambra, 5)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iNotreDame, -5)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iStephansdom, -5)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iSistineChapel, -5)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iKrakDesChevaliers, -5)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iLeaningTower, -3)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iGoldenBull, -3)
        gc.setBuildingPref(Civ.ARABIA.value, xml.iCopernicus, -3)

        gc.setBuildingPref(Civ.BULGARIA.value, xml.iRoundChurch, 20)
        gc.setBuildingPref(Civ.BULGARIA.value, xml.iBoyanaChurch, 20)
        gc.setBuildingPref(Civ.BULGARIA.value, xml.iStCatherineMonastery, 5)
        gc.setBuildingPref(Civ.BULGARIA.value, xml.iSophiaKiev, 5)

        gc.setBuildingPref(Civ.CORDOBA.value, xml.iGardensAlAndalus, 20)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iLaMezquita, 20)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iAlhambra, 20)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iDomeRock, 10)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iAlAzhar, 5)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iMosqueOfKairouan, 10)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iKoutoubiaMosque, 5)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iNotreDame, -5)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iStephansdom, -5)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iSistineChapel, -5)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iKrakDesChevaliers, -5)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iLeaningTower, -3)
        gc.setBuildingPref(Civ.CORDOBA.value, xml.iGoldenBull, -3)

        gc.setBuildingPref(Civ.VENECIA.value, xml.iMarcoPolo, 15)
        gc.setBuildingPref(Civ.VENECIA.value, xml.iSanMarco, 20)
        gc.setBuildingPref(Civ.VENECIA.value, xml.iLanterna, 10)
        gc.setBuildingPref(Civ.VENECIA.value, xml.iLeonardosWorkshop, 5)
        gc.setBuildingPref(Civ.VENECIA.value, xml.iLeaningTower, 5)
        gc.setBuildingPref(Civ.VENECIA.value, xml.iGrandArsenal, 20)
        gc.setBuildingPref(Civ.VENECIA.value, xml.iGalataTower, 10)
        gc.setBuildingPref(Civ.VENECIA.value, xml.iFlorenceDuomo, 10)
        gc.setBuildingPref(Civ.VENECIA.value, xml.iSanGiorgio, 5)

        gc.setBuildingPref(Civ.BURGUNDY.value, xml.iMonasteryOfCluny, 20)
        gc.setBuildingPref(Civ.BURGUNDY.value, xml.iNotreDame, 10)
        gc.setBuildingPref(Civ.BURGUNDY.value, xml.iVersailles, 10)
        gc.setBuildingPref(Civ.BURGUNDY.value, xml.iMontSaintMichel, 10)
        gc.setBuildingPref(Civ.BURGUNDY.value, xml.iFontainebleau, 5)
        gc.setBuildingPref(Civ.BURGUNDY.value, xml.iPalaisPapes, 5)
        gc.setBuildingPref(Civ.BURGUNDY.value, xml.iLouvre, 10)

        gc.setBuildingPref(Civ.GERMANY.value, xml.iBrandenburgGate, 10)
        gc.setBuildingPref(Civ.GERMANY.value, xml.iImperialDiet, 20)
        gc.setBuildingPref(Civ.GERMANY.value, xml.iCopernicus, 5)
        gc.setBuildingPref(Civ.GERMANY.value, xml.iGoldenBull, 10)
        gc.setBuildingPref(Civ.GERMANY.value, xml.iMonasteryOfCluny, 5)
        gc.setBuildingPref(Civ.GERMANY.value, xml.iUraniborg, 5)
        gc.setBuildingPref(Civ.GERMANY.value, xml.iThomaskirche, 20)

        gc.setBuildingPref(Civ.NOVGOROD.value, xml.iStBasil, 10)
        gc.setBuildingPref(Civ.NOVGOROD.value, xml.iSophiaKiev, 10)
        gc.setBuildingPref(Civ.NOVGOROD.value, xml.iRoundChurch, 5)
        gc.setBuildingPref(Civ.NOVGOROD.value, xml.iBoyanaChurch, 5)
        gc.setBuildingPref(Civ.NOVGOROD.value, xml.iBorgundStaveChurch, 5)
        gc.setBuildingPref(Civ.NOVGOROD.value, xml.iPeterhofPalace, 15)

        gc.setBuildingPref(Civ.NORWAY.value, xml.iShrineOfUppsala, 20)
        gc.setBuildingPref(Civ.NORWAY.value, xml.iSamogitianAlkas, 5)
        gc.setBuildingPref(Civ.NORWAY.value, xml.iBorgundStaveChurch, 15)
        gc.setBuildingPref(Civ.NORWAY.value, xml.iUraniborg, 10)
        gc.setBuildingPref(Civ.NORWAY.value, xml.iKalmarCastle, 5)

        gc.setBuildingPref(Civ.KIEV.value, xml.iSophiaKiev, 20)
        gc.setBuildingPref(Civ.KIEV.value, xml.iStBasil, 5)
        gc.setBuildingPref(Civ.KIEV.value, xml.iRoundChurch, 5)
        gc.setBuildingPref(Civ.KIEV.value, xml.iBoyanaChurch, 5)
        gc.setBuildingPref(Civ.KIEV.value, xml.iPeterhofPalace, 10)

        gc.setBuildingPref(Civ.HUNGARY.value, xml.iPressburg, 20)
        gc.setBuildingPref(Civ.HUNGARY.value, xml.iGoldenBull, 20)
        gc.setBuildingPref(Civ.HUNGARY.value, xml.iBibliothecaCorviniana, 20)
        gc.setBuildingPref(Civ.HUNGARY.value, xml.iKazimierz, 10)
        gc.setBuildingPref(Civ.HUNGARY.value, xml.iCopernicus, 5)
        gc.setBuildingPref(Civ.HUNGARY.value, xml.iStephansdom, 5)

        gc.setBuildingPref(Civ.CASTILLE.value, xml.iEscorial, 20)
        gc.setBuildingPref(Civ.CASTILLE.value, xml.iMagellansVoyage, 10)
        gc.setBuildingPref(Civ.CASTILLE.value, xml.iTorreDelOro, 20)
        gc.setBuildingPref(Civ.CASTILLE.value, xml.iBelemTower, 10)

        gc.setBuildingPref(Civ.DENMARK.value, xml.iKalmarCastle, 10)
        gc.setBuildingPref(Civ.DENMARK.value, xml.iShrineOfUppsala, 20)
        gc.setBuildingPref(Civ.DENMARK.value, xml.iSamogitianAlkas, 5)
        gc.setBuildingPref(Civ.DENMARK.value, xml.iBorgundStaveChurch, 15)
        gc.setBuildingPref(Civ.DENMARK.value, xml.iUraniborg, 20)

        gc.setBuildingPref(Civ.SCOTLAND.value, xml.iMagnaCarta, 10)
        gc.setBuildingPref(Civ.SCOTLAND.value, xml.iWestminster, 10)
        gc.setBuildingPref(Civ.SCOTLAND.value, xml.iMonasteryOfCluny, 5)
        gc.setBuildingPref(Civ.SCOTLAND.value, xml.iBorgundStaveChurch, 5)
        gc.setBuildingPref(Civ.SCOTLAND.value, xml.iMontSaintMichel, 5)

        gc.setBuildingPref(Civ.POLAND.value, xml.iPressburg, 10)
        gc.setBuildingPref(Civ.POLAND.value, xml.iCopernicus, 10)
        gc.setBuildingPref(Civ.POLAND.value, xml.iGoldenBull, 5)
        gc.setBuildingPref(Civ.POLAND.value, xml.iKazimierz, 15)
        gc.setBuildingPref(Civ.POLAND.value, xml.iJasnaGora, 20)
        gc.setBuildingPref(Civ.POLAND.value, xml.iBrandenburgGate, 5)

        gc.setBuildingPref(Civ.GENOA.value, xml.iSanGiorgio, 20)
        gc.setBuildingPref(Civ.GENOA.value, xml.iLanterna, 20)
        gc.setBuildingPref(Civ.GENOA.value, xml.iLeonardosWorkshop, 5)
        gc.setBuildingPref(Civ.GENOA.value, xml.iLeaningTower, 5)
        gc.setBuildingPref(Civ.GENOA.value, xml.iSanMarco, 5)
        gc.setBuildingPref(Civ.GENOA.value, xml.iMarcoPolo, 5)
        gc.setBuildingPref(Civ.GENOA.value, xml.iGrandArsenal, 10)
        gc.setBuildingPref(Civ.GENOA.value, xml.iGalataTower, 20)
        gc.setBuildingPref(Civ.GENOA.value, xml.iFlorenceDuomo, 10)

        gc.setBuildingPref(Civ.MOROCCO.value, xml.iGardensAlAndalus, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iLaMezquita, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iAlhambra, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iDomeRock, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iAlAzhar, 5)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iMosqueOfKairouan, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iKoutoubiaMosque, 20)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iNotreDame, -5)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iStephansdom, -5)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iSistineChapel, -5)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iKrakDesChevaliers, -5)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iLeaningTower, -3)
        gc.setBuildingPref(Civ.MOROCCO.value, xml.iGoldenBull, -3)

        gc.setBuildingPref(Civ.ENGLAND.value, xml.iMagnaCarta, 20)
        gc.setBuildingPref(Civ.ENGLAND.value, xml.iWestminster, 20)
        gc.setBuildingPref(Civ.ENGLAND.value, xml.iMonasteryOfCluny, 5)
        gc.setBuildingPref(Civ.ENGLAND.value, xml.iUraniborg, 5)
        gc.setBuildingPref(Civ.ENGLAND.value, xml.iTorreDelOro, 5)
        gc.setBuildingPref(Civ.ENGLAND.value, xml.iBelemTower, 5)

        gc.setBuildingPref(Civ.PORTUGAL.value, xml.iBelemTower, 20)
        gc.setBuildingPref(Civ.PORTUGAL.value, xml.iPalacioDaPena, 20)
        gc.setBuildingPref(Civ.PORTUGAL.value, xml.iMagellansVoyage, 20)
        gc.setBuildingPref(Civ.PORTUGAL.value, xml.iTorreDelOro, 10)

        gc.setBuildingPref(Civ.ARAGON.value, xml.iMagellansVoyage, 10)
        gc.setBuildingPref(Civ.ARAGON.value, xml.iTorreDelOro, 10)
        gc.setBuildingPref(Civ.ARAGON.value, xml.iEscorial, 5)
        gc.setBuildingPref(Civ.ARAGON.value, xml.iBelemTower, 10)

        gc.setBuildingPref(Civ.SWEDEN.value, xml.iKalmarCastle, 20)
        gc.setBuildingPref(Civ.SWEDEN.value, xml.iShrineOfUppsala, 5)
        gc.setBuildingPref(Civ.SWEDEN.value, xml.iBorgundStaveChurch, 15)
        gc.setBuildingPref(Civ.SWEDEN.value, xml.iUraniborg, 10)

        gc.setBuildingPref(Civ.PRUSSIA.value, xml.iBrandenburgGate, 20)
        gc.setBuildingPref(Civ.PRUSSIA.value, xml.iThomaskirche, 10)
        gc.setBuildingPref(Civ.PRUSSIA.value, xml.iCopernicus, 5)
        gc.setBuildingPref(Civ.PRUSSIA.value, xml.iPressburg, 5)

        gc.setBuildingPref(Civ.LITHUANIA.value, xml.iSamogitianAlkas, 20)
        gc.setBuildingPref(Civ.LITHUANIA.value, xml.iGediminasTower, 20)
        gc.setBuildingPref(Civ.LITHUANIA.value, xml.iBorgundStaveChurch, 5)

        gc.setBuildingPref(Civ.AUSTRIA.value, xml.iStephansdom, 20)
        gc.setBuildingPref(Civ.AUSTRIA.value, xml.iThomaskirche, 15)
        gc.setBuildingPref(Civ.AUSTRIA.value, xml.iCopernicus, 5)
        gc.setBuildingPref(Civ.AUSTRIA.value, xml.iGoldenBull, 5)
        gc.setBuildingPref(Civ.AUSTRIA.value, xml.iPressburg, 5)
        gc.setBuildingPref(Civ.AUSTRIA.value, xml.iAustrianOperaHouse, 10)

        gc.setBuildingPref(Civ.OTTOMAN.value, xml.iTopkapiPalace, 20)
        gc.setBuildingPref(Civ.OTTOMAN.value, xml.iBlueMosque, 20)
        gc.setBuildingPref(Civ.OTTOMAN.value, xml.iSelimiyeMosque, 20)
        gc.setBuildingPref(Civ.OTTOMAN.value, xml.iTombAlWalid, 10)
        gc.setBuildingPref(Civ.OTTOMAN.value, xml.iKizilKule, 10)
        gc.setBuildingPref(Civ.OTTOMAN.value, xml.iAlAzhar, 5)

        gc.setBuildingPref(Civ.MOSCOW.value, xml.iStBasil, 20)
        gc.setBuildingPref(Civ.MOSCOW.value, xml.iPeterhofPalace, 20)
        gc.setBuildingPref(Civ.MOSCOW.value, xml.iSophiaKiev, 5)

        gc.setBuildingPref(Civ.DUTCH.value, xml.iBeurs, 20)
        gc.setBuildingPref(Civ.DUTCH.value, xml.iUraniborg, 5)
        gc.setBuildingPref(Civ.DUTCH.value, xml.iThomaskirche, 5)

        gc.setBuildingPref(Civ.POPE.value, xml.iSistineChapel, 20)
        gc.setBuildingPref(Civ.POPE.value, xml.iPalaisPapes, 10)
        gc.setBuildingPref(Civ.POPE.value, xml.iLeaningTower, 5)
        gc.setBuildingPref(Civ.POPE.value, xml.iFlorenceDuomo, 5)
        gc.setBuildingPref(Civ.POPE.value, xml.iLeonardosWorkshop, 5)

        # 3Miro: set the Jews as the minor Religion
        gc.setMinorReligion(Religion.JUDAISM.value)
        gc.setMinorReligionRefugies(0)

        # Manor House + Manorialism: iBuilding + 1000 * iCivic + 100,000 * iGold + 1,000,000 * iResearch + 10,000,000 * iCulture + 100,000,000 * iEspionage
        # 3Miro: moved to XML, no need to put it here
        # gc.setBuildingCivicCommerseCombo1( xml.iManorHouse + 1000 * xml.iManorialism + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
        # gc.setBuildingCivicCommerseCombo2( xml.iFrenchChateau + 1000 * xml.iManorialism + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
        # gc.setBuildingCivicCommerseCombo3(-1)

        # 3Miro: Psycho AI cheat, this will make Ottoman AI think it can win battles vs Constantinople at 90/100 rate
        # 	it will also actually boost the Ottoman's odds (actually lower the defenders chance by 20 percent), but only when attacking Constantinople
        gc.setPsychoAICheat(
            Civ.OTTOMAN.value, *civilizations()[Civ.BYZANTIUM].location.capital.to_tuple()
        )

        # 3Miro: be very careful here, this can really mess the AI
        # 	setHistoricalEnemyAICheat( iAttacker, iDefender, 10 ) gives the attacker +10% bonus, when attacked units belong to the defender
        # 	this modifier only works in AI vs AI battles, it's ignored if either player is Human
        # 	none of the AI players is "aware" of the modification, if you make it too big, it could lead to a couple strange situations
        # 	(where the AI has clear advantage in a battle, yet it still won't attack)
        # 	so this should be a "last resort" solution, other methods are always preferable
        gc.setHistoricalEnemyAICheat(Civ.OTTOMAN.value, Civ.BULGARIA.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.BULGARIA.value, Civ.OTTOMAN.value, -10)

        gc.setHistoricalEnemyAICheat(Civ.CASTILLE.value, Civ.CORDOBA.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.CORDOBA.value, Civ.CASTILLE.value, -10)

        gc.setHistoricalEnemyAICheat(Civ.PORTUGAL.value, Civ.CASTILLE.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.CASTILLE.value, Civ.PORTUGAL.value, -10)

        gc.setHistoricalEnemyAICheat(Civ.AUSTRIA.value, Civ.HUNGARY.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.HUNGARY.value, Civ.AUSTRIA.value, -10)

        gc.setHistoricalEnemyAICheat(Civ.AUSTRIA.value, Civ.GERMANY.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.GERMANY.value, Civ.AUSTRIA.value, -10)

        # 3Miro: this sets rules on how players can Vassalize, first two parameters are the players (we should probably keep this symmetric)
        # 	if the third parameter is -1: cannot Vassalize, 0: has to satisfy a condition (default), 1 can Vassalize without conditions
        # 	the condition is that either one of the players needs to have a city in a province that the other players considers >= the last parameter
        # 	the default for the last parameter is 0, we should call this at least once to set the parameter (it is the same for all players)
        gc.setVassalagaeCondition(
            Civ.CORDOBA.value, Civ.ARABIA.value, 1, ProvinceTypes.OUTER.value
        )
        gc.setVassalagaeCondition(
            Civ.ARABIA.value, Civ.CORDOBA.value, 1, ProvinceTypes.OUTER.value
        )

        # How much culture should we get into a province of this type, ignore the war and settler values (0,0)
        gc.setProvinceTypeParams(ProvinceTypes.NONE.value, 0, 0, 1, 3)  # 1/3 culture
        gc.setProvinceTypeParams(ProvinceTypes.OUTER.value, 0, 0, 1, 1)  # no change to culture
        gc.setProvinceTypeParams(
            ProvinceTypes.POTENTIAL.value, 0, 0, 1, 1
        )  # same as outer culture
        gc.setProvinceTypeParams(ProvinceTypes.NATURAL.value, 0, 0, 2, 1)  # double-culture
        gc.setProvinceTypeParams(ProvinceTypes.CORE.value, 0, 0, 3, 1)  # triple-culture

        # block foundation of Protestantism except by a Catholic player
        gc.setParentSchismReligions(Religion.CATHOLICISM.value, Religion.PROTESTANTISM.value)

        # block declaration of war against newly spawning nations for this many turns (pre-set wars are not affected)
        gc.setPaceTurnsAfterSpawn(5)

        # Absinthe: Visualization parameters are outdated
        # 			display for Core and Normal areas were added in CvEventManager/onGameStart, can be enabled/disabled in the GlobalDefines_Alt.xml
        # 			those are the only 2 you might want to use on the main map, for everything else we have better tools in the WB
        ## set the Visualization parameters, note that those functions can be accessed at any time, not just here
        ## note that if you set Civs for mode 0 and 1 in WB mode, they will stay set until you exit
        # gc.setWhatToPlot( 0 ) # 0 - Core (default), 1 - Normal, 2 - Settler, 3 - Wars
        ##gc.setCivForCore( iByzantium ) # plot the Core of Byzantium (only if setWhatToPlot is set to 0)
        ##gc.setCivForNormal( iByzantium ) # plot the Normal area of Byzantium (only if setWhatToPlot is set to 1)
        ##gc.setCivForSettler( iFrankia ) # plot the Settlers Map of Byzantium (only if setWhatToPlot is set to 2)
        ##gc.setCivForWars( iByzantium ) # plot the Wars Map of of Byzantium (only if setWhatToPlot is set to 3)

        self.postAreas()

    def setTechTimeline(self):
        gc.setTimelineTechModifiers(
            9, 25, -50, 1, 100, 50
        )  # go between 10 times slower and 4 times faster
        # formula is: iAhistoric = iCurrentTurn - iHistoricTurn, capped at ( iTPCap, iTBCap )
        # iCost *= 100 + topPenalty * iHistoric * iAhistoric / BotPenalty, iCost /= 100
        # iCost *= 100 - topBuff * iHistoric * iAhistoric / BotBuff, iCost /= 100
        # gc.setTimelineTechDateForTech( iTech, iTurn )
        gc.setTimelineTechDateForTech(xml.iCalendar, 0)
        gc.setTimelineTechDateForTech(xml.iArchitecture, 30)
        gc.setTimelineTechDateForTech(xml.iBronzeCasting, 15)
        gc.setTimelineTechDateForTech(xml.iTheology, 10)
        gc.setTimelineTechDateForTech(xml.iManorialism, 5)
        gc.setTimelineTechDateForTech(xml.iStirrup, DateTurn.i600AD)
        gc.setTimelineTechDateForTech(xml.iEngineering, 55)  # teir 2
        gc.setTimelineTechDateForTech(xml.iChainMail, 43)
        gc.setTimelineTechDateForTech(xml.iArt, 38)
        gc.setTimelineTechDateForTech(xml.iMonasticism, 50)
        gc.setTimelineTechDateForTech(xml.iVassalage, 60)
        gc.setTimelineTechDateForTech(xml.iAstrolabe, 76)  # teir 3
        gc.setTimelineTechDateForTech(xml.iMachinery, 76)
        gc.setTimelineTechDateForTech(xml.iVaultedArches, 90)  #
        gc.setTimelineTechDateForTech(xml.iMusic, 80)
        gc.setTimelineTechDateForTech(xml.iHerbalMedicine, 95)
        gc.setTimelineTechDateForTech(xml.iFeudalism, DateTurn.i778AD)  # Feudalism
        gc.setTimelineTechDateForTech(xml.iFarriers, 100)
        gc.setTimelineTechDateForTech(xml.iMapMaking, 160)  # this is tier 5
        gc.setTimelineTechDateForTech(xml.iBlastFurnace, 120)  # teir 4
        gc.setTimelineTechDateForTech(xml.iSiegeEngines, DateTurn.i1097AD)  # trebuchets
        gc.setTimelineTechDateForTech(xml.iGothicArchitecture, 130)  # 12th century
        gc.setTimelineTechDateForTech(xml.iLiterature, 145)
        gc.setTimelineTechDateForTech(xml.iCodeOfLaws, 120)
        gc.setTimelineTechDateForTech(xml.iAristocracy, 135)
        gc.setTimelineTechDateForTech(xml.iLateenSails, 125)  # actually this is tier 4
        gc.setTimelineTechDateForTech(
            xml.iPlateArmor, 185
        )  # teir 5: historically late 1200s, and by the 14th century, plate armour was commonly used to supplement mail
        gc.setTimelineTechDateForTech(xml.iMonumentBuilding, 180)
        gc.setTimelineTechDateForTech(xml.iClassicalKnowledge, 175)
        gc.setTimelineTechDateForTech(
            xml.iAlchemy, DateTurn.i1144AD
        )  # Alchemy introduced in Europe
        gc.setTimelineTechDateForTech(xml.iCivilService, 190)  # teir 6
        gc.setTimelineTechDateForTech(xml.iClockmaking, 200)
        gc.setTimelineTechDateForTech(xml.iPhilosophy, 215)
        gc.setTimelineTechDateForTech(xml.iEducation, 220)
        gc.setTimelineTechDateForTech(xml.iGuilds, 200)
        gc.setTimelineTechDateForTech(xml.iChivalry, 195)
        gc.setTimelineTechDateForTech(xml.iOptics, 228)  # teir 7
        gc.setTimelineTechDateForTech(xml.iReplaceableParts, 250)
        gc.setTimelineTechDateForTech(xml.iPatronage, 230)
        gc.setTimelineTechDateForTech(xml.iGunpowder, DateTurn.i1300AD)
        gc.setTimelineTechDateForTech(xml.iBanking, 240)
        gc.setTimelineTechDateForTech(xml.iMilitaryTradition, 260)
        gc.setTimelineTechDateForTech(xml.iShipbuilding, 275)  # teir 8
        gc.setTimelineTechDateForTech(xml.iDrama, 270)
        gc.setTimelineTechDateForTech(xml.iDivineRight, 266)
        gc.setTimelineTechDateForTech(xml.iChemistry, 280)
        gc.setTimelineTechDateForTech(xml.iPaper, 290)
        gc.setTimelineTechDateForTech(xml.iProfessionalArmy, 295)
        gc.setTimelineTechDateForTech(xml.iPrintingPress, DateTurn.i1517AD)  # teir 9 from turn 304
        gc.setTimelineTechDateForTech(xml.iPublicWorks, 310)
        gc.setTimelineTechDateForTech(xml.iMatchlock, DateTurn.i1500AD)
        gc.setTimelineTechDateForTech(xml.iArabicKnowledge, DateTurn.i1491AD)  # fall of Granada
        gc.setTimelineTechDateForTech(xml.iAstronomy, DateTurn.i1514AD)  # teir 10 Copernicus
        gc.setTimelineTechDateForTech(xml.iSteamEngines, DateTurn.i1690AD)  # first steam engine
        gc.setTimelineTechDateForTech(xml.iConstitution, 375)
        gc.setTimelineTechDateForTech(xml.iPolygonalFort, 370)
        gc.setTimelineTechDateForTech(xml.iArabicMedicine, 342)
        gc.setTimelineTechDateForTech(xml.iRenaissanceArt, DateTurn.i1540AD)  # teir 11, 1541
        gc.setTimelineTechDateForTech(xml.iNationalism, 380)
        gc.setTimelineTechDateForTech(xml.iLiberalism, 400)
        gc.setTimelineTechDateForTech(xml.iScientificMethod, DateTurn.i1623AD)  # Galilei
        gc.setTimelineTechDateForTech(xml.iMilitaryTactics, 410)
        gc.setTimelineTechDateForTech(xml.iNavalArchitecture, 385)  # teir 12
        gc.setTimelineTechDateForTech(xml.iCivilEngineering, 395)
        gc.setTimelineTechDateForTech(xml.iRightOfMan, 460)
        gc.setTimelineTechDateForTech(xml.iEconomics, 435)
        gc.setTimelineTechDateForTech(xml.iPhysics, DateTurn.i1687AD)
        gc.setTimelineTechDateForTech(xml.iBiology, 440)
        gc.setTimelineTechDateForTech(xml.iCombinedArms, 430)
        gc.setTimelineTechDateForTech(
            xml.iTradingCompanies, DateTurn.i1600AD
        )  # teir 13 from turn 325
        gc.setTimelineTechDateForTech(xml.iMachineTools, 450)
        gc.setTimelineTechDateForTech(xml.iFreeMarket, 450)
        gc.setTimelineTechDateForTech(xml.iExplosives, 460)
        gc.setTimelineTechDateForTech(xml.iMedicine, 458)
        gc.setTimelineTechDateForTech(xml.iIndustrialTech, DateTurn.i1800AD)

    def preMapsNSizes(self):
        # settlersMaps, DO NOT CHANGE THIS CODE
        gc.setSizeNPlayers(
            WORLD_WIDTH,
            WORLD_HEIGHT,
            civilizations().majors().len(),
            civilizations().drop(Civ.BARBARIAN).len(),
            xml.iNumTechs,
            PlagueType.BUILDING_PLAGUE.value,
            len(Religion),
        )
        for i in civilizations().majors().ids():
            for y in range(WORLD_HEIGHT):
                for x in range(WORLD_WIDTH):
                    gc.setSettlersMap(i, y, x, RFCEMaps.tSettlersMaps[i][y][x])
                    gc.setWarsMap(i, y, x, RFCEMaps.tWarsMaps[i][y][x])

        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                if RFCEMaps.tProvinceMap[y][x] > -1:
                    # "no province" of ocean is settled different than -1, set only non-negative values,
                    # the C++ map is initialized to "no-province" by setSizeNPlayers(...)
                    # "no-province" is returned as -1 via the Cy interface
                    gc.setProvince(x, y, RFCEMaps.tProvinceMap[y][x])
        gc.createProvinceCrossreferenceList()  # make sure to call this AFTER setting all the Province entries

        gc.setProvinceTypeNumber(
            len(ProvinceTypes)
        )  # set the Number of Provinces, call this before you set any AI or culture modifiers

        # birth turns for the players, do not change this loop
        for civ in civilizations().drop(Civ.BARBARIAN):
            gc.setStartingTurn(civ.id, civ.date.birth)

    def postAreas(self):
        # 3Miro: DO NOT CHANGE THIS CODE
        # this adds the Core and Normal Areas from Consts.py into C++. There is Dynamical Memory involved, so don't change this
        for civ in civilizations().majors().ids():
            iCBLx = Consts.tCoreAreasTL[civ][0]
            iCBLy = Consts.tCoreAreasTL[civ][1]
            iCTRx = Consts.tCoreAreasBR[civ][0]
            iCTRy = Consts.tCoreAreasBR[civ][1]
            iNBLx = Consts.tNormalAreasTL[civ][0]
            iNBLy = Consts.tNormalAreasTL[civ][1]
            iNTRx = Consts.tNormalAreasBR[civ][0]
            iNTRy = Consts.tNormalAreasBR[civ][1]
            iCCE = len(Consts.lExtraPlots[civ])
            iCNE = len(Consts.tNormalAreasSubtract[civ])
            gc.setCoreNormal(
                civ, iCBLx, iCBLy, iCTRx, iCTRy, iNBLx, iNBLy, iNTRx, iNTRy, iCCE, iCNE
            )
            for iEx in range(iCCE):
                gc.addCoreException(
                    civ, Consts.lExtraPlots[civ][iEx][0], Consts.lExtraPlots[civ][iEx][1]
                )
            for iEx in range(iCNE):
                gc.addNormalException(
                    civ,
                    Consts.tNormalAreasSubtract[civ][iEx][0],
                    Consts.tNormalAreasSubtract[civ][iEx][1],
                )

        gc.setProsecutorReligions(xml.iProsecutor, PROSECUTOR_UNITCLASS)
        gc.setSaintParameters(
            xml.iGreatProphet, GREAT_PROPHET_FAITH_POINT_BONUS, 20, 40
        )  # try to amass at least 20 and don't bother above 40 points
        gc.setIndependnets(
            min(civilizations().independents().ids()),
            max(civilizations().independents().ids()),
            Civ.BARBARIAN.value,
        )
        gc.setPapalPlayer(Civ.POPE.value, Religion.CATHOLICISM.value)

        gc.setAutorunHack(xml.iCatapult, 32, 0)  # Autorun hack, sync with RNF module

        # 3MiroMercs: set the merc promotion
        gc.setMercPromotion(Promotion.MERC.value)

        for civ in civilizations().majors():
            if civ.initial.condition:
                gc.setStartingWorkers(civ.id, civ.initial.condition.workers)
