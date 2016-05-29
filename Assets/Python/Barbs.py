## Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import PyHelpers		# LOQ
import Popup
import RFCUtils
import Consts as con
import XMLConsts as xml
from StoredData import sd

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer		# LOQ
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


# Independent and barbarians city spawns
# Key: tCity = variations (coordinates, actual city name, chance), owner, population size, defender type, number of defenders, religion, workers
# Notes: Indy cities start with zero-sized culture, barbs with normal culture
#		Added some initial food reserves on founding cities, so even independents won't shrink on their first turn anymore
#		Barbarian cities start with 2 additional defender units
#		Walls (and other buildings) can be added with the onCityBuilt function, in RiseAndFall.py
# 500 AD
tTangier = ( [ ((27, 16), "Tangier", 100) ], iIndependent2, 1, xml.iCordobanBerber, 2, -1, 0 )
tBordeaux = ( [ ((37, 38), "Burdigala", 100) ], iBarbarian, 2, xml.iArcher, 0, -1, 0 )
tAlger = ( [ ((40, 16), "Alger", 100) ], iIndependent3, 1, xml.iArcher, 1, -1, 0 )
tBarcelona = ( [ ((40, 28), "Barcino", 100) ], iIndependent2, 1, xml.iArcher, 1, -1, 0 )
tToulouse = ( [ ((41, 34), "Tolosa", 30), ((40, 34), "Tolosa", 30), ((42, 32), "Narbo", 40) ], iBarbarian, 1, xml.iArcher, 0, -1, 0 )
tMarseilles = ( [ ((46, 32), "Massilia", 50), ((46, 33), "Aquae Sextiae", 50) ], iIndependent, 1, xml.iArcher, 1, xml.iCatholicism, 0 )
tNantes = ( [ ((36, 43), "Naoned", 50), ((35, 43), "Gwened", 30), ((37, 44), "Roazhon", 20) ], iIndependent2, 1, xml.iArcher, 1, -1, 0 )
tCaen = ( [ ((40, 47), "Caen", 100) ], iIndependent4, 2, xml.iArcher, 2, xml.iCatholicism, 1 )
tLyon = ( [ ((46, 37), "Lyon", 100) ], iIndependent3, 2, xml.iArcher, 2, xml.iCatholicism, 1 )
tTunis = ( [ ((49, 17), "Tunis", 100) ], iIndependent4, 1, xml.iArcher, 1, -1, 0 )
tYork = ( [ ((39, 59), "Eboracum", 100) ], iIndependent4, 1, xml.iArcher, 2, -1, 1 )
tLondon = ( [ ((41, 52), "Londinium", 100) ], iIndependent, 2, xml.iArcher, 2, xml.iCatholicism, 0 )
tMilan = ( [ ((52, 37), "Mediolanum", 100) ], iIndependent, 2, xml.iArcher, 2, xml.iCatholicism, 0 )
tFlorence = ( [ ((54, 32), "Florentia", 40), ((53, 32), "Pisae", 40), ((57, 31), "Ankon", 20) ], iIndependent2, 2, xml.iArcher, 2, xml.iCatholicism, 0 )
tTripoli = ( [ ((54, 8), "Tripoli", 100) ], iBarbarian, 1, xml.iArcher, 1, -1, 0 )
tAugsburg = ( [ ((55, 41), "Augsburg", 100) ], iIndependent3, 1, xml.iArcher, 2, -1, 0 )
tNapoli = ( [ ((59, 24), "Neapolis", 40), ((60, 25), "Beneventum", 40), ((62, 24), "Tarentum", 20) ], iIndependent, 2, xml.iArcher, 1, -1, 0 )
tRagusa = ( [ ((64, 28), "Ragusa", 100) ], iIndependent2, 1, xml.iArcher, 2, xml.iCatholicism, 0 )
tSeville = ( [ ((27, 21), "Hispalis", 100) ], iIndependent4, 1, xml.iArcher, 2, -1, 0 )
tPalermo = ( [ ((55, 19), "Palermo", 60), ((58, 17), "Syracuse", 40) ], iIndependent3, 1, xml.iArcher, 1, xml.iCatholicism, 1 )
# 552 AD
tInverness = ( [ ((37, 67), "Inbhir Nis", 50), ((37, 65), "Scaig", 50) ], iBarbarian, 1, xml.iArcher, 1, -1, 0)
# 600 AD
tRhodes = ( [ ((80, 13), "Rhodes", 100) ], iIndependent2, 1, xml.iArcher, 1, xml.iOrthodoxy, 0 )
# 640 AD
tNorwich = ( [ ((43, 55), "Norwich", 100) ], iIndependent3, 1, xml.iArcher, 1, -1, 1 ) #reduced to town on spawn of England
# 680 AD
tToledo = ( [ ((30, 27), "Toledo", 100) ], iBarbarian, 1, xml.iArcher, 1, xml.iCatholicism, 1 )
tLeicester = ( [ ((39, 56), "Ligeraceaster", 100) ], iIndependent, 1, xml.iArcher, 1, -1, 0 ) #reduced to town on spawn of England
# 700 AD
tValencia = ( [ ((36, 25), "Valencia", 100) ], iIndependent, 1, xml.iArcher, 1, xml.iCatholicism, 1 )
tPamplona = ( [ ((35, 32), "Pamplona", 70), ((34, 33), "Pamplona", 30) ], iIndependent4, 1, xml.iCrossbowman, 2, -1, 0 )
tDublin = ( [ ((32, 58), "Dubh Linn", 100) ], iBarbarian, 1, xml.iArcher, 1, xml.iCatholicism, 1 )
tLubeck = ( [ ((57, 54), "Liubice", 100) ], iIndependent2, 1, xml.iArcher, 2, -1, 1 )
tPorto = ( [ ((23, 31), "Portucale", 100) ], iIndependent3, 1, xml.iCrossbowman, 2, xml.iCatholicism, 0 )
# 760 AD
tTonsberg = ( [ ((57, 65), "Tonsberg", 100) ], iIndependent3, 1, xml.iArcher, 2, -1, 0)
# 768 AD
tRaska = ( [ ((68, 28), "Ras", 100) ], iIndependent2, 1, xml.iArcher, 2, -1, 1)
# 780 AD
tFez = ( [ ((29, 12), "Fes", 100) ], iIndependent4, 1, xml.iCrossbowman, 2, -1, 1)
# 800 AD
tMilanR = ( [ ((52, 37), "Milano", 100) ], iIndependent, 4, xml.iArcher, 2, xml.iCatholicism, 0) #respawn, in case it was razed
#tFlorenceR = ( [ ((54, 32), "Firenze", 100) ], iIndependent2, 4, xml.iArcher, 2, xml.iCatholicism, 0 ) #respawn
tPrague = ( [ ((60, 44), "Praha", 100) ], iIndependent, 1, xml.iCrossbowman, 2, xml.iCatholicism, 1)
tKursk = ( [ ((90, 48), "Kursk", 100) ], iIndependent4, 1, xml.iArcher, 2, -1, 0)
tCalais = ( [ ((44, 50), "Calais", 50), ((45, 50), "Dunkerque", 50)  ], iIndependent3, 1, xml.iCrossbowman, 2, -1, 0)
tNidaros = ( [ ((57, 71), "Nidaros", 100) ], iIndependent3, 1, xml.iArcher, 1, -1, 1) #Trondheim
tUppsala = ( [ ((65, 66), "Uppsala", 100) ], iIndependent4, 1, xml.iArcher, 2, -1, 1) #reduced to town on spawn of Sweden
tBeloozero = ( [ ((87, 65), "Beloozero", 100) ], iIndependent4, 1, xml.iCrossbowman, 1, -1, 1)
# 860 AD
#tEdinburgh = ( [ ((37, 63), "Eidyn Dun", 100) ], iBarbarian, 1, xml.iArcher, 1, -1, 0)
# 880 AD
tApulum = ( [ ((73, 35), "Belograd", 100) ], iIndependent, 1, xml.iArcher, 2, -1, 0)
# 900 AD
tTvanksta = ( [ ((69, 53), "Tvanksta", 100) ], iIndependent4, 1, xml.iCrossbowman, 2, -1, 0) #Königsberg
tKrakow = ( [ ((68, 44), "Krakow", 100) ], iIndependent3, 1, xml.iCrossbowman, 2, xml.iCatholicism, 0)
tRiga = ( [ ((74, 58), "Riga", 100) ], iIndependent, 2, xml.iCrossbowman, 2, -1, 1) #maybe call it Duna in the early pediod (Duna is the name of a sheltered natural harbor near Riga)
# 911 AD
tCaenR = ( [ ((40, 47), "Caen", 100) ], iIndependent2, 1,  xml.iCrossbowman, 2, xml.iCatholicism, 0) #respawn, on the establishment of the Duchy of Normandy
# 960 AD
tMinsk = ( [ ((79, 52), "Minsk", 100) ], iIndependent3, 1, xml.iCrossbowman, 2, -1, 0)
tSmolensk = ( [ ((84, 55), "Smolensk", 100) ], iIndependent4, 1, xml.iCrossbowman, 1, -1, 0)
# 1010 AD
tYaroslavl = ( [ ((92, 61), "Yaroslavl", 100) ], iIndependent3, 1, xml.iCrossbowman, 1, -1, 0)
# 1050 AD
tGroningen = ( [ ((52, 54), "Groningen", 100) ], iIndependent2, 1, xml.iCrossbowman, 2, xml.iCatholicism, 0)
tKalmar = ( [ ((64, 60), "Kalmar", 100) ], iIndependent2, 2, xml.iCrossbowman, 1, xml.iCatholicism, 1)
# 1060 AD
tMus = ( [ ((99, 21), "Mus", 100) ], iBarbarian, 1, xml.iLongbowman, 2, -1, 0)
# 1110 AD
tGraz = ( [ ((61, 37), "Graz", 100) ], iIndependent3, 2, xml.iCrossbowman, 2, xml.iCatholicism, 0)
# 1200 AD
tRigaR = ( [ ((74, 58), "Riga", 100) ], iIndependent, 3, xml.iCrossbowman, 2, -1, 1) #respawn
tSaraiBatu = ( [ ((99, 40), "Sarai Batu", 100) ], iBarbarian, 1, xml.iLongbowman, 2, -1, 0)
# 1227 AD
tTripoliR = ( [ ((54, 8), "Tarabulus", 100) ], iBarbarian, 3, xml.iArbalest, 2, xml.iIslam, 1) #respawn
# 1250 AD
tAbo = ( [ ((71, 66), "Abo", 100) ], iIndependent4, 1, xml.iCrossbowman, 1, -1, 0)
# 1320 AD
tNizhnyNovgorod = ( [ ((97, 58), "Nizhny Novgorod", 100) ], iIndependent, 1, xml.iCrossbowman, 1, -1, 0)
# 1392 AD
tTanais = ( [ ((96, 38), "Tana", 100) ], iBarbarian, 1, xml.iLongbowman, 2, xml.iIslam, 0)
# 1410 AD
tReykjavik = ( [ ((2, 70), "Reykjavik", 100) ], iIndependent, 1, xml.iVikingBeserker, 2, -1, 0)
# 1530 AD
tValletta = ( [ ((57, 14), "Valletta", 100) ], iIndependent4, 1, xml.iKnightofStJohns, 3, xml.iCatholicism, 0)

# Currently unused indy cities:
# Key: city coordinates, spawn turn, retries
#lTours = [40,43,0,0] #500 AD
#lOrleans = [42,44,0,0] #500 AD
#lCatania = [58,18,0,0] #500 AD
#lBeograd = [68,30,0,0] #500 AD
#lRavenna = [55,33,0,0] #500 AD
#lKairouan = [49,14,0,0] #500 AD
#lZaragoza = [36,29,45,0] #680 AD
#lBulgar = [97,60,45,0] #680 AD
#lLeon = [27,32,50,0] # 700 AD
#lBurgos = [30,32,50,0] #700 AD
#lCorunna = [24,35,75,0] #800 AD
#lLeipzig = [58,48,75,0] #800 AD
#lKharkov = [90,46,75,0] #800 AD
#lLadoga = [81,65,75,0] #800 AD
#lVelehrad = [64,42,82,0] #833 AD
#lNovgorod = [80,62,87,0] #848 AD
#lNottingham = [39,56,92,0] #867 AD, reduced to town on spawn of England
#lBreslau = [64,46,100,0] #900 AD
#lMunster = [52,50,150,0] #1050 AD
#lMarrakesh = [24,7,157,0] #1071 AD
#lLjubljana = [60,36,173,1] #1120 AD
#lKolyvan = [74,63,200,0] #1200 AD
#lPinsk = [77,48,210,0] #1230 AD
#lSamara = [97,54,240,0] #1320 AD
#lMemel = [70,55,240,0] #1320 AD, Klaipeda
#lVologda = [91,64,240,0] #1320 AD
#lTver = [88,60,240,0] #1320 AD
#lVisby = [67,60,264,0] #1393 AD
#lStaraSich = [88,40,300,0] #1500 AD

dIndependentCities = {
xml.i500AD : [ tTangier, tBordeaux, tAlger, tBarcelona, tToulouse, tMarseilles, tNantes, tCaen, tLyon, tTunis, tYork, tLondon, tMilan, tFlorence, tTripoli, tAugsburg, tNapoli, tRagusa, tSeville, tPalermo],
xml.i552AD : [ tInverness ],
xml.i600AD : [ tRhodes ],
xml.i640AD : [ tNorwich ],
xml.i680AD : [ tToledo, tLeicester ],
xml.i700AD : [ tValencia, tPamplona, tDublin, tLubeck, tPorto ],
xml.i760AD : [ tTonsberg ],
xml.i768AD : [ tRaska ],
xml.i780AD : [ tFez ],
xml.i800AD : [ tMilanR, tPrague, tKursk, tCalais, tNidaros, tUppsala, tBeloozero ],
xml.i880AD : [ tApulum ],
xml.i900AD : [ tTvanksta, tKrakow, tRiga ],
xml.i911AD : [ tCaenR ],
xml.i960AD : [ tMinsk, tSmolensk ],
xml.i1010AD : [ tYaroslavl ],
xml.i1050AD : [ tGroningen, tKalmar ],
xml.i1060AD : [ tMus ],
xml.i1110AD : [ tGraz ],
xml.i1200AD : [ tRigaR, tSaraiBatu ],
xml.i1227AD : [ tTripoliR ],
xml.i1250AD : [ tAbo ],
xml.i1320AD : [ tNizhnyNovgorod ],
xml.i1393AD : [ tTanais ],
xml.i1410AD : [ tReykjavik ],
xml.i1530AD : [ tValletta ],
}


# Minor Nations structure: [ int Province: all cities in this province will revolt
#			list nations: a city controlled by those players will not revolt (i.e. Greece wouldn't revolt against the Byz)
#			list religions: a city owned by someone with one of those state religions will not revolt (i.e. Jerusalem doesn't revolt against Muslims)
#			list revolt dates: the dates for the revolt,
#			list revolt strength: this is subtracted from the odds to suppress the revolt (i.e. high number more likely to succeed in the revolt)
#			list units: corresponding to the revolt, if we crack down on the rebels, what barbarian units should spawn
#			list number: corresponding to the revolt, if we crack down on the rebels, how many units should spawn (note if we don't bribe the Lords, then double the number of Units will spawn)
#			list text keys: text keys for "The Nation" and "Nation Adjective"
# Note: lists 3, 4, 5, 6 should have the same size
# Note: you should increase the size of 'lNextMinorRevolt' in StoredData to be at least the number of minor nations
lMinorNations = [ [ xml.iP_Serbia, [], [], [xml.i508AD,xml.i852AD,xml.i1346AD], [20,20,20], [xml.iAxeman,xml.iAxeman,xml.iLongSwordsman], [2,1,2], ["TXT_KEY_THE_SERBS","TXT_KEY_SERBIAN"] ],
		[ xml.iP_Scotland, [con.iScotland], [], [xml.i1297AD,xml.i1569AD,xml.i1715AD], [20,10,20], [xml.iHighlander,xml.iMusketman,xml.iGrenadier], [2,2,2], ["TXT_KEY_THE_SCOTS","TXT_KEY_SCOTTISH"] ],
		[ xml.iP_Catalonia, [con.iAragon], [], [xml.i1164AD+10,xml.i1640AD], [20,10], [xml.iLongSwordsman,xml.iMusketman], [2,2], ["TXT_KEY_THE_CATALANS","TXT_KEY_CATALAN"] ],
		[ xml.iP_Jerusalem, [con.iArabia,con.iTurkey,con.iByzantium], [xml.iIslam,], [xml.i1099AD+8,xml.i1099AD+16,xml.i1099AD+25,xml.i1099AD+33,xml.i1099AD+40,xml.i1099AD+47,xml.i1099AD+55,xml.i1099AD+65], [30,30,40,40,30,30,30,30], [xml.iMaceman,xml.iMaceman,xml.iMaceman,xml.iKnight,xml.iKnight,xml.iKnight,xml.iKnight,xml.iKnight], [3,3,4,3,3,3,3,3], ["TXT_KEY_THE_MUSLIMS","TXT_KEY_MUSLIM"] ],
		[ xml.iP_Syria, [con.iArabia,con.iTurkey,con.iByzantium], [xml.iIslam,], [xml.i1099AD+8,xml.i1099AD+16,xml.i1099AD+25,xml.i1099AD+33,xml.i1099AD+40,xml.i1099AD+47,xml.i1099AD+55,xml.i1099AD+65], [30,30,40,40,30,30,30,30], [xml.iMaceman,xml.iMaceman,xml.iMaceman,xml.iKnight,xml.iKnight,xml.iKnight,xml.iKnight,xml.iKnight], [3,3,4,3,3,3,3,3], ["TXT_KEY_THE_MUSLIMS","TXT_KEY_MUSLIM"] ],
		[ xml.iP_Oran, [], [], [xml.i1236AD,xml.i1346AD,xml.i1359AD,xml.i1542AD], [40,10,10,20], [xml.iKnight,xml.iHeavyLancer,xml.iHeavyLancer,xml.iMusketman], [2,2,2,2], ["TXT_KEY_THE_ZIYYANIDS","TXT_KEY_ZIYYANID"] ],
		[ xml.iP_Fez, [con.iMorocco], [], [xml.i1473AD], [30], [xml.iArquebusier], [4], ["TXT_KEY_THE_WATTASIDS","TXT_KEY_WATTASID"] ], ]
# 3Miro: Jerusalem and Syria were added here, so the Crusaders will not be able to control it for too long


class Barbs:

	def getRevolDates( self ):
		return sd.scriptDict['lNextMinorRevolt']

	def setRevolDates( self, lNextMinorRevolt ):
		sd.scriptDict['lNextMinorRevolt'] = lNextMinorRevolt

	def getTempFlippingCity( self ):
		return sd.scriptDict['tempFlippingCity']

	def setTempFlippingCity( self, tNewValue ):
		sd.scriptDict['tempFlippingCity'] = tNewValue

	def getNationRevoltIndex( self ):
		return sd.scriptDict['lRevoltinNationRevoltIndex']

	def setNationRevoltIndex( self, iNationIndex, iRevoltIndex ):
		sd.scriptDict['lRevoltinNationRevoltIndex'] = [iNationIndex,iRevoltIndex]

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
		#getHandicapType: Viceroy=0, Monarch=1, Emperor=2
		iHandicap = (gc.getGame().getHandicapType() - 1)
		#iHandicap: Viceroy=-1, Monarch=0, Emperor=1

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
		if (iGameTurn < xml.i600AD):
			self.spawnUnits( iBarbarian, (43,42),(50,50), xml.iAxeman, 1, iGameTurn,11,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
		if (iGameTurn >= xml.i600AD and iGameTurn < xml.i800AD):
			self.spawnUnits( iBarbarian, (43,42),(50,50), xml.iAxeman, 1, iGameTurn,9,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
			self.spawnUnits( iBarbarian, (42,40),(56,48), xml.iAxeman, 1, iGameTurn,11,4,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
		if (gc.getPlayer(con.iFrankia).isHuman()): #extra barbs for human France
			if (iGameTurn < xml.i600AD):
				self.spawnUnits( iBarbarian, (42,40),(56,48), xml.iAxeman, 1, iGameTurn,9,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
				self.spawnUnits( iBarbarian, (45,45),(60,55), xml.iSpearman, 1, iGameTurn,18,7,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
			if (iGameTurn >= xml.i600AD and iGameTurn < xml.i800AD):
				self.spawnUnits( iBarbarian, (43,42),(50,50), xml.iAxeman, 1, iGameTurn,9,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
				self.spawnUnits( iBarbarian, (45,45),(60,55), xml.iSpearman, 1 + iHandicap, iGameTurn,11,4,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))
				self.spawnUnits( iBarbarian, (46,48),(62,55), xml.iAxeman, 1 + iHandicap, iGameTurn,14,9,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()))

		#Longobards in Italy
		if (iGameTurn >= xml.i632AD and iGameTurn <= xml.i800AD):
			self.spawnUnits( iBarbarian, (49,33),(53,36), xml.iAxeman, 1 + iHandicap, iGameTurn,10,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_LONGOBARDS", ()))
			self.spawnUnits( iBarbarian, (49,33),(53,36), xml.iSpearman, 1, iGameTurn,12,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_LONGOBARDS", ()))

		#Christians in Spain
		if (iGameTurn >= xml.i700AD and iGameTurn <= xml.i892AD):
			self.spawnUnits( iBarbarian, (22,21),(26,25), xml.iAxeman, 1, iGameTurn,9,0,utils.outerInvasion,1, "")
			self.spawnUnits( iBarbarian, (20,23),(24,28), xml.iSpearman, 1, iGameTurn,7,2,utils.outerInvasion,1, "")
			self.spawnUnits( iBarbarian, (27,30),(32,35), xml.iAxeman, 1, iGameTurn,11,5,utils.outerInvasion,1, "")
		if (gc.getPlayer(con.iCordoba).isHuman()): #extra barbs for human Cordoba
			if (iGameTurn >= xml.i700AD and iGameTurn <= xml.i892AD):
				self.spawnUnits( iBarbarian, (24,31),(27,36), xml.iAxeman, 1 + iHandicap, iGameTurn,7,0,utils.outerInvasion,1, "")
				self.spawnUnits( iBarbarian, (27,28),(31,36), xml.iMountedInfantry, 1, iGameTurn,6,3,utils.outerInvasion,1, "")

		#Berbers in North Africa
		if (iGameTurn >= xml.i700AD and iGameTurn < xml.i1020AD):
			self.spawnUnits(iBarbarian, (21,3),(27,12), xml.iHorseArcher, 1, iGameTurn,9,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()))
			self.spawnUnits(iBarbarian, (22,3),(27,10), xml.iAxeman, 1, iGameTurn,11,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()))
			self.spawnUnits(iBarbarian, (23,3),(27,8), xml.iSpearman, 1, iGameTurn,7,4,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()))
			self.spawnUnits(iBarbarian, (26,10),(35,14), xml.iHorseArcher, 1 + iHandicap, iGameTurn,7,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()))

		#Avars in the Carpathian Basin
		if (iGameTurn >= xml.i632AD and iGameTurn < xml.i800AD):
			self.spawnUnits( iBarbarian, (60,30),(75,40), xml.iHorseArcher, 1, iGameTurn,5,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_AVARS", ()))
		if (gc.getPlayer(con.iBulgaria).isHuman()): #extra barbs for human Bulgaria
			if (iGameTurn >= xml.i632AD and iGameTurn < xml.i800AD):
				self.spawnUnits( iBarbarian, (66,26),(73,29), xml.iHorseArcher, 1 + iHandicap, iGameTurn,6,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_AVARS", ()))

		#Early barbs for Byzantium:
		#Pre-Bulgarian Slavs in the Balkans
		if (iGameTurn < xml.i640AD):
			self.spawnUnits( iBarbarian, (68,18),(78,28), xml.iAxeman, 1, iGameTurn,8,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS", ()))
		if (gc.getPlayer(con.iByzantium).isHuman()): #extra barbs for human Byzantium
			if (iGameTurn < xml.i640AD):
				self.spawnUnits( iBarbarian, (64,21),(75,25), xml.iAxeman, 1 + iHandicap, iGameTurn,11,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS", ()))
				self.spawnUnits( iBarbarian, (68,18),(78,28), xml.iSpearman, 1, iGameTurn,8,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS", ()))
		#Sassanids in Anatolia
		if (iGameTurn < xml.i640AD):
			self.spawnUnits( iBarbarian, (90,15),(99,28), xml.iLancer, 1, iGameTurn,5,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()))
			self.spawnUnits( iBarbarian, (94,19),(98,26), xml.iLancer, 1, iGameTurn,9,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()))
		if (gc.getPlayer(con.iByzantium).isHuman()): #extra Persians for human Byzantium
			if (iGameTurn < xml.i640AD):
				self.spawnUnits( iBarbarian, (90,15),(99,28), xml.iLancer, 1, iGameTurn,5,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()))
				self.spawnUnits( iBarbarian, (94,19),(98,26), xml.iLancer, 1 + iHandicap, iGameTurn,9,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()))
		#Barbs in Eastern Greece
		if (iGameTurn < xml.i720AD):
			self.spawnUnits( iBarbarian, (66,21),(69,28), xml.iAxeman, 1, iGameTurn,9,3,utils.outerInvasion,1, "")
		if (gc.getPlayer(con.iByzantium).isHuman()): #extra barbs for human Byzantium
			if (iGameTurn < xml.i720AD):
				self.spawnUnits( iBarbarian, (66,21),(69,28), xml.iSpearman, 1 + iHandicap, iGameTurn,9,3,utils.outerInvasion,1, "")

		#Serbs in the Southern Balkans
		if (iGameTurn >= xml.i1025AD and iGameTurn < xml.i1282AD):
			if (gc.getPlayer(con.iByzantium).isHuman()): #more barbs for human Byzantium
				self.spawnUnits( iBarbarian, (67,24),(73,28), xml.iAxeman, 1, iGameTurn,9,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SERBS", ()))
				self.spawnUnits( iBarbarian, (67,24),(73,28), xml.iLancer, 1 + iHandicap, iGameTurn,11,7,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SERBS", ()))
				self.spawnUnits( iBarbarian, (69,25),(71,29), xml.iSwordsman, 1, iGameTurn,7,4,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SERBS", ()))
			else: #less for the AI
				self.spawnUnits( iBarbarian, (67,24),(73,28), xml.iAxeman, 1, iGameTurn,9,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SERBS", ()))

		#Khazars
		if (iGameTurn >= xml.i660AD and iGameTurn < xml.i864AD):
			self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iAxeman, 1, iGameTurn,7,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()))
		if (iGameTurn >= xml.i864AD and iGameTurn < xml.i920AD):
			if (gc.getPlayer(con.iKiev).isHuman()): #more barbs for human Kiev
				self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iAxeman, 1, iGameTurn,9,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()))
				self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iSpearman, 1, iGameTurn,9,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()))
			else: #less for the AI
				self.spawnUnits( iBarbarian, (88,31),(99,40), xml.iAxeman, 1, iGameTurn,9,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()))

		#Pechenegs
		if (iGameTurn >= xml.i920AD and iGameTurn < xml.i1040AD):
			#in the Rus
			self.spawnUnits( iBarbarian, (89,34),(97,40), xml.iSteppeHorseArcher, 1, iGameTurn,8,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()))
			if (gc.getPlayer(con.iKiev).isHuman()): #more barbs for human Kiev
				self.spawnUnits( iBarbarian, (91,35),(99,44), xml.iSteppeHorseArcher, 1 + iHandicap, iGameTurn,5,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()))
			#in Hungary
			self.spawnUnits( iBarbarian, (66,35),(75,42), xml.iSteppeHorseArcher, 1, iGameTurn,9,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()))
			if (gc.getPlayer(con.iHungary).isHuman()): #extra barbs for human Hungary
				self.spawnUnits( iBarbarian, (66,35),(75,42), xml.iSteppeHorseArcher, 1 + iHandicap, iGameTurn,9,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()))
			#in Bulgaria
			if (gc.getPlayer(con.iBulgaria).isHuman()): #barbs for human Bulgaria
				self.spawnUnits( iBarbarian, (77,31),(79,33), xml.iSteppeHorseArcher, 2 + iHandicap, iGameTurn,5,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()))

		#Cumans and Kipchaks
		if (iGameTurn >= xml.i1040AD and iGameTurn < xml.i1200AD):
			#in the Rus
			if (gc.getPlayer(con.iKiev).isHuman()): #more barbs for human Kiev
				self.spawnUnits( iBarbarian, (89,34),(99,40), xml.iSteppeHorseArcher, 2, iGameTurn,7,5,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()))
				self.spawnUnits( iBarbarian, (90,33),(97,44), xml.iSteppeHorseArcher, 2 + iHandicap, iGameTurn,9,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS", ()))
			else: #less for the AI
				self.spawnUnits( iBarbarian, (89,34),(99,40), xml.iSteppeHorseArcher, 1, iGameTurn,7,5,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()))
				self.spawnUnits( iBarbarian, (89,34),(99,40), xml.iSteppeHorseArcher, 1, iGameTurn,9,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS", ()))
			#in Hungary
			self.spawnUnits( iBarbarian, (64,33),(77,43), xml.iSteppeHorseArcher, 1, iGameTurn,7,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()))
			if (gc.getPlayer(con.iHungary).isHuman()): #extra barbs for human Hungary
				self.spawnUnits( iBarbarian, (64,33),(77,43), xml.iSteppeHorseArcher, 1, iGameTurn,7,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()))
				self.spawnUnits( iBarbarian, (66,35),(75,42), xml.iSteppeHorseArcher, 1, iGameTurn,9,4,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS", ()))
			#in Bulgaria
			if (gc.getPlayer(con.iBulgaria).isHuman()): #barbs for human Bulgaria
				self.spawnUnits( iBarbarian, (78,32),(80,34), xml.iSteppeHorseArcher, 1, iGameTurn,7,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()))
				self.spawnUnits( iBarbarian, (78,32),(80,34), xml.iSteppeHorseArcher, 1, iGameTurn,7,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS", ()))

		#Vikings on ships
		if (gc.getPlayer(con.iNorway).isHuman()): #Humans can properly go viking without help
			pass
		elif (iGameTurn >= xml.i780AD and iGameTurn < xml.i1000AD):
			if (gc.getPlayer(con.iFrankia).isHuman()):
				self.spawnVikings( iBarbarian, (35,48),(50,55), xml.iVikingBeserker, 2, iGameTurn,8,0,utils.outerSeaSpawn,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_VIKINGS", ()))
			else:
				self.spawnVikings( iBarbarian, (35,48),(50,55), xml.iVikingBeserker, 1, iGameTurn,8,0,utils.outerSeaSpawn,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_VIKINGS", ()))

		#Swedish Crusades
		if (iGameTurn >= xml.i1150AD and iGameTurn < xml.i1210AD):
			self.spawnVikings( iBarbarian, (71,62),(76,65), xml.iVikingBeserker, 2, iGameTurn,6,1,utils.outerSeaSpawn,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SWEDES", ()))

		#Chudes in Finland and Estonia
		if (iGameTurn >= xml.i864AD and iGameTurn < xml.i1150AD):
			self.spawnUnits( iBarbarian, (72,67),(81,72), xml.iAxeman, 1, iGameTurn,7,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CHUDES", ()))
			self.spawnUnits( iBarbarian, (74,60),(76,63), xml.iAxeman, 1, iGameTurn,11,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_CHUDES", ()))

		#Livonian Order as barbs in the area before the Prussian spawn, but only if Prussia is AI (no need for potentially gained extra units for the human player)
		#Also pre-Lithanian barbs for human Prussia a couple turns before the Lithuanian spawn
		if (gc.getPlayer(con.iPrussia).isHuman()):
			if (iGameTurn >= xml.i1224AD and iGameTurn < xml.i1236AD):
				self.spawnUnits( iBarbarian, (73,56),(76,61), xml.iAxeman, 1, iGameTurn,2,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BALTICS", ()))
				self.spawnUnits( iBarbarian, (72,54),(75,59), xml.iAxeman, 1, iGameTurn,2,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BALTICS", ()))
				self.spawnUnits( iBarbarian, (73,56),(76,61), xml.iHorseArcher, 1 + iHandicap, iGameTurn,2,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BALTICS", ()))
		elif (iGameTurn >= xml.i1200AD and iGameTurn < xml.i1224AD):
			self.spawnUnits( iBarbarian, (73,56),(76,61), xml.iTeutonic, 1, iGameTurn,2,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SWORD_BRETHEN", ()))

		#Anglo-Saxons before the Danish 1st UHV (Conquer England)
		if (iGameTurn >= xml.i970AD and iGameTurn < xml.i1050AD):
			if (gc.getPlayer(con.iDenmark).isHuman()): #more barbs for human Denmark
				self.spawnUnits( iBarbarian, (36,53),(41,59), xml.iAxeman, 1, iGameTurn,8,5,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS", ()))
				self.spawnUnits( iBarbarian, (33,48),(38,56), xml.iAxeman, 1, iGameTurn,5,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS", ()))
				self.spawnUnits( iBarbarian, (33,48),(38,56), xml.iSwordsman, 1, iGameTurn,11,4,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS", ()))
			else: #less for the AI
				self.spawnUnits( iBarbarian, (33,48),(38,56), xml.iAxeman, 1, iGameTurn,5,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS", ()))

		#Scots to keep England busy, but only if Scotland is dead
		if ( not gc.getPlayer(con.iScotland).isAlive() ):
			if (gc.getPlayer(con.iEngland).isHuman()): #hard for the human player
				if (iGameTurn >= xml.i1060AD and iGameTurn < xml.i1320AD):
					self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iHighlander, 2, iGameTurn,11,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
				if (iGameTurn >= xml.i1320AD and iGameTurn < xml.i1500AD):
					self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iHighlander, 2, iGameTurn,9,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
					self.spawnUnits( iBarbarian, (39,64),(44,67), xml.iHighlander, 2 + iHandicap, iGameTurn,17,4,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
			else: #easy for the AI
				if (iGameTurn >= xml.i1060AD and iGameTurn < xml.i1320AD):
					self.spawnUnits( iBarbarian, (39,62),(44,66), xml.iHighlander, 1, iGameTurn,11,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))
				if (iGameTurn >= xml.i1320AD and iGameTurn < xml.i1500AD):
					self.spawnUnits( iBarbarian, (39,64),(44,67), xml.iHighlander, 2, iGameTurn,17,4,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()))

		#Welsh in Britain
		if (gc.getPlayer(con.iEngland).isHuman()): #more barbs for human England
			if (iGameTurn >= xml.i1060AD and iGameTurn < xml.i1160AD):
				self.spawnUnits( iBarbarian, (37,53),(39,57), xml.iWelshLongbowman, 1, iGameTurn,7,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()))
			if (iGameTurn >= xml.i1160AD and iGameTurn < xml.i1452AD):
				self.spawnUnits( iBarbarian, (37,53),(39,57), xml.iWelshLongbowman, 2 + iHandicap, iGameTurn,13,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()))
		else: #less for the AI
			if (iGameTurn >= xml.i1060AD and iGameTurn < xml.i1160AD):
				self.spawnUnits( iBarbarian, (37,53),(39,57), xml.iWelshLongbowman, 1, iGameTurn,13,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()))
			if (iGameTurn >= xml.i1160AD and iGameTurn < xml.i1452AD):
				self.spawnUnits( iBarbarian, (37,53),(39,57), xml.iWelshLongbowman, 1, iGameTurn,7,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()))

		#Magyars (preceeding Hungary)
		if (iGameTurn >= xml.i840AD and iGameTurn < xml.i892AD):
			self.spawnUnits( iBarbarian, (54,40),(62,49), xml.iHorseArcher, 1, iGameTurn,3,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()))
			self.spawnUnits( iBarbarian, (66,26),(73,29), xml.iHorseArcher, 1, iGameTurn,5,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()))
			if (gc.getPlayer(con.iBulgaria).isHuman()): #extra barbs for human Bulgaria
				self.spawnUnits( iBarbarian, (77,31),(80,34), xml.iHorseArcher, 2 + iHandicap, iGameTurn,3,0,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()))
			elif (gc.getPlayer(con.iGermany).isHuman()): #extra barbs for human Germany
				self.spawnUnits( iBarbarian, (54,40),(62,49), xml.iHorseArcher, 2 + iHandicap, iGameTurn,4,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()))

		#Barbs in the middle east
		if (iGameTurn >= xml.i700AD and iGameTurn <= xml.i1300AD ):
			if (not gc.getTeam(gc.getPlayer(con.iArabia).getTeam()).isHasTech(xml.iFarriers)):
				self.spawnUnits( iBarbarian, (94,0),(99,3), xml.iHorseArcher, 1, iGameTurn,11,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()))
			else:
				self.spawnUnits( iBarbarian, (94,0),(99,3), xml.iBedouin, 1, iGameTurn,10,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()))
		if (gc.getPlayer(con.iArabia).isHuman()): #extra barbs for human Arabia
			if (iGameTurn >= xml.i700AD and iGameTurn <= xml.i1300AD ):
				if (not gc.getTeam(gc.getPlayer(con.iArabia).getTeam()).isHasTech(xml.iFarriers)):
					self.spawnUnits( iBarbarian, (94,0),(99,3), xml.iHorseArcher, 1 + iHandicap, iGameTurn,11,3,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()))
					self.spawnUnits( iBarbarian, (92,1),(98,4), xml.iHorseArcher, 1, iGameTurn,8,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()))
				else:
					self.spawnUnits( iBarbarian, (94,0),(99,3), xml.iBedouin, 1 + iHandicap, iGameTurn,10,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()))
					self.spawnUnits( iBarbarian, (95,1),(98,5), xml.iBedouin, 1, iGameTurn,7,3,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()))

		#Banu Hilal and Bani Hassan, in Morocco and Tunesia
		if (iGameTurn >= xml.i1040AD and iGameTurn < xml.i1229AD):
			if (gc.getPlayer(con.iMorocco).isHuman()): #more barbs for human Morocco
				self.spawnUnits( iBarbarian, (40,10),(44,14), xml.iBedouin, 2 + iHandicap, iGameTurn,11,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL", ()))
				self.spawnUnits( iBarbarian, (44,1),(50,8), xml.iTouareg, 2 + iHandicap, iGameTurn,8,5,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL", ()))
			else:
				self.spawnUnits( iBarbarian, (40,10),(44,14), xml.iBedouin, 1, iGameTurn,11,2,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL", ()))
				self.spawnUnits( iBarbarian, (44,1),(50,8), xml.iTouareg, 1, iGameTurn,8,5,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL", ()))
		if (iGameTurn >= xml.i1640AD and iGameTurn < xml.i1680AD):
			self.spawnUnits( iBarbarian, (7,2),(10,10), xml.iBedouin, 5 + iHandicap*2, iGameTurn,3,1,utils.outerInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_BANI_HASSAN", ()))

		#Pre Mongols to keep Kiev busy
		if (iGameTurn >= xml.i900AD and iGameTurn < xml.i1020AD):
			self.spawnUnits( iBarbarian, (93,35),(99,44), xml.iHorseArcher, 1, iGameTurn,12,1,utils.outerInvasion,1, "")
		if (iGameTurn >= xml.i1020AD and iGameTurn < xml.i1236AD):
			self.spawnUnits( iBarbarian, (93,35),(99,44), xml.iHorseArcher, 1, iGameTurn,7,1,utils.outerInvasion,1, "")
		if (gc.getPlayer(con.iKiev).isHuman()): #extra barbs for human Kiev
			if (iGameTurn >= xml.i1020AD and iGameTurn < xml.i1236AD):
				self.spawnUnits( iBarbarian, (94,32),(97,39), xml.iHorseArcher, 2 + iHandicap, iGameTurn,10,1,utils.outerInvasion,1, "")

		#Barbs in Anatolia pre Seljuks (but after Sassanids)
		if (iGameTurn >= xml.i700AD and iGameTurn < xml.i1050AD ):
			self.spawnUnits( iBarbarian, (97,20),(99,26), xml.iHorseArcher, 1, iGameTurn,10,1,utils.outerInvasion,1, "")
			self.spawnUnits( iBarbarian, (95,20),(99,24), xml.iAxeman, 1, iGameTurn,14,2,utils.outerInvasion,1, "")
			self.spawnUnits( iBarbarian, (95,22),(97,26), xml.iSpearman, 1, iGameTurn,16,6,utils.outerInvasion,1, "")
		if (gc.getPlayer(con.iByzantium).isHuman()): #extra barbs for human Byzantium
			if (iGameTurn >= xml.i700AD and iGameTurn < xml.i1050AD ):
				self.spawnUnits( iBarbarian, (97,20),(99,26), xml.iHorseArcher, 1 + iHandicap, iGameTurn,10,1,utils.outerInvasion,1, "")
				self.spawnUnits( iBarbarian, (95,20),(99,24), xml.iAxeman, 1, iGameTurn,14,2,utils.outerInvasion,1, "")
				self.spawnUnits( iBarbarian, (95,20),(99,24), xml.iHorseArcher, 1 + iHandicap, iGameTurn,14,2,utils.outerInvasion,1, "")
				self.spawnUnits( iBarbarian, (95,22),(97,26), xml.iSpearman, 1, iGameTurn,16,6,utils.outerInvasion,1, "")
				self.spawnUnits( iBarbarian, (95,22),(97,26), xml.iHorseArcher, 1 + iHandicap, iGameTurn,16,6,utils.outerInvasion,1, "")

		#Seljuks
		if (iGameTurn >= xml.i1064AD and iGameTurn < xml.i1094AD):
			self.spawnUnits( iBarbarian, (90,21),(99,28), xml.iSeljukLancer, 3, iGameTurn,3,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (90,21),(99,28), xml.iTurcomanHorseArcher, 1, iGameTurn,3,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (90,21),(99,28), xml.iSeljukCrossbow, 1, iGameTurn,3,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (90,21),(99,28), xml.iSeljukSwordsman, 1, iGameTurn,3,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iSeljukLancer, 3, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iTurcomanHorseArcher, 1, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iSeljukGuisarme, 1, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iSeljukFootman, 1, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (95,8),(99,12), xml.iSeljukLancer, 2, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
			self.spawnUnits( iBarbarian, (95,8),(99,12), xml.iSeljukCrossbow, 1, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
		if (gc.getPlayer(con.iByzantium).isHuman()): #extra barbs for human Byzantium
			if (iGameTurn >= xml.i1064AD and iGameTurn < xml.i1094AD):
				self.spawnUnits( iBarbarian, (90,21),(99,28), xml.iSeljukLancer, 2, iGameTurn,3,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (90,21),(99,28), xml.iTurcomanHorseArcher, 1, iGameTurn,3,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (90,21),(99,28), xml.iSeljukCrossbow, 1 + iHandicap, iGameTurn,3,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (90,21),(99,28), xml.iSeljukGuisarme, 1, iGameTurn,3,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (90,21),(99,28), xml.iSeljukFootman, 2 + iHandicap, iGameTurn,3,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iSeljukLancer, 2, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iTurcomanHorseArcher, 1, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iSeljukGuisarme, 1 + iHandicap, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iSeljukCrossbow, 1, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (92,20),(99,25), xml.iSeljukSwordsman, 2 + iHandicap, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
		if (gc.getPlayer(con.iArabia).isHuman()): #extra barbs for human Arabia
			if (iGameTurn >= xml.i1064AD and iGameTurn < xml.i1094AD):
				self.spawnUnits( iBarbarian, (95,8),(99,12), xml.iSeljukLancer, 2 + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))
				self.spawnUnits( iBarbarian, (95,8),(99,12), xml.iSeljukCrossbow, 1, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()))

		#Danishmends
		if (iGameTurn >= xml.i1077AD and iGameTurn < xml.i1147AD):
			if (gc.getPlayer(con.iByzantium).isHuman()): #more barbs for human Byzantium
				self.spawnUnits( iBarbarian, (93,20),(99,22), xml.iTurcomanHorseArcher, 3 + iHandicap, iGameTurn,5,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_DANISHMENDS", ()))
			else:
				self.spawnUnits( iBarbarian, (93,20),(99,22), xml.iTurcomanHorseArcher, 2, iGameTurn,5,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_DANISHMENDS", ()))

		#Mongols
		if (iGameTurn >= xml.i1236AD and iGameTurn < xml.i1288AD):
			#Kiev
			if (gc.getPlayer(con.iKiev).isHuman()):
				self.spawnUnits( iBarbarian, (93,32),(99,42), xml.iMongolKeshik, 5 + iHandicap, iGameTurn,4,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
				self.spawnUnits( iBarbarian, (94,34),(99,45), xml.iMongolKeshik, 4 + iHandicap, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			else:
				self.spawnUnits( iBarbarian, (93,32),(99,42), xml.iMongolKeshik, 3, iGameTurn,4,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
				self.spawnUnits( iBarbarian, (94,34),(99,45), xml.iMongolKeshik, 2, iGameTurn,3,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			#Hungary
			if (gc.getPlayer(con.iHungary).isHuman()):
				self.spawnUnits( iBarbarian, (70,35),(76,45), xml.iMongolKeshik, 4 + iHandicap, iGameTurn,4,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			else:
				self.spawnUnits( iBarbarian, (70,35),(76,45), xml.iMongolKeshik, 2, iGameTurn,4,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			#Poland
			if (gc.getPlayer(con.iPoland).isHuman()):
				self.spawnUnits( iBarbarian, (72,40),(75,56), xml.iMongolKeshik, 4 + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			else:
				self.spawnUnits( iBarbarian, (72,40),(75,56), xml.iMongolKeshik, 2, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			#Bulgaria
			if (gc.getPlayer(con.iBulgaria).isHuman()):
				self.spawnUnits( iBarbarian, (78,32),(83,34), xml.iMongolKeshik, 3 + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			else:
				self.spawnUnits( iBarbarian, (78,32),(83,34), xml.iMongolKeshik, 2, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			#Moscow area
			self.spawnUnits( iBarbarian, (89,46),(95,54), xml.iMongolKeshik, 1, iGameTurn,4,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			self.spawnUnits( iBarbarian, (91,48),(97,53), xml.iMongolKeshik, 2, iGameTurn,6,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			#Middle East
			self.spawnUnits( iBarbarian, (94,20),(99,26), xml.iMongolKeshik, 2, iGameTurn,3,2,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))
			self.spawnUnits( iBarbarian, (92,21),(97,25), xml.iMongolKeshik, 2, iGameTurn,6,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()))

		#Timurids, Tamerlane's conquests (aka Mongols, the return!)
		if (iGameTurn >= xml.i1380AD and iGameTurn <= xml.i1431AD): #Timur started his first western campaigns in 1380AD
			#Eastern Europe
			self.spawnUnits( iBarbarian, (85,47),(99,57), xml.iMongolKeshik, 2, iGameTurn,7,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()))
			#Anatolia
			if (gc.getPlayer(con.iTurkey).isHuman()):
				self.spawnUnits( iBarbarian, (87,17),(96,24), xml.iMongolKeshik, 3 + iHandicap, iGameTurn,4,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()))
				self.spawnUnits( iBarbarian, (94,18),(99,26), xml.iMongolKeshik, 4 + iHandicap, iGameTurn,5,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()))
			else:
				self.spawnUnits( iBarbarian, (87,17),(96,24), xml.iMongolKeshik, 2, iGameTurn,4,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()))
				self.spawnUnits( iBarbarian, (94,18),(99,26), xml.iMongolKeshik, 3, iGameTurn,5,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()))
			#Arabia
			if (gc.getPlayer(con.iArabia).isHuman()):
				self.spawnUnits( iBarbarian, (96,9),(99,15), xml.iMongolKeshik, 3 + iHandicap, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()))
			else:
				self.spawnUnits( iBarbarian, (96,9),(99,15), xml.iMongolKeshik, 2, iGameTurn,4,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()))

		#Nogais
		if (iGameTurn >= xml.i1500AD and iGameTurn <= xml.i1600AD):
			self.spawnUnits( iBarbarian, (93,38),(99,54), xml.iHorseArcher, 3, iGameTurn,7,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_NOGAIS", ()))
			if (gc.getPlayer(con.iMoscow).isHuman()): #extra barbs for human Moscow
				self.spawnUnits( iBarbarian, (93,38),(99,54), xml.iHorseArcher, 2 + iHandicap, iGameTurn,7,1,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_NOGAIS", ()))

		#Kalmyks
		if (iGameTurn >= xml.i1600AD and iGameTurn <= xml.i1715AD):
			self.spawnUnits( iBarbarian, (93,38),(99,54), xml.iMongolKeshik, 3, iGameTurn,7,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KALMYKS", ()))
			if (gc.getPlayer(con.iMoscow).isHuman()): #extra barbs for human Moscow
				self.spawnUnits( iBarbarian, (93,38),(99,54), xml.iMongolKeshik, 3 + iHandicap, iGameTurn,7,0,utils.forcedInvasion,1, localText.getText("TXT_KEY_BARBARIAN_NAMES_KALMYKS", ()))


		# Independent/barb city spawns and minor nations:
		self.doIndependentCities(iGameTurn)

		if ( iGameTurn == 1 ):
			self.setupMinorNation()
		self.doMinorNations(iGameTurn)


	def doIndependentCities(self, iGameTurn):
		if iGameTurn in dIndependentCities.keys():
			for tCity in dIndependentCities[iGameTurn]:
				lVariations, iCiv, iPop, iUnit, iNumUnits, iReligion, iWorkers = tCity
				iChosenCity = -1
				iRand = gc.getGame().getSorenRandNum(100, 'random independent city')
				for iCity in range(len(lVariations)):
					if iRand < lVariations[iCity][2]:
						iChosenCity = iCity
						break
					iRand -= lVariations[iCity][2]
				if iChosenCity == -1:
					continue
				tCoords, sName, iPos = lVariations[iChosenCity]
				self.foundCity(iCiv, tCoords, sName, iPop, iUnit, iNumUnits, iReligion, iWorkers)
				print ("New indy city founded: ", sName)


	def foundCity(self, iCiv, tCoords, name, iPopulation, iUnitType, iNumUnits, iReligion, iWorkers):
		if self.checkRegion(tCoords):
			gc.getPlayer(iCiv).found(tCoords[0], tCoords[1])
			city = gc.getMap().plot(tCoords[0], tCoords[1]).getPlotCity()
			city.setName(name, False)
			if (iPopulation != 1):
				city.setPopulation(iPopulation)
			if (iNumUnits > 0):
				self.makeUnit(iUnitType, iCiv, tCoords, iNumUnits, 0, "")
			if ( iReligion > -1 ):
				city.setHasReligion(iReligion, True, True, False)
			if (iWorkers > 0):
				self.makeUnit(xml.iWorker, iCiv, tCoords, iWorkers, 0, "")


	def checkRegion(self, tCoords):
		cityPlot = gc.getMap().plot(tCoords[0], tCoords[1])

		#checks if the plot already belongs to someone
		if (cityPlot.isOwned()):
			if (cityPlot.getOwner() != iBarbarian ):
				return False
				
		#checks the surroundings and for cities
		for x in range(tCoords[0]-1, tCoords[0]+2):
			for y in range(tCoords[1]-1, tCoords[1]+2):
				currentPlot = gc.getMap().plot(x,y)
				if (currentPlot.isCity()):
					return False
		return True


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
		for x in range(tCoords[0]-1, tCoords[0]+2):	# from x-1 to x+1
			for y in range(tCoords[1]-1, tCoords[1]+2):	# from y-1 to y+1
				killPlot = CyMap().getPlot(x, y)
				for i in range(killPlot.getNumUnits()):
					unit = killPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
					unit.kill(False, iBarbarian)


	def onImprovementDestroyed(self,iX,iY):
		print ("Barb improvement destroyed")
		#getHandicapType: Viceroy=0, Monarch=1, Emperor=2)
		iHandicap = gc.getGame().getHandicapType()
		iTurn = gc.getGame().getGameTurn()
		if (iTurn > xml.i1500AD):
			iBarbUnit = xml.iMusketman
		elif (iTurn > xml.i1284AD):
			iBarbUnit = xml.iArquebusier
		elif (iTurn > xml.i840AD):
			iBarbUnit = xml.iHorseArcher
		else:
			iBarbUnit = xml.iSpearman
		self.spawnUnits(iBarbarian, (iX-1,iY-1),(iX+1,iY+1),iBarbUnit,1 + iHandicap,1,1,0,utils.outerInvasion,1,"")


	def setupMinorNation( self ):
		lNextMinorRevolt = self.getRevolDates()

		for lNation in lMinorNations:
			#iNextRevolt = lNation[3][0] -3 + gc.getGame().getSorenRandNum(6, 'roll to modify the Nations revolt odds')
			iNextRevolt = lNation[3][0]
			while iNextRevolt in lNextMinorRevolt:
				iNextRevolt = lNation[3][0] -3 + gc.getGame().getSorenRandNum(6, 'roll to modify the Nations revolt odds')
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
			lPlayersOwning = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
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


	def doRevoltAI( self, iPlayer, iGameTurn, lNation, iRevoltIndex ):
		cityList = []
		for iI in range( gc.getNumProvinceTiles( lNation[0] ) ):
			iX = gc.getProvinceX( lNation[0], iI )
			iY = gc.getProvinceY( lNation[0], iI )
			if ( gc.getMap().plot( iX, iY ).isCity() ):
				pCity = gc.getMap().plot( iX, iY ).getPlotCity()
				if ( pCity.getOwner() == iPlayer ):
					cityList.append(pCity)

		iNumGarrison = 0
		for iI in range( len( cityList ) ):
			iNumGarrison += self.getGarrasonSize( cityList[iI] )

		# base rebellion odds: maximum 45%
		# odds considering minor nation strength - between 10 and 40
		iSuppressOdds = - lNation[4][iRevoltIndex]
		# stability odds: maximum 20 + lNation[4][iRevoltIndex]
		pPlayer = gc.getPlayer( iPlayer )
		iSuppressOdds += 20 + max( -10, min( pPlayer.getStability() * 2, lNation[4][iRevoltIndex] ) )
		# passive bonus from city garrison: maximum 15
		iSuppressOdds += min( (3 * iNumGarrison) / len( cityList ), 15 )
		# AI bonus
		iSuppressOdds += 10

		# AI always cracks revolt: maximum 35%
		# with a crackdown you will get a turn of unrest and some unhappiness even if it succeeds.
		iSuppressOdds = 10
		iSuppressOdds += min( (5 * iNumGarrison) / len( cityList ), 25 )

		# time to roll the dice
		if ( iSuppressOdds > gc.getGame().getSorenRandNum(100, 'minor nation revolt') ):
			# revolt suppressed
			for iI in range( len( cityList ) ):
				pCity = cityList[iI]
				pCity.changeHurryAngerTimer( 10 )
				pCity.changeOccupationTimer( 1 )
				self.makeRebels( pCity, lNation[5][iRevoltIndex], lNation[6][iRevoltIndex], lNation[7][1] )
		else:
			# revolt succeeded
			iRndNum = gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random independent')
			iNewCiv = con.iIndepStart + iRndNum
			for iI in range( len( cityList ) ):
				pCity = cityList[iI]
				utils.cultureManager((pCity.getX(),pCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
				utils.flipUnitsInCitySecession((pCity.getX(),pCity.getY()), iNewCiv, iPlayer)
				self.setTempFlippingCity((pCity.getX(),pCity.getY()))
				utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iNewCiv, [iPlayer]) #by trade because by conquest may raze the city
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
		#print("Event Apply",iNationIndex, iRevoltIndex, iDecision )
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

		iNumGarrison = 0
		iBribeGold = 0
		for iI in range( len( cityList ) ):
			iNumGarrison += self.getGarrasonSize( cityList[iI] )
			iBribeGold += 10 * cityList[iI].getPopulation()

		# raw suppress score
		iSuppressOdds = - lNation[4][iRevoltIndex]
		pPlayer = gc.getPlayer( iPlayer )
		iSuppressOdds += 20 + max( -10, min( pPlayer.getStability() * 2, lNation[4][iRevoltIndex] ) )
		iSuppressOdds += min( (3 * iNumGarrison) / len( cityList ), 15 )

		# 2nd or 4th choice
		if ( iDecision == 1 or iDecision == 3 ):
			iSuppressOdds += 10 + min( (5 * iNumGarrison) / len( cityList ), 25 )

		# 3rd or 4th choice
		if ( iDecision == 2 or iDecision == 3 ):
			iGovernment = pPlayer.getCivics(0)
			if ( iGovernment == xml.iCivicDespotism ):
				iBribeOdds = 15
			elif ( iGovernment == xml.iCivicFeudalMonarchy ):
				iBribeOdds = 25
			elif ( iGovernment == xml.iCivicDivineMonarchy ):
				iBribeOdds = 30
			elif ( iGovernment == xml.iCivicLimitedMonarchy ):
				iBribeOdds = 25
			elif ( iGovernment == xml.iCivicMerchantRepublic ):
				iBribeOdds = 20
			iGold = pPlayer.getGold()
			if ( iGold < iBribeGold ):
				iBribeOdds = ( iBribeOdds * iGold ) / ( iBribeGold )
			pPlayer.setGold( iGold - min( iGold, iBribeGold ) )
			iSuppressOdds += iBribeOdds

		if ( iSuppressOdds > gc.getGame().getSorenRandNum(100, 'minor nation revolt') ):
			# revolt suppressed
			for iI in range( len( cityList ) ):
				pCity = cityList[iI]
				CyInterface().addMessage(iPlayer, True, con.iDuration, CyTranslator().getText("TXT_KEY_MINOR_NATION_REVOLT_SUPRESSED", (pCity.getName(),)), "", 0, "", ColorTypes(con.iBlue), -1, -1, True, True)
				# cracking the rebels results in unhappiness in the general population:
				if ( iDecision == 1 or iDecision == 3 ):
					pCity.changeHurryAngerTimer( 10 )
					pCity.changeOccupationTimer( 1 )
				# bribing their lords away from their cause angers the rebel militia further:
				if ( iDecision == 2 or iDecision == 3 ):
					self.makeRebels( pCity, lNation[5][iRevoltIndex], 1 + lNation[6][iRevoltIndex], lNation[7][1] )
				else:
					self.makeRebels( pCity, lNation[5][iRevoltIndex], lNation[6][iRevoltIndex], lNation[7][1] )
		else:
			# revolt succeeded
			iRndNum = gc.getGame().getSorenRandNum( con.iIndepEnd - con.iIndepStart + 1, 'random independent')
			iNewCiv = con.iIndepStart + iRndNum
			for iI in range( len( cityList ) ):
				pCity = cityList[iI]
				sNationName = localText.getText(lNation[7][1], ())
				CyInterface().addMessage(iPlayer, True, con.iDuration, CyTranslator().getText("TXT_KEY_MINOR_NATION_REVOLT_SUCCEEDED", (sNationName, pCity.getName(),)), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
				utils.cultureManager((pCity.getX(),pCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
				utils.flipUnitsInCitySecession((pCity.getX(),pCity.getY()), iNewCiv, iPlayer)
				self.setTempFlippingCity((pCity.getX(),pCity.getY()))
				utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iNewCiv, [iPlayer]) #by trade because by conquest may raze the city
				utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)


	# Absinthe: revolution choice effects:
			# base chance: stability bonus adjusted with the revolt strength + base chance + passive military presence - revolt strength
			# suppress with force: + base chance + military strength in the city. revolt +1 turn, unhappy +1 for 10 turns
			# bribe the lords: + financial chance: costs 10 gold per population, suppression depends on the government Divine Monarchy (30%), Feudal or Limited (25%), Merchant (20%), Decentral (15%)
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

		iNumGarrison = 0
		iBribeGold = 0
		for iI in range( len( cityList ) ):
			iNumGarrison += self.getGarrasonSize( cityList[iI] )
			iBribeGold += 10 * cityList[iI].getPopulation()

		# base rebellion odds: maximum 35%
		# odds considering minor nation strength - usually 10, 20, 30, or 40
		iRawOdds = - lNation[4][iRevoltIndex]
		# stability odds: maximum 20 + lNation[4][iRevoltIndex]
		pPlayer = gc.getPlayer( iPlayer )
		iRawOdds += 20 + max( -10, min( pPlayer.getStability() * 2, lNation[4][iRevoltIndex] ) )
		# passive bonus from city garrison: maximum 15
		iRawOdds += min( (3 * iNumGarrison) / len( cityList ), 15 )

		# odds adjusted by a crackdown: maximum 35%
		# with a crackdown you will get a turn of unrest and some unhappiness even if it succeeds.
		iCrackOdds = 10
		iCrackOdds += min( (5 * iNumGarrison) / len( cityList ), 25 )

		# odds adjusted by bribery: maximum 30%
		# bribe the lords, cost 10 gold per population
		# suppression depends on the government Divine Monarchy (30%), Feudal or Limited (25%), Merchant (20%), Decentral (15%)
		iGovernment = pPlayer.getCivics(0)
		if ( iGovernment == xml.iCivicDespotism ):
			iBribeOdds = 15
		elif ( iGovernment == xml.iCivicFeudalMonarchy ):
			iBribeOdds = 25
		elif ( iGovernment == xml.iCivicDivineMonarchy ):
			iBribeOdds = 30
		elif ( iGovernment == xml.iCivicLimitedMonarchy ):
			iBribeOdds = 25
		elif ( iGovernment == xml.iCivicMerchantRepublic ):
			iBribeOdds = 20
		iGold = pPlayer.getGold()
		if ( iGold < iBribeGold ):
			iBribeOdds = ( iBribeOdds * iGold ) / ( iBribeGold )
		iGold = min( iGold, iBribeGold )

		# values should be between 0 and 100
		iAllOdds = max (0, iRawOdds + iBribeOdds + iCrackOdds)
		iBribeOdds = max (0, iRawOdds + iBribeOdds)
		iCrackOdds = max (0, iRawOdds + iCrackOdds)
		iRawOdds = max (0, iRawOdds)

		szRebellName = localText.getText(lNation[7][0], ())
		self.showPopup(7627, localText.getText("TXT_KEY_MINOR_REBELLION_TITLE", (szRebellName,) ), \
				localText.getText("TXT_KEY_MINOR_REBELLION_DESC", (szRebellName,) ), \
				(localText.getText("TXT_KEY_MINOR_REBELLION_DO_NOTHING", ( iRawOdds, )), \
				 localText.getText("TXT_KEY_MINOR_REBELLION_CRACK", ( iCrackOdds, )), \
				 localText.getText("TXT_KEY_MINOR_REBELLION_BRIBE", (iGold, iBribeGold, iBribeOdds, )), \
				 localText.getText("TXT_KEY_MINOR_REBELLION_ALL", ( iAllOdds, )), ))


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

