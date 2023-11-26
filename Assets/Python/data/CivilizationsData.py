from BaseStructures import EnumDataMapper
from CoreTypes import (
    Building,
    Civ,
    CivilizationProperty,
    Leader,
    LeaderType,
    Religion,
    Scenario,
    InitialCondition,
    Modifier,
    Technology,
    Wonder,
)
from CoreStructures import (
    CivDataMapper,
    ReligionDataMapper,
    ScenarioDataMapper,
)
from TimelineData import DateTurn

TECH_STARTERS = [
    [
        Technology.CALENDAR,
        Technology.ARCHITECTURE,
        Technology.BRONZE_CASTING,
        Technology.THEOLOGY,
        Technology.MANORIALISM,
        Technology.STIRRUP,
    ],
    [
        Technology.CALENDAR,
        Technology.ARCHITECTURE,
        Technology.BRONZE_CASTING,
        Technology.THEOLOGY,
        Technology.MANORIALISM,
        Technology.STIRRUP,
        Technology.ENGINEERING,
        Technology.CHAIN_MAIL,
        Technology.ART,
        Technology.MONASTICISM,
        Technology.VASSALAGE,
        Technology.ASTROLABE,
        Technology.MACHINERY,
        Technology.VAULTED_ARCHES,
        Technology.MUSIC,
        Technology.HERBAL_MEDICINE,
        Technology.FEUDALISM,
        Technology.FARRIERS,
    ],
    [
        Technology.CALENDAR,
        Technology.ARCHITECTURE,
        Technology.BRONZE_CASTING,
        Technology.THEOLOGY,
        Technology.MANORIALISM,
        Technology.STIRRUP,
        Technology.ENGINEERING,
        Technology.CHAIN_MAIL,
        Technology.ART,
        Technology.MONASTICISM,
        Technology.VASSALAGE,
        Technology.ASTROLABE,
        Technology.MACHINERY,
        Technology.VAULTED_ARCHES,
        Technology.MUSIC,
        Technology.HERBAL_MEDICINE,
        Technology.FEUDALISM,
        Technology.FARRIERS,
        Technology.MAPMAKING,
        Technology.BLAST_FURNACE,
        Technology.SIEGE_ENGINES,
        Technology.GOTHIC_ARCHITECTURE,
        Technology.LITERATURE,
        Technology.CODE_OF_LAWS,
        Technology.ARISTOCRACY,
        Technology.LATEEN_SAILS,
        Technology.PLATE_ARMOR,
        Technology.MONUMENT_BUILDING,
        Technology.CLASSICAL_KNOWLEDGE,
        Technology.ALCHEMY,
        Technology.CIVIL_SERVICE,
        Technology.CLOCKMAKING,
        Technology.PHILOSOPHY,
        Technology.EDUCATION,
        Technology.GUILDS,
        Technology.CHIVALRY,
    ],
    [
        Technology.CALENDAR,
        Technology.ARCHITECTURE,
        Technology.BRONZE_CASTING,
        Technology.THEOLOGY,
        Technology.MANORIALISM,
        Technology.STIRRUP,
        Technology.ENGINEERING,
        Technology.CHAIN_MAIL,
        Technology.ART,
        Technology.MONASTICISM,
        Technology.VASSALAGE,
        Technology.ASTROLABE,
        Technology.MACHINERY,
        Technology.VAULTED_ARCHES,
        Technology.MUSIC,
        Technology.HERBAL_MEDICINE,
        Technology.FEUDALISM,
        Technology.FARRIERS,
        Technology.MAPMAKING,
        Technology.BLAST_FURNACE,
        Technology.SIEGE_ENGINES,
        Technology.GOTHIC_ARCHITECTURE,
        Technology.LITERATURE,
        Technology.CODE_OF_LAWS,
        Technology.ARISTOCRACY,
        Technology.LATEEN_SAILS,
        Technology.PLATE_ARMOR,
        Technology.MONUMENT_BUILDING,
        Technology.CLASSICAL_KNOWLEDGE,
        Technology.ALCHEMY,
        Technology.CIVIL_SERVICE,
        Technology.CLOCKMAKING,
        Technology.PHILOSOPHY,
        Technology.EDUCATION,
        Technology.GUILDS,
        Technology.CHIVALRY,
        Technology.OPTICS,
        Technology.REPLACEABLE_PARTS,
        Technology.PATRONAGE,
        Technology.GUNPOWDER,
        Technology.BANKING,
        Technology.MILITARY_TRADITION,
        Technology.SHIP_BUILDING,
        Technology.DRAMA,
        Technology.DIVINE_RIGHT,
        Technology.CHEMISTRY,
        Technology.PAPER,
        Technology.PROFESSIONAL_ARMY,
        Technology.PRINTING_PRESS,
        Technology.PUBLIC_WORKS,
        Technology.MATCH_LOCK,
        Technology.ARABIC_KNOWLEDGE,
        Technology.ASTRONOMY,
    ],
]

CIV_INITIAL_TECH = CivDataMapper(
    {
        Civ.BYZANTIUM: [],
        Civ.FRANCE: [],
        Civ.ARABIA: [
            Technology.THEOLOGY,
            Technology.CALENDAR,
            Technology.LATEEN_SAILS,
            Technology.STIRRUP,
            Technology.BRONZE_CASTING,
            Technology.ARCHITECTURE,
            Technology.LITERATURE,
            Technology.MONASTICISM,
            Technology.ART,
            Technology.CODE_OF_LAWS,
            Technology.HERBAL_MEDICINE,
            Technology.ASTROLABE,
            Technology.ARABIC_KNOWLEDGE,
        ],
        Civ.BULGARIA: [
            Technology.THEOLOGY,
            Technology.CALENDAR,
            Technology.STIRRUP,
            Technology.ARCHITECTURE,
            Technology.BRONZE_CASTING,
        ],
        Civ.CORDOBA: [
            Technology.THEOLOGY,
            Technology.CALENDAR,
            Technology.LATEEN_SAILS,
            Technology.STIRRUP,
            Technology.BRONZE_CASTING,
            Technology.ARCHITECTURE,
            Technology.LITERATURE,
            Technology.MONASTICISM,
            Technology.ART,
            Technology.CODE_OF_LAWS,
            Technology.HERBAL_MEDICINE,
            Technology.ASTROLABE,
            Technology.ARABIC_KNOWLEDGE,
            Technology.ENGINEERING,
            Technology.ARABIC_MEDICINE,
        ],
        Civ.VENECIA: TECH_STARTERS[0]
        + [
            Technology.LATEEN_SAILS,
            Technology.ASTROLABE,
            Technology.MONASTICISM,
            Technology.ART,
            Technology.MUSIC,
            Technology.HERBAL_MEDICINE,
            Technology.CHAIN_MAIL,
        ],
        Civ.BURGUNDY: TECH_STARTERS[0]
        + [
            Technology.MONASTICISM,
            Technology.VASSALAGE,
            Technology.FEUDALISM,
            Technology.FARRIERS,
            Technology.ART,
            Technology.ENGINEERING,
            Technology.CHAIN_MAIL,
            Technology.ARISTOCRACY,
            Technology.CODE_OF_LAWS,
            Technology.ASTROLABE,
        ],
        Civ.GERMANY: TECH_STARTERS[0]
        + [
            Technology.MONASTICISM,
            Technology.VASSALAGE,
            Technology.FEUDALISM,
            Technology.FARRIERS,
            Technology.ART,
            Technology.ENGINEERING,
            Technology.CHAIN_MAIL,
            Technology.ARISTOCRACY,
            Technology.CODE_OF_LAWS,
            Technology.ASTROLABE,
        ],
        Civ.NOVGOROD: TECH_STARTERS[0]
        + [
            Technology.MONASTICISM,
            Technology.VASSALAGE,
            Technology.FARRIERS,
            Technology.CHAIN_MAIL,
        ],
        Civ.NORWAY: TECH_STARTERS[0]
        + [
            Technology.VASSALAGE,
            Technology.ASTROLABE,
            Technology.FARRIERS,
            Technology.CHAIN_MAIL,
            Technology.HERBAL_MEDICINE,
        ],
        Civ.KIEV: TECH_STARTERS[0]
        + [
            Technology.MONASTICISM,
            Technology.VASSALAGE,
            Technology.FARRIERS,
            Technology.CHAIN_MAIL,
        ],
        Civ.HUNGARY: TECH_STARTERS[0]
        + [
            Technology.CHAIN_MAIL,
            Technology.HERBAL_MEDICINE,
            Technology.VASSALAGE,
        ],
        Civ.CASTILE: TECH_STARTERS[0]
        + [
            Technology.LATEEN_SAILS,
            Technology.ASTROLABE,
            Technology.MONASTICISM,
            Technology.ART,
            Technology.HERBAL_MEDICINE,
            Technology.VASSALAGE,
            Technology.ENGINEERING,
            Technology.MACHINERY,
            Technology.FEUDALISM,
            Technology.CHAIN_MAIL,
        ],
        Civ.DENMARK: TECH_STARTERS[0]
        + [
            Technology.MONASTICISM,
            Technology.VASSALAGE,
            Technology.FEUDALISM,
            Technology.ARISTOCRACY,
            Technology.CODE_OF_LAWS,
            Technology.ASTROLABE,
            Technology.FARRIERS,
            Technology.CHAIN_MAIL,
            Technology.HERBAL_MEDICINE,
        ],
        Civ.SCOTLAND: TECH_STARTERS[0]
        + [
            Technology.LATEEN_SAILS,
            Technology.ASTROLABE,
            Technology.MONASTICISM,
            Technology.ART,
            Technology.MUSIC,
            Technology.HERBAL_MEDICINE,
            Technology.VASSALAGE,
            Technology.ENGINEERING,
            Technology.MACHINERY,
            Technology.FEUDALISM,
            Technology.CHAIN_MAIL,
            Technology.ARISTOCRACY,
        ],
        Civ.POLAND: TECH_STARTERS[0]
        + [
            Technology.MONASTICISM,
            Technology.HERBAL_MEDICINE,
            Technology.VASSALAGE,
            Technology.FEUDALISM,
            Technology.FARRIERS,
            Technology.ART,
            Technology.ENGINEERING,
            Technology.CHAIN_MAIL,
        ],
        Civ.GENOA: TECH_STARTERS[0]
        + [
            Technology.LATEEN_SAILS,
            Technology.ASTROLABE,
            Technology.MONASTICISM,
            Technology.ART,
            Technology.MUSIC,
            Technology.HERBAL_MEDICINE,
            Technology.VASSALAGE,
            Technology.CODE_OF_LAWS,
            Technology.ENGINEERING,
            Technology.MACHINERY,
            Technology.FEUDALISM,
            Technology.VAULTED_ARCHES,
            Technology.CHAIN_MAIL,
            Technology.ARISTOCRACY,
        ],
        Civ.MOROCCO: TECH_STARTERS[1]
        + [
            Technology.BLAST_FURNACE,
            Technology.CODE_OF_LAWS,
            Technology.LATEEN_SAILS,
            Technology.MAPMAKING,
            Technology.LITERATURE,
            Technology.ARABIC_KNOWLEDGE,
        ],
        Civ.ENGLAND: TECH_STARTERS[1]
        + [
            Technology.BLAST_FURNACE,
            Technology.CODE_OF_LAWS,
            Technology.ARISTOCRACY,
        ],
        Civ.PORTUGAL: TECH_STARTERS[1]
        + [
            Technology.BLAST_FURNACE,
            Technology.CODE_OF_LAWS,
            Technology.LITERATURE,
            Technology.LATEEN_SAILS,
            Technology.MAPMAKING,
            Technology.ARISTOCRACY,
        ],
        Civ.ARAGON: TECH_STARTERS[1]
        + [
            Technology.BLAST_FURNACE,
            Technology.CODE_OF_LAWS,
            Technology.LITERATURE,
            Technology.LATEEN_SAILS,
            Technology.MAPMAKING,
            Technology.ARISTOCRACY,
            Technology.PLATE_ARMOR,
            Technology.GOTHIC_ARCHITECTURE,
            Technology.SIEGE_ENGINES,
        ],
        Civ.SWEDEN: TECH_STARTERS[1]
        + [
            Technology.BLAST_FURNACE,
            Technology.CODE_OF_LAWS,
            Technology.GOTHIC_ARCHITECTURE,
            Technology.CHIVALRY,
            Technology.ARISTOCRACY,
            Technology.PLATE_ARMOR,
            Technology.SIEGE_ENGINES,
            Technology.LATEEN_SAILS,
            Technology.LITERATURE,
            Technology.CLASSICAL_KNOWLEDGE,
            Technology.MONUMENT_BUILDING,
            Technology.PHILOSOPHY,
            Technology.MAPMAKING,
        ],
        Civ.PRUSSIA: TECH_STARTERS[1]
        + [
            Technology.BLAST_FURNACE,
            Technology.CODE_OF_LAWS,
            Technology.GOTHIC_ARCHITECTURE,
            Technology.CHIVALRY,
            Technology.ARISTOCRACY,
            Technology.PLATE_ARMOR,
            Technology.SIEGE_ENGINES,
            Technology.ALCHEMY,
            Technology.CIVIL_SERVICE,
            Technology.LATEEN_SAILS,
            Technology.GUILDS,
            Technology.LITERATURE,
            Technology.CLASSICAL_KNOWLEDGE,
            Technology.MONUMENT_BUILDING,
            Technology.PHILOSOPHY,
        ],
        Civ.LITHUANIA: TECH_STARTERS[1]
        + [
            Technology.BLAST_FURNACE,
            Technology.CODE_OF_LAWS,
            Technology.GOTHIC_ARCHITECTURE,
            Technology.ARISTOCRACY,
            Technology.CIVIL_SERVICE,
            Technology.SIEGE_ENGINES,
            Technology.LITERATURE,
            Technology.ALCHEMY,
            Technology.CLASSICAL_KNOWLEDGE,
            Technology.PLATE_ARMOR,
            Technology.LATEEN_SAILS,
            Technology.MONUMENT_BUILDING,
            Technology.CIVIL_SERVICE,
        ],
        Civ.AUSTRIA: TECH_STARTERS[1]
        + [
            Technology.BLAST_FURNACE,
            Technology.CODE_OF_LAWS,
            Technology.GOTHIC_ARCHITECTURE,
            Technology.CHIVALRY,
            Technology.ARISTOCRACY,
            Technology.PLATE_ARMOR,
            Technology.SIEGE_ENGINES,
            Technology.ALCHEMY,
            Technology.CIVIL_SERVICE,
            Technology.LATEEN_SAILS,
            Technology.GUILDS,
            Technology.LITERATURE,
            Technology.CLASSICAL_KNOWLEDGE,
            Technology.MONUMENT_BUILDING,
            Technology.PHILOSOPHY,
            Technology.EDUCATION,
        ],
        Civ.OTTOMAN: TECH_STARTERS[2]
        + [
            Technology.GUNPOWDER,
            Technology.MILITARY_TRADITION,
            Technology.ARABIC_KNOWLEDGE,
        ],
        Civ.MOSCOW: TECH_STARTERS[1]
        + [
            Technology.BLAST_FURNACE,
            Technology.CODE_OF_LAWS,
            Technology.GOTHIC_ARCHITECTURE,
            Technology.CHIVALRY,
            Technology.ARISTOCRACY,
            Technology.CIVIL_SERVICE,
            Technology.LITERATURE,
            Technology.MONUMENT_BUILDING,
            Technology.PLATE_ARMOR,
            Technology.SIEGE_ENGINES,
            Technology.LATEEN_SAILS,
            Technology.MAPMAKING,
            Technology.CLASSICAL_KNOWLEDGE,
            Technology.CLOCKMAKING,
            Technology.ALCHEMY,
            Technology.GUILDS,
            Technology.PHILOSOPHY,
            Technology.REPLACEABLE_PARTS,
        ],
        Civ.DUTCH: TECH_STARTERS[3],
    }
)

CIV_SCENARIO_CONDITION_500AD = CivDataMapper(
    {
        Civ.BYZANTIUM: {
            InitialCondition.WORKERS: 0,
            InitialCondition.GOLD: 1200,
            InitialCondition.FAITH: 0,
        },
        Civ.FRANCE: {
            InitialCondition.WORKERS: 0,
            InitialCondition.GOLD: 100,
            InitialCondition.FAITH: 0,
        },
        Civ.ARABIA: {
            InitialCondition.WORKERS: 1,
            InitialCondition.GOLD: 200,
            InitialCondition.FAITH: 0,
        },
        Civ.BULGARIA: {
            InitialCondition.WORKERS: 1,
            InitialCondition.GOLD: 100,
            InitialCondition.FAITH: 0,
        },
        Civ.CORDOBA: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 200,
            InitialCondition.FAITH: 0,
        },
        Civ.VENECIA: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 0,
        },
        Civ.BURGUNDY: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 250,
            InitialCondition.FAITH: 0,
        },
        Civ.GERMANY: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 0,
        },
        Civ.NOVGOROD: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 0,
        },
        Civ.NORWAY: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 250,
            InitialCondition.FAITH: 0,
        },
        Civ.KIEV: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 250,
            InitialCondition.FAITH: 0,
        },
        Civ.HUNGARY: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 0,
        },
        Civ.CASTILE: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 500,
            InitialCondition.FAITH: 0,
        },
        Civ.DENMARK: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 0,
        },
        Civ.SCOTLAND: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 0,
        },
        Civ.POLAND: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 0,
        },
        Civ.GENOA: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 0,
        },
        Civ.MOROCCO: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 0,
        },
        Civ.ENGLAND: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 0,
        },
        Civ.PORTUGAL: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 450,
            InitialCondition.FAITH: 0,
        },
        Civ.ARAGON: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 450,
            InitialCondition.FAITH: 0,
        },
        Civ.SWEDEN: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 0,
        },
        Civ.PRUSSIA: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 0,
        },
        Civ.LITHUANIA: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 0,
        },
        Civ.AUSTRIA: {
            InitialCondition.WORKERS: 4,
            InitialCondition.GOLD: 1000,
            InitialCondition.FAITH: 0,
        },
        Civ.OTTOMAN: {
            InitialCondition.WORKERS: 4,
            InitialCondition.GOLD: 1000,
            InitialCondition.FAITH: 0,
        },
        Civ.MOSCOW: {
            InitialCondition.WORKERS: 4,
            InitialCondition.GOLD: 500,
            InitialCondition.FAITH: 0,
        },
        Civ.DUTCH: {
            InitialCondition.WORKERS: 4,
            InitialCondition.GOLD: 1500,
            InitialCondition.FAITH: 0,
        },
        Civ.POPE: {
            InitialCondition.WORKERS: 0,
            InitialCondition.GOLD: 50,
            InitialCondition.FAITH: 0,
        },
    }
)

CIV_SCENARIO_CONDITION_1200AD = CivDataMapper(
    {
        Civ.BYZANTIUM: {
            InitialCondition.WORKERS: 0,
            InitialCondition.GOLD: 750,
            InitialCondition.FAITH: 40,
        },
        Civ.FRANCE: {
            InitialCondition.WORKERS: 0,
            InitialCondition.GOLD: 250,
            InitialCondition.FAITH: 30,
        },
        Civ.ARABIA: {
            InitialCondition.WORKERS: 1,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 50,
        },
        Civ.BULGARIA: {
            InitialCondition.WORKERS: 1,
            InitialCondition.GOLD: 150,
            InitialCondition.FAITH: 50,
        },
        Civ.CORDOBA: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 0,
            InitialCondition.FAITH: 0,
        },
        Civ.VENECIA: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 500,
            InitialCondition.FAITH: 25,
        },
        Civ.BURGUNDY: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 0,
            InitialCondition.FAITH: 0,
        },
        Civ.GERMANY: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 30,
        },
        Civ.NOVGOROD: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 25,
        },
        Civ.NORWAY: {
            InitialCondition.WORKERS: 2,
            InitialCondition.GOLD: 250,
            InitialCondition.FAITH: 0,
        },
        Civ.KIEV: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 250,
            InitialCondition.FAITH: 20,
        },
        Civ.HUNGARY: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 25,
        },
        Civ.CASTILE: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 500,
            InitialCondition.FAITH: 35,
        },
        Civ.DENMARK: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 20,
        },
        Civ.SCOTLAND: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 20,
        },
        Civ.POLAND: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 30,
        },
        Civ.GENOA: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 500,
            InitialCondition.FAITH: 25,
        },
        Civ.MOROCCO: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 35,
        },
        Civ.ENGLAND: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 20,
        },
        Civ.PORTUGAL: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 450,
            InitialCondition.FAITH: 20,
        },
        Civ.ARAGON: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 450,
            InitialCondition.FAITH: 10,
        },
        Civ.SWEDEN: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 0,
        },
        Civ.PRUSSIA: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 300,
            InitialCondition.FAITH: 0,
        },
        Civ.LITHUANIA: {
            InitialCondition.WORKERS: 3,
            InitialCondition.GOLD: 400,
            InitialCondition.FAITH: 0,
        },
        Civ.AUSTRIA: {
            InitialCondition.WORKERS: 4,
            InitialCondition.GOLD: 1000,
            InitialCondition.FAITH: 0,
        },
        Civ.OTTOMAN: {
            InitialCondition.WORKERS: 4,
            InitialCondition.GOLD: 1000,
            InitialCondition.FAITH: 0,
        },
        Civ.MOSCOW: {
            InitialCondition.WORKERS: 4,
            InitialCondition.GOLD: 500,
            InitialCondition.FAITH: 0,
        },
        Civ.DUTCH: {
            InitialCondition.WORKERS: 4,
            InitialCondition.GOLD: 1500,
            InitialCondition.FAITH: 0,
        },
        Civ.POPE: {
            InitialCondition.WORKERS: 0,
            InitialCondition.GOLD: 200,
            InitialCondition.FAITH: 0,
        },
    }
)

CIV_SCENARIO_CONDITION = ScenarioDataMapper(
    {
        Scenario.i500AD: CIV_SCENARIO_CONDITION_500AD,
        Scenario.i1200AD: CIV_SCENARIO_CONDITION_1200AD,
    }
)

# Used by GameBalance
CIV_INITIAL_BUILDINGS = CivDataMapper(
    {
        Civ.BYZANTIUM: None,
        Civ.FRANCE: None,
        Civ.ARABIA: None,
        Civ.BULGARIA: None,
        Civ.CORDOBA: None,
        Civ.VENECIA: [Building.HARBOR, Building.GRANARY],
        Civ.BURGUNDY: None,
        Civ.GERMANY: None,
        Civ.NOVGOROD: None,
        Civ.NORWAY: None,
        Civ.KIEV: None,
        Civ.HUNGARY: None,
        Civ.CASTILE: [Building.BARRACKS],
        Civ.DENMARK: [Building.BARRACKS],
        Civ.SCOTLAND: [Building.BARRACKS],
        Civ.POLAND: None,
        Civ.GENOA: [
            Building.GRANARY,
            Building.BARRACKS,
            Building.HARBOR,
        ],
        Civ.MOROCCO: [
            Building.GRANARY,
            Building.BARRACKS,
        ],
        Civ.ENGLAND: [
            Building.GRANARY,
            Building.BARRACKS,
        ],
        Civ.PORTUGAL: [
            Building.GRANARY,
            Building.BARRACKS,
        ],
        Civ.ARAGON: [
            Building.GRANARY,
            Building.BARRACKS,
            Building.HARBOR,
        ],
        Civ.SWEDEN: [
            Building.GRANARY,
            Building.BARRACKS,
            Building.FORGE,
        ],
        Civ.PRUSSIA: [
            Building.GRANARY,
            Building.BARRACKS,
        ],
        Civ.LITHUANIA: [
            Building.GRANARY,
            Building.BARRACKS,
        ],
        Civ.AUSTRIA: [
            Building.GRANARY,
            Building.BARRACKS,
            Building.FORGE,
        ],
        Civ.OTTOMAN: [
            Building.GRANARY,
            Building.BARRACKS,
            Building.FORGE,
            Building.HARBOR,
        ],
        Civ.MOSCOW: [
            Building.GRANARY,
            Building.BARRACKS,
            Building.FORGE,
            Building.MARKET,
        ],
        Civ.DUTCH: [
            Building.GRANARY,
            Building.BARRACKS,
            Building.FORGE,
            Building.HARBOR,
            Building.AQUEDUCT,
            Building.MARKET,
            Building.LIGHTHOUSE,
            Building.THEATRE,
            Building.SMOKEHOUSE,
        ],
        Civ.POPE: None,
    }
)

# Used by GameBalance
CIV_HUMAN_MODIFIERS = CivDataMapper(
    {
        Civ.BYZANTIUM: EnumDataMapper(
            {
                Modifier.GROWTH: (150, 100, 200, 100, 100, 2),
                Modifier.PRODUCTION: (200, 150, 200, 350),
                Modifier.SUPPORT: (50, 150, 70, 50, 120),
            },
            do_not_cast=True,
        ),
        Civ.FRANCE: EnumDataMapper(
            {
                Modifier.GROWTH: (110, 100, 110, 100, 100, 1),
                Modifier.PRODUCTION: (150, 120, 125, 130),
                Modifier.SUPPORT: (30, 120, 70, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.ARABIA: EnumDataMapper(
            {
                Modifier.GROWTH: (150, 100, 150, 100, 100, 1),
                Modifier.PRODUCTION: (150, 125, 150, 230),
                Modifier.SUPPORT: (30, 150, 70, 40, 120),
            },
            do_not_cast=True,
        ),
        Civ.BULGARIA: EnumDataMapper(
            {
                Modifier.GROWTH: (125, 100, 100, 100, 100, 1),
                Modifier.PRODUCTION: (150, 150, 125, 200),
                Modifier.SUPPORT: (40, 150, 80, 50, 120),
            },
            do_not_cast=True,
        ),
        Civ.CORDOBA: EnumDataMapper(
            {
                Modifier.GROWTH: (150, 100, 100, 100, 100, 1),
                Modifier.PRODUCTION: (200, 180, 140, 230),
                Modifier.SUPPORT: (40, 150, 70, 40, 120),
            },
            do_not_cast=True,
        ),
        Civ.VENECIA: EnumDataMapper(
            {
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (100, 100, 100, 130),
                Modifier.SUPPORT: (20, 100, 60, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.BURGUNDY: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (150, 120, 120, 150),
                Modifier.SUPPORT: (30, 120, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.GERMANY: EnumDataMapper(
            {
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (140, 140, 125, 130),
                Modifier.SUPPORT: (20, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.NOVGOROD: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (125, 125, 125, 150),
                Modifier.SUPPORT: (30, 120, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.NORWAY: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (125, 125, 100, 140),
                Modifier.SUPPORT: (20, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.KIEV: EnumDataMapper(
            {
                Modifier.GROWTH: (150, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (125, 150, 125, 150),
                Modifier.SUPPORT: (30, 120, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.HUNGARY: EnumDataMapper(
            {
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (125, 125, 100, 130),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.CASTILE: EnumDataMapper(
            {
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (125, 100, 100, 120),
                Modifier.SUPPORT: (20, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.DENMARK: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (100, 100, 100, 120),
                Modifier.SUPPORT: (20, 100, 80, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.SCOTLAND: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (110, 110, 110, 125),
                Modifier.SUPPORT: (25, 100, 80, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.POLAND: EnumDataMapper(
            {
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (120, 120, 120, 130),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.GENOA: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (100, 100, 100, 125),
                Modifier.SUPPORT: (20, 100, 60, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.MOROCCO: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (120, 120, 120, 175),
                Modifier.SUPPORT: (25, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.ENGLAND: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (100, 100, 100, 110),
                Modifier.SUPPORT: (20, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.PORTUGAL: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 150, 100, 100, 100, 3),
                Modifier.PRODUCTION: (80, 90, 100, 100),
                Modifier.SUPPORT: (20, 100, 70, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.ARAGON: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 150, 100, 100, 100, 3),
                Modifier.PRODUCTION: (80, 100, 100, 125),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.SWEDEN: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (80, 80, 100, 100),
                Modifier.SUPPORT: (20, 90, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.PRUSSIA: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (75, 80, 120, 100),
                Modifier.SUPPORT: (20, 90, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.LITHUANIA: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (80, 100, 110, 100),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.AUSTRIA: EnumDataMapper(
            {
                # Austria is squashed by other's culture, they need the boost
                Modifier.GROWTH: (100, 150, 100, 100, 100, 3),
                Modifier.PRODUCTION: (80, 80, 100, 100),
                Modifier.SUPPORT: (20, 80, 80, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.OTTOMAN: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 150, 100, 100, 100, 3),
                Modifier.PRODUCTION: (75, 75, 100, 110),
                Modifier.SUPPORT: (30, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.MOSCOW: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (110, 110, 100, 120),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.DUTCH: EnumDataMapper(
            {
                Modifier.GROWTH: (100, 200, 60, 100, 50, 4),
                Modifier.PRODUCTION: (90, 50, 60, 50),
                Modifier.SUPPORT: (20, 70, 80, 50, 100),
            },
            do_not_cast=True,
        ),
    }
).fill_missing_members(EnumDataMapper({}))

# Used by GameBalance
CIV_AI_MODIFIERS = CivDataMapper(
    {
        Civ.BYZANTIUM: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 3, 0),  # 7
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.ST_CATHERINE_MONASTERY, 15),
                    (Wonder.BOYANA_CHURCH, 2),
                    (Wonder.ROUND_CHURCH, 2),
                    (Wonder.SOPHIA_KIEV, 5),
                ],
                Modifier.GROWTH: (200, 100, 200, 100, 100, 2),
                Modifier.PRODUCTION: (200, 200, 200, 350),
                Modifier.SUPPORT: (50, 150, 70, 50, 120),
            },
            do_not_cast=True,
        ),
        Civ.FRANCE: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 3, 0),  # 8
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.NOTRE_DAME, 20),
                    (Wonder.VERSAILLES, 20),
                    (Wonder.FONTAINEBLEAU, 10),
                    (Wonder.MONASTERY_OF_CLUNY, 10),
                    (Wonder.MONT_SAINT_MICHEL, 10),
                    (Wonder.PALAIS_DES_PAPES, 5),
                    (Wonder.LOUVRE, 20),
                ],
                Modifier.GROWTH: (110, 100, 110, 100, 100, 1),
                Modifier.PRODUCTION: (140, 120, 125, 150),
                Modifier.SUPPORT: (30, 120, 70, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.ARABIA: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 3, 1),  # 7
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.DOME_ROCK, 15),
                    (Wonder.TOMB_AL_WALID, 20),
                    (Wonder.ALAZHAR, 20),
                    (Wonder.MOSQUE_OF_KAIROUAN, 10),
                    (Wonder.KOUTOUBIA_MOSQUE, 5),
                    (Wonder.GARDENS_AL_ANDALUS, 5),
                    (Wonder.LA_MEZQUITA, 5),
                    (Wonder.ALHAMBRA, 5),
                    (Wonder.NOTRE_DAME, -5),
                    (Wonder.STEPHANSDOM, -5),
                    (Wonder.SISTINE_CHAPEL, -5),
                    (Wonder.KRAK_DES_CHEVALIERS, -5),
                    (Wonder.LEANING_TOWER, -3),
                    (Wonder.GOLDEN_BULL, -3),
                    (Wonder.COPERNICUS, -3),
                ],
                Modifier.GROWTH: (150, 100, 150, 100, 100, 1),
                Modifier.PRODUCTION: (130, 125, 150, 280),
                Modifier.SUPPORT: (30, 150, 70, 40, 120),
            },
            do_not_cast=True,
        ),
        Civ.BULGARIA: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 4),  # 11
                Modifier.CITY_WAR_DISTANCE: 1,
                Modifier.TECH_PREFERENCE: [
                    (Technology.BRONZE_CASTING, 200),
                ],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.ROUND_CHURCH, 20),
                    (Wonder.BOYANA_CHURCH, 20),
                    (Wonder.ST_CATHERINE_MONASTERY, 5),
                    (Wonder.SOPHIA_KIEV, 5),
                ],
                Modifier.GROWTH: (150, 100, 100, 100, 100, 1),
                Modifier.PRODUCTION: (130, 125, 125, 250),
                Modifier.SUPPORT: (40, 150, 80, 50, 120),
            },
            do_not_cast=True,
        ),
        Civ.CORDOBA: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 2, 1),  # 10
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.GARDENS_AL_ANDALUS, 20),
                    (Wonder.LA_MEZQUITA, 20),
                    (Wonder.ALHAMBRA, 20),
                    (Wonder.DOME_ROCK, 10),
                    (Wonder.ALAZHAR, 5),
                    (Wonder.MOSQUE_OF_KAIROUAN, 10),
                    (Wonder.KOUTOUBIA_MOSQUE, 5),
                    (Wonder.NOTRE_DAME, -5),
                    (Wonder.STEPHANSDOM, -5),
                    (Wonder.SISTINE_CHAPEL, -5),
                    (Wonder.KRAK_DES_CHEVALIERS, -5),
                    (Wonder.LEANING_TOWER, -3),
                    (Wonder.GOLDEN_BULL, -3),
                ],
                Modifier.GROWTH: (150, 100, 100, 100, 100, 1),
                Modifier.PRODUCTION: (180, 170, 130, 250),
                Modifier.SUPPORT: (40, 150, 70, 40, 120),
            },
            do_not_cast=True,
        ),
        Civ.VENECIA: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 1),  # 14
                Modifier.CITY_WAR_DISTANCE: 3,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.MARCO_POLO, 15),
                    (Wonder.SAN_MARCO, 20),
                    (Wonder.LANTERNA, 10),
                    (Wonder.LEONARDOS_WORKSHOP, 5),
                    (Wonder.LEANING_TOWER, 5),
                    (Wonder.GRAND_ARSENAL, 20),
                    (Wonder.GALATA_TOWER, 10),
                    (Wonder.FLORENCE_DUOMO, 10),
                    (Wonder.SAN_GIORGIO, 5),
                ],
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (100, 100, 100, 150),
                Modifier.SUPPORT: (20, 100, 60, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.BURGUNDY: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 3),  # 12
                Modifier.CITY_WAR_DISTANCE: 1,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.MONASTERY_OF_CLUNY, 20),
                    (Wonder.NOTRE_DAME, 10),
                    (Wonder.VERSAILLES, 10),
                    (Wonder.MONT_SAINT_MICHEL, 10),
                    (Wonder.FONTAINEBLEAU, 5),
                    (Wonder.PALAIS_DES_PAPES, 5),
                    (Wonder.LOUVRE, 10),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (130, 120, 120, 150),
                Modifier.SUPPORT: (30, 120, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.GERMANY: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 4),  # 11
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [
                    (Technology.PRINTING_PRESS, 200),
                ],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.BRANDENBURG_GATE, 10),
                    (Wonder.IMPERIAL_DIET, 20),
                    (Wonder.COPERNICUS, 5),
                    (Wonder.GOLDEN_BULL, 10),
                    (Wonder.MONASTERY_OF_CLUNY, 5),
                    (Wonder.URANIBORG, 5),
                    (Wonder.THOMASKIRCHE, 20),
                ],
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (120, 120, 100, 140),
                Modifier.SUPPORT: (20, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.NOVGOROD: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 3, 2),  # 6
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.ST_BASIL, 10),
                    (Wonder.SOPHIA_KIEV, 10),
                    (Wonder.ROUND_CHURCH, 5),
                    (Wonder.BOYANA_CHURCH, 5),
                    (Wonder.BORGUND_STAVE_CHURCH, 5),
                    (Wonder.PETERHOF_PALACE, 15),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (120, 120, 120, 150),
                Modifier.SUPPORT: (30, 120, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.NORWAY: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 2, 1),  # 10
                Modifier.CITY_WAR_DISTANCE: 3,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.SHRINE_OF_UPPSALA, 20),
                    (Wonder.SAMOGITIAN_ALKAS, 5),
                    (Wonder.BORGUND_STAVE_CHURCH, 15),
                    (Wonder.URANIBORG, 10),
                    (Wonder.KALMAR_CASTLE, 5),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (125, 125, 125, 130),
                Modifier.SUPPORT: (20, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.KIEV: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 3, 2),  # 6
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.SOPHIA_KIEV, 20),
                    (Wonder.ST_BASIL, 5),
                    (Wonder.ROUND_CHURCH, 5),
                    (Wonder.BOYANA_CHURCH, 5),
                    (Wonder.PETERHOF_PALACE, 10),
                ],
                Modifier.GROWTH: (150, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (100, 120, 100, 140),
                Modifier.SUPPORT: (30, 120, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.HUNGARY: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 3),  # 12
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.PRESSBURG, 20),
                    (Wonder.GOLDEN_BULL, 20),
                    (Wonder.BIBLIOTHECA_CORVINIANA, 20),
                    (Wonder.KAZIMIERZ, 10),
                    (Wonder.COPERNICUS, 5),
                    (Wonder.STEPHANSDOM, 5),
                ],
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (120, 120, 100, 150),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.CASTILE: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 2, 1),  # 10
                Modifier.CITY_WAR_DISTANCE: 3,
                Modifier.TECH_PREFERENCE: [
                    (Technology.ASTRONOMY, 200),
                ],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.ESCORIAL, 20),
                    (Wonder.MAGELLANS_VOYAGE, 10),
                    (Wonder.TORRE_DEL_ORO, 20),
                    (Wonder.BELEM_TOWER, 10),
                ],
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (100, 100, 100, 130),
                Modifier.SUPPORT: (20, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.DENMARK: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 3),  # 12
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.KALMAR_CASTLE, 10),
                    (Wonder.SHRINE_OF_UPPSALA, 20),
                    (Wonder.SAMOGITIAN_ALKAS, 5),
                    (Wonder.BORGUND_STAVE_CHURCH, 15),
                    (Wonder.URANIBORG, 20),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (100, 100, 100, 110),
                Modifier.SUPPORT: (20, 100, 80, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.SCOTLAND: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 2),  # 13
                Modifier.CITY_WAR_DISTANCE: 1,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.MAGNA_CARTA, 10),
                    (Wonder.WESTMINSTER, 10),
                    (Wonder.MONASTERY_OF_CLUNY, 5),
                    (Wonder.BORGUND_STAVE_CHURCH, 5),
                    (Wonder.MONT_SAINT_MICHEL, 5),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (100, 100, 100, 125),
                Modifier.SUPPORT: (25, 100, 80, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.POLAND: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 3, 0),  # 8
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.PRESSBURG, 10),
                    (Wonder.COPERNICUS, 10),
                    (Wonder.GOLDEN_BULL, 5),
                    (Wonder.KAZIMIERZ, 15),
                    (Wonder.JASNA_GORA, 20),
                    (Wonder.BRANDENBURG_GATE, 5),
                ],
                Modifier.GROWTH: (125, 100, 100, 100, 100, 2),
                Modifier.PRODUCTION: (100, 120, 120, 140),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.GENOA: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 1),  # 14
                Modifier.CITY_WAR_DISTANCE: 3,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.SAN_GIORGIO, 20),
                    (Wonder.LANTERNA, 20),
                    (Wonder.LEONARDOS_WORKSHOP, 5),
                    (Wonder.LEANING_TOWER, 5),
                    (Wonder.SAN_MARCO, 5),
                    (Wonder.MARCO_POLO, 5),
                    (Wonder.GRAND_ARSENAL, 10),
                    (Wonder.GALATA_TOWER, 20),
                    (Wonder.FLORENCE_DUOMO, 10),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (100, 100, 100, 130),
                Modifier.SUPPORT: (20, 100, 60, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.MOROCCO: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 3, 2),  # 6
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.GARDENS_AL_ANDALUS, 10),
                    (Wonder.LA_MEZQUITA, 10),
                    (Wonder.ALHAMBRA, 10),
                    (Wonder.DOME_ROCK, 10),
                    (Wonder.ALAZHAR, 5),
                    (Wonder.MOSQUE_OF_KAIROUAN, 10),
                    (Wonder.KOUTOUBIA_MOSQUE, 20),
                    (Wonder.NOTRE_DAME, -5),
                    (Wonder.STEPHANSDOM, -5),
                    (Wonder.SISTINE_CHAPEL, -5),
                    (Wonder.KRAK_DES_CHEVALIERS, -5),
                    (Wonder.LEANING_TOWER, -3),
                    (Wonder.GOLDEN_BULL, -3),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (120, 120, 120, 175),
                Modifier.SUPPORT: (25, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.ENGLAND: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 2, 1),  # 10
                Modifier.CITY_WAR_DISTANCE: 3,
                Modifier.TECH_PREFERENCE: [
                    (Technology.PRINTING_PRESS, 150),
                ],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.MAGNA_CARTA, 20),
                    (Wonder.WESTMINSTER, 20),
                    (Wonder.MONASTERY_OF_CLUNY, 5),
                    (Wonder.URANIBORG, 5),
                    (Wonder.TORRE_DEL_ORO, 5),
                    (Wonder.BELEM_TOWER, 5),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (80, 80, 100, 120),
                Modifier.SUPPORT: (20, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.PORTUGAL: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 1),  # 14
                Modifier.CITY_WAR_DISTANCE: 3,
                Modifier.TECH_PREFERENCE: [
                    (Technology.ASTRONOMY, 200),
                ],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.BELEM_TOWER, 20),
                    (Wonder.PALACIO_DA_PENA, 20),
                    (Wonder.MAGELLANS_VOYAGE, 20),
                    (Wonder.TORRE_DEL_ORO, 10),
                ],
                Modifier.GROWTH: (100, 150, 100, 100, 100, 3),
                Modifier.PRODUCTION: (70, 90, 100, 110),
                Modifier.SUPPORT: (20, 100, 70, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.ARAGON: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 1),  # 14
                Modifier.CITY_WAR_DISTANCE: 3,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.MAGELLANS_VOYAGE, 10),
                    (Wonder.TORRE_DEL_ORO, 10),
                    (Wonder.ESCORIAL, 5),
                    (Wonder.BELEM_TOWER, 10),
                ],
                Modifier.GROWTH: (100, 150, 100, 100, 100, 3),
                Modifier.PRODUCTION: (75, 90, 100, 125),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.SWEDEN: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 2, 2),  # 9
                Modifier.CITY_WAR_DISTANCE: 3,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.KALMAR_CASTLE, 20),
                    (Wonder.SHRINE_OF_UPPSALA, 5),
                    (Wonder.BORGUND_STAVE_CHURCH, 15),
                    (Wonder.URANIBORG, 10),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (80, 80, 100, 100),
                Modifier.SUPPORT: (20, 90, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.PRUSSIA: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 1),  # 14
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.BRANDENBURG_GATE, 20),
                    (Wonder.THOMASKIRCHE, 10),
                    (Wonder.COPERNICUS, 5),
                    (Wonder.PRESSBURG, 5),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (60, 80, 120, 90),
                Modifier.SUPPORT: (20, 90, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.LITHUANIA: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 3, 0),  # 8
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.SAMOGITIAN_ALKAS, 20),
                    (Wonder.GEDIMINAS_TOWER, 20),
                    (Wonder.BORGUND_STAVE_CHURCH, 5),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (70, 100, 110, 110),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.AUSTRIA: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 3),  # 12
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.STEPHANSDOM, 20),
                    (Wonder.THOMASKIRCHE, 15),
                    (Wonder.COPERNICUS, 5),
                    (Wonder.GOLDEN_BULL, 5),
                    (Wonder.PRESSBURG, 5),
                    (Building.AUSTRIAN_OPERA_HOUSE, 10),
                ],
                # Austria is squashed by other's culture, they need the boost
                Modifier.GROWTH: (100, 200, 100, 100, 100, 3),
                Modifier.PRODUCTION: (50, 80, 100, 80),
                Modifier.SUPPORT: (20, 80, 80, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.OTTOMAN: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 3, 1),  # 7
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.TOPKAPI_PALACE, 20),
                    (Wonder.BLUE_MOSQUE, 20),
                    (Wonder.SELIMIYE_MOSQUE, 20),
                    (Wonder.TOMB_AL_WALID, 10),
                    (Wonder.KIZIL_KULE, 10),
                    (Wonder.ALAZHAR, 5),
                ],
                Modifier.GROWTH: (100, 150, 100, 100, 100, 3),
                Modifier.PRODUCTION: (60, 75, 100, 120),
                Modifier.SUPPORT: (30, 100, 60, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.MOSCOW: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (1, 4, 1),  # 5
                Modifier.CITY_WAR_DISTANCE: 2,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.ST_BASIL, 20),
                    (Wonder.PETERHOF_PALACE, 20),
                    (Wonder.SOPHIA_KIEV, 5),
                ],
                Modifier.GROWTH: (100, 100, 100, 100, 100, 3),
                Modifier.PRODUCTION: (80, 80, 100, 120),
                Modifier.SUPPORT: (25, 100, 70, 40, 100),
            },
            do_not_cast=True,
        ),
        Civ.DUTCH: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: (2, 3, 1),  # 14
                Modifier.CITY_WAR_DISTANCE: 1,
                Modifier.TECH_PREFERENCE: [],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.BEURS, 20),
                    (Wonder.URANIBORG, 5),
                    (Wonder.THOMASKIRCHE, 5),
                ],
                Modifier.GROWTH: (100, 200, 60, 100, 50, 4),
                Modifier.PRODUCTION: (80, 50, 50, 50),
                Modifier.SUPPORT: (20, 70, 80, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.POPE: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: None,
                Modifier.CITY_WAR_DISTANCE: None,
                Modifier.TECH_PREFERENCE: [
                    (Technology.PRINTING_PRESS, 10),  # Pope shouldn't want this
                ],
                Modifier.BUILDING_PREFERENCE: [
                    (Wonder.SISTINE_CHAPEL, 20),
                    (Wonder.PALAIS_DES_PAPES, 10),
                    (Wonder.LEANING_TOWER, 5),
                    (Wonder.FLORENCE_DUOMO, 5),
                    (Wonder.LEONARDOS_WORKSHOP, 5),
                ],
                Modifier.GROWTH: (150, 100, 100, 50, 100, 1),
                Modifier.PRODUCTION: (300, 200, 100, 350),
                Modifier.SUPPORT: (20, 150, 80, 50, 100),
            },
            do_not_cast=True,
        ),
        Civ.INDEPENDENT: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: None,
                Modifier.CITY_WAR_DISTANCE: None,
                Modifier.TECH_PREFERENCE: [],
                Modifier.GROWTH: (100, 100, 100, 50, 100, 1),
                # The peaceful ones
                Modifier.PRODUCTION: (170, 100, 400, 200),
                Modifier.SUPPORT: (10, 100, 10, 20, 100),
            },
            do_not_cast=True,
        ),
        Civ.INDEPENDENT_2: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: None,
                Modifier.CITY_WAR_DISTANCE: None,
                Modifier.TECH_PREFERENCE: [],
                Modifier.GROWTH: (100, 100, 100, 50, 100, 1),
                # The peaceful ones
                Modifier.PRODUCTION: (170, 100, 400, 200),
                Modifier.SUPPORT: (10, 100, 10, 20, 100),
            },
            do_not_cast=True,
        ),
        Civ.INDEPENDENT_3: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: None,
                Modifier.CITY_WAR_DISTANCE: None,
                Modifier.TECH_PREFERENCE: [],
                Modifier.GROWTH: (100, 100, 100, 50, 100, 1),
                # The warlike ones
                Modifier.PRODUCTION: (125, 100, 600, 300),
                Modifier.SUPPORT: (10, 100, 10, 20, 100),
            },
            do_not_cast=True,
        ),
        Civ.INDEPENDENT_4: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: None,
                Modifier.CITY_WAR_DISTANCE: None,
                Modifier.TECH_PREFERENCE: [],
                Modifier.GROWTH: (100, 100, 100, 50, 100, 1),
                # The warlike ones
                Modifier.PRODUCTION: (125, 100, 600, 300),
                Modifier.SUPPORT: (10, 100, 10, 20, 100),
            },
            do_not_cast=True,
        ),
        Civ.BARBARIAN: EnumDataMapper(
            {
                Modifier.CITY_CLUSTER: None,
                Modifier.CITY_WAR_DISTANCE: None,
                Modifier.TECH_PREFERENCE: [],
                Modifier.GROWTH: (100, 100, 100, 50, 100, 1),
                Modifier.PRODUCTION: (125, 100, 900, 350),
                Modifier.SUPPORT: (10, 250, 10, 20, 100),
            },
            do_not_cast=True,
        ),
    }
)

CIV_STABILITY_AI_BONUS = CivDataMapper(
    {
        Civ.BYZANTIUM: 0,
        Civ.FRANCE: 4,
        Civ.ARABIA: 4,
        Civ.BULGARIA: 3,
        Civ.CORDOBA: 2,
        Civ.VENECIA: 3,
        Civ.BURGUNDY: 0,
        Civ.GERMANY: 0,
        Civ.NOVGOROD: 3,
        Civ.NORWAY: 0,
        Civ.KIEV: 6,
        Civ.HUNGARY: 2,
        Civ.CASTILE: 0,
        Civ.DENMARK: 0,
        Civ.SCOTLAND: 0,
        Civ.POLAND: 0,
        Civ.GENOA: 2,
        Civ.MOROCCO: 0,
        Civ.ENGLAND: 0,
        Civ.PORTUGAL: 0,
        Civ.ARAGON: 4,
        Civ.SWEDEN: 0,
        Civ.PRUSSIA: 3,
        Civ.LITHUANIA: 0,
        Civ.AUSTRIA: 4,
        Civ.OTTOMAN: 8,
        Civ.MOSCOW: 0,
        Civ.DUTCH: 0,
    }
)

CIV_INITIAL_CONTACTS_500AD = CivDataMapper(
    {
        Civ.BYZANTIUM: [
            Civ.POPE,
        ],
        Civ.ARABIA: [
            Civ.BYZANTIUM,
        ],
        Civ.BULGARIA: [
            Civ.BYZANTIUM,
        ],
        Civ.CORDOBA: [
            Civ.ARABIA,
        ],
        Civ.VENECIA: [
            Civ.BYZANTIUM,
            Civ.POPE,
        ],
        Civ.BURGUNDY: [
            Civ.FRANCE,
        ],
        Civ.GERMANY: [
            Civ.BURGUNDY,
            Civ.FRANCE,
        ],
        Civ.NOVGOROD: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
        ],
        Civ.KIEV: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.NOVGOROD,
        ],
        Civ.HUNGARY: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.KIEV,
        ],
        Civ.CASTILE: [
            Civ.FRANCE,
            Civ.BURGUNDY,
            Civ.CORDOBA,
        ],
        Civ.DENMARK: [
            Civ.NORWAY,
            Civ.GERMANY,
        ],
        Civ.SCOTLAND: [
            Civ.FRANCE,
            Civ.NORWAY,
        ],
        Civ.POLAND: [
            Civ.GERMANY,
            Civ.HUNGARY,
        ],
        Civ.GENOA: [
            Civ.BURGUNDY,
            Civ.BYZANTIUM,
            Civ.VENECIA,
            Civ.POPE,
        ],
        Civ.MOROCCO: [
            Civ.ARABIA,
            Civ.CASTILE,
            Civ.CORDOBA,
        ],
        Civ.ENGLAND: [
            Civ.FRANCE,
            Civ.DENMARK,
            Civ.SCOTLAND,
            Civ.NORWAY,
        ],
        Civ.PORTUGAL: [
            Civ.CASTILE,
            Civ.CORDOBA,
        ],
        Civ.ARAGON: [
            Civ.BURGUNDY,
            Civ.CASTILE,
            Civ.CORDOBA,
            Civ.FRANCE,
        ],
        Civ.SWEDEN: [
            Civ.DENMARK,
            Civ.NORWAY,
            Civ.NOVGOROD,
        ],
        Civ.PRUSSIA: [
            Civ.GERMANY,
            Civ.POLAND,
            Civ.NOVGOROD,
        ],
        Civ.LITHUANIA: [
            Civ.POLAND,
            Civ.KIEV,
            Civ.NOVGOROD,
            Civ.PRUSSIA,
        ],
        Civ.AUSTRIA: [
            Civ.GERMANY,
            Civ.VENECIA,
            Civ.POLAND,
            Civ.HUNGARY,
        ],
        Civ.OTTOMAN: [
            Civ.BYZANTIUM,
            Civ.ARABIA,
        ],
        Civ.MOSCOW: [
            Civ.KIEV,
            Civ.NOVGOROD,
            Civ.LITHUANIA,
        ],
        Civ.DUTCH: [
            Civ.ENGLAND,
            Civ.CASTILE,
            Civ.FRANCE,
            Civ.GERMANY,
            Civ.DENMARK,
            Civ.NORWAY,
        ],
    }
)

CIV_INITIAL_CONTACTS_1200AD = CivDataMapper(
    {
        Civ.BYZANTIUM: [
            Civ.POPE,
            Civ.VENECIA,
            Civ.GENOA,
            Civ.HUNGARY,
            Civ.BULGARIA,
            Civ.ARABIA,
            Civ.KIEV,
            Civ.NOVGOROD,
        ],
        Civ.FRANCE: [
            Civ.SCOTLAND,
            Civ.ENGLAND,
            Civ.NORWAY,
            Civ.ARAGON,
            Civ.CASTILE,
            Civ.GERMANY,
        ],
        Civ.ARABIA: [
            Civ.BYZANTIUM,
            Civ.MOROCCO,
        ],
        Civ.BULGARIA: [
            Civ.BYZANTIUM,
            Civ.KIEV,
            Civ.NOVGOROD,
            Civ.VENECIA,
            Civ.HUNGARY,
        ],
        Civ.VENECIA: [
            Civ.BYZANTIUM,
            Civ.GENOA,
            Civ.HUNGARY,
            Civ.POPE,
        ],
        Civ.GERMANY: [
            Civ.NORWAY,
            Civ.FRANCE,
            Civ.DENMARK,
            Civ.ENGLAND,
            Civ.POLAND,
            Civ.HUNGARY,
            Civ.VENECIA,
            Civ.GENOA,
            Civ.POPE,
        ],
        Civ.NOVGOROD: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.KIEV,
            Civ.POLAND,
        ],
        Civ.NORWAY: [
            Civ.DENMARK,
            Civ.ENGLAND,
            Civ.SCOTLAND,
            Civ.FRANCE,
        ],
        Civ.KIEV: [
            Civ.BYZANTIUM,
            Civ.HUNGARY,
            Civ.BULGARIA,
            Civ.NOVGOROD,
        ],
        Civ.HUNGARY: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.KIEV,
            Civ.VENECIA,
            Civ.GERMANY,
            Civ.POLAND,
            Civ.POPE,
        ],
        Civ.CASTILE: [
            Civ.MOROCCO,
            Civ.ARAGON,
            Civ.PORTUGAL,
            Civ.FRANCE,
            Civ.CORDOBA,
        ],
        Civ.DENMARK: [
            Civ.NORWAY,
            Civ.GERMANY,
            Civ.FRANCE,
            Civ.ENGLAND,
            Civ.POLAND,
        ],
        Civ.SCOTLAND: [
            Civ.NORWAY,
            Civ.GERMANY,
            Civ.FRANCE,
            Civ.ENGLAND,
        ],
        Civ.POLAND: [
            Civ.GERMANY,
            Civ.HUNGARY,
            Civ.DENMARK,
            Civ.KIEV,
            Civ.NOVGOROD,
        ],
        Civ.GENOA: [
            Civ.BYZANTIUM,
            Civ.FRANCE,
            Civ.VENECIA,
            Civ.GERMANY,
            Civ.POPE,
        ],
        Civ.MOROCCO: [
            Civ.ARABIA,
            Civ.CASTILE,
            Civ.ARAGON,
            Civ.PORTUGAL,
        ],
        Civ.ENGLAND: [
            Civ.FRANCE,
            Civ.DENMARK,
            Civ.SCOTLAND,
            Civ.NORWAY,
            Civ.POPE,
        ],
        Civ.PORTUGAL: [
            Civ.CASTILE,
            Civ.MOROCCO,
            Civ.ARAGON,
            Civ.POPE,
        ],
        Civ.ARAGON: [
            Civ.CASTILE,
            Civ.PORTUGAL,
            Civ.MOROCCO,
            Civ.GENOA,
            Civ.POPE,
        ],
        Civ.SWEDEN: [
            Civ.POLAND,
            Civ.GERMANY,
            Civ.DENMARK,
            Civ.NORWAY,
            Civ.NOVGOROD,
        ],
        Civ.PRUSSIA: [
            Civ.GERMANY,
            Civ.POLAND,
            Civ.NOVGOROD,
        ],
        Civ.LITHUANIA: [
            Civ.POLAND,
            Civ.KIEV,
            Civ.PRUSSIA,
        ],
        Civ.AUSTRIA: [
            Civ.GERMANY,
            Civ.VENECIA,
            Civ.POLAND,
            Civ.HUNGARY,
        ],
        Civ.OTTOMAN: [
            Civ.BYZANTIUM,
            Civ.HUNGARY,
            Civ.ARABIA,
        ],
        Civ.MOSCOW: [
            Civ.KIEV,
            Civ.NOVGOROD,
            Civ.SWEDEN,
            Civ.LITHUANIA,
        ],
        Civ.DUTCH: [
            Civ.ENGLAND,
            Civ.CASTILE,
            Civ.FRANCE,
            Civ.GERMANY,
            Civ.DENMARK,
            Civ.NORWAY,
            Civ.SWEDEN,
        ],
    }
)

CIV_INITIAL_CONTACTS = ScenarioDataMapper(
    {
        Scenario.i500AD: CIV_INITIAL_CONTACTS_500AD,
        Scenario.i1200AD: CIV_INITIAL_CONTACTS_1200AD,
    }
)

CIV_INITIAL_WARS_500AD = CivDataMapper(
    {
        Civ.BYZANTIUM: CivDataMapper(
            {
                Civ.ARABIA: 90,
                Civ.BULGARIA: 90,
                Civ.OTTOMAN: 90,
            },
            do_not_cast=True,
        ),
        Civ.FRANCE: CivDataMapper(
            {
                Civ.ENGLAND: 60,
            },
            do_not_cast=True,
        ),
        Civ.ARABIA: CivDataMapper(
            {
                Civ.OTTOMAN: 60,
            },
            do_not_cast=True,
        ),
        Civ.BULGARIA: CivDataMapper(
            {
                Civ.OTTOMAN: 70,
            },
            do_not_cast=True,
        ),
        Civ.CORDOBA: CivDataMapper(
            {
                Civ.CASTILE: 90,
                Civ.PORTUGAL: 90,
                Civ.ARAGON: 80,
            },
            do_not_cast=True,
        ),
        Civ.NOVGOROD: CivDataMapper(
            {
                Civ.PRUSSIA: 80,
            },
            do_not_cast=True,
        ),
        Civ.DENMARK: CivDataMapper(
            {
                Civ.SWEDEN: 60,
            },
            do_not_cast=True,
        ),
        Civ.SCOTLAND: CivDataMapper(
            {
                Civ.ENGLAND: 60,
            },
            do_not_cast=True,
        ),
        Civ.POLAND: CivDataMapper(
            {
                Civ.PRUSSIA: 20,
            },
            do_not_cast=True,
        ),
        Civ.PRUSSIA: CivDataMapper(
            {
                Civ.LITHUANIA: 80,
            },
            do_not_cast=True,
        ),
        Civ.OTTOMAN: CivDataMapper(
            {
                Civ.INDEPENDENT: 50,
                Civ.INDEPENDENT_2: 50,
                Civ.INDEPENDENT_3: 50,
                Civ.INDEPENDENT_4: 50,
            },
            do_not_cast=True,
        ),
    }
).fill_missing_members(CivDataMapper({}))

CIV_INITIAL_WARS_1200AD = CivDataMapper(
    {
        Civ.BYZANTIUM: CivDataMapper(
            {
                Civ.ARABIA: 20,
                Civ.BULGARIA: 70,
                Civ.VENECIA: 90,
                Civ.OTTOMAN: 90,
            },
            do_not_cast=True,
        ),
        Civ.FRANCE: CivDataMapper(
            {
                Civ.ARABIA: 30,
                Civ.ENGLAND: 90,
            },
            do_not_cast=True,
        ),
        Civ.ARABIA: CivDataMapper(
            {
                Civ.GERMANY: 20,
                Civ.HUNGARY: 20,
                Civ.CASTILE: 30,
                Civ.GENOA: 20,
                Civ.ENGLAND: 20,
                Civ.PORTUGAL: 20,
                Civ.ARAGON: 10,
                Civ.OTTOMAN: 60,
            },
            do_not_cast=True,
        ),
        Civ.BULGARIA: CivDataMapper(
            {
                Civ.OTTOMAN: 70,
            },
            do_not_cast=True,
        ),
        Civ.CORDOBA: CivDataMapper(
            {
                Civ.PORTUGAL: 90,
            },
            do_not_cast=True,
        ),
        Civ.NOVGOROD: CivDataMapper(
            {
                Civ.PRUSSIA: 80,
            },
            do_not_cast=True,
        ),
        Civ.DENMARK: CivDataMapper(
            {
                Civ.SWEDEN: 60,
            },
            do_not_cast=True,
        ),
        Civ.SCOTLAND: CivDataMapper(
            {
                Civ.ENGLAND: 60,
            },
            do_not_cast=True,
        ),
        Civ.POLAND: CivDataMapper(
            {
                Civ.PRUSSIA: 20,
            },
            do_not_cast=True,
        ),
        Civ.MOROCCO: CivDataMapper(
            {
                Civ.CASTILE: 90,
                Civ.PORTUGAL: 80,
                Civ.ARAGON: 80,
            },
            do_not_cast=True,
        ),
        Civ.PRUSSIA: CivDataMapper(
            {
                Civ.LITHUANIA: 80,
            },
            do_not_cast=True,
        ),
        Civ.OTTOMAN: CivDataMapper(
            {
                Civ.INDEPENDENT: 50,
                Civ.INDEPENDENT_2: 50,
                Civ.INDEPENDENT_3: 50,
                Civ.INDEPENDENT_4: 50,
            },
            do_not_cast=True,
        ),
    }
).fill_missing_members(CivDataMapper({}))

CIV_INITIAL_WARS = ScenarioDataMapper(
    {
        Scenario.i500AD: CIV_INITIAL_WARS_500AD,
        Scenario.i1200AD: CIV_INITIAL_WARS_1200AD,
    }
)

# Used for mercenaries (Higher number = less likely to hire)
CIV_HIRE_MERCENARY_THRESHOLD = CivDataMapper(
    {
        Civ.BYZANTIUM: 10,
        Civ.FRANCE: 30,
        Civ.ARABIA: 50,
        Civ.BULGARIA: 10,
        Civ.CORDOBA: 50,
        Civ.VENECIA: 30,
        Civ.BURGUNDY: 10,
        Civ.GERMANY: 70,
        Civ.NOVGOROD: 30,
        Civ.NORWAY: 60,
        Civ.KIEV: 40,
        Civ.HUNGARY: 10,
        Civ.CASTILE: 40,
        Civ.DENMARK: 30,
        Civ.SCOTLAND: 50,
        Civ.POLAND: 60,
        Civ.GENOA: 30,
        Civ.MOROCCO: 40,
        Civ.ENGLAND: 70,
        Civ.PORTUGAL: 40,
        Civ.ARAGON: 30,
        Civ.SWEDEN: 30,
        Civ.PRUSSIA: 50,
        Civ.LITHUANIA: 20,
        Civ.AUSTRIA: 20,
        Civ.OTTOMAN: 80,
        Civ.MOSCOW: 60,
        Civ.DUTCH: 30,
        Civ.POPE: 80,
        Civ.INDEPENDENT: 50,
        Civ.INDEPENDENT_2: 50,
        Civ.INDEPENDENT_3: 50,
        Civ.INDEPENDENT_4: 50,
        Civ.BARBARIAN: 50,
    }
)

# Used for war during rise and respawn of new civs (Higher number means less chance for war)
CIV_AI_STOP_BIRTH_THRESHOLD = CivDataMapper(
    {
        Civ.BYZANTIUM: 30,
        Civ.FRANCE: 60,
        Civ.ARABIA: 50,
        Civ.BULGARIA: 70,
        Civ.CORDOBA: 20,
        Civ.VENECIA: 50,
        Civ.BURGUNDY: 70,
        Civ.GERMANY: 80,
        Civ.NOVGOROD: 80,
        Civ.NORWAY: 70,
        Civ.KIEV: 80,
        Civ.HUNGARY: 60,
        Civ.CASTILE: 70,
        Civ.DENMARK: 40,
        Civ.SCOTLAND: 40,
        Civ.POLAND: 80,
        Civ.GENOA: 80,
        Civ.MOROCCO: 50,
        Civ.ENGLAND: 30,
        Civ.PORTUGAL: 60,
        Civ.ARAGON: 60,
        Civ.SWEDEN: 70,
        Civ.PRUSSIA: 30,
        Civ.LITHUANIA: 50,
        Civ.AUSTRIA: 50,
        Civ.OTTOMAN: 70,
        Civ.MOSCOW: 70,
        Civ.DUTCH: 80,
        Civ.POPE: 90,
    }
)

# Matrix determines how likely the AI is to switch to Protestantism
CIV_AI_REFORMATION_THRESHOLD = CivDataMapper(
    {
        Civ.BYZANTIUM: 20,
        Civ.FRANCE: 40,
        Civ.ARABIA: 40,
        Civ.BULGARIA: 20,
        Civ.CORDOBA: 40,
        Civ.VENECIA: 30,
        Civ.BURGUNDY: 50,
        Civ.GERMANY: 90,
        Civ.NOVGOROD: 30,
        Civ.NORWAY: 80,
        Civ.KIEV: 30,
        Civ.HUNGARY: 50,
        Civ.CASTILE: 10,
        Civ.DENMARK: 80,
        Civ.SCOTLAND: 80,
        Civ.POLAND: 30,
        Civ.GENOA: 20,
        Civ.MOROCCO: 40,
        Civ.ENGLAND: 80,
        Civ.PORTUGAL: 20,
        Civ.ARAGON: 30,
        Civ.SWEDEN: 90,
        Civ.PRUSSIA: 90,
        Civ.LITHUANIA: 30,
        Civ.AUSTRIA: 20,
        Civ.OTTOMAN: 40,
        Civ.MOSCOW: 30,
        Civ.DUTCH: 90,
        Civ.POPE: 0,
        Civ.INDEPENDENT: 40,
        Civ.INDEPENDENT_2: 40,
        Civ.INDEPENDENT_3: 40,
        Civ.INDEPENDENT_4: 40,
        Civ.BARBARIAN: 40,
    }
)

# Used to tune frequency of resurrections.
CIV_RESPAWNING_THRESHOLD = CivDataMapper(
    {
        Civ.BYZANTIUM: 30,
        Civ.FRANCE: 80,
        Civ.ARABIA: 60,
        Civ.BULGARIA: 30,
        Civ.CORDOBA: 20,
        Civ.VENECIA: 40,
        Civ.BURGUNDY: 20,
        Civ.GERMANY: 70,
        Civ.NOVGOROD: 20,
        Civ.NORWAY: 50,
        Civ.KIEV: 30,
        Civ.HUNGARY: 60,
        Civ.CASTILE: 80,
        Civ.DENMARK: 70,
        Civ.SCOTLAND: 40,
        Civ.POLAND: 60,
        Civ.GENOA: 30,
        Civ.MOROCCO: 60,
        Civ.ENGLAND: 70,
        Civ.PORTUGAL: 60,
        Civ.ARAGON: 20,
        Civ.SWEDEN: 70,
        Civ.PRUSSIA: 50,
        Civ.LITHUANIA: 50,
        Civ.AUSTRIA: 70,
        Civ.OTTOMAN: 70,
        Civ.MOSCOW: 80,
        Civ.DUTCH: 60,
        Civ.POPE: 90,
    }
)

CIV_RELIGION_SPREADING_THRESHOLD = CivDataMapper(
    {
        Civ.BYZANTIUM: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 100,
                Religion.ISLAM: 50,
                Religion.CATHOLICISM: 70,
                Religion.ORTHODOXY: 150,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.FRANCE: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 150,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 250,
                Religion.ORTHODOXY: 70,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.ARABIA: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 20,
                Religion.ISLAM: 350,
                Religion.CATHOLICISM: 50,
                Religion.ORTHODOXY: 10,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.BULGARIA: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 80,
                Religion.ISLAM: 50,
                Religion.CATHOLICISM: 80,
                Religion.ORTHODOXY: 400,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.CORDOBA: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 50,
                Religion.ISLAM: 250,
                Religion.CATHOLICISM: 80,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.VENECIA: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 90,
                Religion.ISLAM: 50,
                Religion.CATHOLICISM: 200,
                Religion.ORTHODOXY: 30,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.BURGUNDY: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 150,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 150,
                Religion.ORTHODOXY: 70,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.GERMANY: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 450,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 250,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.NOVGOROD: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 60,
                Religion.ISLAM: 40,
                Religion.CATHOLICISM: 60,
                Religion.ORTHODOXY: 500,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.NORWAY: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 250,
                Religion.ISLAM: 50,
                Religion.CATHOLICISM: 150,
                Religion.ORTHODOXY: 80,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.KIEV: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 90,
                Religion.ISLAM: 60,
                Religion.CATHOLICISM: 90,
                Religion.ORTHODOXY: 400,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.HUNGARY: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 250,
                Religion.ISLAM: 60,
                Religion.CATHOLICISM: 200,
                Religion.ORTHODOXY: 80,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.CASTILE: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 100,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 200,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.DENMARK: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 250,
                Religion.ISLAM: 50,
                Religion.CATHOLICISM: 180,
                Religion.ORTHODOXY: 80,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.SCOTLAND: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 450,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 100,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.POLAND: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 200,
                Religion.ISLAM: 60,
                Religion.CATHOLICISM: 450,
                Religion.ORTHODOXY: 200,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.GENOA: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 190,
                Religion.ISLAM: 50,
                Religion.CATHOLICISM: 250,
                Religion.ORTHODOXY: 30,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.MOROCCO: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 50,
                Religion.ISLAM: 250,
                Religion.CATHOLICISM: 70,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.ENGLAND: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 450,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 100,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.PORTUGAL: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 200,
                Religion.ISLAM: 80,
                Religion.CATHOLICISM: 250,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.ARAGON: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 150,
                Religion.ISLAM: 80,
                Religion.CATHOLICISM: 250,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.SWEDEN: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 450,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 200,
                Religion.ORTHODOXY: 50,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.PRUSSIA: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 450,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 250,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.LITHUANIA: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 80,
                Religion.ISLAM: 80,
                Religion.CATHOLICISM: 80,
                Religion.ORTHODOXY: 80,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.AUSTRIA: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 200,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 250,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.OTTOMAN: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 20,
                Religion.ISLAM: 350,
                Religion.CATHOLICISM: 80,
                Religion.ORTHODOXY: 80,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.MOSCOW: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 100,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 100,
                Religion.ORTHODOXY: 250,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.DUTCH: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 550,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 90,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.POPE: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 10,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 500,
                Religion.ORTHODOXY: 10,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.INDEPENDENT: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 250,
                Religion.ISLAM: 100,
                Religion.CATHOLICISM: 100,
                Religion.ORTHODOXY: 100,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.INDEPENDENT_2: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 250,
                Religion.ISLAM: 100,
                Religion.CATHOLICISM: 100,
                Religion.ORTHODOXY: 100,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.INDEPENDENT_3: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 250,
                Religion.ISLAM: 100,
                Religion.CATHOLICISM: 100,
                Religion.ORTHODOXY: 100,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.INDEPENDENT_4: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 250,
                Religion.ISLAM: 100,
                Religion.CATHOLICISM: 100,
                Religion.ORTHODOXY: 100,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
        Civ.BARBARIAN: ReligionDataMapper(
            {
                Religion.PROTESTANTISM: 20,
                Religion.ISLAM: 20,
                Religion.CATHOLICISM: 20,
                Religion.ORTHODOXY: 20,
                Religion.JUDAISM: 10,
            },
            do_not_cast=True,
        ),
    }
)

# 100 and 80: don't purge any religions; 60: purge islam if christian, and all christian religions if muslim; 40: also judaism; 20: all but state religion
CIV_RELIGIOUS_TOLERANCE = CivDataMapper(
    {
        Civ.BYZANTIUM: 60,
        Civ.FRANCE: 40,
        Civ.ARABIA: 60,
        Civ.BULGARIA: 40,
        Civ.CORDOBA: 80,
        Civ.VENECIA: 40,
        Civ.BURGUNDY: 20,
        Civ.GERMANY: 20,
        Civ.NOVGOROD: 60,
        Civ.NORWAY: 60,
        Civ.KIEV: 40,
        Civ.HUNGARY: 60,
        Civ.CASTILE: 20,
        Civ.DENMARK: 60,
        Civ.SCOTLAND: 40,
        Civ.POLAND: 80,
        Civ.GENOA: 20,
        Civ.MOROCCO: 60,
        Civ.ENGLAND: 40,
        Civ.PORTUGAL: 40,
        Civ.ARAGON: 60,
        Civ.SWEDEN: 60,
        Civ.PRUSSIA: 20,
        Civ.LITHUANIA: 80,
        Civ.AUSTRIA: 20,
        Civ.OTTOMAN: 80,
        Civ.MOSCOW: 40,
        Civ.DUTCH: 40,
        Civ.POPE: 20,
        Civ.INDEPENDENT: 100,
        Civ.INDEPENDENT_2: 100,
        Civ.INDEPENDENT_3: 100,
        Civ.INDEPENDENT_4: 100,
        Civ.BARBARIAN: 100,
    }
)

# Late leader: (leader, starting date, threshold, era)
CIV_LEADERS = CivDataMapper(
    {
        Civ.BYZANTIUM: {
            LeaderType.PRIMARY: Leader.JUSTINIAN,
            LeaderType.EARLY: Leader.JUSTINIAN,
            LeaderType.LATE: [
                (Leader.BASIL_II, DateTurn.i910AD, 10, 2),
                (Leader.PALAIOLOGOS, DateTurn.i1230AD, 5, 2),
            ],
        },
        Civ.FRANCE: {
            LeaderType.PRIMARY: Leader.CHARLEMAGNE,
            LeaderType.EARLY: Leader.CHARLEMAGNE,
            LeaderType.LATE: [
                (Leader.PHILIP_AUGUSTUS, DateTurn.i1101AD, 10, 2),
                (Leader.JOAN, DateTurn.i1376AD, 10, 2),
                (Leader.LOUIS_XIV, DateTurn.i1523AD, 25, 3),
            ],
        },
        Civ.ARABIA: {
            LeaderType.PRIMARY: Leader.ABU_BAKR,
            LeaderType.EARLY: Leader.ABU_BAKR,
            LeaderType.LATE: [
                (Leader.HARUN_AL_RASHID, DateTurn.i752AD, 25, 1),
                (Leader.SALADIN, DateTurn.i1160AD, 25, 2),
            ],
        },
        Civ.BULGARIA: {
            LeaderType.PRIMARY: Leader.SIMEON,
            LeaderType.EARLY: Leader.SIMEON,
            LeaderType.LATE: [
                (Leader.IVAN_ASEN, DateTurn.i1101AD, 10, 2),
            ],
        },
        Civ.CORDOBA: {
            LeaderType.PRIMARY: Leader.ABD_AR_RAHMAN,
            LeaderType.EARLY: Leader.ABD_AR_RAHMAN,
            LeaderType.LATE: [
                (Leader.MOHAMMED_IBN_NASR, DateTurn.i1202AD, 10, 2),
            ],
        },
        Civ.VENECIA: {
            LeaderType.PRIMARY: Leader.ENRICO_DANDOLO,
            LeaderType.EARLY: Leader.ENRICO_DANDOLO,
            LeaderType.LATE: [
                (Leader.ANDREA_GRITTI, DateTurn.i1259AD, 10, 2),
            ],
        },
        Civ.BURGUNDY: {
            LeaderType.PRIMARY: Leader.OTTO_WILLIAM,
            LeaderType.EARLY: Leader.OTTO_WILLIAM,
            LeaderType.LATE: [
                (Leader.BEATRICE, DateTurn.i1200AD, 10, 2),
                (Leader.PHILIP_THE_BOLD, DateTurn.i1356AD, 15, 2),
            ],
        },
        Civ.GERMANY: {
            LeaderType.PRIMARY: Leader.OTTO_I,
            LeaderType.EARLY: Leader.OTTO_I,
            LeaderType.LATE: [
                (Leader.BARBAROSSA, DateTurn.i1139AD, 20, 2),
            ],
        },
        Civ.NOVGOROD: {
            LeaderType.PRIMARY: Leader.RURIK,
            LeaderType.EARLY: Leader.RURIK,
            LeaderType.LATE: [
                (Leader.ALEXANDER_NEVSKY, DateTurn.i1150AD, 10, 2),
                (Leader.MARFA, DateTurn.i1380AD, 10, 3),
            ],
        },
        Civ.NORWAY: {
            LeaderType.PRIMARY: Leader.HARALD_HARDRADA,
            LeaderType.EARLY: Leader.HARALD_HARDRADA,
            LeaderType.LATE: [
                (Leader.HAAKON_IV, DateTurn.i1160AD, 25, 2),
            ],
        },
        Civ.KIEV: {
            LeaderType.PRIMARY: Leader.YAROSLAV,
            LeaderType.EARLY: Leader.YAROSLAV,
            LeaderType.LATE: [
                (Leader.MSTISLAV, DateTurn.i1101AD, 5, 2),
                (Leader.BOHDAN_KHMELNYTSKY, DateTurn.i1520AD, 10, 3),
            ],
        },
        Civ.HUNGARY: {
            LeaderType.PRIMARY: Leader.STEPHEN,
            LeaderType.EARLY: Leader.STEPHEN,
            LeaderType.LATE: [
                (Leader.BELA_III, DateTurn.i1167AD, 15, 2),
                (Leader.MATTHIAS, DateTurn.i1444AD, 5, 3),
            ],
        },
        Civ.CASTILE: {
            LeaderType.PRIMARY: Leader.FERDINAND_III,
            LeaderType.EARLY: Leader.FERDINAND_III,
            LeaderType.LATE: [
                (Leader.ISABELLA, DateTurn.i1250AD, 10, 2),
                (Leader.PHILIP_II, DateTurn.i1520AD, 10, 3),
            ],
        },
        Civ.DENMARK: {
            LeaderType.PRIMARY: Leader.HARALD_BLUETOOTH,
            LeaderType.EARLY: Leader.HARALD_BLUETOOTH,
            LeaderType.LATE: [
                (Leader.MARGARET_I, DateTurn.i1320AD, 10, 2),
                (Leader.CHRISTIAN_IV, DateTurn.i1520AD, 5, 3),
            ],
        },
        Civ.SCOTLAND: {
            LeaderType.PRIMARY: Leader.ROBERT_THE_BRUCE,
            LeaderType.EARLY: Leader.ROBERT_THE_BRUCE,
            LeaderType.LATE: [
                (Leader.JAMES_IV, DateTurn.i1296AD, 10, 2),
            ],
        },
        Civ.POLAND: {
            LeaderType.PRIMARY: Leader.MIESZKO,
            LeaderType.EARLY: Leader.MIESZKO,
            LeaderType.LATE: [
                (Leader.CASIMIR, DateTurn.i1320AD, 20, 2),
                (Leader.SOBIESKI, DateTurn.i1570AD, 10, 3),
            ],
        },
        Civ.GENOA: {
            LeaderType.PRIMARY: Leader.EMBRIACO,
            LeaderType.EARLY: Leader.EMBRIACO,
            LeaderType.LATE: [
                (Leader.BOCCANEGRA, DateTurn.i1101AD, 10, 2),
            ],
        },
        Civ.MOROCCO: {
            LeaderType.PRIMARY: Leader.YAQUB_AL_MANSUR,
            LeaderType.EARLY: Leader.YAQUB_AL_MANSUR,
            LeaderType.LATE: [
                (Leader.ISMAIL_IBN_SHARIF, DateTurn.i1419AD, 5, 3),
            ],
        },
        Civ.ENGLAND: {
            LeaderType.PRIMARY: Leader.WILLIAM,
            LeaderType.EARLY: Leader.WILLIAM,
            LeaderType.LATE: [
                (Leader.ELIZABETH, DateTurn.i1452AD, 10, 3),
                (Leader.GEORGE_III, DateTurn.i1700AD, 10, 3),
            ],
        },
        Civ.PORTUGAL: {
            LeaderType.PRIMARY: Leader.AFONSO,
            LeaderType.EARLY: Leader.AFONSO,
            LeaderType.LATE: [
                (Leader.JOAO, DateTurn.i1419AD, 10, 3),
                (Leader.MARIA_I, DateTurn.i1700AD, 10, 3),
            ],
        },
        Civ.ARAGON: {
            LeaderType.PRIMARY: Leader.JAMES_I,
            LeaderType.EARLY: Leader.JAMES_I,
            LeaderType.LATE: [
                (Leader.JOHN_II, DateTurn.i1397AD, 15, 3),
            ],
        },
        Civ.SWEDEN: {
            LeaderType.PRIMARY: Leader.MAGNUS_LADULAS,
            LeaderType.EARLY: Leader.MAGNUS_LADULAS,
            LeaderType.LATE: [
                (Leader.GUSTAV_VASA, DateTurn.i1470AD, 20, 3),
                (Leader.GUSTAV_ADOLF, DateTurn.i1540AD, 25, 3),
                (Leader.KARL_XII, DateTurn.i1680AD, 10, 3),
            ],
        },
        Civ.PRUSSIA: {
            LeaderType.PRIMARY: Leader.HERMANN_VON_SALZA,
            LeaderType.EARLY: Leader.HERMANN_VON_SALZA,
            LeaderType.LATE: [
                (Leader.FREDERICK, DateTurn.i1580AD, 5, 3),
            ],
        },
        Civ.LITHUANIA: {
            LeaderType.PRIMARY: Leader.MINDAUGAS,
            LeaderType.EARLY: Leader.MINDAUGAS,
            LeaderType.LATE: [
                (Leader.VYTAUTAS, DateTurn.i1377AD, 10, 3),
            ],
        },
        Civ.AUSTRIA: {
            LeaderType.PRIMARY: Leader.MAXIMILIAN,
            LeaderType.EARLY: Leader.MAXIMILIAN,
            LeaderType.LATE: [
                (Leader.MARIA_THERESA, DateTurn.i1700AD, 25, 3),
            ],
        },
        Civ.OTTOMAN: {
            LeaderType.PRIMARY: Leader.MEHMED,
            LeaderType.EARLY: Leader.MEHMED,
            LeaderType.LATE: [
                (Leader.SULEIMAN, DateTurn.i1520AD, 15, 3),
            ],
        },
        Civ.MOSCOW: {
            LeaderType.PRIMARY: Leader.IVAN_IV,
            LeaderType.EARLY: Leader.IVAN_IV,
            LeaderType.LATE: [
                (Leader.PETER, DateTurn.i1570AD, 10, 3),
                (Leader.CATHERINE, DateTurn.i1700AD, 25, 3),
            ],
        },
        Civ.DUTCH: {
            LeaderType.PRIMARY: Leader.WILLEM_VAN_ORANJE,
            LeaderType.EARLY: Leader.WILLEM_VAN_ORANJE,
            LeaderType.LATE: [
                (Leader.JOHAN_DE_WITT, DateTurn.i1650AD, 30, 3),
            ],
        },
        Civ.POPE: {
            LeaderType.PRIMARY: Leader.THE_POPE,
            LeaderType.EARLY: Leader.THE_POPE,
            LeaderType.LATE: None,
        },
    }
)

CIV_PROPERTIES = CivDataMapper(
    {
        Civ.POPE: {
            CivilizationProperty.IS_PLAYABLE: False,
            CivilizationProperty.IS_MINOR: False,
        },
        Civ.INDEPENDENT: {
            CivilizationProperty.IS_PLAYABLE: False,
            CivilizationProperty.IS_MINOR: True,
        },
        Civ.INDEPENDENT_2: {
            CivilizationProperty.IS_PLAYABLE: False,
            CivilizationProperty.IS_MINOR: True,
        },
        Civ.INDEPENDENT_3: {
            CivilizationProperty.IS_PLAYABLE: False,
            CivilizationProperty.IS_MINOR: True,
        },
        Civ.INDEPENDENT_4: {
            CivilizationProperty.IS_PLAYABLE: False,
            CivilizationProperty.IS_MINOR: True,
        },
        Civ.BARBARIAN: {
            CivilizationProperty.IS_PLAYABLE: False,
            CivilizationProperty.IS_MINOR: True,
        },
    }
).fill_missing_members(
    {
        CivilizationProperty.IS_PLAYABLE: True,
        CivilizationProperty.IS_MINOR: False,
    }
)
