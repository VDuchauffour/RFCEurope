# RFC Europe, balancing modifiers are placed here
from CvPythonExtensions import *
import Consts as con
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
		
		# 3Miro: consolidate several modifiers into fewer calls, makes it more structured. Each modfier works as described below.
		
		#void setGrowthModifiers( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop );
		# iInitPop is the initial population in a city, also can use gc.setInitialPopulation( iCiv, iInitPop ) to change a single civ
		# defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiers(iBurgundy,     100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiers(iByzantium,    300, 100, 150, 150, 100, 2 )
		gc.setGrowthModifiers(iFrankia,      100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiers(iArabia,       150, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiers(iBulgaria,     100, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiers(iCordoba,      150, 100, 100, 100, 100, 1 )
		gc.setGrowthModifiers(iSpain,        100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiers(iNorse,        100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiers(iVenecia,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiers(iKiev,         100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiers(iHungary,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiers(iGermany,      100, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiers(iPoland,       150, 100, 100, 100, 100, 2 )
		gc.setGrowthModifiers(iMoscow,       100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiers(iGenoa,        100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiers(iEngland,      100, 100, 100, 100, 100, 3 )
		gc.setGrowthModifiers(iPortugal,     100,  75, 100, 100, 100, 3 )
		gc.setGrowthModifiers(iAustria,      100,  75, 100, 100, 100, 3 )
		gc.setGrowthModifiers(iTurkey,       100,  75, 100, 100, 100, 3 )
		gc.setGrowthModifiers(iSweden,       100,  75, 100, 100, 100, 4 )
		gc.setGrowthModifiers(iDutch,        100,  50, 100, 100, 100, 4 )
		gc.setGrowthModifiers(iPope,         150, 200, 100,  50, 100, 1 )
		gc.setGrowthModifiers(iIndependent,  100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiers(iIndependent2, 100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiers(iIndependent3, 100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiers(iIndependent4, 100, 100, 100,  50, 100, 1 )
		gc.setGrowthModifiers(iBarbarian,    100, 100, 100,  50, 100, 1 )

		
		#void setProductionModifiers( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
		# defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100 )
		# 3Miro: at 100 research cost, the cost is exactly as in the XML files, the cost in general is however increased for all civs
		gc.setProductionModifiers(iBurgundy,  100, 100, 100, 150 )
		gc.setProductionModifiers(iByzantium, 200, 200, 200, 300 )
		gc.setProductionModifiers(iFrankia,   100, 100, 100, 120 )
		gc.setProductionModifiers(iArabia,    150, 150, 100, 150 )
		gc.setProductionModifiers(iBulgaria,  100, 100, 100, 120 )
		gc.setProductionModifiers(iCordoba,   150, 200, 100, 150 )
		gc.setProductionModifiers(iSpain,     100, 100, 100, 120 )
		gc.setProductionModifiers(iNorse,     100, 100, 100, 120 )
		gc.setProductionModifiers(iVenecia,   100, 100, 100, 120 )
		gc.setProductionModifiers(iKiev,      100, 100, 100, 120 )
		gc.setProductionModifiers(iHungary,   100, 100, 100, 120 )
		gc.setProductionModifiers(iGermany,   100, 100, 100, 120 )
		gc.setProductionModifiers(iPoland,    100, 150, 120, 150 )
		gc.setProductionModifiers(iMoscow,     75,  75, 100, 150 )
		gc.setProductionModifiers(iGenoa,     100, 100, 100, 125 )
		gc.setProductionModifiers(iEngland,   100, 100, 100, 100 )
		gc.setProductionModifiers(iPortugal,  100, 100, 100, 110 )
		gc.setProductionModifiers(iAustria,    75,  75, 100,  75 )
		gc.setProductionModifiers(iTurkey,     50,  75, 100, 100 )
		gc.setProductionModifiers(iSweden,     50,  50, 100, 100 )
		gc.setProductionModifiers(iDutch,      75,  50, 100,  75 )
		gc.setProductionModifiers(iPope,      300, 200, 100, 150 )
		gc.setProductionModifiers(iIndependent, 100, 100, 500, 250 )
		gc.setProductionModifiers(iIndependent2, 100, 100, 500, 250 )
		gc.setProductionModifiers(iIndependent3, 100, 100, 500, 250 )
		gc.setProductionModifiers(iIndependent4, 100, 100, 500, 250 )
		gc.setProductionModifiers(iBarbarian, 100, 100, 1000, 350 )

		#void setSupportModifiers( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
		# defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100 )
		gc.setSupportModifiers(iBurgundy,      10, 150,  80,  75, 110 )
		gc.setSupportModifiers(iByzantium,     10, 150,  10,  10, 120 )
		gc.setSupportModifiers(iFrankia,       10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iArabia,        10, 150,  50,  15, 120 )
		gc.setSupportModifiers(iBulgaria,      10, 150,  50,  25, 110 )
		gc.setSupportModifiers(iCordoba,       20, 150,  50,  50, 120 )
		gc.setSupportModifiers(iSpain,         10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iNorse,         10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iVenecia,       10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iKiev,          10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iHungary,       10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iGermany,       10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iPoland,        10, 100,  75,  40, 100 )
		gc.setSupportModifiers(iMoscow,        10, 100,  50,  25, 100 ) # sync with UP
		gc.setSupportModifiers(iGenoa,         10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iEngland,       10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iPortugal,      10, 100,  50,  25, 100 )
		gc.setSupportModifiers(iAustria,       10,  75,  50,  25, 100 )
		gc.setSupportModifiers(iTurkey,        10,  25,  10,  10, 100 )
		gc.setSupportModifiers(iSweden,        10,  75,  50,  10, 100 )
		gc.setSupportModifiers(iDutch,         10, 150,  50,  75, 100 )
		gc.setSupportModifiers(iPope,          10, 200,  50,  25, 100 )
		gc.setSupportModifiers(iIndependent,   10, 100,  10,  20, 100 )
		gc.setSupportModifiers(iIndependent2,  10, 100,  10,  20, 100 )
		gc.setSupportModifiers(iIndependent3,  10, 100,  10,  20, 100 )
		gc.setSupportModifiers(iIndependent4,  10, 100,  10,  20, 100 )
		gc.setSupportModifiers(iBarbarian,     10, 250,  10, 100, 100 )
		
	
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
		#gc.setInitialBuilding( iSpain, con.iHerbalist, True )
		#gc.setInitialBuilding( iSpain, con.iBarracks, True )

		gc.setInitialBuilding( iMoscow, con.iGranary, True )
		gc.setInitialBuilding( iMoscow, con.iHerbalist, True )
		gc.setInitialBuilding( iMoscow, con.iBarracks, True )
		gc.setInitialBuilding( iMoscow, con.iForge, True )
		gc.setInitialBuilding( iMoscow, con.iMarket, True )
		
		gc.setInitialBuilding( iGenoa, con.iGranary, True )
		gc.setInitialBuilding( iGenoa, con.iHerbalist, True )
		gc.setInitialBuilding( iGenoa, con.iBarracks, True )
		
		gc.setInitialBuilding( iEngland, con.iGranary, True )
		gc.setInitialBuilding( iEngland, con.iHerbalist, True )
		gc.setInitialBuilding( iEngland, con.iBarracks, True )
		
		gc.setInitialBuilding( iPortugal, con.iGranary, True )
		gc.setInitialBuilding( iPortugal, con.iHerbalist, True )
		gc.setInitialBuilding( iPortugal, con.iBarracks, True )

		gc.setInitialBuilding( iAustria, con.iGranary, True )
		gc.setInitialBuilding( iAustria, con.iHerbalist, True )
		gc.setInitialBuilding( iAustria, con.iBarracks, True )
		
		gc.setInitialBuilding( iTurkey, con.iGranary, True )
		gc.setInitialBuilding( iTurkey, con.iHerbalist, True )
		gc.setInitialBuilding( iTurkey, con.iBarracks, True )
		gc.setInitialBuilding( iTurkey, con.iForge, True )
		gc.setInitialBuilding( iTurkey, con.iHarbor, True )
		gc.setInitialBuilding( iTurkey, con.iOttomanHammam, True )
		
		gc.setInitialBuilding( iSweden, con.iGranary, True )
		gc.setInitialBuilding( iSweden, con.iHerbalist, True )
		gc.setInitialBuilding( iSweden, con.iBarracks, True )
		gc.setInitialBuilding( iSweden, con.iForge, True )
		gc.setInitialBuilding( iSweden, con.iHarbor, True )
		gc.setInitialBuilding( iSweden, con.iAqueduct, True )

		gc.setInitialBuilding( iDutch, con.iGranary, True )
		gc.setInitialBuilding( iDutch, con.iHerbalist, True )
		gc.setInitialBuilding( iDutch, con.iBarracks, True )
		gc.setInitialBuilding( iDutch, con.iForge, True )
		gc.setInitialBuilding( iDutch, con.iHarbor, True )
		gc.setInitialBuilding( iDutch, con.iAqueduct, True )
		
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
		gc.setCityClusterAI( iArabia, 1, 3, 0 )
		gc.setCityClusterAI( iBulgaria, 1, 2, 1 )
		gc.setCityClusterAI( iCordoba, 1, 3, 1 )
		gc.setCityClusterAI( iSpain, 1, 3, 1 )
		gc.setCityClusterAI( iNorse, 1, 3, 1 )
		gc.setCityClusterAI( iVenecia, 1, 3, 1 )
		gc.setCityClusterAI( iKiev, 1, 4, 1 )
		gc.setCityClusterAI( iHungary, 1, 3, 1 )
		gc.setCityClusterAI( iGermany, 1, 3, 1 )
		gc.setCityClusterAI( iPoland, 1, 3, 0 )
		gc.setCityClusterAI( iMoscow, 1, 4, 1 )
		gc.setCityClusterAI( iGenoa, 1, 3, 1 )
		gc.setCityClusterAI( iEngland, 1, 3, 1 )
		gc.setCityClusterAI( iAustria, 2, 3, 1 )
		gc.setCityClusterAI( iTurkey, 1, 3, 1 )
		gc.setCityClusterAI( iSweden, 1, 2, 1 )		
		gc.setCityClusterAI( iDutch, 2, 3, 1 )

		#3Miro: setCityWarDistanceAI(iCiv,iVal), depending on the type of the empire, modify how likely the AI is to attack a city
		# values are 1 - small empires (Egypt,default), 2 - large contiguous empires (Rome,Arabia), 3 - global empire (England,Russia,Mongolia)
		gc.setCityWarDistanceAI( iBurgundy, 1 )
		gc.setCityWarDistanceAI( iByzantium, 2 )
		gc.setCityWarDistanceAI( iFrankia, 2 )
		gc.setCityWarDistanceAI( iArabia, 2 )
		gc.setCityWarDistanceAI( iBulgaria, 2 )
		gc.setCityWarDistanceAI( iCordoba, 1 )
		gc.setCityWarDistanceAI( iSpain, 2 )
		gc.setCityWarDistanceAI( iNorse, 3 )
		gc.setCityWarDistanceAI( iVenecia, 3 )
		gc.setCityWarDistanceAI( iKiev, 2 )
		gc.setCityWarDistanceAI( iHungary, 2 )
		gc.setCityWarDistanceAI( iGermany, 2 )
		gc.setCityWarDistanceAI( iPoland, 2 )
		gc.setCityWarDistanceAI( iMoscow, 2 )
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
		gc.setTechPreferenceAI(iBulgaria,con.iBronzeCasting,200)				
		gc.setTechPreferenceAI(iGermany,con.iPrintingPress,200)
		gc.setTechPreferenceAI(iEngland,con.iPrintingPress,150)

		
		#3Miro: setDiplomacyModifiers(iCiv1,iCiv2,iVal) hidden modifier for the two civ's AI relations. More likely to have OB and so on.
		# + means they will like each other - they will hate each other.
		# from Civ1 towards Civ2
		gc.setDiplomacyModifiers( iCordoba, iArabia, +8 )
		gc.setDiplomacyModifiers( iArabia, iCordoba, +8 )
		gc.setDiplomacyModifiers( iArabia, iByzantium, -10 )
		gc.setDiplomacyModifiers( iByzantium, iArabia, -10 )
		gc.setDiplomacyModifiers( iCordoba, iSpain, -20 )
		gc.setDiplomacyModifiers( iSpain, iCordoba, -20 )
		gc.setDiplomacyModifiers( iPortugal, iSpain, +8 )
		gc.setDiplomacyModifiers( iSpain, iPortugal, +8 )
		gc.setDiplomacyModifiers( iCordoba, iPortugal, -10 )
		gc.setDiplomacyModifiers( iPortugal, iCordoba, -10 )		
		gc.setDiplomacyModifiers( iFrankia, iBurgundy, +4 )
		gc.setDiplomacyModifiers( iBurgundy, iFrankia, +4 )
		gc.setDiplomacyModifiers( iTurkey, iByzantium, -10 )
		gc.setDiplomacyModifiers( iByzantium, iTurkey, -10 )
		gc.setDiplomacyModifiers( iGermany, iPoland, -5 )
		gc.setDiplomacyModifiers( iMoscow, iPoland, -5 )
		gc.setDiplomacyModifiers( iAustria, iPoland, -2 )
		gc.setDiplomacyModifiers( iSweden, iPoland, -2 )
		
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
		
		gc.setUP( iBurgundy, iUP_Happiness, 1 )
		gc.setUP( iBurgundy, iUP_PerCityCommerce, 200)
		
		gc.setUP( iByzantium, iUP_Emperor, 1 )
		
		gc.setUP( iFrankia, iUP_LandStability, 1 )
		gc.setUP( iFrankia, iUP_CulturalTolerance, 0 )
		
		gc.setUP( iArabia, iUP_Faith, 1 )
		
		gc.setUP( iBulgaria, iUP_NoResistance, 0 )
		
		gc.setUP( iCordoba, iUP_PromotionI, con.iPromotionMedicI )
		
		gc.setUP( iSpain, iUP_Inquisition, 1 )
		gc.setUP( iSpain, iUP_PerCityCommerce, 2 )
		
		gc.setUP( iNorse, iUP_CanEnterTerrain, con.iTerrainOcean )
		
		gc.setUP( iVenecia, iUP_EnableCivic, 100* con.iCivicMerchantRepublic + con.iCivicRepublic )
		#gc.setUP( iVenecia, iUP_ForeignSea, 1 )
		
		gc.setUP( iKiev, iUP_CityTileYield, 100000 * 2 )
		
		gc.setUP( iHungary, iUP_CulturalTolerance, 0 )
		gc.setUP( iHungary, iUP_ReligiousTolerance, 0 )
		
		gc.setUP( iGermany, iUP_UnitProduction, con.iGunpowder * 100 + 75 )
		
		gc.setUP( iPoland, iUP_Happiness, 1 )
		gc.setUP( iPoland, iUP_CommercePercent, 100000 )
		
		gc.setSupportModifiers(iMoscow, 10, 100, 25, 12, 100 )
		gc.setUP( iMoscow, iUP_EndlessLand, 50 )
		
		gc.setUP( iGenoa, iUP_Mercenaries, 1 )
		
		gc.setUP( iEngland, iUP_ImprovementBonus, con.iImprovementWorkshop * 1000000 + 200 )
		
		gc.setUP( iPortugal, iUP_Discovery, con.iNumNotColonies * 1000000 + (con.iNumTotalColonies-1) * 1000 + 60 );
		
		for i in range( iNumTotalPlayers ):
			if ( not i == iAustria ):
				gc.setDiplomacyModifiers( i, iAustria, +4 )
				
		gc.setUP( iTurkey, iUP_Conscription, 330 )
		
		gc.setUP( iSweden, iUP_PromotionI, con.iPromotionFormation )
		
		gc.setUP( iDutch, iUP_TradeRoutes, 2 )
		
		# GlobalWarming
		gc.setGlobalWarming( False )
		
		# Set FastTerrain (i.e. double movement over ocean)
		gc.setFastTerrain( con.iTerrainOcean )
		
		# set religious spread factors
		for iCiv in range( iNumTotalPlayers + 1 ): # include barbs
			for iRel in range( con.iNumReligions ):
				gc.setReligionSpread( iCiv, iRel, con.tReligionSpreadFactor[iCiv][iRel] )
				
		# set the religions and year of the great schism
		gc.setSchism( con.iCatholicism, con.iOrthodoxy, con.i1053AD )

		gc.setHoliestCity( con.iJerusalem[0], con.iJerusalem[1] )
		
		# 3Miro: Faith Points benefits
		# gc.setReligionBenefit( iReligion, iFP_(whatever it is), iParameter )
		# 	note that for powers iParameter = -1 means that this religion doesn't have this power (-1 is the default)
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
		
		gc.setReligionBenefit( con.iOrthodoxy, con.iFP_Stability, 20 )
		gc.setReligionBenefit( con.iOrthodoxy, con.iFP_Civic, 66 )
		
		gc.setReligionBenefit( con.iIslam, con.iFP_Growth, 50 )
		gc.setReligionBenefit( con.iIslam, con.iFP_Units, 50 )
		
		gc.setReligionBenefit( con.iProtestantism, con.iFP_Science, 50 )
		gc.setReligionBenefit( con.iProtestantism, con.iFP_Production, 50 )
		
		gc.setReligionBenefit( con.iCatholicism, con.iFP_Displomacy, 10 )
		gc.setReligionBenefit( con.iIslam, con.iFP_Displomacy, 10 )
		gc.setReligionBenefit( con.iProtestantism, con.iFP_Displomacy, 10 )

		# every nation gets a lan tile that is normally impassible and now pass through it
		gc.setStrategicTile( iVenecia, 56, 35 )
		
		
		self.postAreas()
		
	def preMapsNSizes( self ):
		# settlersMaps, DO NOT CHANGE THIS CODE
		gc.setSizeNPlayers( con.iMapMaxX, con.iMapMaxY, iNumPlayers, iNumTotalPlayers, con.iNumTechs, con.iNumBuildingsPlague, con.iNumReligions )
		for i in range( iNumPlayers ):
			for y in range( con.iMapMaxY ):
				for x in range( con.iMapMaxX ):
					gc.setSettlersMap( i, y, x, rfcemaps.tSettlersMaps[i][y][x] )
					gc.setWarsMap( i, y, x, rfcemaps.tWarsMaps[i][y][x] )
	
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
				
		gc.setProsecutorReligions( con.iProsecutor, con.iProsecutorClass )
		gc.setSaintParameters( con.iProphet, con.iSaintBenefit, 20, 40 ) # try to amass at least 20 and don't bother above 40 points
		gc.setIndependnets( con.iIndepStart, con.iIndepEnd, con.iBarbarian )
		gc.setPapalPlayer( iPope, con.iCatholicism )
		
		
		for iCiv in range( iNumPlayers ):
			#print( "  sw: ",iCiv )
			gc.setStartingWorkers( iCiv, con.tStartingWorkers[iCiv] )
		
