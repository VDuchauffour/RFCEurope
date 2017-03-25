## This file is part of RFC Europe. Created by 3Miro, revised and improved by AbsintheRed

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import RFCUtils
import Consts as con
import XMLConsts as xml
import RFCEMaps as rfceMaps
import CityNameManager
from StoredData import sd

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()
cnm = CityNameManager.CityNameManager()

iNumCrusades = con.iNumCrusades
tJerusalem = con.tJerusalem
iCatholicism = xml.iCatholicism
iOrthodoxy = xml.iOrthodoxy

ProvMap = rfceMaps.tProinceMap

# Can call DC to aid Catholics, if at war with Non-Catholic and Non-Orthodox player, who isn't vassal of Catholic or Orthodox player and has at least one city in the provinces listed here
tDefensiveCrusadeMap = [
[], #Byzantium
[xml.iP_IleDeFrance,xml.iP_Aquitania,xml.iP_Orleans,xml.iP_Champagne,xml.iP_Bretagne,xml.iP_Normandy,xml.iP_Provence,xml.iP_Flanders,xml.iP_Burgundy,xml.iP_Picardy], #France
[], #Arabia
[], #Bulgaria
[xml.iP_Leon, xml.iP_GaliciaSpain, xml.iP_Lusitania, xml.iP_Aragon, xml.iP_Catalonia, xml.iP_Navarre, xml.iP_Castile, xml.iP_Andalusia, xml.iP_LaMancha, xml.iP_Valencia], #Cordoba (for consistency)
[xml.iP_Verona, xml.iP_Tuscany, xml.iP_Arberia, xml.iP_Dalmatia], #Venecia
[xml.iP_Flanders, xml.iP_Provence, xml.iP_Burgundy, xml.iP_Champagne, xml.iP_Lorraine,xml.iP_Picardy], #Burgundy
[xml.iP_Lorraine, xml.iP_Swabia, xml.iP_Bavaria, xml.iP_Saxony, xml.iP_Franconia, xml.iP_Flanders, xml.iP_Brandenburg, xml.iP_Holstein, xml.iP_Bohemia], #Germany
[], #Novgorod
[], #Norway
[], #Kiev
[xml.iP_Hungary, xml.iP_Transylvania, xml.iP_UpperHungary, xml.iP_Wallachia, xml.iP_Slavonia, xml.iP_Pannonia, xml.iP_Austria, xml.iP_Carinthia, xml.iP_Serbia, xml.iP_Moesia, xml.iP_Banat, xml.iP_Bosnia, xml.iP_Dalmatia], #Hungary
[xml.iP_Leon, xml.iP_GaliciaSpain, xml.iP_Lusitania, xml.iP_Aragon, xml.iP_Catalonia, xml.iP_Navarre, xml.iP_Castile, xml.iP_Andalusia, xml.iP_LaMancha, xml.iP_Valencia], #Spain
[xml.iP_Estonia], #Denmark
[], #Scotland
[xml.iP_GreaterPoland, xml.iP_LesserPoland, xml.iP_Silesia, xml.iP_Pomerania, xml.iP_Masovia, xml.iP_GaliciaPoland, xml.iP_Brest], #Poland
[xml.iP_Liguria, xml.iP_Lombardy, xml.iP_Corsica, xml.iP_Sardinia, xml.iP_Tuscany], #Genoa
[], #Morocco
[], #England
[xml.iP_Leon, xml.iP_GaliciaSpain, xml.iP_Lusitania, xml.iP_Aragon, xml.iP_Catalonia, xml.iP_Navarre, xml.iP_Castile, xml.iP_Andalusia, xml.iP_LaMancha, xml.iP_Valencia], #Portugal
[xml.iP_Valencia,xml.iP_Balears,xml.iP_Sicily,xml.iP_Apulia,xml.iP_Calabria], #Aragon
[xml.iP_Osterland], #Sweden
[xml.iP_Livonia,xml.iP_Estonia,xml.iP_Lithuania,xml.iP_Prussia], #Prussia
[], #Lithuania
[xml.iP_Austria, xml.iP_Carinthia, xml.iP_Bavaria, xml.iP_Bohemia, xml.iP_Moravia, xml.iP_Silesia], #Austria
[], #Turkey
[], #Moscow
[], #Dutch
[] #Papal States
];


class Crusades:

###############
### Popups 3Miro: taken from RFC Congress ###
#############

	def getCrusadeInit( self, iCrusade ):
		return sd.scriptDict['lCrusadeInit'][iCrusade]

	def setCrusadeInit( self, iCrusade, iNewCode ):
		# codes are:	-2, no crusade yet
		#				-1 crusade is active but waiting to start (Holy City is Christian and/or another Crusade in progress)
		#				0 or more, the turn when it was initialized
		sd.scriptDict['lCrusadeInit'][iCrusade] = iNewCode

	def addSelectedUnit( self, iUnitPlace ):
		sd.scriptDict['lSelectedUnits'][iUnitPlace] += 1

	def setSelectedUnit( self, iUnitPlace, iNewNumber ):
		sd.scriptDict['lSelectedUnits'][iUnitPlace] = iNewNumber

	def getSelectedUnit( self, iUnitPlace ):
		return sd.scriptDict['lSelectedUnits'][iUnitPlace]

	def getActiveCrusade( self, iGameTurn ):
		for i in range( iNumCrusades ):
			iInit = sd.scriptDict['lCrusadeInit'][i]
			if ( iInit > -1 and iInit + 9 > iGameTurn ):
				return i
		return -1

	def getParticipate( self ):
		return sd.scriptDict['bParticipate']

	def setParticipate( self, bVal ):
		sd.scriptDict['bParticipate'] = bVal

	def getVotingPower( self, iCiv ):
		return sd.scriptDict['lVotingPower'][iCiv]

	def setVotingPower( self, iCiv, iVotes ):
		sd.scriptDict['lVotingPower'][iCiv] = iVotes

	def getCrusadePower( self ):
		return sd.scriptDict['iCrusadePower']

	def setCrusadePower( self, iPower ):
		sd.scriptDict['iCrusadePower'] = iPower

	def getFavorite( self ):
		return sd.scriptDict['iFavorite']

	def setFavorite( self, iFavorite ):
		sd.scriptDict['iFavorite'] = iFavorite

	def getPowerful( self ):
		return sd.scriptDict['iPowerful']

	def setPowerful( self, iPowerful ):
		sd.scriptDict['iPowerful'] = iPowerful

	def getLeader( self ):
		return sd.scriptDict['iLeader']

	def setLeader( self, iLeader ):
		sd.scriptDict['iLeader'] = iLeader

	def getVotesGatheredFavorite( self ):
		return sd.scriptDict['lVotesGathered'][0]

	def setVotesGatheredFavorite( self, iVotes ):
		sd.scriptDict['lVotesGathered'][0] = iVotes

	def getVotesGatheredPowerful( self ):
		return sd.scriptDict['lVotesGathered'][1]

	def setVotesGatheredPowerful( self, iVotes ):
		sd.scriptDict['lVotesGathered'][1] = iVotes

	def getRichestCatholic( self ):
		return sd.scriptDict['iRichestCatholic']

	def setRichestCatholic( self, iPlayer ):
		sd.scriptDict['iRichestCatholic'] = iPlayer

	def getIsTarget( self, iCiv ):
		return sd.scriptDict['lDeviateTargets'][iCiv]

	def setIsTarget( self, iCiv, bTarget ):
		sd.scriptDict['lDeviateTargets'][iCiv] = bTarget
		
	def getTargetPlot( self ):
		return sd.scriptDict['tTarget']

 	def setTarget( self, iX, iY ):
		sd.scriptDict['tTarget'] = (iX, iY)

	def hasSucceeded( self ):
		iSucc = sd.scriptDict['iCrusadeSucceeded']
		iTest = iSucc == 1
		return iTest

	def setSucceeded( self ):
		sd.scriptDict['iCrusadeSucceeded'] = 1

	def getCrusadeToReturn( self ):
		return sd.scriptDict['iCrusadeToReturn']

	def setCrusadeToReturn( self, iNewValue ):
		sd.scriptDict['iCrusadeToReturn'] = iNewValue

	def isDCEnabled( self ):
		return sd.scriptDict['bDCEnabled']

	def setDCEnabled( self, bNewValue ):
		sd.scriptDict['bDCEnabled'] = bNewValue

	def getDCLast( self ):
		return sd.scriptDict['iDCLast']

	def setDCLast( self, iLast ):
		sd.scriptDict['iDCLast'] = iLast

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
		iCost = gc.getPlayer( utils.getHumanID() ).getGold() / 3
		sString = CyTranslator().getText("TXT_KEY_CRUSADE_RICHEST", ()) + CyTranslator().getText("TXT_KEY_CRUSADE_COST", ()) + " " + str(iCost) + " " + CyTranslator().getText("TXT_KEY_CRUSADE_GOLD", ()) + gc.getPlayer( self.getLeader() ).getName() + " " + CyTranslator().getText("TXT_KEY_CRUSADE_CURRENT_LEADER", ())
		self.showPopup( 7619, CyTranslator().getText("TXT_KEY_CRUSADE_DEVIATE", ()), sString, \
			( CyTranslator().getText("TXT_KEY_CRUSADE_DECIDE_WEALTH", ()), CyTranslator().getText("TXT_KEY_CRUSADE_DECIDE_FAITH", ()) ) )

	def deviateNewTargetPopup( self ):
		lTargetList = []
		lTargetList.append( gc.getMap().plot( tJerusalem[0], tJerusalem[1] ).getPlotCity().getName() + " (" + gc.getPlayer( gc.getMap().plot( tJerusalem[0], tJerusalem[1] ).getPlotCity().getOwner() ).getCivilizationAdjective(0) + ")" )
		for iPlayer in range( con.iNumPlayers ):
			pPlayer = gc.getPlayer( iPlayer )
			if ( iPlayer == con.iPope or pPlayer.getStateReligion() == iCatholicism or ( not pPlayer.isAlive() ) ):
				self.setIsTarget( iPlayer, False )
			else:
				self.setIsTarget( iPlayer, True )
				lTargetList.append( pPlayer.getCapitalCity().getName() + " (" + pPlayer.getCivilizationAdjective(0) + ")" )
		# Absinthe: might be a good idea to add a couple more target cities (only if the owner is a major civ with Islam as a state religion)
		#			like Alexandria, Damascus, Sevilla, Tangier
	#	tAlexandriaPlot = 
	#	tPlotDamascus = 
	#	tPlotSevilla = 
	#	tPlotTanja = 
	#	lCityPlots = []
	#	for tPlot in lCityPlots:
	#		pPlot = gc.getMap().plot( tPlot )
	#		pCity = pPlot.getPlotCity()
	#		iOwner = pCity.getOwner()
	#		sName = pCity.getName()
	#		pPlayer = gc.getPlayer( iOwner )
	#		iReligion = pPlayer.getStateReligion()
	#		if (iOwner < con.iNumPlayers and iReligion == xml.iIslam):
	#			self.setIsTarget( iOwner, True )
	#			lTargetList.append( sName + " (" + pPlayer.getCivilizationAdjective(0) + ")" )
		self.showPopup( 7620, CyTranslator().getText("TXT_KEY_CRUSADE_CORRUPT", ()), CyTranslator().getText("TXT_KEY_CRUSADE_TARGET", ()), lTargetList )

	def underCrusadeAttackPopup( self, sCityName, iLeader ):
		sText = CyTranslator().getText("TXT_KEY_CRUSADE_UNDER_ATTACK1", (gc.getPlayer(iLeader).getCivilizationAdjective(0), gc.getPlayer(iLeader).getName(), sCityName))
		self.showPopup( 7621, CyTranslator().getText("TXT_KEY_CRUSADE_UNDER_ATTACK", ()), sText, (CyTranslator().getText("TXT_KEY_CRUSADE_PREPARE", ()),) )

	def endCrusades(self):
		for i in range( iNumCrusades ):
			if ( self.getCrusadeInit( i ) < 0 ):
				self.setCrusadeInit( i, 0 )

	def checkTurn( self, iGameTurn ):
		#print(" 3Miro Crusades ")
		#self.informPopup()

		if ( self.getCrusadeToReturn() > -1 ):
			self.freeCrusaders( self.getCrusadeToReturn() )
			self.setCrusadeToReturn( -1 )

		# Absinthe: crusade date - 5 means the exact time for the arrival
		if ( iGameTurn == (xml.i1096AD - 5) ): #First Crusade arrives in 1096AD
			self.setCrusadeInit( 0, -1 ) # turn 160
		elif ( iGameTurn >= (xml.i1147AD - 7) and self.getCrusadeInit( 0 ) > 0 and self.getCrusadeInit(1) == -2 ): # Crusade of 1147AD, little earlier (need to be more than 9 turns between crusades)
			self.setCrusadeInit( 1, -1 ) # turn 176
		elif ( iGameTurn >= (xml.i1187AD - 8) and self.getCrusadeInit( 1 ) > 0 and self.getCrusadeInit(2) == -2 ): # Crusade of 1187AD, little earlier (need to be more than 9 turns between crusades)
			self.setCrusadeInit( 2, -1 ) # turn 187
		elif ( iGameTurn >= (xml.i1202AD - 4) and self.getCrusadeInit( 2 ) > 0 and self.getCrusadeInit(3) == -2 ): # Crusade of 1202AD, little later (need to be more than 9 turns between crusades)
			self.setCrusadeInit( 3, -1 ) # turn 197
		elif ( iGameTurn >= (xml.i1229AD - 3) and self.getCrusadeInit( 3 ) > 0 and self.getCrusadeInit(4) == -2 ): # Crusade of 1229AD, little later (need to be more than 9 turns between crusades)
			self.setCrusadeInit( 4, -1 ) # turn 207
	#	elif ( iGameTurn >= (xml.i1271AD - 5) and self.getCrusadeInit( 4 ) > 0 and self.getCrusadeInit(5) == -2 ): # Crusade of 1270AD
	#		self.setCrusadeInit( 5, -1 ) # turn 219

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

			elif ( iStartDate + 1 == iGameTurn ):
				self.computeVotingPower( iGameTurn )
				self.setCrusaders()
				for i in range( 8 ):
					self.setSelectedUnit( i, 0 )
				for iPlayer in range( con.iNumPlayers ):
					if ( self.getVotingPower( iPlayer ) > 0 ):
						self.sendUnits( iPlayer )
				print( " After the units are sent: " )
				print( " Crusade has Power: ", self.getCrusadePower() )
				print( " Crusade Templars: ",self.getSelectedUnit( 0 ) )
				print( " Crusade Teutonic: ",self.getSelectedUnit( 1 ) )
				print( " Crusade Hospitallers: ",self.getSelectedUnit( 2 ) )
				print( " Crusade Knights: ",self.getSelectedUnit( 3 ) )
				print( " Crusade H Lancers: ",self.getSelectedUnit( 4 ) )
				print( " Crusade Lancers: ",self.getSelectedUnit( 5 ) )
				print( " Crusade Siege: ",self.getSelectedUnit( 6 ) )
				print( " Crusade Other: ",self.getSelectedUnit( 7 ) )
				if ( not self.anyParticipate() ):
					return
				self.chooseCandidates( iGameTurn )
				self.voteForCandidatesAI()
				self.voteForCandidatesHuman()
				#print("  Votes are: ",self.getVotesGatheredFavorite(), self.getVotesGatheredPowerful() )

			elif ( iStartDate + 2 == iGameTurn ):
				if ( not self.anyParticipate() ):
					return
				self.selectVoteWinner()
				self.decideTheRichestCatholic( iActiveCrusade )
				if ( self.getRichestCatholic() == utils.getHumanID() ):
					self.decideDeviateHuman()
				else:
					self.decideDeviateAI()

			elif ( iStartDate + 5 == iGameTurn ):
				if ( not self.anyParticipate() ):
					return
				print( " Arrival " )
				self.crusadeArrival()

			elif ( iStartDate + 8 == iGameTurn ):
				iLeader = self.getLeader()
				self.setCrusadeToReturn( iLeader )
				self.setLeader(-1)
				self.returnCrusaders()

	def checkToStart( self, iGameTurn ):
	# if Jerusalem is Islamic or Pagan, Crusade has been initialized and it has been at least 5 turns since the last crusade and there are any Catholics, begin crusade
		pJPlot = gc.getMap().plot( tJerusalem[0], tJerusalem[1] )
		for i in range( iNumCrusades ): # check the Crusades
			if ( self.getCrusadeInit( i ) == -1 ): # if this one is to start
				if ( pJPlot.isCity() and self.anyCatholic() ): # if there is Jerusalem and there are any Catholics
					#Sedna17 -- allowing crusades against independent Jerusalem
					#if ( pJPlot.getPlotCity().getOwner() < con.iNumMajorPlayers ): # if Jerusalem is not Independent
					#iTmJerusalem = gc.getTeam( gc.getPlayer( gc.getMap().plot( tJerusalem[0], tJerusalem[1] ).getPlotCity().getOwner() ).getTeam() )
					iVictim = pJPlot.getPlotCity().getOwner() # get the information for the potential Victim
					pVictim = gc.getPlayer( iVictim )
					teamVictim = gc.getTeam( pVictim.getTeam() )
					iVictimReligion = pVictim.getStateReligion()
					if ( (iVictimReligion != iCatholicism and iVictimReligion != iOrthodoxy) or (pJPlot.getPlotCity().getOwner() > con.iNumMajorPlayers) ): # if the Victim is non-Catholic non-Orthodox
						bVassalOfImmune = False
						for iPlayerMaster in range( con.iNumMajorPlayers ): # for all the players, check to see if the Victim is a Vassal of a Catholic or Orthodox player
							pMaster = gc.getPlayer( iPlayerMaster ) # they are immune from Crusades
							iTMaster = pMaster.getTeam()
							if ( iPlayerMaster != iVictim and teamVictim.isVassal( iTMaster ) ):
								iMasterReligion = pMaster.getStateReligion()
								if ( iMasterReligion == iOrthodoxy or iMasterReligion == iCatholicism ):
									bVassalOfImmune = True

						if ( (not bVassalOfImmune) and (i == 0 or ( self.getCrusadeInit( i-1 ) > -1 and self.getCrusadeInit( i-1 ) + 9 < iGameTurn ) ) ):
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
			CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_DENY_FAITH", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
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
			pHuman.setGold( pHuman.getGold() - pHuman.getGold() / 3 )
			self.setLeader( iHuman )
			self.setCrusadePower( self.getCrusadePower() / 2 )
			self.deviateNewTargetPopup()
		else:
			self.setTarget( tJerusalem[0], tJerusalem[1] )
			self.startCrusade()

	def eventApply7620( self, popupReturn ):
		iDecision = popupReturn.getButtonClicked()
		if ( iDecision == 0 ):
			self.setTarget( tJerusalem[0], tJerusalem[1] )
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

		print( " Candidates ", iFavorite, iPowerful )
		for i in range( con.iNumPlayers ):
			print( " Civ voting power is: ", i, self.getVotingPower(i) )
		if ( iPowerful == iFavorite ):
			self.setPowerful( -1 )
		else:
			self.setPowerful( iPowerful )


	def computeVotingPower( self, iGameTurn ):
		iTmJerusalem = gc.getPlayer( gc.getMap().plot( tJerusalem[0], tJerusalem[1] ).getPlotCity().getOwner() ).getTeam()
		for iPlayer in range( con.iNumPlayers ):
			pPlayer = gc.getPlayer( iPlayer )
			if ( (con.tBirth[iPlayer] > iGameTurn) or (not pPlayer.isAlive()) or (pPlayer.getStateReligion() != iCatholicism) or ( gc.getTeam( pPlayer.getTeam() ).isVassal( iTmJerusalem ) )  ):
				self.setVotingPower( iPlayer, 0 )
			else:
				# We use the (similarly named) getVotingPower from CvPlayer.cpp to determine a vote value for a given State Religion, but it's kinda strange
				# Will leave it this way for now, but might be a good idea to improve it at some point
				self.setVotingPower( iPlayer, pPlayer.getVotingPower( iCatholicism ) )

		# No votes from the human player if he/she won't participate (AI civs will always participate)
		iHuman = utils.getHumanID()
		if ( not self.getParticipate() ):
			self.setVotingPower( iHuman, 0 )

		# The Pope has more votes (Rome is small anyway)
		self.setVotingPower( con.iPope, self.getVotingPower( con.iPope ) * (5 / 4) )

		iPower = 0
		for iPlayer in range( con.iNumPlayers ):
			iPower += self.getVotingPower( iPlayer )

		self.setCrusadePower( iPower )
		# Note that voting power is increased after this (but before the actual vote) for each sent unit by 2


	def setCrusaders( self ):
		iHuman = utils.getHumanID()
		#teamJerusalem = gc.getTeam( gc.getPlayer( gc.getMap().plot( tJerusalem[0], tJerusalem[1] ).getPlotCity().getOwner() ).getTeam() )
		for iPlayer in range( con.iNumPlayers ):
			if ( (not iPlayer == iHuman) and self.getVotingPower( iPlayer ) > 0 ):
				gc.getPlayer( iPlayer ).setIsCrusader( True )


	def sendUnits( self, iPlayer ):
		#iHuman = utils.getHumanID()
		pPlayer = gc.getPlayer( iPlayer )
		iNumUnits = pPlayer.getNumUnits()
		if ( con.tBirth[iPlayer] + 10 > gc.getGame().getGameTurn() ): # in the first 10 turns
			if (iNumUnits < 10):
				iMaxToSend = 0
			else:
				iMaxToSend = 1
		elif ( con.tBirth[iPlayer] + 25 > gc.getGame().getGameTurn() ): # between turn 10-25
			iMaxToSend = min( 10, max( 1, (5*iNumUnits) / 50 ) )
		else:
			iMaxToSend = min( 10, max( 1, (5*iNumUnits) / 35 ) ) # after turn 25
		iCrusadersSend = 0
		print ("iMaxToSend", iPlayer, iNumUnits, iMaxToSend)
		if (iMaxToSend > 0):
			for i in range( iNumUnits ):
				pUnit = pPlayer.getUnit( i )
				# Absinthe: check only for combat units and ignore naval units
				if (pUnit.baseCombatStr() > 0 and pUnit.getDomainType() != 0):
					# Absinthe: mercenaries and leaders (units with attached Great Generals) won't go
					if ( (not pUnit.isHasPromotion( xml.iPromotionMerc )) and (not pUnit.isHasPromotion( xml.iPromotionLeader )) ):
						iCrusadeCategory = self.unitCrusadeCategory( pUnit.getUnitType() )
						pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
						iRandNum = gc.getGame().getSorenRandNum(100, 'roll to send Unit to Crusade')
						# Absinthe: much bigger chance for special Crusader units and Knights
						if ( iCrusadeCategory < 4):
							if ( pPlot.isCity() ):
								if ( self.getNumDefendersAtPlot( pPlot ) > 3 ):
									if (iRandNum < 90 ):
										iCrusadersSend += 1
										self.sendUnit( pUnit )
								elif ( self.getNumDefendersAtPlot( pPlot ) > 1 ):
									if (iRandNum < 60 ):
										iCrusadersSend += 1
										self.sendUnit( pUnit )
							elif (iRandNum < 90 ):
								iCrusadersSend += 1
								self.sendUnit( pUnit )
						else:
							if ( pPlot.isCity() ):
								if ( self.getNumDefendersAtPlot( pPlot ) > 2 ):
									if (iRandNum < self.unitProbability( pUnit.getUnitType() ) ):
										iCrusadersSend += 1
										self.sendUnit( pUnit )
							elif ( iRandNum < self.unitProbability( pUnit.getUnitType() ) ):
									iCrusadersSend += 1
									self.sendUnit( pUnit )
						if ( iCrusadersSend == iMaxToSend ):
							return
			# Absinthe: extra chance for some random units, if we didn't fill the quota
			for i in range( 15 ):
				iRandUnit = gc.getGame().getSorenRandNum(iNumUnits, 'roll to pick Unit for Crusade')
				pUnit = pPlayer.getUnit( iRandUnit )
				pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
				# Absinthe: check only for combat units and ignore naval units
				if (pUnit.baseCombatStr() > 0 and pUnit.getDomainType() != 0):
					# Absinthe: mercenaries and leaders (units with attached Great Generals) won't go
					if ( (not pUnit.isHasPromotion( xml.iPromotionMerc )) and (not pUnit.isHasPromotion( xml.iPromotionLeader )) ):
						if ( pPlot.isCity() ):
							if ( self.getNumDefendersAtPlot( pPlot ) > 2 ):
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
			pUnit = pPlot.getUnit(i)
			if ( pUnit.getOwner() == iOwner ):
				if (pUnit.baseCombatStr() > 0 and pUnit.getDomainType() != 0):
					iDefenders += 1
		return iDefenders


	def sendUnit( self, pUnit ):
		iHuman = utils.getHumanID()
		iOwner = pUnit.getOwner()
		self.addSelectedUnit( self.unitCrusadeCategory( pUnit.getUnitType() ) )
		self.setVotingPower( iOwner, self.getVotingPower( iOwner ) + 2 )
		print ("Unit was chosen for Crusade:", iOwner, pUnit.getUnitType() )
		if ( iOwner == iHuman ):
			CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_CRUSADE_LEAVE", ()) + " " + pUnit.getName(), "AS2D_BUILD_CHRISTIAN", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
		pUnit.kill( 0, -1 )


	def unitProbability( self, iUnitType ):
		if iUnitType in [xml.iArcher, xml.iCrossbowman, xml.iArbalest, xml.iGenoaBalestrieri, xml.iLongbowman, xml.iEnglishLongbowman, xml.iPortugalFootKnight]:
			return 33
		if iUnitType in [xml.iLancer, xml.iBulgarianKonnik, xml.iCordobanBerber, xml.iHeavyLancer, xml.iHungarianHuszar, xml.iArabiaGhazi, xml.iByzantineCataphract, xml.iKievDruzhina, xml.iKnight, xml.iMoscowBoyar, xml.iBurgundianPaladin]:
			return 66
		if iUnitType in [xml.iTemplar, xml.iTeutonic, xml.iKnightofStJohns, xml.iCalatravaKnight, xml.iDragonKnight]:
			return 90
		if ( iUnitType < xml.iArcher or iUnitType > xml.iFieldArtillery ): # Workers, Executives, Missionaries, Sea Units and Mercenaries do not go
			return -1
		return 50


	def unitCrusadeCategory( self, iUnitType ):
		if ( iUnitType == xml.iTemplar ):
			return 0
		if ( iUnitType == xml.iTeutonic ):
			return 1
		if iUnitType in [xml.iKnightofStJohns, xml.iCalatravaKnight, xml.iDragonKnight]:
			return 2
		if iUnitType in [xml.iKnight, xml.iMoscowBoyar, xml.iBurgundianPaladin]:
			return 3
		if iUnitType in [xml.iHeavyLancer, xml.iHungarianHuszar, xml.iArabiaGhazi, xml.iByzantineCataphract, xml.iKievDruzhina]:
			return 4
		if iUnitType in [xml.iLancer, xml.iBulgarianKonnik, xml.iCordobanBerber]:
			return 5
		if iUnitType in [xml.iCatapult, xml.iTrebuchet]:
			return 6
		return 7


	def voteForCandidatesAI( self ):
		iHuman = utils.getHumanID()
		if ( self.getPowerful() == -1 ):
			self.setLeader( self.getFavorite() )
			if ( self.getParticipate() ):
				self.informLeaderPopup()
			elif utils.isActive(iHuman):
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
		elif utils.isActive(utils.getHumanID()):
			CyInterface().addMessage(utils.getHumanID(), True, con.iDuration/2, gc.getPlayer( self.getLeader() ).getName() + CyTranslator().getText("TXT_KEY_CRUSADE_LEAD", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)

		# not yet, check to see for deviations
		#pJPlot = gc.getMap().plot( tJerusalem[0], tJerusalem[1] )
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
		if ( iRichest == con.iVenecia or iRichest == con.iGenoa ):
			pByzantium = gc.getPlayer( con.iByzantium )
			if ( pByzantium.isAlive() ):
				# Only if Byzantium holds Constantinople and not a vassal
				pConstantinoplePlot = gc.getMap().plot( 81, 24 ) # tCapitals[con.iByzantium]
				pConstantinopleCity = pConstantinoplePlot.getPlotCity()
				iConstantinopleOwner = pConstantinopleCity.getOwner()
				bIsNotAVassal = not utils.isAVassal(con.iByzantium)
				if (iConstantinopleOwner == con.iByzantium and bIsNotAVassal):
					self.crusadeStolenAI( iRichest, con.iByzantium )
					bStolen = True
		if ( iRichest == con.iSpain or iRichest == con.iPortugal or iRichest == con.iAragon ):
			pCordoba = gc.getPlayer( con.iCordoba )
			if ( pCordoba.isAlive() ):
				# Only if Cordoba is Muslim and not a vassal
				bIsNotAVassal = not utils.isAVassal(con.iCordoba)
				if (pCordoba.getStateReligion() == xml.iIslam and bIsNotAVassal):
					self.crusadeStolenAI( iRichest, con.iCordoba )
					bStolen = True
		if ( iRichest == con.iHungary or iRichest == con.iPoland or iRichest == con.iAustria ):
			pTurkey = gc.getPlayer( con.iTurkey )
			if ( pTurkey.isAlive() ):
				# Only if the Ottomans are Muslim and not a vassal
				bIsNotAVassal = not utils.isAVassal(con.iTurkey)
				if (pTurkey.getStateReligion() == xml.iIslam and bIsNotAVassal):
					self.crusadeStolenAI( iRichest, con.iTurkey )
					bStolen = True
		if ( not bStolen ):
			self.setTarget( tJerusalem[0], tJerusalem[1] )

		self.startCrusade()

	def crusadeStolenAI( self, iNewLeader, iNewTarget ):
		self.setLeader( iNewLeader )
		pLeader = gc.getPlayer( iNewLeader )
		iHuman = utils.getHumanID()
		if utils.isActive(iHuman):
			CyInterface().addMessage(iHuman, False, con.iDuration/2, pLeader.getName() + CyTranslator().getText("TXT_KEY_CRUSADE_DEVIATED", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
		#pLeader.setGold( pLeader.getGold() - gc.getPlayer( con.iPope ).getGold() / 3 )
		#pLeader.setGold( gc.getPlayer( con.iPope ).getGold() / 4 )
		pLeader.setGold( 2 * pLeader.getGold() / 3 )
		pTarget = gc.getPlayer( iNewTarget ).getCapitalCity()
		self.setTarget( pTarget.getX(), pTarget.getY() )
		self.setCrusadePower( self.getCrusadePower() / 2 )

	def startCrusade( self ):
		iHuman = utils.getHumanID()
		iLeader = self.getLeader()
		iX, iY = self.getTargetPlot()
		pTargetCity = gc.getMap().plot( iX, iY ).getPlotCity()
		iTargetPlayer = pTargetCity.getOwner()
		# Target city can change ownership during the voting
		if ( gc.getPlayer( iTargetPlayer ).getStateReligion() == iCatholicism ):
			self.setLeader( -1 )
			self.returnCrusaders()
			return
		if ( iTargetPlayer == iHuman ):
			self.underCrusadeAttackPopup( pTargetCity.getName(), iLeader )
		elif utils.isActive(iHuman):
			sCityName = cnm.lookupName(pTargetCity,con.iPope)
			if ( sCityName == 'Unknown' ):
				sCityName = cnm.lookupName(pTargetCity,iLeader)
			sText = CyTranslator().getText("TXT_KEY_CRUSADE_START", (gc.getPlayer(iLeader).getCivilizationAdjectiveKey(), gc.getPlayer(iLeader).getName(), gc.getPlayer(iTargetPlayer).getCivilizationAdjectiveKey(), sCityName))
			CyInterface().addMessage(iHuman, False, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)

		gc.getTeam( gc.getPlayer( iLeader ).getTeam() ).declareWar( gc.getPlayer( pTargetCity.getOwner() ).getTeam(), True, -1 )

	def returnCrusaders( self ):
		for i in range( con.iNumPlayers ):
			gc.getPlayer( i ).setIsCrusader( False )

	def crusadeArrival( self ):
		iTX, iTY = self.getTargetPlot()
		iChosenX = -1
		iChosenY = -1

		# if the leader has been destroyed, cancel the Crusade
		iLeader = self.getLeader()
		if ( (iLeader==-1) or (not gc.getPlayer( iLeader ).isAlive()) ):
			self.returnCrusaders()
			return

		# if in the mean time Jerusalem has been captured by an Orthodox or Catholic player (and target is Jerusalem), cancel the Crusade
		if ( iTX == tJerusalem[0] and iTY == tJerusalem[1] ): # if the target is Jerusalem
			pPlot = gc.getMap().plot( tJerusalem[0], tJerusalem[1] )
			if ( pPlot.isCity() ): # and it is still there
				iVictim = pPlot.getPlotCity().getOwner() # get the Victim
				if ( iVictim < con.iNumMajorPlayers ): # if not Independent
					iReligion = gc.getPlayer( iVictim ).getStateReligion()
					if ( iReligion == iCatholicism or iReligion == iOrthodoxy ): # now controlled by Orthodox or Catholic (i.e. change of Religion)
						return

		# if not at war with the owner of the city, declare war
		pPlot = gc.getMap().plot( iTX, iTY )
		if ( pPlot.isCity() ):
			iVictim = pPlot.getPlotCity().getOwner()
			if ( iVictim != iLeader and gc.getPlayer(iVictim).getStateReligion() != iCatholicism ):
				teamLeader = gc.getTeam( gc.getPlayer(iLeader).getTeam() )
				iTeamVictim = gc.getTeam( gc.getPlayer(iVictim).getTeam() ).getID()
				if ( not teamLeader.isAtWar( iTeamVictim ) ):
					if ( teamLeader.canDeclareWar( iTeamVictim ) ):
						teamLeader.declareWar(iTeamVictim, False, -1)
					else:
						# we cannot declare war to the current owner of the target city
						self.returnCrusaders()
						return

		for y in range( 3 ):
			for x in range( 3 ):
				iX = iTX + x - 1 # try to spawn not across the river
				iY = iTY - y + 1
				if ( iChosenX == -1 ): # if we haven't found a valid plot yet
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
					iY = iTY - y + 1
					if ( iChosenX == -1 ): # if we haven't found a valid plot yet
						if ( (iX>=0) and (iX<con.iMapMaxX) and (iY>=0) and (iY<con.iMapMaxY) ):
							pPlot = gc.getMap().plot( iX, iY )
							if ( pPlot.isHills or pPlot.isFlatlands() ):
								iN = pPlot.getNumUnits()
								for i in range( iN ):
									pPlot.getUnit( i ).kill( False, con.iBarbarian )
									iChosenX = iX
									iChosenY = iY

				print("Made Units on:", iChosenX, iChosenY, iLeader)

		# Absinthe: if a valid plot is found, make the units and send a message about the arrival to the human player
		if ( (iChosenX>=0) and (iChosenX<con.iMapMaxX) and (iChosenY>=0) and (iChosenY<con.iMapMaxY) ):
			self.crusadeMakeUnits( [iChosenX,iChosenY] )
			if (utils.getHumanID() == iLeader):
				pTargetCity = gc.getMap().plot( iTX, iTY ).getPlotCity()
				sCityName = cnm.lookupName(pTargetCity,con.iPope)
				if ( sCityName == 'Unknown' ):
					sCityName = cnm.lookupName(pTargetCity,iLeader)
				CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_ARRIVAL", (sCityName, )) + "!", "", 0, "", ColorTypes(con.iGreen), iChosenX, iChosenY, True, True)
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
		teamLeader = gc.getTeam( gc.getPlayer( iLeader ).getTeam() )

		print( " Crusade has Power: ", self.getCrusadePower() )
		print( " Crusade Templars: ",self.getSelectedUnit( 0 ) )
		print( " Crusade Teutonic: ",self.getSelectedUnit( 1 ) )
		print( " Crusade Hospitallers: ",self.getSelectedUnit( 2 ) )
		print( " Crusade Knights: ",self.getSelectedUnit( 3 ) )
		print( " Crusade H Lancers: ",self.getSelectedUnit( 4 ) )
		print( " Crusade Lancers: ",self.getSelectedUnit( 5 ) )
		print( " Crusade Siege: ",self.getSelectedUnit( 6 ) )
		print( " Crusade Other: ",self.getSelectedUnit( 7 ) )

		iTX, iTY = self.getTargetPlot()
		# if the target is Jerusalem
		if ( iTX == tJerusalem[0] and iTY == tJerusalem[1] ):
			iRougeModifier = 100
			if (teamLeader.isHasTech( xml.iChivalry )):
				self.makeUnit( xml.iKnight, iLeader, tPlot, 1 )
				self.makeUnit( xml.iBurgundianPaladin, iLeader, tPlot, 1 )
				self.makeUnit( xml.iTemplar, iLeader, tPlot, 1 )
				self.makeUnit( xml.iTeutonic, iLeader, tPlot, 1 )
				self.makeUnit( xml.iGuisarme, iLeader, tPlot, 1 )
				self.makeUnit( xml.iCatapult, iLeader, tPlot, 1 )
			else:
				self.makeUnit( xml.iHeavyLancer, iLeader, tPlot, 2 )
				self.makeUnit( xml.iLancer, iLeader, tPlot, 1 )
				self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, 1 )
				self.makeUnit( xml.iSpearman, iLeader, tPlot, 1 )
				self.makeUnit( xml.iTrebuchet, iLeader, tPlot, 1 )
		# if the Crusade is stolen
		else:
			iRougeModifier = 200
			if (teamLeader.isHasTech( xml.iChivalry )):
				self.makeUnit( xml.iKnight, iLeader, tPlot, 1 )
				self.makeUnit( xml.iTeutonic, iLeader, tPlot, 1 )
				self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, 1 )
				self.makeUnit( xml.iGuisarme, iLeader, tPlot, 1 )
				self.makeUnit( xml.iCatapult, iLeader, tPlot, 1 )
			else:
				self.makeUnit( xml.iHeavyLancer, iLeader, tPlot, 1 )
				self.makeUnit( xml.iLancer, iLeader, tPlot, 1 )
				self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, 1 )
				self.makeUnit( xml.iSpearman, iLeader, tPlot, 1 )
				self.makeUnit( xml.iTrebuchet, iLeader, tPlot, 1 )

		# Absinthe: not all units should arrive near Jerusalem
		#			later Crusades have more units in the pool, so they should have bigger reduction
		iGameTurn = gc.getGame().getGameTurn()
		iCrusade = self.getActiveCrusade( iGameTurn )
		iHuman = utils.getHumanID()
		# Absinthe: this reduction is very significant for an AI-controlled Jerusalem, but Crusades should remain an increasing threat to the human player
		pPlot = gc.getMap().plot( tJerusalem[0], tJerusalem[1] )
		iVictim = pPlot.getPlotCity().getOwner()
		if (iVictim != iHuman):
			if ( iCrusade == 0 ):
				iRougeModifier *= 7 / 5
			elif ( iCrusade == 1 ):
				iRougeModifier *= 8 / 5
			elif ( iCrusade == 2 ):
				iRougeModifier *= 10 / 5
			elif ( iCrusade == 3 ):
				iRougeModifier *= 12 / 5
			elif ( iCrusade == 4 ):
				iRougeModifier *= 15 / 5
			else:
				iRougeModifier *= 18 / 5
		else:
			if ( iCrusade == 0 ):
				iRougeModifier *= 6 / 5
			elif ( iCrusade == 1 ):
				iRougeModifier *= 7 / 5
			elif ( iCrusade == 2 ):
				iRougeModifier *= 8 / 5
			elif ( iCrusade == 3 ):
				iRougeModifier *= 9 / 5
			elif ( iCrusade == 4 ):
				iRougeModifier *= 10 / 5
			else:
				iRougeModifier *= 12 / 5

		if ( self.getSelectedUnit( 0 ) > 0 ):
			self.makeUnit( xml.iTemplar, iLeader, tPlot, self.getSelectedUnit( 0 ) * 100 / iRougeModifier )
		if ( self.getSelectedUnit( 1 ) > 0 ):
			self.makeUnit( xml.iTeutonic, iLeader, tPlot, self.getSelectedUnit( 1 ) * 100 / iRougeModifier )
		if ( self.getSelectedUnit( 2 ) > 0 ):
			self.makeUnit( xml.iKnightofStJohns, iLeader, tPlot, self.getSelectedUnit( 2 ) * 100 / iRougeModifier )
		if ( self.getSelectedUnit( 3 ) > 0 ):
			iKnightNumber = self.getSelectedUnit( 3 ) * 100 / iRougeModifier
			if ( iLeader == con.iBurgundy ):
				for i in range( 0, iKnightNumber ):
					if (gc.getGame().getSorenRandNum(10, 'chance for Paladin') > 4): # Absinthe: 50% chance for a Paladin for each unit
						self.makeUnit( xml.iBurgundianPaladin, iLeader, tPlot, 1 )
					else:
						self.makeUnit( xml.iKnight, iLeader, tPlot, 1 )
			else:
				for i in range( 0, iKnightNumber ):
					if (gc.getGame().getSorenRandNum(10, 'chance for Paladin') > 7): # Absinthe: 20% chance for a Paladin for each unit
						self.makeUnit( xml.iBurgundianPaladin, iLeader, tPlot, 1 )
					else:
						self.makeUnit( xml.iKnight, iLeader, tPlot, 1 )
		if ( self.getSelectedUnit( 4 ) > 0 ):
			iLightCavNumber = self.getSelectedUnit( 4 ) * 100 / iRougeModifier
			if ( iLeader == con.iHungary ):
				for i in range( 0, iLightCavNumber ):
					if (gc.getGame().getSorenRandNum(10, 'chance for Huszar') > 4): # Absinthe: 50% chance for a Huszár for each unit
						self.makeUnit( xml.iHungarianHuszar, iLeader, tPlot, 1 )
					else:
						self.makeUnit( xml.iHeavyLancer, iLeader, tPlot, 1 )
			else:
				self.makeUnit( xml.iHeavyLancer, iLeader, tPlot, iLightCavNumber )
		if ( self.getSelectedUnit( 5 ) > 0 ):
			self.makeUnit( xml.iLancer, iLeader, tPlot, self.getSelectedUnit( 5 ) * 100 / iRougeModifier )
		if ( self.getSelectedUnit( 6 ) > 0 ):
			iSiegeNumber = self.getSelectedUnit( 6 ) * 100 / iRougeModifier
			if (iSiegeNumber > 2):
				self.makeUnit( xml.iCatapult, iLeader, tPlot, 2 )
				self.makeUnit( xml.iTrebuchet, iLeader, tPlot, iSiegeNumber - 2 )
			else:
				self.makeUnit( xml.iCatapult, iLeader, tPlot, iSiegeNumber )
		if ( self.getSelectedUnit( 7 ) > 0 ):
			iFootNumber = self.getSelectedUnit( 7 ) * 100 / iRougeModifier
			for i in range( 0, iFootNumber ):
				if (gc.getGame().getSorenRandNum(2, 'coinflip') == 1): # Absinthe: 50% chance for both type
					self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, 1 )
				else:
					self.makeUnit( xml.iGuisarme, iLeader, tPlot, 1 )


		#if ( self.getCrusadePower() >  20 ):
		#	self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, 1 )

		#if ( self.getCrusadePower() > 40 ):
		#	self.makeUnit( xml.iLongSwordsman, iLeader, tPlot, 1 )
		#	self.makeUnit( xml.iCatapult, iLeader, tPlot, 1 )

		#if ( self.getCrusadePower() > 50 ):
		#	self.makeUnit( xml.iLancer, iLeader, tPlot, 1 )

		#if ( self.getCrusadePower() > 60 ):
		#	#self.makeUnit( xml.iLancer, iLeader, tPlot, 1 )
		#	self.makeUnit( xml.iTrebuchet, iLeader, tPlot, 1 )

		#if ( self.getCrusadePower() > 70 ):
		#	self.makeUnit( xml.iLancer, iLeader, tPlot, 1 )

		#if ( self.getCrusadePower() > 90 ):
		#	self.makeUnit( xml.iKnight, iLeader, tPlot, 1 )
		#	self.makeUnit( xml.iTrebuchet, iLeader, tPlot, 1 )


	def freeCrusaders( self, iPlayer ):
		# the majority of Crusader units will return from the Crusade, so the Crusading civ will have harder time keeping Jerusalem and the Levant
		unitList = PyPlayer( iPlayer ).getUnitList()
		for pUnit in unitList:
			if ( pUnit.getMercID() == -5 ): # so this is a Crusader Unit
				pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
				iOdds = 80
				iCrusadeCategory = self.unitCrusadeCategory( pUnit.getUnitType() )
				if ( iCrusadeCategory < 3 ):
					iOdds = -1 # Knight Orders don't return
				elif ( iCrusadeCategory == 7 ):
					iOdds = 50 # leave some defenders
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
						CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_CRUSADE_CRUSADERS_RETURNING_HOME", ()) + " " + pUnit.getName(), "", 0, "", ColorTypes(con.iLime), -1, -1, True, True)


	# Absinthe: called from CvRFCEventHandler.onCityAcquired
	def success( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		if ( not self.hasSucceeded() ):
			pPlayer.changeGoldenAgeTurns( gc.getPlayer( iPlayer).getGoldenAgeLength() )
			self.setSucceeded()
			pCurrent = gc.getMap().plot( tJerusalem[0]-1, tJerusalem[1]-1 )
			utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( tJerusalem[0]-1, tJerusalem[1] )
			utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( tJerusalem[0]-1, tJerusalem[1]+1 )
			utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( tJerusalem[0]+1, tJerusalem[1]+1 )
			utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( tJerusalem[0]+1, tJerusalem[1] )
			utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( tJerusalem[0]+1, tJerusalem[1]-1 )
			utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( tJerusalem[0], tJerusalem[1]+1 )
			utils.convertPlotCulture(pCurrent, iPlayer, 100, False)
			pCurrent = gc.getMap().plot( tJerusalem[0], tJerusalem[1]-1 )
			utils.convertPlotCulture(pCurrent, iPlayer, 100, False)


	def doDC( self, iGameTurn ):
		#print(" DC Check 1",iGameTurn,self.getDCLast())
		if ( iGameTurn < self.getDCLast() + 15 ): # wait 15 turns between DCs (Defensive Crusades)
			return
		if ( iGameTurn % 3 != gc.getGame().getSorenRandNum(3, 'roll to see if we should DC')  ): # otherwise every turn gets too much to check
			return
		#print(" DC Check")
		lPotentials = []
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
		if utils.isActive(iHuman):
			if ( gc.getTeam( pHuman.getTeam() ).canContact( pPlayer.getTeam() ) or pHuman.getStateReligion() == iCatholicism ): # as you have contact with the Pope by default
				sText = CyTranslator().getText("TXT_KEY_CRUSADE_DEFENSIVE_AI_MESSAGE", ()) + " " + pPlayer.getName()
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
		if ( iX == -1 or iY == -1 ):
			apCityList = PyPlayer(iPlayer).getCityList()
			if ( len(apCityList) > 0 ):
				pCity = apCityList[gc.getGame().getSorenRandNum(len(apCityList), 'random city for DC')]
				city = pCity.GetCy()
				iX = city.getX()
				iY = city.getY()
			else:
				return

		# Absinthe: interface message for the player
		if (gc.getPlayer(iPlayer).isHuman()):
			CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_DEFENSIVE_HUMAN_MESSAGE", ()), "", 0, "", ColorTypes(con.iGreen), iX, iY, True, True)

		pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( pPlayer.getNumCities() < 6 ): # smaller Empires need a bit more help
			if (iBestCavalry == xml.iKnight):
				if (gc.getGame().getSorenRandNum(10, 'chance for Paladin') > 6): # 30% chance for a Paladin
					pPlayer.initUnit(xml.iBurgundianPaladin, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				else:
					pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			else:
				pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 4 ):
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 11 ):
			if (iBestCavalry == xml.iKnight):
				if (gc.getGame().getSorenRandNum(10, 'chance for Paladin') > 6): # 30% chance for a Paladin
					pPlayer.initUnit(xml.iBurgundianPaladin, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				else:
					pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			else:
				pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 20 ):
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if ( iFaith > 33 ):
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		# extra units for the AI, it is dumb anyway
		if ( not iPlayer == utils.getHumanID() ):
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			if (iBestCavalry == xml.iKnight):
				if (gc.getGame().getSorenRandNum(10, 'chance for Paladin') > 6): # 30% chance for a Paladin
					pPlayer.initUnit(xml.iBurgundianPaladin, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				else:
					pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			else:
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

	def do1200ADCrusades( self ):
		self.setCrusadeInit(0, xml.i1096AD)
		self.setCrusadeInit(1, xml.i1147AD)
		self.setCrusadeInit(2, xml.i1187AD)