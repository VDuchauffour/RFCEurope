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
tByzantiumCore = [xml.iP_Constantinople,xml.iP_Thrace,xml.iP_Thessaly,xml.iP_Macedonia,xml.iP_Epirus,xml.iP_Morea,xml.iP_Illyria,xml.iP_Opsikion,xml.iP_Paphlagonia,xml.iP_Thrakesion,xml.iP_Cilicia,xml.iP_Anatolikon,xml.iP_Armeniakon,xml.iP_Charsiadon,xml.iP_Antiochia,xml.iP_Galilee,xml.iP_Jerusalem,xml.iP_Egypt]
tByzantiumNorm = []
tByzantiumOuter = []
tByzantiumPot2Core = []
tByzantiumPot2Norm = []
tByzantiumDesire = []

tFranceCore = []
tFranceNorm = []
tFranceOuter = [xml.iP_Catalonia,xml.iP_Aragon,xml.iP_Lorraine]
tFrancePot2Core = [xml.iP_IleDeFrance,xml.iP_Aquitania,xml.iP_Orleans,xml.iP_Champagne,xml.iP_Bretagne]
tFrancePot2Norm = [xml.iP_Normandy,xml.iP_Provence,xml.iP_Flanders]
tFranceDesire = []

tArabiaCore = []
tArabiaNorm = []
tArabiaOuter = [xml.iP_Tunisia,xml.iP_Algiers,xml.iP_Oran,xml.iP_Lybia,xml.iP_Sicily]
tArabiaPot2Core = [xml.iP_Syria,xml.iP_Galilee,xml.iP_Jerusalem,xml.iP_Egypt,xml.iP_Arabia]
tArabiaPot2Norm = [xml.iP_Benghazi,xml.iP_Antiochia]
tArabiaDesire = []

tBulgariaCore = []
tBulgariaNorm = []
tBulgariaOuter = [xml.iP_Serbia,xml.iP_Epirus,xml.iP_Thessaloniki,xml.iP_Illyria,xml.iP_Constantinople]
tBulgariaPot2Core = [xml.iP_Moesia,xml.iP_Macedonia]
tBulgariaPot2Norm = [xml.iP_Thrace,xml.iP_Wallachia]
tBulgariaDesire = []

tCordobaCore = []
tCordobaNorm = []
tCordobaOuter = []
tCordobaPot2Core = []
tCordobaPot2Norm = []
tCordobaDesire = []

tNorseCore = []
tNorseNorm = []
tNorseOuter = []
tNorsePot2Core = []
tNorsePot2Norm = []
tNorseDesire = []

tVeniceCore = []
tVeniceNorm = []
tVeniceOuter = []
tVenicePot2Core = []
tVenicePot2Norm = []
tVeniceDesire = []

tBurgundyCore = []
tBurgundyNorm = []
tBurgundyOuter = []
tBurgundyPot2Core = []
tBurgundyPot2Norm = []
tBurgundyDesire = []

tGermanyCore = []
tGermanyNorm = []
tGermanyOuter = []
tGermanyPot2Core = []
tGermanyPot2Norm = []
tGermanyDesire = []

tKievCore = []
tKievNorm = []
tKievOuter = []
tKievPot2Core = []
tKievPot2Norm = []
tKievDesire = []

tHungaryCore = []
tHungaryNorm = []
tHungaryOuter = []
tHungaryPot2Core = []
tHungaryPot2Norm = []
tHungaryDesire = []

tSpainCore = []
tSpainNorm = []
tSpainOuter = []
tSpainPot2Core = []
tSpainPot2Norm = []
tSpainDesire = []

tPolandCore = []
tPolandNorm = []
tPolandOuter = []
tPolandPot2Core = []
tPolandPot2Norm = []
tPolandDesire = []

tGenoaCore = []
tGenoaNorm = []
tGenoaOuter = []
tGenoaPot2Core = []
tGenoaPot2Norm = []
tGenoaDesire = []

tEnglandCore = []
tEnglandNorm = []
tEnglandOuter = [xml.iP_IleDeFrance,xml.iP_Bretagne]
tEnglandPot2Core = [xml.iP_London,xml.iP_EastAnglia,xml.iP_Midlands,xml.iP_Northumbria,xml.iP_Wessex,xml.iP_Wales]
tEnglandPot2Norm = [xml.iP_Scotland,xml.iP_Ireland,xml.iP_Normandy]
tEnglandDesire = []

tPortugalCore = []
tPortugalNorm = []
tPortugalOuter = []
tPortugalPot2Core = []
tPortugalPot2Norm = []
tPortugalDesire = []

tAustriaCore = []
tAustriaNorm = []
tAustriaOuter = []
tAustriaPot2Core = []
tAustriaPot2Norm = []
tAustriaDesire = []

tTurkeyCore = []
tTurkeyNorm = []
tTurkeyOuter = []
tTurkeyPot2Core = []
tTurkeyPot2Norm = []
tTurkeyDesire = []

tMoscowCore = []
tMoscowNorm = []
tMoscowOuter = []
tMoscowPot2Core = []
tMoscowPot2Norm = []
tMoscowDesire = []

tSwedenCore = []
tSwedenNorm = []
tSwedenOuter = []
tSwedenPot2Core = []
tSwedenPot2Norm = []
tSwedenDesire = []

tDutchCore = []
tDutchNorm = []
tDutchOuter = []
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
                                        iAustria : tAustriaDesire,
                                        iTurkey : tTurkeyDesire,
                                        iMoscow : tMoscowDesire,
                                        iSweden : tSwedenDesire,
                                        iDutch : tDutchDesire,
                                        }
        
        def setup( self ):
                # set the initial situation for all players
                pass

        def onCityBuilt(self, iPlayer, x, y):
                #print(" ProvinceManager Build")
                pass
                
        def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
                #print(" ProvinceManager Won")
                pass
        
        def onCityRazed(self, iOwner, playerType, city):
                #print(" ProvinceManager Razed")
                pass
        

