## This file is part of RFC Europe. Created by 3Miro

from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup
import cPickle as pickle
import RFCUtils
import Consts as con
import RFCEMaps as rfceMaps
import CityNameManager

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()
cnm = CityNameManager.CityNameManager()

iNumCrusades = con.iNumCrusades
iJerusalem = con.iJerusalem
iCatholicism = con.iCatholicism
iOrthodoxy = con.iOrthodoxy
iIslam = con.iIslam
iNumReligions = con.iNumReligions

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
			
	def underCrusadeAttackPopup( self, sCityName ):
		sText = CyTranslator().getText("TXT_KEY_CRUSADE_UNDER_ATTACK1", ()) + " " + sCityName + " " + CyTranslator().getText("TXT_KEY_CRUSADE_UNDER_ATTACK2", ()) 
		self.showPopup( 7621, CyTranslator().getText("TXT_KEY_CRUSADE_ATTACK", ()), sText, (CyTranslator().getText("TXT_KEY_CRUSADE_OK", ()),) )
	
	def endCrusades(self):
		for i in range( iNumCrusades ):
			if ( self.getCrusadeInit( i ) < 0 ):
				self.setCrusadeInit( i, 0 )
		
	def checkTurn( self, iGameTurn ):
		#print(" 3Miro Crusades ")
		#self.informPopup()
		
		if ( iGameTurn == 160 ):
			self.setCrusadeInit( 0, -1 )
		if ( iGameTurn >= 182 and self.getCrusadeInit( 0 ) > 0 and self.getCrusadeInit(1) == -2 ):
			self.setCrusadeInit( 1, -1 )
		if ( iGameTurn >= 195 and self.getCrusadeInit( 1 ) > 0 and self.getCrusadeInit(2) == -2 ):
			self.setCrusadeInit( 2, -1 )
		if ( iGameTurn >= 201 and self.getCrusadeInit( 2 ) > 0 and self.getCrusadeInit(3) == -2 ):
			self.setCrusadeInit( 3, -1 )
		if ( iGameTurn >= 212 and self.getCrusadeInit( 3 ) > 0 and self.getCrusadeInit(4) == -2 ):
			self.setCrusadeInit( 4, -1 )
		
		#if ( iGameTurn == 50 ): #debug
		if ( iGameTurn == 133 ): # indulgances for the Reconquista given by the Catholic Church
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
					if ( pJPlot.getPlotCity().getOwner() < con.iNumMajorPlayers ): # if Jerusalem is not Independent
						#iTJerusalem = gc.getTeam( gc.getPlayer( gc.getMap().plot( iJerusalem[0], iJerusalem[1] ).getPlotCity().getOwner() ).getTeam() )
						iVictim = pJPlot.getPlotCity().getOwner() # get the information for the potential Victim
						pVictim = gc.getPlayer( iVictim )
						teamVictim = gc.getTeam( pVictim.getTeam() )
						iVictimReligion = pVictim.getStateReligion()
						if ( iVictimReligion != iCatholicism and iVictimReligion != iOrthodoxy ): # if the Victim is non-Catholic non-Orthodox
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
								print( " Crusade Starting Turn ",iGameTurn )
								
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
			if ( not pUnit.isHasPromotion( con.iMercPromotion ) ):
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
		if ( iUnitType == con.iArcher or iUnitType == con.iCrossbowman or iUnitType == con.iArbalest or iUnitType == con.iGenoaBalestrieri or iUnitType == con.iLongbowman or iUnitType == con.iEnglishLongbowman or iUnitType == con.iPortugalFootKnight ):
			return 33
		if ( iUnitType == con.iHungarianLancer or iUnitType == con.iLancer or iUnitType == con.iCordobanBerber or iUnitType == con.iHeavyLancer or iUnitType == con.iArabiaGhazi or iUnitType == con.iByzantineCataphract or iUnitType == con.iKnight or iUnitType == con.iMoscowBoyar or iUnitType == con.iPolishWingedHussar or iUnitType == con.iBurgundianPaladin ):
			return 66
		if ( iUnitType == con.iTemplar or iUnitType == con.iTeutonic ):
			return 90
		if ( iUnitType < con.iArcher or iUnitType > con.iFieldArtillery ): # Workers, Executives, Missionaries, Sea Units and Tagmata do not go
			return -1
		return 50
		
	def unitCrusadeCategory( self, iUnitType ):
		if ( iUnitType == con.iTemplar ):
			return 0
		if ( iUnitType == con.iTeutonic ):
			return 1
		if ( iUnitType == con.iKnight or iUnitType == con.iMoscowBoyar or iUnitType == con.iPolishWingedHussar or iUnitType == con.iBurgundianPaladin ):
			return 2
		if ( iUnitType == con.iHeavyLancer or iUnitType == con.iArabiaGhazi or iUnitType == con.iByzantineCataphract or iUnitType == con.iKievDruzhina ):
			return 3
		if ( iUnitType == con.iCatapult or iUnitType == con.iTrebuchet ):
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
		if ( iTargetPlayer == iHuman ):
			self.underCrusadeAttackPopup( pTargetCity.getName() )
		
		sCityName = cnm.lookupName(pTargetCity,con.iPope)
		if ( sCityName == 'Unknown' ):
			sCityName = cnm.lookupName(pTargetCity,iLeader)
		sText = CyTranslator().getText("TXT_KEY_CRUSADE_START1", ()) + " " + gc.getPlayer( iLeader ).getName() + " " + CyTranslator().getText("TXT_KEY_CRUSADE_START2", ()) + " " + sCityName + " " + CyTranslator().getText("TXT_KEY_CRUSADE_START3", ())
		#sText = CyTranslator().getText("TXT_KEY_CRUSADE_START1", ()) + " " + gc.getPlayer( iLeader ).getName() + " " + CyTranslator().getText("TXT_KEY_CRUSADE_START2", ()) + " " + cnm.lookupName(pTargetCity,con.iPope) + " " + CyTranslator().getText("TXT_KEY_CRUSADE_START3", ())
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
		#print("Target:", iTX, iTY)
		if ( iTX == iJerusalem[0] and iTY == iJerusalem[1] ): # if the Terget is Jerusalem
			pPlot = gc.getMap().plot( iJerusalem[0], iJerusalem[1] )
			if ( pPlot.isCity() ): # and it is still there
				iVictim = pPlot.getPlotCity().getOwner() # get the Victim
				if ( iVictim < con.iNumMajorPlayers ): # if not Independent
					iReligion = gc.getPlayer( iVictim ).getStateReligion()
					if ( iReligion == iCatholicism or iReligion == iOrthodoxy ): # now controlled by Orthodox or Catholic (i.e. change of Religion)
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
								pPlot.getUnit( i ).kill( False )
								iChosenX = iX
								iChosenY = iY
			
		self.crusadeMakeUnits( [iChosenX,iChosenY] )
		print("Made Units on:", iChosenX, iChosenY)
		
        def makeUnit(self, iUnit, iPlayer, tCoords, iNum): #by LOQ
                'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
                for i in range(iNum):
                        player = gc.getPlayer(iPlayer)
                        player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		
	def crusadeMakeUnits( self, tPlot ):
		iLeader = self.getLeader()
		self.makeUnit( con.iLancer, iLeader, tPlot, 1 )
		self.makeUnit( con.iKnight, iLeader, tPlot, 1 )
		self.makeUnit( con.iLongSwordsman, iLeader, tPlot, 1 )
		self.makeUnit( con.iSpearman, iLeader, tPlot, 1 )
		self.makeUnit( con.iGuisarme, iLeader, tPlot, 1 )
		self.makeUnit( con.iCatapult, iLeader, tPlot, 2 )
		self.makeUnit( con.iTrebuchet, iLeader, tPlot, 1 )

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
			self.makeUnit( con.iTemplar, iLeader, tPlot, self.getSelectedUnit( 0 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 1 ) > 0 ):
			self.makeUnit( con.iTeutonic, iLeader, tPlot, self.getSelectedUnit( 1 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 2 ) > 0 ):
			if ( iLeader == con.iBurgundy ):
				self.makeUnit( con.iBurgundianPaladin, iLeader, tPlot, self.getSelectedUnit( 2 ) / iRougeModifier  )
			else:
				self.makeUnit( con.iKnight, iLeader, tPlot, self.getSelectedUnit( 2 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 3 ) > 0 ):
			self.makeUnit( con.iHeavyLancer, iLeader, tPlot, self.getSelectedUnit( 3 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 4 ) > 0 ):
			self.makeUnit( con.iCatapult, iLeader, tPlot, self.getSelectedUnit( 4 ) / iRougeModifier  )
			if ( self.getSelectedUnit( 4 ) > 3 ):
				self.makeUnit( con.iTrebuchet, iLeader, tPlot, self.getSelectedUnit( 4 ) / iRougeModifier  )
		if ( self.getSelectedUnit( 5 ) > 0 ):
			self.makeUnit( con.iLongSwordsman, iLeader, tPlot, self.getSelectedUnit( 5 ) / (10*iRougeModifier) )
			self.makeUnit( con.iGuisarme, iLeader, tPlot, self.getSelectedUnit( 5 ) / (10*iRougeModifier)  )
			

		#if ( self.getCrusadePower() >  20 ):
		#	self.makeUnit( con.iLongSwordsman, iLeader, tPlot, 1 )
	
		#if ( self.getCrusadePower() > 40 ):
		#	self.makeUnit( con.iLongSwordsman, iLeader, tPlot, 1 )
		#	self.makeUnit( con.iCatapult, iLeader, tPlot, 1 )
			
		#if ( self.getCrusadePower() > 50 ):
		#	self.makeUnit( con.iLancer, iLeader, tPlot, 1 )
		#	
		#if ( self.getCrusadePower() > 60 ):
		#	#self.makeUnit( con.iLancer, iLeader, tPlot, 1 )
		#	self.makeUnit( con.iTrebuchet, iLeader, tPlot, 1 )
			
		#if ( self.getCrusadePower() > 70 ):
		#	self.makeUnit( con.iLancer, iLeader, tPlot, 1 )
 
		#if ( self.getCrusadePower() > 90 ):
		#	self.makeUnit( con.iKnight, iLeader, tPlot, 1 )
		#	self.makeUnit( con.iTrebuchet, iLeader, tPlot, 1 )
		
	def success( self, iPlayer ):
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
		if ( iGameTurn < self.getDCLast() + 20 ): # wait 20 turns between DC (Defensive Crusades)
			return
		lPotentials = []
		if ( iGameTurn % 3 != gc.getGame().getSorenRandNum(3, 'roll to see if we should DC')  ): # otherwise every turn gets too much to check
			return
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
					if ( iRandNum < 0 ):
						iChosen = lPotentials[i]
						break
		if ( iChosen > -1 ):
			iHuman = utils.getHumanID()
			if ( iChosen == iHuman ):
				self.callDCHuman()
			else:
				self.callDCAI( iChosen )
			self.setDCLast( iGameTurn )
				
				
				
	def canDC( self, iPlayer, iGameTurn ):
		pPlayer = gc.getPlayer( iPlayer )
		if ( (iGameTurn < con.tBirth[iPlayer]+5) or (not pPlayer.isAlive()) or pPlayer.getStateReligion() != iCatholicism ): 
		# only born, flipped and living Catholics can DC
			return False
		teamPlayer = gc.getTeam( pPlayer.getTeam() )
		if ( not teamPlayer.isOpenBorders( con.iPope ) ):
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
		for iEnemy in range( con.iNumPlayers ):
			pEnemy = gc.getPlayer( iEnemy )
			if ( teamPlayer.isAtWar( pEnemy.getTeam() ) and con.tBirth[iEnemy] + 10 > iGameTurn ):
				iEnemyReligion = pEnemy.getStateReligion()
				#print( " Crusade condition war meet: ",iEnemy,iEnemyReligion )
				if ( iEnemyReligion != iCatholicism and iEnemyReligion != iOrthodoxy ):
					#print( " Crusade condition Enemy Religion Meet: " )
					for pyCity in PyPlayer(iEnemy).getCityList():
						pCity = pyCity.GetCy()
						if ( rfceMaps.tWarsMaps[iPlayer][con.iMapMaxY-1-pCity.getY()][pCity.getX()] > 0 ):
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
		pPlayer.changeFaith( - min( 5, pPlayer.getFaith() ) )	
		
	def eventApply7625( self, popupReturn ):
		iDecision = popupReturn.getButtonClicked()
		iHuman = utils.getHumanID()
		pHuman = gc.getPlayer( iHuman )
		if ( iDecision == 0 ):
			self.makeDCUnits( iHuman )
			pHuman.changeFaith( - min( 5, pHuman.getFaith() ) )
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
		if ( iFaith > 4 ):
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 9 ):
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 19 ):	
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 29 ):
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		# 2 extra cavalry for the AI, it is dumb anyway
		if ( not iPlayer == utils.getHumanID() ):
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					
	def getDCBestInfantry( self, iPlayer ):
		teamPlayer = gc.getTeam( gc.getPlayer( iPlayer ).getTeam() )
		if ( teamPlayer.isHasTech( con.iNationalism ) and teamPlayer.isHasTech( con.iChemistry ) ):
			return con.iGrenadier
		if ( teamPlayer.isHasTech( con.iCivilService ) and teamPlayer.isHasTech( con.iMachinery ) ):
			return con.iMaceman
		if ( teamPlayer.isHasTech( con.iBlastFurnace ) ):
			return con.iLongSwordsman
		if ( teamPlayer.isHasTech( con.iChainMail ) ):
			return con.iSwordsman
		return con.iAxeman
		
	def getDCBestCavalry( self, iPlayer ):
		teamPlayer = gc.getTeam( gc.getPlayer( iPlayer ).getTeam() )
		if ( teamPlayer.isHasTech( con.iMilitaryTactics ) ):
			return con.iCuirassier
		if ( teamPlayer.isHasTech( con.iPlateArmor ) and teamPlayer.isHasTech( con.iChivalry ) ):
			return con.iKnight
		if ( teamPlayer.isHasTech( con.iFarriers ) and teamPlayer.isHasTech( con.iFeudalism ) ):
			return con.iHeavyLancer
		if ( teamPlayer.isHasTech( con.iManorialism ) and teamPlayer.isHasTech( con.iStirrup ) ):
			return con.iLancer
		return con.iScout
		
		
