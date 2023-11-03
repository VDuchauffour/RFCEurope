# RFC Europe - Province manager

from CvPythonExtensions import *
from CoreData import civilizations
from CoreStructures import player
import RFCEMaps
import RFCUtils  # Absinthe
import PyHelpers  # Absinthe

from TimelineData import DateTurn
from CoreTypes import Civ, Province, Scenario, ProvinceTypes

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer  # Absinthe
utils = RFCUtils.RFCUtils()  # Absinthe


############ Lists of all the provinces for each Civ ###################
tByzantiumCore = [
    Province.CONSTANTINOPLE.value,
    Province.THRACE.value,
    Province.THESSALY.value,
    Province.THESSALONIKI.value,
    Province.EPIRUS.value,
    Province.MOREA.value,
    Province.OPSIKION.value,
    Province.PAPHLAGONIA.value,
    Province.THRAKESION.value,
    Province.CILICIA.value,
    Province.ANATOLIKON.value,
    Province.ARMENIAKON.value,
    Province.CHARSIANON.value,
    Province.COLONEA.value,
    Province.ANTIOCHIA.value,
]
tByzantiumNorm = [
    Province.MOESIA.value,
    Province.SERBIA.value,
    Province.MACEDONIA.value,
    Province.ARBERIA.value,
    Province.CYPRUS.value,
    Province.CRETE.value,
    Province.RHODES.value,
    Province.SYRIA.value,
    Province.LEBANON.value,
    Province.JERUSALEM.value,
    Province.EGYPT.value,
    Province.CYRENAICA.value,
]
tByzantiumOuter = [
    Province.CRIMEA.value,
    Province.ARABIA.value,
    Province.BOSNIA.value,
    Province.SLAVONIA.value,
    Province.DALMATIA.value,
    Province.VERONA.value,
    Province.LOMBARDY.value,
    Province.LIGURIA.value,
    Province.TUSCANY.value,
    Province.LATIUM.value,
    Province.SARDINIA.value,
    Province.CORSICA.value,
]
tByzantiumPot2Core = []
tByzantiumPot2Norm = [
    Province.CALABRIA.value,
    Province.APULIA.value,
    Province.SICILY.value,
    Province.MALTA.value,
    Province.TRIPOLITANIA.value,
    Province.IFRIQIYA.value,
]

tFranceCore = [Province.ILE_DE_FRANCE.value, Province.ORLEANS.value, Province.CHAMPAGNE.value]
tFranceNorm = [
    Province.PICARDY.value,
    Province.NORMANDY.value,
    Province.AQUITAINE.value,
    Province.LORRAINE.value,
]
tFranceOuter = [
    Province.CATALONIA.value,
    Province.ARAGON.value,
    Province.NAVARRE.value,
    Province.NETHERLANDS.value,
    Province.BAVARIA.value,
    Province.SAXONY.value,
    Province.SWABIA.value,
    Province.FRANCONIA.value,
    Province.LOMBARDY.value,
    Province.LIGURIA.value,
    Province.CORSICA.value,
]
tFrancePot2Core = []
tFrancePot2Norm = [
    Province.BRETAGNE.value,
    Province.PROVENCE.value,
    Province.BURGUNDY.value,
    Province.FLANDERS.value,
]

tArabiaCore = [
    Province.SYRIA.value,
    Province.LEBANON.value,
    Province.JERUSALEM.value,
    Province.ARABIA.value,
]
tArabiaNorm = [Province.EGYPT.value, Province.CYRENAICA.value]
tArabiaOuter = [
    Province.ORAN.value,
    Province.ALGIERS.value,
    Province.SICILY.value,
    Province.MALTA.value,
    Province.CRETE.value,
    Province.RHODES.value,
    Province.CILICIA.value,
]
tArabiaPot2Core = []
tArabiaPot2Norm = [
    Province.ANTIOCHIA.value,
    Province.CYPRUS.value,
    Province.IFRIQIYA.value,
    Province.TRIPOLITANIA.value,
]

tBulgariaCore = [Province.MOESIA.value]
tBulgariaNorm = [Province.MACEDONIA.value, Province.WALLACHIA.value]
tBulgariaOuter = [
    Province.SERBIA.value,
    Province.BANAT.value,
    Province.EPIRUS.value,
    Province.ARBERIA.value,
    Province.CONSTANTINOPLE.value,
]
tBulgariaPot2Core = []
tBulgariaPot2Norm = [Province.THRACE.value, Province.THESSALONIKI.value]

tCordobaCore = [Province.ANDALUSIA.value, Province.VALENCIA.value, Province.LA_MANCHA.value]
tCordobaNorm = [Province.TETOUAN.value]
tCordobaOuter = [
    Province.LEON.value,
    Province.LUSITANIA.value,
    Province.NAVARRE.value,
    Province.CASTILE.value,
    Province.ORAN.value,
]
tCordobaPot2Core = []
tCordobaPot2Norm = [
    Province.MOROCCO.value,
    Province.FEZ.value,
    Province.MARRAKESH.value,
    Province.CATALONIA.value,
    Province.ARAGON.value,
    Province.BALEARS.value,
]

tVeniceCore = [Province.VERONA.value]
tVeniceNorm = [Province.DALMATIA.value]
tVeniceOuter = [
    Province.EPIRUS.value,
    Province.MOREA.value,
    Province.RHODES.value,
    Province.CONSTANTINOPLE.value,
]
tVenicePot2Core = []
tVenicePot2Norm = [
    Province.TUSCANY.value,
    Province.ARBERIA.value,
    Province.CRETE.value,
    Province.CYPRUS.value,
]

tBurgundyCore = [Province.BURGUNDY.value]
tBurgundyNorm = [Province.PROVENCE.value, Province.FLANDERS.value]
tBurgundyOuter = [
    Province.LORRAINE.value,
    Province.SWABIA.value,
    Province.LOMBARDY.value,
    Province.LIGURIA.value,
    Province.BRETAGNE.value,
]
tBurgundyPot2Core = []
tBurgundyPot2Norm = [
    Province.CHAMPAGNE.value,
    Province.PICARDY.value,
    Province.ILE_DE_FRANCE.value,
    Province.AQUITAINE.value,
    Province.ORLEANS.value,
    Province.NORMANDY.value,
]

tGermanyCore = [
    Province.FRANCONIA.value,
    Province.LORRAINE.value,
    Province.BAVARIA.value,
    Province.SWABIA.value,
    Province.SAXONY.value,
]
tGermanyNorm = [Province.BRANDENBURG.value]
tGermanyOuter = [
    Province.CHAMPAGNE.value,
    Province.PICARDY.value,
    Province.BURGUNDY.value,
    Province.LIGURIA.value,
    Province.VERONA.value,
    Province.TUSCANY.value,
    Province.AUSTRIA.value,
    Province.MORAVIA.value,
    Province.SILESIA.value,
    Province.GREATER_POLAND.value,
    Province.CARINTHIA.value,
]
tGermanyPot2Core = []
tGermanyPot2Norm = [
    Province.BOHEMIA.value,
    Province.HOLSTEIN.value,
    Province.POMERANIA.value,
    Province.NETHERLANDS.value,
    Province.FLANDERS.value,
    Province.LOMBARDY.value,
]

tNovgorodCore = [Province.NOVGOROD.value, Province.KARELIA.value]
tNovgorodNorm = [Province.ROSTOV.value, Province.VOLOGDA.value]
tNovgorodOuter = [Province.SMOLENSK.value, Province.POLOTSK.value, Province.LIVONIA.value]
tNovgorodPot2Core = []
tNovgorodPot2Norm = [Province.ESTONIA.value, Province.OSTERLAND.value]

tNorwayCore = [Province.NORWAY.value, Province.VESTFOLD.value]
tNorwayNorm = [Province.ICELAND.value]
tNorwayOuter = [
    Province.SCOTLAND.value,
    Province.NORTHUMBRIA.value,
    Province.IRELAND.value,
    Province.NORMANDY.value,
    Province.SVEALAND.value,
    Province.NORRLAND.value,
    Province.SICILY.value,
    Province.APULIA.value,
    Province.CALABRIA.value,
    Province.MALTA.value,
]
tNorwayPot2Core = []
tNorwayPot2Norm = [Province.THE_ISLES.value, Province.JAMTLAND.value]

tKievCore = [
    Province.KIEV.value,
    Province.SLOBODA.value,
    Province.PEREYASLAVL.value,
    Province.CHERNIGOV.value,
]
tKievNorm = [Province.PODOLIA.value, Province.VOLHYNIA.value]
tKievOuter = [
    Province.MOLDOVA.value,
    Province.GALICJA.value,
    Province.BREST.value,
    Province.POLOTSK.value,
    Province.NOVGOROD.value,
    Province.MOSCOW.value,
    Province.MUROM.value,
    Province.SIMBIRSK.value,
    Province.CRIMEA.value,
    Province.DONETS.value,
    Province.KUBAN.value,
]
tKievPot2Core = []
tKievPot2Norm = [Province.MINSK.value, Province.SMOLENSK.value, Province.ZAPORIZHIA.value]

tHungaryCore = [
    Province.HUNGARY.value,
    Province.UPPER_HUNGARY.value,
    Province.PANNONIA.value,
    Province.TRANSYLVANIA.value,
]
tHungaryNorm = [
    Province.SLAVONIA.value,
    Province.BANAT.value,
    Province.BOSNIA.value,
    Province.DALMATIA.value,
]
tHungaryOuter = [
    Province.SERBIA.value,
    Province.WALLACHIA.value,
    Province.MOLDOVA.value,
    Province.GALICJA.value,
    Province.BAVARIA.value,
    Province.BOHEMIA.value,
    Province.SILESIA.value,
]
tHungaryPot2Core = []
tHungaryPot2Norm = [Province.MORAVIA.value, Province.AUSTRIA.value, Province.CARINTHIA.value]

tSpainCore = [Province.LEON.value, Province.GALICIA.value, Province.CASTILE.value]
tSpainNorm = []
tSpainOuter = [
    Province.LUSITANIA.value,
    Province.CATALONIA.value,
    Province.ARAGON.value,
    Province.BALEARS.value,
    Province.AQUITAINE.value,
    Province.PROVENCE.value,
    Province.TETOUAN.value,
    Province.FEZ.value,
    Province.ORAN.value,
    Province.ALGIERS.value,
    Province.SARDINIA.value,
    Province.CORSICA.value,
    Province.AZORES.value,
    Province.SICILY.value,
    Province.CALABRIA.value,
    Province.APULIA.value,
]
tSpainPot2Core = []
tSpainPot2Norm = [
    Province.NAVARRE.value,
    Province.ANDALUSIA.value,
    Province.VALENCIA.value,
    Province.LA_MANCHA.value,
    Province.CANARIES.value,
    Province.MADEIRA.value,
]

tDenmarkCore = [Province.DENMARK.value, Province.SKANELAND.value]
tDenmarkNorm = []
tDenmarkOuter = [
    Province.GOTALAND.value,
    Province.SVEALAND.value,
    Province.NORTHUMBRIA.value,
    Province.MERCIA.value,
    Province.EAST_ANGLIA.value,
    Province.LONDON.value,
    Province.BRANDENBURG.value,
    Province.NORWAY.value,
    Province.VESTFOLD.value,
    Province.NORMANDY.value,
    Province.SICILY.value,
    Province.APULIA.value,
    Province.CALABRIA.value,
    Province.MALTA.value,
]
tDenmarkPot2Core = []
tDenmarkPot2Norm = [Province.ESTONIA.value, Province.GOTLAND.value, Province.HOLSTEIN.value]

tScotlandCore = [Province.SCOTLAND.value]
tScotlandNorm = [Province.THE_ISLES.value]
tScotlandOuter = [Province.IRELAND.value, Province.MERCIA.value, Province.WALES.value]
tScotlandPot2Core = []
tScotlandPot2Norm = [Province.NORTHUMBRIA.value]

tPolandCore = [Province.GREATER_POLAND.value, Province.LESSER_POLAND.value, Province.MASOVIA.value]
tPolandNorm = [Province.BREST.value, Province.GALICJA.value]
tPolandOuter = [
    Province.PRUSSIA.value,
    Province.LITHUANIA.value,
    Province.POLOTSK.value,
    Province.MINSK.value,
    Province.VOLHYNIA.value,
    Province.PODOLIA.value,
    Province.MOLDOVA.value,
    Province.KIEV.value,
]
tPolandPot2Core = []
tPolandPot2Norm = [Province.POMERANIA.value, Province.SILESIA.value, Province.SUVALKIJA.value]

tGenoaCore = [Province.LIGURIA.value]
tGenoaNorm = [Province.CORSICA.value, Province.SARDINIA.value]
tGenoaOuter = [
    Province.CONSTANTINOPLE.value,
    Province.CRETE.value,
    Province.CYPRUS.value,
    Province.MOREA.value,
    Province.ARMENIAKON.value,
    Province.PAPHLAGONIA.value,
    Province.THRAKESION.value,
]
tGenoaPot2Core = []
tGenoaPot2Norm = [
    Province.SICILY.value,
    Province.MALTA.value,
    Province.LOMBARDY.value,
    Province.TUSCANY.value,
    Province.RHODES.value,
    Province.CRIMEA.value,
]

tMoroccoCore = [Province.MARRAKESH.value, Province.MOROCCO.value, Province.FEZ.value]
tMoroccoNorm = [Province.TETOUAN.value]
tMoroccoOuter = [
    Province.IFRIQIYA.value,
    Province.ANDALUSIA.value,
    Province.VALENCIA.value,
    Province.TRIPOLITANIA.value,
    Province.SAHARA.value,
]
tMoroccoPot2Core = []
tMoroccoPot2Norm = [Province.ORAN.value, Province.ALGIERS.value]

tEnglandCore = [
    Province.LONDON.value,
    Province.EAST_ANGLIA.value,
    Province.MERCIA.value,
    Province.WESSEX.value,
]
tEnglandNorm = [Province.NORTHUMBRIA.value]
tEnglandOuter = [
    Province.ILE_DE_FRANCE.value,
    Province.BRETAGNE.value,
    Province.AQUITAINE.value,
    Province.ORLEANS.value,
    Province.CHAMPAGNE.value,
    Province.FLANDERS.value,
    Province.NORMANDY.value,
    Province.PICARDY.value,
    Province.SCOTLAND.value,
    Province.THE_ISLES.value,
    Province.IRELAND.value,
]
tEnglandPot2Core = []
tEnglandPot2Norm = [Province.WALES.value]

tPortugalCore = [Province.LUSITANIA.value]
tPortugalNorm = [Province.AZORES.value]
tPortugalOuter = [
    Province.MOROCCO.value,
    Province.TETOUAN.value,
    Province.LEON.value,
    Province.GALICIA.value,
]
tPortugalPot2Core = []
tPortugalPot2Norm = [Province.MADEIRA.value, Province.CANARIES.value, Province.ANDALUSIA.value]

tAragonCore = [
    Province.ARAGON.value,
    Province.CATALONIA.value,
    Province.BALEARS.value,
    Province.VALENCIA.value,
]
tAragonNorm = []
tAragonOuter = [
    Province.CASTILE.value,
    Province.PROVENCE.value,
    Province.CORSICA.value,
    Province.THESSALY.value,
]
tAragonPot2Core = []
tAragonPot2Norm = [
    Province.NAVARRE.value,
    Province.ANDALUSIA.value,
    Province.LA_MANCHA.value,
    Province.SARDINIA.value,
    Province.SICILY.value,
    Province.APULIA.value,
    Province.CALABRIA.value,
    Province.MALTA.value,
]

tSwedenCore = [Province.NORRLAND.value, Province.SVEALAND.value]
tSwedenNorm = [Province.GOTALAND.value, Province.GOTLAND.value]
tSwedenOuter = [
    Province.SKANELAND.value,
    Province.VESTFOLD.value,
    Province.POMERANIA.value,
    Province.LIVONIA.value,
    Province.PRUSSIA.value,
    Province.NOVGOROD.value,
]
tSwedenPot2Core = []
tSwedenPot2Norm = [
    Province.JAMTLAND.value,
    Province.OSTERLAND.value,
    Province.KARELIA.value,
    Province.ESTONIA.value,
]

tPrussiaCore = [Province.PRUSSIA.value]
tPrussiaNorm = []
tPrussiaOuter = [
    Province.BRANDENBURG.value,
    Province.ESTONIA.value,
    Province.GOTLAND.value,
    Province.LITHUANIA.value,
    Province.SUVALKIJA.value,
]
tPrussiaPot2Core = []
tPrussiaPot2Norm = [Province.POMERANIA.value, Province.LIVONIA.value]

tLithuaniaCore = [Province.LITHUANIA.value]
tLithuaniaNorm = [Province.SUVALKIJA.value, Province.MINSK.value, Province.POLOTSK.value]
tLithuaniaOuter = [
    Province.GREATER_POLAND.value,
    Province.LESSER_POLAND.value,
    Province.MASOVIA.value,
    Province.GALICJA.value,
    Province.SLOBODA.value,
    Province.PEREYASLAVL.value,
    Province.LIVONIA.value,
    Province.ESTONIA.value,
    Province.NOVGOROD.value,
    Province.SMOLENSK.value,
    Province.CHERNIGOV.value,
]
tLithuaniaPot2Core = []
tLithuaniaPot2Norm = [
    Province.BREST.value,
    Province.PODOLIA.value,
    Province.VOLHYNIA.value,
    Province.KIEV.value,
]

tAustriaCore = [Province.AUSTRIA.value, Province.CARINTHIA.value]
tAustriaNorm = [Province.BOHEMIA.value, Province.MORAVIA.value]
tAustriaOuter = [
    Province.VERONA.value,
    Province.HUNGARY.value,
    Province.TRANSYLVANIA.value,
    Province.SLAVONIA.value,
    Province.DALMATIA.value,
    Province.LESSER_POLAND.value,
    Province.GALICJA.value,
    Province.NETHERLANDS.value,
    Province.FLANDERS.value,
]
tAustriaPot2Core = []
tAustriaPot2Norm = [
    Province.BAVARIA.value,
    Province.SILESIA.value,
    Province.PANNONIA.value,
    Province.UPPER_HUNGARY.value,
]

tTurkeyCore = [
    Province.OPSIKION.value,
    Province.THRAKESION.value,
    Province.PAPHLAGONIA.value,
    Province.ANATOLIKON.value,
    Province.CONSTANTINOPLE.value,
]
tTurkeyNorm = [
    Province.THRACE.value,
    Province.ARMENIAKON.value,
    Province.CHARSIANON.value,
    Province.CILICIA.value,
]
tTurkeyOuter = [
    Province.THESSALY.value,
    Province.EPIRUS.value,
    Province.MOREA.value,
    Province.ARBERIA.value,
    Province.WALLACHIA.value,
    Province.SERBIA.value,
    Province.BOSNIA.value,
    Province.BANAT.value,
    Province.SLAVONIA.value,
    Province.PANNONIA.value,
    Province.HUNGARY.value,
    Province.TRANSYLVANIA.value,
    Province.MOLDOVA.value,
    Province.CRIMEA.value,
    Province.CRETE.value,
    Province.CYRENAICA.value,
    Province.TRIPOLITANIA.value,
    Province.KUBAN.value,
]
tTurkeyPot2Core = []
tTurkeyPot2Norm = [
    Province.COLONEA.value,
    Province.ANTIOCHIA.value,
    Province.SYRIA.value,
    Province.LEBANON.value,
    Province.JERUSALEM.value,
    Province.EGYPT.value,
    Province.ARABIA.value,
    Province.MACEDONIA.value,
    Province.THESSALONIKI.value,
    Province.MOESIA.value,
    Province.CYPRUS.value,
    Province.RHODES.value,
]

tMoscowCore = [
    Province.MOSCOW.value,
    Province.MUROM.value,
    Province.ROSTOV.value,
    Province.SMOLENSK.value,
]
tMoscowNorm = [
    Province.NIZHNYNOVGOROD.value,
    Province.SIMBIRSK.value,
    Province.PEREYASLAVL.value,
    Province.CHERNIGOV.value,
]
tMoscowOuter = [
    Province.CRIMEA.value,
    Province.MOLDOVA.value,
    Province.GALICJA.value,
    Province.KUBAN.value,
    Province.BREST.value,
    Province.LITHUANIA.value,
    Province.LIVONIA.value,
    Province.ESTONIA.value,
    Province.KARELIA.value,
    Province.OSTERLAND.value,
    Province.PRUSSIA.value,
    Province.SUVALKIJA.value,
]
tMoscowPot2Core = []
tMoscowPot2Norm = [
    Province.NOVGOROD.value,
    Province.VOLOGDA.value,
    Province.KIEV.value,
    Province.MINSK.value,
    Province.POLOTSK.value,
    Province.VOLHYNIA.value,
    Province.PODOLIA.value,
    Province.DONETS.value,
    Province.SLOBODA.value,
    Province.ZAPORIZHIA.value,
]

tDutchCore = [Province.NETHERLANDS.value]
tDutchNorm = [Province.FLANDERS.value]
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
            Civ.CASTILE.value: tSpainCore,
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
            Civ.CASTILE.value: tSpainNorm,
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
            Civ.CASTILE.value: tSpainOuter,
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
            Civ.CASTILE.value: tSpainPot2Core,
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
            Civ.CASTILE.value: tSpainPot2Norm,
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
        for civ in civilizations().main():
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
            for civ in civilizations().main():
                if civ.date.birth < DateTurn.i1200AD:
                    self.onSpawn(civ.id)

    def checkTurn(self, iGameTurn):
        # Norse provinces switch back to unstable after the fall of the Norman Kingdom of Sicily
        if iGameTurn == DateTurn.i1194AD + 1:
            player(Civ.NORWAY).setProvinceType(Province.APULIA.value, ProvinceTypes.NONE.value)
            player(Civ.NORWAY).setProvinceType(Province.CALABRIA.value, ProvinceTypes.NONE.value)
            player(Civ.NORWAY).setProvinceType(Province.SICILY.value, ProvinceTypes.NONE.value)
            player(Civ.NORWAY).setProvinceType(Province.MALTA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.APULIA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.CALABRIA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.SICILY.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.MALTA.value, ProvinceTypes.NONE.value)
        # Prussia direction change
        elif iGameTurn == DateTurn.i1618AD:
            player(Civ.PRUSSIA).setProvinceType(Province.ESTONIA.value, ProvinceTypes.NONE.value)
            player(Civ.PRUSSIA).setProvinceType(Province.LITHUANIA.value, ProvinceTypes.NONE.value)
            player(Civ.PRUSSIA).setProvinceType(Province.SUVALKIJA.value, ProvinceTypes.NONE.value)
            player(Civ.PRUSSIA).setProvinceType(Province.LIVONIA.value, ProvinceTypes.OUTER.value)
            player(Civ.PRUSSIA).setProvinceType(
                Province.POMERANIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.PRUSSIA).setProvinceType(
                Province.BRANDENBURG.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.PRUSSIA).setProvinceType(
                Province.SILESIA.value, ProvinceTypes.POTENTIAL.value
            )
            player(Civ.PRUSSIA).setProvinceType(
                Province.GREATER_POLAND.value, ProvinceTypes.OUTER.value
            )

    def onCityBuilt(self, iPlayer, x, y):
        if iPlayer >= civilizations().main().len():
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
        if iPlayer >= civilizations().main().len():
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
            for iProv in range(len(Province)):
                player(Civ.CORDOBA).setProvinceType(iProv, ProvinceTypes.NONE.value)
            player(Civ.CORDOBA).setProvinceType(Province.IFRIQIYA.value, ProvinceTypes.CORE.value)
            player(Civ.CORDOBA).setProvinceType(
                Province.ALGIERS.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.CORDOBA).setProvinceType(Province.ORAN.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(
                Province.TRIPOLITANIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.CORDOBA).setProvinceType(Province.TETOUAN.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(Province.MOROCCO.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(Province.FEZ.value, ProvinceTypes.OUTER.value)

    def resetProvinces(self, iPlayer):
        # Absinthe: keep in mind that this will reset all to the initial status, so won't take later province changes into account
        pPlayer = gc.getPlayer(iPlayer)
        for iProv in range(len(Province)):
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
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CYRENAICA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.TRIPOLITANIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.IFRIQIYA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.EGYPT.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.ARABIA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.SYRIA.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.LEBANON.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.JERUSALEM.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ANTIOCHIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CILICIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CHARSIANON.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.COLONEA.value, ProvinceTypes.NATURAL.value
            )
        elif iPlayer == Civ.BULGARIA.value:
            player(Civ.BYZANTIUM).setProvinceType(Province.SERBIA.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.MOESIA.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.THRACE.value, ProvinceTypes.NATURAL.value
            )
        elif iPlayer == Civ.VENECIA.value:
            player(Civ.BYZANTIUM).setProvinceType(
                Province.DALMATIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.BOSNIA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.SLAVONIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.VERONA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.TUSCANY.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.LOMBARDY.value, ProvinceTypes.NONE.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.LIGURIA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.CORSICA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.SARDINIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.LATIUM.value, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.BURGUNDY.value:
            # these areas flip to Burgundy, so resetting them to Potential won't cause any issues
            player(Civ.FRANCE).setProvinceType(
                Province.PROVENCE.value, ProvinceTypes.POTENTIAL.value
            )
            player(Civ.FRANCE).setProvinceType(
                Province.BURGUNDY.value, ProvinceTypes.POTENTIAL.value
            )
        elif iPlayer == Civ.GERMANY.value:
            player(Civ.FRANCE).setProvinceType(Province.LORRAINE.value, ProvinceTypes.OUTER.value)
            player(Civ.FRANCE).setProvinceType(Province.BAVARIA.value, ProvinceTypes.NONE.value)
            player(Civ.FRANCE).setProvinceType(Province.FRANCONIA.value, ProvinceTypes.NONE.value)
            player(Civ.FRANCE).setProvinceType(Province.SAXONY.value, ProvinceTypes.NONE.value)
            player(Civ.FRANCE).setProvinceType(
                Province.NETHERLANDS.value, ProvinceTypes.NONE.value
            )
        elif iPlayer == Civ.HUNGARY.value:
            player(Civ.BULGARIA).setProvinceType(Province.BANAT.value, ProvinceTypes.NONE.value)
            player(Civ.BULGARIA).setProvinceType(
                Province.WALLACHIA.value, ProvinceTypes.OUTER.value
            )
        elif iPlayer == Civ.CASTILE.value:
            player(Civ.CORDOBA).setProvinceType(
                Province.LA_MANCHA.value, ProvinceTypes.NATURAL.value
            )
        elif iPlayer == Civ.MOROCCO.value:
            player(Civ.CORDOBA).setProvinceType(Province.MOROCCO.value, ProvinceTypes.NONE.value)
            player(Civ.CORDOBA).setProvinceType(Province.MARRAKESH.value, ProvinceTypes.NONE.value)
            player(Civ.CORDOBA).setProvinceType(Province.FEZ.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(Province.TETOUAN.value, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.ENGLAND.value:
            player(Civ.FRANCE).setProvinceType(
                Province.NORMANDY.value, ProvinceTypes.POTENTIAL.value
            )  # it flips to England, so resetting them to Potential won't cause any issues
            player(Civ.SCOTLAND).setProvinceType(
                Province.NORTHUMBRIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.SCOTLAND).setProvinceType(Province.MERCIA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(
                Province.NORTHUMBRIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.DENMARK).setProvinceType(Province.MERCIA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(
                Province.EAST_ANGLIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.DENMARK).setProvinceType(Province.LONDON.value, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.ARAGON.value:
            player(Civ.BYZANTIUM).setProvinceType(Province.APULIA.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CALABRIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.SICILY.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.MALTA.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(Province.ARAGON.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(
                Province.CATALONIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.CORDOBA).setProvinceType(
                Province.VALENCIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.CORDOBA).setProvinceType(Province.BALEARS.value, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.SWEDEN.value:
            player(Civ.NORWAY).setProvinceType(Province.SVEALAND.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.GOTALAND.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.SVEALAND.value, ProvinceTypes.NONE.value)
            player(Civ.NOVGOROD).setProvinceType(
                Province.OSTERLAND.value, ProvinceTypes.OUTER.value
            )
        elif iPlayer == Civ.AUSTRIA.value:
            player(Civ.HUNGARY).setProvinceType(
                Province.CARINTHIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.HUNGARY).setProvinceType(Province.AUSTRIA.value, ProvinceTypes.OUTER.value)
            player(Civ.HUNGARY).setProvinceType(Province.MORAVIA.value, ProvinceTypes.OUTER.value)
            player(Civ.HUNGARY).setProvinceType(Province.BAVARIA.value, ProvinceTypes.NONE.value)
            player(Civ.GERMANY).setProvinceType(Province.BAVARIA.value, ProvinceTypes.OUTER.value)
            player(Civ.GERMANY).setProvinceType(Province.BOHEMIA.value, ProvinceTypes.OUTER.value)
            player(Civ.CASTILE).setProvinceType(
                Province.NETHERLANDS.value, ProvinceTypes.OUTER.value
            )
            player(Civ.CASTILE).setProvinceType(Province.FLANDERS.value, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.OTTOMAN.value:
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ANTIOCHIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CILICIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CHARSIANON.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.COLONEA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ARMENIAKON.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.CYPRUS.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ANATOLIKON.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.OPSIKION.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.THRAKESION.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.PAPHLAGONIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.HUNGARY).setProvinceType(Province.DALMATIA.value, ProvinceTypes.OUTER.value)
            player(Civ.HUNGARY).setProvinceType(Province.BOSNIA.value, ProvinceTypes.OUTER.value)
            player(Civ.HUNGARY).setProvinceType(Province.BANAT.value, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.MOSCOW.value:
            player(Civ.NOVGOROD).setProvinceType(Province.ROSTOV.value, ProvinceTypes.OUTER.value)
            player(Civ.NOVGOROD).setProvinceType(Province.SMOLENSK.value, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.DUTCH.value:
            player(Civ.CASTILE).setProvinceType(
                Province.NETHERLANDS.value, ProvinceTypes.NONE.value
            )
            player(Civ.CASTILE).setProvinceType(Province.FLANDERS.value, ProvinceTypes.NONE.value)
            player(Civ.AUSTRIA).setProvinceType(
                Province.NETHERLANDS.value, ProvinceTypes.NONE.value
            )
            player(Civ.AUSTRIA).setProvinceType(Province.FLANDERS.value, ProvinceTypes.NONE.value)

        utils.refreshStabilityOverlay()  # refresh the stability overlay
