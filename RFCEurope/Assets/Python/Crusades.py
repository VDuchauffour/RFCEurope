## This file is part of RFC Europe. Created by 3Miro

from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup
import cPickle as pickle
import RFCUtils
import Consts as con
import XMLConsts as xml
import RFCEMaps as rfceMaps
import CityNameManager

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()
cnm = CityNameManager.CityNameManager()

iNumCrusades = con.iNumCrusades
iJerusalem = con.iJerusalem
iCatholicism = xml.iCatholicism
iOrthodoxy = xml.iOrthodoxy
iIslam = xml.iIslam
iNumReligions = xml.iNumReligions

ProvMap = rfceMaps.tProinceMap

# tDefensiveCrusadeMap, can call DC, if at war with Non-Catholic and Non-Orthodox player, who isn't vassal of Catholic or Orthodox player and has at least one city in the provinces listed here
tDefensiveCrusadeMap = [
[], #tByzantium
[xml.iP_IleDeFrance,xml.iP_Aquitania,xml.iP_Orleans,xml.iP_Champagne,xml.iP_Bretagne,xml.iP_Normandy,xml.iP_Provence,xml.iP_Flanders,xml.iP_Burgundy,xml.iP_Picardy], #tFrance
[], #tArabia
[], #tBulgaria
[xml.iP_Leon,xml.iP_GaliciaSpain,xml.iP_Aragon,xml.iP_Catalonia,xml.iP_Castile,xml.iP_Andalusia,xml.iP_Valencia], #tCordoba (for consistency)
[], #tNorse
[xml.iP_Verona, xml.iP_Tuscany, xml.iP_Carinthia, xml.iP_Dalmatia], #tVenecia
[xml.iP_Flanders, xml.iP_Provence, xml.iP_Burgundy, xml.iP_Champagne, xml.iP_Lorraine,xml.iP_Picardy], #tBurgundy
[xml.iP_Lorraine, xml.iP_Swabia, xml.iP_Bavaria, xml.iP_Saxony, xml.iP_Franconia, xml.iP_Flanders, xml.iP_Brandenburg, xml.iP_Bohemia], #tGermany
[], #tKiev
[xml.iP_Hungary, xml.iP_Transylvania, xml.iP_UpperHungary, xml.iP_Wallachia, xml.iP_Slavonia, xml.iP_Pannonia, xml.iP_Austria], #tHungary
[xml.iP_Leon,xml.iP_GaliciaSpain,xml.iP_Aragon,xml.iP_Catalonia,xml.iP_Castile,xml.iP_Andalusia,xml.iP_Valencia], #tSpain
[xml.iP_GreaterPoland, xml.iP_LesserPoland, xml.iP_Silesia, xml.iP_Pomerania, xml.iP_Masovia, xml.iP_GaliciaPoland], #tPoland
[xml.iP_Lombardy, xml.iP_Corsica, xml.iP_Sardinia, xml.iP_Tuscany], #tGenoa
[], #tEngland
[xml.iP_Leon,xml.iP_GaliciaSpain,xml.iP_Aragon,xml.iP_Catalonia,xml.iP_Castile,xml.iP_Andalusia,xml.iP_Valencia], #tPortugal
[], #tLithuania
[xml.iP_Austria, xml.iP_Bavaria, xml.iP_Bohemia, xml.iP_Moravia], #tAustria
[], #tTurkey
[], #tMoscow
[], #tSweden
[], #tDutch
[] #tRome
];


class Crusades:
	
###############
### Popups 3Miro: taken from RFC Congress ###
#############

	def getCrusadeInit( self, iCrusade ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lCrusadeInit'][iCrusade]
                
	def setCrusadeInit( self, iCrusade, iNewCode ):
		# codes are: -2, no crusade yet, 
		#-1 crusade is active but waiting to start (Holy City is Christian and/or another Crusade in progress)
		# 0 or more, the turn when it was initialized
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lCrusadeInit'][iCrusade] = iNewCode
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    
                
        def addSelectedUnit( self, iUnitPlace ):
        	scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lSelectedUnits'][iUnitPlace] += 1
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
        
        def setSelectedUnit( self, iUnitPlace, iNewNumber ):
        	scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lSelectedUnits'][iUnitPlace] = iNewNumber
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
        
        def getSelectedUnit( self, iUnitPlace ):
	        scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lSelectedUnits'][iUnitPlace]

	def getActiveCrusade( self, iGameTurn ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		for i in range( iNumCrusades ):
			iInit = scriptDict['lCrusadeInit'][i] 
			if ( iInit > -1 and iInit + 7 > iGameTurn ):
				return i
		return -1
		
	def getParticipate( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['bParticipate']

	def setParticipate( self, bVal ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['bParticipate'] = bVal
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    
	
	def getVotingPower( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lVotingPower'][iCiv]
	
	def setVotingPower( self, iCiv, iVotes ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lVotingPower'][iCiv] = iVotes
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    
                
        def getCrusadePower( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iCrusadePower']
        	
        def setCrusadePower( self, iPower ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iCrusadePower'] = iPower
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    
        	        
        def getFavorite( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iFavorite']
        	
        
        def setFavorite( self, iFavorite ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iFavorite'] = iFavorite
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getPowerful( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iPowerful']
        
        def setPowerful( self, iPowerful ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iPowerful'] = iPowerful
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )        
                
        def getLeader( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iLeader']
        	
        def setLeader( self, iLeader ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iLeader'] = iLeader
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )        
	
	def getVotesGatheredFavorite( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lVotesGathered'][0]
	
	def setVotesGatheredFavorite( self, iVotes ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lVotesGathered'][0] = iVotes
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    
	
	def getVotesGatheredPowerful( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lVotesGathered'][1]
	
	def setVotesGatheredPowerful( self, iVotes ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lVotesGathered'][1] = iVotes
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    
                
        def getRichestCatholic( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iRichestCatholic']
        
        def setRichestCatholic( self, iPlayer ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iRichestCatholic'] = iPlayer
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    
	
	def getIsTarget( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lDeviateTargets'][iCiv]
	
	def setIsTarget( self, iCiv, bTarget ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lDeviateTargets'][iCiv] = bTarget
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    
 
 	def getTargetX( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iTarget'][0]
 	
 	def getTargetY( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iTarget'][1]
 	
 	def setTarget( self, iX, iY ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iTarget'] = [ iX, iY ]
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    

	def hasSucceeded( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		iSucc = scriptDict['iCrusadeSucceeded']
		iTest = iSucc == 1
                return iTest
        
        def setSucceeded( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iCrusadeSucceeded'] = 1
                gc.getGame().setScriptData( pickle.dumps(scriptDict) ) 
                
	def isDCEnabled( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['bDCEnabled']
                
	def setDCEnabled( self, bNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['bDCEnabled'] = bNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    

	def getDCLast( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iDCLast']
                
	def setDCLast( self, iLast ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iDCLast'] = iLast
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )    

        ''' popupID has to be a registered ID in CvRhyesCatapultEventManager.__init__!! '''
        def showPopup(self, popupID, title, message, labels):
                popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
                popup.setHeaderString(title)
                popup.setBodyString(message)
                for i in labels:
                    popup.addButton( i )
                popup.launch(False)
		
	def initVotePopup( self ):
		self.showPopup( 7616, CyTranslator().getText("TXT_KEY_CRUSADE_INIT_POPUP", ()), CyTranslator().getText("TXT_KEY_CRUSADE_INIT", ()), \
		(CyTranslator().getText("TXT_KEY_CRUSADE_ACCEPT", ()),CyTranslator().getText("TXT_KEY_CRUSADE_DENY", ())) )
		
	def informLeaderPopup( self ):
		self.showPopup( 7617, CyTranslator().getText("TXT_KEY_CRUSADE_LEADER_POPUP", ()), gc.getPlayer( self.getLeader() ).getName() + CyTranslator().getText("TXT_KEY_CRUSADE_LEAD", ()), (CyTranslator().getText("TXT_KEY_CRUSADE_OK", ()),) )
		
	def voteHumanPopup( self ):
		self.showPopup( 7618, CyTranslator().getText("TXT_KEY_CRUSADE_VOTE_POPUP", ()), CyTranslator().getText("TXT_KEY_CRUSADE_VOTE", ()), \
			( gc.getPlayer( self.getFavorite() ).getName(), gc.getPlayer( self.getPowerful() ).getName() ) )
			
	def deviateHumanPopup( self ):
		#iCost = gc.getPlayer( con.iPope ).getGold() / 3
		iCost = gc.getPlayer( utils.getHumanID() ).getGold() / 4 
		sString = CyTranslator().getText("TXT_KEY_CRUSADE_RICHEST", ()) + CyTranslator().getText("TXT_KEY_CRUSADE_COST", ()) + " " + str(iCost) + " " + CyTranslator().getText("TXT_KEY_CRUSADE_GOLD", ()) + gc.getPlayer( self.getLeader() ).getName() + " " + CyTranslator().getText("TXT_KEY_CRUSADE_CURRENT_LEADER", ())
		self.showPopup( 7619, CyTranslator().getText("TXT_KEY_CRUSADE_DEVIATE", ()), sString, \
			( CyTranslator().getText("TXT_KEY_CRUSADE_DECIDE_WEALTH", ()), CyTranslator().getText("TXT_KEY_CRUSADE_DECIDE_FAITH", ()) ) )
	
	def deviateNewTargetPopup( self ):
		lTargetList = []
		lTargetList.append( gc.getMap().plot( iJerusalem[0], iJerusalem[1] ).getPlotCity().getName() + " (" + gc.getPlayer( gc.getMap().plot( iJerusalem[0], iJerusalem[1] ).getPlotCity().getOwner() ).getCivilizationAdjective(0) + ")" )
		for iPlayer in range( con.iNumPlayers ):
			pPlayer = gc.getPlayer( iPlayer )
			if ( iPlayer == con.iPope or iPlayer == con.iPope or pPlayer.getStateReligion() == iCatholicism or ( not pPlayer.isAlive() ) ):
				self.setIsTarget( iPlayer, False )
			else:
				self.setIsTarget( iPlayer, True )
				lTargetList.append( pPlayer.getCapitalCity().getName() + " (" + pPlayer.getCivilizationAdjective(0) + ")" )
		self.showPopup( 7620, CyTranslator().getText("TXT_KEY_CRUSADE_CORRUPT", ()), CyTranslator().getText("TXT_KEY_CRUSADE_TARGET", ()), lTargetList )
			
	def underCrusadeAttackPopup( self, sCityName, iLeader ):
		sText = CyTranslator().getText("TXT_KEY_CRUSADE_UNDER_ATTACK1", (gc.getPlayer(iLeader).getCivilizationAdjective(0), gc.getPlayer(iLeader).getName(), sCityName))
		self.showPopup( 7621, CyTranslator().getText("TXT_KEY_CRUSADE_ATTACK", ()), sText, (CyTranslator().getText("TXT_KEY_CRUSADE_OK", ()),) )
	
	def endCrusades(self):
		for i in range( iNumCrusades ):
			if ( self.getCrusadeInit( i ) < 0 ):
				self.setCrusadeInit( i, 0 )
		
	def checkTurn( self, iGameTurn ):
		#print(" 3Miro Crusades ")
		#self.informPopup()
		
		if ( iGameTurn == xml.i1099AD - 6 ): #1080AD to arrive 1099AD
			self.setCrusadeInit( 0, -1 )
		if ( iGameTurn >= xml.i1147AD - 6 and self.getCrusadeInit( 0 ) > 0 and self.getCrusadeInit(1) == -2 ): # to arrive 1147AD
			self.setCrusadeInit( 1, -1 )
		if ( iGameTurn >= xml.i1187AD - 6 and self.getCrusadeInit( 1 ) > 0 and self.getCrusadeInit(2) == -2 ): # to arrive 1187AD
			self.setCrusadeInit( 2, -1 )
		if ( iGameTurn >= xml.i1202AD - 6 and self.getCrusadeInit( 2 ) > 0 and self.getCrusadeInit(3) == -2 ): # to arrive 1202AD
			self.setCrusadeInit( 3, -1 )
		if ( iGameTurn >= xml.i1229AD - 6 and self.getCrusadeInit( 3 ) > 0 and self.getCrusadeInit(4) == -2 ): # to arrive 1229AD
			self.setCrusadeInit( 4, -1 )
		
		#if ( iGameTurn == 50 ): #debug
		if ( iGameTurn == xml.i1000AD ): # indulgances for the Reconquista given by the Catholic Church 1000AD
			self.setDCEnabled( True )
			
		if ( self.isDCEnabled() ):
			self.doDC( iGameTurn )
		
		self.checkToStart( iGameTurn )
		
		iActiveCrusade = self.getActiveCrusade( iGameTurn )
		if ( iActiveCrusade > -1 ):
			iStartDate = self.getCrusadeInit( iActiveCrusade )
			if ( iStartDate == iGameTurn ):
				self.doParticipation( iGameTurn )
				
			if ( iStartDate + 1 == iGameTurn ):
				self.computeVotingPower( iGameTurn )
				self.setCrusaders()
				for i in range( 6 ):
					self.setSelectedUnit( i, 0 )
				for iPlayer in range( con.iNumPlayers ):
					if ( self.getVotingPower( iPlayer ) > 0 ):
						self.sendUnits( iPlayer )
				if ( not self.anyParticipate() ):
					return
				self.chooseCandidates( iGameTurn )
				self.voteForCandidatesAI()
				self.voteForCandidatesHuman()
				#print("  Votes are: ",self.getVotesGatheredFavorite(), self.getVotesGatheredPowerful() )
				
			if ( iStartDate + 2 == iGameTurn ):
				if ( not self.anyParticipate() ):
					return
				self.selectVoteWinner()
				self.decideTheRichestCatholic( iActiveCrusade )
				if ( self.getRichestCatholic() == utils.getHumanID() ):
					self.decideDeviateHuman()
				else:
					self.decideDeviateAI()
					
			if ( iStartDate + 5 == iGameTurn ):
				if ( not self.anyParticipate() ):
					return
				print( " Arival " )
				self.crusadeArrival()
				
			if ( iStartDate + 6 == iGameTurn ):
				self.returnCrusaders()
		
	def checkToStart( self, iGameTurn ):
	# if Jerusalem is Islamic or Pagan, Crusade has been initialized and it has been at least 5 turns since the last crusade and there are any Catholics, begin crusade
		pJPlot = gc.getMap().plot( iJerusalem[0], iJerusalem[1] )
		for i in range( iNumCrusades ): # check the Crusades
			if ( self.getCrusadeInit( i ) == -1 ): # if this one is to start
				if ( pJPlot.isCity() and self.anyCatholic() ): # if there is Jerusalem and there are any Catholics
					#Sedna17 -- allowing crusades against independent Jerusalem 
					#if ( pJPlot.getPlotCity().getOwner() < con.iNumMajorPlayers ): # if Jerusalem is not Independent
					#iTJerusalem = gc.getTeam( gc.getPlayer( gc.getMap().plot( iJerusalem[0], iJerusalem[1] ).getPlotCity().getOwner() ).getTeam() )
					iVictim = pJPlot.getPlotCity().getOwner() # get the information for the potential Victim
					pVictim = gc.getPlayer( iVictim )
					teamVictim = gc.getTeam( pVictim.getTeam() )
					iVictimReligion = pVictim.getStateReligion()
					if ( (iVictimReligion != iCatholicism and iVictimReligion != iOrthodoxy) or (pJPlot.getPlotCity().getOwner() > con.iNumMajorPlayers) ): # if the Victim is non-Catholic non-Orthodox
						bVassalOfImmune = False
						for iPlayerMaster in range( con.iNumMajorPlayers ): # for all the players, check to see if the Vicitm is a Vassal of a Catholic or Orthodox player
							pMaster = gc.getPlayer( iPlayerMaster )	    # they are immune from Crusades
							iTMaster = pMaster.getTeam()
							if ( iPlayerMaster != iVictim and teamVictim.isVassal( iTMaster ) ):
								iMasterReligion = pMaster.getStateReligion()
								if ( iMasterReligion == iOrthodoxy or iMasterReligion == iCatholicism ):
									bVassalOfImmune = True
						
						if ( (not bVassalOfImmune) and (i == 0 or ( self.getCrusadeInit( i-1 ) > -1 and self.getCrusadeInit( i-1 ) + 8 < iGameTurn ) ) ):
							self.setCrusadeInit( i, iGameTurn )
							print( "Crusade Starting Turn ",iGameTurn )
								
	def anyCatholic( self ):
		for i in range( con.iNumPlayers ):
			if ( not ( i == con.iPope ) ):
				if ( gc.getPlayer(i).getStateReligion() == iCatholicism ):
					return True
		return False
		
	def anyParticipate( self ):
		for i in range( con.iNumPlayers ):
			if ( not ( i == con.iPope ) ):
				if ( self.getVotingPower( i ) > 0 ):
					return True
		return False	
	
	def eventApply7616( self, popupReturn ):
		if ( popupReturn.getButtonClicked() == 0 ):
			self.setParticipate( True )
			gc.getPlayer( utils.getHumanID() ).setIsCrusader( True )
			print("  Going on a Crusade " )
		else:
			self.setParticipate( False )
			iHuman = utils.getHumanID()
			pPlayer = gc.getPlayer( iHuman )
			pPlayer.setIsCrusader( False )
			pPlayer.changeFaith( - min( 5, pPlayer.getFaith() ) )
			gc.getPlayer( con.iPope ).AI_changeMemoryCount( iHuman, MemoryTypes.MEMORY_REJECTED_DEMAND, 2 )
			#3Miro: put penalty for not going to the crusade
			
	def eventApply7618( self, popupReturn ):
		if ( popupReturn.getButtonClicked() == 0 ):
			self.setVotesGatheredFavorite( self.getVotesGatheredFavorite() + self.getVotingPower( utils.getHumanID() ) )
		else:
			self.setVotesGatheredPowerful( self.getVotesGatheredPowerful() + self.getVotingPower( utils.getHumanID() ) )
	
	def eventApply7619( self, popupReturn ):
		if ( popupReturn.getButtonClicked() == 0 ):
			iHuman = utils.getHumanID()
			pHuman = gc.getPlayer( iHuman )
			#pHuman.setGold( pHuman.getGold() - gc.getPlayer( utils.getHumanID() ).getGold() / 4 )
			pHuman.setGold( pHuman.getGold() - pHuman.getGold() / 4 )
			self.setLeader( iHuman )
			self.setCrusadePower( self.getCrusadePower() / 2 )
			self.deviateNewTargetPopup()
		else:
			self.setTarget( iJerusalem[0], iJerusalem[1] )
			self.startCrusade()
			
	def eventApply7620( self, popupReturn ):
		iDecision = popupReturn.getButtonClicked()
		if ( iDecision == 0 ):
			self.setTarget( iJerusalem[0], iJerusalem[1] )
			self.startCrusade()
			return
		iTargets = 0
		#print(" 3Miro Deviate Crusade: ",iDecision )
		for i in range( con.iNumPlayers ):
			if ( self.getIsTarget( i ) ):
				iTargets += 1
			if ( iTargets == iDecision ):
				pTargetCity = gc.getPlayer( i ).getCapitalCity()
				self.setTarget( pTargetCity.getX(), pTargetCity.getY() )
				iDecision = -2
		
		self.startCrusade()
	
	def doParticipation( self, iGameTurn ):
		iHuman = utils.getHumanID()
		#print(" 3Miro Crusades doPart", iHuman, iGameTurn )
		if ( con.tBirth[iHuman] < iGameTurn ):
			pHuman = gc.getPlayer( iHuman )
			if ( pHuman.getStateReligion() != iCatholicism ):
				self.setParticipate( False )
				CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_CRUSADE_CALLED", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
				#print(" 3Miro Crusades not Catholic: " )
			else:
				#print(" 3Miro Crusades not Vote ")
				self.initVotePopup()	
		else:
			self.setParticipate( False )
		
	def chooseCandidates( self, iGameTurn ):
		bFound = False
		iFavorite = 0
		iFavor = 0
		for i in range( con.iNumPlayers ):
			if ( not ( i == con.iPope ) ):
				if ( self.getVotingPower( i ) > 0 ):
					if ( bFound ):
						iNFavor = gc.getRelationTowards( con.iPope, i )
						if ( iNFavor > iFavor ):
							iNFavor = iFavor
							iFavorite = i
					else:
						iFavor = gc.getRelationTowards( con.iPope, i )
						iFavorite = i
						bFound = True
		self.setFavorite( iFavorite )
		
		iPowerful = iFavorite
		iPower = self.getVotingPower( iPowerful )
		
		for i in range( con.iNumPlayers ):
			if ( not ( i == con.iPope ) ):
				if ( self.getVotingPower( i ) > iPower or ( iPowerful == iFavorite and self.getVotingPower( i ) > 0 ) ):
					iPowerful = i
					iPower = self.getVotingPower( iPowerful )
				
		print( " Candidates ",iFavorite,iPowerful )
		print( "  voting power is: ",self.getVotingPower(0), self.getVotingPower(1), self.getVotingPower(2) )
		if ( iPowerful == iFavorite ):
			self.setPowerful( -1 )
		else:
			self.setPowerful( iPowerful )
					
		
		
	def computeVotingPower( self, iGameTurn ):
		#teamJerusalem = gc.getTeam( gc.getPlayer( gc.getMap().plot( iJerusalem[0], iJerusalem[1] ).getPlotCity().getOwner() ).getTeam() )
		#pPJerusalem = gc.getPlayer( gc.getMap().plot( iJerusalem[0], iJerusalem[1] ).getPlotCity().getOwner() )
		#iPJerusalem = gc.getMap().plot( iJerusalem[0], iJerusalem[1] ).getPlotCity().getOwner()
		iTJerusalem = gc.getPlayer( gc.getMap().plot( iJerusalem[0], iJerusalem[1] ).getPlotCity().getOwner() ).getTeam()
		
		for iPlayer in range( con.iNumPlayers ):
			pPlayer = gc.getPlayer( iPlayer )
			if ( (con.tBirth[iPlayer] > iGameTurn) or (not pPlayer.isAlive()) or (pPlayer.getStateReligion() != iCatholicism) or ( gc.getTeam( pPlayer.getTeam() ).isVassal( iTJerusalem ) )  ):
				self.setVotingPower( iPlayer, 0 )
			else:
				self.setVotingPower( iPlayer, pPlayer.getVotingPower( iCatholicism ) )	
				
		iHuman = utils.getHumanID()
		if ( not self.getParticipate() ):
			self.setVotingPower( iHuman, 0 )
			
		# the Pope has tripple votes (Rome is small anyway)
		self.setVotingPower( con.iPope, 3*self.getVotingPower( con.iPope ) )
		
		iPower = 0
		for iPlayer in range( con.iNumPlayers ):
			iPower += self.getVotingPower( iPlayer )
			
		self.setCrusadePower( iPower )
			
			
	def setCrusaders( self ):
		iHuman = utils.getHumanID()
		#teamJerusalem = gc.getTeam( gc.getPlayer( gc.getMap().plot( iJerusalem[0], iJerusalem[1] ).getPlotCity().getOwner() ).getTeam() )
		for iPlayer in range( con.iNumPlayers ):
			if ( (not iPlayer == iHuman) and self.getVotingPower( iPlayer ) > 0 ):
				gc.getPlayer( iPlayer ).setIsCrusader( True )
	
	def sendUnits( self, iPlayer ):
		#iHuman = utils.getHumanID()
		pPlayer = gc.getPlayer( iPlayer )
		iNumUnits = pPlayer.getNumUnits()
		if ( con.tBirth[iPlayer] + 20 > gc.getGame().getGameTurn() ):
			iMaxToSend = min( 10, max( 2, (5*iNumUnits) / 100 ) )
		else:
			iMaxToSend = min( 10, max( 1, (5*iNumUnits) / 100 ) )
		iCrusadersSend = 0
		for i in range( iNumUnits ):
			pUnit = pPlayer.getUnit( i )
			if ( (not pUnit.isHasPromotion( con.iMercPromotion )) and (not pUnit.isHasPromotion( xml.iPromotionLeader )) ):
				iCrusadeCategory = self.unitCrusadeCategory( pUnit.getUnitType() )
				if ( iCrusadeCategory < 3 ):
					pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
					if ( pPlot.isCity() ):
						#if ( pPlot.getNumUnits() > 2 ):
						if ( self.getNumDefendersAtPlot( pPlot ) > 3 ):
							iRandNum = gc.getGame().getSorenRandNum(100, 'roll to send special Unit to Crusade')
							if ( iCrusadeCategory < 3 and iRandNum < 90 ):
								iCrusadersSend += 1
								self.sendUnit( pUnit )
							elif ( iRandNum < 50 ):
								iCrusadersSend += 1
								self.sendUnit( pUnit )
					else:
						iRandNum = gc.getGame().getSorenRandNum(100, 'roll to send special Unit to Crusade')
						if ( iCrusadeCategory < 3 and iRandNum < 90 ):
							iCrusadersSend += 1
							self.sendUnit( pUnit )
						elif ( iRandNum < 50 ):
							iCrusadersSend += 1
							self.sendUnit( pUnit )
					if ( iCrusadersSend == iMaxToSend ):
						return
			
		for i in range( 20 ):
			iRandUnit = gc.getGame().getSorenRandNum(iNumUnits, 'roll to pick Unit for Crusade')
			pUnit = pPlayer.getUnit( iRandUnit )
			pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
			if ( not pUnit.isHasPromotion( con.iMercPromotion ) ):
				if ( pPlot.isCity() ):
					#if ( pPlot.getNumUnits() > 2 ):
					if ( self.getNumDefendersAtPlot( pPlot ) > 3 ):
						if ( gc.getGame().getSorenRandNum(100, 'roll to send Unit to Crusade') < self.unitProbability( pUnit.getUnitType() ) ):
							iCrusadersSend += 1
							self.sendUnit( pUnit )
				else:
					if ( gc.getGame().getSorenRandNum(100, 'roll to send Unit to Crusade') < self.unitProbability( pUnit.getUnitType() ) ):
						iCrusadersSend += 1
						self.sendUnit( pUnit )
				if ( iCrusadersSend == iMaxToSend ):
					break
	def getNumDefendersAtPlot( self, pPlot ):
		iOwner = pPlot.getOwner()
		if ( iOwner < 0 ):
			return 0
		iNumUnits = pPlot.getNumUnits()
		iDefenders = 0
		for i in range( iNumUnits ):
			if ( pPlot.getUnit(i).getOwner() == iOwner ):
				iDefenders += 1
		return iDefenders
		
			
	def sendUnit( self, pUnit ):
		iHuman = utils.getHumanID()
		iOwner = pUnit.getOwner()
		self.addSelectedUnit( self.unitCrusadeCategory( pUnit.getUnitType() ) )
		self.setVotingPower( iOwner, self.getVotingPower( iOwner ) + 2 )
		if ( iOwner == iHuman ):
			CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_CRUSADE_LEAVE", ()) + " " + pUnit.getName(), "AS2D_BUILD_CHRISTIAN", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
		pUnit.kill( 0, -1 )
				
	def unitProbability( self, iUnitType ):
		if ( iUnitType == xml.iArcher or iUnitType == xml.iCrossbowman or iUnitType == xml.iArbalest or iUnitType == xml.iGenoaBalestrieri or iUnitType == xml.iLongbowman or iUnitType == xml.iEnglishLongbowman or iUnitType == xml.iPortugalFootKnight ):
			return 33
		if ( iUnitType == xml.iHungarianLancer or iUnitType == xml.iLancer or iUnitType == xml.iCordobanBerber or iUnitType == xml.iHeavyLancer or iUnitType == xml.iArabiaGhazi or iUnitType == xml.iByzantineCataphract or iUnitType == xml.iKnight or iUnitType == xml.iMoscowBoyar or iUnitType == xml.iPolishWingedHussar or iUnitType == xml.iBurgundianPaladin ):
			return 66
		if ( iUnitType == xml.iTemplar or iUnitType == xml.iTeutonic ):
			return 90
		if ( iUnitType < xml.iArcher or iUnitType > xml.iFieldArtillery ): # Workers, Executives, Missionaries, Sea Units and Tagmata do not go
			return -1
		return 50
		
	def unitCrusadeCategory( self, iUnitType ):
		if ( iUnitType == xml.iTemplar ):
			return 0
		if ( iUnitType == xml.iTeutonic ):
			return 1
		if ( iUnitType == xml.iKnight or iUnitType == xml.iMoscowBoyar or iUnitType == xml.iPolishWingedHussar or iUnitType == xml.iBurgundianPaladin ):
			return 2
		if ( iUnitType == xml.iHeavyLancer or iUnitType == xml.iArabiaGhazi or iUnitType == xml.iByzantineCataphract or iUnitType == xml.iKievDruzhina ):
			return 3
		if ( iUnitType == xml.iCatapult or iUnitType == xml.iTrebuchet ):
			return 4
		return 5
					
			
	def voteForCandidatesAI( self ):
		iHuman = utils.getHumanID()
		if ( self.getPowerful() == -1 ):
			self.setLeader( self.getFavorite() )
			if ( self.getParticipate() ):
				self.informLeaderPopup()
			else:
				CyInterface().addMessage(iHuman, True, con.iDuration/2, gc.getPlayer( self.getLeader() ).getName() + CyTranslator().getText("TXT_KEY_CRUSADE_LEAD", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
			return
		
		iFavorite = self.getFavorite()
		iPowerful = self.getPowerful()
		if ( iFavorite == iHuman ):
			iFavorVotes = 0
		else:
			iFavorVotes = self.getVotingPower( iFavorite )
		if ( iPowerful == iHuman ):
			iPowerVotes = 0
		else:
			iPowerVotes = self.getVotingPower( iPowerful )
		
		#print( " AI Voting for self", iFavorVotes, iPowerVotes )
		
		for i in range( con.iNumPlayers ):
			iVotes = self.getVotingPower( i )
			if ( iVotes > 0 and ( not ( (i == iHuman) or (i == iFavorite) or (i == iPowerful) ) ) ):
				# vote AI
				#print( " AI now voting ",i,iVotes )
				if ( gc.getRelationTowards( i, iFavorite ) > gc.getRelationTowards( i, iPowerful ) ):
					iFavorVotes += iVotes
				else:
					iPowerVotes += iVotes
		
		print( " AI Voting ", iFavorVotes, iPowerVotes )
		
		self.setVotesGatheredFavorite( iFavorVotes )
		self.setVotesGatheredPowerful( iPowerVotes )
	
	def voteForCandidatesHuman( self ):
		if ( self.getParticipate() and ( not self.getPowerful() == -1 ) ):
			self.voteHumanPopup()
			
	def selectVoteWinner( self ):
		if ( self.getVotesGatheredPowerful() > self.getVotesGatheredFavorite() ):
			self.setLeader( self.getPowerful() )
		else:
			self.setLeader( self.getFavorite() )
			
		if ( self.getParticipate() ):
			self.informLeaderPopup()
		else:
			CyInterface().addMessage(utils.getHumanID(), True, con.iDuration/2, gc.getPlayer( self.getLeader() ).getName() + CyTranslator().getText("TXT_KEY_CRUSADE_LEAD", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
		
		# not yet, check to see for deviations
		#pJPlot = gc.getMap().plot( iJerusalem[0], iJerusalem[1] )
		#gc.getTeam( gc.getPlayer( self.getLeader() ) ).declareWar( pJPlot.getPlotCity().getOwner(), True, -1 )
		
		
	def decideTheRichestCatholic( self, iActiveCrusade ):
		iRichest = -1
		iMoney = 0
		#iPopeMoney = gc.getPlayer( con.iPope ).getGold()
		for i in range( con.iNumPlayers -1 ):
			pPlayer = gc.getPlayer( i )
			if ( self.getVotingPower( i ) > 0 ):
				iPlayerMoney = pPlayer.getGold()
				#if ( iPlayerMoney > iMoney and iPlayerMoney > iPopeMoney ):
				if ( iPlayerMoney > iMoney ):
					iRichest = i
					iMoney = iPlayerMoney
		
		if ( not iRichest == con.iPope ):
			self.setRichestCatholic( iRichest )
		else:
			self.setRichestCatholic( -1 )
			
		# The First Crusade cannot be deviated
		if ( iActiveCrusade == 0 ):
			self.setRichestCatholic( -1 )
	
	def decideDeviateHuman( self ):
		self.deviateHumanPopup()
	
	def decideDeviateAI( self ):
		iRichest = self.getRichestCatholic()
		bStolen = False
		#if ( iRichest == con.iVenecia or iRichest == con.iGenoa or iRichest == con.iFrankia ):
		if ( iRichest == con.iVenecia or iRichest == con.iGenoa ):
			pByzantium = gc.getPlayer( con.iByzantium )
			if ( pByzantium.isAlive() ):
				self.crusadeStolenAI( iRichest, con.iByzantium )
				bStolen = True
		if ( iRichest == con.iSpain ):
			pCordoba = gc.getPlayer( con.iCordoba )
			if ( pCordoba.isAlive() ):
				self.crusadeStolenAI( iRichest, con.iCordoba )
				bStolen = True
		if ( not bStolen ):
			self.setTarget( iJerusalem[0], iJerusalem[1] )
				
		self.startCrusade()		
			
	def crusadeStolenAI( self, iNewLeader, iNewTarget ):
		self.setLeader( iNewLeader )
		pLeader = gc.getPlayer( iNewLeader )
		CyInterface().addMessage(utils.getHumanID(), True, con.iDuration/2, pLeader.getName() + " " + CyTranslator().getText("TXT_KEY_CRUSADE_DEVIATED", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
		#pLeader.setGold( pLeader.getGold() - gc.getPlayer( con.iPope ).getGold() / 3 )
		#pLeader.setGold( gc.getPlayer( con.iPope ).getGold() / 4 )
		pLeader.setGold( 3* pLeader.getGold() / 4 )
		pTarget = gc.getPlayer( iNewTarget ).getCapitalCity()
		self.setTarget( pTarget.getX(), pTarget.getY() )
		self.setCrusadePower( self.getCrusadePower() / 2 )
		
		
	def startCrusade( self ):
		iHuman = utils.getHumanID()
		iLeader = self.getLeader()
		pTargetCity = gc.getMap().plot( self.getTargetX(), self.getTargetY() ).getPlotCity()
		iTargetPlayer = pTargetCity.getOwner()
                # Jerusalem can change ownership during the voting
                if ( gc.getPlayer( iTargetPlayer ).getStateReligion() == xml.iCatholicism ):
                        self.setLeader( -1 )
                        self.returnCrusaders()
                        return
                if ( iTargetPlayer == iHuman ):
			self.underCrusadeAttackPopup( pTargetCity.getName(), iLeader )
		else: 
                        sCityName = cnm.lookupName(pTargetCity,con.iPope)
                        if ( sCityName == 'Unknown' ):
                                sCityName = cnm.lookupName(pTargetCity,iLeader)
                        sText = CyTranslator().getText("TXT_KEY_CRUSADE_START", (gc.getPlayer(iLeader).getCivilizationAdjectiveKey(), gc.getPlayer(iLeader).getName(), gc.getPlayer(iTargetPlayer).getCivilizationAdjectiveKey(), sCityName))
                        CyInterface().addMessage(iHuman, True, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
		
		gc.getTeam( gc.getPlayer( iLeader ).getTeam() ).declareWar( gc.getPlayer( pTargetCity.getOwner() ).getTeam(), True, -1 )
		
		
	def returnCrusaders( self ):
		for i in range( con.iNumPlayers ):
			gc.getPlayer( i ).setIsCrusader( False )
		
	def crusadeArrival( self ):
		iTX = self.getTargetX()
		iTY = self.getTargetY()
		iChosenX = -1
		iChosenY = -1
                
                # if the leader has been destroyed, cancel the crusade
                iLeader = self.getLeader()
                if ( (iLeader>-1) and (not gc.getPlayer( iLeader ).isAlive()) ):
                        self.returnCrusaders()
                        return
		
                # if in the mean time Jerusalem has been captured by an Orthodox or Catholic player (and target is Jerusalem), cancel the Crusade
		if ( iTX == iJerusalem[0] and iTY == iJerusalem[1] ): # if the Terget is Jerusalem
			pPlot = gc.getMap().plot( iJerusalem[0], iJerusalem[1] )
			if ( pPlot.isCity() ): # and it is still there
				iVictim = pPlot.getPlotCity().getOwner() # get the Victim
				if ( iVictim < con.iNumMajorPlayers ): # if not Independent
					iReligion = gc.getPlayer( iVictim ).getStateReligion()
					if ( iReligion == iCatholicism or iReligion == iOrthodoxy ): # now controlled by Orthodox or Catholic (i.e. change of Religion)
						return
			
                # if not at war with the owener of the city, declare war
                pPlot = gc.getMap().plot( iTX, iTY )
                if ( pPlot.isCity() ):
                        iVictim = pPlot.getPlotCity().getOwner()
                        if ( iVictim != iLeader and gc.getPlayer(iVictim).getStateReligion() != xml.iCatholicism ):
                                teamLeader = gc.getTeam( gc.getPlayer(iLeader).getTeam() )
                                iTeamVictim = gc.getTeam( gc.getPlayer(iVictim).getTeam() ).getID()
                                if ( not teamLeader.isAtWar( iTeamVictim ) ):
                                        if ( teamLeader.canDeclareWar( iTeamVictim ) ):
                                                teamLeader.declareWar(iTeamVictim, True, -1)
                                        else:
                                                # we cannot declare war to the current owner of the target city
                                                self.returnCrusaders()
                                                return

		for y in range( 3 ):
			for x in range( 3 ):
				iX = iTX - x + 1 # try to spawn not across the river
				iY = iTY + y - 1
				if ( (iX>=0) and (iX<con.iMapMaxX) and (iY>=0) and (iY<con.iMapMaxY) ):
					pPlot = gc.getMap().plot( iX, iY )
					if ( pPlot.isHills() or pPlot.isFlatlands() ):
						if ( pPlot.getNumUnits() == 0 and (not pPlot.isCity()) ):
							iChosenX = iX
							iChosenY = iY
						
		if ( iChosenX == -1 ):
			for y in range( 3 ):
				for x in range( 3 ):
					iX = iTX + x - 1
					iY = iTY + y - 1
					if ( (iX>=0) and (iX<con.iMapMaxX) and (iY>=0) and (iY<con.iMapMaxY) ):
						pPlot = gc.getMap().plot( iX, iY )
						
						if ( pPlot.isHills or pPlot.isFlatlands() ):
							iN = pPlot.getNumUnits()
							for i in range( iN ):
								pPlot.getUnit( i ).kill( False, con.iBarbarian )
								iChosenX = iX
								iChosenY = iY
			
				print("Made Units on:", iChosenX, iChosenY,iLeader)	
                                
                if ( (iChosenX>=0) and (iChosenX<con.iMapMaxX) and (iChosenY>=0) and (iChosenY<con.iMapMaxY) ):
                        self.crusadeMakeUnits( [iChosenX,iChosenY] )
                else:
                        self.returnCrusaders()
		
        def makeUnit(self, iUnit, iPlayer, tCoords, iNum): #by LOQ
                'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
                pPlayer = gc.getPlayer(iPlayer)
                for i in range(iNum):
                        pUnit = pPlayer.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
                        pUnit.setMercID( -5 ) # 3Miro: this is a hack to distinguish Crusades without making a separate variable

		
	def crusadeMakeUnits( self, tPlot ):
		iLeader = self.getLeader()

		self.makeUnit( xml.iHeavyLancer, iLeader, tPlot, 2 )
		self.makeUnit( xml.iKnight, iLeader, tPlot, 3 )
		self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, 1 )
		self.makeUnit( xml.iSpearman, iLeader, tPlot, 1 )
		self.makeUnit( xml.iGuisarme, iLeader, tPlot, 1 )
		self.makeUnit( xml.iCatapult, iLeader, tPlot, 2 )
		self.makeUnit( xml.iTrebuchet, iLeader, tPlot, 1 )

		#print( " Crusade has Power ", self.getCrusadePower() )
		
		#print( " Crusade Templars : ",self.getSelectedUnit( 0 ) )
		#print( " Crusade Teutonic : ",self.getSelectedUnit( 1 ) )
		#print( " Crusade Knights  : ",self.getSelectedUnit( 2 ) )
		#print( " Crusade H Lancers: ",self.getSelectedUnit( 3 ) )
		#print( " Crusade Siege    : ",self.getSelectedUnit( 4 ) )
		#print( " Crusade Other    : ",self.getSelectedUnit( 5 ) )
		
		iTX = self.getTargetX()
		iTY = self.getTargetY()
		if ( iTX == iJerusalem[0] and iTY == iJerusalem[1] ): # if the Terget is Jerusalem
			iRougeModifier = 1
		else:
			iRougeModifier = 2
			
		if ( self.getSelectedUnit( 0 ) > 0 ):
			self.makeUnit( xml.iTemplar, iLeader, tPlot, self.getSelectedUnit( 0 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 1 ) > 0 ):
			self.makeUnit( xml.iTeutonic, iLeader, tPlot, self.getSelectedUnit( 1 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 2 ) > 0 ):
			if ( iLeader == con.iBurgundy ):
				self.makeUnit( xml.iBurgundianPaladin, iLeader, tPlot, self.getSelectedUnit( 2 ) / iRougeModifier  )
			else:
				self.makeUnit( xml.iKnight, iLeader, tPlot, self.getSelectedUnit( 2 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 3 ) > 0 ):
			self.makeUnit( xml.iHeavyLancer, iLeader, tPlot, self.getSelectedUnit( 3 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 4 ) > 0 ):
			self.makeUnit( xml.iCatapult, iLeader, tPlot, self.getSelectedUnit( 4 ) / iRougeModifier  )
			if ( self.getSelectedUnit( 4 ) > 3 ):
				self.makeUnit( xml.iTrebuchet, iLeader, tPlot, self.getSelectedUnit( 4 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 5 ) > 0 ):
			self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, self.getSelectedUnit( 5 ) / (10*iRougeModifier) )
			self.makeUnit( xml.iGuisarme, iLeader, tPlot, self.getSelectedUnit( 5 ) / (10*iRougeModifier)  )
			

		#if ( self.getCrusadePower() >  20 ):
		#	self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, 1 )
	
		#if ( self.getCrusadePower() > 40 ):
		#	self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, 1 )
		#	self.makeUnit( xml.iCatapult, iLeader, tPlot, 1 )
			
		#if ( self.getCrusadePower() > 50 ):
		#	self.makeUnit( xml.iLancer, iLeader, tPlot, 1 )
		#	
		#if ( self.getCrusadePower() > 60 ):
		#	#self.makeUnit( xml.iLancer, iLeader, tPlot, 1 )
		#	self.makeUnit( xml.iTrebuchet, iLeader, tPlot, 1 )
			
		#if ( self.getCrusadePower() > 70 ):
		#	self.makeUnit( xml.iLancer, iLeader, tPlot, 1 )
 
		#if ( self.getCrusadePower() > 90 ):
		#	self.makeUnit( xml.iKnight, iLeader, tPlot, 1 )
		#	self.makeUnit( xml.iTrebuchet, iLeader, tPlot, 1 )
        def freeCrusaders( self, iPlayer ):
                # this will kill the majority of Crusader units belonging to the player so that the Crusaders will have harder time keeping Jerusalem
                unitList = PyPlayer( iPlayer ).getUnitList()
                for pUnit in unitList:
                        if ( pUnit.getMercID() == -5 ):
                                # this is a Crusader Unit
                                pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
                                iOdds = 80
                                iCrusadeCategory = self.unitCrusadeCategory( pUnit.getUnitType() )
                                if ( iCrusadeCategory < 3 ):
                                        iOdds = -1 # Knight Orders don't return
                                elif ( iCrusadeCategory == 5 ):
                                        iOdds = 40 # leave some defenders
                                if ( iOdds > 0 and pPlot.isCity() ):
                                        if ( pPlot.getPlotCity().getOwner() == iPlayer ):
                                                iDefenders = self.getNumDefendersAtPlot( pPlot )
                                                if ( iDefenders < 4 ):
                                                        iOdds = 20
                                                        if ( iDefenders == 0 ):
                                                                iOdds = -1
                                                        
                                if ( gc.getGame().getSorenRandNum(100, 'free Crusaders') < iOdds ):
                                        pUnit.kill( 0, -1 )
                                        iHuman = utils.getHumanID()
                                        if ( iHuman == iPlayer ):
                                                CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_CRUSADE_RETURNING_AFTER_VICTORY", ()) + " " + pUnit.getName(), "", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                                                        
                                
		
	def success( self, iPlayer ):
                self.freeCrusaders( iPlayer )
		pPlayer = gc.getPlayer( iPlayer )
		if ( not self.hasSucceeded() ):
			pPlayer.changeGoldenAgeTurns( gc.getPlayer( iPlayer).getGoldenAgeLength() )
			self.setSucceeded()
			pCurrent = gc.getMap().plot( iJerusalem[0]-1, iJerusalem[1]-1 )
                        utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( iJerusalem[0]-1, iJerusalem[1] )
                        utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( iJerusalem[0]-1, iJerusalem[1]+1 )
                        utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( iJerusalem[0]+1, iJerusalem[1]+1 )
                        utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( iJerusalem[0]+1, iJerusalem[1] )
                        utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( iJerusalem[0]+1, iJerusalem[1]-1 )
                        utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( iJerusalem[0], iJerusalem[1]+1 )
                        utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( iJerusalem[0], iJerusalem[1]-1 )
                        utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
	
	def doDC( self, iGameTurn ):
                #print(" DC Check 1",iGameTurn,self.getDCLast())
		if ( iGameTurn < self.getDCLast() + 15 ): # wait 20 turns between DC (Defensive Crusades)
			return
		lPotentials = []
		#if ( iGameTurn % 3 != gc.getGame().getSorenRandNum(3, 'roll to see if we should DC')  ): # otherwise every turn gets too much to check
		#	return
                #print(" DC Check")
		for iPlayer in range( con.iNumPlayers - 1 ): # everyone except the Pope
			if ( self.canDC( iPlayer, iGameTurn ) ):
				lPotentials.append( iPlayer )
				#print(" Oh, Holy Father, ",iPlayer," needs help! ")
		iChosen = -1
		if ( len(lPotentials) > 0 ):
			#print(" Oh, Holy Father, someone needs help! " )
			pPope = gc.getPlayer( con.iPope )
			iCatholicFaith = 0
			for i in range( len(lPotentials) ):
				pPlayer = gc.getPlayer( lPotentials[i] )
				iCatholicFaith += pPlayer.getFaith() + pPope.AI_getAttitude( lPotentials[i] )
			#print(" Faith of the needy: ",iCatholicFaith )
			if ( iCatholicFaith > 0 ):
				iCatholicFaith += iCatholicFaith / 2 + 1
				iRandNum = gc.getGame().getSorenRandNum(iCatholicFaith, 'roll to pick Someone for DC')
				for i in range( len(lPotentials) ):
					pPlayer = gc.getPlayer( lPotentials[i] )
					iRandNum -= pPlayer.getFaith() + pPope.AI_getAttitude( lPotentials[i] )
					if ( iRandNum <= 0 ):
						iChosen = lPotentials[i]
						break
                #print(" DC Chosen ",iChosen)
		if ( iChosen > -1 ):
			iHuman = utils.getHumanID()
			if ( iChosen == iHuman ):
				self.callDCHuman()
			else:
				self.callDCAI( iChosen )
			self.setDCLast( iGameTurn )
				
				
				
	def canDC( self, iPlayer, iGameTurn ):
                #print(" DC Chech for player ",iPlayer,iGameTurn)
		pPlayer = gc.getPlayer( iPlayer )
		if ( (iGameTurn < con.tBirth[iPlayer]+5) or (not pPlayer.isAlive()) or pPlayer.getStateReligion() != iCatholicism ): 
		# only born, flipped and living Catholics can DC
			return False
		teamPlayer = gc.getTeam( pPlayer.getTeam() )
		if ( not teamPlayer.isOpenBorders( gc.getPlayer( con.iPope ).getTeam() ) ):
			return False
		#print( " Check to see if player can apply for DC ",iPlayer )
		#for iX in range( con.tNormalAreasTL[iPlayer][0], con.tNormalAreasBR[iPlayer][0] +1 ):
		#	for iY in range( con.tNormalAreasTL[iPlayer][1], con.tNormalAreasBR[iPlayer][1] +1 ):
		#		if ((iX,iY) not in con.tNormalAreasSubtract[iPlayer]):
		#			pPlot = gc.getMap().plot( iX, iY ) # plot in normal area
		#			if ( pPlot.isCity() ): # is a city
		#				pCity = pPlot.getPlotCity()
		#				print( " A city " )
		#				if ( pCity.getOwner() != iPlayer ): # owned by someone else
		#					print( " owned by enemy ",pCity.getName() )
		#					pEnemy = gc.getPlayer( pCity.getOwner() )
		#					iEnemyReligion = pEnemy.getStateReligion()
		#					if ( iEnemyReligion != iCatholicism and iEnemyReligion != iOrthodoxy ):
		#						print( " Enemy is an infidel " )
		#						# who is potential victim (i.e. infidel)
		#						if ( gc.getTeam( pPlayer.getTeam() ).isAtWar( pEnemy.getTeam() ) ):
		#							teamEnemy = gc.getTeam( pEnemy.getTeam() )
		#							print( " at war " )
		#							# check to see if Vassalized By Christians
		#							for iPotentialGuardian in range ( con.iNumPlayers ):
		#								pPotentialGuardian = gc.getPlayer( iPotentialGuardian )
		#								if ( pPotentialGuardian.isAlive() and teamEnemy.isVassal( pPotentialGuardian.getTeam() ) ):
		#									iGuardianReligion = pPotentialGuardian.getStateReligion()
		#									if ( iGuardianReligion != iCatholicism and iGuardianReligion != iOrthodoxy ):
		#										return True
		#for iEnemy in range( con.iNumPlayers ):
		#	pEnemy = gc.getPlayer( iEnemy )
		#	if ( teamPlayer.isAtWar( pEnemy.getTeam() ) and con.tBirth[iEnemy] + 10 < iGameTurn ):
		#		iEnemyReligion = pEnemy.getStateReligion()
		#		print( " Crusade condition war meet: ",iEnemy,iEnemyReligion )
		#		if ( iEnemyReligion != iCatholicism and iEnemyReligion != iOrthodoxy ):
		#			print( " Crusade condition Enemy Religion Meet: " )
		#			for pyCity in PyPlayer(iEnemy).getCityList():
		#				pCity = pyCity.GetCy()
		#				if ( rfceMaps.tWarsMaps[iPlayer][con.iMapMaxY-1-pCity.getY()][pCity.getX()] > 0 ):
		#					print( " Crusade War map condition meat: ",pCity.getName() )
		#					teamEnemy = gc.getTeam( pEnemy.getTeam() )
		#					bSafe = False
		#					for iPotentialGuardian in range ( con.iNumPlayers ):
		#						pPotentialGuardian = gc.getPlayer( iPotentialGuardian )
		#						#print( " Crusade potential guardian: ",iPotentialGuardian )
		#						if ( pPotentialGuardian.isAlive() and iPotentialGuardian != iEnemy and teamEnemy.isVassal( pPotentialGuardian.getTeam() ) ):
		#							iGuardianReligion = pPotentialGuardian.getStateReligion()
		#							#print( " Crusade has a guardian ",iGuardianReligion )
		#							if ( iGuardianReligion == iCatholicism or iGuardianReligion == iOrthodoxy ):
		#								#print( " Crusade guardian saves " )
		#								bSafe = True
		#					if ( not bSafe ):
		#						return True
                tPlayerDCMap = tDefensiveCrusadeMap[iPlayer]
                for iEnemy in range( con.iNumPlayers ):
			pEnemy = gc.getPlayer( iEnemy )
			if ( teamPlayer.isAtWar( pEnemy.getTeam() ) and con.tBirth[iEnemy] + 10 < iGameTurn ):
				iEnemyReligion = pEnemy.getStateReligion()
				#print( " Crusade condition war meet: ",iEnemy,iEnemyReligion )
				if ( iEnemyReligion != iCatholicism and iEnemyReligion != iOrthodoxy ):
					#print( " Crusade condition Enemy Religion Meet: " )
					for pyCity in PyPlayer(iEnemy).getCityList():
						pCity = pyCity.GetCy()
						if ( ProvMap[pCity.getY()][pCity.getX()] in tPlayerDCMap ):
							#print( " Crusade War map condition meat: ",pCity.getName() )
							teamEnemy = gc.getTeam( pEnemy.getTeam() )
							bSafe = False
							for iPotentialGuardian in range ( con.iNumPlayers ):
								pPotentialGuardian = gc.getPlayer( iPotentialGuardian )
								#print( " Crusade potential guardian: ",iPotentialGuardian )
								if ( pPotentialGuardian.isAlive() and iPotentialGuardian != iEnemy and teamEnemy.isVassal( pPotentialGuardian.getTeam() ) ):
									iGuardianReligion = pPotentialGuardian.getStateReligion()
									#print( " Crusade has a guardian ",iGuardianReligion )
									if ( iGuardianReligion == iCatholicism or iGuardianReligion == iOrthodoxy ):
										#print( " Crusade guardian saves " )
										bSafe = True
							if ( not bSafe ):
								return True
							
		return False
		
	def callDCHuman( self ):
		iHuman = utils.getHumanID()
		self.showPopup( 7625, CyTranslator().getText("TXT_KEY_CRUSADE_DEFENSIVE_PROPOSAL_POPUP", ()), CyTranslator().getText("TXT_KEY_CRUSADE_DEFENSIVE_PROPOSAL", ()), \
			( CyTranslator().getText("TXT_KEY_CRUSADE_DEFENSIVE_PROPOSAL_YES", ()), CyTranslator().getText("TXT_KEY_CRUSADE_DEFENSIVE_PROPOSAL_NO", ()) ) )
				
	def callDCAI( self, iPlayer ):
		iHuman = utils.getHumanID()
		pHuman = gc.getPlayer( iHuman )
		pPlayer = gc.getPlayer( iPlayer )
		if ( gc.getTeam( pHuman.getTeam() ).canContact( pPlayer.getTeam() ) or pHuman.getStateReligion() == iCatholicism ):
			sText = CyTranslator().getText("TXT_KEY_CRUSADE_DEFENSIVE_MESSAGE", ()) + " " + pPlayer.getName()
			CyInterface().addMessage(iHuman, True, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
		self.makeDCUnits( iPlayer )
		pPlayer.changeFaith( - min( 2, pPlayer.getFaith() ) )	
		
	def eventApply7625( self, popupReturn ):
		iDecision = popupReturn.getButtonClicked()
		iHuman = utils.getHumanID()
		pHuman = gc.getPlayer( iHuman )
		if ( iDecision == 0 ):
			self.makeDCUnits( iHuman )
			pHuman.changeFaith( - min( 2, pHuman.getFaith() ) )
		else:
			#pHuman.changeFaith( - min( 1, pHuman.getFaith() ) )
			pass
	
	def makeDCUnits( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		print(" Crusade Defensive for: ",pPlayer.getName() )
		iFaith = pPlayer.getFaith()
		iBestInfantry = self.getDCBestInfantry( iPlayer )
		iBestCavalry = self.getDCBestCavalry( iPlayer )
		pCapital = pPlayer.getCapitalCity()
		iX = pCapital.getX()
		iY = pCapital.getY()
		pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
                if ( pPlayer.getNumCities() < 6 ): # smaller Empires need a bit more help
                        pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 6 ):
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 12 ):
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 18 ):	
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 36 ):
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		# 2 extra cavalry for the AI, it is dumb anyway
		if ( not iPlayer == utils.getHumanID() ):
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					
	def getDCBestInfantry( self, iPlayer ):
		teamPlayer = gc.getTeam( gc.getPlayer( iPlayer ).getTeam() )
		if ( teamPlayer.isHasTech( xml.iNationalism ) and teamPlayer.isHasTech( xml.iChemistry ) ):
			return xml.iGrenadier
		if ( teamPlayer.isHasTech( xml.iCivilService ) and teamPlayer.isHasTech( xml.iMachinery ) ):
			return xml.iMaceman
		if ( teamPlayer.isHasTech( xml.iBlastFurnace ) ):
			return xml.iLongSwordsman
		if ( teamPlayer.isHasTech( xml.iChainMail ) ):
			return xml.iSwordsman
		return xml.iAxeman
		
	def getDCBestCavalry( self, iPlayer ):
		teamPlayer = gc.getTeam( gc.getPlayer( iPlayer ).getTeam() )
		if ( teamPlayer.isHasTech( xml.iMilitaryTactics ) ):
			return xml.iCuirassier
		if ( teamPlayer.isHasTech( xml.iChivalry ) ):
			return xml.iKnight
		if ( teamPlayer.isHasTech( xml.iFarriers ) and teamPlayer.isHasTech( xml.iFeudalism ) ):
			return xml.iHeavyLancer
		if ( teamPlayer.isHasTech( xml.iManorialism ) and teamPlayer.isHasTech( xml.iStirrup ) ):
			return xml.iLancer
		return xml.iScout
		
		
