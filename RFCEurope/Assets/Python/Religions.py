# Rhye's and Fall of Civilization - Religions management

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import Consts as con
import XMLConsts as xml
import RFCUtils
import RFCEMaps as rfcemaps
from StoredData import sd

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()

### Constants ###

iNumPlayers = con.iNumPlayers
iNumTotalPlayers = con.iNumTotalPlayers
iBarbarian = con.iBarbarian
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2

# initialise religion variables to religion indices from XML

# initialise coordinates

tToledo = (30,27)
tAugsburg = (55,41)
tSpainTL = (25,20)
tSpainBR = (38,34)
tMainzTL = (49,41)
tMainzBR = (55,52)
tPolandTL = (64,43)
tPolandBR = (75,54)

### Religious Buildings that give Faith Points ###
tCatholicBuildings = [ xml.iCatholicTemple, xml.iCatholicMonastery, xml.iCatholicCathedral ]
tOrthodoxBuildings = [ xml.iOrthodoxTemple, xml.iOrthodoxMonastery, xml.iOrthodoxCathedral ]
tProtestantBuildings = [ xml.iProtestantTemple, xml.iProtestantSchool, xml.iProtestantCathedral ]
tIslamicBuildings = [ xml.iIslamicTemple, xml.iIslamicCathedral, xml.iIslamicMadrassa ]
tReligiousWonders = [ xml.iMonasteryOfCluny, xml.iImperialDiet, xml.iKrakDesChevaliers, xml.iNotreDame, xml.iPalaisPapes, xml.iStBasil, xml.iSophiaKiev, xml.iDomeRock, xml.iRoundChurch, xml.iWestminster ]


### Reformation Begin ###
#Matrix determines how likely the AI is to switch to Protestantism
lReformationMatrix = [
20, #Byzantium
40, #France
40, #Arabia
20, #Bulgaria
40, #Cordoba
30, #Venice
50, #Burgundy
90, #Germany
30, #Novgorod
80, #Norway
30, #Kiev
50, #Hungary
10, #Spain
80, #Denmark
80, #Scotland
30, #Poland
20, #Genoa
40, #Morocco
80, #England
20, #Portugal
30, #Aragon
90, #Sweden
90, #Prussia
30, #Lithuania
20, #Austria
40, #Turkey
30, #Moscow
90, #Dutch
0,  #Rome
40,  #Indies and Barbs
40,
40,
40,
40
]

#Reformation neighbours spread reformation choice to each other
lReformationNeighbours = [
[con.iArabia,con.iBulgaria,con.iTurkey], #Byzantium
[con.iBurgundy,con.iSpain,con.iGermany,con.iGenoa,con.iEngland,con.iDutch,con.iScotland], #France
[con.iByzantium,con.iCordoba,con.iTurkey], #Arabia
[con.iByzantium,con.iKiev,con.iHungary,con.iTurkey], #Bulgaria
[con.iArabia,con.iSpain,con.iPortugal,con.iAragon,con.iMorocco], #Cordoba
[con.iGenoa,con.iGermany,con.iAustria,con.iHungary,con.iPope], #Venice
[con.iFrankia,con.iGermany,con.iGenoa,con.iDutch], #Burgundy
[con.iBurgundy,con.iFrankia,con.iDenmark,con.iVenecia,con.iHungary,con.iPoland,con.iGenoa,con.iAustria,con.iDutch], #Germany
[con.iSweden,con.iHungary,con.iPoland,con.iMoscow,con.iLithuania,con.iKiev], #Novgorod
[con.iDenmark,con.iSweden], #Norway
[con.iBulgaria,con.iHungary,con.iPoland,con.iMoscow,con.iLithuania,con.iNovgorod], #Kiev
[con.iBulgaria,con.iVenecia,con.iKiev,con.iGermany,con.iPoland,con.iAustria,con.iTurkey], #Hungary
[con.iFrankia,con.iCordoba,con.iPortugal,con.iAragon], #Spain
[con.iNorway,con.iSweden,con.iGermany], #Denmark
[con.iFrankia,con.iDutch,con.iEngland], #Scotland
[con.iKiev,con.iHungary,con.iGermany,con.iMoscow,con.iAustria,con.iLithuania], #Poland
[con.iBurgundy,con.iFrankia,con.iVenecia,con.iGermany,con.iPope,con.iAragon], #Genoa
[con.iArabia,con.iSpain,con.iPortugal,con.iAragon,con.iCordoba], #Morocco
[con.iFrankia,con.iDutch,con.iScotland], #England
[con.iSpain,con.iCordoba,con.iAragon], #Portugal
[con.iSpain,con.iCordoba,con.iPortugal,con.iFrankia,con.iGenoa], #Aragon
[con.iNorway,con.iDenmark,con.iMoscow,con.iNovgorod], #Sweden
[con.iGermany,con.iLithuania,con.iMoscow,con.iAustria,con.iPoland], #Prussia
[con.iKiev,con.iMoscow,con.iPrussia,con.iNovgorod,con.iPoland], #Lithuania
[con.iVenecia,con.iHungary,con.iGermany,con.iPoland], #Austria
[con.iByzantium,con.iArabia,con.iBulgaria,con.iHungary], #Turkey
[con.iKiev,con.iPoland,con.iSweden,con.iLithuania,con.iNovgorod], #Moscow
[con.iBurgundy,con.iFrankia,con.iGermany,con.iEngland,con.iScotland], #Dutch
[con.iVenecia,con.iGenoa] #Pope
]
### Reformation End ###


### Regions to spread religion ###
tProvinceMap = rfcemaps.tProinceMap
tSpain = [xml.iP_Leon,xml.iP_GaliciaSpain,xml.iP_Aragon,xml.iP_Catalonia,xml.iP_Castile,xml.iP_LaMancha,xml.iP_Andalusia,xml.iP_Valencia]
tPoland = [xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Masovia,xml.iP_Silesia,xml.iP_Suvalkija,xml.iP_Brest,xml.iP_Pomerania,xml.iP_GaliciaPoland]
tGermany = [xml.iP_Lorraine,xml.iP_Franconia,xml.iP_Bavaria,xml.iP_Swabia]
tWestAfrica = [xml.iP_Tetouan,xml.iP_Morocco,xml.iP_Marrakesh,xml.iP_Fez,xml.iP_Oran]
tNorthAfrica = [xml.iP_Algiers,xml.iP_Ifriqiya,xml.iP_Tripolitania,xml.iP_Cyrenaica]
tBalkansAndAnatolia = [xml.iP_Constantinople,xml.iP_Thrace,xml.iP_Opsikion,xml.iP_Paphlagonia,xml.iP_Thrakesion,xml.iP_Cilicia,xml.iP_Anatolikon,xml.iP_Armeniakon,xml.iP_Charsianon]
tCentralEurope = [xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Masovia,xml.iP_GaliciaPoland,xml.iP_Brest,xml.iP_Suvalkija,xml.iP_Lithuania,xml.iP_Prussia,xml.iP_Pomerania,xml.iP_Saxony,xml.iP_Brandenburg,xml.iP_Holstein,xml.iP_Denmark,xml.iP_Bavaria,xml.iP_Swabia,xml.iP_Bohemia,xml.iP_Moravia,xml.iP_Silesia,xml.iP_Hungary,xml.iP_Transylvania,xml.iP_UpperHungary,xml.iP_Pannonia,xml.iP_Slavonia,xml.iP_Carinthia,xml.iP_Austria]
tMaghrebAndalusia = [xml.iP_Tetouan,xml.iP_Morocco,xml.iP_Marrakesh,xml.iP_Fez,xml.iP_Oran,xml.iP_Algiers,xml.iP_Ifriqiya,xml.iP_Tripolitania,xml.iP_Cyrenaica,xml.iP_LaMancha,xml.iP_Andalusia,xml.iP_Valencia]
tBulgariaBalkans = [xml.iP_Moesia,xml.iP_Macedonia,xml.iP_Serbia,xml.iP_Wallachia]
tOldRus = [xml.iP_Novgorod,xml.iP_Rostov,xml.iP_Polotsk,xml.iP_Smolensk,xml.iP_Minsk,xml.iP_Chernigov,xml.iP_Kiev,xml.iP_Pereyaslavl,xml.iP_Sloboda]
tSouthScandinavia = [xml.iP_Denmark,xml.iP_Gotaland,xml.iP_Skaneland,xml.iP_Vestfold,xml.iP_Norway]
tHungary = [xml.iP_Hungary,xml.iP_Transylvania,xml.iP_UpperHungary,xml.iP_Pannonia]

class Religions:

##################################################
### Secure storage & retrieval of script data ###
################################################

	def getSeed( self ):
		return sd.scriptDict['iSeed']

	def setSeed( self ):
		sd.scriptDict['iSeed'] = gc.getGame().getSorenRandNum(100, 'Seed for random delay')

	def getReformationActive( self ):
		return sd.scriptDict['bReformationActive']

	def setReformationActive( self, bNewValue ):
		sd.scriptDict['bReformationActive'] = bNewValue

	def getReformationHitMatrix( self, iCiv ):
		return sd.scriptDict['lReformationHitMatrix'][iCiv]

	def setReformationHitMatrix( self, iCiv, bNewValue ):
		sd.scriptDict['lReformationHitMatrix'][iCiv] = bNewValue

	def getReformationHitMatrixAll( self ):
		return sd.scriptDict['lReformationHitMatrix']

	def getCounterReformationActive( self ):
		return sd.scriptDict['bCounterReformationActive']

	def setCounterReformationActive( self, bNewValue ):
		sd.scriptDict['bCounterReformationActive'] = bNewValue


#######################################
### Main methods (Event-Triggered) ###
#####################################

	def setup(self):
		gc.getPlayer(con.iTurkey).changeFaith( 20 )
		self.setSeed()

	def checkTurn(self, iGameTurn):
		# Absinthe: Spreading religion in a couple preset dates
		if (iGameTurn == xml.i700AD-2):
			# Spread Judaism to Toledo
			self.spreadReligion(tToledo,xml.iJudaism)
			# Spread Islam to a random city in Africa
			tCity = self.selectRandomCityArea(tNorthAfrica)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iIslam)
		elif (iGameTurn == xml.i700AD+2):
			# Spread Judaism and Islam to a random city in Africa
			tCity = self.selectRandomCityArea(tWestAfrica)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iIslam)
			tCity = self.selectRandomCityArea(tWestAfrica)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iJudaism)
		elif (iGameTurn == xml.i900AD):
			# Spread Judaism to another city in Spain
			tCity = self.selectRandomCityArea(tSpain)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iJudaism)
		elif (iGameTurn == xml.i1000AD):
			# Spread Judaism to a city in France/Germany
			tCity = self.selectRandomCityArea(tGermany)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iJudaism)
			# Spread Islam to another city in Africa
			tCity = self.selectRandomCityArea(tNorthAfrica)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iIslam)
		elif (iGameTurn == xml.i1101AD):
			# Spread Judaism to a couple towns in Poland
			tCity = self.selectRandomCityArea(tPoland)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iJudaism)
		elif (iGameTurn == xml.i1200AD):
			# Spread Judaism to a couple towns in Poland
			tCity = self.selectRandomCityArea(tPoland)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iJudaism)
		elif (iGameTurn > xml.i1299AD and iGameTurn < xml.i1350AD and iGameTurn % 3 == 0):
			# Spread Islam to a couple cities in Anatolia before the Ottoman spawn
			tCity = self.selectRandomCityArea(tBalkansAndAnatolia)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iIslam)
		elif (iGameTurn == xml.i1401AD):
			# Spread Judaism to a couple towns in Poland
			tCity = self.selectRandomCityArea(tPoland)
			if (tCity != 0):
				self.spreadReligion(tCity,xml.iJudaism)

		# Absinthe: Spreading Judaism in random dates
		# General 6% chance to spread Jews to a random city in every third turn
		if (iGameTurn > xml.i800AD and iGameTurn < xml.i1700AD and iGameTurn % 3 == 0):
			if ( gc.getGame().getSorenRandNum(100, 'Spread Jews') < 6 ):
				tCity = self.selectRandomCityAll()
				if (tCity != 0):
					self.spreadReligion(tCity,xml.iJudaism)
		# Additional 11% chance to spread Jews to a random Central European city in every third turn
		if (iGameTurn > xml.i1000AD and iGameTurn < xml.i1500AD and iGameTurn % 3 == 1):
			if ( gc.getGame().getSorenRandNum(100, 'Spread Jews') < 11 ):
				tCity = self.selectRandomCityArea(tCentralEurope)
				if (tCity != 0):
					self.spreadReligion(tCity,xml.iJudaism)

		# Absinthe: Encouraging desired religion spread in a couple areas (mostly for Islam and Orthodoxy)
		# Maghreb and Cordoba:
		if (iGameTurn > xml.i700AD and iGameTurn < xml.i1200AD and iGameTurn % 3 == 2):
			if ( gc.getGame().getSorenRandNum(100, 'Spread chance') < 22 ):
				tCity = self.selectRandomCityAreaNoReligion(tMaghrebAndalusia)
				if (tCity != 0):
					self.spreadReligion(tCity,xml.iIslam)
		# Bulgaria and Balkans:
		if (iGameTurn > xml.i700AD and iGameTurn < xml.i800AD and iGameTurn % 3 == 1):
			if ( gc.getGame().getSorenRandNum(100, 'Spread chance') < 25 ):
				tCity = self.selectRandomCityAreaNoReligion(tBulgariaBalkans)
				if (tCity != 0):
					self.spreadReligion(tCity,xml.iOrthodoxy)
		if (iGameTurn > xml.i800AD and iGameTurn < xml.i1000AD and iGameTurn % 4 == 1):
			if ( gc.getGame().getSorenRandNum(100, 'Spread chance') < 15 ):
				tCity = self.selectRandomCityAreaNoReligion(tBulgariaBalkans)
				if (tCity != 0):
					self.spreadReligion(tCity,xml.iOrthodoxy)
		# Old Rus territories:
		if (iGameTurn > xml.i852AD and iGameTurn < xml.i1300AD and iGameTurn % 4 == 3):
			if ( gc.getGame().getSorenRandNum(100, 'Spread chance') < 25 ):
				tCity = self.selectRandomCityAreaNoReligion(tOldRus)
				if (tCity != 0):
					self.spreadReligion(tCity,xml.iOrthodoxy)
		# Extra chance for early Orthodoxy spread in Novgorod:
		if (iGameTurn > xml.i852AD and iGameTurn < xml.i1000AD and iGameTurn % 5 == 2):
			if ( gc.getGame().getSorenRandNum(100, 'Spread chance') < 20 ):
				tCity = self.selectRandomCityAreaNoReligion([xml.iP_Novgorod, xml.iP_Polotsk, xml.iP_Smolensk])
				if (tCity != 0):
					self.spreadReligion(tCity,xml.iOrthodoxy)
		# Hungary:
		if (iGameTurn > xml.i960AD and iGameTurn < xml.i1200AD and iGameTurn % 4 == 2):
			if ( gc.getGame().getSorenRandNum(100, 'Spread chance') < 18 ):
				tCity = self.selectRandomCityAreaNoReligion(tHungary)
				if (tCity != 0):
					self.spreadReligion(tCity,xml.iCatholicism)
		# Scandinavia:
		if (iGameTurn > xml.i1000AD and iGameTurn < xml.i1300AD and iGameTurn % 4 == 0):
			if ( gc.getGame().getSorenRandNum(100, 'Spread chance') < 22 ):
				tCity = self.selectRandomCityAreaNoReligion(tSouthScandinavia)
				if (tCity != 0):
					self.spreadReligion(tCity,xml.iCatholicism)

		# Absinthe: Persecution cooldown
		for i in range( con.iNumPlayers ):
			pPlayer = gc.getPlayer( i )
			if ( pPlayer.getProsecutionCount() > 0 ):
				pPlayer.changeProsecutionCount( -1 )

		# Absinthe: Resettle Jewish refugees
		iRefugies = gc.getMinorReligionRefugies()
		for i in range(iRefugies):
			self.resettleRefugies()
		gc.setMinorReligionRefugies( 0 )

		# Absinthe: Benefits for Catholics from the Pope
		# Gold gifts
		if ( iGameTurn > xml.i1648AD ): # End of religious wars
			iDivBy = 14
		elif ( iGameTurn > xml.i1517AD ): # Protestantism
			iDivBy = 11
		elif ( iGameTurn > xml.i1053AD ): # Schism
			iDivBy = 6
		else:
			iDivBy = 9
		if ( iGameTurn >= xml.i752AD and iGameTurn % iDivBy == 3 ):
			pPope = gc.getPlayer( con.iPope )
			teamPope = gc.getTeam( pPope.getTeam() )
			if ( pPope.getGold() > 100 ):
				iCatholicFaith = 0
				for i in range( iNumPlayers - 1 ): # The Pope cannot add any gifts to himself
					pPlayer = gc.getPlayer( i )
					if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
						# Relations with the Pope are much more important here
						iCatholicFaith += pPlayer.getFaith()
						iCatholicFaith += 8 * max( 0, pPope.AI_getAttitude( i ) )
				if ( iCatholicFaith > 0 ):
					iCatholicFaith += iCatholicFaith / 10 + 1 # So there is around 10% chance for not giving anything
					if ( iGameTurn < 100 ):
						iGift = 20
					else:
						iGift = 50
					iRandomNum = gc.getGame().getSorenRandNum(iCatholicFaith, 'random Pope gold gift')
					for i in range( iNumPlayers - 1 ):
						pPlayer = gc.getPlayer( i )
						if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
							iRandomNum -= pPlayer.getFaith()
							iRandomNum -= 8 * max( 0, pPope.AI_getAttitude( i ) )
							if ( iRandomNum <= 0 ): # The given civ is chosen
								pPope.changeGold( -iGift )
								pPlayer.changeGold( iGift )
								if ( utils.getHumanID() == i ):
									sText = CyTranslator().getText("TXT_KEY_FAITH_GIFT", ())
									CyInterface().addMessage(i, False, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iBlue), -1, -1, True, True)
								break
		# Free religious building
		if ( iGameTurn > xml.i1648AD ): # End of religious wars
			iDivBy = 21
		elif ( iGameTurn > xml.i1517AD ): # Protestantism
			iDivBy = 14
		elif ( iGameTurn > xml.i1053AD ): # Schism
			iDivBy = 8
		else:
			iDivBy = 11
		if ( iGameTurn > xml.i800AD ): # The crowning of Charlemagne
			if ( iGameTurn % iDivBy == 2 ):
				pPope = gc.getPlayer( con.iPope )
				teamPope = gc.getTeam( pPope.getTeam() )
				iCatholicFaith = 0
				iJerusalemOwner = gc.getMap().plot( con.tJerusalem[0], con.tJerusalem[1]).getPlotCity().getOwner()
				for i in range( iNumPlayers - 1 ): # The Pope cannot add any gifts to himself
					pPlayer = gc.getPlayer( i )
					if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
						# Faith points are the deciding factor for buildings
						iCatholicFaith += pPlayer.getFaith()
						iCatholicFaith += 2 * max( 0, pPope.AI_getAttitude( i ) )
						if ( i == iJerusalemOwner ): # The Catholic owner of Jerusalem has a greatly improved chance
							iCatholicFaith += 30
				if ( iCatholicFaith > 0 ):
					iCatholicFaith += iCatholicFaith / 5 + 1 # So there is around 20% chance for not giving anything
					iRandomNum = gc.getGame().getSorenRandNum(iCatholicFaith, 'random Pope Building Build')
					for i in range( iNumPlayers - 1 ):
						pPlayer = gc.getPlayer( i )
						if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
							iRandomNum -= pPlayer.getFaith()
							iRandomNum -= 2 * max( 0, pPope.AI_getAttitude( i ) )
							if ( i == iJerusalemOwner ):
								iCatholicFaith -= 30
							if ( iRandomNum <= 0 ): # The given civ is chosen
								# No chance for monastery if the selected player knows the Scientific Method tech (which obsoletes monasteries)
								teamPlayer = gc.getTeam(pPlayer.getTeam())
								if (teamPlayer.isHasTech(xml.iScientificMethod)):
									iCatholicBuilding = xml.iCatholicTemple
								else: # 50-50% chance for temple and monastery otherwise
									if ( gc.getGame().getSorenRandNum(100, 'random Catholic BuildingType') % 2 == 0 ):
										iCatholicBuilding = xml.iCatholicTemple
									else:
										iCatholicBuilding = xml.iCatholicMonastery
								self.buildInRandomCity( i, iCatholicBuilding, xml.iCatholicism )
								break

		##Reformation code
		if ( self.getCounterReformationActive() ):
			self.doCounterReformation()
		if (self.getReformationActive() ):
			#print( " Reformation #1 " )
			self.reformationArrayChoice()
			if (self.getReformationActive() ):
				#print( " Reformation #2 " )
				self.reformationArrayChoice()
				if (self.getReformationActive() ):
					#print( " Reformation #3 " )
					self.reformationArrayChoice()


	def foundReligion(self, tPlot, iReligion):
		if (tPlot != False):
			plot = gc.getMap().plot( tPlot[0], tPlot[1] )
			if (not plot.getPlotCity().isNone()):
				#if (gc.getPlayer(city.getOwner()).isHuman() == 0):
				#if (not gc.getGame().isReligionFounded(iReligion)):
				gc.getGame().setHolyCity(iReligion, plot.getPlotCity(), True)
				return True
			else:
				return False

		return False

	def onReligionSpread(self, iReligion, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		if ( pPlayer.getStateReligion() == iReligion ):
			pPlayer.changeFaith( 1 )
		else:
			pPlayer.changeFaith( -1 )

	def onBuildingBuild(seld, iPlayer, iBuilding ):
		pPlayer = gc.getPlayer( iPlayer )
		iStateReligion = pPlayer.getStateReligion()
		if ( iStateReligion == xml.iCatholicism and ( iBuilding in tCatholicBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iCatholicCathedral ):
				pPlayer.changeFaith( 3 )
		elif ( iStateReligion == xml.iOrthodoxy and ( iBuilding in tOrthodoxBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iOrthodoxCathedral ):
				pPlayer.changeFaith( 3 )
		elif ( iStateReligion == xml.iIslam and ( iBuilding in tIslamicBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iIslamicCathedral ):
				pPlayer.changeFaith( 3 )
		elif ( iStateReligion == xml.iProtestantism and ( iBuilding in tProtestantBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iProtestantCathedral ):
				pPlayer.changeFaith( 3 )
		if ( iBuilding in tReligiousWonders ):
			pPlayer.changeFaith( 6 )
		if ( iStateReligion != xml.iJudaism and iBuilding == xml.iKazimierz ):
			pPlayer.changeFaith( - min( 1, pPlayer.getFaith() ) )
			# Kazimierz tries to spread Judaism to a couple new cities
			apCityList = PyPlayer(iPlayer).getCityList()
			iJewCityNum = max ((len(apCityList) + 2) / 3 + 1, 3) # number of tries are based on number of cities, but at least 3
			for i in range(iJewCityNum):
				pCity = apCityList[gc.getGame().getSorenRandNum(len(apCityList), 'random city for jews')].GetCy()
				if (not pCity.isHasReligion(xml.iJudaism)):
					pCity.setHasReligion(xml.iJudaism, True, True, False)
			# Adds Jewish Quarter to all cities which already has Judaism (including the ones where it just spread)
			for i in range(len(apCityList)):
				pCity = apCityList[i].GetCy()
				if (pCity.isHasReligion(xml.iJudaism) and not pCity.hasBuilding(xml.iJewishQuarter)):
					pCity.setHasRealBuilding(xml.iJewishQuarter, True)


	def selectRandomCityAll(self):
		cityList = []
		for x in range( con.iMapMaxX ):
			for y in range( con.iMapMaxY ):
				pCurrent = gc.getMap().plot( x, y )
				if ( pCurrent.isCity()):
					cityList.append(pCurrent.getPlotCity())
		if (len(cityList) >= 1):
			iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iCity]
			return (city.getX(), city.getY())
		else:
			return 0

	def selectRandomCityCiv(self, iCiv):
		if (gc.getPlayer(iCiv).isAlive()):
			cityList = []
			for pyCity in PyPlayer(iCiv).getCityList():
				cityList.append(pyCity.GetCy())
			iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iCity]
			return (city.getX(), city.getY())
		return 0

	def selectRandomCityArea(self, tProvinces):
		cityList = []
		for x in range( con.iMapMaxX ):
			for y in range( con.iMapMaxY ):
				if ( tProvinceMap[y][x] in tProvinces ):
					pCurrent = gc.getMap().plot( x, y )
					if ( pCurrent.isCity()):
						cityList.append(pCurrent.getPlotCity())
		if (len(cityList) >= 1):
			iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iCity]
			return (city.getX(), city.getY())
		else:
			return 0

	def selectRandomCityAreaNoReligion(self, tProvinces):
		cityList = []
		for x in range( con.iMapMaxX ):
			for y in range( con.iMapMaxY ):
				if ( tProvinceMap[y][x] in tProvinces ):
					pCurrent = gc.getMap().plot( x, y )
					if ( pCurrent.isCity()):
						bNoReligion = True
						PlotCity = pCurrent.getPlotCity()
						# Check if there is a religion already present in the city
						for iReligion in range( xml.iNumReligions ):
							if (PlotCity.isHasReligion(iReligion)):
								bNoReligion = False
								break
						if bNoReligion:
							cityList.append(pCurrent.getPlotCity())
		if (len(cityList) >= 1):
			iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iCity]
			return (city.getX(), city.getY())
		else:
			return 0

	def selectRandomCityAreaCiv(self, tTopLeft, tBottomRight, iCiv):
		cityList = []
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				pCurrent = gc.getMap().plot( x, y )
				if ( pCurrent.isCity()):
					if (pCurrent.getPlotCity().getOwner() == iCiv):
						cityList.append(pCurrent.getPlotCity())
		if (cityList):
			iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iCity]
			return (city.getX(), city.getY())
		else:
			return 0

	def selectRandomCityReligion(self, iReligion):
		if (gc.getGame().isReligionFounded(iReligion)):
			cityList = []
			for iPlayer in range(iNumPlayers):
				for pyCity in PyPlayer(iPlayer).getCityList():
					if pyCity.GetCy().isHasReligion(iReligion):
						cityList.append(pyCity.GetCy())
			iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iCity]
			return (city.getX(), city.getY())
		return 0

	def selectRandomCityReligionCiv(self, iReligion, iCiv):
		if (gc.getGame().isReligionFounded(iReligion)):
			cityList = []
			for iPlayer in range(iNumPlayers):
				for pyCity in PyPlayer(iPlayer).getCityList():
					if pyCity.GetCy().isHasReligion(iReligion):
						if (pyCity.GetCy().getOwner() == iCiv):
							cityList.append(pyCity.GetCy())
			if (cityList):
				iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
				city = cityList[iCity]
				return (city.getX(), city.getY())
		return 0

	def spreadReligion(self, tPlot, iReligion ):
		pPlot = gc.getMap().plot( tPlot[0], tPlot[1] )
		if ( pPlot.isCity() ):
			pPlot.getPlotCity().setHasReligion(iReligion,1,1,0) # Absinthe: puts the given religion into this city, with interface message

	def buildInRandomCity( self, iPlayer, iBuilding, iReligion ):
		#print(" Building ",iBuilding," for ",iPlayer )
		cityList = []
		for pyCity in PyPlayer(iPlayer).getCityList():
			if ( (not pyCity.GetCy().hasBuilding(iBuilding)) and pyCity.GetCy().isHasReligion( iReligion ) ):
				cityList.append(pyCity.GetCy())
		if ( len(cityList) > 0 ):
			iRandCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iRandCity]
			city.setHasRealBuilding(iBuilding, True)
			gc.getPlayer( iPlayer ).changeFaith( 1 )
			if ( utils.getHumanID() == iPlayer ):
				sText = CyTranslator().getText("TXT_KEY_FAITH_BUILDING1", ()) +" " + gc.getBuildingInfo( iBuilding ).getDescription() + " " + CyTranslator().getText("TXT_KEY_FAITH_BUILDING2", ()) + " " + city.getName()
				CyInterface().addMessage(iPlayer, False, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iBlue), -1, -1, True, True)

##REFORMATION

	def showPopup(self, popupID, title, message, labels):
		popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
			popup.addButton( i )
		popup.launch(False)

	def reformationPopup(self):
		self.showPopup(7624, CyTranslator().getText("TXT_KEY_REFORMATION_TITLE", ()), CyTranslator().getText("TXT_KEY_REFORMATION_MESSAGE",()), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))

	def eventApply7624(self, popupReturn):
		iHuman = utils.getHumanID()
		if(popupReturn.getButtonClicked() == 0):
			self.reformationyes(iHuman)
		elif(popupReturn.getButtonClicked() == 1):
			self.reformationno(iHuman)

	def onTechAcquired(self, iTech, iPlayer):
		if (iTech == xml.iPrintingPress):
			if (gc.getPlayer(iPlayer).getStateReligion() == xml.iCatholicism):
				if (not gc.getGame().isReligionFounded(xml.iProtestantism)):
					gc.getPlayer(iPlayer).foundReligion(xml.iProtestantism,xml.iProtestantism,false)
					gc.getGame().getHolyCity(xml.iProtestantism).setNumRealBuilding(xml.iProtestantShrine,1)
					self.setReformationActive(True)
					self.reformationchoice(iPlayer)
					self.reformationOther(con.iIndependent)
					self.reformationOther(con.iIndependent2)
					self.reformationOther(con.iIndependent3)
					self.reformationOther(con.iIndependent4)
					self.reformationOther(con.iBarbarian)
					self.setReformationHitMatrix(iPlayer,2)
					for iCiv in range(iNumPlayers):
						if ((iCiv in lReformationNeighbours[iPlayer]) and self.getReformationHitMatrix(iCiv) == 0):
							self.setReformationHitMatrix(iCiv,1)

	def reformationArrayChoice(self):
		# 3Miro: this should be fixed, recursion and Python don't go well together
		iCiv = gc.getGame().getSorenRandNum(iNumPlayers, 'Civ chosen for reformation')
		while ( self.getReformationHitMatrix(iCiv) != 1 ):
			iCiv = gc.getGame().getSorenRandNum(iNumPlayers, 'Civ chosen for reformation')
		#print( " Chosen civ:", iCiv )
		if (self.getReformationHitMatrix(iCiv) == 1):
			#print( " Chosen civ eligible for Reformation")
			pPlayer = gc.getPlayer( iCiv )
			if ( pPlayer.isAlive() and pPlayer.getStateReligion() == xml.iCatholicism ):
				self.reformationchoice(iCiv)
			#	print( "Catholic choice:", iCiv )
			else:
				self.reformationOther( iCiv )
			#	print( "Not catholic and alive choice", iCiv )
			self.setReformationHitMatrix(iCiv,2)
			for iNextCiv in range(iNumPlayers):
				if ((iNextCiv in lReformationNeighbours[iCiv]) and self.getReformationHitMatrix(iNextCiv) == 0):
					self.setReformationHitMatrix(iNextCiv,1)
			print( self.getReformationHitMatrixAll(), 2*iNumPlayers )
			if (sum(self.getReformationHitMatrixAll()) == 2*iNumPlayers):
				self.setReformationActive(False)
				self.setCounterReformationActive(True) # after all players have been hit by the Reformation
		else:
			self.reformationArrayChoice()

	def reformationchoice(self, iCiv):
		if ( gc.getPlayer(iCiv).getStateReligion() == xml.iProtestantism ):
			self.reformationyes(iCiv)
		elif ((gc.getPlayer(iCiv)).isHuman()):
			self.reformationPopup()
		elif (lReformationMatrix[iCiv] != 0): # Absinthe: totally exclude the Pope from the Reformation
			rndnum = gc.getGame().getSorenRandNum(100, 'Reformation')
			#print( "Reformation calculus:", rndnum, lReformationMatrix[iCiv] )
			if (rndnum <= lReformationMatrix[iCiv]):
				self.reformationyes(iCiv)
				#print( " Yes to Reformation" )
			else:
				self.reformationno(iCiv)
				#print( " No to Reformation" )

	def reformationyes(self, iCiv):
		cityList = PyPlayer(iCiv).getCityList()
		iFaith = 0
		for city in cityList:
			if(city.city.isHasReligion(xml.iCatholicism)):
				iFaith += self.reformationReformCity( city.city, iCiv )

		pPlayer = gc.getPlayer(iCiv)
		#iStateReligion = pPlayer.getStateReligion()
		#if (pPlayer.getStateReligion() == xml.iCatholicism):
		pPlayer.setLastStateReligion(xml.iProtestantism)
		pPlayer.setConversionTimer(10)
		pPlayer.setFaith( iFaith )

	def reformationno(self, iCiv):
		cityList = PyPlayer(iCiv).getCityList()
		iLostFaith = 0
		pPlayer = gc.getPlayer(iCiv)
		for city in cityList:
			if(city.city.isHasReligion(xml.iCatholicism) and not city.city.isHasReligion(xml.iProtestantism)):
				rndnum = gc.getGame().getSorenRandNum(100, 'ReformationAnyway')
				if(rndnum <= 25 + (lReformationMatrix[iCiv] / 2)): # only add the religion, chance between 30% and 70%, based on lReformationMatrix
					city.city.setHasReligion(xml.iProtestantism, True, False, False)
					if ( pPlayer.isHuman() ): # message for the human player
						CityName = city.getNameKey()
						CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, CyTranslator().getText("TXT_KEY_REFORMATION_RELIGION_STILL_SPREAD", (CityName,)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, "", ColorTypes(con.iWhite), -1, -1, True, True)
					iLostFaith += 1
		gc.getPlayer(iCiv).changeFaith( - min( gc.getPlayer(iCiv).getFaith(), iLostFaith ) )

	def reformationOther( self, iCiv ):
		cityList = PyPlayer(iCiv).getCityList()
		iChanged = False
		for city in cityList:
			if(city.city.isHasReligion(xml.iCatholicism)):
				self.reformationOtherCity( city.city, iCiv )

	def reformationReformCity( self, pCity, iCiv ):
		iFaith = 0
		iPopBonus = 0
		bCathBuildings = False
		pPlayer = gc.getPlayer(iCiv)
		# bigger cities have more chance for a new religion to spread
		if (pCity.getPopulation() > 11 ):
			iPopBonus = 20
		elif (pCity.getPopulation() > 8 ):
			iPopBonus = 15
		elif (pCity.getPopulation() > 5 ):
			iPopBonus = 10
		elif (pCity.getPopulation() > 2 ):
			iPopBonus = 5
		# civ-specific, between 3 and 27
		iCivRef = (lReformationMatrix[pCity.getOwner()] / 10) * 3

		# spread the religion: range goes from 53-73% (Catholicism-lovers) to 77-97% (Protestantism-lovers), based on lReformationMatrix
		if (gc.getGame().getSorenRandNum(100, 'Religion spread to City') < 50 + iCivRef + iPopBonus):
			pCity.setHasReligion(xml.iProtestantism,True,True,False)
			iFaith += 1
			# if protestantism has spread, chance for replacing the buildings: between 58% and 82%, based on lReformationMatrix
			if(pCity.hasBuilding(xml.iCatholicChapel) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') < 55 + iCivRef ):
				pCity.setHasRealBuilding(xml.iCatholicChapel, False)
				pCity.setHasRealBuilding(xml.iProtestantChapel, True)
			if(pCity.hasBuilding(xml.iCatholicTemple) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') < 55 + iCivRef ):
				pCity.setHasRealBuilding(xml.iCatholicTemple, False)
				pCity.setHasRealBuilding(xml.iProtestantTemple, True)
				iFaith += 1
			if(pCity.hasBuilding(xml.iCatholicMonastery) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') < 55 + iCivRef ):
				pCity.setHasRealBuilding(xml.iCatholicMonastery, False)
				pCity.setHasRealBuilding(xml.iProtestantSeminary, True)
				iFaith += 1
			if(pCity.hasBuilding(xml.iCatholicCathedral) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') < 55 + iCivRef ):
				pCity.setHasRealBuilding(xml.iCatholicCathedral, False)
				if ( pCity.hasBuilding(xml.iCatholicReliquary) ):
					pCity.setHasRealBuilding(xml.iCatholicReliquary, False) # remove Reliquary since it is connected to the Cathedral
				pCity.setHasRealBuilding(xml.iProtestantCathedral, True)
				iFaith += 2

			# remove Catholicism if there are no religious buildings left, and there are no catholic wonders in the city
			if (gc.getGame().getSorenRandNum(100, 'Remove Religion') < 55 + ((lReformationMatrix[iCiv] / 5) * 2) - iPopBonus ): # range goes from 39-59% to 71-91%, based on lReformationMatrix
				lCathlist = [xml.iCatholicTemple, xml.iCatholicChapel, xml.iCatholicMonastery, xml.iCatholicCathedral, xml.iMonasteryOfCluny, xml.iKrakDesChevaliers, xml.iPalaisPapes, xml.iNotreDame, xml.iWestminster]
				for i in range( 0, len(lCathlist) ):
					if ( pCity.hasBuilding (lCathlist[i]) ):
						bCathBuildings = True
					#print( "lCathlist", lCathlist[i])
					#print( "bCathBuildings", bCathBuildings)
				if not bCathBuildings:
					pCity.setHasReligion(xml.iCatholicism,False,False,False)
					if ( pPlayer.isHuman() ): # message for the human player
						CityName = pCity.getNameKey()
						CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, CyTranslator().getText("TXT_KEY_REFORMATION_PEOPLE_ABANDON_CATHOLICISM_1", (CityName,)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, "", ColorTypes(con.iWhite), -1, -1, True, True)

		return iFaith

	def reformationOtherCity( self, pCity, iCiv ):
		iPopBonus = 0
		bCathBuildings = False
		pPlayer = gc.getPlayer(iCiv)
		# bigger cities have more chance for a new religion to spread
		if (pCity.getPopulation() > 11 ):
			iPopBonus = 30
		elif (pCity.getPopulation() > 7 ):
			iPopBonus = 20
		elif (pCity.getPopulation() > 3 ):
			iPopBonus = 10
		# civ-specific, between 3 and 27
		iCivRef = (lReformationMatrix[pCity.getOwner()] / 10) * 3

		# spread the religion: range goes from 23-53% (Catholicism-lovers) to 47-77% (Protestantism-lovers), based on lReformationMatrix
		if (gc.getGame().getSorenRandNum(100, 'Religion spread to City') < 20 + iCivRef + iPopBonus):
			pCity.setHasReligion(xml.iProtestantism,True,True,False)
			# if protestantism has spread, chance for replacing the buildings: between 31% and 79%, based on lReformationMatrix
			if(pCity.hasBuilding(xml.iCatholicChapel) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') < 25 + 2*iCivRef ):
				pCity.setHasRealBuilding(xml.iCatholicChapel, False)
				pCity.setHasRealBuilding(xml.iProtestantChapel, True)
			if(pCity.hasBuilding(xml.iCatholicTemple) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') < 25 + 2*iCivRef ):
				pCity.setHasRealBuilding(xml.iCatholicTemple, False)
				pCity.setHasRealBuilding(xml.iProtestantTemple, True)
			if(pCity.hasBuilding(xml.iCatholicMonastery) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') < 25 + 2*iCivRef ):
				pCity.setHasRealBuilding(xml.iCatholicMonastery, False)
				pCity.setHasRealBuilding(xml.iProtestantSeminary, True)
			if(pCity.hasBuilding(xml.iCatholicCathedral) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') < 25 + 2*iCivRef ):
				pCity.setHasRealBuilding(xml.iCatholicCathedral, False)
				if ( pCity.hasBuilding(xml.iCatholicReliquary) ):
					pCity.setHasRealBuilding(xml.iCatholicReliquary, False) # remove Reliquary since it is connected to the Cathedral
				pCity.setHasRealBuilding(xml.iProtestantCathedral, True)

			# remove Catholicism if there are no religious buildings left, and there are no catholic wonders in the city
			if (gc.getGame().getSorenRandNum(100, 'Remove Religion') < 50 + ((lReformationMatrix[iCiv] / 5) * 2) - (iPopBonus / 2) ): # range goes from 39-54% to 71-86%, based on lReformationMatrix
				lCathlist = [xml.iCatholicTemple, xml.iCatholicChapel, xml.iCatholicMonastery, xml.iCatholicCathedral, xml.iMonasteryOfCluny, xml.iKrakDesChevaliers, xml.iPalaisPapes, xml.iNotreDame, xml.iWestminster]
				for i in range( 0, len(lCathlist) ):
					if ( pCity.hasBuilding (lCathlist[i]) ):
						bCathBuildings = True
				if not bCathBuildings:
					pCity.setHasReligion(xml.iCatholicism,False,False,False)
					if ( pPlayer.isHuman() ): # message for the human player
						CityName = pCity.getNameKey()
						if ( pPlayer.getStateReligion() == xml.iIslam ):
							CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, CyTranslator().getText("TXT_KEY_REFORMATION_PEOPLE_ABANDON_CATHOLICISM_2", (CityName,)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, "", ColorTypes(con.iWhite), -1, -1, True, True)
						else:
							CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, CyTranslator().getText("TXT_KEY_REFORMATION_PEOPLE_ABANDON_CATHOLICISM_3", (CityName,)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, "", ColorTypes(con.iWhite), -1, -1, True, True)

	def doCounterReformation(self):
		print(" Counter Reformation ")
		for iPlayer in range( con.iPope - 1 ):
			pPlayer = gc.getPlayer( iPlayer )
			if ( pPlayer.isAlive() and pPlayer.getStateReligion() == xml.iCatholicism ):
				if ( pPlayer.isHuman() ):
					self.doCounterReformationHuman( iPlayer )
				elif ( lReformationMatrix[iPlayer] < gc.getGame().getSorenRandNum(100, 'Counter Reformation AI') ):
					self.doCounterReformationYes( iPlayer )
				else:
					self.doCounterReformationNo( iPlayer )
		self.setCounterReformationActive(False)

	def doCounterReformationHuman( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		szMessageYes = CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_YES_1", ()) + "+%d " %(max( 1, pPlayer.getNumCities() / 3 )) + CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_YES_2", ())
		szMessageNo = CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_NO_1", ()) + "+%d " %(max( 1, pPlayer.getNumCities() / 3 )) + CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_NO_2", ())
		self.showCounterPopup(7626, CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_TITLE", ()), CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE",()), (szMessageYes, szMessageNo))

	def showCounterPopup(self, popupID, title, message, labels):
		popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
			popup.addButton( i )
		popup.launch(False)

	def eventApply7626(self, popupReturn):
		iHuman = utils.getHumanID()
		if(popupReturn.getButtonClicked() == 0):
			self.doCounterReformationYes(iHuman)
		elif(popupReturn.getButtonClicked() == 1):
			self.doCounterReformationNo(iHuman)

	def eventApply7628(self, popupReturn):		#Absinthe: persecution popup
		"""Persecution popup event."""
		iPlotX, iPlotY, iUnitID = utils.getPersecutionData()
		religionList = utils.getPersecutionReligions()
		utils.prosecute(iPlotX, iPlotY, iUnitID, religionList[popupReturn.getButtonClicked()])

	def doCounterReformationYes( self, iPlayer ):
		print(" Counter Reformation Yes",iPlayer)
		pPlayer = gc.getPlayer( iPlayer )
		pCapital = pPlayer.getCapitalCity()
		iX = pCapital.getX()
		iY = pCapital.getY()
		if ( iX == -1 or iY == -1 ):
			if ( pPlayer.getNumCities() > 0 ):
				apCityList = PyPlayer(iPlayer).getCityList()
				pCapital = apCityList[gc.getGame().getSorenRandNum(len(apCityList), 'random city for prosecutors')].GetCy()
				iX = pCapital.getX()
				iY = pCapital.getY()
			else:
				return
		iNumProsecutors = max( 1, pPlayer.getNumCities() / 3 )
		for i in range( iNumProsecutors ):
			#print(" 3Miro CR",iPlayer,iX,iY,xml.iProsecutor)
			pPlayer.initUnit(xml.iProsecutor, iX, iY, UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
		for iNbr in range( len( lReformationNeighbours[iPlayer] ) ):
			pNbr = gc.getPlayer( lReformationNeighbours[iPlayer][iNbr] )
			if ( pNbr.isAlive() and pNbr.getStateReligion() == xml.iProtestantism ):
				pNCapital = pNbr.getCapitalCity()
				iX = pNCapital.getX()
				iY = pNCapital.getY()
				if ( iX == -1 or iY == -1 ):
					if ( pNbr.getNumCities() > 0 ):
						apCityList = PyPlayer(lReformationNeighbours[iPlayer][iNbr]).getCityList()
						pNCapital = apCityList[gc.getGame().getSorenRandNum(len(apCityList), 'random city for prosecutors')].GetCy()
						iX = pNCapital.getX()
						iY = pNCapital.getY()
					else:
						return

				pNbr.initUnit(xml.iProsecutor, iX, iY, UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)

	def doCounterReformationNo( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		pPlayer.changeStabilityBase( con.iCathegoryCities, max( 1, pPlayer.getNumCities() / 3 ) )
	### End Reformation ###

	def resettleRefugies( self ):
		intolerance = [-1]*con.iNumTotalPlayersB
		for iI in range( con.iNumTotalPlayersB ):
			pPlayer = gc.getPlayer( iI )
			if ( pPlayer.isAlive() ):
				if ( iI < con.iPope ):
					# add a random element
					intolerance[iI] += gc.getGame().getSorenRandNum(100, 'roll to randomize the migration of refugies')
					intolerance[iI] += 10*pPlayer.getProsecutionCount()
					if ( pPlayer.getProsecutionCount() == 0 ):
						intolerance[iI] = max( 0, intolerance[iI] - 30 ) # if this player doesn't prosecute, decrease intolerance
					iRCivic = pPlayer.getCivics(4)
					if ( iRCivic == xml.iCivicTheocracy ):
						intolerance[iI] += 50
					if ( iRCivic == xml.iCivicFreeReligion ):
						intolerance[iI] = max( 0, intolerance[iI] - 30 )
				if ( iI > con.iPope ):
					intolerance[iI] += gc.getGame().getSorenRandNum(100, 'roll to randomize the migration of refugies')
		# once we have the list of potential nations
		iCandidate1 = 0
		for iI in range( con.iNumTotalPlayersB ):
			if ( intolerance[iI] > -1 and intolerance[iI] < intolerance[iCandidate1] ):
				iCandidate1 = iI
		iCandidate2 = 0
		if ( iCandidate2 == iCandidate1 ):
			iCandidate2 = 1
		for iI in range( con.iNumTotalPlayersB ):
			if ( intolerance[iI] > -1 and iI != iCandidate1 and intolerance[iI] < intolerance[iCandidate1] ):
				iCandidate2 = iI

		if ( gc.getGame().getSorenRandNum(100, 'roll to migrate to one of the two most tolerant players') > 50 ):
			self.migrateJews( iCandidate1 )
		else:
			self.migrateJews( iCandidate2 )

	def migrateJews( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )

		lCityList = []
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			if ( not city.isHasReligion( xml.iJudaism ) ):
				lCityList.append( city )

		if ( len( lCityList ) > 0 ):
			city = lCityList[gc.getGame().getSorenRandNum(len(lCityList), 'random city to migrate')]
			city.setHasReligion(xml.iJudaism, True, True, False)

	def spread1200ADJews(self):
		# Spread Judaism to a random city in Africa
		tCity = self.selectRandomCityArea(tWestAfrica)
		self.spreadReligion(tCity, xml.iJudaism)
		# Spread Judaism to another city in Spain
		tCity = self.selectRandomCityArea(tSpain)
		self.spreadReligion(tCity, xml.iJudaism)
		# Spread Judaism to a city in France/Germany
		tCity = self.selectRandomCityArea(tGermany)
		self.spreadReligion(tCity, xml.iJudaism)

	def set1200Faith(self):
		for iPlayer in range(con.iNumPlayers):
			pPlayer = gc.getPlayer(iPlayer)
			pPlayer.setFaith(con.t1200ADFaith[iPlayer])