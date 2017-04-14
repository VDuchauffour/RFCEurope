# Rhye's and Fall of Civilization: Europe - Crusades
# Created by 3Miro, revised and improved by AbsintheRed

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
import random

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()
cnm = CityNameManager.CityNameManager()

iNumCrusades = con.iNumCrusades
tJerusalem = con.tJerusalem
iCatholicism = xml.iCatholicism
iOrthodoxy = xml.iOrthodoxy

ProvMap = rfceMaps.tProvinceMap

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

	def changeNumUnitsSent( self, iPlayer, iChange ):
		sd.scriptDict['lNumUnitsSent'][iPlayer] += iChange

	def setNumUnitsSent( self, iPlayer, iNewNumber ):
		sd.scriptDict['lNumUnitsSent'][iPlayer] = iNewNumber

	def getNumUnitsSent( self, iPlayer ):
		return sd.scriptDict['lNumUnitsSent'][iPlayer]

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
		iHuman = utils.getHumanID()
		pHuman = gc.getPlayer(iHuman)
		iActiveCrusade = self.getActiveCrusade( gc.getGame().getGameTurn() )
		iBribe = 200 + 50 * iActiveCrusade
		if pHuman.getGold() >= iBribe:
			self.showPopup( 7616, CyTranslator().getText("TXT_KEY_CRUSADE_INIT_POPUP", ()), CyTranslator().getText("TXT_KEY_CRUSADE_INIT", ()), \
			(CyTranslator().getText("TXT_KEY_CRUSADE_ACCEPT", ()), CyTranslator().getText("TXT_KEY_CRUSADE_DENY", ()), CyTranslator().getText("TXT_KEY_CRUSADE_DENY_RUDE", ()), CyTranslator().getText("TXT_KEY_CRUSADE_BRIBE_OUT", (iBribe, ))) )
		else:
			self.showPopup( 7616, CyTranslator().getText("TXT_KEY_CRUSADE_INIT_POPUP", ()), CyTranslator().getText("TXT_KEY_CRUSADE_INIT", ()), \
			(CyTranslator().getText("TXT_KEY_CRUSADE_ACCEPT", ()), CyTranslator().getText("TXT_KEY_CRUSADE_DENY", ()), CyTranslator().getText("TXT_KEY_CRUSADE_DENY_RUDE", ())) )

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
			if iPlayer == con.iPope or pPlayer.getStateReligion() == iCatholicism or not pPlayer.isAlive():
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
			if self.getCrusadeInit( i ) < 0:
				self.setCrusadeInit( i, 0 )
		# Absinthe: reset sent unit counter after the Crusades are over (so it won't give Company benefits forever based on the last one)
		for iPlayer in range( con.iNumPlayers ):
			self.setNumUnitsSent( iPlayer, 0 )

	def checkTurn( self, iGameTurn ):
		#print(" 3Miro Crusades ")
		#self.informPopup()

		if self.getCrusadeToReturn() > -1:
			self.freeCrusaders( self.getCrusadeToReturn() )
			self.setCrusadeToReturn( -1 )

		# Absinthe: crusade date - 5 means the exact time for the arrival
		if iGameTurn == (xml.i1096AD - 5): #First Crusade arrives in 1096AD
			self.setCrusadeInit( 0, -1 ) # turn 160
		elif iGameTurn >= (xml.i1147AD - 7) and self.getCrusadeInit( 0 ) > 0 and self.getCrusadeInit( 1 ) == -2: # Crusade of 1147AD, little earlier (need to be more than 9 turns between crusades)
			self.setCrusadeInit( 1, -1 ) # turn 176
		elif iGameTurn >= (xml.i1187AD - 8) and self.getCrusadeInit( 1 ) > 0 and self.getCrusadeInit( 2 ) == -2: # Crusade of 1187AD, little earlier (need to be more than 9 turns between crusades)
			self.setCrusadeInit( 2, -1 ) # turn 187
		elif iGameTurn >= (xml.i1202AD - 4) and self.getCrusadeInit( 2 ) > 0 and self.getCrusadeInit( 3 ) == -2: # Crusade of 1202AD, little later (need to be more than 9 turns between crusades)
			self.setCrusadeInit( 3, -1 ) # turn 197
		elif iGameTurn >= (xml.i1229AD - 3) and self.getCrusadeInit( 3 ) > 0 and self.getCrusadeInit( 4 ) == -2: # Crusade of 1229AD, little later (need to be more than 9 turns between crusades)
			self.setCrusadeInit( 4, -1 ) # turn 207
		elif iGameTurn >= (xml.i1271AD - 5) and self.getCrusadeInit( 4 ) > 0 and self.getCrusadeInit( 5 ) == -2: # Crusade of 1270AD
			self.setCrusadeInit( 5, -1 ) # turn 219

		# Start of Defensive Crusades: indulgences for the Reconquista given by the Catholic Church in 1000AD
		if iGameTurn == xml.i1000AD:
			self.setDCEnabled( True )

		# End of Defensive Crusades: no more DCs after Protestantism is founded
		if self.isDCEnabled():
			if gc.getGame().isReligionFounded(xml.iProtestantism):
				self.setDCEnabled( False )

		if self.isDCEnabled():
			self.doDC( iGameTurn )

		self.checkToStart( iGameTurn )

		iActiveCrusade = self.getActiveCrusade( iGameTurn )
		if iActiveCrusade > -1:
			iStartDate = self.getCrusadeInit( iActiveCrusade )
			if iStartDate == iGameTurn:
				self.doParticipation( iGameTurn )

			elif iStartDate + 1 == iGameTurn:
				self.computeVotingPower( iGameTurn )
				self.setCrusaders()
				for i in range( 8 ):
					self.setSelectedUnit( i, 0 )
				for iPlayer in range( con.iNumPlayers ):
					# Absinthe: first we set all civs' unit counter to 0, then send the new round of units
					self.setNumUnitsSent( iPlayer, 0 )
					if self.getVotingPower( iPlayer ) > 0:
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
				if not self.anyParticipate():
					return
				self.chooseCandidates( iGameTurn )
				self.voteForCandidatesAI()
				self.voteForCandidatesHuman()
				#print("  Votes are: ",self.getVotesGatheredFavorite(), self.getVotesGatheredPowerful() )

			elif iStartDate + 2 == iGameTurn:
				if not self.anyParticipate():
					return
				self.selectVoteWinner()
				self.decideTheRichestCatholic( iActiveCrusade )
				if self.getRichestCatholic() == utils.getHumanID():
					self.decideDeviateHuman()
				else:
					self.decideDeviateAI()

			elif iStartDate + 5 == iGameTurn:
				if not self.anyParticipate():
					return
				print( " Arrival " )
				self.crusadeArrival( iActiveCrusade )

			elif iStartDate + 8 == iGameTurn:
				iLeader = self.getLeader()
				self.setCrusadeToReturn( iLeader )
				self.setLeader(-1)
				self.returnCrusaders()


	def checkToStart( self, iGameTurn ):
		# if Jerusalem is Islamic or Pagan, Crusade has been initialized and it has been at least 5 turns since the last crusade and there are any Catholics, begin crusade
		pJPlot = gc.getMap().plot( tJerusalem[0], tJerusalem[1] )
		for i in range( iNumCrusades ): # check the Crusades
			if self.getCrusadeInit( i ) == -1: # if this one is to start
				if pJPlot.isCity() and self.anyCatholic(): # if there is Jerusalem and there are any Catholics
					#Sedna17 -- allowing crusades against independent Jerusalem
					iVictim = pJPlot.getPlotCity().getOwner()
					if self.isOrMasterChristian(iVictim):
						break
					if i == 0 or ( self.getCrusadeInit( i-1 ) > -1 and self.getCrusadeInit( i-1 ) + 9 < iGameTurn ):
						self.setCrusadeInit( i, iGameTurn )
						print( "Crusade Starting Turn ",iGameTurn )

	def anyCatholic( self ):
		for i in range( con.iNumPlayers-1 ):
			if gc.getPlayer(i).getStateReligion() == iCatholicism:
				return True
		return False

	def anyParticipate( self ):
		for i in range( con.iNumPlayers-1 ):
			if self.getVotingPower( i ) > 0:
				return True
		return False

	def eventApply7616( self, popupReturn ):
		iHuman = utils.getHumanID()
		if popupReturn.getButtonClicked() == 0:
			self.setParticipate( True )
			gc.getPlayer( iHuman ).setIsCrusader( True )
			print("Going on a Crusade " )
		elif popupReturn.getButtonClicked() == 1 or popupReturn.getButtonClicked() == 2:
			self.setParticipate( False )
			pPlayer = gc.getPlayer( iHuman )
			pPlayer.setIsCrusader( False )
			pPlayer.changeFaith( - min( 5, pPlayer.getFaith() ) )
			CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_DENY_FAITH", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
			gc.getPlayer( con.iPope ).AI_changeMemoryCount( iHuman, MemoryTypes.MEMORY_REJECTED_DEMAND, 2 )
			# Absinthe: some units from Chivalric Orders might leave you nevertheless
			unitList = PyPlayer( iHuman ).getUnitList()
			for pUnit in unitList:
				iUnitType = pUnit.getUnitType()
				if iUnitType in [xml.iKnightofStJohns, xml.iTemplar, xml.iTeutonic]:
					pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
					iRandNum = gc.getGame().getSorenRandNum(100, 'roll to send Unit to Crusade')
					if pPlot.isCity():
						if self.getNumDefendersAtPlot( pPlot ) > 3:
							if iRandNum < 50:
								self.addSelectedUnit( self.unitCrusadeCategory( iUnitType ) )
								CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_DENY_LEAVE_ANYWAY", ()), "", 0, gc.getUnitInfo(iUnitType).getButton(), ColorTypes(con.iLightRed), pUnit.getX(), pUnit.getY(), True, True)
						elif self.getNumDefendersAtPlot( pPlot ) > 1:
							if iRandNum < 10:
								self.addSelectedUnit( self.unitCrusadeCategory( iUnitType ) )
								CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_DENY_LEAVE_ANYWAY", ()), "", 0, gc.getUnitInfo(iUnitType).getButton(), ColorTypes(con.iLightRed), pUnit.getX(), pUnit.getY(), True, True)
					elif iRandNum < 30:
						self.addSelectedUnit( self.unitCrusadeCategory( iUnitType ) )
						CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_DENY_LEAVE_ANYWAY", ()), "", 0, gc.getUnitInfo(iUnitType).getButton(), ColorTypes(con.iLightRed), pUnit.getX(), pUnit.getY(), True, True)
		# Absinthe: 3rd option, only if you have enough money to make a contribution to the Crusade instead of sending units
		else:
			self.setParticipate( False )
			pPlayer = gc.getPlayer( iHuman )
			pPlayer.setIsCrusader( False )
			pPope = gc.getPlayer(con.iPope)
			iActiveCrusade = self.getActiveCrusade( gc.getGame().getGameTurn() )
			iBribe = 200 + 50 * iActiveCrusade
			pPope.changeGold( iBribe )
			pPlayer.changeGold( -iBribe )
			gc.getPlayer( con.iPope ).AI_changeMemoryCount( iHuman, MemoryTypes.MEMORY_REJECTED_DEMAND, 1 )

	def eventApply7618( self, popupReturn ):
		if popupReturn.getButtonClicked() == 0:
			self.setVotesGatheredFavorite( self.getVotesGatheredFavorite() + self.getVotingPower( utils.getHumanID() ) )
		else:
			self.setVotesGatheredPowerful( self.getVotesGatheredPowerful() + self.getVotingPower( utils.getHumanID() ) )

	def eventApply7619( self, popupReturn ):
		if popupReturn.getButtonClicked() == 0:
			iHuman = utils.getHumanID()
			pHuman = gc.getPlayer( iHuman )
			#pHuman.setGold( pHuman.getGold() - gc.getPlayer( utils.getHumanID() ).getGold() / 4 )
			pHuman.changeGold( - pHuman.getGold() / 3 )
			self.setLeader( iHuman )
			self.setCrusadePower( self.getCrusadePower() / 2 )
			self.deviateNewTargetPopup()
		else:
			self.setTarget( tJerusalem[0], tJerusalem[1] )
			self.startCrusade()

	def eventApply7620( self, popupReturn ):
		iDecision = popupReturn.getButtonClicked()
		if iDecision == 0:
			self.setTarget( tJerusalem[0], tJerusalem[1] )
			self.startCrusade()
			return
		iTargets = 0
		#print(" 3Miro Deviate Crusade: ",iDecision )
		for i in range( con.iNumPlayers ):
			if self.getIsTarget( i ):
				iTargets += 1
			if iTargets == iDecision:
				pTargetCity = gc.getPlayer( i ).getCapitalCity()
				self.setTarget( pTargetCity.getX(), pTargetCity.getY() )
				iDecision = -2

		self.startCrusade()

	def doParticipation( self, iGameTurn ):
		iHuman = utils.getHumanID()
		#print(" 3Miro Crusades doPart", iHuman, iGameTurn )
		if con.tBirth[iHuman] < iGameTurn:
			pHuman = gc.getPlayer( iHuman )
			if pHuman.getStateReligion() != iCatholicism:
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
		for i in range( con.iNumPlayers-1 ):
			if self.getVotingPower( i ) > 0:
				if bFound:
					iNFavor = gc.getRelationTowards( con.iPope, i )
					if iNFavor > iFavor:
						iNFavor = iFavor
						iFavorite = i
				else:
					iFavor = gc.getRelationTowards( con.iPope, i )
					iFavorite = i
					bFound = True
		self.setFavorite( iFavorite )

		iPowerful = iFavorite
		iPower = self.getVotingPower( iPowerful )

		for i in range( con.iNumPlayers-1 ):
			if self.getVotingPower( i ) > iPower or ( iPowerful == iFavorite and self.getVotingPower( i ) > 0 ):
				iPowerful = i
				iPower = self.getVotingPower( iPowerful )

		print( " Candidates ", iFavorite, iPowerful )
		for i in range( con.iNumPlayers ):
			print( " Civ voting power is: ", i, self.getVotingPower(i) )
		if iPowerful == iFavorite:
			self.setPowerful( -1 )
		else:
			self.setPowerful( iPowerful )


	def computeVotingPower( self, iGameTurn ):
		iTmJerusalem = gc.getPlayer( gc.getMap().plot( tJerusalem[0], tJerusalem[1] ).getPlotCity().getOwner() ).getTeam()
		for iPlayer in range( con.iNumPlayers ):
			pPlayer = gc.getPlayer( iPlayer )
			if con.tBirth[iPlayer] > iGameTurn or not pPlayer.isAlive() or pPlayer.getStateReligion() != iCatholicism or gc.getTeam( pPlayer.getTeam() ).isVassal( iTmJerusalem ):
				self.setVotingPower( iPlayer, 0 )
			else:
				# We use the (similarly named) getVotingPower from CvPlayer.cpp to determine a vote value for a given State Religion, but it's kinda strange
				# Will leave it this way for now, but might be a good idea to improve it at some point
				self.setVotingPower( iPlayer, pPlayer.getVotingPower( iCatholicism ) )

		# No votes from the human player if he/she won't participate (AI civs will always participate)
		iHuman = utils.getHumanID()
		if not self.getParticipate():
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
			if not iPlayer == iHuman and self.getVotingPower( iPlayer ) > 0:
				gc.getPlayer( iPlayer ).setIsCrusader( True )


	def sendUnits( self, iPlayer ):
		#iHuman = utils.getHumanID()
		pPlayer = gc.getPlayer( iPlayer )
		iNumUnits = pPlayer.getNumUnits()
		if con.tBirth[iPlayer] + 10 > gc.getGame().getGameTurn(): # in the first 10 turns
			if iNumUnits < 10:
				iMaxToSend = 0
			else:
				iMaxToSend = 1
		elif con.tBirth[iPlayer] + 25 > gc.getGame().getGameTurn(): # between turn 10-25
			iMaxToSend = min( 10, max( 1, (5*iNumUnits) / 50 ) )
		else:
			iMaxToSend = min( 10, max( 1, (5*iNumUnits) / 35 ) ) # after turn 25
		iCrusadersSend = 0
		print ("iMaxToSend", iPlayer, iNumUnits, iMaxToSend)
		if iMaxToSend > 0:
			# Absinthe: a randomized list of all units of the civ
			lUnits = [pPlayer.getUnit( i ) for i in range(iNumUnits)]
			random.shuffle(lUnits)
			for pUnit in lUnits:
				# Absinthe: check only for combat units and ignore naval units
				if pUnit.baseCombatStr() > 0 and pUnit.getDomainType() != DomainTypes.DOMAIN_SEA:
					# Absinthe: mercenaries and leaders (units with attached Great Generals) won't go
					if not pUnit.isHasPromotion( xml.iPromotionMerc ) and not pUnit.isHasPromotion( xml.iPromotionLeader ):
						iCrusadeCategory = self.unitCrusadeCategory( pUnit.getUnitType() )
						pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
						iRandNum = gc.getGame().getSorenRandNum(100, 'roll to send Unit to Crusade')
						# Absinthe: much bigger chance for special Crusader units and Knights
						if iCrusadeCategory < 4:
							if pPlot.isCity():
								if self.getNumDefendersAtPlot( pPlot ) > 3:
									if iRandNum < 80:
										iCrusadersSend += 1
										self.sendUnit( pUnit )
								elif self.getNumDefendersAtPlot( pPlot ) > 1:
									if iRandNum < 40:
										iCrusadersSend += 1
										self.sendUnit( pUnit )
							elif iRandNum < 80:
								iCrusadersSend += 1
								self.sendUnit( pUnit )
						else:
							if pPlot.isCity():
								if self.getNumDefendersAtPlot( pPlot ) > 2:
									if iRandNum < (self.unitProbability( pUnit.getUnitType() ) - 10):
										iCrusadersSend += 1
										self.sendUnit( pUnit )
							elif iRandNum < (self.unitProbability( pUnit.getUnitType() ) - 10):
									iCrusadersSend += 1
									self.sendUnit( pUnit )
						if iCrusadersSend == iMaxToSend:
							return
			# Absinthe: extra chance for some random units, if we didn't fill the quota
			for i in range( 15 ):
				iNumUnits = pPlayer.getNumUnits() # we have to recalculate each time, as some units might have gone on the Crusade already
				iRandUnit = gc.getGame().getSorenRandNum(iNumUnits, 'roll to pick Unit for Crusade')
				pUnit = pPlayer.getUnit( iRandUnit )
				# Absinthe: check only for combat units and ignore naval units
				if pUnit.baseCombatStr() > 0 and pUnit.getDomainType() != 0:
					# Absinthe: mercenaries and leaders (units with attached Great Generals) won't go
					if not pUnit.isHasPromotion( xml.iPromotionMerc ) and not pUnit.isHasPromotion( xml.iPromotionLeader ):
						pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
						if pPlot.isCity():
							if self.getNumDefendersAtPlot( pPlot ) > 2:
								if gc.getGame().getSorenRandNum(100, 'roll to send Unit to Crusade') < self.unitProbability( pUnit.getUnitType() ):
									iCrusadersSend += 1
									self.sendUnit( pUnit )
						else:
							if gc.getGame().getSorenRandNum(100, 'roll to send Unit to Crusade') < self.unitProbability( pUnit.getUnitType() ):
								iCrusadersSend += 1
								self.sendUnit( pUnit )
						if iCrusadersSend == iMaxToSend:
							return


	def getNumDefendersAtPlot( self, pPlot ):
		iOwner = pPlot.getOwner()
		if iOwner < 0:
			return 0
		iNumUnits = pPlot.getNumUnits()
		iDefenders = 0
		for i in range( iNumUnits ):
			pUnit = pPlot.getUnit(i)
			if pUnit.getOwner() == iOwner:
				if pUnit.baseCombatStr() > 0 and pUnit.getDomainType() != DomainTypes.DOMAIN_SEA:
					iDefenders += 1
		return iDefenders


	def sendUnit( self, pUnit ):
		iHuman = utils.getHumanID()
		iOwner = pUnit.getOwner()
		self.addSelectedUnit( self.unitCrusadeCategory( pUnit.getUnitType() ) )
		self.setVotingPower( iOwner, self.getVotingPower( iOwner ) + 2 )
		self.changeNumUnitsSent( iOwner, 1 ) # Absinthe: counter for sent units per civ
		print ("Unit was chosen for Crusade:", iOwner, pUnit.getUnitType() )
		if iOwner == iHuman:
			CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_CRUSADE_LEAVE", ()) + " " + pUnit.getName(), "AS2D_BUILD_CHRISTIAN", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
		pUnit.kill( 0, -1 )


	def unitProbability( self, iUnitType ):
		if iUnitType in [xml.iArcher, xml.iCrossbowman, xml.iArbalest, xml.iGenoaBalestrieri, xml.iLongbowman, xml.iEnglishLongbowman, xml.iPortugalFootKnight]:
			return 10
		if iUnitType in [xml.iLancer, xml.iBulgarianKonnik, xml.iCordobanBerber, xml.iHeavyLancer, xml.iHungarianHuszar, xml.iArabiaGhazi, xml.iByzantineCataphract, xml.iKievDruzhina, xml.iKnight, xml.iMoscowBoyar, xml.iBurgundianPaladin]:
			return 70
		if iUnitType in [xml.iTemplar, xml.iTeutonic, xml.iKnightofStJohns, xml.iCalatravaKnight, xml.iDragonKnight]:
			return 90
		if iUnitType <= xml.iIslamicMissionary or iUnitType >= xml.iWorkboat: # Workers, Executives, Missionaries, Sea Units and Mercenaries do not go
			return -1
		return 50


	def unitCrusadeCategory( self, iUnitType ):
		if iUnitType == xml.iTemplar:
			return 0
		if iUnitType == xml.iTeutonic:
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
		if self.getPowerful() == -1:
			self.setLeader( self.getFavorite() )
			if self.getParticipate():
				self.informLeaderPopup()
			elif utils.isActive(iHuman):
				CyInterface().addMessage(iHuman, True, con.iDuration/2, gc.getPlayer( self.getLeader() ).getName() + CyTranslator().getText("TXT_KEY_CRUSADE_LEAD", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
			return

		iFavorite = self.getFavorite()
		iPowerful = self.getPowerful()
		if iFavorite == iHuman:
			iFavorVotes = 0
		else:
			iFavorVotes = self.getVotingPower( iFavorite )
		if iPowerful == iHuman:
			iPowerVotes = 0
		else:
			iPowerVotes = self.getVotingPower( iPowerful )

		#print( " AI Voting for self", iFavorVotes, iPowerVotes )

		for iPlayer in range( con.iNumPlayers ):
			if iPlayer == iHuman or iPlayer == iFavorite or iPlayer == iPowerful: continue
			iVotes = self.getVotingPower( iPlayer )
			if iVotes > 0:
				# vote AI
				#print( " AI now voting ",i,iVotes )
				if gc.getRelationTowards( iPlayer, iFavorite ) > gc.getRelationTowards( iPlayer, iPowerful ):
					iFavorVotes += iVotes
				else:
					iPowerVotes += iVotes

		print( " AI Voting ", iFavorVotes, iPowerVotes )

		self.setVotesGatheredFavorite( iFavorVotes )
		self.setVotesGatheredPowerful( iPowerVotes )

	def voteForCandidatesHuman( self ):
		if self.getParticipate() and not self.getPowerful() == -1:
			self.voteHumanPopup()

	def selectVoteWinner( self ):
		if self.getVotesGatheredPowerful() > self.getVotesGatheredFavorite():
			self.setLeader( self.getPowerful() )
		else:
			self.setLeader( self.getFavorite() )

		if self.getParticipate():
			self.informLeaderPopup()
		elif utils.isActive(utils.getHumanID()):
			CyInterface().addMessage(utils.getHumanID(), True, con.iDuration/2, gc.getPlayer( self.getLeader() ).getName() + CyTranslator().getText("TXT_KEY_CRUSADE_LEAD", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)

		# not yet, check to see for deviations
		#pJPlot = gc.getMap().plot( tJerusalem[0], tJerusalem[1] )
		#gc.getTeam( gc.getPlayer( self.getLeader() ) ).declareWar( pJPlot.getPlotCity().getOwner(), True, -1 )

	def decideTheRichestCatholic( self, iActiveCrusade ):
		# The First Crusade cannot be deviated
		if iActiveCrusade == 0:
			self.setRichestCatholic( -1 )
			return

		iRichest = -1
		iMoney = 0
		#iPopeMoney = gc.getPlayer( con.iPope ).getGold()
		for i in range( con.iNumPlayers-1 ):
			if self.getVotingPower( i ) > 0:
				pPlayer = gc.getPlayer( i )
				iPlayerMoney = pPlayer.getGold()
				#if ( iPlayerMoney > iMoney and iPlayerMoney > iPopeMoney ):
				if iPlayerMoney > iMoney:
					iRichest = i
					iMoney = iPlayerMoney

		if iRichest != con.iPope:
			self.setRichestCatholic( iRichest )
		else:
			self.setRichestCatholic( -1 )


	def decideDeviateHuman( self ):
		self.deviateHumanPopup()

	def decideDeviateAI( self ):
		iRichest = self.getRichestCatholic()
		bStolen = False
		if iRichest in [con.iVenecia, con.iGenoa]:
			pByzantium = gc.getPlayer( con.iByzantium )
			if pByzantium.isAlive():
				# Only if Byzantium holds Constantinople and not a vassal
				pConstantinoplePlot = gc.getMap().plot( 81, 24 ) # tCapitals[con.iByzantium]
				pConstantinopleCity = pConstantinoplePlot.getPlotCity()
				iConstantinopleOwner = pConstantinopleCity.getOwner()
				bIsNotAVassal = not utils.isAVassal(con.iByzantium)
				if iConstantinopleOwner == con.iByzantium and bIsNotAVassal:
					self.crusadeStolenAI( iRichest, con.iByzantium )
					bStolen = True
		elif iRichest in [con.iSpain, con.iPortugal, con.iAragon]:
			pCordoba = gc.getPlayer( con.iCordoba )
			if pCordoba.isAlive():
				# Only if Cordoba is Muslim and not a vassal
				bIsNotAVassal = not utils.isAVassal(con.iCordoba)
				if pCordoba.getStateReligion() == xml.iIslam and bIsNotAVassal:
					self.crusadeStolenAI( iRichest, con.iCordoba )
					bStolen = True
		elif iRichest in [con.iHungary, con.iPoland, con.iAustria]:
			pTurkey = gc.getPlayer( con.iTurkey )
			if pTurkey.isAlive():
				# Only if the Ottomans are Muslim and not a vassal
				bIsNotAVassal = not utils.isAVassal(con.iTurkey)
				if pTurkey.getStateReligion() == xml.iIslam and bIsNotAVassal:
					self.crusadeStolenAI( iRichest, con.iTurkey )
					bStolen = True
		if not bStolen:
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
		if gc.getPlayer( iTargetPlayer ).getStateReligion() == iCatholicism:
			self.setLeader( -1 )
			self.returnCrusaders()
			return
		if iTargetPlayer == iHuman:
			self.underCrusadeAttackPopup( pTargetCity.getName(), iLeader )
		elif utils.isActive(iHuman):
			sCityName = cnm.lookupName(pTargetCity, con.iPope)
			if sCityName == 'Unknown':
				sCityName = cnm.lookupName(pTargetCity, iLeader)
			sText = CyTranslator().getText("TXT_KEY_CRUSADE_START", (gc.getPlayer(iLeader).getCivilizationAdjectiveKey(), gc.getPlayer(iLeader).getName(), gc.getPlayer(iTargetPlayer).getCivilizationAdjectiveKey(), sCityName))
			CyInterface().addMessage(iHuman, False, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)

		gc.getTeam( gc.getPlayer( iLeader ).getTeam() ).declareWar( gc.getPlayer( pTargetCity.getOwner() ).getTeam(), True, -1 )

	def returnCrusaders( self ):
		for i in range( con.iNumPlayers ):
			gc.getPlayer( i ).setIsCrusader( False )

	def crusadeArrival( self, iActiveCrusade ):
		iTX, iTY = self.getTargetPlot()
		iChosenX = -1
		iChosenY = -1

		# if the leader has been destroyed, cancel the Crusade
		iLeader = self.getLeader()
		if iLeader == -1 or not gc.getPlayer( iLeader ).isAlive():
			self.returnCrusaders()
			return

		# if the target is Jerusalem, and in the mean time it has been captured by an Orthodox or Catholic player (or the owner of Jerusalem converted to a Christian religion), cancel the Crusade
		if (iTX, iTY) == tJerusalem:
			pPlot = gc.getMap().plot( tJerusalem[0], tJerusalem[1] )
			if pPlot.isCity():
				iVictim = pPlot.getPlotCity().getOwner()
				if iVictim < con.iNumMajorPlayers:
					iReligion = gc.getPlayer( iVictim ).getStateReligion()
					if iReligion in [iCatholicism, iOrthodoxy]:
						return

		# if not at war with the owner of the city, declare war
		pPlot = gc.getMap().plot( iTX, iTY )
		if pPlot.isCity():
			iVictim = pPlot.getPlotCity().getOwner()
			if iVictim != iLeader and gc.getPlayer(iVictim).getStateReligion() != iCatholicism:
				teamLeader = gc.getTeam( gc.getPlayer(iLeader).getTeam() )
				iTeamVictim = gc.getPlayer(iVictim).getTeam()
				if not teamLeader.isAtWar( iTeamVictim ):
					if teamLeader.canDeclareWar( iTeamVictim ):
						teamLeader.declareWar(iTeamVictim, False, -1)
					else:
						# we cannot declare war to the current owner of the target city
						self.returnCrusaders()
						return

		lFreeLandPlots = []
		lLandPlots = []
		for (x, y) in utils.surroundingPlots((iTX, iTY)):
			pPlot = gc.getMap().plot(x, y)
			if (pPlot.isHills() or pPlot.isFlatlands()) and not pPlot.isCity():
				lLandPlots.append((x, y))
				if pPlot.getNumUnits() == 0:
					lFreeLandPlots.append((x, y))

		# Absinthe: we try to spawn the army west from the target city (preferably northwest), or at least on as low x coordinates as possible
		#			works great both for Jerusalem (try not to spawn across the Jordan river) and for Constantinople (European side, where the actual city is located)
		#			also better for most cities in the Levant and in Egypt, and doesn't really matter for the rest
		if lFreeLandPlots:
			iChosenX = 200
			iChosenY = 200
			for tFreeLandPlot in lFreeLandPlots:
				if tFreeLandPlot[0] < iChosenX:
					iChosenX = tFreeLandPlot[0]
					iChosenY = tFreeLandPlot[1]
				elif tFreeLandPlot[0] == iChosenX:
					if tFreeLandPlot[0] > iChosenY:
						iChosenY = tFreeLandPlot[1]
		elif lLandPlots:
			iChosenX = 200
			iChosenY = 200
			for tLandPlot in lLandPlots:
				if tLandPlot[0] < iChosenX:
					iChosenX = tLandPlot[0]
					iChosenY = tLandPlot[1]
				elif tLandPlot[0] == iChosenX:
					if tLandPlot[0] > iChosenY:
						iChosenY = tLandPlot[1]
			pPlot = gc.getMap().plot(iChosenX, iChosenY)
			for i in range( pPlot.getNumUnits() ):
				pPlot.getUnit(0).kill( False, con.iBarbarian )

		print("Made Units on:", iChosenX, iChosenY, iLeader)

		# Absinthe: if a valid plot is found, make the units and send a message about the arrival to the human player
		if (iChosenX, iChosenY) != (-1, -1):
			self.crusadeMakeUnits( (iChosenX, iChosenY), iActiveCrusade )
			if utils.getHumanID() == iLeader:
				pTargetCity = gc.getMap().plot( iTX, iTY ).getPlotCity()
				sCityName = cnm.lookupName(pTargetCity, con.iPope)
				if sCityName == 'Unknown':
					sCityName = cnm.lookupName(pTargetCity, iLeader)
				CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_ARRIVAL", (sCityName, )) + "!", "", 0, "", ColorTypes(con.iGreen), iChosenX, iChosenY, True, True)
		else:
			self.returnCrusaders()

	def makeUnit(self, iUnit, iPlayer, iActiveCrusade, tCoords, iNum): #by LOQ
		'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
		pPlayer = gc.getPlayer(iPlayer)
		print ("iActiveCrusade on units arriving", iActiveCrusade)
		for i in range(iNum):
			pUnit = pPlayer.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pUnit.setMercID( -5 - iActiveCrusade ) # 3Miro: this is a hack to distinguish Crusades without making a separate variable

	def crusadeMakeUnits( self, tPlot, iActiveCrusade ):
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
		if (iTX, iTY) == tJerusalem:
			iRougeModifier = 100
			if teamLeader.isHasTech( xml.iChivalry ):
				self.makeUnit( xml.iBurgundianPaladin, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iTemplar, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iTeutonic, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iKnightofStJohns, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iGuisarme, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iCatapult, iLeader, iActiveCrusade, tPlot, 1 )
			else:
				self.makeUnit( xml.iHeavyLancer, iLeader, iActiveCrusade, tPlot, 2 )
				self.makeUnit( xml.iLancer, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iLongSwordsman, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iSpearman, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iTrebuchet, iLeader, iActiveCrusade, tPlot, 1 )
			# there are way too many generic units in most Crusades:
			if self.getSelectedUnit( 7 ) > 1:
				iReducedNumber = self.getSelectedUnit( 7 ) * 6 / 10 # note that this is before the specific Crusade reduction
				self.setSelectedUnit( 7 , iReducedNumber )
		# if the Crusade was derailed
		else:
			iRougeModifier = 200
			if teamLeader.isHasTech( xml.iChivalry ):
				self.makeUnit( xml.iKnight, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iTeutonic, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iLongSwordsman, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iGuisarme, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iCatapult, iLeader, iActiveCrusade, tPlot, 1 )
			else:
				self.makeUnit( xml.iHeavyLancer, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iLancer, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iLongSwordsman, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iSpearman, iLeader, iActiveCrusade, tPlot, 1 )
				self.makeUnit( xml.iTrebuchet, iLeader, iActiveCrusade, tPlot, 1 )
			# there are way too many generic units in most Crusades:
			if self.getSelectedUnit( 7 ) > 1:
				iReducedNumber = self.getSelectedUnit( 7 ) * 8 / 10 # note that this is before the specific Crusade reduction
				self.setSelectedUnit( 7 , iReducedNumber )

		# Absinthe: not all units should arrive near Jerusalem
		#			later Crusades have more units in the pool, so they should have bigger reduction
		iHuman = utils.getHumanID()
		pPlot = gc.getMap().plot( tJerusalem[0], tJerusalem[1] )
		iVictim = pPlot.getPlotCity().getOwner()
		# Absinthe: this reduction is very significant for an AI-controlled Jerusalem, but Crusades should remain an increasing threat to the human player
		if iVictim != iHuman:
			if iActiveCrusade == 0:
				iRougeModifier *= 7 / 5
			elif iActiveCrusade == 1:
				iRougeModifier *= 8 / 5
			elif iActiveCrusade == 2:
				iRougeModifier *= 9 / 5
			elif iActiveCrusade == 3:
				iRougeModifier *= 10 / 5
			elif iActiveCrusade == 4:
				iRougeModifier *= 12 / 5
			else:
				iRougeModifier *= 14 / 5
		else:
			if iActiveCrusade == 0:
				iRougeModifier *= 11 / 10
			elif iActiveCrusade == 1:
				iRougeModifier *= 6 / 5
			elif iActiveCrusade == 2:
				iRougeModifier *= 7 / 5
			elif iActiveCrusade == 3:
				iRougeModifier *= 8 / 5
			elif iActiveCrusade == 4:
				iRougeModifier *= 9 / 5
			else:
				iRougeModifier *= 10 / 5

		if self.getSelectedUnit( 0 ) > 0:
			self.makeUnit( xml.iTemplar, iLeader, iActiveCrusade, tPlot, self.getSelectedUnit( 0 ) * 100 / iRougeModifier )
		if self.getSelectedUnit( 1 ) > 0:
			self.makeUnit( xml.iTeutonic, iLeader, iActiveCrusade, tPlot, self.getSelectedUnit( 1 ) * 100 / iRougeModifier )
		if self.getSelectedUnit( 2 ) > 0:
			self.makeUnit( xml.iKnightofStJohns, iLeader, iActiveCrusade, tPlot, self.getSelectedUnit( 2 ) * 100 / iRougeModifier )
		if self.getSelectedUnit( 3 ) > 0:
			iKnightNumber = self.getSelectedUnit( 3 ) * 100 / iRougeModifier
			if iLeader == con.iBurgundy:
				for i in range( 0, iKnightNumber ):
					if gc.getGame().getSorenRandNum(10, 'chance for Paladin') >= 5: # Absinthe: 50% chance for a Paladin for each unit
						self.makeUnit( xml.iBurgundianPaladin, iLeader, iActiveCrusade, tPlot, 1 )
					else:
						self.makeUnit( xml.iKnight, iLeader, iActiveCrusade, tPlot, 1 )
			else:
				for i in range( 0, iKnightNumber ):
					if gc.getGame().getSorenRandNum(10, 'chance for Paladin') >= 8: # Absinthe: 20% chance for a Paladin for each unit
						self.makeUnit( xml.iBurgundianPaladin, iLeader, iActiveCrusade, tPlot, 1 )
					else:
						self.makeUnit( xml.iKnight, iLeader, iActiveCrusade, tPlot, 1 )
		if self.getSelectedUnit( 4 ) > 0:
			iLightCavNumber = self.getSelectedUnit( 4 ) * 100 / iRougeModifier
			if iLeader == con.iHungary:
				for i in range( 0, iLightCavNumber ):
					if (gc.getGame().getSorenRandNum(10, 'chance for Huszar') >= 5): # Absinthe: 50% chance for a Huszár for each unit
						self.makeUnit( xml.iHungarianHuszar, iLeader, iActiveCrusade, tPlot, 1 )
					else:
						self.makeUnit( xml.iHeavyLancer, iLeader, iActiveCrusade, tPlot, 1 )
			else:
				self.makeUnit( xml.iHeavyLancer, iLeader, iActiveCrusade, tPlot, iLightCavNumber )
		if self.getSelectedUnit( 5 ) > 0:
			self.makeUnit( xml.iLancer, iLeader, iActiveCrusade, tPlot, self.getSelectedUnit( 5 ) * 100 / iRougeModifier )
		if self.getSelectedUnit( 6 ) > 0:
			iSiegeNumber = self.getSelectedUnit( 6 ) * 100 / iRougeModifier
			if iSiegeNumber > 2:
				self.makeUnit( xml.iCatapult, iLeader, iActiveCrusade, tPlot, 2 )
				self.makeUnit( xml.iTrebuchet, iLeader, iActiveCrusade, tPlot, iSiegeNumber - 2 )
			else:
				self.makeUnit( xml.iCatapult, iLeader, iActiveCrusade, tPlot, iSiegeNumber )
		if self.getSelectedUnit( 7 ) > 0:
			iFootNumber = self.getSelectedUnit( 7 ) * 100 / iRougeModifier
			for i in range( 0, iFootNumber ):
				if gc.getGame().getSorenRandNum(2, 'coinflip') == 1: # Absinthe: 50% chance for both type
					self.makeUnit( xml.iLongSwordsman, iLeader, iActiveCrusade, tPlot, 1 )
				else:
					self.makeUnit( xml.iGuisarme, iLeader, iActiveCrusade, tPlot, 1 )


	def freeCrusaders( self, iPlayer ):
		# the majority of Crusader units will return from the Crusade, so the Crusading civ will have harder time keeping Jerusalem and the Levant
		unitList = PyPlayer( iPlayer ).getUnitList()
		iPrevGameTurn = gc.getGame().getGameTurn() - 1 # process for freeCrusaders was actually started in the previous turn, iActiveCrusade might have changed for this turn
		iActiveCrusade = self.getActiveCrusade( iPrevGameTurn ) # Absinthe: the Crusader units are called back before the next Crusade is initialized
		print ("iActiveCrusade on units returning", iActiveCrusade)
		iHuman = utils.getHumanID()
		for pUnit in unitList:
			if pUnit.getMercID() == (-5 - iActiveCrusade): # Absinthe: so this is a Crusader Unit of the active Crusade
				pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
				iOdds = 80
				iCrusadeCategory = self.unitCrusadeCategory( pUnit.getUnitType() )
				if iCrusadeCategory < 3:
					continue # Knight Orders don't return
				elif iCrusadeCategory == 7:
					iOdds = 50 # leave some defenders
				if pPlot.isCity():
					if pPlot.getPlotCity().getOwner() == iPlayer:
						iDefenders = self.getNumDefendersAtPlot( pPlot )
						if iDefenders < 4:
							iOdds = 20
							if iDefenders == 0:
								continue

				if gc.getGame().getSorenRandNum(100, 'free Crusaders') < iOdds:
					pUnit.kill( 0, -1 )
					if iHuman == iPlayer:
						CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_CRUSADE_CRUSADERS_RETURNING_HOME", ()) + " " + pUnit.getName(), "", 0, "", ColorTypes(con.iLime), -1, -1, True, True)

		# benefits for the other participants on Crusade return - Faith points, GG points
		for iCiv in range( con.iNumPlayers-1 ): # no such benefits for the Pope
			if iCiv == iPlayer: continue # not the leader
			pCiv = gc.getPlayer( iCiv )
			if pCiv.getStateReligion() == iCatholicism:
				iUnitNumber = self.getNumUnitsSent( iCiv )
				if iUnitNumber > 0:
					if iCiv == iHuman:
						CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_CRUSADERS_ARRIVED_HOME", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
					pCiv.changeCombatExperience( 10 * iUnitNumber )
					pCiv.changeFaith( 2 * iUnitNumber )

	# Absinthe: called from CvRFCEventHandler.onCityAcquired
	def success( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		if not self.hasSucceeded():
			pPlayer.changeGoldenAgeTurns( gc.getPlayer( iPlayer).getGoldenAgeLength() )
			self.setSucceeded()
			for (x, y) in utils.surroundingPlots(tJerusalem):
				pPlot = gc.getMap().plot( x, y )
				utils.convertPlotCulture(pPlot, iPlayer, 100, False)


	# Absinthe: pilgrims in Jerusalem if it's held by a Catholic civ
	def checkPlayerTurn(self, iGameTurn, iPlayer):
		if iGameTurn % 3 == 1: # checked every 3rd turn
			pCity = gc.getMap().plot(tJerusalem[0], tJerusalem[1]).getPlotCity()
			if pCity.getOwner() == iPlayer:
				pPlayer = gc.getPlayer( iPlayer )
				if pPlayer.getStateReligion() == iCatholicism:
					# possible population gain, chance based on the current size
					iRandom = gc.getGame().getSorenRandNum(10, 'random pop threshold')
					if (1 + pCity.getPopulation()) <= iRandom: # 1 -> 80%, 2 -> 70%, 3 -> 60% ...  7 -> 20%, 8 -> 10%, 9+ -> 0%
						pCity.changePopulation(1)
						if iPlayer == utils.getHumanID():
							CyInterface().addMessage(iPlayer, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_CRUSADE_JERUSALEM_PILGRIMS", ()), "", 0, "", ColorTypes(con.iGreen), pCity.getX(), pCity.getY(), True, True)
						# spread Catholicism if not present
						if not pCity.isHasReligion( iCatholicism ):
							pCity.setHasReligion(iCatholicism, True, True, False)


	def doDC( self, iGameTurn ):
		#print(" DC Check 1",iGameTurn,self.getDCLast())
		if iGameTurn < self.getDCLast() + 15: # wait 15 turns between DCs (Defensive Crusades)
			return
		if iGameTurn % 5 != gc.getGame().getSorenRandNum(5, 'roll to see if we should DC'): # otherwise every turn gets too much to check
			return
		if gc.getGame().getSorenRandNum(3, 'Random entry') == 0: # 33% chance for no DC
			return
		#print(" DC Check")
		lPotentials = [iPlayer for iPlayer in range(con.iNumPlayers-1) if self.canDC(iPlayer, iGameTurn)] # exclude the Pope
		if lPotentials:
			#print(" Oh, Holy Father, someone needs help! " )
			pPope = gc.getPlayer( con.iPope )
			lWeightValues = []
			for iPlayer in lPotentials:
				iCatholicFaith = 0
				pPlayer = gc.getPlayer(iPlayer)
				# while faith points matter more, diplomatic relations are also very important
				iCatholicFaith += pPlayer.getFaith()
				iCatholicFaith += 3 * max(0, pPope.AI_getAttitude(iPlayer))
				if iCatholicFaith > 0:
					lWeightValues.append((iPlayer, iCatholicFaith))
			iChosenPlayer = utils.getRandomByWeight(lWeightValues)
			if iChosenPlayer != -1:
				#print(" DC Chosen ", iChosenPlayer)
				if iChosenPlayer == utils.getHumanID():
					self.callDCHuman()
				else:
					self.callDCAI( iChosenPlayer )
				self.setDCLast( iGameTurn )


	def canDC( self, iPlayer, iGameTurn ):
		#print(" DC Chech for player ",iPlayer,iGameTurn)
		pPlayer = gc.getPlayer( iPlayer )
		teamPlayer = gc.getTeam( pPlayer.getTeam() )
		# only born, flipped and living Catholics can DC
		if (iGameTurn < con.tBirth[iPlayer]+5) or not pPlayer.isAlive() or pPlayer.getStateReligion() != iCatholicism:
			return False
		# need to have open borders with the Pope
		if not teamPlayer.isOpenBorders( gc.getPlayer( con.iPope ).getTeam() ):
			return False

		tPlayerDCMap = tDefensiveCrusadeMap[iPlayer]
		# Can DC if at war with a non-catholic/orthodox enemy, enemy is not a vassal of a catholic/orthodox civ and has a city in the DC map
		for iEnemy in range( con.iNumPlayers-1 ): # exclude the Pope
			pEnemy = gc.getPlayer( iEnemy )
			if teamPlayer.isAtWar( pEnemy.getTeam() ) and con.tBirth[iEnemy] + 10 < iGameTurn:
				if self.isOrMasterChristian(iEnemy):
					continue
				for pCity in utils.getCityList(iEnemy):
					if ProvMap[pCity.getY()][pCity.getX()] in tPlayerDCMap:
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
			if gc.getTeam( pHuman.getTeam() ).canContact( pPlayer.getTeam() ) or pHuman.getStateReligion() == iCatholicism: # as you have contact with the Pope by default
				sText = CyTranslator().getText("TXT_KEY_CRUSADE_DEFENSIVE_AI_MESSAGE", ()) + " " + pPlayer.getName()
				CyInterface().addMessage(iHuman, True, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
		self.makeDCUnits( iPlayer )
		pPlayer.changeFaith( - min( 2, pPlayer.getFaith() ) )


	def eventApply7625( self, popupReturn ):
		iDecision = popupReturn.getButtonClicked()
		iHuman = utils.getHumanID()
		pHuman = gc.getPlayer( iHuman )
		if iDecision == 0:
			self.makeDCUnits( iHuman )
			pHuman.changeFaith( - min( 2, pHuman.getFaith() ) )
		# else:
			# #pHuman.changeFaith( - min( 1, pHuman.getFaith() ) )
			# pass


	def makeDCUnits( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		print(" Crusade Defensive for: ",pPlayer.getName() )
		iFaith = pPlayer.getFaith()
		iBestInfantry = self.getDCBestInfantry( iPlayer )
		iBestCavalry = self.getDCBestCavalry( iPlayer )
		pCapital = pPlayer.getCapitalCity()
		if pCapital:
			iX = pCapital.getX()
			iY = pCapital.getY()
		else:
			city = utils.getRandomEntry(utils.getCityList(iPlayer))
			if city:
				iX = city.getX()
				iY = city.getY()
			else:
				return

		# Absinthe: interface message for the player
		if gc.getPlayer(iPlayer).isHuman():
			CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_CRUSADE_DEFENSIVE_HUMAN_MESSAGE", ()), "", 0, "", ColorTypes(con.iGreen), iX, iY, True, True)

		pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		# smaller Empires need a bit more help
		if pPlayer.getNumCities() < 6:
			if iBestCavalry == xml.iKnight:
				if gc.getGame().getSorenRandNum(10, 'chance for Paladin') >= 7: # 30% chance for a Paladin
					pPlayer.initUnit(xml.iBurgundianPaladin, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				else:
					pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			else:
				pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		if iFaith > 4:
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if iFaith > 11:
			if iBestCavalry == xml.iKnight:
				if gc.getGame().getSorenRandNum(10, 'chance for Paladin') >= 7: # 30% chance for a Paladin
					pPlayer.initUnit(xml.iBurgundianPaladin, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				else:
					pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			else:
				pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if iFaith > 20:
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		if iFaith > 33:
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		# extra units for the AI, it is dumb anyway
		if not iPlayer == utils.getHumanID():
			pPlayer.initUnit(iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			if iBestCavalry == xml.iKnight:
				if gc.getGame().getSorenRandNum(10, 'chance for Paladin') >= 7: # 30% chance for a Paladin
					pPlayer.initUnit(xml.iBurgundianPaladin, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				else:
					pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			else:
				pPlayer.initUnit(iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)


	def getDCBestInfantry( self, iPlayer ):
		pPlayer = gc.getPlayer(iPlayer)
		lUnits = [xml.iGrenadier, xml.iMaceman, xml.iLongSwordsman, xml.iSwordsman]
		for iUnit in lUnits:
			if pPlayer.canTrain(utils.getUniqueUnit(iPlayer, iUnit), False, False):
				return utils.getUniqueUnit(iPlayer, iUnit)
		return utils.getUniqueUnit(iPlayer, xml.iAxeman)


	def getDCBestCavalry( self, iPlayer ):
		pPlayer = gc.getPlayer(iPlayer)
		lUnits = [xml.iCuirassier, xml.iKnight, xml.iHeavyLancer, xml.iLancer]
		for iUnit in lUnits:
			if pPlayer.canTrain(utils.getUniqueUnit(iPlayer, iUnit), False, False):
				return utils.getUniqueUnit(iPlayer, iUnit)
		return utils.getUniqueUnit(iPlayer, xml.iScout)

	def do1200ADCrusades( self ):
		self.setCrusadeInit(0, xml.i1096AD)
		self.setCrusadeInit(1, xml.i1147AD)
		self.setCrusadeInit(2, xml.i1187AD)

	def isOrMasterChristian(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iReligion = pPlayer.getStateReligion()
		if iReligion in [iCatholicism, iOrthodoxy]:
			return True
		iMaster = utils.getMaster(iPlayer)
		if iMaster != -1:
			iMasterReligion = gc.getPlayer(iMaster).getStateReligion()
			if iMasterReligion in [iCatholicism, iOrthodoxy]:
				return True
		return False