# ruff: noqa

from CoreTypes import (
    AreaType,
    City,
    Civ,
    CivGroup,
    Colony,
    Company,
    Province,
    ProvinceEvent,
    ProvinceType,
    Region,
    Scenario,
    Lake,
    Area,
)
from BaseStructures import DataMapper, EnumDataMapper
from CoreStructures import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    CompanyDataMapper,
    ScenarioDataMapper,
    Tile,
    CivDataMapper,
    TilesFactory,
    concat_tiles,
    parse_area_dict,
)
from TimelineData import DateTurn

MINOR_CIVS = (
    Civ.INDEPENDENT,
    Civ.INDEPENDENT_2,
    Civ.INDEPENDENT_3,
    Civ.INDEPENDENT_4,
    Civ.BARBARIAN,
)

CITIES = EnumDataMapper(
    {
        City.CONSTANTINOPLE: [(81, 24)],
        City.PARIS: [(44, 46)],
        City.DAMASCUS: [(97, 10)],
        City.PRESLAV: [(78, 29)],
        City.CORDOBA: [(30, 23)],
        City.VENICE: [(56, 35)],
        City.DIJON: [(47, 41)],
        City.FRANKFURT: [(53, 46)],
        City.NOVGOROD: [(80, 62)],
        City.TONSBERG: [(57, 65)],
        City.KIEV: [(83, 45)],
        City.BUDA: [(66, 37)],
        City.LEON: [(27, 32)],
        City.ROSKILDE: [(59, 57)],
        City.EDINBURGH: [(37, 63)],
        City.POZNAN: [(65, 49)],
        City.GENOA: [(50, 34)],
        City.MARRAKESH: [(24, 7)],
        City.LONDON: [(41, 52)],
        City.LISBOA: [(21, 25)],
        City.ZARAGOZA: [(36, 29)],
        City.STOCKHOLM: [(66, 64)],
        City.KONIGSBERG: [(69, 53)],
        City.VILNUS: [(75, 53)],
        City.WIEN: [(62, 40)],
        City.GALLIPOLI: [(78, 22)],
        City.MOSCOW: [(91, 56)],
        City.AMSTERDAM: [(49, 52)],
        City.ROME: [(56, 27)],
        City.JERUSALEM: [(93, 5)],
        City.TANGIER: [(27, 16)],
        City.BORDEAUX: [(37, 38)],
        City.ALGER: [(40, 16)],
        City.TLEMCEN: [(34, 13)],
        City.BARCELONA: [(40, 28)],
        City.TOULOUSE: [(41, 34), (40, 34)],
        City.NARBONA: [(42, 32)],
        City.MARSEILLES: [(46, 32)],
        City.AIS_DE_PROVENCA: [(46, 33)],
        City.NANTES: [(36, 43)],
        City.VANNES: [(35, 43)],
        City.RENNES: [(37, 44)],
        City.CAEN: [(40, 47)],
        City.LYON: [(46, 37)],
        City.TUNIS: [(49, 17)],
        City.YORK: [(39, 59)],
        City.MILAN: [(52, 37)],
        City.FLORENCE: [(54, 32)],
        City.PISA: [(53, 32)],
        City.ANCONA: [(57, 31)],
        City.TRIPOLI: [(54, 8)],
        City.AUGSBURG: [(55, 41)],
        City.NAPOLI: [(59, 24)],
        City.BENEVENTO: [(60, 25)],
        City.TARANTO: [(62, 24)],
        City.RAGUSA: [(64, 28)],
        City.SEVILLE: [(27, 21)],
        City.PALERMO: [(55, 19)],
        City.SYRACUSE: [(58, 17)],
        City.INVERNESS: [(37, 67), (37, 65)],
        City.RHODES: [(80, 13)],
        City.NORWICH: [(43, 55)],
        City.KAIROUAN: [(48, 14)],
        City.TOLEDO: [(30, 27)],
        City.LEICESTER: [(39, 56)],
        City.VALENCIA: [(36, 25)],
        City.PAMPLONA: [(35, 32), (34, 33)],
        City.LUBECK: [(57, 54), (57, 53)],
        City.PORTO: [(23, 31)],
        City.DUBLIN: [(32, 58)],
        City.DOWNPATRICK: [(33, 61)],
        City.RATHCROGHAN: [(29, 60)],
        City.CASHEL: [(29, 56)],
        City.RASKA: [(68, 28)],
        City.FEZ: [(29, 12)],
        City.PRAGUE: [(60, 44)],
        City.KURSK: [(90, 48)],
        City.CALAIS: [(44, 50)],
        City.DUNKERQUE: [(45, 50)],
        City.NIDAROS: [(57, 71)],
        City.UPPSALA: [(65, 66)],
        City.BELOOZERO: [(87, 65)],
        City.ZAGREB: [(62, 34)],
        City.BRANDEBURG: [(59, 50), (60, 50)],
        City.BELGRADE: [(73, 35)],
        City.NAPOCA: [(73, 37)],
        City.KOENIGSBERG: [(69, 53)],
        City.KRAKOW: [(68, 44)],
        City.RIGA: [(74, 58)],
        City.CARDIFF: [(36, 54)],
        City.ABERFFRAW: [(35, 57)],
        City.VISBY: [(67, 60)],
        City.MINSK: [(79, 52)],
        City.SMOLENSK: [(84, 55)],
        City.YAROSLAVL: [(92, 61)],
        City.GRONINGEN: [(52, 54)],
        City.KALMAR: [(64, 60)],
        City.GRAZ: [(61, 37)],
        City.HALYCH: [(77, 41)],
        City.ABO: [(71, 66)],
        City.PEREKOP: [(87, 36)],
        City.NIZHNY_NOVGOROD: [(97, 58)],
        City.TANAIS: [(96, 38)],
        City.REYKJAVIK: [(2, 70)],
        City.VALLETTA: [(57, 14)],
    }
).applymap(lambda x: Tile(x))

INDY_CITIES_TO_BE_REDUCED = [
    City.INVERNESS,
    City.NORWICH,
    City.LEICESTER,
    City.UPPSALA,
]

REGIONS = EnumDataMapper(
    {
        Region.IBERIA: [
            Province.GALICIA.value,
            Province.CASTILE.value,
            Province.LEON.value,
            Province.LUSITANIA.value,
            Province.CATALONIA.value,
            Province.ARAGON.value,
            Province.VALENCIA.value,
            Province.ANDALUSIA.value,
            Province.NAVARRE.value,
            Province.LA_MANCHA.value,
        ],
        Region.FRANCE: [
            Province.NORMANDY.value,
            Province.BRETAGNE.value,
            Province.ILE_DE_FRANCE.value,
            Province.ORLEANS.value,
            Province.PICARDY.value,
        ],
        Region.BURGUNDY: [
            Province.PROVENCE.value,
            Province.BURGUNDY.value,
            Province.CHAMPAGNE.value,
            Province.FLANDERS.value,
        ],
        Region.BRITAIN: [
            Province.LONDON.value,
            Province.WALES.value,
            Province.WESSEX.value,
            Province.SCOTLAND.value,
            Province.EAST_ANGLIA.value,
            Province.MERCIA.value,
            Province.NORTHUMBRIA.value,
            Province.IRELAND.value,
        ],
        Region.SCANDINAVIA: [
            Province.DENMARK.value,
            Province.OSTERLAND.value,
            Province.NORWAY.value,
            Province.VESTFOLD.value,
            Province.GOTALAND.value,
            Province.SVEALAND.value,
            Province.NORRLAND.value,
            Province.JAMTLAND.value,
            Province.SKANELAND.value,
            Province.GOTLAND.value,
        ],
        Region.GERMANY: [
            Province.LORRAINE.value,
            Province.SWABIA.value,
            Province.SAXONY.value,
            Province.BAVARIA.value,
            Province.FRANCONIA.value,
            Province.BRANDENBURG.value,
            Province.HOLSTEIN.value,
        ],
        Region.POLAND: [
            Province.POMERANIA.value,
            Province.GALICJA.value,
            Province.GREATER_POLAND.value,
            Province.LESSER_POLAND.value,
            Province.SILESIA.value,
            Province.MASOVIA.value,
        ],
        Region.LITHUANIA: [
            Province.LITHUANIA.value,
            Province.LIVONIA.value,
            Province.ESTONIA.value,
        ],
        Region.AUSTRIA: [
            Province.CARINTHIA.value,
            Province.AUSTRIA.value,
            Province.MORAVIA.value,
            Province.BOHEMIA.value,
            Province.SILESIA.value,
        ],
        Region.HUNGARY: [
            Province.TRANSYLVANIA.value,
            Province.HUNGARY.value,
            Province.SLAVONIA.value,
            Province.PANNONIA.value,
            Province.UPPER_HUNGARY.value,
        ],
        Region.BALKANS: [
            Province.SERBIA.value,
            Province.THRACE.value,
            Province.MACEDONIA.value,
            Province.MOESIA.value,
            Province.ARBERIA.value,
            Province.DALMATIA.value,
            Province.BOSNIA.value,
            Province.BANAT.value,
        ],
        Region.GREECE: [
            Province.CONSTANTINOPLE.value,
            Province.THESSALY.value,
            Province.EPIRUS.value,
            Province.MOREA.value,
            Province.THESSALONIKI.value,
        ],
        Region.ASIA_MINOR: [
            Province.COLONEA.value,
            Province.CHARSIANON.value,
            Province.CILICIA.value,
            Province.ARMENIAKON.value,
            Province.ANATOLIKON.value,
            Province.PAPHLAGONIA.value,
            Province.THRAKESION.value,
            Province.OPSIKION.value,
        ],
        Region.MIDDLE_EAST: [
            Province.ANTIOCHIA.value,
            Province.SYRIA.value,
            Province.LEBANON.value,
            Province.ARABIA.value,
            Province.JERUSALEM.value,
        ],
        Region.AFRICA: [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
            Province.TETOUAN.value,
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.FEZ.value,
        ],
        Region.KIEV: [
            Province.MOLDOVA.value,
            Province.KIEV.value,
            Province.CRIMEA.value,
            Province.ZAPORIZHIA.value,
            Province.SLOBODA.value,
            Province.PEREYASLAVL.value,
            Province.CHERNIGOV.value,
            Province.PODOLIA.value,
            Province.MINSK.value,
        ],
        Region.ITALY: [
            Province.LOMBARDY.value,
            Province.LIGURIA.value,
            Province.VERONA.value,
            Province.TUSCANY.value,
            Province.LATIUM.value,
            Province.CALABRIA.value,
            Province.APULIA.value,
            Province.ARBERIA.value,
            Province.MALTA.value,
            Province.DALMATIA.value,
        ],
        Region.SWISS: [
            Province.BAVARIA.value,
            Province.AUSTRIA.value,
            Province.SWABIA.value,
            Province.BURGUNDY.value,
            Province.LORRAINE.value,
            Province.CHAMPAGNE.value,
            Province.PROVENCE.value,
            Province.LOMBARDY.value,
            Province.LIGURIA.value,
            Province.VERONA.value,
            Province.FRANCONIA.value,
            Province.BOHEMIA.value,
        ],
        Region.NOT_EUROPE: [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
            Province.TETOUAN.value,
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.FEZ.value,
            Province.SAHARA.value,
            Province.EGYPT.value,
            Province.ANTIOCHIA.value,
            Province.SYRIA.value,
            Province.LEBANON.value,
            Province.ARABIA.value,
            Province.JERUSALEM.value,
            Province.COLONEA.value,
            Province.CHARSIANON.value,
            Province.CILICIA.value,
            Province.ARMENIAKON.value,
            Province.ANATOLIKON.value,
            Province.PAPHLAGONIA.value,
            Province.THRAKESION.value,
            Province.OPSIKION.value,
        ],
    }
)

COMPANY_REGION = CompanyDataMapper(
    {
        Company.HOSPITALLERS: [
            Province.ANTIOCHIA,
            Province.LEBANON,
            Province.JERUSALEM,
            Province.CYPRUS,
            Province.EGYPT,
            Province.RHODES,
            Province.CRETE,
            Province.MALTA,
            Province.SICILY,
            Province.CORSICA,
            Province.SARDINIA,
            Province.LATIUM,
            Province.CALABRIA,
            Province.APULIA,
        ],
        Company.TEMPLARS: [
            Province.ANTIOCHIA,
            Province.LEBANON,
            Province.JERUSALEM,
            Province.CYPRUS,
            Province.EGYPT,
            Province.ILE_DE_FRANCE,
            Province.ORLEANS,
            Province.BURGUNDY,
            Province.CHAMPAGNE,
            Province.PICARDY,
            Province.PROVENCE,
            Province.AQUITAINE,
            Province.NORMANDY,
            Province.LONDON,
            Province.WALES,
            Province.WESSEX,
            Province.EAST_ANGLIA,
            Province.MERCIA,
            Province.NORTHUMBRIA,
        ],
        Company.TEUTONS: [
            Province.ANTIOCHIA,
            Province.LEBANON,
            Province.JERUSALEM,
            Province.CYPRUS,
            Province.EGYPT,
            Province.TRANSYLVANIA,
            Province.PRUSSIA,
            Province.LIVONIA,
            Province.ESTONIA,
            Province.POMERANIA,
            Province.BRANDENBURG,
            Province.HOLSTEIN,
            Province.SAXONY,
            Province.NETHERLANDS,
            Province.FLANDERS,
            Province.LORRAINE,
            Province.FRANCONIA,
            Province.SWABIA,
            Province.BAVARIA,
            Province.BOHEMIA,
            Province.MORAVIA,
            Province.SILESIA,
        ],
        Company.HANSA: [
            Province.SAXONY,
            Province.BRANDENBURG,
            Province.HOLSTEIN,
            Province.LONDON,
            Province.EAST_ANGLIA,
            Province.NORWAY,
            Province.VESTFOLD,
            Province.DENMARK,
            Province.SKANELAND,
            Province.GOTALAND,
            Province.GOTLAND,
            Province.SVEALAND,
            Province.PRUSSIA,
            Province.LIVONIA,
            Province.ESTONIA,
            Province.POMERANIA,
            Province.NETHERLANDS,
            Province.FLANDERS,
            Province.NOVGOROD,
            Province.KARELIA,
            Province.OSTERLAND,
        ],
        Company.MEDICI: [
            Province.TUSCANY,
            Province.LOMBARDY,
            Province.VERONA,
            Province.LATIUM,
            Province.CALABRIA,
            Province.APULIA,
            Province.DALMATIA,
            Province.ARBERIA,
            Province.EPIRUS,
            Province.MOREA,
        ],
        Company.AUGSBURG: [
            Province.BAVARIA,
            Province.SWABIA,
            Province.FRANCONIA,
            Province.AUSTRIA,
            Province.CARINTHIA,
            Province.BOHEMIA,
            Province.MORAVIA,
            Province.SILESIA,
            Province.UPPER_HUNGARY,
            Province.HUNGARY,
            Province.PANNONIA,
            Province.SLAVONIA,
        ],
        Company.ST_GEORGE: [
            Province.LIGURIA,
            Province.LOMBARDY,
            Province.TUSCANY,
            Province.LATIUM,
            Province.CORSICA,
            Province.SARDINIA,
            Province.SICILY,
            Province.CALABRIA,
            Province.APULIA,
            Province.PROVENCE,
            Province.CATALONIA,
            Province.BALEARS,
        ],
        Company.DRAGON: [
            Province.HUNGARY,
            Province.PANNONIA,
            Province.UPPER_HUNGARY,
            Province.TRANSYLVANIA,
            Province.SLAVONIA,
            Province.DALMATIA,
            Province.BANAT,
            Province.BOSNIA,
            Province.SERBIA,
            Province.ARBERIA,
            Province.WALLACHIA,
            Province.MOESIA,
        ],
        Company.CALATRAVA: [
            Province.GALICIA,
            Province.CASTILE,
            Province.LEON,
            Province.LUSITANIA,
            Province.CATALONIA,
            Province.ARAGON,
            Province.VALENCIA,
            Province.ANDALUSIA,
            Province.NAVARRE,
            Province.LA_MANCHA,
            Province.BALEARS,
        ],
    }
)

# Used for the Colony panel
COLONY_LOCATIONS = EnumDataMapper(
    {
        Colony.VINLAND: (275, 150),
        Colony.GOLD_COAST: (480, 335),
        Colony.IVORY_COAST: (440, 335),
        Colony.CUBA: (145, 265),
        Colony.HISPANIOLA: (185, 280),
        Colony.BRAZIL: (290, 410),
        Colony.HUDSON: (160, 110),
        Colony.VIRGINIA: (170, 210),
        Colony.EAST_AFRICA: (610, 390),
        Colony.CHINA: (875, 225),
        Colony.INDIA: (760, 260),
        Colony.EAST_INDIES: (930, 360),
        Colony.MALAYSIA: (870, 320),
        Colony.CAPE_TOWN: (560, 510),
        Colony.AZTECS: (60, 260),
        Colony.INCA: (170, 420),
        Colony.QUEBEC: (245, 120),
        Colony.NEW_ENGLAND: (200, 180),
        Colony.JAMAICA: (155, 285),
        Colony.PANAMA: (130, 325),
        Colony.LOUISIANA: (110, 220),
        Colony.PHILIPPINES: (960, 320),
    }
)

LAKE_LOCATIONS = EnumDataMapper(
    {
        Lake.LOUGH_NEAGH: [(32, 61)],
        Lake.LAKE_BALATON: [(64, 36)],
        Lake.DEAD_SEA: [
            (94, 4),
            (94, 5),
        ],
        Lake.SEA_OF_GALILEE: [(95, 8)],
        Lake.LAKE_TUZ: [
            (88, 19),
            (89, 19),
        ],
        Lake.LAKE_EGIRDIR: [(85, 18)],
        Lake.LAKE_BEYSEHIR: [(86, 17)],
        Lake.LAKE_GARDA: [(54, 37)],
        Lake.LAKE_GENEVA: [(49, 39)],
        Lake.LAKE_CONSTANCE: [(53, 40)],
        Lake.LAKE_SKADAR: [(66, 27)],
        Lake.LAKE_OHRID: [(69, 23)],
        Lake.LAKE_SNIARDWY: [(71, 52)],
        Lake.LAKE_VATTERN: [
            (62, 62),
            (62, 63),
        ],
        Lake.LAKE_VANERN: [
            (60, 64),
            (61, 64),
            (61, 65),
        ],
        Lake.LAKE_MALAREN: [
            (64, 64),
            (65, 64),
        ],
        Lake.LAKE_STORSJON: [(62, 71)],
        Lake.LAKE_PEIPUS: [
            (77, 60),
            (77, 61),
            (77, 62),
        ],
        Lake.LAKE_ILMEN: [(80, 61)],
        Lake.LAKE_LADOGA: [
            (79, 67),
            (79, 68),
            (80, 65),
            (80, 66),
            (80, 67),
            (80, 68),
            (80, 69),
            (81, 66),
            (81, 67),
            (81, 68),
        ],
        Lake.LAKE_ONEGA: [
            (84, 69),
            (84, 70),
            (85, 68),
            (85, 69),
            (85, 70),
        ],
        Lake.LAKE_BELOYE: [(87, 66)],
        Lake.LAKE_SAIMAA: [
            (77, 68),
            (77, 69),
            (78, 70),
        ],
        Lake.LAKE_PAIJANNE: [
            (74, 68),
            (74, 69),
        ],
        Lake.LAKE_VYGOZERO: [(85, 72)],
        Lake.LAKE_SEGOZERO: [(83, 72)],
        Lake.LAKE_KALLAVESI: [(76, 71)],
        Lake.LAKE_KEITELE: [(74, 71)],
        Lake.LAKE_PIELINEN: [(78, 72)],
        Lake.LAKE_NASIJARVI: [(72, 68)],
        Lake.LIMFJORDEN: [(55, 59)],
        Lake.TRONDHEIMFJORDEN: [(58, 71)],
    }
).applymap(lambda x: Tile(x))

CIV_CAPITAL_LOCATIONS = CivDataMapper(
    {
        Civ.BYZANTIUM: CITIES[City.CONSTANTINOPLE][0],
        Civ.FRANCE: CITIES[City.PARIS][0],
        Civ.ARABIA: CITIES[City.DAMASCUS][0],
        Civ.BULGARIA: CITIES[City.PRESLAV][0],
        Civ.CORDOBA: CITIES[City.CORDOBA][0],
        Civ.VENECIA: CITIES[City.VENICE][0],
        Civ.BURGUNDY: CITIES[City.DIJON][0],
        Civ.GERMANY: CITIES[City.FRANKFURT][0],
        Civ.NOVGOROD: CITIES[City.NOVGOROD][0],
        Civ.NORWAY: CITIES[City.TONSBERG][0],
        Civ.KIEV: CITIES[City.KIEV][0],
        Civ.HUNGARY: CITIES[City.BUDA][0],
        Civ.CASTILE: CITIES[City.LEON][0],
        Civ.DENMARK: CITIES[City.ROSKILDE][0],
        Civ.SCOTLAND: CITIES[City.EDINBURGH][0],
        Civ.POLAND: CITIES[City.POZNAN][0],
        Civ.GENOA: CITIES[City.GENOA][0],
        Civ.MOROCCO: CITIES[City.MARRAKESH][0],
        Civ.ENGLAND: CITIES[City.LONDON][0],
        Civ.PORTUGAL: CITIES[City.LISBOA][0],
        Civ.ARAGON: CITIES[City.ZARAGOZA][0],
        Civ.SWEDEN: CITIES[City.STOCKHOLM][0],
        Civ.PRUSSIA: CITIES[City.KONIGSBERG][0],
        Civ.LITHUANIA: CITIES[City.VILNUS][0],
        Civ.AUSTRIA: CITIES[City.WIEN][0],
        Civ.OTTOMAN: CITIES[City.GALLIPOLI][0],
        Civ.MOSCOW: CITIES[City.MOSCOW][0],
        Civ.DUTCH: CITIES[City.AMSTERDAM][0],
        Civ.POPE: CITIES[City.ROME][0],
    }
)

# Used for respawning
CIV_NEW_CAPITAL_LOCATIONS = CivDataMapper(
    {
        Civ.ARABIA: [
            (83, 3),
            (84, 3),
            (84, 4),
        ],  # Alexandria
        Civ.CORDOBA: [
            (48, 16),
            (50, 18),
        ],  # Tunis
        Civ.GERMANY: [(57, 41)],  # Munich
        Civ.NORWAY: [(59, 64)],  # Oslo
        Civ.KIEV: [(88, 40)],  # Stara Sich
        Civ.CASTILE: [
            (30, 27),
            (31, 27),
            (31, 28),
            (32, 28),
        ],  # Toledo or Madrid
        Civ.MOROCCO: [(25, 13)],  # Rabat
        Civ.ARAGON: [(59, 24)],  # Naples
        Civ.PRUSSIA: [
            (60, 48),
            (61, 48),
            (61, 49),
            (62, 48),
        ],  # Berlin
    }
).applymap(lambda x: Tile(x))

CIV_NEIGHBOURS = CivDataMapper(
    {
        Civ.BYZANTIUM: [
            Civ.BULGARIA,
            Civ.ARABIA,
            Civ.OTTOMAN,
        ],
        Civ.FRANCE: [
            Civ.BURGUNDY,
            Civ.ENGLAND,
            Civ.SCOTLAND,
            Civ.ARAGON,
        ],
        Civ.ARABIA: [
            Civ.BYZANTIUM,
            Civ.OTTOMAN,
        ],
        Civ.BULGARIA: [
            Civ.BYZANTIUM,
            Civ.HUNGARY,
            Civ.KIEV,
        ],
        Civ.CORDOBA: [
            Civ.CASTILE,
            Civ.PORTUGAL,
            Civ.ARAGON,
            Civ.MOROCCO,
        ],
        Civ.VENECIA: [
            Civ.GENOA,
            Civ.GERMANY,
            Civ.AUSTRIA,
            Civ.HUNGARY,
            Civ.POPE,
        ],
        Civ.BURGUNDY: [
            Civ.FRANCE,
            Civ.GENOA,
            Civ.DUTCH,
            Civ.GERMANY,
        ],
        Civ.GERMANY: [
            Civ.BURGUNDY,
            Civ.DUTCH,
            Civ.AUSTRIA,
            Civ.PRUSSIA,
            Civ.VENECIA,
            Civ.GENOA,
            Civ.POLAND,
            Civ.HUNGARY,
            Civ.DENMARK,
        ],
        Civ.NOVGOROD: [
            Civ.KIEV,
            Civ.MOSCOW,
            Civ.POLAND,
            Civ.LITHUANIA,
            Civ.PRUSSIA,
            Civ.SWEDEN,
        ],
        Civ.NORWAY: [
            Civ.DENMARK,
            Civ.SCOTLAND,
            Civ.SWEDEN,
        ],
        Civ.KIEV: [
            Civ.BULGARIA,
            Civ.MOSCOW,
            Civ.POLAND,
            Civ.LITHUANIA,
            Civ.NOVGOROD,
        ],
        Civ.HUNGARY: [
            Civ.BULGARIA,
            Civ.VENECIA,
            Civ.POLAND,
            Civ.GERMANY,
            Civ.AUSTRIA,
        ],
        Civ.CASTILE: [
            Civ.CORDOBA,
            Civ.PORTUGAL,
            Civ.ARAGON,
            Civ.MOROCCO,
        ],
        Civ.DENMARK: [
            Civ.SWEDEN,
            Civ.NORWAY,
            Civ.GERMANY,
        ],
        Civ.SCOTLAND: [
            Civ.ENGLAND,
            Civ.FRANCE,
            Civ.DUTCH,
            Civ.NORWAY,
        ],
        Civ.POLAND: [
            Civ.GERMANY,
            Civ.AUSTRIA,
            Civ.HUNGARY,
            Civ.KIEV,
            Civ.MOSCOW,
            Civ.LITHUANIA,
            Civ.PRUSSIA,
            Civ.NOVGOROD,
        ],
        Civ.GENOA: [
            Civ.GERMANY,
            Civ.VENECIA,
            Civ.BURGUNDY,
            Civ.POPE,
        ],
        Civ.MOROCCO: [
            Civ.CASTILE,
            Civ.PORTUGAL,
            Civ.CORDOBA,
        ],
        Civ.ENGLAND: [
            Civ.FRANCE,
            Civ.DUTCH,
            Civ.SCOTLAND,
        ],
        Civ.PORTUGAL: [
            Civ.CASTILE,
            Civ.CORDOBA,
            Civ.MOROCCO,
        ],
        Civ.SWEDEN: [
            Civ.NORWAY,
            Civ.DENMARK,
            Civ.PRUSSIA,
            Civ.NOVGOROD,
        ],
        Civ.ARAGON: [
            Civ.CORDOBA,
            Civ.CASTILE,
            Civ.FRANCE,
        ],
        Civ.PRUSSIA: [
            Civ.GERMANY,
            Civ.POLAND,
            Civ.LITHUANIA,
            Civ.NOVGOROD,
            Civ.SWEDEN,
        ],
        Civ.LITHUANIA: [
            Civ.KIEV,
            Civ.POLAND,
            Civ.NOVGOROD,
            Civ.PRUSSIA,
            Civ.MOSCOW,
        ],
        Civ.AUSTRIA: [
            Civ.GERMANY,
            Civ.HUNGARY,
            Civ.POLAND,
            Civ.VENECIA,
        ],
        Civ.OTTOMAN: [
            Civ.BYZANTIUM,
            Civ.ARABIA,
        ],
        Civ.MOSCOW: [
            Civ.KIEV,
            Civ.NOVGOROD,
            Civ.POLAND,
            Civ.LITHUANIA,
        ],
        Civ.DUTCH: [
            Civ.GERMANY,
            Civ.ENGLAND,
            Civ.BURGUNDY,
            Civ.SCOTLAND,
        ],
        Civ.POPE: [
            Civ.VENECIA,
            Civ.GENOA,
        ],
    }
)

# Used for stability on spawn
CIV_OLDER_NEIGHBOURS = CivDataMapper(
    {
        Civ.ARABIA: [Civ.BYZANTIUM],
        Civ.BULGARIA: [Civ.BYZANTIUM],
        Civ.KIEV: [Civ.BULGARIA],
        Civ.HUNGARY: [Civ.BULGARIA],
        Civ.CASTILE: [Civ.CORDOBA],
        Civ.DENMARK: [Civ.GERMANY],
        Civ.POLAND: [
            Civ.GERMANY,
            Civ.KIEV,
        ],
        Civ.GENOA: [
            Civ.VENECIA,
            Civ.GERMANY,
            Civ.CORDOBA,
        ],
        Civ.MOROCCO: [Civ.CORDOBA],
        Civ.ENGLAND: [
            Civ.FRANCE,
            Civ.SCOTLAND,
        ],
        Civ.PORTUGAL: [
            Civ.CASTILE,
            Civ.CORDOBA,
        ],
        Civ.ARAGON: [Civ.CASTILE],
        Civ.SWEDEN: [
            Civ.NORWAY,
            Civ.DENMARK,
            Civ.NOVGOROD,
        ],
        Civ.PRUSSIA: [Civ.POLAND],
        Civ.LITHUANIA: [
            Civ.PRUSSIA,
            Civ.NOVGOROD,
        ],
        Civ.AUSTRIA: [
            Civ.GERMANY,
            Civ.HUNGARY,
            Civ.VENECIA,
            Civ.GENOA,
        ],
        Civ.OTTOMAN: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.ARABIA,
        ],
        Civ.MOSCOW: [
            Civ.KIEV,
            Civ.POLAND,
            Civ.LITHUANIA,
            Civ.NOVGOROD,
        ],
        Civ.DUTCH: [
            Civ.GERMANY,
            Civ.FRANCE,
        ],
    }
)

# Used for the Colony panel
CIV_HOME_LOCATIONS = CivDataMapper(
    {
        Civ.BYZANTIUM: (578, 179),
        Civ.FRANCE: (480, 152),
        Civ.ARABIA: (614, 212),
        Civ.BULGARIA: (567, 166),
        Civ.CORDOBA: (455, 195),
        Civ.VENECIA: (518, 157),
        Civ.BURGUNDY: (490, 160),
        Civ.GERMANY: (510, 140),
        Civ.NOVGOROD: (580, 103),
        Civ.NORWAY: (509, 102),
        Civ.KIEV: (590, 140),
        Civ.HUNGARY: (550, 155),
        Civ.CASTILE: (460, 180),
        Civ.DENMARK: (515, 118),
        Civ.SCOTLAND: (466, 115),
        Civ.POLAND: (540, 130),
        Civ.GENOA: (503, 165),
        Civ.MOROCCO: (444, 228),
        Civ.ENGLAND: (473, 132),
        Civ.PORTUGAL: (441, 190),
        Civ.ARAGON: (470, 182),
        Civ.SWEDEN: (531, 92),
        Civ.PRUSSIA: (545, 131),
        Civ.LITHUANIA: (556, 119),
        Civ.AUSTRIA: (535, 150),
        Civ.OTTOMAN: (590, 195),
        Civ.MOSCOW: (595, 110),
        Civ.DUTCH: (492, 131),
    }
)

# Used for initial spawn location, no longer relevant for stability.
CIV_CORE_AREA = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: {
                Area.TILE_MIN: (66, 14),
                Area.TILE_MAX: (84, 26),
            },
            Civ.FRANCE: {
                Area.TILE_MIN: (42, 43),
                Area.TILE_MAX: (46, 48),
            },
            Civ.ARABIA: {
                Area.TILE_MIN: (92, 0),
                Area.TILE_MAX: (99, 12),
            },
            Civ.BULGARIA: {
                Area.TILE_MIN: (74, 27),
                Area.TILE_MAX: (80, 30),
            },
            Civ.CORDOBA: {
                Area.TILE_MIN: (24, 19),
                Area.TILE_MAX: (37, 28),
                Area.ADDITIONAL_TILES: [
                    (26, 15),
                    (26, 16),
                    (26, 17),
                    (26, 18),
                    (27, 15),
                    (27, 16),
                    (27, 17),
                    (27, 18),
                    (28, 15),
                    (28, 16),
                    (28, 17),
                    (28, 18),
                    (29, 15),
                    (29, 16),
                    (29, 17),
                    (29, 18),
                ],
            },
            Civ.VENECIA: {
                Area.TILE_MIN: (55, 33),
                Area.TILE_MAX: (59, 36),
                Area.ADDITIONAL_TILES: [
                    (60, 33),
                    (60, 34),
                    (60, 35),
                ],
            },
            Civ.BURGUNDY: {
                Area.TILE_MIN: (44, 32),
                Area.TILE_MAX: (48, 42),
                Area.ADDITIONAL_TILES: [
                    (49, 39),
                    (49, 40),
                    (49, 41),
                    (49, 42),
                ],
            },
            Civ.GERMANY: {
                Area.TILE_MIN: (51, 40),
                Area.TILE_MAX: (58, 50),
            },
            Civ.NOVGOROD: {
                Area.TILE_MIN: (79, 59),
                Area.TILE_MAX: (82, 69),
                Area.ADDITIONAL_TILES: [
                    (78, 59),
                    (78, 60),
                ],
            },
            Civ.NORWAY: {
                Area.TILE_MIN: (53, 63),
                Area.TILE_MAX: (59, 72),
            },
            Civ.KIEV: {
                Area.TILE_MIN: (79, 42),
                Area.TILE_MAX: (88, 50),
            },
            Civ.HUNGARY: {
                Area.TILE_MIN: (64, 33),
                Area.TILE_MAX: (73, 39),
            },
            Civ.CASTILE: {
                Area.TILE_MIN: (25, 30),
                Area.TILE_MAX: (32, 36),
            },
            Civ.DENMARK: {
                Area.TILE_MIN: (54, 55),
                Area.TILE_MAX: (64, 61),
            },
            Civ.SCOTLAND: {
                Area.TILE_MIN: (35, 62),
                Area.TILE_MAX: (39, 68),
                Area.ADDITIONAL_TILES: [
                    (37, 69),
                    (38, 69),
                ],
            },
            Civ.POLAND: {
                Area.TILE_MIN: (64, 43),
                Area.TILE_MAX: (70, 50),
                Area.ADDITIONAL_TILES: [
                    (63, 46),
                    (63, 47),
                    (63, 48),
                    (63, 49),
                    (63, 50),
                ],
            },
            Civ.GENOA: {
                Area.TILE_MIN: (49, 27),
                Area.TILE_MAX: (52, 35),
            },
            Civ.MOROCCO: {
                Area.TILE_MIN: (18, 3),
                Area.TILE_MAX: (31, 16),
            },
            Civ.ENGLAND: {
                Area.TILE_MIN: (37, 48),
                Area.TILE_MAX: (43, 60),
                Area.ADDITIONAL_TILES: [
                    (37, 46),
                    (37, 47),
                    (38, 46),
                    (38, 47),
                    (39, 46),
                    (39, 47),
                    (40, 46),
                    (40, 47),
                    (41, 46),
                    (41, 47),
                    (42, 47),
                ],
            },
            Civ.PORTUGAL: {
                Area.TILE_MIN: (21, 24),
                Area.TILE_MAX: (24, 32),
                Area.ADDITIONAL_TILES: [
                    (25, 27),
                    (25, 28),
                    (25, 29),
                    (25, 30),
                    (25, 31),
                ],
            },
            Civ.ARAGON: {
                Area.TILE_MIN: (35, 26),
                Area.TILE_MAX: (42, 31),
                Area.ADDITIONAL_TILES: [
                    (40, 23),
                    (42, 23),
                    (42, 24),
                    (44, 24),
                ],
            },
            Civ.SWEDEN: {
                Area.TILE_MIN: (61, 60),
                Area.TILE_MAX: (65, 70),
                Area.ADDITIONAL_TILES: [
                    (60, 61),
                    (60, 62),
                    (60, 63),
                    (61, 71),
                    (62, 71),
                    (62, 72),
                    (63, 71),
                    (63, 72),
                    (64, 71),
                    (64, 72),
                    (65, 71),
                    (65, 72),
                    (66, 64),
                    (66, 65),
                    (66, 66),
                    (66, 72),
                    (68, 65),
                    (70, 67),
                    (70, 68),
                    (71, 66),
                    (71, 67),
                    (71, 68),
                    (72, 65),
                    (72, 66),
                    (72, 67),
                ],
            },
            Civ.PRUSSIA: {
                Area.TILE_MIN: (70, 52),
                Area.TILE_MAX: (71, 58),
                Area.ADDITIONAL_TILES: [
                    (68, 51),
                    (68, 52),
                    (68, 53),
                    (69, 51),
                    (69, 52),
                    (69, 53),
                    (70, 51),
                    (71, 59),
                    (72, 57),
                    (72, 58),
                    (73, 57),
                    (73, 58),
                    (74, 57),
                    (74, 58),
                    (74, 59),
                    (74, 60),
                    (75, 57),
                    (75, 58),
                    (75, 59),
                    (75, 60),
                    (76, 58),
                    (76, 59),
                    (76, 60),
                ],
            },
            Civ.LITHUANIA: {
                Area.TILE_MIN: (72, 51),
                Area.TILE_MAX: (80, 56),
                Area.ADDITIONAL_TILES: [
                    (76, 57),
                    (77, 57),
                    (78, 57),
                    (79, 57),
                    (80, 57),
                ],
            },
            Civ.AUSTRIA: {
                Area.TILE_MIN: (59, 37),
                Area.TILE_MAX: (62, 44),
                Area.ADDITIONAL_TILES: [
                    (60, 36),
                    (61, 36),
                ],
            },
            Civ.OTTOMAN: {
                Area.TILE_MIN: (76, 16),
                Area.TILE_MAX: (84, 22),
                Area.ADDITIONAL_TILES: [
                    (76, 23),
                    (77, 23),
                    (78, 23),
                    (79, 23),
                ],
            },
            Civ.MOSCOW: {
                Area.TILE_MIN: (84, 53),
                Area.TILE_MAX: (97, 59),
                Area.ADDITIONAL_TILES: [
                    (83, 53),
                    (83, 54),
                    (83, 55),
                    (83, 56),
                    (83, 57),
                    (87, 60),
                    (88, 60),
                    (89, 60),
                    (90, 60),
                    (91, 60),
                    (92, 60),
                    (93, 60),
                    (94, 60),
                    (95, 60),
                    (96, 60),
                    (97, 60),
                    (88, 61),
                    (89, 61),
                    (90, 61),
                    (91, 61),
                    (92, 61),
                    (93, 61),
                    (94, 61),
                    (95, 61),
                    (96, 61),
                    (97, 61),
                    (88, 62),
                    (89, 62),
                    (90, 62),
                    (91, 62),
                    (92, 62),
                    (93, 62),
                    (94, 62),
                    (95, 62),
                    (96, 62),
                    (97, 62),
                    (88, 63),
                    (89, 63),
                    (90, 63),
                    (91, 63),
                    (92, 63),
                    (93, 63),
                    (94, 63),
                    (95, 63),
                    (96, 63),
                    (97, 63),
                ],
            },
            Civ.DUTCH: {
                Area.TILE_MIN: (46, 50),
                Area.TILE_MAX: (52, 55),
                Area.ADDITIONAL_TILES: [
                    (46, 49),
                    (47, 49),
                    (48, 49),
                    (49, 49),
                    (50, 49),
                ],
            },
            Civ.POPE: {
                Area.TILE_MIN: (54, 25),
                Area.TILE_MAX: (58, 29),
            },
        }
    ).apply(lambda d: parse_area_dict(d))
    # .apply(
    #     lambda area: (
    #         TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
    #         .rectangle(
    #             area[Area.TILE_MIN],
    #             area[Area.TILE_MAX],
    #         )
    #         .extend(area.get(Area.ADDITIONAL_TILES))
    #         .substract(area.get(Area.EXCEPTION_TILES))
    #         .attach_area(AreaType.CORE)
    #         .normalize()
    #         .get_results()
    #     )
    # )
)

# Used for resurrection
CIV_NORMAL_AREA = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: {
                Area.TILE_MIN: (66, 13),
                Area.TILE_MAX: (75, 24),
            },
            Civ.FRANCE: {
                Area.TILE_MIN: (33, 32),
                Area.TILE_MAX: (44, 46),
                Area.EXCEPTION_TILES: [
                    (33, 32),
                    (33, 33),
                    (33, 34),
                    (33, 35),
                    (33, 36),
                    (34, 32),
                    (34, 33),
                    (34, 34),
                    (34, 35),
                    (35, 32),
                    (35, 33),
                    (35, 34),
                    (36, 32),
                    (36, 33),
                    (37, 32),
                    (38, 32),
                ],
            },
            Civ.ARABIA: {
                Area.TILE_MIN: (53, 0),
                Area.TILE_MAX: (99, 11),
                Area.EXCEPTION_TILES: [
                    (73, 10),
                    (74, 10),
                    (75, 10),
                    (76, 10),
                    (87, 10),
                    (87, 11),
                    (88, 10),
                    (88, 11),
                    (89, 11),
                ],
            },
            Civ.BULGARIA: {
                Area.TILE_MIN: (72, 27),
                Area.TILE_MAX: (80, 31),
            },
            Civ.CORDOBA: {
                Area.TILE_MIN: (43, 8),
                Area.TILE_MAX: (52, 19),
            },
            Civ.VENECIA: {
                Area.TILE_MIN: (54, 32),
                Area.TILE_MAX: (60, 37),
                Area.EXCEPTION_TILES: [
                    (54, 32),
                    (54, 33),
                    (54, 34),
                    (55, 32),
                    (55, 33),
                    (55, 34),
                    (56, 32),
                    (56, 33),
                    (56, 34),
                    (57, 32),
                    (57, 33),
                    (58, 32),
                    (59, 37),
                    (60, 36),
                    (60, 37),
                ],
            },
            Civ.BURGUNDY: {
                Area.TILE_MIN: (45, 32),
                Area.TILE_MAX: (49, 43),
                Area.EXCEPTION_TILES: [
                    (49, 32),
                    (49, 33),
                    (49, 34),
                    (49, 35),
                    (49, 36),
                ],
            },
            Civ.GERMANY: {
                Area.TILE_MIN: (51, 43),
                Area.TILE_MAX: (61, 54),
                Area.EXCEPTION_TILES: [
                    (51, 51),
                    (51, 52),
                    (51, 53),
                    (51, 54),
                    (52, 51),
                    (52, 52),
                    (52, 53),
                    (52, 54),
                    (59, 48),
                    (59, 49),
                    (59, 50),
                    (59, 51),
                    (59, 52),
                    (59, 53),
                    (59, 54),
                    (60, 48),
                    (60, 49),
                    (60, 50),
                    (60, 51),
                    (60, 52),
                    (60, 53),
                    (60, 54),
                    (61, 48),
                    (61, 49),
                    (61, 50),
                    (61, 51),
                    (61, 52),
                    (61, 53),
                    (61, 54),
                ],
            },
            Civ.NOVGOROD: {
                Area.TILE_MIN: (77, 59),
                Area.TILE_MAX: (88, 72),
                Area.EXCEPTION_TILES: [
                    (84, 59),
                    (84, 60),
                    (85, 59),
                    (85, 60),
                    (85, 61),
                    (86, 59),
                    (86, 60),
                    (86, 61),
                    (86, 62),
                    (87, 59),
                    (87, 60),
                    (87, 61),
                    (87, 62),
                    (88, 59),
                    (88, 60),
                    (88, 61),
                    (88, 62),
                ],
            },
            Civ.NORWAY: {
                Area.TILE_MIN: (53, 63),
                Area.TILE_MAX: (58, 72),
            },
            Civ.KIEV: {
                Area.TILE_MIN: (78, 41),
                Area.TILE_MAX: (91, 50),
                Area.EXCEPTION_TILES: [
                    (87, 41),
                    (88, 41),
                    (89, 41),
                    (90, 41),
                    (91, 41),
                ],
            },
            Civ.HUNGARY: {
                Area.TILE_MIN: (63, 32),
                Area.TILE_MAX: (77, 41),
                Area.EXCEPTION_TILES: [
                    (63, 32),
                    (63, 39),
                    (63, 40),
                    (63, 41),
                    (64, 41),
                    (72, 32),
                    (73, 32),
                    (74, 32),
                    (75, 32),
                    (75, 41),
                    (76, 32),
                    (76, 40),
                    (76, 41),
                    (77, 32),
                    (77, 39),
                    (77, 40),
                    (77, 41),
                ],
            },
            Civ.CASTILE: {
                Area.TILE_MIN: (25, 26),
                Area.TILE_MAX: (34, 36),
                Area.EXCEPTION_TILES: [
                    (25, 26),
                    (25, 27),
                    (25, 28),
                    (25, 29),
                    (25, 30),
                    (25, 31),
                    (34, 36),
                ],
            },
            Civ.DENMARK: {
                Area.TILE_MIN: (54, 55),
                Area.TILE_MAX: (59, 61),
            },
            Civ.SCOTLAND: {
                Area.TILE_MIN: (34, 63),
                Area.TILE_MAX: (39, 69),
                Area.EXCEPTION_TILES: [
                    (34, 69),
                ],
            },
            Civ.POLAND: {
                Area.TILE_MIN: (63, 43),
                Area.TILE_MAX: (77, 50),
                Area.EXCEPTION_TILES: [
                    (63, 43),
                    (63, 44),
                    (63, 45),
                    (64, 43),
                    (64, 44),
                    (65, 43),
                ],
            },
            Civ.GENOA: {
                Area.TILE_MIN: (49, 22),
                Area.TILE_MAX: (52, 36),
            },
            Civ.MOROCCO: {
                Area.TILE_MIN: (18, 3),
                Area.TILE_MAX: (27, 13),
            },
            Civ.ENGLAND: {
                Area.TILE_MIN: (32, 50),
                Area.TILE_MAX: (43, 62),
                Area.EXCEPTION_TILES: [
                    (32, 55),
                    (32, 56),
                    (32, 57),
                    (32, 58),
                    (32, 59),
                    (32, 60),
                    (32, 61),
                    (32, 62),
                    (33, 56),
                    (33, 57),
                    (33, 58),
                    (33, 59),
                    (33, 60),
                    (33, 61),
                    (33, 62),
                ],
            },
            Civ.PORTUGAL: {
                Area.TILE_MIN: (21, 21),
                Area.TILE_MAX: (25, 32),
                Area.EXCEPTION_TILES: [
                    (25, 21),
                    (25, 22),
                    (25, 23),
                    (25, 24),
                    (25, 25),
                    (25, 26),
                    (25, 32),
                ],
            },
            Civ.ARAGON: {
                Area.TILE_MIN: (54, 16),
                Area.TILE_MAX: (64, 26),
            },
            Civ.SWEDEN: {
                Area.TILE_MIN: (60, 59),
                Area.TILE_MAX: (75, 72),
                Area.EXCEPTION_TILES: [
                    (60, 59),
                    (60, 60),
                    (60, 61),
                    (60, 70),
                    (60, 71),
                    (60, 72),
                    (61, 59),
                    (61, 60),
                    (61, 72),
                    (70, 59),
                    (70, 60),
                    (70, 61),
                    (71, 59),
                    (71, 60),
                    (71, 61),
                    (72, 59),
                    (72, 60),
                    (72, 61),
                    (73, 59),
                    (73, 60),
                    (73, 61),
                    (73, 62),
                    (74, 59),
                    (74, 60),
                    (74, 61),
                    (74, 62),
                    (74, 63),
                    (75, 59),
                    (75, 60),
                    (75, 61),
                    (75, 62),
                    (75, 63),
                ],
            },
            Civ.PRUSSIA: {
                Area.TILE_MIN: (59, 48),
                Area.TILE_MAX: (71, 55),
                Area.EXCEPTION_TILES: [
                    (59, 55),
                    (60, 55),
                    (61, 55),
                    (63, 48),
                    (63, 49),
                    (63, 50),
                    (64, 48),
                    (64, 49),
                    (64, 50),
                    (65, 48),
                    (65, 49),
                    (65, 50),
                    (66, 48),
                    (66, 49),
                    (66, 50),
                    (67, 48),
                    (67, 49),
                    (67, 50),
                    (68, 48),
                    (68, 49),
                    (68, 50),
                    (69, 48),
                    (69, 49),
                    (69, 50),
                    (70, 48),
                    (70, 49),
                    (70, 50),
                    (71, 48),
                    (71, 49),
                    (71, 50),
                    (71, 55),
                ],
            },
            Civ.LITHUANIA: {
                Area.TILE_MIN: (70, 51),
                Area.TILE_MAX: (77, 63),
                Area.EXCEPTION_TILES: [
                    (70, 51),
                    (70, 52),
                    (70, 53),
                    (70, 54),
                    (70, 55),
                    (70, 59),
                    (70, 60),
                    (70, 61),
                    (70, 62),
                    (70, 63),
                    (71, 51),
                    (71, 52),
                    (71, 53),
                    (71, 54),
                    (71, 60),
                    (71, 61),
                    (71, 62),
                    (71, 63),
                    (72, 51),
                    (72, 60),
                    (72, 61),
                    (72, 62),
                    (72, 63),
                    (73, 63),
                    (77, 59),
                    (77, 60),
                    (77, 61),
                    (77, 62),
                    (77, 63),
                ],
            },
            Civ.AUSTRIA: {
                Area.TILE_MIN: (57, 36),
                Area.TILE_MAX: (63, 42),
                Area.EXCEPTION_TILES: [
                    (57, 36),
                    (57, 37),
                    (58, 36),
                    (58, 37),
                    (59, 36),
                    (63, 36),
                    (63, 37),
                    (63, 38),
                ],
            },
            Civ.OTTOMAN: {
                Area.TILE_MIN: (76, 14),
                Area.TILE_MAX: (98, 27),
                Area.EXCEPTION_TILES: [
                    (76, 27),
                    (77, 27),
                    (78, 27),
                    (79, 27),
                    (80, 27),
                ],
            },
            Civ.MOSCOW: {
                Area.TILE_MIN: (83, 51),
                Area.TILE_MAX: (98, 63),
                Area.EXCEPTION_TILES: [
                    (83, 59),
                    (83, 60),
                    (83, 61),
                    (83, 62),
                    (83, 63),
                    (84, 61),
                    (84, 62),
                    (84, 63),
                    (85, 62),
                    (85, 63),
                    (86, 63),
                    (87, 63),
                    (88, 63),
                ],
            },
            Civ.DUTCH: {
                Area.TILE_MIN: (47, 50),
                Area.TILE_MAX: (52, 54),
                Area.EXCEPTION_TILES: [
                    (51, 50),
                    (52, 50),
                ],
            },
            Civ.POPE: {
                Area.TILE_MIN: (54, 25),
                Area.TILE_MAX: (58, 29),
            },
        }
    ).apply(lambda d: parse_area_dict(d))
    # .apply(
    #     lambda area: (
    #         TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
    #         .rectangle(
    #             area[Area.TILE_MIN],
    #             area[Area.TILE_MAX],
    #         )
    #         .extend(area.get(Area.ADDITIONAL_TILES))
    #         .substract(area.get(Area.EXCEPTION_TILES))
    #         .attach_area(AreaType.NORMAL)
    #         .normalize()
    #         .get_results()
    #     )
    # )
)

# Used in civ birth only
CIV_BROADER_AREA = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: {
                Area.TILE_MIN: (68, 14),
                Area.TILE_MAX: (83, 27),
            },
            Civ.FRANCE: {
                Area.TILE_MIN: (39, 41),
                Area.TILE_MAX: (49, 51),
            },
            Civ.ARABIA: {
                Area.TILE_MIN: (92, 7),
                Area.TILE_MAX: (99, 15),
            },
            Civ.BULGARIA: {
                Area.TILE_MIN: (71, 28),
                Area.TILE_MAX: (80, 31),
            },
            Civ.CORDOBA: {
                Area.TILE_MIN: (24, 23),
                Area.TILE_MAX: (34, 33),
            },
            Civ.VENECIA: {
                Area.TILE_MIN: (52, 29),
                Area.TILE_MAX: (62, 39),
            },
            Civ.BURGUNDY: {
                Area.TILE_MIN: (42, 36),
                Area.TILE_MAX: (52, 46),
            },
            Civ.GERMANY: {
                Area.TILE_MIN: (49, 41),
                Area.TILE_MAX: (58, 51),
            },
            Civ.NOVGOROD: {
                Area.TILE_MIN: (77, 59),
                Area.TILE_MAX: (89, 72),
            },
            Civ.NORWAY: {
                Area.TILE_MIN: (53, 63),
                Area.TILE_MAX: (61, 72),
            },
            Civ.KIEV: {
                Area.TILE_MIN: (81, 37),
                Area.TILE_MAX: (91, 47),
            },
            Civ.HUNGARY: {
                Area.TILE_MIN: (64, 27),
                Area.TILE_MAX: (74, 37),
            },
            Civ.CASTILE: {
                Area.TILE_MIN: (23, 31),
                Area.TILE_MAX: (33, 41),
            },
            Civ.DENMARK: {
                Area.TILE_MIN: (55, 55),
                Area.TILE_MAX: (59, 60),
            },
            Civ.SCOTLAND: {
                Area.TILE_MIN: (31, 57),
                Area.TILE_MAX: (45, 69),
            },
            Civ.POLAND: {
                Area.TILE_MIN: (64, 42),
                Area.TILE_MAX: (74, 52),
            },
            Civ.GENOA: {
                Area.TILE_MIN: (45, 29),
                Area.TILE_MAX: (55, 39),
            },
            Civ.MOROCCO: {
                Area.TILE_MIN: (11, 2),
                Area.TILE_MAX: (29, 27),
            },
            Civ.ENGLAND: {
                Area.TILE_MIN: (38, 49),
                Area.TILE_MAX: (48, 59),
            },
            Civ.PORTUGAL: {
                Area.TILE_MIN: (17, 27),
                Area.TILE_MAX: (27, 37),
            },
            Civ.ARAGON: {
                Area.TILE_MIN: (33, 25),
                Area.TILE_MAX: (43, 34),
            },
            Civ.SWEDEN: {
                Area.TILE_MIN: (60, 58),
                Area.TILE_MAX: (77, 72),
            },
            Civ.PRUSSIA: {
                Area.TILE_MIN: (59, 49),
                Area.TILE_MAX: (72, 55),
            },
            Civ.LITHUANIA: {
                Area.TILE_MIN: (68, 45),
                Area.TILE_MAX: (82, 64),
            },
            Civ.AUSTRIA: {
                Area.TILE_MIN: (56, 35),
                Area.TILE_MAX: (66, 45),
            },
            Civ.OTTOMAN: {
                Area.TILE_MIN: (83, 17),
                Area.TILE_MAX: (93, 27),
            },
            Civ.MOSCOW: {
                Area.TILE_MIN: (83, 51),
                Area.TILE_MAX: (93, 61),
            },
            Civ.DUTCH: {
                Area.TILE_MIN: (44, 47),
                Area.TILE_MAX: (54, 57),
            },
            Civ.POPE: {
                Area.TILE_MIN: (54, 25),
                Area.TILE_MAX: (58, 29),
            },
        }
    ).apply(lambda d: parse_area_dict(d))
    # .apply(
    #     lambda area: (
    #         TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
    #         .rectangle(
    #             area[Area.TILE_MIN],
    #             area[Area.TILE_MAX],
    #         )
    #         .extend(area.get(Area.ADDITIONAL_TILES))
    #         .substract(area.get(Area.EXCEPTION_TILES))
    #         .attach_area(AreaType.BROADER)
    #         .normalize()
    #         .get_results()
    #     )
    # )
)

CIV_AREAS = CivDataMapper(
    dict(
        (
            civ,
            {
                AreaType.CORE: CIV_CORE_AREA[civ],
                AreaType.NORMAL: CIV_NORMAL_AREA[civ],
                AreaType.BROADER: CIV_BROADER_AREA[civ],
            },
        )
        for civ in CIV_CORE_AREA.keys()
        if civ not in MINOR_CIVS
    )
)

CIV_PROVINCES = CivDataMapper(
    {
        Civ.BYZANTIUM: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.CONSTANTINOPLE,
                    Province.THRACE,
                    Province.THESSALY,
                    Province.THESSALONIKI,
                    Province.EPIRUS,
                    Province.MOREA,
                    Province.OPSIKION,
                    Province.PAPHLAGONIA,
                    Province.THRAKESION,
                    Province.CILICIA,
                    Province.ANATOLIKON,
                    Province.ARMENIAKON,
                    Province.CHARSIANON,
                    Province.COLONEA,
                    Province.ANTIOCHIA,
                ],
                ProvinceType.HISTORICAL: [
                    Province.MOESIA,
                    Province.SERBIA,
                    Province.MACEDONIA,
                    Province.ARBERIA,
                    Province.CYPRUS,
                    Province.CRETE,
                    Province.RHODES,
                    Province.SYRIA,
                    Province.LEBANON,
                    Province.JERUSALEM,
                    Province.EGYPT,
                    Province.CYRENAICA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.CALABRIA,
                    Province.APULIA,
                    Province.SICILY,
                    Province.MALTA,
                    Province.TRIPOLITANIA,
                    Province.IFRIQIYA,
                ],
                ProvinceType.CONTESTED: [
                    Province.CRIMEA,
                    Province.ARABIA,
                    Province.BOSNIA,
                    Province.SLAVONIA,
                    Province.DALMATIA,
                    Province.VERONA,
                    Province.LOMBARDY,
                    Province.LIGURIA,
                    Province.TUSCANY,
                    Province.LATIUM,
                    Province.SARDINIA,
                    Province.CORSICA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.FRANCE: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.ILE_DE_FRANCE,
                    Province.ORLEANS,
                    Province.CHAMPAGNE,
                ],
                ProvinceType.HISTORICAL: [
                    Province.PICARDY,
                    Province.NORMANDY,
                    Province.AQUITAINE,
                    Province.LORRAINE,
                ],
                ProvinceType.POTENTIAL: [
                    Province.BRETAGNE,
                    Province.PROVENCE,
                    Province.BURGUNDY,
                    Province.FLANDERS,
                ],
                ProvinceType.CONTESTED: [
                    Province.CATALONIA,
                    Province.ARAGON,
                    Province.NAVARRE,
                    Province.NETHERLANDS,
                    Province.BAVARIA,
                    Province.SAXONY,
                    Province.SWABIA,
                    Province.FRANCONIA,
                    Province.LOMBARDY,
                    Province.LIGURIA,
                    Province.CORSICA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.ARABIA: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.SYRIA,
                    Province.LEBANON,
                    Province.JERUSALEM,
                    Province.ARABIA,
                ],
                ProvinceType.HISTORICAL: [
                    Province.EGYPT,
                    Province.CYRENAICA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.ANTIOCHIA,
                    Province.CYPRUS,
                    Province.IFRIQIYA,
                    Province.TRIPOLITANIA,
                ],
                ProvinceType.CONTESTED: [
                    Province.ORAN,
                    Province.ALGIERS,
                    Province.SICILY,
                    Province.MALTA,
                    Province.CRETE,
                    Province.RHODES,
                    Province.CILICIA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.BULGARIA: EnumDataMapper(
            {
                ProvinceType.CORE: [Province.MOESIA],
                ProvinceType.HISTORICAL: [
                    Province.MACEDONIA,
                    Province.WALLACHIA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.THRACE,
                    Province.THESSALONIKI,
                ],
                ProvinceType.CONTESTED: [
                    Province.SERBIA,
                    Province.BANAT,
                    Province.EPIRUS,
                    Province.ARBERIA,
                    Province.CONSTANTINOPLE,
                ],
            },
            do_not_cast=True,
        ),
        Civ.CORDOBA: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.ANDALUSIA,
                    Province.VALENCIA,
                    Province.LA_MANCHA,
                ],
                ProvinceType.HISTORICAL: [Province.TETOUAN],
                ProvinceType.POTENTIAL: [
                    Province.MOROCCO,
                    Province.FEZ,
                    Province.MARRAKESH,
                    Province.CATALONIA,
                    Province.ARAGON,
                    Province.BALEARS,
                ],
                ProvinceType.CONTESTED: [
                    Province.LEON,
                    Province.LUSITANIA,
                    Province.NAVARRE,
                    Province.CASTILE,
                    Province.ORAN,
                ],
            },
            do_not_cast=True,
        ),
        Civ.VENECIA: EnumDataMapper(
            {
                ProvinceType.CORE: [Province.VERONA],
                ProvinceType.HISTORICAL: [Province.DALMATIA],
                ProvinceType.POTENTIAL: [
                    Province.TUSCANY,
                    Province.ARBERIA,
                    Province.CRETE,
                    Province.CYPRUS,
                ],
                ProvinceType.CONTESTED: [
                    Province.EPIRUS,
                    Province.MOREA,
                    Province.RHODES,
                    Province.CONSTANTINOPLE,
                ],
            },
            do_not_cast=True,
        ),
        Civ.BURGUNDY: EnumDataMapper(
            {
                ProvinceType.CORE: [Province.BURGUNDY],
                ProvinceType.HISTORICAL: [
                    Province.PROVENCE,
                    Province.FLANDERS,
                ],
                ProvinceType.POTENTIAL: [
                    Province.CHAMPAGNE,
                    Province.PICARDY,
                    Province.ILE_DE_FRANCE,
                    Province.AQUITAINE,
                    Province.ORLEANS,
                    Province.NORMANDY,
                ],
                ProvinceType.CONTESTED: [
                    Province.LORRAINE,
                    Province.SWABIA,
                    Province.LOMBARDY,
                    Province.LIGURIA,
                    Province.BRETAGNE,
                ],
            },
            do_not_cast=True,
        ),
        Civ.GERMANY: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.FRANCONIA,
                    Province.LORRAINE,
                    Province.BAVARIA,
                    Province.SWABIA,
                    Province.SAXONY,
                ],
                ProvinceType.HISTORICAL: [Province.BRANDENBURG],
                ProvinceType.POTENTIAL: [
                    Province.BOHEMIA,
                    Province.HOLSTEIN,
                    Province.POMERANIA,
                    Province.NETHERLANDS,
                    Province.FLANDERS,
                    Province.LOMBARDY,
                ],
                ProvinceType.CONTESTED: [
                    Province.CHAMPAGNE,
                    Province.PICARDY,
                    Province.BURGUNDY,
                    Province.LIGURIA,
                    Province.VERONA,
                    Province.TUSCANY,
                    Province.AUSTRIA,
                    Province.MORAVIA,
                    Province.SILESIA,
                    Province.GREATER_POLAND,
                    Province.CARINTHIA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.NOVGOROD: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.NOVGOROD,
                    Province.KARELIA,
                ],
                ProvinceType.HISTORICAL: [
                    Province.ROSTOV,
                    Province.VOLOGDA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.ESTONIA,
                    Province.OSTERLAND,
                ],
                ProvinceType.CONTESTED: [
                    Province.SMOLENSK,
                    Province.POLOTSK,
                    Province.LIVONIA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.NORWAY: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.NORWAY,
                    Province.VESTFOLD,
                ],
                ProvinceType.HISTORICAL: [Province.ICELAND],
                ProvinceType.POTENTIAL: [
                    Province.THE_ISLES,
                    Province.JAMTLAND,
                ],
                ProvinceType.CONTESTED: [
                    Province.SCOTLAND,
                    Province.NORTHUMBRIA,
                    Province.IRELAND,
                    Province.NORMANDY,
                    Province.SVEALAND,
                    Province.NORRLAND,
                    Province.SICILY,
                    Province.APULIA,
                    Province.CALABRIA,
                    Province.MALTA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.KIEV: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.KIEV,
                    Province.SLOBODA,
                    Province.PEREYASLAVL,
                    Province.CHERNIGOV,
                ],
                ProvinceType.HISTORICAL: [
                    Province.PODOLIA,
                    Province.VOLHYNIA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.MINSK,
                    Province.SMOLENSK,
                    Province.ZAPORIZHIA,
                ],
                ProvinceType.CONTESTED: [
                    Province.MOLDOVA,
                    Province.GALICJA,
                    Province.BREST,
                    Province.POLOTSK,
                    Province.NOVGOROD,
                    Province.MOSCOW,
                    Province.MUROM,
                    Province.SIMBIRSK,
                    Province.CRIMEA,
                    Province.DONETS,
                    Province.KUBAN,
                ],
            },
            do_not_cast=True,
        ),
        Civ.HUNGARY: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.HUNGARY,
                    Province.UPPER_HUNGARY,
                    Province.PANNONIA,
                    Province.TRANSYLVANIA,
                ],
                ProvinceType.HISTORICAL: [
                    Province.SLAVONIA,
                    Province.BANAT,
                    Province.BOSNIA,
                    Province.DALMATIA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.MORAVIA,
                    Province.AUSTRIA,
                    Province.CARINTHIA,
                ],
                ProvinceType.CONTESTED: [
                    Province.SERBIA,
                    Province.WALLACHIA,
                    Province.MOLDOVA,
                    Province.GALICJA,
                    Province.BAVARIA,
                    Province.BOHEMIA,
                    Province.SILESIA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.CASTILE: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.LEON,
                    Province.GALICIA,
                    Province.CASTILE,
                ],
                ProvinceType.HISTORICAL: [],
                ProvinceType.POTENTIAL: [
                    Province.NAVARRE,
                    Province.ANDALUSIA,
                    Province.VALENCIA,
                    Province.LA_MANCHA,
                    Province.CANARIES,
                    Province.MADEIRA,
                ],
                ProvinceType.CONTESTED: [
                    Province.LUSITANIA,
                    Province.CATALONIA,
                    Province.ARAGON,
                    Province.BALEARS,
                    Province.AQUITAINE,
                    Province.PROVENCE,
                    Province.TETOUAN,
                    Province.FEZ,
                    Province.ORAN,
                    Province.ALGIERS,
                    Province.SARDINIA,
                    Province.CORSICA,
                    Province.AZORES,
                    Province.SICILY,
                    Province.CALABRIA,
                    Province.APULIA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.DENMARK: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.DENMARK,
                    Province.SKANELAND,
                ],
                ProvinceType.HISTORICAL: [],
                ProvinceType.POTENTIAL: [
                    Province.ESTONIA,
                    Province.GOTLAND,
                    Province.HOLSTEIN,
                ],
                ProvinceType.CONTESTED: [
                    Province.GOTALAND,
                    Province.SVEALAND,
                    Province.NORTHUMBRIA,
                    Province.MERCIA,
                    Province.EAST_ANGLIA,
                    Province.LONDON,
                    Province.BRANDENBURG,
                    Province.NORWAY,
                    Province.VESTFOLD,
                    Province.NORMANDY,
                    Province.SICILY,
                    Province.APULIA,
                    Province.CALABRIA,
                    Province.MALTA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.SCOTLAND: EnumDataMapper(
            {
                ProvinceType.CORE: [Province.SCOTLAND],
                ProvinceType.HISTORICAL: [Province.THE_ISLES],
                ProvinceType.POTENTIAL: [Province.NORTHUMBRIA],
                ProvinceType.CONTESTED: [
                    Province.IRELAND,
                    Province.MERCIA,
                    Province.WALES,
                ],
            },
            do_not_cast=True,
        ),
        Civ.POLAND: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.GREATER_POLAND,
                    Province.LESSER_POLAND,
                    Province.MASOVIA,
                ],
                ProvinceType.HISTORICAL: [
                    Province.BREST,
                    Province.GALICJA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.POMERANIA,
                    Province.SILESIA,
                    Province.SUVALKIJA,
                ],
                ProvinceType.CONTESTED: [
                    Province.PRUSSIA,
                    Province.LITHUANIA,
                    Province.POLOTSK,
                    Province.MINSK,
                    Province.VOLHYNIA,
                    Province.PODOLIA,
                    Province.MOLDOVA,
                    Province.KIEV,
                ],
            },
            do_not_cast=True,
        ),
        Civ.GENOA: EnumDataMapper(
            {
                ProvinceType.CORE: [Province.LIGURIA],
                ProvinceType.HISTORICAL: [
                    Province.CORSICA,
                    Province.SARDINIA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.SICILY,
                    Province.MALTA,
                    Province.LOMBARDY,
                    Province.TUSCANY,
                    Province.RHODES,
                    Province.CRIMEA,
                ],
                ProvinceType.CONTESTED: [
                    Province.CONSTANTINOPLE,
                    Province.CRETE,
                    Province.CYPRUS,
                    Province.MOREA,
                    Province.ARMENIAKON,
                    Province.PAPHLAGONIA,
                    Province.THRAKESION,
                ],
            },
            do_not_cast=True,
        ),
        Civ.MOROCCO: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.MARRAKESH,
                    Province.MOROCCO,
                    Province.FEZ,
                ],
                ProvinceType.HISTORICAL: [Province.TETOUAN],
                ProvinceType.POTENTIAL: [
                    Province.ORAN,
                    Province.ALGIERS,
                ],
                ProvinceType.CONTESTED: [
                    Province.IFRIQIYA,
                    Province.ANDALUSIA,
                    Province.VALENCIA,
                    Province.TRIPOLITANIA,
                    Province.SAHARA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.ENGLAND: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.LONDON,
                    Province.EAST_ANGLIA,
                    Province.MERCIA,
                    Province.WESSEX,
                ],
                ProvinceType.HISTORICAL: [Province.NORTHUMBRIA],
                ProvinceType.POTENTIAL: [Province.WALES],
                ProvinceType.CONTESTED: [
                    Province.ILE_DE_FRANCE,
                    Province.BRETAGNE,
                    Province.AQUITAINE,
                    Province.ORLEANS,
                    Province.CHAMPAGNE,
                    Province.FLANDERS,
                    Province.NORMANDY,
                    Province.PICARDY,
                    Province.SCOTLAND,
                    Province.THE_ISLES,
                    Province.IRELAND,
                ],
            },
            do_not_cast=True,
        ),
        Civ.PORTUGAL: EnumDataMapper(
            {
                ProvinceType.CORE: [Province.LUSITANIA],
                ProvinceType.HISTORICAL: [Province.AZORES],
                ProvinceType.POTENTIAL: [
                    Province.MADEIRA,
                    Province.CANARIES,
                    Province.ANDALUSIA,
                ],
                ProvinceType.CONTESTED: [
                    Province.MOROCCO,
                    Province.TETOUAN,
                    Province.LEON,
                    Province.GALICIA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.ARAGON: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.ARAGON,
                    Province.CATALONIA,
                    Province.BALEARS,
                    Province.VALENCIA,
                ],
                ProvinceType.HISTORICAL: [],
                ProvinceType.POTENTIAL: [
                    Province.NAVARRE,
                    Province.ANDALUSIA,
                    Province.LA_MANCHA,
                    Province.SARDINIA,
                    Province.SICILY,
                    Province.APULIA,
                    Province.CALABRIA,
                    Province.MALTA,
                ],
                ProvinceType.CONTESTED: [
                    Province.CASTILE,
                    Province.PROVENCE,
                    Province.CORSICA,
                    Province.THESSALY,
                ],
            },
            do_not_cast=True,
        ),
        Civ.SWEDEN: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.NORRLAND,
                    Province.SVEALAND,
                ],
                ProvinceType.HISTORICAL: [
                    Province.GOTALAND,
                    Province.GOTLAND,
                ],
                ProvinceType.POTENTIAL: [
                    Province.JAMTLAND,
                    Province.OSTERLAND,
                    Province.KARELIA,
                    Province.ESTONIA,
                ],
                ProvinceType.CONTESTED: [
                    Province.SKANELAND,
                    Province.VESTFOLD,
                    Province.POMERANIA,
                    Province.LIVONIA,
                    Province.PRUSSIA,
                    Province.NOVGOROD,
                ],
            },
            do_not_cast=True,
        ),
        Civ.PRUSSIA: EnumDataMapper(
            {
                ProvinceType.CORE: [Province.PRUSSIA],
                ProvinceType.HISTORICAL: [],
                ProvinceType.POTENTIAL: [
                    Province.POMERANIA,
                    Province.LIVONIA,
                ],
                ProvinceType.CONTESTED: [
                    Province.BRANDENBURG,
                    Province.ESTONIA,
                    Province.GOTLAND,
                    Province.LITHUANIA,
                    Province.SUVALKIJA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.LITHUANIA: EnumDataMapper(
            {
                ProvinceType.CORE: [Province.LITHUANIA],
                ProvinceType.HISTORICAL: [
                    Province.SUVALKIJA,
                    Province.MINSK,
                    Province.POLOTSK,
                ],
                ProvinceType.POTENTIAL: [
                    Province.BREST,
                    Province.PODOLIA,
                    Province.VOLHYNIA,
                    Province.KIEV,
                ],
                ProvinceType.CONTESTED: [
                    Province.GREATER_POLAND,
                    Province.LESSER_POLAND,
                    Province.MASOVIA,
                    Province.GALICJA,
                    Province.SLOBODA,
                    Province.PEREYASLAVL,
                    Province.LIVONIA,
                    Province.ESTONIA,
                    Province.NOVGOROD,
                    Province.SMOLENSK,
                    Province.CHERNIGOV,
                ],
            },
            do_not_cast=True,
        ),
        Civ.AUSTRIA: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.AUSTRIA,
                    Province.CARINTHIA,
                ],
                ProvinceType.HISTORICAL: [
                    Province.BOHEMIA,
                    Province.MORAVIA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.BAVARIA,
                    Province.SILESIA,
                    Province.PANNONIA,
                    Province.UPPER_HUNGARY,
                ],
                ProvinceType.CONTESTED: [
                    Province.VERONA,
                    Province.HUNGARY,
                    Province.TRANSYLVANIA,
                    Province.SLAVONIA,
                    Province.DALMATIA,
                    Province.LESSER_POLAND,
                    Province.GALICJA,
                    Province.NETHERLANDS,
                    Province.FLANDERS,
                ],
            },
            do_not_cast=True,
        ),
        Civ.OTTOMAN: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.OPSIKION,
                    Province.THRAKESION,
                    Province.PAPHLAGONIA,
                    Province.ANATOLIKON,
                    Province.CONSTANTINOPLE,
                ],
                ProvinceType.HISTORICAL: [
                    Province.THRACE,
                    Province.ARMENIAKON,
                    Province.CHARSIANON,
                    Province.CILICIA,
                ],
                ProvinceType.POTENTIAL: [
                    Province.COLONEA,
                    Province.ANTIOCHIA,
                    Province.SYRIA,
                    Province.LEBANON,
                    Province.JERUSALEM,
                    Province.EGYPT,
                    Province.ARABIA,
                    Province.MACEDONIA,
                    Province.THESSALONIKI,
                    Province.MOESIA,
                    Province.CYPRUS,
                    Province.RHODES,
                ],
                ProvinceType.CONTESTED: [
                    Province.THESSALY,
                    Province.EPIRUS,
                    Province.MOREA,
                    Province.ARBERIA,
                    Province.WALLACHIA,
                    Province.SERBIA,
                    Province.BOSNIA,
                    Province.BANAT,
                    Province.SLAVONIA,
                    Province.PANNONIA,
                    Province.HUNGARY,
                    Province.TRANSYLVANIA,
                    Province.MOLDOVA,
                    Province.CRIMEA,
                    Province.CRETE,
                    Province.CYRENAICA,
                    Province.TRIPOLITANIA,
                    Province.KUBAN,
                ],
            },
            do_not_cast=True,
        ),
        Civ.MOSCOW: EnumDataMapper(
            {
                ProvinceType.CORE: [
                    Province.MOSCOW,
                    Province.MUROM,
                    Province.ROSTOV,
                    Province.SMOLENSK,
                ],
                ProvinceType.HISTORICAL: [
                    Province.NIZHNYNOVGOROD,
                    Province.SIMBIRSK,
                    Province.PEREYASLAVL,
                    Province.CHERNIGOV,
                ],
                ProvinceType.POTENTIAL: [
                    Province.NOVGOROD,
                    Province.VOLOGDA,
                    Province.KIEV,
                    Province.MINSK,
                    Province.POLOTSK,
                    Province.VOLHYNIA,
                    Province.PODOLIA,
                    Province.DONETS,
                    Province.SLOBODA,
                    Province.ZAPORIZHIA,
                ],
                ProvinceType.CONTESTED: [
                    Province.CRIMEA,
                    Province.MOLDOVA,
                    Province.GALICJA,
                    Province.KUBAN,
                    Province.BREST,
                    Province.LITHUANIA,
                    Province.LIVONIA,
                    Province.ESTONIA,
                    Province.KARELIA,
                    Province.OSTERLAND,
                    Province.PRUSSIA,
                    Province.SUVALKIJA,
                ],
            },
            do_not_cast=True,
        ),
        Civ.DUTCH: EnumDataMapper(
            {
                ProvinceType.CORE: [Province.NETHERLANDS],
                ProvinceType.HISTORICAL: [Province.FLANDERS],
                ProvinceType.POTENTIAL: [],
                ProvinceType.CONTESTED: [],
            },
            do_not_cast=True,
        ),
    },
)

CIV_EVENT_DRIVE_PROVINCES = CivDataMapper(
    {
        Civ.ARABIA: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.BYZANTIUM, Province.CYRENAICA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.TRIPOLITANIA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.IFRIQIYA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.EGYPT, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.ARABIA, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.SYRIA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.LEBANON, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.JERUSALEM, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.ANTIOCHIA, ProvinceType.HISTORICAL),
                    (Civ.BYZANTIUM, Province.CILICIA, ProvinceType.HISTORICAL),
                    (Civ.BYZANTIUM, Province.CHARSIANON, ProvinceType.HISTORICAL),
                    (Civ.BYZANTIUM, Province.COLONEA, ProvinceType.HISTORICAL),
                ]
            },
            do_not_cast=True,
        ),
        Civ.BULGARIA: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.BYZANTIUM, Province.SERBIA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.MOESIA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.THRACE, ProvinceType.HISTORICAL),
                ]
            },
            do_not_cast=True,
        ),
        Civ.CORDOBA: EnumDataMapper(
            {
                ProvinceEvent.ON_RESPAWN: [(province, ProvinceType.NONE) for province in Province]
                + [
                    (Province.IFRIQIYA, ProvinceType.CORE),
                    (Province.ALGIERS, ProvinceType.HISTORICAL),
                    (Province.ORAN, ProvinceType.CONTESTED),
                    (Province.TRIPOLITANIA, ProvinceType.CONTESTED),
                    (Province.TETOUAN, ProvinceType.CONTESTED),
                    (Province.MOROCCO, ProvinceType.CONTESTED),
                    (Province.FEZ, ProvinceType.CONTESTED),
                ],
            },
            do_not_cast=True,
        ),
        Civ.VENECIA: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.BYZANTIUM, Province.DALMATIA, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.BOSNIA, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.SLAVONIA, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.VERONA, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.TUSCANY, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.LOMBARDY, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.LIGURIA, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.CORSICA, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.SARDINIA, ProvinceType.NONE),
                    (Civ.BYZANTIUM, Province.LATIUM, ProvinceType.NONE),
                ]
            },
            do_not_cast=True,
        ),
        Civ.BURGUNDY: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.FRANCE, Province.PROVENCE, ProvinceType.POTENTIAL),
                    (Civ.FRANCE, Province.BURGUNDY, ProvinceType.POTENTIAL),
                ]
            },
            do_not_cast=True,
        ),
        Civ.GERMANY: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.FRANCE, Province.LORRAINE, ProvinceType.CONTESTED),
                    (Civ.FRANCE, Province.BAVARIA, ProvinceType.NONE),
                    (Civ.FRANCE, Province.FRANCONIA, ProvinceType.NONE),
                    (Civ.FRANCE, Province.SAXONY, ProvinceType.NONE),
                    (Civ.FRANCE, Province.NETHERLANDS, ProvinceType.NONE),
                ]
            },
            do_not_cast=True,
        ),
        Civ.NORWAY: EnumDataMapper(
            {
                ProvinceEvent.ON_DATETURN: {
                    # Provinces switch back to unstable after the fall of the Norman Kingdom of Sicily
                    DateTurn.i1194AD
                    + 1: [
                        (Province.APULIA, ProvinceType.NONE),
                        (Province.CALABRIA, ProvinceType.NONE),
                        (Province.SICILY, ProvinceType.NONE),
                        (Province.MALTA, ProvinceType.NONE),
                    ]
                }
            },
            do_not_cast=True,
        ),
        Civ.HUNGARY: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.BULGARIA, Province.BANAT, ProvinceType.NONE),
                    (Civ.BULGARIA, Province.WALLACHIA, ProvinceType.CONTESTED),
                ]
            },
            do_not_cast=True,
        ),
        Civ.CASTILE: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.CORDOBA, Province.LA_MANCHA, ProvinceType.HISTORICAL),
                ]
            },
            do_not_cast=True,
        ),
        Civ.DENMARK: EnumDataMapper(
            {
                ProvinceEvent.ON_DATETURN: {
                    # Provinces switch back to unstable after the fall of the Norman Kingdom of Sicily
                    DateTurn.i1194AD
                    + 1: [
                        (Province.APULIA, ProvinceType.NONE),
                        (Province.CALABRIA, ProvinceType.NONE),
                        (Province.SICILY, ProvinceType.NONE),
                        (Province.MALTA, ProvinceType.NONE),
                    ]
                }
            },
            do_not_cast=True,
        ),
        Civ.MOROCCO: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.CORDOBA, Province.MOROCCO, ProvinceType.NONE),
                    (Civ.CORDOBA, Province.MARRAKESH, ProvinceType.NONE),
                    (Civ.CORDOBA, Province.FEZ, ProvinceType.CONTESTED),
                    (Civ.CORDOBA, Province.TETOUAN, ProvinceType.CONTESTED),
                ]
            },
            do_not_cast=True,
        ),
        Civ.ENGLAND: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.FRANCE, Province.NORMANDY, ProvinceType.POTENTIAL),
                    (Civ.SCOTLAND, Province.NORTHUMBRIA, ProvinceType.CONTESTED),
                    (Civ.SCOTLAND, Province.MERCIA, ProvinceType.NONE),
                    (Civ.DENMARK, Province.NORTHUMBRIA, ProvinceType.NONE),
                    (Civ.DENMARK, Province.MERCIA, ProvinceType.NONE),
                    (Civ.DENMARK, Province.EAST_ANGLIA, ProvinceType.NONE),
                    (Civ.DENMARK, Province.LONDON, ProvinceType.NONE),
                ]
            },
            do_not_cast=True,
        ),
        Civ.ARAGON: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.BYZANTIUM, Province.APULIA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.CALABRIA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.SICILY, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.MALTA, ProvinceType.CONTESTED),
                    (Civ.CORDOBA, Province.ARAGON, ProvinceType.CONTESTED),
                    (Civ.CORDOBA, Province.CATALONIA, ProvinceType.CONTESTED),
                    (Civ.CORDOBA, Province.VALENCIA, ProvinceType.HISTORICAL),
                    (Civ.CORDOBA, Province.BALEARS, ProvinceType.CONTESTED),
                ]
            },
            do_not_cast=True,
        ),
        Civ.SWEDEN: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.NORWAY, Province.SVEALAND, ProvinceType.NONE),
                    (Civ.DENMARK, Province.GOTALAND, ProvinceType.NONE),
                    (Civ.DENMARK, Province.SVEALAND, ProvinceType.NONE),
                    (Civ.NOVGOROD, Province.OSTERLAND, ProvinceType.CONTESTED),
                ]
            },
            do_not_cast=True,
        ),
        Civ.PRUSSIA: EnumDataMapper(
            {
                ProvinceEvent.ON_DATETURN: DataMapper(
                    {
                        DateTurn.i1618AD: [
                            (Province.ESTONIA, ProvinceType.NONE),
                            (Province.LITHUANIA, ProvinceType.NONE),
                            (Province.SUVALKIJA, ProvinceType.NONE),
                            (Province.LIVONIA, ProvinceType.CONTESTED),
                            (Province.POMERANIA, ProvinceType.HISTORICAL),
                            (Province.BRANDENBURG, ProvinceType.HISTORICAL),
                            (Province.SILESIA, ProvinceType.POTENTIAL),
                            (Province.GREATER_POLAND, ProvinceType.CONTESTED),
                        ]
                    }
                ),
            },
            do_not_cast=True,
        ),
        Civ.AUSTRIA: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.HUNGARY, Province.CARINTHIA, ProvinceType.CONTESTED),
                    (Civ.HUNGARY, Province.AUSTRIA, ProvinceType.CONTESTED),
                    (Civ.HUNGARY, Province.MORAVIA, ProvinceType.CONTESTED),
                    (Civ.HUNGARY, Province.BAVARIA, ProvinceType.NONE),
                    (Civ.GERMANY, Province.BAVARIA, ProvinceType.CONTESTED),
                    (Civ.GERMANY, Province.BOHEMIA, ProvinceType.CONTESTED),
                    (Civ.CASTILE, Province.NETHERLANDS, ProvinceType.CONTESTED),
                    (Civ.CASTILE, Province.FLANDERS, ProvinceType.CONTESTED),
                ]
            },
            do_not_cast=True,
        ),
        Civ.OTTOMAN: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.BYZANTIUM, Province.ANTIOCHIA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.CILICIA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.CHARSIANON, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.COLONEA, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.ARMENIAKON, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.CYPRUS, ProvinceType.CONTESTED),
                    (Civ.BYZANTIUM, Province.ANATOLIKON, ProvinceType.HISTORICAL),
                    (Civ.BYZANTIUM, Province.OPSIKION, ProvinceType.HISTORICAL),
                    (Civ.BYZANTIUM, Province.THRAKESION, ProvinceType.HISTORICAL),
                    (Civ.BYZANTIUM, Province.PAPHLAGONIA, ProvinceType.HISTORICAL),
                    (Civ.HUNGARY, Province.DALMATIA, ProvinceType.CONTESTED),
                    (Civ.HUNGARY, Province.BOSNIA, ProvinceType.CONTESTED),
                    (Civ.HUNGARY, Province.BANAT, ProvinceType.CONTESTED),
                ]
            },
            do_not_cast=True,
        ),
        Civ.MOSCOW: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.NOVGOROD, Province.ROSTOV, ProvinceType.CONTESTED),
                    (Civ.NOVGOROD, Province.SMOLENSK, ProvinceType.NONE),
                ]
            },
            do_not_cast=True,
        ),
        Civ.DUTCH: EnumDataMapper(
            {
                ProvinceEvent.ON_SPAWN: [
                    (Civ.CASTILE, Province.NETHERLANDS, ProvinceType.NONE),
                    (Civ.CASTILE, Province.FLANDERS, ProvinceType.NONE),
                    (Civ.AUSTRIA, Province.NETHERLANDS, ProvinceType.NONE),
                    (Civ.AUSTRIA, Province.FLANDERS, ProvinceType.NONE),
                ]
            },
            do_not_cast=True,
        ),
    },
).fill_missing_members(EnumDataMapper({}))

CIV_VISIBLE_AREA_500AD = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: [
                {
                    Area.TILE_MIN: (64, 0),
                    Area.TILE_MAX: (99, 34),
                },
                {
                    Area.TILE_MIN: (49, 1),
                    Area.TILE_MAX: (63, 38),
                },
                {
                    Area.TILE_MIN: (24, 13),
                    Area.TILE_MAX: (48, 36),
                },
            ],
            Civ.FRANCE: [
                {
                    Area.TILE_MIN: (35, 31),
                    Area.TILE_MAX: (52, 51),
                },
                {
                    Area.TILE_MIN: (49, 26),
                    Area.TILE_MAX: (59, 38),
                },
            ],
            Civ.ARABIA: [
                {
                    Area.TILE_MIN: (79, 0),
                    Area.TILE_MAX: (89, 6),
                },
                {
                    Area.TILE_MIN: (90, 0),
                    Area.TILE_MAX: (99, 22),
                },
            ],
            Civ.BULGARIA: [
                {
                    Area.TILE_MIN: (69, 23),
                    Area.TILE_MAX: (81, 32),
                },
                {
                    Area.TILE_MIN: (78, 31),
                    Area.TILE_MAX: (99, 41),
                },
            ],
            Civ.CORDOBA: [
                {
                    Area.TILE_MIN: (18, 13),
                    Area.TILE_MAX: (39, 33),
                },
                {
                    Area.TILE_MIN: (40, 0),
                    Area.TILE_MAX: (59, 20),
                },
                {
                    Area.TILE_MIN: (60, 0),
                    Area.TILE_MAX: (95, 7),
                },
            ],
            Civ.VENECIA: [
                {
                    Area.TILE_MIN: (47, 14),
                    Area.TILE_MAX: (59, 38),
                },
                {
                    Area.TILE_MIN: (60, 18),
                    Area.TILE_MAX: (63, 35),
                },
                {
                    Area.TILE_MIN: (64, 18),
                    Area.TILE_MAX: (68, 29),
                },
            ],
            Civ.BURGUNDY: [
                {
                    Area.TILE_MIN: (43, 31),
                    Area.TILE_MAX: (53, 53),
                },
            ],
            Civ.GERMANY: [
                {
                    Area.TILE_MIN: (44, 31),
                    Area.TILE_MAX: (46, 52),
                },
                {
                    Area.TILE_MIN: (47, 27),
                    Area.TILE_MAX: (61, 55),
                },
                {
                    Area.TILE_MIN: (62, 50),
                    Area.TILE_MAX: (70, 55),
                },
            ],
            Civ.NOVGOROD: [
                {
                    Area.TILE_MIN: (72, 55),
                    Area.TILE_MAX: (90, 72),
                },
                {
                    Area.TILE_MIN: (79, 41),
                    Area.TILE_MAX: (88, 54),
                },
            ],
            Civ.NORWAY: [
                {
                    Area.TILE_MIN: (49, 52),
                    Area.TILE_MAX: (71, 72),
                },
                {
                    Area.TILE_MIN: (30, 56),
                    Area.TILE_MAX: (48, 72),
                },
            ],
            Civ.KIEV: [
                {
                    Area.TILE_MIN: (77, 24),
                    Area.TILE_MAX: (82, 40),
                },
                {
                    Area.TILE_MIN: (83, 33),
                    Area.TILE_MAX: (88, 46),
                },
                {
                    Area.TILE_MIN: (77, 39),
                    Area.TILE_MAX: (91, 56),
                },
            ],
            Civ.HUNGARY: [
                {
                    Area.TILE_MIN: (59, 30),
                    Area.TILE_MAX: (82, 42),
                },
                {
                    Area.TILE_MIN: (83, 36),
                    Area.TILE_MAX: (92, 42),
                },
            ],
            Civ.CASTILE: [
                {
                    Area.TILE_MIN: (22, 25),
                    Area.TILE_MAX: (35, 38),
                },
                {
                    Area.TILE_MIN: (36, 25),
                    Area.TILE_MAX: (43, 40),
                },
            ],
            Civ.DENMARK: [
                {
                    Area.TILE_MIN: (34, 46),
                    Area.TILE_MAX: (49, 72),
                },
                {
                    Area.TILE_MIN: (50, 50),
                    Area.TILE_MAX: (71, 72),
                },
                {
                    Area.TILE_MIN: (72, 57),
                    Area.TILE_MAX: (78, 64),
                },
            ],
            Civ.SCOTLAND: [
                {
                    Area.TILE_MIN: (30, 51),
                    Area.TILE_MAX: (46, 72),
                },
                {
                    Area.TILE_MIN: (35, 46),
                    Area.TILE_MAX: (46, 50),
                },
            ],
            Civ.POLAND: [
                {
                    Area.TILE_MIN: (60, 40),
                    Area.TILE_MAX: (74, 55),
                },
                {
                    Area.TILE_MIN: (75, 40),
                    Area.TILE_MAX: (79, 48),
                },
            ],
            Civ.GENOA: [
                {
                    Area.TILE_MIN: (39, 20),
                    Area.TILE_MAX: (60, 38),
                },
                {
                    Area.TILE_MIN: (47, 14),
                    Area.TILE_MAX: (63, 32),
                },
                {
                    Area.TILE_MIN: (64, 16),
                    Area.TILE_MAX: (67, 29),
                },
            ],
            Civ.MOROCCO: [
                {
                    Area.TILE_MIN: (12, 2),
                    Area.TILE_MAX: (42, 31),
                },
                {
                    Area.TILE_MIN: (43, 10),
                    Area.TILE_MAX: (53, 20),
                },
            ],
            Civ.ENGLAND: [
                {
                    Area.TILE_MIN: (31, 49),
                    Area.TILE_MAX: (45, 64),
                },
                {
                    Area.TILE_MIN: (37, 46),
                    Area.TILE_MAX: (45, 48),
                },
            ],
            Civ.PORTUGAL: [
                {
                    Area.TILE_MIN: (18, 22),
                    Area.TILE_MAX: (34, 39),
                },
            ],
            Civ.ARAGON: [
                {
                    Area.TILE_MIN: (19, 23),
                    Area.TILE_MAX: (56, 40),
                },
                {
                    Area.TILE_MIN: (25, 21),
                    Area.TILE_MAX: (45, 22),
                },
                {
                    Area.TILE_MIN: (46, 14),
                    Area.TILE_MAX: (63, 28),
                },
            ],
            Civ.SWEDEN: [
                {
                    Area.TILE_MIN: (39, 52),
                    Area.TILE_MAX: (82, 66),
                },
                {
                    Area.TILE_MIN: (34, 61),
                    Area.TILE_MAX: (71, 72),
                },
            ],
            Civ.PRUSSIA: [
                {
                    Area.TILE_MIN: (51, 43),
                    Area.TILE_MAX: (73, 56),
                },
                {
                    Area.TILE_MIN: (66, 57),
                    Area.TILE_MAX: (82, 62),
                },
                {
                    Area.TILE_MIN: (69, 63),
                    Area.TILE_MAX: (79, 66),
                },
            ],
            Civ.LITHUANIA: [
                {
                    Area.TILE_MIN: (67, 46),
                    Area.TILE_MAX: (76, 55),
                },
                {
                    Area.TILE_MIN: (73, 44),
                    Area.TILE_MAX: (81, 58),
                },
            ],
            Civ.AUSTRIA: [
                {
                    Area.TILE_MIN: (49, 27),
                    Area.TILE_MAX: (61, 55),
                },
                {
                    Area.TILE_MIN: (62, 34),
                    Area.TILE_MAX: (67, 46),
                },
            ],
            Civ.OTTOMAN: [
                {
                    Area.TILE_MIN: (75, 13),
                    Area.TILE_MAX: (99, 27),
                },
                {
                    Area.TILE_MIN: (92, 4),
                    Area.TILE_MAX: (99, 12),
                },
            ],
            Civ.MOSCOW: [
                {
                    Area.TILE_MIN: (77, 42),
                    Area.TILE_MAX: (99, 51),
                },
                {
                    Area.TILE_MIN: (74, 52),
                    Area.TILE_MAX: (99, 67),
                },
            ],
            Civ.DUTCH: [
                {
                    Area.TILE_MIN: (40, 45),
                    Area.TILE_MAX: (65, 57),
                },
                {
                    Area.TILE_MIN: (49, 58),
                    Area.TILE_MAX: (67, 66),
                },
                {
                    Area.TILE_MIN: (46, 39),
                    Area.TILE_MAX: (63, 44),
                },
            ],
            Civ.POPE: [
                {
                    Area.TILE_MIN: (39, 12),
                    Area.TILE_MAX: (73, 44),
                },
            ],
        }
    ).applymap(lambda d: parse_area_dict(d))
    # .applymap(
    #     lambda areas: (
    #         TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
    #         .rectangle(
    #             areas[Area.TILE_MIN],
    #             areas[Area.TILE_MAX],
    #         )
    #         .get_results()
    #     )
    # )
    # .apply(lambda tiles: concat_tiles(*tiles))
    # .apply(lambda tile: normalize_tiles(tile))
)

CIV_VISIBLE_AREA_1200AD = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: [
                {
                    Area.TILE_MIN: (64, 0),
                    Area.TILE_MAX: (99, 34),
                },
                {
                    Area.TILE_MIN: (49, 1),
                    Area.TILE_MAX: (63, 38),
                },
                {
                    Area.TILE_MIN: (24, 13),
                    Area.TILE_MAX: (48, 36),
                },
            ],
            Civ.FRANCE: [
                {
                    Area.TILE_MIN: (30, 26),
                    Area.TILE_MAX: (59, 54),
                },
                {
                    Area.TILE_MIN: (35, 55),
                    Area.TILE_MAX: (40, 70),
                },
            ],
            Civ.ARABIA: [
                {
                    Area.TILE_MIN: (26, 20),
                    Area.TILE_MAX: (35, 23),
                },
                {
                    Area.TILE_MIN: (22, 5),
                    Area.TILE_MAX: (27, 19),
                },
                {
                    Area.TILE_MIN: (28, 9),
                    Area.TILE_MAX: (53, 19),
                },
                {
                    Area.TILE_MIN: (47, 0),
                    Area.TILE_MAX: (85, 8),
                },
                {
                    Area.TILE_MIN: (86, 0),
                    Area.TILE_MAX: (99, 20),
                },
            ],
            Civ.BULGARIA: [
                {
                    Area.TILE_MIN: (65, 12),
                    Area.TILE_MAX: (83, 38),
                },
                {
                    Area.TILE_MIN: (78, 31),
                    Area.TILE_MAX: (99, 41),
                },
            ],
            Civ.CORDOBA: [
                {
                    Area.TILE_MIN: (18, 13),
                    Area.TILE_MAX: (39, 33),
                },
                {
                    Area.TILE_MIN: (40, 0),
                    Area.TILE_MAX: (59, 20),
                },
                {
                    Area.TILE_MIN: (60, 0),
                    Area.TILE_MAX: (95, 7),
                },
            ],
            Civ.VENECIA: [
                {
                    Area.TILE_MIN: (46, 14),
                    Area.TILE_MAX: (70, 41),
                },
                {
                    Area.TILE_MIN: (49, 7),
                    Area.TILE_MAX: (82, 25),
                },
                {
                    Area.TILE_MIN: (83, 7),
                    Area.TILE_MAX: (91, 13),
                },
            ],
            Civ.BURGUNDY: [
                {
                    Area.TILE_MIN: (43, 31),
                    Area.TILE_MAX: (53, 53),
                },
            ],
            Civ.GERMANY: [
                {
                    Area.TILE_MIN: (41, 31),
                    Area.TILE_MAX: (61, 58),
                },
                {
                    Area.TILE_MIN: (47, 27),
                    Area.TILE_MAX: (61, 30),
                },
                {
                    Area.TILE_MIN: (62, 34),
                    Area.TILE_MAX: (70, 55),
                },
                {
                    Area.TILE_MIN: (55, 22),
                    Area.TILE_MAX: (61, 26),
                },
            ],
            Civ.NOVGOROD: [
                {
                    Area.TILE_MIN: (72, 55),
                    Area.TILE_MAX: (90, 72),
                },
                {
                    Area.TILE_MIN: (79, 41),
                    Area.TILE_MAX: (88, 54),
                },
                {
                    Area.TILE_MIN: (91, 60),
                    Area.TILE_MAX: (99, 72),
                },
            ],
            Civ.NORWAY: [
                {
                    Area.TILE_MIN: (30, 52),
                    Area.TILE_MAX: (71, 72),
                },
                {
                    Area.TILE_MIN: (0, 67),
                    Area.TILE_MAX: (29, 72),
                },
            ],
            Civ.KIEV: [
                {
                    Area.TILE_MIN: (75, 42),
                    Area.TILE_MAX: (94, 62),
                },
                {
                    Area.TILE_MIN: (77, 31),
                    Area.TILE_MAX: (94, 41),
                },
                {
                    Area.TILE_MIN: (77, 24),
                    Area.TILE_MAX: (82, 40),
                },
            ],
            Civ.HUNGARY: [
                {
                    Area.TILE_MIN: (56, 27),
                    Area.TILE_MAX: (82, 45),
                },
                {
                    Area.TILE_MIN: (83, 31),
                    Area.TILE_MAX: (92, 42),
                },
                {
                    Area.TILE_MIN: (65, 12),
                    Area.TILE_MAX: (82, 26),
                },
            ],
            Civ.CASTILE: [
                {
                    Area.TILE_MIN: (20, 17),
                    Area.TILE_MAX: (56, 40),
                },
            ],
            Civ.DENMARK: [
                {
                    Area.TILE_MIN: (34, 46),
                    Area.TILE_MAX: (71, 72),
                },
                {
                    Area.TILE_MIN: (72, 57),
                    Area.TILE_MAX: (78, 72),
                },
            ],
            Civ.SCOTLAND: [
                {
                    Area.TILE_MIN: (30, 43),
                    Area.TILE_MAX: (46, 72),
                },
            ],
            Civ.POLAND: [
                {
                    Area.TILE_MIN: (60, 37),
                    Area.TILE_MAX: (79, 60),
                },
            ],
            Civ.GENOA: [
                {
                    Area.TILE_MIN: (39, 15),
                    Area.TILE_MAX: (60, 39),
                },
                {
                    Area.TILE_MIN: (47, 9),
                    Area.TILE_MAX: (82, 25),
                },
                {
                    Area.TILE_MIN: (61, 26),
                    Area.TILE_MAX: (67, 32),
                },
            ],
            Civ.MOROCCO: [
                {
                    Area.TILE_MIN: (12, 2),
                    Area.TILE_MAX: (42, 31),
                },
                {
                    Area.TILE_MIN: (43, 2),
                    Area.TILE_MAX: (53, 20),
                },
            ],
            Civ.ENGLAND: [
                {
                    Area.TILE_MIN: (26, 54),
                    Area.TILE_MAX: (46, 64),
                },
                {
                    Area.TILE_MIN: (31, 34),
                    Area.TILE_MAX: (46, 53),
                },
            ],
            Civ.PORTUGAL: [
                {
                    Area.TILE_MIN: (18, 17),
                    Area.TILE_MAX: (34, 39),
                },
            ],
            Civ.ARAGON: [
                {
                    Area.TILE_MIN: (19, 29),
                    Area.TILE_MAX: (56, 40),
                },
                {
                    Area.TILE_MIN: (19, 21),
                    Area.TILE_MAX: (34, 28),
                },
                {
                    Area.TILE_MIN: (35, 14),
                    Area.TILE_MAX: (63, 28),
                },
            ],
            Civ.SWEDEN: [
                {
                    Area.TILE_MIN: (39, 52),
                    Area.TILE_MAX: (82, 66),
                },
                {
                    Area.TILE_MIN: (34, 61),
                    Area.TILE_MAX: (71, 72),
                },
            ],
            Civ.PRUSSIA: [
                {
                    Area.TILE_MIN: (51, 43),
                    Area.TILE_MAX: (73, 56),
                },
                {
                    Area.TILE_MIN: (66, 57),
                    Area.TILE_MAX: (82, 62),
                },
                {
                    Area.TILE_MIN: (69, 63),
                    Area.TILE_MAX: (79, 66),
                },
            ],
            Civ.LITHUANIA: [
                {
                    Area.TILE_MIN: (67, 46),
                    Area.TILE_MAX: (76, 55),
                },
                {
                    Area.TILE_MIN: (73, 44),
                    Area.TILE_MAX: (81, 58),
                },
            ],
            Civ.AUSTRIA: [
                {
                    Area.TILE_MIN: (49, 27),
                    Area.TILE_MAX: (61, 55),
                },
                {
                    Area.TILE_MIN: (62, 34),
                    Area.TILE_MAX: (67, 46),
                },
            ],
            Civ.OTTOMAN: [
                {
                    Area.TILE_MIN: (75, 13),
                    Area.TILE_MAX: (99, 27),
                },
                {
                    Area.TILE_MIN: (92, 4),
                    Area.TILE_MAX: (99, 12),
                },
            ],
            Civ.MOSCOW: [
                {
                    Area.TILE_MIN: (77, 42),
                    Area.TILE_MAX: (99, 51),
                },
                {
                    Area.TILE_MIN: (74, 52),
                    Area.TILE_MAX: (99, 67),
                },
            ],
            Civ.DUTCH: [
                {
                    Area.TILE_MIN: (40, 45),
                    Area.TILE_MAX: (65, 57),
                },
                {
                    Area.TILE_MIN: (49, 58),
                    Area.TILE_MAX: (67, 66),
                },
                {
                    Area.TILE_MIN: (46, 39),
                    Area.TILE_MAX: (63, 44),
                },
            ],
            Civ.POPE: [
                {
                    Area.TILE_MIN: (39, 12),
                    Area.TILE_MAX: (73, 44),
                },
            ],
        }
    ).applymap(lambda d: parse_area_dict(d))
    # .applymap(
    #     lambda areas: (
    #         TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
    #         .rectangle(
    #             areas[Area.TILE_MIN],
    #             areas[Area.TILE_MAX],
    #         )
    #         .get_results()
    #     )
    # )
    # .apply(lambda tiles: concat_tiles(*tiles))
    # .apply(lambda tile: normalize_tiles(tile))
)

CIV_VISIBLE_AREA = ScenarioDataMapper(
    {
        Scenario.i500AD: CIV_VISIBLE_AREA_500AD,
        Scenario.i1200AD: CIV_VISIBLE_AREA_1200AD,
    }
)

# Used for Congresses and Victory
CIV_GROUPS = EnumDataMapper(
    {
        CivGroup.EASTERN: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.NOVGOROD,
            Civ.KIEV,
            Civ.LITHUANIA,
            Civ.MOSCOW,
        ],
        CivGroup.CENTRAL: [
            Civ.BURGUNDY,
            Civ.HUNGARY,
            Civ.GERMANY,
            Civ.POLAND,
            Civ.PRUSSIA,
            Civ.AUSTRIA,
        ],
        CivGroup.ATLANTIC: [
            Civ.FRANCE,
            Civ.CASTILE,
            Civ.ENGLAND,
            Civ.PORTUGAL,
            Civ.DUTCH,
            Civ.ARAGON,
            Civ.SCOTLAND,
        ],
        CivGroup.ISLAMIC: [
            Civ.ARABIA,
            Civ.CORDOBA,
            Civ.MOROCCO,
            Civ.OTTOMAN,
        ],
        CivGroup.ITALIAN: [
            Civ.GENOA,
            Civ.VENECIA,
            Civ.POPE,
        ],
        CivGroup.SCANDINAVIAN: [
            Civ.NORWAY,
            Civ.DENMARK,
            Civ.SWEDEN,
        ],
    }
)
