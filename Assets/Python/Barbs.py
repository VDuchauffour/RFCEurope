## Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import PyHelpers        # LOQ
import Popup
import cPickle as pickle        	# LOQ 2005-10-12
import RFCUtils
import Consts as con

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()


### Constants ###

iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iIndependent3 = con.iIndependent3
iIndependent4 = con.iIndependent4
#pIndependent = gc.getPlayer(iIndependent)
#pIndependent2 = gc.getPlayer(iIndependent2)
#teamIndependent = gc.getTeam(pIndependent.getTeam())
#teamIndependent2 = gc.getTeam(pIndependent2.getTeam())

iBarbarian = con.iBarbarian
pBarbarian = gc.getPlayer(iBarbarian)
teamBarbarian = gc.getTeam(pBarbarian.getTeam())
      

# 3Miro: comment all out for now, what do spawn and respawn mean, Babylon is never barbarian nor independent? what is retry?
# 3Miro: I believe those are only used for barb spawns coordinates in the class below
# city coordinates, spawn 1st turn and retries

lMarrakesh = [18,14,157,0] #1071 AD
lTangier = [24,23,0,0] #500 AD
lCorunna = [25,40,75,0] #500 AD
lToledo = [28,32,45,0] #700 AD
lLeon = [28,37,50,0] # 720 AD
lBurgos = [32,35,50,0] # 720 AD
#lZaragoza = [35,32,45,0] # 720 AD
lValencia = [34,29,50,0] #700 AD
lPamplona = [35,35,50,0] #500 AD
lBurdigala = [37,40,0,0] #500 AD
lNantes = [37,45,0,0] #500 AD
lAlger = [39,20,0,0] #500 AD
lBarcino = [39,31,0,0] #500 AD
#lCaen = [40,48,0,0] #500 AD
lCalais = [45,50,100,0] #500 AD
lToulouse = [41,37,0,0] #500 AD
lTours = [42,42,0,0] #500 AD
lMarseilles = [45,33,0,0] #500 AD
lLyon = [46,37,0,0] #500 AD
lTunis = [49,17,0,0] #500 AD
lPisae = [52,32,0,0] #500 AD These guys want to start with Catholicism?
lMilano = [52,37,0,0] #500 AD
lFirenze = [55,31,0,0] #500 AD
lTripoli = [56,6,0,0] #500 AD
lRoma = [56,27,0,0] #500 AD
lAugsburg = [56,41,0,0] #500 AD
lCatania = [58,18,0,0] #500 AD
lNapoli = [59,24,0,0] #500 AD
lRagusa = [64,28,0,0] #500 AD
lBeograd = [68,32,0,0] #500 AD
lRhodes = [79,12,0,0] # 500 AD
lYork = [44,58,50,0] # 700 AD
lEdinburgh = [42,62,90,0] #860 AD
lDublin = [36,58,50,0] # 700 AD
lLubeck = [58,53,50,0] #700 AD
lTonsberg = [58,64,65,0] #760 AD
lLeipzig = [59,48,75,0] #800 AD
lPrague = [61,44,75,0] #800 AD
lKharkov = [90,46,75,0] #800 AD
lSamara = [97,54,240,0] #800 AD
lKazan = [97,60,240,0] #800 AD
lNovgorod = [80,62,240,0] #800 AD
lMinsk = [76,50,120,0] #800 AD
lRiga = [72,58,240,0] #900 AD
lMemel = [70,55,240,0] #900 AD
lTvanksta = [70,54,100,0] #900 AD
lBreslau = [65,46,100,0] #900 AD
lYaroslavl = [92,61,240,0] #900 AD
lVologda = [89,64,240,0] #900 AD
lTver = [85,60,240,0] #900 AD
lSmolensk = [85,53,240,0] #900 AD
lAstrakhan = [99,40,200,0] #1200 AD


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
		if (iGameTurn <= con.i1000AD):
                        self.spawnUnits( iBarbarian, (56, 53), (99, 72), con.iWolf, 1, iGameTurn, 17, 2, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (86, 40), (99, 72), con.iBear, 1, iGameTurn, 19, 4, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (0, 1), (52, 10), con.iLion, 1, iGameTurn, 23, 1, utils.outerInvasion, 0)
                
		#Mediterranean Pirates (Light before 1500,then heavy for rest of game)
		if ( iGameTurn >= con.i960AD and iGameTurn < con.i1401AD):
			self.spawnPirate( iBarbarian, (9,15), (55,33), con.iWarGalley, 1, 0, 0, iGameTurn, 10, 3, utils.outerSeaSpawn, 0)
		
		if ( iGameTurn >= con.i1401AD ):
			self.spawnPirate( iBarbarian, (9,15), (55,33), con.iCorsair, 1, 0, 0, iGameTurn, 5,3, utils.outerSeaSpawn, 0)
			
		#if ( iGameTurn >= con.i1401AD ):
		#	self.spawnPirate( iBarbarian, (9,15), (55,33), con.iCara, 1, 0, 0, iGameTurn, 10, 7, utils.outerSeaSpawn, 0)

		if ( iGameTurn >= con.i1200AD and iGameTurn < con.i1500AD):
			self.spawnPirate( iBarbarian, (9,15), (55,33), con.iCogge, 1, con.iSwordsman, 2, iGameTurn, 10, 5, utils.outerSeaSpawn, 0)

		if ( iGameTurn >= con.i1500AD ):
			self.spawnPirate( iBarbarian, (9,15), (55,33), con.iGalleon, 1, con.iMusketman, 2, iGameTurn, 10, 5, utils.outerSeaSpawn, 0)

		
		#Germanic Barbarians throughout Western Europe (France, Germany)
		if (iGameTurn >= con.i500AD and iGameTurn < con.i800AD):
			self.spawnUnits( iBarbarian, (45,45),(62,55), con.iAxeman, 1 + iHandicap*2, iGameTurn,10,0,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (45,45),(62,55), con.iSpearman, 1 + iHandicap*2, iGameTurn,15,0,utils.outerInvasion,1)
		if (iGameTurn >= con.i800AD and iGameTurn <= con.i1000AD):
			self.spawnUnits( iBarbarian, (45,45),(62,55), con.iHorseArcher, 1 + iHandicap*2, iGameTurn,7,0,utils.outerInvasion,1)

		#Longobards in Italy

		if (iGameTurn >= con.i632AD and iGameTurn <= con.i800AD):
			self.spawnUnits( iBarbarian, (50,30),(55,38), con.iAxeman, 1 + iHandicap*2, iGameTurn,10,0,utils.outerInvasion,1)
		
		#Christians in Spain
		if (iGameTurn >= con.i700AD and iGameTurn <= con.i880AD):
			self.spawnUnits( iBarbarian, (24,32),(28,40), con.iAxeman, 1 + iHandicap*2, iGameTurn,7,0,utils.outerInvasion,1)
		
		#Berbers in North Africa
		#if (iGameTurn >= con.i1000AD and iGameTurn < con.i1060AD):
		#	self.spawnUnits(iBarbarian, (16,12),(22,20), con.iCordobanBerber, 3 + iHandicap*2, iGameTurn,5,0,utils.outerInvasion,1)
		
		#Avars in Austria-Hungary from 550 AD to 800 AD	
		if (iGameTurn >= con.i632AD and iGameTurn < con.i800AD):
			self.spawnUnits( iBarbarian, (60,30),(75,40), con.iScout, 1 + iHandicap*2, iGameTurn,5,0,utils.outerInvasion,1)
		
		#Pre-Bulgarian Slavs in South Balkans
		if (iGameTurn > con.i500AD and iGameTurn < con.i640AD):
			self.spawnUnits( iBarbarian, (68,18),(78,28), con.iScout, 1 + iHandicap*2, iGameTurn,5,0,utils.outerInvasion,1)	

		#Misc Asiatic tribes to keep Ukraine empty
		if (iGameTurn >= con.i632AD and iGameTurn < con.i1000AD):
			self.spawnUnits( iBarbarian, (80,36),(87,40), con.iScout, 1 + iHandicap*2, iGameTurn,7,1,utils.outerInvasion,1)

		#Cumans and Pechenegs 800 to 1100 		
		if (iGameTurn >= con.i800AD and iGameTurn < con.i940AD):
			self.spawnUnits( iBarbarian, (90,20),(99,40), con.iHorseArcher, 1 + iHandicap*2, iGameTurn,10,0,utils.outerInvasion,1)
		if (iGameTurn >= con.i940AD and iGameTurn < con.i1000AD):
			self.spawnUnits( iBarbarian, (90,20),(99,40), con.iLancer, 1 + iHandicap*2, iGameTurn,10,1,utils.outerInvasion,1)
		
		#Vikings on ships 
		if (iGameTurn >= con.i800AD and iGameTurn < con.i880AD):
			self.spawnVikings( iBarbarian, (35,48),(50,55), con.iVikingBeserker, 1, iGameTurn,10,0,utils.outerSeaSpawn,1)

		

		#Scots and Welsh to keep England busy
		if (iGameTurn>=con.i1000AD and iGameTurn < con.i1060AD):
			#Scots
			self.spawnUnits( iBarbarian, (39,62),(44,66), con.iAxeman, 2 + iHandicap*2, iGameTurn,4,0,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (39,62),(44,66), con.iSpearman, 2 + iHandicap*2, iGameTurn,4,0,utils.outerInvasion,1)
		if (gc.getPlayer(con.iEngland).isHuman()): #anti-exploit
			if (iGameTurn >= con.i1060AD and iGameTurn < con.i1320AD):
				self.spawnUnits( iBarbarian, (39,62),(44,66), con.iHighlander, 1 + iHandicap*2, iGameTurn,13,0,utils.outerInvasion,1)
			if (iGameTurn >= con.i1320AD and iGameTurn < con.i1500AD):
				self.spawnUnits( iBarbarian, (39,64),(44,67), con.iHighlander, 1 + iHandicap*2, iGameTurn,19,0,utils.outerInvasion,1)
			if (iGameTurn>=con.i1060AD and iGameTurn < con.i1160AD):
				#Welsh
				self.spawnUnits( iBarbarian, (37,55),(39,57), con.iWelshLongbowman, 1 + iHandicap*2, iGameTurn,13,1,utils.outerInvasion,1)
		else:
			if (iGameTurn >= con.i1060AD and iGameTurn < con.i1320AD):
				self.spawnUnits( iBarbarian, (39,62),(44,66), con.iHighlander, 1 + iHandicap*2, iGameTurn,16,0,utils.outerInvasion,1)
			if (iGameTurn >= con.i1320AD and iGameTurn < con.i1500AD):
				self.spawnUnits( iBarbarian, (39,64),(44,67), con.iHighlander, 1 + iHandicap*2, iGameTurn,24,0,utils.outerInvasion,1)
			if (iGameTurn>=con.i1060AD and iGameTurn < con.i1160AD):
				#Welsh
				self.spawnUnits( iBarbarian, (37,55),(39,57), con.iWelshLongbowman, 1 + iHandicap*2, iGameTurn,17,3,utils.outerInvasion,1)

		
		#Magyars (preceeding Hungary)
		if (iGameTurn >= con.i840AD and iGameTurn < con.i940AD):
			self.spawnUnits( iBarbarian, (54,40),(62,49), con.iHorseArcher, 1 + iHandicap*2, iGameTurn,5,0,utils.outerInvasion,1)

		
		#Seljuks 1070
		if (iGameTurn>=con.i1050AD and iGameTurn < con.i1080AD):
			#Middle East
			self.spawnUnits( iBarbarian, (95,15),(99,28), con.iSeljuk, 3 + iHandicap*2, iGameTurn,2,0,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (95,15),(99,28), con.iSeljuk, 3 + iHandicap*2, iGameTurn,2,1,utils.outerInvasion,1)
			
		#Mongols! 1250
		if (iGameTurn >=con.i1236AD and iGameTurn < con.i1284AD):
			#Kiev
			self.spawnUnits( iBarbarian, (93,32),(99,44), con.iMongolKeshik, 3 + iHandicap*2, iGameTurn,4,0,utils.outerInvasion,1)
			self.spawnUnits( iBarbarian, (93,32),(99,44), con.iMongolKeshik, 3 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,1)
			#Central Europe (So Kiev can't keep them out)
			self.spawnUnits( iBarbarian, (70,30),(90,55), con.iMongolKeshik, 3 + iHandicap*2, iGameTurn,4,2,utils.outerInvasion,1)
			#self.spawnUnits( iBarbarian, (79,37),(85,47), con.iMongolKeshik, 3 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,0)
			#Moscow
			self.spawnUnits( iBarbarian, (89,46),(99,56), con.iMongolKeshik, 3 + iHandicap*2, iGameTurn,4,0,utils.outerInvasion,1)
			#self.spawnUnits( iBarbarian, (89,46),(99,56), con.iMongolKeshik, 3 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,0)
			#Middle East
			self.spawnUnits( iBarbarian, (94,15),(99,26), con.iMongolKeshik, 2 + iHandicap*2, iGameTurn,4,2,utils.outerInvasion,1)
			#self.spawnUnits( iBarbarian, (94,15),(99,26), con.iMongolKeshik, 1 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,0)

		#Mongols, the return! (aka Tamerlane)
		if (iGameTurn >=con.i1359AD and iGameTurn <=con.i1431AD):
			#Eastern Europe
			self.spawnUnits( iBarbarian, (99,47),(85,57), con.iMongolKeshik, 1 + iHandicap*2, iGameTurn,7,0,utils.outerInvasion,1)
			#Anatolia
			self.spawnUnits( iBarbarian, (99,17),(87,26), con.iMongolKeshik, 2 + iHandicap*2, iGameTurn,4,0,utils.outerInvasion,1)
			
		

               # 3Miro Barbarian and Independent city spawna nd barbarian invasions go here. Check with original RFC file for details
		self.foundCity(iBarbarian, lMarrakesh, "Marrakesh", iGameTurn, 1, con.iCrossbowman, 2) # Pop size, unit, num units UnitOwner=23 -> iBarbarian
		self.foundCity(iIndependent2, lTangier, "Tangier", iGameTurn, 1, con.iCordobanBerber, 2) #UnitOwner = 22 -> iIndy2 
		#self.foundCity(iIndependent3, lCorunna, "A Corunna", iGameTurn, 1, con.iCrossbowman, 2) #UnitOnwer = 21 -> iIndy
		self.foundCity(iBarbarian, lToledo, "Toledo", iGameTurn, 1, con.iArcher, 2)
		#self.foundCity(iIndependent3, lLeon, "Leon", iGameTurn, 1, con.iCrossbowman, 2)
		#self.foundCity(iIndependent3, lBurgos, "Burgos", iGameTurn, 1, con.iArcher, 2)
		self.foundCity(iIndependent, lValencia, "Valencia", iGameTurn, 1, con.iArcher, 1)
		#self.foundCity(iIndependent2,lZaragoza, "Zaragoza", iGameTurn, 1, con.iArcher, 1) 
		self.foundCity(iIndependent2, lPamplona, "Pamplona", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iBarbarian, lBurdigala, "Burdigala", iGameTurn, 2, con.iArcher, 1)
		#self.foundCity(iIndependent2, lNantes, "Nantes", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent3, lAlger, "Alger", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent4, lBarcino, "Barcino", iGameTurn, 1, con.iArcher, 1)
		#self.foundCity(iIndependent, lCaen, "Caen", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent, lCalais, "Calais", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iBarbarian, lToulouse, "Toulouse", iGameTurn, 1, con.iArcher, 1)
		#self.foundCity(iIndependent2, lTours, "Tours", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent3, lMarseilles, "Marseilles", iGameTurn, 1, con.iArcher, 1)
		#self.foundCity(iIndependent2, lLyon, "Lyon", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent4, lTunis, "Tunis", iGameTurn, 1, con.iArcher, 1)
		#self.foundCity(iIndependent, lPisae, "Pisae", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent, lMilano, "Milano", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent2, lFirenze, "Firenze", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iBarbarian, lTripoli, "Tripoli", iGameTurn, 1, con.iArcher, 1) 
		# self.foundCity(iIndependent, lRoma, "Roma", iGameTurn, 5, con.iArcher, 1)
		self.foundCity(iIndependent, lAugsburg, "Augsburg", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent2, lCatania, "Catania", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent3, lNapoli, "Napoli", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent3, lRagusa, "Ragusa", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iBarbarian, lBeograd, "Beograd", iGameTurn, 1, con.iArcher, 1)
		self.foundCity(iIndependent4, lRhodes, "Rhodes", iGameTurn, 1, con.iArcher, 1) #Start with Orthodoxy and a Harbor?
		self.foundCity(iIndependent4, lYork, "Eboracum", iGameTurn, 1, con.iArcher, 2)
		self.foundCity(iBarbarian, lEdinburgh, "Edinburgh", iGameTurn, 1, con.iArcher, 2)
		self.foundCity(iIndependent, lDublin, "Dubh Linn", iGameTurn, 1, con.iArcher, 2)
		self.foundCity(iIndependent2, lTonsberg, "Tonsberg", iGameTurn, 1, con.iArcher, 2)
		self.foundCity(iBarbarian, lRiga, "Riga", iGameTurn, 1, con.iCrossbowman, 2)
		#self.foundCity(iIndependent2, lMemel, "Memel", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iIndependent, lTvanksta, "Tvanksta", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iIndependent, lLubeck, "Liubice", iGameTurn, 1, con.iArcher, 2)
		#self.foundCity(iIndependent2, lLeipzig, "Leipzig", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iIndependent, lPrague, "Prague", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iIndependent2, lBreslau, "Breslau", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iIndependent3, lKharkov, "Kharkov", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iBarbarian, lSamara, "Samara", iGameTurn, 1, con.iCrossbowman, 1)
		self.foundCity(iBarbarian, lKazan, "Bulgar", iGameTurn, 1, con.iCrossbowman, 1)
		self.foundCity(iIndependent4, lYaroslavl, "Yaroslavl", iGameTurn, 1, con.iCrossbowman, 1)
		self.foundCity(iIndependent, lVologda, "Vologda", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iIndependent2, lNovgorod, "Novgorod", iGameTurn, 1, con.iCrossbowman, 2)
		#self.foundCity(iIndependent, lTver, "Tver", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iIndependent4, lSmolensk, "Smolensk", iGameTurn, 1, con.iCrossbowman, 1)
		self.foundCity(iIndependent3, lMinsk, "Minsk", iGameTurn, 1, con.iCrossbowman, 2)
		self.foundCity(iBarbarian, lAstrakhan, "Astrakhan", iGameTurn, 1, con.iLongbowman, 2)



        def getCity(self, tCoords): #by LOQ
                'Returns a city at coordinates tCoords.'
                return CyGlobalContext().getMap().plot(tCoords[0], tCoords[1]).getPlotCity()

        def foundCity(self, iCiv, lCity, name, iTurn, iPopulation, iUnitType, iNumUnits):
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
       	#This is just a clone of spawnUnits but attempting to but a boat under them
        def spawnVikings(self, iCiv, tTopLeft, tBottomRight, iUnitType, iNumUnits, iTurn, iPeriod, iRest, function, iForceAttack):
                if (iTurn % iPeriod == iRest):
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, [] )
                        if (len(plotList)):
                                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
                                result = plotList[rndNum]
                                if (result):
                                	pPlayer = gc.getPlayer( iCiv )
                                	pPlayer.initUnit(con.iGalley, result[0], result[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
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
                                	#pPlayer.initUnit(con.iGalley, result[0], result[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
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

