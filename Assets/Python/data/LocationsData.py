# coding: utf-8

from CoreTypes import (
    AreaTypes,
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
from CoreStructures import ScenarioDataMapper, Tile, CivDataMapper, TilesFactory, merge_tiles
from MiscData import WORLD_WIDTH, WORLD_HEIGHT


JERUSALEM = Tile((93, 5))


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

COMPANY_REGION = EnumDataMapper(
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
        Lake.LOUGH_NEAGH: [Tile((32, 61))],
        Lake.LAKE_BALATON: [Tile((64, 36))],
        Lake.DEAD_SEA: [
            Tile((94, 4)),
            Tile((94, 5)),
        ],
        Lake.SEA_OF_GALILEE: [Tile((95, 8))],
        Lake.LAKE_TUZ: [
            Tile((88, 19)),
            Tile((89, 19)),
        ],
        Lake.LAKE_EGIRDIR: [Tile((85, 18))],
        Lake.LAKE_BEYSEHIR: [Tile((86, 17))],
        Lake.LAKE_GARDA: [Tile((54, 37))],
        Lake.LAKE_GENEVA: [Tile((49, 39))],
        Lake.LAKE_CONSTANCE: [Tile((53, 40))],
        Lake.LAKE_SKADAR: [Tile((66, 27))],
        Lake.LAKE_OHRID: [Tile((69, 23))],
        Lake.LAKE_SNIARDWY: [Tile((71, 52))],
        Lake.LAKE_VATTERN: [
            Tile((62, 62)),
            Tile((62, 63)),
        ],
        Lake.LAKE_VANERN: [
            Tile((60, 64)),
            Tile((61, 64)),
            Tile((61, 65)),
        ],
        Lake.LAKE_MALAREN: [
            Tile((64, 64)),
            Tile((65, 64)),
        ],
        Lake.LAKE_STORSJON: [Tile((62, 71))],
        Lake.LAKE_PEIPUS: [
            Tile((77, 60)),
            Tile((77, 61)),
            Tile((77, 62)),
        ],
        Lake.LAKE_ILMEN: [Tile((80, 61))],
        Lake.LAKE_LADOGA: [
            Tile((79, 67)),
            Tile((79, 68)),
            Tile((80, 65)),
            Tile((80, 66)),
            Tile((80, 67)),
            Tile((80, 68)),
            Tile((80, 69)),
            Tile((81, 66)),
            Tile((81, 67)),
            Tile((81, 68)),
        ],
        Lake.LAKE_ONEGA: [
            Tile((84, 69)),
            Tile((84, 70)),
            Tile((85, 68)),
            Tile((85, 69)),
            Tile((85, 70)),
        ],
        Lake.LAKE_BELOYE: [Tile((87, 66))],
        Lake.LAKE_SAIMAA: [
            Tile((77, 68)),
            Tile((77, 69)),
            Tile((78, 70)),
        ],
        Lake.LAKE_PAIJANNE: [
            Tile((74, 68)),
            Tile((74, 69)),
        ],
        Lake.LAKE_VYGOZERO: [Tile((85, 72))],
        Lake.LAKE_SEGOZERO: [Tile((83, 72))],
        Lake.LAKE_KALLAVESI: [Tile((76, 71))],
        Lake.LAKE_KEITELE: [Tile((74, 71))],
        Lake.LAKE_PIELINEN: [Tile((78, 72))],
        Lake.LAKE_NASIJARVI: [Tile((72, 68))],
        Lake.LIMFJORDEN: [Tile((55, 59))],
        Lake.TRONDHEIMFJORDEN: [Tile((58, 71))],
    }
)

CIV_CAPITAL_LOCATIONS = CivDataMapper(
    {
        Civ.BYZANTIUM: Tile((81, 24)),  # Constantinople
        Civ.FRANCE: Tile((44, 46)),  # Paris
        Civ.ARABIA: Tile((97, 10)),  # Damascus
        Civ.BULGARIA: Tile((78, 29)),  # Preslav
        Civ.CORDOBA: Tile((30, 23)),  # Cordoba
        Civ.VENECIA: Tile((56, 35)),  # Venice
        Civ.BURGUNDY: Tile((47, 41)),  # Dijon
        Civ.GERMANY: Tile((53, 46)),  # Frankfurt
        Civ.NOVGOROD: Tile((80, 62)),  # Novgorod
        Civ.NORWAY: Tile((57, 65)),  # Tonsberg
        Civ.KIEV: Tile((83, 45)),  # Kiev
        Civ.HUNGARY: Tile((66, 37)),  # Buda
        Civ.CASTILLE: Tile((27, 32)),  # Leon
        Civ.DENMARK: Tile((59, 57)),  # Roskilde / Kobenhavn
        Civ.SCOTLAND: Tile((37, 63)),  # Edinburgh
        Civ.POLAND: Tile((65, 49)),  # Poznan
        Civ.GENOA: Tile((50, 34)),  # Genoa
        Civ.MOROCCO: Tile((24, 7)),  # Marrakesh
        Civ.ENGLAND: Tile((41, 52)),  # London
        Civ.PORTUGAL: Tile((21, 25)),  # Lisboa
        Civ.ARAGON: Tile((36, 29)),  # Zaragoza
        Civ.SWEDEN: Tile((66, 64)),  # Stockholm
        Civ.PRUSSIA: Tile((69, 53)),  # Königsberg
        Civ.LITHUANIA: Tile((75, 53)),  # Vilnus
        Civ.AUSTRIA: Tile((62, 40)),  # Wien
        Civ.OTTOMAN: Tile((78, 22)),  # Gallipoli
        Civ.MOSCOW: Tile((91, 56)),  # Moscow
        Civ.DUTCH: Tile((49, 52)),  # Amsterdam
        Civ.POPE: Tile((56, 27)),  # Rome
    }
).fill_missing_members(None)

# Used for respawning
CIV_NEW_CAPITAL_LOCATIONS = CivDataMapper(
    {
        Civ.ARABIA: [
            Tile((83, 3)),
            Tile((84, 3)),
            Tile((84, 4)),
        ],  # Alexandria
        Civ.CORDOBA: [
            Tile((48, 16)),
            Tile((50, 18)),
        ],  # Tunis
        Civ.GERMANY: [Tile((57, 41))],  # Munich
        Civ.NORWAY: [Tile((59, 64))],  # Oslo
        Civ.KIEV: [Tile((88, 40))],  # Stara Sich
        Civ.CASTILLE: [
            Tile((30, 27)),
            Tile((31, 27)),
            Tile((31, 28)),
            Tile((32, 28)),
        ],  # Toledo or Madrid
        Civ.MOROCCO: [Tile((25, 13))],  # Rabat
        Civ.ARAGON: [Tile((59, 24))],  # Naples
        Civ.PRUSSIA: [
            Tile((60, 48)),
            Tile((61, 48)),
            Tile((61, 49)),
            Tile((62, 48)),
        ],  # Berlin
    }
).fill_missing_members(None)

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
).fill_missing_members(None)

CIV_CORE_AREA = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: {
                Area.TILE_MIN: Tile((66, 14)),
                Area.TILE_MAX: Tile((84, 26)),
            },
            Civ.FRANCE: {
                Area.TILE_MIN: Tile((42, 43)),
                Area.TILE_MAX: Tile((46, 48)),
            },
            Civ.ARABIA: {
                Area.TILE_MIN: Tile((92, 0)),
                Area.TILE_MAX: Tile((99, 12)),
            },
            Civ.BULGARIA: {
                Area.TILE_MIN: Tile((74, 27)),
                Area.TILE_MAX: Tile((80, 30)),
            },
            Civ.CORDOBA: {
                Area.TILE_MIN: Tile((24, 19)),
                Area.TILE_MAX: Tile((37, 28)),
                Area.ADDITIONAL_TILES: [
                    Tile((26, 15)),
                    Tile((26, 16)),
                    Tile((26, 17)),
                    Tile((26, 18)),
                    Tile((27, 15)),
                    Tile((27, 16)),
                    Tile((27, 17)),
                    Tile((27, 18)),
                    Tile((28, 15)),
                    Tile((28, 16)),
                    Tile((28, 17)),
                    Tile((28, 18)),
                    Tile((29, 15)),
                    Tile((29, 16)),
                    Tile((29, 17)),
                    Tile((29, 18)),
                ],
            },
            Civ.VENECIA: {
                Area.TILE_MIN: Tile((55, 33)),
                Area.TILE_MAX: Tile((59, 36)),
                Area.ADDITIONAL_TILES: [
                    Tile((60, 33)),
                    Tile((60, 34)),
                    Tile((60, 35)),
                ],
            },
            Civ.BURGUNDY: {
                Area.TILE_MIN: Tile((44, 32)),
                Area.TILE_MAX: Tile((48, 42)),
                Area.ADDITIONAL_TILES: [
                    Tile((49, 39)),
                    Tile((49, 40)),
                    Tile((49, 41)),
                    Tile((49, 42)),
                ],
            },
            Civ.GERMANY: {
                Area.TILE_MIN: Tile((51, 40)),
                Area.TILE_MAX: Tile((58, 50)),
            },
            Civ.NOVGOROD: {
                Area.TILE_MIN: Tile((79, 59)),
                Area.TILE_MAX: Tile((82, 69)),
                Area.ADDITIONAL_TILES: [
                    Tile((78, 59)),
                    Tile((78, 60)),
                ],
            },
            Civ.NORWAY: {
                Area.TILE_MIN: Tile((53, 63)),
                Area.TILE_MAX: Tile((59, 72)),
            },
            Civ.KIEV: {
                Area.TILE_MIN: Tile((79, 42)),
                Area.TILE_MAX: Tile((88, 50)),
            },
            Civ.HUNGARY: {
                Area.TILE_MIN: Tile((64, 33)),
                Area.TILE_MAX: Tile((73, 39)),
            },
            Civ.CASTILLE: {
                Area.TILE_MIN: Tile((25, 30)),
                Area.TILE_MAX: Tile((32, 36)),
            },
            Civ.DENMARK: {
                Area.TILE_MIN: Tile((54, 55)),
                Area.TILE_MAX: Tile((64, 61)),
            },
            Civ.SCOTLAND: {
                Area.TILE_MIN: Tile((35, 62)),
                Area.TILE_MAX: Tile((39, 68)),
                Area.ADDITIONAL_TILES: [
                    Tile((37, 69)),
                    Tile((38, 69)),
                ],
            },
            Civ.POLAND: {
                Area.TILE_MIN: Tile((64, 43)),
                Area.TILE_MAX: Tile((70, 50)),
                Area.ADDITIONAL_TILES: [
                    Tile((63, 46)),
                    Tile((63, 47)),
                    Tile((63, 48)),
                    Tile((63, 49)),
                    Tile((63, 50)),
                ],
            },
            Civ.GENOA: {
                Area.TILE_MIN: Tile((49, 27)),
                Area.TILE_MAX: Tile((52, 35)),
            },
            Civ.MOROCCO: {
                Area.TILE_MIN: Tile((18, 3)),
                Area.TILE_MAX: Tile((31, 16)),
            },
            Civ.ENGLAND: {
                Area.TILE_MIN: Tile((37, 48)),
                Area.TILE_MAX: Tile((43, 60)),
                Area.ADDITIONAL_TILES: [
                    Tile((37, 46)),
                    Tile((37, 47)),
                    Tile((38, 46)),
                    Tile((38, 47)),
                    Tile((39, 46)),
                    Tile((39, 47)),
                    Tile((40, 46)),
                    Tile((40, 47)),
                    Tile((41, 46)),
                    Tile((41, 47)),
                    Tile((42, 47)),
                ],
            },
            Civ.PORTUGAL: {
                Area.TILE_MIN: Tile((21, 24)),
                Area.TILE_MAX: Tile((24, 32)),
                Area.ADDITIONAL_TILES: [
                    Tile((25, 27)),
                    Tile((25, 28)),
                    Tile((25, 29)),
                    Tile((25, 30)),
                    Tile((25, 31)),
                ],
            },
            Civ.ARAGON: {
                Area.TILE_MIN: Tile((35, 26)),
                Area.TILE_MAX: Tile((42, 31)),
                Area.ADDITIONAL_TILES: [
                    Tile((40, 23)),
                    Tile((42, 23)),
                    Tile((42, 24)),
                    Tile((44, 24)),
                ],
            },
            Civ.SWEDEN: {
                Area.TILE_MIN: Tile((61, 60)),
                Area.TILE_MAX: Tile((65, 70)),
                Area.ADDITIONAL_TILES: [
                    Tile((60, 61)),
                    Tile((60, 62)),
                    Tile((60, 63)),
                    Tile((61, 71)),
                    Tile((62, 71)),
                    Tile((62, 72)),
                    Tile((63, 71)),
                    Tile((63, 72)),
                    Tile((64, 71)),
                    Tile((64, 72)),
                    Tile((65, 71)),
                    Tile((65, 72)),
                    Tile((66, 64)),
                    Tile((66, 65)),
                    Tile((66, 66)),
                    Tile((66, 72)),
                    Tile((68, 65)),
                    Tile((70, 67)),
                    Tile((70, 68)),
                    Tile((71, 66)),
                    Tile((71, 67)),
                    Tile((71, 68)),
                    Tile((72, 65)),
                    Tile((72, 66)),
                    Tile((72, 67)),
                ],
            },
            Civ.PRUSSIA: {
                Area.TILE_MIN: Tile((70, 52)),
                Area.TILE_MAX: Tile((71, 58)),
                Area.ADDITIONAL_TILES: [
                    Tile((68, 51)),
                    Tile((68, 52)),
                    Tile((68, 53)),
                    Tile((69, 51)),
                    Tile((69, 52)),
                    Tile((69, 53)),
                    Tile((70, 51)),
                    Tile((71, 59)),
                    Tile((72, 57)),
                    Tile((72, 58)),
                    Tile((73, 57)),
                    Tile((73, 58)),
                    Tile((74, 57)),
                    Tile((74, 58)),
                    Tile((74, 59)),
                    Tile((74, 60)),
                    Tile((75, 57)),
                    Tile((75, 58)),
                    Tile((75, 59)),
                    Tile((75, 60)),
                    Tile((76, 58)),
                    Tile((76, 59)),
                    Tile((76, 60)),
                ],
            },
            Civ.LITHUANIA: {
                Area.TILE_MIN: Tile((72, 51)),
                Area.TILE_MAX: Tile((80, 56)),
                Area.ADDITIONAL_TILES: [
                    Tile((76, 57)),
                    Tile((77, 57)),
                    Tile((78, 57)),
                    Tile((79, 57)),
                    Tile((80, 57)),
                ],
            },
            Civ.AUSTRIA: {
                Area.TILE_MIN: Tile((59, 37)),
                Area.TILE_MAX: Tile((62, 44)),
                Area.ADDITIONAL_TILES: [
                    Tile((60, 36)),
                    Tile((61, 36)),
                ],
            },
            Civ.OTTOMAN: {
                Area.TILE_MIN: Tile((76, 16)),
                Area.TILE_MAX: Tile((84, 22)),
                Area.ADDITIONAL_TILES: [
                    Tile((76, 23)),
                    Tile((77, 23)),
                    Tile((78, 23)),
                    Tile((79, 23)),
                ],
            },
            Civ.MOSCOW: {
                Area.TILE_MIN: Tile((84, 53)),
                Area.TILE_MAX: Tile((97, 59)),
                Area.ADDITIONAL_TILES: [
                    Tile((83, 53)),
                    Tile((83, 54)),
                    Tile((83, 55)),
                    Tile((83, 56)),
                    Tile((83, 57)),
                    Tile((87, 60)),
                    Tile((88, 60)),
                    Tile((89, 60)),
                    Tile((90, 60)),
                    Tile((91, 60)),
                    Tile((92, 60)),
                    Tile((93, 60)),
                    Tile((94, 60)),
                    Tile((95, 60)),
                    Tile((96, 60)),
                    Tile((97, 60)),
                    Tile((88, 61)),
                    Tile((89, 61)),
                    Tile((90, 61)),
                    Tile((91, 61)),
                    Tile((92, 61)),
                    Tile((93, 61)),
                    Tile((94, 61)),
                    Tile((95, 61)),
                    Tile((96, 61)),
                    Tile((97, 61)),
                    Tile((88, 62)),
                    Tile((89, 62)),
                    Tile((90, 62)),
                    Tile((91, 62)),
                    Tile((92, 62)),
                    Tile((93, 62)),
                    Tile((94, 62)),
                    Tile((95, 62)),
                    Tile((96, 62)),
                    Tile((97, 62)),
                    Tile((88, 63)),
                    Tile((89, 63)),
                    Tile((90, 63)),
                    Tile((91, 63)),
                    Tile((92, 63)),
                    Tile((93, 63)),
                    Tile((94, 63)),
                    Tile((95, 63)),
                    Tile((96, 63)),
                    Tile((97, 63)),
                ],
            },
            Civ.DUTCH: {
                Area.TILE_MIN: Tile((46, 50)),
                Area.TILE_MAX: Tile((52, 55)),
                Area.ADDITIONAL_TILES: [
                    Tile((46, 49)),
                    Tile((47, 49)),
                    Tile((48, 49)),
                    Tile((49, 49)),
                    Tile((50, 49)),
                ],
            },
            Civ.POPE: {
                Area.TILE_MIN: Tile((54, 25)),
                Area.TILE_MAX: Tile((58, 29)),
            },
        }
    )
    .apply(
        lambda area: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                area[Area.TILE_MIN],
                area[Area.TILE_MAX],
            )
            .extend(area.get(Area.ADDITIONAL_TILES))
            .substract(area.get(Area.EXCEPTION_TILES))
            .normalize()
            .data
        )
    )
    .fill_missing_members(None)
)

CIV_NORMAL_AREA = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: {
                Area.TILE_MIN: Tile((66, 13)),
                Area.TILE_MAX: Tile((75, 24)),
            },
            Civ.FRANCE: {
                Area.TILE_MIN: Tile((33, 32)),
                Area.TILE_MAX: Tile((44, 46)),
                Area.EXCEPTION_TILES: [
                    Tile((33, 32)),
                    Tile((33, 33)),
                    Tile((33, 34)),
                    Tile((33, 35)),
                    Tile((33, 36)),
                    Tile((34, 32)),
                    Tile((34, 33)),
                    Tile((34, 34)),
                    Tile((34, 35)),
                    Tile((35, 32)),
                    Tile((35, 33)),
                    Tile((35, 34)),
                    Tile((36, 32)),
                    Tile((36, 33)),
                    Tile((37, 32)),
                    Tile((38, 32)),
                ],
            },
            Civ.ARABIA: {
                Area.TILE_MIN: Tile((53, 0)),
                Area.TILE_MAX: Tile((99, 11)),
                Area.EXCEPTION_TILES: [
                    Tile((73, 10)),
                    Tile((74, 10)),
                    Tile((75, 10)),
                    Tile((76, 10)),
                    Tile((87, 10)),
                    Tile((87, 11)),
                    Tile((88, 10)),
                    Tile((88, 11)),
                    Tile((89, 11)),
                ],
            },
            Civ.BULGARIA: {
                Area.TILE_MIN: Tile((72, 27)),
                Area.TILE_MAX: Tile((80, 31)),
            },
            Civ.CORDOBA: {
                Area.TILE_MIN: Tile((43, 8)),
                Area.TILE_MAX: Tile((52, 19)),
            },
            Civ.VENECIA: {
                Area.TILE_MIN: Tile((54, 32)),
                Area.TILE_MAX: Tile((60, 37)),
                Area.EXCEPTION_TILES: [
                    Tile((54, 32)),
                    Tile((54, 33)),
                    Tile((54, 34)),
                    Tile((55, 32)),
                    Tile((55, 33)),
                    Tile((55, 34)),
                    Tile((56, 32)),
                    Tile((56, 33)),
                    Tile((56, 34)),
                    Tile((57, 32)),
                    Tile((57, 33)),
                    Tile((58, 32)),
                    Tile((59, 37)),
                    Tile((60, 36)),
                    Tile((60, 37)),
                ],
            },
            Civ.BURGUNDY: {
                Area.TILE_MIN: Tile((45, 32)),
                Area.TILE_MAX: Tile((49, 43)),
                Area.EXCEPTION_TILES: [
                    Tile((49, 32)),
                    Tile((49, 33)),
                    Tile((49, 34)),
                    Tile((49, 35)),
                    Tile((49, 36)),
                ],
            },
            Civ.GERMANY: {
                Area.TILE_MIN: Tile((51, 43)),
                Area.TILE_MAX: Tile((61, 54)),
                Area.EXCEPTION_TILES: [
                    Tile((51, 51)),
                    Tile((51, 52)),
                    Tile((51, 53)),
                    Tile((51, 54)),
                    Tile((52, 51)),
                    Tile((52, 52)),
                    Tile((52, 53)),
                    Tile((52, 54)),
                    Tile((59, 48)),
                    Tile((59, 49)),
                    Tile((59, 50)),
                    Tile((59, 51)),
                    Tile((59, 52)),
                    Tile((59, 53)),
                    Tile((59, 54)),
                    Tile((60, 48)),
                    Tile((60, 49)),
                    Tile((60, 50)),
                    Tile((60, 51)),
                    Tile((60, 52)),
                    Tile((60, 53)),
                    Tile((60, 54)),
                    Tile((61, 48)),
                    Tile((61, 49)),
                    Tile((61, 50)),
                    Tile((61, 51)),
                    Tile((61, 52)),
                    Tile((61, 53)),
                    Tile((61, 54)),
                ],
            },
            Civ.NOVGOROD: {
                Area.TILE_MIN: Tile((77, 59)),
                Area.TILE_MAX: Tile((88, 72)),
                Area.EXCEPTION_TILES: [
                    Tile((84, 59)),
                    Tile((84, 60)),
                    Tile((85, 59)),
                    Tile((85, 60)),
                    Tile((85, 61)),
                    Tile((86, 59)),
                    Tile((86, 60)),
                    Tile((86, 61)),
                    Tile((86, 62)),
                    Tile((87, 59)),
                    Tile((87, 60)),
                    Tile((87, 61)),
                    Tile((87, 62)),
                    Tile((88, 59)),
                    Tile((88, 60)),
                    Tile((88, 61)),
                    Tile((88, 62)),
                ],
            },
            Civ.NORWAY: {
                Area.TILE_MIN: Tile((53, 63)),
                Area.TILE_MAX: Tile((58, 72)),
            },
            Civ.KIEV: {
                Area.TILE_MIN: Tile((78, 41)),
                Area.TILE_MAX: Tile((91, 50)),
                Area.EXCEPTION_TILES: [
                    Tile((87, 41)),
                    Tile((88, 41)),
                    Tile((89, 41)),
                    Tile((90, 41)),
                    Tile((91, 41)),
                ],
            },
            Civ.HUNGARY: {
                Area.TILE_MIN: Tile((63, 32)),
                Area.TILE_MAX: Tile((77, 41)),
                Area.EXCEPTION_TILES: [
                    Tile((63, 32)),
                    Tile((63, 39)),
                    Tile((63, 40)),
                    Tile((63, 41)),
                    Tile((64, 41)),
                    Tile((72, 32)),
                    Tile((73, 32)),
                    Tile((74, 32)),
                    Tile((75, 32)),
                    Tile((75, 41)),
                    Tile((76, 32)),
                    Tile((76, 40)),
                    Tile((76, 41)),
                    Tile((77, 32)),
                    Tile((77, 39)),
                    Tile((77, 40)),
                    Tile((77, 41)),
                ],
            },
            Civ.CASTILLE: {
                Area.TILE_MIN: Tile((25, 26)),
                Area.TILE_MAX: Tile((34, 36)),
                Area.EXCEPTION_TILES: [
                    Tile((25, 26)),
                    Tile((25, 27)),
                    Tile((25, 28)),
                    Tile((25, 29)),
                    Tile((25, 30)),
                    Tile((25, 31)),
                    Tile((34, 36)),
                ],
            },
            Civ.DENMARK: {
                Area.TILE_MIN: Tile((54, 55)),
                Area.TILE_MAX: Tile((59, 61)),
            },
            Civ.SCOTLAND: {
                Area.TILE_MIN: Tile((34, 63)),
                Area.TILE_MAX: Tile((39, 69)),
                Area.EXCEPTION_TILES: [
                    Tile((34, 69)),
                ],
            },
            Civ.POLAND: {
                Area.TILE_MIN: Tile((63, 43)),
                Area.TILE_MAX: Tile((77, 50)),
                Area.EXCEPTION_TILES: [
                    Tile((63, 43)),
                    Tile((63, 44)),
                    Tile((63, 45)),
                    Tile((64, 43)),
                    Tile((64, 44)),
                    Tile((65, 43)),
                ],
            },
            Civ.GENOA: {
                Area.TILE_MIN: Tile((49, 22)),
                Area.TILE_MAX: Tile((52, 36)),
            },
            Civ.MOROCCO: {
                Area.TILE_MIN: Tile((18, 3)),
                Area.TILE_MAX: Tile((27, 13)),
            },
            Civ.ENGLAND: {
                Area.TILE_MIN: Tile((32, 50)),
                Area.TILE_MAX: Tile((43, 62)),
                Area.EXCEPTION_TILES: [
                    Tile((32, 55)),
                    Tile((32, 56)),
                    Tile((32, 57)),
                    Tile((32, 58)),
                    Tile((32, 59)),
                    Tile((32, 60)),
                    Tile((32, 61)),
                    Tile((32, 62)),
                    Tile((33, 56)),
                    Tile((33, 57)),
                    Tile((33, 58)),
                    Tile((33, 59)),
                    Tile((33, 60)),
                    Tile((33, 61)),
                    Tile((33, 62)),
                ],
            },
            Civ.PORTUGAL: {
                Area.TILE_MIN: Tile((21, 21)),
                Area.TILE_MAX: Tile((25, 32)),
                Area.EXCEPTION_TILES: [
                    Tile((25, 21)),
                    Tile((25, 22)),
                    Tile((25, 23)),
                    Tile((25, 24)),
                    Tile((25, 25)),
                    Tile((25, 26)),
                    Tile((25, 32)),
                ],
            },
            Civ.ARAGON: {
                Area.TILE_MIN: Tile((54, 16)),
                Area.TILE_MAX: Tile((64, 26)),
            },
            Civ.SWEDEN: {
                Area.TILE_MIN: Tile((60, 59)),
                Area.TILE_MAX: Tile((75, 72)),
                Area.EXCEPTION_TILES: [
                    Tile((60, 59)),
                    Tile((60, 60)),
                    Tile((60, 61)),
                    Tile((60, 70)),
                    Tile((60, 71)),
                    Tile((60, 72)),
                    Tile((61, 59)),
                    Tile((61, 60)),
                    Tile((61, 72)),
                    Tile((70, 59)),
                    Tile((70, 60)),
                    Tile((70, 61)),
                    Tile((71, 59)),
                    Tile((71, 60)),
                    Tile((71, 61)),
                    Tile((72, 59)),
                    Tile((72, 60)),
                    Tile((72, 61)),
                    Tile((73, 59)),
                    Tile((73, 60)),
                    Tile((73, 61)),
                    Tile((73, 62)),
                    Tile((74, 59)),
                    Tile((74, 60)),
                    Tile((74, 61)),
                    Tile((74, 62)),
                    Tile((74, 63)),
                    Tile((75, 59)),
                    Tile((75, 60)),
                    Tile((75, 61)),
                    Tile((75, 62)),
                    Tile((75, 63)),
                ],
            },
            Civ.PRUSSIA: {
                Area.TILE_MIN: Tile((59, 48)),
                Area.TILE_MAX: Tile((71, 55)),
                Area.EXCEPTION_TILES: [
                    Tile((59, 55)),
                    Tile((60, 55)),
                    Tile((61, 55)),
                    Tile((63, 48)),
                    Tile((63, 49)),
                    Tile((63, 50)),
                    Tile((64, 48)),
                    Tile((64, 49)),
                    Tile((64, 50)),
                    Tile((65, 48)),
                    Tile((65, 49)),
                    Tile((65, 50)),
                    Tile((66, 48)),
                    Tile((66, 49)),
                    Tile((66, 50)),
                    Tile((67, 48)),
                    Tile((67, 49)),
                    Tile((67, 50)),
                    Tile((68, 48)),
                    Tile((68, 49)),
                    Tile((68, 50)),
                    Tile((69, 48)),
                    Tile((69, 49)),
                    Tile((69, 50)),
                    Tile((70, 48)),
                    Tile((70, 49)),
                    Tile((70, 50)),
                    Tile((71, 48)),
                    Tile((71, 49)),
                    Tile((71, 50)),
                    Tile((71, 55)),
                ],
            },
            Civ.LITHUANIA: {
                Area.TILE_MIN: Tile((70, 51)),
                Area.TILE_MAX: Tile((77, 63)),
                Area.EXCEPTION_TILES: [
                    Tile((70, 51)),
                    Tile((70, 52)),
                    Tile((70, 53)),
                    Tile((70, 54)),
                    Tile((70, 55)),
                    Tile((70, 59)),
                    Tile((70, 60)),
                    Tile((70, 61)),
                    Tile((70, 62)),
                    Tile((70, 63)),
                    Tile((71, 51)),
                    Tile((71, 52)),
                    Tile((71, 53)),
                    Tile((71, 54)),
                    Tile((71, 60)),
                    Tile((71, 61)),
                    Tile((71, 62)),
                    Tile((71, 63)),
                    Tile((72, 51)),
                    Tile((72, 60)),
                    Tile((72, 61)),
                    Tile((72, 62)),
                    Tile((72, 63)),
                    Tile((73, 63)),
                    Tile((77, 59)),
                    Tile((77, 60)),
                    Tile((77, 61)),
                    Tile((77, 62)),
                    Tile((77, 63)),
                ],
            },
            Civ.AUSTRIA: {
                Area.TILE_MIN: Tile((57, 36)),
                Area.TILE_MAX: Tile((63, 42)),
                Area.EXCEPTION_TILES: [
                    Tile((57, 36)),
                    Tile((57, 37)),
                    Tile((58, 36)),
                    Tile((58, 37)),
                    Tile((59, 36)),
                    Tile((63, 36)),
                    Tile((63, 37)),
                    Tile((63, 38)),
                ],
            },
            Civ.OTTOMAN: {
                Area.TILE_MIN: Tile((76, 14)),
                Area.TILE_MAX: Tile((98, 27)),
                Area.EXCEPTION_TILES: [
                    Tile((76, 27)),
                    Tile((77, 27)),
                    Tile((78, 27)),
                    Tile((79, 27)),
                    Tile((80, 27)),
                ],
            },
            Civ.MOSCOW: {
                Area.TILE_MIN: Tile((83, 51)),
                Area.TILE_MAX: Tile((98, 63)),
                Area.EXCEPTION_TILES: [
                    Tile((83, 59)),
                    Tile((83, 60)),
                    Tile((83, 61)),
                    Tile((83, 62)),
                    Tile((83, 63)),
                    Tile((84, 61)),
                    Tile((84, 62)),
                    Tile((84, 63)),
                    Tile((85, 62)),
                    Tile((85, 63)),
                    Tile((86, 63)),
                    Tile((87, 63)),
                    Tile((88, 63)),
                ],
            },
            Civ.DUTCH: {
                Area.TILE_MIN: Tile((47, 50)),
                Area.TILE_MAX: Tile((52, 54)),
                Area.EXCEPTION_TILES: [
                    Tile((51, 50)),
                    Tile((52, 50)),
                ],
            },
            Civ.POPE: {
                Area.TILE_MIN: Tile((54, 25)),
                Area.TILE_MAX: Tile((58, 29)),
            },
        }
    )
    .apply(
        lambda area: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                area[Area.TILE_MIN],
                area[Area.TILE_MAX],
            )
            .extend(area.get(Area.ADDITIONAL_TILES))
            .substract(area.get(Area.EXCEPTION_TILES))
            .normalize()
            .data
        )
    )
    .fill_missing_members(None)
)

CIV_BROADER_AREA = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: {
                Area.TILE_MIN: Tile((68, 14)),
                Area.TILE_MAX: Tile((83, 27)),
            },
            Civ.FRANCE: {
                Area.TILE_MIN: Tile((39, 41)),
                Area.TILE_MAX: Tile((49, 51)),
            },
            Civ.ARABIA: {
                Area.TILE_MIN: Tile((92, 7)),
                Area.TILE_MAX: Tile((99, 15)),
            },
            Civ.BULGARIA: {
                Area.TILE_MIN: Tile((71, 28)),
                Area.TILE_MAX: Tile((80, 31)),
            },
            Civ.CORDOBA: {
                Area.TILE_MIN: Tile((24, 23)),
                Area.TILE_MAX: Tile((34, 33)),
            },
            Civ.VENECIA: {
                Area.TILE_MIN: Tile((52, 29)),
                Area.TILE_MAX: Tile((62, 39)),
            },
            Civ.BURGUNDY: {
                Area.TILE_MIN: Tile((42, 36)),
                Area.TILE_MAX: Tile((52, 46)),
            },
            Civ.GERMANY: {
                Area.TILE_MIN: Tile((49, 41)),
                Area.TILE_MAX: Tile((58, 51)),
            },
            Civ.NOVGOROD: {
                Area.TILE_MIN: Tile((77, 59)),
                Area.TILE_MAX: Tile((89, 72)),
            },
            Civ.NORWAY: {
                Area.TILE_MIN: Tile((53, 63)),
                Area.TILE_MAX: Tile((61, 72)),
            },
            Civ.KIEV: {
                Area.TILE_MIN: Tile((81, 37)),
                Area.TILE_MAX: Tile((91, 47)),
            },
            Civ.HUNGARY: {
                Area.TILE_MIN: Tile((64, 27)),
                Area.TILE_MAX: Tile((74, 37)),
            },
            Civ.CASTILLE: {
                Area.TILE_MIN: Tile((23, 31)),
                Area.TILE_MAX: Tile((33, 41)),
            },
            Civ.DENMARK: {
                Area.TILE_MIN: Tile((55, 55)),
                Area.TILE_MAX: Tile((59, 60)),
            },
            Civ.SCOTLAND: {
                Area.TILE_MIN: Tile((31, 57)),
                Area.TILE_MAX: Tile((45, 69)),
            },
            Civ.POLAND: {
                Area.TILE_MIN: Tile((64, 42)),
                Area.TILE_MAX: Tile((74, 52)),
            },
            Civ.GENOA: {
                Area.TILE_MIN: Tile((45, 29)),
                Area.TILE_MAX: Tile((55, 39)),
            },
            Civ.MOROCCO: {
                Area.TILE_MIN: Tile((11, 2)),
                Area.TILE_MAX: Tile((29, 27)),
            },
            Civ.ENGLAND: {
                Area.TILE_MIN: Tile((38, 49)),
                Area.TILE_MAX: Tile((48, 59)),
            },
            Civ.PORTUGAL: {
                Area.TILE_MIN: Tile((17, 27)),
                Area.TILE_MAX: Tile((27, 37)),
            },
            Civ.ARAGON: {
                Area.TILE_MIN: Tile((33, 25)),
                Area.TILE_MAX: Tile((43, 34)),
            },
            Civ.SWEDEN: {
                Area.TILE_MIN: Tile((60, 58)),
                Area.TILE_MAX: Tile((77, 72)),
            },
            Civ.PRUSSIA: {
                Area.TILE_MIN: Tile((59, 49)),
                Area.TILE_MAX: Tile((72, 55)),
            },
            Civ.LITHUANIA: {
                Area.TILE_MIN: Tile((68, 45)),
                Area.TILE_MAX: Tile((82, 64)),
            },
            Civ.AUSTRIA: {
                Area.TILE_MIN: Tile((56, 35)),
                Area.TILE_MAX: Tile((66, 45)),
            },
            Civ.OTTOMAN: {
                Area.TILE_MIN: Tile((83, 17)),
                Area.TILE_MAX: Tile((93, 27)),
            },
            Civ.MOSCOW: {
                Area.TILE_MIN: Tile((83, 51)),
                Area.TILE_MAX: Tile((93, 61)),
            },
            Civ.DUTCH: {
                Area.TILE_MIN: Tile((44, 47)),
                Area.TILE_MAX: Tile((54, 57)),
            },
            Civ.POPE: {
                Area.TILE_MIN: Tile((54, 25)),
                Area.TILE_MAX: Tile((58, 29)),
            },
        }
    )
    .apply(
        lambda area: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                area[Area.TILE_MIN],
                area[Area.TILE_MAX],
            )
            .extend(area.get(Area.ADDITIONAL_TILES))
            .substract(area.get(Area.EXCEPTION_TILES))
            .normalize()
            .data
        )
    )
    .fill_missing_members(None)
)

CIV_AREAS = CivDataMapper(
    {
        civ: {
            AreaTypes.CORE: CIV_CORE_AREA[civ],
            AreaTypes.NORMAL: CIV_NORMAL_AREA[civ],
            AreaTypes.BROADER: CIV_BROADER_AREA[civ],
        }
        for civ in Civ
    }
)

CIV_VISIBLE_AREA_500AD = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: [
                {
                    Area.TILE_MIN: Tile((64, 0)),
                    Area.TILE_MAX: Tile((99, 34)),
                },
                {
                    Area.TILE_MIN: Tile((49, 1)),
                    Area.TILE_MAX: Tile((63, 38)),
                },
                {
                    Area.TILE_MIN: Tile((24, 13)),
                    Area.TILE_MAX: Tile((48, 36)),
                },
            ],
            Civ.FRANCE: [
                {
                    Area.TILE_MIN: Tile((35, 31)),
                    Area.TILE_MAX: Tile((52, 51)),
                },
                {
                    Area.TILE_MIN: Tile((49, 26)),
                    Area.TILE_MAX: Tile((59, 38)),
                },
            ],
            Civ.ARABIA: [
                {
                    Area.TILE_MIN: Tile((79, 0)),
                    Area.TILE_MAX: Tile((89, 6)),
                },
                {
                    Area.TILE_MIN: Tile((90, 0)),
                    Area.TILE_MAX: Tile((99, 22)),
                },
            ],
            Civ.BULGARIA: [
                {
                    Area.TILE_MIN: Tile((69, 23)),
                    Area.TILE_MAX: Tile((81, 32)),
                },
                {
                    Area.TILE_MIN: Tile((78, 31)),
                    Area.TILE_MAX: Tile((99, 41)),
                },
            ],
            Civ.CORDOBA: [
                {
                    Area.TILE_MIN: Tile((18, 13)),
                    Area.TILE_MAX: Tile((39, 33)),
                },
                {
                    Area.TILE_MIN: Tile((40, 0)),
                    Area.TILE_MAX: Tile((59, 20)),
                },
                {
                    Area.TILE_MIN: Tile((60, 0)),
                    Area.TILE_MAX: Tile((95, 7)),
                },
            ],
            Civ.VENECIA: [
                {
                    Area.TILE_MIN: Tile((47, 14)),
                    Area.TILE_MAX: Tile((59, 38)),
                },
                {
                    Area.TILE_MIN: Tile((60, 18)),
                    Area.TILE_MAX: Tile((63, 35)),
                },
                {
                    Area.TILE_MIN: Tile((64, 18)),
                    Area.TILE_MAX: Tile((68, 29)),
                },
            ],
            Civ.BURGUNDY: [
                {
                    Area.TILE_MIN: Tile((43, 31)),
                    Area.TILE_MAX: Tile((53, 53)),
                },
            ],
            Civ.GERMANY: [
                {
                    Area.TILE_MIN: Tile((44, 31)),
                    Area.TILE_MAX: Tile((46, 52)),
                },
                {
                    Area.TILE_MIN: Tile((47, 27)),
                    Area.TILE_MAX: Tile((61, 55)),
                },
                {
                    Area.TILE_MIN: Tile((62, 50)),
                    Area.TILE_MAX: Tile((70, 55)),
                },
            ],
            Civ.NOVGOROD: [
                {
                    Area.TILE_MIN: Tile((72, 55)),
                    Area.TILE_MAX: Tile((90, 72)),
                },
                {
                    Area.TILE_MIN: Tile((79, 41)),
                    Area.TILE_MAX: Tile((88, 54)),
                },
            ],
            Civ.NORWAY: [
                {
                    Area.TILE_MIN: Tile((49, 52)),
                    Area.TILE_MAX: Tile((71, 72)),
                },
                {
                    Area.TILE_MIN: Tile((30, 56)),
                    Area.TILE_MAX: Tile((48, 72)),
                },
            ],
            Civ.KIEV: [
                {
                    Area.TILE_MIN: Tile((77, 24)),
                    Area.TILE_MAX: Tile((82, 40)),
                },
                {
                    Area.TILE_MIN: Tile((83, 33)),
                    Area.TILE_MAX: Tile((88, 46)),
                },
                {
                    Area.TILE_MIN: Tile((77, 39)),
                    Area.TILE_MAX: Tile((91, 56)),
                },
            ],
            Civ.HUNGARY: [
                {
                    Area.TILE_MIN: Tile((59, 30)),
                    Area.TILE_MAX: Tile((82, 42)),
                },
                {
                    Area.TILE_MIN: Tile((83, 36)),
                    Area.TILE_MAX: Tile((92, 42)),
                },
            ],
            Civ.CASTILLE: [
                {
                    Area.TILE_MIN: Tile((22, 25)),
                    Area.TILE_MAX: Tile((35, 38)),
                },
                {
                    Area.TILE_MIN: Tile((36, 25)),
                    Area.TILE_MAX: Tile((43, 40)),
                },
            ],
            Civ.DENMARK: [
                {
                    Area.TILE_MIN: Tile((34, 46)),
                    Area.TILE_MAX: Tile((49, 72)),
                },
                {
                    Area.TILE_MIN: Tile((50, 50)),
                    Area.TILE_MAX: Tile((71, 72)),
                },
                {
                    Area.TILE_MIN: Tile((72, 57)),
                    Area.TILE_MAX: Tile((78, 64)),
                },
            ],
            Civ.SCOTLAND: [
                {
                    Area.TILE_MIN: Tile((30, 51)),
                    Area.TILE_MAX: Tile((46, 72)),
                },
                {
                    Area.TILE_MIN: Tile((35, 46)),
                    Area.TILE_MAX: Tile((46, 50)),
                },
            ],
            Civ.POLAND: [
                {
                    Area.TILE_MIN: Tile((60, 40)),
                    Area.TILE_MAX: Tile((74, 55)),
                },
                {
                    Area.TILE_MIN: Tile((75, 40)),
                    Area.TILE_MAX: Tile((79, 48)),
                },
            ],
            Civ.GENOA: [
                {
                    Area.TILE_MIN: Tile((39, 20)),
                    Area.TILE_MAX: Tile((60, 38)),
                },
                {
                    Area.TILE_MIN: Tile((47, 14)),
                    Area.TILE_MAX: Tile((63, 32)),
                },
                {
                    Area.TILE_MIN: Tile((64, 16)),
                    Area.TILE_MAX: Tile((67, 29)),
                },
            ],
            Civ.MOROCCO: [
                {
                    Area.TILE_MIN: Tile((12, 2)),
                    Area.TILE_MAX: Tile((42, 31)),
                },
                {
                    Area.TILE_MIN: Tile((43, 10)),
                    Area.TILE_MAX: Tile((53, 20)),
                },
            ],
            Civ.ENGLAND: [
                {
                    Area.TILE_MIN: Tile((31, 49)),
                    Area.TILE_MAX: Tile((45, 64)),
                },
                {
                    Area.TILE_MIN: Tile((37, 46)),
                    Area.TILE_MAX: Tile((45, 48)),
                },
            ],
            Civ.PORTUGAL: [
                {
                    Area.TILE_MIN: Tile((18, 22)),
                    Area.TILE_MAX: Tile((34, 39)),
                },
            ],
            Civ.ARAGON: [
                {
                    Area.TILE_MIN: Tile((19, 23)),
                    Area.TILE_MAX: Tile((56, 40)),
                },
                {
                    Area.TILE_MIN: Tile((25, 21)),
                    Area.TILE_MAX: Tile((45, 22)),
                },
                {
                    Area.TILE_MIN: Tile((46, 14)),
                    Area.TILE_MAX: Tile((63, 28)),
                },
            ],
            Civ.SWEDEN: [
                {
                    Area.TILE_MIN: Tile((39, 52)),
                    Area.TILE_MAX: Tile((82, 66)),
                },
                {
                    Area.TILE_MIN: Tile((34, 61)),
                    Area.TILE_MAX: Tile((71, 72)),
                },
            ],
            Civ.PRUSSIA: [
                {
                    Area.TILE_MIN: Tile((51, 43)),
                    Area.TILE_MAX: Tile((73, 56)),
                },
                {
                    Area.TILE_MIN: Tile((66, 57)),
                    Area.TILE_MAX: Tile((82, 62)),
                },
                {
                    Area.TILE_MIN: Tile((69, 63)),
                    Area.TILE_MAX: Tile((79, 66)),
                },
            ],
            Civ.LITHUANIA: [
                {
                    Area.TILE_MIN: Tile((67, 46)),
                    Area.TILE_MAX: Tile((76, 55)),
                },
                {
                    Area.TILE_MIN: Tile((73, 44)),
                    Area.TILE_MAX: Tile((81, 58)),
                },
            ],
            Civ.AUSTRIA: [
                {
                    Area.TILE_MIN: Tile((49, 27)),
                    Area.TILE_MAX: Tile((61, 55)),
                },
                {
                    Area.TILE_MIN: Tile((62, 34)),
                    Area.TILE_MAX: Tile((67, 46)),
                },
            ],
            Civ.OTTOMAN: [
                {
                    Area.TILE_MIN: Tile((75, 13)),
                    Area.TILE_MAX: Tile((99, 27)),
                },
                {
                    Area.TILE_MIN: Tile((92, 4)),
                    Area.TILE_MAX: Tile((99, 12)),
                },
            ],
            Civ.MOSCOW: [
                {
                    Area.TILE_MIN: Tile((77, 42)),
                    Area.TILE_MAX: Tile((99, 51)),
                },
                {
                    Area.TILE_MIN: Tile((74, 52)),
                    Area.TILE_MAX: Tile((99, 67)),
                },
            ],
            Civ.DUTCH: [
                {
                    Area.TILE_MIN: Tile((40, 45)),
                    Area.TILE_MAX: Tile((65, 57)),
                },
                {
                    Area.TILE_MIN: Tile((49, 58)),
                    Area.TILE_MAX: Tile((67, 66)),
                },
                {
                    Area.TILE_MIN: Tile((46, 39)),
                    Area.TILE_MAX: Tile((63, 44)),
                },
            ],
            Civ.POPE: [
                {
                    Area.TILE_MIN: Tile((39, 12)),
                    Area.TILE_MAX: Tile((73, 44)),
                },
            ],
        }
    )
    .applymap(
        lambda areas: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                areas[Area.TILE_MIN],
                areas[Area.TILE_MAX],
            )
            .normalize()
            .data
        )
    )
    .apply(lambda tiles: merge_tiles(*tiles))
)

CIV_VISIBLE_AREA_1200AD = (
    CivDataMapper(
        {
            Civ.BYZANTIUM: [
                {
                    Area.TILE_MIN: Tile((64, 0)),
                    Area.TILE_MAX: Tile((99, 34)),
                },
                {
                    Area.TILE_MIN: Tile((49, 1)),
                    Area.TILE_MAX: Tile((63, 38)),
                },
                {
                    Area.TILE_MIN: Tile((24, 13)),
                    Area.TILE_MAX: Tile((48, 36)),
                },
            ],
            Civ.FRANCE: [
                {
                    Area.TILE_MIN: Tile((30, 26)),
                    Area.TILE_MAX: Tile((59, 54)),
                },
                {
                    Area.TILE_MIN: Tile((35, 55)),
                    Area.TILE_MAX: Tile((40, 70)),
                },
            ],
            Civ.ARABIA: [
                {
                    Area.TILE_MIN: Tile((26, 20)),
                    Area.TILE_MAX: Tile((35, 23)),
                },
                {
                    Area.TILE_MIN: Tile((22, 5)),
                    Area.TILE_MAX: Tile((27, 19)),
                },
                {
                    Area.TILE_MIN: Tile((28, 9)),
                    Area.TILE_MAX: Tile((53, 19)),
                },
                {
                    Area.TILE_MIN: Tile((47, 0)),
                    Area.TILE_MAX: Tile((85, 8)),
                },
                {
                    Area.TILE_MIN: Tile((86, 0)),
                    Area.TILE_MAX: Tile((99, 20)),
                },
            ],
            Civ.BULGARIA: [
                {
                    Area.TILE_MIN: Tile((65, 12)),
                    Area.TILE_MAX: Tile((83, 38)),
                },
                {
                    Area.TILE_MIN: Tile((78, 31)),
                    Area.TILE_MAX: Tile((99, 41)),
                },
            ],
            Civ.CORDOBA: [
                {
                    Area.TILE_MIN: Tile((18, 13)),
                    Area.TILE_MAX: Tile((39, 33)),
                },
                {
                    Area.TILE_MIN: Tile((40, 0)),
                    Area.TILE_MAX: Tile((59, 20)),
                },
                {
                    Area.TILE_MIN: Tile((60, 0)),
                    Area.TILE_MAX: Tile((95, 7)),
                },
            ],
            Civ.VENECIA: [
                {
                    Area.TILE_MIN: Tile((46, 14)),
                    Area.TILE_MAX: Tile((70, 41)),
                },
                {
                    Area.TILE_MIN: Tile((49, 7)),
                    Area.TILE_MAX: Tile((82, 25)),
                },
                {
                    Area.TILE_MIN: Tile((83, 7)),
                    Area.TILE_MAX: Tile((91, 13)),
                },
            ],
            Civ.BURGUNDY: [
                {
                    Area.TILE_MIN: Tile((43, 31)),
                    Area.TILE_MAX: Tile((53, 53)),
                },
            ],
            Civ.GERMANY: [
                {
                    Area.TILE_MIN: Tile((41, 31)),
                    Area.TILE_MAX: Tile((61, 58)),
                },
                {
                    Area.TILE_MIN: Tile((47, 27)),
                    Area.TILE_MAX: Tile((61, 30)),
                },
                {
                    Area.TILE_MIN: Tile((62, 34)),
                    Area.TILE_MAX: Tile((70, 55)),
                },
                {
                    Area.TILE_MIN: Tile((55, 22)),
                    Area.TILE_MAX: Tile((61, 26)),
                },
            ],
            Civ.NOVGOROD: [
                {
                    Area.TILE_MIN: Tile((72, 55)),
                    Area.TILE_MAX: Tile((90, 72)),
                },
                {
                    Area.TILE_MIN: Tile((79, 41)),
                    Area.TILE_MAX: Tile((88, 54)),
                },
                {
                    Area.TILE_MIN: Tile((91, 60)),
                    Area.TILE_MAX: Tile((99, 72)),
                },
            ],
            Civ.NORWAY: [
                {
                    Area.TILE_MIN: Tile((30, 52)),
                    Area.TILE_MAX: Tile((71, 72)),
                },
                {
                    Area.TILE_MIN: Tile((0, 67)),
                    Area.TILE_MAX: Tile((29, 72)),
                },
            ],
            Civ.KIEV: [
                {
                    Area.TILE_MIN: Tile((75, 42)),
                    Area.TILE_MAX: Tile((94, 62)),
                },
                {
                    Area.TILE_MIN: Tile((77, 31)),
                    Area.TILE_MAX: Tile((94, 41)),
                },
                {
                    Area.TILE_MIN: Tile((77, 24)),
                    Area.TILE_MAX: Tile((82, 40)),
                },
            ],
            Civ.HUNGARY: [
                {
                    Area.TILE_MIN: Tile((56, 27)),
                    Area.TILE_MAX: Tile((82, 45)),
                },
                {
                    Area.TILE_MIN: Tile((83, 31)),
                    Area.TILE_MAX: Tile((92, 42)),
                },
                {
                    Area.TILE_MIN: Tile((65, 12)),
                    Area.TILE_MAX: Tile((82, 26)),
                },
            ],
            Civ.CASTILLE: [
                {
                    Area.TILE_MIN: Tile((20, 17)),
                    Area.TILE_MAX: Tile((56, 40)),
                },
            ],
            Civ.DENMARK: [
                {
                    Area.TILE_MIN: Tile((34, 46)),
                    Area.TILE_MAX: Tile((71, 72)),
                },
                {
                    Area.TILE_MIN: Tile((72, 57)),
                    Area.TILE_MAX: Tile((78, 72)),
                },
            ],
            Civ.SCOTLAND: [
                {
                    Area.TILE_MIN: Tile((30, 43)),
                    Area.TILE_MAX: Tile((46, 72)),
                },
            ],
            Civ.POLAND: [
                {
                    Area.TILE_MIN: Tile((60, 37)),
                    Area.TILE_MAX: Tile((79, 60)),
                },
            ],
            Civ.GENOA: [
                {
                    Area.TILE_MIN: Tile((39, 15)),
                    Area.TILE_MAX: Tile((60, 39)),
                },
                {
                    Area.TILE_MIN: Tile((47, 9)),
                    Area.TILE_MAX: Tile((82, 25)),
                },
                {
                    Area.TILE_MIN: Tile((61, 26)),
                    Area.TILE_MAX: Tile((67, 32)),
                },
            ],
            Civ.MOROCCO: [
                {
                    Area.TILE_MIN: Tile((12, 2)),
                    Area.TILE_MAX: Tile((42, 31)),
                },
                {
                    Area.TILE_MIN: Tile((43, 2)),
                    Area.TILE_MAX: Tile((53, 20)),
                },
            ],
            Civ.ENGLAND: [
                {
                    Area.TILE_MIN: Tile((26, 54)),
                    Area.TILE_MAX: Tile((46, 64)),
                },
                {
                    Area.TILE_MIN: Tile((31, 34)),
                    Area.TILE_MAX: Tile((46, 53)),
                },
            ],
            Civ.PORTUGAL: [
                {
                    Area.TILE_MIN: Tile((18, 17)),
                    Area.TILE_MAX: Tile((34, 39)),
                },
            ],
            Civ.ARAGON: [
                {
                    Area.TILE_MIN: Tile((19, 29)),
                    Area.TILE_MAX: Tile((56, 40)),
                },
                {
                    Area.TILE_MIN: Tile((19, 21)),
                    Area.TILE_MAX: Tile((34, 28)),
                },
                {
                    Area.TILE_MIN: Tile((35, 14)),
                    Area.TILE_MAX: Tile((63, 28)),
                },
            ],
            Civ.SWEDEN: [
                {
                    Area.TILE_MIN: Tile((39, 52)),
                    Area.TILE_MAX: Tile((82, 66)),
                },
                {
                    Area.TILE_MIN: Tile((34, 61)),
                    Area.TILE_MAX: Tile((71, 72)),
                },
            ],
            Civ.PRUSSIA: [
                {
                    Area.TILE_MIN: Tile((51, 43)),
                    Area.TILE_MAX: Tile((73, 56)),
                },
                {
                    Area.TILE_MIN: Tile((66, 57)),
                    Area.TILE_MAX: Tile((82, 62)),
                },
                {
                    Area.TILE_MIN: Tile((69, 63)),
                    Area.TILE_MAX: Tile((79, 66)),
                },
            ],
            Civ.LITHUANIA: [
                {
                    Area.TILE_MIN: Tile((67, 46)),
                    Area.TILE_MAX: Tile((76, 55)),
                },
                {
                    Area.TILE_MIN: Tile((73, 44)),
                    Area.TILE_MAX: Tile((81, 58)),
                },
            ],
            Civ.AUSTRIA: [
                {
                    Area.TILE_MIN: Tile((49, 27)),
                    Area.TILE_MAX: Tile((61, 55)),
                },
                {
                    Area.TILE_MIN: Tile((62, 34)),
                    Area.TILE_MAX: Tile((67, 46)),
                },
            ],
            Civ.OTTOMAN: [
                {
                    Area.TILE_MIN: Tile((75, 13)),
                    Area.TILE_MAX: Tile((99, 27)),
                },
                {
                    Area.TILE_MIN: Tile((92, 4)),
                    Area.TILE_MAX: Tile((99, 12)),
                },
            ],
            Civ.MOSCOW: [
                {
                    Area.TILE_MIN: Tile((77, 42)),
                    Area.TILE_MAX: Tile((99, 51)),
                },
                {
                    Area.TILE_MIN: Tile((74, 52)),
                    Area.TILE_MAX: Tile((99, 67)),
                },
            ],
            Civ.DUTCH: [
                {
                    Area.TILE_MIN: Tile((40, 45)),
                    Area.TILE_MAX: Tile((65, 57)),
                },
                {
                    Area.TILE_MIN: Tile((49, 58)),
                    Area.TILE_MAX: Tile((67, 66)),
                },
                {
                    Area.TILE_MIN: Tile((46, 39)),
                    Area.TILE_MAX: Tile((63, 44)),
                },
            ],
            Civ.POPE: [
                {
                    Area.TILE_MIN: Tile((39, 12)),
                    Area.TILE_MAX: Tile((73, 44)),
                },
            ],
        }
    )
    .applymap(
        lambda areas: (
            TilesFactory(WORLD_WIDTH, WORLD_HEIGHT)
            .rectangle(
                areas[Area.TILE_MIN],
                areas[Area.TILE_MAX],
            )
            .extend(areas.get(Area.ADDITIONAL_TILES))
            .substract(areas.get(Area.EXCEPTION_TILES))
            .normalize()
            .data
        )
    )
    .apply(lambda tiles: merge_tiles(*tiles))
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
