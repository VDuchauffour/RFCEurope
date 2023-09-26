# RFC Europe - Province manager

from CvPythonExtensions import *
import Consts
import XMLConsts as xml
import RFCEMaps
import RFCUtils  # Absinthe
import PyHelpers  # Absinthe

from TimelineData import CIV_BIRTHDATE
from CoreStructures import get_civ_by_id
from CoreTypes import Scenario

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer  # Absinthe
utils = RFCUtils.RFCUtils()  # Absinthe


pBurgundy = gc.getPlayer(Consts.iBurgundy)
pByzantium = gc.getPlayer(Consts.iByzantium)
pFrankia = gc.getPlayer(Consts.iFrankia)
pArabia = gc.getPlayer(Consts.iArabia)
pBulgaria = gc.getPlayer(Consts.iBulgaria)
pCordoba = gc.getPlayer(Consts.iCordoba)
pSpain = gc.getPlayer(Consts.iSpain)
pNorway = gc.getPlayer(Consts.iNorway)
pDenmark = gc.getPlayer(Consts.iDenmark)
pVenecia = gc.getPlayer(Consts.iVenecia)
pNovgorod = gc.getPlayer(Consts.iNovgorod)
pKiev = gc.getPlayer(Consts.iKiev)
pHungary = gc.getPlayer(Consts.iHungary)
pGermany = gc.getPlayer(Consts.iGermany)
pScotland = gc.getPlayer(Consts.iScotland)
pPoland = gc.getPlayer(Consts.iPoland)
pMoscow = gc.getPlayer(Consts.iMoscow)
pGenoa = gc.getPlayer(Consts.iGenoa)
pMorocco = gc.getPlayer(Consts.iMorocco)
pEngland = gc.getPlayer(Consts.iEngland)
pPortugal = gc.getPlayer(Consts.iPortugal)
pAragon = gc.getPlayer(Consts.iAragon)
pPrussia = gc.getPlayer(Consts.iPrussia)
pLithuania = gc.getPlayer(Consts.iLithuania)
pAustria = gc.getPlayer(Consts.iAustria)
pTurkey = gc.getPlayer(Consts.iTurkey)
pSweden = gc.getPlayer(Consts.iSweden)
pDutch = gc.getPlayer(Consts.iDutch)
pPope = gc.getPlayer(Consts.iPope)


############ Lists of all the provinces for each Civ ###################
tByzantiumCore = [
    xml.iP_Constantinople,
    xml.iP_Thrace,
    xml.iP_Thessaly,
    xml.iP_Thessaloniki,
    xml.iP_Epirus,
    xml.iP_Morea,
    xml.iP_Opsikion,
    xml.iP_Paphlagonia,
    xml.iP_Thrakesion,
    xml.iP_Cilicia,
    xml.iP_Anatolikon,
    xml.iP_Armeniakon,
    xml.iP_Charsianon,
    xml.iP_Colonea,
    xml.iP_Antiochia,
]
tByzantiumNorm = [
    xml.iP_Moesia,
    xml.iP_Serbia,
    xml.iP_Macedonia,
    xml.iP_Arberia,
    xml.iP_Cyprus,
    xml.iP_Crete,
    xml.iP_Rhodes,
    xml.iP_Syria,
    xml.iP_Lebanon,
    xml.iP_Jerusalem,
    xml.iP_Egypt,
    xml.iP_Cyrenaica,
]
tByzantiumOuter = [
    xml.iP_Crimea,
    xml.iP_Arabia,
    xml.iP_Bosnia,
    xml.iP_Slavonia,
    xml.iP_Dalmatia,
    xml.iP_Verona,
    xml.iP_Lombardy,
    xml.iP_Liguria,
    xml.iP_Tuscany,
    xml.iP_Latium,
    xml.iP_Sardinia,
    xml.iP_Corsica,
]
tByzantiumPot2Core = []
tByzantiumPot2Norm = [
    xml.iP_Calabria,
    xml.iP_Apulia,
    xml.iP_Sicily,
    xml.iP_Malta,
    xml.iP_Tripolitania,
    xml.iP_Ifriqiya,
]

tFranceCore = [xml.iP_IleDeFrance, xml.iP_Orleans, xml.iP_Champagne]
tFranceNorm = [xml.iP_Picardy, xml.iP_Normandy, xml.iP_Aquitania, xml.iP_Lorraine]
tFranceOuter = [
    xml.iP_Catalonia,
    xml.iP_Aragon,
    xml.iP_Navarre,
    xml.iP_Netherlands,
    xml.iP_Bavaria,
    xml.iP_Saxony,
    xml.iP_Swabia,
    xml.iP_Franconia,
    xml.iP_Lombardy,
    xml.iP_Liguria,
    xml.iP_Corsica,
]
tFrancePot2Core = []
tFrancePot2Norm = [xml.iP_Bretagne, xml.iP_Provence, xml.iP_Burgundy, xml.iP_Flanders]

tArabiaCore = [xml.iP_Syria, xml.iP_Lebanon, xml.iP_Jerusalem, xml.iP_Arabia]
tArabiaNorm = [xml.iP_Egypt, xml.iP_Cyrenaica]
tArabiaOuter = [
    xml.iP_Oran,
    xml.iP_Algiers,
    xml.iP_Sicily,
    xml.iP_Malta,
    xml.iP_Crete,
    xml.iP_Rhodes,
    xml.iP_Cilicia,
]
tArabiaPot2Core = []
tArabiaPot2Norm = [xml.iP_Antiochia, xml.iP_Cyprus, xml.iP_Ifriqiya, xml.iP_Tripolitania]

tBulgariaCore = [xml.iP_Moesia]
tBulgariaNorm = [xml.iP_Macedonia, xml.iP_Wallachia]
tBulgariaOuter = [
    xml.iP_Serbia,
    xml.iP_Banat,
    xml.iP_Epirus,
    xml.iP_Arberia,
    xml.iP_Constantinople,
]
tBulgariaPot2Core = []
tBulgariaPot2Norm = [xml.iP_Thrace, xml.iP_Thessaloniki]

tCordobaCore = [xml.iP_Andalusia, xml.iP_Valencia, xml.iP_LaMancha]
tCordobaNorm = [xml.iP_Tetouan]
tCordobaOuter = [xml.iP_Leon, xml.iP_Lusitania, xml.iP_Navarre, xml.iP_Castile, xml.iP_Oran]
tCordobaPot2Core = []
tCordobaPot2Norm = [
    xml.iP_Morocco,
    xml.iP_Fez,
    xml.iP_Marrakesh,
    xml.iP_Catalonia,
    xml.iP_Aragon,
    xml.iP_Balears,
]

tVeniceCore = [xml.iP_Verona]
tVeniceNorm = [xml.iP_Dalmatia]
tVeniceOuter = [xml.iP_Epirus, xml.iP_Morea, xml.iP_Rhodes, xml.iP_Constantinople]
tVenicePot2Core = []
tVenicePot2Norm = [xml.iP_Tuscany, xml.iP_Arberia, xml.iP_Crete, xml.iP_Cyprus]

tBurgundyCore = [xml.iP_Burgundy]
tBurgundyNorm = [xml.iP_Provence, xml.iP_Flanders]
tBurgundyOuter = [xml.iP_Lorraine, xml.iP_Swabia, xml.iP_Lombardy, xml.iP_Liguria, xml.iP_Bretagne]
tBurgundyPot2Core = []
tBurgundyPot2Norm = [
    xml.iP_Champagne,
    xml.iP_Picardy,
    xml.iP_IleDeFrance,
    xml.iP_Aquitania,
    xml.iP_Orleans,
    xml.iP_Normandy,
]

tGermanyCore = [xml.iP_Franconia, xml.iP_Lorraine, xml.iP_Bavaria, xml.iP_Swabia, xml.iP_Saxony]
tGermanyNorm = [xml.iP_Brandenburg]
tGermanyOuter = [
    xml.iP_Champagne,
    xml.iP_Picardy,
    xml.iP_Burgundy,
    xml.iP_Liguria,
    xml.iP_Verona,
    xml.iP_Tuscany,
    xml.iP_Austria,
    xml.iP_Moravia,
    xml.iP_Silesia,
    xml.iP_GreaterPoland,
    xml.iP_Carinthia,
]
tGermanyPot2Core = []
tGermanyPot2Norm = [
    xml.iP_Bohemia,
    xml.iP_Holstein,
    xml.iP_Pomerania,
    xml.iP_Netherlands,
    xml.iP_Flanders,
    xml.iP_Lombardy,
]

tNovgorodCore = [xml.iP_Novgorod, xml.iP_Karelia]
tNovgorodNorm = [xml.iP_Rostov, xml.iP_Vologda]
tNovgorodOuter = [xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_Livonia]
tNovgorodPot2Core = []
tNovgorodPot2Norm = [xml.iP_Estonia, xml.iP_Osterland]

tNorwayCore = [xml.iP_Norway, xml.iP_Vestfold]
tNorwayNorm = [xml.iP_Iceland]
tNorwayOuter = [
    xml.iP_Scotland,
    xml.iP_Northumbria,
    xml.iP_Ireland,
    xml.iP_Normandy,
    xml.iP_Svealand,
    xml.iP_Norrland,
    xml.iP_Sicily,
    xml.iP_Apulia,
    xml.iP_Calabria,
    xml.iP_Malta,
]
tNorwayPot2Core = []
tNorwayPot2Norm = [xml.iP_TheIsles, xml.iP_Jamtland]

tKievCore = [xml.iP_Kiev, xml.iP_Sloboda, xml.iP_Pereyaslavl, xml.iP_Chernigov]
tKievNorm = [xml.iP_Podolia, xml.iP_Volhynia]
tKievOuter = [
    xml.iP_Moldova,
    xml.iP_GaliciaPoland,
    xml.iP_Brest,
    xml.iP_Polotsk,
    xml.iP_Novgorod,
    xml.iP_Moscow,
    xml.iP_Murom,
    xml.iP_Simbirsk,
    xml.iP_Crimea,
    xml.iP_Donets,
    xml.iP_Kuban,
]
tKievPot2Core = []
tKievPot2Norm = [xml.iP_Minsk, xml.iP_Smolensk, xml.iP_Zaporizhia]

tHungaryCore = [xml.iP_Hungary, xml.iP_UpperHungary, xml.iP_Pannonia, xml.iP_Transylvania]
tHungaryNorm = [xml.iP_Slavonia, xml.iP_Banat, xml.iP_Bosnia, xml.iP_Dalmatia]
tHungaryOuter = [
    xml.iP_Serbia,
    xml.iP_Wallachia,
    xml.iP_Moldova,
    xml.iP_GaliciaPoland,
    xml.iP_Bavaria,
    xml.iP_Bohemia,
    xml.iP_Silesia,
]
tHungaryPot2Core = []
tHungaryPot2Norm = [xml.iP_Moravia, xml.iP_Austria, xml.iP_Carinthia]

tSpainCore = [xml.iP_Leon, xml.iP_GaliciaSpain, xml.iP_Castile]
tSpainNorm = []
tSpainOuter = [
    xml.iP_Lusitania,
    xml.iP_Catalonia,
    xml.iP_Aragon,
    xml.iP_Balears,
    xml.iP_Aquitania,
    xml.iP_Provence,
    xml.iP_Tetouan,
    xml.iP_Fez,
    xml.iP_Oran,
    xml.iP_Algiers,
    xml.iP_Sardinia,
    xml.iP_Corsica,
    xml.iP_Azores,
    xml.iP_Sicily,
    xml.iP_Calabria,
    xml.iP_Apulia,
]
tSpainPot2Core = []
tSpainPot2Norm = [
    xml.iP_Navarre,
    xml.iP_Andalusia,
    xml.iP_Valencia,
    xml.iP_LaMancha,
    xml.iP_Canaries,
    xml.iP_Madeira,
]

tDenmarkCore = [xml.iP_Denmark, xml.iP_Skaneland]
tDenmarkNorm = []
tDenmarkOuter = [
    xml.iP_Gotaland,
    xml.iP_Svealand,
    xml.iP_Northumbria,
    xml.iP_Mercia,
    xml.iP_EastAnglia,
    xml.iP_London,
    xml.iP_Brandenburg,
    xml.iP_Norway,
    xml.iP_Vestfold,
    xml.iP_Normandy,
    xml.iP_Sicily,
    xml.iP_Apulia,
    xml.iP_Calabria,
    xml.iP_Malta,
]
tDenmarkPot2Core = []
tDenmarkPot2Norm = [xml.iP_Estonia, xml.iP_Gotland, xml.iP_Holstein]

tScotlandCore = [xml.iP_Scotland]
tScotlandNorm = [xml.iP_TheIsles]
tScotlandOuter = [xml.iP_Ireland, xml.iP_Mercia, xml.iP_Wales]
tScotlandPot2Core = []
tScotlandPot2Norm = [xml.iP_Northumbria]

tPolandCore = [xml.iP_GreaterPoland, xml.iP_LesserPoland, xml.iP_Masovia]
tPolandNorm = [xml.iP_Brest, xml.iP_GaliciaPoland]
tPolandOuter = [
    xml.iP_Prussia,
    xml.iP_Lithuania,
    xml.iP_Polotsk,
    xml.iP_Minsk,
    xml.iP_Volhynia,
    xml.iP_Podolia,
    xml.iP_Moldova,
    xml.iP_Kiev,
]
tPolandPot2Core = []
tPolandPot2Norm = [xml.iP_Pomerania, xml.iP_Silesia, xml.iP_Suvalkija]

tGenoaCore = [xml.iP_Liguria]
tGenoaNorm = [xml.iP_Corsica, xml.iP_Sardinia]
tGenoaOuter = [
    xml.iP_Constantinople,
    xml.iP_Crete,
    xml.iP_Cyprus,
    xml.iP_Morea,
    xml.iP_Armeniakon,
    xml.iP_Paphlagonia,
    xml.iP_Thrakesion,
]
tGenoaPot2Core = []
tGenoaPot2Norm = [
    xml.iP_Sicily,
    xml.iP_Malta,
    xml.iP_Lombardy,
    xml.iP_Tuscany,
    xml.iP_Rhodes,
    xml.iP_Crimea,
]

tMoroccoCore = [xml.iP_Marrakesh, xml.iP_Morocco, xml.iP_Fez]
tMoroccoNorm = [xml.iP_Tetouan]
tMoroccoOuter = [
    xml.iP_Ifriqiya,
    xml.iP_Andalusia,
    xml.iP_Valencia,
    xml.iP_Tripolitania,
    xml.iP_Sahara,
]
tMoroccoPot2Core = []
tMoroccoPot2Norm = [xml.iP_Oran, xml.iP_Algiers]

tEnglandCore = [xml.iP_London, xml.iP_EastAnglia, xml.iP_Mercia, xml.iP_Wessex]
tEnglandNorm = [xml.iP_Northumbria]
tEnglandOuter = [
    xml.iP_IleDeFrance,
    xml.iP_Bretagne,
    xml.iP_Aquitania,
    xml.iP_Orleans,
    xml.iP_Champagne,
    xml.iP_Flanders,
    xml.iP_Normandy,
    xml.iP_Picardy,
    xml.iP_Scotland,
    xml.iP_TheIsles,
    xml.iP_Ireland,
]
tEnglandPot2Core = []
tEnglandPot2Norm = [xml.iP_Wales]

tPortugalCore = [xml.iP_Lusitania]
tPortugalNorm = [xml.iP_Azores]
tPortugalOuter = [xml.iP_Morocco, xml.iP_Tetouan, xml.iP_Leon, xml.iP_GaliciaSpain]
tPortugalPot2Core = []
tPortugalPot2Norm = [xml.iP_Madeira, xml.iP_Canaries, xml.iP_Andalusia]

tAragonCore = [xml.iP_Aragon, xml.iP_Catalonia, xml.iP_Balears, xml.iP_Valencia]
tAragonNorm = []
tAragonOuter = [xml.iP_Castile, xml.iP_Provence, xml.iP_Corsica, xml.iP_Thessaly]
tAragonPot2Core = []
tAragonPot2Norm = [
    xml.iP_Navarre,
    xml.iP_Andalusia,
    xml.iP_LaMancha,
    xml.iP_Sardinia,
    xml.iP_Sicily,
    xml.iP_Apulia,
    xml.iP_Calabria,
    xml.iP_Malta,
]

tSwedenCore = [xml.iP_Norrland, xml.iP_Svealand]
tSwedenNorm = [xml.iP_Gotaland, xml.iP_Gotland]
tSwedenOuter = [
    xml.iP_Skaneland,
    xml.iP_Vestfold,
    xml.iP_Pomerania,
    xml.iP_Livonia,
    xml.iP_Prussia,
    xml.iP_Novgorod,
]
tSwedenPot2Core = []
tSwedenPot2Norm = [xml.iP_Jamtland, xml.iP_Osterland, xml.iP_Karelia, xml.iP_Estonia]

tPrussiaCore = [xml.iP_Prussia]
tPrussiaNorm = []
tPrussiaOuter = [
    xml.iP_Brandenburg,
    xml.iP_Estonia,
    xml.iP_Gotland,
    xml.iP_Lithuania,
    xml.iP_Suvalkija,
]
tPrussiaPot2Core = []
tPrussiaPot2Norm = [xml.iP_Pomerania, xml.iP_Livonia]

tLithuaniaCore = [xml.iP_Lithuania]
tLithuaniaNorm = [xml.iP_Suvalkija, xml.iP_Minsk, xml.iP_Polotsk]
tLithuaniaOuter = [
    xml.iP_GreaterPoland,
    xml.iP_LesserPoland,
    xml.iP_Masovia,
    xml.iP_GaliciaPoland,
    xml.iP_Sloboda,
    xml.iP_Pereyaslavl,
    xml.iP_Livonia,
    xml.iP_Estonia,
    xml.iP_Novgorod,
    xml.iP_Smolensk,
    xml.iP_Chernigov,
]
tLithuaniaPot2Core = []
tLithuaniaPot2Norm = [xml.iP_Brest, xml.iP_Podolia, xml.iP_Volhynia, xml.iP_Kiev]

tAustriaCore = [xml.iP_Austria, xml.iP_Carinthia]
tAustriaNorm = [xml.iP_Bohemia, xml.iP_Moravia]
tAustriaOuter = [
    xml.iP_Verona,
    xml.iP_Hungary,
    xml.iP_Transylvania,
    xml.iP_Slavonia,
    xml.iP_Dalmatia,
    xml.iP_LesserPoland,
    xml.iP_GaliciaPoland,
    xml.iP_Netherlands,
    xml.iP_Flanders,
]
tAustriaPot2Core = []
tAustriaPot2Norm = [xml.iP_Bavaria, xml.iP_Silesia, xml.iP_Pannonia, xml.iP_UpperHungary]

tTurkeyCore = [
    xml.iP_Opsikion,
    xml.iP_Thrakesion,
    xml.iP_Paphlagonia,
    xml.iP_Anatolikon,
    xml.iP_Constantinople,
]
tTurkeyNorm = [xml.iP_Thrace, xml.iP_Armeniakon, xml.iP_Charsianon, xml.iP_Cilicia]
tTurkeyOuter = [
    xml.iP_Thessaly,
    xml.iP_Epirus,
    xml.iP_Morea,
    xml.iP_Arberia,
    xml.iP_Wallachia,
    xml.iP_Serbia,
    xml.iP_Bosnia,
    xml.iP_Banat,
    xml.iP_Slavonia,
    xml.iP_Pannonia,
    xml.iP_Hungary,
    xml.iP_Transylvania,
    xml.iP_Moldova,
    xml.iP_Crimea,
    xml.iP_Crete,
    xml.iP_Cyrenaica,
    xml.iP_Tripolitania,
    xml.iP_Kuban,
]
tTurkeyPot2Core = []
tTurkeyPot2Norm = [
    xml.iP_Colonea,
    xml.iP_Antiochia,
    xml.iP_Syria,
    xml.iP_Lebanon,
    xml.iP_Jerusalem,
    xml.iP_Egypt,
    xml.iP_Arabia,
    xml.iP_Macedonia,
    xml.iP_Thessaloniki,
    xml.iP_Moesia,
    xml.iP_Cyprus,
    xml.iP_Rhodes,
]

tMoscowCore = [xml.iP_Moscow, xml.iP_Murom, xml.iP_Rostov, xml.iP_Smolensk]
tMoscowNorm = [xml.iP_NizhnyNovgorod, xml.iP_Simbirsk, xml.iP_Pereyaslavl, xml.iP_Chernigov]
tMoscowOuter = [
    xml.iP_Crimea,
    xml.iP_Moldova,
    xml.iP_GaliciaPoland,
    xml.iP_Kuban,
    xml.iP_Brest,
    xml.iP_Lithuania,
    xml.iP_Livonia,
    xml.iP_Estonia,
    xml.iP_Karelia,
    xml.iP_Osterland,
    xml.iP_Prussia,
    xml.iP_Suvalkija,
]
tMoscowPot2Core = []
tMoscowPot2Norm = [
    xml.iP_Novgorod,
    xml.iP_Vologda,
    xml.iP_Kiev,
    xml.iP_Minsk,
    xml.iP_Polotsk,
    xml.iP_Volhynia,
    xml.iP_Podolia,
    xml.iP_Donets,
    xml.iP_Sloboda,
    xml.iP_Zaporizhia,
]

tDutchCore = [xml.iP_Netherlands]
tDutchNorm = [xml.iP_Flanders]
tDutchOuter = []
tDutchPot2Core = []
tDutchPot2Norm = []


class ProvinceManager:
    def __init__(self):
        self.tCoreProvinces = {
            Consts.iByzantium: tByzantiumCore,
            Consts.iFrankia: tFranceCore,
            Consts.iArabia: tArabiaCore,
            Consts.iBulgaria: tBulgariaCore,
            Consts.iCordoba: tCordobaCore,
            Consts.iVenecia: tVeniceCore,
            Consts.iBurgundy: tBurgundyCore,
            Consts.iGermany: tGermanyCore,
            Consts.iNovgorod: tNovgorodCore,
            Consts.iNorway: tNorwayCore,
            Consts.iKiev: tKievCore,
            Consts.iHungary: tHungaryCore,
            Consts.iSpain: tSpainCore,
            Consts.iDenmark: tDenmarkCore,
            Consts.iScotland: tScotlandCore,
            Consts.iPoland: tPolandCore,
            Consts.iGenoa: tGenoaCore,
            Consts.iMorocco: tMoroccoCore,
            Consts.iEngland: tEnglandCore,
            Consts.iPortugal: tPortugalCore,
            Consts.iAragon: tAragonCore,
            Consts.iSweden: tSwedenCore,
            Consts.iPrussia: tPrussiaCore,
            Consts.iLithuania: tLithuaniaCore,
            Consts.iAustria: tAustriaCore,
            Consts.iTurkey: tTurkeyCore,
            Consts.iMoscow: tMoscowCore,
            Consts.iDutch: tDutchCore,
        }

        self.tNormProvinces = {
            Consts.iByzantium: tByzantiumNorm,
            Consts.iFrankia: tFranceNorm,
            Consts.iArabia: tArabiaNorm,
            Consts.iBulgaria: tBulgariaNorm,
            Consts.iCordoba: tCordobaNorm,
            Consts.iVenecia: tVeniceNorm,
            Consts.iBurgundy: tBurgundyNorm,
            Consts.iGermany: tGermanyNorm,
            Consts.iNovgorod: tNovgorodNorm,
            Consts.iNorway: tNorwayNorm,
            Consts.iKiev: tKievNorm,
            Consts.iHungary: tHungaryNorm,
            Consts.iSpain: tSpainNorm,
            Consts.iDenmark: tDenmarkNorm,
            Consts.iScotland: tScotlandNorm,
            Consts.iPoland: tPolandNorm,
            Consts.iGenoa: tGenoaNorm,
            Consts.iMorocco: tMoroccoNorm,
            Consts.iEngland: tEnglandNorm,
            Consts.iPortugal: tPortugalNorm,
            Consts.iAragon: tAragonNorm,
            Consts.iSweden: tSwedenNorm,
            Consts.iPrussia: tPrussiaNorm,
            Consts.iLithuania: tLithuaniaNorm,
            Consts.iAustria: tAustriaNorm,
            Consts.iTurkey: tTurkeyNorm,
            Consts.iMoscow: tMoscowNorm,
            Consts.iDutch: tDutchNorm,
        }

        self.tOuterProvinces = {
            Consts.iByzantium: tByzantiumOuter,
            Consts.iFrankia: tFranceOuter,
            Consts.iArabia: tArabiaOuter,
            Consts.iBulgaria: tBulgariaOuter,
            Consts.iCordoba: tCordobaOuter,
            Consts.iVenecia: tVeniceOuter,
            Consts.iBurgundy: tBurgundyOuter,
            Consts.iGermany: tGermanyOuter,
            Consts.iNovgorod: tNovgorodOuter,
            Consts.iNorway: tNorwayOuter,
            Consts.iKiev: tKievOuter,
            Consts.iHungary: tHungaryOuter,
            Consts.iSpain: tSpainOuter,
            Consts.iDenmark: tDenmarkOuter,
            Consts.iScotland: tScotlandOuter,
            Consts.iPoland: tPolandOuter,
            Consts.iGenoa: tGenoaOuter,
            Consts.iMorocco: tMoroccoOuter,
            Consts.iEngland: tEnglandOuter,
            Consts.iPortugal: tPortugalOuter,
            Consts.iAragon: tAragonOuter,
            Consts.iSweden: tSwedenOuter,
            Consts.iPrussia: tPrussiaOuter,
            Consts.iLithuania: tLithuaniaOuter,
            Consts.iAustria: tAustriaOuter,
            Consts.iTurkey: tTurkeyOuter,
            Consts.iMoscow: tMoscowOuter,
            Consts.iDutch: tDutchOuter,
        }

        self.tPot2CoreProvinces = {
            Consts.iByzantium: tByzantiumPot2Core,
            Consts.iFrankia: tFrancePot2Core,
            Consts.iArabia: tArabiaPot2Core,
            Consts.iBulgaria: tBulgariaPot2Core,
            Consts.iCordoba: tCordobaPot2Core,
            Consts.iVenecia: tVenicePot2Core,
            Consts.iBurgundy: tBurgundyPot2Core,
            Consts.iGermany: tGermanyPot2Core,
            Consts.iNovgorod: tNovgorodPot2Core,
            Consts.iNorway: tNorwayPot2Core,
            Consts.iKiev: tKievPot2Core,
            Consts.iHungary: tHungaryPot2Core,
            Consts.iSpain: tSpainPot2Core,
            Consts.iDenmark: tDenmarkPot2Core,
            Consts.iScotland: tScotlandPot2Core,
            Consts.iPoland: tPolandPot2Core,
            Consts.iGenoa: tGenoaPot2Core,
            Consts.iMorocco: tMoroccoPot2Core,
            Consts.iEngland: tEnglandPot2Core,
            Consts.iPortugal: tPortugalPot2Core,
            Consts.iAragon: tAragonPot2Core,
            Consts.iSweden: tSwedenPot2Core,
            Consts.iPrussia: tPrussiaPot2Core,
            Consts.iLithuania: tLithuaniaPot2Core,
            Consts.iAustria: tAustriaPot2Core,
            Consts.iTurkey: tTurkeyPot2Core,
            Consts.iMoscow: tMoscowPot2Core,
            Consts.iDutch: tDutchPot2Core,
        }

        self.tPot2NormProvinces = {
            Consts.iByzantium: tByzantiumPot2Norm,
            Consts.iFrankia: tFrancePot2Norm,
            Consts.iArabia: tArabiaPot2Norm,
            Consts.iBulgaria: tBulgariaPot2Norm,
            Consts.iCordoba: tCordobaPot2Norm,
            Consts.iVenecia: tVenicePot2Norm,
            Consts.iBurgundy: tBurgundyPot2Norm,
            Consts.iGermany: tGermanyPot2Norm,
            Consts.iNovgorod: tNovgorodPot2Norm,
            Consts.iNorway: tNorwayPot2Norm,
            Consts.iKiev: tKievPot2Norm,
            Consts.iHungary: tHungaryPot2Norm,
            Consts.iSpain: tSpainPot2Norm,
            Consts.iDenmark: tDenmarkPot2Norm,
            Consts.iScotland: tScotlandPot2Norm,
            Consts.iPoland: tPolandPot2Norm,
            Consts.iGenoa: tGenoaPot2Norm,
            Consts.iMorocco: tMoroccoPot2Norm,
            Consts.iEngland: tEnglandPot2Norm,
            Consts.iPortugal: tPortugalPot2Norm,
            Consts.iAragon: tAragonPot2Norm,
            Consts.iSweden: tSwedenPot2Norm,
            Consts.iPrussia: tPrussiaPot2Norm,
            Consts.iLithuania: tLithuaniaPot2Norm,
            Consts.iAustria: tAustriaPot2Norm,
            Consts.iTurkey: tTurkeyPot2Norm,
            Consts.iMoscow: tMoscowPot2Norm,
            Consts.iDutch: tDutchPot2Norm,
        }

    def setup(self):
        # set the initial situation for all players
        for iPlayer in range(Consts.iNumPlayers - 1):  # this discounts the Pope
            pPlayer = gc.getPlayer(iPlayer)
            for iProv in self.tCoreProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, Consts.iProvinceCore)
            for iProv in self.tNormProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, Consts.iProvinceNatural)
            for iProv in self.tOuterProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, Consts.iProvinceOuter)
            for iProv in self.tPot2CoreProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, Consts.iProvincePotential)
            for iProv in self.tPot2NormProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, Consts.iProvincePotential)
        # update provinces for the 1200 AD Scenario
        if utils.getScenario() == Scenario.i1200AD:
            for iPlayer in range(Consts.iNumPlayers - 1):
                if CIV_BIRTHDATE[get_civ_by_id(iPlayer)] < xml.i1200AD:
                    self.onSpawn(iPlayer)

    def checkTurn(self, iGameTurn):
        # Norse provinces switch back to unstable after the fall of the Norman Kingdom of Sicily
        if iGameTurn == xml.i1194AD + 1:
            pNorway.setProvinceType(xml.iP_Apulia, Consts.iProvinceNone)
            pNorway.setProvinceType(xml.iP_Calabria, Consts.iProvinceNone)
            pNorway.setProvinceType(xml.iP_Sicily, Consts.iProvinceNone)
            pNorway.setProvinceType(xml.iP_Malta, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_Apulia, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_Calabria, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_Sicily, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_Malta, Consts.iProvinceNone)
        # Prussia direction change
        elif iGameTurn == xml.i1618AD:
            pPrussia.setProvinceType(xml.iP_Estonia, Consts.iProvinceNone)
            pPrussia.setProvinceType(xml.iP_Lithuania, Consts.iProvinceNone)
            pPrussia.setProvinceType(xml.iP_Suvalkija, Consts.iProvinceNone)
            pPrussia.setProvinceType(xml.iP_Livonia, Consts.iProvinceOuter)
            pPrussia.setProvinceType(xml.iP_Pomerania, Consts.iProvinceNatural)
            pPrussia.setProvinceType(xml.iP_Brandenburg, Consts.iProvinceNatural)
            pPrussia.setProvinceType(xml.iP_Silesia, Consts.iProvincePotential)
            pPrussia.setProvinceType(xml.iP_GreaterPoland, Consts.iProvinceOuter)
            print("Yes! Prussia can into Germany!")

    def onCityBuilt(self, iPlayer, x, y):
        if iPlayer >= Consts.iNumPlayers - 1:  # Pope, indies, barbs
            return
        pPlayer = gc.getPlayer(iPlayer)
        iProv = RFCEMaps.tProvinceMap[y][x]
        if pPlayer.getProvinceType(iProv) == Consts.iProvincePotential:
            if iProv in self.tPot2NormProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, Consts.iProvinceNatural)
                utils.refreshStabilityOverlay()  # refresh the stability overlay
            elif iProv in self.tPot2CoreProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, Consts.iProvinceCore)
                utils.refreshStabilityOverlay()  # refresh the stability overlay
            # Absinthe: bug if we tie potential only to the preset status of provinces
            else:  # also update if it was changed to be a potential province later in the game
                pPlayer.setProvinceType(iProv, Consts.iProvinceNatural)
                utils.refreshStabilityOverlay()  # refresh the stability overlay

    def onCityAcquired(self, owner, iPlayer, city, bConquest, bTrade):
        if iPlayer >= Consts.iNumPlayers - 1:  # Pope, indies, barbs
            return
        pPlayer = gc.getPlayer(iPlayer)
        iProv = city.getProvince()
        if pPlayer.getProvinceType(iProv) == Consts.iProvincePotential:
            if iProv in self.tPot2NormProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, Consts.iProvinceNatural)
                utils.refreshStabilityOverlay()  # refresh the stability overlay
            elif iProv in self.tPot2CoreProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, Consts.iProvinceCore)
                utils.refreshStabilityOverlay()  # refresh the stability overlay
            # Absinthe: bug if we tie potential only to the preset status of provinces
            else:  # also update if it was changed to be a potential province later in the game
                pPlayer.setProvinceType(iProv, Consts.iProvinceNatural)
                utils.refreshStabilityOverlay()  # refresh the stability overlay

    def onCityRazed(self, iOwner, iPlayer, city):
        pass

    def updatePotential(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        for city in utils.getCityList(iPlayer):
            iProv = city.getProvince()
            if pPlayer.getProvinceType(iProv) == Consts.iProvincePotential:
                if iProv in self.tPot2NormProvinces[iPlayer]:
                    pPlayer.setProvinceType(iProv, Consts.iProvinceNatural)
                elif iProv in self.tPot2CoreProvinces[iPlayer]:
                    pPlayer.setProvinceType(iProv, Consts.iProvinceCore)
                # Absinthe: bug if we tie potential only to the preset status of provinces
                else:  # also update if it was changed to be a potential province later in the game
                    pPlayer.setProvinceType(iProv, Consts.iProvinceNatural)
        utils.refreshStabilityOverlay()  # refresh the stability overlay

    def onRespawn(self, iPlayer):
        # Absinthe: reset the original potential provinces, but only if they wasn't changed to something entirely different later on
        pPlayer = gc.getPlayer(iPlayer)
        for iProv in self.tPot2CoreProvinces[iPlayer]:
            if pPlayer.getProvinceType(iProv) == Consts.iProvinceCore:
                pPlayer.setProvinceType(iProv, Consts.iProvincePotential)
        for iProv in self.tPot2NormProvinces[iPlayer]:
            if pPlayer.getProvinceType(iProv) == Consts.iProvinceNatural:
                pPlayer.setProvinceType(iProv, Consts.iProvincePotential)

        # Absinthe: special respawn conditions
        # if ( iPlayer == iArabia ):
        # 	self.resetProvinces(iPlayer)
        if iPlayer == Consts.iCordoba:
            for iProv in range(xml.iP_MaxNumberOfProvinces):
                pCordoba.setProvinceType(iProv, Consts.iProvinceNone)
            pCordoba.setProvinceType(xml.iP_Ifriqiya, Consts.iProvinceCore)
            pCordoba.setProvinceType(xml.iP_Algiers, Consts.iProvinceNatural)
            pCordoba.setProvinceType(xml.iP_Oran, Consts.iProvinceOuter)
            pCordoba.setProvinceType(xml.iP_Tripolitania, Consts.iProvinceOuter)
            pCordoba.setProvinceType(xml.iP_Tetouan, Consts.iProvinceOuter)
            pCordoba.setProvinceType(xml.iP_Morocco, Consts.iProvinceOuter)
            pCordoba.setProvinceType(xml.iP_Fez, Consts.iProvinceOuter)

    def resetProvinces(self, iPlayer):
        # Absinthe: keep in mind that this will reset all to the initial status, so won't take later province changes into account
        pPlayer = gc.getPlayer(iPlayer)
        for iProv in range(xml.iP_MaxNumberOfProvinces):
            pPlayer.setProvinceType(iProv, Consts.iProvinceNone)
        for iProv in self.tCoreProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, Consts.iProvinceCore)
        for iProv in self.tNormProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, Consts.iProvinceNatural)
        for iProv in self.tOuterProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, Consts.iProvinceOuter)
        for iProv in self.tPot2CoreProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, Consts.iProvincePotential)
        for iProv in self.tPot2NormProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, Consts.iProvincePotential)

    def onSpawn(self, iPlayer):
        # when a new nations spawns, old nations in the region should lose some of their provinces
        if iPlayer == Consts.iArabia:
            pByzantium.setProvinceType(xml.iP_Cyrenaica, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Tripolitania, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Ifriqiya, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Egypt, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Arabia, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Syria, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Lebanon, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Jerusalem, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Antiochia, Consts.iProvinceNatural)
            pByzantium.setProvinceType(xml.iP_Cilicia, Consts.iProvinceNatural)
            pByzantium.setProvinceType(xml.iP_Charsianon, Consts.iProvinceNatural)
            pByzantium.setProvinceType(xml.iP_Colonea, Consts.iProvinceNatural)
        elif iPlayer == Consts.iBulgaria:
            pByzantium.setProvinceType(xml.iP_Serbia, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Moesia, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Thrace, Consts.iProvinceNatural)
        elif iPlayer == Consts.iVenecia:
            pByzantium.setProvinceType(xml.iP_Dalmatia, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Bosnia, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Slavonia, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Verona, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Tuscany, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Lombardy, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Liguria, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Corsica, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Sardinia, Consts.iProvinceNone)
            pByzantium.setProvinceType(xml.iP_Latium, Consts.iProvinceNone)
        elif iPlayer == Consts.iBurgundy:
            # these areas flip to Burgundy, so resetting them to Potential won't cause any issues
            pFrankia.setProvinceType(xml.iP_Provence, Consts.iProvincePotential)
            pFrankia.setProvinceType(xml.iP_Burgundy, Consts.iProvincePotential)
        elif iPlayer == Consts.iGermany:
            pFrankia.setProvinceType(xml.iP_Lorraine, Consts.iProvinceOuter)
            pFrankia.setProvinceType(xml.iP_Bavaria, Consts.iProvinceNone)
            pFrankia.setProvinceType(xml.iP_Franconia, Consts.iProvinceNone)
            pFrankia.setProvinceType(xml.iP_Saxony, Consts.iProvinceNone)
            pFrankia.setProvinceType(xml.iP_Netherlands, Consts.iProvinceNone)
        elif iPlayer == Consts.iHungary:
            pBulgaria.setProvinceType(xml.iP_Banat, Consts.iProvinceNone)
            pBulgaria.setProvinceType(xml.iP_Wallachia, Consts.iProvinceOuter)
        elif iPlayer == Consts.iSpain:
            pCordoba.setProvinceType(xml.iP_LaMancha, Consts.iProvinceNatural)
        elif iPlayer == Consts.iMorocco:
            pCordoba.setProvinceType(xml.iP_Morocco, Consts.iProvinceNone)
            pCordoba.setProvinceType(xml.iP_Marrakesh, Consts.iProvinceNone)
            pCordoba.setProvinceType(xml.iP_Fez, Consts.iProvinceOuter)
            pCordoba.setProvinceType(xml.iP_Tetouan, Consts.iProvinceOuter)
        elif iPlayer == Consts.iEngland:
            pFrankia.setProvinceType(
                xml.iP_Normandy, Consts.iProvincePotential
            )  # it flips to England, so resetting them to Potential won't cause any issues
            pScotland.setProvinceType(xml.iP_Northumbria, Consts.iProvinceOuter)
            pScotland.setProvinceType(xml.iP_Mercia, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_Northumbria, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_Mercia, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_EastAnglia, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_London, Consts.iProvinceNone)
        elif iPlayer == Consts.iAragon:
            pByzantium.setProvinceType(xml.iP_Apulia, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Calabria, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Sicily, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Malta, Consts.iProvinceOuter)
            pCordoba.setProvinceType(xml.iP_Aragon, Consts.iProvinceOuter)
            pCordoba.setProvinceType(xml.iP_Catalonia, Consts.iProvinceOuter)
            pCordoba.setProvinceType(xml.iP_Valencia, Consts.iProvinceNatural)
            pCordoba.setProvinceType(xml.iP_Balears, Consts.iProvinceOuter)
        elif iPlayer == Consts.iSweden:
            pNorway.setProvinceType(xml.iP_Svealand, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_Gotaland, Consts.iProvinceNone)
            pDenmark.setProvinceType(xml.iP_Svealand, Consts.iProvinceNone)
            pNovgorod.setProvinceType(xml.iP_Osterland, Consts.iProvinceOuter)
        elif iPlayer == Consts.iAustria:
            pHungary.setProvinceType(xml.iP_Carinthia, Consts.iProvinceOuter)
            pHungary.setProvinceType(xml.iP_Austria, Consts.iProvinceOuter)
            pHungary.setProvinceType(xml.iP_Moravia, Consts.iProvinceOuter)
            pHungary.setProvinceType(xml.iP_Bavaria, Consts.iProvinceNone)
            pGermany.setProvinceType(xml.iP_Bavaria, Consts.iProvinceOuter)
            pGermany.setProvinceType(xml.iP_Bohemia, Consts.iProvinceOuter)
            pSpain.setProvinceType(xml.iP_Netherlands, Consts.iProvinceOuter)
            pSpain.setProvinceType(xml.iP_Flanders, Consts.iProvinceOuter)
        elif iPlayer == Consts.iTurkey:
            pByzantium.setProvinceType(xml.iP_Antiochia, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Cilicia, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Charsianon, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Colonea, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Armeniakon, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Cyprus, Consts.iProvinceOuter)
            pByzantium.setProvinceType(xml.iP_Anatolikon, Consts.iProvinceNatural)
            pByzantium.setProvinceType(xml.iP_Opsikion, Consts.iProvinceNatural)
            pByzantium.setProvinceType(xml.iP_Thrakesion, Consts.iProvinceNatural)
            pByzantium.setProvinceType(xml.iP_Paphlagonia, Consts.iProvinceNatural)
            pHungary.setProvinceType(xml.iP_Dalmatia, Consts.iProvinceOuter)
            pHungary.setProvinceType(xml.iP_Bosnia, Consts.iProvinceOuter)
            pHungary.setProvinceType(xml.iP_Banat, Consts.iProvinceOuter)
        elif iPlayer == Consts.iMoscow:
            pNovgorod.setProvinceType(xml.iP_Rostov, Consts.iProvinceOuter)
            pNovgorod.setProvinceType(xml.iP_Smolensk, Consts.iProvinceNone)
        elif iPlayer == Consts.iDutch:
            pSpain.setProvinceType(xml.iP_Netherlands, Consts.iProvinceNone)
            pSpain.setProvinceType(xml.iP_Flanders, Consts.iProvinceNone)
            pAustria.setProvinceType(xml.iP_Netherlands, Consts.iProvinceNone)
            pAustria.setProvinceType(xml.iP_Flanders, Consts.iProvinceNone)

        utils.refreshStabilityOverlay()  # refresh the stability overlay
