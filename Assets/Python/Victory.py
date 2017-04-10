# Rhye's and Fall of Civilization: Europe - Historical Victory Goals

from CvPythonExtensions import *
import PyHelpers
import Popup
import Consts as con
import XMLConsts as xml
import RFCUtils
import Crusades as cru
import UniquePowers
import RFCEMaps as rfcemaps
from StoredData import sd

# Globals
utils = RFCUtils.RFCUtils()
up = UniquePowers.UniquePowers()
gc = CyGlobalContext()
localText = CyTranslator() #Absinthe
PyPlayer = PyHelpers.PyPlayer

# Constants
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
tFrankControl = [ xml.iP_Swabia, xml.iP_Saxony, xml.iP_Lorraine, xml.iP_IleDeFrance, xml.iP_Normandy, xml.iP_Picardy, xml.iP_Aquitania, xml.iP_Provence, xml.iP_Burgundy, xml.iP_Orleans, xml.iP_Champagne, xml.iP_Catalonia, xml.iP_Lombardy, xml.iP_Tuscany ]
tArabiaControlI = [ xml.iP_Egypt, xml.iP_Antiochia, xml.iP_Syria, xml.iP_Lebanon, xml.iP_Arabia, xml.iP_Jerusalem ]
tArabiaControlII = [ xml.iP_Oran, xml.iP_Algiers, xml.iP_Ifriqiya, xml.iP_Cyrenaica, xml.iP_Tripolitania, xml.iP_Egypt, xml.iP_Antiochia, xml.iP_Syria, xml.iP_Lebanon, xml.iP_Arabia, xml.iP_Jerusalem]
tBulgariaControl = [ xml.iP_Constantinople, xml.iP_Thessaloniki, xml.iP_Serbia, xml.iP_Thrace, xml.iP_Macedonia, xml.iP_Moesia, xml.iP_Arberia ]
tCordobaWonders = [ xml.iAlhambra, xml.iLaMezquita, xml.iGardensAlAndalus ]
tCordobaIslamize = [ xml.iP_GaliciaSpain, xml.iP_Castile, xml.iP_Leon, xml.iP_Lusitania, xml.iP_Catalonia, xml.iP_Aragon, xml.iP_Navarre, xml.iP_Valencia, xml.iP_LaMancha, xml.iP_Andalusia ]
tNorwayControl = [xml.iP_TheIsles, xml.iP_Ireland, xml.iP_Scotland, xml.iP_Normandy, xml.iP_Sicily, xml.iP_Apulia, xml.iP_Calabria, xml.iP_Iceland]
tNorwayOutrank = [ iSweden, iDenmark, iScotland, iEngland, iGermany, iFrankia ]
#tNorseControl = [ xml.iP_Sicily, xml.iP_Iceland, xml.iP_Northumbria, xml.iP_Scotland, xml.iP_Normandy, xml.iP_Ireland, xml.iP_Novgorod ]
tVenetianControl = [ xml.iP_Epirus, xml.iP_Dalmatia, xml.iP_Verona, xml.iP_Arberia ]
tVenetianControlII = [ xml.iP_Thessaly, xml.iP_Morea, xml.iP_Crete, xml.iP_Cyprus ]
tBurgundyControl = [ xml.iP_Flanders, xml.iP_Picardy, xml.iP_Provence, xml.iP_Burgundy, xml.iP_Champagne, xml.iP_Lorraine ]
tBurgundyOutrank = [ iFrankia, iEngland, iGermany ]
tGermanyControl = [ xml.iP_Tuscany, xml.iP_Lombardy, xml.iP_Lorraine, xml.iP_Swabia, xml.iP_Saxony, xml.iP_Bavaria, xml.iP_Franconia, xml.iP_Brandenburg, xml.iP_Holstein ]
tGermanyControlII = [ xml.iP_Austria, xml.iP_Flanders, xml.iP_Pomerania, xml.iP_Silesia, xml.iP_Bohemia, xml.iP_Moravia, xml.iP_Swabia, xml.iP_Saxony, xml.iP_Bavaria, xml.iP_Franconia, xml.iP_Brandenburg, xml.iP_Holstein ]
tKievControl = [ xml.iP_Kiev, xml.iP_Podolia, xml.iP_Pereyaslavl, xml.iP_Sloboda, xml.iP_Chernigov, xml.iP_Volhynia, xml.iP_Minsk, xml.iP_Polotsk, xml.iP_Smolensk, xml.iP_Moscow, xml.iP_Murom, xml.iP_Rostov, xml.iP_Novgorod, xml.iP_Vologda ]
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
tMoroccoControl = [ xml.iP_Morocco, xml.iP_Marrakesh, xml.iP_Fez, xml.iP_Tetouan, xml.iP_Oran, xml.iP_Algiers, xml.iP_Ifriqiya, xml.iP_Andalusia, xml.iP_Valencia, xml.iP_Balears ]
tAragonControlI = [ xml.iP_Catalonia, xml.iP_Valencia, xml.iP_Balears, xml.iP_Sicily ]
tAragonControlII = [ xml.iP_Catalonia, xml.iP_Valencia, xml.iP_Aragon, xml.iP_Balears, xml.iP_Corsica, xml.iP_Sardinia, xml.iP_Sicily, xml.iP_Calabria, xml.iP_Apulia, xml.iP_Provence, xml.iP_Thessaly ]
tPrussiaControlI = [ xml.iP_Lithuania, xml.iP_Suvalkija, xml.iP_Livonia, xml.iP_Estonia, xml.iP_Pomerania, xml.iP_Prussia]
tPrussiaDefeat = [ iAustria, iMoscow, iGermany, iSweden, iFrankia, iSpain ]
tScotlandControl = [ xml.iP_Scotland, xml.iP_TheIsles, xml.iP_Ireland, xml.iP_Wales, xml.iP_Bretagne ]
tDenmarkControlI = [ xml.iP_Denmark, xml.iP_Skaneland, xml.iP_Gotaland, xml.iP_Svealand, xml.iP_Mercia, xml.iP_London, xml.iP_EastAnglia, xml.iP_Northumbria ]
#tDenmarkControlII = [ xml.iP_Brandenburg, xml.iP_Pomerania, xml.iP_Estonia ]
tDenmarkControlIII = [ xml.iP_Denmark, xml.iP_Norway, xml.iP_Vestfold, xml.iP_Skaneland, xml.iP_Gotaland, xml.iP_Svealand, xml.iP_Norrland, xml.iP_Gotland, xml.iP_Osterland, xml.iP_Estonia, xml.iP_Iceland ]

#tHugeHungaryControl = ( 0, 23, 99, 72 )
totalLand = gc.getMap().getLandPlots()

iCathegoryExpansion = con.iCathegoryExpansion

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

	def setup( self ):
		# ignore AI goals
		bIgnoreAI = (gc.getDefineINT("NO_AI_UHV_CHECKS") == 1)
		self.setIgnoreAI(bIgnoreAI)
		if bIgnoreAI:
			for iPlayer in range(iNumPlayers):
				if utils.getHumanID() != iPlayer:
					self.setAllUHVFailed(iPlayer)

	def isIgnoreAI(self):
		return sd.scriptDict['bIgnoreAIUHV']

	def setIgnoreAI(self, bVal):
		sd.scriptDict['bIgnoreAIUHV'] = bVal

#######################################
### Main methods (Event-Triggered) ###
#####################################

	def checkTurn(self, iGameTurn):
		pass


	def checkPlayerTurn(self, iGameTurn, iPlayer):
		# We use Python version of Switch statement, it is supposed to be better, now all condition checks are in separate functions
		pPlayer = gc.getPlayer(iPlayer)
		if iPlayer != utils.getHumanID() and self.isIgnoreAI():
			return
		if not gc.getGame().isVictoryValid(7): #7 == historical
			return
		if not pPlayer.isAlive():
			return
		if iPlayer >= iNumMajorPlayers - 1: # don't count the Pope
			return

		self.switchConditionsPerCiv[iPlayer](iGameTurn)

		# Generic checks:
		if not pPlayer.getUHV2of3():
			if utils.countAchievedGoals(iPlayer) == 2:
				#intermediate bonus
				pPlayer.setUHV2of3( True )
				if pPlayer.getNumCities() > 0: #this check is needed, otherwise game crashes
					capital = pPlayer.getCapitalCity()
					# 3Miro: Golden Age after 2/3 victories
					capital.setHasRealBuilding(xml.iTriumphalArch, True)
					if pPlayer.isHuman():
						CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_VICTORY_INTERMEDIATE", ()), "", 0, "", ColorTypes(con.iPurple), -1, -1, True, True)
						for iCiv in range(iNumPlayers):
							if iCiv != iPlayer:
								pCiv = gc.getPlayer(iCiv)
								if pCiv.isAlive():
									iAttitude = pCiv.AI_getAttitude(iPlayer)
									if iAttitude != 0:
										pCiv.AI_setAttitudeExtra(iPlayer, iAttitude-1)

						# Absinthe: maximum 3 of your rivals declare war on you
						lCivs = [iCiv for iCiv in range(iNumPlayers-1) if iCiv != iPlayer and gc.getPlayer(iCiv).isAlive()]
						iStartCivIndex = gc.getGame().getSorenRandNum(len(lCivs), 'first civ to check')
						iWarCounter = 0
						# starting at a random civ, we run through all available civs to check for potential wars
						for i in range( iStartCivIndex, len(lCivs) + iStartCivIndex ):
							iCiv = lCivs[i % len(lCivs)]
							pCiv = gc.getPlayer(iCiv)
							teamCiv = gc.getTeam(pCiv.getTeam())
							teamOwn = gc.getTeam(pPlayer.getTeam())
							if teamCiv != teamOwn:
								if pCiv.canContact(iPlayer) and pCiv.AI_getAttitude(iPlayer) < 2 and not teamCiv.isAtWar(iPlayer):
									teamCiv.declareWar(iPlayer, True, -1)
									iWarCounter += 1
									if (iWarCounter == 3):
										break
						if iWarCounter > 0:
							CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_VICTORY_RIVAL_CIVS", ()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)

		if gc.getGame().getWinner() == -1:
			if pPlayer.getUHV(0) == 1 and pPlayer.getUHV(1) == 1 and pPlayer.getUHV(2) == 1:
				gc.getGame().setWinner(iPlayer, 7) # Historical Victory


	def onCityBuilt(self, city, iPlayer): #see onCityBuilt in CvRFCEventHandler
		# Portugal UHV 1: Settle 3 cities on the Azores, Canaries and Madeira and 2 in Morocco, Tetouan and Oran
		if iPlayer == iPortugal:
			if self.isPossibleUHV(iPlayer, 0, False):
				iProv = city.getProvince()
				if iProv in tPortugalControlI or iProv in tPortugalControlII:
					iCounter = pPortugal.getUHVCounter( 0 )
					iIslands = iCounter % 100
					iAfrica = iCounter / 100
					if iProv in tPortugalControlI:
						iIslands += 1
					else:
						iAfrica += 1
					if iIslands >= 3 and iAfrica >= 2:
						self.wonUHV( iPortugal, 0 )
					pPortugal.setUHVCounter( 0, iAfrica * 100 + iIslands )


	def onReligionFounded(self, iReligion, iFounder):
		# Germany UHV 2: Start the Reformation (Found Protestantism)
		if iReligion == xml.iProtestantism:
			if iFounder == iGermany:
				self.wonUHV( iGermany, 1 )
			else:
				self.lostUHV( iGermany, 1 )


	def onCityAcquired(self, owner, iNewOwner, city, bConquest):
		if not gc.getGame().isVictoryValid(7): # Victory 7 == historical
			return

		iPlayer = owner
		iGameTurn = gc.getGame().getGameTurn()

		# Bulgaria UHV 3: Do not lose a city to barbarians (Mongols), Byzantines, or Ottomans before 1396
		if iPlayer == iBulgaria:
			if self.isPossibleUHV(iPlayer, 2, False):
				if iGameTurn <= xml.i1396AD:
					if iNewOwner in [iBarbarian, iTurkey, iByzantium]:
						self.lostUHV( iBulgaria, 2 )

		# Portugal UHV 2: Do not lose a city before 1640
		elif iPlayer == iPortugal:
			if self.isPossibleUHV(iPlayer, 1, False):
				if bConquest:
					self.lostUHV( iPortugal, 1 )

		# Norway UHV 1: Going Viking
		elif iNewOwner == iNorway:
			pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + city.getPopulation() )
			# Absinthe: city is already reduced by 1 on city conquest, so city.getPopulation() is one less than the original size (unless it was already 1)
			if bConquest: # note that if the size was 1 originally you get one extra point this way, but that's probably not a big issue
				pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + 1 )

		# Poland UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
		elif iNewOwner == iPoland:
			if self.isPossibleUHV(iNewOwner, 2, False):
				if city.hasBuilding( xml.iKazimierz ): # you cannot acquire religious buildings on conquest, only wonders
					iCounter = pPoland.getUHVCounter( 2 )
					iCathCath = ( iCounter / 10000 ) % 10
					iOrthCath = ( iCounter / 1000 ) % 10
					iProtCath = ( iCounter / 100 ) % 10
					iJewishQu = 99
					iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
					pPoland.setUHVCounter( 2, iCounter )
					if iCathCath >= 3 and iOrthCath >= 2 and iProtCath >= 2 and iJewishQu >= 2:
						self.wonUHV( iPoland, 2 )

		# Prussia UHV 2: Conquer two cities from each of Austria, Muscowy, Germany, Sweden, France and Spain between 1650 and 1763, if they are still alive
		elif iNewOwner == iPrussia:
			if self.isPossibleUHV(iNewOwner, 1, False):
				if owner in tPrussiaDefeat and xml.i1650AD <= iGameTurn <= xml.i1763AD:
					lNumConq = []
					iConqRaw = pPrussia.getUHVCounter(1)
					bConq = True
					for iI in range(len(tPrussiaDefeat)):
						lNumConq.append((iConqRaw / pow(10, iI)) % 10)
						if tPrussiaDefeat[iI] == owner:
							lNumConq[iI] += 1
							if lNumConq[iI] > 9:
								# Prevent overflow
								lNumConq[iI] = 9
						if lNumConq[iI] < 2 and gc.getPlayer(tPrussiaDefeat[iI]).isAlive():
							bConq = False

					if bConq:
						self.wonUHV( iPrussia, 1 )

					iConqRaw = 0
					for iI in range(len(tPrussiaDefeat)):
						iConqRaw += lNumConq[iI] * pow(10, iI)
					pPrussia.setUHVCounter(1, iConqRaw)


	def onCityRazed(self, iPlayer, city):
		# Sweden UHV 2: Raze 5 Catholic cities while being Protestant by 1660
		if iPlayer == iSweden:
			if self.isPossibleUHV(iPlayer, 1, False):
				if pSweden.getStateReligion() == xml.iProtestantism and city.isHasReligion(xml.iCatholicism):
					iRazed = pSweden.getUHVCounter(1)+1
					pSweden.setUHVCounter(1, iRazed)
					if iRazed >= 5:
						self.wonUHV( iSweden, 1 )


	def onPillageImprovement( self, iPillager, iVictim, iImprovement, iRoute, iX, iY ):
		# Norway UHV 1: Going Viking
		if iPillager == iNorway and iRoute == -1:
			if gc.getMap().plot( iX, iY ).getOwner() != iNorway:
				pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + 1 )


	def onCombatResult(self, argsList):
		pWinningUnit,pLosingUnit = argsList
		cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())

		# Norway UHV 1: Going Viking
		if pWinningUnit.getOwner() == iNorway:
			if cLosingUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
				# Absinthe: only 1 Viking point for Work Boats
				#print ("viking", pLosingUnit.getUnitType())
				if pLosingUnit.getUnitType() != xml.iWorkboat:
					pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + 2 )
				else:
					pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + 1 )


	def onTechAcquired(self, iTech, iPlayer):
		if not gc.getGame().isVictoryValid(7): #7 == historical
			return

		# England UHV 3: Be the first to enter the Industrial age
		if iTech == xml.iIndustrialTech:
			if self.isPossibleUHV(iEngland, 2, False):
				if iPlayer == iEngland:
					self.wonUHV( iEngland, 2 )
				else:
					self.lostUHV( iEngland, 2 )


	def onBuildingBuilt(self, iPlayer, iBuilding):
		if not gc.getGame().isVictoryValid(7): #7 == historical
			return

		iGameTurn = gc.getGame().getGameTurn()

		# Kiev UHV 1: Build 2 Orthodox cathedrals and 8 Orthodox monasteries by 1250
		if iPlayer == iKiev:
			if self.isPossibleUHV(iPlayer, 0, False):
				if iBuilding in [xml.iOrthodoxMonastery, xml.iOrthodoxCathedral]:
					iBuildSoFar = pKiev.getUHVCounter( 0 )
					iCathedralCounter = iBuildSoFar % 100
					iMonasteryCounter = iBuildSoFar / 100
					if iBuilding == xml.iOrthodoxMonastery:
						iMonasteryCounter += 1
					else:
						iCathedralCounter += 1
					if iCathedralCounter >= 2 and iMonasteryCounter >= 8:
						self.wonUHV( iKiev, 0 )
					pKiev.setUHVCounter( 0, 100 * iMonasteryCounter + iCathedralCounter )

		# Poland UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
		# HHG: Polish UHV3 now uses Wonder Kazimierz with maximum value 99, and all other buildings have boundary checks
		elif iPlayer == iPoland:
			if self.isPossibleUHV(iPlayer, 2, False):
				lBuildingList = [xml.iCatholicCathedral, xml.iOrthodoxCathedral, xml.iProtestantCathedral, xml.iJewishQuarter, xml.iKazimierz]
				if iBuilding in lBuildingList:
					iCounter = pPoland.getUHVCounter( 2 )
					iCathCath = ( iCounter / 10000 ) % 10
					iOrthCath = ( iCounter / 1000 ) % 10
					iProtCath = ( iCounter / 100 ) % 10
					iJewishQu = iCounter % 100
					if iBuilding == xml.iCatholicCathedral and iCathCath < 9:
						iCathCath += 1
					elif iBuilding == xml.iOrthodoxCathedral and iOrthCath < 9:
						iOrthCath += 1
					elif iBuilding == xml.iProtestantCathedral and iProtCath < 9:
						iProtCath += 1
					elif iBuilding == xml.iKazimierz:
						iJewishQu = 99
					elif iBuilding == xml.iJewishQuarter and iJewishQu < 99:
						iJewishQu += 1
					if iCathCath >= 3 and iOrthCath >= 3 and iProtCath >= 2 and iJewishQu >= 2:
						self.wonUHV( iPoland, 2 )
					iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
					pPoland.setUHVCounter( 2, iCounter )

		# Genoa UHV 2: Build 8 Banks
		elif iPlayer == iGenoa:
			if self.isPossibleUHV(iPlayer, 1, False):
				if iBuilding == xml.iGenoaBank:
					iBanks = pGenoa.getUHVCounter( 1 )
					iBanks += 1
					if iBanks >= 8:
						self.wonUHV( iGenoa, 1 )
					pGenoa.setUHVCounter( 1, iBanks )

		# Cordoba UHV 2: Build the Alhambra, the Gardens of Al-Andalus, and La Mezquita by 1309
		if iBuilding in tCordobaWonders:
			if self.isPossibleUHV(iCordoba, 1, False):
				if iPlayer == iCordoba:
					iWondersBuilt = pCordoba.getUHVCounter( 1 )
					pCordoba.setUHVCounter( 1, iWondersBuilt + 1 )
					if iWondersBuilt == 2: # so we already had 2 wonders
						self.wonUHV( iCordoba, 1 )
				else:
					self.lostUHV( iCordoba, 1 )


	def onProjectBuilt(self, iPlayer, iProject):
		bColony = self.isProjectAColony( iProject )
		# Absinthe: note that getProjectCount (thus getNumRealColonies too) won't count the latest project/colony (which is currently buing built) if called from this function
		#			way more straightforward, and also faster to use the UHVCounters for the UHV checks

		# Venice UHV 3: Be the first to build a Colony from the Age of Discovery (Vinland is from the Viking Age)
		if self.isPossibleUHV(iVenecia, 2, False):
			if iProject != xml.iColVinland:
				if bColony:
					if iPlayer == iVenecia:
						self.wonUHV( iVenecia, 2 )
					else:
						self.lostUHV( iVenecia, 2 )

		# France UHV 3: Build 5 Colonies
		if iPlayer == iFrankia:
			if self.isPossibleUHV(iPlayer, 2, False):
				if bColony:
					pFrankia.setUHVCounter( 2, pFrankia.getUHVCounter( 2 ) + 1 )
					if pFrankia.getUHVCounter( 2 ) >= 5:
						self.wonUHV( iFrankia, 2 )

		# England UHV 2: Build 7 Colonies
		elif iPlayer == iEngland:
			if self.isPossibleUHV(iPlayer, 1, False):
				if bColony:
					pEngland.setUHVCounter( 1, pEngland.getUHVCounter( 1 ) + 1 )
					if pEngland.getUHVCounter( 1 ) >= 7:
						self.wonUHV( iEngland, 1 )

		# Spain UHV 2: Have more Colonies than any other nation in 1588 (while having at least 3)
		# this is only for the Main Screen counter
		elif iPlayer == iSpain:
			pSpain.setUHVCounter( 1, pSpain.getUHVCounter( 1 ) + 1 )

		# Portugal UHV 3: Build 5 Colonies
		elif iPlayer == iPortugal:
			if self.isPossibleUHV(iPlayer, 2, False):
				if bColony:
					pPortugal.setUHVCounter( 2, pPortugal.getUHVCounter( 2 ) + 1 )
					if pPortugal.getUHVCounter( 2 ) >= 5:
						self.wonUHV( iPortugal, 2 )

		# Dutch UHV 2: Build 3 Colonies and complete both Trading Companies
		elif iPlayer == iDutch:
			if self.isPossibleUHV(iPlayer, 1, False):
				if bColony:
					pDutch.setUHVCounter( 1, pDutch.getUHVCounter( 1 ) + 1 )
				if pDutch.getUHVCounter( 1 ) >= 3:
					iWestCompany = teamDutch.getProjectCount(xml.iWestIndiaCompany)
					iEastCompany = teamDutch.getProjectCount(xml.iEastIndiaCompany)
					# if the companies are already built previously, or currently being built (one of them is the current project)
					if iProject == xml.iWestIndiaCompany or iWestCompany >= 1:
						if iProject == xml.iEastIndiaCompany or iEastCompany >= 1:
							self.wonUHV( iDutch, 1 )

		# Denmark UHV 3: Build 3 Colonies and complete both Trading Companies
		elif iPlayer == iDenmark:
			if self.isPossibleUHV(iPlayer, 2, False):
				if bColony:
					pDenmark.setUHVCounter( 2, pDenmark.getUHVCounter( 2 ) + 1 )
				if pDenmark.getUHVCounter( 2 ) >= 3:
					iWestCompany = teamDenmark.getProjectCount(xml.iWestIndiaCompany)
					iEastCompany = teamDenmark.getProjectCount(xml.iEastIndiaCompany)
					# if the companies are already built previously, or currently being built (one of them is the current project)
					if iProject == xml.iWestIndiaCompany or iWestCompany == 1:
						if iProject == xml.iEastIndiaCompany or iEastCompany == 1:
							self.wonUHV( iDenmark, 2 )


	def getOwnedLuxes( self, pPlayer ):
		lBonus = [xml.iSheep, xml.iDye, xml.iFur, xml.iGems, xml.iGold, xml.iIncense, xml.iIvory,
			xml.iSilk, xml.iSilver, xml.iSpices, xml.iWine, xml.iHoney, xml.iWhale, xml.iAmber,
			xml.iCotton, xml.iCoffee, xml.iTea, xml.iTobacco]
		iCount = 0
		for iBonus in lBonus:
			iCount += pPlayer.countOwnedBonuses(iBonus)
		return iCount


	def getOwnedGrain( self, pPlayer ):
		iCount = 0
		iCount += pPlayer.countOwnedBonuses( xml.iWheat )
		iCount += pPlayer.countOwnedBonuses( xml.iBarley )
		return iCount


	def isProjectAColony( self, iProject ):
		if iProject >= xml.iNumNotColonies:
			return True
		else:
			return False


	def getNumRealColonies(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		tPlayer = gc.getTeam(pPlayer.getTeam())
		iCount = 0
		for iProject in range( xml.iNumNotColonies, xml.iNumProjects ):
			if tPlayer.getProjectCount(iProject) > 0:
				iCount += 1
		return iCount


	def getTerritoryPercentEurope(self, iPlayer, bReturnTotal = False):
		iTotal = 0
		iCount = 0
		for (x, y) in utils.getWorldPlotsList():
			plot = gc.getMap().plot(x,y)
			if plot.isWater(): continue
			iProvinceID = rfcemaps.tProvinceMap[y][x]
			if iProvinceID in xml.lNotEurope: continue
			iTotal += 1
			if plot.getOwner() == iPlayer:
				iCount += 1
		if bReturnTotal:
			return iCount, iTotal
		return iCount


	def checkByzantium( self, iGameTurn ):

		# UHV 1: Make Constantinople the largest and most cultured city in 1025
		if iGameTurn == xml.i1025AD:
			if self.isPossibleUHV(iByzantium, 0, True):
				x, y = con.tCapitals[iByzantium]
				if gc.isLargestCity( x, y ) and gc.isTopCultureCity( x, y ) and gc.getMap().plot( x, y ).getPlotCity().getOwner() == iByzantium:
					self.wonUHV( iByzantium, 0 )
				else:
					self.lostUHV( iByzantium, 0 )

		# UHV 2: Control Constantinople, Thrace, Thessaloniki, Moesia, Macedonia, Serbia, Arberia, Epirus, Thessaly, Morea, Colonea, Antiochia, Charsianon, Cilicia, Armeniakon, Anatolikon, Paphlagonia, Thrakesion and Opsikion in 1282
		elif iGameTurn == xml.i1282AD:
			if self.isPossibleUHV(iByzantium, 1, True):
				if self.checkProvincesStates(iByzantium, tByzantumControl):
					self.wonUHV( iByzantium, 1 )
				else:
					self.lostUHV( iByzantium, 1 )

		# UHV 3: Be the richest empire in the world in 1453
		elif iGameTurn == xml.i1453AD:
			if self.isPossibleUHV(iByzantium, 2, True):
				iGold = pByzantium.getGold()
				bMost = True
				for iCiv in range( iNumPlayers ):
					if iCiv != iByzantium and gc.getPlayer( iCiv ).isAlive():
						if gc.getPlayer(iCiv).getGold() > iGold:
							bMost = False
							break
				if bMost:
					self.wonUHV( iByzantium, 2 )
				else:
					self.lostUHV( iByzantium, 2 )


	def checkFrankia( self, iGameTurn ):

		# UHV 1: Achieve Charlemagne's Empire by 840
		if self.isPossibleUHV(iFrankia, 0, True):
			if self.checkProvincesStates(iFrankia, tFrankControl):
				self.wonUHV( iFrankia, 0 )
		if iGameTurn == xml.i840AD:
			self.expireUHV(iFrankia, 0)

		# UHV 2: Control Jerusalem in 1291
		elif iGameTurn == xml.i1291AD:
			if self.isPossibleUHV(iFrankia, 1, True):
				pJPlot = gc.getMap().plot( con.tJerusalem[0], con.tJerusalem[1] )
				if pJPlot.isCity():
					if pJPlot.getPlotCity().getOwner() == iFrankia:
						self.wonUHV( iFrankia, 1 )
					else:
						self.lostUHV( iFrankia, 1 )
				else:
					self.lostUHV( iFrankia, 1 )

		# UHV 3: Build 5 Colonies
		# handled in the onProjectBuilt function


	def checkArabia( self, iGameTurn ):

		# UHV 1: Control all territories from Egypt to Asia Minor in 955
		if iGameTurn == xml.i955AD:
			if self.isPossibleUHV(iArabia, 0, True):
				if self.checkProvincesStates(iArabia, tArabiaControlI):
					self.wonUHV( iArabia, 0 )
				else:
					self.lostUHV( iArabia, 0 )

		# UHV 2: Control all territories from Oran to Asia Minor in 1291
		elif iGameTurn == xml.i1291AD:
			if self.isPossibleUHV(iArabia, 1, True):
				if self.checkProvincesStates(iArabia, tArabiaControlII):
					self.wonUHV( iArabia, 1 )
				else:
					self.lostUHV( iArabia, 1 )

		# UHV 3: Spread Islam to at least 35% of the population of Europe
		if self.isPossibleUHV(iArabia, 2, True):
			iPerc = gc.getGame().calculateReligionPercent( xml.iIslam )
			if iPerc >= 35:
				self.wonUHV( iArabia, 2 )


	def checkBulgaria( self, iGameTurn ):

		# UHV 1: Conquer Moesia, Thrace, Macedonia, Serbia, Arberia, Thessaloniki and Constantinople by 917
		if self.isPossibleUHV(iBulgaria, 0, True):
			if self.checkProvincesStates(iBulgaria, tBulgariaControl):
				self.wonUHV( iBulgaria, 0 )
		if iGameTurn == xml.i917AD:
			self.expireUHV(iBulgaria, 0)

		# UHV 2: Accumulate at least 100 Orthodox Faith Points by 1259
		if self.isPossibleUHV(iBulgaria, 1, True):
			if pBulgaria.getStateReligion() == xml.iOrthodoxy:
				if pBulgaria.getFaith() >= 100:
					self.wonUHV( iBulgaria, 1 )
		if iGameTurn == xml.i1259AD:
			self.expireUHV( iBulgaria, 1 )

		# UHV 3: Do not lose a city to barbarians (Mongols), Byzantines, or Ottomans before 1396
		# Controlled in the onCityAcquired function
		elif iGameTurn == xml.i1396AD:
			if self.isPossibleUHV(iBulgaria, 2, True):
				self.wonUHV( iBulgaria, 2 )


	def checkCordoba( self, iGameTurn ):

		# UHV 1: Make Cordoba the largest city in the world in 961
		if iGameTurn == xml.i961AD:
			if self.isPossibleUHV(iCordoba, 0, True):
				x, y = con.tCapitals[iCordoba]
				if gc.isLargestCity( x, y ) and gc.getMap().plot( x, y ).getPlotCity().getOwner() == iCordoba:
					self.wonUHV( iCordoba, 0 )
				else:
					self.lostUHV( iCordoba, 0 )

		# UHV 2: Build the Alhambra, the Gardens of Al-Andalus, and La Mezquita by 1309
		# Controlled in the onBuildingBuilt function
		elif iGameTurn == xml.i1309AD:
			self.expireUHV( iCordoba, 1 )

		# UHV 3: Make sure Islam is present in every city in the Iberian peninsula in 1492
		elif iGameTurn == xml.i1492AD:
			if self.isPossibleUHV(iCordoba, 2, True):
				bIslamized = True
				for iProv in tCordobaIslamize:
					if not pCordoba.provinceIsSpreadReligion( iProv, xml.iIslam ):
						bIslamized = False
						break
				if bIslamized:
					self.wonUHV( iCordoba, 2 )
				else:
					self.lostUHV( iCordoba, 2 )


	def checkNorway( self, iGameTurn ):

		# Old UHV1: explore all water tiles
		#if ( iGameTurn == xml.i1009AD and pNorway.getUHV( 0 ) == -1 ):
		#	if ( gc.canSeeAllTerrain( iNorway, xml.iTerrainOcean ) ):
		#		self.wonUHV( iNorway, 0 )
		#	else:
		#		self.lostUHV( iNorway, 0 )

		# UHV 1: Gain 100 Viking points and build Vinland by 1066
		# Viking points counted in the onCityAcquired, onPillageImprovement and onCombatResult functions
		if self.isPossibleUHV(iNorway, 0, True):
			if pNorway.getUHVCounter( 2 ) >= 100 and teamNorway.getProjectCount(xml.iColVinland) >= 1: # It's still counter 2, for the sake of convenience and confusion
				self.wonUHV( iNorway, 0 )
		if iGameTurn == xml.i1066AD:
			self.expireUHV( iNorway, 0 )

		# UHV 2: Conquer The Isles, Ireland, Scotland, Normandy, Sicily, Apulia, Calabria and Iceland by 1194
		if iGameTurn <= xml.i1194AD:
			if self.isPossibleUHV(iNorway, 1, True):
				if self.checkProvincesStates(iNorway, tNorwayControl):
					self.wonUHV( iNorway, 1 )
		if iGameTurn == xml.i1194AD:
			self.expireUHV( iNorway, 1 )

		# UHV 3: Have a higher score than Sweden, Denmark, Scotland, England, Germany and France in 1320
		elif iGameTurn == xml.i1320AD:
			if self.isPossibleUHV(iNorway, 2, True):
				iNorwayRank = gc.getGame().getTeamRank(iNorway)
				bIsOnTop = True
				for iTestPlayer in tNorwayOutrank:
					if gc.getGame().getTeamRank(iTestPlayer) < iNorwayRank:
						bIsOnTop = False
						break
				if bIsOnTop:
					self.wonUHV( iNorway, 2 )
				else:
					self.lostUHV( iNorway, 2 )


	def checkDenmark(self, iGameTurn):

		# UHV 1: Control Denmark, Skaneland, Götaland, Svealand, Mercia, London, Northumbria and East Anglia in 1050
		if iGameTurn == xml.i1050AD:
			if self.isPossibleUHV(iDenmark, 0, True):
				if self.checkProvincesStates(iDenmark, tDenmarkControlI):
					self.wonUHV( iDenmark, 0 )
				else:
					self.lostUHV( iDenmark, 0 )

		# UHV 2: Control Denmark, Norway, Vestfold, Skaneland, Götaland, Svealand, Norrland, Gotland, Österland, Estonia and Iceland in 1523
		elif iGameTurn == xml.i1523AD:
			if self.isPossibleUHV(iDenmark, 1, True):
				if self.checkProvincesStates(iDenmark, tDenmarkControlIII):
					self.wonUHV( iDenmark, 1 )
				else:
					self.lostUHV( iDenmark, 1 )

		# UHV 3: Build 3 Colonies and complete both Trading Companies
		# handled in the onProjectBuilt function


	def checkVenecia( self, iGameTurn ):

		# UHV 1: Conquer the Adriatic by 1004
		if self.isPossibleUHV(iVenecia, 0, True):
			if self.checkProvincesStates(iVenecia, tVenetianControl):
				self.wonUHV( iVenecia, 0 )
		if iGameTurn == xml.i1004AD:
			self.expireUHV( iVenecia, 0 )

		# UHV 2: Conquer Constantinople, Thessaly, Morea, Crete and Cyprus by 1204
		if self.isPossibleUHV(iVenecia, 1, True):
			if pVenecia.getProvinceCurrentState( xml.iP_Constantinople ) >= con.iProvinceConquer:
				if self.checkProvincesStates(iVenecia, tVenetianControlII):
					self.wonUHV( iVenecia, 1 )
		if iGameTurn == xml.i1204AD:
			self.expireUHV( iVenecia, 1 )

		# UHV 3: Be the first to build a Colony from the Age of Discovery (Vinland is from the Viking Age)
		# handled in the onProjectBuilt function


	def checkBurgundy( self, iGameTurn ):

		# UHV 1: Produce 10,000 culture points by 1336
		if self.isPossibleUHV(iBurgundy, 0, True):
			iCulture = pBurgundy.getUHVCounter( 0 ) + pBurgundy.countCultureProduced()
			pBurgundy.setUHVCounter( 0, iCulture )
			if iCulture >= 10000:
				self.wonUHV( iBurgundy, 0 )
		if iGameTurn == xml.i1336AD:
			self.expireUHV( iBurgundy, 0 )

		# UHV 2: Control Burgundy, Provence, Picardy, Flanders, Champagne and Lorraine in 1376
		elif iGameTurn == xml.i1376AD:
			if self.isPossibleUHV(iBurgundy, 1, True):
				if self.checkProvincesStates(iBurgundy, tBurgundyControl):
					self.wonUHV( iBurgundy, 1 )
				else:
					self.lostUHV( iBurgundy, 1 )

		# UHV 3: Have a higher score than France, England and Germany in 1473
		elif iGameTurn == xml.i1473AD:
			if self.isPossibleUHV(iBurgundy, 2, True):
				iBurgundyRank = gc.getGame().getTeamRank(iBurgundy)
				bIsOnTop = True
				for iTestPlayer in tBurgundyOutrank:
					if gc.getGame().getTeamRank(iTestPlayer) < iBurgundyRank:
						bIsOnTop = False
						break
				if bIsOnTop:
					self.wonUHV( iBurgundy, 2 )
				else:
					self.lostUHV( iBurgundy, 2 )


	def checkGermany( self, iGameTurn ):

		# Old UHVs: Have most Catholic FPs in 1077 (Walk to Canossa)
		#			Have 3 vassals

		# UHV 1: Control Lorraine, Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Lombardy and Tuscany in 1167
		if iGameTurn == xml.i1167AD:
			if self.isPossibleUHV(iGermany, 0, True):
				if self.checkProvincesStates(iGermany, tGermanyControl):
					self.wonUHV( iGermany, 0 )
				else:
					self.lostUHV( iGermany, 0 )

		# UHV 2: Start the Reformation (Found Protestantism)
		# Controlled in the onReligionFounded function

		# UHV 3: Control Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Flanders, Pomerania, Silesia, Bohemia, Moravia and Austria in 1648
		elif iGameTurn == xml.i1648AD:
			if self.isPossibleUHV(iGermany, 2, True):
				if self.checkProvincesStates(iGermany, tGermanyControlII):
					self.wonUHV( iGermany, 2 )
				else:
					self.lostUHV( iGermany, 2 )


	def checkNovgorod( self, iGameTurn ):

		# UHV 1: Control Novgorod, Karelia, Estonia and Livonia in 1284
		if iGameTurn == xml.i1284AD:
			if self.isPossibleUHV(iNovgorod, 0, True):
				if self.checkProvincesStates(iNovgorod, tNovgorodControl):
					self.wonUHV( iNovgorod, 0 )
				else:
					self.lostUHV( iNovgorod, 0 )

		# UHV 2: Control eleven sources of fur by 1397
		if self.isPossibleUHV(iNovgorod, 1, True):
			if pNovgorod.countCultBorderBonuses(xml.iFur) >= 11:
				self.wonUHV( iNovgorod, 1 )
		if iGameTurn == xml.i1397AD:
				self.expireUHV( iNovgorod, 1 )

		# UHV 3: Have seven cities in Karelia and Vologda in 1478
		elif iGameTurn == xml.i1478AD:
			if self.isPossibleUHV(iNovgorod, 2, True):
				iNumCities = 0
				for iProv in tNovgorodControlII:
					iNumCities += pNovgorod.getProvinceCityCount( iProv )
				if iNumCities >= 7:
					self.wonUHV( iNovgorod, 2 )
				else:
					self.lostUHV( iNovgorod, 2 )


	def checkKiev( self, iGameTurn ):

		# UHV 1: Build 2 Orthodox cathedrals and 8 Orthodox monasteries by 1250
		# Controlled in the onBuildingBuilt function
		if iGameTurn == xml.i1250AD+1:
			self.expireUHV( iKiev, 0 )

		# UHV 2: Control 10 provinces out of Kiev, Podolia, Pereyaslavl, Sloboda, Chernigov, Volhynia, Minsk, Polotsk, Smolensk, Moscow, Murom, Rostov, Novgorod and Vologda in 1288
		elif iGameTurn == xml.i1288AD:
			if self.isPossibleUHV(iKiev, 1, True):
				iConq = 0
				for iProv in tKievControl:
					if pKiev.getProvinceCurrentState( iProv ) >= con.iProvinceConquer:
						iConq += 1
				if iConq >= 10:
					self.wonUHV( iKiev, 1 )
				else:
					self.lostUHV( iKiev, 1 )

		# UHV 3: Produce 25000 food by 1300
		if self.isPossibleUHV(iKiev, 2, True):
			iFood = pKiev.getUHVCounter( 2 ) + pKiev.calculateTotalYield(YieldTypes.YIELD_FOOD)
			pKiev.setUHVCounter( 2, iFood )
			if iFood > 25000:
				self.wonUHV( iKiev, 2 )
		if iGameTurn == xml.i1300AD:
			self.expireUHV( iKiev, 2 )


	def checkHungary( self, iGameTurn ):

		# UHV 1: Allow no Ottoman cities in Europe in 1444
		if iGameTurn == xml.i1444AD:
			if self.isPossibleUHV(iHungary, 0, True):
				bClean = True
				if pTurkey.isAlive():
					for iProv in tHungarynControl:
						if pTurkey.getProvinceCityCount( iProv ) > 0:
							bClean = False
							break
				if bClean:
					self.wonUHV( iHungary, 0 )
				else:
					self.lostUHV( iHungary, 0 )

		# UHV 2: Control the most territory in Europe in 1490
		elif iGameTurn == xml.i1490AD:
			if self.isPossibleUHV(iHungary, 1, True):
				bMost = True
				iCount = self.getTerritoryPercentEurope(iHungary)
				for iOtherPlayer in range(con.iNumPlayers):
					if not gc.getPlayer(iOtherPlayer).isAlive() or iOtherPlayer == iHungary: continue
					iOtherCount = self.getTerritoryPercentEurope(iOtherPlayer)
					if iOtherCount >= iCount:
						bMost = False
						break
				if bMost:
					self.wonUHV( iHungary, 1 )
				else:
					self.lostUHV( iHungary, 1 )

		# UHV 3: Be the first to adopt Free Religion
		if self.isPossibleUHV(iHungary, 2, True):
			iCivic = pHungary.getCivics(4)
			if iCivic == xml.iCivicFreeReligion:
				self.wonUHV( iHungary, 2 )
			else:
				for iPlayer in range( iNumMajorPlayers ):
					pPlayer = gc.getPlayer( iPlayer )
					if pPlayer.isAlive() and pPlayer.getCivics(4) == xml.iCivicFreeReligion:
						self.lostUHV( iHungary, 2 )


	def checkSpain( self, iGameTurn ):

		# UHV 1: Reconquista (make sure Catholicism is the only religion present in every city in the Iberian peninsula in 1492)
		if iGameTurn == xml.i1492AD:
			if self.isPossibleUHV(iSpain, 0, True):
				bConverted = True
				for iProv in tSpainConvert:
					if not pSpain.provinceIsConvertReligion( iProv, xml.iCatholicism ):
						bConverted = False
						break
				if bConverted:
					self.wonUHV( iSpain, 0 )
				else:
					self.lostUHV( iSpain, 0 )

		# UHV 2: Have more Colonies than any other nation in 1588 (while having at least 3)
		elif iGameTurn == xml.i1588AD:
			if self.isPossibleUHV(iSpain, 1, True):
				bMost = True
				iSpainColonies = self.getNumRealColonies(iSpain)
				for iPlayer in range( iNumPlayers ):
					if iPlayer != iSpain:
						pPlayer = gc.getPlayer( iPlayer )
						if pPlayer.isAlive() and self.getNumRealColonies(iPlayer) >= iSpainColonies:
							bMost = False
				if bMost and iSpainColonies >= 3:
					self.wonUHV( iSpain, 1 )
				else:
					self.lostUHV( iSpain, 1 )

		# UHV 3: Ensure that the Catholic nations have more population and more land than any other religion in 1648
		elif iGameTurn == xml.i1648AD:
			if self.isPossibleUHV(iSpain, 2, True):
				if pSpain.getStateReligion() != xml.iCatholicism:
					self.lostUHV( iSpain, 2)
				else:
					lLand = [ 0, 0, 0, 0, 0, 0 ] # Prot, Islam, Cath, Orth, Jew, Pagan
					lPop  = [ 0, 0, 0, 0, 0, 0 ]
					for iPlayer in range( iNumPlayers ):
						pPlayer = gc.getPlayer( iPlayer )
						iStateReligion = pPlayer.getStateReligion()
						if iStateReligion > -1:
							lLand[ iStateReligion ] += pPlayer.getTotalLand()
							lPop[ iStateReligion ] += pPlayer.getTotalPopulation()
						else:
							lLand[ 5 ] += pPlayer.getTotalLand()
							lPop[ 5 ] += pPlayer.getTotalPopulation()

					iCathLand = lLand[ xml.iCatholicism ]
					iCathPop  = lPop[ xml.iCatholicism ]

					bWon = True
					for iReligion in range( xml.iNumReligions + 1 ):
						if iReligion != xml.iCatholicism:
							if lLand[ iReligion ] > iCathLand:
								bWon = False
								break
							if lPop[ iReligion ] > iCathPop:
								bWon = False
								break

					if bWon:
						self.wonUHV( iSpain, 2 )
					else:
						self.lostUHV( iSpain, 2 )


	def checkScotland( self, iGameTurn ):

		# UHV 1: Have 10 Forts and 4 Castles by 1296
		if self.isPossibleUHV(iScotland, 0, True):
			iForts = pScotland.getImprovementCount( xml.iImprovementFort )
			iCastles = pScotland.countNumBuildings( xml.iCastle )
			print("Forts:",iForts,"Castles:",iCastles)
			if iForts >= 10 and iCastles >= 4:
				self.wonUHV( iScotland, 0 )
		if iGameTurn == xml.i1296AD:
			self.expireUHV( iScotland, 0 )

		# UHV 2: Have 2500 attitude points with France by 1560 (attitude points go up every turn depending on your relations)
		if self.isPossibleUHV(iScotland, 1, True):
			if pFrankia.isAlive():
				# Being at war with France gives a big penalty (and ignores all bonuses!)
				if teamScotland.isAtWar(iFrankia):
					iScore = -10
				else:
					# -2 for Furious -1 for Annoyed 0 for Cautious 1 for Pleased 2 for Friendly
					iScore = pFrankia.AI_getAttitude(iScotland) - 2
					# Agreements
					if teamFrankia.isOpenBorders(iScotland):
						iScore+=1
					if teamFrankia.isDefensivePact(iScotland):
						iScore+=2
					# Imports/Exports
					iTrades = 0
					iTrades += pScotland.getNumTradeBonusImports(iFrankia)
					iTrades += pFrankia.getNumTradeBonusImports(iScotland)
					iScore += iTrades/3
					# Common Wars
					for iEnemy in xrange(iNumPlayers):
						if iEnemy in [iScotland, iFrankia]:
							continue
						if teamFrankia.isAtWar(iEnemy) and teamScotland.isAtWar(iEnemy):
							iScore+=2
				# Different religion from France also gives a penalty
				if pScotland.getStateReligion() != pFrankia.getStateReligion():
					iScore -= 3
				iOldScore = pScotland.getUHVCounter(1)
				iNewScore = iOldScore + iScore
				pScotland.setUHVCounter(1, iNewScore)
				if iNewScore >= 2500:
					self.wonUHV( iScotland, 1 )
		if iGameTurn == xml.i1560AD:
			self.expireUHV( iScotland, 1 )

		# UHV 3: Control Scotland, The Isles, Ireland, Wales, Brittany and Galicia in 1700
		elif iGameTurn == xml.i1700AD:
			if self.isPossibleUHV(iScotland, 2, True):
				if self.checkProvincesStates(iScotland, tScotlandControl):
					self.wonUHV( iScotland, 2 )
				else:
					self.lostUHV( iScotland, 2 )


	def checkPoland( self, iGameTurn ):

		# Old UHVs: Don't lose cities until 1772 or conquer Russia until 1772
		#			Vassalize Russia, Germany and Austria

		# UHV 1: Food production between 1500 and 1520
		if xml.i1500AD <= iGameTurn <= xml.i1520AD:
			if self.isPossibleUHV(iPoland, 0, True):
				iAgriculturePolish = pPoland.calculateTotalYield(YieldTypes.YIELD_FOOD)
				bFood = True
				for iPlayer in range( iNumMajorPlayers ):
					if gc.getPlayer( iPlayer ).calculateTotalYield(YieldTypes.YIELD_FOOD ) > iAgriculturePolish:
						bFood = False
						break
				if bFood:
					self.wonUHV( iPoland, 0 )
		if iGameTurn == xml.i1520AD+1:
			self.expireUHV( iPoland, 0 )

		# UHV 2: Own at least 12 cities in the given provinces in 1600
		elif iGameTurn == xml.i1600AD:
			if self.isPossibleUHV(iPoland, 1, True):
				iNumCities = 0
				for iProv in tPolishControl:
					iNumCities += pPoland.getProvinceCityCount( iProv )
				if iNumCities >= 12:
					self.wonUHV( iPoland, 1 )
				else:
					self.lostUHV( iPoland, 1 )

		# UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
		# Controlled in the onBuildingBuilt and onCityAcquired functions


	def checkGenoa( self, iGameTurn ):

		# UHV 1: Control Corsica, Sardinia, Crete, Rhodes and Crimea in 1566
		if iGameTurn == xml.i1566AD:
			if self.isPossibleUHV(iGenoa, 0, True):
				if self.checkProvincesStates(iGenoa, tGenoaControl):
					self.wonUHV( iGenoa, 0 )
				else:
					self.lostUHV( iGenoa, 0 )

		# UHV 2: Build 8 Banks
		# Controlled in the onBuildingBuilt function

		# UHV 3: Have the largest total amount of commerce from foreign Trade Route Exports and Imports in 1640
		elif iGameTurn == xml.i1640AD:
			if self.isPossibleUHV(iGenoa, 2, True):
				iGenoaTrade = iImports = pGenoa.calculateTotalImports(YieldTypes.YIELD_COMMERCE) + pGenoa.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
				bLargest = True
				for iPlayer in range( iNumMajorPlayers ):
					if iPlayer != iGenoa:
						pPlayer = gc.getPlayer(iPlayer)
						if pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE) + pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE) > iGenoaTrade:
							bLargest = False
							break
				if bLargest:
					self.wonUHV( iGenoa, 2 )
				else:
					self.lostUHV( iGenoa, 2 )


	def checkMorocco( self, iGameTurn ):

		# UHV 1: Control Morocco, Marrakesh, Fez, Tetouan, Oran, Algiers, Ifriqiya, Andalusia, Valencia and the Balearic Islands in 1227
		if iGameTurn == xml.i1227AD:
			if self.isPossibleUHV(iMorocco, 0, True):
				if self.checkProvincesStates(iMorocco, tMoroccoControl):
					self.wonUHV( iMorocco, 0 )
				else:
					self.lostUHV( iMorocco, 0 )

		# UHV 2: Have 5000 culture in each of three cities in 1465
		elif iGameTurn == xml.i1465AD:
			if self.isPossibleUHV(iMorocco, 1, True):
				iGoodCities = 0
				for city in utils.getCityList(iPlayer):
					if city.getCulture(iMorocco) >= 5000:
						iGoodCities += 1
				if iGoodCities >= 3:
					self.wonUHV( iMorocco, 1 )
				else:
					self.lostUHV( iMorocco, 1 )

		# UHV 3: Destroy or vassalize Portugal, Spain, and Aragon by 1578
		if xml.i1164AD <= iGameTurn <= xml.i1578AD:
			if self.isPossibleUHV(iMorocco, 2, True):
				bConq = True
				if pSpain.isAlive() and not teamSpain.isVassal( teamMorocco.getID() ):
					bConq = False
				elif pPortugal.isAlive() and not teamPortugal.isVassal( teamMorocco.getID() ):
					bConq = False
				elif pAragon.isAlive() and not teamAragon.isVassal( teamMorocco.getID() ):
					bConq = False

				if bConq:
					self.wonUHV( iMorocco, 2 )
		if iGameTurn == xml.i1578AD+1:
			self.expireUHV( iMorocco, 2 )


	def checkEngland( self, iGameTurn ):

		# UHV 1: Control London, Wessex, East Anglia, Mercia, Northumbria, Scotland, Wales, Ireland, Normandy, Picardy, Bretagne, Il-de-France, Aquitania and Orleans in 1452
		if iGameTurn == xml.i1452AD:
			if self.isPossibleUHV(iEngland, 0, True):
				if self.checkProvincesStates(iEngland, tEnglandControl):
					self.wonUHV( iEngland, 0 )
				else:
					self.lostUHV( iEngland, 0 )

		# UHV 2: Build 7 Colonies
		# Controlled in the onProjectBuilt function

		# UHV 3: Be the first to enter the Industrial age
		# Controlled in the onTechAcquired function


	def checkPortugal( self, iGameTurn ):

		# UHV 1: Settle 3 cities on the Azores, Canaries and Madeira and 2 in Morocco, Tetouan and Oran
		# Controlled in the onCityBuilt function

		# UHV 2: Do not lose a city before 1640
		# Controlled in the onCityAcquired function
		if iGameTurn == xml.i1640AD:
			if self.isPossibleUHV(iPortugal, 1, True):
				self.wonUHV( iPortugal, 1 )

		# UHV 3: Build 5 Colonies
		# Controlled in the onProjectBuilt function


	def checkAragon( self, iGameTurn ):

		# UHV 1: Control Catalonia, Valencia, Balears and Sicily in 1282
		if iGameTurn == xml.i1282AD:
			if self.isPossibleUHV(iAragon, 0, True):
				if self.checkProvincesStates(iAragon, tAragonControlI):
					self.wonUHV( iAragon, 0 )
				else:
					self.lostUHV( iAragon, 0 )

		# UHV 2: Have 12 Consulates of the Sea in 1444
		elif iGameTurn == xml.i1444AD:
			if self.isPossibleUHV(iAragon, 1, True):
				iPorts = pAragon.countNumBuildings(xml.iAragonSeaport)
				print("Ports:",iPorts)
				if iPorts >= 12:
					self.wonUHV( iAragon, 1 )
				else:
					self.lostUHV( iAragon, 1 )

		# UHV 3: Control Catalonia, Valencia, Aragon, Balears, Corsica, Sardinia, Sicily, Calabria, Apulia, Provence and Thessaly in 1474
		elif iGameTurn == xml.i1474AD:
			if self.isPossibleUHV(iAragon, 2, True):
				if self.checkProvincesStates(iAragon, tAragonControlII):
					self.wonUHV( iAragon, 2 )
				else:
					self.lostUHV( iAragon, 2 )


	def checkPrussia( self, iGameTurn ):

		# UHV 1: Control Prussia, Suvalkija, Lithuania, Livonia, Estonia, and Pomerania in 1410
		if iGameTurn == xml.i1410AD:
			if self.isPossibleUHV(iPrussia, 0, True):
				if self.checkProvincesStates(iPrussia, tPrussiaControlI):
					self.wonUHV( iPrussia, 0 )
				else:
					self.lostUHV( iPrussia, 0 )

		# UHV 2: Conquer two cities from each of Austria, Muscowy, Germany, Sweden, France and Spain between 1650 and 1763, if they are still alive
		# Controlled in the onCityAcquired function
		if iGameTurn > xml.i1763AD:
			self.expireUHV( iPrussia, 1 )

		# UHV 3: Settle a total of 15 Great People in your capital
		if self.isPossibleUHV(iPrussia, 2, True):
			pCapital = pPrussia.getCapitalCity()
			iGPStart = gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST")
			iGPEnd = gc.getInfoTypeForString("SPECIALIST_GREAT_SPY")
			iGPeople = 0
			for iType in range(iGPStart, iGPEnd+1):
				iGPeople += pCapital.getFreeSpecialistCount(iType)
			if iGPeople >= 15:
				self.wonUHV( iPrussia, 2 )


	def checkLithuania( self, iGameTurn ):

		# UHV 1: Accumulate 2000 Culture points without declaring a state religion before 1386
		if self.isPossibleUHV(iLithuania, 0, True):
			if pLithuania.getStateReligion() != -1:
				self.lostUHV( iLithuania, 0 )
			iCulture = pLithuania.getUHVCounter( 0 ) + pLithuania.countCultureProduced()
			pLithuania.setUHVCounter( 0, iCulture )
			if iCulture >= 2000:
				self.wonUHV( iLithuania, 0 )
		if iGameTurn == xml.i1386AD:
			self.expireUHV( iLithuania, 0 )

		# UHV 2: Have at least 18 cities in 1569
		elif iGameTurn == xml.i1569AD:
			if self.isPossibleUHV(iLithuania, 1, True):
				if pLithuania.getNumCities() >= 18:
					self.wonUHV( iLithuania, 1 )
				else:
					self.lostUHV( iLithuania, 1 )

		# UHV 3: Conquer the province of Moscow or vassalize Muscovy
		if self.isPossibleUHV(iLithuania, 2, True):
			if pMoscow.isAlive() and teamMoscow.isVassal( teamLithuania.getID() ):
				self.wonUHV( iLithuania, 2 )
			elif iGameTurn > xml.i1401AD and pLithuania.getProvinceCurrentState( xml.iP_Moscow ) >= con.iProvinceConquer:
				self.wonUHV( iLithuania, 2 )


	def checkAustria( self, iGameTurn ):

		# UHV 1: Control all of medieval Austria, Hungary and Bohemia in 1617
		if iGameTurn == xml.i1617AD:
			if self.isPossibleUHV(iAustria, 0, True):
				if self.checkProvincesStates(iAustria, tAustriaControl):
					self.wonUHV( iAustria, 0 )
				else:
					self.lostUHV( iAustria, 0 )

		# UHV 2: Have 3 vassals in 1700
		elif iGameTurn == xml.i1700AD:
			if self.isPossibleUHV(iAustria, 1, True):
				iCount = 0
				for iPlayer in range( iNumMajorPlayers ):
					if iPlayer == iAustria: continue
					pPlayer = gc.getPlayer( iPlayer )
					if pPlayer.isAlive():
						if gc.getTeam( pPlayer.getTeam() ).isVassal( iAustria ):
							iCount += 1
				if iCount >= 3:
					self.wonUHV( iAustria, 1 )
				else:
					self.lostUHV( iAustria, 1 )

		# UHV 3: Have the highest score in 1780
		elif iGameTurn == xml.i1780AD:
			if self.isPossibleUHV(iAustria, 2, True):
				if gc.getGame().getTeamRank(iAustria) == 0:
					self.wonUHV( iAustria, 2 )
				else:
					self.lostUHV( iAustria, 2 )


	def checkTurkey( self, iGameTurn ):

		# UHV 1: Control the Balkans in 1453
		if iGameTurn == xml.i1453AD:
			if self.isPossibleUHV(iTurkey, 0, True):
				if self.checkProvincesStates(iTurkey, tOttomanControlI):
					self.wonUHV( iTurkey, 0 )
				else:
					self.lostUHV( iTurkey, 0 )

		# UHV 2: Control Anatolia, the Levant and Egypt in 1517
		elif iGameTurn == xml.i1517AD:
			if self.isPossibleUHV(iTurkey, 1, True):
				if self.checkProvincesStates(iTurkey, tOttomanControlII):
					self.wonUHV( iTurkey, 1 )
				else:
					self.lostUHV( iTurkey, 1 )

		# UHV 3: Conquer Austria by 1683
		if self.isPossibleUHV(iTurkey, 2, True):
			if self.checkProvincesStates(iTurkey, tOttomanControlIII):
				self.wonUHV( iTurkey, 2 )
		if iGameTurn == xml.i1683AD:
			self.expireUHV( iTurkey, 2 )


	def checkMoscow( self, iGameTurn ):

		# UHV 1: Free Eastern Europe from the Mongols
		if iGameTurn == xml.i1482AD:
			if self.isPossibleUHV(iMoscow, 0, True):
				bClean = True
				for iProv in tMoscowControl:
					if pBarbarian.getProvinceCityCount( iProv ) > 0:
						bClean = False
						break
				if bClean:
					self.wonUHV( iMoscow, 0 )
				else:
					self.lostUHV( iMoscow, 0 )

		# UHV 2: Control at least 20% of Europe
		if self.isPossibleUHV(iMoscow, 1, True):
			totalLand = gc.getMap().getLandPlots()
			RussianLand = pMoscow.getTotalLand()
			if totalLand > 0:
				landPercent = (RussianLand * 100.0) / totalLand
			else:
				landPercent = 0.0
			if landPercent >= 20:
				self.wonUHV( iMoscow, 1 )

		# UHV 3: Get into warm waters
		if self.isPossibleUHV(iMoscow, 2, True):
			if pMoscow.countCultBorderBonuses( xml.iAccess ) > 0:
				self.wonUHV( iMoscow, 2 )
			elif gc.getMap().plot( con.tCapitals[iByzantium][0], con.tCapitals[iByzantium][1] ).getPlotCity().getOwner() == iMoscow:
				self.wonUHV( iMoscow, 2 )


	def checkSweden( self, iGameTurn ):

		# Old UHVs: Conquer Gotaland, Svealand, Norrland, Skaneland, Gotland and Osterland in 1600
		#			Don't lose any cities to Poland, Lithuania or Russia before 1700
		#			Have 15 cities in Saxony, Brandenburg, Holstein, Pomerania, Prussia, Greater Poland, Masovia, Suvalkija, Lithuania, Livonia, Estonia, Smolensk, Polotsk, Minsk, Murom, Chernigov, Moscow, Novgorod and Rostov in 1750

		# UHV 1: Have six cities in Norrland, Osterland and Karelia in 1323
		if iGameTurn == xml.i1323AD:
			if self.isPossibleUHV(iSweden, 0, True):
				iNumCities = 0
				for iProv in tSwedenControl:
					iNumCities += pSweden.getProvinceCityCount(iProv)
				if iNumCities >= 6:
					self.wonUHV( iSweden, 0 )
				else:
					self.lostUHV( iSweden, 0 )

		# UHV 2: Raze 5 Catholic cities while being Protestant by 1660
		# Controlled in the onCityRazed function
		elif iGameTurn == xml.i1660AD:
			self.expireUHV( iSweden, 1 )

		# UHV 3: Control every coastal city on the Baltic in 1750
		elif iGameTurn == xml.i1750AD:
			if self.isPossibleUHV(iSweden, 2, True):
				if up.getNumForeignCitiesOnBaltic(iSweden, True) > 0:
					self.lostUHV( iSweden, 2 )
				else:
					self.wonUHV( iSweden, 2 )


	def checkDutch( self, iGameTurn ):

		# UHV 1: Settle 5 Great Merchants in Amsterdam by 1750
		if self.isPossibleUHV(iDutch, 0, True):
			pPlot = gc.getMap().plot( con.tCapitals[iDutch][0], con.tCapitals[iDutch][1])
			if pPlot.isCity():
				city = pPlot.getPlotCity()
				if city.getFreeSpecialistCount(xml.iGreatMerchant) >= 5 and city.getOwner() == iDutch:
					self.wonUHV( iDutch, 0 )
		if iGameTurn == xml.i1750AD:
			self.expireUHV( iDutch, 0 )

		# UHV 2: Build 3 Colonies and complete both Trading Companies
		# Controlled in the onProjectBuilt function

		# UHV 3: Become the richest country in Europe
		if self.isPossibleUHV(iDutch, 2, True):
			iGold = pDutch.getGold()
			bMost = True
			for iCiv in range( iNumPlayers ):
				if iCiv == iDutch: continue
				pPlayer = gc.getPlayer(iCiv)
				if pPlayer.isAlive():
					if pPlayer.getGold() > iGold:
						bMost = False
						break
			if bMost:
				self.wonUHV( iDutch, 2 )


	def checkProvincesStates(self, iPlayer, tProvinces):
		pPlayer = gc.getPlayer(iPlayer)
		for iProv in tProvinces:
			if pPlayer.getProvinceCurrentState( iProv ) < con.iProvinceConquer:
				return False
		return True


	def wonUHV(self, iCiv, iUHV):
		pCiv = gc.getPlayer(iCiv)
		pCiv.setUHV( iUHV, 1 )
		pCiv.changeStabilityBase( iCathegoryExpansion, 3 )
		if utils.getHumanID() == iCiv:
			popup = Popup.PyPopup()
			popup.setBodyString(localText.getText("TXT_KEY_VICTORY_UHV_GOAL_WON", (iUHV+1,)))
			popup.launch()


	def lostUHV(self, iCiv, iUHV):
		pCiv = gc.getPlayer(iCiv)
		pCiv.setUHV( iUHV, 0 )
		if utils.getHumanID() == iCiv:
			popup = Popup.PyPopup()
			popup.setBodyString(localText.getText("TXT_KEY_VICTORY_UHV_GOAL_LOST", (iUHV+1,)))
			popup.launch()


	def setAllUHVFailed( self, iCiv ):
		pPlayer = gc.getPlayer(iCiv)
		for i in range(3):
			pPlayer.setUHV( i, 0 )


	def SwitchUHV(self, iNewCiv, iOldCiv):
		pPlayer = gc.getPlayer(iNewCiv)
		for i in range(3):
			pPlayer.setUHV( i, -1 )
		if self.isIgnoreAI():
			self.setAllUHVFailed(iOldCiv)


	def isPossibleUHV(self, iCiv, iUHV, bAlreadyAIChecked):
		pCiv = gc.getPlayer(iCiv)
		if pCiv.getUHV(iUHV) != -1: return False
		if not pCiv.isAlive(): return False

		if not bAlreadyAIChecked:
			if iCiv != utils.getHumanID() and self.isIgnoreAI(): # Skip calculations if no AI UHV option is enabled
				return False

		return True


	def expireUHV(self, iCiv, iUHV):
		if self.isPossibleUHV(iCiv, iUHV, True):
			self.lostUHV(iCiv, iUHV)


	def set1200UHVDone( self, iCiv ):
		if iCiv == iByzantium:
			pByzantium.setUHV( 0, 1 )
		elif iCiv == iFrankia:
			pFrankia.setUHV( 0, 1 )
		elif iCiv == iArabia:
			pArabia.setUHV( 0, 1 )
		elif iCiv == iBulgaria:
			pBulgaria.setUHV( 0, 1 )
		elif iCiv == iVenecia: # Venice gets conquerors near Constantinople for 2nd UHV
			pVenecia.setUHV( 0, 1 )
		elif iCiv == iGermany:
			pGermany.setUHV( 0, 1 )
		elif iCiv == iNorway:
			pNorway.setUHV( 0, 1 )
		elif iCiv == iDenmark:
			pDenmark.setUHV( 0, 1 )
		elif iCiv == iScotland:
			pScotland.setUHVCounter(1, 100)
