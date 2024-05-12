from CoreData import civilizations
from CoreStructures import player
from CoreTypes import Civ
import cPickle as pickle
from MiscData import NUM_CRUSADES


class GameData:
    def __init__(self):
        self.setup()

    def load(self):
        """Loads and unpickles script data"""
        self.__dict__.update(pickle.loads(player(Civ.BARBARIAN).getScriptData()))

    def save(self):
        """Pickles and saves script data"""
        player(Civ.BARBARIAN).setScriptData(pickle.dumps(self.__dict__))

    def setup(self):
        """Initialise the global script data for usage."""

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
        self.lColonistsAlreadyGiven = [0] * civilizations().majors().len()
        self.lNumCities = [0] * civilizations().majors().len()
        self.lSpawnDelay = [0] * civilizations().majors().len()
        self.lFlipsDelay = [0] * civilizations().majors().len()
        self.iBetrayalTurns = 0
        self.lLatestRebellionTurn = [0] * civilizations().majors().len()
        self.iRebelCiv = 0
        self.lRebelCities = []  # 3Miro: store the rebelling cities
        self.lRebelSuppress = [0] * civilizations().majors().len()
        self.lExileData = [-1, -1, -1, -1, -1]
        self.lCheatersCheck = [0, -1]
        self.lDeleteMode = [
            -1,
            -1,
            -1,
        ]  # first is a bool, the other values are capital coordinates

        # Religions
        self.lReligionFounded = [-1, -1, -1, -1, -1]
        # Absinthe: Reformation
        self.bReformationActive = False
        self.lReformationHitMatrix = [0] * civilizations().majors().len()
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
        self.lPlagueCountdown = [0] * civilizations().len()
        self.lGenericPlagueDates = [-1, -1, -1, -1, -1]
        self.bBadPlague = False
        self.bFirstPlague = False

        # Crusades
        self.lCrusadeInit = [-2] * NUM_CRUSADES
        self.bParticipate = False
        self.lVotingPower = [0] * civilizations().majors().len()
        self.iFavorite = 0
        self.iPowerful = 0
        self.iLeader = 0
        self.lVotesGathered = [0, 0]
        self.iRichestCatholic = 0
        self.lDeviateTargets = [False] * civilizations().majors().len()
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
        self.lNumUnitsSent = [0] * civilizations().majors().len()
        self.bDCEnabled = False
        self.iDCLast = 0

        # Absinthe: Respawns
        self.lSpecialRespawnTurn = [0] * civilizations().majors().len()
        self.lLastTurnAlive = [0] * civilizations().majors().len()
        self.lLastRespawnTurn = [0] * civilizations().majors().len()

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

        self.lBaseStabilityLastTurn = [0] * civilizations().majors().len()

        self.save()


data = GameData()


def get_data(key, subkey=None):
    if subkey is None:
        return data.__dict__[key]
    else:
        return data.__dict__[key][subkey]


def set_data(key, value, subkey=None):
    if subkey is None:
        data.__dict__[key] = value
    else:
        data.__dict__[key][subkey] = value


def mod_data(key, value=1, subkey=None):
    set_data(key, get_data(key, subkey) + value, subkey)
