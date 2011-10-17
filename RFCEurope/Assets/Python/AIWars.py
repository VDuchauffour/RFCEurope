# Rhye's and Fall of Civilization - AI Wars

from CvPythonExtensions import *
import CvUtil
import PyHelpers        # LOQ
import Popup
import cPickle as pickle        	# LOQ 2005-10-12
import Consts as con
import XMLConsts as xml
import RFCUtils
import RFCEMaps as rfcemaps

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()

### Constants ###


iStartTurn = xml.i500AD
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


# for AI Hack
pVenice = gc.getPlayer( con.iVenecia )
teamVenice = gc.getTeam( pVenice.getTeam() )
      
  
class AIWars:

        def getAttackingCivsArray( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lAttackingCivsArray'][iCiv]

        def setAttackingCivsArray( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lAttackingCivsArray'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )                
                
        def getNextTurnAIWar( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iNextTurnAIWar']

        def setNextTurnAIWar( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iNextTurnAIWar'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def setup(self):
                iTurn = iStartTurn
                #if (not gc.getPlayer(0).isPlayable()):  #late start condition
                #        iTurn = con.i900AD
                self.setNextTurnAIWar(iTurn + gc.getGame().getSorenRandNum(iMaxIntervalEarly-iMinIntervalEarly, 'random turn'))



        def checkTurn(self, iGameTurn):

                #turn automatically peace on between independent cities and all the major civs
                if (iGameTurn % 20 == 0):
                	utils.restorePeaceHuman(con.iIndependent2, False)
                if (iGameTurn % 20 == 5):
                	utils.restorePeaceHuman(con.iIndependent, False)
		if (iGameTurn % 20 == 10):
                	utils.restorePeaceHuman(con.iIndependent3, False)
		if (iGameTurn % 20 == 15):
                	utils.restorePeaceHuman(con.iIndependent4, False)
                if (iGameTurn % 60 == 0 and iGameTurn > 50):
                        utils.restorePeaceAI(con.iIndependent, False)
                if (iGameTurn % 60 == 15 and iGameTurn > 50):
                        utils.restorePeaceAI(con.iIndependent2, False)
		if (iGameTurn % 60 == 30 and iGameTurn > 50):
                        utils.restorePeaceAI(con.iIndependent3, False)
		if (iGameTurn % 60 == 45 and iGameTurn > 50):
                        utils.restorePeaceAI(con.iIndependent4, False)
                #turn automatically war on between independent cities and some AI major civs
                if (iGameTurn % 60 == 2 and iGameTurn > 50): #1 turn after restorePeace()
                        utils.minorWars(con.iIndependent)
                if (iGameTurn % 60 == 17 and iGameTurn > 50): #1 turn after restorePeace()
                        utils.minorWars(con.iIndependent2)
		if (iGameTurn % 60 == 32 and iGameTurn > 50): #1 turn after restorePeace()
                        utils.minorWars(con.iIndependent3)
		if (iGameTurn % 60 == 47 and iGameTurn > 50): #1 turn after restorePeace()
                        utils.minorWars(con.iIndependent4)


                ### 3Miro: AI Hacking - Venice has hard time dealing with Indy Ragusa
                if ( (iGameTurn % 7 == 3) and (not pVenice.isHuman()) ):
                        pRagusa = gc.getMap().plot( 64, 28 )
                        if ( pRagusa.isCity() ):
                                pRagusa = pRagusa.getPlotCity()
                                if ( utils.isIndep( pRagusa.getOwner() ) ):
                                        #pTeamRagusa = gc.getTeam( gc.getPlayer( pRagusa.getOwner() ).getTeam() ).setAtWar
                                        teamVenice.setAtWar( gc.getPlayer( pRagusa.getOwner() ).getTeam(), True )
                ### 3Miro: End of AI Hacking

                     
                if (iGameTurn == self.getNextTurnAIWar()):
                    
                    	# 3Miro: how long it takes (the else from the statement goes all the way down
                        #if (iGameTurn > con.i1600AD): #longer periods due to globalization of contacts
                        #        iMinInterval = iMinIntervalLate
                        #        iMaxInterval = iMaxIntervalLate
                        #else:
                        iMinInterval = iMinIntervalEarly
                        iMaxInterval = iMaxIntervalEarly

                        #skip if in a world war already
                        #print ("AIWars iTargetCiv missing", iCiv)
                        iCiv, iTargetCiv = self.pickCivs()
                        if (iTargetCiv >= 0 and iTargetCiv <= iNumTotalPlayers):
				if (iTargetCiv != con.iPope and iCiv != con.iPope ):
					self.initWar(iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval)
					return
                        else:
                                print ("AIWars iTargetCiv missing again", iCiv)

                        #make sure we don't miss this
                        print("Skipping AIWar")
                        self.setNextTurnAIWar(iGameTurn + iMinInterval + gc.getGame().getSorenRandNum(iMaxInterval-iMinInterval, 'random turn'))
                
                #print(" 3MiroDebug: end AI wars ")


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
                gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iTargetCiv, True, -1) ##False?
                self.setNextTurnAIWar(iGameTurn + iMinInterval + gc.getGame().getSorenRandNum(iMaxInterval-iMinInterval, 'random turn'))
                print("Setting AIWar", iCiv, "attacking", iTargetCiv)

##        def initArray(self):
##                for k in range( iNumPlayers ):
##                        grid = []                
##                        for j in range( con.iMapMaxY ):
##                                line = []
##                                for i in range( con.iMapMaxX ):        
##                                        line.append( gc.getPlayer(iCiv).getSettlersMaps( con.iMapMaxY-j-1, i ) )
##                                grid.append( line )
##                        self.lSettlersMap.append( grid )
##                print self.lSettlersMap




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
                                                #check if a world war is already in place
                                                iNumAlreadyWar = 0
                                                tLoopCiv = gc.getTeam(gc.getPlayer(iLoopCiv).getTeam())
                                                for kLoopCiv in range( iNumPlayers ):
                                                        if (tLoopCiv.isAtWar(kLoopCiv)):
                                                                iNumAlreadyWar += 1
                                                if (iNumAlreadyWar >= 5):
                                                        iAlreadyAttacked += 2 #much less likely to attack
                                                elif (iNumAlreadyWar >= 3):
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
##                        for jLoopCiv in range( iNumTotalPlayers ):
##                                if (tCiv.isDefensivePact(jLoopCiv) and gc.getTeam(gc.getPlayer(iLoopCiv).getTeam()).isDefensivePact(jLoopCiv)):
##                                        lTargetCivs[iLoopCiv] /= 2
                                
                                
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


