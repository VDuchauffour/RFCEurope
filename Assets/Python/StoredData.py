from Core import civilizations
from CoreTypes import RandomEvent
from MiscData import NUM_CRUSADES
from PyUtils import rand


class PlayerData(object):
    def __init__(self, player_id):
        self.id = player_id
        self.setup()

    def update(self, data):
        self.__dict__.update(data)

    def setup(self):
        # RiseAndFall
        self.num_cities = 0
        self.spawn_delay = 0
        self.flips_Delay = 0
        self.latest_rebellion_turn = 0
        self.rebel_suppress = 0

        # Reformation
        self.reformation_hit = 0

        # Plague
        self.plague_countdown = 0

        # Crusades
        self.voting_power = 0
        self.deviate_targets = False
        self.num_units_sent = 0

        # Respawns
        self.special_respawn_turn = 0
        self.last_turn_alive = 0
        self.last_respawn_turn = 0


class GameData(object):
    def __init__(self):
        self.setup()

    def update(self, data):
        self.__dict__.update(data)

    def init_random_values(self):
        self.random_events = {}
        self.random_events[RandomEvent.LIGHTHOUSE_EARTHQUAKE] = rand(40)
        self.random_events[RandomEvent.BYZANTIUM_VIKING_ATTACK] = rand(10)

    def setup(self):
        """Initialise the global script data for usage."""
        self.players = dict((civ.key, PlayerData(civ.id)) for civ in civilizations().majors())

        # Temporary variables
        self.iTempTopLeft = -1
        self.iTempBottomRight = -1
        self.iTempFlippingCity = -1

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

        # Absinthe: Reformation
        self.bReformationActive = False
        self.bCounterReformationActive = False
        # Absinthe: Persecution
        self.lPersecutionData = [-1, -1, -1]
        self.lPersecutionReligions = []
        # Absinthe: Free religious revolution
        self.lReligionChoices = []

        # AIWars
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

        # Absinthe: Plagues
        self.lGenericPlagueDates = [-1, -1, -1, -1, -1]
        self.bBadPlague = False
        self.bFirstPlague = False

        # Crusades
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

        # Absinthe: Event Turn Randomization
        self.lEventRandomness = [0] * 10

        # 3Miro: Minor Nations
        self.lNextMinorRevolt = [-1, -1, -1, -1, -1, -1, -1]
        self.lRevoltinNationRevoltIndex = [-1, -1, -1, -1, -1, -1, -1]

        # 3Miro: Mercenaries
        self.lMercGlobalPool = []
        self.lMercsHiredBy = [
            -1
        ] * 500  # must be at least as long as lMercList (currently allow for 500)
        # Merijn: AI UHV
        self.bIgnoreAIUHV = True

        self.init_random_values()


data = GameData()
