# Rhye's and Fall of Civilization: Europe - Main RFC mechanics

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

lExtraPlots = con.lExtraPlots

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
		if popupReturn.getButtonClicked() == 0: # 1st button
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
		lPlots = utils.getPlotList(tTopLeft, tBottomRight) + lExtraPlots[iNewCiv]
		for (x, y) in lPlots:
			plot = gc.getMap().plot( x, y )
			if plot.isCity():
				if plot.getPlotCity().getOwner() == iHuman:
					if not plot.getPlotCity().isCapital():
						flipText += (plot.getPlotCity().getName() + "\n")
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
		lPlots = utils.getPlotList(tTopLeft, tBottomRight) + lExtraPlots[self.getNewCivFlip()]
		for (x, y) in lPlots:
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				city = plot.getPlotCity()
				if city.getOwner() == iHuman:
					if not city.isCapital():
						humanCityList.append(city)

		if popupReturn.getButtonClicked() == 0: # 1st button
			print ("Flip agreed")
			CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_AGREED", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)

			if humanCityList:
				for city in humanCityList:
					tCity = (city.getX(),city.getY())
					print ("flipping ", city.getName())
					utils.cultureManager(tCity, 100, iNewCivFlip, iHuman, False, False, False)
					utils.flipUnitsInCityBefore(tCity, iNewCivFlip, iHuman)
					self.setTempFlippingCity(tCity)
					utils.flipCity(tCity, 0, 0, iNewCivFlip, [iHuman])
					utils.flipUnitsInCityAfter(tCity, iNewCivFlip)

					#iEra = gc.getPlayer(iNewCivFlip).getCurrentEra()
					#if (iEra >= 2): #medieval
					#	if (city.getPopulation() < iEra):
					#		city.setPopulation(iEra) #causes an unidentifiable C++ exception

					#humanCityList[i].setHasRealBuilding(con.iPlague, False) #buggy

			#same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
			for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
				betrayalPlot = gc.getMap().plot(x,y)
				iNumUnitsInAPlot = betrayalPlot.getNumUnits()
				if iNumUnitsInAPlot > 0:
					for i in range(iNumUnitsInAPlot):
						unit = betrayalPlot.getUnit(i)
						if unit.getOwner() == iHuman:
							rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
							if rndNum >= iBetrayalThreshold:
								if unit.getDomainType() == DomainTypes.DOMAIN_SEA: #land unit
									iUnitType = unit.getUnitType()
									unit.kill(False, iNewCivFlip)
									utils.makeUnit(iUnitType, iNewCivFlip, (x,y), 1)
									i = i - 1

			if self.getCheatersCheck(0) == 0:
				self.setCheatersCheck(0, iCheatersPeriod)
				self.setCheatersCheck(1, self.getNewCivFlip())

		elif popupReturn.getButtonClicked() == 1: # 2nd button
			print ("Flip disagreed")
			CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)


			if humanCityList:
				for city in humanCityList:
					#city.setCulture(self.getNewCivFlip(), city.countTotalCulture(), True)
					pCurrent = gc.getMap().plot(city.getX(), city.getY())
					oldCulture = pCurrent.getCulture(iHuman)
					# Absinthe: changeCulture instead of setCulture, otherwise previous culture will be lost
					pCurrent.changeCulture(iNewCivFlip, oldCulture/2, True)
					pCurrent.setCulture(iHuman, oldCulture/2, True)
					iWar = self.getSpawnWar() + 1
					self.setSpawnWar(iWar)
					if self.getSpawnWar() == 1:
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
		if iChoice == 1:
			lList = self.getRebelSuppress()
			lList[iHuman] = 2 # let go + war
			self.setRebelSuppress( lList )
		elif iChoice == 2:
			if gc.getGame().getSorenRandNum(100, 'odds') < 40:
				lCityList = self.getRebelCities()
				for (x, y) in lCityList:
					pCity = gc.getMap().plot(x, y).getPlotCity()
					if pCity.getOwner() == iHuman:
						pCity.changeOccupationTimer( 2 )
						pCity.changeHurryAngerTimer( 10 )
				lList = self.getRebelSuppress()
				lList[iHuman] = 3 # keep cities + war
				self.setRebelSuppress( lList )
			else:
				lList = self.getRebelSuppress()
				lList[iHuman] = 4 # let go + war
				self.setRebelSuppress( lList )
		elif iChoice == 3:
			iLoyalPrice = min( (10 * gc.getPlayer( iHuman ).getGold()) / 100, 50 * iNumCities )
			gc.getPlayer( iHuman ).setGold( gc.getPlayer( iHuman ).getGold() - iLoyalPrice )
			if gc.getGame().getSorenRandNum(100, 'odds') < iLoyalPrice / iNumCities:
				lList = self.getRebelSuppress()
				lList[iHuman] = 1 # keep + no war
				self.setRebelSuppress( lList )
		elif iChoice == 4:
			iLoyalPrice = min( (10 * gc.getPlayer( iHuman ).getGold()) / 100, 50 * iNumCities )
			gc.getPlayer( iHuman ).setGold( gc.getPlayer( iHuman ).getGold() - iLoyalPrice )
			if gc.getGame().getSorenRandNum(100, 'odds') < iLoyalPrice / iNumCities + 40:
				lCityList = self.getRebelCities()
				for (x, y) in lCityList:
					pCity = gc.getMap().plot(x, y).getPlotCity()
					if pCity.getOwner() == iHuman:
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


	def onCityBuilt(self, iPlayer, pCity):
		tCity = (pCity.getX(), pCity.getY())
		x, y = tCity
		self.pm.onCityBuilt (iPlayer, pCity.getX(), pCity.getY())
		# Absinthe: We can add free buildings for new cities here
		#			Note that it will add the building every time a city is founded on the plot, not just on the first time
		# 			Venice (56, 35), Augsburg (55, 41), Porto (23, 31), Prague (60, 44), Riga (74, 58), Perekop (87, 36)
		#			London (41, 52), Novgorod (80, 62) currently has preplaced fort on the map instead
		if tCity in [(56, 35), (55, 41), (23, 31), (60, 44), (74, 58), (87, 36)]:
			pCity.setHasRealBuilding( utils.getUniqueBuilding(iPlayer, xml.iWalls), True )
		elif tCity == (75, 53): # Vilnius - important for AI Lithuania against Prussia
			if not gc.getPlayer(iLithuania).isHuman():
				pCity.setHasRealBuilding( utils.getUniqueBuilding(iPlayer, xml.iWalls), True )


	def onCityAcquired(self, owner, iPlayer, city, bConquest, bTrade):
		self.pm.onCityAcquired(owner, iPlayer, city, bConquest, bTrade)
		if iPlayer == iTurkey:
			cityList = utils.getCityList(iPlayer)
			if (city.getX(), city.getY()) == tCapitals[iByzantium]: # Constantinople (81,24)
				for loopCity in cityList:
					if loopCity != city:
						loopCity.setHasRealBuilding((xml.iPalace), False)
				city.setHasRealBuilding(xml.iPalace, True)
				if pTurkey.getStateReligion() == xml.iIslam:
					city.setHasReligion(xml.iIslam, True, True, False)

			# Absinthe: Edirne becomes capital if conquered before Constantinople
			else:
				if (city.getX(), city.getY()) == (76, 25):
					bHasIstanbul = False
					IstanbulPlot = gc.getMap().plot(tCapitals[iByzantium][0], tCapitals[iByzantium][1])
					if IstanbulPlot.isCity():
						if IstanbulPlot.getPlotCity().getOwner() == iPlayer:
							bHasIstanbul = True
					if not bHasIstanbul:
						gc.getPlayer(iPlayer).getCapitalCity().setHasRealBuilding(xml.iPalace, False)
						city.setHasRealBuilding(xml.iPalace, True)
					if pTurkey.getStateReligion() == xml.iIslam: # you get Islam anyway, as a bonus
						city.setHasReligion(xml.iIslam, True, True, False)


	def onCityRazed(self, iOwner, iPlayer, city):
		self.pm.onCityRazed(iOwner, iPlayer, city) # Province Manager


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
			if iCiv >= iArabia and not gc.getPlayer(iCiv).isHuman():
				self.setBirthTurnModifier(iCiv, (gc.getGame().getSorenRandNum(11, 'BirthTurnModifier') - 5)) # -5 to +5
		#now make sure that no civs spawn in the same turn and cause a double "new civ" popup
		for iCiv in range(iNumPlayers):
			if iCiv > utils.getHumanID() and iCiv < iNumPlayers:
				for j in range(iNumPlayers-1-iCiv):
					iNextCiv = iCiv+j+1
					if con.tBirth[iCiv]+self.getBirthTurnModifier(iCiv) == con.tBirth[iNextCiv]+self.getBirthTurnModifier(iNextCiv):
						self.setBirthTurnModifier(iNextCiv, (self.getBirthTurnModifier(iNextCiv)+1))


	def setEarlyLeaders(self):
		for iPlayer in range(iNumActivePlayers):
			if tEarlyLeaders[iPlayer] != tLeaders[iPlayer][0]:
				if not gc.getPlayer(iPlayer).isHuman():
					gc.getPlayer(iPlayer).setLeader(tEarlyLeaders[iPlayer])
					print ("leader starting switch:", tEarlyLeaders[iPlayer], "in civ", iPlayer)


	def setWarOnSpawn(self):
		for i in range( iNumMajorPlayers - 1 ): # exclude the Pope
			for j in range( iNumTotalPlayers ):
				if con.tWarAtSpawn[utils.getScenario()][i][j] > 0: # if there is a chance for war
					if gc.getGame().getSorenRandNum(100, 'war on spawn roll') < con.tWarAtSpawn[utils.getScenario()][i][j]:
						# Absinthe: will use setAtWar here instead of declareWar, so it won't affect diplo relations and other stuff between major civs
						gc.getTeam( gc.getPlayer(i).getTeam() ).setAtWar( gc.getPlayer(j).getTeam(), True )
						gc.getTeam( gc.getPlayer(j).getTeam() ).setAtWar( gc.getPlayer(i).getTeam(), True )


	def checkTurn(self, iGameTurn):

		#Trigger betrayal mode
		if self.getBetrayalTurns() > 0:
			self.initBetrayal()

		if self.getCheatersCheck(0) > 0:
			teamPlayer = gc.getTeam(gc.getPlayer(utils.getHumanID()).getTeam())
			if teamPlayer.isAtWar(self.getCheatersCheck(1)):
				print ("No cheaters!")
				self.initMinorBetrayal(self.getCheatersCheck(1))
				self.setCheatersCheck(0, 0)
				self.setCheatersCheck(1, -1)
			else:
				self.setCheatersCheck(0, self.getCheatersCheck(0)-1)

		if iGameTurn % 20 == 0:
			for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
				pIndy = gc.getPlayer( i )
				if pIndy.isAlive():
					utils.updateMinorTechs(i, iBarbarian)

		# Absinthe: checking the spawn dates
		for iLoopCiv in range( iNumMajorPlayers ):
			if con.tBirth[iLoopCiv] != 0 and iGameTurn >= con.tBirth[iLoopCiv] - 2 and iGameTurn <= con.tBirth[iLoopCiv] + 4:
				self.initBirth(iGameTurn, con.tBirth[iLoopCiv], iLoopCiv)

		# Fragment minor civs:
		# 3Miro: Shuffle cities between Indies and Barbs to make sure there is no big Independent nation
		if iGameTurn >= 20:
			if iGameTurn % 15 == 6:
				self.fragmentIndependents()
			if iGameTurn % 30 == 12:
				self.fragmentBarbarians(iGameTurn)

		# Fall of civs:
		# Barb collapse: if more than 1/3 of the empire is conquered and/or held by barbs = collapse
		# Generic collapse: if 1/2 of the empire is lost in only a few turns (16 ATM) = collapse
		# Motherland collapse: if no city is in the core area and the number of cities in the normal area is less than the number of foreign cities = collapse
		# Secession: if stability is negative there is a chance (bigger chance with worse stability) for a random city to declare it's independence
		if iGameTurn >= 64 and iGameTurn % 7 == 0: #mainly for Seljuks, Mongols, Timurids
			self.collapseByBarbs(iGameTurn)
		if iGameTurn >= 34 and iGameTurn % 16 == 0:
			self.collapseGeneric(iGameTurn)
		if iGameTurn >= 34 and iGameTurn % 9 == 7:
			self.collapseMotherland(iGameTurn)
		if iGameTurn > 20 and iGameTurn % 3 == 1:
			self.secession(iGameTurn)

		# Resurrection of civs:
		# This is one place to control the frequency of resurrection; will not be called with high iNumDeadCivs
		# Generally we want to allow Kiev, Bulgaria, Cordoba, Burgundy, Byzantium at least to be dead in late game without respawning
		# Absinthe: was 12 and 8 originally in RFCE, but we don't need that many dead civs
		iNumDeadCivs1 = 8 #5 in vanilla RFC, 8 in warlords RFC
		iNumDeadCivs2 = 5 #3 in vanilla RFC, 6 in warlords RFC

		iCiv = self.getSpecialRespawn( iGameTurn )
		if iCiv > -1:
			self.resurrection(iGameTurn,iCiv)
		elif gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs1:
			if iGameTurn % 10 == 7:
				self.resurrection(iGameTurn, -1)
		elif gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs2:
			if iGameTurn % 23 == 11:
				self.resurrection(iGameTurn, -1)
		#lSpecialRespawnTurn = self.getSpecialRespawnTurns()
		#print("Special Respawn Turns ",lSpecialRespawnTurn)
		#if iGameTurn in lSpecialRespawnTurn:
		#	iCiv = lSpecialRespawnTurn.index(iGameTurn)#Lookup index for
		#	print("Special Respawn For Player: ",iCiv)
		#	if iCiv < iNumMajorPlayers and iCiv > 0:
		#		self.resurrection(iGameTurn,iCiv)

		# Absinthe: Reduce cities to towns, in order to make room for new civs
		if iGameTurn == con.tBirth[con.iScotland] -3:
			# Reduce Inverness and Scone, so more freedom in where to found cities in Scotland
			self.reduceCity((37,65))
			self.reduceCity((37,67))
		elif iGameTurn == con.tBirth[con.iEngland] -3:
			# Reduce Norwich and Nottingham, so more freedom in where to found cities in England
			self.reduceCity((43,55))
			self.reduceCity((39,56))
		elif iGameTurn == con.tBirth[con.iSweden] -2:
			# Reduce Uppsala
			self.reduceCity((65,66))


	def reduceCity(self, tPlot):
		# Absinthe: disappearing cities (reducing them to an improvement)
		pPlot = gc.getMap().plot(tPlot[0],tPlot[1])
		if pPlot.isCity():
			# Absinthe: apologize from the player:
			msgString = CyTranslator().getText("TXT_KEY_REDUCE_CITY_1", ()) + " " + pPlot.getPlotCity().getName() + " " + CyTranslator().getText("TXT_KEY_REDUCE_CITY_2", ())
			CyInterface().addMessage(pPlot.getPlotCity().getOwner(), False, con.iDuration, msgString, "", 0, "", ColorTypes(con.iOrange), tPlot[0], tPlot[1], True, True)

			pPlot.eraseCityDevelopment()
			pPlot.setImprovementType(xml.iImprovementTown) # Improvement Town instead of the city
			pPlot.setRouteType(0) # Also adding a road there


	def checkPlayerTurn(self, iGameTurn, iPlayer):
		# Absinthe: leader switching
		# Merijn: upto infinite leaders now
		if len(tLeaders[iPlayer]) > 1:
			for tLeader in reversed(tLateLeaders[iPlayer]):
				if iGameTurn >= tLeader[1]:
					self.switchLateLeaders(iPlayer, tLeader)

		# Absinthe: potential leader switching on anarchy
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

		# 3Miro: English cheat, the AI is utterly incompetent when it has to launch an invasion on an island
		#			if in 1300AD Dublin is still Barbarian, it will flip to England
		if iGameTurn == xml.i1300AD and utils.getHumanID() != iEngland and iPlayer == iEngland and pEngland.isAlive():
			tDublin = (32, 58)
			pPlot = gc.getMap().plot(tDublin[0], tDublin[1])
			if pPlot.isCity():
				if pPlot.getPlotCity().getOwner() == con.iBarbarian:
					pDublin = pPlot.getPlotCity()
					utils.cultureManager(tDublin, 50, iEngland, iBarbarian, False, True, True)
					utils.flipUnitsInCityBefore(tDublin, iEngland, iBarbarian)
					self.setTempFlippingCity(tDublin)
					utils.flipCity(tDublin, 0, 0, iEngland, [iBarbarian]) #by trade because by conquest may raze the city
					utils.flipUnitsInCityAfter(tDublin, iEngland)

		# Absinthe: Another English AI cheat, extra defenders and defensive buildings in Normandy some turns after spawn - from RFCE++
		if iGameTurn == xml.i1066AD + 3 and utils.getHumanID() != iEngland and iPlayer == iEngland and pEngland.isAlive():
			print("Giving England some help in Normandy..")
			for (x, y) in utils.getPlotList((39, 46), (45, 50)):
				print("Is ", x, y, " an English city?")
				pCurrent = gc.getMap().plot( x, y )
				if pCurrent.isCity():
					pCity = pCurrent.getPlotCity()
					if pCity.getOwner() == iEngland:
						print("Yes! Defenders get!")
						utils.makeUnit(xml.iGuisarme, iEngland, (x, y), 1)
						utils.makeUnit(xml.iArbalest, iEngland, (x, y), 1)
						pCity.setHasRealBuilding(xml.iWalls, True)
						pCity.setHasRealBuilding(xml.iCastle,True)


	def switchLateLeaders(self, iPlayer, tLeader):
		iLeader, iDate, iThreshold, iEra = tLeader
		if iLeader == gc.getPlayer(iPlayer).getLeader():
			return
		if gc.getPlayer(iPlayer).getCurrentEra() >= iEra:
			iThreshold *= 2
		if gc.getPlayer(iPlayer).getAnarchyTurns() != 0 or utils.getPlagueCountdown(iPlayer) > 0 or utils.getStability(iPlayer) <= -10 or gc.getGame().getSorenRandNum(100, 'die roll') < iThreshold:
			gc.getPlayer(iPlayer).setLeader(iLeader)
			#print ("leader late switch:", tLateLeaders[iPlayer][iLeaderIndex], "in civ", iPlayer)

			# Absinthe: message about the leader switch for the human player
			iHuman = utils.getHumanID()
			HumanTeam = gc.getTeam(gc.getPlayer(iHuman).getTeam())
			PlayerTeam = gc.getPlayer(iPlayer).getTeam()
			if HumanTeam.isHasMet(PlayerTeam) and utils.isActive(iHuman): # only if it's a known civ
				CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_LEADER_SWITCH", (gc.getPlayer(iPlayer).getName(), gc.getPlayer(iPlayer).getCivilizationDescriptionKey())), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, "", ColorTypes(con.iPurple), -1, -1, True, True)


	def fragmentIndependents(self):
		for iIndep1 in range( con.iIndepStart, con.iIndepEnd + 1):
			pIndep1 = gc.getPlayer( iIndep1 )
			iNumCities1 = pIndep1.getNumCities()
			for iIndep2 in range( con.iIndepStart, con.iIndepEnd + 1):
				if iIndep1 == iIndep2: continue
				pIndep2 = gc.getPlayer( iIndep2 )
				iNumCities2 = pIndep2.getNumCities()
				if abs(iNumCities1 - iNumCities2) > 5:
					if iNumCities1 > iNumCities2:
						iBig = iIndep1
						iSmall = iIndep2
					else:
						iBig = iIndep2
						iSmall = iIndep1
					iDivideCounter = 0
					iCounter = 0
					for city in utils.getCityList(iBig):
						iDivideCounter += 1
						if iDivideCounter % 2 == 1:
							tCity = (city.getX(), city.getY())
							pCurrent = gc.getMap().plot(tCity[0], tCity[1])
							utils.cultureManager(tCity, 50, iSmall, iBig, False, True, True)
							utils.flipUnitsInCityBefore(tCity, iSmall, iBig)
							self.setTempFlippingCity(tCity)
							utils.flipCity(tCity, 0, 0, iSmall, [iBig]) #by trade because by conquest may raze the city
							utils.flipUnitsInCityAfter(tCity, iSmall)
							iCounter += 1
							if iCounter == 3:
								break


	def fragmentBarbarians(self, iGameTurn):
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iNumPlayers):
			iDeadCiv = (j + iRndnum) % iNumPlayers
			if not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > con.tBirth[iDeadCiv] + 50:
				pDeadCiv = gc.getPlayer(iDeadCiv)
				teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
				lCities = []
				for (x, y) in utils.getPlotList(tNormalAreasTL[iDeadCiv], tNormalAreasBR[iDeadCiv]):
					plot = gc.getMap().plot( x, y )
					if plot.isCity():
						if plot.getPlotCity().getOwner() == iBarbarian:
							lCities.append((x, y))
				if len(lCities) > 5:
					iDivideCounter = 0
					for tCity in lCities:
						iNewCiv = con.iIndepStart + gc.getGame().getSorenRandNum(con.iIndepEnd - con.iIndepStart + 1, 'randomIndep')
						if iDivideCounter % 4 in [0, 1]:
							utils.cultureManager(tCity, 50, iNewCiv, iBarbarian, False, True, True)
							utils.flipUnitsInCityBefore(tCity, iNewCiv, iBarbarian)
							self.setTempFlippingCity(tCity)
							utils.flipCity(tCity, 0, 0, iNewCiv, [iBarbarian]) #by trade because by conquest may raze the city
							utils.flipUnitsInCityAfter(tCity, iNewCiv)
							iDivideCounter += 1
					return


	def collapseByBarbs(self, iGameTurn):
		# Absinthe: collapses if more than 1/3 of the empire is conquered and/or held by barbs
		for iCiv in range(iNumPlayers):
			pCiv = gc.getPlayer(iCiv)
			if pCiv.isAlive():
				# Absinthe: no barb collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
				iRespawnTurn = utils.getLastRespawnTurn( iCiv )
				if iGameTurn >= con.tBirth[iCiv] + 20 and iGameTurn >= iRespawnTurn + 10 and not utils.collapseImmune(iCiv):
					iNumCities = pCiv.getNumCities()
					iLostCities = gc.countCitiesLostTo( iCiv, iBarbarian )
					# Absinthe: if the civ is respawned, it's harder to collapse them by barbs
					if pCiv.getRespawnedAlive():
						iLostCities = max( iLostCities-(iNumCities/4), 0 )
					# Absinthe: if more than one third is captured, the civ collapses
					if iLostCities*2 > iNumCities+1 and iNumCities > 0:
						print ("COLLAPSE BARBS", gc.getPlayer(iCiv).getCivilizationAdjective(0))
						if not pCiv.isHuman():
							utils.killAndFragmentCiv(iCiv, False, False)
						elif pCiv.getNumCities() > 1:
							utils.killAndFragmentCiv(iCiv, False, True)

		# Absinthe: another instance of cities revolting, but only in case of very bad stability
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iNumPlayers):
			iPlayer = (j + iRndnum) % iNumPlayers
			pPlayer = gc.getPlayer(iPlayer)
			iRespawnTurn = utils.getLastRespawnTurn( iPlayer )
			if pPlayer.isAlive() and iGameTurn >= con.tBirth[iPlayer] + 20 and iGameTurn >= iRespawnTurn + 10:
				iStability = pPlayer.getStability()
				if pPlayer.getStability() < -15 and not utils.collapseImmune(iPlayer) and pPlayer.getNumCities() > 10: #civil war
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
			if pCiv.isAlive():
				lNumCitiesLastTime[iCiv] = self.getNumCities(iCiv)
				iNumCitiesCurrently = pCiv.getNumCities()
				self.setNumCities(iCiv, iNumCitiesCurrently)
				# Absinthe: no generic collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
				iRespawnTurn = utils.getLastRespawnTurn( iCiv )
				if iGameTurn >= con.tBirth[iCiv] + 20 and iGameTurn >= iRespawnTurn + 10 and not utils.collapseImmune(iCiv):
					# Absinthe: pass for small civs, we have bad stability collapses and collapseMotherland anyway, which is better suited for the collapse of those
					if lNumCitiesLastTime[iCiv] > 2 and iNumCitiesCurrently * 2 <= lNumCitiesLastTime[iCiv]:
						print ("COLLAPSE GENERIC", pCiv.getCivilizationAdjective(0), iNumCitiesCurrently * 2, "<=", lNumCitiesLastTime[iCiv])
						if not pCiv.isHuman():
							utils.killAndFragmentCiv(iCiv, False, False)
						elif pCiv.getNumCities() > 1:
							utils.killAndFragmentCiv(iCiv, False, True)


	def collapseMotherland(self, iGameTurn):
		# Absinthe: collapses if completely pushed out of the core area and also doesn't have enough presence in the normal area
		for iCiv in range(iNumPlayers):
			pCiv = gc.getPlayer(iCiv)
			teamCiv = gc.getTeam(pCiv.getTeam())
			if pCiv.isAlive():
				# Absinthe: no motherland collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
				iRespawnTurn = utils.getLastRespawnTurn( iCiv )
				if iGameTurn >= con.tBirth[iCiv] + 20 and iGameTurn >= iRespawnTurn + 10 and not utils.collapseImmune(iCiv):
					# Absinthe: respawned Cordoba or Aragon shouldn't collapse because not holding the original core area
					if iCiv in [con.iCordoba, con.iAragon] and pCiv.getRespawnedAlive():
						continue
					if not gc.safeMotherland( iCiv ):
						print ("COLLAPSE MOTHERLAND", gc.getPlayer(iCiv).getCivilizationAdjective(0))
						if not pCiv.isHuman():
							utils.killAndFragmentCiv(iCiv, False, False)
						elif pCiv.getNumCities() > 1:
							utils.killAndFragmentCiv(iCiv, False, True)


	def secession(self, iGameTurn):
		# Absinthe: if stability is negative there is a chance for a random city to declare it's independence, checked every 3 turns
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iNumPlayers):
			iPlayer = (j + iRndnum) % iNumPlayers
			pPlayer = gc.getPlayer(iPlayer)
			# Absinthe: no city secession for 15 turns after spawn, for 10 turns after respawn
			iRespawnTurn = utils.getLastRespawnTurn( iPlayer )
			if pPlayer.isAlive() and iGameTurn >= con.tBirth[iPlayer] + 15 and iGameTurn >= iRespawnTurn + 10:
				iStability = pPlayer.getStability()
				if gc.getGame().getSorenRandNum(10, 'do the check for city secession') < -iStability: # x/10 chance with -x stability
					self.revoltCity( iPlayer, False )
					return # max 1 secession per turn


	def revoltCity( self, iPlayer, bForce ):
		pPlayer = gc.getPlayer(iPlayer)
		iStability = pPlayer.getStability()

		cityList = []
		for city in utils.getCityList(iPlayer):
			tCity = (city.getX(), city.getY())
			x, y = tCity
			pCurrent = gc.getMap().plot(city.getX(), city.getY())

			# Absinthe: cities with We Love The King Day, your current and original capitals, and cities very close to your current capital won't revolt
			if not city.isWeLoveTheKingDay() and not city.isCapital() and tCity != tCapitals[iPlayer]:
				if pPlayer.getNumCities() > 0: # this check is needed, otherwise game crashes
					capital = gc.getPlayer(iPlayer).getCapitalCity()
					iDistance = utils.calculateDistance(x, y, capital.getX(), capital.getY())
					if iDistance > 3:
						bCollapseImmuneCity = utils.collapseImmuneCity(iPlayer, x, y)
						iProvType = pPlayer.getProvinceType( city.getProvince() )
						# Absinthe: if forced revolt, all cities go into the list by default
						#			angry population, bad health, untolerated religion, no military garrison can add the city to the list a couple more times (per type)
						#			if the city is in a contested province, the city is added a couple more times by default, if in a foreign province, a lot more times
						if bForce:
							cityList.append(city)
						# Absinthe: Byzantine UP: cities in normal and core provinces won't go on the list
						if city.angryPopulation(0) > 0:
							# Absinthe: bigger chance to choose the city if unhappy
							if not bCollapseImmuneCity:
								for i in range(2):
									cityList.append(city)
							elif iProvType < con.iProvincePotential:
								for i in range(4):
									cityList.append(city)
						if city.goodHealth() - city.badHealth(False) < -1:
							# Absinthe: health issues do not cause city secession in core provinces for anyone
							#			also less chance from unhealth for cities in contested and foreign provinces
							if iProvType < con.iProvincePotential:
								cityList.append(city)
						if city.getReligionBadHappiness() < 0:
							# Absinthe: also not a cause for secession in core provinces, no need to punish the player this much (and especially the AI) for using the civic
							if iProvType < con.iProvincePotential:
								for i in range(2):
									cityList.append(city)
						if city.getNoMilitaryPercentAnger() > 0:
							if not bCollapseImmuneCity:
								cityList.append(city)
							elif iProvType < con.iProvincePotential:
								for i in range(2):
									cityList.append(city)
						# Absinthe: also add the city if it has less than 30% own culture (and the civ doesn't have the Cultural Tolerance UP)
						if city.countTotalCultureTimes100() > 0 and (city.getCulture(iPlayer) * 10000 / city.countTotalCultureTimes100()) < 30 and not gc.hasUP( iPlayer, con.iUP_CulturalTolerance ):
							if not bCollapseImmuneCity:
								for i in range(2):
									cityList.append(city)
							elif iProvType < con.iProvincePotential:
								for i in range(3):
									cityList.append(city)
						if iProvType == con.iProvinceOuter:
							for i in range(2):
								cityList.append(city)
						elif iProvType == con.iProvinceNone:
							for i in range(7):
								cityList.append(city)

		if cityList:
			# Absinthe: city goes to random independent
			iRndNum = gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random independent')
			iNewCiv = con.iIndepStart + iRndNum

			# Absinthe: choosing one city from the list (where each city can appear multiple times)
			splittingCity = utils.getRandomEntry(cityList)
			tCity = (splittingCity.getX(), splittingCity.getY())
			sCityName = splittingCity.getName()
			if iPlayer == utils.getHumanID():
				CyInterface().addMessage(iPlayer, True, con.iDuration, sCityName + " " + CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
			utils.cultureManager(tCity, 50, iNewCiv, iPlayer, False, True, True)
			utils.flipUnitsInCitySecession(tCity, iNewCiv, iPlayer)
			self.setTempFlippingCity(tCity)
			utils.flipCity(tCity, 0, 0, iNewCiv, [iPlayer]) #by trade because by conquest may raze the city
			utils.flipUnitsInCityAfter(tCity, iNewCiv)

			print ("SECESSION", gc.getPlayer(iPlayer).getCivilizationAdjective(0), sCityName, "Stability:", iStability)
			# Absinthe: loosing a city to secession/revolt gives a small boost to stability, to avoid a city-revolting chain reaction
			pPlayer.changeStabilityBase( con.iCathegoryExpansion, 2 )
			# Absinthe: AI declares war on the indy city right away
			teamPlayer = gc.getTeam( pPlayer.getTeam() )
			teamPlayer.declareWar(iNewCiv, False, WarPlanTypes.WARPLAN_LIMITED)


	def resurrection(self, iGameTurn, iDeadCiv):
		if iDeadCiv == -1:
			iDeadCiv = self.findCivToResurect(iGameTurn , 0, -1)
		else:
			iDeadCiv = self.findCivToResurect(iGameTurn , 1, iDeadCiv) #For special re-spawn
		#print ("iDeadCiv", iDeadCiv)
		if iDeadCiv > -1:
			self.suppressResurection( iDeadCiv )
			#self.resurectCiv( iDeadCiv )


	def findCivToResurect( self, iGameTurn , bSpecialRespawn, iDeadCiv):
		#print("Looking up a civ to resurrect, iDeadCiv: ",iDeadCiv)
		if bSpecialRespawn:
			iMinNumCities = 1
		else:
			iMinNumCities = 2

		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iNumPlayers):
			if not bSpecialRespawn:
				iDeadCiv = (j + iRndnum) % iNumPlayers
			else:
				iDeadCiv = iDeadCiv #We want a specific civ for special re-spawn
			cityList = []
			if not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > con.tBirth[iDeadCiv] + 25 and iGameTurn > utils.getLastTurnAlive(iDeadCiv) + 10: #Sedna17: Allow re-spawns only 10 turns after death and 25 turns after birth
				pDeadCiv = gc.getPlayer(iDeadCiv)
				teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
				tTopLeft = tNormalAreasTL[iDeadCiv]
				tBottomRight = tNormalAreasBR[iDeadCiv]

				for tPlot in utils.getPlotList(tTopLeft, tBottomRight):
					x, y = tPlot
					if tPlot in con.tNormalAreasSubtract[iDeadCiv]: continue
					#if ((x,y) not in con.lExtraPlots[iDeadCiv]):
					plot = gc.getMap().plot( x, y )
					if plot.isCity():
						city = plot.getPlotCity()
						print("Considering city at: (x,y) ",x,y)
						iOwner = city.getOwner()
						if iOwner >= iNumActivePlayers: #if (iOwner == iBarbarian or iOwner == iIndependent or iOwner == iIndependent2): #remove in vanilla
							cityList.append(tPlot)
							#print (iDeadCiv, plot.getPlotCity().getName(), plot.getPlotCity().getOwner(), "1", cityList)
						else:
							iMinNumCitiesOwner = 3
							#iOwnerStability = utils.getStability(iOwner)
							iOwnerStability = gc.getPlayer(iOwner).getStability()
							if not gc.getPlayer(iOwner).isHuman():
								iMinNumCitiesOwner = 2
								iOwnerStability -= 5
							if gc.getPlayer(iOwner).getNumCities() >= iMinNumCitiesOwner:
								if iOwnerStability < -5:
									if not city.isWeLoveTheKingDay() and not city.isCapital():
										cityList.append(tPlot)
										#print (iDeadCiv, plot.getPlotCity().getName(), plot.getPlotCity().getOwner(), "2", cityList)
								elif iOwnerStability < 0:
									if not city.isWeLoveTheKingDay() and not city.isCapital() and tPlot != tCapitals[iOwner]:
										if gc.getPlayer(iOwner).getNumCities() > 0: #this check is needed, otherwise game crashes
											capital = gc.getPlayer(iOwner).getCapitalCity()
											iDistance = utils.calculateDistance(x, y, capital.getX(), capital.getY())
											if (iDistance >= 6 and gc.getPlayer(iOwner).getNumCities() >= 4) or \
												city.angryPopulation(0) > 0 or \
												city.goodHealth() - city.badHealth(False) < -1 or \
												city.getReligionBadHappiness() < 0 or \
												city.getLargestCityHappiness() < 0 or \
												city.getHurryAngerModifier() > 0 or \
												city.getNoMilitaryPercentAnger() > 0:
													cityList.append(tPlot)
													#print (iDeadCiv, plot.getPlotCity().getName(), plot.getPlotCity().getOwner(), "3", cityList)
								if not bSpecialRespawn and iOwnerStability < 10:
									if tPlot == tCapitals[iDeadCiv]:
										if tPlot not in cityList:
											cityList.append(tPlot)
				if len(cityList) >= iMinNumCities:
					if bSpecialRespawn or (gc.getGame().getSorenRandNum(100, 'roll') < con.tResurrectionProb[iDeadCiv]): #If special, always happens
						self.setRebelCities( cityList )
						self.setRebelCiv(iDeadCiv) #for popup and CollapseCapitals()
						return iDeadCiv
		return -1


	def suppressResurection( self, iDeadCiv ):
		lSuppressList = self.getRebelSuppress()
		#print ("lSuppressList for iCiv", lSuppressList)
		lCityList = self.getRebelCities()
		lCityCount = [-1] * iNumPlayers #major players only

		for (x, y) in lCityList:
			iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
			if iOwner < iNumMajorPlayers:
				lCityCount[iOwner] += 1

		iHuman = utils.getHumanID()
		for iCiv in range( iNumMajorPlayers ):
			if lCityCount[iCiv] > 0:
				if iCiv != iHuman:
					# Absinthe: for the AI there is 30% chance that the actual respawn does not happen (under these suppress situations), only some revolt in the corresponding cities
					iActualSpawnChance = gc.getGame().getSorenRandNum(100, 'odds')
					print ("iActualSpawnChance", iActualSpawnChance)
					if iActualSpawnChance > 70:
						lSuppressList[iCiv] = 1
						for (x, y) in lCityList:
							pCity = gc.getMap().plot(x, y).getPlotCity()
							if pCity.getOwner() == iCiv:
								pCity.changeOccupationTimer( 1 )
								pCity.changeHurryAngerTimer( 10 )
					else:
						lSuppressList[iCiv] = 0

		self.setRebelSuppress( lSuppressList )

		# Possible issue here for AI civs - do we always "resurrect" the new civ, even without any cities actually selected for resurrection?
		if lCityCount[iHuman] > 0:
			self.rebellionPopup( iDeadCiv, lCityCount[iHuman] )
		else:
			self.resurectCiv( iDeadCiv )


	def resurectCiv( self, iDeadCiv ):

		lCityList = self.getRebelCities()
		lSuppressList = self.getRebelSuppress()
		bSuppressed = True
		iHuman = utils.getHumanID()

		# Absinthe: if any of the AI civs didn't manage to suppress it, there is resurrection
		for iCiv in range( iNumMajorPlayers ):
			if iCiv != iHuman and lSuppressList[iCiv] == 0:
				bSuppressed = False
		# Absinthe: if the human player didn't choose any suppress options (so it has 0, 2 or 4 in the lSuppressList), there is resurrection
		if lSuppressList[iHuman] in [0, 2, 4]:
			bSuppressed = False
		# Absinthe: if neither of the above happened, so everyone managed to suppress it, no resurrection
		if bSuppressed:
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

		# Absinthe: we shouldn't get a previous leader on respawn - would be changed to a newer one in a couple turns anyway
		#			instead we have a random chance to remain with the leader before the collapse, or to switch to the next one
		tLeaderCiv = tLeaders[iDeadCiv]
		if len(tLeaderCiv) > 1:
			for iLeader in range(len(tLeaderCiv)-1): # no change if we are already at the last leader
				if pDeadCiv.getLeader() == tLeaderCiv[iLeader]:
					iRnd = gc.getGame().getSorenRandNum(5, 'odds')
					if iRnd > 1: # 60 chance for the next leader
						print ("leader switch after resurrection", pDeadCiv.getLeader(), tLeaderCiv[iLeader])
						pDeadCiv.setLeader(tLeaderCiv[iLeader])
					break
		# Absinthe: old code for leader-change on respawn
		#if (len(tLeaders[iDeadCiv]) > 1):
		#	iLen = len(tLeaders[iDeadCiv])
		#	iRnd = gc.getGame().getSorenRandNum(iLen, 'odds')
		#	for k in range(iLen):
		#		iLeader = (iRnd + k) % iLen
		#		if (pDeadCiv.getLeader() != tLeaders[iDeadCiv][iLeader]):
		#			print ("leader switch after resurrection", pDeadCiv.getLeader(), tLeaders[iDeadCiv][iLeader])
		#			pDeadCiv.setLeader(tLeaders[iDeadCiv][iLeader])
		#			break

		for iCiv in range(iNumPlayers):
			if iCiv != iDeadCiv:
				teamDeadCiv.makePeace(iCiv)
		self.setNumCities(iDeadCiv, 0) #reset collapse condition

		# Absinthe: reset vassalage and update dynamic civ names
		for iOtherCiv in range(iNumPlayers):
			if iOtherCiv != iDeadCiv:
				if teamDeadCiv.isVassal(iOtherCiv) or gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).isVassal(iDeadCiv):
					print ("vassalage reset on resurrection", iDeadCiv, iOtherCiv)
					teamDeadCiv.freeVassal(iOtherCiv)
					gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).freeVassal(iDeadCiv)
					gc.getPlayer(iOtherCiv).processCivNames()
					gc.getPlayer(iDeadCiv).processCivNames()

		# Absinthe: no vassalization in the first 10 turns after resurrection?

		iNewUnits = 2
		if self.getLatestRebellionTurn(iDeadCiv) > 0:
			iNewUnits = 4
		self.setLatestRebellionTurn(iDeadCiv, gc.getGame().getGameTurn() )

		print ("RESURRECTION", gc.getPlayer(iDeadCiv).getCivilizationAdjective(0))

		bHuman = False
		for (x, y) in lCityList:
			if gc.getMap().plot(x, y).getPlotCity().getOwner() == iHuman:
				bHuman = True
				break

		ownersList = []
		bAlreadyVassal = False
		for tCity in lCityList:
			#print ("INDEPENDENCE: ", cityList[k].getName()) #may cause a c++ exception
			pCity = gc.getMap().plot( tCity[0], tCity[1] ).getPlotCity()
			iOwner = pCity.getOwner()
			teamOwner = gc.getTeam(gc.getPlayer(iOwner).getTeam())
			bOwnerVassal = teamOwner.isAVassal()
			bOwnerHumanVassal = teamOwner.isVassal(iHuman)

			if iOwner >= iNumPlayers:
				utils.cultureManager(tCity, 100, iDeadCiv, iOwner, False, True, True)
				utils.flipUnitsInCityBefore(tCity, iDeadCiv, iOwner)
				self.setTempFlippingCity(tCity)
				utils.flipCity(tCity, 0, 0, iDeadCiv, [iOwner])
				utils.flipUnitsInCityAfter(tCity, iOwner)
				utils.flipUnitsInArea((tCity[0]-2, tCity[1]-2), (tCity[0]+2, tCity[1]+2), iDeadCiv, iOwner, True, False)
			else:
				print ("iOwner lSuppressList iDeadCiv", iOwner, lSuppressList[iOwner], iDeadCiv)
				if lSuppressList[iOwner] in [0, 2, 4]:
					utils.cultureManager(tCity, 50, iDeadCiv, iOwner, False, True, True)
					utils.pushOutGarrisons(tCity, iOwner)
					utils.relocateSeaGarrisons(tCity, iOwner)
					self.setTempFlippingCity(tCity)
					utils.flipCity(tCity, 0, 0, iDeadCiv, [iOwner]) #by trade because by conquest may raze the city
					utils.createGarrisons(tCity, iDeadCiv, iNewUnits)

			#cityList[k].setHasRealBuilding(con.iPlague, False)

				# 3Miro: indent to make part of the else on the if statement, otherwise one can make peace with the Barbs
				bAtWar = False #AI won't vassalise if another owner has declared war; on the other hand, it won't declare war if another one has vassalised
				if iOwner != iHuman and iOwner not in ownersList and iOwner != iDeadCiv and lSuppressList[iOwner] == 0: #declare war or peace only once - the 3rd condition is obvious but "vassal of themselves" was happening
					rndNum = gc.getGame().getSorenRandNum(100, 'odds')
					if rndNum >= tAIStopBirthThreshold[iOwner] and not bOwnerHumanVassal and not bAlreadyVassal: #if bOwnerHumanVassal is true, it will skip to the 3rd condition, as bOwnerVassal is true as well
						teamOwner.declareWar(iDeadCiv, False, -1)
						bAtWar = True
					# Absinthe: do we really want to auto-vassal them on respawn? why?
					#			set it to 0 from 60 temporarily (so it's never true), as a quick fix until the mechanics are revised
					elif (rndNum <= 0 - (tAIStopBirthThreshold[iOwner]/2)):
						teamOwner.makePeace(iDeadCiv)
						if not bAlreadyVassal and not bHuman and not bOwnerVassal and not bAtWar: #bHuman == False cos otherwise human player can be deceived to declare war without knowing the new master
							gc.getTeam(gc.getPlayer(iDeadCiv).getTeam()).setVassal(iOwner, True, False)
							gc.getPlayer(iOwner).processCivNames() # setVassal already updates DCN for iDeadCiv
							bAlreadyVassal = True
					else:
						teamOwner.makePeace(iDeadCiv)
					ownersList.append(iOwner)
					for iTech in range(xml.iNumTechs):
						if teamOwner.isHasTech(iTech):
							teamDeadCiv.setHasTech(iTech, True, iDeadCiv, False, False)

		# all techs added from minor civs
		for iTech in range(xml.iNumTechs):
			if teamBarbarian.isHasTech(iTech) or teamIndependent.isHasTech(iTech) or teamIndependent2.isHasTech(iTech) or teamIndependent3.isHasTech(iTech) or teamIndependent4.isHasTech(iTech):
				teamDeadCiv.setHasTech(iTech, True, iDeadCiv, False, False)

		self.moveBackCapital(iDeadCiv)

		#add former colonies that are still free
		# 3Miro: no need, we don't have "colonies", this causes trouble with Cordoba's special respawn, getting cities back from Iberia
		#colonyList = []
		#for iIndCiv in range(iNumActivePlayers, iNumTotalPlayersB): #barbarians too
		#	if gc.getPlayer(iIndCiv).isAlive():
		#		for indepCity in utils.getCityList(iIndCiv):
		#			if indepCity.getOriginalOwner() == iDeadCiv:
		#				print ("colony:", indepCity.getName(), indepCity.getOriginalOwner())
		#				indX = indepCity.getX()
		#				indY = indepCity.getY()
		#				tCitySpot = ( indX, indY );
		#				if gc.getPlayer(iDeadCiv).getSettlersMaps( con.iMapMaxY-indY-1, indX ) >= 90:
		#					if tCitySpot not in lCityList and indepCity not in colonyList:
		#						colonyList.append(indepCity)
		#if colonyList:
		#	for colony in colonyList:
		#		print ("INDEPENDENCE: ", colony.getName())
		#		iOwner = colony.getOwner()
		#		tColony = (colony.getX(), colony.getY())
		#		utils.cultureManager(tColony, 100, iDeadCiv, iOwner, False, True, True)
		#		utils.flipUnitsInCityBefore(tColony, iDeadCiv, iOwner)
		#		self.setTempFlippingCity(tColony)
		#		utils.flipCity(tColony, 0, 0, iDeadCiv, [iOwner])
		#		utils.flipUnitsInArea((tColony[0]-2, tColony[1]-2), (tColony[0]+2, tColony[1]+2), iDeadCiv, iOwner, True, False)

		if utils.isActive(iHuman):
			CyInterface().addMessage(iHuman, True, con.iDuration, (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pDeadCiv.getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(con.iDarkPink), -1, -1, True, True)
		#if (bHuman == True):
		#	self.rebellionPopup(iDeadCiv)
		if lSuppressList[iHuman] in [2, 3, 4]:
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
		cityList = utils.getCityList(iCiv)
		for tPlot in tNewCapitals[iCiv]:
			plot = gc.getMap().plot( tPlot[0], tPlot[1] )
			if plot.isCity():
				newCapital = plot.getPlotCity()
				if newCapital.getOwner() == iCiv:
					if not newCapital.hasBuilding(xml.iPalace):
						for city in cityList:
							city.setHasRealBuilding((xml.iPalace), False)
						newCapital.setHasRealBuilding((xml.iPalace), True)
						self.makeResurectionUnits( iCiv, newCapital.getX(), newCapital.getY() )
		else:
			iMaxValue = 0
			bestCity = None
			for loopCity in cityList:
				#loopCity.AI_cityValue() doesn't work as area AI types aren't updated yet
				loopValue = max(0, 500-loopCity.getGameTurnFounded()) + loopCity.getPopulation()*10
				#print ("loopValue", loopCity.getName(), loopCity.AI_cityValue(), loopValue) #causes C++ exception
				if loopValue > iMaxValue:
					iMaxValue = loopValue
					bestCity = loopCity
			if bestCity != None:
				for loopCity in cityList:
					if loopCity != bestCity:
						loopCity.setHasRealBuilding((xml.iPalace), False)
				bestCity.setHasRealBuilding((xml.iPalace), True)
				self.makeResurectionUnits( iCiv, bestCity.getX(), bestCity.getY() )


	def makeResurectionUnits( self, iPlayer, iX, iY ):
		if iPlayer == iCordoba:
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
		for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
			pCurrent = gc.getMap().plot( x, y )
			if pCurrent.isCity():
				for (ix, iy) in utils.surroundingPlots((x, y)):
					pCityArea = gc.getMap().plot( ix, iy )
					iCivCulture = pCityArea.getCulture(iCiv)
					iLoopCivCulture = 0
					for iLoopCiv in range(iNumPlayers, iNumTotalPlayersB): #barbarians too
						iLoopCivCulture += pCityArea.getCulture(iLoopCiv)
						pCityArea.setCulture(iLoopCiv, 0, True)
					pCityArea.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

				city = pCurrent.getPlotCity()
				iCivCulture = city.getCulture(iCiv)
				iLoopCivCulture = 0
				for iLoopCiv in range(iNumPlayers, iNumTotalPlayersB): #barbarians too
					iLoopCivCulture += city.getCulture(iLoopCiv)
					city.setCulture(iLoopCiv, 0, True)
				city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

	def initBirth(self, iCurrentTurn, iBirthYear, iCiv):
		iHuman = utils.getHumanID()
		#print("iBirthYear:%d, iCurrentTurn:%d" %(iBirthYear, iCurrentTurn))
		#print("getSpawnDelay:%d, getFlipsDelay:%d" %(self.getSpawnDelay(iCiv), self.getFlipsDelay(iCiv)))
		if iCurrentTurn == iBirthYear-1 + self.getSpawnDelay(iCiv) + self.getFlipsDelay(iCiv):
			tCapital = tCapitals[iCiv]
			tTopLeft = tCoreAreasTL[iCiv]
			tBottomRight = tCoreAreasBR[iCiv]
			tBroaderTopLeft = tBroaderAreasTL[iCiv]
			tBroaderBottomRight = tBroaderAreasBR[iCiv]
			if self.getFlipsDelay(iCiv) == 0: #city hasn't already been founded)

				# Absinthe: this probably fixes a couple instances of the -1 turn autoplay bug - code adapted from SoI
				if iCiv == iHuman:
					killPlot = gc.getMap().plot(tCapital[0], tCapital[1])
					iNumUnitsInAPlot = killPlot.getNumUnits()
					if iNumUnitsInAPlot > 0:
						for i in range(iNumUnitsInAPlot):
							unit = killPlot.getUnit(i)
							if unit.getOwner() != iCiv:
								unit.kill(False, iBarbarian)

				bDeleteEverything = False
				if gc.getMap().plot(tCapital[0], tCapital[1]).isOwned():
					if iCiv == iHuman or not gc.getPlayer(iHuman).isAlive():
						bDeleteEverything = True
						print ("bDeleteEverything 1")
					else:
						bDeleteEverything = True
						for (x, y) in utils.surroundingPlots(tCapital):
							plot = gc.getMap().plot(x, y)
							if plot.isCity() and plot.getPlotCity().getOwner() == iHuman:
								bDeleteEverything = False
								print ("bDeleteEverything 2")
								break
				print ("bDeleteEverything", bDeleteEverything)
				if not gc.getMap().plot(tCapital[0], tCapital[1]).isOwned():
					#if (iCiv == iNetherlands or iCiv == iPortugal): #dangerous starts
					#	self.setDeleteMode(0, iCiv)
					self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				elif bDeleteEverything:
					for (x, y) in utils.surroundingPlots(tCapital):
						self.setDeleteMode(0, iCiv)
						#print ("deleting", x, y)
						plot = gc.getMap().plot(x, y)
						#self.moveOutUnits(x, y, tCapital[0], tCapital[1])
						for iLoopCiv in range(iNumTotalPlayersB): #Barbarians as well
							if iCiv != iLoopCiv:
								utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iLoopCiv, True, False)
								utils.flipUnitsInPlots(con.lExtraPlots[iCiv], iCiv, iLoopCiv, True, False)
						if plot.isCity():
							plot.eraseAIDevelopment() #new function, similar to erase but won't delete rivers, resources and features
						for iLoopCiv in range(iNumTotalPlayersB): #Barbarians as well
							if iCiv != iLoopCiv:
								plot.setCulture(iLoopCiv, 0, True)
						#pCurrent.setCulture(iCiv,10,True)
						plot.setOwner(-1)
					self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				else:
					self.birthInForeignBorders(iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight, tCapital)
			else:
				print ( "setBirthType again: flips" )
				self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)

		# 3MiroCrusader modification. Crusaders cannot change nations.
		# Sedna17: Straight-up no switching within 40 turns of your birth
		if iCurrentTurn == iBirthYear + self.getSpawnDelay(iCiv):
			if gc.getPlayer(iCiv).isAlive() and not self.getAlreadySwitched() and iCurrentTurn > con.tBirth[iHuman] + 40 and not gc.getPlayer( iHuman ).getIsCrusader():
				self.newCivPopup(iCiv)


##	def moveOutUnits(self, x, y, tCapitalX, tCapitalY) #not used
##		pCurrent=gc.getMap().plot(x, y)
##		if pCurrent.getNumUnits() > 0:
##			unit = pCurrent.getUnit(0)
##			tDestination = (-1, -1)
##			plotList = []
##			if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
##				plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodPlots, [] )
##				#plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodOwnedPlots, [] )
##			else: #sea unit
##				plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodOwnedPlots, [] )
##
##			if plotList:
##				tPlot = utils.getRandomEntry(plotList)
##			print ("moving units around to", (tPlot[0], tPlot[1]))
##			if tPlot != (-1, -1):
##				for i in range(pCurrent.getNumUnits()):
##					unit = pCurrent.getUnit(0)
##					unit.setXY(tPlot[0], tPlot[1])


	def deleteMode(self, iCurrentPlayer):
		iCiv = self.getDeleteMode(0)
		print ("deleteMode after", iCurrentPlayer)
		tCapital = con.tCapitals[iCiv]
		if iCurrentPlayer == iCiv:
			for (x, y) in utils.surroundingPlots(tCapital, 2):
				plot = gc.getMap().plot(x, y)
				plot.setCulture(iCiv, 300, True)
			for (x, y) in utils.surroundingPlots(tCapital):
				plot = gc.getMap().plot(x, y)
				utils.convertPlotCulture(plot, iCiv, 100, True)
				if plot.getCulture(iCiv) < 3000:
					plot.setCulture(iCiv, 3000, True) #2000 in vanilla/warlords, cos here Portugal is choked by Spanish culture
				plot.setOwner(iCiv)
			self.setDeleteMode(0, -1)
			return

		#print ("iCurrentPlayer", iCurrentPlayer, "iCiv", iCiv)
		if iCurrentPlayer != iCiv-1:
			return

		for (x, y) in utils.surroundingPlots(tCapital):
			#print ("deleting again", x, y)
			plot = gc.getMap().plot(x, y)
			if plot.isOwned():
				for iLoopCiv in range(iNumTotalPlayersB): #Barbarians as well
					if iLoopCiv != iCiv:
						plot.setCulture(iLoopCiv, 0, True)
					#else:
					#	if plot.getCulture(iCiv) < 4000:
					#		plot.setCulture(iCiv, 4000, True)
				#plot.setOwner(-1)
				plot.setOwner(iCiv)

		# Absinthe: what's this +-11?
		for (x, y) in utils.surroundingPlots(tCapital, 11): # must include the distance from Sogut to the Caspius
			#print ("units", x, y, gc.getMap().plot(x, y).getNumUnits(), tCapital[0], tCapital[1])
			if tCapital != (x, y):
				plot = gc.getMap().plot(x, y)
				if plot.getNumUnits() > 0 and not plot.isWater():
					unit = plot.getUnit(0)
					#print ("units2", x, y, plot.getNumUnits(), unit.getOwner(), iCiv)
					if unit.getOwner() == iCiv:
						print ("moving starting units from", x, y, "to", (tCapital[0], tCapital[1]))
						for i in range(plot.getNumUnits()):
							unit = plot.getUnit(0)
							unit.setXYOld(tCapital[0], tCapital[1])
						#may intersect plot close to tCapital
##							for (i, j) in utils.surroundingPlots((x, y), 6):
##								pCurrentFar = gc.getMap().plot(i, j)
##								if pCurrentFar.getNumUnits() == 0:
##									pCurrentFar.setRevealed(iCiv, False, True, -1);


	def birthInFreeRegion(self, iCiv, tCapital, tTopLeft, tBottomRight):
		startingPlot = gc.getMap().plot( tCapital[0], tCapital[1] )
		if self.getFlipsDelay(iCiv) == 0:
			iFlipsDelay = self.getFlipsDelay(iCiv) + 2
			print ("Entering birthInFreeRegion")
##			if startingPlot.getNumUnits() > 0:
##				unit = startingPlot.getUnit(0)
##				if unit.getOwner() != utils.getHumanID() or iCiv == utils.getHumanID(): #2nd check needed because in delete mode it finds the civ's (human's) units placed
##					for i in range(startingPlot.getNumUnits()):
##						unit = startingPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
##						unit.kill(False, iCiv)
##					iFlipsDelay = self.getFlipsDelay(iCiv) + 2
##					#utils.debugTextPopup( 'birthInFreeRegion in starting location' )
##				else: #search another place
##					plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.goodPlots, [] )
##					if plotList:
##						tPlot = utils.getRandomEntry(plotList)
##						self.createStartingUnits(iCiv, tPlot)
##						tCapital = tPlot
##						print ("birthInFreeRegion in another location")
##						#utils.debugTextPopup( 'birthInFreeRegion in another location' )
##						iFlipsDelay = self.getFlipsDelay(iCiv) + 1 #add delay before flipping other cities
##					else:
##						if self.getSpawnDelay(iCiv) < 10: #wait
##							iSpawnDelay = self.getSpawnDelay(iCiv) + 1
##							self.setSpawnDelay(iCiv, iSpawnDelay)
##			else:
##				iFlipsDelay = self.getFlipsDelay(iCiv) + 2

			if iFlipsDelay > 0:
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
##					if unit.getUnitType() == xml.iSettler:
##						break
##				unit.found()

				# Absinthe: there was another silly mistake here with barbarian and indy unit flips... 
				#			we don't simply want to check an area based on distance from capital, as it might lead out from the actual spawn area
				#			so we check plots which are in the core area, and in 4 distance for barb units, 2 distance for indies
				lPlotBarbFlip = []
				lPlotIndyFlip = []
				# if inside the core rectangle and extra plots, and in 4 (barb) or 2 (indy) distance from the starting plot, append to barb or indy flip zone
				lPlots = utils.getPlotList(tTopLeft, tBottomRight) + lExtraPlots[iCiv]
				lSurroundingPlots4 = utils.surroundingPlots(tCapital, 4)
				lSurroundingPlots2 = utils.surroundingPlots(tCapital, 2)
				for tPlot in lPlots:
					if tPlot in lSurroundingPlots2:
						lPlotIndyFlip.append(tPlot)
						lPlotBarbFlip.append(tPlot)
					elif tPlot in lSurroundingPlots4:
						lPlotBarbFlip.append(tPlot)
				utils.flipUnitsInPlots(lPlotBarbFlip, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ
				for iIndyCiv in range( con.iIndepStart, con.iIndepEnd + 1 ):
					utils.flipUnitsInPlots(lPlotIndyFlip, iCiv, iIndyCiv, True, False) #remaining independents in the region now belong to the new civ
				self.assignTechs(iCiv)
				utils.setPlagueCountdown(iCiv, -con.iImmunity)
				utils.clearPlague(iCiv)
				self.setFlipsDelay(iCiv, iFlipsDelay) #save


		else: #starting units have already been placed, now the second part
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, tTopLeft, tBottomRight)
			self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			utils.flipUnitsInPlots(lExtraPlots[iCiv], iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			for iIndyCiv in range( con.iIndepStart, con.iIndepEnd + 1 ):
				utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndyCiv, False, False) #remaining independents in the region now belong to the new civ
				utils.flipUnitsInPlots(lExtraPlots[iCiv], iCiv, iIndyCiv, False, False) #remaining independents in the region now belong to the new civ
			print ("utils.flipUnitsInArea()")
			#cover plots revealed by the catapult
			plotZero = gc.getMap().plot( 32, 0 ) #sync with rfcebalance module
			if (plotZero.getNumUnits()):
				catapult = plotZero.getUnit(0)
				catapult.kill(False, iCiv)
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


	def birthInForeignBorders(self, iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight, tCapital):

		print( " 3Miro: Birth in Foreign Land: ",iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight, tCapital)
		iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, tTopLeft, tBottomRight)
		self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)

		print ("iNumAICitiesConverted", iNumAICitiesConverted)
		print ("iNumHumanCitiesToConvert", iNumHumanCitiesToConvert)

		#now starting units must be placed
		if iNumAICitiesConverted > 0:
			#utils.debugTextPopup( 'iConverted OK for placing units' )
			# Absinthe: there is an issue that core area are not calculated correctly for flips, as the additional tiles in lExtraPlots are not checked here
			#			so if all flipped cities are outside of the core area (they are in the "exceptions"), the civ will start without it's starting units and techs
			print ("tTopLeft, tBottomRight", tTopLeft, tBottomRight)
			plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iCiv )
			print ("plotList", plotList)
			# Absinthe: add the exception plots
			for tPlot in lExtraPlots[iCiv]:
				plot = gc.getMap().plot( tPlot[0], tPlot[1] )
				if plot.getOwner() == iCiv:
					if plot.isCity():
						plotList.append(tPlot)
			print ("plotList", plotList)
			if plotList:
				tPlot = utils.getRandomEntry(plotList)
				self.createStartingUnits(iCiv, tPlot)
				#utils.debugTextPopup( 'birthInForeignBorders after a flip' )
				self.assignTechs(iCiv)
				utils.setPlagueCountdown(iCiv, -con.iImmunity)
				utils.clearPlague(iCiv)
				#gc.getPlayer(iCiv).changeAnarchyTurns(1)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			utils.flipUnitsInPlots(con.lExtraPlots[iCiv], iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			for iIndyCiv in range( con.iIndepStart, con.iIndepEnd + 1 ):
				utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndyCiv, False, False) #remaining independents in the region now belong to the new civ
				utils.flipUnitsInPlots(con.lExtraPlots[iCiv], iCiv, iIndyCiv, False, False) #remaining independents in the region now belong to the new civ

		else: #search another place
			# Absinthe: there is an issue that core area are not calculated correctly for flips, as the additional tiles in lExtraPlots are not checked here
			#			so if all flipped cities are outside of the core area (they are in the "exceptions"), the civ will start without it's starting units and techs
			plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.goodPlots, [] )
			# Absinthe: add the exception plots
			for tPlot in lExtraPlots[iCiv]:
				plot = gc.getMap().plot( tPlot[0], tPlot[1] )
				if (plot.isHills() or plot.isFlatlands()) and not plot.isImpassable():
					if not plot.isUnit():
						if plot.getTerrainType() not in [xml.iTerrainDesert, xml.iTerrainTundra] and plot.getFeatureType() not in [xml.iMarsh, xml.iJungle]:
							if plot.countTotalCulture() == 0:
								plotList.append(tPlot)
			rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching another free plot')
			if plotList:
				tPlot = utils.getRandomEntry(tPlot)
				self.createStartingUnits(iCiv, tPlot)
				#utils.debugTextPopup( 'birthInForeignBorders in another location' )
				self.assignTechs(iCiv)
				utils.setPlagueCountdown(iCiv, -con.iImmunity)
				utils.clearPlague(iCiv)
			else:
				plotList = utils.squareSearch( tBroaderTopLeft, tBroaderBottomRight, utils.goodPlots, [] )
				if plotList:
					tPlot = utils.getRandomEntry(plotList)
					self.createStartingUnits(iCiv, tPlot)
					self.createStartingWorkers(iCiv, tPlot)
					#utils.debugTextPopup( 'birthInForeignBorders in a broader area' )
					self.assignTechs(iCiv)
					utils.setPlagueCountdown(iCiv, -con.iImmunity)
					utils.clearPlague(iCiv)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ
			utils.flipUnitsInPlots(con.lExtraPlots[iCiv], iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ
			for iIndyCiv in range( con.iIndepStart, con.iIndepEnd + 1 ):
				utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndyCiv, True, False) #remaining independents in the region now belong to the new civ
				utils.flipUnitsInPlots(con.lExtraPlots[iCiv], iCiv, iIndyCiv, True, False) #remaining independents in the region now belong to the new civ

		if iNumHumanCitiesToConvert> 0:
			self.flipPopup(iCiv, tTopLeft, tBottomRight)


	def convertSurroundingCities(self, iCiv, tTopLeft, tBottomRight):
		iConvertedCitiesCount = 0
		iNumHumanCities = 0
		cityList = []
		self.setSpawnWar(0)
		pCiv = gc.getPlayer(iCiv)

		#collect all the cities in the spawn region
		lPlots = utils.getPlotList(tTopLeft, tBottomRight) + lExtraPlots[iCiv]
		for (x, y) in lPlots:
			plot = gc.getMap().plot( x, y )
			if plot.isCity():
				if plot.getPlotCity().getOwner() != iCiv:
					#print ("append", x,y)
					cityList.append(plot.getPlotCity())

		print ("Birth", iCiv)
		#print (cityList)

		#for each city
		if cityList:
			for loopCity in cityList:
				loopX = loopCity.getX()
				loopY = loopCity.getY()
				#print ("cityList", loopCity.getName(), (loopX, loopY))
				iHuman = utils.getHumanID()
				iOwner = loopCity.getOwner()
				iCultureChange = 0 #if 0, no flip; if > 0, flip will occur with the value as variable for utils.CultureManager()

				if iOwner >= iNumPlayers:
					#utils.debugTextPopup( 'BARB' )
					iCultureChange = 100
				#case 2: human city
				elif iOwner == iHuman and not loopCity.isCapital():
					if iNumHumanCities == 0:
						iNumHumanCities += 1
						#self.flipPopup(iCiv, tTopLeft, tBottomRight)
				#case 3: other
				elif not loopCity.isCapital(): # 3Miro: this keeps crashing in the C++, makes no sense
				#elif ( True ): #utils.debugTextPopup( 'OTHER' )
					if iConvertedCitiesCount < 6: #there won't be more than 5 flips in the area
						#utils.debugTextPopup( 'iConvertedCities OK' )
						iCultureChange = 50
						if gc.getGame().getGameTurn() <= con.tBirth[iCiv] + 5: #if we're during a birth
							rndNum = gc.getGame().getSorenRandNum(100, 'odds')
							#3Miro: I don't know why the iOwner check is needed below, but the module crashes sometimes
							if iOwner > -1 and iOwner < iNumMajorPlayers and rndNum >= tAIStopBirthThreshold[iOwner]:
								print (iOwner, "stops birth", iCiv, "rndNum:", rndNum, "threshold:", tAIStopBirthThreshold[iOwner])
								pOwner = gc.getPlayer(iOwner)
								if not gc.getTeam(pOwner.getTeam()).isAtWar(iCiv):
									gc.getTeam(pOwner.getTeam()).declareWar(iCiv, False, -1)
									if pCiv.getNumCities() > 0: #this check is needed, otherwise game crashes
										print ("capital:", pCiv.getCapitalCity().getX(), pCiv.getCapitalCity().getY())
										if (pCiv.getCapitalCity().getX(), pCiv.getCapitalCity().getY()) != (-1, -1):
											self.createAdditionalUnits(iCiv, (pCiv.getCapitalCity().getX(), pCiv.getCapitalCity().getY()))
										else:
											self.createAdditionalUnits(iCiv, tCapitals[iCiv])


				if iCultureChange > 0:
					#print ("flipping ", cityList[i].getName())
					utils.cultureManager((loopX, loopY), iCultureChange, iCiv, iOwner, True, False, False)
					#gc.getMap().plot(cityList[i].getX(),cityList[i].getY()).setImprovementType(-1)

					utils.flipUnitsInCityBefore((loopX, loopY), iCiv, iOwner)
					self.setTempFlippingCity((loopX, loopY)) #necessary for the (688379128, 0) bug
					utils.flipCity((loopX,loopY), 0, 0, iCiv, [iOwner])
					#print ("cityList[i].getXY", cityList[i].getX(), cityList[i].getY())
					utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iCiv)

					iConvertedCitiesCount += 1
					print ("iConvertedCitiesCount", iConvertedCitiesCount)

		if iConvertedCitiesCount > 0:
			if gc.getPlayer(iCiv).isHuman():
				CyInterface().addMessage(iCiv, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_TO_US", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)

		#print( "converted cities", iConvertedCitiesCount)
		return (iConvertedCitiesCount, iNumHumanCities)


	def convertSurroundingPlotCulture(self, iCiv, tTopLeft, tBottomRight):

		lPlots = utils.getPlotList(tTopLeft, tBottomRight) + lExtraPlots[iCiv]
		for (x, y) in lPlots:
			plot = gc.getMap().plot( x, y )
			if not plot.isCity():
				utils.convertPlotCulture(plot, iCiv, 100, False)


	def findSeaPlots( self, tCoords, iRange):
		"""Searches a sea plot that isn't occupied by a unit within range of the starting coordinates"""
		# we can search inside other players territory, since all naval units can cross sea borders
		seaPlotList = []
		for (x, y) in utils.surroundingPlots(tCoords, iRange):
			plot = gc.getMap().plot( x, y )
			if plot.isWater() and not plot.isUnit():
				seaPlotList.append((x, y))
				# this is a good plot, so paint it and continue search
		if seaPlotList:
			return utils.getRandomEntry(seaPlotList)
		return None


	def giveColonists( self, iCiv, tBroaderAreaTL, tBroaderAreaBR):
	# 3Miro: Conquistador event
		pass


	def onFirstContact(self, iTeamX, iHasMetTeamY):
	# 3Miro: Conquistador event
		pass


	def getSpecialRespawn( self, iGameTurn ): #Absinthe: only the first civ for which it is true is returned, so the order of the civs is very important here
		if self.canSpecialRespawn(iFrankia, iGameTurn, 12):
			# France united in it's modern borders, start of the Bourbon royal line
			if xml.i1588AD < iGameTurn < xml.i1700AD and iGameTurn % 5 == 3:
				return iFrankia
		if self.canSpecialRespawn(iArabia, iGameTurn):
			# Saladin, Ayyubid Dynasty
			if xml.i1080AD < iGameTurn < xml.i1291AD and iGameTurn % 7 == 3:
				return iArabia
		if self.canSpecialRespawn(iBulgaria, iGameTurn):
			# second Bulgarian Empire
			if xml.i1080AD < iGameTurn < xml.i1299AD and iGameTurn % 5 == 1:
				return iBulgaria
		if self.canSpecialRespawn(iCordoba, iGameTurn):
			# special respawn as the Hafsid dynasty in North Africa
			if xml.i1229AD < iGameTurn < xml.i1540AD and iGameTurn % 5 == 3:
				return iCordoba
		if self.canSpecialRespawn(iBurgundy, iGameTurn, 20):
			# Burgundy in the 100 years war
			if xml.i1336AD < iGameTurn < xml.i1453AD and iGameTurn % 8 == 1:
				return iBurgundy
		if self.canSpecialRespawn(iPrussia, iGameTurn):
			# respawn as the unified Prussia
			if iGameTurn > xml.i1618AD and iGameTurn % 3 == 1:
				return iPrussia
		if self.canSpecialRespawn(iHungary, iGameTurn):
			# reconquest of Buda from the Ottomans
			if iGameTurn > xml.i1680AD and iGameTurn % 6 == 2:
				return iHungary
		if self.canSpecialRespawn(iSpain, iGameTurn, 25):
			# respawn as the Castile/Aragon Union
			if xml.i1470AD < iGameTurn < xml.i1580AD and iGameTurn % 5 == 0:
				return iSpain
		if self.canSpecialRespawn(iEngland, iGameTurn, 12):
			# restoration of monarchy
			if iGameTurn > xml.i1660AD and iGameTurn % 6 == 2:
				return iEngland
		if self.canSpecialRespawn(iScotland, iGameTurn, 30):
			if iGameTurn <= xml.i1600AD and iGameTurn % 6 == 3:
				return iScotland
		if self.canSpecialRespawn(iPortugal, iGameTurn):
			# respawn to be around for colonies
			if xml.i1431AD < iGameTurn < xml.i1580AD and iGameTurn % 5 == 3:
				return iPortugal
		if self.canSpecialRespawn(iAustria, iGameTurn):
			# increasing Habsburg influence in Hungary
			if xml.i1526AD < iGameTurn < xml.i1690AD and iGameTurn % 8 == 3:
				return iAustria
		if self.canSpecialRespawn(iKiev, iGameTurn):
			# Cossack Hetmanate
			if xml.i1620AD < iGameTurn < xml.i1750AD and iGameTurn % 5 == 3:
				return iKiev
		if self.canSpecialRespawn(iMorocco, iGameTurn):
			# Alaouite Dynasty
			if iGameTurn > xml.i1631AD and iGameTurn % 8 == 7:
				return iMorocco
		if self.canSpecialRespawn(iAragon, iGameTurn):
			# Kingdom of Sicily
			if iGameTurn > xml.i1700AD and iGameTurn % 8 == 7:
				return iAragon
		if self.canSpecialRespawn(iVenecia, iGameTurn):
			if xml.i1401AD < iGameTurn < xml.i1571AD and iGameTurn % 8 == 7:
				return iVenecia
		if self.canSpecialRespawn(iPoland, iGameTurn):
			if xml.i1410AD < iGameTurn < xml.i1570AD and iGameTurn % 8 == 7:
				return iPoland
		if self.canSpecialRespawn(iTurkey, iGameTurn):
			# Mehmed II's conquests
			if xml.i1453AD < iGameTurn < xml.i1514AD and iGameTurn % 6 == 3:
				return iTurkey
		return -1


	def canSpecialRespawn(self, iPlayer, iGameTurn, iLastAliveInterval = 10):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive(): return False
		if pPlayer.getEverRespawned(): return False
		if iGameTurn <= con.tBirth[iPlayer] + 25: return False
		if iGameTurn <= (utils.getLastTurnAlive(iPlayer) + iLastAliveInterval): return False
		return True


	def initMinorBetrayal( self, iCiv ):
		iHuman = utils.getHumanID()
		plotList = utils.squareSearch( tCoreAreasTL[iCiv], tCoreAreasBR[iCiv], utils.outerInvasion, [] )
		if plotList:
			tPlot = utils.getRandomEntry(plotList)
			self.createAdditionalUnits(iCiv, tPlot)
			self.unitsBetrayal(iCiv, iHuman, tCoreAreasTL[iCiv], tCoreAreasBR[iCiv], tPlot)


	def initBetrayal( self ):
		iHuman = utils.getHumanID()
		turnsLeft = self.getBetrayalTurns()
		plotList = utils.squareSearch( self.getTempTopLeft(), self.getTempBottomRight(), utils.outerInvasion, [] )
		if not plotList:
			plotList = utils.squareSearch( self.getTempTopLeft(), self.getTempBottomRight(), utils.innerSpawn, [self.getOldCivFlip(), self.getNewCivFlip()] )
		if not plotList:
			plotList = utils.squareSearch( self.getTempTopLeft(), self.getTempBottomRight(), utils.forcedInvasion, [self.getOldCivFlip(), self.getNewCivFlip()] )
		if plotList:
			tPlot = utils.getRandomEntry(plotList)
			if turnsLeft == iBetrayalPeriod:
				self.createAdditionalUnits(self.getNewCivFlip(), tPlot)
			self.unitsBetrayal(self.getNewCivFlip(), self.getOldCivFlip(), self.getTempTopLeft(), self.getTempBottomRight(), tPlot)
		self.setBetrayalTurns(turnsLeft - 1)


	def unitsBetrayal( self, iNewOwner, iOldOwner, tTopLeft, tBottomRight, tPlot ):
		#print ("iNewOwner", iNewOwner, "iOldOwner", iOldOwner, "tPlot", tPlot)
		if gc.getPlayer(self.getOldCivFlip()).isHuman():
			CyInterface().addMessage(self.getOldCivFlip(), False, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
		elif gc.getPlayer(self.getNewCivFlip()).isHuman():
			CyInterface().addMessage(self.getNewCivFlip(), False, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL_NEW", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
		for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
			killPlot = gc.getMap().plot(x,y)
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				for i in range(iNumUnitsInAPlot):
					unit = killPlot.getUnit(i)
					if unit.getOwner() == iOldOwner:
						rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
						if rndNum >= iBetrayalThreshold:
							if unit.getDomainType() == DomainTypes.DOMAIN_LAND: #land unit
								iUnitType = unit.getUnitType()
								unit.kill(False, iNewOwner)
								utils.makeUnit(iUnitType, iNewOwner, tPlot, 1)
								i = i - 1


	def createAdditionalUnits( self, iCiv, tPlot ):
		# additional starting units if someone declares war on the civ during birth
		if iCiv == iArabia:
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
		elif iCiv == iBulgaria:
			utils.makeUnit(xml.iBulgarianKonnik, iCiv, tPlot, 2)
		elif iCiv == iCordoba:
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
		elif iCiv == iVenecia:
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
		elif iCiv == iBurgundy:
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
		elif iCiv == iGermany:
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
		elif iCiv == iNovgorod:
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
		elif iCiv == iNorway:
			utils.makeUnit(xml.iVikingBeserker, iCiv, tPlot, 4)
		elif iCiv == iKiev:
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 3)
		elif iCiv == iHungary:
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
		elif iCiv == iSpain:
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 2)
		elif iCiv == iDenmark:
			utils.makeUnit(xml.iDenmarkHuskarl, iCiv, tPlot, 3)
		elif iCiv == iScotland:
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 3)
		elif iCiv == iPoland:
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 3)
		elif iCiv == iGenoa:
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
		elif iCiv == iMorocco:
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif iCiv == iEngland:
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif iCiv == iPortugal:
			utils.makeUnit(xml.iPortugalFootKnight, iCiv, tPlot, 3)
		elif iCiv == iAragon:
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 4)
		elif iCiv == iSweden:
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif iCiv == iPrussia:
			utils.makeUnit(xml.iTeutonic, iCiv, tPlot, 3)
		elif iCiv == iLithuania:
			utils.makeUnit(xml.iLithuanianBajoras, iCiv, tPlot, 2)
		elif iCiv == iAustria:
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif iCiv == iTurkey:
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
		elif iCiv == iMoscow:
			utils.makeUnit(xml.iMoscowBoyar, iCiv, tPlot, 2)
		elif iCiv == iDutch:
			utils.makeUnit(xml.iNetherlandsGrenadier, iCiv, tPlot, 2)


	def createStartingUnits( self, iCiv, tPlot ):
		# set the provinces
		self.pm.onSpawn( iCiv )
		iHuman = utils.getHumanID()
		# Change here to make later starting civs work
		if iCiv == iArabia:
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSpearman, iCiv, tPlot, 2)
			# additional units for the AI
			if (iCiv != iHuman):
				utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 2)
				utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
				utils.makeUnit(xml.iSpearman, iCiv, tPlot, 2)
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
		elif iCiv == iBulgaria:
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iBulgarianKonnik, iCiv, tPlot, 5)
			# additional units for the AI
			if iCiv != iHuman:
				utils.makeUnit(xml.iArcher, iCiv, tPlot, 1)
				utils.makeUnit(xml.iSpearman, iCiv, tPlot, 2)
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
		elif iCiv == iCordoba:
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 3)
			# additional units for the AI
			if iCiv != iHuman:
				utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
				utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 2)
		elif (iCiv == iVenecia):
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
			utils.makeUnit(xml.iSpearman, iCiv, tPlot, 1)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots((57,35), 2)
			if tSeaPlot:
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
				pVenecia.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pVenecia.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iArcher,iCiv,tSeaPlot,1)
				pVenecia.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iSpearman,iCiv,tSeaPlot,1)
		elif iCiv == iBurgundy:
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
		elif iCiv == iGermany:
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			# additional units for the AI
			if iCiv != iHuman:
				utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
				utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
		elif iCiv == iNovgorod:
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 1)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 1)
			# additional units for the AI
			if iCiv != iHuman:
				utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
		elif iCiv == iNorway:
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iVikingBeserker, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if tSeaPlot:
				pNorway.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pNorway.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pNorway.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iArcher, iCiv, tSeaPlot, 1 )
		elif iCiv == iKiev:
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 3)
			# additional units for the AI
			if iCiv != iHuman:
				utils.makeUnit(xml.iArcher, iCiv, tPlot, 3)
				utils.makeUnit(xml.iSpearman, iCiv, tPlot, 3)
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
		elif iCiv == iHungary:
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
			# additional units for the AI
			if iCiv != iHuman:
				utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
				utils.makeUnit(xml.iSpearman, iCiv, tPlot, 2)
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
		elif iCiv == iSpain:
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iLancer, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCatapult, iCiv, tPlot, 1)
		elif iCiv == iDenmark:
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iDenmarkHuskarl, iCiv, tPlot, 4)
			tSeaPlot = self.findSeaPlots((60,57), 2)
			if tSeaPlot:
				pDenmark.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pDenmark.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pDenmark.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(xml.iCrossbowman, iCiv, tSeaPlot, 1 )
		elif iCiv == iScotland:
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
		elif iCiv == iPoland:
			utils.makeUnit(xml.iArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			# additional units for the AI
			if iCiv != iHuman:
				utils.makeUnit(xml.iArcher, iCiv, tPlot, 2)
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
		elif iCiv == iGenoa:
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if tSeaPlot:
				pGenoa.initUnit(xml.iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pGenoa.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
		elif iCiv == iMorocco:
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 1)
			# additional units for the AI
			if iCiv != iHuman:
				utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
				utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 2)
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
		elif iCiv == iEngland:
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iLongSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if tSeaPlot:
				pEngland.initUnit(xml.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
			if not gc.getPlayer(iEngland).isHuman():
				utils.makeUnit(xml.iSettler, iCiv, tPlot, 1)
				utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 1)
		elif iCiv == iPortugal:
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iPortugalFootKnight, iCiv, tPlot, 4)
			utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 1)
		elif iCiv == iAragon:
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iAragonAlmogavar, iCiv, tPlot, 5)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			# Look for a sea plot close to the coast
			tSeaPlot = self.findSeaPlots((39,28), 2)
			if tSeaPlot:
				pAragon.initUnit(xml.iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pAragon.initUnit(xml.iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
		elif iCiv == iSweden:
			utils.makeUnit(xml.iLongSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots((69,65), 2)
			if tSeaPlot:
				utils.makeUnit(xml.iWorkboat, iCiv, tSeaPlot, 1 )
				pSweden.initUnit(xml.iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pSweden.initUnit(xml.iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pSweden.initUnit(xml.iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(xml.iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(xml.iCrossbowman,iCiv,tSeaPlot,1)
		elif iCiv == iPrussia:
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iTeutonic, iCiv, tPlot, 3) # at least one will probably leave for Crusade
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 2)
			utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 3)
		elif iCiv == iLithuania:
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iLithuanianBajoras, iCiv, tPlot, 5)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 3)
		elif iCiv == iAustria:
			utils.makeUnit(xml.iArbalest, iCiv, tPlot, 4)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iHeavyLancer, iCiv, tPlot, 3)
			utils.makeUnit(xml.iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iKnight, iCiv, tPlot, 4)
			utils.makeUnit(xml.iCatholicMissionary, iCiv, tPlot, 2)
		elif iCiv == iTurkey:
			utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 5)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iKnight, iCiv, tPlot, 2)
			utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 4)
			utils.makeUnit(xml.iTrebuchet, iCiv, tPlot, 2)
			utils.makeUnit(xml.iTurkeyGreatBombard, iCiv, tPlot, 3)
			utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 4)
			# additional units for the AI
			if iCiv != iHuman:
				utils.makeUnit(xml.iKnight, iCiv, tPlot, 2)
				utils.makeUnit(xml.iHorseArcher, iCiv, tPlot, 2)
				utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 3)
		elif iCiv == iMoscow:
			utils.makeUnit(xml.iArbalest, iCiv, tPlot, 5)
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 3)
			utils.makeUnit(xml.iMoscowBoyar, iCiv, tPlot, 5)
			utils.makeUnit(xml.iGuisarme, iCiv, tPlot, 4)
			utils.makeUnit(xml.iOrthodoxMissionary, iCiv, tPlot, 3)
		elif iCiv == iDutch:
			utils.makeUnit(xml.iSettler, iCiv, tPlot, 2)
			utils.makeUnit(xml.iMusketman, iCiv, tPlot, 8)
			utils.makeUnit(xml.iMaceman, iCiv, tPlot, 3)
			utils.makeUnit(xml.iProtestantMissionary, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if tSeaPlot:
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
		if iCiv == iTurkey:
			self.ottomanInvasion(iCiv, (77, 23))


	def create1200ADstartingUnits( self ):
		iHuman = utils.getHumanID()
		if con.tBirth[iHuman] > xml.i1200AD: # so iSweden, iPrussia, iLithuania, iAustria, iTurkey, iMoscow, iDutch
			tStart = tCapitals[iHuman]

			# Absinthe: changes in the unit positions, in order to prohibit these contacts in 1200AD
			if iHuman == iSweden: # contact with Denmark
				tStart = (tCapitals[iSweden][0]-2, tCapitals[iSweden][1]+2)
			elif iHuman == iPrussia: # contact with Poland
				tStart = (tCapitals[iPrussia][0]+1, tCapitals[iPrussia][1]+1)
			elif iHuman == iLithuania: # contact with Kiev
				tStart = (tCapitals[iLithuania][0]-2, tCapitals[iLithuania][1])
			elif iHuman == iAustria: # contact with Germany and Hungary
				tStart = (tCapitals[iAustria][0]-3, tCapitals[iAustria][1]-1)
			elif iHuman == iTurkey: # contact with Byzantium
				tStart = (98, 18)

			utils.makeUnit(xml.iSettler, iHuman, tStart, 1)
			utils.makeUnit(xml.iMaceman, iHuman, tStart, 1)


	def ottomanInvasion(self,iCiv,tPlot):
		print("I made Ottomans on Gallipoli")
		utils.makeUnit(xml.iLongbowman, iCiv, tPlot, 2)
		utils.makeUnit(xml.iMaceman, iCiv, tPlot, 2)
		utils.makeUnit(xml.iKnight, iCiv, tPlot, 3)
		utils.makeUnit(xml.iTurkeyGreatBombard, iCiv, tPlot, 2)
		utils.makeUnit(xml.iIslamicMissionary, iCiv, tPlot, 2)


	def create500ADstartingUnits( self ):
		# 3Miro: units on start (note Spearman might become an upgraded defender, tech dependent)

		utils.makeUnit(xml.iSettler, iFrankia, tCapitals[iFrankia], 3)
		utils.makeUnit(xml.iArcher, iFrankia, tCapitals[iFrankia], 4)
		utils.makeUnit(xml.iAxeman, iFrankia, tCapitals[iFrankia], 5)
		utils.makeUnit(xml.iScout, iFrankia, tCapitals[iFrankia], 1)
		utils.makeUnit(xml.iWorker, iFrankia, tCapitals[iFrankia], 2)
		utils.makeUnit(xml.iCatholicMissionary, iFrankia, tCapitals[iFrankia], 2)

		self.showArea(iByzantium)
		self.initContact(iByzantium)
		self.showArea(iFrankia)
		self.showArea(iPope)

		iHuman = utils.getHumanID()
		if con.tBirth[iHuman] > xml.i500AD: # so everyone apart from Byzantium and France
			tStart = tCapitals[iHuman]

			# Absinthe: changes in the unit positions, in order to prohibit these contacts in 500AD
			if iHuman == iArabia: # contact with Byzantium
				tStart = (tCapitals[iArabia][0], tCapitals[iArabia][1] - 10)
			elif iHuman == iBulgaria: # contact with Byzantium
				tStart = (tCapitals[iBulgaria][0], tCapitals[iBulgaria][1] + 1)
			elif iHuman == iTurkey: # contact with Byzantium
				tStart = (97, 23)

			utils.makeUnit(xml.iSettler, iHuman, tStart, 1)
			utils.makeUnit(xml.iSpearman, iHuman, tStart, 1)

	def assign1200ADtechs(self, iCiv):
		# As a temporary solution, everyone gets Aragon's starting techs
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

		if con.tBirth[iCiv] == 0:
			return

		if iCiv == iArabia:
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

		elif iCiv == iBulgaria:
			teamBulgaria.setHasTech( xml.iTheology, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iCalendar, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iStirrup, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iArchitecture, True, iCiv, False, False )
			teamBulgaria.setHasTech( xml.iBronzeCasting, True, iCiv, False, False )

		elif iCiv == iCordoba:
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

		elif iCiv == iVenecia:
			for iTech in range( xml.iStirrup + 1 ):
				teamVenecia.setHasTech( iTech, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iMusic, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamVenecia.setHasTech( xml.iChainMail, True, iCiv, False, False )

		elif iCiv == iBurgundy:
			for iTech in range( xml.iStirrup + 1 ):
				teamBurgundy.setHasTech( iTech, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iArt, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iEngineering, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamBurgundy.setHasTech( xml.iAstrolabe, True, iCiv, False, False )

		elif iCiv == iGermany:
			for iTech in range( xml.iStirrup + 1 ):
				teamGermany.setHasTech( iTech, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iFeudalism, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iArt, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iEngineering, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iAristocracy, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamGermany.setHasTech( xml.iAstrolabe, True, iCiv, False, False )

		elif iCiv == iNovgorod:
			for iTech in range( xml.iStirrup + 1 ):
				teamNovgorod.setHasTech( iTech, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamNovgorod.setHasTech( xml.iChainMail, True, iCiv, False, False )

		elif iCiv == iNorway:
			for iTech in range( xml.iStirrup + 1):
				teamNorway.setHasTech( iTech, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iAstrolabe, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamNorway.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )

		elif iCiv == iKiev:
			for iTech in range( xml.iStirrup + 1 ):
				teamKiev.setHasTech( iTech, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iVassalage, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iFarriers, True, iCiv, False, False )
			teamKiev.setHasTech( xml.iChainMail, True, iCiv, False, False )

		elif iCiv == iHungary:
			for iTech in range( xml.iStirrup + 1 ):
				teamHungary.setHasTech( iTech, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iChainMail, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iArt, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iHerbalMedicine, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iMonasticism, True, iCiv, False, False )
			teamHungary.setHasTech( xml.iVassalage, True, iCiv, False, False )

		elif iCiv == iSpain:
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

		elif iCiv == iDenmark:
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

		elif iCiv == iScotland:
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

		elif iCiv == iPoland:
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

		elif iCiv == iGenoa:
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

		elif iCiv == iMorocco:
			for iTech in range( xml.iFarriers + 1 ):
				teamMorocco.setHasTech( iTech, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iMapMaking, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamMorocco.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )

		elif iCiv == iEngland:
			for iTech in range( xml.iFarriers + 1 ):
				teamEngland.setHasTech( iTech, True, iCiv, False, False )
			teamEngland.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamEngland.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamEngland.setHasTech( xml.iAristocracy, True, iCiv, False, False )

		elif iCiv == iPortugal:
			for iTech in range( xml.iFarriers + 1 ):
				teamPortugal.setHasTech( iTech, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iBlastFurnace, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iCodeOfLaws, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iLiterature, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iLateenSails, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iMapMaking, True, iCiv, False, False )
			teamPortugal.setHasTech( xml.iAristocracy, True, iCiv, False, False )

		elif iCiv == iAragon:
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

		elif iCiv == iSweden:
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

		elif iCiv == iPrussia:
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

		elif iCiv == iLithuania:
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

		elif iCiv == iAustria:
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

		elif iCiv == iTurkey:
			for iTech in range( xml.iChivalry + 1 ):
				teamTurkey.setHasTech( iTech, True, iCiv, False, False )
			teamTurkey.setHasTech( xml.iGunpowder, True, iCiv, False, False )
			teamTurkey.setHasTech( xml.iMilitaryTradition, True, iCiv, False, False )
			teamTurkey.setHasTech( xml.iArabicKnowledge, True, iCiv, False, False )

		elif iCiv == iMoscow:
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

		elif iCiv == iDutch:
			for iTech in range( xml.iAstronomy + 1 ):
				teamDutch.setHasTech( iTech, True, iCiv, False, False )

		self.hitNeighboursStability(iCiv)


	def hitNeighboursStability( self, iCiv ):
		# 3Miro: Stability on Spawn
		if len(con.lOlderNeighbours[iCiv]) > 0:
		#	print "Got inside hitStability!!!"
			bHuman = False
			#for iLoop in con.lOlderNeighbours[iCiv]:
				#if (gc.getPlayer(iLoop).isAlive()):
				##	print("iLoop =",iLoop)
					#if (iLoop == utils.getHumanID()):
						#bHuman = True
					#utils.setStabilityParameters(iLoop, con.iParDiplomacyE, utils.getStabilityParameters(iLoop, con.iParDiplomacyE)-5)
					#utils.setStability(iLoop, utils.getStability(iLoop)-5)


	def showRect( self, iCiv, tArea ):
		iXs, iYs, iXe, iYe = tArea
		for (iX, iY) in utils.getPlotList((iXs, iYs), (iXe, iYe)):
			gc.getMap().plot(iX, iY).setRevealed(gc.getPlayer(iCiv).getTeam(), True, False, -1)


	def showArea(self, iCiv, iScenario = con.i500ADScenario):
		#print(" Visible for: ",iCiv )
		for iI in range( len( tVisible[iScenario][iCiv] ) ):
			self.showRect( iCiv, tVisible[iScenario][iCiv][iI] )
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