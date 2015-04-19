# Rhye's and Fall of Civilization - Religions management

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import cPickle as pickle
import Consts as con
import XMLConsts as xml
import RFCUtils
import RFCEMaps as rfcemaps

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
10, #Byzantium
40, #France
10, #Arabia
30, #Bulgaria
10, #Cordoba
30, #Venecia
50, #Burgundy
90, #Germany
20, #Novgorod
80, #Norway
20, #Kiev
50, #Hungary
10, #Spain
80, #Denmark
80, #Scotland
30, #Poland
30, #Genoa
10, #Morocco
80, #England
30, #Portugal
30, #Aragon
90, #Sweden
90, #Prussia
30, #Lithuania
50, #Austria
10, #Turkey
10, #Moscow
90, #Dutch
0,  #Rome
0,  #Indies and Barbs
0,
0,
0,
0
]

#Reformation neighbours spread reformation choice to each other
lReformationNeighbours = [
[con.iArabia,con.iBulgaria,con.iTurkey], #Byzantium
[con.iBurgundy,con.iSpain,con.iGermany,con.iGenoa,con.iEngland,con.iDutch,con.iScotland], #Frankia
[con.iByzantium,con.iCordoba,con.iTurkey],			#Arabia
[con.iByzantium,con.iKiev,con.iHungary,con.iTurkey],		#Bulgaria
[con.iArabia,con.iSpain,con.iPortugal,con.iAragon,con.iMorocco],			#Cordoba
[con.iGenoa,con.iGermany,con.iAustria,con.iHungary,con.iPope],			#Venecia
[con.iFrankia,con.iGermany,con.iGenoa,con.iDutch],			#Burgundy
[con.iBurgundy,con.iFrankia,con.iDenmark,con.iVenecia,con.iHungary,con.iPoland,con.iGenoa,con.iAustria,con.iDutch],		#Germany
[con.iSweden,con.iHungary,con.iPoland,con.iMoscow,con.iLithuania,con.iKiev],		#Novgorod
[con.iDenmark,con.iSweden],		#Norway
[con.iBulgaria,con.iHungary,con.iPoland,con.iMoscow,con.iLithuania,con.iNovgorod],		#Kiev
[con.iBulgaria,con.iVenecia,con.iKiev,con.iGermany,con.iPoland,con.iAustria,con.iTurkey],		#Hungary
[con.iFrankia,con.iCordoba,con.iPortugal,con.iAragon],			#Spain
[con.iNorway,con.iSweden,con.iGermany],		#Denmark
[con.iFrankia,con.iDutch,con.iEngland],			#Scotland
[con.iKiev,con.iHungary,con.iGermany,con.iMoscow,con.iAustria,con.iLithuania],			#Poland
[con.iBurgundy,con.iFrankia,con.iVenecia,con.iGermany,con.iPope,con.iAragon],		#Genoa
[con.iArabia,con.iSpain,con.iPortugal,con.iAragon,con.iCordoba],	#Morocco
[con.iFrankia,con.iDutch,con.iScotland],			#England
[con.iSpain,con.iCordoba,con.iAragon],			#Portugal
[con.iSpain,con.iCordoba,con.iPortugal,con.iFrankia,con.iGenoa],		#Aragon
[con.iNorway,con.iDenmark,con.iMoscow,con.iNovgorod],		#Sweden
[con.iGermany,con.iLithuania,con.iMoscow,con.iAustria,con.iPoland],		#Prussia
[con.iKiev,con.iMoscow,con.iPrussia,con.iNovgorod,con.iPoland],		#Lithuania
[con.iVenecia,con.iHungary,con.iGermany,con.iPoland],		#Austria
[con.iByzantium,con.iArabia,con.iBulgaria,con.iHungary],		#Turkey
[con.iKiev,con.iPoland,con.iSweden,con.iLithuania,con.iNovgorod],			#Moscow
[con.iBurgundy,con.iFrankia,con.iGermany,con.iEngland,con.iScotland],			#Dutch
[con.iVenecia,con.iGenoa]			#Pope
]
### Reformation End ###


### Regions to spread religion ###
tProvinceMap = rfcemaps.tProinceMap
tSpain = [xml.iP_Leon,xml.iP_GaliciaSpain,xml.iP_Aragon,xml.iP_Catalonia,xml.iP_Castile,xml.iP_Andalusia,xml.iP_Valencia]
tPoland = [xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Masovia,xml.iP_Silesia,xml.iP_Suvalkija,xml.iP_Brest,xml.iP_Pomerania]
tGermany = [xml.iP_Lorraine,xml.iP_Franconia,xml.iP_Bavaria,xml.iP_Swabia]
tWestAfrica = [xml.iP_Tetouan,xml.iP_Morocco,xml.iP_Marrakesh,xml.iP_Fez,xml.iP_Oran]
tNorthAfrica = [xml.iP_Algiers,xml.iP_Ifriqiya,xml.iP_Tripolitania,xml.iP_Cyrenaica]
tBalkansAndAnatolia = [xml.iP_Constantinople,xml.iP_Thrace,xml.iP_Opsikion,xml.iP_Paphlagonia,xml.iP_Thrakesion,xml.iP_Cilicia,xml.iP_Anatolikon,xml.iP_Armeniakon,xml.iP_Charsianon]
tCentralEurope = [xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Masovia,xml.iP_GaliciaPoland,xml.iP_Brest,xml.iP_Suvalkija,xml.iP_Lithuania,xml.iP_Prussia,xml.iP_Pomerania,xml.iP_Saxony,xml.iP_Brandenburg,xml.iP_Holstein,xml.iP_Denmark,xml.iP_Bavaria,xml.iP_Swabia,xml.iP_Bohemia,xml.iP_Moravia,xml.iP_Silesia,xml.iP_Hungary,xml.iP_Transylvania,xml.iP_UpperHungary,xml.iP_Pannonia,xml.iP_Slavonia,xml.iP_Carinthia,xml.iP_Austria]

class Religions:

##################################################
### Secure storage & retrieval of script data ###
################################################

	def getSeed( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['iSeed']

	def setSeed( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['iSeed'] = gc.getGame().getSorenRandNum(100, 'Seed for random delay')
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getReformationActive( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['bReformationActive']

	def setReformationActive( self, bNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['bReformationActive'] = bNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getReformationHitMatrix( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lReformationHitMatrix'][iCiv]

	def setReformationHitMatrix( self, iCiv, bNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lReformationHitMatrix'][iCiv] = bNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getReformationHitMatrixAll( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lReformationHitMatrix']

	def getCounterReformationActive( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['bCounterReformationActive']

	def setCounterReformationActive( self, bNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['bCounterReformationActive'] = bNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )


#######################################
### Main methods (Event-Triggered) ###
#####################################

	def setup(self):
		gc.getPlayer(con.iTurkey).changeFaith( 20 )
		self.setSeed()

	def checkTurn(self, iGameTurn):
		# Absinthe: Spreading religions in a couple preset dates
		if (iGameTurn == xml.i700AD-2):
			# Spread Judaism to Toledo
			self.spreadReligion(tToledo,xml.iJudaism)
			# Spread Judaism and Islam to a random city in Africa
			tCity = self.selectRandomCityArea(tNorthAfrica)
			self.spreadReligion(tCity,xml.iIslam)
			tCity = self.selectRandomCityArea(tNorthAfrica)
			self.spreadReligion(tCity,xml.iIslam)
		if (iGameTurn == xml.i700AD+2):
			# Spread Judaism and Islam to a random city in Africa
			tCity = self.selectRandomCityArea(tWestAfrica)
			self.spreadReligion(tCity,xml.iIslam)
			tCity = self.selectRandomCityArea(tWestAfrica)
			self.spreadReligion(tCity,xml.iJudaism)
		if (iGameTurn == xml.i900AD):
			# Spread Judaism to another city in Spain
			tCity = self.selectRandomCityArea(tSpain)
			self.spreadReligion(tCity,xml.iJudaism)
		if (iGameTurn == xml.i1000AD):
			# Spread Judaism to a city in France/Germany
			tCity = self.selectRandomCityArea(tGermany)
			self.spreadReligion(tCity,xml.iJudaism)
			# Spread Islam to another city in Africa
			tCity = self.selectRandomCityArea(tNorthAfrica)
			self.spreadReligion(tCity,xml.iIslam)
		if (iGameTurn == xml.i1101AD):
			# Spread Judaism to a couple towns in Poland
			tCity = self.selectRandomCityArea(tPoland)
			self.spreadReligion(tCity,xml.iJudaism)
		if (iGameTurn == xml.i1200AD):
			# Spread Judaism to a couple towns in Poland
			tCity = self.selectRandomCityArea(tPoland)
			self.spreadReligion(tCity,xml.iJudaism)
		if (iGameTurn > xml.i1299AD and iGameTurn < xml.i1350AD and iGameTurn % 3 == 0):
			# Spread Islam to a couple cities in Anatolia before the Ottoman spawn
			tCity = self.selectRandomCityArea(tBalkansAndAnatolia)
			self.spreadReligion(tCity,xml.iIslam)
		if (iGameTurn == xml.i1401AD):
			# Spread Judaism to a couple towns in Poland
			tCity = self.selectRandomCityArea(tPoland)
			self.spreadReligion(tCity,xml.iJudaism)
		if (iGameTurn == xml.i1580AD and (not gc.getGame().isReligionFounded(xml.iProtestantism) ) ):
			# If Protestantism has not been founded by the time the Dutch spawn, then the Dutch should found it
			gc.getPlayer(con.iDutch).foundReligion(xml.iProtestantism,xml.iProtestantism,false)
			gc.getGame().getHolyCity(xml.iProtestantism).setNumRealBuilding(xml.iProtestantShrine,1)
			self.setReformationActive(True)
			self.reformationchoice(con.iDutch)
			self.reformationOther(con.iIndependent)
			self.reformationOther(con.iIndependent2)
			self.reformationOther(con.iIndependent3)
			self.reformationOther(con.iIndependent4)
			self.reformationOther(con.iBarbarian)
			self.setReformationHitMatrix(con.iDutch,2)
			for iCiv in range(iNumPlayers):
				if ((iCiv in lReformationNeighbours[con.iDutch]) and self.getReformationHitMatrix(iCiv) == 0):
					self.setReformationHitMatrix(iCiv,1)

		# Absinthe: Spreading Judaism in random dates
		# general 5% chance to spread Jews to a random city in every third turn
		if (iGameTurn > xml.i800AD and iGameTurn < xml.i1700AD and iGameTurn % 3 == 0):
			if ( gc.getGame().getSorenRandNum(100, 'Spread Jews') < 5 ):
				tCity = self.selectRandomCityAll()
				self.spreadReligion(tCity,xml.iJudaism)
		# additional 9% chance to spread Jews to a random central european city in every third turn
		if (iGameTurn > xml.i1000AD and iGameTurn < xml.i1500AD and iGameTurn % 3 == 1):
			if ( gc.getGame().getSorenRandNum(100, 'Spread Jews') < 9 ):
				tCity = self.selectRandomCityArea(tCentralEurope)
				self.spreadReligion(tCity,xml.iJudaism)

		# Persecution
		for i in range( con.iNumPlayers ):
			pPlayer = gc.getPlayer( i )
			if ( pPlayer.getProsecutionCount() > 0 ):
				pPlayer.changeProsecutionCount( -1 )

		# Resettle Jewish refugies
		iRefugies = gc.getMinorReligionRefugies()
		for i in range(iRefugies):
			self.resettleRefugies()
		gc.setMinorReligionRefugies( 0 )

		# 3Miro: Catholic Benefits from the Pope
		# the Pope gifts gold every 3 turns
		if ( iGameTurn > xml.i1053AD ):
			iDivBy = 7
		else:
			iDivBy = 17
		if ( iGameTurn >= xml.i752AD and iGameTurn % iDivBy == 3 ):
			pPope = gc.getPlayer( con.iPope )
			teamPope = gc.getTeam( pPope.getTeam() )
			if ( pPope.getGold() > 100 ):
				iCatholicFaith = 0
				for i in range( iNumPlayers - 1 ): # the Pope cannot gift to himself
					pPlayer = gc.getPlayer( i )
					if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
						iCatholicFaith += pPlayer.getFaith()
				if ( iCatholicFaith > 0 ):
					iCatholicFaith += iCatholicFaith / 10 + 1
					if ( iGameTurn < 100 ):
						iGift = 20
					else:
						iGift = 50
					iRandomNum = gc.getGame().getSorenRandNum(iCatholicFaith, 'random Pope gold gift')
					for i in range( iNumPlayers - 1 ):
						pPlayer = gc.getPlayer( i )
						if ( pPlayer.getStateReligion() == xml.iCatholicism  and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
							iRandomNum -= pPlayer.getFaith()
							if ( iRandomNum <= 0 ):
								#print(" The Pope gifts 50 gold to ",i )
								pPope.changeGold( -iGift )
								pPlayer.changeGold( iGift )
								if ( utils.getHumanID() == i ):
									sText = CyTranslator().getText("TXT_KEY_FAITH_GIFT", ())
									CyInterface().addMessage(i, True, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
								break

		# free religious building every 6 turns
		if ( iGameTurn > xml.i800AD ): # 66 = 800AD, the crouning of Charlemagne
			if ( iGameTurn % 11 == 3 ):
				#print(" 3Miro Pope Builds " )
				pPope = gc.getPlayer( con.iPope )
				teamPope = gc.getTeam( pPope.getTeam() )
				iCatholicFaith = 0
				iJerusalemOwner = gc.getMap().plot( con.iJerusalem[0], con.iJerusalem[1]).getPlotCity().getOwner()
				for i in range( iNumPlayers - 1 ): # the Pope cannot gift to himself
					pPlayer = gc.getPlayer( i )
					if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
						#iCatholicFaith += pPlayer.getFaith() + pPope.AI_getAttitude( i )
						iCatholicFaith += max( 0, pPope.AI_getAttitude( i ) )
						if ( i == iJerusalemOwner ):
							iCatholicFaith += 20
				#print(" Catholic Faith: ",iCatholicFaith)
				if ( iCatholicFaith > 0 ):
					iCatholicFaith += iCatholicFaith / 5 + 1
					if ( gc.getGame().getSorenRandNum(100, 'random Catholic BuildingType') % 2 == 0 ):
						iCatholicBuilding = xml.iCatholicTemple
					else:
						iCatholicBuilding = xml.iCatholicMonastery
					iRandomNum = gc.getGame().getSorenRandNum(iCatholicFaith, 'random Pope Building Build')
					#print(" 3Miro Pope Builds " )
					for i in range( iNumPlayers - 1 ):
						pPlayer = gc.getPlayer( i )
						if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
							#iRandomNum -= pPlayer.getFaith() + pPope.AI_getAttitude( i )
							iRandomNum -= max( 0, pPope.AI_getAttitude( i ) )
							if ( i == iJerusalemOwner ):
								iCatholicFaith -= 20
							if ( iRandomNum <= 0 ):
								#print(" The Pope Builds ",iCatholicBuilding," for ",i )
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
		if ( iStateReligion == xml.iOrthodoxy and ( iBuilding in tOrthodoxBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iOrthodoxCathedral ):
				pPlayer.changeFaith( 3 )
		if ( iStateReligion == xml.iIslam and ( iBuilding in tIslamicBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iIslamicCathedral ):
				pPlayer.changeFaith( 3 )
		if ( iStateReligion == xml.iProtestantism and ( iBuilding in tProtestantBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iProtestantCathedral ):
				pPlayer.changeFaith( 3 )
		if ( iBuilding in tReligiousWonders ):
			pPlayer.changeFaith( 6 )
		if ( iStateReligion != xml.iJudaism and iBuilding == xml.iKazimierz ):
			pPlayer.changeFaith( - min( 1, pPlayer.getFaith() ) )
			# Kazimierz should also spread Judaism
			apCityList = PyPlayer(iPlayer).getCityList()
			for i in range(4):
				pCity = apCityList[gc.getGame().getSorenRandNum(len(apCityList), 'random city for jews')].GetCy()
				if (not pCity.isHasReligion(xml.iJudaism) ):
					pCity.setHasReligion(xml.iJudaism, True, True, False)


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
			return False

	def selectRandomCityCiv(self, iCiv):
		if (gc.getPlayer(iCiv).isAlive()):
			cityList = []
			for pyCity in PyPlayer(iCiv).getCityList():
				cityList.append(pyCity.GetCy())
			iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iCity]
			return (city.getX(), city.getY())
		return False

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
			return False

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
			return False

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
		return False

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
		return False

	def spreadReligion(self, tPlot, iReligion ):
		pPlot = gc.getMap().plot( tPlot[0], tPlot[1] )
		if ( pPlot.isCity() ):
			pPlot.getPlotCity().setHasReligion(iReligion,1,1,0) # Absinthe: puts the given religion (iReligion) into this city, with interface message

	def buildInRandomCity( self, iPlayer, iBuilding, iReligion ):
		#print(" Building ",iBuilding," for ",iPlayer )
		cityList = []
		for pyCity in PyPlayer(iPlayer).getCityList():
			if ( (not pyCity.GetCy().hasBuilding(iBuilding)) and pyCity.GetCy().isHasReligion( iReligion )  ):
				cityList.append(pyCity.GetCy())
		if ( len(cityList) > 0 ):
			iRandCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iRandCity]
			city.setHasRealBuilding(iBuilding, True)
			gc.getPlayer( iPlayer ).changeFaith( 1 )
			if ( utils.getHumanID() == iPlayer ):
				sText = CyTranslator().getText("TXT_KEY_FAITH_BUILDING1", ()) +" " + gc.getBuildingInfo( iBuilding ).getDescription() + " " + CyTranslator().getText("TXT_KEY_FAITH_BUILDING2", ()) + " " + city.getName()
				CyInterface().addMessage(iPlayer, True, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)

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
		if(self.getReformationHitMatrix(iCiv) == 1):
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

	def reformationOther( self, iCiv ):
		cityList = PyPlayer(iCiv).getCityList()
		iChanged = False
		for city in cityList:
			if(city.city.isHasReligion(xml.iCatholicism)):
				iDummy = self.reformationReformCity( city.city, 11, False )



	def reformationchoice(self, iCiv):
		if ( gc.getPlayer(iCiv).getStateReligion() == xml.iProtestantism ):
			self.reformationyes(iCiv)
		elif ((gc.getPlayer(iCiv)).isHuman()):
			self.reformationPopup()
		else:
			rndnum = gc.getGame().getSorenRandNum(100, 'Reformation')
			#print( "Reformation calculus:", rndnum, lReformationMatrix[iCiv] )
			if(rndnum <= lReformationMatrix[iCiv]):
				self.reformationyes(iCiv)
				#print( " Yes to Reformation" )
			else:
				self.reformationno(iCiv)
				#print( " No to Reformation" )

	def reformationReformCity( self, pCity, iKeepCatholicismBound, bForceConvertSmall ):
		iFaith = 0
		if(pCity.isHasReligion(xml.iCatholicism)):
			#iRandNum = gc.getSorenRandNum(100, 'Reformation of a City')
			if (pCity.getPopulation() > iKeepCatholicismBound ):
				pCity.setHasReligion(xml.iProtestantism,True,True,False)
				if(pCity.hasBuilding(xml.iCatholicChapel) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
					pCity.setHasRealBuilding(xml.iCatholicChapel, False)
					pCity.setHasRealBuilding(xml.iProtestantChapel, True)
				if(pCity.hasBuilding(xml.iCatholicTemple) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
					pCity.setHasRealBuilding(xml.iCatholicTemple, False)
					pCity.setHasRealBuilding(xml.iProtestantTemple, True)
					iFaith += 1
				if(pCity.hasBuilding(xml.iCatholicMonastery) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
					pCity.setHasRealBuilding(xml.iCatholicMonastery, False)
					pCity.setHasRealBuilding(xml.iProtestantSeminary, True)
					iFaith += 1
				if(pCity.hasBuilding(xml.iCatholicCathedral) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
					pCity.setHasRealBuilding(xml.iCatholicCathedral, False)
					if ( pCity.hasBuilding(xml.iCatholicReliquary) ):
						pCity.setHasRealBuilding(xml.iCatholicReliquary, False) # remove Reliquary since it is connected to the Cathedral
					pCity.setHasRealBuilding(xml.iProtestantCathedral, True)
					iFaith += 1
			elif ( bForceConvertSmall or gc.getGame().getSorenRandNum(100, 'Reformation of a City') < lReformationMatrix[pCity.getOwner()] ):
				pCity.setHasReligion(xml.iProtestantism,True,True,False)
				iFaith += 1
				if(pCity.hasBuilding(xml.iCatholicReliquary)):
					pCity.setHasRealBuilding(xml.iCatholicReliquary, False)
				if(pCity.hasBuilding(xml.iCatholicChapel)):
					pCity.setHasRealBuilding(xml.iCatholicChapel, False)
					pCity.setHasRealBuilding(xml.iProtestantChapel, True)
				if(pCity.hasBuilding(xml.iCatholicTemple)):
					pCity.setHasRealBuilding(xml.iCatholicTemple, False)
					pCity.setHasRealBuilding(xml.iProtestantTemple, True)
					iFaith += 1
				if(pCity.hasBuilding(xml.iCatholicMonastery)):
					pCity.setHasRealBuilding(xml.iCatholicMonastery, False)
					pCity.setHasRealBuilding(xml.iProtestantSeminary, True)
					iFaith += 1
				if(pCity.hasBuilding(xml.iCatholicCathedral)):
					pCity.setHasRealBuilding(xml.iCatholicCathedral, False)
					pCity.setHasRealBuilding(xml.iProtestantCathedral, True)
					iFaith += 1
				pCity.setHasReligion(xml.iCatholicism,False,False,False)
		return iFaith

	def reformationyes(self, iCiv):
		cityList = PyPlayer(iCiv).getCityList()
		iFaith = 0
		for city in cityList:
			if(city.city.isHasReligion(xml.iCatholicism)):
				iFaith += self.reformationReformCity( city.city, 7, True )

		pPlayer = gc.getPlayer(iCiv)
		#iStateReligion = pPlayer.getStateReligion()
		#if (pPlayer.getStateReligion() == xml.iCatholicism):
		pPlayer.setLastStateReligion(xml.iProtestantism)
		pPlayer.setFaith( iFaith )

	def reformationno(self, iCiv):
		cityList = PyPlayer(iCiv).getCityList()
		iLostFaith = 0
		for city in cityList:
			if(city.city.isHasReligion(xml.iCatholicism)):
				rndnum = gc.getGame().getSorenRandNum(100, 'ReformationAnyway')
				if(rndnum <= lReformationMatrix[iCiv]):
					city.city.setHasReligion(xml.iProtestantism, True, False, False)
					iLostFaith += 1
					#iLostFaith += self.reformationReformCity( city.city, 9, False )
		gc.getPlayer(iCiv).changeFaith( - min( gc.getPlayer(iCiv).getFaith(), iLostFaith ) )

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
			#if ( city.getProvince() in lMercList[ lMerc[0] ][4] ):
			if ( not city.isHasReligion( xml.iJudaism ) ):
			      lCityList.append( city )

		if ( len( lCityList ) > 0 ):
			city = lCityList[gc.getGame().getSorenRandNum(len(lCityList), 'random city to migrate')]
			city.setHasReligion(xml.iJudaism, True, True, False)


