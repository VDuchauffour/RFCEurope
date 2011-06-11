# RFC Europe, balancing modifiers are placed here
from CvPythonExtensions import *
import Consts as con
import XMLConsts as xml
import RFCEMaps as rfcemaps


gc = CyGlobalContext()


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
iLithuania = con.iLithuania
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
pLithuania = gc.getPlayer(iLithuania)
pAustria = gc.getPlayer(iAustria)
pTurkey = gc.getPlayer(iTurkey)
pSweden = gc.getPlayer(iSweden)
pDutch = gc.getPlayer(iDutch)
pPope = gc.getPlayer(iPope)

# Province States
iProvinceNone = con.iProvinceNone
iProvinceOwn = con.iProvinceOwn           
iProvinceConquer = con.iProvinceConquer  
iProvinceDominate = con.iProvinceDominate 
iProvinceLost = con.iProvinceLost         

# ProvinceTypes
iProvinceNone      = con.iProvinceNone 
iProvinceDesired   = con.iProvinceDesired 
iProvinceOuter     = con.iProvinceOuter 
iProvincePotential = con.iProvincePotential 
iProvinceNatural   = con.iProvinceNatural 
iProvinceCore      = con.iProvinceCore 
iNumProvinceTypes  = con.iNumProvinceTypes 

############ Lists of all the provinces for each Civ ###################
tByzantiumCore = [xml.iP_Constantinople,xml.iP_Thrace,xml.iP_Thessaly,xml.iP_Thessaloniki,xml.iP_Macedonia,xml.iP_Epirus,xml.iP_Morea,xml.iP_Arberia,xml.iP_Opsikion,xml.iP_Paphlagonia,xml.iP_Thrakesion,xml.iP_Cilicia,xml.iP_Anatolikon,xml.iP_Armeniakon,xml.iP_Charsiadon,xml.iP_Antiochia,xml.iP_Lebanon,xml.iP_Jerusalem,xml.iP_Egypt]
tByzantiumNorm = [xml.iP_Colonea]
tByzantiumOuter = [xml.iP_Moesia,xml.iP_Serbia,xml.iP_Cyrenaica]
tByzantiumPot2Core = []
tByzantiumPot2Norm = [xml.iP_Cyprus,xml.iP_Crete,xml.iP_Rhodes]
tByzantiumDesire = []

tFranceCore = []
tFranceNorm = []
tFranceOuter = [xml.iP_Catalonia,xml.iP_Aragon,xml.iP_Lorraine,xml.iP_Bavaria,xml.iP_Saxony,xml.iP_Swabia,xml.iP_Franconia,xml.iP_Lombardy]
tFrancePot2Core = [xml.iP_IleDeFrance,xml.iP_Aquitania,xml.iP_Orleans,xml.iP_Champagne,xml.iP_Bretagne]
tFrancePot2Norm = [xml.iP_Normandy,xml.iP_Provence,xml.iP_Flanders,xml.iP_Burgundy,xml.iP_Picardy]
tFranceDesire = []

tArabiaCore = []
tArabiaNorm = []
tArabiaOuter = [xml.iP_Ifriqiya,xml.iP_Algiers,xml.iP_Oran,xml.iP_Tripolitania,xml.iP_Sicily]
tArabiaPot2Core = [xml.iP_Syria,xml.iP_Lebanon,xml.iP_Jerusalem,xml.iP_Egypt,xml.iP_Arabia]
tArabiaPot2Norm = [xml.iP_Antiochia,xml.iP_Cyrenaica]
tArabiaDesire = []

tBulgariaCore = []
tBulgariaNorm = []
tBulgariaOuter = [xml.iP_Serbia,xml.iP_Epirus,xml.iP_Thessaloniki,xml.iP_Arberia,xml.iP_Constantinople]
tBulgariaPot2Core = [xml.iP_Moesia,xml.iP_Macedonia]
tBulgariaPot2Norm = [xml.iP_Thrace,xml.iP_Wallachia]
tBulgariaDesire = []

tCordobaCore = []
tCordobaNorm = []
tCordobaOuter = [xml.iP_Leon,xml.iP_Lusitania,xml.iP_Catalonia,xml.iP_Aragon,xml.iP_Marrakesh,xml.iP_Oran]
tCordobaPot2Core = [xml.iP_Andalusia,xml.iP_Valencia,xml.iP_Castile,xml.iP_Tetouan,xml.iP_Morocco]
tCordobaPot2Norm = []
tCordobaDesire = []

tNorseCore = []
tNorseNorm = []
tNorseOuter = [xml.iP_Scotland,xml.iP_Northumbria,xml.iP_Mercia,xml.iP_Novgorod,xml.iP_Crimea,xml.iP_Sicily,xml.iP_Ireland]
tNorsePot2Core = [xml.iP_Denmark,xml.iP_Norway,xml.iP_Vestfold,xml.iP_Gotaland,xml.iP_Svealand,xml.iP_Oppland,xml.iP_Norrland,xml.iP_Skaneland]
tNorsePot2Norm = [xml.iP_Normandy,xml.iP_Iceland]
tNorseDesire = []

tVeniceCore = []
tVeniceNorm = []
tVeniceOuter = [xml.iP_Arberia,xml.iP_Epirus,xml.iP_Morea,xml.iP_Crete,xml.iP_Rhodes,xml.iP_Constantinople]
tVenicePot2Core = [xml.iP_Verona,xml.iP_Dalmatia]
tVenicePot2Norm = [xml.iP_Carinthia,xml.iP_Tuscany,xml.iP_Croatia]
tVeniceDesire = []

tBurgundyCore = []
tBurgundyNorm = []
tBurgundyOuter = [xml.iP_IleDeFrance,xml.iP_Aquitania,xml.iP_Lorraine,xml.iP_Swabia,xml.iP_Lombardy,xml.iP_Orleans, xml.iP_Normandy]
tBurgundyPot2Core = [xml.iP_Burgundy,xml.iP_Provence,xml.iP_Champagne]
tBurgundyPot2Norm = [xml.iP_Flanders,xml.iP_Picardy]
tBurgundyDesire = []

tGermanyCore = []
tGermanyNorm = []
tGermanyOuter = [xml.iP_Netherlands,xml.iP_Champagne,xml.iP_Flanders,xml.iP_Picardy,xml.iP_Burgundy,xml.iP_Lombardy,xml.iP_Verona,xml.iP_Tuscany,xml.iP_Austria,xml.iP_Moravia,xml.iP_Silesia,xml.iP_GreaterPoland,xml.iP_Pomerania]
tGermanyPot2Core = [xml.iP_Franconia,xml.iP_Bavaria,xml.iP_Swabia,xml.iP_Brandenburg,xml.iP_Saxony,xml.iP_Lorraine]
tGermanyPot2Norm = [xml.iP_Bohemia]
tGermanyDesire = []

tKievCore = []
tKievNorm = []
tKievOuter = [xml.iP_WhiteRus,xml.iP_Kuban,xml.iP_Donets,xml.iP_Simbirsk,xml.iP_Chernigov]
tKievPot2Core = [xml.iP_Kiev,xml.iP_Moldova,xml.iP_Podolia,xml.iP_Pereyaslavl,xml.iP_Zaporizhia,xml.iP_Sloboda]
tKievPot2Norm = [xml.iP_Crimea,xml.iP_Volhynia]
tKievDesire = [xml.iP_Wallachia,xml.iP_Moesia]

tHungaryCore = []
tHungaryNorm = []
tHungaryOuter = [xml.iP_Bavaria,xml.iP_Carinthia,xml.iP_Dalmatia,xml.iP_Bosnia,xml.iP_Serbia,xml.iP_Moesia,xml.iP_Wallachia,xml.iP_Moldova,xml.iP_GaliciaPoland,xml.iP_Bohemia,xml.iP_Silesia]
tHungaryPot2Core = [xml.iP_Hungary,xml.iP_UpperHungary,xml.iP_Pannonia,xml.iP_Transylvania]
tHungaryPot2Norm = [xml.iP_Slavonia,xml.iP_Croatia,xml.iP_Moravia,xml.iP_Austria]
tHungaryDesire = []

tSpainCore = []
tSpainNorm = []
tSpainOuter = [xml.iP_Lusitania,xml.iP_Aquitania,xml.iP_Tetouan,xml.iP_Provence,xml.iP_Balears,xml.iP_Oran,xml.iP_Sardinia,xml.iP_Corsica,xml.iP_Netherlands,xml.iP_Canaries]
tSpainPot2Core = [xml.iP_Leon,xml.iP_GaliciaSpain,xml.iP_Aragon]
tSpainPot2Norm = [xml.iP_Catalonia,xml.iP_Castile,xml.iP_Andalusia,xml.iP_Valencia]
tSpainDesire = []

tPolandCore = []
tPolandNorm = []
tPolandOuter = [xml.iP_Lithuania,xml.iP_Livonia,xml.iP_Polotsk,xml.iP_WhiteRus,xml.iP_Volhynia,xml.iP_Podolia]
tPolandPot2Core = [xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Pomerania,xml.iP_Masovia,xml.iP_Brest]
tPolandPot2Norm = [xml.iP_Silesia,xml.iP_Suvalkija,xml.iP_GaliciaPoland]
tPolandDesire = []

tGenoaCore = []
tGenoaNorm = []
tGenoaOuter = [xml.iP_Ifriqiya,xml.iP_Constantinople,xml.iP_Crete,xml.iP_Rhodes,xml.iP_Cyprus,xml.iP_Crimea,xml.iP_Morea,xml.iP_Malta]
tGenoaPot2Core = [xml.iP_Lombardy,xml.iP_Tuscany,xml.iP_Corsica,xml.iP_Sardinia]
tGenoaPot2Norm = [xml.iP_Sicily]
tGenoaDesire = []

tEnglandCore = []
tEnglandNorm = []
tEnglandOuter = [xml.iP_IleDeFrance,xml.iP_Bretagne,xml.iP_Aquitania,xml.iP_Orleans,xml.iP_Champagne,xml.iP_Flanders,xml.iP_Iceland,xml.iP_Normandy,xml.iP_Picardy]
tEnglandPot2Core = [xml.iP_London,xml.iP_EastAnglia,xml.iP_Northumbria,xml.iP_Mercia,xml.iP_Wessex,xml.iP_Wales]
tEnglandPot2Norm = [xml.iP_Scotland,xml.iP_Ireland]
tEnglandDesire = []

tPortugalCore = []
tPortugalNorm = []
tPortugalOuter = [xml.iP_Morocco,xml.iP_Tetouan,xml.iP_Andalusia,xml.iP_Castile,xml.iP_Leon,xml.iP_GaliciaSpain]
tPortugalPot2Core = [xml.iP_Lusitania]
tPortugalPot2Norm = [xml.iP_Canaries,xml.iP_Azores]
tPortugalDesire = []

tLithuaniaCore = []
tLithuaniaNorm = []
tLithuaniaOuter = [xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Pomerania,xml.iP_Masovia,xml.iP_GaliciaPoland,xml.iP_Volhynia,xml.iP_Podolia,xml.iP_Kiev,xml.iP_Pereyaslavl,xml.iP_Sloboda,xml.iP_Chernigov,xml.iP_Novgorod,xml.iP_Estonia]
tLithuaniaPot2Core = [xml.iP_Lithuania,xml.iP_Livonia,xml.iP_Polotsk]
tLithuaniaPot2Norm = [xml.iP_Suvalkija,xml.iP_Smolensk,xml.iP_WhiteRus]
tLithuaniaDesire = []

tAustriaCore = []
tAustriaNorm = []
tAustriaOuter = [xml.iP_Verona,xml.iP_Bavaria,xml.iP_Pannonia,xml.iP_UpperHungary,xml.iP_Hungary,xml.iP_Transylvania,xml.iP_Croatia,xml.iP_Slavonia,xml.iP_Silesia,xml.iP_GaliciaPoland]
tAustriaPot2Core = [xml.iP_Austria,xml.iP_Carinthia]
tAustriaPot2Norm = [xml.iP_Bohemia,xml.iP_Moravia]
tAustriaDesire = []

tTurkeyCore = []
tTurkeyNorm = []
tTurkeyOuter = [xml.iP_Thessaly,xml.iP_Epirus,xml.iP_Morea,xml.iP_Arberia,xml.iP_Serbia,xml.iP_Moesia,xml.iP_Hungary,xml.iP_Croatia,xml.iP_Bosnia,xml.iP_Slavonia,xml.iP_Transylvania,xml.iP_Pannonia,xml.iP_Moldova]
tTurkeyPot2Core = [xml.iP_Opsikion,xml.iP_Thrakesion,xml.iP_Paphlagonia,xml.iP_Anatolikon,xml.iP_Cilicia,xml.iP_Armeniakon,xml.iP_Charsiadon,xml.iP_Constantinople,xml.iP_Thrace,xml.iP_Colonea]
tTurkeyPot2Norm = [xml.iP_Antiochia,xml.iP_Syria,xml.iP_Lebanon,xml.iP_Jerusalem,xml.iP_Egypt,xml.iP_Arabia,xml.iP_Macedonia,xml.iP_Thessaloniki]
tTurkeyDesire = []

tMoscowCore = []
tMoscowNorm = []
tMoscowOuter = [xml.iP_Zaporizhia,xml.iP_Crimea,xml.iP_Moldova,xml.iP_GaliciaPoland,xml.iP_Wallachia,xml.iP_Kuban,xml.iP_Brest,xml.iP_Polotsk,xml.iP_Lithuania,xml.iP_Livonia,xml.iP_Estonia,xml.iP_Finland,xml.iP_Pomerania,xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Suvalkija]
tMoscowPot2Core = [xml.iP_Moscow,xml.iP_Murom,xml.iP_NizhnyNovgorod,xml.iP_Rostov,xml.iP_Vologda,xml.iP_Karelia,xml.iP_Smolensk,xml.iP_Chernigov,xml.iP_Simbirsk]
tMoscowPot2Norm = [xml.iP_Novgorod,xml.iP_Kiev,xml.iP_WhiteRus,xml.iP_Volhynia,xml.iP_Donets,xml.iP_Pereyaslavl,xml.iP_Sloboda,xml.iP_Podolia]
tMoscowDesire = []

tSwedenCore = []
tSwedenNorm = []
tSwedenOuter = [xml.iP_Denmark,xml.iP_Pomerania,xml.iP_Skaneland]
tSwedenPot2Core = [xml.iP_Gotaland,xml.iP_Norrland,xml.iP_Svealand,]
tSwedenPot2Norm = [xml.iP_Finland,xml.iP_Norway,xml.iP_Vestfold,xml.iP_Oppland]
tSwedenDesire = []

tDutchCore = []
tDutchNorm = []
tDutchOuter = [xml.iP_Flanders]
tDutchPot2Core = [xml.iP_Netherlands]
tDutchPot2Norm = []
tDutchDesire = []

class ProvinceManager:
        
        def __init__( self ):
                self.tCoreProvinces = { iByzantium : tByzantiumCore,
                                        iFrankia : tFranceCore,
                                        iArabia : tArabiaCore,
                                        iBulgaria : tBulgariaCore,
                                        iCordoba : tCordobaCore,
                                        iNorse : tNorseCore,
                                        iVenecia : tVeniceCore,
                                        iBurgundy : tBurgundyCore,
                                        iGermany : tGermanyCore,
                                        iKiev : tKievCore,
                                        iHungary : tHungaryCore,
                                        iSpain : tSpainCore,
                                        iPoland : tPolandCore,
                                        iGenoa : tGenoaCore,
                                        iEngland : tEnglandCore,
                                        iPortugal : tPortugalCore,
                                        iLithuania : tLithuaniaCore,
                                        iAustria : tAustriaCore,
                                        iTurkey : tTurkeyCore,
                                        iMoscow : tMoscowCore,
                                        iSweden : tSwedenCore,
                                        iDutch : tDutchCore,
                                        }
                self.tNormProvinces = { iByzantium : tByzantiumNorm,
                                        iFrankia : tFranceNorm,
                                        iArabia : tArabiaNorm,
                                        iBulgaria : tBulgariaNorm,
                                        iCordoba : tCordobaNorm,
                                        iNorse : tNorseNorm,
                                        iVenecia : tVeniceNorm,
                                        iBurgundy : tBurgundyNorm,
                                        iGermany : tGermanyNorm,
                                        iKiev : tKievNorm,
                                        iHungary : tHungaryNorm,
                                        iSpain : tSpainNorm,
                                        iPoland : tPolandNorm,
                                        iGenoa : tGenoaNorm,
                                        iEngland : tEnglandNorm,
                                        iPortugal : tPortugalNorm,
                                        iLithuania : tLithuaniaNorm,
                                        iAustria : tAustriaNorm,
                                        iTurkey : tTurkeyNorm,
                                        iMoscow : tMoscowNorm,
                                        iSweden : tSwedenNorm,
                                        iDutch : tDutchNorm,
                                        }
                self.tOuterProvinces = { iByzantium : tByzantiumOuter,
                                        iFrankia : tFranceOuter,
                                        iArabia : tArabiaOuter,
                                        iBulgaria : tBulgariaOuter,
                                        iCordoba : tCordobaOuter,
                                        iNorse : tNorseOuter,
                                        iVenecia : tVeniceOuter,
                                        iBurgundy : tBurgundyOuter,
                                        iGermany : tGermanyOuter,
                                        iKiev : tKievOuter,
                                        iHungary : tHungaryOuter,
                                        iSpain : tSpainOuter,
                                        iPoland : tPolandOuter,
                                        iGenoa : tGenoaOuter,
                                        iEngland : tEnglandOuter,
                                        iPortugal : tPortugalOuter,
                                        iLithuania : tLithuaniaOuter,
                                        iAustria : tAustriaOuter,
                                        iTurkey : tTurkeyOuter,
                                        iMoscow : tMoscowOuter,
                                        iSweden : tSwedenOuter,
                                        iDutch : tDutchOuter,
                                        }
                self.tPot2CoreProvinces = { iByzantium : tByzantiumPot2Core,
                                        iFrankia : tFrancePot2Core,
                                        iArabia : tArabiaPot2Core,
                                        iBulgaria : tBulgariaPot2Core,
                                        iCordoba : tCordobaPot2Core,
                                        iNorse : tNorsePot2Core,
                                        iVenecia : tVenicePot2Core,
                                        iBurgundy : tBurgundyPot2Core,
                                        iGermany : tGermanyPot2Core,
                                        iKiev : tKievPot2Core,
                                        iHungary : tHungaryPot2Core,
                                        iSpain : tSpainPot2Core,
                                        iPoland : tPolandPot2Core,
                                        iGenoa : tGenoaPot2Core,
                                        iEngland : tEnglandPot2Core,
                                        iPortugal : tPortugalPot2Core,
                                        iLithuania : tLithuaniaPot2Core,
                                        iAustria : tAustriaPot2Core,
                                        iTurkey : tTurkeyPot2Core,
                                        iMoscow : tMoscowPot2Core,
                                        iSweden : tSwedenPot2Core,
                                        iDutch : tDutchPot2Core,
                                        }
                self.tPot2NormProvinces = { iByzantium : tByzantiumPot2Norm,
                                        iFrankia : tFrancePot2Norm,
                                        iArabia : tArabiaPot2Norm,
                                        iBulgaria : tBulgariaPot2Norm,
                                        iCordoba : tCordobaPot2Norm,
                                        iNorse : tNorsePot2Norm,
                                        iVenecia : tVenicePot2Norm,
                                        iBurgundy : tBurgundyPot2Norm,
                                        iGermany : tGermanyPot2Norm,
                                        iKiev : tKievPot2Norm,
                                        iHungary : tHungaryPot2Norm,
                                        iSpain : tSpainPot2Norm,
                                        iPoland : tPolandPot2Norm,
                                        iGenoa : tGenoaPot2Norm,
                                        iEngland : tEnglandPot2Norm,
                                        iPortugal : tPortugalPot2Norm,
                                        iLithuania : tLithuaniaPot2Norm,
                                        iAustria : tAustriaPot2Norm,
                                        iTurkey : tTurkeyPot2Norm,
                                        iMoscow : tMoscowPot2Norm,
                                        iSweden : tSwedenPot2Norm,
                                        iDutch : tDutchPot2Norm,
                                        }
                self.tDesireProvinces = { iByzantium : tByzantiumDesire,
                                        iFrankia : tFranceDesire,
                                        iArabia : tArabiaDesire,
                                        iBulgaria : tBulgariaDesire,
                                        iCordoba : tCordobaDesire,
                                        iNorse : tNorseDesire,
                                        iVenecia : tVeniceDesire,
                                        iBurgundy : tBurgundyDesire,
                                        iGermany : tGermanyDesire,
                                        iKiev : tKievDesire,
                                        iHungary : tHungaryDesire,
                                        iSpain : tSpainDesire,
                                        iPoland : tPolandDesire,
                                        iGenoa : tGenoaDesire,
                                        iEngland : tEnglandDesire,
                                        iPortugal : tPortugalDesire,
                                        iLithuania : tLithuaniaDesire,
                                        iAustria : tAustriaDesire,
                                        iTurkey : tTurkeyDesire,
                                        iMoscow : tMoscowDesire,
                                        iSweden : tSwedenDesire,
                                        iDutch : tDutchDesire,
                                        }
                self.tpPlayerList = {   iByzantium : pByzantium,
                                        iFrankia : pFrankia,
                                        iArabia : pArabia,
                                        iBulgaria : pBulgaria,
                                        iCordoba : pCordoba,
                                        iNorse : pNorse,
                                        iVenecia : pVenecia,
                                        iBurgundy : pBurgundy,
                                        iGermany : pGermany,
                                        iKiev : pKiev,
                                        iHungary : pHungary,
                                        iSpain : pSpain,
                                        iPoland : pPoland,
                                        iGenoa : pGenoa,
                                        iEngland : pEngland,
                                        iPortugal : pPortugal,
                                        iLithuania : pLithuania,
                                        iAustria : pAustria,
                                        iTurkey : pTurkey,
                                        iMoscow : pMoscow,
                                        iSweden : pSweden,
                                        iDutch : pDutch,
                                        }
        
        def setup( self ):
                # set the initial situation for all players
                for iPlayer in range( con.iNumPlayers -1 ): # this discounts the Pope
                        pPlayer = self.tpPlayerList[iPlayer]
                        for iProv in self.tCoreProvinces[iPlayer]:
                                pPlayer.setProvinceType( iProv, iProvinceCore )
                        for iProv in self.tNormProvinces[iPlayer]:
                                pPlayer.setProvinceType( iProv, iProvinceNatural)
                        for iProv in self.tOuterProvinces[iPlayer]:
                                pPlayer.setProvinceType( iProv, iProvinceOuter )
                        for iProv in self.tPot2CoreProvinces[iPlayer]:
                                pPlayer.setProvinceType( iProv, iProvincePotential )
                        for iProv in self.tPot2NormProvinces[iPlayer]:
                                pPlayer.setProvinceType( iProv, iProvincePotential )
                        for iProv in self.tDesireProvinces[iPlayer]:
                                pPlayer.setProvinceType( iProv, iProvinceDesired )

        def onCityBuilt(self, iPlayer, x, y):
                #print(" ProvinceManager Build")
                if ( iPlayer >= con.iNumPlayers -1 ):
                        return
                pPlayer = self.tpPlayerList[iPlayer]
                iProv = rfcemaps.tProinceMap[y][x]
                if ( pPlayer.getProvinceType( iProv ) == iProvincePotential ):
                        if ( iProv in self.tPot2NormProvinces[iPlayer] ):
                                pPlayer.setProvinceType( iProv, iProvinceNatural )
                        if ( iProv in self.tPot2CoreProvinces[iPlayer] ):
                                pPlayer.setProvinceType( iProv, iProvinceCore )
                
                
        def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
                if ( playerType >= con.iNumPlayers -1 ):
                        return
                pPlayer = self.tpPlayerList[playerType]
                iProv = city.getProvince()
                if ( pPlayer.getProvinceType( iProv ) == iProvincePotential ):
                        if ( iProv in self.tPot2NormProvinces[playerType] ):
                                pPlayer.setProvinceType( iProv, iProvinceNatural )
                        if ( iProv in self.tPot2CoreProvinces[playerType] ):
                                pPlayer.setProvinceType( iProv, iProvinceCore )
        
        def onCityRazed(self, iOwner, playerType, city):
                #print(" ProvinceManager Razed")
                pass
                
        def onRespawn(self, iPlayer ):
                # reset the provinces
                pPlayer = self.tpPlayerList[iPlayer]
                for iProv in self.tCoreProvinces[iPlayer]:
                        pPlayer.setProvinceType( iProv, iProvinceCore )
                for iProv in self.tNormProvinces[iPlayer]:
                        pPlayer.setProvinceType( iProv, iProvinceNatural)
                for iProv in self.tOuterProvinces[iPlayer]:
                        pPlayer.setProvinceType( iProv, iProvinceOuter )
                for iProv in self.tPot2CoreProvinces[iPlayer]:
                        pPlayer.setProvinceType( iProv, iProvincePotential )
                for iProv in self.tPot2NormProvinces[iPlayer]:
                        pPlayer.setProvinceType( iProv, iProvincePotential )
                for iProv in self.tDesireProvinces[iPlayer]:
                        pPlayer.setProvinceType( iProv, iProvinceDesired )
                
                #### -------- Special Respawn Conditions ---------- ####
                if ( iPlayer == iArabia ):
                        for iProv in range( xml.iP_MaxNumberOfProvinces ):
                                pArabia.setProvinceType( iProv, iProvinceNone )
                        for iProv in self.tCoreProvinces[iPlayer]:
                                pArabia.setProvinceType( iProv, iProvinceCore )
                        for iProv in self.tNormProvinces[iPlayer]:
                                pArabia.setProvinceType( iProv, iProvinceNatural)
                        for iProv in self.tOuterProvinces[iPlayer]:
                                pArabia.setProvinceType( iProv, iProvinceOuter )
                        for iProv in self.tPot2CoreProvinces[iPlayer]:
                                pArabia.setProvinceType( iProv, iProvincePotential )
                        for iProv in self.tPot2NormProvinces[iPlayer]:
                                pArabia.setProvinceType( iProv, iProvincePotential )
                        for iProv in self.tDesireProvinces[iPlayer]:
                                pArabia.setProvinceType( iProv, iProvinceDesired )
                elif ( iPlayer == iCordoba ):
                        for iProv in range( xml.iP_MaxNumberOfProvinces ):
                                pCordoba.setProvinceType( iProv, iProvinceNone )
                        pCordoba.setProvinceType( xml.iP_Ifriqiya, iProvinceCore )
                        pCordoba.setProvinceType( xml.iP_Algiers, iProvinceNatural )
                        pCordoba.setProvinceType( xml.iP_Oran, iProvinceOuter )
                        pCordoba.setProvinceType( xml.iP_Tripolitania, iProvinceOuter )
                        pCordoba.setProvinceType( xml.iP_Tetouan, iProvinceOuter )
                        pCordoba.setProvinceType( xml.iP_Morocco, iProvinceOuter )
        
        def onSpawn( self, iPlayer ):
                # when a new nations spawns, old nation should lose some of their provinces
                if ( iPlayer == iArabia ):
                        pByzantium.setProvinceType( xml.iP_Syria, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Arabia, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Egypt, iProvinceNone )
                        pByzantium.setProvinceType( xml.iP_Antiochia, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Lebanon, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Jerusalem, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Cilicia, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Charsiadon, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Colonea, iProvinceOuter )
                elif ( iPlayer == iBulgaria ):
                        pByzantium.setProvinceType( xml.iP_Thrace, iProvinceOuter )
                elif ( iPlayer == iBurgundy ):
                        pFrankia.setProvinceType( xml.iP_Provence, iProvincePotential )
                        pFrankia.setProvinceType( xml.iP_Burgundy, iProvincePotential )
                elif ( iPlayer == iGermany ):
                        pFrankia.setProvinceType( xml.iP_Bavaria, iProvinceNone )
                        pFrankia.setProvinceType( xml.iP_Saxony, iProvinceNone )
                        pFrankia.setProvinceType( xml.iP_Swabia, iProvinceNone )
                        pFrankia.setProvinceType( xml.iP_Franconia, iProvinceOuter )
                        pFrankia.setProvinceType( xml.iP_Lombardy, iProvinceOuter )
                elif ( iPlayer == iSpain ):
                        pCordoba.setProvinceType( xml.iP_Castile, iProvinceOuter )
                elif ( iPlayer == iEngland ):
                        pFrankia.setProvinceType( xml.iP_Normandy, iProvincePotential )
                elif ( iPlayer == iAustria ):
                        pHungary.setProvinceType( xml.iP_Austria, iProvinceOuter ) # maybe others
                        pHungary.setProvinceType( xml.iP_Moravia, iProvinceOuter )
                elif ( iPlayer == iTurkey ):
                        pByzantium.setProvinceType( xml.iP_Opsikion, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Thrakesion, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Anatolikon, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Cilicia, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Charsiadon, iProvinceOuter )
                        pByzantium.setProvinceType( xml.iP_Armeniakon, iProvinceOuter )
                elif ( iPlayer == iSweden ):
                        pNorse.setProvinceType( xml.iP_Norrland, iProvinceOuter )
                        pNorse.setProvinceType( xml.iP_Svealand, iProvinceOuter )
                        pNorse.setProvinceType( xml.iP_Gotaland, iProvinceOuter )
