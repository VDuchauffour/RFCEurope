from Enum import Enum, IntEnum


class Civ(IntEnum):
    BYZANTIUM = 0
    FRANCE = 1
    ARABIA = 2
    BULGARIA = 3
    CORDOBA = 4
    VENECIA = 5
    BURGUNDY = 6
    GERMANY = 7
    NOVGOROD = 8
    NORWAY = 9
    KIEV = 10
    HUNGARY = 11
    CASTILLE = 12
    DENMARK = 13
    SCOTLAND = 14
    POLAND = 15
    GENOA = 16
    MOROCCO = 17
    ENGLAND = 18
    PORTUGAL = 19
    ARAGON = 20
    SWEDEN = 21
    PRUSSIA = 22
    LITHUANIA = 23
    AUSTRIA = 24
    OTTOMAN = 25
    MOSCOW = 26
    DUTCH = 27
    POPE = 28
    INDEPENDENT = 29
    INDEPENDENT_2 = 30
    INDEPENDENT_3 = 31
    INDEPENDENT_4 = 32
    BARBARIAN = 33


class CivilizationProperty(Enum):
    IS_PLAYABLE = 0
    IS_MINOR = 1


class CivGroup(Enum):
    EASTERN = 0
    CENTRAL = 1
    ATLANTIC = 2
    ISLAMIC = 3
    ITALIAN = 4
    SCANDINAVIAN = 5


class Scenario(Enum):
    i500AD = 0
    i1200AD = 1


class StartingSituation(Enum):
    WORKERS = 0
    GOLD = 1
    FAITH = 2


class Religion(Enum):
    PROTESTANTISM = 0
    ISLAM = 1
    CATHOLICISM = 2
    ORTHODOXY = 3
    JUDAISM = 4


class Company(Enum):
    HOSPITALLERS = 0
    TEMPLARS = 1
    TEUTONS = 2
    HANSA = 3
    MEDICI = 4
    AUGSBURG = 5
    ST_GEORGE = 6
    DRAGON = 7
    CALATRAVA = 8


class Technology(IntEnum):
    CALENDAR = 0  # early middle age
    ARCHITECTURE = 1
    BRONZE_CASTING = 2
    THEOLOGY = 3
    MANORIALISM = 4
    STIRRUP = 5
    ENGINEERING = 6
    CHAIN_MAIL = 7
    ART = 8
    MONASTICISM = 9
    VASSALAGE = 10
    ASTROLABE = 11
    MACHINERY = 12
    VAULTED_ARCHES = 13
    MUSIC = 14
    HERBAL_MEDICINE = 15
    FEUDALISM = 16
    FARRIERS = 17
    MAPMAKING = 18  # high middle age
    BLAST_FURNACE = 19
    SIEGE_ENGINES = 20
    GOTHIC_ARCHITECTURE = 21
    LITERATURE = 22
    CODEOFLAWS = 23
    ARISTOCRACY = 24
    LATEEN_SAILS = 25
    PLATE_ARMOR = 26
    MONUMENT_BUILDING = 27
    CLASSICAL_KNOWLEDGE = 28
    ALCHEMY = 29
    CIVIL_SERVICE = 30
    CLOCKMAKING = 31
    PHILOSOPHY = 32
    EDUCATION = 33
    GUILDS = 34
    CHIVALRY = 35
    OPTICS = 36  # late middle age
    REPLACEABLE_PARTS = 37
    PATRONAGE = 38
    GUNPOWDER = 39
    BANKING = 40
    MILITARY_TRADITION = 41
    SHIP_BUILDING = 42
    DRAMA = 43
    DIVINE_RIGHT = 44
    CHEMISTRY = 45
    PAPER = 46
    PROFESSIONAL_ARMY = 47
    PRINTING_PRESS = 48
    PUBLIC_WORKS = 49
    MATCH_LOCK = 50
    ARABIC_KNOWLEDGE = 51
    ASTRONOMY = 52  # renaissance
    STEAM_ENGINES = 53
    CONSTITUTION = 54
    POLYGONAL_FORT = 55
    ARABIC_MEDICINE = 56
    RENAISSANCE_ART = 57
    NATIONALISM = 58
    LIBERALISM = 59
    SCIENTIFIC_METHOD = 60
    MILITARY_TACTICS = 61
    NAVAL_ARCHITECTURE = 62
    CIVIL_ENGINEERING = 63
    RIGHT_OF_MAN = 64
    ECONOMICS = 65
    PHYSICS = 66
    BIOLOGY = 67
    COMBINED_ARMS = 68
    TRADING_COMPANIES = 69
    MACHINE_TOOLS = 70
    FREE_MARKET = 71
    EXPLOSIVES = 72
    MEDICINE = 73
    INDUSTRIAL_TECH = 74


class Unit(Enum):
    SETTLER = 0
    WORKER = 1
    CATHOLIC_MISSIONARY = 2
    ORTHODOX_MISSIONARY = 3
    PROTESTANT_MISSIONARY = 4
    ISLAMIC_MISSIONARY = 5
    ARCHER = 6
    CROSSBOWMAN = 7
    ARBALEST = 8
    GENOA_BALESTRIERI = 9
    LONGBOWMAN = 10
    ENGLISH_LONGBOWMAN = 11
    SPEARMAN = 12
    GUISARME = 13
    ARAGON_ALMOGAVAR = 14
    SCOTLAND_SHELTRON = 15
    PIKEMAN = 16
    HOLY_ROMAN_LANDSKNECHT = 17
    AXEMAN = 18
    VIKING_BERSERKER = 19
    SWORDSMAN = 20
    DENMARK_HUSKARL = 21
    LONG_SWORDSMAN = 22
    MACEMAN = 23
    PORTUGAL_FOOT_KNIGHT = 24
    LITHUANIAN_BAJORAS = 25
    NOVGOROD_USHKUINIK = 26
    GRENADIER = 27
    NETHERLANDS_GRENADIER = 28
    ARQUEBUSIER = 29
    MUSKETMAN = 30
    SWEDISH_KAROLIN = 31
    SPANISH_TERCIO = 32
    FRENCH_MUSKETEER = 33
    MOROCCO_BLACKGUARD = 34
    LINE_INFANTRY = 35
    DRAGOON = 36
    SCOUT = 37
    MOUNTED_INFANTRY = 38
    HORSE_ARCHER = 39
    PISTOLIER = 40
    HUSSAR = 41
    PRUSSIA_DEATHS_HEADHUSSAR = 42
    LANCER = 43
    BULGARIAN_KONNIK = 44
    CORDOBAN_BERBER = 45
    HEAVY_LANCER = 46
    HUNGARIAN_HUSZAR = 47
    ARABIA_GHAZI = 48
    BYZANTINE_CATAPHRACT = 49
    KIEV_DRUZHINA = 50
    KNIGHT = 51
    MOSCOW_BOYAR = 52
    BURGUNDIAN_PALADIN = 53
    CUIRASSIER = 54
    AUSTRIAN_KURASSIER = 55
    POLISH_WINGED_HUSSAR = 56
    TEMPLAR = 57
    TEUTONIC = 58
    KNIGHT_OF_ST_JOHNS = 59
    DRAGON_KNIGHT = 60
    CALATRAVA_KNIGHT = 61
    CATAPULT = 62
    TREBUCHET = 63
    BOMBARD = 64
    TURKEY_GREAT_BOMBARD = 65
    CANNON = 66
    FIELD_ARTILLERY = 67
    WORKBOAT = 68
    GALLEY = 69
    COGGE = 70
    HOLK = 71
    GALLEON = 72
    WAR_GALLEY = 73
    GUN_GALLEY = 74
    VENICE_GALLEAS = 75
    CARRACK = 76
    FRIGATE = 77
    CARAVEL = 78
    PRIVATEER = 79
    SPY = 80
    PROSECUTOR = 81
    HOLY_RELIC = 82
    GREAT_PROPHET = 83
    GREAT_ARTIST = 84
    GREAT_SCIENTIST = 85
    GREAT_MERCHANT = 86
    GREAT_ENGINEER = 87
    GREAT_GENERAL = 88
    GREAT_SPY = 89
    MONGOL_KESHIK = 90
    SELJUK_LANCER = 91
    JANISSARY = 92
    TAGMATA = 93
    CORSAIR = 94
    HIGHLANDER = 95
    WELSH_LONGBOWMAN = 96
    CONDOTTIERI = 97
    SWISS_PIKEMAN = 98
    VARANGIAN_GUARD = 99
    HACKAPELL = 100
    REITER = 101
    ZAPOROZHIAN_COSSACK = 102
    DON_COSSACK = 103
    DOPPELSOLDNER = 104
    IRISH_BRIGADE = 105
    STRADIOT = 106
    WAARDGELDER = 107
    NAFFATUN = 108
    TURKOPOLES = 109
    WALLOON_GUARD = 110
    SWISS_GUN = 111
    LIPKA_TATAR = 112
    HIGHLANDER_GUN = 113
    ZANJI = 114
    TOUAREG = 115
    NUBIAN_LONGBOWMAN = 116
    BEDOUIN = 117
    TURCOMAN_HORSE_ARCHER = 118
    MAMLUK_HEAVY_CAVALRY = 119
    SOUTH_SLAV_VLASTELA = 120
    BOHEMIAN_WAR_WAGON = 121
    LOMBARD_HEAVY_FOOTMAN = 122
    STEPPE_HORSE_ARCHER = 123
    CRIMEAN_TATAR_RIDER = 124
    SELJUK_CROSSBOW = 125
    SELJUK_SWORDSMAN = 126
    SELJUK_FOOTMAN = 127
    SELJUK_GUISARME = 128


class Bonus(Enum):
    HEMP = 0
    COAL = 1
    COPPER = 2
    HORSE = 3
    IRON = 4
    MARBLE = 5
    STONE = 6
    BANANA = 7
    CLAM = 8
    CORN = 9
    COW = 10
    CRAB = 11
    DEER = 12
    FISH = 13
    PIG = 14
    RICE = 15
    SHEEP = 16
    WHEAT = 17
    DYE = 18
    FUR = 19
    GEMS = 20
    GOLD = 21
    INCENSE = 22
    IVORY = 23
    SILK = 24
    SILVER = 25
    SPICES = 26
    SUGAR = 27
    WINE = 28
    WHALE = 29
    COTTON = 30
    APPLE = 31
    BARLEY = 32
    HONEY = 33
    POTATO = 34
    SALT = 35
    SULPHUR = 36
    TIMBER = 37
    COFFEE = 38
    SLAVES = 39
    TEA = 40
    TOBACCO = 41
    OLIVES = 42
    ACCESS = 43
    NORTH_ACCESS = 44
    SOUTH_ACCESS = 45
    ASIA_ACCESS = 46
    AMBER = 47
    CITRUS = 48
    DATES = 49
    CAMELS = 50
    COCOA = 51
    OPIUM = 52


class Building(Enum):
    PALACE = 0
    SUMMER_PALACE = 1
    HEROIC_EPIC = 2
    NATIONAL_EPIC = 3
    NATIONAL_THEATRE = 4
    NATIONAL_GALLERY = 5
    NATIONAL_UNIVERSITY = 6
    ROYAL_DUNGEON = 7
    ROYAL_ACADEMY = 8
    STAR_FORT = 9
    WALLS = 10
    MOROCCO_KASBAH = 11
    CASTLE = 12
    MOSCOW_KREMLIN = 13
    HUNGARIAN_STRONGHOLD = 14
    SPANISH_CITADEL = 15
    BARRACKS = 16
    ARCHERY_RANGE = 17
    STABLE = 18
    BULGARIAN_STAN = 19
    GRANARY = 20
    CORDOBAN_NORIA = 21
    POLISH_FOLWARK = 22
    SMOKEHOUSE = 23
    SCOTLAND_SHIELING = 24
    AQUEDUCT = 25
    OTTOMAN_HAMMAM = 26
    HARBOR = 27
    VIKING_TRADING_POST = 28
    LIGHTHOUSE = 29
    PORTUGAL_FEITORIA = 30
    ARAGON_SEAPORT = 31
    WHARF = 32
    CUSTOM_HOUSE = 33
    DRYDOCK = 34
    FORGE = 35
    GUILD_HALL = 36
    NOVGOROD_KONETS = 37
    TEXTILE_MILL = 38
    UNIVERSITY = 39
    OBSERVATORY = 40
    PRUSSIA_PUBLIC_SCHOOL = 41
    DENMARK_RESEARCH_INSTITUTE = 42
    APOTHECARY = 43
    HOSPITAL = 44
    THEATRE = 45
    BYZANTINE_HIPPODROME = 46
    AUSTRIAN_OPERA_HOUSE = 47
    MARKET = 48
    ARABIC_CARAVAN = 49
    BREWERY = 50
    BURGUNDIAN_WINERY = 51
    JEWELER = 52
    WEAVER = 53
    TANNERY = 54
    INN = 55
    COFFEE_HOUSE = 56
    LUXURY_STORE = 57
    WAREHOUSE = 58
    BANK = 59
    GENOA_BANK = 60
    ENGLISH_ROYAL_EXCHANGE = 61
    MANOR_HOUSE = 62
    FRENCH_CHATEAU = 63
    VENICE_NAVAL_BASE = 64
    COURTHOUSE = 65
    KIEV_VECHE = 66
    HOLY_ROMAN_RATHAUS = 67
    LITHUANIAN_VOIVODESHIP = 68
    DUNGEON = 69
    NIGHT_WATCH = 70
    SWEDISH_TENNANT = 71
    LEVEE = 72
    NETHERLANDS_DIKE = 73
    PAGAN_SHRINE = 74
    JEWISH_QUARTER = 75
    JEWISH_SHRINE = 76
    PROTESTANT_TEMPLE = 77
    PROTESTANT_SCHOOL = 78
    PROTESTANT_CATHEDRAL = 79
    PROTESTANT_CHAPEL = 80
    PROTESTANT_SEMINARY = 81
    PROTESTANT_SHRINE = 82
    ISLAMIC_TEMPLE = 83
    ISLAMIC_CHAPEL = 84
    ISLAMIC_CATHEDRAL = 85
    ISLAMIC_SCHOOL = 86
    ISLAMIC_MADRASSA = 87
    ISLAMIC_SHRINE = 88
    CATHOLIC_TEMPLE = 89
    CATHOLIC_CATHEDRAL = 90
    CATHOLIC_CHAPEL = 91
    CATHOLIC_MONASTERY = 92
    CATHOLIC_SEMINARY = 93
    CATHOLIC_SHRINE = 94
    ORTHODOX_TEMPLE = 95
    ORTHODOX_CATHEDRAL = 96
    ORTHODOX_CHAPEL = 97
    ORTHODOX_MONASTERY = 98
    ORTHODOX_SEMINARY = 99
    ORTHODOX_SHRINE = 100
    RELIQUARY = 101
    INFIRMARY = 102
    KONTOR = 103
    CORPORATION1 = 104
    CORPORATION2 = 105
    CORPORATION3 = 106
    CORPORATION4 = 107
    CORPORATION5 = 108
    CORPORATION6 = 109
    CORPORATION7 = 110
    CORPORATION8 = 111
    CORPORATION9 = 112
    TRIUMPHAL_ARCH = 175
    PLAGUE = 176
    BUILDING_PLAGE = 177


class Wonder(Enum):
    VERSAILLES = 113
    NOTRE_DAME = 114
    LEANING_TOWER = 115
    SISTINE_CHAPEL = 116
    THEODOSIAN_WALLS = 117
    TOPKAPI_PALACE = 118
    JASNAGORA = 119
    SHRINE_OF_UPPSALA = 120
    SAMOGITIAN_ALKAS = 121
    GEDIMINAS_TOWER = 122
    GRAND_ARSENAL = 123
    GALATA_TOWER = 124
    KIZIL_KULE = 125
    MONT_SAINT_MICHEL = 126
    BOYANA_CHURCH = 127
    TORRE_DEL_ORO = 128
    FLORENCE_DUOMO = 129
    BORGUND_STAVE_CHURCH = 130
    BLUE_MOSQUE = 131
    SELIMIYE_MOSQUE = 132
    ALAZHAR = 133
    MOSQUE_OF_KAIROUAN = 134
    KOUTOUBIA_MOSQUE = 135
    ST_CATHERINE_MONASTERY = 136
    GREAT_LIGHTHOUSE = 137
    ALHAMBRA = 138
    KRAK_DES_CHEVALIERS = 139
    SAN_MARCO = 140
    LA_MEZQUITA = 141
    ST_BASIL = 142
    MAGNA_CARTA = 143
    SOPHIA_KIEV = 144
    DOME_ROCK = 145
    BRANDENBURG_GATE = 146
    PALACIO_DA_PENA = 147
    MONASTERY_OF_CLUNY = 148
    ROUND_CHURCH = 149
    LEONARDOS_WORKSHOP = 150
    GARDENS_AL_ANDALUS = 151
    MAGELLANS_VOYAGE = 152
    MARCO_POLO = 153
    ESCORIAL = 154
    KAZIMIERZ = 155
    BELEM_TOWER = 156
    GOLDEN_BULL = 157
    KALMARC_ASTLE = 158
    PALAIS_DES_PAPES = 159
    TOMB_AL_WALID = 160
    STEPHANSDOM = 161
    BIBLIOTHE_CACORVINIANA = 162
    LOUVRE = 163
    PETERHOF_PALACE = 164
    URANIBORG = 165
    THOMASKIRCHE = 166
    FONTAINEBLEAU = 167
    IMPERIAL_DIET = 168
    BEURS = 169
    COPERNICUS = 170
    SAN_GIORGIO = 171
    WESTMINSTER = 172
    PRESSBURG = 173
    LANTERNA = 174


class Colony(Enum):
    VINLAND = 0
    GOLD_COAST = 1
    IVORY_COAST = 2
    CUBA = 3
    HISPANIOLA = 4
    BRAZIL = 5
    HUDSON = 6
    VIRGINIA = 7
    EAST_AFRICA = 8
    CHINA = 9
    INDIA = 10
    EAST_INDIES = 11
    MALAYSIA = 12
    CAPE_TOWN = 13
    AZTECS = 14
    INCA = 15
    QUEBEC = 16
    NEW_ENGLAND = 17
    JAMAICA = 18
    PANAMA = 19
    LOUISIANA = 20
    PHILIPPINES = 21


class Project(Enum):
    ENCYCLOPEDIE = 0
    EAST_INDIA_COMPANY = 1
    WEST_INDIA_COMPANY = 2


class Specialist(Enum):
    CITIZEN = 0
    PRIEST = 1
    ARTIST = 2
    SCIENTIST = 3
    MERCHANT = 4
    ENGINEER = 5
    SPY = 6
    GREAT_PROPHET = 7
    GREAT_ARTIST = 8
    GREAT_SCIENTIST = 9
    GREAT_MERCHANT = 10
    GREAT_ENGINEER = 11
    GREAT_GENERAL = 12
    GREATSPY = 13


class Era(Enum):
    EARLY_MIDDLE_AGE = 0
    HIGH_MIDDLE_AGE = 1
    LATE_MIDDLE_AGE = 2
    RENAISSANCE = 3


class Improvement(Enum):
    LAND_WORKED = 0
    WATER_WORKED = 1
    CITY_RUINS = 2
    GOODY_HUT = 3
    FARM = 4
    FISHING_BOATS = 5
    WHALING_BOATS = 6
    MINE = 7
    WORKSHOP = 8
    LUMBERMILL = 9
    WINDMILL = 10
    WATERMILL = 11
    PLANTATION = 12
    QUARRY = 13
    PASTURE = 14
    CAMP = 15
    COLONIAL_TRADE = 16
    WINERY = 17
    COTTAGE = 18
    HAMLET = 19
    VILLAGE = 20
    TOWN = 21
    FORT = 22
    FOREST_PRESERVE = 23
    APIARY = 24


class Civic(Enum):
    DESPOTISM = 0
    FEUDAL_MONARCHY = 1
    DIVINE_MONARCHY = 2
    LIMITE_DMONARCHY = 3
    MERCHANT_REPUBLIC = 4
    TIBAL_LAW = 5
    FEUDAL_LAW = 6
    BUREAUCRACY = 7
    RELIGIOUS_LAW = 8
    COMMON_LAW = 9
    TRIBALISM = 10
    SERFDOM = 11
    FREE_PEASANTRY = 12
    APPRENTICESHIP = 13
    FREE_LABOR = 14
    DECENTRALIZATION = 15
    MANORIALISM = 16
    TRADE_ECONOMY = 17
    GUILDS = 18
    MERCANTILISM = 19
    PAGANISM = 20
    STATE_RELIGION = 21
    THEOCRACY = 22
    ORGANIZED_RELIGION = 23
    FREE_RELIGION = 24
    SUBJUGATION = 25
    VASSALAGE = 26
    IMPERIALISM = 27
    OCCUPATION = 28
    COLONIALISM = 29


class Feature(Enum):
    ICE = 0
    JUNGLE = 1
    DENSEFOREST = 2
    OASIS = 3
    FLOODPLAINS = 4
    WOODLAND = 5
    MARSH = 6
    PALMFOREST = 7
    ISLANDS = 8
    REEF = 9
    PYRAMID = 10


class Terain(Enum):
    GRASS = 0
    PLAINS = 1
    SEMIDESERT = 2
    DESERT = 3
    WETLAND = 4
    MOORLAND = 5
    TUNDRA = 6
    SNOW = 7
    FRESHLAKE = 8
    SALTLAKE = 9
    COAST = 10
    OCEAN = 11
    PEAK = 12
    HILL = 13


class Promotion(Enum):
    COMBAT = 0
    COMBAT_2 = 1
    COMBAT_3 = 2
    COMBAT_4 = 3
    COMBAT_5 = 4
    COVER = 5
    SHOCK = 6
    PINCH = 7
    FORMATION = 8
    CHARGE = 9
    AMBUSH = 10
    FEINT = 11
    AMPHIBIOUS = 12
    MARCH = 13
    MEDIC = 14
    MEDIC_2 = 15
    GUERILLA = 16
    GUERILLA_2 = 17
    GUERILLA_3 = 18
    WOODSMAN = 19
    WOODSMAN_2 = 20
    WOODSMAN_3 = 21
    CITYRAIDER = 22
    CITYRAIDER_2 = 23
    CITYRAIDER_3 = 24
    CITYGARRISON = 25
    CITYGARRISON_2 = 26
    CITYGARRISON_3 = 27
    DRILL = 28
    DRILL_2 = 29
    DRILL_3 = 30
    DRILL_4 = 31
    BARRAGE = 32
    BARRAGE_2 = 33
    BARRAGE_3 = 34
    ACCURACY = 35
    FLANKING = 36
    FLANKING_2 = 37
    SENTRY = 38
    MOBILITY = 39
    NAVIGATION = 40
    NAVIGATION_2 = 41
    CARGO = 42
    LEADER = 43
    LEADERSHIP = 44
    TACTICS = 45
    COMMANDO = 46
    COMBAT_6 = 47
    MORALE = 48
    MEDIC_3 = 49
    MERC = 50


class LeaderType(Enum):
    PRIMARY = 0
    EARLY = 1
    LATE = 2


class Leader(Enum):
    BARBARIAN = 0
    YAQUB_AL_MANSUR = 1
    MARIA_THERESA = 2
    ABU_BAKR = 3
    JOAN = 4
    MATTHIAS = 5
    BARBAROSSA = 6
    CATHERINE = 7
    CHARLEMAGNE = 8
    PHILIP_II = 9
    SOBIESKI = 10
    CHRISTIAN_IV = 11
    WILLIAM = 12
    AFONSO = 13
    MEHMED = 14
    SALADIN = 15
    MAXIMILIAN = 16
    SIMEON = 17
    PHILIP_THE_BOLD = 18
    JUSTINIAN = 19
    ABD_AR_RAHMAN = 20
    WILLEM_VAN_ORANJE = 21
    ELIZABETH = 22
    LOUIS_XIV = 23
    BOCCANEGRA = 24
    FREDERICK = 25
    STEPHEN = 26
    YAROSLAV = 27
    PETER = 28
    CASIMIR = 29
    JOAO = 30
    ISABELLA = 31
    GUSTAV_VASA = 32
    SULEIMAN = 33
    ENRICO_DANDOLO = 34
    THE_POPE = 35
    HARALD_HARDRADA = 36
    IVAN_IV = 37
    GEORGE_III = 38
    MARIA_I = 39
    ANDREA_GRITTI = 40
    HAAKON_IV = 41
    MINDAUGAS = 42
    VYTAUTAS = 43
    KARL_XII = 44
    IVAN_ASEN = 45
    HARUN_AL_RASHID = 46
    BELA_III = 47
    GUSTAV_ADOLF = 48
    BASIL_II = 49
    PALAIOLOGOS = 50
    MARGARET_I = 51
    MIESZKO = 52
    PHILIP_AUGUSTUS = 53
    MSTISLAV = 54
    FERDINAND_III = 55
    BOHDAN_KHMELNYTSKY = 56
    MOHAMMED_IBN_NASR = 57
    OTTO_I = 58
    OTTO_WILLIAM = 59
    BEATRICE = 60
    EMBRIACO = 61
    ROBERT_THE_BRUCE = 62
    RURIK = 63
    ALEXANDER_NEVSKY = 64
    MARFA = 65
    ISMAIL_IBN_SHARIF = 66
    HERMANN_VON_SALZA = 67
    JAMES_I = 68
    HARALD_BLUETOOTH = 69
    MAGNUS_LADULAS = 70
    JAMES_IV = 71
    JOHAN_DE_WITT = 72
    JOHN_II = 73


class UniquePower(Enum):
    HAPPINESS_BONUS = 0
    PER_CITY_COMMERCE_BONUS = 1
    CITY_TILE_YIELD_BONUS = 2
    NO_INSTABILITY_WITH_FOREIGN_RELIGION = 3
    NO_UNHAPPINESS_WITH_FOREIGN_CULTURE = 4
    COMMERCE_BONUS = 5  # currently unused
    FASTER_UNIT_PRODUCTION = 6
    PRE_ACCESS_CIVICS = 7
    EXTRA_TRADE_ROUTES = 8
    IMPROVEMENT_BONUS = 9
    PROMOTION_FOR_ALL_VALID_UNITS = 10
    PROMOTION_FOR_ALL_UNITS = 11  # currently unused
    CAN_ENTER_TERRAIN = 12
    NO_RESISTANCE = 13
    CONSCRIPTION = 14  # currently unused
    LESS_INSTABILITY_WITH_RELIGIOUS_PROSECUTION = 15
    NO_COLLAPSE_IN_CORE_AND_NORMAL_AREAS = 16
    SPREAD_STATE_RELIGION_TO_NEW_CITIES = 17
    HALVE_COST_OF_MERCENARIES = 18
    LESS_INSTABILITY_WITH_FOREIGN_LAND = 19
    LOWER_COST_FOR_PROJECTS = 20
    LOWER_CITY_MAINTENANCE_COST = 21
    ALLOW_SHIPS_IN_FOREIGN_SEA = 22  # currently unused (allowed by default for all civs)
    IMPROVE_GAIN_FAITH_POINTS = 23
    CULTURE_BONUS_WITH_NO_STATE_RELIGION = 24
    HAPPINESS_BONUS_WITH_NO_STATE_RELIGION = 25
    GROWTH_CITY_WITH_HEALTH_EXCESS = 26
    TERRAIN_BONUS = 27
    FEATURE_BONUS = 28
    STABILITY_BONUS_WITH_CONQUEST = 29  # currently unused
    STABILITY_BONUS_FOUNDING = 30  # currently unused
    STABILITY_PLACEHOLDER = 31  # currently unused
    STABILITY_PLACEHOLDER_2 = 32  # currently unused
    FREE_UNITS_WITH_FOREIGN_RELIGIONS = 33
    IMPROVEMENT_BONUS_2 = 3
    IMPROVEMENT_BONUS_3 = 35
    IMPROVEMENT_BONUS_4 = 36
    IMPROVEMENT_BONUS_5 = 37
    GOLD_BONUS_WITH_COASTAL_CITIES = 38
    NO_INSTABILITY_WITH_CIVIC_AND_STATE_RELIGION_CHANGE = 39
    EXTRA_COMMERCE_BONUS = 40
    EXTRA_UNITS_WHEN_LOSING_CITY = 41


class FaithPointBonusCategory(Enum):
    BOOST_STABILITY = 0
    REDUCE_CIVIC_UPKEEP = 1
    FASTER_POP_GROWTH = 2
    REDUCING_COST_UNITS = 3
    REDUCING_TECH_COST = 4
    REDUCING_WONDER_COST = 5
    BOOST_DIPLOMACY = 6


class StabilityCategory(Enum):
    CITIES = 0
    CIVICS = 1
    ECONOMY = 2
    EXPANSION = 3


class SpecialParameter(Enum):
    HAS_STEPHANSDOM = 0
    HAS_ESCORIAL = 1
    MERCENARY_COST_PER_TUN = 2
    JANISSARY_POINTS = 3
    HAS_UPPSALA_SHRINE = 4
    HAS_KOUTOUBIA_MOSQUE = 5
    HAS_MAGNACARTA = 6
    HAS_GALATA_TOWER = 7


class Area(Enum):
    TILE_MIN = 0
    TILE_MAX = 1
    ADDITIONAL_TILES = 2
    EXCEPTION_TILES = 3


class AreaTypes(IntEnum):
    CORE = 0
    NORMAL = 1
    BROADER = 2


class ProvinceTypes(Enum):
    NONE = 0
    OUTER = 1
    POTENTIAL = 2
    NATURAL = 3
    CORE = 4


class ProvinceStatus(Enum):
    LOST = 2
    DOMINATE = 3
    CONQUER = 4
    OWN = 5


class Province(Enum):
    GALICIA = 0
    CASTILE = 1
    NAVARRE = 2
    LEON = 3
    LUSITANIA = 4
    LA_MANCHA = 5
    CATALONIA = 6
    ARAGON = 7
    VALENCIA = 8
    ANDALUSIA = 9
    BRETAGNE = 10
    NORMANDY = 11
    AQUITAINE = 12
    ILE_DE_FRANCE = 13
    PROVENCE = 14
    BURGUNDY = 15
    ORLEANS = 16
    CHAMPAGNE = 17
    FLANDERS = 18
    NETHERLANDS = 19
    LONDON = 20
    WESSEX = 21
    WALES = 22
    SCOTLAND = 23
    IRELAND = 24
    MERCIA = 25
    EAST_ANGLIA = 26
    NORTHUMBRIA = 27
    THE_ISLES = 28
    ICELAND = 29
    DENMARK = 30
    OSTERLAND = 31
    NORWAY = 32
    VESTFOLD = 33
    GOTALAND = 34
    SVEALAND = 35
    NORRLAND = 36
    JAMTLAND = 37
    SKANELAND = 38
    GOTLAND = 39
    SWABIA = 40
    BAVARIA = 41
    BOHEMIA = 42
    SAXONY = 43
    LORRAINE = 44
    FRANCONIA = 45
    BRANDENBURG = 46
    HOLSTEIN = 47
    PRUSSIA = 48
    DUMMY = 49
    POMERANIA = 50
    GALICJA = 51
    GREATER_POLAND = 52
    MASOVIA = 53
    LESSER_POLAND = 54
    SUVALKIJA = 55
    LITHUANIA = 56
    LIVONIA = 57
    ESTONIA = 58
    DUMMY_2 = 59
    CARINTHIA = 60
    AUSTRIA = 61
    SLAVONIA = 62
    DUMMY_3 = 63
    TRANSYLVANIA = 64
    HUNGARY = 65
    MORAVIA = 66
    SILESIA = 67
    PANNONIA = 68
    UPPER_HUNGARY = 69
    LOMBARDY = 70
    VERONA = 71
    TUSCANY = 72
    LATIUM = 73
    CALABRIA = 74
    APULIA = 75
    LIGURIA = 76
    ARBERIA = 77
    DALMATIA = 78
    BANAT = 79
    MOESIA = 80
    CONSTANTINOPLE = 81
    THRACE = 82
    THESSALY = 83
    MACEDONIA = 84
    SERBIA = 85
    BOSNIA = 86
    EPIRUS = 87
    MOREA = 88
    WALLACHIA = 89
    JERUSALEM = 90
    PAPHLAGONIA = 91
    OPSIKION = 92
    THRAKESION = 93
    CILICIA = 94
    ANATOLIKON = 95
    ARMENIAKON = 96
    CHARSIANON = 97
    COLONEA = 98
    ANTIOCHIA = 99
    SYRIA = 100
    LEBANON = 101
    ARABIA = 102
    EGYPT = 103
    CYRENAICA = 104
    TRIPOLITANIA = 105
    IFRIQIYA = 106
    ALGIERS = 107
    TETOUAN = 108
    ORAN = 109
    SICILY = 110
    CRETE = 111
    CYPRUS = 112
    RHODES = 113
    CORSICA = 114
    SARDINIA = 115
    BALEARS = 116
    CANARIES = 117
    AZORES = 118
    MOROCCO = 119
    MOLDOVA = 120
    CRIMEA = 121
    NOVGOROD = 122
    KUBAN = 123
    ZAPORIZHIA = 124
    ROSTOV = 125
    MOSCOW = 126
    VOLOGDA = 127
    SMOLENSK = 128
    POLOTSK = 129
    MUROM = 130
    CHERNIGOV = 131
    PEREYASLAVL = 132
    SLOBODA = 133
    DONETS = 134
    KIEV = 135
    PODOLIA = 136
    MINSK = 137
    BREST = 138
    SIMBIRSK = 139
    NIZHNYNOVGOROD = 140
    KARELIA = 141
    VOLHYNIA = 142
    SAHARA = 143
    THESSALONIKI = 144
    MARRAKESH = 145
    MADEIRA = 146
    MALTA = 147
    FEZ = 148
    PICARDY = 149


class Region(Enum):
    IBERIA = 0
    FRANCE = 1
    BURGUNDY = 2
    BRITAIN = 3
    SCANDINAVIA = 4
    GERMANY = 5
    POLAND = 6
    LITHUANIA = 7
    AUSTRIA = 8
    HUNGARY = 9
    BALKANS = 10
    GREECE = 11
    ASIA_MINOR = 12
    MIDDLE_EAST = 13
    AFRICA = 14
    KIEV = 15
    ITALY = 16
    SWISS = 17
    NOT_EUROPE = 18


class Lake(Enum):
    LOUGH_NEAGH = 0
    LAKE_BALATON = 1
    DEAD_SEA = 2
    SEA_OF_GALILEE = 3
    LAKE_TUZ = 4
    LAKE_EGIRDIR = 5
    LAKE_BEYSEHIR = 6
    LAKE_GARDA = 7
    LAKE_GENEVA = 8
    LAKE_CONSTANCE = 9
    LAKE_SKADAR = 10
    LAKE_OHRID = 11
    LAKE_SNIARDWY = 12
    LAKE_VATTERN = 13
    LAKE_VANERN = 14
    LAKE_MALAREN = 15
    LAKE_STORSJON = 16
    LAKE_PEIPUS = 17
    LAKE_ILMEN = 18
    LAKE_LADOGA = 19
    LAKE_ONEGA = 20
    LAKE_BELOYE = 21
    LAKE_SAIMAA = 22
    LAKE_PAIJANNE = 23
    LAKE_VYGOZERO = 24
    LAKE_SEGOZERO = 25
    LAKE_KALLAVESI = 26
    LAKE_KEITELE = 27
    LAKE_PIELINEN = 28
    LAKE_NASIJARVI = 29
    LIMFJORDEN = 30
    TRONDHEIMFJORDEN = 31
