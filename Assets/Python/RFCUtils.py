# Rhye's and Fall of Civilization: Europe - Utilities

from CvPythonExtensions import *
import CvUtil
import CvScreenEnums #Absinthe
import RFCEMaps #Absinthe
import PyHelpers
import Popup #Absinthe
import Consts as con
import XMLConsts as xml
from StoredData import sd

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
		return sd.scriptDict['lLastTurnAlive'][iCiv]

	def setLastTurnAlive( self, iCiv, iNewValue ):
		sd.scriptDict['lLastTurnAlive'][iCiv] = iNewValue

	def getLastRespawnTurn( self, iCiv ):
		return sd.scriptDict['lLastRespawnTurn'][iCiv]

	def setLastRespawnTurn( self, iCiv, iNewValue ):
		sd.scriptDict['lLastRespawnTurn'][iCiv] = iNewValue

	#Victory
	#def getGoal( self, i, j ):
		#return sd.scriptDict['lGoals'][i][j]

	#def setGoal( self, i, j, iNewValue ):
		#sd.scriptDict['lGoals'][i][j] = iNewValue

	#Stability
	def getTempFlippingCity( self ):
		return sd.scriptDict['tempFlippingCity']

	def setTempFlippingCity( self, tNewValue ):
		sd.scriptDict['tempFlippingCity'] = tNewValue

	def getStability( self, iCiv ):
		return gc.getPlayer( iCiv ).getStability()

	#def setStability( self, iCiv, iNewValue ):
		#sd.scriptDict['lStability'][iCiv] = iNewValue

	#def getBaseStabilityLastTurn( self, iCiv ):
		#return sd.scriptDict['lBaseStabilityLastTurn'][iCiv]

	#def setBaseStabilityLastTurn( self, iCiv, iNewValue ):
		#sd.scriptDict['lBaseStabilityLastTurn'][iCiv] = iNewValue

	#def getStabilityParameters( self, iCiv, iParameter ):
		#return sd.scriptDict['lStabilityParameters'][iCiv][iParameter]

	#def setStabilityParameters( self, iCiv,iParameter, iNewValue ):
		#sd.scriptDict['lStabilityParameters'][iCiv][iParameter] = iNewValue

	#def getGreatDepressionCountdown( self, iCiv ):
		#return sd.scriptDict['lGreatDepressionCountdown'][iCiv]

	#def setGreatDepressionCountdown( self, iCiv, iNewValue ):
		#sd.scriptDict['lGreatDepressionCountdown'][iCiv] = iNewValue

	#def getLastRecordedStabilityStuff( self, iParameter ):
		#return sd.scriptDict['lLastRecordedStabilityStuff'][iParameter]

	#def setLastRecordedStabilityStuff( self, iParameter, iNewValue ):
		#sd.scriptDict['lLastRecordedStabilityStuff'][iParameter] = iNewValue

	def getProsecutionCount( self, iCiv ):
		#return sd.scriptDict['iProsecutionCount'][iCiv]
		return gc.getProsecutionCount( iCiv )

	def setProsecutionCount( self, iCiv, iNewValue ):
		#sd.scriptDict['iProsecutionCount'][iCiv] = iNewValue
		gc.setProsecutionCount( iCiv, iNewValue )

	#Plague
	def getPlagueCountdown( self, iCiv ):
		return sd.scriptDict['lPlagueCountdown'][iCiv]

	def setPlagueCountdown( self, iCiv, iNewValue ):
		sd.scriptDict['lPlagueCountdown'][iCiv] = iNewValue

	def getSeed( self ):
		return sd.scriptDict['iSeed']

#######################################

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
		#if ( sd.scriptDict['lGoals'][con.iBurgundy][1] == -1 ):
		#	return sd.scriptDict['iBurgundyCulture']
		#else:
		#	return -1

	def getArabianInfluence( self ):
		return 0
		#if ( sd.scriptDict['lGoals'][con.iArabia][1] == -1 ):
		#	return gc.getGame().calculateReligionPercent( xml.iIslam )
		#else:
		#	return -1

	def getNorseRazed( self ):
		return 0
		#if ( sd.scriptDict['lGoals'][con.iNorse][1] == -1 ):
		#	return sd.scriptDict['iNorseRazed']
		#else:
		#	return -1

	def getKievFood( self ):
		return 0
		#if ( sd.scriptDict['lGoals'][con.iKiev][0] == -1 ):
		#	return sd.scriptDict['iKievFood']
		#else:
		#	return -1
	# 3Miro: END Utilities


	#Plague, UP
	def getRandomCity(self, iPlayer):
		cityList =  self.getCityList(iPlayer)
		if cityList:
			return self.getRandomEntry(cityList)
		return -1

	def getRandomCiv( self ):
		civList = [iCiv for iCiv in range(iNumPlayers) if gc.getPlayer(iCiv).isAlive()]
		return self.getRandomEntry(civList)

	def isMortalUnit(self, unit):
		# Absinthe: leader units, and great people won't be killed by the plague
		if unit.isHasPromotion(xml.iPromotionLeader):
			if not gc.getPlayer(unit.getOwner()).isHuman():
				return False
		iUnitType = unit.getUnitType()
		if xml.iProphet <= iUnitType <= xml.iGreatSpy:
			return False
		return True

	def isDefenderUnit(self, unit):
		return False

	#AIWars
	def checkUnitsInEnemyTerritory(self, iCiv1, iCiv2):
		unitList = PyPlayer(iCiv1).getUnitList()
		if unitList:
			for unit in unitList:
				iX = unit.getX()
				iY = unit.getY()
				if gc.getMap().plot( iX, iY ).getOwner() == iCiv2:
					return True
		return False

	#AIWars
	def restorePeaceAI(self, iMinorCiv, bOpenBorders):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for iActiveCiv in range( iNumActivePlayers ):
			if gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman():
				if teamMinor.isAtWar(iActiveCiv):
					bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
					bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)
					if (not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory):
						teamMinor.makePeace(iActiveCiv)
						if bOpenBorders:
							teamMinor.signOpenBorders(iActiveCiv)

	#AIWars
	def restorePeaceHuman(self, iMinorCiv):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for iActiveCiv in range( iNumActivePlayers ):
			if gc.getPlayer(iActiveCiv).isHuman():
				if gc.getPlayer(iActiveCiv).isAlive():
					if teamMinor.isAtWar(iActiveCiv):
						bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
						bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)
						if (not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory):
							teamMinor.makePeace(iActiveCiv)
				return

	#AIWars
	def minorWars(self, iMinorCiv, iGameTurn):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for city in self.getCityList(iMinorCiv):
			x = city.getX()
			y = city.getY()
			for iActiveCiv in range( iNumActivePlayers ):
				if gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman() and not iActiveCiv == con.iPope:
					if not teamMinor.isAtWar(iActiveCiv):
						if iGameTurn > con.tBirth[iActiveCiv] + 20:
							# Absinthe: probably better to use war maps instead of settler maps, but let the AI concentrate on it's core area first
							#			maybe we should use both settler and war maps? distance calculations would be great, but use too much iterations
							#if (gc.getPlayer(iActiveCiv).getSettlersMaps( con.iMapMaxY-y-1, x ) >= 90 or gc.getPlayer(iActiveCiv).getSettlersMaps( con.iMapMaxY-y-1, x ) == -1):
							#if (gc.getPlayer(iActiveCiv).getWarsMaps( con.iMapMaxY-y-1, x ) >= 2):
							iRndNum = gc.getGame().getSorenRandNum( 10, 'random warmap chance')
							teamActive = gc.getTeam(gc.getPlayer(iActiveCiv).getTeam())
							iWarValue = gc.getPlayer(iActiveCiv).getWarsMaps( con.iMapMaxY-y-1, x )
							if iWarValue >= 10:
								# 100% chance for cities with high war map value
								teamActive.declareWar(iMinorCiv, False, WarPlanTypes.WARPLAN_LIMITED)
								print ("minorWars", city.getName(), gc.getPlayer(iActiveCiv).getCivilizationAdjective(0), gc.getPlayer(iActiveCiv).getSettlersMaps( con.iMapMaxY-y-1, x ), gc.getPlayer(iActiveCiv).getWarsMaps( con.iMapMaxY-y-1, x ), "WARPLAN_LIMITED")
							elif iWarValue >= 6:
								if iRndNum < 7: # 70% chance for cities with medium war map value
									teamActive.declareWar(iMinorCiv, False, WarPlanTypes.WARPLAN_LIMITED)
									print ("minorWars", city.getName(), gc.getPlayer(iActiveCiv).getCivilizationAdjective(0), gc.getPlayer(iActiveCiv).getSettlersMaps( con.iMapMaxY-y-1, x ), gc.getPlayer(iActiveCiv).getWarsMaps( con.iMapMaxY-y-1, x ), "WARPLAN_LIMITED")
							elif iWarValue >= 2:
								if iRndNum < 3: # 30% chance for cities with low war map value
									teamActive.declareWar(iMinorCiv, False, WarPlanTypes.WARPLAN_LIMITED)
									print ("minorWars", city.getName(), gc.getPlayer(iActiveCiv).getCivilizationAdjective(0), gc.getPlayer(iActiveCiv).getSettlersMaps( con.iMapMaxY-y-1, x ), gc.getPlayer(iActiveCiv).getWarsMaps( con.iMapMaxY-y-1, x ), "WARPLAN_LIMITED")

	#AIWars
	# Absinthe: declare war sooner / more frequently if an Indy city has huge value on the civ's war map
	def minorCoreWars(self, iMinorCiv, iGameTurn):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for city in self.getCityList(iMinorCiv):
			x = city.getX()
			y = city.getY()
			for iActiveCiv in range( iNumActivePlayers ):
				if gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman() and not iActiveCiv == con.iPope:
					# Absinthe: do not want to force the AI into these wars with WARPLAN_TOTAL too early
					if iGameTurn > con.tBirth[iActiveCiv] + 40:
						if not teamMinor.isAtWar(iActiveCiv):
							if gc.getPlayer(iActiveCiv).getWarsMaps( con.iMapMaxY-y-1, x ) == 16:
								teamActive = gc.getTeam(gc.getPlayer(iActiveCiv).getTeam())
								teamActive.declareWar(iMinorCiv, False, WarPlanTypes.WARPLAN_TOTAL)
								print ("minorWars", city.getName(), gc.getPlayer(iActiveCiv).getCivilizationAdjective(0), gc.getPlayer(iActiveCiv).getSettlersMaps( con.iMapMaxY-y-1, x ), gc.getPlayer(iActiveCiv).getWarsMaps( con.iMapMaxY-y-1, x ), "WARPLAN_TOTAL")

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
			if gc.getTeam(gc.getPlayer(iMajorCiv).getTeam()).isHasTech(t):
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
		return gc.getGame().getActivePlayer()

	#RiseAndFall
	# Absinthe: separate city flip rules for secession and minor nation mechanics
	def flipUnitsInCitySecession(self, tCityPlot, iNewOwner, iOldOwner):
		plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
		city = plotCity.getPlotCity()
		iNumUnitsInAPlot = plotCity.getNumUnits()
		j = 0 # Absinthe: index for remaining units in the plot
		k = 0 # Absinthe: counter for all units from the original owner

		# Absinthe: one free defender unit
		pPlayer = gc.getPlayer(iOldOwner)
		iFreeDefender = xml.iArcher
		lUnits = [xml.iLineInfantry, xml.iMusketman, xml.iLongbowman, xml.iArbalest, xml.iCrossbowman]
		for iUnit in lUnits:
			if pPlayer.canTrain(self.getUniqueUnit(iNewOwner, iUnit), False, False):
				iFreeDefender = self.getUniqueUnit(iNewOwner, iUnit)
				break
		self.makeUnit(iFreeDefender, iNewOwner, (28, 0), 1)

		for i in range(iNumUnitsInAPlot):
			unit = plotCity.getUnit(j)
			unitType = unit.getUnitType()
			bSafeUnit = False
			if unit.getOwner() == iOldOwner:
				# Absinthe: # no civilian units will flip on city secession
				lNoFlip = [xml.iSettler, xml.iProphet, xml.iArtist, xml.iScientist, xml.iMerchant, xml.iEngineer, xml.iGreatGeneral, xml.iGreatSpy]
				for i in range( 0, len(lNoFlip) ):
					if lNoFlip[i] == unitType:
						bSafeUnit = True
				if not bSafeUnit:
					# Absinthe: instead of switching all units to indy, only 60% chance that the unit will defect
					#			the first unit from the old owner should always defect though
					k += 1
					if ( k < 2 or gc.getGame().getSorenRandNum(10, 'Convert Unit') < 6 ):
						unit.kill(False, con.iBarbarian)
						self.makeUnit(unitType, iNewOwner, [28, 0], 1)
					# Absinthe: skip unit if it won't defect, so it will move out of the city territory
					else:
						j += 1
				# Absinthe: skip unit if civilian
				else:
					j += 1
			# Absinthe: skip unit if from another player
			else:
				j += 1

	#RiseAndFall
	# Absinthe: this is for city flips connected to spawn, collapse and respawn mechanics
	def flipUnitsInCityBefore(self, tCityPlot, iNewOwner, iOldOwner):
		#print ("tCityPlot Before", tCityPlot)
		plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
		city = plotCity.getPlotCity()
		iNumUnitsInAPlot = plotCity.getNumUnits()
		j = 0 # Absinthe: index for remaining units in the plot
		for i in range(iNumUnitsInAPlot):
			unit = plotCity.getUnit(j)
			unitType = unit.getUnitType()
			if unit.getOwner() == iOldOwner:
				unit.kill(False, con.iBarbarian)
				if iNewOwner < con.iNumActivePlayers or unitType > xml.iSettler: # Absinthe: major players can even flip settlers (spawn/respawn mechanics)
					self.makeUnit(unitType, iNewOwner, (28, 0), 1)
			# Absinthe: skip unit if from another player
			else:
				j += 1

	#RiseAndFall
	def flipUnitsInCityAfter(self, tCityPlot, iCiv):
		#moves new units back in their place
		#print ("tCityPlot After", tCityPlot)
		tempPlot = gc.getMap().plot(28, 0)
		if tempPlot.getNumUnits() != 0:
			iNumUnitsInAPlot = tempPlot.getNumUnits()
			#print ("iNumUnitsInAPlot", iNumUnitsInAPlot)
			for i in range(iNumUnitsInAPlot):
				unit = tempPlot.getUnit(0)
				#print("  3Miro Unit Type and Owner ",unit.getUnitType(),"  ",unit.getOwner() )
				unit.setXYOld(tCityPlot[0],tCityPlot[1])
		#cover revealed plots
		gc.getMap().plot(27, 0).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(28, 0).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(29, 0).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(27, 1).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(28, 1).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(29, 1).setRevealed(iCiv, False, True, -1);

		# Absinthe: if there are no units in the city after the flip, add a free defender
		cityPlot = gc.getMap().plot(tCityPlot[0],tCityPlot[1])
		if cityPlot.getNumUnits() == 0:
			# The latest available ranged/gun class
			RangedClass = self.getUniqueUnit(iCiv, xml.iArcher)
			lRangedList = [xml.iLineInfantry, xml.iMusketman, xml.iLongbowman, xml.iArbalest, xml.iCrossbowman, xml.iArcher]
			for iUnit in lRangedList:
				if gc.getPlayer(iCiv).canTrain(self.getUniqueUnit(iCiv, iUnit), False, False):
					RangedClass = self.getUniqueUnit(iCiv, iUnit)
					break
			self.makeUnit(RangedClass, iCiv, tCityPlot, 1)

	def killUnitsInArea(self, tTopLeft, tBottomRight, iCiv):
		for (x, y) in self.getPlotList(tTopLeft, tBottomRight):
			killPlot = gc.getMap().plot(x,y)
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				iSkippedUnit = 0
				for i in range(iNumUnitsInAPlot):
					unit = killPlot.getUnit(iSkippedUnit)
					if unit.getOwner() == iCiv:
						unit.kill(False, con.iBarbarian)
					else:
						iSkippedUnit += 1

	def killAllUnitsInArea(self, tTopLeft, tBottomRight):
		for (x, y) in self.getPlotList(tTopLeft, tBottomRight):
			killPlot = gc.getMap().plot(x,y)
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				for i in range(iNumUnitsInAPlot):
					unit = killPlot.getUnit(0)
					unit.kill(False, con.iBarbarian)

	def killUnitsInPlots(self, lPlots, iCiv):
		for (x, y) in lPlots:
			killPlot = gc.getMap().plot(x,y)
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				iSkippedUnit = 0
				for i in range(iNumUnitsInAPlot):
					unit = killPlot.getUnit(iSkippedUnit)
					if unit.getOwner() == iCiv:
						unit.kill(False, con.iBarbarian)
					else:
						iSkippedUnit += 1

	#RiseAndFall
	# Absinthe: create units at (28, 0), in the unreachable desert area, near the autoplay plot
	def flipUnitsInArea(self, tTopLeft, tBottomRight, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
		"""Deletes, recreates units in 28, 0 and moves them to the previous tile.
		If there are units belonging to others in that plot and the new owner is barbarian, the units aren't recreated.
		Settlers aren't created.
		If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
		# Absinthe: safety check, kill all units on the tempplot before the flip
		killPlot = gc.getMap().plot(28, 0)
		iNumUnitsInAPlot = killPlot.getNumUnits()
		if iNumUnitsInAPlot > 0:
			for i in range(iNumUnitsInAPlot):
				unit = killPlot.getUnit(0)
				unit.kill(False, con.iBarbarian)
		for (x, y) in self.getPlotList(tTopLeft, tBottomRight):
			killPlot = gc.getMap().plot(x,y)
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				bRevealedZero = False
				if gc.getMap().plot(28, 0).isRevealed(iNewOwner, False):
					bRevealedZero = True
				#print ("killplot", x, y)
				if bSkipPlotCity and killPlot.isCity():
					#print (killPlot.isCity())
					#print 'do nothing'
					pass
				else:
					j = 0
					for i in range(iNumUnitsInAPlot):
						unit = killPlot.getUnit(j)
						#print ("killplot", x, y, unit.getUnitType(), unit.getOwner(), "j", j)
						if unit.getOwner() == iOldOwner:
							unit.kill(False, con.iBarbarian)
							if bKillSettlers:
								if (unit.getUnitType() > iSettler):
									self.makeUnit(unit.getUnitType(), iNewOwner, (28, 0), 1)
							else:
								if (unit.getUnitType() >= iSettler): #skip animals
									self.makeUnit(unit.getUnitType(), iNewOwner, (28, 0), 1)
						else:
							j += 1
					tempPlot = gc.getMap().plot(28, 0)
					#moves new units back in their place
					if tempPlot.getNumUnits() != 0:
						iNumUnitsInAPlot = tempPlot.getNumUnits()
						for i in range(iNumUnitsInAPlot):
							unit = tempPlot.getUnit(0)
							unit.setXYOld(x,y)
						iCiv = iNewOwner
						if not bRevealedZero:
							gc.getMap().plot(27, 0).setRevealed(iCiv, False, True, -1)
							gc.getMap().plot(28, 0).setRevealed(iCiv, False, True, -1)
							gc.getMap().plot(29, 0).setRevealed(iCiv, False, True, -1)
							gc.getMap().plot(27, 1).setRevealed(iCiv, False, True, -1)
							gc.getMap().plot(28, 1).setRevealed(iCiv, False, True, -1)
							gc.getMap().plot(29, 1).setRevealed(iCiv, False, True, -1)


	#RiseAndFall
	# Absinthe: similar to the function above, but flips on a list of plots
	def flipUnitsInPlots(self, lPlots, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
		"""Deletes, recreates units in 28, 0 and moves them to the previous tile.
		If there are units belonging to others in that plot and the new owner is barbarian, the units aren't recreated.
		Settlers aren't created.
		If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
		# Absinthe: safety check, kill all units on the tempplot before the flip
		killPlot = gc.getMap().plot(28, 0)
		iNumUnitsInAPlot = killPlot.getNumUnits()
		if iNumUnitsInAPlot > 0:
			for i in range(iNumUnitsInAPlot):
				unit = killPlot.getUnit(0)
				unit.kill(False, con.iBarbarian)
		#print ("searched plots", lPlots)
		for (x, y) in lPlots:
			#print ("searched plot", (x, y))
			killPlot = gc.getMap().plot(x,y)
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				bRevealedZero = False
				if gc.getMap().plot(28, 0).isRevealed(iNewOwner, False):
					bRevealedZero = True
				#print ("killplot", x, y)
				if bSkipPlotCity and killPlot.isCity():
					#print (killPlot.isCity())
					#print 'do nothing'
					pass
				else:
					j = 0
					for i in range(iNumUnitsInAPlot):
						unit = killPlot.getUnit(j)
						#print ("killplot", x, y, unit.getUnitType(), unit.getOwner(), "j", j)
						if unit.getOwner() == iOldOwner:
							unit.kill(False, con.iBarbarian)
							if bKillSettlers:
								if unit.getUnitType() > iSettler:
									self.makeUnit(unit.getUnitType(), iNewOwner, (28, 0), 1)
							else:
								if unit.getUnitType() >= iSettler: #skip animals
									self.makeUnit(unit.getUnitType(), iNewOwner, (28, 0), 1)
						else:
							j += 1
					tempPlot = gc.getMap().plot(28, 0)
					#moves new units back in their place
					if tempPlot.getNumUnits() > 0:
						iNumUnitsInAPlot = tempPlot.getNumUnits()
						for i in range(iNumUnitsInAPlot):
							unit = tempPlot.getUnit(0)
							unit.setXYOld(x,y)
						iCiv = iNewOwner
						if  not bRevealedZero:
							gc.getMap().plot(27, 0).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(28, 0).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(29, 0).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(27, 1).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(28, 1).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(29, 1).setRevealed(iCiv, False, True, -1);


	#RiseAndFall
	def flipCity(self, tCityPlot, bFlipType, bKillUnits, iNewOwner, lOldOwners):
		"""Changes owner of city specified by tCityPlot.
		bFlipType specifies if it's conquered or traded.
		If bKillUnits != 0 all the units in the city will be killed.
		iRetainCulture will determine the split of the current culture between old and new owner. -1 will skip
		lOldOwners is a list. Flip happens only if the old owner is in the list.
		An empty list will cause the flip to always happen."""
		pNewOwner = gc.getPlayer(iNewOwner)
		if gc.getMap().plot(tCityPlot[0], tCityPlot[1]).isCity():
			city = gc.getMap().plot(tCityPlot[0], tCityPlot[1]).getPlotCity()
			if not city.isNone():
				iOldOwner = city.getOwner()
				if iOldOwner in lOldOwners or not lOldOwners:
					if bKillUnits:
						killPlot = gc.getMap().plot( tCityPlot[0], tCityPlot[1] )
						for i in range(killPlot.getNumUnits()):
							unit = killPlot.getUnit(0)
							unit.kill(False, iNewOwner)
					if bFlipType: #conquest
						if city.getPopulation() <= 2:
							city.changePopulation(1)
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
		if pCity.isCity():
			iCurrentCityCulture = city.getCulture(iOldOwner)
		#	print ("iCulturePercent", iCulturePercent)
		#	print ("iCurrentCityCulture", iCurrentCityCulture)
		#	print ("iCurrentCityCulture2", city.getCulture(iNewOwner))
		#	print ("iCurrentCityCultureOldOwner", iCurrentCityCulture*(100-iCulturePercent)/100)
		#	print ("iCurrentCityCultureNewOwner", iCurrentCityCulture*iCulturePercent/100)

			if iNewOwner != con.iBarbarian:
				city.setCulture(con.iBarbarian, 0, True)

			# Absinthe: changeCulture instead of setCulture for the new civ, so previously acquired culture won't disappear
			#			for the old civ some of the culture is lost when the city is conquered
			#			note that this is the amount of culture "resource" for each civ, not population percent
			city.changeCulture(iNewOwner, iCurrentCityCulture*iCulturePercent/100, False)
			# Absinthe: only half of the amount is lost, so only 25% on city secession and minor nation revolts
			city.setCulture(iOldOwner, iCurrentCityCulture*(100-(iCulturePercent/2))/100, False)

			if city.getCulture(iNewOwner) <= 10:
				city.setCulture(iNewOwner, 10, False)
		#	print ("iCurrentCityCulture3", city.getCulture(iOldOwner))
		#	print ("iCurrentCityCulture4", city.getCulture(iNewOwner))

		#halve barbarian culture in a broader area
		if bBarbarian2x2Decay or bBarbarian2x2Conversion:
			lMinors = [con.iBarbarian, con.iIndependent, con.iIndependent2, con.iIndependent3, con.iIndependent4]
			if iNewOwner not in lMinors:
				for (x, y) in self.surroundingPlots(tCityPlot, 2):
					for iMinor in lMinors:
						iPlotMinorCulture = gc.getMap().plot(x, y).getCulture(iMinor)
						if iPlotMinorCulture > 0:
							if gc.getMap().plot(x, y).getPlotCity().isNone() or (x, y) == tCityPlot:
								if bBarbarian2x2Decay:
									gc.getMap().plot(x, y).setCulture(iMinor, iPlotMinorCulture/4, True)
								if bBarbarian2x2Conversion:
									gc.getMap().plot(x, y).setCulture(iMinor, 0, True)
									# Absinthe: changeCulture instead of setCulture for the new civ, so previously acquired culture won't disappear
									gc.getMap().plot(x, y).changeCulture(iNewOwner, iPlotMinorCulture, True)

		#plot
		for (x, y) in self.surroundingPlots(tCityPlot):
			pCurrent = gc.getMap().plot(x, y)
			iCurrentPlotCulture = pCurrent.getCulture(iOldOwner)

			if pCurrent.isCity():
				# Absinthe: changeCulture instead of setCulture for the new civ, so previously acquired culture won't disappear
				pCurrent.changeCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/100, True)
				# Absinthe: only half of the amount is lost
				pCurrent.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent/2)/100, True)
			else:
				# Absinthe: changeCulture instead of setCulture for the new civ, so previously acquired culture won't disappear
				pCurrent.changeCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/3/100, True)
				# Absinthe: only half of the amount is lost
				pCurrent.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent/6)/100, True)

			#cut other players culture
##				for iCiv in range(iNumPlayers):
##					if (iCiv != iNewOwner and iCiv != iOldOwner):
##						iPlotCulture = gc.getMap().plot(x, y).getCulture(iCiv)
##						if (iPlotCulture > 0):
##							gc.getMap().plot(x, y).setCulture(iCiv, iPlotCulture/3, True)
			#print (x, y, pCurrent.getCulture(iNewOwner), ">", pCurrent.getCulture(iOldOwner))

			if not pCurrent.isCity():
				if bAlwaysOwnPlots:
					pCurrent.setOwner(iNewOwner)
				else:
					if pCurrent.getCulture(iNewOwner)*4 > pCurrent.getCulture(iOldOwner):
						pCurrent.setOwner(iNewOwner)
				#print ("NewOwner", pCurrent.getOwner())


	#RFCEventHandler
	def spreadMajorCulture(self, iMajorCiv, iX, iY):
		# Absinthe: spread some of the major civ's culture to the nearby indy cities
		for (x, y) in self.surroundingPlots((iX, iY), 4):
			pCurrent = gc.getMap().plot(x, y)
			if pCurrent.isCity():
				city = pCurrent.getPlotCity()
				#print ("city.getPreviousOwner", city.getPreviousOwner())
				if city.getPreviousOwner() >= iNumMajorPlayers:
					iMinor = city.getPreviousOwner()
					iDen = 25
					if gc.getPlayer(iMajorCiv).getSettlersMaps( con.iMapMaxY-y-1, x ) >= 400:
						iDen = 10
					elif gc.getPlayer(iMajorCiv).getSettlersMaps( con.iMapMaxY-y-1, x ) >= 150:
						iDen = 15

					# Absinthe: changeCulture instead of setCulture, otherwise previous culture will be lost
					iMinorCityCulture = city.getCulture(iMinor)
					#print ("iMinorculture", city.getCulture(iMinor) )
					#print ("iMajorculturebefore", city.getCulture(iMajorCiv) )
					city.changeCulture(iMajorCiv, iMinorCityCulture/iDen, True)
					#print ("iMajorcultureafter", city.getCulture(iMajorCiv) )

					iMinorPlotCulture = pCurrent.getCulture(iMinor)
					pCurrent.changeCulture(iMajorCiv, iMinorPlotCulture/iDen, True)


	#UniquePowers, Crusades, RiseAndFall
	def convertPlotCulture(self, pCurrent, iCiv, iPercent, bOwner):

		if pCurrent.isCity():
			city = pCurrent.getPlotCity()
			iCivCulture = city.getCulture(iCiv)
			iLoopCivCulture = 0
			for iLoopCiv in range(iNumTotalPlayers):
				if iLoopCiv != iCiv:
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
			if iLoopCiv != iCiv:
				iLoopCivCulture += pCurrent.getCulture(iLoopCiv)
				pCurrent.setCulture(iLoopCiv, pCurrent.getCulture(iLoopCiv)*(100-iPercent)/100, True)
		pCurrent.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)
		if bOwner:
			pCurrent.setOwner(iCiv)


	#RiseAndFall
	def pushOutGarrisons(self, tCityPlot, iOldOwner):
		tDestination = (-1, -1)
		for (x, y) in self.surroundingPlots(tCityPlot, 2):
			pDestination = gc.getMap().plot(x, y)
			if pDestination.getOwner() == iOldOwner and not pDestination.isWater() and not pDestination.isImpassable():
				tDestination = (x, y)
				break
		if tDestination != (-1, -1):
			plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
			iNumUnitsInAPlot = plotCity.getNumUnits()
			j = 0
			for i in range(iNumUnitsInAPlot):
				unit = plotCity.getUnit(j)
				if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
					#print("  3Miro 2 Unit Type and Owner ",unit.getUnitType(),"  ",unit.getOwner() )
					unit.setXYOld(tDestination[0], tDestination[1])
				else:
					j = j + 1

	#RiseAndFall
	def relocateSeaGarrisons(self, tCityPlot, iOldOwner):
		tDestination = (-1, -1)
		for city in self.getCityList(iOldOwner):
			if city.isCoastalOld():
				tDestination = (city.getX(), city.getY())
				break
		if tDestination == (-1, -1):
			for (x, y) in self.surroundingPlots(tCityPlot, 12):
				pDestination = gc.getMap().plot(x, y)
				if pDestination.isWater():
					tDestination = (x, y)
					break
		if tDestination != (-1, -1):
			plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
			iNumUnitsInAPlot = plotCity.getNumUnits()
			j = 0
			for i in range(iNumUnitsInAPlot):
				unit = plotCity.getUnit(j)
				if unit.getDomainType() == DomainTypes.DOMAIN_SEA:
					#print("  3Miro 3 Unit Type and Owner ",unit.getUnitType(),"  ",unit.getOwner() )
					unit.setXYOld(tDestination[0], tDestination[1])
				else:
					j = j + 1

	#RiseAndFall
	def createGarrisons(self, tCityPlot, iNewOwner, iNumUnits):
		pPlayer = gc.getPlayer(iNewOwner)

		# Sedna17: makes garrison units based on new tech tree/units
		iUnitType = xml.iArcher
		lUnits = [xml.iLineInfantry, xml.iMusketman, xml.iArquebusier, xml.iArbalest, xml.iArbalest, xml.iCrossbowman]
		for iUnit in lUnits:
			if pPlayer.canTrain(self.getUniqueUnit(iNewOwner, iUnit), False, False):
				iUnitType = self.getUniqueUnit(iNewOwner, iUnit)
				break

		self.makeUnit(iUnitType, iNewOwner, tCityPlot, iNumUnits)


	#RiseAndFall, Stability
	# Absinthe: currently unused
	def killCiv(self, iCiv, iNewCiv):
		self.clearPlague(iCiv)
		for city in self.getCityList(iPlayer):
			tCoords = (city.getX(), city.getY())
			self.cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
			self.flipCity(tCoords, 0, 0, iNewCiv, [iCiv]) #by trade because by conquest may raze the city
			#city.setHasRealBuilding(con.iPlague, False) #buggy
		self.flipUnitsInArea([0,0], [con.iMapMaxX,con.iMapMaxY], iNewCiv, iCiv, False, True)

		self.resetUHV(iCiv)
		self.setLastTurnAlive(iCiv, gc.getGame().getGameTurn())
		# Absinthe: respawn status
		if gc.getPlayer( iCiv ).getRespawnedAlive():
			gc.getPlayer( iCiv ).setRespawnedAlive( False )


	def killAndFragmentCiv(self, iCiv, bBarbs, bAssignOneCity):
		self.clearPlague(iCiv)
		iNumLoyalCities = 0
		iCounter = gc.getGame().getSorenRandNum(6, 'random start')
		for city in self.getCityList(iCiv):
			tCoords = (city.getX(), city.getY())
			iX, iY = tCoords
			pCurrent = gc.getMap().plot(iX, iY)
			#1 loyal city for the human player
			if bAssignOneCity and iNumLoyalCities < 1 and city.isCapital():
				iNumLoyalCities += 1
				#gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iNewCiv1, False, -1) #too dangerous?
				#gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iNewCiv2, False, -1)
				for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
					gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(i, False, -1)
				continue
			#assign to neighbours first
			bNeighbour = False
			iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
			for j in range(iNumPlayers): #only major players
				iLoopCiv = (j + iRndnum) % iNumPlayers
				if gc.getPlayer(iLoopCiv).isAlive() and iLoopCiv != iCiv and not gc.getPlayer(iLoopCiv).isHuman():
					if pCurrent.getCulture(iLoopCiv) > 0:
						if (pCurrent.getCulture(iLoopCiv)*100 / (pCurrent.getCulture(iLoopCiv) + pCurrent.getCulture(iCiv) + pCurrent.getCulture(iBarbarian) + pCurrent.getCulture(iIndependent) + pCurrent.getCulture(iIndependent2)) >= 5): #change in vanilla
							self.flipUnitsInCityBefore(tCoords, iLoopCiv, iCiv)
							self.setTempFlippingCity(tCoords)
							self.flipCity(tCoords, 0, 0, iLoopCiv, [iCiv])
							#city.setHasRealBuilding(con.iPlague, False) #buggy
							#Sedna17: Possibly buggy, used to flip units in 2 radius, which could take us outside the map.
							self.flipUnitsInArea((iX-1, iY-1), (iX+1, iY+1), iLoopCiv, iCiv, False, True)
							self.flipUnitsInCityAfter(self.getTempFlippingCity(), iLoopCiv)
							bNeighbour = True
							break
			if bNeighbour:
				continue
			#fragmentation in 2
			if not bBarbs:
				#if (iCounter % 2 == 0):
				#	iNewCiv = iNewCiv1
				#elif (iCounter % 2 == 1):
				#	iNewCiv = iNewCiv2
				iNewCiv = con.iIndepStart + gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random indep' )
				self.flipUnitsInCityBefore(tCoords, iNewCiv, iCiv)
				self.setTempFlippingCity(tCoords)
				self.cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
				self.flipCity(tCoords, 0, 0, iNewCiv, [iCiv])
				#city.setHasRealBuilding(con.iPlague, False) #buggy
				self.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
				iCounter += 1
				self.flipUnitsInArea((iX-1, iY-1), (iX+1, iY+1), iNewCiv, iCiv, False, True)
			#fragmentation with barbs
			else:
				#if (iCounter % 3 == 0):
				#	iNewCiv = iNewCiv1
				#elif (iCounter % 3 == 1):
				#	iNewCiv = iNewCiv2
				#elif (iCounter % 3 == 2):
				#	iNewCiv = iNewCiv3
				iNewCiv = con.iIndepStart + gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 2, 'random indep' )
				if iNewCiv == con.iIndepEnd + 1:
					iNewCiv = iBarbarian
				self.flipUnitsInCityBefore(tCoords, iNewCiv, iCiv)
				self.setTempFlippingCity(tCoords)
				self.cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
				self.flipCity(tCoords, 0, 0, iNewCiv, [iCiv])
				#city.setHasRealBuilding(con.iPlague, False) #buggy
				self.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
				iCounter += 1
				self.flipUnitsInArea((iX-1, iY-1), (iX+1, iY+1), iNewCiv, iCiv, False, True)
		if not bAssignOneCity:
			#self.flipUnitsInArea((0,0), (123,67), iNewCiv1, iCiv, False, True) #causes a bug: if a unit was inside another city's civ, when it becomes independent or barbarian, may raze it
			self.killUnitsInArea((0, 0), (con.iMapMaxX, con.iMapMaxY), iCiv)
			self.resetUHV(iCiv)
		self.setLastTurnAlive(iCiv, gc.getGame().getGameTurn())
		# Absinthe: respawn status
		#print ("getRespawnedAlive", gc.getPlayer( iCiv ).getRespawnedAlive())
		if gc.getPlayer( iCiv ).getRespawnedAlive():
			gc.getPlayer( iCiv ).setRespawnedAlive( False )


	def resetUHV(self, iPlayer):
		if iPlayer < iNumMajorPlayers:
			pPlayer = gc.getPlayer( iPlayer )
			for i in range(3):
				if pPlayer.getUHV( i ) == -1:
					pPlayer.setUHV( i, 0 )


	def clearPlague(self, iCiv):
		for city in self.getCityList(iCiv):
			if city.hasBuilding(xml.iPlague):
				city.setHasRealBuilding(xml.iPlague, False)


	#AIWars
	def isAVassal(self, iCiv):
		return gc.getTeam(gc.getPlayer(iCiv).getTeam()).isAVassal()


	def isActive(self, iPlayer):
		"""Returns true if the player is spawned and alive."""
		if gc.getPlayer(iPlayer).getNumCities() < 1: return False
		if not gc.getPlayer(iPlayer).isAlive: return False
		iGameTurn = gc.getGame().getGameTurn()
		if iGameTurn < con.tBirth[iPlayer]: return False
		return True


	# UP, UHV, idea from DoC
	def getMaster(self, iCiv):
		team = gc.getTeam(gc.getPlayer(iCiv).getTeam())
		if team.isAVassal():
			for iMaster in range(iNumTotalPlayers):
				if team.isVassal(iMaster):
					return iMaster
		return -1


	def squareSearch( self, tTopLeft, tBottomRight, function, argsList ): #by LOQ
		"""Searches all tile in the square from tTopLeft to tBottomRight and calls function for every tile, passing argsList."""
		tPaintedList = []
		for tPlot in self.getPlotList(tTopLeft, tBottomRight):
			bPaintPlot = function(tPlot, argsList)
			if bPaintPlot:
				tPaintedList.append(tPlot)
		return tPaintedList

	def outerInvasion( self, tCoords, argsList ):
		"""Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.isHills() or pCurrent.isFlatlands():
			if pCurrent.getFeatureType() not in [xml.iMarsh, xml.iJungle]:
				if not pCurrent.isCity() and not pCurrent.isUnit():
					if pCurrent.countTotalCulture() == 0:
						return True
		return False

	def forcedInvasion( self, tCoords, argsList ):
		"""Plot is valid if it's hill or flatlands, it isn't marsh or jungle, and it isn't occupied by a unit or city."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.isHills() or pCurrent.isFlatlands():
			if pCurrent.getFeatureType() not in [xml.iMarsh, xml.iJungle]:
				if not pCurrent.isCity() and not pCurrent.isUnit():
					return True
		return False

	def outerSeaSpawn( self, tCoords, argsList ):
		"""Plot is valid if it's water (coast), it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.isWater() and pCurrent.getTerrainType() == xml.iTerrainCoast:
			if not pCurrent.isUnit():
				if pCurrent.countTotalCulture() == 0:
					for (x, y) in self.surroundingPlots(tCoords):
						if gc.getMap().plot(x, y).isUnit():
							return False
					return True
		return False

	def innerSeaSpawn( self, tCoords, argsList ):
		"""Plot is valid if it's water (coast) and it isn't occupied by any unit. Unit check extended to adjacent plots."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.isWater() and pCurrent.getTerrainType() == xml.iTerrainCoast:
			if not pCurrent.isUnit():
				for (x, y) in self.surroundingPlots(tCoords):
					if gc.getMap().plot(x, y).isUnit():
						return False
				return True
		return False

	def outerSpawn( self, tCoords, argsList ):
		"""Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory. Unit check extended to adjacent plots."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.isHills() or pCurrent.isFlatlands():
			if pCurrent.getFeatureType() not in [xml.iMarsh, xml.iJungle]:
				if not pCurrent.isCity() and not pCurrent.isUnit():
					if pCurrent.countTotalCulture() == 0:
						for (x, y) in self.surroundingPlots(tCoords):
							if gc.getMap().plot(x, y).isUnit():
								return False
						return True
		return False

	def innerSpawn( self, tCoords, argsList ):
		"""Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it's in a given civ's territory. Unit check extended to adjacent plots."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.isHills() or pCurrent.isFlatlands():
			if pCurrent.getFeatureType() not in [xml.iMarsh, xml.iJungle]:
				if not pCurrent.isCity() and not pCurrent.isUnit():
					if pCurrent.getOwner() in argsList:
						for (x, y) in self.surroundingPlots(tCoords):
							if gc.getMap().plot(x, y).isUnit():
								return False
						return True
		return False

	def goodPlots( self, tCoords, argsList ):
		"""Plot is valid if it's hill or flatlands, it isn't desert, tundra, marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory. Unit check extended to adjacent plots."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.isHills() or pCurrent.isFlatlands():
			if not pCurrent.isImpassable():
				if not pCurrent.isCity() and not pCurrent.isUnit():
					if pCurrent.getTerrainType() not in [xml.iTerrainDesert, xml.iTerrainTundra] and pCurrent.getFeatureType() not in [xml.iMarsh, xml.iJungle]:
						if pCurrent.countTotalCulture() == 0:
							return True
		return False

	def ownedCityPlots( self, tCoords, argsList ):
		"""Plot is valid if it contains a city belonging to the given civ."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.getOwner() == argsList:
			if pCurrent.isCity():
				return True
		return False

	def ownedPlots( self, tCoords, argsList ):
		"""Plot is valid if it is in the given civ's territory."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.getOwner() == argsList:
			return True
		return False

	def goodOwnedPlots( self, tCoords, argsList ):
		"""Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit and if it is in the given civ's territory."""
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if pCurrent.isHills() or pCurrent.isFlatlands():
			if pCurrent.getFeatureType() not in [xml.iMarsh, xml.iJungle]:
				if not pCurrent.isCity() and not pCurrent.isUnit():
					if pCurrent.getOwner() == argsList:
						return True
		return False

	def collapseImmune( self, iCiv ):
		#3MiroUP: Emperor
		if gc.hasUP(iCiv,con.iUP_Emperor):
			#print(" 3Miro: has the power: ",iCiv)
			plot = gc.getMap().plot( con.tCapitals[iCiv][0], con.tCapitals[iCiv][1])
			if plot.isCity():
				#print(" 3Miro: has the city: ",iCiv)
				if plot.getOwner() == iCiv:
					#print(" 3Miro: collapse immune ",iCiv)
					return true
		#print(" 3Miro: not immune ",iCiv)
		return false

	def collapseImmuneCity( self, iCiv, x, y ):
		#3MiroUP: Emperor
		if gc.hasUP(iCiv, con.iUP_Emperor):
			plot = gc.getMap().plot( con.tCapitals[iCiv][0], con.tCapitals[iCiv][1])
			if plot.isCity():
				if plot.getOwner() == iCiv:
					if (x >= con.tCoreAreasTL[iCiv][0]) and (x <= con.tCoreAreasBR[iCiv][0]) and (y >= con.tCoreAreasTL[iCiv][1]) and (y <= con.tCoreAreasBR[iCiv][1]):
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
		return sd.scriptDict['lPersecutionData'][0], sd.scriptDict['lPersecutionData'][1], sd.scriptDict['lPersecutionData'][2]

	def setPersecutionData(self, iPlotX, iPlotY, iUnitID):
		sd.scriptDict['lPersecutionData'] = [iPlotX, iPlotY, iUnitID]

	def getPersecutionReligions(self):
		return sd.scriptDict['lPersecutionReligions']

	def setPersecutionReligions(self, val):
		sd.scriptDict['lPersecutionReligions'] = val
	#Absinthe: end

	#Absinthe: persecution
	def prosecute( self, iPlotX, iPlotY, iUnitID, iReligion=None ):
		"""Removes one religion from the city and handles the consequences."""

		if gc.getMap().plot(iPlotX, iPlotY).isCity():
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
						# so this will be remain the iReligion for further calculations
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
		if (iPlotX, iPlotY) == con.tJerusalem:
			iChance -= 25
		# lower chance if the city has the chosen religion's buildings/wonders:
		iChance -= (len(lReligionBuilding) * 8 + lReligionWonder * 17)		# the wonders have an extra chance reduction (in addition to the first reduction)
		# bonus for the AI:
		if self.getHumanID() != iOwner:
			iChance += 15

		if gc.getGame().getSorenRandNum(100, "purge chance") < iChance:
		# on successful persecution:
			print ("Successful persecution for civ:", iOwner, iReligion, (iPlotX, iPlotY), city.getName())

			# remove a single non-state religion and its buildings from the city, count the loot
			iLootModifier = 3 * city.getPopulation() / city.getReligionCount()
			iLoot = 5 + iLootModifier
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
			iLoot = iLoot + gc.getGame().getSorenRandNum(iLoot, 'random loot')
			pPlayer.changeGold(iLoot)

			# add faith for the persecution itself (there is an indirect increase too, the negative modifier from having a non-state religion is gone)
			pPlayer.changeFaith( 1 )

			# apply diplomatic penalty
			for iLoopPlayer in range(con.iNumPlayers):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive() and iLoopPlayer != iOwner:
					if pLoopPlayer.getStateReligion() == iReligion:
						pLoopPlayer.AI_changeAttitudeExtra(iOwner, -1)

			# count minor religion persecutions - resettling jewish people on persecution is handled another way
			#if ( i == minorReligion ){ // 3Miro: count the minor religion prosecutions
			#minorReligionRefugies++;
			#gc.setMinorReligionRefugies( 0 )

			# interface message for the player
			CyInterface().addMessage(iOwner, False, con.iDuration, localText.getText("TXT_KEY_MESSAGE_INQUISITION", (city.getName(), gc.getReligionInfo(iReligion).getDescription(), iLoot)), "AS2D_PLAGUE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), ColorTypes(con.iGreen), iPlotX, iPlotY, True, True)

			# Jews may spread to another random city
			if iReligion == xml.iJudaism:
				if gc.getGame().getSorenRandNum(100, "Judaism spread chance") < 80:
					tCity = self.selectRandomCity()
					self.spreadJews(tCity, xml.iJudaism)
					pSpreadCity = gc.getMap().plot(tCity[0], tCity[1]).getPlotCity()
					if pSpreadCity.getOwner() == iOwner:
						CyInterface().addMessage(iOwner, False, con.iDuration, localText.getText("TXT_KEY_MESSAGE_JEWISH_MOVE_OWN_CITY", (city.getName(), pSpreadCity.getName())), "AS2D_PLAGUE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), ColorTypes(con.iGreen), iPlotX, iPlotY, True, True)
					else:
						CyInterface().addMessage(iOwner, False, con.iDuration, localText.getText("TXT_KEY_MESSAGE_JEWISH_MOVE", (city.getName(), )), "AS2D_PLAGUE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), ColorTypes(con.iGreen), iPlotX, iPlotY, True, True)

			# persecution countdown for the civ (causes indirect instability - stability.recalcCity)
			if gc.hasUP(iOwner,con.iUP_Inquisition): # Spanish UP
				pPlayer.changeProsecutionCount( 4 )
			else:
				#self.setProsecutionCount( iOwner, self.getProsecutionCount( iOwner ) + 10 )
				pPlayer.changeProsecutionCount( 8 )
				# also some swing instability:
				pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() - 3  )

			# "We cannot forget your cruel oppression" unhappiness from persecution
			city.changeHurryAngerTimer(city.flatHurryAngerLength())

		else: # on failed persecution:
			print ("Unsuccessful persecution for civ:", iOwner, iReligion, (iPlotX, iPlotY), city.getName())
			CyInterface().addMessage(iOwner, False, con.iDuration, localText.getText("TXT_KEY_MESSAGE_INQUISITION_FAIL", (city.getName(), )), "AS2D_SABOTAGE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), ColorTypes(con.iRed), iPlotX, iPlotY, True, True)

			# persecution countdown for the civ (causes indirect instability - stability.recalcCity)
			if gc.hasUP(iOwner,con.iUP_Inquisition): # Spanish UP
				pPlayer.changeProsecutionCount( 2 )
			else:
				pPlayer.changeProsecutionCount( 4 )

		# start a small revolt
		city.changeCultureUpdateTimer(1);
		city.changeOccupationTimer(1);

		# consume the inquisitor
		pUnit.kill(0, -1)

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
		for iPlayer in range( con.iNumPlayers ):	# current civ range is iNumPlayers, so it can only be a major player's city
			if gc.getPlayer(iPlayer).isAlive():
				cityList.extend(self.getCityList(iPlayer))
		if cityList:
			city = self.getRandomEntry(cityList)
			return (city.getX(), city.getY())
		return False


	def spreadJews(self, tPlot, iReligion):
		if tPlot:
			plot = gc.getMap().plot( tPlot[0], tPlot[1] )
			if not plot.getPlotCity().isNone():
				plot.getPlotCity().setHasReligion(iReligion, 1, 0, 0) # puts the religion into this city
				return True
			else:
				return False
		return False


	def isIndep( self, iCiv ):
		if iCiv >= con.iIndepStart and iCiv <= con.iIndepEnd:
			return True
		return False


	#Absinthe: old stability system, not used anymore
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
		iGlobeLayerOptionsY_Regular = 170 # distance from bottom edge
		iGlobeLayerOptionsY_Minimal = 38 # distance from bottom edge
		iGlobeLayerOptionsWidth = 400
		iGlobeLayerOptionHeight = 20
		iY = yResolution - iGlobeLayerOptionsY_Regular
		iCurY = iY
		iMaxTextWidth = -1
		for iCiv in range( con.iNumMajorPlayers - 1 ): # all major civs except the Papal States
			szDropdownName = str("StabilityOverlayCiv") + str(iCiv)
			szCaption = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
			if iCiv == self.getHumanID():
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
				if RFCEMaps.tProvinceMap[plot.getY()][plot.getX()] == -1: # ocean and non-province tiles
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
		if iScreenIsUp == 1:
			# clear the highlight
			engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)

			# if no civ was selected before
			global iSelectedCivID
			if iSelectedCivID == -1:
				iSelectedCivID = iHuman

			# apply the highlight
			for i in range(map.numPlots()):
				plot = map.plotByIndex(i)
				if gc.getGame().isDebugMode() or plot.isRevealed(iHumanTeam, False):
					if RFCEMaps.tProvinceMap[plot.getY()][plot.getX()] == -1: # ocean and non-province tiles
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
		iGlobeLayerOptionsY_Regular = 170 # distance from bottom edge
		iGlobeLayerOptionsY_Minimal = 38 # distance from bottom edge
		iGlobeLayerOptionsWidth = 400
		iGlobeLayerOptionHeight = 20
		iY = yResolution - iGlobeLayerOptionsY_Regular
		iCurY = iY
		iMaxTextWidth = -1
		for iCiv in range( con.iNumMajorPlayers - 1 ): # all major civs except the Papal States
			szDropdownName = str("StabilityOverlayCiv") + str(iCiv)
			szCaption = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
			if iCiv == iSelectedCivID:
				szBuffer = "  <color=0,255,255>%s</color>  " % (szCaption)
			elif iCiv == self.getHumanID():
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
				if RFCEMaps.tProvinceMap[plot.getY()][plot.getX()] == -1: # ocean and non-province tiles
					szColor = "COLOR_GREY"
				else:
					szColor = colors[self.getProvinceStabilityLevel(iChoice, plot.getProvince())]
				engine.addColoredPlotAlt(plot.getX(), plot.getY(), int(PlotStyles.PLOT_STYLE_BOX_FILL), int(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER), szColor, .2)


	def getProvinceStabilityLevel(self, iCiv, iProvince):
		"""Returns the stability level of the province for the given civ."""

		pPlayer = gc.getPlayer( iCiv )
		iProvType = pPlayer.getProvinceType( iProvince )
		if iProvType == con.iProvinceCore:
			return 4 # core
		elif iProvType == con.iProvinceNatural:
			return 3 # natural/historical
		elif iProvType == con.iProvincePotential:
			return 2 # potential
		elif iProvType == con.iProvinceOuter:
			return 1 # border/contested
		else:
			return 0 # unstable
	#Absinthe: end

	def getScenario(self):
		if gc.getPlayer(con.iBurgundy).isPlayable(): return con.i500ADScenario
		return con.i1200ADScenario

	def getScenarioStartYear(self):
		lStartYears = [500, 1200]
		return lStartYears[self.getScenario()]

	def getScenarioStartTurn(self):
		lStartTurn = [xml.i500AD, xml.i1200AD]
		return lStartTurn[self.getScenario()]

	def getUniqueUnit(self, iPlayer, iUnit):
		pPlayer = gc.getPlayer(iPlayer)
		return gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getUnitInfo(iUnit).getUnitClassType())

	def getBaseUnit(self, iUnit):
		return gc.getUnitClassInfo(gc.getUnitInfo(iUnit).getUnitClassType()).getDefaultUnitIndex()

	def getUniqueBuilding(self, iPlayer, iBuilding):
		return gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(gc.getBuildingInfo(iBuilding).getBuildingClassType())

	def getPlotList(self, tTL, tBR, tExceptions=()):
		return [(x, y) for x in range(tTL[0], tBR[0]+1) for y in range(tTL[1], tBR[1]+1) if 0 <= x < con.iMapMaxX and 0 <= y < con.iMapMaxY and (x, y) not in tExceptions]

	def surroundingPlots(self, tPlot, iRadius=1, filter=lambda (x, y): False):
		x, y = tPlot
		return [(i , j) for i in range(x-iRadius, x+iRadius+1) for j in range(y-iRadius, y+iRadius+1) if 0 <= i < con.iMapMaxX and 0 <= j < con.iMapMaxY and not filter((i, j))]

	def getCityList(self, iCiv):
		if iCiv is None: return []
		return [pCity.GetCy() for pCity in PyPlayer(iCiv).getCityList()]

	def getRandomEntry(self, list):
		if not list: return False
		return list[gc.getGame().getSorenRandNum(len(list), 'Random entry')]

	def isWonder(self, iBuilding):
		return xml.iBeginWonders <= iBuilding <= xml.iEndWonders

	def getWorldPlotsList(self):
		return [(x, y) for x in range(con.iMapMaxX) for y in range(con.iMapMaxY)]

	def getRandomByWeight(self, lList):
		if not lList: return -1
		iTemp = 0
		iRand = gc.getGame().getSorenRandNum(sum(x[1] for x in lList), 'Random entry')
		for (iPlayer, iValue) in lList:
			iTemp += iValue
			if iTemp >= iRand:
				return iPlayer
		return -1
