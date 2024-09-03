from Core import civilizations
from CoreTypes import RandomEvent
from MiscData import NUM_CRUSADES
from PyUtils import rand


class BaseData(object):
    def update(self, data):
        self.__dict__.update(data)


class CivData(BaseData):
    def __init__(self, player_id):
        self.id = player_id
        self.setup()

    def setup(self):
        self.plague_countdown = 0


class PlayerData(BaseData):
    def __init__(self, player_id):
        self.id = player_id
        self.setup()

    def setup(self):
        # RiseAndFall
        self.num_cities = 0
        self.spawn_delay = 0
        self.flips_Delay = 0
        self.latest_rebellion_turn = 0
        self.rebel_suppress = 0

        # Reformation
        self.reformation_hit = 0

        # Crusades
        self.voting_power = 0
        self.deviate_targets = False
        self.num_units_sent = 0

        # Respawns
        self.special_respawn_turn = 0
        self.last_turn_alive = 0
        self.last_respawn_turn = 0


class GameData(BaseData):
    def __init__(self):
        self.setup()

    def update(self, data):
        self.__dict__.update(data)

        for player in self.players:
            data = player.__dict__.copy()
            player.setup()
            player.update(data)

        for civ in self.civs:
            data = civ.__dict__.copy()
            civ.setup()
            civ.update(data)

    def init_temp_values(self):
        self.temp_top_left = -1
        self.temp_bottom_right = -1
        self.temp_flipping_city = -1

    def init_random_values(self):
        self.random_events = {}
        self.random_events[RandomEvent.LIGHTHOUSE_EARTHQUAKE] = rand(40)
        self.random_events[RandomEvent.BYZANTIUM_VIKING_ATTACK] = rand(10)

    def init_crusade(self):
        self.lCrusadeInit = [-2] * NUM_CRUSADES
        self.bParticipate = False
        self.iFavorite = 0
        self.iPowerful = 0
        self.iLeader = 0
        self.lVotesGathered = [0, 0]
        self.iRichestCatholic = 0
        self.tTarget = (0, 0)
        self.iCrusadePower = 0
        self.iCrusadeSucceeded = 0
        self.iCrusadeToReturn = -1
        self.lSelectedUnits = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]  # Templar Knights, Teutonic Knights, Hospitaller Knights, Knights, Heavy Lancers, Lancers, Siege Weapons, Generic
        self.bDCEnabled = False
        self.iDCLast = 0

    def init_plagues(self):
        # Sedna17: Set number of GenericPlagues in StoredData
        # 3Miro: Plague 0 strikes France too hard, make it less random and force it to pick Byzantium as starting land
        self.plagues = [
            28 + rand(5) - 10,  # Plagues of Constantinople
            247 + rand(40) - 20,  # 1341 Black Death
            300 + rand(40) - 20,  # Generic recurrence of plague
            375 + rand(40) - 30,  # 1650 Great Plague
            440 + rand(40) - 30,  # 1740 Small Pox
        ]
        self.is_a_bad_plague = False
        self.is_first_plague = False

    def init_rise_and_fall(self):
        # RiseAndFall
        self.iNewCiv = -1
        self.iNewCivFlip = -1
        self.iOldCivFlip = -1
        self.iSpawnWar = 0  # if 1, add units and declare war. If >=2, do nothing
        self.bAlreadySwitched = False
        self.iBetrayalTurns = 0
        self.iRebelCiv = 0
        self.lRebelCities = []
        self.lRebelSuppress = [0] * civilizations().majors().len()
        self.lCheatersCheck = [0, -1]
        self.lDeleteMode = [
            -1,
            -1,
            -1,
        ]  # first is a bool, the other values are capital coordinates

    def init_reformation(self):
        self.is_reformation_active = False
        self.is_counter_reformation_active = False

    def init_persecution(self):
        self.persecution_data = [-1, -1, -1]
        self.persecution_religions = []

    def init_ai_wars(self):
        self.lAttackingCivsArray = [
            0,
            0,
            -1,
            -1,
            0,
            0,
            0,
            -1,
            0,
            -1,
            -1,
            -1,
            -1,
            -1,
            0,
            0,
            0,
            -1,
            -1,
            0,
            0,
            -1,
            0,
            0,
            -1,
            -1,
            -1,
            0,
            0,
        ]  # major players only
        self.iNextTurnAIWar = -1

    def init_minor_nations(self):
        self.lNextMinorRevolt = [-1, -1, -1, -1, -1, -1, -1]
        self.lRevoltinNationRevoltIndex = [-1, -1, -1, -1, -1, -1, -1]

    def init_mercenaries(self):
        self.lMercGlobalPool = []
        self.lMercsHiredBy = [
            -1
        ] * 500  # must be at least as long as lMercList (currently allow for 500)

    def init_civics_values(self):
        self.free_religion_choices = []

    def setup(self):
        """Initialise the global script data for usage."""
        self.players = dict((civ.key, PlayerData(civ.id)) for civ in civilizations().majors())
        self.civs = dict((civ.key, CivData(civ.id)) for civ in civilizations())
        self.init_temp_values()
        self.init_random_values()
        self.init_crusade()
        self.init_plagues()
        self.init_rise_and_fall()
        self.init_reformation()
        self.init_persecution()
        self.init_ai_wars()
        self.init_minor_nations()
        self.init_mercenaries()
        self.init_civics_values()

        self.bIgnoreAIUHV = True


data = GameData()
