# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
import cPickle as pickle
import Consts as con
import XMLConsts as xml

iNumPlayers = con.iNumPlayers

iMercPromotion = 48

#PyGame = PyHelpers.PyGame()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iMercCostPerTurn = con.iMercCostPerTurn

# list of all available mercs, unit type, text key name, start turn, end turn, provinces, blocked religions, odds
lMercList = [ [xml.iArcher, "TXT_KEY_SERBIAN", 0, 100, [xml.iP_Serbia,xml.iP_IleDeFrance,xml.iP_Orleans], [], 10 ],
                ]

### A few Parameters for Mercs only:
# Promotions and their odds, higher promotions have very low probability, leaders and navigation don't appear
# combat 1 - 5, cover (vs archer), shock (vs heavy infantry), formation (vs heavy horse), charge (vs siege), ambush (vs light cav), feint (vs polearm), amphibious, march (movement heal), medic 1-2, 
# gurilla (hill defense) 1-3, woodsman 1-3, city raider 1-3, garrason 1-3, drill 1-4, barrage (collateral) 1-3, accuracy (more bombard), flanking (vs siege) 1-2, sentry (vision), mobility (movement), 
# navigation 1-2, leader, leadership (more XP), tactic (withdraw), commando (enemy roads), combat 6, morale (movement), medic 3, merc 
lPromotionOdds = [ 100, 80, 40, 10,  5, 50, 50, 60, 40, 20, 50, 20, 10, 40, 20, 80, 50, 30, 80, 50, 30, 80, 40, 10, 60, 30, 10, 60, 40, 10,  5, 60, 40, 10, 60, 50, 30, 20, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
# The way promotions would affect the cost of the mercenary (percentage wise)
lPromotionCost = [  10, 15, 30, 30, 40, 20, 20, 20, 20, 20, 20, 30, 40, 20, 30, 15, 20, 30, 15, 20, 30, 20, 30, 50, 20, 30, 50, 10, 20, 40, 50, 10, 10, 10, 20, 10, 10, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
iNumPromotions = 39 # without navigation and leaders
iNumPromotionsSoftCap = 3 # canget more promotions if you get a high promotion (i.e. combat 5), but overall it should be unlikely


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
                
        def setPrereqConsistentPromotions( self, lPromotions ):
                bPass = True
                while ( not bPass ):
                        bPass = True
                        for iPromotion in lPromotions:
                                pPromotionInfo = gc.getPromotionInfo( iPromotion )
                                iPrereq = pPromotionInfo.getPrereqOrPromotion1()
                                if ( iPrereq != -1 and ( not iPrereq in lPromotions ) ):
                                        lPromotions.append( iPrereq )
                                        bPass = False
                                iPrereq = pPromotionInfo.getPrereqOrPromotion2()
                                if ( iPrereq != -1 and ( not iPrereq in lPromotions ) ):
                                        lPromotions.append( iPrereq )
                                        bPass = False
                return lPromotions
                
        def addNewMerc( self, iMerc ):
                # this processes the available promotions
                lMercInfo = lMercList[iMerc]
                
                # get the promotions
                iNumPromotions = 0
                lPromotions = []
                while ( iNumPromotions < iNumPromotionsSoftCap ):
                        iPromotion = gc.getGame().getSorenRandNum( iNumPromotions, 'merc get promotion')
                        if ( isPromotionValid(iPromotionInfoType, lMercInfo[0], False) ):
                                if ( gc.getGame().getSorenRandNum( 100, 'merc set promotion') < lPromotionOdds[iPromotion] ):
                                        lPromotions.append(iPromotion)
                                        lPromotions = self.setPrereqConsistentPromotions( lPromotions )
                                        iNumPromotions = len( lPromotions )
                # compute cost?                        
                                        
                
                pass
                
        def processNewMercs( self, iGameTurn ):
                # add new mercs to the pool
                
                potentialMercs = []
                alreadyAvailableMercs = []
                for iI in range( len( self.lGlobalPool ) ):
                        alreadyAvailableMercs.append( self.lGlobalPool[iI][0] )
                
                for iMerc in range( len( lMercList ) ):
                        if ( self.lHiredBy[iMerc] == -1 and (not iMerc in alreadyAvailableMercs) and iGameTurn >= lMercList[iMerc][2] and iGameTurn <= lMercList[iMerc][3] ):
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
                
                
