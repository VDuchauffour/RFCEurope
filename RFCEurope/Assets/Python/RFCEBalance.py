# RFC Europe, balancing modifiers are placed here
from CvPythonExtensions import *
from Consts import *
from XMLConsts import *
import RFCEMaps as rfcemaps

gc = CyGlobalContext()	# LOQ


class RFCEBalance:

	def setBalanceParameters( self ):

		self.preMapsNSizes()
		self.setTechTimeline() # Timeline for correct tech three

		# 3Miro: consolidate several modifiers into fewer calls, makes it more structured. Each modifier works as described below.

		#void setGrowthModifiers( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop );
		# iInitPop is the initial population in a city, also can use gc.setInitialPopulation( iCiv, iInitPop ) to change a single civ
		# defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100, 1 )
		# 3Miro: ABOUT CULTURE notice the culture modifier is different from the others, it modifies the culture output as opposed to the culture threshhold
		# 	50 means less culture, 200 means more culture. This is applied to Culture output of 10 or more.
		gc.setGrowthModifiersAI(iBurgundy,     100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersHu(iBurgundy,     100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersAI(iByzantium,    200, 100, 200, 100, 100, 2 )
		gc.setGrowthModifiersHu(iByzantium,    150, 100, 200, 100, 100, 2 )
		gc.setGrowthModifiersAI(iFrankia,      110, 100, 110, 100, 100, 1 )
		gc.setGrowthModifiersHu(iFrankia,      110, 100, 110, 100, 100, 1 )
		gc.setGrowthModifiersAI(iArabia,       150, 100, 150, 100, 100, 1 )
		gc.setGrowthModifiersHu(iArabia,       150, 100, 150, 100, 100, 1 )
		gc.setGrowthModifiersAI(iBulgaria,     150, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersHu(iBulgaria,     125, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersAI(iCordoba,      150, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersHu(iCordoba,      150, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersAI(iSpain,        125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iSpain,        125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iNorway,       100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iNorway,       100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iDenmark,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iDenmark,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iVenecia,      125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iVenecia,      125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iNovgorod,     100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iNovgorod,     100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iKiev,         150, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iKiev,         150, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iHungary,      125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iHungary,      125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iGermany,      125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iGermany,      125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iScotland,     100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iScotland,     100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iPoland,       125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iPoland,       125, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iMoscow,       100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iMoscow,       100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iGenoa,        100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iGenoa,        100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iMorocco,      100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iMorocco,      100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iEngland,      100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iEngland,      100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iPortugal,     100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iPortugal,     100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iAragon,       100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iAragon,       100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iPrussia,      100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iPrussia,      100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iLithuania,    100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iLithuania,    100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iAustria,      100, 200, 100, 100, 100, 3 ) # Austria is squashed by other's culture, they need the boost
		gc.setGrowthModifiersHu(iAustria,      100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iTurkey,       100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iTurkey,       100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iSweden,       100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iSweden,       100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iDutch,        100, 200,  50, 100,  50, 4 )
		gc.setGrowthModifiersHu(iDutch,        100, 200,  60, 100,  50, 4 )
		gc.setGrowthModifiersAI(iPope,         150, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iIndependent,  100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iIndependent2, 100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iIndependent3, 100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iIndependent4, 100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iBarbarian,    100, 100, 100,  50, 100, 1 )


		#void setProductionModifiers( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
		# defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100 )
		# 3Miro: at 100 research cost, the cost is exactly as in the XML files, the cost in general is however increased for all civs
		gc.setProductionModifiersAI(iBurgundy,     130, 120, 120, 150 )
		gc.setProductionModifiersHu(iBurgundy,     150, 120, 120, 150 )
		gc.setProductionModifiersAI(iByzantium,    200, 200, 200, 350 )
		gc.setProductionModifiersHu(iByzantium,    200, 150, 200, 350 )
		gc.setProductionModifiersAI(iFrankia,      140, 120, 125, 150 )
		gc.setProductionModifiersHu(iFrankia,      150, 120, 125, 130 )
		gc.setProductionModifiersAI(iArabia,       130, 125, 150, 280 )
		gc.setProductionModifiersHu(iArabia,       150, 125, 150, 230 )
		gc.setProductionModifiersAI(iBulgaria,     130, 125, 125, 250 )
		gc.setProductionModifiersHu(iBulgaria,     150, 150, 125, 200 )
		gc.setProductionModifiersAI(iCordoba,      125, 150, 125, 250 )
		gc.setProductionModifiersHu(iCordoba,      150, 150, 125, 230 )
		gc.setProductionModifiersAI(iSpain,        100, 100, 100, 120 )
		gc.setProductionModifiersHu(iSpain,        125, 100, 100, 120 )
		gc.setProductionModifiersAI(iNorway,       150, 150, 125, 125 )
		gc.setProductionModifiersHu(iNorway,       125, 125, 100, 125 )
		gc.setProductionModifiersAI(iDenmark,      100, 100, 100, 100 )
		gc.setProductionModifiersHu(iDenmark,      100, 100, 100, 100 )
		gc.setProductionModifiersAI(iVenecia,      100, 100, 100, 135 )
		gc.setProductionModifiersHu(iVenecia,      100, 100, 100, 130 )
		gc.setProductionModifiersAI(iNovgorod,     200, 150, 125, 150 )
		gc.setProductionModifiersHu(iNovgorod,     150, 125, 125, 150 )
		gc.setProductionModifiersAI(iKiev,         100, 125, 100, 150 )
		gc.setProductionModifiersHu(iKiev,         125, 150, 125, 150 )
		gc.setProductionModifiersAI(iHungary,      100, 100, 100, 140 )
		gc.setProductionModifiersHu(iHungary,      125, 125, 100, 140 )
		gc.setProductionModifiersAI(iGermany,      100, 100, 100, 130 )
		gc.setProductionModifiersHu(iGermany,      125, 125, 125, 120 )
		gc.setProductionModifiersAI(iScotland,     125, 125, 125, 125 )
		gc.setProductionModifiersHu(iScotland,     125, 125, 125, 125 )
		gc.setProductionModifiersAI(iPoland,       100, 125, 130, 130 )
		gc.setProductionModifiersHu(iPoland,       125, 150, 130, 130 )
		gc.setProductionModifiersAI(iMoscow,        80,  80, 100, 150 )
		gc.setProductionModifiersHu(iMoscow,       100, 100, 100, 150 )
		gc.setProductionModifiersAI(iGenoa,        100, 100, 100, 125 )
		gc.setProductionModifiersHu(iGenoa,        100, 100, 100, 125 )
		gc.setProductionModifiersAI(iMorocco,      125, 125, 125, 175 )
		gc.setProductionModifiersHu(iMorocco,      125, 125, 125, 175 )
		gc.setProductionModifiersAI(iEngland,       80,  80, 100, 110 )
		gc.setProductionModifiersHu(iEngland,      100, 100, 100, 100 )
		gc.setProductionModifiersAI(iPortugal,      70,  90, 100,  90 )
		gc.setProductionModifiersHu(iPortugal,      80,  90, 100,  90 )
		gc.setProductionModifiersAI(iAragon,        80, 100, 100, 125 )
		gc.setProductionModifiersHu(iAragon,        80, 100, 100, 125 )
		gc.setProductionModifiersAI(iPrussia,       60,  80, 120,  90 )
		gc.setProductionModifiersHu(iPrussia,       75,  80, 120, 100 )
		gc.setProductionModifiersAI(iLithuania,     70, 100, 110, 100 )
		gc.setProductionModifiersHu(iLithuania,     80, 100, 110, 100 )
		gc.setProductionModifiersAI(iAustria,       50,  75, 100,  70 )
		gc.setProductionModifiersHu(iAustria,       75,  75, 100,  70 )
		gc.setProductionModifiersAI(iTurkey,        40,  75, 100, 100 )
		gc.setProductionModifiersHu(iTurkey,        75,  75, 100, 100 )
		gc.setProductionModifiersAI(iSweden,        80,  80, 100, 100 )
		gc.setProductionModifiersHu(iSweden,        80,  80, 100, 100 )
		gc.setProductionModifiersAI(iDutch,         80,  50,  50,  40 )
		gc.setProductionModifiersHu(iDutch,         90,  50,  60,  40 )
		gc.setProductionModifiersAI(iPope,         300, 200, 100, 350 )
		gc.setProductionModifiersAI(iIndependent,  170, 100, 400, 200 ) #The peaceful ones
		gc.setProductionModifiersAI(iIndependent2, 170, 100, 400, 200 )
		gc.setProductionModifiersAI(iIndependent3, 125, 100, 600, 300 ) #The warlike ones
		gc.setProductionModifiersAI(iIndependent4, 125, 100, 600, 300 )
		gc.setProductionModifiersAI(iBarbarian,    125, 100, 1000, 350 )

		#void setSupportModifiers( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
		# defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100 )
		gc.setSupportModifiersAI(iBurgundy,      10, 150,  60,  40, 100 )
		gc.setSupportModifiersHu(iBurgundy,      10, 150,  60,  40, 100 )
		gc.setSupportModifiersAI(iByzantium,     60, 150,  100,  75, 120 )
		gc.setSupportModifiersHu(iByzantium,     60, 150,  80,  50, 120 )
		gc.setSupportModifiersAI(iFrankia,       30, 120,  80,  35, 100 )
		gc.setSupportModifiersHu(iFrankia,       30, 120,  80,  35, 100 )
		gc.setSupportModifiersAI(iArabia,        30, 150,  70,  15, 120 )
		gc.setSupportModifiersHu(iArabia,        30, 150,  70,  15, 120 )
		gc.setSupportModifiersAI(iBulgaria,      40, 150,  80,  50, 120 )
		gc.setSupportModifiersHu(iBulgaria,      40, 150,  70,  40, 120 )
		gc.setSupportModifiersAI(iCordoba,       50, 150,  70,  50, 120 )
		gc.setSupportModifiersHu(iCordoba,       50, 150,  70,  50, 120 )
		gc.setSupportModifiersAI(iSpain,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iSpain,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iNorway,        10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iNorway,        10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iDenmark,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iDenmark,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iVenecia,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iVenecia,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iNovgorod,      10, 150,  50,  25, 100 )
		gc.setSupportModifiersHu(iNovgorod,      10, 150,  50,  25, 100 )
		gc.setSupportModifiersAI(iKiev,          10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iKiev,          10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iHungary,       20, 100,  60,  25, 100 )
		gc.setSupportModifiersHu(iHungary,       20, 100,  60,  25, 100 )
		gc.setSupportModifiersAI(iGermany,       10, 100,  60,  25, 100 )
		gc.setSupportModifiersHu(iGermany,       10, 100,  60,  25, 100 )
		gc.setSupportModifiersAI(iScotland,      10, 100,  75,  40, 100 )
		gc.setSupportModifiersHu(iScotland,      10, 100,  75,  40, 100 )
		gc.setSupportModifiersAI(iPoland,        10, 100,  70,  25, 100 )
		gc.setSupportModifiersHu(iPoland,        10, 100,  70,  25, 100 )
		gc.setSupportModifiersAI(iMoscow,        10, 100,  50,  25, 100 ) # sync with UP
		gc.setSupportModifiersHu(iMoscow,        10, 100,  50,  25, 100 ) # sync with UP
		gc.setSupportModifiersAI(iGenoa,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iGenoa,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iMorocco,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iMorocco,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iEngland,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iEngland,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iPortugal,      10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iPortugal,      10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iAragon,        10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iAragon,        10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iPrussia,       10,  85,  50,  40, 100 )
		gc.setSupportModifiersHu(iPrussia,       10,  85,  50,  40, 100 )
		gc.setSupportModifiersAI(iLithuania,     10,  85,  50,  25, 100 )
		gc.setSupportModifiersHu(iLithuania,     10,  85,  50,  25, 100 )
		gc.setSupportModifiersAI(iAustria,       10,  65,  50,  25,  80 )
		gc.setSupportModifiersHu(iAustria,       10,  65,  50,  25,  80 )
		gc.setSupportModifiersAI(iTurkey,        30,  50,  50,  20, 100 )
		gc.setSupportModifiersHu(iTurkey,        30,  50,  50,  20, 100 )
		gc.setSupportModifiersAI(iSweden,        10,  75,  50,  25, 100 )
		gc.setSupportModifiersHu(iSweden,        10,  75,  50,  25, 100 )
		gc.setSupportModifiersAI(iDutch,         10,  50,  50,  50, 100 )
		gc.setSupportModifiersHu(iDutch,         10,  50,  50,  50, 100 )
		gc.setSupportModifiersAI(iPope,          10, 200,  50,  25, 100 )
		gc.setSupportModifiersAI(iIndependent,   10, 100,  10,  20, 100 )
		gc.setSupportModifiersAI(iIndependent2,  10, 100,  10,  20, 100 )
		gc.setSupportModifiersAI(iIndependent3,  10, 100,  10,  20, 100 )
		gc.setSupportModifiersAI(iIndependent4,  10, 100,  10,  20, 100 )
		gc.setSupportModifiersAI(iBarbarian,     10, 250,  10, 100, 100 )


		#3Miro: setGrowthTreshold(iCiv,iVal), for each civ, a value in percent. How much food is needed for the next growth level.
		# in c++, iTreshold *= value, iTreshlod /= 100 (value is in percent, with integer truncation, default 100)
		# low percent means faster growth

		#3Miro: setProductionModifiersUnits(iCiv,iVal) for each civ. Same as growth.
		# on all production, low percent means fast production

		#3Miro: setProductionModifiersBuildings(iCiv,iVal) for each civ. Same as growth.

		#3Miro: setProductionModifiersWonders(iCiv,iVal) for each civ. Same as growth.

		#3Miro: setInflationModifier(iCiv,iVal) for each civ. Same as growth.
		# low percent means low inflation

		#3Miro: setGPModifier(iCiv,iVal) for each civ. The rate at which GP would appear. Same as growth.
		# low percent means faster GP rate

		#3Miro: setUnitSupportModifier(iCiv, iVal), set unit support modifiers for the player. Same as growth.
		# low percent means lower support cost)

		#3Miro: setDistanceSupportModifier(iCiv,iVal), set modifiers for the distance to the capital support. Same as growth.
		# low percent means low cost

		#3Miro: setNumberOfCitiesSupport(iCiv,iVal), set number of cities modifier. Same as growth
		# low percent means low cost

		#3Miro: setCivicSupportModifier(iCiv,iVal), set the civic support modifiers. Same as growth.
		# low percent means low cost

		#3Miro: setResearchModifier(iCiv, iVal), set research modifier for all the civs. Same as growth.
		# low percent means faster research

		#3Miro: setHealthModifier(iCiv,iVal), multiply the health modifier for the difficulty level by iVal

		#3Miro: setWorkerModifier(iCiv,iVal), modify the rate at witch workers build improvements. Not the same as growth.
		# higher number, faster workers

		# 3Miro: setCultureModifier(iCiv, iVal ), modify culture if the city makes more than 4 (especially low for Indeps and Barbs)
		# Same as growth. higher number more culture

		##### Set Initial buildings for the civs
		#gc.setInitialBuilding( iCiv, iBuilding, True\False ), if ( True) give iCiv, building iBuildings else don't Default is False
		# we can change True <-> False with the onTechAquire event

		gc.setInitialBuilding( iVenecia, iHarbor, True )
		gc.setInitialBuilding( iVenecia, iGranary, True )

		gc.setInitialBuilding( iSpain, iBarracks, True )

		gc.setInitialBuilding( iDenmark, iBarracks, True )

		gc.setInitialBuilding( iScotland, iBarracks, True )

		gc.setInitialBuilding( iMoscow, iGranary, True )
		gc.setInitialBuilding( iMoscow, iBarracks, True )
		gc.setInitialBuilding( iMoscow, iForge, True )
		gc.setInitialBuilding( iMoscow, iMarket, True )

		gc.setInitialBuilding( iGenoa, iGranary, True )
		gc.setInitialBuilding( iGenoa, iBarracks, True )
		gc.setInitialBuilding( iGenoa, iHarbor, True )

		gc.setInitialBuilding( iMorocco, iGranary, True )
		gc.setInitialBuilding( iMorocco, iBarracks, True )

		gc.setInitialBuilding( iEngland, iGranary, True )
		gc.setInitialBuilding( iEngland, iBarracks, True )

		gc.setInitialBuilding( iPortugal, iGranary, True )
		gc.setInitialBuilding( iPortugal, iBarracks, True )

		gc.setInitialBuilding( iAragon, iGranary, True )
		gc.setInitialBuilding( iAragon, iBarracks, True )

		gc.setInitialBuilding( iPrussia, iGranary, True )
		gc.setInitialBuilding( iPrussia, iBarracks, True )

		gc.setInitialBuilding( iLithuania, iGranary, True )
		gc.setInitialBuilding( iLithuania, iBarracks, True )

		gc.setInitialBuilding( iAustria, iGranary, True )
		gc.setInitialBuilding( iAustria, iBarracks, True )
		gc.setInitialBuilding( iAustria, iForge, True )

		gc.setInitialBuilding( iTurkey, iGranary, True )
		gc.setInitialBuilding( iTurkey, iBarracks, True )
		gc.setInitialBuilding( iTurkey, iForge, True )
		gc.setInitialBuilding( iTurkey, iHarbor, True )

		gc.setInitialBuilding( iSweden, iGranary, True )
		gc.setInitialBuilding( iSweden, iBarracks, True )
		gc.setInitialBuilding( iSweden, iHarbor, True )

		gc.setInitialBuilding( iDutch, iGranary, True )
		gc.setInitialBuilding( iDutch, iBarracks, True )
		gc.setInitialBuilding( iDutch, iForge, True )
		gc.setInitialBuilding( iDutch, iHarbor, True )
		gc.setInitialBuilding( iDutch, iAqueduct, True )
		gc.setInitialBuilding( iDutch, iMarket, True )
		gc.setInitialBuilding( iDutch, iLighthouse, True )
		gc.setInitialBuilding( iDutch, iTheatre, True )
		gc.setInitialBuilding( iDutch, iSmokehouse, True )

		####### AI Modifiers
		#3Miro: setCityClusterAI(iCiv,iTop,iBottom,iMinus) for each AI civilization (set them for all, but only the AI make difference)
		# this determines how clustered the cities would be
		# AI_foundValue in PlayerAI would compute for a candidate city location the number of plots that are taken (i.e. by another city)
		# in CivIV, if more than a third of the tiles are "taken", do not found city there. In RFC, cities are clustered closer
		# if ( iTaken > 21 * iTop / iBottom - iMinus ) do not build city there.
		# RFC default values are 2/3 -1 for Europe, 1/3 - 0 for Russia and 1/2 for Mongolia
		# for example gc.setCityClusterAI( iByzantium, 1, 3, 1 ) would force Byzantium to spread out
		gc.setCityClusterAI( iBurgundy, 2, 3, 3 ) #12
		gc.setCityClusterAI( iByzantium, 1, 3, 1 ) #7
		gc.setCityClusterAI( iFrankia, 1, 3, 1 ) #7
		gc.setCityClusterAI( iArabia, 1, 3, 1 ) #7
		gc.setCityClusterAI( iBulgaria, 1, 2, 1 ) #10
		gc.setCityClusterAI( iCordoba, 1, 2, 2 ) #9
		gc.setCityClusterAI( iSpain, 1, 2, 2 ) #9
		gc.setCityClusterAI( iNorway, 1, 2, 2 ) #9
		gc.setCityClusterAI( iDenmark, 2, 3, 3 ) #12
		gc.setCityClusterAI( iVenecia, 2, 3, 1 ) #14
		gc.setCityClusterAI( iNovgorod, 1, 4, 1 ) #5
		gc.setCityClusterAI( iKiev, 1, 4, 1 ) #5
		gc.setCityClusterAI( iHungary, 1, 2, 1 ) #10
		gc.setCityClusterAI( iGermany, 2, 3, 3 ) #12
		gc.setCityClusterAI( iScotland, 2, 3, 3 ) #12
		gc.setCityClusterAI( iPoland, 1, 3, 1 ) #7
		gc.setCityClusterAI( iMoscow, 1, 4, 1 ) #5
		gc.setCityClusterAI( iPortugal, 2, 3, 1 ) #14
		gc.setCityClusterAI( iAragon, 2, 3, 1 ) #14
		gc.setCityClusterAI( iPrussia, 2, 3, 1 ) #14
		gc.setCityClusterAI( iLithuania, 1, 3, 1 ) #7
		gc.setCityClusterAI( iGenoa, 2, 3, 1 ) #14
		gc.setCityClusterAI( iMorocco, 1, 3, 1 ) #7
		gc.setCityClusterAI( iEngland, 1, 2, 2 ) #9
		gc.setCityClusterAI( iAustria, 2, 3, 3 ) #12
		gc.setCityClusterAI( iTurkey, 1, 3, 1 ) #7
		gc.setCityClusterAI( iSweden, 1, 2, 2 ) #9
		gc.setCityClusterAI( iDutch, 2, 3, 1 ) #14

		#3Miro: setCityWarDistanceAI(iCiv,iVal), depending on the type of the empire, modify how likely the AI is to attack a city
		# values are 1 - small empires, 2 - large continuous empires, 3 - not necessarily continuous empires
		gc.setCityWarDistanceAI( iBurgundy, 1 )
		gc.setCityWarDistanceAI( iByzantium, 2 )
		gc.setCityWarDistanceAI( iFrankia, 2 )
		gc.setCityWarDistanceAI( iArabia, 2 )
		gc.setCityWarDistanceAI( iBulgaria, 2 )
		gc.setCityWarDistanceAI( iCordoba, 1 )
		gc.setCityWarDistanceAI( iSpain, 3 )
		gc.setCityWarDistanceAI( iAragon, 3 )
		gc.setCityWarDistanceAI( iNorway, 3 )
		gc.setCityWarDistanceAI( iDenmark, 2 )
		gc.setCityWarDistanceAI( iVenecia, 3 )
		gc.setCityWarDistanceAI( iNovgorod, 2 )
		gc.setCityWarDistanceAI( iKiev, 2 )
		gc.setCityWarDistanceAI( iHungary, 2 )
		gc.setCityWarDistanceAI( iGermany, 2 )
		gc.setCityWarDistanceAI( iScotland, 1 )
		gc.setCityWarDistanceAI( iPoland, 2 )
		gc.setCityWarDistanceAI( iMoscow, 2 )
		gc.setCityWarDistanceAI( iPortugal, 2 )
		gc.setCityWarDistanceAI( iPrussia, 2 )
		gc.setCityWarDistanceAI( iLithuania, 2 )
		gc.setCityWarDistanceAI( iGenoa, 3 )
		gc.setCityWarDistanceAI( iMorocco, 2 )
		gc.setCityWarDistanceAI( iEngland, 3 )
		gc.setCityWarDistanceAI( iAustria, 2 )
		gc.setCityWarDistanceAI( iTurkey, 2 )
		gc.setCityWarDistanceAI( iSweden, 2 )
		gc.setCityWarDistanceAI( iDutch, 1 )

		#3Miro: setTechPreferenceAI(iCiv,iTech,iVal), for each civ, for each tech, specify how likable it is. iVal is same as in growth.
		# low percent makes the tech less desirable
		#gc.setTechPreferenceAI(iByzantium,1,200)
		#gc.setTechPreferenceAI(iFrankia,1,200)
		gc.setTechPreferenceAI(iBulgaria,iBronzeCasting,200)
		gc.setTechPreferenceAI(iGermany,iPrintingPress,200)
		gc.setTechPreferenceAI(iEngland,iPrintingPress,150)
		gc.setTechPreferenceAI(iPope,iPrintingPress,10) # Pope shouldn't want this
		gc.setTechPreferenceAI(iSpain,iAstronomy,200)
		gc.setTechPreferenceAI(iPortugal,iAstronomy,200)

		#3Miro: setDiplomacyModifiers(iCiv1,iCiv2,iVal) hidden modifier for the two civ's AI relations. More likely to have OB and so on.
		# + means they will like each other - they will hate each other.
		# from Civ1 towards Civ2 (make them symmetric)
		gc.setDiplomacyModifiers( iCordoba, iArabia, +5 )
		gc.setDiplomacyModifiers( iArabia, iCordoba, +5 )
		gc.setDiplomacyModifiers( iArabia, iByzantium, -8 )
		gc.setDiplomacyModifiers( iByzantium, iArabia, -8 )
		gc.setDiplomacyModifiers( iBulgaria, iByzantium, +3 )
		gc.setDiplomacyModifiers( iByzantium, iBulgaria, +3 )
		gc.setDiplomacyModifiers( iCordoba, iSpain, -14 )
		gc.setDiplomacyModifiers( iSpain, iCordoba, -14 )
		gc.setDiplomacyModifiers( iMorocco, iSpain, -10 )
		gc.setDiplomacyModifiers( iSpain, iMorocco, -10 )
		gc.setDiplomacyModifiers( iAragon, iSpain, +4 )
		gc.setDiplomacyModifiers( iSpain, iAragon, +4 )
		gc.setDiplomacyModifiers( iPortugal, iSpain, +6 )
		gc.setDiplomacyModifiers( iSpain, iPortugal, +6 )
		gc.setDiplomacyModifiers( iCordoba, iPortugal, -8 )
		gc.setDiplomacyModifiers( iPortugal, iCordoba, -8 )
		gc.setDiplomacyModifiers( iKiev, iNovgorod, +5 )
		gc.setDiplomacyModifiers( iNovgorod, iKiev, +5 )
		gc.setDiplomacyModifiers( iMoscow, iNovgorod, -8 )
		gc.setDiplomacyModifiers( iNovgorod, iMoscow, -8 )
		gc.setDiplomacyModifiers( iFrankia, iBurgundy, -2 )
		gc.setDiplomacyModifiers( iBurgundy, iFrankia, -2 )
		gc.setDiplomacyModifiers( iTurkey, iByzantium, -14 )
		gc.setDiplomacyModifiers( iByzantium, iTurkey, -14 )
		gc.setDiplomacyModifiers( iGermany, iPoland, -5 )
		gc.setDiplomacyModifiers( iPoland, iGermany, -5 )
		gc.setDiplomacyModifiers( iMoscow, iPoland, -4 )
		gc.setDiplomacyModifiers( iPoland, iMoscow, -4 )
		gc.setDiplomacyModifiers( iMoscow, iLithuania, -2 )
		gc.setDiplomacyModifiers( iLithuania, iMoscow, -2 )
		gc.setDiplomacyModifiers( iAustria, iPoland, -2 )
		gc.setDiplomacyModifiers( iPoland, iAustria, -2 )
		gc.setDiplomacyModifiers( iLithuania, iPoland, +4 )
		gc.setDiplomacyModifiers( iPoland, iLithuania, +4 )
		gc.setDiplomacyModifiers( iHungary, iPoland, +3 )
		gc.setDiplomacyModifiers( iPoland, iHungary, +3 )
		gc.setDiplomacyModifiers( iAustria, iHungary, -6)
		gc.setDiplomacyModifiers( iHungary, iAustria, -6)
		gc.setDiplomacyModifiers( iSweden, iPoland, -2 )
		gc.setDiplomacyModifiers( iPoland, iSweden, -2 )
		gc.setDiplomacyModifiers( iSweden, iMoscow, -8 )
		gc.setDiplomacyModifiers( iMoscow, iSweden, -8 )
		gc.setDiplomacyModifiers( iPrussia, iPoland, -6 )
		gc.setDiplomacyModifiers( iPoland, iPrussia, -6 )
		gc.setDiplomacyModifiers( iPrussia, iLithuania, -8 )
		gc.setDiplomacyModifiers( iLithuania, iPrussia, -8 )
		gc.setDiplomacyModifiers( iEngland, iScotland, -8 )
		gc.setDiplomacyModifiers( iScotland, iEngland, -8 )
		gc.setDiplomacyModifiers( iFrankia, iScotland, +4 )
		gc.setDiplomacyModifiers( iScotland, iFrankia, +4 )
		gc.setDiplomacyModifiers( iNorway, iDenmark, +4 )
		gc.setDiplomacyModifiers( iDenmark, iNorway, +4 )
		gc.setDiplomacyModifiers( iSweden, iDenmark, -4 )
		gc.setDiplomacyModifiers( iDenmark, iSweden, -4 )


		####### 3Miro: UNIQUE POWERS
		#3Miro: setUP(iCiv,iPower) sets the Unique Powers for C++

		#3Miro: setUP(iCiv,iPower,iParameter)
		# iUP_Happiness, iParameter = the amount of additional happiness
		# iUP_PerCityCommerce, iParameter = 1000000 * bonus_in_gold + 10000*bonus_in_research + 100*bonus_in_culture + bonus_in_espionage (bonuses are limited to 0 - 99)
		# iUP_CommercePercent, iParameter = 1000000 * bonus_in_gold + 10000*bonus_in_research + 100*bonus_in_culture + bonus_in_espionage (bonuses are limited to 0 - 99 percent)
		# iUP_CulturalTolerance. iParameter = 0 for no unhappiness or unhappiness = unhappiness / iParameter
		# iUP_ReligiousTolerance. iParameter = 0 for no instability
		# iUP_Conscription, iParameter = percent of foreign culture needed to draft + 100 * max number of units to draft per turn
		# iUP_NoResistance, iParameter = 0 for no resistance or resistance turns = resistance turns / iParameter
		# iUP_UnitProduction, iParameter = iRequiredTech * 100 + Percent ( 75% for 25% faster unit building)
		# iUP_EnableCivic, iParameter = Civic5 * 100000000 + Civic4 * 1000000 + Civic3 * 10000 + Civic2 * 100 + Civic1, NOTE: also need to enable this in the WB, civic indexed by 0 is always available, civic5 cannot be bigger than 20
		# iUP_TradeRoutes, iParameter = number of extra trade routes, NOTE: this must be synchronized with GlobalDefines.xml: max trade routes
		# iUP_PromotionI, iParameter = the bonus promotion
		# iUP_PromotionII, iParameter = the bonus promotion
		# iUP_Inquisition, iParameter is not used
		# iUP_CanEnterTerrain, iParameter is the terrain to enter
		# iUP_Discoveru, iParameter = ColonyStart * 1000000 + ColonyEnd * 1000 + iModifier modifies the cost associated with all projects (iCost *= iModifier; iCost /= 100 )
		# iUP_EndlessLand, iParameter = percent change (i.e. upkeep *= iParameter, upkeep /= 100 )
		# iUP_ForeignSea, use iParameter = 1
		# iUP_Pious, whenever changeFaith( x ) is called, x is multiplied by iParameter
		# iUP_HealthFood, use iParameter = 1 to activate
		# iUP_TerrainBonus, iParameter = iActivate * 100000 (1 to be active) + iTerrain * 1000 + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus (bonuses are limited to 0-9)
		# iUP_FeatureBonus, iParameter = iActivate * 100000 (1 to be active) + iFeature * 1000 + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus (bonuses are limited to 0-9)
		# iUP_ImprovementBonus, iParameter = iActivate * 100000 (1 to be active) + iImprovement * 1000 + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus (bonuses are limited to 0-9)
		# iUP_CityTileYield, iParameter = iActivate * 1000 (1 to be active) + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus, (bonuses are limited to 0-9)

		gc.setUP( iBurgundy, iUP_Happiness, 1 )
		gc.setUP( iBurgundy, iUP_PerCityCommerce, 200)

		gc.setUP( iByzantium, iUP_Emperor, 1 )

		gc.setUP( iFrankia, iUP_LandStability, 1 )

		gc.setUP( iArabia, iUP_Faith, 1 )

		gc.setUP( iBulgaria, iUP_NoResistance, 0 )

		gc.setUP( iCordoba, iUP_PromotionI, iPromotionMedic1 )
		gc.setUP( iCordoba, iUP_HealthFood, 1 )

		gc.setUP( iMorocco, iUP_TerrainBonus, 1 * 100000 + iTerrainDesert * 1000 + 10 + 1 )
		gc.setUP( iMorocco, iUP_FeatureBonus, 1 * 100000 + iOasis * 1000 + 100 + 1 )

		gc.setUP( iSpain, iUP_Inquisition, 1 )
		gc.setUP( iSpain, iUP_PerCityCommerce, 2 )

		gc.setUP( iNorway, iUP_CanEnterTerrain, iTerrainOcean )
		gc.setUP( iNorway, iUP_StabilitySettler, 1 )

		gc.setUP( iVenecia, iUP_EnableCivic, iCivicMerchantRepublic )
		#gc.setUP( iVenecia, iUP_ForeignSea, 1 )

		gc.setUP( iKiev, iUP_CityTileYield, 100 * 2 )

		gc.setUP( iHungary, iUP_Happiness, 1 )
		gc.setUP( iHungary, iUP_CulturalTolerance, 0 )

		gc.setUP( iGermany, iUP_UnitProduction, iGunpowder * 100 + 75 )

		gc.setUP( iPoland, iUP_ReligiousTolerance, 0 )

		gc.setUP( iLithuania, iUP_PaganCulture, 200 )
		gc.setUP( iLithuania, iUP_PaganHappy, 1 )

		gc.setSupportModifiersAI(iMoscow, 10, 100, 25, 12, 100 )
		gc.setSupportModifiersHu(iMoscow, 10, 100, 25, 12, 100 )
		gc.setUP( iMoscow, iUP_EndlessLand, 50 )

		gc.setUP( iGenoa, iUP_Mercenaries, 1 ) # this actually has no effect, it is implemented in Mercenaries.py entirely

		gc.setUP( iEngland, iUP_ImprovementBonus, 1 * 100000 + iImprovementWorkshop * 1000 + 10 + 1 )

		# Speedup East/West India Trading Companies
		gc.setUP( iPortugal, iUP_Discovery, (iNumNotColonies-2) * 1000000 + (iNumTotalColonies-1) * 1000 + 40 );
		gc.setUP( iPortugal, iUP_StabilitySettler, 1 )

		for i in range( iNumTotalPlayers ):
			if ( not i == iAustria ):
				gc.setDiplomacyModifiers( i, iAustria, +4 )
		gc.setUP( iAustria, iUP_PerCityCommerce, 200)

		#gc.setUP( iTurkey, iUP_Conscription, 330 )
		#gc.setUP( iTurkey, iUP_Conscription, 1 )
		gc.setUP( iTurkey, iUP_Janissary, 1 )

		gc.setUP( iSweden, iUP_PromotionI, iPromotionFormation )

		gc.setUP( iNovgorod, iUP_EnableCivic, iCivicBureaucracy )

		gc.setUP( iPrussia, iUP_EnableCivic, iCivicTheocracy )
		# Absinthe: handled in python currently
		#gc.setUP( iPrussia, iUP_NoAnarchyInstability, 1 )

		# Absinthe: handled in python currently
		#gc.setUP( iAragon, iUP_ProvinceCommerce, 0 )

		# Absinthe: handled in python currently
		#gc.setUP( iScotland, iUP_Defiance, 1 )

		gc.setUP( iDutch, iUP_TradeRoutes, 2 )
		gc.setUP( iDutch, iUP_Pious, 2 ) # 3Miro: "hidden" buff to the Dutch FP, otherwise they have too little piety (not enough cities)
		gc.setUP( iDutch, iUP_Discovery, (iNumNotColonies-2) * 1000000 + (iNumTotalColonies-1) * 1000 + 30 );

		gc.setUP( iPope, iUP_Emperor, 1 )

		# GlobalWarming
		gc.setGlobalWarming( False )

		# Set FastTerrain (i.e. double movement over ocean)
		gc.setFastTerrain( iTerrainOcean )

		# set religious spread factors
		for iCiv in range( iNumTotalPlayers + 1 ): # include barbs
			for iRel in range( iNumReligions ):
				gc.setReligionSpread( iCiv, iRel, tReligionSpreadFactor[iCiv][iRel] )

		# set the religions and year of the great schism
		gc.setSchism( iCatholicism, iOrthodoxy, i1053AD )

		gc.setHoliestCity( tJerusalem[0], tJerusalem[1] )

		# 3Miro: Faith Points benefits
		#gc.setReligionBenefit( iReligion, iFP_(whatever it is), iParameter, iCap )
		#	note that for powers iParameter = -1 means that this religion doesn't have this power (-1 is the default)
		#	iCap sets a cap for the maximum number of FP a religion can have (per player) Can be adjusted per Player
		#
		#iFP_Stability: stability += iParameter * num_FaithPoints / 100
		#		 i.e. 1 Faith Point = iParameter percent of a stability point
		#iFP_Civic: civic_upkeep *= 100 - (num_FaithPoints * iParameter) / 100
		#		civic_upkeep /= 100
		#		iParameter = 200, means 2% lower cost per Faith Point, iParameter = 50 means .5% lower cost per FP
		#iFP_Growth: iTreshhold *= 100 - (num_FaithPoints * iParameter) / 100
		#		iTreshhold /= 100
		#		iParameter = 200, means 2% faster growth per Faith Point, iParameter = 50 means .5% faster growth per FP
		#iFP_Units: iProductionNeeded *= 100 - (num_FaithPoints * iParameter) / 100
		#		iProductionNeeded /= 100
		#		iParameter = 200, means 2% faster production per Faith Point, iParameter = 50 means .5% faster production per FP
		#iFP_Science: same as units, iParameter = 200, means 2% lower tech cost per Faith Point, iParameter = 50 means .5% lower tech cost per FP
		#iFP_Production: iProductionNeeded *= 100 - (num_FaithPoints * iParameter) / 100
		#		iProductionNeeded /= 100
		#		iParameter = 200, means 2% faster production per Faith Point, iParameter = 50 means .5% faster production per FP
		#		Counts for Wonders and Projects
		#iFP_Displomacy: iAttitude += iParameter * num_FaithPoints / 100
		#		i.e. 1 Faith Point = iParameter percent of an attitude point

		gc.setReligionBenefit( iOrthodoxy, iFP_Stability, 10, 100 )
		gc.setReligionBenefit( iOrthodoxy, iFP_Civic, 50, 100 )

		gc.setReligionBenefit( iIslam, iFP_Growth, 50, 100 )
		gc.setReligionBenefit( iIslam, iFP_Units, 50, 100 )

		gc.setReligionBenefit( iProtestantism, iFP_Science, 30, 100 )
		gc.setReligionBenefit( iProtestantism, iFP_Production, 30, 100 )

		gc.setReligionBenefit( iCatholicism, iFP_Displomacy, 7, 100 )
		gc.setReligionBenefit( iIslam, iFP_Displomacy, 6, 100 )
		gc.setReligionBenefit( iProtestantism, iFP_Displomacy, 5, 100 )
		gc.setReligionBenefit( iOrthodoxy, iFP_Displomacy, 3, 100 )

		# every nation gets a land tile that is normally impassible and now pass through it
		#gc.setStrategicTile( iVenecia, 56, 35 )

		# set AI modifiers for preferred buildings
		# use values -10 for very unlikely, 0 for default neutral and positive for desirable
		# values less than -10 might not work, above 10 should be fine

		gc.setBuildingPref( iBurgundy, iMonasteryOfCluny, 20 )

		gc.setBuildingPref( iByzantium, iRoundChurch, -3 )
		gc.setBuildingPref( iByzantium, iGoldenBull, -3 )

		gc.setBuildingPref( iFrankia, iNotreDame, 20 )
		gc.setBuildingPref( iFrankia, iVersailles, 10 )
		gc.setBuildingPref( iFrankia, iFontainebleau, 10 )

		gc.setBuildingPref( iArabia, iDomeRock, 10 )
		gc.setBuildingPref( iArabia, iTombKhal, 20 )
		gc.setBuildingPref( iArabia, iNotreDame, -5 )
		gc.setBuildingPref( iArabia, iStephansdom, -5 )
		gc.setBuildingPref( iArabia, iSistineChapel, -5 )
		gc.setBuildingPref( iArabia, iKrakDesChevaliers, -5 )
		gc.setBuildingPref( iArabia, iLeaningTower, -3 )
		gc.setBuildingPref( iArabia, iGoldenBull, -3 )
		gc.setBuildingPref( iArabia, iCopernicus, -3 )

		gc.setBuildingPref( iBulgaria, iRoundChurch, 20 )

		gc.setBuildingPref( iCordoba, iGardensAlAndalus, 20 )
		gc.setBuildingPref( iCordoba, iLaMezquita, 20 )
		gc.setBuildingPref( iCordoba, iAlhambra, 20 )
		gc.setBuildingPref( iCordoba, iDomeRock, 10 )
		gc.setBuildingPref( iCordoba, iNotreDame, -5 )
		gc.setBuildingPref( iCordoba, iStephansdom, -5 )
		gc.setBuildingPref( iCordoba, iSistineChapel, -5 )
		gc.setBuildingPref( iCordoba, iKrakDesChevaliers, -5 )
		gc.setBuildingPref( iCordoba, iLeaningTower, -3 )
		gc.setBuildingPref( iCordoba, iGoldenBull, -3 )

		gc.setBuildingPref( iSpain, iEscorial, 20 )
		gc.setBuildingPref( iSpain, iMagellansVoyage, 10 )

		gc.setBuildingPref( iNorway, iShrineOfUppsala, 20 )

		gc.setBuildingPref( iDenmark, iKalmarCastle, 10 )

		gc.setBuildingPref( iVenecia, iMarcoPolo, 15 )
		gc.setBuildingPref( iVenecia, iSanMarco, 15 )
		gc.setBuildingPref( iVenecia, iLanterna, 10 )
		gc.setBuildingPref( iVenecia, iLeonardosWorkshop, 5 )
		gc.setBuildingPref( iVenecia, iLeaningTower, 5 )

		gc.setBuildingPref( iKiev, iSophiaKiev, 20 )

		gc.setBuildingPref( iHungary, iPressburg, 20 )
		gc.setBuildingPref( iHungary, iGoldenBull, 20 )
		gc.setBuildingPref( iHungary, iBibliothecaCorviniana, 15 )
		gc.setBuildingPref( iHungary, iKazimierz, 10 )

		gc.setBuildingPref( iPrussia, iBrandenburgGate, 20 )

		gc.setBuildingPref( iGermany, iBrandenburgGate, 10 )
		gc.setBuildingPref( iGermany, iImperialDiet, 20 )
		gc.setBuildingPref( iGermany, iCopernicus, 5 )

		gc.setBuildingPref( iPoland, iPressburg, 10 )
		gc.setBuildingPref( iPoland, iCopernicus, 10 )
		gc.setBuildingPref( iPoland, iGoldenBull, 5 )
		gc.setBuildingPref( iPoland, iKazimierz, 15 )

		gc.setBuildingPref( iMoscow, iStBasil, 20 )

		gc.setBuildingPref( iGenoa, iSanGiorgio, 20 )
		gc.setBuildingPref( iGenoa, iLanterna, 20 )
		gc.setBuildingPref( iGenoa, iLeonardosWorkshop, 5 )
		gc.setBuildingPref( iGenoa, iLeaningTower, 5 )

		gc.setBuildingPref( iEngland, iMagnaCarta, 20 )
		gc.setBuildingPref( iEngland, iWestminster, 10 )

		gc.setBuildingPref( iPortugal, iBelemTower, 20 )
		gc.setBuildingPref( iPortugal, iPalacioDaPena, 20 )

		gc.setBuildingPref( iAustria, iStephansdom, 20 )
		gc.setBuildingPref( iAustria, iAustrianOperaHouse, 10 )

		gc.setBuildingPref( iTurkey, iTopkapiPalace, 20 )

		gc.setBuildingPref( iSweden, iKalmarCastle, 20 )

		gc.setBuildingPref( iDutch, iBeurs, 20 )

		gc.setBuildingPref( iPope, iSistineChapel, 20 )

		# 3Miro: set the Jews as the minor Religion
		gc.setMinorReligion( iJudaism )
		gc.setMinorReligionRefugies( 0 )

		# Manor House + Manorism: iBuilding + 1000 * iCivic + 100,000 * iGold + 1,000,000 * iResearch + 10,000,000 * iCulture + 100,000,000 * iEspionage
			# 3Miro: moved to XML, no need to put it here
		#gc.setBuildingCivicCommerseCombo1( iManorHouse + 1000 * iManorialism + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
		#gc.setBuildingCivicCommerseCombo2( iFrenchChateau + 1000 * iManorialism + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
		#gc.setBuildingCivicCommerseCombo3(-1)

		# 3Miro: Psycho AI cheat, this will make Ottoman AI think it can win battles vs Constantinople at 90/100 rate
		#	it will also actually boost the Ottoman's odds (actually lower the defenders chance by 20 percent), but only when attacking Constantinople
		gc.setPsychoAICheat( iTurkey, tCapitals[iByzantium][0], tCapitals[iByzantium][1] ) # Constantinople (81, 24)

		# 3Miro: be very careful here, this can really mess the AI
		#	setHistoricalEnemyAICheat( iAttacker, iDefender, 10 ) gives the attacker +10% bonus, when attacked units belong to the defender
		#	this modifier only works in AI vs AI battles, it's ignored if either player is Human
		#	none of the AI players is "aware" of the modification, if you make it too big, it could lead to a couple strange situations
		#	(where the AI has clear advantage in a battle, yet it still won't attack)
		#	so this should be a "last resort" solution, other methods are always preferable
		gc.setHistoricalEnemyAICheat( iTurkey, iBulgaria,  10 )
		gc.setHistoricalEnemyAICheat( iBulgaria, iTurkey, -10 )

		gc.setHistoricalEnemyAICheat( iSpain, iCordoba,  10 )
		gc.setHistoricalEnemyAICheat( iCordoba, iSpain, -10 )

		gc.setHistoricalEnemyAICheat( iPortugal, iSpain,  10 )
		gc.setHistoricalEnemyAICheat( iSpain, iPortugal, -10 )

		gc.setHistoricalEnemyAICheat( iAustria, iHungary,  10 )
		gc.setHistoricalEnemyAICheat( iHungary, iAustria, -10 )

		gc.setHistoricalEnemyAICheat( iAustria, iGermany,  10 )
		gc.setHistoricalEnemyAICheat( iGermany, iAustria, -10 )

		# 3Miro: this sets rules on how players can Vassalize, first two parameters are the players (we should probably keep this symmetric)
		#	if the third parameter is -1: cannot Vassalize, 0: has to satisfy a condition (default), 1 can Vassalize without conditions
		#	the condition is that either one of the players needs to have a city in a province that the other players considers >= the last parameter
		#	the default for the last parameter is 0, we should call this at least once to set the parameter (it is the same for all players)
		gc.setVassalagaeCondition( iCordoba, iArabia, 1, iProvinceOuter )
		gc.setVassalagaeCondition( iArabia, iCordoba, 1, iProvinceOuter )

		# How much culture should we get into a province of this type, ignore the war and settler values (0,0)
		gc.setProvinceTypeParams( iProvinceNone, 0, 0, 1, 3 ) # 1/3 culture
		gc.setProvinceTypeParams( iProvinceOuter, 0, 0, 1, 1 ) # no change to culture
		gc.setProvinceTypeParams( iProvincePotential, 0, 0, 1, 1 ) # same as outer culture
		gc.setProvinceTypeParams( iProvinceNatural, 0, 0, 2, 1 ) # double-culture
		gc.setProvinceTypeParams( iProvinceCore, 0, 0, 3, 1 ) # triple-culture

		# block foundation of Protestantism except by a Catholic player
		gc.setParentSchismReligions( iCatholicism, iProtestantism )

		# block declaration of war against newly spawning nations for this many turns (pre-set wars are not affected)
		gc.setPaceTurnsAfterSpawn( 5 )

		# set the Visualization parameters, note that those functions can be accessed at any time, not just here
		# note that if you set Civs for mode 0 and 1 in WB mode, they will stay set until you exit
		gc.setWhatToPlot( 0 ) # 0 - Core (default), 1 - Normal, 2 - Settler, 3 - Wars
		#gc.setCivForCore( iByzantium ) # plot the Core of Byzantium (only if setWhatToPlot is set to 0)
		#gc.setCivForNormal( iByzantium ) # plot the Normal area of Byzantium (only if setWhatToPlot is set to 1)
		#gc.setCivForSettler( iFrankia ) # plot the Settlers Map of Byzantium (only if setWhatToPlot is set to 2)
		#gc.setCivForWars( iByzantium ) # plot the Wars Map of of Byzantium (only if setWhatToPlot is set to 3)

		self.postAreas()

	def setTechTimeline( self ):
		gc.setTimelineTechModifiers( 9, 25, -50, 1, 100, 50 ) # go between 10 times slower and 4 times faster
		# formula is: iAhistoric = iCurrentTurn - iHistoricTurn, capped at ( iTPCap, iTBCap )
		# iCost *= 100 + topPenalty * iHistoric * iAhistoric / BotPenalty, iCost /= 100
		# iCost *= 100 - topBuff * iHistoric * iAhistoric / BotBuff, iCost /= 100
		# gc.setTimelineTechDateForTech( iTech, iTurn )
		gc.setTimelineTechDateForTech( iCalendar, 0 )
		gc.setTimelineTechDateForTech( iArchitecture, 30 )
		gc.setTimelineTechDateForTech( iBronzeCasting, 15 )
		gc.setTimelineTechDateForTech( iTheology, 10 )
		gc.setTimelineTechDateForTech( iManorialism, 5 )
		gc.setTimelineTechDateForTech( iStirrup, i600AD )
		gc.setTimelineTechDateForTech( iEngineering, 55 ) #teir 2
		gc.setTimelineTechDateForTech( iChainMail, 43 )
		gc.setTimelineTechDateForTech( iArt, 38 )
		gc.setTimelineTechDateForTech( iMonasticism, 50 )
		gc.setTimelineTechDateForTech( iVassalage, 60 )
		gc.setTimelineTechDateForTech( iAstrolabe, 76 ) # teir 3
		gc.setTimelineTechDateForTech( iMachinery, 76 )
		gc.setTimelineTechDateForTech( iVaultedArches, 90 ) #
		gc.setTimelineTechDateForTech( iMusic, 80 )
		gc.setTimelineTechDateForTech( iHerbalMedicine, 95 )
		gc.setTimelineTechDateForTech( iFeudalism, i778AD ) # Feudalism
		gc.setTimelineTechDateForTech( iFarriers, 100 )
		gc.setTimelineTechDateForTech( iMapMaking, 145 )  # this is tier 5
		gc.setTimelineTechDateForTech( iBlastFurnace, 120 )# teir 4
		gc.setTimelineTechDateForTech( iSiegeEngines, i1097AD ) #trebuchets
		gc.setTimelineTechDateForTech( iGothicArchitecture, 130 ) # 12th century
		gc.setTimelineTechDateForTech( iLiterature, 145 )
		gc.setTimelineTechDateForTech( iCodeOfLaws, 120 )
		gc.setTimelineTechDateForTech( iAristocracy, 135 )
		gc.setTimelineTechDateForTech( iLateenSails, 125 ) # actually this is tier 4
		gc.setTimelineTechDateForTech( iPlateArmor, 152 ) # teir 5: Late 1200s, By the 14th century, plate armour was commonly used to supplement mail.
		gc.setTimelineTechDateForTech( iMonumentBuilding, 180 )
		gc.setTimelineTechDateForTech( iClassicalKnowledge, 175 )
		gc.setTimelineTechDateForTech( iAlchemy, i1003AD )
		gc.setTimelineTechDateForTech( iCivilService, 190 ) # teir 6
		gc.setTimelineTechDateForTech( iClockmaking, 200 )
		gc.setTimelineTechDateForTech( iPhilosophy, 215 )
		gc.setTimelineTechDateForTech( iEducation, 220 )
		gc.setTimelineTechDateForTech( iGuilds, 200 )
		gc.setTimelineTechDateForTech( iChivalry, 210 )
		gc.setTimelineTechDateForTech( iOptics, 228 ) # teir 7
		gc.setTimelineTechDateForTech( iReplaceableParts, 250 )
		gc.setTimelineTechDateForTech( iPatronage, 230 )
		gc.setTimelineTechDateForTech( iGunpowder, i1300AD )
		gc.setTimelineTechDateForTech( iBanking, 240 )
		gc.setTimelineTechDateForTech( iMilitaryTradition, 260 )
		gc.setTimelineTechDateForTech( iShipbuilding, 275 ) # teir 8
		gc.setTimelineTechDateForTech( iDrama, 270 )
		gc.setTimelineTechDateForTech( iDivineRight, 266 )
		gc.setTimelineTechDateForTech( iChemistry, 280 )
		gc.setTimelineTechDateForTech( iPaper, 290 )
		gc.setTimelineTechDateForTech( iProfessionalArmy, 295 )
		gc.setTimelineTechDateForTech( iPrintingPress, i1517AD ) # teir 9 turn 304
		gc.setTimelineTechDateForTech( iPublicWorks, 310 )
		gc.setTimelineTechDateForTech( iMatchlock, i1500AD )
		gc.setTimelineTechDateForTech( iArabicKnowledge, i1491AD ) # fall of Granada
		gc.setTimelineTechDateForTech( iAstronomy, i1514AD ) # teir 10 Copernicus
		gc.setTimelineTechDateForTech( iSteamEngines, i1690AD ) # first steam engine
		gc.setTimelineTechDateForTech( iConstitution, 375 )
		gc.setTimelineTechDateForTech( iPolygonalFort, 370 )
		gc.setTimelineTechDateForTech( iArabicMedicine, 342 )
		gc.setTimelineTechDateForTech( iRenaissanceArt, i1540AD ) # teir 11, 1541
		gc.setTimelineTechDateForTech( iNationalism, 380 )
		gc.setTimelineTechDateForTech( iLiberalism, 400 )
		gc.setTimelineTechDateForTech( iScientificMethod, i1623AD ) # Galileo
		gc.setTimelineTechDateForTech( iMilitaryTactics, 410 )
		gc.setTimelineTechDateForTech( iNavalArchitecture, 385 ) # teir 12
		gc.setTimelineTechDateForTech( iCivilEngineering, 395 )
		gc.setTimelineTechDateForTech( iRightOfMan, 460 )
		gc.setTimelineTechDateForTech( iEconomics, 435 )
		gc.setTimelineTechDateForTech( iPhysics, i1687AD )
		gc.setTimelineTechDateForTech( iBiology, 440 )
		gc.setTimelineTechDateForTech( iCombinedArms, 430 )
		gc.setTimelineTechDateForTech( iTradingCompanies, i1600AD ) # teir 13 TradingCompanies turn 325
		gc.setTimelineTechDateForTech( iMachineTools, 450 )
		gc.setTimelineTechDateForTech( iFreeMarket, 450 )
		gc.setTimelineTechDateForTech( iExplosives, 460 )
		gc.setTimelineTechDateForTech( iMedicine, 458 )
		gc.setTimelineTechDateForTech( iIndustrialTech, i1800AD )

	def preMapsNSizes( self ):
		# settlersMaps, DO NOT CHANGE THIS CODE
		gc.setSizeNPlayers( iMapMaxX, iMapMaxY, iNumPlayers, iNumTotalPlayers, iNumTechs, iNumBuildingsPlague, iNumReligions )
		for i in range( iNumPlayers ):
			for y in range( iMapMaxY ):
				for x in range( iMapMaxX ):
					gc.setSettlersMap( i, y, x, rfcemaps.tSettlersMaps[i][y][x] )
					gc.setWarsMap( i, y, x, rfcemaps.tWarsMaps[i][y][x] )

		for y in range( iMapMaxY ):
			for x in range( iMapMaxX ):
				if ( rfcemaps.tProinceMap[y][x] > -1 ):
					# "no province" of ocean is settled different than -1, set only non-negative values,
					# the C++ map is initialized to "no-province" by setSizeNPlayers(...)
					# "no-province" is returned as -1 via the Cy interface
					gc.setProvince( x, y, rfcemaps.tProinceMap[y][x] )
		gc.createProvinceCrossreferenceList() # make sure to call this AFTER setting all the Province entries

		gc.setProvinceTypeNumber( iNumProvinceTypes ) # set the Number of Provinces, call this before you set any AI or culture modifiers

		## Absinthe: disabled, was only needed for the AI regions
		#gc.setNumRegions( iNumMapRegions )
		#for lRegion in tRegionMap:
		#	iIndex = tRegionMap.index( lRegion )
		#	for iProvince in lRegion:
		#		gc.setProvinceToRegion( iProvince, iIndex )

		# birth turns for the players, do not change this loop
		for i in range( iNumTotalPlayers ):
			gc.setStartingTurn( i, tBirth[i] )

	def postAreas( self ):
		#3Miro: DO NOT CHANGE THIS CODE
		# this adds the Core and Normal Areas from Consts.py into C++. There is Dynamical Memory involved, so don't change this
		for iCiv in range( iNumPlayers ):
			iCBLx = tCoreAreasTL[iCiv][0]
			iCBLy = tCoreAreasTL[iCiv][1]
			iCTRx = tCoreAreasBR[iCiv][0]
			iCTRy = tCoreAreasBR[iCiv][1]
			iNBLx = tNormalAreasTL[iCiv][0]
			iNBLy = tNormalAreasTL[iCiv][1]
			iNTRx = tNormalAreasBR[iCiv][0]
			iNTRy = tNormalAreasBR[iCiv][1]
			iCCE = len( tExceptions[iCiv] )
			iCNE = len( tNormalAreasSubtract[iCiv] )
			gc.setCoreNormal( iCiv, iCBLx, iCBLy, iCTRx, iCTRy, iNBLx, iNBLy, iNTRx, iNTRy, iCCE, iCNE )
			for iEx in range( iCCE ):
				gc.addCoreException( iCiv, tExceptions[iCiv][iEx][0], tExceptions[iCiv][iEx][1] )
			for iEx in range( iCNE ):
				gc.addNormalException( iCiv, tNormalAreasSubtract[iCiv][iEx][0], tNormalAreasSubtract[iCiv][iEx][1] )

		gc.setProsecutorReligions( iProsecutor, iProsecutorClass )
		gc.setSaintParameters( iProphet, iSaintBenefit, 20, 40 ) # try to amass at least 20 and don't bother above 40 points
		gc.setIndependnets( iIndepStart, iIndepEnd, iBarbarian )
		gc.setPapalPlayer( iPope, iCatholicism )

		gc.setAutorunHack( iCatapult, 30, 0 ) # Autorun hack, sync with RNF module

		#3MiroMercs: set the merc promotion
		gc.setMercPromotion( iPromotionMerc )

		for iCiv in range( iNumPlayers ):
			#print( "  sw: ",iCiv )
			gc.setStartingWorkers( iCiv, tStartingWorkers[iCiv] )

