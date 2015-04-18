from CvPythonExtensions import *
import CvUtil
import CvEventManager #Mercenaries
import sys #Mercenaries
import PyHelpers
import CvMainInterface #Mercenaries
import CvMercenaryManager #Mercenaries
import CvScreenEnums  #Mercenaries
import Popup as PyPopup

import StoredData
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
import Mercenaries
import RFCEMaps as rfcemaps

gc = CyGlobalContext()
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
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers


#Mercenaries - start

PyPlayer = PyHelpers.PyPlayer
PyGame = PyHelpers.PyGame()
PyInfo = PyHelpers.PyInfo

# Set g_bGameTurnMercenaryCreation to true if mercenary creation should happen during the
# onBeginGameTurn method, false if it should happen during the onBeginPlayerTurn method
# Default value is true
g_bGameTurnMercenaryCreation = true

# Set g_bDisplayMercenaryManagerOnBeginPlayerTurn to true if the "Mercenary Manager"
# screen should be displayed at the beginning of every player turn.
# Default value is false
g_bDisplayMercenaryManagerOnBeginPlayerTurn = false

# This value also controls the "Mercenary Manager" button and when it should be displayed.
# Default value is "ERA_ANCIENT"
#Rhye - start (was causing an assert)
#g_iStartingEra = gc.getInfoTypeForString("ERA_ANCIENT")
g_iStartingEra = 0
#Rhye - end

# Change this to false if mercenaries should be removed from the global mercenary pool
# at the beginning of the game turn. When set to true a number of mercenaries will
# wander away from the global mercenary pool. This is another variable used to control
# the load time for the "Mercenary Manager" screen.
# Default valus is true
g_bWanderlustMercenaries = true

# Change this to increase the max number of mercenaries that may wander away from the
# global mercenary pool.
# Default valus is 3
g_iWanderlustMercenariesMaximum = 7 #Rhye

# Default valus is 0
g_iWanderlustMercenariesMinimum = 2 #Rhye

# Change this to false to supress the mercenary messages.
# Default value is true
g_bDisplayMercenaryMessages = false #Rhye

# Set to true to print out debug messages in the logs
g_bDebug = true

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
                eventManager.addEventHandler("OnLoad",self.onLoadGame) #Mercenaries
                eventManager.addEventHandler("unitPromoted",self.onUnitPromoted) #Mercenaries
                eventManager.addEventHandler("techAcquired",self.onTechAcquired) #Mercenaries, Rhye #Stability
                #eventManager.addEventHandler("improvementDestroyed",self.onImprovementDestroyed) #Stability
                eventManager.addEventHandler("unitPillage",self.onUnitPillage) #Stability
                eventManager.addEventHandler("religionSpread",self.onReligionSpread) #Stability
                eventManager.addEventHandler("firstContact",self.onFirstContact)
                eventManager.addEventHandler("corporationFounded",self.onCorporationFounded) #Stability

                self.eventManager = eventManager


                self.data = StoredData.StoredData()
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
                self.mercs = Mercenaries.MercenaryManager() # 3MiroMercs


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
##			g_bGameTurnMercenaryCreation = config.getboolean("Mercenaries Mod", "Game Turn Mercenary Creation", true)
##			g_bDisplayMercenaryManagerOnBeginPlayerTurn = config.getboolean("Mercenaries Mod", "Display Mercenary Manager On Begin Player Turn", false)
##			g_iStartingEra = gc.getInfoTypeForString(config.get("Mercenaries Mod","Starting Era","ERA_ANCIENT"))
##			g_bWanderlustMercenaries = config.getboolean("Mercenaries Mod", "Wanderlust Mercenaries", true)
##			g_iWanderlustMercenariesMaximum = config.getint("Mercenaries Mod","Wanderlust Mercenaries Maximum", 5)
##			g_bDisplayMercenaryMessages = config.getboolean("Mercenaries Mod", "Display Mercenary Messages", true)
		#Rhye - end comment

                #objMercenaryUtils = MercenaryUtils.MercenaryUtils()
                #Mercenaries - end


        def onGameStart(self, argsList):
                'Called at the start of the game'
                #self.pm.setup()
                self.data.setupScriptData()
                self.rnf.setup()
                self.rel.setup()
                self.pla.setup()
                self.sta.setup()
                self.aiw.setup()

                # 3Miro: WarOnSpawn
                self.rnf.setWarOnSpawn()

                #Mercenaries - start
                #global objMercenaryUtils
                #objMercenaryUtils = MercenaryUtils.MercenaryUtils()
                #Mercenaries - end

                return 0


	def onCityAcquired(self, argsList):
		#'City Acquired'
		owner,playerType,city,bConquest,bTrade = argsList
		#CvUtil.pyPrint('City Acquired Event: %s' %(city.getName()))

		self.rnf.onCityAcquired(owner,playerType,city,bConquest,bTrade)
		self.cnm.renameCities(city, playerType)

		# 3Miro: Arab UP
		if ( gc.hasUP( playerType, con.iUP_Faith ) ):
			self.up.faithUP( playerType, city )

		# Absinthe: Scottish UP
		if ( owner == iScotland and playerType < iNumPlayers):
			self.up.defianceUP( owner )

		# Absinthe: Spread some culture of the conqueror civ to the occupied city
		if (playerType < iNumMajorPlayers):
			utils.spreadMajorCulture(playerType, city.getX(), city.getY())

		self.sta.onCityAcquired(owner,playerType,city,bConquest,bTrade)

		# 3Miro: Jerusalem's Golden Age Incentive
		if ( city.getX() == con.iJerusalem[0] and city.getY() == con.iJerusalem[1] ):
			pPlayer = gc.getPlayer(playerType)
			if ( pPlayer.getStateReligion() == xml.iCatholicism ):
				self.crusade.success( playerType )

		# Sedna17: code for Krak des Chevaliers
		bKrak = false
		if (bConquest):
			iNewOwner = city.getOwner()
			lCities = PyPlayer( iNewOwner).getCityList( )
			for iCity in range(len(lCities)):
				pCity = gc.getPlayer( iNewOwner ).getCity( lCities[ iCity ].getID( ) )
				if(pCity.isHasRealBuilding(xml.iKrakDesChevaliers)):
					bKrak = true

		if bKrak:
			city.setHasRealBuilding(xml.iWalls, True)
			if iNewOwner == con.iSpain:
				city.setHasRealBuilding(xml.iSpanishCitadel, True)
			elif iNewOwner == con.iMoscow:
				city.setHasRealBuilding(xml.iMoscowKremlin, True)
			elif iNewOwner == con.iHungary:
				city.setHasRealBuilding(xml.iHungarianStronghold, True)
			else:
				city.setHasRealBuilding(xml.iCastle, True)
		# Sedna17, end

                # 3Miro: National wonders and city acquire by trade
                #if (bTrade):
                #        for i in range (con.iScotlandYard +1 - con.iHeroicEpic):
                #                iNationalWonder = i + con.iHeroicEpic
                #                if (city.hasBuilding(iNationalWonder)):
                #                        city.setHasRealBuilding((iNationalWonder), False)

                self.pla.onCityAcquired(owner,playerType,city) #Plague
                self.vic.onCityAcquired(owner, playerType, city, bConquest) #Victory

                return 0

        def onCityRazed(self, argsList):
                #'City Razed'
                city, iPlayer = argsList

                self.rnf.onCityRazed(city.getOwner(),iPlayer,city) # Rise and Fall
                self.sta.onCityRazed(city.getOwner(),iPlayer,city) # Stability
                self.vic.onCityRazed(iPlayer,city) # Victory
                self.pla.onCityRazed(city,iPlayer) # Plague


        def onCityBuilt(self, argsList):
                'City Built'
                city = argsList[0]

                iOwner = city.getOwner()

                self.rnf.onCityBuilt(iOwner, city )

                if (iOwner < con.iNumActivePlayers):
                        self.cnm.assignName(city)


                # Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
                pCurrent = gc.getMap().plot( city.getX(), city.getY() )
                for i in range(con.iNumTotalPlayers - con.iNumActivePlayers):
                        iMinorCiv = i + con.iNumActivePlayers
                        pCurrent.setCulture(iMinorCiv, 0, True)
                pCurrent.setCulture(con.iBarbarian, 0, True)

                if (iOwner < iNumMajorPlayers):
                        utils.spreadMajorCulture(iOwner, city.getX(), city.getY())

                if ( iOwner == iPortugal and gc.getTeam( gc.getPlayer( iPortugal ).getTeam() ).isHasTech( xml.iAstronomy ) ):
                        city.setHasRealBuilding( xml.iPortugalFeitoria, True )

                if ( iOwner == con.iPortugal ):
                	self.vic.onCityBuilt(city, iOwner) #Victory

		# 3MiroUP: faith on city found
		if ( gc.hasUP( iOwner, con.iUP_Faith ) ):
			self.up.faithUP( iOwner, city )

                if (iOwner < con.iNumPlayers):
                        self.sta.onCityBuilt(iOwner, city.getX(), city.getY() )

        def onCombatResult(self, argsList):
                #self.up.aztecUP(argsList)
                self.vic.onCombatResult(argsList)
                self.sta.onCombatResult(argsList)


	def onReligionFounded(self, argsList):
		'Religion Founded'
		iReligion, iFounder = argsList

		lCities = PyPlayer( iFounder ).getCityList( )
		for iCity in range( len( lCities ) ):
			pCity = gc.getPlayer( iFounder ).getCity( lCities[ iCity ].getID( ) )
			if ( pCity.isHolyCityByType( iReligion ) and iReligion <> xml.iJudaism): # Sedna: Protestant Shrine is now starting point for consistency with Religion.xml, Judaism is special
				if (iReligion == 0):
					iTemple = xml.iProtestantTemple
					iShrine = xml.iProtestantShrine
				if (iReligion == 1):
					iTemple = xml.iIslamicTemple
					iShrine = xml.iIslamicShrine
				if (iReligion == 2):
					iTemple = xml.iCatholicTemple
					iShrine = xml.iCatholicShrine
				if (iReligion == 3):
					iTemple = xml.iOrthodoxTemple
					iShrine = xml.iOrthodoxShrine
				if ( not pCity.isHasRealBuilding(iShrine) ):
					pCity.setHasRealBuilding(iShrine, True )
				if ( not pCity.isHasRealBuilding(iTemple) ):
					pCity.setHasRealBuilding(iTemple, True )

		self.vic.onReligionFounded(iReligion, iFounder)

		if (iFounder < con.iNumPlayers):
			self.sta.onReligionFounded(iFounder)

		# 3Miro: end Crusades for the Holy Land after the Reformation
		if (iReligion == xml.iProtestantism ):
			self.crusade.endCrusades()


	def onCorporationFounded(self, argsList):
		'Corporation Founded'
		iCorporation, iFounder = argsList
		#player = PyPlayer(iFounder)

		if (iFounder < con.iNumPlayers):
			self.sta.onCorporationFounded(iFounder)
			self.vic.onCorporationFounded(iFounder)


	def onBuildingBuilt(self, argsList):
		city, iBuildingType = argsList
		iOwner = city.getOwner()
		self.vic.onBuildingBuilt(city.getOwner(), iBuildingType)
		if (city.getOwner() < con.iNumPlayers):
			self.sta.onBuildingBuilt(iOwner, iBuildingType, city)
		# 3Miro: Faith
		self.rel.onBuildingBuild( iOwner, iBuildingType )


	def onProjectBuilt(self, argsList):
		city, iProjectType = argsList
		self.vic.onProjectBuilt(city.getOwner(), iProjectType)
		if (city.getOwner() < con.iNumPlayers):
			self.sta.onProjectBuilt(city.getOwner(), iProjectType)


	def onUnitPillage(self, argsList):
		print ("Improvement Destroyed")
		pUnit, iImprovement, iRoute, iOwner = argsList
		iPlotX = pUnit.getX()
		iPlotY = pUnit.getY()
		pPlot = CyMap().plot(iPlotX, iPlotY)
		if (pPlot.countTotalCulture() == 0 ):
			print("No culture, so bard/indy satisfied")
			if (iImprovement >= xml.iImprovementCottage and iImprovement <= xml.iImprovementTown):
				print ("Improve Type Satisfied")
				self.barb.onImprovementDestroyed(iPlotX,iPlotY)
		iVictim = pPlot.getOwner()
		if ( iVictim > -1 and iVictim < con.iNumPlayers ):
			self.sta.onImprovementDestroyed( iVictim )

		self.vic.onPillageImprovement( pUnit.getOwner(), iVictim, iImprovement, iRoute, iPlotX, iPlotY )


	def onBeginGameTurn(self, argsList):
		iGameTurn = argsList[0]

		if ( iGameTurn == xml.i1053AD ):
			iHuman = utils.getHumanID()
			sText = CyTranslator().getText("TXT_KEY_GREAT_SCHISM", ())
			CyInterface().addMessage(iHuman, True, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)

		print("3Miro: Byz Rank is: ",gc.getGame().getTeamRank(iByzantium))

		print(" 3Miro onBegTurn: ",iGameTurn)
		self.barb.checkTurn(iGameTurn)
		self.rnf.checkTurn(iGameTurn)
		self.rel.checkTurn(iGameTurn)
		self.res.checkTurn(iGameTurn)
		self.up.checkTurn(iGameTurn)
		self.aiw.checkTurn(iGameTurn)
		#self.cong.checkTurn(iGameTurn) # 3Miro: no congress
		self.pla.checkTurn(iGameTurn)
		self.vic.checkTurn(iGameTurn)
		self.sta.checkTurn(iGameTurn)
		#self.com.checkTurn(iGameTurn) # 3Miro: no communication problem
		self.crusade.checkTurn(iGameTurn)

                #Mercenaries - start

                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):
                #if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):

                        ## Get the list of active players in the game
                        #playerList = PyGame.getCivPlayerList()

                        ## Go through each of the players and deduct their mercenary maintenance amount from their gold
                        #for i in range(len(playerList)):
                                #playerList[i].setGold(playerList[i].getGold()-objMercenaryUtils.getPlayerMercenaryMaintenanceCost(playerList[i].getID()))
                                #playerList[i].setGold(playerList[i].getGold()+objMercenaryUtils.getPlayerMercenaryContractIncome(playerList[i].getID()))

                        ## Have some mercenaries wander away from the global mercenary pool if
                        ## g_bWanderlustMercenaries is set to true.
                        #if(g_bWanderlustMercenaries):

                                ##Rhye - start (less frequent updates)
                                ##wanderingMercenaryCount = gc.getGame().getMapRand().get(g_iWanderlustMercenariesMaximum, "Random Num")
                                ##objMercenaryUtils.removeMercenariesFromPool(wanderingMercenaryCount)
                                #teamPlayer = gc.getTeam(gc.getActivePlayer().getTeam())
                                ##if (not teamPlayer.isHasTech(con.iNationalism)):
                                #if (iGameTurn % g_bUpdatePeriod == (g_bUpdatePeriod-1)):
                                	#wanderingMercenaryCount = gc.getGame().getMapRand().get(g_iWanderlustMercenariesMaximum, "Random Num") + g_iWanderlustMercenariesMinimum
                                	#objMercenaryUtils.removeMercenariesFromPool(wanderingMercenaryCount)
                                ##Rhye - end


                        ## Add the mercenaries to the global mercenary pool if the g_bGameTurnMercenaryCreation
                        ## is set to true
                        #if(g_bGameTurnMercenaryCreation):

                                ##Rhye - start (less frequent updates)
                                ##objMercenaryUtils.addMercenariesToPool()
                                #if (iGameTurn % g_bUpdatePeriod == (g_bUpdatePeriod-1)):
                                        #objMercenaryUtils.addMercenariesToPool()
                                ##Rhye - end
                #print(" 3Miro onBegTurn out: ",iGameTurn)

                return 0



	def onBeginPlayerTurn(self, argsList):
		#print( " in Begin Player Turn ")
		iGameTurn, iPlayer = argsList

		print ("onBeginPlayerTurn PLAYER", iPlayer)

		if (self.rnf.getDeleteMode(0) != -1):
			self.rnf.deleteMode(iPlayer)

		# Denmark UP
		if(iPlayer == con.iDenmark):
			self.up.soundUP(iPlayer)

		# Aragon UP
		if(iPlayer == con.iAragon):
			self.up.confederationUP(iPlayer)

		self.pla.checkPlayerTurn(iGameTurn, iPlayer)

		if (gc.getPlayer(iPlayer).isAlive()):
			self.vic.checkPlayerTurn(iGameTurn, iPlayer)

		if (gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers and gc.getPlayer(iPlayer).getNumCities() > 0):
			self.sta.updateBaseStability(iGameTurn, iPlayer)

		if (gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers and not gc.getPlayer(iPlayer).isHuman()):
			self.rnf.checkPlayerTurn(iGameTurn, iPlayer) #for leaders switch

		if ( gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers ):
			utils.setLastTurnAlive( iPlayer, iGameTurn )

		if ( gc.hasUP( iPlayer, con.iUP_Janissary ) ):
			self.up.janissary( iPlayer )

                #Mercenaries - start

                # This method will add mercenaries to the global mercenary pool, display the mercenary manager screen
                # and provide the logic to make the computer players think.
                #player = gc.getPlayer(iPlayer)

                ##if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
                #if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):

                        ## Debug code - start
                        #if(g_bDebug):
                                #CvUtil.pyPrint(player.getName() + " Gold: " + str(player.getGold()) + " is human: " + str(player.isHuman()))
                        ## Debug code - end

                        ## Add the mercenaries to the global mercenary pool if the
                        ## g_bGameTurnMercenaryCreation is set to false
                        #if(not g_bGameTurnMercenaryCreation):
                                #objMercenaryUtils.addMercenariesToPool()

                        ## if g_bDisplayMercenaryManagerOnBeginPlayerTurn is true the the player is human
                        ## then display the mercenary manager screen
                        #if(g_bDisplayMercenaryManagerOnBeginPlayerTurn and player.isHuman()):
                                #self.mercenaryManager.interfaceScreen()

                        ## if the player is not human then run the think method
                        #if(not player.isHuman()):

                                ##Rhye - start
                                ##objMercenaryUtils.computerPlayerThink(iPlayer)
                                #if (player.isAlive()):
                                        ##if (iPlayer % (g_bAIThinkPeriod) == iGameTurn % (g_bAIThinkPeriod) and not gc.getTeam(player.getTeam()).isHasTech(con.iNationalism)):
                                        #if (iPlayer % (g_bAIThinkPeriod) == iGameTurn % (g_bAIThinkPeriod)):
                                                #print ("AI thinking (Mercenaries)", iPlayer) #Rhye
                                                #objMercenaryUtils.computerPlayerThink(iPlayer)
                                ##Rhye - end

                        ## Place any mercenaries that might be ready to be placed.
                        #objMercenaryUtils.placeMercenaries(iPlayer)
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


	#Rhye - start
	def onTechAcquired(self, argsList):

		#print ("onTechAcquired", argsList)
		iPlayer = argsList[2]

		iHuman = utils.getHumanID()

		self.vic.onTechAcquired(argsList[0], argsList[2])
		#self.res.onTechAcquired(argsList[0], argsList[2])

		if (gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > con.tBirth[iPlayer] and iPlayer < con.iNumPlayers):
			self.rel.onTechAcquired(argsList[0], argsList[2])

		if (gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > con.tBirth[iPlayer] and iPlayer < con.iNumPlayers):
			self.sta.onTechAcquired(argsList[0], argsList[2])
	#Rhye - end


	# This method creates a new instance of the MercenaryUtils class to be used later
	def onLoadGame(self, argsList):
		pass

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

                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
                #if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):

                        #unit = argsList[0]

                        ## Debug code - start
                        #if(g_bDebug):
                                #CvUtil.pyPrint("lost: " + unit.getName())
                        ## Debug code - end

                        ## If the unit being lost is a mercenary, check to see if they have been
                        ## replaced by an upgraded version of themselves. If they are then save
                        ## the new upgraded version of themselves and return immediately.
                        #if(objMercenaryUtils.isMercenary(unit)):

                                ## Debug code - start
                                #if(g_bDebug):
                                        #CvUtil.pyPrint("mercenary unit lost: " + unit.getName())
                                ## Debug code - end

                                ## Get the active player ID
                                #iPlayer = gc.getGame().getActivePlayer()

                                ## Get the reference of the actual player
                                #pyPlayer = PyPlayer(iPlayer)

                                ## Get the list of units for the player
                                #unitList = pyPlayer.getUnitList()

                                ## Go through the list of units to see if an upgraded version of
                                ## the unit has been added. If it exists then save it and return
                                ## immediately.
                                #for unit in unitList:

                                        #if(unit.getUnitType() != argsList[0].getUnitType() and unit.getNameNoDesc() == argsList[0].getNameNoDesc()):

                                                ## Debug code - start
                                                #if(g_bDebug):
                                                        #CvUtil.pyPrint("mercenary unit upgraded: " + unit.getName())
                                                ## Debug code - end

                                                #tmpMerc = objMercenaryUtils.createBlankMercenary()
                                                #tmpMerc.loadUnitData(unit)
                                                #tmpMerc.iBuilder = -1
                                                #objMercenaryUtils.saveMercenary(tmpMerc)
                                                #return

                        #mercenary = objMercenaryUtils.getMercenary(unit.getNameNoDesc())

                        #if(mercenary != None and g_bDisplayMercenaryMessages and mercenary.getBuilder() != -1 and unit.isDead()):
                                #strMessage = mercenary.getName() + " was lost under " + gc.getPlayer(mercenary.getOwner()).getName() + "'s service."
                                ## Inform the player that the mercenary has died.
                                #CyInterface().addMessage(mercenary.getBuilder(), True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True)
                        #unit = argsList[0]

                        ## Debug code - start
                        #if(g_bDebug):
                                #CvUtil.pyPrint("lost??: " + unit.getNameNoDesc())
                        ## Debug code - end

                        #objMercenaryUtils.removePlayerMercenary(unit)


        # This method handles the key input and will bring up the mercenary manager screen if the
        # player has at least one city and presses the 'M' key.
        def onKbdEvent(self, argsList):
                'keypress handler - return 1 if the event was consumed'

                iHuman = utils.getHumanID()
                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
                if (gc.getGame().getGameTurn() >= con.tBirth[iHuman]):

                        # TO DO: REMOVE THE FOLLOWING LINE BEFORE RELEASE.
                        #gc.getPlayer(0).setGold(20000)
                        eventType,key,mx,my,px,py = argsList

                        theKey=int(key)

                        if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_M) and self.eventManager.bAlt and gc.getActivePlayer().getNumCities() > 0 and gc.getActivePlayer().getCurrentEra() >= g_iStartingEra):

                                self.mercenaryManager.interfaceScreen()

                #Rhye - start debug
                eventType,key,mx,my,px,py = argsList

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
                        iDebugDeadCiv = iCarthage #default iEthiopia: always dead in 600AD
                        # 3Miro: not sure
                        #gc.getTeam(gc.getPlayer(iDebugDeadCiv).getTeam()).setHasTech(con.iCalendar, True, iDebugDeadCiv, False, False)
                        utils.makeUnit(con.iAxeman, iDebugDeadCiv, (0,0), 1)
                        gc.getGame().setActivePlayer(iDebugDeadCiv, False)
                        gc.getPlayer(iDebugDeadCiv).setPlayable(True)


                #Rhye - end debug

		# Absinthe: province highlight - based on SoI
		if eventType == self.EventKeyDown and px >= 0 and py >= 0 and int(key) == 45 and self.eventManager.bCtrl and not self.eventManager.bAlt:

			plot = gc.getMap().plot(px,py)
			iActivePlayer = gc.getGame().getActivePlayer()
			iActiveTeam = gc.getPlayer(iActivePlayer).getTeam()
			iProvinceID = rfcemaps.tProinceMap[plot.getY()][plot.getX()]

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
			self.lastProvinceID = rfcemaps.tProinceMap[plot.getY()][plot.getX()]

			# select an appriopriate color
			if rfcemaps.tProinceMap[plot.getY()][plot.getX()] == -1: # ocean and non-province tiles
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
				if rfcemaps.tProinceMap[plot.getY()][plot.getX()] == iProvinceID and (gc.getGame().isDebugMode() or plot.isRevealed(iActiveTeam, False)):
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

