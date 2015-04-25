# Rhye's and Fall of Civilization - Utilities

from CvPythonExtensions import *
import CvUtil
import CvScreenEnums #Absinhe
import RFCEMaps #Absinthe
import PyHelpers
import Popup #Absinthe
import Consts as con
import XMLConsts as xml
import cPickle as pickle

# globals
gc = CyGlobalContext()
localText = CyTranslator() #Absinthe
PyPlayer = PyHelpers.PyPlayer

iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNumTotalPlayers = con.iNumTotalPlayers
iBarbarian = con.iBarbarian

iSettler = xml.iSettler

iNumBuildingsPlague = xml.iNumBuildingsPlague

tCol = (
'255,255,255',
'200,200,200',
'150,150,150',
'128,128,128')

iScreenIsUp = 0
iSelectedCivID = -1

class RFCUtils:

	#Absinthe: stability overlay
	bStabilityOverlay = False

	#RiseAndFall, Stability
	def getLastTurnAlive( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lLastTurnAlive'][iCiv]

	def setLastTurnAlive( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lLastTurnAlive'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	#Victory
	#def getGoal( self, i, j ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#return scriptDict['lGoals'][i][j]

	#def setGoal( self, i, j, iNewValue ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#scriptDict['lGoals'][i][j] = iNewValue
		#gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	#Stability
	def getTempFlippingCity( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['tempFlippingCity']

	def setTempFlippingCity( self, tNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['tempFlippingCity'] = tNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getStability( self, iCiv ):
		return gc.getPlayer( iCiv ).getStability()

	#def setStability( self, iCiv, iNewValue ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#scriptDict['lStability'][iCiv] = iNewValue
		#gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	#def getBaseStabilityLastTurn( self, iCiv ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#return scriptDict['lBaseStabilityLastTurn'][iCiv]

	#def setBaseStabilityLastTurn( self, iCiv, iNewValue ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#scriptDict['lBaseStabilityLastTurn'][iCiv] = iNewValue
		#gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	#def getStabilityParameters( self, iCiv, iParameter ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#return scriptDict['lStabilityParameters'][iCiv][iParameter]

	#def setStabilityParameters( self, iCiv,iParameter, iNewValue ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#scriptDict['lStabilityParameters'][iCiv][iParameter] = iNewValue
		#gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	#def getGreatDepressionCountdown( self, iCiv ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#return scriptDict['lGreatDepressionCountdown'][iCiv]

	#def setGreatDepressionCountdown( self, iCiv, iNewValue ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#scriptDict['lGreatDepressionCountdown'][iCiv] = iNewValue
		#gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	#def getLastRecordedStabilityStuff( self, iParameter ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#return scriptDict['lLastRecordedStabilityStuff'][iParameter]

	#def setLastRecordedStabilityStuff( self, iParameter, iNewValue ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#scriptDict['lLastRecordedStabilityStuff'][iParameter] = iNewValue
		#gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getProsecutionCount( self, iCiv ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#return scriptDict['iProsecutionCount'][iCiv]
		return gc.getProsecutionCount( iCiv )

	def setProsecutionCount( self, iCiv, iNewValue ):
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#scriptDict['iProsecutionCount'][iCiv] = iNewValue
		#gc.getGame().setScriptData( pickle.dumps(scriptDict) )
		gc.setProsecutionCount( iCiv, iNewValue )

	#Plague
	def getPlagueCountdown( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lPlagueCountdown'][iCiv]

	def setPlagueCountdown( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lPlagueCountdown'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getSeed( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['iSeed']

#######################################

	#Stability, RiseNFall, CvFinanceAdvisor
	#def setParameter(self, iPlayer, iParameter, bPreviousAmount, iAmount):
		#if (bPreviousAmount):
			#self.setStabilityParameters(iPlayer, iParameter, self.getStabilityParameters(iPlayer,iParameter) + iAmount)
		#else:
			#self.setStabilityParameters(iPlayer, iParameter, 0 + iAmount)

	## 3Miro: for numbers in the stability screen
	#def getParString( self, iPlayer, iCathegory ):
		#if ( gc.getPlayer(iPlayer).isHuman()):
			#if ( iCathegory == 0 ):
				#sString = "%i | %i" %( self.getStabilityParameters(iPlayer, con.iParCitiesE), self.getStabilityParameters(iPlayer,con.iParCities3) )
			#elif ( iCathegory == 1 ):
				#sString = "%i | %i | %i" %(self.getStabilityParameters(iPlayer, con.iParCivicsE), self.getStabilityParameters(iPlayer, con.iParCivics3), self.getStabilityParameters(iPlayer, con.iParCivics1) )
			#elif ( iCathegory == 2 ):
				#sString = "%i | %i | %i" %(self.getStabilityParameters(iPlayer, con.iParEconomyE), self.getStabilityParameters(iPlayer, con.iParEconomy3), self.getStabilityParameters(iPlayer, con.iParEconomy1) )
			#elif ( iCathegory == 3 ):
				#sString = "%i | %i | %i" %(self.getStabilityParameters(iPlayer, con.iParExpansionE), self.getStabilityParameters(iPlayer, con.iParExpansion3), self.getStabilityParameters(iPlayer, con.iParExpansion1) )
			#elif ( iCathegory == 4 ):
				#sString = "%i | %i" %(self.getStabilityParameters(iPlayer, con.iParDiplomacyE), self.getStabilityParameters(iPlayer, con.iParDiplomacy3) )
			#else:
				#sString = ""
		#else:
			#sString = ""
		#return sString

	##CvFinanceAdvisor
	#def getParCities(self,iCiv):
		#if (self.getStabilityParameters(iCiv,con.iParCitiesE) > 7):
			#return self.getStabilityParameters(iCiv,con.iParCities3) + self.getStabilityParameters(iCiv,con.iParCitiesE)
		#elif (self.getStabilityParameters(iCiv, con.iParCitiesE) < -7):
			#return self.getStabilityParameters(iCiv,con.iParCities3) + self.getStabilityParameters(iCiv,con.iParCitiesE)
		#else:
			#return self.getStabilityParameters(iCiv,con.iParCities3) + self.getStabilityParameters(iCiv,con.iParCitiesE)

	#def getParCivics(self,iCiv):
		#if (self.getStabilityParameters(iCiv, con.iParCivicsE) > 7):
			#return self.getStabilityParameters(iCiv, con.iParCivics3) + self.getStabilityParameters(iCiv, con.iParCivics1) + self.getStabilityParameters(iCiv, con.iParCivicsE)
		#elif (self.getStabilityParameters(iCiv, con.iParCivicsE) < -7):
			#return self.getStabilityParameters(iCiv, con.iParCivics3) + self.getStabilityParameters(iCiv, con.iParCivics1) + self.getStabilityParameters(iCiv, con.iParCivicsE)
		#else:
			#return self.getStabilityParameters(iCiv, con.iParCivics3) + self.getStabilityParameters(iCiv, con.iParCivics1) + self.getStabilityParameters(iCiv, con.iParCivicsE)

	#def getParDiplomacy(self,iCiv):
		#if (self.getStabilityParameters(iCiv, con.iParDiplomacyE) > 7):
			#return self.getStabilityParameters(iCiv, con.iParDiplomacy3) + self.getStabilityParameters(iCiv, con.iParDiplomacyE)
		#elif (self.getStabilityParameters(iCiv, con.iParDiplomacyE) < -7):
			#return self.getStabilityParameters(iCiv, con.iParDiplomacy3) + self.getStabilityParameters(iCiv, con.iParDiplomacyE)
		#else:
			#return self.getStabilityParameters(iCiv, con.iParDiplomacy3) + self.getStabilityParameters(iCiv, con.iParDiplomacyE)

	#def getParEconomy(self, iCiv):
		##print ("ECO", self.getStabilityParameters(con.iParEconomy3), self.getStabilityParameters(con.iParEconomy1), self.getStabilityParameters(con.iParEconomyE))
		#if (self.getStabilityParameters(iCiv, con.iParEconomyE) > 7):
			#return self.getStabilityParameters(iCiv, con.iParEconomy3) + self.getStabilityParameters(iCiv, con.iParEconomy1) + self.getStabilityParameters(iCiv, con.iParEconomyE)
		#elif (self.getStabilityParameters(iCiv, con.iParEconomyE) < -7):
			#return self.getStabilityParameters(iCiv, con.iParEconomy3) + self.getStabilityParameters(iCiv, con.iParEconomy1) + self.getStabilityParameters(iCiv, con.iParEconomyE)
		#else:
			#return self.getStabilityParameters(iCiv, con.iParEconomy3) + self.getStabilityParameters(iCiv, con.iParEconomy1) + self.getStabilityParameters(iCiv, con.iParEconomyE)

	#def getParExpansion(self, iCiv):
		#if (self.getStabilityParameters(iCiv, con.iParExpansionE) > 7):
			#return self.getStabilityParameters(iCiv, con.iParExpansion3) + self.getStabilityParameters(iCiv, con.iParExpansion1) + self.getStabilityParameters(iCiv, con.iParExpansionE)
		#elif (self.getStabilityParameters(iCiv, con.iParExpansionE) < -7):
			#return self.getStabilityParameters(iCiv, con.iParExpansion3) + self.getStabilityParameters(iCiv, con.iParExpansion1) + self.getStabilityParameters(iCiv, con.iParExpansionE)
		#else:
			#return self.getStabilityParameters(iCiv, con.iParExpansion3) + self.getStabilityParameters(iCiv, con.iParExpansion1) + self.getStabilityParameters(iCiv, con.iParExpansionE)

	#def getArrow(self, iParameter):
		#if (iParameter == 0):
			#if (self.getStability(self.getHumanID()) >= self.getLastRecordedStabilityStuff(iParameter) + 6):
				#return 1
			#elif (self.getStability(self.getHumanID()) <= self.getLastRecordedStabilityStuff(iParameter) - 6):
				#return -1
			#else:
				#return 0
		#else:
			#if (iParameter == 1):
				#iNewValue = self.getParCities()
			#elif (iParameter == 2):
				#iNewValue = self.getParCivics()
			#elif (iParameter == 3):
				#iNewValue = self.getParEconomy()
			#elif (iParameter == 4):
				#iNewValue = self.getParExpansion()
			#elif (iParameter == 5):
				#iNewValue = self.getParDiplomacy()
			#if (iNewValue >= self.getLastRecordedStabilityStuff(iParameter) + 4):
				#return 1
			#elif (iNewValue <= self.getLastRecordedStabilityStuff(iParameter) - 4):
				#return -1
			#else:
				#return 0

	#Victory
	def countAchievedGoals(self, iPlayer):
		pPlayer = gc.getPlayer( iPlayer )
		iResult = 0
		for j in range(3):
			iTemp = pPlayer.getUHV( j )
			if (iTemp < 0):
				iTemp = 0
			iResult += iTemp
			#if (self.getGoal(iPlayer, j) == 1):
			#	iResult += 1
		return iResult

	def getGoalsColor(self, iPlayer): #by CyberChrist
		pPlayer = gc.getPlayer( iPlayer )
		iCol = 0
		for j in range(3):
			if (pPlayer.getUHV( j ) == 0):
				iCol += 1
		return tCol[iCol]

	# 3Miro: BEGIN Utilities for the extra UHV info
	def getBurgundyCulture( self ):
		return 0
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#if ( scriptDict['lGoals'][con.iBurgundy][1] == -1 ):
		#	return scriptDict['iBurgundyCulture']
		#else:
		#	return -1

	def getArabianInfluence( self ):
		return 0
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#if ( scriptDict['lGoals'][con.iArabia][1] == -1 ):
		#	return gc.getGame().calculateReligionPercent( xml.iIslam )
		#else:
		#	return -1

	def getNorseRazed( self ):
		return 0
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#if ( scriptDict['lGoals'][con.iNorse][1] == -1 ):
		#	return scriptDict['iNorseRazed']
		#else:
		#	return -1

	def getKievFood( self ):
		return 0
		#scriptDict = pickle.loads( gc.getGame().getScriptData() )
		#if ( scriptDict['lGoals'][con.iKiev][0] == -1 ):
		#	return scriptDict['iKievFood']
		#else:
		#	return -1
	# 3Miro: END Utilities


	#Plague
	def getRandomCity(self, iPlayer):
		cityList = []
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			cityList.append(pCity.GetCy())
		if (len(cityList)):
			return cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')]
		else:
			return -1

	def getRandomCiv( self ):
		civList = []
		for i in range( iNumPlayers ):
			if ( gc.getPlayer( i ).isAlive() ):
				civList.append( i )
		return civList[gc.getGame().getSorenRandNum(len(civList), 'random civ')]

	def isMortalUnit(self, unit):
		if (unit.isHasPromotion(42)): #leader
			if (not gc.getPlayer(unit.getOwner()).isHuman()):
				return False
		iUnitType = unit.getUnitType()
		if (iUnitType >= xml.iProphet ):
			return False
		return True

	def isDefenderUnit(self, unit):
		return False

	#AIWars
	def checkUnitsInEnemyTerritory(self, iCiv1, iCiv2):
		unitList = PyPlayer(iCiv1).getUnitList()
		if(len(unitList)):
			for unit in unitList:
				iX = unit.getX()
				iY = unit.getY()
				if (gc.getMap().plot( iX, iY ).getOwner() == iCiv2):
					return True
		return False

	#AIWars
	def restorePeaceAI(self, iMinorCiv, bOpenBorders):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for iActiveCiv in range( iNumActivePlayers ):
			if (gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman()):
				if (teamMinor.isAtWar(iActiveCiv)):
					bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
					bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)
					if (not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory):
						teamMinor.makePeace(iActiveCiv)
						if (bOpenBorders):
							teamMinor.signOpenBorders(iActiveCiv)

	#AIWars
	def restorePeaceHuman(self, iMinorCiv, bOpenBorders):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for iActiveCiv in range( iNumActivePlayers ):
			if (gc.getPlayer(iActiveCiv).isHuman()):
				if (gc.getPlayer(iActiveCiv).isAlive()):
					if (teamMinor.isAtWar(iActiveCiv)):
						bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
						bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)
						if (not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory):
							teamMinor.makePeace(iActiveCiv)
				return

	#AIWars
	def minorWars(self, iMinorCiv):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		apCityList = PyPlayer(iMinorCiv).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			x = city.getX()
			y = city.getY()
			for iActiveCiv in range( iNumActivePlayers ):
				# 3MiroPapal: the Pope does not attack independent
				if ( gc.getPlayer(iActiveCiv).isAlive() and (not gc.getPlayer(iActiveCiv).isHuman()) and (not iActiveCiv == con.iPope) ):
					if (gc.getPlayer(iActiveCiv).getSettlersMaps( con.iMapMaxY-y-1, x ) >= 90):
						if (not teamMinor.isAtWar(iActiveCiv)):
							teamMinor.declareWar(iActiveCiv, False, WarPlanTypes.WARPLAN_LIMITED)
							print ("Minor war", city.getName(), gc.getPlayer(iActiveCiv).getCivilizationAdjective(0))


	#RiseAndFall, Stability
	def calculateDistance(self, x1, y1, x2, y2):
		dx = abs(x2-x1)
		dy = abs(y2-y1)
		return max(dx, dy)

	#RiseAndFall
	def debugTextPopup(self, strText):
		popup = Popup.PyPopup()
		popup.setBodyString( strText )
		popup.launch()

	#RiseAndFall
	def updateMinorTechs( self, iMinorCiv, iMajorCiv):
		for t in range(xml.iNumTechs):
			if (gc.getTeam(gc.getPlayer(iMajorCiv).getTeam()).isHasTech(t)):
				    gc.getTeam(gc.getPlayer(iMinorCiv).getTeam()).setHasTech(t, True, iMinorCiv, False, False)

	#RiseAndFall, Religions, UniquePowers
	def makeUnit(self, iUnit, iPlayer, tCoords, iNum): #by LOQ
		'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
		#if ( tCoords[0] < 0 or tCoords[0] >= con.iMapMaxX or tCoords[1] < 0 or tCoords[1] >= con.iMapMaxY ):
		#	print(" MAKING UNIT OFF THE FACE OF EUROPE: ",tCoords )
		pPlayer = gc.getPlayer(iPlayer)
		for i in range(iNum):
			#print(" 3Miro: Making units for Player: ",iPlayer)
			#if ( player == ObjectNone ):
			#	print(" 3Miro: Error: ",iPlayer)
			pPlayer.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	#RiseAndFall, Religions
	def getHumanID(self):
##		for iCiv in range(iNumPlayers):
##			if (gc.getPlayer(iCiv).isHuman()):
##				return iCiv
		return gc.getGame().getActivePlayer()

	#RiseAndFall
	def flipUnitsInCityBefore(self, tCityPlot, iNewOwner, iOldOwner):
		#print ("tCityPlot Before", tCityPlot)
		plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
		city = plotCity.getPlotCity()
		iNumUnitsInAPlot = plotCity.getNumUnits()
		j = 0
		for i in range(iNumUnitsInAPlot):
			unit = plotCity.getUnit(j)
			unitType = unit.getUnitType()
			if (unit.getOwner() == iOldOwner):
				unit.kill(False, con.iBarbarian)
				if (iNewOwner < con.iNumActivePlayers or unitType > xml.iSettler):
					# 3Miro: 0, 72 change, see below
					self.makeUnit(unitType, iNewOwner, [0, 72], 1)
			else:
				j += 1

	#RiseAndFall
	def flipUnitsInCityAfter(self, tCityPlot, iCiv):
		#moves new units back in their place
		#print ("tCityPlot After", tCityPlot)
		tempPlot = gc.getMap().plot(0,72)
		if (tempPlot.getNumUnits() != 0):
			iNumUnitsInAPlot = tempPlot.getNumUnits()
			#print ("iNumUnitsInAPlot", iNumUnitsInAPlot)
			for i in range(iNumUnitsInAPlot):
				unit = tempPlot.getUnit(0)
				#print("  3Miro Unit Type and Owner ",unit.getUnitType(),"  ",unit.getOwner() )
				unit.setXYOld(tCityPlot[0],tCityPlot[1])
		#cover plots revealed
		#gc.getMap().plot(0, 67).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(0, 66).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(1, 66).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(1, 67).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(123, 67).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(123, 66).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(2, 67).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(2, 66).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(2, 65).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(1, 65).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(0, 65).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(122, 67).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(122, 66).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(122, 65).setRevealed(iCiv, False, True, -1);
		#gc.getMap().plot(123, 65).setRevealed(iCiv, False, True, -1);
		# 3Miro: wierd unit creation, see below
		gc.getMap().plot(0, 72).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(0, 71).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(1, 72).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(1, 71).setRevealed(iCiv, False, True, -1);

	def killUnitsInArea(self, tTopLeft, tBottomRight, iCiv):
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				killPlot = gc.getMap().plot(x,y)
				iNumUnitsInAPlot = killPlot.getNumUnits()
				if (iNumUnitsInAPlot):
					for i in range(iNumUnitsInAPlot):
						unit = killPlot.getUnit(0)
						if (unit.getOwner() == iCiv):
							unit.kill(False, con.iBarbarian)

	#RiseAndFall
	# 3Miro: why create units at (0, 67), have seen it in other places.
	# Multiple civs may have units in those tiles, still maybe better to check in a unit can be created in the tile before it is created
	def flipUnitsInArea(self, tTopLeft, tBottomRight, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
		"""Deletes, recreates units in 0,67 and moves them to the previous tile.
		If there are units belonging to others in that plot and the new owner is barbarian, the units aren't recreated.
		Settlers aren't created.
		If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
		# 3Miro: begin - ARGHHHHHHHHHHHHHHHHHHH
		# if a city is flipped that is at the edge of the map, then this will get called for (x,y) > map_size leaving Units off the edge of the screen
		# basically units will be falling off the edge of the map without kill(...), so next time the Unit is accessed and called for plot() the game crashes
		ttTopLeft0 = max( tTopLeft[0], 0 )
		ttBottomRight0 = min( tBottomRight[0], con.iMapMaxX-1 )
		ttTopLeft1 = max( tTopLeft[1], 0 )
		ttBottomRight1 = min( tBottomRight[1], con.iMapMaxY-1 )
		# 3Miro: end - ARGHHHHHHHHHHHHHHHHHHH
		for x in range(ttTopLeft0, ttBottomRight0+1):
			for y in range(ttTopLeft1, ttBottomRight1+1):
				killPlot = gc.getMap().plot(x,y)
				iNumUnitsInAPlot = killPlot.getNumUnits()
				if (iNumUnitsInAPlot):
					bRevealedZero = False
					if (gc.getMap().plot(0, 72).isRevealed(iNewOwner, False)):
						bRevealedZero = True
					#print ("killplot", x, y)
					if (bSkipPlotCity == True) and (killPlot.isCity()):
						#print (killPlot.isCity())
						#print 'do nothing'
						pass
					else:
						j = 0
						for i in range(iNumUnitsInAPlot):
							unit = killPlot.getUnit(j)
							#print ("killplot", x, y, unit.getUnitType(), unit.getOwner(), "j", j)
							if (unit.getOwner() == iOldOwner):
								unit.kill(False, con.iBarbarian)
								if (bKillSettlers):
									if ((unit.getUnitType() > iSettler)):
										self.makeUnit(unit.getUnitType(), iNewOwner, [0, 72], 1)
								else:
									if ((unit.getUnitType() >= iSettler)): #skip animals
										self.makeUnit(unit.getUnitType(), iNewOwner, [0, 72], 1)
							else:
								j += 1
						tempPlot = gc.getMap().plot(0,72)
						#moves new units back in their place
						if (tempPlot.getNumUnits() != 0):
							iNumUnitsInAPlot = tempPlot.getNumUnits()
							for i in range(iNumUnitsInAPlot):
								unit = tempPlot.getUnit(0)
								#print("  3Miro 1 Unit Type and Owner plot ",unit.getID(),unit.getUnitType(),"  ",unit.getOwner(),x,y )
								unit.setXYOld(x,y)
							iCiv = iNewOwner
							if (bRevealedZero == False):
								#gc.getMap().plot(0, 67).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(0, 66).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(1, 66).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(1, 67).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(123, 67).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(123, 66).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(2, 67).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(2, 66).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(2, 65).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(1, 65).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(0, 65).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(122, 67).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(122, 66).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(122, 65).setRevealed(iCiv, False, True, -1);
								#gc.getMap().plot(123, 65).setRevealed(iCiv, False, True, -1);
								gc.getMap().plot(0, 72).setRevealed(iCiv, False, True, -1);
								gc.getMap().plot(0, 71).setRevealed(iCiv, False, True, -1);
								gc.getMap().plot(1, 72).setRevealed(iCiv, False, True, -1);
								gc.getMap().plot(1, 71).setRevealed(iCiv, False, True, -1);


	#RiseAndFall
	def flipCity(self, tCityPlot, bFlipType, bKillUnits, iNewOwner, iOldOwners):
		"""Changes owner of city specified by tCityPlot.
		bFlipType specifies if it's conquered or traded.
		If bKillUnits != 0 all the units in the city will be killed.
		iRetainCulture will determine the split of the current culture between old and new owner. -1 will skip
		iOldOwners is a list. Flip happens only if the old owner is in the list.
		An empty list will cause the flip to always happen."""
		pNewOwner = gc.getPlayer(iNewOwner)
		city = gc.getMap().plot(tCityPlot[0], tCityPlot[1]).getPlotCity()
		if (gc.getMap().plot(tCityPlot[0], tCityPlot[1]).isCity()):
			if not city.isNone():
				iOldOwner = city.getOwner()
				if (iOldOwner in iOldOwners or not iOldOwners):
					if (bKillUnits):
						killPlot = gc.getMap().plot( tCityPlot[0], tCityPlot[1] )
						for i in range(killPlot.getNumUnits()):
							unit = killPlot.getUnit(0)
							unit.kill(False, iNewOwner)
					if (bFlipType): #conquest
						if (city.getPopulation() == 2):
							city.setPopulation(3)
						if (city.getPopulation() == 1):
							city.setPopulation(2)
						pNewOwner.acquireCity(city, True, False)
					else: #trade
						pNewOwner.acquireCity(city, False, True)
					return True
		return False


	#RiseAndFall
	def cultureManager(self, tCityPlot, iCulturePercent, iNewOwner, iOldOwner, bBarbarian2x2Decay, bBarbarian2x2Conversion, bAlwaysOwnPlots):
		"""Converts the culture of the city and of the surrounding plots to the new owner of a city.
		iCulturePercent determine the percentage that goes to the new owner.
		If old owner is barbarian, all the culture is converted"""

		pCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
		city = pCity.getPlotCity()

		#city
		if (pCity.isCity()):
			iCurrentCityCulture = city.getCulture(iOldOwner)
			city.setCulture(iOldOwner, iCurrentCityCulture*(100-iCulturePercent)/100, False)
			if (iNewOwner != con.iBarbarian):
				city.setCulture(con.iBarbarian, 0, True)
			city.setCulture(iNewOwner, iCurrentCityCulture*iCulturePercent/100, False)
			if (city.getCulture(iNewOwner) <= 10):
				city.setCulture(iNewOwner, 20, False)

		#halve barbarian culture in a broader area
		if (bBarbarian2x2Decay or bBarbarian2x2Conversion):
			if (iNewOwner != con.iBarbarian and iNewOwner != con.iIndependent and iNewOwner != con.iIndependent2 and iNewOwner != con.iIndependent3 and iNewOwner != con.iIndependent4):
				for x in range(tCityPlot[0]-2, tCityPlot[0]+3):				# from x-2 to x+2
					for y in range(tCityPlot[1]-2, tCityPlot[1]+3):		# from y-2 to y+2
						iPlotBarbCulture = gc.getMap().plot(x, y).getCulture(con.iBarbarian)
						if (iPlotBarbCulture > 0):
							if (gc.getMap().plot(x, y).getPlotCity().isNone() or (x==tCityPlot[0] and y==tCityPlot[1])):
								if (bBarbarian2x2Decay):
									gc.getMap().plot(x, y).setCulture(con.iBarbarian, iPlotBarbCulture/4, True)
								if (bBarbarian2x2Conversion):
									gc.getMap().plot(x, y).setCulture(con.iBarbarian, 0, True)
									gc.getMap().plot(x, y).setCulture(iNewOwner, iPlotBarbCulture, True)
						iPlotIndependentCulture = gc.getMap().plot(x, y).getCulture(con.iIndependent)
						if (iPlotIndependentCulture > 0):
							if (gc.getMap().plot(x, y).getPlotCity().isNone() or (x==tCityPlot[0] and y==tCityPlot[1])):
								if (bBarbarian2x2Decay):
									gc.getMap().plot(x, y).setCulture(con.iIndependent, iPlotIndependentCulture/4, True)
								if (bBarbarian2x2Conversion):
									gc.getMap().plot(x, y).setCulture(con.iIndependent, 0, True)
									gc.getMap().plot(x, y).setCulture(iNewOwner, iPlotIndependentCulture, True)
						iPlotIndependent2Culture = gc.getMap().plot(x, y).getCulture(con.iIndependent2)
						if (iPlotIndependent2Culture > 0):
							if (gc.getMap().plot(x, y).getPlotCity().isNone() or (x==tCityPlot[0] and y==tCityPlot[1])):
								if (bBarbarian2x2Decay):
									gc.getMap().plot(x, y).setCulture(con.iIndependent2, iPlotIndependent2Culture/4, True)
								if (bBarbarian2x2Conversion):
									gc.getMap().plot(x, y).setCulture(con.iIndependent2, 0, True)
									gc.getMap().plot(x, y).setCulture(iNewOwner, iPlotIndependent2Culture, True)

		#plot
		for x in range(tCityPlot[0]-1, tCityPlot[0]+2):				# from x-1 to x+1
			for y in range(tCityPlot[1]-1, tCityPlot[1]+2):		# from y-1 to y+1
				pCurrent = gc.getMap().plot(x, y)
				iCurrentPlotCulture = pCurrent.getCulture(iOldOwner)

				if (pCurrent.isCity()):
					pCurrent.setCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/100, True)
					pCurrent.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent)/100, True)
				else:
					pCurrent.setCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/3/100, True)
					pCurrent.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent/3)/100, True)

				#cut other players culture
##				for iCiv in range(iNumPlayers):
##					if (iCiv != iNewOwner and iCiv != iOldOwner):
##						iPlotCulture = gc.getMap().plot(x, y).getCulture(iCiv)
##						if (iPlotCulture > 0):
##							gc.getMap().plot(x, y).setCulture(iCiv, iPlotCulture/3, True)
				#print (x, y, pCurrent.getCulture(iNewOwner), ">", pCurrent.getCulture(iOldOwner))

				if (not pCurrent.isCity()):
					if (bAlwaysOwnPlots):
						pCurrent.setOwner(iNewOwner)
					else:
						if (pCurrent.getCulture(iNewOwner)*4 > pCurrent.getCulture(iOldOwner)):
							pCurrent.setOwner(iNewOwner)
					#print ("NewOwner", pCurrent.getOwner())


	#handler
	def spreadMajorCulture(self, iMajorCiv, iX, iY):
		for x in range(iX-4, iX+5):	# from x-4 to x+4
			for y in range(iY-4, iY+5):	# from y-4 to y+4
				pCurrent = gc.getMap().plot(x, y)
				if (pCurrent.isCity()):
					city = pCurrent.getPlotCity()
					if (city.getOwner() >= iNumMajorPlayers):
						iMinor = city.getOwner()
						iDen = 25
						if (gc.getPlayer(iMajorCiv).getSettlersMaps( con.iMapMaxY-y-1, x ) >= 400):
							iDen = 10
						elif (gc.getPlayer(iMajorCiv).getSettlersMaps( con.iMapMaxY-y-1, x ) >= 150):
							iDen = 15

						iMinorCityCulture = city.getCulture(iMinor)
						city.setCulture(iMajorCiv, iMinorCityCulture/iDen, True)

						iMinorPlotCulture = pCurrent.getCulture(iMinor)
						pCurrent.setCulture(iMajorCiv, iMinorPlotCulture/iDen, True)


	#UniquePowers
	# 3Miro: Turkey I guess
	def convertPlotCulture(self, pCurrent, iCiv, iPercent, bOwner):

		if (pCurrent.isCity()):
			city = pCurrent.getPlotCity()
			iCivCulture = city.getCulture(iCiv)
			iLoopCivCulture = 0
			for iLoopCiv in range(iNumTotalPlayers):
				if (iLoopCiv != iCiv):
					iLoopCivCulture += city.getCulture(iLoopCiv)
					city.setCulture(iLoopCiv, city.getCulture(iLoopCiv)*(100-iPercent)/100, True)
			city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

##		for iLoopCiv in range(iNumTotalPlayers):
##			if (iLoopCiv != iCiv):
##				iLoopCivCulture = pCurrent.getCulture(iLoopCiv)
##				iCivCulture = pCurrent.getCulture(iCiv)
##				pCurrent.setCulture(iLoopCiv, iLoopCivCulture*(100-iPercent)/100, True)
##				pCurrent.setCulture(iCiv, iCivCulture + iLoopCivCulture*iPercent/100, True)
		iCivCulture = pCurrent.getCulture(iCiv)
		iLoopCivCulture = 0
		for iLoopCiv in range(iNumTotalPlayers):
			if (iLoopCiv != iCiv):
				iLoopCivCulture += pCurrent.getCulture(iLoopCiv)
				pCurrent.setCulture(iLoopCiv, pCurrent.getCulture(iLoopCiv)*(100-iPercent)/100, True)
		pCurrent.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)
		if (bOwner == True):
			pCurrent.setOwner(iCiv)


	#RiseAndFall
	def pushOutGarrisons(self, tCityPlot, iOldOwner):
		tDestination = (-1, -1)
		for x in range(tCityPlot[0]-2, tCityPlot[0]+3):
			for y in range(tCityPlot[1]-2, tCityPlot[1]+3):
				pDestination = gc.getMap().plot(x, y)
				if (pDestination.getOwner() == iOldOwner and (not pDestination.isWater()) and (not pDestination.isImpassable())):
					tDestination = (x, y)
					break
					break
		if (tDestination != (-1, -1)):
			plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
			iNumUnitsInAPlot = plotCity.getNumUnits()
			j = 0
			for i in range(iNumUnitsInAPlot):
				unit = plotCity.getUnit(j)
				if (unit.getDomainType() == 2): #land unit
					#print("  3Miro 2 Unit Type and Owner ",unit.getUnitType(),"  ",unit.getOwner() )
					unit.setXYOld(tDestination[0], tDestination[1])
				else:
					j = j + 1

	#RiseAndFall
	def relocateSeaGarrisons(self, tCityPlot, iOldOwner):
		tDestination = (-1, -1)
		cityList = PyPlayer(iOldOwner).getCityList()
		for pyCity in cityList:
			if (pyCity.GetCy().isCoastalOld()):
				tDestination = (pyCity.GetCy().getX(), pyCity.GetCy().getY())
		if (tDestination == (-1, -1)):
			for x in range(tCityPlot[0]-12, tCityPlot[0]+12):
				for y in range(tCityPlot[1]-12, tCityPlot[1]+12):
					pDestination = gc.getMap().plot(x, y)
					if (pDestination.isWater()):
						tDestination = (x, y)
						break
						break
		if (tDestination != (-1, -1)):
			plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
			iNumUnitsInAPlot = plotCity.getNumUnits()
			j = 0
			for i in range(iNumUnitsInAPlot):
				unit = plotCity.getUnit(j)
				if (unit.getDomainType() == 0): #sea unit
					#print("  3Miro 3 Unit Type and Owner ",unit.getUnitType(),"  ",unit.getOwner() )
					unit.setXYOld(tDestination[0], tDestination[1])
				else:
					j = j + 1

	#RiseAndFall
	def createGarrisons(self, tCityPlot, iNewOwner, iNumUnits):
		plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
		city = plotCity.getPlotCity()
		iNumUnitsInAPlot = plotCity.getNumUnits()
		pCiv = gc.getPlayer(iNewOwner)

		# Sedna17: makes garrison units based on new tech tree/units
		if (gc.getTeam(pCiv.getTeam()).isHasTech(xml.iNationalism) and gc.getTeam(pCiv.getTeam()).isHasTech(xml.iMilitaryTactics)):
			iUnitType = xml.iLineInfantry
		elif (gc.getTeam(pCiv.getTeam()).isHasTech(xml.iMatchlock)):
			iUnitType = xml.iMusketman
		elif (gc.getTeam(pCiv.getTeam()).isHasTech(xml.iGunpowder)):
			iUnitType = xml.iArquebusier
		elif (gc.getTeam(pCiv.getTeam()).isHasTech(xml.iMilitaryTradition)):
			iUnitType = xml.iArquebusier
		elif (gc.getTeam(pCiv.getTeam()).isHasTech(xml.iClockmaking)):
			iUnitType = xml.iArbalest
		elif (gc.getTeam(pCiv.getTeam()).isHasTech(xml.iMachinery)):
			iUnitType = xml.iCrossbowman
		else:
			iUnitType = xml.iArcher

		self.makeUnit(iUnitType, iNewOwner, [tCityPlot[0], tCityPlot[1]], iNumUnits)


	#RiseAndFall, Stability
	def killCiv(self, iCiv, iNewCiv):
		self.clearPlague(iCiv)
		for pyCity in PyPlayer(iCiv).getCityList():
			tCoords = (pyCity.GetCy().getX(), pyCity.GetCy().getY())
			self.cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
			self.flipCity(tCoords, 0, 0, iNewCiv, [iCiv]) #by trade because by conquest may raze the city
			#pyCity.GetCy().setHasRealBuilding(con.iPlague, False)  #buggy
		self.flipUnitsInArea([0,0], [con.iMapMaxX,con.iMapMaxY], iNewCiv, iCiv, False, True)
		#self.flipUnitsInArea([0,0], [123,67], iNewCiv, iCiv, False, True)
		#self.killUnitsInArea([0,0], [123,67], iNewCiv, iCiv) ?
		#if (iCiv < iNumMajorPlayers):
		#	self.clearEmbassies(iCiv)
		self.setLastTurnAlive(iCiv, gc.getGame().getGameTurn())
		self.resetUHV(iCiv)

	def killAndFragmentCiv(self, iCiv, bBarbs, bAssignOneCity):
		self.clearPlague(iCiv)
		iNumLoyalCities = 0
		iCounter = gc.getGame().getSorenRandNum(6, 'random start')
		for pyCity in PyPlayer(iCiv).getCityList():
			tCoords = (pyCity.GetCy().getX(), pyCity.GetCy().getY())
			pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
			#1 loyal city for the human player
			if (bAssignOneCity and iNumLoyalCities < 1 and pyCity.GetCy().isCapital()):
				iNumLoyalCities += 1
				#gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iNewCiv1, False, -1) #too dangerous?
				#gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iNewCiv2, False, -1)
				for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
					gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(i, False, -1)
				continue
			#assign to neighbours first
			bNeighbour = False
			iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
			for j in range(iRndnum, iRndnum + iNumPlayers): #only major players
				iLoopCiv = j % iNumPlayers
				if (gc.getPlayer(iLoopCiv).isAlive() and iLoopCiv != iCiv and not gc.getPlayer(iLoopCiv).isHuman()):
					if (pCurrent.getCulture(iLoopCiv) > 0):
						if (pCurrent.getCulture(iLoopCiv)*100 / (pCurrent.getCulture(iLoopCiv) + pCurrent.getCulture(iCiv) + pCurrent.getCulture(iBarbarian) + pCurrent.getCulture(iIndependent) + pCurrent.getCulture(iIndependent2)) >= 5): #change in vanilla
							self.flipUnitsInCityBefore((tCoords[0],tCoords[1]), iLoopCiv, iCiv)
							self.setTempFlippingCity((tCoords[0],tCoords[1]))
							self.flipCity(tCoords, 0, 0, iLoopCiv, [iCiv])
							#pyCity.GetCy().setHasRealBuilding(con.iPlague, False)  #buggy
							#Sedna17: Possibly buggy, used to flip units in 2x2 radius, which could take us outside the map.
							self.flipUnitsInArea([tCoords[0]-1,tCoords[1]-1], [tCoords[0]+1,tCoords[1]-1], iLoopCiv, iCiv, False, True)
							self.flipUnitsInCityAfter(self.getTempFlippingCity(), iLoopCiv)
							bNeighbour = True
							break
			if (bNeighbour):
				continue
			#fragmentation in 2
			if ( not bBarbs ):
				#if (iCounter % 2 == 0):
				#	iNewCiv = iNewCiv1
				#elif (iCounter % 2 == 1):
				#	iNewCiv = iNewCiv2
				iNewCiv = con.iIndepStart + gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random indep' )
				self.flipUnitsInCityBefore((tCoords[0],tCoords[1]), iNewCiv, iCiv)
				self.setTempFlippingCity((tCoords[0],tCoords[1]))
				self.cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
				self.flipCity(tCoords, 0, 0, iNewCiv, [iCiv])
				#pyCity.GetCy().setHasRealBuilding(con.iPlague, False)  #buggy
				self.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
				iCounter += 1
				self.flipUnitsInArea([tCoords[0]-1,tCoords[1]-1], [tCoords[0]+1,tCoords[1]+1], iNewCiv, iCiv, False, True)
			#fragmentation with barbs
			else:
				#if (iCounter % 3 == 0):
				#	iNewCiv = iNewCiv1
				#elif (iCounter % 3 == 1):
				#	iNewCiv = iNewCiv2
				#elif (iCounter % 3 == 2):
				#	iNewCiv = iNewCiv3
				iNewCiv = con.iIndepStart + gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 2, 'random indep' )
				if ( iNewCiv == con.iIndepEnd + 1 ):
					iNewCiv = iBarbarian
				self.flipUnitsInCityBefore((tCoords[0],tCoords[1]), iNewCiv, iCiv)
				self.setTempFlippingCity((tCoords[0],tCoords[1]))
				self.cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
				self.flipCity(tCoords, 0, 0, iNewCiv, [iCiv])
				#pyCity.GetCy().setHasRealBuilding(con.iPlague, False) #buggy
				self.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
				iCounter += 1
				self.flipUnitsInArea([tCoords[0]-1,tCoords[1]-1], [tCoords[0]+1,tCoords[1]+1], iNewCiv, iCiv, False, True)
		if (bAssignOneCity == False):
			#self.flipUnitsInArea([0,0], [123,67], iNewCiv1, iCiv, False, True) #causes a bug: if a unit was inside another city's civ, when it becomes independent or barbarian, may raze it
			self.killUnitsInArea([0,0], [con.iMapMaxX,con.iMapMaxY], iCiv)
			self.resetUHV(iCiv)
		if (iCiv < iNumMajorPlayers):
			self.clearEmbassies(iCiv)
		self.setLastTurnAlive(iCiv, gc.getGame().getGameTurn())


	def resetUHV(self, iPlayer):
		if (iPlayer < iNumMajorPlayers):
			pPlayer = gc.getPlayer( iPlayer )
			if ( pPlayer.getUHV( 0 ) == -1 ):
				pPlayer.setUHV( 0, 0 )
			if ( pPlayer.getUHV( 1 ) == -1 ):
				pPlayer.setUHV( 1, 0 )
			if ( pPlayer.getUHV( 2 ) == -1 ):
				pPlayer.setUHV( 2, 0 )

	def clearEmbassies(self, iDeadCiv):
		#for i in range (iNumTotalPlayers):
		#	for pyCity in PyPlayer(i).getCityList():
		#		if (pyCity.GetCy().hasBuilding(iNumBuildingsPlague + iDeadCiv)):
		#			pyCity.GetCy().setHasRealBuilding(iNumBuildingsPlague + iDeadCiv, False)
		#			continue
		pass

	def clearPlague(self, iCiv):
		for pyCity in PyPlayer(iCiv).getCityList():
			if (pyCity.GetCy().hasBuilding(xml.iPlague)):
				pyCity.GetCy().setHasRealBuilding(xml.iPlague, False)


	#AIWars
	def isNoVassal(self, iCiv):
		iMaster = 0
		for iMaster in range (iNumTotalPlayers):
			if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iMaster)):
				return False
		return True

	def isAVassal(self, iCiv):
		iMaster = 0
		for iMaster in range (iNumTotalPlayers):
			if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iMaster)):
				return True
		return False

	# UP, UHV, by Leoreth
	def getMaster(self, iCiv):
		team = gc.getTeam(gc.getPlayer(iCiv).getTeam())
		for iMaster in range(iNumTotalPlayers):
			if team.isVassal(iMaster):
				return iMaster
		return -1

	#Barbs, RiseAndFall
	def squareSearch( self, tTopLeft, tBottomRight, function, argsList ): #by LOQ
		"""Searches all tile in the square from tTopLeft to tBottomRight and calls function for
		every tile, passing argsList. The function called must return a tuple: (1) a result, (2) if
		a plot should be painted and (3) if the search should continue."""
		tPaintedList = []
		result = None
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				result, bPaintPlot, bContinueSearch = function((x, y), result, argsList)
				if bPaintPlot:				# paint plot
					tPaintedList.append((x, y))
				if not bContinueSearch:		# goal reached, so stop
					return result, tPaintedList
		return result, tPaintedList

	#Barbs, RiseAndFall
	def outerInvasion( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getFeatureType() != xml.iMarsh) and (pCurrent.getFeatureType() != xml.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					if (pCurrent.countTotalCulture() == 0 ):
						# this is a good plot, so paint it and continue search
						return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def forcedInvasion( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, and it isn't occupied by a unit or city"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getFeatureType() != xml.iMarsh) and (pCurrent.getFeatureType() != xml.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					#if (pCurrent.countTotalCulture() == 0 ):
					 # this is a good plot, so paint it and continue search
					 return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#Barbs
	def innerSeaSpawn( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's water and it isn't occupied by any unit. Unit check extended to adjacent plots"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isWater()) and (pCurrent.getTerrainType() == xml.iTerrainCoast):
			if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
				iClean = 0
				for x in range(tCoords[0] - 1, tCoords[0] + 2):				# from x-1 to x+1
					for y in range(tCoords[1] - 1, tCoords[1] + 2):		# from y-1 to y+1
						if (pCurrent.getNumUnits() != 0):
							iClean += 1
				if ( iClean == 0 ):
					# this is a good plot, so paint it and continue search
					return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#Barbs
	def outerSeaSpawn( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's water and it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isWater()) and (pCurrent.getTerrainType() == xml.iTerrainCoast):
			if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
				if (pCurrent.countTotalCulture() == 0 ):
					iClean = 0
					for x in range(tCoords[0] - 1, tCoords[0] + 2):				# from x-1 to x+1
						for y in range(tCoords[1] - 1, tCoords[1] + 2):		# from y-1 to y+1
							if (pCurrent.getNumUnits() != 0):
								iClean += 1
					if ( iClean == 0 ):
						# this is a good plot, so paint it and continue search
						return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#Barbs
	def outerSpawn( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory.
		Unit check extended to adjacent plots"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getFeatureType() != xml.iMarsh) and (pCurrent.getFeatureType() != xml.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					iClean = 0
					for x in range(tCoords[0] - 1, tCoords[0] + 2):				# from x-1 to x+1
						for y in range(tCoords[1] - 1, tCoords[1] + 2):		# from y-1 to y+1
							if (pCurrent.getNumUnits() != 0):
								iClean += 1
					if ( iClean == 0 ):
						if (pCurrent.countTotalCulture() == 0 ):
							# this is a good plot, so paint it and continue search
							return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#RiseAndFall
	def innerInvasion( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getFeatureType() != xml.iMarsh) and (pCurrent.getFeatureType() != xml.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					    # this is a good plot, so paint it and continue search
					    return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def innerSpawn( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getFeatureType() != xml.iMarsh) and (pCurrent.getFeatureType() != xml.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					iClean = 0
					for x in range(tCoords[0] - 1, tCoords[0] + 2):				# from x-1 to x+1
						for y in range(tCoords[1] - 1, tCoords[1] + 2):		# from y-1 to y+1
							if (pCurrent.getNumUnits() != 0):
								iClean += 1
					if ( iClean == 0 ):
						if (pCurrent.getOwner() in argsList ):
							# this is a good plot, so paint it and continue search
							return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#RiseAndFall
	def goodPlots( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't desert, tundra, marsh or jungle; it isn't occupied by a unit or city and if it isn't a civ's territory.
		Unit check extended to adjacent plots"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if ( not pCurrent.isImpassable()):
				if ( not pCurrent.isUnit() ):
					if (pCurrent.getTerrainType() != xml.iTerrainDesert) and (pCurrent.getTerrainType() != xml.iTerrainTundra) and (pCurrent.getFeatureType() != xml.iMarsh) and (pCurrent.getFeatureType() != xml.iJungle):
						if (pCurrent.countTotalCulture() == 0 ):
							# this is a good plot, so paint it and continue search
							return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#RiseAndFall
	def ownedCityPlots( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it contains a city belonging to the civ"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if (pCurrent.getOwner() == argsList ):
			if (pCurrent.isCity()):
				# this is a good plot, so paint it and continue search
				return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def ownedPlots( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it is in civ's territory."""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if (pCurrent.getOwner() == argsList ):
			# this is a good plot, so paint it and continue search
			return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def goodOwnedPlots( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands; it isn't marsh or jungle, it isn't occupied by a unit and if it is in civ's territory."""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getFeatureType() != xml.iMarsh) and (pCurrent.getFeatureType() != xml.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					    if (pCurrent.getOwner() == argsList ):
						    # this is a good plot, so paint it and continue search
						    return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def collapseImmune( self, iCiv ):
		#3MiroUP: Emperor
		if ( gc.hasUP(iCiv,con.iUP_Emperor) ):
			#print(" 3Miro: has the power: ",iCiv)
			if (gc.getMap().plot( con.tCapitals[iCiv][0], con.tCapitals[iCiv][1]).isCity()):
				#print(" 3Miro: has the city: ",iCiv)
				if(gc.getMap().plot( con.tCapitals[iCiv][0], con.tCapitals[iCiv][1]).getPlotCity().getOwner() == iCiv):
					#print(" 3Miro: collapse immune ",iCiv)
					return true
		#print(" 3Miro: not immune ",iCiv)
		return false

	def collapseImmuneCity( self, iCiv, x, y ):
		#3MiroUP: Emperor
		if ( gc.hasUP(iCiv,con.iUP_Emperor) ):
			if (gc.getMap().plot( con.tCapitals[iCiv][0], con.tCapitals[iCiv][1]).isCity()):
				if(gc.getMap().plot( con.tCapitals[iCiv][0], con.tCapitals[iCiv][1]).getPlotCity().getOwner() == iCiv):
					if( (x>=con.tCoreAreasTL[iCiv][0]) and (x<=con.tCoreAreasBR[iCiv][0]) and (y>=con.tCoreAreasTL[iCiv][1]) and (y<=con.tCoreAreasBR[iCiv][1]) ):
						#print(" 3Miro: collapse immune ",iCiv,x,y)
						return true
		#print(" 3Miro: collapse not immune ",iCiv,x,y)
		return false

	#Absinthe: chooseable persecution popup
	def showPersecutionPopup(self):
		"""Asks the human player to select a religion to persecute."""

		popup = Popup.PyPopup(7628, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString("Religious Persecution")
		popup.setBodyString("Choose a religious minority to deal with...")
		religionList = self.getPersecutionReligions()
		for iReligion in religionList:
			strIcon = gc.getReligionInfo(iReligion).getType()
			strIcon = "[%s]" %(strIcon.replace("RELIGION_", "ICON_"))
			strButtonText = "%s %s" %(localText.getText(strIcon, ()), gc.getReligionInfo(iReligion).getText())
			popup.addButton(strButtonText)
		popup.launch(False)

	def getPersecutionData(self):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lPersecutionData'][0], scriptDict['lPersecutionData'][1], scriptDict['lPersecutionData'][2]

	def setPersecutionData(self, iPlotX, iPlotY, iUnitID):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lPersecutionData'] = [iPlotX, iPlotY, iUnitID]
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getPersecutionReligions(self):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lPersecutionReligions']

	def setPersecutionReligions(self, val):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lPersecutionReligions'] = val
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )
	#Absinthe: end

	#Absinthe: persecution
	def prosecute( self, iPlotX, iPlotY, iUnitID, iReligion=None ):
		"""Removes one religion from the city and handles the consequences."""

		if (gc.getMap().plot(iPlotX, iPlotY).isCity()):
			city = gc.getMap().plot(iPlotX, iPlotY).getPlotCity()
		else:
			return

		iOwner = city.getOwner()
		pPlayer = gc.getPlayer(iOwner)
		pUnit = pPlayer.getUnit(iUnitID)
		iStateReligion = pPlayer.getStateReligion()

		# sanity check - can only persecute with a state religion
		if iStateReligion == -1:
			return False

		# determine the target religion, if not supplied by the popup decision (for the AI)
		if not iReligion:
			for iReligion in con.tPersecutionOrder[iStateReligion]:
				if not city.isHolyCityByType(iReligion): # spare holy cities
					if city.isHasReligion(iReligion):
						break

		# count the number of religious buildings and wonders (for the chance)
		if iReligion > -1:
			lReligionBuilding = []
			lReligionWonder = 0
			for iBuilding in xrange(gc.getNumBuildingInfos()):
				if city.getNumRealBuilding(iBuilding):
					BuildingInfo = gc.getBuildingInfo(iBuilding)
					if BuildingInfo.getPrereqReligion() == iReligion:
						lReligionBuilding.append(iBuilding)
						if isWorldWonderClass(BuildingInfo.getBuildingClassType()) or isNationalWonderClass(BuildingInfo.getBuildingClassType()):
							lReligionWonder += 1
		else:
			return False	# when there is no available religion to purge

		# base chance to work: about 50-90, based on faith:
		## iChance = 60 + max(-10, min(30, pPlayer.getFaith()/3))
		iChance = 55 + pPlayer.getFaith()/3
		# lower chance for purging any religion from Jerusalem:
		if (iPlotX == con.iJerusalem[0] and iPlotY == con.iJerusalem[1]):
			iChance -= 25
		# lower chance if the city has the chosen religion's buildings/wonders:
		iChance -= (len(lReligionBuilding) * 8 + lReligionWonder * 17)		# the wonders have an extra chance reduction (in addition to the first reduction)

		if gc.getGame().getSorenRandNum(100, "purge chance") < iChance:
		# on successful persecution:

			# remove a single non-state religion and its buildings from the city, count the loot
			iLootModifier = 2 * city.getPopulation() / city.getReligionCount() + 1
			iLoot = 2 + iLootModifier
			city.setHasReligion(iReligion, 0, 0, 0)
			for i in range(len(lReligionBuilding)):
				city.setNumRealBuilding(lReligionBuilding[i], 0)
				iLoot += iLootModifier
			if iReligion == xml.iJudaism:
				iLoot = iLoot*3/2

			# kill / expel some population
			if city.getPopulation() > 15 and city.getReligionCount() < 2:
				city.changePopulation(-4)
			elif city.getPopulation() > 10 and city.getReligionCount() < 3:
				city.changePopulation(-3)
			elif city.getPopulation() > 6 and city.getReligionCount() < 4:
				city.changePopulation(-2)
			elif city.getPopulation() > 3:
				city.changePopulation(-1)

			# distribute the loot
			iLoot = iLoot/2 + gc.getGame().getSorenRandNum(iLoot/2, 'random loot')
			pPlayer.changeGold(iLoot)

			# add faith for the persecution itself (there is an indirect increase too, the negative modifier from having a non-state religion is gone)
			pPlayer.changeFaith( 1 )

			# apply diplomatic penalty
			for iLoopPlayer in range(con.iNumPlayers):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive() and iLoopPlayer != iOwner:
					if pLoopPlayer.getStateReligion() == iReligion:
						pLoopPlayer.AI_changeAttitudeExtra(iOwner, -1)

		## count minor religion persecutions??
	#		if ( i == minorReligion ){ // 3Miro: count the minor religion prosecutions
	#		minorReligionRefugies++;
	#		gc.setMinorReligionRefugies( 0 )

		## Spanish UP?
	#		if ( not gc.hasUP(iOwner,con.iUP_Inquisition) ):
	#			#self.setProsecutionCount( iOwner, self.getProsecutionCount( iOwner ) + 10 )
	#			pPlayer.changeProsecutionCount( 10 )

			# interface message for the player
			CyInterface().addMessage(iOwner, False, con.iDuration, localText.getText("TXT_KEY_MESSAGE_INQUISITION", (city.getName(), gc.getReligionInfo(iReligion).getDescription(), iLoot)), "AS2D_PLAGUE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), ColorTypes(con.iGreen), iPlotX, iPlotY, True, True)

			# Jews may spread to another random city
			if iReligion == xml.iJudaism:
				if gc.getGame().getSorenRandNum(100, "judaism spread chance") < 80:
					tCity = self.selectRandomCity()
					self.spreadJews(tCity,xml.iJudaism)
					CyInterface().addMessage(iOwner, False, con.iDuration, localText.getText("TXT_KEY_MESSAGE_JEWISH_MOVE", (city.getName(), )), "AS2D_PLAGUE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), ColorTypes(con.iGreen), iPlotX, iPlotY, True, True)

		else: # message on failed persecution:
			CyInterface().addMessage(iOwner, False, con.iDuration, localText.getText("TXT_KEY_MESSAGE_INQUISITION_FAIL", (city.getName(), )), "AS2D_SABOTAGE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), ColorTypes(con.iRed), iPlotX, iPlotY, True, True)

		# start a small revolt
		city.changeCultureUpdateTimer(1);
		city.changeOccupationTimer(1);

		# consume the inquisitor
		pUnit.kill(0, -1)

		# unhappiness from persecution
		city.changeHurryAngerTimer(city.flatHurryAngerLength())

		return True
	#Absinthe: end

	def saint( self, iOwner, iUnitID ):
		# 3Miro: kill the Saint :), just make it so he cannot be used for other purposes
		pPlayer = gc.getPlayer( iOwner )
		pPlayer.changeFaith( con.iSaintBenefit )
		pUnit = pPlayer.getUnit(iUnitID)
		pUnit.kill(0, -1)

	def selectRandomCity(self):
		cityList = []
		for i in range( con.iNumPlayers ):	# current civ range is iNumPlayers, so it can only be a major player's city
			if (gc.getPlayer(i).isAlive()):
				for pyCity in PyPlayer(i).getCityList():
					cityList.append(pyCity.GetCy())
		iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
		city = cityList[iCity]
		return (city.getX(), city.getY())

	def spreadJews(self,tPlot,iReligion):
		if (tPlot != False):
			plot = gc.getMap().plot( tPlot[0], tPlot[1] )
			if (not plot.getPlotCity().isNone()):
				plot.getPlotCity().setHasReligion(iReligion,1,0,0) # puts the religion into this city
				return True
			else:
				return False
		return False

	def isIndep( self, iCiv ):
		if ( iCiv >= con.iIndepStart and iCiv <= con.iIndepEnd ):
			return True
		return False

	def zeroStability(self,iPlayer): # called by RiseAndFall Resurrection
		for iCount in range(con.iNumStabilityParameters):
			self.setParameter(iPlayer, iCount, False, 0)


	#Absinthe: stability overlay
	def toggleStabilityOverlay(self):

		engine = CyEngine()
		map = CyMap()

		# clear the highlight
		engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)

		global iScreenIsUp
		if self.bStabilityOverlay: # if it's already on
			self.bStabilityOverlay = False
			iScreenIsUp = 0
			CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", False)
			# remove the selectable civs and the selection box
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
			for i in range( con.iNumMajorPlayers - 1 ):
				szName = "StabilityOverlayCiv" + str(i)
				screen.hide( szName )
			screen.hide( "ScoreBackground" )
			return

		self.bStabilityOverlay = True
		iScreenIsUp = 1
		CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", True)

		# set up colors
		colors = []
		colors.append("COLOR_HIGHLIGHT_FOREIGN")
		colors.append("COLOR_HIGHLIGHT_BORDER")
		colors.append("COLOR_HIGHLIGHT_POTENTIAL")
		colors.append("COLOR_HIGHLIGHT_NATURAL")
		colors.append("COLOR_HIGHLIGHT_CORE")

		# reset to human player, whenever the overlay is triggered
		iHuman = self.getHumanID()
		iHumanTeam = gc.getPlayer(iHuman).getTeam()
		iSelectedCivID = iHuman

		# Globe View type civ choice
		# when one of the civs is clicked on, it will run the StabilityOverlayCiv function with the chosen civ (check handleInput in CvMainInterface.py)
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		iGlobeLayerOptionsY_Regular  = 170 # distance from bottom edge
		iGlobeLayerOptionsY_Minimal  = 38 # distance from bottom edge
		iGlobeLayerOptionsWidth = 400
		iGlobeLayerOptionHeight = 20
		iY = yResolution - iGlobeLayerOptionsY_Regular
		iCurY = iY
		iMaxTextWidth = -1
		for iCiv in range( con.iNumMajorPlayers - 1 ): # all major civs except the Papal States
			szDropdownName = str("StabilityOverlayCiv") + str(iCiv)
			szCaption = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
			if(iCiv == self.getHumanID()):
				szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
			else:
				szBuffer = "  %s  " % (szCaption)
			iTextWidth = CyInterface().determineWidth( szBuffer )

			screen.setText( szDropdownName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight-10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, iCiv, 1234 )
			screen.show( szDropdownName )

			iCurY -= iGlobeLayerOptionHeight

			if iTextWidth > iMaxTextWidth:
				iMaxTextWidth = iTextWidth

		# panel for the Globe View type civ choice:
		iCurY -= iGlobeLayerOptionHeight;
		iPanelWidth = iMaxTextWidth + 16
		iPanelHeight = iY - iCurY
		iPanelX = xResolution - 14 - iPanelWidth
		iPanelY = iCurY
		screen.setPanelSize( "ScoreBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight )
		screen.show( "ScoreBackground" )

		# apply the highlight for the default civ (the human civ)
		for i in range(map.numPlots()):
			plot = map.plotByIndex(i)
			if gc.getGame().isDebugMode() or plot.isRevealed(iHumanTeam, False):
				if RFCEMaps.tProinceMap[plot.getY()][plot.getX()] == -1: # ocean and non-province tiles
					szColor = "COLOR_GREY"
				else:
					szColor = colors[self.getProvinceStabilityLevel(iHuman, plot.getProvince())]
				engine.addColoredPlotAlt(plot.getX(), plot.getY(), int(PlotStyles.PLOT_STYLE_BOX_FILL), int(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER), szColor, .2)


	def refreshStabilityOverlay(self):

		engine = CyEngine()
		map = CyMap()

		colors = []
		colors.append("COLOR_HIGHLIGHT_FOREIGN")
		colors.append("COLOR_HIGHLIGHT_BORDER")
		colors.append("COLOR_HIGHLIGHT_POTENTIAL")
		colors.append("COLOR_HIGHLIGHT_NATURAL")
		colors.append("COLOR_HIGHLIGHT_CORE")
		iHuman = self.getHumanID()
		iHumanTeam = gc.getPlayer(iHuman).getTeam()

		# if it's on, refresh the overlay, with showing the stability for the last selected civ
		global iScreenIsUp
		if (iScreenIsUp == 1):
			# clear the highlight
			engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)

			# if no civ was selected before
			global iSelectedCivID
			if (iSelectedCivID == -1):
				iSelectedCivID = iHuman

			# apply the highlight
			for i in range(map.numPlots()):
				plot = map.plotByIndex(i)
				if gc.getGame().isDebugMode() or plot.isRevealed(iHumanTeam, False):
					if RFCEMaps.tProinceMap[plot.getY()][plot.getX()] == -1: # ocean and non-province tiles
						szColor = "COLOR_GREY"
					else:
						szColor = colors[self.getProvinceStabilityLevel(iSelectedCivID, plot.getProvince())]
					engine.addColoredPlotAlt(plot.getX(), plot.getY(), int(PlotStyles.PLOT_STYLE_BOX_FILL), int(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER), szColor, .2)


	def StabilityOverlayCiv(self, iChoice):

		engine = CyEngine()
		map = CyMap()

		# clear the highlight
		engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)

		# set up colors
		colors = []
		colors.append("COLOR_HIGHLIGHT_FOREIGN")
		colors.append("COLOR_HIGHLIGHT_BORDER")
		colors.append("COLOR_HIGHLIGHT_POTENTIAL")
		colors.append("COLOR_HIGHLIGHT_NATURAL")
		colors.append("COLOR_HIGHLIGHT_CORE")

		iHuman = self.getHumanID()
		iHumanTeam = gc.getPlayer(iHuman).getTeam()

		# save the last selected civ in a global variable
		global iSelectedCivID
		iSelectedCivID = iChoice

		# refreshing and coloring Globe View type civ choice
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		iGlobeLayerOptionsY_Regular  = 170 # distance from bottom edge
		iGlobeLayerOptionsY_Minimal  = 38 # distance from bottom edge
		iGlobeLayerOptionsWidth = 400
		iGlobeLayerOptionHeight = 20
		iY = yResolution - iGlobeLayerOptionsY_Regular
		iCurY = iY
		iMaxTextWidth = -1
		for iCiv in range( con.iNumMajorPlayers - 1 ): # all major civs except the Papal States
			szDropdownName = str("StabilityOverlayCiv") + str(iCiv)
			szCaption = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
			if(iCiv == iSelectedCivID):
				szBuffer = "  <color=0,255,255>%s</color>  " % (szCaption)
			elif(iCiv == self.getHumanID()):
				szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
			else:
				szBuffer = "  %s  " % (szCaption)
			iTextWidth = CyInterface().determineWidth( szBuffer )

			screen.setText( szDropdownName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight-10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, iCiv, 1234 )
			screen.show( szDropdownName )

			iCurY -= iGlobeLayerOptionHeight

			if iTextWidth > iMaxTextWidth:
				iMaxTextWidth = iTextWidth

		# apply the highlight
		for i in range(map.numPlots()):
			plot = map.plotByIndex(i)
			if gc.getGame().isDebugMode() or plot.isRevealed(iHumanTeam, False):
				if RFCEMaps.tProinceMap[plot.getY()][plot.getX()] == -1: # ocean and non-province tiles
					szColor = "COLOR_GREY"
				else:
					szColor = colors[self.getProvinceStabilityLevel(iChoice, plot.getProvince())]
				engine.addColoredPlotAlt(plot.getX(), plot.getY(), int(PlotStyles.PLOT_STYLE_BOX_FILL), int(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER), szColor, .2)


	def getProvinceStabilityLevel(self, iCiv, iProvince):
		"""Returns the stability level of the province for the given civ."""

		pPlayer = gc.getPlayer( iCiv )
		if pPlayer.getProvinceType( iProvince ) == con.iProvinceCore:
			return 4 # core
		elif pPlayer.getProvinceType( iProvince ) == con.iProvinceNatural:
			return 3 # natural/historical
		elif pPlayer.getProvinceType( iProvince ) == con.iProvincePotential:
			return 2 # potential
		elif pPlayer.getProvinceType( iProvince ) == con.iProvinceOuter:
			return 1 # border/contested
		else:
			return 0 # unstable
	#Absinthe: end
