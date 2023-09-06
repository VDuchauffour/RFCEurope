# Rhye's and Fall of Civilization: Europe - Event handler

from CvPythonExtensions import *
import CvUtil
import CvEventManager #Mercenaries
import sys #Mercenaries
import PyHelpers
import CvMainInterface #Mercenaries
import CvMercenaryManager #Mercenaries
import CvScreenEnums #Mercenaries
import Popup

from StoredData import sd #edead
import RiseAndFall
import Barbs
import Religions
import Resources
import CityNameManager
import UniquePowers
import AIWars
import Consts as con
import XMLConsts as xml
import RFCUtils
utils = RFCUtils.RFCUtils()
import CvScreenEnums #Mercenaries
import Victory
import Stability
import Plague
import Crusades
import Companies
import DataLoader
import ProvinceManager
import Mercenaries
import RFCEMaps as rfcemaps

gc = CyGlobalContext()
localText = CyTranslator() #Absinthe
#iBetrayalCheaters = 15

#Civ constants
iByzantium = con.iByzantium
iFrankia = con.iFrankia
iArabia = con.iArabia
iBulgaria = con.iBulgaria
iCordoba = con.iCordoba
iVenecia = con.iVenecia
iBurgundy = con.iBurgundy
iGermany = con.iGermany
iNovgorod = con.iNovgorod
iNorway = con.iNorway
iKiev = con.iKiev
iHungary = con.iHungary
iSpain = con.iSpain
iDenmark = con.iDenmark
iScotland = con.iScotland
iPoland = con.iPoland
iGenoa = con.iGenoa
iMorocco = con.iMorocco
iEngland = con.iEngland
iPortugal = con.iPortugal
iAragon = con.iAragon
iSweden = con.iSweden
iPrussia = con.iPrussia
iLithuania = con.iLithuania
iAustria = con.iAustria
iTurkey = con.iTurkey
iMoscow = con.iMoscow
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

# Absinthe: Turn Randomization constants
iLighthouseEarthQuake = 0
iByzantiumVikingAttack = 1

# Absinthe: all of this Mercenary stuff is unused
#Mercenaries - start

PyPlayer = PyHelpers.PyPlayer
PyGame = PyHelpers.PyGame()
PyInfo = PyHelpers.PyInfo

# Set g_bGameTurnMercenaryCreation to True if mercenary creation should happen during the
# onBeginGameTurn method, False if it should happen during the onBeginPlayerTurn method
# Default value is True
g_bGameTurnMercenaryCreation = True

# Set g_bDisplayMercenaryManagerOnBeginPlayerTurn to True if the "Mercenary Manager"
# screen should be displayed at the beginning of every player turn.
# Default value is False
g_bDisplayMercenaryManagerOnBeginPlayerTurn = False

# This value also controls the "Mercenary Manager" button and when it should be displayed.
# Default value is "ERA_ANCIENT"
#Rhye - start (was causing an assert)
#g_iStartingEra = gc.getInfoTypeForString("ERA_ANCIENT")
g_iStartingEra = 0
#Rhye - end

# Change this to False if mercenaries should be removed from the global mercenary pool
# at the beginning of the game turn. When set to True a number of mercenaries will
# wander away from the global mercenary pool. This is another variable used to control
# the load time for the "Mercenary Manager" screen.
# Default valus is True
g_bWanderlustMercenaries = True

# Change this to increase the max number of mercenaries that may wander away from the
# global mercenary pool.
# Default valus is 3
g_iWanderlustMercenariesMaximum = 7 #Rhye

# Default valus is 0
g_iWanderlustMercenariesMinimum = 2 #Rhye

# Change this to False to supress the mercenary messages.
# Default value is True
g_bDisplayMercenaryMessages = False #Rhye

# Set to True to print out debug messages in the logs
g_bDebug = True

# Default valus is 1
g_bUpdatePeriod = 5 #Rhye

# Default valus is 1
g_bAIThinkPeriod = 6 #Rhye (5 in Warlords, 4 in vanilla)

# globals

#Mercenaries - end


###################################################
class CvRFCEventHandler:

	mercenaryManager = None #Mercenaries

	def __init__(self, eventManager):

		self.lastProvinceID = -1
		self.bStabilityOverlay = False
		self.EventKeyDown = 6
		self.EventKeyUp = 7
		self.eventManager = eventManager

		# initialize base class
		eventManager.addEventHandler("GameStart", self.onGameStart) #Stability
		eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn) #Stability
		eventManager.addEventHandler("cityAcquired", self.onCityAcquired) #Stability
		eventManager.addEventHandler("cityAcquiredAndKept", self.onCityAcquiredAndKept) #Stability
		eventManager.addEventHandler("cityRazed", self.onCityRazed) #Stability
		eventManager.addEventHandler("cityBuilt", self.onCityBuilt) #Stability
		eventManager.addEventHandler("combatResult", self.onCombatResult) #Stability
		#eventManager.addEventHandler("changeWar", self.onChangeWar)
		eventManager.addEventHandler("religionFounded",self.onReligionFounded) #Victory
		eventManager.addEventHandler("buildingBuilt",self.onBuildingBuilt) #Victory
		eventManager.addEventHandler("projectBuilt",self.onProjectBuilt) #Victory
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn) #Mercenaries
		#eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn) #Stability
		eventManager.addEventHandler("kbdEvent",self.onKbdEvent) #Mercenaries and Stability overlay
		eventManager.addEventHandler("unitLost",self.onUnitLost) #Mercenaries
		eventManager.addEventHandler("unitKilled",self.onUnitKilled) #Mercenaries
		eventManager.addEventHandler("OnPreSave",self.onPreSave) #edead: StoredData
		eventManager.addEventHandler("OnLoad",self.onLoadGame) #Mercenaries, StoredData
		eventManager.addEventHandler("unitPromoted",self.onUnitPromoted) #Mercenaries
		eventManager.addEventHandler("techAcquired",self.onTechAcquired) #Mercenaries #Stability
		#eventManager.addEventHandler("improvementDestroyed",self.onImprovementDestroyed) #Stability
		eventManager.addEventHandler("unitPillage",self.onUnitPillage) #Stability
		eventManager.addEventHandler("religionSpread",self.onReligionSpread) #Stability
		eventManager.addEventHandler("firstContact",self.onFirstContact)
		eventManager.addEventHandler("playerChangeAllCivics", self.onPlayerChangeAllCivics) # Absinthe: Python Event for civic changes
		eventManager.addEventHandler("playerChangeSingleCivic", self.onPlayerChangeSingleCivic) # Absinthe: Python Event for civic changes
		eventManager.addEventHandler("playerChangeStateReligion", self.onPlayerChangeStateReligion)

		self.eventManager = eventManager

		self.rnf = RiseAndFall.RiseAndFall()
		self.barb = Barbs.Barbs()
		self.rel = Religions.Religions()
		self.res = Resources.Resources()
		self.cnm = CityNameManager.CityNameManager()
		self.up = UniquePowers.UniquePowers()
		self.aiw = AIWars.AIWars()
		self.vic = Victory.Victory()
		self.sta = Stability.Stability()
		self.pla = Plague.Plague()
		self.crusade = Crusades.Crusades()
		self.province = ProvinceManager.ProvinceManager()
		self.mercs = Mercenaries.MercenaryManager() # 3MiroMercs
		self.company = Companies.Companies() # Absinthe


		#Mercenaries - start

		self.mercenaryManager = CvMercenaryManager.CvMercenaryManager(CvScreenEnums.MERCENARY_MANAGER)

		global g_bGameTurnMercenaryCreation
		global g_bDisplayMercenaryManagerOnBeginPlayerTurn
		global g_iStartingEra
		global g_bWanderlustMercenaries
		global g_iWanderlustMercenariesMaximum
		global g_bDisplayMercenaryMessages

		#Rhye - start comment
##		# Load the Mercenaries Mod Config INI file containing all of the configuration information
##		config = CvConfigParser.CvConfigParser("Mercenaries Mod Config.ini")
##
##		# If we actually were able to open the "Mercenaries Mod Config.ini" file then read in the values.
##		# otherwise we'll keep the default values that were set at the top of this file.
##		if(config != None):
##			g_bGameTurnMercenaryCreation = config.getboolean("Mercenaries Mod", "Game Turn Mercenary Creation", True)
##			g_bDisplayMercenaryManagerOnBeginPlayerTurn = config.getboolean("Mercenaries Mod", "Display Mercenary Manager On Begin Player Turn", False)
##			g_iStartingEra = gc.getInfoTypeForString(config.get("Mercenaries Mod","Starting Era","ERA_ANCIENT"))
##			g_bWanderlustMercenaries = config.getboolean("Mercenaries Mod", "Wanderlust Mercenaries", True)
##			g_iWanderlustMercenariesMaximum = config.getint("Mercenaries Mod","Wanderlust Mercenaries Maximum", 5)
##			g_bDisplayMercenaryMessages = config.getboolean("Mercenaries Mod", "Display Mercenary Messages", True)
		#Rhye - end comment


	def onGameStart(self, argsList):
		'Called at the start of the game'
		#self.pm.setup()
		DataLoader.setup()
		sd.setup() # initialise global script data
		self.rnf.setup()
		self.rel.setup()
		self.pla.setup()
		self.sta.setup()
		self.aiw.setup()
		self.company.setup() # Absinthe: initial company setup for the 1200AD scenario

		# 3Miro: WarOnSpawn
		self.rnf.setWarOnSpawn()
		self.vic.setup()

		# Absinthe: generate and store randomized turn modifiers
		sd.scriptDict['lEventRandomness'][iLighthouseEarthQuake] = gc.getGame().getSorenRandNum(40, 'Final Earthquake')
		sd.scriptDict['lEventRandomness'][iByzantiumVikingAttack] = gc.getGame().getSorenRandNum(10, 'Viking Attack')

		# Absinthe: rename cities on the 1200AD scenario - the WB file cannot handle special chars and long names properly
		#			some of the cities intentionally have different names though (compared to the CNM), for example some Kievan cities
		#			thus it's only set for Hungary for now, we can add more civs/cities later on if there are naming issues
		if utils.getScenario() == con.i1200ADScenario:
			for city in utils.getCityList(con.iHungary):
				self.cnm.renameCities(city, con.iHungary)
		# Absinthe: for all civs:
		#if utils.getScenario() == con.i1200ADScenario:
		#	for iPlayer in range(con.iNumPlayers - 1):
		#		for city in utils.getCityList(iPlayer):
		#			self.cnm.renameCities(city, iPlayer)

		# Absinthe: refresh Dynamic Civ Names for all civs on the initial turn of the given scenario
		for iPlayer in range(con.iNumMajorPlayers):
			gc.getPlayer(iPlayer).processCivNames()

		return 0


	def onCityAcquired(self, argsList):
		'City Acquired'
		owner, playerType, city, bConquest, bTrade = argsList
		#CvUtil.pyPrint('City Acquired Event: %s' %(city.getName()))

		self.rnf.onCityAcquired(owner,playerType,city,bConquest,bTrade)
		self.cnm.renameCities(city, playerType)

		tCity = (city.getX(), city.getY())

		# Absinthe: If Arabia doesn't found it's first city, but acquires it with a different method (conquest, flip, trade), it should found Islam there (otherwise no holy city at all)
		if playerType == iArabia and not gc.getGame().isReligionFounded(xml.iIslam):
			# has to be done before the Arab UP is triggered
			gc.getPlayer(iArabia).foundReligion(xml.iIslam, xml.iIslam, False)
			gc.getGame().getHolyCity(xml.iIslam).setNumRealBuilding(xml.iIslamicShrine, 1)

		# 3Miro: Arab UP
		if gc.hasUP( playerType, con.iUP_Faith ):
			self.up.faithUP( playerType, city )

		# Absinthe: Ottoman UP
		if gc.hasUP( playerType, con.iUP_Janissary ):
			self.up.janissaryNewCityUP( playerType, city, bConquest )

		# Absinthe: Scottish UP
		#			against all players (including indies and barbs), but only on conquest
		if owner == iScotland and bConquest: # playerType < con.iNumTotalPlayersB
			# only in cities with at least 20% Scottish culture
			iTotalCulture = city.countTotalCultureTimes100()
			if iTotalCulture == 0 or (city.getCulture(owner) * 10000) / iTotalCulture > 20:
				self.up.defianceUP( owner )

		# Absinthe: Aragonese UP
		#			UP tile yields should be recalculated right away, in case the capital was conquered, or province number changed
		if owner == iAragon:
			self.up.confederationUP( owner )
		if playerType == iAragon:
			self.up.confederationUP( playerType )

		# Absinthe: If Protestantism has not been founded by the time the Dutch spawn, then the Dutch should found it with their first city
		if playerType == iDutch and not gc.getGame().isReligionFounded(xml.iProtestantism):
			gc.getPlayer(iDutch).foundReligion(xml.iProtestantism, xml.iProtestantism, False)
			gc.getGame().getHolyCity(xml.iProtestantism).setNumRealBuilding(xml.iProtestantShrine, 1)
			self.rel.setReformationActive(True)
			self.rel.reformationchoice(iDutch)
			self.rel.reformationOther(iIndependent)
			self.rel.reformationOther(iIndependent2)
			self.rel.reformationOther(iIndependent3)
			self.rel.reformationOther(iIndependent4)
			self.rel.reformationOther(iBarbarian)
			self.rel.setReformationHitMatrix(iDutch, 2)
			for iCiv in range(iNumPlayers):
				if iCiv in Religions.lReformationNeighbours[iDutch] and self.rel.getReformationHitMatrix(iCiv) == 0:
					self.rel.setReformationHitMatrix(iCiv, 1)

		# Absinthe: Spread some culture to the newly acquired city - this is for nearby indy cities, so should be applied in all cases (conquest, flip, trade)
		if ( playerType < iNumMajorPlayers ):
			utils.spreadMajorCulture( playerType, city.getX(), city.getY() )

		self.sta.onCityAcquired( owner, playerType, city, bConquest, bTrade )

		# 3Miro: Jerusalem's Golden Age Incentive
		if tCity == con.tJerusalem:
			pPlayer = gc.getPlayer( playerType )
			if pPlayer.getStateReligion() == xml.iCatholicism:
				# Absinthe: interface message for the player
				if pPlayer.isHuman():
					CityName = city.getNameKey()
					CyInterface().addMessage(utils.getHumanID(), True, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_JERUSALEM_SAFE", (CityName, )), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
				# Absinthe: spread Catholicism if not present already
				if not city.isHasReligion( xml.iCatholicism ):
					self.rel.spreadReligion( tCity, xml.iCatholicism )
				self.crusade.success( playerType )

			# Absinthe: acquiring Jerusalem, with any faith (but not Paganism) -> chance to find a relic
			#			maybe only after a specific date? maybe only if there isn't any ongoing Crusades?
			if gc.getGame().getSorenRandNum(100, 'Relic found') < 15:
				# for major players only
				if ( playerType < iNumMajorPlayers ):
					if pPlayer.getStateReligion() in range(xml.iNumReligions):
						pPlayer.initUnit( xml.iHolyRelic, con.tJerusalem[0], con.tJerusalem[1], UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH )

		# Sedna17: code for Krak des Chevaliers
		if bConquest:
			iNewOwner = city.getOwner()
			pNewOwner = gc.getPlayer(iNewOwner)
			if pNewOwner.countNumBuildings(xml.iKrakDesChevaliers) > 0:
				city.setHasRealBuilding(utils.getUniqueBuilding(iNewOwner, xml.iWalls), True)
				# Absinthe: if the Castle building were built with the Krak, then it should add stability
				#			the safety checks are probably unnecessary, as Castle buildings are destroyed on conquest (theoretically)
				if not (city.isHasBuilding(xml.iSpanishCitadel) or city.isHasBuilding(xml.iMoscowKremlin) or city.isHasBuilding(xml.iHungarianStronghold) or city.isHasBuilding(xml.iCastle)):
					city.setHasRealBuilding(utils.getUniqueBuilding(iNewOwner, xml.iCastle), True)
					pNewOwner.changeStabilityBase( con.iCathegoryExpansion, 1 )
		# Sedna17, end

		# 3Miro: National wonders and city acquire by trade
		#if (bTrade):
		#	for i in range (con.iScotlandYard +1 - con.iHeroicEpic):
		#		iNationalWonder = i + con.iHeroicEpic
		#		if (city.hasBuilding(iNationalWonder)):
		#			city.setHasRealBuilding((iNationalWonder), False)

		self.pla.onCityAcquired(owner, playerType, city) #Plague
		self.vic.onCityAcquired(owner, playerType, city, bConquest, bTrade) #Victory
		self.company.onCityAcquired(owner, playerType, city)

		# Remove Silk resource near Constantinople if it is conquered
		if tCity == (81, 24):
			self.res.removeResource(80, 24)

		# Remove horse resource near Hadrianople in 1200 AD scenario if someone captures Hadrianople or Constantinople
		if utils.getScenario() == con.i1200ADScenario:
			if tCity == (76, 25) or tCity == (81, 24):
				self.res.removeResource(77, 24)

		return 0


	def onCityAcquiredAndKept(self, argsList):
		'City Acquired and Kept'
		iOwner, pCity = argsList

		self.mercs.onCityAcquiredAndKept(iOwner, pCity)


	def onCityRazed(self, argsList):
		'City Razed'
		city, iPlayer = argsList

		iPreviousOwner = city.getOwner()
		if iPreviousOwner == iPlayer and city.getPreviousOwner() != -1:
			iPreviousOwner = city.getPreviousOwner()

		self.rnf.onCityRazed(iPreviousOwner,iPlayer,city) # Rise and Fall
		self.sta.onCityRazed(iPreviousOwner,iPlayer,city) # Stability
		self.company.onCityRazed(iPreviousOwner,iPlayer,city)
		self.vic.onCityRazed(iPlayer,city) # Victory
		self.pla.onCityRazed(city,iPlayer) # Plague

		# Absinthe: Aragonese UP
		#			UP tile yields should be recalculated if your new city is razed
		if iPlayer == iAragon:
			self.up.confederationUP( iPlayer )


	def onCityBuilt(self, argsList):
		'City Built'
		city = argsList[0]

		iOwner = city.getOwner()

		self.rnf.onCityBuilt( iOwner, city )
		tCity = (city.getX(), city.getY())

		if iOwner < con.iNumActivePlayers:
			self.cnm.assignName(city)

		# Absinthe: merc notifications, after the city is named
		self.mercs.onCityBuilt(iOwner, city)

		# Absinthe: Aragonese UP
		#			UP tile yields should be recalculated on city foundation
		if iOwner == iAragon:
			self.up.confederationUP( iOwner )

		# Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
		pCurrent = gc.getMap().plot( city.getX(), city.getY() )
		for i in range(con.iNumTotalPlayers - con.iNumActivePlayers):
			iMinorCiv = i + con.iNumActivePlayers
			pCurrent.setCulture(iMinorCiv, 0, True)
		pCurrent.setCulture(con.iBarbarian, 0, True)

		if iOwner < iNumMajorPlayers:
			utils.spreadMajorCulture(iOwner, city.getX(), city.getY())

			if iOwner == iPortugal:
				self.vic.onCityBuilt(city, iOwner) # needed in Victory.py

				if gc.getTeam( gc.getPlayer( iPortugal ).getTeam() ).isHasTech( xml.iAstronomy ):
					city.setHasRealBuilding( xml.iPortugalFeitoria, True )

		# Absinthe: Free buildings if city is built on a tile improvement
		#			The problem is that the improvement is auto-destroyed before the city is founded, and totally separately from this function, thus a workaround is needed
		#			Solution: getting the coordinates of the last destroyed improvement from a different file in a global variable
		#			If the last destroyed improvement in the game is a fort, and it was in the same place as the city, then it's good enough for me
		#			(only problem might be if currently there is no improvement on the city-founding tile, but the last destroyed improvement in the game
		#				was a fort on the exact same plot some turns ago - but IMO that's not much of a stress of reality, there was a fort there after all)
		#			Note that CvEventManager.iImpBeforeCity needs to have some initial value if a city is founded before the first destroyed improvement
		#				adding an improvement in the scenario map to one of the preplaced Byzantine cities won't work perfectly:
		#				while the improvement will be autorazed on the beginning of the 1st players turn when starting in 500AD, does nothing if you load a saved game
		iImpBeforeCityType = (CvEventManager.iImpBeforeCity / 10000) % 100
		iImpBeforeCityX = (CvEventManager.iImpBeforeCity / 100) % 100
		iImpBeforeCityY = CvEventManager.iImpBeforeCity % 100
		#print ("new city coordinates: ", city.getX(), city.getY())
		#print ("destroyed improvement values: ", CvEventManager.iImpBeforeCity, iImpBeforeCityType, iImpBeforeCityX, iImpBeforeCityY)
		# Absinthe: free walls if built on fort
		if iImpBeforeCityType == xml.iImprovementFort and (iImpBeforeCityX, iImpBeforeCityY) == tCity:
			city.setHasRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWalls), True)
		# Absinthe: free granary if built on hamlet
		if iImpBeforeCityType == xml.iImprovementHamlet and (iImpBeforeCityX, iImpBeforeCityY) == tCity:
			city.setHasRealBuilding(utils.getUniqueBuilding(iOwner, xml.iGranary), True)
		# Absinthe: free granary and +1 population if built on village or town
		if iImpBeforeCityType in [xml.iImprovementTown, xml.iImprovementVillage]:
			if (iImpBeforeCityX, iImpBeforeCityY) == tCity:
				city.changePopulation(1)
				city.setHasRealBuilding(utils.getUniqueBuilding(iOwner, xml.iGranary), True)

		# Absinthe: Some initial food for all cities on foundation
		#			So Leon and Roskilde for example don't lose a population in the first couple turns
		#			Nor the indy cities on spawn (they start with zero-sized culture, so they shrink without some food reserves)
		#			Currently 1/5 of the treshold of the next population growth
		city.setFood( city.growthThreshold() / 5 )

		# 3MiroUP: spread religion on city foundation
		if gc.hasUP( iOwner, con.iUP_Faith ):
			self.up.faithUP( iOwner, city )

		# Absinthe: If Protestantism has not been founded by the time the Dutch spawn, then the Dutch should found it with their first city
		if iOwner == iDutch and not gc.getGame().isReligionFounded(xml.iProtestantism):
			gc.getPlayer(iDutch).foundReligion(xml.iProtestantism, xml.iProtestantism, False)
			gc.getGame().getHolyCity(xml.iProtestantism).setNumRealBuilding(xml.iProtestantShrine, 1)
			self.rel.setReformationActive(True)
			self.rel.reformationchoice(iDutch)
			self.rel.reformationOther(iIndependent)
			self.rel.reformationOther(iIndependent2)
			self.rel.reformationOther(iIndependent3)
			self.rel.reformationOther(iIndependent4)
			self.rel.reformationOther(iBarbarian)
			self.rel.setReformationHitMatrix(iDutch, 2)
			for iCiv in range(iNumPlayers):
				if iCiv in Religions.lReformationNeighbours[iDutch] and self.rel.getReformationHitMatrix(iCiv) == 0:
					self.rel.setReformationHitMatrix(iCiv, 1)

		if iOwner < con.iNumPlayers:
			self.sta.onCityBuilt( iOwner, city.getX(), city.getY() )


	def onCombatResult(self, argsList):
		self.vic.onCombatResult(argsList)
		self.sta.onCombatResult(argsList)


	def onReligionFounded(self, argsList):
		'Religion Founded'
		iReligion, iFounder = argsList

		if iReligion != xml.iJudaism:
			for city in utils.getCityList(iFounder):
				if city.isHolyCityByType( iReligion ): # Sedna: Protestant Shrine is now starting point for consistency with Religion.xml, Judaism is special
					if iReligion == xml.iProtestantism:
						iTemple = xml.iProtestantTemple
						iShrine = xml.iProtestantShrine
					elif iReligion == xml.iIslam:
						iTemple = xml.iIslamicTemple
						iShrine = xml.iIslamicShrine
					elif iReligion == xml.iCatholicism:
						iTemple = xml.iCatholicTemple
						iShrine = xml.iCatholicShrine
					elif iReligion == xml.iOrthodoxy:
						iTemple = xml.iOrthodoxTemple
						iShrine = xml.iOrthodoxShrine
					if not city.isHasRealBuilding(iShrine):
						city.setHasRealBuilding(iShrine, True )
					if not city.isHasRealBuilding(iTemple):
						city.setHasRealBuilding(iTemple, True )
					break

		self.vic.onReligionFounded(iReligion, iFounder)

		if iFounder < con.iNumPlayers:
			self.sta.onReligionFounded(iFounder)

		# 3Miro: end Crusades for the Holy Land after the Reformation
		if iReligion == xml.iProtestantism:
			self.crusade.endCrusades()


	def onBuildingBuilt(self, argsList):
		city, iBuildingType = argsList
		iOwner = city.getOwner()

		self.vic.onBuildingBuilt(iOwner, iBuildingType)
		if city.getOwner() < con.iNumPlayers:
			self.sta.onBuildingBuilt(iOwner, iBuildingType)
			self.company.onBuildingBuilt(iOwner, iBuildingType)
		# Absinthe: Faith, Kazimierz, Mont Saint-Michel
		self.rel.onBuildingBuilt( iOwner, iBuildingType )

		# Absinthe: Aragonese UP
		# UP tile yields should be recalculated right away if a new Palace was built
		if iOwner == con.iAragon and iBuildingType == xml.iPalace:
			self.up.confederationUP(iOwner)


	def onProjectBuilt(self, argsList):
		city, iProjectType = argsList
		self.vic.onProjectBuilt(city.getOwner(), iProjectType)
		if city.getOwner() < con.iNumPlayers:
			self.sta.onProjectBuilt(city.getOwner(), iProjectType)


	def onUnitPillage(self, argsList):
		print ("Improvement Destroyed")
		pUnit, iImprovement, iRoute, iOwner = argsList
		iPlotX = pUnit.getX()
		iPlotY = pUnit.getY()
		pPlot = CyMap().plot(iPlotX, iPlotY)
		if pPlot.countTotalCulture() == 0:
			print ("No culture, so barb/indy satisfied")
			if iImprovement >= xml.iImprovementCottage and iImprovement <= xml.iImprovementTown:
				print ("Improve Type Satisfied")
				self.barb.onImprovementDestroyed(iPlotX,iPlotY)
		iVictim = pPlot.getOwner()
		if iVictim > -1 and iVictim < con.iNumPlayers:
			self.sta.onImprovementDestroyed( iVictim )

		self.vic.onPillageImprovement( pUnit.getOwner(), iVictim, iImprovement, iRoute, iPlotX, iPlotY )


	def onBeginGameTurn(self, argsList):
		iGameTurn = argsList[0]

		# Absinthe tests
		#if iGameTurn == xml.i508AD:
		#	for city in utils.getCityList(con.iFrankia):
		#		plot = gc.getMap().plot(city.getX(),city.getY())
		#		print ('provincetest', plot.getProvinceID (), city.getName())

		#	unitList = PyPlayer(con.iFrankia).getUnitList()
		#	for unit in unitList:
		#		iCargoSpace = unit.cargoSpace()
		#		print ("iCargoSpace", iCargoSpace)

		#	for iCiv in range(con.iNumPlayers):
		#		pCiv = gc.getPlayer(iCiv)
		#		leaderName = pCiv.getLeader()
		#		leaderName2 = gc.getLeaderHeadInfo( pCiv.getLeaderType() )
		#		leaderName3 = leaderName2.getDescription()
		#		leaderName4 = leaderName2.getLeaderHead()
		#	#	leaderName5 = (pCiv.getLeaderType()).getLeaderID()
		#	#	leaderName6 = leaderName2.getLeaderType()
		#		leaderName7 = pCiv.getLeaderType()
		#		LeaderType = gc.getLeaderHeadInfo(pCiv.getLeaderType()).getType()
		#		print ("leaderName7", leaderName7)
		#		print ("LeaderType", LeaderType)

		#for city in utils.getCityList(con.iHungary):
		#	city.setBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_GRANARY"), CommerceTypes.COMMERCE_GOLD, 2)
		#	city.setBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_CASTLE"), CommerceTypes.COMMERCE_GOLD, 12)
		#	city.setBuildingYieldChange(gc.getInfoTypeForString("BUILDINGCLASS_GRANARY"), YieldTypes.YIELD_COMMERCE, 4)
		#	city.setBuildingYieldChange(gc.getInfoTypeForString("BUILDINGCLASS_GRANARY"), YieldTypes.YIELD_FOOD, 2)
		#	city.setBuildingYieldChange(gc.getInfoTypeForString("BUILDINGCLASS_CASTLE"), YieldTypes.YIELD_FOOD, 3)

		#	for x in range(76):
		#		plot = CyMap().plot(x, 46) # France, Paris included
		#		print ("cityname at y height", x, plot.getCityNameMap(1))
		#	for x in range(76):
		#		plot = CyMap().plot(x, 36) # Hungary, accents
		#		print ("cityname at y height", x, plot.getCityNameMap(11))

		# Absinthe: 868AD Viking attack on Constantinople
		if iGameTurn == xml.i860AD + sd.scriptDict['lEventRandomness'][iByzantiumVikingAttack] - 2:
			if utils.getHumanID() == con.iByzantium:
				popup = Popup.PyPopup()
				popup.setBodyString(localText.getText("TXT_KEY_EVENT_VIKING_CONQUERERS_RUMOURS", ()))
				popup.launch()

		if iGameTurn == xml.i860AD + sd.scriptDict['lEventRandomness'][iByzantiumVikingAttack]:
			if utils.getHumanID() == con.iByzantium:
				self.barb.spawnMultiTypeUnits(iBarbarian, (80, 24), (80, 25), [xml.iVikingBerserker, xml.iDenmarkHuskarl], [4, 3], iGameTurn, 1, 0, utils.forcedInvasion, 1, localText.getText("TXT_KEY_BARBARIAN_NAMES_VIKINGS", ()))
				CyInterface().addMessage(iByzantium, False, con.iDuration, CyTranslator().getText("TXT_KEY_EVENT_VIKING_CONQUERERS_ARRIVE", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)

		# Absinthe: Message for the human player about the Schism
		elif iGameTurn == xml.i1053AD:
			iHuman = utils.getHumanID()
			if utils.isActive(iHuman):
				sText = CyTranslator().getText("TXT_KEY_GREAT_SCHISM", ())
				CyInterface().addMessage(iHuman, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iDarkPink), -1, -1, True, True)

		# Absinthe: Remove the Great Lighthouse, message for the human player if the city is visible
		elif iGameTurn == xml.i1323AD - 40 + sd.scriptDict['lEventRandomness'][iLighthouseEarthQuake]:
			for iPlayer in range(con.iNumTotalPlayers):
				bFound = 0
				for city in utils.getCityList(iPlayer):
					if city.isHasBuilding(xml.iGreatLighthouse):
						city.setHasRealBuilding(xml.iGreatLighthouse, False)
						GLcity = city
						bFound = 1
				if bFound and utils.getHumanID() == iPlayer:
					pPlayer = gc.getPlayer(iPlayer)
					iTeam = pPlayer.getTeam()
					if GLcity.isRevealed(iTeam, False):
						CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_BUILDING_GREAT_LIGHTHOUSE_REMOVED", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)

		#print(" 3Miro: Byz Rank is: ",gc.getGame().getTeamRank(iByzantium))

		print(" 3Miro onBegTurn: ",iGameTurn)
		self.barb.checkTurn(iGameTurn)
		self.rnf.checkTurn(iGameTurn)
		self.rel.checkTurn(iGameTurn)
		self.res.checkTurn(iGameTurn)
		self.up.checkTurn(iGameTurn)
		self.aiw.checkTurn(iGameTurn)
		self.pla.checkTurn(iGameTurn)
		self.vic.checkTurn(iGameTurn)
		self.sta.checkTurn(iGameTurn)
		self.crusade.checkTurn(iGameTurn)
		self.province.checkTurn(iGameTurn)
		self.company.checkTurn(iGameTurn)

		#print(" 3Miro onBegTurn out: ",iGameTurn)

		return 0


	def onBeginPlayerTurn(self, argsList):
		iGameTurn, iPlayer = argsList
		iHuman = utils.getHumanID()

		print ("onBeginPlayerTurn PLAYER", iPlayer)

		if self.rnf.getDeleteMode(0) != -1:
			self.rnf.deleteMode(iPlayer)

		# Absinthe: refresh Dynamic Civ Names
		if iPlayer < con.iNumMajorPlayers:
			gc.getPlayer(iPlayer).processCivNames()

		## Absinthe: refresh Dynamic Civ Names for all civs on the human player's initial turn of the given scenario
		##			it's probably enough to refresh it on onGameStart for the scenario
		#if utils.getHumanID() == iPlayer:
		#	if iGameTurn == utils.getScenarioStartTurn():
		#		for iDCNPlayer in range(con.iNumMajorPlayers):
		#			gc.getPlayer(iDCNPlayer).processCivNames()

		# Absinthe: Byzantine conqueror army
		if iGameTurn == xml.i520AD:
			if iPlayer == con.iByzantium:
				pByzantium = gc.getPlayer(iByzantium)
				tStartingPlot = (59,16)
				pByzantium.initUnit(xml.iGalley, tStartingPlot[0], tStartingPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pByzantium.initUnit(xml.iGalley, tStartingPlot[0], tStartingPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pByzantium.initUnit(xml.iGalley, tStartingPlot[0], tStartingPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pByzantium.initUnit(xml.iGalley, tStartingPlot[0], tStartingPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pByzantium.initUnit(xml.iGalley, tStartingPlot[0], tStartingPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pByzantium.initUnit(xml.iGreatGeneral, tStartingPlot[0], tStartingPlot[1], UnitAITypes.UNITAI_GENERAL, DirectionTypes.DIRECTION_SOUTH)
				pPlot = CyMap().plot(tStartingPlot[0], tStartingPlot[1])
				for iUnitLoop in range(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(iUnitLoop)
					if (pUnit.getUnitType() == CvUtil.findInfoTypeNum(gc.getUnitInfo,gc.getNumUnitInfos(),'UNIT_GREAT_GENERAL')):
						pUnit.setName(localText.getText("TXT_KEY_GREAT_PERSON_BELISARIUS", ()))
				utils.makeUnit(xml.iSwordsman, con.iByzantium, tStartingPlot, 4)
				utils.makeUnit(xml.iAxeman, con.iByzantium, tStartingPlot, 3)
				utils.makeUnit(xml.iArcher, con.iByzantium, tStartingPlot, 2)
				if iPlayer == iHuman:
					popup = Popup.PyPopup()
					popup.setBodyString(localText.getText("TXT_KEY_EVENT_CONQUEROR_BELISARIUS", ()))
					popup.launch()

		# Absinthe: popup message a couple turns before the Seljuk/Mongol/Timurid invasions
		if iPlayer == iHuman:
			# Seljuks
			if iGameTurn == xml.i1064AD - 7:
				if iPlayer == con.iByzantium:
					popup = Popup.PyPopup()
					popup.setBodyString(localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_START", ()))
					popup.launch()
			elif iGameTurn == xml.i1094AD + 1:
				if iPlayer == con.iByzantium:
					popup = Popup.PyPopup()
					sText = "Seljuk"
					popup.setBodyString(localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_END", (sText,)))
					popup.launch()
			# Mongols
			elif iGameTurn == xml.i1236AD - 7:
				if iPlayer in [con.iKiev, con.iHungary, con.iPoland, con.iBulgaria]:
					popup = Popup.PyPopup()
					popup.setBodyString(localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_START", ()))
					popup.launch()
			elif iGameTurn == xml.i1288AD + 1:
				if iPlayer in [con.iKiev, con.iHungary, con.iPoland, con.iBulgaria]:
					popup = Popup.PyPopup()
					sText = "Tatar"
					popup.setBodyString(localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_END", (sText,)))
					popup.launch()
			# Timurids
			elif iGameTurn == xml.i1380AD - 7:
				if iPlayer in [con.iArabia, con.iTurkey, con.iByzantium]:
					popup = Popup.PyPopup()
					popup.setBodyString(localText.getText("TXT_KEY_EVENT_TIMURID_INVASION_START", ()))
					popup.launch()
			elif iGameTurn == xml.i1431AD + 1:
				if iPlayer in [con.iArabia, con.iTurkey, con.iByzantium]:
					popup = Popup.PyPopup()
					sText = "Timurid"
					popup.setBodyString(localText.getText("TXT_KEY_EVENT_BARBARIAN_INVASION_END", (sText,)))
					popup.launch()

		# Absinthe: Denmark UP
		if iPlayer == con.iDenmark:
			self.up.soundUP(iPlayer)

		# Absinthe: Aragonese UP
		# safety check: probably redundant, calls from onBuildingBuilt, onCityBuilt, onCityAcquired and onCityRazed should be enough
		elif iPlayer == con.iAragon:
			self.up.confederationUP(iPlayer)

		# Ottoman UP
		if gc.hasUP( iPlayer, con.iUP_Janissary ):
			self.up.janissaryDraftUP( iPlayer )

		self.pla.checkPlayerTurn(iGameTurn, iPlayer)
		self.vic.checkPlayerTurn(iGameTurn, iPlayer)

		if gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers:
			if gc.getPlayer(iPlayer).getNumCities() > 0:
				self.sta.updateBaseStability(iGameTurn, iPlayer)

			# for the AI only, leader switch and cheats
			if iPlayer != iHuman:
				self.rnf.checkPlayerTurn(iGameTurn, iPlayer)

			# not really needed, we set it on collapse anyway
			# utils.setLastTurnAlive( iPlayer, iGameTurn )

		self.crusade.checkPlayerTurn(iGameTurn, iPlayer)

		##print ("PLAYER FINE", iPlayer)
		##print( " out Begin Player Turn ",iGameTurn, iPlayer )


	def onEndPlayerTurn(self, argsList):
		# 3Miro does not get called
		iGameTurn, iPlayer = argsList
		#print (" 3Miro END PLAYER", iPlayer, iGameTurn)

		'Called at the end of a players turn'


	def onEndGameTurn(self, argsList):
		# 3Miro when everyone end their turn
		iGameTurn = argsList[0]
		print (" 3Miro END TURN ", iGameTurn)
		self.sta.checkImplosion(iGameTurn)
		# 3MiroMercs
		self.mercs.doMercsTurn(iGameTurn)


	def onReligionSpread(self, argsList):

		iReligion, iOwner, pSpreadCity = argsList
		self.sta.onReligionSpread(iReligion, iOwner)
		self.rel.onReligionSpread(iReligion, iOwner)


	def onFirstContact(self, argsList):

		iTeamX,iHasMetTeamY = argsList
		self.rnf.onFirstContact(iTeamX, iHasMetTeamY)


	# Absinthe: Python Event for civic changes
	def onPlayerChangeAllCivics(self, argsList):
		# note that this only reports civic change if it happened via normal revolution
		'Player changes his civics'
		iPlayer = argsList[0]
		lNewCivics = [argsList[1], argsList[2], argsList[3], argsList[4], argsList[5], argsList[6]]
		lOldCivics = [argsList[7], argsList[8], argsList[9], argsList[10], argsList[11], argsList[12]]
		if iPlayer < con.iNumPlayers:
			print ("ChangeAllCivics civic change, player:", iPlayer)
			print ("ChangeAllCivics civic change, new civics:", lNewCivics)
			print ("ChangeAllCivics civic change, old civics:", lOldCivics)
			self.rel.onPlayerChangeAllCivics(iPlayer, lNewCivics, lOldCivics)


	def onPlayerChangeSingleCivic(self, argsList):
		# note that this reports all civic changes in single instances (so also reports force converts by diplomacy or with spies)
		'Civics are changed for a player'
		iPlayer, iNewCivic, iOldCivic = argsList
		if iPlayer < con.iNumPlayers:
			print ("ChangeSingleCivic civic change, Player, NewCivic, OldCivic:", argsList)
	# Absinthe: end


	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList

		if iPlayer < iNumPlayers:
			self.company.onPlayerChangeStateReligion(argsList)


	def onTechAcquired(self, argsList):

		#print ("onTechAcquired", argsList)
		iPlayer = argsList[2]

		iHuman = utils.getHumanID()

		self.vic.onTechAcquired(argsList[0], argsList[2])
		#self.res.onTechAcquired(argsList[0], argsList[2])

		if gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > con.tBirth[iPlayer] and iPlayer < con.iNumPlayers:
			self.rel.onTechAcquired(argsList[0], argsList[2])
			self.sta.onTechAcquired(argsList[0], argsList[2])

	def onPreSave(self, argsList):
		'called before a game is actually saved'
		sd.save() # edead: pickle & save script data

	# This method creates a new instance of the MercenaryUtils class to be used later
	def onLoadGame(self, argsList):
		sd.load() # edead: load & unpickle script data
		DataLoader.setup() # Absinthe: also needed on loading saved games
		#pass

		#if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
		#if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):

			#global objMercenaryUtils

			#objMercenaryUtils = MercenaryUtils.MercenaryUtils()


	# This method will redraw the main interface once a unit is promoted. This way the
	# gold/turn information will be updated.
	def onUnitPromoted(self, argsList):
		'Unit Promoted'

		self.mercs.onUnitPromoted( argsList )

		#if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
		#if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):
		#	pUnit, iPromotion = argsList
		#	player = PyPlayer(pUnit.getOwner())
		#
		#	if (objMercenaryUtils.isMercenary(pUnit)):
		#		CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)


	# This method will remove a mercenary unit from the game if it is killed
	def onUnitKilled(self, argsList):
		'Unit Killed'

		self.mercs.onUnitKilled( argsList )

		#if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
		#if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):

			#unit, iAttacker = argsList

			#mercenary = objMercenaryUtils.getMercenary(unit.getNameNoDesc())

			#if(mercenary != None and g_bDisplayMercenaryMessages and mercenary.getBuilder() != -1 and unit.isDead()):
				#strMessage = mercenary.getName() + " has died under " + gc.getPlayer(mercenary.getOwner()).getName() + "'s service."
				## Inform the player that the mercenary has died.
				#CyInterface().addMessage(mercenary.getBuilder(), True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True)

			#objMercenaryUtils.removePlayerMercenary(unit)


	# This method will remove a mercenary unit from the game if it is lost
	def onUnitLost(self, argsList):
		'Unit Lost'

		#print(" 3Miro: onUnitLost ")
		self.mercs.onUnitLost( argsList )


	# This method handles the key input and will bring up the mercenary manager screen if the
	# player has at least one city and presses 'ctrl' and the 'M' key.
	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'

		iHuman = utils.getHumanID()
		if (gc.getGame().getGameTurn() >= con.tBirth[iHuman]):

			eventType,key,mx,my,px,py = argsList

			theKey=int(key)

			if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_M) and self.eventManager.bCtrl and gc.getActivePlayer().getNumCities() > 0):

				self.mercenaryManager.interfaceScreen()

		#Rhye - start debug
		eventType, key, mx, my, px, py = argsList

		theKey=int(key)

		if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_B) and self.eventManager.bAlt):

			iGameTurn = gc.getGame().getGameTurn()
			pass


		if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_N) and self.eventManager.bAlt):

			print("ALT-N")

			#self.printEmbassyDebug()
			self.printPlotsDebug()
			#self.printStabilityDebug()


		if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_E) and self.eventManager.bAlt and self.eventManager.bShift):
			print("SHIFT-ALT-E") #picks a dead civ so that autoplay can be started with game.AIplay xx
			iDebugDeadCiv = iBurgundy #always dead in 500AD
			# 3Miro: not sure
			#gc.getTeam(gc.getPlayer(iDebugDeadCiv).getTeam()).setHasTech(con.iCalendar, True, iDebugDeadCiv, False, False)
			utils.makeUnit(xml.iAxeman, iDebugDeadCiv, (0,0), 1)
			gc.getGame().setActivePlayer(iDebugDeadCiv, False)
			gc.getPlayer(iDebugDeadCiv).setPlayable(True)
		#Rhye - end debug


		# Absinthe: province highlight - based on SoI
		if eventType == self.EventKeyDown and px >= 0 and py >= 0 and int(key) == 45 and self.eventManager.bCtrl and not self.eventManager.bAlt:

			plot = gc.getMap().plot(px,py)
			iActivePlayer = gc.getGame().getActivePlayer()
			iActiveTeam = gc.getPlayer(iActivePlayer).getTeam()
			iProvinceID = rfcemaps.tProvinceMap[plot.getY()][plot.getX()]

			# do not show provinces of unrevealed tiles
			if not plot.isRevealed(iActiveTeam, False) and not gc.getGame().isDebugMode():
				return

			# do not redraw if already drawn
			if self.lastProvinceID == iProvinceID:
				return

			map = CyMap()
			engine = CyEngine()

			# clear the highlight
			engine.clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)
			#engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS)

			# cache the plot's coords
			self.lastProvinceID = rfcemaps.tProvinceMap[plot.getY()][plot.getX()]

			# select an appropriate color
			if rfcemaps.tProvinceMap[plot.getY()][plot.getX()] == -1: # ocean and non-province tiles
				return
			else:
				iLevel = utils.getProvinceStabilityLevel(iHuman, iProvinceID)
				if iLevel == 4:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_CORE")).getColor()
				elif iLevel == 3:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_NATURAL")).getColor()
				elif iLevel == 2:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_POTENTIAL")).getColor()
				elif iLevel == 1:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_BORDER")).getColor()
				else:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_FOREIGN")).getColor()

			# apply the highlight
			for i in range(map.numPlots()):
				plot = map.plotByIndex(i)
				if rfcemaps.tProvinceMap[plot.getY()][plot.getX()] == iProvinceID and (gc.getGame().isDebugMode() or plot.isRevealed(iActiveTeam, False)):
					engine.fillAreaBorderPlot(plot.getX(), plot.getY(), color, AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)

			return

		# clear all highlights
		if (eventType == self.EventKeyUp and self.eventManager.bCtrl) or (eventType == self.EventKeyDown):
			CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)
			self.lastProvinceID = -1
		# Absinthe: end

	def printDebug(self, iGameTurn):
		pass

	def printPlotsDebug(self):
		pass

	def printEmbassyDebug(self):
		pass

	def printStabilityDebug(self):
		print ("Stability")
		for iCiv in range(con.iNumPlayers):
			if (gc.getPlayer(iCiv).isAlive()):
				print ("Base:", utils.getBaseStabilityLastTurn(iCiv), "Modifier:", utils.getStability(iCiv)-utils.getBaseStabilityLastTurn(iCiv), "Total:", utils.getStability(iCiv), "civic", gc.getPlayer(iCiv).getCivics(5), gc.getPlayer(iCiv).getCivilizationDescription(0))
				for i in range(con.iNumStabilityParameters):
					print("Parameter", i, utils.getStabilityParameters(iCiv,i))
			else:
				print ("dead", iCiv)
		for i in range(con.iNumPlayers):
			print (gc.getPlayer(i).getCivilizationShortDescription(0), "PLOT OWNERSHIP ABROAD:", self.sta.getOwnedPlotsLastTurn(i), "CITY OWNERSHIP LOST:", self.sta.getOwnedCitiesLastTurn(i) )

