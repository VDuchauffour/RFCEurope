from CvPythonExtensions import *
from CoreTypes import City, Civ, ProvinceStatus
from LocationsData import CITIES, CIV_CAPITAL_LOCATIONS
import PyHelpers
import Popup
import Consts
import XMLConsts as xml
import RFCUtils
import UniquePowers
import RFCEMaps
from StoredData import sd
import random

from MiscData import MessageData

# Globals
utils = RFCUtils.RFCUtils()
up = UniquePowers.UniquePowers()
gc = CyGlobalContext()
localText = CyTranslator()  # Absinthe
PyPlayer = PyHelpers.PyPlayer


pBurgundy = gc.getPlayer(Consts.iBurgundy)
pByzantium = gc.getPlayer(Consts.iByzantium)
pFrankia = gc.getPlayer(Consts.iFrankia)
pArabia = gc.getPlayer(Consts.iArabia)
pBulgaria = gc.getPlayer(Consts.iBulgaria)
pCordoba = gc.getPlayer(Consts.iCordoba)
pSpain = gc.getPlayer(Consts.iSpain)
pNorway = gc.getPlayer(Consts.iNorway)
pDenmark = gc.getPlayer(Consts.iDenmark)
pVenecia = gc.getPlayer(Consts.iVenecia)
pNovgorod = gc.getPlayer(Consts.iNovgorod)
pKiev = gc.getPlayer(Consts.iKiev)
pHungary = gc.getPlayer(Consts.iHungary)
pGermany = gc.getPlayer(Consts.iGermany)
pScotland = gc.getPlayer(Consts.iScotland)
pPoland = gc.getPlayer(Consts.iPoland)
pPrussia = gc.getPlayer(Consts.iPrussia)
pLithuania = gc.getPlayer(Consts.iLithuania)
pMoscow = gc.getPlayer(Consts.iMoscow)
pGenoa = gc.getPlayer(Consts.iGenoa)
pMorocco = gc.getPlayer(Consts.iMorocco)
pEngland = gc.getPlayer(Consts.iEngland)
pPortugal = gc.getPlayer(Consts.iPortugal)
pAragon = gc.getPlayer(Consts.iAragon)
pAustria = gc.getPlayer(Consts.iAustria)
pTurkey = gc.getPlayer(Consts.iTurkey)
pSweden = gc.getPlayer(Consts.iSweden)
pDutch = gc.getPlayer(Consts.iDutch)
pPope = gc.getPlayer(Consts.iPope)
pIndependent = gc.getPlayer(Consts.iIndependent)
pIndependent2 = gc.getPlayer(Consts.iIndependent2)
pBarbarian = gc.getPlayer(Consts.iBarbarian)

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
tByzantiumControl = [
    xml.iP_Calabria,
    xml.iP_Apulia,
    xml.iP_Dalmatia,
    xml.iP_Verona,
    xml.iP_Lombardy,
    xml.iP_Liguria,
    xml.iP_Tuscany,
    xml.iP_Latium,
    xml.iP_Corsica,
    xml.iP_Sardinia,
    xml.iP_Sicily,
    xml.iP_Tripolitania,
    xml.iP_Ifriqiya,
]
tByzantiumControlII = [
    xml.iP_Colonea,
    xml.iP_Antiochia,
    xml.iP_Charsianon,
    xml.iP_Cilicia,
    xml.iP_Armeniakon,
    xml.iP_Anatolikon,
    xml.iP_Paphlagonia,
    xml.iP_Thrakesion,
    xml.iP_Opsikion,
    xml.iP_Constantinople,
    xml.iP_Thrace,
    xml.iP_Thessaloniki,
    xml.iP_Moesia,
    xml.iP_Macedonia,
    xml.iP_Serbia,
    xml.iP_Arberia,
    xml.iP_Epirus,
    xml.iP_Thessaly,
    xml.iP_Morea,
]
tFrankControl = [
    xml.iP_Swabia,
    xml.iP_Saxony,
    xml.iP_Lorraine,
    xml.iP_IleDeFrance,
    xml.iP_Normandy,
    xml.iP_Picardy,
    xml.iP_Aquitania,
    xml.iP_Provence,
    xml.iP_Burgundy,
    xml.iP_Orleans,
    xml.iP_Champagne,
    xml.iP_Catalonia,
    xml.iP_Lombardy,
    xml.iP_Tuscany,
]
tArabiaControlI = [
    xml.iP_Arabia,
    xml.iP_Jerusalem,
    xml.iP_Syria,
    xml.iP_Lebanon,
    xml.iP_Antiochia,
    xml.iP_Egypt,
    xml.iP_Cyrenaica,
    xml.iP_Tripolitania,
    xml.iP_Ifriqiya,
    xml.iP_Sicily,
    xml.iP_Crete,
    xml.iP_Cyprus,
]
tArabiaControlII = [
    xml.iP_Arabia,
    xml.iP_Jerusalem,
    xml.iP_Syria,
    xml.iP_Lebanon,
    xml.iP_Antiochia,
    xml.iP_Egypt,
]
tBulgariaControl = [
    xml.iP_Constantinople,
    xml.iP_Thessaloniki,
    xml.iP_Serbia,
    xml.iP_Thrace,
    xml.iP_Macedonia,
    xml.iP_Moesia,
    xml.iP_Arberia,
]
tCordobaWonders = [xml.iAlhambra, xml.iLaMezquita, xml.iGardensAlAndalus]
tCordobaIslamize = [
    xml.iP_GaliciaSpain,
    xml.iP_Castile,
    xml.iP_Leon,
    xml.iP_Lusitania,
    xml.iP_Catalonia,
    xml.iP_Aragon,
    xml.iP_Navarre,
    xml.iP_Valencia,
    xml.iP_LaMancha,
    xml.iP_Andalusia,
]
tNorwayControl = [
    xml.iP_TheIsles,
    xml.iP_Ireland,
    xml.iP_Scotland,
    xml.iP_Normandy,
    xml.iP_Sicily,
    xml.iP_Apulia,
    xml.iP_Calabria,
    xml.iP_Iceland,
]
tNorwayOutrank = [
    Consts.iSweden,
    Consts.iDenmark,
    Consts.iScotland,
    Consts.iEngland,
    Consts.iGermany,
    Consts.iFrankia,
]
# tNorseControl = [ xml.iP_Sicily, xml.iP_Iceland, xml.iP_Northumbria, xml.iP_Scotland, xml.iP_Normandy, xml.iP_Ireland, xml.iP_Novgorod ]
tVenetianControl = [xml.iP_Epirus, xml.iP_Dalmatia, xml.iP_Verona, xml.iP_Arberia]
tVenetianControlII = [xml.iP_Thessaly, xml.iP_Morea, xml.iP_Crete, xml.iP_Cyprus]
tBurgundyControl = [
    xml.iP_Flanders,
    xml.iP_Picardy,
    xml.iP_Provence,
    xml.iP_Burgundy,
    xml.iP_Champagne,
    xml.iP_Lorraine,
]
tBurgundyOutrank = [Consts.iFrankia, Consts.iEngland, Consts.iGermany]
tGermanyControl = [
    xml.iP_Tuscany,
    xml.iP_Liguria,
    xml.iP_Lombardy,
    xml.iP_Lorraine,
    xml.iP_Swabia,
    xml.iP_Saxony,
    xml.iP_Bavaria,
    xml.iP_Franconia,
    xml.iP_Brandenburg,
    xml.iP_Holstein,
]
tGermanyControlII = [
    xml.iP_Austria,
    xml.iP_Flanders,
    xml.iP_Pomerania,
    xml.iP_Silesia,
    xml.iP_Bohemia,
    xml.iP_Moravia,
    xml.iP_Swabia,
    xml.iP_Saxony,
    xml.iP_Bavaria,
    xml.iP_Franconia,
    xml.iP_Brandenburg,
    xml.iP_Holstein,
]
tKievControl = [
    xml.iP_Kiev,
    xml.iP_Podolia,
    xml.iP_Pereyaslavl,
    xml.iP_Sloboda,
    xml.iP_Chernigov,
    xml.iP_Volhynia,
    xml.iP_Minsk,
    xml.iP_Polotsk,
    xml.iP_Smolensk,
    xml.iP_Moscow,
    xml.iP_Murom,
    xml.iP_Rostov,
    xml.iP_Novgorod,
    xml.iP_Vologda,
]
tHungaryControl = [
    xml.iP_Austria,
    xml.iP_Carinthia,
    xml.iP_Moravia,
    xml.iP_Silesia,
    xml.iP_Bohemia,
    xml.iP_Dalmatia,
    xml.iP_Bosnia,
    xml.iP_Banat,
    xml.iP_Wallachia,
    xml.iP_Moldova,
]
tHungaryControlII = [
    xml.iP_Thrace,
    xml.iP_Moesia,
    xml.iP_Macedonia,
    xml.iP_Thessaloniki,
    xml.iP_Wallachia,
    xml.iP_Thessaly,
    xml.iP_Morea,
    xml.iP_Epirus,
    xml.iP_Arberia,
    xml.iP_Serbia,
    xml.iP_Banat,
    xml.iP_Bosnia,
    xml.iP_Dalmatia,
    xml.iP_Slavonia,
]
tSpainConvert = [
    xml.iP_GaliciaSpain,
    xml.iP_Castile,
    xml.iP_Leon,
    xml.iP_Lusitania,
    xml.iP_Catalonia,
    xml.iP_Aragon,
    xml.iP_Navarre,
    xml.iP_Valencia,
    xml.iP_LaMancha,
    xml.iP_Andalusia,
]
tPolishControl = [
    xml.iP_Bohemia,
    xml.iP_Moravia,
    xml.iP_UpperHungary,
    xml.iP_Prussia,
    xml.iP_Lithuania,
    xml.iP_Livonia,
    xml.iP_Polotsk,
    xml.iP_Minsk,
    xml.iP_Volhynia,
    xml.iP_Podolia,
    xml.iP_Moldova,
    xml.iP_Kiev,
]
tGenoaControl = [
    xml.iP_Corsica,
    xml.iP_Sardinia,
    xml.iP_Crete,
    xml.iP_Rhodes,
    xml.iP_Thrakesion,
    xml.iP_Cyprus,
    xml.iP_Crimea,
]
tEnglandControl = [
    xml.iP_Aquitania,
    xml.iP_London,
    xml.iP_Wales,
    xml.iP_Wessex,
    xml.iP_Scotland,
    xml.iP_EastAnglia,
    xml.iP_Mercia,
    xml.iP_Northumbria,
    xml.iP_Ireland,
    xml.iP_Normandy,
    xml.iP_Bretagne,
    xml.iP_IleDeFrance,
    xml.iP_Orleans,
    xml.iP_Picardy,
]
tPortugalControlI = [xml.iP_Azores, xml.iP_Canaries, xml.iP_Madeira]
tPortugalControlII = [xml.iP_Morocco, xml.iP_Tetouan, xml.iP_Oran]
# tLithuaniaControl = [ xml.iP_Lithuania, xml.iP_GreaterPoland, xml.iP_LesserPoland, xml.iP_Pomerania, xml.iP_Masovia, xml.iP_Brest, xml.iP_Suvalkija, xml.iP_Livonia, xml.iP_Novgorod, xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_Minsk, xml.iP_Chernigov, xml.iP_Pereyaslavl, xml.iP_Kiev, xml.iP_GaliciaPoland, xml.iP_Sloboda ]
tAustriaControl = [
    xml.iP_Hungary,
    xml.iP_UpperHungary,
    xml.iP_Austria,
    xml.iP_Carinthia,
    xml.iP_Bavaria,
    xml.iP_Transylvania,
    xml.iP_Pannonia,
    xml.iP_Moravia,
    xml.iP_Silesia,
    xml.iP_Bohemia,
]
tOttomanControlI = [
    xml.iP_Serbia,
    xml.iP_Bosnia,
    xml.iP_Banat,
    xml.iP_Macedonia,
    xml.iP_Thrace,
    xml.iP_Moesia,
    xml.iP_Constantinople,
    xml.iP_Arberia,
    xml.iP_Epirus,
    xml.iP_Thessaloniki,
    xml.iP_Thessaly,
    xml.iP_Morea,
    xml.iP_Colonea,
    xml.iP_Antiochia,
    xml.iP_Charsianon,
    xml.iP_Cilicia,
    xml.iP_Armeniakon,
    xml.iP_Anatolikon,
    xml.iP_Paphlagonia,
    xml.iP_Thrakesion,
    xml.iP_Opsikion,
    xml.iP_Syria,
    xml.iP_Lebanon,
    xml.iP_Jerusalem,
    xml.iP_Egypt,
]
tOttomanWonders = [xml.iTopkapiPalace, xml.iBlueMosque, xml.iSelimiyeMosque, xml.iTombAlWalid]
tOttomanControlII = [xml.iP_Austria, xml.iP_Pannonia, xml.iP_LesserPoland]
tMoscowControl = [
    xml.iP_Donets,
    xml.iP_Kuban,
    xml.iP_Zaporizhia,
    xml.iP_Sloboda,
    xml.iP_Kiev,
    xml.iP_Moldova,
    xml.iP_Crimea,
    xml.iP_Pereyaslavl,
    xml.iP_Chernigov,
    xml.iP_Simbirsk,
    xml.iP_NizhnyNovgorod,
    xml.iP_Vologda,
    xml.iP_Rostov,
    xml.iP_Novgorod,
    xml.iP_Karelia,
    xml.iP_Smolensk,
    xml.iP_Polotsk,
    xml.iP_Minsk,
    xml.iP_Volhynia,
    xml.iP_Podolia,
    xml.iP_Moscow,
    xml.iP_Murom,
]
# tSwedenControlI = [ xml.iP_Gotaland, xml.iP_Svealand, xml.iP_Norrland, xml.iP_Skaneland, xml.iP_Gotland, xml.iP_Osterland ]
# tSwedenControlII = [ xml.iP_Saxony, xml.iP_Brandenburg, xml.iP_Holstein, xml.iP_Pomerania, xml.iP_Prussia, xml.iP_GreaterPoland, xml.iP_Masovia, xml.iP_Suvalkija, xml.iP_Lithuania, xml.iP_Livonia, xml.iP_Estonia, xml.iP_Smolensk, xml.iP_Polotsk, xml.iP_Minsk, xml.iP_Murom, xml.iP_Chernigov, xml.iP_Moscow, xml.iP_Novgorod, xml.iP_Rostov ]
tSwedenControl = [xml.iP_Norrland, xml.iP_Osterland, xml.iP_Karelia]
tNovgorodControl = [
    xml.iP_Novgorod,
    xml.iP_Karelia,
    xml.iP_Estonia,
    xml.iP_Livonia,
    xml.iP_Rostov,
    xml.iP_Vologda,
    xml.iP_Osterland,
]
# tNovgorodControlII = [ xml.iP_Karelia, xml.iP_Vologda ]
tMoroccoControl = [
    xml.iP_Morocco,
    xml.iP_Marrakesh,
    xml.iP_Fez,
    xml.iP_Tetouan,
    xml.iP_Oran,
    xml.iP_Algiers,
    xml.iP_Ifriqiya,
    xml.iP_Andalusia,
    xml.iP_Valencia,
    xml.iP_Balears,
]
tAragonControlI = [xml.iP_Catalonia, xml.iP_Valencia, xml.iP_Balears, xml.iP_Sicily]
tAragonControlII = [
    xml.iP_Catalonia,
    xml.iP_Valencia,
    xml.iP_Aragon,
    xml.iP_Balears,
    xml.iP_Corsica,
    xml.iP_Sardinia,
    xml.iP_Sicily,
    xml.iP_Calabria,
    xml.iP_Apulia,
    xml.iP_Provence,
    xml.iP_Thessaly,
]
tPrussiaControlI = [
    xml.iP_Lithuania,
    xml.iP_Suvalkija,
    xml.iP_Livonia,
    xml.iP_Estonia,
    xml.iP_Pomerania,
    xml.iP_Prussia,
]
tPrussiaDefeat = [
    Consts.iAustria,
    Consts.iMoscow,
    Consts.iGermany,
    Consts.iSweden,
    Consts.iFrankia,
    Consts.iSpain,
]
tScotlandControl = [
    xml.iP_Scotland,
    xml.iP_TheIsles,
    xml.iP_Ireland,
    xml.iP_Wales,
    xml.iP_Bretagne,
]
tDenmarkControlI = [
    xml.iP_Denmark,
    xml.iP_Skaneland,
    xml.iP_Gotaland,
    xml.iP_Svealand,
    xml.iP_Mercia,
    xml.iP_London,
    xml.iP_EastAnglia,
    xml.iP_Northumbria,
]
# tDenmarkControlII = [ xml.iP_Brandenburg, xml.iP_Pomerania, xml.iP_Estonia ]
tDenmarkControlIII = [
    xml.iP_Denmark,
    xml.iP_Norway,
    xml.iP_Vestfold,
    xml.iP_Skaneland,
    xml.iP_Gotaland,
    xml.iP_Svealand,
    xml.iP_Norrland,
    xml.iP_Gotland,
    xml.iP_Osterland,
    xml.iP_Estonia,
    xml.iP_Iceland,
]

# tHugeHungaryControl = ( 0, 23, 99, 72 )
totalLand = gc.getMap().getLandPlots()

iCathegoryExpansion = Consts.iCathegoryExpansion


class Victory:
    def __init__(self):
        self.switchConditionsPerCiv = {
            Consts.iByzantium: self.checkByzantium,
            Consts.iFrankia: self.checkFrankia,
            Consts.iArabia: self.checkArabia,
            Consts.iBulgaria: self.checkBulgaria,
            Consts.iCordoba: self.checkCordoba,
            Consts.iVenecia: self.checkVenecia,
            Consts.iBurgundy: self.checkBurgundy,
            Consts.iGermany: self.checkGermany,
            Consts.iNovgorod: self.checkNovgorod,
            Consts.iNorway: self.checkNorway,
            Consts.iKiev: self.checkKiev,
            Consts.iHungary: self.checkHungary,
            Consts.iSpain: self.checkSpain,
            Consts.iDenmark: self.checkDenmark,
            Consts.iScotland: self.checkScotland,
            Consts.iPoland: self.checkPoland,
            Consts.iGenoa: self.checkGenoa,
            Consts.iMorocco: self.checkMorocco,
            Consts.iEngland: self.checkEngland,
            Consts.iPortugal: self.checkPortugal,
            Consts.iAragon: self.checkAragon,
            Consts.iSweden: self.checkSweden,
            Consts.iPrussia: self.checkPrussia,
            Consts.iLithuania: self.checkLithuania,
            Consts.iAustria: self.checkAustria,
            Consts.iTurkey: self.checkTurkey,
            Consts.iMoscow: self.checkMoscow,
            Consts.iDutch: self.checkDutch,
        }

    ##################################################
    ### Secure storage & retrieval of script data ###
    ################################################

    def setup(self):
        # ignore AI goals
        bIgnoreAI = gc.getDefineINT("NO_AI_UHV_CHECKS") == 1
        self.setIgnoreAI(bIgnoreAI)
        if bIgnoreAI:
            for iPlayer in range(Consts.iNumPlayers):
                if utils.getHumanID() != iPlayer:
                    self.setAllUHVFailed(iPlayer)

    def isIgnoreAI(self):
        return sd.scriptDict["bIgnoreAIUHV"]

    def setIgnoreAI(self, bVal):
        sd.scriptDict["bIgnoreAIUHV"] = bVal

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
        if not gc.getGame().isVictoryValid(7):  # 7 == historical
            return
        if not pPlayer.isAlive():
            return
        if iPlayer >= Consts.iNumMajorPlayers - 1:  # don't count the Pope
            return

        self.switchConditionsPerCiv[iPlayer](iGameTurn)

        # Generic checks:
        if not pPlayer.getUHV2of3():
            if (
                utils.countAchievedGoals(iPlayer) >= 2
            ):  # in case the last 2 goals were achieved in the same turn
                # intermediate bonus
                pPlayer.setUHV2of3(True)
                if pPlayer.getNumCities() > 0:  # this check is needed, otherwise game crashes
                    capital = pPlayer.getCapitalCity()
                    # 3Miro: Golden Age after 2/3 victories
                    capital.setHasRealBuilding(xml.iTriumphalArch, True)
                    if pPlayer.isHuman():
                        CyInterface().addMessage(
                            iPlayer,
                            False,
                            MessageData.DURATION,
                            CyTranslator().getText("TXT_KEY_VICTORY_INTERMEDIATE", ()),
                            "",
                            0,
                            "",
                            ColorTypes(MessageData.PURPLE),
                            -1,
                            -1,
                            True,
                            True,
                        )
                        for iCiv in range(Consts.iNumPlayers):
                            if iCiv != iPlayer:
                                pCiv = gc.getPlayer(iCiv)
                                if pCiv.isAlive():
                                    iAttitude = pCiv.AI_getAttitude(iPlayer)
                                    if iAttitude != 0:
                                        pCiv.AI_setAttitudeExtra(iPlayer, iAttitude - 1)

                        # Absinthe: maximum 3 of your rivals declare war on you
                        lCivs = [
                            iCiv
                            for iCiv in range(Consts.iNumPlayers - 1)
                            if iCiv != iPlayer and gc.getPlayer(iCiv).isAlive()
                        ]
                        iWarCounter = 0
                        # we run through a randomized list of all available civs
                        random.shuffle(lCivs)
                        for iCiv in lCivs:
                            pCiv = gc.getPlayer(iCiv)
                            teamCiv = gc.getTeam(pCiv.getTeam())
                            # skip civ if it's vassal (safety check for own vassals, want to look for the master for other vassals)
                            if teamCiv.isAVassal():
                                continue
                            if teamCiv.canDeclareWar(pPlayer.getTeam()):
                                # AI_getAttitude: ATTITUDE_FRIENDLY == 4, ATTITUDE_PLEASED == 3, ATTITUDE_CAUTIOUS == 2, ATTITUDE_ANNOYED == 1, ATTITUDE_FURIOUS == 0
                                if pCiv.canContact(iPlayer) and not teamCiv.isAtWar(iPlayer):
                                    iModifier = 0
                                    # bigger chance for civs which hate you
                                    if pCiv.AI_getAttitude(iPlayer) == 0:
                                        iModifier += 3
                                    elif pCiv.AI_getAttitude(iPlayer) == 1:
                                        iModifier += 1
                                    elif pCiv.AI_getAttitude(iPlayer) == 3:
                                        iModifier -= 1
                                    elif pCiv.AI_getAttitude(iPlayer) == 4:
                                        iModifier -= 3
                                    # bigger chance for close civs
                                    PlayerCapital = gc.getPlayer(iPlayer).getCapitalCity()
                                    CivCapital = gc.getPlayer(iCiv).getCapitalCity()
                                    iDistance = utils.calculateDistance(
                                        CivCapital.getX(),
                                        CivCapital.getY(),
                                        PlayerCapital.getX(),
                                        PlayerCapital.getY(),
                                    )
                                    if iDistance < 20:
                                        iModifier += 2
                                    elif iDistance < 40:
                                        iModifier += 1
                                    # bigger chance for big civs
                                    if pCiv.getNumCities() > 19:
                                        iModifier += 4
                                    elif pCiv.getNumCities() > 14:
                                        iModifier += 3
                                    elif pCiv.getNumCities() > 9:
                                        iModifier += 2
                                    elif pCiv.getNumCities() > 4:
                                        iModifier += 1
                                    print("iCiv, iModifier", iCiv, iModifier)
                                    iRndnum = gc.getGame().getSorenRandNum(7, "war chance")
                                    if iRndnum + iModifier > 6:
                                        teamCiv.declareWar(pPlayer.getTeam(), True, -1)
                                        iWarCounter += 1
                                        if iWarCounter == 3:
                                            break
                        if iWarCounter > 0:
                            CyInterface().addMessage(
                                iPlayer,
                                False,
                                MessageData.DURATION,
                                CyTranslator().getText("TXT_KEY_VICTORY_RIVAL_CIVS", ()),
                                "",
                                0,
                                "",
                                ColorTypes(MessageData.LIGHT_RED),
                                -1,
                                -1,
                                True,
                                True,
                            )

        if gc.getGame().getWinner() == -1:
            if pPlayer.getUHV(0) == 1 and pPlayer.getUHV(1) == 1 and pPlayer.getUHV(2) == 1:
                gc.getGame().setWinner(iPlayer, 7)  # Historical Victory

    def onCityBuilt(self, city, iPlayer):  # see onCityBuilt in CvRFCEventHandler
        # Portugal UHV 1: Settle 3 cities on the Azores, Canaries and Madeira and 2 in Morocco, Tetouan and Oran
        if iPlayer == Consts.iPortugal:
            if self.isPossibleUHV(iPlayer, 0, False):
                iProv = city.getProvince()
                if iProv in tPortugalControlI or iProv in tPortugalControlII:
                    iCounter = pPortugal.getUHVCounter(0)
                    iIslands = iCounter % 100
                    iAfrica = iCounter / 100
                    if iProv in tPortugalControlI:
                        iIslands += 1
                    else:
                        iAfrica += 1
                    if iIslands >= 3 and iAfrica >= 2:
                        self.wonUHV(Consts.iPortugal, 0)
                    pPortugal.setUHVCounter(0, iAfrica * 100 + iIslands)

    def onReligionFounded(self, iReligion, iFounder):
        # Germany UHV 2: Start the Reformation (Found Protestantism)
        if iReligion == xml.iProtestantism:
            if iFounder == Consts.iGermany:
                self.wonUHV(Consts.iGermany, 1)
            else:
                self.lostUHV(Consts.iGermany, 1)

    def onCityAcquired(self, owner, iNewOwner, city, bConquest, bTrade):
        if not gc.getGame().isVictoryValid(7):  # Victory 7 == historical
            return

        iPlayer = owner
        iGameTurn = gc.getGame().getGameTurn()

        # Bulgaria UHV 3: Do not lose a city to Barbarians, Mongols, Byzantines, or Ottomans before 1396
        if iPlayer == Consts.iBulgaria:
            if self.isPossibleUHV(iPlayer, 2, False):
                if iGameTurn <= xml.i1396AD:
                    if iNewOwner in [Consts.iBarbarian, Consts.iByzantium, Consts.iTurkey]:
                        # conquered and flipped cities always count
                        # for traded cities, there should be a distinction between traded in peace (gift) and traded in ending a war (peace negotiations)
                        # instead of that, we check if the civ is at peace when the trade happens
                        # TODO#BUG# unfortunately the trade deal just ending a war is taken into account as a peace deal - maybe check if there was a war in this turn, or the last couple turns?
                        if not bTrade:
                            self.lostUHV(Consts.iBulgaria, 2)
                        else:
                            bIsAtWar = False
                            for iCiv in [Consts.iByzantium, Consts.iTurkey]:
                                pCiv = gc.getPlayer(iCiv)
                                if pCiv.isAlive():
                                    if teamBulgaria.isAtWar(iCiv):
                                        bIsAtWar = True
                            if bIsAtWar:
                                self.lostUHV(Consts.iBulgaria, 2)

        # Portugal UHV 2: Do not lose a city before 1640
        elif iPlayer == Consts.iPortugal:
            if self.isPossibleUHV(iPlayer, 1, False):
                # conquered and flipped cities always count
                # for traded cities, there should be a distinction between traded in peace (gift) and traded in ending a war (peace negotiations)
                # instead of that, we check if the civ is at peace when the trade happens
                # TODO#BUG# unfortunately the trade deal just ending a war is taken into account as a peace deal - maybe check if there was a war in this turn, or the last couple turns?
                if not bTrade:
                    self.lostUHV(Consts.iPortugal, 1)
                else:
                    bIsAtWar = False
                    for iCiv in range(Consts.iNumPlayers):
                        pCiv = gc.getPlayer(iCiv)
                        if pCiv.isAlive():
                            if teamBulgaria.isAtWar(iCiv):
                                bIsAtWar = True
                    if bIsAtWar:
                        self.lostUHV(Consts.iPortugal, 1)

        # Norway UHV 1: Going Viking
        elif iNewOwner == Consts.iNorway and iGameTurn < xml.i1066AD + 2:
            # Absinthe: city is already reduced by 1 on city conquest, so city.getPopulation() is one less than the original size (unless it was already 1)
            if bConquest:
                if city.getPopulation() > 1:
                    pNorway.setUHVCounter(0, pNorway.getUHVCounter(0) + city.getPopulation() + 1)
                else:
                    pNorway.setUHVCounter(0, pNorway.getUHVCounter(0) + city.getPopulation())

        # Poland UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
        elif iNewOwner == Consts.iPoland:
            if self.isPossibleUHV(iNewOwner, 2, False):
                if city.hasBuilding(
                    xml.iKazimierz
                ):  # you cannot acquire religious buildings on conquest, only wonders
                    iCounter = pPoland.getUHVCounter(2)
                    iCathCath = (iCounter / 10000) % 10
                    iOrthCath = (iCounter / 1000) % 10
                    iProtCath = (iCounter / 100) % 10
                    iJewishQu = 99
                    iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
                    pPoland.setUHVCounter(2, iCounter)
                    if iCathCath >= 3 and iOrthCath >= 2 and iProtCath >= 2 and iJewishQu >= 2:
                        self.wonUHV(Consts.iPoland, 2)

        # Prussia UHV 2: Conquer two cities from each of Austria, Muscovy, Germany, Sweden, France and Spain between 1650 and 1763, if they are still alive
        elif iNewOwner == Consts.iPrussia:
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
                        self.wonUHV(Consts.iPrussia, 1)

                    iConqRaw = 0
                    for iI in range(len(tPrussiaDefeat)):
                        iConqRaw += lNumConq[iI] * pow(10, iI)
                    pPrussia.setUHVCounter(1, iConqRaw)

    def onCityRazed(self, iPlayer, city):
        # Sweden UHV 2: Raze 5 Catholic cities while being Protestant by 1660
        if iPlayer == Consts.iSweden:
            if self.isPossibleUHV(iPlayer, 1, False):
                if pSweden.getStateReligion() == xml.iProtestantism and city.isHasReligion(
                    xml.iCatholicism
                ):
                    iRazed = pSweden.getUHVCounter(1) + 1
                    pSweden.setUHVCounter(1, iRazed)
                    if iRazed >= 5:
                        self.wonUHV(Consts.iSweden, 1)

    def onPillageImprovement(self, iPillager, iVictim, iImprovement, iRoute, iX, iY):
        # Norway UHV 1: Going Viking
        if (
            iPillager == Consts.iNorway
            and iRoute == -1
            and gc.getGame().getGameTurn() < xml.i1066AD + 2
        ):
            if gc.getMap().plot(iX, iY).getOwner() != Consts.iNorway:
                pNorway.setUHVCounter(0, pNorway.getUHVCounter(0) + 1)

    def onCombatResult(self, argsList):
        pWinningUnit, pLosingUnit = argsList
        cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())

        # Norway UHV 1: Going Viking
        if (
            pWinningUnit.getOwner() == Consts.iNorway
            and gc.getGame().getGameTurn() < xml.i1066AD + 2
        ):
            if cLosingUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
                # Absinthe: only 1 Viking point for Work Boats
                # print ("viking", pLosingUnit.getUnitType())
                if pLosingUnit.getUnitType() != xml.iWorkboat:
                    pNorway.setUHVCounter(0, pNorway.getUHVCounter(0) + 2)
                else:
                    pNorway.setUHVCounter(0, pNorway.getUHVCounter(0) + 1)

    def onTechAcquired(self, iTech, iPlayer):
        if not gc.getGame().isVictoryValid(7):  # 7 == historical
            return

        # England UHV 3: Be the first to enter the Industrial age
        if iTech == xml.iIndustrialTech:
            if self.isPossibleUHV(Consts.iEngland, 2, False):
                if iPlayer == Consts.iEngland:
                    self.wonUHV(Consts.iEngland, 2)
                else:
                    self.lostUHV(Consts.iEngland, 2)

    def onBuildingBuilt(self, iPlayer, iBuilding):
        if not gc.getGame().isVictoryValid(7):  # 7 == historical
            return

        iGameTurn = gc.getGame().getGameTurn()

        # Kiev UHV 1: Build 2 Orthodox cathedrals and 8 Orthodox monasteries by 1250
        if iPlayer == Consts.iKiev:
            if self.isPossibleUHV(iPlayer, 0, False):
                if iBuilding in [xml.iOrthodoxMonastery, xml.iOrthodoxCathedral]:
                    iBuildSoFar = pKiev.getUHVCounter(0)
                    iCathedralCounter = iBuildSoFar % 100
                    iMonasteryCounter = iBuildSoFar / 100
                    if iBuilding == xml.iOrthodoxMonastery:
                        iMonasteryCounter += 1
                    else:
                        iCathedralCounter += 1
                    if iCathedralCounter >= 2 and iMonasteryCounter >= 8:
                        self.wonUHV(Consts.iKiev, 0)
                    pKiev.setUHVCounter(0, 100 * iMonasteryCounter + iCathedralCounter)

        # Poland UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
        # HHG: Polish UHV3 now uses Wonder Kazimierz with maximum value 99, and all other buildings have boundary checks
        elif iPlayer == Consts.iPoland:
            if self.isPossibleUHV(iPlayer, 2, False):
                lBuildingList = [
                    xml.iCatholicCathedral,
                    xml.iOrthodoxCathedral,
                    xml.iProtestantCathedral,
                    xml.iJewishQuarter,
                    xml.iKazimierz,
                ]
                if iBuilding in lBuildingList:
                    iCounter = pPoland.getUHVCounter(2)
                    iCathCath = (iCounter / 10000) % 10
                    iOrthCath = (iCounter / 1000) % 10
                    iProtCath = (iCounter / 100) % 10
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
                        self.wonUHV(Consts.iPoland, 2)
                    iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
                    pPoland.setUHVCounter(2, iCounter)

        # Cordoba UHV 2: Build the Alhambra, the Gardens of Al-Andalus, and La Mezquita by 1309
        if iBuilding in tCordobaWonders:
            if self.isPossibleUHV(Consts.iCordoba, 1, False):
                if iPlayer == Consts.iCordoba:
                    iWondersBuilt = pCordoba.getUHVCounter(1)
                    pCordoba.setUHVCounter(1, iWondersBuilt + 1)
                    if iWondersBuilt == 2:  # so we already had 2 wonders, and this is the 3rd one
                        self.wonUHV(Consts.iCordoba, 1)
                else:
                    self.lostUHV(Consts.iCordoba, 1)

        # Ottoman UHV 2: Construct the Topkapi Palace, the Blue Mosque, the Selimiye Mosque and the Tomb of Al-Walid by 1616
        if iBuilding in tOttomanWonders:
            if self.isPossibleUHV(Consts.iTurkey, 1, False):
                if iPlayer == Consts.iTurkey:
                    iWondersBuilt = pTurkey.getUHVCounter(1)
                    pTurkey.setUHVCounter(1, iWondersBuilt + 1)
                    if iWondersBuilt == 3:  # so we already had 3 wonders, and this is the 4th one
                        self.wonUHV(Consts.iTurkey, 1)
                else:
                    self.lostUHV(Consts.iTurkey, 1)

    def onProjectBuilt(self, iPlayer, iProject):
        bColony = self.isProjectAColony(iProject)
        # Absinthe: note that getProjectCount (thus getNumRealColonies too) won't count the latest project/colony (which was currently built) if called from this function
        # 			way more straightforward, and also faster to use the UHVCounters for the UHV checks

        # Venice UHV 3: Be the first to build a Colony from the Age of Discovery (Vinland is from the Viking Age)
        if self.isPossibleUHV(Consts.iVenecia, 2, False):
            if iProject != xml.iColVinland:
                if bColony:
                    if iPlayer == Consts.iVenecia:
                        self.wonUHV(Consts.iVenecia, 2)
                    else:
                        self.lostUHV(Consts.iVenecia, 2)

        # France UHV 3: Build 5 Colonies
        if iPlayer == Consts.iFrankia:
            if self.isPossibleUHV(iPlayer, 2, False):
                if bColony:
                    pFrankia.setUHVCounter(2, pFrankia.getUHVCounter(2) + 1)
                    if pFrankia.getUHVCounter(2) >= 5:
                        self.wonUHV(Consts.iFrankia, 2)

        # England UHV 2: Build 7 Colonies
        elif iPlayer == Consts.iEngland:
            if self.isPossibleUHV(iPlayer, 1, False):
                if bColony:
                    pEngland.setUHVCounter(1, pEngland.getUHVCounter(1) + 1)
                    if pEngland.getUHVCounter(1) >= 7:
                        self.wonUHV(Consts.iEngland, 1)

        # Spain UHV 2: Have more Colonies than any other nation in 1588 (while having at least 3)
        # this is only for the Main Screen counter
        elif iPlayer == Consts.iSpain:
            pSpain.setUHVCounter(1, pSpain.getUHVCounter(1) + 1)

        # Portugal UHV 3: Build 5 Colonies
        elif iPlayer == Consts.iPortugal:
            if self.isPossibleUHV(iPlayer, 2, False):
                if bColony:
                    pPortugal.setUHVCounter(2, pPortugal.getUHVCounter(2) + 1)
                    if pPortugal.getUHVCounter(2) >= 5:
                        self.wonUHV(Consts.iPortugal, 2)

        # Dutch UHV 2: Build 3 Colonies and complete both Trading Companies
        elif iPlayer == Consts.iDutch:
            if self.isPossibleUHV(iPlayer, 1, False):
                if bColony:
                    pDutch.setUHVCounter(1, pDutch.getUHVCounter(1) + 1)
                if pDutch.getUHVCounter(1) >= 3:
                    iWestCompany = teamDutch.getProjectCount(xml.iWestIndiaCompany)
                    iEastCompany = teamDutch.getProjectCount(xml.iEastIndiaCompany)
                    # if the companies are already built previously, or currently being built (one of them is the current project)
                    if iProject == xml.iWestIndiaCompany or iWestCompany >= 1:
                        if iProject == xml.iEastIndiaCompany or iEastCompany >= 1:
                            self.wonUHV(Consts.iDutch, 1)

        # Denmark UHV 3: Build 3 Colonies and complete both Trading Companies
        elif iPlayer == Consts.iDenmark:
            if self.isPossibleUHV(iPlayer, 2, False):
                if bColony:
                    pDenmark.setUHVCounter(2, pDenmark.getUHVCounter(2) + 1)
                if pDenmark.getUHVCounter(2) >= 3:
                    iWestCompany = teamDenmark.getProjectCount(xml.iWestIndiaCompany)
                    iEastCompany = teamDenmark.getProjectCount(xml.iEastIndiaCompany)
                    # if the companies are already built previously, or currently being built (one of them is the current project)
                    if iProject == xml.iWestIndiaCompany or iWestCompany == 1:
                        if iProject == xml.iEastIndiaCompany or iEastCompany == 1:
                            self.wonUHV(Consts.iDenmark, 2)

    def getOwnedLuxes(self, pPlayer):
        lBonus = [
            xml.iSheep,
            xml.iDye,
            xml.iFur,
            xml.iGems,
            xml.iGold,
            xml.iIncense,
            xml.iIvory,
            xml.iSilk,
            xml.iSilver,
            xml.iSpices,
            xml.iWine,
            xml.iHoney,
            xml.iWhale,
            xml.iAmber,
            xml.iCotton,
            xml.iCoffee,
            xml.iTea,
            xml.iTobacco,
        ]
        iCount = 0
        for iBonus in lBonus:
            iCount += pPlayer.countOwnedBonuses(iBonus)
        return iCount

    def getOwnedGrain(self, pPlayer):
        iCount = 0
        iCount += pPlayer.countOwnedBonuses(xml.iWheat)
        iCount += pPlayer.countOwnedBonuses(xml.iBarley)
        return iCount

    def isProjectAColony(self, iProject):
        if iProject >= xml.iNumNotColonies:
            return True
        else:
            return False

    def getNumRealColonies(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        tPlayer = gc.getTeam(pPlayer.getTeam())
        iCount = 0
        for iProject in range(xml.iNumNotColonies, xml.iNumProjects):
            if tPlayer.getProjectCount(iProject) > 0:
                iCount += 1
        return iCount

    def getTerritoryPercentEurope(self, iPlayer, bReturnTotal=False):
        iTotal = 0
        iCount = 0
        for (x, y) in utils.getWorldPlotsList():
            plot = gc.getMap().plot(x, y)
            if plot.isWater():
                continue
            iProvinceID = RFCEMaps.tProvinceMap[y][x]
            if iProvinceID in xml.lNotEurope:
                continue
            iTotal += 1
            if plot.getOwner() == iPlayer:
                iCount += 1
        if bReturnTotal:
            return iCount, iTotal
        return iCount

    def checkByzantium(self, iGameTurn):

        # UHV 1: Own at least 6 cities in Calabria, Apulia, Dalmatia, Verona, Lombardy, Liguria, Tuscany, Latium, Corsica, Sardinia, Sicily, Tripolitania and Ifriqiya provinces in 632
        if iGameTurn == xml.i632AD:
            if self.isPossibleUHV(Consts.iByzantium, 0, True):
                iNumCities = 0
                for iProv in tByzantiumControl:
                    iNumCities += pByzantium.getProvinceCityCount(iProv)
                if iNumCities >= 6:
                    self.wonUHV(Consts.iByzantium, 0)
                else:
                    self.lostUHV(Consts.iByzantium, 0)

        # UHV 2: Control Constantinople, Thrace, Thessaloniki, Moesia, Macedonia, Serbia, Arberia, Epirus, Thessaly, Morea, Colonea, Antiochia, Charsianon, Cilicia, Armeniakon, Anatolikon, Paphlagonia, Thrakesion and Opsikion in 1282
        elif iGameTurn == xml.i1282AD:
            if self.isPossibleUHV(Consts.iByzantium, 1, True):
                if self.checkProvincesStates(Consts.iByzantium, tByzantiumControlII):
                    self.wonUHV(Consts.iByzantium, 1)
                else:
                    self.lostUHV(Consts.iByzantium, 1)

        # UHV 3: Make Constantinople the largest and most cultured city while being the richest empire in the world in 1453
        elif iGameTurn == xml.i1453AD:
            if self.isPossibleUHV(Consts.iByzantium, 2, True):
                x, y = CIV_CAPITAL_LOCATIONS[Civ.BYZATIUM].to_tuple()
                iGold = pByzantium.getGold()
                bMost = True
                for iCiv in range(Consts.iNumPlayers):
                    if iCiv != Consts.iByzantium and gc.getPlayer(iCiv).isAlive():
                        if gc.getPlayer(iCiv).getGold() > iGold:
                            bMost = False
                            break
                if (
                    gc.isLargestCity(x, y)
                    and gc.isTopCultureCity(x, y)
                    and gc.getMap().plot(x, y).getPlotCity().getOwner() == Consts.iByzantium
                    and bMost
                ):
                    self.wonUHV(Consts.iByzantium, 2)
                else:
                    self.lostUHV(Consts.iByzantium, 2)

    def checkFrankia(self, iGameTurn):

        # UHV 1: Achieve Charlemagne's Empire by 840
        if self.isPossibleUHV(Consts.iFrankia, 0, True):
            if self.checkProvincesStates(Consts.iFrankia, tFrankControl):
                self.wonUHV(Consts.iFrankia, 0)
        if iGameTurn == xml.i840AD:
            self.expireUHV(Consts.iFrankia, 0)

        # UHV 2: Control Jerusalem in 1291
        elif iGameTurn == xml.i1291AD:
            if self.isPossibleUHV(Consts.iFrankia, 1, True):
                pJPlot = gc.getMap().plot(*CITIES[City.JERUSALEM].to_tuple())
                if pJPlot.isCity():
                    if pJPlot.getPlotCity().getOwner() == Consts.iFrankia:
                        self.wonUHV(Consts.iFrankia, 1)
                    else:
                        self.lostUHV(Consts.iFrankia, 1)
                else:
                    self.lostUHV(Consts.iFrankia, 1)

        # UHV 3: Build 5 Colonies
        # handled in the onProjectBuilt function

    def checkArabia(self, iGameTurn):

        # UHV 1: Control all territories from Tunisia to Asia Minor in 850
        if iGameTurn == xml.i850AD:
            if self.isPossibleUHV(Consts.iArabia, 0, True):
                if self.checkProvincesStates(Consts.iArabia, tArabiaControlI):
                    self.wonUHV(Consts.iArabia, 0)
                else:
                    self.lostUHV(Consts.iArabia, 0)

        # UHV 2: Control the Levant and Egypt in 1291AD while being the most advanced civilization
        elif iGameTurn == xml.i1291AD:
            if self.isPossibleUHV(Consts.iArabia, 1, True):
                iMostAdvancedCiv = utils.getMostAdvancedCiv()
                if (
                    self.checkProvincesStates(Consts.iArabia, tArabiaControlII)
                    and iMostAdvancedCiv == Consts.iArabia
                ):
                    self.wonUHV(Consts.iArabia, 1)
                else:
                    self.lostUHV(Consts.iArabia, 1)

        # UHV 3: Spread Islam to at least 35% of the population of Europe
        if self.isPossibleUHV(Consts.iArabia, 2, True):
            iPerc = gc.getGame().calculateReligionPercent(xml.iIslam)
            if iPerc >= 35:
                self.wonUHV(Consts.iArabia, 2)

    def checkBulgaria(self, iGameTurn):

        # UHV 1: Conquer Moesia, Thrace, Macedonia, Serbia, Arberia, Thessaloniki and Constantinople by 917
        if self.isPossibleUHV(Consts.iBulgaria, 0, True):
            if self.checkProvincesStates(Consts.iBulgaria, tBulgariaControl):
                self.wonUHV(Consts.iBulgaria, 0)
        if iGameTurn == xml.i917AD:
            self.expireUHV(Consts.iBulgaria, 0)

        # UHV 2: Accumulate at least 100 Orthodox Faith Points by 1259
        if self.isPossibleUHV(Consts.iBulgaria, 1, True):
            if pBulgaria.getStateReligion() == xml.iOrthodoxy:
                if pBulgaria.getFaith() >= 100:
                    self.wonUHV(Consts.iBulgaria, 1)
        if iGameTurn == xml.i1259AD:
            self.expireUHV(Consts.iBulgaria, 1)

        # UHV 3: Do not lose a city to Barbarians, Mongols, Byzantines, or Ottomans before 1396
        # Controlled in the onCityAcquired function
        elif iGameTurn == xml.i1396AD:
            if self.isPossibleUHV(Consts.iBulgaria, 2, True):
                self.wonUHV(Consts.iBulgaria, 2)

    def checkCordoba(self, iGameTurn):

        # UHV 1: Make Cordoba the largest city in the world in 961
        if iGameTurn == xml.i961AD:
            if self.isPossibleUHV(Consts.iCordoba, 0, True):
                x, y = CIV_CAPITAL_LOCATIONS[Civ.CORDOBA].to_tuple()
                if (
                    gc.isLargestCity(x, y)
                    and gc.getMap().plot(x, y).getPlotCity().getOwner() == Consts.iCordoba
                ):
                    self.wonUHV(Consts.iCordoba, 0)
                else:
                    self.lostUHV(Consts.iCordoba, 0)

        # UHV 2: Build the Alhambra, the Gardens of Al-Andalus, and La Mezquita by 1309
        # Controlled in the onBuildingBuilt function
        elif iGameTurn == xml.i1309AD:
            self.expireUHV(Consts.iCordoba, 1)

        # UHV 3: Make sure Islam is present in every city in the Iberian peninsula in 1492
        elif iGameTurn == xml.i1492AD:
            if self.isPossibleUHV(Consts.iCordoba, 2, True):
                bIslamized = True
                for iProv in tCordobaIslamize:
                    if not pCordoba.provinceIsSpreadReligion(iProv, xml.iIslam):
                        bIslamized = False
                        break
                if bIslamized:
                    self.wonUHV(Consts.iCordoba, 2)
                else:
                    self.lostUHV(Consts.iCordoba, 2)

    def checkNorway(self, iGameTurn):

        # Old UHV1: explore all water tiles
        # if ( iGameTurn == xml.i1009AD and pNorway.getUHV( 0 ) == -1 ):
        # 	if ( gc.canSeeAllTerrain( iNorway, xml.iTerrainOcean ) ):
        # 		self.wonUHV( iNorway, 0 )
        # 	else:
        # 		self.lostUHV( iNorway, 0 )

        # UHV 1: Gain 100 Viking Points and build Vinland by 1066
        # Viking points counted in the onCityAcquired, onPillageImprovement and onCombatResult functions
        if self.isPossibleUHV(Consts.iNorway, 0, True):
            if (
                pNorway.getUHVCounter(0) >= 100
                and teamNorway.getProjectCount(xml.iColVinland) >= 1
            ):
                self.wonUHV(Consts.iNorway, 0)
        if iGameTurn == xml.i1066AD:
            self.expireUHV(Consts.iNorway, 0)

        # UHV 2: Conquer The Isles, Ireland, Scotland, Normandy, Sicily, Apulia, Calabria and Iceland by 1194
        if iGameTurn <= xml.i1194AD:
            if self.isPossibleUHV(Consts.iNorway, 1, True):
                if self.checkProvincesStates(Consts.iNorway, tNorwayControl):
                    self.wonUHV(Consts.iNorway, 1)
        if iGameTurn == xml.i1194AD:
            self.expireUHV(Consts.iNorway, 1)

        # UHV 3: Have a higher score than Sweden, Denmark, Scotland, England, Germany and France in 1320
        elif iGameTurn == xml.i1320AD:
            if self.isPossibleUHV(Consts.iNorway, 2, True):
                iNorwayRank = gc.getGame().getTeamRank(Consts.iNorway)
                bIsOnTop = True
                for iTestPlayer in tNorwayOutrank:
                    if gc.getGame().getTeamRank(iTestPlayer) < iNorwayRank:
                        bIsOnTop = False
                        break
                if bIsOnTop:
                    self.wonUHV(Consts.iNorway, 2)
                else:
                    self.lostUHV(Consts.iNorway, 2)

    def checkDenmark(self, iGameTurn):

        # UHV 1: Control Denmark, Skaneland, G�taland, Svealand, Mercia, London, Northumbria and East Anglia in 1050
        if iGameTurn == xml.i1050AD:
            if self.isPossibleUHV(Consts.iDenmark, 0, True):
                if self.checkProvincesStates(Consts.iDenmark, tDenmarkControlI):
                    self.wonUHV(Consts.iDenmark, 0)
                else:
                    self.lostUHV(Consts.iDenmark, 0)

        # UHV 2: Control Denmark, Norway, Vestfold, Skaneland, G�taland, Svealand, Norrland, Gotland, �sterland, Estonia and Iceland in 1523
        elif iGameTurn == xml.i1523AD:
            if self.isPossibleUHV(Consts.iDenmark, 1, True):
                if self.checkProvincesStates(Consts.iDenmark, tDenmarkControlIII):
                    self.wonUHV(Consts.iDenmark, 1)
                else:
                    self.lostUHV(Consts.iDenmark, 1)

        # UHV 3: Build 3 Colonies and complete both Trading Companies
        # handled in the onProjectBuilt function

    def checkVenecia(self, iGameTurn):

        # UHV 1: Conquer the Adriatic by 1004
        if self.isPossibleUHV(Consts.iVenecia, 0, True):
            if self.checkProvincesStates(Consts.iVenecia, tVenetianControl):
                self.wonUHV(Consts.iVenecia, 0)
        if iGameTurn == xml.i1004AD:
            self.expireUHV(Consts.iVenecia, 0)

        # UHV 2: Conquer Constantinople, Thessaly, Morea, Crete and Cyprus by 1204
        if self.isPossibleUHV(Consts.iVenecia, 1, True):
            if pVenecia.getProvinceCurrentState(xml.iP_Constantinople) >= ProvinceStatus.CONQUER:
                if self.checkProvincesStates(Consts.iVenecia, tVenetianControlII):
                    self.wonUHV(Consts.iVenecia, 1)
        if iGameTurn == xml.i1204AD:
            self.expireUHV(Consts.iVenecia, 1)

        # UHV 3: Be the first to build a Colony from the Age of Discovery
        # UHV 3: Vinland is from the Viking Age, all other Colonies are from the Age of Discovery
        # handled in the onProjectBuilt function

    def checkBurgundy(self, iGameTurn):

        # UHV 1: Produce 12,000 culture points in your cities by 1336
        # The counter should be updated until the deadline for the challenge UHVs, even after UHV completion
        if iGameTurn < xml.i1336AD + 2:
            iCulture = pBurgundy.getUHVCounter(0) + pBurgundy.countCultureProduced()
            pBurgundy.setUHVCounter(0, iCulture)
            if self.isPossibleUHV(Consts.iBurgundy, 0, True):
                if iCulture >= 12000:
                    self.wonUHV(Consts.iBurgundy, 0)
        if iGameTurn == xml.i1336AD:
            self.expireUHV(Consts.iBurgundy, 0)

        # UHV 2: Control Burgundy, Provence, Picardy, Flanders, Champagne and Lorraine in 1376
        elif iGameTurn == xml.i1376AD:
            if self.isPossibleUHV(Consts.iBurgundy, 1, True):
                if self.checkProvincesStates(Consts.iBurgundy, tBurgundyControl):
                    self.wonUHV(Consts.iBurgundy, 1)
                else:
                    self.lostUHV(Consts.iBurgundy, 1)

        # UHV 3: Have a higher score than France, England and Germany in 1473
        elif iGameTurn == xml.i1473AD:
            if self.isPossibleUHV(Consts.iBurgundy, 2, True):
                iBurgundyRank = gc.getGame().getTeamRank(Consts.iBurgundy)
                bIsOnTop = True
                for iTestPlayer in tBurgundyOutrank:
                    if gc.getGame().getTeamRank(iTestPlayer) < iBurgundyRank:
                        bIsOnTop = False
                        break
                if bIsOnTop:
                    self.wonUHV(Consts.iBurgundy, 2)
                else:
                    self.lostUHV(Consts.iBurgundy, 2)

    def checkGermany(self, iGameTurn):

        # Old UHVs: Have most Catholic FPs in 1077 (Walk to Canossa)
        # 			Have 3 vassals

        # UHV 1: Control Lorraine, Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Lombardy, Liguria and Tuscany in 1167
        if iGameTurn == xml.i1167AD:
            if self.isPossibleUHV(Consts.iGermany, 0, True):
                if self.checkProvincesStates(Consts.iGermany, tGermanyControl):
                    self.wonUHV(Consts.iGermany, 0)
                else:
                    self.lostUHV(Consts.iGermany, 0)

        # UHV 2: Start the Reformation (Found Protestantism)
        # Controlled in the onReligionFounded function

        # UHV 3: Control Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Flanders, Pomerania, Silesia, Bohemia, Moravia and Austria in 1648
        elif iGameTurn == xml.i1648AD:
            if self.isPossibleUHV(Consts.iGermany, 2, True):
                if self.checkProvincesStates(Consts.iGermany, tGermanyControlII):
                    self.wonUHV(Consts.iGermany, 2)
                else:
                    self.lostUHV(Consts.iGermany, 2)

    def checkNovgorod(self, iGameTurn):

        # UHV 1: Control Novgorod, Karelia, Estonia, Livonia, Rostov, Vologda and Osterland in 1284
        if iGameTurn == xml.i1284AD:
            if self.isPossibleUHV(Consts.iNovgorod, 0, True):
                if self.checkProvincesStates(Consts.iNovgorod, tNovgorodControl):
                    self.wonUHV(Consts.iNovgorod, 0)
                else:
                    self.lostUHV(Consts.iNovgorod, 0)

        # UHV 2: Control eleven sources of fur by 1397
        if self.isPossibleUHV(Consts.iNovgorod, 1, True):
            if pNovgorod.countCultBorderBonuses(xml.iFur) >= 11:
                self.wonUHV(Consts.iNovgorod, 1)
        if iGameTurn == xml.i1397AD:
            self.expireUHV(Consts.iNovgorod, 1)

        # UHV 3: Control the province of Moscow or have Muscovy as a vassal in 1478
        if iGameTurn == xml.i1478AD:
            if self.isPossibleUHV(Consts.iNovgorod, 2, True):
                if pNovgorod.getProvinceCurrentState(xml.iP_Moscow) >= ProvinceStatus.CONQUER:
                    self.wonUHV(Consts.iNovgorod, 2)
                elif pMoscow.isAlive() and teamMoscow.isVassal(teamNovgorod.getID()):
                    self.wonUHV(Consts.iNovgorod, 2)
                else:
                    self.lostUHV(Consts.iNovgorod, 2)

    def checkKiev(self, iGameTurn):

        # UHV 1: Build 2 Orthodox cathedrals and 8 Orthodox monasteries by 1250
        # Controlled in the onBuildingBuilt function
        if iGameTurn == xml.i1250AD + 1:
            self.expireUHV(Consts.iKiev, 0)

        # UHV 2: Control 10 provinces out of Kiev, Podolia, Pereyaslavl, Sloboda, Chernigov, Volhynia, Minsk, Polotsk, Smolensk, Moscow, Murom, Rostov, Novgorod and Vologda in 1288
        elif iGameTurn == xml.i1288AD:
            if self.isPossibleUHV(Consts.iKiev, 1, True):
                iConq = 0
                for iProv in tKievControl:
                    if pKiev.getProvinceCurrentState(iProv) >= ProvinceStatus.CONQUER:
                        iConq += 1
                if iConq >= 10:
                    self.wonUHV(Consts.iKiev, 1)
                else:
                    self.lostUHV(Consts.iKiev, 1)

        # UHV 3: Produce 25000 food by 1300
        # The counter should be updated until the deadline for the challenge UHVs, even after UHV completion
        if iGameTurn < xml.i1300AD + 2:
            iFood = pKiev.getUHVCounter(2) + pKiev.calculateTotalYield(YieldTypes.YIELD_FOOD)
            pKiev.setUHVCounter(2, iFood)
            if self.isPossibleUHV(Consts.iKiev, 2, True):
                if iFood > 25000:
                    self.wonUHV(Consts.iKiev, 2)
        if iGameTurn == xml.i1300AD:
            self.expireUHV(Consts.iKiev, 2)

    def checkHungary(self, iGameTurn):

        # UHV 1: Control Austria, Carinthia, Moravia, Silesia, Bohemia, Dalmatia, Bosnia, Banat, Wallachia and Moldova in 1490
        if iGameTurn == xml.i1490AD:
            if self.isPossibleUHV(Consts.iHungary, 0, True):
                if self.checkProvincesStates(Consts.iHungary, tHungaryControl):
                    self.wonUHV(Consts.iHungary, 0)
                else:
                    self.lostUHV(Consts.iHungary, 0)

        # UHV 2: Allow no Ottoman cities in Europe in 1541
        elif iGameTurn == xml.i1541AD:
            if self.isPossibleUHV(Consts.iHungary, 1, True):
                bClean = True
                if pTurkey.isAlive():
                    for iProv in tHungaryControlII:
                        if pTurkey.getProvinceCityCount(iProv) > 0:
                            bClean = False
                            break
                if bClean:
                    self.wonUHV(Consts.iHungary, 1)
                else:
                    self.lostUHV(Consts.iHungary, 1)

        # UHV 3: Be the first to adopt Free Religion
        if self.isPossibleUHV(Consts.iHungary, 2, True):
            iReligiousCivic = pHungary.getCivics(4)
            if iReligiousCivic == xml.iCivicFreeReligion:
                self.wonUHV(Consts.iHungary, 2)
            else:
                for iPlayer in range(Consts.iNumMajorPlayers):
                    pPlayer = gc.getPlayer(iPlayer)
                    if pPlayer.isAlive() and pPlayer.getCivics(4) == xml.iCivicFreeReligion:
                        self.lostUHV(Consts.iHungary, 2)

    def checkSpain(self, iGameTurn):

        # UHV 1: Reconquista (make sure Catholicism is the only religion present in every city in the Iberian peninsula in 1492)
        if iGameTurn == xml.i1492AD:
            if self.isPossibleUHV(Consts.iSpain, 0, True):
                bConverted = True
                for iProv in tSpainConvert:
                    if not pSpain.provinceIsConvertReligion(iProv, xml.iCatholicism):
                        bConverted = False
                        break
                if bConverted:
                    self.wonUHV(Consts.iSpain, 0)
                else:
                    self.lostUHV(Consts.iSpain, 0)

        # UHV 2: Have more Colonies than any other nation in 1588, while having at least 3
        elif iGameTurn == xml.i1588AD:
            if self.isPossibleUHV(Consts.iSpain, 1, True):
                bMost = True
                iSpainColonies = self.getNumRealColonies(Consts.iSpain)
                for iPlayer in range(Consts.iNumPlayers):
                    if iPlayer != Consts.iSpain:
                        pPlayer = gc.getPlayer(iPlayer)
                        if (
                            pPlayer.isAlive()
                            and self.getNumRealColonies(iPlayer) >= iSpainColonies
                        ):
                            bMost = False
                if bMost and iSpainColonies >= 3:
                    self.wonUHV(Consts.iSpain, 1)
                else:
                    self.lostUHV(Consts.iSpain, 1)

        # UHV 3: Ensure that Catholic nations have more population and more land than any other religion in 1648
        elif iGameTurn == xml.i1648AD:
            if self.isPossibleUHV(Consts.iSpain, 2, True):
                if pSpain.getStateReligion() != xml.iCatholicism:
                    self.lostUHV(Consts.iSpain, 2)
                else:
                    lLand = [0, 0, 0, 0, 0, 0]  # Prot, Islam, Cath, Orth, Jew, Pagan
                    lPop = [0, 0, 0, 0, 0, 0]
                    for iPlayer in range(Consts.iNumPlayers):
                        pPlayer = gc.getPlayer(iPlayer)
                        iStateReligion = pPlayer.getStateReligion()
                        if iStateReligion > -1:
                            lLand[iStateReligion] += pPlayer.getTotalLand()
                            lPop[iStateReligion] += pPlayer.getTotalPopulation()
                        else:
                            lLand[5] += pPlayer.getTotalLand()
                            lPop[5] += pPlayer.getTotalPopulation()
                    # The Barbarian civ counts as Pagan, Independent cities are included separately, based on the religion of the population
                    pBarbarian = gc.getPlayer(Consts.iBarbarian)
                    lLand[5] += pBarbarian.getTotalLand()
                    lPop[5] += pBarbarian.getTotalPopulation()
                    for iIndyCiv in [
                        Consts.iIndependent,
                        Consts.iIndependent2,
                        Consts.iIndependent3,
                        Consts.iIndependent4,
                    ]:
                        for pCity in utils.getCityList(iIndyCiv):
                            pIndyCiv = gc.getPlayer(iIndyCiv)
                            iAverageCityLand = pIndyCiv.getTotalLand() / pIndyCiv.getNumCities()
                            if pCity.getReligionCount() == 0:
                                lLand[5] += iAverageCityLand
                                lPop[5] += pCity.getPopulation()
                            else:
                                for iReligion in range(xml.iNumReligions):
                                    if pCity.isHasReligion(iReligion):
                                        lLand[iReligion] += (
                                            iAverageCityLand / pCity.getReligionCount()
                                        )
                                        lPop[iReligion] += (
                                            pCity.getPopulation() / pCity.getReligionCount()
                                        )

                    iCathLand = lLand[xml.iCatholicism]
                    iCathPop = lPop[xml.iCatholicism]

                    bWon = True
                    for iReligion in range(xml.iNumReligions + 1):
                        if iReligion != xml.iCatholicism:
                            if lLand[iReligion] >= iCathLand:
                                bWon = False
                                break
                            if lPop[iReligion] >= iCathPop:
                                bWon = False
                                break

                    if bWon:
                        self.wonUHV(Consts.iSpain, 2)
                    else:
                        self.lostUHV(Consts.iSpain, 2)

    def checkScotland(self, iGameTurn):

        # UHV 1: Have 10 Forts and 4 Castles by 1296
        if self.isPossibleUHV(Consts.iScotland, 0, True):
            iForts = pScotland.getImprovementCount(xml.iImprovementFort)
            iCastles = pScotland.countNumBuildings(xml.iCastle)
            # print("Forts:",iForts,"Castles:",iCastles)
            if iForts >= 10 and iCastles >= 4:
                self.wonUHV(Consts.iScotland, 0)
        if iGameTurn == xml.i1296AD:
            self.expireUHV(Consts.iScotland, 0)

        # UHV 2: Have 1500 Attitude Points with France by 1560 (Attitude Points are added every turn depending on your relations)
        if self.isPossibleUHV(Consts.iScotland, 1, True):
            if pFrankia.isAlive():
                # Being at war with France gives a big penalty (and ignores most bonuses!)
                if teamScotland.isAtWar(Consts.iFrankia):
                    iScore = -10
                else:
                    # -1 for Furious 0 for Annoyed 1 for Cautious 2 for Pleased 3 for Friendly
                    iScore = pFrankia.AI_getAttitude(Consts.iScotland) - 1
                    # Agreements
                    if teamFrankia.isOpenBorders(Consts.iScotland):
                        iScore += 1
                    if teamFrankia.isDefensivePact(Consts.iScotland):
                        iScore += 2
                    # Imports/Exports
                    iTrades = 0
                    iTrades += pScotland.getNumTradeBonusImports(Consts.iFrankia)
                    iTrades += pFrankia.getNumTradeBonusImports(Consts.iScotland)
                    iScore += iTrades / 2
                    # Common Wars
                    for iEnemy in xrange(Consts.iNumPlayers):
                        if iEnemy in [Consts.iScotland, Consts.iFrankia]:
                            continue
                        if teamFrankia.isAtWar(iEnemy) and teamScotland.isAtWar(iEnemy):
                            iScore += 2
                # Different religion from France also gives a penalty, same religion gives a bonus (but only if both have a state religion)
                iScotStateReligion = pScotland.getStateReligion()
                iFraStateReligion = pFrankia.getStateReligion()
                if iScotStateReligion != -1 and iFraStateReligion != -1:
                    if iScotStateReligion != iFraStateReligion:
                        iScore -= 3
                    elif iScotStateReligion == iFraStateReligion:
                        iScore += 1
                iOldScore = pScotland.getUHVCounter(1)
                iNewScore = iOldScore + iScore
                pScotland.setUHVCounter(1, iNewScore)
                if iNewScore >= 1500:
                    self.wonUHV(Consts.iScotland, 1)
        if iGameTurn == xml.i1560AD:
            self.expireUHV(Consts.iScotland, 1)

        # UHV 3: Control Scotland, The Isles, Ireland, Wales, Brittany and Galicia in 1700
        elif iGameTurn == xml.i1700AD:
            if self.isPossibleUHV(Consts.iScotland, 2, True):
                if self.checkProvincesStates(Consts.iScotland, tScotlandControl):
                    self.wonUHV(Consts.iScotland, 2)
                else:
                    self.lostUHV(Consts.iScotland, 2)

    def checkPoland(self, iGameTurn):

        # Old UHVs: Don't lose cities until 1772 or conquer Russia until 1772
        # 			Vassalize Russia, Germany and Austria

        # UHV 1: Food production between 1500 and 1520
        if xml.i1500AD <= iGameTurn <= xml.i1520AD:
            if self.isPossibleUHV(Consts.iPoland, 0, True):
                iAgriculturePolish = pPoland.calculateTotalYield(YieldTypes.YIELD_FOOD)
                bFood = True
                for iPlayer in range(Consts.iNumMajorPlayers):
                    if (
                        gc.getPlayer(iPlayer).calculateTotalYield(YieldTypes.YIELD_FOOD)
                        > iAgriculturePolish
                    ):
                        bFood = False
                        break
                if bFood:
                    self.wonUHV(Consts.iPoland, 0)
        if iGameTurn == xml.i1520AD + 1:
            self.expireUHV(Consts.iPoland, 0)

        # UHV 2: Own at least 12 cities in the given provinces in 1569
        elif iGameTurn == xml.i1569AD:
            if self.isPossibleUHV(Consts.iPoland, 1, True):
                iNumCities = 0
                for iProv in tPolishControl:
                    iNumCities += pPoland.getProvinceCityCount(iProv)
                if iNumCities >= 12:
                    self.wonUHV(Consts.iPoland, 1)
                else:
                    self.lostUHV(Consts.iPoland, 1)

        # UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
        # Controlled in the onBuildingBuilt and onCityAcquired functions

    def checkGenoa(self, iGameTurn):

        # UHV 1: Control Corsica, Sardinia, Crete, Rhodes, Thrakesion, Cyprus and Crimea in 1400
        if iGameTurn == xml.i1400AD:
            if self.isPossibleUHV(Consts.iGenoa, 0, True):
                if self.checkProvincesStates(Consts.iGenoa, tGenoaControl):
                    self.wonUHV(Consts.iGenoa, 0)
                else:
                    self.lostUHV(Consts.iGenoa, 0)

        # UHV 2: Have the largest total amount of commerce from foreign Trade Route Exports and Imports in 1566
        # UHV 2: Export is based on your cities' trade routes with foreign cities, import is based on foreign cities' trade routes with your cities
        elif iGameTurn == xml.i1566AD:
            if self.isPossibleUHV(Consts.iGenoa, 1, True):
                iGenoaTrade = pGenoa.calculateTotalImports(
                    YieldTypes.YIELD_COMMERCE
                ) + pGenoa.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                bLargest = True
                for iPlayer in range(Consts.iNumMajorPlayers):
                    if iPlayer != Consts.iGenoa:
                        pPlayer = gc.getPlayer(iPlayer)
                        if (
                            pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
                            + pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                            > iGenoaTrade
                        ):
                            bLargest = False
                            break
                if bLargest:
                    self.wonUHV(Consts.iGenoa, 1)
                else:
                    self.lostUHV(Consts.iGenoa, 1)

        # UHV 3: Have 8 Banks and own all Bank of St. George cities in 1625
        elif iGameTurn == xml.i1625AD:
            if self.isPossibleUHV(Consts.iGenoa, 2, True):
                iBanks = 0
                for city in utils.getCityList(Consts.iGenoa):
                    if (
                        city.getNumRealBuilding(xml.iBank) > 0
                        or city.getNumRealBuilding(xml.iGenoaBank) > 0
                        or city.getNumRealBuilding(xml.iEnglishRoyalExchange) > 0
                    ):
                        iBanks += 1
                iCompanyCities = pGenoa.countCorporations(xml.iStGeorge)
                if iBanks >= 8 and iCompanyCities == xml.tCompaniesLimit[xml.iStGeorge]:
                    self.wonUHV(Consts.iGenoa, 2)
                else:
                    self.lostUHV(Consts.iGenoa, 2)

    def checkMorocco(self, iGameTurn):

        # UHV 1: Control Morocco, Marrakesh, Fez, Tetouan, Oran, Algiers, Ifriqiya, Andalusia, Valencia and the Balearic Islands in 1248
        if iGameTurn == xml.i1248AD:
            if self.isPossibleUHV(Consts.iMorocco, 0, True):
                if self.checkProvincesStates(Consts.iMorocco, tMoroccoControl):
                    self.wonUHV(Consts.iMorocco, 0)
                else:
                    self.lostUHV(Consts.iMorocco, 0)

        # UHV 2: Have 5000 culture in each of three cities in 1465
        elif iGameTurn == xml.i1465AD:
            if self.isPossibleUHV(Consts.iMorocco, 1, True):
                iGoodCities = 0
                for city in utils.getCityList(Consts.iMorocco):
                    if city.getCulture(Consts.iMorocco) >= 5000:
                        iGoodCities += 1
                if iGoodCities >= 3:
                    self.wonUHV(Consts.iMorocco, 1)
                else:
                    self.lostUHV(Consts.iMorocco, 1)

        # UHV 3: Destroy or vassalize Portugal, Spain, and Aragon by 1578
        if xml.i1164AD <= iGameTurn <= xml.i1578AD:
            if self.isPossibleUHV(Consts.iMorocco, 2, True):
                bConq = True
                if pSpain.isAlive() and not teamSpain.isVassal(teamMorocco.getID()):
                    bConq = False
                elif pPortugal.isAlive() and not teamPortugal.isVassal(teamMorocco.getID()):
                    bConq = False
                elif pAragon.isAlive() and not teamAragon.isVassal(teamMorocco.getID()):
                    bConq = False

                if bConq:
                    self.wonUHV(Consts.iMorocco, 2)
        if iGameTurn == xml.i1578AD + 1:
            self.expireUHV(Consts.iMorocco, 2)

    def checkEngland(self, iGameTurn):

        # UHV 1: Control London, Wessex, East Anglia, Mercia, Northumbria, Scotland, Wales, Ireland, Normandy, Picardy, Bretagne, Il-de-France, Aquitania and Orleans in 1452
        if iGameTurn == xml.i1452AD:
            if self.isPossibleUHV(Consts.iEngland, 0, True):
                if self.checkProvincesStates(Consts.iEngland, tEnglandControl):
                    self.wonUHV(Consts.iEngland, 0)
                else:
                    self.lostUHV(Consts.iEngland, 0)

        # UHV 2: Build 7 Colonies
        # Controlled in the onProjectBuilt function

        # UHV 3: Be the first to enter the Industrial age
        # Controlled in the onTechAcquired function

    def checkPortugal(self, iGameTurn):

        # UHV 1: Settle 3 cities on the Azores, Canaries and Madeira and 2 in Morocco, Tetouan and Oran
        # Controlled in the onCityBuilt function

        # UHV 2: Do not lose a city before 1640
        # Controlled in the onCityAcquired function
        if iGameTurn == xml.i1640AD:
            if self.isPossibleUHV(Consts.iPortugal, 1, True):
                self.wonUHV(Consts.iPortugal, 1)

        # UHV 3: Build 5 Colonies
        # Controlled in the onProjectBuilt function

    def checkAragon(self, iGameTurn):

        # UHV 1: Control Catalonia, Valencia, Balears and Sicily in 1282
        if iGameTurn == xml.i1282AD:
            if self.isPossibleUHV(Consts.iAragon, 0, True):
                if self.checkProvincesStates(Consts.iAragon, tAragonControlI):
                    self.wonUHV(Consts.iAragon, 0)
                else:
                    self.lostUHV(Consts.iAragon, 0)

        # UHV 2: Have 12 Consulates of the Sea and 30 Trade Ships in 1444
        # UHV 2: Ships with at least one cargo space count as Trade Ships
        elif iGameTurn == xml.i1444AD:
            if self.isPossibleUHV(Consts.iAragon, 1, True):
                iPorts = pAragon.countNumBuildings(xml.iAragonSeaport)
                iCargoShips = utils.getCargoShips(Consts.iAragon)
                # print("Ports:",iPorts)
                if iPorts >= 12 and iCargoShips >= 30:
                    self.wonUHV(Consts.iAragon, 1)
                else:
                    self.lostUHV(Consts.iAragon, 1)

        # UHV 3: Control Catalonia, Valencia, Aragon, Balears, Corsica, Sardinia, Sicily, Calabria, Apulia, Provence and Thessaly in 1474
        elif iGameTurn == xml.i1474AD:
            if self.isPossibleUHV(Consts.iAragon, 2, True):
                if self.checkProvincesStates(Consts.iAragon, tAragonControlII):
                    self.wonUHV(Consts.iAragon, 2)
                else:
                    self.lostUHV(Consts.iAragon, 2)

    def checkPrussia(self, iGameTurn):

        # UHV 1: Control Prussia, Suvalkija, Lithuania, Livonia, Estonia, and Pomerania in 1410
        if iGameTurn == xml.i1410AD:
            if self.isPossibleUHV(Consts.iPrussia, 0, True):
                if self.checkProvincesStates(Consts.iPrussia, tPrussiaControlI):
                    self.wonUHV(Consts.iPrussia, 0)
                else:
                    self.lostUHV(Consts.iPrussia, 0)

        # UHV 2: Conquer two cities from each of Austria, Muscovy, Germany, Sweden, France and Spain between 1650 and 1763, if they are still alive
        # Controlled in the onCityAcquired function
        if iGameTurn == xml.i1763AD + 1:
            self.expireUHV(Consts.iPrussia, 1)

        # UHV 3: Settle a total of 15 Great People in your capital
        # UHV 3: Great People can be settled in any combination, Great Generals included
        if self.isPossibleUHV(Consts.iPrussia, 2, True):
            pCapital = pPrussia.getCapitalCity()
            iGPStart = gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST")
            iGPEnd = gc.getInfoTypeForString("SPECIALIST_GREAT_SPY")
            iGPeople = 0
            for iType in range(iGPStart, iGPEnd + 1):
                iGPeople += pCapital.getFreeSpecialistCount(iType)
            if iGPeople >= 15:
                self.wonUHV(Consts.iPrussia, 2)

    def checkLithuania(self, iGameTurn):

        # UHV 1: Accumulate 2500 Culture points without declaring a state religion before 1386
        # The counter should be updated until the deadline for the challenge UHVs, even after UHV completion
        if iGameTurn < xml.i1386AD + 2:
            iCulture = pLithuania.getUHVCounter(0) + pLithuania.countCultureProduced()
            pLithuania.setUHVCounter(0, iCulture)
            if self.isPossibleUHV(Consts.iLithuania, 0, True):
                if pLithuania.getStateReligion() != -1:
                    self.lostUHV(Consts.iLithuania, 0)
                else:
                    if iCulture >= 2500:
                        self.wonUHV(Consts.iLithuania, 0)
        if iGameTurn == xml.i1386AD:
            self.expireUHV(Consts.iLithuania, 0)

        # UHV 2: Control the most territory in Europe in 1430
        elif iGameTurn == xml.i1430AD:
            if self.isPossibleUHV(Consts.iLithuania, 1, True):
                bMost = True
                iCount = self.getTerritoryPercentEurope(Consts.iLithuania)
                for iOtherPlayer in range(Consts.iNumPlayers):
                    if (
                        not gc.getPlayer(iOtherPlayer).isAlive()
                        or iOtherPlayer == Consts.iLithuania
                    ):
                        continue
                    iOtherCount = self.getTerritoryPercentEurope(iOtherPlayer)
                    if iOtherCount >= iCount:
                        bMost = False
                        break
                if bMost:
                    self.wonUHV(Consts.iLithuania, 1)
                else:
                    self.lostUHV(Consts.iLithuania, 1)

        # UHV 3: Destroy or Vassalize Muscovy, Novgorod and Prussia by 1795
        if xml.i1380AD <= iGameTurn <= xml.i1795AD:
            if self.isPossibleUHV(Consts.iLithuania, 2, True):
                bConq = True
                if pMoscow.isAlive() and not teamMoscow.isVassal(teamLithuania.getID()):
                    bConq = False
                elif pNovgorod.isAlive() and not teamNovgorod.isVassal(teamLithuania.getID()):
                    bConq = False
                elif pPrussia.isAlive() and not teamPrussia.isVassal(teamLithuania.getID()):
                    bConq = False

                if bConq:
                    self.wonUHV(Consts.iLithuania, 2)
        if iGameTurn == xml.i1795AD + 1:
            self.expireUHV(Consts.iLithuania, 2)

    def checkAustria(self, iGameTurn):

        # UHV 1: Control all of medieval Austria, Hungary and Bohemia in 1617
        if iGameTurn == xml.i1617AD:
            if self.isPossibleUHV(Consts.iAustria, 0, True):
                if self.checkProvincesStates(Consts.iAustria, tAustriaControl):
                    self.wonUHV(Consts.iAustria, 0)
                else:
                    self.lostUHV(Consts.iAustria, 0)

        # UHV 2: Have 3 vassals in 1700
        elif iGameTurn == xml.i1700AD:
            if self.isPossibleUHV(Consts.iAustria, 1, True):
                iCount = 0
                for iPlayer in range(Consts.iNumMajorPlayers):
                    if iPlayer == Consts.iAustria:
                        continue
                    pPlayer = gc.getPlayer(iPlayer)
                    if pPlayer.isAlive():
                        if gc.getTeam(pPlayer.getTeam()).isVassal(teamAustria.getID()):
                            iCount += 1
                if iCount >= 3:
                    self.wonUHV(Consts.iAustria, 1)
                else:
                    self.lostUHV(Consts.iAustria, 1)

        # UHV 3: Have the highest score in 1780
        elif iGameTurn == xml.i1780AD:
            if self.isPossibleUHV(Consts.iAustria, 2, True):
                if gc.getGame().getTeamRank(Consts.iAustria) == 0:
                    self.wonUHV(Consts.iAustria, 2)
                else:
                    self.lostUHV(Consts.iAustria, 2)

    def checkTurkey(self, iGameTurn):

        # UHV 1: Control Constantinople, the Balkans, Anatolia, the Levant and Egypt in 1517
        if iGameTurn == xml.i1517AD:
            if self.isPossibleUHV(Consts.iTurkey, 0, True):
                if self.checkProvincesStates(Consts.iTurkey, tOttomanControlI):
                    self.wonUHV(Consts.iTurkey, 0)
                else:
                    self.lostUHV(Consts.iTurkey, 0)

        # UHV 2: Construct the Topkapi Palace, the Blue Mosque, the Selimiye Mosque and the Tomb of Al-Walid by 1616
        # Controlled in the onBuildingBuilt function
        elif iGameTurn == xml.i1616AD:
            self.expireUHV(Consts.iTurkey, 1)

        # UHV 3: Conquer Austria, Pannonia and Lesser Poland by 1683
        if self.isPossibleUHV(Consts.iTurkey, 2, True):
            if self.checkProvincesStates(Consts.iTurkey, tOttomanControlII):
                self.wonUHV(Consts.iTurkey, 2)
        if iGameTurn == xml.i1683AD:
            self.expireUHV(Consts.iTurkey, 2)

    def checkMoscow(self, iGameTurn):

        # UHV 1: Free Eastern Europe from the Mongols (Make sure there are no Mongol (or any other Barbarian) cities in Russia and Ukraine in 1482)
        if iGameTurn == xml.i1482AD:
            if self.isPossibleUHV(Consts.iMoscow, 0, True):
                bClean = True
                for iProv in tMoscowControl:
                    if pBarbarian.getProvinceCityCount(iProv) > 0:
                        bClean = False
                        break
                if bClean:
                    self.wonUHV(Consts.iMoscow, 0)
                else:
                    self.lostUHV(Consts.iMoscow, 0)

        # UHV 2: Control at least 25% of Europe
        if self.isPossibleUHV(Consts.iMoscow, 1, True):
            totalLand = gc.getMap().getLandPlots()
            RussianLand = pMoscow.getTotalLand()
            if totalLand > 0:
                landPercent = (RussianLand * 100.0) / totalLand
            else:
                landPercent = 0.0
            if landPercent >= 25:
                self.wonUHV(Consts.iMoscow, 1)

        # UHV 3: Get into warm waters (Conquer Constantinople or control an Atlantic Access resource)
        if self.isPossibleUHV(Consts.iMoscow, 2, True):
            if pMoscow.countCultBorderBonuses(xml.iAccess) > 0:
                self.wonUHV(Consts.iMoscow, 2)
            elif (
                gc.getMap()
                .plot(*CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM].to_tuple())
                .getPlotCity()
                .getOwner()
                == Consts.iMoscow
            ):
                self.wonUHV(Consts.iMoscow, 2)

    def checkSweden(self, iGameTurn):

        # Old UHVs: Conquer Gotaland, Svealand, Norrland, Skaneland, Gotland and Osterland in 1600
        # 			Don't lose any cities to Poland, Lithuania or Russia before 1700
        # 			Have 15 cities in Saxony, Brandenburg, Holstein, Pomerania, Prussia, Greater Poland, Masovia, Suvalkija, Lithuania, Livonia, Estonia, Smolensk, Polotsk, Minsk, Murom, Chernigov, Moscow, Novgorod and Rostov in 1750

        # UHV 1: Have six cities in Norrland, Osterland and Karelia in 1323
        if iGameTurn == xml.i1323AD:
            if self.isPossibleUHV(Consts.iSweden, 0, True):
                iNumCities = 0
                for iProv in tSwedenControl:
                    iNumCities += pSweden.getProvinceCityCount(iProv)
                if iNumCities >= 6:
                    self.wonUHV(Consts.iSweden, 0)
                else:
                    self.lostUHV(Consts.iSweden, 0)

        # UHV 2: Raze 5 Catholic cities while being Protestant by 1660
        # Controlled in the onCityRazed function
        elif iGameTurn == xml.i1660AD:
            self.expireUHV(Consts.iSweden, 1)

        # UHV 3: Control every coastal city on the Baltic Sea in 1750
        elif iGameTurn == xml.i1750AD:
            if self.isPossibleUHV(Consts.iSweden, 2, True):
                if up.getNumForeignCitiesOnBaltic(Consts.iSweden, True) > 0:
                    self.lostUHV(Consts.iSweden, 2)
                else:
                    self.wonUHV(Consts.iSweden, 2)

    def checkDutch(self, iGameTurn):

        # UHV 1: Settle 5 Great Merchants in Amsterdam by 1750
        if self.isPossibleUHV(Consts.iDutch, 0, True):
            pPlot = gc.getMap().plot(*CIV_CAPITAL_LOCATIONS[Civ.DUTCH].to_tuple())
            if pPlot.isCity():
                city = pPlot.getPlotCity()
                if (
                    city.getFreeSpecialistCount(xml.iSpecialistGreatMerchant) >= 5
                    and city.getOwner() == Consts.iDutch
                ):
                    self.wonUHV(Consts.iDutch, 0)
        if iGameTurn == xml.i1750AD:
            self.expireUHV(Consts.iDutch, 0)

        # UHV 2: Build 3 Colonies and complete both Trading Companies
        # Controlled in the onProjectBuilt function

        # UHV 3: Become the richest country in Europe
        if self.isPossibleUHV(Consts.iDutch, 2, True):
            iGold = pDutch.getGold()
            bMost = True
            for iCiv in range(Consts.iNumPlayers):
                if iCiv == Consts.iDutch:
                    continue
                pPlayer = gc.getPlayer(iCiv)
                if pPlayer.isAlive():
                    if pPlayer.getGold() > iGold:
                        bMost = False
                        break
            if bMost:
                self.wonUHV(Consts.iDutch, 2)

    def checkProvincesStates(self, iPlayer, tProvinces):
        pPlayer = gc.getPlayer(iPlayer)
        for iProv in tProvinces:
            if pPlayer.getProvinceCurrentState(iProv) < ProvinceStatus.CONQUER:
                return False
        return True

    def wonUHV(self, iCiv, iUHV):
        pCiv = gc.getPlayer(iCiv)
        pCiv.setUHV(iUHV, 1)
        pCiv.changeStabilityBase(iCathegoryExpansion, 3)
        if utils.getHumanID() == iCiv:
            if iUHV == 0:
                sText = "first"
            elif iUHV == 1:
                sText = "second"
            elif iUHV == 2:
                sText = "third"
            popup = Popup.PyPopup()
            popup.setBodyString(localText.getText("TXT_KEY_VICTORY_UHV_GOAL_WON", (sText,)))
            popup.launch()

    def lostUHV(self, iCiv, iUHV):
        pCiv = gc.getPlayer(iCiv)
        pCiv.setUHV(iUHV, 0)
        if utils.getHumanID() == iCiv:
            if iUHV == 0:
                sText = "first"
            elif iUHV == 1:
                sText = "second"
            elif iUHV == 2:
                sText = "third"
            popup = Popup.PyPopup()
            popup.setBodyString(localText.getText("TXT_KEY_VICTORY_UHV_GOAL_LOST", (sText,)))
            popup.launch()

    def setAllUHVFailed(self, iCiv):
        pPlayer = gc.getPlayer(iCiv)
        for i in range(3):
            pPlayer.setUHV(i, 0)

    def switchUHV(self, iNewCiv, iOldCiv):
        pPlayer = gc.getPlayer(iNewCiv)
        for i in range(3):
            pPlayer.setUHV(i, -1)
        if self.isIgnoreAI():
            self.setAllUHVFailed(iOldCiv)

    def isPossibleUHV(self, iCiv, iUHV, bAlreadyAIChecked):
        pCiv = gc.getPlayer(iCiv)
        if pCiv.getUHV(iUHV) != -1:
            return False
        if not pCiv.isAlive():
            return False

        if not bAlreadyAIChecked:
            if (
                iCiv != utils.getHumanID() and self.isIgnoreAI()
            ):  # Skip calculations if no AI UHV option is enabled
                return False

        return True

    def expireUHV(self, iCiv, iUHV):
        # UHVs have to expire on the given deadline, even if the civ is not alive currently (would be an issue on respawns otherwise)
        # if self.isPossibleUHV(iCiv, iUHV, True):
        pCiv = gc.getPlayer(iCiv)
        if pCiv.getUHV(iUHV) == -1:
            self.lostUHV(iCiv, iUHV)

    def set1200UHVDone(self, iCiv):
        if iCiv == Consts.iByzantium:
            pByzantium.setUHV(0, 1)
        elif iCiv == Consts.iFrankia:
            pFrankia.setUHV(0, 1)
        elif iCiv == Consts.iArabia:
            pArabia.setUHV(0, 1)
        elif iCiv == Consts.iBulgaria:
            pBulgaria.setUHV(0, 1)
        elif iCiv == Consts.iVenecia:  # Venice gets conquerors near Constantinople for 2nd UHV
            pVenecia.setUHV(0, 1)
        elif iCiv == Consts.iGermany:
            pGermany.setUHV(0, 1)
        elif iCiv == Consts.iNorway:
            pNorway.setUHV(0, 1)
        elif iCiv == Consts.iDenmark:
            pDenmark.setUHV(0, 1)
        elif iCiv == Consts.iScotland:
            pScotland.setUHVCounter(1, 100)
