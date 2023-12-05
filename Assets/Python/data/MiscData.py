from BaseStructures import EnumDataMapper
from CoreTypes import Building, Civ, Company, Religion, Unit, Wonder
from CoreStructures import CivDataMapper, CompanyDataMapper

PLAGUE_IMMUNITY = 20
GREAT_PROPHET_FAITH_POINT_BONUS = 8
NUM_CRUSADES = 6
PROSECUTOR_UNITCLASS = 53

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
        Civ.CASTILE: ("910", "TXT_KEY_AD"),
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

RELIGIOUS_BUILDINGS = EnumDataMapper(
    {
        Religion.PROTESTANTISM: [
            Building.PROTESTANT_TEMPLE,
            Building.PROTESTANT_SCHOOL,
            Building.PROTESTANT_CATHEDRAL,
        ],
        Religion.ISLAM: [
            Religion.CATHOLICISM,
            Religion.ORTHODOXY,
            Religion.PROTESTANTISM,
            Religion.JUDAISM,
        ],
        Religion.CATHOLICISM: [
            Building.CATHOLIC_TEMPLE,
            Building.CATHOLIC_MONASTERY,
            Building.CATHOLIC_CATHEDRAL,
        ],
        Religion.ORTHODOXY: [
            Building.ISLAMIC_TEMPLE,
            Building.ISLAMIC_CATHEDRAL,
            Building.ISLAMIC_MADRASSA,
        ],
        Religion.JUDAISM: [],
    }
)

RELIGIOUS_WONDERS = [
    Wonder.MONASTERY_OF_CLUNY,
    Wonder.WESTMINSTER,
    Wonder.KRAK_DES_CHEVALIERS,
    Wonder.NOTRE_DAME,
    Wonder.PALAIS_DES_PAPES,
    Wonder.ST_BASIL,
    Wonder.SOPHIA_KIEV,
    Wonder.ST_CATHERINE_MONASTERY,
    Wonder.SISTINE_CHAPEL,
    Wonder.JASNA_GORA,
    Wonder.MONT_SAINT_MICHEL,
    Wonder.BOYANA_CHURCH,
    Wonder.FLORENCE_DUOMO,
    Wonder.BORGUND_STAVE_CHURCH,
    Wonder.DOME_ROCK,
    Wonder.THOMASKIRCHE,
    Wonder.BLUE_MOSQUE,
    Wonder.SELIMIYE_MOSQUE,
    Wonder.MOSQUE_OF_KAIROUAN,
    Wonder.KOUTOUBIA_MOSQUE,
    Wonder.LA_MEZQUITA,
    Wonder.SAN_MARCO,
    Wonder.STEPHANSDOM,
    Wonder.ROUND_CHURCH,
]

COMPANY_BUILDINGS = [
    Building.CORPORATION.value,
    Building.CORPORATION_2.value,
    Building.CORPORATION_3.value,
    Building.CORPORATION_4.value,
    Building.CORPORATION_5.value,
    Building.CORPORATION_6.value,
    Building.CORPORATION_7.value,
    Building.CORPORATION_8.value,
    Building.CORPORATION_9.value,
]

DIPLOMACY_MODIFIERS = [
    (Civ.CORDOBA, Civ.ARABIA, 5),
    (Civ.ARABIA, Civ.CORDOBA, 5),
    (Civ.ARABIA, Civ.BYZANTIUM, -8),
    (Civ.BYZANTIUM, Civ.ARABIA, -8),
    (Civ.BULGARIA, Civ.BYZANTIUM, 3),
    (Civ.BYZANTIUM, Civ.BULGARIA, 3),
    (Civ.CORDOBA, Civ.CASTILE, -14),
    (Civ.CASTILE, Civ.CORDOBA, -14),
    (Civ.MOROCCO, Civ.CASTILE, -10),
    (Civ.CASTILE, Civ.MOROCCO, -10),
    (Civ.ARAGON, Civ.CASTILE, 4),
    (Civ.CASTILE, Civ.ARAGON, 4),
    (Civ.PORTUGAL, Civ.CASTILE, 6),
    (Civ.CASTILE, Civ.PORTUGAL, 6),
    (Civ.CORDOBA, Civ.PORTUGAL, -8),
    (Civ.PORTUGAL, Civ.CORDOBA, -8),
    (Civ.KIEV, Civ.NOVGOROD, 5),
    (Civ.NOVGOROD, Civ.KIEV, 5),
    (Civ.MOSCOW, Civ.NOVGOROD, -8),
    (Civ.NOVGOROD, Civ.MOSCOW, -8),
    (Civ.FRANCE, Civ.BURGUNDY, -2),
    (Civ.BURGUNDY, Civ.FRANCE, -2),
    (Civ.OTTOMAN, Civ.BYZANTIUM, -14),
    (Civ.BYZANTIUM, Civ.OTTOMAN, -14),
    (Civ.GERMANY, Civ.POLAND, -5),
    (Civ.POLAND, Civ.GERMANY, -5),
    (Civ.MOSCOW, Civ.POLAND, -4),
    (Civ.POLAND, Civ.MOSCOW, -4),
    (Civ.MOSCOW, Civ.LITHUANIA, -2),
    (Civ.LITHUANIA, Civ.MOSCOW, -2),
    (Civ.AUSTRIA, Civ.POLAND, -2),
    (Civ.POLAND, Civ.AUSTRIA, -2),
    (Civ.LITHUANIA, Civ.POLAND, 4),
    (Civ.POLAND, Civ.LITHUANIA, 4),
    (Civ.HUNGARY, Civ.POLAND, 3),
    (Civ.POLAND, Civ.HUNGARY, 3),
    (Civ.AUSTRIA, Civ.HUNGARY, -6),
    (Civ.HUNGARY, Civ.AUSTRIA, -6),
    (Civ.SWEDEN, Civ.POLAND, -2),
    (Civ.POLAND, Civ.SWEDEN, -2),
    (Civ.SWEDEN, Civ.MOSCOW, -8),
    (Civ.MOSCOW, Civ.SWEDEN, -8),
    (Civ.PRUSSIA, Civ.POLAND, -6),
    (Civ.POLAND, Civ.PRUSSIA, -6),
    (Civ.PRUSSIA, Civ.LITHUANIA, -8),
    (Civ.LITHUANIA, Civ.PRUSSIA, -8),
    (Civ.ENGLAND, Civ.SCOTLAND, -8),
    (Civ.SCOTLAND, Civ.ENGLAND, -8),
    (Civ.FRANCE, Civ.SCOTLAND, 4),
    (Civ.SCOTLAND, Civ.FRANCE, 4),
    (Civ.NORWAY, Civ.DENMARK, 4),
    (Civ.DENMARK, Civ.NORWAY, 4),
    (Civ.SWEDEN, Civ.DENMARK, -4),
    (Civ.DENMARK, Civ.SWEDEN, -4),
]

HISTORICAL_ENEMIES = [
    (Civ.OTTOMAN, Civ.BULGARIA, 10),
    (Civ.BULGARIA, Civ.OTTOMAN, -10),
    (Civ.CASTILE, Civ.CORDOBA, 10),
    (Civ.CORDOBA, Civ.CASTILE, -10),
    (Civ.PORTUGAL, Civ.CASTILE, 10),
    (Civ.CASTILE, Civ.PORTUGAL, -10),
    (Civ.AUSTRIA, Civ.HUNGARY, 10),
    (Civ.HUNGARY, Civ.AUSTRIA, -10),
    (Civ.AUSTRIA, Civ.GERMANY, 10),
    (Civ.GERMANY, Civ.AUSTRIA, -10),
]
