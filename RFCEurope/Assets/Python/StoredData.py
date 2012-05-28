# Rhye's and Fall of Civilization - Stored Data

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
import cPickle as pickle        	# LOQ 2005-10-12

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	


class StoredData:

        def setupScriptData( self ):
                """Initialise the global script data dictionary for usage."""
                #print( " 3Miro: Set The Array ",gc.getGame().getScriptData() )
                scriptDict = {      #------------RiseAndFall
                                    'iNewCiv': -1,
                                    'iNewCivFlip': -1,
                                    'iOldCivFlip': -1,
                                    'tTempTopLeft': -1,
                                    'tTempBottomRight': -1,
                                    'iSpawnWar': 0, #if 1, add units and declare war. If >=2, do nothing
                                    'bAlreadySwitched': False,
                                    'lColonistsAlreadyGiven': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #active players
                                    'lNumCities': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #total players to contain Byzantium too
                                    'lLastTurnAlive': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #total players to contain Byzantium too
                                    'lSpawnDelay': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #active players
                                    'lFlipsDelay': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'iBetrayalTurns': 0,
                                    'lLatestRebellionTurn': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'iRebelCiv': 0,
                                    'lRebelCities': [], # 3Miro: store the rebelling cities
                                    'lRebelSuppress': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lExileData': [-1, -1, -1, -1, -1],
                                    'tTempFlippingCity': -1,
                                    'lCheatersCheck': [0, -1],
                                    'lBirthTurnModifier': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lDeleteMode': [-1, -1, -1], #first is a bool, the other values are capital coordinates
                                    'bCorpsFounded':0,
                                    #------------Religions
                                    'iSeed': -1,
                                    'bReformationActive': False,
                                    'lReformationHitMatrix': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'bCounterReformationActive': False,
                                    #------------AIWars
                                    'lAttackingCivsArray': [0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
                                    'iNextTurnAIWar': -1,
                                    #------------Plague
                                    'lPlagueCountdown': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #total players + barbarians
                                    'lGenericPlagueDates': [-1, -1, -1, -1, -1],
									'bBadPlague':False,
                                    'lReligionFounded': [-1, -1, -1, -1, -1],
                                    # 3MiroCrusades
                                    'lCrusadeInit': [-2,-2,-2,-2,-2],
                                    'bParticipate': False,
                                    'lVotingPower': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                                    'iFavorite': 0,
                                    'iPowerful': 0,
                                    'iLeader': 0,
                                    'lVotesGathered': [0,0],
                                    'iRichestCatholic': 0,
                                    'lDeviateTargets': [ False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                                    'iTarget':[0,0],
                                    'iCrusadePower':0,
                                    'iCrusadeSucceeded':0,
                                    'iCrusadeToReturn':-1,
                                    'lSelectedUnits':[0, 0, 0, 0, 0, 0], # Templars, Zerglings ops! ... Teutonic Knights, Knights, Heavy Lancers, Siege Weapons, Generic
                                    'bDCEnabled': False,
                                    'iDCLast':0,
                                    #Sedna17 Respawns
                                    'lRespawnTurns': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    #3Miro: Minor Nations Respawn
                                    'lNextMinorRevolt':[-1,-1,-1,-1,-1,-1,-1],
                                    'lRevoltinNationRevoltIndex':[-1,-1,-1,-1,-1,-1,-1],
                                    #3Miro: hired mercs
                                    'lMercGlobalPool':[],
                                    #3Miro: must be at least as long as lMercList (currently allow for 150)
                                    'lMercsHiredBy':[-1]*150,
                                    #Absinthe: persecution popup
                                    'lPersecutionData': [-1, -1, -1],
                                    'lPersecutionReligions': [],
                                }
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
