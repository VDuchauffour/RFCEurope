# Rhye's and Fall of Civilization: Europe - Balancing modifiers are placed here

from CvPythonExtensions import *
import Consts
import XMLConsts as xml
import RFCEMaps as rfcemaps
import RFCUtils

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
        gc.setGrowthModifiersAI(Consts.iByzantium, 200, 100, 200, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iByzantium, 150, 100, 200, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iFrankia, 110, 100, 110, 100, 100, 1)
        gc.setGrowthModifiersHu(Consts.iFrankia, 110, 100, 110, 100, 100, 1)
        gc.setGrowthModifiersAI(Consts.iArabia, 150, 100, 150, 100, 100, 1)
        gc.setGrowthModifiersHu(Consts.iArabia, 150, 100, 150, 100, 100, 1)
        gc.setGrowthModifiersAI(Consts.iBulgaria, 150, 100, 100, 100, 100, 1)
        gc.setGrowthModifiersHu(Consts.iBulgaria, 125, 100, 100, 100, 100, 1)
        gc.setGrowthModifiersAI(Consts.iCordoba, 150, 100, 100, 100, 100, 1)
        gc.setGrowthModifiersHu(Consts.iCordoba, 150, 100, 100, 100, 100, 1)
        gc.setGrowthModifiersAI(Consts.iVenecia, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iVenecia, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iBurgundy, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iBurgundy, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iGermany, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iGermany, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iNovgorod, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iNovgorod, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iNorway, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iNorway, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iKiev, 150, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iKiev, 150, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iHungary, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iHungary, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iSpain, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iSpain, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iDenmark, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iDenmark, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iScotland, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iScotland, 100, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iPoland, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersHu(Consts.iPoland, 125, 100, 100, 100, 100, 2)
        gc.setGrowthModifiersAI(Consts.iGenoa, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iGenoa, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iMorocco, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iMorocco, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iEngland, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iEngland, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iPortugal, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iPortugal, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iAragon, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iAragon, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iSweden, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iSweden, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iPrussia, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iPrussia, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iLithuania, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iLithuania, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(
            Consts.iAustria, 100, 200, 100, 100, 100, 3
        )  # Austria is squashed by other's culture, they need the boost
        gc.setGrowthModifiersHu(Consts.iAustria, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iTurkey, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iTurkey, 100, 150, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iMoscow, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersHu(Consts.iMoscow, 100, 100, 100, 100, 100, 3)
        gc.setGrowthModifiersAI(Consts.iDutch, 100, 200, 60, 100, 50, 4)
        gc.setGrowthModifiersHu(Consts.iDutch, 100, 200, 60, 100, 50, 4)
        gc.setGrowthModifiersAI(Consts.iPope, 150, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Consts.iIndependent, 100, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Consts.iIndependent2, 100, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Consts.iIndependent3, 100, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Consts.iIndependent4, 100, 100, 100, 50, 100, 1)
        gc.setGrowthModifiersAI(Consts.iBarbarian, 100, 100, 100, 50, 100, 1)

        # void setProductionModifiers( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100 )
        # 3Miro: at 100 research cost, the cost is exactly as in the XML files, the cost in general is however increased for all civs
        gc.setProductionModifiersAI(Consts.iByzantium, 200, 200, 200, 350)
        gc.setProductionModifiersHu(Consts.iByzantium, 200, 150, 200, 350)
        gc.setProductionModifiersAI(Consts.iFrankia, 140, 120, 125, 150)
        gc.setProductionModifiersHu(Consts.iFrankia, 150, 120, 125, 130)
        gc.setProductionModifiersAI(Consts.iArabia, 130, 125, 150, 280)
        gc.setProductionModifiersHu(Consts.iArabia, 150, 125, 150, 230)
        gc.setProductionModifiersAI(Consts.iBulgaria, 130, 125, 125, 250)
        gc.setProductionModifiersHu(Consts.iBulgaria, 150, 150, 125, 200)
        gc.setProductionModifiersAI(Consts.iCordoba, 180, 170, 130, 250)
        gc.setProductionModifiersHu(Consts.iCordoba, 200, 180, 140, 230)
        gc.setProductionModifiersAI(Consts.iVenecia, 100, 100, 100, 150)
        gc.setProductionModifiersHu(Consts.iVenecia, 100, 100, 100, 130)
        gc.setProductionModifiersAI(Consts.iBurgundy, 130, 120, 120, 150)
        gc.setProductionModifiersHu(Consts.iBurgundy, 150, 120, 120, 150)
        gc.setProductionModifiersAI(Consts.iGermany, 120, 120, 100, 140)
        gc.setProductionModifiersHu(Consts.iGermany, 140, 140, 125, 130)
        gc.setProductionModifiersAI(Consts.iNovgorod, 120, 120, 120, 150)
        gc.setProductionModifiersHu(Consts.iNovgorod, 125, 125, 125, 150)
        gc.setProductionModifiersAI(Consts.iNorway, 125, 125, 125, 130)
        gc.setProductionModifiersHu(Consts.iNorway, 125, 125, 100, 140)
        gc.setProductionModifiersAI(Consts.iKiev, 100, 120, 100, 140)
        gc.setProductionModifiersHu(Consts.iKiev, 125, 150, 125, 150)
        gc.setProductionModifiersAI(Consts.iHungary, 120, 120, 100, 150)
        gc.setProductionModifiersHu(Consts.iHungary, 125, 125, 100, 130)
        gc.setProductionModifiersAI(Consts.iSpain, 100, 100, 100, 130)
        gc.setProductionModifiersHu(Consts.iSpain, 125, 100, 100, 120)
        gc.setProductionModifiersAI(Consts.iDenmark, 100, 100, 100, 110)
        gc.setProductionModifiersHu(Consts.iDenmark, 100, 100, 100, 120)
        gc.setProductionModifiersAI(Consts.iScotland, 100, 100, 100, 125)
        gc.setProductionModifiersHu(Consts.iScotland, 110, 110, 110, 125)
        gc.setProductionModifiersAI(Consts.iPoland, 100, 120, 120, 140)
        gc.setProductionModifiersHu(Consts.iPoland, 120, 120, 120, 130)
        gc.setProductionModifiersAI(Consts.iGenoa, 100, 100, 100, 130)
        gc.setProductionModifiersHu(Consts.iGenoa, 100, 100, 100, 125)
        gc.setProductionModifiersAI(Consts.iMorocco, 120, 120, 120, 175)
        gc.setProductionModifiersHu(Consts.iMorocco, 120, 120, 120, 175)
        gc.setProductionModifiersAI(Consts.iEngland, 80, 80, 100, 120)
        gc.setProductionModifiersHu(Consts.iEngland, 100, 100, 100, 110)
        gc.setProductionModifiersAI(Consts.iPortugal, 70, 90, 100, 110)
        gc.setProductionModifiersHu(Consts.iPortugal, 80, 90, 100, 100)
        gc.setProductionModifiersAI(Consts.iAragon, 75, 90, 100, 125)
        gc.setProductionModifiersHu(Consts.iAragon, 80, 100, 100, 125)
        gc.setProductionModifiersAI(Consts.iSweden, 80, 80, 100, 100)
        gc.setProductionModifiersHu(Consts.iSweden, 80, 80, 100, 100)
        gc.setProductionModifiersAI(Consts.iPrussia, 60, 80, 120, 90)
        gc.setProductionModifiersHu(Consts.iPrussia, 75, 80, 120, 100)
        gc.setProductionModifiersAI(Consts.iLithuania, 70, 100, 110, 110)
        gc.setProductionModifiersHu(Consts.iLithuania, 80, 100, 110, 100)
        gc.setProductionModifiersAI(Consts.iAustria, 50, 80, 100, 80)
        gc.setProductionModifiersHu(Consts.iAustria, 80, 80, 100, 100)
        gc.setProductionModifiersAI(Consts.iTurkey, 60, 75, 100, 120)
        gc.setProductionModifiersHu(Consts.iTurkey, 75, 75, 100, 110)
        gc.setProductionModifiersAI(Consts.iMoscow, 80, 80, 100, 120)
        gc.setProductionModifiersHu(Consts.iMoscow, 110, 110, 100, 120)
        gc.setProductionModifiersAI(Consts.iDutch, 80, 50, 50, 50)
        gc.setProductionModifiersHu(Consts.iDutch, 90, 50, 60, 50)
        gc.setProductionModifiersAI(Consts.iPope, 300, 200, 100, 350)
        gc.setProductionModifiersAI(Consts.iIndependent, 170, 100, 400, 200)  # The peaceful ones
        gc.setProductionModifiersAI(Consts.iIndependent2, 170, 100, 400, 200)  # The peaceful ones
        gc.setProductionModifiersAI(Consts.iIndependent3, 125, 100, 600, 300)  # The warlike ones
        gc.setProductionModifiersAI(Consts.iIndependent4, 125, 100, 600, 300)  # The warlike ones
        gc.setProductionModifiersAI(Consts.iBarbarian, 125, 100, 900, 350)

        # void setSupportModifiers( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100 )
        # note that iCityNum also gets an additional modifier based on population in the city
        # note that the base for inflation is modified by turn number (among many other things)
        gc.setSupportModifiersAI(Consts.iByzantium, 50, 150, 70, 50, 120)
        gc.setSupportModifiersHu(Consts.iByzantium, 50, 150, 70, 50, 120)
        gc.setSupportModifiersAI(Consts.iFrankia, 30, 120, 70, 50, 100)
        gc.setSupportModifiersHu(Consts.iFrankia, 30, 120, 70, 50, 100)
        gc.setSupportModifiersAI(Consts.iArabia, 30, 150, 70, 40, 120)
        gc.setSupportModifiersHu(Consts.iArabia, 30, 150, 70, 40, 120)
        gc.setSupportModifiersAI(Consts.iBulgaria, 40, 150, 80, 50, 120)
        gc.setSupportModifiersHu(Consts.iBulgaria, 40, 150, 80, 50, 120)
        gc.setSupportModifiersAI(Consts.iCordoba, 40, 150, 70, 40, 120)
        gc.setSupportModifiersHu(Consts.iCordoba, 40, 150, 70, 40, 120)
        gc.setSupportModifiersAI(Consts.iVenecia, 20, 100, 60, 50, 100)
        gc.setSupportModifiersHu(Consts.iVenecia, 20, 100, 60, 50, 100)
        gc.setSupportModifiersAI(Consts.iBurgundy, 30, 120, 70, 40, 100)
        gc.setSupportModifiersHu(Consts.iBurgundy, 30, 120, 70, 40, 100)
        gc.setSupportModifiersAI(Consts.iGermany, 20, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Consts.iGermany, 20, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Consts.iNovgorod, 30, 120, 70, 40, 100)
        gc.setSupportModifiersHu(Consts.iNovgorod, 30, 120, 70, 40, 100)
        gc.setSupportModifiersAI(Consts.iNorway, 20, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Consts.iNorway, 20, 100, 60, 40, 100)
        gc.setSupportModifiersAI(Consts.iKiev, 30, 120, 60, 40, 100)
        gc.setSupportModifiersHu(Consts.iKiev, 30, 120, 60, 40, 100)
        gc.setSupportModifiersAI(Consts.iHungary, 25, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Consts.iHungary, 25, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Consts.iSpain, 20, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Consts.iSpain, 20, 100, 60, 40, 100)
        gc.setSupportModifiersAI(Consts.iDenmark, 20, 100, 80, 50, 100)
        gc.setSupportModifiersHu(Consts.iDenmark, 20, 100, 80, 50, 100)
        gc.setSupportModifiersAI(Consts.iScotland, 25, 100, 80, 50, 100)
        gc.setSupportModifiersHu(Consts.iScotland, 25, 100, 80, 50, 100)
        gc.setSupportModifiersAI(Consts.iPoland, 25, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Consts.iPoland, 25, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Consts.iGenoa, 20, 100, 60, 50, 100)
        gc.setSupportModifiersHu(Consts.iGenoa, 20, 100, 60, 50, 100)
        gc.setSupportModifiersAI(Consts.iMorocco, 25, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Consts.iMorocco, 25, 100, 60, 40, 100)
        gc.setSupportModifiersAI(Consts.iEngland, 20, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Consts.iEngland, 20, 100, 60, 40, 100)
        gc.setSupportModifiersAI(Consts.iPortugal, 20, 100, 70, 50, 100)
        gc.setSupportModifiersHu(Consts.iPortugal, 20, 100, 70, 50, 100)
        gc.setSupportModifiersAI(Consts.iAragon, 25, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Consts.iAragon, 25, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Consts.iSweden, 20, 90, 70, 40, 100)
        gc.setSupportModifiersHu(Consts.iSweden, 20, 90, 70, 40, 100)
        gc.setSupportModifiersAI(Consts.iPrussia, 20, 90, 70, 40, 100)
        gc.setSupportModifiersHu(Consts.iPrussia, 20, 90, 70, 40, 100)
        gc.setSupportModifiersAI(Consts.iLithuania, 25, 100, 70, 40, 100)
        gc.setSupportModifiersHu(Consts.iLithuania, 25, 100, 70, 40, 100)
        gc.setSupportModifiersAI(Consts.iAustria, 20, 80, 80, 40, 100)
        gc.setSupportModifiersHu(Consts.iAustria, 20, 80, 80, 40, 100)
        gc.setSupportModifiersAI(Consts.iTurkey, 30, 100, 60, 40, 100)
        gc.setSupportModifiersHu(Consts.iTurkey, 30, 100, 60, 40, 100)
        gc.setSupportModifiersAI(
            Consts.iMoscow, 25, 100, 70, 40, 100
        )  # note that the city maintenance values are further modified by their UP
        gc.setSupportModifiersHu(
            Consts.iMoscow, 25, 100, 70, 40, 100
        )  # note that the city maintenance values are further modified by their UP
        gc.setSupportModifiersAI(Consts.iDutch, 20, 70, 80, 50, 100)
        gc.setSupportModifiersHu(Consts.iDutch, 20, 70, 80, 50, 100)
        gc.setSupportModifiersAI(Consts.iPope, 20, 150, 80, 50, 100)
        gc.setSupportModifiersAI(Consts.iIndependent, 10, 100, 10, 20, 100)
        gc.setSupportModifiersAI(Consts.iIndependent2, 10, 100, 10, 20, 100)
        gc.setSupportModifiersAI(Consts.iIndependent3, 10, 100, 10, 20, 100)
        gc.setSupportModifiersAI(Consts.iIndependent4, 10, 100, 10, 20, 100)
        gc.setSupportModifiersAI(Consts.iBarbarian, 10, 250, 10, 20, 100)

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

        gc.setInitialBuilding(Consts.iVenecia, xml.iHarbor, True)
        gc.setInitialBuilding(Consts.iVenecia, xml.iGranary, True)

        gc.setInitialBuilding(Consts.iSpain, xml.iBarracks, True)

        gc.setInitialBuilding(Consts.iDenmark, xml.iBarracks, True)

        gc.setInitialBuilding(Consts.iScotland, xml.iBarracks, True)

        gc.setInitialBuilding(Consts.iMoscow, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iMoscow, xml.iBarracks, True)
        gc.setInitialBuilding(Consts.iMoscow, xml.iForge, True)
        gc.setInitialBuilding(Consts.iMoscow, xml.iMarket, True)

        gc.setInitialBuilding(Consts.iGenoa, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iGenoa, xml.iBarracks, True)
        gc.setInitialBuilding(Consts.iGenoa, xml.iHarbor, True)

        gc.setInitialBuilding(Consts.iMorocco, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iMorocco, xml.iBarracks, True)

        gc.setInitialBuilding(Consts.iEngland, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iEngland, xml.iBarracks, True)

        gc.setInitialBuilding(Consts.iPortugal, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iPortugal, xml.iBarracks, True)

        gc.setInitialBuilding(Consts.iAragon, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iAragon, xml.iBarracks, True)
        gc.setInitialBuilding(Consts.iAragon, xml.iHarbor, True)

        gc.setInitialBuilding(Consts.iPrussia, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iPrussia, xml.iBarracks, True)

        gc.setInitialBuilding(Consts.iLithuania, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iLithuania, xml.iBarracks, True)

        gc.setInitialBuilding(Consts.iAustria, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iAustria, xml.iBarracks, True)
        gc.setInitialBuilding(Consts.iAustria, xml.iForge, True)

        gc.setInitialBuilding(Consts.iTurkey, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iTurkey, xml.iBarracks, True)
        gc.setInitialBuilding(Consts.iTurkey, xml.iForge, True)
        gc.setInitialBuilding(Consts.iTurkey, xml.iHarbor, True)

        gc.setInitialBuilding(Consts.iSweden, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iSweden, xml.iBarracks, True)
        gc.setInitialBuilding(Consts.iSweden, xml.iHarbor, True)

        gc.setInitialBuilding(Consts.iDutch, xml.iGranary, True)
        gc.setInitialBuilding(Consts.iDutch, xml.iBarracks, True)
        gc.setInitialBuilding(Consts.iDutch, xml.iForge, True)
        gc.setInitialBuilding(Consts.iDutch, xml.iHarbor, True)
        gc.setInitialBuilding(Consts.iDutch, xml.iAqueduct, True)
        gc.setInitialBuilding(Consts.iDutch, xml.iMarket, True)
        gc.setInitialBuilding(Consts.iDutch, xml.iLighthouse, True)
        gc.setInitialBuilding(Consts.iDutch, xml.iTheatre, True)
        gc.setInitialBuilding(Consts.iDutch, xml.iSmokehouse, True)

        ####### AI Modifiers
        # 3Miro: setCityClusterAI(iCiv,iTop,iBottom,iMinus) for each AI civilization (set them for all, but only the AI make difference)
        # this determines how clustered the cities would be
        # AI_foundValue in PlayerAI would compute for a candidate city location the number of plots that are taken (i.e. by another city)
        # in CivIV, if more than a third of the tiles are "taken", do not found city there. In RFC, cities are clustered closer
        # if ( iTaken > 21 * iTop / iBottom - iMinus ) do not build city there.
        # RFC default values are 2/3 -1 for Europe, 1/3 - 0 for Russia and 1/2 for Mongolia
        # for example gc.setCityClusterAI( iByzantium, 1, 3, 0 ) wouldn't allow Byzantium to settle cities if more than 7 tiles are taken
        gc.setCityClusterAI(Consts.iByzantium, 1, 3, 0)  # won't settle if 8+ tiles are taken
        gc.setCityClusterAI(Consts.iFrankia, 1, 3, 0)  # 8
        gc.setCityClusterAI(Consts.iArabia, 1, 3, 1)  # 7
        gc.setCityClusterAI(Consts.iBulgaria, 2, 3, 4)  # 11
        gc.setCityClusterAI(Consts.iCordoba, 1, 2, 1)  # 10
        gc.setCityClusterAI(Consts.iVenecia, 2, 3, 1)  # 14
        gc.setCityClusterAI(Consts.iBurgundy, 2, 3, 3)  # 12
        gc.setCityClusterAI(Consts.iGermany, 2, 3, 4)  # 11
        gc.setCityClusterAI(Consts.iNovgorod, 1, 3, 2)  # 6
        gc.setCityClusterAI(Consts.iNorway, 1, 2, 1)  # 10
        gc.setCityClusterAI(Consts.iKiev, 1, 3, 2)  # 6
        gc.setCityClusterAI(Consts.iHungary, 2, 3, 3)  # 12
        gc.setCityClusterAI(Consts.iSpain, 1, 2, 1)  # 10
        gc.setCityClusterAI(Consts.iDenmark, 2, 3, 3)  # 12
        gc.setCityClusterAI(Consts.iScotland, 2, 3, 2)  # 13
        gc.setCityClusterAI(Consts.iPoland, 1, 3, 0)  # 8
        gc.setCityClusterAI(Consts.iGenoa, 2, 3, 1)  # 14
        gc.setCityClusterAI(Consts.iMorocco, 1, 3, 2)  # 6
        gc.setCityClusterAI(Consts.iEngland, 1, 2, 1)  # 10
        gc.setCityClusterAI(Consts.iPortugal, 2, 3, 1)  # 14
        gc.setCityClusterAI(Consts.iAragon, 2, 3, 1)  # 14
        gc.setCityClusterAI(Consts.iSweden, 1, 2, 2)  # 9
        gc.setCityClusterAI(Consts.iPrussia, 2, 3, 1)  # 14
        gc.setCityClusterAI(Consts.iLithuania, 1, 3, 0)  # 8
        gc.setCityClusterAI(Consts.iAustria, 2, 3, 3)  # 12
        gc.setCityClusterAI(Consts.iTurkey, 1, 3, 1)  # 7
        gc.setCityClusterAI(Consts.iMoscow, 1, 4, 1)  # 5
        gc.setCityClusterAI(Consts.iDutch, 2, 3, 1)  # 14

        # 3Miro: setCityWarDistanceAI(iCiv,iVal), depending on the type of the empire, modify how likely the AI is to attack a city
        # values are 1 - small empires, 2 - large continuous empires, 3 - not necessarily continuous empires
        gc.setCityWarDistanceAI(Consts.iByzantium, 2)
        gc.setCityWarDistanceAI(Consts.iFrankia, 2)
        gc.setCityWarDistanceAI(Consts.iArabia, 2)
        gc.setCityWarDistanceAI(Consts.iBulgaria, 1)
        gc.setCityWarDistanceAI(Consts.iCordoba, 2)
        gc.setCityWarDistanceAI(Consts.iVenecia, 3)
        gc.setCityWarDistanceAI(Consts.iBurgundy, 1)
        gc.setCityWarDistanceAI(Consts.iGermany, 2)
        gc.setCityWarDistanceAI(Consts.iNovgorod, 2)
        gc.setCityWarDistanceAI(Consts.iNorway, 3)
        gc.setCityWarDistanceAI(Consts.iKiev, 2)
        gc.setCityWarDistanceAI(Consts.iHungary, 2)
        gc.setCityWarDistanceAI(Consts.iSpain, 3)
        gc.setCityWarDistanceAI(Consts.iDenmark, 2)
        gc.setCityWarDistanceAI(Consts.iScotland, 1)
        gc.setCityWarDistanceAI(Consts.iPoland, 2)
        gc.setCityWarDistanceAI(Consts.iGenoa, 3)
        gc.setCityWarDistanceAI(Consts.iMorocco, 2)
        gc.setCityWarDistanceAI(Consts.iEngland, 3)
        gc.setCityWarDistanceAI(Consts.iPortugal, 3)
        gc.setCityWarDistanceAI(Consts.iAragon, 3)
        gc.setCityWarDistanceAI(Consts.iSweden, 3)
        gc.setCityWarDistanceAI(Consts.iPrussia, 2)
        gc.setCityWarDistanceAI(Consts.iLithuania, 2)
        gc.setCityWarDistanceAI(Consts.iAustria, 2)
        gc.setCityWarDistanceAI(Consts.iTurkey, 2)
        gc.setCityWarDistanceAI(Consts.iMoscow, 2)
        gc.setCityWarDistanceAI(Consts.iDutch, 1)

        # 3Miro: setTechPreferenceAI(iCiv,iTech,iVal), for each civ, for each tech, specify how likable it is. iVal is same as in growth.
        # low percent makes the tech less desirable
        gc.setTechPreferenceAI(Consts.iBulgaria, xml.iBronzeCasting, 200)
        gc.setTechPreferenceAI(Consts.iGermany, xml.iPrintingPress, 200)
        gc.setTechPreferenceAI(Consts.iEngland, xml.iPrintingPress, 150)
        gc.setTechPreferenceAI(Consts.iPope, xml.iPrintingPress, 10)  # Pope shouldn't want this
        gc.setTechPreferenceAI(Consts.iSpain, xml.iAstronomy, 200)
        gc.setTechPreferenceAI(Consts.iPortugal, xml.iAstronomy, 200)

        # 3Miro: setDiplomacyModifiers(iCiv1,iCiv2,iVal) hidden modifier for the two civ's AI relations. More likely to have OB and so on.
        # + means they will like each other - they will hate each other.
        # from Civ1 towards Civ2 (make them symmetric)
        gc.setDiplomacyModifiers(Consts.iCordoba, Consts.iArabia, +5)
        gc.setDiplomacyModifiers(Consts.iArabia, Consts.iCordoba, +5)
        gc.setDiplomacyModifiers(Consts.iArabia, Consts.iByzantium, -8)
        gc.setDiplomacyModifiers(Consts.iByzantium, Consts.iArabia, -8)
        gc.setDiplomacyModifiers(Consts.iBulgaria, Consts.iByzantium, +3)
        gc.setDiplomacyModifiers(Consts.iByzantium, Consts.iBulgaria, +3)
        gc.setDiplomacyModifiers(Consts.iCordoba, Consts.iSpain, -14)
        gc.setDiplomacyModifiers(Consts.iSpain, Consts.iCordoba, -14)
        gc.setDiplomacyModifiers(Consts.iMorocco, Consts.iSpain, -10)
        gc.setDiplomacyModifiers(Consts.iSpain, Consts.iMorocco, -10)
        gc.setDiplomacyModifiers(Consts.iAragon, Consts.iSpain, +4)
        gc.setDiplomacyModifiers(Consts.iSpain, Consts.iAragon, +4)
        gc.setDiplomacyModifiers(Consts.iPortugal, Consts.iSpain, +6)
        gc.setDiplomacyModifiers(Consts.iSpain, Consts.iPortugal, +6)
        gc.setDiplomacyModifiers(Consts.iCordoba, Consts.iPortugal, -8)
        gc.setDiplomacyModifiers(Consts.iPortugal, Consts.iCordoba, -8)
        gc.setDiplomacyModifiers(Consts.iKiev, Consts.iNovgorod, +5)
        gc.setDiplomacyModifiers(Consts.iNovgorod, Consts.iKiev, +5)
        gc.setDiplomacyModifiers(Consts.iMoscow, Consts.iNovgorod, -8)
        gc.setDiplomacyModifiers(Consts.iNovgorod, Consts.iMoscow, -8)
        gc.setDiplomacyModifiers(Consts.iFrankia, Consts.iBurgundy, -2)
        gc.setDiplomacyModifiers(Consts.iBurgundy, Consts.iFrankia, -2)
        gc.setDiplomacyModifiers(Consts.iTurkey, Consts.iByzantium, -14)
        gc.setDiplomacyModifiers(Consts.iByzantium, Consts.iTurkey, -14)
        gc.setDiplomacyModifiers(Consts.iGermany, Consts.iPoland, -5)
        gc.setDiplomacyModifiers(Consts.iPoland, Consts.iGermany, -5)
        gc.setDiplomacyModifiers(Consts.iMoscow, Consts.iPoland, -4)
        gc.setDiplomacyModifiers(Consts.iPoland, Consts.iMoscow, -4)
        gc.setDiplomacyModifiers(Consts.iMoscow, Consts.iLithuania, -2)
        gc.setDiplomacyModifiers(Consts.iLithuania, Consts.iMoscow, -2)
        gc.setDiplomacyModifiers(Consts.iAustria, Consts.iPoland, -2)
        gc.setDiplomacyModifiers(Consts.iPoland, Consts.iAustria, -2)
        gc.setDiplomacyModifiers(Consts.iLithuania, Consts.iPoland, +4)
        gc.setDiplomacyModifiers(Consts.iPoland, Consts.iLithuania, +4)
        gc.setDiplomacyModifiers(Consts.iHungary, Consts.iPoland, +3)
        gc.setDiplomacyModifiers(Consts.iPoland, Consts.iHungary, +3)
        gc.setDiplomacyModifiers(Consts.iAustria, Consts.iHungary, -6)
        gc.setDiplomacyModifiers(Consts.iHungary, Consts.iAustria, -6)
        gc.setDiplomacyModifiers(Consts.iSweden, Consts.iPoland, -2)
        gc.setDiplomacyModifiers(Consts.iPoland, Consts.iSweden, -2)
        gc.setDiplomacyModifiers(Consts.iSweden, Consts.iMoscow, -8)
        gc.setDiplomacyModifiers(Consts.iMoscow, Consts.iSweden, -8)
        gc.setDiplomacyModifiers(Consts.iPrussia, Consts.iPoland, -6)
        gc.setDiplomacyModifiers(Consts.iPoland, Consts.iPrussia, -6)
        gc.setDiplomacyModifiers(Consts.iPrussia, Consts.iLithuania, -8)
        gc.setDiplomacyModifiers(Consts.iLithuania, Consts.iPrussia, -8)
        gc.setDiplomacyModifiers(Consts.iEngland, Consts.iScotland, -8)
        gc.setDiplomacyModifiers(Consts.iScotland, Consts.iEngland, -8)
        gc.setDiplomacyModifiers(Consts.iFrankia, Consts.iScotland, +4)
        gc.setDiplomacyModifiers(Consts.iScotland, Consts.iFrankia, +4)
        gc.setDiplomacyModifiers(Consts.iNorway, Consts.iDenmark, +4)
        gc.setDiplomacyModifiers(Consts.iDenmark, Consts.iNorway, +4)
        gc.setDiplomacyModifiers(Consts.iSweden, Consts.iDenmark, -4)
        gc.setDiplomacyModifiers(Consts.iDenmark, Consts.iSweden, -4)

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

        gc.setUP(Consts.iBurgundy, Consts.iUP_Happiness, 1)
        gc.setUP(Consts.iBurgundy, Consts.iUP_PerCityCommerce, 200)

        gc.setUP(Consts.iByzantium, Consts.iUP_Emperor, 1)
        gc.setUP(Consts.iByzantium, Consts.iUP_EnableCivics, xml.iCivicImperialism)

        gc.setUP(Consts.iFrankia, Consts.iUP_LandStability, 1)

        gc.setUP(Consts.iArabia, Consts.iUP_Faith, 1)

        gc.setUP(Consts.iBulgaria, Consts.iUP_NoResistance, 0)

        gc.setUP(Consts.iCordoba, Consts.iUP_PromotionI, xml.iPromotionMedic1)
        gc.setUP(Consts.iCordoba, Consts.iUP_HealthFood, 50)

        gc.setUP(
            Consts.iMorocco,
            Consts.iUP_TerrainBonus,
            1 * 100000 + xml.iTerrainDesert * 1000 + 10 + 1,
        )
        gc.setUP(
            Consts.iMorocco, Consts.iUP_FeatureBonus, 1 * 100000 + xml.iOasis * 1000 + 100 + 1
        )

        gc.setUP(Consts.iSpain, Consts.iUP_Inquisition, 1)
        gc.setUP(Consts.iSpain, Consts.iUP_PerCityCommerce, 2)

        gc.setUP(Consts.iNorway, Consts.iUP_CanEnterTerrain, xml.iTerrainOcean)
        gc.setUP(Consts.iNorway, Consts.iUP_StabilitySettler, 1)  # "hidden" part of the UP

        gc.setUP(Consts.iVenecia, Consts.iUP_EnableCivics, xml.iCivicMerchantRepublic)
        # gc.setUP( iVenecia, iUP_ForeignSea, 1 )

        gc.setUP(Consts.iKiev, Consts.iUP_CityTileYield, 1 * 1000 + 100 * 2)

        gc.setUP(Consts.iHungary, Consts.iUP_Happiness, 1)
        gc.setUP(Consts.iHungary, Consts.iUP_CulturalTolerance, 0)

        gc.setUP(Consts.iGermany, Consts.iUP_UnitProduction, xml.iGunpowder * 100 + 75)

        gc.setUP(Consts.iPoland, Consts.iUP_ReligiousTolerance, 0)

        gc.setUP(Consts.iLithuania, Consts.iUP_PaganCulture, 200)
        gc.setUP(Consts.iLithuania, Consts.iUP_PaganHappy, 1)

        gc.setSupportModifiersAI(Consts.iMoscow, 10, 100, 20, 10, 100)  # sync with preset values
        gc.setSupportModifiersHu(Consts.iMoscow, 10, 100, 20, 10, 100)  # sync with preset values
        gc.setUP(Consts.iMoscow, Consts.iUP_EndlessLand, 50)

        gc.setUP(
            Consts.iGenoa, Consts.iUP_Mercenaries, 1
        )  # Absinthe: this actually has no effect, it is implemented in Mercenaries.py entirely

        gc.setUP(
            Consts.iScotland,
            Consts.iUP_ImprovementBonus,
            1 * 100000 + xml.iImprovementFort * 1000 + 2,
        )

        gc.setUP(
            Consts.iEngland,
            Consts.iUP_ImprovementBonus,
            1 * 100000 + xml.iImprovementWorkshop * 1000 + 1,
        )
        gc.setUP(
            Consts.iEngland,
            Consts.iUP_ImprovementBonus2,
            1 * 100000 + xml.iImprovementCottage * 1000 + 10,
        )
        gc.setUP(
            Consts.iEngland,
            Consts.iUP_ImprovementBonus3,
            1 * 100000 + xml.iImprovementHamlet * 1000 + 10,
        )
        gc.setUP(
            Consts.iEngland,
            Consts.iUP_ImprovementBonus4,
            1 * 100000 + xml.iImprovementVillage * 1000 + 10,
        )
        gc.setUP(
            Consts.iEngland,
            Consts.iUP_ImprovementBonus5,
            1 * 100000 + xml.iImprovementTown * 1000 + 10,
        )

        # Speed up East/West India Trading Companies and all Colonies
        gc.setUP(
            Consts.iPortugal,
            Consts.iUP_Discovery,
            (xml.iNumNotColonies - 2) * 1000000 + (xml.iNumTotalColonies - 1) * 1000 + 30,
        )
        gc.setUP(Consts.iPortugal, Consts.iUP_StabilitySettler, 1)  # "hidden" part of the UP

        for i in range(Consts.iNumTotalPlayers):
            if not i == Consts.iAustria:
                gc.setDiplomacyModifiers(i, Consts.iAustria, +4)
        gc.setUP(Consts.iAustria, Consts.iUP_PerCityCommerce, 200)

        # gc.setUP( iTurkey, iUP_Conscription, 330 )
        # gc.setUP( iTurkey, iUP_Conscription, 1 )
        gc.setUP(Consts.iTurkey, Consts.iUP_Janissary, 1)

        gc.setUP(Consts.iSweden, Consts.iUP_PromotionI, xml.iPromotionFormation)

        gc.setUP(Consts.iNovgorod, Consts.iUP_EnableCivics, xml.iCivicBureaucracy)

        gc.setUP(Consts.iPrussia, Consts.iUP_EnableCivics, xml.iCivicTheocracy)
        # Absinthe: handled in python currently
        # gc.setUP( iPrussia, iUP_NoAnarchyInstability, 1 )

        # Absinthe: handled in python currently
        # gc.setUP( iAragon, iUP_ProvinceCommerce, 0 )

        # Absinthe: handled in python currently
        # gc.setUP( iScotland, iUP_Defiance, 1 )

        gc.setUP(Consts.iDutch, Consts.iUP_TradeRoutes, 2)
        gc.setUP(
            Consts.iDutch, Consts.iUP_Pious, 2
        )  # 3Miro: "hidden" buff to the Dutch FP, otherwise they have too little piety (not enough cities)
        gc.setUP(
            Consts.iDutch,
            Consts.iUP_Discovery,
            (xml.iNumNotColonies - 2) * 1000000 + (xml.iNumTotalColonies - 1) * 1000 + 30,
        )  # "hidden" part of the UP

        gc.setUP(Consts.iPope, Consts.iUP_Emperor, 1)

        # GlobalWarming
        gc.setGlobalWarming(False)

        # Set FastTerrain (i.e. double movement over ocean)
        gc.setFastTerrain(xml.iTerrainOcean)

        # set religious spread factors
        for iCiv in range(Consts.iNumTotalPlayers + 1):  # include barbs
            for iRel in range(xml.iNumReligions):
                gc.setReligionSpread(iCiv, iRel, Consts.tReligionSpreadFactor[iCiv][iRel])

        # set the religions and year of the great schism
        gc.setSchism(xml.iCatholicism, xml.iOrthodoxy, xml.i1053AD)

        gc.setHoliestCity(Consts.tJerusalem[0], Consts.tJerusalem[1])

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

        gc.setReligionBenefit(xml.iOrthodoxy, Consts.iFP_Stability, 10, 100)
        gc.setReligionBenefit(xml.iOrthodoxy, Consts.iFP_Civic, 50, 100)

        gc.setReligionBenefit(xml.iIslam, Consts.iFP_Growth, 50, 100)
        gc.setReligionBenefit(xml.iIslam, Consts.iFP_Units, 50, 100)

        gc.setReligionBenefit(xml.iProtestantism, Consts.iFP_Science, 30, 100)
        gc.setReligionBenefit(xml.iProtestantism, Consts.iFP_Production, 30, 100)

        gc.setReligionBenefit(xml.iCatholicism, Consts.iFP_Diplomacy, 6, 100)
        gc.setReligionBenefit(xml.iIslam, Consts.iFP_Diplomacy, 5, 100)
        gc.setReligionBenefit(xml.iProtestantism, Consts.iFP_Diplomacy, 4, 100)
        gc.setReligionBenefit(xml.iOrthodoxy, Consts.iFP_Diplomacy, 3, 100)

        # a land tile that is normally impassable but the desired player can pass through it
        # gc.setStrategicTile( iVenecia, 56, 35 )

        # set AI modifiers for preferred buildings
        # use values -10 for very unlikely, 0 for default neutral and positive for desirable
        # values less than -10 might not work, above 10 should be fine

        # the utils.getUniqueBuilding function does not work, probably the util functions are not yet usable when these initial values are set
        # but in the .dll these values are only used for the civ-specific building of the given buildingclass, so we can these add redundantly
        for iPlayer in range(Consts.iNumPlayers):
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

        gc.setBuildingPref(Consts.iByzantium, xml.iStCatherineMonastery, 15)
        gc.setBuildingPref(Consts.iByzantium, xml.iBoyanaChurch, 2)
        gc.setBuildingPref(Consts.iByzantium, xml.iRoundChurch, 2)
        gc.setBuildingPref(Consts.iByzantium, xml.iSophiaKiev, 5)

        gc.setBuildingPref(Consts.iFrankia, xml.iNotreDame, 20)
        gc.setBuildingPref(Consts.iFrankia, xml.iVersailles, 20)
        gc.setBuildingPref(Consts.iFrankia, xml.iFontainebleau, 10)
        gc.setBuildingPref(Consts.iFrankia, xml.iMonasteryOfCluny, 10)
        gc.setBuildingPref(Consts.iFrankia, xml.iMontSaintMichel, 10)
        gc.setBuildingPref(Consts.iFrankia, xml.iPalaisPapes, 5)
        gc.setBuildingPref(Consts.iFrankia, xml.iLouvre, 20)

        gc.setBuildingPref(Consts.iArabia, xml.iDomeRock, 15)
        gc.setBuildingPref(Consts.iArabia, xml.iTombAlWalid, 20)
        gc.setBuildingPref(Consts.iArabia, xml.iAlAzhar, 20)
        gc.setBuildingPref(Consts.iArabia, xml.iMosqueOfKairouan, 10)
        gc.setBuildingPref(Consts.iArabia, xml.iKoutoubiaMosque, 5)
        gc.setBuildingPref(Consts.iArabia, xml.iGardensAlAndalus, 5)
        gc.setBuildingPref(Consts.iArabia, xml.iLaMezquita, 5)
        gc.setBuildingPref(Consts.iArabia, xml.iAlhambra, 5)
        gc.setBuildingPref(Consts.iArabia, xml.iNotreDame, -5)
        gc.setBuildingPref(Consts.iArabia, xml.iStephansdom, -5)
        gc.setBuildingPref(Consts.iArabia, xml.iSistineChapel, -5)
        gc.setBuildingPref(Consts.iArabia, xml.iKrakDesChevaliers, -5)
        gc.setBuildingPref(Consts.iArabia, xml.iLeaningTower, -3)
        gc.setBuildingPref(Consts.iArabia, xml.iGoldenBull, -3)
        gc.setBuildingPref(Consts.iArabia, xml.iCopernicus, -3)

        gc.setBuildingPref(Consts.iBulgaria, xml.iRoundChurch, 20)
        gc.setBuildingPref(Consts.iBulgaria, xml.iBoyanaChurch, 20)
        gc.setBuildingPref(Consts.iBulgaria, xml.iStCatherineMonastery, 5)
        gc.setBuildingPref(Consts.iBulgaria, xml.iSophiaKiev, 5)

        gc.setBuildingPref(Consts.iCordoba, xml.iGardensAlAndalus, 20)
        gc.setBuildingPref(Consts.iCordoba, xml.iLaMezquita, 20)
        gc.setBuildingPref(Consts.iCordoba, xml.iAlhambra, 20)
        gc.setBuildingPref(Consts.iCordoba, xml.iDomeRock, 10)
        gc.setBuildingPref(Consts.iCordoba, xml.iAlAzhar, 5)
        gc.setBuildingPref(Consts.iCordoba, xml.iMosqueOfKairouan, 10)
        gc.setBuildingPref(Consts.iCordoba, xml.iKoutoubiaMosque, 5)
        gc.setBuildingPref(Consts.iCordoba, xml.iNotreDame, -5)
        gc.setBuildingPref(Consts.iCordoba, xml.iStephansdom, -5)
        gc.setBuildingPref(Consts.iCordoba, xml.iSistineChapel, -5)
        gc.setBuildingPref(Consts.iCordoba, xml.iKrakDesChevaliers, -5)
        gc.setBuildingPref(Consts.iCordoba, xml.iLeaningTower, -3)
        gc.setBuildingPref(Consts.iCordoba, xml.iGoldenBull, -3)

        gc.setBuildingPref(Consts.iVenecia, xml.iMarcoPolo, 15)
        gc.setBuildingPref(Consts.iVenecia, xml.iSanMarco, 20)
        gc.setBuildingPref(Consts.iVenecia, xml.iLanterna, 10)
        gc.setBuildingPref(Consts.iVenecia, xml.iLeonardosWorkshop, 5)
        gc.setBuildingPref(Consts.iVenecia, xml.iLeaningTower, 5)
        gc.setBuildingPref(Consts.iVenecia, xml.iGrandArsenal, 20)
        gc.setBuildingPref(Consts.iVenecia, xml.iGalataTower, 10)
        gc.setBuildingPref(Consts.iVenecia, xml.iFlorenceDuomo, 10)
        gc.setBuildingPref(Consts.iVenecia, xml.iSanGiorgio, 5)

        gc.setBuildingPref(Consts.iBurgundy, xml.iMonasteryOfCluny, 20)
        gc.setBuildingPref(Consts.iBurgundy, xml.iNotreDame, 10)
        gc.setBuildingPref(Consts.iBurgundy, xml.iVersailles, 10)
        gc.setBuildingPref(Consts.iBurgundy, xml.iMontSaintMichel, 10)
        gc.setBuildingPref(Consts.iBurgundy, xml.iFontainebleau, 5)
        gc.setBuildingPref(Consts.iBurgundy, xml.iPalaisPapes, 5)
        gc.setBuildingPref(Consts.iBurgundy, xml.iLouvre, 10)

        gc.setBuildingPref(Consts.iGermany, xml.iBrandenburgGate, 10)
        gc.setBuildingPref(Consts.iGermany, xml.iImperialDiet, 20)
        gc.setBuildingPref(Consts.iGermany, xml.iCopernicus, 5)
        gc.setBuildingPref(Consts.iGermany, xml.iGoldenBull, 10)
        gc.setBuildingPref(Consts.iGermany, xml.iMonasteryOfCluny, 5)
        gc.setBuildingPref(Consts.iGermany, xml.iUraniborg, 5)
        gc.setBuildingPref(Consts.iGermany, xml.iThomaskirche, 20)

        gc.setBuildingPref(Consts.iNovgorod, xml.iStBasil, 10)
        gc.setBuildingPref(Consts.iNovgorod, xml.iSophiaKiev, 10)
        gc.setBuildingPref(Consts.iNovgorod, xml.iRoundChurch, 5)
        gc.setBuildingPref(Consts.iNovgorod, xml.iBoyanaChurch, 5)
        gc.setBuildingPref(Consts.iNovgorod, xml.iBorgundStaveChurch, 5)
        gc.setBuildingPref(Consts.iNovgorod, xml.iPeterhofPalace, 15)

        gc.setBuildingPref(Consts.iNorway, xml.iShrineOfUppsala, 20)
        gc.setBuildingPref(Consts.iNorway, xml.iSamogitianAlkas, 5)
        gc.setBuildingPref(Consts.iNorway, xml.iBorgundStaveChurch, 15)
        gc.setBuildingPref(Consts.iNorway, xml.iUraniborg, 10)
        gc.setBuildingPref(Consts.iNorway, xml.iKalmarCastle, 5)

        gc.setBuildingPref(Consts.iKiev, xml.iSophiaKiev, 20)
        gc.setBuildingPref(Consts.iKiev, xml.iStBasil, 5)
        gc.setBuildingPref(Consts.iKiev, xml.iRoundChurch, 5)
        gc.setBuildingPref(Consts.iKiev, xml.iBoyanaChurch, 5)
        gc.setBuildingPref(Consts.iKiev, xml.iPeterhofPalace, 10)

        gc.setBuildingPref(Consts.iHungary, xml.iPressburg, 20)
        gc.setBuildingPref(Consts.iHungary, xml.iGoldenBull, 20)
        gc.setBuildingPref(Consts.iHungary, xml.iBibliothecaCorviniana, 20)
        gc.setBuildingPref(Consts.iHungary, xml.iKazimierz, 10)
        gc.setBuildingPref(Consts.iHungary, xml.iCopernicus, 5)
        gc.setBuildingPref(Consts.iHungary, xml.iStephansdom, 5)

        gc.setBuildingPref(Consts.iSpain, xml.iEscorial, 20)
        gc.setBuildingPref(Consts.iSpain, xml.iMagellansVoyage, 10)
        gc.setBuildingPref(Consts.iSpain, xml.iTorreDelOro, 20)
        gc.setBuildingPref(Consts.iSpain, xml.iBelemTower, 10)

        gc.setBuildingPref(Consts.iDenmark, xml.iKalmarCastle, 10)
        gc.setBuildingPref(Consts.iDenmark, xml.iShrineOfUppsala, 20)
        gc.setBuildingPref(Consts.iDenmark, xml.iSamogitianAlkas, 5)
        gc.setBuildingPref(Consts.iDenmark, xml.iBorgundStaveChurch, 15)
        gc.setBuildingPref(Consts.iDenmark, xml.iUraniborg, 20)

        gc.setBuildingPref(Consts.iScotland, xml.iMagnaCarta, 10)
        gc.setBuildingPref(Consts.iScotland, xml.iWestminster, 10)
        gc.setBuildingPref(Consts.iScotland, xml.iMonasteryOfCluny, 5)
        gc.setBuildingPref(Consts.iScotland, xml.iBorgundStaveChurch, 5)
        gc.setBuildingPref(Consts.iScotland, xml.iMontSaintMichel, 5)

        gc.setBuildingPref(Consts.iPoland, xml.iPressburg, 10)
        gc.setBuildingPref(Consts.iPoland, xml.iCopernicus, 10)
        gc.setBuildingPref(Consts.iPoland, xml.iGoldenBull, 5)
        gc.setBuildingPref(Consts.iPoland, xml.iKazimierz, 15)
        gc.setBuildingPref(Consts.iPoland, xml.iJasnaGora, 20)
        gc.setBuildingPref(Consts.iPoland, xml.iBrandenburgGate, 5)

        gc.setBuildingPref(Consts.iGenoa, xml.iSanGiorgio, 20)
        gc.setBuildingPref(Consts.iGenoa, xml.iLanterna, 20)
        gc.setBuildingPref(Consts.iGenoa, xml.iLeonardosWorkshop, 5)
        gc.setBuildingPref(Consts.iGenoa, xml.iLeaningTower, 5)
        gc.setBuildingPref(Consts.iGenoa, xml.iSanMarco, 5)
        gc.setBuildingPref(Consts.iGenoa, xml.iMarcoPolo, 5)
        gc.setBuildingPref(Consts.iGenoa, xml.iGrandArsenal, 10)
        gc.setBuildingPref(Consts.iGenoa, xml.iGalataTower, 20)
        gc.setBuildingPref(Consts.iGenoa, xml.iFlorenceDuomo, 10)

        gc.setBuildingPref(Consts.iMorocco, xml.iGardensAlAndalus, 10)
        gc.setBuildingPref(Consts.iMorocco, xml.iLaMezquita, 10)
        gc.setBuildingPref(Consts.iMorocco, xml.iAlhambra, 10)
        gc.setBuildingPref(Consts.iMorocco, xml.iDomeRock, 10)
        gc.setBuildingPref(Consts.iMorocco, xml.iAlAzhar, 5)
        gc.setBuildingPref(Consts.iMorocco, xml.iMosqueOfKairouan, 10)
        gc.setBuildingPref(Consts.iMorocco, xml.iKoutoubiaMosque, 20)
        gc.setBuildingPref(Consts.iMorocco, xml.iNotreDame, -5)
        gc.setBuildingPref(Consts.iMorocco, xml.iStephansdom, -5)
        gc.setBuildingPref(Consts.iMorocco, xml.iSistineChapel, -5)
        gc.setBuildingPref(Consts.iMorocco, xml.iKrakDesChevaliers, -5)
        gc.setBuildingPref(Consts.iMorocco, xml.iLeaningTower, -3)
        gc.setBuildingPref(Consts.iMorocco, xml.iGoldenBull, -3)

        gc.setBuildingPref(Consts.iEngland, xml.iMagnaCarta, 20)
        gc.setBuildingPref(Consts.iEngland, xml.iWestminster, 20)
        gc.setBuildingPref(Consts.iEngland, xml.iMonasteryOfCluny, 5)
        gc.setBuildingPref(Consts.iEngland, xml.iUraniborg, 5)
        gc.setBuildingPref(Consts.iEngland, xml.iTorreDelOro, 5)
        gc.setBuildingPref(Consts.iEngland, xml.iBelemTower, 5)

        gc.setBuildingPref(Consts.iPortugal, xml.iBelemTower, 20)
        gc.setBuildingPref(Consts.iPortugal, xml.iPalacioDaPena, 20)
        gc.setBuildingPref(Consts.iPortugal, xml.iMagellansVoyage, 20)
        gc.setBuildingPref(Consts.iPortugal, xml.iTorreDelOro, 10)

        gc.setBuildingPref(Consts.iAragon, xml.iMagellansVoyage, 10)
        gc.setBuildingPref(Consts.iAragon, xml.iTorreDelOro, 10)
        gc.setBuildingPref(Consts.iAragon, xml.iEscorial, 5)
        gc.setBuildingPref(Consts.iAragon, xml.iBelemTower, 10)

        gc.setBuildingPref(Consts.iSweden, xml.iKalmarCastle, 20)
        gc.setBuildingPref(Consts.iSweden, xml.iShrineOfUppsala, 5)
        gc.setBuildingPref(Consts.iSweden, xml.iBorgundStaveChurch, 15)
        gc.setBuildingPref(Consts.iSweden, xml.iUraniborg, 10)

        gc.setBuildingPref(Consts.iPrussia, xml.iBrandenburgGate, 20)
        gc.setBuildingPref(Consts.iPrussia, xml.iThomaskirche, 10)
        gc.setBuildingPref(Consts.iPrussia, xml.iCopernicus, 5)
        gc.setBuildingPref(Consts.iPrussia, xml.iPressburg, 5)

        gc.setBuildingPref(Consts.iLithuania, xml.iSamogitianAlkas, 20)
        gc.setBuildingPref(Consts.iLithuania, xml.iGediminasTower, 20)
        gc.setBuildingPref(Consts.iLithuania, xml.iBorgundStaveChurch, 5)

        gc.setBuildingPref(Consts.iAustria, xml.iStephansdom, 20)
        gc.setBuildingPref(Consts.iAustria, xml.iThomaskirche, 15)
        gc.setBuildingPref(Consts.iAustria, xml.iCopernicus, 5)
        gc.setBuildingPref(Consts.iAustria, xml.iGoldenBull, 5)
        gc.setBuildingPref(Consts.iAustria, xml.iPressburg, 5)
        gc.setBuildingPref(Consts.iAustria, xml.iAustrianOperaHouse, 10)

        gc.setBuildingPref(Consts.iTurkey, xml.iTopkapiPalace, 20)
        gc.setBuildingPref(Consts.iTurkey, xml.iBlueMosque, 20)
        gc.setBuildingPref(Consts.iTurkey, xml.iSelimiyeMosque, 20)
        gc.setBuildingPref(Consts.iTurkey, xml.iTombAlWalid, 10)
        gc.setBuildingPref(Consts.iTurkey, xml.iKizilKule, 10)
        gc.setBuildingPref(Consts.iTurkey, xml.iAlAzhar, 5)

        gc.setBuildingPref(Consts.iMoscow, xml.iStBasil, 20)
        gc.setBuildingPref(Consts.iMoscow, xml.iPeterhofPalace, 20)
        gc.setBuildingPref(Consts.iMoscow, xml.iSophiaKiev, 5)

        gc.setBuildingPref(Consts.iDutch, xml.iBeurs, 20)
        gc.setBuildingPref(Consts.iDutch, xml.iUraniborg, 5)
        gc.setBuildingPref(Consts.iDutch, xml.iThomaskirche, 5)

        gc.setBuildingPref(Consts.iPope, xml.iSistineChapel, 20)
        gc.setBuildingPref(Consts.iPope, xml.iPalaisPapes, 10)
        gc.setBuildingPref(Consts.iPope, xml.iLeaningTower, 5)
        gc.setBuildingPref(Consts.iPope, xml.iFlorenceDuomo, 5)
        gc.setBuildingPref(Consts.iPope, xml.iLeonardosWorkshop, 5)

        # 3Miro: set the Jews as the minor Religion
        gc.setMinorReligion(xml.iJudaism)
        gc.setMinorReligionRefugies(0)

        # Manor House + Manorialism: iBuilding + 1000 * iCivic + 100,000 * iGold + 1,000,000 * iResearch + 10,000,000 * iCulture + 100,000,000 * iEspionage
        # 3Miro: moved to XML, no need to put it here
        # gc.setBuildingCivicCommerseCombo1( xml.iManorHouse + 1000 * xml.iManorialism + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
        # gc.setBuildingCivicCommerseCombo2( xml.iFrenchChateau + 1000 * xml.iManorialism + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
        # gc.setBuildingCivicCommerseCombo3(-1)

        # 3Miro: Psycho AI cheat, this will make Ottoman AI think it can win battles vs Constantinople at 90/100 rate
        # 	it will also actually boost the Ottoman's odds (actually lower the defenders chance by 20 percent), but only when attacking Constantinople
        gc.setPsychoAICheat(
            Consts.iTurkey,
            Consts.tCapitals[Consts.iByzantium][0],
            Consts.tCapitals[Consts.iByzantium][1],
        )  # Constantinople (81, 24)

        # 3Miro: be very careful here, this can really mess the AI
        # 	setHistoricalEnemyAICheat( iAttacker, iDefender, 10 ) gives the attacker +10% bonus, when attacked units belong to the defender
        # 	this modifier only works in AI vs AI battles, it's ignored if either player is Human
        # 	none of the AI players is "aware" of the modification, if you make it too big, it could lead to a couple strange situations
        # 	(where the AI has clear advantage in a battle, yet it still won't attack)
        # 	so this should be a "last resort" solution, other methods are always preferable
        gc.setHistoricalEnemyAICheat(Consts.iTurkey, Consts.iBulgaria, 10)
        gc.setHistoricalEnemyAICheat(Consts.iBulgaria, Consts.iTurkey, -10)

        gc.setHistoricalEnemyAICheat(Consts.iSpain, Consts.iCordoba, 10)
        gc.setHistoricalEnemyAICheat(Consts.iCordoba, Consts.iSpain, -10)

        gc.setHistoricalEnemyAICheat(Consts.iPortugal, Consts.iSpain, 10)
        gc.setHistoricalEnemyAICheat(Consts.iSpain, Consts.iPortugal, -10)

        gc.setHistoricalEnemyAICheat(Consts.iAustria, Consts.iHungary, 10)
        gc.setHistoricalEnemyAICheat(Consts.iHungary, Consts.iAustria, -10)

        gc.setHistoricalEnemyAICheat(Consts.iAustria, Consts.iGermany, 10)
        gc.setHistoricalEnemyAICheat(Consts.iGermany, Consts.iAustria, -10)

        # 3Miro: this sets rules on how players can Vassalize, first two parameters are the players (we should probably keep this symmetric)
        # 	if the third parameter is -1: cannot Vassalize, 0: has to satisfy a condition (default), 1 can Vassalize without conditions
        # 	the condition is that either one of the players needs to have a city in a province that the other players considers >= the last parameter
        # 	the default for the last parameter is 0, we should call this at least once to set the parameter (it is the same for all players)
        gc.setVassalagaeCondition(Consts.iCordoba, Consts.iArabia, 1, Consts.iProvinceOuter)
        gc.setVassalagaeCondition(Consts.iArabia, Consts.iCordoba, 1, Consts.iProvinceOuter)

        # How much culture should we get into a province of this type, ignore the war and settler values (0,0)
        gc.setProvinceTypeParams(Consts.iProvinceNone, 0, 0, 1, 3)  # 1/3 culture
        gc.setProvinceTypeParams(Consts.iProvinceOuter, 0, 0, 1, 1)  # no change to culture
        gc.setProvinceTypeParams(Consts.iProvincePotential, 0, 0, 1, 1)  # same as outer culture
        gc.setProvinceTypeParams(Consts.iProvinceNatural, 0, 0, 2, 1)  # double-culture
        gc.setProvinceTypeParams(Consts.iProvinceCore, 0, 0, 3, 1)  # triple-culture

        # block foundation of Protestantism except by a Catholic player
        gc.setParentSchismReligions(xml.iCatholicism, xml.iProtestantism)

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
        gc.setTimelineTechDateForTech(xml.iStirrup, xml.i600AD)
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
        gc.setTimelineTechDateForTech(xml.iFeudalism, xml.i778AD)  # Feudalism
        gc.setTimelineTechDateForTech(xml.iFarriers, 100)
        gc.setTimelineTechDateForTech(xml.iMapMaking, 160)  # this is tier 5
        gc.setTimelineTechDateForTech(xml.iBlastFurnace, 120)  # teir 4
        gc.setTimelineTechDateForTech(xml.iSiegeEngines, xml.i1097AD)  # trebuchets
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
        gc.setTimelineTechDateForTech(xml.iAlchemy, xml.i1144AD)  # Alchemy introduced in Europe
        gc.setTimelineTechDateForTech(xml.iCivilService, 190)  # teir 6
        gc.setTimelineTechDateForTech(xml.iClockmaking, 200)
        gc.setTimelineTechDateForTech(xml.iPhilosophy, 215)
        gc.setTimelineTechDateForTech(xml.iEducation, 220)
        gc.setTimelineTechDateForTech(xml.iGuilds, 200)
        gc.setTimelineTechDateForTech(xml.iChivalry, 195)
        gc.setTimelineTechDateForTech(xml.iOptics, 228)  # teir 7
        gc.setTimelineTechDateForTech(xml.iReplaceableParts, 250)
        gc.setTimelineTechDateForTech(xml.iPatronage, 230)
        gc.setTimelineTechDateForTech(xml.iGunpowder, xml.i1300AD)
        gc.setTimelineTechDateForTech(xml.iBanking, 240)
        gc.setTimelineTechDateForTech(xml.iMilitaryTradition, 260)
        gc.setTimelineTechDateForTech(xml.iShipbuilding, 275)  # teir 8
        gc.setTimelineTechDateForTech(xml.iDrama, 270)
        gc.setTimelineTechDateForTech(xml.iDivineRight, 266)
        gc.setTimelineTechDateForTech(xml.iChemistry, 280)
        gc.setTimelineTechDateForTech(xml.iPaper, 290)
        gc.setTimelineTechDateForTech(xml.iProfessionalArmy, 295)
        gc.setTimelineTechDateForTech(xml.iPrintingPress, xml.i1517AD)  # teir 9 from turn 304
        gc.setTimelineTechDateForTech(xml.iPublicWorks, 310)
        gc.setTimelineTechDateForTech(xml.iMatchlock, xml.i1500AD)
        gc.setTimelineTechDateForTech(xml.iArabicKnowledge, xml.i1491AD)  # fall of Granada
        gc.setTimelineTechDateForTech(xml.iAstronomy, xml.i1514AD)  # teir 10 Copernicus
        gc.setTimelineTechDateForTech(xml.iSteamEngines, xml.i1690AD)  # first steam engine
        gc.setTimelineTechDateForTech(xml.iConstitution, 375)
        gc.setTimelineTechDateForTech(xml.iPolygonalFort, 370)
        gc.setTimelineTechDateForTech(xml.iArabicMedicine, 342)
        gc.setTimelineTechDateForTech(xml.iRenaissanceArt, xml.i1540AD)  # teir 11, 1541
        gc.setTimelineTechDateForTech(xml.iNationalism, 380)
        gc.setTimelineTechDateForTech(xml.iLiberalism, 400)
        gc.setTimelineTechDateForTech(xml.iScientificMethod, xml.i1623AD)  # Galilei
        gc.setTimelineTechDateForTech(xml.iMilitaryTactics, 410)
        gc.setTimelineTechDateForTech(xml.iNavalArchitecture, 385)  # teir 12
        gc.setTimelineTechDateForTech(xml.iCivilEngineering, 395)
        gc.setTimelineTechDateForTech(xml.iRightOfMan, 460)
        gc.setTimelineTechDateForTech(xml.iEconomics, 435)
        gc.setTimelineTechDateForTech(xml.iPhysics, xml.i1687AD)
        gc.setTimelineTechDateForTech(xml.iBiology, 440)
        gc.setTimelineTechDateForTech(xml.iCombinedArms, 430)
        gc.setTimelineTechDateForTech(xml.iTradingCompanies, xml.i1600AD)  # teir 13 from turn 325
        gc.setTimelineTechDateForTech(xml.iMachineTools, 450)
        gc.setTimelineTechDateForTech(xml.iFreeMarket, 450)
        gc.setTimelineTechDateForTech(xml.iExplosives, 460)
        gc.setTimelineTechDateForTech(xml.iMedicine, 458)
        gc.setTimelineTechDateForTech(xml.iIndustrialTech, xml.i1800AD)

    def preMapsNSizes(self):
        # settlersMaps, DO NOT CHANGE THIS CODE
        gc.setSizeNPlayers(
            Consts.iMapMaxX,
            Consts.iMapMaxY,
            Consts.iNumPlayers,
            Consts.iNumTotalPlayers,
            xml.iNumTechs,
            xml.iNumBuildingsPlague,
            xml.iNumReligions,
        )
        for i in range(Consts.iNumPlayers):
            for y in range(Consts.iMapMaxY):
                for x in range(Consts.iMapMaxX):
                    gc.setSettlersMap(i, y, x, rfcemaps.tSettlersMaps[i][y][x])
                    gc.setWarsMap(i, y, x, rfcemaps.tWarsMaps[i][y][x])

        for y in range(Consts.iMapMaxY):
            for x in range(Consts.iMapMaxX):
                if rfcemaps.tProvinceMap[y][x] > -1:
                    # "no province" of ocean is settled different than -1, set only non-negative values,
                    # the C++ map is initialized to "no-province" by setSizeNPlayers(...)
                    # "no-province" is returned as -1 via the Cy interface
                    gc.setProvince(x, y, rfcemaps.tProvinceMap[y][x])
        gc.createProvinceCrossreferenceList()  # make sure to call this AFTER setting all the Province entries

        gc.setProvinceTypeNumber(
            Consts.iNumProvinceTypes
        )  # set the Number of Provinces, call this before you set any AI or culture modifiers

        ## Absinthe: disabled, was only needed for the AI regions
        # gc.setNumRegions( xml.iNumMapRegions )
        # for lRegion in xml.tRegionMap:
        # 	iIndex = xml.tRegionMap.index( lRegion )
        # 	for iProvince in lRegion:
        # 		gc.setProvinceToRegion( iProvince, iIndex )

        # birth turns for the players, do not change this loop
        for i in range(Consts.iNumTotalPlayers):
            gc.setStartingTurn(i, Consts.tBirth[i])

    def postAreas(self):
        # 3Miro: DO NOT CHANGE THIS CODE
        # this adds the Core and Normal Areas from Consts.py into C++. There is Dynamical Memory involved, so don't change this
        for iCiv in range(Consts.iNumPlayers):
            iCBLx = Consts.tCoreAreasTL[iCiv][0]
            iCBLy = Consts.tCoreAreasTL[iCiv][1]
            iCTRx = Consts.tCoreAreasBR[iCiv][0]
            iCTRy = Consts.tCoreAreasBR[iCiv][1]
            iNBLx = Consts.tNormalAreasTL[iCiv][0]
            iNBLy = Consts.tNormalAreasTL[iCiv][1]
            iNTRx = Consts.tNormalAreasBR[iCiv][0]
            iNTRy = Consts.tNormalAreasBR[iCiv][1]
            iCCE = len(Consts.lExtraPlots[iCiv])
            iCNE = len(Consts.tNormalAreasSubtract[iCiv])
            gc.setCoreNormal(
                iCiv, iCBLx, iCBLy, iCTRx, iCTRy, iNBLx, iNBLy, iNTRx, iNTRy, iCCE, iCNE
            )
            for iEx in range(iCCE):
                gc.addCoreException(
                    iCiv, Consts.lExtraPlots[iCiv][iEx][0], Consts.lExtraPlots[iCiv][iEx][1]
                )
            for iEx in range(iCNE):
                gc.addNormalException(
                    iCiv,
                    Consts.tNormalAreasSubtract[iCiv][iEx][0],
                    Consts.tNormalAreasSubtract[iCiv][iEx][1],
                )

        gc.setProsecutorReligions(xml.iProsecutor, xml.iProsecutorClass)
        gc.setSaintParameters(
            xml.iGreatProphet, Consts.iSaintBenefit, 20, 40
        )  # try to amass at least 20 and don't bother above 40 points
        gc.setIndependnets(Consts.iIndepStart, Consts.iIndepEnd, Consts.iBarbarian)
        gc.setPapalPlayer(Consts.iPope, xml.iCatholicism)

        gc.setAutorunHack(xml.iCatapult, 32, 0)  # Autorun hack, sync with RNF module

        # 3MiroMercs: set the merc promotion
        gc.setMercPromotion(xml.iPromotionMerc)

        for iCiv in range(Consts.iNumPlayers):
            # print( "  sw: ",iCiv )
            gc.setStartingWorkers(iCiv, Consts.tStartingWorkers[iCiv])
