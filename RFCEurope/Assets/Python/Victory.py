# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
import cPickle as pickle
import Consts as con
import XMLConsts as xml
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
iLithuania = con.iLithuania
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
pLithuania = gc.getPlayer(iLithuania)
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
teamLithuania = gc.getTeam(pLithuania.getTeam())
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

# 3Miro: areas
#tBurgundyControl = (( 46, 40, 52, 53 ),(44, 33, 48,39))
#tByzantineControl = ( 68, 15, 99, 26 )
##tFrankControl = ((35,31,41,35),(37,36,42,40),(44,33,48,42),(52,40,57,48),(49,31,57,37)) # Northeast Spain, Southwest France, Rhone, W Germany, Northern Italy
#tArabiaControl = ( (93, 0, 99, 17), (76, 0, 92, 4), (31, 0, 54, 21), (55, 0, 88, 9) ) # Levant and Allepo and Antioch, Egypt, Egypt and Libia, Algeria and Tunisia
#tBulgariaControl = ( 66, 23, 82, 32 )
##tCordobaControl = (( 20,24,40,40 ),( 11,14,47,23 )) # Iberia, North-West Africa
#tSpainControl = (( 20, 24, 35, 40 ),(36, 30, 41, 35)) # Iberia
#tSpainControl2 = ((15,14,48,23),(49,6,52,18),(49,22,50,29),(54,16,58,19),(59,19,64,27),(51,25,58,33),(49,43,58,39) ) # Africa x2, Islands (Corsica + Sardines), Sicily, Italy x3
#tNorseSettle = ( (35, 46, 46, 50 ), (39, 52, 45, 67 ), (35, 52, 38, 56 ), (31, 57, 37, 62 ), ( 0, 69, 4, 72 ), ( 54, 16, 58, 19)  ) # North France, Britain, Britain, Ireland, Iseland, Sicily
##tVenecianControl = ( (59, 32, 61, 36), (61, 28, 64, 32), ( 65, 17, 67, 29 ), ( 67, 23, 81, 25 ), ( 67, 14, 73, 22 ), ( 88, 11, 91, 13 ), ( 71, 10, 75, 10 ), ( 78, 11, 79, 12 ) ) # 3x Dalmatian Coast, 2x Main Land Greece, Cyprus, Crete, Rhodes
#tVenecianControl = ( (56, 33, 60, 36), (61, 29, 62, 34), (63, 25, 65, 30), (66, 21, 67, 27), ( 67, 23, 81, 25 ), ( 67, 14, 73, 22 ), ( 88, 11, 91, 13 ), ( 71, 10, 75, 10 ), ( 78, 11, 79, 12 ) ) # 4x Dalmatian Coast, 2x Main Land Greece, Cyprus, Crete, Rhodes
#tKievControl = (83, 32, 99, 39 )
#tHungarianControl = ( 0, 23, 99, 72 )
#tHungarianControl2 = ( (20,24,48,72),(49,30,99,72),(54,20,76,29),(60,14,75,19),(81,29,77,23) )
#tGermanyControl = ( 49, 40, 54, 53 )
#tMoscowControl = ( 77, 32, 99, 70 )
##tGenoaControl = (( 49, 22, 50, 25 ), ( 44, 32, 46, 34 ), ( 51, 36, 53, 38 ), ( 88, 11, 91, 13 ), ( 72, 10, 75, 10 ), (86, 32, 91, 35 ) ) #Sardinia, Marseilles, Milano, Cyprus, Crete, Crimea
#tPolandControl = ((58, 38, 64, 44),(65, 32, 77, 40),(78, 35, 94, 47),(72,48,82,63)) #Bohemia, Hungary, Ukraine, Lithuania
#tBaltic = (61,52,79,72)
#tBlackSea = (78,24,99,39)

#tGenoaControl = (( 49, 22, 50, 25 ), ( 44, 32, 46, 34 ), ( 51, 36, 53, 38 ), ( 88, 11, 91, 13 ), ( 72, 10, 75, 10 ) ) #Sardinia, Marseilles, Milano, Cyprus, Crete 
#tEnglishControl = ((39, 61, 44, 67), (31,57,37,62), (37,55,40,57)) # Scotland, Ireland, Wales
#tPortugalControl = ((1,15,8,39),(7,0,27,24),(4,0,6,7)) # Islands, Africa x 2
#tNormanControl = ((35,40,38,47), (39,46,45,50)) # Bits of France (redurced areas to 2, should be more easy to recognize now
#tAustrianControl = ( 58, 33, 70, 38 )
#tTurkishControl = (( 77, 14, 99, 26 ), ( 65, 14, 80, 29 ), (93, 0, 99, 17), (76, 0, 92, 4), ( 60, 33, 63, 41 ) ) # Constantinople Area and Anatolia, Balkans and Peloponnesian, Levant, Egypt, Vienna
#tSwedishControl = (( 60, 56, 68, 72 ), ( 69, 63, 77, 72 ),(59, 43, 90, 55) ) # Sweden, Finland/Estland and east Germany through Central Russia

# ------------------- NEW UHV CONDITIONS
tByzantumControl = [ xml.iP_Colonea, xml.iP_Antiochia, xml.iP_Charsiadon, xml.iP_Cilicia, xml.iP_Armeniakon, xml.iP_Anatolikon, xml.iP_Paphlagonia, xml.iP_Thrakesion, xml.iP_Opsikion, xml.iP_Constantinople ]
tFrankControl = [ xml.iP_Bavaria, xml.iP_Saxony, xml.iP_IleDeFrance, xml.iP_Aquitania, xml.iP_Provence, xml.iP_Burgundy, xml.iP_Orleans, xml.iP_Champagne, xml.iP_Catalonia, xml.iP_Lombardy, xml.iP_Tuscany ] # Update this with the Province keys
tArabiaControlI = [ xml.iP_Egypt, xml.iP_Antiochia, xml.iP_Syria, xml.iP_Lebanon, xml.iP_Arabia, xml.iP_Jerusalem ]
tArabiaControlII = [ xml.iP_Oran, xml.iP_Algiers, xml.iP_Ifriqiya, xml.iP_Cyrenaica, xml.iP_Tripolitania, xml.iP_Egypt, xml.iP_Antiochia, xml.iP_Syria, xml.iP_Lebanon, xml.iP_Arabia, xml.iP_Jerusalem]
tBulgariaControl = [ xml.iP_Constantinople, xml.iP_Thessaloniki, xml.iP_Serbia, xml.iP_Thrace, xml.iP_Macedonia, xml.iP_Moesia, xml.iP_Arberia ]
tCordobaWonders = [ xml.iAlhambra, xml.iLaMezquita, xml.iGardensAlAndalus ]
tCordobaIslamize = [ xml.iP_GaliciaSpain, xml.iP_Castile, xml.iP_Leon, xml.iP_Lusitania, xml.iP_Catalonia, xml.iP_Aragon, xml.iP_Valencia, xml.iP_Andalusia ]
tNorseControl = [ xml.iP_Sicily, xml.iP_Iceland, xml.iP_Yorkshire, xml.iP_Scotland, xml.iP_Normandy, xml.iP_Ireland, xml.iP_Crimea ]
#tVenetianControl = [ xml.iP_Morea, xml.iP_Epirus, xml.iP_Dalmatia, xml.iP_Verona, xml.iP_Crete, xml.iP_Cyprus ]
tVenetianControl = [ xml.iP_Epirus, xml.iP_Dalmatia, xml.iP_Verona, xml.iP_Arberia ]
tBurgundyControl = [ xml.iP_Flanders, xml.iP_Provence, xml.iP_Burgundy, xml.iP_Champagne, xml.iP_Lorraine ]
tBurgundyOutrank = [ iFrankia, iEngland, iGermany ]
tGermanyControl = [ xml.iP_Lorraine, xml.iP_Swabia, xml.iP_Saxony, xml.iP_Bavaria, xml.iP_Franconia, xml.iP_Brandenburg ]
tKievControl = [ xml.iP_Moldova, xml.iP_Kiev, xml.iP_Crimea, xml.iP_Zaporizhia, xml.iP_Sloboda, xml.iP_Pereyaslavl, xml.iP_Chernigov, xml.iP_Podolia, xml.iP_WhiteRus ]
tHungarynControl = [ xml.iP_Thrace, xml.iP_Moesia, xml.iP_Macedonia, xml.iP_Thessaloniki, xml.iP_Wallachia, xml.iP_Thessaly, xml.iP_Epirus, xml.iP_Arberia, xml.iP_Serbia, xml.iP_Bosnia, xml.iP_Dalmatia, xml.iP_Croatia ]
tSpainConvert = [ xml.iP_GaliciaSpain, xml.iP_Castile, xml.iP_Leon, xml.iP_Lusitania, xml.iP_Catalonia, xml.iP_Aragon, xml.iP_Valencia, xml.iP_Andalusia ]
tPolishControl = [ xml.iP_Bohemia, xml.iP_Moravia, xml.iP_UpperHungary, xml.iP_Hungary, xml.iP_Lithuania, xml.iP_Brest, xml.iP_Podolia, xml.iP_Kiev ]
tGenoaControl = [ xml.iP_Lombardy, xml.iP_Sardinia, xml.iP_Cyprus, xml.iP_Crete ]
tEnglandControl = [ xml.iP_London, xml.iP_Wales, xml.iP_Wessex, xml.iP_Scotland, xml.iP_EastAnglia, xml.iP_Yorkshire, xml.iP_Ireland, xml.iP_Normandy, xml.iP_Bretagne, xml.iP_IleDeFrance, xml.iP_Aquitania, xml.iP_Orleans ]
tPortugalControlI = [ xml.iP_Azores, xml.iP_Canaries ]
tPortugalControlII = [ xml.iP_Morocco, xml.iP_Tetouan, xml.iP_Oran ]
tLithuaniaControl = [ xml.iP_Lithuania, xml.iP_GreaterPoland, xml.iP_LesserPoland, xml.iP_Pomerania, xml.iP_Masovia, xml.iP_Suvalkija, xml.iP_Livonia, xml.iP_Novgorod, xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_WhiteRus, xml.iP_Pereyaslavl, xml.iP_Kiev, xml.iP_GaliciaPoland, xml.iP_Sloboda ]
tAustriaControl = [ xml.iP_Hungary, xml.iP_UpperHungary, xml.iP_Austria, xml.iP_Salzburg, xml.iP_Transylvania, xml.iP_Pannonia, xml.iP_Moravia, xml.iP_Bohemia ]
tOttomanControlI = [ xml.iP_Serbia, xml.iP_Bosnia, xml.iP_Macedonia, xml.iP_Thrace, xml.iP_Moesia, xml.iP_Constantinople, xml.iP_Arberia, xml.iP_Epirus, xml.iP_Thessaloniki, xml.iP_Thessaly, xml.iP_Morea ]
tOttomanControlII = [ xml.iP_Colonea, xml.iP_Antiochia, xml.iP_Charsiadon, xml.iP_Cilicia, xml.iP_Armeniakon, xml.iP_Anatolikon, xml.iP_Paphlagonia, xml.iP_Thrakesion, xml.iP_Opsikion, xml.iP_Syria, xml.iP_Lebanon, xml.iP_Jerusalem, xml.iP_Egypt ]
tOttomanControlIII = [ xml.iP_Austria ]
tMoscowControl = [ xml.iP_Donets, xml.iP_Kuban, xml.iP_Zaporizhia, xml.iP_Sloboda, xml.iP_Kiev, xml.iP_Moldova, xml.iP_Crimea, xml.iP_Pereyaslavl, xml.iP_Chernigov, xml.iP_Simbirsk, xml.iP_NizhnyNovgorod, xml.iP_Vologda, xml.iP_Rostov, xml.iP_Novgorod, xml.iP_Karelia, xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_WhiteRus, xml.iP_Volhynia, xml.iP_Podolia, xml.iP_Moscow, xml.iP_Murom ]
tSwedenControlI = [ xml.iP_Gotaland, xml.iP_Svealand, xml.iP_Norrland, xml.iP_Finland ]
tSwedenControlII = [ xml.iP_Saxony, xml.iP_Brandenburg, xml.iP_Pomerania, xml.iP_GreaterPoland, xml.iP_Masovia, xml.iP_Suvalkija, xml.iP_Lithuania, xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_Murom, xml.iP_Chernigov, xml.iP_Moscow, xml.iP_Novgorod, xml.iP_Rostov ]

tOLDHungarianControl = ( 0, 23, 99, 72 )

totalLand = gc.getMap().getLandPlots()

class Victory:

        def __init__(self ):
                self.switchConditionsPerCiv = { iByzantium : self.checkByzantium,
                                                iFrankia : self.checkFrankia,
                                                iArabia : self.checkArabia,
                                                iBulgaria : self.checkBulgaria,
                                                iCordoba : self.checkCordoba,
                                                iNorse : self.checkNorse,
                                                iVenecia : self.checkVenecia,
                                                iBurgundy : self.checkBurgundy,
                                                iGermany : self.checkGermany,
                                                iKiev : self.checkKiev,
                                                iHungary : self.checkHungary,
                                                iSpain : self.checkSpain,
                                                iPoland : self.checkPoland,
                                                iGenoa : self.checkGenoa,
                                                iEngland : self.checkEngland,
                                                iPortugal : self.checkPortugal,
                                                iLithuania : self.checkLithuania,
                                                iAustria : self.checkAustria,
                                                iTurkey : self.checkTurkey,
                                                iMoscow : self.checkMoscow,
                                                iSweden : self.checkSweden,
                                                iDutch : self.checkDutch,
                                                }
     
##################################################
### Secure storage & retrieval of script data ###
################################################

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
                # we use Python version of Switch statement, it is supposed to be better, now all condition checks are in separate functions
                pPlayer = gc.getPlayer(iPlayer)
                if ( iPlayer < iPope and pPlayer.isAlive() ): # don't count the Pope
                        self.switchConditionsPerCiv[iPlayer](iGameTurn)

                #generic checks
                #pPlayer = gc.getPlayer(iPlayer)
                if (pPlayer.isAlive() and iPlayer < iNumMajorPlayers):
                        if ( not pPlayer.getUHV2of3() ):
                                if (utils.countAchievedGoals(iPlayer) == 2):
                                        #intermediate bonus
                                        pPlayer.setUHV2of3( True )
                                        if (pPlayer.getNumCities() > 0): #this check is needed, otherwise game crashes
                                                capital = pPlayer.getCapitalCity()
                                                # 3Miro: Golden Age after 2/3 victories
                                                capital.setHasRealBuilding(xml.iTriumphalArch, True)
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
                                                                if ((iCiv != con.iPope) and pCiv.isAlive() and pCiv.canContact(iPlayer)):                                                                
                                                                        if (pCiv.AI_getAttitude(iPlayer) < 0):
                                                                                teamCiv = gc.getTeam(pCiv.getTeam())
                                                                                if (not teamCiv.isAtWar(iPlayer)):
                                                                                        teamCiv.declareWar(iPlayer, True, -1)
                                                                                        iWarCounter += 1
                                                                                        if (iWarCounter == 2):
                                                                                                break


                if (gc.getGame().getWinner() == -1):
                        if ( pPlayer.getUHV(0) == 1 and pPlayer.getUHV(1) == 1 and pPlayer.getUHV(2) == 1):
                                gc.getGame().setWinner(iPlayer, 7) #Historical Victory


        def onCityBuilt(self, city, iPlayer): #see onCityBuilt in CvRFCEventHandler
                #if ( iPlayer == iPortugal and self.getGoal( iPortugal, 0 ) == -1 ):
                        #iIslands = gc.countOwnedCities( iPortugal, tPortugalControl[0][0], tPortugalControl[0][1], tPortugalControl[0][2], tPortugalControl[0][3] )
                        #iAfrica  = gc.countOwnedCities( iPortugal, tPortugalControl[1][0], tPortugalControl[1][1], tPortugalControl[1][2], tPortugalControl[1][3] ) 
                        #iAfrica += gc.countOwnedCities( iPortugal, tPortugalControl[2][0], tPortugalControl[2][1], tPortugalControl[2][2], tPortugalControl[2][3] )  
                        #if ( iIslands >= 3 and iAfrica >= 2 ):
                                #self.setGoal( iPortugal, 0, 1 )
                if ( iPlayer == iPortugal and pPortugal.getUHV( 0 ) == -1 ):
                        iProv = city.getProvince()
                        if ( iProv in tPortugalControlI or iProv in tPortugalControlII ):
                                iCounter = pPortugal.getUHVCounter( 0 )
                                iIslands = iCounter % 100
                                iAfrica = iCounter / 100
                                if ( iProv in tPortugalControlI ):
                                        iIslands += 1
                                else:
                                        iAfrica += 1
                                if ( iIslands >= 3 and iAfrica >= 2 ):
                                        pPortugal.setUHV( 0, 1 )
                                pPortugal.setUHVCounter( 0, iAfrica * 100 + iIslands )

        def onReligionFounded(self, iReligion, iFounder):
                pass


        def onCityAcquired(self, owner, playerType, bConquest):
                # 3Miro: almost everything in this file is mine as well
                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                iPlayer = owner
                iGameTurn = gc.getGame().getGameTurn()
                
                if ( iPlayer == iBulgaria and pBulgaria.isAlive() ):
                        if (playerType == iBarbarian or playerType == iTurkey or playerType == iByzantium ):
                                pBulgaria.setUHV( 2, 0 )

                elif ( iPlayer == iPortugal and pPortugal.isAlive() ):
                        if ( bConquest ):
                                if ( pPortugal.getUHV( 1 ) == -1 ):
                                        pPortugal.setUHV( 1, 0 )

                elif ( iPlayer == iSweden and pSweden.isAlive() ):
                        if ( bConquest ):
                                if ( pSweden.getUHV( 1 ) == -1 ):
                                        if ( playerType == iMoscow or playerType == iPoland ):
                                                pSweden.setUHV( 1, 0 )
                if ( playerType == iSpain ):
                        if ( gc.getPlayer( playerType ).getStateReligion() == xml.iProtestantism ):
                                iConqueredCities = pSpain.getUHVCounter( 2 ) + 1
                                pSpain.setUHVCounter( 2, iConqueredCities )
                                if ( pSpain.getUHV( 2 ) == - 1 and iConqueredCities >= 3 ):
                                        pSpain.setUHV( 2, 1 )

        def onCityRazed(self, iPlayer,city):
                if (iPlayer == iNorse): # Sedna17: Norse goal of razing 10? cities
                        if ( pNorse.isAlive() and pNorse.getUHV( 2 ) == -1):
                                if ( city.getOwner() < iNumPlayers ):
                                        #ioldrazed = self.getNorseRazed()
                                        #if (ioldrazed >= 9):
                                                #self.setGoal(iNorse,2,1)
                                        #else:
                                                #self.setNorseRazed(ioldrazed+1)
                                        iRazed = pNorse.getUHVCounter( 2 ) + 1
                                        pNorse.setUHVCounter( 2, iRazed )
                                        if ( iRazed >= 6 ):
                                                pNorse.setUHV( 2, 1 )


        def onTechAcquired(self, iTech, iPlayer):
                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                if ( iTech == xml.iIndustrialTech ):
                        if ( pEngland.getUHV( 2 ) == -1 ):
                                if ( iPlayer == iEngland ):
                                        pEngland.setUHV( 2, 1 )
                                else:
                                        pEngland.setUHV( 2, 0 )

        def onBuildingBuilt(self, iPlayer, iBuilding):
                # 3Miro: everything is coded by me
                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                iGameTurn = gc.getGame().getGameTurn()

                if ( iPlayer == iKiev ):
                        if ( pKiev.isAlive() and pKiev.getUHV( 2 ) == -1 ):
                                if ( iBuilding == xml.iOrthodoxMonastery or iBuilding == xml.iOrthodoxCathedral ):
                                        iBuildSoFar = pKiev.getUHVCounter( 2 )
                                        iCathedralCounter = iBuildSoFar % 100
                                        iMonasteryCounter = iBuildSoFar / 100
                                        if ( iBuilding == xml.iOrthodoxMonastery ):
                                                iMonasteryCounter += 1
                                        else:
                                                iCathedralCounter += 1
                                        if ( iCathedralCounter >= 2 and iMonasteryCounter >= 8 ):
                                                pKiev.setUHV( 2, 1 )
                                        pKiev.setUHVCounter( 2, 100 * iMonasteryCounter + iCathedralCounter )
                # Sedna17: Polish UHV changed again                 	                	
                elif ( iPlayer == iPoland ):
                        if ( pPoland.isAlive() and pPoland.getUHV( 2 ) == -1 ):
                                lBuildingList = [xml.iCatholicCathedral,xml.iOrthodoxCathedral,xml.iProtestantCathedral,xml.iJewishQuarter]
                                if ( iBuilding in lBuildingList):
                                        iCounter = pPoland.getUHVCounter( 2 )
                                        iCathCath = ( iCounter / 10000 ) % 10
                                        iOrthCath = ( iCounter / 1000 ) % 10 
                                        iProtCath = ( iCounter / 100 ) % 10
                                        iJewishQu = iCounter % 100
                                        if ( iBuilding == xml.iCatholicCathedral ):
                                                iCathCath += 1
                                        elif ( iBuilding == xml.iOrthodoxCathedral ):
                                                iOrthCath += 1
                                        elif ( iBuilding == xml.iProtestantCathedral ):
                                                iProtCath += 1
                                        elif ( iBuilding == xml.iJewishQuarter ):
                                                iJewishQu += 1
                                        if ( iCathCath >= 3 and iOrthCath >= 2 and iProtCath >= 2 and iJewishQu >= 2 ):
                                                pPoland.setUHV( 2, 1 )
                                        iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
                                        pPoland.setUHVCounter( 2, iCounter )

                elif ( iPlayer == iGenoa ): # Buildings Goal 2
                        if ( pGenoa.isAlive() and pGenoa.getUHV( 1 ) == -1 ):
                                if ( iBuilding == xml.iGenoaBank ):
                                        iCounter = pGenoa.getUHVCounter( 1 )
                                        iCorps = iCounter % 100
                                        iBanks = iCounter / 100 + 1
                                        if ( iBanks >= 8 and iCorps >= 2 ):
                                                pGenoa.setUHV( 1, 1 )
                                        pGenoa.setUHVCounter( 1, 100 * iBanks + iCorps )

                if ( iBuilding in tCordobaWonders ):
                        if (pCordoba.isAlive() and pCordoba.getUHV( 1 ) == -1 ):
                                if (iPlayer == iCordoba):
                                        iWondersBuilt = pCordoba.getUHVCounter( 1 )
                                        pCordoba.setUHVCounter( 1, iWondersBuilt + 1 )
                                        if (iWondersBuilt == 2):                
                                                pCordoba.setUHV( 1, 1 )
                                else:
                                        pCordoba.setUHV( 1, 0 )

        def onProjectBuilt(self, iPlayer, iProject):
                if ( self.isProjectAColony( iProject )):
                        #self.changeColonies( iPlayer, 1 )
                        if ( pVenecia.getUHV( 2 ) == -1 ):
                                if ( iPlayer == iVenecia ):
                                        pVenecia.setUHV( 2, 1 )
                                else:
                                        pVenecia.setUHV( 2, 0 )

        def onCorporationFounded(self, iPlayer ):
                self.setCorporationsFounded( self.getCorporationsFounded() + 1 )
                if ( iPlayer == iGenoa ):
                        #self.setGenoaCorporations( self.getGenoaCorporations() + 1 )
                        iCounter = pGenoa.getUHVCounter( 1 )
                        iCorps = iCounter % 100 + 1
                        iBanks = iCounter / 100
                        if ( iBanks >= 8 and iCorps >= 2 ):
                                pGenoa.setUHV( 1, 1 )
                        pGenoa.setUHVCounter( 1, 100 * iBanks + iCorps )
                if ( self.getCorporationsFounded() == 7 and pGenoa.getUHV( 1 ) == -1 ):
                        pGenoa.setUHV( 1, 0 )

        def getOwnedLuxes( self, pPlayer ):
                iCount = 0
                iCount += pPlayer.countOwnedBonuses( xml.iSheep )
                iCount += pPlayer.countOwnedBonuses( xml.iDye )
                iCount += pPlayer.countOwnedBonuses( xml.iFur )
                iCount += pPlayer.countOwnedBonuses( xml.iGems )
                iCount += pPlayer.countOwnedBonuses( xml.iGold )
                iCount += pPlayer.countOwnedBonuses( xml.iIncense )
                iCount += pPlayer.countOwnedBonuses( xml.iIvory )
                iCount += pPlayer.countOwnedBonuses( xml.iSilk )
                iCount += pPlayer.countOwnedBonuses( xml.iSilver )
                iCount += pPlayer.countOwnedBonuses( xml.iSpices )
                iCount += pPlayer.countOwnedBonuses( xml.iWine )
                iCount += pPlayer.countOwnedBonuses( xml.iHoney )
                iCount += pPlayer.countOwnedBonuses( xml.iWhale )
                iCount += pPlayer.countOwnedBonuses( xml.iRelic )
                iCount += pPlayer.countOwnedBonuses( xml.iCotton )
                iCount += pPlayer.countOwnedBonuses( xml.iCoffee )
                iCount += pPlayer.countOwnedBonuses( xml.iTea )
                iCount += pPlayer.countOwnedBonuses( xml.iTobacco )
                return iCount

        def getOwnedGrain( self, pPlayer ):
                iCount = 0
                iCount += pPlayer.countOwnedBonuses( xml.iWheat )
                iCount += pPlayer.countOwnedBonuses( xml.iBarley )
                return iCount

        def isProjectAColony( self, iProject ):
                if (iProject >= xml.iNumNotColonies): 
                        return True
                else:
                        return False

        def checkByzantium( self, iGameTurn ):
                if ( iGameTurn == xml.i1025AD and pByzantium.getUHV( 0 ) == -1 ):
                        if ( gc.isLargestCity( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ) and gc.isTopCultureCity( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ) and gc.getMap().plot( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ).getPlotCity().getOwner() == iByzantium ):
                                pByzantium.setUHV( 0, 1 )
                        else:
                                pByzantium.setUHV( 0, 0 )
                
                # 3Miro: Control Asia Minor and Greece in xml.i1282AD
                if ( iGameTurn == xml.i1282AD and pByzantium.getUHV( 1 ) == -1 ):
                        bOwn = True
                        for iProv in tByzantumControl:
                                if ( pByzantium.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bOwn = False
                                        break
                        if ( bOwn ):
                                pByzantium.setUHV( 1, 1 )
                        else:
                                pByzantium.setUHV( 1, 0 )
                
                if ( iGameTurn == xml.i1453AD and pByzantium.getUHV( 2 ) == -1 ):
                        iGold = pByzantium.getGold()
                        bMost = True
                        for iCiv in range( iNumPlayers ):
                                if ( iCiv != iByzantium and gc.getPlayer( iCiv ).isAlive() ):
                                        if (gc.getPlayer(iCiv).getGold() > iGold):
                                                bMost = False
                        if ( bMost ):
                                 pByzantium.setUHV( 2, 1 )
                        else:
                                 pByzantium.setUHV( 2, 0 )
                
        def checkFrankia( self, iGameTurn ):
                if ( iGameTurn <= xml.i840AD and pFrankia.getUHV(0) == -1 ):
                        bCharlemagneEmpire = True
                        for iProv in tFrankControl:
                                iHave = pFrankia.getProvinceCurrentState( iProv )
                                if ( iHave < con.iProvinceConquer ):
                                        bCharlemagneEmpire = False
                                        break
                        if ( bCharlemagneEmpire ):
                                pFrankia.setUHV( 0, 1 )
                        elif ( iGameTurn == xml.i840AD ):
                                pFrankia.setUHV( 0, 0 )
                                
                if (iGameTurn == xml.i1291AD and pFrankia.getUHV(1) == -1 ):
                        pJPlot = gc.getMap().plot( con.iJerusalem[0], con.iJerusalem[1] )
                        if ( pJPlot.isCity()):
                                if ( pJPlot.getPlotCity().getOwner() == iFrankia ):
                                        pFrankia.setUHV( 1, 1 )
                                else:
                                        pFrankia.setUHV( 1, 0 )
                        else:
                                pFrankia.setUHV( 1, 0 )
                                
                if ( pFrankia.getUHV( 2 ) == -1 ):
                        if ( pFrankia.getNumColonies() > 5 ):
                                pFrankia.setUHV( 2, 1 )
                
        def checkArabia( self, iGameTurn ):
                # conquest by i955AD Egypt to Asia Minor UHV 0
                if ( iGameTurn == xml.i955AD and pArabia.getUHV( 0 ) == -1 ):
                        bConq = True
                        for iProv in tArabiaControlI:
                                if ( pArabia.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pArabia.setUHV( 0, 1 )
                        else:
                                pArabia.setUHV( 0, 0 )
                # conquest of Oran to Asia Minor (including defeat the Crusaders) i1291AD UHV 1
                if ( iGameTurn == xml.i1291AD and pArabia.getUHV( 1 ) == -1 ):
                        bConq = True
                        for iProv in tArabiaControlII:
                                if ( pArabia.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pArabia.setUHV( 1, 1 )
                        else:
                                pArabia.setUHV( 1, 0 )

                if ( pArabia.getUHV( 2 ) == -1 ):
                        iPerc = gc.getGame().calculateReligionPercent( xml.iIslam )
                        if ( iPerc >= 25 ):
                                pArabia.setUHV( 2, 1 )
                
        def checkBulgaria( self, iGameTurn ):
                if ( iGameTurn <= xml.i917AD and pBulgaria.getUHV( 0 ) == -1 ):
                        bConq = True
                        for iProv in tBulgariaControl:
                                if ( pBulgaria.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pBulgaria.setUHV( 0, 1 )
                        elif ( iGameTurn == xml.i917AD ):
                                pBulgaria.setUHV( 0, 0 )
                
                if ( iGameTurn <= xml.i1259AD and pBulgaria.getUHV( 1 ) == -1 ):
                        if ( pBulgaria.getFaith() >= 100 ):
                                pBulgaria.setUHV( 1, 1 )
                        elif ( iGameTurn == xml.i1259AD ):
                                pBulgaria.setUHV( 1, 0 )
                                
                if ( iGameTurn == xml.i1393AD and pBulgaria.getUHV( 2 ) == -1 ):
                        pBulgaria.setUHV( 2, 1 )
                
        def checkCordoba( self, iGameTurn ):
                if ( iGameTurn == xml.i961AD and pCordoba.getUHV(0) == -1 ):
                        if ( gc.isLargestCity( con.tCapitals[iCordoba][0], con.tCapitals[iCordoba][1] ) and gc.getMap().plot( con.tCapitals[iCordoba][0], con.tCapitals[iCordoba][1] ).getPlotCity().getOwner() == iCordoba ):
                                pCordoba.setUHV( 0, 1 )
                        else:
                                pCordoba.setUHV( 0, 0 )
                                
                if ( iGameTurn == xml.i1309AD+1 and pCordoba.getUHV(1) == -1 ):
                        pCordoba.setUHV( 1, 0 )
                                
                if ( iGameTurn == xml.i1492AD and pCordoba.getUHV(2) == -1 ):
                        bIslamized = True
                        for iProv in tCordobaIslamize:
                                if ( not ( pCordoba.provinceIsSpreadReligion( iProv, xml.iIslam ) ) ):
                                        bIslamized = False
                                        break
                        if ( bIslamized ):
                                pCordoba.setUHV( 2, 1 )
                        else:
                                pCordoba.setUHV( 2, 0 )

                
        def checkNorse( self, iGameTurn ):
                #if ( iGameTurn == xml.i1009AD and pNorse.getUHV( 0 ) == -1 ):
                #        if ( gc.canSeeAllTerrain( iNorse, xml.iTerrainOcean ) ):
                #                pNorse.setUHV( 0, 1 )
                #        else:
                #                pNorse.setUHV( 0, 0 )
                if ( iGameTurn <= xml.i1009AD+1 and pNorse.getUHV( 0 ) == -1 ): # there is one turn delay between Building and this function being called
                        if ( pNorse.getNumColonies() >= 1 ):
                                pNorse.setUHV( 0, 1 )
                        elif ( iGameTurn == xml.i1009AD+1 ):
                                pNorse.setUHV( 0, 0 )
                

                if ( iGameTurn <= xml.i1061AD and pNorse.getUHV( 1 ) == -1 ):
                        bConq = True
                        for iProv in tNorseControl:
                                if ( pNorse.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pNorse.setUHV( 1, 1 )
                        elif ( iGameTurn == xml.i1061AD ):
                                pNorse.setUHV( 1, 0 )
                
                
        def checkVenecia( self, iGameTurn ):
                if ( iGameTurn <= xml.i1004AD and pVenecia.getUHV( 0 ) == -1 ):
                        bConq = True
                        for iProv in tVenetianControl:
                                if ( pVenecia.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pVenecia.setUHV( 0, 1 )
                        elif ( iGameTurn == xml.i1004AD ):
                                pVenecia.setUHV( 0, 0 )
                # conquer Constantinople by 1204AD
                if ( iGameTurn <= xml.i1204AD and pVenecia.getUHV( 1 ) == -1 ):
                        if ( pVenecia.getProvinceCurrentState( xml.iP_Constantinople ) >= con.iProvinceConquer ):
                                pVenecia.setUHV( 1, 1 )
                        elif ( iGameTurn == xml.i1204AD ):
                                pVenecia.setUHV( 1, 0 )
                
                # one colony project
                
        def checkBurgundy( self, iGameTurn ):
                #if ( iGameTurn == xml.i1200AD and pBurgundy.getUHV(0) == -1 ):
                #        iBurgundyRhine = gc.doesOwnCities( iBurgundy, tBurgundyControl[0][0], tBurgundyControl[0][1], tBurgundyControl[0][2], tBurgundyControl[0][3] )
                #        iBurgundyRhone = gc.doesOwnCities( iBurgundy, tBurgundyControl[1][0], tBurgundyControl[1][1], tBurgundyControl[1][2], tBurgundyControl[1][3] )
                #        if (iBurgundyRhine == 11 and iBurgundyRhone == 11):
                #                pBurgundy.setUHV( 0, 1 )
                #        else:
                #                pBurgundy.setUHV( 0, 0 )
                if ( iGameTurn == xml.i1376AD and pBurgundy.getUHV( 0 ) == -1 ):
                        bOwn = True
                        for iProv in tBurgundyControl:
                                if ( pBurgundy.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bOwn = False
                                        break
                        if ( bOwn ):
                                pBurgundy.setUHV( 0, 1 )
                        else:
                                pBurgundy.setUHV( 0, 0 )
                        
                iCulture =pBurgundy.getUHVCounter(1) + pBurgundy.countCultureProduced() # 3Miro: testing, move it below later
                pBurgundy.setUHVCounter(1, iCulture)
                if ( iGameTurn <= xml.i1336AD and pBurgundy.getUHV(1) == -1 ):
                        if ( iCulture >= 10000 ):
                                pBurgundy.setUHV( 1, 1 )
                        else:
                                if ( iGameTurn == xml.i1336AD ):
                                        pBurgundy.setUHV( 1, 0 )
                
                if ( iGameTurn == xml.i1473AD and pBurgundy.getUHV(2) == -1 ):
                        iBurgundyRank = gc.getGame().getTeamRank(iBurgundy)
                        bIsOnTop = True
                        for iTestPlayer in tBurgundyOutrank:
                                if ( gc.getGame().getTeamRank(iTestPlayer) > iBurgundyRank ):
                                        bIsOnTop = False
                                        break
                        if ( bIsOnTop ):
                                pBurgundy.setUHV( 2, 1 )
                        else:
                                pBurgundy.setUHV( 2, 0 )
                
        def checkGermany( self, iGameTurn ):
                # Have most Catholic FP in 1077 (Walk to Canossa)
                # Have vassals (Hapsburg)
                # Start the reformation
                if ( iGameTurn == xml.i1359AD and pGermany.getUHV( 0 ) == -1 ):
                        bOwn = True
                        for iProv in tGermanyControl:
                                if ( pGermany.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bOwn = False
                                        break
                        if ( bOwn ):
                                pGermany.setUHV( 0, 1 )
                        else:
                                pGermany.setUHV( 0, 0 )

                if ( iGameTurn == xml.i1461AD and pGermany.getUHV( 1 ) == -1 ):
                        iCount = 0
                        for iVassal in range( iNumMajorPlayers ):
                                pVassal = gc.getPlayer( iVassal )
                                if ( iVassal != iGermany and pVassal.isAlive() ):
                                        if ( gc.getTeam( pVassal.getTeam() ).isVassal( pGermany.getTeam() ) ):
                                                iCount += 1
                        
                        if ( iCount >= 3 ):
                                pGermany.setUHV( 1, 1 )
                        else:
                                pGermany.setUHV( 1, 0 )

                if ( iGameTurn == xml.i1540AD and pGermany.getUHV( 2 ) == -1 ):
                        iGermanPower = teamGermany.getPower(False)
                        bPower = True
                        for iPlayer in range( iNumMajorPlayers ):
                                pPlayer = gc.getPlayer( iPlayer )
                                if ( pPlayer.isAlive() and gc.getTeam( pPlayer.getTeam() ).getPower(False) > iGermanPower ):
                                        bPower = False
                        if ( bPower ):
                                pGermany.setUHV( 2, 1 )
                        else:
                                pGermany.setUHV( 2, 0 )
                
        def checkKiev( self, iGameTurn ):
                iFood = pKiev.getUHVCounter( 0 ) + pKiev.calculateTotalYield(YieldTypes.YIELD_FOOD)
                pKiev.setUHVCounter( 0, iFood )
                if ( iGameTurn <= xml.i1300AD and pKiev.getUHV( 0 ) == -1 ):
                        if ( iFood > 20000 ):
                                pKiev.setUHV( 0, 1 )
                        elif ( iGameTurn == xml.i1300AD ):
                                pKiev.setUHV( 0, 0 )
                                
                if ( iGameTurn == xml.i1288AD and pKiev.getUHV( 1 ) == -1 ):
                        bConq = True
                        for iProv in tKievControl:
                                if ( pKiev.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pKiev.setUHV( 1, 1 )
                        else:
                                pKiev.setUHV( 1, 0 )
                
                if ( iGameTurn == xml.i1250AD+1 and pKiev.getUHV( 2 ) == -1 ):
                        pKiev.setUHV( 2, 0 )
                
        def checkHungary( self, iGameTurn ):
                if ( iGameTurn == xml.i1491AD and pHungary.getUHV( 1 ) == -1 ):
                        if ( gc.controlMostTeritory( iHungary, tOLDHungarianControl[0], tOLDHungarianControl[1], tOLDHungarianControl[2], tOLDHungarianControl[3] ) ):
                                pHungary.setUHV( 0, 1 )
                        else:
                                pHungary.setUHV( 0, 0 )
                
                if ( pHungary.getUHV( 1 ) == -1 ):
                        iCivic = pHungary.getCivics(4)
                        if ( iCivic == 24 ):
                                pHungary.setUHV( 1, 1 )
                        else:
                                for iPlayer in range( iNumMajorPlayers ):
                                        pPlayer = gc.getPlayer( iPlayer )
                                        if ( pPlayer.isAlive() and pPlayer.getCivics(4) == 24 ):
                                                pHungary.setUHV( 1, 0 )
                
                if ( iGameTurn == xml.i1444AD and pHungary.getUHV( 2 ) == -1 ):
                        bClean = True
                        if ( pTurkey.isAlive() ):
                                for iProv in tHungarynControl:
                                        if ( pTurkey.getProvinceCityCount( iProv ) > 0):
                                                bClean = False
                                                break
                        if ( bClean ):
                                pHungary.setUHV( 2, 1 )
                        else:
                                pHungary.setUHV( 2, 0 )
                
        def checkSpain( self, iGameTurn ):
                # reconquista (no muslims in Iberia)
                if ( iGameTurn == xml.i1492AD and pSpain.getUHV(0) == -1 ):
                        bConverted = True
                        for iProv in tSpainConvert:
                                if ( not ( pSpain.provinceIsConvertReligion( iProv, xml.iCatholicism ) ) ):
                                        bConverted = False
                                        break
                        if ( bConverted ):
                                pSpain.setUHV( 0, 1 )
                        else:
                                pSpain.setUHV( 0, 0 )
                # many colonies
                if ( iGameTurn == xml.i1542AD and pSpain.getUHV( 1 ) == -1 ):
                        bMost = True
                        iSpainColonies = pSpain.getNumColonies()
                        for iPlayer in range( iNumPlayers ):
                                if ( iPlayer != iSpain ):
                                        pPlayer = gc.getPlayer( iPlayer )
                                        if ( pPlayer.isAlive() and pPlayer.getNumColonies() >= iSpainColonies ):
                                                bMost = False
                        if ( bMost ):
                                pSpain.setUHV( 1, 1 )
                        else:
                                pSpain.setUHV( 1, 0 )
                # purge protestants
                if ( iGameTurn == xml.i1588AD and pSpain.getUHV( 2 ) == -1 ):
                        # we have not captured enough cities
                        bConverted = True
                        for iPlayer in range( iNumPlayers ):
                                if ( iPlayer != iSpain ):
                                        pPlayer = gc.getPlayer( iPlayer )
                                        if ( pPlayer.getStateReligion() == xml.iProtestantism ):
                                                bConverted = False
                                                break
                        if ( bConverted ):
                                pSpain.setUHV( 2, 1 )
                        else:
                                pSpain.setUHV( 2, 0 )
                                                
                
        def checkPoland( self, iGameTurn ):
                # dont lose cities until or conquer Russia? 1772 alt. Vassalize Russia, Germany or Austria
                if (iGameTurn == xml.i1600AD and pPoland.getUHV( 0 ) == -1 ): #Really 1600
                        iNumCities = 0
                        for iProv in tPolishControl:
                                iNumCities += pPoland.getProvinceCityCount( iProv )
                        if ( iNumCities >= 12 ):
                                pPoland.setUHV( 0, 1 )
                        else:
                                pPoland.setUHV( 0, 0 )
                #Really 1500 to 1520
                if ((iGameTurn >= xml.i1500AD) and (iGameTurn <= xml.i1520AD) and pPoland.getUHV( 1 ) == -1 ):
                        iAgriculturePolish = pPoland.calculateTotalYield(YieldTypes.YIELD_FOOD)
                        bFood = True
                        for iPlayer in range( iNumMajorPlayers ):
                                if ( gc.getPlayer( iPlayer ).calculateTotalYield(YieldTypes.YIELD_FOOD ) > iAgriculturePolish ):
                                        bFood = False
                        if (bFood):
                                pPoland.setUHV( 1, 1 )
                        elif ( iGameTurn == xml.i1520AD ):
                                pPoland.setUHV( 1, 0 )

                
        def checkGenoa( self, iGameTurn ):
                if ( iGameTurn == xml.i1540AD and pGenoa.getUHV( 0 ) == -1 ):
                        bConq = True
                        for iProv in tGenoaControl:
                                if ( pGenoa.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pGenoa.setUHV( 0, 1 )
                        else:
                                pGenoa.setUHV( 0, 0 )
                
                if ( iGameTurn == xml.i1640AD and pGenoa.getUHV( 2 ) == -1 ):
                        iCount = 0
                        for iPlayer in range( iNumMajorPlayers ):
                                if ( iPlayer != iGenoa and teamGenoa.isOpenBorders( iPlayer ) ):
                                        iCount += 1
                        if ( iCount >= 10 ):
                                pGenoa.setUHV( 1, 1 )
                        else:
                                pGenoa.setUHV( 1, 0 )
                                
                
        def checkEngland( self, iGameTurn ):
                # 100 years war, conquer France
                if ( iGameTurn == xml.i1452AD and pEngland.getUHV( 0 ) == -1 ):
                        bConq = True
                        for iProv in tEnglandControl:
                                if ( pEngland.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pEngland.setUHV( 0, 1 )
                        else:
                                pEngland.setUHV( 0, 0 )
                # Colonies
                if ( pEngland.getUHV( 1 ) == -1 ):
                        if ( pEngland.getNumColonies() >= 8 ):
                                pEngland.setUHV( 1, 1 )
                # Industrial revolution
                pass
                
        def checkPortugal( self, iGameTurn ):
                if ( pPortugal.getUHV( 2 ) == -1 ):
                        if ( pPortugal.getNumColonies() >= 6 ):
                                pPortugal.setUHV( 2, 1 )
                
        def checkLithuania( self, iGameTurn ):
                iCulture = pLithuania.getUHVCounter(0) + pLithuania.countCultureProduced() # 3Miro: testing, move it below later
                pLithuania.setUHVCounter(0, iCulture)
                if ( iGameTurn <= xml.i1386AD and pLithuania.getUHV( 0 ) == -1 ):
                        if ( pLithuania.getStateReligion() != -1 ):
                                pLithuania.setUHV( 0, 0 )
                        elif ( iCulture >= 4000 ):
                                pLithuania.setUHV( 0, 1 )
                        elif ( iGameTurn == xml.i1386AD ):
                                pLithuania.setUHV( 0, 0 )
                                
                if ( iGameTurn == xml.i1569AD and pLithuania.getUHV( 1 ) == -1 ):
                        bConq = True
                        for iProv in tLithuaniaControl:
                                if ( pLithuania.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pLithuania.setUHV( 1, 1 )
                        else:
                                pLithuania.setUHV( 1, 0 )
                                
                if ( pLithuania.getUHV( 2 ) == -1 ):
                        if ( pMoscow.isAlive() and teamMoscow.isVassal( teamLithuania.getID() ) ):
                                pLithuania.setUHV( 2, 1 )
                        elif ( pLithuania.getProvinceCurrentState( xml.iP_Moscow ) >= con.iProvinceConquer ):
                                pLithuania.setUHV( 2, 1 )
                
        def checkAustria( self, iGameTurn ):
                if ( iGameTurn == xml.i1600AD and pAustria.getUHV( 0 ) == -1 ):
                        bConq = True
                        for iProv in tAustriaControl:
                                if ( pAustria.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pAustria.setUHV( 0, 1 )
                        else:
                                pAustria.setUHV( 0, 0 )
                                
                if ( iGameTurn == xml.i1700AD and pAustria.getUHV( 1 ) == -1 ):
                        iCount = 0
                        for iPlayer in range( iNumMajorPlayers ):
                                pPlayer = gc.getPlayer( iPlayer )
                                if ( iPlayer != iAustria and pPlayer.isAlive() ):
                                        if ( gc.getTeam( pPlayer.getTeam() ).isVassal( iAustria ) ):
                                                iCount += 1

                        if ( iCount >= 3 ):
                                 pAustria.setUHV( 1, 1 )
                        else:
                                 pAustria.setUHV( 1, 0 )
                                
                if ( iGameTurn == xml.i1750AD and pAustria.getUHV( 2 ) == -1 ):
                        iCount = 0
                        for iPlayer in range( iNumMajorPlayers ):
                                if ( iPlayer != iAustria and teamAustria.isDefensivePact( iPlayer ) ):
                                        iCount += 1

                        if ( iCount >= 2 ):
                                 pAustria.setUHV( 2, 1 )
                        else:
                                 pAustria.setUHV( 2, 0 )
                
        def checkTurkey( self, iGameTurn ):
                # conquer the Balkans (1453), Middle East (1517) and Austria (1683)
                if ( iGameTurn == xml.i1453AD and pTurkey.getUHV( 0 ) == -1 ):
                        bConq = True
                        for iProv in tOttomanControlI:
                                if ( pTurkey.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pTurkey.setUHV( 0, 1 )
                        else:
                                pTurkey.setUHV( 0, 0 )
                                
                if ( iGameTurn == xml.i1517AD and pTurkey.getUHV( 1 ) == -1 ):
                        bConq = True
                        for iProv in tOttomanControlII:
                                if ( pTurkey.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pTurkey.setUHV( 1, 1 )
                        else:
                                pTurkey.setUHV( 1, 0 )
                                
                if ( iGameTurn <= xml.i1683AD and pTurkey.getUHV( 2 ) == -1 ):
                        bConq = True
                        for iProv in tOttomanControlIII:
                                if ( pTurkey.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pTurkey.setUHV( 2, 1 )
                        elif ( iGameTurn == xml.i1683AD ):
                                pTurkey.setUHV( 2, 0 )
                
                
        def checkMoscow( self, iGameTurn ):
                # Free eastern Europe from the Mongols
                if ( iGameTurn == xml.i1482AD and pMoscow.getUHV( 0 ) == -1 ):
                        bClean = True
                        for iProv in tMoscowControl:
                                if ( pBarbarian.getProvinceCityCount( iProv ) > 0):
                                        bClean = False
                                        break
                        if ( bClean ):
                                pMoscow.setUHV( 0, 1 )
                        else:
                                pMoscow.setUHV( 0, 0 )
                # Get huge land (20%)
                if ( pMoscow.getUHV( 1 ) == -1 ):
                        RussianLand = pMoscow.getTotalLand()
                        if (totalLand > 0):
                                landPercent = (RussianLand * 100.0) / totalLand
                        else:
                                landPercent = 0.0
                        if ( landPercent >= 20 ):
                                pMoscow.setUHV( 1, 1 )
                # get Warm water
                if ( pMoscow.getUHV( 2 ) == -1 ):
                        if ( pMoscow.countOwnedBonuses( xml.iAccess ) > 0 ):
                                self.setGoal( iMoscow, 2, 1 )
                        elif ( gc.getMap().plot( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ).getPlotCity().getOwner() == iMoscow ):
                                self.setGoal( iMoscow, 2, 1 )
                
        def checkSweden( self, iGameTurn ):
                if ( iGameTurn == xml.i1600AD and pSweden.getUHV( 0 ) == -1 ):
                        bConq = True
                        for iProv in tSwedenControlI:
                                if ( pSweden.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
                                        bConq = False
                                        break
                        if ( bConq ):
                                pSweden.setUHV( 0, 1 )
                        else:
                                pSweden.setUHV( 0, 0 )
                
                if ( iGameTurn == xml.i1700AD and pSweden.getUHV( 1 ) == -1 ):
                        pSweden.setUHV( 1, 1 )
                        
                if (iGameTurn == xml.i1750AD and pSweden.getUHV( 2 ) == -1 ): #Really 1600
                        iNumCities = 0
                        for iProv in tSwedenControlII:
                                iNumCities += pSweden.getProvinceCityCount( iProv )
                        if ( iNumCities >= 5 ):
                                pSweden.setUHV( 0, 1 )
                        else:
                                pSweden.setUHV( 0, 0 )
                
        def checkDutch( self, iGameTurn ):
                if ( iGameTurn == xml.i1640AD and pDutch.getUHV( 0 ) == - 1 ):
                        iCount = 0
                        for iPlayer in range( iNumMajorPlayers ):
                                if ( iPlayer != iDutch and teamDutch.isOpenBorders( iPlayer ) ):
                                        iCount += 1

                        if ( iCount >= 10 ):
                                pDutch.setUHV( 0, 1 )
                        else:
                                pDutch.setUHV( 0, 0 )

                if ( iGameTurn <= xml.i1750AD and pDutch.getUHV( 1 ) == - 1 ):
                        pPlot = gc.getMap().plot( con.tCapitals[iDutch][0], con.tCapitals[iDutch][1])
                        if ( pPlot.isCity() ):
                                iGMerchant = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_MERCHANT")
                                if ( pPlot.getPlotCity().getFreeSpecialistCount(iGMerchant) >= 5 ):
                                        pDutch.setUHV( 1, 1 )
                else:
                        if ( pDutch.getUHV( 1 ) == - 1 ):
                                pDutch.setUHV( 1, 0 )

                if ( pDutch.getUHV( 2 ) == -1 ):
                        if ( pDutch.getNumColonies() > 3 ):
                                pDutch.setUHV( 2, 1 )
                
