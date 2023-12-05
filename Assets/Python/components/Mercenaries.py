# Rhye's and Fall of Civilization: Europe - Mercenaries
# Written mostly by 3Miro

from CvPythonExtensions import *
from CoreData import civilizations, civilization
from CoreFunctions import text
from CoreStructures import human, turn
from CoreTypes import Civ, Region, SpecialParameter, Religion, Promotion, Unit, Province
from LocationsData import REGIONS
import PyHelpers
from PyUtils import percentage_chance, rand, choice

# import cPickle as pickle
import RFCUtils
from StoredData import data

from Consts import MessageData

# globals
utils = RFCUtils.RFCUtils()
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
PyPlayer = PyHelpers.PyPlayer


# list of all available mercs, unit type, text key name, start turn, end turn, provinces, blocked by religions, odds
# note that the province list is treated as a set (only iProvince in list or Set(list) are ever called)
# the odds show the odds of the merc to appear every turn, this is nothing more than a delay on when the merc would appear (90-100 means right at the date, 10-30 should be good for most mercs)
lMercList = [
    [Unit.AXEMAN.value, "TXT_KEY_MERC_SERBIAN", 60, 108, REGIONS[Region.BALKANS], [], 20],
    [Unit.ARCHER.value, "TXT_KEY_MERC_SERBIAN", 60, 108, REGIONS[Region.BALKANS], [], 20],
    [
        Unit.HORSE_ARCHER.value,
        "TXT_KEY_MERC_KHAZAR",
        25,
        90,
        REGIONS[Region.BALKANS] + [Province.CONSTANTINOPLE.value],
        [],
        20,
    ],
    [
        Unit.HORSE_ARCHER.value,
        "TXT_KEY_MERC_KHAZAR",
        25,
        108,
        REGIONS[Region.BALKANS] + [Province.CONSTANTINOPLE.value],
        [],
        20,
    ],
    [
        Unit.HORSE_ARCHER.value,
        "TXT_KEY_MERC_AVAR",
        25,
        75,
        REGIONS[Region.BALKANS]
        + REGIONS[Region.AUSTRIA]
        + REGIONS[Region.HUNGARY]
        + [Province.CONSTANTINOPLE.value],
        [],
        20,
    ],
    [
        Unit.HORSE_ARCHER.value,
        "TXT_KEY_MERC_AVAR",
        25,
        75,
        REGIONS[Region.BALKANS]
        + REGIONS[Region.AUSTRIA]
        + REGIONS[Region.HUNGARY]
        + [Province.CONSTANTINOPLE.value],
        [],
        20,
    ],
    [Unit.MOUNTED_INFANTRY.value, "TXT_KEY_MERC_GENERIC", 50, 80, REGIONS[Region.FRANCE], [], 20],
    [Unit.MOUNTED_INFANTRY.value, "TXT_KEY_MERC_GENERIC", 50, 80, REGIONS[Region.GERMANY], [], 20],
    [Unit.MOUNTED_INFANTRY.value, "TXT_KEY_MERC_GENERIC", 50, 80, REGIONS[Region.IBERIA], [], 20],
    [Unit.ARCHER.value, "TXT_KEY_MERC_GENERIC", 50, 80, REGIONS[Region.FRANCE], [], 20],
    [Unit.ARCHER.value, "TXT_KEY_MERC_GENERIC", 50, 80, REGIONS[Region.GERMANY], [], 20],
    [Unit.ARCHER.value, "TXT_KEY_MERC_GENERIC", 50, 80, REGIONS[Region.IBERIA], [], 20],
    [Unit.CROSSBOWMAN.value, "TXT_KEY_MERC_GENERIC", 100, 200, REGIONS[Region.FRANCE], [], 20],
    [Unit.CROSSBOWMAN.value, "TXT_KEY_MERC_GENERIC", 100, 200, REGIONS[Region.GERMANY], [], 20],
    [Unit.CROSSBOWMAN.value, "TXT_KEY_MERC_GENERIC", 100, 200, REGIONS[Region.IBERIA], [], 20],
    [Unit.CROSSBOWMAN.value, "TXT_KEY_MERC_GENERIC", 100, 200, REGIONS[Region.BRITAIN], [], 20],
    [Unit.CROSSBOWMAN.value, "TXT_KEY_MERC_GENERIC", 100, 200, REGIONS[Region.POLAND], [], 20],
    [Unit.CROSSBOWMAN.value, "TXT_KEY_MERC_GENERIC", 100, 200, REGIONS[Region.HUNGARY], [], 20],
    [
        Unit.CROSSBOWMAN.value,
        "TXT_KEY_MERC_GENERIC",
        100,
        200,
        REGIONS[Region.MIDDLE_EAST],
        [],
        20,
    ],
    [Unit.LONGBOWMAN.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.FRANCE], [], 20],
    [Unit.LONGBOWMAN.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.GERMANY], [], 20],
    [Unit.LONGBOWMAN.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.IBERIA], [], 20],
    [Unit.LONGBOWMAN.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.BRITAIN], [], 20],
    [Unit.LONGBOWMAN.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.BALKANS], [], 20],
    [Unit.SPEARMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.FRANCE], [], 20],
    [Unit.SPEARMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.GERMANY], [], 20],
    [Unit.SPEARMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.IBERIA], [], 20],
    [Unit.SPEARMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.BRITAIN], [], 20],
    [Unit.SPEARMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.POLAND], [], 20],
    [Unit.SPEARMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.HUNGARY], [], 20],
    [Unit.SPEARMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.BALKANS], [], 20],
    [Unit.SPEARMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.KIEV], [], 20],
    [Unit.SPEARMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.MIDDLE_EAST], [], 20],
    [Unit.SWORDSMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.FRANCE], [], 20],
    [Unit.SWORDSMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.GERMANY], [], 20],
    [Unit.SWORDSMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.IBERIA], [], 20],
    [Unit.SWORDSMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.BRITAIN], [], 20],
    [Unit.SWORDSMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.POLAND], [], 20],
    [Unit.SWORDSMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.HUNGARY], [], 20],
    [Unit.SWORDSMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.BALKANS], [], 20],
    [Unit.SWORDSMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.KIEV], [], 20],
    [Unit.SWORDSMAN.value, "TXT_KEY_MERC_GENERIC", 50, 150, REGIONS[Region.MIDDLE_EAST], [], 20],
    [Unit.KNIGHT.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.FRANCE], [], 20],
    [Unit.KNIGHT.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.GERMANY], [], 20],
    [Unit.KNIGHT.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.IBERIA], [], 20],
    [Unit.KNIGHT.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.BRITAIN], [], 20],
    [Unit.KNIGHT.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.POLAND], [], 20],
    [Unit.KNIGHT.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.HUNGARY], [], 20],
    [Unit.KNIGHT.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.BALKANS], [], 20],
    [Unit.KNIGHT.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.KIEV], [], 20],
    [Unit.KNIGHT.value, "TXT_KEY_MERC_GENERIC", 200, 300, REGIONS[Region.MIDDLE_EAST], [], 20],
    [Unit.MUSKETMAN.value, "TXT_KEY_MERC_GENERIC", 300, 400, REGIONS[Region.FRANCE], [], 20],
    [Unit.MUSKETMAN.value, "TXT_KEY_MERC_GENERIC", 300, 400, REGIONS[Region.GERMANY], [], 20],
    [Unit.MUSKETMAN.value, "TXT_KEY_MERC_GENERIC", 300, 400, REGIONS[Region.IBERIA], [], 20],
    [Unit.MUSKETMAN.value, "TXT_KEY_MERC_GENERIC", 300, 400, REGIONS[Region.BRITAIN], [], 20],
    [Unit.MUSKETMAN.value, "TXT_KEY_MERC_GENERIC", 300, 400, REGIONS[Region.POLAND], [], 20],
    [Unit.MUSKETMAN.value, "TXT_KEY_MERC_GENERIC", 300, 400, REGIONS[Region.HUNGARY], [], 20],
    [Unit.MUSKETMAN.value, "TXT_KEY_MERC_GENERIC", 300, 400, REGIONS[Region.BALKANS], [], 20],
    [Unit.MUSKETMAN.value, "TXT_KEY_MERC_GENERIC", 300, 400, REGIONS[Region.KIEV], [], 20],
    [Unit.MUSKETMAN.value, "TXT_KEY_MERC_GENERIC", 300, 400, REGIONS[Region.MIDDLE_EAST], [], 20],
    [
        Unit.TEMPLAR.value,
        "TXT_KEY_MERC_TEMPLAR",
        170,
        300,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        50,
    ],
    [
        Unit.TEMPLAR.value,
        "TXT_KEY_MERC_TEMPLAR",
        170,
        300,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        50,
    ],
    [
        Unit.TEMPLAR.value,
        "TXT_KEY_MERC_TEMPLAR",
        170,
        300,
        [Province.JERUSALEM.value],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        50,
    ],
    [
        Unit.TEUTONIC.value,
        "TXT_KEY_MERC_TEUTONIC",
        170,
        300,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        50,
    ],
    [
        Unit.TEUTONIC.value,
        "TXT_KEY_MERC_TEUTONIC",
        170,
        300,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        50,
    ],
    [
        Unit.TEUTONIC.value,
        "TXT_KEY_MERC_TEUTONIC",
        170,
        300,
        [Province.JERUSALEM.value],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        50,
    ],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 217, 233, REGIONS[Region.ITALY], [], 10],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 233, 249, REGIONS[Region.ITALY], [], 10],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 249, 265, REGIONS[Region.ITALY], [], 10],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 265, 281, REGIONS[Region.ITALY], [], 10],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 281, 296, REGIONS[Region.ITALY], [], 10],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 296, 311, REGIONS[Region.ITALY], [], 10],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 311, 327, REGIONS[Region.ITALY], [], 10],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 327, 343, REGIONS[Region.ITALY], [], 10],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 343, 359, REGIONS[Region.ITALY], [], 10],
    [Unit.CONDOTTIERI.value, "TXT_KEY_MERC_ITALIAN", 359, 375, REGIONS[Region.ITALY], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 233, 243, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 243, 253, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 253, 263, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 263, 273, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 273, 283, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 283, 293, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 293, 303, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 303, 313, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 238, 248, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 248, 258, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 258, 268, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 268, 278, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 278, 288, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 288, 298, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_PIKEMAN.value, "TXT_KEY_MERC_SWISS", 298, 308, REGIONS[Region.SWISS], [], 10],
    [
        Unit.VARANGIAN_GUARD.value,
        "TXT_KEY_MERC_VARANGIAN",
        129,
        144,
        [Province.CONSTANTINOPLE.value],
        [Religion.ISLAM.value],
        10,
    ],
    [
        Unit.VARANGIAN_GUARD.value,
        "TXT_KEY_MERC_VARANGIAN",
        144,
        159,
        [Province.CONSTANTINOPLE.value],
        [Religion.ISLAM.value],
        10,
    ],
    [
        Unit.VARANGIAN_GUARD.value,
        "TXT_KEY_MERC_VARANGIAN",
        159,
        174,
        [Province.CONSTANTINOPLE.value],
        [Religion.ISLAM.value],
        10,
    ],
    [
        Unit.VARANGIAN_GUARD.value,
        "TXT_KEY_MERC_VARANGIAN",
        174,
        189,
        [Province.CONSTANTINOPLE.value],
        [Religion.ISLAM.value],
        10,
    ],
    [
        Unit.VARANGIAN_GUARD.value,
        "TXT_KEY_MERC_VARANGIAN",
        189,
        214,
        [Province.CONSTANTINOPLE.value],
        [Religion.ISLAM.value],
        20,
    ],
    [
        Unit.VARANGIAN_GUARD.value,
        "TXT_KEY_MERC_VARANGIAN",
        214,
        239,
        [Province.CONSTANTINOPLE.value],
        [Religion.ISLAM.value],
        20,
    ],
    [
        Unit.DENMARK_HUSKARL.value,
        "TXT_KEY_MERC_DANISH",
        120,
        140,
        [Province.DENMARK.value, Province.SKANELAND.value],
        [],
        10,
    ],
    [
        Unit.DENMARK_HUSKARL.value,
        "TXT_KEY_MERC_DANISH",
        140,
        160,
        [Province.DENMARK.value, Province.SKANELAND.value],
        [],
        10,
    ],
    [
        Unit.DENMARK_HUSKARL.value,
        "TXT_KEY_MERC_DANISH",
        160,
        170,
        REGIONS[Region.SCANDINAVIA],
        [],
        10,
    ],
    [
        Unit.DENMARK_HUSKARL.value,
        "TXT_KEY_MERC_DANISH",
        170,
        180,
        REGIONS[Region.SCANDINAVIA],
        [],
        10,
    ],
    [
        Unit.DENMARK_HUSKARL.value,
        "TXT_KEY_MERC_DANISH",
        180,
        190,
        REGIONS[Region.SCANDINAVIA],
        [],
        10,
    ],
    [
        Unit.DENMARK_HUSKARL.value,
        "TXT_KEY_MERC_DANISH",
        190,
        200,
        REGIONS[Region.SCANDINAVIA],
        [],
        10,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        188,
        198,
        [Province.CATALONIA.value, Province.ARAGON.value],
        [],
        10,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        198,
        208,
        [Province.CATALONIA.value, Province.ARAGON.value],
        [],
        10,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        208,
        218,
        [Province.CATALONIA.value, Province.ARAGON.value],
        [],
        15,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        218,
        228,
        [Province.CATALONIA.value, Province.ARAGON.value, Province.VALENCIA.value],
        [],
        15,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        228,
        238,
        [Province.CATALONIA.value, Province.ARAGON.value, Province.VALENCIA.value],
        [],
        15,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        238,
        248,
        [Province.CATALONIA.value, Province.ARAGON.value, Province.VALENCIA.value],
        [],
        10,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        248,
        258,
        [Province.CATALONIA.value, Province.ARAGON.value, Province.VALENCIA.value],
        [],
        10,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        258,
        267,
        [Province.CATALONIA.value, Province.ARAGON.value, Province.VALENCIA.value],
        [],
        10,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        234,
        246,
        [Province.THESSALY.value, Province.THESSALONIKI.value],
        [],
        10,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        246,
        258,
        [Province.THESSALY.value, Province.THESSALONIKI.value],
        [],
        15,
    ],
    [
        Unit.ARAGON_ALMOGAVAR.value,
        "TXT_KEY_MERC_ARAGON",
        258,
        270,
        [Province.THESSALY.value, Province.THESSALONIKI.value],
        [],
        10,
    ],
    [
        Unit.MOROCCO_BLACKGUARD.value,
        "TXT_KEY_MERC_MOROCCO",
        375,
        385,
        [
            Province.MOROCCO.value,
            Province.ORAN.value,
            Province.TETOUAN.value,
            Province.MARRAKESH.value,
            Province.FEZ.value,
        ],
        [],
        10,
    ],
    [
        Unit.MOROCCO_BLACKGUARD.value,
        "TXT_KEY_MERC_MOROCCO",
        385,
        395,
        [
            Province.MOROCCO.value,
            Province.ORAN.value,
            Province.TETOUAN.value,
            Province.MARRAKESH.value,
            Province.FEZ.value,
        ],
        [],
        10,
    ],
    [
        Unit.MOROCCO_BLACKGUARD.value,
        "TXT_KEY_MERC_MOROCCO",
        395,
        405,
        [
            Province.MOROCCO.value,
            Province.ORAN.value,
            Province.TETOUAN.value,
            Province.MARRAKESH.value,
            Province.FEZ.value,
        ],
        [],
        10,
    ],
    [
        Unit.MOROCCO_BLACKGUARD.value,
        "TXT_KEY_MERC_MOROCCO",
        405,
        415,
        [
            Province.MOROCCO.value,
            Province.ORAN.value,
            Province.TETOUAN.value,
            Province.MARRAKESH.value,
            Province.FEZ.value,
        ],
        [],
        10,
    ],
    [
        Unit.MOROCCO_BLACKGUARD.value,
        "TXT_KEY_MERC_MOROCCO",
        415,
        425,
        [
            Province.MOROCCO.value,
            Province.ORAN.value,
            Province.TETOUAN.value,
            Province.MARRAKESH.value,
            Province.FEZ.value,
        ],
        [],
        10,
    ],
    [
        Unit.MOROCCO_BLACKGUARD.value,
        "TXT_KEY_MERC_MOROCCO",
        425,
        430,
        [
            Province.MOROCCO.value,
            Province.ORAN.value,
            Province.TETOUAN.value,
            Province.MARRAKESH.value,
            Province.FEZ.value,
        ],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        359,
        375,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        375,
        390,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        390,
        405,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        405,
        420,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        420,
        435,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        435,
        450,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        450,
        460,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        460,
        470,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        470,
        480,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        480,
        490,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.HACKAPELL.value,
        "TXT_KEY_MERC_FINNISH",
        490,
        500,
        [Province.OSTERLAND.value, Province.NORRLAND.value, Province.KARELIA.value],
        [],
        10,
    ],
    [
        Unit.REITER.value,
        "TXT_KEY_MERC_GERMAN",
        350,
        360,
        [
            Province.SILESIA.value,
            Province.LESSER_POLAND.value,
            Province.MASOVIA.value,
            Province.GREATER_POLAND.value,
            Province.POMERANIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.REITER.value,
        "TXT_KEY_MERC_GERMAN",
        360,
        370,
        [
            Province.SILESIA.value,
            Province.LESSER_POLAND.value,
            Province.MASOVIA.value,
            Province.GREATER_POLAND.value,
            Province.POMERANIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.REITER.value,
        "TXT_KEY_MERC_GERMAN",
        370,
        380,
        [
            Province.SILESIA.value,
            Province.LESSER_POLAND.value,
            Province.MASOVIA.value,
            Province.GREATER_POLAND.value,
            Province.POMERANIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.REITER.value,
        "TXT_KEY_MERC_GERMAN",
        380,
        390,
        [
            Province.SILESIA.value,
            Province.LESSER_POLAND.value,
            Province.MASOVIA.value,
            Province.GREATER_POLAND.value,
            Province.POMERANIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.REITER.value,
        "TXT_KEY_MERC_GERMAN",
        390,
        400,
        [
            Province.SILESIA.value,
            Province.LESSER_POLAND.value,
            Province.MASOVIA.value,
            Province.GREATER_POLAND.value,
            Province.POMERANIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.REITER.value,
        "TXT_KEY_MERC_GERMAN",
        357,
        366,
        [
            Province.SILESIA.value,
            Province.LESSER_POLAND.value,
            Province.MASOVIA.value,
            Province.GREATER_POLAND.value,
            Province.POMERANIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.REITER.value,
        "TXT_KEY_MERC_GERMAN",
        366,
        375,
        [
            Province.SILESIA.value,
            Province.LESSER_POLAND.value,
            Province.MASOVIA.value,
            Province.GREATER_POLAND.value,
            Province.POMERANIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.REITER.value,
        "TXT_KEY_MERC_GERMAN",
        375,
        384,
        [
            Province.SILESIA.value,
            Province.LESSER_POLAND.value,
            Province.MASOVIA.value,
            Province.GREATER_POLAND.value,
            Province.POMERANIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        300,
        320,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        5,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        320,
        340,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        5,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        340,
        360,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        5,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        360,
        380,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        10,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        380,
        400,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        10,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        400,
        420,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        10,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        420,
        440,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        10,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        440,
        460,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        10,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        460,
        480,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        10,
    ],
    [
        Unit.ZAPOROZHIAN_COSSACK.value,
        "TXT_KEY_MERC_ZAPOROZHIAN",
        480,
        500,
        [Province.ZAPORIZHIA.value, Province.KIEV.value, Province.SLOBODA.value],
        [],
        10,
    ],
    [
        Unit.DON_COSSACK.value,
        "TXT_KEY_MERC_DON",
        350,
        370,
        [Province.KUBAN.value, Province.DONETS.value],
        [],
        10,
    ],
    [
        Unit.DON_COSSACK.value,
        "TXT_KEY_MERC_DON",
        370,
        390,
        [Province.KUBAN.value, Province.DONETS.value],
        [],
        10,
    ],
    [
        Unit.DON_COSSACK.value,
        "TXT_KEY_MERC_DON",
        390,
        410,
        [Province.KUBAN.value, Province.DONETS.value],
        [],
        10,
    ],
    [
        Unit.DON_COSSACK.value,
        "TXT_KEY_MERC_DON",
        410,
        425,
        [Province.KUBAN.value, Province.DONETS.value],
        [],
        10,
    ],
    [
        Unit.DON_COSSACK.value,
        "TXT_KEY_MERC_DON",
        425,
        440,
        [Province.KUBAN.value, Province.DONETS.value],
        [],
        10,
    ],
    [
        Unit.DON_COSSACK.value,
        "TXT_KEY_MERC_DON",
        440,
        455,
        [Province.KUBAN.value, Province.DONETS.value],
        [],
        10,
    ],
    [
        Unit.DON_COSSACK.value,
        "TXT_KEY_MERC_DON",
        455,
        470,
        [Province.KUBAN.value, Province.DONETS.value],
        [],
        10,
    ],
    [
        Unit.DON_COSSACK.value,
        "TXT_KEY_MERC_DON",
        470,
        485,
        [Province.KUBAN.value, Province.DONETS.value],
        [],
        10,
    ],
    [
        Unit.DON_COSSACK.value,
        "TXT_KEY_MERC_DON",
        485,
        500,
        [Province.KUBAN.value, Province.DONETS.value],
        [],
        10,
    ],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 300, 310, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 310, 320, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 320, 330, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 330, 340, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 340, 350, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 350, 360, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 360, 370, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 370, 380, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 380, 390, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 390, 400, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 335, 345, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 345, 355, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 355, 365, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 365, 375, REGIONS[Region.GERMANY], [], 10],
    [Unit.DOPPELSOLDNER.value, "TXT_KEY_MERC_GERMAN", 375, 385, REGIONS[Region.GERMANY], [], 10],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 390, 400, [Province.IRELAND.value], [], 10],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 400, 410, [Province.IRELAND.value], [], 10],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 410, 420, [Province.IRELAND.value], [], 10],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 420, 430, [Province.IRELAND.value], [], 10],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 430, 440, [Province.IRELAND.value], [], 10],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 440, 450, [Province.IRELAND.value], [], 15],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 450, 460, [Province.IRELAND.value], [], 15],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 460, 470, [Province.IRELAND.value], [], 15],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 470, 480, [Province.IRELAND.value], [], 15],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 480, 490, [Province.IRELAND.value], [], 15],
    [Unit.IRISH_BRIGADE.value, "TXT_KEY_MERC_IRISH", 490, 500, [Province.IRELAND.value], [], 15],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        280,
        295,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        295,
        310,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        310,
        325,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        325,
        340,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        340,
        355,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        355,
        370,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        370,
        385,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        385,
        400,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        400,
        415,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.STRADIOT.value,
        "TXT_KEY_MERC_BALKAN",
        415,
        430,
        REGIONS[Region.BALKANS] + [Province.CALABRIA.value, Province.APULIA.value],
        [],
        10,
    ],
    [
        Unit.WAARDGELDER.value,
        "TXT_KEY_MERC_BALKAN",
        340,
        355,
        [Province.NETHERLANDS.value, Province.FLANDERS.value],
        [],
        10,
    ],
    [
        Unit.WAARDGELDER.value,
        "TXT_KEY_MERC_BALKAN",
        355,
        370,
        [Province.NETHERLANDS.value, Province.FLANDERS.value],
        [],
        10,
    ],
    [
        Unit.WAARDGELDER.value,
        "TXT_KEY_MERC_BALKAN",
        370,
        395,
        [Province.NETHERLANDS.value, Province.FLANDERS.value],
        [],
        10,
    ],
    [
        Unit.WAARDGELDER.value,
        "TXT_KEY_MERC_BALKAN",
        395,
        410,
        [Province.NETHERLANDS.value, Province.FLANDERS.value],
        [],
        10,
    ],
    [
        Unit.WAARDGELDER.value,
        "TXT_KEY_MERC_BALKAN",
        410,
        425,
        [Province.NETHERLANDS.value, Province.FLANDERS.value],
        [],
        10,
    ],
    [
        Unit.WAARDGELDER.value,
        "TXT_KEY_MERC_BALKAN",
        425,
        440,
        [Province.NETHERLANDS.value, Province.FLANDERS.value],
        [],
        10,
    ],
    [
        Unit.WAARDGELDER.value,
        "TXT_KEY_MERC_BALKAN",
        440,
        450,
        [Province.NETHERLANDS.value, Province.FLANDERS.value],
        [],
        10,
    ],
    [
        Unit.NAFFATUN.value,
        "TXT_KEY_MERC_ARABIAN",
        160,
        170,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.NAFFATUN.value,
        "TXT_KEY_MERC_ARABIAN",
        170,
        180,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.NAFFATUN.value,
        "TXT_KEY_MERC_ARABIAN",
        180,
        190,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.NAFFATUN.value,
        "TXT_KEY_MERC_ARABIAN",
        190,
        200,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.NAFFATUN.value,
        "TXT_KEY_MERC_ARABIAN",
        200,
        210,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.NAFFATUN.value,
        "TXT_KEY_MERC_ARABIAN",
        210,
        217,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.NAFFATUN.value,
        "TXT_KEY_MERC_ARABIAN",
        175,
        190,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.NAFFATUN.value,
        "TXT_KEY_MERC_ARABIAN",
        190,
        205,
        REGIONS[Region.MIDDLE_EAST],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.TURKOPOLES.value,
        "TXT_KEY_MERC_TURKISH",
        160,
        170,
        REGIONS[Region.MIDDLE_EAST] + [Province.EGYPT.value],
        [Religion.ISLAM.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TURKOPOLES.value,
        "TXT_KEY_MERC_TURKISH",
        170,
        180,
        REGIONS[Region.MIDDLE_EAST] + [Province.EGYPT.value],
        [Religion.ISLAM.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TURKOPOLES.value,
        "TXT_KEY_MERC_TURKISH",
        175,
        185,
        REGIONS[Region.MIDDLE_EAST] + [Province.EGYPT.value],
        [Religion.ISLAM.value, Religion.PROTESTANTISM.value],
        30,
    ],
    [
        Unit.TURKOPOLES.value,
        "TXT_KEY_MERC_TURKISH",
        180,
        190,
        REGIONS[Region.MIDDLE_EAST] + [Province.EGYPT.value],
        [Religion.ISLAM.value, Religion.PROTESTANTISM.value],
        15,
    ],
    [
        Unit.TURKOPOLES.value,
        "TXT_KEY_MERC_TURKISH",
        185,
        195,
        REGIONS[Region.MIDDLE_EAST] + [Province.EGYPT.value],
        [Religion.ISLAM.value, Religion.PROTESTANTISM.value],
        30,
    ],
    [
        Unit.TURKOPOLES.value,
        "TXT_KEY_MERC_TURKISH",
        190,
        200,
        REGIONS[Region.MIDDLE_EAST] + [Province.EGYPT.value],
        [Religion.ISLAM.value, Religion.PROTESTANTISM.value],
        15,
    ],
    [
        Unit.TURKOPOLES.value,
        "TXT_KEY_MERC_TURKISH",
        195,
        205,
        REGIONS[Region.MIDDLE_EAST] + [Province.EGYPT.value],
        [Religion.ISLAM.value, Religion.PROTESTANTISM.value],
        30,
    ],
    [
        Unit.TURKOPOLES.value,
        "TXT_KEY_MERC_TURKISH",
        200,
        210,
        REGIONS[Region.MIDDLE_EAST] + [Province.EGYPT.value],
        [Religion.ISLAM.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TURKOPOLES.value,
        "TXT_KEY_MERC_TURKISH",
        210,
        217,
        REGIONS[Region.MIDDLE_EAST] + [Province.EGYPT.value],
        [Religion.ISLAM.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.WALLOON_GUARD.value,
        "TXT_KEY_MERC_WALLOON",
        434,
        444,
        [Province.FLANDERS.value, Province.LORRAINE.value, Province.PICARDY.value],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.WALLOON_GUARD.value,
        "TXT_KEY_MERC_WALLOON",
        444,
        454,
        [Province.FLANDERS.value, Province.LORRAINE.value, Province.PICARDY.value],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.WALLOON_GUARD.value,
        "TXT_KEY_MERC_WALLOON",
        454,
        464,
        [Province.FLANDERS.value, Province.LORRAINE.value, Province.PICARDY.value],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.WALLOON_GUARD.value,
        "TXT_KEY_MERC_WALLOON",
        464,
        474,
        [Province.FLANDERS.value, Province.LORRAINE.value, Province.PICARDY.value],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        15,
    ],
    [
        Unit.WALLOON_GUARD.value,
        "TXT_KEY_MERC_WALLOON",
        474,
        484,
        [Province.FLANDERS.value, Province.LORRAINE.value, Province.PICARDY.value],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        15,
    ],
    [
        Unit.WALLOON_GUARD.value,
        "TXT_KEY_MERC_WALLOON",
        484,
        494,
        [Province.FLANDERS.value, Province.LORRAINE.value, Province.PICARDY.value],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        15,
    ],
    [
        Unit.WALLOON_GUARD.value,
        "TXT_KEY_MERC_WALLOON",
        494,
        500,
        [Province.FLANDERS.value, Province.LORRAINE.value, Province.PICARDY.value],
        [Religion.ISLAM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        20,
    ],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 375, 385, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 385, 395, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 395, 405, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 405, 415, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 415, 425, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 425, 435, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 435, 445, REGIONS[Region.SWISS], [], 15],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 430, 440, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 445, 455, REGIONS[Region.SWISS], [], 15],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 440, 450, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 455, 465, REGIONS[Region.SWISS], [], 15],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 450, 460, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 465, 475, REGIONS[Region.SWISS], [], 15],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 460, 470, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 475, 485, REGIONS[Region.SWISS], [], 15],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 470, 480, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 485, 495, REGIONS[Region.SWISS], [], 15],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 480, 490, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 485, 495, REGIONS[Region.SWISS], [], 15],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 490, 500, REGIONS[Region.SWISS], [], 10],
    [Unit.SWISS_GUN.value, "TXT_KEY_MERC_SWISS", 485, 500, REGIONS[Region.SWISS], [], 20],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        240,
        255,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        5,
    ],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        255,
        270,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        5,
    ],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        270,
        285,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        10,
    ],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        285,
        300,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        10,
    ],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        300,
        315,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        10,
    ],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        315,
        330,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        10,
    ],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        330,
        345,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        10,
    ],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        345,
        360,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        10,
    ],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        360,
        375,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        10,
    ],
    [
        Unit.LIPKA_TATAR.value,
        "TXT_KEY_MERC_BALTIC",
        375,
        385,
        REGIONS[Region.LITHUANIA]
        + [Province.POLOTSK.value, Province.SUVALKIJA.value, Province.MINSK.value],
        [],
        5,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        380,
        390,
        [Province.SCOTLAND.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        390,
        400,
        [Province.SCOTLAND.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        400,
        410,
        [Province.SCOTLAND.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        410,
        420,
        [Province.SCOTLAND.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        420,
        430,
        [Province.SCOTLAND.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        430,
        440,
        [Province.SCOTLAND.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        440,
        450,
        [Province.SCOTLAND.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        450,
        460,
        [Province.SCOTLAND.value],
        [],
        15,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        460,
        470,
        [Province.SCOTLAND.value],
        [],
        15,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        470,
        480,
        [Province.SCOTLAND.value],
        [],
        15,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        480,
        490,
        [Province.SCOTLAND.value],
        [],
        15,
    ],
    [
        Unit.HIGHLANDER_GUN.value,
        "TXT_KEY_MERC_SCOTTISH",
        490,
        500,
        [Province.SCOTLAND.value],
        [],
        15,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        42,
        57,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        57,
        72,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        72,
        87,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        87,
        102,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        102,
        117,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        117,
        132,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        132,
        147,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        147,
        162,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        162,
        177,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        177,
        192,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.ZANJI.value,
        "TXT_KEY_MERC_AFRICAN",
        192,
        200,
        REGIONS[Region.AFRICA] + [Province.EGYPT.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        50,
        65,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        65,
        80,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        80,
        95,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        95,
        110,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        110,
        125,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        125,
        140,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        140,
        165,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        165,
        180,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        180,
        195,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        195,
        210,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        210,
        225,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        225,
        240,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        240,
        255,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.TOUAREG.value,
        "TXT_KEY_MERC_AFRICAN",
        255,
        266,
        [
            Province.MOROCCO.value,
            Province.MARRAKESH.value,
            Province.TETOUAN.value,
            Province.ORAN.value,
            Province.FEZ.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [Unit.NUBIAN_LONGBOWMAN.value, "TXT_KEY_MERC_NUBIAN", 37, 48, [Province.EGYPT.value], [], 5],
    [Unit.NUBIAN_LONGBOWMAN.value, "TXT_KEY_MERC_NUBIAN", 48, 58, [Province.EGYPT.value], [], 10],
    [Unit.NUBIAN_LONGBOWMAN.value, "TXT_KEY_MERC_NUBIAN", 58, 68, [Province.EGYPT.value], [], 10],
    [Unit.NUBIAN_LONGBOWMAN.value, "TXT_KEY_MERC_NUBIAN", 68, 78, [Province.EGYPT.value], [], 10],
    [Unit.NUBIAN_LONGBOWMAN.value, "TXT_KEY_MERC_NUBIAN", 78, 88, [Province.EGYPT.value], [], 10],
    [Unit.NUBIAN_LONGBOWMAN.value, "TXT_KEY_MERC_NUBIAN", 88, 98, [Province.EGYPT.value], [], 10],
    [Unit.NUBIAN_LONGBOWMAN.value, "TXT_KEY_MERC_NUBIAN", 98, 108, [Province.EGYPT.value], [], 10],
    [
        Unit.NUBIAN_LONGBOWMAN.value,
        "TXT_KEY_MERC_NUBIAN",
        108,
        118,
        [Province.EGYPT.value],
        [],
        10,
    ],
    [
        Unit.NUBIAN_LONGBOWMAN.value,
        "TXT_KEY_MERC_NUBIAN",
        118,
        128,
        [Province.EGYPT.value],
        [],
        10,
    ],
    [
        Unit.NUBIAN_LONGBOWMAN.value,
        "TXT_KEY_MERC_NUBIAN",
        128,
        139,
        [Province.EGYPT.value],
        [],
        10,
    ],
    [Unit.NUBIAN_LONGBOWMAN.value, "TXT_KEY_MERC_NUBIAN", 139, 150, [Province.EGYPT.value], [], 5],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        180,
        195,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        5,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        195,
        210,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        5,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        210,
        225,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        225,
        240,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        240,
        255,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        255,
        270,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        270,
        285,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        285,
        300,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        300,
        315,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        315,
        330,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        330,
        345,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        345,
        360,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        10,
    ],
    [
        Unit.HIGHLANDER.value,
        "TXT_KEY_MERC_SCOTTISH",
        360,
        370,
        [Province.SCOTLAND.value, Province.NORTHUMBRIA.value, Province.THE_ISLES.value],
        [],
        5,
    ],
    [Unit.WELSH_LONGBOWMAN.value, "TXT_KEY_MERC_WELSH", 200, 220, [Province.WALES.value], [], 5],
    [Unit.WELSH_LONGBOWMAN.value, "TXT_KEY_MERC_WELSH", 220, 240, [Province.WALES.value], [], 10],
    [Unit.WELSH_LONGBOWMAN.value, "TXT_KEY_MERC_WELSH", 240, 260, [Province.WALES.value], [], 10],
    [Unit.WELSH_LONGBOWMAN.value, "TXT_KEY_MERC_WELSH", 260, 280, [Province.WALES.value], [], 10],
    [Unit.WELSH_LONGBOWMAN.value, "TXT_KEY_MERC_WELSH", 280, 300, [Province.WALES.value], [], 10],
    [Unit.WELSH_LONGBOWMAN.value, "TXT_KEY_MERC_WELSH", 300, 320, [Province.WALES.value], [], 10],
    [Unit.WELSH_LONGBOWMAN.value, "TXT_KEY_MERC_WELSH", 320, 340, [Province.WALES.value], [], 10],
    [Unit.WELSH_LONGBOWMAN.value, "TXT_KEY_MERC_WELSH", 340, 350, [Province.WALES.value], [], 5],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 80, 100, REGIONS[Region.ASIA_MINOR], [], 5],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 100, 120, REGIONS[Region.ASIA_MINOR], [], 5],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 120, 140, REGIONS[Region.ASIA_MINOR], [], 5],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 140, 160, REGIONS[Region.ASIA_MINOR], [], 10],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 160, 180, REGIONS[Region.ASIA_MINOR], [], 10],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 80, 100, [Province.CONSTANTINOPLE.value], [], 5],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 100, 120, [Province.CONSTANTINOPLE.value], [], 5],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 120, 140, [Province.CONSTANTINOPLE.value], [], 5],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 140, 160, [Province.CONSTANTINOPLE.value], [], 5],
    [Unit.TAGMATA.value, "TXT_KEY_MERC_GREEK", 160, 180, [Province.CONSTANTINOPLE.value], [], 5],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        260,
        280,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        280,
        300,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        300,
        320,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        320,
        340,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        340,
        360,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        360,
        380,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        380,
        400,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        400,
        420,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        420,
        440,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        10,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        440,
        450,
        [
            Province.ORAN.value,
            Province.ALGIERS.value,
            Province.IFRIQIYA.value,
            Province.CYRENAICA.value,
            Province.TRIPOLITANIA.value,
        ],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        260,
        280,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        280,
        300,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        300,
        320,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        320,
        340,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        340,
        360,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        360,
        380,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        380,
        400,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        400,
        420,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        420,
        440,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.CORSAIR.value,
        "TXT_KEY_MERC_CORSAIR",
        440,
        450,
        [Province.IFRIQIYA.value],
        [Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, Religion.PROTESTANTISM.value],
        5,
    ],
    [
        Unit.MAMLUK_HEAVY_CAVALRY.value,
        "TXT_KEY_MERC_EGYPTIAN",
        200,
        220,
        [Province.EGYPT.value],
        [],
        20,
    ],
    [
        Unit.MAMLUK_HEAVY_CAVALRY.value,
        "TXT_KEY_MERC_EGYPTIAN",
        220,
        240,
        [Province.EGYPT.value],
        [],
        20,
    ],
    [
        Unit.MAMLUK_HEAVY_CAVALRY.value,
        "TXT_KEY_MERC_EGYPTIAN",
        240,
        260,
        [Province.EGYPT.value],
        [],
        20,
    ],
    [
        Unit.MAMLUK_HEAVY_CAVALRY.value,
        "TXT_KEY_MERC_EGYPTIAN",
        260,
        280,
        [Province.EGYPT.value],
        [],
        20,
    ],
    [
        Unit.MAMLUK_HEAVY_CAVALRY.value,
        "TXT_KEY_MERC_EGYPTIAN",
        280,
        300,
        [Province.EGYPT.value],
        [],
        20,
    ],
    [
        Unit.SOUTH_SLAV_VLASTELA.value,
        "TXT_KEY_MERC_BALKAN",
        160,
        170,
        [
            Province.SERBIA.value,
            Province.BOSNIA.value,
            Province.BANAT.value,
            Province.SLAVONIA.value,
            Province.DALMATIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.SOUTH_SLAV_VLASTELA.value,
        "TXT_KEY_MERC_BALKAN",
        170,
        180,
        [
            Province.SERBIA.value,
            Province.BOSNIA.value,
            Province.BANAT.value,
            Province.SLAVONIA.value,
            Province.DALMATIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.SOUTH_SLAV_VLASTELA.value,
        "TXT_KEY_MERC_BALKAN",
        180,
        190,
        [
            Province.SERBIA.value,
            Province.BOSNIA.value,
            Province.BANAT.value,
            Province.SLAVONIA.value,
            Province.DALMATIA.value,
        ],
        [],
        15,
    ],
    [
        Unit.SOUTH_SLAV_VLASTELA.value,
        "TXT_KEY_MERC_BALKAN",
        190,
        200,
        [
            Province.SERBIA.value,
            Province.BOSNIA.value,
            Province.BANAT.value,
            Province.SLAVONIA.value,
            Province.DALMATIA.value,
        ],
        [],
        15,
    ],
    [
        Unit.SOUTH_SLAV_VLASTELA.value,
        "TXT_KEY_MERC_BALKAN",
        200,
        210,
        [
            Province.SERBIA.value,
            Province.BOSNIA.value,
            Province.BANAT.value,
            Province.SLAVONIA.value,
            Province.DALMATIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.SOUTH_SLAV_VLASTELA.value,
        "TXT_KEY_MERC_BALKAN",
        210,
        217,
        [
            Province.SERBIA.value,
            Province.BOSNIA.value,
            Province.BANAT.value,
            Province.SLAVONIA.value,
            Province.DALMATIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.BOHEMIAN_WAR_WAGON.value,
        "TXT_KEY_MERC_BOHEMIAN",
        200,
        220,
        [Province.BOHEMIA.value, Province.MORAVIA.value],
        [],
        20,
    ],
    [
        Unit.BOHEMIAN_WAR_WAGON.value,
        "TXT_KEY_MERC_BOHEMIAN",
        220,
        240,
        [Province.BOHEMIA.value, Province.MORAVIA.value],
        [],
        20,
    ],
    [
        Unit.BOHEMIAN_WAR_WAGON.value,
        "TXT_KEY_MERC_BOHEMIAN",
        240,
        260,
        [Province.BOHEMIA.value, Province.MORAVIA.value],
        [],
        20,
    ],
    [
        Unit.BOHEMIAN_WAR_WAGON.value,
        "TXT_KEY_MERC_BOHEMIAN",
        260,
        280,
        [Province.BOHEMIA.value, Province.MORAVIA.value],
        [],
        20,
    ],
    [
        Unit.BOHEMIAN_WAR_WAGON.value,
        "TXT_KEY_MERC_BOHEMIAN",
        280,
        300,
        [Province.BOHEMIA.value, Province.MORAVIA.value],
        [],
        20,
    ],
    [
        Unit.LOMBARD_HEAVY_FOOTMAN.value,
        "TXT_KEY_MERC_ITALIAN",
        188,
        198,
        [
            Province.LOMBARDY.value,
            Province.VERONA.value,
            Province.TUSCANY.value,
            Province.LIGURIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.LOMBARD_HEAVY_FOOTMAN.value,
        "TXT_KEY_MERC_ITALIAN",
        198,
        208,
        [
            Province.LOMBARDY.value,
            Province.VERONA.value,
            Province.TUSCANY.value,
            Province.LIGURIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.LOMBARD_HEAVY_FOOTMAN.value,
        "TXT_KEY_MERC_ITALIAN",
        208,
        218,
        [
            Province.LOMBARDY.value,
            Province.VERONA.value,
            Province.TUSCANY.value,
            Province.LIGURIA.value,
        ],
        [],
        15,
    ],
    [
        Unit.LOMBARD_HEAVY_FOOTMAN.value,
        "TXT_KEY_MERC_ITALIAN",
        218,
        228,
        [
            Province.LOMBARDY.value,
            Province.VERONA.value,
            Province.TUSCANY.value,
            Province.LIGURIA.value,
        ],
        [],
        15,
    ],
    [
        Unit.LOMBARD_HEAVY_FOOTMAN.value,
        "TXT_KEY_MERC_ITALIAN",
        228,
        238,
        [
            Province.LOMBARDY.value,
            Province.VERONA.value,
            Province.TUSCANY.value,
            Province.LIGURIA.value,
        ],
        [],
        15,
    ],
    [
        Unit.LOMBARD_HEAVY_FOOTMAN.value,
        "TXT_KEY_MERC_ITALIAN",
        238,
        248,
        [
            Province.LOMBARDY.value,
            Province.VERONA.value,
            Province.TUSCANY.value,
            Province.LIGURIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.LOMBARD_HEAVY_FOOTMAN.value,
        "TXT_KEY_MERC_ITALIAN",
        248,
        258,
        [
            Province.LOMBARDY.value,
            Province.VERONA.value,
            Province.TUSCANY.value,
            Province.LIGURIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.LOMBARD_HEAVY_FOOTMAN.value,
        "TXT_KEY_MERC_ITALIAN",
        258,
        267,
        [
            Province.LOMBARDY.value,
            Province.VERONA.value,
            Province.TUSCANY.value,
            Province.LIGURIA.value,
        ],
        [],
        10,
    ],
    [
        Unit.CRIMEAN_TATAR_RIDER.value,
        "TXT_KEY_MERC_CRIMEAN",
        250,
        280,
        [Province.CRIMEA.value],
        [],
        10,
    ],
    [
        Unit.CRIMEAN_TATAR_RIDER.value,
        "TXT_KEY_MERC_CRIMEAN",
        280,
        310,
        [Province.CRIMEA.value],
        [],
        10,
    ],
    [
        Unit.CRIMEAN_TATAR_RIDER.value,
        "TXT_KEY_MERC_CRIMEAN",
        310,
        340,
        [Province.CRIMEA.value],
        [],
        10,
    ],
    [
        Unit.CRIMEAN_TATAR_RIDER.value,
        "TXT_KEY_MERC_CRIMEAN",
        340,
        370,
        [Province.CRIMEA.value],
        [],
        10,
    ],
    [
        Unit.CRIMEAN_TATAR_RIDER.value,
        "TXT_KEY_MERC_CRIMEAN",
        370,
        400,
        [Province.CRIMEA.value],
        [],
        10,
    ],
]

### A few Parameters for Mercs only:
# Promotions and their odds, advanced promotions have very low probability, leader-tied promotions, commando, navigation and cargo capacity don't appear
# combat 1 - 5, cover (vs archer), shock (vs heavy infantry), pinch, formation (vs heavy horse), charge (vs siege), ambush (vs light cav), feint (vs polearm), amphibious, march (movement heal), medic 1-2,
# guerilla (hill defense) 1-3, woodsman 1-3, city raider 1-3, garrison 1-3, drill 1-4, barrage (collateral) 1-3, accuracy (more bombard), flanking (vs siege) 1-2, sentry (vision), mobility (movement),
# navigation 1-2, cargo, leader, leadership (more XP), tactic (withdraw), commando (enemy roads), combat 6, morale (movement), medic 3, merc
lPromotionOdds = [
    100,
    80,
    40,
    10,
    5,
    50,
    50,
    40,
    60,
    40,
    20,
    50,
    20,
    10,
    30,
    20,
    50,
    30,
    10,
    50,
    30,
    10,
    80,
    40,
    10,
    60,
    30,
    10,
    60,
    40,
    10,
    5,
    60,
    40,
    10,
    60,
    50,
    30,
    20,
    40,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]
# The way promotions would affect the cost of the mercenary (percentage wise)
lPromotionCost = [
    15,
    20,
    25,
    30,
    35,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    35,
    50,
    30,
    40,
    15,
    20,
    30,
    15,
    20,
    30,
    20,
    30,
    40,
    20,
    30,
    40,
    15,
    20,
    25,
    30,
    10,
    15,
    20,
    20,
    20,
    25,
    10,
    25,
    20,
    25,
    10,
    80,
    60,
    50,
    50,
    40,
    40,
    50,
    0,
    0,
]
iNumTotalMercPromotions = 40  # without navigation 1-2, cargo, commando and leader-tied promotions - those are unnecessary here (unavailable as base promotions for all mercs)
iNumPromotionsSoftCap = 3  # can get more promotions if you get a high promotion (i.e. combat 5), but overall it should be unlikely
iNumPromotionIterations = 4  # how many attemps shall we make to add promotion (the bigger the number, the more likely it is for a unit to have at least iNumPromotionsSoftCap promotions)

# 3MiroUP: set the merc cost modifiers here
lMercCostModifier = (
    150,  # Byzantium
    120,  # Frankia
    100,  # Arabia
    100,  # Bulgaria
    100,  # Cordoba
    100,  # Venecia
    100,  # Burgundy
    110,  # Germany
    100,  # Novgorod
    100,  # Norway
    100,  # Kiev
    100,  # Hungary
    100,  # Spain
    100,  # Denmark
    100,  # Scotland
    100,  # Poland
    50,  # Genoa
    100,  # Morocco
    100,  # England
    100,  # Portugal
    100,  # Aragon
    100,  # Sweden
    100,  # Prussia
    100,  # Lithuania
    100,  # Austria
    100,  # Turkey
    100,  # Moscow
    100,  # Dutch
    0,  # Pope
    0,
    0,
    0,
    0,
    0,
)


class MercenaryManager:
    def __init__(self):
        self.lGlobalPool = []
        self.lHiredBy = []
        self.GMU = GlobalMercenaryUtils()
        pass

    def getMercLists(self):
        self.lGlobalPool = data.lMercGlobalPool
        self.lHiredBy = data.lMercsHiredBy

    def setMercLists(self):
        data.lMercGlobalPool = self.lGlobalPool
        data.lMercsHiredBy = self.lHiredBy

    def rendomizeMercProvinces(self, iGameTurn):
        if iGameTurn % 2 == rand(2):
            iHuman = gc.getGame().getActivePlayer()
            lHumanProvinces = self.GMU.getOwnedProvinces(iHuman)
            iMercsLeft = 0
            for lMerc in self.lGlobalPool:
                if percentage_chance(lMercList[lMerc[0]][6] / 2, strict=True):
                    self.lGlobalPool.remove(lMerc)
                    if lMerc[4] in lHumanProvinces:
                        CyInterface().addMessage(
                            iHuman,
                            False,
                            MessageData.DURATION / 2,
                            text("TXT_KEY_MERC_NEW_MERC_MOVING"),
                            "",
                            0,
                            "",
                            ColorTypes(MessageData.LIME),
                            -1,
                            -1,
                            True,
                            True,
                        )
                    iMercsLeft += 1
                    if iMercsLeft > 1:
                        # don't let too many mercs leave the pool
                        return

    def setPrereqConsistentPromotions(self, lPromotions):
        bPass = False
        while not bPass:
            bPass = True
            for iPromotion in lPromotions:
                pPromotionInfo = gc.getPromotionInfo(iPromotion)
                iPrereq = pPromotionInfo.getPrereqOrPromotion1()
                if iPrereq != -1 and iPrereq not in lPromotions:
                    lPromotions.append(iPrereq)
                    bPass = False
                iPrereq = pPromotionInfo.getPrereqOrPromotion2()
                if iPrereq != -1 and iPrereq not in lPromotions:
                    lPromotions.append(iPrereq)
                    bPass = False
        return lPromotions

    def addNewMerc(self, iMerc):
        # this processes the available promotions
        lMercInfo = lMercList[iMerc]
        iMercType = lMercInfo[0]

        # get the promotions
        iNumPromotions = 0
        lPromotions = []
        iIterations = (
            0  # limit the number of iterations so we can have mercs with only a few promotions
        )
        while iNumPromotions < iNumPromotionsSoftCap and iIterations < iNumPromotionIterations:
            iPromotion = rand(iNumTotalMercPromotions)
            if isPromotionValid(iPromotion, iMercType, False):
                if iPromotion not in lPromotions and percentage_chance(
                    lPromotionOdds[iPromotion], strict=True
                ):
                    lPromotions.append(iPromotion)
                    lPromotions = self.setPrereqConsistentPromotions(lPromotions)
                    iNumPromotions = len(lPromotions)
            iIterations += 1
        # add the default (free) promotions for the given unit type
        for iPromotion in range(len(Promotion) - 1):
            if gc.getUnitInfo(iMercType).getFreePromotions(iPromotion):
                if iPromotion not in lPromotions:
                    lPromotions.append(iPromotion)

        (iPurchaseCost, iUpkeepCost) = self.GMU.getCost(iMerc, lPromotions)
        iCurrentProvince = choice(lMercInfo[4])

        # Absinthe: different message for the human player for the various cases
        iHuman = gc.getGame().getActivePlayer()
        pHuman = gc.getPlayer(iHuman)
        ProvMessage = False
        if pHuman.getProvinceCityCount(iCurrentProvince) > 0:
            # Absinthe: different message if the mercenaries don't like the player's state religion
            iStateReligion = pHuman.getStateReligion()
            if iStateReligion in lMercList[iMerc][5]:
                szProvName = "TXT_KEY_PROVINCE_NAME_%i" % iCurrentProvince
                szCurrentProvince = text(szProvName)
                CyInterface().addMessage(
                    iHuman,
                    False,
                    MessageData.DURATION / 2,
                    text("TXT_KEY_MERC_NEW_MERC_AVAILABLE")
                    + " "
                    + szCurrentProvince
                    + text("TXT_KEY_MERC_NEW_MERC_RELIGION"),
                    "",
                    0,
                    "",
                    ColorTypes(MessageData.LIME),
                    -1,
                    -1,
                    True,
                    True,
                )
            else:
                # Absinthe: normal message
                for city in utils.getCityList(iHuman):
                    if city.getProvince() == iCurrentProvince:
                        if city.getCultureLevel() >= 2:
                            szProvName = "TXT_KEY_PROVINCE_NAME_%i" % iCurrentProvince
                            szCurrentProvince = text(szProvName)
                            CyInterface().addMessage(
                                iHuman,
                                False,
                                MessageData.DURATION / 2,
                                text("TXT_KEY_MERC_NEW_MERC_AVAILABLE")
                                + " "
                                + szCurrentProvince
                                + "!",
                                "",
                                0,
                                "",
                                ColorTypes(MessageData.LIME),
                                -1,
                                -1,
                                True,
                                True,
                            )
                            ProvMessage = True
                            break
                # Absinthe: different message if the player doesn't have enough culture in the province
                if not ProvMessage:
                    szProvName = "TXT_KEY_PROVINCE_NAME_%i" % iCurrentProvince
                    szCurrentProvince = text(szProvName)
                    CyInterface().addMessage(
                        iHuman,
                        False,
                        MessageData.DURATION / 2,
                        text("TXT_KEY_MERC_NEW_MERC_AVAILABLE")
                        + " "
                        + szCurrentProvince
                        + text("TXT_KEY_MERC_NEW_MERC_CULTURE"),
                        "",
                        0,
                        "",
                        ColorTypes(MessageData.LIME),
                        -1,
                        -1,
                        True,
                        True,
                    )

        # add the merc, keep the merc index, costs and promotions
        self.lGlobalPool.append([iMerc, lPromotions, iPurchaseCost, iUpkeepCost, iCurrentProvince])

    def processNewMercs(self, iGameTurn):
        # add new mercs to the pool

        potentialMercs = []
        alreadyAvailableMercs = []
        for iI in range(len(self.lGlobalPool)):
            alreadyAvailableMercs.append(self.lGlobalPool[iI][0])

        for iMerc in range(len(lMercList)):
            if (
                self.lHiredBy[iMerc] == -1
                and iMerc not in alreadyAvailableMercs
                and iGameTurn >= lMercList[iMerc][2]
                and iGameTurn <= lMercList[iMerc][3]
            ):
                potentialMercs.append(iMerc)

        iNumPotentialMercs = len(potentialMercs)
        if iNumPotentialMercs == 0:
            return
        # if there are mercs to be potentially added
        iStart = rand(iNumPotentialMercs)
        for iOffset in range(iNumPotentialMercs):
            iMerc = potentialMercs[(iOffset + iStart) % iNumPotentialMercs]
            if percentage_chance(lMercList[iMerc][6], strict=True):
                self.addNewMerc(iMerc)

    def doMercsTurn(self, iGameTurn):
        # this is called at the end of the game turn
        # thus the AI gets the advantage to make the Merc "decision" with the most up-to-date political data and they can get the mercs instantly
        # the Human gets the advantage to get the first pick at the available mercs

        self.getMercLists()  # load the current mercenary pool
        iHuman = gc.getGame().getActivePlayer()

        # for lMerc in self.lGlobalPool:

        # Go through each of the players and deduct their mercenary maintenance amount from their gold (round up)
        for iPlayer in civilizations().main().ids():
            pPlayer = gc.getPlayer(iPlayer)
            if pPlayer.isAlive():
                if (
                    pPlayer.getCommercePercent(CommerceTypes.COMMERCE_GOLD) == 100
                    and pPlayer.getGold()
                    < (
                        pPlayer.getPicklefreeParameter(
                            SpecialParameter.MERCENARY_COST_PER_TURN.value
                        )
                        + 99
                    )
                    / 100
                ):
                    # not enough gold to pay the mercs, they will randomly desert you
                    self.desertMercs(iPlayer)

                # Absinthe: added the subtraction directly in the inflated cost calculations in the .dll, so this is now redundant
                # pPlayer.setGold(pPlayer.getGold()-(pPlayer.getPicklefreeParameter( iMercCostPerTurn )+99)/100 )
                # TODO: AI
                if iPlayer != iHuman:
                    self.processMercAI(iPlayer)

        self.rendomizeMercProvinces(iGameTurn)  # some mercs may leave

        self.processNewMercs(iGameTurn)  # add new Merc to the pool
        self.processNewMercs(iGameTurn)  # can add up to 2 mercs per turn

        ### DEBUG - start
        # self.addNewMerc( 12 )
        # self.addNewMerc( 76 )
        ### DEBUG - end

        self.setMercLists()  # save the potentially modified merc list (this allows for pickle read/write only once per turn)

        # self.GMU.hireMerc( self.lGlobalPool[0], Civ.FRANCE.value )

    def desertMercs(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        if iPlayer == human():
            CyInterface().addMessage(
                iPlayer,
                False,
                MessageData.DURATION / 2,
                text("TXT_KEY_MERC_NEW_MERC_DESERTERS"),
                "",
                0,
                "",
                ColorTypes(MessageData.LIGHT_RED),
                -1,
                -1,
                True,
                True,
            )

        while True:
            lHiredMercs = [
                unit for unit in PyPlayer(iPlayer).getUnitList() if unit.getMercID() > -1
            ]

            if lHiredMercs:
                self.GMU.fireMerc(choice(lHiredMercs))
            else:
                break

    def onCityAcquiredAndKept(self, iCiv, pCity):
        # Absinthe: if there are mercs available in the new city's province, interface message about it to the human player
        iProvince = pCity.getProvince()
        self.getMercLists()  # load the current mercenary pool
        for lMerc in self.lGlobalPool:
            if lMerc[4] == iProvince:
                if iCiv == human():
                    CyInterface().addMessage(
                        iCiv,
                        False,
                        MessageData.DURATION / 2,
                        CyTranslator().getText(
                            "TXT_KEY_MERC_AVAILABLE_NEAR_NEW_CITY", (pCity.getName(),)
                        ),
                        "",
                        0,
                        ArtFileMgr.getInterfaceArtInfo("INTERFACE_MERCENARY_ICON").getPath(),
                        ColorTypes(MessageData.LIME),
                        pCity.getX(),
                        pCity.getY(),
                        True,
                        True,
                    )
                    break

    def onCityBuilt(self, iCiv, pCity):
        # Absinthe: if there are mercs available in the new city's province, interface message about it to the human player
        iProvince = pCity.getProvince()
        self.getMercLists()  # load the current mercenary pool
        for lMerc in self.lGlobalPool:
            if lMerc[4] == iProvince:
                if iCiv == human():
                    CyInterface().addMessage(
                        iCiv,
                        False,
                        MessageData.DURATION / 2,
                        CyTranslator().getText(
                            "TXT_KEY_MERC_AVAILABLE_NEAR_NEW_CITY", (pCity.getName(),)
                        ),
                        "",
                        0,
                        ArtFileMgr.getInterfaceArtInfo("INTERFACE_MERCENARY_ICON").getPath(),
                        ColorTypes(MessageData.LIME),
                        pCity.getX(),
                        pCity.getY(),
                        True,
                        True,
                    )
                    break

    def onUnitPromoted(self, argsList):
        pUnit, iNewPromotion = argsList
        iMerc = pUnit.getMercID()
        if iMerc > -1:
            # redraw the main screen to update the upkeep info
            CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)

            lPromotionList = []
            # almost all promotions are available through experience, so this is not only for the otherwise used iNumTotalMercPromotions
            for iPromotion in range(len(Promotion) - 1):
                if pUnit.isHasPromotion(iPromotion):
                    lPromotionList.append(iPromotion)
            if iNewPromotion not in lPromotionList:
                lPromotionList.append(iNewPromotion)

            # get the new cost for this unit
            iOwner = pUnit.getOwner()
            iOldUpkeep = pUnit.getMercUpkeep()
            dummy, iNewUpkeep = self.GMU.getCost(iMerc, lPromotionList)
            iNewUpkeep = self.GMU.getModifiedCostPerPlayer(iNewUpkeep, iOwner)

            pUnit.setMercUpkeep(iNewUpkeep)

            pPlayer = gc.getPlayer(iOwner)
            pPlayer.setPicklefreeParameter(
                SpecialParameter.MERCENARY_COST_PER_TURN.value,
                max(
                    0,
                    pPlayer.getPicklefreeParameter(SpecialParameter.MERCENARY_COST_PER_TURN.value)
                    - iOldUpkeep
                    + iNewUpkeep,
                ),
            )
            # self.GMU.playerMakeUpkeepSane( iOwner )

    def onUnitKilled(self, argsList):
        pUnit, iAttacker = argsList

        iMerc = pUnit.getMercID()

        if iMerc > -1:
            lHiredByList = self.GMU.getMercHiredBy()
            if lHiredByList[iMerc] == -1:  # merc was fired, then don't remove permanently
                return
            # unit is gone
            pPlayer = gc.getPlayer(pUnit.getOwner())
            pPlayer.setPicklefreeParameter(
                SpecialParameter.MERCENARY_COST_PER_TURN.value,
                max(
                    0,
                    pPlayer.getPicklefreeParameter(SpecialParameter.MERCENARY_COST_PER_TURN.value)
                    - pUnit.getMercUpkeep(),
                ),
            )

            lHiredByList = self.GMU.getMercHiredBy()
            # remove the merc permanently
            lHiredByList[iMerc] = -2
            self.GMU.setMercHiredBy(lHiredByList)

    def onUnitLost(self, argsList):
        # this gets called on lost and on upgrade, check to remove the merc if it has not been upgraded?
        pUnit = argsList[0]
        iMerc = pUnit.getMercID()

        if iMerc > -1:
            # is a merc, check to see if it has just been killed
            lHiredByList = self.GMU.getMercHiredBy()
            if lHiredByList[iMerc] < 0:
                # unit has just been killed and onUnitKilled has been called or fired (-1 and -2)
                return

            # check to see if it has been replaced by an upgraded (promoted) version of itself
            # Get the list of units for the player
            iPlayer = pUnit.getOwner()
            # unitList = PyPlayer( iPlayer ).getUnitList()
            # for pTestUnit in unitList:
            # 	if ( pTestUnit.getMercID() == iMerc ):
            # 		return

            # unit is gone
            pPlayer = gc.getPlayer(iPlayer)
            pPlayer.setPicklefreeParameter(
                SpecialParameter.MERCENARY_COST_PER_TURN.value,
                max(
                    0,
                    pPlayer.getPicklefreeParameter(SpecialParameter.MERCENARY_COST_PER_TURN.value)
                    - pUnit.getMercUpkeep(),
                ),
            )

            # remove the merc (presumably disbanded here)
            lHiredByList[iMerc] = -1
            self.GMU.setMercHiredBy(lHiredByList)

    def processMercAI(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        if pPlayer.isHuman() or pPlayer.isBarbarian() or iPlayer == Civ.POPE.value:
            return

        iWarValue = 0  # compute the total number of wars being fought at the moment

        teamPlayer = gc.getTeam(pPlayer.getTeam())
        for iOponent in civilizations().drop(Civ.BARBARIAN).ids():
            if teamPlayer.isAtWar(gc.getPlayer(iOponent).getTeam()):
                iWarValue += 1
                if iOponent <= Civ.POPE.value:
                    iWarValue += 3

        # decide to hire or fire mercs
        # if we are at peace or have only a small war, then we can keep the merc if the expense is trivial
        # otherwise we should get rid of some mercs
        # we should also fire mercs if we spend too much

        bFire = False

        iGold = pPlayer.getGold()
        iUpkeep = pPlayer.getPicklefreeParameter(SpecialParameter.MERCENARY_COST_PER_TURN.value)

        if 100 * iGold < iUpkeep:
            # can't afford mercs, fire someone
            bFire = True
        elif iWarValue < 4 and 50 * iGold < iUpkeep:
            # mercs cost > 1/2 of our gold
            bFire = True
        elif iWarValue < 2 and 20 * iGold < iUpkeep:
            bFire = True

        if bFire:
            # the AI fires a Merc
            self.FireMercAI(iPlayer)

            # make sure we can affort the mercs that we keep
            while pPlayer.getPicklefreeParameter(
                SpecialParameter.MERCENARY_COST_PER_TURN.value
            ) > 0 and 100 * pPlayer.getGold() < pPlayer.getPicklefreeParameter(
                SpecialParameter.MERCENARY_COST_PER_TURN.value
            ):
                self.GMU.playerMakeUpkeepSane(pPlayer.getID())
                self.FireMercAI(iPlayer)
            return

        if iWarValue > 0:
            # we have to be at war to hire
            iOdds = civilization(iPlayer).misc.hire_mercenary_threshold
            if iWarValue < 2:
                iOdds *= 2  # small wars are hardly worth the trouble
            elif iWarValue > 4:  # large war
                iOdds /= 2

            if percentage_chance(iOdds, strict=True, reverse=True):
                self.HireMercAI(iPlayer)

    def FireMercAI(self, iPlayer):
        iGameTurn = turn()
        lMercs = [unit for unit in PyPlayer(iPlayer).getUnitList() if unit.getMercID() > -1]

        if lMercs:
            # we have mercs, so fire someone
            lMercValue = []  # estimate how "valuable" the merc is (high value is bad)
            for pUnit in lMercs:
                iValue = pUnit.getMercUpkeep()
                pPlot = gc.getMap().plot(pUnit.getX(), pUnit.getY())
                if pPlot.isCity():
                    if pPlot.getPlotCity().getOwner() == iPlayer:
                        # keep the city defenders
                        iDefenders = self.getNumDefendersAtPlot(pPlot)
                        if iDefenders < 2:
                            iValue /= 100
                        elif iDefenders < 4:
                            iValue /= 2

                if iGameTurn > lMercList[pUnit.getMercID()][3]:
                    # obsolete units
                    iValue *= 2
                if iGameTurn > lMercList[pUnit.getMercID()][3] + 100:
                    # really obsolete units
                    iValue *= 5
                lMercValue.append(iValue)

            iSum = 0
            for iTempValue in lMercValue:
                iSum += iTempValue

            iFireRand = rand(iSum)
            for iI in range(len(lMercValue)):
                iFireRand -= lMercValue[iI]
                if iFireRand < 0:
                    self.GMU.fireMerc(lMercs[iI])
                    return

    def HireMercAI(self, iPlayer):
        # decide which mercenary to hire
        lCanHireMercs = []
        pPlayer = gc.getPlayer(iPlayer)
        lPlayerProvinces = self.GMU.getCulturedProvinces(iPlayer)
        iGold = pPlayer.getGold()
        iStateReligion = pPlayer.getStateReligion()
        for lMerc in self.lGlobalPool:
            iMercTotalCost = self.GMU.getModifiedCostPerPlayer(
                lMerc[2] + (lMerc[3] + 99) / 100, iPlayer
            )
            if (
                iGold > iMercTotalCost
                and iStateReligion not in lMercList[lMerc[0]][5]
                and lMerc[4] in lPlayerProvinces
            ):
                lCanHireMercs.append(lMerc)

        if lCanHireMercs:
            self.GMU.hireMerc(choice(lCanHireMercs), iPlayer)
            self.getMercLists()

    def getNumDefendersAtPlot(self, pPlot):
        iOwner = pPlot.getOwner()
        if iOwner < 0:
            return 0
        iNumUnits = pPlot.getNumUnits()
        iDefenders = 0
        for i in range(iNumUnits):
            if pPlot.getUnit(i).getOwner() == iOwner:
                iDefenders += 1
        return iDefenders


class GlobalMercenaryUtils:
    # the idea of this class is to provide ways to manipulate the mercenaries without the need to make a separate instance of the MercenaryManager
    # the MercManager provides event driven functions and those should be called from the event interface
    # the Utils class should be used for interface commands (like for the Human UI)

    def getMercGlobalPool(self):
        return data.lMercGlobalPool

    def setMercGlobalPool(self, lNewPool):
        data.lMercGlobalPool = lNewPool

    def getMercHiredBy(self):
        return data.lMercsHiredBy

    def setMercHiredBy(self, lNewList):
        data.lMercsHiredBy = lNewList

    def getOwnedProvinces(self, iPlayer):
        lProvList = []  # all available cities that the Merc can appear in
        for city in utils.getCityList(iPlayer):
            iProvince = city.getProvince()
            if iProvince not in lProvList:
                lProvList.append(iProvince)
        return lProvList

    def getCulturedProvinces(self, iPlayer):
        lProvList = []  # all available cities that the Merc can appear in
        for city in utils.getCityList(iPlayer):
            iProvince = city.getProvince()
            if iProvince not in lProvList and city.getCultureLevel() >= 2:
                lProvList.append(iProvince)
        return lProvList

    def playerMakeUpkeepSane(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        lMercs = [unit for unit in PyPlayer(iPlayer).getUnitList() if unit.getMercID() > -1]

        iTotalUpkeep = 0
        for pUnit in lMercs:
            # iTotalUpkeep += self.getModifiedCostPerPlayer( pUnit.getMercUpkeep(), iPlayer )
            iTotalUpkeep += pUnit.getMercUpkeep()

        iSavedUpkeep = pPlayer.getPicklefreeParameter(
            SpecialParameter.MERCENARY_COST_PER_TURN.value
        )
        if iSavedUpkeep != iTotalUpkeep:
            pPlayer.setPicklefreeParameter(
                SpecialParameter.MERCENARY_COST_PER_TURN.value, iTotalUpkeep
            )
            return False
        return True

    def getCost(self, iMerc, lPromotions):
        # note that the upkeep is in the units of 100, i.e. iUpkeepCost = 100 means 1 gold
        lMercInfo = lMercList[iMerc]

        # compute cost
        iBaseCost = (
            30 + (85 * gc.getUnitInfo(lMercInfo[0]).getProductionCost()) / 100
        )  # note that this is the base production cost (between 30 and 200), without the civ-specific modifiers
        iPercentage = 0
        for iPromotion in lPromotions:
            iPercentage += lPromotionCost[iPromotion]
        iPromotionModifier = 100 + (iPercentage * 3) / 5  # in percentage
        iPurchaseCost = (iBaseCost * iPromotionModifier) / 100

        # 1 gold of upkeep for each 55 hammers in the unit's production cost
        # the minimum amount is 1,4 gold, the maximum is 4,5 gold for the base upkeep
        iUpkeepBaseCost = 85 + max(
            55, min((100 * gc.getUnitInfo(lMercInfo[0]).getProductionCost()) / 55, 365)
        )  # note that this is the base production cost (between 30 and 200), without the civ-specific modifiers
        iUpkeepPromotionModifier = 100 + (iPercentage * 2) / 5  # in percentage
        iUpkeepCost = (iUpkeepBaseCost * iUpkeepPromotionModifier) / 100

        return (iPurchaseCost, iUpkeepCost)

    def getModifiedCostPerPlayer(self, iCost, iPlayer):
        # Absinthe: we need to make it sure this is modified only once for each mercenary on the mercenary screen
        # 			handled on the screen separately, this should be fine the way it is now
        # 3MiroUP: this function gets called:
        # 	- every time a merc is hired (pPlayer.initUnit) to set the upkeep
        # 	- every time a merc cost is considered
        # 	- every time a merc cost is to be displayed (in the merc screen)
        return (iCost * lMercCostModifier[iPlayer]) / 100

    def hireMerc(self, lMerc, iPlayer):
        # the player would hire a merc
        lGlobalPool = self.getMercGlobalPool()
        lHiredByList = self.getMercHiredBy()
        iCost = self.getModifiedCostPerPlayer(lMerc[2], iPlayer)
        iUpkeep = self.getModifiedCostPerPlayer(lMerc[3], iPlayer)
        pPlayer = gc.getPlayer(iPlayer)
        if pPlayer.getGold() < iCost:
            return

        lCityList = []  # all available cities that the Merc can appear in
        for city in utils.getCityList(iPlayer):
            if city.getProvince() == lMerc[4]:
                # Absinthe: note that naval mercs can appear in all coastal cities if we have enough culture in the province (at least one cultured enough city)
                iMercType = lMercList[lMerc[0]][0]
                if gc.getUnitInfo(iMercType).getDomainType() == 0:
                    if city.isCoastal(1):
                        lCityList.append(city)
                # Absinthe: otherwise only in cities with enough culture
                else:
                    if city.getCultureLevel() >= 2:
                        lCityList.append(city)

        if not lCityList:
            return

        pCity = choice(lCityList)

        iX = pCity.getX()
        iY = pCity.getY()

        # do the Gold
        pPlayer.setGold(pPlayer.getGold() - iCost)
        pPlayer.setPicklefreeParameter(
            SpecialParameter.MERCENARY_COST_PER_TURN.value,
            pPlayer.getPicklefreeParameter(SpecialParameter.MERCENARY_COST_PER_TURN.value)
            + iUpkeep,
        )

        # remove the merc from the global pool and set the "hired by" index
        lGlobalPool.remove(lMerc)
        lHiredByList[lMerc[0]] = iPlayer

        self.setMercGlobalPool(lGlobalPool)
        self.setMercHiredBy(lHiredByList)

        # message for the human player if another civ hired a merc which was also available for him/her
        iHuman = human()
        if iPlayer != iHuman:
            lHumanProvList = self.getOwnedProvinces(iHuman)
            if lMerc[4] in lHumanProvList:
                szProvName = "TXT_KEY_PROVINCE_NAME_%i" % lMerc[4]
                szCurrentProvince = text(szProvName)
                CyInterface().addMessage(
                    iHuman,
                    False,
                    MessageData.DURATION / 2,
                    text("TXT_KEY_MERC_HIRED_BY_SOMEONE", szCurrentProvince),
                    "",
                    0,
                    "",
                    ColorTypes(MessageData.LIME),
                    -1,
                    -1,
                    True,
                    True,
                )

        # make the unit:
        pUnit = pPlayer.initUnit(
            lMercList[lMerc[0]][0], iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH
        )
        if lMercList[lMerc[0]][1] != "TXT_KEY_MERC_GENERIC":
            pUnit.setName(text(lMercList[lMerc[0]][1]))

        # add the promotions
        for iPromotion in lMerc[1]:
            pUnit.setHasPromotion(iPromotion, True)

        if not pUnit.isHasPromotion(Promotion.MERC.value):
            pUnit.setHasPromotion(Promotion.MERC.value, True)

        # set the MercID
        pUnit.setMercID(lMerc[0])

        # set the Upkeep
        pUnit.setMercUpkeep(iUpkeep)

    def fireMerc(self, pMerc):
        # fires the merc unit pMerc (pointer to CyUnit)
        lHiredByList = self.getMercHiredBy()

        # get the Merc info
        iMerc = pMerc.getMercID()
        iUpkeep = pMerc.getMercUpkeep()
        if iMerc < 0:
            return

        # free the Merc for a new contract
        lHiredByList[iMerc] = -1
        self.setMercHiredBy(lHiredByList)

        # lower the upkeep
        pPlayer = gc.getPlayer(pMerc.getOwner())
        pPlayer.setPicklefreeParameter(
            SpecialParameter.MERCENARY_COST_PER_TURN.value,
            max(
                0,
                pPlayer.getPicklefreeParameter(SpecialParameter.MERCENARY_COST_PER_TURN.value)
                - iUpkeep,
            ),
        )

        pMerc.kill(0, -1)
