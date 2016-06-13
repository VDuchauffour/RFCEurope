# Rhye's and Fall of Civilization - Stored Data

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import cPickle as pickle		# LOQ 2005-10-12
import Consts as con

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class StoredData:

	def __init__(self):
		self.setup()

	def load(self):
		"""Loads and unpickles script data"""
		self.scriptDict.update(pickle.loads(gc.getPlayer(con.iBarbarian).getScriptData()))

	def save(self):
		"""Pickles and saves script data"""
		gc.getPlayer(con.iBarbarian).setScriptData(pickle.dumps(self.scriptDict))

	def setup( self ):
		"""Initialise the global script data dictionary for usage."""
		#print( " 3Miro: Set The Array ",gc.getGame().getScriptData() )

		self.scriptDict = {
				# RiseAndFall
				'iNewCiv': -1,
				'iNewCivFlip': -1,
				'iOldCivFlip': -1,
				'tTempTopLeft': -1,
				'tTempBottomRight': -1,
				'iSpawnWar': 0, #if 1, add units and declare war. If >=2, do nothing
				'bAlreadySwitched': False,
				'lColonistsAlreadyGiven': [0 for i in range(con.iNumPlayers)], #major players only, currently unused
				'lNumCities': [0 for i in range(con.iNumPlayers)], #major players only
				'lSpawnDelay': [0 for i in range(con.iNumPlayers)], #major players only
				'lFlipsDelay': [0 for i in range(con.iNumPlayers)], #major players only
				'iBetrayalTurns': 0,
				'lLatestRebellionTurn': [0 for i in range(con.iNumPlayers)], #major players only
				'iRebelCiv': 0,
				'lRebelCities': [], # 3Miro: store the rebelling cities
				'lRebelSuppress': [0 for i in range(con.iNumPlayers)], #major players only
				'lExileData': [-1, -1, -1, -1, -1],
				'tTempFlippingCity': -1,
				'lCheatersCheck': [0, -1],
				'lBirthTurnModifier': [0 for i in range(con.iNumPlayers)], #major players only, currently unused
				'lDeleteMode': [-1, -1, -1], #first is a bool, the other values are capital coordinates
				'bCorpsFounded': 0,
				'iSeed': -1, # random delay, currently unused

				# Religions
				'lReligionFounded': [-1, -1, -1, -1, -1],
				# Absinthe: Reformation
				'bReformationActive': False,
				'lReformationHitMatrix': [0 for i in range(con.iNumPlayers)], #major players only
				'bCounterReformationActive': False,
				# Absinthe: Persecution
				'lPersecutionData': [-1, -1, -1],
				'lPersecutionReligions': [],

				# AIWars
				'lAttackingCivsArray': [0, 0, -1, -1, 0, 0, 0, -1, 0, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, 0, 0, -1, 0, 0, -1, -1, -1, 0, 0], #major players only
				'iNextTurnAIWar': -1,

				# Absinthe: Plagues
				'lPlagueCountdown': [0 for i in range(con.iNumTotalPlayersB)], #total players B (major + indy + barbarian)
				'lGenericPlagueDates': [-1, -1, -1, -1, -1],
				'bBadPlague':False,
				'bFirstPlague':False,

				# Crusades
				'lCrusadeInit': [-2, -2, -2, -2, -2],
				'bParticipate': False,
				'lVotingPower': [0 for i in range(con.iNumPlayers)], #major players only
				'iFavorite': 0,
				'iPowerful': 0,
				'iLeader': 0,
				'lVotesGathered': [0, 0],
				'iRichestCatholic': 0,
				'lDeviateTargets': [False for i in range(con.iNumPlayers)], #major players only
				'tTarget': (0, 0),
				'iCrusadePower': 0,
				'iCrusadeSucceeded': 0,
				'iCrusadeToReturn': -1,
				'lSelectedUnits': [0, 0, 0, 0, 0, 0], # Templars, Zerglings, oops! ... Templar Knights, Teutonic Knights, Knights, Heavy Lancers, Siege Weapons, Generic
				'bDCEnabled': False,
				'iDCLast': 0,

				# Absinthe: Respawns
				'lSpecialRespawnTurn': [0 for i in range(con.iNumPlayers)], #major players only, currently unused
				'lLastTurnAlive': [0 for i in range(con.iNumPlayers)], #major players only
				'lLastRespawnTurn': [0 for i in range(con.iNumPlayers)], #major players only

				# 3Miro: Minor Nations
				'lNextMinorRevolt': [-1, -1, -1, -1, -1, -1, -1],
				'lRevoltinNationRevoltIndex': [-1, -1, -1, -1, -1, -1, -1],

				# 3Miro: Mercenaries
				'lMercGlobalPool': [],
				'lMercsHiredBy': [-1]*500, # must be at least as long as lMercList (currently allow for 500)

				# Merijn: AI UHV
				'bIgnoreAIUHV': True,
				}
		self.save()

# All modules import the following single instance, not the class

sd = StoredData()