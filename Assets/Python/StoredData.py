# Rhye's and Fall of Civilization: Europe - Stored Data

from CvPythonExtensions import *
from CoreData import CIVILIZATIONS
from CoreTypes import Civ
import PyHelpers
import cPickle as pickle  # LOQ 2005-10-12
from MiscData import NUM_CRUSADES

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer


class StoredData:
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
            "lColonistsAlreadyGiven": [0] * CIVILIZATIONS.majors().len(),
            "lNumCities": [0] * CIVILIZATIONS.majors().len(),
            "lSpawnDelay": [0] * CIVILIZATIONS.majors().len(),
            "lFlipsDelay": [0] * CIVILIZATIONS.majors().len(),
            "iBetrayalTurns": 0,
            "lLatestRebellionTurn": [0] * CIVILIZATIONS.majors().len(),
            "iRebelCiv": 0,
            "lRebelCities": [],  # 3Miro: store the rebelling cities
            "lRebelSuppress": [0] * CIVILIZATIONS.majors().len(),
            "lExileData": [-1, -1, -1, -1, -1],
            "tTempFlippingCity": -1,
            "lCheatersCheck": [0, -1],
            "lBirthTurnModifier": [0] * CIVILIZATIONS.majors().len(),
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
            "lReformationHitMatrix": [0] * CIVILIZATIONS.majors().len(),
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
            "lPlagueCountdown": [0] * CIVILIZATIONS.len(),
            "lGenericPlagueDates": [-1, -1, -1, -1, -1],
            "bBadPlague": False,
            "bFirstPlague": False,
            # Crusades
            "lCrusadeInit": [-2] * NUM_CRUSADES,
            "bParticipate": False,
            "lVotingPower": [0] * CIVILIZATIONS.majors().len(),
            "iFavorite": 0,
            "iPowerful": 0,
            "iLeader": 0,
            "lVotesGathered": [0, 0],
            "iRichestCatholic": 0,
            "lDeviateTargets": [False] * CIVILIZATIONS.majors().len(),
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
            "lNumUnitsSent": [0] * CIVILIZATIONS.majors().len(),
            "bDCEnabled": False,
            "iDCLast": 0,
            # Absinthe: Respawns
            "lSpecialRespawnTurn": [0] * CIVILIZATIONS.majors().len(),
            "lLastTurnAlive": [0] * CIVILIZATIONS.majors().len(),
            "lLastRespawnTurn": [0] * CIVILIZATIONS.majors().len(),
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


# All modules import the following single instance, not the class

sd = StoredData()
