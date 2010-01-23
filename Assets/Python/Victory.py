# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
import cPickle as pickle
import Consts as con
import RFCUtils
import Crusades as cru

utils = RFCUtils.RFCUtils()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer





### Constants ###
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
pPope = gc.getPlayer(iPope)

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
teamIndependent = gc.getTeam(pIndependent.getTeam())
teamIndependent2 = gc.getTeam(pIndependent2.getTeam())
teamBarbarian = gc.getTeam(pBarbarian.getTeam())

# 3Miro: years
i1000AD = con.i1000AD
i1101AD = con.i1101AD
i1200AD = con.i1200AD
i1281AD = con.i1281AD
i1300AD = con.i1300AD
i1350AD = con.i1350AD
i1359AD = con.i1359AD
i1401AD = con.i1401AD
i1419AD = con.i1419AD
i1431AD = con.i1431AD
i1449AD = con.i1449AD
i1452AD = con.i1452AD
i1461AD = con.i1461AD
i1470AD = con.i1470AD
i1482AD = con.i1482AD
i1491AD = con.i1491AD
i1500AD = con.i1500AD
i1520AD = con.i1520AD
i1526AD = con.i1526AD
i1540AD = con.i1540AD
i1570AD = con.i1570AD
i1600AD = con.i1600AD
i1620AD = con.i1620AD
i1640AD = con.i1640AD
i1650AD = con.i1650AD
i1660AD = con.i1660AD
i1670AD = con.i1670AD
i1680AD = con.i1680AD
i1700AD = con.i1700AD
i1730AD = con.i1730AD
i1750AD = con.i1750AD



# 3Miro: areas
tBurgundyControl = (( 46, 40, 52, 53 ),(44, 33, 48,39))
tByzantineControl = ( 68, 15, 99, 26 )
tFrankControl = (( 36, 36, 40, 49 ),(41, 33, 47, 49)) #France is now two rectangles
tArabiaControl = ( (93, 0, 99, 17), (76, 0, 92, 4), (31, 0, 54, 21), (55, 0, 88, 9) ) # Levant and Allepo and Antioch, Egypt, Egypt and Libia, Algeria and Tunisia
tBulgariaControl = ( 66, 23, 82, 32 )
tCordobaControl = (( 20,24,40,40 ),( 11,14,47,23 )) # Iberia, North-West Africa
tSpainControl = (( 20, 24, 35, 40 ),(36, 30, 41, 35)) # Iberia
tSpainControl2 = ((15,14,48,23),(49,6,52,18),(49,22,50,29),(54,16,58,19),(59,19,64,27),(51,25,58,33),(49,43,58,39) ) # Africa x2, Islands (Corsica + Sardines), Sicily, Italy x3
tNorseSettle = ( (35, 46, 46, 50 ), (39, 52, 45, 67 ), (35, 52, 38, 56 ), (31, 57, 37, 62 ), ( 0, 69, 4, 72 ), ( 54, 16, 58, 19)  ) # North France, Britain, Britain, Ireland, Iseland, Sicily
#tVenecianControl = ( (59, 32, 61, 36), (61, 28, 64, 32), ( 65, 17, 67, 29 ), ( 67, 23, 81, 25 ), ( 67, 14, 73, 22 ), ( 88, 11, 91, 13 ), ( 71, 10, 75, 10 ), ( 78, 11, 79, 12 ) ) # 3x Dalmatian Coast, 2x Main Land Greece, Cyprus, Crete, Rhodes
tVenecianControl = ( (56, 33, 60, 36), (61, 29, 62, 34), (63, 25, 65, 30), (66, 21, 67, 27), ( 67, 23, 81, 25 ), ( 67, 14, 73, 22 ), ( 88, 11, 91, 13 ), ( 71, 10, 75, 10 ), ( 78, 11, 79, 12 ) ) # 4x Dalmatian Coast, 2x Main Land Greece, Cyprus, Crete, Rhodes
tKievControl = (83, 32, 99, 39 )
tHungarianControl = ( 0, 23, 99, 72 )
tHungarianControl2 = ( (20,24,48,72),(49,30,99,72),(54,20,76,29),(60,14,75,19),(81,29,77,23) )
tGermanyControl = ( 49, 40, 54, 53 )
tMoscowControl = ( 77, 32, 99, 70 )
#tGenoaControl = (( 49, 22, 50, 25 ), ( 44, 32, 46, 34 ), ( 51, 36, 53, 38 ), ( 88, 11, 91, 13 ), ( 72, 10, 75, 10 ), (86, 32, 91, 35 ) ) #Sardinia, Marseilles, Milano, Cyprus, Crete, Crimea

tGenoaControl = (( 49, 22, 50, 25 ), ( 44, 32, 46, 34 ), ( 51, 36, 53, 38 ), ( 88, 11, 91, 13 ), ( 72, 10, 75, 10 ) ) #Sardinia, Marseilles, Milano, Cyprus, Crete 
tEnglishControl = ((39, 61, 44, 67), (31,57,37,62), (37,55,40,57)) # Scotland, Ireland, Wales
tPortugalControl = ((1,15,8,39),(7,0,27,24),(4,0,6,7)) # Islands, Africa x 2
tNormanControl = ((39,47,46,50), (35,45,38,47), (36,38,41,44), (43,45,46,46)) # Bits of France
tAustrianControl = ( 58, 33, 70, 38 )
tTurkishControl = (( 77, 14, 99, 26 ), ( 65, 14, 80, 29 ), (93, 0, 99, 17), (76, 0, 92, 4), ( 60, 33, 63, 41 ) ) # Constantinople Area and Anatolia, Balkans and Peloponnesian, Levant, Egypt, Vienna
tSwedishControl = (( 60, 56, 68, 72 ), ( 69, 63, 77, 72 ) ) # Sweden, Finland/Estland

class Victory:

     
##################################################
### Secure storage & retrieval of script data ###
################################################   
		           

        def getGoal( self, i, j ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lGoals'][i][j]

        def setGoal( self, i, j, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lGoals'][i][j] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getReligionFounded( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lReligionFounded'][iCiv]

        def setReligionFounded( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lReligionFounded'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getEnslavedUnits( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iEnslavedUnits']

        def getRazedByMongols( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iRazedByMongols']
            
        def setRazedByMongols( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iRazedByMongols'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getEnglishEras( self, i ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lEnglishEras'][i]

        def setEnglishEras( self, i, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lEnglishEras'][i] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getGreekTechs( self, i ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lGreekTechs'][i]

        def setGreekTechs( self, i, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lGreekTechs'][i] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getWondersBuilt( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lWondersBuilt'][iCiv]

        def setWondersBuilt( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lWondersBuilt'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def get2OutOf3( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['l2OutOf3'][iCiv]

        def set2OutOf3( self, iCiv, bNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['l2OutOf3'][iCiv] = bNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getNumSinks( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iNumSinks']
            
        def setNumSinks( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iNumSinks'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getBabylonianTechs( self, i ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lBabylonianTechs'][i]

        def setBabylonianTechs( self, i, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lBabylonianTechs'][i] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getMediterraneanColonies( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iMediterraneanColonies']
            
        def setMediterraneanColonies( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iMediterraneanColonies'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getPortugueseColonies( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iPortugueseColonies']
            
        def setPortugueseColonies( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iPortugueseColonies'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getNorseRazed( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iNorseRazed']

        def setNorseRazed( self, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iNorseRazed'] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getNewWorld( self, i ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lNewWorld'][i]

        def setNewWorld( self, i, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lNewWorld'][i] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
		
	def getColonies( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lColonies'][iCiv]
		
	def changeColonies( self, iCiv, iChange ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lColonies'][iCiv] += iChange
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getGenoaBanks( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return (scriptDict['bGenoaBanks'] == 1)
		
	def setGenoaBanks( self, iChange ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['bGenoaBanks'] = iChange
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getGenoaCorporations( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['bGenoaCorps']
		
	def setGenoaCorporations( self, iChange ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['bGenoaCorps'] = iChange
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getCorporationsFounded( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['bCorpsFounded']
		
	def setCorporationsFounded( self, iChange ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['bCorpsFounded'] = iChange
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

                
#######################################
### Main methods (Event-Triggered) ###
#####################################  


        def checkOwnedCiv(self, iActiveCiv, iOwnedCiv):
                dummy1, plotList1 = utils.squareSearch( tNormalAreasTL[iOwnedCiv], tNormalAreasBR[iOwnedCiv], utils.ownedCityPlots, iActiveCiv )
                dummy2, plotList2 = utils.squareSearch( tNormalAreasTL[iOwnedCiv], tNormalAreasBR[iOwnedCiv], utils.ownedCityPlots, iOwnedCiv )
                if ((len(plotList1) >= 2 and len(plotList1) > len(plotList2)) or (len(plotList1) >= 1 and not gc.getPlayer(iOwnedCiv).isAlive())):
                        return True
                else:
                        return False


        def checkOwnedArea(self, iActiveCiv, tTopLeft, tBottomRight, iThreshold):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                if (len(plotList) >= iThreshold):
                        return True
                else:
                        return False

        def checkNotOwnedArea(self, iActiveCiv, tTopLeft, tBottomRight):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                if (len(plotList)):
                        return False
                else:
                        return True

        def checkNotOwnedArea_Skip(self, iActiveCiv, tTopLeft, tBottomRight, tSkipTopLeft, tSkipBottomRight):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                if (not len(plotList)):
                        return True
                else:
                        for loopPlot in plotList:
                                if not (loopPlot[0] >= tSkipTopLeft[0] and loopPlot[0] <= tSkipBottomRight[0] and \
                                    loopPlot[1] >= tSkipTopLeft[1] and loopPlot[1] <= tSkipBottomRight[1]):
                                        return False
                return True
                                        

        def checkOwnedCoastalArea(self, iActiveCiv, tTopLeft, tBottomRight, iThreshold):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                iCounter = 0
                for i in range(len(plotList)):
                        x = plotList[i][0]
                        y = plotList[i][1]
                        plot = gc.getMap().plot(x, y)
                        if (plot.isCity()):
                               if (plot.getPlotCity().isCoastalOld()):
                                       iCounter += 1
                if (iCounter >= iThreshold):
                        return True
                else:
                        return False


        def checkTurn(self, iGameTurn):

                #debug
                #self.setGoal(iEgypt, 0, 1)
                #self.setGoal(iEgypt, 1, 1)
                #self.setGoal(iEgypt, 2, 1)

                pass
                #for iCiv in range(iNumPlayers):
                #    print (iCiv, self.getGoal(iCiv, 0), self.getGoal(iCiv, 1), self.getGoal(iCiv, 2))


                    
       	
        def checkPlayerTurn(self, iGameTurn, iPlayer):
		# 3Miro: pretty much everything here is written by me, the victory check at the end is Rhye's, but the rest is mine
		# Sedna: Made Burgundy and Frankis check that gc.doesOwnCities == 11 (previously just checked true, which would be satisfied with no cities)
		if ( iPlayer == iBurgundy and pBurgundy.isAlive() ):
			if ( iGameTurn == con.i1200AD and self.getGoal(iBurgundy, 0 ) == -1 ):
				iBurgundyRhine = gc.doesOwnCities( iBurgundy, tBurgundyControl[0][0], tBurgundyControl[0][1], tBurgundyControl[0][2], tBurgundyControl[0][3] )
				iBurgundyRhone = gc.doesOwnCities( iBurgundy, tBurgundyControl[1][0], tBurgundyControl[1][1], tBurgundyControl[1][2], tBurgundyControl[1][3] )
				if (iBurgundyRhine == 11 and iBurgundyRhone == 11):
					self.setGoal( iBurgundy, 0, 1 )
				else:
					self.setGoal( iBurgundy, 0, 0 )
			if (iGameTurn == con.i1300AD and self.getGoal(iBurgundy, 1) == -1 ):
				pJPlot = gc.getMap().plot( con.iJerusalem[0], con.iJerusalem[1] )
				if ( pJPlot.isCity()):
					if ( pJPlot.getPlotCity().getOwner() == iBurgundy ):
						self.setGoal(iBurgundy,1,1)
					else:
						self.setGoal(iBurgundy,1,0)
					
			#if ( iGameTurn == i1401AD and self.getGoal( iBurgundy, 1 ) == -1 ): #see onCityAquire
			#	self.setGoal( iBurgundy, 1, 1 )
			
			if ( iGameTurn == i1470AD and self.getGoal( iBurgundy, 2 ) == -1 ):
				tOwnedLuxes = []
				tCompete = [pPortugal,pSpain,pEngland,pFrankia,pGenoa,pVenecia,pPope,pGermany,pNorse]
				for pPlayer in tCompete:
					if ( pPlayer.isAlive()):
						tOwnedLuxes.append(self.getOwnedLuxes(pPlayer))
				print("Owned Luxuries:", tOwnedLuxes)
				if ( self.getOwnedLuxes( pBurgundy ) > max(tOwnedLuxes) ):
					self.setGoal( iBurgundy, 2, 1 )
				else:
					self.setGoal( iBurgundy, 2, 0 )

		elif ( iPlayer == iByzantium and pByzantium.isAlive() ):
			if ( iGameTurn == i1000AD and self.getGoal( iByzantium, 0) == -1 ):
				if ( gc.isLargestCity( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ) and gc.isTopCultureCity( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ) and gc.getMap().plot( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ).getPlotCity().getOwner() == iByzantium ):
					self.setGoal( iByzantium, 0, 1 )
				else:
					self.setGoal( iByzantium, 0, 0 )
					
			if ( iGameTurn == i1300AD and self.getGoal( iByzantium, 1) == -1 ):
				iOwn = gc.doesOwnCities( iByzantium, tByzantineControl[0], tByzantineControl[1], tByzantineControl[2], tByzantineControl[3] )
				if ( gc.getMap().plot( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ).isCity() and iOwn == 11 ):
					self.setGoal( iByzantium, 1, 1 )
				else:
					self.setGoal( iByzantium, 1, 0 )
					
			if ( iGameTurn == i1500AD and self.getGoal( iByzantium, 2) == -1 ):
				iGold = pByzantium.getGold()
				iMost = true
				for iCiv in range( iNumPlayers ):
					if ( iCiv != iByzantium and gc.getPlayer( iCiv ).isAlive() ):
						if (gc.getPlayer(iCiv).getGold() > iGold):
							iMost = false
				if ( iMost ):
					self.setGoal( iByzantium, 2, 1 )
				else:
					self.setGoal( iByzantium, 2, 0 )
		elif ( iPlayer == iFrankia and pFrankia.isAlive() ):
			
			if ( iGameTurn == i1500AD and self.getGoal( iFrankia, 0) == -1 ):
				iOwn = gc.doesOwnCities( iFrankia, tFrankControl[0][0], tFrankControl[0][1], tFrankControl[0][2], tFrankControl[0][3] )
				iOwn += gc.doesOwnCities( iFrankia, tFrankControl[1][0], tFrankControl[1][1], tFrankControl[1][2], tFrankControl[1][3] )
				if ( iOwn > 20 ):
					self.setGoal( iFrankia, 0, 1 )
				else:
					self.setGoal( iFrankia, 0, 0 )
			
			if ( iGameTurn <= i1680AD and self.getGoal( iFrankia, 1) == -1 ):
				pPlot = gc.getMap().plot( con.tCapitals[iFrankia][0], con.tCapitals[iFrankia][1] )
				if ( pPlot.isCity() and pPlot.getPlotCity().getOwner() == iFrankia and pPlot.getPlotCity().getCulture( iFrankia ) >= 15000 ):
					self.setGoal( iFrankia, 1, 1 )

			if ( iGameTurn == i1680AD+1 and self.getGoal( iFrankia, 1) == -1 ):
				self.setGoal( iFrankia, 1, 0 )
					
			if ( self.getGoal( iFrankia, 2 ) == - 1 ):
				if ( self.getColonies( iFrankia ) > 5 ):
					self.setGoal( iFrankia, 2, 1 )

		elif( iPlayer == iArabia and pArabia.isAlive() ):
			
			if ( iGameTurn == i1000AD and self.getGoal( iArabia, 0) == -1 ):
				iOwn = gc.doesOwnCities( iArabia, tArabiaControl[0][0], tArabiaControl[0][1], tArabiaControl[0][2], tArabiaControl[0][3] )
				iOwn += gc.doesOwnCities( iArabia, tArabiaControl[1][0], tArabiaControl[1][1], tArabiaControl[1][2], tArabiaControl[1][3] )
				if ( (iOwn % 10 > 0) and (iOwn / 10 == 2) ):
					self.setGoal( iArabia, 0, 1 )
				else:
					self.setGoal( iArabia, 0, 0 )
					
			if ( self.getGoal(iArabia, 1) == -1 ):
				perc = gc.getGame().calculateReligionPercent(con.iIslam)
				if ( perc >= 25 ):
					self.setGoal( iArabia, 1, 1 )
					
			if ( iGameTurn == i1540AD and self.getGoal( iArabia, 2) == -1 ):
				iOwn = gc.doesOwnCities( iArabia, tArabiaControl[2][0], tArabiaControl[2][1], tArabiaControl[2][2], tArabiaControl[2][3] )
				iOwn += gc.doesOwnCities( iArabia, tArabiaControl[3][0], tArabiaControl[3][1], tArabiaControl[3][2], tArabiaControl[3][3] )
				if ( (iOwn % 10 > 0) and (iOwn / 10 == 2) ):
					self.setGoal( iArabia, 2, 1 )
				else:
					self.setGoal( iArabia, 2, 0 )
					

		elif ( iPlayer == iBulgaria and pBulgaria.isAlive() ):
			# 3Miro: check for the Bulgarian control
			iOwn = True
			if ( iGameTurn <= i1200AD and self.getGoal( iBulgaria, 1 ) == -1 ): #3Miro: teritory goal 1
				iOwn = gc.doesOwnCities( iBulgaria, tBulgariaControl[0], tBulgariaControl[1], tBulgariaControl[2], tBulgariaControl[3] )
				# iOwn == 11, there cities and all the controled, iOwn == 10, there are no cities, iOwn == 0, there is a foreign city
                        	if ( iOwn == 11 ):
                        		self.setGoal( iBulgaria, 1, 1 )
                        else:
                        	if ( self.getGoal( iBulgaria, 1 ) == -1 ):
                        		self.setGoal( iBulgaria, 1, 0 )
                        		
                        if ( iGameTurn == i1401AD and self.getGoal( iBulgaria, 0 ) == -1 ): # see onCityAquire, if no cities lost so far
                        	self.setGoal( iBulgaria, 0, 1 )
                        	
                        if ( iGameTurn == i1449AD+1 and self.getGoal( iBulgaria, 2 ) == -1 ):
                        	self.setGoal( iBulgaria, 2, 0 )
                        	
		elif ( iPlayer == iCordoba and pCordoba.isAlive() ):
			if ( iGameTurn == i1000AD and self.getGoal( iCordoba, 0) == -1 ):
				if ( gc.isLargestCity( con.tCapitals[iCordoba][0], con.tCapitals[iCordoba][1] ) and gc.getMap().plot( con.tCapitals[iCordoba][0], con.tCapitals[iCordoba][1] ).getPlotCity().getOwner() == iCordoba ):
					self.setGoal( iCordoba, 0, 1 )
				else:
					self.setGoal( iCordoba, 0, 0 ) 
		
			if ( iGameTurn == i1300AD+1 and self.getGoal( iCordoba, 1) == -1 ):
				self.setGoal( iCordoba, 1, 0 )
			
			#if ( iGameTurn == i1500AD and self.getGoal( iCordoba, 2 ) == -1 ):
			#	self.setGoal( iCordoba, 2, 1 )
			if ( iGameTurn == i1491AD and self.getGoal(iCordoba,2) == -1 ):
				if (gc.countOwnedCities( iCordoba, tCordobaControl[0][0], tCordobaControl[0][1], tCordobaControl[0][2], tCordobaControl[0][3] ) >= 4 and gc.countOwnedCities( iCordoba, tCordobaControl[1][0], tCordobaControl[1][1], tCordobaControl[1][2], tCordobaControl[1][3] ) >= 4 ):
					self.setGoal( iCordoba, 2, 1 )
				else:
					self.setGoal( iCordoba, 2, 0 )

								
		elif ( iPlayer == iSpain and pSpain.isAlive() ):
			
			if ( iGameTurn == i1600AD and self.getGoal(iSpain, 0) == -1 ):
				if ( gc.doesOwnOrVassalCities( iSpain, tSpainControl[0][0], tSpainControl[0][1], tSpainControl[0][2], tSpainControl[0][3] ) == 11 ) and ( gc.doesOwnOrVassalCities( iSpain, tSpainControl[1][0], tSpainControl[1][1], tSpainControl[1][2], tSpainControl[1][3] ) == 11 ):
					if ( not gc.doesHaveOtherReligion(tSpainControl[0][0], tSpainControl[0][1], tSpainControl[0][2], tSpainControl[0][3], con.iCatholicism)):
						self.setGoal( iSpain, 0, 1 )
					else:
						self.setGoal( iSpain, 0, 0 )
				else:
					self.setGoal( iSpain, 0, 0 )
			
			if ( self.getGoal( iSpain, 1 ) == -1 ):
				iCountCities  = gc.countOwnedCities( iSpain, tSpainControl2[0][0], tSpainControl2[0][1], tSpainControl2[0][2], tSpainControl2[0][3] )
				iCountCities += gc.countOwnedCities( iSpain, tSpainControl2[1][0], tSpainControl2[1][1], tSpainControl2[1][2], tSpainControl2[1][3] ) 
				iCountCities += gc.countOwnedCities( iSpain, tSpainControl2[2][0], tSpainControl2[2][1], tSpainControl2[2][2], tSpainControl2[2][3] ) 
				iCountCities += gc.countOwnedCities( iSpain, tSpainControl2[3][0], tSpainControl2[3][1], tSpainControl2[3][2], tSpainControl2[3][3] ) 
				iCountCities += gc.countOwnedCities( iSpain, tSpainControl2[4][0], tSpainControl2[4][1], tSpainControl2[4][2], tSpainControl2[4][3] ) 
				iCountCities += gc.countOwnedCities( iSpain, tSpainControl2[5][0], tSpainControl2[5][1], tSpainControl2[5][2], tSpainControl2[5][3] ) 
				iCountCities += gc.countOwnedCities( iSpain, tSpainControl2[6][0], tSpainControl2[6][1], tSpainControl2[6][2], tSpainControl2[6][3] )  
				if ( iCountCities >= 4 ):
					self.setGoal( iSpain, 1, 1 )
				
		
			if ( self.getGoal( iSpain, 2 ) == -1 ):
				if ( self.getColonies( iSpain ) > 5 ):
					self.setGoal( iSpain, 2, 1 )
					
		elif ( iPlayer == iNorse and pNorse.isAlive() ):
		
			#if ( iGameTurn == i1000AD and self.getGoal( iNorse, 0 ) == -1 ):
			#	iCount = gc.countOwnedCities( iNorse, tNorseSettle[1][0], tNorseSettle[1][1], tNorseSettle[1][2], tNorseSettle[1][3] ) + gc.countOwnedCities( iNorse, tNorseSettle[2][0], tNorseSettle[2][1], tNorseSettle[2][2], tNorseSettle[2][3] )
			#	if ( iCount >= 3 ):
			#		self.setGoal( iNorse, 0, 1 )
			#	else:
			#		self.setGoal( iNorse, 0, 0 )
			
			if ( iGameTurn <= con.i1050AD and self.getGoal( iNorse, 0 ) == -1 ):
				iCitiesFrance = gc.countOwnedCities( iNorse, tNorseSettle[0][0], tNorseSettle[0][1], tNorseSettle[0][2], tNorseSettle[0][3] ) 
				iCitiesBritain = gc.countOwnedCities( iNorse, tNorseSettle[1][0], tNorseSettle[1][1], tNorseSettle[1][2], tNorseSettle[1][3] ) + gc.countOwnedCities( iNorse, tNorseSettle[2][0], tNorseSettle[2][1], tNorseSettle[2][2], tNorseSettle[2][3] )
				iCitiesIreland = gc.countOwnedCities( iNorse, tNorseSettle[3][0], tNorseSettle[3][1], tNorseSettle[3][2], tNorseSettle[3][3] )
				iCitiesIceland = gc.countOwnedCities( iNorse, tNorseSettle[4][0], tNorseSettle[4][1], tNorseSettle[4][2], tNorseSettle[4][3] )
				iCitiesSicily = gc.countOwnedCities( iNorse, tNorseSettle[5][0], tNorseSettle[5][1], tNorseSettle[5][2], tNorseSettle[5][3] )
				if ( iCitiesFrance >0 and iCitiesBritain >0 and iCitiesIreland >0 and iCitiesIceland >0 and iCitiesSicily > 0):
					self.setGoal( iNorse, 0, 1 )
			
			if (iGameTurn == con.i1050AD+1 and self.getGoal(iNorse,0) == -1):
				self.setGoal( iNorse, 0, 0 )

			if (self.getGoal(iNorse,1) == -1):
				if ( iGameTurn <= i1281AD):
					if ( gc.canSeeAllTerrain( iNorse, con.iTerrainOcean ) ):
						self.setGoal( iNorse, 1, 1 )
				else:
					self.setGoal( iNorse, 1, 0 )
					
		elif ( iPlayer == iVenecia and pVenecia.isAlive() ):
			
			if ( iGameTurn <= i1419AD and self.getGoal( iVenecia, 0 ) == -1 ):
				iDalmatia = gc.doesOwnCities( iVenecia, tVenecianControl[0][0], tVenecianControl[0][1], tVenecianControl[0][2], tVenecianControl[0][3] ) + gc.doesOwnCities( iVenecia, tVenecianControl[1][0], tVenecianControl[1][1], tVenecianControl[1][2], tVenecianControl[1][3] ) + gc.doesOwnCities( iVenecia, tVenecianControl[2][0], tVenecianControl[2][1], tVenecianControl[2][2], tVenecianControl[2][3] ) + gc.doesOwnCities( iVenecia, tVenecianControl[3][0], tVenecianControl[3][1], tVenecianControl[3][2], tVenecianControl[3][3] )
				iGreece = gc.countOwnedCities( iVenecia, tVenecianControl[4][0], tVenecianControl[4][1], tVenecianControl[4][2], tVenecianControl[4][3] ) + gc.countOwnedCities( iVenecia, tVenecianControl[5][0], tVenecianControl[5][1], tVenecianControl[5][2], tVenecianControl[5][3] )
				iCyprus = gc.countOwnedCities( iVenecia, tVenecianControl[6][0], tVenecianControl[6][1], tVenecianControl[6][2], tVenecianControl[6][3] )
				iCrete = gc.countOwnedCities( iVenecia, tVenecianControl[7][0], tVenecianControl[7][1], tVenecianControl[7][2], tVenecianControl[7][3] )
				if ( iDalmatia >= 40 and iGreece >= 1 and iCyprus >= 1 and iCrete >= 1 ):
					self.setGoal( iVenecia, 0, 1 )
			else:
				if ( self.getGoal( iVenecia, 0 ) == -1 ):
					self.setGoal( iVenecia, 0, 0 )
					
			if ( iGameTurn <= i1500AD and self.getGoal( iVenecia, 1 ) == -1 ):
				iRhodes = gc.countOwnedCities( iVenecia, tVenecianControl[8][0], tVenecianControl[8][1], tVenecianControl[8][2], tVenecianControl[8][3] )
				if ( iRhodes == 1 ):
					self.setGoal( iVenecia, 1, 1 )
			else:
				if ( self.getGoal( iVenecia, 1 ) == -1 ):
					self.setGoal( iVenecia, 1, 0 )
					
			if ( self.getGoal( iVenecia, 2 ) == -1 ):
				if ( iGameTurn <= i1570AD and self.getOwnedLuxes( pVenecia ) >= 8 ):
					self.setGoal( iVenecia, 2, 1 )
				elif ( iGameTurn == i1570AD ):
					self.setGoal( iVenecia, 2, 0 )
					
		elif ( iPlayer == iKiev and pKiev.isAlive() ):
		  
			if ( iGameTurn == i1300AD and self.getGoal( iKiev, 0 ) == - 1 ):
				if ( self.getOwnedGrain( pKiev ) >= 10 ):
					self.setGoal( iKiev, 0, 1 )
				else:
					self.setGoal( iKiev, 0, 0 )
			
			if ( iGameTurn == i1350AD and self.getGoal( iKiev, 1 ) == - 1 ):
				if ( gc.doesOwnCities( iKiev, tKievControl[0], tKievControl[1], tKievControl[2], tKievControl[3] ) == 11 ):
					self.setGoal( iKiev, 1, 1 )
				else:
					self.setGoal( iKiev, 1, 0 )
					
			if ( iGameTurn == i1431AD+1 and self.getGoal( iKiev, 2 ) == - 1):
				self.setGoal( iKiev, 2, 0 )
				
		elif ( iPlayer == iHungary and pHungary.isAlive() ):
			
			if ( iGameTurn == i1491AD and self.getGoal( iHungary, 0 ) == -1 ):
				if ( gc.controlMostTeritory( iHungary, tHungarianControl[0], tHungarianControl[1], tHungarianControl[2], tHungarianControl[3] ) ):
					self.setGoal( iHungary, 0, 1 )
				else:
					self.setGoal( iHungary, 0, 0 )
			
			if ( self.getGoal( iHungary, 1 ) == -1 ):
				iCivic = pHungary.getCivics(4)
				if ( iCivic == 24 ):
					self.setGoal( iHungary, 1, 1 )
				else:
					for iPlayer in range( iNumMajorPlayers ):
						pPlayer = gc.getPlayer( iPlayer )
						if ( pPlayer.isAlive() and pPlayer.getCivics(4) == 24 ):
							self.setGoal( iHungary, 1, 0 )
			
			if ( iGameTurn == i1526AD and self.getGoal( iHungary, 2 ) == -1 ):
				iTurkeyCities = 0
				for i in range( 5 ):				
					iTurkeyCities += gc.countOwnedCities( iTurkey, tHungarianControl2[i][0], tHungarianControl2[i][1], tHungarianControl2[i][2], tHungarianControl2[i][3] ) 
				if ( iTurkeyCities == 0 ):
					self.setGoal( iHungary, 2, 1 )
				else:
					self.setGoal( iHungary, 2, 0 )
			
				
		elif ( iPlayer == iGermany and pGermany.isAlive() ):
			
			if ( iGameTurn == i1359AD and self.getGoal( iGermany, 0 ) == -1 ):
				if ( gc.doesOwnCities( iGermany, tGermanyControl[0], tGermanyControl[1], tGermanyControl[2], tGermanyControl[3] ) == 11 ):
					self.setGoal( iGermany, 0, 1 )
				else:
					self.setGoal( iGermany, 0, 0 )
					
			if ( iGameTurn == i1461AD and self.getGoal( iGermany, 1 ) == -1 ):
				iCount = 0
				for iVassal in range( iNumMajorPlayers ):
					pVassal = gc.getPlayer( iVassal )
					if ( iVassal != iGermany and pVassal.isAlive() ):
						if ( gc.getTeam( pVassal.getTeam() ).isVassal( pGermany.getTeam() ) ):
							iCount += 1
				
				if ( iCount >= 3 ):
					self.setGoal( iGermany, 1, 1 )
				else:
					self.setGoal( iGermany, 1, 0 )
					
			if ( iGameTurn == i1540AD and self.getGoal( iGermany, 2 ) == -1 ):
				iGermanPower = teamGermany.getPower(False)
				bPower = True
				for iPlayer in range( iNumMajorPlayers ):
					pPlayer = gc.getPlayer( iPlayer )
					if ( pPlayer.isAlive() and gc.getTeam( pPlayer.getTeam() ).getPower(False) > iGermanPower ):
						bPower = False
						
				if ( bPower ):
					self.setGoal( iGermany, 2, 1 )
				else:
					self.setGoal( iGermany, 2, 0 )
					
		elif ( iPlayer == iPoland and pPoland.isAlive() ):
			
			if ( iGameTurn == i1540AD and self.getGoal( iPoland, 0 ) == - 1 ):
				iPolandPopulation = pPoland.getRealPopulation()
				bMost = True
				for iPlayer in range( iNumMajorPlayers ):
					pPlayer = gc.getPlayer( iPlayer )
					if ( pPlayer.getRealPopulation() > iPolandPopulation ):
						bMost = False
						
				if ( bMost ):
					self.setGoal( iPoland, 0, 1 )
				else:
					self.setGoal( iPoland, 0, 0 )
					
			if ( iGameTurn == i1600AD and self.getGoal( iPoland, 1 ) == -1 ):
				self.setGoal( iPoland, 1, 1 )
				
			#if ( iGameTurn == i1660AD+1 and self.getGoal( iPoland, 2 ) == -1 ):
			#	self.setGoal( iPoland, 2, 0 )
			if ( iGameTurn == con.i1730AD and self.getGoal( iPoland, 2 ) == -1 ):
				iPolishFaith = pPoland.getFaith()
				bMostFaithful = True
				# 3Miro: iNumPlayers - 1 => do not count the Pope
				for iFaithful in range( iNumPlayers - 1 ):
					pFaithful = gc.getPlayer( iFaithful )
					if ( pFaithful.isAlive() and pFaithful.getStateReligion() == con.iCatholicism and pFaithful.getFaith() > iPolishFaith ):
						bMostFaithful = False
				if ( pPoland.getStateReligion() != con.iCatholicism ):
					bMostFaithful = False
				if ( bMostFaithful ):
					self.setGoal( iPoland, 2, 1 )
				else:
					self.setGoal( iPoland, 2, 0 )
					
				
		elif ( iPlayer == iMoscow and pMoscow.isAlive() ):
			
			#if ( iGameTurn == i1401AD and self.getGoal( iMoscow, 0 ) == -1 ):
			#	self.setGoal( iMoscow, 0, 1 )
			if ( iGameTurn == i1482AD and self.getGoal( iMoscow, 0 ) == -1 ):
				if ( gc.countOwnedCities( con.iBarbarian, tMoscowControl[0], tMoscowControl[1], tMoscowControl[2], tMoscowControl[3] ) == 0 ):
					self.setGoal( iMoscow, 0, 1 )
				else:
					self.setGoal( iMoscow, 0, 0 )
				
			if ( iGameTurn == i1600AD and self.getGoal( iMoscow, 1 ) == -1 ):
				if ( pMoscow.getNumCities() >= 15 ):
					self.setGoal( iMoscow, 1, 1 )
				else:
					self.setGoal( iMoscow, 1, 0 )
					
			if ( self.getGoal( iMoscow, 2 ) == -1 ):
				if ( pMoscow.countOwnedBonuses( con.iAccess ) > 0 ):
					self.setGoal( iMoscow, 2, 1 )
				elif ( gc.getMap().plot( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ).getPlotCity().getOwner() == iMoscow ):
					self.setGoal( iMoscow, 2, 1 )
					
		elif ( iPlayer == iGenoa and pGenoa.isAlive() ):
			
			if ( iGameTurn == i1540AD and self.getGoal( iGenoa, 0 ) == -1 ):
				iSardinia = gc.doesOwnCities( iGenoa, tGenoaControl[0][0], tGenoaControl[0][1], tGenoaControl[0][2], tGenoaControl[0][3] )
				iMarseilles = gc.doesOwnCities( iGenoa, tGenoaControl[1][0], tGenoaControl[1][1], tGenoaControl[1][2], tGenoaControl[1][3] )
				iMilano = gc.doesOwnCities( iGenoa, tGenoaControl[2][0], tGenoaControl[2][1], tGenoaControl[2][2], tGenoaControl[2][3] )
				iCyprus = gc.doesOwnCities( iGenoa, tGenoaControl[3][0], tGenoaControl[3][1], tGenoaControl[3][2], tGenoaControl[3][3] )
				iCrete = gc.doesOwnCities( iGenoa, tGenoaControl[4][0], tGenoaControl[4][1], tGenoaControl[4][2], tGenoaControl[4][3] )
				if ( iSardinia == 11 and iMarseilles > 9 and iMilano > 9 and iCyprus == 11 and iCrete == 11 ):
					self.setGoal( iGenoa, 0, 1 )
				else:
					self.setGoal( iGenoa, 0, 0 )
					
			# see cops and buildings for second UHV
			if ( self.getGoal( iGenoa, 1 ) == -1 and self.getGenoaBanks() and self.getGenoaCorporations() >= 2 ):
				self.setGoal( iGenoa, 1, 1 )
					
			if ( iGameTurn == i1640AD and self.getGoal( iGenoa, 2 ) == -1 ):
				iCount = 0
				for iPlayer in range( iNumMajorPlayers ):
					if ( iPlayer != iGenoa and teamGenoa.isOpenBorders( iPlayer ) ):
						iCount += 1
				
				if ( iCount >= 10 ):
					self.setGoal( iGenoa, 2, 1 )
				else:
					self.setGoal( iGenoa, 2, 0 )
					
		elif ( iPlayer == iEngland and pEngland.isAlive() ):
			
			if ( iGameTurn == con.i1452AD and self.getGoal( iEngland, 0 ) == -1 ):
				tVicList = []
				iRegions = 0
				for tregion in tEnglishControl:
					iVic = gc.doesOwnCities( iEngland, tregion[0], tregion[1], tregion[2], tregion[3] )
					tVicList.append(iVic)
					iRegions += 1
				for tregion in tNormanControl:
					iVic = gc.doesOwnCities( iEngland, tregion[0], tregion[1], tregion[2], tregion[3] )
					tVicList.append(iVic)
					iRegions += 1
				#print("Number of Regions",iRegions)
				#print("VicList",tVicList)
				if ( tVicList.count(11) == iRegions):
					self.setGoal( iEngland, 0, 1 )
				else:
					self.setGoal( iEngland, 0, 0 )
					
			if ( self.getGoal( iEngland, 1 ) == -1 ):
				if ( self.getColonies( iEngland ) > 7 ):
					self.setGoal( iEngland, 1, 1 )
					
		elif ( iPlayer == iPortugal and pPortugal.isAlive() ):
			
			#if ( iGameTurn == i1600AD and self.getGoal( iPortugal, 0 ) == -1 ):
			#	if ( pSpain.isAlive() ):
			#		if ( pPortugal.getGold() < pSpain.getGold() ):
			#			self.setGoal( iPortugal, 0, 0 )
			#		else:
			#			iTSpain = 0
			#			iTPortugal = 0
			#			for iTech in range( con.iNumTechs ):
			#				if ( teamSpain.isHasTech( iTech ) ):
			#					iTSpain += 1
			#				if ( teamPortugal.isHasTech( iTech ) ):
			#					iTPortugal += 1
			#			
			#			if ( iTPortugal > iTSpain ):
			#				self.setGoal( iPortugal, 0, 1 )
			#			else:
			#				self.setGoal( iPortugal, 0, 0 )
			#				
			#	else:
			#		self.setGoal( iPortugal, 0, 1 )
					
			if ( iGameTurn == i1640AD and self.getGoal( iPortugal, 1 ) == -1 ):
				self.setGoal( iPortugal, 1, 1 )
				
			if ( self.getGoal( iPortugal, 2 ) == -1 ):
				if ( self.getColonies( iPortugal) > 5 ):
					self.setGoal( iPortugal, 2, 1 )
				
		elif ( iPlayer == iAustria and pAustria.isAlive() ):
			
			if ( iGameTurn == i1600AD and self.getGoal( iAustria, 0 ) == -1 ):
				if ( gc.doesOwnCities( iAustria, tAustrianControl[0], tAustrianControl[1], tAustrianControl[2], tAustrianControl[3] ) == 11 ):
					self.setGoal( iAustria, 0, 1 )
				else:
					self.setGoal( iAustria, 0, 0 )
			
			if ( iGameTurn == i1700AD and self.getGoal( iAustria, 1 ) == -1 ):
				iCount = 0
				for iPlayer in range( iNumMajorPlayers ):
					pPlayer = gc.getPlayer( iPlayer )
					if ( iPlayer != iAustria and pPlayer.isAlive() ):
						if ( gc.getTeam( pPlayer.getTeam() ).isVassal( iAustria ) ):
							iCount += 1
				
				if ( iCount >= 3 ):
					self.setGoal( iAustria, 1, 1 )
				else:
					self.setGoal( iAustria, 1, 0 )
					
			if ( iGameTurn == i1750AD and self.getGoal( iAustria, 2 ) == -1 ):
				iCount = 0
				for iPlayer in range( iNumMajorPlayers ):
					if ( iPlayer != iAustria and teamAustria.isDefensivePact( iPlayer ) ):
						iCount += 1
				
				if ( iCount >= 2 ):
					self.setGoal( iAustria, 2, 1 )
				else:
					self.setGoal( iAustria, 2, 0 )
			
		elif ( iPlayer == iTurkey and pTurkey.isAlive() ):
			
			if ( iGameTurn == i1520AD and self.getGoal( iTurkey, 0 ) == -1 ):
				if ( gc.doesOwnCities( iTurkey, tTurkishControl[0][0], tTurkishControl[0][1], tTurkishControl[0][2], tTurkishControl[0][3] ) == 11 ):
					self.setGoal( iTurkey, 0, 1 )
				else:
					self.setGoal( iTurkey, 0, 0 )
					
			if ( iGameTurn == i1620AD and self.getGoal( iTurkey, 1 ) == -1 ):
				if ( gc.doesOwnCities( iTurkey, tTurkishControl[1][0], tTurkishControl[1][1], tTurkishControl[1][2], tTurkishControl[1][3] ) == 11 ):
					self.setGoal( iTurkey, 1, 1 )
				else:
					self.setGoal( iTurkey, 1, 0 )
					
			if ( iGameTurn <= i1700AD and self.getGoal( iTurkey, 2 ) == -1 ):
				iLevant = gc.doesOwnCities( iTurkey, tTurkishControl[2][0], tTurkishControl[2][1], tTurkishControl[2][2], tTurkishControl[2][3] )
				iEgypt  = gc.doesOwnCities( iTurkey, tTurkishControl[3][0], tTurkishControl[3][1], tTurkishControl[3][2], tTurkishControl[3][3] )
				iVienna = gc.doesOwnCities( iTurkey, tTurkishControl[4][0], tTurkishControl[4][1], tTurkishControl[4][2], tTurkishControl[4][3] )
				if ( iLevant == 11 and iEgypt == 11 and iVienna == 11 ):
					self.setGoal( iTurkey, 2, 1 )
			else:
				if ( self.getGoal( iTurkey, 2 ) == -1 ):
					self.setGoal( iTurkey, 2, 0 )
					
		elif ( iPlayer == iSweden and pSweden.isAlive() ):
			
			if ( iGameTurn == i1600AD and self.getGoal( iSweden, 0 ) == -1 ):
				iSwedenC  = gc.doesOwnCities( iSweden, tSwedishControl[0][0], tSwedishControl[0][1], tSwedishControl[0][2], tSwedishControl[0][3] )
				iFinland = gc.doesOwnCities( iSweden, tSwedishControl[1][0], tSwedishControl[1][1], tSwedishControl[1][2], tSwedishControl[1][3] )
				if ( iSwedenC == 11 and iFinland == 11 ):
					self.setGoal( iSweden, 0, 1 )
				else:
					self.setGoal( iSweden, 0, 0 )
					
			if ( iGameTurn == i1700AD and self.getGoal( iSweden, 1 ) == -1 ):
				self.setGoal( iSweden, 1, 1 )
				
			
			if ( iGameTurn == i1750AD and self.getGoal( iSweden, 2 ) == -1 ):
				iNumCities = pSweden.getNumCities()
				iCount = 0
				for iCity in range(iNumCities):
					pCity = pSweden.getCity(iCity)
					iX = pCity.getX()
					iY = pCity.getY()
					if ( iX >= 70 or iY <= 55 ):
						iCount += 1
				
				if ( iCount >= 3 ):
					self.setGoal( iSweden, 2, 1 )
				else:
					self.setGoal( iSweden, 2, 0 )
					
		elif ( iPlayer == iDutch and pDutch.isAlive() ):
			
			if ( iGameTurn == i1640AD and self.getGoal( iDutch, 0 ) == - 1 ):
				iCount = 0
				for iPlayer in range( iNumMajorPlayers ):
					if ( iPlayer != iDutch and teamDutch.isOpenBorders( iPlayer ) ):
						iCount += 1
				
				if ( iCount >= 10 ):
					self.setGoal( iDutch, 0, 1 )
				else:
					self.setGoal( iDutch, 0, 0 )
					
			if ( iGameTurn <= i1750AD and self.getGoal( iDutch, 1 ) == - 1 ):
				pPlot = gc.getMap().plot( con.tCapitals[iDutch][0], con.tCapitals[iDutch][1])
				if ( pPlot.isCity() ):
					iGMerchant = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_MERCHANT")
					if ( pPlot.getPlotCity().getFreeSpecialistCount(iGMerchant) >= 5 ):
						self.setGoal( iDutch, 1, 1 )
			else:
				if ( self.getGoal( iDutch, 1 ) == - 1 ):
					self.setGoal( iDutch, 1, 0 )
						
			
			if ( self.getGoal( iDutch, 2 ) == -1 ):
				if ( self.getColonies( iDutch ) > 3 ):
					self.setGoal( iDutch, 2, 1 )
					
					
					
                #generic checks
                pPlayer = gc.getPlayer(iPlayer)
                if (pPlayer.isAlive() and iPlayer < iNumMajorPlayers):
                    
                        if (self.get2OutOf3(iPlayer) == False):                              
                                if (utils.countAchievedGoals(iPlayer) == 2):
                                        #intermediate bonus
                                        self.set2OutOf3(iPlayer, True)
                                        if (gc.getPlayer(iPlayer).getNumCities() > 0): #this check is needed, otherwise game crashes
                                                capital = gc.getPlayer(iPlayer).getCapitalCity()
                                                # 3Miro: Golden Age after 2/3 victories
                                                capital.setHasRealBuilding(con.iTriumphalArch, True)
                                                if (pPlayer.isHuman()):
                                                        CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_VICTORY_INTERMEDIATE", ()), "", 0, "", ColorTypes(con.iPurple), -1, -1, True, True)
                                                        
                                                        for iCiv in range(iNumPlayers):
                                                                if (iCiv != iPlayer):
                                                                        pCiv = gc.getPlayer(iCiv)
                                                                        if (pCiv.isAlive()):
                                                                                iAttitude = pCiv.AI_getAttitude(iPlayer)
                                                                                if (iAttitude != 0):
                                                                                        pCiv.AI_setAttitudeExtra(iPlayer, iAttitude-1) #da controllare

                                                        iWarCounter = 0
                                                        iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'civs')
                                                        for i in range( iRndnum, iNumPlayers + iRndnum ):
                                                                iCiv = i % iNumPlayers
                                                                pCiv = gc.getPlayer(iCiv)
                                                                if ((iCiv == con.iPope) and pCiv.isAlive() and pCiv.canContact(iPlayer)):                                                                
                                                                        if (pCiv.AI_getAttitude(iPlayer) < 0):
                                                                                teamCiv = gc.getTeam(pCiv.getTeam())
                                                                                if (not teamCiv.isAtWar(iPlayer)):
                                                                                        teamCiv.declareWar(iPlayer, True, -1)
                                                                                        iWarCounter += 1
                                                                                        if (iWarCounter == 2):
                                                                                                break
                                

                        if (gc.getGame().getWinner() == -1):                              
                                if (self.getGoal(iPlayer, 0) == 1 and self.getGoal(iPlayer, 1) == 1 and self.getGoal(iPlayer, 2) == 1):
                                        gc.getGame().setWinner(iPlayer, 7) #Historical Victory




        def onCityBuilt(self, city, iPlayer): #see onCityBuilt in CvRFCEventHandler
		if ( iPlayer == iPortugal and self.getGoal( iPortugal, 0 ) == -1 ):
			iIslands = gc.countOwnedCities( iPortugal, tPortugalControl[0][0], tPortugalControl[0][1], tPortugalControl[0][2], tPortugalControl[0][3] )
			iAfrica  = gc.countOwnedCities( iPortugal, tPortugalControl[1][0], tPortugalControl[1][1], tPortugalControl[1][2], tPortugalControl[1][3] ) 
			iAfrica += gc.countOwnedCities( iPortugal, tPortugalControl[2][0], tPortugalControl[2][1], tPortugalControl[2][2], tPortugalControl[2][3] )  
			if ( iIslands >= 3 and iAfrica >= 2 ):
				self.setGoal( iPortugal, 0, 1 )
		

                                                
                        
        def onReligionFounded(self, iReligion, iFounder):
		pass


        def onCityAcquired(self, owner, playerType, bConquest):
        	# 3Miro: everything in this file si mine as well
        	if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return
		
	        iPlayer = owner
                iGameTurn = gc.getGame().getGameTurn()
        
		if (iPlayer == iBulgaria): # 3Miro: 0th Bulgarian goal, no lost city
                        if (pBulgaria.isAlive()):
                                if (bConquest):
                                        if (self.getGoal(iBulgaria, 0) == -1):
                                        	if (playerType == iBarbarian or playerType == iTurkey or playerType == iByzantium ):
                                                        self.setGoal(iBulgaria, 0, 0)
                elif (iPlayer == iBurgundy):
                	if ( pBurgundy.isAlive()):
                		if (bConquest):
                			if ( self.getGoal(iBurgundy, 1) == -1 ):
                				if(playerType == iGermany or playerType == iFrankia ):
                					self.setGoal(iBurgundy,1,0 )
                					
                elif ( iPlayer == iPoland ):
                	if ( pPoland.isAlive() ):
                		if ( bConquest ):
                			if ( self.getGoal( iPoland, 1 ) == -1 ):
                				# 3Miro: Change UHV to "any" city
                				#if ( playerType == iGermany or playerType == iMoscow or playerType == iKiev ):
                				self.setGoal( iPoland, 1, 0 )
                					
                elif ( iPlayer == iMoscow ):
                	if ( pMoscow.isAlive() ):
                		if ( bConquest ):
                			if ( self.getGoal( iMoscow, 0 ) == -1 ):
                				if ( playerType == iBarbarian ):
                					self.setGoal( iMoscow, 0, 0 )
                					
                elif ( iPlayer == iPortugal ):
                	if ( pPortugal.isAlive() ):
                		if ( bConquest ):
                			if ( self.getGoal( iPortugal, 1 ) == -1 ):
                				self.setGoal( iPortugal, 1, 0 )
                				
                elif ( iPlayer == iSweden ):
                	if ( pSweden.isAlive() ):
                		if ( bConquest ):
                			if ( self.getGoal( iSweden, 1 ) == -1 ):
                				if ( playerType == iMoscow or playerType == iPoland ):
                					self.setGoal( iSweden, 1, 0 )
               
       


        def onCityRazed(self, iPlayer):
        	print("City Razed",iPlayer)
		if (iPlayer == iNorse): # Sedna17: Norse goal of razing 10? cities
                        if (pNorse.isAlive()):
				if (self.getGoal(iNorse,2) == -1):
					ioldrazed = self.getNorseRazed()
					print("Norse Cities Razed =",ioldrazed)
					if (ioldrazed >= 9):
						self.setGoal(iNorse,2,1)
					else:
						self.setNorseRazed(ioldrazed+1)
        	pass
                                                


        def onTechAcquired(self, iTech, iPlayer):
        	if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return
        
        	#if ( iTech == con.iScientificMethod ):
        	#	if ( iPlayer == iCordoba ):
        	#		if ( self.getGoal( iCordoba, 2 ) == -1 ):
        	#			self.setGoal( iCordoba, 2, 1 )
        	#	else:
        	#		if ( self.getGoal( iCordoba, 2 ) == -1 ):
        	#			self.setGoal( iCordoba, 2, 0 )
		if ( iTech == con.iIndustrialTech ):
			if ( iPlayer == iEngland ):
				if ( self.getGoal( iEngland, 2 ) == -1 ):
					self.setGoal( iEngland, 2, 1 )
			else:
				if ( self.getGoal( iEngland, 2 ) == -1 ):
					self.setGoal( iEngland, 2, 0 )


        def onBuildingBuilt(self, iPlayer, iBuilding):
        	# 3Miro: everything is coded by me
        	if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

		iGameTurn = gc.getGame().getGameTurn()
		
		if ( iPlayer == iBulgaria ): # Buildings Goal 2
			if ( pBulgaria.isAlive() ):
				if (self.getGoal(iBulgaria, 2) == -1):
					if ( iGameTurn <= i1600AD ):
						if ( iBuilding == con.iOrthodoxMonastery or iBuilding == con.iOrthodoxCathedral or iBuilding == con.iOrthodoxScriptorium ):
							iNumCities = pBulgaria.getNumCities()
							if ( iNumCities > 7 ): # if there are enough cities
								iCathedralCounter = 0
								iMonasteryCounter = 0
								iLibraryCounter = 0
								for iCity in range(iNumCities):
									pCity = pBulgaria.getCity(iCity)
                                        	                        if (pCity.hasBuilding(con.iOrthodoxCathedral)):
                                        	                                iCathedralCounter += 1
                                        	                        if (pCity.hasBuilding(con.iOrthodoxMonastery)):
                                        	                                iMonasteryCounter += 1
                                        	                        if (pCity.hasBuilding(con.iOrthodoxScriptorium)):
                                        	                                iLibraryCounter += 1
                                        	                if ( iCathedralCounter >= 2 and iMonasteryCounter >= 8 and iLibraryCounter >= 8 ):
                                        	                	self.setGoal( iBulgaria, 2, 1 )
                
                
                elif ( iPlayer == iKiev ):
                	if ( pKiev.isAlive() ):
                		if ( self.getGoal( iKiev, 2 ) == -1 ):
                			if ( iGameTurn <= i1600AD ):
                				if ( iBuilding == con.iOrthodoxMonastery or iBuilding == con.iOrthodoxCathedral ):
							iNumCities = pKiev.getNumCities()
							if ( iNumCities > 7 ): # if there are enough cities
								iCathedralCounter = 0
								iMonasteryCounter = 0
								for iCity in range(iNumCities):
									pCity = pKiev.getCity(iCity)
                                        	                        if (pCity.hasBuilding(con.iOrthodoxCathedral)):
                                        	                                iCathedralCounter += 1
                                        	                        if (pCity.hasBuilding(con.iOrthodoxMonastery)):
                                        	                                iMonasteryCounter += 1
                                        	                if ( iCathedralCounter >= 2 and iMonasteryCounter >= 8 ):
                                        	                	self.setGoal( iKiev, 2, 1 ) 
                # 3Miro: Polish UHV chnaged                 	                	
                #elif ( iPlayer == iPoland ):
                #	if ( pPoland.isAlive() ):
                #		if ( self.getGoal( iPoland, 2 ) == -1 ):
                #			if ( iGameTurn <= i1700AD ):
                #				if ( iBuilding == con.iCatholicMonastery or iBuilding == con.iCatholicCathedral ):
                #					iNumCities = pPoland.getNumCities()
                #					if ( iNumCities > 7 ):
		#						iCathedralCounter = 0
		#						iMonasteryCounter = 0
		#						for iCity in range(iNumCities):
		#							pCity = pPoland.getCity(iCity)
                #                        	                        if (pCity.hasBuilding(con.iCatholicCathedral)):
                #                        	                                iCathedralCounter += 1
                #                        	                        if (pCity.hasBuilding(con.iCatholicMonastery)):
                #                        	                                iMonasteryCounter += 1
                #                        	                if ( iCathedralCounter >= 2 and iMonasteryCounter >= 8 ):
                #                        	                	self.setGoal( iPoland, 2, 1 )                 						

		elif ( iPlayer == iGenoa ): # Buildings Goal 2
			if ( pGenoa.isAlive() ):
				if ( not self.getGenoaBanks() ):
					if ( iBuilding == con.iGenoaMint ):
						iNumCities = pGenoa.getNumCities()
						if ( iNumCities > 7 ): # if there are enough cities
							iBankCounter = 0
							for iCity in range(iNumCities):
								pCity = pGenoa.getCity(iCity)
                                        	                if (pCity.hasBuilding(con.iGenoaMint)):
                                        	                	iBankCounter += 1
							if ( iBankCounter >= 8 ):
								self.setGenoaBanks( 1 )

		if (iBuilding == con.iLaMezquita or iBuilding == con.iAlhambra or iBuilding == con.iGardensAlAndalus):
			print("I see a wonder being built")
			if (iPlayer == iCordoba):
				if (pCordoba.isAlive()):
					if (self.getGoal(iCordoba, 1) == -1):
						iWondersBuilt = self.getWondersBuilt(iCordoba)
						print("Cordoba has:",iWondersBuilt,"Wonders")
						self.setWondersBuilt(iCordoba, iWondersBuilt + 1)
						if (iWondersBuilt == 2):                                    
							self.setGoal(iCordoba, 1, 1)
			else:
				if (pCordoba.isAlive()):
					if (self.getGoal(iCordoba, 1) == -1):
						self.setGoal(iCordoba,1,0)

                            
        def onProjectBuilt(self, iPlayer, iProject):
		if ( self.isProjectAColony( iProject )):
			self.changeColonies( iPlayer, 1 )

	def onCorporationFounded(self, iPlayer ):
		self.setCorporationsFounded( self.getCorporationsFounded() + 1 )
		if ( iPlayer == iGenoa ):
			self.setGenoaCorporations( self.getGenoaCorporations() + 1 )
		if ( self.getCorporationsFounded() == 7 and self.getGenoaCorporations() < 2 ):
			self.setGoal( iGenoa, 1, 0 )	


        def onCombatResult(self, argsList):
		pass
                                        


        def calculateTopCityCulture(self, x, y):
                pass


        def calculateTopCityPopulation(self, x, y):
                pass

	def getOwnedLuxes( self, pPlayer ):
		iCount = 0
		iCount += pPlayer.countOwnedBonuses( con.iSheep )
		iCount += pPlayer.countOwnedBonuses( con.iDye )
		iCount += pPlayer.countOwnedBonuses( con.iFur )
		iCount += pPlayer.countOwnedBonuses( con.iGems )
		iCount += pPlayer.countOwnedBonuses( con.iGold )
		iCount += pPlayer.countOwnedBonuses( con.iIncense )
		iCount += pPlayer.countOwnedBonuses( con.iIvory )
		iCount += pPlayer.countOwnedBonuses( con.iSilk )
		iCount += pPlayer.countOwnedBonuses( con.iSilver )
		iCount += pPlayer.countOwnedBonuses( con.iSpices )
		iCount += pPlayer.countOwnedBonuses( con.iWine )
		iCount += pPlayer.countOwnedBonuses( con.iHoney )
		iCount += pPlayer.countOwnedBonuses( con.iWhale )
		iCount += pPlayer.countOwnedBonuses( con.iRelic )
		iCount += pPlayer.countOwnedBonuses( con.iCotton )
		iCount += pPlayer.countOwnedBonuses( con.iCoffee )
		iCount += pPlayer.countOwnedBonuses( con.iTea )
		iCount += pPlayer.countOwnedBonuses( con.iTobacco )
		return iCount

	def getOwnedGrain( self, pPlayer ):
		iCount = 0
		iCount += pPlayer.countOwnedBonuses( con.iWheat )
		iCount += pPlayer.countOwnedBonuses( con.iBarley )
		return iCount

	def isProjectAColony( self, iProject ):
		if (iProject >= con.iNumNotColonies): 
			return True
		else:
			return False
