# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
import cPickle as pickle
import Consts as con
import XMLConsts as xml

iNumPlayers = con.iNumPlayers

#PyGame = PyHelpers.PyGame()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iMercCostPerTurn = con.iMercCostPerTurn

# list of all available mercs, unit type, text key name, start turn, end turn, provinces, blocked religions, odds
lMercList = [ [xml.iArcher, "TXT_KEY_SERBIAN", 0, 100, [xml.iP_Serbia,xml.iP_IleDeFrance,xml.iP_Orleans], [], 10 ],
                ]

class MercenaryManager:

        def __init__(self ):
                self.lGlobalPool = []
                self.lHiredBy = []
		pass

        def getMercLists(self):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                self.lGlobalPool = scriptDict['lMercGlobalPool']
                self.lHiredBy = scriptDict['lMercsHiredBy']
                
        def setMercLists( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lMercGlobalPool'] = self.lGlobalPool
                scriptDict['lMercsHiredBy'] = self.lHiredBy
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def addNewMerc( self, iMerc ):
                # this processes the available promotions
                pass
                
        def processNewMercs( self, iGameTurn ):
                # add new mercs to the pool
                
                potentialMercs = []
                for iMerc in range( len( lMercList ) ):
                        if ( self.lHiredBy[iMerc] == -1 and iGameTurn >= lMercList[iMerc][2] and iGameTurn <= lMercList[iMerc][3] ):
                                potentialMercs.append( iMerc )
                
                iNumPotentialMercs = len( potentialMercs )
                if ( iNumPotentialMercs == 0 ):
                        return
                # if there are mercs to be potentially added
                iStart = gc.getGame().getSorenRandNum( iNumPotentialMercs, 'starting Merc')
                for iOffset in range( iNumPotentialMercs ):
                        iMerc = potentialMercs[( iOffset + iStart ) % iNumPotentialMercs]
                        if ( gc.getGame().getSorenRandNum( 100, 'merc appearing in global pool') < lMercList[iMerc][6] ):
                                # adding a new merc
                                self.addNewMerc( iMerc )

        def doMercsTurn( self, iGameTurn ):
        # this is called at the end of the game turn
        # thus the AI gets the advantage to make the Merc "decision" with the most up-to-date political data and they can get the mercs instantly
        # the Human gets the advantage to get the first pick at the available mercs
        
                self.getMercLists() # load the current mercenary pool
                        
                # Go through each of the players and deduct their mercenary maintenance amount from their gold (round up)
                for iPlayer in range( iNumPlayers ): # minus the Pope
                        pPlayer = gc.getPlayer( iPlayer )
                        if ( pPlayer.isAlive() ):
                                pPlayer.setGold(pPlayer.getGold()-(pPlayer.getPicklefreeParameter( iMercCostPerTurn )+99)/100 )
                        #playerList[i].setGold(playerList[i].getGold()-(playerList[i].getPicklefreeParameter( iMercCostPerTurn )+99)/100 )
                        
                
                        
                self.setMercLists() # save the potentially modified merc list (this allows for pickle read/write only once per turn)

        def onUnitPromoted( self, argsList ):
                pUnit, iPromotion = argsList
                if ( pUnit.getMercID() > -1 ):
                        # redraw the main screen to update the upkeep info
                        CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)


        def onUnitKilled(self, argsList):
                unit, iAttacker = argsList
                pass

        def onUnitLost(self, argsList):
                # this gets called on lost and on upgrade, check to remove the merc if it has not been upgraded?
                unit = argsList[0]
                
                
                pass
                
                
