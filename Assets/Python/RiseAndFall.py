# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
import PyHelpers        # LOQ
import Popup
import cPickle as pickle                # LOQ 2005-10-12
import CvTranslator
import RFCUtils
import Consts as con


################
### Globals ###
##############

gc = CyGlobalContext()        # LOQ
PyPlayer = PyHelpers.PyPlayer        # LOQ
utils = RFCUtils.RFCUtils()

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 66
iRebellionDelay = 15
iEscapePeriod = 30
tAIStopBirthThreshold = con.tAIStopBirthThreshold
tBirth = con.tBirth

iWorker = con.iWorker
iSettler = con.iSettler
iSpearman = con.iSpearman

# initialise player variables
iBurgundy = con.iBurgundy
iByzantium = con.iByzantium
iFrankia = con.iFrankia
iArabia = con.iArabia
iBulgaria = con.iBulgaria
iCordoba = con.iCordoba
iSpain = con.iSpain
iNorse = con.iNorse
iVenecia = con.iVenecia
iKiev = con.iKiev
iHungary = con.iHungary
iGermany = con.iGermany
iPoland = con.iPoland
iMoscow = con.iMoscow
iGenoa = con.iGenoa
iEngland = con.iEngland
iPortugal = con.iPortugal
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
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers


pBurgundy = gc.getPlayer(iBurgundy)
pByzantium = gc.getPlayer(iByzantium)
pFrankia = gc.getPlayer(iFrankia)
pArabia = gc.getPlayer(iArabia)
pBulgaria = gc.getPlayer(iBulgaria)
pCordoba = gc.getPlayer(iCordoba)
pSpain = gc.getPlayer(iSpain)
pNorse = gc.getPlayer(iNorse)
pVenecia = gc.getPlayer(iVenecia)
pKiev = gc.getPlayer(iKiev)
pHungary = gc.getPlayer(iHungary)
pGermany = gc.getPlayer(iGermany)
pPoland = gc.getPlayer(iPoland)
pMoscow = gc.getPlayer(iMoscow)
pGenoa = gc.getPlayer(iGenoa)
pEngland = gc.getPlayer(iEngland)
pPortugal = gc.getPlayer(iPortugal)
pAustria = gc.getPlayer(iAustria)
pTurkey = gc.getPlayer(iTurkey)
pSweden = gc.getPlayer(iSweden)
pDutch = gc.getPlayer(iDutch)
pPope = gc.getPlayer( iPope )
pIndependent = gc.getPlayer(iIndependent)
pIndependent2 = gc.getPlayer(iIndependent2)
pBarbarian = gc.getPlayer(iBarbarian)

teamBurgundy = gc.getTeam(pBurgundy.getTeam())
teamByzantium = gc.getTeam(pByzantium.getTeam())
teamFrankia = gc.getTeam(pFrankia.getTeam())
teamArabia = gc.getTeam(pArabia.getTeam())
teamBulgaria = gc.getTeam(pBulgaria.getTeam())
teamCordoba = gc.getTeam(pCordoba.getTeam())
teamSpain = gc.getTeam(pSpain.getTeam())
teamNorse = gc.getTeam(pNorse.getTeam())
teamVenecia = gc.getTeam(pVenecia.getTeam())
teamKiev = gc.getTeam(pKiev.getTeam())
teamHungary = gc.getTeam(pHungary.getTeam())
teamGermany = gc.getTeam(pGermany.getTeam())
teamPoland = gc.getTeam(pPoland.getTeam())
teamMoscow = gc.getTeam(pMoscow.getTeam())
teamGenoa = gc.getTeam(pGenoa.getTeam())
teamEngland = gc.getTeam(pEngland.getTeam())
teamPortugal = gc.getTeam(pPortugal.getTeam())
teamAustria = gc.getTeam(pAustria.getTeam())
teamTurkey = gc.getTeam(pTurkey.getTeam())
teamSweden = gc.getTeam(pSweden.getTeam())
teamDutch = gc.getTeam(pDutch.getTeam())
teamPope = gc.getTeam(pPope.getTeam())
teamIndependent = gc.getTeam(pIndependent.getTeam())
teamIndependent2 = gc.getTeam(pIndependent2.getTeam())
teamBarbarian = gc.getTeam(pBarbarian.getTeam())


#for not allowing new civ popup if too close
#Sedna17, moving around the order in which civs rise without changing their WBS requires you to do funny things here to prevent "Change Civ?" popups
#Spain and Moscow have really long delays for this reason
#This is now obsolete
#tDifference = (0, 0, 0, 1, 0, 1, 10, 0, 0, 1, 0, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

lReformationMatrix = con.lReformationMatrix

tVisible = con.tVisible


# starting locations coordinates
tCapitals = con.tCapitals



# core areas coordinates (top left and bottom right)

tCoreAreasTL = con.tCoreAreasTL
tCoreAreasBR = con.tCoreAreasBR

tExceptions = con.tExceptions

tNormalAreasTL = con.tNormalAreasTL
tNormalAreasBR = con.tNormalAreasBR

tBroaderAreasTL = con.tBroaderAreasTL 
tBroaderAreasBR = con.tBroaderAreasBR

tLeaders = con.tLeaders
tEarlyLeaders = con.tEarlyLeaders
tLateLeaders = con.tLateLeaders

class RiseAndFall:


##################################################
### Secure storage & retrieval of script data ###
################################################
        

        def getNewCiv( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iNewCiv']

        def setNewCiv( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iNewCiv'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )        

        def getNewCivFlip( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iNewCivFlip']

        def setNewCivFlip( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iNewCivFlip'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )      

        def getOldCivFlip( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iOldCivFlip']

        def setOldCivFlip( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iOldCivFlip'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getTempTopLeft( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['tempTopLeft']

        def setTempTopLeft( self, tNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['tempTopLeft'] = tNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) ) 

        def getTempBottomRight( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['tempBottomRight']

        def setTempBottomRight( self, tNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['tempBottomRight'] = tNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) ) 

        def getSpawnWar( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iSpawnWar']

        def setSpawnWar( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iSpawnWar'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getAlreadySwitched( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['bAlreadySwitched']

        def setAlreadySwitched( self, bNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['bAlreadySwitched'] = bNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getColonistsAlreadyGiven( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lColonistsAlreadyGiven'][iCiv]

        def setColonistsAlreadyGiven( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lColonistsAlreadyGiven'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getNumCities( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lNumCities'][iCiv]

        def setNumCities( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lNumCities'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getSpawnDelay( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lSpawnDelay'][iCiv]

        def setSpawnDelay( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lSpawnDelay'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getFlipsDelay( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lFlipsDelay'][iCiv]

        def setFlipsDelay( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lFlipsDelay'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getBetrayalTurns( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iBetrayalTurns']

        def setBetrayalTurns( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iBetrayalTurns'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )  

        def getLatestFlipTurn( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iLatestFlipTurn']

        def setLatestFlipTurn( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iLatestFlipTurn'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getLatestRebellionTurn( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lLatestRebellionTurn'][iCiv]

        def setLatestRebellionTurn( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lLatestRebellionTurn'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getRebelCiv( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iRebelCiv']

        def setRebelCiv( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iRebelCiv'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getRebelCities( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lRebelCities']
                
        def setRebelCities( self, lCityList ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lRebelCities'] = lCityList
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getRebelSuppress( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lRebelSuppress']
                
        def setRebelSuppress( self, lSuppressList ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lRebelSuppress'] = lSuppressList
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getExileData( self, i ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lExileData'][i]

        def setExileData( self, i, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lExileData'][i] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
        
        def getTempFlippingCity( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['tempFlippingCity']

        def setTempFlippingCity( self, tNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['tempFlippingCity'] = tNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) ) 

        def getCheatersCheck( self, i ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lCheatersCheck'][i]

        def setCheatersCheck( self, i, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lCheatersCheck'][i] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getBirthTurnModifier( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lBirthTurnModifier'][iCiv]

        def setBirthTurnModifier( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lBirthTurnModifier'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )   

        def getDeleteMode( self, i ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lDeleteMode'][i]

        def setDeleteMode( self, i, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lDeleteMode'][i] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getFirstContactConquerors( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lFirstContactConquerors'][iCiv]

        def setFirstContactConquerors( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lFirstContactConquerors'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) ) 
                
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
                        gc.getActivePlayer().setHandicapType(gc.getPlayer(self.getNewCiv()).getHandicapType())
                        gc.getGame().setActivePlayer(self.getNewCiv(), False)
                        gc.getPlayer(self.getNewCiv()).setHandicapType(iOldHandicap)
                        for i in range(con.iNumStabilityParameters):
                                utils.setStabilityParameters(utils.getHumanID(),i, 0)
                                utils.setLastRecordedStabilityStuff(0, 0)
                                utils.setLastRecordedStabilityStuff(1, 0)
                                utils.setLastRecordedStabilityStuff(2, 0)
                                utils.setLastRecordedStabilityStuff(3, 0)
                                utils.setLastRecordedStabilityStuff(4, 0)
                                utils.setLastRecordedStabilityStuff(5, 0)
                        for iMaster in range(con.iNumPlayers):
                                if (gc.getTeam(gc.getPlayer(self.getNewCiv()).getTeam()).isVassal(iMaster)):
                                        gc.getTeam(gc.getPlayer(self.getNewCiv()).getTeam()).setVassal(iMaster, False, False)
                        self.setAlreadySwitched(True)
                        gc.getPlayer(self.getNewCiv()).setPlayable(True)
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
                        CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_AGREED", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
                                                
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
                                        #        if (city.getPopulation() < iEra):
                                        #                city.setPopulation(iEra) #causes an unidentifiable C++ exception

                                        #humanCityList[i].setHasRealBuilding(con.iPlague, False) #buggy

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
                        CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
                                                

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
                #self.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
                #               CyTranslator().getText("TXT_KEY_REBELLION_TEXT", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
                #               (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), \
                #                CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
                iLoyalPrice = min( (10 * gc.getPlayer( iHuman ).getGold()) / 100, 50 * iNumCities )
                self.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
                                CyTranslator().getText("TXT_KEY_REBELION_HUMAN", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
                                (CyTranslator().getText("TXT_KEY_REBELION_LETGO", ()), \
                                CyTranslator().getText("TXT_KEY_REBELION_DONOTHING", ()), \
                                CyTranslator().getText("TXT_KEY_REBELION_CRACK", ()), \
                                CyTranslator().getText("TXT_KEY_REBELION_BRIBE", ()) + " " + str(iLoyalPrice), \
                                CyTranslator().getText("TXT_KEY_REBELION_BOTH", ())))

        def eventApply7622(self, popupReturn):
                #iHuman = utils.getHumanID()
                #iRebelCiv = self.getRebelCiv()
                #if( popupReturn.getButtonClicked() == 0 ): # 1st button
                #        gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iRebelCiv)                                                   
                #elif( popupReturn.getButtonClicked() == 1 ): # 2nd button
                #        gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iRebelCiv, False, -1)
                iHuman = utils.getHumanID()
                iRebelCiv = self.getRebelCiv()
                iChoice = popupReturn.getButtonClicked()
                if ( iChoice == 1 ):
                        lList = self.getRebelSurppress()
                        lList[iHuman] = 2 # let go + war
                        self.setRebelSurppress( lList )
                elif( iChoice == 2 ):
                        if ( gc.getGame().getSorenRandNum(100, 'odds') > 55 ):
                                lCityList = self.getRebelCities()
                                for iCity in range( len( lCityList ) ):
                                        pCity = gc.getMap().plot( lCityList[iCity][0], lCityList[iCity][1] ).getPlotCity()
                                        if ( pCity.getOwner() == iHuman ):
                                                pCity.changeOccupationTimer( 2 )
                                                pCity.changeHurryAngerTimer( 10 )
                                lList = self.getRebelSurppress()
                                lList[iHuman] = 3 # keep cities + war
                                self.setRebelSurppress( lList )
                        else:
                                lList = self.getRebelSurppress()
                                lList[iHuman] = 4 # let go + war
                                self.setRebelSurppress( lList )
                elif( iChoice == 3 ):
                        iLoyalPrice = min( (10 * gc.getPlayer( iHuman ).getGold()) / 100, 50 * iNumCities )
                        gc.getPlayer( iHuman ).setGold( gc.getPlayer( iHuman ).getGold() - iLoyalPrice )
                        if ( gc.getGame().getSorenRandNum(100, 'odds') < iLoyalPrice / iNumCities ):
                                lList = self.getRebelSurppress()
                                lList[iHuman] = 1 # keep + no war
                                self.setRebelSurppress( lList )
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
                                lList = self.getRebelSurppress()
                                lList[iHuman] = 3 # keep + no war
                                self.setRebelSurppress( lList )
                                                        
                        else:
                                lList = self.getRebelSurppress()
                                lList[iHuman] = 2 # let go + war
                                self.setRebelSurppress( lList )        
                self.resurectCiv( self.getRebelCiv() )
        ### Reformation Begin ###
        def reformationPopup(self):
                self.showPopup(7624, CyTranslator().getText("TXT_KEY_REFORMATION_TITLE", ()), CyTranslator().getText("TXT_KEY_REFORMATION_MESSAGE",()), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))

        def eventApply7624(self, popupReturn):
                iHuman = utils.getHumanID()
                if(popupReturn.getButtonClicked() == 0):
                        self.reformationyes(iHuman)
                elif(popupReturn.getButtonClicked() == 1):
                        self.reformationno(iHuman)
        ### Reformation End ###




#######################################
### Main methods (Event-Triggered) ###
#####################################  

        def setup(self):            

                #self.setupBirthTurnModifiers() (causes a crash on civ switch)

                # 3Miro:
                #if (not gc.getPlayer(0).isPlayable()): #late start condition
                #        self.clear600ADChina()

                #if (gc.getPlayer(0).isPlayable()): #late start condition
                self.create4000BCstartingUnits()
                #else:
                #        self.create600ADstartingUnits()
                #self.assign4000BCtechs()
                self.setEarlyLeaders()


                # initial Gold and Stability modifyers
                #if (not gc.getPlayer(0).isPlayable()): #late start condition
                #        self.assign600ADTechs()
                #        pChina.changeGold(300)
                #        pJapan.changeGold(150)
                #        pIndependent.changeGold(100)
                #        pIndependent2.changeGold(100)
                #        pNative.changeGold(300)
                #        pCeltia.changeGold(500)
                #        utils.setStability(iVikings, utils.getStability(iVikings) + 2)
                #        utils.setStability(iChina, utils.getStability(iChina) + 3)
                #        utils.setStability(iJapan, utils.getStability(iJapan) + 4)
                #else:
                #        utils.setStability(iChina, utils.getStability(iChina) + 2)
                #        utils.setStability(iIndia, utils.getStability(iIndia) + 2)
                #        pIndependent.changeGold(50)
                #        pIndependent2.changeGold(50)
                #        pNative.changeGold(100)
                
                
                               
                # set starting gold
                pBurgundy.changeGold( 50 )
                pByzantium.changeGold( 1000 )
                pFrankia.changeGold( 50 )
                pArabia.changeGold( 200 )
                pBulgaria.changeGold( 100 )
                pCordoba.changeGold( 200 )
                pSpain.changeGold( 500 )
                pNorse.changeGold( 200 )
                pVenecia.changeGold(300)
                pKiev.changeGold(250)
                pHungary.changeGold(300)
                pGermany.changeGold(300)
                pPoland.changeGold(300)
                pMoscow.changeGold(400)
                pGenoa.changeGold(400)
                pEngland.changeGold(400)
                pPortugal.changeGold(450)
                pAustria.changeGold(700)
                pTurkey.changeGold(1000)
                pSweden.changeGold(1000)
                pDutch.changeGold(1500)
                pIndependent.changeGold(50)
                pIndependent2.changeGold(50)
           
                # display welcome message
                #self.displayWelcomePopup()

                # 3Miro: only the very first civ in the WB file
                if (pBurgundy.isHuman()):
                        plotBurgundy = gc.getMap().plot(tCapitals[iBurgundy][0], tCapitals[iBurgundy][1])   
                        unit = plotBurgundy.getUnit(0)
                        unit.centerCamera()
                #center camera on Egyptian units
                #if (pEgypt.isHuman()):
                #        plotEgypt = gc.getMap().plot(tCapitals[iEgypt][0], tCapitals[iEgypt][1])   
                #        unit = plotEgypt.getUnit(0)
                #        unit.centerCamera()
                #        #print (unit)


        def clear600ADChina(self):
                pass
                


        def setupBirthTurnModifiers(self):
                #3Miro: first and last civ (first that does not start)
                # not sure if this even gets called, could be depricated
                for iCiv in range(iNumPlayers):
                        if (iCiv >= iArabia and not gc.getPlayer(iCiv).isHuman()):
                                self.setBirthTurnModifier(iCiv, (gc.getGame().getSorenRandNum(11, 'BirthTurnModifier') - 5)) # -5 to +5
                #now make sure that no civs spawn in the same turn and cause a double "new civ" popup
                for iCiv in range(iNumPlayers):
                        if (iCiv > utils.getHumanID() and iCiv < iByzantium):
                                for j in range(iNumPlayers-1-iCiv):
                                        iNextCiv = iCiv+j+1
                                        if (con.tBirth[iCiv]+self.getBirthTurnModifier(iCiv) == con.tBirth[iNextCiv]+self.getBirthTurnModifier(iNextCiv)):
                                                self.setBirthTurnModifier(iNextCiv, (self.getBirthTurnModifier(iNextCiv)+1))



        def setEarlyLeaders(self):
                for i in range(iNumActivePlayers):
                        if (tEarlyLeaders[i] != tLeaders[i][0]):
                                if (not gc.getPlayer(i).isHuman()):
                                        gc.getPlayer(i).setLeader(tEarlyLeaders[i])
                                        print ("leader starting switch:", tEarlyLeaders[i], "in civ", i)
        
        def setWarOnSpawn( self ):
                for i in range( iNumMajorPlayers - 1 ): # exclude the Pope
                        iTeamMajor = gc.getPlayer(i).getTeam()
                        pTeamMajor = gc.getTeam( iTeamMajor )
                        for j in range( iNumTotalPlayers ):
                                if ( con.tWarAtSpawn[i][j] > 0 ): # if there is a chance for war
                                        if ( gc.getGame().getSorenRandNum(100, 'war on spawn roll') < con.tWarAtSpawn[i][j] ):
                                                iTeamSecond = gc.getPlayer(j).getTeam()
                                                pTeamSecond = gc.getTeam( iTeamSecond )
                                                #print(" 3Miro WAR ON SPAWN between ",iTeamMajor,iTeamSecond)
                                                #pTeamMajor.setAtWar( iTeamSecond, True )
                                                #pTeamSecond.setAtWar( iTeamMajot, True )
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
                        for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
                                pIndy = gc.getPlayer( i )
                                if ( pIndy.isAlive() ):
                                        utils.updateMinorTechs(i, iBarbarian)
                        #if (pIndependent.isAlive()):                                  
                        #        utils.updateMinorTechs(iIndependent, iBarbarian)
                        #if (pIndependent2.isAlive()):                                  
                        #        utils.updateMinorTechs(iIndependent2, iBarbarian)

                #Colonists
                # 3Miro: not sure what this does, Conquistadors?
                #if (iGameTurn >= (con.i1350AD + 5 + self.getColonistsAlreadyGiven(iSpain)*6)) and (iGameTurn <= con.i1918AD):
                #        self.giveColonists(iSpain, tBroaderAreasTL[iSpain], tBroaderAreasBR[iSpain])
                #if (iGameTurn >= (con.i1450AD + 5 + self.getColonistsAlreadyGiven(iEngland)*6)) and (iGameTurn <= con.i1918AD):
                #        self.giveColonists(iEngland, tBroaderAreasTL[iEngland], tBroaderAreasBR[iEngland])
                #if (iGameTurn >= (con.i1450AD + 5 + self.getColonistsAlreadyGiven(iFrance)*6)) and (iGameTurn <= con.i1918AD):
                #        self.giveColonists(iFrance, tBroaderAreasTL[iFrance], tBroaderAreasBR[iFrance])
                #if (iGameTurn >= (con.i1350AD + 5 + self.getColonistsAlreadyGiven(iPortugal)*6)) and (iGameTurn <= con.i1918AD):
                #        self.giveColonists(iPortugal, tNormalAreasTL[iPortugal], tNormalAreasBR[iPortugal])
                #if (iGameTurn >= (con.i1450AD + 5 + self.getColonistsAlreadyGiven(iHolland)*6)) and (iGameTurn <= con.i1918AD):
                #        self.giveColonists(iHolland, tNormalAreasTL[iHolland], tNormalAreasBR[iHolland])
                        
                #birth of civs
##                if (gc.getPlayer(0).isPlayable()): #late start condition
##                        self.initBirth(iGameTurn, con.tBirth[iGreece], iGreece)
##                        self.initBirth(iGameTurn, con.tBirth[iPersia], iPersia)    
##                        self.initBirth(iGameTurn, con.tBirth[iCarthage], iCarthage)
##                        self.initBirth(iGameTurn, con.tBirth[iRome], iRome)
##                        self.initBirth(iGameTurn, con.tBirth[iJapan], iJapan)
##                        self.initBirth(iGameTurn, con.tBirth[iEthiopia], iEthiopia)
##                        self.initBirth(iGameTurn, con.tBirth[iMaya], iMaya)
##                        self.initBirth(iGameTurn, con.tBirth[iVikings], iVikings)
##                        self.initBirth(iGameTurn, con.tBirth[iArabia], iArabia)
##                self.initBirth(iGameTurn, con.tBirth[iKhmer], iKhmer)
##                self.initBirth(iGameTurn, con.tBirth[iSpain], iSpain)
##                self.initBirth(iGameTurn, con.tBirth[iFrance], iFrance)
##                self.initBirth(iGameTurn, con.tBirth[iEngland], iEngland)
##                self.initBirth(iGameTurn, con.tBirth[iGermany], iGermany)
##                self.initBirth(iGameTurn, con.tBirth[iRussia], iRussia)
##                self.initBirth(iGameTurn, con.tBirth[iNetherlands], iNetherlands)
##                self.initBirth(iGameTurn, con.tBirth[iMali], iMali)
##                self.initBirth(iGameTurn, con.tBirth[iTurkey], iTurkey)
##                self.initBirth(iGameTurn, con.tBirth[iPortugal], iPortugal)
##                self.initBirth(iGameTurn, con.tBirth[iInca], iInca)
##                self.initBirth(iGameTurn, con.tBirth[iMongolia], iMongolia)
##                self.initBirth(iGameTurn, con.tBirth[iAztecs], iAztecs)
##                self.initBirth(iGameTurn, con.tBirth[iAmerica], iAmerica)
                        
                #if (gc.getPlayer(0).isPlayable()):
                #        iFirstSpawn = iGreece
                #else:
                #        iFirstSpawn = iKhmer
                # 3Miro this should be Arabia
                #iFirstSpawn = iArabia
                #for iLoopCiv in range(iFirstSpawn, iNumMajorPlayers):
                for iLoopCiv in range( iNumMajorPlayers ):
                        if ( (not (tBirth[iLoopCiv] == 0) ) and iGameTurn >= con.tBirth[iLoopCiv] - 3 and iGameTurn <= con.tBirth[iLoopCiv] + 6):
                                self.initBirth(iGameTurn, con.tBirth[iLoopCiv], iLoopCiv)
                # two turns earlier and six turns later call init Birth


                #fragment utility
                # 3Miro: Shuffle cities between Indeps and barbs to make sure there is no big Indep nation   
                if (iGameTurn >= 20 and iGameTurn % 15 == 6):
                        self.fragmentIndependents()
                if (iGameTurn >= 20 and iGameTurn % 30 == 12):
                        self.fragmentBarbarians(iGameTurn)
                        
                        
                #fall of civs
                # 3Miro: check if a civ is conquered and collapsed by barbs or generic
                # 2/3 conquered by barbs = collapse
                # if generically lost 1/2 of the empire in only a few turns (18 I think) = collapse
                # if no city is in the core area and the number of cities in the normal area is less than the other's cities and have no vassal = collapse
                # if stability is bad (-40,-20) and city has some discomfort (not capital, not celebrating, hunger, unhappy, unhealthy, whip ...) 
                #        pick a random city and declare independence
                if (iGameTurn >= 144 and iGameTurn % 4 == 0):
                        self.collapseByBarbs(iGameTurn)                                        
                if (iGameTurn >= 34 and iGameTurn % 18 == 0): #used to be 15 in vanilla, because we must give some time for vassal states to form
                        self.collapseGeneric(iGameTurn)
                if (iGameTurn >= 34 and iGameTurn % 11 == 7): #used to be 8 in vanilla, because we must give some time for vassal states to form
                        self.collapseMotherland(iGameTurn)
                if (iGameTurn > 20 and iGameTurn % 5 == 3):
                #if (iGameTurn > 20 and iGameTurn % 2 == 0):
                        #print(" 3Miro: scession ")
                        self.secession(iGameTurn)
                #debug
                #self.collapseMotherland()

                #resurrection of civs
                # 3Miro: this should not be called with high iNumDeadCivs*
                # Sedna: This is one place to control the frequency of resurrection.
                # Generally we want to allow Kiev, Bulgaria, Cordoba, Burgundy, Byzantium at least to be dead in late game without respawning.
                iNumDeadCivs1 = 12 #5 in vanilla, 8 in warlords (that includes native and celt)
                iNumDeadCivs2 = 6 #3 in vanilla, 6 in Warlords: here we must count natives and celts as dead too
                #if (not gc.getPlayer(0).isPlayable()):  #late start condition
                #        iNumDeadCivs1 -= 2
                #        iNumDeadCivs2 -= 2
                if (gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs1): 
                        if (iGameTurn % 15 == 10):
                                self.resurrection(iGameTurn)                        
                elif (gc.getGame().countCivPlayersEverAlive() - gc.getGame().countCivPlayersAlive() > iNumDeadCivs2): 
                        if (iGameTurn % 30 == 15):
                                self.resurrection(iGameTurn)

                

                #debug
                #self.resurrection(iGameTurn)          
                #self.resurrectionFromBarbs(iGameTurn)




        def checkPlayerTurn(self, iGameTurn, iPlayer):
                #switch leader on first anarchy if early leader is different from primary one, and in a late game anarchy period to a late leader              
##                if (len(tLeaders[iPlayer]) > 1):
##                        if (tEarlyLeaders[iPlayer] != tLeaders[iPlayer][0]):
##                                if (iGameTurn > tBirth[iPlayer]+3 and iGameTurn < tBirth[iPlayer]+50):
##                                        if (gc.getPlayer(iPlayer).getAnarchyTurns() != 0):                                        
##                                                gc.getPlayer(iPlayer).setLeader(tLeaders[iPlayer][0])
##                                                print ("leader early switch:", tLeaders[iPlayer][0], "in civ", iPlayer)                        
##                        elif (iGameTurn >= tLateLeaders[iPlayer][1]):
##                                if (tLateLeaders[iPlayer][0] != tLeaders[iPlayer][0]):   
##                                        if (gc.getPlayer(iPlayer).getAnarchyTurns() != 0):                                                                                     
##                                                gc.getPlayer(iPlayer).setLeader(tLateLeaders[iPlayer][0])
##                                                print ("leader late switch:", tLateLeaders[iPlayer][0], "in civ", iPlayer) 
                if (len(tLeaders[iPlayer]) > 1):
                        if (len(tLateLeaders[iPlayer]) > 5):
                                if (iGameTurn >= tLateLeaders[iPlayer][5]):
                                        self.switchLateLeaders(iPlayer, 4)
                                elif (iGameTurn >= tLateLeaders[iPlayer][1]):
                                        self.switchLateLeaders(iPlayer, 0)
                        else:
                                if (iGameTurn >= tLateLeaders[iPlayer][1]):
                                        self.switchLateLeaders(iPlayer, 0)
            
                    #print( " 3Miro: Called for - ",iPlayer," on turn ",iGameTurn )
                    #utils.setLastTurnAlive( iPlayer, iGameTurn )



        def switchLateLeaders(self, iPlayer, iLeaderIndex):
                if (tLateLeaders[iPlayer][iLeaderIndex] != gc.getPlayer(iPlayer).getLeader()):
                        iThreshold = tLateLeaders[iPlayer][iLeaderIndex+2]
                        if (gc.getPlayer(iPlayer).getCurrentEra() >= tLateLeaders[iPlayer][iLeaderIndex+3]):
                                iThreshold *= 2
                        if (gc.getPlayer(iPlayer).getAnarchyTurns() != 0 or \
                            utils.getPlagueCountdown(iPlayer) > 0 or \
                            utils.getGreatDepressionCountdown(iPlayer) > 0 or \
                            utils.getStability(iPlayer) <= -10 or \
                            gc.getGame().getSorenRandNum(100, 'die roll') < iThreshold):
                                gc.getPlayer(iPlayer).setLeader(tLateLeaders[iPlayer][iLeaderIndex])
                                print ("leader late switch:", tLateLeaders[iPlayer][iLeaderIndex], "in civ", iPlayer)
            
            

        def fragmentIndependents(self):

                for iTest1 in range( con.iIndepStart, con.iIndepEnd + 1):
                        for iTest2 in range( con.iIndepStart, con.iIndepEnd + 1):
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
                                                                utils.flipCity((city.getX(),city.getY()), 0, 0, iSmall, [iBig])   #by trade because by conquest may raze the city
                                                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iSmall)
                                                                iCounter += 1
                                                        if ( iCounter == 3 ):
                                                                break
                                                
                                                        

##                if (pIndependent.getNumCities() > 8 or pIndependent2.getNumCities() > 8 ):
##                        iBigIndependent = -1
##                        iSmallIndependent = -1
##                        if (pIndependent.getNumCities() > 2*pIndependent2.getNumCities()):
##                                iBigIndependent = iIndependent
##                                iSmallIndependent = iIndependent2
##                        if (2*pIndependent.getNumCities() < 2*pIndependent2.getNumCities()):
##                                iBigIndependent = iIndependent2
##                                iSmallIndependent = iIndependent
##                        if (iBigIndependent != -1):
##                                iDivideCounter = 0
##                                iCounter = 0
##                                cityList = []
##                                apCityList = PyPlayer(iBigIndependent).getCityList()
##                                for pCity in apCityList:
##                                        iDivideCounter += 1 #convert 3 random cities cycling just once
##                                        if (iDivideCounter % 2 == 1):
##                                                city = pCity.GetCy()
##                                                if ( city.getX() != 56 and city.getY() != 27 ):
##                                                        pCurrent = gc.getMap().plot(city.getX(), city.getY())                                        
##                                                        utils.cultureManager((city.getX(),city.getY()), 50, iSmallIndependent, iBigIndependent, False, True, True)
##                                                        utils.flipUnitsInCityBefore((city.getX(),city.getY()), iSmallIndependent, iBigIndependent)                            
##                                                        self.setTempFlippingCity((city.getX(),city.getY()))
##                                                        utils.flipCity((city.getX(),city.getY()), 0, 0, iSmallIndependent, [iBigIndependent])   #by trade because by conquest may raze the city
##                                                        utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iSmallIndependent)
##                                                        iCounter += 1
##                                                        if (iCounter == 3):
##                                                                return



        def fragmentBarbarians(self, iGameTurn):

                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
                for j in range(iRndnum, iRndnum + iNumPlayers):
                        iDeadCiv = j % iNumPlayers                                                        
                        if (not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > con.tBirth[iDeadCiv] + 50):
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
                                                                        #        iNewCiv = iIndependent
                                                                        #elif (iDivideCounter % 4 == 1):
                                                                        #        iNewCiv = iIndependent2
                                                                        iNewCiv = con.iIndepStart + gc.getGame().getSorenRandNum(con.iIndepEnd - con.iIndepStart + 1, 'randomIndep')
                                                                        if (iDivideCounter % 4 == 0 or iDivideCounter % 4 == 1):
                                                                                utils.cultureManager((city.getX(),city.getY()), 50, iNewCiv, iBarbarian, False, True, True)
                                                                                utils.flipUnitsInCityBefore((city.getX(),city.getY()), iNewCiv, iBarbarian)                            
                                                                                self.setTempFlippingCity((city.getX(),city.getY()))
                                                                                utils.flipCity((city.getX(),city.getY()), 0, 0, iNewCiv, [iBarbarian])   #by trade because by conquest may raze the city
                                                                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
                                                                                iDivideCounter += 1
                                        return






##        def collapseCapitals(self, iOldOwner, city, iNewOwner):
##        #Persian UP inside
##        #AI tweaked in CvCity::getCulturePercentAnger()
##        
##                bCapital = False
##                bPersia = False
##                iModifier = 0
##                for i in range(iNumPlayers):
##                        if (city.getX() == tCapitals[i][0] and city.getY() == tCapitals[i][1]):
##                                if (city.getOwner() == i): #otherwise it's no longer a capital
##                                        bCapital = True                                
##                if (iNewOwner == iPersia):
##                        bPersia = True
##                        if (not bCapital):
##                                iModifier = 1
##                if (iNewOwner == self.getRebelCiv() and gc.getGame().getGameTurn() == self.getLatestRebellionTurn(self.getRebelCiv())):
##                        return #don't mess up with resurrection()
##                #print ("iNewOwner", iNewOwner, con.tBirth[iNewOwner])
##                if (iNewOwner == iBarbarian):
##                        return
##                if (iNewOwner != iBarbarian):
##                        if (gc.getGame().getGameTurn() <= con.tBirth[iNewOwner] + 2):
##                                return #don't mess up with birth (case of delay still a problem...)
##                if (bCapital or bPersia):
##                        for x in range(city.getX() -3 +iModifier, city.getX() +4 -iModifier):
##                                for y in range(city.getY() -3 +iModifier, city.getY() +4 -iModifier):
##                                        pCurrent = gc.getMap().plot( x, y )
##                                        if ( pCurrent.isCity()):
##                                                cityNear = pCurrent.getPlotCity()
##                                                iOwnerNear = cityNear.getOwner()
##                                                #print ("iOwnerNear", iOwnerNear, "citynear", cityNear.getName())
##                                                if (iOwnerNear != iNewOwner and iOwnerNear == iOldOwner):
##                                                        if (cityNear != city):
##                                                                if (cityNear.getPopulation() <= city.getPopulation() and not cityNear.isCapital()):
##                                                                        if (bPersia == True and iModifier == 1): #Persian UP - any city, 2x2 area
##                                                                                if (cityNear.getPopulation() <= 8):
##                                                                                        if (self.getLatestFlipTurn() != gc.getGame().getGameTurn()):                                                                               
##                                                                                                utils.flipUnitsInCityBefore((x,y), iNewOwner, iOwnerNear)
##                                                                                                self.setTempFlippingCity((x,y))
##                                                                                                utils.flipCity((x,y), 0, 0, iNewOwner, [iOwnerNear])
##                                                                                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewOwner)
##                                                                                                self.setLatestFlipTurn(gc.getGame().getGameTurn())
##                                                                                                utils.cultureManager(self.getTempFlippingCity(), 50, iOwnerNear, iNewOwner, False, False, False)
##                                                                        else:   
##                                                                                utils.flipUnitsInCityBefore((x,y), iNewOwner, iOwnerNear)
##                                                                                self.setTempFlippingCity((x,y))
##                                                                                utils.flipCity((x,y), 0, 0, iNewOwner, [iOwnerNear])
##                                                                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewOwner)
##                                                                                utils.cultureManager(self.getTempFlippingCity(), 50, iOwnerNear, iNewOwner, False, False, False)
##                                                                                print ("COLLAPSE: CAPITALS", gc.getPlayer(iOwnerNear).getCivilizationShortDescription(0))
                                                                                     

                            

        def collapseByBarbs(self, iGameTurn):
                for iCiv in range(iNumPlayers):
                        if (gc.getPlayer(iCiv).isHuman() == 0 and gc.getPlayer(iCiv).isAlive()):
                                # 3MiroUP: Emperor
                                if (iGameTurn >= con.tBirth[iCiv] + 25 and not utils.collapseImmune(iCiv)):
                                        iNumCities = gc.getPlayer(iCiv).getNumCities()
                                        iLostCities = gc.countCitiesLostTo( iCiv, iBarbarian )
##                                        iLostCities = 0
##                                        for x in range(0, con.iMapMaxX):
##                                                for y in range(0, con.iMapMaxY):
##                                                        if (gc.getMap().plot( x,y ).isCity()):
##                                                                city = gc.getMap().plot( x,y ).getPlotCity()
##                                                                if (city.getOwner() == iBarbarian):
##                                                                        if (city.getOriginalOwner() == iCiv):
##                                                                                iLostCities = iLostCities + 1                                                
                                        if (iLostCities*2 > iNumCities and iNumCities > 0): #if more than one third is captured, the civ collapses
                                                print ("COLLAPSE BY BARBS", gc.getPlayer(iCiv).getCivilizationAdjective(0))
                                                #utils.killAndFragmentCiv(iCiv, iIndependent, iIndependent2, -1, False)
                                                utils.killAndFragmentCiv(iCiv, False, False)

        def collapseGeneric(self, iGameTurn):
                #lNumCitiesNew = con.l0Array
                lNumCitiesNew = con.l0ArrayTotal #for late start
                for iCiv in range(iNumTotalPlayers):
                        if (iCiv < iNumActivePlayers ): #late start condition
                                pCiv = gc.getPlayer(iCiv)
                                teamCiv = gc.getTeam(pCiv.getTeam())
                                if (pCiv.isAlive()):
                                        # 3MiroUP: Emperor
                                        if (iGameTurn >= con.tBirth[iCiv] + 25 and not utils.collapseImmune(iCiv)):
                                                lNumCitiesNew[iCiv] = pCiv.getNumCities()
                                                if (lNumCitiesNew[iCiv]*2 <= self.getNumCities(iCiv)): #if number of cities is less than half than some turns ago, the civ collapses
                                                        print ("COLLAPSE GENERIC", pCiv.getCivilizationAdjective(0), lNumCitiesNew[iCiv]*2, "<=", self.getNumCities(iCiv))
                                                        if (gc.getPlayer(iCiv).isHuman() == 0):
                                                                bVassal = False
                                                                for iMaster in range(con.iNumPlayers):
                                                                        if (teamCiv.isVassal(iMaster)):
                                                                                bVassal = True
                                                                                break
                                                                if (not bVassal):
                                                                        #utils.killAndFragmentCiv(iCiv, iIndependent, iIndependent2, -1, False)
                                                                        utils.killAndFragmentCiv(iCiv, False, False)
                                                else:
                                                        self.setNumCities(iCiv, lNumCitiesNew[iCiv])

        def collapseMotherland(self, iGameTurn):
                #collapses if completely out of broader areas
                for iCiv in range(iNumPlayers):
                        pCiv = gc.getPlayer(iCiv)
                        teamCiv = gc.getTeam(pCiv.getTeam())
                        if (pCiv.isHuman() == 0 and pCiv.isAlive()):
                                # 3MiroUP: Emperor
                                if (iGameTurn >= con.tBirth[iCiv] + 25 and not utils.collapseImmune(iCiv)):
                                        if ( not gc.safeMotherland( iCiv ) ):
                                                print ("COLLAPSE: MOTHERLAND", gc.getPlayer(iCiv).getCivilizationAdjective(0))
                                                #utils.killAndFragmentCiv(iCiv, iIndependent, iIndependent2, -1, False)
                                                utils.killAndFragmentCiv(iCiv, False, False)
##                                        bSafe = False
##                                        #print(" civilization to test: ",iCiv,tCoreAreasTL[iCiv][0],tCoreAreasBR[iCiv][0],tCoreAreasTL[iCiv][1],tCoreAreasBR[iCiv][1])
##                                        for x in range(tCoreAreasTL[iCiv][0], tCoreAreasBR[iCiv][0]+1):
##                                                for y in range(tCoreAreasTL[iCiv][1], tCoreAreasBR[iCiv][1]+1):
##                                                        pCurrent = gc.getMap().plot( x, y )
##                                                        #print(" coords: ",x,y)
##                                                        if ( pCurrent.isCity()):
##                                                                #print(" city ")
##                                                                #print (pCurrent.getPlotCity().getOwner(), pCurrent.getPlotCity().getName(), pCurrent.getPlotCity().getX(), pCurrent.getPlotCity().getY())
##                                                                if (pCurrent.getPlotCity().getOwner() == iCiv):
##                                                                        #print ("iCiv", iCiv, "bSafe", bSafe)
##                                                                        bSafe = True
##                                                                        break
##                                                                        break
##                                        if (bSafe == False):
##                                                iCitiesOwned = 0
##                                                iCitiesLost = 0
##                                                for x in range(tNormalAreasTL[iCiv][0], tNormalAreasBR[iCiv][0]+1):
##                                                        for y in range(tNormalAreasTL[iCiv][1], tNormalAreasBR[iCiv][1]+1):
##                                                                pCurrent = gc.getMap().plot( x, y )
##                                                                if ( pCurrent.isCity()):
##                                                                        #print (pCurrent.getPlotCity().getOwner(), pCurrent.getPlotCity().getName(), pCurrent.getPlotCity().getX(), pCurrent.getPlotCity().getY())
##                                                                        if (pCurrent.getPlotCity().getOwner() == iCiv):
##                                                                                iCitiesOwned += 1
##                                                                        else:
##                                                                                iCitiesLost += 1
##                                                if (iCitiesOwned > iCitiesLost):
##                                                        bSafe = True
##                                        #print ("iCiv", iCiv, "bSafe", bSafe)
##                                        if (bSafe == False):
##                                                bVassal = False
##                                                for iMaster in range(con.iNumPlayers):
##                                                        if (teamCiv.isVassal(iMaster)):
##                                                                bVassal = True
##                                                                break
##                                                if (not bVassal):
##                                                        print ("COLLAPSE: MOTHERLAND", gc.getPlayer(iCiv).getCivilizationAdjective(0))
##                                                        utils.killAndFragmentCiv(iCiv, iIndependent, iIndependent2, -1, False)
##                                                return
                        


        def collapseHuman(self, iOldOwner, city, iNewOwner):
                # 3Miro: not sure what it does
                bEnabled = False
                bCapital = False
                bGeneric = False
                
                # 3Miro: no code of laws
                #if (gc.getTeam(gc.getPlayer(iNewOwner).getTeam()).isHasTech(con.iCodeOfLaws)):
                bEnabled = True
                                    
                iHuman = utils.getHumanID()
                if (city.getX() == tCapitals[iHuman][0] and city.getY() == tCapitals[iHuman][1]):
                        bCapital = True

                print ("bEnabled:", bEnabled, "bCapital:", bCapital, "bGeneric:", bGeneric)

                #debug
                #iNumCitiesNew = gc.getPlayer(iHuman).getNumCities()
                #if (iNumCitiesNew*2 <= self.getNumCities(iHuman)):
                #        print ("HumanCollapseGeneric", iNumCitiesNew*2, "<=", self.getNumCities(iHuman))
                #        bGeneric = True

                #debug
                #bEnabled = True
                #bCapital = True
                
                if ((bCapital or bGeneric) and bEnabled):
                        self.exile(iNewOwner)


        def exile(self, iWinner):
                # 3Miro: not sure what it does
                iHuman = utils.getHumanID()
                pWinner = gc.getPlayer(iWinner)
                teamWinner = gc.getTeam(pWinner.getTeam())
                iDestination = -1
                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'start index')
                for i in range( iRndnum, iNumPlayers + iRndnum ):
                        iCiv = i % iNumPlayers
                        if (gc.getPlayer(iCiv).isAlive() and iCiv != iWinner):
                                if (pWinner.canContact(iCiv)):
                                        if (not teamWinner.isAtWar(iCiv)):
                                                if (gc.getGame().getPlayerRank(iCiv) > gc.getGame().getPlayerRank(iHuman) + 1):
                                                        iDestination = iCiv
                                                        break                                          

                print (iDestination)
                popup = Popup.PyPopup()
                popup.setHeaderString(CyTranslator().getText("TXT_KEY_EXILE_TITLE", ()))          
                popup.setBodyString( CyTranslator().getText("TXT_KEY_EXILE_TEXT", (gc.getPlayer(iWinner).getCivilizationAdjectiveKey(), gc.getPlayer(iDestination).getCivilizationShortDescription(0))))
                popup.launch()
                self.setExileData(0, tCapitals[iHuman][0])
                self.setExileData(1, tCapitals[iHuman][1])
                self.setExileData(2, gc.getGame().getGameTurn())
                self.setExileData(3, iHuman)
                self.setExileData(4, iWinner)

                for iMaster in range(con.iNumPlayers):
                        if (gc.getTeam(gc.getPlayer(iDestination).getTeam()).isVassal(iMaster)):
                                gc.getTeam(gc.getPlayer(iDestination).getTeam()).setVassal(iMaster, False, False)
                
                iTempHumanLeader = gc.getPlayer(iHuman).getLeader()
                iTempDestinationLeader = gc.getPlayer(iDestination).getLeader()
                gc.getPlayer(iDestination).setLeader(iTempHumanLeader)
                gc.getGame().setActivePlayer(iDestination, False)
                gc.getPlayer(iHuman).setLeader(iTempDestinationLeader)
                teamWinner.makePeace(iHuman) #now managed by AI
                iTempLeader = gc.getPlayer(iHuman)

                

        def escape(self, city):
                # 3Miro: not sure what it does
                if (gc.getGame().getGameTurn() <= self.getExileData(2) + iEscapePeriod):
                        iOldHuman = self.getExileData(3)
                        if (gc.getPlayer(iOldHuman).isAlive()):
                                iHuman = utils.getHumanID()
                                utils.flipCity((city.getX(),city.getY()), 0, 0, iOldHuman, [iHuman])
                                popup = Popup.PyPopup()
                                popup.setHeaderString(CyTranslator().getText("TXT_KEY_ESCAPE_TITLE", ()))          
                                popup.setBodyString( CyTranslator().getText("TXT_KEY_ESCAPE_TEXT", (gc.getPlayer(iOldHuman).getCivilizationAdjectiveKey(),)))
                                popup.launch()

                                for iMaster in range(con.iNumPlayers):
                                        if (gc.getTeam(gc.getPlayer(iOldHuman).getTeam()).isVassal(iMaster)):
                                                gc.getTeam(gc.getPlayer(iOldHuman).getTeam()).setVassal(iMaster, False, False)
                                
                                iTempHumanLeader = gc.getPlayer(iHuman).getLeader()
                                iTempOldHumanLeader = gc.getPlayer(iOldHuman).getLeader()
                                gc.getPlayer(iOldHuman).setLeader(iTempHumanLeader)
                                gc.getGame().setActivePlayer(iOldHuman, False)
                                gc.getPlayer(iHuman).setLeader(iTempOldHumanLeader)
                                city.setHasRealBuilding((0), True) #0 == palace
                                teamWinner = gc.getTeam(gc.getPlayer(self.getExileData(4)).getTeam())
                                teamWinner.declareWar(iOldHuman, True, -1)
                                teamWinner.makePeace(iHuman) #now managed by AI
                                self.setExileData(0, -1)
                                self.setExileData(1, -1)
                                self.setExileData(2, -1)
                                self.setExileData(3, -1)
                                self.setExileData(4, -1)

                

        def secession(self, iGameTurn):
            
                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
                for j in range(iRndnum, iRndnum + iNumPlayers):
                        iPlayer = j % iNumPlayers
                        #print(" 3Miro: player ",iPlayer)
                        if (gc.getPlayer(iPlayer).isAlive() and iGameTurn >= con.tBirth[iPlayer] + 30):
                                #if (utils.getStability(iPlayer) >= -40 and utils.getStability(iPlayer) < -20): #secession
                                if (utils.getStability(iPlayer) < -20): #secession, 3Miro: do regarless of how low stability is

                                        #print("3Miro: unstable")
                                        cityList = []
                                        apCityList = PyPlayer(iPlayer).getCityList()
                                        for pCity in apCityList:
                                                city = pCity.GetCy()
                                                pCurrent = gc.getMap().plot(city.getX(), city.getY())

                                                if ((not city.isWeLoveTheKingDay()) and (not city.isCapital()) and (not (city.getX() == tCapitals[iPlayer][0] and city.getY() == tCapitals[iPlayer][1])) and (not utils.collapseImmuneCity(iPlayer,city.getX(),city.getY()))):
                                                        # 3MiroUP: Emperor
                                                        if (gc.getPlayer(iPlayer).getNumCities() > 0): #this check is needed, otherwise game crashes
                                                                capital = gc.getPlayer(iPlayer).getCapitalCity()
                                                                iDistance = utils.calculateDistance(city.getX(), city.getY(), capital.getX(), capital.getY())
                                                                if (iDistance > 3):                                                                                               
                                                            
                                                                        if (city.angryPopulation(0) > 0 or \
                                                                            city.healthRate(False, 0) < 0 or \
                                                                            city.getReligionBadHappiness() > 0 or \
                                                                            city.getLargestCityHappiness() < 0 or \
                                                                            city.getHurryAngerModifier() > 0 or \
                                                                            city.getNoMilitaryPercentAnger() > 0 or \
                                                                            city.getWarWearinessPercentAnger() > 0):
                                                                                cityList.append(city)
                                                                                continue
                                                                        
                                                                        for iLoop in range(iNumTotalPlayers+1):
                                                                                if (iLoop != iPlayer):
                                                                                        if (pCurrent.getCulture(iLoop) > 0):
                                                                                                cityList.append(city)
                                                                                                break

                                        if (len(cityList)):
                                                #iNewCiv = iIndependent
                                                #iRndNum = gc.getGame().getSorenRandNum(2, 'random independent')
                                                #if (iRndNum % 2 == 0):
                                                #        iNewCiv = iIndependent2                        
                                                iRndNum = gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random independent')
                                                iNewCiv = con.iIndepStart + iRndNum
                                                
                                                splittingCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')]
                                                utils.cultureManager((splittingCity.getX(),splittingCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
                                                utils.flipUnitsInCityBefore((splittingCity.getX(),splittingCity.getY()), iNewCiv, iPlayer)                            
                                                self.setTempFlippingCity((splittingCity.getX(),splittingCity.getY()))
                                                utils.flipCity((splittingCity.getX(),splittingCity.getY()), 0, 0, iNewCiv, [iPlayer])   #by trade because by conquest may raze the city
                                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
                                                if (iPlayer == utils.getHumanID()):
                                                        CyInterface().addMessage(iPlayer, True, con.iDuration, splittingCity.getName() + " " + \
                                                                                           CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                                                #print ("SECESSION", gc.getPlayer(iPlayer).getCivilizationAdjective(0), splittingCity.getName()) #causes c++ exception??
                                                utils.setParameter(iPlayer, con.iParExpansionE, True, 2) #to counterbalance the stability hit on city acquired event, leading to a chain reaction
                                                
                                                utils.setStability(iPlayer, utils.getStability(iPlayer) + 2) #to counterbalance the stability hit on city acquired event, leading to a chain reaction

                                        return #just 1 secession per turn


                              
        def resurrection(self, iGameTurn):
        
                iDeadCiv = self.findCivToResurect( iGameTurn )
                #print ("iDeadCiv", iDeadCiv)
                if ( iDeadCiv > -1 ):
                        self.suppressResurection( iDeadCiv )
                        #self.resurectCiv( iDeadCiv )
                                
        def findCivToResurect( self, iGameTurn ):
                iMinNumCities = 2
        
                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
                cityList = []
                for j in range(iRndnum, iRndnum + iNumPlayers):
                        iDeadCiv = j % iNumPlayers
                        cityList = []
                        if (not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > con.tBirth[iDeadCiv] + 50 and iGameTurn > utils.getLastTurnAlive(iDeadCiv) + 30):
                                pDeadCiv = gc.getPlayer(iDeadCiv)
                                teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
                                #3Miro: inRFC Civs spawn according to Normal Areas, but here we want Core areas. Otherwise Normal Areas should not overlap and that is Hard.
                                #Sedna17: Normal Areas no longer overlap, so we can respawn here.
                                tTopLeft = tNormalAreasTL[iDeadCiv]
                                tBottomRight = tNormalAreasBR[iDeadCiv]
                                #tTopLeft = tCoreAreasTL[iDeadCiv]
                                #tBottomRight = tCoreAreasBR[iDeadCiv]
                                
                                for x in range(tTopLeft[0], tBottomRight[0]+1):
                                        for y in range(tTopLeft[1], tBottomRight[1]+1):
                                                if ((x,y) not in con.tNormalAreasSubtract[iDeadCiv]):
                                                #if ((x,y) not in con.tExceptions[iDeadCiv]):
                                                        pCurrent = gc.getMap().plot( x, y )
                                                        if ( pCurrent.isCity()):
                                                                city = pCurrent.getPlotCity()
                                                                iOwner = city.getOwner()
                                                                if (iOwner >= iNumActivePlayers): #if (iOwner == iBarbarian or iOwner == iIndependent or iOwner == iIndependent2): #remove in vanilla
                                                                        cityList.append(pCurrent.getPlotCity())
                                                                        #print (iDeadCiv, pCurrent.getPlotCity().getName(), pCurrent.getPlotCity().getOwner(), "1", cityList)
                                                                else:
                                                                        iMinNumCitiesOwner = 3
                                                                        iOwnerStability = utils.getStability(iOwner)
                                                                        if (not gc.getPlayer(iOwner).isHuman()):
                                                                                iMinNumCitiesOwner = 2
                                                                                iOwnerStability -= 20
                                                                        if (gc.getPlayer(iOwner).getNumCities() >= iMinNumCitiesOwner):
                                                                                if (iOwnerStability < -20):
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
                                                                                                                city.getNoMilitaryPercentAnger() > 0 or \
                                                                                                                city.getWarWearinessPercentAnger() > 0):
                                                                                                                        cityList.append(pCurrent.getPlotCity())
                                                                                                                        #print (iDeadCiv, pCurrent.getPlotCity().getName(), pCurrent.getPlotCity().getOwner(), "3", cityList)
                                                                                if (iOwnerStability < 20):
                                                                                                if (city.getX() == tCapitals[iDeadCiv][0] and city.getY() == tCapitals[iDeadCiv][1]):
                                                                                                        if (pCurrent.getPlotCity() not in cityList):
                                                                                                                cityList.append(pCurrent.getPlotCity())
                                if (len(cityList) >= iMinNumCities ):
                                        if (gc.getGame().getSorenRandNum(100, 'roll') < con.tResurrectionProb[iDeadCiv]):
                                                lCityList = []
                                                for iCity in range( len(cityList)  ):
                                                        lCityList.append( (cityList[iCity].getX(), cityList[iCity].getY()) )
                                                self.setRebelCities( lCityList )
                                                self.setRebelCiv(iDeadCiv) #for popup and CollapseCapitals()
                                                return iDeadCiv
                return -1
                
        def suppressResurection( self, iDeadCiv ):
                lSuppressList = self.getRebelSuppress()
                lCityList = self.getRebelCities()
                lCityCount = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
                
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
        
                if (len(tLeaders[iDeadCiv]) > 1):
                        iLen = len(tLeaders[iDeadCiv])
                        iRnd = gc.getGame().getSorenRandNum(iLen, 'odds')
                        for k in range (iLen):
                                iLeader = (iRnd + k) % iLen
                                if (pDeadCiv.getLeader() != tLeaders[iDeadCiv][iLeader]):
                                        print ("leader switch after resurrection", pDeadCiv.getLeader(), tLeaders[iDeadCiv][iLeader])
                                        pDeadCiv.setLeader(tLeaders[iDeadCiv][iLeader])
                                        break                                                        
                                
                for l in range(iNumPlayers):
                        teamDeadCiv.makePeace(l)
                self.setNumCities(iDeadCiv, 0) #reset collapse condition

                #reset vassallage
                for iOtherCiv in range(iNumPlayers):
                        if (teamDeadCiv.isVassal(iOtherCiv) or gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).isVassal(iDeadCiv)):
                                teamDeadCiv.freeVassal(iOtherCiv)
                                gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).freeVassal(iDeadCiv)
                                                
                iNewUnits = 2
                if (self.getLatestRebellionTurn(iDeadCiv) > 0):
                        iNewUnits = 4
                self.setLatestRebellionTurn(iDeadCiv, iGameTurn)
                bHuman = False
                
                print ("RESURRECTION", gc.getPlayer(iDeadCiv).getCivilizationAdjective(0))
                       
                
                for k0 in range(len(lCityList)):
                        if ( gc.getMap().plot( lCityList[k0][0], lCityList[k0][0] ).getPlotCity().getOwner() == iHuman ):
                                bHuman = True

                ownersList = []        
                bAlreadyVassal = False
                for k in range(len(lCityList)):
                        #print ("INDEPENDENCE: ", cityList[k].getName()) #may cause a c++ exception                                       
                        pCity = gc.getMap().plot( lCityList[k], lCityList[k] ).getPlotCity()
                        iOwner = pCity.getOwner()
                        teamOwner = gc.getTeam(gc.getPlayer(iOwner).getTeam())
                        bOwnerVassal = teamOwner.isAVassal()
                        bOwnerHumanVassal = teamOwner.isVassal(iHuman)

                        #if (iOwner == iBarbarian or iOwner == iIndependent or iOwner == iIndependent2 ):
                        if (iOwner == iBarbarian or utils.isIndep( iOwner )  ):
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
                                        utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iDeadCiv, [iOwner])   #by trade because by conquest may raze the city
                                        utils.createGarrisons(self.getTempFlippingCity(), iDeadCiv, iNewUnits)
                                
                        #cityList[k].setHasRealBuilding(con.iPlague, False)
                        
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
                                                                gc.getTeam(gc.getPlayer(iDeadCiv).getTeam()).setVassal(iOwner, True, False)  #remove in vanilla
                                                                bAlreadyVassal = True
                                        else:
                                                teamOwner.makePeace(iDeadCiv)
                                        ownersList.append(iOwner)
                                        for t in range(con.iNumTechs):
                                                if (teamOwner.isHasTech(t)): 
                                                        teamDeadCiv.setHasTech(t, True, iDeadCiv, False, False)

                for t in range(con.iNumTechs):
                        if (teamBarbarian.isHasTech(t) or teamIndependent.isHasTech(t) or teamIndependent2.isHasTech(t)): #remove indep in vanilla
                                teamDeadCiv.setHasTech(t, True, iDeadCiv, False, False)

                self.moveBackCapital(iDeadCiv)

                #add former colonies that are still free
                colonyList = []
                for iIndCiv in range(iNumTotalPlayers+1): #barbarians too
                        if (iIndCiv >= iNumActivePlayers):
                                if (gc.getPlayer(iIndCiv).isAlive()):
                                        apCityList = PyPlayer(iIndCiv).getCityList()
                                        for pCity in apCityList:
                                                indepCity = pCity.GetCy()                                                                
                                                if (indepCity.getOriginalOwner() == iDeadCiv):
                                                        print ("colony:", indepCity.getName(), indepCity.getOriginalOwner())
                                                        indX = indepCity.getX()
                                                        indY = indepCity.getY()
                                                        if (gc.getPlayer(iDeadCiv).getSettlersMaps( con.iMapMaxY-indY-1, indX ) >= 90):
                                                                if (indepCity not in cityList and indepCity not in colonyList):
                                                                        colonyList.append(indepCity)
                if (len(colonyList) > 0):
                        for k in range(len(colonyList)):
                                print ("INDEPENDENCE: ", colonyList[k].getName())   
                                iOwner = colonyList[k].getOwner()
                                utils.cultureManager((colonyList[k].getX(),colonyList[k].getY()), 100, iDeadCiv, iOwner, False, True, True)
                                utils.flipUnitsInCityBefore((colonyList[k].getX(),colonyList[k].getY()), iDeadCiv, iOwner)
                                self.setTempFlippingCity((colonyList[k].getX(),colonyList[k].getY()))
                                utils.flipCity((colonyList[k].getX(),colonyList[k].getY()), 0, 0, iDeadCiv, [iOwner])
                                tCoords = self.getTempFlippingCity()
                                utils.flipUnitsInCityAfter(tCoords, iOwner)
                                utils.flipUnitsInArea((tCoords[0]-2, tCoords[1]-2), (tCoords[0]+2, tCoords[1]+2), iDeadCiv, iOwner, True, False)
                                
                CyInterface().addMessage(iHuman, True, con.iDuration, \
                                        (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pDeadCiv.getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
                #if (bHuman == True):                                        
                #        self.rebellionPopup(iDeadCiv)
                if ( lSuppressList[iHuman] == 2 or lSuppressList[iHuman] == 3 or lSuppressList[iHuman] == 4 ):
                        gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iDeadCiv, False, -1)
                else:
                        gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iDeadCiv)
                utils.setBaseStabilityLastTurn(iDeadCiv, 0)
                utils.zeroStability(iDeadCiv)
                utils.setParameter(iDeadCiv,con.iParExpansionE,False,10)
                utils.setStability(iDeadCiv, 10) ##the new civs start as slightly stable
                utils.setPlagueCountdown(iDeadCiv, -10)
                utils.clearPlague(iDeadCiv)                                
                self.convertBackCulture(iDeadCiv)
                return

        def moveBackCapital(self, iCiv):
                apCityList = PyPlayer(iCiv).getCityList()
                if (gc.getMap().plot(tCapitals[iCiv][0], tCapitals[iCiv][1]).isCity()):
                        oldCapital = gc.getMap().plot(tCapitals[iCiv][0], tCapitals[iCiv][1]).getPlotCity()
                        if (oldCapital.getOwner() == iCiv):
                                if (not oldCapital.hasBuilding(con.iPalace)):                                        
                                        for pCity in apCityList:
                                                pCity.GetCy().setHasRealBuilding((con.iPalace), False)
                                        oldCapital.setHasRealBuilding((con.iPalace), True)
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
                                                loopCity.setHasRealBuilding((con.iPalace), False)
                                bestCity.setHasRealBuilding((con.iPalace), True)
                                                
                                                

        def convertBackCulture(self, iCiv):
                #3Miro: same as Normal Ares in Resurection
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
                                        for ix in range(pCurrent.getX()-1, pCurrent.getX()+2):        # from x-1 to x+1
                                                for iy in range(pCurrent.getY()-1, pCurrent.getY()+2):        # from y-1 to y+1
                                                        pCityArea = gc.getMap().plot( ix, iy )
                                                        iCivCulture = pCityArea.getCulture(iCiv)
                                                        iLoopCivCulture = 0
                                                        for iLoopCiv in range(con.iNumTotalPlayers+1): #barbarians too
                                                                if (iLoopCiv >= iNumPlayers):
                                                                        iLoopCivCulture += pCityArea.getCulture(iLoopCiv)      
                                                                        pCityArea.setCulture(iLoopCiv, 0, True)
                                                        pCityArea.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

                                        city = pCurrent.getPlotCity()
                                        iCivCulture = city.getCulture(iCiv)
                                        iLoopCivCulture = 0
                                        for iLoopCiv in range(con.iNumTotalPlayers+1): #barbarians too
                                                if (iLoopCiv >= iNumPlayers):
                                                        iLoopCivCulture += city.getCulture(iLoopCiv)                                
                                                        city.setCulture(iLoopCiv, 0, True)
                                        city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True) 

                            
                                    
        def initBirth(self, iCurrentTurn, iBirthYear, iCiv):
                iHuman = utils.getHumanID()
                if (iCurrentTurn == iBirthYear-1 + self.getSpawnDelay(iCiv) + self.getFlipsDelay(iCiv)):
                        tCapital = tCapitals[iCiv]
                        tTopLeft = tCoreAreasTL[iCiv]
                        tBottomRight = tCoreAreasBR[iCiv]
                        tBroaderTopLeft = tBroaderAreasTL[iCiv]
                        tBroaderBottomRight = tBroaderAreasBR[iCiv]                    
                        if (self.getFlipsDelay(iCiv) == 0): #city hasn't already been founded)
                                bDeleteEverything = False
                                if (gc.getMap().plot(tCapital[0], tCapital[1]).isOwned()):
                                        if (iCiv == iHuman or not gc.getPlayer(iHuman).isAlive()):
                                                bDeleteEverything = True
                                                print ("bDeleteEverything 1")
                                        else:
                                                bDeleteEverything = True
                                                for x in range(tCapital[0] - 1, tCapital[0] + 2):        # from x-1 to x+1
                                                        for y in range(tCapital[1] - 1, tCapital[1] + 2):        # from y-1 to y+1
                                                                pCurrent=gc.getMap().plot(x, y)
                                                                if (pCurrent.isCity() and pCurrent.getPlotCity().getOwner() == iHuman):
                                                                        bDeleteEverything = False
                                                                        print ("bDeleteEverything 2")
                                                                        break
                                                                        break
                                print ("bDeleteEverything", bDeleteEverything)
                                if (not gc.getMap().plot(tCapital[0], tCapital[1]).isOwned()):
                                        #if (iCiv == iNetherlands or iCiv == iPortugal): #dangerous starts
                                        #        self.setDeleteMode(0, iCiv)
                                        self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
                                elif (bDeleteEverything):
                                        for x in range(tCapital[0] - 1, tCapital[0] + 2):        # from x-1 to x+1
                                                for y in range(tCapital[1] - 1, tCapital[1] + 2):        # from y-1 to y+1
                                                        self.setDeleteMode(0, iCiv)
                                                        #print ("deleting", x, y)
                                                        pCurrent=gc.getMap().plot(x, y)
                                                        #self.moveOutUnits(x, y, tCapital[0], tCapital[1])
                                                        for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
                                                                if (iCiv != iLoopCiv):
                                                                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iLoopCiv, True, False)
                                                        if (pCurrent.isCity()):
                                                                pCurrent.eraseAIDevelopment() #new function, similar to erase but won't delete rivers, resources and features()
                                                        for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
                                                                if (iCiv != iLoopCiv):
                                                                        pCurrent.setCulture(iLoopCiv, 0, True)
                                                        pCurrent.setOwner(-1)
                                        self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
                                else:                                
                                        self.birthInForeignBorders(iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight)
                        else:
                                print ( "setBirthType again: flips" )
                                self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
                                       
                # 3MiroCrusader modification. Crusaders cannot change nations.
                # Sedna17: Straight-up no switching within 40 turns of your birth
                if (iCurrentTurn == iBirthYear + self.getSpawnDelay(iCiv)) and (gc.getPlayer(iCiv).isAlive()) and (self.getAlreadySwitched() == False) and (iCurrentTurn > tBirth[iHuman]+40) and ( not gc.getPlayer( iHuman ).getIsCrusader() ):
                        self.newCivPopup(iCiv)   


##        def moveOutUnits(self, x, y, tCapitalX, tCapitalY) #not used
##                pCurrent=gc.getMap().plot(x, y)
##                if (pCurrent.getNumUnits() > 0):
##                        unit = pCurrent.getUnit(0)
##                        tDestination = (-1, -1)
##                        plotList = []
##                        if (unit.getDomainType() == 2): #land unit
##                                dummy, plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodPlots, [] )
##                                #dummy, plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodOwnedPlots, [] )
##                        else: #sea unit
##                                dummy, plotList = utils.squareSearch( (tCapitalX-3, tCapitalY-3), (tCapitalX+4, tCapitalY+4), utils.goodOwnedPlots, [] )
##                        
##                        rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching another free plot')
##                        if (len(plotList)):
##                                result = plotList[rndNum]
##                                if (result):
##                                        tDestination = result
##                        print ("moving units around to", (tDestination[0], tDestination[1]))
##                        if (tDestination != (-1, -1)):
##                                for i in range(pCurrent.getNumUnits()):                                                                
##                                        unit = pCurrent.getUnit(0)
##                                        unit.setXY(tDestination[0], tDestination[1])

                                
                

        def deleteMode(self, iCurrentPlayer):
                iCiv = self.getDeleteMode(0)
                print ("deleteMode after", iCurrentPlayer)
                tCapital = con.tCapitals[iCiv]
                if (iCurrentPlayer == iCiv):
                        for x in range(tCapital[0] - 2, tCapital[0] + 3):        # from x-2 to x+2
                                for y in range(tCapital[1] - 2, tCapital[1] + 3):        # from y-2 to y+2
                                        pCurrent=gc.getMap().plot(x, y)
                                        pCurrent.setCulture(iCiv, 300, True)
                        for x in range(tCapital[0] - 1, tCapital[0] + 2):        # from x-1 to x+1
                                for y in range(tCapital[1] - 1, tCapital[1] + 2):        # from y-1 to y+1
                                        pCurrent=gc.getMap().plot(x, y)
                                        utils.convertPlotCulture(pCurrent, iCiv, 100, True)
                                        if (pCurrent.getCulture(iCiv) < 3000):
                                                pCurrent.setCulture(iCiv, 3000, True) #2000 in vanilla/warlords, cos here Portugal is choked by spanish culture
                                        pCurrent.setOwner(iCiv)
                        self.setDeleteMode(0, -1)
                        return
                    
                #print ("iCurrentPlayer", iCurrentPlayer, "iCiv", iCiv)
                if (iCurrentPlayer != iCiv-1):
                        return
                
                bNotOwned = True
                for x in range(tCapital[0] - 1, tCapital[0] + 2):        # from x-1 to x+1
                        for y in range(tCapital[1] - 1, tCapital[1] + 2):        # from y-1 to y+1
                                #print ("deleting again", x, y)
                                pCurrent=gc.getMap().plot(x, y)
                                if (pCurrent.isOwned()):
                                        bNotOwned = False
                                        for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
                                                if(iLoopCiv != iCiv):
                                                        pCurrent.setCulture(iLoopCiv, 0, True)
                                                #else:
                                                #        if (pCurrent.getCulture(iCiv) < 4000):
                                                #                pCurrent.setCulture(iCiv, 4000, True)
                                        #pCurrent.setOwner(-1)
                                        pCurrent.setOwner(iCiv)
                
                for x in range(tCapital[0] - 11, tCapital[0] + 12):        # must include the distance from Sogut to the Caspius
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
##                                                        for farX in range(x - 6, x + 7):
##                                                                for farY in range(y - 6, y + 7):
##                                                                        pCurrentFar = gc.getMap().plot(farX, farY)
##                                                                        if (pCurrentFar.getNumUnits() == 0):
##                                                                                pCurrentFar.setRevealed(iCiv, False, True, -1);

                


            
                    
        def birthInFreeRegion(self, iCiv, tCapital, tTopLeft, tBottomRight):
                startingPlot = gc.getMap().plot( tCapital[0], tCapital[1] )
                if (self.getFlipsDelay(iCiv) == 0):
                        iFlipsDelay = self.getFlipsDelay(iCiv) + 2
                        print ("Entering birthInFreeRegion")
##                        if (startingPlot.getNumUnits() > 0):
##                                unit = startingPlot.getUnit(0)
##                                if (unit.getOwner() != utils.getHumanID() or iCiv == utils.getHumanID()): #2nd check needed because in delete mode it finds the civ's (human's) units placed
##                                        for i in range(startingPlot.getNumUnits()):
##                                                unit = startingPlot.getUnit(0)        # 0 instead of i because killing units changes the indices
##                                                unit.kill(False, iCiv)
##                                        iFlipsDelay = self.getFlipsDelay(iCiv) + 2
##                                        #utils.debugTextPopup( 'birthInFreeRegion in starting location' ) 
##                                else:   #search another place
##                                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.goodPlots, [] )
##                                        rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching another free plot')
##                                        if (len(plotList)):
##                                                result = plotList[rndNum]
##                                                if (result):
##                                                        self.createStartingUnits(iCiv, result)
##                                                        tCapital = result
##                                                        print ("birthInFreeRegion in another location")
##                                                        #utils.debugTextPopup( 'birthInFreeRegion in another location' )
##                                                        iFlipsDelay = self.getFlipsDelay(iCiv) + 1 #add delay before flipping other cities
##                                        else: 
##                                                if (self.getSpawnDelay(iCiv) < 10):  #wait
##                                                        iSpawnDelay = self.getSpawnDelay(iCiv) + 1
##                                                        self.setSpawnDelay(iCiv, iSpawnDelay)                                                        
##                        else:
##                                iFlipsDelay = self.getFlipsDelay(iCiv) + 2

                        if (iFlipsDelay > 0):
                                #startingPlot.setImprovementType(-1)
                            
                                #gc.getPlayer(iCiv).found(tCapital[0], tCapital[1])
                                #gc.getMap().plot(tCapital[0], tCapital[1]).setRevealed(iCiv, False, True, -1);
                                #gc.getMap().plot(tCapital[0], tCapital[1]).setRevealed(iCiv, True, True, -1);
                                
                                print ("starting units in", tCapital[0], tCapital[1])
                                self.createStartingUnits(iCiv, (tCapital[0], tCapital[1]))

                                #if (self.getDeleteMode(0) == iCiv):                                                                
                                #        self.createStartingWorkers(iCiv, tCapital) #XXX bugfix? no!
                                                                
##                                settlerPlot = gc.getMap().plot( tCapital[0], tCapital[1] )
##                                for i in range(settlerPlot.getNumUnits()):
##                                        unit = settlerPlot.getUnit(i)
##                                        if (unit.getUnitType() == iSettler):
##                                                break
##                                unit.found()                                
                                utils.flipUnitsInArea((tCapital[0]-2, tCapital[1]-2), (tCapital[0]+2, tCapital[1]+2), iCiv, iBarbarian, True, True) #This is for AI only. During Human player spawn, that area is already cleaned                        
                                for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
                                        utils.flipUnitsInArea((tCapital[0]-2, tCapital[1]-2), (tCapital[0]+2, tCapital[1]+2), iCiv, i, True, False) #This is for AI only. During Human player spawn, that area is already cleaned                        
                                #utils.flipUnitsInArea((tCapital[0]-2, tCapital[1]-2), (tCapital[0]+2, tCapital[1]+2), iCiv, iIndependent, True, False) #This is for AI only. During Human player spawn, that area is already cleaned                        
                                #utils.flipUnitsInArea((tCapital[0]-2, tCapital[1]-2), (tCapital[0]+2, tCapital[1]+2), iCiv, iIndependent2, True, False) #This is for AI only. During Human player spawn, that area is already cleaned                        
                                self.assignTechs(iCiv)
                                utils.setPlagueCountdown(iCiv, -con.iImmunity)
                                utils.clearPlague(iCiv)
                                #gc.getPlayer(iCiv).changeAnarchyTurns(1)
                                #gc.getPlayer(iCiv).setCivics(2, 11)
                                self.setFlipsDelay(iCiv, iFlipsDelay) #save
                                

                else: #starting units have already been placed, now the second part                    
                        iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, tTopLeft, tBottomRight)
                        self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ   
                        for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
                                utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, i, False, False) #remaining independents in the region now belong to the new civ   
                        #utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
                        #utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, False, False) #remaining independents in the region now belong to the new civ   
                        print ("utils.flipUnitsInArea()") 
                        #cover plots revealed by the lion
                        plotZero = gc.getMap().plot( 10, 0 )                        
                        if (plotZero.getNumUnits()):
                                catapult = plotZero.getUnit(0)
                                catapult.kill(False, iCiv)
                        #gc.getMap().plot(0, 0).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(0, 1).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(1, 1).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(1, 0).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(123, 0).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(123, 1).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(2, 0).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(2, 1).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(2, 2).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(1, 2).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(0, 2).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(122, 0).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(122, 1).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(122, 2).setRevealed(iCiv, False, True, -1);
                        #gc.getMap().plot(123, 2).setRevealed(iCiv, False, True, -1);
                        gc.getMap().plot( 9, 0).setRevealed(iCiv, False, True, -1);
                        gc.getMap().plot(10, 0).setRevealed(iCiv, False, True, -1);
                        gc.getMap().plot(11, 0).setRevealed(iCiv, False, True, -1);
                        gc.getMap().plot( 9, 1).setRevealed(iCiv, False, True, -1);
                        gc.getMap().plot(10, 1).setRevealed(iCiv, False, True, -1);
                        gc.getMap().plot(11, 1).setRevealed(iCiv, False, True, -1);
                        print ("Plots covered")

                        if (gc.getPlayer(iCiv).getNumCities() > 0):
                                capital = gc.getPlayer(iCiv).getCapitalCity()
                                self.createStartingWorkers(iCiv, (capital.getX(), capital.getY()))

                        if (iNumHumanCitiesToConvert> 0):
                                self.flipPopup(iCiv, tTopLeft, tBottomRight)

                        
        def birthInForeignBorders(self, iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight):
                
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
                                        utils.setPlagueCountdown(iCiv, -con.iImmunity)
                                        utils.clearPlague(iCiv)
                                        #gc.getPlayer(iCiv).changeAnarchyTurns(1)
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ 
                        for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
                                utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, i, False, False) #remaining barbs in the region now belong to the new civ 
                        #utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, False, False) #remaining barbs in the region now belong to the new civ 
                        #utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, False, False) #remaining barbs in the region now belong to the new civ 
                        
                else:   #search another place
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.goodPlots, [] )
                        rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching another free plot')
                        if (len(plotList)):
                                result = plotList[rndNum]
                                if (result):
                                        self.createStartingUnits(iCiv, result)
                                        #utils.debugTextPopup( 'birthInForeignBorders in another location' )
                                        self.assignTechs(iCiv)
                                        utils.setPlagueCountdown(iCiv, -con.iImmunity)
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
                                                utils.setPlagueCountdown(iCiv, -con.iImmunity)
                                                utils.clearPlague(iCiv)
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ 
                        for i in range( con.iIndepStart, con.iIndepEnd + 1 ):
                                utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, i, True, False) #remaining barbs in the region now belong to the new civ 
                        #utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, True, False) #remaining barbs in the region now belong to the new civ 
                        #utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, True, False) #remaining barbs in the region now belong to the new civ 

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
                                                cityList.append(pCurrent.getPlotCity())

                #Exceptions
                if (len(tExceptions[iCiv])):
                        for j in range(len(tExceptions[iCiv])):
                                pCurrent = gc.getMap().plot( tExceptions[iCiv][j][0], tExceptions[iCiv][j][1] )
                                if ( pCurrent.isCity()):
                                        if (pCurrent.getPlotCity().getOwner() != iCiv):
                                                print ("append", pCurrent)
                                                cityList.append(pCurrent.getPlotCity())

                print ("Birth", iCiv)
                #print (cityList)

                #for each city
                if (len(cityList)):
                        for i in range(len(cityList)):
                                loopCity = cityList[i]
                                loopX = loopCity.getX()
                                loopY = loopCity.getY()
                                print ("cityList", loopCity.getName(), (loopX, loopY))
                                iHuman = utils.getHumanID()
                                iOwner = loopCity.getOwner()
                                iCultureChange = 0 #if 0, no flip; if > 0, flip will occur with the value as variable for utils.CultureManager()
                                
                                #case 1: barbarian/independent city
                                #if (iOwner == iBarbarian or iOwner == iIndependent or iOwner == iIndependent2 ):
                                if (iOwner == iBarbarian or utils.isIndep( iOwner ) ):
                                        #utils.debugTextPopup( 'BARB' )
                                        iCultureChange = 100
                                #case 2: human city
                                elif (iOwner == iHuman and not loopCity.isCapital()):
                                        #utils.debugTextPopup( 'HUMAN' )
        ##                                bForeigners = False
        ##                                cityPlot = gc.getMap().plot(cityList[i].getX(), cityList[i].getY())
        ##                                cityCulture = cityList[i].countTotalCulture()
        ##                                iCultureThreshold = 10
        ##                                for j in range(iNumPlayers+1):
        ##                                        if (cityList[i].getCulture(j)*100 / cityCulture >= iCultureThreshold) and (j != iHuman):
        ##                                                bForeigners = True
        ##                                humanCapital = gc.getPlayer(iHuman).getCapitalCity()
        ##                                iDistance = gc.getMap().calculatePathDistance(cityPlot, gc.getMap().plot(humanCapital.getX(),humanCapital.getY()))
        ##                                if (cityList[i].isOccupation()) or (cityList[i].isDisorder()) or (bForeigners == True) or (not cityPlot.getNumUnits()) or ((not cityList[i].isGovernmentCenter()) and (iDistance >= 8) and (gc.getPlayer(iHuman).getNumCities() >= 5)):
                                        if (iNumHumanCities == 0):
                                                iNumHumanCities += 1
                                                #iConvertedCitiesCount += 1
                                                #self.flipPopup(iCiv, tTopLeft, tBottomRight)
                                #case 3: other
                                elif (not loopCity.isCapital()):   #utils.debugTextPopup( 'OTHER' )                                
                                        if (iConvertedCitiesCount < 6): #there won't be more than 5 flips in the area
                                                #utils.debugTextPopup( 'iConvertedCities OK' )
                                                iCultureChange = 50
                                                if (gc.getGame().getGameTurn() <= con.tBirth[iCiv] + 5): #if we're during a birth
                                                        rndNum = gc.getGame().getSorenRandNum(100, 'odds')
                                                        if (rndNum >= tAIStopBirthThreshold[iOwner]):
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

                                        #iEra = gc.getPlayer(iCiv).getCurrentEra()
                                        #if (iEra >= 2): #medieval
                                        #        if (loopCity.getPopulation() < iEra):
                                        #                loopCity.setPopulation(iEra) #causes an unidentifiable C++ exception
                                                #doesn't work (assigns UBs too)
                                                #for iLoopBuilding in range(con.iNumBuildingsPlague):                                                        
                                                #        if (gc.getBuildingInfo(iLoopBuilding).getFreeStartEra() >= 0):
                                                #                if (iEra >= gc.getBuildingInfo(iLoopBuilding).getFreeStartEra()):
                                                #                        print (iEra, iLoopBuilding, gc.getBuildingInfo(iLoopBuilding).getFreeStartEra(), loopCity.canConstruct(iLoopBuilding, False, False, False))
                                                #                        if (loopCity.canConstruct(iLoopBuilding, False, False, False)):
                                                #                                if (not loopCity.hasBuilding(iLoopBuilding)):
                                                #                                        loopCity.setHasRealBuilding(iLoopBuilding, True)

                                        #cityList[i].setHasRealBuilding(con.iPlague, False)   #buggy
                                        
                                        iConvertedCitiesCount += 1
                                        print ("iConvertedCitiesCount", iConvertedCitiesCount)

                if (iConvertedCitiesCount > 0):
                        if (gc.getPlayer(iCiv).isHuman()):
                                CyInterface().addMessage(iCiv, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_TO_US", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)

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
                """Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
                seaPlotList = []
                for x in range(tCoords[0] - iRange, tCoords[0] + iRange+1):        
                        for y in range(tCoords[1] - iRange, tCoords[1] + iRange+1):        
                                pCurrent = gc.getMap().plot( x, y )
                                if ( pCurrent.isWater()):
                                        if ( not pCurrent.isUnit() ):
                                                if (pCurrent.countTotalCulture() == 0 ):
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
                        CyInterface().addMessage(self.getOldCivFlip(), False, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
                elif (gc.getPlayer(self.getNewCivFlip()).isHuman()):
                        CyInterface().addMessage(self.getNewCivFlip(), False, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL_NEW", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
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
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 3)
                if ( iCiv == iBulgaria ):
                        utils.makeUnit(con.iKonnik, iCiv, tPlot, 2)
                if ( iCiv == iCordoba ):
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 2)
                if ( iCiv == iSpain ):
                        utils.makeUnit(con.iLancer, iCiv, tPlot, 3)
                if ( iCiv == iNorse ):
                        utils.makeUnit(con.iVikingBeserker, iCiv, tPlot, 4)
                if ( iCiv == iVenecia ):
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 4)
                if ( iCiv == iKiev ):
                        utils.makeUnit(con.iLancer, iCiv, tPlot, 2)
                if ( iCiv == iHungary ):
                        utils.makeUnit(con.iLancer, iCiv, tPlot, 2)
                if ( iCiv == iGermany ):
                        utils.makeUnit(con.iLancer, iCiv, tPlot, 3)
                if ( iCiv == iPoland ):
                        utils.makeUnit(con.iLancer, iCiv, tPlot, 3)
                if ( iCiv == iMoscow ):
                        utils.makeUnit(con.iMoscowBoyar, iCiv, tPlot, 1)
                if ( iCiv == iGenoa ):
                        utils.makeUnit(con.iHeavyLancer, iCiv, tPlot, 3)
                if ( iCiv == iEngland ):
                        utils.makeUnit(con.iHeavyLancer, iCiv, tPlot, 3)
                if ( iCiv == iPortugal ):
                        utils.makeUnit(con.iPortugalFootKnight, iCiv, tPlot, 4)
                if ( iCiv == iAustria ):
                        utils.makeUnit(con.iHeavyLancer, iCiv, tPlot, 4)
                if ( iCiv == iTurkey ):
                        utils.makeUnit(con.iHeavyLancer, iCiv, tPlot, 4)
                if ( iCiv == iSweden ):
                        utils.makeUnit(con.iSwedishKarolin, iCiv, tPlot, 4)
                if ( iCiv == iDutch ):
                        utils.makeUnit(con.iNetherlandsGrenadier, iCiv, tPlot, 4)                       
                # 3Miro: on war declaration (Greece gets 4! Phalanx!)
                #if (iCiv == iAmerica):
                #        utils.makeUnit(con.iPikeman, iCiv, tPlot, 3)
                #        utils.makeUnit(con.iMusketman, iCiv, tPlot, 3)
                #        utils.makeUnit(con.iCannon, iCiv, tPlot, 3)
                pass


        def createStartingUnits( self, iCiv, tPlot ):
                # Change here to make later starting civs work
                if (iCiv == iArabia):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 3)
                if (iCiv == iBulgaria):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iBulgarianKonnik, iCiv, tPlot, 6)
                if (iCiv == iCordoba):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 3)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iIslamicMissionary, iCiv, tPlot, 3)
                if (iCiv == iSpain):
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 3)
                        utils.makeUnit(con.iCatholicMissionary, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iLancer, iCiv, tPlot, 2)
                if (iCiv == iNorse):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 1)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 1)
                        utils.makeUnit(con.iVikingBeserker, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 1)
                        tSeaPlot = self.findSeaPlots(tPlot, 2)
                        if ( tSeaPlot ):
                                #utils.makeUnit(con.iGalley, iCiv, tSeaPlot, 1 )
                                #utils.makeUnit(con.iWarGalley, iCiv, tSeaPlot, 1 )
                                pNorse.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                pNorse.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1 )
                                utils.makeUnit(con.iArcher, iCiv, tSeaPlot, 1 )
                if (iCiv == iVenecia):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 1)
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 1)
                        utils.makeUnit(con.iCatholicMissionary, iCiv, tPlot, 2)
                        tSeaPlot = self.findSeaPlots(tPlot, 2)
                        if ( tSeaPlot ):
                                utils.makeUnit(con.iWorkboat, iCiv, tSeaPlot, 1 )
                                pVenecia.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                pVenecia.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler,iCiv,tSeaPlot,1)
                                utils.makeUnit(con.iArcher,iCiv,tSeaPlot,1)
                if (iCiv == iKiev):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iGuisarme, iCiv, tPlot, 2)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 2)
                if (iCiv == iHungary):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 3)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 3)
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 1)
                        utils.makeUnit(con.iGuisarme, iCiv, tPlot, 1)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 1)
                if (iCiv == iGermany):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 3)
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 2)
                if (iCiv == iPoland):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 1)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 1)
                if (iCiv == iMoscow):
                        utils.makeUnit(con.iArbalest, iCiv, tPlot, 4)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 3)
                        utils.makeUnit(con.iMoscowBoyar, iCiv, tPlot, 6)
                        utils.makeUnit(con.iGuisarme, iCiv, tPlot, 5)
                if (iCiv == iGenoa):
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iCatholicMissionary, iCiv, tPlot, 2)
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 4)
                        tSeaPlot = self.findSeaPlots(tPlot, 2)
                        if ( tSeaPlot ):
                                pGenoa.initUnit(con.iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                pGenoa.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler,iCiv,tSeaPlot,1)
                                utils.makeUnit(con.iCrossbowman,iCiv,tSeaPlot,1)
                                utils.makeUnit(con.iWorkboat, iCiv, tSeaPlot, 1 )

                if (iCiv == iEngland):
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iLongSwordsman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iHeavyLancer, iCiv, tPlot, 2)
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 4)
                if (iCiv == iPortugal):
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 4)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iPortugalFootKnight, iCiv, tPlot, 4)
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iGuisarme, iCiv, tPlot, 2)
                if (iCiv == iAustria):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 4)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 3)
                        utils.makeUnit(con.iMaceman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iLongSwordsman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iKnight, iCiv, tPlot, 2)
                if (iCiv == iTurkey):
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 3)
                        utils.makeUnit(con.iMaceman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iKnight, iCiv, tPlot, 3)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iTrebuchet, iCiv, tPlot, 2)
                        utils.makeUnit(con.iTurkeyGreatBombard, iCiv, tPlot, 1)
                        utils.makeUnit(con.iIslamicMissionary, iCiv, tPlot, 3)
                if (iCiv == iSweden):
                        utils.makeUnit(con.iSwedishKarolin, iCiv, tPlot, 5)
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iKnight, iCiv, tPlot, 2)
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 4)
                        tSeaPlot = self.findSeaPlots(tPlot, 2)
                        if ( tSeaPlot ):
                                utils.makeUnit(con.iWorkboat, iCiv, tSeaPlot, 1 )
                                utils.makeUnit(con.iCarrack, iCiv, tSeaPlot, 1 )
                                utils.makeUnit(con.iGalleon, iCiv, tSeaPlot, 1 )
                if (iCiv == iDutch):
                        utils.makeUnit(con.iSettler, iCiv, tPlot, 2)
                        utils.makeUnit(con.iMusketman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 3)
                        tSeaPlot = self.findSeaPlots(tPlot, 2)
                        if ( tSeaPlot ):
                                utils.makeUnit(con.iWorkboat, iCiv, tSeaPlot, 1 )
                                utils.makeUnit(con.iGalleon, iCiv, tSeaPlot, 2 )

                self.showArea(iCiv)
                self.initContact(iCiv)
                # 3Miro: create units on spawn
                #if (iCiv == iGreece):
                #        utils.makeUnit(con.iSettler, iCiv, tPlot, 1)
                #        utils.makeUnit(con.iWarrior, iCiv, tPlot, 2)
                #        utils.makeUnit(con.iGreekPhalanx, iCiv, tPlot, 2) #3
                #        tSeaPlot = self.findSeaPlots(tPlot, 1)
                #        if (tSeaPlot):
                #                #utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 1)
                #                pGreece.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                #                utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
                pass
                        

                                
        def createStartingWorkers( self, iCiv, tPlot ):
                # 3Miro: get the workers
                #if (iCiv == iGreece):
                #        utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
                if ( iCiv == iArabia ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iBulgaria ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iCordoba ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iSpain ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iNorse ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iVenecia ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iKiev ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iHungary ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iGermany ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iPoland ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iMoscow ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iGenoa ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iEngland ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iPortugal ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iAustria ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iTurkey ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iSweden ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])
                if ( iCiv == iDutch ):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, con.tStartingWorkers[iCiv])

        def create600ADstartingUnits( self ):
                # 3Miro: not needed
                pass
                

        def create4000BCstartingUnits( self ):
                # 3Miro: units on start (note Spearman might be an up to date upgraded defender, tech dependent)
                # for the late starts those get destroyed
                utils.makeUnit(iSettler, iBurgundy, tCapitals[iBurgundy], 1)
                utils.makeUnit(con.iArcher, iBurgundy, tCapitals[iBurgundy], 2)
                utils.makeUnit(con.iWorker, iBurgundy, tCapitals[iBurgundy], 1)
                
                # 3Miro: Byzantium Starting Units are in the WB file
                #utils.makeUnit(iSettler, iByzantium, tCapitals[iByzantium], 1)
                #utils.makeUnit(iSpearman, iByzantium, tCapitals[iByzantium], 1)
                
                utils.makeUnit(iSettler, iFrankia, tCapitals[iFrankia], 1)
                utils.makeUnit(con.iArcher, iFrankia, tCapitals[iFrankia], 2)
                utils.makeUnit(con.iCatholicMissionary, iFrankia, tCapitals[iFrankia], 1)
                utils.makeUnit(con.iWorker, iFrankia, tCapitals[iFrankia], 1)

                self.showArea(iBurgundy)
                self.showArea(iByzantium)
                self.initContact(iByzantium)
                self.showArea(iFrankia)
                self.showArea(iPope)

                if ( pArabia.isHuman() and tBirth[iArabia] > 0 ):
                        # 3Miro: prohibit contact on turn 0
                        tArabStart = ( tCapitals[iArabia][0]+2, tCapitals[iArabia][1] )
                        utils.makeUnit(iSettler, iArabia, tArabStart, 1)
                        utils.makeUnit(iSpearman, iArabia, tArabStart, 1)
                if ( pBulgaria.isHuman() and tBirth[iBulgaria] > 0 ):
                        # 3Miro: prohibit contact on turn 0
                        tBulgStart = ( tCapitals[iBulgaria][0], tCapitals[iBulgaria][1] + 1 )
                        utils.makeUnit(iSettler, iBulgaria, tBulgStart, 1)
                        utils.makeUnit(iSpearman, iBulgaria, tBulgStart, 1)
                        
                if ( pCordoba.isHuman() and tBirth[iCordoba] > 0 ):
                        utils.makeUnit(iSettler, iCordoba, tCapitals[iCordoba], 1)
                        utils.makeUnit(iSpearman, iCordoba, tCapitals[iCordoba], 1)
                        
                if ( pSpain.isHuman() and tBirth[iSpain] > 0 ):
                        utils.makeUnit(iSettler, iSpain, tCapitals[iSpain], 1)
                        utils.makeUnit(iSpearman, iSpain, tCapitals[iSpain], 1)
                        
                if ( pNorse.isHuman() and tBirth[iNorse] > 0 ):
                        utils.makeUnit(iSettler, iNorse, tCapitals[iNorse], 1)
                        utils.makeUnit(iSpearman, iNorse, tCapitals[iNorse], 1)
                        
                if ( pVenecia.isHuman() and tBirth[iVenecia] > 0 ):
                        utils.makeUnit(iSettler, iVenecia, tCapitals[iVenecia], 1)
                        utils.makeUnit(iSpearman, iVenecia, tCapitals[iVenecia], 1)

                if ( pKiev.isHuman() and tBirth[iKiev] > 0 ):
                        utils.makeUnit(iSettler, iKiev, tCapitals[iKiev], 1)
                        utils.makeUnit(iSpearman, iKiev, tCapitals[iKiev], 1)

                if ( pHungary.isHuman() and tBirth[iHungary] > 0 ):
                        utils.makeUnit(iSettler, iHungary, tCapitals[iHungary], 1)
                        utils.makeUnit(iSpearman, iHungary, tCapitals[iHungary], 1)

                if ( pGermany.isHuman() and tBirth[iGermany] > 0 ):
                        utils.makeUnit(iSettler, iGermany, tCapitals[iGermany], 1)
                        utils.makeUnit(iSpearman, iGermany, tCapitals[iGermany], 1)

                if ( pPoland.isHuman() and tBirth[iPoland] > 0 ):
                        utils.makeUnit(iSettler, iPoland, tCapitals[iPoland], 1)
                        utils.makeUnit(iSpearman, iPoland, tCapitals[iPoland], 1)

                if ( pMoscow.isHuman() and tBirth[iMoscow] > 0 ):
                        utils.makeUnit(iSettler, iMoscow, tCapitals[iMoscow], 1)
                        utils.makeUnit(iSpearman, iMoscow, tCapitals[iMoscow], 1)

                if ( pGenoa.isHuman() and tBirth[iGenoa] > 0 ):
                        utils.makeUnit(iSettler, iGenoa, tCapitals[iGenoa], 1)
                        utils.makeUnit(iSpearman, iGenoa, tCapitals[iGenoa], 1)

                if ( pEngland.isHuman() and tBirth[iEngland] > 0 ):
                        utils.makeUnit(iSettler, iEngland, tCapitals[iEngland], 1)
                        utils.makeUnit(con.iSwordsman, iEngland, tCapitals[iEngland], 1)

                if ( pPortugal.isHuman() and tBirth[iPortugal] > 0 ):
                        utils.makeUnit(iSettler, iPortugal, tCapitals[iPortugal], 1)
                        utils.makeUnit(con.iSwordsman, iPortugal, tCapitals[iPortugal], 1)

                if ( pAustria.isHuman() and tBirth[iAustria] > 0 ):
                        utils.makeUnit(iSettler, iAustria, tCapitals[iAustria], 1)
                        utils.makeUnit(con.iLongSwordsman, iAustria, tCapitals[iAustria], 1)

                if ( pTurkey.isHuman() and tBirth[iTurkey] > 0 ):
                        tTurkishStart = ( tCapitals[iTurkey][0]+1, tCapitals[iTurkey][1]+1 )
                        utils.makeUnit(iSettler, iTurkey, tTurkishStart, 1)
                        utils.makeUnit(con.iMaceman, iTurkey, tTurkishStart, 1)

                if ( pSweden.isHuman() and tBirth[iSweden] > 0 ):
                        utils.makeUnit(iSettler, iSweden, tCapitals[iSweden], 1)
                        utils.makeUnit(con.iMaceman, iSweden, tCapitals[iSweden], 1)

                if ( pDutch.isHuman() and tBirth[iDutch] > 0 ):
                        utils.makeUnit(iSettler, iDutch, tCapitals[iDutch], 1)
                        utils.makeUnit(con.iMaceman, iDutch, tCapitals[iDutch], 1)


                #if ( pGreece.isHuman() ):
                #    utils.makeUnit(iSettler, iGreece, tCapitals[iGreece], 1)
                #    utils.makeUnit(iScout, iGreece, tCapitals[iGreece], 1)
                



        def assign600ADTechs( self ):
            # 3Miro: not needed
            pass
                
        def assignTechs( self, iCiv ):
                #popup = Popup.PyPopup()
                #popup.setBodyString( 'assigning techs to civ #%d' %(iCiv))
                #popup.launch()
                
                # 3Miro: other than the original techs
                
                if ( tBirth[iCiv] == 0 ):
                        return
              
                if ( iCiv == iArabia ):
                        teamArabia.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iLateenSails, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iLiterature, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iCodeOfLaws, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iHerbalMedicine, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iAstrolabe, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iArabicKnowledge, True, iCiv, False, False )
                        teamArabia.setHasTech( con.iHerbalMedicine, True, iCiv, False, False )
                        
                
                if ( iCiv == iBulgaria ):
                        teamBulgaria.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamBulgaria.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamBulgaria.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamBulgaria.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamBulgaria.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        
                if ( iCiv == iCordoba ):
                        teamCordoba.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iLateenSails, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iLiterature, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iCodeOfLaws, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iHerbalMedicine, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iAstrolabe, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iArabicKnowledge, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iHerbalMedicine, True, iCiv, False, False )
                        teamCordoba.setHasTech( con.iEngineering, True, iCiv, False, False )

                if ( iCiv == iSpain ):
                        teamSpain.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iLateenSails, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iAstrolabe, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iMusic, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iHerbalMedicine, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iManorialism, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iVassalage, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iEngineering, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iMachinery, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iFeudalism, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iChainMail, True, iCiv, False, False )
                        teamSpain.setHasTech( con.iAristocracy, True, iCiv, False, False )
                
                if ( iCiv == iNorse ):
                        teamNorse.setHasTech( con.iVassalage, True, iCiv, False, False )
                        teamNorse.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamNorse.setHasTech( con.iAstrolabe, True, iCiv, False, False )
                        teamNorse.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamNorse.setHasTech( con.iManorialism, True, iCiv, False, False )
                        teamNorse.setHasTech( con.iBronzeCasting, True, iCiv, False, False )

                
                if ( iCiv == iVenecia ):
                        teamVenecia.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iLateenSails, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iAstrolabe, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iMusic, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iLiterature, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iHerbalMedicine, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iManorialism, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iVassalage, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iCodeOfLaws, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                        teamVenecia.setHasTech( con.iChainMail, True, iCiv, False, False )

                        
                if ( iCiv == iKiev ):        
                        teamKiev.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iManorialism, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iVassalage, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iFeudalism, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iFarriers, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                        teamKiev.setHasTech( con.iChainMail, True, iCiv, False, False )

                        
                if ( iCiv == iHungary ):
                        teamHungary.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iManorialism, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iVassalage, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iFeudalism, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iFarriers, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iChainMail, True, iCiv, False, False )
                        teamHungary.setHasTech( con.iArt, True, iCiv, False, False )
                        
                if ( iCiv == iGermany ):
                        teamGermany.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iManorialism, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iVassalage, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iFeudalism, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iFarriers, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iArt, True, iCiv, False, False )  
                        teamGermany.setHasTech( con.iEngineering, True, iCiv, False, False ) 
                        teamGermany.setHasTech( con.iMachinery, True, iCiv, False, False ) 
                        teamGermany.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iChainMail, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iAristocracy, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iCodeOfLaws, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iAstrolabe, True, iCiv, False, False )
                        teamGermany.setHasTech( con.iMusic, True, iCiv, False, False )
                        
                if ( iCiv == iPoland ):
                        teamPoland.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iManorialism, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iVassalage, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iFeudalism, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iFarriers, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iArt, True, iCiv, False, False )  
                        teamPoland.setHasTech( con.iEngineering, True, iCiv, False, False ) 
                        teamPoland.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                        teamPoland.setHasTech( con.iChainMail, True, iCiv, False, False )
                        

                if ( iCiv == iMoscow ):
                 #     teamMoscow.setHasTech( con.iCalendar, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iArchitecture, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iTheology, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iMonasticism, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iManorialism, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iVassalage, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iFeudalism, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iStirrup, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iFarriers, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iArt, True, iCiv, False, False )  
                 #     teamMoscow.setHasTech( con.iEngineering, True, iCiv, False, False ) 
                 #     teamMoscow.setHasTech( con.iMachinery, True, iCiv, False, False ) 
                 #     teamMoscow.setHasTech( con.iMusic, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iBlastFurnace, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                 #     teamMoscow.setHasTech( con.iChainMail, True, iCiv, False, False )
                        for iTech in range( con.iFarriers + 1 ):
                                teamMoscow.setHasTech( iTech, True, iCiv, False, False )
                        teamMoscow.setHasTech( con.iBlastFurnace, True, iCiv, False, False )
                        teamMoscow.setHasTech( con.iCodeOfLaws, True, iCiv, False, False )
                        teamMoscow.setHasTech( con.iGothicArchitecture, True, iCiv, False, False )
                        teamMoscow.setHasTech( con.iChivalry, True, iCiv, False, False )
                        teamMoscow.setHasTech( con.iAristocracy, True, iCiv, False, False )
                        teamMoscow.setHasTech( con.iCivilService, True, iCiv, False, False )

                        
                if ( iCiv == iGenoa ):
                        teamGenoa.setHasTech( con.iCalendar, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iLateenSails, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iAstrolabe, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iArchitecture, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iTheology, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iMonasticism, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iMusic, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iLiterature, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iHerbalMedicine, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iManorialism, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iVassalage, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iCodeOfLaws, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iStirrup, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iEngineering, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iMachinery, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iFeudalism, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iVaultedArches, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iBronzeCasting, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iChainMail, True, iCiv, False, False )
                        teamGenoa.setHasTech( con.iAristocracy, True, iCiv, False, False )

                        
                if ( iCiv == iEngland ):
                        for iTech in range( con.iFarriers + 1 ):
                                teamEngland.setHasTech( iTech, True, iCiv, False, False )
                        teamEngland.setHasTech( con.iBlastFurnace, True, iCiv, False, False )
                        teamEngland.setHasTech( con.iCodeOfLaws, True, iCiv, False, False )
                        teamEngland.setHasTech( con.iAristocracy, True, iCiv, False, False )

                        
                if ( iCiv == iPortugal ):
                        for iTech in range( con.iFarriers + 1 ):
                                teamPortugal.setHasTech( iTech, True, iCiv, False, False )
                        teamPortugal.setHasTech( con.iBlastFurnace, True, iCiv, False, False )
                        teamPortugal.setHasTech( con.iCodeOfLaws, True, iCiv, False, False )
                        teamPortugal.setHasTech( con.iLiterature, True, iCiv, False, False )
                        teamPortugal.setHasTech( con.iMapMaking, True, iCiv, False, False )
                        teamPortugal.setHasTech( con.iAristocracy, True, iCiv, False, False )

                        
                if ( iCiv == iAustria ):
                        for iTech in range( con.iFarriers + 1 ):
                                teamAustria.setHasTech( iTech, True, iCiv, False, False )
                        teamAustria.setHasTech( con.iBlastFurnace, True, iCiv, False, False )
                        teamAustria.setHasTech( con.iCodeOfLaws, True, iCiv, False, False )
                        teamAustria.setHasTech( con.iGothicArchitecture, True, iCiv, False, False )
                        teamAustria.setHasTech( con.iChivalry, True, iCiv, False, False )
                        teamAustria.setHasTech( con.iAristocracy, True, iCiv, False, False )

                        
                if ( iCiv == iTurkey ):
                        for iTech in range( con.iChivalry + 1 ):
                                teamTurkey.setHasTech( iTech, True, iCiv, False, False )
                        teamTurkey.setHasTech( con.iGunpowder, True, iCiv, False, False )   
                        teamTurkey.setHasTech( con.iMilitaryTradition, True, iCiv, False, False )
                        teamTurkey.setHasTech( con.iArabicKnowledge, True, iCiv, False, False )              
           
                
                if ( iCiv == iSweden ):
                        for iTech in range( con.iProfessionalArmy + 1 ):
                                teamSweden.setHasTech( iTech, True, iCiv, False, False )   
                        teamSweden.setHasTech(con.iMatchlock, True, iCiv, False, False)
                                
                if ( iCiv == iDutch ):
                        for iTech in range( con.iAstronomy + 1 ):
                                teamDutch.setHasTech( iTech, True, iCiv, False, False )

                self.hitNeighboursStability(iCiv)

        def hitNeighboursStability( self, iCiv ):
                if (len(con.lOlderNeighbours[iCiv]) > 0):
                #        print "Got inside hitStability!!!"
                        bHuman = False
                        for iLoop in con.lOlderNeighbours[iCiv]:
                                if (gc.getPlayer(iLoop).isAlive()):
                                #        print("iLoop =",iLoop)
                                        if (iLoop == utils.getHumanID()):
                                                bHuman = True
                                        utils.setStabilityParameters(iLoop, con.iParDiplomacyE, utils.getStabilityParameters(iLoop, con.iParDiplomacyE)-5)
                                        utils.setStability(iLoop, utils.getStability(iLoop)-5)
        ### Begin Reformation ###
        def reformation(self):
                for iCiv in range(iNumTotalPlayers):
                        #cityList = PyPlayer(iCiv).getCityList()
                        #for city in cityList:
                        #        if(city.city.isHasReligion(con.iCatholicism)):
                        #                self.reformationchoice(iCiv)
                        #                break
                        # Orthodoxes and Muslims don't have Reformation
                        pPlayer = gc.getPlayer( iCiv )
                        if ( pPlayer.isAlive() and pPlayer.getStateReligion() == con.iCatholicism ):
                                self.reformationchoice(iCiv)
                        else:
                                self.reformationOther( iCiv )
                                
        def reformationOther( self, iCiv ):
                cityList = PyPlayer(iCiv).getCityList()
                iChanged = False
                for city in cityList:
                        if(city.city.isHasReligion(con.iCatholicism)):
                                iDummy = self.reformationReformCity( city.city, 11, False )
                                
                

        def reformationchoice(self, iCiv):
                if ((gc.getPlayer(iCiv)).isHuman()):
                        self.reformationPopup()
                else:
                        rndnum = gc.getGame().getSorenRandNum(100, 'Reformation')
                        if(rndnum <= lReformationMatrix[iCiv]):
                                self.reformationyes(iCiv)
                        else:
                                self.reformationno(iCiv)
                                
        def reformationReformCity( self, pCity, iKeepCatholicismBound, bForceConvertSmall ):
                iFaith = 0
                if(pCity.isHasReligion(con.iCatholicism)):
                        #iRandNum = gc.getSorenRandNum(100, 'Reformation of a City')
                        if (pCity.getPopulation() > iKeepCatholicismBound ):
                                pCity.setHasReligion(con.iProtestantism,True,True,False)
                                if(pCity.hasBuilding(con.iCatholicReliquary) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(con.iCatholicReliquary, False)
                                if(pCity.hasBuilding(con.iCatholicScriptorium) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(con.iCatholicScriptorium, False)
                                if(pCity.hasBuilding(con.iCatholicChapel) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(con.iCatholicChapel, False)
                                        pCity.setHasRealBuilding(con.iProtestantChapel, True)
                                if(pCity.hasBuilding(con.iCatholicTemple) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(con.iCatholicTemple, False)
                                        pCity.setHasRealBuilding(con.iProtestantTemple, True)
                                        iFaith += 1
                                if(pCity.hasBuilding(con.iCatholicMonastery) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(con.iCatholicMonastery, False)
                                        pCity.setHasRealBuilding(con.iProtestantSeminary, True)
                                        iFaith += 1
                                if(pCity.hasBuilding(con.iCatholicCathedral) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(con.iCatholicCathedral, False)
                                        pCity.setHasRealBuilding(con.iProtestantCathedral, True)
                                        iFaith += 1
                        elif ( bForceConvertSmall or gc.getGame().getSorenRandNum(100, 'Reformation of a City') < lReformationMatrix[pCity.getOwner()] ):
                                pCity.setHasReligion(con.iProtestantism,True,True,False)
                                iFaith += 1
                                if(pCity.hasBuilding(con.iCatholicReliquary)):
                                        pCity.setHasRealBuilding(con.iCatholicReliquary, False)
                                if(pCity.hasBuilding(con.iCatholicScriptorium)):
                                        pCity.setHasRealBuilding(con.iCatholicScriptorium, False)
                                if(pCity.hasBuilding(con.iCatholicChapel)):
                                        pCity.setHasRealBuilding(con.iCatholicChapel, False)
                                        pCity.setHasRealBuilding(con.iProtestantChapel, True)
                                if(pCity.hasBuilding(con.iCatholicTemple)):
                                        pCity.setHasRealBuilding(con.iCatholicTemple, False)
                                        pCity.setHasRealBuilding(con.iProtestantTemple, True)
                                        iFaith += 1
                                if(pCity.hasBuilding(con.iCatholicMonastery)):
                                        pCity.setHasRealBuilding(con.iCatholicMonastery, False)
                                        pCity.setHasRealBuilding(con.iProtestantSeminary, True)
                                        iFaith += 1
                                if(pCity.hasBuilding(con.iCatholicCathedral)):
                                        pCity.setHasRealBuilding(con.iCatholicCathedral, False)
                                        pCity.setHasRealBuilding(con.iProtestantCathedral, True)
                                        iFaith += 1
                                pCity.setHasReligion(con.iCatholicism,False,False,False)
                return iFaith

        def reformationyes(self, iCiv):
                cityList = PyPlayer(iCiv).getCityList()
                iFaith = 0
                for city in cityList:
                        if(city.city.isHasReligion(con.iCatholicism)):
                                iFaith += self.reformationReformCity( city.city, 7, True )

                pPlayer = gc.getPlayer(iCiv)
                #iStateReligion = pPlayer.getStateReligion()
                #if (pPlayer.getStateReligion() == con.iCatholicism):
                pPlayer.setLastStateReligion(con.iProtestantism)
                pPlayer.setFaith( iFaith )

        def reformationno(self, iCiv):
                cityList = PyPlayer(iCiv).getCityList()
                iLostFaith = 0
                for city in cityList:
                        if(city.city.isHasReligion(con.iCatholicism)):
                                rndnum = gc.getGame().getSorenRandNum(100, 'ReformationAnyway')
                                if(rndnum <= lReformationMatrix[iCiv]):
                                        city.city.setHasReligion(con.iProtestantism, True, False, False)
                                        iLostFaith += 1
                                        #iLostFaith += self.reformationReformCity( city.city, 9, False )
                gc.getPlayer(iCiv).changeFaith( - max( gc.getPlayer(iCiv).getFaith(), iLostFaith ) )
        ### End Reformation ###

        def showRect( self, iCiv, iXs, iYs, iXe, iYe ):
                for iX in range( iXs, iXe + 1 ):
                        for iY in range( iYs, iYe + 1 ):
                                gc.getMap().plot(iX, iY).setRevealed(gc.getPlayer(iCiv).getTeam(), True, False, -1)

        def showArea(self,iCiv):
                #print("  Visible for: ",iCiv )
                for iI in range( len( tVisible[iCiv] ) ):
                        self.showRect( iCiv, tVisible[iCiv][iI][0], tVisible[iCiv][iI][1], tVisible[iCiv][iI][2], tVisible[iCiv][iI][3] )
                #print("  Visible for: ",iCiv )
                #pass

        def initContact(self, iCiv ):
                if ( iCiv == iByzantium ):
                        if ( pPope.isAlive() and ( not teamByzantium.isHasMet( pPope.getTeam() ) ) ):
                                teamByzantium.meet( pPope.getTeam(), True )
                if ( iCiv == iCordoba ):
                        if ( pArabia.isAlive() and ( not teamCordoba.isHasMet( pArabia.getTeam() ) ) ):
                                teamCordoba.meet( pArabia.getTeam(), True )
                if ( iCiv == iSpain ):
                        if ( pBurgundy.isAlive() and ( not teamSpain.isHasMet( pBurgundy.getTeam() ) ) ):
                                teamSpain.meet( pBurgundy.getTeam(), True )
                        if ( pFrankia.isAlive() and ( not teamSpain.isHasMet( pFrankia.getTeam() ) ) ):
                                teamSpain.meet( pFrankia.getTeam(), True )
                        if ( pCordoba.isAlive() and ( not teamSpain.isHasMet( pCordoba.getTeam() ) ) ):
                                teamSpain.meet( pCordoba.getTeam(), True )
                if ( iCiv == iVenecia ):
                        if ( pByzantium.isAlive() and ( not teamVenecia.isHasMet( pByzantium.getTeam() ) ) ):
                                teamVenecia.meet( pByzantium.getTeam(), True )
                if ( iCiv == iKiev ):
                        if ( pBulgaria.isAlive() and ( not teamKiev.isHasMet( pBulgaria.getTeam() ) ) ):
                                teamKiev.meet( pBulgaria.getTeam(), True )
                        if ( pByzantium.isAlive() and ( not teamKiev.isHasMet( pByzantium.getTeam() ) ) ):
                                teamKiev.meet( pByzantium.getTeam(), True )
                if ( iCiv == iHungary ):
                        if ( pBulgaria.isAlive() and ( not teamHungary.isHasMet( pBulgaria.getTeam() ) ) ):
                                teamHungary.meet( pBulgaria.getTeam(), True )
                        if ( pByzantium.isAlive() and ( not teamHungary.isHasMet( pByzantium.getTeam() ) ) ):
                                teamHungary.meet( pByzantium.getTeam(), True )
                if ( iCiv == iGermany ):
                        if ( pBurgundy.isAlive() and ( not teamGermany.isHasMet( pBurgundy.getTeam() ) ) ):
                                teamGermany.meet( pBurgundy.getTeam(), True )
                        if ( pFrankia.isAlive() and ( not teamGermany.isHasMet( pFrankia.getTeam() ) ) ):
                                teamGermany.meet( pFrankia.getTeam(), True )
                        if ( pHungary.isAlive() and ( not teamGermany.isHasMet( pHungary.getTeam() ) ) ):
                                teamGermany.meet( pHungary.getTeam(), True )
                if ( iCiv == iPoland ):
                        if ( pGermany.isAlive() and ( not teamPoland.isHasMet( pGermany.getTeam() ) ) ):
                                teamPoland.meet( pGermany.getTeam(), True )
                        if ( pHungary.isAlive() and ( not teamPoland.isHasMet( pHungary.getTeam() ) ) ):
                                teamPoland.meet( pHungary.getTeam(), True )
                if ( iCiv == iMoscow ):
                        if ( pByzantium.isAlive() and ( not teamMoscow.isHasMet( pByzantium.getTeam() ) ) ):
                                teamMoscow.meet( pByzantium.getTeam(), True )
                        if ( pBulgaria.isAlive() and ( not teamMoscow.isHasMet( pBulgaria.getTeam() ) ) ):
                                teamMoscow.meet( pBulgaria.getTeam(), True )
                        if ( pKiev.isAlive() and ( not teamMoscow.isHasMet( pKiev.getTeam() ) ) ):
                                teamMoscow.meet( pKiev.getTeam(), True )
                if ( iCiv == iGenoa ):
                        if ( pBurgundy.isAlive() and ( not teamGenoa.isHasMet( pBurgundy.getTeam() ) ) ):
                                teamGenoa.meet( pBurgundy.getTeam(), True )
                        if ( pByzantium.isAlive() and ( not teamGenoa.isHasMet( pByzantium.getTeam() ) ) ):
                                teamGenoa.meet( pByzantium.getTeam(), True )
                        if ( pVenecia.isAlive() and ( not teamGenoa.isHasMet( pVenecia.getTeam() ) ) ):
                                teamGenoa.meet( pVenecia.getTeam(), True )
                if ( iCiv == iSweden ):
                        if ( pMoscow.isAlive() and ( not teamSweden.isHasMet( pMoscow.getTeam() ) ) ):
                                teamSweden.meet( pMoscow.getTeam(), True )
                        if ( pPoland.isAlive() and ( not teamSweden.isHasMet( pPoland.getTeam() ) ) ):
                                teamSweden.meet( pPoland.getTeam(), True )
                        if ( pGermany.isAlive() and ( not teamSweden.isHasMet( pGermany.getTeam() ) ) ):
                                teamSweden.meet( pGermany.getTeam(), True )
