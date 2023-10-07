# RFC Europe - Province manager

from CvPythonExtensions import *
from CoreData import CIVILIZATIONS
import XMLConsts as xml
import RFCEMaps
import RFCUtils  # Absinthe
import PyHelpers  # Absinthe

from TimelineData import CIV_BIRTHDATE, DateTurn
from CoreTypes import Civ, Scenario, ProvinceTypes

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer  # Absinthe
utils = RFCUtils.RFCUtils()  # Absinthe

# TODO clean this
pBurgundy = gc.getPlayer(Civ.BURGUNDY.value)
pByzantium = gc.getPlayer(Civ.BYZANTIUM.value)
pFrankia = gc.getPlayer(Civ.FRANCE.value)
pArabia = gc.getPlayer(Civ.ARABIA.value)
pBulgaria = gc.getPlayer(Civ.BULGARIA.value)
pCordoba = gc.getPlayer(Civ.CORDOBA.value)
pSpain = gc.getPlayer(Civ.CASTILLE.value)
pNorway = gc.getPlayer(Civ.NORWAY.value)
pDenmark = gc.getPlayer(Civ.DENMARK.value)
pVenecia = gc.getPlayer(Civ.VENECIA.value)
pNovgorod = gc.getPlayer(Civ.NOVGOROD.value)
pKiev = gc.getPlayer(Civ.KIEV.value)
pHungary = gc.getPlayer(Civ.HUNGARY.value)
pGermany = gc.getPlayer(Civ.GERMANY.value)
pScotland = gc.getPlayer(Civ.SCOTLAND.value)
pPoland = gc.getPlayer(Civ.POLAND.value)
pMoscow = gc.getPlayer(Civ.MOSCOW.value)
pGenoa = gc.getPlayer(Civ.GENOA.value)
pMorocco = gc.getPlayer(Civ.MOROCCO.value)
pEngland = gc.getPlayer(Civ.ENGLAND.value)
pPortugal = gc.getPlayer(Civ.PORTUGAL.value)
pAragon = gc.getPlayer(Civ.ARAGON.value)
pPrussia = gc.getPlayer(Civ.PRUSSIA.value)
pLithuania = gc.getPlayer(Civ.LITHUANIA.value)
pAustria = gc.getPlayer(Civ.AUSTRIA.value)
pTurkey = gc.getPlayer(Civ.OTTOMAN.value)
pSweden = gc.getPlayer(Civ.SWEDEN.value)
pDutch = gc.getPlayer(Civ.DUTCH.value)
pPope = gc.getPlayer(Civ.POPE.value)


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
            Civ.BYZANTIUM.value: tByzantiumCore,
            Civ.FRANCE.value: tFranceCore,
            Civ.ARABIA.value: tArabiaCore,
            Civ.BULGARIA.value: tBulgariaCore,
            Civ.CORDOBA.value: tCordobaCore,
            Civ.VENECIA.value: tVeniceCore,
            Civ.BURGUNDY.value: tBurgundyCore,
            Civ.GERMANY.value: tGermanyCore,
            Civ.NOVGOROD.value: tNovgorodCore,
            Civ.NORWAY.value: tNorwayCore,
            Civ.KIEV.value: tKievCore,
            Civ.HUNGARY.value: tHungaryCore,
            Civ.CASTILLE.value: tSpainCore,
            Civ.DENMARK.value: tDenmarkCore,
            Civ.SCOTLAND.value: tScotlandCore,
            Civ.POLAND.value: tPolandCore,
            Civ.GENOA.value: tGenoaCore,
            Civ.MOROCCO.value: tMoroccoCore,
            Civ.ENGLAND.value: tEnglandCore,
            Civ.PORTUGAL.value: tPortugalCore,
            Civ.ARAGON.value: tAragonCore,
            Civ.SWEDEN.value: tSwedenCore,
            Civ.PRUSSIA.value: tPrussiaCore,
            Civ.LITHUANIA.value: tLithuaniaCore,
            Civ.AUSTRIA.value: tAustriaCore,
            Civ.OTTOMAN.value: tTurkeyCore,
            Civ.MOSCOW.value: tMoscowCore,
            Civ.DUTCH.value: tDutchCore,
        }

        self.tNormProvinces = {
            Civ.BYZANTIUM.value: tByzantiumNorm,
            Civ.FRANCE.value: tFranceNorm,
            Civ.ARABIA.value: tArabiaNorm,
            Civ.BULGARIA.value: tBulgariaNorm,
            Civ.CORDOBA.value: tCordobaNorm,
            Civ.VENECIA.value: tVeniceNorm,
            Civ.BURGUNDY.value: tBurgundyNorm,
            Civ.GERMANY.value: tGermanyNorm,
            Civ.NOVGOROD.value: tNovgorodNorm,
            Civ.NORWAY.value: tNorwayNorm,
            Civ.KIEV.value: tKievNorm,
            Civ.HUNGARY.value: tHungaryNorm,
            Civ.CASTILLE.value: tSpainNorm,
            Civ.DENMARK.value: tDenmarkNorm,
            Civ.SCOTLAND.value: tScotlandNorm,
            Civ.POLAND.value: tPolandNorm,
            Civ.GENOA.value: tGenoaNorm,
            Civ.MOROCCO.value: tMoroccoNorm,
            Civ.ENGLAND.value: tEnglandNorm,
            Civ.PORTUGAL.value: tPortugalNorm,
            Civ.ARAGON.value: tAragonNorm,
            Civ.SWEDEN.value: tSwedenNorm,
            Civ.PRUSSIA.value: tPrussiaNorm,
            Civ.LITHUANIA.value: tLithuaniaNorm,
            Civ.AUSTRIA.value: tAustriaNorm,
            Civ.OTTOMAN.value: tTurkeyNorm,
            Civ.MOSCOW.value: tMoscowNorm,
            Civ.DUTCH.value: tDutchNorm,
        }

        self.tOuterProvinces = {
            Civ.BYZANTIUM.value: tByzantiumOuter,
            Civ.FRANCE.value: tFranceOuter,
            Civ.ARABIA.value: tArabiaOuter,
            Civ.BULGARIA.value: tBulgariaOuter,
            Civ.CORDOBA.value: tCordobaOuter,
            Civ.VENECIA.value: tVeniceOuter,
            Civ.BURGUNDY.value: tBurgundyOuter,
            Civ.GERMANY.value: tGermanyOuter,
            Civ.NOVGOROD.value: tNovgorodOuter,
            Civ.NORWAY.value: tNorwayOuter,
            Civ.KIEV.value: tKievOuter,
            Civ.HUNGARY.value: tHungaryOuter,
            Civ.CASTILLE.value: tSpainOuter,
            Civ.DENMARK.value: tDenmarkOuter,
            Civ.SCOTLAND.value: tScotlandOuter,
            Civ.POLAND.value: tPolandOuter,
            Civ.GENOA.value: tGenoaOuter,
            Civ.MOROCCO.value: tMoroccoOuter,
            Civ.ENGLAND.value: tEnglandOuter,
            Civ.PORTUGAL.value: tPortugalOuter,
            Civ.ARAGON.value: tAragonOuter,
            Civ.SWEDEN.value: tSwedenOuter,
            Civ.PRUSSIA.value: tPrussiaOuter,
            Civ.LITHUANIA.value: tLithuaniaOuter,
            Civ.AUSTRIA.value: tAustriaOuter,
            Civ.OTTOMAN.value: tTurkeyOuter,
            Civ.MOSCOW.value: tMoscowOuter,
            Civ.DUTCH.value: tDutchOuter,
        }

        self.tPot2CoreProvinces = {
            Civ.BYZANTIUM.value: tByzantiumPot2Core,
            Civ.FRANCE.value: tFrancePot2Core,
            Civ.ARABIA.value: tArabiaPot2Core,
            Civ.BULGARIA.value: tBulgariaPot2Core,
            Civ.CORDOBA.value: tCordobaPot2Core,
            Civ.VENECIA.value: tVenicePot2Core,
            Civ.BURGUNDY.value: tBurgundyPot2Core,
            Civ.GERMANY.value: tGermanyPot2Core,
            Civ.NOVGOROD.value: tNovgorodPot2Core,
            Civ.NORWAY.value: tNorwayPot2Core,
            Civ.KIEV.value: tKievPot2Core,
            Civ.HUNGARY.value: tHungaryPot2Core,
            Civ.CASTILLE.value: tSpainPot2Core,
            Civ.DENMARK.value: tDenmarkPot2Core,
            Civ.SCOTLAND.value: tScotlandPot2Core,
            Civ.POLAND.value: tPolandPot2Core,
            Civ.GENOA.value: tGenoaPot2Core,
            Civ.MOROCCO.value: tMoroccoPot2Core,
            Civ.ENGLAND.value: tEnglandPot2Core,
            Civ.PORTUGAL.value: tPortugalPot2Core,
            Civ.ARAGON.value: tAragonPot2Core,
            Civ.SWEDEN.value: tSwedenPot2Core,
            Civ.PRUSSIA.value: tPrussiaPot2Core,
            Civ.LITHUANIA.value: tLithuaniaPot2Core,
            Civ.AUSTRIA.value: tAustriaPot2Core,
            Civ.OTTOMAN.value: tTurkeyPot2Core,
            Civ.MOSCOW.value: tMoscowPot2Core,
            Civ.DUTCH.value: tDutchPot2Core,
        }

        self.tPot2NormProvinces = {
            Civ.BYZANTIUM.value: tByzantiumPot2Norm,
            Civ.FRANCE.value: tFrancePot2Norm,
            Civ.ARABIA.value: tArabiaPot2Norm,
            Civ.BULGARIA.value: tBulgariaPot2Norm,
            Civ.CORDOBA.value: tCordobaPot2Norm,
            Civ.VENECIA.value: tVenicePot2Norm,
            Civ.BURGUNDY.value: tBurgundyPot2Norm,
            Civ.GERMANY.value: tGermanyPot2Norm,
            Civ.NOVGOROD.value: tNovgorodPot2Norm,
            Civ.NORWAY.value: tNorwayPot2Norm,
            Civ.KIEV.value: tKievPot2Norm,
            Civ.HUNGARY.value: tHungaryPot2Norm,
            Civ.CASTILLE.value: tSpainPot2Norm,
            Civ.DENMARK.value: tDenmarkPot2Norm,
            Civ.SCOTLAND.value: tScotlandPot2Norm,
            Civ.POLAND.value: tPolandPot2Norm,
            Civ.GENOA.value: tGenoaPot2Norm,
            Civ.MOROCCO.value: tMoroccoPot2Norm,
            Civ.ENGLAND.value: tEnglandPot2Norm,
            Civ.PORTUGAL.value: tPortugalPot2Norm,
            Civ.ARAGON.value: tAragonPot2Norm,
            Civ.SWEDEN.value: tSwedenPot2Norm,
            Civ.PRUSSIA.value: tPrussiaPot2Norm,
            Civ.LITHUANIA.value: tLithuaniaPot2Norm,
            Civ.AUSTRIA.value: tAustriaPot2Norm,
            Civ.OTTOMAN.value: tTurkeyPot2Norm,
            Civ.MOSCOW.value: tMoscowPot2Norm,
            Civ.DUTCH.value: tDutchPot2Norm,
        }

    def setup(self):
        # set the initial situation for all players
        for civ in CIVILIZATIONS.main():
            for iProv in self.tCoreProvinces[civ.id]:
                civ.player.setProvinceType(iProv, ProvinceTypes.CORE.value)
            for iProv in self.tNormProvinces[civ.id]:
                civ.player.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
            for iProv in self.tOuterProvinces[civ.id]:
                civ.player.setProvinceType(iProv, ProvinceTypes.OUTER.value)
            for iProv in self.tPot2CoreProvinces[civ.id]:
                civ.player.setProvinceType(iProv, ProvinceTypes.POTENTIAL.value)
            for iProv in self.tPot2NormProvinces[civ.id]:
                civ.player.setProvinceType(iProv, ProvinceTypes.POTENTIAL.value)
        # update provinces for the 1200 AD Scenario
        if utils.getScenario() == Scenario.i1200AD:
            for civ in CIVILIZATIONS.main():
                if CIV_BIRTHDATE[civ.id] < DateTurn.i1200AD:
                    self.onSpawn(civ.id)

    def checkTurn(self, iGameTurn):
        # Norse provinces switch back to unstable after the fall of the Norman Kingdom of Sicily
        if iGameTurn == DateTurn.i1194AD + 1:
            pNorway.setProvinceType(xml.iP_Apulia, ProvinceTypes.NONE.value)
            pNorway.setProvinceType(xml.iP_Calabria, ProvinceTypes.NONE.value)
            pNorway.setProvinceType(xml.iP_Sicily, ProvinceTypes.NONE.value)
            pNorway.setProvinceType(xml.iP_Malta, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_Apulia, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_Calabria, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_Sicily, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_Malta, ProvinceTypes.NONE.value)
        # Prussia direction change
        elif iGameTurn == DateTurn.i1618AD:
            pPrussia.setProvinceType(xml.iP_Estonia, ProvinceTypes.NONE.value)
            pPrussia.setProvinceType(xml.iP_Lithuania, ProvinceTypes.NONE.value)
            pPrussia.setProvinceType(xml.iP_Suvalkija, ProvinceTypes.NONE.value)
            pPrussia.setProvinceType(xml.iP_Livonia, ProvinceTypes.OUTER.value)
            pPrussia.setProvinceType(xml.iP_Pomerania, ProvinceTypes.NATURAL.value)
            pPrussia.setProvinceType(xml.iP_Brandenburg, ProvinceTypes.NATURAL.value)
            pPrussia.setProvinceType(xml.iP_Silesia, ProvinceTypes.POTENTIAL.value)
            pPrussia.setProvinceType(xml.iP_GreaterPoland, ProvinceTypes.OUTER.value)
            print("Yes! Prussia can into Germany!")

    def onCityBuilt(self, iPlayer, x, y):
        if iPlayer >= CIVILIZATIONS.main().len():
            return
        pPlayer = gc.getPlayer(iPlayer)
        iProv = RFCEMaps.tProvinceMap[y][x]
        if pPlayer.getProvinceType(iProv) == ProvinceTypes.POTENTIAL.value:
            if iProv in self.tPot2NormProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
                utils.refreshStabilityOverlay()  # refresh the stability overlay
            elif iProv in self.tPot2CoreProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, ProvinceTypes.CORE.value)
                utils.refreshStabilityOverlay()  # refresh the stability overlay
            # Absinthe: bug if we tie potential only to the preset status of provinces
            else:  # also update if it was changed to be a potential province later in the game
                pPlayer.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
                utils.refreshStabilityOverlay()  # refresh the stability overlay

    def onCityAcquired(self, owner, iPlayer, city, bConquest, bTrade):
        if iPlayer >= CIVILIZATIONS.main().len():
            return
        pPlayer = gc.getPlayer(iPlayer)
        iProv = city.getProvince()
        if pPlayer.getProvinceType(iProv) == ProvinceTypes.POTENTIAL.value:
            if iProv in self.tPot2NormProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
                utils.refreshStabilityOverlay()  # refresh the stability overlay
            elif iProv in self.tPot2CoreProvinces[iPlayer]:
                pPlayer.setProvinceType(iProv, ProvinceTypes.CORE.value)
                utils.refreshStabilityOverlay()  # refresh the stability overlay
            # Absinthe: bug if we tie potential only to the preset status of provinces
            else:  # also update if it was changed to be a potential province later in the game
                pPlayer.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
                utils.refreshStabilityOverlay()  # refresh the stability overlay

    def onCityRazed(self, iOwner, iPlayer, city):
        pass

    def updatePotential(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        for city in utils.getCityList(iPlayer):
            iProv = city.getProvince()
            if pPlayer.getProvinceType(iProv) == ProvinceTypes.POTENTIAL.value:
                if iProv in self.tPot2NormProvinces[iPlayer]:
                    pPlayer.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
                elif iProv in self.tPot2CoreProvinces[iPlayer]:
                    pPlayer.setProvinceType(iProv, ProvinceTypes.CORE.value)
                # Absinthe: bug if we tie potential only to the preset status of provinces
                else:  # also update if it was changed to be a potential province later in the game
                    pPlayer.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
        utils.refreshStabilityOverlay()  # refresh the stability overlay

    def onRespawn(self, iPlayer):
        # Absinthe: reset the original potential provinces, but only if they wasn't changed to something entirely different later on
        pPlayer = gc.getPlayer(iPlayer)
        for iProv in self.tPot2CoreProvinces[iPlayer]:
            if pPlayer.getProvinceType(iProv) == ProvinceTypes.CORE.value:
                pPlayer.setProvinceType(iProv, ProvinceTypes.POTENTIAL.value)
        for iProv in self.tPot2NormProvinces[iPlayer]:
            if pPlayer.getProvinceType(iProv) == ProvinceTypes.NATURAL.value:
                pPlayer.setProvinceType(iProv, ProvinceTypes.POTENTIAL.value)

        # Absinthe: special respawn conditions
        # if ( iPlayer == iArabia ):
        # 	self.resetProvinces(iPlayer)
        if iPlayer == Civ.CORDOBA.value:
            for iProv in range(xml.iP_MaxNumberOfProvinces):
                pCordoba.setProvinceType(iProv, ProvinceTypes.NONE.value)
            pCordoba.setProvinceType(xml.iP_Ifriqiya, ProvinceTypes.CORE.value)
            pCordoba.setProvinceType(xml.iP_Algiers, ProvinceTypes.NATURAL.value)
            pCordoba.setProvinceType(xml.iP_Oran, ProvinceTypes.OUTER.value)
            pCordoba.setProvinceType(xml.iP_Tripolitania, ProvinceTypes.OUTER.value)
            pCordoba.setProvinceType(xml.iP_Tetouan, ProvinceTypes.OUTER.value)
            pCordoba.setProvinceType(xml.iP_Morocco, ProvinceTypes.OUTER.value)
            pCordoba.setProvinceType(xml.iP_Fez, ProvinceTypes.OUTER.value)

    def resetProvinces(self, iPlayer):
        # Absinthe: keep in mind that this will reset all to the initial status, so won't take later province changes into account
        pPlayer = gc.getPlayer(iPlayer)
        for iProv in range(xml.iP_MaxNumberOfProvinces):
            pPlayer.setProvinceType(iProv, ProvinceTypes.NONE.value)
        for iProv in self.tCoreProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, ProvinceTypes.CORE.value)
        for iProv in self.tNormProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
        for iProv in self.tOuterProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, ProvinceTypes.OUTER.value)
        for iProv in self.tPot2CoreProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, ProvinceTypes.POTENTIAL.value)
        for iProv in self.tPot2NormProvinces[iPlayer]:
            pPlayer.setProvinceType(iProv, ProvinceTypes.POTENTIAL.value)

    def onSpawn(self, iPlayer):
        # when a new nations spawns, old nations in the region should lose some of their provinces
        if iPlayer == Civ.ARABIA.value:
            pByzantium.setProvinceType(xml.iP_Cyrenaica, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Tripolitania, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Ifriqiya, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Egypt, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Arabia, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Syria, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Lebanon, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Jerusalem, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Antiochia, ProvinceTypes.NATURAL.value)
            pByzantium.setProvinceType(xml.iP_Cilicia, ProvinceTypes.NATURAL.value)
            pByzantium.setProvinceType(xml.iP_Charsianon, ProvinceTypes.NATURAL.value)
            pByzantium.setProvinceType(xml.iP_Colonea, ProvinceTypes.NATURAL.value)
        elif iPlayer == Civ.BULGARIA.value:
            pByzantium.setProvinceType(xml.iP_Serbia, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Moesia, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Thrace, ProvinceTypes.NATURAL.value)
        elif iPlayer == Civ.VENECIA.value:
            pByzantium.setProvinceType(xml.iP_Dalmatia, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Bosnia, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Slavonia, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Verona, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Tuscany, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Lombardy, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Liguria, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Corsica, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Sardinia, ProvinceTypes.NONE.value)
            pByzantium.setProvinceType(xml.iP_Latium, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.BURGUNDY.value:
            # these areas flip to Burgundy, so resetting them to Potential won't cause any issues
            pFrankia.setProvinceType(xml.iP_Provence, ProvinceTypes.POTENTIAL.value)
            pFrankia.setProvinceType(xml.iP_Burgundy, ProvinceTypes.POTENTIAL.value)
        elif iPlayer == Civ.GERMANY.value:
            pFrankia.setProvinceType(xml.iP_Lorraine, ProvinceTypes.OUTER.value)
            pFrankia.setProvinceType(xml.iP_Bavaria, ProvinceTypes.NONE.value)
            pFrankia.setProvinceType(xml.iP_Franconia, ProvinceTypes.NONE.value)
            pFrankia.setProvinceType(xml.iP_Saxony, ProvinceTypes.NONE.value)
            pFrankia.setProvinceType(xml.iP_Netherlands, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.HUNGARY.value:
            pBulgaria.setProvinceType(xml.iP_Banat, ProvinceTypes.NONE.value)
            pBulgaria.setProvinceType(xml.iP_Wallachia, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.CASTILLE.value:
            pCordoba.setProvinceType(xml.iP_LaMancha, ProvinceTypes.NATURAL.value)
        elif iPlayer == Civ.MOROCCO.value:
            pCordoba.setProvinceType(xml.iP_Morocco, ProvinceTypes.NONE.value)
            pCordoba.setProvinceType(xml.iP_Marrakesh, ProvinceTypes.NONE.value)
            pCordoba.setProvinceType(xml.iP_Fez, ProvinceTypes.OUTER.value)
            pCordoba.setProvinceType(xml.iP_Tetouan, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.ENGLAND.value:
            pFrankia.setProvinceType(
                xml.iP_Normandy, ProvinceTypes.POTENTIAL.value
            )  # it flips to England, so resetting them to Potential won't cause any issues
            pScotland.setProvinceType(xml.iP_Northumbria, ProvinceTypes.OUTER.value)
            pScotland.setProvinceType(xml.iP_Mercia, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_Northumbria, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_Mercia, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_EastAnglia, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_London, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.ARAGON.value:
            pByzantium.setProvinceType(xml.iP_Apulia, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Calabria, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Sicily, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Malta, ProvinceTypes.OUTER.value)
            pCordoba.setProvinceType(xml.iP_Aragon, ProvinceTypes.OUTER.value)
            pCordoba.setProvinceType(xml.iP_Catalonia, ProvinceTypes.OUTER.value)
            pCordoba.setProvinceType(xml.iP_Valencia, ProvinceTypes.NATURAL.value)
            pCordoba.setProvinceType(xml.iP_Balears, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.SWEDEN.value:
            pNorway.setProvinceType(xml.iP_Svealand, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_Gotaland, ProvinceTypes.NONE.value)
            pDenmark.setProvinceType(xml.iP_Svealand, ProvinceTypes.NONE.value)
            pNovgorod.setProvinceType(xml.iP_Osterland, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.AUSTRIA.value:
            pHungary.setProvinceType(xml.iP_Carinthia, ProvinceTypes.OUTER.value)
            pHungary.setProvinceType(xml.iP_Austria, ProvinceTypes.OUTER.value)
            pHungary.setProvinceType(xml.iP_Moravia, ProvinceTypes.OUTER.value)
            pHungary.setProvinceType(xml.iP_Bavaria, ProvinceTypes.NONE.value)
            pGermany.setProvinceType(xml.iP_Bavaria, ProvinceTypes.OUTER.value)
            pGermany.setProvinceType(xml.iP_Bohemia, ProvinceTypes.OUTER.value)
            pSpain.setProvinceType(xml.iP_Netherlands, ProvinceTypes.OUTER.value)
            pSpain.setProvinceType(xml.iP_Flanders, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.OTTOMAN.value:
            pByzantium.setProvinceType(xml.iP_Antiochia, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Cilicia, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Charsianon, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Colonea, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Armeniakon, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Cyprus, ProvinceTypes.OUTER.value)
            pByzantium.setProvinceType(xml.iP_Anatolikon, ProvinceTypes.NATURAL.value)
            pByzantium.setProvinceType(xml.iP_Opsikion, ProvinceTypes.NATURAL.value)
            pByzantium.setProvinceType(xml.iP_Thrakesion, ProvinceTypes.NATURAL.value)
            pByzantium.setProvinceType(xml.iP_Paphlagonia, ProvinceTypes.NATURAL.value)
            pHungary.setProvinceType(xml.iP_Dalmatia, ProvinceTypes.OUTER.value)
            pHungary.setProvinceType(xml.iP_Bosnia, ProvinceTypes.OUTER.value)
            pHungary.setProvinceType(xml.iP_Banat, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.MOSCOW.value:
            pNovgorod.setProvinceType(xml.iP_Rostov, ProvinceTypes.OUTER.value)
            pNovgorod.setProvinceType(xml.iP_Smolensk, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.DUTCH.value:
            pSpain.setProvinceType(xml.iP_Netherlands, ProvinceTypes.NONE.value)
            pSpain.setProvinceType(xml.iP_Flanders, ProvinceTypes.NONE.value)
            pAustria.setProvinceType(xml.iP_Netherlands, ProvinceTypes.NONE.value)
            pAustria.setProvinceType(xml.iP_Flanders, ProvinceTypes.NONE.value)

        utils.refreshStabilityOverlay()  # refresh the stability overlay
