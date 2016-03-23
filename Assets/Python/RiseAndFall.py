# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
import Popup
import CvTranslator
import RFCUtils
import ProvinceManager # manage provinces here to link to spawn/rebirth
from Consts import *
from XMLConsts import *
import Religions
import Victory
from StoredData import sd


################
### Globals ###
##############

gc = CyGlobalContext()	# LOQ
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()
rel = Religions.Religions()
vic = Victory.Victory()

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 66
iRebellionDelay = 15
iEscapePeriod = 30

#This is now obsolete
#for not allowing new civ popup if too close
#Sedna17, moving around the order in which civs rise without changing their WBS requires you to do funny things here to prevent "Change Civ?" popups
#Spain and Moscow have really long delays for this reason
#This is now obsolete
#tDifference = (0, 0, 0, 1, 0, 1, 10, 0, 0, 1, 0, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

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
	def setRespawnTurn( self, iCiv, iNewValue ):
		sd.scriptDict['lRespawnTurns'][iCiv] = iNewValue

	def getAllRespawnTurns( self):
		return sd.scriptDict['lRespawnTurns']


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
			#for i in range(iNumStabilityParameters):
			#	utils.setStabilityParameters(utils.getHumanID(),i, 0)
			#	utils.setLastRecordedStabilityStuff(0, 0)
			#	utils.setLastRecordedStabilityStuff(1, 0)
			#	utils.setLastRecordedStabilityStuff(2, 0)
			#	utils.setLastRecordedStabilityStuff(3, 0)
			#	utils.setLastRecordedStabilityStuff(4, 0)
			#	utils.setLastRecordedStabilityStuff(5, 0)
			for iMaster in range(iNumPlayers):
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
			CyInterface().addMessage(iHuman, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_AGREED", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)

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

					#humanCityList[i].setHasRealBuilding(iPlague, False) #buggy

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
			CyInterface().addMessage(iHuman, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)


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

		self.setEarlyLeaders()

		#Sedna17 Respawn setup special respawn turns
		self.setupRespawnTurns()

		iHuman = utils.getHumanID()
		if utils.getScenario() == i500ADScenario:
			self.create500ADstartingUnits()
		else:
			self.create1200ADstartingUnits()
			for iCiv in range(iAragon+1):
				self.showArea(iCiv, i1200ADScenario)
				self.assign1200ADtechs(iCiv)	#Temporary all civs get Aragon starting techs
				self.initContact(iCiv, False)
			rel.set1200Faith()
			self.setDiplo1200AD()
			self.LeaningTowerGP()
			rel.spread1200ADJews() # Spread Jews to some random cities
			vic.set1200UHVDone(iHuman)
			self.assign1200ADtechs(iPope)	#Temporary all civs get Aragon starting techs

		self.assignGold(utils.getScenario())

	def assignGold(self, iScenario):
		for iPlayer in range(iNumPlayers):
			gc.getPlayer(iPlayer).changeGold(tStartingGold[iScenario][iPlayer])

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
			pCity.setHasRealBuilding( iWalls, True )
		if ( (pCity.getX()==55) and (pCity.getY()==41) ): #Augsburg
			pCity.setHasRealBuilding( iWalls, True )
		#if ( (pCity.getX()==41) and (pCity.getY()==52) ): #London			preplaced fort on the map instead of preplaced walls
		#	pCity.setHasRealBuilding( iWalls, True )
		if ( (pCity.getX()==23) and (pCity.getY()==31) ): #Porto
			pCity.setHasRealBuilding( iWalls, True )
		if ( (pCity.getX()==60) and (pCity.getY()==44) ): #Prague
			pCity.setHasRealBuilding( iWalls, True )
		#if ( (pCity.getX()==80) and (pCity.getY()==62) ): #Novgorod		preplaced fort on the map instead of preplaced walls
		#	pCity.setHasRealBuilding( iWalls, True )
		if ( (pCity.getX()==74) and (pCity.getY()==58) ): #Riga
			pCity.setHasRealBuilding( iWalls, True )
		if (not gc.getPlayer(iLithuania).isHuman()):
			if ( (pCity.getX()==75) and (pCity.getY()==53) ): #Vilnius - important for AI Lithuania against Prussia
				pCity.setHasRealBuilding( iWalls, True )


	def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
		self.pm.onCityAcquired(owner, playerType, city, bConquest, bTrade)
		if ( playerType == iTurkey ):
			if ( city.getX() == tCapitals[iByzantium][0] and city.getY() == tCapitals[iByzantium][1] ): # Constantinople (81,24)
				apCityList = PyPlayer(playerType).getCityList()
				for pCity in apCityList:
					loopCity = pCity.GetCy()
					if (loopCity != city):
						loopCity.setHasRealBuilding((iPalace), False)
				city.setHasRealBuilding((iPalace), True)
				if ( pTurkey.getStateReligion() == iIslam ):
					city.setHasReligion(iIslam,1,1,0)

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
								loopCity.setHasRealBuilding((iPalace), False)
						city.setHasRealBuilding((iPalace), True)
					if ( pTurkey.getStateReligion() == iIslam ): # you get Islam anyway, as a bonus
						city.setHasReligion(iIslam,1,1,0)


	def onCityRazed(self, iOwner, playerType, city):
		self.pm.onCityRazed(iOwner, playerType, city) # Province Manager


	def clear600ADChina(self):
		pass


	#Sedna17 Respawn
	def setupRespawnTurns(self):
		for iCiv in range(iNumMajorPlayers):
			self.setRespawnTurn(iCiv, tRespawnTime[iCiv]+(gc.getGame().getSorenRandNum(21, 'BirthTurnModifier') - 10)+(gc.getGame().getSorenRandNum(21, 'BirthTurnModifier2') - 10)) #bell-curve-like spawns within +/- 10 turns of desired turn (3Miro: Uniform, not a bell-curve)


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
					if (tBirth[iCiv]+self.getBirthTurnModifier(iCiv) == tBirth[iNextCiv]+self.getBirthTurnModifier(iNextCiv)):
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
				if ( tWarAtSpawn[utils.getScenario()][i][j] > 0 ): # if there is a chance for war
					if ( gc.getGame().getSorenRandNum(100, 'war on spawn roll') < tWarAtSpawn[utils.getScenario()][i][j] ):
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
			for i in range( iIndepStart, iIndepEnd + 1 ):
				pIndy = gc.getPlayer( i )
				if ( pIndy.isAlive() ):
					utils.updateMinorTechs(i, iBarbarian)
			#if (pIndependent.isAlive()):
			#	utils.updateMinorTechs(iIndependent, iBarbarian)
			#if (pIndependent2.isAlive()):
			#	utils.updateMinorTechs(iIndependent2, iBarbarian)

		# Absinthe: checking the spawn dates
		for iLoopCiv in range( iNumMajorPlayers ):
			if ( (not (tBirth[iLoopCiv] == 0) ) and iGameTurn >= tBirth[iLoopCiv] - 2 and iGameTurn <= tBirth[iLoopCiv] + 4):
				self.initBirth(iGameTurn, tBirth[iLoopCiv], iLoopCiv)


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
		if (iGameTurn >= 64 and iGameTurn % 5 == 0): #mainly for Seljuks, Mongols, Timurids
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
		# Absinthe: was 12 and 8, we don't need too many dead civs
		iNumDeadCivs1 = 10 #5 in vanilla RFC, 8 in warlords RFC (that includes native and celt)
		iNumDeadCivs2 = 7 #3 in vanilla RFC, 6 in Warlords RFC (where we must count natives and celts as dead too)

		iCiv = self.getSpecialRespawn( iGameTurn )
		if ( iCiv > -1 ):
			self.resurrection(iGameTurn,iCiv)
		elif (gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs1):
			if (iGameTurn % 14 == 11):
				self.resurrection(iGameTurn, -1)
		elif (gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs2):
			if (iGameTurn % 31 == 13):
				self.resurrection(iGameTurn, -1)
		#lRespawnTurns = self.getAllRespawnTurns()
		#print("Special Respawn Turns ",lRespawnTurns)
		#if iGameTurn in lRespawnTurns:
		#	iCiv = lRespawnTurns.index(iGameTurn)#Lookup index for
		#	print("Special Respawn For Player: ",iCiv)
		#	if iCiv < iNumMajorPlayers and iCiv > 0:
		#		self.resurrection(iGameTurn,iCiv)

		# Absinthe: Reduce cities to towns, in order to make room for new civs
		if(iGameTurn == tBirth[iEngland] -3):
			# Reduce Norwich and Nottingham, so more freedom in where to found cities in England
			self.reduceCity((43,55))
			self.reduceCity((39,56))
		elif(iGameTurn == tBirth[iSweden] -2):
			# Reduce Uppsala
			self.reduceCity((65,66))


	# Absinthe: disappearing cities (reducing them to an improvement)
	def reduceCity(self, tPlot):
		pPlot = gc.getMap().plot(tPlot[0],tPlot[1])
		if(pPlot.isCity()):
			# Apologize from the player:
			msgString = CyTranslator().getText("TXT_KEY_REDUCE_CITY_1", ()) + " " + pPlot.getPlotCity().getName() + " " + CyTranslator().getText("TXT_KEY_REDUCE_CITY_2", ())
			CyInterface().addMessage(pPlot.getPlotCity().getOwner(), True, iDuration, msgString, "", 0, "", ColorTypes(iLightRed), tPlot[0], tPlot[1], True, True)

			pPlot.eraseCityDevelopment()
			pPlot.setImprovementType(iImprovementTown) # Improvement Town instead of the city
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
		#	if in 1300AD Dublin is still Barbarian, it will flip to England
		if ( iGameTurn == i1300AD and utils.getHumanID() != iEngland and iPlayer == iEngland and pEngland.isAlive() ):
			pPlot = gc.getMap().plot( 32, 58 )
			if ( pPlot.isCity() ):
				if ( pPlot.getPlotCity().getOwner() == iBarbarian ):
					pDublin = pPlot.getPlotCity()
					utils.cultureManager((pDublin.getX(),pDublin.getY()), 50, iEngland, iBarbarian, False, True, True)
					utils.flipUnitsInCityBefore((pDublin.getX(),pDublin.getY()), iEngland, iBarbarian)
					self.setTempFlippingCity((pDublin.getX(),pDublin.getY()))
					utils.flipCity((pDublin.getX(),pDublin.getY()), 0, 0, iEngland, [iBarbarian]) #by trade because by conquest may raze the city
					utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iEngland)
			#print( " 3Miro: Called for - ",iPlayer," on turn ",iGameTurn )
			#utils.setLastTurnAlive( iPlayer, iGameTurn )

		# Absinthe: Another English AI cheat, extra defenders and defensive buildings in Normandy some turns after spawn - from RFCE++
		if( iGameTurn == i1066AD + 3 and utils.getHumanID() != iEngland and iPlayer == iEngland and pEngland.isAlive() ):
			print("Giving England some help in Normandy..")
			for loopx in range(39,46):
				for loopy in range(47,51):
					print("Is ", loopx, loopy, " an English city?")
					pCurrent = gc.getMap().plot( loopx, loopy )
					if ( pCurrent.isCity()):
						pCity = pCurrent.getPlotCity()
						if(pCity.getOwner() == iEngland):
							print("Yes! Defenders get!")
							utils.makeUnit(iGuisarme, iEngland, (loopx,loopy), 1)
							utils.makeUnit(iArbalest, iEngland, (loopx,loopy), 1)
							pCity.setHasRealBuilding(iWalls, True)
							pCity.setHasRealBuilding(iCastle,True)


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
					CyInterface().addMessage(iHuman, True, iDuration/2, CyTranslator().getText("TXT_KEY_LEADER_SWITCH", (gc.getPlayer(iPlayer).getName(), gc.getPlayer(iPlayer).getCivilizationDescriptionKey())), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, "", ColorTypes(iPurple), -1, -1, True, True)


	def fragmentIndependents(self):
		for iTest1 in range( iIndepStart, iIndepEnd + 1):
			for iTest2 in range( iIndepStart, iIndepEnd + 1):
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
			if (not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > tBirth[iDeadCiv] + 50):
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
									iNewCiv = iIndepStart + gc.getGame().getSorenRandNum(iIndepEnd - iIndepStart + 1, 'randomIndep')
									if (iDivideCounter % 4 == 0 or iDivideCounter % 4 == 1):
										utils.cultureManager((city.getX(),city.getY()), 50, iNewCiv, iBarbarian, False, True, True)
										utils.flipUnitsInCityBefore((city.getX(),city.getY()), iNewCiv, iBarbarian)
										self.setTempFlippingCity((city.getX(),city.getY()))
										utils.flipCity((city.getX(),city.getY()), 0, 0, iNewCiv, [iBarbarian]) #by trade because by conquest may raze the city
										utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
										iDivideCounter += 1
					return


	def collapseByBarbs(self, iGameTurn):
		for iCiv in range(iNumPlayers):
			if (gc.getPlayer(iCiv).isHuman() == 0 and gc.getPlayer(iCiv).isAlive()):
				# 3MiroUP: Emperor
				if (iGameTurn >= tBirth[iCiv] + 25 and not utils.collapseImmune(iCiv)):
					iNumCities = gc.getPlayer(iCiv).getNumCities()
					iLostCities = gc.countCitiesLostTo( iCiv, iBarbarian )
##					iLostCities = 0
##					for x in range(0, iMapMaxX):
##						for y in range(0, iMapMaxY):
##							if (gc.getMap().plot( x,y ).isCity()):
##								city = gc.getMap().plot( x,y ).getPlotCity()
##								if (city.getOwner() == iBarbarian):
##									if (city.getOriginalOwner() == iCiv):
##										iLostCities = iLostCities + 1
					if (iLostCities*2 > iNumCities+1 and iNumCities > 0): #if a little more than one third is captured, the civ collapses
						print ("COLLAPSE BY BARBS", gc.getPlayer(iCiv).getCivilizationAdjective(0))
						#utils.killAndFragmentCiv(iCiv, iIndependent, iIndependent2, -1, False)
						utils.killAndFragmentCiv(iCiv, False, False)
		# Add this part to force several cities to revolt in the case of very bad stability
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iPlayer = j % iNumPlayers
			#print(" 3Miro: player ",iPlayer)
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive() and iGameTurn >= tBirth[iPlayer] + 25):
				iStability = pPlayer.getStability()
				if (pPlayer.getStability() < -15 and (not utils.collapseImmune(iPlayer)) and (pPlayer.getNumCities() > 10) ): #civil war
					self.revoltCity( iPlayer, False )
					self.revoltCity( iPlayer, False )
					self.revoltCity( iPlayer, True )
					self.revoltCity( iPlayer, True )


	def collapseGeneric(self, iGameTurn):
		#lNumCitiesNew = l0Array
		lNumCitiesNew = l0ArrayTotal #for late start
		for iCiv in range(iNumTotalPlayers):
			if (iCiv < iNumActivePlayers ): #late start condition
				pCiv = gc.getPlayer(iCiv)
				teamCiv = gc.getTeam(pCiv.getTeam())
				if (pCiv.isAlive()):
					# 3MiroUP: Emperor
					if (iGameTurn >= tBirth[iCiv] + 25 and not utils.collapseImmune(iCiv)):
						lNumCitiesNew[iCiv] = pCiv.getNumCities()
						if (lNumCitiesNew[iCiv]*2 <= self.getNumCities(iCiv)): #if number of cities is less than half than some turns ago, the civ collapses
							print ("COLLAPSE GENERIC", pCiv.getCivilizationAdjective(0), lNumCitiesNew[iCiv]*2, "<=", self.getNumCities(iCiv))
							if (gc.getPlayer(iCiv).isHuman() == 0):
								bVassal = False
								for iMaster in range(iNumPlayers):
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
				if (iGameTurn >= tBirth[iCiv] + 25 and not utils.collapseImmune(iCiv)):
					if ( not gc.safeMotherland( iCiv ) ):
						print ("COLLAPSE: MOTHERLAND", gc.getPlayer(iCiv).getCivilizationAdjective(0))
						#utils.killAndFragmentCiv(iCiv, iIndependent, iIndependent2, -1, False)
						utils.killAndFragmentCiv(iCiv, False, False)


	def secession(self, iGameTurn): # checked every 3 turns
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iPlayer = j % iNumPlayers
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive() and iGameTurn >= tBirth[iPlayer] + 15):
				iStability = pPlayer.getStability()
				if ( gc.getGame().getSorenRandNum(10, 'do the check for city secession') < -iStability ): # x/10 chance with -x stability
					self.revoltCity( iPlayer, False )
					return # max 1 secession per turn


	def revoltCity( self, iPlayer, bForce ):
		# Absinthe: if bForce is true, then any city can revolt
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
							elif (iProvType < iProvincePotential):
								cityList.append(city)
								cityList.append(city)
						if (city.healthRate(False, 0) < -2):
							if (not utils.collapseImmuneCity(iPlayer,city.getX(),city.getY())):
								cityList.append(city)
							elif (iProvType < iProvincePotential):
								cityList.append(city)
								cityList.append(city)
						if (city.getReligionBadHappiness() > 0):
							if (not utils.collapseImmuneCity(iPlayer,city.getX(),city.getY())):
								cityList.append(city)
							elif (iProvType < iProvincePotential):
								cityList.append(city)
								cityList.append(city)
						if (city.getNoMilitaryPercentAnger() > 0):
							if (not utils.collapseImmuneCity(iPlayer,city.getX(),city.getY())):
								cityList.append(city)
							elif (iProvType < iProvincePotential):
								cityList.append(city)
								cityList.append(city)
						if ( iProvType == iProvinceOuter ):
							cityList.append(city)
						if ( iProvType == iProvinceNone ):
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
			iRndNum = gc.getGame().getSorenRandNum( iIndepEnd - iIndepStart + 1, 'random independent')
			iNewCiv = iIndepStart + iRndNum

			# Absinthe: choosing one city from the list (where each city can appear multiple times)
			splittingCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')]
			if (iPlayer == utils.getHumanID()):
				CyInterface().addMessage(iPlayer, True, iDuration, splittingCity.getName() + " " + CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(iOrange), -1, -1, True, True)
			utils.cultureManager((splittingCity.getX(),splittingCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
			utils.flipUnitsInCityBefore((splittingCity.getX(),splittingCity.getY()), iNewCiv, iPlayer)
			self.setTempFlippingCity((splittingCity.getX(),splittingCity.getY()))
			utils.flipCity((splittingCity.getX(),splittingCity.getY()), 0, 0, iNewCiv, [iPlayer]) #by trade because by conquest may raze the city
			utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
			#print ("SECESSION", gc.getPlayer(iPlayer).getCivilizationAdjective(0), splittingCity.getName()) #causes c++ exception??
			#Absinthe: loosing a city to secession/revolt gives a small boost to stability, to avoid a city-revolting chain reaction
			pPlayer.changeStabilityBase( iCathegoryExpansion, 2 )


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
			if (not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > tBirth[iDeadCiv] + 25 and iGameTurn > utils.getLastTurnAlive(iDeadCiv) + 10): #Sedna17: Allow re-spawns only 10 turns after death and 25 turns after birth
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
						if ((x,y) not in tNormalAreasSubtract[iDeadCiv]):
						#if ((x,y) not in tExceptions[iDeadCiv]):
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
														city.getNoMilitaryPercentAnger() > 0):
															cityList.append(pCurrent.getPlotCity())
															#print (iDeadCiv, pCurrent.getPlotCity().getName(), pCurrent.getPlotCity().getOwner(), "3", cityList)
										if ( (not bSpecialRespawn) and (iOwnerStability < 10) ):
												if (city.getX() == tCapitals[iDeadCiv][0] and city.getY() == tCapitals[iDeadCiv][1]):
													if (pCurrent.getPlotCity() not in cityList):
														cityList.append(pCurrent.getPlotCity())
				if (len(cityList) >= iMinNumCities ):
					if bSpecialRespawn or (gc.getGame().getSorenRandNum(100, 'roll') < tResurrectionProb[iDeadCiv]): #If special, always happens
						lCityList = []
						for iCity in range( len(cityList) ):
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
			if (iOwner == iBarbarian or utils.isIndep( iOwner ) ):
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
					utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iDeadCiv, [iOwner]) #by trade because by conquest may raze the city
					utils.createGarrisons(self.getTempFlippingCity(), iDeadCiv, iNewUnits)

			#cityList[k].setHasRealBuilding(iPlague, False)

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
								gc.getTeam(gc.getPlayer(iDeadCiv).getTeam()).setVassal(iOwner, True, False) #remove in vanilla
								bAlreadyVassal = True
					else:
						teamOwner.makePeace(iDeadCiv)
					ownersList.append(iOwner)
					for t in range(iNumTechs):
						if (teamOwner.isHasTech(t)):
							teamDeadCiv.setHasTech(t, True, iDeadCiv, False, False)

		for t in range(iNumTechs):
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
		#					if (gc.getPlayer(iDeadCiv).getSettlersMaps( iMapMaxY-indY-1, indX ) >= 90):
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

		CyInterface().addMessage(iHuman, True, iDuration, (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pDeadCiv.getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		#if (bHuman == True):
		#	self.rebellionPopup(iDeadCiv)
		if ( lSuppressList[iHuman] == 2 or lSuppressList[iHuman] == 3 or lSuppressList[iHuman] == 4 ):
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iDeadCiv, False, -1)
		else:
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iDeadCiv)
		# Absinthe: the new civs start as slightly stable
		pDeadCiv.changeStabilityBase( iCathegoryCities, -pDeadCiv.getStabilityBase( iCathegoryCities ) )
		pDeadCiv.changeStabilityBase( iCathegoryCivics, -pDeadCiv.getStabilityBase( iCathegoryCivics ) )
		pDeadCiv.changeStabilityBase( iCathegoryEconomy, -pDeadCiv.getStabilityBase( iCathegoryEconomy ) )
		pDeadCiv.changeStabilityBase( iCathegoryExpansion, -pDeadCiv.getStabilityBase( iCathegoryExpansion ) )
		pDeadCiv.changeStabilityBase( iCathegoryExpansion, 3 )
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
						if (not newCapital.hasBuilding(iPalace)):
							for pCity in apCityList:
								pCity.GetCy().setHasRealBuilding((iPalace), False)
							newCapital.setHasRealBuilding((iPalace), True)
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
						loopCity.setHasRealBuilding((iPalace), False)
				bestCity.setHasRealBuilding((iPalace), True)
				self.makeResurectionUnits( iCiv, bestCity.getX(), bestCity.getY() )


	def makeResurectionUnits( self, iPlayer, iX, iY ):
		if ( iPlayer == iCordoba ):
			utils.makeUnit(iSettler, iCordoba, [iX,iY], 2)
			utils.makeUnit(iCrossbowman, iCordoba, [iX,iY], 2)
			utils.makeUnit(iIslamicMissionary, iCordoba, [iX,iY], 1)


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
			#if (gc.getPlayer(iCiv).isAlive()) and (self.getAlreadySwitched() == False) and (iCurrentTurn > tBirth[iHuman]+40) and ( not gc.getPlayer( iHuman ).getIsCrusader() ):
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
		tCapital = tCapitals[iCiv]
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
##					if (unit.getUnitType() == iSettler):
##						break
##				unit.found()
				utils.flipUnitsInArea((tCapital[0]-4, tCapital[1]-4), (tCapital[0]+4, tCapital[1]+4), iCiv, iBarbarian, True, True) #This is for AI only. During Human player spawn, that area is already cleaned
				for i in range( iIndepStart, iIndepEnd + 1 ):
					utils.flipUnitsInArea((tCapital[0]-2, tCapital[1]-2), (tCapital[0]+2, tCapital[1]+2), iCiv, i, True, False) #This is for AI only. During Human player spawn, that area is already cleaned
				self.assignTechs(iCiv)
				utils.setPlagueCountdown(iCiv, -iImmunity)
				utils.clearPlague(iCiv)
				#gc.getPlayer(iCiv).changeAnarchyTurns(1)
				#gc.getPlayer(iCiv).setCivics(2, 11)
				self.setFlipsDelay(iCiv, iFlipsDelay) #save


		else: #starting units have already been placed, now the second part
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, tTopLeft, tBottomRight)
			self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			for i in range( iIndepStart, iIndepEnd + 1 ):
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
					utils.setPlagueCountdown(iCiv, -iImmunity)
					utils.clearPlague(iCiv)
					#gc.getPlayer(iCiv).changeAnarchyTurns(1)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			for i in range( iIndepStart, iIndepEnd + 1 ):
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
					utils.setPlagueCountdown(iCiv, -iImmunity)
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
						utils.setPlagueCountdown(iCiv, -iImmunity)
						utils.clearPlague(iCiv)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ
			for i in range( iIndepStart, iIndepEnd + 1 ):
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
						if (gc.getGame().getGameTurn() <= tBirth[iCiv] + 5): #if we're during a birth
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
				CyInterface().addMessage(iCiv, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_TO_US", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)

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
		if ( (not pFrankia.isAlive()) and (not pFrankia.getRespawned()) and iGameTurn > tBirth[iFrankia] + 25 and iGameTurn > utils.getLastTurnAlive(iFrankia) + 12 ):
			# France united in it's modern borders, start of the Bourbon royal line
			if ( iGameTurn > i1588AD and iGameTurn < i1700AD and iGameTurn % 5 == 3 ):
				return iFrankia
		if ( (not pArabia.isAlive()) and (not pArabia.getRespawned()) and iGameTurn > tBirth[iArabia] + 25 and iGameTurn > utils.getLastTurnAlive(iArabia) + 10 ):
			# Saladin, Ayyubid Dynasty
			if ( iGameTurn > i1080AD and iGameTurn < i1291AD and iGameTurn % 7 == 3 ):
				return iArabia
		if ( (not pBulgaria.isAlive()) and (not pBulgaria.getRespawned()) and iGameTurn > tBirth[iBulgaria] + 25 and iGameTurn > utils.getLastTurnAlive(iBulgaria) + 10 ):
			# second Bulgarian Empire
			if ( iGameTurn > i1080AD and iGameTurn < i1299AD and iGameTurn % 5 == 1 ):
				return iBulgaria
		if ( (not pCordoba.isAlive()) and (not pCordoba.getRespawned()) and iGameTurn > tBirth[iCordoba] + 25 and iGameTurn > utils.getLastTurnAlive(iCordoba) + 10 ):
			# special respawn as the Hafsid dynasty in North Africa
			if ( iGameTurn > i1229AD and iGameTurn < i1540AD and iGameTurn % 5 == 3 ):
				return iCordoba
		if ( (not pBurgundy.isAlive()) and (not pBurgundy.getRespawned()) and iGameTurn > tBirth[iBurgundy] + 25 and iGameTurn > utils.getLastTurnAlive(iBurgundy) + 20 ):
			# Burgundy in the 100 years war
			if ( iGameTurn > i1336AD and iGameTurn < i1453AD and iGameTurn % 8 == 1 ):
				return iBurgundy
		if ( (not pPrussia.isAlive()) and (not pPrussia.getRespawned()) and iGameTurn > tBirth[iPrussia] + 25 and iGameTurn > utils.getLastTurnAlive(iPrussia) + 10 ):
			# respawn as the unified Prussia
			if ( iGameTurn > i1618AD and iGameTurn % 3 == 1 ):
				return iPrussia
		if ( (not pHungary.isAlive()) and (not pHungary.getRespawned()) and iGameTurn > tBirth[iHungary] + 25 and iGameTurn > utils.getLastTurnAlive(iHungary) + 10 ):
			# reconquest of Buda from the Ottomans
			if ( iGameTurn > i1680AD and iGameTurn % 6 == 2 ):
				return iHungary
		if ( (not pSpain.isAlive()) and (not pSpain.getRespawned()) and iGameTurn > tBirth[iSpain] + 25 and iGameTurn > utils.getLastTurnAlive(iSpain) + 25 ):
			# respawn as the Castile/Aragon Union
			if ( iGameTurn > i1470AD and iGameTurn < i1580AD and iGameTurn % 5 == 0 ):
				return iSpain
		if ( (not pEngland.isAlive()) and (not pEngland.getRespawned()) and iGameTurn > tBirth[iEngland] + 25 and iGameTurn > utils.getLastTurnAlive(iEngland) + 12 ):
			# restoration of monarchy
			if ( iGameTurn > i1660AD and iGameTurn % 6 == 2 ):
				return iEngland
		if ( (not pScotland.isAlive()) and (not pScotland.getRespawned()) and iGameTurn > tBirth[iScotland] + 25 and iGameTurn > utils.getLastTurnAlive(iScotland) + 30 ):
			if ( iGameTurn <= i1600AD and iGameTurn % 6 == 3 ):
				return iScotland
		if ( (not pPortugal.isAlive()) and (not pPortugal.getRespawned()) and iGameTurn > tBirth[iPortugal] + 25 and iGameTurn > utils.getLastTurnAlive(iPortugal) + 10 ):
			# respawn to be around for colonies
			if ( iGameTurn > i1431AD and iGameTurn < i1580AD and iGameTurn % 5 == 3 ):
				return iPortugal
		if ( (not pAustria.isAlive()) and (not pAustria.getRespawned()) and iGameTurn > tBirth[iAustria] + 25 and iGameTurn > utils.getLastTurnAlive(iAustria) + 10 ):
			# increasing Habsburg influence in Hungary
			if ( iGameTurn > i1526AD and iGameTurn < i1690AD and iGameTurn % 8 == 3 ):
				return iAustria
		if ( (not pKiev.isAlive()) and (not pKiev.getRespawned()) and iGameTurn > tBirth[iKiev] + 25 and iGameTurn > utils.getLastTurnAlive(iKiev) + 10 ):
			# Cossack Hetmanate
			if ( iGameTurn >= i1620AD and iGameTurn < i1750AD and iGameTurn % 5 == 3 ):
				return iKiev
		if ( (not pMorocco.isAlive()) and (not pMorocco.getRespawned()) and iGameTurn > tBirth[iMorocco] + 25 and iGameTurn > utils.getLastTurnAlive(iMorocco) + 10 ):
			# Alaouite Dynasty
			if ( iGameTurn > i1631AD and iGameTurn % 8 == 7 ):
				return iMorocco
		if ( (not pAragon.isAlive()) and (not pAragon.getRespawned()) and iGameTurn > tBirth[iAragon] + 25 and iGameTurn > utils.getLastTurnAlive(iAragon) + 10 ):
			# Kingdom of Sicily
			if ( iGameTurn > i1700AD and iGameTurn % 8 == 7 ):
				return iAragon
		if ( (not pVenecia.isAlive()) and (not pVenecia.getRespawned()) and iGameTurn > tBirth[iVenecia] + 25 and iGameTurn > utils.getLastTurnAlive(iVenecia) + 10 ):
			if ( iGameTurn > i1401AD and iGameTurn < i1571AD and iGameTurn % 8 == 7 ):
				return iVenecia
		if ( (not pPoland.isAlive()) and (not pPoland.getRespawned()) and iGameTurn > tBirth[iPoland] + 25 and iGameTurn > utils.getLastTurnAlive(iPoland) + 10 ):
			if ( iGameTurn > i1410AD and iGameTurn < i1570AD and iGameTurn % 8 == 7 ):
				return iPoland
		if ( (not pTurkey.isAlive()) and (not pTurkey.getRespawned()) and iGameTurn > tBirth[iTurkey] + 25 and iGameTurn > utils.getLastTurnAlive(iTurkey) + 10 ):
			# Mehmed II's conquests
			if ( iGameTurn > i1453AD and iGameTurn < i1514AD and iGameTurn % 6 == 3 ):
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
			CyInterface().addMessage(self.getOldCivFlip(), False, iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		elif (gc.getPlayer(self.getNewCivFlip()).isHuman()):
			CyInterface().addMessage(self.getNewCivFlip(), False, iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL_NEW", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
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
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 4)
		elif ( iCiv == iBulgaria ):
			utils.makeUnit(iBulgarianKonnik, iCiv, tPlot, 2)
		elif ( iCiv == iCordoba ):
			utils.makeUnit(iAxeman, iCiv, tPlot, 2)
		elif ( iCiv == iVenecia ):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
		elif ( iCiv == iBurgundy ):
			utils.makeUnit(iLancer, iCiv, tPlot, 2)
		elif ( iCiv == iGermany ):
			utils.makeUnit(iLancer, iCiv, tPlot, 2)
		elif ( iCiv == iNovgorod ):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
		elif ( iCiv == iNorway ):
			utils.makeUnit(iVikingBeserker, iCiv, tPlot, 4)
		elif ( iCiv == iKiev ):
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 3)
		elif ( iCiv == iHungary ):
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 4)
		elif ( iCiv == iSpain ):
			utils.makeUnit(iLancer, iCiv, tPlot, 2)
		elif ( iCiv == iDenmark ):
			utils.makeUnit(iDenmarkHuskarl, iCiv, tPlot, 3)
		elif ( iCiv == iScotland ):
			utils.makeUnit(iAxeman, iCiv, tPlot, 3)
		elif ( iCiv == iPoland ):
			utils.makeUnit(iLancer, iCiv, tPlot, 3)
		elif ( iCiv == iGenoa ):
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 2)
		elif ( iCiv == iMorocco ):
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iEngland ):
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iPortugal ):
			utils.makeUnit(iPortugalFootKnight, iCiv, tPlot, 3)
		elif ( iCiv == iAragon ):
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 4)
		elif ( iCiv == iSweden ):
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iPrussia ):
			utils.makeUnit(iTeutonic, iCiv, tPlot, 3)
		elif ( iCiv == iLithuania ):
			utils.makeUnit(iLithuanianBajoras, iCiv, tPlot, 2)
		elif ( iCiv == iAustria ):
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iTurkey ):
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 3)
		elif ( iCiv == iMoscow ):
			utils.makeUnit(iMoscowBoyar, iCiv, tPlot, 2)
		elif ( iCiv == iDutch ):
			utils.makeUnit(iNetherlandsGrenadier, iCiv, tPlot, 2)


	def createStartingUnits( self, iCiv, tPlot ):
		# set the provinces
		self.pm.onSpawn( iCiv )
		# Change here to make later starting civs work
		if (iCiv == iArabia):
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 6)
		elif (iCiv == iBulgaria):
			utils.makeUnit(iArcher, iCiv, tPlot, 4)
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iBulgarianKonnik, iCiv, tPlot, 5)
		elif (iCiv == iCordoba):
			utils.makeUnit(iArcher, iCiv, tPlot, 4)
			utils.makeUnit(iSettler, iCiv, tPlot, 1)
			utils.makeUnit(iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(iIslamicMissionary, iCiv, tPlot, 3)
		elif (iCiv == iVenecia):
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSettler, iCiv, tPlot, 1)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 1)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1 )
				pVenecia.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pVenecia.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(iArcher,iCiv,tSeaPlot,1)
				pVenecia.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(iCrossbowman,iCiv,tSeaPlot,1)
		elif (iCiv == iBurgundy):
			utils.makeUnit(iSettler, iCiv, tPlot, 1)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 1)
		elif (iCiv == iGermany):
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iAxeman, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 2)
		elif (iCiv == iNovgorod):
			utils.makeUnit(iArcher, iCiv, tPlot, 3)
			utils.makeUnit(iSettler, iCiv, tPlot, 3)
			utils.makeUnit(iAxeman, iCiv, tPlot, 1)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 1)
		elif (iCiv == iNorway):
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iVikingBeserker, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				pNorway.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pNorway.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pNorway.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1 )
		elif (iCiv == iKiev):
			utils.makeUnit(iArcher, iCiv, tPlot, 4)
			utils.makeUnit(iSettler, iCiv, tPlot, 3)
			utils.makeUnit(iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 3)
		elif (iCiv == iHungary):
			utils.makeUnit(iArcher, iCiv, tPlot, 4)
			utils.makeUnit(iSettler, iCiv, tPlot, 3)
			utils.makeUnit(iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 4)
		elif (iCiv == iSpain):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSettler, iCiv, tPlot, 3)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(iLancer, iCiv, tPlot, 3)
			utils.makeUnit(iCatapult, iCiv, tPlot, 1)
		elif (iCiv == iDenmark):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iDenmarkHuskarl, iCiv, tPlot, 4)
			tSeaPlot = self.findSeaPlots((60,57), 2)
			if ( tSeaPlot ):
				pDenmark.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pDenmark.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pDenmark.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(iCrossbowman, iCiv, tSeaPlot, 1 )
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1 )
				utils.makeUnit(iCrossbowman, iCiv, tSeaPlot, 1 )
		elif (iCiv == iScotland):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 2)
		elif (iCiv == iPoland):
			utils.makeUnit(iArcher, iCiv, tPlot, 4)
			utils.makeUnit(iSettler, iCiv, tPlot, 3)
			utils.makeUnit(iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 2)
		elif (iCiv == iGenoa):
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				pGenoa.initUnit(iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pGenoa.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(iCrossbowman,iCiv,tSeaPlot,1)
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1 )
		elif (iCiv == iMorocco):
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iMaceman, iCiv, tPlot, 2)
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(iIslamicMissionary, iCiv, tPlot, 1)
		elif (iCiv == iEngland):
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iLongSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				pEngland.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
			if (not gc.getPlayer(iEngland).isHuman()):
				utils.makeUnit(iSettler, iCiv, tPlot, 1)
				utils.makeUnit(iCrossbowman, iCiv, tPlot, 1)
		elif (iCiv == iPortugal):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iPortugalFootKnight, iCiv, tPlot, 4)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 2)
			utils.makeUnit(iGuisarme, iCiv, tPlot, 2)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 1)
		elif (iCiv == iAragon):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iAragonAlmogavar, iCiv, tPlot, 5)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 2)
			# Look for a sea plot close to the coast
			tSeaPlot = self.findSeaPlots((39,28), 2)
			if ( tSeaPlot ):
				pAragon.initUnit(iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pAragon.initUnit(iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(iCrossbowman,iCiv,tSeaPlot,1)
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1 )
		elif (iCiv == iSweden):
			utils.makeUnit(iLongSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 2)
			utils.makeUnit(iSettler, iCiv, tPlot, 3)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots((71,64), 2)
			if ( tSeaPlot ):
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1 )
				pSweden.initUnit(iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pSweden.initUnit(iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pSweden.initUnit(iCogge, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler,iCiv,tSeaPlot,1)
				utils.makeUnit(iCrossbowman,iCiv,tSeaPlot,1)
		elif (iCiv == iPrussia):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iTeutonic, iCiv, tPlot, 3) # one will probably leave for Crusade
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 1)
			utils.makeUnit(iExecutive3, iCiv, tPlot, 2)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 3)
		elif (iCiv == iLithuania):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 4)
			utils.makeUnit(iSettler, iCiv, tPlot, 3)
			utils.makeUnit(iLithuanianBajoras, iCiv, tPlot, 5)
			utils.makeUnit(iGuisarme, iCiv, tPlot, 2)
		elif (iCiv == iAustria):
			utils.makeUnit(iArbalest, iCiv, tPlot, 4)
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iMaceman, iCiv, tPlot, 2)
			utils.makeUnit(iHeavyLancer, iCiv, tPlot, 3)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iKnight, iCiv, tPlot, 3)
			utils.makeUnit(iCatholicMissionary, iCiv, tPlot, 2)
		elif (iCiv == iTurkey):
			utils.makeUnit(iLongbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSettler, iCiv, tPlot, 3)
			utils.makeUnit(iMaceman, iCiv, tPlot, 2)
			utils.makeUnit(iKnight, iCiv, tPlot, 3)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 2)
			utils.makeUnit(iTurkeyGreatBombard, iCiv, tPlot, 2)
			utils.makeUnit(iIslamicMissionary, iCiv, tPlot, 4)
		elif (iCiv == iMoscow):
			utils.makeUnit(iArbalest, iCiv, tPlot, 4)
			utils.makeUnit(iSettler, iCiv, tPlot, 3)
			utils.makeUnit(iMoscowBoyar, iCiv, tPlot, 5)
			utils.makeUnit(iGuisarme, iCiv, tPlot, 4)
			utils.makeUnit(iOrthodoxMissionary, iCiv, tPlot, 3)
		elif (iCiv == iDutch):
			utils.makeUnit(iSettler, iCiv, tPlot, 2)
			utils.makeUnit(iMusketman, iCiv, tPlot, 6)
			utils.makeUnit(iProtestantMissionary, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 2)
			if ( tSeaPlot ):
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2 )
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 2 )

		self.showArea(iCiv)
		self.initContact(iCiv)


	def createStartingWorkers( self, iCiv, tPlot ):
		# 3Miro: get the workers
		# Sedna17: Cleaned the code
		print("Making starting workers")
		utils.makeUnit(iWorker, iCiv, tPlot, tStartingWorkers[iCiv])
		# Absinthe: second Ottoman spawn stack may stay, although they now spawn in Gallipoli in the first place (one plot SE)
		if ( iCiv == iTurkey ):
			self.ottomanInvasion(iCiv,(77,23))


	def create1200ADstartingUnits( self ):

		if ( pSweden.isHuman() and tBirth[iSweden] > 0 ):
			utils.makeUnit(iSettler, iSweden, tCapitals[iSweden], 1)
			utils.makeUnit(iSwordsman, iSweden, tCapitals[iSweden], 1)

		elif ( pPrussia.isHuman() and tBirth[iPrussia] > 0 ):
			utils.makeUnit(iSettler, iPrussia, tCapitals[iPrussia], 1)
			utils.makeUnit(iSwordsman, iPrussia, tCapitals[iPrussia], 1)

		elif ( pLithuania.isHuman() and tBirth[iLithuania] > 0 ):
			utils.makeUnit(iSettler, iLithuania, tCapitals[iLithuania], 1)
			utils.makeUnit(iSwordsman, iLithuania, tCapitals[iLithuania], 1)

		elif ( pAustria.isHuman() and tBirth[iAustria] > 0 ):
			utils.makeUnit(iSettler, iAustria, tCapitals[iAustria], 1)
			utils.makeUnit(iLongSwordsman, iAustria, tCapitals[iAustria], 1)

		elif ( pTurkey.isHuman() and tBirth[iTurkey] > 0 ):
			tTurkishStart = ( tCapitals[iTurkey][0]+5, tCapitals[iTurkey][1]+30 )
			utils.makeUnit(iSettler, iTurkey, tTurkishStart, 1)
			utils.makeUnit(iMaceman, iTurkey, tTurkishStart, 1)

		elif ( pDutch.isHuman() and tBirth[iDutch] > 0 ):
			utils.makeUnit(iSettler, iDutch, tCapitals[iDutch], 1)
			utils.makeUnit(iMaceman, iDutch, tCapitals[iDutch], 1)

	def ottomanInvasion(self,iCiv,tPlot):
		print("I made Ottomans on Gallipoli")
		utils.makeUnit(iLongbowman, iCiv, tPlot, 2)
		utils.makeUnit(iMaceman, iCiv, tPlot, 2)
		utils.makeUnit(iKnight, iCiv, tPlot, 3)
		utils.makeUnit(iTurkeyGreatBombard, iCiv, tPlot, 2)
		utils.makeUnit(iIslamicMissionary, iCiv, tPlot, 2)


	def create500ADstartingUnits( self ):
		# 3Miro: units on start (note Spearman might be an up to date upgraded defender, tech dependent)

		utils.makeUnit(iSettler, iFrankia, tCapitals[iFrankia], 3)
		utils.makeUnit(iArcher, iFrankia, tCapitals[iFrankia], 3)
		utils.makeUnit(iAxeman, iFrankia, tCapitals[iFrankia], 4)
		utils.makeUnit(iWorker, iFrankia, tCapitals[iFrankia], 2)
		utils.makeUnit(iCatholicMissionary, iFrankia, tCapitals[iFrankia], 1)

		self.showArea(iByzantium)
		self.initContact(iByzantium)
		self.showArea(iFrankia)
		self.showArea(iPope)

		if ( pBurgundy.isHuman() and tBirth[iBurgundy] > 0 ):
			# 3Miro: prohibit contact on turn 0 (with the Chronological spawn order this should not be needed)
			tBurgundyStart = ( tCapitals[iBurgundy][0]+2, tCapitals[iBurgundy][1] )
			utils.makeUnit(iSettler, iBurgundy, tCapitals[iBurgundy], 1)
			utils.makeUnit(iArcher, iBurgundy, tCapitals[iBurgundy], 1)
			utils.makeUnit(iWorker, iBurgundy, tCapitals[iBurgundy], 1)

		elif ( pArabia.isHuman() and tBirth[iArabia] > 0 ):
			# 3Miro: prohibit contact on turn 0
			tArabStart = ( tCapitals[iArabia][0], tCapitals[iArabia][1]-10)
			utils.makeUnit(iSettler, iArabia, tArabStart, 1)
			utils.makeUnit(iSpearman, iArabia, tArabStart, 1)

		elif ( pBulgaria.isHuman() and tBirth[iBulgaria] > 0 ):
			# 3Miro: prohibit contact on turn 0
			tBulgStart = ( tCapitals[iBulgaria][0], tCapitals[iBulgaria][1] + 1 )
			utils.makeUnit(iSettler, iBulgaria, tBulgStart, 1)
			utils.makeUnit(iSpearman, iBulgaria, tBulgStart, 1)

		elif ( pCordoba.isHuman() and tBirth[iCordoba] > 0 ):
			utils.makeUnit(iSettler, iCordoba, tCapitals[iCordoba], 1)
			utils.makeUnit(iSpearman, iCordoba, tCapitals[iCordoba], 1)

		elif ( pSpain.isHuman() and tBirth[iSpain] > 0 ):
			utils.makeUnit(iSettler, iSpain, tCapitals[iSpain], 1)
			utils.makeUnit(iSpearman, iSpain, tCapitals[iSpain], 1)

		elif ( pNorway.isHuman() and tBirth[iNorway] > 0 ):
			utils.makeUnit(iSettler, iNorway, tCapitals[iNorway], 1)
			utils.makeUnit(iSpearman, iNorway, tCapitals[iNorway], 1)

		elif ( pDenmark.isHuman() and tBirth[iDenmark] > 0 ):
			utils.makeUnit(iSettler, iDenmark, tCapitals[iDenmark], 1)
			utils.makeUnit(iSpearman, iDenmark, tCapitals[iDenmark], 1)

		elif ( pVenecia.isHuman() and tBirth[iVenecia] > 0 ):
			utils.makeUnit(iSettler, iVenecia, tCapitals[iVenecia], 1)
			utils.makeUnit(iSpearman, iVenecia, tCapitals[iVenecia], 1)

		elif ( pNovgorod.isHuman() and tBirth[iNovgorod] > 0 ):
			utils.makeUnit(iSettler, iNovgorod, tCapitals[iNovgorod], 1)
			utils.makeUnit(iSpearman, iNovgorod, tCapitals[iNovgorod], 1)

		elif ( pKiev.isHuman() and tBirth[iKiev] > 0 ):
			utils.makeUnit(iSettler, iKiev, tCapitals[iKiev], 1)
			utils.makeUnit(iSpearman, iKiev, tCapitals[iKiev], 1)

		elif ( pHungary.isHuman() and tBirth[iHungary] > 0 ):
			utils.makeUnit(iSettler, iHungary, tCapitals[iHungary], 1)
			utils.makeUnit(iSpearman, iHungary, tCapitals[iHungary], 1)

		elif ( pGermany.isHuman() and tBirth[iGermany] > 0 ):
			utils.makeUnit(iSettler, iGermany, tCapitals[iGermany], 1)
			utils.makeUnit(iSpearman, iGermany, tCapitals[iGermany], 1)

		elif ( pScotland.isHuman() and tBirth[iScotland] > 0 ):
			utils.makeUnit(iSettler, iScotland, tCapitals[iScotland], 1)
			utils.makeUnit(iSpearman, iScotland, tCapitals[iScotland], 1)

		elif ( pPoland.isHuman() and tBirth[iPoland] > 0 ):
			utils.makeUnit(iSettler, iPoland, tCapitals[iPoland], 1)
			utils.makeUnit(iSpearman, iPoland, tCapitals[iPoland], 1)

		elif ( pMoscow.isHuman() and tBirth[iMoscow] > 0 ):
			utils.makeUnit(iSettler, iMoscow, tCapitals[iMoscow], 1)
			utils.makeUnit(iSpearman, iMoscow, tCapitals[iMoscow], 1)

		elif ( pGenoa.isHuman() and tBirth[iGenoa] > 0 ):
			utils.makeUnit(iSettler, iGenoa, tCapitals[iGenoa], 1)
			utils.makeUnit(iSpearman, iGenoa, tCapitals[iGenoa], 1)

		elif ( pMorocco.isHuman() and tBirth[iMorocco] > 0 ):
			utils.makeUnit(iSettler, iMorocco, tCapitals[iMorocco], 1)
			utils.makeUnit(iSpearman, iMorocco, tCapitals[iMorocco], 1)

		elif ( pEngland.isHuman() and tBirth[iEngland] > 0 ):
			utils.makeUnit(iSettler, iEngland, tCapitals[iEngland], 1)
			utils.makeUnit(iSwordsman, iEngland, tCapitals[iEngland], 1)

		elif ( pPortugal.isHuman() and tBirth[iPortugal] > 0 ):
			utils.makeUnit(iSettler, iPortugal, tCapitals[iPortugal], 1)
			utils.makeUnit(iSwordsman, iPortugal, tCapitals[iPortugal], 1)

		elif ( pAragon.isHuman() and tBirth[iAragon] > 0 ):
			utils.makeUnit(iSettler, iAragon, tCapitals[iAragon], 1)
			utils.makeUnit(iSwordsman, iAragon, tCapitals[iAragon], 1)

		elif ( pPrussia.isHuman() and tBirth[iPrussia] > 0 ):
			utils.makeUnit(iSettler, iPrussia, tCapitals[iPrussia], 1)
			utils.makeUnit(iSwordsman, iPrussia, tCapitals[iPrussia], 1)

		elif ( pLithuania.isHuman() and tBirth[iLithuania] > 0 ):
			utils.makeUnit(iSettler, iLithuania, tCapitals[iLithuania], 1)
			utils.makeUnit(iSwordsman, iLithuania, tCapitals[iLithuania], 1)

		elif ( pAustria.isHuman() and tBirth[iAustria] > 0 ):
			utils.makeUnit(iSettler, iAustria, tCapitals[iAustria], 1)
			utils.makeUnit(iLongSwordsman, iAustria, tCapitals[iAustria], 1)

		elif ( pTurkey.isHuman() and tBirth[iTurkey] > 0 ):
			tTurkishStart = ( tCapitals[iTurkey][0]+5, tCapitals[iTurkey][1]+30 )
			utils.makeUnit(iSettler, iTurkey, tTurkishStart, 1)
			utils.makeUnit(iMaceman, iTurkey, tTurkishStart, 1)

		elif ( pSweden.isHuman() and tBirth[iSweden] > 0 ):
			utils.makeUnit(iSettler, iSweden, tCapitals[iSweden], 1)
			utils.makeUnit(iSwordsman, iSweden, tCapitals[iSweden], 1)

		elif ( pDutch.isHuman() and tBirth[iDutch] > 0 ):
			utils.makeUnit(iSettler, iDutch, tCapitals[iDutch], 1)
			utils.makeUnit(iMaceman, iDutch, tCapitals[iDutch], 1)

	def assign1200ADtechs(self, iCiv):
		# Temporary everyone gets Aragon techs
		teamCiv = gc.getTeam(iCiv)
		for iTech in range( iFarriers + 1 ):
			teamCiv.setHasTech( iTech, True, iCiv, False, False )
		teamCiv.setHasTech( iBlastFurnace, True, iCiv, False, False )
		teamCiv.setHasTech( iCodeOfLaws, True, iCiv, False, False )
		teamCiv.setHasTech( iLiterature, True, iCiv, False, False )
		teamCiv.setHasTech( iLateenSails, True, iCiv, False, False )
		teamCiv.setHasTech( iMapMaking, True, iCiv, False, False )
		teamCiv.setHasTech( iAristocracy, True, iCiv, False, False )
		teamCiv.setHasTech( iPlateArmor, True, iCiv, False, False )
		teamCiv.setHasTech( iGothicArchitecture, True, iCiv, False, False )
		teamCiv.setHasTech( iSiegeEngines, True, iCiv, False, False )
		if iCiv in [iArabia, iMorocco]:
			teamCiv.setHasTech( iArabicKnowledge, True, iCiv, False, False )

	def assignTechs( self, iCiv ):
		# 3Miro: other than the original techs

		if ( tBirth[iCiv] == 0 ):
			return

		if ( iCiv == iArabia ):
			teamArabia.setHasTech( iTheology, True, iCiv, False, False )
			teamArabia.setHasTech( iCalendar, True, iCiv, False, False )
			teamArabia.setHasTech( iLateenSails, True, iCiv, False, False )
			teamArabia.setHasTech( iStirrup, True, iCiv, False, False )
			teamArabia.setHasTech( iBronzeCasting, True, iCiv, False, False )
			teamArabia.setHasTech( iArchitecture, True, iCiv, False, False )
			teamArabia.setHasTech( iLiterature, True, iCiv, False, False )
			teamArabia.setHasTech( iMonasticism, True, iCiv, False, False )
			teamArabia.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamArabia.setHasTech( iHerbalMedicine, True, iCiv, False, False )
			teamArabia.setHasTech( iAstrolabe, True, iCiv, False, False )
			teamArabia.setHasTech( iArabicKnowledge, True, iCiv, False, False )

		elif ( iCiv == iBulgaria ):
			teamBulgaria.setHasTech( iTheology, True, iCiv, False, False )
			teamBulgaria.setHasTech( iCalendar, True, iCiv, False, False )
			teamBulgaria.setHasTech( iStirrup, True, iCiv, False, False )
			teamBulgaria.setHasTech( iArchitecture, True, iCiv, False, False )
			teamBulgaria.setHasTech( iBronzeCasting, True, iCiv, False, False )

		elif ( iCiv == iCordoba ):
			teamCordoba.setHasTech( iTheology, True, iCiv, False, False )
			teamCordoba.setHasTech( iCalendar, True, iCiv, False, False )
			teamCordoba.setHasTech( iLateenSails, True, iCiv, False, False )
			teamCordoba.setHasTech( iStirrup, True, iCiv, False, False )
			teamCordoba.setHasTech( iBronzeCasting, True, iCiv, False, False )
			teamCordoba.setHasTech( iArchitecture, True, iCiv, False, False )
			teamCordoba.setHasTech( iLiterature, True, iCiv, False, False )
			teamCordoba.setHasTech( iMonasticism, True, iCiv, False, False )
			teamCordoba.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamCordoba.setHasTech( iHerbalMedicine, True, iCiv, False, False )
			teamCordoba.setHasTech( iAstrolabe, True, iCiv, False, False )
			teamCordoba.setHasTech( iArabicKnowledge, True, iCiv, False, False )
			teamCordoba.setHasTech( iEngineering, True, iCiv, False, False )
			teamCordoba.setHasTech( iArabicMedicine, True, iCiv, False, False )

		elif ( iCiv == iVenecia ):
			for iTech in range( iStirrup + 1 ):
				teamVenecia.setHasTech( iTech, True, iCiv, False, False )
			teamVenecia.setHasTech( iLateenSails, True, iCiv, False, False )
			teamVenecia.setHasTech( iAstrolabe, True, iCiv, False, False )
			teamVenecia.setHasTech( iMonasticism, True, iCiv, False, False )
			teamVenecia.setHasTech( iMusic, True, iCiv, False, False )
			teamVenecia.setHasTech( iHerbalMedicine, True, iCiv, False, False )
			teamVenecia.setHasTech( iVassalage, True, iCiv, False, False )
			teamVenecia.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamVenecia.setHasTech( iChainMail, True, iCiv, False, False )
			
		elif ( iCiv == iBurgundy ):
			for iTech in range( iStirrup + 1 ):
				teamBurgundy.setHasTech( iTech, True, iCiv, False, False )
			teamBurgundy.setHasTech( iMonasticism, True, iCiv, False, False )
			teamBurgundy.setHasTech( iVassalage, True, iCiv, False, False )
			teamBurgundy.setHasTech( iFeudalism, True, iCiv, False, False )
			teamBurgundy.setHasTech( iFarriers, True, iCiv, False, False )
			teamBurgundy.setHasTech( iArt, True, iCiv, False, False )
			teamBurgundy.setHasTech( iEngineering, True, iCiv, False, False )
			teamBurgundy.setHasTech( iChainMail, True, iCiv, False, False )
			teamBurgundy.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamBurgundy.setHasTech( iAstrolabe, True, iCiv, False, False )

		elif ( iCiv == iGermany ):
			for iTech in range( iStirrup + 1 ):
				teamGermany.setHasTech( iTech, True, iCiv, False, False )
			teamGermany.setHasTech( iMonasticism, True, iCiv, False, False )
			teamGermany.setHasTech( iVassalage, True, iCiv, False, False )
			teamGermany.setHasTech( iFeudalism, True, iCiv, False, False )
			teamGermany.setHasTech( iFarriers, True, iCiv, False, False )
			teamGermany.setHasTech( iArt, True, iCiv, False, False )
			teamGermany.setHasTech( iEngineering, True, iCiv, False, False )
			teamGermany.setHasTech( iMachinery, True, iCiv, False, False )
			teamGermany.setHasTech( iChainMail, True, iCiv, False, False )
			teamGermany.setHasTech( iAristocracy, True, iCiv, False, False )
			teamGermany.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamGermany.setHasTech( iAstrolabe, True, iCiv, False, False )

		elif ( iCiv == iNovgorod ):
			for iTech in range( iStirrup + 1 ):
				teamNovgorod.setHasTech( iTech, True, iCiv, False, False )
			teamNovgorod.setHasTech( iMonasticism, True, iCiv, False, False )
			teamNovgorod.setHasTech( iVassalage, True, iCiv, False, False )
			teamNovgorod.setHasTech( iFeudalism, True, iCiv, False, False )
			teamNovgorod.setHasTech( iFarriers, True, iCiv, False, False )
			teamNovgorod.setHasTech( iChainMail, True, iCiv, False, False )

		elif ( iCiv == iNorway ):
			for iTech in range( iStirrup + 1):
				teamNorway.setHasTech( iTech, True, iCiv, False, False )
			teamNorway.setHasTech( iMonasticism, True, iCiv, False, False )
			teamNorway.setHasTech( iVassalage, True, iCiv, False, False )
			teamNorway.setHasTech( iAstrolabe, True, iCiv, False, False )
			teamNorway.setHasTech( iFarriers, True, iCiv, False, False )
			teamNorway.setHasTech( iChainMail, True, iCiv, False, False )
			teamNorway.setHasTech( iHerbalMedicine, True, iCiv, False, False )

		elif ( iCiv == iKiev ):
			for iTech in range( iStirrup + 1 ):
				teamKiev.setHasTech( iTech, True, iCiv, False, False )
			teamKiev.setHasTech( iMonasticism, True, iCiv, False, False )
			teamKiev.setHasTech( iVassalage, True, iCiv, False, False )
			teamKiev.setHasTech( iFarriers, True, iCiv, False, False )
			teamKiev.setHasTech( iChainMail, True, iCiv, False, False )

		elif ( iCiv == iHungary ):
			for iTech in range( iStirrup + 1 ):
				teamHungary.setHasTech( iTech, True, iCiv, False, False )
			teamHungary.setHasTech( iChainMail, True, iCiv, False, False )
			teamHungary.setHasTech( iArt, True, iCiv, False, False )
			teamHungary.setHasTech( iHerbalMedicine, True, iCiv, False, False )
			teamHungary.setHasTech( iMonasticism, True, iCiv, False, False )
			teamHungary.setHasTech( iVassalage, True, iCiv, False, False )

		elif ( iCiv == iSpain ):
			for iTech in range( iStirrup + 1 ):
				teamSpain.setHasTech( iTech, True, iCiv, False, False )
			teamSpain.setHasTech( iLateenSails, True, iCiv, False, False )
			teamSpain.setHasTech( iAstrolabe, True, iCiv, False, False )
			teamSpain.setHasTech( iMonasticism, True, iCiv, False, False )
			teamSpain.setHasTech( iHerbalMedicine, True, iCiv, False, False )
			teamSpain.setHasTech( iVassalage, True, iCiv, False, False )
			teamSpain.setHasTech( iEngineering, True, iCiv, False, False )
			teamSpain.setHasTech( iMachinery, True, iCiv, False, False )
			teamSpain.setHasTech( iFeudalism, True, iCiv, False, False )
			teamSpain.setHasTech( iChainMail, True, iCiv, False, False )

		elif ( iCiv == iDenmark ):
			for iTech in range( iStirrup + 1):
				teamDenmark.setHasTech( iTech, True, iCiv, False, False )
			teamDenmark.setHasTech( iMonasticism, True, iCiv, False, False )
			teamDenmark.setHasTech( iVassalage, True, iCiv, False, False )
			teamDenmark.setHasTech( iFeudalism, True, iCiv, False, False )
			teamDenmark.setHasTech( iAristocracy, True, iCiv, False, False )
			teamDenmark.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamDenmark.setHasTech( iAstrolabe, True, iCiv, False, False )
			teamDenmark.setHasTech( iFarriers, True, iCiv, False, False )
			teamDenmark.setHasTech( iChainMail, True, iCiv, False, False )
			teamDenmark.setHasTech( iHerbalMedicine, True, iCiv, False, False )

		elif ( iCiv == iScotland ):
			for iTech in range( iStirrup + 1 ):
				teamScotland.setHasTech( iTech, True, iCiv, False, False )
			teamScotland.setHasTech( iLateenSails, True, iCiv, False, False )
			teamScotland.setHasTech( iAstrolabe, True, iCiv, False, False )
			teamScotland.setHasTech( iMonasticism, True, iCiv, False, False )
			teamScotland.setHasTech( iMusic, True, iCiv, False, False )
			teamScotland.setHasTech( iHerbalMedicine, True, iCiv, False, False )
			teamScotland.setHasTech( iVassalage, True, iCiv, False, False )
			teamScotland.setHasTech( iEngineering, True, iCiv, False, False )
			teamScotland.setHasTech( iMachinery, True, iCiv, False, False )
			teamScotland.setHasTech( iFeudalism, True, iCiv, False, False )
			teamScotland.setHasTech( iChainMail, True, iCiv, False, False )
			teamScotland.setHasTech( iAristocracy, True, iCiv, False, False )

		elif ( iCiv == iPoland ):
			for iTech in range( iStirrup + 1 ):
				teamPoland.setHasTech( iTech, True, iCiv, False, False )
			teamPoland.setHasTech( iMonasticism, True, iCiv, False, False )
			teamPoland.setHasTech( iHerbalMedicine, True, iCiv, False, False )
			teamPoland.setHasTech( iVassalage, True, iCiv, False, False )
			teamPoland.setHasTech( iFeudalism, True, iCiv, False, False )
			teamPoland.setHasTech( iFarriers, True, iCiv, False, False )
			teamPoland.setHasTech( iArt, True, iCiv, False, False )
			teamPoland.setHasTech( iEngineering, True, iCiv, False, False )
			teamPoland.setHasTech( iChainMail, True, iCiv, False, False )

		elif ( iCiv == iGenoa ):
			for iTech in range( iStirrup + 1 ):
				teamGenoa.setHasTech( iTech, True, iCiv, False, False )
			teamGenoa.setHasTech( iLateenSails, True, iCiv, False, False )
			teamGenoa.setHasTech( iAstrolabe, True, iCiv, False, False )
			teamGenoa.setHasTech( iMonasticism, True, iCiv, False, False )
			teamGenoa.setHasTech( iMusic, True, iCiv, False, False )
			teamGenoa.setHasTech( iHerbalMedicine, True, iCiv, False, False )
			teamGenoa.setHasTech( iVassalage, True, iCiv, False, False )
			teamGenoa.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamGenoa.setHasTech( iEngineering, True, iCiv, False, False )
			teamGenoa.setHasTech( iMachinery, True, iCiv, False, False )
			teamGenoa.setHasTech( iFeudalism, True, iCiv, False, False )
			teamGenoa.setHasTech( iVaultedArches, True, iCiv, False, False )
			teamGenoa.setHasTech( iChainMail, True, iCiv, False, False )
			teamGenoa.setHasTech( iAristocracy, True, iCiv, False, False )

		elif ( iCiv == iMorocco ):
			for iTech in range( iFarriers + 1 ):
				teamMorocco.setHasTech( iTech, True, iCiv, False, False )
			teamMorocco.setHasTech( iBlastFurnace, True, iCiv, False, False )
			teamMorocco.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamMorocco.setHasTech( iLateenSails, True, iCiv, False, False )
			teamMorocco.setHasTech( iMapMaking, True, iCiv, False, False )
			teamMorocco.setHasTech( iArabicKnowledge, True, iCiv, False, False )

		elif ( iCiv == iEngland ):
			for iTech in range( iFarriers + 1 ):
				teamEngland.setHasTech( iTech, True, iCiv, False, False )
			teamEngland.setHasTech( iBlastFurnace, True, iCiv, False, False )
			teamEngland.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamEngland.setHasTech( iAristocracy, True, iCiv, False, False )

		elif ( iCiv == iPortugal ):
			for iTech in range( iFarriers + 1 ):
				teamPortugal.setHasTech( iTech, True, iCiv, False, False )
			teamPortugal.setHasTech( iBlastFurnace, True, iCiv, False, False )
			teamPortugal.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamPortugal.setHasTech( iLiterature, True, iCiv, False, False )
			teamPortugal.setHasTech( iLateenSails, True, iCiv, False, False )
			teamPortugal.setHasTech( iMapMaking, True, iCiv, False, False )
			teamPortugal.setHasTech( iAristocracy, True, iCiv, False, False )

		elif ( iCiv == iAragon ):
			for iTech in range( iFarriers + 1 ):
				teamAragon.setHasTech( iTech, True, iCiv, False, False )
			teamAragon.setHasTech( iBlastFurnace, True, iCiv, False, False )
			teamAragon.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamAragon.setHasTech( iLiterature, True, iCiv, False, False )
			teamAragon.setHasTech( iLateenSails, True, iCiv, False, False )
			teamAragon.setHasTech( iMapMaking, True, iCiv, False, False )
			teamAragon.setHasTech( iAristocracy, True, iCiv, False, False )
			teamAragon.setHasTech( iPlateArmor, True, iCiv, False, False )
			teamAragon.setHasTech( iGothicArchitecture, True, iCiv, False, False )
			teamAragon.setHasTech( iSiegeEngines, True, iCiv, False, False )

		elif ( iCiv == iSweden ):
			for iTech in range( iFarriers + 1 ):
				teamSweden.setHasTech( iTech, True, iCiv, False, False )
			teamSweden.setHasTech( iBlastFurnace, True, iCiv, False, False )
			teamSweden.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamSweden.setHasTech( iGothicArchitecture, True, iCiv, False, False )
			teamSweden.setHasTech( iChivalry, True, iCiv, False, False )
			teamSweden.setHasTech( iAristocracy, True, iCiv, False, False )
			teamSweden.setHasTech( iPlateArmor, True, iCiv, False, False )
			teamSweden.setHasTech( iSiegeEngines, True, iCiv, False, False )
			teamSweden.setHasTech( iLateenSails, True, iCiv, False, False )
			teamSweden.setHasTech( iLiterature, True, iCiv, False, False )
			teamSweden.setHasTech( iClassicalKnowledge, True, iCiv, False, False )
			teamSweden.setHasTech( iMonumentBuilding, True, iCiv, False, False )
			teamSweden.setHasTech( iPhilosophy, True, iCiv, False, False )
			teamSweden.setHasTech( iMapMaking, True, iCiv, False, False )

		elif ( iCiv == iPrussia ):
			for iTech in range( iFarriers + 1 ):
				teamPrussia.setHasTech( iTech, True, iCiv, False, False )
			teamPrussia.setHasTech( iBlastFurnace, True, iCiv, False, False )
			teamPrussia.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamPrussia.setHasTech( iGothicArchitecture, True, iCiv, False, False )
			teamPrussia.setHasTech( iChivalry, True, iCiv, False, False )
			teamPrussia.setHasTech( iAristocracy, True, iCiv, False, False )
			teamPrussia.setHasTech( iPlateArmor, True, iCiv, False, False )
			teamPrussia.setHasTech( iSiegeEngines, True, iCiv, False, False )
			teamPrussia.setHasTech( iAlchemy, True, iCiv, False, False )
			teamPrussia.setHasTech( iCivilService, True, iCiv, False, False )
			teamPrussia.setHasTech( iLateenSails, True, iCiv, False, False )
			teamPrussia.setHasTech( iGuilds, True, iCiv, False, False )
			teamPrussia.setHasTech( iLiterature, True, iCiv, False, False )
			teamPrussia.setHasTech( iClassicalKnowledge, True, iCiv, False, False )
			teamPrussia.setHasTech( iMonumentBuilding, True, iCiv, False, False )
			teamPrussia.setHasTech( iPhilosophy, True, iCiv, False, False )

		elif ( iCiv == iLithuania ):
			for iTech in range( iFarriers + 1 ):
				teamLithuania.setHasTech( iTech, True, iCiv, False, False )
			teamLithuania.setHasTech( iBlastFurnace, True, iCiv, False, False )
			teamLithuania.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamLithuania.setHasTech( iGothicArchitecture, True, iCiv, False, False )
			teamLithuania.setHasTech( iAristocracy, True, iCiv, False, False )
			teamLithuania.setHasTech( iCivilService, True, iCiv, False, False )
			teamLithuania.setHasTech( iSiegeEngines, True, iCiv, False, False )
			teamLithuania.setHasTech( iLiterature, True, iCiv, False, False )
			teamLithuania.setHasTech( iAlchemy, True, iCiv, False, False )
			teamLithuania.setHasTech( iClassicalKnowledge, True, iCiv, False, False )
			teamLithuania.setHasTech( iPlateArmor, True, iCiv, False, False )
			teamLithuania.setHasTech( iLateenSails, True, iCiv, False, False )
			teamLithuania.setHasTech( iMonumentBuilding, True, iCiv, False, False )
			teamLithuania.setHasTech( iCivilService, True, iCiv, False, False )

		elif ( iCiv == iAustria ):
			for iTech in range( iFarriers + 1 ):
				teamAustria.setHasTech( iTech, True, iCiv, False, False )
			teamAustria.setHasTech( iBlastFurnace, True, iCiv, False, False )
			teamAustria.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamAustria.setHasTech( iGothicArchitecture, True, iCiv, False, False )
			teamAustria.setHasTech( iChivalry, True, iCiv, False, False )
			teamAustria.setHasTech( iAristocracy, True, iCiv, False, False )
			teamAustria.setHasTech( iPlateArmor, True, iCiv, False, False )
			teamAustria.setHasTech( iSiegeEngines, True, iCiv, False, False )
			teamAustria.setHasTech( iAlchemy, True, iCiv, False, False )
			teamAustria.setHasTech( iCivilService, True, iCiv, False, False )
			teamAustria.setHasTech( iLateenSails, True, iCiv, False, False )
			teamAustria.setHasTech( iGuilds, True, iCiv, False, False )
			teamAustria.setHasTech( iLiterature, True, iCiv, False, False )
			teamAustria.setHasTech( iClassicalKnowledge, True, iCiv, False, False )
			teamAustria.setHasTech( iMonumentBuilding, True, iCiv, False, False )
			teamAustria.setHasTech( iPhilosophy, True, iCiv, False, False )
			teamAustria.setHasTech( iEducation, True, iCiv, False, False )

		elif ( iCiv == iTurkey ):
			for iTech in range( iChivalry + 1 ):
				teamTurkey.setHasTech( iTech, True, iCiv, False, False )
			teamTurkey.setHasTech( iGunpowder, True, iCiv, False, False )
			teamTurkey.setHasTech( iMilitaryTradition, True, iCiv, False, False )
			teamTurkey.setHasTech( iArabicKnowledge, True, iCiv, False, False )

		elif ( iCiv == iMoscow ):
			for iTech in range( iFarriers + 1 ):
				teamMoscow.setHasTech( iTech, True, iCiv, False, False )
			teamMoscow.setHasTech( iBlastFurnace, True, iCiv, False, False )
			teamMoscow.setHasTech( iCodeOfLaws, True, iCiv, False, False )
			teamMoscow.setHasTech( iGothicArchitecture, True, iCiv, False, False )
			teamMoscow.setHasTech( iChivalry, True, iCiv, False, False )
			teamMoscow.setHasTech( iAristocracy, True, iCiv, False, False )
			teamMoscow.setHasTech( iCivilService, True, iCiv, False, False )
			teamMoscow.setHasTech( iLiterature, True, iCiv, False, False )
			teamMoscow.setHasTech( iMonumentBuilding, True, iCiv, False, False )
			teamMoscow.setHasTech( iPlateArmor, True, iCiv, False, False )
			teamMoscow.setHasTech( iSiegeEngines, True, iCiv, False, False )
			teamMoscow.setHasTech( iLateenSails, True, iCiv, False, False )
			teamMoscow.setHasTech( iMapMaking, True, iCiv, False, False )
			teamMoscow.setHasTech( iClassicalKnowledge, True, iCiv, False, False )
			teamMoscow.setHasTech( iClockmaking, True, iCiv, False, False )
			teamMoscow.setHasTech( iAlchemy, True, iCiv, False, False )
			teamMoscow.setHasTech( iGuilds, True, iCiv, False, False )
			teamMoscow.setHasTech( iPhilosophy, True, iCiv, False, False )
			teamMoscow.setHasTech( iReplaceableParts, True, iCiv, False, False )

		elif ( iCiv == iDutch ):
			for iTech in range( iAstronomy + 1 ):
				teamDutch.setHasTech( iTech, True, iCiv, False, False )

		self.hitNeighboursStability(iCiv)


	def hitNeighboursStability( self, iCiv ):
		# 3Miro: Stability on Spawn
		if (len(lOlderNeighbours[iCiv]) > 0):
		#	print "Got inside hitStability!!!"
			bHuman = False
			#for iLoop in lOlderNeighbours[iCiv]:
				#if (gc.getPlayer(iLoop).isAlive()):
				##	print("iLoop =",iLoop)
					#if (iLoop == utils.getHumanID()):
						#bHuman = True
					#utils.setStabilityParameters(iLoop, iParDiplomacyE, utils.getStabilityParameters(iLoop, iParDiplomacyE)-5)
					#utils.setStability(iLoop, utils.getStability(iLoop)-5)


	def showRect( self, iCiv, iXs, iYs, iXe, iYe ):
		for iX in range( iXs, iXe + 1 ):
			for iY in range( iYs, iYe + 1 ):
				gc.getMap().plot(iX, iY).setRevealed(gc.getPlayer(iCiv).getTeam(), True, False, -1)


	def showArea(self, iCiv, iScenario = i500ADScenario):
		#print(" Visible for: ",iCiv )
		for iI in range( len( tVisible[iScenario][iCiv] ) ):
			self.showRect( iCiv, tVisible[iScenario][iCiv][iI][0], tVisible[iScenario][iCiv][iI][1], tVisible[iScenario][iCiv][iI][2], tVisible[iScenario][iCiv][iI][3] )
		#print(" Visible for: ",iCiv )
		#pass


	def initContact(self, iCiv , bMeet = True):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		for iOtherPlayer in lInitialContacts[utils.getScenario()][iCiv]:
			pOtherPlayer = gc.getPlayer(iOtherPlayer)
			tOtherPlayer = pOtherPlayer.getTeam()
			if pOtherPlayer.isAlive() and not teamCiv.isHasMet(tOtherPlayer):
				teamCiv.meet(tOtherPlayer, bMeet)

	def LeaningTowerGP(self):
		iGP = gc.getGame().getSorenRandNum(7, 'starting count')
		pFlorentia = gc.getMap().plot(54, 32).getPlotCity()
		iSpecialist = iGreatProphet + iGP
		pFlorentia.setFreeSpecialistCount(iSpecialist, 1)

	def setDiplo1200AD(self):
		self.changeAttitudeExtra(iByzantium, iArabia, -2)
		self.changeAttitudeExtra(iScotland, iFrankia, 4)

	def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):	
		gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
		gc.getPlayer(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)