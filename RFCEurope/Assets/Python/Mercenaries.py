# Rhye's and Fall of Civilization - Mercenaries Written mostly by 3Miro


from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
import cPickle as pickle
import Consts as con
import XMLConsts as xml

from sets import Set

iNumPlayers = con.iNumPlayers

iMercPromotion = 48

#PyGame = PyHelpers.PyGame()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iMercCostPerTurn = con.iMercCostPerTurn

# list of all available mercs, unit type, text key name, start turn, end turn, provinces, blocked by religions, odds
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
iNumTotalPromotions = 39 # without navigation and leaders
iNumPromotionsSoftCap = 3 # canget more promotions if you get a high promotion (i.e. combat 5), but overall it should be unlikely
iNumPromorionIterations = 3 # how many attemps shall we make to add promotion (the bigger the number, the more likely it is for a unit to have at least iNumPromotionsSoftCap promotions)

class MercenaryManager:

        def __init__(self ):
                self.lGlobalPool = []
                self.lHiredBy = []
                self.GMU = GlobalMercenaryUtils()
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
                iIterations = 0 # limit the number of iterations so we can have mercs with only a few promotions
                while ( iNumPromotions < iNumPromotionsSoftCap and iIterations < iNumPromorionIterations):
                        iPromotion = gc.getGame().getSorenRandNum( iNumTotalPromotions, 'merc get promotion')
                        if ( isPromotionValid(iPromotion, lMercInfo[0], False) ):
                                if ( (not iPromotion in lPromotions) and gc.getGame().getSorenRandNum( 100, 'merc set promotion') < lPromotionOdds[iPromotion] ):
                                        lPromotions.append(iPromotion)
                                        lPromotions = self.setPrereqConsistentPromotions( lPromotions )
                                        iNumPromotions = len( lPromotions )
                        iIterations += 1
                
                (iPurchaseCost, iUpkeepCost) = self.GMU.getCost( iMerc, lPromotions )
                
                # add the merc, keep the merc index, costs and promotions
                self.lGlobalPool.append( [iMerc, lPromotions, iPurchaseCost, iUpkeepCost] )
                
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
                iHuman = gc.getGame().getActivePlayer()
                
                #for lMerc in self.lGlobalPool:
                #        print( "3Miro Merc Pool: ", iGameTurn, lMerc)
                
                # Go through each of the players and deduct their mercenary maintenance amount from their gold (round up)
                for iPlayer in range( iNumPlayers ): # minus the Pope
                        pPlayer = gc.getPlayer( iPlayer )
                        if ( pPlayer.isAlive() ):
                                pPlayer.setGold(pPlayer.getGold()-(pPlayer.getPicklefreeParameter( iMercCostPerTurn )+99)/100 )
                                # TODO: AI
                                #if ( iPlayer != iHuman ):
                                #        self.processMercAI( pPlayer )
                        #playerList[i].setGold(playerList[i].getGold()-(playerList[i].getPicklefreeParameter( iMercCostPerTurn )+99)/100 )
                        
                
                
                        
                self.processNewMercs( iGameTurn ) # add new Merc to the pool
                        
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
                
        def processMercAI( self, pPlayer ):
                if ( pPlayer.isHuman() or pPlayer.isBarbarian() or pPlayer.getID() == con.iPope ):
                        return
                        
                iWarValue = 0 # compute the total number of wars being fought at the moment
                
                teamPlayer = gc.getTeam(pPlayer.getTeam())
                for iOponent in range( con.iNumTotalPlayers ):
                        if ( teamPlayer.isAtWar( gc.getPlayer( iOponent ).getTeam() ) ):
                               iWarValue += 1
                               if ( iOponent <= con.iPope ):
                                       iWarValue += 3
                                       
                # decide to hire or fire mercs
                # if we are at peace or have only a small war, then we can keep the merc if the expense is trivial
                # otherwise we should get rid of some mercs
                # we should also fire mercs if we spend too much
                
                bFire = False
                
                iGold = pPlayer.getGold()
                iUpkeep = pPlayer.getPicklefreeParameter( iMercCostPerTurn )
                
                if ( 100*iGold < iUpkeep ):
                        # can't affort mercs, fire someone
                        bFire = True
                elif ( iWarValue < 4 and 50*iGold < iUpkeep ):
                        # mercs cost > 1/2 of our gold
                        bFire = True
                elif ( iWarValue < 2 and 20*iGold < iUpkeep ):
                        bFire = True
                
                if ( bFire ):
                        # the AI fires a Merc
                        self.FireMercAI( pPlayer )
                        
                        # make sure we can affort the mercs that we keep
                        while ( pPayer.getPicklefreeParameter( iMercCostPerTurn )>0 and 100*pPlayer.getGold() < pPayer.getPicklefreeParameter( iMercCostPerTurn ) ):
                                self.FireMercAI( pPlayer )
                        return
                        
                if ( iWarValue > 0 ):
                        #we ave to be at war to hire
                        iOdds = con.tHire[pPlayer.getID()]
                        if ( iWarValue < 2 ):
                                iOdds *= 2 # small wars are hardly worth the trouble
                        if ( iWarValue > 4 ): # large war
                                iOdds /= 2
                        
                        if ( gc.getGame().getSorenRandNum(100, 'shall we hire a merc') > iOdds ):
                                # hiring a merc
                                self.HireMercAI( pPlayer )
                        
                        
        def FireMercAI( self, pPlayer ):
                iNumUnits = pPlayer.getNumUnits()
                lMercs = []
                iGameTurn = gc.getGame().getGameTurn()
                for iUnit in range( iNumUnits ):
                        pUnit = pPlayer.getUnit( iUnit )
                        if ( pUnit.getMercID() > -1 ):
                                lMercs.append( pUnit )
                                
                if ( len( lMercs ) > 0 ):
                        # we have mercs, so fire someone
                        lMercValue = [] # estimate how "valuable" the merc is (high value is bad)
                        for pUnit in lMercs:
                                iValue = pUnit.getMercUpkeep()
                                pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
                                if ( pPlot.isCity() ):
                                        if ( pPlot.getPlotCity().getOwner() == pPlayer.getID() ):
                                                # keep the city defenders
                                                iDefenders = self.getNumDefendersAtPlot( pPlot )
                                                if ( iDefenders < 2 ):
                                                        iValue /= 100
                                                elif ( iDefenders < 4 ):
                                                        iValue /= 2
                                
                                if ( iGameTurn > lMercList[ pUnit.getMercID() ][3] ):
                                        # obsolete units
                                        iValue *= 2
                                if ( iGameTurn > lMercList[ pUnit.getMercID() ][3] + 100 ):
                                        # really obsolete units
                                        iValue *= 10
                                lMercValue.append( iValue )
                                
                        iSum = 0
                        for iI in range( len( lMercValue ) ):
                                iSum += lMercValue[iI]

                        iFireRand = gc.getGame().getSorenRandNum(iSum, 'random merc city')
                        for iI in range( len( lMercValue ) ):
                                iFireRand -= lMercValue[iI]
                                if ( iFireRand < 0 ):
                                        self.GMU.fireMerc( lMercs[iI] )
                                        return
                                        
        def HireMercAI( self, pPlayer ):
                # decide which merc to hire
                lCanHireMercs = []
                sPlayerProvinces = Set( self.getOwnedProvinces( pPlayer ) )
                iGold = pPlayer.getGold()
                for lMerc in self.lGlobalPool:
                        iMercTotalCost = lMerc[2] + (lMerc[3]+99)/100
                        sMercProvinces = Set( lMercList[lMerc[0]][4] )
                        if ( iGold > iMercTotalCost and len( sPlayerProvinces & sMercProvinces ) > 0 ):
                              lCanHireMercs.append( lMerc )
                              
                if ( len( lCanHireMercs ) > 0 ):
                        iRandomMerc = gc.getGame().getSorenRandNum(len( lCanHireMercs ), 'random merc to hire')
                        
                        self.GMU.hireMerc( lCanHireMercs[iRandomMerc], pPlayer.getID() )
                        self.getMercLists()
                        
        def getOwnedProvinces( self, pPlayer ):
                lProvList = [] # all available cities that the Merc can appear in
                apCityList = PyPlayer(pPlayer.getID()).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        iProvince = city.getProvince()
                        if ( not (iProvince in lProvList) ):
                              lProvList.append( iProvince )
                return lProvList
                        
        def getNumDefendersAtPlot( self, pPlot ):
		iOwner = pPlot.getOwner()
		if ( iOwner < 0 ):
			return 0
		iNumUnits = pPlot.getNumUnits()
		iDefenders = 0
		for i in range( iNumUnits ):
			if ( pPlot.getUnit(i).getOwner() == iOwner ):
				iDefenders += 1
		return iDefenders
                
                
class GlobalMercenaryUtils:
        # the idea of this class is to provide ways to manipulate the mercenaries without the need to make a separate instance of the MercenaryManager
        # the MercManager provides event driven functions and those should be called from the event interface
        # the Utils class should be used for interface commands (like for the Human UI)
        
        def getMercGlobalPool( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lMercGlobalPool']
                
        def setMercGlobalPool( self, lNewPool ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lMercGlobalPool'] = lNewPool
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getMercHiredBy( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lMercsHiredBy']
        
        def setMercHiredBy( self, lNewList ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lMercsHiredBy'] = lNewList
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getCost( self, iMerc, lPromotions ):
                # note that the upkeep is in the units of 100, i.e. iUpkeepCost = 100 means 1 gold
                lMercInfo = lMercList[iMerc]
                
                # compute cost
                iBaseCost = (80 * gc.getUnitInfo( lMercInfo[0] ).getProductionCost()) / 100
                iPercentage = 0
                for iPromotion in lPromotions:
                        iPercentage += lPromotionCost[iPromotion]
                iPurchaseCost = ( iBaseCost * ( 100 + iPercentage ) ) / 100
                
                iUpkeepCost = 100 + 3*iPercentage # 1 gold for 1/3 increase of cost due to promotions
                
                return (iPurchaseCost, iUpkeepCost)
                
        
        def hireMerc( self, lMerc, iPlayer ):
                # the player would hire a merc
                lGlobalPool = self.getMercGlobalPool()
                lHiredByList = self.getMercHiredBy()
                
                pPlayer = gc.getPlayer( iPlayer )
                if ( pPlayer.getGold() < lMerc[2] ):
                        return
                
                lCityList = [] # all available cities that the Merc can appear in
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        if ( city.getProvince() in lMercList[ lMerc[0] ][4] ):
                              lCityList.append( city )
                              
                if ( len( lCityList ) == 0 ):
                        return
                
                pCity = lCityList[gc.getGame().getSorenRandNum(len(lCityList), 'random merc city')]
                
                iX = pCity.getX()
                iY = pCity.getY()
                
                # do the Gold
                pPlayer.setGold( pPlayer.getGold() - lMerc[2] )
                pPlayer.setPicklefreeParameter( iMercCostPerTurn, pPlayer.getPicklefreeParameter( iMercCostPerTurn ) + lMerc[3] )
                
                # remove the merc from the golbal pool and set the "hired by" index
                lGlobalPool.remove( lMerc )
                lHiredByList[lMerc[0]] = iPlayer
                
                self.setMercGlobalPool( lGlobalPool )
                self.setMercHiredBy( lHiredByList )
                
                # make the unit:
                pUnit = pPlayer.initUnit( lMercList[lMerc[0]][0], iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH )
                pUnit.setName( CyTranslator().getText( lMercList[lMerc[0]][1] , ()) )
                
                # add the promotions
                for iPromotion in lMerc[1]:
                        pUnit.setHasPromotion( iPromotion, False )
                        
                pUnit.setHasPromotion( iMercPromotion, False )
                
                # set the MercID
                pUnit.setMercID( lMerc[0] )
                
                # set the Upkeep
                pUnit.setMercUpkeep( lMerc[3] )
                
        def fireMerc( self, pMerc ):
                # fires the merc unit pMerc (pointer to CyUnit)
                lHiredByList = self.getMercHiredBy()
                
                # get the Merc info
                iMerc = pMerc.getMercID()
                iUpkeep = pMerc.getMercUpkeep()
                
                if ( iMerc < 0 ):
                        return
                
                # free the Merc for a new contract
                lHiredByList[iMerc] = -1
                self.setMercHiredBy( lHiredByList )
                
                # lower the upkeep
                pPlayer = gc.getPlayer( pMerc.getOwner() )
                pPlayer.setPicklefreeParameter( iMercCostPerTurn, max( 0, pPlayer.getPicklefreeParameter( iMercCostPerTurn ) - iUpkeep ) )
                
                pMerc.kill( 0, -1 )
                
                
                
                
                
        
