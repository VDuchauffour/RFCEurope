# Rhye's and Fall of Civilization - AI Wars

from CvPythonExtensions import *
import CvUtil
import PyHelpers		# LOQ
import Popup
import Consts as con
import XMLConsts as xml
import RFCUtils
import RFCEMaps as rfcemaps
from StoredData import sd

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer		# LOQ
utils = RFCUtils.RFCUtils()

### Constants ###

iMinIntervalEarly = 15
iMaxIntervalEarly = 30
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30
iNumPlayers = con.iNumMajorPlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iIndependent3 = con.iIndependent3
iIndependent4 = con.iIndependent4
iNumTotalPlayers = con.iNumTotalPlayers

tWarsMap = rfcemaps.tWarsMaps


class AIWars:

	def getAttackingCivsArray( self, iCiv ):
		return sd.scriptDict['lAttackingCivsArray'][iCiv]

	def setAttackingCivsArray( self, iCiv, iNewValue ):
		sd.scriptDict['lAttackingCivsArray'][iCiv] = iNewValue

	def getNextTurnAIWar( self ):
		return sd.scriptDict['iNextTurnAIWar']

	def setNextTurnAIWar( self, iNewValue ):
		sd.scriptDict['iNextTurnAIWar'] = iNewValue


	def setup(self):
		iTurn = utils.getScenarioStartTurn() #only check from the start turn of the scenario
		self.setNextTurnAIWar(iTurn + gc.getGame().getSorenRandNum(iMaxIntervalEarly-iMinIntervalEarly, 'random turn'))


	def checkTurn(self, iGameTurn):

		# Absinthe: automatically turn peace on between independent cities and all the major civs
		if (iGameTurn % 20 == 4 and iGameTurn > 20):
			utils.restorePeaceHuman(con.iIndependent2)
		if (iGameTurn % 20 == 9 and iGameTurn > 20):
			utils.restorePeaceHuman(con.iIndependent)
		if (iGameTurn % 20 == 14 and iGameTurn > 20):
			utils.restorePeaceHuman(con.iIndependent3)
		if (iGameTurn % 20 == 19 and iGameTurn > 20):
			utils.restorePeaceHuman(con.iIndependent4)
		if (iGameTurn % 36 == 0 and iGameTurn > 30):
			utils.restorePeaceAI(con.iIndependent, False)
		if (iGameTurn % 36 == 9 and iGameTurn > 30):
			utils.restorePeaceAI(con.iIndependent2, False)
		if (iGameTurn % 36 == 18 and iGameTurn > 30):
			utils.restorePeaceAI(con.iIndependent3, False)
		if (iGameTurn % 36 == 27 and iGameTurn > 30):
			utils.restorePeaceAI(con.iIndependent4, False)

		# Absinthe: automatically turn war on between independent cities and some AI major civs
		if (iGameTurn % 36 == 2 and iGameTurn > 30): #1 turn after restorePeace()
			utils.minorWars(con.iIndependent, iGameTurn)
		if (iGameTurn % 36 == 11 and iGameTurn > 30): #1 turn after restorePeace()
			utils.minorWars(con.iIndependent2, iGameTurn)
		if (iGameTurn % 36 == 20 and iGameTurn > 30): #1 turn after restorePeace()
			utils.minorWars(con.iIndependent3, iGameTurn)
		if (iGameTurn % 36 == 29 and iGameTurn > 30): #1 turn after restorePeace()
			utils.minorWars(con.iIndependent4, iGameTurn)

		# Absinthe: declare war sooner / more frequently if there is an Indy city inside the core area
		#			so the AI will declare war much sooner after an indy city appeared in it's core
		if (iGameTurn % 12 == 1 and iGameTurn > 40):
			utils.minorCoreWars(con.iIndependent4, iGameTurn)
		if (iGameTurn % 12 == 4 and iGameTurn > 40):
			utils.minorCoreWars(con.iIndependent3, iGameTurn)
		if (iGameTurn % 12 == 7 and iGameTurn > 40):
			utils.minorCoreWars(con.iIndependent2, iGameTurn)
		if (iGameTurn % 12 == 10 and iGameTurn > 40):
			utils.minorCoreWars(con.iIndependent, iGameTurn)

		# Absinthe: Venice always seeks war with an Independent Ragusa - should help AI Venice significantly
		pVenice = gc.getPlayer( con.iVenecia )
		teamVenice = gc.getTeam( pVenice.getTeam() )
		if ( (pVenice.isAlive()) and (iGameTurn % 9 == 2) and (not pVenice.isHuman()) ):
			pRagusaPlot = gc.getMap().plot( 64, 28 )
			if ( pRagusaPlot.isCity() ):
				pRagusaCity = pRagusaPlot.getPlotCity()
				iRagusa = pRagusaCity.getOwner()
				if ( utils.isIndep( iRagusa ) ):
					# Absinthe: probably better to use declareWar instead of setAtWar
					teamVenice.declareWar(iRagusa, False, WarPlanTypes.WARPLAN_LIMITED)
					print ("minorWars_Ragusa", "WARPLAN_LIMITED")
					#teamVenice.setAtWar( gc.getPlayer( iRagusa ).getTeam(), True )
					#teamRagusa = gc.getTeam( gc.getPlayer( iRagusa ).getTeam() )
					#teamRagusa.setAtWar( pVenice.getTeam(), True )

		if (iGameTurn == self.getNextTurnAIWar()):

			# 3Miro: how long it takes (the else from the statement goes all the way down)
			#if (iGameTurn > xml.i1600AD): #longer periods due to globalization of contacts
			#	iMinInterval = iMinIntervalLate
			#	iMaxInterval = iMaxIntervalLate
			#else:
			iMinInterval = iMinIntervalEarly
			iMaxInterval = iMaxIntervalEarly

			#skip if already in a world war
			#print ("AIWars iTargetCiv missing", iCiv)
			iCiv, iTargetCiv = self.pickCivs()
			if (iTargetCiv >= 0 and iTargetCiv <= iNumTotalPlayers):
				if (iTargetCiv != con.iPope and iCiv != con.iPope and iCiv != iTargetCiv):
					self.initWar(iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval)
					return
			else:
				print ("AIWars iTargetCiv missing again", iCiv)

			#make sure we don't miss this
			print("Skipping AIWar")
			self.setNextTurnAIWar(iGameTurn + iMinInterval + gc.getGame().getSorenRandNum(iMaxInterval-iMinInterval, 'random turn'))


	def pickCivs(self):
		iCiv = -1
		iTargetCiv = -1
		iCiv = self.chooseAttackingPlayer()
		if (iCiv >= 0 and iCiv <= iNumPlayers):
			iTargetCiv = self.checkGrid(iCiv)
			return (iCiv, iTargetCiv)
		else:
			print ("AIWars iCiv missing", iCiv)
			return (-1, -1)


	def initWar(self, iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval):
		# Absinthe: don't declare if couldn't do it otherwise
		teamAgressor = gc.getTeam( gc.getPlayer(iCiv).getTeam() )
		if ( teamAgressor.canDeclareWar( iTargetCiv ) ):
			gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iTargetCiv, True, -1)
			self.setNextTurnAIWar(iGameTurn + iMinInterval + gc.getGame().getSorenRandNum(iMaxInterval-iMinInterval, 'random turn'))
			print("Setting AIWar", iCiv, "attacking", iTargetCiv)
		# Absinthe: if not, next try will come 1/2 time later
		else:
			self.setNextTurnAIWar(iGameTurn + (iMinInterval + gc.getGame().getSorenRandNum(iMaxInterval-iMinInterval, 'random turn') / 2))
			print("No AIWar this time, but the next try will come sooner")


##	def initArray(self):
##		for k in range( iNumPlayers ):
##			grid = []
##			for j in range( con.iMapMaxY ):
##				line = []
##				for i in range( con.iMapMaxX ):
##					line.append( gc.getPlayer(iCiv).getSettlersMaps( con.iMapMaxY-j-1, i ) )
##				grid.append( line )
##			self.lSettlersMap.append( grid )
##		print self.lSettlersMap


	def chooseAttackingPlayer(self):
		#finding max teams ever alive (countCivTeamsEverAlive() doesn't work as late human starting civ gets killed every turn)
		iMaxCivs = iNumPlayers
		for i in range( iNumPlayers ):
			j = iNumPlayers -1 - i
			if (gc.getPlayer(j).isAlive()):
				iMaxCivs = j
				break
		#print ("iMaxCivs", iMaxCivs)

		if (gc.getGame().countCivPlayersAlive() <= 2):
			return -1
		else:
			iRndnum = gc.getGame().getSorenRandNum(iMaxCivs, 'attacking civ index')
			#print ("iRndnum", iRndnum)
			iAlreadyAttacked = -100
			iMin = 100
			iCiv = -1
			for i in range( iRndnum, iRndnum + iMaxCivs ):
				iLoopCiv = i % iMaxCivs
				if (gc.getPlayer(iLoopCiv).isAlive() and not gc.getPlayer(iLoopCiv).isHuman()):
					if (utils.getPlagueCountdown(iLoopCiv) >= -10 and utils.getPlagueCountdown(iLoopCiv) <= 0): #civ is not under plague or quit recently from it
						iAlreadyAttacked = self.getAttackingCivsArray(iLoopCiv)
						if (utils.isAVassal(iLoopCiv)):
							iAlreadyAttacked += 1 #less likely to attack
						#check if a world war is already in place:
						iNumAlreadyWar = 0
						tLoopCiv = gc.getTeam(gc.getPlayer(iLoopCiv).getTeam())
						for kLoopCiv in range( iNumPlayers ):
							if (tLoopCiv.isAtWar(kLoopCiv)):
								iNumAlreadyWar += 1
						if (iNumAlreadyWar >= 4):
							iAlreadyAttacked += 2 #much less likely to attack
						elif (iNumAlreadyWar >= 2):
							iAlreadyAttacked += 1 #less likely to attack

						if (iAlreadyAttacked < iMin):
							iMin = iAlreadyAttacked
							iCiv = iLoopCiv
			#print ("attacking civ", iCiv)
			if (iAlreadyAttacked != -100):
				self.setAttackingCivsArray(iCiv, iAlreadyAttacked + 1)
				return iCiv
			else:
				return -1
		return -1


	def checkGrid(self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		tCiv = gc.getTeam(pCiv.getTeam())
		lTargetCivs = []
		#lTargetCivs = con.l0ArrayTotal

		#clean it, sometimes it takes old values in memory
		for k in range( iNumTotalPlayers ):
			lTargetCivs.append(0)
			#lTargetCivs[k] = 0

		##set alive civs to 1 to differentiate them from dead civs
		for k in range( iNumPlayers ):
			if (gc.getPlayer(k).isAlive() and tCiv.isHasMet(k)): #canContact here?
				if (lTargetCivs[k] == 0):
					lTargetCivs[k] = 1
		for k in range( iNumTotalPlayers ):
			if (k >= iNumPlayers):
				if (gc.getPlayer(k).isAlive() and tCiv.isHasMet(k)):
					lTargetCivs[k] = 1

		##set master or vassal to 0
		for k in range( iNumPlayers ):
			if (gc.getTeam(gc.getPlayer(k).getTeam()).isVassal(iCiv) or tCiv.isVassal(k)):
				 lTargetCivs[k] = 0

		#if already at war
		for k in range( iNumTotalPlayers ):
			if (tCiv.isAtWar(k)):
				lTargetCivs[k] = 0

		lTargetCivs[iCiv] = 0

		for j in range( con.iMapMaxY ):
			for i in range( con.iMapMaxX ):
				iOwner = gc.getMap().plot( i, j ).getOwner()
				if (iOwner >= 0 and iOwner < iNumTotalPlayers and iOwner != iCiv):
					if (lTargetCivs[iOwner] > 0):
						lTargetCivs[iOwner] += tWarsMap[iCiv][con.iMapMaxY-1-j][i]

		#there are other routines for this
		lTargetCivs[iIndependent] /= 3
		lTargetCivs[iIndependent2] /= 3
		lTargetCivs[iIndependent3] /= 3
		lTargetCivs[iIndependent4] /= 3

		#can they attack civs with lost contact?
		for k in range( iNumPlayers ):
			if (not pCiv.canContact(k)):
				lTargetCivs[k] /= 8

		#print(lTargetCivs)

		#normalization
		iMaxTempValue = -1
		for k in range( iNumTotalPlayers ):
			if (lTargetCivs[k] > iMaxTempValue):
				iMaxTempValue = lTargetCivs[k]
		#print(iMaxTempValue)
		if (iMaxTempValue > 0):
			for k in range( iNumTotalPlayers ):
				if (lTargetCivs[k] > 0):
					#lTargetCivs[k] *= 500 #non va!
					#lTargetCivs[k] / iMaxTempValue
					lTargetCivs[k] = lTargetCivs[k]*500/iMaxTempValue

		#print(lTargetCivs)

		for iLoopCiv in range( iNumTotalPlayers ):

			if (lTargetCivs[iLoopCiv] <= 0):
				continue

			#add a random value
			if (lTargetCivs[iLoopCiv] <= iThreshold):
				lTargetCivs[iLoopCiv] += gc.getGame().getSorenRandNum(100, 'random modifier')
			if (lTargetCivs[iLoopCiv] > iThreshold):
				lTargetCivs[iLoopCiv] += gc.getGame().getSorenRandNum(300, 'random modifier')
			#balanced with attitude
			attitude = 2*(pCiv.AI_getAttitude(iLoopCiv) - 2)
			if (attitude > 0):
				lTargetCivs[iLoopCiv] /= attitude
			#exploit plague
			if (utils.getPlagueCountdown(iLoopCiv) > 0 or utils.getPlagueCountdown(iLoopCiv) < -10 and not (gc.getGame().getGameTurn() <= con.tBirth[iLoopCiv] + 20)):
				lTargetCivs[iLoopCiv] *= 3
				lTargetCivs[iLoopCiv] /= 2

			#balanced with master's attitude
			for j in range( iNumTotalPlayers ):
				if (tCiv.isVassal(j)):
					attitude = 2*(gc.getPlayer(j).AI_getAttitude(iLoopCiv) - 2)
					if (attitude > 0):
						lTargetCivs[iLoopCiv] /= attitude

			#if already at war
			if (not tCiv.isAtWar(iLoopCiv)):
				#consider peace counter
				iCounter = min(7,max(1,tCiv.AI_getAtPeaceCounter(iLoopCiv)))
				if (iCounter <= 7):
					lTargetCivs[iLoopCiv] *= 20 + 10*iCounter
					lTargetCivs[iLoopCiv] /= 100

			#if under pact
			if (tCiv.isDefensivePact(iLoopCiv)):
				lTargetCivs[iLoopCiv] /= 4
			#if friend of a friend
##			for jLoopCiv in range( iNumTotalPlayers ):
##				if (tCiv.isDefensivePact(jLoopCiv) and gc.getTeam(gc.getPlayer(iLoopCiv).getTeam()).isDefensivePact(jLoopCiv)):
##					lTargetCivs[iLoopCiv] /= 2

		#print(lTargetCivs)

		#find max
		iMaxValue = 0
		iTargetCiv = -1
		for iLoopCiv in range( iNumTotalPlayers ):
			if (lTargetCivs[iLoopCiv] > iMaxValue):
				iMaxValue = lTargetCivs[iLoopCiv]
				iTargetCiv = iLoopCiv

		#print ("maxvalue", iMaxValue)
		#print("target civ", iTargetCiv)

		if (iMaxValue >= iMinValue):
			return iTargetCiv
		return -1


	def forgetMemory(self, iTech, iPlayer):
		pass

