# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
import Popup
import cPickle as pickle		# LOQ 2005-10-12
import CvTranslator
import RFCUtils
import ProvinceManager # manage provinces here to link to spawn/rebirth
import Consts as con
import XMLConsts as xml


################
### Globals ###
##############

gc = CyGlobalContext()	# LOQ
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 66
iRebellionDelay = 15
iEscapePeriod = 30
tAIStopBirthThreshold = con.tAIStopBirthThreshold
tBirth = con.tBirth

iWorker = xml.iWorker
iSettler = xml.iSettler
iSpearman = xml.iSpearman

# initialise player variables
iBurgundy = con.iBurgundy
iByzantium = con.iByzantium
iFrankia = con.iFrankia
iArabia = con.iArabia
iBulgaria = con.iBulgaria
iCordoba = con.iCordoba
iSpain = con.iSpain
iNorway = con.iNorway
iDenmark = con.iDenmark
iVenecia = con.iVenecia
iNovgorod = con.iNovgorod
iKiev = con.iKiev
iHungary = con.iHungary
iGermany = con.iGermany
iScotland = con.iScotland
iPoland = con.iPoland
iMoscow = con.iMoscow
iGenoa = con.iGenoa
iMorocco = con.iMorocco
iEngland = con.iEngland
iPortugal = con.iPortugal
iAragon = con.iAragon
iPrussia = con.iPrussia
iLithuania = con.iLithuania
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

pBurgundy = gc.getPlayer(iBurgundy)
pByzantium = gc.getPlayer(iByzantium)
pFrankia = gc.getPlayer(iFrankia)
pArabia = gc.getPlayer(iArabia)
pBulgaria = gc.getPlayer(iBulgaria)
pCordoba = gc.getPlayer(iCordoba)
pSpain = gc.getPlayer(iSpain)
pNorway = gc.getPlayer(iNorway)
pDenmark = gc.getPlayer(iDenmark)
pVenecia = gc.getPlayer(iVenecia)
pNovgorod = gc.getPlayer(iNovgorod)
pKiev = gc.getPlayer(iKiev)
pHungary = gc.getPlayer(iHungary)
pGermany = gc.getPlayer(iGermany)
pScotland = gc.getPlayer(iScotland)
pPoland = gc.getPlayer(iPoland)
pMoscow = gc.getPlayer(iMoscow)
pGenoa = gc.getPlayer(iGenoa)
pMorocco = gc.getPlayer(iMorocco)
pEngland = gc.getPlayer(iEngland)
pPortugal = gc.getPlayer(iPortugal)
pAragon = gc.getPlayer(iAragon)
pPrussia = gc.getPlayer(iPrussia)
pLithuania = gc.getPlayer(iLithuania)
pAustria = gc.getPlayer(iAustria)
pTurkey = gc.getPlayer(iTurkey)
pSweden = gc.getPlayer(iSweden)
pDutch = gc.getPlayer(iDutch)
pPope = gc.getPlayer(iPope)
pIndependent = gc.getPlayer(iIndependent)
pIndependent2 = gc.getPlayer(iIndependent2)
pIndependent3 = gc.getPlayer(iIndependent3)
pIndependent4 = gc.getPlayer(iIndependent4)
pBarbarian = gc.getPlayer(iBarbarian)

teamBurgundy = gc.getTeam(pBurgundy.getTeam())
teamByzantium = gc.getTeam(pByzantium.getTeam())
teamFrankia = gc.getTeam(pFrankia.getTeam())
teamArabia = gc.getTeam(pArabia.getTeam())
teamBulgaria = gc.getTeam(pBulgaria.getTeam())
teamCordoba = gc.getTeam(pCordoba.getTeam())
teamSpain = gc.getTeam(pSpain.getTeam())
teamNorway = gc.getTeam(pNorway.getTeam())
teamDenmark = gc.getTeam(pDenmark.getTeam())
teamVenecia = gc.getTeam(pVenecia.getTeam())
teamNovgorod = gc.getTeam(pNovgorod.getTeam())
teamKiev = gc.getTeam(pKiev.getTeam())
teamHungary = gc.getTeam(pHungary.getTeam())
teamGermany = gc.getTeam(pGermany.getTeam())
teamScotland = gc.getTeam(pScotland.getTeam())
teamPoland = gc.getTeam(pPoland.getTeam())
teamMoscow = gc.getTeam(pMoscow.getTeam())
teamGenoa = gc.getTeam(pGenoa.getTeam())
teamMorocco = gc.getTeam(pMorocco.getTeam())
teamEngland = gc.getTeam(pEngland.getTeam())
teamPortugal = gc.getTeam(pPortugal.getTeam())
teamAragon = gc.getTeam(pAragon.getTeam())
teamPrussia = gc.getTeam(pPrussia.getTeam())
teamLithuania = gc.getTeam(pLithuania.getTeam())
teamAustria = gc.getTeam(pAustria.getTeam())
teamTurkey = gc.getTeam(pTurkey.getTeam())
teamSweden = gc.getTeam(pSweden.getTeam())
teamDutch = gc.getTeam(pDutch.getTeam())
teamPope = gc.getTeam(pPope.getTeam())
teamIndependent = gc.getTeam(pIndependent.getTeam())
teamIndependent2 = gc.getTeam(pIndependent2.getTeam())
teamIndependent3 = gc.getTeam(pIndependent3.getTeam())
teamIndependent4 = gc.getTeam(pIndependent4.getTeam())
teamBarbarian = gc.getTeam(pBarbarian.getTeam())


#This is now obsolete
#for not allowing new civ popup if too close
#Sedna17, moving around the order in which civs rise without changing their WBS requires you to do funny things here to prevent "Change Civ?" popups
#Spain and Moscow have really long delays for this reason
#This is now obsolete
#tDifference = (0, 0, 0, 1, 0, 1, 10, 0, 0, 1, 0, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

tVisible = con.tVisible


# starting locations coordinates and respawn coords
tCapitals = con.tCapitals
tNewCapitals = con.tNewCapitals


# core areas coordinates (top left and bottom right)

tCoreAreasTL = con.tCoreAreasTL
tCoreAreasBR = con.tCoreAreasBR

tExceptions = con.tExceptions

tNormalAreasTL = con.tNormalAreasTL
tNormalAreasBR = con.tNormalAreasBR

tBroaderAreasTL = con.tBroaderAreasTL
tBroaderAreasBR = con.tBroaderAreasBR

tLeaders = con.tLeaders
tEarlyLeaders = con.tEarlyLeaders
tLateLeaders = con.tLateLeaders

class RiseAndFall:

	def __init__(self):
		self.pm = ProvinceManager.ProvinceManager()
		# Init the Province Manager

##################################################
### Secure storage & retrieval of script data ###
################################################


	def getNewCiv( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['iNewCiv']

	def setNewCiv( self, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iNewCiv'] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getNewCivFlip( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['iNewCivFlip']

	def setNewCivFlip( self, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iNewCivFlip'] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getOldCivFlip( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['iOldCivFlip']

	def setOldCivFlip( self, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iOldCivFlip'] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getTempTopLeft( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['tempTopLeft']

	def setTempTopLeft( self, tNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['tempTopLeft'] = tNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getTempBottomRight( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['tempBottomRight']

	def setTempBottomRight( self, tNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['tempBottomRight'] = tNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getSpawnWar( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['iSpawnWar']

	def setSpawnWar( self, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iSpawnWar'] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getAlreadySwitched( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['bAlreadySwitched']

	def setAlreadySwitched( self, bNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['bAlreadySwitched'] = bNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getColonistsAlreadyGiven( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lColonistsAlreadyGiven'][iCiv]

	def setColonistsAlreadyGiven( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lColonistsAlreadyGiven'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getNumCities( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lNumCities'][iCiv]

	def setNumCities( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lNumCities'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getSpawnDelay( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lSpawnDelay'][iCiv]

	def setSpawnDelay( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lSpawnDelay'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getFlipsDelay( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lFlipsDelay'][iCiv]

	def setFlipsDelay( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lFlipsDelay'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getBetrayalTurns( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['iBetrayalTurns']

	def setBetrayalTurns( self, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iBetrayalTurns'] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getLatestFlipTurn( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['iLatestFlipTurn']

	def setLatestFlipTurn( self, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iLatestFlipTurn'] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getLatestRebellionTurn( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lLatestRebellionTurn'][iCiv]

	def setLatestRebellionTurn( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lLatestRebellionTurn'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getRebelCiv( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['iRebelCiv']

	def setRebelCiv( self, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iRebelCiv'] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getRebelCities( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lRebelCities']

	def setRebelCities( self, lCityList ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lRebelCities'] = lCityList
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getRebelSuppress( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lRebelSuppress']

	def setRebelSuppress( self, lSuppressList ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lRebelSuppress'] = lSuppressList
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getExileData( self, i ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lExileData'][i]

	def setExileData( self, i, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lExileData'][i] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getTempFlippingCity( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['tempFlippingCity']

	def setTempFlippingCity( self, tNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['tempFlippingCity'] = tNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getCheatersCheck( self, i ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lCheatersCheck'][i]

	def setCheatersCheck( self, i, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lCheatersCheck'][i] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getBirthTurnModifier( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lBirthTurnModifier'][iCiv]

	def setBirthTurnModifier( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lBirthTurnModifier'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getDeleteMode( self, i ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lDeleteMode'][i]

	def setDeleteMode( self, i, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lDeleteMode'][i] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getFirstContactConquerors( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lFirstContactConquerors'][iCiv]

	def setFirstContactConquerors( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lFirstContactConquerors'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	#Sedna17 Respawn
	def setRespawnTurn( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lRespawnTurns'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getAllRespawnTurns( self):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lRespawnTurns']


###############
### Popups ###
#############

	''' popupID has to be a registered ID in CvRhyesCatapultEventManager.__init__!! '''
	def showPopup(self, popupID, title, message, labels):
		popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
		    popup.addButton( i )
		popup.launch(False)


	def newCivPopup(self, iCiv):
		self.showPopup(7614, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), CyTranslator().getText("TXT_KEY_NEWCIV_MESSAGE", (gc.getPlayer(iCiv).getCivilizationAdjectiveKey(),)), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
		self.setNewCiv(iCiv)

	def eventApply7614(self, popupReturn):
		if( popupReturn.getButtonClicked() == 0 ): # 1st button
			iOldHandicap = gc.getActivePlayer().getHandicapType()
			gc.getActivePlayer().setHandicapType(gc.getPlayer(self.getNewCiv()).getHandicapType())
			gc.getGame().setActivePlayer(self.getNewCiv(), False)
			gc.getPlayer(self.getNewCiv()).setHandicapType(iOldHandicap)
			#for i in range(con.iNumStabilityParameters):
			#	utils.setStabilityParameters(utils.getHumanID(),i, 0)
			#	utils.setLastRecordedStabilityStuff(0, 0)
			#	utils.setLastRecordedStabilityStuff(1, 0)
			#	utils.setLastRecordedStabilityStuff(2, 0)
			#	utils.setLastRecordedStabilityStuff(3, 0)
			#	utils.setLastRecordedStabilityStuff(4, 0)
			#	utils.setLastRecordedStabilityStuff(5, 0)
			for iMaster in range(con.iNumPlayers):
				if (gc.getTeam(gc.getPlayer(self.getNewCiv()).getTeam()).isVassal(iMaster)):
					gc.getTeam(gc.getPlayer(self.getNewCiv()).getTeam()).setVassal(iMaster, False, False)
			self.setAlreadySwitched(True)
			gc.getPlayer(self.getNewCiv()).setPlayable(True)
			#CyInterface().addImmediateMessage("first button", "")
		#elif( popupReturn.getButtonClicked() == 1 ): # 2nd button
			#CyInterface().addImmediateMessage("second button", "")


	def flipPopup(self, iNewCiv, tTopLeft, tBottomRight):
		iHuman = utils.getHumanID()
		flipText = CyTranslator().getText("TXT_KEY_FLIPMESSAGE1", ())
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				pCurrent = gc.getMap().plot( x, y )
				if ( pCurrent.isCity()):
					if (pCurrent.getPlotCity().getOwner() == iHuman):
						if (not pCurrent.getPlotCity().isCapital()):
							flipText += (pCurrent.getPlotCity().getName() + "\n")
		#exceptions
		if (len(tExceptions[iNewCiv])):
			for j in range(len(tExceptions[iNewCiv])):
				pCurrent = gc.getMap().plot( tExceptions[iNewCiv][j][0], tExceptions[iNewCiv][j][1] )
				if (pCurrent.isCity()):
					if (pCurrent.getPlotCity().getOwner() == iHuman):
						if (not pCurrent.getPlotCity().isCapital()):
							flipText += (pCurrent.getPlotCity().getName() + "\n")
		flipText += CyTranslator().getText("TXT_KEY_FLIPMESSAGE2", ())

		self.showPopup(7615, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), flipText, (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
		self.setNewCivFlip(iNewCiv)
		self.setOldCivFlip(iHuman)
		self.setTempTopLeft(tTopLeft)
		self.setTempBottomRight(tBottomRight)

	def eventApply7615(self, popupReturn):
		iHuman = utils.getHumanID()
		tTopLeft = self.getTempTopLeft()
		tBottomRight = self.getTempBottomRight()
		iNewCivFlip = self.getNewCivFlip()

		humanCityList = []
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				pCurrent = gc.getMap().plot( x, y )
				if ( pCurrent.isCity()):
					city = pCurrent.getPlotCity()
					if (city.getOwner() == iHuman):
						if (not city.isCapital()):
							humanCityList.append(city)
		#exceptions
		if (len(tExceptions[iNewCivFlip])):
			for j in range(len(tExceptions[self.getNewCivFlip()])):
				pCurrent = gc.getMap().plot( tExceptions[iNewCivFlip][j][0], tExceptions[iNewCivFlip][j][1] )
				if (pCurrent.isCity()):
					city = pCurrent.getPlotCity()
					if (city.getOwner() == iHuman):
						if (not city.isCapital()):
							humanCityList.append(city)

		if( popupReturn.getButtonClicked() == 0 ): # 1st button
			print ("Flip agreed")
			CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_AGREED", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)

			if (len(humanCityList)):
				for i in range(len(humanCityList)):
					city = humanCityList[i]
					print ("flipping ", city.getName())
					utils.cultureManager((city.getX(),city.getY()), 100, iNewCivFlip, iHuman, False, False, False)
					utils.flipUnitsInCityBefore((city.getX(),city.getY()), iNewCivFlip, iHuman)
					self.setTempFlippingCity((city.getX(),city.getY()))
					utils.flipCity((city.getX(), city.getY()), 0, 0, iNewCivFlip, [iHuman])
					utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCivFlip)

					#iEra = gc.getPlayer(iNewCivFlip).getCurrentEra()
					#if (iEra >= 2): #medieval
					#	if (city.getPopulation() < iEra):
					#		city.setPopulation(iEra) #causes an unidentifiable C++ exception

					#humanCityList[i].setHasRealBuilding(con.iPlague, False) #buggy

			#same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
			for x in range(tTopLeft[0], tBottomRight[0]+1):
				for y in range(tTopLeft[1], tBottomRight[1]+1):
					betrayalPlot = gc.getMap().plot(x,y)
					iNumUnitsInAPlot = betrayalPlot.getNumUnits()
					if (iNumUnitsInAPlot):
						for i in range(iNumUnitsInAPlot):
							unit = betrayalPlot.getUnit(i)
							if (unit.getOwner() == iHuman):
								rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
								if (rndNum >= iBetrayalThreshold):
									if (unit.getDomainType() == 2): #land unit
										iUnitType = unit.getUnitType()
										unit.kill(False, iNewCivFlip)
										utils.makeUnit(iUnitType, iNewCivFlip, (x,y), 1)
										i = i - 1

			if (self.getCheatersCheck(0) == 0):
				self.setCheatersCheck(0, iCheatersPeriod)
				self.setCheatersCheck(1, self.getNewCivFlip())

		elif( popupReturn.getButtonClicked() == 1 ): # 2nd button
			print ("Flip disagreed")
			CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)


			if (len(humanCityList)):
				for i in range(len(humanCityList)):
					city = humanCityList[i]
					#city.setCulture(self.getNewCivFlip(), city.countTotalCulture(), True)
					pCurrent = gc.getMap().plot(city.getX(), city.getY())
					oldCulture = pCurrent.getCulture(iHuman)
					pCurrent.setCulture(iNewCivFlip, oldCulture/2, True)
					pCurrent.setCulture(iHuman, oldCulture/2, True)
					iWar = self.getSpawnWar() + 1
					self.setSpawnWar(iWar)
					if (self.getSpawnWar() == 1):
						#CyInterface().addImmediateMessage(CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "")
						gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).declareWar(iHuman, False, -1) ##True??
						self.setBetrayalTurns(iBetrayalPeriod)
						self.initBetrayal()


	def rebellionPopup(self, iRebelCiv, iNumCities ):
		iLoyalPrice = min( (10 * gc.getPlayer( utils.getHumanID() ).getGold()) / 100, 50 * iNumCities )
		self.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_HUMAN", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
				(CyTranslator().getText("TXT_KEY_REBELLION_LETGO", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_DONOTHING", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_CRACK", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_BRIBE", ()) + " " + str(iLoyalPrice), \
				CyTranslator().getText("TXT_KEY_REBELLION_BOTH", ())))


	def eventApply7622(self, popupReturn):
		iHuman = utils.getHumanID()
		iRebelCiv = self.getRebelCiv()
		iChoice = popupReturn.getButtonClicked()
		lCityList = self.getRebelCities()
		iNumCities = len( lCityList )
		if ( iChoice == 1 ):
			lList = self.getRebelSuppress()
			lList[iHuman] = 2 # let go + war
			self.setRebelSuppress( lList )
		elif( iChoice == 2 ):
			if ( gc.getGame().getSorenRandNum(100, 'odds') < 40 ):
				lCityList = self.getRebelCities()
				for iCity in range( len( lCityList ) ):
					pCity = gc.getMap().plot( lCityList[iCity][0], lCityList[iCity][1] ).getPlotCity()
					if ( pCity.getOwner() == iHuman ):
						pCity.changeOccupationTimer( 2 )
						pCity.changeHurryAngerTimer( 10 )
				lList = self.getRebelSuppress()
				lList[iHuman] = 3 # keep cities + war
				self.setRebelSuppress( lList )
			else:
				lList = self.getRebelSuppress()
				lList[iHuman] = 4 # let go + war
				self.setRebelSuppress( lList )
		elif( iChoice == 3 ):
			iLoyalPrice = min( (10 * gc.getPlayer( iHuman ).getGold()) / 100, 50 * iNumCities )
			gc.getPlayer( iHuman ).setGold( gc.getPlayer( iHuman ).getGold() - iLoyalPrice )
			if ( gc.getGame().getSorenRandNum(100, 'odds') < iLoyalPrice / iNumCities ):
				lList = self.getRebelSuppress()
				lList[iHuman] = 1 # keep + no war
				self.setRebelSuppress( lList )
		elif( iChoice == 4 ):
			iLoyalPrice = min( (10 * gc.getPlayer( iHuman ).getGold()) / 100, 50 * iNumCities )
			gc.getPlayer( iHuman ).setGold( gc.getPlayer( iHuman ).getGold() - iLoyalPrice )
			if ( gc.getGame().getSorenRandNum(100, 'odds') < iLoyalPrice / iNumCities + 40 ):
				lCityList = self.getRebelCities()
				for iCity in range( len( lCityList ) ):
					pCity = gc.getMap().plot( lCityList[iCity][0], lCityList[iCity][1] ).getPlotCity()
					if ( pCity.getOwner() == iHuman ):
						pCity.changeOccupationTimer( 2 )
						pCity.changeHurryAngerTimer( 10 )
				lList = self.getRebelSuppress()
				lList[iHuman] = 3 # keep + war
				self.setRebelSuppress( lList )

			else:
				lList = self.getRebelSuppress()
				lList[iHuman] = 2 # let go + war
				self.setRebelSuppress( lList )
		self.resurectCiv( self.getRebelCiv() )



#######################################
### Main methods (Event-Triggered) ###
#####################################

	def setup(self):

		self.pm.setup()

		#self.setupBirthTurnModifiers() #causes a crash on civ switch?

		# 3Miro:
		#if (not gc.getPlayer(0).isPlayable()): #late start condition
		#	self.clear600ADChina()

		#if (gc.getPlayer(0).isPlayable()): #late start condition
		self.create4000BCstartingUnits()
		#else:
		#	self.create600ADstartingUnits()
		#self.assign4000BCtechs()
		self.setEarlyLeaders()

		#Sedna17 Respawn setup special respawn turns
		self.setupRespawnTurns()

		# set starting gold
		pBurgundy.changeGold(250)
		pByzantium.changeGold(1000)
		pFrankia.changeGold(50)
		pArabia.changeGold(200)
		pBulgaria.changeGold(100)
		pCordoba.changeGold(200)
		pSpain.changeGold(500)
		pNorway.changeGold( 250 )
		pDenmark.changeGold( 300 )
		pVenecia.changeGold(300)
		pNovgorod.changeGold(400)
		pKiev.changeGold(250)
		pHungary.changeGold(300)
		pGermany.changeGold(300)
		pScotland.changeGold(300)
		pPoland.changeGold(300)
		pPrussia.changeGold(300)
		pLithuania.changeGold(400)
		pMoscow.changeGold(400)
		pGenoa.changeGold(400)
		pMorocco.changeGold(400)
		pEngland.changeGold(400)
		pPortugal.changeGold(450)
		pAragon.changeGold(450)
		pAustria.changeGold(1000)
		pTurkey.changeGold(1000)
		pSweden.changeGold(400)
		pDutch.changeGold(1500)
		pIndependent.changeGold(50)
		pIndependent2.changeGold(50)
		pIndependent3.changeGold(50)
		pIndependent4.changeGold(50)

		# display welcome message
		#self.displayWelcomePopup()

		# 3Miro: only the very first civ in the WB file
		# Sedna17: Not wanted when Burgundy spawns late?
		# 3Miro: I don't know what the point of this is, I think it has to do with the first nation spawning with no units
		#		coded in the WB, lets remove it to see what breaks
		#if (pBurgundy.isHuman()):
		#	plotBurgundy = gc.getMap().plot(tCapitals[iBurgundy][0], tCapitals[iBurgundy][1])
		#	unit = plotBurgundy.getUnit(0)
		#	unit.centerCamera()
		#center camera on Egyptian units
		#if (pEgypt.isHuman()):
		#	plotEgypt = gc.getMap().plot(tCapitals[iEgypt][0], tCapitals[iEgypt][1])
		#	unit = plotEgypt.getUnit(0)
		#	unit.centerCamera()
		#	#print (unit)


	### 3Miro Province Related Functions ###
	def onCityBuilt(self, iPlayer, pCity):
		self.pm.onCityBuilt (iPlayer, pCity.getX(), pCity.getY())
		# Absinthe: We can add free buildings for new cities here
		#			It will add the building every time a city is founded on the plot, not just on the first time
		if ( (pCity.getX()==56) and (pCity.getY()==35) ): #Venice - early defense boost, the rivers alone are not enough
			pCity.setHasRealBuilding( xml.iWalls, True )
		if ( (pCity.getX()==55) and (pCity.getY()==41) ): #Augsburg
			pCity.setHasRealBuilding( xml.iWalls, True )
		#if ( (pCity.getX()==41) and (pCity.getY()==52) ): #London
		#	pCity.setHasRealBuilding( xml.iWalls, True )
		if ( (pCity.getX()==23) and (pCity.getY()==31) ): #Porto
			pCity.setHasRealBuilding( xml.iWalls, True )
		if ( (pCity.getX()==60) and (pCity.getY()==44) ): #Prague
			pCity.setHasRealBuilding( xml.iWalls, True )
		#if ( (pCity.getX()==80) and (pCity.getY()==62) ): #Novgorod
		#	pCity.setHasRealBuilding( xml.iWalls, True )
		if ( (pCity.getX()==74) and (pCity.getY()==58) ): #Riga
			pCity.setHasRealBuilding( xml.iWalls, True )


	def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
		self.pm.onCityAcquired(owner, playerType, city, bConquest, bTrade)
		if ( playerType == iTurkey ):
			if ( city.getX() == tCapitals[iByzantium][0] and city.getY() == tCapitals[iByzantium][1] ): # Constantinople (81,24)
				apCityList = PyPlayer(playerType).getCityList()
				for pCity in apCityList:
					loopCity = pCity.GetCy()
					if (loopCity != city):
						loopCity.setHasRealBuilding((xml.iPalace), False)
				city.setHasRealBuilding((xml.iPalace), True)
				if ( pTurkey.getStateReligion() == xml.iIslam ):
					city.setHasReligion(xml.iIslam,1,1,0)

			# Absinthe: Edirne becomes capital if conquered before Constantinople
			else:
				if ( city.getX() == 76 and city.getY() == 25 ): # Adrianople/Edirne (76,25)
					apCityList = PyPlayer(playerType).getCityList()
					bHasIstanbul = False
					for pCity in apCityList: # checks if Constantinople is currently an Ottoman city
						loopCity = pCity.GetCy()
						if ( loopCity.getX() == tCapitals[iByzantium][0] and loopCity.getY() == tCapitals[iByzantium][1] ):
							bHasIstanbul = True
					if ( bHasIstanbul == False ): # if it's not, then sets all cities without palace, apart from the newly conquered Adrianople/Edirne
						for pCity in apCityList:
							loopCity = pCity.GetCy()
							if (loopCity != city):
								loopCity.setHasRealBuilding((xml.iPalace), False)
						city.setHasRealBuilding((xml.iPalace), True)
					if ( pTurkey.getStateReligion() == xml.iIslam ): # you get Islam anyway, as a bonus
						city.setHasReligion(xml.iIslam,1,1,0)


	def onCityRazed(self, iOwner, playerType, city):
		self.pm.onCityRazed(iOwner, playerType, city) # Province Manager


	def clear600ADChina(self):
		pass


	#Sedna17 Respawn
	def setupRespawnTurns(self):
		for iCiv in range(iNumMajorPlayers):
			self.setRespawnTurn(iCiv, con.tRespawnTime[iCiv]+(gc.getGame().getSorenRandNum(21, 'BirthTurnModifier') - 10)+(gc.getGame().getSorenRandNum(21, 'BirthTurnModifier2') - 10)) #bell-curve-like spawns within +/- 10 turns of desired turn (3Miro: Uniform, not a bell-curve)


	def setupBirthTurnModifiers(self):
		#3Miro: first and last civ (first that does not start)
		#Absinthe: currently unused
		for iCiv in range(iNumPlayers):
			if ((iCiv >= iArabia and not gc.getPlayer(iCiv).isHuman())):
				self.setBirthTurnModifier(iCiv, (gc.getGame().getSorenRandNum(11, 'BirthTurnModifier') - 5)) # -5 to +5
		#now make sure that no civs spawn in the same turn and cause a double "new civ" popup
		for iCiv in range(iNumPlayers):
			if (iCiv > utils.getHumanID() and iCiv < iNumPlayers):
				for j in range(iNumPlayers-1-iCiv):
					iNextCiv = iCiv+j+1
					if (con.tBirth[iCiv]+self.getBirthTurnModifier(iCiv) == con.tBirth[iNextCiv]+self.getBirthTurnModifier(iNextCiv)):
						self.setBirthTurnModifier(iNextCiv, (self.getBirthTurnModifier(iNextCiv)+1))


	def setEarlyLeaders(self):
		for i in range(iNumActivePlayers):
			if (tEarlyLeaders[i] != tLeaders[i][0]):
				if (not gc.getPlayer(i).isHuman()):
					gc.getPlayer(i).setLeader(tEarlyLeaders[i])
					print ("leader starting switch:", tEarlyLeaders[i], "in civ", i)


	def setWarOnSpawn(self):
		for i in range( iNumMajorPlayers - 1 ): # exclude the Pope
			iTeamMajor = gc.getPlayer(i).getTeam()
			pTeamMajor = gc.getTeam( iTeamMajor )
			for j in range( iNumTotalPlayers ):
				if ( con.tWarAtSpawn[i][j] > 0 ): # if there is a chance for war
					if ( gc.getGame().getSorenRandNum(100, 'war on spawn roll') < con.tWarAtSpawn[i][j] ):
						iTeamSecond = gc.getPlayer(j).getTeam()
						pTeamSecond = gc.getTeam( iTeamSecond )
						#print(" 3Miro WAR ON SPAWN between ",iTeamMajor,iTeamSecond)
						#pTeamMajor.setAtWar( iTeamSecond, True )
						#pTeamSecond.setAtWar( iTeamMajor, True )
						gc.getTeam( gc.getPlayer(i).getTeam() ).setAtWar( gc.getPlayer(j).getTeam(), True )
						gc.getTeam( gc.getPlayer(j).getTeam() ).setAtWar( gc.getPlayer(i).getTeam(), True )


	def checkTurn(self, iGameTurn):

		#Trigger betrayal mode
		if (self.getBetrayalTurns() > 0):
			self.initBetrayal()

		if (self.getCheatersCheck(0) > 0):
			teamPlayer = gc.getTeam(gc.getPlayer(utils.getHumanID()).getTeam())
			if (teamPlayer.isAtWar(self.getCheatersCheck(1))):
				print ("No cheaters!")
				self.initMinorBetrayal(self.getCheatersCheck(1))
				self.setCheatersCheck(0, 0)
				self.setCheatersCheck(1, -1)
			else:
				self.setCheatersCheck(0, self.getCheatersCheck(0)-1)

		if (iGameTurn % 20 == 0):
			for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
				pIndy = gc.getPlayer( i )
				if ( pIndy.isAlive() ):
					utils.updateMinorTechs(i, iBarbarian)
			#if (pIndependent.isAlive()):
			#	utils.updateMinorTechs(iIndependent, iBarbarian)
			#if (pIndependent2.isAlive()):
			#	utils.updateMinorTechs(iIndependent2, iBarbarian)

		# 3Miro this should be Arabia
		#iFirstSpawn = iArabia
		#for iLoopCiv in range(iFirstSpawn, iNumMajorPlayers):
		for iLoopCiv in range( iNumMajorPlayers ):
			if ( (not (tBirth[iLoopCiv] == 0) ) and iGameTurn >= con.tBirth[iLoopCiv] - 3 and iGameTurn <= con.tBirth[iLoopCiv] + 6):
				self.initBirth(iGameTurn, con.tBirth[iLoopCiv], iLoopCiv)


		#fragment utility
		# 3Miro: Shuffle cities between Indeps and barbs to make sure there is no big Indep nation
		if (iGameTurn >= 20 and iGameTurn % 15 == 6):
			self.fragmentIndependents()
		if (iGameTurn >= 20 and iGameTurn % 30 == 12):
			self.fragmentBarbarians(iGameTurn)


		# Fall of civs:
		# Barb collapse: if a little more than 1/3 of the empire is conquered and/or held by barbs = collapse
		# Generic collapse: if 1/2 of the empire is lost in only a few turns (18 I think) = collapse
		# Motherland collapse: if no city is in the core area and the number of cities in the normal area is less than the other's cities and have no vassal = collapse
		# Secession: if stability is negative there is a chance (bigger chance with worse stability) for a random city to it's declare independence
		if (iGameTurn >= 64 and iGameTurn % 4 == 0): #mainly for seljuks, mongols, timurids
			self.collapseByBarbs(iGameTurn)
		if (iGameTurn >= 34 and iGameTurn % 16 == 0): #used to be 15 in vanilla
			self.collapseGeneric(iGameTurn)
		if (iGameTurn >= 34 and iGameTurn % 9 == 7): #used to be 8 in vanilla
			self.collapseMotherland(iGameTurn)
		if (iGameTurn > 20 and iGameTurn % 3 == 1):
			self.secession(iGameTurn)

		#resurrection of civs
		# 3Miro: this should not be called with high iNumDeadCivs*
		# Sedna: This is one place to control the frequency of resurrection.
		# Generally we want to allow Kiev, Bulgaria, Cordoba, Burgundy, Byzantium at least to be dead in late game without respawning.
		# Absinthe: 12 and 8 for now, even with the new civs
		iNumDeadCivs1 = 12 #5 in vanilla RFC, 8 in warlords RFC (that includes native and celt)
		iNumDeadCivs2 = 8 #3 in vanilla RFC, 6 in Warlords RFC (where we must count natives and celts as dead too)

		iCiv = self.getSpecialRespawn( iGameTurn )
		if ( iCiv > -1 ):
			self.resurrection(iGameTurn,iCiv)
		elif (gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs1):
			if (iGameTurn % 18 == 11):
				self.resurrection(iGameTurn, -1)
		elif (gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs2):
			if (iGameTurn % 35 == 13):
				self.resurrection(iGameTurn, -1)
		#lRespawnTurns = self.getAllRespawnTurns()
		#print("Special Respawn Turns ",lRespawnTurns)
		#if iGameTurn in lRespawnTurns:
		#	iCiv = lRespawnTurns.index(iGameTurn)#Lookup index for
		#	print("Special Respawn For Player: ",iCiv)
		#	if iCiv < iNumMajorPlayers and iCiv > 0:
		#		self.resurrection(iGameTurn,iCiv)

		# Absinthe: Reduce cities to towns, in order to make room for new civs
		if(iGameTurn == con.tBirth[con.iEngland] -1):
			# Reduce Norwich and Nottingham, so more freedom in where to found cities in England
			self.reduceCity((43,55))
			self.reduceCity((39,56))
		elif(iGameTurn == con.tBirth[con.iSweden] -1):
			# Reduce Uppsala
			self.reduceCity((65,66))


	def reduceCity(self, tPlot):
		pPlot = gc.getMap().plot(tPlot[0],tPlot[1])
		if(pPlot.isCity()):
			# Apologize from the player:
			msgString = CyTranslator().getText("TXT_KEY_REDUCE_CITY_1", ()) + " " + pPlot.getPlotCity().getName() + " " + CyTranslator().getText("TXT_KEY_REDUCE_CITY_2", ())
			CyInterface().addMessage(pPlot.getPlotCity().getOwner(), True, con.iDuration, msgString, "", 0, "", ColorTypes(con.iLightRed), tPlot[0], tPlot[1], True, True)

			pPlot.eraseAIDevelopment()
			pPlot.setImprovementType(21) # Improvement Town instead of the city
			pPlot.setRouteType(0) # Also adding a road there


	def checkPlayerTurn(self, iGameTurn, iPlayer):
		#switch leader on first anarchy if early leader is different from primary one, and in a late game anarchy period to a late leader
		#if (len(tLeaders[iPlayer]) > 1):
		#	if (tEarlyLeaders[iPlayer] != tLeaders[iPlayer][0]):
		#		if (iGameTurn > tBirth[iPlayer]+3 and iGameTurn < tBirth[iPlayer]+50):
		#			if (gc.getPlayer(iPlayer).getAnarchyTurns() != 0):
		#				gc.getPlayer(iPlayer).setLeader(tLeaders[iPlayer][0])
		#				print ("leader early switch:", tLeaders[iPlayer][0], "in civ", iPlayer)
		#	elif (iGameTurn >= tLateLeaders[iPlayer][1]):
		#		if (tLateLeaders[iPlayer][0] != tLeaders[iPlayer][0]):
		#			if (gc.getPlayer(iPlayer).getAnarchyTurns() != 0):
		#				gc.getPlayer(iPlayer).setLeader(tLateLeaders[iPlayer][0])
		#				print ("leader late switch:", tLateLeaders[iPlayer][0], "in civ", iPlayer)

		# Absinthe: leader switching for up to 4 leaders
		if (len(tLeaders[iPlayer]) > 1):
			if (len(tLateLeaders[iPlayer]) > 5):
				if (len(tLateLeaders[iPlayer]) > 9):
					if (iGameTurn >= tLateLeaders[iPlayer][9]):
						self.switchLateLeaders(iPlayer, 8)
					elif (iGameTurn >= tLateLeaders[iPlayer][5]):
						self.switchLateLeaders(iPlayer, 4)
					elif (iGameTurn >= tLateLeaders[iPlayer][1]):
						self.switchLateLeaders(iPlayer, 0)
				else:
					if (iGameTurn >= tLateLeaders[iPlayer][5]):
						self.switchLateLeaders(iPlayer, 4)
					elif (iGameTurn >= tLateLeaders[iPlayer][1]):
						self.switchLateLeaders(iPlayer, 0)
			else:
				if (iGameTurn >= tLateLeaders[iPlayer][1]):
					self.switchLateLeaders(iPlayer, 0)

		# 3Miro: English cheat, the AI is utterly incompetent when it has to launch an invasion on an island
		#	if in 1300AD Dublin is still Barbarian, it will flip to England
		if ( iGameTurn == xml.i1300AD and utils.getHumanID() != iEngland and iPlayer == iEngland and pEngland.isAlive() ):
			pPlot = gc.getMap().plot( 32, 58 )
			if ( pPlot.isCity() ):
				if ( pPlot.getPlotCity().getOwner() == con.iBarbarian ):
					pDublin = pPlot.getPlotCity()
					utils.cultureManager((pDublin.getX(),pDublin.getY()), 50, iEngland, iBarbarian, False, True, True)
					utils.flipUnitsInCityBefore((pDublin.getX(),pDublin.getY()), iEngland, iBarbarian)
					self.setTempFlippingCity((pDublin.getX(),pDublin.getY()))
					utils.flipCity((pDublin.getX(),pDublin.getY()), 0, 0, iEngland, [iBarbarian])   #by trade because by conquest may raze the city
					utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iEngland)
			#print( " 3Miro: Called for - ",iPlayer," on turn ",iGameTurn )
			#utils.setLastTurnAlive( iPlayer, iGameTurn )

		# Absinthe: Another English cheat, extra defenders and defensive buildings in Normandy some turns after spawn - from RFCE++
		if( iGameTurn == xml.i1066AD + 3 and utils.getHumanID() != iEngland and iPlayer == iEngland and pEngland.isAlive() ):
			print("Giving England some help in Normandy..")
			for loopx in range(39,46):
				for loopy in range(47,51):
					print("Is ", loopx, loopy, " an English city?")
					pCurrent = gc.getMap().plot( loopx, loopy )
					if ( pCurrent.isCity()):
						pCity = pCurrent.getPlotCity()
						if(pCity.getOwner() == iEngland):
							print("Yes! Defenders get!")
							utils.makeUnit(xml.iGuisarme, iEngland, (loopx,loopy), 1)
							utils.makeUnit(xml.iArbalest, iEngland, (loopx,loopy), 1)
							pCity.setHasRealBuilding(xml.iWalls, True)
							pCity.setHasRealBuilding(xml.iCastle,True)

		# Absinthe: Prussia direction change
		if(iGameTurn == xml.i1618AD and iPlayer == iPrussia):
			pPrussia.setProvinceType( xml.iP_Estonia, con.iProvinceNone )
			pPrussia.setProvinceType( xml.iP_Livonia, con.iProvinceOuter )
			pPrussia.setProvinceType( xml.iP_Brandenburg, con.iProvinceNatural )
			pPrussia.setProvinceType( xml.iP_Silesia, con.iProvincePotential )
			pPrussia.setProvinceType( xml.iP_GreaterPoland, con.iProvinceOuter )


	def switchLateLeaders(self, iPlayer, iLeaderIndex):
		if (tLateLeaders[iPlayer][iLeaderIndex] != gc.getPlayer(iPlayer).getLeader()):
			iThreshold = tLateLeaders[iPlayer][iLeaderIndex+2]
			if (gc.getPlayer(iPlayer).getCurrentEra() >= tLateLeaders[iPlayer][iLeaderIndex+3]):
				iThreshold *= 2
			if (gc.getPlayer(iPlayer).getAnarchyTurns() != 0 or utils.getPlagueCountdown(iPlayer) > 0 or utils.getStability(iPlayer) <= -10 or gc.getGame().getSorenRandNum(100, 'die roll') < iThreshold):
				gc.getPlayer(iPlayer).setLeader(tLateLeaders[iPlayer][iLeaderIndex])
				print ("leader late switch:", tLateLeaders[iPlayer][iLeaderIndex], "in civ", iPlayer)


	def fragmentIndependents(self):
		for iTest1 in range( con.iIndepStart, con.iIndepEnd + 1):
			for iTest2 in range( con.iIndepStart, con.iIndepEnd + 1):
				if ( not (iTest1 == iTest2) ):
					pTest1 = gc.getPlayer( iTest1 )
					pTest2 = gc.getPlayer( iTest2 )
					if ( abs( pTest1.getNumCities() - pTest2.getNumCities() ) > 5 ):
						if ( pTest1.getNumCities() > pTest2.getNumCities() ):
							iBig = iTest1
							pBig = pTest1
							iSmall = iTest2
							pSmall = pTest2
						else:
							iBig = iTest2
							pBig = pTest2
							iSmall = iTest1
							pSmall = pTest1
						apCityList = PyPlayer(iBig).getCityList()
						iDivideCounter = 0
						iCounter = 0
						for pCity in apCityList:
							iDivideCounter += 1
							if (iDivideCounter % 2 == 1):
								city = pCity.GetCy()
								pCurrent = gc.getMap().plot(city.getX(), city.getY())
								utils.cultureManager((city.getX(),city.getY()), 50, iSmall, iBig, False, True, True)
								utils.flipUnitsInCityBefore((city.getX(),city.getY()), iSmall, iBig)
								self.setTempFlippingCity((city.getX(),city.getY()))
								utils.flipCity((city.getX(),city.getY()), 0, 0, iSmall, [iBig])   #by trade because by conquest may raze the city
								utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iSmall)
								iCounter += 1
							if ( iCounter == 3 ):
								break


	def fragmentBarbarians(self, iGameTurn):
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iDeadCiv = j % iNumPlayers
			if (not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > con.tBirth[iDeadCiv] + 50):
				pDeadCiv = gc.getPlayer(iDeadCiv)
				teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
				iCityCounter = 0
				for x in range(tNormalAreasTL[iDeadCiv][0], tNormalAreasBR[iDeadCiv][0]+1):
					for y in range(tNormalAreasTL[iDeadCiv][1], tNormalAreasBR[iDeadCiv][1]+1):
						pCurrent = gc.getMap().plot( x, y )
						if ( pCurrent.isCity()):
							if (pCurrent.getPlotCity().getOwner() == iBarbarian):
								iCityCounter += 1
				if (iCityCounter > 5):
					iDivideCounter = 0
					for x in range(tNormalAreasTL[iDeadCiv][0], tNormalAreasBR[iDeadCiv][0]+1):
						for y in range(tNormalAreasTL[iDeadCiv][1], tNormalAreasBR[iDeadCiv][1]+1):
							pCurrent = gc.getMap().plot( x, y )
							if ( pCurrent.isCity()):
								city = pCurrent.getPlotCity()
								if (city.getOwner() == iBarbarian):
									#if (iDivideCounter % 4 == 0):
									#	iNewCiv = iIndependent
									#elif (iDivideCounter % 4 == 1):
									#	iNewCiv = iIndependent2
									iNewCiv = con.iIndepStart + gc.getGame().getSorenRandNum(con.iIndepEnd - con.iIndepStart + 1, 'randomIndep')
									if (iDivideCounter % 4 == 0 or iDivideCounter % 4 == 1):
										utils.cultureManager((city.getX(),city.getY()), 50, iNewCiv, iBarbarian, False, True, True)
										utils.flipUnitsInCityBefore((city.getX(),city.getY()), iNewCiv, iBarbarian)
										self.setTempFlippingCity((city.getX(),city.getY()))
										utils.flipCity((city.getX(),city.getY()), 0, 0, iNewCiv, [iBarbarian])   #by trade because by conquest may raze the city
										utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
										iDivideCounter += 1
					return


	def collapseByBarbs(self, iGameTurn):
		for iCiv in range(iNumPlayers):
			if (gc.getPlayer(iCiv).isHuman() == 0 and gc.getPlayer(iCiv).isAlive()):
				# 3MiroUP: Emperor
				if (iGameTurn >= con.tBirth[iCiv] + 25 and not utils.collapseImmune(iCiv)):
					iNumCities = gc.getPlayer(iCiv).getNumCities()
					iLostCities = gc.countCitiesLostTo( iCiv, iBarbarian )
##					iLostCities = 0
##					for x in range(0, con.iMapMaxX):
##						for y in range(0, con.iMapMaxY):
##							if (gc.getMap().plot( x,y ).isCity()):
##								city = gc.getMap().plot( x,y ).getPlotCity()
##								if (city.getOwner() == iBarbarian):
##									if (city.getOriginalOwner() == iCiv):
##										iLostCities = iLostCities + 1
					if (iLostCities*2 > iNumCities+2 and iNumCities > 0): #if a little more than one third is captured, the civ collapses
						print ("COLLAPSE BY BARBS", gc.getPlayer(iCiv).getCivilizationAdjective(0))
						#utils.killAndFragmentCiv(iCiv, iIndependent, iIndependent2, -1, False)
						utils.killAndFragmentCiv(iCiv, False, False)
		# Add this part to force several cities to revolt in the case of very bad stability
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iPlayer = j % iNumPlayers
			#print(" 3Miro: player ",iPlayer)
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive() and iGameTurn >= con.tBirth[iPlayer] + 30):
				iStability = pPlayer.getStability()
				if (pPlayer.getStability() < -15 and (not utils.collapseImmune(iPlayer)) and (pPlayer.getNumCities() > 10) ): #civil war
					self.revoltCity( iPlayer, False )
					self.revoltCity( iPlayer, False )
					self.revoltCity( iPlayer, True )
					self.revoltCity( iPlayer, True )


	def collapseGeneric(self, iGameTurn):
		#lNumCitiesNew = con.l0Array
		lNumCitiesNew = con.l0ArrayTotal #for late start
		for iCiv in range(iNumTotalPlayers):
			if (iCiv < iNumActivePlayers ): #late start condition
				pCiv = gc.getPlayer(iCiv)
				teamCiv = gc.getTeam(pCiv.getTeam())
				if (pCiv.isAlive()):
					# 3MiroUP: Emperor
					if (iGameTurn >= con.tBirth[iCiv] + 25 and not utils.collapseImmune(iCiv)):
						lNumCitiesNew[iCiv] = pCiv.getNumCities()
						if (lNumCitiesNew[iCiv]*2 <= self.getNumCities(iCiv)): #if number of cities is less than half than some turns ago, the civ collapses
							print ("COLLAPSE GENERIC", pCiv.getCivilizationAdjective(0), lNumCitiesNew[iCiv]*2, "<=", self.getNumCities(iCiv))
							if (gc.getPlayer(iCiv).isHuman() == 0):
								bVassal = False
								for iMaster in range(con.iNumPlayers):
									if (teamCiv.isVassal(iMaster)):
										bVassal = True
										break
								if (not bVassal):
									#utils.killAndFragmentCiv(iCiv, iIndependent, iIndependent2, -1, False)
									utils.killAndFragmentCiv(iCiv, False, False)
						else:
							self.setNumCities(iCiv, lNumCitiesNew[iCiv])


	def collapseMotherland(self, iGameTurn):
		#collapses if completely out of core and normal areas
		for iCiv in range(iNumPlayers):
			pCiv = gc.getPlayer(iCiv)
			teamCiv = gc.getTeam(pCiv.getTeam())
			if (pCiv.isHuman() == 0 and pCiv.isAlive()):
				# 3MiroUP: Emperor
				if (iGameTurn >= con.tBirth[iCiv] + 25 and not utils.collapseImmune(iCiv)):
					if ( not gc.safeMotherland( iCiv ) ):
						print ("COLLAPSE: MOTHERLAND", gc.getPlayer(iCiv).getCivilizationAdjective(0))
						#utils.killAndFragmentCiv(iCiv, iIndependent, iIndependent2, -1, False)
						utils.killAndFragmentCiv(iCiv, False, False)


	def secession(self, iGameTurn): # checked every 3 turns
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iPlayer = j % iNumPlayers
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive() and iGameTurn >= con.tBirth[iPlayer] + 20):
				iStability = pPlayer.getStability()
				if ( gc.getGame().getSorenRandNum(10, 'do the check for city secession') < -iStability ): # x/10 chance with -x stability
					self.revoltCity( iPlayer, False )
					return # max 1 secession per turn


	def revoltCity( self, iPlayer, bForce ):
		# if bForce is true, then any city can revolt
		pPlayer = gc.getPlayer(iPlayer)
		iStability = pPlayer.getStability()

		cityList = []
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			pCurrent = gc.getMap().plot(city.getX(), city.getY())

			if ((not city.isWeLoveTheKingDay()) and (not city.isCapital()) and (not (city.getX() == tCapitals[iPlayer][0] and city.getY() == tCapitals[iPlayer][1])) and (not utils.collapseImmuneCity(iPlayer,city.getX(),city.getY()))): # 3MiroUP: Emperor
				if (pPlayer.getNumCities() > 0): # this check is needed, otherwise game crashes
					capital = gc.getPlayer(iPlayer).getCapitalCity()
					iDistance = utils.calculateDistance(city.getX(), city.getY(), capital.getX(), capital.getY())
					if (iDistance > 3):
						iProvType = pPlayer.getProvinceType( city.getProvince() )
						# Absinthe: any city can get into the revolt if it has angry population, bad health, untolerated religion, no military garrison
						if ( bForce or iProvType < con.iProvinceNatural or city.angryPopulation(0) > 1 or city.healthRate(False, 0) < -2 or city.getReligionBadHappiness() > 1 or city.getNoMilitaryPercentAnger() > 0 ):
							# Absinthe: the following random chance is not necessary, there is already one in the secession function
							#if ( gc.getGame().getSorenRandNum(100, 'city secession') < 20 - 5 * pPlayer.getStability() ): # 100% if stability is less than -15
								cityList.append(city)
								# Absinthe: cities in border/contested provinces have 4*chance to be chosen, cities in foreign provinces have 9*chance
								if ( iProvType == con.iProvinceNone ):
									cityList.append(city)
									cityList.append(city)
									cityList.append(city)
									cityList.append(city)
									cityList.append(city)
									cityList.append(city)
									cityList.append(city)
									cityList.append(city)
								if ( iProvType == con.iProvinceOuter ):
									cityList.append(city)
									cityList.append(city)
									cityList.append(city)
								continue

						# Absinthe: also add the city to the list if it has foreign culture - currently unused
						#for iLoop in range(iNumTotalPlayers+1):
						#	if (iLoop != iPlayer):
						#		if (pCurrent.getCulture(iLoop) > 0):
						#			cityList.append(city)
						#			break

		if (len(cityList)):
			#iNewCiv = iIndependent
			#iRndNum = gc.getGame().getSorenRandNum(2, 'random independent')
			#if (iRndNum % 2 == 0):
			#	iNewCiv = iIndependent2
			iRndNum = gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random independent')
			iNewCiv = con.iIndepStart + iRndNum

			splittingCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')]
			if (iPlayer == utils.getHumanID()):
				CyInterface().addMessage(iPlayer, True, con.iDuration, splittingCity.getName() + " " + CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
			utils.cultureManager((splittingCity.getX(),splittingCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
			utils.flipUnitsInCityBefore((splittingCity.getX(),splittingCity.getY()), iNewCiv, iPlayer)
			self.setTempFlippingCity((splittingCity.getX(),splittingCity.getY()))
			utils.flipCity((splittingCity.getX(),splittingCity.getY()), 0, 0, iNewCiv, [iPlayer])   #by trade because by conquest may raze the city
			utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
			#print ("SECESSION", gc.getPlayer(iPlayer).getCivilizationAdjective(0), splittingCity.getName()) #causes c++ exception??
			#Sedna17: Now loosing a city to secession gives a positive boost to stability. Should help Byzantium be less frustrating.
			#utils.setParameter(iPlayer, con.iParExpansionE, True, 5) #to counterbalance the stability hit on city acquired event, leading to a chain reaction
			#utils.setStability(iPlayer, utils.getStability(iPlayer) + 5) #to counterbalance the stability hit on city acquired event, leading to a chain reaction
			pPlayer.changeStabilityBase( con.iCathegoryExpansion, 3 )


	def resurrection(self, iGameTurn, iDeadCiv):
		if iDeadCiv == -1:
			iDeadCiv = self.findCivToResurect( iGameTurn , 0, -1)
		else:
			iDeadCiv = self.findCivToResurect( iGameTurn , 1, iDeadCiv) #For special re-spawn
		#print ("iDeadCiv", iDeadCiv)
		if ( iDeadCiv > -1 ):
			self.suppressResurection( iDeadCiv )
			#self.resurectCiv( iDeadCiv )


	def findCivToResurect( self, iGameTurn , bSpecialRespawn, iDeadCiv):
		#print("Looking up a civ to resurect, iDeadCiv: ",iDeadCiv)
		if ( bSpecialRespawn ):
			iMinNumCities = 1
		else:
			iMinNumCities = 2

		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		cityList = []
		for j in range(iRndnum, iRndnum + iNumPlayers):
			if not bSpecialRespawn:
				iDeadCiv = j % iNumPlayers
			else:
				iDeadCiv = iDeadCiv #We want a specific civ for special re-spawn
			cityList = []
			if (not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > con.tBirth[iDeadCiv] + 25 and iGameTurn > utils.getLastTurnAlive(iDeadCiv) + 10): #Sedna17: Allow re-spawns only 10 turns after death and 25 turns after birth
				pDeadCiv = gc.getPlayer(iDeadCiv)
				teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
				#3Miro: inRFC Civs spawn according to Normal Areas, but here we want Core areas. Otherwise Normal Areas should not overlap and that is Hard.
				#Sedna17: Normal Areas no longer overlap, so we can respawn here.
				tTopLeft = tNormalAreasTL[iDeadCiv]
				tBottomRight = tNormalAreasBR[iDeadCiv]
				#tTopLeft = tCoreAreasTL[iDeadCiv]
				#tBottomRight = tCoreAreasBR[iDeadCiv]

				for x in range(tTopLeft[0], tBottomRight[0]+1):
					for y in range(tTopLeft[1], tBottomRight[1]+1):
						if ((x,y) not in con.tNormalAreasSubtract[iDeadCiv]):
						#if ((x,y) not in con.tExceptions[iDeadCiv]):
							pCurrent = gc.getMap().plot( x, y )
							if ( pCurrent.isCity()):
								city = pCurrent.getPlotCity()
								print("Considering city at: (x,y) ",x,y)
								iOwner = city.getOwner()
								if (iOwner >= iNumActivePlayers): #if (iOwner == iBarbarian or iOwner == iIndependent or iOwner == iIndependent2): #remove in vanilla
									cityList.append(pCurrent.getPlotCity())
									#print (iDeadCiv, pCurrent.getPlotCity().getName(), pCurrent.getPlotCity().getOwner(), "1", cityList)
								else:
									iMinNumCitiesOwner = 3
									#iOwnerStability = utils.getStability(iOwner)
									iOwnerStability = gc.getPlayer(iOwner).getStability()
									if (not gc.getPlayer(iOwner).isHuman()):
										iMinNumCitiesOwner = 2
										iOwnerStability -= 5
									if (gc.getPlayer(iOwner).getNumCities() >= iMinNumCitiesOwner):
										if (iOwnerStability < -5):
											if (not city.isWeLoveTheKingDay() and not city.isCapital()):
													cityList.append(pCurrent.getPlotCity())
													#print (iDeadCiv, pCurrent.getPlotCity().getName(), pCurrent.getPlotCity().getOwner(), "2", cityList)
										elif (iOwnerStability < 0):
											if (not city.isWeLoveTheKingDay() and not city.isCapital() and (not (city.getX() == tCapitals[iOwner][0] and city.getY() == tCapitals[iOwner][1]))):
												if (gc.getPlayer(iOwner).getNumCities() > 0): #this check is needed, otherwise game crashes
													capital = gc.getPlayer(iOwner).getCapitalCity()
													iDistance = utils.calculateDistance(x, y, capital.getX(), capital.getY())
													if ((iDistance >= 6 and gc.getPlayer(iOwner).getNumCities() >= 4) or \
														city.angryPopulation(0) > 0 or \
														city.healthRate(False, 0) < 0 or \
														city.getReligionBadHappiness() > 0 or \
														city.getLargestCityHappiness() < 0 or \
														city.getHurryAngerModifier() > 0 or \
														city.getNoMilitaryPercentAnger() > 0 or \
														city.getWarWearinessPercentAnger() > 0):
															cityList.append(pCurrent.getPlotCity())
															#print (iDeadCiv, pCurrent.getPlotCity().getName(), pCurrent.getPlotCity().getOwner(), "3", cityList)
										if ( (not bSpecialRespawn) and (iOwnerStability < 10) ):
												if (city.getX() == tCapitals[iDeadCiv][0] and city.getY() == tCapitals[iDeadCiv][1]):
													if (pCurrent.getPlotCity() not in cityList):
														cityList.append(pCurrent.getPlotCity())
				if (len(cityList) >= iMinNumCities ):
					if bSpecialRespawn or (gc.getGame().getSorenRandNum(100, 'roll') < con.tResurrectionProb[iDeadCiv]): #If special, always happens
						lCityList = []
						for iCity in range( len(cityList)  ):
							lCityList.append( (cityList[iCity].getX(), cityList[iCity].getY()) )
						self.setRebelCities( lCityList )
						self.setRebelCiv(iDeadCiv) #for popup and CollapseCapitals()
						return iDeadCiv
		return -1


	def suppressResurection( self, iDeadCiv ):
		lSuppressList = self.getRebelSuppress()
		lCityList = self.getRebelCities()
		lCityCount = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1] #major players only

		for iCity in range( len( lCityList ) ):
			iOwner = gc.getMap().plot( lCityList[iCity][0], lCityList[iCity][1] ).getPlotCity().getOwner()
			if ( iOwner < iNumMajorPlayers ):
				lCityCount[iOwner] += 1

		iHuman = utils.getHumanID()
		for iCiv in range( iNumMajorPlayers ):
			if ( lCityCount[iCiv] > 0 ):
				if ( iCiv != iHuman ):
					if ( gc.getGame().getSorenRandNum(100, 'odds') > 50 ):
						lSuppressList[iCiv] = 1
						for iCity in range( len( lCityList ) ):
							pCity = gc.getMap().plot( lCityList[iCity][0], lCityList[iCity][1] ).getPlotCity()
							if ( pCity.getOwner() == iCiv ):
								pCity.changeOccupationTimer( 1 )
								pCity.changeHurryAngerTimer( 10 )
					else:
						lSuppressList[iCiv] = 0

		self.setRebelSuppress( lSuppressList )

		if ( lCityCount[iHuman] > 0 ):
			self.rebellionPopup( iDeadCiv, lCityCount[iHuman] )
		else:
			self.resurectCiv( iDeadCiv )


	def resurectCiv( self, iDeadCiv ):

		lCityList = self.getRebelCities()
		lSuppressList = self.getRebelSuppress()
		bSuppressed = True
		iHuman = utils.getHumanID()
		for iCiv in range( iNumMajorPlayers ):
			if ( iCiv != iHuman and lSuppressList[iCiv] == 0 ):
				bSuppressed = False

		if ( lSuppressList[iHuman] == 0 or lSuppressList[iHuman] == 2 or lSuppressList[iHuman] == 4 ):
			bSuppressed = False

		# 3Miro: if rebellion has been suppressed
		if ( bSuppressed == True ):
			return

		pDeadCiv = gc.getPlayer(iDeadCiv)
		teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())

		# 3Miro: set respawned
		pDeadCiv.setRespawned( True )

		if (len(tLeaders[iDeadCiv]) > 1):
			iLen = len(tLeaders[iDeadCiv])
			iRnd = gc.getGame().getSorenRandNum(iLen, 'odds')
			for k in range(iLen):
				iLeader = (iRnd + k) % iLen
				if (pDeadCiv.getLeader() != tLeaders[iDeadCiv][iLeader]):
					print ("leader switch after resurrection", pDeadCiv.getLeader(), tLeaders[iDeadCiv][iLeader])
					pDeadCiv.setLeader(tLeaders[iDeadCiv][iLeader])
					break

		for l in range(iNumPlayers):
			teamDeadCiv.makePeace(l)
		self.setNumCities(iDeadCiv, 0) #reset collapse condition

		#reset vassalage
		for iOtherCiv in range(iNumPlayers):
			if (teamDeadCiv.isVassal(iOtherCiv) or gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).isVassal(iDeadCiv)):
				teamDeadCiv.freeVassal(iOtherCiv)
				gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).freeVassal(iDeadCiv)

		iNewUnits = 2
		if (self.getLatestRebellionTurn(iDeadCiv) > 0):
			iNewUnits = 4
		self.setLatestRebellionTurn(iDeadCiv, gc.getGame().getGameTurn() )
		bHuman = False

		print ("RESURRECTION", gc.getPlayer(iDeadCiv).getCivilizationAdjective(0))

		for k0 in range(len(lCityList)):
			if ( gc.getMap().plot( lCityList[k0][0], lCityList[k0][1] ).getPlotCity().getOwner() == iHuman ):
				bHuman = True
			#iOwner = lCityList[k0][0].getOwner()
			#if ( iOwner == iHuman ):
			#	bHuman = True

		ownersList = []
		bAlreadyVassal = False
		for k in range(len(lCityList)):
			#print ("INDEPENDENCE: ", cityList[k].getName()) #may cause a c++ exception
			pCity = gc.getMap().plot( lCityList[k][0], lCityList[k][1] ).getPlotCity()
			iOwner = pCity.getOwner()
			teamOwner = gc.getTeam(gc.getPlayer(iOwner).getTeam())
			bOwnerVassal = teamOwner.isAVassal()
			bOwnerHumanVassal = teamOwner.isVassal(iHuman)

			#if (iOwner == iBarbarian or iOwner == iIndependent or iOwner == iIndependent2 ):
			if (iOwner == iBarbarian or utils.isIndep( iOwner )  ):
				utils.cultureManager((pCity.getX(),pCity.getY()), 100, iDeadCiv, iOwner, False, True, True)
				utils.flipUnitsInCityBefore((pCity.getX(),pCity.getY()), iDeadCiv, iOwner)
				self.setTempFlippingCity((pCity.getX(),pCity.getY()))
				utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iDeadCiv, [iOwner])
				tCoords = self.getTempFlippingCity()
				utils.flipUnitsInCityAfter(tCoords, iOwner)
				utils.flipUnitsInArea((tCoords[0]-2, tCoords[1]-2), (tCoords[0]+2, tCoords[1]+2), iDeadCiv, iOwner, True, False)
			else:
				if ( lSuppressList[iOwner] == 0 or lSuppressList[iOwner] == 2 or lSuppressList[iOwner] == 4 ):
					utils.cultureManager((pCity.getX(),pCity.getY()), 50, iDeadCiv, iOwner, False, True, True)
					utils.pushOutGarrisons((pCity.getX(),pCity.getY()), iOwner)
					utils.relocateSeaGarrisons((pCity.getX(),pCity.getY()), iOwner)
					self.setTempFlippingCity((pCity.getX(),pCity.getY()))
					utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iDeadCiv, [iOwner])   #by trade because by conquest may raze the city
					utils.createGarrisons(self.getTempFlippingCity(), iDeadCiv, iNewUnits)

			#cityList[k].setHasRealBuilding(con.iPlague, False)

				# 3Miro: indent to make part of the else on the if statement, otherwise one can make peace with the Barbs
				bAtWar = False #AI won't vassalise if another owner has declared war; on the other hand, it won't declare war if another one has vassalised
				if (iOwner != iHuman and iOwner not in ownersList and iOwner != iDeadCiv and lSuppressList[iOwner] == 0): #declare war or peace only once - the 3rd condition is obvious but "vassal of themselves" was happening
					rndNum = gc.getGame().getSorenRandNum(100, 'odds')
					if (rndNum >= tAIStopBirthThreshold[iOwner] and bOwnerHumanVassal == False and bAlreadyVassal == False): #if bOwnerHumanVassal is true, it will skip to the 3rd condition, as bOwnerVassal is true as well
						teamOwner.declareWar(iDeadCiv, False, -1)
						bAtWar = True
					elif (rndNum <= (100-tAIStopBirthThreshold[iOwner])/2):
						teamOwner.makePeace(iDeadCiv)
						if (bAlreadyVassal == False and bHuman == False and bOwnerVassal == False and bAtWar == False): #bHuman == False cos otherwise human player can be deceived to declare war without knowing the new master
							if (iOwner < iNumActivePlayers):
								gc.getTeam(gc.getPlayer(iDeadCiv).getTeam()).setVassal(iOwner, True, False)  #remove in vanilla
								bAlreadyVassal = True
					else:
						teamOwner.makePeace(iDeadCiv)
					ownersList.append(iOwner)
					for t in range(xml.iNumTechs):
						if (teamOwner.isHasTech(t)):
							teamDeadCiv.setHasTech(t, True, iDeadCiv, False, False)

		for t in range(xml.iNumTechs):
			if (teamBarbarian.isHasTech(t) or teamIndependent.isHasTech(t) or teamIndependent2.isHasTech(t) or teamIndependent3.isHasTech(t) or teamIndependent4.isHasTech(t)): #remove indep in vanilla
				teamDeadCiv.setHasTech(t, True, iDeadCiv, False, False)

		self.moveBackCapital(iDeadCiv)

		#add former colonies that are still free
		# 3Miro: no need, we don't have "colonies", this causes trouble with Cordoba's special respawn, getting cities back from Iberia
		colonyList = []
		#for iIndCiv in range(iNumTotalPlayers+1): #barbarians too
		#	if (iIndCiv >= iNumActivePlayers):
		#		if (gc.getPlayer(iIndCiv).isAlive()):
		#			apCityList = PyPlayer(iIndCiv).getCityList()
		#			for pCity in apCityList:
		#				indepCity = pCity.GetCy()
		#				if (indepCity.getOriginalOwner() == iDeadCiv):
		#					print ("colony:", indepCity.getName(), indepCity.getOriginalOwner())
		#					indX = indepCity.getX()
		#					indY = indepCity.getY()
		#					lCitySpot = ( indX, indY );
		#					if (gc.getPlayer(iDeadCiv).getSettlersMaps( con.iMapMaxY-indY-1, indX ) >= 90):
		#						if ((lCitySpot not in lCityList) and indepCity not in colonyList):
		#							colonyList.append(indepCity)
		#if (len(colonyList) > 0):
		#	for k in range(len(colonyList)):
		#		print ("INDEPENDENCE: ", colonyList[k].getName())
		#		iOwner = colonyList[k].getOwner()
		#		utils.cultureManager((colonyList[k].getX(),colonyList[k].getY()), 100, iDeadCiv, iOwner, False, True, True)
		#		utils.flipUnitsInCityBefore((colonyList[k].getX(),colonyList[k].getY()), iDeadCiv, iOwner)
		#		self.setTempFlippingCity((colonyList[k].getX(),colonyList[k].getY()))
		#		utils.flipCity((colonyList[k].getX(),colonyList[k].getY()), 0, 0, iDeadCiv, [iOwner])
		#		tCoords = self.getTempFlippingCity()
		#		utils.flipUnitsInCityAfter(tCoords, iOwner)
		#		utils.flipUnitsInArea((tCoords[0]-2, tCoords[1]-2), (tCoords[0]+2, tCoords[1]+2), iDeadCiv, iOwner, True, False)

		CyInterface().addMessage(iHuman, True, con.iDuration, \
					(CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pDeadCiv.getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
		#if (bHuman == True):
		#	self.rebellionPopup(iDeadCiv)
		if ( lSuppressList[iHuman] == 2 or lSuppressList[iHuman] == 3 or lSuppressList[iHuman] == 4 ):
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iDeadCiv, False, -1)
		else:
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iDeadCiv)
		#utils.setBaseStabilityLastTurn(iDeadCiv, 0)
		#utils.zeroStability(iDeadCiv)
		##tils.setParameter(iDeadCiv,con.iParExpansionE,False,10)
		#utils.setStability(iDeadCiv, 15) ##the new civs start as slightly stable
		pDeadCiv.changeStabilityBase( con.iCathegoryCities, -pDeadCiv.getStabilityBase( con.iCathegoryCities ) )
		pDeadCiv.changeStabilityBase( con.iCathegoryCivics, -pDeadCiv.getStabilityBase( con.iCathegoryCivics ) )
		pDeadCiv.changeStabilityBase( con.iCathegoryEconomy, -pDeadCiv.getStabilityBase( con.iCathegoryEconomy ) )
		pDeadCiv.changeStabilityBase( con.iCathegoryExpansion, 3-pDeadCiv.getStabilityBase( con.iCathegoryExpansion ) )
		utils.setPlagueCountdown(iDeadCiv, -10)
		utils.clearPlague(iDeadCiv)
		self.convertBackCulture(iDeadCiv)

		self.pm.onRespawn( iDeadCiv ) # 3Miro: for Cordoba's new provinces
		gc.getPlayer( iDeadCiv ).setRespawned( True )
		return


	def moveBackCapital(self, iCiv):
		apCityList = PyPlayer(iCiv).getCityList()
		if (len(tNewCapitals[iCiv])):
			for j in range(len(tNewCapitals[iCiv])):
				pCurrent = gc.getMap().plot( tNewCapitals[iCiv][j][0], tNewCapitals[iCiv][j][1] )
				if ( pCurrent.isCity()):
					newCapital = pCurrent.getPlotCity()
					if (newCapital.getOwner() == iCiv):
						if (not newCapital.hasBuilding(xml.iPalace)):
							for pCity in apCityList:
								pCity.GetCy().setHasRealBuilding((xml.iPalace), False)
							newCapital.setHasRealBuilding((xml.iPalace), True)
							self.makeResurectionUnits( iCiv, newCapital.getX(), newCapital.getY() )
		else:
			iMaxValue = 0
			bestCity = None
			for pCity in apCityList:
				loopCity = pCity.GetCy()
				#loopCity.AI_cityValue() doesn't work as area AI types aren't updated yet
				loopValue = max(0,500-loopCity.getGameTurnFounded()) + loopCity.getPopulation()*10
				#print ("loopValue", loopCity.getName(), loopCity.AI_cityValue(), loopValue) #causes C++ exception
				if (loopValue > iMaxValue):
					iMaxValue = loopValue
					bestCity = loopCity
			if (bestCity != None):
				for pCity in apCityList:
					loopCity = pCity.GetCy()
					if (loopCity != bestCity):
						loopCity.setHasRealBuilding((xml.iPalace), False)
				bestCity.setHasRealBuilding((xml.iPalace), True)
				self.makeResurectionUnits( iCiv, bestCity.getX(), bestCity.getY() )


	def makeResurectionUnits( self, iPlayer, iX, iY ):
		if ( iPlayer == iCordoba ):
			utils.makeUnit(xml.iSettler, iCordoba, [iX,iY], 2)
			utils.makeUnit(xml.iCrossbowman, iCordoba, [iX,iY], 2)
			utils.makeUnit(xml.iIslamicMissionary, iCordoba, [iX,iY], 1)


	def convertBackCulture(self, iCiv):
		#3Miro: same as Normal Ares in Resurection
		#Sedna17: restored to be normal areas, not core
		#tTopLeft = tCoreAreasTL[iCiv]
		#tBottomRight = tCoreAreasBR[iCiv]
		tTopLeft = tNormalAreasTL[iCiv]
		tBottomRight = tNormalAreasBR[iCiv]
		cityList = []
		#collect all the cities in the region
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				pCurrent = gc.getMap().plot( x, y )
				if ( pCurrent.isCity()):
					for ix in range(pCurrent.getX()-1, pCurrent.getX()+2):	# from x-1 to x+1
						for iy in range(pCurrent.getY()-1, pCurrent.getY()+2):	# from y-1 to y+1
							pCityArea = gc.getMap().plot( ix, iy )
							iCivCulture = pCityArea.getCulture(iCiv)
							iLoopCivCulture = 0
							for iLoopCiv in range(con.iNumTotalPlayers+1): #barbarians too
								if (iLoopCiv >= iNumPlayers):
									iLoopCivCulture += pCityArea.getCulture(iLoopCiv)
									pCityArea.setCulture(iLoopCiv, 0, True)
							pCityArea.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

					city = pCurrent.getPlotCity()
					iCivCulture = city.getCulture(iCiv)
					iLoopCivCulture = 0
					for iLoopCiv in range(con.iNumTotalPlayers+1): #barbarians too
						if (iLoopCiv >= iNumPlayers):
							iLoopCivCulture += city.getCulture(iLoopCiv)
							city.setCulture(iLoopCiv, 0, True)
					city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)


	def initBirth(self, iCurrentTurn, iBirthYear, iCiv):
		iHuman = utils.getHumanID()
		if (iCurrentTurn == iBirthYear-1 + self.getSpawnDelay(iCiv) + self.getFlipsDelay(iCiv)):
			tCapital = tCapitals[iCiv]
			tTopLeft = tCoreAreasTL[iCiv]
			tBottomRight = tCoreAreasBR[iCiv]
			tBroaderTopLeft = tBroaderAreasTL[iCiv]
			tBroaderBottomRight = tBroaderAreasBR[iCiv]
			if (self.getFlipsDelay(iCiv) == 0): #city hasn't already been founded)
				bDeleteEverything = False
				if (gc.getMap().plot(tCapital[0], tCapital[1]).isOwned()):
					if (iCiv == iHuman or not gc.getPlayer(iHuman).isAlive()):
						bDeleteEverything = True
						print ("bDeleteEverything 1")
					else:
						bDeleteEverything = True
						for x in range(tCapital[0] - 1, tCapital[0] + 2):	# from x-1 to x+1
							for y in range(tCapital[1] - 1, tCapital[1] + 2):	# from y-1 to y+1
								pCurrent=gc.getMap().plot(x, y)
								if (pCurrent.isCity() and pCurrent.getPlotCity().getOwner() == iHuman):
									bDeleteEverything = False
									print ("bDeleteEverything 2")
									break
									break
				print ("bDeleteEverything", bDeleteEverything)
				if (not gc.getMap().plot(tCapital[0], tCapital[1]).isOwned()):
					#if (iCiv == iNetherlands or iCiv == iPortugal): #dangerous starts
					#	self.setDeleteMode(0, iCiv)
					self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				elif (bDeleteEverything):
					for x in range(tCapital[0] - 1, tCapital[0] + 2):	# from x-1 to x+1
						for y in range(tCapital[1] - 1, tCapital[1] + 2):	# from y-1 to y+1
							self.setDeleteMode(0, iCiv)
							#print ("deleting", x, y)
							pCurrent=gc.getMap().plot(x, y)
							#self.moveOutUnits(x, y, tCapital[0], tCapital[1])
							for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
								if (iCiv != iLoopCiv):
									utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iLoopCiv, True, False)
							if (pCurrent.isCity()):
								pCurrent.eraseAIDevelopment() #new function, similar to erase but won't delete rivers, resources and features()
							for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
								if (iCiv != iLoopCiv):
									pCurrent.setCulture(iLoopCiv, 0, True)
							#pCurrent.setCulture(iCiv,10,True)
							pCurrent.setOwner(-1)
					self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				else:
					self.birthInForeignBorders(iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight)
			else:
				print ( "setBirthType again: flips" )
				self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)

		# 3MiroCrusader modification. Crusaders cannot change nations.
		# Sedna17: Straight-up no switching within 40 turns of your birth
		if (iCurrentTurn == iBirthYear + self.getSpawnDelay(iCiv)) and (gc.getPlayer(iCiv).isAlive()) and (self.getAlreadySwitched() == False) and (iCurrentTurn > tBirth[iHuman]+40) and ( not gc.getPlayer( iHuman ).getIsCrusader() ):
			self.newCivPopup(iCiv)


##	def moveOutUnits(self, x, y, tCapitalX, tCapitalY) #not used
##		pCurrent=gc.getMap().plot(x, y)
##		if (pCurrent.getNumUnits() > 0):
##			unit = pCurrent.getUnit(0)
##			tDestination = (-1, -1)
##			plotList = []
##			if (unit.getDomainType() == 2): #land unit
##				dummy, plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodPlots, [] )
##				#dummy, plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodOwnedPlots, [] )
##			else: #sea unit
##				dummy, plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodOwnedPlots, [] )
##
##			rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching another free plot')
##			if (len(plotList)):
##				result = plotList[rndNum]
##				if (result):
##					tDestination = result
##			print ("moving units around to", (tDestination[0], tDestination[1]))
##			if (tDestination != (-1, -1)):
##				for i in range(pCurrent.getNumUnits()):
##					unit = pCurrent.getUnit(0)
##					unit.setXY(tDestination[0], tDestination[1])


	def deleteMode(self, iCurrentPlayer):
		iCiv = self.getDeleteMode(0)
		print ("deleteMode after", iCurrentPlayer)
		tCapital = con.tCapitals[iCiv]
		if (iCurrentPlayer == iCiv):
			for x in range(tCapital[0] - 2, tCapital[0] + 3):	# from x-2 to x+2
				for y in range(tCapital[1] - 2, tCapital[1] + 3):	# from y-2 to y+2
					pCurrent=gc.getMap().plot(x, y)
					pCurrent.setCulture(iCiv, 300, True)
			for x in range(tCapital[0] - 1, tCapital[0] + 2):	# from x-1 to x+1
				for y in range(tCapital[1] - 1, tCapital[1] + 2):	# from y-1 to y+1
					pCurrent=gc.getMap().plot(x, y)
					utils.convertPlotCulture(pCurrent, iCiv, 100, True)
					if (pCurrent.getCulture(iCiv) < 3000):
						pCurrent.setCulture(iCiv, 3000, True) #2000 in vanilla/warlords, cos here Portugal is choked by spanish culture
					pCurrent.setOwner(iCiv)
			self.setDeleteMode(0, -1)
			return

		#print ("iCurrentPlayer", iCurrentPlayer, "iCiv", iCiv)
		if (iCurrentPlayer != iCiv-1):
			return

		bNotOwned = True
		for x in range(tCapital[0] - 1, tCapital[0] + 2):	# from x-1 to x+1
			for y in range(tCapital[1] - 1, tCapital[1] + 2):	# from y-1 to y+1
				#print ("deleting again", x, y)
				pCurrent=gc.getMap().plot(x, y)
				if (pCurrent.isOwned()):
					bNotOwned = False
					for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
						if(iLoopCiv != iCiv):
							pCurrent.setCulture(iLoopCiv, 0, True)
						#else:
						#	if (pCurrent.getCulture(iCiv) < 4000):
						#		pCurrent.setCulture(iCiv, 4000, True)
					#pCurrent.setOwner(-1)
					pCurrent.setOwner(iCiv)

		for x in range(tCapital[0] - 11, tCapital[0] + 12):	# must include the distance from Sogut to the Caspius
			for y in range(tCapital[1] - 11, tCapital[1] + 12):
				#print ("units", x, y, gc.getMap().plot(x, y).getNumUnits(), tCapital[0], tCapital[1])
				if (x != tCapital[0] or y != tCapital[1]):
					pCurrent=gc.getMap().plot(x, y)
					if (pCurrent.getNumUnits() > 0 and not pCurrent.isWater()):
						unit = pCurrent.getUnit(0)
						#print ("units2", x, y, gc.getMap().plot(x, y).getNumUnits(), unit.getOwner(), iCiv)
						if (unit.getOwner() == iCiv):
							print ("moving starting units from", x, y, "to", (tCapital[0], tCapital[1]))
							for i in range(pCurrent.getNumUnits()):
								unit = pCurrent.getUnit(0)
								unit.setXYOld(tCapital[0], tCapital[1])
							#may intersect plot close to tCapital
##							for farX in range(x - 6, x + 7):
##								for farY in range(y - 6, y + 7):
##									pCurrentFar = gc.getMap().plot(farX, farY)
##									if (pCurrentFar.getNumUnits() == 0):
##										pCurrentFar.setRevealed(iCiv, False, True, -1);


	def birthInFreeRegion(self, iCiv, tCapital, tTopLeft, tBottomRight):
		startingPlot = gc.getMap().plot( tCapital[0], tCapital[1] )
		if (self.getFlipsDelay(iCiv) == 0):
			iFlipsDelay = self.getFlipsDelay(iCiv) + 2
			print ("Entering birthInFreeRegion")
##			if (startingPlot.getNumUnits() > 0):
##				unit = startingPlot.getUnit(0)
##				if (unit.getOwner() != utils.getHumanID() or iCiv == utils.getHumanID()): #2nd check needed because in delete mode it finds the civ's (human's) units placed
##					for i in range(startingPlot.getNumUnits()):
##						unit = startingPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
##						unit.kill(False, iCiv)
##					iFlipsDelay = self.getFlipsDelay(iCiv) + 2
##					#utils.debugTextPopup( 'birthInFreeRegion in starting location' )
##				else:   #search another place
##					dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.goodPlots, [] )
##					rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching another free plot')
##					if (len(plotList)):
##						result = plotList[rndNum]
##						if (result):
##							self.createStartingUnits(iCiv, result)
##							tCapital = result
##							print ("birthInFreeRegion in another location")
##							#utils.debugTextPopup( 'birthInFreeRegion in another location' )
##							iFlipsDelay = self.getFlipsDelay(iCiv) + 1 #add delay before flipping other cities
##					else:
##						if (self.getSpawnDelay(iCiv) < 10):  #wait
##							iSpawnDelay = self.getSpawnDelay(iCiv) + 1
##							self.setSpawnDelay(iCiv, iSpawnDelay)
##			else:
##				iFlipsDelay = self.getFlipsDelay(iCiv) + 2

			if (iFlipsDelay > 0):
				#startingPlot.setImprovementType(-1)

				#gc.getPlayer(iCiv).found(tCapital[0], tCapital[1])
				#gc.getMap().plot(tCapital[0], tCapital[1]).setRevealed(iCiv, False, True, -1);
				#gc.getMap().plot(tCapital[0], tCapital[1]).setRevealed(iCiv, True, True, -1);

				print ("starting units in", tCapital[0], tCapital[1])
				self.createStartingUnits(iCiv, (tCapital[0], tCapital[1]))

				#if (self.getDeleteMode(0) == iCiv):
				#	self.createStartingWorkers(iCiv, tCapital) #XXX bugfix? no!

##				settlerPlot = gc.getMap().plot( tCapital[0], tCapital[1] )
##				for i in range(settlerPlot.getNumUnits()):
##					unit = settlerPlot.getUnit(i)
##					if (unit.getUnitType() == iSettler):
##						break
##				unit.found()
				utils.flipUnitsInArea((tCapital[0]-4, tCapital[1]-4), (tCapital[0]+4, tCapital[1]+4), iCiv, iBarbarian, True, True) #This is for AI only. During Human player spawn, that area is already cleaned
				for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
					utils.flipUnitsInArea((tCapital[0]-2, tCapital[1]-2), (tCapital[0]+2, tCapital[1]+2), iCiv, i, True, False) #This is for AI only. During Human player spawn, that area is already cleaned
				#utils.flipUnitsInArea((tCapital[0]-2, tCapital[1]-2), (tCapital[0]+2, tCapital[1]+2), iCiv, iIndependent, True, False) #This is for AI only. During Human player spawn, that area is already cleaned
				#utils.flipUnitsInArea((tCapital[0]-2, tCapital[1]-2), (tCapital[0]+2, tCapital[1]+2), iCiv, iIndependent2, True, False) #This is for AI only. During Human player spawn, that area is already cleaned
				self.assignTechs(iCiv)
				utils.setPlagueCountdown(iCiv, -con.iImmunity)
				utils.clearPlague(iCiv)
				#gc.getPlayer(iCiv).changeAnarchyTurns(1)
				#gc.getPlayer(iCiv).setCivics(2, 11)
				self.setFlipsDelay(iCiv, iFlipsDelay) #save


		else: #starting units have already been placed, now the second part
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, tTopLeft, tBottomRight)
			self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
				utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, i, False, False) #remaining independents in the region now belong to the new civ
			#utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, False, False) #remaining independents in the region now belong to the new civ
			#utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, False, False) #remaining independents in the region now belong to the new civ
			print ("utils.flipUnitsInArea()")
			#cover plots revealed by the lion
			plotZero = gc.getMap().plot( 32, 0 )
			if (plotZero.getNumUnits()):
				catapult = plotZero.getUnit(0)
				catapult.kill(False, iCiv)
			#gc.getMap().plot(0, 0).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(0, 1).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(1, 1).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(1, 0).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(123, 0).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(123, 1).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(2, 0).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(2, 1).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(2, 2).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(1, 2).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(0, 2).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(122, 0).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(122, 1).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(122, 2).setRevealed(iCiv, False, True, -1);
			#gc.getMap().plot(123, 2).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(31, 0).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(32, 0).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(33, 0).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(31, 1).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(32, 1).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(33, 1).setRevealed(iCiv, False, True, -1);
			print ("Plots covered")

			if (gc.getPlayer(iCiv).getNumCities() > 0):
				capital = gc.getPlayer(iCiv).getCapitalCity()
				self.createStartingWorkers(iCiv, (capital.getX(), capital.getY()))

			if (iNumHumanCitiesToConvert> 0):
				self.flipPopup(iCiv, tTopLeft, tBottomRight)


	def birthInForeignBorders(self, iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight):

		print( " 3Miro: Birth in Foreign Land: ",iCiv,tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight)
		iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, tTopLeft, tBottomRight)
		self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)

		#now starting units must be placed
		if (iNumAICitiesConverted > 0):
			#utils.debugTextPopup( 'iConverted OK for placing units' )
			dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iCiv )
			rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching any city just flipped')
			#print ("rndNum for starting units", rndNum)
			if (len(plotList)):
				result = plotList[rndNum]
				if (result):
					self.createStartingUnits(iCiv, result)
					#utils.debugTextPopup( 'birthInForeignBorders after a flip' )
					self.assignTechs(iCiv)
					utils.setPlagueCountdown(iCiv, -con.iImmunity)
					utils.clearPlague(iCiv)
					#gc.getPlayer(iCiv).changeAnarchyTurns(1)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
				utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, i, False, False) #remaining barbs in the region now belong to the new civ
			#utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, False, False) #remaining barbs in the region now belong to the new civ
			#utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, False, False) #remaining barbs in the region now belong to the new civ

		else:   #search another place
			dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.goodPlots, [] )
			rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching another free plot')
			if (len(plotList)):
				result = plotList[rndNum]
				if (result):
					self.createStartingUnits(iCiv, result)
					#utils.debugTextPopup( 'birthInForeignBorders in another location' )
					self.assignTechs(iCiv)
					utils.setPlagueCountdown(iCiv, -con.iImmunity)
					utils.clearPlague(iCiv)
			else:
				dummy1, plotList = utils.squareSearch( tBroaderTopLeft, tBroaderBottomRight, utils.goodPlots, [] )
				rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching other good plots in a broader region')
				if (len(plotList)):
					result = plotList[rndNum]
					if (result):
						self.createStartingUnits(iCiv, result)
						self.createStartingWorkers(iCiv, result)
						#utils.debugTextPopup( 'birthInForeignBorders in a broader area' )
						self.assignTechs(iCiv)
						utils.setPlagueCountdown(iCiv, -con.iImmunity)
						utils.clearPlague(iCiv)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ
			for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
				utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, i, True, False) #remaining barbs in the region now belong to the new civ
			#utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, True, False) #remaining barbs in the region now belong to the new civ
			#utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, True, False) #remaining barbs in the region now belong to the new civ

		if (iNumHumanCitiesToConvert> 0):
			self.flipPopup(iCiv, tTopLeft, tBottomRight)


	def convertSurroundingCities(self, iCiv, tTopLeft, tBottomRight):
		iConvertedCitiesCount = 0
		iNumHumanCities = 0
		cityList = []
		self.setSpawnWar(0)

		#collect all the cities in the spawn region
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				pCurrent = gc.getMap().plot( x, y )
				if ( pCurrent.isCity()):
					if (pCurrent.getPlotCity().getOwner() != iCiv):
						#print ("append", x,y)
						cityList.append(pCurrent.getPlotCity())

		#Exceptions
		if (len(tExceptions[iCiv])):
			for j in range(len(tExceptions[iCiv])):
				pCurrent = gc.getMap().plot( tExceptions[iCiv][j][0], tExceptions[iCiv][j][1] )
				if ( pCurrent.isCity()):
					if (pCurrent.getPlotCity().getOwner() != iCiv):
						#print ("append e1", pCurrent.getPlotCity().getX(),pCurrent.getPlotCity().getY())
						#print ("append e2", tExceptions[iCiv][j][0], tExceptions[iCiv][j][1])
						cityList.append(pCurrent.getPlotCity())

		print ("Birth", iCiv)
		#print (cityList)

		#for each city
		if (len(cityList)):
			for i in range(len(cityList)):
				loopCity = cityList[i]
				loopX = loopCity.getX()
				loopY = loopCity.getY()
				#print ("cityList", loopCity.getName(), (loopX, loopY))
				iHuman = utils.getHumanID()
				iOwner = loopCity.getOwner()
				iCultureChange = 0 #if 0, no flip; if > 0, flip will occur with the value as variable for utils.CultureManager()

				if (iOwner == iBarbarian or utils.isIndep( iOwner ) ):
					#utils.debugTextPopup( 'BARB' )
					iCultureChange = 100
				#case 2: human city
				elif (iOwner == iHuman and not loopCity.isCapital()):
					if (iNumHumanCities == 0):
						iNumHumanCities += 1
						#iConvertedCitiesCount += 1
						#self.flipPopup(iCiv, tTopLeft, tBottomRight)
				#case 3: other
				elif (not loopCity.isCapital()): # 3Miro: this keeps crashing in the C++, makes no sense
				#elif ( True ):   #utils.debugTextPopup( 'OTHER' )
					if (iConvertedCitiesCount < 6): #there won't be more than 5 flips in the area
						#utils.debugTextPopup( 'iConvertedCities OK' )
						iCultureChange = 50
						if (gc.getGame().getGameTurn() <= con.tBirth[iCiv] + 5): #if we're during a birth
							rndNum = gc.getGame().getSorenRandNum(100, 'odds')
							#3Miro: I don't know why the iOwner check is needed below, but the module crashes sometimes
							if ((iOwner>-1)and(iOwner<iNumMajorPlayers)and(rndNum >= tAIStopBirthThreshold[iOwner])):
								print (iOwner, "stops birth", iCiv, "rndNum:", rndNum, "threshold:", tAIStopBirthThreshold[iOwner])
								if (not gc.getTeam(gc.getPlayer(iOwner).getTeam()).isAtWar(iCiv)):
									gc.getTeam(gc.getPlayer(iOwner).getTeam()).declareWar(iCiv, False, -1)
									if (gc.getPlayer(iCiv).getNumCities() > 0): #this check is needed, otherwise game crashes
										print ("capital:", gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY())
										if (gc.getPlayer(iCiv).getCapitalCity().getX() != -1 and gc.getPlayer(iCiv).getCapitalCity().getY() != -1):
											self.createAdditionalUnits(iCiv, (gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY()))
										else:
											self.createAdditionalUnits(iCiv, tCapitals[iCiv])


				if (iCultureChange > 0):
					#print ("flipping ", cityList[i].getName())
					utils.cultureManager((loopX,loopY), iCultureChange, iCiv, iOwner, True, False, False)
					#gc.getMap().plot(cityList[i].getX(),cityList[i].getY()).setImprovementType(-1)

					utils.flipUnitsInCityBefore((loopX,loopY), iCiv, iOwner)
					self.setTempFlippingCity((loopX,loopY)) #necessary for the (688379128, 0) bug
					utils.flipCity((loopX,loopY), 0, 0, iCiv, [iOwner])
					#print ("cityList[i].getXY", cityList[i].getX(), cityList[i].getY())
					utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iCiv)

					iConvertedCitiesCount += 1
					print ("iConvertedCitiesCount", iConvertedCitiesCount)

		if (iConvertedCitiesCount > 0):
			if (gc.getPlayer(iCiv).isHuman()):
				CyInterface().addMessage(iCiv, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_TO_US", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)

		#print( "converted cities", iConvertedCitiesCount)
		return (iConvertedCitiesCount, iNumHumanCities)


	def convertSurroundingPlotCulture(self, iCiv, tTopLeft, tBottomRight):

		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				pCurrent = gc.getMap().plot( x, y )
				if (not pCurrent.isCity()):
					utils.convertPlotCulture(pCurrent, iCiv, 100, False)

		if (len(tExceptions[iCiv])):
			for j in range(len(tExceptions[iCiv])):
				pCurrent = gc.getMap().plot( tExceptions[iCiv][j][0], tExceptions[iCiv][j][1] )
				if (not pCurrent.isCity()):
					utils.convertPlotCulture(pCurrent, iCiv, 100, False)


	def findSeaPlots( self, tCoords, iRange):
		"""Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
		seaPlotList = []
		for x in range(tCoords[0] - iRange, tCoords[0] + iRange+1):
			for y in range(tCoords[1] - iRange, tCoords[1] + iRange+1):
				pCurrent = gc.getMap().plot( x, y )
				if ( pCurrent.isWater()):
					if ( not pCurrent.isUnit() ):
						if (pCurrent.countTotalCulture() == 0 ):
							seaPlotList.append(pCurrent)
							# this is a good plot, so paint it and continue search
		if (len(seaPlotList) > 0):
			rndNum = gc.getGame().getSorenRandNum(len(seaPlotList), 'sea plot')
			result = seaPlotList[rndNum]
			if (result):
				    return ((result.getX(), result.getY()))
		return (None)


	def giveColonists( self, iCiv, tBroaderAreaTL, tBroaderAreaBR):
	# 3Miro: Conquistador event
		pass


	def onFirstContact(self, iTeamX, iHasMetTeamY):
	# 3Miro: Conquistador event
		pass


	def getSpecialRespawn( self, iGameTurn ): #Absinthe: only the first civ for which it is true is returned, so the order of the civs is very important here
		if ( (not pFrankia.isAlive()) and (not pFrankia.getRespawned()) and iGameTurn > con.tBirth[iFrankia] + 25 and iGameTurn > utils.getLastTurnAlive(iFrankia) + 12 ):
			# France united in it's modern borders, start of the Bourbon royal line
			if ( iGameTurn > xml.i1588AD and iGameTurn < xml.i1700AD and iGameTurn % 5 == 3 ):
				return iFrankia
		if ( (not pArabia.isAlive()) and (not pArabia.getRespawned()) and iGameTurn > con.tBirth[iArabia] + 25 and iGameTurn > utils.getLastTurnAlive(iArabia) + 10 ):
			# Saladin, Ayyubid Dynasty
			if ( iGameTurn > xml.i1080AD and iGameTurn < xml.i1291AD and iGameTurn % 7 == 3 ):
				return iArabia
		if ( (not pBulgaria.isAlive()) and (not pBulgaria.getRespawned()) and iGameTurn > con.tBirth[iBulgaria] + 25 and iGameTurn > utils.getLastTurnAlive(iBulgaria) + 10 ):
			# second Bulgarian Empire
			if ( iGameTurn > xml.i1080AD and iGameTurn < xml.i1299AD and iGameTurn % 5 == 1 ):
				return iBulgaria
		if ( (not pCordoba.isAlive()) and (not pCordoba.getRespawned()) and iGameTurn > con.tBirth[iCordoba] + 25 and iGameTurn > utils.getLastTurnAlive(iCordoba) + 10 ):
			# special respawn as the Hafsid dynasty in North Africa
			if ( iGameTurn > xml.i1229AD and iGameTurn < xml.i1540AD and iGameTurn % 5 == 3 ):
				return iCordoba
		if ( (not pBurgundy.isAlive()) and (not pBurgundy.getRespawned()) and iGameTurn > con.tBirth[iBurgundy] + 25 and iGameTurn > utils.getLastTurnAlive(iBurgundy) + 20 ):
			# Burgundy in the 100 years war
			if ( iGameTurn > xml.i1336AD and iGameTurn < xml.i1453AD and iGameTurn % 8 == 1 ):
				return iBurgundy
		if ( (not pPrussia.isAlive()) and (not pPrussia.getRespawned()) and iGameTurn > con.tBirth[iPrussia] + 25 and iGameTurn > utils.getLastTurnAlive(iPrussia) + 10 ):
			# respawn as the unified Prussia
			if ( iGameTurn > xml.i1618AD and iGameTurn % 3 == 1 ):
				return iPrussia
		if ( (not pHungary.isAlive()) and (not pHungary.getRespawned()) and iGameTurn > con.tBirth[iHungary] + 25 and iGameTurn > utils.getLastTurnAlive(iHungary) + 10 ):
			# reconquest of Buda from the Ottomans
			if ( iGameTurn > xml.i1680AD and iGameTurn % 6 == 2 ):
				return iHungary
		if ( (not pSpain.isAlive()) and (not pSpain.getRespawned()) and iGameTurn > con.tBirth[iSpain] + 25 and iGameTurn > utils.getLastTurnAlive(iSpain) + 25 ):
			# respawn as the Castile/Aragon Union
			if ( iGameTurn > xml.i1470AD and iGameTurn < xml.i1580AD and iGameTurn % 5 == 0 ):
				return iSpain
		if ( (not pEngland.isAlive()) and (not pEngland.getRespawned()) and iGameTurn > con.tBirth[iEngland] + 25 and iGameTurn > utils.getLastTurnAlive(iEngland) + 12 ):
			# restoration of monarchy
			if ( iGameTurn > xml.i1660AD and iGameTurn % 6 == 2 ):
				return iEngland
		if ( (not pScotland.isAlive()) and (not pScotland.getRespawned()) and iGameTurn > con.tBirth[iScotland] + 25 and iGameTurn > utils.getLastTurnAlive(iScotland) + 30 ):
			if ( iGameTurn <= xml.i1600AD and iGameTurn % 6 == 3 ):
				return iScotland
		if ( (not pPortugal.isAlive()) and (not pPortugal.getRespawned()) and iGameTurn > con.tBirth[iPortugal] + 25 and iGameTurn > utils.getLastTurnAlive(iPortugal) + 10 ):
			# respawn to be around for colonies
			if ( iGameTurn > xml.i1431AD and iGameTurn < xml.i1580AD and iGameTurn % 5 == 3 ):
				return iPortugal
		if ( (not pAustria.isAlive()) and (not pAustria.getRespawned()) and iGameTurn > con.tBirth[iAustria] + 25 and iGameTurn > utils.getLastTurnAlive(iAustria) + 10 ):
			# increasing Habsburg influence in Hungary
			if ( iGameTurn > xml.i1526AD and iGameTurn < xml.i1690AD and iGameTurn % 8 == 3 ):
				return iAustria
		if ( (not pKiev.isAlive()) and (not pKiev.getRespawned()) and iGameTurn > con.tBirth[iKiev] + 25 and iGameTurn > utils.getLastTurnAlive(iKiev) + 10 ):
			# Cossack Hetmanate
			if ( iGameTurn >= xml.i1620AD and iGameTurn < xml.i1750AD and iGameTurn % 5 == 3 ):
				return iKiev
		if ( (not pMorocco.isAlive()) and (not pMorocco.getRespawned()) and iGameTurn > con.tBirth[iMorocco] + 25 and iGameTurn > utils.getLastTurnAlive(iMorocco) + 10 ):
			# Alaouite Dynasty
			if ( iGameTurn > xml.i1631AD and iGameTurn % 8 == 7 ):
				return iMorocco
		if ( (not pAragon.isAlive()) and (not pAragon.getRespawned()) and iGameTurn > con.tBirth[iAragon] + 25 and iGameTurn > utils.getLastTurnAlive(iAragon) + 10 ):
			# Kingdom of Sicily
			if ( iGameTurn > xml.i1700AD and iGameTurn % 8 == 7 ):
				return iAragon
		if ( (not pVenecia.isAlive()) and (not pVenecia.getRespawned()) and iGameTurn > con.tBirth[iVenecia] + 25 and iGameTurn > utils.getLastTurnAlive(iVenecia) + 10 ):
			if ( iGameTurn > xml.i1401AD and iGameTurn < xml.i1571AD and iGameTurn % 8 == 7 ):
				return iVenecia
		if ( (not pPoland.isAlive()) and (not pPoland.getRespawned()) and iGameTurn > con.tBirth[iPoland] + 25 and iGameTurn > utils.getLastTurnAlive(iPoland) + 10 ):
			if ( iGameTurn > xml.i1410AD and iGameTurn < xml.i1570AD and iGameTurn % 8 == 7 ):
				return iPoland
		if ( (not pTurkey.isAlive()) and (not pTurkey.getRespawned()) and iGameTurn > con.tBirth[iTurkey] + 25 and iGameTurn > utils.getLastTurnAlive(iTurkey) + 10 ):
			# Mehmed II's conquests
			if ( iGameTurn > xml.i1453AD and iGameTurn < xml.i1514AD and iGameTurn % 6 == 3 ):
				return iTurkey
		return -1


	def initMinorBetrayal( self, iCiv ):
		iHuman = utils.getHumanID()
		dummy, plotList = utils.squareSearch( tCoreAreasTL[iCiv], tCoreAreasBR[iCiv], utils.outerInvasion, [] )
		rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot abroad human players borders')
		if (len(plotList)):
			result = plotList[rndNum]
			if (result):
				self.createAdditionalUnits(iCiv, result)
				self.unitsBetrayal(iCiv, iHuman, tCoreAreasTL[iCiv], tCoreAreasBR[iCiv], result)


	def initBetrayal( self ):
		iHuman = utils.getHumanID()
		turnsLeft = self.getBetrayalTurns()
		dummy, plotList = utils.squareSearch( self.getTempTopLeft(), self.getTempBottomRight(), utils.outerInvasion, [] )
		rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot abroad human players (or in general, the old civ if human player just swtiched) borders')
		if (not len(plotList)):
			dummy, plotList = utils.squareSearch( self.getTempTopLeft(), self.getTempBottomRight(), utils.innerSpawn, [self.getOldCivFlip(), self.getNewCivFlip()] )
			rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot within human or new civs border but distant from units')
		if (not len(plotList)):
			dummy, plotList = utils.squareSearch( self.getTempTopLeft(), self.getTempBottomRight(), utils.innerInvasion, [self.getOldCivFlip(), self.getNewCivFlip()] )
			rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot within human or new civs border')
		if (len(plotList)):
			result = plotList[rndNum]
			if (result):
				if (turnsLeft == iBetrayalPeriod):
					self.createAdditionalUnits(self.getNewCivFlip(), result)
				self.unitsBetrayal(self.getNewCivFlip(), self.getOldCivFlip(), self.getTempTopLeft(), self.getTempBottomRight(), result)
		self.setBetrayalTurns(turnsLeft - 1)


	def unitsBetrayal( self, iNewOwner, iOldOwner, tTopLeft, tBottomRight, tPlot ):
		#print ("iNewOwner", iNewOwner, "iOldOwner", iOldOwner, "tPlot", tPlot)
		if (gc.getPlayer(self.getOldCivFlip()).isHuman()):
			CyInterface().addMessage(self.getOldCivFlip(), False, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
		elif (gc.getPlayer(self.getNewCivFlip()).isHuman()):
			CyInterface().addMessage(self.getNewCivFlip(), False, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL_NEW", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				killPlot = gc.getMap().plot(x,y)
				iNumUnitsInAPlot = killPlot.getNumUnits()
				if (iNumUnitsInAPlot):
					for i in range(iNumUnitsInAPlot):
						unit = killPlot.getUnit(i)
						if (unit.getOwner() == iOldOwner):
							rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
							if (rndNum >= iBetrayalThreshold):
								if (unit.getDomainType() == 2): #land unit
									iUnitType = unit.getUnitType()
									unit.kill(False, iNewOwner)
									utils.makeUnit(iUnitType, iNewOwner, tPlot, 1)
									i = i - 1


	def createAdditionalUnits( self, iCiv, tPlot ):
		if ( iCiv == iBurgundy ):
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
		if ( iCiv == iArabia ):
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
		if ( iCiv == iBulgaria ):
			utils.makeUnit(xml.iBulgarianKonnik, iCiv, tPlot, 2)
		if ( iCiv == iCordoba ):
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
		if ( iCiv == iSpain ):
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
		if ( iCiv == iNorway ):
			utils.makeUnit(xml.iVikingBeserker, iCiv, tPlot, 4)
		if ( iCiv == iDenmark ):
			utils.makeUnit(xml.iHuscarl, iCiv, tPlot, 3)
		if ( iCiv == iVenecia ):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
		if ( iCiv == iNovgorod ):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
		if ( iCiv == iKiev ):
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 3)
		if ( iCiv == iHungary ):
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
		if ( iCiv == iGermany ):
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
		if ( iCiv == iScotland ):
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 3)
		if ( iCiv == iPoland ):
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 3)
		if ( iCiv == iMoscow ):
			utils.makeUnit(xml.iMoscowBoyar, iCiv, tPlot, 2)
		if ( iCiv == iGenoa ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
		if ( iCiv == iMorocco ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		if ( iCiv == iEngland ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		if ( iCiv == iPortugal ):
			utils.makeUnit(xml.iPortugalFootKnight, iCiv, tPlot, 3)
		if ( iCiv == iAragon ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 4)
		if ( iCiv == iPrussia ):
			utils.makeUnit(xml.iTeutonic, iCiv, tPlot, 3)
		if ( iCiv == iLithuania ):
			utils.makeUnit(xml.iLithuanianBajoras, iCiv, tPlot, 2)
		if ( iCiv == iAustria ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		if ( iCiv == iTurkey ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		if ( iCiv == iSweden ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		if ( iCiv == iDutch ):
			utils.makeUnit(xml.iNetherlandsGrenadier, iCiv, tPlot, 2)


	def createStartingUnits( self, iCiv, tPlot ):
		# set the provinces
		self.pm.onSpawn( iCiv )
		# Change here to make later starting civs work
		if (iCiv == iBurgundy):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
		if (iCiv == iArabia):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 6)
		if (iCiv == iBulgaria):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iBulgarianKonnik, iCiv, tPlot, 5)
			utils.makeUnit(xml.iOrthodoxMissionary, iCiv, tPlot, 1)
		if (iCiv == iCordoba):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 3)
		if (iCiv == iSpain):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCatapult, iCiv, tPlot, 1)
		if (iCiv == iNorway):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iVikingBeserker, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				pNorway.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pNorway.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pNorway.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iArcher, iCiv, tSeaPlot, 1 )
		if (iCiv == iDenmark):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHuscarl, iCiv, tPlot, 4)
			tSeaPlot = self.findSeaPlots((61,56), 2)
			if ( tSeaPlot ):
				pDenmark.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pDenmark.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pDenmark.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1 )
		if (iCiv == iVenecia):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
				pVenecia.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pVenecia.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iArcher,iCiv,tSeaPlot,1)
				pVenecia.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
		if (iCiv == iNovgorod):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 1)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 1)
			utils.makeUnit(xml.iOrthodoxMissionary, iCiv, tPlot, 1)
		if (iCiv == iKiev):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 3)
		if (iCiv == iHungary):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
		if (iCiv == iGermany):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
		if (iCiv == iScotland):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
		if (iCiv == iPoland):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
		if (iCiv == iMoscow):
			utils.makeUnit(xml.iArbalest, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iMoscowBoyar, iCiv, tPlot, 5)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 4)
			utils.makeUnit(xml.iOrthodoxMissionary, iCiv, tPlot, 3)
		if (iCiv == iGenoa):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				pGenoa.initUnit(xml.iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pGenoa.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
		if (iCiv == iMorocco):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 1)
		if (iCiv == iEngland):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iLongSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 3)		# HHG: Calais-culture mostly prevents spawn of the galley. Range changed from 2 to 3.
			if ( tSeaPlot ):
				pEngland.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
		if (iCiv == iPortugal):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iPortugalFootKnight, iCiv, tPlot, 4)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
		if (iCiv == iAragon):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAlmogavar, iCiv, tPlot, 5)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			# Look for a sea plot by the coast (not by the starting point)
			tSeaPlot = self.findSeaPlots((38,29), 2)
			if ( tSeaPlot ):
				pAragon.initUnit(xml.iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pAragon.initUnit(xml.iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
		if (iCiv == iPrussia):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iTeutonic, iCiv, tPlot, 2)
			utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 1)
			utils.makeUnit(xml.iExecutive3, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 3)
		if (iCiv == iLithuania):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iLithuanianBajoras, iCiv, tPlot, 5)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
		if (iCiv == iAustria):
			utils.makeUnit(xml.iArbalest, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iKnight, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
		if (iCiv == iTurkey):
			utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iKnight, iCiv, tPlot, 3)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
			utils.makeUnit(xml.iTurkeyGreatBombard, iCiv, tPlot, 2)
			utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 4)
		if (iCiv == iSweden):
			utils.makeUnit(xml.iLongSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots((71,64), 2)
			if ( tSeaPlot ):
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
				pSweden.initUnit(xml.iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pSweden.initUnit(xml.iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pSweden.initUnit(xml.iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
		if (iCiv == iDutch):
			#print(" 3Miro: make Dutch Units in Plot ",tPlot )
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iMusketman, iCiv, tPlot, 6)
			utils.makeUnit(xml.iProtestantMissionary, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 2 )
				utils.makeUnit(xml.iGalleon, iCiv, tSeaPlot, 2 )

		self.showArea(iCiv)
		self.initContact(iCiv)


	def createStartingWorkers( self, iCiv, tPlot ):
		# 3Miro: get the workers
		# Sedna17: Cleaned the code
		print("Making starting workers")
		utils.makeUnit(xml.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
		# Absinthe: second Ottoman spawn stack may stay, altough they now spawn in Gallipoli in the first place (one plot SE)
		if ( iCiv == iTurkey ):
			self.ottomanInvasion(iCiv,(77,23))


	def create600ADstartingUnits( self ):
		# 3Miro: not needed
		pass


	def ottomanInvasion(self,iCiv,tPlot):
		print("I made Ottomans on Gallipoli")
		utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 2)
		utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
		utils.makeUnit(xml.iKnight, iCiv, tPlot, 3)
		utils.makeUnit(xml.iTurkeyGreatBombard, iCiv, tPlot, 2)
		utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 2)


	def create4000BCstartingUnits( self ):
		# 3Miro: units on start (note Spearman might be an up to date upgraded defender, tech dependent)

		utils.makeUnit(xml.iSettler, iFrankia, tCapitals[iFrankia], 3)
		utils.makeUnit(xml.iArcher, iFrankia, tCapitals[iFrankia], 3)
		utils.makeUnit(xml.iAxeman, iFrankia, tCapitals[iFrankia], 4)
		utils.makeUnit(xml.iWorker, iFrankia, tCapitals[iFrankia], 2)
		utils.makeUnit(xml.iCatholicMissionary, iFrankia, tCapitals[iFrankia], 1)

		#self.showArea(iBurgundy)
		self.showArea(iByzantium)
		self.initContact(iByzantium)
		self.showArea(iFrankia)
		self.showArea(iPope)

		if ( pBurgundy.isHuman() and tBirth[iBurgundy] > 0 ):
			# 3Miro: prohibit contact on turn 0 (with the Chronological spawn order this should not be needed)
			tBurgundyStart = ( tCapitals[iBurgundy][0]+2, tCapitals[iBurgundy][1] )
			utils.makeUnit(iSettler, iBurgundy, tCapitals[iBurgundy], 1)
			utils.makeUnit(xml.iArcher, iBurgundy, tCapitals[iBurgundy], 1)
			utils.makeUnit(xml.iWorker, iBurgundy, tCapitals[iBurgundy], 1)

		if ( pArabia.isHuman() and tBirth[iArabia] > 0 ):
			# 3Miro: prohibit contact on turn 0
			tArabStart = ( tCapitals[iArabia][0], tCapitals[iArabia][1]-10)
			utils.makeUnit(iSettler, iArabia, tArabStart, 1)
			utils.makeUnit(iSpearman, iArabia, tArabStart, 1)

		if ( pBulgaria.isHuman() and tBirth[iBulgaria] > 0 ):
			# 3Miro: prohibit contact on turn 0
			tBulgStart = ( tCapitals[iBulgaria][0], tCapitals[iBulgaria][1] + 1 )
			utils.makeUnit(iSettler, iBulgaria, tBulgStart, 1)
			utils.makeUnit(iSpearman, iBulgaria, tBulgStart, 1)

		if ( pCordoba.isHuman() and tBirth[iCordoba] > 0 ):
			utils.makeUnit(iSettler, iCordoba, tCapitals[iCordoba], 1)
			utils.makeUnit(iSpearman, iCordoba, tCapitals[iCordoba], 1)

		if ( pSpain.isHuman() and tBirth[iSpain] > 0 ):
			utils.makeUnit(iSettler, iSpain, tCapitals[iSpain], 1)
			utils.makeUnit(iSpearman, iSpain, tCapitals[iSpain], 1)

		if ( pNorway.isHuman() and tBirth[iNorway] > 0 ):
			utils.makeUnit(iSettler, iNorway, tCapitals[iNorway], 1)
			utils.makeUnit(iSpearman, iNorway, tCapitals[iNorway], 1)

		if ( pDenmark.isHuman() and tBirth[iDenmark] > 0 ):
			utils.makeUnit(iSettler, iDenmark, tCapitals[iDenmark], 1)
			utils.makeUnit(iSpearman, iDenmark, tCapitals[iDenmark], 1)

		if ( pVenecia.isHuman() and tBirth[iVenecia] > 0 ):
			utils.makeUnit(iSettler, iVenecia, tCapitals[iVenecia], 1)
			utils.makeUnit(iSpearman, iVenecia, tCapitals[iVenecia], 1)

		if ( pNovgorod.isHuman() and tBirth[iNovgorod] > 0 ):
			utils.makeUnit(iSettler, iNovgorod, tCapitals[iNovgorod], 1)
			utils.makeUnit(iSpearman, iNovgorod, tCapitals[iNovgorod], 1)

		if ( pKiev.isHuman() and tBirth[iKiev] > 0 ):
			utils.makeUnit(iSettler, iKiev, tCapitals[iKiev], 1)
			utils.makeUnit(iSpearman, iKiev, tCapitals[iKiev], 1)

		if ( pHungary.isHuman() and tBirth[iHungary] > 0 ):
			utils.makeUnit(iSettler, iHungary, tCapitals[iHungary], 1)
			utils.makeUnit(iSpearman, iHungary, tCapitals[iHungary], 1)

		if ( pGermany.isHuman() and tBirth[iGermany] > 0 ):
			utils.makeUnit(iSettler, iGermany, tCapitals[iGermany], 1)
			utils.makeUnit(iSpearman, iGermany, tCapitals[iGermany], 1)

		if ( pScotland.isHuman() and tBirth[iScotland] > 0 ):
			utils.makeUnit(iSettler, iScotland, tCapitals[iScotland], 1)
			utils.makeUnit(iSpearman, iScotland, tCapitals[iScotland], 1)

		if ( pPoland.isHuman() and tBirth[iPoland] > 0 ):
			utils.makeUnit(iSettler, iPoland, tCapitals[iPoland], 1)
			utils.makeUnit(iSpearman, iPoland, tCapitals[iPoland], 1)

		if ( pMoscow.isHuman() and tBirth[iMoscow] > 0 ):
			utils.makeUnit(iSettler, iMoscow, tCapitals[iMoscow], 1)
			utils.makeUnit(iSpearman, iMoscow, tCapitals[iMoscow], 1)

		if ( pGenoa.isHuman() and tBirth[iGenoa] > 0 ):
			utils.makeUnit(iSettler, iGenoa, tCapitals[iGenoa], 1)
			utils.makeUnit(iSpearman, iGenoa, tCapitals[iGenoa], 1)

		if ( pMorocco.isHuman() and tBirth[iMorocco] > 0 ):
			utils.makeUnit(iSettler, iMorocco, tCapitals[iMorocco], 1)
			utils.makeUnit(iSpearman, iMorocco, tCapitals[iMorocco], 1)

		if ( pEngland.isHuman() and tBirth[iEngland] > 0 ):
			utils.makeUnit(iSettler, iEngland, tCapitals[iEngland], 1)
			utils.makeUnit(xml.iSwordsman, iEngland, tCapitals[iEngland], 1)

		if ( pPortugal.isHuman() and tBirth[iPortugal] > 0 ):
			utils.makeUnit(iSettler, iPortugal, tCapitals[iPortugal], 1)
			utils.makeUnit(xml.iSwordsman, iPortugal, tCapitals[iPortugal], 1)

		if ( pAragon.isHuman() and tBirth[iAragon] > 0 ):
			utils.makeUnit(iSettler, iAragon, tCapitals[iAragon], 1)
			utils.makeUnit(xml.iSwordsman, iAragon, tCapitals[iAragon], 1)

		if ( pPrussia.isHuman() and tBirth[iPrussia] > 0 ):
			utils.makeUnit(iSettler, iPrussia, tCapitals[iPrussia], 1)
			utils.makeUnit(xml.iSwordsman, iPrussia, tCapitals[iPrussia], 1)

		if ( pLithuania.isHuman() and tBirth[iLithuania] > 0 ):
			utils.makeUnit(iSettler, iLithuania, tCapitals[iLithuania], 1)
			utils.makeUnit(xml.iSwordsman, iLithuania, tCapitals[iLithuania], 1)

		if ( pAustria.isHuman() and tBirth[iAustria] > 0 ):
			utils.makeUnit(iSettler, iAustria, tCapitals[iAustria], 1)
			utils.makeUnit(xml.iLongSwordsman, iAustria, tCapitals[iAustria], 1)

		if ( pTurkey.isHuman() and tBirth[iTurkey] > 0 ):
			tTurkishStart = ( tCapitals[iTurkey][0]+5, tCapitals[iTurkey][1]+30 )
			utils.makeUnit(iSettler, iTurkey, tTurkishStart, 1)
			utils.makeUnit(xml.iMaceman, iTurkey, tTurkishStart, 1)

		if ( pSweden.isHuman() and tBirth[iSweden] > 0 ):
			utils.makeUnit(iSettler, iSweden, tCapitals[iSweden], 1)
			utils.makeUnit(xml.iSwordsman, iSweden, tCapitals[iSweden], 1)

		if ( pDutch.isHuman() and tBirth[iDutch] > 0 ):
			utils.makeUnit(iSettler, iDutch, tCapitals[iDutch], 1)
			utils.makeUnit(xml.iMaceman, iDutch, tCapitals[iDutch], 1)


	def assign600ADTechs( self ):
		# 3Miro: not needed
		pass


	def assignTechs( self, iCiv ):
		# 3Miro: other than the original techs

		if ( tBirth[iCiv] == 0 ):
			return

		if ( iCiv == iBurgundy ):
			for iTech in range( xml.iStirrup + 1 ):
				teamBurgundy.setHasTech( iTech, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iArt, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iEngineering, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iAstrolabe, True, iCiv, False, False )

		if ( iCiv == iArabia ):
			teamArabia.setHasTech( xml.iTheology, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iCalendar, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iStirrup, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iBronzeCasting, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iArchitecture, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamArabia.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )

		if ( iCiv == iBulgaria ):
			teamBulgaria.setHasTech( xml.iTheology, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iCalendar, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iStirrup, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iArchitecture, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iBronzeCasting, True, iCiv, False, False )

		if ( iCiv == iCordoba ):
			teamCordoba.setHasTech( xml.iTheology, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iCalendar, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iStirrup, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iBronzeCasting, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iArchitecture, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iEngineering, True, iCiv, False, False )

		if ( iCiv == iSpain ):
			for iTech in range( xml.iStirrup + 1 ):
				teamSpain.setHasTech( iTech, True, iCiv, False, False )
			teamSpain.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamSpain.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamSpain.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamSpain.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamSpain.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamSpain.setHasTech( xml.iEngineering, True, iCiv, False, False )
			teamSpain.setHasTech( xml.iMachinery, True, iCiv, False, False )
			teamSpain.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamSpain.setHasTech( xml.iChainMail, True, iCiv, False, False )

		if ( iCiv == iScotland ):
			for iTech in range( xml.iStirrup + 1 ):
				teamScotland.setHasTech( iTech, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iMusic, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iEngineering, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iMachinery, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamScotland.setHasTech( xml.iAristocracy, True, iCiv, False, False )

		if ( iCiv == iNorway ):
			for iTech in range( xml.iStirrup + 1):
				teamNorway.setHasTech( iTech, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )

		if ( iCiv == iDenmark ):
			for iTech in range( xml.iStirrup + 1):
				teamDenmark.setHasTech( iTech, True, iCiv, False, False )
			teamDenmark.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamDenmark.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamDenmark.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamDenmark.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamDenmark.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamDenmark.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamDenmark.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamDenmark.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamDenmark.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )

		if ( iCiv == iVenecia ):
			for iTech in range( xml.iStirrup + 1 ):
				teamVenecia.setHasTech( iTech, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iMusic, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iChainMail, True, iCiv, False, False )

		if ( iCiv == iNovgorod ):
			for iTech in range( xml.iStirrup + 1 ):
				teamNovgorod.setHasTech( iTech, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iChainMail, True, iCiv, False, False )

		if ( iCiv == iKiev ):
			for iTech in range( xml.iStirrup + 1 ):
				teamKiev.setHasTech( iTech, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iChainMail, True, iCiv, False, False )

		if ( iCiv == iHungary ):
			for iTech in range( xml.iStirrup + 1 ):
				teamHungary.setHasTech( iTech, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iArt, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iVassalage, True, iCiv, False, False )

		if ( iCiv == iGermany ):
			for iTech in range( xml.iStirrup + 1 ):
				teamGermany.setHasTech( iTech, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iArt, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iEngineering, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iMachinery, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iAstrolabe, True, iCiv, False, False )

		if ( iCiv == iPoland ):
			for iTech in range( xml.iStirrup + 1 ):
				teamPoland.setHasTech( iTech, True, iCiv, False, False )
			teamPoland.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamPoland.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamPoland.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamPoland.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamPoland.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamPoland.setHasTech( xml.iArt, True, iCiv, False, False )
			teamPoland.setHasTech( xml.iEngineering, True, iCiv, False, False )
			teamPoland.setHasTech( xml.iChainMail, True, iCiv, False, False )

		if ( iCiv == iMoscow ):
			for iTech in range( xml.iFarriers + 1 ):
				teamMoscow.setHasTech( iTech, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iGothicArchitecture, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iChivalry, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iCivilService, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iMonumentBuilding, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iPlateArmor, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iSiegeEngines, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iMapMaking, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iClassicalKnowledge, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iClockmaking, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iAlchemy, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iGuilds, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iPhilosophy, True, iCiv, False, False )
			teamMoscow.setHasTech( xml.iReplaceableParts, True, iCiv, False, False )

		if ( iCiv == iGenoa ):
			for iTech in range( xml.iStirrup + 1 ):
				teamGenoa.setHasTech( iTech, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iMusic, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iEngineering, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iMachinery, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iVaultedArches, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamGenoa.setHasTech( xml.iAristocracy, True, iCiv, False, False )

		if ( iCiv == iEngland ):
			for iTech in range( xml.iFarriers + 1 ):
				teamEngland.setHasTech( iTech, True, iCiv, False, False )
			teamEngland.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamEngland.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamEngland.setHasTech( xml.iAristocracy, True, iCiv, False, False )

		if ( iCiv == iMorocco ):
			for iTech in range( xml.iFarriers + 1 ):
				teamMorocco.setHasTech( iTech, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iMapMaking, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )

		if ( iCiv == iPortugal ):
			for iTech in range( xml.iFarriers + 1 ):
				teamPortugal.setHasTech( iTech, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iMapMaking, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iAristocracy, True, iCiv, False, False )

		if ( iCiv == iAragon ):
			for iTech in range( xml.iFarriers + 1 ):
				teamAragon.setHasTech( iTech, True, iCiv, False, False )
			teamAragon.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamAragon.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamAragon.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamAragon.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamAragon.setHasTech( xml.iMapMaking, True, iCiv, False, False )
			teamAragon.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamAragon.setHasTech( xml.iPlateArmor, True, iCiv, False, False )
			teamAragon.setHasTech( xml.iGothicArchitecture, True, iCiv, False, False )
			teamAragon.setHasTech( xml.iSiegeEngines, True, iCiv, False, False )

		if ( iCiv == iSweden ):
			for iTech in range( xml.iFarriers + 1 ):
				teamSweden.setHasTech( iTech, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iGothicArchitecture, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iChivalry, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iPlateArmor, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iSiegeEngines, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iClassicalKnowledge, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iMonumentBuilding, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iPhilosophy, True, iCiv, False, False )
			teamSweden.setHasTech( xml.iMapMaking, True, iCiv, False, False )

		if ( iCiv == iPrussia ):
			for iTech in range( xml.iFarriers + 1 ):
				teamPrussia.setHasTech( iTech, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iGothicArchitecture, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iChivalry, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iPlateArmor, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iSiegeEngines, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iAlchemy, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iCivilService, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iGuilds, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iClassicalKnowledge, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iMonumentBuilding, True, iCiv, False, False )
			teamPrussia.setHasTech( xml.iPhilosophy, True, iCiv, False, False )

		if ( iCiv == iLithuania ):
			for iTech in range( xml.iFarriers + 1 ):
				teamLithuania.setHasTech( iTech, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iGothicArchitecture, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iCivilService, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iSiegeEngines, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iAlchemy, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iClassicalKnowledge, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iPlateArmor, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iMonumentBuilding, True, iCiv, False, False )
			teamLithuania.setHasTech( xml.iCivilService, True, iCiv, False, False )

		if ( iCiv == iAustria ):
			for iTech in range( xml.iFarriers + 1 ):
				teamAustria.setHasTech( iTech, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iGothicArchitecture, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iChivalry, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iPlateArmor, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iSiegeEngines, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iAlchemy, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iCivilService, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iGuilds, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iClassicalKnowledge, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iMonumentBuilding, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iPhilosophy, True, iCiv, False, False )
			teamAustria.setHasTech( xml.iEducation, True, iCiv, False, False )

		if ( iCiv == iTurkey ):
			for iTech in range( xml.iChivalry + 1 ):
				teamTurkey.setHasTech( iTech, True, iCiv, False, False )
			teamTurkey.setHasTech( xml.iGunpowder, True, iCiv, False, False )
			teamTurkey.setHasTech( xml.iMilitaryTradition, True, iCiv, False, False )
			teamTurkey.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )

		if ( iCiv == iDutch ):
			for iTech in range( xml.iAstronomy + 1 ):
				teamDutch.setHasTech( iTech, True, iCiv, False, False )

		self.hitNeighboursStability(iCiv)


	def hitNeighboursStability( self, iCiv ):
		# 3Miro: Stability on Spawn
		if (len(con.lOlderNeighbours[iCiv]) > 0):
		#	print "Got inside hitStability!!!"
			bHuman = False
			#for iLoop in con.lOlderNeighbours[iCiv]:
				#if (gc.getPlayer(iLoop).isAlive()):
				##	print("iLoop =",iLoop)
					#if (iLoop == utils.getHumanID()):
						#bHuman = True
					#utils.setStabilityParameters(iLoop, con.iParDiplomacyE, utils.getStabilityParameters(iLoop, con.iParDiplomacyE)-5)
					#utils.setStability(iLoop, utils.getStability(iLoop)-5)


	def showRect( self, iCiv, iXs, iYs, iXe, iYe ):
		for iX in range( iXs, iXe + 1 ):
			for iY in range( iYs, iYe + 1 ):
				gc.getMap().plot(iX, iY).setRevealed(gc.getPlayer(iCiv).getTeam(), True, False, -1)


	def showArea(self,iCiv):
		#print("  Visible for: ",iCiv )
		for iI in range( len( tVisible[iCiv] ) ):
			self.showRect( iCiv, tVisible[iCiv][iI][0], tVisible[iCiv][iI][1], tVisible[iCiv][iI][2], tVisible[iCiv][iI][3] )
		#print("  Visible for: ",iCiv )
		#pass


	def initContact(self, iCiv ):
		if ( iCiv == iByzantium ):
			if ( pPope.isAlive() and ( not teamByzantium.isHasMet( pPope.getTeam() ) ) ):
				teamByzantium.meet( pPope.getTeam(), True )
		elif ( iCiv == iBurgundy ):
			if ( pFrankia.isAlive() and ( not teamBurgundy.isHasMet( pFrankia.getTeam() ) ) ):
				teamBurgundy.meet( pFrankia.getTeam(), True )
		elif ( iCiv == iCordoba ):
			if ( pArabia.isAlive() and ( not teamCordoba.isHasMet( pArabia.getTeam() ) ) ):
				teamCordoba.meet( pArabia.getTeam(), True )
		elif ( iCiv == iSpain ):
			if ( pBurgundy.isAlive() and ( not teamSpain.isHasMet( pBurgundy.getTeam() ) ) ):
				teamSpain.meet( pBurgundy.getTeam(), True )
			if ( pFrankia.isAlive() and ( not teamSpain.isHasMet( pFrankia.getTeam() ) ) ):
				teamSpain.meet( pFrankia.getTeam(), True )
			if ( pCordoba.isAlive() and ( not teamSpain.isHasMet( pCordoba.getTeam() ) ) ):
				teamSpain.meet( pCordoba.getTeam(), True )
		elif ( iCiv == iVenecia ):
			if ( pPope.isAlive() and ( not teamByzantium.isHasMet( pPope.getTeam() ) ) ):
				teamByzantium.meet( pPope.getTeam(), True )
			if ( pByzantium.isAlive() and ( not teamVenecia.isHasMet( pByzantium.getTeam() ) ) ):
				teamVenecia.meet( pByzantium.getTeam(), True )
		elif ( iCiv == iNovgorod ):
			if ( pBulgaria.isAlive() and ( not teamNovgorod.isHasMet( pBulgaria.getTeam() ) ) ):
				teamNovgorod.meet( pBulgaria.getTeam(), True )
			if ( pByzantium.isAlive() and ( not teamNovgorod.isHasMet( pByzantium.getTeam() ) ) ):
				teamNovgorod.meet( pByzantium.getTeam(), True )
		elif ( iCiv == iKiev ):
			if ( pBulgaria.isAlive() and ( not teamKiev.isHasMet( pBulgaria.getTeam() ) ) ):
				teamKiev.meet( pBulgaria.getTeam(), True )
			if ( pByzantium.isAlive() and ( not teamKiev.isHasMet( pByzantium.getTeam() ) ) ):
				teamKiev.meet( pByzantium.getTeam(), True )
			if ( pNovgorod.isAlive() and ( not teamKiev.isHasMet( pNovgorod.getTeam() ) ) ):
				teamKiev.meet( pNovgorod.getTeam(), True )
		elif ( iCiv == iHungary ):
			if ( pBulgaria.isAlive() and ( not teamHungary.isHasMet( pBulgaria.getTeam() ) ) ):
				teamHungary.meet( pBulgaria.getTeam(), True )
			if ( pByzantium.isAlive() and ( not teamHungary.isHasMet( pByzantium.getTeam() ) ) ):
				teamHungary.meet( pByzantium.getTeam(), True )
		elif ( iCiv == iGermany ):
			if ( pBurgundy.isAlive() and ( not teamGermany.isHasMet( pBurgundy.getTeam() ) ) ):
				teamGermany.meet( pBurgundy.getTeam(), True )
			if ( pFrankia.isAlive() and ( not teamGermany.isHasMet( pFrankia.getTeam() ) ) ):
				teamGermany.meet( pFrankia.getTeam(), True )
			if ( pHungary.isAlive() and ( not teamGermany.isHasMet( pHungary.getTeam() ) ) ):
				teamGermany.meet( pHungary.getTeam(), True )
		elif ( iCiv == iScotland ):
			if ( pFrankia.isAlive() and ( not teamScotland.isHasMet( pFrankia.getTeam() ) ) ):
				teamScotland.meet( pFrankia.getTeam(), True )
			if ( pNorway.isAlive() and ( not teamScotland.isHasMet( pNorway.getTeam() ) ) ):
				teamScotland.meet( pNorway.getTeam(), True )
		elif ( iCiv == iPoland ):
			if ( pGermany.isAlive() and ( not teamPoland.isHasMet( pGermany.getTeam() ) ) ):
				teamPoland.meet( pGermany.getTeam(), True )
			if ( pHungary.isAlive() and ( not teamPoland.isHasMet( pHungary.getTeam() ) ) ):
				teamPoland.meet( pHungary.getTeam(), True )
		elif ( iCiv == iPrussia):
			if ( pPoland.isAlive() and ( not teamPrussia.isHasMet( pPoland.getTeam() ) ) ):
				teamPrussia.meet( pPoland.getTeam(), True )
			if ( pNovgorod.isAlive() and ( not teamPrussia.isHasMet( pNovgorod.getTeam() ) ) ):
				teamPrussia.meet( pNovgorod.getTeam(), True )
			if ( pGermany.isAlive() and ( not teamPrussia.isHasMet( pGermany.getTeam() ) ) ):
				teamPrussia.meet( pGermany.getTeam(), True )
		elif ( iCiv == iLithuania):
			if ( pPoland.isAlive() and ( not teamLithuania.isHasMet( pPoland.getTeam() ) ) ):
				teamLithuania.meet( pPoland.getTeam(), True )
			if ( pKiev.isAlive() and ( not teamLithuania.isHasMet( pKiev.getTeam() ) ) ):
				teamLithuania.meet( pKiev.getTeam(), True )
			if ( pPrussia.isAlive() and ( not teamLithuania.isHasMet( pPrussia.getTeam() ) ) ):
				teamLithuania.meet( pPrussia.getTeam(), True )
		elif ( iCiv == iMoscow ):
			if ( pKiev.isAlive() and ( not teamMoscow.isHasMet( pKiev.getTeam() ) ) ):
				teamMoscow.meet( pKiev.getTeam(), True )
			if ( pNovgorod.isAlive() and ( not teamMoscow.isHasMet( pNovgorod.getTeam() ) ) ):
				teamMoscow.meet( pNovgorod.getTeam(), True )
			if ( pSweden.isAlive() and ( not teamMoscow.isHasMet( pSweden.getTeam() ) ) ):
				teamMoscow.meet( pSweden.getTeam(), True )
			if ( pLithuania.isAlive() and ( not teamMoscow.isHasMet( pLithuania.getTeam() ) ) ):
				teamMoscow.meet( pLithuania.getTeam(), True )
		elif ( iCiv == iGenoa ):
			if ( pBurgundy.isAlive() and ( not teamGenoa.isHasMet( pBurgundy.getTeam() ) ) ):
				teamGenoa.meet( pBurgundy.getTeam(), True )
			if ( pByzantium.isAlive() and ( not teamGenoa.isHasMet( pByzantium.getTeam() ) ) ):
				teamGenoa.meet( pByzantium.getTeam(), True )
			if ( pVenecia.isAlive() and ( not teamGenoa.isHasMet( pVenecia.getTeam() ) ) ):
				teamGenoa.meet( pVenecia.getTeam(), True )
		elif ( iCiv == iMorocco ):
			if ( pArabia.isAlive() and ( not teamMorocco.isHasMet( pArabia.getTeam() ) ) ):
				teamMorocco.meet( pArabia.getTeam(), True )
			if ( pSpain.isAlive() and ( not teamMorocco.isHasMet( pSpain.getTeam() ) ) ):
				teamMorocco.meet( pSpain.getTeam(), True )
			if ( pCordoba.isAlive() and ( not teamMorocco.isHasMet( pCordoba.getTeam() ) ) ):
				teamMorocco.meet( pCordoba.getTeam(), True )
		elif ( iCiv == iSweden ):
			if ( pPoland.isAlive() and ( not teamSweden.isHasMet( pPoland.getTeam() ) ) ):
				teamSweden.meet( pPoland.getTeam(), True )
			if ( pGermany.isAlive() and ( not teamSweden.isHasMet( pGermany.getTeam() ) ) ):
				teamSweden.meet( pGermany.getTeam(), True )
			if ( pNovgorod.isAlive() and ( not teamSweden.isHasMet( pNovgorod.getTeam() ) ) ):
				teamSweden.meet( pNovgorod.getTeam(), True )
			if ( pDenmark.isAlive() and ( not teamDutch.isHasMet( pDenmark.getTeam() ) ) ):
				teamDutch.meet( pDenmark.getTeam(), True )
			if ( pNorway.isAlive() and ( not teamDutch.isHasMet( pNorway.getTeam() ) ) ):
				teamDutch.meet( pNorway.getTeam(), True )
		elif ( iCiv == iDutch ):
			if ( pEngland.isAlive() and ( not teamDutch.isHasMet( pEngland.getTeam() ) ) ):
				teamDutch.meet( pEngland.getTeam(), True )
			if ( pSpain.isAlive() and ( not teamDutch.isHasMet( pSpain.getTeam() ) ) ):
				teamDutch.meet( pSpain.getTeam(), True )
			if ( pFrankia.isAlive() and ( not teamDutch.isHasMet( pFrankia.getTeam() ) ) ):
				teamDutch.meet( pFrankia.getTeam(), True )
			if ( pGermany.isAlive() and ( not teamDutch.isHasMet( pGermany.getTeam() ) ) ):
				teamDutch.meet( pGermany.getTeam(), True )
			if ( pDenmark.isAlive() and ( not teamDutch.isHasMet( pDenmark.getTeam() ) ) ):
				teamDutch.meet( pDenmark.getTeam(), True )
			if ( pNorway.isAlive() and ( not teamDutch.isHasMet( pNorway.getTeam() ) ) ):
				teamDutch.meet( pNorway.getTeam(), True )
			if ( pSweden.isAlive() and ( not teamDutch.isHasMet( pSweden.getTeam() ) ) ):
				teamDutch.meet( pSweden.getTeam(), True )

