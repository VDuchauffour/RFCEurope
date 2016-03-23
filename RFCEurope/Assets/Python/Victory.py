# Rhye's and Fall of Civilizations: Europe - Historical Victory Goals

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
from Consts import *
from XMLConsts import *
import RFCUtils
import Crusades as cru
import UniquePowers
import RFCEMaps as rfcemaps
from StoredData import sd

utils = RFCUtils.RFCUtils()
up = UniquePowers.UniquePowers()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

# ------------------- NEW UHV CONDITIONS
tByzantumControl = [ iP_Colonea, iP_Antiochia, iP_Charsianon, iP_Cilicia, iP_Armeniakon, iP_Anatolikon, iP_Paphlagonia, iP_Thrakesion, iP_Opsikion, iP_Constantinople, iP_Thrace, iP_Thessaloniki, iP_Moesia, iP_Macedonia, iP_Serbia, iP_Arberia, iP_Epirus, iP_Thessaly, iP_Morea ]
tFrankControl = [ iP_Swabia, iP_Saxony, iP_Lorraine, iP_IleDeFrance, iP_Picardy, iP_Aquitania, iP_Provence, iP_Burgundy, iP_Orleans, iP_Champagne, iP_Catalonia, iP_Lombardy, iP_Tuscany ]
tArabiaControlI = [ iP_Egypt, iP_Antiochia, iP_Syria, iP_Lebanon, iP_Arabia, iP_Jerusalem ]
tArabiaControlII = [ iP_Oran, iP_Algiers, iP_Ifriqiya, iP_Cyrenaica, iP_Tripolitania, iP_Egypt, iP_Antiochia, iP_Syria, iP_Lebanon, iP_Arabia, iP_Jerusalem]
tBulgariaControl = [ iP_Constantinople, iP_Thessaloniki, iP_Serbia, iP_Thrace, iP_Macedonia, iP_Moesia, iP_Arberia ]
tCordobaWonders = [ iAlhambra, iLaMezquita, iGardensAlAndalus ]
tCordobaIslamize = [ iP_GaliciaSpain, iP_Castile, iP_Leon, iP_Lusitania, iP_Catalonia, iP_Aragon, iP_Navarre, iP_Valencia, iP_LaMancha, iP_Andalusia ]
tNorwayControl = [iP_TheIsles, iP_Ireland, iP_Mercia, iP_Normandy, iP_Iceland]
tNorwayOutrank = [ iSweden, iDenmark, iScotland, iEngland, iGermany, iFrankia ]
#tNorseControl = [ iP_Sicily, iP_Iceland, iP_Northumbria, iP_Scotland, iP_Normandy, iP_Ireland, iP_Novgorod ]
#tVenetianControl = [ iP_Morea, iP_Epirus, iP_Dalmatia, iP_Verona, iP_Crete, iP_Cyprus ]
tVenetianControl = [ iP_Epirus, iP_Dalmatia, iP_Verona, iP_Arberia ]
tBurgundyControl = [ iP_Flanders, iP_Picardy, iP_Provence, iP_Burgundy, iP_Champagne, iP_Lorraine ]
tBurgundyOutrank = [ iFrankia, iEngland, iGermany ]
tGermanyControl = [ iP_Tuscany, iP_Lombardy, iP_Lorraine, iP_Swabia, iP_Saxony, iP_Bavaria, iP_Franconia, iP_Brandenburg, iP_Holstein ]
tGermanyControlII = [ iP_Austria, iP_Flanders, iP_Pomerania, iP_Silesia, iP_Bohemia, iP_Moravia, iP_Swabia, iP_Saxony, iP_Bavaria, iP_Franconia, iP_Brandenburg, iP_Holstein ]
tKievControl = [ iP_Kiev, iP_Podolia, iP_Pereyaslavl, iP_Sloboda, iP_Chernigov, iP_Volhynia, iP_Minsk, iP_Polotsk, iP_Smolensk, iP_Moscow, iP_Murom, iP_Rostov, iP_Novgorod, iP_Vologda ]
tHungarynControl = [ iP_Thrace, iP_Moesia, iP_Macedonia, iP_Thessaloniki, iP_Wallachia, iP_Thessaly, iP_Morea, iP_Epirus, iP_Arberia, iP_Serbia, iP_Banat, iP_Bosnia, iP_Dalmatia, iP_Slavonia ]
tSpainConvert = [ iP_GaliciaSpain, iP_Castile, iP_Leon, iP_Lusitania, iP_Catalonia, iP_Aragon, iP_Navarre, iP_Valencia, iP_LaMancha, iP_Andalusia ]
tPolishControl = [ iP_Bohemia, iP_Moravia, iP_UpperHungary, iP_Prussia, iP_Lithuania, iP_Livonia, iP_Polotsk, iP_Minsk, iP_Volhynia, iP_Podolia, iP_Moldova, iP_Kiev ]
tGenoaControl = [ iP_Sardinia, iP_Corsica, iP_Crete, iP_Rhodes, iP_Crimea ]
tEnglandControl = [ iP_Aquitania, iP_London, iP_Wales, iP_Wessex, iP_Scotland, iP_EastAnglia, iP_Mercia, iP_Northumbria, iP_Ireland, iP_Normandy, iP_Bretagne, iP_IleDeFrance, iP_Orleans, iP_Picardy ]
tPortugalControlI = [ iP_Azores, iP_Canaries, iP_Madeira ]
tPortugalControlII = [ iP_Morocco, iP_Tetouan, iP_Oran ]
#tLithuaniaControl = [ iP_Lithuania, iP_GreaterPoland, iP_LesserPoland, iP_Pomerania, iP_Masovia, iP_Brest, iP_Suvalkija, iP_Livonia, iP_Novgorod, iP_Smolensk, iP_Polotsk, iP_Minsk, iP_Chernigov, iP_Pereyaslavl, iP_Kiev, iP_GaliciaPoland, iP_Sloboda ]
tAustriaControl = [ iP_Hungary, iP_UpperHungary, iP_Austria, iP_Carinthia, iP_Bavaria, iP_Transylvania, iP_Pannonia, iP_Moravia, iP_Silesia, iP_Bohemia ]
tOttomanControlI = [ iP_Serbia, iP_Bosnia, iP_Banat, iP_Macedonia, iP_Thrace, iP_Moesia, iP_Constantinople, iP_Arberia, iP_Epirus, iP_Thessaloniki, iP_Thessaly, iP_Morea ]
tOttomanControlII = [ iP_Colonea, iP_Antiochia, iP_Charsianon, iP_Cilicia, iP_Armeniakon, iP_Anatolikon, iP_Paphlagonia, iP_Thrakesion, iP_Opsikion, iP_Syria, iP_Lebanon, iP_Jerusalem, iP_Egypt ]
tOttomanControlIII = [ iP_Austria ]
tMoscowControl = [ iP_Donets, iP_Kuban, iP_Zaporizhia, iP_Sloboda, iP_Kiev, iP_Moldova, iP_Crimea, iP_Pereyaslavl, iP_Chernigov, iP_Simbirsk, iP_NizhnyNovgorod, iP_Vologda, iP_Rostov, iP_Novgorod, iP_Karelia, iP_Smolensk, iP_Polotsk, iP_Minsk, iP_Volhynia, iP_Podolia, iP_Moscow, iP_Murom ]
#tSwedenControlI = [ iP_Gotaland, iP_Svealand, iP_Norrland, iP_Skaneland, iP_Gotland, iP_Osterland ]
#tSwedenControlII = [ iP_Saxony, iP_Brandenburg, iP_Holstein, iP_Pomerania, iP_Prussia, iP_GreaterPoland, iP_Masovia, iP_Suvalkija, iP_Lithuania, iP_Livonia, iP_Estonia, iP_Smolensk, iP_Polotsk, iP_Minsk, iP_Murom, iP_Chernigov, iP_Moscow, iP_Novgorod, iP_Rostov ]
tSwedenControl = [ iP_Norrland, iP_Osterland, iP_Karelia]
tNovgorodControl = [ iP_Novgorod, iP_Karelia, iP_Estonia, iP_Livonia, ]
tNovgorodControlII = [ iP_Karelia, iP_Vologda ]
tMoroccoControl = [ iP_Morocco, iP_Marrakesh, iP_Fez, iP_Tetouan, iP_Oran, iP_Algiers, iP_Ifriqiya, iP_Tripolitania, iP_Andalusia, iP_Valencia ]
tAragonControlI = [ iP_Catalonia, iP_Valencia, iP_Balears, iP_Sicily ]
tAragonControlII = [ iP_Catalonia, iP_Valencia, iP_Aragon, iP_Balears, iP_Corsica, iP_Sardinia, iP_Sicily, iP_Apulia, iP_Provence, iP_Thessaly ]
tPrussiaControlI = [ iP_Lithuania, iP_Suvalkija, iP_Livonia, iP_Estonia, iP_Pomerania, iP_Prussia]
tPrussiaDefeat = [ iAustria, iMoscow, iGermany, iSweden, iFrankia, iSpain ]
tScotlandControl = [ iP_Scotland, iP_TheIsles, iP_Ireland, iP_Wales, iP_Bretagne ]
tDenmarkControlI = [ iP_Denmark, iP_Skaneland, iP_Gotaland, iP_Svealand, iP_Mercia, iP_London, iP_EastAnglia, iP_Northumbria ]
#tDenmarkControlII = [ iP_Brandenburg, iP_Pomerania, iP_Estonia ]
tDenmarkControlIII = [ iP_Denmark, iP_Norway, iP_Vestfold, iP_Skaneland, iP_Gotaland, iP_Svealand, iP_Norrland, iP_Gotland, iP_Osterland, iP_Estonia, iP_Iceland ]

#tHugeHungaryControl = ( 0, 23, 99, 72 )
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

	def setup( self ):
		# ignore AI goals
		bIgnoreAI = (gc.getDefineINT("NO_AI_UHV_CHECKS") == 1)
		self.setIgnoreAI(bIgnoreAI)
		if bIgnoreAI:
			for iPlayer in range(iNumPlayers):
				if utils.getHumanID() != iPlayer:
					self.setAllUHVFailed(iPlayer)
			

	def getCorporationsFounded( self ):
		return sd.scriptDict['bCorpsFounded']

	def setCorporationsFounded( self, iChange ):
		sd.scriptDict['bCorpsFounded'] = iChange
		
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
		#if ( iPlayer < iPope and pPlayer.isAlive() ): # don't count the Pope
		if iPlayer != utils.getHumanID() and self.isIgnoreAI():
			return
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return
		self.switchConditionsPerCiv[iPlayer](iGameTurn)

		# Generic checks:
		if (pPlayer.isAlive() and iPlayer < iNumMajorPlayers):
			if ( not pPlayer.getUHV2of3() ):
				if (utils.countAchievedGoals(iPlayer) == 2):
					#intermediate bonus
					pPlayer.setUHV2of3( True )
					if (pPlayer.getNumCities() > 0): #this check is needed, otherwise game crashes
						capital = pPlayer.getCapitalCity()
						# 3Miro: Golden Age after 2/3 victories
						capital.setHasRealBuilding(iTriumphalArch, True)
						if (pPlayer.isHuman()):
							CyInterface().addMessage(iPlayer, False, iDuration, CyTranslator().getText("TXT_KEY_VICTORY_INTERMEDIATE", ()), "", 0, "", ColorTypes(iPurple), -1, -1, True, True)
							for iCiv in range(iNumPlayers):
								if (iCiv != iPlayer):
									pCiv = gc.getPlayer(iCiv)
									if (pCiv.isAlive()):
										iAttitude = pCiv.AI_getAttitude(iPlayer)
										if (iAttitude != 0):
											pCiv.AI_setAttitudeExtra(iPlayer, iAttitude-1) #da controllare

							# Absinthe: maximum 3 of your rivals declare war on you
							iWarCounter = 0
							iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'civs')
							CyInterface().addMessage(iPlayer, False, iDuration, CyTranslator().getText("TXT_KEY_VICTORY_RIVAL_CIVS", ()), "", 0, "", ColorTypes(iPurple), -1, -1, True, True)
							for i in range( iRndnum, iNumPlayers + iRndnum ):
								iCiv = i % iNumPlayers
								pCiv = gc.getPlayer(iCiv)
								teamCiv = gc.getTeam(pCiv.getTeam())
								teamOwn = gc.getTeam(pPlayer.getTeam())
								if ((iCiv != iPope) and pCiv.isAlive() and pCiv.canContact(iPlayer) and (teamCiv != teamOwn)):
									if (pCiv.AI_getAttitude(iPlayer) < 2):
										if (not teamCiv.isAtWar(iPlayer)):
											teamCiv.declareWar(iPlayer, True, -1)
											iWarCounter += 1
											if (iWarCounter == 3):
												break

		if (gc.getGame().getWinner() == -1):
			if ( pPlayer.getUHV(0) == 1 and pPlayer.getUHV(1) == 1 and pPlayer.getUHV(2) == 1):
				gc.getGame().setWinner(iPlayer, 7) # Historical Victory


	def onCityBuilt(self, city, iPlayer): #see onCityBuilt in CvRFCEventHandler
		# Portugal UHV 1:
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
					pPortugal.changeStabilityBase( iCathegoryExpansion, 3 )
				pPortugal.setUHVCounter( 0, iAfrica * 100 + iIslands )


	def onReligionFounded(self, iReligion, iFounder):
		# Germany UHV 2:
		if (iReligion == iProtestantism):
			if iFounder == iGermany:
				pGermany.setUHV( 1, 1 )
				pGermany.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pGermany.setUHV( 1, 0 )


	def onCityAcquired(self, owner, playerType, city, bConquest):
		if (not gc.getGame().isVictoryValid(7)): # Victory 7 == historical
			return

		iPlayer = owner
		iGameTurn = gc.getGame().getGameTurn()

		# Bulgaria UHV 3:
		if ( iPlayer == iBulgaria and pBulgaria.isAlive() ):
			if ( iGameTurn <= i1393AD and pBulgaria.getUHV( 2 ) == -1 ):
				if ( playerType == iBarbarian or playerType == iTurkey or playerType == iByzantium ):
					pBulgaria.setUHV( 2, 0 )

		# Portugal UHV 2:
		elif ( iPlayer == iPortugal and pPortugal.isAlive() ):
			if ( bConquest ):
				if ( pPortugal.getUHV( 1 ) == -1 ):
					pPortugal.setUHV( 1, 0 )

		# Norway UHV 1: Going Viking
		elif ( playerType == iNorway ):
			pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + city.getPopulation() )

		# Poland UHV 3:
		elif ( playerType == iPoland and pPoland.getUHV( 2 ) == -1 ):
			if ( city.hasBuilding( iKazimierz )): # you cannot acquire religious buildings on conquest, only wonders
				iCounter = pPoland.getUHVCounter( 2 )
				iCathCath = ( iCounter / 10000 ) % 10
				iOrthCath = ( iCounter / 1000 ) % 10
				iProtCath = ( iCounter / 100 ) % 10
				iJewishQu = 99
				iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
				pPoland.setUHVCounter( 2, iCounter )
				if ( iCathCath >= 3 and iOrthCath >= 2 and iProtCath >= 2 and iJewishQu >= 2 ):
					pPoland.setUHV( 2, 1 )
					pPoland.changeStabilityBase( iCathegoryExpansion, 3 )

		# Prussia UHV 2: Conquer two cities from each of Austria, Muscowy, Germany, Sweden, France and Spain between 1650AD and 1763AD, if they are still alive.
		elif(playerType == iPrussia and owner in tPrussiaDefeat and iGameTurn >= i1650AD and iGameTurn <= i1763AD):
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
				pPrussia.setUHV( 1, 1 )
				pPrussia.changeStabilityBase( iCathegoryExpansion, 3 )

			iConqRaw = 0
			for iI in range(len(tPrussiaDefeat)):
				iConqRaw += lNumConq[iI] * pow(10,iI)
			pPrussia.setUHVCounter(1,iConqRaw)


	def onCityRazed(self, iPlayer, city):
		# Sweden UHV 2: Raze 5 Catholic cities while being Protestant
		if(iPlayer == iSweden):
			if(pSweden.getStateReligion() == iProtestantism and city.isHasReligion(iCatholicism)):
				iRazed = pSweden.getUHVCounter(1)+1
				pSweden.setUHVCounter(1,iRazed)
				if(iRazed >= 5):
					pSweden.setUHV( 1, 1 )
					pSweden.changeStabilityBase( iCathegoryExpansion, 3 )


	def onPillageImprovement( self, iPillager, iVictim, iImprovement, iRoute, iX, iY ):
		# Norway UHV 1: Going Viking
		if ( iPillager == iNorway and iRoute == -1 ):
			if ( gc.getMap().plot( iX, iY ).getOwner() != iNorway ):
				pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + 1 )


	def onCombatResult(self, argsList):
		pWinningUnit,pLosingUnit = argsList
		cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())

		# Norway UHV 1: Going Viking
		if ( pWinningUnit.getOwner() == iNorway ):
			if (cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_SEA")):
				pNorway.setUHVCounter( 2, pNorway.getUHVCounter( 2 ) + 2 )


	def onTechAcquired(self, iTech, iPlayer):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		# England UHV 3:
		if ( iTech == iIndustrialTech ):
			if ( pEngland.getUHV( 2 ) == -1 ):
				if ( iPlayer == iEngland ):
					pEngland.setUHV( 2, 1 )
					pEngland.changeStabilityBase( iCathegoryExpansion, 3 )
				else:
					pEngland.setUHV( 2, 0 )


	def onBuildingBuilt(self, iPlayer, iBuilding):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		iGameTurn = gc.getGame().getGameTurn()

		# Kiev UHV 1:
		if ( iPlayer == iKiev ):
			if ( pKiev.isAlive() and pKiev.getUHV( 0 ) == -1 ):
				if ( iBuilding == iOrthodoxMonastery or iBuilding == iOrthodoxCathedral ):
					iBuildSoFar = pKiev.getUHVCounter( 0 )
					iCathedralCounter = iBuildSoFar % 100
					iMonasteryCounter = iBuildSoFar / 100
					if ( iBuilding == iOrthodoxMonastery ):
						iMonasteryCounter += 1
					else:
						iCathedralCounter += 1
					if ( iCathedralCounter >= 2 and iMonasteryCounter >= 8 ):
						pKiev.setUHV( 0, 1 )
						pKiev.changeStabilityBase( iCathegoryExpansion, 3 )
					pKiev.setUHVCounter( 0, 100 * iMonasteryCounter + iCathedralCounter )

		# Poland UHV 3:
		# HHG: Polish UHV3 now uses Wonder Kazimierz with maximum value 99, and all other buildings have boundary checks
		elif ( iPlayer == iPoland ):
			if ( pPoland.isAlive() and pPoland.getUHV( 2 ) == -1 ):
				lBuildingList = [iCatholicCathedral,iOrthodoxCathedral,iProtestantCathedral,iJewishQuarter,iKazimierz]
				if ( iBuilding in lBuildingList):
					iCounter = pPoland.getUHVCounter( 2 )
					iCathCath = ( iCounter / 10000 ) % 10
					iOrthCath = ( iCounter / 1000 ) % 10
					iProtCath = ( iCounter / 100 ) % 10
					iJewishQu = iCounter % 100
					if ( iBuilding == iCatholicCathedral and iCathCath < 9 ):
						iCathCath += 1
					elif ( iBuilding == iOrthodoxCathedral and iOrthCath < 9 ):
						iOrthCath += 1
					elif ( iBuilding == iProtestantCathedral and iProtCath < 9 ):
						iProtCath += 1
					elif ( iBuilding == iKazimierz ):
						iJewishQu = 99
					elif ( iBuilding == iJewishQuarter and iJewishQu < 99 ):
						iJewishQu += 1
					if ( iCathCath >= 3 and iOrthCath >= 3 and iProtCath >= 2 and iJewishQu >= 2 ):
						pPoland.setUHV( 2, 1 )
						pPoland.changeStabilityBase( iCathegoryExpansion, 3 )
					iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
					pPoland.setUHVCounter( 2, iCounter )

		# Genoa UHV 2:
		elif ( iPlayer == iGenoa ):
			if ( pGenoa.isAlive() and pGenoa.getUHV( 1 ) == -1 ):
				if ( iBuilding == iGenoaBank ):
					iCounter = pGenoa.getUHVCounter( 1 )
					iCorps = iCounter % 100
					iBanks = iCounter / 100 + 1
					if ( iBanks >= 8 and iCorps >= 2 ):
						pGenoa.setUHV( 1, 1 )
						pGenoa.changeStabilityBase( iCathegoryExpansion, 3 )
					pGenoa.setUHVCounter( 1, 100 * iBanks + iCorps )

		# Cordoba UHV 2:
		if ( iBuilding in tCordobaWonders ):
			if (pCordoba.isAlive() and pCordoba.getUHV( 1 ) == -1 ):
				if (iPlayer == iCordoba):
					iWondersBuilt = pCordoba.getUHVCounter( 1 )
					pCordoba.setUHVCounter( 1, iWondersBuilt + 1 )
					if (iWondersBuilt == 2): # so we already had 2 wonders
						pCordoba.setUHV( 1, 1 )
						pCordoba.changeStabilityBase( iCathegoryExpansion, 3 )
				else:
					pCordoba.setUHV( 1, 0 )


	def onProjectBuilt(self, iPlayer, iProject):
		bColony = self.isProjectAColony( iProject )
		# Absinthe: note that getProjectCount (thus getNumRealColonies too) won't count the latest project/colony (which is currently buing built) if called from this function
		#			way more straightforward, and also faster to use the UHVCounters for the UHV checks

		# Venice UHV 3:
		if ( pVenecia.getUHV( 2 ) == -1 and iProject != iColVinland ):
			if bColony:
				if ( iPlayer == iVenecia ):
					pVenecia.setUHV( 2, 1 )
					pVenecia.changeStabilityBase( iCathegoryExpansion, 3 )
				else:
					pVenecia.setUHV( 2, 0 )

		# France UHV 3:
		if ( iPlayer == iFrankia ):
			if bColony:
				pFrankia.setUHVCounter( 2, pFrankia.getUHVCounter( 2 ) + 1 )
				if ( pFrankia.getUHV( 2 ) == -1 ):
					if ( pFrankia.getUHVCounter( 2 ) >= 5 ):
						pFrankia.setUHV( 2, 1 )
						pFrankia.changeStabilityBase( iCathegoryExpansion, 3 )

		# England UHV 2:
		elif ( iPlayer == iEngland ):
			if bColony:
				pEngland.setUHVCounter( 1, pEngland.getUHVCounter( 1 ) + 1 )
				if ( pEngland.getUHV( 1 ) == -1 ):
					if ( pEngland.getUHVCounter( 1 ) >= 7 ):
						pEngland.setUHV( 1, 1 )
						pEngland.changeStabilityBase( iCathegoryExpansion, 3 )

		# Spain UHV 2: this is only for the Main Screen counter
		elif ( iPlayer == iSpain ):
			if bColony:
				pSpain.setUHVCounter( 1, pSpain.getUHVCounter( 1 ) + 1 )

		# Portugal UHV 3:
		elif ( iPlayer == iPortugal ):
			if bColony:
				pPortugal.setUHVCounter( 2, pPortugal.getUHVCounter( 2 ) + 1 )
				if ( pPortugal.getUHV( 2 ) == -1 ):
					if ( pPortugal.getUHVCounter( 2 ) >= 5 ):
						pPortugal.setUHV( 2, 1 )
						pPortugal.changeStabilityBase( iCathegoryExpansion, 3 )

		# Dutch UHV 2:
		elif ( iPlayer == iDutch ):
			if bColony:
				pDutch.setUHVCounter( 1, pDutch.getUHVCounter( 1 ) + 1 )
			if ( pDutch.getUHV( 1 ) == -1 ):
				if ( pDutch.getUHVCounter( 1 ) >= 3 ):
					iWestCompany = teamDutch.getProjectCount(iWestIndiaCompany)
					iEastCompany = teamDutch.getProjectCount(iEastIndiaCompany)
					# if the companies are already built previously, or currently being built (one of them is the current project)
					if ( iProject == iWestIndiaCompany or iWestCompany == 1 ):
						if ( iProject == iEastIndiaCompany or iEastCompany == 1):
							pDutch.setUHV( 1, 1 )
							pDutch.changeStabilityBase( iCathegoryExpansion, 3 )

		# Denmark UHV 3:
		elif ( iPlayer == iDenmark ):
			if bColony:
				pDenmark.setUHVCounter( 2, pDenmark.getUHVCounter( 2 ) + 1 )
			if ( pDenmark.getUHV( 2 ) == -1 ):
				if ( pDenmark.getUHVCounter( 2 ) >= 3 ):
					iWestCompany = teamDenmark.getProjectCount(iWestIndiaCompany)
					iEastCompany = teamDenmark.getProjectCount(iEastIndiaCompany)
					# if the companies are already built previously, or currently being built (one of them is the current project)
					if ( iProject == iWestIndiaCompany or iWestCompany == 1 ):
						if ( iProject == iEastIndiaCompany or iEastCompany == 1):
							pDenmark.setUHV( 2, 1 )
							pDenmark.changeStabilityBase( iCathegoryExpansion, 3 )


	def onCorporationFounded(self, iPlayer ):
		# Genoa UHV 2:
		self.setCorporationsFounded( self.getCorporationsFounded() + 1 )
		if ( iPlayer == iGenoa ):
			iCounter = pGenoa.getUHVCounter( 1 )
			iCorps = iCounter % 100 + 1
			iBanks = iCounter / 100
			if ( iBanks >= 8 and iCorps >= 2 ):
				pGenoa.setUHV( 1, 1 )
				pGenoa.changeStabilityBase( iCathegoryExpansion, 3 )
			pGenoa.setUHVCounter( 1, 100 * iBanks + iCorps )
		if ( self.getCorporationsFounded() == 7 and pGenoa.getUHV( 1 ) == -1 ):
			iCounter = pGenoa.getUHVCounter( 1 )
			iCorps = iCounter % 100 + 1
			if ( iCorps < 2 ):
				pGenoa.setUHV( 1, 0 )


	def getOwnedLuxes( self, pPlayer ):
		iCount = 0
		iCount += pPlayer.countOwnedBonuses( iSheep )
		iCount += pPlayer.countOwnedBonuses( iDye )
		iCount += pPlayer.countOwnedBonuses( iFur )
		iCount += pPlayer.countOwnedBonuses( iGems )
		iCount += pPlayer.countOwnedBonuses( iGold )
		iCount += pPlayer.countOwnedBonuses( iIncense )
		iCount += pPlayer.countOwnedBonuses( iIvory )
		iCount += pPlayer.countOwnedBonuses( iSilk )
		iCount += pPlayer.countOwnedBonuses( iSilver )
		iCount += pPlayer.countOwnedBonuses( iSpices )
		iCount += pPlayer.countOwnedBonuses( iWine )
		iCount += pPlayer.countOwnedBonuses( iHoney )
		iCount += pPlayer.countOwnedBonuses( iWhale )
		iCount += pPlayer.countOwnedBonuses( iAmber )
		iCount += pPlayer.countOwnedBonuses( iCotton )
		iCount += pPlayer.countOwnedBonuses( iCoffee )
		iCount += pPlayer.countOwnedBonuses( iTea )
		iCount += pPlayer.countOwnedBonuses( iTobacco )
		#iCount += pPlayer.countOwnedBonuses( iRelic )
		return iCount


	def getOwnedGrain( self, pPlayer ):
		iCount = 0
		iCount += pPlayer.countOwnedBonuses( iWheat )
		iCount += pPlayer.countOwnedBonuses( iBarley )
		return iCount


	def isProjectAColony( self, iProject ):
		if (iProject >= iNumNotColonies):
			return True
		else:
			return False


	def getNumRealColonies(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		tPlayer = gc.getTeam(pPlayer.getTeam())
		iCount = 0
		for iProject in range( iNumNotColonies, iNumProjects ):
			if tPlayer.getProjectCount(iProject) > 0:
				iCount += 1
		return iCount

	def getTerritoryPercentEurope(self, iPlayer, bReturnTotal = False):
		iTotal = 0
		iCount = 0
		for x in range(iMapMaxX):
			for y in range(iMapMaxY):
				plot = gc.getMap().plot(x,y)
				if plot.isWater(): continue
				iProvinceID = rfcemaps.tProinceMap[plot.getY()][plot.getX()]
				if iProvinceID in lNotEurope: continue
				iTotal += 1
				if plot.getOwner() == iPlayer:
					iCount += 1
		if bReturnTotal:
			return iCount, iTotal
		return iCount

	def checkByzantium( self, iGameTurn ):

		# UHV 1: Make Constantinople the largest and most cultured city in 1025
		if ( iGameTurn == i1025AD and pByzantium.getUHV( 0 ) == -1 ):
			if ( gc.isLargestCity( tCapitals[iByzantium][0], tCapitals[iByzantium][1] ) and gc.isTopCultureCity( tCapitals[iByzantium][0], tCapitals[iByzantium][1] ) and gc.getMap().plot( tCapitals[iByzantium][0], tCapitals[iByzantium][1] ).getPlotCity().getOwner() == iByzantium ):
				pByzantium.setUHV( 0, 1 )
				pByzantium.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pByzantium.setUHV( 0, 0 )

		# UHV 2: Keep or reconquer Constantinople, Thrace, Thessaloniki, Moesia, Macedonia, Serbia, Arberia, Epirus, Thessaly, Morea, Colonea, Antiochia, Charsianon, Cilicia, Armeniakon, Anatolikon, Paphlagonia, Thrakesion and Opsikion in 1282
		if ( iGameTurn == i1282AD and pByzantium.getUHV( 1 ) == -1 ):
			bOwn = True
			for iProv in tByzantumControl:
				if ( pByzantium.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pByzantium.setUHV( 1, 1 )
				pByzantium.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pByzantium.setUHV( 1, 0 )

		# UHV 3: Be the richest empire in the world in 1453
		if ( iGameTurn == i1453AD and pByzantium.getUHV( 2 ) == -1 ):
			iGold = pByzantium.getGold()
			bMost = True
			for iCiv in range( iNumPlayers ):
				if ( iCiv != iByzantium and gc.getPlayer( iCiv ).isAlive() ):
					if (gc.getPlayer(iCiv).getGold() > iGold):
						bMost = False
			if ( bMost ):
				 pByzantium.setUHV( 2, 1 )
				 pByzantium.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				 pByzantium.setUHV( 2, 0 )


	def checkFrankia( self, iGameTurn ):

		# UHV 1: Charlemagne's Empire
		if ( iGameTurn <= i840AD and pFrankia.getUHV(0) == -1 ):
			bCharlemagneEmpire = True
			for iProv in tFrankControl:
				iHave = pFrankia.getProvinceCurrentState( iProv )
				if ( iHave < iProvinceConquer ):
					bCharlemagneEmpire = False
					break
			if ( bCharlemagneEmpire ):
				pFrankia.setUHV( 0, 1 )
				pFrankia.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i840AD ):
				pFrankia.setUHV( 0, 0 )

		# UHV 2: Control Jerusalem in 1291
		if (iGameTurn == i1291AD and pFrankia.getUHV(1) == -1 ):
			pJPlot = gc.getMap().plot( tJerusalem[0], tJerusalem[1] )
			if ( pJPlot.isCity()):
				if ( pJPlot.getPlotCity().getOwner() == iFrankia ):
					pFrankia.setUHV( 1, 1 )
					pFrankia.changeStabilityBase( iCathegoryExpansion, 3 )
				else:
					pFrankia.setUHV( 1, 0 )
			else:
				pFrankia.setUHV( 1, 0 )

		# UHV 3: Build 5 Colonies
		# handled in the onProjectBuilt function


	def checkArabia( self, iGameTurn ):

		# UHV 1: Conquer all territories from Egypt to Asia Minor by 955 AD
		if ( iGameTurn == i955AD and pArabia.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tArabiaControlI:
				if ( pArabia.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pArabia.setUHV( 0, 1 )
				pArabia.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pArabia.setUHV( 0, 0 )

		# UHV 2: Conquer all territories from Oran to Asia Minor by 1291
		if ( iGameTurn == i1291AD and pArabia.getUHV( 1 ) == -1 ):
			bConq = True
			for iProv in tArabiaControlII:
				if ( pArabia.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pArabia.setUHV( 1, 1 )
				pArabia.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pArabia.setUHV( 1, 0 )

		# UHV 3: Spread Islam to at least 35% of the population of Europe
		if ( pArabia.getUHV( 2 ) == -1 ):
			iPerc = gc.getGame().calculateReligionPercent( iIslam )
			if ( iPerc >= 35 ):
				pArabia.setUHV( 2, 1 )
				pArabia.changeStabilityBase( iCathegoryExpansion, 3 )


	def checkBulgaria( self, iGameTurn ):

		# UHV 1: Conquer Moesia, Thrace, Macedonia, Serbia, Arberia, Thessaloniki and Constantinople by 917
		if ( iGameTurn <= i917AD and pBulgaria.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tBulgariaControl:
				if ( pBulgaria.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pBulgaria.setUHV( 0, 1 )
				pBulgaria.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i917AD ):
				pBulgaria.setUHV( 0, 0 )

		# UHV 2: Accumulate at least 100 Orthodox Faith Points by 1259
		if ( iGameTurn <= i1259AD and pBulgaria.getUHV( 1 ) == -1 ):
			if ( pBulgaria.getFaith() >= 100 ):
				pBulgaria.setUHV( 1, 1 )
				pBulgaria.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i1259AD ):
				pBulgaria.setUHV( 1, 0 )

		# UHV 3: Do not lose a city to barbarians (Mongols), Byzantines, or Ottomans before 1393
		# Controlled in the onCityAcquired function
		if ( iGameTurn == i1393AD and pBulgaria.getUHV( 2 ) == -1 ):
			pBulgaria.setUHV( 2, 1 )
			pBulgaria.changeStabilityBase( iCathegoryExpansion, 3 )


	def checkCordoba( self, iGameTurn ):

		# UHV 1: Make Cordoba the largest city in the world in 961
		if ( iGameTurn == i961AD and pCordoba.getUHV(0) == -1 ):
			if ( gc.isLargestCity( tCapitals[iCordoba][0], tCapitals[iCordoba][1] ) and gc.getMap().plot( tCapitals[iCordoba][0], tCapitals[iCordoba][1] ).getPlotCity().getOwner() == iCordoba ):
				pCordoba.setUHV( 0, 1 )
				pCordoba.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pCordoba.setUHV( 0, 0 )

		# UHV 2: Build the Alhambra, the Gardens of Al-Andalus, and La Mezquita by 1309
		# Controlled in the onBuildingBuilt function
		if ( iGameTurn == i1309AD and pCordoba.getUHV(1) == -1 ):
			pCordoba.setUHV( 1, 0 )

		# UHV 3: Have Islam spread in every city in Andalusia, Galicia, Leon, Castile, Navarre, Lusitania, Catalonia, Aragon, La Mancha and Valencia in 1492
		if ( iGameTurn == i1492AD and pCordoba.getUHV(2) == -1 ):
			bIslamized = True
			for iProv in tCordobaIslamize:
				if ( not ( pCordoba.provinceIsSpreadReligion( iProv, iIslam ) ) ):
					bIslamized = False
					break
			if ( bIslamized ):
				pCordoba.setUHV( 2, 1 )
				pCordoba.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pCordoba.setUHV( 2, 0 )


	def checkNorway( self, iGameTurn ):

		# Old UHVs: explore all water tiles
		#if ( iGameTurn == i1009AD and pNorway.getUHV( 0 ) == -1 ):
		#	if ( gc.canSeeAllTerrain( iNorway, iTerrainOcean ) ):
		#		pNorway.setUHV( 0, 1 )
		#	else:
		#		pNorway.setUHV( 0, 0 )

		# UHV 1: Gain 80 Viking points by 1066
		# Counted in the onCityAcquired, onPillageImprovement and onCombatResult functions
		if ( iGameTurn <= i1066AD and pNorway.getUHV( 0 ) == -1 ):
			if ( pNorway.getUHVCounter( 2 ) >= 80 ): # It's still counter 2, for the sake of convenience and confusion
				pNorway.setUHV( 0, 1 )
				pNorway.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i1066AD ):
				pNorway.setUHV( 0, 0 )

		# UHV 2: Conquer The Isles, Ireland, Mercia, Normandy, Iceland and build Vinland by 1263
		if ( iGameTurn <= i1263AD and pNorway.getUHV( 1 ) == -1 ):
			bConq = True
			for iProv in tNorwayControl:
				if(pNorway.getProvinceCurrentState( iProv ) < iProvinceConquer):
					bConq = False
					break
			if(bConq and teamNorway.getProjectCount(iColVinland) >= 1):
				pNorway.setUHV( 1, 1 )
				pNorway.changeStabilityBase( iCathegoryExpansion, 3 )
			elif(iGameTurn == i1263AD):
				pNorway.setUHV( 1, 0 )

		# UHV 3: Have higher score than Sweden, Denmark, Scotland, England, Germany and France in 1320
		if ( iGameTurn == i1320AD and pNorway.getUHV(2) == -1 ):
			iNorwayRank = gc.getGame().getTeamRank(iNorway)
			bIsOnTop = True
			for iTestPlayer in tNorwayOutrank:
				if(gc.getGame().getTeamRank(iTestPlayer) < iNorwayRank):
					bIsOnTop = False
					break
			if(bIsOnTop):
				pNorway.setUHV( 2, 1 )
				pNorway.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pNorway.setUHV( 2, 0 )


	def checkDenmark(self,iGameTurn):

		# UHV 1: Control Denmark, Skaneland, Götaland, Svealand, Mercia, London, Northumbria and East Anglia in 1050
		if ( iGameTurn == i1050AD and pDenmark.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tDenmarkControlI:
				if ( pDenmark.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pDenmark.setUHV( 0, 1 )
				pDenmark.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pDenmark.setUHV( 0, 0 )

		# UHV 2: Control Denmark, Norway, Vestfold, Skaneland, Götaland, Svealand, Norrland, Gotland, Österland, Estonia and Iceland in 1523
		if ( iGameTurn == i1523AD and pDenmark.getUHV( 1 ) == -1 ):
			bConq = True
			for iProv in tDenmarkControlIII:
				if ( pDenmark.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pDenmark.setUHV( 1, 1 )
				pDenmark.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pDenmark.setUHV( 1, 0 )

		# UHV 3: Get 3 Colonies and complete both Trading Companies
		# handled in the onProjectBuilt function


	def checkVenecia( self, iGameTurn ):

		# UHV 1: Control the Adriatic and some Mediterranean islands in 1004
		if ( iGameTurn <= i1004AD and pVenecia.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tVenetianControl:
				if ( pVenecia.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pVenecia.setUHV( 0, 1 )
				pVenecia.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i1004AD ):
				pVenecia.setUHV( 0, 0 )

		# UHV 2: Conquer Constantinople by 1204
		if ( iGameTurn <= i1204AD and pVenecia.getUHV( 1 ) == -1 ):
			if ( pVenecia.getProvinceCurrentState( iP_Constantinople ) >= iProvinceConquer ):
				pVenecia.setUHV( 1, 1 )
				pVenecia.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i1204AD ):
				pVenecia.setUHV( 1, 0 )

		# UHV 3: Be the first to build a modern Colony (so Vinland doesn't count)
		# handled in the onProjectBuilt function


	def checkBurgundy( self, iGameTurn ):

		# UHV 1: Produce 10,000 culture points by 1336
		iCulture = pBurgundy.getUHVCounter( 0 ) + pBurgundy.countCultureProduced()
		pBurgundy.setUHVCounter( 0, iCulture )
		if ( iGameTurn <= i1336AD and pBurgundy.getUHV( 0 ) == -1 ):
			if ( iCulture >= 10000 ):
				pBurgundy.setUHV( 0, 1 )
				pBurgundy.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				if ( iGameTurn == i1336AD ):
					pBurgundy.setUHV( 0, 0 )

		# UHV 2: Conquer Burgundy, Provence, Picardy, Flanders, Champagne and Lorraine in 1376
		if ( iGameTurn == i1376AD and pBurgundy.getUHV( 1 ) == -1 ):
			bOwn = True
			for iProv in tBurgundyControl:
				if ( pBurgundy.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pBurgundy.setUHV( 1, 1 )
				pBurgundy.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pBurgundy.setUHV( 1, 0 )

		# UHV 3: Have higher score than France, England and Germany in 1473
		if ( iGameTurn == i1473AD and pBurgundy.getUHV(2) == -1 ):
			iBurgundyRank = gc.getGame().getTeamRank(iBurgundy)
			bIsOnTop = True
			for iTestPlayer in tBurgundyOutrank:
				if ( gc.getGame().getTeamRank(iTestPlayer) < iBurgundyRank ):
					bIsOnTop = False
					break
			if ( bIsOnTop ):
				pBurgundy.setUHV( 2, 1 )
				pBurgundy.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pBurgundy.setUHV( 2, 0 )


	def checkGermany( self, iGameTurn ):

		# Old UHVs: Have most Catholic FP in 1077 (Walk to Canossa)
		#			Have 3 vassals

		# UHV 1: Control Lorraine, Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Lombardy and Tuscany in 1167
		if ( iGameTurn == i1167AD and pGermany.getUHV( 0 ) == -1 ):
			bOwn = True
			for iProv in tGermanyControl:
				if ( pGermany.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pGermany.setUHV( 0, 1 )
				pGermany.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pGermany.setUHV( 0, 0 )

		# UHV 2: Start the Reformation (Found Protestantism)
		# Controlled in the onReligionFounded function

		# UHV 3: Conquer Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Flanders, Pomerania, Silesia, Bohemia, Moravia and Austria in 1648
		if ( iGameTurn == i1648AD and pGermany.getUHV( 2 ) == -1 ):
			bOwn = True
			for iProv in tGermanyControlII:
				if ( pGermany.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pGermany.setUHV( 2, 1 )
				pGermany.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pGermany.setUHV( 2, 0 )


	def checkNovgorod( self, iGameTurn ):

		# UHV 1: Control Novgorod, Karelia, Estonia and Livonia in 1250
		if ( iGameTurn == i1250AD and pNovgorod.getUHV( 0 ) == -1 ):
			bOwn = True
			for iProv in tNovgorodControl:
				if ( pNovgorod.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pNovgorod.setUHV( 0, 1 )
				pNovgorod.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pNovgorod.setUHV( 0, 0 )

		# UHV 2: Control twelve sources of fur by 1397
		if (pNovgorod.getUHV( 1 ) == -1):
			if (iGameTurn <= i1397AD):
				if (pNovgorod.countOwnedBonuses(iFur) >= 12):
					pNovgorod.setUHV( 1, 1 )
					pNovgorod.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pNovgorod.setUHV( 1, 0 )

		# UHV 3: Have seven cities in Karelia and Vologda in 1478
		if (iGameTurn == i1478AD and pNovgorod.getUHV( 2 ) == -1 ):
			iNumCities = 0
			for iProv in tNovgorodControlII:
				iNumCities += pNovgorod.getProvinceCityCount( iProv )
			if ( iNumCities >= 7 ):
				pNovgorod.setUHV( 2, 1 )
				pNovgorod.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pNovgorod.setUHV( 2, 0 )


	def checkKiev( self, iGameTurn ):

		# UHV 1: Build 2 Orthodox cathedrals and 8 Orthodox monasteries by 1250
		# Controlled in the onBuildingBuilt function
		if ( iGameTurn == i1250AD+1 and pKiev.getUHV( 0 ) == -1 ):
			pKiev.setUHV( 0, 0 )

		# UHV 2: Conquer 10 provinces in Eastern Europe
		if ( iGameTurn == i1288AD and pKiev.getUHV( 1 ) == -1 ):
			iConq = 0
			for iProv in tKievControl:
				if ( pKiev.getProvinceCurrentState( iProv ) >= iProvinceConquer ):
					iConq += 1
			if ( iConq > 9 ):
				pKiev.setUHV( 1, 1 )
				pKiev.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pKiev.setUHV( 1, 0 )

		# UHV 3: Produce 25000 food by 1300
		iFood = pKiev.getUHVCounter( 2 ) + pKiev.calculateTotalYield(YieldTypes.YIELD_FOOD)
		pKiev.setUHVCounter( 2, iFood )
		if ( iGameTurn <= i1300AD and pKiev.getUHV( 2 ) == -1 ):
			if ( iFood > 25000 ):
				pKiev.setUHV( 2, 1 )
				pKiev.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i1300AD ):
				pKiev.setUHV( 2, 0 )


	def checkHungary( self, iGameTurn ):

		# UHV 1: Allow no Ottoman cities in Europe in 1444
		if ( iGameTurn == i1444AD and pHungary.getUHV( 0 ) == -1 ):
			bClean = True
			if ( pTurkey.isAlive() ):
				for iProv in tHungarynControl:
					if ( pTurkey.getProvinceCityCount( iProv ) > 0):
						bClean = False
						break
			if ( bClean ):
				pHungary.setUHV( 0, 1 )
				pHungary.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pHungary.setUHV( 0, 0 )

		# UHV 2: Control the most territory in Europe in 1490
		if ( iGameTurn == i1490AD and pHungary.getUHV( 1 ) == -1 ):
			bMost = True
			iCount = self.getTerritoryPercentEurope(iHungary)
			for iOtherPlayer in range(iNumPlayers):
				if not gc.getPlayer(iOtherPlayer).isAlive() or iOtherPlayer == iHungary: continue
				iOtherCount = self.getTerritoryPercentEurope(iOtherPlayer)
				if iOtherCount >= iCount:
					bMost = False
					break
			if bMost:
				pHungary.setUHV( 1, 1 )
				pHungary.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pHungary.setUHV( 1, 0 )

		# UHV 3: Be the first to adopt Free Religion
		if ( pHungary.getUHV( 2 ) == -1 ):
			iCivic = pHungary.getCivics(4)
			if ( iCivic == iCivicFreeReligion ):
				pHungary.setUHV( 2, 1 )
				pHungary.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				for iPlayer in range( iNumMajorPlayers ):
					pPlayer = gc.getPlayer( iPlayer )
					if ( pPlayer.isAlive() and pPlayer.getCivics(4) == iCivicFreeReligion ):
						pHungary.setUHV( 2, 0 )


	def checkSpain( self, iGameTurn ):

		# UHV 1: Reconquista (Make Catholicism the only religion in the Iberian peninsula in 1492 and spread catholicism to all the cities)
		if ( iGameTurn == i1492AD and pSpain.getUHV( 0 ) == -1 ):
			bConverted = True
			for iProv in tSpainConvert:
				if ( not ( pSpain.provinceIsConvertReligion( iProv, iCatholicism ) ) ):
					bConverted = False
					break
			if ( bConverted ):
				pSpain.setUHV( 0, 1 )
				pSpain.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pSpain.setUHV( 0, 0 )

		# UHV 2: Have more Colonies than any other nation in 1588AD (while having at least 3)
		if ( iGameTurn == i1588AD and pSpain.getUHV( 1 ) == -1 ):
			bMost = True
			iSpainColonies = self.getNumRealColonies(iSpain)
			for iPlayer in range( iNumPlayers ):
				if ( iPlayer != iSpain ):
					pPlayer = gc.getPlayer( iPlayer )
					if ( pPlayer.isAlive() and self.getNumRealColonies(iPlayer) >= iSpainColonies ):
						bMost = False
			if ( bMost and iSpainColonies >= 3 ):
				pSpain.setUHV( 1, 1 )
				pSpain.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pSpain.setUHV( 1, 0 )

		# UHV 3: Ensure that the Catholic nations have more population and more land than any other religion in 1648
		if ( iGameTurn == i1648AD and pSpain.getUHV( 2 ) == -1 ):
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

			iCathLand = lLand[ iCatholicism ]
			iCathPop  = lPop[ iCatholicism ]

			bWon = True

			for iReligion in range( iNumReligions + 1 ):
				if ( iReligion != iCatholicism ):
					if ( lLand[ iReligion ] > iCathLand ):
						bWon = False
					if ( lPop[ iReligion ] > iCathPop ):
						bWon = False

			if ( pSpain.getStateReligion() == iCatholicism and bWon ):
				pSpain.setUHV( 2, 1 )
				pSpain.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pSpain.setUHV( 2, 0 )


	def checkScotland( self, iGameTurn ):

		# UHV 1: Have 10 Forts and 4 Castles by 1296.
		if ( iGameTurn <= i1296AD and pScotland.getUHV( 0 ) == -1):
			iForts = pScotland.getImprovementCount( iImprovementFort )
			iCastles = pScotland.countNumBuildings( iCastle )
			print("Forts:",iForts,"Castles:",iCastles)
			if( iForts >= 10 and iCastles >= 4 ):
				pScotland.setUHV( 0, 1 )
				pScotland.changeStabilityBase( iCathegoryExpansion, 3 )
		if ( iGameTurn == i1296AD and pScotland.getUHV( 0 ) == -1):
			pScotland.setUHV( 0, 0 )

		# UHV 2: Have 2500 attitude points with France by 1560. Attitude points go up every turn depending on relations
		if ( iGameTurn <= i1560AD and pFrankia.isAlive() and pScotland.getUHV( 1 ) == -1):
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
			if(iNewScore >= 2500):
				pScotland.setUHV( 1, 1 )
				pScotland.changeStabilityBase( iCathegoryExpansion, 3 )
		elif ( iGameTurn > i1560AD and pScotland.getUHV( 1 ) == -1 ):
			pScotland.setUHV( 1, 0 )

		# UHV 3: Control Scotland, The Isles, Ireland, Wales, Brittany and Galicia in 1700.
		if ( iGameTurn == i1700AD and pScotland.getUHV( 2 ) == -1 ):
			bConq = True
			for iProv in tScotlandControl:
				if ( pScotland.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pScotland.setUHV( 2, 1 )
				pScotland.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pScotland.setUHV( 2, 0 )


	def checkPoland( self, iGameTurn ):

		# Old UHVs: Don't lose cities until 1772 AD or conquer Russia until 1772 AD
		#			Vassalize Russia, Germany and Austria

		# UHV 1: Food production between 1500 and 1520 AD
		if ((iGameTurn >= i1500AD) and (iGameTurn <= i1520AD) and pPoland.getUHV( 0 ) == -1 ):
			iAgriculturePolish = pPoland.calculateTotalYield(YieldTypes.YIELD_FOOD)
			bFood = True
			for iPlayer in range( iNumMajorPlayers ):
				if ( gc.getPlayer( iPlayer ).calculateTotalYield(YieldTypes.YIELD_FOOD ) > iAgriculturePolish ):
					bFood = False
					break
			if (bFood):
				pPoland.setUHV( 0, 1 )
				pPoland.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i1520AD ):
				pPoland.setUHV( 0, 0 )

		# UHV 2: Control 12 cities in the given provinces in 1600 AD
		if (iGameTurn == i1600AD and pPoland.getUHV( 1 ) == -1 ):
			iNumCities = 0
			for iProv in tPolishControl:
				iNumCities += pPoland.getProvinceCityCount( iProv )
			if ( iNumCities >= 12 ):
				pPoland.setUHV( 1, 1 )
				pPoland.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pPoland.setUHV( 1, 0 )

		# UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
		# Controlled in the onBuildingBuilt and onCityAcquired functions


	def checkGenoa( self, iGameTurn ):

		# UHV 1: Control Corsica, Sardinia, Crete, Rhodes and Crimea in 1566
		if ( iGameTurn == i1566AD and pGenoa.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tGenoaControl:
				if ( pGenoa.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pGenoa.setUHV( 0, 1 )
				pGenoa.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pGenoa.setUHV( 0, 0 )

		# UHV 2: Found 2 Corporations and build 8 Banks
		# Controlled in the onBuildingBuilt and onCorporationFounded functions

		# UHV 3: Have the largest total amount of commerce from foreign Trade Route Exports and Imports in 1640
		if ( iGameTurn == i1640AD and pGenoa.getUHV( 2 ) == -1 ):
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
				pGenoa.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pGenoa.setUHV( 2, 0 )


	def checkMorocco( self, iGameTurn ):

		# UHV 1: Control Morocco, Marrakesh, Fez, Tetouan, Oran, Algiers, Ifriqiya, Tripolitania, Andalusia, and Valencia in 1227AD.
		if (iGameTurn == i1227AD and pMorocco.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tMoroccoControl:
				if ( pMorocco.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pMorocco.setUHV( 0, 1 )
				pMorocco.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pMorocco.setUHV( 0, 0 )

		# UHV 2: Have 5000 culture in each of three cities in 1465AD.
		if (iGameTurn == i1465AD and pMorocco.getUHV( 1 ) == -1):
			iGoodCities = 0
			apCityList = PyPlayer(iMorocco).getCityList()
			for pLoopCity in apCityList:
				pCity = pLoopCity.GetCy()
				if(pCity.getCulture(iMorocco) >= 5000):
					iGoodCities += 1;

			if(iGoodCities >= 3):
				pMorocco.setUHV( 1, 1 )
				pMorocco.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pMorocco.setUHV( 1, 0 )

		# UHV 3: Collapse or vassalize Portugal, Spain, and Aragon by 1578AD.
		if (iGameTurn >= i1164AD and iGameTurn <= i1578AD and pMorocco.getUHV( 2 ) == -1):
			bConq = True
			if ( pSpain.isAlive() and (not teamSpain.isVassal( teamMorocco.getID() )) ):
				bConq = False
			elif ( pPortugal.isAlive() and (not teamPortugal.isVassal( teamMorocco.getID() )) ):
				bConq = False
			elif ( pAragon.isAlive() and (not teamAragon.isVassal( teamMorocco.getID() )) ):
				bConq = False

			if( bConq ):
				pMorocco.setUHV( 2, 1 )
				pMorocco.changeStabilityBase( iCathegoryExpansion, 3 )
		elif (iGameTurn > i1578AD and pMorocco.getUHV( 2 ) == -1):
			pMorocco.setUHV( 2, 0 )


	def checkEngland( self, iGameTurn ):

		# UHV 1: Conquer London, Wessex, East Anglia, Mercia, Northumbria, Scotland, Wales, Ireland, Normandy, Picardy, Bretagne, Il-de-France, Aquitania and Orleans in 1452
		if ( iGameTurn == i1452AD and pEngland.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tEnglandControl:
				if ( pEngland.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pEngland.setUHV( 0, 1 )
				pEngland.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pEngland.setUHV( 0, 0 )

		# UHV 2: Build 7 Colonies
		# Controlled in the onProjectBuilt function

		# UHV 3: Be the first to enter the Industrial age
		# Controlled in the onTechAcquired function


	def checkPortugal( self, iGameTurn ):

		# UHV 1: Settle 3 cities on the Azores, Canaries and Madeira and 2 in Morocco, Tetouan and Oran
		# Controlled in the onCityBuilt function

		# UHV 2: Do not lose a city before 1640
		# Controlled in the onCityAcquired function
		if ( iGameTurn == i1640AD and pPortugal.getUHV( 1 ) == -1 ):
			pPortugal.setUHV( 1, 1 )
			pPortugal.changeStabilityBase( iCathegoryExpansion, 3 )

		# UHV 3: Build 5 Colonies
		# Controlled in the onProjectBuilt function


	def checkAragon( self, iGameTurn ):

		# UHV 1: Control Catalonia, Valencia, Balears and Sicily in 1282
		if ( iGameTurn == i1282AD and pAragon.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tAragonControlI:
				if ( pAragon.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pAragon.setUHV( 0, 1 )
				pAragon.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pAragon.setUHV( 0, 0 )

		# UHV 2: Have 12 seaports in 1444
		if ( iGameTurn == i1444AD ):
			iPorts = pAragon.countNumBuildings(iAragonSeaport)
			print("Ports:",iPorts)
			if( iPorts >= 12  ):
				pAragon.setUHV( 1, 1 )
				pAragon.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pAragon.setUHV( 1, 0 )

		# UHV 3: Control Catalonia, Valencia, Aragon, Balears, Corsica, Sardinia, Sicily, Apulia, Provence and Thessaly in 1474
		if ( iGameTurn == i1474AD and pAragon.getUHV( 2 ) == -1 ):
			bConq = True
			for iProv in tAragonControlII:
				if ( pAragon.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pAragon.setUHV( 2, 1 )
				pAragon.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pAragon.setUHV( 2, 0 )


	def checkPrussia( self, iGameTurn ):

		# UHV 1: Control Prussia, Suvalkija, Lithuania, Livonia, Estonia, and Pomerania in 1410
		if ( iGameTurn == i1410AD and pPrussia.getUHV( 0 ) == -1 ):
			bOwn = True
			for iProv in tPrussiaControlI:
				if ( pPrussia.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bOwn = False
					break
			if ( bOwn ):
				pPrussia.setUHV( 0, 1 )
				pPrussia.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pPrussia.setUHV( 0, 0 )

		# UHV 2: Conquer two cities from each of Austria, Muscowy, Germany, Sweden, France and Spain between 1650 and 1763, if they are still alive
		# Controlled in the onCityAcquired function
		if ( iGameTurn > i1763AD and pPrussia.getUHV( 1 ) == -1 ):
			pPrussia.setUHV( 1, 0 )

		# UHV 3: Settle a total of 15 Great People in your capital
		if ( pPrussia.getUHV(2) == - 1 ):
			pCapital = pPrussia.getCapitalCity()
			iGPStart = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_PRIEST")
			iGPEnd = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_SPY")
			iGPeople = 0
			for iType in range(iGPStart, iGPEnd+1):
				iGPeople += pCapital.getFreeSpecialistCount(iType)
			if(iGPeople >= 15):
				pPrussia.setUHV( 2, 1 )
				pPrussia.changeStabilityBase( iCathegoryExpansion, 3 )


	def checkLithuania( self, iGameTurn ):

		# UHV 1: Accumulate 2000 Culture points without declaring state religion before 1386
		iCulture = pLithuania.getUHVCounter( 0 ) + pLithuania.countCultureProduced()
		pLithuania.setUHVCounter( 0, iCulture )
		if ( iGameTurn <= i1386AD and pLithuania.getUHV( 0 ) == -1 ):
			if ( pLithuania.getStateReligion() != -1 ):
				pLithuania.setUHV( 0, 0 )
			elif ( iCulture >= 2000 ):
				pLithuania.setUHV( 0, 1 )
				pLithuania.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i1386AD ):
				pLithuania.setUHV( 0, 0 )

		# UHV 2: Have at least 18 cities in 1569
		if ( iGameTurn == i1569AD and pLithuania.getUHV( 1 ) == -1 ):
			if ( pLithuania.getNumCities() >= 18 ):
				pLithuania.setUHV( 1, 1 )
				pLithuania.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pLithuania.setUHV( 1, 0 )

		# UHV 3: Conquer or Vassalize Moscow
		if ( pLithuania.getUHV( 2 ) == -1 ):
			if ( pMoscow.isAlive() and teamMoscow.isVassal( teamLithuania.getID() ) ):
				pLithuania.setUHV( 2, 1 )
				pLithuania.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( (iGameTurn > i1401AD) and (pLithuania.getProvinceCurrentState( iP_Moscow ) >= iProvinceConquer) ):
				pLithuania.setUHV( 2, 1 )
				pLithuania.changeStabilityBase( iCathegoryExpansion, 3 )


	def checkAustria( self, iGameTurn ):

		# UHV 1: Control all of medieval Austria, Hungary and Bohemia in 1617
		if ( iGameTurn == i1617AD and pAustria.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tAustriaControl:
				if ( pAustria.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pAustria.setUHV( 0, 1 )
				pAustria.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pAustria.setUHV( 0, 0 )

		# UHV 2: Have 3 vassals in 1700
		if ( iGameTurn == i1700AD and pAustria.getUHV( 1 ) == -1 ):
			iCount = 0
			for iPlayer in range( iNumMajorPlayers ):
				pPlayer = gc.getPlayer( iPlayer )
				if ( iPlayer != iAustria and pPlayer.isAlive() ):
					if ( gc.getTeam( pPlayer.getTeam() ).isVassal( iAustria ) ):
						iCount += 1
			if ( iCount >= 3 ):
				 pAustria.setUHV( 1, 1 )
				 pAustria.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				 pAustria.setUHV( 1, 0 )

		# UHV 3: Have the highest score in 1780
		if ( iGameTurn == i1780AD and pAustria.getUHV( 2 ) == -1 ):
			if ( gc.getGame().getTeamRank(iAustria) == 0 ):
				 pAustria.setUHV( 2, 1 )
				 pAustria.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				 pAustria.setUHV( 2, 0 )


	def checkTurkey( self, iGameTurn ):

		# UHV 1: Conquer the Balkans by 1453
		if ( iGameTurn == i1453AD and pTurkey.getUHV( 0 ) == -1 ):
			bConq = True
			for iProv in tOttomanControlI:
				if ( pTurkey.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pTurkey.setUHV( 0, 1 )
				pTurkey.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pTurkey.setUHV( 0, 0 )

		# UHV 2: Conquer Anatolia, the Levant and Egypt by 1517
		if ( iGameTurn == i1517AD and pTurkey.getUHV( 1 ) == -1 ):
			bConq = True
			for iProv in tOttomanControlII:
				if ( pTurkey.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pTurkey.setUHV( 1, 1 )
				pTurkey.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pTurkey.setUHV( 1, 0 )

		# UHV 3: Conquer Austria by 1683
		if ( iGameTurn <= i1683AD and pTurkey.getUHV( 2 ) == -1 ):
			bConq = True
			for iProv in tOttomanControlIII:
				if ( pTurkey.getProvinceCurrentState( iProv ) < iProvinceConquer ):
					bConq = False
					break
			if ( bConq ):
				pTurkey.setUHV( 2, 1 )
				pTurkey.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( iGameTurn == i1683AD ):
				pTurkey.setUHV( 2, 0 )


	def checkMoscow( self, iGameTurn ):

		# UHV 1: Free Eastern Europe from the Mongols
		if ( iGameTurn == i1482AD and pMoscow.getUHV( 0 ) == -1 ):
			bClean = True
			for iProv in tMoscowControl:
				if ( pBarbarian.getProvinceCityCount( iProv ) > 0):
					bClean = False
					break
			if ( bClean ):
				pMoscow.setUHV( 0, 1 )
				pMoscow.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pMoscow.setUHV( 0, 0 )

		# UHV 2: Control at least 20% of Europe
		if ( pMoscow.getUHV( 1 ) == -1 ):
			totalLand = gc.getMap().getLandPlots()
			RussianLand = pMoscow.getTotalLand()
			if (totalLand > 0):
				landPercent = (RussianLand * 100.0) / totalLand
			else:
				landPercent = 0.0
			if ( landPercent >= 20 ):
				pMoscow.setUHV( 1, 1 )
				pMoscow.changeStabilityBase( iCathegoryExpansion, 3 )

		# UHV 3: Get into warm waters
		if ( pMoscow.getUHV( 2 ) == -1 ):
			if ( pMoscow.countOwnedBonuses( iAccess ) > 0 ):
				pMoscow.setUHV( 2, 1 )
				pMoscow.changeStabilityBase( iCathegoryExpansion, 3 )
			elif ( gc.getMap().plot( tCapitals[iByzantium][0], tCapitals[iByzantium][1] ).getPlotCity().getOwner() == iMoscow ):
				pMoscow.setUHV( 2, 1 )
				pMoscow.changeStabilityBase( iCathegoryExpansion, 3 )


	def checkSweden( self, iGameTurn ):

		# Old UHVs: Conquer Gotaland, Svealand, Norrland, Skaneland, Gotland and Osterland in 1600
		#			Don't lose any cities to Poland, Lithuania or Russia before 1700
		#			Have 15 cities in Saxony, Brandenburg, Holstein, Pomerania, Prussia, Greater Poland, Masovia, Suvalkija, Lithuania, Livonia, Estonia, Smolensk, Polotsk, Minsk, Murom, Chernigov, Moscow, Novgorod and Rostov in 1750

		# UHV 1: Have six cities in Norrland, Osterland and Karelia in 1323
		if ( iGameTurn == i1323AD and pSweden.getUHV( 0 ) == -1 ):
			iNumCities = 0
			for iProv in tSwedenControl:
				iNumCities += pSweden.getProvinceCityCount(iProv)
			if ( iNumCities >= 6 ):
				pSweden.setUHV( 0, 1 )
				pSweden.changeStabilityBase( iCathegoryExpansion, 3 )
			else:
				pSweden.setUHV( 0, 0 )

		# UHV 2: Raze 5 Catholic cities while being Protestant by 1660
		# Controlled in the onCityRazed function
		if ( iGameTurn == i1660AD and pSweden.getUHV( 1 ) == -1 ):
			pSweden.setUHV( 1, 0 )

		# UHV 3: Control every coastal city on the Baltic in 1750
		if (iGameTurn == i1750AD):
			if(up.getNumForeignCitiesOnBaltic(iSweden, True) > 0):
				pSweden.setUHV( 2, 0 )
			else:
				pSweden.setUHV( 2, 1 )
				pSweden.changeStabilityBase( iCathegoryExpansion, 3 )


	def checkDutch( self, iGameTurn ):

		# UHV 1: Settle 5 Great Merchants in Amsterdam by 1750
		if ( iGameTurn <= i1750AD and pDutch.getUHV( 0 ) == -1 ):
			pPlot = gc.getMap().plot( tCapitals[iDutch][0], tCapitals[iDutch][1])
			if ( pPlot.isCity() ):
				if ( pPlot.getPlotCity().getFreeSpecialistCount(iGreatMerchant) >= 5 ):
					pDutch.setUHV( 0, 1 )
					pDutch.changeStabilityBase( iCathegoryExpansion, 3 )
		else:
			if ( pDutch.getUHV( 0 ) == -1 ):
				pDutch.setUHV( 0, 0 )

		# UHV 2: Build 3 Colonies and complete both Trading Companies
		# Controlled in the onProjectBuilt function

		# UHV 3: Become the richest country in Europe
		if ( pDutch.getUHV( 2 ) == -1 ):
			iGold = pDutch.getGold()
			bMost = True
			for iCiv in range( iNumPlayers ):
				if ( iCiv != iDutch and gc.getPlayer( iCiv ).isAlive() ):
					if (gc.getPlayer(iCiv).getGold() > iGold):
						bMost = False
			if ( bMost ):
				 pDutch.setUHV( 2, 1 )
				 pDutch.changeStabilityBase( iCathegoryExpansion, 3 )

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

	def set1200UHVDone( self, iCiv ):
		if iCiv == iByzantium:
			pByzantium.setUHV( 0, 1 )
		elif iCiv == iFrankia:
			pFrankia.setUHV( 0, 1 )
		elif iCiv == iArabia:
			pArabia.setUHV( 0, 1 )
		elif iCiv == iBulgaria:
			pBulgaria.setUHV( 0, 1 )
		elif iCiv == iVenecia: #Venice gets conquerors near Constantinople for 2nd UHV
			pVenecia.setUHV( 0, 1 )
		elif iCiv == iGermany:
			pGermany.setUHV( 0, 1 )
		elif iCiv == iNorway:
			pNorway.setUHV( 0, 1 )
		elif iCiv == iDenmark:
			pDenmark.setUHV( 0, 1 )
		elif iCiv == iScotland:
			pScotland.setUHVCounter(1, 100)
