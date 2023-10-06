# coding: utf-8

from CoreTypes import (
    AreaTypes,
    City,
    Civ,
    CivGroup,
    Colony,
    Company,
    Province,
    Region,
    Scenario,
    Lake,
    Area,
)
from BaseStructures import EnumDataMapper
from CoreStructures import (
    CompanyDataMapper,
    ScenarioDataMapper,
    Tile,
    CivDataMapper,
    TilesFactory,
    concat_tiles,
    parse_area_dict,
)
from MiscData import WORLD_HEIGHT, WORLD_WIDTH


CITIES = EnumDataMapper(
    {
        City.JERUSALEM: (93, 5),
    }
).apply(lambda x: Tile(x))

REGIONS = EnumDataMapper(
    {
        Region.IBERIA: [
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
        ],
        Region.FRANCE: [
            Province.NORMANDY,
            Province.BRETAGNE,
            Province.ILE_DE_FRANCE,
            Province.ORLEANS,
            Province.PICARDY,
        ],
        Region.BURGUNDY: [
            Province.PROVENCE,
            Province.BURGUNDY,
            Province.CHAMPAGNE,
            Province.FLANDERS,
        ],
        Region.BRITAIN: [
            Province.LONDON,
            Province.WALES,
            Province.WESSEX,
            Province.SCOTLAND,
            Province.EAST_ANGLIA,
            Province.MERCIA,
        ],
        Region.SCANDINAVIA: [
            Province.DENMARK,
            Province.OSTERLAND,
            Province.NORWAY,
            Province.VESTFOLD,
            Province.GOTALAND,
            Province.SVEALAND,
            Province.NORRLAND,
            Province.JAMTLAND,
            Province.SKANELAND,
            Province.GOTLAND,
        ],
        Region.GERMANY: [
            Province.LORRAINE,
            Province.SWABIA,
            Province.SAXONY,
            Province.BAVARIA,
            Province.FRANCONIA,
            Province.BRANDENBURG,
            Province.HOLSTEIN,
        ],
        Region.POLAND: [
            Province.POMERANIA,
            Province.GALICJA,
            Province.GREATER_POLAND,
            Province.LESSER_POLAND,
            Province.SILESIA,
            Province.MASOVIA,
        ],
        Region.LITHUANIA: [
            Province.LITHUANIA,
            Province.LIVONIA,
            Province.ESTONIA,
        ],
        Region.AUSTRIA: [
            Province.CARINTHIA,
            Province.AUSTRIA,
            Province.MORAVIA,
            Province.BOHEMIA,
            Province.SILESIA,
        ],
        Region.HUNGARY: [
            Province.TRANSYLVANIA,
            Province.HUNGARY,
            Province.SLAVONIA,
            Province.PANNONIA,
            Province.UPPER_HUNGARY,
        ],
        Region.BALKANS: [
            Province.SERBIA,
            Province.THRACE,
            Province.MACEDONIA,
            Province.MOESIA,
            Province.ARBERIA,
            Province.DALMATIA,
            Province.BOSNIA,
            Province.BANAT,
        ],
        Region.GREECE: [
            Province.CONSTANTINOPLE,
            Province.THESSALY,
            Province.EPIRUS,
            Province.MOREA,
            Province.THESSALONIKI,
        ],
        Region.ASIA_MINOR: [
            Province.COLONEA,
            Province.CHARSIANON,
            Province.CILICIA,
            Province.ARMENIAKON,
            Province.ANATOLIKON,
            Province.PAPHLAGONIA,
            Province.THRAKESION,
            Province.OPSIKION,
        ],
        Region.MIDDLE_EAST: [
            Province.ANTIOCHIA,
            Province.SYRIA,
            Province.LEBANON,
            Province.ARABIA,
            Province.JERUSALEM,
        ],
        Region.AFRICA: [
            Province.ORAN,
            Province.ALGIERS,
            Province.IFRIQIYA,
            Province.CYRENAICA,
            Province.TRIPOLITANIA,
            Province.TETOUAN,
            Province.MOROCCO,
            Province.MARRAKESH,
            Province.FEZ,
        ],
        Region.KIEV: [
            Province.MOLDOVA,
            Province.KIEV,
            Province.CRIMEA,
            Province.ZAPORIZHIA,
            Province.SLOBODA,
            Province.PEREYASLAVL,
            Province.CHERNIGOV,
            Province.PODOLIA,
            Province.MINSK,
        ],
        Region.ITALY: [
            Province.LOMBARDY,
            Province.LIGURIA,
            Province.VERONA,
            Province.TUSCANY,
            Province.LATIUM,
            Province.CALABRIA,
            Province.APULIA,
            Province.ARBERIA,
            Province.MALTA,
            Province.DALMATIA,
        ],
        Region.SWISS: [
            Province.BAVARIA,
            Province.AUSTRIA,
            Province.SWABIA,
            Province.BURGUNDY,
            Province.LORRAINE,
            Province.CHAMPAGNE,
            Province.PROVENCE,
            Province.LOMBARDY,
            Province.LIGURIA,
            Province.VERONA,
            Province.FRANCONIA,
            Province.BOHEMIA,
        ],
        Region.NOT_EUROPE: [
            Province.ORAN,
            Province.ALGIERS,
            Province.IFRIQIYA,
            Province.CYRENAICA,
            Province.TRIPOLITANIA,
            Province.TETOUAN,
            Province.MOROCCO,
            Province.MARRAKESH,
            Province.FEZ,
            Province.SAHARA,
            Province.EGYPT,
            Province.ANTIOCHIA,
            Province.SYRIA,
            Province.LEBANON,
            Province.ARABIA,
            Province.JERUSALEM,
            Province.COLONEA,
            Province.CHARSIANON,
            Province.CILICIA,
            Province.ARMENIAKON,
            Province.ANATOLIKON,
            Province.PAPHLAGONIA,
            Province.THRAKESION,
            Province.OPSIKION,
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

CIV_CAPITAL_LOCATIONS = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: (81, 24),  # Constantinople
            Civ.FRANCE: (44, 46),  # Paris
            Civ.ARABIA: (97, 10),  # Damascus
            Civ.BULGARIA: (78, 29),  # Preslav
            Civ.CORDOBA: (30, 23),  # Cordoba
            Civ.VENECIA: (56, 35),  # Venice
            Civ.BURGUNDY: (47, 41),  # Dijon
            Civ.GERMANY: (53, 46),  # Frankfurt
            Civ.NOVGOROD: (80, 62),  # Novgorod
            Civ.NORWAY: (57, 65),  # Tonsberg
            Civ.KIEV: (83, 45),  # Kiev
            Civ.HUNGARY: (66, 37),  # Buda
            Civ.CASTILLE: (27, 32),  # Leon
            Civ.DENMARK: (59, 57),  # Roskilde / Kobenhavn
            Civ.SCOTLAND: (37, 63),  # Edinburgh
            Civ.POLAND: (65, 49),  # Poznan
            Civ.GENOA: (50, 34),  # Genoa
            Civ.MOROCCO: (24, 7),  # Marrakesh
            Civ.ENGLAND: (41, 52),  # London
            Civ.PORTUGAL: (21, 25),  # Lisboa
            Civ.ARAGON: (36, 29),  # Zaragoza
            Civ.SWEDEN: (66, 64),  # Stockholm
            Civ.PRUSSIA: (69, 53),  # Königsberg
            Civ.LITHUANIA: (75, 53),  # Vilnus
            Civ.AUSTRIA: (62, 40),  # Wien
            Civ.OTTOMAN: (78, 22),  # Gallipoli
            Civ.MOSCOW: (91, 56),  # Moscow
            Civ.DUTCH: (49, 52),  # Amsterdam
            Civ.POPE: (56, 27),  # Rome
        }
    )
    .apply(lambda x: Tile(x))
    .fill_missing_members(None)
)

# Used for respawning
CIV_NEW_CAPITAL_LOCATIONS = (
    CivDataMapper(
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
            Civ.CASTILLE: [
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
    )
    .applymap(lambda x: Tile(x))
    .fill_missing_members(None)
)

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
            Civ.CASTILLE,
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
        Civ.CASTILLE: [
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
            Civ.CASTILLE,
            Civ.PORTUGAL,
            Civ.CORDOBA,
        ],
        Civ.ENGLAND: [
            Civ.FRANCE,
            Civ.DUTCH,
            Civ.SCOTLAND,
        ],
        Civ.PORTUGAL: [
            Civ.CASTILLE,
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
            Civ.CASTILLE,
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
).fill_missing_members(None)

# Used for stability on spawn
CIV_OLDER_NEIGHBOURS = CivDataMapper(
    {
        Civ.ARABIA: [Civ.BYZANTIUM],
        Civ.BULGARIA: [Civ.BYZANTIUM],
        Civ.KIEV: [Civ.BULGARIA],
        Civ.HUNGARY: [Civ.BULGARIA],
        Civ.CASTILLE: [Civ.CORDOBA],
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
            Civ.CASTILLE,
            Civ.CORDOBA,
        ],
        Civ.ARAGON: [Civ.CASTILLE],
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
).fill_missing_members(None)

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
        Civ.CASTILLE: (460, 180),
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
            Civ.CASTILLE: {
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
    )
    .apply(lambda d: parse_area_dict(d))
    .apply(
        lambda area: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                area[Area.TILE_MIN],
                area[Area.TILE_MAX],
            )
            .extend(area.get(Area.ADDITIONAL_TILES))
            .substract(area.get(Area.EXCEPTION_TILES))
            .attach_area(AreaTypes.CORE)
            .normalize()
            .get_results()
        )
    )
    .fill_missing_members(None)
)

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
            Civ.CASTILLE: {
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
    )
    .apply(lambda d: parse_area_dict(d))
    .apply(
        lambda area: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                area[Area.TILE_MIN],
                area[Area.TILE_MAX],
            )
            .extend(area.get(Area.ADDITIONAL_TILES))
            .substract(area.get(Area.EXCEPTION_TILES))
            .attach_area(AreaTypes.NORMAL)
            .normalize()
            .get_results()
        )
    )
    .fill_missing_members(None)
)

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
            Civ.CASTILLE: {
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
    )
    .apply(lambda d: parse_area_dict(d))
    .apply(
        lambda area: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                area[Area.TILE_MIN],
                area[Area.TILE_MAX],
            )
            .extend(area.get(Area.ADDITIONAL_TILES))
            .substract(area.get(Area.EXCEPTION_TILES))
            .attach_area(AreaTypes.BROADER)
            .normalize()
            .get_results()
        )
    )
    .fill_missing_members(None)
)

CIV_AREAS = CivDataMapper(
    dict(
        (
            civ,
            {
                AreaTypes.CORE: CIV_CORE_AREA[civ],
                AreaTypes.NORMAL: CIV_NORMAL_AREA[civ],
                AreaTypes.BROADER: CIV_BROADER_AREA[civ],
            },
        )
        for civ in Civ
    )
)

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
            Civ.CASTILLE: [
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
    )
    .applymap(lambda d: parse_area_dict(d))
    .applymap(
        lambda areas: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                areas[Area.TILE_MIN],
                areas[Area.TILE_MAX],
            )
            .get_results()
        )
    )
    .apply(lambda tiles: concat_tiles(*tiles))
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
            Civ.CASTILLE: [
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
    )
    .applymap(lambda d: parse_area_dict(d))
    .applymap(
        lambda areas: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                areas[Area.TILE_MIN],
                areas[Area.TILE_MAX],
            )
            .get_results()
        )
    )
    .apply(lambda tiles: concat_tiles(*tiles))
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
            Civ.CASTILLE,
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
