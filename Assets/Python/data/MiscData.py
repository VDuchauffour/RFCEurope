from BaseStructures import EnumDataMapper
from CoreTypes import Civ, Company, Religion, Unit
from CoreStructures import CivDataMapper, CompanyDataMapper

WORLD_WIDTH = 100
WORLD_HEIGHT = 73

PLAGUE_IMMUNITY = 20
GREAT_PROPHET_FAITH_POINT_BONUS = 8
NUM_CRUSADES = 6
PROSECUTOR_UNITCLASS = 53

# Used for messages
class MessageData(object):
    DURATION = 14
    WHITE = 0
    RED = 7
    GREEN = 8
    BLUE = 9
    LIGHT_BLUE = 10
    YELLOW = 11
    DARK_PINK = 12
    LIGHT_RED = 20
    PURPLE = 25
    CYAN = 44
    BROWN = 55
    ORANGE = 88
    TAN = 90
    LIME = 100


MERCENARY_ONLY_UNITS = [
    Unit.CONDOTTIERI,
    Unit.REITER,
    Unit.BOHEMIAN_WAR_WAGON,
    Unit.CORSAIR,
    Unit.CRIMEAN_TATAR_RIDER,
    Unit.DON_COSSACK,
    Unit.DOPPELSOLDNER,
    Unit.HACKAPELL,
    Unit.HIGHLANDER,
    Unit.HIGHLANDER_GUN,
    Unit.IRISH_BRIGADE,
    Unit.LIPKA_TATAR,
    Unit.LOMBARD_HEAVY_FOOTMAN,
    Unit.MAMLUK_HEAVY_CAVALRY,
    Unit.NUBIAN_LONGBOWMAN,
    Unit.NAFFATUN,
    Unit.SOUTH_SLAV_VLASTELA,
    Unit.STRADIOT,
    Unit.SWISS_PIKEMAN,
    Unit.SWISS_GUN,
    Unit.TAGMATA,
    Unit.TOUAREG,
    Unit.TURKOPOLES,
    Unit.VARANGIAN_GUARD,
    Unit.WAARDGELDER,
    Unit.WALLOON_GUARD,
    Unit.WELSH_LONGBOWMAN,
    Unit.ZANJI,
    Unit.ZAPOROZHIAN_COSSACK,
]

BARBARIAN_ONLY_UNITS = [
    Unit.BEDOUIN,
    Unit.CORSAIR,
    Unit.HIGHLANDER,
    Unit.MONGOL_KESHIK,
    Unit.SELJUK_CROSSBOW,
    Unit.SELJUK_FOOTMAN,
    Unit.SELJUK_GUISARME,
    Unit.SELJUK_LANCER,
    Unit.SELJUK_SWORDSMAN,
    Unit.STEPPE_HORSE_ARCHER,
    Unit.TOUAREG,
    Unit.TURCOMAN_HORSE_ARCHER,
    Unit.WELSH_LONGBOWMAN,
]

COMPANY_LIMIT = CompanyDataMapper(
    {
        Company.HOSPITALLERS: 3,
        Company.TEMPLARS: 4,
        Company.TEUTONS: 3,
        Company.HANSA: 3,
        Company.MEDICI: 4,
        Company.AUGSBURG: 4,
        Company.ST_GEORGE: 3,
        Company.DRAGON: 5,
        Company.CALATRAVA: 5,
    }
)

CIV_DAWN_OF_MAN_VALUES = CivDataMapper(
    {
        Civ.BYZANTIUM: ("500", "TXT_KEY_AD"),
        Civ.FRANCE: ("500", "TXT_KEY_AD"),
        Civ.ARABIA: ("632", "TXT_KEY_AD"),
        Civ.BULGARIA: ("680", "TXT_KEY_AD"),
        Civ.CORDOBA: ("711", "TXT_KEY_AD"),
        Civ.VENECIA: ("810", "TXT_KEY_AD"),
        Civ.BURGUNDY: ("843", "TXT_KEY_AD"),
        Civ.GERMANY: ("856", "TXT_KEY_AD"),
        Civ.NOVGOROD: ("864", "TXT_KEY_AD"),
        Civ.NORWAY: ("872", "TXT_KEY_AD"),
        Civ.KIEV: ("880", "TXT_KEY_AD"),
        Civ.HUNGARY: ("895", "TXT_KEY_AD"),
        Civ.CASTILLE: ("910", "TXT_KEY_AD"),
        Civ.DENMARK: ("936", "TXT_KEY_AD"),
        Civ.SCOTLAND: ("960", "TXT_KEY_AD"),
        Civ.POLAND: ("966", "TXT_KEY_AD"),
        Civ.GENOA: ("1016", "TXT_KEY_AD"),
        Civ.MOROCCO: ("1040", "TXT_KEY_AD"),
        Civ.ENGLAND: ("1066", "TXT_KEY_AD"),
        Civ.PORTUGAL: ("1139", "TXT_KEY_AD"),
        Civ.ARAGON: ("1164", "TXT_KEY_AD"),
        Civ.SWEDEN: ("1210", "TXT_KEY_AD"),
        Civ.PRUSSIA: ("1224", "TXT_KEY_AD"),
        Civ.LITHUANIA: ("1236", "TXT_KEY_AD"),
        Civ.AUSTRIA: ("1282", "TXT_KEY_AD"),
        Civ.OTTOMAN: ("1356", "TXT_KEY_AD"),
        Civ.MOSCOW: ("1380", "TXT_KEY_AD"),
        Civ.DUTCH: ("1581", "TXT_KEY_AD"),
        Civ.POPE: ("500", "TXT_KEY_AD"),
    }
)

RELIGION_PERSECUTION_ORDER = EnumDataMapper(
    {
        Religion.PROTESTANTISM: [
            Religion.CATHOLICISM,
            Religion.ISLAM,
            Religion.ORTHODOXY,
            Religion.JUDAISM,
        ],
        Religion.ISLAM: [
            Religion.CATHOLICISM,
            Religion.ORTHODOXY,
            Religion.PROTESTANTISM,
            Religion.JUDAISM,
        ],
        Religion.CATHOLICISM: [
            Religion.ISLAM,
            Religion.PROTESTANTISM,
            Religion.JUDAISM,
            Religion.ORTHODOXY,
        ],
        Religion.ORTHODOXY: [
            Religion.ISLAM,
            Religion.JUDAISM,
            Religion.CATHOLICISM,
            Religion.PROTESTANTISM,
        ],
        Religion.JUDAISM: [
            Religion.ISLAM,
            Religion.PROTESTANTISM,
            Religion.ORTHODOXY,
            Religion.CATHOLICISM,
        ],
    }
)
