from BaseStructures import CompanyDataMapper
from CoreTypes import Building, Civ, Company, Technology, Unit

PLAGUE_IMMUNITY = 20
GREAT_PROPHET_FAITH_POINT_BONUS = 8
NUM_CRUSADES = 6
PROSECUTOR_UNITCLASS = 53

REVEAL_DATE_TECHNOLOGY = Technology.CALENDAR

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

COMPANY_BUILDINGS = [
    Building.CORPORATION,
    Building.CORPORATION_2,
    Building.CORPORATION_3,
    Building.CORPORATION_4,
    Building.CORPORATION_5,
    Building.CORPORATION_6,
    Building.CORPORATION_7,
    Building.CORPORATION_8,
    Building.CORPORATION_9,
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

MODNET_EVENTS = {
    "CHANGE_COMMERCE_PERCENT": 1200,
}
