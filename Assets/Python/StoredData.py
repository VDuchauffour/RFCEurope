# Rhye's and Fall of Civilization: Europe - Stored Data

from CvPythonExtensions import *
from CoreData import civilizations
from CoreTypes import Civ
import cPickle as pickle
from MiscData import NUM_CRUSADES

gc = CyGlobalContext()


class GameData:
    def __init__(self):
        self.setup()

    def load(self):
        """Loads and unpickles script data"""
        self.scriptDict.update(pickle.loads(gc.getPlayer(Civ.BARBARIAN.value).getScriptData()))

    def save(self):
        """Pickles and saves script data"""
        gc.getPlayer(Civ.BARBARIAN.value).setScriptData(pickle.dumps(self.scriptDict))

    def setup(self):
        """Initialise the global script data dictionary for usage."""

        self.scriptDict = {
            # RiseAndFall
            "iNewCiv": -1,
            "iNewCivFlip": -1,
            "iOldCivFlip": -1,
            "tTempTopLeft": -1,
            "tTempBottomRight": -1,
            "iSpawnWar": 0,  # if 1, add units and declare war. If >=2, do nothing
            "bAlreadySwitched": False,
            "lColonistsAlreadyGiven": [0] * civilizations().majors().len(),
            "lNumCities": [0] * civilizations().majors().len(),
            "lSpawnDelay": [0] * civilizations().majors().len(),
            "lFlipsDelay": [0] * civilizations().majors().len(),
            "iBetrayalTurns": 0,
            "lLatestRebellionTurn": [0] * civilizations().majors().len(),
            "iRebelCiv": 0,
            "lRebelCities": [],  # 3Miro: store the rebelling cities
            "lRebelSuppress": [0] * civilizations().majors().len(),
            "lExileData": [-1, -1, -1, -1, -1],
            "tTempFlippingCity": -1,
            "lCheatersCheck": [0, -1],
            "lDeleteMode": [
                -1,
                -1,
                -1,
            ],  # first is a bool, the other values are capital coordinates
            "iSeed": -1,  # random delay, currently unused
            # Religions
            "lReligionFounded": [-1, -1, -1, -1, -1],
            # Absinthe: Reformation
            "bReformationActive": False,
            "lReformationHitMatrix": [0] * civilizations().majors().len(),
            "bCounterReformationActive": False,
            # Absinthe: Persecution
            "lPersecutionData": [-1, -1, -1],
            "lPersecutionReligions": [],
            # Absinthe: Free religious revolution
            "lReligionChoices": [],
            # AIWars
            "lAttackingCivsArray": [
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
            ],  # major players only
            "iNextTurnAIWar": -1,
            # Absinthe: Plagues
            "lPlagueCountdown": [0] * civilizations().len(),
            "lGenericPlagueDates": [-1, -1, -1, -1, -1],
            "bBadPlague": False,
            "bFirstPlague": False,
            # Crusades
            "lCrusadeInit": [-2] * NUM_CRUSADES,
            "bParticipate": False,
            "lVotingPower": [0] * civilizations().majors().len(),
            "iFavorite": 0,
            "iPowerful": 0,
            "iLeader": 0,
            "lVotesGathered": [0, 0],
            "iRichestCatholic": 0,
            "lDeviateTargets": [False] * civilizations().majors().len(),
            "tTarget": (0, 0),
            "iCrusadePower": 0,
            "iCrusadeSucceeded": 0,
            "iCrusadeToReturn": -1,
            "lSelectedUnits": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ],  # Templar Knights, Teutonic Knights, Hospitaller Knights, Knights, Heavy Lancers, Lancers, Siege Weapons, Generic
            "lNumUnitsSent": [0] * civilizations().majors().len(),
            "bDCEnabled": False,
            "iDCLast": 0,
            # Absinthe: Respawns
            "lSpecialRespawnTurn": [0] * civilizations().majors().len(),
            "lLastTurnAlive": [0] * civilizations().majors().len(),
            "lLastRespawnTurn": [0] * civilizations().majors().len(),
            # Absinthe: Event Turn Randomization
            "lEventRandomness": [0] * 10,
            # 3Miro: Minor Nations
            "lNextMinorRevolt": [-1, -1, -1, -1, -1, -1, -1],
            "lRevoltinNationRevoltIndex": [-1, -1, -1, -1, -1, -1, -1],
            # 3Miro: Mercenaries
            "lMercGlobalPool": [],
            "lMercsHiredBy": [-1]
            * 500,  # must be at least as long as lMercList (currently allow for 500)
            # Merijn: AI UHV
            "bIgnoreAIUHV": True,
        }
        self.save()


data = GameData()
