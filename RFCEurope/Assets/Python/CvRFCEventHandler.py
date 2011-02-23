from CvPythonExtensions import *
import CvUtil
import CvEventManager #Mercenaries
import sys #Mercenaries
import PyHelpers 
import CvMainInterface #Mercenaries
import CvMercenaryManager #Mercenaries
import MercenaryUtils #Mercenaries
import CvScreenEnums  #Mercenaries
#import CvConfigParser #Mercenaries #Rhye
import Popup as PyPopup 

import StoredData
import RiseAndFall        
import Barbs                
import Religions        
import Resources        
import CityNameManager  
import UniquePowers     
import AIWars           
#import Congresses
import Consts as con
import XMLConsts as xml
import RFCUtils
utils = RFCUtils.RFCUtils()
import CvScreenEnums #Mercenaries, Rhye
import Victory
import Stability
import Plague
#import Communications
import Crusades  
import RFCEMaps as rfcemaps      
        
gc = CyGlobalContext()        
#iBetrayalCheaters = 15


#Rhye - start
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
iLithuania = con.iLithuania
iAustria = con.iAustria
iTurkey = con.iTurkey
iSweden = con.iSweden
iDutch = con.iDutch
iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers
#Rhye - end



#Mercenaries - start
objMercenaryUtils = MercenaryUtils.MercenaryUtils()

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

                self.EventKeyDown=6 #Mercenaries

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
                eventManager.addEventHandler("kbdEvent",self.onKbdEvent) #Mercenaries
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
                #self.cong = Congresses.Congresses()
                self.vic = Victory.Victory()
                self.sta = Stability.Stability()
                self.pla = Plague.Plague()
                #self.com = Communications.Communications()
                self.crusade = Crusades.Crusades()
                
                
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

                objMercenaryUtils = MercenaryUtils.MercenaryUtils()
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
                
                #gc.getTeam(gc.getPlayer(iLoopCiv).getTeam()).setAtWar(iCiv, True)
                #teamCiv.setAtWar(iLoopCiv, True)
                #gc.getTeam(gc.getPlayer(iBulgaria).getTeam()).setAtWar(gc.getPlayer(iByzantium).getTeam(), True)
                #gc.getTeam(gc.getPlayer(iByzantium).getTeam()).setAtWar(gc.getPlayer(iBulgaria).getTeam(), True)
                # 3Miro: WarOnSpawn
                self.rnf.setWarOnSpawn()

                #Mercenaries - start
                global objMercenaryUtils        
                objMercenaryUtils = MercenaryUtils.MercenaryUtils()
		#Mercenaries - end
                
                return 0


        def onCityAcquired(self, argsList):
                #'City Acquired'
                owner,playerType,city,bConquest,bTrade = argsList
                #CvUtil.pyPrint('City Acquired Event: %s' %(city.getName()))
                #if ( owner >= con.iNumMajorPlayers and playerType < con.iNumMajorPlayers and rfcemaps.tWarsMaps[playerType][con.iMapMaxY-city.getY()-1][city.getX()] == 0 ):
                #	print("  3Miro - Special City Captured: ")
                #	print("  Params: ",owner,playerType,bConquest,bTrade)
                
                self.rnf.onCityAcquired(owner,playerType,city,bConquest,bTrade)
                	
                self.cnm.renameCities(city, playerType)
                
                # 3Miro Arab and Turkish UP
                if ( gc.hasUP( playerType, con.iUP_Faith ) ):
                	self.up.faithUP( playerType, city )
                #elif (playerType == con.iTurkey):
                #        self.up.turkishUP(city)

                if (playerType < iNumMajorPlayers):
                         utils.spreadMajorCulture(playerType, city.getX(), city.getY())

                self.sta.onCityAcquired(owner,playerType,city,bConquest,bTrade)

                # 3Miro: Remove exile mechanics, if you are human and you lose your capital, might as well load a new game
                #if (bConquest):
                #        #self.rnf.collapseCapitals(owner, city, playerType)
                #        if (owner == utils.getHumanID() and playerType != con.iBarbarian):
                #                self.rnf.collapseHuman(owner, city, playerType)
                #        #print ("exile data:", self.rnf.getExileData(0), city.getX(), self.rnf.getExileData(1), city.getY(), self.rnf.getExileData(2))
                #        if (self.rnf.getExileData(0) == city.getX() and self.rnf.getExileData(1) == city.getY()):
                #                if (playerType == utils.getHumanID() and self.rnf.getExileData(2) != -1):
                #                        self.rnf.escape(city)

		# 3Miro: Jerusalem's Golden Age Insentive
		pPlayer = gc.getPlayer(playerType)
		if ( pPlayer.getStateReligion() == xml.iCatholicism ):
			if ( city.getX() == con.iJerusalem[0] and city.getY() == con.iJerusalem[1] ):
				self.crusade.success( playerType )

		#Sedna17, added code for Krak des Chevaliers
		#Begin Krak
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

		# End Krak des Chevaliers
				
                # 3Miro: National wonders and city acuire by trade
                #if (bTrade):
                #        for i in range (con.iScotlandYard +1 - con.iHeroicEpic):
                #                iNationalWonder = i + con.iHeroicEpic
                #                if (city.hasBuilding(iNationalWonder)):
                #                        city.setHasRealBuilding((iNationalWonder), False)

                self.pla.onCityAcquired(owner,playerType,city) #Plague

                self.vic.onCityAcquired(owner, playerType, bConquest) #Victory
                
                return 0

        def onCityRazed(self, argsList):
                #'City Razed'
                city, iPlayer = argsList

                self.rnf.onCityRazed(city.getOwner(),iPlayer,city)

                self.sta.onCityRazed(city.getOwner(),iPlayer,city)
                self.vic.onCityRazed(iPlayer,city)
		
                #if (iPlayer == con.iMongolia):
                #        self.up.setLatestRazeData(0, gc.getGame().getGameTurn())
                #        owner = city.getOwner()
                #        if (city.getOwner() == iPlayer):
                #                if (city.getPreviousOwner() != -1):
                #                        owner = city.getPreviousOwner()                        
                #        self.up.setLatestRazeData(1, owner)
                #        self.up.setLatestRazeData(2, city.getPopulation())
                #        self.up.setLatestRazeData(3, city.getX())
                #        self.up.setLatestRazeData(4, city.getY())
                #        print ("city.getPopulation()", city.getPopulation())
                #        print ("prev", city.getPreviousOwner(), "curr", city.getOwner())
                #        self.up.setMongolAI()

                self.pla.onCityRazed(city,iPlayer) #Plague
                        
                #if (iPlayer == con.iMongolia):
                #        self.vic.onCityRazed(iPlayer) #Victory



        def onCityBuilt(self, argsList):
                'City Built'
                city = argsList[0]
                
                iOwner = city.getOwner()
                
                self.rnf.onCityBuilt(iOwner, city.getX(), city.getY() )
                
                if (iOwner < con.iNumActivePlayers): 
                        self.cnm.assignName(city)


                #Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
                pCurrent = gc.getMap().plot( city.getX(), city.getY() )
                for i in range(con.iNumTotalPlayers - con.iNumActivePlayers):
                        iMinorCiv = i + con.iNumActivePlayers
                        pCurrent.setCulture(iMinorCiv, 0, True)
                pCurrent.setCulture(con.iBarbarian, 0, True)

                if (iOwner < iNumMajorPlayers):
                        utils.spreadMajorCulture(iOwner, city.getX(), city.getY())

		# 3Miro: Turkish UP
                #if (iOwner == con.iTurkey):
                #        self.up.turkishUP(city)


		# 3Miro: USA UHV
                #if (self.vic.getNewWorld(0) == -1):
                #        if (iOwner not in con.lCivGroups[5] and iOwner < iNumActivePlayers):
                #                if (city.getX() >= con.tAmericasTL[0] and city.getX() <= con.tAmericasBR[0] and city.getY() >= con.tAmericasTL[1] and city.getY() <= con.tAmericasBR[1]):
                #                        self.vic.setNewWorld(0, iOwner)

		# 3Miro: nations with city build UHV
                #if (iOwner == con.iRussia or \
                #    iOwner == con.iFrance or \
                #    iOwner == con.iEngland or \
                #    iOwner == con.iSpain or \
                #    #iOwner == con.iCarthage or \
                #    iOwner == con.iVikings or \
                #    iOwner == con.iPortugal or \
                #    iOwner == con.iNetherlands):    
                if ( iOwner == con.iPortugal ):
                	self.vic.onCityBuilt(city, iOwner) #Victory

		# 3MiroUP: faith on city found
		if ( gc.hasUP( iOwner, con.iUP_Faith ) ):
			self.up.faithUP( iOwner, city )

                if (iOwner < con.iNumPlayers):
                        self.sta.onCityBuilt(iOwner, city.getX(), city.getY() )

        def onCombatResult(self, argsList):
                #self.up.aztecUP(argsList)
                #self.vic.onCombatResult(argsList)
                self.sta.onCombatResult(argsList)



##        def onChangeWar(self, argsList):
##                print ("No cheaters1")
##                if (bIsWar):
##                        print ("No cheaters2")
##                        if (argsList[1] == utils.getHumanID() and gc.getGame().getGameTurn() <= con.tBirth[argsList[1]] + iBetrayalCheaters):
##                                print ("No cheaters3")
##                                self.rnf.setNewCivFlip(argsList[1])
##                                self.rnf.setTempTopLeft(rnf.tCoreAreasTL[argsList[1]])
##                                self.rnf.setTempBottomRight(rnf.tCoreAreasBR[argsList[1]])
##                                self.rnf.setBetrayalTurns(rnf.iBetrayalPeriod)
##                                self.rnf.initBetrayal()



        def onReligionFounded(self, argsList):
                'Religion Founded'
                iReligion, iFounder = argsList

                #if (not gc.getPlayer(0).isPlayable() and gc.getGame().getGameTurn() == 151): #late start condition
                #        return
        
        	lCities = PyPlayer( iFounder ).getCityList( )
        	for iCity in range( len( lCities ) ):
        		pCity = gc.getPlayer( iFounder ).getCity( lCities[ iCity ].getID( ) )
        		if ( pCity.isHolyCityByType( iReligion ) and iReligion <> xml.iJudaism): #Sedna -- ProtestantShrine is now starting point for consistency with Religion.xml, Judaism is special
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
                        
                # 3MiroCrusade: end Crusades for the Holy Land after the Reformation
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
                        #self.com.onBuildingBuilt(iOwner, iBuildingType, city) # 3Miro: no communications
                # 3Miro: no congress
                #self.cong.onBuildingBuilt(iOwner, iBuildingType, city)
                #3MiroFaith
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

#	def onImprovementDestroyed(self, argsList):
#		print ("Improvement Destroyed")
#		iImprovement, iOwner, iX, iY = argsList
#		print ("Owner was",iOwner)
#		if (iOwner < con.iNumPlayers):
#			self.sta.onImprovementDestroyed(iOwner)
#		self.barb.onImprovementDestroyed(iX,iY)
#		if (iOwner >= iNumTotalPlayers or iOwner < 0):
#			print("Owner Satisfied")
#			if (iImprovement >= con.iImprovementCottage and iImprovement <= con.iImprovementTown):
#				print ("Improve Type Satisfied")
#				self.barb.onImprovementDestroyed(iX,iY)

        def onBeginGameTurn(self, argsList):
                iGameTurn = argsList[0]

		if ( iGameTurn == xml.i1053AD ):
			iHuman = utils.getHumanID()
			sText = CyTranslator().getText("TXT_KEY_GREAT_SCHISM", ())
			CyInterface().addMessage(iHuman, True, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)


                #print ("iGameTurn", iGameTurn)
                #self.printDebug(iGameTurn)

                #debug - stop autoplay
                #utils.makeUnit(con.iAxeman, con.iAmerica, (0,0), 1)
                #if (iGameTurn == 250):
                #        utils.makeUnit(con.iAxeman, con.iAmerica, (0,0), 1)

		#print(" 3Miro onBegTurn ")                
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
		#print("********* Polish Test *********")
		#print(gc.getPlayer(iPoland).getAgricultureHistory(iGameTurn))
		#iAgriculture = gc.getPlayer(iPoland).calculateTotalYield(YieldTypes.YIELD_FOOD)
		#print(iAgriculture)
		#print("*******************************")
                #Mercenaries - start

                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):
                if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):
                        
                        # Get the list of active players in the game
                        playerList = PyGame.getCivPlayerList()
                        
                        # Go through each of the players and deduct their mercenary maintenance amount from their gold
                        for i in range(len(playerList)):
                                playerList[i].setGold(playerList[i].getGold()-objMercenaryUtils.getPlayerMercenaryMaintenanceCost(playerList[i].getID()))
                                playerList[i].setGold(playerList[i].getGold()+objMercenaryUtils.getPlayerMercenaryContractIncome(playerList[i].getID()))
                
                        # Have some mercenaries wander away from the global mercenary pool if 
                        # g_bWanderlustMercenaries is set to true.        
                        if(g_bWanderlustMercenaries):

                                #Rhye - start (less frequent updates)
                                #wanderingMercenaryCount = gc.getGame().getMapRand().get(g_iWanderlustMercenariesMaximum, "Random Num")
                                #objMercenaryUtils.removeMercenariesFromPool(wanderingMercenaryCount)
                                teamPlayer = gc.getTeam(gc.getActivePlayer().getTeam())
                                #if (not teamPlayer.isHasTech(con.iNationalism)):                     
                                if (iGameTurn % g_bUpdatePeriod == (g_bUpdatePeriod-1)):
                                	wanderingMercenaryCount = gc.getGame().getMapRand().get(g_iWanderlustMercenariesMaximum, "Random Num") + g_iWanderlustMercenariesMinimum
                                	objMercenaryUtils.removeMercenariesFromPool(wanderingMercenaryCount)
                                #Rhye - end
                            
                                
                        # Add the mercenaries to the global mercenary pool if the g_bGameTurnMercenaryCreation 
                        # is set to true
                        if(g_bGameTurnMercenaryCreation):
                            
                                #Rhye - start (less frequent updates)
                                #objMercenaryUtils.addMercenariesToPool()                  
                                if (iGameTurn % g_bUpdatePeriod == (g_bUpdatePeriod-1)):
                                        objMercenaryUtils.addMercenariesToPool()
                                #Rhye - end                
                #print(" 3Miro onBegTurn out: ",iGameTurn)
                
                #if ( iGameTurn % 10 == 0 ):
                #	print( " 3Miro: Turn: ",iGameTurn )
                #	for i in range( con.iNumPlayers ):
                #		print( "    - tech Player ",i,"   research: ",utils.getRC( i ) )
                
                return 0



        def onBeginPlayerTurn(self, argsList):        
        	print( " in Begin Player Turn ")
                iGameTurn, iPlayer = argsList                

                #print ("PLAYER", iPlayer)
                #iYeald = gc.getPlayer(iPlayer).calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
                #print(" Commerce: ",iPlayer, iYeald )
                #if (iPlayer == con.iMongolia):
                #        if (iGameTurn == self.up.getLatestRazeData(0) +1):
                #                self.up.setMongolAI()
                
                #debug - stop autoplay
                #utils.makeUnit(con.iAxeman, iAmerica, (0,0), 1)

                if (self.rnf.getDeleteMode(0) != -1):
                        self.rnf.deleteMode(iPlayer)
                        
                self.pla.checkPlayerTurn(iGameTurn, iPlayer)

                if (gc.getPlayer(iPlayer).isAlive()):
                        self.vic.checkPlayerTurn(iGameTurn, iPlayer)


                if (gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers and gc.getPlayer(iPlayer).getNumCities() > 0):
                        self.sta.updateBaseStability(iGameTurn, iPlayer)

                if (gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers and not gc.getPlayer(iPlayer).isHuman()):
                        self.rnf.checkPlayerTurn(iGameTurn, iPlayer) #for leaders switch
                        
                if ( gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers ):
                	utils.setLastTurnAlive( iPlayer, iGameTurn )

                #Mercenaries - start
        
                # This method will add mercenaries to the global mercenary pool, display the mercenary manager screen
                # and provide the logic to make the computer players think.
                player = gc.getPlayer(iPlayer)

                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
                if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):

                        # Debug code - start
                        if(g_bDebug):
                                CvUtil.pyPrint(player.getName() + " Gold: " + str(player.getGold()) + " is human: " + str(player.isHuman()))
                        # Debug code - end        
                        
                        # Add the mercenaries to the global mercenary pool if the 
                        # g_bGameTurnMercenaryCreation is set to false
                        if(not g_bGameTurnMercenaryCreation):
                                objMercenaryUtils.addMercenariesToPool()

                        # if g_bDisplayMercenaryManagerOnBeginPlayerTurn is true the the player is human
                        # then display the mercenary manager screen
                        if(g_bDisplayMercenaryManagerOnBeginPlayerTurn and player.isHuman()):
                                self.mercenaryManager.interfaceScreen()

                        # if the player is not human then run the think method
                        if(not player.isHuman()):
                            
                                #Rhye - start
                                #objMercenaryUtils.computerPlayerThink(iPlayer)                                        
                                if (player.isAlive()):
                                        #if (iPlayer % (g_bAIThinkPeriod) == iGameTurn % (g_bAIThinkPeriod) and not gc.getTeam(player.getTeam()).isHasTech(con.iNationalism)):
                                        if (iPlayer % (g_bAIThinkPeriod) == iGameTurn % (g_bAIThinkPeriod)):
                                                print ("AI thinking (Mercenaries)", iPlayer) #Rhye
                                                objMercenaryUtils.computerPlayerThink(iPlayer)                                                                
                                #Rhye - end
                
                        # Place any mercenaries that might be ready to be placed.
                        objMercenaryUtils.placeMercenaries(iPlayer)
                #print ("PLAYER FINE", iPlayer)
                print( " out Begin Player Turn ",iGameTurn, iPlayer )
                
                # 3Miro: decrease the prosecution count
                #iProsecutionCount = utils.getProsecutionCount( iPlayer )
                #if ( iProsecutionCount > 1 ):
                #	iProsecutionCount -= 1
                #	utils.setProsecutionCount( iPlayer, iProsecutionCount )
                	
                #if ( con.tBirth[iPlayer] == iGameTurn ):
                #	for i in range( con.iNumTechs ):
                #		if ( gc.getTeam( gc.getPlayer(iPlayer).getTeam() ).isHasTech( i ) ):
                #			utils.setRC( iPlayer, utils.getRC( iPlayer ) + gc.getTechInfo( i ).getResearchCost() )
                			
                #utils.setRC( iPlayer, utils.getRC( iPlayer ) + gc.getPlayer( iPlayer ).getCommerceRate( CommerceTypes.COMMERCE_RESEARCH ) )
        
        
        def onEndPlayerTurn(self, argsList):
		# 3Miro does not get called
                iGameTurn, iPlayer = argsList
                #print (" 3Miro END PLAYER", iPlayer, iGameTurn)
                
                'Called at the end of a players turn'


##                if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
##                
##                        iGameTurn, iPlayer = argsList
##                        
##                        player = gc.getPlayer(iPlayer)
##
##                        CyInterface().addImmediateMessage(player.getName(),"")
##                #print ("END PLAYER FINE", iPlayer)



        def onEndGameTurn(self, argsList):
            	# 3Miro when everyone end their turn
                iGameTurn = argsList[0]
                #print (" 3Miro END TURN ", iGameTurn)
                self.sta.checkImplosion(iGameTurn)
                
                


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
                
                #if (not gc.getPlayer(0).isPlayable() and gc.getGame().getGameTurn() == 151): #late start condition
                #        return
                
                # 3Miro: tech related UHV
                #if (gc.getGame().getGameTurn() > con.tBirth[iPlayer]):                    
                #        if (iPlayer == con.iGreece or \
                #            iPlayer == con.iMaya or \
                #            iPlayer == con.iEngland or \
                #            iPlayer == con.iGermany or \
                #            iPlayer == con.iAztecs or \
                #            iPlayer == con.iBabylonia):                            
                #                self.vic.onTechAcquired(argsList[0], argsList[2])		
                self.vic.onTechAcquired(argsList[0], argsList[2])
                                
                if (gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > con.tBirth[iPlayer] and iPlayer < con.iNumPlayers):
                        self.rel.onTechAcquired(argsList[0], argsList[2])
                
                if (gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > con.tBirth[iPlayer] and iPlayer < con.iNumPlayers):
                        self.sta.onTechAcquired(argsList[0], argsList[2])

		# 3Miro: as soon as someone discovers the Gunpowder, the Theodosian walls will disapear from Constantinople
		#  this will make the city much easier to conquer by the Ottomans
		# 3Miro: update - this helps Bulgaria, but not Turkey ... go figure
		#if ( argsList[0] == con.iGunpowder ):
		#	pCity = gc.getMap().plot( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1]).getPlotCity()
		#	if ( pCity.hasBuilding( con.iTheodosianWalls ) ):
		#		pCity.setHasRealBuilding(con.iTheodosianWalls, False)

		# 3Miro: no congress
                #if (gc.getGame().getGameTurn() > con.i1000AD):
                #        self.cong.onTechAcquired(argsList[0], argsList[2])

		# 3Miro: obsolete Mercenaries with Nationalism
                #if (gc.getGame().getGameTurn() >= con.tBirth[iHuman]):
                #	pass

                        #if (argsList[0] == con.iNationalism):
                        #if (argsList[2] == iHuman):
                        #	for iLoopCiv in range (con.iNumPlayers):
                        #            
                        #		mercenaryDict = objMercenaryUtils.getPlayerMercenaries(iLoopCiv)
                        #                mercenary = objMercenaryUtils.getHighestMaintenanceMercenary(mercenaryDict)

                        #                while(mercenary != None):
                        #                        # Get the mercenary with the highest maintenance cost
                        #                	mercenaryDict = objMercenaryUtils.getPlayerMercenaries(iLoopCiv)
                        #                        mercenary = objMercenaryUtils.getHighestMaintenanceMercenary(mercenaryDict)
                        #                        # Have the computer fire the mercenary
                        #                        if(mercenary != None):
                        #                        	objMercenaryUtils.fireMercenary(mercenary.getName(), iLoopCiv)
                        #        screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
                        #        screen.hide("MercenaryManagerButton")
                        #        CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_MERCENARIES_DISABLED", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
                                
        #Rhye - end
                
                



        # This method creates a new instance of the MercenaryUtils class to be used later
	def onLoadGame(self, argsList):

                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
		if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):

			global objMercenaryUtils

			objMercenaryUtils = MercenaryUtils.MercenaryUtils()



        # This method will redraw the main interface once a unit is promoted. This way the 
        # gold/turn information will be updated.        
        def onUnitPromoted(self, argsList):
                'Unit Promoted'

                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye   
                if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):
                        pUnit, iPromotion = argsList
                        player = PyPlayer(pUnit.getOwner())

                        if(objMercenaryUtils.isMercenary(pUnit)):
                                CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)




        # This method will remove a mercenary unit from the game if it is killed
        def onUnitKilled(self, argsList):
                'Unit Killed'

                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
                if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):
                    
                        unit, iAttacker = argsList
                        
                        mercenary = objMercenaryUtils.getMercenary(unit.getNameNoDesc())

                        if(mercenary != None and g_bDisplayMercenaryMessages and mercenary.getBuilder() != -1 and unit.isDead()):
                                strMessage = mercenary.getName() + " has died under " + gc.getPlayer(mercenary.getOwner()).getName() + "'s service."
                                # Inform the player that the mercenary has died.
                                CyInterface().addMessage(mercenary.getBuilder(), True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True) 

                        objMercenaryUtils.removePlayerMercenary(unit)


        # This method will remove a mercenary unit from the game if it is lost
        def onUnitLost(self, argsList):
                'Unit Lost'

                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
                if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):
        
                        unit = argsList[0]
                        
                        # Debug code - start
                        if(g_bDebug):
                                CvUtil.pyPrint("lost: " + unit.getName())
                        # Debug code - end
                        
                        # If the unit being lost is a mercenary, check to see if they have been
                        # replaced by an upgraded version of themselves. If they are then save
                        # the new upgraded version of themselves and return immediately.
                        if(objMercenaryUtils.isMercenary(unit)):

                                # Debug code - start
                                if(g_bDebug):        
                                        CvUtil.pyPrint("mercenary unit lost: " + unit.getName())
                                # Debug code - end
                                        
                                # Get the active player ID
                                iPlayer = gc.getGame().getActivePlayer()
                                
                                # Get the reference of the actual player
                                pyPlayer = PyPlayer(iPlayer)

                                # Get the list of units for the player
                                unitList = pyPlayer.getUnitList()
                                        
                                # Go through the list of units to see if an upgraded version of 
                                # the unit has been added. If it exists then save it and return
                                # immediately.
                                for unit in unitList:

                                        if(unit.getUnitType() != argsList[0].getUnitType() and unit.getNameNoDesc() == argsList[0].getNameNoDesc()):

                                                # Debug code - start
                                                if(g_bDebug):        
                                                        CvUtil.pyPrint("mercenary unit upgraded: " + unit.getName())
                                                # Debug code - end
                                                
                                                tmpMerc = objMercenaryUtils.createBlankMercenary()
                                                tmpMerc.loadUnitData(unit)
                                                tmpMerc.iBuilder = -1
                                                objMercenaryUtils.saveMercenary(tmpMerc)
                                                return
                                                
                        mercenary = objMercenaryUtils.getMercenary(unit.getNameNoDesc())

                        if(mercenary != None and g_bDisplayMercenaryMessages and mercenary.getBuilder() != -1 and unit.isDead()):
                                strMessage = mercenary.getName() + " was lost under " + gc.getPlayer(mercenary.getOwner()).getName() + "'s service."
                                # Inform the player that the mercenary has died.
                                CyInterface().addMessage(mercenary.getBuilder(), True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True) 
                        unit = argsList[0]
                        
                        # Debug code - start
                        if(g_bDebug):        
                                CvUtil.pyPrint("lost??: " + unit.getNameNoDesc())        
                        # Debug code - end

                        objMercenaryUtils.removePlayerMercenary(unit)


        # This method handles the key input and will bring up the mercenary manager screen if the 
        # player has at least one city and presses the 'M' key.
        def onKbdEvent(self, argsList):
                'keypress handler - return 1 if the event was consumed'

                #if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]): #Rhye
                if (gc.getGame().getGameTurn() >= con.tBirth[utils.getHumanID()]):
                
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


                        iHuman = utils.getHumanID()
                        iGameTurn = gc.getGame().getGameTurn()

                        
##                        print("fava", gc.getGame().getGameTurn())
##                        print(self.rnf.getNewCiv(), self.rnf.getNewCivFlip(), self.rnf.getSpawnDelay(con.iPersia), self.rnf.getFlipsDelay(con.iPersia))

                        #print(self.aiw.getNextTurnAIWar())
                        #self.aiw.setNextTurnAIWar(gc.getGame().getGameTurn())
                        #self.aiw.checkTurn(gc.getGame().getGameTurn())
                        #print(self.aiw.getNextTurnAIWar())
                        ##for i in range(iNumPlayers):
                        #        print(i)
                        #        self.aiw.checkGrid(i)
                        
                        #gc.getGame().setGameTurn(400)

                        #for a in range(1):
                                #self.sta.test1(gc.getGame().getGameTurn())
                                #self.sta.test2(gc.getGame().getGameTurn())

                        #for a in range(iNumMajorPlayers):
                        #        if (gc.getPlayer(a).isAlive()):
                                        #self.sta.updateBaseStabilityTestOld(gc.getGame().getGameTurn(), a)
                                        #self.sta.updateBaseStabilityTest(gc.getGame().getGameTurn(), a)
                        
                        #gc.getTeam(gc.getPlayer(con.iCarthage).getTeam()).setVassal(con.iMongolia, True, True)
                        #gc.getTeam(gc.getPlayer(iEngland).getTeam()).signDefensivePact(iJapan)
                        #gc.getTeam(gc.getPlayer(iInca).getTeam()).declareWar(iMongolia, True, -1)                        
                        #gc.getGame().setActivePlayer(con.iVikings, False)
                        #gc.getTeam(gc.getPlayer(iAztecs).getTeam()).makePeace(iMongolia)

                        
                        #utils.killCiv(con.iVikings, con.iRussia)
                        #self.sta.checkTurn(gc.getGame().getGameTurn())
                        #self.rnf.resurrection(gc.getGame().getGameTurn())

##                        gc.getMap().plot(27, 30).setFeatureType(-1, 0)
##                        gc.getMap().plot(28, 31).setFeatureType(-1, 0)
##                        gc.getMap().plot(31, 13).setPlotType(PlotTypes.PLOT_HILLS, True, True)

                        #self.com.decay(con.iGermany)                
                        #self.data.setupScriptData()
                        #gc.getGame().setWinner(con.iEgypt, 0)
                        #if (len(lLeaders[iDeadCiv]) > 1):
                        #gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).signOpenBorders(con.iChina)
                        #print ("CC1", gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).canContact(con.iEgypt))
                        #print ("ME1", gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).isHasMet(con.iEgypt))
                        #gc.getTeam(gc.getPlayer(con.iJapan).getTeam()).cutContact(con.iChina)
                        #gc.getTeam(gc.getPlayer(con.iChina).getTeam()).cutContact(con.iJapan)
                        #print ("CC2", gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).canContact(con.iEgypt))
                        #print ("ME2", gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).isHasMet(con.iEgypt))
                        #for i in range (con.iNumPlayers):
                        #        gc.getTeam(gc.getPlayer(con.iInca).getTeam()).cutContact(i)
                        #gc.getTeam(gc.getPlayer(con.iChina).getTeam()).setVassal(con.iJapan, True, True)
                        #gc.getGame().changePlayer(con.iChina, 0, 22, con.iChina, False, True)
                        #gc.getPlayer(con.iBabylonia).setLeader(24)
                        #gc.getPlayer(con.iEgypt).changeGold(3000)
                        #gc.getMap().plot(72, 32).getPlotCity().changeBuildingProduction(con.iBroadway,639)
                        #print ("CC2", gc.getTeam(gc.getPlayer(con.iEgypt).getTeam()).canContact(con.iNative))
                        #newCivDesc = CyTranslator().getText("TXT_KEY_NAM_CHI1", ())
##                        newCivDesc = "TXT_KEY_NAM_CHI1"
##                        newDesc = newCivDesc.encode('latin-1')
##                        gc.getPlayer(con.iChina).setCivDescription(newDesc)
##                        print (gc.getPlayer(con.iChina).getCivilizationDescription(0), gc.getPlayer(con.iChina).getCivilizationDescriptionKey(), gc.getPlayer(con.iChina).getCivilizationAdjective(0), gc.getPlayer(con.iChina).getCivilizationAdjectiveKey())
##                        print (gc.getPlayer(con.iIndia).getCivilizationDescription(0), gc.getPlayer(con.iIndia).getCivilizationDescriptionKey(), gc.getPlayer(con.iIndia).getCivilizationAdjective(0), gc.getPlayer(con.iIndia).getCivilizationAdjectiveKey())
##                        self.rnf.showPopup(7614, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), CyTranslator().getText("TXT_KEY_NEWCIV_MESSAGE", (gc.getPlayer(con.iChina).getCivilizationDescriptionKey(),)), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))

                        #gc.getTeam(gc.getPlayer(con.iChina).getTeam()).setVassal(con.iArabia, True, True)

                        
                        #invasion attempt
                        #if (iGameTurn == 100):
                        #        utils.makeUnit(con.iAxeman, iGermany, con.tCapitals[iGermany], 3)
                        #        utils.makeUnit(con.iSwordsman, iGermany, con.tCapitals[iGermany], 3)
                        
                        #for iCiv in range(iNumPlayers):
                        #        for pyCity in PyPlayer(iCiv).getCityList():
                        #                print (pyCity.GetCy().getName())

                        #debug - kills every unit
                        #for x in range(40, 123):
                        #        for y in range(0, 67):
                        #                pCurrent = gc.getMap().plot( x, y )
                        #                if (pCurrent.getNumUnits() > 0):
                        #                        for i in range (pCurrent.getNumUnits()):
                        #                                unit = pCurrent.getUnit(0)
                        #                                unit.kill(False, con.iBarbarian)


##                        if (gc.getPlayer(utils.getHumanID()).getNumCities() > 1):
##                                CyInterface().addImmediateMessage(CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "")
##                                utils.killAndFragmentCiv(utils.getHumanID(), True)
##                                utils.setStability(utils.getHumanID(), -15)


                        #self.pla.setGenericPlagueDates(0, 96)
                        #self.pla.spreadPlague(con.iJapan)
                        #self.pla.stopPlague(con.iJapan)
                        #self.pla.infectCity(utils.getRandomCity(con.iJapan))
                        #print ("Countdown", self.pla.getPlagueCountdown( con.iJapan ))
                    
                        
                        #utils.killAndFragmentCiv(con.iEngland, iIndependent, iIndependent2, -1, False)
                        #self.rnf.resurrection(302)
                        
                        #utils.killAndFragmentCiv(con.iRome, iIndependent, iIndependent2, -1, True)
                        #gc.getGame().setActivePlayer(con.iEgypt, False)
                        #teamEgypt.changeResearchProgress(con.iNationalism, 3299, iEgypt)
                        #teamAztecs.changeResearchProgress(con.iSteel, 3399, iAztecs)
                        
                        #self.sta.normalization(200)
                        #gc.getGame().setActivePlayer(con.iNetherlands, False)
                        #gc.getPlayer(con.iPortugal).changeGold(200)
                        
                        #CyInterface().addImmediateMessage(CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()), "")
                        #CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, CyTranslator().getText("TXT_KEY_EMBASSY_ESTABLISHED", (gc.getPlayer(con.iRussia).getCivilizationAdjectiveKey(),)) + " " + "Citta di prova", "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)

                        #CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_PERIOD", ()) + " " + CyTranslator().getText("TXT_KEY_STABILITY_GREAT_DEPRESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                        #CyInterface().addMessage(utils.getHumanID(), True, 5, CyTranslator().getText("TXT_KEY_CONGRESS_NOTIFY_YES2", ()), "", 0, "", ColorTypes(100), -1, -1, True, True)
##                        for i in range(128):
##                                CyInterface().addMessage(utils.getHumanID(), True, 1, "i", "", 0, "", ColorTypes(i), -1, -1, False, True)
##                                if (i % 10 == 0):
##                                         CyInterface().addMessage(utils.getHumanID(), True, 1, "10", "", 0, "", ColorTypes(0), -1, -1, False, True)
                        #print ("vic", self.vic.getNumSinks())

                        #dummy, plotList = utils.squareSearch( (29,28), (31,31), utils.outerInvasion, [])
                        #print (plotList)
                        #utils.setStability(con.iChina, -25)
                        
                        #city = gc.getMap().plot( 79, 40 ).getPlotCity() 
                        #self.pla.infectCity(city)
                        #self.pla.spreadPlague(con.iPersia)
                        #self.pla.processPlague(con.iPersia)

                        #city = gc.getMap().plot( 90, 40 ).getPlotCity()
                        #print ("9040", city.getCulture(con.iIndia), 4000 + 2000*gc.getPlayer(con.iIndia).getCurrentEra())

                        
                        #CyInterface().DoSoundtrack("AS2D_R_F_C")
                        #if (gc.getPlayer(con.iNetherlands).countOwnedBonuses(con.iSpices) + gc.getPlayer(con.iNetherlands).getBonusImport(con.iSpices) >= 5):
                        #        self.vic.setGoal(iNetherlands, 2, 0)

                        #utils.setLastRecordedStabilityStuff(2, 0)
                        #utils.setLastRecordedStabilityStuff(1, 40)

##                        #print (CyGame().getCurrentLanguage())
##                        popup = PyPopup.PyPopup()
##                        popup.setHeaderString(CyTranslator().getText("TXT_KEY_EXILE_TITLE", ()))          
##                        popup.setBodyString( CyTranslator().getText("TXT_KEY_EXILE_TEXT", (gc.getPlayer(con.iGermany).getCivilizationAdjectiveKey(), gc.getPlayer(con.iSpain).getCivilizationShortDescription(0))))
####                        popup.setHeaderString(CyTranslator().getText("TXT_KEY_ESCAPE_TITLE", ()))          
####                        popup.setBodyString( CyTranslator().getText("TXT_KEY_ESCAPE_TEXT", (gc.getPlayer(con.iGermany).getCivilizationAdjectiveKey(),)))
##                        popup.launch()
##
##                        CyInterface().addMessage(utils.getHumanID(), True, con.iDuration/2, ("XXX" + " " + \
##                                                                                   CyTranslator().getText("TXT_KEY_CONGRESS_NOTIFY_YES", (gc.getPlayer(con.iSpain).getCivilizationAdjectiveKey(),))), \
##                                                                                   "", 0, "", ColorTypes(con.iCyan), -1, -1, True, True)
##                        self.rnf.newCivPopup(con.iSpain)
##
##                        self.rnf.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
##                               CyTranslator().getText("TXT_KEY_REBELLION_TEXT", (gc.getPlayer(con.iGermany).getCivilizationAdjectiveKey(),)), \
##                               (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), \
##                                CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
##
##                        CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, \
##                                                                                 CyTranslator().getText("TXT_KEY_STABILITY_GREAT_DEPRESSION_INFLUENCE", (gc.getPlayer(con.iSpain).getCivilizationDescription(0),)), \
##                                                                                 "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
##
####                        CyInterface().addMessage(utils.getHumanID(), True, con.iDuration, \
####                                                        (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (gc.getPlayer(con.iGermany).getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
##                                
                        #print ("ERA", gc.getInfoTypeForString("ERA_CLASSICAL"))
##                        for iEuroCiv in range(iNumPlayers):
##                                if (iEuroCiv in con.lCivGroups[0]):
##                                        if (not self.vic.checkNotOwnedArea_Skip(iEuroCiv, (24, 3), (43, 32), (32,14), (43,30))):
##                                                CyInterface().addImmediateMessage(CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "")

##                        for x in range(0, 123):
##                                for y in range(0, 67):
##                                        pCurrent = gc.getMap().plot( x, y )
##                                        if (pCurrent.isWater()):
##                                                pCurrent.setOwner(-1)

                        
                        pass


                if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_N) and self.eventManager.bAlt):

                        print("ALT-N")
                        
                        self.printEmbassyDebug()
                        self.printPlotsDebug()
                        self.printStabilityDebug()


                if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_E) and self.eventManager.bAlt and self.eventManager.bShift):
                        print("SHIFT-ALT-E") #picks a dead civ so that autoplay can be started with game.AIplay xx
                        iDebugDeadCiv = iCarthage #default iEthiopia: always dead in 600AD
                        # 3Miro: not sure
                        #gc.getTeam(gc.getPlayer(iDebugDeadCiv).getTeam()).setHasTech(con.iCalendar, True, iDebugDeadCiv, False, False)
                        utils.makeUnit(con.iAxeman, iDebugDeadCiv, (0,0), 1)
                        gc.getGame().setActivePlayer(iDebugDeadCiv, False)
                        gc.getPlayer(iDebugDeadCiv).setPlayable(True)
                        
                        
                #Rhye - end debug
        
        #Mercenaries - end



        #Rhye - start
        def printDebug(self, iGameTurn):

                
                #if (iGameTurn %10 == 1):
                #        self.printEmbassyDebug()

                #if (iGameTurn %5 == 0):
                #        self.printPlotsDebug()

                #if (iGameTurn %5 == 0): 
                #        self.printStabilityDebug()
                pass


                        
        def printPlotsDebug(self):

##                for i in range(124):
##                        for j in range(68):
##                                print (i, j, gc.getMap().plot(i,j).getArea())
            
                #countTotalUnits
                iTotal = 0
                iTotalCities = 0
##                lType = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
##                lOwner = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                
                #lOwnerLongbow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #         0, 0, 0, 0, 0, 0, 0]
                #lOwnerCannon = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #         0, 0, 0, 0, 0, 0, 0]
##                lPlotOwner = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0]
                #lPlotOwner2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0]
##                lCityOwner2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0]
                #lCityOwner_sb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0]
                for x in range(0, 123):
                        for y in range(0, 67):
                                pCurrent = gc.getMap().plot( x, y )
                                iTotal += pCurrent.getNumUnits()
##                                if (pCurrent.getNumUnits() > 0):
##                                        for i in range (pCurrent.getNumUnits()):
##                                                unit = pCurrent.getUnit(i)
##                                                lType[unit.getUnitType()] += 1
##                                                lOwner[unit.getOwner()] += 1
                                                #if (unit.getUnitType() == con.iLongbowman):
                                                #       lOwnerLongbow[unit.getOwner()] += 1
                                                #if (unit.getUnitType() == con.iCannon):
                                                #       lOwnerCannon[unit.getOwner()] += 1

                                if ( pCurrent.isCity()):
                                        iTotalCities += 1
                                        
                print ("TOTAL UNITS", iTotal)  
                print ("TOTAL CITIES", iTotalCities)

##                print ("Unit types")
##                for i in range (len(lType)):
##                        print (i, lType[i])
##                print ("Unit owners")
##                for i in range (len(lOwner)):
##                        print (i, lOwner[i])
                #print ("LB owners")
                #for j in range (len(lOwnerLongbow)):
                #        print (j, lOwnerLongbow[j])               
                #print ("Cannon owners")
                #for j in range (len(lOwnerCannon)):
                #        print (j, lOwnerCannon[j])               
        
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

	def AI_unitUpdate( self ):
		print( " Update the Unit AI ")
