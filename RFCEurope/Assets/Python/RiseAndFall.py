# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
import Popup
import CvTranslator
import RFCUtils
import ProvinceManager # manage provinces here to link to spawn/rebirth
import Consts as con
import XMLConsts as xml
import Religions
import Victory
from StoredData import sd
import Crusades


################
### Globals ###
##############

gc = CyGlobalContext()	# LOQ
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()
rel = Religions.Religions()
vic = Victory.Victory()
cru = Crusades.Crusades()

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 66
iRebellionDelay = 15
iEscapePeriod = 30
tAIStopBirthThreshold = con.tAIStopBirthThreshold

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
iNumTotalPlayersB = con.iNumTotalPlayersB

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
		return sd.scriptDict['iNewCiv']

	def setNewCiv( self, iNewValue ):
		sd.scriptDict['iNewCiv'] = iNewValue

	def getNewCivFlip( self ):
		return sd.scriptDict['iNewCivFlip']

	def setNewCivFlip( self, iNewValue ):
		sd.scriptDict['iNewCivFlip'] = iNewValue

	def getOldCivFlip( self ):
		return sd.scriptDict['iOldCivFlip']

	def setOldCivFlip( self, iNewValue ):
		sd.scriptDict['iOldCivFlip'] = iNewValue

	def getTempTopLeft( self ):
		return sd.scriptDict['tempTopLeft']

	def setTempTopLeft( self, tNewValue ):
		sd.scriptDict['tempTopLeft'] = tNewValue

	def getTempBottomRight( self ):
		return sd.scriptDict['tempBottomRight']

	def setTempBottomRight( self, tNewValue ):
		sd.scriptDict['tempBottomRight'] = tNewValue

	def getSpawnWar( self ):
		return sd.scriptDict['iSpawnWar']

	def setSpawnWar( self, iNewValue ):
		sd.scriptDict['iSpawnWar'] = iNewValue

	def getAlreadySwitched( self ):
		return sd.scriptDict['bAlreadySwitched']

	def setAlreadySwitched( self, bNewValue ):
		sd.scriptDict['bAlreadySwitched'] = bNewValue

	def getColonistsAlreadyGiven( self, iCiv ):
		return sd.scriptDict['lColonistsAlreadyGiven'][iCiv]

	def setColonistsAlreadyGiven( self, iCiv, iNewValue ):
		sd.scriptDict['lColonistsAlreadyGiven'][iCiv] = iNewValue

	def getNumCities( self, iCiv ):
		return sd.scriptDict['lNumCities'][iCiv]

	def setNumCities( self, iCiv, iNewValue ):
		sd.scriptDict['lNumCities'][iCiv] = iNewValue

	def getSpawnDelay( self, iCiv ):
		return sd.scriptDict['lSpawnDelay'][iCiv]

	def setSpawnDelay( self, iCiv, iNewValue ):
		sd.scriptDict['lSpawnDelay'][iCiv] = iNewValue

	def getFlipsDelay( self, iCiv ):
		return sd.scriptDict['lFlipsDelay'][iCiv]

	def setFlipsDelay( self, iCiv, iNewValue ):
		sd.scriptDict['lFlipsDelay'][iCiv] = iNewValue

	def getBetrayalTurns( self ):
		return sd.scriptDict['iBetrayalTurns']

	def setBetrayalTurns( self, iNewValue ):
		sd.scriptDict['iBetrayalTurns'] = iNewValue

	def getLatestFlipTurn( self ):
		return sd.scriptDict['iLatestFlipTurn']

	def setLatestFlipTurn( self, iNewValue ):
		sd.scriptDict['iLatestFlipTurn'] = iNewValue

	def getLatestRebellionTurn( self, iCiv ):
		return sd.scriptDict['lLatestRebellionTurn'][iCiv]

	def setLatestRebellionTurn( self, iCiv, iNewValue ):
		sd.scriptDict['lLatestRebellionTurn'][iCiv] = iNewValue

	def getRebelCiv( self ):
		return sd.scriptDict['iRebelCiv']

	def setRebelCiv( self, iNewValue ):
		sd.scriptDict['iRebelCiv'] = iNewValue

	def getRebelCities( self ):
		return sd.scriptDict['lRebelCities']

	def setRebelCities( self, lCityList ):
		sd.scriptDict['lRebelCities'] = lCityList

	def getRebelSuppress( self ):
		return sd.scriptDict['lRebelSuppress']

	def setRebelSuppress( self, lSuppressList ):
		sd.scriptDict['lRebelSuppress'] = lSuppressList

	def getExileData( self, i ):
		return sd.scriptDict['lExileData'][i]

	def setExileData( self, i, iNewValue ):
		sd.scriptDict['lExileData'][i] = iNewValue

	def getTempFlippingCity( self ):
		return sd.scriptDict['tempFlippingCity']

	def setTempFlippingCity( self, tNewValue ):
		sd.scriptDict['tempFlippingCity'] = tNewValue

	def getCheatersCheck( self, i ):
		return sd.scriptDict['lCheatersCheck'][i]

	def setCheatersCheck( self, i, iNewValue ):
		sd.scriptDict['lCheatersCheck'][i] = iNewValue

	def getBirthTurnModifier( self, iCiv ):
		return sd.scriptDict['lBirthTurnModifier'][iCiv]

	def setBirthTurnModifier( self, iCiv, iNewValue ):
		sd.scriptDict['lBirthTurnModifier'][iCiv] = iNewValue

	def getDeleteMode( self, i ):
		return sd.scriptDict['lDeleteMode'][i]

	def setDeleteMode( self, i, iNewValue ):
		sd.scriptDict['lDeleteMode'][i] = iNewValue

	def getFirstContactConquerors( self, iCiv ):
		return sd.scriptDict['lFirstContactConquerors'][iCiv]

	def setFirstContactConquerors( self, iCiv, iNewValue ):
		sd.scriptDict['lFirstContactConquerors'][iCiv] = iNewValue

	#Sedna17 Respawn
	def setSpecialRespawnTurn( self, iCiv, iNewValue ):
		sd.scriptDict['lSpecialRespawnTurn'][iCiv] = iNewValue

	def getSpecialRespawnTurns( self):
		return sd.scriptDict['lSpecialRespawnTurn']


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
			iNewCiv = self.getNewCiv()
			vic.SwitchUHV(iNewCiv, utils.getHumanID())
			gc.getActivePlayer().setHandicapType(gc.getPlayer(iNewCiv).getHandicapType())
			gc.getGame().setActivePlayer(iNewCiv, False)
			gc.getPlayer(iNewCiv).setHandicapType(iOldHandicap)
			#for i in range(con.iNumStabilityParameters):
			#	utils.setStabilityParameters(utils.getHumanID(),i, 0)
			#	utils.setLastRecordedStabilityStuff(0, 0)
			#	utils.setLastRecordedStabilityStuff(1, 0)
			#	utils.setLastRecordedStabilityStuff(2, 0)
			#	utils.setLastRecordedStabilityStuff(3, 0)
			#	utils.setLastRecordedStabilityStuff(4, 0)
			#	utils.setLastRecordedStabilityStuff(5, 0)
			for iMaster in range(con.iNumPlayers):
				if (gc.getTeam(gc.getPlayer(iNewCiv).getTeam()).isVassal(iMaster)):
					gc.getTeam(gc.getPlayer(iNewCiv).getTeam()).setVassal(iMaster, False, False)
			self.setAlreadySwitched(True)
			gc.getPlayer(iNewCiv).setPlayable(True)
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
					# Absinthe: changeCulture instead of setCulture, otherwise previous culture will be lost
					pCurrent.changeCulture(iNewCivFlip, oldCulture/2, True)
					pCurrent.setCulture(iHuman, oldCulture/2, True)
					iWar = self.getSpawnWar() + 1
					self.setSpawnWar(iWar)
					if (self.getSpawnWar() == 1):
						#CyInterface().addImmediateMessage(CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "")
						gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).declareWar(iHuman, False, -1) ##True??
						self.setBetrayalTurns(iBetrayalPeriod)
						self.initBetrayal()


	# resurrection when some human controlled cities are also included
	def rebellionPopup(self, iRebelCiv, iNumCities ):
		iLoyalPrice = min( (10 * gc.getPlayer( utils.getHumanID() ).getGold()) / 100, 50 * iNumCities )
		self.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_HUMAN", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
				(CyTranslator().getText("TXT_KEY_REBELLION_LETGO", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_DONOTHING", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_CRACK", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_BRIBE", ()) + " " + str(iLoyalPrice), \
				CyTranslator().getText("TXT_KEY_REBELLION_BOTH", ())))


	# resurrection when some human controlled cities are also included
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

		self.setEarlyLeaders()

		#Sedna17 Respawn setup special respawn turns
		self.setupRespawnTurns()

		iHuman = utils.getHumanID()
		if utils.getScenario() == con.i500ADScenario:
			self.create500ADstartingUnits()
		else:
			self.create1200ADstartingUnits()
			for iCiv in range(iAragon+1):
				self.showArea(iCiv, con.i1200ADScenario)
				self.assign1200ADtechs(iCiv) # Temporarily all civs get the same starting techs as Aragon
				self.initContact(iCiv, False)
			rel.set1200Faith()
			self.setDiplo1200AD()
			self.LeaningTowerGP()
			rel.spread1200ADJews() # Spread Jews to some random cities
			vic.set1200UHVDone(iHuman)
			self.assign1200ADtechs(iPope) # Temporarily all civs get the same starting techs as Aragon
			cru.do1200ADCrusades()

		self.assignGold(utils.getScenario())

	def assignGold(self, iScenario):
		for iPlayer in range(con.iNumPlayers):
			gc.getPlayer(iPlayer).changeGold(con.tStartingGold[iScenario][iPlayer])

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
		if ( (pCity.getX()==56) and (pCity.getY()==35) ): #Venice - early defence boost, the rivers alone are not enough
			pCity.setHasRealBuilding( xml.iWalls, True )
		if ( (pCity.getX()==55) and (pCity.getY()==41) ): #Augsburg
			pCity.setHasRealBuilding( xml.iWalls, True )
		#if ( (pCity.getX()==41) and (pCity.getY()==52) ): #London			preplaced fort on the map instead of preplaced walls
		#	pCity.setHasRealBuilding( xml.iWalls, True )
		if ( (pCity.getX()==23) and (pCity.getY()==31) ): #Porto
			pCity.setHasRealBuilding( xml.iWalls, True )
		if ( (pCity.getX()==60) and (pCity.getY()==44) ): #Prague
			pCity.setHasRealBuilding( xml.iWalls, True )
		#if ( (pCity.getX()==80) and (pCity.getY()==62) ): #Novgorod		preplaced fort on the map instead of preplaced walls
		#	pCity.setHasRealBuilding( xml.iWalls, True )
		if ( (pCity.getX()==74) and (pCity.getY()==58) ): #Riga
			pCity.setHasRealBuilding( xml.iWalls, True )
		if (not gc.getPlayer(iLithuania).isHuman()):
			if ( (pCity.getX()==75) and (pCity.getY()==53) ): #Vilnius - important for AI Lithuania against Prussia
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
			self.setSpecialRespawnTurn(iCiv, con.tRespawnTime[iCiv]+(gc.getGame().getSorenRandNum(21, 'BirthTurnModifier') - 10)+(gc.getGame().getSorenRandNum(21, 'BirthTurnModifier2') - 10)) #bell-curve-like spawns within +/- 10 turns of desired turn (3Miro: Uniform, not a bell-curve)


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
			for j in range( iNumTotalPlayers ):
				if ( con.tWarAtSpawn[utils.getScenario()][i][j] > 0 ): # if there is a chance for war
					if ( gc.getGame().getSorenRandNum(100, 'war on spawn roll') < con.tWarAtSpawn[utils.getScenario()][i][j] ):
						# Absinthe: will use setAtWar here instead of declareWar, so it won't affect diplo relations and other stuff between major civs
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

		# Absinthe: checking the spawn dates
		for iLoopCiv in range( iNumMajorPlayers ):
			if ( (not (con.tBirth[iLoopCiv] == 0) ) and iGameTurn >= con.tBirth[iLoopCiv] - 2 and iGameTurn <= con.tBirth[iLoopCiv] + 4):
				self.initBirth(iGameTurn, con.tBirth[iLoopCiv], iLoopCiv)

		# Fragment minor civs:
		# 3Miro: Shuffle cities between Indies and Barbs to make sure there is no big Independent nation
		if (iGameTurn >= 20 and iGameTurn % 15 == 6):
			self.fragmentIndependents()
		if (iGameTurn >= 20 and iGameTurn % 30 == 12):
			self.fragmentBarbarians(iGameTurn)

		# Fall of civs:
		# Barb collapse: if more than 1/3 of the empire is conquered and/or held by barbs = collapse
		# Generic collapse: if 1/2 of the empire is lost in only a few turns (16 ATM) = collapse
		# Motherland collapse: if no city is in the core area and the number of cities in the normal area is less than the number of foreign cities = collapse
		# Secession: if stability is negative there is a chance (bigger chance with worse stability) for a random city to declare it's independence
		if (iGameTurn >= 64 and iGameTurn % 7 == 0): #mainly for Seljuks, Mongols, Timurids
			self.collapseByBarbs(iGameTurn)
		if (iGameTurn >= 34 and iGameTurn % 16 == 0):
			self.collapseGeneric(iGameTurn)
		if (iGameTurn >= 34 and iGameTurn % 9 == 7):
			self.collapseMotherland(iGameTurn)
		if (iGameTurn > 20 and iGameTurn % 3 == 1):
			self.secession(iGameTurn)

		# Resurrection of civs:
		# This is one place to control the frequency of resurrection; will not be called with high iNumDeadCivs
		# Generally we want to allow Kiev, Bulgaria, Cordoba, Burgundy, Byzantium at least to be dead in late game without respawning
		# Absinthe: was 12 and 8 originally in RFCE, but we don't need that many dead civs
		iNumDeadCivs1 = 8 #5 in vanilla RFC, 8 in warlords RFC
		iNumDeadCivs2 = 5 #3 in vanilla RFC, 6 in warlords RFC

		iCiv = self.getSpecialRespawn( iGameTurn )
		if ( iCiv > -1 ):
			self.resurrection(iGameTurn,iCiv)
		elif (gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs1):
			if (iGameTurn % 10 == 7):
				self.resurrection(iGameTurn, -1)
		elif (gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs2):
			if (iGameTurn % 23 == 11):
				self.resurrection(iGameTurn, -1)
		#lSpecialRespawnTurn = self.getSpecialRespawnTurns()
		#print("Special Respawn Turns ",lSpecialRespawnTurn)
		#if iGameTurn in lSpecialRespawnTurn:
		#	iCiv = lSpecialRespawnTurn.index(iGameTurn)#Lookup index for
		#	print("Special Respawn For Player: ",iCiv)
		#	if iCiv < iNumMajorPlayers and iCiv > 0:
		#		self.resurrection(iGameTurn,iCiv)

		# Absinthe: Reduce cities to towns, in order to make room for new civs
		if (iGameTurn == con.tBirth[con.iScotland] -3):
			# Reduce Inverness and Scone, so more freedom in where to found cities in Scotland
			self.reduceCity((37,65))
			self.reduceCity((37,67))
		elif (iGameTurn == con.tBirth[con.iEngland] -3):
			# Reduce Norwich and Nottingham, so more freedom in where to found cities in England
			self.reduceCity((43,55))
			self.reduceCity((39,56))
		elif (iGameTurn == con.tBirth[con.iSweden] -2):
			# Reduce Uppsala
			self.reduceCity((65,66))


	def reduceCity(self, tPlot):
		# Absinthe: disappearing cities (reducing them to an improvement)
		pPlot = gc.getMap().plot(tPlot[0],tPlot[1])
		if(pPlot.isCity()):
			# Absinthe: apologize from the player:
			msgString = CyTranslator().getText("TXT_KEY_REDUCE_CITY_1", ()) + " " + pPlot.getPlotCity().getName() + " " + CyTranslator().getText("TXT_KEY_REDUCE_CITY_2", ())
			CyInterface().addMessage(pPlot.getPlotCity().getOwner(), True, con.iDuration, msgString, "", 0, "", ColorTypes(con.iOrange), tPlot[0], tPlot[1], True, True)

			pPlot.eraseCityDevelopment()
			pPlot.setImprovementType(xml.iImprovementTown) # Improvement Town instead of the city
			pPlot.setRouteType(0) # Also adding a road there


	def checkPlayerTurn(self, iGameTurn, iPlayer):
		#switch leader on first anarchy if early leader is different from primary one, and in a late game anarchy period to a late leader
		#if (len(tLeaders[iPlayer]) > 1):
		#	if (tEarlyLeaders[iPlayer] != tLeaders[iPlayer][0]):
		#		if (iGameTurn > con.tBirth[iPlayer]+3 and iGameTurn < con.tBirth[iPlayer]+50):
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
			if (len(tLeaders[iPlayer]) > 2):
				if (len(tLeaders[iPlayer]) > 3):
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
		#			if in 1300AD Dublin is still Barbarian, it will flip to England
		if ( iGameTurn == xml.i1300AD and utils.getHumanID() != iEngland and iPlayer == iEngland and pEngland.isAlive() ):
			pPlot = gc.getMap().plot( 32, 58 )
			if ( pPlot.isCity() ):
				if ( pPlot.getPlotCity().getOwner() == con.iBarbarian ):
					pDublin = pPlot.getPlotCity()
					utils.cultureManager((pDublin.getX(),pDublin.getY()), 50, iEngland, iBarbarian, False, True, True)
					utils.flipUnitsInCityBefore((pDublin.getX(),pDublin.getY()), iEngland, iBarbarian)
					self.setTempFlippingCity((pDublin.getX(),pDublin.getY()))
					utils.flipCity((pDublin.getX(),pDublin.getY()), 0, 0, iEngland, [iBarbarian]) #by trade because by conquest may raze the city
					utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iEngland)

		# Absinthe: Another English AI cheat, extra defenders and defensive buildings in Normandy some turns after spawn - from RFCE++
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


	def switchLateLeaders(self, iPlayer, iLeaderIndex):
		if (tLateLeaders[iPlayer][iLeaderIndex] != gc.getPlayer(iPlayer).getLeader()):
			iThreshold = tLateLeaders[iPlayer][iLeaderIndex+2]
			if (gc.getPlayer(iPlayer).getCurrentEra() >= tLateLeaders[iPlayer][iLeaderIndex+3]):
				iThreshold *= 2
			if (gc.getPlayer(iPlayer).getAnarchyTurns() != 0 or utils.getPlagueCountdown(iPlayer) > 0 or utils.getStability(iPlayer) <= -10 or gc.getGame().getSorenRandNum(100, 'die roll') < iThreshold):
				gc.getPlayer(iPlayer).setLeader(tLateLeaders[iPlayer][iLeaderIndex])
				#print ("leader late switch:", tLateLeaders[iPlayer][iLeaderIndex], "in civ", iPlayer)

				# Absinthe: message about the leader switch for the human player
				iHuman = utils.getHumanID()
				HumanTeam = gc.getTeam(gc.getPlayer(iHuman).getTeam())
				PlayerTeam = gc.getPlayer(iPlayer).getTeam()
				if (HumanTeam.isHasMet(PlayerTeam)): # only if it's a known civ
					CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_LEADER_SWITCH", (gc.getPlayer(iPlayer).getName(), gc.getPlayer(iPlayer).getCivilizationDescriptionKey())), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, "", ColorTypes(con.iPurple), -1, -1, True, True)


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
								utils.flipCity((city.getX(),city.getY()), 0, 0, iSmall, [iBig]) #by trade because by conquest may raze the city
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
										utils.flipCity((city.getX(),city.getY()), 0, 0, iNewCiv, [iBarbarian]) #by trade because by conquest may raze the city
										utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
										iDivideCounter += 1
					return


	def collapseByBarbs(self, iGameTurn):
		# Absinthe: collapses if more than 1/3 of the empire is conquered and/or held by barbs
		for iCiv in range(iNumPlayers):
			pCiv = gc.getPlayer(iCiv)
			if (pCiv.isAlive()):
				# Absinthe: no barb collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
				iRespawnTurn = utils.getLastRespawnTurn( iCiv )
				if (iGameTurn >= con.tBirth[iCiv] + 20 and iGameTurn >= iRespawnTurn + 10 and not utils.collapseImmune(iCiv)):
					iNumCities = pCiv.getNumCities()
					iLostCities = gc.countCitiesLostTo( iCiv, iBarbarian )
					# Absinthe: if the civ is respawned, it's harder to collapse them by barbs
					if ( pCiv.getRespawnedAlive() == True ):
						iLostCities = max( iLostCities-(iNumCities/4), 0 )
					# Absinthe: if more than one third is captured, the civ collapses
					if (iLostCities*2 > iNumCities+1 and iNumCities > 0):
						print ("COLLAPSE BARBS", gc.getPlayer(iCiv).getCivilizationAdjective(0))
						if (pCiv.isHuman() == 0):
							utils.killAndFragmentCiv(iCiv, False, False)
						elif (pCiv.getNumCities() > 1):
							utils.killAndFragmentCiv(iCiv, False, True)

		# Absinthe: another instance of cities revolting, but only in case of very bad stability
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iPlayer = j % iNumPlayers
			pPlayer = gc.getPlayer(iPlayer)
			iRespawnTurn = utils.getLastRespawnTurn( iPlayer )
			if (pPlayer.isAlive() and iGameTurn >= con.tBirth[iPlayer] + 20 and iGameTurn >= iRespawnTurn + 10 ):
				iStability = pPlayer.getStability()
				if (pPlayer.getStability() < -15 and (not utils.collapseImmune(iPlayer)) and (pPlayer.getNumCities() > 10) ): #civil war
					self.revoltCity( iPlayer, False )
					self.revoltCity( iPlayer, False )
					self.revoltCity( iPlayer, True )
					self.revoltCity( iPlayer, True )


	def collapseGeneric(self, iGameTurn):
		# Absinthe: collapses if number of cities is less than half than some turns ago
		lNumCitiesLastTime = con.l0ArrayMajor
		for iCiv in range(iNumActivePlayers):
			pCiv = gc.getPlayer(iCiv)
			teamCiv = gc.getTeam(pCiv.getTeam())
			if (pCiv.isAlive()):
				lNumCitiesLastTime[iCiv] = self.getNumCities(iCiv)
				iNumCitiesCurrently = pCiv.getNumCities()
				self.setNumCities(iCiv, iNumCitiesCurrently)
				# Absinthe: no generic collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
				iRespawnTurn = utils.getLastRespawnTurn( iCiv )
				if (iGameTurn >= con.tBirth[iCiv] + 20 and iGameTurn >= iRespawnTurn + 10 and not utils.collapseImmune(iCiv)):
					# Absinthe: pass for small civs, we have bad stability collapses and collapseMotherland anyway, which is better suited for the collapse of those
					if (lNumCitiesLastTime[iCiv] > 2 and iNumCitiesCurrently * 2 <= lNumCitiesLastTime[iCiv]):
						print ("COLLAPSE GENERIC", pCiv.getCivilizationAdjective(0), iNumCitiesCurrently * 2, "<=", lNumCitiesLastTime[iCiv])
						if (pCiv.isHuman() == 0):
							utils.killAndFragmentCiv(iCiv, False, False)
						elif (pCiv.getNumCities() > 1):
							utils.killAndFragmentCiv(iCiv, False, True)


	def collapseMotherland(self, iGameTurn):
		# Absinthe: collapses if completely pushed out of the core area and also doesn't have enough presence in the normal area
		for iCiv in range(iNumPlayers):
			pCiv = gc.getPlayer(iCiv)
			teamCiv = gc.getTeam(pCiv.getTeam())
			if (pCiv.isAlive()):
				# Absinthe: no motherland collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
				iRespawnTurn = utils.getLastRespawnTurn( iCiv )
				if (iGameTurn >= con.tBirth[iCiv] + 20 and iGameTurn >= iRespawnTurn + 10 and not utils.collapseImmune(iCiv)):
					# Absinthe: respawned Cordoba or Aragon shouldn't collapse because not holding the original core area
					if (iCiv in [con.iCordoba, con.iAragon] and pCiv.getRespawnedAlive() == True):
						continue
					if ( not gc.safeMotherland( iCiv ) ):
						print ("COLLAPSE MOTHERLAND", gc.getPlayer(iCiv).getCivilizationAdjective(0))
						if (pCiv.isHuman() == 0):
							utils.killAndFragmentCiv(iCiv, False, False)
						elif (pCiv.getNumCities() > 1):
							utils.killAndFragmentCiv(iCiv, False, True)


	def secession(self, iGameTurn):
		# Absinthe: if stability is negative there is a chance for a random city to declare it's independence, checked every 3 turns
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iPlayer = j % iNumPlayers
			pPlayer = gc.getPlayer(iPlayer)
			# Absinthe: no city secession for 15 turns after spawn, for 10 turns after respawn
			iRespawnTurn = utils.getLastRespawnTurn( iPlayer )
			if (pPlayer.isAlive() and iGameTurn >= con.tBirth[iPlayer] + 15 and iGameTurn >= iRespawnTurn + 10):
				iStability = pPlayer.getStability()
				if ( gc.getGame().getSorenRandNum(10, 'do the check for city secession') < -iStability ): # x/10 chance with -x stability
					self.revoltCity( iPlayer, False )
					return # max 1 secession per turn


	def revoltCity( self, iPlayer, bForce ):
		pPlayer = gc.getPlayer(iPlayer)
		iStability = pPlayer.getStability()

		cityList = []
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			pCurrent = gc.getMap().plot(city.getX(), city.getY())

			# Absinthe: cities with We Love The King Day, your current and original capitals, and cities very close to your current capital won't revolt
			if ((not city.isWeLoveTheKingDay()) and (not city.isCapital()) and (not (city.getX() == tCapitals[iPlayer][0] and city.getY() == tCapitals[iPlayer][1]))):
				if (pPlayer.getNumCities() > 0): # this check is needed, otherwise game crashes
					capital = gc.getPlayer(iPlayer).getCapitalCity()
					iDistance = utils.calculateDistance(city.getX(), city.getY(), capital.getX(), capital.getY())
					if (iDistance > 3):
						iProvType = pPlayer.getProvinceType( city.getProvince() )
						# Absinthe: if forced revolt, all cities go into the list by default
						#			angry population, bad health, untolerated religion, no military garrison adds the city to the list once more (per type)
						#			if the city is in an border/contested province, the city is added 3 more times, if in foreign, 8 more times
						if (bForce):
							cityList.append(city)
						# Absinthe: Byzantine UP: cities in normal and core provinces won't go on the list
						if (city.angryPopulation(0) > 0):
							if (not utils.collapseImmuneCity(iPlayer,city.getX(),city.getY())):
								cityList.append(city)
							elif (iProvType < con.iProvincePotential):
								cityList.append(city)
								cityList.append(city)
						if (city.goodHealth() - city.badHealth(False) < -1):
							if (not utils.collapseImmuneCity(iPlayer,city.getX(),city.getY())):
								cityList.append(city)
							elif (iProvType < con.iProvincePotential):
								cityList.append(city)
								cityList.append(city)
						if (city.getReligionBadHappiness() < 0):
							if (not utils.collapseImmuneCity(iPlayer,city.getX(),city.getY())):
								cityList.append(city)
							elif (iProvType < con.iProvincePotential):
								cityList.append(city)
								cityList.append(city)
						if (city.getNoMilitaryPercentAnger() > 0):
							if (not utils.collapseImmuneCity(iPlayer,city.getX(),city.getY())):
								cityList.append(city)
							elif (iProvType < con.iProvincePotential):
								cityList.append(city)
								cityList.append(city)
						if ( iProvType == con.iProvinceOuter ):
							cityList.append(city)
						if ( iProvType == con.iProvinceNone ):
							cityList.append(city)
							cityList.append(city)
							cityList.append(city)
							cityList.append(city)
							cityList.append(city)
							cityList.append(city)
						continue

						# Absinthe: also add the city to the list if it has foreign culture - currently unused
						#for iLoop in range(iNumTotalPlayersB):
						#	if (iLoop != iPlayer):
						#		if (pCurrent.getCulture(iLoop) > 0):
						#			cityList.append(city)
						#			break

		if (len(cityList)):
			# Absinthe: city goes to random independent
			iRndNum = gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random independent')
			iNewCiv = con.iIndepStart + iRndNum

			# Absinthe: choosing one city from the list (where each city can appear multiple times)
			splittingCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')]
			sCityName = splittingCity.getName()
			if (iPlayer == utils.getHumanID()):
				CyInterface().addMessage(iPlayer, True, con.iDuration, sCityName + " " + CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
			utils.cultureManager((splittingCity.getX(),splittingCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
			utils.flipUnitsInCitySecession((splittingCity.getX(),splittingCity.getY()), iNewCiv, iPlayer)
			self.setTempFlippingCity((splittingCity.getX(),splittingCity.getY()))
			utils.flipCity((splittingCity.getX(),splittingCity.getY()), 0, 0, iNewCiv, [iPlayer]) #by trade because by conquest may raze the city
			utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)

			print ("SECESSION", gc.getPlayer(iPlayer).getCivilizationAdjective(0), sCityName, "Stability:", iStability)
			# Absinthe: loosing a city to secession/revolt gives a small boost to stability, to avoid a city-revolting chain reaction
			pPlayer.changeStabilityBase( con.iCathegoryExpansion, 2 )
			# Absinthe: AI declares war on the indy city right away
			teamPlayer = gc.getTeam( pPlayer.getTeam() )
			teamPlayer.declareWar(iNewCiv, False, WarPlanTypes.WARPLAN_LIMITED)


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
		#print("Looking up a civ to resurrect, iDeadCiv: ",iDeadCiv)
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
				#3Miro: in RFC Civs spawn according to Normal Areas, but here we want Core areas. Otherwise Normal Areas should not overlap and that is Hard.
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
														city.goodHealth() - city.badHealth(False) < -1 or \
														city.getReligionBadHappiness() < 0 or \
														city.getLargestCityHappiness() < 0 or \
														city.getHurryAngerModifier() > 0 or \
														city.getNoMilitaryPercentAnger() > 0):
															cityList.append(pCurrent.getPlotCity())
															#print (iDeadCiv, pCurrent.getPlotCity().getName(), pCurrent.getPlotCity().getOwner(), "3", cityList)
										if ( (not bSpecialRespawn) and (iOwnerStability < 10) ):
												if (city.getX() == tCapitals[iDeadCiv][0] and city.getY() == tCapitals[iDeadCiv][1]):
													if (pCurrent.getPlotCity() not in cityList):
														cityList.append(pCurrent.getPlotCity())
				if (len(cityList) >= iMinNumCities ):
					if bSpecialRespawn or (gc.getGame().getSorenRandNum(100, 'roll') < con.tResurrectionProb[iDeadCiv]): #If special, always happens
						lCityList = []
						for iCity in range( len(cityList) ):
							lCityList.append( (cityList[iCity].getX(), cityList[iCity].getY()) )
						self.setRebelCities( lCityList )
						self.setRebelCiv(iDeadCiv) #for popup and CollapseCapitals()
						return iDeadCiv
		return -1


	def suppressResurection( self, iDeadCiv ):
		lSuppressList = self.getRebelSuppress()
		#print ("lSuppressList for iCiv", lSuppressList)
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
					# Absinthe: for the AI there is 30% chance that the actual respawn does not happen (under these suppress situations), only some revolt in the corresponding cities
					iActualSpawnChance = gc.getGame().getSorenRandNum(100, 'odds')
					print ("iActualSpawnChance", iActualSpawnChance)
					if ( iActualSpawnChance > 70 ):
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
		# Absinthe: what's the point of bSuppressed and the various player options in the popup if we always set it to false here?
		for iCiv in range( iNumMajorPlayers ):
			if ( iCiv != iHuman and lSuppressList[iCiv] == 0 ):
				bSuppressed = False

		if ( lSuppressList[iHuman] == 0 or lSuppressList[iHuman] == 2 or lSuppressList[iHuman] == 4 ):
			bSuppressed = False

		print ("bSuppressed", bSuppressed)
		# 3Miro: if rebellion has been suppressed
		if ( bSuppressed == True ):
			return

		pDeadCiv = gc.getPlayer(iDeadCiv)
		teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())

		# Absinthe: respawn status
		pDeadCiv.setRespawnedAlive( True )
		pDeadCiv.setEverRespawned( True ) # needed for first turn vassalization and peace status fixes

		# Absinthe: store the turn of the latest respawn for each civ
		iGameTurn = gc.getGame().getGameTurn()
		utils.setLastRespawnTurn( iDeadCiv, iGameTurn )
		print ("Last respawn for civ:", iDeadCiv, "in turn:", iGameTurn)

		# Absinthe: update province status before the cities are flipped, so potential provinces will update if there are cities in them
		self.pm.onRespawn( iDeadCiv ) # Absinthe: resetting the original potential provinces, and adding special province changes on respawn (Cordoba)

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
			if (l != iDeadCiv):
				teamDeadCiv.makePeace(l)
		self.setNumCities(iDeadCiv, 0) #reset collapse condition

		# Absinthe: reset vassalage and update dynamic civ names
		for iOtherCiv in range(iNumPlayers):
			if (iOtherCiv != iDeadCiv):
				if (teamDeadCiv.isVassal(iOtherCiv) or gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).isVassal(iDeadCiv)):
					teamDeadCiv.freeVassal(iOtherCiv)
					gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).freeVassal(iDeadCiv)
					gc.getPlayer(iOtherCiv).processCivNames()
					gc.getPlayer(iDeadCiv).processCivNames()

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

			if (iOwner == iBarbarian or utils.isIndep( iOwner ) ):
				utils.cultureManager((pCity.getX(),pCity.getY()), 100, iDeadCiv, iOwner, False, True, True)
				utils.flipUnitsInCityBefore((pCity.getX(),pCity.getY()), iDeadCiv, iOwner)
				self.setTempFlippingCity((pCity.getX(),pCity.getY()))
				utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iDeadCiv, [iOwner])
				tCoords = self.getTempFlippingCity()
				utils.flipUnitsInCityAfter(tCoords, iOwner)
				utils.flipUnitsInArea((tCoords[0]-2, tCoords[1]-2), (tCoords[0]+2, tCoords[1]+2), iDeadCiv, iOwner, True, False)
			else:
				print ("iOwner lSuppressList iDeadCiv", iOwner, lSuppressList[iOwner], iDeadCiv)
				if ( lSuppressList[iOwner] == 0 or lSuppressList[iOwner] == 2 or lSuppressList[iOwner] == 4 ):
					utils.cultureManager((pCity.getX(),pCity.getY()), 50, iDeadCiv, iOwner, False, True, True)
					utils.pushOutGarrisons((pCity.getX(),pCity.getY()), iOwner)
					utils.relocateSeaGarrisons((pCity.getX(),pCity.getY()), iOwner)
					self.setTempFlippingCity((pCity.getX(),pCity.getY()))
					utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iDeadCiv, [iOwner]) #by trade because by conquest may raze the city
					utils.createGarrisons(self.getTempFlippingCity(), iDeadCiv, iNewUnits)

			#cityList[k].setHasRealBuilding(con.iPlague, False)

				# 3Miro: indent to make part of the else on the if statement, otherwise one can make peace with the Barbs
				bAtWar = False #AI won't vassalise if another owner has declared war; on the other hand, it won't declare war if another one has vassalised
				if (iOwner != iHuman and iOwner not in ownersList and iOwner != iDeadCiv and lSuppressList[iOwner] == 0): #declare war or peace only once - the 3rd condition is obvious but "vassal of themselves" was happening
					rndNum = gc.getGame().getSorenRandNum(100, 'odds')
					if (rndNum >= tAIStopBirthThreshold[iOwner] and bOwnerHumanVassal == False and bAlreadyVassal == False): #if bOwnerHumanVassal is true, it will skip to the 3rd condition, as bOwnerVassal is true as well
						teamOwner.declareWar(iDeadCiv, False, -1)
						bAtWar = True
					# Absinthe: de we really want to auto-vassal them on respawn?
					elif (rndNum <= 60 - (tAIStopBirthThreshold[iOwner]/2)):
						teamOwner.makePeace(iDeadCiv)
						if (bAlreadyVassal == False and bHuman == False and bOwnerVassal == False and bAtWar == False): #bHuman == False cos otherwise human player can be deceived to declare war without knowing the new master
							if (iOwner < iNumActivePlayers):
								gc.getTeam(gc.getPlayer(iDeadCiv).getTeam()).setVassal(iOwner, True, False)
								gc.getPlayer(iOwner).processCivNames() # setVassal already updates DCN for iDeadCiv
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
		#for iIndCiv in range(iNumTotalPlayersB): #barbarians too
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

		CyInterface().addMessage(iHuman, True, con.iDuration, (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pDeadCiv.getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(con.iDarkPink), -1, -1, True, True)
		#if (bHuman == True):
		#	self.rebellionPopup(iDeadCiv)
		if ( lSuppressList[iHuman] == 2 or lSuppressList[iHuman] == 3 or lSuppressList[iHuman] == 4 ):
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iDeadCiv, False, -1)
		else:
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iDeadCiv)

		# Absinthe: the new civs start as slightly stable
		pDeadCiv.changeStabilityBase( con.iCathegoryCities, -pDeadCiv.getStabilityBase( con.iCathegoryCities ) )
		pDeadCiv.changeStabilityBase( con.iCathegoryCivics, -pDeadCiv.getStabilityBase( con.iCathegoryCivics ) )
		pDeadCiv.changeStabilityBase( con.iCathegoryEconomy, -pDeadCiv.getStabilityBase( con.iCathegoryEconomy ) )
		pDeadCiv.changeStabilityBase( con.iCathegoryExpansion, -pDeadCiv.getStabilityBase( con.iCathegoryExpansion ) )
		pDeadCiv.changeStabilityBase( con.iCathegoryExpansion, 3 )

		# Absinthe: refresh dynamic civ name for the new civ
		gc.getPlayer(iDeadCiv).processCivNames()

		utils.setPlagueCountdown(iDeadCiv, -10)
		utils.clearPlague(iDeadCiv)
		self.convertBackCulture(iDeadCiv)
		#gc.getPlayer( iDeadCiv ).setRespawnedAlive( True )
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
		#3Miro: same as Normal Areas in Resurrection
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
							for iLoopCiv in range(iNumTotalPlayersB): #barbarians too
								if (iLoopCiv >= iNumPlayers):
									iLoopCivCulture += pCityArea.getCulture(iLoopCiv)
									pCityArea.setCulture(iLoopCiv, 0, True)
							pCityArea.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

					city = pCurrent.getPlotCity()
					iCivCulture = city.getCulture(iCiv)
					iLoopCivCulture = 0
					for iLoopCiv in range(iNumTotalPlayersB): #barbarians too
						if (iLoopCiv >= iNumPlayers):
							iLoopCivCulture += city.getCulture(iLoopCiv)
							city.setCulture(iLoopCiv, 0, True)
					city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)


	def initBirth(self, iCurrentTurn, iBirthYear, iCiv):
		iHuman = utils.getHumanID()
		#print("iBirthYear:%d, iCurrentTurn:%d" %(iBirthYear, iCurrentTurn))
		#print("getSpawnDelay:%d, getFlipsDelay:%d" %(self.getSpawnDelay(iCiv), self.getFlipsDelay(iCiv)))
		if (iCurrentTurn == iBirthYear-1 + self.getSpawnDelay(iCiv) + self.getFlipsDelay(iCiv)):
			tCapital = tCapitals[iCiv]
			tTopLeft = tCoreAreasTL[iCiv]
			tBottomRight = tCoreAreasBR[iCiv]
			tBroaderTopLeft = tBroaderAreasTL[iCiv]
			tBroaderBottomRight = tBroaderAreasBR[iCiv]
			if (self.getFlipsDelay(iCiv) == 0): #city hasn't already been founded)

			# Absinthe: this probably fixes a couple instances of the -1 turn autoplay bug - code adapted from SoI
				if (iCiv == iHuman): 
					killPlot = gc.getMap().plot(tCapital[0], tCapital[1])
					iNumUnitsInAPlot = killPlot.getNumUnits()
					if (iNumUnitsInAPlot):
						for i in range(iNumUnitsInAPlot):
							unit = killPlot.getUnit(i)
							if (unit.getOwner() != iCiv):
								unit.kill(False, iBarbarian)

				bDeleteEverything = False
				if (gc.getMap().plot(tCapital[0], tCapital[1]).isOwned()):
					if (iCiv == iHuman or not gc.getPlayer(iHuman).isAlive()):
						bDeleteEverything = True
						print ("bDeleteEverything 1")
					else:
						bDeleteEverything = True
						for x in range(tCapital[0] - 1, tCapital[0] + 2):	# from x-1 to x+1, range in python works this way
							for y in range(tCapital[1] - 1, tCapital[1] + 2):	# from y-1 to y+1, range in python works this way
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
							for iLoopCiv in range(iNumTotalPlayersB): #Barbarians as well
								if (iCiv != iLoopCiv):
									utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iLoopCiv, True, False)
							if (pCurrent.isCity()):
								pCurrent.eraseAIDevelopment() #new function, similar to erase but won't delete rivers, resources and features
							for iLoopCiv in range(iNumTotalPlayersB): #Barbarians as well
								if (iCiv != iLoopCiv):
									pCurrent.setCulture(iLoopCiv, 0, True)
							#pCurrent.setCulture(iCiv,10,True)
							pCurrent.setOwner(-1)
					self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				else:
					self.birthInForeignBorders(iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight, tCapital)
			else:
				print ( "setBirthType again: flips" )
				self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)

		# 3MiroCrusader modification. Crusaders cannot change nations.
		# Sedna17: Straight-up no switching within 40 turns of your birth
		if (iCurrentTurn == iBirthYear + self.getSpawnDelay(iCiv)):
			if (gc.getPlayer(iCiv).isAlive()) and (self.getAlreadySwitched() == False) and (iCurrentTurn > con.tBirth[iHuman] + 40) and ( not gc.getPlayer( iHuman ).getIsCrusader() ):
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
						pCurrent.setCulture(iCiv, 3000, True) #2000 in vanilla/warlords, cos here Portugal is choked by Spanish culture
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
					for iLoopCiv in range(iNumTotalPlayersB): #Barbarians as well
						if(iLoopCiv != iCiv):
							pCurrent.setCulture(iLoopCiv, 0, True)
						#else:
						#	if (pCurrent.getCulture(iCiv) < 4000):
						#		pCurrent.setCulture(iCiv, 4000, True)
					#pCurrent.setOwner(-1)
					pCurrent.setOwner(iCiv)

		for x in range(tCapital[0] - 11, tCapital[0] + 12): # must include the distance from Sogut to the Caspius
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
##				else: #search another place
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
##						if (self.getSpawnDelay(iCiv) < 10): #wait
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
##					if (unit.getUnitType() == xml.iSettler):
##						break
##				unit.found()
				utils.flipUnitsInArea((tCapital[0]-4, tCapital[1]-4), (tCapital[0]+4, tCapital[1]+4), iCiv, iBarbarian, True, True) #This is for AI only. During Human player spawn, that area is already cleaned
				for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
					utils.flipUnitsInArea((tCapital[0]-2, tCapital[1]-2), (tCapital[0]+2, tCapital[1]+2), iCiv, i, True, False) #This is for AI only. During Human player spawn, that area is already cleaned
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
			print ("utils.flipUnitsInArea()")
			#cover plots revealed by the catapult
			plotZero = gc.getMap().plot( 30, 0 ) #sync with rfcebalance module
			if (plotZero.getNumUnits()):
				catapult = plotZero.getUnit(0)
				catapult.kill(False, iCiv)
			gc.getMap().plot(29, 0).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(30, 0).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(31, 0).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(29, 1).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(30, 1).setRevealed(iCiv, False, True, -1);
			gc.getMap().plot(31, 1).setRevealed(iCiv, False, True, -1);
			print ("Plots covered")

			if (gc.getPlayer(iCiv).getNumCities() > 0):
				capital = gc.getPlayer(iCiv).getCapitalCity()
				self.createStartingWorkers(iCiv, (capital.getX(), capital.getY()))

			if (iNumHumanCitiesToConvert> 0):
				self.flipPopup(iCiv, tTopLeft, tBottomRight)


	def birthInForeignBorders(self, iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight, tCapital):

		print( " 3Miro: Birth in Foreign Land: ",iCiv,tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight, tCapital)
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

		else: #search another place
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
						#self.flipPopup(iCiv, tTopLeft, tBottomRight)
				#case 3: other
				elif (not loopCity.isCapital()): # 3Miro: this keeps crashing in the C++, makes no sense
				#elif ( True ): #utils.debugTextPopup( 'OTHER' )
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
		"""Searches a sea plot that isn't occupied by a unit within range of the starting coordinates"""
		# we can search inside other players territory, since all naval units can cross sea borders
		seaPlotList = []
		for x in range(tCoords[0] - iRange, tCoords[0] + iRange+1):
			for y in range(tCoords[1] - iRange, tCoords[1] + iRange+1):
				pCurrent = gc.getMap().plot( x, y )
				if ( pCurrent.isWater()):
					if ( not pCurrent.isUnit() ):
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
		if ( (not pFrankia.isAlive()) and (not pFrankia.getEverRespawned()) and iGameTurn > con.tBirth[iFrankia] + 25 and iGameTurn > utils.getLastTurnAlive(iFrankia) + 12 ):
			# France united in it's modern borders, start of the Bourbon royal line
			if ( iGameTurn > xml.i1588AD and iGameTurn < xml.i1700AD and iGameTurn % 5 == 3 ):
				return iFrankia
		if ( (not pArabia.isAlive()) and (not pArabia.getEverRespawned()) and iGameTurn > con.tBirth[iArabia] + 25 and iGameTurn > utils.getLastTurnAlive(iArabia) + 10 ):
			# Saladin, Ayyubid Dynasty
			if ( iGameTurn > xml.i1080AD and iGameTurn < xml.i1291AD and iGameTurn % 7 == 3 ):
				return iArabia
		if ( (not pBulgaria.isAlive()) and (not pBulgaria.getEverRespawned()) and iGameTurn > con.tBirth[iBulgaria] + 25 and iGameTurn > utils.getLastTurnAlive(iBulgaria) + 10 ):
			# second Bulgarian Empire
			if ( iGameTurn > xml.i1080AD and iGameTurn < xml.i1299AD and iGameTurn % 5 == 1 ):
				return iBulgaria
		if ( (not pCordoba.isAlive()) and (not pCordoba.getEverRespawned()) and iGameTurn > con.tBirth[iCordoba] + 25 and iGameTurn > utils.getLastTurnAlive(iCordoba) + 10 ):
			# special respawn as the Hafsid dynasty in North Africa
			if ( iGameTurn > xml.i1229AD and iGameTurn < xml.i1540AD and iGameTurn % 5 == 3 ):
				return iCordoba
		if ( (not pBurgundy.isAlive()) and (not pBurgundy.getEverRespawned()) and iGameTurn > con.tBirth[iBurgundy] + 25 and iGameTurn > utils.getLastTurnAlive(iBurgundy) + 20 ):
			# Burgundy in the 100 years war
			if ( iGameTurn > xml.i1336AD and iGameTurn < xml.i1453AD and iGameTurn % 8 == 1 ):
				return iBurgundy
		if ( (not pPrussia.isAlive()) and (not pPrussia.getEverRespawned()) and iGameTurn > con.tBirth[iPrussia] + 25 and iGameTurn > utils.getLastTurnAlive(iPrussia) + 10 ):
			# respawn as the unified Prussia
			if ( iGameTurn > xml.i1618AD and iGameTurn % 3 == 1 ):
				return iPrussia
		if ( (not pHungary.isAlive()) and (not pHungary.getEverRespawned()) and iGameTurn > con.tBirth[iHungary] + 25 and iGameTurn > utils.getLastTurnAlive(iHungary) + 10 ):
			# reconquest of Buda from the Ottomans
			if ( iGameTurn > xml.i1680AD and iGameTurn % 6 == 2 ):
				return iHungary
		if ( (not pSpain.isAlive()) and (not pSpain.getEverRespawned()) and iGameTurn > con.tBirth[iSpain] + 25 and iGameTurn > utils.getLastTurnAlive(iSpain) + 25 ):
			# respawn as the Castile/Aragon Union
			if ( iGameTurn > xml.i1470AD and iGameTurn < xml.i1580AD and iGameTurn % 5 == 0 ):
				return iSpain
		if ( (not pEngland.isAlive()) and (not pEngland.getEverRespawned()) and iGameTurn > con.tBirth[iEngland] + 25 and iGameTurn > utils.getLastTurnAlive(iEngland) + 12 ):
			# restoration of monarchy
			if ( iGameTurn > xml.i1660AD and iGameTurn % 6 == 2 ):
				return iEngland
		if ( (not pScotland.isAlive()) and (not pScotland.getEverRespawned()) and iGameTurn > con.tBirth[iScotland] + 25 and iGameTurn > utils.getLastTurnAlive(iScotland) + 30 ):
			if ( iGameTurn <= xml.i1600AD and iGameTurn % 6 == 3 ):
				return iScotland
		if ( (not pPortugal.isAlive()) and (not pPortugal.getEverRespawned()) and iGameTurn > con.tBirth[iPortugal] + 25 and iGameTurn > utils.getLastTurnAlive(iPortugal) + 10 ):
			# respawn to be around for colonies
			if ( iGameTurn > xml.i1431AD and iGameTurn < xml.i1580AD and iGameTurn % 5 == 3 ):
				return iPortugal
		if ( (not pAustria.isAlive()) and (not pAustria.getEverRespawned()) and iGameTurn > con.tBirth[iAustria] + 25 and iGameTurn > utils.getLastTurnAlive(iAustria) + 10 ):
			# increasing Habsburg influence in Hungary
			if ( iGameTurn > xml.i1526AD and iGameTurn < xml.i1690AD and iGameTurn % 8 == 3 ):
				return iAustria
		if ( (not pKiev.isAlive()) and (not pKiev.getEverRespawned()) and iGameTurn > con.tBirth[iKiev] + 25 and iGameTurn > utils.getLastTurnAlive(iKiev) + 10 ):
			# Cossack Hetmanate
			if ( iGameTurn >= xml.i1620AD and iGameTurn < xml.i1750AD and iGameTurn % 5 == 3 ):
				return iKiev
		if ( (not pMorocco.isAlive()) and (not pMorocco.getEverRespawned()) and iGameTurn > con.tBirth[iMorocco] + 25 and iGameTurn > utils.getLastTurnAlive(iMorocco) + 10 ):
			# Alaouite Dynasty
			if ( iGameTurn > xml.i1631AD and iGameTurn % 8 == 7 ):
				return iMorocco
		if ( (not pAragon.isAlive()) and (not pAragon.getEverRespawned()) and iGameTurn > con.tBirth[iAragon] + 25 and iGameTurn > utils.getLastTurnAlive(iAragon) + 10 ):
			# Kingdom of Sicily
			if ( iGameTurn > xml.i1700AD and iGameTurn % 8 == 7 ):
				return iAragon
		if ( (not pVenecia.isAlive()) and (not pVenecia.getEverRespawned()) and iGameTurn > con.tBirth[iVenecia] + 25 and iGameTurn > utils.getLastTurnAlive(iVenecia) + 10 ):
			if ( iGameTurn > xml.i1401AD and iGameTurn < xml.i1571AD and iGameTurn % 8 == 7 ):
				return iVenecia
		if ( (not pPoland.isAlive()) and (not pPoland.getEverRespawned()) and iGameTurn > con.tBirth[iPoland] + 25 and iGameTurn > utils.getLastTurnAlive(iPoland) + 10 ):
			if ( iGameTurn > xml.i1410AD and iGameTurn < xml.i1570AD and iGameTurn % 8 == 7 ):
				return iPoland
		if ( (not pTurkey.isAlive()) and (not pTurkey.getEverRespawned()) and iGameTurn > con.tBirth[iTurkey] + 25 and iGameTurn > utils.getLastTurnAlive(iTurkey) + 10 ):
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
		rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot abroad human players (or in general, the old civ if human player just switched) borders')
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
		if ( iCiv == iArabia ):
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
		elif ( iCiv == iBulgaria ):
			utils.makeUnit(xml.iBulgarianKonnik, iCiv, tPlot, 2)
		elif ( iCiv == iCordoba ):
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
		elif ( iCiv == iVenecia ):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
		elif ( iCiv == iBurgundy ):
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
		elif ( iCiv == iGermany ):
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
		elif ( iCiv == iNovgorod ):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
		elif ( iCiv == iNorway ):
			utils.makeUnit(xml.iVikingBeserker, iCiv, tPlot, 4)
		elif ( iCiv == iKiev ):
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 3)
		elif ( iCiv == iHungary ):
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
		elif ( iCiv == iSpain ):
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
		elif ( iCiv == iDenmark ):
			utils.makeUnit(xml.iDenmarkHuskarl, iCiv, tPlot, 3)
		elif ( iCiv == iScotland ):
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 3)
		elif ( iCiv == iPoland ):
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 3)
		elif ( iCiv == iGenoa ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
		elif ( iCiv == iMorocco ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iEngland ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iPortugal ):
			utils.makeUnit(xml.iPortugalFootKnight, iCiv, tPlot, 3)
		elif ( iCiv == iAragon ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 4)
		elif ( iCiv == iSweden ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iPrussia ):
			utils.makeUnit(xml.iTeutonic, iCiv, tPlot, 3)
		elif ( iCiv == iLithuania ):
			utils.makeUnit(xml.iLithuanianBajoras, iCiv, tPlot, 2)
		elif ( iCiv == iAustria ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iTurkey ):
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iMoscow ):
			utils.makeUnit(xml.iMoscowBoyar, iCiv, tPlot, 2)
		elif ( iCiv == iDutch ):
			utils.makeUnit(xml.iNetherlandsGrenadier, iCiv, tPlot, 2)


	def createStartingUnits( self, iCiv, tPlot ):
		# set the provinces
		self.pm.onSpawn( iCiv )
		# Change here to make later starting civs work
		if (iCiv == iArabia):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 6)
		elif (iCiv == iBulgaria):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iBulgarianKonnik, iCiv, tPlot, 5)
		elif (iCiv == iCordoba):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 3)
		elif (iCiv == iVenecia):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 1)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots((57,35), 2)
			if ( tSeaPlot ):
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
				pVenecia.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pVenecia.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iArcher,iCiv,tSeaPlot,1)
				pVenecia.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
		elif (iCiv == iBurgundy):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
		elif (iCiv == iGermany):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
		elif (iCiv == iNovgorod):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 1)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 1)
		elif (iCiv == iNorway):
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
		elif (iCiv == iKiev):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 3)
		elif (iCiv == iHungary):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
		elif (iCiv == iSpain):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCatapult, iCiv, tPlot, 1)
		elif (iCiv == iDenmark):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iDenmarkHuskarl, iCiv, tPlot, 4)
			tSeaPlot = self.findSeaPlots((60,57), 2)
			if ( tSeaPlot ):
				pDenmark.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pDenmark.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pDenmark.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1 )
		elif (iCiv == iScotland):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
		elif (iCiv == iPoland):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
		elif (iCiv == iGenoa):
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
		elif (iCiv == iMorocco):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 1)
		elif (iCiv == iEngland):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iLongSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				pEngland.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
			if (not gc.getPlayer(iEngland).isHuman()):
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
				utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 1)
		elif (iCiv == iPortugal):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iPortugalFootKnight, iCiv, tPlot, 4)
			utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
		elif (iCiv == iAragon):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAragonAlmogavar, iCiv, tPlot, 5)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			# Look for a sea plot close to the coast
			tSeaPlot = self.findSeaPlots((39,28), 2)
			if ( tSeaPlot ):
				pAragon.initUnit(xml.iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pAragon.initUnit(xml.iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
		elif (iCiv == iSweden):
			utils.makeUnit(xml.iLongSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots((69,65), 2)
			if ( tSeaPlot ):
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
				pSweden.initUnit(xml.iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pSweden.initUnit(xml.iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pSweden.initUnit(xml.iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
		elif (iCiv == iPrussia):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iTeutonic, iCiv, tPlot, 3) # one will probably leave for Crusade
			utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
			utils.makeUnit(xml.iExecutive3, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 3)
		elif (iCiv == iLithuania):
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iLithuanianBajoras, iCiv, tPlot, 5)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 3)
		elif (iCiv == iAustria):
			utils.makeUnit(xml.iArbalest, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iKnight, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
		elif (iCiv == iTurkey):
			utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 5)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iKnight, iCiv, tPlot, 4)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
			utils.makeUnit(xml.iTurkeyGreatBombard, iCiv, tPlot, 3)
			utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 4)
		elif (iCiv == iMoscow):
			utils.makeUnit(xml.iArbalest, iCiv, tPlot, 5)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iMoscowBoyar, iCiv, tPlot, 5)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 4)
			utils.makeUnit(xml.iOrthodoxMissionary, iCiv, tPlot, 3)
		elif (iCiv == iDutch):
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iMusketman, iCiv, tPlot, 8)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 3)
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
		# Absinthe: second Ottoman spawn stack may stay, although they now spawn in Gallipoli in the first place (one plot SE)
		if ( iCiv == iTurkey ):
			self.ottomanInvasion(iCiv,(77,23))


	def create1200ADstartingUnits( self ):

		if ( pSweden.isHuman() and con.tBirth[iSweden] > 0 ):
			# Absinthe: prohibit Danish contact in 1200AD
			tSwedishStart = ( tCapitals[iSweden][0]-2, tCapitals[iSweden][1]+2)
			utils.makeUnit(xml.iSettler, iSweden, tSwedishStart, 1)
			utils.makeUnit(xml.iSwordsman, iSweden, tSwedishStart, 1)

		elif ( pPrussia.isHuman() and con.tBirth[iPrussia] > 0 ):
			# Absinthe: prohibit Polish contact in 1200AD
			tPrussianStart = ( tCapitals[iPrussia][0]+1, tCapitals[iPrussia][1]+1)
			utils.makeUnit(xml.iSettler, iPrussia, tPrussianStart, 1)
			utils.makeUnit(xml.iSwordsman, iPrussia, tPrussianStart, 1)

		elif ( pLithuania.isHuman() and con.tBirth[iLithuania] > 0 ):
			# Absinthe: prohibit Kievan contact in 1200AD
			tLithuanianStart = ( tCapitals[iLithuania][0]-2, tCapitals[iLithuania][1])
			utils.makeUnit(xml.iSettler, iLithuania, tLithuanianStart, 1)
			utils.makeUnit(xml.iSwordsman, iLithuania, tLithuanianStart, 1)

		elif ( pAustria.isHuman() and con.tBirth[iAustria] > 0 ):
			# Absinthe: prohibit German and Hungarian contact in 1200AD
			tAustrianStart = ( tCapitals[iAustria][0]-3, tCapitals[iAustria][1]-1)
			utils.makeUnit(xml.iSettler, iAustria, tAustrianStart, 1)
			utils.makeUnit(xml.iLongSwordsman, iAustria, tAustrianStart, 1)

		elif ( pTurkey.isHuman() and con.tBirth[iTurkey] > 0 ):
			# Absinthe: prohibit Byzantine contact in 1200AD
			tTurkishStart = ( 98, 18 )
			utils.makeUnit(xml.iSettler, iTurkey, tTurkishStart, 1)
			utils.makeUnit(xml.iMaceman, iTurkey, tTurkishStart, 1)

		elif ( pMoscow.isHuman() and con.tBirth[iMoscow] > 0 ):
			utils.makeUnit(xml.iSettler, iMoscow, tCapitals[iMoscow], 1)
			utils.makeUnit(xml.iMaceman, iMoscow, tCapitals[iMoscow], 1)

		elif ( pDutch.isHuman() and con.tBirth[iDutch] > 0 ):
			utils.makeUnit(xml.iSettler, iDutch, tCapitals[iDutch], 1)
			utils.makeUnit(xml.iMaceman, iDutch, tCapitals[iDutch], 1)


	def ottomanInvasion(self,iCiv,tPlot):
		print("I made Ottomans on Gallipoli")
		utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 2)
		utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
		utils.makeUnit(xml.iKnight, iCiv, tPlot, 3)
		utils.makeUnit(xml.iTurkeyGreatBombard, iCiv, tPlot, 2)
		utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 2)


	def create500ADstartingUnits( self ):
		# 3Miro: units on start (note Spearman might be an up to date upgraded defender, tech dependent)

		utils.makeUnit(xml.iSettler, iFrankia, tCapitals[iFrankia], 3)
		utils.makeUnit(xml.iArcher, iFrankia, tCapitals[iFrankia], 3)
		utils.makeUnit(xml.iAxeman, iFrankia, tCapitals[iFrankia], 4)
		utils.makeUnit(xml.iWorker, iFrankia, tCapitals[iFrankia], 2)
		utils.makeUnit(xml.iCatholicMissionary, iFrankia, tCapitals[iFrankia], 1)

		self.showArea(iByzantium)
		self.initContact(iByzantium)
		self.showArea(iFrankia)
		self.showArea(iPope)

		if ( pBurgundy.isHuman() and con.tBirth[iBurgundy] > 0 ):
			utils.makeUnit(xml.iSettler, iBurgundy, tCapitals[iBurgundy], 1)
			utils.makeUnit(xml.iArcher, iBurgundy, tCapitals[iBurgundy], 1)

		elif ( pArabia.isHuman() and con.tBirth[iArabia] > 0 ):
			# Absinthe: prohibit Byzantine contact on turn 0
			tArabStart = ( tCapitals[iArabia][0], tCapitals[iArabia][1]-10)
			utils.makeUnit(xml.iSettler, iArabia, tArabStart, 1)
			utils.makeUnit(xml.iSpearman, iArabia, tArabStart, 1)

		elif ( pBulgaria.isHuman() and con.tBirth[iBulgaria] > 0 ):
			# Absinthe: prohibit Byzantine contact on turn 0
			tBulgStart = ( tCapitals[iBulgaria][0], tCapitals[iBulgaria][1] + 1 )
			utils.makeUnit(xml.iSettler, iBulgaria, tBulgStart, 1)
			utils.makeUnit(xml.iSpearman, iBulgaria, tBulgStart, 1)

		elif ( pCordoba.isHuman() and con.tBirth[iCordoba] > 0 ):
			utils.makeUnit(xml.iSettler, iCordoba, tCapitals[iCordoba], 1)
			utils.makeUnit(xml.iSpearman, iCordoba, tCapitals[iCordoba], 1)

		elif ( pSpain.isHuman() and con.tBirth[iSpain] > 0 ):
			utils.makeUnit(xml.iSettler, iSpain, tCapitals[iSpain], 1)
			utils.makeUnit(xml.iSpearman, iSpain, tCapitals[iSpain], 1)

		elif ( pNorway.isHuman() and con.tBirth[iNorway] > 0 ):
			utils.makeUnit(xml.iSettler, iNorway, tCapitals[iNorway], 1)
			utils.makeUnit(xml.iSpearman, iNorway, tCapitals[iNorway], 1)

		elif ( pDenmark.isHuman() and con.tBirth[iDenmark] > 0 ):
			utils.makeUnit(xml.iSettler, iDenmark, tCapitals[iDenmark], 1)
			utils.makeUnit(xml.iSpearman, iDenmark, tCapitals[iDenmark], 1)

		elif ( pVenecia.isHuman() and con.tBirth[iVenecia] > 0 ):
			utils.makeUnit(xml.iSettler, iVenecia, tCapitals[iVenecia], 1)
			utils.makeUnit(xml.iSpearman, iVenecia, tCapitals[iVenecia], 1)

		elif ( pNovgorod.isHuman() and con.tBirth[iNovgorod] > 0 ):
			utils.makeUnit(xml.iSettler, iNovgorod, tCapitals[iNovgorod], 1)
			utils.makeUnit(xml.iSpearman, iNovgorod, tCapitals[iNovgorod], 1)

		elif ( pKiev.isHuman() and con.tBirth[iKiev] > 0 ):
			utils.makeUnit(xml.iSettler, iKiev, tCapitals[iKiev], 1)
			utils.makeUnit(xml.iSpearman, iKiev, tCapitals[iKiev], 1)

		elif ( pHungary.isHuman() and con.tBirth[iHungary] > 0 ):
			utils.makeUnit(xml.iSettler, iHungary, tCapitals[iHungary], 1)
			utils.makeUnit(xml.iSpearman, iHungary, tCapitals[iHungary], 1)

		elif ( pGermany.isHuman() and con.tBirth[iGermany] > 0 ):
			utils.makeUnit(xml.iSettler, iGermany, tCapitals[iGermany], 1)
			utils.makeUnit(xml.iSpearman, iGermany, tCapitals[iGermany], 1)

		elif ( pScotland.isHuman() and con.tBirth[iScotland] > 0 ):
			utils.makeUnit(xml.iSettler, iScotland, tCapitals[iScotland], 1)
			utils.makeUnit(xml.iSpearman, iScotland, tCapitals[iScotland], 1)

		elif ( pPoland.isHuman() and con.tBirth[iPoland] > 0 ):
			utils.makeUnit(xml.iSettler, iPoland, tCapitals[iPoland], 1)
			utils.makeUnit(xml.iSpearman, iPoland, tCapitals[iPoland], 1)

		elif ( pMoscow.isHuman() and con.tBirth[iMoscow] > 0 ):
			utils.makeUnit(xml.iSettler, iMoscow, tCapitals[iMoscow], 1)
			utils.makeUnit(xml.iSpearman, iMoscow, tCapitals[iMoscow], 1)

		elif ( pGenoa.isHuman() and con.tBirth[iGenoa] > 0 ):
			utils.makeUnit(xml.iSettler, iGenoa, tCapitals[iGenoa], 1)
			utils.makeUnit(xml.iSpearman, iGenoa, tCapitals[iGenoa], 1)

		elif ( pMorocco.isHuman() and con.tBirth[iMorocco] > 0 ):
			utils.makeUnit(xml.iSettler, iMorocco, tCapitals[iMorocco], 1)
			utils.makeUnit(xml.iSpearman, iMorocco, tCapitals[iMorocco], 1)

		elif ( pEngland.isHuman() and con.tBirth[iEngland] > 0 ):
			utils.makeUnit(xml.iSettler, iEngland, tCapitals[iEngland], 1)
			utils.makeUnit(xml.iSwordsman, iEngland, tCapitals[iEngland], 1)

		elif ( pPortugal.isHuman() and con.tBirth[iPortugal] > 0 ):
			utils.makeUnit(xml.iSettler, iPortugal, tCapitals[iPortugal], 1)
			utils.makeUnit(xml.iSwordsman, iPortugal, tCapitals[iPortugal], 1)

		elif ( pAragon.isHuman() and con.tBirth[iAragon] > 0 ):
			utils.makeUnit(xml.iSettler, iAragon, tCapitals[iAragon], 1)
			utils.makeUnit(xml.iSwordsman, iAragon, tCapitals[iAragon], 1)

		elif ( pPrussia.isHuman() and con.tBirth[iPrussia] > 0 ):
			utils.makeUnit(xml.iSettler, iPrussia, tCapitals[iPrussia], 1)
			utils.makeUnit(xml.iSwordsman, iPrussia, tCapitals[iPrussia], 1)

		elif ( pLithuania.isHuman() and con.tBirth[iLithuania] > 0 ):
			utils.makeUnit(xml.iSettler, iLithuania, tCapitals[iLithuania], 1)
			utils.makeUnit(xml.iSwordsman, iLithuania, tCapitals[iLithuania], 1)

		elif ( pAustria.isHuman() and con.tBirth[iAustria] > 0 ):
			utils.makeUnit(xml.iSettler, iAustria, tCapitals[iAustria], 1)
			utils.makeUnit(xml.iLongSwordsman, iAustria, tCapitals[iAustria], 1)

		elif ( pTurkey.isHuman() and con.tBirth[iTurkey] > 0 ):
			# Absinthe: prohibit Byzantine contact on turn 0
			tTurkishStart = ( 97, 23 )
			utils.makeUnit(xml.iSettler, iTurkey, tTurkishStart, 1)
			utils.makeUnit(xml.iMaceman, iTurkey, tTurkishStart, 1)

		elif ( pSweden.isHuman() and con.tBirth[iSweden] > 0 ):
			utils.makeUnit(xml.iSettler, iSweden, tCapitals[iSweden], 1)
			utils.makeUnit(xml.iSwordsman, iSweden, tCapitals[iSweden], 1)

		elif ( pDutch.isHuman() and con.tBirth[iDutch] > 0 ):
			utils.makeUnit(xml.iSettler, iDutch, tCapitals[iDutch], 1)
			utils.makeUnit(xml.iMaceman, iDutch, tCapitals[iDutch], 1)

	def assign1200ADtechs(self, iCiv):
		# Temporary everyone gets Aragon techs
		teamCiv = gc.getTeam(iCiv)
		for iTech in range( xml.iFarriers + 1 ):
			teamCiv.setHasTech( iTech, True, iCiv, False, False )
		teamCiv.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
		teamCiv.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
		teamCiv.setHasTech( xml.iLiterature, True, iCiv, False, False )
		teamCiv.setHasTech( xml.iLateenSails, True, iCiv, False, False )
		teamCiv.setHasTech( xml.iMapMaking, True, iCiv, False, False )
		teamCiv.setHasTech( xml.iAristocracy, True, iCiv, False, False )
		teamCiv.setHasTech( xml.iPlateArmor, True, iCiv, False, False )
		teamCiv.setHasTech( xml.iGothicArchitecture, True, iCiv, False, False )
		teamCiv.setHasTech( xml.iSiegeEngines, True, iCiv, False, False )
		if iCiv in [iArabia, iMorocco]:
			teamCiv.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )

	def assignTechs( self, iCiv ):
		# 3Miro: other than the original techs

		if ( con.tBirth[iCiv] == 0 ):
			return

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

		elif ( iCiv == iBulgaria ):
			teamBulgaria.setHasTech( xml.iTheology, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iCalendar, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iStirrup, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iArchitecture, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iBronzeCasting, True, iCiv, False, False )

		elif ( iCiv == iCordoba ):
			teamCordoba.setHasTech( xml.iTheology, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iCalendar, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iStirrup, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iBronzeCasting, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iArchitecture, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iEngineering, True, iCiv, False, False )
			teamCordoba.setHasTech( xml.iArabicMedicine, True, iCiv, False, False )

		elif ( iCiv == iVenecia ):
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
			
		elif ( iCiv == iBurgundy ):
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

		elif ( iCiv == iGermany ):
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

		elif ( iCiv == iNovgorod ):
			for iTech in range( xml.iStirrup + 1 ):
				teamNovgorod.setHasTech( iTech, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iChainMail, True, iCiv, False, False )

		elif ( iCiv == iNorway ):
			for iTech in range( xml.iStirrup + 1):
				teamNorway.setHasTech( iTech, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )

		elif ( iCiv == iKiev ):
			for iTech in range( xml.iStirrup + 1 ):
				teamKiev.setHasTech( iTech, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iChainMail, True, iCiv, False, False )

		elif ( iCiv == iHungary ):
			for iTech in range( xml.iStirrup + 1 ):
				teamHungary.setHasTech( iTech, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iArt, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iVassalage, True, iCiv, False, False )

		elif ( iCiv == iSpain ):
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

		elif ( iCiv == iDenmark ):
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

		elif ( iCiv == iScotland ):
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

		elif ( iCiv == iPoland ):
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

		elif ( iCiv == iGenoa ):
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

		elif ( iCiv == iMorocco ):
			for iTech in range( xml.iFarriers + 1 ):
				teamMorocco.setHasTech( iTech, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iMapMaking, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )

		elif ( iCiv == iEngland ):
			for iTech in range( xml.iFarriers + 1 ):
				teamEngland.setHasTech( iTech, True, iCiv, False, False )
			teamEngland.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamEngland.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamEngland.setHasTech( xml.iAristocracy, True, iCiv, False, False )

		elif ( iCiv == iPortugal ):
			for iTech in range( xml.iFarriers + 1 ):
				teamPortugal.setHasTech( iTech, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iMapMaking, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iAristocracy, True, iCiv, False, False )

		elif ( iCiv == iAragon ):
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

		elif ( iCiv == iSweden ):
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

		elif ( iCiv == iPrussia ):
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

		elif ( iCiv == iLithuania ):
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

		elif ( iCiv == iAustria ):
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

		elif ( iCiv == iTurkey ):
			for iTech in range( xml.iChivalry + 1 ):
				teamTurkey.setHasTech( iTech, True, iCiv, False, False )
			teamTurkey.setHasTech( xml.iGunpowder, True, iCiv, False, False )
			teamTurkey.setHasTech( xml.iMilitaryTradition, True, iCiv, False, False )
			teamTurkey.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )

		elif ( iCiv == iMoscow ):
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

		elif ( iCiv == iDutch ):
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


	def showArea(self, iCiv, iScenario = con.i500ADScenario):
		#print(" Visible for: ",iCiv )
		for iI in range( len( tVisible[iScenario][iCiv] ) ):
			self.showRect( iCiv, tVisible[iScenario][iCiv][iI][0], tVisible[iScenario][iCiv][iI][1], tVisible[iScenario][iCiv][iI][2], tVisible[iScenario][iCiv][iI][3] )
		#print(" Visible for: ",iCiv )
		#pass


	def initContact(self, iCiv , bMeet = True):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		for iOtherPlayer in con.lInitialContacts[utils.getScenario()][iCiv]:
			pOtherPlayer = gc.getPlayer(iOtherPlayer)
			tOtherPlayer = pOtherPlayer.getTeam()
			if pOtherPlayer.isAlive() and not teamCiv.isHasMet(tOtherPlayer):
				teamCiv.meet(tOtherPlayer, bMeet)

	def LeaningTowerGP(self):
		iGP = gc.getGame().getSorenRandNum(7, 'starting count')
		pFlorentia = gc.getMap().plot(54, 32).getPlotCity()
		iSpecialist = xml.iGreatProphet + iGP
		pFlorentia.setFreeSpecialistCount(iSpecialist, 1)

	def setDiplo1200AD(self):
		self.changeAttitudeExtra(iByzantium, iArabia, -2)
		self.changeAttitudeExtra(iScotland, iFrankia, 4)

	def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):
		gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
		gc.getPlayer(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)