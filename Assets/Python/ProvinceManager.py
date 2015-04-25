# RFC Europe, balancing modifiers are placed here
from CvPythonExtensions import *
import Consts as con
import XMLConsts as xml
import RFCEMaps as rfcemaps
import RFCUtils # Absinthe


gc = CyGlobalContext()
utils = RFCUtils.RFCUtils() # Absinthe


### Constants ###
iBurgundy = con.iBurgundy
iByzantium = con.iByzantium
iFrankia = con.iFrankia
iArabia = con.iArabia
iBulgaria = con.iBulgaria
iCordoba = con.iCordoba
iSpain = con.iSpain
iNorway = con.iNorway
iDenmark = con.iDenmark
iVenecia = con.iVenecia
iNovgorod = con.iNovgorod
iKiev = con.iKiev
iHungary = con.iHungary
iGermany = con.iGermany
iScotland = con.iScotland
iPoland = con.iPoland
iMoscow = con.iMoscow
iGenoa = con.iGenoa
iMorocco = con.iMorocco
iEngland = con.iEngland
iPortugal = con.iPortugal
iAragon = con.iAragon
iPrussia = con.iPrussia
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
pNorway = gc.getPlayer(iNorway)
pDenmark = gc.getPlayer(iDenmark)
pVenecia = gc.getPlayer(iVenecia)
pNovgorod = gc.getPlayer(iNovgorod)
pKiev = gc.getPlayer(iKiev)
pHungary = gc.getPlayer(iHungary)
pGermany = gc.getPlayer(iGermany)
pScotland = gc.getPlayer(iScotland)
pPoland = gc.getPlayer(iPoland)
pMoscow = gc.getPlayer(iMoscow)
pGenoa = gc.getPlayer(iGenoa)
pMorocco = gc.getPlayer(iMorocco)
pEngland = gc.getPlayer(iEngland)
pPortugal = gc.getPlayer(iPortugal)
pAragon = gc.getPlayer(iAragon)
pPrussia = gc.getPlayer(iPrussia)
pLithuania = gc.getPlayer(iLithuania)
pAustria = gc.getPlayer(iAustria)
pTurkey = gc.getPlayer(iTurkey)
pSweden = gc.getPlayer(iSweden)
pDutch = gc.getPlayer(iDutch)
pPope = gc.getPlayer(iPope)

# Province Status
iProvinceNone = con.iProvinceNone
iProvinceOwn = con.iProvinceOwn
iProvinceConquer = con.iProvinceConquer
iProvinceDominate = con.iProvinceDominate
iProvinceLost = con.iProvinceLost

# Province Types
iProvinceNone      = con.iProvinceNone
iProvinceOuter     = con.iProvinceOuter
iProvincePotential = con.iProvincePotential
iProvinceNatural   = con.iProvinceNatural
iProvinceCore      = con.iProvinceCore
iNumProvinceTypes  = con.iNumProvinceTypes

############ Lists of all the provinces for each Civ ###################
tByzantiumCore = [xml.iP_Constantinople,xml.iP_Thrace,xml.iP_Thessaly,xml.iP_Thessaloniki,xml.iP_Epirus,xml.iP_Morea,xml.iP_Opsikion,xml.iP_Paphlagonia,xml.iP_Thrakesion,xml.iP_Cilicia,xml.iP_Anatolikon,xml.iP_Armeniakon,xml.iP_Charsianon,xml.iP_Colonea,xml.iP_Antiochia]
tByzantiumNorm = [xml.iP_Moesia,xml.iP_Serbia,xml.iP_Macedonia,xml.iP_Arberia,xml.iP_Cyprus,xml.iP_Crete,xml.iP_Rhodes,xml.iP_Syria,xml.iP_Lebanon,xml.iP_Jerusalem,xml.iP_Egypt,xml.iP_Cyrenaica]
tByzantiumOuter = [xml.iP_Crimea,xml.iP_Arabia,xml.iP_Bosnia,xml.iP_Slavonia,xml.iP_Dalmatia,xml.iP_Verona,xml.iP_Lombardy,xml.iP_Liguria,xml.iP_Tuscany,xml.iP_Latium,xml.iP_Sardinia,xml.iP_Corsica]
tByzantiumPot2Core = []
tByzantiumPot2Norm = [xml.iP_Calabria,xml.iP_Apulia,xml.iP_Sicily,xml.iP_Malta,xml.iP_Tripolitania,xml.iP_Ifriqiya]

tFranceCore = [xml.iP_IleDeFrance,xml.iP_Orleans,xml.iP_Champagne]
tFranceNorm = [xml.iP_Picardy,xml.iP_Normandy,xml.iP_Aquitania]
tFranceOuter = [xml.iP_Catalonia,xml.iP_Aragon,xml.iP_Navarre,xml.iP_Lorraine,xml.iP_Netherlands,xml.iP_Bavaria,xml.iP_Saxony,xml.iP_Swabia,xml.iP_Franconia,xml.iP_Lombardy,xml.iP_Liguria,xml.iP_Corsica]
tFrancePot2Core = []
tFrancePot2Norm = [xml.iP_Bretagne,xml.iP_Provence,xml.iP_Burgundy,xml.iP_Flanders]

tArabiaCore = [xml.iP_Syria,xml.iP_Lebanon,xml.iP_Jerusalem,xml.iP_Arabia]
tArabiaNorm = [xml.iP_Egypt,xml.iP_Cyrenaica]
tArabiaOuter = [xml.iP_Oran,xml.iP_Algiers,xml.iP_Sicily,xml.iP_Malta,xml.iP_Crete,xml.iP_Rhodes,xml.iP_Cilicia]
tArabiaPot2Core = []
tArabiaPot2Norm = [xml.iP_Antiochia,xml.iP_Cyprus,xml.iP_Ifriqiya,xml.iP_Tripolitania]

tBulgariaCore = [xml.iP_Moesia]
tBulgariaNorm = [xml.iP_Macedonia,xml.iP_Wallachia]
tBulgariaOuter = [xml.iP_Serbia,xml.iP_Banat,xml.iP_Epirus,xml.iP_Arberia,xml.iP_Constantinople]
tBulgariaPot2Core = []
tBulgariaPot2Norm = [xml.iP_Thrace,xml.iP_Thessaloniki]

tCordobaCore = [xml.iP_Andalusia,xml.iP_Valencia,xml.iP_LaMancha]
tCordobaNorm = [xml.iP_Tetouan]
tCordobaOuter = [xml.iP_Leon,xml.iP_Lusitania,xml.iP_Navarre,xml.iP_Castile,xml.iP_Oran]
tCordobaPot2Core = []
tCordobaPot2Norm = [xml.iP_Morocco,xml.iP_Fez,xml.iP_Marrakesh,xml.iP_Catalonia,xml.iP_Aragon,xml.iP_Balears]

tVeniceCore = [xml.iP_Verona]
tVeniceNorm = [xml.iP_Dalmatia]
tVeniceOuter = [xml.iP_Epirus,xml.iP_Morea,xml.iP_Rhodes,xml.iP_Constantinople]
tVenicePot2Core = []
tVenicePot2Norm = [xml.iP_Tuscany,xml.iP_Arberia,xml.iP_Crete,xml.iP_Cyprus]

tBurgundyCore = [xml.iP_Burgundy]
tBurgundyNorm = [xml.iP_Provence,xml.iP_Flanders]
tBurgundyOuter = [xml.iP_Lorraine,xml.iP_Swabia,xml.iP_Lombardy,xml.iP_Liguria,xml.iP_Bretagne]
tBurgundyPot2Core = []
tBurgundyPot2Norm = [xml.iP_Champagne,xml.iP_Picardy,xml.iP_IleDeFrance,xml.iP_Aquitania,xml.iP_Orleans,xml.iP_Normandy]

tGermanyCore = [xml.iP_Franconia,xml.iP_Lorraine,xml.iP_Bavaria,xml.iP_Swabia,xml.iP_Saxony]
tGermanyNorm = [xml.iP_Brandenburg]
tGermanyOuter = [xml.iP_Champagne,xml.iP_Picardy,xml.iP_Burgundy,xml.iP_Liguria,xml.iP_Verona,xml.iP_Tuscany,xml.iP_Austria,xml.iP_Moravia,xml.iP_Silesia,xml.iP_GreaterPoland,xml.iP_Carinthia]
tGermanyPot2Core = []
tGermanyPot2Norm = [xml.iP_Bohemia,xml.iP_Holstein,xml.iP_Pomerania,xml.iP_Netherlands,xml.iP_Flanders,xml.iP_Lombardy]

tNovgorodCore = [xml.iP_Novgorod, xml.iP_Karelia]
tNovgorodNorm = [xml.iP_Rostov, xml.iP_Vologda]
tNovgorodOuter = [xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_Livonia, xml.iP_Osterland]
tNovgorodPot2Core = []
tNovgorodPot2Norm = [xml.iP_Estonia]

tKievCore = [xml.iP_Kiev,xml.iP_Sloboda,xml.iP_Pereyaslavl,xml.iP_Chernigov]
tKievNorm = [xml.iP_Podolia,xml.iP_Volhynia]
tKievOuter = [xml.iP_Moldova,xml.iP_GaliciaPoland,xml.iP_Brest,xml.iP_Polotsk,xml.iP_Novgorod,xml.iP_Moscow,xml.iP_Murom,xml.iP_Simbirsk,xml.iP_Crimea,xml.iP_Donets,xml.iP_Kuban]
tKievPot2Core = []
tKievPot2Norm = [xml.iP_Minsk,xml.iP_Smolensk,xml.iP_Zaporizhia]

tHungaryCore = [xml.iP_Hungary,xml.iP_UpperHungary,xml.iP_Pannonia,xml.iP_Transylvania]
tHungaryNorm = [xml.iP_Slavonia,xml.iP_Banat,xml.iP_Bosnia,xml.iP_Dalmatia]
tHungaryOuter = [xml.iP_Serbia,xml.iP_Wallachia,xml.iP_Moldova,xml.iP_GaliciaPoland,xml.iP_Bavaria,xml.iP_Bohemia,xml.iP_Silesia]
tHungaryPot2Core = []
tHungaryPot2Norm = [xml.iP_Moravia,xml.iP_Austria,xml.iP_Carinthia]

tSpainCore = [xml.iP_Leon,xml.iP_GaliciaSpain,xml.iP_Castile]
tSpainNorm = []
tSpainOuter = [xml.iP_Lusitania,xml.iP_Catalonia,xml.iP_Aragon,xml.iP_Balears,xml.iP_Aquitania,xml.iP_Provence,xml.iP_Tetouan,xml.iP_Fez,xml.iP_Oran,xml.iP_Algiers,xml.iP_Sardinia,xml.iP_Corsica,xml.iP_Azores,xml.iP_Sicily,xml.iP_Calabria,xml.iP_Apulia]
tSpainPot2Core = []
tSpainPot2Norm = [xml.iP_Navarre,xml.iP_Andalusia,xml.iP_Valencia,xml.iP_LaMancha,xml.iP_Canaries,xml.iP_Madeira]

tScotlandCore = [xml.iP_Scotland]
tScotlandNorm = [xml.iP_TheIsles]
tScotlandOuter = [xml.iP_Ireland, xml.iP_Mercia, xml.iP_Wales]
tScotlandPot2Core = []
tScotlandPot2Norm = [xml.iP_Northumbria]

tPolandCore = [xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Masovia]
tPolandNorm = [xml.iP_Brest,xml.iP_GaliciaPoland]
tPolandOuter = [xml.iP_Prussia,xml.iP_Lithuania,xml.iP_Polotsk,xml.iP_Minsk,xml.iP_Volhynia,xml.iP_Podolia,xml.iP_Moldova,xml.iP_Kiev]
tPolandPot2Core = []
tPolandPot2Norm = [xml.iP_Pomerania,xml.iP_Silesia,xml.iP_Suvalkija]

tGenoaCore = [xml.iP_Liguria]
tGenoaNorm = [xml.iP_Corsica,xml.iP_Sardinia]
tGenoaOuter = [xml.iP_Ifriqiya,xml.iP_Constantinople,xml.iP_Crete,xml.iP_Cyprus,xml.iP_Morea]
tGenoaPot2Core = []
tGenoaPot2Norm = [xml.iP_Sicily,xml.iP_Malta,xml.iP_Lombardy,xml.iP_Tuscany,xml.iP_Rhodes,xml.iP_Crimea]

tMoroccoCore = [xml.iP_Marrakesh, xml.iP_Morocco, xml.iP_Fez]
tMoroccoNorm = [xml.iP_Tetouan]
tMoroccoOuter = [xml.iP_Ifriqiya, xml.iP_Andalusia, xml.iP_Valencia, xml.iP_Tripolitania]
tMoroccoPot2Core = []
tMoroccoPot2Norm = [xml.iP_Oran, xml.iP_Algiers]

tEnglandCore = [xml.iP_London,xml.iP_EastAnglia,xml.iP_Mercia,xml.iP_Wessex]
tEnglandNorm = [xml.iP_Northumbria]
tEnglandOuter = [xml.iP_IleDeFrance,xml.iP_Bretagne,xml.iP_Aquitania,xml.iP_Orleans,xml.iP_Champagne,xml.iP_Flanders,xml.iP_Normandy,xml.iP_Picardy,xml.iP_Scotland,xml.iP_TheIsles,xml.iP_Ireland]
tEnglandPot2Core = []
tEnglandPot2Norm = [xml.iP_Wales]

tPortugalCore = [xml.iP_Lusitania]
tPortugalNorm = [xml.iP_Azores]
tPortugalOuter = [xml.iP_Morocco,xml.iP_Tetouan,xml.iP_Leon,xml.iP_GaliciaSpain]
tPortugalPot2Core = []
tPortugalPot2Norm = [xml.iP_Madeira,xml.iP_Canaries,xml.iP_Andalusia]

tAragonCore = [xml.iP_Aragon,xml.iP_Catalonia,xml.iP_Balears,xml.iP_Valencia]
tAragonNorm = []
tAragonOuter = [xml.iP_Castile,xml.iP_Provence,xml.iP_Corsica,xml.iP_Thessaly]
tAragonPot2Core = []
tAragonPot2Norm = [xml.iP_Navarre,xml.iP_Andalusia,xml.iP_LaMancha,xml.iP_Sardinia,xml.iP_Sicily,xml.iP_Apulia,xml.iP_Calabria,xml.iP_Malta]

tPrussiaCore = [xml.iP_Prussia]
tPrussiaNorm = []
tPrussiaOuter = [xml.iP_Brandenburg,xml.iP_Estonia,xml.iP_Gotland]
tPrussiaPot2Core = []
tPrussiaPot2Norm = [xml.iP_Pomerania,xml.iP_Livonia]

tLithuaniaCore = [xml.iP_Lithuania]
tLithuaniaNorm = [xml.iP_Suvalkija,xml.iP_Minsk,xml.iP_Polotsk]
tLithuaniaOuter = [xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Masovia,xml.iP_GaliciaPoland,xml.iP_Sloboda,xml.iP_Pereyaslavl,xml.iP_Livonia,xml.iP_Estonia,xml.iP_Novgorod,xml.iP_Smolensk,xml.iP_Chernigov]
tLithuaniaPot2Core = []
tLithuaniaPot2Norm = [xml.iP_Brest,xml.iP_Podolia,xml.iP_Volhynia,xml.iP_Kiev]

tAustriaCore = [xml.iP_Austria,xml.iP_Carinthia]
tAustriaNorm = [xml.iP_Bohemia,xml.iP_Moravia]
tAustriaOuter = [xml.iP_Verona,xml.iP_Hungary,xml.iP_Transylvania,xml.iP_Slavonia,xml.iP_Dalmatia,xml.iP_LesserPoland,xml.iP_GaliciaPoland,xml.iP_Netherlands,xml.iP_Flanders]
tAustriaPot2Core = []
tAustriaPot2Norm = [xml.iP_Bavaria,xml.iP_Silesia,xml.iP_Pannonia,xml.iP_UpperHungary]

tTurkeyCore = [xml.iP_Opsikion,xml.iP_Thrakesion,xml.iP_Paphlagonia,xml.iP_Anatolikon,xml.iP_Constantinople]
tTurkeyNorm = [xml.iP_Thrace,xml.iP_Armeniakon,xml.iP_Charsianon,xml.iP_Cilicia]
tTurkeyOuter = [xml.iP_Thessaly,xml.iP_Epirus,xml.iP_Morea,xml.iP_Arberia,xml.iP_Wallachia,xml.iP_Serbia,xml.iP_Bosnia,xml.iP_Banat,xml.iP_Slavonia,xml.iP_Pannonia,xml.iP_Hungary,xml.iP_Transylvania,xml.iP_Moldova,xml.iP_Crimea,xml.iP_Crete,xml.iP_Cyrenaica,xml.iP_Tripolitania]
tTurkeyPot2Core = []
tTurkeyPot2Norm = [xml.iP_Colonea,xml.iP_Antiochia,xml.iP_Syria,xml.iP_Lebanon,xml.iP_Jerusalem,xml.iP_Egypt,xml.iP_Arabia,xml.iP_Macedonia,xml.iP_Thessaloniki,xml.iP_Moesia,xml.iP_Cyprus,xml.iP_Rhodes]

tMoscowCore = [xml.iP_Moscow,xml.iP_Murom,xml.iP_Rostov,xml.iP_Smolensk]
tMoscowNorm = [xml.iP_NizhnyNovgorod,xml.iP_Simbirsk,xml.iP_Pereyaslavl,xml.iP_Chernigov]
tMoscowOuter = [xml.iP_Crimea,xml.iP_Moldova,xml.iP_GaliciaPoland,xml.iP_Kuban,xml.iP_Brest,xml.iP_Lithuania,xml.iP_Livonia,xml.iP_Estonia,xml.iP_Karelia,xml.iP_Osterland,xml.iP_Prussia,xml.iP_Suvalkija]
tMoscowPot2Core = []
tMoscowPot2Norm = [xml.iP_Novgorod,xml.iP_Vologda,xml.iP_Kiev,xml.iP_Minsk,xml.iP_Polotsk,xml.iP_Volhynia,xml.iP_Podolia,xml.iP_Donets,xml.iP_Sloboda,xml.iP_Zaporizhia]

tNorwayCore = [xml.iP_Norway,xml.iP_Vestfold]
tNorwayNorm = [xml.iP_Iceland]
tNorwayOuter = [xml.iP_Scotland,xml.iP_Northumbria,xml.iP_Ireland,xml.iP_Normandy,xml.iP_Svealand,xml.iP_Norrland]
tNorwayPot2Core = []
tNorwayPot2Norm = [xml.iP_TheIsles,xml.iP_Jamtland]

tDenmarkCore = [xml.iP_Denmark,xml.iP_Skaneland]
tDenmarkNorm = []
tDenmarkOuter = [xml.iP_Gotaland,xml.iP_Svealand,xml.iP_Northumbria,xml.iP_Mercia,xml.iP_EastAnglia,xml.iP_London,xml.iP_Brandenburg,xml.iP_Norway,xml.iP_Vestfold,xml.iP_Normandy]
tDenmarkPot2Core = []
tDenmarkPot2Norm = [xml.iP_Estonia,xml.iP_Gotland,xml.iP_Holstein]

tSwedenCore = [xml.iP_Norrland,xml.iP_Svealand]
tSwedenNorm = [xml.iP_Gotaland,xml.iP_Gotland]
tSwedenOuter = [xml.iP_Skaneland,xml.iP_Vestfold,xml.iP_Pomerania,xml.iP_Livonia,xml.iP_Prussia,xml.iP_Novgorod]
tSwedenPot2Core = []
tSwedenPot2Norm = [xml.iP_Jamtland,xml.iP_Osterland,xml.iP_Karelia,xml.iP_Estonia]

tDutchCore = [xml.iP_Netherlands]
tDutchNorm = [xml.iP_Flanders]
tDutchOuter = []
tDutchPot2Core = []
tDutchPot2Norm = []


class ProvinceManager:

	def __init__( self ):
		self.tCoreProvinces = {
			iByzantium : tByzantiumCore,
			iFrankia : tFranceCore,
			iArabia : tArabiaCore,
			iBulgaria : tBulgariaCore,
			iCordoba : tCordobaCore,
			iVenecia : tVeniceCore,
			iBurgundy : tBurgundyCore,
			iGermany : tGermanyCore,
			iNovgorod : tNovgorodCore,
			iNorway : tNorwayCore,
			iKiev : tKievCore,
			iHungary : tHungaryCore,
			iSpain : tSpainCore,
			iDenmark : tDenmarkCore,
			iScotland : tScotlandCore,
			iPoland : tPolandCore,
			iGenoa : tGenoaCore,
			iMorocco : tMoroccoCore,
			iEngland : tEnglandCore,
			iPortugal : tPortugalCore,
			iAragon : tAragonCore,
			iSweden : tSwedenCore,
			iPrussia : tPrussiaCore,
			iLithuania : tLithuaniaCore,
			iAustria : tAustriaCore,
			iTurkey : tTurkeyCore,
			iMoscow : tMoscowCore,
			iDutch : tDutchCore,
			}

		self.tNormProvinces = {
			iByzantium : tByzantiumNorm,
			iFrankia : tFranceNorm,
			iArabia : tArabiaNorm,
			iBulgaria : tBulgariaNorm,
			iCordoba : tCordobaNorm,
			iVenecia : tVeniceNorm,
			iBurgundy : tBurgundyNorm,
			iGermany : tGermanyNorm,
			iNovgorod : tNovgorodNorm,
			iNorway : tNorwayNorm,
			iKiev : tKievNorm,
			iHungary : tHungaryNorm,
			iSpain : tSpainNorm,
			iDenmark : tDenmarkNorm,
			iScotland : tScotlandNorm,
			iPoland : tPolandNorm,
			iGenoa : tGenoaNorm,
			iMorocco : tMoroccoNorm,
			iEngland : tEnglandNorm,
			iPortugal : tPortugalNorm,
			iAragon : tAragonNorm,
			iSweden : tSwedenNorm,
			iPrussia : tPrussiaNorm,
			iLithuania : tLithuaniaNorm,
			iAustria : tAustriaNorm,
			iTurkey : tTurkeyNorm,
			iMoscow : tMoscowNorm,
			iDutch : tDutchNorm,
			}

		self.tOuterProvinces = {
			iByzantium : tByzantiumOuter,
			iFrankia : tFranceOuter,
			iArabia : tArabiaOuter,
			iBulgaria : tBulgariaOuter,
			iCordoba : tCordobaOuter,
			iVenecia : tVeniceOuter,
			iBurgundy : tBurgundyOuter,
			iGermany : tGermanyOuter,
			iNovgorod : tNovgorodOuter,
			iNorway : tNorwayOuter,
			iKiev : tKievOuter,
			iHungary : tHungaryOuter,
			iSpain : tSpainOuter,
			iDenmark : tDenmarkOuter,
			iScotland : tScotlandOuter,
			iPoland : tPolandOuter,
			iGenoa : tGenoaOuter,
			iMorocco : tMoroccoOuter,
			iEngland : tEnglandOuter,
			iPortugal : tPortugalOuter,
			iAragon : tAragonOuter,
			iSweden : tSwedenOuter,
			iPrussia : tPrussiaOuter,
			iLithuania : tLithuaniaOuter,
			iAustria : tAustriaOuter,
			iTurkey : tTurkeyOuter,
			iMoscow : tMoscowOuter,
			iDutch : tDutchOuter,
			}

		self.tPot2CoreProvinces = {
			iByzantium : tByzantiumPot2Core,
			iFrankia : tFrancePot2Core,
			iArabia : tArabiaPot2Core,
			iBulgaria : tBulgariaPot2Core,
			iCordoba : tCordobaPot2Core,
			iVenecia : tVenicePot2Core,
			iBurgundy : tBurgundyPot2Core,
			iGermany : tGermanyPot2Core,
			iNovgorod : tNovgorodPot2Core,
			iNorway : tNorwayPot2Core,
			iKiev : tKievPot2Core,
			iHungary : tHungaryPot2Core,
			iSpain : tSpainPot2Core,
			iDenmark : tDenmarkPot2Core,
			iScotland : tScotlandPot2Core,
			iPoland : tPolandPot2Core,
			iGenoa : tGenoaPot2Core,
			iMorocco : tMoroccoPot2Core,
			iEngland : tEnglandPot2Core,
			iPortugal : tPortugalPot2Core,
			iAragon : tAragonPot2Core,
			iSweden : tSwedenPot2Core,
			iPrussia : tPrussiaPot2Core,
			iLithuania : tLithuaniaPot2Core,
			iAustria : tAustriaPot2Core,
			iTurkey : tTurkeyPot2Core,
			iMoscow : tMoscowPot2Core,
			iDutch : tDutchPot2Core,
			}

		self.tPot2NormProvinces = {
			iByzantium : tByzantiumPot2Norm,
			iFrankia : tFrancePot2Norm,
			iArabia : tArabiaPot2Norm,
			iBulgaria : tBulgariaPot2Norm,
			iCordoba : tCordobaPot2Norm,
			iVenecia : tVenicePot2Norm,
			iBurgundy : tBurgundyPot2Norm,
			iGermany : tGermanyPot2Norm,
			iNovgorod : tNovgorodPot2Norm,
			iNorway : tNorwayPot2Norm,
			iKiev : tKievPot2Norm,
			iHungary : tHungaryPot2Norm,
			iSpain : tSpainPot2Norm,
			iDenmark : tDenmarkPot2Norm,
			iScotland : tScotlandPot2Norm,
			iPoland : tPolandPot2Norm,
			iGenoa : tGenoaPot2Norm,
			iMorocco : tMoroccoPot2Norm,
			iEngland : tEnglandPot2Norm,
			iPortugal : tPortugalPot2Norm,
			iAragon : tAragonPot2Norm,
			iSweden : tSwedenPot2Norm,
			iPrussia : tPrussiaPot2Norm,
			iLithuania : tLithuaniaPot2Norm,
			iAustria : tAustriaPot2Norm,
			iTurkey : tTurkeyPot2Norm,
			iMoscow : tMoscowPot2Norm,
			iDutch : tDutchPot2Norm,
			}

		self.tpPlayerList = {
			iByzantium : pByzantium,
			iFrankia : pFrankia,
			iArabia : pArabia,
			iBulgaria : pBulgaria,
			iCordoba : pCordoba,
			iVenecia : pVenecia,
			iBurgundy : pBurgundy,
			iGermany : pGermany,
			iNovgorod : pNovgorod,
			iNorway : pNorway,
			iKiev : pKiev,
			iHungary : pHungary,
			iSpain : pSpain,
			iDenmark : pDenmark,
			iScotland : pScotland,
			iPoland : pPoland,
			iGenoa : pGenoa,
			iMorocco : pMorocco,
			iEngland : pEngland,
			iPortugal : pPortugal,
			iAragon : pAragon,
			iSweden : pSweden,
			iPrussia : pPrussia,
			iLithuania : pLithuania,
			iAustria : pAustria,
			iTurkey : pTurkey,
			iMoscow : pMoscow,
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

	def onCityBuilt(self, iPlayer, x, y):
		if ( iPlayer >= con.iNumPlayers -1 ):
			return
		pPlayer = self.tpPlayerList[iPlayer]
		iProv = rfcemaps.tProinceMap[y][x]
		if ( pPlayer.getProvinceType( iProv ) == iProvincePotential ):
			if ( iProv in self.tPot2NormProvinces[iPlayer] ):
				pPlayer.setProvinceType( iProv, iProvinceNatural )
				utils.refreshStabilityOverlay() # refresh the stability overlay
			if ( iProv in self.tPot2CoreProvinces[iPlayer] ):
				pPlayer.setProvinceType( iProv, iProvinceCore )
				utils.refreshStabilityOverlay() # refresh the stability overlay

	def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
		if ( playerType >= con.iNumPlayers -1 ):
			return
		pPlayer = self.tpPlayerList[playerType]
		iProv = city.getProvince()
		if ( pPlayer.getProvinceType( iProv ) == iProvincePotential ):
			if ( iProv in self.tPot2NormProvinces[playerType] ):
				pPlayer.setProvinceType( iProv, iProvinceNatural )
				utils.refreshStabilityOverlay() # refresh the stability overlay
			if ( iProv in self.tPot2CoreProvinces[playerType] ):
				pPlayer.setProvinceType( iProv, iProvinceCore )
				utils.refreshStabilityOverlay() # refresh the stability overlay

	def onCityRazed(self, iOwner, playerType, city):
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
		elif ( iPlayer == iCordoba ):
			for iProv in range( xml.iP_MaxNumberOfProvinces ):
				pCordoba.setProvinceType( iProv, iProvinceNone )
			pCordoba.setProvinceType( xml.iP_Ifriqiya, iProvinceCore )
			pCordoba.setProvinceType( xml.iP_Algiers, iProvinceNatural )
			pCordoba.setProvinceType( xml.iP_Oran, iProvinceOuter )
			pCordoba.setProvinceType( xml.iP_Tripolitania, iProvinceOuter )
			pCordoba.setProvinceType( xml.iP_Tetouan, iProvinceOuter )
			pCordoba.setProvinceType( xml.iP_Morocco, iProvinceOuter )
			pCordoba.setProvinceType( xml.iP_Fez, iProvinceOuter )

	def onSpawn( self, iPlayer ):
		# when a new nations spawns, old nations in the region should lose some of their provinces
		if ( iPlayer == iArabia ):
			pByzantium.setProvinceType( xml.iP_Cyrenaica, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Tripolitania, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Ifriqiya, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Egypt, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Arabia, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Syria, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Lebanon, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Jerusalem, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Antiochia, iProvinceNatural )
			pByzantium.setProvinceType( xml.iP_Cilicia, iProvinceNatural )
			pByzantium.setProvinceType( xml.iP_Charsianon, iProvinceNatural )
			pByzantium.setProvinceType( xml.iP_Colonea, iProvinceNatural )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iBulgaria ):
			pByzantium.setProvinceType( xml.iP_Serbia, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Moesia, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Thrace, iProvinceNatural )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iVenecia ):
			pByzantium.setProvinceType( xml.iP_Dalmatia, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Bosnia, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Slavonia, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Verona, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Tuscany, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Lombardy, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Liguria, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Corsica, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Sardinia, iProvinceNone )
			pByzantium.setProvinceType( xml.iP_Latium, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iBurgundy ):
			pFrankia.setProvinceType( xml.iP_Provence, iProvincePotential ) # these areas flip to Burgundy, so resetting them to Potential will work perfectly
			pFrankia.setProvinceType( xml.iP_Burgundy, iProvincePotential ) # these areas flip to Burgundy, so resetting them to Potential will work perfectly
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iGermany ):
			pFrankia.setProvinceType( xml.iP_Bavaria, iProvinceNone )
			pFrankia.setProvinceType( xml.iP_Franconia, iProvinceNone )
			pFrankia.setProvinceType( xml.iP_Saxony, iProvinceNone )
			pFrankia.setProvinceType( xml.iP_Netherlands, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iHungary ):
			pBulgaria.setProvinceType( xml.iP_Banat, iProvinceNone )
			pBulgaria.setProvinceType( xml.iP_Wallachia, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iSpain ):
			pCordoba.setProvinceType( xml.iP_LaMancha, iProvinceNatural )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iMorocco ):
			pCordoba.setProvinceType( xml.iP_Morocco, iProvinceNone )
			pCordoba.setProvinceType( xml.iP_Marrakesh, iProvinceNone )
			pCordoba.setProvinceType( xml.iP_Fez, iProvinceOuter )
			pCordoba.setProvinceType( xml.iP_Tetouan, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iAragon ):
			pByzantium.setProvinceType( xml.iP_Apulia, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Calabria, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Sicily, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Malta, iProvinceOuter )
			pCordoba.setProvinceType( xml.iP_Aragon, iProvinceOuter )
			pCordoba.setProvinceType( xml.iP_Catalonia, iProvinceOuter )
			pCordoba.setProvinceType( xml.iP_Valencia, iProvinceNatural )
			pCordoba.setProvinceType( xml.iP_Balears, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iEngland ):
			pFrankia.setProvinceType( xml.iP_Normandy, iProvincePotential )
			pFrankia.setProvinceType( xml.iP_Picardy, iProvincePotential )
			pScotland.setProvinceType( xml.iP_Northumbria, iProvinceOuter )
			pScotland.setProvinceType( xml.iP_Mercia, iProvinceNone )
			pNorway.setProvinceType( xml.iP_Normandy, iProvinceNone )
			pNorway.setProvinceType( xml.iP_Northumbria, iProvinceNone )
			pDenmark.setProvinceType( xml.iP_Normandy, iProvinceNone )
			pDenmark.setProvinceType( xml.iP_Northumbria, iProvinceNone )
			pDenmark.setProvinceType( xml.iP_Mercia, iProvinceNone )
			pDenmark.setProvinceType( xml.iP_EastAnglia, iProvinceNone )
			pDenmark.setProvinceType( xml.iP_London, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iAustria ):
			pHungary.setProvinceType( xml.iP_Carinthia, iProvinceOuter )
			pHungary.setProvinceType( xml.iP_Austria, iProvinceOuter )
			pHungary.setProvinceType( xml.iP_Moravia, iProvinceOuter )
			pHungary.setProvinceType( xml.iP_Bavaria, iProvinceNone )
			pGermany.setProvinceType( xml.iP_Bavaria, iProvinceOuter )
			pGermany.setProvinceType( xml.iP_Bohemia, iProvinceOuter )
			pSpain.setProvinceType( xml.iP_Netherlands, iProvinceOuter )
			pSpain.setProvinceType( xml.iP_Flanders, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iTurkey ):
			pByzantium.setProvinceType( xml.iP_Antiochia, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Cilicia, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Charsianon, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Colonea, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Armeniakon, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Cyprus, iProvinceOuter )
			pByzantium.setProvinceType( xml.iP_Anatolikon, iProvinceNatural )
			pByzantium.setProvinceType( xml.iP_Opsikion, iProvinceNatural )
			pByzantium.setProvinceType( xml.iP_Thrakesion, iProvinceNatural )
			pByzantium.setProvinceType( xml.iP_Paphlagonia, iProvinceNatural )
			pHungary.setProvinceType( xml.iP_Dalmatia, iProvinceOuter )
			pHungary.setProvinceType( xml.iP_Bosnia, iProvinceOuter )
			pHungary.setProvinceType( xml.iP_Banat, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iSweden ):
			pNorway.setProvinceType( xml.iP_Svealand, iProvinceNone )
			pDenmark.setProvinceType(xml.iP_Gotaland, iProvinceNone )
			pDenmark.setProvinceType(xml.iP_Svealand, iProvinceNone )
			pNovgorod.setProvinceType( xml.iP_Osterland, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iDutch ):
			pSpain.setProvinceType( xml.iP_Netherlands, iProvinceNone )
			pSpain.setProvinceType( xml.iP_Flanders, iProvinceNone )
			pAustria.setProvinceType( xml.iP_Netherlands, iProvinceNone )
			pAustria.setProvinceType( xml.iP_Flanders, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iMoscow ):
			pNovgorod.setProvinceType( xml.iP_Rostov, iProvinceOuter )
			pNovgorod.setProvinceType( xml.iP_Smolensk, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay

