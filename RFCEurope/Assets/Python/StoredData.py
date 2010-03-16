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
                                    'lColonistsAlreadyGiven': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #active players
                                    'lNumCities': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #total players to contain Byzantium too
                                    'lLastTurnAlive': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #total players to contain Byzantium too
                                    'lSpawnDelay': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #active players
                                    'lFlipsDelay': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'iBetrayalTurns': 0,
                                    'lLatestRebellionTurn': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'iRebelCiv': 0,
                                    'lRebelCities': [], # 3Miro: store the rebelling cities
                                    'lRebelSuppress': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lExileData': [-1, -1, -1, -1, -1],
                                    'tTempFlippingCity': -1,
                                    'lCheatersCheck': [0, -1],
                                    'lBirthTurnModifier': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lDeleteMode': [-1, -1, -1], #first is a bool, the other values are capital coordinates
                                    'lFirstContactConquerors': [0, 0, 0], #maya, inca, aztecs
                                    #------------Religions
                                    'iSeed': -1,
                                    'bReformationActive': False,
                                    'lReformationHitMatrix': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    #------------UP
                                    'iImmigrationTurnLength': 0,
                                    'iImmigrationCurrentTurn': 0,
                                    'iLatestFlipTurn': 0,
                                    'lLatestRazeData': [-1, -1, -1, -1, -1],
                                    #------------AIWars
                                    'lAttackingCivsArray': [0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
                                    'iNextTurnAIWar': -1,
                                    #------------Congresses
                                    'bCongressEnabled': False,
                                    'iCivsWithNationalism': 0,
                                    'bUNbuilt': False,
                                    'lInvitedNations': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                                    'lVotes': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lTempActiveCiv': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                                    'lTempReqCity': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                                    'iLoopIndex': 0,
                                    'lTempReqCityHuman': [-1, -1, -1, -1, -1],
                                    'tempReqCityNI': -1,
                                    'tempActiveCivNI': -1,
                                    'lTempAttackingCivsNI': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                                    'iNumNationsTemp': 0,
                                    'lBribe' : [-1, -1, -1],
                                    'lCivsToBribe': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                                    'tTempFlippingCityCongress': -1,
                                    'lMemory': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #total players + barbarians (minors and barbs are not used, but necessary for not going out of range)
                                    #------------Plague
                                    'lPlagueCountdown': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #total players + barbarians
                                    'lGenericPlagueDates': [-1, -1, -1, -1, -1],
									'bBadPlague':False,
                                     #------------Victories
                                    'lGoals': [[-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1],
                                               [-1, -1, -1]],
                                    'lReligionFounded': [-1, -1, -1, -1],
                                    'iEnslavedUnits': 0,
                                    'iRazedByMongols': 0,
                                    'lEnglishEras': [-1, -1],
                                    'lGreekTechs': [-1, -1, -1],
                                    'lNewWorld': [-1, -1], #first founded; circumnavigated (still unused)
                                    'iNumSinks': 0,
                                    'lBabylonianTechs': [-1, -1, -1],    
				    'lColonies':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                                    #'iMediterraneanColonies': 0,
                                    'iPortugueseColonies': 0,
				    'iNorseRazed':0,
                                    'lWondersBuilt': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				    'bGenoaBanks':0,
				    'bGenoaCorps':0,
				    'bCorpsFounded':0,
                                    'l2OutOf3': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                                    #------------Stability
                                    'lBaseStabilityLastTurn': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lPartialBaseStability': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lStability': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lOwnedPlotsLastTurn': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lOwnedCitiesLastTurn': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lCombatResultTempModifier': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lGNPold': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lGNPnew': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lHasEscorial': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				    'lHasStephansdom': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lStatePropertyCountdown': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lDemocracyCountdown': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    'lStabilityParameters': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2+3+2+3+3
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                    'lLastRecordedStabilityStuff': [0, 0, 0, 0, 0, 0], # total + 5 parameters
                                    # 3MiroCrusades
                                    'lCrusadeInit': [-2,-2,-2,-2,-2],
                                    'bParticipate': False,
                                    'lVotingPower': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                                    'iFavorite': 0,
                                    'iPowerful': 0,
                                    'iLeader': 0,
                                    'lVotesGathered': [0,0],
                                    'iRichestCatholic': 0,
                                    'lDeviateTargets': [ False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                                    'iTarget':[0,0],
                                    'iCrusadePower':0,
				    'iCrusadeSucceeded':0,
				    'lSelectedUnits':[0, 0, 0, 0, 0, 0], # Templars, Zerglings ops! ... Teutonic Knights, Knights, Heavy Lancers, Siege Weapons, Generic
				    'bDCEnabled': False,
				    'iDCLast':0,
				    #Sedna17 Respawns
				    'lRespawnTurns': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				}
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
