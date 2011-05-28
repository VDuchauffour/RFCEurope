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

lMarrakesh = [18,14,157,0] #1071 AD
lTangier = [24,23,0,0] #500 AD
lCorunna = [25,40,75,0] #800 AD
lToledo = [28,32,45,0] #680 AD
lLeon = [28,37,50,0] # 700 AD
lBurgos = [32,35,50,0] # 700 AD
#lZaragoza = [35,32,45,0] # 680 AD
lValencia = [34,29,50,0] #700 AD
lPamplona = [35,35,50,0] #700 AD
lBurdigala = [37,40,0,0] #500 AD
lNantes = [37,45,0,0] #500 AD
lAlger = [39,20,0,0] #500 AD
lBarcino = [39,31,0,0] #500 AD
#lCaen = [40,48,0,0] #500 AD
lCalais = [45,50,100,0] #900 AD
lToulouse = [41,37,0,0] #500 AD
lTours = [42,42,0,0] #500 AD
lMarseilles = [45,33,0,0] #500 AD
lLyon = [46,37,0,0] #500 AD
lTunis = [49,17,0,0] #500 AD
lPisae = [52,32,0,0] #500 AD These guys want to start with Catholicism?
lMediolanum = [52,37,0,0] #500 AD
lMilan = [52,37,75,0] #800 AD The respawn gambit, so that it still exists if razed
lFlorentia = [54,31,0,0] #500 AD
lFirenze = [54,31,75,0] #800 AD Same as Mediolanum--->Milan 
lTripoli = [56,6,0,0] #500 AD
lRoma = [56,27,0,0] #500 AD
lAugsburg = [55,41,0,0] #500 AD
#lCatania = [58,18,0,0] #500 AD
lNapoli = [60,24,0,0] #500 AD
lRagusa = [64,28,0,0] #500 AD
lBeograd = [68,31,0,0] #500 AD
lRhodes = [79,12,0,0] # 500 AD
lYork = [44,58,50,0] # 700 AD
lEdinburgh = [42,62,90,0] #860 AD
lDublin = [36,58,50,0] # 700 AD
lLubeck = [58,53,50,0] #700 AD
lTonsberg = [58,64,65,0] #760 AD
lLeipzig = [59,48,75,0] #800 AD
lPrague = [61,44,75,0] #800 AD
lKharkov = [90,46,75,0] #800 AD
lSamara = [97,54,240,0] #1320 AD
lKazan = [97,60,240,0] #1320 AD
lNovgorod = [80,62,240,0] #1320 AD
lMinsk = [76,50,120,0] #960 AD
lAlbaIulia = [73,34,100,0] #900 AD
lRiga = [72,58,240,0] #1320 AD
lMemel = [70,55,240,0] #1320 AD
lTvanksta = [70,54,100,0] #900 AD
lBreslau = [65,45,100,0] #900 AD
lKrakow = [69,44,100,0] #900 AD
lYaroslavl = [92,61,240,0] #1320 AD
lVologda = [89,64,240,0] #1320 AD
lTver = [85,60,240,0] #1320 AD
lSmolensk = [85,53,240,0] #1320 AD
lSaraiBatu = [99,40,200,0] #1200 AD
lMus = [99,21,153,0] #1060 AD
lPalermo = [55,19,2,0] # 508 AD
lGroningen = [52,54,150,0] #1050 AD

#handicap level modifier
iHandicapOld = (gc.getGame().getHandicapType() - 1)



class Barbs:

        def makeUnit(self, iUnit, iPlayer, tCoords, iNum, iForceAttack):
                'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
                for i in range(iNum):
                        player = gc.getPlayer(iPlayer)
                        if (iForceAttack == 0):
                                player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
                        elif (iForceAttack == 1):
                                player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)                                  
                        elif (iForceAttack == 2):
                                player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK_SEA, DirectionTypes.DIRECTION_SOUTH)


        def checkTurn(self, iGameTurn):
            
                #handicap level modifier
                iHandicap = (gc.getGame().getHandicapType() - 1)

                #debug
                #if (iGameTurn % 50 == 1):
                #        print ("iHandicap", iHandicap)
                #        print ("iHandicapOld", iHandicapOld)

		#Animals. Wolves in Scandinavia. Bears in Russia, Lions in Africa
		if (iGameTurn <= xml.i1000AD):
                        self.spawnUnits( iBarbarian, (56, 53), (99, 72), xml.iWolf, 1, iGameTurn, 17, 2, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (86, 40), (99, 72), xml.iBear, 1, iGameTurn, 19, 4, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (0, 1), (52, 10), xml.iLion, 1, iGameTurn, 23, 1, utils.outerInvasion, 0)
                
		#Mediterranean Pirates (Light before 1500,then heavy for rest of game)
		if ( iGameTurn >= xml.i960AD and iGameTurn < xml.i1401AD):
			self.spawnPirate( iBarbarian, (9,15), (55,33), xml.iWarGalley, 1, 0, 0, iGameTurn, 10, 3, utils.outerSeaSpawn, 1)
		
		if ( iGameTurn >= xml.i1401AD ):
			self.spawnPirate( iBarbarian, (9,15), (55,33), xml.iCorsair, 1, 0, 0, iGameTurn, 5,3, utils.outerSeaSpawn, 1)
			
		#if ( iGameTurn >= con.i1401AD ):
		#	self.spawnPirate( iBarbarian, (9,15), (55,33), con.iCara, 1, 0, 0, iGameTurn, 10, 7, utils.outerSeaSpawn, 1)

		if ( iGameTurn >= xml.i1200AD and iGameTurn < xml.i1500AD):
			self.spawnPirate( iBarbarian, (9,15), (55,33), xml.iCogge, 1, xml.iSwordsman, 2, iGameTurn, 10, 5, utils.outerSeaSpawn, 1)

		if ( iGameTurn >= xml.i1500AD ):
			self.spawnPirate( iBarbarian, (9,15), (55,33), xml.iGalleon, 1, xml.iMusketman, 2, iGameTurn, 10, 5, utils.outerSeaSpawn, 1)

		
		#Germanic Barbarians throughout Western Europe (France, Germany)
		if (iGameTurn < xml.i800AD):
			self.spawnUnits( iBarbarian, (45,45),(62,55), xml.iAxeman, 1 + iHandicap*2, iGameTurn,10,0,utils.outerInvasion,1)
			#self.spawnUnits( iBarbarian, (45,45),(62,55), con.iSpearman, 1 + iHandicap*2, iGameTurn,15,0,utils.outerInvasion,1)
		#if (iGameTurn >= con.i800AD and iGameTurn <= con.i1000AD):
		#	self.spawnUnits( iBarbarian, (45,45),(62,55), con.iHorseArcher, 1 + iHandicap*2, iGameTurn,4,0,utils.outerInvasion,1)
		if (iGameTurn < xml.i770AD):
                        self.spawnUnits( iBarbarian, (45,45),(62,55), xml.iAxeman, 1 + iHandicap*2, iGameTurn,12,6,utils.outerInvasion,1)

		#Longobards in Italy

		if (iGameTurn >= xml.i632AD and iGameTurn <= xml.i800AD):
			self.spawnUnits( iBarbarian, (50,30),(55,38), xml.iAxeman, 1 + iHandicap*2, iGameTurn,10,0,utils.outerInvasion,1)
		
		#Christians in Spain, this might be a bit overtuned, but lets wait for feedback
		if (iGameTurn >= xml.i700AD and iGameTurn <= xml.i880AD):
			self.spawnUnits( iBarbarian, (24,32),(28,40), xml.iAxeman, 1 + iHandicap*2, iGameTurn,14,0,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (24,32),(28,40), xml.iSpearman, 1 + iHandicap*2, iGameTurn,18,3,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (24,32),(28,40), xml.iMountedInfantry, 1 + iHandicap*2, iGameTurn,15,5,utils.outerInvasion,1)
			
			self.spawnUnits( iBarbarian, (20,28),(24,34), xml.iAxeman, 1 + iHandicap*2, iGameTurn,14,5,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (20,28),(24,34), xml.iSpearman, 1 + iHandicap*2, iGameTurn,18,9,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (20,28),(24,34), xml.iMountedInfantry, 1 + iHandicap*2, iGameTurn,16,14,utils.outerInvasion,1)
		
		#Berbers in North Africa
		if (iGameTurn >= xml.i700AD and iGameTurn < xml.i1060AD):
			self.spawnUnits(iBarbarian, (19,18),(27,21), xml.iHorseArcher, 1 + iHandicap*2, iGameTurn,25,3,utils.outerInvasion,1)
		
		#Avars in Austria-Hungary from 550 AD to 800 AD	
		if (iGameTurn >= xml.i632AD and iGameTurn < xml.i800AD):
			self.spawnUnits( iBarbarian, (60,30),(75,40), xml.iHorseArcher, 1 + iHandicap*2, iGameTurn,5,0,utils.outerInvasion,1)
		
		#Pre-Bulgarian Slavs in South Balkans
		if (iGameTurn < xml.i640AD):
			self.spawnUnits( iBarbarian, (68,18),(78,28), xml.iHorseArcher, 1 + iHandicap*2, iGameTurn,5,0,utils.outerInvasion,1)
		#East Greeece from 
		if (iGameTurn < xml.i720AD):
			self.spawnUnits( iBarbarian, (66,21),(69,28), xml.iAxeman, 1 + iHandicap*2, iGameTurn,12,3,utils.outerInvasion,1)

		#Misc Asiatic tribes to keep Ukraine empty
		if (iGameTurn >= xml.i632AD and iGameTurn < xml.i800AD):
			self.spawnUnits( iBarbarian, (80,36),(87,40), xml.iScout, 1 + iHandicap*2, iGameTurn,7,1,utils.outerInvasion,1)

		#Khazars 800 to 1100 		
		if (iGameTurn >= xml.i800AD and iGameTurn < xml.i940AD):
			self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iHorseArcher, 1 + iHandicap*2, iGameTurn,7,0,utils.outerInvasion,1)
		if (iGameTurn >= xml.i940AD and iGameTurn < xml.i1000AD):
			self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iHorseArcher, 1 + iHandicap*2, iGameTurn,5,1,utils.outerInvasion,1)

		#Pechenegs and Cumans in Northern Balkans
		if (iGameTurn >= xml.i940AD and iGameTurn < xml.i1160AD):
			self.spawnUnits( iBarbarian, (66,33),(78,43), xml.iHorseArcher, 2 + iHandicap*2, iGameTurn,6,1,utils.outerInvasion,1)
		
		#Vikings on ships 
		if (gc.getPlayer(con.iNorse).isHuman()): #Humans can properly go viking without help
			pass
		elif (iGameTurn >= xml.i800AD and iGameTurn < xml.i1000AD):
			self.spawnVikings( iBarbarian, (35,48),(50,55), xml.iVikingBeserker, 2, iGameTurn,8,0,utils.outerSeaSpawn,1)
		
		#Scots and Welsh to keep England busy
		if (iGameTurn>=xml.i1000AD and iGameTurn < xml.i1060AD):
			#Scots
			self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iAxeman, 2 + iHandicap*2, iGameTurn,8,0,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iSpearman, 2 + iHandicap*2, iGameTurn,8,0,utils.outerInvasion,1)
		if (gc.getPlayer(con.iEngland).isHuman()): #anti-exploit
			if (iGameTurn >= xml.i1060AD and iGameTurn < xml.i1320AD):
				self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iHighlander, 1 + iHandicap*2, iGameTurn,13,0,utils.outerInvasion,1)
			if (iGameTurn >= xml.i1320AD and iGameTurn < xml.i1500AD):
				self.spawnUnits( iBarbarian, (39,64),(44,67), xml.iHighlander, 1 + iHandicap*2, iGameTurn,19,0,utils.outerInvasion,1)
			if (iGameTurn>=xml.i1060AD and iGameTurn < xml.i1160AD):
				#Welsh
				self.spawnUnits( iBarbarian, (37,55),(39,57), xml.iWelshLongbowman, 1 + iHandicap*2, iGameTurn,13,1,utils.outerInvasion,1)
		else:
			if (iGameTurn >= xml.i1060AD and iGameTurn < xml.i1320AD):
				self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iHighlander, 1 + iHandicap*2, iGameTurn,16,0,utils.outerInvasion,1)
			if (iGameTurn >= xml.i1320AD and iGameTurn < xml.i1500AD):
				self.spawnUnits( iBarbarian, (39,64),(44,67), xml.iHighlander, 1 + iHandicap*2, iGameTurn,24,0,utils.outerInvasion,1)
			if (iGameTurn>=xml.i1060AD and iGameTurn < xml.i1160AD):
				#Welsh
				self.spawnUnits( iBarbarian, (37,55),(39,57), xml.iWelshLongbowman, 1 + iHandicap*2, iGameTurn,17,3,utils.outerInvasion,1)

		
		#Magyars (preceeding Hungary)
		if (iGameTurn >= xml.i840AD and iGameTurn < xml.i940AD):
			self.spawnUnits( iBarbarian, (54,40),(62,49), xml.iHorseArcher, 1 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,1)

                #barbs in the middle east
		if (gc.getPlayer(con.iArabia).isAlive()):
                        if (iGameTurn>=xml.i700AD and iGameTurn <= xml.i1300AD ):
                            if (not gc.getTeam(gc.getPlayer(con.iArabia).getTeam()).isHasTech(xml.iFarriers)):
                                self.spawnUnits( iBarbarian, (94,0),(99,3), xml.iHorseArcher, 1 + iHandicap*2, iGameTurn,12,3,utils.outerInvasion,1)
                            else:
                                self.spawnUnits( iBarbarian, (94,0),(99,3), xml.iArabiaGhazi, 1 + iHandicap*2, iGameTurn,10,2,utils.outerInvasion,1)

                #Pre Mongols to keep Kiev busy
		if (iGameTurn >=xml.i900AD and iGameTurn < xml.i1236AD):
                        self.spawnUnits( iBarbarian, (93,32),(99,44), xml.iHorseArcher, 1 + iHandicap*2, iGameTurn,12,3,utils.outerInvasion,1)

                #bars in anatolia pre Seljuks
                if (iGameTurn < xml.i1050AD ):
			#Middle East
			self.spawnUnits( iBarbarian, (97,20),(99,26), xml.iHorseArcher, 1 + iHandicap*2, iGameTurn,12,11,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (97,20),(99,26), xml.iAxeman, 1 + iHandicap*2, iGameTurn,14,2,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (97,20),(99,26), xml.iSpearman, 1 + iHandicap*2, iGameTurn,16,6,utils.outerInvasion,1)
		
		#Seljuks 1067
		if (iGameTurn>=xml.i1067AD and iGameTurn < xml.i1089AD):
			#Middle East
			self.spawnUnits( iBarbarian, (90,15),(99,28), xml.iSeljuk, 5 + iHandicap*2, iGameTurn,3,0,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (90,15),(99,28), xml.iSeljuk, 5 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (95,0),(99,15), xml.iSeljuk, 5 + iHandicap*2, iGameTurn,3,2,utils.outerInvasion,1)

		#Mongols! 1250
		if (iGameTurn >=xml.i1236AD and iGameTurn < xml.i1288AD):
			if iHandicap == 1: #Sedna17: Making mongols too weak in viceroy makes AI Kiev a super-power.
				iExtra = 1
			else:
				iExtra = 0
			#Kiev
			self.spawnUnits( iBarbarian, (93,32),(99,44), xml.iMongolKeshik, 3 + iExtra*2, iGameTurn,4,0,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (93,32),(99,44), xml.iMongolKeshik, 3 + iExtra*2, iGameTurn,3,1,utils.outerInvasion,1)
			#Central Europe (So Kiev can't keep them out)
			self.spawnUnits( iBarbarian, (65,30),(90,55), xml.iMongolKeshik, 4 + iExtra*2, iGameTurn,4,2,utils.outerInvasion,1)
			#self.spawnUnits( iBarbarian, (79,37),(85,47), xml.iMongolKeshik, 3 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,0)
			#Moscow
			self.spawnUnits( iBarbarian, (89,46),(99,56), xml.iMongolKeshik, 3 + iExtra*2, iGameTurn,4,0,utils.outerInvasion,1)
			#self.spawnUnits( iBarbarian, (89,46),(99,56), xml.iMongolKeshik, 3 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,0)
			#Middle East
			self.spawnUnits( iBarbarian, (94,15),(99,26), xml.iMongolKeshik, 3 + iExtra*2, iGameTurn,3,2,utils.outerInvasion,1)
			#self.spawnUnits( iBarbarian, (94,15),(99,26), xml.iMongolKeshik, 1 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,0)

		#Mongols, the return! (aka Tamerlane)
		if (iGameTurn >=xml.i1359AD and iGameTurn <=xml.i1431AD):
			#Eastern Europe
			self.spawnUnits( iBarbarian, (85,47),(99,57), xml.iMongolKeshik, 1 + iHandicap*2, iGameTurn,7,0,utils.outerInvasion,1)
			#Anatolia
			self.spawnUnits( iBarbarian, (87,17),(99,26), xml.iMongolKeshik, 2 + iHandicap*2, iGameTurn,4,0,utils.innerInvasion,1)
			
		
		#Setting cities to size 2 initially has no effect. They start with zero-sized culture, so immediately shrink one pop. Hack is to start with three.
		# 3Miro Barbarian and Independent city spawn and barbarian invasions go here. Check with original RFC file for details
		self.foundCity(iBarbarian, lMarrakesh, "Marrakesh", iGameTurn, 1, xml.iCrossbowman, 2, xml.iIslam) # Pop size, unit, num units UnitOwner=23 -> iBarbarian
		self.foundCity(iIndependent2, lTangier, "Tangier", iGameTurn, 1, xml.iCordobanBerber, 2, -1) #UnitOwner = 22 -> iIndy2 
		self.foundCity(iBarbarian, lToledo, "Toledo", iGameTurn, 1, xml.iArcher, 2, xml.iCatholicism)
		self.foundCity(iIndependent, lValencia, "Valencia", iGameTurn, 1, xml.iArcher, 1, xml.iCatholicism)
		self.foundCity(iIndependent3, lLyon, "Lyon", iGameTurn, 1, xml.iArcher, 2, xml.iCatholicism) # 3Miro add Lyon to flip to Burgundy
		self.foundCity(iIndependent3, lPalermo, "Palermo", iGameTurn, 1, xml.iArcher, 1, xml.iCatholicism)
		self.foundCity(iIndependent4, lPamplona, "Pamplona", iGameTurn, 1, xml.iCrossbowman, 2, -1)
		self.foundCity(iBarbarian, lBurdigala, "Burdigala", iGameTurn, 2, xml.iArcher, 1, -1)
		self.foundCity(iIndependent3, lAlger, "Alger", iGameTurn, 1, xml.iArcher, 1, -1)
		self.foundCity(iIndependent2, lBarcino, "Barcino", iGameTurn, 1, xml.iArcher, 1, -1)
		self.foundCity(iIndependent4, lCalais, "Calais", iGameTurn, 1, xml.iCrossbowman, 2, -1)
		self.foundCity(iBarbarian, lToulouse, "Tolosa", iGameTurn, 1, xml.iArcher, 1, -1)
		self.foundCity(iIndependent, lMarseilles, "Massilia", iGameTurn, 1, xml.iArcher, 1, xml.iCatholicism)
		self.foundCity(iIndependent2, lTunis, "Tunis", iGameTurn, 1, xml.iArcher, 1, -1)
		self.foundCity(iIndependent, lMediolanum, "Mediolanum", iGameTurn, 3, xml.iArcher, 1, xml.iCatholicism)
		self.foundCity(iIndependent, lMilan, "Milano", iGameTurn, 5, xml.iArcher, 2, xml.iCatholicism)
		self.foundCity(iIndependent2, lFlorentia, "Florentia", iGameTurn, 3, xml.iArcher, 1, xml.iCatholicism)
		self.foundCity(iIndependent2, lFirenze, "Firenze", iGameTurn, 5, xml.iArcher, 2, xml.iCatholicism)
		self.foundCity(iBarbarian, lTripoli, "Tripoli", iGameTurn, 1, xml.iArcher, 1, -1) 
		self.foundCity(iIndependent3, lAugsburg, "Augsburg", iGameTurn, 1, xml.iArcher, 1, -1)
		self.foundCity(iIndependent, lNapoli, "Neapolis", iGameTurn, 3, xml.iArcher, 1, -1)
		self.foundCity(iIndependent2, lRagusa, "Ragusa", iGameTurn, 1, xml.iArcher, 1, xml.iCatholicism)
		self.foundCity(iBarbarian, lBeograd, "Beograd", iGameTurn, 1, xml.iArcher, 2, -1)
		self.foundCity(iIndependent2, lRhodes, "Rhodes", iGameTurn, 1, xml.iArcher, 1, xml.iOrthodoxy) #Start with Orthodoxy and a Harbor?
		self.foundCity(iIndependent4, lYork, "Eboracum", iGameTurn, 1, xml.iArcher, 2, -1)
		self.foundCity(iBarbarian, lEdinburgh, "Eidyn Dun", iGameTurn, 1, xml.iArcher, 2, -1)
		self.foundCity(iBarbarian, lDublin, "Dubh Linn", iGameTurn, 1, xml.iArcher, 2, xml.iCatholicism)
		self.foundCity(iIndependent3, lTonsberg, "Tonsberg", iGameTurn, 1, xml.iArcher, 2, -1)
		self.foundCity(iBarbarian, lRiga, "Riga", iGameTurn, 1, xml.iCrossbowman, 2, -1)
		self.foundCity(iIndependent4, lTvanksta, "Tvanksta", iGameTurn, 1, xml.iCrossbowman, 2, -1)
		self.foundCity(iIndependent2, lLubeck, "Liubice", iGameTurn, 1, xml.iArcher, 2, -1)
		self.foundCity(iIndependent, lPrague, "Praha", iGameTurn, 1, xml.iCrossbowman, 2, xml.iCatholicism)
		self.foundCity(iIndependent3, lKrakow, "Krakow", iGameTurn, 1, xml.iCrossbowman, 2, xml.iCatholicism)
		self.foundCity(iIndependent4, lKharkov, "Kharkov", iGameTurn, 1, xml.iCrossbowman, 2, xml.iCatholicism)
		self.foundCity(iBarbarian, lAlbaIulia, "Belograd", iGameTurn, 1, xml.iCrossbowman, 1, -1)
		self.foundCity(iBarbarian, lSamara, "Samara", iGameTurn, 1, xml.iCrossbowman, 1, -1)
		self.foundCity(iBarbarian, lKazan, "Bulgar", iGameTurn, 1, xml.iCrossbowman, 1, -1)
		self.foundCity(iIndependent3, lYaroslavl, "Yaroslavl", iGameTurn, 1, xml.iCrossbowman, 1, -1)
		self.foundCity(iIndependent2, lVologda, "Vologda", iGameTurn, 1, xml.iCrossbowman, 2, -1)
		self.foundCity(iIndependent2, lNovgorod, "Novgorod", iGameTurn, 1, xml.iCrossbowman, 2, -1)
		self.foundCity(iIndependent4, lSmolensk, "Smolensk", iGameTurn, 1, xml.iCrossbowman, 1, -1)
		self.foundCity(iIndependent3, lMinsk, "Minsk", iGameTurn, 1, xml.iCrossbowman, 2, -1)
		self.foundCity(iBarbarian, lSaraiBatu, "Sarai Batu", iGameTurn, 1, xml.iLongbowman, 2, -1)
		self.foundCity(iBarbarian, lMus, "Mus", iGameTurn, 1, xml.iLongbowman, 2, -1)
		self.foundCity(iIndependent2, lGroningen, "Groningen", iGameTurn, 1, xml.iCrossbowman, 2, xml.iCatholicism)


        def getCity(self, tCoords): #by LOQ
                'Returns a city at coordinates tCoords.'
                return CyGlobalContext().getMap().plot(tCoords[0], tCoords[1]).getPlotCity()

        def foundCity(self, iCiv, lCity, name, iTurn, iPopulation, iUnitType, iNumUnits,iReligion):
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
                                        self.makeUnit(iUnitType, iCiv, (lCity[0], lCity[1]), iNumUnits, 0)
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
                                iNumUnitsInAPlot = currentPlot.getNumUnits()
                                if (iNumUnitsInAPlot):
                                        for i in range(iNumUnitsInAPlot):
                                                unit = currentPlot.getUnit(i)
                                                iOwner = unit.getOwner()
                                                pOwner = gc.getPlayer(iOwner)
                                                if (pOwner.isHuman()):
                                                        return (False, tCity[3]+1)
                return (True, tCity[3])



        def spawnUnits(self, iCiv, tTopLeft, tBottomRight, iUnitType, iNumUnits, iTurn, iPeriod, iRest, function, iForceAttack):
                if (iTurn % iPeriod == iRest):
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, [] )
                        if (len(plotList)):
                                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
                                result = plotList[rndNum]
                                if (result):
                                        self.makeUnit(iUnitType, iCiv, result, iNumUnits, iForceAttack)
       	#This is just a clone of spawnUnits but attempting to put a boat under them
        def spawnVikings(self, iCiv, tTopLeft, tBottomRight, iUnitType, iNumUnits, iTurn, iPeriod, iRest, function, iForceAttack):
                if (iTurn % iPeriod == iRest):
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, [] )
                        if (len(plotList)):
                                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
                                result = plotList[rndNum]
                                if (result):
                                	pPlayer = gc.getPlayer( iCiv )
                                	pPlayer.initUnit(xml.iGalley, result[0], result[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                        self.makeUnit(iUnitType, iCiv, result, iNumUnits, iForceAttack)
       
	def spawnPirate(self, iCiv, tTopLeft, tBottomRight, iShipType, iNumShips, iFighterType, iNumFighters, iTurn, iPeriod, iRest, function, iForceAttack):
		if (iTurn % iPeriod == iRest):
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, [] )
                        if (len(plotList)):
                                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
                                result = plotList[rndNum]
                                if (result):
                                	#pPlayer = gc.getPlayer( iCiv )
                                	#pPlayer.initUnit(iUnitType, result[0], result[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                	#pPlayer.initUnit(xml.iGalley, result[0], result[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                	self.makeUnit(iShipType, iCiv, result, iNumShips, 2)
                                	self.makeUnit(iFighterType, iCiv, result, iNumFighters, 1)

	    
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
			self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iMusketman,1,1,1,0,utils.outerInvasion,1)
		elif (iTurn > xml.i1284AD):
			self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iArquebusier,1,1,1,0,utils.outerInvasion,1)
			self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iArquebusier,1,1,1,0,utils.outerInvasion,1)
		elif (iTurn > xml.i840AD):
			self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iGuisarme,1,1,1,0,utils.outerInvasion,1)
			self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iHorseArcher,1,1,1,0,utils.outerInvasion,1)
		else:
			self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iSpearman,1,1,1,0,utils.outerInvasion,1)
			self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),xml.iScout,1,1,1,0,utils.outerInvasion,1)

