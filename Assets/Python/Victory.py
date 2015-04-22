# Rhye's and Fall of Civilizations: Europe - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import cPickle as pickle
import Consts as con
import XMLConsts as xml
import RFCUtils
import Crusades as cru
import UniquePowers

utils = RFCUtils.RFCUtils()
up = UniquePowers.UniquePowers()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer


### Constants ###
# initialise player variables
iBurgundy = con.iBurgundy
iByzantium = con.iByzantium
iFrankia = con.iFrankia
iArabia = con.iArabia
iBulgaria = con.iBulgaria
iCordoba = con.iCordoba
iSpain = con.iSpain
iNorway = con.iNorway
iDenmark = con.iDenmark
iVenecia = con.iVenecia
iNovgorod = con.iNovgorod
iKiev = con.iKiev
iHungary = con.iHungary
iGermany = con.iGermany
iScotland = con.iScotland
iPoland = con.iPoland
iPrussia = con.iPrussia
iLithuania = con.iLithuania
iMoscow = con.iMoscow
iGenoa = con.iGenoa
iMorocco = con.iMorocco
iEngland = con.iEngland
iPortugal = con.iPortugal
iAragon = con.iAragon
iAustria = con.iAustria
iTurkey = con.iTurkey
iSweden = con.iSweden
iDutch = con.iDutch
iPope = con.iPope

iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers

pBurgundy = gc.getPlayer(iBurgundy)
pByzantium = gc.getPlayer(iByzantium)
pFrankia = gc.getPlayer(iFrankia)
pArabia = gc.getPlayer(iArabia)
pBulgaria = gc.getPlayer(iBulgaria)
pCordoba = gc.getPlayer(iCordoba)
pSpain = gc.getPlayer(iSpain)
pNorway = gc.getPlayer(iNorway)
pDenmark = gc.getPlayer(iDenmark)
pVenecia = gc.getPlayer(iVenecia)
pNovgorod = gc.getPlayer(iNovgorod)
pKiev = gc.getPlayer(iKiev)
pHungary = gc.getPlayer(iHungary)
pGermany = gc.getPlayer(iGermany)
pScotland = gc.getPlayer(iScotland)
pPoland = gc.getPlayer(iPoland)
pPrussia = gc.getPlayer(iPrussia)
pLithuania = gc.getPlayer(iLithuania)
pMoscow = gc.getPlayer(iMoscow)
pGenoa = gc.getPlayer(iGenoa)
pMorocco = gc.getPlayer(iMorocco)
pEngland = gc.getPlayer(iEngland)
pPortugal = gc.getPlayer(iPortugal)
pAragon = gc.getPlayer(iAragon)
pAustria = gc.getPlayer(iAustria)
pTurkey = gc.getPlayer(iTurkey)
pSweden = gc.getPlayer(iSweden)
pDutch = gc.getPlayer(iDutch)
pPope = gc.getPlayer(iPope)
pIndependent = gc.getPlayer(iIndependent)
pIndependent2 = gc.getPlayer(iIndependent2)
pBarbarian = gc.getPlayer(iBarbarian)

teamBurgundy = gc.getTeam(pBurgundy.getTeam())
teamByzantium = gc.getTeam(pByzantium.getTeam())
teamFrankia = gc.getTeam(pFrankia.getTeam())
teamArabia = gc.getTeam(pArabia.getTeam())
teamBulgaria = gc.getTeam(pBulgaria.getTeam())
teamCordoba = gc.getTeam(pCordoba.getTeam())
teamSpain = gc.getTeam(pSpain.getTeam())
teamNorway = gc.getTeam(pNorway.getTeam())
teamDenmark = gc.getTeam(pDenmark.getTeam())
teamVenecia = gc.getTeam(pVenecia.getTeam())
teamNovgorod = gc.getTeam(pNovgorod.getTeam())
teamKiev = gc.getTeam(pKiev.getTeam())
teamHungary = gc.getTeam(pHungary.getTeam())
teamGermany = gc.getTeam(pGermany.getTeam())
teamScotland = gc.getTeam(pScotland.getTeam())
teamPoland = gc.getTeam(pPoland.getTeam())
teamPrussia = gc.getTeam(pPrussia.getTeam())
teamLithuania = gc.getTeam(pLithuania.getTeam())
teamMoscow = gc.getTeam(pMoscow.getTeam())
teamGenoa = gc.getTeam(pGenoa.getTeam())
teamMorocco = gc.getTeam(pMorocco.getTeam())
teamEngland = gc.getTeam(pEngland.getTeam())
teamPortugal = gc.getTeam(pPortugal.getTeam())
teamAragon = gc.getTeam(pAragon.getTeam())
teamAustria = gc.getTeam(pAustria.getTeam())
teamTurkey = gc.getTeam(pTurkey.getTeam())
teamSweden = gc.getTeam(pSweden.getTeam())
teamDutch = gc.getTeam(pDutch.getTeam())
teamIndependent = gc.getTeam(pIndependent.getTeam())
teamIndependent2 = gc.getTeam(pIndependent2.getTeam())
teamBarbarian = gc.getTeam(pBarbarian.getTeam())

# ------------------- NEW UHV CONDITIONS
tByzantumControl = [ xml.iP_Colonea, xml.iP_Antiochia, xml.iP_Charsianon, xml.iP_Cilicia, xml.iP_Armeniakon, xml.iP_Anatolikon, xml.iP_Paphlagonia, xml.iP_Thrakesion, xml.iP_Opsikion, xml.iP_Constantinople, xml.iP_Thrace, xml.iP_Thessaloniki, xml.iP_Moesia, xml.iP_Macedonia, xml.iP_Serbia, xml.iP_Arberia, xml.iP_Epirus, xml.iP_Thessaly, xml.iP_Morea ]
tFrankControl = [ xml.iP_Swabia, xml.iP_Saxony, xml.iP_Lorraine, xml.iP_IleDeFrance, xml.iP_Picardy, xml.iP_Aquitania, xml.iP_Provence, xml.iP_Burgundy, xml.iP_Orleans, xml.iP_Champagne, xml.iP_Catalonia, xml.iP_Lombardy, xml.iP_Tuscany ]
tArabiaControlI = [ xml.iP_Egypt, xml.iP_Antiochia, xml.iP_Syria, xml.iP_Lebanon, xml.iP_Arabia, xml.iP_Jerusalem ]
tArabiaControlII = [ xml.iP_Oran, xml.iP_Algiers, xml.iP_Ifriqiya, xml.iP_Cyrenaica, xml.iP_Tripolitania, xml.iP_Egypt, xml.iP_Antiochia, xml.iP_Syria, xml.iP_Lebanon, xml.iP_Arabia, xml.iP_Jerusalem]
tBulgariaControl = [ xml.iP_Constantinople, xml.iP_Thessaloniki, xml.iP_Serbia, xml.iP_Thrace, xml.iP_Macedonia, xml.iP_Moesia, xml.iP_Arberia ]
tCordobaWonders = [ xml.iAlhambra, xml.iLaMezquita, xml.iGardensAlAndalus ]
tCordobaIslamize = [ xml.iP_GaliciaSpain, xml.iP_Castile, xml.iP_Leon, xml.iP_Lusitania, xml.iP_Catalonia, xml.iP_Aragon, xml.iP_Navarre, xml.iP_Valencia, xml.iP_LaMancha, xml.iP_Andalusia ]
tNorwayControl = [xml.iP_TheIsles, xml.iP_Ireland, xml.iP_Mercia, xml.iP_Normandy, xml.iP_Iceland]
tNorwayOutrank = [ iSweden, iDenmark, iScotland, iEngland, iGermany, iFrankia ]
#tNorseControl = [ xml.iP_Sicily, xml.iP_Iceland, xml.iP_Northumbria, xml.iP_Scotland, xml.iP_Normandy, xml.iP_Ireland, xml.iP_Novgorod ]
#tVenetianControl = [ xml.iP_Morea, xml.iP_Epirus, xml.iP_Dalmatia, xml.iP_Verona, xml.iP_Crete, xml.iP_Cyprus ]
tVenetianControl = [ xml.iP_Epirus, xml.iP_Dalmatia, xml.iP_Verona, xml.iP_Arberia ]
tBurgundyControl = [ xml.iP_Flanders, xml.iP_Picardy, xml.iP_Provence, xml.iP_Burgundy, xml.iP_Champagne, xml.iP_Lorraine ]
tBurgundyOutrank = [ iFrankia, iEngland, iGermany ]
tGermanyControl = [ xml.iP_Tuscany, xml.iP_Lombardy, xml.iP_Lorraine, xml.iP_Swabia, xml.iP_Saxony, xml.iP_Bavaria, xml.iP_Franconia, xml.iP_Brandenburg, xml.iP_Holstein ]
tGermanyControlII = [ xml.iP_Austria, xml.iP_Flanders, xml.iP_Pomerania, xml.iP_Silesia, xml.iP_Bohemia, xml.iP_Moravia, xml.iP_Swabia, xml.iP_Saxony, xml.iP_Bavaria, xml.iP_Franconia, xml.iP_Brandenburg, xml.iP_Holstein ]
tKievControl = [ xml.iP_Kiev, xml.iP_Podolia, xml.iP_Pereyaslavl, xml.iP_Sloboda, xml.iP_Chernigov, xml.iP_Volhynia, xml.iP_Minsk, xml.iP_Polotsk, xml.iP_Smolensk, xml.iP_Murom, xml.iP_Rostov, xml.iP_Novgorod, xml.iP_Vologda ]
tHungarynControl = [ xml.iP_Thrace, xml.iP_Moesia, xml.iP_Macedonia, xml.iP_Thessaloniki, xml.iP_Wallachia, xml.iP_Thessaly, xml.iP_Morea, xml.iP_Epirus, xml.iP_Arberia, xml.iP_Serbia, xml.iP_Banat, xml.iP_Bosnia, xml.iP_Dalmatia, xml.iP_Slavonia ]
tSpainConvert = [ xml.iP_GaliciaSpain, xml.iP_Castile, xml.iP_Leon, xml.iP_Lusitania, xml.iP_Catalonia, xml.iP_Aragon, xml.iP_Navarre, xml.iP_Valencia, xml.iP_LaMancha, xml.iP_Andalusia ]
tPolishControl = [ xml.iP_Bohemia, xml.iP_Moravia, xml.iP_UpperHungary, xml.iP_Prussia, xml.iP_Lithuania, xml.iP_Livonia, xml.iP_Polotsk, xml.iP_Minsk, xml.iP_Volhynia, xml.iP_Podolia, xml.iP_Moldova, xml.iP_Kiev ]
tGenoaControl = [ xml.iP_Sardinia, xml.iP_Corsica, xml.iP_Crete, xml.iP_Rhodes, xml.iP_Crimea ]
tEnglandControl = [ xml.iP_Aquitania, xml.iP_London, xml.iP_Wales, xml.iP_Wessex, xml.iP_Scotland, xml.iP_EastAnglia, xml.iP_Mercia, xml.iP_Northumbria, xml.iP_Ireland, xml.iP_Normandy, xml.iP_Bretagne, xml.iP_IleDeFrance, xml.iP_Orleans, xml.iP_Picardy ]
tPortugalControlI = [ xml.iP_Azores, xml.iP_Canaries, xml.iP_Madeira ]
tPortugalControlII = [ xml.iP_Morocco, xml.iP_Tetouan, xml.iP_Oran ]
#tLithuaniaControl = [ xml.iP_Lithuania, xml.iP_GreaterPoland, xml.iP_LesserPoland, xml.iP_Pomerania, xml.iP_Masovia, xml.iP_Brest, xml.iP_Suvalkija, xml.iP_Livonia, xml.iP_Novgorod, xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_Minsk, xml.iP_Chernigov, xml.iP_Pereyaslavl, xml.iP_Kiev, xml.iP_GaliciaPoland, xml.iP_Sloboda ]
tAustriaControl = [ xml.iP_Hungary, xml.iP_UpperHungary, xml.iP_Austria, xml.iP_Carinthia, xml.iP_Bavaria, xml.iP_Transylvania, xml.iP_Pannonia, xml.iP_Moravia, xml.iP_Silesia, xml.iP_Bohemia ]
tOttomanControlI = [ xml.iP_Serbia, xml.iP_Bosnia, xml.iP_Banat, xml.iP_Macedonia, xml.iP_Thrace, xml.iP_Moesia, xml.iP_Constantinople, xml.iP_Arberia, xml.iP_Epirus, xml.iP_Thessaloniki, xml.iP_Thessaly, xml.iP_Morea ]
tOttomanControlII = [ xml.iP_Colonea, xml.iP_Antiochia, xml.iP_Charsianon, xml.iP_Cilicia, xml.iP_Armeniakon, xml.iP_Anatolikon, xml.iP_Paphlagonia, xml.iP_Thrakesion, xml.iP_Opsikion, xml.iP_Syria, xml.iP_Lebanon, xml.iP_Jerusalem, xml.iP_Egypt ]
tOttomanControlIII = [ xml.iP_Austria ]
tMoscowControl = [ xml.iP_Donets, xml.iP_Kuban, xml.iP_Zaporizhia, xml.iP_Sloboda, xml.iP_Kiev, xml.iP_Moldova, xml.iP_Crimea, xml.iP_Pereyaslavl, xml.iP_Chernigov, xml.iP_Simbirsk, xml.iP_NizhnyNovgorod, xml.iP_Vologda, xml.iP_Rostov, xml.iP_Novgorod, xml.iP_Karelia, xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_Minsk, xml.iP_Volhynia, xml.iP_Podolia, xml.iP_Moscow, xml.iP_Murom ]
#tSwedenControlI = [ xml.iP_Gotaland, xml.iP_Svealand, xml.iP_Norrland, xml.iP_Skaneland, xml.iP_Gotland, xml.iP_Osterland ]
#tSwedenControlII = [ xml.iP_Saxony, xml.iP_Brandenburg, xml.iP_Holstein, xml.iP_Pomerania, xml.iP_Prussia, xml.iP_GreaterPoland, xml.iP_Masovia, xml.iP_Suvalkija, xml.iP_Lithuania, xml.iP_Livonia, xml.iP_Estonia, xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_Minsk, xml.iP_Murom, xml.iP_Chernigov, xml.iP_Moscow, xml.iP_Novgorod, xml.iP_Rostov ]
tSwedenControl = [ xml.iP_Norrland, xml.iP_Osterland, xml.iP_Karelia]
tNovgorodControl = [ xml.iP_Novgorod, xml.iP_Karelia, xml.iP_Estonia, xml.iP_Livonia, ]
tNovgorodControlII = [ xml.iP_Karelia, xml.iP_Vologda ]
tMoroccoControl = [ xml.iP_Morocco, xml.iP_Marrakesh, xml.iP_Fez, xml.iP_Tetouan, xml.iP_Oran, xml.iP_Algiers, xml.iP_Ifriqiya, xml.iP_Tripolitania, xml.iP_Andalusia, xml.iP_Valencia ]
tAragonControlI = [ xml.iP_Catalonia, xml.iP_Valencia, xml.iP_Balears, xml.iP_Sicily ]
tAragonControlII = [ xml.iP_Catalonia, xml.iP_Valencia, xml.iP_Aragon, xml.iP_Balears, xml.iP_Corsica, xml.iP_Sardinia, xml.iP_Sicily, xml.iP_Apulia, xml.iP_Provence, xml.iP_Thessaly ]
tPrussiaControlI = [ xml.iP_Lithuania, xml.iP_Livonia, xml.iP_Estonia, xml.iP_Pomerania, xml.iP_Prussia]
tPrussiaDefeat = [ iAustria, iMoscow, iGermany, iSweden, iFrankia, iSpain ]
tScotlandControl = [ xml.iP_Scotland, xml.iP_TheIsles, xml.iP_Ireland, xml.iP_Wales, xml.iP_Bretagne ]
tDenmarkControlI = [ xml.iP_Denmark, xml.iP_Skaneland, xml.iP_Svealand, xml.iP_Vestfold, xml.iP_Mercia, xml.iP_London, xml.iP_EastAnglia, xml.iP_Northumbria ]
#tDenmarkControlII = [ xml.iP_Brandenburg, xml.iP_Pomerania, xml.iP_Estonia ]
tDenmarkControlIII = [ xml.iP_Denmark, xml.iP_Norway, xml.iP_Vestfold, xml.iP_Skaneland, xml.iP_Gotaland, xml.iP_Svealand, xml.iP_Norrland, xml.iP_Gotland, xml.iP_Osterland, xml.iP_Estonia, xml.iP_Iceland ]

tHugeHungaryControl = ( 0, 23, 99, 72 )
totalLand = gc.getMap().getLandPlots()

class Victory:

	def __init__(self ):
		self.switchConditionsPerCiv = { iByzantium : self.checkByzantium,
						iFrankia : self.checkFrankia,
						iArabia : self.checkArabia,
						iBulgaria : self.checkBulgaria,
						iCordoba : self.checkCordoba,
						iVenecia : self.checkVenecia,
						iBurgundy : self.checkBurgundy,
						iGermany : self.checkGermany,
						iNovgorod : self.checkNovgorod,
						iNorway : self.checkNorway,
						iKiev : self.checkKiev,
						iHungary : self.checkHungary,
						iSpain : self.checkSpain,
						iDenmark : self.checkDenmark,
						iScotland : self.checkScotland,
						iPoland : self.checkPoland,
						iGenoa : self.checkGenoa,
						iMorocco : self.checkMorocco,
						iEngland : self.checkEngland,
						iPortugal : self.checkPortugal,
						iAragon : self.checkAragon,
						iSweden : self.checkSweden,
						iPrussia : self.checkPrussia,
						iLithuania : self.checkLithuania,
						iAustria : self.checkAustria,
						iTurkey : self.checkTurkey,
						iMoscow : self.checkMoscow,
						iDutch : self.checkDutch,
						}

##################################################
### Secure storage & retrieval of script data ###
################################################

	def getCorporationsFounded( self ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['bCorpsFounded']

	def setCorporationsFounded( self, iChange ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['bCorpsFounded'] = iChange
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

#######################################
### Main methods (Event-Triggered) ###
#####################################

	def checkTurn(self, iGameTurn):
		pass

	def checkPlayerTurn(self, iGameTurn, iPlayer):
		# We use Python version of Switch statement, it is supposed to be better, now all condition checks are in separate functions
		pPlayer = gc.getPlayer(iPlayer)
		if ( iPlayer < iPope and pPlayer.isAlive() ): # don't count the Pope
			self.switchConditionsPerCiv[iPlayer](iGameTurn)

		# Generic checks:
		#pPlayer = gc.getPlayer(iPlayer)
		if (pPlayer.isAlive() and iPlayer < iNumMajorPlayers):
			if ( not pPlayer.getUHV2of3() ):
				if (utils.countAchievedGoals(iPlayer) == 2):
					#intermediate bonus
					pPlayer.setUHV2of3( True )
					if (pPlayer.getNumCities() > 0): #this check is needed, otherwise game crashes
						capital = pPlayer.getCapitalCity()
						# 3Miro: Golden Age after 2/3 victories
						capital.setHasRealBuilding(xml.iTriumphalArch, True)
						if (pPlayer.isHuman()):
							CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_VICTORY_INTERMEDIATE", ()), "", 0, "", ColorTypes(con.iPurple), -1, -1, True, True)
							for iCiv in range(iNumPlayers):
								if (iCiv != iPlayer):
									pCiv = gc.getPlayer(iCiv)
									if (pCiv.isAlive()):
										iAttitude = pCiv.AI_getAttitude(iPlayer)
										if (iAttitude != 0):
											pCiv.AI_setAttitudeExtra(iPlayer, iAttitude-1) #da controllare

							iWarCounter = 0
							iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'civs')
							for i in range( iRndnum, iNumPlayers + iRndnum ):
								iCiv = i % iNumPlayers
								pCiv = gc.getPlayer(iCiv)
								if ((iCiv != con.iPope) and pCiv.isAlive() and pCiv.canContact(iPlayer)):
									if (pCiv.AI_getAttitude(iPlayer) < 2):
										teamCiv = gc.getTeam(pCiv.getTeam())
										if (not teamCiv.isAtWar(iPlayer)):
											teamCiv.declareWar(iPlayer, True, -1)
											iWarCounter += 1
											if (iWarCounter == 2):
												break

		if (gc.getGame().getWinner() == -1):
			if ( pPlayer.getUHV(0) == 1 and pPlayer.getUHV(1) == 1 and pPlayer.getUHV(2) == 1):
				gc.getGame().setWinner(iPlayer, 7) # Historical Victory

	def onCityBuilt(self, city, iPlayer): #see onCityBuilt in CvRFCEventHandler
		#if ( iPlayer == iPortugal and self.getGoal( iPortugal, 0 ) == -1 ):
			#iIslands = gc.countOwnedCities( iPortugal, tPortugalControl[0][0], tPortugalControl[0][1], tPortugalControl[0][2], tPortugalControl[0][3] )
			#iAfrica  = gc.countOwnedCities( iPortugal, tPortugalControl[1][0], tPortugalControl[1][1], tPortugalControl[1][2], tPortugalControl[1][3] )
			#iAfrica += gc.countOwnedCities( iPortugal, tPortugalControl[2][0], tPortugalControl[2][1], tPortugalControl[2][2], tPortugalControl[2][3] )
			#if ( iIslands >= 3 and iAfrica >= 2 ):
				#self.setGoal( iPortugal, 0, 1 )
		if ( iPlayer == iPortugal and pPortugal.getUHV( 0 ) == -1 ):
			iProv = city.getProvince()
			if ( iProv in tPortugalControlI or iProv in tPortugalControlII ):
				iCounter = pPortugal.getUHVCounter( 0 )
				iIslands = iCounter % 100
				iAfrica = iCounter / 100
				if ( iProv in tPortugalControlI ):
					iIslands += 1
				else:
					iAfrica += 1
				if ( iIslands >= 3 and iAfrica >= 2 ):
					pPortugal.setUHV( 0, 1 )
				pPortugal.setUHVCounter( 0, iAfrica * 100 + iIslands )

	def onReligionFounded(self, iReligion, iFounder):
		if ( iFounder == iGermany and pGermany.getUHV( 1 ) == -1 ):
			pGermany.setUHV( 1, 1 )
		elif ( iReligion == xml.iProtestantism and pGermany.getUHV( 1 ) == -1 ):
			pGermany.setUHV( 1, 0 )

	def onCityAcquired(self, owner, playerType, city, bConquest):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		iPlayer = owner
		iGameTurn = gc.getGame().getGameTurn()

		if ( iPlayer == iBulgaria and pBulgaria.isAlive() ):
			if ( iGameTurn <= xml.i1393AD and pBulgaria.getUHV( 2 ) == -1 ):
				if ( playerType == iBarbarian or playerType == iTurkey or playerType == iByzantium ):
					pBulgaria.setUHV( 2, 0 )

		elif ( iPlayer == iPortugal and pPortugal.isAlive() ):
			if ( bConquest ):
				if ( pPortugal.getUHV( 1 ) == -1 ):
					pPortugal.setUHV( 1, 0 )

		# old Swedish UHV 2
		#elif ( iPlayer == iSweden and pSweden.isAlive() ):
		#	if ( bConquest ):
		#		if ( pSweden.getUHV( 1 ) == -1 ):
		#			if ( playerType == iMoscow or playerType == iPoland or playerType == iLithuania):
		#				pSweden.setUHV( 1, 0 )

		#elif ( playerType == iAragon ):
		#	if ( city.hasBuilding( xml.iAragonSeaport )):
		#		iSeaports = pAragon.getUHVCounter(1)
		#		pAragon.setUHVCounter( 1, iSeaports + 1 )

		elif ( playerType == iNorway ):
			pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + city.getPopulation() )

		elif ( playerType == iPoland and pPoland.getUHV( 2 ) == -1 ):
			if ( city.hasBuilding( xml.iKazimierz )): # you cannot acquire religious buildings on conquest, only wonders
				iCounter = pPoland.getUHVCounter( 2 )
				iCathCath = ( iCounter / 10000 ) % 10
				iOrthCath = ( iCounter / 1000 ) % 10
				iProtCath = ( iCounter / 100 ) % 10
				iJewishQu = 99
				iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
				pPoland.setUHVCounter( 2, iCounter )
				if ( iCathCath >= 3 and iOrthCath >= 2 and iProtCath >= 2 and iJewishQu >= 2 ):
					pPoland.setUHV( 2, 1 )

		# Prussia UHV2: Conquer two cities from each of Austria, Muscowy, Germany, Sweden, France and Spain between 1650AD and 1763AD, if they are still alive.
		elif(playerType == iPrussia and owner in tPrussiaDefeat and iGameTurn >= xml.i1650AD and iGameTurn <= xml.i1763AD):
			lNumConq = []
			iConqRaw = pPrussia.getUHVCounter(1)
			bConq = True
			for iI in range(len(tPrussiaDefeat)):
				lNumConq.append((iConqRaw / pow(10,iI)) % 10)
				if(tPrussiaDefeat[iI] == owner):
					lNumConq[iI] += 1
					if(lNumConq[iI] > 9):
						# Prevent overflow
						lNumConq[iI] = 9
				if(lNumConq[iI] < 2 and gc.getPlayer(tPrussiaDefeat[iI]).isAlive()):
					bConq = False

			if(pPrussia.getUHV(1) == -1 and bConq):
				pPrussia.setUHV(1,1)

			iConqRaw = 0
			for iI in range(len(tPrussiaDefeat)):
				iConqRaw += lNumConq[iI] * pow(10,iI)
			pPrussia.setUHVCounter(1,iConqRaw)

	def onCityRazed(self, iPlayer, city):
		#if (iPlayer == iNorse): # Sedna17: Norse goal of razing 10? cities
		#	if ( pNorse.isAlive() and pNorse.getUHV( 2 ) == -1):
		#		if ( city.getOwner() < iNumPlayers ):
		#			#ioldrazed = self.getNorseRazed()
		#			#if (ioldrazed >= 9):
		#				#self.setGoal(iNorse,2,1)
		#			#else:
		#				#self.setNorseRazed(ioldrazed+1)
		#		       iRazed = pNorse.getUHVCounter( 2 ) + 1
		#			pNorse.setUHVCounter( 2, iRazed )
		#			if ( iRazed >= 6 ):
		#				pNorse.setUHV( 2, 1 )

		if(iPlayer == iSweden): # Swedish goal of razing 5 catholic cities while protestant
			if(pSweden.getStateReligion() == xml.iProtestantism and city.isHasReligion(xml.iCatholicism)):
				iRazed = pSweden.getUHVCounter(1)+1
				pSweden.setUHVCounter(1,iRazed)
				if(iRazed >= 5):
					pSweden.setUHV(1,1)

	def onPillageImprovement( self, iPillager, iVictim, iImprovement, iRoute, iX, iY ):
		#print( "3Miro: ", iPillager, iVictim, iImprovement, iRoute )
		if ( iPillager == iNorway and iRoute == -1 ):
			if ( gc.getMap().plot( iX, iY ).getOwner() != iNorway ):
				pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + 1 )

	def onCombatResult(self, argsList):
		pWinningUnit,pLosingUnit = argsList
		cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
		#Norwegian Viking points
		if ( pWinningUnit.getOwner() == iNorway ):
			if (cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_SEA")):
				pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + 2 )

	def onTechAcquired(self, iTech, iPlayer):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		#if ( iTech == xml.iPrintingPress ):
		#	if ( pGermany.getUHV( 1 ) == -1 ):
		#		if ( iPlayer == iGermany ):
		#			pGermany.setUHV( 1, 1 )
		#		else:
		#			pGermany.setUHV( 1, 0 )
		if ( iTech == xml.iIndustrialTech ):
			if ( pEngland.getUHV( 2 ) == -1 ):
				if ( iPlayer == iEngland ):
					pEngland.setUHV( 2, 1 )
				else:
					pEngland.setUHV( 2, 0 )

	def onBuildingBuilt(self, iPlayer, iBuilding):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		iGameTurn = gc.getGame().getGameTurn()

		if ( iPlayer == iKiev ):
			if ( pKiev.isAlive() and pKiev.getUHV( 0 ) == -1 ):
				if ( iBuilding == xml.iOrthodoxMonastery or iBuilding == xml.iOrthodoxCathedral ):
					iBuildSoFar = pKiev.getUHVCounter( 0 )
					iCathedralCounter = iBuildSoFar % 100
					iMonasteryCounter = iBuildSoFar / 100
					if ( iBuilding == xml.iOrthodoxMonastery ):
						iMonasteryCounter += 1
					else:
						iCathedralCounter += 1
					if ( iCathedralCounter >= 2 and iMonasteryCounter >= 8 ):
						pKiev.setUHV( 0, 1 )
					pKiev.setUHVCounter( 0, 100 * iMonasteryCounter + iCathedralCounter )
		# Sedna17: Polish UHV changed again
		# HHG: Polish UHV3 now uses Wonder Kazimierz with maximum value 99, and all other buildings have boundary checks
		elif ( iPlayer == iPoland ):
			if ( pPoland.isAlive() and pPoland.getUHV( 2 ) == -1 ):
				lBuildingList = [xml.iCatholicCathedral,xml.iOrthodoxCathedral,xml.iProtestantCathedral,xml.iJewishQuarter,xml.iKazimierz]
				if ( iBuilding in lBuildingList):
					iCounter = pPoland.getUHVCounter( 2 )
					iCathCath = ( iCounter / 10000 ) % 10
					iOrthCath = ( iCounter / 1000 ) % 10
					iProtCath = ( iCounter / 100 ) % 10
					iJewishQu = iCounter % 100
					if ( iCathCath < 9 and iBuilding == xml.iCatholicCathedral ):
						iCathCath += 1
					elif ( iOrthCath < 9 and iBuilding == xml.iOrthodoxCathedral ):
						iOrthCath += 1
					elif ( iProtCath < 9 and iBuilding == xml.iProtestantCathedral ):
						iProtCath += 1
					elif ( iBuilding == xml.iKazimierz ):
						iJewishQu = 99
					elif ( iJewishQu < 99 and iBuilding == xml.iJewishQuarter ):
						iJewishQu += 1
					if ( iCathCath >= 3 and iOrthCath >= 3 and iProtCath >= 2 and iJewishQu >= 2 ):
						pPoland.setUHV( 2, 1 )
					iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
					pPoland.setUHVCounter( 2, iCounter )

		elif ( iPlayer == iGenoa ): # Buildings Goal 2
			if ( pGenoa.isAlive() and pGenoa.getUHV( 1 ) == -1 ):
				if ( iBuilding == xml.iGenoaBank ):
					iCounter = pGenoa.getUHVCounter( 1 )
					iCorps = iCounter % 100
					iBanks = iCounter / 100 + 1
					if ( iBanks >= 8 and iCorps >= 2 ):
						pGenoa.setUHV( 1, 1 )
					pGenoa.setUHVCounter( 1, 100 * iBanks + iCorps )

		if ( iBuilding in tCordobaWonders ):
			if (pCordoba.isAlive() and pCordoba.getUHV( 1 ) == -1 ):
				if (iPlayer == iCordoba):
					iWondersBuilt = pCordoba.getUHVCounter( 1 )
					pCordoba.setUHVCounter( 1, iWondersBuilt + 1 )
					if (iWondersBuilt == 2):
						pCordoba.setUHV( 1, 1 )
				else:
					pCordoba.setUHV( 1, 0 )


	def onProjectBuilt(self, iPlayer, iProject):
		if ( self.isProjectAColony( iProject )):
			if ( pVenecia.getUHV( 2 ) == -1 and iProject != xml.iColVinland ):
				if ( iPlayer == iVenecia ):
					pVenecia.setUHV( 2, 1 )
				else:
					pVenecia.setUHV( 2, 0 )
			if ( iPlayer == iFrankia ):
				pFrankia.setUHVCounter( 2, pFrankia.getUHVCounter( 2 ) + 1 )
				if ( pFrankia.getUHV( 2 ) == -1 ):
					if ( self.getNumRealColonies(iFrankia) >= 5 ):
						pFrankia.setUHV( 2, 1 )
			elif ( iPlayer == iEngland ):
				pEngland.setUHVCounter( 1, pEngland.getUHVCounter( 1 ) + 1 )
				if ( pEngland.getUHV( 1 ) == -1 ):
					if ( self.getNumRealColonies(iEngland) >= 7 ):
						pEngland.setUHV( 1, 1 )
			elif ( iPlayer == iSpain ):
				pSpain.setUHVCounter( 1, pSpain.getUHVCounter( 1 ) + 1 )
			elif ( iPlayer == iPortugal ):
				pPortugal.setUHVCounter( 2, pPortugal.getUHVCounter( 2 ) + 1 )
				if ( pPortugal.getUHV( 2 ) == -1 ):
					if ( self.getNumRealColonies(iPortugal) >= 5 ):
						pPortugal.setUHV( 2, 1 )
			elif ( iPlayer == iDutch ):
				pDutch.setUHVCounter( 1, pDutch.getUHVCounter( 1 ) + 1 )
				if ( pDutch.getUHV( 1 ) == -1 ):
					iWestCompany = teamDutch.getProjectCount(xml.iWestIndiaCompany)
					iEastCompany = teamDutch.getProjectCount(xml.iEastIndiaCompany)
					if ( self.getNumRealColonies(iDutch) >= 3 and iWestCompany == 1 and iEastCompany == 1):
						pDutch.setUHV( 1, 1 )
			elif ( iPlayer == iDenmark ):
				pDenmark.setUHVCounter( 2, pDenmark.getUHVCounter( 2 ) + 1 )
				if ( pDenmark.getUHV( 2 ) == -1 ):
					iWestCompany = teamDenmark.getProjectCount(xml.iWestIndiaCompany)
					iEastCompany = teamDenmark.getProjectCount(xml.iEastIndiaCompany)
					if ( self.getNumRealColonies(iDenmark) >= 3 and iWestCompany == 1 and iEastCompany == 1):
						pDenmark.setUHV( 2, 1 )


	def onCorporationFounded(self, iPlayer ):
		self.setCorporationsFounded( self.getCorporationsFounded() + 1 )
		if ( iPlayer == iGenoa ):
			#self.setGenoaCorporations( self.getGenoaCorporations() + 1 )
			iCounter = pGenoa.getUHVCounter( 1 )
			iCorps = iCounter % 100 + 1
			iBanks = iCounter / 100
			if ( iBanks >= 8 and iCorps >= 2 ):
				pGenoa.setUHV( 1, 1 )
			pGenoa.setUHVCounter( 1, 100 * iBanks + iCorps )
		if ( self.getCorporationsFounded() == 7 and pGenoa.getUHV( 1 ) == -1 ):
			iCounter = pGenoa.getUHVCounter( 1 )
			iCorps = iCounter % 100 + 1
			if ( iCorps < 2 ):
				pGenoa.setUHV( 1, 0 )

	def getOwnedLuxes( self, pPlayer ):
		iCount = 0
		iCount += pPlayer.countOwnedBonuses( xml.iSheep )
		iCount += pPlayer.countOwnedBonuses( xml.iDye )
		iCount += pPlayer.countOwnedBonuses( xml.iFur )
		iCount += pPlayer.countOwnedBonuses( xml.iGems )
		iCount += pPlayer.countOwnedBonuses( xml.iGold )
		iCount += pPlayer.countOwnedBonuses( xml.iIncense )
		iCount += pPlayer.countOwnedBonuses( xml.iIvory )
		iCount += pPlayer.countOwnedBonuses( xml.iSilk )
		iCount += pPlayer.countOwnedBonuses( xml.iSilver )
		iCount += pPlayer.countOwnedBonuses( xml.iSpices )
		iCount += pPlayer.countOwnedBonuses( xml.iWine )
		iCount += pPlayer.countOwnedBonuses( xml.iHoney )
		iCount += pPlayer.countOwnedBonuses( xml.iWhale )
		iCount += pPlayer.countOwnedBonuses( xml.iAmber )
		iCount += pPlayer.countOwnedBonuses( xml.iCotton )
		iCount += pPlayer.countOwnedBonuses( xml.iCoffee )
		iCount += pPlayer.countOwnedBonuses( xml.iTea )
		iCount += pPlayer.countOwnedBonuses( xml.iTobacco )
		#iCount += pPlayer.countOwnedBonuses( xml.iRelic )
		return iCount

	def getOwnedGrain( self, pPlayer ):
		iCount = 0
		iCount += pPlayer.countOwnedBonuses( xml.iWheat )
		iCount += pPlayer.countOwnedBonuses( xml.iBarley )
		return iCount

	def isProjectAColony( self, iProject ):
		if (iProject >= xml.iNumNotColonies):
			return True
		else:
			return False

	def checkByzantium( self, iGameTurn ):
		if ( iGameTurn == xml.i1025AD and pByzantium.getUHV( 0 ) == -1 ):
			if ( gc.isLargestCity( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ) and gc.isTopCultureCity( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ) and gc.getMap().plot( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ).getPlotCity().getOwner() == iByzantium ):
				pByzantium.setUHV( 0, 1 )
			else:
				pByzantium.setUHV( 0, 0 )

		# UHV2: Keep or reconquer Constantinople, Thrace, Thessaloniki, Moesia, Macedonia, Serbia, Arberia, Epirus, Thessaly, Morea, Colonea, Antiochia, Charsianon, Cilicia, Armeniakon, Anatolikon, Paphlagonia, Thrakesion and Opsikion in 1282AD
		if ( iGameTurn == xml.i1282AD and pByzantium.getUHV( 1 ) == -1 ):
			bOwn = True
			for iProv in tByzantumControl:
				if ( pByzantium.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pByzantium.setUHV( 1, 1 )
			else:
				pByzantium.setUHV( 1, 0 )

		if ( iGameTurn == xml.i1453AD and pByzantium.getUHV( 2 ) == -1 ):
			iGold = pByzantium.getGold()
			bMost = True
			for iCiv in range( iNumPlayers ):
				if ( iCiv != iByzantium and gc.getPlayer( iCiv ).isAlive() ):
					if (gc.getPlayer(iCiv).getGold() > iGold):
						bMost = False
			if ( bMost ):
				 pByzantium.setUHV( 2, 1 )
			else:
				 pByzantium.setUHV( 2, 0 )

	def checkFrankia( self, iGameTurn ):
		if ( iGameTurn <= xml.i840AD and pFrankia.getUHV(0) == -1 ):
			bCharlemagneEmpire = True
			for iProv in tFrankControl:
				iHave = pFrankia.getProvinceCurrentState( iProv )
				if ( iHave < con.iProvinceConquer ):
					bCharlemagneEmpire = False
					break
			if ( bCharlemagneEmpire ):
				pFrankia.setUHV( 0, 1 )
			elif ( iGameTurn == xml.i840AD ):
				pFrankia.setUHV( 0, 0 )

		if (iGameTurn == xml.i1291AD and pFrankia.getUHV(1) == -1 ):
			pJPlot = gc.getMap().plot( con.iJerusalem[0], con.iJerusalem[1] )
			if ( pJPlot.isCity()):
				if ( pJPlot.getPlotCity().getOwner() == iFrankia ):
					pFrankia.setUHV( 1, 1 )
				else:
					pFrankia.setUHV( 1, 0 )
			else:
				pFrankia.setUHV( 1, 0 )

		# UHV3: Build 5 Colonies.
		# handled in the onProjectBuilt function


	def checkArabia( self, iGameTurn ):
		# UHV1: Conquer all territories from Egypt to Asia Minor by 955 AD
		if ( iGameTurn == xml.i955AD and pArabia.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tArabiaControlI:
				if ( pArabia.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pArabia.setUHV( 0, 1 )
			else:
				pArabia.setUHV( 0, 0 )
		# UHV2: Conquer all territories from Oran to Asia Minor by 1291 AD
		if ( iGameTurn == xml.i1291AD and pArabia.getUHV( 1 ) == -1 ):
			bConq = True
			for iProv in tArabiaControlII:
				if ( pArabia.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pArabia.setUHV( 1, 1 )
			else:
				pArabia.setUHV( 1, 0 )
		# UHV3: Spread Islam to 35% of the world population
		if ( pArabia.getUHV( 2 ) == -1 ):
			iPerc = gc.getGame().calculateReligionPercent( xml.iIslam )
			if ( iPerc >= 35 ):
				pArabia.setUHV( 2, 1 )

	def checkBulgaria( self, iGameTurn ):
		if ( iGameTurn <= xml.i917AD and pBulgaria.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tBulgariaControl:
				if ( pBulgaria.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pBulgaria.setUHV( 0, 1 )
			elif ( iGameTurn == xml.i917AD ):
				pBulgaria.setUHV( 0, 0 )

		if ( iGameTurn <= xml.i1259AD and pBulgaria.getUHV( 1 ) == -1 ):
			if ( pBulgaria.getFaith() >= 100 ):
				pBulgaria.setUHV( 1, 1 )
			elif ( iGameTurn == xml.i1259AD ):
				pBulgaria.setUHV( 1, 0 )

		if ( iGameTurn == xml.i1393AD and pBulgaria.getUHV( 2 ) == -1 ):
			pBulgaria.setUHV( 2, 1 )

	def checkCordoba( self, iGameTurn ):
		if ( iGameTurn == xml.i961AD and pCordoba.getUHV(0) == -1 ):
			if ( gc.isLargestCity( con.tCapitals[iCordoba][0], con.tCapitals[iCordoba][1] ) and gc.getMap().plot( con.tCapitals[iCordoba][0], con.tCapitals[iCordoba][1] ).getPlotCity().getOwner() == iCordoba ):
				pCordoba.setUHV( 0, 1 )
			else:
				pCordoba.setUHV( 0, 0 )

		if ( iGameTurn == xml.i1309AD+1 and pCordoba.getUHV(1) == -1 ):
			pCordoba.setUHV( 1, 0 )

		if ( iGameTurn == xml.i1492AD and pCordoba.getUHV(2) == -1 ):
			bIslamized = True
			for iProv in tCordobaIslamize:
				if ( not ( pCordoba.provinceIsSpreadReligion( iProv, xml.iIslam ) ) ):
					bIslamized = False
					break
			if ( bIslamized ):
				pCordoba.setUHV( 2, 1 )
			else:
				pCordoba.setUHV( 2, 0 )

	def checkNorway( self, iGameTurn ):
		# UHV1 old: explore all water tiles
		#if ( iGameTurn == xml.i1009AD and pNorway.getUHV( 0 ) == -1 ):
		#	if ( gc.canSeeAllTerrain( iNorway, xml.iTerrainOcean ) ):
		#		pNorway.setUHV( 0, 1 )
		#	else:
		#		pNorway.setUHV( 0, 0 )

		# UHV1: Gain 50 Viking points by 1066AD.
		if ( iGameTurn <= xml.i1066AD and pNorway.getUHV( 0 ) == -1 ):
			if ( pNorway.getUHVCounter( 2 ) >= 50 ): # It's still counter 2, for the sake of convenience and confusion
				pNorway.setUHV( 0, 1 )
			elif ( iGameTurn == xml.i1066AD ):
				pNorway.setUHV( 0, 0 )

		# UHV2: Conquer The Isles, Ireland, Mercia, Normandy, Iceland and build Vinland by 1263AD.
		if ( iGameTurn <= xml.i1263AD and pNorway.getUHV( 1 ) == -1 ):
			bConq = True
			for iProv in tNorwayControl:
				if(pNorway.getProvinceCurrentState( iProv ) < con.iProvinceConquer):
					bConq = False
					break
			if(bConq and pNorway.getNumColonies() >= 1):
				pNorway.setUHV( 1, 1 )
			elif(iGameTurn == xml.i1263AD):
				pNorway.setUHV( 1, 0 )

		# UHV3: Have higher score than Sweden, Denmark, Scotland, England, Germany and France in 1320AD.
		if ( iGameTurn == xml.i1320AD and pNorway.getUHV(2) == -1 ):
			iNorwayRank = gc.getGame().getTeamRank(iNorway)
			bIsOnTop = True
			for iTestPlayer in tNorwayOutrank:
				if(gc.getGame().getTeamRank(iTestPlayer) < iNorwayRank):
					bIsOnTop = False
					break
			if(bIsOnTop):
				pNorway.setUHV( 2, 1 )
			else:
				pNorway.setUHV( 2, 0 )


	def checkDenmark(self,iGameTurn):

		# UHV1: Control Denmark, Skaneland, Svealand, Vestfold, Mercia, London, Northumbria and East Anglia in 1050.
		if ( iGameTurn == xml.i1050AD and pDenmark.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tDenmarkControlI:
				if ( pDenmark.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pDenmark.setUHV( 0, 1 )
			else:
				pDenmark.setUHV( 0, 0 )

		# UHV2: Control Denmark, Norway, Vestfold, Skaneland, Götaland, Svealand, Norrland, Gotland, Österland, Estonia and Iceland in 1523.
		if ( iGameTurn == xml.i1523AD and pDenmark.getUHV( 1 ) == -1 ):
			bConq = True
			for iProv in tDenmarkControlIII:
				if ( pDenmark.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pDenmark.setUHV( 1, 1 )
			else:
				pDenmark.setUHV( 1, 0 )

		# UHV3: Get 3 Colonies and complete both Trading Companies.
		# handled in the onProjectBuilt function


	def checkVenecia( self, iGameTurn ):

		# UHV1: Control the Adriatic and some Mediterranean islands in 1004 AD
		if ( iGameTurn <= xml.i1004AD and pVenecia.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tVenetianControl:
				if ( pVenecia.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pVenecia.setUHV( 0, 1 )
			elif ( iGameTurn == xml.i1004AD ):
				pVenecia.setUHV( 0, 0 )

		# UHV2: Conquer Constantinople by 1204 AD
		if ( iGameTurn <= xml.i1204AD and pVenecia.getUHV( 1 ) == -1 ):
			if ( pVenecia.getProvinceCurrentState( xml.iP_Constantinople ) >= con.iProvinceConquer ):
				pVenecia.setUHV( 1, 1 )
			elif ( iGameTurn == xml.i1204AD ):
				pVenecia.setUHV( 1, 0 )

		# UHV3: Be the first to build a modern Colony (so Vinland doesn't count)
		# handled in the onProjectBuilt function

	def checkBurgundy( self, iGameTurn ):
		# Culture counter
		iCulture =pBurgundy.getUHVCounter( 0 ) + pBurgundy.countCultureProduced() # 3Miro: testing, move it below later
		pBurgundy.setUHVCounter( 0, iCulture )

		# UHV1: 10000 culture
		if ( iGameTurn <= xml.i1336AD and pBurgundy.getUHV( 0 ) == -1 ):
			if ( iCulture >= 10000 ):
				pBurgundy.setUHV( 0, 1 )
			else:
				if ( iGameTurn == xml.i1336AD ):
					pBurgundy.setUHV( 0, 0 )

		# UHV2: control provinces
		if ( iGameTurn == xml.i1376AD and pBurgundy.getUHV( 1 ) == -1 ):
			bOwn = True
			for iProv in tBurgundyControl:
				if ( pBurgundy.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pBurgundy.setUHV( 1, 1 )
			else:
				pBurgundy.setUHV( 1, 0 )

		# UHV3: high score
		if ( iGameTurn == xml.i1473AD and pBurgundy.getUHV(2) == -1 ):
			iBurgundyRank = gc.getGame().getTeamRank(iBurgundy)
			bIsOnTop = True
			for iTestPlayer in tBurgundyOutrank:
				if ( gc.getGame().getTeamRank(iTestPlayer) < iBurgundyRank ):
					bIsOnTop = False
					break
			if ( bIsOnTop ):
				pBurgundy.setUHV( 2, 1 )
			else:
				pBurgundy.setUHV( 2, 0 )

	def checkGermany( self, iGameTurn ):
		# Have most Catholic FP in 1077 (Walk to Canossa)
		# Have vassals (Habsburg)
		# Start the reformation
		if ( iGameTurn == xml.i1167AD and pGermany.getUHV( 0 ) == -1 ):
			bOwn = True
			for iProv in tGermanyControl:
				if ( pGermany.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pGermany.setUHV( 0, 1 )
			else:
				pGermany.setUHV( 0, 0 )

		if ( iGameTurn == xml.i1648AD and pGermany.getUHV( 2 ) == -1 ):
			bOwn = True
			for iProv in tGermanyControlII:
				if ( pGermany.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pGermany.setUHV( 2, 1 )
			else:
				pGermany.setUHV( 2, 0 )


	def checkNovgorod( self, iGameTurn ):

		# UHV1: Control Novgorod, Karelia, Estonia and Livonia in 1250.
		if ( iGameTurn == xml.i1250AD and pNovgorod.getUHV( 0 ) == -1 ):
			bOwn = True
			for iProv in tNovgorodControl:
				if ( pNovgorod.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pNovgorod.setUHV( 0, 1 )
			else:
				pNovgorod.setUHV( 0, 0 )

		# UHV2: Control twelve sources of fur by 1397.
		if (pNovgorod.getUHV( 1 ) == -1):
			if (iGameTurn <= xml.i1397AD):
				if (pNovgorod.countOwnedBonuses(xml.iFur) >= 12):
					pNovgorod.setUHV( 1, 1 )
			else:
				pNovgorod.setUHV( 1, 0 )

		# UHV3: Have seven cities in Karelia and Vologda in 1478.
		if (iGameTurn == xml.i1478AD and pNovgorod.getUHV( 2 ) == -1 ):
			iNumCities = 0
			for iProv in tNovgorodControlII:
				iNumCities += pNovgorod.getProvinceCityCount( iProv )
			if ( iNumCities >= 7 ):
				pNovgorod.setUHV( 2, 1 )
			else:
				pNovgorod.setUHV( 2, 0 )


	def checkKiev( self, iGameTurn ):
		# Food counter
		iFood = pKiev.getUHVCounter( 2 ) + pKiev.calculateTotalYield(YieldTypes.YIELD_FOOD)
		pKiev.setUHVCounter( 2, iFood )

		# UHV1: Orthodox buildings
		if ( iGameTurn == xml.i1250AD+1 and pKiev.getUHV( 0 ) == -1 ):
			pKiev.setUHV( 0, 0 )

		# UHV2: Conquer 10 provinces
		if ( iGameTurn == xml.i1288AD and pKiev.getUHV( 1 ) == -1 ):
			iConq = 0
			for iProv in tKievControl:
				if ( pKiev.getProvinceCurrentState( iProv ) >= con.iProvinceConquer ):
					iConq += 1
			if ( iConq > 9 ):
				pKiev.setUHV( 1, 1 )
			else:
				pKiev.setUHV( 1, 0 )

		# UHV3: 20000 food
		if ( iGameTurn <= xml.i1300AD and pKiev.getUHV( 2 ) == -1 ):
			if ( iFood > 20000 ):
				pKiev.setUHV( 2, 1 )
			elif ( iGameTurn == xml.i1300AD ):
				pKiev.setUHV( 2, 0 )


	def checkHungary( self, iGameTurn ):

		# UHV1: No Ottoman cities in Europe
		if ( iGameTurn == xml.i1444AD and pHungary.getUHV( 0 ) == -1 ):
			bClean = True
			if ( pTurkey.isAlive() ):
				for iProv in tHungarynControl:
					if ( pTurkey.getProvinceCityCount( iProv ) > 0):
						bClean = False
						break
			if ( bClean ):
				pHungary.setUHV( 0, 1 )
			else:
				pHungary.setUHV( 0, 0 )

		# UHV2: Biggest country in Europe
		if ( iGameTurn == xml.i1490AD and pHungary.getUHV( 1 ) == -1 ):
			if ( gc.controlMostTeritory( iHungary, tHugeHungaryControl[0], tHugeHungaryControl[1], tHugeHungaryControl[2], tHugeHungaryControl[3] ) ):
				pHungary.setUHV( 1, 1 )
			else:
				pHungary.setUHV( 1, 0 )

		# UHV3: Free Religion
		if ( pHungary.getUHV( 2 ) == -1 ):
			iCivic = pHungary.getCivics(4)
			if ( iCivic == 24 ):
				pHungary.setUHV( 2, 1 )
			else:
				for iPlayer in range( iNumMajorPlayers ):
					pPlayer = gc.getPlayer( iPlayer )
					if ( pPlayer.isAlive() and pPlayer.getCivics(4) == 24 ):
						pHungary.setUHV( 2, 0 )


	def checkSpain( self, iGameTurn ):

		# UHV1: Reconquista (no muslims in Iberia)
		if ( iGameTurn == xml.i1492AD and pSpain.getUHV( 0 ) == -1 ):
			bConverted = True
			for iProv in tSpainConvert:
				if ( not ( pSpain.provinceIsConvertReligion( iProv, xml.iCatholicism ) ) ):
					bConverted = False
					break
			if ( bConverted ):
				pSpain.setUHV( 0, 1 )
			else:
				pSpain.setUHV( 0, 0 )

		# UHV2: Have more Colonies than any other nation in 1588AD (while having at least 3)
		if ( iGameTurn == xml.i1588AD and pSpain.getUHV( 1 ) == -1 ):
			bMost = True
			iSpainColonies = self.getNumRealColonies(iSpain)
			for iPlayer in range( iNumPlayers ):
				if ( iPlayer != iSpain ):
					pPlayer = gc.getPlayer( iPlayer )
					if ( pPlayer.isAlive() and self.getNumRealColonies(iPlayer) >= iSpainColonies ):
						bMost = False
			if ( bMost and iSpainColonies >= 3 ):
				pSpain.setUHV( 1, 1 )
			else:
				pSpain.setUHV( 1, 0 )

		# UHV3: catholic lands/population superior
		if ( iGameTurn == xml.i1648AD and pSpain.getUHV( 2 ) == -1 ):
			lLand = [ 0, 0, 0, 0, 0, 0 ] # Prot, Islam, Cath, Orth, Jew, Pagan
			lPop  = [ 0, 0, 0, 0, 0, 0 ]
			for iPlayer in range( iNumPlayers ):
				pPlayer = gc.getPlayer( iPlayer )
				iStateReligion = pPlayer.getStateReligion()
				if ( iStateReligion > -1 ):
					lLand[ iStateReligion ] += pPlayer.getTotalLand()
					lPop[ iStateReligion ] += pPlayer.getTotalPopulation()
				else:
					lLand[ 5 ] += pPlayer.getTotalLand()
					lPop[ 5 ] += pPlayer.getTotalPopulation()

			iCathLand = lLand[ xml.iCatholicism ]
			iCathPop  = lPop[ xml.iCatholicism ]

			bWon = True

			for iReligion in range( xml.iNumReligions + 1 ):
				if ( iReligion != xml.iCatholicism ):
					if ( lLand[ iReligion ] > iCathLand ):
						bWon = False
					if ( lPop[ iReligion ] > iCathPop ):
						bWon = False

			if ( pSpain.getStateReligion() == xml.iCatholicism and bWon ):
				pSpain.setUHV( 2, 1 )
			else:
				pSpain.setUHV( 2, 0 )


	def checkScotland( self, iGameTurn ):

		# UHV1: Have 10 Forts and 4 Castles in 1296.
		if ( iGameTurn == xml.i1296AD ):
			iForts = pScotland.getImprovementCount( xml.iImprovementFort )
			iCastles = pScotland.countNumBuildings( xml.iCastle )
			print("Forts:",iForts,"Castles:",iCastles)
			if( iForts >= 10 and iCastles >= 4 ):
				pScotland.setUHV( 0, 1 )
			else:
				pScotland.setUHV( 0, 0 )

		# UHV2: Have 1000 attitude points with France by 1560. Attitude points go up every turn depending on relations
		if ( iGameTurn <= xml.i1560AD and pFrankia.isAlive()):
			# -2 for Furious -1 for Annoyed 0 for Cautious 1 for Pleased 2 for Friendly
			iScore = pFrankia.AI_getAttitude(iScotland) - 2
			# Agreements
			if(teamFrankia.isOpenBorders(iScotland)):
				iScore+=1
			if(teamFrankia.isDefensivePact(iScotland)):
				iScore+=2
			# Imports/Exports
			iTrades = 0
			iTrades += pScotland.getNumTradeBonusImports(iFrankia)
			iTrades += pFrankia.getNumTradeBonusImports(iScotland)
			iScore += iTrades/3
			# Common Wars
			for iEnemy in xrange(0,iNumPlayers):
				if(iEnemy == iScotland or iEnemy == iFrankia):
					continue
				if(teamFrankia.isAtWar(iEnemy) and teamScotland.isAtWar(iEnemy)):
					iScore+=2
			# Being at war with France gives a big penalty (and no bonuses)!
			if(teamScotland.isAtWar(iFrankia)):
				iScore = -10
			# Different religion from France also gives a penalty
			if(pScotland.getStateReligion() != pFrankia.getStateReligion()):
				iScore -= 3
			iOldScore = pScotland.getUHVCounter(1)
			iNewScore = iOldScore + iScore
			pScotland.setUHVCounter(1, iNewScore)
			if(iNewScore >= 1000):
				pScotland.setUHV( 1, 1 )
		elif ( iGameTurn > xml.i1560AD and pScotland.getUHV( 1 ) == -1 ):
			pScotland.setUHV( 1, 0 )

		# UHV3: Control Scotland, The Isles, Ireland, Wales, Brittany and Galicia in 1700.
		if ( iGameTurn == xml.i1700AD and pScotland.getUHV( 2 ) == -1 ):
			bConq = True
			for iProv in tScotlandControl:
				if ( pScotland.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pScotland.setUHV( 2, 1 )
			else:
				pScotland.setUHV( 2, 0 )


	def checkPoland( self, iGameTurn ):
		# UHV 1: Food production between 1500 and 1520 AD
		if ((iGameTurn >= xml.i1500AD) and (iGameTurn <= xml.i1520AD) and pPoland.getUHV( 0 ) == -1 ):
			iAgriculturePolish = pPoland.calculateTotalYield(YieldTypes.YIELD_FOOD)
			bFood = True
			for iPlayer in range( iNumMajorPlayers ):
				if ( gc.getPlayer( iPlayer ).calculateTotalYield(YieldTypes.YIELD_FOOD ) > iAgriculturePolish ):
					bFood = False
			if (bFood):
				pPoland.setUHV( 0, 1 )
			elif ( iGameTurn == xml.i1520AD ):
				pPoland.setUHV( 0, 0 )
		# UHV 2: Control 12 cities in the given provinces in 1600 AD
		# Old UHVs:		Dont lose cities until 1772 AD or conquer Russia until 1772 AD
		#				Vassalize Russia, Germany and Austria
		if (iGameTurn == xml.i1600AD and pPoland.getUHV( 1 ) == -1 ):
			iNumCities = 0
			for iProv in tPolishControl:
				iNumCities += pPoland.getProvinceCityCount( iProv )
			if ( iNumCities >= 12 ):
				pPoland.setUHV( 1, 1 )
			else:
				pPoland.setUHV( 1, 0 )
#		# HHG: the code below was intended to recalculate UHV3 conditions if messed up - but currently it does nothing
#		# UHV 2: 3 Catholic, 3 Orthodox, 2 Protestant Cathedrals and 2 Jewish Quarters
#		if (pPoland.getUHV( 2 ) == -1 and pPoland.getNumCities() > 0):
#			iCathCath = 0
#			iOrthCath = 0
#			iProtCath = 0
#			iJewishQu = 0
#			apCityList = pPoland.getCityList()
#			for pCity in apCityList:
#				if ( iCathCath < 9 and pCity.hasBuilding( xml.iCatholicCathedral )):
#					iCathCath += 1
#				if ( iOrthCath < 9 and pCity.hasBuilding( xml.iOrthodoxCathedral )):
#					iOrthCath += 1
#				if ( iProtCath < 9 and pCity.hasBuilding( xml.iProtestantCathedral )):
#					iProtCath += 1
#				if ( pCity.hasBuilding( xml.iKazimierz )):
#					iJewishQu = 99
#				elif ( iJewishQu < 99 and pCity.hasBuilding( xml.iJewishQuarter )):
#					iJewishQu += 1
#			if ( iCathCath >= 3 and iOrthCath >= 3 and iProtCath >= 2 and iJewishQu >= 2 ):
#				pPoland.setUHV( 2, 1 )
#			iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
#			pPoland.setUHVCounter( 2, iCounter )


	def checkGenoa( self, iGameTurn ):
		if ( iGameTurn == xml.i1566AD and pGenoa.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tGenoaControl:
				if ( pGenoa.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pGenoa.setUHV( 0, 1 )
			else:
				pGenoa.setUHV( 0, 0 )

		if ( iGameTurn == xml.i1640AD and pGenoa.getUHV( 2 ) == -1 ):
			iGenoaTrade = iImports = pGenoa.calculateTotalImports(YieldTypes.YIELD_COMMERCE) + pGenoa.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
			bLargest = True
			for iPlayer in range( iNumMajorPlayers ):
				if ( iPlayer != iGenoa ):
					pPlayer = gc.getPlayer(iPlayer)
					if ( pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE) + pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE) > iGenoaTrade ):
						bLargest = False
						break
			if ( bLargest ):
				pGenoa.setUHV( 2, 1 )
			else:
				pGenoa.setUHV( 2, 0 )

	def checkMorocco( self, iGameTurn ):
		# UHV 1: Control Morocco, Marrakesh, Fez, Tetouan, Oran, Algiers, Ifriqiya, Tripolitania, Andalusia, and Valencia in 1227AD.
		if (iGameTurn == xml.i1227AD and pMorocco.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tMoroccoControl:
				if ( pMorocco.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pMorocco.setUHV( 0, 1 )
			else:
				pMorocco.setUHV( 0, 0 )

		# UHV 2: Have 5000 culture in each of three cities in 1465AD.
		if (iGameTurn == xml.i1465AD and pMorocco.getUHV( 1 ) == -1):
			iGoodCities = 0
			apCityList = PyPlayer(iMorocco).getCityList()
			for pLoopCity in apCityList:
				pCity = pLoopCity.GetCy()
				if(pCity.getCulture(iMorocco) >= 5000):
					iGoodCities += 1;

			if(iGoodCities >= 3):
				pMorocco.setUHV( 1, 1 )
			else:
				pMorocco.setUHV( 1, 0 )

		# UHV 3: Collapse or vassalize Portugal, Spain, and Aragon by 1578AD.
		if (iGameTurn >= xml.i1164AD and iGameTurn <= xml.i1578AD and pMorocco.getUHV( 2 ) == -1):
			bConq = True
			if ( pSpain.isAlive() and (not teamSpain.isVassal( teamMorocco.getID() )) ):
				bConq = False
			elif ( pPortugal.isAlive() and (not teamPortugal.isVassal( teamMorocco.getID() )) ):
				bConq = False
			elif ( pAragon.isAlive() and (not teamAragon.isVassal( teamMorocco.getID() )) ):
				bConq = False

			if( bConq ):
				pMorocco.setUHV( 2, 1 )
		elif (iGameTurn > xml.i1578AD and pMorocco.getUHV( 2 ) == -1):
			pMorocco.setUHV( 2, 0 )


	def checkEngland( self, iGameTurn ):

		# UHV1: Conquer London, Wessex, East Anglia, Mercia, Northumbria, Scotland, Wales, Ireland, Normandy, Picardy, Bretagne, Il-de-France, Aquitania and Orleans in 1452AD
		if ( iGameTurn == xml.i1452AD and pEngland.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tEnglandControl:
				if ( pEngland.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pEngland.setUHV( 0, 1 )
			else:
				pEngland.setUHV( 0, 0 )

		# UHV2: Build 7 Colonies
		# handled in the onProjectBuilt function

		# UHV3: Be the first to enter the Industrial age
		pass


	def checkPortugal( self, iGameTurn ):
		if ( iGameTurn == xml.i1640AD and pPortugal.getUHV( 1 ) == -1 ):
			pPortugal.setUHV( 1, 1 )

		# UHV3: Build 5 Colonies
		# handled in the onProjectBuilt function


	def checkAragon( self, iGameTurn ):

		# UHV 1: Control Catalonia, Valencia, Baleares and Sicily in 1282AD.
		if ( iGameTurn == xml.i1282AD and pAragon.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tAragonControlI:
				if ( pAragon.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pAragon.setUHV( 0, 1 )
			else:
				pAragon.setUHV( 0, 0 )

		# UHV 2: Have 12 seaports in 1444AD.
		if ( iGameTurn == xml.i1444AD ):
			iPorts = pAragon.countNumBuildings(xml.iAragonSeaport)
			print("Ports:",iPorts)
			if( iPorts >= 12  ):
				pAragon.setUHV( 1, 1 )
			else:
				pAragon.setUHV( 1, 0 )

		# UHV 3: Control Catalonia, Valencia, Aragon, Baleares, Corsica, Sardinia, Sicily, Apulia, Provence and Thessaly in 1474AD.
		if ( iGameTurn == xml.i1474AD and pAragon.getUHV( 2 ) == -1 ):
			bConq = True
			for iProv in tAragonControlII:
				if ( pAragon.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pAragon.setUHV( 2, 1 )
			else:
				pAragon.setUHV( 2, 0 )


	def checkPrussia( self, iGameTurn ):
		# UHV 1: Control Lithuania, Livonia, Estonia, and Pomerania in 1410AD.
		if ( iGameTurn == xml.i1410AD and pPrussia.getUHV( 0 ) == -1 ):
			bOwn = True
			for iProv in tPrussiaControlI:
				if ( pPrussia.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pPrussia.setUHV( 0, 1 )
			else:
				pPrussia.setUHV( 0, 0 )

		# UHV 2: Conquer two cities from each of Austria, Muscowy, Germany, Sweden, France and Spain between 1650AD and 1763AD, if they are still alive
		# Controlled in the onCityAcquired function
		if(iGameTurn > xml.i1763AD and pPrussia.getUHV(1) == -1):
			pPrussia.setUHV(1,0)

		# UHV 3: Settle a total of 15 Great People in your capital
		if (pPrussia.getUHV(2) == - 1):
			pCapital = pPrussia.getCapitalCity()
			iGPStart = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_PRIEST")
			iGPEnd = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_SPY")
			iGPeople = 0
			for iType in range(iGPStart, iGPEnd+1):
				iGPeople += pCapital.getFreeSpecialistCount(iType)
			if(iGPeople >= 15):
				pPrussia.setUHV( 2, 1 )

	def checkLithuania( self, iGameTurn ):
		iCulture = pLithuania.getUHVCounter(0) + pLithuania.countCultureProduced() # 3Miro: testing, move it below later
		pLithuania.setUHVCounter(0, iCulture)
		if ( iGameTurn <= xml.i1386AD and pLithuania.getUHV( 0 ) == -1 ):
			if ( pLithuania.getStateReligion() != -1 ):
				pLithuania.setUHV( 0, 0 )
			elif ( iCulture >= 2000 ):
				pLithuania.setUHV( 0, 1 )
			elif ( iGameTurn == xml.i1386AD ):
				pLithuania.setUHV( 0, 0 )

		if ( iGameTurn == xml.i1569AD and pLithuania.getUHV( 1 ) == -1 ):
			if ( pLithuania.getNumCities() >= 18 ):
				pLithuania.setUHV( 1, 1 )
			else:
				pLithuania.setUHV( 1, 0 )

		if ( pLithuania.getUHV( 2 ) == -1 ):
			if ( pMoscow.isAlive() and teamMoscow.isVassal( teamLithuania.getID() ) ):
				pLithuania.setUHV( 2, 1 )
			elif ( (iGameTurn > xml.i1401AD) and (pLithuania.getProvinceCurrentState( xml.iP_Moscow ) >= con.iProvinceConquer) ):
				pLithuania.setUHV( 2, 1 )

	def checkAustria( self, iGameTurn ):
		if ( iGameTurn == xml.i1617AD and pAustria.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tAustriaControl:
				if ( pAustria.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pAustria.setUHV( 0, 1 )
			else:
				pAustria.setUHV( 0, 0 )

		if ( iGameTurn == xml.i1700AD and pAustria.getUHV( 1 ) == -1 ):
			iCount = 0
			for iPlayer in range( iNumMajorPlayers ):
				pPlayer = gc.getPlayer( iPlayer )
				if ( iPlayer != iAustria and pPlayer.isAlive() ):
					if ( gc.getTeam( pPlayer.getTeam() ).isVassal( iAustria ) ):
						iCount += 1

			if ( iCount >= 3 ):
				 pAustria.setUHV( 1, 1 )
			else:
				 pAustria.setUHV( 1, 0 )

		if ( iGameTurn == xml.i1780AD and pAustria.getUHV( 2 ) == -1 ):
			if ( gc.getGame().getTeamRank(iAustria) == 0 ):
				 pAustria.setUHV( 2, 1 )
			else:
				 pAustria.setUHV( 2, 0 )

	def checkTurkey( self, iGameTurn ):
		# UHV 1: Conquer the Balkans (1453)
		if ( iGameTurn == xml.i1453AD and pTurkey.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tOttomanControlI:
				if ( pTurkey.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pTurkey.setUHV( 0, 1 )
			else:
				pTurkey.setUHV( 0, 0 )
		# UHV 2: Conquer the Middle East (1517)
		if ( iGameTurn == xml.i1517AD and pTurkey.getUHV( 1 ) == -1 ):
			bConq = True
			for iProv in tOttomanControlII:
				if ( pTurkey.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pTurkey.setUHV( 1, 1 )
			else:
				pTurkey.setUHV( 1, 0 )
		# UHV 3: Conquer Austria (1683)
		if ( iGameTurn <= xml.i1683AD and pTurkey.getUHV( 2 ) == -1 ):
			bConq = True
			for iProv in tOttomanControlIII:
				if ( pTurkey.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pTurkey.setUHV( 2, 1 )
			elif ( iGameTurn == xml.i1683AD ):
				pTurkey.setUHV( 2, 0 )

	def checkMoscow( self, iGameTurn ):
		# UHV 1: Free eastern Europe from the Mongols
		if ( iGameTurn == xml.i1482AD and pMoscow.getUHV( 0 ) == -1 ):
			bClean = True
			for iProv in tMoscowControl:
				if ( pBarbarian.getProvinceCityCount( iProv ) > 0):
					bClean = False
					break
			if ( bClean ):
				pMoscow.setUHV( 0, 1 )
			else:
				pMoscow.setUHV( 0, 0 )
		# UHV 2: Get 20% land
		if ( pMoscow.getUHV( 1 ) == -1 ):
			totalLand = gc.getMap().getLandPlots()
			RussianLand = pMoscow.getTotalLand()
			if (totalLand > 0):
				landPercent = (RussianLand * 100.0) / totalLand
			else:
				landPercent = 0.0
			#print(" RUSSIAUHV: ",totalLand,RussianLand,landPercent)
			if ( landPercent >= 20 ):
				pMoscow.setUHV( 1, 1 )
		# UHV 3: Get into warm waters
		if ( pMoscow.getUHV( 2 ) == -1 ):
			if ( pMoscow.countOwnedBonuses( xml.iAccess ) > 0 ):
				pMoscow.setUHV( 2, 1 )
			elif ( gc.getMap().plot( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ).getPlotCity().getOwner() == iMoscow ):
				pMoscow.setUHV( 2, 1 )

	def checkSweden( self, iGameTurn ):
		# UHV 1: Have six cities in Norrland, Osterland and Karelia in 1323.
		if ( iGameTurn == xml.i1323AD and pSweden.getUHV( 0 ) == -1 ):
			iNumCities = 0
			for iProv in tSwedenControl:
				iNumCities += pSweden.getProvinceCityCount(iProv)
			if ( iNumCities >= 6 ):
				pSweden.setUHV(0,1)
			else:
				pSweden.setUHV(0,0)

		# UHV 2: Raze 5 Catholic cities while being Protestant by 1660.
		if ( iGameTurn == xml.i1660AD and pSweden.getUHV( 1 ) == -1 ):
			pSweden.setUHV(1,0)

		# UHV 3: Control every coastal city on the Baltic in 1750.
		if (iGameTurn == xml.i1750AD):
			if(up.getNumForeignCitiesOnBaltic(iSweden, True) > 0):
				pSweden.setUHV(2,0)
			else:
				pSweden.setUHV(2,1)

		# Old UHV set:
		## UHV 1: Conquer Gotaland, Svealand, Norrland, Skaneland, Gotland and Osterland in 1600AD
		#if ( iGameTurn == xml.i1600AD and pSweden.getUHV( 0 ) == -1 ):
		#	bConq = True
		#	for iProv in tSwedenControlI:
		#		if ( pSweden.getProvinceCurrentState( iProv ) < con.iProvinceConquer ):
		#			bConq = False
		#			break
		#	if ( bConq ):
		#		pSweden.setUHV( 0, 1 )
		#	else:
		#		pSweden.setUHV( 0, 0 )

		## UHV 2: Don't lose any cities to Poland, Lithuania or Russia before 1700AD
		#if ( iGameTurn == xml.i1700AD and pSweden.getUHV( 1 ) == -1 ):
		#	pSweden.setUHV( 1, 1 )

		## UHV 3: Have 15 cities in Saxony, Brandenburg, Holstein, Pomerania, Prussia, Greater Poland, Masovia, Suvalkija, Lithuania, Livonia, Estonia, Smolensk, Polotsk, Minsk, Murom, Chernigov, Moscow, Novgorod and Rostov in 1750AD
		#if (iGameTurn == xml.i1750AD and pSweden.getUHV( 2 ) == -1 ): #Really 1600
		#	iNumCities = 0
		#	for iProv in tSwedenControlII:
		#		iNumCities += pSweden.getProvinceCityCount( iProv )
		#	if ( iNumCities >= 15 ):
		#		pSweden.setUHV( 2, 1 )
		#	else:
		#		pSweden.setUHV( 2, 0 )

	def checkDutch( self, iGameTurn ):
		if ( iGameTurn <= xml.i1750AD and pDutch.getUHV( 0 ) == -1 ):
			pPlot = gc.getMap().plot( con.tCapitals[iDutch][0], con.tCapitals[iDutch][1])
			if ( pPlot.isCity() ):
				iGMerchant = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_MERCHANT")
				if ( pPlot.getPlotCity().getFreeSpecialistCount(iGMerchant) >= 5 ):
					pDutch.setUHV( 0, 1 )
		else:
			if ( pDutch.getUHV( 0 ) == -1 ):
				pDutch.setUHV( 0, 0 )

		# UHV 2: Build 3 Colonies and complete both Trading Companies
		# handled in the onProjectBuilt function

		if ( pDutch.getUHV( 2 ) == -1 ):
			iGold = pDutch.getGold()
			bMost = True
			for iCiv in range( iNumPlayers ):
				if ( iCiv != iDutch and gc.getPlayer( iCiv ).isAlive() ):
					if (gc.getPlayer(iCiv).getGold() > iGold):
						bMost = False
			if ( bMost ):
				 pDutch.setUHV( 2, 1 )


	def getNumRealColonies(self, iPlayer):
		tPlayer = gc.getTeam(iPlayer)
		iCount = 0
		for iProject in range(xml.iNumProjects):
			if iProject in [xml.iEncyclopedie, xml.iEastIndiaCompany, xml.iWestIndiaCompany]: continue
			if tPlayer.getProjectCount(iProject) > 0:
				iCount += 1
		return iCount

