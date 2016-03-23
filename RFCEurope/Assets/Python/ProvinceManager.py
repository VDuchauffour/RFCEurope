# RFC Europe, balancing modifiers are placed here
from CvPythonExtensions import *
from Consts import *
from XMLConsts import *
import RFCEMaps as rfcemaps
import RFCUtils # Absinthe

gc = CyGlobalContext()
utils = RFCUtils.RFCUtils() # Absinthe


############ Lists of all the provinces for each Civ ###################
tByzantiumCore = [iP_Constantinople,iP_Thrace,iP_Thessaly,iP_Thessaloniki,iP_Epirus,iP_Morea,iP_Opsikion,iP_Paphlagonia,iP_Thrakesion,iP_Cilicia,iP_Anatolikon,iP_Armeniakon,iP_Charsianon,iP_Colonea,iP_Antiochia]
tByzantiumNorm = [iP_Moesia,iP_Serbia,iP_Macedonia,iP_Arberia,iP_Cyprus,iP_Crete,iP_Rhodes,iP_Syria,iP_Lebanon,iP_Jerusalem,iP_Egypt,iP_Cyrenaica]
tByzantiumOuter = [iP_Crimea,iP_Arabia,iP_Bosnia,iP_Slavonia,iP_Dalmatia,iP_Verona,iP_Lombardy,iP_Liguria,iP_Tuscany,iP_Latium,iP_Sardinia,iP_Corsica]
tByzantiumPot2Core = []
tByzantiumPot2Norm = [iP_Calabria,iP_Apulia,iP_Sicily,iP_Malta,iP_Tripolitania,iP_Ifriqiya]

tFranceCore = [iP_IleDeFrance,iP_Orleans,iP_Champagne]
tFranceNorm = [iP_Picardy,iP_Normandy,iP_Aquitania]
tFranceOuter = [iP_Catalonia,iP_Aragon,iP_Navarre,iP_Lorraine,iP_Netherlands,iP_Bavaria,iP_Saxony,iP_Swabia,iP_Franconia,iP_Lombardy,iP_Liguria,iP_Corsica]
tFrancePot2Core = []
tFrancePot2Norm = [iP_Bretagne,iP_Provence,iP_Burgundy,iP_Flanders]

tArabiaCore = [iP_Syria,iP_Lebanon,iP_Jerusalem,iP_Arabia]
tArabiaNorm = [iP_Egypt,iP_Cyrenaica]
tArabiaOuter = [iP_Oran,iP_Algiers,iP_Sicily,iP_Malta,iP_Crete,iP_Rhodes,iP_Cilicia]
tArabiaPot2Core = []
tArabiaPot2Norm = [iP_Antiochia,iP_Cyprus,iP_Ifriqiya,iP_Tripolitania]

tBulgariaCore = [iP_Moesia]
tBulgariaNorm = [iP_Macedonia,iP_Wallachia]
tBulgariaOuter = [iP_Serbia,iP_Banat,iP_Epirus,iP_Arberia,iP_Constantinople]
tBulgariaPot2Core = []
tBulgariaPot2Norm = [iP_Thrace,iP_Thessaloniki]

tCordobaCore = [iP_Andalusia,iP_Valencia,iP_LaMancha]
tCordobaNorm = [iP_Tetouan]
tCordobaOuter = [iP_Leon,iP_Lusitania,iP_Navarre,iP_Castile,iP_Oran]
tCordobaPot2Core = []
tCordobaPot2Norm = [iP_Morocco,iP_Fez,iP_Marrakesh,iP_Catalonia,iP_Aragon,iP_Balears]

tVeniceCore = [iP_Verona]
tVeniceNorm = [iP_Dalmatia]
tVeniceOuter = [iP_Epirus,iP_Morea,iP_Rhodes,iP_Constantinople]
tVenicePot2Core = []
tVenicePot2Norm = [iP_Tuscany,iP_Arberia,iP_Crete,iP_Cyprus]

tBurgundyCore = [iP_Burgundy]
tBurgundyNorm = [iP_Provence,iP_Flanders]
tBurgundyOuter = [iP_Lorraine,iP_Swabia,iP_Lombardy,iP_Liguria,iP_Bretagne]
tBurgundyPot2Core = []
tBurgundyPot2Norm = [iP_Champagne,iP_Picardy,iP_IleDeFrance,iP_Aquitania,iP_Orleans,iP_Normandy]

tGermanyCore = [iP_Franconia,iP_Lorraine,iP_Bavaria,iP_Swabia,iP_Saxony]
tGermanyNorm = [iP_Brandenburg]
tGermanyOuter = [iP_Champagne,iP_Picardy,iP_Burgundy,iP_Liguria,iP_Verona,iP_Tuscany,iP_Austria,iP_Moravia,iP_Silesia,iP_GreaterPoland,iP_Carinthia]
tGermanyPot2Core = []
tGermanyPot2Norm = [iP_Bohemia,iP_Holstein,iP_Pomerania,iP_Netherlands,iP_Flanders,iP_Lombardy]

tNovgorodCore = [iP_Novgorod, iP_Karelia]
tNovgorodNorm = [iP_Rostov, iP_Vologda]
tNovgorodOuter = [iP_Smolensk, iP_Polotsk, iP_Livonia]
tNovgorodPot2Core = []
tNovgorodPot2Norm = [iP_Estonia, iP_Osterland]

tNorwayCore = [iP_Norway,iP_Vestfold]
tNorwayNorm = [iP_Iceland]
tNorwayOuter = [iP_Scotland,iP_Northumbria,iP_Ireland,iP_Normandy,iP_Svealand,iP_Norrland]
tNorwayPot2Core = []
tNorwayPot2Norm = [iP_TheIsles,iP_Jamtland]

tKievCore = [iP_Kiev,iP_Sloboda,iP_Pereyaslavl,iP_Chernigov]
tKievNorm = [iP_Podolia,iP_Volhynia]
tKievOuter = [iP_Moldova,iP_GaliciaPoland,iP_Brest,iP_Polotsk,iP_Novgorod,iP_Moscow,iP_Murom,iP_Simbirsk,iP_Crimea,iP_Donets,iP_Kuban]
tKievPot2Core = []
tKievPot2Norm = [iP_Minsk,iP_Smolensk,iP_Zaporizhia]

tHungaryCore = [iP_Hungary,iP_UpperHungary,iP_Pannonia,iP_Transylvania]
tHungaryNorm = [iP_Slavonia,iP_Banat,iP_Bosnia,iP_Dalmatia]
tHungaryOuter = [iP_Serbia,iP_Wallachia,iP_Moldova,iP_GaliciaPoland,iP_Bavaria,iP_Bohemia,iP_Silesia]
tHungaryPot2Core = []
tHungaryPot2Norm = [iP_Moravia,iP_Austria,iP_Carinthia]

tSpainCore = [iP_Leon,iP_GaliciaSpain,iP_Castile]
tSpainNorm = []
tSpainOuter = [iP_Lusitania,iP_Catalonia,iP_Aragon,iP_Balears,iP_Aquitania,iP_Provence,iP_Tetouan,iP_Fez,iP_Oran,iP_Algiers,iP_Sardinia,iP_Corsica,iP_Azores,iP_Sicily,iP_Calabria,iP_Apulia]
tSpainPot2Core = []
tSpainPot2Norm = [iP_Navarre,iP_Andalusia,iP_Valencia,iP_LaMancha,iP_Canaries,iP_Madeira]

tDenmarkCore = [iP_Denmark,iP_Skaneland]
tDenmarkNorm = []
tDenmarkOuter = [iP_Gotaland,iP_Svealand,iP_Northumbria,iP_Mercia,iP_EastAnglia,iP_London,iP_Brandenburg,iP_Norway,iP_Vestfold,iP_Normandy]
tDenmarkPot2Core = []
tDenmarkPot2Norm = [iP_Estonia,iP_Gotland,iP_Holstein]

tScotlandCore = [iP_Scotland]
tScotlandNorm = [iP_TheIsles]
tScotlandOuter = [iP_Ireland, iP_Mercia, iP_Wales]
tScotlandPot2Core = []
tScotlandPot2Norm = [iP_Northumbria]

tPolandCore = [iP_GreaterPoland,iP_LesserPoland,iP_Masovia]
tPolandNorm = [iP_Brest,iP_GaliciaPoland]
tPolandOuter = [iP_Prussia,iP_Lithuania,iP_Polotsk,iP_Minsk,iP_Volhynia,iP_Podolia,iP_Moldova,iP_Kiev]
tPolandPot2Core = []
tPolandPot2Norm = [iP_Pomerania,iP_Silesia,iP_Suvalkija]

tGenoaCore = [iP_Liguria]
tGenoaNorm = [iP_Corsica,iP_Sardinia]
tGenoaOuter = [iP_Ifriqiya,iP_Constantinople,iP_Crete,iP_Cyprus,iP_Morea]
tGenoaPot2Core = []
tGenoaPot2Norm = [iP_Sicily,iP_Malta,iP_Lombardy,iP_Tuscany,iP_Rhodes,iP_Crimea]

tMoroccoCore = [iP_Marrakesh, iP_Morocco, iP_Fez]
tMoroccoNorm = [iP_Tetouan]
tMoroccoOuter = [iP_Ifriqiya, iP_Andalusia, iP_Valencia, iP_Tripolitania]
tMoroccoPot2Core = []
tMoroccoPot2Norm = [iP_Oran, iP_Algiers]

tEnglandCore = [iP_London,iP_EastAnglia,iP_Mercia,iP_Wessex]
tEnglandNorm = [iP_Northumbria]
tEnglandOuter = [iP_IleDeFrance,iP_Bretagne,iP_Aquitania,iP_Orleans,iP_Champagne,iP_Flanders,iP_Normandy,iP_Picardy,iP_Scotland,iP_TheIsles,iP_Ireland]
tEnglandPot2Core = []
tEnglandPot2Norm = [iP_Wales]

tPortugalCore = [iP_Lusitania]
tPortugalNorm = [iP_Azores]
tPortugalOuter = [iP_Morocco,iP_Tetouan,iP_Leon,iP_GaliciaSpain]
tPortugalPot2Core = []
tPortugalPot2Norm = [iP_Madeira,iP_Canaries,iP_Andalusia]

tAragonCore = [iP_Aragon,iP_Catalonia,iP_Balears,iP_Valencia]
tAragonNorm = []
tAragonOuter = [iP_Castile,iP_Provence,iP_Corsica,iP_Thessaly]
tAragonPot2Core = []
tAragonPot2Norm = [iP_Navarre,iP_Andalusia,iP_LaMancha,iP_Sardinia,iP_Sicily,iP_Apulia,iP_Calabria,iP_Malta]

tSwedenCore = [iP_Norrland,iP_Svealand]
tSwedenNorm = [iP_Gotaland,iP_Gotland]
tSwedenOuter = [iP_Skaneland,iP_Vestfold,iP_Pomerania,iP_Livonia,iP_Prussia,iP_Novgorod]
tSwedenPot2Core = []
tSwedenPot2Norm = [iP_Jamtland,iP_Osterland,iP_Karelia,iP_Estonia]

tPrussiaCore = [iP_Prussia]
tPrussiaNorm = []
tPrussiaOuter = [iP_Brandenburg,iP_Estonia,iP_Gotland]
tPrussiaPot2Core = []
tPrussiaPot2Norm = [iP_Pomerania,iP_Livonia]

tLithuaniaCore = [iP_Lithuania]
tLithuaniaNorm = [iP_Suvalkija,iP_Minsk,iP_Polotsk]
tLithuaniaOuter = [iP_GreaterPoland,iP_LesserPoland,iP_Masovia,iP_GaliciaPoland,iP_Sloboda,iP_Pereyaslavl,iP_Livonia,iP_Estonia,iP_Novgorod,iP_Smolensk,iP_Chernigov]
tLithuaniaPot2Core = []
tLithuaniaPot2Norm = [iP_Brest,iP_Podolia,iP_Volhynia,iP_Kiev]

tAustriaCore = [iP_Austria,iP_Carinthia]
tAustriaNorm = [iP_Bohemia,iP_Moravia]
tAustriaOuter = [iP_Verona,iP_Hungary,iP_Transylvania,iP_Slavonia,iP_Dalmatia,iP_LesserPoland,iP_GaliciaPoland,iP_Netherlands,iP_Flanders]
tAustriaPot2Core = []
tAustriaPot2Norm = [iP_Bavaria,iP_Silesia,iP_Pannonia,iP_UpperHungary]

tTurkeyCore = [iP_Opsikion,iP_Thrakesion,iP_Paphlagonia,iP_Anatolikon,iP_Constantinople]
tTurkeyNorm = [iP_Thrace,iP_Armeniakon,iP_Charsianon,iP_Cilicia]
tTurkeyOuter = [iP_Thessaly,iP_Epirus,iP_Morea,iP_Arberia,iP_Wallachia,iP_Serbia,iP_Bosnia,iP_Banat,iP_Slavonia,iP_Pannonia,iP_Hungary,iP_Transylvania,iP_Moldova,iP_Crimea,iP_Crete,iP_Cyrenaica,iP_Tripolitania]
tTurkeyPot2Core = []
tTurkeyPot2Norm = [iP_Colonea,iP_Antiochia,iP_Syria,iP_Lebanon,iP_Jerusalem,iP_Egypt,iP_Arabia,iP_Macedonia,iP_Thessaloniki,iP_Moesia,iP_Cyprus,iP_Rhodes]

tMoscowCore = [iP_Moscow,iP_Murom,iP_Rostov,iP_Smolensk]
tMoscowNorm = [iP_NizhnyNovgorod,iP_Simbirsk,iP_Pereyaslavl,iP_Chernigov]
tMoscowOuter = [iP_Crimea,iP_Moldova,iP_GaliciaPoland,iP_Kuban,iP_Brest,iP_Lithuania,iP_Livonia,iP_Estonia,iP_Karelia,iP_Osterland,iP_Prussia,iP_Suvalkija]
tMoscowPot2Core = []
tMoscowPot2Norm = [iP_Novgorod,iP_Vologda,iP_Kiev,iP_Minsk,iP_Polotsk,iP_Volhynia,iP_Podolia,iP_Donets,iP_Sloboda,iP_Zaporizhia]

tDutchCore = [iP_Netherlands]
tDutchNorm = [iP_Flanders]
tDutchOuter = []
tDutchPot2Core = []
tDutchPot2Norm = []


class ProvinceManager:

	def __init__( self ):
		self.tCoreProvinces = {
			iByzantium : tByzantiumCore,
			iFrankia : tFranceCore,
			iArabia : tArabiaCore,
			iBulgaria : tBulgariaCore,
			iCordoba : tCordobaCore,
			iVenecia : tVeniceCore,
			iBurgundy : tBurgundyCore,
			iGermany : tGermanyCore,
			iNovgorod : tNovgorodCore,
			iNorway : tNorwayCore,
			iKiev : tKievCore,
			iHungary : tHungaryCore,
			iSpain : tSpainCore,
			iDenmark : tDenmarkCore,
			iScotland : tScotlandCore,
			iPoland : tPolandCore,
			iGenoa : tGenoaCore,
			iMorocco : tMoroccoCore,
			iEngland : tEnglandCore,
			iPortugal : tPortugalCore,
			iAragon : tAragonCore,
			iSweden : tSwedenCore,
			iPrussia : tPrussiaCore,
			iLithuania : tLithuaniaCore,
			iAustria : tAustriaCore,
			iTurkey : tTurkeyCore,
			iMoscow : tMoscowCore,
			iDutch : tDutchCore,
			}

		self.tNormProvinces = {
			iByzantium : tByzantiumNorm,
			iFrankia : tFranceNorm,
			iArabia : tArabiaNorm,
			iBulgaria : tBulgariaNorm,
			iCordoba : tCordobaNorm,
			iVenecia : tVeniceNorm,
			iBurgundy : tBurgundyNorm,
			iGermany : tGermanyNorm,
			iNovgorod : tNovgorodNorm,
			iNorway : tNorwayNorm,
			iKiev : tKievNorm,
			iHungary : tHungaryNorm,
			iSpain : tSpainNorm,
			iDenmark : tDenmarkNorm,
			iScotland : tScotlandNorm,
			iPoland : tPolandNorm,
			iGenoa : tGenoaNorm,
			iMorocco : tMoroccoNorm,
			iEngland : tEnglandNorm,
			iPortugal : tPortugalNorm,
			iAragon : tAragonNorm,
			iSweden : tSwedenNorm,
			iPrussia : tPrussiaNorm,
			iLithuania : tLithuaniaNorm,
			iAustria : tAustriaNorm,
			iTurkey : tTurkeyNorm,
			iMoscow : tMoscowNorm,
			iDutch : tDutchNorm,
			}

		self.tOuterProvinces = {
			iByzantium : tByzantiumOuter,
			iFrankia : tFranceOuter,
			iArabia : tArabiaOuter,
			iBulgaria : tBulgariaOuter,
			iCordoba : tCordobaOuter,
			iVenecia : tVeniceOuter,
			iBurgundy : tBurgundyOuter,
			iGermany : tGermanyOuter,
			iNovgorod : tNovgorodOuter,
			iNorway : tNorwayOuter,
			iKiev : tKievOuter,
			iHungary : tHungaryOuter,
			iSpain : tSpainOuter,
			iDenmark : tDenmarkOuter,
			iScotland : tScotlandOuter,
			iPoland : tPolandOuter,
			iGenoa : tGenoaOuter,
			iMorocco : tMoroccoOuter,
			iEngland : tEnglandOuter,
			iPortugal : tPortugalOuter,
			iAragon : tAragonOuter,
			iSweden : tSwedenOuter,
			iPrussia : tPrussiaOuter,
			iLithuania : tLithuaniaOuter,
			iAustria : tAustriaOuter,
			iTurkey : tTurkeyOuter,
			iMoscow : tMoscowOuter,
			iDutch : tDutchOuter,
			}

		self.tPot2CoreProvinces = {
			iByzantium : tByzantiumPot2Core,
			iFrankia : tFrancePot2Core,
			iArabia : tArabiaPot2Core,
			iBulgaria : tBulgariaPot2Core,
			iCordoba : tCordobaPot2Core,
			iVenecia : tVenicePot2Core,
			iBurgundy : tBurgundyPot2Core,
			iGermany : tGermanyPot2Core,
			iNovgorod : tNovgorodPot2Core,
			iNorway : tNorwayPot2Core,
			iKiev : tKievPot2Core,
			iHungary : tHungaryPot2Core,
			iSpain : tSpainPot2Core,
			iDenmark : tDenmarkPot2Core,
			iScotland : tScotlandPot2Core,
			iPoland : tPolandPot2Core,
			iGenoa : tGenoaPot2Core,
			iMorocco : tMoroccoPot2Core,
			iEngland : tEnglandPot2Core,
			iPortugal : tPortugalPot2Core,
			iAragon : tAragonPot2Core,
			iSweden : tSwedenPot2Core,
			iPrussia : tPrussiaPot2Core,
			iLithuania : tLithuaniaPot2Core,
			iAustria : tAustriaPot2Core,
			iTurkey : tTurkeyPot2Core,
			iMoscow : tMoscowPot2Core,
			iDutch : tDutchPot2Core,
			}

		self.tPot2NormProvinces = {
			iByzantium : tByzantiumPot2Norm,
			iFrankia : tFrancePot2Norm,
			iArabia : tArabiaPot2Norm,
			iBulgaria : tBulgariaPot2Norm,
			iCordoba : tCordobaPot2Norm,
			iVenecia : tVenicePot2Norm,
			iBurgundy : tBurgundyPot2Norm,
			iGermany : tGermanyPot2Norm,
			iNovgorod : tNovgorodPot2Norm,
			iNorway : tNorwayPot2Norm,
			iKiev : tKievPot2Norm,
			iHungary : tHungaryPot2Norm,
			iSpain : tSpainPot2Norm,
			iDenmark : tDenmarkPot2Norm,
			iScotland : tScotlandPot2Norm,
			iPoland : tPolandPot2Norm,
			iGenoa : tGenoaPot2Norm,
			iMorocco : tMoroccoPot2Norm,
			iEngland : tEnglandPot2Norm,
			iPortugal : tPortugalPot2Norm,
			iAragon : tAragonPot2Norm,
			iSweden : tSwedenPot2Norm,
			iPrussia : tPrussiaPot2Norm,
			iLithuania : tLithuaniaPot2Norm,
			iAustria : tAustriaPot2Norm,
			iTurkey : tTurkeyPot2Norm,
			iMoscow : tMoscowPot2Norm,
			iDutch : tDutchPot2Norm,
			}

	def setup( self ):
		# set the initial situation for all players
		for iPlayer in range( iNumPlayers -1 ): # this discounts the Pope
			pPlayer = gc.getPlayer(iPlayer)
			for iProv in self.tCoreProvinces[iPlayer]:
				pPlayer.setProvinceType( iProv, iProvinceCore )
			for iProv in self.tNormProvinces[iPlayer]:
				pPlayer.setProvinceType( iProv, iProvinceNatural)
			for iProv in self.tOuterProvinces[iPlayer]:
				pPlayer.setProvinceType( iProv, iProvinceOuter )
			for iProv in self.tPot2CoreProvinces[iPlayer]:
				pPlayer.setProvinceType( iProv, iProvincePotential )
			for iProv in self.tPot2NormProvinces[iPlayer]:
				pPlayer.setProvinceType( iProv, iProvincePotential )
		#Update provinces for 1200 Scenario
		if utils.getScenario() == i1200ADScenario:
			for iPlayer in range(iNumPlayers -1):
				if tBirth[iPlayer] < i1200AD:
					self.onSpawn(iPlayer)

	def checkTurn(self, iGameTurn):
		# Prussia direction change
		if (iGameTurn == i1618AD):
			pPrussia.setProvinceType( iP_Estonia, iProvinceNone )
			pPrussia.setProvinceType( iP_Livonia, iProvinceOuter )
			pPrussia.setProvinceType( iP_Brandenburg, iProvinceNatural )
			pPrussia.setProvinceType( iP_Silesia, iProvincePotential )
			pPrussia.setProvinceType( iP_GreaterPoland, iProvinceOuter )
			print("Yes! Prussia can into Germany!")

	def onCityBuilt(self, iPlayer, x, y):
		if ( iPlayer >= iNumPlayers -1 ):
			return
		pPlayer = gc.getPlayer(iPlayer)
		iProv = rfcemaps.tProinceMap[y][x]
		if ( pPlayer.getProvinceType( iProv ) == iProvincePotential ):
			if ( iProv in self.tPot2NormProvinces[iPlayer] ):
				pPlayer.setProvinceType( iProv, iProvinceNatural )
				utils.refreshStabilityOverlay() # refresh the stability overlay
			if ( iProv in self.tPot2CoreProvinces[iPlayer] ):
				pPlayer.setProvinceType( iProv, iProvinceCore )
				utils.refreshStabilityOverlay() # refresh the stability overlay

	def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
		if ( playerType >= iNumPlayers -1 ):
			return
		pPlayer = gc.getPlayer(playerType)
		iProv = city.getProvince()
		if ( pPlayer.getProvinceType( iProv ) == iProvincePotential ):
			if ( iProv in self.tPot2NormProvinces[playerType] ):
				pPlayer.setProvinceType( iProv, iProvinceNatural )
				utils.refreshStabilityOverlay() # refresh the stability overlay
			if ( iProv in self.tPot2CoreProvinces[playerType] ):
				pPlayer.setProvinceType( iProv, iProvinceCore )
				utils.refreshStabilityOverlay() # refresh the stability overlay

	def onCityRazed(self, iOwner, playerType, city):
		pass

	def onRespawn(self, iPlayer ):
		# reset the provinces
		pPlayer = gc.getPlayer(iPlayer)
		for iProv in self.tCoreProvinces[iPlayer]:
			pPlayer.setProvinceType( iProv, iProvinceCore )
		for iProv in self.tNormProvinces[iPlayer]:
			pPlayer.setProvinceType( iProv, iProvinceNatural)
		for iProv in self.tOuterProvinces[iPlayer]:
			pPlayer.setProvinceType( iProv, iProvinceOuter )
		for iProv in self.tPot2CoreProvinces[iPlayer]:
			pPlayer.setProvinceType( iProv, iProvincePotential )
		for iProv in self.tPot2NormProvinces[iPlayer]:
			pPlayer.setProvinceType( iProv, iProvincePotential )

		#### -------- Special Respawn Conditions ---------- ####
		if ( iPlayer == iArabia ):
			for iProv in range( iP_MaxNumberOfProvinces ):
				pArabia.setProvinceType( iProv, iProvinceNone )
			for iProv in self.tCoreProvinces[iPlayer]:
				pArabia.setProvinceType( iProv, iProvinceCore )
			for iProv in self.tNormProvinces[iPlayer]:
				pArabia.setProvinceType( iProv, iProvinceNatural)
			for iProv in self.tOuterProvinces[iPlayer]:
				pArabia.setProvinceType( iProv, iProvinceOuter )
			for iProv in self.tPot2CoreProvinces[iPlayer]:
				pArabia.setProvinceType( iProv, iProvincePotential )
			for iProv in self.tPot2NormProvinces[iPlayer]:
				pArabia.setProvinceType( iProv, iProvincePotential )
		elif ( iPlayer == iCordoba ):
			for iProv in range( iP_MaxNumberOfProvinces ):
				pCordoba.setProvinceType( iProv, iProvinceNone )
			pCordoba.setProvinceType( iP_Ifriqiya, iProvinceCore )
			pCordoba.setProvinceType( iP_Algiers, iProvinceNatural )
			pCordoba.setProvinceType( iP_Oran, iProvinceOuter )
			pCordoba.setProvinceType( iP_Tripolitania, iProvinceOuter )
			pCordoba.setProvinceType( iP_Tetouan, iProvinceOuter )
			pCordoba.setProvinceType( iP_Morocco, iProvinceOuter )
			pCordoba.setProvinceType( iP_Fez, iProvinceOuter )

	def onSpawn( self, iPlayer ):
		# when a new nations spawns, old nations in the region should lose some of their provinces
		if ( iPlayer == iArabia ):
			pByzantium.setProvinceType( iP_Cyrenaica, iProvinceOuter )
			pByzantium.setProvinceType( iP_Tripolitania, iProvinceOuter )
			pByzantium.setProvinceType( iP_Ifriqiya, iProvinceOuter )
			pByzantium.setProvinceType( iP_Egypt, iProvinceOuter )
			pByzantium.setProvinceType( iP_Arabia, iProvinceNone )
			pByzantium.setProvinceType( iP_Syria, iProvinceOuter )
			pByzantium.setProvinceType( iP_Lebanon, iProvinceOuter )
			pByzantium.setProvinceType( iP_Jerusalem, iProvinceOuter )
			pByzantium.setProvinceType( iP_Antiochia, iProvinceNatural )
			pByzantium.setProvinceType( iP_Cilicia, iProvinceNatural )
			pByzantium.setProvinceType( iP_Charsianon, iProvinceNatural )
			pByzantium.setProvinceType( iP_Colonea, iProvinceNatural )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iBulgaria ):
			pByzantium.setProvinceType( iP_Serbia, iProvinceOuter )
			pByzantium.setProvinceType( iP_Moesia, iProvinceOuter )
			pByzantium.setProvinceType( iP_Thrace, iProvinceNatural )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iVenecia ):
			pByzantium.setProvinceType( iP_Dalmatia, iProvinceNone )
			pByzantium.setProvinceType( iP_Bosnia, iProvinceNone )
			pByzantium.setProvinceType( iP_Slavonia, iProvinceNone )
			pByzantium.setProvinceType( iP_Verona, iProvinceNone )
			pByzantium.setProvinceType( iP_Tuscany, iProvinceNone )
			pByzantium.setProvinceType( iP_Lombardy, iProvinceNone )
			pByzantium.setProvinceType( iP_Liguria, iProvinceNone )
			pByzantium.setProvinceType( iP_Corsica, iProvinceNone )
			pByzantium.setProvinceType( iP_Sardinia, iProvinceNone )
			pByzantium.setProvinceType( iP_Latium, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iBurgundy ):
			pFrankia.setProvinceType( iP_Provence, iProvincePotential ) # these areas flip to Burgundy, so resetting them to Potential will work perfectly
			pFrankia.setProvinceType( iP_Burgundy, iProvincePotential ) # these areas flip to Burgundy, so resetting them to Potential will work perfectly
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iGermany ):
			pFrankia.setProvinceType( iP_Bavaria, iProvinceNone )
			pFrankia.setProvinceType( iP_Franconia, iProvinceNone )
			pFrankia.setProvinceType( iP_Saxony, iProvinceNone )
			pFrankia.setProvinceType( iP_Netherlands, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iHungary ):
			pBulgaria.setProvinceType( iP_Banat, iProvinceNone )
			pBulgaria.setProvinceType( iP_Wallachia, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iSpain ):
			pCordoba.setProvinceType( iP_LaMancha, iProvinceNatural )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iMorocco ):
			pCordoba.setProvinceType( iP_Morocco, iProvinceNone )
			pCordoba.setProvinceType( iP_Marrakesh, iProvinceNone )
			pCordoba.setProvinceType( iP_Fez, iProvinceOuter )
			pCordoba.setProvinceType( iP_Tetouan, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iEngland ):
			pFrankia.setProvinceType( iP_Normandy, iProvincePotential )
			pFrankia.setProvinceType( iP_Picardy, iProvincePotential )
			pScotland.setProvinceType( iP_Northumbria, iProvinceOuter )
			pScotland.setProvinceType( iP_Mercia, iProvinceNone )
			pNorway.setProvinceType( iP_Normandy, iProvinceNone )
			pNorway.setProvinceType( iP_Northumbria, iProvinceNone )
			pDenmark.setProvinceType( iP_Normandy, iProvinceNone )
			pDenmark.setProvinceType( iP_Northumbria, iProvinceNone )
			pDenmark.setProvinceType( iP_Mercia, iProvinceNone )
			pDenmark.setProvinceType( iP_EastAnglia, iProvinceNone )
			pDenmark.setProvinceType( iP_London, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iAragon ):
			pByzantium.setProvinceType( iP_Apulia, iProvinceOuter )
			pByzantium.setProvinceType( iP_Calabria, iProvinceOuter )
			pByzantium.setProvinceType( iP_Sicily, iProvinceOuter )
			pByzantium.setProvinceType( iP_Malta, iProvinceOuter )
			pCordoba.setProvinceType( iP_Aragon, iProvinceOuter )
			pCordoba.setProvinceType( iP_Catalonia, iProvinceOuter )
			pCordoba.setProvinceType( iP_Valencia, iProvinceNatural )
			pCordoba.setProvinceType( iP_Balears, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iSweden ):
			pNorway.setProvinceType( iP_Svealand, iProvinceNone )
			pDenmark.setProvinceType(iP_Gotaland, iProvinceNone )
			pDenmark.setProvinceType(iP_Svealand, iProvinceNone )
			pNovgorod.setProvinceType( iP_Osterland, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iAustria ):
			pHungary.setProvinceType( iP_Carinthia, iProvinceOuter )
			pHungary.setProvinceType( iP_Austria, iProvinceOuter )
			pHungary.setProvinceType( iP_Moravia, iProvinceOuter )
			pHungary.setProvinceType( iP_Bavaria, iProvinceNone )
			pGermany.setProvinceType( iP_Bavaria, iProvinceOuter )
			pGermany.setProvinceType( iP_Bohemia, iProvinceOuter )
			pSpain.setProvinceType( iP_Netherlands, iProvinceOuter )
			pSpain.setProvinceType( iP_Flanders, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iTurkey ):
			pByzantium.setProvinceType( iP_Antiochia, iProvinceOuter )
			pByzantium.setProvinceType( iP_Cilicia, iProvinceOuter )
			pByzantium.setProvinceType( iP_Charsianon, iProvinceOuter )
			pByzantium.setProvinceType( iP_Colonea, iProvinceOuter )
			pByzantium.setProvinceType( iP_Armeniakon, iProvinceOuter )
			pByzantium.setProvinceType( iP_Cyprus, iProvinceOuter )
			pByzantium.setProvinceType( iP_Anatolikon, iProvinceNatural )
			pByzantium.setProvinceType( iP_Opsikion, iProvinceNatural )
			pByzantium.setProvinceType( iP_Thrakesion, iProvinceNatural )
			pByzantium.setProvinceType( iP_Paphlagonia, iProvinceNatural )
			pHungary.setProvinceType( iP_Dalmatia, iProvinceOuter )
			pHungary.setProvinceType( iP_Bosnia, iProvinceOuter )
			pHungary.setProvinceType( iP_Banat, iProvinceOuter )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iMoscow ):
			pNovgorod.setProvinceType( iP_Rostov, iProvinceOuter )
			pNovgorod.setProvinceType( iP_Smolensk, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay
		elif ( iPlayer == iDutch ):
			pSpain.setProvinceType( iP_Netherlands, iProvinceNone )
			pSpain.setProvinceType( iP_Flanders, iProvinceNone )
			pAustria.setProvinceType( iP_Netherlands, iProvinceNone )
			pAustria.setProvinceType( iP_Flanders, iProvinceNone )
			utils.refreshStabilityOverlay() # refresh the stability overlay