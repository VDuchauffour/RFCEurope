# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
import cPickle as pickle
import Consts as con
import RFCUtils
utils = RFCUtils.RFCUtils()

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

iPlague = con.iPlague

#Sedna17: Black Death is now set to be especially severe.
iDuration = 6
iImmunity = con.iImmunity
iNumPlagues = 5
iConstantinople = 0
iBlackDeath = 1

#iHuman = utils.getHumanID()

class Plague:



     
##################################################
### Secure storage & retrieval of script data ###
################################################   
                           
                           
        def getPlagueCountdown( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lPlagueCountdown'][iCiv]

        def setPlagueCountdown( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lPlagueCountdown'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getGenericPlagueDates( self, i ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lGenericPlagueDates'][i]

        def setGenericPlagueDates( self, i, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lGenericPlagueDates'][i] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                                
        def getBadPlague( self ):
                        scriptDict = pickle.loads( gc.getGame().getScriptData() )
                        return scriptDict['bBadPlague']

        def setBadPlague( self, bBad ):
                        scriptDict = pickle.loads( gc.getGame().getScriptData() )
                        scriptDict['bBadPlague'] = bBad
                        gc.getGame().setScriptData(pickle.dumps(scriptDict))


                
#######################################
### Main methods (Event-Triggered) ###
#####################################  



        def setup(self):

                for i in range(iNumMajorPlayers):
                        self.setPlagueCountdown(i, -iImmunity) 

                #Sedna17: Set number of GenericPlagues in StoredData
                #3Miro: Pague 0 strikes France and Burgundy too hard, make it less random and force it to pick Byzantium as starting land
                #3Miro: follow up - remove Plague 0 since it hits too early
                self.setGenericPlagueDates(0, 40 + gc.getGame().getSorenRandNum(3, 'Variation') - 10) #Plagues of Constantinople
                self.setGenericPlagueDates(1, 247 + gc.getGame().getSorenRandNum(40, 'Variation') - 20) #1341 Black Death
                self.setGenericPlagueDates(2, 300 + gc.getGame().getSorenRandNum(40, 'Variation') - 20) #Generic reaccurance of plague
                self.setGenericPlagueDates(3, 375 + gc.getGame().getSorenRandNum(40, 'Variation') - 30) #1650 Great Plague
                self.setGenericPlagueDates(4, 440 + gc.getGame().getSorenRandNum(40, 'Variation') - 30) #1740 Small Pox
                #self.setGenericPlagueDates(0, 40 + gc.getGame().getSorenRandNum(4, 'Variation') - 2) # test date 40 (-2, +2)
                #self.setGenericPlagueDates(0, 40 ) # test date 40

            
        def checkTurn(self, iGameTurn):

                for i in range(iNumTotalPlayersB):
                        if (gc.getPlayer(i).isAlive()):
                                if (self.getPlagueCountdown(i) > 0):                                        
                                        self.setPlagueCountdown(i, self.getPlagueCountdown(i)-1)
                                        print ("plague countdown", i, self.getPlagueCountdown(i))
                                        if (self.getPlagueCountdown(i) == 2):
                                                self.preStopPlague(i)
                                        if (self.getPlagueCountdown(i) == 0):
                                                self.stopPlague(i)
                                elif (self.getPlagueCountdown(i) < 0):
                                        self.setPlagueCountdown(i, self.getPlagueCountdown(i)+1)

                for i in range(iNumPlagues):
                        if ( iGameTurn == self.getGenericPlagueDates( i ) ):
                                self.startPlague(i)
                                
                        # if the plague has stopped too quickly, restart
                        if (iGameTurn == self.getGenericPlagueDates(i) + 4):
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
                iWorstHealth = 200
                for i in range(iNumMajorPlayers):
                        pPlayer = gc.getPlayer(i)
                        if (pPlayer.isAlive()):
                                iHealth = self.calcHealth( i )
                                print(" player health ",i,iHealth )
                                if (self.isVulnerable(i, iHealth) ):
                                        #print(" Vulnerable civ ",i)
                                        #iHealth2 = iHealth/2
                                        iHealth2 = iHealth/2 + gc.getGame().getSorenRandNum(20, 'random modifier')
                                        print( " modified ",iHealth2 )
                                        
                                        if ( iHealth2 < iWorstHealth ):
                                                iWorstCiv = i
                                                iWorstHealth = iHealth2
                
                #3Miro: Plague of Constantinople (that started at Alexandria)
                if ( iPlagueCount == iConstantinople ):
                        iWorstCiv = con.iByzantium
                if (iPlagueCount == iBlackDeath):
                                        self.setBadPlague(True)

                print( " startPlague: worst civ: ",iWorstCiv )
                if ( iWorstCiv == -1 ):
                        iWorstCiv = utils.getRandomCiv()
                        
                pWorstCiv = gc.getPlayer(iWorstCiv)
                city = utils.getRandomCity(iWorstCiv)
                if (city != -1):                                
                        self.spreadPlague(iWorstCiv)
                        self.infectCity(city)
                        iHuman = utils.getHumanID()
                        if (gc.getPlayer(iHuman).canContact(iWorstCiv) and iHuman != iWorstCiv):
                                CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + " (" + gc.getPlayer(city.getOwner()).getCivilizationAdjective(0) + ")!", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                        


        def calcHealth( self, iPlayer ):
                pPlayer = gc.getPlayer(iPlayer)
                iTCH = pPlayer.calculateTotalCityHealthiness()
                iTCU = pPlayer.calculateTotalCityUnhealthiness()
                if ( iTCH > 0 ):
                        return int((1.0 * iTCH) / (iTCH + iTCU) * 100) - 60
                else:
                        return -30
                

        def isVulnerable(self, iPlayer, iHealth):
                # Indys and Barbs are vulnerable for more than -10
                # calculate the total health percent, to determine if vulnerable or not (also tech immunicy goes here)
                # if Health == -100, calculate player's health, else: use the value
                if (iPlayer >= iNumMajorPlayers):
                        if (self.getPlagueCountdown(iPlayer) <= 0 and self.getPlagueCountdown(iPlayer) > -10 ): #more vulnerable
                                return True
                else:                        
                        pPlayer = gc.getPlayer(iPlayer)  
                        #print( " iPlayer, countdown: ",iPlayer,self.getPlagueCountdown(iPlayer) )
                        if (self.getPlagueCountdown(iPlayer) == 0): #vulnerable
                                if ( iHealth == -100 ):
                                        iHealth = self.calcHealth( iPlayer )
                                        #print(" iPlayer:  iHealth: ",iPlayer, iHealth )
                                        if (iHealth < 14): #no spread for iHealth >= 74 years
                                                return True
                                else:
                                        if ( iHealth < 14 ):
                                                return True
                return False


        def spreadPlague( self, iPlayer ):
                iHealth = self.calcHealth( iPlayer )
                iHealth /= 7 #duration range will be -4 to +5 for 30 to 90
                self.setPlagueCountdown(iPlayer, iDuration - iHealth)

        def infectCity( self, city ):
                city.setHasRealBuilding(iPlague, True)
                if (gc.getPlayer(city.getOwner()).isHuman()):
                        CyInterface().addMessage(city.getOwner(), True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + "!", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                for x in range(city.getX()-2, city.getX()+3):
                        for y in range(city.getY()-2, city.getY()+3):
                                if ( x>=0 and x<con.iMapMaxX and y>=0 and y<con.iMapMaxY ):
                                        pCurrent = gc.getMap().plot( x, y )                
                                        iImprovement = pCurrent.getImprovementType()
                                        if (iImprovement == con.iImprovementHamlet):
                                                pCurrent.setImprovementType(con.iImprovementCottage)
                                        if (iImprovement == con.iImprovementVillage):
                                                pCurrent.setImprovementType(con.iImprovementHamlet)
                                        if (iImprovement == con.iImprovementTown):
                                                pCurrent.setImprovementType(con.iImprovementVillage)
                                        
                self.killUnitsByPlague(city, gc.getMap().plot( city.getX(), city.getY() ) , 0, 120, 0)     

        
        def killUnitsByPlague( self, city, plot, iTreshhold, iDamage, iPreserveDefenders ):
                iCityOwner = city.getOwner()
                pCityOwner = gc.getPlayer(iCityOwner)
                teamCityOwner = gc.getTeam( pCityOwner.getTeam() )
                
                iNumUnitsInAPlot = plot.getNumUnits()
                
                iPreserveHumanDefenders = iPreserveDefenders
                iHuman = utils.getHumanID()
                
                iCityHealthRate = city.healthRate(False, 0)
                # do something about preserving the defenders in a city
                
                
                if (iNumUnitsInAPlot):                        
                        for j in range(iNumUnitsInAPlot):
                                i = iNumUnitsInAPlot - j - 1 # count back from the weakest unit
                                unit = plot.getUnit(i)
                                if ( utils.isMortalUnit( unit ) and gc.getGame().getSorenRandNum(100, 'roll') > iTreshhold + 5*iCityHealthRate ):
                                        iUnitDamage = unit.getDamage()
                                        if ( unit.getOwner() == iHuman and iPreserveHumanDefenders > 0 ):
                                                iPreserveHumanDefenders -= 1
                                                if ( iUnitDamage < 50 ):
                                                        #print( "  raw damage ", iUnitDamage + iDamage - unit.getExperience()/10 - 2*unit.baseCombatStr() / 7 )
                                                        unit.setDamage( max( iUnitDamage, min( 50, iUnitDamage + iDamage - unit.getExperience()/10 - 2*unit.baseCombatStr() ) ), iBarbarian )                                              
                                                        #print( " Damage Human Defender: ", unit.getDamage() )
                                        elif ( unit.getOwner() == iCityOwner and iPreserveDefenders > 0 ):
                                                iPreserveDefenders -= 1
                                                if ( iUnitDamage < 30 ):
                                                        #print( "  raw damage ", iUnitDamage + iDamage - unit.getExperience()/10 - 2*unit.baseCombatStr() / 7 )
                                                        unit.setDamage( max( iUnitDamage, min( 30, iUnitDamage + iDamage - unit.getExperience()/10 - 2*unit.baseCombatStr() ) ), iBarbarian )                                             
                                                        #print( " Damage AI Defender: ", unit.getDamage() )
                                        else:
                                                #print( "  raw damage ", iUnitDamage + iDamage - unit.getExperience()/10 - 2*unit.baseCombatStr() )
                                                iUnitDamage = max( iUnitDamage, unit.getDamage() + iDamage - unit.getExperience()/10 - 2*unit.baseCombatStr() / 7 )
                                                #print( "   iUnitDamage ",iUnitDamage )
                                                if ( iUnitDamage >= 100 ):
                                                        unit.kill( False, iBarbarian )
                                                        #print( " Kill Unit: ", unit.getDamage() )
                                                        if ( iCityOwner != unit.getOwner() and unit.getOwner() == iHuman ):
                                                                CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_PROCESS_UNIT", ()) + " " + city.getName(), "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                                                else:
                                                        #print( " Damage Unit: ", unit.getDamage() )
                                                        unit.setDamage( iUnitDamage, iBarbarian )
                                                # if we have many units, decrease the damage for every other unit
                                                iDamage *= 3
                                                iDamage /= 4
        
        def processPlague( self, iPlayer ):
                
                bBadPlague = self.getBadPlague()
                pPlayer = gc.getPlayer(iPlayer)
                #first spread to close locations
                cityList = [] #see below, make a list of city objects, apCityList is a list generated by a Python utility
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        cityList.append(city) #see below
                        if (city.hasBuilding(iPlague)):
                                # kill citizens
                                if (city.getPopulation() > 1):
					iRandom = gc.getGame().getSorenRandNum(100, 'roll')
                                        if (iRandom > 30 + 5*city.healthRate(False, 0)) and bBadPlague:
                                                city.changePopulation(-2)
                                                print("This is the Black Death")
                                        elif (iRandom > 40 + 5*city.healthRate(False, 0)):
                                                city.changePopulation(-1)
                                # infect vassals
                                if (city.isCapital()):
                                        for iLoopCiv in range(iNumMajorPlayers):
                                                if (gc.getTeam(pPlayer.getTeam()).isVassal(iLoopCiv) or gc.getTeam(gc.getPlayer(iLoopCiv).getTeam()).isVassal(iPlayer)):
                                                        if (gc.getPlayer(iLoopCiv).getNumCities() > 0): #this check is needed, otherwise game crashes
                                                                capital = gc.getPlayer(iLoopCiv).getCapitalCity()
                                                                if ( self.isVulnerable(iLoopCiv, -100 ) ):
                                                                        if (self.getPlagueCountdown(iPlayer) > 2):
                                                                                self.spreadPlague(iLoopCiv)
                                                                                self.infectCity(capital)
                                
                                #kill units and spread plague in a 2x2 around the city                                                
                                for x in range(city.getX()-2, city.getX()+3):
                                        for y in range(city.getY()-2, city.getY()+3):
                                                if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
                                                        pCurrent = gc.getMap().plot( x, y )
                                                        # spread to neighbours
                                                        if (pCurrent.getOwner() != iPlayer and pCurrent.getOwner() >= 0):
                                                                #print(" doesn't own and owner >0 ")
                                                                if (self.getPlagueCountdown(iPlayer) > 2): #don't spread the last turns
                                                                        #print(" more than 2 turns ")
                                                                        if (self.isVulnerable(pCurrent.getOwner(), -100)):
                                                                                print(" Vulnerable ")
                                                                                self.spreadPlague(pCurrent.getOwner())
                                                                                self.infectCitiesNear(pCurrent.getOwner(), x, y)
                                                        else:
                                                                # if it is a city
                                                                if (pCurrent.isCity() and not (x == city.getX() and y == city.getY())):
                                                                        cityNear = pCurrent.getPlotCity() 
                                                                        if (not cityNear.hasBuilding(iPlague)):
                                                                                if (self.getPlagueCountdown(iPlayer) > 2): #don't spread the last turns
                                                                                        self.infectCity(cityNear)
                                                                else:
                                                                # if just a plot, kill units
                                                                        if (x == city.getX() and y == city.getY()):
                                                                                self.killUnitsByPlague(city, pCurrent, 0, 50, 2)
                                                                        else:
                                                                                if (pCurrent.isRoute()):
                                                                                        self.killUnitsByPlague(city, pCurrent, 10, 35, 0)
                                                                                elif (pCurrent.isWater()):
                                                                                        self.killUnitsByPlague(city, pCurrent, 25, 35, 0)
                                                                                else:
                                                                                        self.killUnitsByPlague(city, pCurrent, 30, 35, 0)
                                #kill units further from the city
                                for x in range(city.getX()-3, city.getX()+4):
                                        y = city.getY() - 3
                                        if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
                                                pCurrent = gc.getMap().plot( x, y )
                                                if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
                                                        if (not pCurrent.isCity()):
                                                                if (pCurrent.isRoute() or pCurrent.isWater()):
                                                                        self.killUnitsByPlague(city, pCurrent, 30, 35, 0)
                                        y = city.getY() +3
                                        if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
                                                pCurrent = gc.getMap().plot( x, y )
                                                if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
                                                        if (not pCurrent.isCity()):
                                                                if (pCurrent.isRoute() or pCurrent.isWater()):
                                                                        self.killUnitsByPlague(city, pCurrent, 30, 35, 0)
                                for y in range(city.getY()-2, city.getY()+3):
                                        x = city.getX() - 3
                                        if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
                                                pCurrent = gc.getMap().plot( x, y )
                                                if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
                                                        if (not pCurrent.isCity()):
                                                                if (pCurrent.isRoute() or pCurrent.isWater()):
                                                                        self.killUnitsByPlague(city, pCurrent, 30, 35, 0)
                                        x = city.getX() +3
                                        if ( x>=0 and x<con.iMapMaxX and y >=0 and y <con.iMapMaxY ):
                                                pCurrent = gc.getMap().plot( x, y )
                                                if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
                                                        if (not pCurrent.isCity()):
                                                                if (pCurrent.isRoute() or pCurrent.isWater()):
                                                                        self.killUnitsByPlague(city, pCurrent, 30, 35, 0)
                                
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
                                                                        if (self.isVulnerable(iOwner, -100) ):
                                                                                self.spreadPlague(iOwner)
                                                                                self.infectCity(loopCity)
                                                                                iHuman = utils.getHumanID()
                                                                                if (gc.getPlayer(iHuman).canContact(iOwner) and iHuman != iOwner):
                                                                                        CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + loopCity.getName() + " (" + gc.getPlayer(iOwner).getCivilizationAdjective(0) + ")", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                                                                                        
                #spread to other cities
                if (len(cityList)):
                        if (self.getPlagueCountdown(iPlayer) > 2): #don't spread the last turns
                                for city1 in cityList:
                                        if (city1.hasBuilding(iPlague)):
                                                for city2 in cityList:
                                                        if (not city2.hasBuilding(iPlague)):
                                                                if (city1.isConnectedTo(city2)):
                                                                        if (utils.calculateDistance(city1.getX(), city1.getY(), city2.getX(), city2.getY()) <= 6):
                                                                                self.infectCity(city2)
                                                                                return # stop if one city infected, don't infect all at the same time
        
        def infectCitiesNear(self, iPlayer, startingX, startingY):
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        if (utils.calculateDistance(city.getX(), city.getY(), startingX, startingY) <= 3):
                                self.infectCity(city)
                                iHuman = utils.getHumanID()
                                if (gc.getPlayer(iHuman).canContact(iPlayer) and iHuman != iPlayer):
                                        CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + " (" + gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ")", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
        
        
        
        def preStopPlague(self, iPlayer):
                cityList = []
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        if (city.hasBuilding(iPlague)):
                                cityList.append(city)
                                
                if (len(cityList)):
                        iModifier = 0
                        for city in cityList:
                                if (gc.getGame().getSorenRandNum(100, 'roll') > 30 - 5*city.healthRate(False, 0) + iModifier):
                                        city.setHasRealBuilding(iPlague, False)
                                        iModifier += 5 #not every city should quit
                                        
        def stopPlague(self, iPlayer):
                
                self.setPlagueCountdown(iPlayer, -iImmunity)
                apCityList = PyPlayer(iPlayer).getCityList()
                
                for pCity in apCityList:
                        pCity.GetCy().setHasRealBuilding(iPlague, False)
        
        def onCityAcquired(self, iOldOwner, iNewOwner, city):
                if (city.hasBuilding(iPlague)):
                        if (self.getPlagueCountdown(iNewOwner) <= 0 and gc.getGame().getGameTurn() > con.tBirth[iNewOwner] + iImmunity ): #skip immunity in this case, but not for the new born civs
                                self.spreadPlague(iNewOwner)
                                apCityList = PyPlayer(iNewOwner).getCityList()
                                for pCity in apCityList:
                                        cityNear = pCity.GetCy()
                                        if (utils.calculateDistance(city.getX(), city.getY(), cityNear.getX(), cityNear.getY()) <= 3):
                                                self.infectCity(cityNear)
                        else:
                                city.setHasRealBuilding(iPlague, False)
                
        def onCityRazed(self, city, iNewOwner):
                # even if you raze the city, you shoul dstill get the plague
                pass
                                                                
