# RFC Europe, balancing modifiers are placed here
from CvPythonExtensions import *
import Consts as con
import XMLConsts as xml
import RFCEMaps as rfcemaps

gc = CyGlobalContext()	# LOQ


iBurgundy = con.iBurgundy
iByzantium = con.iByzantium
iFrankia = con.iFrankia
iArabia = con.iArabia
iBulgaria = con.iBulgaria
iCordoba = con.iCordoba
iSpain = con.iSpain
iNorse = con.iNorse
iVenecia = con.iVenecia
iKiev = con.iKiev
iHungary = con.iHungary
iGermany = con.iGermany
iPoland = con.iPoland
iLithuania = con.iLithuania
iMoscow = con.iMoscow
iGenoa = con.iGenoa
iEngland = con.iEngland
iPortugal = con.iPortugal
iAustria = con.iAustria
iTurkey = con.iTurkey
iSweden = con.iSweden
iDutch = con.iDutch
iPope = con.iPope
iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iIndependent3 = con.iIndependent3
iIndependent4 = con.iIndependent4
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers

iUP_Happiness = con.iUP_Happiness
iUP_PerCityCommerce = con.iUP_PerCityCommerce
iUP_CityTileYield = con.iUP_CityTileYield
iUP_ReligiousTolerance = con.iUP_ReligiousTolerance
iUP_CulturalTolerance = con.iUP_CulturalTolerance
iUP_CommercePercent = con.iUP_CommercePercent
iUP_UnitProduction = con.iUP_UnitProduction
iUP_EnableCivic = con.iUP_EnableCivic
iUP_TradeRoutes = con.iUP_TradeRoutes
iUP_ImprovementBonus = con.iUP_ImprovementBonus
iUP_PromotionI = con.iUP_PromotionI
iUP_PromotionII = con.iUP_PromotionII
iUP_CanEnterTerrain = con.iUP_CanEnterTerrain
iUP_NoResistance = con.iUP_NoResistance
iUP_Conscription = con.iUP_Conscription
iUP_Inquisition = con.iUP_Inquisition
iUP_Emperor = con.iUP_Emperor
iUP_Mercenaries = con.iUP_Mercenaries
iUP_Faith = con.iUP_Faith
iUP_LandStability = con.iUP_LandStability
iUP_Discovery = con.iUP_Discovery
iUP_EndlessLand = con.iUP_EndlessLand
iUP_ForeignSea = con.iUP_ForeignSea
iUP_Pious = con.iUP_Pious
iUP_PaganCulture = con.iUP_PaganCulture
iUP_PaganHappy = con.iUP_PaganHappy
iUP_StabilityConquestBoost = con.iUP_StabilityConquestBoost
iUP_StabilitySettler = con.iUP_StabilitySettler
iUP_Janissary = con.iUP_Janissary

iFP_Stability = con.iFP_Stability		
iFP_Civic = con.iFP_Civic			
iFP_Growth = con.iFP_Growth			
iFP_Units = con.iFP_Units			
iFP_Science = con.iFP_Science			
iFP_Production = con.iFP_Production		
iFP_Displomacy = con.iFP_Displomacy		

class RFCEBalance:

	def setBalanceParameters( self ):
	
		self.preMapsNSizes()
                
                self.setTechTimeline() # Timeline for correct tech three
		
		# 3Miro: consolidate several modifiers into fewer calls, makes it more structured. Each modfier works as described below.
		
		#void setGrowthModifiers( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop );
		# iInitPop is the initial population in a city, also can use gc.setInitialPopulation( iCiv, iInitPop ) to change a single civ
		# defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100, 1 )
		# 3Miro: ABOUT CULTURE notice the culture modifier is different from the others, it modifies the culture output as opposed to the culture threshhold
		# 	50 means less culture, 200 means more culture. This is applied to Culture output of 10 or more.
		gc.setGrowthModifiersAI(iBurgundy,     100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersHu(iBurgundy,     100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersAI(iByzantium,    150, 100, 200, 100, 100, 2 )
		gc.setGrowthModifiersHu(iByzantium,    150, 100, 200, 100, 100, 2 )
		gc.setGrowthModifiersAI(iFrankia,      100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersHu(iFrankia,      100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersAI(iArabia,       150, 100, 150, 100, 100, 1 )
		gc.setGrowthModifiersHu(iArabia,       150, 100, 150, 100, 100, 1 )
		gc.setGrowthModifiersAI(iBulgaria,     100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersHu(iBulgaria,     100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersAI(iCordoba,      150, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersHu(iCordoba,      150, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiersAI(iSpain,        100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iSpain,        100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iNorse,        100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iNorse,        100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iVenecia,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iVenecia,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iKiev,         100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iKiev,         100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iHungary,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iHungary,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iGermany,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iGermany,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iPoland,       100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersHu(iPoland,       100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiersAI(iMoscow,       100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iMoscow,       100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iGenoa,        100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iGenoa,        100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iEngland,      100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iEngland,      100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iPortugal,     100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iPortugal,     100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iLithuania,    100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iLithuania,    100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iAustria,      100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iAustria,      100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iTurkey,       100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersHu(iTurkey,       100, 150, 100, 100, 100, 3 )
		gc.setGrowthModifiersAI(iSweden,       100, 150, 100, 100, 100, 4 )
		gc.setGrowthModifiersHu(iSweden,       100, 150, 100, 100, 100, 4 )
		gc.setGrowthModifiersAI(iDutch,        100, 200,  50, 100,  50, 4 )
		gc.setGrowthModifiersHu(iDutch,        100, 200,  50, 100,  50, 4 )
		gc.setGrowthModifiersAI(iPope,         150,  75, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iIndependent,  100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iIndependent2, 100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iIndependent3, 100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iIndependent4, 100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiersAI(iBarbarian,    100, 100, 100,  50, 100, 1 )

		
		#void setProductionModifiers( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
		# defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100 )
		# 3Miro: at 100 research cost, the cost is exactly as in the XML files, the cost in general is however increased for all civs
		gc.setProductionModifiersAI(iBurgundy,  110, 110, 120, 130 )
		gc.setProductionModifiersHu(iBurgundy,  110, 110, 120, 130 )
		gc.setProductionModifiersAI(iByzantium, 220, 150, 200, 350 )
		gc.setProductionModifiersHu(iByzantium, 220, 150, 200, 350 )
		gc.setProductionModifiersAI(iFrankia,   125, 110, 125, 125 )
		gc.setProductionModifiersHu(iFrankia,   125, 110, 125, 125 )
		gc.setProductionModifiersAI(iArabia,    125, 125, 150, 250 )
		gc.setProductionModifiersHu(iArabia,    125, 125, 150, 250 )
		gc.setProductionModifiersAI(iBulgaria,  125, 100, 125, 150 )
		gc.setProductionModifiersHu(iBulgaria,  125, 100, 125, 150 )
		gc.setProductionModifiersAI(iCordoba,   125, 150, 125, 250 )
		gc.setProductionModifiersHu(iCordoba,   125, 150, 125, 250 )
		gc.setProductionModifiersAI(iSpain,      85, 100, 100, 120 )
		gc.setProductionModifiersHu(iSpain,      90, 100, 100, 120 )
		gc.setProductionModifiersAI(iNorse,     100, 100, 100, 100 )
		gc.setProductionModifiersHu(iNorse,     100, 100, 100, 100 )
		gc.setProductionModifiersAI(iVenecia,   125, 100, 100, 125 )
		gc.setProductionModifiersHu(iVenecia,   125, 100, 100, 125 )
		gc.setProductionModifiersAI(iKiev,      100, 100, 100, 150 )
		gc.setProductionModifiersHu(iKiev,      100, 100, 100, 150 )
		gc.setProductionModifiersAI(iHungary,   125, 125, 100, 150 )
		gc.setProductionModifiersHu(iHungary,   125, 125, 100, 150 )
		gc.setProductionModifiersAI(iGermany,   110, 110, 120, 130 )
		gc.setProductionModifiersHu(iGermany,   110, 110, 120, 130 )
		gc.setProductionModifiersAI(iPoland,    100, 160, 140, 140 )
		gc.setProductionModifiersHu(iPoland,    100, 160, 140, 140 )
		gc.setProductionModifiersAI(iMoscow,     75,  75, 100, 150 )
		gc.setProductionModifiersHu(iMoscow,     75,  75, 100, 150 )
		gc.setProductionModifiersAI(iGenoa,     100, 100, 100, 125 )
		gc.setProductionModifiersHu(iGenoa,     100, 100, 100, 125 )
		gc.setProductionModifiersAI(iEngland,   90, 100, 100, 100 )
		gc.setProductionModifiersHu(iEngland,   90, 100, 100, 100 )
		gc.setProductionModifiersAI(iPortugal,  100, 100, 100,  90 )
		gc.setProductionModifiersHu(iPortugal,  100, 100, 100,  90 )
		gc.setProductionModifiersAI(iLithuania, 100, 150, 140, 100 )
		gc.setProductionModifiersHu(iLithuania, 100, 150, 140, 100 )
		gc.setProductionModifiersAI(iAustria,    60,  75, 100,  75 )
		gc.setProductionModifiersHu(iAustria,    60,  75, 100,  75 )
		gc.setProductionModifiersAI(iTurkey,     40,  75, 100,  90 )
		gc.setProductionModifiersHu(iTurkey,     40,  75, 100,  90 )
		gc.setProductionModifiersAI(iSweden,     50,  50, 100,  80 )
		gc.setProductionModifiersHu(iSweden,     50,  50, 100,  80 )
		gc.setProductionModifiersAI(iDutch,     100,  50,  30,  40 )
		gc.setProductionModifiersHu(iDutch,     100,  50,  30,  40 )
		gc.setProductionModifiersAI(iPope,      300, 200, 100, 350 )
		gc.setProductionModifiersAI(iIndependent, 170, 100, 400, 200 ) #The peaceful ones
		gc.setProductionModifiersAI(iIndependent2, 170, 100, 400, 200 )
		gc.setProductionModifiersAI(iIndependent3, 125, 100, 600, 300 ) #The warlike ones
		gc.setProductionModifiersAI(iIndependent4, 125, 100, 600, 300 )
		gc.setProductionModifiersAI(iBarbarian, 125, 100, 1000, 350 )

		#void setSupportModifiers( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
		# defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100 )
		gc.setSupportModifiersAI(iBurgundy,      10, 150,  80,  75, 110 )
		gc.setSupportModifiersHu(iBurgundy,      10, 150,  80,  75, 110 )
		gc.setSupportModifiersAI(iByzantium,     30, 150,  10,  10, 120 )
		gc.setSupportModifiersHu(iByzantium,     30, 150,  10,  10, 120 )
		gc.setSupportModifiersAI(iFrankia,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iFrankia,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iArabia,        10, 100,  50,  15, 120 )
		gc.setSupportModifiersHu(iArabia,        10, 100,  50,  15, 120 )
		gc.setSupportModifiersAI(iBulgaria,      10, 150,  50,  25, 110 )
		gc.setSupportModifiersHu(iBulgaria,      10, 150,  50,  25, 110 )
		gc.setSupportModifiersAI(iCordoba,       20, 100,  50,  50, 120 )
		gc.setSupportModifiersHu(iCordoba,       20, 100,  50,  50, 120 )
		gc.setSupportModifiersAI(iSpain,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iSpain,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iNorse,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iNorse,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iVenecia,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iVenecia,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iKiev,          10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iKiev,          10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iHungary,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iHungary,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iGermany,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iGermany,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iPoland,        10, 100,  75,  40, 100 )
		gc.setSupportModifiersHu(iPoland,        10, 100,  75,  40, 100 )
		gc.setSupportModifiersAI(iMoscow,        10, 100,  50,  25, 100 ) # sync with UP
		gc.setSupportModifiersHu(iMoscow,        10, 100,  50,  25, 100 ) # sync with UP
		gc.setSupportModifiersAI(iGenoa,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iGenoa,         10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iEngland,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iEngland,       10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iPortugal,      10, 100,  50,  25, 100 )
		gc.setSupportModifiersHu(iPortugal,      10, 100,  50,  25, 100 )
		gc.setSupportModifiersAI(iLithuania,     10,  85,  50,  40, 100 )
		gc.setSupportModifiersHu(iLithuania,     10,  85,  50,  40, 100 )
		gc.setSupportModifiersAI(iAustria,       10,  75,  50,  25, 100 )
		gc.setSupportModifiersHu(iAustria,       10,  75,  50,  25, 100 )
		gc.setSupportModifiersAI(iTurkey,        10,  25,  10,  10, 100 )
		gc.setSupportModifiersHu(iTurkey,        10,  25,  10,  10, 100 )
		gc.setSupportModifiersAI(iSweden,        10,  75,  50,  10, 100 )
		gc.setSupportModifiersHu(iSweden,        10,  75,  50,  10, 100 )
		gc.setSupportModifiersAI(iDutch,         10,  50, 200, 200, 100 )
		gc.setSupportModifiersHu(iDutch,         10,  50, 200, 200, 100 )
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

		#3Miro: setUnitSupportModifier(iCiv, iVal), set unit sipport modifiers for the player. Same as growth.
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
		
		#gc.setInitialBuilding( iSpain, con.iGranary, True )
		gc.setInitialBuilding( iSpain, xml.iBarracks, True )

		gc.setInitialBuilding( iMoscow, xml.iGranary, True )
		gc.setInitialBuilding( iMoscow, xml.iBarracks, True )
		gc.setInitialBuilding( iMoscow, xml.iForge, True )
		gc.setInitialBuilding( iMoscow, xml.iMarket, True )
		
		gc.setInitialBuilding( iGenoa, xml.iGranary, True )
		gc.setInitialBuilding( iGenoa, xml.iBarracks, True )
		
		gc.setInitialBuilding( iEngland, xml.iGranary, True )
		gc.setInitialBuilding( iEngland, xml.iBarracks, True )
		
		gc.setInitialBuilding( iPortugal, xml.iGranary, True )
		gc.setInitialBuilding( iPortugal, xml.iBarracks, True )
		#gc.setInitialBuilding( iPortugal, xml.iPortugalFeitoria, True )
                
		gc.setInitialBuilding( iLithuania, xml.iGranary, True )
		gc.setInitialBuilding( iLithuania, xml.iBarracks, True )

		gc.setInitialBuilding( iAustria, xml.iGranary, True )
		gc.setInitialBuilding( iAustria, xml.iBarracks, True )
		
		gc.setInitialBuilding( iTurkey, xml.iGranary, True )
		gc.setInitialBuilding( iTurkey, xml.iBarracks, True )
		gc.setInitialBuilding( iTurkey, xml.iForge, True )
		gc.setInitialBuilding( iTurkey, xml.iHarbor, True )
		gc.setInitialBuilding( iTurkey, xml.iOttomanHammam, True )
		
		gc.setInitialBuilding( iSweden, xml.iGranary, True )
		gc.setInitialBuilding( iSweden, xml.iSwedishTennant, True )
		gc.setInitialBuilding( iSweden, xml.iForge, True )
		gc.setInitialBuilding( iSweden, xml.iHarbor, True )
		gc.setInitialBuilding( iSweden, xml.iAqueduct, True )

		gc.setInitialBuilding( iDutch, xml.iGranary, True )
		gc.setInitialBuilding( iDutch, xml.iBarracks, True )
		gc.setInitialBuilding( iDutch, xml.iForge, True )
		gc.setInitialBuilding( iDutch, xml.iHarbor, True )
		gc.setInitialBuilding( iDutch, xml.iAqueduct, True )
		gc.setInitialBuilding( iDutch, xml.iMarket, True )
		gc.setInitialBuilding( iDutch, xml.iLighthouse, True )
		gc.setInitialBuilding( iDutch, xml.iTheatre, True )
		gc.setInitialBuilding( iDutch, xml.iSmokehouse, True )
		
		####### AI Modifiers
		#3Miro: setCityClusterAI(iCiv,iTop,iBottom,iMinus) for each AI civilization (set them for all, but only the AI make difference)
		# this determines how clustered the cities would be
		# AI_foundValue in PlayerAI would compute for a candidate city location the number of plots that are taken (i.e. by another city)
		# in CivIV, if more than a third of the tiles are "taken", do not found city there. In RFC, cities are clustered closer
		# if ( iTaken > 21 * iTop / iBottom - iMinus ) do not build city there.
		# default values are 2/3 -1 for Europe, 1/3 - 0 for Russia and 1/2 for Mongolia
		# for example gc.setCityClusterAI( iByzantium, 1, 3, 1 ) would force Byzantium to spread out
		gc.setCityClusterAI( iBurgundy, 2, 3, 1 )
		gc.setCityClusterAI( iByzantium, 1, 3, 1 )
		gc.setCityClusterAI( iFrankia, 1, 3, 1 )
		gc.setCityClusterAI( iArabia, 1, 3, 1 )
		gc.setCityClusterAI( iBulgaria, 1, 2, 1 )
		gc.setCityClusterAI( iCordoba, 1, 2, 1 )
		gc.setCityClusterAI( iSpain, 1, 2, 1 )
		gc.setCityClusterAI( iNorse, 1, 3, 1 )
		gc.setCityClusterAI( iVenecia, 1, 3, 1 )
		gc.setCityClusterAI( iKiev, 1, 4, 1 )
		gc.setCityClusterAI( iHungary, 1, 3, 1 )
		gc.setCityClusterAI( iGermany, 1, 3, 1 )
		gc.setCityClusterAI( iPoland, 1, 4, 1 )
		gc.setCityClusterAI( iMoscow, 1, 4, 1 )
		gc.setCityClusterAI( iPortugal, 1, 2, 1 )
		gc.setCityClusterAI( iLithuania, 1, 4, 1 )
		gc.setCityClusterAI( iGenoa, 1, 3, 1 )
		gc.setCityClusterAI( iEngland, 1, 3, 1 )
		gc.setCityClusterAI( iAustria, 1, 3, 1 )
		gc.setCityClusterAI( iTurkey, 1, 3, 1 )
		gc.setCityClusterAI( iSweden, 1, 3, 1 )		
		gc.setCityClusterAI( iDutch, 3, 4, 1 )

		#3Miro: setCityWarDistanceAI(iCiv,iVal), depending on the type of the empire, modify how likely the AI is to attack a city
		# values are 1 - small empires (Egypt,default), 2 - large contiguous empires (Rome,Arabia), 3 - global empire (England,Russia,Mongolia)
		gc.setCityWarDistanceAI( iBurgundy, 1 )
		gc.setCityWarDistanceAI( iByzantium, 2 )
		gc.setCityWarDistanceAI( iFrankia, 2 )
		gc.setCityWarDistanceAI( iArabia, 2 )
		gc.setCityWarDistanceAI( iBulgaria, 2 )
		gc.setCityWarDistanceAI( iCordoba, 1 )
		gc.setCityWarDistanceAI( iSpain, 3 )
		gc.setCityWarDistanceAI( iNorse, 3 )
		gc.setCityWarDistanceAI( iVenecia, 3 )
		gc.setCityWarDistanceAI( iKiev, 2 )
		gc.setCityWarDistanceAI( iHungary, 2 )
		gc.setCityWarDistanceAI( iGermany, 2 )
		gc.setCityWarDistanceAI( iPoland, 2 )
		gc.setCityWarDistanceAI( iMoscow, 2 )
		gc.setCityWarDistanceAI( iPortugal, 2 )
		gc.setCityWarDistanceAI( iLithuania, 2 )
		gc.setCityWarDistanceAI( iGenoa, 3 )
		gc.setCityWarDistanceAI( iEngland, 3 )
		gc.setCityWarDistanceAI( iAustria, 2 )		
		gc.setCityWarDistanceAI( iTurkey, 2 )
		gc.setCityWarDistanceAI( iSweden, 2 )
		gc.setCityWarDistanceAI( iDutch, 1 )

		#3Miro: setTechPreferenceAI(iCiv,iTech,iVal), for each civ, for each tech, specify how likable it is. iVal is same as in growth.
		# low percent makes the tech less desirable
		#gc.setTechPreferenceAI(iByzantium,1,200)
		#gc.setTechPreferenceAI(iFrankia,1,200)
		gc.setTechPreferenceAI(iBulgaria,xml.iBronzeCasting,200)				
		gc.setTechPreferenceAI(iGermany,xml.iPrintingPress,200)
		gc.setTechPreferenceAI(iEngland,xml.iPrintingPress,150)
		gc.setTechPreferenceAI(iPope,xml.iPrintingPress,10) # Pope shouldn't want this

		gc.setTechPreferenceAI(iSpain,xml.iAstronomy,200)
		gc.setTechPreferenceAI(iPortugal,xml.iAstronomy,200)
		
		#3Miro: setDiplomacyModifiers(iCiv1,iCiv2,iVal) hidden modifier for the two civ's AI relations. More likely to have OB and so on.
		# + means they will like each other - they will hate each other.
		# from Civ1 towards Civ2 (make them symmetric)
		gc.setDiplomacyModifiers( iCordoba, iArabia, +8 )
		gc.setDiplomacyModifiers( iArabia, iCordoba, +8 )
		gc.setDiplomacyModifiers( iArabia, iByzantium, -10 )
		gc.setDiplomacyModifiers( iByzantium, iArabia, -10 )
		gc.setDiplomacyModifiers( iBulgaria, iByzantium, +4 )
		gc.setDiplomacyModifiers( iByzantium, iBulgaria, +4 )		
		gc.setDiplomacyModifiers( iCordoba, iSpain, -20 )
		gc.setDiplomacyModifiers( iSpain, iCordoba, -20 )
		gc.setDiplomacyModifiers( iPortugal, iSpain, +8 )
		gc.setDiplomacyModifiers( iSpain, iPortugal, +8 )
		gc.setDiplomacyModifiers( iCordoba, iPortugal, -10 )
		gc.setDiplomacyModifiers( iPortugal, iCordoba, -10 )		
		#gc.setDiplomacyModifiers( iFrankia, iBurgundy, -6 )
		#gc.setDiplomacyModifiers( iBurgundy, iFrankia, -6 )
		gc.setDiplomacyModifiers( iTurkey, iByzantium, -20 )
		gc.setDiplomacyModifiers( iByzantium, iTurkey, -20 )
		gc.setDiplomacyModifiers( iGermany, iPoland, -5 )
		gc.setDiplomacyModifiers( iPoland, iGermany, -5 )
		gc.setDiplomacyModifiers( iMoscow, iPoland, -5 )
		gc.setDiplomacyModifiers( iPoland, iMoscow, -5 )
		gc.setDiplomacyModifiers( iAustria, iPoland, -2 )
		gc.setDiplomacyModifiers( iPoland, iAustria, -2 )
		gc.setDiplomacyModifiers( iLithuania, iPoland, +4 )
		gc.setDiplomacyModifiers( iPoland, iLithuania, +4 )
		gc.setDiplomacyModifiers( iHungary, iPoland, +3 )
		gc.setDiplomacyModifiers( iPoland, iHungary, +3 )
		gc.setDiplomacyModifiers( iAustria, iHungary, -10)
		gc.setDiplomacyModifiers( iHungary, iAustria, -10)
		gc.setDiplomacyModifiers( iSweden, iPoland, -2 )
		gc.setDiplomacyModifiers( iPoland, iSweden, -2 )
		
		#gc.setDiplomacyModifiers( iIndependent, iIndependent2, -10 )
		
			
		####### 3Miro: UNIQUE POWERS
		#3Miro: setUP(iCiv,iPower) sets the Unique Powers for C++
		
		#3Miro: setUP(iCiv,iPower,iParameter)
		# iUP_Happiness, iParameter = the amount of additional happiness
		# iUP_PerCityCommerce, iParameter = 1000000 * bonus_in_gold + 10000*bonus_in_research + 100*bonus_in_culture + bonus_in_espionage (bonuses are limited to 0 - 99)
		# iUP_CityTileYield, iParameter = 100000 * iFoodBonus + 1000 * iProductionBonus + iCommerceBonus, food and production are limited to (0-99) and commerce to (0-999)
		# iUP_CommercePercent, iParameter = 1000000 * bonus_in_gold + 10000*bonus_in_research + 100*bonus_in_culture + bonus_in_espionage (bonuses are limited to 0 - 99 percent)
		# iUP_CulturalTolerance. iParameter = 0 for no unhappiness or unhappiness = unhappiness / iParameter
		# iUP_ReligiousTolerance. iParameter = 0 for no instability
		# iUP_Conscription, iParameter = percent of foreign culture needed to draft + 100 * max number of units to draft per turn
		# iUP_NoResistance, iParameter = 0 for no resistane or resistance turns = resistance turns / iParameter
		# iUP_UnitProduction, iParameter = iRequiredTech * 100 + Percent ( 75% for 25% faster unit building)
		# iUP_EnableCivic, iParameter = Civic5 * 100000000 + Civic4 * 1000000 + Civic3 * 10000 + Civic2 * 100 + Civic1, NOTE: also need to enable this in the WB, civic indexed by 0 is always available, civic5 cannot be bigger than 20
		# iUP_TradeRoutes, iParameter = number of extra trade routes, NOTE: this must be syncronized with GlobalDefines.xml: max trade routes
		# iUP_ImprovementBonus, iParameter = iImprovement * 1000000 + iFoodBonus * 10000 + iProductionBonus * 100 + iCommerceBonus, bonuses are limited to (0-99)
		# iUP_PromotionI, iParameter = the bonus promotion
		# iUP_PromotionII, iParameter = the bonus promotion
		# iUP_Inquisition, iParameter is not used
		# iUP_CanEnterTerrain, iParameter is the terrain to enter
		# iUP_Discoveru, iParameter = ColonyStart * 1000000 + ColonyEnd * 1000 + iModifier modifies the cost assosiated with all projects (iCost *= iModifier; iCost /= 100 )
		# iUP_EndlessLand, iParameter = percent change (i.e. upkeep *= iParameter, upkeep /= 100 )
		# iUP_ForeignSea, use iParameter = 1
		# iUP_Pious, whenever changeFaith( x ) is called, x is multiplied by iParameter
		
		gc.setUP( iBurgundy, iUP_Happiness, 1 )
		gc.setUP( iBurgundy, iUP_PerCityCommerce, 200)
		
		gc.setUP( iByzantium, iUP_Emperor, 1 )
		
		gc.setUP( iFrankia, iUP_LandStability, 1 )
		gc.setUP( iFrankia, iUP_CulturalTolerance, 0 )
		
		gc.setUP( iArabia, iUP_Faith, 1 )
		
		gc.setUP( iBulgaria, iUP_NoResistance, 0 )		

		gc.setUP( iCordoba, iUP_PromotionI, xml.iPromotionMedicI )
		
		gc.setUP( iSpain, iUP_Inquisition, 1 )
		gc.setUP( iSpain, iUP_PerCityCommerce, 2 )
		
		gc.setUP( iNorse, iUP_CanEnterTerrain, xml.iTerrainOcean )
                gc.setUP( iNorse, iUP_StabilitySettler, 1 )

		#JediClemente: changed to only Merchant Republic
		gc.setUP( iVenecia, iUP_EnableCivic, xml.iCivicMerchantRepublic ) # before + con.iCivicRepublic
		#gc.setUP( iVenecia, iUP_ForeignSea, 1 )
		
		gc.setUP( iKiev, iUP_CityTileYield, 100000 * 2 )
		
		gc.setUP( iHungary, iUP_Happiness, 1 )
		gc.setUP( iHungary, iUP_CulturalTolerance, 0 )
		
		gc.setUP( iGermany, iUP_UnitProduction, xml.iGunpowder * 100 + 75 )
		
		gc.setUP( iPoland, iUP_ReligiousTolerance, 0 )
                
                gc.setUP( iLithuania, iUP_PaganCulture, 200 )
                gc.setUP( iLithuania, iUP_PaganHappy, 1 )
		
		gc.setSupportModifiersAI(iMoscow, 10, 100, 25, 12, 100 )
                gc.setSupportModifiersHu(iMoscow, 10, 100, 25, 12, 100 )
		gc.setUP( iMoscow, iUP_EndlessLand, 50 )
		
		gc.setUP( iGenoa, iUP_Mercenaries, 1 ) # this actually has no effect, it is implemented in Mercenaries entirelly
		
		gc.setUP( iEngland, iUP_ImprovementBonus, xml.iImprovementWorkshop * 1000000 + 200 )
		
                # Speedup East/West India Trading Companies
		gc.setUP( iPortugal, iUP_Discovery, (xml.iNumNotColonies-2) * 1000000 + (xml.iNumTotalColonies-1) * 1000 + 40 );
                gc.setUP( iPortugal, iUP_StabilitySettler, 1 )
		
		for i in range( iNumTotalPlayers ):
			if ( not i == iAustria ):
				gc.setDiplomacyModifiers( i, iAustria, +4 )
				
		#gc.setUP( iTurkey, iUP_Conscription, 330 )
                #gc.setUP( iTurkey, iUP_Conscription, 1 )
                gc.setUP( iTurkey, iUP_Janissary, 1 )
		
		gc.setUP( iSweden, iUP_PromotionI, xml.iPromotionFormation )
		
		gc.setUP( iDutch, iUP_TradeRoutes, 2 )
		gc.setUP( iDutch, iUP_Pious, 2 ) # 3Miro: "hidden" buff to the Dutch FP, otherwise they have too little (not enouth cities)
                gc.setUP( iDutch, iUP_Discovery, (xml.iNumNotColonies-2) * 1000000 + (xml.iNumTotalColonies-1) * 1000 + 30 );

		gc.setUP( iPope, iUP_Emperor, 1 )

		# GlobalWarming
		gc.setGlobalWarming( False )
		
		# Set FastTerrain (i.e. double movement over ocean)
		gc.setFastTerrain( xml.iTerrainOcean )
		
		# set religious spread factors
		for iCiv in range( iNumTotalPlayers + 1 ): # include barbs
			for iRel in range( xml.iNumReligions ):
				gc.setReligionSpread( iCiv, iRel, con.tReligionSpreadFactor[iCiv][iRel] )
				
		# set the religions and year of the great schism
		gc.setSchism( xml.iCatholicism, xml.iOrthodoxy, xml.i1053AD )

		gc.setHoliestCity( con.iJerusalem[0], con.iJerusalem[1] )
		
		# 3Miro: Faith Points benefits
		# gc.setReligionBenefit( iReligion, iFP_(whatever it is), iParameter, iCap )
		# 	note that for powers iParameter = -1 means that this religion doesn't have this power (-1 is the default)
		#	iCap sets a cap for the maximum number of FP a religion can have (per player) Can be adjusted per Player
		#
		# iFP_Stability: stability += iParameter * num_FaithPoints / 100
		#		 i.e. 1 Faith Point = iParameter percent of a stability point
		# iFP_Civic: civic_upkeep *= 100 - (num_FaithPoints * iParameter) / 100
		#	     civic_upkeep /= 100
		#	     iParameter = 200, means 2% lower cost per Faith Point, iParameter = 50 means .5% lower cost per FP
		# iFP_Growth: iTreshhold *= 100 - (num_FaithPoints * iParameter) / 100
		#	      iTreshhold /= 100
		#	      iParameter = 200, means 2% faster growth per Faith Point, iParameter = 50 means .5% faster growth per FP
		# iFP_Units: iProductionNeeded *= 100 - (num_FaithPoints * iParameter) / 100
		#	     iProductionNeeded /= 100
		#	     iParameter = 200, means 2% faster production per Faith Point, iParameter = 50 means .5% faster production per FP
		# iFP_Science: same as units, iParameter = 200, means 2% lower tech cost per Faith Point, iParameter = 50 means .5% lower tech cost per FP
		# iFP_Production: iProductionNeeded *= 100 - (num_FaithPoints * iParameter) / 100
		#	     	  iProductionNeeded /= 100
		#	     	  iParameter = 200, means 2% faster production per Faith Point, iParameter = 50 means .5% faster production per FP
		#		  Counts for Wonders and Projects
		# iFP_Displomacy: iAttitude += 	iParameter * num_FaithPoints / 100
		#		 i.e. 1 Faith Point = iParameter percent of an attitude point
		
		gc.setReligionBenefit( xml.iOrthodoxy, con.iFP_Stability, 8, 100 )
		gc.setReligionBenefit( xml.iOrthodoxy, con.iFP_Civic, 50, 100 )
		
		gc.setReligionBenefit( xml.iIslam, con.iFP_Growth, 50, 100 )
		gc.setReligionBenefit( xml.iIslam, con.iFP_Units, 50, 100 )
		
		gc.setReligionBenefit( xml.iProtestantism, con.iFP_Science, 30, 100 )
		gc.setReligionBenefit( xml.iProtestantism, con.iFP_Production, 30, 100 )
		
		gc.setReligionBenefit( xml.iCatholicism, con.iFP_Displomacy, 6, 100 )
		gc.setReligionBenefit( xml.iIslam, con.iFP_Displomacy, 10, 100 )
		gc.setReligionBenefit( xml.iProtestantism, con.iFP_Displomacy, 6, 100 )

		# every nation gets a land tile that is normally impassible and now pass through it
		#gc.setStrategicTile( iVenecia, 56, 35 )
		
		# set AI modifiers for preffered buildings (it is possible that it works only for wonders)
		# gc.setBuildingPref( iFrankia, con.iNotreDame, 10 )
		# gc.setBuildingPref( iCordoba, con.iNotreDame, -10 )
		# use values -10 for very unlikely, 0 for default neutral and positive for desirable
		# values less than -10 might not work, above 10 should be fine
		
		gc.setBuildingPref( iBurgundy, xml.iMonasteryOfCluny, 20 )
		
		gc.setBuildingPref( iByzantium, xml.iRoundChurch, -3 )
		gc.setBuildingPref( iByzantium, xml.iGoldenBull, -3 )
		
		gc.setBuildingPref( iFrankia, xml.iNotreDame, 20 )
		gc.setBuildingPref( iFrankia, xml.iVersailles, 10 )
		gc.setBuildingPref( iFrankia, xml.iFontainebleau, 10 )
		
		gc.setBuildingPref( iArabia, xml.iDomeRock, 10 )
		gc.setBuildingPref( iArabia, xml.iTombKhal, 20 )
		gc.setBuildingPref( iArabia, xml.iNotreDame, -3 )
		gc.setBuildingPref( iArabia, xml.iSistineChapel, -3 )
		gc.setBuildingPref( iArabia, xml.iKrakDesChevaliers, -3 )
		gc.setBuildingPref( iArabia, xml.iGoldenBull, -3 )
		gc.setBuildingPref( iArabia, xml.iCopernicus, -3 )
		
		gc.setBuildingPref( iBulgaria, xml.iRoundChurch, 20 )
		
		gc.setBuildingPref( iCordoba, xml.iGardensAlAndalus, 20 )
		gc.setBuildingPref( iCordoba, xml.iLaMezquita, 20 )
		gc.setBuildingPref( iCordoba, xml.iAlhambra, 20 )
		gc.setBuildingPref( iCordoba, xml.iDomeRock, 10 )
		gc.setBuildingPref( iCordoba, xml.iNotreDame, -3 )
		gc.setBuildingPref( iCordoba, xml.iSistineChapel, -3 )
		gc.setBuildingPref( iCordoba, xml.iKrakDesChevaliers, -3 )
		gc.setBuildingPref( iCordoba, xml.iGoldenBull, -3 )
		
		gc.setBuildingPref( iSpain, xml.iEscorial, 20 )
		gc.setBuildingPref( iSpain, xml.iMagellansVoyage, 10 )
		
		gc.setBuildingPref( iNorse, xml.iShrineOfUppsala, 20 )
		gc.setBuildingPref( iNorse, xml.iKalmarCastle, 10 )
		
		gc.setBuildingPref( iVenecia, xml.iMarcoPolo, 10 )
		gc.setBuildingPref( iVenecia, xml.iSanMarco, 10 )
		gc.setBuildingPref( iVenecia, xml.iLanterna, 10 )
		gc.setBuildingPref( iVenecia, xml.iLeonardosWorkshop, 5 )
		
		gc.setBuildingPref( iKiev, xml.iSophiaKiev, 20 )
		
		gc.setBuildingPref( iHungary, xml.iPressburg, 20 )
		gc.setBuildingPref( iHungary, xml.iGoldenBull, 20 )
		gc.setBuildingPref( iHungary, xml.iBibliothecaCorviniana, 10 )
		gc.setBuildingPref( iHungary, xml.iTempleMount, 5 )

		gc.setBuildingPref( iGermany, xml.iBrandenburgGate, 20 )
		gc.setBuildingPref( iGermany, xml.iImperialDiet, 10 )
		gc.setBuildingPref( iGermany, xml.iCopernicus, 5 )
		
		gc.setBuildingPref( iPoland, xml.iPressburg, 10 )
		gc.setBuildingPref( iPoland, xml.iCopernicus, 5 )
		gc.setBuildingPref( iPoland, xml.iGoldenBull, 5 )
		gc.setBuildingPref( iPoland, xml.iTempleMount, 15 )
		
		gc.setBuildingPref( iMoscow, xml.iStBasil, 20 )
		
		gc.setBuildingPref( iGenoa, xml.iSanGiorgio, 20 )
		gc.setBuildingPref( iGenoa, xml.iLanterna, 20 )
		gc.setBuildingPref( iGenoa, xml.iLeonardosWorkshop, 5 )
		
		gc.setBuildingPref( iEngland, xml.iMagnaCarta, 20 )
		gc.setBuildingPref( iEngland, xml.iWestminster, 10 )
		#JediClemente: Tower of London is a national wonder!
		
		gc.setBuildingPref( iPortugal, xml.iBelemTower, 20 )
		gc.setBuildingPref( iPortugal, xml.iRibeira, 20 )
		
		gc.setBuildingPref( iAustria, xml.iStephansdom, 20 )
		
		gc.setBuildingPref( iTurkey, xml.iTopkapiPalace, 20 )
		
		gc.setBuildingPref( iSweden, xml.iKalmarCastle, 20 )
		
		gc.setBuildingPref( iDutch, xml.iBeurs, 20 )

		gc.setBuildingPref( iPope, xml.iSistineChapel, 20 )


		# Manor House + Manorism: iBuilding + 1000 * iCivic + 100,000 * iGold + 1,000,000 * iResearch + 10,000,000 * iCulture + 100,000,000 * iEspionage
                # 3Miro: moved to XML, no need to put it here
		#gc.setBuildingCivicCommerseCombo1( xml.iManorHouse + 1000 * xml.iManorialism + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
		#gc.setBuildingCivicCommerseCombo2( xml.iFrenchChateau + 1000 * xml.iManorialism + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
		#gc.setBuildingCivicCommerseCombo3(-1)

		# 3Miro: Psycho AI cheat, this will make Ottoman AI think it can win battles vs Constantinople at 90/100 rate
		#  it will also indeed boost Ottoman's odds, but only by about 60 percent (maybe even less)
		#   works only for AI vs AI, Humans are excempts of this rule
		#gc.setPsychoAICheat( iBulgaria, con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ); # This is for testing only
		gc.setPsychoAICheat( iTurkey, con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] )

		# 3Miro: be very careful here, this can really mess the AI
		#        this works only for AI vs AI, if either player is Human, this is ignored
		#        setHistoricalEnemyAICheat( iAttacker, iDefender, 10 ) gives the attacker +10% bonus, when attacking units belonging to the defender
		#        none of the AI players is "aware" of the modification, if you make it too big, then the AI will act really stupid (even for an AI)
		#        this should be "last" resot solution, other methods are always preferable
		gc.setHistoricalEnemyAICheat( iTurkey, iBulgaria,  10 )
		gc.setHistoricalEnemyAICheat( iBulgaria, iTurkey, -10 )
                
                gc.setHistoricalEnemyAICheat( iSpain, iCordoba,  10 )
		gc.setHistoricalEnemyAICheat( iCordoba, iSpain, -10 )
                
                # 3Miro: this sets rules on how players can Vassalize, first two parameters are the players (we should probably keep this symmetric)
                #        second parameter is -1: cannot Vassalize, 0: has to satisfy a condition (default), 1 can Vassalize without conditions
                #        the condition is that either one of the players needs to have a city in a province that the other players considers >= the last parameter
                #        the default for the last parameter is 0, we should call this at least once to set the parameter (it is the same for all players)
                gc.setVassalagaeCondition( iCordoba, iArabia, 1, con.iProvinceDesired )
                gc.setVassalagaeCondition( iArabia, iCordoba, 1, con.iProvinceDesired )
                
                # How much culture should we get into a province of this type, ignoe the war and settler values (0,0)
                gc.setProvinceTypeParams( con.iProvinceNone, 0, 0, 2, 3 ) # 2/3 culture 
                gc.setProvinceTypeParams( con.iProvinceDesired, 0, 0, 1, 2 ) # this is not used
                gc.setProvinceTypeParams( con.iProvinceOuter, 0, 0, 1, 1 ) # no change to culture 
                gc.setProvinceTypeParams( con.iProvincePotential, 0, 0, 1, 1 ) # same as outer culture 
                gc.setProvinceTypeParams( con.iProvinceNatural, 0, 0, 2, 1 ) # double-culture 
                gc.setProvinceTypeParams( con.iProvinceCore, 0, 0, 2, 1 ) # double-culture 

		self.postAreas()
                
        def setTechTimeline( self ):
                gc.setTimelineTechModifiers( 9, 25, -50, 1, 100, 50 ) # go between 10 times slower and 4 times faster
                # formula is: iAhistoric = iCurrentTurn - iHistoricTurn, capped at ( iTPCap, iTBCap )
                # iCost *= 100 + topPenalty * iHistoric * iAhistoric / BotPenalty, iCost /= 100
                # iCost *= 100 - topBuff * iHistoric * iAhistoric / BotBuff, iCost /= 100
                # gc.setTimelineTechDateForTech( iTech, iTurn )
                gc.setTimelineTechDateForTech( xml.iCalendar, 0 )
                gc.setTimelineTechDateForTech( xml.iArchitecture, 30 )
                gc.setTimelineTechDateForTech( xml.iBronzeCasting, 15 )
                gc.setTimelineTechDateForTech( xml.iTheology, 10 )
                gc.setTimelineTechDateForTech( xml.iManorialism, 5 )
                gc.setTimelineTechDateForTech( xml.iStirrup, xml.i600AD )
                gc.setTimelineTechDateForTech( xml.iEngineering, 55 ) #teir 2
                gc.setTimelineTechDateForTech( xml.iChainMail, 43 )
                gc.setTimelineTechDateForTech( xml.iArt, 38 )
                gc.setTimelineTechDateForTech( xml.iMonasticism, 50 )
                gc.setTimelineTechDateForTech( xml.iVassalage, 60 )
                gc.setTimelineTechDateForTech( xml.iAstrolabe, 76 ) # teir 3
                gc.setTimelineTechDateForTech( xml.iMachinery, 76 )
                gc.setTimelineTechDateForTech( xml.iVaultedArches, 90 ) # 
                gc.setTimelineTechDateForTech( xml.iMusic, 80 )
                gc.setTimelineTechDateForTech( xml.iHerbalMedicine, 95 )
                gc.setTimelineTechDateForTech( xml.iFeudalism, xml.i778AD ) # Feudalism
                gc.setTimelineTechDateForTech( xml.iFarriers, 100 )
                gc.setTimelineTechDateForTech( xml.iMapMaking, 145 )  # this is tier 5
                gc.setTimelineTechDateForTech( xml.iBlastFurnace, 120 )# teir 4
                gc.setTimelineTechDateForTech( xml.iSiegeEngines, xml.i1097AD ) #trebuchets
                gc.setTimelineTechDateForTech( xml.iGothicArchitecture, 130 ) # 12th century
                gc.setTimelineTechDateForTech( xml.iLiterature, 145 )
                gc.setTimelineTechDateForTech( xml.iCodeOfLaws, 120 )
                gc.setTimelineTechDateForTech( xml.iAristocracy, 135 )
                gc.setTimelineTechDateForTech( xml.iLateenSails, 125 ) # actually this is tier 4
                gc.setTimelineTechDateForTech( xml.iPlateArmor, 152 ) # teir 5: Late 1200s, By the 14th century, plate armour was commonly used to supplement mail.
                gc.setTimelineTechDateForTech( xml.iMonumentBuilding, 180 )
                gc.setTimelineTechDateForTech( xml.iClassicalKnowledge, 175 )
                gc.setTimelineTechDateForTech( xml.iAlchemy, xml.i1003AD )
                gc.setTimelineTechDateForTech( xml.iCivilService, 190 ) # teir 6
                gc.setTimelineTechDateForTech( xml.iClockmaking, 200 )
                gc.setTimelineTechDateForTech( xml.iPhilosophy, 215 )
                gc.setTimelineTechDateForTech( xml.iEducation, 220 )
                gc.setTimelineTechDateForTech( xml.iGuilds, 200 )
                gc.setTimelineTechDateForTech( xml.iChivalry, 210 )
                gc.setTimelineTechDateForTech( xml.iOptics, 228 ) # teir 7
                gc.setTimelineTechDateForTech( xml.iReplaceableParts, 250 )
                gc.setTimelineTechDateForTech( xml.iPatronage, 230 )
                gc.setTimelineTechDateForTech( xml.iGunpowder, xml.i1300AD )
                gc.setTimelineTechDateForTech( xml.iBanking, 240 )
                gc.setTimelineTechDateForTech( xml.iMilitaryTradition, 260 )
                gc.setTimelineTechDateForTech( xml.iShipbuilding, 275 ) # teir 8
                gc.setTimelineTechDateForTech( xml.iDrama, 270 )
                gc.setTimelineTechDateForTech( xml.iDivineRight, 266 )
                gc.setTimelineTechDateForTech( xml.iChemistry, 280 )
                gc.setTimelineTechDateForTech( xml.iPaper, 290 )
                gc.setTimelineTechDateForTech( xml.iProfessionalArmy, 295 )
                gc.setTimelineTechDateForTech( xml.iPrintingPress, xml.i1517AD ) # teir 9 turn 304
                gc.setTimelineTechDateForTech( xml.iPublicWorks, 310 )
                gc.setTimelineTechDateForTech( xml.iMatchlock, xml.i1500AD )
                gc.setTimelineTechDateForTech( xml.iArabicKnowledge, xml.i1491AD ) # fall of Granada
                gc.setTimelineTechDateForTech( xml.iAstronomy, xml.i1514AD ) # teir 10 Copernicus
                gc.setTimelineTechDateForTech( xml.iSteamEngines, xml.i1690AD ) # first steam engine
                gc.setTimelineTechDateForTech( xml.iConstitution, 375 )
                gc.setTimelineTechDateForTech( xml.iPolygonalFort, 370 )
                gc.setTimelineTechDateForTech( xml.iArabicMedicine, 342 )
                gc.setTimelineTechDateForTech( xml.iRenaissanceArt, xml.i1540AD ) # teir 11, 1541
                gc.setTimelineTechDateForTech( xml.iNationalism, 380 )
                gc.setTimelineTechDateForTech( xml.iLiberalism, 400 )
                gc.setTimelineTechDateForTech( xml.iScientificMethod, xml.i1623AD ) # Galileo 
                gc.setTimelineTechDateForTech( xml.iMilitaryTactics, 410 )
                gc.setTimelineTechDateForTech( xml.iNavalArchitecture, 385 ) # teir 12
                gc.setTimelineTechDateForTech( xml.iCivilEngineering, 395 )
                gc.setTimelineTechDateForTech( xml.iRightOfMan, 460 )
                gc.setTimelineTechDateForTech( xml.iEconomics, 435 )
                gc.setTimelineTechDateForTech( xml.iPhysics, xml.i1687AD )
                gc.setTimelineTechDateForTech( xml.iBiology, 440 )
                gc.setTimelineTechDateForTech( xml.iCombinedArms, 430 )
                gc.setTimelineTechDateForTech( xml.iTradingCompanies, xml.i1600AD ) # teir 13 TradingCompanies turn 325
                gc.setTimelineTechDateForTech( xml.iMachineTools, 450 )
                gc.setTimelineTechDateForTech( xml.iFreeMarket, 450 )
                gc.setTimelineTechDateForTech( xml.iExplosives, 460 )
                gc.setTimelineTechDateForTech( xml.iMedicine, 458 )
                gc.setTimelineTechDateForTech( xml.iIndustrialTech, xml.i1800AD )
                
                # block foundation of Protestantism except by a Catholic player
                gc.setParentSchismReligions( xml.iCatholicism, xml.iProtestantism )
                

	def preMapsNSizes( self ):
		# settlersMaps, DO NOT CHANGE THIS CODE
                gc.setSizeNPlayers( con.iMapMaxX, con.iMapMaxY, iNumPlayers, iNumTotalPlayers, xml.iNumTechs, xml.iNumBuildingsPlague, xml.iNumReligions )
                for i in range( iNumPlayers ):
                        for y in range( con.iMapMaxY ):
                                for x in range( con.iMapMaxX ):
                                        gc.setSettlersMap( i, y, x, rfcemaps.tSettlersMaps[i][y][x] )
                                        gc.setWarsMap( i, y, x, rfcemaps.tWarsMaps[i][y][x] )
	
                for y in range( con.iMapMaxY ):
                        for x in range( con.iMapMaxX ):
                                if ( rfcemaps.tProinceMap[y][x] > -1 ): 
                                        # "no province" of ocean is settled different than -1, set only non-negative values, 
                                        # the C++ map is initialized to "no-province" by setSizeNPlayers(...)
                                        # "no-province" is returned as -1 via the Cy interface
                                        gc.setProvince( x, y, rfcemaps.tProinceMap[y][x] )
                gc.createProvinceCrossreferenceList() # make sure to call this AFTER setting all the Province entries
                
                gc.setProvinceTypeNumber( con.iNumProvinceTypes ) # set the Number of Provinces, call this before you set any AI or culture modifiers
        
                # birth turns for the players, do not change this loop
                for i in range( iNumTotalPlayers ):
                        gc.setStartingTurn( i, con.tBirth[i] )	
			
	def postAreas( self ):
		#3Miro: DO NOT CHANGE THIS CODE
		# this adds the Core and Notmal Areas from Consts.py into C++. There is Dynamical Memory involved, so don't change this
		for iCiv in range( iNumPlayers ):
			iCBLx = con.tCoreAreasTL[iCiv][0]
			iCBLy = con.tCoreAreasTL[iCiv][1]
			iCTRx = con.tCoreAreasBR[iCiv][0]
			iCTRy = con.tCoreAreasBR[iCiv][1]
			iNBLx = con.tNormalAreasTL[iCiv][0]
			iNBLy = con.tNormalAreasTL[iCiv][1]
			iNTRx = con.tNormalAreasBR[iCiv][0]
			iNTRy = con.tNormalAreasBR[iCiv][1]
			iCCE = len( con.tExceptions[iCiv] )
			iCNE = len( con.tNormalAreasSubtract[iCiv] )
			gc.setCoreNormal( iCiv, iCBLx, iCBLy, iCTRx, iCTRy, iNBLx, iNBLy, iNTRx, iNTRy, iCCE, iCNE )
			for iEx in range( iCCE ):
				gc.addCoreException( iCiv, con.tExceptions[iCiv][iEx][0], con.tExceptions[iCiv][iEx][1] )
			for iEx in range( iCNE ):
				gc.addNormalException( iCiv, con.tNormalAreasSubtract[iCiv][iEx][0], con.tNormalAreasSubtract[iCiv][iEx][1] )
				
		gc.setProsecutorReligions( xml.iProsecutor, xml.iProsecutorClass )
		gc.setSaintParameters( xml.iProphet, con.iSaintBenefit, 20, 40 ) # try to amass at least 20 and don't bother above 40 points
		gc.setIndependnets( con.iIndepStart, con.iIndepEnd, con.iBarbarian )
		gc.setPapalPlayer( iPope, xml.iCatholicism )

		gc.setAutorunHack( xml.iCatapult, 32, 0 ) # Autorun hack, sync with RNF module
                
                #3MiroMercs: set the merc promotion
                gc.setMercPromotion( xml.iPromotionMerc )
		
		
		for iCiv in range( iNumPlayers ):
			#print( "  sw: ",iCiv )
			gc.setStartingWorkers( iCiv, con.tStartingWorkers[iCiv] )
		
