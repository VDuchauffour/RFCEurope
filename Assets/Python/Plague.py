# Rhye's and Fall of Civilization: Europe - Plague

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import Consts as con
import XMLConsts as xml
import RFCUtils
utils = RFCUtils.RFCUtils()
from StoredData import sd

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNumTotalPlayers = con.iNumTotalPlayers
iBarbarian = con.iBarbarian
iNumTotalPlayersB = con.iNumTotalPlayersB

iPlague = xml.iPlague

# Absinthe: Black Death is more severe, while the Plague of Justinian is less severe than the others plagues
iBaseHumanDuration = 10
iBaseAIDuration = 6
iImmunity = con.iImmunity
iNumPlagues = 5
iConstantinople = 0
iBlackDeath = 1


class Plague:


##################################################
### Secure storage & retrieval of script data ###
################################################


	def getPlagueCountdown( self, iCiv ):
		return sd.scriptDict['lPlagueCountdown'][iCiv]


	def setPlagueCountdown( self, iCiv, iNewValue ):
		sd.scriptDict['lPlagueCountdown'][iCiv] = iNewValue


	def getGenericPlagueDates( self, i ):
		return sd.scriptDict['lGenericPlagueDates'][i]


	def setGenericPlagueDates( self, i, iNewValue ):
		sd.scriptDict['lGenericPlagueDates'][i] = iNewValue


	def getBadPlague( self ):
		return sd.scriptDict['bBadPlague']


	def setBadPlague( self, bBad ):
		sd.scriptDict['bBadPlague'] = bBad


	def getFirstPlague( self ):
		return sd.scriptDict['bFirstPlague']


	def setFirstPlague( self, bFirst ):
		sd.scriptDict['bFirstPlague'] = bFirst


#######################################
### Main methods (Event-Triggered) ###
#####################################


	def setup(self):

		for i in range(iNumMajorPlayers):
			self.setPlagueCountdown(i, -iImmunity)

		#Sedna17: Set number of GenericPlagues in StoredData
		#3Miro: Plague 0 strikes France too hard, make it less random and force it to pick Byzantium as starting land
		self.setGenericPlagueDates(0, 28 + gc.getGame().getSorenRandNum(5, 'Variation') - 10) #Plagues of Constantinople
		self.setGenericPlagueDates(1, 247 + gc.getGame().getSorenRandNum(40, 'Variation') - 20) #1341 Black Death
		self.setGenericPlagueDates(2, 300 + gc.getGame().getSorenRandNum(40, 'Variation') - 20) #Generic recurrence of plague
		self.setGenericPlagueDates(3, 375 + gc.getGame().getSorenRandNum(40, 'Variation') - 30) #1650 Great Plague
		self.setGenericPlagueDates(4, 440 + gc.getGame().getSorenRandNum(40, 'Variation') - 30) #1740 Small Pox
		for i in range(iNumPlagues):
			print ( "plagues", self.getGenericPlagueDates( i ) )


	def checkTurn(self, iGameTurn):

		for i in range(iNumTotalPlayersB):
			if (gc.getPlayer(i).isAlive()):
				if (self.getPlagueCountdown(i) > 0):
					self.setPlagueCountdown(i, self.getPlagueCountdown(i)-1)
					iPlagueCountDown = self.getPlagueCountdown(i)
					if (iPlagueCountDown == 2):
						self.preStopPlague(i, iPlagueCountDown)
					elif (iPlagueCountDown == 1):
						self.preStopPlague(i, iPlagueCountDown)
					elif (iPlagueCountDown == 0):
						self.stopPlague(i)
				elif (self.getPlagueCountdown(i) < 0):
					self.setPlagueCountdown(i, self.getPlagueCountdown(i)+1)

		for i in range(iNumPlagues):
			if ( iGameTurn == self.getGenericPlagueDates( i ) ):
				self.startPlague(i)

			# if the plague has stopped too quickly, restart
			if (iGameTurn == self.getGenericPlagueDates(i) + 4):
				# not on the first one, that's mostly for one civ anyway
				bFirstPlague = self.getFirstPlague()
				if not bFirstPlague:
					iInfectedCounter = 0
					for j in range(iNumTotalPlayersB):
						if ( gc.getPlayer(j).isAlive() and self.getPlagueCountdown(j) > 0):
							iInfectedCounter += 1
					if ( iInfectedCounter <= 1 ):
						self.startPlague(i)


	def checkPlayerTurn(self, iGameTurn, iPlayer):
		if (iPlayer < iNumTotalPlayersB):
			if (self.getPlagueCountdown(iPlayer) > 0):
				self.processPlague(iPlayer)


	def startPlague( self, iPlagueCount ):
		iWorstCiv = -1
		iWorstHealth = 100
		for i in range(iNumMajorPlayers):
			pPlayer = gc.getPlayer(i)
			if (pPlayer.isAlive()):
				if (self.isVulnerable(i) ):
					iHealth = self.calcHealth( i ) - gc.getGame().getSorenRandNum(10, 'random modifier')
					if ( iHealth < iWorstHealth ):
						iWorstCiv = i
						iWorstHealth = iHealth

		# Absinthe: specific plagues:
		# Plague of Constantinople (that started at Alexandria)
		if (iPlagueCount == iConstantinople):
			iWorstCiv = con.iByzantium
			self.setFirstPlague(True)
			self.setBadPlague(False)
		# Black Death in the 14th century
		elif (iPlagueCount == iBlackDeath):
			self.setFirstPlague(False)
			self.setBadPlague(True)
		# All the others
		else:
			self.setFirstPlague(False)
			self.setBadPlague(False)

		if ( iWorstCiv == -1 ):
			iWorstCiv = utils.getRandomCiv()

		pWorstCiv = gc.getPlayer(iWorstCiv)
		city = utils.getRandomCity(iWorstCiv)
		if (city != -1):
			self.spreadPlague(iWorstCiv, city)
			self.infectCity(city)


	def calcHealth( self, iPlayer ):
		pPlayer = gc.getPlayer(iPlayer)
		iTCH = pPlayer.calculateTotalCityHealthiness()
		iTCU = pPlayer.calculateTotalCityUnhealthiness()
		# Absinthe: use average city health instead
		iNumCities = pPlayer.getNumCities()
		iAverageCityHealth = int((10 * (iTCH - iTCU)) / iNumCities) # 10x the average health actually
		print ("iAverageCityHealth", iAverageCityHealth)
		return iAverageCityHealth
		#if ( iTCH > 0 ):
		#	return int((10.0 * iTCH) / (iTCH + iTCU)) - 5 # theoretically between 5 and -5, but almost always between -2 and +2
		#else:
		#	return -4


	def isVulnerable(self, iPlayer):
		# determine if vulnerable based on recent infections and the average city healthiness (also tech immunity should go here, if ever get added to the mod)
		if (iPlayer >= iNumMajorPlayers):
			if (self.getPlagueCountdown(iPlayer) == 0):
				return True
		else:
			pPlayer = gc.getPlayer(iPlayer)
			if (self.getPlagueCountdown(iPlayer) == 0):
				iHealth = self.calcHealth( iPlayer )
				if (iHealth < 42): # won't spread at all if the average surplus health in the cities is at least 4.2
					return True
		return False


	def spreadPlague( self, iPlayer, city ):
		# Absinthe: the Plague of Justinian shouldn't spread to Italy and France, even if it was as deadly as the Black Death
		if (iPlayer == con.iFrankia and gc.getGame().getGameTurn() <= xml.i632AD): return
		if (iPlayer == con.iPope and gc.getGame().getGameTurn() <= xml.i632AD): return

		# Absinthe: message about the spread
		iHuman = utils.getHumanID()
		if (gc.getPlayer(iHuman).canContact(iPlayer) and iHuman != iPlayer):
			if (city != -1 and city.isRevealed(iHuman, False)):
				CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + " (" + gc.getPlayer(city.getOwner()).getCivilizationAdjective(0) + ")!", "AS2D_PLAGUE", 0, gc.getBuildingInfo(iPlague).getButton(), ColorTypes(con.iLime), city.getX(), city.getY(), True, True)
			elif (city != -1):
				pCiv = gc.getPlayer(city.getOwner())
				print ("pCiv.getCivilizationDescriptionKey()", pCiv.getCivilizationDescriptionKey())
				print ("pCiv.getCivilizationDescription(0)", pCiv.getCivilizationDescription(0))
				CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CIV", ()) + " " + pCiv.getCivilizationDescription(0) + "!", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)

		# Absinthe: this is where the duration is handled for each civ
		#			number of cities should be a significant factor, so plague isn't way more deadly for smaller civs
		iHealth = self.calcHealth( iPlayer )
		iHealthDuration = max ( min ( (iHealth / 14), 3 ), -4 ) # between -4 and +3
		apCityList = PyPlayer(iPlayer).getCityList()
		iCityDuration = min ( (len(apCityList) + 2) / 3, 10 ) # between 1 and 10 from cities
		print ("plague duration iCities", iCityDuration)
		if iPlayer == iHuman:
			# Overall duration for the plague is between 4 and 12 (usually between 6-8)
			iValue = ( iBaseHumanDuration + iCityDuration - iHealthDuration ) / 2
		else:
			# Overall duration for the plague is between 2 and 10 (usually around 5-6)
			iValue = max ((( iBaseAIDuration + iCityDuration - iHealthDuration ) / 2), 4) # at least 4
		print ("plague duration overall, iPlayer, iValue", iPlayer, iValue)
		self.setPlagueCountdown(iPlayer, iValue)


	def infectCity( self, city ):
		# Absinthe: the Plague of Justinian shouldn't spread to Italy and France, even if it was as deadly as the Black Death
		if (city.getOwner() == con.iFrankia and gc.getGame().getGameTurn() <= xml.i632AD): return
		if (city.getOwner() == con.iPope and gc.getGame().getGameTurn() <= xml.i632AD): return
		city.setHasRealBuilding(iPlague, True)
		if (gc.getPlayer(city.getOwner()).isHuman()):
			CyInterface().addMessage(city.getOwner(), True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + "!", "AS2D_PLAGUE", 0, gc.getBuildingInfo(iPlague).getButton(), ColorTypes(con.iLime), city.getX(), city.getY(), True, True)
		for x in range(city.getX()-2, city.getX()+3):	# from x-2 to x+2, range in python works this way
			for y in range(city.getY()-2, city.getY()+3):	# from y-2 to y+2, range in python works this way
				if ( x>=0 and x<con.iMapMaxX and y>=0 and y<con.iMapMaxY ):
					pCurrent = gc.getMap().plot( x, y )
					iImprovement = pCurrent.getImprovementType()
					# Absinthe: chance for reducing the improvement vs. only resetting the process towards the next level to 0
					if (iImprovement == xml.iImprovementTown): # 100% chance to reduce towns
						pCurrent.setImprovementType(xml.iImprovementVillage)
					if (iImprovement == xml.iImprovementVillage):
						iRand = gc.getGame().getSorenRandNum(100, 'roll')
						if (iRand < 75): # 75% for reducing, 25% for resetting
							pCurrent.setImprovementType(xml.iImprovementHamlet)
						else:
							pCurrent.setUpgradeProgress(0)
					if (iImprovement == xml.iImprovementHamlet):
						iRand = gc.getGame().getSorenRandNum(100, 'roll')
						if (iRand < 50): # 50% for reducing, 50% for resetting
							pCurrent.setImprovementType(xml.iImprovementCottage)
						else:
							pCurrent.setUpgradeProgress(0)
					if (iImprovement == xml.iImprovementCottage):
						iRand = gc.getGame().getSorenRandNum(100, 'roll')
						if (iRand < 25): # 25% for reducing, 75% for resetting
							pCurrent.setImprovementType(-1)
						else:
							pCurrent.setUpgradeProgress(0)

		# Absinthe: one population is killed by default
		if (city.getPopulation() > 1):
			city.changePopulation(-1)

		# Absinthe: plagues won't kill units instantly on spread anymore
		#			Plague of Justinian deals even less initial damage
		bFirstPlague = self.getFirstPlague()
		if bFirstPlague:
			self.killUnitsByPlague(city, gc.getMap().plot( city.getX(), city.getY() ) , 0, 80, 0)
		else:
			self.killUnitsByPlague(city, gc.getMap().plot( city.getX(), city.getY() ) , 0, 90, 0)


	def killUnitsByPlague( self, city, plot, iThreshold, iDamage, iPreserveDefenders ):
		iCityOwner = city.getOwner()
		pCityOwner = gc.getPlayer(iCityOwner)
		teamCityOwner = gc.getTeam( pCityOwner.getTeam() )

		iNumUnitsInAPlot = plot.getNumUnits()
		iHuman = utils.getHumanID()
		iCityHealthRate = city.healthRate(False, 0)

		if (iNumUnitsInAPlot):
			# Absinthe: if we mix up the order of the units, health will be much less static for the chosen defender units
			bOrderChange = False
			if (gc.getGame().getSorenRandNum(4, 'roll') == 1):
				bOrderChange = True
			for j in range(iNumUnitsInAPlot):
				if bOrderChange:
					i = j # we are counting from the strongest unit
				else:
					i = iNumUnitsInAPlot - j - 1 # count back from the weakest unit
				unit = plot.getUnit(i)
				if ( utils.isMortalUnit( unit ) and gc.getGame().getSorenRandNum(100, 'roll') > iThreshold + 5*iCityHealthRate ):
					iUnitDamage = unit.getDamage()
					# if some defenders are set to be preserved for some reason, they won't get more damage if they are already under 50%
					if ( unit.getOwner() == iCityOwner and iPreserveDefenders > 0 and unit.getDomainType() != 0 and unit.baseCombatStr() > 0): # only units which can really defend
						iPreserveDefenders -= 1
						unit.setDamage( max( iUnitDamage, min( 50, iUnitDamage + iDamage - unit.getExperience()/10 - 3*unit.baseCombatStr() / 7 ) ), iBarbarian )
					else:
						if (unit.baseCombatStr() > 0):
							if (unit.getDomainType() == 0): # naval units get less damage, won't be killed unless they were very badly damaged originally
								iShipDamage = iDamage * 93 / 100
								iUnitDamage = max( iUnitDamage, unit.getDamage() + iShipDamage - unit.getExperience()/10 - 3*unit.baseCombatStr() / 7 )
							else:
								iUnitDamage = max( iUnitDamage, unit.getDamage() + iDamage - unit.getExperience()/10 - 3*unit.baseCombatStr() / 7 )
						else: # less damage for civilian units - workers, settlers, missionaries, etc.
							iCivilDamage = iDamage * 96 / 100 # workers will be killed with any value here if they are automated (thus moving instead of healing)
							iUnitDamage = max( iUnitDamage, unit.getDamage() + iCivilDamage)
						# kill the unit if necessary
						if ( iUnitDamage >= 100 ):
							unit.kill( False, iBarbarian )
							if ( unit.getOwner() == iHuman ):
								CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_PROCESS_UNIT", (unit.getName(), )) + " " + city.getName() + "!", "AS2D_PLAGUE", 0, gc.getBuildingInfo(iPlague).getButton(), ColorTypes(con.iLime), plot.getX(), plot.getY(), True, True)
						else:
							unit.setDamage( iUnitDamage, iBarbarian )
						# if we have many units in the same plot, decrease the damage for every other unit
						iDamage *= 7
						iDamage /= 8


	def processPlague( self, iPlayer ):
		bBadPlague = self.getBadPlague()
		bFirstPlague = self.getFirstPlague()
		pPlayer = gc.getPlayer(iPlayer)
		iHuman = utils.getHumanID()
		# first spread to close locations
		cityList = [] # make a list of city objects, apCityList is a list generated by a Python utility
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			cityList.append(city)
			if (city.hasBuilding(iPlague)):
				# kill citizens
				if (city.getPopulation() > 1):
					iRandom = gc.getGame().getSorenRandNum(100, 'roll')
					iPopSize = city.getPopulation()
					# the plague itself also greatly contributes to unhealth, so the health rate will almost always be negative
					iHealthRate = city.goodHealth() - city.badHealth(False)
					# always between -5 and +5
					if (iHealthRate < -5):
						iHealthRate = -5
					elif (iHealthRate > 5):
						iHealthRate = 5
						min ( 5, max (5, iHealthRate))
					# if it's the Black Death, bigger chance for population loss
					if bBadPlague:
						if (iRandom < 10 + 10*(iPopSize-4) - 5*iHealthRate):
							city.changePopulation(-1)
							if ( city.getOwner() == iHuman ):
								CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_PROCESS_CITY", (city.getName(), )) + " " + city.getName() + "!", "AS2D_PLAGUE", 0, gc.getBuildingInfo(iPlague).getButton(), ColorTypes(con.iLime), city.getX(), city.getY(), True, True)
					# if it's the Plague of Justinian, smaller chance for population loss
					elif bFirstPlague:
						if (iRandom < 10*(iPopSize-4) - 5*iHealthRate):
							city.changePopulation(-1)
							if ( city.getOwner() == iHuman ):
								CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_PROCESS_CITY", (city.getName(), )) + " " + city.getName() + "!", "AS2D_PLAGUE", 0, gc.getBuildingInfo(iPlague).getButton(), ColorTypes(con.iLime), city.getX(), city.getY(), True, True)
					# in "normal" plagues the range for a given pop size is from 10*(size-6) to 10*(size-1)
					# so with size 2: from -40 to 10, size 5: -10 to 40, size 8: 20 to 70, size 12: 60 to 110, size 15: 90 to 140
					elif (iRandom < 5 + 10*(iPopSize-4) - 5*iHealthRate):
						city.changePopulation(-1)
						if ( city.getOwner() == iHuman ):
							CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_PROCESS_CITY", (city.getName(), )) + " " + city.getName() + "!", "AS2D_PLAGUE", 0, gc.getBuildingInfo(iPlague).getButton(), ColorTypes(con.iLime), city.getX(), city.getY(), True, True)

				# infect vassals
				if (city.isCapital()):
					for iLoopCiv in range(iNumMajorPlayers):
						if (gc.getTeam(pPlayer.getTeam()).isVassal(iLoopCiv) or gc.getTeam(gc.getPlayer(iLoopCiv).getTeam()).isVassal(iPlayer)):
							if (gc.getPlayer(iLoopCiv).getNumCities() > 0): # this check is needed, otherwise game crashes
								capital = gc.getPlayer(iLoopCiv).getCapitalCity()
								if ( self.isVulnerable(iLoopCiv) ):
									if (self.getPlagueCountdown(iPlayer) > 2):
										self.spreadPlague(iLoopCiv, capital)
										self.infectCity(capital)

				# kill units and spread plague in 2 distance around the city
				for x in range(city.getX()-2, city.getX()+3):
					for y in range(city.getY()-2, city.getY()+3):
						if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
							pCurrent = gc.getMap().plot( x, y )
							# spread to neighbours
							if (pCurrent.getOwner() != iPlayer and pCurrent.getOwner() >= 0):
								if (self.getPlagueCountdown(iPlayer) > 2): # don't spread in the last turns
									if (self.isVulnerable(pCurrent.getOwner())):
										self.spreadPlague(pCurrent.getOwner(), -1)
										self.infectCitiesNear(pCurrent.getOwner(), x, y)
							else:
								# if it is a city
								if (pCurrent.isCity() and not (x == city.getX() and y == city.getY())):
									cityNear = pCurrent.getPlotCity()
									if (not cityNear.hasBuilding(iPlague)):
										if (self.getPlagueCountdown(iPlayer) > 2): # don't spread in the last turns
											self.infectCity(cityNear)
								else:
									if (x == city.getX() and y == city.getY()):
										self.killUnitsByPlague(city, pCurrent, 20, 40, 2)
									# if just a plot, kill units
									else:
										if (pCurrent.isRoute()):
											self.killUnitsByPlague(city, pCurrent, 20, 30, 0)
										elif (pCurrent.isWater()):
											self.killUnitsByPlague(city, pCurrent, 30, 30, 0)
										else:
											self.killUnitsByPlague(city, pCurrent, 30, 30, 0)

				# kill units further from the city
				for x in range(city.getX()-3, city.getX()+4):
					y = city.getY() - 3
					if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
						pCurrent = gc.getMap().plot( x, y )
						if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
							if (not pCurrent.isCity()):
								if (pCurrent.isRoute() or pCurrent.isWater()):
									self.killUnitsByPlague(city, pCurrent, 30, 30, 0)
					y = city.getY() +3
					if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
						pCurrent = gc.getMap().plot( x, y )
						if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
							if (not pCurrent.isCity()):
								if (pCurrent.isRoute() or pCurrent.isWater()):
									self.killUnitsByPlague(city, pCurrent, 30, 30, 0)
				for y in range(city.getY()-2, city.getY()+3):
					x = city.getX() - 3
					if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
						pCurrent = gc.getMap().plot( x, y )
						if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
							if (not pCurrent.isCity()):
								if (pCurrent.isRoute() or pCurrent.isWater()):
									self.killUnitsByPlague(city, pCurrent, 30, 30, 0)
					x = city.getX() +3
					if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
						pCurrent = gc.getMap().plot( x, y )
						if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
							if (not pCurrent.isCity()):
								if (pCurrent.isRoute() or pCurrent.isWater()):
									self.killUnitsByPlague(city, pCurrent, 30, 30, 0)

				# spread by the trade routes
				if (self.getPlagueCountdown(iPlayer) > 2):
					for i in range(city.getTradeRoutes()):
						loopCity = city.getTradeCity(i)
						if (not loopCity.isNone()):
							if (not loopCity.hasBuilding(iPlague)):
								iOwner = loopCity.getOwner()
								if ( iOwner == iPlayer ):
									self.infectCity(loopCity)
								elif ( gc.getTeam(pPlayer.getTeam()).isOpenBorders(iOwner) or gc.getTeam(pPlayer.getTeam()).isVassal(iOwner) or gc.getTeam(gc.getPlayer(iOwner).getTeam()).isVassal(iPlayer) ):
									if (self.isVulnerable(iOwner) ):
										self.spreadPlague(iOwner, loopCity)
										self.infectCity(loopCity)

		# Absinthe: spread to a couple cities which are not too far from already infected ones
		#			cities are chosen randomly from the possible targets
		#			the maximum number of infections is based on the size of the empire
		iInfectedCites = 0
		iMaxNumInfections = 1
		if (len(apCityList) > 21):
			iMaxNumInfections = 4
		elif (len(apCityList) > 14):
			iMaxNumInfections = 3
		elif (len(apCityList) > 7):
			iMaxNumInfections = 2
		iNumSpreads = gc.getGame().getSorenRandNum(iMaxNumInfections, 'max number of new infections')
		if ( len(apCityList) > 0 ):
			if (self.getPlagueCountdown(iPlayer) > 2): # don't spread in the last turns, when preStopPlague is active
				for x in range(0, len(apCityList)):
					pCity1 = apCityList[gc.getGame().getSorenRandNum(len(apCityList), 'random city')]
					city1 = pCity1.GetCy()
					if (city1.hasBuilding(iPlague)):
						for y in range(0, len(apCityList)):
							pCity2 = apCityList[gc.getGame().getSorenRandNum(len(apCityList), 'random city')]
							city2 = pCity2.GetCy()
							if (not city2.hasBuilding(iPlague)):
								if (city1.isConnectedTo(city2)):
									if (utils.calculateDistance(city1.getX(), city1.getY(), city2.getX(), city2.getY()) <= 10):
										self.infectCity(city2)
										iInfectedCites += 1
										if (iInfectedCites > iNumSpreads): # number of new cities
											return # stop after infecting a couple new cities, don't infect all at the same time


	def infectCitiesNear(self, iPlayer, startingX, startingY):
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			if (utils.calculateDistance(city.getX(), city.getY(), startingX, startingY) <= 3):
				if (not city.hasBuilding(iPlague)):
					self.infectCity(city)


	def preStopPlague(self, iPlayer, iPlagueCountDown):
		cityList = []
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			if (city.hasBuilding(iPlague)):
				cityList.append(city)

		if (len(cityList)):
			iRemoveModifier = 0
			iTimeModifier = iPlagueCountDown * 15
			iPopModifier = 0
			iHealthModifier = 0
			# small cities should have a good chance to be chosen
			for city in cityList:
				# iPopModifier: -28, -21, -14, -7, 0, 7, 14, 21, 28, 35, etc.
				iPopModifier = 7 * city.getPopulation() - 35
				iHealthModifier = 5 * city.healthRate(False, 0)
				if (gc.getGame().getSorenRandNum(100, 'roll') < (100 - iTimeModifier - iPopModifier + iHealthModifier - iRemoveModifier)):
					city.setHasRealBuilding(iPlague, False)
					iRemoveModifier += 5 # less chance for each city which already quit


	def stopPlague(self, iPlayer):
		self.setPlagueCountdown(iPlayer, -iImmunity)
		apCityList = PyPlayer(iPlayer).getCityList()

		for pCity in apCityList:
			pCity.GetCy().setHasRealBuilding(iPlague, False)


	def onCityAcquired(self, iOldOwner, iNewOwner, city):
		if (city.hasBuilding(iPlague)):
			# reinfect the human player if conquering plagued cities
			if iNewOwner == utils.getHumanID():
				# only if it's not a recently born civ
				if (gc.getGame().getGameTurn() > con.tBirth[iNewOwner] + iImmunity):
					# if > 0 do nothing, if < 0 skip immunity and restart the plague, if == 0 start the plague
					if (self.getPlagueCountdown(iNewOwner) <= 0):
						self.spreadPlague(iNewOwner, -1)
						apCityList = PyPlayer(iNewOwner).getCityList()
						for pCity in apCityList:
							cityNear = pCity.GetCy()
							if (utils.calculateDistance(city.getX(), city.getY(), cityNear.getX(), cityNear.getY()) <= 3):
								self.infectCity(cityNear)
				else:
					city.setHasRealBuilding(iPlague, False)
			# no reinfect for the AI, only infect
			else:
				# only if it's not a recently born civ
				if (gc.getGame().getGameTurn() > con.tBirth[iNewOwner] + iImmunity):
					# if > 0 do nothing, if < 0 keep immunity and remove plague from the city, if == 0 start the plague
					if (self.getPlagueCountdown(iNewOwner) == 0):
						self.spreadPlague(iNewOwner, -1)
						apCityList = PyPlayer(iNewOwner).getCityList()
						for pCity in apCityList:
							cityNear = pCity.GetCy()
							if (utils.calculateDistance(city.getX(), city.getY(), cityNear.getX(), cityNear.getY()) <= 3):
								self.infectCity(cityNear)
					elif (self.getPlagueCountdown(iNewOwner) < 0):
						city.setHasRealBuilding(iPlague, False)
				else:
					city.setHasRealBuilding(iPlague, False)


	def onCityRazed(self, city, iNewOwner):
		pass

