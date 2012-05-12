## Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import PyHelpers        # LOQ
import Popup
import cPickle as pickle        	# LOQ 2005-10-12
import RFCUtils
import Consts as con
import XMLConsts as xml

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()
localText = CyTranslator()

### Constants ###

iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iIndependent3 = con.iIndependent3
iIndependent4 = con.iIndependent4

iBarbarian = con.iBarbarian
pBarbarian = gc.getPlayer(iBarbarian)
teamBarbarian = gc.getTeam(pBarbarian.getTeam())


# 3Miro: I believe those are only used for barb spawns coordinates in the class below
# city coordinates, spawn 1st turn and retries


lTangier = [27,16,0,0] #500 AD
lBurdigala = [37,38,0,0] #500 AD, Bordeaux
#lNantes = [36,43,0,0] #500 AD
lAlger = [40,16,0,0] #500 AD
lBarcino = [40,28,0,0] #500 AD
#lCaen = [40,47,0,0] #500 AD
lToulouse = [41,34,0,0] #500 AD
#lTours = [40,43,0,0] #500 AD
#lOrleans = [42,44,0,0] #500 AD
lMarseilles = [46,32,0,0] #500 AD
lLyon = [46,37,0,0] #500 AD
lTunis = [49,17,0,0] #500 AD
#lPisae = [53,32,0,0] #500 AD
lMediolanum = [52,37,0,0] #500 AD, Milan
lFlorentia = [54,32,0,0] #500 AD, Firenze
lTripoli = [54,8,0,0] #500 AD
#lRoma = [56,27,0,0] #500 AD
lAugsburg = [55,41,0,0] #500 AD
#lCatania = [58,18,0,0] #500 AD
lNapoli = [59,24,0,0] #500 AD
lRagusa = [64,28,0,0] #500 AD
lBeograd = [68,31,0,0] #500 AD
lRhodes = [79,12,0,0] # 500 AD
lPalermo = [55,19,2,0] # 508 AD
#lZaragoza = [36,29,45,0] # 680 AD
lToledo = [30,27,45,0] #680 AD
#lLeon = [27,32,50,0] # 700 AD
#lBurgos = [30,32,50,0] # 700 AD
lValencia = [36,25,50,0] #700 AD
lPamplona = [35,32,50,0] #700 AD
lPorto = [23,31,50,0] #700 AD
lYork = [39,59,50,0] # 700 AD
lDublin = [32,58,50,0] # 700 AD
lLubeck = [57,53,50,0] #700 AD
lTonsberg = [57,65,65,0] #760 AD
#lCorunna = [24,35,75,0] #800 AD
lMilan = [52,37,75,0] #800 AD, Respawn of Mediolanum, so that it still exists if razed
lFirenze = [54,32,75,0] #800 AD, Respawn of Florentia 
#lLeipzig = [58,48,75,0] #800 AD
lPrague = [60,44,75,0] #800 AD
#lKharkov = [90,46,75,0] #800 AD
lKursk = [90,48,75,0] #800 AD
lCalais = [44,50,75,0] #800 AD
lNidaros = [57,71,75,0] #800 AD, Trondheim
lNovgorod = [80,62,87,0] #848 AD
lEdinburgh = [37,63,90,0] #860 AD
lAlbaIulia = [73,34,95,0] #880 AD
lTvanksta = [69,53,100,0] #900 AD, Konigsberg
#lBreslau = [64,46,100,0] #900 AD
lKrakow = [68,44,100,0] #900 AD
lRiga = [74,58,100,0] #900 AD
lMinsk = [79,52,120,0] #960 AD
lSmolensk = [84,55,120,0] #960 AD
lYaroslavl = [92,61,137,0] #1010 AD
lGroningen = [52,54,150,0] #1050 AD
#lMunster = [52,50,150,0] #1050 AD
lMus = [99,21,153,0] #1060 AD
lMarrakesh = [24,7,157,0] #1071 AD
lSaraiBatu = [99,40,200,0] #1200 AD
lTarabulus = [54,8,209,0] #1227 AD, Respawn of Tripoli
lAbo = [71,66,217,0] #1250 AD
lNizhnyNovgorod = [97,58,240,0] #1320 AD
#lMemel = [70,55,240,0] #1320 AD, Klaipeda
lVologda = [91,64,240,0] #1320 AD
#lTver = [88,60,240,0] #1320 AD
lReykjavik = [2,70,270,0] #1410 AD
lValletta = [57,14,315,0] #1530 AD



# Minor Nations sructure: [ int Province: all cities in this province will revolt
#                           list nations: a city controlled by those players will not revolt (i.e. Greece wouldn't revolt against the Byz)
#                           list religions: a city owned by someone with one of those state religions will not revolt (i.e. Jerusalem doesn't revolt against Muslims)
#                           list revolt dates: the dates for the revolt,
#                           list revolt strength: this is substracted from the odds to suppress the revolt (i.e. high number more likely to succeed in the revolt)
#                           list units: corresponding to the revolt, if we crack down on the rebels, what barbarian units should spawn
#                           list number: corresponding to the revolt, if we crack down on the rebels, how many units should spawn (note if we don't bribe the Lords, then double the number of Units will spawn)
#                           list text keys: text keys for "The Nation" and "Nation Adjective"
# Note: lists 3, 4, 5, 6 should have the same size
# Note: you should increase the size of 'lNextMinorRevolt' in StoredData to be at least the number of minor nations
lMinorNations = [ [ xml.iP_Serbia, [], [], [xml.i852AD,xml.i1346AD], [20,20], [xml.iAxeman,xml.iLongSwordsman], [1,2], ["TXT_KEY_THE_SERBS","TXT_KEY_SERBIAN"] ],
                  [ xml.iP_Scotland, [], [], [xml.i1297AD,xml.i1569AD,xml.i1715AD], [20,10,20], [xml.iHighlander,xml.iMusketman,xml.iGrenadier], [2,2,2], ["TXT_KEY_THE_SCOTS","TXT_KEY_SCOTISH"] ],
                  [ xml.iP_Catalonia, [], [], [xml.i1164AD,xml.i1640AD], [20,10], [xml.iLongSwordsman,xml.iMusketman], [2,2], ["TXT_KEY_THE_CATALANS","TXT_KEY_CATALAN"] ],
                  [ xml.iP_Jerusalem, [con.iArabia,con.iTurkey,con.iByzantium], [xml.iIslam,], [xml.i1099AD+8,xml.i1099AD+16,xml.i1099AD+25,xml.i1099AD+33,xml.i1099AD+40,xml.i1099AD+47,xml.i1099AD+55,xml.i1099AD+65], [30,30,40,40,30,30,30,30], [xml.iMaceman,xml.iMaceman,xml.iMaceman,xml.iKnight,xml.iKnight,xml.iKnight,xml.iKnight,xml.iKnight], [3,3,4,3,3,3,3,3], ["TXT_KEY_THE_MUSLIMS","TXT_KEY_MUSLIM"] ],
                  [ xml.iP_Syria, [con.iArabia,con.iTurkey,con.iByzantium], [xml.iIslam,], [xml.i1099AD+8,xml.i1099AD+16,xml.i1099AD+25,xml.i1099AD+33,xml.i1099AD+40,xml.i1099AD+47,xml.i1099AD+55,xml.i1099AD+65], [30,30,40,40,30,30,30,30], [xml.iMaceman,xml.iMaceman,xml.iMaceman,xml.iKnight,xml.iKnight,xml.iKnight,xml.iKnight,xml.iKnight], [3,3,4,3,3,3,3,3], ["TXT_KEY_THE_MUSLIMS","TXT_KEY_MUSLIM"] ],
                  [ xml.iP_Oran, [], [], [xml.i1236AD,xml.i1346AD,xml.i1359AD,xml.i1542AD], [40,10,10,20], [xml.iKnight,xml.iHeavyLancer,xml.iHeavyLancer,xml.iMusketman], [2,2,2,2], ["TXT_KEY_THE_ZIYYANIDS","TXT_KEY_ZIYYANID"] ],
                  [ xml.iP_Tetouan, [con.iCordoba, con.iSpain, con.iPortugal], [], [xml.i1473AD], [30], [xml.iArquebusier], [4], ["TXT_KEY_THE_WATTASIDS","TXT_KEY_WATTASID"] ],
                ]
# 3Miro: Jerusalem is added so that the Crusaders will not be able to control it for too long



class Barbs:
        
        def getRevolDates( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lNextMinorRevolt']
                
        def setRevolDates( self, lNextMinorRevolt ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lNextMinorRevolt'] = lNextMinorRevolt
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getTempFlippingCity( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['tempFlippingCity']

        def setTempFlippingCity( self, tNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['tempFlippingCity'] = tNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getNationRevoltIndex( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lRevoltinNationRevoltIndex']
                
        def setNationRevoltIndex( self, iNationIndex, iRevoltIndex ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lRevoltinNationRevoltIndex'] = [iNationIndex,iRevoltIndex]
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def makeUnit(self, iUnit, iPlayer, tCoords, iNum, iForceAttack, szName ):
                'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
                for i in range(iNum):
                        player = gc.getPlayer(iPlayer)
                        if (iForceAttack == 0):
                                pUnit = player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
                        elif (iForceAttack == 1):
                                pUnit = player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)                                  
                        elif (iForceAttack == 2):
                                pUnit = player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK_SEA, DirectionTypes.DIRECTION_SOUTH)
                        if ( szName != "" ):
                                pUnit.setName( szName )


        def checkTurn(self, iGameTurn):
            
                #handicap level modifier
                #getHandicapType: Viceroy=0, Monarch=1, Emperor=2)
                iHandicap = (gc.getGame().getHandicapType() - 1)

                #debug
                #if (iGameTurn % 50 == 1):
                #        print ("iHandicap", iHandicap)

                
		#Mediterranean Pirates (Light before 1500, then heavy for rest of game)
		if ( iGameTurn >= xml.i960AD and iGameTurn < xml.i1401AD):
			self.spawnPirate( iBarbarian, (9,15), (55,33), xml.iWarGalley, 2, 0, 0, iGameTurn, 10, 3, utils.outerSeaSpawn, 1, "")
		if ( iGameTurn >= xml.i1401AD ):
			self.spawnPirate( iBarbarian, (9,15), (55,33), xml.iCorsair, 2, 0, 0, iGameTurn, 10,3, utils.outerSeaSpawn, 1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BARBARY_PIRATES", ()))
			#extra corsairs around Tunisia
			self.spawnPirate( iBarbarian, (42,15), (54,23), xml.iCorsair, 1, 0, 0, iGameTurn, 5,0, utils.outerSeaSpawn, 1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BARBARY_PIRATES", ()))
		if ( iGameTurn >= xml.i1200AD and iGameTurn < xml.i1500AD):
			self.spawnPirate( iBarbarian, (9,15), (55,33), xml.iCogge, 1, xml.iSwordsman, 2, iGameTurn, 10, 5, utils.outerSeaSpawn, 1, "")
		if ( iGameTurn >= xml.i1500AD ):
			self.spawnPirate( iBarbarian, (9,15), (55,33), xml.iGalleon, 1, xml.iMusketman, 2, iGameTurn, 10, 5, utils.outerSeaSpawn, 1, "")
		
		#Germanic Barbarians throughout Western Europe (France, Germany)
		if (iGameTurn < xml.i800AD):
			self.spawnUnits( iBarbarian, (45,45),(60,55), xml.iAxeman, 1 + iHandicap, iGameTurn,10,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
			self.spawnUnits( iBarbarian, (52,42),(66,50), xml.iAxeman, 1 + iHandicap, iGameTurn,8,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
			self.spawnUnits( iBarbarian, (46,48),(62,55), xml.iSpearman, 1 + iHandicap, iGameTurn,12,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
		if (iGameTurn < xml.i770AD):
			self.spawnUnits( iBarbarian, (42,40),(56,48), xml.iAxeman, 1 + iHandicap, iGameTurn,15,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
		
		#Longobards in Italy
		if (iGameTurn >= xml.i632AD and iGameTurn <= xml.i800AD):
			self.spawnUnits( iBarbarian, (49,33),(53,36), xml.iAxeman, 1 + iHandicap, iGameTurn,10,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_LONGOBARDS", ()))
		
		#Christians in Spain, this might be a bit overtuned, but lets wait for feedback
		if (iGameTurn >= xml.i700AD and iGameTurn <= xml.i880AD):
			self.spawnUnits( iBarbarian, (24,32),(28,40), xml.iAxeman, 1 + iHandicap, iGameTurn,14,0,utils.outerInvasion,1, "")
			self.spawnUnits( iBarbarian, (24,32),(28,40), xml.iScout, 1 + iHandicap, iGameTurn,15,5,utils.outerInvasion,1, "")
			self.spawnUnits( iBarbarian, (20,28),(24,34), xml.iAxeman, 1 + iHandicap, iGameTurn,14,5,utils.outerInvasion,1, "")
			self.spawnUnits( iBarbarian, (20,28),(24,34), xml.iSpearman, 1 + iHandicap, iGameTurn,16,14,utils.outerInvasion,1, "")
		if (gc.getPlayer(con.iCordoba).isHuman()): #extra barbs for human Cordoba
			if (iGameTurn >= xml.i700AD and iGameTurn <= xml.i880AD):
				self.spawnUnits( iBarbarian, (24,32),(28,40), xml.iAxeman, 1 + iHandicap, iGameTurn,14,0,utils.outerInvasion,1, "")
				self.spawnUnits( iBarbarian, (24,32),(28,40), xml.iMountedInfantry, 1 + iHandicap, iGameTurn,18,3,utils.outerInvasion,1, "")
				self.spawnUnits( iBarbarian, (20,28),(24,34), xml.iSpearman, 1 + iHandicap, iGameTurn,18,9,utils.outerInvasion,1, "")
		
		#Berbers in North Africa
		if (iGameTurn >= xml.i700AD and iGameTurn < xml.i1060AD):
			self.spawnUnits(iBarbarian, (19,18),(27,21), xml.iHorseArcher, 2 + iHandicap, iGameTurn,10,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()))
		
		#Avars in Austria-Hungary from 550 AD to 800 AD	
		if (iGameTurn >= xml.i632AD and iGameTurn < xml.i800AD):
			self.spawnUnits( iBarbarian, (60,30),(75,40), xml.iHorseArcher, 1 + iHandicap, iGameTurn,5,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_AVARS", ()))
		if (gc.getPlayer(con.iBulgaria).isHuman()): #extra barbs for human Bulgaria
			if (iGameTurn >= xml.i632AD and iGameTurn < xml.i800AD):
				self.spawnUnits( iBarbarian, (66,26),(73,29), xml.iHorseArcher, 2 + iHandicap, iGameTurn,6,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_AVARS", ()))
		
		#Early barbs in Byzantium:
		#Pre-Bulgarian Slavs in South Balkans
		if (iGameTurn < xml.i640AD):
			self.spawnUnits( iBarbarian, (68,18),(78,28), xml.iAxeman, 1 + iHandicap, iGameTurn,5,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS", ()))
		#Sassanids in Anatolia
		if (iGameTurn < xml.i640AD):
			self.spawnUnits( iBarbarian, (90,15),(99,28), xml.iLancer, 1 + iHandicap, iGameTurn,7,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()))
		if (iGameTurn < xml.i640AD):
			self.spawnUnits( iBarbarian, (94,19),(98,26), xml.iLancer, 1 + iHandicap, iGameTurn,9,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()))
		#Barbs in Eastern Greece 
		if (iGameTurn < xml.i720AD):
			self.spawnUnits( iBarbarian, (66,21),(69,28), xml.iAxeman, 1 + iHandicap, iGameTurn,12,3,utils.outerInvasion,1, "")
		
		#Misc Asiatic tribes to keep Ukraine empty
		if (iGameTurn >= xml.i632AD and iGameTurn < xml.i800AD):
			self.spawnUnits( iBarbarian, (84,36),(89,43), xml.iScout, 1 + iHandicap, iGameTurn,7,1,utils.outerInvasion,1, "")
		
		#Khazars 800 to 1100
		if (iGameTurn >= xml.i800AD and iGameTurn < xml.i940AD):
			self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iHorseArcher, 1 + iHandicap, iGameTurn,7,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()))
		if (iGameTurn >= xml.i940AD and iGameTurn < xml.i1000AD):
			self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iHorseArcher, 1 + iHandicap, iGameTurn,5,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()))
		if (gc.getPlayer(con.iKiev).isHuman()): #extra barbs for human Kiev
			if (iGameTurn >= xml.i800AD and iGameTurn < xml.i940AD):
				self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iHorseArcher, 1 + iHandicap, iGameTurn,7,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()))
			if (iGameTurn >= xml.i940AD and iGameTurn < xml.i1000AD):
				self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iHorseArcher, 2 + iHandicap*2, iGameTurn,8,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()))
		
		#Pechenegs and Cumans in Northern Balkans
		if (iGameTurn >= xml.i940AD and iGameTurn < xml.i1160AD):
			self.spawnUnits( iBarbarian, (64,33),(77,43), xml.iHorseArcher, 1 + iHandicap, iGameTurn,5,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()))
			self.spawnUnits( iBarbarian, (66,35),(75,42), xml.iHorseArcher, 1 + iHandicap, iGameTurn,6,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()))
		if (gc.getPlayer(con.iHungary).isHuman()): #extra barbs for human Hungary
			if (iGameTurn >= xml.i940AD and iGameTurn < xml.i1160AD):
				self.spawnUnits( iBarbarian, (64,33),(77,43), xml.iHorseArcher, 1 + iHandicap, iGameTurn,5,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()))
				self.spawnUnits( iBarbarian, (66,35),(75,42), xml.iHorseArcher, 1 + iHandicap, iGameTurn,6,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()))		
		if (gc.getPlayer(con.iBulgaria).isHuman()): #extra barbs for human Bulgaria
			if (iGameTurn >= xml.i940AD and iGameTurn < xml.i1160AD):
				self.spawnUnits( iBarbarian, (78,32),(80,34), xml.iHorseArcher, 2 + iHandicap, iGameTurn,5,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()))
				self.spawnUnits( iBarbarian, (77,31),(79,33), xml.iHorseArcher, 1 + iHandicap, iGameTurn,6,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()))
		
		#Vikings on ships
		if (gc.getPlayer(con.iNorse).isHuman()): #Humans can properly go viking without help
			pass
		elif (iGameTurn >= xml.i800AD and iGameTurn < xml.i1000AD):
			self.spawnVikings( iBarbarian, (35,48),(50,55), xml.iVikingBeserker, 2, iGameTurn,8,0,utils.outerSeaSpawn,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_VIKINGS", ()))
		
		#Swedish Crusades (from Morholt)
		if (iGameTurn >= xml.i1150AD and iGameTurn < xml.i1210AD):
			self.spawnVikings( iBarbarian, (71,62),(76,65), xml.iVikingBeserker, 2, iGameTurn,8,0,utils.outerSeaSpawn,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SWEDES", ()))
		
		#Chudes in Finland and Estonia (from Morholt)
		if (iGameTurn >= xml.i864AD and iGameTurn < xml.i1150AD):
			self.spawnUnits( iBarbarian, (72,67),(81,72), xml.iAxeman, 1 + iHandicap*2, iGameTurn,8,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CHUDES", ()))
			self.spawnUnits( iBarbarian, (73,60),(75,63), xml.iAxeman, 1 + iHandicap*2, iGameTurn,10,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CHUDES", ()))
		
		#Scots and Welsh to keep England busy
		if (iGameTurn>=xml.i1000AD and iGameTurn < xml.i1060AD):
			self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iAxeman, 2 + iHandicap, iGameTurn,8,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
			self.spawnUnits( iBarbarian, (39,64),(44,67), xml.iSpearman, 1 + iHandicap, iGameTurn,8,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
		#hard for the human player:
		if (gc.getPlayer(con.iEngland).isHuman()):
			if (iGameTurn >= xml.i1060AD and iGameTurn < xml.i1320AD):
				self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iHighlander, 2 + iHandicap, iGameTurn,13,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
			if (iGameTurn >= xml.i1320AD and iGameTurn < xml.i1500AD):
				self.spawnUnits( iBarbarian, (39,64),(44,67), xml.iHighlander, 3 + iHandicap, iGameTurn,23,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
			if (iGameTurn>=xml.i1060AD and iGameTurn < xml.i1160AD):
				self.spawnUnits( iBarbarian, (37,55),(39,57), xml.iWelshLongbowman, 2 + iHandicap, iGameTurn,13,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()))
		#easy for the AI:
		else:
			if (iGameTurn >= xml.i1060AD and iGameTurn < xml.i1320AD):
				self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iHighlander, 1 + iHandicap, iGameTurn,16,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
			if (iGameTurn >= xml.i1320AD and iGameTurn < xml.i1500AD):
				self.spawnUnits( iBarbarian, (39,64),(44,67), xml.iHighlander, 2 + iHandicap, iGameTurn,24,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
			if (iGameTurn>=xml.i1060AD and iGameTurn < xml.i1160AD):
				self.spawnUnits( iBarbarian, (37,55),(39,57), xml.iWelshLongbowman, 1 + iHandicap, iGameTurn,17,3,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()))
		
		#Magyars (preceeding Hungary)
		if (iGameTurn >= xml.i840AD and iGameTurn < xml.i892AD):
			self.spawnUnits( iBarbarian, (54,40),(62,49), xml.iHorseArcher, 1 + iHandicap, iGameTurn,3,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()))
		if (iGameTurn >= xml.i840AD and iGameTurn < xml.i892AD):
			self.spawnUnits( iBarbarian, (66,26),(73,29), xml.iHorseArcher, 1 + iHandicap, iGameTurn,5,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()))
		if (gc.getPlayer(con.iBulgaria).isHuman()): #extra barbs for human Bulgaria
			if (iGameTurn >= xml.i840AD and iGameTurn < xml.i892AD):
				self.spawnUnits( iBarbarian, (77,31),(80,34), xml.iHorseArcher, 2 + iHandicap, iGameTurn,3,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()))
		if (gc.getPlayer(con.iGermany).isHuman()): #extra barbs for human Germany
			if (iGameTurn >= xml.i840AD and iGameTurn < xml.i892AD):
				self.spawnUnits( iBarbarian, (54,40),(62,49), xml.iHorseArcher, 2 + iHandicap, iGameTurn,4,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()))
		
		#Barbs in the middle east
		if (gc.getPlayer(con.iArabia).isAlive()):
			if (iGameTurn>=xml.i700AD and iGameTurn <= xml.i1300AD ):
				if (not gc.getTeam(gc.getPlayer(con.iArabia).getTeam()).isHasTech(xml.iFarriers)):
					self.spawnUnits( iBarbarian, (94,0),(99,3), xml.iHorseArcher, 2 + iHandicap, iGameTurn,8,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()))
				else:
					self.spawnUnits( iBarbarian, (94,0),(99,3), xml.iArabiaGhazi, 2 + iHandicap, iGameTurn,10,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()))
		
		#Pre Mongols to keep Kiev busy
		if (iGameTurn >= xml.i900AD and iGameTurn < xml.i1236AD):
			self.spawnUnits( iBarbarian, (93,32),(99,44), xml.iHorseArcher, 2 + iHandicap, iGameTurn,10,1,utils.outerInvasion,1, "")
		
		#Barbs in Anatolia pre Seljuks (but after Sassanids)
		if (iGameTurn >= xml.i700AD and iGameTurn < xml.i1050AD ):
			self.spawnUnits( iBarbarian, (97,20),(99,26), xml.iHorseArcher, 1 + iHandicap, iGameTurn,12,2,utils.outerInvasion,1, "")
			self.spawnUnits( iBarbarian, (95,20),(99,24), xml.iAxeman, 1 + iHandicap, iGameTurn,14,2,utils.outerInvasion,1, "")
			self.spawnUnits( iBarbarian, (95,22),(97,26), xml.iSpearman, 1 + iHandicap, iGameTurn,16,6,utils.outerInvasion,1, "")
		
		#Seljuks 1067
		if (iGameTurn >= xml.i1067AD and iGameTurn < xml.i1089AD):
			self.spawnUnits( iBarbarian, (90,18),(99,28), xml.iSeljuk, 2 + iHandicap, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (90,18),(99,28), xml.iCrossbowman, 1 + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iSeljuk, 2 + iHandicap, iGameTurn,3,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iGuisarme, 1 + iHandicap, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (95,0),(99,15), xml.iSeljuk, 2 + iHandicap, iGameTurn,3,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (95,0),(99,15), xml.iCrossbowman, 1 + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
		if (gc.getPlayer(con.iByzantium).isHuman()): #extra barbs for human Byzantium
			if (iGameTurn >= xml.i1067AD and iGameTurn < xml.i1089AD):
				self.spawnUnits( iBarbarian, (90,18),(99,28), xml.iSeljuk, 4 + iHandicap*2, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (90,18),(99,28), xml.iCrossbowman, 1 + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iSeljuk, 3 + iHandicap*2, iGameTurn,3,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iGuisarme, 1 + iHandicap, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
		if (gc.getPlayer(con.iArabia).isHuman()): #extra barbs for human Arabia
			if (iGameTurn >= xml.i1067AD and iGameTurn < xml.i1089AD):
				self.spawnUnits( iBarbarian, (95,0),(99,15), xml.iSeljuk, 3 + iHandicap*2, iGameTurn,3,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (95,0),(99,15), xml.iCrossbowman, 1 + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
		
		#Mongols 1236
		if (iGameTurn >= xml.i1236AD and iGameTurn < xml.i1288AD):
			if ( iHandicap == -1 ): #Sedna17: Making mongols too weak in viceroy makes AI Kiev a super-power.
				iExtra = 1
			else:
				iExtra = 0
			#Kiev
			if (gc.getPlayer(con.iKiev).isHuman()):
				self.spawnUnits( iBarbarian, (93,32),(99,44), xml.iMongolKeshik, 5 + iExtra*2 + iHandicap*2, iGameTurn,4,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
				self.spawnUnits( iBarbarian, (94,34),(99,48), xml.iMongolKeshik, 4 + iExtra*2 + iHandicap*2, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			else:
				self.spawnUnits( iBarbarian, (93,32),(99,44), xml.iMongolKeshik, 3 + iExtra + iHandicap, iGameTurn,4,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
				self.spawnUnits( iBarbarian, (94,34),(99,48), xml.iMongolKeshik, 2 + iExtra + iHandicap, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			#Hungary
			if (gc.getPlayer(con.iHungary).isHuman()):
				self.spawnUnits( iBarbarian, (70,35),(76,45), xml.iMongolKeshik, 4 + iExtra*2 + iHandicap*2, iGameTurn,4,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			else:
				self.spawnUnits( iBarbarian, (70,35),(76,45), xml.iMongolKeshik, 2 + iExtra + iHandicap, iGameTurn,4,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			#Poland
			if (gc.getPlayer(con.iPoland).isHuman()):
				self.spawnUnits( iBarbarian, (72,40),(75,58), xml.iMongolKeshik, 4 + iExtra*2 + iHandicap*2, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			else:
				self.spawnUnits( iBarbarian, (72,40),(75,58), xml.iMongolKeshik, 2 + iExtra + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))				
			#Bulgaria
			if (gc.getPlayer(con.iBulgaria).isHuman()):
				self.spawnUnits( iBarbarian, (78,32),(83,34), xml.iMongolKeshik, 3 + iExtra*2 + iHandicap*2, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			else:
				self.spawnUnits( iBarbarian, (78,32),(83,34), xml.iMongolKeshik, 2 + iExtra + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			#Moscow area
			self.spawnUnits( iBarbarian, (89,46),(99,56), xml.iMongolKeshik, 2 + iExtra*2 + iHandicap*2, iGameTurn,4,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			self.spawnUnits( iBarbarian, (91,48),(97,54), xml.iMongolKeshik, 2 + iExtra + iHandicap, iGameTurn,6,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))			
			#Middle East
			self.spawnUnits( iBarbarian, (94,20),(99,26), xml.iMongolKeshik, 2 + iExtra*2 + iHandicap*2, iGameTurn,3,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			self.spawnUnits( iBarbarian, (92,21),(97,25), xml.iMongolKeshik, 2 + iExtra + iHandicap, iGameTurn,6,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			
		#Mongols, the return! (aka Tamerlane)
		if (iGameTurn >=xml.i1359AD and iGameTurn <=xml.i1431AD):
			#Eastern Europe
			self.spawnUnits( iBarbarian, (85,47),(99,57), xml.iMongolKeshik, 2 + iHandicap, iGameTurn,7,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			#Anatolia
			self.spawnUnits( iBarbarian, (87,17),(99,26), xml.iMongolKeshik, 3 + iHandicap*2, iGameTurn,4,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			self.spawnUnits( iBarbarian, (94,15),(99,26), xml.iMongolKeshik, 4 + iHandicap*2, iGameTurn,5,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			
		#Nogais (from Morholt)
		if (iGameTurn >=xml.i1500AD and iGameTurn <=xml.i1600AD):
			self.spawnUnits( iBarbarian, (93,38),(99,54), xml.iHorseArcher, 3 + iHandicap*2, iGameTurn,7,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_NOGAIS", ()))
		if (gc.getPlayer(con.iMoscow).isHuman()): #extra barbs for human Moscow
			if (iGameTurn >=xml.i1500AD and iGameTurn <=xml.i1600AD):
				self.spawnUnits( iBarbarian, (93,38),(99,54), xml.iHorseArcher, 2 + iHandicap*2, iGameTurn,7,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_NOGAIS", ()))
		
		#Kalmyks (from Morholt)
		if (iGameTurn >=xml.i1600AD and iGameTurn <=xml.i1715AD):
			self.spawnUnits( iBarbarian, (93,38),(99,54), xml.iMongolKeshik, 3 + iHandicap*2, iGameTurn,7,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KALMYKS", ()))
		if (gc.getPlayer(con.iMoscow).isHuman()): #extra barbs for human Moscow
			if (iGameTurn >=xml.i1600AD and iGameTurn <=xml.i1715AD):
				self.spawnUnits( iBarbarian, (93,38),(99,54), xml.iMongolKeshik, 3 + iHandicap*2, iGameTurn,7,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KALMYKS", ()))
		
		
		#Setting cities to size 2 initially has no effect. They start with zero-sized culture, so immediately shrink one pop. Hack is to start with three.
		# 3Miro Barbarian and Independent city spawn and barbarian invasions go here. Check with original RFC file for details
		# self.foundCity(owner, self.lCity, name, iGameTurn, pop size, unit, num units, religion )
		
                if ( iGameTurn < xml.i700AD ):
                        #500AD
                        self.foundCity(iIndependent2, lTangier, "Tangier", iGameTurn, 1, xml.iCordobanBerber, 2, -1, 0 ) 
                        self.foundCity(iBarbarian, lBurdigala, "Burdigala", iGameTurn, 2, xml.iArcher, 1, -1, 0 )
                        self.foundCity(iIndependent3, lAlger, "Alger", iGameTurn, 1, xml.iArcher, 1, -1, 1 )
                        self.foundCity(iIndependent2, lBarcino, "Barcino", iGameTurn, 1, xml.iArcher, 1, -1, 0 )
                        self.foundCity(iBarbarian, lToulouse, "Tolosa", iGameTurn, 1, xml.iArcher, 1, -1, 0 )
                        self.foundCity(iIndependent, lMarseilles, "Massilia", iGameTurn, 1, xml.iArcher, 1, xml.iCatholicism, 0 )
                        self.foundCity(iIndependent3, lLyon, "Lyon", iGameTurn, 1, xml.iArcher, 2, xml.iCatholicism, 1 ) # 3Miro - Lyon flips to Burgundy
                        self.foundCity(iIndependent2, lTunis, "Tunis", iGameTurn, 1, xml.iArcher, 1, -1, 0 )
                        self.foundCity(iIndependent, lMediolanum, "Mediolanum", iGameTurn, 3, xml.iArcher, 1, xml.iCatholicism, 0 )
                        self.foundCity(iIndependent2, lFlorentia, "Florentia", iGameTurn, 3, xml.iArcher, 1, xml.iCatholicism, 0 )
                        self.foundCity(iBarbarian, lTripoli, "Tripoli", iGameTurn, 1, xml.iArcher, 1, -1, 0 ) 
                        self.foundCity(iIndependent3, lAugsburg, "Augsburg", iGameTurn, 1, xml.iArcher, 2, -1, 0 )
                        self.foundCity(iIndependent, lNapoli, "Neapolis", iGameTurn, 3, xml.iArcher, 1, -1, 0 )
                        self.foundCity(iIndependent2, lRagusa, "Ragusa", iGameTurn, 1, xml.iArcher, 1, xml.iCatholicism, 0 )
                        self.foundCity(iBarbarian, lBeograd, "Beograd", iGameTurn, 1, xml.iArcher, 2, -1, 0 )
                        self.foundCity(iIndependent2, lRhodes, "Rhodes", iGameTurn, 1, xml.iArcher, 1, xml.iOrthodoxy, 0 )
                        # 508AD
                        self.foundCity(iIndependent3, lPalermo, "Palermo", iGameTurn, 1, xml.iArcher, 1, xml.iCatholicism, 1 ) 
                        # 680AD
                        self.foundCity(iBarbarian, lToledo, "Toledo", iGameTurn, 1, xml.iArcher, 2, xml.iCatholicism, 1 )
                if ( iGameTurn > xml.i680AD and iGameTurn < xml.i900AD ):        
                        # 700AD
                        self.foundCity(iIndependent, lValencia, "Valencia", iGameTurn, 1, xml.iArcher, 1, xml.iCatholicism, 1 )
                        self.foundCity(iIndependent4, lPamplona, "Pamplona", iGameTurn, 1, xml.iCrossbowman, 2, -1, 0 )
                        self.foundCity(iIndependent4, lYork, "Eboracum", iGameTurn, 1, xml.iArcher, 2, -1, 1 )
                        self.foundCity(iBarbarian, lDublin, "Dubh Linn", iGameTurn, 1, xml.iArcher, 2, xml.iCatholicism, 1 )
                        self.foundCity(iIndependent2, lLubeck, "Liubice", iGameTurn, 1, xml.iArcher, 2, -1, 1 )
                        self.foundCity(iIndependent3, lPorto, "Portucale", iGameTurn, 1, xml.iCrossbowman, 3, xml.iCatholicism, 0 )
                        # 760AD
                        self.foundCity(iIndependent3, lTonsberg, "Tonsberg", iGameTurn, 1, xml.iArcher, 2, -1, 0 )
                        # 800AD
                        self.foundCity(iIndependent, lMilan, "Milano", iGameTurn, 5, xml.iArcher, 2, xml.iCatholicism, 0 )
                        self.foundCity(iIndependent2, lFirenze, "Firenze", iGameTurn, 5, xml.iArcher, 2, xml.iCatholicism, 0 )
                        self.foundCity(iIndependent, lPrague, "Praha", iGameTurn, 1, xml.iCrossbowman, 2, xml.iCatholicism, 1 )
                        self.foundCity(iIndependent4, lKursk, "Kursk", iGameTurn, 1, xml.iArcher, 2, -1, 0 )
                        self.foundCity(iIndependent3, lCalais, "Calais", iGameTurn, 1, xml.iCrossbowman, 2, -1, 0 )
                        self.foundCity(iIndependent2, lNidaros, "Nidaros", iGameTurn, 1, xml.iArcher, 2, -1, 0 )
                        # 848AD
                        self.foundCity(iIndependent2, lNovgorod, "Novgorod", iGameTurn, 1, xml.iCrossbowman, 2, -1, 1 )
                        # 860AD
                        self.foundCity(iBarbarian, lEdinburgh, "Eidyn Dun", iGameTurn, 1, xml.iArcher, 2, -1, 0 )
                        # 880AD
                        self.foundCity(iIndependent, lAlbaIulia, "Belograd", iGameTurn, 1, xml.iArcher, 2, -1, 0 )
                if ( iGameTurn > xml.i880AD and iGameTurn < xml.i1259AD ):
                        # 900AD
                        self.foundCity(iIndependent4, lTvanksta, "Tvanksta", iGameTurn, 1, xml.iCrossbowman, 2, -1, 0 )
                        self.foundCity(iIndependent3, lKrakow, "Krakow", iGameTurn, 1, xml.iCrossbowman, 2, xml.iCatholicism, 0 )
                        self.foundCity(iIndependent, lRiga, "Riga", iGameTurn, 2, xml.iCrossbowman, 2, -1, 1 )
                        # 960AD
                        self.foundCity(iIndependent3, lMinsk, "Minsk", iGameTurn, 1, xml.iCrossbowman, 2, -1, 0 )
                        self.foundCity(iIndependent4, lSmolensk, "Smolensk", iGameTurn, 1, xml.iCrossbowman, 1, -1, 0 )
                        # 1010AD
                        self.foundCity(iIndependent3, lYaroslavl, "Yaroslavl", iGameTurn, 1, xml.iCrossbowman, 1, -1, 0 )
                        # 1050AD
                        self.foundCity(iIndependent2, lGroningen, "Groningen", iGameTurn, 1, xml.iCrossbowman, 2, xml.iCatholicism, 0 )
                        # 1060AD
                        self.foundCity(iBarbarian, lMus, "Mus", iGameTurn, 1, xml.iLongbowman, 2, -1, 0 )
                        # 1071AD
                        self.foundCity(iBarbarian, lMarrakesh, "Marrakesh", iGameTurn, 3, xml.iCrossbowman, 2, xml.iIslam, 1 )
                        # 1200AD
                        self.foundCity(iBarbarian, lSaraiBatu, "Sarai Batu", iGameTurn, 1, xml.iLongbowman, 2, -1, 0 )
                        # 1227 AD
                        self.foundCity(iBarbarian, lTarabulus, "Tarabulus", iGameTurn, 4, xml.iArbalest, 2, xml.iIslam, 1 )
                        # 1250 AD
                        self.foundCity(iIndependent2, lAbo, "Abo", iGameTurn, 1, xml.iCrossbowman, 1, -1, 0 ) #Abo - flips to Sweden
                if ( iGameTurn > xml.i1300AD and iGameTurn < xml.i1540AD ):
                        # 1320AD
                        self.foundCity(iIndependent, lNizhnyNovgorod, "Nizhny Novgorod", iGameTurn, 1, xml.iCrossbowman, 1, -1, 0 )
                        self.foundCity(iIndependent2, lVologda, "Vologda", iGameTurn, 1, xml.iCrossbowman, 2, -1, 0 )
                        # 1410AD
                        self.foundCity(iIndependent, lReykjavik, "Reykjavik", iGameTurn, 1, xml.iVikingBeserker, 2, -1, 1 ) #Morholt
                        # 1530AD
                        self.foundCity(iIndependent4, lValletta, "Valletta", iGameTurn, 1, xml.iKnightofStJohns, 3, xml.iCatholicism, 0 ) #Morholt
                        
                if ( iGameTurn == 1 ):
                        self.setupMinorNation()
                
                self.doMinorNations(iGameTurn)
                
                
                
        def getCity(self, tCoords): #by LOQ
                'Returns a city at coordinates tCoords.'
                return CyGlobalContext().getMap().plot(tCoords[0], tCoords[1]).getPlotCity()

        def foundCity(self, iCiv, lCity, name, iTurn, iPopulation, iUnitType, iNumUnits,iReligion, iWorkers ):
                if ((iTurn == lCity[2] + lCity[3]) and (lCity[3]<10)):
                        #print self.checkRegion(tUr)
                        bResult, lCity[3] = self.checkRegion(lCity)
                        if (bResult == True):
                                pCiv = gc.getPlayer(iCiv)
                                pCiv.found(lCity[0], lCity[1])
                                self.getCity((lCity[0], lCity[1])).setName(name, False)
                                if (iPopulation != 1):
                                        self.getCity((lCity[0], lCity[1])).setPopulation(iPopulation)
                                if (iNumUnits > 0):
                                        self.makeUnit(iUnitType, iCiv, (lCity[0], lCity[1]), iNumUnits, 0, "")
                                if (iWorkers > 0):
                                        self.makeUnit(xml.iWorker, iCiv, (lCity[0], lCity[1]), iWorkers, 0, "")
                                if ( iReligion > -1 ):
                                        self.getCity((lCity[0], lCity[1])).setHasReligion(iReligion, True, True, False)
                                return True
                        if (bResult == False) and (lCity[3] == -1):
                                return False
                               

        def checkRegion(self, tCity):
                cityPlot = gc.getMap().plot(tCity[0], tCity[1])
##                iNumUnitsInAPlot = cityPlot.getNumUnits()
##                print iNumUnitsInAPlot
                
                #checks if the plot already belongs to someone
                if (cityPlot.isOwned()):
                        if (cityPlot.getOwner() != iBarbarian ):
                                return (False, -1)
                    
##                #checks if there's a unit on the plot
##                if (iNumUnitsInAPlot):
##                        for i in range(iNumUnitsInAPlot):
##                                unit = currentPlot.getUnit(i)
##                                iOwner = unit.getOwner()
##                                pOwner = gc.getPlayer(iOwner)
##                                if (pOwner.isHuman()):
##                                        return (False, tCity[3]+1)

                #checks the surroundings and allows only AI units
                for x in range(tCity[0]-1, tCity[0]+2):
                        for y in range(tCity[1]-1, tCity[1]+2):
                                currentPlot=gc.getMap().plot(x,y)
                                if (currentPlot.isCity()):
                                        return (False, -1)
                                # 3Miro: Allow city founding even if the Human has units nearby
                                #iNumUnitsInAPlot = currentPlot.getNumUnits()
                                #if (iNumUnitsInAPlot):
                                #        for i in range(iNumUnitsInAPlot):
                                #                unit = currentPlot.getUnit(i)
                                #                iOwner = unit.getOwner()
                                #                pOwner = gc.getPlayer(iOwner)
                                #                if (pOwner.isHuman()):
                                #                        pass
                                #                       #return (False, tCity[3]+1)
                return (True, tCity[3])



        def spawnUnits(self, iCiv, tTopLeft, tBottomRight, iUnitType, iNumUnits, iTurn, iPeriod, iRest, function, iForceAttack, szName):
                if (iTurn % iPeriod == iRest):
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, [] )
                        if (len(plotList)):
                                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
                                result = plotList[rndNum]
                                if (result):
                                        self.makeUnit(iUnitType, iCiv, result, iNumUnits, iForceAttack, szName)
       	#This is just a clone of spawnUnits but attempting to put a boat under them
        def spawnVikings(self, iCiv, tTopLeft, tBottomRight, iUnitType, iNumUnits, iTurn, iPeriod, iRest, function, iForceAttack, szName):
                if (iTurn % iPeriod == iRest):
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, [] )
                        if (len(plotList)):
                                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
                                result = plotList[rndNum]
                                if (result):
                                        pPlayer = gc.getPlayer( iCiv )
                                        pUnit = pPlayer.initUnit(xml.iGalley, result[0], result[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                        if ( szName != "" ):
                                                pUnit.setName( szName )
                                        self.makeUnit(iUnitType, iCiv, result, iNumUnits, iForceAttack, szName )
       
        def spawnPirate(self, iCiv, tTopLeft, tBottomRight, iShipType, iNumShips, iFighterType, iNumFighters, iTurn, iPeriod, iRest, function, iForceAttack, szName):
                if (iTurn % iPeriod == iRest):
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, [] )
                        if (len(plotList)):
                                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
                                result = plotList[rndNum]
                                if (result):
                                	#pPlayer = gc.getPlayer( iCiv )
                                	#pPlayer.initUnit(iUnitType, result[0], result[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                	#pPlayer.initUnit(xml.iGalley, result[0], result[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                	self.makeUnit(iShipType, iCiv, result, iNumShips, 2, szName)
                                	self.makeUnit(iFighterType, iCiv, result, iNumFighters, 1, szName)


        def killNeighbours(self, tCoords):
                'Kills all units in the neigbbouring tiles of plot (as well as plot itself) so late starters have some space.'
                for x in range(tCoords[0]-1, tCoords[0]+2):        # from x-1 to x+1
                        for y in range(tCoords[1]-1, tCoords[1]+2):	# from y-1 to y+1
                                killPlot = CyMap().getPlot(x, y)
                                for i in range(killPlot.getNumUnits()):
                                        unit = killPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
                                        unit.kill(False, iBarbarian)

        def onImprovementDestroyed(self,iX,iY):
                print ("Barb improvement destroyed")
                iTurn = gc.getGame().getGameTurn()
                if (iTurn > xml.i1500AD):
                        self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iMusketman,1,1,1,0,utils.outerInvasion,1)
                elif (iTurn > xml.i1284AD):
                        self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iArquebusier,1,1,1,0,utils.outerInvasion,1)
                elif (iTurn > xml.i840AD):
                        self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iHorseArcher,1,1,1,0,utils.outerInvasion,1)
                else:
                        self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iSpearman,1,1,1,0,utils.outerInvasion,1)

# 3Miro: Minor Nations Start
        def setupMinorNation( self ):
                lNextMinorRevolt = self.getRevolDates()
                
                for lNation in lMinorNations:
                        #iNextRevolt = lNation[3][0] -3 + gc.getGame().getSorenRandNum(6, 'roll to modify the Natios revolt odds')
                        iNextRevolt = lNation[3][0]
                        while iNextRevolt in lNextMinorRevolt:
                                iNextRevolt = lNation[3][0] -3 + gc.getGame().getSorenRandNum(6, 'roll to modify the Natios revolt odds')
                        print(" Revolt Date ",iNextRevolt)
                        iNationIndex = lMinorNations.index(lNation)                        
                        print(" NationIndex ",iNationIndex)
                        lNextMinorRevolt[iNationIndex] = iNextRevolt
                
                self.setRevolDates( lNextMinorRevolt )
                        

        def doMinorNations( self, iGameTurn ):
                lNextMinorRevolt = self.getRevolDates()
                
                if ( iGameTurn in lNextMinorRevolt ):
                        #iNation = lNextMinorRevolt.index( iGameTurn )
                        lNation = lMinorNations[ lNextMinorRevolt.index( iGameTurn ) ]
                        lRevolts = lNation[3]
                        for iRevoltDate in lRevolts:
                                if ( (iRevoltDate - 3 <= iGameTurn) and (iRevoltDate + 3 >= iGameTurn) ):
                                        iRevoltIndex = lRevolts.index( iRevoltDate )
                                        break
                        # loop over all the province tiles to find the cities revolting
                        lPlayersOwning = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
                        iProvince = lNation[0]
                        for iI in range( gc.getNumProvinceTiles( iProvince ) ):
                                iX = gc.getProvinceX( iProvince, iI )
                                iY = gc.getProvinceY( iProvince, iI )
                                if ( gc.getMap().plot( iX, iY ).isCity() ):
                                        iOwner = gc.getMap().plot( iX, iY ).getPlotCity().getOwner()
                                        if ( iOwner > -1 and iOwner < con.iPope ): # pope doesn't count here
                                                if ( (not iOwner in lNation[1]) and ( not gc.getPlayer( iOwner ).getStateReligion() in lNation[2] ) ):
                                                        lPlayersOwning[iOwner] += 1
                        
                        for iPlayer in range( con.iPope ):
                                if ( lPlayersOwning[iPlayer] > 0 ):
                                        if ( utils.getHumanID() == iPlayer ):
                                                self.doRevoltHuman( iPlayer, iGameTurn, lNation, iRevoltIndex )
                                        else:
                                                self.doRevoltAI( iPlayer, iGameTurn, lNation, iRevoltIndex )
                        # setup next revolt
                        iRevoltIndex += 1
                        if ( iRevoltIndex < len( lNation[3] ) ):
                                iNextRevolt = lNation[3][iRevoltIndex] -3 + gc.getGame().getSorenRandNum(6, 'roll to modify the Natios revolt odds')
                                while iNextRevolt in lNextMinorRevolt:
                                        iNextRevolt = lNation[3][iRevoltIndex] -3 + gc.getGame().getSorenRandNum(6, 'roll to modify the Natios revolt odds')
                                lNextMinorRevolt[lNextMinorRevolt.index( iGameTurn )] = iNextRevolt
                                self.setRevolDates( lNextMinorRevolt )
                        
                                                
        # revolution choice effects: suppress with force, revolt +1 turn, unhappy +1 for 10 turns, suppression chance 20% + 5% per unit stationed (cap at 33%)
        #                            bribe the lords, 10 gold per population, suppression depends on the government Divine Monarchy (33%), Feudal or Limited (25%), Merchant (20%), Decentral (15%)
        #                            passive stability: >0 add 20%, additional +2% for every point above 5 (cap at 34% for +12 Stability)
        def doRevoltAI( self, iPlayer, iGameTurn, lNation, iRevoltIndex ):
                cityList = []
                for iI in range( gc.getNumProvinceTiles( lNation[0] ) ):
                        iX = gc.getProvinceX( lNation[0], iI )
                        iY = gc.getProvinceY( lNation[0], iI )
                        if ( gc.getMap().plot( iX, iY ).isCity() ):
                                pCity = gc.getMap().plot( iX, iY ).getPlotCity()
                                if ( pCity.getOwner() == iPlayer ):
                                        cityList.append(pCity)
                
                # AI always cracks on revolt
                iSuppressOdds = 20
                iNumGarrason = 0
                for iI in range( len( cityList ) ):
                        iNumGarrason += self.getGarrasonSize( cityList[iI] )
                iSuppressOdds += min( (5 * iNumGarrason) / len( cityList ), 13 )
                # Passive bonus from Stability
                pPlayer = gc.getPlayer( iPlayer )
                if ( pPlayer.getStability() > 0 ):
                        iSuppressOdds += 20 + max( 0, min( (pPlayer.getStability() - 5)*2, 14 ) )
                
                # substract the strength of the revolt
                iSuppressOdds -= lNation[4][iRevoltIndex]
                # time to roll the dice
                if ( iSuppressOdds > gc.getGame().getSorenRandNum(100, 'monor nation revolt') ):
                        # revolt suppressed
                        for iI in range( len( cityList ) ):
                                pCity = cityList[iI]
                                pCity.changeHurryAngerTimer( 10 )
                                pCity.changeOccupationTimer( 1 )
                                self.makeRebels( pCity, lNation[5][iRevoltIndex], 2*lNation[6][iRevoltIndex], lNation[7][1] )
                else:
                        # revolt succeeded
                        iRndNum = gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random independent')
                        iNewCiv = con.iIndepStart + iRndNum
                        for iI in range( len( cityList ) ):
                                pCity = cityList[iI]
                                utils.cultureManager((pCity.getX(),pCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
                                utils.flipUnitsInCityBefore((pCity.getX(),pCity.getY()), iNewCiv, iPlayer)                            
                                self.setTempFlippingCity((pCity.getX(),pCity.getY()))
                                utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iNewCiv, [iPlayer])   #by trade because by conquest may raze the city
                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
                                
        def showPopup(self, popupID, title, message, labels):
                popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
                popup.setHeaderString(title)
                popup.setBodyString(message)
                for i in labels:
                    popup.addButton( i )
                popup.launch(False)
                
                
        
        def eventApply7627( self, popupReturn ):
                iDecision = popupReturn.getButtonClicked()
                iNationIndex, iRevoltIndex = self.getNationRevoltIndex()
                #print("Event Apply",iNationIndex, iRevoltIndex,iDecision )
                lNation = lMinorNations[iNationIndex]
                iPlayer = utils.getHumanID()
                
                cityList = []
                for iI in range( gc.getNumProvinceTiles( lNation[0] ) ):
                        iX = gc.getProvinceX( lNation[0], iI )
                        iY = gc.getProvinceY( lNation[0], iI )
                        if ( gc.getMap().plot( iX, iY ).isCity() ):
                                pCity = gc.getMap().plot( iX, iY ).getPlotCity()
                                if ( pCity.getOwner() == iPlayer ):
                                        cityList.append(pCity)
                
                # raw suppress score
                iSuppressOdds = - lNation[4][iRevoltIndex]
                pPlayer = gc.getPlayer( iPlayer )
                if ( pPlayer.getStability() > 0 ):
                        iSuppressOdds += 20 + max( 0, min( (pPlayer.getStability() - 5)*2, 14 ) )
                
                if ( iDecision == 1 or iDecision == 3 ):
                        iNumGarrason = 0
                        for iI in range( len( cityList ) ):
                                iNumGarrason += self.getGarrasonSize( cityList[iI] )
                        iSuppressOdds += 20 + min( (5 * iNumGarrason) / len( cityList ), 13 )
                
                if ( iDecision == 2 or iDecision == 3 ):
                        iBribeGold = 0
                        for iI in range( len( cityList ) ):
                                iBribeGold += 10 * cityList[iI].getPopulation()
                        iGovernment = pPlayer.getCivics(0)
                        if ( iGovernment == xml.iCivicDespotism ):
                                iBribeOdds = 15
                        elif ( iGovernment == xml.iCivicFeudalMonarchy ):
                                iBribeOdds = 25
                        elif ( iGovernment == xml.iCivicDivineMonarchy ):
                                iBribeOdds = 33
                        elif ( iGovernment == xml.iCivicLimitedMonarchy ):
                                iBribeOdds = 25
                        elif ( iGovernment == xml.iCivicMerchantRepublic ):
                                iBribeOdds = 20
                        iGold = pPlayer.getGold()
                        if ( iGold < iBribeGold ):
                                iBribeOdds = ( iBribeOdds * iGold ) / ( iBribeGold )
                        pPlayer.setGold( iGold - min( iGold, iBribeGold ) )
                        iSuppressOdds += iBribeOdds
                 
                #if ( iSuppressOdds > gc.getGame().getSorenRandNum(100, 'monor nation revolt') ):
                #print(" Chance to suppress. ")
                if ( iSuppressOdds > gc.getGame().getSorenRandNum(100, 'monor nation revolt') ):
                        # revolt suppressed
                        if ( iDecision == 1 or iDecision == 3 ):
                                for iI in range( len( cityList ) ):
                                        pCity = cityList[iI]
                                        pCity.changeHurryAngerTimer( 10 )
                                        pCity.changeOccupationTimer( 1 )
                                        if ( iDecision == 2 or iDecision == 3 ):
                                                self.makeRebels( pCity, lNation[5][iRevoltIndex], lNation[6][iRevoltIndex], lNation[7][1] )
                                        else:
                                                self.makeRebels( pCity, lNation[5][iRevoltIndex], 2*lNation[6][iRevoltIndex], lNation[7][1] )
                else:
                        # revolt succeeded
                        iRndNum = gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random independent')
                        iNewCiv = con.iIndepStart + iRndNum
                        for iI in range( len( cityList ) ):
                                pCity = cityList[iI]
                                CyInterface().addMessage(iPlayer, True, con.iDuration, pCity.getName() + " " + CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                                utils.cultureManager((pCity.getX(),pCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
                                utils.flipUnitsInCityBefore((pCity.getX(),pCity.getY()), iNewCiv, iPlayer)                            
                                self.setTempFlippingCity((pCity.getX(),pCity.getY()))
                                utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iNewCiv, [iPlayer])   #by trade because by conquest may raze the city
                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)       
                                
                
                        
        def doRevoltHuman( self, iPlayer, iGameTurn, lNation, iRevoltIndex ):
                self.setNationRevoltIndex( lMinorNations.index(lNation), iRevoltIndex )
                
                cityList = []
                for iI in range( gc.getNumProvinceTiles( lNation[0] ) ):
                        iX = gc.getProvinceX( lNation[0], iI )
                        iY = gc.getProvinceY( lNation[0], iI )
                        if ( gc.getMap().plot( iX, iY ).isCity() ):
                                pCity = gc.getMap().plot( iX, iY ).getPlotCity()
                                if ( pCity.getOwner() == iPlayer ):
                                        cityList.append(pCity)
                
                # rebellion odds
                # raw odds considering minor nation strength and player stability
                iRawOdds = - lNation[4][iRevoltIndex]
                pPlayer = gc.getPlayer( iPlayer )
                if ( pPlayer.getStability() > 0 ):
                        iRawOdds += 20 + max( 0, min( (pPlayer.getStability() - 5)*2, 14 ) )
                # odds adjusted by a crack-down
                iCrackOdds = 20
                iNumGarrason = 0
                iBribeGold = 0
                for iI in range( len( cityList ) ):
                        iNumGarrason += self.getGarrasonSize( cityList[iI] )
                        iBribeGold += 10 * cityList[iI].getPopulation()
                iCrackOdds += min( (5 * iNumGarrason) / len( cityList ), 13 )
                # bibery odds
                #bribe the lords, 10 gold per population, suppression depends on the government Divine Monarchy (33%), Feudal or Limited (25%), Merchant (20%), Decentral (15%)
                iGovernment = pPlayer.getCivics(0)
                if ( iGovernment == xml.iCivicDespotism ):
                        iBribeOdds = 15
                elif ( iGovernment == xml.iCivicFeudalMonarchy ):
                        iBribeOdds = 25
                elif ( iGovernment == xml.iCivicDivineMonarchy ):
                        iBribeOdds = 33
                elif ( iGovernment == xml.iCivicLimitedMonarchy ):
                        iBribeOdds = 25
                elif ( iGovernment == xml.iCivicMerchantRepublic ):
                        iBribeOdds = 20
                iGold = pPlayer.getGold()
                if ( iGold < iBribeGold ):
                        iBribeOdds = ( iBribeOdds * iGold ) / ( iBribeGold )
                
                
                #iLoyalPrice = min( (10 * gc.getPlayer( utils.getHumanID() ).getGold()) / 100, 50 * iNumCities )
                szRebellName = localText.getText(lNation[7][0], ())
                #print( szTitle )
                self.showPopup(7627, localText.getText("TXT_KEY_MINOR_REBELLION_TITLE", (szRebellName,) ), \
                                localText.getText("TXT_KEY_MINOR_REBELLION_DESC", (szRebellName,) ), \
                                (localText.getText("TXT_KEY_MINOR_REBELLION_DO_NOTHING", ( iRawOdds, )), \
                                 localText.getText("TXT_KEY_MINOR_REBELLION_CRACK", ( iRawOdds + iCrackOdds, )), \
                                 localText.getText("TXT_KEY_MINOR_REBELLION_BRIBE", ( min( iGold, iBribeGold ), iRawOdds + iBribeOdds, )), \
                                 localText.getText("TXT_KEY_MINOR_REBELLION_ALL", ( iRawOdds + iBribeOdds + iCrackOdds, )), \
                                  ))


        def getGarrasonSize( self, pCity ):
                pPlot = gc.getMap().plot( pCity.getX(), pCity.getY() )
		iOwner = pPlot.getOwner()
		if ( iOwner < 0 ):
			return 0
		iNumUnits = pPlot.getNumUnits()
		iDefenders = 0
		for i in range( iNumUnits ):
			if ( pPlot.getUnit(i).getOwner() == iOwner ):
				iDefenders += 1
		return iDefenders

        def makeRebels( self, pCity, iUnit, iCount, szName ):
                lAvailableFreeTiles = []
                lAvailableTiles = []
                iTX = pCity.getX()
                iTY = pCity.getY()
                for y in range( 3 ):
                        for x in range( 3 ):
                                iX = iTX + x - 1 # try to spawn not across the river
                                iY = iTY + y - 1
                                if ( (iX>=0) and (iX<con.iMapMaxX) and (iY>=0) and (iY<con.iMapMaxY) ):
                                        pPlot = gc.getMap().plot( iX, iY )
                                        if ( pPlot.isHills() or pPlot.isFlatlands() ):
                                                if ( pPlot.getNumUnits() == 0 and (not pPlot.isCity()) ):
                                                        lAvailableFreeTiles.append( (iX, iY) )
                                                elif ( not pPlot.isCity() ): 
                                                        lAvailableTiles.append( (iX, iY) )
                                                        
                if ( len( lAvailableFreeTiles ) > 0 ):
                        iI = gc.getGame().getSorenRandNum(len(lAvailableFreeTiles),'select a free tile for the rebels')
                        iTX = lAvailableFreeTiles[iI][0]
                        iTY = lAvailableFreeTiles[iI][1]
                elif ( len( lAvailableTiles ) > 0 ):
                        # if all tiles are taken, select one tile at random and kill all units there
                        iI = gc.getGame().getSorenRandNum(len(lAvailableTiles),'select a taken tile for the rebels')
                        iTX = lAvailableTiles[iI][0]
                        iTY = lAvailableTiles[iI][1]
                        pPlot = gc.getMap().plot( iX, iY )
                        iN = pPlot.getNumUnits()
                        for i in range( iN ):
                                pPlot.getUnit( i ).kill( False, con.iBarbarian )
                else:
                        iTX = -1
                        iTY = -1

                if ( iTX != -1 and iTY != -1 ):
                        pBarb = gc.getPlayer( con.iBarbarian )
                        for iI in range( iCount ):
                                pUnit = pBarb.initUnit(iUnit, iTX, iTY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
                                pUnit.setName( localText.getText(szName, ()) )
        
